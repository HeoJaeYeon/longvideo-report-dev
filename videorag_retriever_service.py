#!/usr/bin/env python3
"""
Video-RAG retrieval service (WorldMM backend) implementing Deep-Reporter's search contract.

Deep-Reporter's search_node POSTs {query_list, type: "text"|"image", topk} to `retriever_url`
and stores `results` as section evidence. This service answers from one video's WorldMM
memories (no repo file is modified; WorldMM components are composed directly):

  text  -> episodic captions (HippoRAG graphs per granularity, filter mode L0/L1/full)
           + semantic triples (video-level knowledge, no timestamp)
  image -> visual clips (VLM2Vec similarity) -> center frame JPEG + matching 10sec caption

Per-query ranked lists are merged with reciprocal rank fusion (WorldMM returns no comparable
scores), so `score` is an RRF value and `score_type` says so.

Episodic filter modes (config retrieval.episodic_filter):
  L0   : LLM-free HippoRAG graph search (HippoRAG.retrieve without the DSPy fact filter)
  L1   : L0 candidates of all queries -> one WorldMM multiscale_filter LLM call per request
  full : WorldMM episodic_memory.retrieve per query (DSPy filter x granularities + multiscale filter)

Episodic graphs must be pre-built (prebuild_episodic_index.py). Loading refuses incomplete
caches, because HippoRAG's OpenIE swallows LLM errors and would persist empty results.

Endpoints:
  POST /videos/<video_id>/search   Deep-Reporter contract
  POST /videos/<video_id>/load     preload a video (optional; search loads on demand)
  GET  /health
Usage:
  python videorag_retriever_service.py --config config.yaml --gpu 0 [--preload VID]
  Deep-Reporter: generate_article(..., retriever_url="http://127.0.0.1:8020/videos/<VID>/search")
"""

import argparse
import ast
import json
import logging
import os
import sys
import threading
import time
from typing import Any, Dict, List, Optional, Sequence, Tuple

import numpy as np
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
from prebuild_episodic_index import make_labeled_episodic_memory_class, plan_video  # noqa: E402

logger = logging.getLogger("videorag_retriever")


# ---------------------------------------------------------------------------
# LLM clients used inside WorldMM components
# ---------------------------------------------------------------------------

class NoLLM:
    """L0: any LLM call is a bug (OpenIE on an incomplete cache, or a filter call)."""
    model_name = "none"

    def generate(self, *args, **kwargs):
        raise RuntimeError("LLM is disabled in L0 mode")


class EndpointLLM:
    """WorldMM-compatible `.generate(messages) -> str` over an OpenAI-compatible endpoint."""

    def __init__(self, base_url: Optional[str], api_key: str, model: str, max_tokens: int, token_param: str):
        from openai import OpenAI
        self.client = OpenAI(base_url=base_url, api_key=api_key)
        self.model_name = model
        self.max_tokens = max_tokens
        self.token_param = token_param
        self.calls = 0
        self.failures = 0

    @classmethod
    def from_config(cls, cfg: Dict[str, Any]) -> "EndpointLLM":
        backend, max_tokens = cfg["llm"]["backend"], int(cfg["retrieval"]["filter_max_tokens"])
        if backend == "local":
            ep = cfg["llm"]["local"]["endpoint"]
            return cls(f"http://{ep['host']}:{ep['port']}/v1", ep["api_key"], ep["model"], max_tokens, "max_tokens")
        if backend == "openai":
            api_key = os.environ.get("OPENAI_API_KEY")
            if not api_key:
                raise SystemExit("llm.backend=openai requires OPENAI_API_KEY")
            return cls(os.environ.get("OPENAI_BASE_URL"), api_key, cfg["llm"]["openai"]["endpoint"]["model"],
                       max_tokens, "max_completion_tokens")
        raise SystemExit(f"Unknown llm.backend: {backend}")

    def generate(self, messages, text_format=None, **kwargs) -> str:
        if text_format is not None:
            raise RuntimeError("Structured generation (OpenIE) is not allowed in the retrieval service; "
                               "run prebuild_episodic_index.py first")
        if isinstance(messages, str):
            messages = [{"role": "user", "content": messages}]
        self.calls += 1
        try:
            response = self.client.chat.completions.create(
                model=self.model_name, messages=messages, **{self.token_param: self.max_tokens})
            return response.choices[0].message.content or ""
        except Exception:
            self.failures += 1
            raise


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def rrf_merge(ranked_lists: Sequence[Sequence[Any]], key, k: int) -> List[Tuple[Any, float]]:
    """Reciprocal rank fusion: score(item) = sum over lists of 1 / (k + rank), rank from 1."""
    scores: Dict[str, float] = {}
    items: Dict[str, Any] = {}
    for ranked in ranked_lists:
        for rank, item in enumerate(ranked, 1):
            item_key = key(item)
            scores[item_key] = scores.get(item_key, 0.0) + 1.0 / (k + rank)
            items.setdefault(item_key, item)
    return sorted(((items[i], s) for i, s in scores.items()), key=lambda x: -x[1])


def hms(time_str: str) -> str:
    """WorldMM time 'HHMMSSFF' -> 'HH:MM:SS'."""
    t = str(time_str).zfill(8)
    return f"{t[0:2]}:{t[2:4]}:{t[4:6]}"


def seconds(time_str: str) -> float:
    t = str(time_str).zfill(8)
    return float(int(t[0:2]) * 3600 + int(t[2:4]) * 60 + int(t[4:6]))


# ---------------------------------------------------------------------------
# Retriever over one loaded video
# ---------------------------------------------------------------------------

class WorldMMRetriever:
    def __init__(self, cfg: Dict[str, Any], embedding_model, llm_model):
        from worldmm.llm import PromptTemplateManager
        self.cfg = cfg
        self.paths, self.wm, self.rcfg = cfg["paths"], cfg["worldmm"], cfg["retrieval"]
        self.mode = self.rcfg["episodic_filter"]
        if self.mode not in ("L0", "L1", "full"):
            raise ValueError(f"retrieval.episodic_filter must be L0|L1|full, got {self.mode}")
        self.embedding_model = embedding_model
        self.llm_model = llm_model
        self.prompt_template_manager = PromptTemplateManager()
        self.LabeledEpisodicMemory = make_labeled_episodic_memory_class()
        self.lock = threading.Lock()
        self.video_id: Optional[str] = None
        self.episodic = self.semantic = self.visual = None
        self.text_to_entry: Dict[str, Dict[str, Any]] = {}
        self.caption_10sec: Dict[str, Dict[str, Any]] = {}

    # ---------------- loading ----------------

    def check_inputs(self, video_id: str) -> List[str]:
        """Problems that prevent loading `video_id` (empty list = OK)."""
        label = self.wm["episodic_cache_label"]
        plan = plan_video(self.cfg, video_id, label)
        problems = list(plan["missing"])
        for g, s in plan["granularities"].items():
            if s["cached"] != s["chunks"]:
                problems.append(f"episodic cache incomplete for {g}: {s['cached']}/{s['chunks']} chunks "
                                f"(label={label}); run prebuild_episodic_index.py")
        meta = self.paths["metadata_dir"]
        for path in (os.path.join(meta, "semantic_memory", video_id,
                                  f"semantic_consolidation_results_{self.wm['metadata_model']}.json"),
                     os.path.join(meta, "visual_memory", video_id, "visual_embeddings.pkl")):
            if not os.path.isfile(path):
                problems.append(f"missing {path}")
        return problems

    def load(self, video_id: str) -> None:
        if self.video_id == video_id:
            return
        if not os.path.isdir(os.path.join(self.paths["caption_dir"], video_id)):
            raise KeyError(f"Unknown video_id: {video_id}")
        problems = self.check_inputs(video_id)
        if problems:
            raise RuntimeError(f"Cannot load {video_id}: " + "; ".join(problems))

        from worldmm.memory.semantic import SemanticMemory
        from worldmm.memory.visual import VisualMemory
        self.release()
        start = time.time()
        caption_dir = os.path.join(self.paths["caption_dir"], video_id)
        meta = self.paths["metadata_dir"]
        query_time = int(self.wm["query_time"])

        episodic = self.LabeledEpisodicMemory(
            embedding_model=self.embedding_model, llm_model=self.llm_model,
            prompt_template_manager=self.prompt_template_manager,
            granularities=self.wm["granularities"],
            save_dir_root=os.path.join(self.paths["episodic_cache_root"], video_id, "episodic_memory"),
            llm_label=self.wm["episodic_cache_label"])
        episodic.load_captions_from_files({g: os.path.join(caption_dir, f"{g}.json") for g in self.wm["granularities"]})
        episodic.index(query_time)

        semantic = SemanticMemory(embedding_model=self.embedding_model)
        semantic.load_triples_from_file(os.path.join(
            meta, "semantic_memory", video_id, f"semantic_consolidation_results_{self.wm['metadata_model']}.json"))
        semantic.index(query_time)

        with open(os.path.join(caption_dir, "10sec.json"), "r", encoding="utf-8") as f:
            captions_10sec = json.load(f)
        visual = VisualMemory(embedding_model=self.embedding_model)
        visual.load_embeddings_from_file(os.path.join(meta, "visual_memory", video_id, "visual_embeddings.pkl"))
        visual.load_clips_from_data(captions_10sec)
        visual.index(query_time)

        self.episodic, self.semantic, self.visual = episodic, semantic, visual
        # Per-granularity text -> entry (EpisodicMemory.text_to_entry is shared across granularities).
        self.text_to_entry = {g: {e.text: e for e in episodic.indexed_entries[g]} for g in self.wm["granularities"]}
        self.caption_10sec = {str(c.get("start_time", "")): c for c in captions_10sec}
        self.video_id = video_id
        logger.info(f"Loaded {video_id} in {time.time() - start:.1f}s: episodic "
                    f"{ {g: len(v) for g, v in self.text_to_entry.items()} }, semantic "
                    f"{semantic.get_indexed_count()}, visual {visual.get_indexed_count()}")

    def release(self) -> None:
        for memory in (self.semantic, self.visual):
            if memory is not None:
                memory.cleanup()
        self.episodic = self.semantic = self.visual = None
        self.video_id = None

    # ---------------- episodic ----------------

    def _graph_search(self, granularity: str, query: str, k: int) -> List[Any]:
        """HippoRAG.retrieve for one query without the DSPy fact filter (LLM-free)."""
        hipporag = self.episodic.hipporag.get(granularity)
        if hipporag is None or k <= 0:
            return []
        if not hipporag.ready_to_retrieve:
            hipporag.prepare_retrieval_objects()
        hipporag.get_query_embeddings([query])
        fact_scores = hipporag.get_fact_scores(query)
        try:
            if len(fact_scores) == 0 or len(hipporag.fact_node_keys) == 0:
                doc_ids, _ = hipporag.dense_passage_retrieval(query)
            else:
                link_top_k = hipporag.global_config.linking_top_k
                # Same candidate selection as HippoRAG.rerank_facts, minus the DSPy LLM filter.
                if len(fact_scores) <= link_top_k:
                    fact_indices = np.argsort(fact_scores)[::-1].tolist()
                else:
                    fact_indices = np.argsort(fact_scores)[-link_top_k:][::-1].tolist()
                fact_ids = [hipporag.fact_node_keys[i] for i in fact_indices]
                rows = hipporag.fact_embedding_store.get_rows(fact_ids)
                facts = [ast.literal_eval(rows[i]["content"]) for i in fact_ids]
                doc_ids, _ = hipporag.graph_search_with_fact_entities(
                    query=query, link_top_k=link_top_k, query_fact_scores=fact_scores,
                    top_k_facts=facts, top_k_fact_indices=fact_indices,
                    passage_node_weight=hipporag.global_config.passage_node_weight)
        except Exception as e:  # e.g. graph_search asserts no fact entity is in the graph
            logger.warning(f"graph search failed ({granularity}, {query!r}): {e}; using dense passage retrieval")
            doc_ids, _ = hipporag.dense_passage_retrieval(query)

        entries = []
        for idx in doc_ids:
            text = hipporag.chunk_embedding_store.get_row(hipporag.passage_node_keys[idx])["content"]
            entry = self.text_to_entry[granularity].get(text)
            if entry is not None:
                entries.append(entry)
                if len(entries) >= k:
                    break
        return entries

    def search_episodic(self, queries: List[str], n: int, meta: Dict[str, Any]) -> List[Tuple[Any, float]]:
        if n <= 0:
            return []
        rrf_k = int(self.rcfg["rrf_k"])
        if self.mode == "full":
            # Enough per query to fill n after merging (LLM calls do not depend on final_top_k).
            per_query_k = max(int(self.rcfg["full_top_k_per_query"]), -(-n // len(queries)))
            ranked = [self.episodic.retrieve(query=q, final_top_k=per_query_k, as_context=False) for q in queries]
            return rrf_merge(ranked, key=lambda e: e.id, k=rrf_k)[:n]

        per_query = self.rcfg["episodic_candidates_per_query"]
        ranked = [self._graph_search(g, q, int(per_query.get(g, 0)))
                  for q in queries for g in self.wm["granularities"]]
        merged = rrf_merge(ranked, key=lambda e: e.id, k=rrf_k)
        meta["episodic_candidates"] = len(merged)
        if self.mode == "L0" or len(merged) <= n:
            meta["episodic_filter"] = "none" if self.mode == "L0" else "skipped(<=n)"
            return merged[:n]

        # L1: one WorldMM multiscale_filter call over all candidates of this request.
        score_of = {e.id: s for e, s in merged}
        calls, failures = self.llm_model.calls, self.llm_model.failures
        selected = self.episodic._filter_with_llm(query="; ".join(queries), candidates=merged, final_top_k=n)
        ran = self.llm_model.calls > calls and self.llm_model.failures == failures
        meta["episodic_filter"] = "llm" if ran else "fallback_rrf(llm_failed)"
        return [(e, score_of[e.id]) for e in selected]

    # ---------------- semantic / visual ----------------

    def search_semantic(self, queries: List[str], n: int) -> List[Tuple[Any, float]]:
        if n <= 0:
            return []
        k = int(self.rcfg["semantic_k_per_query"])
        ranked = [self.semantic.retrieve(q, top_k=k, as_context=False) for q in queries]
        return rrf_merge(ranked, key=lambda e: e.id, k=int(self.rcfg["rrf_k"]))[:n]

    def search_visual(self, queries: List[str], n: int) -> List[Tuple[Any, float]]:
        if n <= 0:
            return []
        k = int(self.rcfg["visual_k_per_query"])
        # _retrieve_by_similarity: always embedding search (retrieve() would treat a
        # "DAY X HH:MM:SS - ..." string as a time range and return frames instead of clips).
        ranked = [self.visual._retrieve_by_similarity(q, top_k=k, as_context=False) for q in queries]
        return rrf_merge(ranked, key=lambda c: c.id, k=int(self.rcfg["rrf_k"]))[:n]

    def abs_video_path(self, path: str) -> str:
        return path if os.path.isabs(path) else os.path.join(self.paths["worldmm_root"], path)

    def extract_center_frame(self, clip) -> Optional[Tuple[str, float]]:
        """Center frame of the clip interval -> {frames_dir}/{video}/{start_time}.jpg (cached)."""
        out = os.path.join(self.cfg["service"]["frames_dir"], self.video_id, f"{clip.start_time}.jpg")
        center = (clip.clip_start_sec + clip.clip_end_sec) / 2.0
        if os.path.isfile(out):
            return out, center
        try:
            from decord import VideoReader, cpu
            from PIL import Image
            reader = VideoReader(self.abs_video_path(clip.video_path), ctx=cpu(0))
            index = min(int(center * reader.get_avg_fps()), len(reader) - 1)
            os.makedirs(os.path.dirname(out), exist_ok=True)
            tmp = out + ".tmp.jpg"
            Image.fromarray(reader[index].asnumpy()).save(tmp, quality=90)
            os.replace(tmp, out)
            return out, center
        except Exception as e:
            logger.error(f"Frame extraction failed for {clip.video_path} @ {center:.1f}s: {e}")
            return None

    # ---------------- Deep-Reporter items ----------------

    def _base(self, uid: str, source: str, score: float, score_type: str, rank: int) -> Dict[str, Any]:
        return {"id": uid, "uid": uid, "source": source, "score": round(float(score), 6),
                "score_type": score_type, "rank": rank, "video_id": self.video_id}

    def episodic_item(self, entry, score: float, score_type: str, rank: int) -> Dict[str, Any]:
        item = self._base(f"{self.video_id}:episodic:{entry.id}", "worldmm-episodic", score, score_type, rank)
        item.update({
            "type": "text",
            "content": f"[{hms(entry.start_time)}-{hms(entry.end_time)} | episodic {entry.granularity}] {entry.text}",
            "text": entry.text, "granularity": entry.granularity, "date": entry.date,
            "start_time": entry.start_time, "end_time": entry.end_time,
            "start_sec": seconds(entry.start_time), "end_sec": seconds(entry.end_time),
            "video_path": self.abs_video_path(entry.video_path or ""),
        })
        return item

    def semantic_item(self, entry, score: float, rank: int) -> Dict[str, Any]:
        item = self._base(f"{self.video_id}:semantic:{entry.id}", "worldmm-semantic", score, "rrf", rank)
        item.update({
            "type": "text",
            "content": f"[video-level knowledge | semantic] ({entry.subject}, {entry.predicate}, {entry.object})",
            "text": entry.to_display_str(), "triple": entry.triple,
            "start_time": None, "end_time": None, "start_sec": None, "end_sec": None,
            "time_grounded": False,
        })
        return item

    def image_item(self, clip, score: float, rank: int, img_path: str, center_sec: float) -> Dict[str, Any]:
        caption = self.caption_10sec.get(clip.start_time, {}).get("text", "")
        label = f"[{hms(clip.start_time)}-{hms(clip.end_time)} | video frame at {center_sec:.1f}s] {caption}".strip()
        item = self._base(f"{self.video_id}:visual:{clip.start_time}", "worldmm-visual", score, "rrf", rank)
        item.update({
            "type": "image", "caption": label, "description": label, "img_path": img_path,
            "frame_sec": center_sec, "date": clip.date,
            "start_time": clip.start_time, "end_time": clip.end_time,
            "start_sec": clip.clip_start_sec, "end_sec": clip.clip_end_sec,
            "video_path": self.abs_video_path(clip.video_path),
        })
        return item

    # ---------------- request entry point ----------------

    def search(self, video_id: str, queries: List[str], data_type: str, topk: int) -> Dict[str, Any]:
        with self.lock:
            self.load(video_id)
            start = time.time()
            meta: Dict[str, Any] = {"video_id": video_id, "mode": self.mode, "queries": len(queries)}
            results: List[Dict[str, Any]] = []
            if data_type == "text":
                n_epi = min(int(self.rcfg["episodic_k"]), topk)
                n_sem = min(int(self.rcfg["semantic_k"]), max(topk - n_epi, 0))
                episodic = self.search_episodic(queries, n_epi, meta)
                score_type = "rrf" if meta.get("episodic_filter") != "llm" else "rrf(order=llm_filter)"
                results += [self.episodic_item(e, s, score_type, r) for r, (e, s) in enumerate(episodic, 1)]
                semantic = self.search_semantic(queries, n_sem)
                results += [self.semantic_item(e, s, r) for r, (e, s) in enumerate(semantic, 1)]
                meta["counts"] = {"episodic": len(episodic), "semantic": len(semantic)}
            else:
                clips = self.search_visual(queries, min(int(self.rcfg["image_k"]), topk))
                for rank, (clip, score) in enumerate(clips, 1):
                    frame = self.extract_center_frame(clip)
                    if frame is not None:
                        results.append(self.image_item(clip, score, rank, *frame))
                meta["counts"] = {"visual_clips": len(clips), "frames": len(results)}
            meta["elapsed_sec"] = round(time.time() - start, 2)
            if not results:
                logger.warning(f"0 results for {data_type} queries {queries}")
            logger.info(f"search {data_type}: {meta}")
            return {"status": "success", "type": data_type, "total_hits": len(results),
                    "results": results, "meta": meta}


# ---------------------------------------------------------------------------
# Flask app
# ---------------------------------------------------------------------------

def create_app(retriever: WorldMMRetriever):
    from flask import Flask, jsonify, request
    app = Flask(__name__)

    def error(message: str, status: int):
        return jsonify({"status": "error", "error": message}), status

    @app.get("/health")
    def health():
        return jsonify({"status": "ok", "loaded_video": retriever.video_id, "mode": retriever.mode})

    @app.post("/videos/<video_id>/load")
    def load(video_id: str):
        try:
            with retriever.lock:
                retriever.load(video_id)
        except KeyError as e:
            return error(str(e), 404)
        except RuntimeError as e:
            return error(str(e), 409)
        return jsonify({"status": "success", "loaded_video": video_id})

    @app.post("/videos/<video_id>/search")
    def search(video_id: str):
        data = request.get_json(force=True, silent=True) or {}
        queries = [q for q in data.get("query_list", []) if isinstance(q, str) and q.strip()]
        data_type = data.get("type", "text")
        if not queries:
            return error("query_list must contain non-empty strings", 400)
        if data_type not in ("text", "image"):
            return error("type must be 'text' or 'image'", 400)
        try:
            topk = int(data.get("topk", 10))
            return jsonify(retriever.search(video_id, queries, data_type, topk))
        except KeyError as e:
            return error(str(e), 404)
        except RuntimeError as e:
            return error(str(e), 409)
        except Exception as e:
            logger.exception("search failed")
            return error(f"search failed: {e}", 500)

    return app


def main() -> None:
    parser = argparse.ArgumentParser(description="Video-RAG retrieval service (WorldMM) for Deep-Reporter")
    parser.add_argument("--config", required=True)
    parser.add_argument("--gpu", default=None, help="CUDA_VISIBLE_DEVICES (set before torch import)")
    parser.add_argument("--port", type=int, default=None)
    parser.add_argument("--preload", default="", help="Video id to load at startup")
    args = parser.parse_args()

    cfg = yaml.safe_load(open(args.config, encoding="utf-8"))
    os.environ["HF_HOME"] = cfg["paths"]["hf_home"]
    if args.gpu is not None:
        os.environ["CUDA_VISIBLE_DEVICES"] = args.gpu
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")

    from worldmm.embedding import EmbeddingModel
    embedding_model = EmbeddingModel(text_model_name=cfg["worldmm"]["text_embedding_model"])
    embedding_model.load_model()  # text (Qwen3-Embedding) + vision (VLM2Vec)
    mode = cfg["retrieval"]["episodic_filter"]
    llm_model = NoLLM() if mode == "L0" else EndpointLLM.from_config(cfg)
    retriever = WorldMMRetriever(cfg, embedding_model, llm_model)
    if args.preload:
        retriever.load(args.preload)

    host, port = cfg["service"]["host"], args.port or int(cfg["service"]["port"])
    logger.info(f"Serving retrieval (mode={mode}, llm={getattr(llm_model, 'model_name', '-')}) "
                f"at http://{host}:{port}/videos/<video_id>/search")
    create_app(retriever).run(host=host, port=port, threaded=True)


if __name__ == "__main__":
    main()
