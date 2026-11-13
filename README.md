# report_framework — 장편 영상 근거 인용 보고서 생성 프레임워크

장편 영상에 대한 질의를 받아 **outline 계획 → 섹션별 영상 메모리 검색(Video-RAG) → 근거 인용이 붙은 보고서 작성 → 후처리·검증**을 수행한다.
검색은 [WorldMM](https://github.com/wgcyeo/WorldMM)의 메모리(episodic·semantic·visual)를, 보고서 생성은 [Deep-Report](https://github.com/fangda-ye/Deep-Report)의 그래프(planner/query/writer)를 쓴다. 검색기는 나중에 [MERIT](https://github.com/choi-yeeun/MERIT)로 바꿀 수 있게 HTTP 계약으로 분리했다.
첫 대상은 Video-MME long subset(WorldMM 메모리를 구축한 50개 영상)이고, 이후 관제(surveillance) 도메인으로 확장한다.

```
질의 ─► Deep-Reporter planner (영상 개요 = 10min 캡션) ─► 섹션 N개
         └─ 섹션마다: query 생성 ─► videorag_retriever_service (WorldMM episodic·semantic·visual) ─► writer
      ─► grounding_postprocessor (인용 번호·References·그림, 규칙 검사, 반복 제거, 결말 검사) ─► 검증 ─► report.md
```

## 폴더 배치

세 upstream 저장소와 이 저장소를 **같은 상위 폴더에 나란히** 둔다. 설정의 기본 경로가 이 배치를 가정한다(다른 배치는 `config.yaml`에서 바꾼다).

```
VideoRAG/
├── WorldMM/            github.com/wgcyeo/WorldMM @ 3a55b65 + patches/worldmm/*.patch
│   ├── data/Video-MME/ 데이터셋 (data/ = 영상, videomme/test.json)
│   └── output/memory/videomme_long_qwen3vl-8b/   구축된 메모리 + 사전 인덱스 (그 폴더의 README.md)
├── Deep-Report/        github.com/fangda-ye/Deep-Report @ ee9f853 (수정 없음, PYTHONPATH로 import)
├── MERIT/              github.com/choi-yeeun/MERIT @ 6edea6e (수정 없음, 아직 쓰지 않음)
└── report_framework/   이 저장소
```

이 저장소의 구성:

| 경로 | 내용 |
|---|---|
| `run_report.py` | 보고서 1건 생성 진입점 (사전 확인 → 생성 → 후처리 → 검증 → 저장) |
| `videorag_retriever_service.py` | Deep-Reporter 검색 계약을 구현한 WorldMM 검색 서비스 (Flask, 기본 포트 8020) |
| `local_llm_server.py` | Qwen3-VL-8B를 OpenAI 호환 API로 제공 (Flask, 기본 포트 8010) |
| `prebuild_episodic_index.py` | 영상별 HippoRAG 그래프 사전 구축 (OpenIE를 LLM 서버로) |
| `domain_templates.py` | Deep-Reporter 템플릿의 범위 한정 교체 (Video-MME용 planner·query·writer 규칙) |
| `grounding_postprocessor.py` | 인용·그림 정리, 규칙 기반 근거 검사, 반복 문장 제거, 영상 시작·끝 서술 검사 |
| `report_translator.py` | 한국어 번역 (섹션 단위, 인용·고유명사 보호) |
| `rf_config.py`, `config.yaml` | 설정과 경로 해석 |
| `run_prebuild.sh`, `run_prebuild_http.sh` | 사전 인덱싱 실행 스크립트 |
| `scripts/memory_build/` | WorldMM 메모리 구축 (자막 → 캡션 → 다단위 요약 → episodic/semantic/visual) |
| `scripts/launch/` | GPU 메모리 상한을 건 LLM 서버·검색 서비스 실행 래퍼 |
| `experiments/` | GPU 배치 실행기 (사전 인덱싱·보고서 반복 실행·검색 확인, 메모리 감시 포함) |
| `analysis/` | 결과 분석 도구 (CPU) → 결과는 `results/` |
| `tests/unit/`, `tests/gpu/`, `tests/fixtures/` | CPU 테스트, GPU 확인 스크립트, 테스트 입력 |
| `docker/` | 실행 환경 컨테이너 정의 |
| `patches/worldmm/` | 이 프레임워크가 의존하는 WorldMM 로컬 수정 |
| `docs/` | 설계·파이프라인·이슈 문서 (색인: `docs/README.md`) |
| `internal/` | 작업 기록 (상태·인수인계·분석·미팅·legacy) |
| `cache/`, `outputs/`, `logs/`, `backups/`, `tests/_artifacts/` | 실행 산출물 (git 제외) |

## 준비

1. **저장소**: 위 배치대로 clone하고 WorldMM은 `3a55b65`에서 patch를 적용한다(`patches/worldmm/README.md`).
2. **실행 환경**: `docker/`에서 `make docker-base`, `make docker-user`, `make docker-run` (CUDA 12.8, torch 2.8, `/opt/venv`). 컨테이너는 `WORLDMM_DIR`, `DEEPREPORTER_DIR`, `MERIT_DIR`, `PYTHONPATH=<Deep-Report>`를 설정하고 worldmm·hipporag·merit를 editable로 연결한다(`docker/Makefile` 머리 주석).
3. **모델** (HF 캐시): `Qwen/Qwen3-VL-8B-Instruct`, `Qwen/Qwen3-Embedding-4B`, `VLM2Vec/VLM2Vec-V2.0`, (메모리 구축 시) Whisper `distil-large-v3.5`.
4. **데이터**: Video-MME 영상을 `WorldMM/data/Video-MME/data/`에, 메모리를 `WorldMM/output/memory/videomme_long_qwen3vl-8b/`에 둔다. 메모리를 새로 만들려면 아래 "메모리 구축".
5. **설정** `config.yaml`: 경로 값은 `report_framework/` 기준 상대 경로, `${VAR}`(환경변수), 절대 경로 중 하나로 쓴다(`rf_config.py`). 기기마다 바꿔야 하는 값은 `paths.hf_home`(모델 캐시)이다.

## 실행

**메모리 구축** (선택, GPU, 영상당 수 시간): `scripts/memory_build/queue_worker.sh <GPU>`를 GPU마다 하나씩 띄운다. 영상 목록은 메모리 폴더의 `lists/video_list.json`, 진행은 `full_status.sh`. 설정과 동작은 각 스크립트 머리 주석에 있다.

**사전 인덱싱** (GPU): 검색 서비스는 사전 구축된 HippoRAG 그래프가 없는 영상을 거부한다(HTTP 409).

```bash
python prebuild_episodic_index.py --config config.yaml --dry-run          # 계획만 (모델·쓰기 없음): 영상별 남은 OpenIE 호출 수
./run_prebuild_http.sh <LLM_GPUS e.g. 4,5,6> <INDEXER_GPU e.g. 7> [--videos=<vid>]
```

**보고서 생성** (GPU, LLM 서버와 검색 서비스를 먼저 띄운다):

```bash
python local_llm_server.py --config config.yaml --gpu 0                 # :8010
python videorag_retriever_service.py --config config.yaml --gpu 1 --preload=<VID>   # :8020
python run_report.py --config config.yaml --video-id=<VID> \
    --query "Write a report describing what happens in this video: ..." [--checklist "..."] [--out-dir <dir>]
```

- `-`로 시작하는 영상 id는 `--video-id=<id>`, `--preload=<id>`처럼 `=`로 넘긴다.
- 출력(`<out-dir>`, 기본 `outputs/<vid>_<시각>/`): `report.md`(근거 정리본), `report_raw.md`, `report.json`, `validation.json`, `frames/`, `report_ko.md`(한국어 번역본: `config.yaml`의 `report.translate_ko`로 켜고 끔, 기본 `false`).
- 종료 코드: 0 = 검증 통과, 1 = 검증 오류(출력은 씀), 2 = 사전 확인·설정 실패.
- 다른 사용자와 GPU를 같이 쓰면 상한 래퍼(`scripts/launch/run_*_capped.py`)와 감시가 있는 배치 실행기(`experiments/gpu_3videos.py`, `gpu_report_batch.py`)를 쓴다.

**테스트** (CPU, 모델 없음, WorldMM 메모리와 영상 파일은 읽음):

```bash
for t in tests/unit/test_*.py; do CUDA_VISIBLE_DEVICES= python -B "$t"; done   # 각 파일 끝의 ALL PASS / RESULT 줄로 판정
```

## 현재 상태

- 50개 영상의 WorldMM 메모리는 구축되어 있다. 사전 인덱스는 검증 영상 3개(`-QuCz7kxBr8`, `0RxMZBLeqRI`, `54k2g9ddy4M`)만 있다.
- 현재 상태와 다음 작업: `internal/status/CURRENT_STATUS.md`. 알려진 품질 문제와 대응: `docs/REPORT_ISSUES_AND_FIXES.md`. 설계·결정·검증 기록: `internal/status/DESIGN_AND_STATUS.md`.
- 2026-11-10 경로·폴더 정리 기록: `internal/status/REORG_LOG_20261110.md`.
- 배포·공유본: `VideoRAG/longvideo-report/`. 같은 코드를 패키지 구조로 정리했고(2026-11-13), 이후 개발은 그쪽에서 한다. WorldMM·Deep-Report 원본에서 바꾼 점은 각 폴더의 `LOCAL_CHANGES.md`에 있다.
