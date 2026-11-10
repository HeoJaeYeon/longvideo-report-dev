# ════════════════════════════════════════════════════════════
#  make docker-base                       # uv 캐시 프리워밍(flash-attn 컴파일 1회)
#  make docker-user                       # 호스트 UID:GID 사용자 오버레이
#  make docker-run                        # 8장 전체
#  make docker-run GPUS='"device=0,1"'    # 일부만
#  make docker-exec
#  ── 최초 1회(컨테이너 안): cd $WORLDMM_DIR && uv sync   (repo/.venv 생성, 캐시 웜)
#     이후 공식 script 그대로: bash script/2_preprocess.sh ...
#  ── OpenAI/HF 토큰은 호스트 env 로 전달(이미지 미베이크):
#       export OPENAI_API_KEY=... ; export HF_TOKEN=... ; make docker-run
#  주의: 이 Makefile 은 sudo 로 실행하지 않는다 (USER_NAME 이 root 로 바뀜)
#  주의: 빌드 컨텍스트 = WorldMM 루트('..'). base.Dockerfile 이 pyproject/uv.lock/src 를 COPY.
#        → WorldMM/.dockerignore 가 data/ 등 대용량을 컨텍스트에서 제외(필수).
# ════════════════════════════════════════════════════════════
IMAGE_NAME  = worldmm
IMAGE_TAG   = cu128-torch28-tf4576-ubuntu2204

UID        := $(shell id -u)
GID        := $(shell id -g)
USER_NAME  := $(shell whoami)
CONTAINER_NAME = worldmm

GPUS          ?= all
PORT_JUPYTER  ?= 8807
PORT_TB       ?= 8808

WORKSPACE = /data1/$(USER_NAME)/workspace
WORLDMM   = $(WORKSPACE)/VideoRAG/WorldMM
CACHEROOT = $(WORKSPACE)/.cache
CONTEXT   = ..

.PHONY: docker-base docker-user docker-run docker-exec docker-stop docker-rm dirs

dirs:
	mkdir -p $(CACHEROOT)/huggingface/hub /data1/$(USER_NAME)/.claude

docker-base:
	$(eval FULL := $(IMAGE_NAME):$(IMAGE_TAG))
	DOCKER_BUILDKIT=1 docker build -t $(FULL) \
		-f ./docker/base.Dockerfile $(CONTEXT)

docker-user:
	$(eval FULL := $(IMAGE_NAME):$(IMAGE_TAG))
	DOCKER_BUILDKIT=1 docker build -t $(USER_NAME)/$(FULL) \
		--build-arg IMAGE_NAME=$(FULL) \
		--build-arg UID=$(UID) \
		--build-arg GID=$(GID) \
		--build-arg USER_NAME=$(USER_NAME) \
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
		-e "HF_HOME=$(CACHEROOT)/huggingface" \
		-e "HUGGINGFACE_HUB_CACHE=$(CACHEROOT)/huggingface/hub" \
		-e "TOKENIZERS_PARALLELISM=false" \
		-e "TORCH_CUDA_ARCH_LIST=8.6" \
		-e "NCCL_IB_DISABLE=1" \
		-e OPENAI_API_KEY \
		-e HF_TOKEN \
		-w $(WORLDMM) \
		-v $(WORKSPACE):$(WORKSPACE) \
		-v /data:/data -v /data1:/data1 -v /data2:/data2 -v /data3:/data3 \
		-v /data4:/data4 -v /data5:/data5 -v /data6:/data6 \
		-v /data1/$(USER_NAME)/.claude:/home/$(USER_NAME)/.claude \
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
