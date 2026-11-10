"""
OpenIE degeneration experiment on long 10min chunks (Qwen3-VL-8B, transformers, same chat template and
model generation_config as WorldMM Qwen3VLModel; text-only so the processor path reduces to the tokenizer).
Per chunk: NER -> triple extraction (WorldMM templates), `--samples` times, with one decoding setting:
  base      : model generation_config (do_sample, T=0.7, top_p=0.8, top_k=20, repetition_penalty=1.0), max_new_tokens=2048
  rp105     : + repetition_penalty=1.05 (HF: applies to prompt AND generated tokens)
  rp110gen  : + RepetitionPenaltyLogitsProcessor(1.10, prompt_ignore_length=<prompt len>) (generated tokens only)
Records per call: tokens, seconds, hit max, strict parse ok (= WorldMM parser), loop metrics.
Run with CUDA_VISIBLE_DEVICES=<gpu>; per-process cap 19,000 MiB.
  python analysis/openie_degeneration_exp.py --setting base --out <json> [--samples 2]
"""
import argparse, json, os, re, sys, time
from collections import Counter

RF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RF)
from rf_config import load_config  # noqa: E402
CFG = load_config(os.path.join(RF, "config.yaml"))
os.environ.setdefault("HF_HOME", CFG["paths"]["hf_home"])
import torch
torch.cuda.set_per_process_memory_fraction(19000 / (torch.cuda.get_device_properties(0).total_memory / 2**20))
from transformers import AutoProcessor, Qwen3VLForConditionalGeneration, LogitsProcessorList
from transformers.generation.logits_process import RepetitionPenaltyLogitsProcessor
from worldmm.llm import PromptTemplateManager
from worldmm.llm.qwen3vl import Qwen3VLModel
from worldmm.memory.episodic.utils import NerRawOutput, TripleRawOutput, filter_invalid_triples

CAP = CFG["paths"]["caption_dir"]
CHUNKS = [("0RxMZBLeqRI", 0), ("0RxMZBLeqRI", 1), ("0RxMZBLeqRI", 2), ("-QuCz7kxBr8", 0)]


def salvage(text):
    """Complete top-level items of a (possibly truncated) JSON list / {"key": [...]} response."""
    s = text.strip()
    if s.startswith("```"):
        s = s.split("\n", 1)[-1]
    i = s.find("[", s.find(":") if s.lstrip().startswith("{") else 0)
    dec, out, i = json.JSONDecoder(strict=False), [], i + 1
    while 0 < i < len(s):
        while i < len(s) and s[i] in " \n\r\t,":
            i += 1
        try:
            v, i = dec.raw_decode(s, i)
        except Exception:
            break
        out.append(v)
    return out


def loop_metrics(triples):
    run = best = 1
    for a, b in zip(triples, triples[1:]):
        run = run + 1 if a[:2] == b[:2] else 1
        best = max(best, run)
    sp = Counter(tuple(map(str, t[:2])) for t in triples)
    return {"max_run_same_subj_pred": best if triples else 0, "max_count_same_subj_pred": max(sp.values()) if sp else 0}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--setting", choices=["base", "rp105", "rp110gen"], required=True)
    ap.add_argument("--samples", type=int, default=2)
    ap.add_argument("--out", required=True)
    a = ap.parse_args()
    name = "Qwen/Qwen3-VL-8B-Instruct"
    model = Qwen3VLForConditionalGeneration.from_pretrained(name, torch_dtype=torch.bfloat16,
                                                            attn_implementation="flash_attention_2", device_map="auto")
    proc = AutoProcessor.from_pretrained(name)
    ptm = PromptTemplateManager(role_mapping={"system": "system", "user": "user", "assistant": "assistant"})

    def gen(messages):
        text = proc.apply_chat_template(messages, tokenize=False, add_generation_prompt=True)
        inputs = proc(text=[text], return_tensors="pt").to(model.device)
        n = inputs.input_ids.shape[1]
        kw = {"max_new_tokens": 2048}
        if a.setting == "rp105":
            kw["repetition_penalty"] = 1.05
        elif a.setting == "rp110gen":
            kw["logits_processor"] = LogitsProcessorList([RepetitionPenaltyLogitsProcessor(1.10, prompt_ignore_length=n)])
        t = time.time()
        out = model.generate(**inputs, **kw)[0][n:]
        sec = time.time() - t
        ntok = int(out.shape[0])
        hit = ntok >= 2048
        resp = proc.batch_decode([out], skip_special_tokens=True, clean_up_tokenization_spaces=False)[0].strip()
        return resp, {"prompt_tokens": n, "completion_tokens": ntok, "hit_max": hit, "sec": round(sec, 1)}

    def parse(resp, fmt):
        try:
            return Qwen3VLModel._parse_structured_response(None, resp, fmt), None
        except Exception as e:
            return None, str(e)[:200]

    rows = []
    for vid, idx in CHUNKS:
        passage = json.load(open(f"{CAP}/{vid}/10min.json"))[idx]["text"]
        for s in range(a.samples):
            r = {"video": vid, "chunk": idx, "sample": s, "setting": a.setting}
            resp, st = gen(ptm.render(name="ner", passage=passage))
            ner, err = parse(resp, NerRawOutput)
            ents = ner.named_entities if ner else [e for e in salvage(resp) if isinstance(e, str)]
            r["ner"] = {**st, "parse_ok": ner is not None, "error": err, "entities": len(ents), "unique": len(set(ents))}
            resp, st = gen(ptm.render(name="triple_extraction", passage=passage,
                                      named_entity_json=json.dumps({"named_entities": ents})))
            tri, err = parse(resp, TripleRawOutput)
            trip = filter_invalid_triples(tri.triples) if tri else [t for t in salvage(resp) if isinstance(t, list) and len(t) == 3]
            r["triples"] = {**st, "parse_ok": tri is not None, "error": err, "n": len(trip), **loop_metrics(trip)}
            r["triples_sample"] = trip[:8]
            rows.append(r)
            print(json.dumps({k: r[k] for k in ("video", "chunk", "sample", "ner", "triples")}, ensure_ascii=False), flush=True)
            json.dump(rows, open(a.out, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
