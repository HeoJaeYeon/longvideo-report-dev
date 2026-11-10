# ════════════════════════════════════════════════════════════════════════════
#  WorldMM + Deep-Reporter + MERIT 통합 이미지 (base) — "완성된 venv를 베이크"
#
#  Host : Ubuntu 22.04.5 / GPU RTX A6000 등 Ampere~Hopper (아래 CUDA_ARCH_LIST)
#  Stack: python 3.13 / torch 2.8.0+cu128 / transformers 4.57.6 / flash-attn 2.8.3
#
#  설계 요약:
#    - 빌드: /opt/venv 에 '서드파티 의존성'만 베이크.
#        envs/{pyproject.toml,uv.lock,.python-version} (= WorldMM 의존성 스펙, 소스 아님)로
#        `uv sync --no-install-project --no-install-package hipporag`
#          → worldmm·hipporag '패키지 자체'는 skip(소스 불필요), 그 외 전부(torch/flash-attn/hipporag deps…) 설치.
#        + `uv pip install -r envs/extras-integration.txt` (langchain/langgraph/flask/opencv, openai 2.54).
#    - 런타임: 소스는 '마운트된 실제 repo'에서 editable 연결(user.Dockerfile 가 최초 1회 자동):
#        worldmm, hipporag(=WorldMM/src/HippoRAG), merit = `pip install --no-deps -e`
#        deep_reporter = PYTHONPATH.
#    → Docker/ 는 WorldMM 소스를 품지 않음(의존성 lock 3개만). 세 repo 는 마운트에서 라이브.
#
#  ★자기완결 빌드: 컨텍스트 = Docker/ 하나(Makefile CONTEXT=.). 외부 WorldMM 경로 비의존.
#    make vendor 가 WorldMM 의 lock 3개 파일을 envs/ 로 동기화.
# ════════════════════════════════════════════════════════════════════════════

# 공식 uv 바이너리 (재현성 위해 태그 핀)
FROM ghcr.io/astral-sh/uv:0.9.5 AS uvbin

# 베이스: CUDA 12.8 devel (nvcc → flash-attn 소스 빌드, torch cu128 정합)
FROM nvidia/cuda:12.8.1-cudnn-devel-ubuntu22.04
LABEL maintainer="JaeYeon Heo <jyheo@rcv.sejong.ac.kr>"
LABEL description="WorldMM+Deep-Reporter+MERIT unified-venv(baked /opt/venv): torch2.8+cu128 / tf4.57.6"

ARG DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=Asia/Seoul

# ── 소스 컴파일 확장(flash-attn)의 타깃 CUDA 아키텍처 ──
#   8.0=A100 / 8.6=A6000·A40·A10·RTX3090 / 8.9=RTX4090·L40 / 9.0=H100.
#   (flash-attn 2.8.3 미지원: sm_75 Turing, sm_100/120 Blackwell.) 서버별 단축: --build-arg CUDA_ARCH_LIST="9.0"
ARG CUDA_ARCH_LIST="8.0;8.6;8.9;9.0"
ENV TORCH_CUDA_ARCH_LIST="${CUDA_ARCH_LIST}"
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH}
# flash-attn 병렬 컴파일 상한(과다 시 OOM)
ENV MAX_JOBS=8

# uv: 캐시/관리형 파이썬/프로젝트 환경 경로 고정. UV_COMPILE_BYTECODE 는 끔(nofile 고갈 이력).
ENV UV_CACHE_DIR=/opt/uv-cache \
    UV_PYTHON_INSTALL_DIR=/opt/uv-python \
    UV_PROJECT_ENVIRONMENT=/opt/venv \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

ARG PY_VERSION=3.13

# ── 1) 시스템 패키지: 빌드도구 + 영상/오디오 I/O + 공통 런타임 libs ──
#     libgl1-mesa-glx / libsm6 / libxext6 / libglib2.0-0 = opencv(cv2) 런타임 공유lib (MERIT 가 import).
RUN apt-get update && apt-get install -y -qq --no-install-recommends \
      apt-utils build-essential sudo cmake pkg-config ninja-build \
      git git-lfs curl wget vim less tree htop tmux rsync unzip locales \
      ca-certificates gnupg openssh-client tini \
      ffmpeg libavcodec-dev libavformat-dev libavutil-dev \
      libswscale-dev libavfilter-dev libavdevice-dev libsndfile1 \
      libglib2.0-0 libjpeg-dev libpng-dev libsm6 libxext6 libxrender1 \
      libgl1-mesa-glx \
      numactl libnuma-dev \
 && rm -rf /var/lib/apt/lists/* \
 && git lfs install --system || true

# ── 2) Node.js + Claude Code 최신판 (실패해도 빌드 계속) ──
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*
RUN npm install -g @anthropic-ai/claude-code@latest \
    || echo "[WARN] claude-code npm install failed - install manually inside container"

# ── 3) uv (공식 바이너리 COPY) ──
COPY --from=uvbin /uv /uvx /usr/local/bin/

# ── 4) /opt/venv 베이크 #1: WorldMM 서드파티 deps 설치 (소스 불필요) ──
#     envs/ 의 lock 3개만 COPY(= WorldMM 의존성 스펙; 소스/README 아님).
#     --no-install-project         : worldmm '패키지'는 skip(런타임 마운트 editable).
#     --no-install-package hipporag: hipporag '패키지'도 skip(런타임 마운트 editable). deps 는 설치됨.
WORKDIR /opt/wmbuild
COPY envs/pyproject.toml envs/uv.lock envs/.python-version ./
RUN uv python install ${PY_VERSION} && \
    uv sync --frozen --no-install-project --no-install-package hipporag && \
    echo "[base] /opt/venv WorldMM deps 설치 완료"

# ── 5) 빌드타임 검증 #1 (GPU 없는 빌드 → cuda.is_available() 미호출. worldmm/hipporag 는 미설치) ──
RUN /opt/venv/bin/python - <<'PY'
import sys, torch, transformers
print("[deps] python", sys.version.split()[0], "| torch", torch.__version__,
      "| built-cuda", torch.version.cuda, "| transformers", transformers.__version__)
try:
    import flash_attn; print("[deps] flash-attn", flash_attn.__version__)
except Exception as e:
    print("[deps] flash-attn import 실패:", e)
import importlib.util as u
for m in ("qwen3_vl","qwen2_5_vl","qwen2_vl"):
    print(f"[deps] transformers.{m}:", "OK" if u.find_spec(f"transformers.models.{m}") else "없음")
print("[deps] OK (worldmm/hipporag 는 런타임 editable)")
PY

# ── 6) /opt/venv 베이크 #2: 통합 extras(langchain/langgraph/flask/opencv + openai2.54) ──
#     런타임 참조와 '같은 파일'(단일 출처). /opt/venv 에 설치.
COPY envs/extras-integration.txt /tmp/extras-integration.txt
RUN uv pip install --python /opt/venv/bin/python -r /tmp/extras-integration.txt && \
    echo "[base] /opt/venv 통합 extras 설치 완료"

# ── 7) 빌드타임 검증 #2 (Deep-Report/MERIT/worldmm 소스는 런타임 연결 → 여기선 외부 패키지만) ──
RUN /opt/venv/bin/python - <<'PY'
import importlib.metadata as m
for p in ("langgraph","langchain-core","langchain-openai","openai","flask","opencv-python-headless"):
    print(f"[extras] {p}", m.version(p))
from langgraph.graph import StateGraph, END
from langgraph.config import get_stream_writer
from langchain_openai import ChatOpenAI
from langchain_core.runnables import RunnableConfig
import cv2; print("[extras] cv2", cv2.__version__)
print("[extras] core API import OK")
PY

# 정리: 빌드 입력(lock 3개 복사본)·임시 extras 제거. /opt/venv(완성 venv)만 남김.
RUN rm -rf /opt/wmbuild /tmp/extras-integration.txt
WORKDIR /

# 런타임(비루트)이 /opt/venv 에 worldmm/hipporag/merit editable 설치·sentinel 기록할 수 있도록 쓰기 권한.
RUN chmod -R a+rwX /opt/venv /opt/uv-cache /opt/uv-python
