# ════════════════════════════════════════════════════════════════════════════
#  WorldMM + Deep-Reporter + MERIT 통합 이미지 — 빌드/실행 (단일 venv)
#
#  ★자기완결(self-contained) 빌드: 빌드 컨텍스트 = 이 Docker/ 디렉토리 '하나'.
#    의존성 스펙 = envs/{pyproject.toml,uv.lock,.python-version}(= WorldMM lock, 이미 Docker/ 에 포함).
#    → 빌드는 외부 WorldMM 경로에 의존하지 않음. Docker/ 를 통째 복사하면 그대로 빌드 가능.
#
#  빌드:  make docker-base   # /opt/venv 에 서드파티 deps + extras 베이크 (envs/ 의 lock 사용)
#         make docker-user   # 호스트 UID:GID 사용자 오버레이
#  실행:  make docker-run [GPUS='"device=6,7"']  /  docker-exec / docker-stop / docker-rm
#  (선택) make vendor        # envs/ 의 lock 을 WorldMM 에서 재동기화. ★빌드 전 필수 아님★
#                            #   (envs/ lock 은 이미 포함. WorldMM lock 이 바뀌어 재베이크할 때만.)
#
#  진입 즉시 사용(한번에): /opt/venv 자동 활성 + (소스 있으면) worldmm/hipporag/merit editable 자동연결(수 초).
#    소스 없으면 자동연결 건너뜀(에러 없음) → 컨테이너 안 git clone 후 `intsetup`, 점검 `intcheck`.
#    ※ worldmm/hipporag/merit = '라이브 마운트' editable(코드 편집 즉시 반영), deep_reporter = PYTHONPATH.
#
#  토큰/엔드포인트(이미지 미베이크, 호스트 env 로 전달):
#    OPENAI_API_KEY / OPENAI_BASE_URL(로컬 vLLM) / HF_TOKEN
#  주의: sudo 로 실행 금지(USER_NAME 이 root 로 바뀜). 기존 'worldmm' 이미지/컨테이너와 분리(이름/포트).
#  GPU 호환: flash-attn 을 8.0/8.6/8.9/9.0(A100/A6000·3090·A40/4090·L40/H100)로 컴파일(ARG CUDA_ARCH_LIST).
# ════════════════════════════════════════════════════════════════════════════
IMAGE_NAME  = videorag_report
IMAGE_TAG   = cu128-torch28-ubuntu2204

UID        := $(shell id -u)
GID        := $(shell id -g)
USER_NAME  := $(shell whoami)
CONTAINER_NAME = videorag_report

GPUS          ?= all
PORT_JUPYTER  ?= 8809
PORT_TB       ?= 8810
# flash-attn 타깃 아키(호환성 우선). 특정 서버 빌드단축: make docker-base CUDA_ARCH_LIST=9.0
CUDA_ARCH_LIST ?= 8.0;8.6;8.9;9.0

# ── 경로: 하드코딩(/data1/<계정>) 제거, 이 Makefile(Docker/) 위치에서 자동 유도 ──
# DOCKER_DIR = 이 Makefile 의 절대 디렉토리(=…/VideoRAG/report_framework/docker; 2026-11-10 Deep-Report/Docker 에서 복사, 2단계 위가 같은 VideoRAG 라 동작 동일).
DOCKER_DIR := $(patsubst %/,%,$(dir $(abspath $(lastword $(MAKEFILE_LIST)))))
# VideoRAG = 그 2단계 위(= WorldMM/MERIT/Deep-Report 의 부모). 다른 레이아웃이면 오버라이드:
#   make docker-run VideoRAG=/path/to/parent
VideoRAG    ?= $(abspath $(DOCKER_DIR)/../..)
# WORKSPACE = VideoRAG 의 부모(= Docker/ 의 3단계 위, 평소 'workspace'). 이 전체를 same-path 마운트.
WORKSPACE  ?= $(abspath $(DOCKER_DIR)/../../..)
# 컨테이너 repo 경로 = 호스트 경로(same-path). .bashrc 의 WORLDMM_DIR 등 베이스(build-arg 로 user 와 일치).
MOUNT_ROOT ?= $(VideoRAG)
# 데이터 디스크 same-path 마운트: /data1~/data6 중 '호스트에 실제 존재하는 것만' 자동 포함.
#   $(wildcard)로 없는 디스크는 자동 생략 → 서버가 달라도 에러 없음(이식성 유지). 오버라이드 가능.
DATA_MOUNTS ?= $(foreach d,/data1 /data2 /data3 /data4 /data5 /data6,$(if $(wildcard $(d)),-v $(d):$(d),))
# (선택) 그 외 추가 마운트. 기본 없음.
#   예: make docker-run EXTRA_MOUNTS='-v /data:/data -v /mnt/x:/mnt/x'
EXTRA_MOUNTS ?=
# vendor 전용: WorldMM 소스 위치(기본=VideoRAG 하위). 'make vendor' 에서만 참조.
WORLDMM_SRC ?= $(VideoRAG)/WorldMM
# 빌드 컨텍스트 = 이 Docker/ 디렉토리(자기완결).
CONTEXT     = .

# ── 값 정규화(robustness) ──
# 에디터가 값 끝에 넣는 공백/탭을 제거. 안 하면 docker 인자가 쪼개져 깨짐
#  (예: IMAGE_NAME 끝 탭 → 'repository name'/인자과다, PORT 끝 공백 → 'invalid hostPort').
# 주의: 커맨드라인 오버라이드(make X=..)는 우선순위가 높아 이 := 에 영향받지 않음(그 값은 이미 공백 없음).
IMAGE_NAME     := $(strip $(IMAGE_NAME))
IMAGE_TAG      := $(strip $(IMAGE_TAG))
CONTAINER_NAME := $(strip $(CONTAINER_NAME))
PORT_JUPYTER   := $(strip $(PORT_JUPYTER))
PORT_TB        := $(strip $(PORT_TB))
CUDA_ARCH_LIST := $(strip $(CUDA_ARCH_LIST))

.PHONY: vendor docker-base docker-user docker-run docker-exec docker-stop docker-rm dirs

dirs:
	mkdir -p $(VideoRAG)/.cache/huggingface/hub $(VideoRAG)/.claude

# vendor (선택·유지보수): WorldMM 의 의존성 lock 3개를 envs/ 로 '재동기화'.
#   ★빌드 전 필수가 아님★ — envs/ 에 lock 이 이미 있으면 바로 `make docker-base` 가능.
#   언제 실행? WorldMM 의 pyproject/uv.lock 이 바뀌어 /opt/venv 를 다시 베이크해야 할 때만.
#   (pyproject.toml / uv.lock / .python-version 만 복사. README·src·HippoRAG 제외.
#    소스 worldmm/hipporag/merit 는 vendor 대상 아님 → 런타임 마운트 editable.)
vendor:
	@test -f "$(WORLDMM_SRC)/uv.lock" || { echo "ERROR: WorldMM not found at $(WORLDMM_SRC). Use: make vendor WORLDMM_SRC=/path/to/WorldMM"; exit 1; }
	mkdir -p envs
	cp "$(WORLDMM_SRC)/pyproject.toml" "$(WORLDMM_SRC)/uv.lock" "$(WORLDMM_SRC)/.python-version" envs/
	@echo "[vendor] WorldMM 의존성 lock → envs/{pyproject.toml,uv.lock,.python-version} (소스 없음). 크기: $$(du -sh envs | cut -f1)"

# base: envs/ 의 lock + extras 로 /opt/venv 베이크. 컨텍스트 = 이 디렉토리(자기완결).
docker-base:
	@test -f envs/uv.lock || { echo "ERROR: envs/uv.lock 없음(Docker/ 복사 누락?). WorldMM 가 있으면 'make vendor' 로 생성."; exit 1; }
	$(eval FULL := $(IMAGE_NAME):$(IMAGE_TAG))
	DOCKER_BUILDKIT=1 docker build -t $(FULL) \
		--build-arg CUDA_ARCH_LIST="$(CUDA_ARCH_LIST)" \
		-f ./docker/base.Dockerfile $(CONTEXT)

# user: base 위에 호스트 UID:GID 사용자 오버레이
docker-user:
	$(eval FULL := $(IMAGE_NAME):$(IMAGE_TAG))
	DOCKER_BUILDKIT=1 docker build -t $(USER_NAME)/$(FULL) \
		--build-arg IMAGE_NAME=$(FULL) \
		--build-arg UID=$(UID) \
		--build-arg GID=$(GID) \
		--build-arg USER_NAME=$(USER_NAME) \
		--build-arg MOUNT_ROOT=$(MOUNT_ROOT) \
		-f ./docker/user.Dockerfile $(CONTEXT)

docker-run: dirs
	$(eval FULL := $(IMAGE_NAME):$(IMAGE_TAG))
	docker run -it \
		-u $(UID):$(GID) \
		--gpus $(GPUS) \
		--name $(USER_NAME)_$(CONTAINER_NAME) \
		--hostname $(CONTAINER_NAME) \
		-p 127.0.0.1:$(PORT_JUPYTER):$(PORT_JUPYTER) \
		-p 127.0.0.1:$(PORT_TB):$(PORT_TB) \
		-e "TERM=xterm-256color" \
		-e "HF_HOME=$(MOUNT_ROOT)/.cache/huggingface" \
		-e "HUGGINGFACE_HUB_CACHE=$(MOUNT_ROOT)/.cache/huggingface/hub" \
		-e "TOKENIZERS_PARALLELISM=false" \
		-e "TORCH_CUDA_ARCH_LIST=$(CUDA_ARCH_LIST)" \
		-e OPENAI_API_KEY \
		-e OPENAI_BASE_URL \
		-e HF_TOKEN \
		-w $(MOUNT_ROOT) \
		-v $(WORKSPACE):$(WORKSPACE) \
		-v $(VideoRAG)/.claude:/home/$(USER_NAME)/.claude \
		$(DATA_MOUNTS) \
		$(EXTRA_MOUNTS) \
		--shm-size=128G \
		--ipc=host \
		--ulimit memlock=-1 \
		--ulimit stack=67108864 \
		--ulimit nofile=1048576:1048576 \
		$(USER_NAME)/$(FULL) /bin/bash

docker-exec:
	docker exec -it $(USER_NAME)_$(CONTAINER_NAME) /bin/bash

docker-stop:
	docker stop $(USER_NAME)_$(CONTAINER_NAME)

docker-rm:
	docker rm -f $(USER_NAME)_$(CONTAINER_NAME)
