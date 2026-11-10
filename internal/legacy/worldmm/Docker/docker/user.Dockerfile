# ════════════════════════════════════════════════════════════
#  WorldMM 사용자 오버레이 (user)
#  base 위에 호스트 UID:GID 사용자 생성 + 런타임 repo/.venv 자동 PATH
#  정책: 의존성 = 이미지(캐시) / 환경 = 마운트 repo 의 .venv (uv sync 로 생성)
# ════════════════════════════════════════════════════════════
ARG IMAGE_NAME=
FROM $IMAGE_NAME

ARG UID=
ARG GID=
ARG USER_NAME=

# 호스트 UID:GID 매칭 그룹/사용자 + NOPASSWD sudo (기존 이미지 규약 유지)
RUN groupadd -g ${GID} ${USER_NAME} 2>/dev/null || true && \
    useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USER_NAME} && \
    echo "$USER_NAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USER_NAME && \
    chmod 0440 /etc/sudoers.d/$USER_NAME

USER $USER_NAME
SHELL ["/bin/bash", "-lc"]

RUN mkdir -p ~/.cache ~/.claude ~/.config

# 런타임 환경 = 마운트된 WorldMM repo 의 .venv (최초 1회 `uv sync` 로 생성)
#  → 공식 script 의 `source .venv/bin/activate` 와 정합. PATH 에 미리 넣어 sync 후 python 즉시 사용.
RUN { \
      echo ''; \
      echo '# ===== WorldMM project ====='; \
      echo "export WORLDMM_DIR=/data1/${USER_NAME}/workspace/VideoRAG/WorldMM"; \
      echo 'export VIRTUAL_ENV_DISABLE_PROMPT=1'; \
      echo '[ -f "$WORLDMM_DIR/.venv/bin/activate" ] && source "$WORLDMM_DIR/.venv/bin/activate"'; \
      echo '[ -n "${VIRTUAL_ENV:-}" ] && [ "${PS1#(worldmm) }" = "$PS1" ] && PS1="(worldmm) ${PS1:-}"'; \
      echo '# uv: 캐시/관리형 파이썬은 이미지(마운트 밖) 고정 경로 사용, 환경은 repo/.venv(기본값)'; \
      echo 'export UV_CACHE_DIR=/opt/uv-cache'; \
      echo 'export UV_PYTHON_INSTALL_DIR=/opt/uv-python'; \
      echo 'export TOKENIZERS_PARALLELISM=false'; \
      echo 'export TORCH_CUDA_ARCH_LIST=8.6'; \
      echo 'export OMP_NUM_THREADS=8'; \
      echo '# --- NCCL (단일 노드 A6000 x8) ---'; \
      echo 'export NCCL_DEBUG=WARN'; \
      echo 'export NCCL_IB_DISABLE=1'; \
      echo '# NCCL_SOCKET_IFNAME 은 자동 선택에 맡김(멀티노드 확장 시 lo 강제 회피)'; \
      echo "alias wmsync='cd \$WORLDMM_DIR && uv sync'   # 최초 1회 / 의존성 변경 시"; \
    } >> ~/.bashrc

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/bin/bash"]
