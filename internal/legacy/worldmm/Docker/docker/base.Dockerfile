# ════════════════════════════════════════════════════════════
#  WorldMM 통합 이미지 (base) — 전략 B (캐시 프리워밍 + 런타임 repo .venv)
#  Host : Ubuntu 22.04.5 / GPU RTX A6000 ×8 (sm_86, 48GB)
#  Stack: python 3.13 / torch 2.8.0+cu128 / transformers 4.57.6 / flash-attn 2.8.3
#         (버전의 진실의 원천 = 프로젝트 루트 pyproject.toml + uv.lock)
#  정책 : 빌드 때는 '도구 + uv 캐시(flash-attn 컴파일 결과)'만 굽고,
#         런타임에 마운트된 repo 에서 `uv sync` → repo/.venv 생성(캐시 웜, 무재컴파일).
#         → 공식 script(`source .venv/bin/activate`) 무수정 호환 + host source 라이브 반영.
#  주의 : 빌드 컨텍스트 = WorldMM 루트 (Makefile 이 context 를 '..' 로 지정)
# ════════════════════════════════════════════════════════════

# 공식 uv 바이너리 (재현성 위해 태그 핀. 실재 태그인지 확인/조정: ghcr.io/astral-sh/uv tags)
FROM ghcr.io/astral-sh/uv:0.9.5 AS uvbin

# 베이스: CUDA 12.8 devel (nvcc → flash-attn/torchcodec 소스 빌드, torch cu128 정합)
FROM nvidia/cuda:12.8.1-cudnn-devel-ubuntu22.04
LABEL maintainer="JaeYeon Heo <jyheo@rcv.sejong.ac.kr>"
LABEL description="WorldMM base (strategy B): torch2.8+cu128 / transformers4.57.6 / uv cache prewarmed"

ARG DEBIAN_FRONTEND=noninteractive
ENV LANG=C.UTF-8 LC_ALL=C.UTF-8 TZ=Asia/Seoul

# ── A6000 = sm_86 만 타깃 → 확장모듈 컴파일 시간 단축 ──
ENV TORCH_CUDA_ARCH_LIST="8.6"
ENV CUDA_HOME=/usr/local/cuda
ENV PATH=/usr/local/cuda/bin:${PATH}
ENV LD_LIBRARY_PATH=/usr/local/cuda/lib64:${LD_LIBRARY_PATH}
# flash-attn 컴파일 메모리 폭주 방지 (16 → OOM 위험)
ENV MAX_JOBS=8

# ── uv: 캐시/관리형 파이썬을 '마운트 밖' 고정 경로에 (런타임 sync 가 재사용) ──
# 주의: UV_COMPILE_BYTECODE 는 켜지 않는다.
#  - 프리워밍 venv 는 곧 삭제하므로 .pyc 컴파일이 무의미하고,
#  - 컴파일 단계가 다수 인터프리터를 띄워 파일디스크립터(nofile)를 고갈시켜 빌드가 실패했음
#    (error: No file descriptors available / os error 24).
ENV UV_CACHE_DIR=/opt/uv-cache \
    UV_PYTHON_INSTALL_DIR=/opt/uv-python \
    UV_LINK_MODE=copy \
    PYTHONUNBUFFERED=1 \
    PIP_DISABLE_PIP_VERSION_CHECK=1

ARG PY_VERSION=3.13

# ------------------------------------------------------------
# 1) 시스템 패키지 (빌드도구 + 영상/오디오 I/O + 공통 런타임 libs)
# ------------------------------------------------------------
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

# ------------------------------------------------------------
# 2) Node.js + Claude Code (실패해도 빌드 계속)
# ------------------------------------------------------------
RUN curl -fsSL https://deb.nodesource.com/setup_20.x | bash - && \
    apt-get install -y --no-install-recommends nodejs && \
    rm -rf /var/lib/apt/lists/*
RUN npm install -g @anthropic-ai/claude-code \
    || echo "[WARN] claude-code npm install failed - install manually inside container"

# ------------------------------------------------------------
# 3) uv (공식 바이너리 COPY)
# ------------------------------------------------------------
COPY --from=uvbin /uv /uvx /usr/local/bin/

# ------------------------------------------------------------
# 4) uv 캐시 프리워밍: uv.lock 전체를 임시 venv 로 1회 설치·컴파일
#    → flash-attn 등 빌드 결과가 /opt/uv-cache 에 적재. 임시 venv 는 제거(캐시만 유지).
#    (런타임에 repo 에서 `uv sync` 하면 이 캐시를 재사용 → 무재컴파일)
# ------------------------------------------------------------
WORKDIR /opt/worldmm/prewarm
COPY pyproject.toml uv.lock .python-version README.md ./
COPY src ./src
RUN uv python install ${PY_VERSION} && \
    UV_PROJECT_ENVIRONMENT=/opt/worldmm/prewarm/.venv uv sync --frozen && \
    echo "[base] prewarm uv sync 완료 — 빌드 검증 시작"

# ------------------------------------------------------------
# 5) 빌드타임 검증 (임시 venv 로. GPU 없는 빌드 단계이므로 cuda.is_available()은 호출하지 않음)
# ------------------------------------------------------------
RUN /opt/worldmm/prewarm/.venv/bin/python - <<'PY'
import sys, torch, transformers
print("[worldmm] python", sys.version.split()[0])
print("[worldmm] torch", torch.__version__, "| built-cuda", torch.version.cuda)
print("[worldmm] transformers", transformers.__version__)
try:
    import flash_attn; print("[worldmm] flash-attn", flash_attn.__version__)
except Exception as e:
    print("[worldmm] flash-attn import 실패:", e)
import importlib.util as u
for m in ("qwen3_vl","qwen2_5_vl","qwen2_vl"):
    print(f"[worldmm] transformers.{m:10s}:", "OK" if u.find_spec(f"transformers.models.{m}") else "없음")
import worldmm, hipporag
print("[worldmm] worldmm import from:", worldmm.__file__)   # 빌드 시엔 prewarm 사본; 런타임엔 host repo
print("[worldmm] hipporag OK")
PY

# 임시 venv/소스 제거 — '캐시(/opt/uv-cache) + 관리형 파이썬(/opt/uv-python)'만 이미지에 남김
RUN rm -rf /opt/worldmm/prewarm
WORKDIR /

# 런타임 `uv sync`(비루트 사용자)가 캐시/파이썬을 읽고 쓸 수 있도록
RUN chmod -R a+rwX /opt/uv-cache /opt/uv-python
