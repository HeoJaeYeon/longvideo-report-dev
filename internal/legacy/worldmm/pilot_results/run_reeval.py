#!/usr/bin/env python3
"""Re-eval the videos that failed in the first pilot eval (CUDA OOM / round
exhaustion), one video per GPU on 5/6/7, then produce a corrected merged result.
All artifacts under claude_output."""
import os, sys, json, subprocess

ROOT = "/data1/USER/workspace/VideoRAG/WorldMM"
BASE = f"{ROOT}/claude_output/pilot"
os.chdir(ROOT)

# videos that scored 0/3 in the first pass (OOM or unable)
FAILED = ["GsYi-l5PEEs", "lAgwMGRvJrM", "H8fGd3fCJbg"]
GPUS = [5, 6, 7]

data = json.load(open(f"{BASE}/pilot_test.json"))
procs = []
for gpu, vid in zip(GPUS, FAILED):
    sub = [r for r in data if r["video_id"] == vid]
    ej = f"{BASE}/reeval_{vid}.json"; json.dump(sub, open(ej, "w"))
    outdir = f"{BASE}/reeval_out/{vid}"; cache = f"{BASE}/reeval_cache/{vid}"
    env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(gpu),
               PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True")
    log = open(f"{BASE}/reeval_{vid}.log", "w")
    cmd = [sys.executable, "eval/eval.py", "--eval-json", ej,
           "--caption-dir", f"{BASE}/caption_all", "--metadata-dir", f"{BASE}/metadata_all",
           "--retriever-model", "qwen3vl-8b", "--respond-model", "qwen3vl-8b",
           "--max-rounds", "5", "--episodic-top-k", "3", "--semantic-top-k", "10",
           "--visual-top-k", "3", "--output-dir", outdir, "--episodic-cache-dir", cache]
    print(f"[reeval] launch GPU{gpu}: {vid} ({len(sub)}Q)", flush=True)
    procs.append((vid, subprocess.Popen(cmd, env=env, stdout=log, stderr=subprocess.STDOUT)))

for vid, p in procs:
    print(f"[reeval] {vid} exited rc={p.wait()}", flush=True)

# build corrected merged: original results minus failed videos + new results
orig = json.load(open(f"{BASE}/pilot_eval_merged.json"))
kept = [r for r in orig if r["video_id"] not in set(FAILED)]
newres = []
for vid in FAILED:
    rp = f"{BASE}/reeval_out/{vid}/qwen3vl_8b_qwen3vl_8b/videomme_eval.json"
    if os.path.exists(rp):
        newres += json.load(open(rp))
final = kept + newres
json.dump(final, open(f"{BASE}/pilot_eval_final.json", "w"), indent=2)

n = len(final); c = sum(1 for r in final if r.get("evaluate"))
print("\n" + "=" * 50, flush=True)
print(f"[reeval] CORRECTED PILOT: {c}/{n} = {c/n:.4f}", flush=True)
from collections import Counter
def kind(r):
    s = str(r.get("response", "")).strip()
    if "Unable" in s: return "Unable"
    if s.startswith("Index error") or "out of memory" in s: return "OOM"
    if s[:1] in "ABCD": return "letter"
    return "other"
kc = Counter(kind(r) for r in final)
print(f"[reeval] response kinds: {dict(kc)}", flush=True)
letters = [r for r in final if kind(r) == "letter"]
lc = sum(1 for r in letters if r.get("evaluate"))
if letters: print(f"[reeval] clean-letter acc: {lc}/{len(letters)} = {lc/len(letters):.4f}", flush=True)
print("[reeval] DONE", flush=True)
