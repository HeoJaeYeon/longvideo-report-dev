#!/usr/bin/env python3
"""Pilot eval orchestrator (all artifacts under claude_output).
Merges captions, shards the 8 pilot videos across GPU 5/6/7, runs eval.py per
shard, merges results, and prints an accuracy summary. Run in background after
build_memory completes."""
import os, sys, json, subprocess, time

ROOT = "/data1/jyheo/workspace/VideoRAG/WorldMM"
BASE = f"{ROOT}/claude_output/pilot"
GPUS = [4, 5, 6, 7]
os.chdir(ROOT)

# 1) unified caption dir (symlinks to the 8 videos' caption subdirs)
capall = f"{BASE}/caption_all"
os.makedirs(capall, exist_ok=True)
for shard in ("g5", "g6"):
    cdir = f"{BASE}/{shard}/caption"
    if os.path.isdir(cdir):
        for v in os.listdir(cdir):
            link = f"{capall}/{v}"
            if not os.path.lexists(link):
                os.symlink(os.path.realpath(f"{cdir}/{v}"), link)
print(f"[eval] caption_all videos: {len(os.listdir(capall))}", flush=True)

# 2) split pilot test.json by video across GPUs
data = json.load(open(f"{BASE}/pilot_test.json"))
vids = sorted({r["video_id"] for r in data})
groups = {g: [] for g in GPUS}
for i, v in enumerate(vids):
    groups[GPUS[i % len(GPUS)]].append(v)

procs = []
for g in GPUS:
    gset = set(groups[g])
    sub = [r for r in data if r["video_id"] in gset]
    if not sub:
        continue
    ej = f"{BASE}/eval_shard_g{g}.json"
    json.dump(sub, open(ej, "w"))
    outdir = f"{BASE}/eval_out/g{g}"
    cache = f"{BASE}/eval_cache/g{g}"
    env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(g),
               PYTORCH_CUDA_ALLOC_CONF="expandable_segments:True")
    log = open(f"{BASE}/eval_g{g}.log", "w")
    cmd = [sys.executable, "eval/eval.py",
           "--eval-json", ej, "--caption-dir", capall,
           "--metadata-dir", f"{BASE}/metadata_all",
           "--retriever-model", "qwen3vl-8b", "--respond-model", "qwen3vl-8b",
           "--max-rounds", "5", "--episodic-top-k", "3",
           "--semantic-top-k", "10", "--visual-top-k", "3",
           "--output-dir", outdir, "--episodic-cache-dir", cache]
    print(f"[eval] launch GPU{g}: {len(sub)}Q over {len(gset)} videos", flush=True)
    procs.append((g, subprocess.Popen(cmd, env=env, stdout=log, stderr=subprocess.STDOUT)))

# 3) wait
for g, p in procs:
    rc = p.wait()
    print(f"[eval] GPU{g} exited rc={rc}", flush=True)

# 4) merge + summarize
allres = []
for g in GPUS:
    rp = f"{BASE}/eval_out/g{g}/qwen3vl_8b_qwen3vl_8b/videomme_eval.json"
    if os.path.exists(rp):
        allres += json.load(open(rp))
json.dump(allres, open(f"{BASE}/pilot_eval_merged.json", "w"), indent=2)

n = len(allres)
correct = sum(1 for r in allres if r.get("evaluate"))
print("\n" + "=" * 50, flush=True)
print(f"[eval] PILOT RESULT: {correct}/{n} = {correct/n:.4f}" if n else "[eval] no results", flush=True)
by_type = {}
for r in allres:
    t = r.get("type", "?")
    by_type.setdefault(t, [0, 0])
    by_type[t][0] += int(bool(r.get("evaluate")))
    by_type[t][1] += 1
for t in sorted(by_type):
    c, tot = by_type[t]
    print(f"    {t}: {c}/{tot}", flush=True)
print(f"[eval] merged -> {BASE}/pilot_eval_merged.json", flush=True)
print("[eval] DONE", flush=True)
