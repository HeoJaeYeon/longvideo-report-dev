#!/bin/bash
# Queue worker: repeatedly claim the next unprocessed video and build it on GPU $1.
# Waits for the GPU to have enough free memory (avoids OOM from other users).
# Atomic claim via mkdir. Idempotent/resumable. Usage: queue_worker.sh <GPU>
set -u
GPU=$1
ROOT=/data1/USER/workspace/VideoRAG/WorldMM
cd "$ROOT"; source .venv/bin/activate
B=claude_output/full
WLOG=$B/logs/worker_gpu$GPU.log
MIN_FREE=28000   # MiB; build_memory (qwen3vl + embedding) needs ~24GB
mapfile -t VIDS < <(python -c "import json;[print(v) for v in json.load(open('$B/video_list.json'))]")
echo "[worker$GPU] START $(date) videos=${#VIDS[@]}" >> "$WLOG"

for VID in "${VIDS[@]}"; do
  # skip finished
  [ -d "$B/done/$VID" ] && continue
  # atomic claim
  mkdir "$B/claims/$VID" 2>/dev/null || continue
  # wait until GPU free enough (other users' contention)
  while :; do
    free=$(nvidia-smi --query-gpu=memory.free --format=csv,noheader,nounits -i $GPU 2>/dev/null)
    [ -n "$free" ] && [ "$free" -ge "$MIN_FREE" ] && break
    sleep 60
  done
  echo "[worker$GPU] processing $VID $(date)" >> "$WLOG"
  if bash "$B/process_one_video.sh" "$GPU" "$VID"; then
    mkdir -p "$B/done/$VID"
    echo "[worker$GPU] done $VID $(date)" >> "$WLOG"
  else
    rc=$?
    mkdir -p "$B/failed/$VID"; echo "$rc" > "$B/failed/$VID/rc"
    echo "[worker$GPU] FAILED $VID rc=$rc $(date)" >> "$WLOG"
    # release claim so a later retry pass can re-attempt
    rmdir "$B/claims/$VID" 2>/dev/null || true
  fi
done
echo "[worker$GPU] QUEUE-EMPTY $(date)" >> "$WLOG"
