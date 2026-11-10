# internal/legacy — 프레임워크 이전·바깥에서 만든 기록 (2026-11-10 정리)

`report_framework/` 밖의 `claude_output/` 폴더들에 흩어져 있던 이 프로젝트 관련 문서와 증거 파일을 한곳에 모았다.
모두 **당시 기록**이다. 본문 경로(`/data1/jyheo/workspace/VAU_RAG/...` 등)와 수치는 작성 시점 기준이며 고치지 않았다.
원본은 `report_framework/internal/REORG_LOG_20261110.md`에 적은 대로 남아 있거나(문서) 지워졌다(pilot·smoke).

| 폴더 | 원래 위치 | 내용 |
|---|---|---|
| `videorag/` | `VideoRAG/claude_output/` | 2026-10-13~20 통합 전 분석·설계 문서 6개 (`VideoRAG_ReportGen_analysis*.md`, `WorldMM_DeepReport_integration_{strategy,design}.md`, `deepreporter_env_compat_checklist.md`, `PROJECT_CONTEXT_HANDOFF.md`). 같은 폴더의 HolmesVAU·HIVAU 문서 3개는 다른 프로젝트라 가져오지 않았다 |
| `deep-report/` | `Deep-Report/claude_output/` | Deep-Report 분석, 통합 맥락, Docker 구성 기록 3개 |
| `deep-report/reverted_README_korean_tree.patch` | `Deep-Report/README.md`의 로컬 수정 | 한국어 디렉토리 설명 26줄. 2026-11-10 Deep-Report를 원본으로 되돌리면서 내용을 보존 |
| `worldmm/` | `WorldMM/claude_output/` | 2026-09 WorldMM 재현 기록: `HANDOFF.md`(로컬 수정 이유 §2), `REPORT.md`(pilot 결과), `WorldMM_analysis.md` |
| `worldmm/pilot_results/` | `WorldMM/claude_output/pilot/` | pilot QA 평가 결과(8개 영상 24문항, 보정 12/24)와 평가 실행 스크립트(`run_pilot_eval.py`, `run_reeval.py`), 문항 `pilot_test.json`. pilot의 나머지(평가 캐시·로그·셸 스크립트)는 지웠다 |
| `worldmm/diag/` | `WorldMM/claude_output/{diag_concurrency.py, logs/}` | 동시 `generate()` → CUDA 오류 진단(`patches/worldmm/0001`의 lock 근거) |
| `worldmm/Docker/` | `WorldMM/Docker/` (로그 제외) | 예전 `worldmm` 컨테이너 정의. 메모리 구축이 쓰는 `WorldMM/.venv`를 만든 환경 |
| `worldmm/reverted_4_eval_model_names.patch` | `WorldMM/script/{,videomme/}4_eval.sh`의 로컬 수정 | 모델명 `qwen3vl`(WorldMM `MODEL_DICT`에 없는 이름이라 `ValueError`). 2026-11-10 원본으로 되돌리면서 보존 |
| `worldmm/DELETED_20261110_pilot_smoke.txt` | — | 지운 pilot·smoke 파일 412개(md5·크기)와 끊어진 링크 18개 목록 |

pilot의 영상 8개 메모리는 다시 쓸 수 있어 `WorldMM/output/memory/videomme_long_pilot8_qwen3vl-8b/`로 옮겼다.
