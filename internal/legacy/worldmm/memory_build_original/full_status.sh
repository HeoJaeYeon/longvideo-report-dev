#!/bin/bash
# One-line progress/alert for the full-300 build. COMPLETE when done==300.
cd /data1/USER/workspace/VideoRAG/WorldMM
B=claude_output/full
TARGET=$(python3 -c "import json;print(len(json.load(open('claude_output/full/video_list.json')))))" 2>/dev/null || echo 50)
now=$(date '+%m-%d %H:%M:%S')
done=$(ls "$B/done" 2>/dev/null | wc -l)
failed=$(ls "$B/failed" 2>/dev/null | wc -l)
inprog=$(ls "$B/claims" 2>/dev/null | wc -l)
workers=$(pgrep -f "queue_worker.sh" | grep -vc pgrep)
# current video per worker (from worker logs)
cur=""
for g in 4 5 6 7; do
  v=$(grep "processing" "$B/logs/worker_gpu$g.log" 2>/dev/null | tail -1 | grep -oE "processing [A-Za-z0-9_-]+" | awk '{print $2}')
  [ -n "$v" ] && cur="$cur g$g:$v"
done
if [ "$done" -ge "$TARGET" ]; then echo "COMPLETE $now build done=$TARGET failed=$failed"; exit 0; fi
# all workers gone but not complete -> alert
if [ "$workers" -eq 0 ] && [ "$done" -lt 300 ]; then echo "ALERT-FATAL $now all queue workers exited (done=$done/$TARGET failed=$failed)"; exit 0; fi
gpu=$(nvidia-smi --query-gpu=memory.free,utilization.gpu --format=csv,noheader -i 4,5,6,7 2>/dev/null | tr '\n' ';')
echo "STATUS $now build done=$done/$TARGET failed=$failed inprogress=$inprog workers=$workers |$cur | GPU4-7[$gpu]"
