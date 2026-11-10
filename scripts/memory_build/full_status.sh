#!/bin/bash
# One-line progress/alert for the memory build run by queue_worker.sh (read-only: counts markers, reads worker logs,
# queries nvidia-smi). Prints COMPLETE when done == number of videos in the video list. Usage: full_status.sh
#
# Settings: WORLDMM_DIR, WORLDMM_MEMORY_DIR (same defaults as process_one_video.sh); target = length of
#   $WORLDMM_MEMORY_DIR/lists/video_list.json (50 if it cannot be read).
# Fixed values kept from the 2026-09 build (edit here for another setup):
#   GPUS=4 5 6 7   GPUs whose worker logs (current video) and free memory / utilization are shown
#   300            the ALERT-FATAL check below still compares done with 300 (the original 300-video plan), not with
#                  TARGET; it only matters when all workers have exited before TARGET is reached
# Moved here on 2026-11-10 from WorldMM/claude_output/full/full_status.sh (paths changed; the TARGET line had one ')'
# too many, so the original always fell back to 50 — the same value as the current 50-video list).
HERE="$(cd "$(dirname "$0")" && pwd)"
WORLDMM_DIR="${WORLDMM_DIR:-$HERE/../../../WorldMM}"
WORLDMM_MEMORY_DIR="${WORLDMM_MEMORY_DIR:-$WORLDMM_DIR/output/memory/videomme_long_qwen3vl-8b}"
cd "$WORLDMM_DIR"
B=$WORLDMM_MEMORY_DIR
S=$B/build_state
GPUS="4 5 6 7"
TARGET=$(python3 -c "import json;print(len(json.load(open('$B/lists/video_list.json'))))" 2>/dev/null || echo 50)
now=$(date '+%m-%d %H:%M:%S')
done=$(ls "$S/done" 2>/dev/null | wc -l)
failed=$(ls "$S/failed" 2>/dev/null | wc -l)
inprog=$(ls "$S/claims" 2>/dev/null | wc -l)
workers=$(pgrep -f "queue_worker.sh" | grep -vc pgrep)
# current video per worker (from worker logs)
cur=""
for g in $GPUS; do
  v=$(grep "processing" "$B/logs/worker_gpu$g.log" 2>/dev/null | tail -1 | grep -oE "processing [A-Za-z0-9_-]+" | awk '{print $2}')
  [ -n "$v" ] && cur="$cur g$g:$v"
done
if [ "$done" -ge "$TARGET" ]; then echo "COMPLETE $now build done=$TARGET failed=$failed"; exit 0; fi
# all workers gone but not complete -> alert
if [ "$workers" -eq 0 ] && [ "$done" -lt 300 ]; then echo "ALERT-FATAL $now all queue workers exited (done=$done/$TARGET failed=$failed)"; exit 0; fi
gpu=$(nvidia-smi --query-gpu=memory.free,utilization.gpu --format=csv,noheader -i ${GPUS// /,} 2>/dev/null | tr '\n' ';')
echo "STATUS $now build done=$done/$TARGET failed=$failed inprogress=$inprog workers=$workers |$cur | GPU4-7[$gpu]"
