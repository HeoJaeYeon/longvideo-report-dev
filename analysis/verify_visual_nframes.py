"""
Check how many frames per 10sec segment the stored WorldMM visual embeddings were made from (2026-11-03, CPU only).
The preprocessing log does not record --num-frames; process_one_video.sh (edited 2026-10-21, after the build) says 10.
Re-embed a few segments with VLM2Vec-V2.0 on CPU (bfloat16, sdpa; reproduce_retrieval_cpu.cpu_vlm2vec) with 10 and
with 16 frames (WorldMM default) and compare each with the stored vector (cosine).
Usage: python analysis/verify_visual_nframes.py [--video=-QuCz7kxBr8] [--segments 00004000,00344000]
Output: analysis/visual_nframes_check_<vid>.json
"""
import argparse, json, os, pickle, sys

RF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RF)
sys.path.insert(0, os.path.join(RF, "analysis"))
import numpy as np
from reproduce_retrieval_cpu import cpu_vlm2vec

WM = "/data1/jyheo/workspace/VideoRAG/WorldMM"


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", default="-QuCz7kxBr8")
    ap.add_argument("--segments", default="00004000,00344000")
    a = ap.parse_args()
    stored = pickle.load(open(f"{WM}/claude_output/full/metadata/visual_memory/{a.video}/visual_embeddings.pkl", "rb"))
    model = cpu_vlm2vec("VLM2Vec/VLM2Vec-V2.0")
    vp = f"{WM}/data/Video-MME/data/{a.video}.mp4"
    rows = []
    for key in a.segments.split(","):
        s0 = int(key[0:2]) * 3600 + int(key[2:4]) * 60 + int(key[4:6])
        ref = stored[key]
        for nf in (10, 16):
            e = model.encode_video([{"video": vp, "video_start": float(s0), "video_end": float(s0 + 10)}], nframes=nf, batch_size=1)[0]
            cos = float(np.dot(e, ref) / np.linalg.norm(e) / np.linalg.norm(ref))
            rows.append({"segment": key, "nframes": nf, "cosine_to_stored": round(cos, 5)})
            print(rows[-1], flush=True)
    out = os.path.join(RF, "analysis", f"visual_nframes_check_{a.video}.json")
    json.dump({"video_id": a.video, "embedding": "VLM2Vec-V2.0 CPU bf16 sdpa", "rows": rows}, open(out, "w"), indent=1)
    print("wrote", out)


if __name__ == "__main__":
    main()
