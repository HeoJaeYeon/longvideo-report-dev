#!/bin/bash
# Episodic pre-indexing with HTTP OpenIE (decision 1 = A).
# Starts one local_llm_server.py per LLM GPU (19,000 MiB cap each), waits for /health, runs
# prebuild_episodic_index.py on the indexer GPU (embedding only, 19,000 MiB cap), then stops
# only the servers it started. Idempotent: finished videos are skipped (done markers).
# Usage: ./run_prebuild_http.sh <LLM_GPUS e.g. 4,5,6> <INDEXER_GPU e.g. 7> [prebuild args: --videos a,b | --shard K/N]
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
# WorldMM checkout: $WORLDMM_DIR (set in the videorag_report container), else the one next to report_framework/.
WORLDMM="${WORLDMM_DIR:-$HERE/../WorldMM}"
# Python with worldmm/hipporag installed (default: the container venv); override with RF_PYTHON.
PY="${RF_PYTHON:-/opt/venv/bin/python}"
LLM_GPUS="${1:?usage: run_prebuild_http.sh <LLM_GPUS> <INDEXER_GPU> [args]}"
INDEXER_GPU="${2:?usage: run_prebuild_http.sh <LLM_GPUS> <INDEXER_GPU> [args]}"
shift 2
BASE_PORT="${PREBUILD_LLM_BASE_PORT:-18710}"
LOG_DIR="$HERE/logs"
mkdir -p "$LOG_DIR"
STAMP="$(date +%Y%m%d_%H%M%S)"

PIDS=()
cleanup() { for p in "${PIDS[@]}"; do kill "$p" 2>/dev/null || true; done; wait 2>/dev/null || true; }
trap cleanup EXIT

ENDPOINTS=()
i=0
for g in ${LLM_GPUS//,/ }; do
  port=$((BASE_PORT + i))
  CUDA_VISIBLE_DEVICES="$g" PYTHONDONTWRITEBYTECODE=1 "$PY" -B "$HERE/tests/run_llm_server_capped.py" "$port" \
      > "$LOG_DIR/prebuild_llm_${STAMP}_gpu${g}.log" 2>&1 &
  PIDS+=($!)
  ENDPOINTS+=("http://127.0.0.1:${port}/v1")
  echo "LLM server pid=$! gpu=$g port=$port"
  i=$((i + 1))
done

for e in "${ENDPOINTS[@]}"; do
  base="${e%/v1}"
  for _ in $(seq 1 120); do
    curl -sf "$base/health" > /dev/null && break
    for p in "${PIDS[@]}"; do kill -0 "$p" 2>/dev/null || { echo "LLM server $p exited"; exit 1; }; done
    sleep 5
  done
  curl -sf "$base/health" > /dev/null || { echo "$base not ready"; exit 1; }
done
echo "LLM servers ready: ${ENDPOINTS[*]}"

cd "$WORLDMM"
CUDA_VISIBLE_DEVICES="$INDEXER_GPU" PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True PYTHONDONTWRITEBYTECODE=1 \
  "$PY" -B "$HERE/prebuild_episodic_index.py" --config "$HERE/config.yaml" \
  --llm-endpoints "$(IFS=,; echo "${ENDPOINTS[*]}")" --gpu-mem-cap-mib 19000 "$@"
