#!/bin/bash
# Queue worker: repeatedly claim the next unprocessed video and build it on GPU $1 (process_one_video.sh).
# Waits for the GPU to have enough free memory (avoids OOM from other users).
# Atomic claim via mkdir. Idempotent/resumable. Usage: queue_worker.sh <GPU>
#   One worker per GPU, e.g. `setsid bash queue_worker.sh 6 &` and `setsid bash queue_worker.sh 7 &`; progress: full_status.sh.
#
# Settings: same environment variables as process_one_video.sh (WORLDMM_DIR, WORLDMM_MEMORY_DIR, WORLDMM_VENV).
#   Video list : $WORLDMM_MEMORY_DIR/lists/video_list.json (JSON list of video ids)
#   Bookkeeping: $WORLDMM_MEMORY_DIR/build_state/{claims,done,failed}/<VID>/ (failed/<VID>/rc = exit code)
#   Worker log : $WORLDMM_MEMORY_DIR/logs/worker_gpu<GPU>.log
#   MIN_FREE   : 28,000 MiB free on the GPU before a video starts (fixed value kept from the 2026-09 build)
# A claim is kept after success (done/ decides skipping); a failed video's claim is released for a later pass.
# Moved here on 2026-11-10 from WorldMM/claude_output/full/queue_worker.sh (paths only changed).
set -u
GPU=$1
HERE="$(cd "$(dirname "$0")" && pwd)"
export WORLDMM_DIR="${WORLDMM_DIR:-$HERE/../../../WorldMM}"
export WORLDMM_MEMORY_DIR="${WORLDMM_MEMORY_DIR:-$WORLDMM_DIR/output/memory/videomme_long_qwen3vl-8b}"
export WORLDMM_VENV="${WORLDMM_VENV:-$WORLDMM_DIR/.venv}"
cd "$WORLDMM_DIR"; source "$WORLDMM_VENV/bin/activate"
B=$WORLDMM_MEMORY_DIR
S=$B/build_state
mkdir -p "$B/logs" "$S/claims" "$S/done" "$S/failed"
WLOG=$B/logs/worker_gpu$GPU.log
MIN_FREE=28000   # MiB; build_memory (qwen3vl + embedding) needs ~24GB
mapfile -t VIDS < <(python -c "import json;[print(v) for v in json.load(open('$B/lists/video_list.json'))]")
echo "[worker$GPU] START $(date) videos=${#VIDS[@]}" >> "$WLOG"

for VID in "${VIDS[@]}"; do
  # skip finished
  [ -d "$S/done/$VID" ] && continue
  # atomic claim
  mkdir "$S/claims/$VID" 2>/dev/null || continue
  # wait until GPU free enough (other users' contention)
  while :; do
    free=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits -i $GPU 2>/dev/null)
    [ -n "$free" ] && [ "$free" -ge "$MIN_FREE" ] && break
    sleep 60
  done
  echo "[worker$GPU] processing $VID $(date)" >> "$WLOG"
  if bash "$HERE/process_one_video.sh" "$GPU" "$VID"; then
    mkdir -p "$S/done/$VID"
    echo "[worker$GPU] done $VID $(date)" >> "$WLOG"
  else
    rc=$?
    mkdir -p "$S/failed/$VID"; echo "$rc" > "$S/failed/$VID/rc"
    echo "[worker$GPU] FAILED $VID rc=$rc $(date)" >> "$WLOG"
    # release claim so a later retry pass can re-attempt
    rmdir "$S/claims/$VID" 2>/dev/null || true
  fi
done
echo "[worker$GPU] QUEUE-EMPTY $(date)" >> "$WLOG"
