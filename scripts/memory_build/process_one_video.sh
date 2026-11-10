#!/bin/bash
# Full WorldMM memory build for ONE video on a pinned GPU. Idempotent (skips finished sub-steps).
# Usage: process_one_video.sh <GPU> <VID>        (normally started by queue_worker.sh)
#
# How it works: this script only calls the original WorldMM programs, from the WorldMM checkout, and passes
# every output location as an argument (no WorldMM code is changed; the input video path stays relative to the
# WorldMM root because generate_fine_caption.py records it in each caption entry as `video_path`):
#   1) data/Video-MME/utils/transcribe.py               -> $WORLDMM_MEMORY_DIR/transcript/<VID>.srt
#   2) preprocess/episodic_memory/generate_fine_caption.py -> $WORLDMM_MEMORY_DIR/caption/<VID>/10sec.json
#   3) python -m worldmm.memory.episodic.multiscale     -> $WORLDMM_MEMORY_DIR/caption/<VID>/{30sec,3min,10min}.json
#   4) preprocess/build_memory.py --step episodic|semantic|visual
#                                                       -> $WORLDMM_MEMORY_DIR/metadata/{episodic,semantic,visual}_memory/<VID>/
#   Log: $WORLDMM_MEMORY_DIR/logs/<VID>.log. Exit codes 11-15 name the failed step (below).
#
# Settings (environment variables; defaults = the layout VideoRAG/{WorldMM, report_framework}):
#   WORLDMM_DIR         WorldMM checkout (container sets it)  default: <report_framework>/../WorldMM
#   WORLDMM_MEMORY_DIR  output folder                         default: $WORLDMM_DIR/output/memory/videomme_long_qwen3vl-8b
#   WORLDMM_VENV        venv with WorldMM installed           default: $WORLDMM_DIR/.venv (the venv the 50-video memory
#                       was built with in 2026-09; not /opt/venv)
# Fixed values kept from the 2026-09 build: model qwen3vl-8b, Whisper distil-large-v3.5 (batch 1), unit time 10 s,
# multiscale windows 30/180/600 s, 10 frames per segment for VLM2Vec, >= 12,000 MiB free before the visual step.
# Moved here on 2026-11-10 from WorldMM/claude_output/full/process_one_video.sh (paths only changed: the output
# folder is a setting, build bookkeeping lives in build_state/, the work/ caption link is relative).
set -u
GPU=$1; VID=$2
HERE="$(cd "$(dirname "$0")" && pwd)"
WORLDMM_DIR="${WORLDMM_DIR:-$HERE/../../../WorldMM}"
WORLDMM_MEMORY_DIR="${WORLDMM_MEMORY_DIR:-$WORLDMM_DIR/output/memory/videomme_long_qwen3vl-8b}"
WORLDMM_VENV="${WORLDMM_VENV:-$WORLDMM_DIR/.venv}"
cd "$WORLDMM_DIR"; source "$WORLDMM_VENV/bin/activate"
export CUDA_VISIBLE_DEVICES=$GPU
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True
B=$WORLDMM_MEMORY_DIR
mkdir -p "$B/logs" "$B/transcript" "$B/caption" "$B/metadata"
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
# build_memory processes every video under --caption-dir, so it gets a folder that links only this video's captions
# (relative link, so the memory folder can be moved without breaking it).
mkdir -p "$B/build_state/work/$VID/cap"
ln -sfnr "$B/caption/$VID" "$B/build_state/work/$VID/cap/$VID"
for STEP in episodic semantic; do
  python preprocess/build_memory.py --caption-dir "$B/build_state/work/$VID/cap" --output-dir "$B/metadata" \
    --model qwen3vl-8b --step "$STEP" --gpu 0 --num-frames 10 >> "$LOG" 2>&1 \
    || { echo "[$VID] FAIL build_memory-$STEP $(date)" >> "$LOG"; exit 14; }
done
# visual: build_memory's visual worker sets CUDA_VISIBLE_DEVICES=<--gpu token>
# for its child, which would land on PHYSICAL GPU 0 if we pass "--gpu 0" (the
# child ignores the parent's CUDA_VISIBLE_DEVICES). So unset CUDA_VISIBLE_DEVICES
# and pass the real physical GPU number ($GPU). Retry on contention.
vok=0
for att in $(seq 1 15); do
  while :; do
    f=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits -i $GPU 2>/dev/null)
    [ -n "$f" ] && [ "$f" -ge 12000 ] && break
    sleep 60
  done
  if env -u CUDA_VISIBLE_DEVICES python preprocess/build_memory.py --caption-dir "$B/build_state/work/$VID/cap" --output-dir "$B/metadata" \
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
