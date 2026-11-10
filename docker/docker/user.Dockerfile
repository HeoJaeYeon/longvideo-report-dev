# ════════════════════════════════════════════════════════════════════════════
#  통합 이미지 사용자 오버레이 (user)
#    base의 완성된 /opt/venv 위에 호스트 UID:GID 사용자 + 자동 환경 + 소스 editable 자동연결.
#    정책: 의존성 = 이미지(/opt/venv 베이크) / 라이브 소스(worldmm·merit·deep_reporter) = 마운트 연결.
#    → 컨테이너 진입 즉시 사용(최초 1회 수 초 자동 editable). 수동 intsetup/느린 uv sync 불필요.
# ════════════════════════════════════════════════════════════════════════════
ARG IMAGE_NAME=
FROM $IMAGE_NAME

ARG UID=
ARG GID=
ARG USER_NAME=
# 컨테이너 안 프로젝트 루트(= Makefile MOUNT_ROOT 와 일치. 마운트 지점). 호스트 경로와 무관.
ARG MOUNT_ROOT=/workspace/VideoRAG

# 호스트 UID:GID 매칭 사용자 + NOPASSWD sudo (기존 이미지 규약 유지)
RUN groupadd -g ${GID} ${USER_NAME} 2>/dev/null || true && \
    useradd -m -u ${UID} -g ${GID} -s /bin/bash ${USER_NAME} && \
    echo "$USER_NAME ALL=(root) NOPASSWD:ALL" > /etc/sudoers.d/$USER_NAME && \
    chmod 0440 /etc/sudoers.d/$USER_NAME

USER $USER_NAME
SHELL ["/bin/bash", "-lc"]
RUN mkdir -p ~/.cache ~/.claude ~/.config

# ── .bashrc: /opt/venv 자동 활성 + 환경변수 + 소스 editable 자동연결(최초 1회) + 점검 ──
#    색상 CLI: useradd -m 이 /etc/skel/.bashrc(우분투 색상 블록) 복사 → 아래는 그 '뒤'에 append.
#              Makefile 이 TERM=xterm-256color 전달 → 컬러 프롬프트/ls/grep 유지.
RUN { \
      echo ''; \
      echo '# ===== 통합 프로젝트 경로 (컨테이너 고정 루트 = MOUNT_ROOT, 호스트 경로 무관) ====='; \
      echo "export WORLDMM_DIR=${MOUNT_ROOT}/WorldMM"; \
      echo "export MERIT_DIR=${MOUNT_ROOT}/MERIT"; \
      echo "export DEEPREPORTER_DIR=${MOUNT_ROOT}/Deep-Report"; \
      echo ''; \
      echo '# 통합 venv = 이미지에 베이크된 /opt/venv (세 repo 공유). 공식 script 의 source .venv 대신 이 환경 사용.'; \
      echo 'export VIRTUAL_ENV_DISABLE_PROMPT=1'; \
      echo 'source /opt/venv/bin/activate'; \
      echo '[ "${PS1#(videorag_report) }" = "$PS1" ] && PS1="(videorag_report) ${PS1:-}"'; \
      echo ''; \
      echo '# uv/런타임 환경변수 (캐시·관리형 파이썬은 이미지 고정 경로)'; \
      echo 'export UV_CACHE_DIR=/opt/uv-cache'; \
      echo 'export UV_PYTHON_INSTALL_DIR=/opt/uv-python'; \
      echo 'export TOKENIZERS_PARALLELISM=false'; \
      echo 'export TORCH_CUDA_ARCH_LIST="8.0;8.6;8.9;9.0"'; \
      echo 'export OMP_NUM_THREADS=8'; \
      echo 'export NCCL_DEBUG=WARN'; \
      echo 'export NCCL_IB_DISABLE=1'; \
      echo '# deep_reporter 는 설치형이 아님 → PYTHONPATH 로 import 가능하게'; \
      echo 'export PYTHONPATH="$DEEPREPORTER_DIR${PYTHONPATH:+:$PYTHONPATH}"'; \
      echo ''; \
      echo '# ===== 소스 editable 연결 (tolerant: repo 가 있을 때만) ====='; \
      echo '#  worldmm/hipporag/merit 를 "마운트된 repo 가 존재하면" editable 연결(deps 는 /opt/venv 에 이미 있음 → --no-deps).'; \
      echo '#  repo 가 아직 없어도(= git clone 전) 컨테이너는 정상 동작. clone 후 진입 또는 수동 intsetup 으로 연결.'; \
      echo '#  intsetup: 존재하는 repo 만 골라 설치(부분 clone 안전). deep_reporter 는 PYTHONPATH 라 설치 불필요.'; \
      echo 'intsetup() { local t=(); [ -d "$WORLDMM_DIR/src/worldmm" ] && t+=(-e "$WORLDMM_DIR"); [ -d "$WORLDMM_DIR/src/HippoRAG" ] && t+=(-e "$WORLDMM_DIR/src/HippoRAG"); [ -d "$MERIT_DIR/src/merit" ] && t+=(-e "$MERIT_DIR"); if [ ${#t[@]} -gt 0 ]; then uv pip install --no-deps "${t[@]}" && touch /opt/venv/.integration_ready && echo "[intsetup] editable 연결 완료: ${t[*]}"; else echo "[intsetup] 연결할 소스 없음 — WorldMM/MERIT 를 git clone 후 intsetup 재실행"; fi; }'; \
      echo '# 자동 연결: 세 repo 소스가 모두 감지되고 아직 미연결이면 최초 1회 자동 intsetup. 없으면 조용히 건너뜀.'; \
      echo 'if [ ! -f /opt/venv/.integration_ready ] && [ -d "$WORLDMM_DIR/src/worldmm" ] && [ -d "$WORLDMM_DIR/src/HippoRAG" ] && [ -d "$MERIT_DIR/src/merit" ]; then echo "[integration] 소스 감지 — 최초 1회 자동 연결..."; intsetup; fi'; \
      echo '# 통합 임포트 점검(연결 후): worldmm/merit/deep_reporter 가 clone+intsetup 돼 있어야 성공'; \
      echo "alias intcheck='python -c \"import worldmm, hipporag, merit, deep_reporter, langgraph, langchain_openai, cv2, flask; print(\\\"integration imports OK\\\")\"'"; \
    } >> ~/.bashrc

ENTRYPOINT ["/usr/bin/tini", "--"]
CMD ["/bin/bash"]
