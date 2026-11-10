# 서버 이전 인수인계 메모 (2026-10-23)

> 새 서버에서 작업을 이어갈 때 **이 문서를 가장 먼저 읽는다.** 그다음 `DESIGN_AND_STATUS.md` §2·§13, `REPORT_ISSUES_AND_FIXES.md` 순서로 읽는다.
> 이 문서는 `DESIGN_AND_STATUS.md`(2026-10-22 오후 기준)에 아직 반영되지 않은 내용만 담는다. 표기: ✔ = 직접 확인, (사용자) = 사용자가 알려준 사실, (계획) = 아직 하지 않은 일.
>
> **2026-11-10 경로 정리** (동작 변경 없음, `internal/status/REORG_LOG_20261110.md`): 사전 인덱싱 캐시 `cache/episodic/` → `WorldMM/output/memory/videomme_long_qwen3vl-8b/report_framework_index/`, WorldMM 메모리 `WorldMM/claude_output/full/` → 같은 폴더(`caption/`, `metadata/`, …). 메모리·캐시의 옛 경로 표기는 작성 당시 기준이다. 메모리 구축 스크립트는 `scripts/memory_build/`, Docker 정의 사본은 `report_framework/docker/`. 같은 날 폴더 재배치(P2): 스크립트·결과 경로(`tests/*` → `tests/unit/`·`tests/gpu/`·`experiments/`·`scripts/launch/`, `analysis/*.json` → `results/`, `inspect/`·`running_example/` → `internal/`)는 본문에서도 새 위치로 고쳐 적었다. 문서 위치는 `docs/README.md` 색인.
>
> **2026-10-25 갱신**
> - §2의 내용(대기 실행 기록, HF 캐시 정정)은 `DESIGN_AND_STATUS.md` §3·§9.9·§10·§11과 `REPORT_ISSUES_AND_FIXES.md` I4·I22·I27에 반영했다.
> - **사용자가 이전 서버의 GPU 4–7 사용을 허용해(2026-10-25) 작업을 이전 서버에서 계속한다.** 2026-10-23 복사 이후 이전 서버에서 바뀌거나 생긴 파일(문서 6종, 캐시, `outputs/`, 로그 등)은 실제로 옮길 때 같은 rsync 명령으로 다시 동기화해야 한다(§1.1).
> - 모델 위치는 `HF_HOME`이 아니라 컨테이너의 **`HUGGINGFACE_HUB_CACHE`**로 정해진다(§2.2, §4.3). 시각은 컨테이너 시계(UTC) 기준이다.
> - **2026-10-25 C 단계 이후(이전 서버)**: 검증 영상 3개의 4개 단위 캐시 완성(C-1), 검색 확인(C-3), 보고서 11건(C-4·C-5) 생성. `report_framework/`가 76M(10/23 복사 시점)에서 365M가 됐다(`cache/` 108M, `backups/` 138M — 캐시 사본 2벌 포함, `outputs/` 67M, `tests/_artifacts/` 50M, `.git/` 1.5M, 2026-10-25 `du -sh`). 루트 `CLAUDE.md`도 갱신됐다. 새 서버로 옮길 때 같은 rsync 명령으로 다시 동기화한다(규칙에 `report_framework/**`와 `/CLAUDE.md` 포함).
> - 새 서버에서도 지킬 실행 규칙: 같은 영상을 검색 서비스 2개 이상이 동시에 불러오지 않는다(I29), 같은 작업 폴더에서 Claude 세션을 하나만 쓴다(I30). 결과는 `DESIGN_AND_STATUS.md` §9.10–§9.15.

---

## 1. 이전 개요

| 항목 | 이전 서버 | 새 서버 |
|---|---|---|
| 프로젝트 경로 | `/data1/jyheo/workspace/VideoRAG` | **`/home/jyheo/workspace/VideoRAG`** (사용자) |
| 호스트 | 컨테이너 `videorag_report` (이미지 `videorag_report:cu128-torch28-ubuntu2204`) | `super`, 211.180.114.160, SSH 포트 20202 (사용자). 호스트 키 ED25519 `SHA256:GGKbrk8GzdNKcvP0868fR0ZhnreaKJpNX10lxFXFqU0` |
| Video-MME 영상 | `/data6/dataset/Video-MME/videomme/data` (링크) | **`/DATA3/datasets/Video-MME/videomme/data`** (사용자, `-QuCz7kxBr8.mp4` 존재 확인) |
| HF 모델 | `/data1/jyheo/workspace/.cache/huggingface/hub` 와 `VideoRAG/.cache/huggingface/hub` (같은 내용 두 벌, ✔) | **복사하지 않음.** `/DATA3/models`에 새로 내려받는다 (사용자, §4.3) |
| GPU | A6000 × 8, 다른 사용자와 공유 | A6000 (사용자). 사용할 GPU와 공유 여부는 **새 서버에서 사용자에게 확인** |
| 디스크 여유 | — | `/` 404GB, `/DATA3` 689GB, `/DATA1` 569GB, `/DATA2` 846GB (사용자 `df`, 2026-10-23) |

### 1.1 복사한 것과 복사하지 않은 것 (✔)

- 방법: 이전 서버 컨테이너에서 `rsync -aH --partial -e "ssh -p 20202" --filter="merge migration/videorag_transfer_nomodels.filter"`. `--delete` 없이.
- 결과: 2,944개(일반 1,861, 폴더 1,015, 링크 68), 757,881,549 bytes 전송. 체크섬 비교(`rsync -aHcn --itemize-changes`) **차이 0건**.
- 새 서버 확인: `report_framework` 76M, `WorldMM` 532M, `MERIT` 101M, `Deep-Report` 1.5M(원본에서 `__pycache__` 248K 제외한 크기와 같음), 캡션 50, visual 메모리 50, WorldMM 로컬 수정 4개 유지.

| 복사함 | 복사하지 않음 (이유) |
|---|---|
| `report_framework/` (`__pycache__` 제외) | `WorldMM/.venv/` (9월에 만든 옛 venv, `/opt/uv-python`에 묶임. 실행 환경은 이미지의 `/opt/venv`) |
| `WorldMM/` (로컬 수정: `src/worldmm/llm/qwen3vl.py`, `src/worldmm/memory/episodic/multiscale.py`, `script/4_eval.sh`, `script/videomme/4_eval.sh`. **git clone으로 대체 불가**) | `WorldMM/data/Video-MME/{data,subtitle}`, `videomme/test-00000-of-00001.parquet` (이전 서버 `/data6`를 가리키는 링크. 새 서버에서 다시 만든다) |
| `MERIT/`, `Deep-Report/` (Docker 빌드 폴더 `Deep-Report/Docker/` 포함) | `.cache/` 전체 (HF 모델은 새로 내려받기로 함) |
| `claude_output/` (VideoRAG 바로 아래, 이전 설계 문서), `CLAUDE.md` | `.claude/.credentials.json` 및 세션 임시 상태(`sessions`, `plugins`, `skills`, `cache` 등) |
| `.claude/projects/`, `.claude/history.jsonl`, `.claude/settings*.json` | `HolmesVAU/`(8.5G), `AdaVideoRAG/`, `Vgent/` (현재 코드가 참조하지 않음, 전수 검색 ✔) |

- 함께 넘어간 끊긴 링크 68개(`WorldMM/claude_output/pilot` 18개, `claude_output/full/work/*/cap` 50개)는 옛 경로 `/data1/jyheo/workspace/VAU_RAG/...`를 가리키며 **이전 서버에서도 이미 끊겨 있었다.** 과거 전처리용이고 현재 실행과 무관하다.

### 1.2 `report_framework/migration/` (2026-10-23 생성)

| 파일 | 내용 |
|---|---|
| `videorag_transfer_nomodels.filter` | 실제 사용한 rsync 규칙 |
| `videorag_transfer.filter` | 모델 4개(약 30GB)까지 포함하는 규칙. **사용하지 않음** |
| `videos50.md5` | 이전 서버의 50개 영상 md5 (15.59GB). 새 서버 데이터셋과 같은 파일인지 확인용 |
| `opt_venv_freeze.txt` | 이전 서버 `/opt/venv`의 `pip freeze --exclude-editable` (183줄). 새 이미지와 비교용 |

---

## 2. `DESIGN_AND_STATUS.md`에 아직 없는 내용

### 2.1 대기 후 자동 시작 실행 (2026-10-22 16:05 – 2026-10-23 00:06) — 시작하지 못함 (✔)

- 사용자 지시: "2시간 있다가 영상 3개 검증 수행, report 작성까지. GPU 6,7 사용, 다른 user 작업 중단 금지."
- 새 파일 `experiments/delayed_gpu_3videos.py`: `--delay-sec`(기본 7200) 대기 → GPU 6·7을 30초마다 측정해 최근 `--hold-sec`(600초)의 최대 사용량을 구함 → `max_used[llm] + 19,000 + margin ≤ 47,500` 그리고 `max_used[aux] + 15,000 + margin ≤ 47,500`(margin 1,500 MiB)을 만족하는 배치가 있을 때만 `experiments/gpu_3videos.py`를 1회 실행. `--max-wait-sec`(6시간) 안에 조건을 못 맞추면 시작하지 않는다. 자동 재시도 없음. `GPUS = (6, 7)`이 코드에 고정돼 있다.
- 결과(`outputs/3videos_20261022_160548_gated/gate_run.log`, `gate.json`): 18:15부터 00:05까지 698번 판단, **한 번도 통과하지 못함.** 가장 큰 여유는 18:35–18:36의 **−961 MiB**. 우리 프로세스는 하나도 띄우지 않았고 캐시 변경도 없다.
- 다른 사용자 사용량(각 판단 시점의 최근 10분 최대값):

| 시간대 | GPU 6 | GPU 7 | 최대 여유 |
|---|---|---|---|
| 18시 | 30.4–35.1 GB | 29.0–34.2 GB | −961 MiB |
| 19시 | 32.2–36.1 GB | 28.5–35.6 GB | −2,221 MiB |
| 20시 | 35.3–37.4 GB | 33.0–37.0 GB | −4,453 MiB |
| 21시 | 32.3–37.5 GB | 33.7–37.2 GB | −3,777 MiB |
| 22시 | 31.8–37.6 GB | 34.4–38.1 GB | −5,009 MiB |
| 23시 | 32.6–38.2 GB | 37.3–39.2 GB | −5,715 MiB |
| 00시 | 36.3–37.4 GB | 38.7–39.0 GB | −7,825 MiB |

- 해석: 다른 사용자가 37–39GB를 쓰면 남는 메모리는 10–12GB뿐이라 모델 서버(약 19GB)도, 인덱서·검색 서비스(약 15GB)도 들어갈 수 없다. 조건을 느슨하게 했다면 감시 장치가 바로 중단시켰거나, 최악의 경우 다른 사용자 프로세스가 메모리 부족으로 죽을 수 있었다. 이 결과가 서버 이전의 직접적인 배경이다.

### 2.2 `DESIGN_AND_STATUS.md` §3의 정정할 내용 (✔ 2026-10-23, 2026-10-25 원인 확인 후 문서 반영 완료)

- §3에 "환경변수 `HF_HOME=/data1/jyheo/workspace/VideoRAG/.cache/huggingface`에는 **모델이 없다**"고 적혀 있으나 사실이 아니다. 그 위치에도 2026-10-21 16:26–16:31에 모델 4개가 들어와 있었고, `/data1/jyheo/workspace/.cache/huggingface/hub`와 snapshot 해시·바이트 수가 같았다. 새 서버에서는 두 경로를 하나로 정리하므로(§4.3) 문서를 고칠 때 새 구조로 바꿔 쓴다.
- **원인 (2026-10-25 확인)**: 컨테이너에는 `HF_HOME` 외에 `HUGGINGFACE_HUB_CACHE=<VideoRAG>/.cache/huggingface/hub`가 설정돼 있고(Makefile `docker-run`), `huggingface_hub`는 이것을 `HF_HOME`보다 먼저 쓴다. 그래서 우리 스크립트가 `HF_HOME`을 `paths.hf_home`으로 바꿔도 모델 위치는 그대로였고, 2026-10-21 16:24–16:31 GPU 스모크와 LLM 서버가 그 위치에 모델을 내려받았다. 이후 모든 실제 모델 실행은 `VideoRAG/.cache/huggingface/hub`의 모델을 썼다(`REPORT_ISSUES_AND_FIXES.md` I4).
- §13.5 등 문서 곳곳의 `/data1/jyheo/workspace/...` 경로 표기는 이전 서버 기준이다.

### 2.3 이전 직전 상태 (변화 없음, ✔)

- episodic 캐시: `-QuCz7kxBr8`은 10sec·30sec·3min만 있음, `0RxMZBLeqRI` 없음, `54k2g9ddy4M` 없음, `_done/` 비어 있음.
- 영상 3개 dry-run: OpenIE 호출 12 / 178 / 240, 합계 **430회**.
- CPU 테스트 5종: 30 / 50 / 67 / 9 / 18개 모두 통과(2026-10-22 기준).
- GPU 검증(분할 OpenIE 효과, 4개 단위 캐시로 검색, 현재 코드로 보고서)은 모두 **미실행**.

---

## 3. 새 서버 환경 메모

- Docker: `Deep-Report/Docker/Makefile`은 자기 위치에서 경로를 유도한다 → 새 서버에서 `VideoRAG=/home/jyheo/workspace/VideoRAG`, `WORKSPACE=/home/jyheo/workspace`, 컨테이너 안 경로도 같다(same-path 마운트). `VideoRAG/.claude`가 컨테이너의 `~/.claude`로 마운트된다.
- **데이터 디스크 자동 마운트 대상은 소문자 `/data1`–`/data6`뿐**이다. 새 서버의 `/DATA1`·`/DATA2`·`/DATA3`는 대상이 아니므로 `make docker-run EXTRA_MOUNTS='-v /DATA3:/DATA3'`가 반드시 필요하다(영상과 모델이 모두 `/DATA3`).
- 컨테이너 환경변수 `HF_HOME=/home/jyheo/workspace/VideoRAG/.cache/huggingface`, **`HUGGINGFACE_HUB_CACHE=/home/jyheo/workspace/VideoRAG/.cache/huggingface/hub`** (Makefile 고정). 모델 위치를 정하는 것은 `HUGGINGFACE_HUB_CACHE`다(§2.2). `config.yaml`의 `paths.hf_home`은 컨테이너 안에서는 모델 위치에 영향이 없다.
- 빌드 정보: `docker-base`는 `nvidia/cuda:12.8.1-cudnn-devel-ubuntu22.04` 기반, uv 0.9.5, `envs/uv.lock`(= WorldMM `uv.lock`과 동일 ✔) + `envs/extras-integration.txt`(langgraph 1.2.16, langchain-core 1.6.12, langchain-openai 1.4.3, flask 3.1.3). extras의 하위 의존성은 버전이 고정돼 있지 않아 이전 서버와 다를 수 있다 → `migration/opt_venv_freeze.txt`와 비교.
- 이전 서버 드라이버 580.126.09 / CUDA 12.8. 새 서버 드라이버도 CUDA 12.8 이상을 지원해야 한다.
- 대화 기록 폴더는 실행 경로로 이름이 정해진다: 새 서버에서는 `.claude/projects/-home-jyheo-workspace-VideoRAG`.

---

## 4. 새 서버에서 할 일 (순서대로)

### 4.1 호스트 준비 (계획)

1. 이전 서버에서 마지막 동기화(이 세션 종료 후, 같은 rsync 명령) → 체크섬 비교 출력 0건 확인.
2. `ln -sfn /DATA3/datasets/Video-MME/videomme/data WorldMM/data/Video-MME/data` → `migration/videos50.md5`로 50개 비교(`md5sum -c`).
3. **마지막 동기화 뒤에** `mv .claude/projects/-data1-jyheo-workspace-VideoRAG .claude/projects/-home-jyheo-workspace-VideoRAG` (먼저 바꾸면 동기화가 옛 이름 폴더를 다시 만든다).
4. `mkdir -p /DATA3/models/huggingface/hub` → `ln -sfn /DATA3/models/huggingface VideoRAG/.cache/huggingface`.
5. `docker ps`(권한), `nvidia-smi`(드라이버·다른 사용자 사용량), `docker info | grep -i runtime`(nvidia 런타임) 확인.

### 4.2 Docker (계획)

```bash
cd /home/jyheo/workspace/VideoRAG/Deep-Report/Docker
make docker-base CUDA_ARCH_LIST=8.6
make docker-user
make docker-run GPUS='"device=<사용자가 허용한 GPU>"' EXTRA_MOUNTS='-v /DATA3:/DATA3'   # 포트 충돌 시 PORT_JUPYTER/PORT_TB
# 컨테이너 안
intcheck; pip list --editable          # worldmm·hipporag·merit → /home/jyheo/workspace/VideoRAG/...
pip freeze --exclude-editable | diff /home/jyheo/workspace/VideoRAG/report_framework/migration/opt_venv_freeze.txt -
```

### 4.3 모델 (계획) — HF 캐시 구조로, 이전 서버와 같은 revision

코드는 모델을 저장소 이름(`Qwen/Qwen3-VL-8B-Instruct` 등)으로 불러오므로 일반 폴더가 아니라 HF 캐시 구조여야 한다. 컨테이너 안에서 `hf download`는 `HUGGINGFACE_HUB_CACHE`(`/home/jyheo/workspace/VideoRAG/.cache/huggingface/hub`)에 저장하고, §4.1의 링크(`VideoRAG/.cache/huggingface` → `/DATA3/models/huggingface`)를 거쳐 실제 파일은 `/DATA3/models/huggingface/hub`에 쌓인다. 미리 받지 않아도 첫 모델 로드 때 같은 위치로 자동 다운로드된다(인터넷 필요):

| 모델 | revision | 이전 서버 snapshot 바이트 |
|---|---|---|
| `Qwen/Qwen3-VL-8B-Instruct` | `0c351dd01ed87e9c1b53cbc748cba10e6187ff3b` | 17,545,915,423 |
| `Qwen/Qwen3-Embedding-4B` | `5cf2132abc99cad020ac570b19d031efec650f2b` | 8,059,532,576 |
| `Qwen/Qwen2-VL-2B-Instruct` | `895c3a49bc3fa70a340399125c650a463535e71c` | 4,418,115,643 (가중치 4개 파일만 있었음. 전체를 받으면 작은 파일이 더해짐) |
| `VLM2Vec/VLM2Vec-V2.0` | `e39ff079b8275ef876d3656da8c0bddbff3c4dde` | 52,853,130 |

```bash
hf download <repo> --revision <revision>
```

- **모델(최소한 Qwen3-VL-8B 토크나이저)을 받은 뒤에 CPU 테스트와 dry-run을 실행한다.** `prebuild_episodic_index.count_tokens`는 `try_to_load_from_cache`로 HF 캐시(`HUGGINGFACE_HUB_CACHE`)에서 `tokenizer.json`을 찾기만 하고 내려받지 않는다. 없으면 `FileNotFoundError`(`test_openie_split_guard.py`, `--dry-run`이 사용).

### 4.4 경로 수정 (계획, **수정 전 보고·승인 필요**)

`/data1/jyheo/workspace/...`가 박혀 있는 파일 13개(✔ 전수 검색). 바꿀 값: `/data1/jyheo/workspace/VideoRAG` → `/home/jyheo/workspace/VideoRAG`, 모델 경로 `/data1/jyheo/workspace/.cache/huggingface` → `/DATA3/models/huggingface`(컨테이너 안에서는 `HUGGINGFACE_HUB_CACHE`가 우선해 모델 위치에 영향이 없지만, 컨테이너 밖 실행과 표기 일관성을 위해 바꾼다). 수정 전 사본을 `backups/`에 둔다.

| 파일 | 행 | 현재 값 |
|---|---|---|
| `config.yaml` | 6, 8, 10, 11, 13, 14, 59, 67, 68 (7행은 주석) | `paths.worldmm_root`, `paths.hf_home`, `caption_dir`, `metadata_dir`, `episodic_cache_root`, `log_dir`, `service.frames_dir`, `report.outputs_dir`, `report.deep_reporter_log_dir` |
| `domain_templates.py` | 45 | `DEEP_REPORT_ROOT` |
| `run_prebuild.sh` | 9 | `WORLDMM=` |
| `run_prebuild_http.sh` | 10 | `WORLDMM=` |
| `experiments/gpu_3videos.py` | 19 | `WORLDMM` |
| `tests/gpu/gpu_smoke.py` | 15 | `RF` |
| `tests/gpu/gpu_report_smoke.py` | 12 | `RF` |
| `scripts/launch/run_llm_server_capped.py` | 5, 7 | `sys.path`, `--config` |
| `scripts/launch/run_service_capped.py` | 9 | `sys.path` |
| `tests/unit/test_openie_split_guard.py` | 6, 18 | `HF_HOME`, `CAP` |
| `tests/unit/test_retriever.py` | 14 | `RF` |
| `tests/unit/test_templates.py` | 11 | `RF` |
| `analysis/openie_degeneration_exp.py` | 15, 24 | `HF_HOME`, `CAP` |

- 수정하지 않는 것: `tests/_artifacts/`, `outputs/`, `logs/`, `backups/` 안의 옛 경로(과거 실행 기록). `WorldMM/claude_output/full/*.sh`의 옛 경로(전처리를 다시 할 때만 쓰는 스크립트, 그때 판단).
- `experiments/delayed_gpu_3videos.py`는 2026-10-25 `--gpus` 인자를 받게 고쳤다. 새 서버에서는 컨테이너 안 번호(예: `--gpus 0,1`)로 넘긴다.
- `report_framework/`는 2026-10-25부터 git 저장소다(`.git/` 포함). rsync 규칙(`report_framework/**`)이 `.git/`도 함께 옮긴다. 루트 `CLAUDE.md`도 같은 날 갱신했다(규칙의 `/CLAUDE.md` 항목으로 옮겨진다).
- 문서 6종의 경로 표기와 §2.2 정정은 경로 수정 후 함께 갱신한다(기존 문서 수정 → 보고·승인).

### 4.5 검증 → 작업 재개 (계획)

1. CPU 테스트 5종(기대 30 / 50 / 67 / 9 / 18개 통과), 영상 3개 dry-run(기대 430회).
2. GPU 규칙을 사용자에게 확인 → `experiments/gpu_3videos.py --llm-gpu <A> --aux-gpu <B>` (사전 인덱싱 430회 → 보고서 3건). GPU를 혼자 쓰면 약 1–1.5시간(추정).
3. 이후 `DESIGN_AND_STATUS.md` §13.3 (2)·(3) 순서.

---

## 5. 그대로 이어지는 규칙 (사용자 지시)

- 분석과 답변은 추측·거짓 없이, 필요한 문서·코드를 직접 읽고 확인한 내용만. 확인하지 않은 것은 미확인이라고 쓴다.
- WorldMM, MERIT, Deep-Report 코드는 삭제·수정하지 않는다. 새 파일은 `report_framework/`에만 둔다. `report_framework/`의 기존 파일도 수정 전에 대상·위치·내용을 보고하고 승인을 받으며, 사본을 `backups/`에 둔다.
- GPU는 사용자가 허용한 GPU만, 다른 사용자의 프로세스를 절대 침범하지 않는 범위에서. 자기 PID만 종료한다. GPU 프로세스에는 메모리 상한(`scripts/launch/run_*_capped.py`, `--gpu-mem-cap-mib`)과 감시(`experiments/gpu_3videos.py`)를 쓴다.
- 대상 지정 없이 `uv sync`를 실행하지 않는다(`/opt/venv`의 langgraph 등 20여 개가 삭제됨).
- `-`로 시작하는 영상 id는 `--video-id=<id>`, `--videos=<id>`, `--preload=<id>` 형식으로 넘긴다.
- 답변은 한국어로.
- 루트 `VideoRAG/CLAUDE.md`는 옛 HolmesVAU 프로젝트 기준(컨테이너 `vau-rag`, `/claude_output`)이라 현재 규칙과 다르다. 갱신 여부는 사용자에게 확인한다.
