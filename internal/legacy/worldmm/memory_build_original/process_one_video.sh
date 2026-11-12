#!/bin/bash
# Full build pipeline for ONE video on a pinned GPU. Idempotent (skips finished
# sub-steps). All outputs under claude_output/full/. Usage: process_one_video.sh <GPU> <VID>
set -u
GPU=$1; VID=$2
ROOT=/data1/USER/workspace/VideoRAG/WorldMM
cd "$ROOT"; source .venv/bin/activate
export CUDA_VISIBLE_DEVICES=$GPU
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
B=claude_output/full
LOG=$B/logs/$VID.log
echo "[$VID] START gpu=$GPU $(date)" >> "$LOG"

# 1) transcribe
if [ ! -f "$B/transcript/$VID.srt" ]; then
  python data/Video-MME/utils/transcribe.py --input-path "data/Video-MME/data/$VID.mp4" \
    --output-path "$B/transcript/$VID.srt" --model distil-large-v3.5 --batch-size 1 >> "$LOG" 2>&1 || { echo "[$VID] FAIL transcribe"; exit 11; }
fi
# 2) caption (per-video via single transcript file)
if [ ! -f "$B/caption/$VID/10sec.json" ]; then
  python preprocess/episodic_memory/generate_fine_caption.py --video-path data/Video-MME/data \
    --transcript-path "$B/transcript/$VID.srt" --output-path "$B/caption" --model qwen3vl-8b --unit-time 10 >> "$LOG" 2>&1 || { echo "[$VID] FAIL caption"; exit 12; }
fi
# 3) multiscale (single-video dir)
if [ ! -f "$B/caption/$VID/10min.json" ]; then
  python -m worldmm.memory.episodic.multiscale --caption_dir "$B/caption/$VID" --model qwen3vl-8b \
    --windows "30,180,600" --granularity_names "30sec,3min,10min" --perspective general >> "$LOG" 2>&1 || { echo "[$VID] FAIL multiscale"; exit 13; }
fi
# 4) build_memory (isolated single-video caption dir -> shared metadata)
# Run each step as a SEPARATE process. With --step all, the parent holds the
# LLM+embedding (~24GB) on the GPU while spawning the visual worker, which then
# OOMs. Separate processes release memory between steps, so visual (VLM2Vec
# ~5GB) runs clean. Each step is idempotent (skips already-built videos).
mkdir -p "$B/work/$VID/cap"
ln -sfn "$ROOT/$B/caption/$VID" "$B/work/$VID/cap/$VID"
for STEP in episodic semantic; do
  python preprocess/build_memory.py --caption-dir "$B/work/$VID/cap" --output-dir "$B/metadata" \
    --model qwen3vl-8b --step "$STEP" --gpu 0 --num-frames 10 >> "$LOG" 2>&1 \
    || { echo "[$VID] FAIL build_memory-$STEP $(date)" >> "$LOG"; exit 14; }
done
# visual: build_memory's visual worker sets CUDA_VISIBLE_DEVICES=<--gpu token>
# for its child, which would land on PHYSICAL GPU 0 if we pass "--gpu 0" (the
# child ignores the parent's CUDA_VISIBLE_DEVICES). So unset CUDA_VISIBLE_DEVICES
# and pass the real physical GPU number ($GPU, always 4-7). Retry on contention.
vok=0
for att in $(seq 1 15); do
  while :; do
    f=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits -i $GPU 2>/dev/null)
    [ -n "$f" ] && [ "$f" -ge 12000 ] && break
    sleep 60
  done
  if env -u CUDA_VISIBLE_DEVICES python preprocess/build_memory.py --caption-dir "$B/work/$VID/cap" --output-dir "$B/metadata" \
       --model qwen3vl-8b --step visual --gpu "$GPU" --num-frames 10 >> "$LOG" 2>&1; then vok=1; break; fi
  echo "[$VID] visual attempt#$att failed, retry $(date)" >> "$LOG"; sleep 60
done
[ "$vok" = 1 ] || { echo "[$VID] FAIL build_memory-visual $(date)" >> "$LOG"; exit 14; }

# verify all 3 memories present
if [ -d "$B/metadata/episodic_memory/$VID" ] && [ -d "$B/metadata/semantic_memory/$VID" ] && [ -f "$B/metadata/visual_memory/$VID/visual_embeddings.pkl" ]; then
  echo "[$VID] DONE $(date)" >> "$LOG"; exit 0
else
  echo "[$VID] FAIL incomplete-metadata $(date)" >> "$LOG"; exit 15
fi
