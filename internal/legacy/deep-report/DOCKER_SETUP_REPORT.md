# WorldMM + Deep-Reporter + MERIT 통합 Docker — 설계·구축 보고서 (v6, 최종 — 유연 경로)

> 갱신 2026-10-21. 위치: **`Deep-Report/Docker/`**. 이미지 `videorag_report:cu128-torch28-ubuntu2204`.
> 핵심 원칙: **(A) 서드파티 라이브러리는 이미지(`/opt/venv`)에 베이크 / (B) 프로젝트 소스(worldmm·hipporag·merit·deep_reporter)는 런타임 마운트에서 연결.** 이미지 빌드는 (A)만 필요 → **프로젝트 소스 없이도 환경 구축 가능**.
> ⚠️ 파일 작성 + 정적 검증(`make -n`, TAB, `.bashrc` `bash -n`+4시나리오, uv dry-run)까지 완료. **실제 `docker build` 는 미실행**(사용자 수행). §8 디스클로저 필독.

---

## 0. 핵심 개념 — (A) 라이브러리 vs (B) 프로젝트 소스
| | (A) 서드파티 라이브러리 | (B) 프로젝트 소스 |
|---|---|---|
| 예 | torch2.8+cu128, transformers4.57.6, flash-attn2.8.3, langchain/langgraph, opencv, hipporag의 deps … | worldmm, hipporag, merit, deep_reporter |
| 성격 | PyPI 설치형(버전 핀) | PyPI에 없는 **자기 코드**(소스) |
| 어디 | **이미지 `/opt/venv`에 베이크**(빌드) | **마운트된 repo**(이미지에 안 넣음) |
| 언제 | `make docker-base`(빌드) | 런타임 진입 시 editable 연결(`intsetup`) |
→ **이미지 빌드 = (A)만.** (B) 소스가 없어도 이미지·컨테이너는 정상 구축·진입됨.

## 1. 디렉토리 구조 (`Deep-Report/Docker/`)
```
Docker/
├── Makefile
├── check_port_used.py
├── .dockerignore
├── docker/base.Dockerfile       # (A) /opt/venv 베이크
├── docker/user.Dockerfile       # 사용자 + 자동환경 + (B) tolerant 연결
└── envs/                        # 빌드가 쓰는 의존성 스펙(이미 포함, 소스 아님)
    ├── extras-integration.txt   # (A) langchain/langgraph/flask/opencv
    ├── pyproject.toml           # ┐ WorldMM 의존성 lock(= 빌드 재현용 config)
    ├── uv.lock                  # │  (574K; 대부분 이 파일)
    └── .python-version          # ┘
```
- `worldmm/` 디렉토리·WorldMM 소스·README **없음**. 빌드 입력 = envs/ 의 lock 3개 + extras.

## 2. ★make 타깃과 환경·맥락 (지금 설정 그대로)
| 변수 | 값 | 비고 |
|---|---|---|
| IMAGE | `videorag_report:cu128-torch28-ubuntu2204` | base=이 이름, user=`$(USER)/videorag_report:…` |
| CONTAINER / hostname | `$(USER)_videorag_report` / `videorag_report` | 기존 worldmm 과 분리(동시가동) |
| PORT | 8809 / 8810 (기본) | `make docker-run PORT_JUPYTER=.. PORT_TB=..` 로 변경 |
| CUDA_ARCH_LIST | `8.0;8.6;8.9;9.0` | A100/A6000·3090·A40/4090·L40/H100 |
| VAU_RAG (호스트) | **자동 유도** = `Docker/`의 2단계 위(= WorldMM/MERIT/Deep-Report 부모). `make … VAU_RAG=/경로`로 오버라이드 | /data1/<계정> 하드코딩 제거 |
| MOUNT_ROOT (컨테이너) | `/workspace/VAU_RAG` (고정) | 호스트 경로와 무관. `$(VAU_RAG)` 를 여기로 마운트 |
| EXTRA_MOUNTS | (기본 없음) | 호스트 데이터 디스크 추가: `EXTRA_MOUNTS='-v /data1:/data1'` |
| CONTEXT | `.` (= Docker/) | 자기완결 빌드(외부경로 비의존) |

타깃:
- **`make docker-base`** (필수) — `envs/` lock 으로 `/opt/venv` 베이크. 가드: `envs/uv.lock` 존재 확인.
- **`make docker-user`** (필수) — 호스트 UID:GID 사용자 오버레이.
- **`make docker-run`** — 컨테이너 기동(마운트·GPU·포트). `docker-exec/stop/rm`.
- **`make vendor`** — **선택(유지보수)**. envs/ 의 lock 을 WorldMM 에서 재동기화. **빌드 전 필수 아님**(envs/ 에 이미 포함). WorldMM lock 이 바뀌어 재베이크할 때만.
- 값 정규화: 모든 변수에 `$(strip)` 적용 → 에디터가 넣는 끝 공백/탭으로 docker 인자가 깨지는 사고 방지.

## 3. 빌드가 하는 일 (`docker/base.Dockerfile`) — (A)만
1. 시스템 패키지(빌드도구 + ffmpeg/opencv 런타임 libs) + Node20 + Claude Code(@latest) + uv 바이너리.
2. `COPY envs/{pyproject.toml,uv.lock,.python-version}` → **`uv sync --frozen --no-install-project --no-install-package hipporag`** 로 `/opt/venv` 에 **서드파티 deps 전체 설치**(torch/flash-attn/transformers/hipporag deps…). worldmm·hipporag '패키지 자체'는 skip.
3. `COPY envs/extras-integration.txt` → `uv pip install --python /opt/venv/bin/python -r` (langchain/langgraph/flask/opencv; openai 2.29→2.54).
4. 빌드 검증(GPU 없이 import만), `/opt/wmbuild`·임시파일 제거, `chmod -R a+rwX /opt/venv /opt/uv-cache /opt/uv-python`(런타임 editable 쓰기 허용).
- flash-attn 은 `CUDA_ARCH_LIST` 로 멀티아키 컴파일(§6).

## 4. 런타임이 하는 일 (`docker/user.Dockerfile` → `.bashrc`) — (B) tolerant 연결
컨테이너 진입(대화형 셸)마다 자동:
- `source /opt/venv/bin/activate` (베이크된 통합 venv 활성), 프롬프트 `(videorag_report)`.
- 환경변수(UV·TORCH_CUDA_ARCH_LIST·NCCL …) + `PYTHONPATH=$DEEPREPORTER_DIR`(deep_reporter 용).
- **`intsetup` 함수** + **tolerant 자동 연결 가드**:
  - 가드: `세 소스(worldmm/HippoRAG/merit) 모두 존재 && 미연결`일 때만 1회 자동 `intsetup`. 없으면 **조용히 건너뜀(에러 없음)**.
  - `intsetup`: 존재하는 repo만 골라 `uv pip install --no-deps -e …` (editable, deps 는 /opt/venv 에 있음). sentinel `/opt/venv/.integration_ready` 로 1회만. **부분 clone 안전**.
  - `intcheck`: `import worldmm, hipporag, merit, deep_reporter, langgraph, langchain_openai, cv2, flask` 점검.

`intsetup`(= 그 함수)은 "PyPI에 없는 자기 코드(worldmm/hipporag/merit)를 마운트 소스에 editable 연결"하는 작업입니다. deep_reporter 는 설치형이 아니라 PYTHONPATH 로 처리(intsetup 대상 아님).

## 5. `~/.bashrc` / `/opt` / `/opt/venv` (개념)
- **`~/.bashrc`** = `/home/$(USER)/.bashrc`. 대화형 bash 셸을 열 때마다 자동 실행되는 환경 셋업 스크립트(색상 프롬프트 + 위 §4). 이미지에 구워짐(마운트 아님).
- **`/opt`** = FHS의 add-on 소프트웨어 영역. **마운트에 가려지지 않는 이미지 고유 경로**라 베이크 산출물을 둠(`/opt/venv`, `/opt/uv-cache`, `/opt/uv-python`).
- **`/opt/venv`** = 베이크된 파이썬 가상환경(자기만의 bin/python + site-packages). 활성 시 이 환경의 라이브러리를 사용. (A) 전부 설치됨 + 런타임에 (B) editable 연결.

## 6. GPU 멀티아키 호환 & 색상 CLI
- flash-attn(유일한 아키 민감 소스빌드)을 `8.0;8.6;8.9;9.0` 로 컴파일. base `ARG`/Makefile `--build-arg`/런타임 `-e` 3곳 일관. **최초 빌드 시간만** 증가(런타임 성능 동일). 단축: `make docker-base CUDA_ARCH_LIST=9.0`.
- 색상: base image `/etc/skel/.bashrc`(색상블록) + `useradd -m` + `-e TERM=xterm-256color` → worldmm 과 동일 컬러 프롬프트/ls/grep (실측 확인).

## 7. ★사용 순서 (vendor=선택, 경로=자동유도)
```bash
# Docker/ 가 어디에 있든(VAU_RAG/Deep-Report/Docker 구조면) 경로 자동 유도
cd <...>/VAU_RAG/Deep-Report/Docker

# [빌드]  vendor 불필요 — envs/ 에 lock 이 이미 포함돼 있음
make docker-base       # /opt/venv 베이크(1회, flash-attn 멀티아키 → 수십 분)
make docker-user
make docker-run PORT_JUPYTER=8809 PORT_TB=8810   # 포트 점유 시 check_port_used.py 로 확인

# [컨테이너 안] 작업디렉토리는 /workspace/VAU_RAG (= 호스트 VAU_RAG 마운트, 고정 경로)
#  (B) 소스가 없으면 여기서 git clone → 자동으로 editable 연결됨
cd /workspace/VAU_RAG
git clone <WorldMM-url>     WorldMM
git clone <MERIT-url>       MERIT
git clone <Deep-Report-url> Deep-Report     # (Docker/ 가 들어있는 그 repo. 이미 있으면 생략 가능)
intsetup               # worldmm/hipporag/merit editable 연결(존재하는 것만)
intcheck               # → integration imports OK

# [선택/유지보수] WorldMM 의존성이 바뀐 경우에만:
make vendor && make docker-base    # envs/ lock 재동기화 후 /opt/venv 재베이크

# [오버라이드] repo 부모 레이아웃이 다르거나 데이터 디스크가 필요하면:
make docker-run VAU_RAG=/절대/부모경로 EXTRA_MOUNTS='-v /data1:/data1'

# (로컬 vLLM 작성 LLM 사용 시) make docker-run 전에:
#   export OPENAI_BASE_URL=http://<host>:<port>/v1 ; export OPENAI_API_KEY=dummy
```
> ※ `/workspace/VAU_RAG` 는 호스트의 VAU_RAG(= Docker/ 의 2단계 위)를 마운트한 **컨테이너 고정 경로**입니다. 즉 Deep-Report 는 보통 이미 거기 있고(= Docker/ 의 부모), WorldMM/MERIT 를 그 옆에 clone 하면 됩니다.

## 8. ★다른 GPU 서버로 이식 — 경로는 자동 유도(하드코딩 없음)
- **빌드가 요구하는 것**: `Docker/` 디렉토리 하나(그 안 `envs/` 포함)뿐. 외부 WorldMM 경로 **비의존**. → `Docker/` 를 **`envs/` 포함해** 복사하면 `make docker-base` 가능(vendor 불필요).
- **경로 자동 유도(= /data1/<계정> 하드코딩 제거)**:
  - 호스트 `VAU_RAG` = **이 Makefile(Docker/)의 2단계 위**로 자동 계산(WorldMM/MERIT/Deep-Report 의 부모). 즉 `Docker/` 를 `VAU_RAG/Deep-Report/Docker` 위치에만 두면 서버·계정·디스크가 달라도 그대로 동작.
  - 컨테이너 안은 항상 **`/workspace/VAU_RAG`**(= `MOUNT_ROOT`, 고정)로 보임. `.bashrc` 의 `WORLDMM_DIR/MERIT_DIR/DEEPREPORTER_DIR` 는 이 고정 경로 기반(build-arg).
  - clone 위치: 컨테이너 안 `/workspace/VAU_RAG/{WorldMM,MERIT,Deep-Report}` = 호스트 `$(VAU_RAG)/{...}`.
- **오버라이드(레이아웃이 다를 때만)**:
  - repo 부모가 다른 곳: `make docker-run VAU_RAG=/절대/부모경로` (docker-base/user 에도 동일 지정 가능).
  - 호스트 데이터 디스크 필요: `EXTRA_MOUNTS='-v /data1:/data1 -v /mnt/x:/mnt/x'`.
  - 컨테이너 마운트 지점 변경(드묾): `MOUNT_ROOT=/..` — 단 `.bashrc` 에 build-arg 로 구워지므로 `make docker-user` 도 같은 값으로 재빌드.
- HF 캐시(`$(VAU_RAG)/.cache/huggingface`)·`.claude`(`$(VAU_RAG)/.claude`)도 VAU_RAG 하위로 자동 유도(하드코딩 없음).

## 9. ★디스클로저 — 숨김 없이
1. **실제 `docker build` 미실행**(정적/문법/dry-run 검증까지). flash-attn 멀티아키라 첫 빌드 수십 분.
2. **이미지 빌드 = (A)-only**: 프로젝트 소스 없이도 구축·진입 정상(4시나리오 검증: 소스 0/일부/전부/수동 intsetup).
3. **(B)는 런타임 마운트 editable**: `import worldmm/merit/deep_reporter/hipporag` 는 **clone + intsetup 후에만** 성공(그 전엔 ModuleNotFoundError = 정상).
4. **첫 `intsetup` 시 setuptools 빌드백엔드 1회 fetch 가능**(hipporag/merit 가 setuptools 빌드). 네트워크 有 환경이면 수 초. `import hipporag` 실패 시 `uv pip install -e $WORLDMM_DIR/src/HippoRAG`(--no-deps 없이) fallback.
5. **openai 2.29→2.54** 가 /opt/venv 전체(WorldMM 포함)에 적용. 둘 다 openai 2.x API → 저위험.
6. **MERIT** 는 자기 테스트 조합(torch2.6/tf4.57.3/openai2.8.1)이 아닌 WorldMM 스택 위 구동(미검증, 가능성 높음) → `intcheck` + 소규모 eval 스모크 권장.
7. **lock 정합**: envs/ 의 lock 은 *기준 WorldMM* 것. clone 한 WorldMM 의 lock 이 다르면 `make vendor && make docker-base` 로 재베이크.
8. **vLLM(로컬 qwen3 writer)은 이미지 미포함**: torch 핀 충돌 우려 → 별도 컨테이너로 서빙.
9. **런타임은 자기완결 아님**: `docker-run` 은 마운트(호스트 `$(VAU_RAG)` → 컨테이너 `/workspace/VAU_RAG`) 의존. **빌드만** 자기완결(Docker/ 하나).
10. **작업디렉토리** `-w /workspace/VAU_RAG` 는 마운트 지점이라 **항상 존재**(옛 `-w .../WorldMM` 처럼 빈 디렉토리가 생기는 문제 없음). 데이터 디스크(/data1 등)는 기본 미마운트 → 필요 시 `EXTRA_MOUNTS` 로만 추가(없어도 빌드·진입 정상).
11. **경로 자동유도 전제**: `Docker/` 가 `VAU_RAG/Deep-Report/Docker` 구조여야 `VAU_RAG` 자동계산이 맞음. 아니면 `VAU_RAG=` 로 지정.

## 10. 파일별 요약
| 파일 | 역할 |
|---|---|
| `Makefile` | `docker-base/user/run`(필수) · `vendor`(선택·재동기화) · `$(strip)` 정규화 · `CONTEXT=.`(자기완결) · `CUDA_ARCH_LIST` |
| `docker/base.Dockerfile` | (A) `/opt/venv` 베이크(`uv sync --no-install-project --no-install-package hipporag` + extras) |
| `docker/user.Dockerfile` | 사용자 + `/opt/venv` 자동활성 + PYTHONPATH + **tolerant `intsetup`/자동가드** + `(videorag_report)` 라벨 + `intcheck` |
| `envs/extras-integration.txt` | langchain/langgraph/flask/opencv (단일 출처) |
| `envs/{pyproject.toml,uv.lock,.python-version}` | WorldMM 의존성 lock(빌드 재현용, 이미 포함) |
| `check_port_used.py` | 포트 점검(원본 복사) |

## 11. 안전성/유지보수 요약
- **안전**: 기존 worldmm 이미지/컨테이너/포트와 분리. 소스 미설정이어도 이미지 구축·진입 정상. (B) tolerant 연결로 clone 전/부분/후 모두 안전. docker-base 가드가 envs/uv.lock 확인(복사 누락 조기 감지).
- **유지보수**: (A) 단일 출처(envs/), `vendor` 는 선택적 재동기화 한 명령, `$(strip)` 공백 사고 방지, 자기완결 빌드(외부 경로 비의존), 경로 요구사항 문서화(§8).
