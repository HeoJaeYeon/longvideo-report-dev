#!/usr/bin/env python3
"""
Offline pre-indexing of WorldMM episodic memory (one HippoRAG graph per granularity)
for the report framework.

The retrieval service later loads these persistent caches, so serving needs no
OpenIE LLM calls. No existing repo file is modified:
  - LabeledEpisodicMemory subclasses WorldMM's EpisodicMemory only to pass an
    llm_name label to HippoRAG (upstream leaves it at the default "gpt-5-mini").
  - 10sec OpenIE results from WorldMM preprocessing are written into HippoRAG's
    cache format ("seeding"), so only the remaining chunks need LLM calls.
    Seeding is used only when the indexing LLM equals the preprocessing LLM.

OpenIE LLM (decision 1 = A): with --llm-endpoints the OpenIE calls go over HTTP to one
or more local_llm_server.py processes (round-robin), so this process only loads the
embedding model. The request is equivalent to WorldMM's in-process call: same chat
messages, max_new_tokens=2048 (Qwen3VLModel default), no sampling override (model
generation_config), same JSON parsing (Qwen3VLModel._parse_structured_response) and the
same retry depth (3 here x 5 in OpenIE). Without --llm-endpoints the LLM is loaded
in-process as before.

Long passages (2026-10-22, see REPORT_ISSUES_AND_FIXES.md): Qwen3-VL OpenIE outputs on
10min captions (up to 2,048 tokens, some truncated at generation) often exceed the
2,048-token output cap -> truncated JSON -> up to 15 retries per chunk. Passages above
SPLIT_MIN_TOKENS are therefore OpenIE'd in paragraph pieces (<= SPLIT_PIECE_TOKENS, WorldMM
OpenIE.ner/triple_extraction per piece), merged per chunk and written into the HippoRAG
cache like seeding (graph structure unchanged: one passage node per chunk). HTTP path only:
a response that fails to parse keeps its complete, well-formed list items (else the usual
retry); triple runs of one (subject, predicate) longer than MAX_SAME_SUBJ_PRED_RUN are cut;
salvaged entity lists are capped at MAX_SALVAGED_ENTITIES. Counts go to the log/done marker.

Usage:
  python prebuild_episodic_index.py --config config.yaml --dry-run      # no model load, writes nothing
  ./run_prebuild.sh <GPU_ID> [--videos a,b] [--shard 0/4]               # real run (/opt/venv, GPU)
  ./run_prebuild.sh <GPU_ID> --llm-endpoints http://127.0.0.1:18710/v1,http://127.0.0.1:18711/v1 \
      --gpu-mem-cap-mib 19000                                            # HTTP OpenIE (decision 1 = A)
"""

import argparse
import hashlib
import json
import logging
import os
import re
import sys
import time
from typing import Any, Dict, List, Tuple

import yaml

logger = logging.getLogger("prebuild")

# Long-passage OpenIE (thresholds from the 2026-10-22 runs: 0 truncated outputs in 333 calls on
# passages <= 1,025 tokens; all truncations on 10min passages of 1,733-2,048 tokens).
SPLIT_MIN_TOKENS = 1100
SPLIT_PIECE_TOKENS = 700
TOKENIZER_REPO = "Qwen/Qwen3-VL-8B-Instruct"   # tokenizer of the OpenIE LLM (qwen3vl-8b), token counts only
# Output guards (HTTP path). Observed runs of one (subject, predicate): legitimate <= 14, runaway 39-115.
MAX_SAME_SUBJ_PRED_RUN = 15
MAX_SALVAGED_ENTITIES = 100
_tokenizer = None


def load_json(path: str) -> Any:
    with open(path, "r", encoding="utf-8") as f:
        return json.load(f)


def chunk_id(text: str) -> str:
    """Same key as HippoRAG chunk store / OpenIE ("chunk-" + md5)."""
    return "chunk-" + hashlib.md5(text.encode()).hexdigest()


def caption_end_ts(entry: Dict[str, Any]) -> int:
    """Same as WorldMM CaptionEntry.timestamp_int[1]."""
    day = str(entry.get("date", "")).replace("DAY", "").replace("Day", "")
    return int(day + str(entry.get("end_time", "")).zfill(8))


def indexed_texts(caption_file: str, query_time: int) -> List[str]:
    """Texts EpisodicMemory.index(query_time) hands to HippoRAG for one granularity."""
    return [str(e.get("text", "")) for e in load_json(caption_file) if caption_end_ts(e) <= query_time]


def openie_cache_path(cache_root: str, video_id: str, granularity: str, label: str) -> str:
    """HippoRAG.openie_results_path for save_dir = {cache_root}/{vid}/episodic_memory/{g}."""
    return os.path.join(cache_root, video_id, "episodic_memory", granularity,
                        f"openie_results_ner_{label.replace('/', '_')}.json")


def cached_openie_keys(path: str) -> set:
    if not os.path.isfile(path):
        return set()
    return {chunk_id(d["passage"]) for d in load_json(path).get("docs", [])}


def build_seed_docs(texts: List[str], metadata_openie: Dict[str, Any]) -> List[Dict[str, Any]]:
    """
    Convert WorldMM preprocessing OpenIE ({ner_results, triple_results}) into HippoRAG
    docs. Only passages present in `texts` are included (HippoRAG.index asserts
    #chunks == #openie entries), deduplicated by hash. Empty triple lists are not
    seeded: they cannot be told apart from swallowed OpenIE errors, so HippoRAG
    recomputes them.
    """
    ner, triples = metadata_openie["ner_results"], metadata_openie["triple_results"]
    docs, seen = [], set()
    for text in texts:
        key = chunk_id(text)
        if key in seen or not triples.get(key):
            continue
        seen.add(key)
        docs.append({"idx": key, "passage": text,
                     "extracted_entities": ner.get(key, []),
                     "extracted_triples": triples[key]})
    return docs


def count_tokens(text: str) -> int:
    """Token count with the OpenIE LLM's tokenizer (tokenizers only: dry-run must not import torch)."""
    global _tokenizer
    if _tokenizer is None:
        from huggingface_hub import try_to_load_from_cache
        from tokenizers import Tokenizer
        path = try_to_load_from_cache(TOKENIZER_REPO, "tokenizer.json")
        if not isinstance(path, str):
            raise FileNotFoundError(f"tokenizer.json of {TOKENIZER_REPO} not in the HF cache (HF_HOME={os.environ.get('HF_HOME')})")
        _tokenizer = Tokenizer.from_file(path)
    return len(_tokenizer.encode(text, add_special_tokens=False).ids)


def split_passage(text: str, budget: int = SPLIT_PIECE_TOKENS) -> List[str]:
    """Pack blank-line paragraphs (sentences for an over-long paragraph) into pieces of <= budget tokens.
    A single sentence longer than budget stays one piece."""
    units = []
    for para in re.split(r"\n\s*\n", text):
        para = para.strip()
        if not para:
            continue
        if count_tokens(para) <= budget:
            units.append(para)
        else:
            units.extend(s for s in re.split(r"(?<=[.!?])\s+", para) if s)
    pieces, cur, n = [], [], 0
    for u in units:
        k = count_tokens(u)
        if cur and n + k > budget:
            pieces.append("\n\n".join(cur))
            cur, n = [], 0
        cur.append(u)
        n += k
    if cur:
        pieces.append("\n\n".join(cur))
    return pieces


def json_list_items(content: str, field: str) -> List[Any]:
    """Complete top-level items of the JSON list in a (possibly truncated / malformed) response:
    a bare list, or the list under `field` of an object. Stops at the first undecodable item."""
    s = content.strip()
    if s.startswith("```"):
        s = s.split("\n", 1)[-1]
    if s.startswith("{"):
        k = s.find(f'"{field}"')
        start = s.find("[", k) if k >= 0 else -1
    else:
        start = s.find("[")
    if start < 0:
        return []
    dec, items, i = json.JSONDecoder(strict=False), [], start + 1
    while i < len(s):
        while i < len(s) and s[i] in " \n\r\t,":
            i += 1
        if i >= len(s) or s[i] == "]":
            break
        try:
            value, i = dec.raw_decode(s, i)
        except json.JSONDecodeError:
            break
        items.append(value)
    return items


def salvage_structured(content: str, text_format: type) -> Any:
    """Well-formed items of an unparsable NER / triple response, validated as text_format.
    Raises ValueError when nothing is usable (the caller's retry then applies as before)."""
    fields = list(getattr(text_format, "model_fields", {}))
    if fields == ["named_entities"]:
        seen, values = set(), []
        for x in json_list_items(content, "named_entities"):
            if isinstance(x, str) and x.strip() and x not in seen:
                seen.add(x)
                values.append(x)
        values = values[:MAX_SALVAGED_ENTITIES]
    elif fields == ["triples"]:
        values = [x for x in json_list_items(content, "triples")
                  if isinstance(x, list) and x and all(isinstance(e, str) for e in x)]
    else:
        raise ValueError(f"no salvage rule for {text_format}")
    if not values:
        raise ValueError("no well-formed items to salvage")
    return text_format.model_validate({fields[0]: values})


def cut_long_runs(triples: List[List[str]], max_run: int = MAX_SAME_SUBJ_PRED_RUN) -> List[List[str]]:
    """Drop items beyond max_run in a consecutive run of the same (subject, predicate)."""
    out, prev, run = [], None, 0
    for t in triples:
        key = tuple(t[:2])
        run = run + 1 if key == prev else 1
        prev = key
        if run <= max_run:
            out.append(t)
    return out


def write_cache_docs(cache_file: str, new_docs: List[Dict[str, Any]]) -> int:
    """Add docs to a HippoRAG OpenIE cache file, keeping existing entries. Returns #docs added."""
    docs = load_json(cache_file).get("docs", []) if os.path.isfile(cache_file) else []
    have = {d["idx"] for d in docs}
    added = [d for d in new_docs if d["idx"] not in have]
    os.makedirs(os.path.dirname(cache_file), exist_ok=True)
    with open(cache_file, "w", encoding="utf-8") as f:
        json.dump({"docs": docs + added}, f, ensure_ascii=False)
    return len(added)


def openie_split_docs(openie: Any, split: Dict[str, Dict[str, Any]]) -> Tuple[List[Dict[str, Any]], Dict[str, int]]:
    """OpenIE each piece (NER -> triples, WorldMM OpenIE methods), merge per chunk in piece order."""
    from concurrent.futures import ThreadPoolExecutor
    from worldmm.memory.episodic.utils import filter_invalid_triples

    def run(key, piece):
        ner = openie.ner(chunk_key=key, passage=piece)
        tri = openie.triple_extraction(chunk_key=key, passage=piece, named_entities=ner.unique_entities)
        return ner, tri

    with ThreadPoolExecutor() as ex:   # same default concurrency as OpenIE.batch_openie
        futures = {key: [ex.submit(run, key, p) for p in s["pieces"]] for key, s in split.items()}
        results = {key: [f.result() for f in fs] for key, fs in futures.items()}
    docs, stats = [], {"chunks": len(split), "pieces": 0, "failed_pieces": 0}
    for key, outs in results.items():
        entities, triples = [], []
        for ner, tri in outs:
            stats["pieces"] += 1
            stats["failed_pieces"] += bool(ner.metadata.get("error") or tri.metadata.get("error"))
            entities += [e for e in ner.unique_entities if e not in entities]
            triples += tri.triples
        docs.append({"idx": key, "passage": split[key]["text"], "extracted_entities": entities,
                     "extracted_triples": filter_invalid_triples(triples)})
    return docs, stats


def plan_video(cfg: Dict[str, Any], video_id: str, label: str) -> Dict[str, Any]:
    """Count chunks / seedable / cached chunks and the OpenIE LLM calls still needed (2 per chunk,
    2 per piece for passages above SPLIT_MIN_TOKENS)."""
    paths, wm = cfg["paths"], cfg["worldmm"]
    plan = {"video_id": video_id, "granularities": {}, "missing": [], "llm_calls": 0}
    seed_allowed = label == wm["metadata_model"]
    metadata_openie_file = os.path.join(paths["metadata_dir"], "episodic_memory", video_id,
                                        f"openie_results_{wm['metadata_model']}.json")
    for g in wm["granularities"]:
        caption_file = os.path.join(paths["caption_dir"], video_id, f"{g}.json")
        if not os.path.isfile(caption_file):
            plan["missing"].append(caption_file)
            continue
        texts = indexed_texts(caption_file, wm["query_time"])
        unique = {chunk_id(t) for t in texts}
        cache_file = openie_cache_path(paths["episodic_cache_root"], video_id, g, label)
        cached = cached_openie_keys(cache_file) & unique
        seed_docs: List[Dict[str, Any]] = []
        if g == "10sec" and seed_allowed and not os.path.isfile(cache_file):
            if os.path.isfile(metadata_openie_file):
                seed_docs = build_seed_docs(texts, load_json(metadata_openie_file))
            else:
                plan["missing"].append(metadata_openie_file)
        seeded = {d["idx"] for d in seed_docs}
        split: Dict[str, Dict[str, Any]] = {}
        for t in texts:
            key = chunk_id(t)
            if key not in cached and key not in seeded and key not in split and count_tokens(t) > SPLIT_MIN_TOKENS:
                split[key] = {"text": t, "pieces": split_passage(t)}
        to_compute = len(unique - cached - seeded - set(split))
        pieces = sum(len(s["pieces"]) for s in split.values())
        plan["granularities"][g] = {"chunks": len(unique), "cached": len(cached), "seeded": len(seeded),
                                    "to_compute": to_compute, "split": split, "split_pieces": pieces,
                                    "cache_file": cache_file, "seed_docs": seed_docs}
        plan["llm_calls"] += 2 * (to_compute + pieces)
    return plan


def make_labeled_episodic_memory_class():
    """Deferred import: dry-run must not load torch / models."""
    from hipporag import HippoRAG
    from hipporag.utils.config_utils import BaseConfig
    from worldmm.memory.episodic import EpisodicMemory

    class LabeledEpisodicMemory(EpisodicMemory):
        """EpisodicMemory whose HippoRAG caches are labeled with the real LLM name."""

        def __init__(self, *args, llm_label: str, **kwargs):
            super().__init__(*args, **kwargs)
            self.llm_label = llm_label

        def _get_or_create_hipporag(self, granularity: str):
            if granularity not in self.hipporag:
                self.hipporag[granularity] = HippoRAG(
                    global_config=BaseConfig(llm_name=self.llm_label),
                    save_dir=f"{self.save_dir_root}/{granularity}",
                    llm_model=self.llm_model,
                    embedding_model=self.embedding_model)
            return self.hipporag[granularity]

    return LabeledEpisodicMemory


def make_http_llm_model(endpoints: List[str], served_model: str, label: str, timeout: float = 1800.0):
    """
    Drop-in for WorldMM LLMModel as used by HippoRAG/OpenIE (indexing only uses
    .generate(messages, text_format=...) and .model_name). Deferred import (torch via worldmm).
    """
    import itertools
    import threading
    import requests
    from worldmm.llm import dynamic_retry_decorator
    from worldmm.llm.qwen3vl import Qwen3VLModel

    class HttpLLMModel:
        def __init__(self):
            self.model_name = label
            self.max_retries = 3           # = Qwen3VLModel default (retry decorator reads this)
            self.kwargs: Dict[str, Any] = {}
            self._cycle = itertools.cycle(endpoints)
            self._lock = threading.Lock()
            self.calls = 0
            self.failures = 0
            self.guard = {"salvaged_ner": 0, "salvaged_triples": 0, "cut_triples": 0}

        @dynamic_retry_decorator
        def generate(self, prompt, text_format=None, **kwargs):
            messages = [{"role": "user", "content": prompt}] if isinstance(prompt, str) else prompt
            with self._lock:
                endpoint = next(self._cycle)
                self.calls += 1
            body = {"model": served_model, "messages": messages,
                    "max_tokens": int(kwargs.get("max_new_tokens", 2048))}
            try:
                r = requests.post(f"{endpoint}/chat/completions", json=body, timeout=timeout)
                if r.status_code != 200:
                    raise RuntimeError(f"{endpoint}: HTTP {r.status_code} {r.text[:200]}")
                content = r.json()["choices"][0]["message"]["content"]
                content = content.strip() if content else ""
                if not text_format:
                    return content
                # Same parser as the in-process path (does not use instance state); on failure keep the
                # well-formed items (truncated / malformed output), else raise -> retry as before.
                try:
                    parsed = Qwen3VLModel._parse_structured_response(None, content, text_format)
                except Exception:
                    parsed = salvage_structured(content, text_format)
                    with self._lock:
                        self.guard["salvaged_ner" if hasattr(parsed, "named_entities") else "salvaged_triples"] += 1
                if hasattr(parsed, "triples"):
                    kept = cut_long_runs(parsed.triples)
                    if len(kept) < len(parsed.triples):
                        with self._lock:
                            self.guard["cut_triples"] += len(parsed.triples) - len(kept)
                        parsed = text_format.model_validate({"triples": kept})
                return parsed
            except Exception:
                with self._lock:
                    self.failures += 1
                raise

        def __repr__(self):
            return f"HttpLLMModel(label={label}, endpoints={endpoints})"

    return HttpLLMModel()


def check_endpoints(endpoints: List[str], served_model: str) -> None:
    import requests
    for e in endpoints:
        base = e[:-len("/v1")] if e.endswith("/v1") else e
        r = requests.get(f"{base}/health", timeout=10)
        r.raise_for_status()
        model = r.json().get("model")
        if model != served_model:
            raise SystemExit(f"{e}: serves model {model!r}, expected {served_model!r}")


def select_videos(caption_dir: str, videos_arg: str, shard_arg: str) -> List[str]:
    videos = sorted(d for d in os.listdir(caption_dir) if os.path.isdir(os.path.join(caption_dir, d)))
    if videos_arg:
        wanted = videos_arg.split(",")
        unknown = [v for v in wanted if v not in videos]
        if unknown:
            raise SystemExit(f"Unknown video ids: {unknown}")
        videos = wanted
    if shard_arg:
        k, n = (int(x) for x in shard_arg.split("/"))
        videos = videos[k::n]
    return videos


def print_plans(plans: List[Dict[str, Any]], granularities: List[str]) -> None:
    header = f"{'video':14s} " + " ".join(f"{g:>22s}" for g in granularities) + f" {'LLM calls':>10s}"
    print(header + "\n" + " " * 15 + " ".join(f"{'chunk/cache/seed/new/split(pc)':>22s}" for _ in granularities))
    for p in plans:
        cells = []
        for g in granularities:
            s = p["granularities"].get(g)
            cells.append(f"{s['chunks']}/{s['cached']}/{s['seeded']}/{s['to_compute']}/{len(s['split'])}({s['split_pieces']})"
                         if s else "MISSING")
        print(f"{p['video_id']:14s} " + " ".join(f"{c:>22s}" for c in cells) + f" {p['llm_calls']:>10d}")
    total = sum(p["llm_calls"] for p in plans)
    print(f"\nvideos={len(plans)}  total OpenIE LLM calls={total}  "
          f"(mean {total / max(len(plans), 1):.0f}/video)")
    for p in plans:
        for m in p["missing"]:
            print(f"MISSING [{p['video_id']}]: {m}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Offline WorldMM episodic (HippoRAG) pre-indexing")
    parser.add_argument("--config", required=True)
    parser.add_argument("--videos", default="", help="Comma-separated video ids (default: all in caption_dir)")
    parser.add_argument("--shard", default="", help="K/N: process every N-th video starting at K")
    parser.add_argument("--dry-run", action="store_true", help="Plan only: no model load, no writes")
    parser.add_argument("--llm-endpoints", default="",
                        help="Comma-separated OpenAI-compatible base URLs (local_llm_server.py, .../v1) for OpenIE; "
                             "default: load the LLM in-process")
    parser.add_argument("--gpu-mem-cap-mib", type=int, default=0,
                        help="Hard per-process GPU memory cap (torch set_per_process_memory_fraction)")
    args = parser.parse_args()
    endpoints = [e.strip().rstrip("/") for e in args.llm_endpoints.split(",") if e.strip()]

    cfg = yaml.safe_load(open(args.config, encoding="utf-8"))
    paths, wm = cfg["paths"], cfg["worldmm"]
    label = cfg["llm"][cfg["llm"]["backend"]]["worldmm_model"]
    videos = select_videos(paths["caption_dir"], args.videos, args.shard)
    # Must be set before importing torch/transformers (via worldmm) and huggingface_hub (count_tokens).
    os.environ["HF_HOME"] = paths["hf_home"]

    if args.dry_run:
        logging.basicConfig(level=logging.WARNING)
        print(f"backend={cfg['llm']['backend']} llm_label={label} "
              f"seeding={'on' if label == wm['metadata_model'] else 'off (label != metadata_model)'}")
        print_plans([plan_video(cfg, v, label) for v in videos], wm["granularities"])
        return

    os.makedirs(paths["log_dir"], exist_ok=True)
    logging.basicConfig(
        level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s",
        handlers=[logging.StreamHandler(),
                  logging.FileHandler(os.path.join(paths["log_dir"], f"prebuild_{time.strftime('%Y%m%d_%H%M%S')}.log"))])
    done_dir = os.path.join(paths["episodic_cache_root"], "_done")
    os.makedirs(done_dir, exist_ok=True)

    if args.gpu_mem_cap_mib:
        import torch
        total_mib = torch.cuda.get_device_properties(0).total_memory / 2**20
        torch.cuda.set_per_process_memory_fraction(args.gpu_mem_cap_mib / total_mib)
        logger.info(f"GPU memory cap {args.gpu_mem_cap_mib} MiB of {total_mib:.0f} MiB")
    from worldmm.embedding import EmbeddingModel
    from worldmm.llm import LLMModel, PromptTemplateManager
    LabeledEpisodicMemory = make_labeled_episodic_memory_class()

    if endpoints:
        served_model = cfg["llm"]["local"]["endpoint"]["model"]
        if cfg["llm"]["backend"] != "local" or served_model != label:
            raise SystemExit(f"--llm-endpoints needs llm.backend=local and endpoint model == worldmm_model "
                             f"(got backend={cfg['llm']['backend']}, endpoint model={served_model}, label={label})")
        check_endpoints(endpoints, served_model)
        llm_model = make_http_llm_model(endpoints, served_model, label)
    logger.info(f"Loading models (llm={label} {'via ' + ','.join(endpoints) if endpoints else 'in-process'}, "
                f"embedding={wm['text_embedding_model']})")
    embedding_model = EmbeddingModel(text_model_name=wm["text_embedding_model"])
    embedding_model.load_model(model_type="text")
    if not endpoints:
        llm_model = LLMModel(model_name=label)
    prompt_template_manager = PromptTemplateManager()
    from worldmm.memory.episodic.openie import OpenIE
    openie = OpenIE(llm_model=llm_model)   # split long passages only (HippoRAG keeps its own instance)

    failed = []
    for i, video_id in enumerate(videos, 1):
        done_marker = os.path.join(done_dir, f"{video_id}.{label.replace('/', '_')}.json")
        if os.path.isfile(done_marker):
            logger.info(f"[{i}/{len(videos)}] {video_id}: already done, skip")
            continue
        plan = plan_video(cfg, video_id, label)
        if plan["missing"]:
            logger.error(f"[{i}/{len(videos)}] {video_id}: missing inputs {plan['missing']}")
            failed.append(video_id)
            continue
        start = time.time()
        try:
            logger.info(f"[{i}/{len(videos)}] {video_id}: indexing, expected OpenIE LLM calls={plan['llm_calls']}")
            split_stats = {}
            for g, s in plan["granularities"].items():
                if s["seed_docs"]:
                    write_cache_docs(s["cache_file"], s["seed_docs"])
                    logger.info(f"{video_id}/{g}: seeded {len(s['seed_docs'])} OpenIE docs")
                if s["split"]:
                    t0 = time.time()
                    docs, split_stats[g] = openie_split_docs(openie, s["split"])
                    write_cache_docs(s["cache_file"], docs)
                    logger.info(f"{video_id}/{g}: split OpenIE {split_stats[g]} in {time.time() - t0:.0f}s")

            memory = LabeledEpisodicMemory(
                embedding_model=embedding_model, llm_model=llm_model,
                prompt_template_manager=prompt_template_manager,
                granularities=wm["granularities"],
                save_dir_root=os.path.join(paths["episodic_cache_root"], video_id, "episodic_memory"),
                llm_label=label)
            memory.load_captions_from_files(
                {g: os.path.join(paths["caption_dir"], video_id, f"{g}.json") for g in wm["granularities"]})
            memory.index(wm["query_time"])

            after = plan_video(cfg, video_id, label)
            remaining = {g: s["to_compute"] + len(s["split"]) for g, s in after["granularities"].items()
                         if s["to_compute"] or s["split"]}
            if remaining:
                raise RuntimeError(f"OpenIE cache incomplete after indexing: {remaining}")
            empty = {}
            for g, s in after["granularities"].items():
                docs = load_json(s["cache_file"]).get("docs", [])
                empty[g] = {"empty_triples": sum(1 for d in docs if not d.get("extracted_triples")),
                            "empty_entities": sum(1 for d in docs if not d.get("extracted_entities"))}
            with open(done_marker, "w", encoding="utf-8") as f:
                json.dump({"video_id": video_id, "llm_label": label, "seconds": round(time.time() - start, 1),
                           "llm_calls_planned": plan["llm_calls"],
                           "llm_mode": "http:" + ",".join(endpoints) if endpoints else "in-process",
                           "chunks": {g: s["chunks"] for g, s in after["granularities"].items()},
                           "split": split_stats, "cache_empty": empty,
                           "guard_cumulative": dict(getattr(llm_model, "guard", {}))}, f, indent=2)
            logger.info(f"[{i}/{len(videos)}] {video_id}: done in {time.time() - start:.0f}s")
        except Exception as e:
            logger.exception(f"[{i}/{len(videos)}] {video_id}: failed: {e}")
            failed.append(video_id)
        finally:
            memory = None

    if endpoints:
        logger.info(f"HTTP OpenIE requests={llm_model.calls} failed_requests={llm_model.failures} guard={llm_model.guard}")
    logger.info(f"Finished. failed={len(failed)} {failed}")
    sys.exit(1 if failed else 0)


if __name__ == "__main__":
    main()
