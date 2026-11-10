#!/bin/bash
# Offline WorldMM episodic pre-indexing on one GPU (idempotent; finished videos are skipped).
# Usage: ./run_prebuild.sh <GPU_ID> [--videos a,b] [--shard K/N]
# Plan only (no GPU, no writes):
#   /opt/venv/bin/python prebuild_episodic_index.py --config config.yaml --dry-run
set -euo pipefail

HERE="$(cd "$(dirname "$0")" && pwd)"
# WorldMM checkout: $WORLDMM_DIR (set in the videorag_report container), else the one next to report_framework/.
WORLDMM="${WORLDMM_DIR:-$HERE/../WorldMM}"
# Python with worldmm/hipporag installed (default: the container venv); override with RF_PYTHON.
PY="${RF_PYTHON:-/opt/venv/bin/python}"
GPU="${1:?usage: run_prebuild.sh <GPU_ID> [--videos a,b] [--shard K/N]}"
shift

export CUDA_VISIBLE_DEVICES="$GPU"
export PYTORCH_CUDA_ALLOC_CONF=expandable_segments:True

cd "$WORLDMM"   # same working directory as WorldMM eval
# /opt/venv = container venv with worldmm/hipporag editable installs (HF_HOME is set from config.yaml).
exec "$PY" "$HERE/prebuild_episodic_index.py" --config "$HERE/config.yaml" "$@"
