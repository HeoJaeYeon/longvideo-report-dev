# 문서 색인

프로젝트 개요·설치·실행은 저장소 루트의 `README.md`를 먼저 본다. 모든 문서는 한국어이고, 시각은 UTC다.

## `docs/` — 프레임워크를 이해하기 위한 문서

| 문서 | 내용 |
|---|---|
| `FRAMEWORK_OVERVIEW.md` | 설계·통합·이슈를 한 번에 정리한 개요 (구성 요소, 결정, 주요 이슈) |
| `REPORT_PIPELINE.md` | 보고서 1건이 만들어지는 단계별 구조와 실제 입력·출력 (planner → query → 검색 → writer → 후처리·검증) |
| `PIPELINE_WALKTHROUGH.md` | 영상 3개로 따라가 보는 파이프라인 튜토리얼과 단계별 이슈 이력 |
| `REPORT_ISSUES_AND_FIXES.md` | 보고서 품질 문제 P1–P19, 파이프라인·운영 문제 I1–I30과 대응 상태 |

## `internal/` — 작업 기록 (내부용)

| 위치 | 내용 |
|---|---|
| `internal/status/CURRENT_STATUS.md` | 지금의 상태와 다음 작업 (짧은 요약, 상태가 바뀌면 고쳐 씀) |
| `internal/status/DESIGN_AND_STATUS.md` | 분석·설계·구현·검증의 전체 기록과 인수인계(§2 현재 상태, §13 인수인계) |
| `internal/status/MIGRATION_HANDOFF.md` | 서버 이전 메모 |
| `internal/status/REORG_LOG_20261110.md` | 2026-11-10 경로·폴더 정리 기록 (무엇을 어디로 옮겼고 어떻게 확인했는지) |
| `internal/analysis/` | 결정 4·7 분석(`ANALYSIS_D4_D7.md`), 보고서 9건 텍스트 분석(`REPORT_TEXT_REVIEW.md`), 반복 실행 간 차이(`SELF_CONSISTENCY_{ANALYSIS,CAUSES}.md`) |
| `internal/meetings/` | 미팅·발표 자료 구성안 |
| `internal/running_example/` | 영상 3개 실행의 단계별 실제 입력·출력 (`RUNNING_EXAMPLE.md`, 그림 `assets/`). `analysis/build_running_example_combined.py`로 다시 만든다 |
| `internal/inspect/` | 기준 실행 9건의 프롬프트·근거·후처리 원문. `analysis/export_stages.py`로 다시 만든다 |
| `internal/legacy/` | 프레임워크 이전·바깥에서 만든 기록 (색인: 그 폴더의 `README.md`) |

문서 안의 다른 문서 이름(예: `DESIGN_AND_STATUS.md` §13)은 위 표의 위치를 가리킨다.
