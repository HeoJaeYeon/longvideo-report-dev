# 현재 상태 (2026-11-13)

이 문서는 "지금 어디까지 됐고 다음에 무엇을 하나"만 짧게 적는다. 근거와 이력은 `DESIGN_AND_STATUS.md`(기록), 정리 작업 기록은 `REORG_LOG_20261110.md`, 문서 위치는 `docs/README.md`.
상태가 바뀌면 이 문서를 고쳐 쓴다(이력은 쌓지 않는다).

## 0. 저장소 두 개 (2026-11-13)

| 위치 | 성격 | 내용 |
|---|---|---|
| `VideoRAG/report_framework/` (이 저장소) | 내부본 | 개발 기록·분석 문서·실행 결과·인수인계 맥락 전체. 코드는 2026-11-13 시점 그대로(스크립트가 루트에 있는 구조). git 원격 `origin`은 개인 비공개 저장소(이력 보관용) |
| `VideoRAG/longvideo-report/` | 배포·공유본 | 같은 코드를 패키지 구조(`src/longvideo_report/`, 명령 4개)로 정리하고 설정·스크립트·테스트·fixtures·results를 넣었다. **이후 개발은 여기서 한다.** 사용법은 그 `README.md` |

- WorldMM·Deep-Report 원본에서 바꾼 점(목적, 위치, 되돌린 것, 지운 것)은 각 폴더의 `LOCAL_CHANGES.md`에 있다.

## 1. 무엇이 되는가

- 장편 영상 1개와 질의를 받아 근거 인용이 붙은 영어 보고서를 만든다: LLM 서버(`local_llm_server.py`, Qwen3-VL-8B) + 검색 서비스(`videorag_retriever_service.py`, WorldMM) + `run_report.py`.
- 출력: `report.md`(섹션 6개 이하, 결론 포함, 본문 인용 `[n]`, 그림, References), `report_raw.md`, `report.json`, `validation.json`, `frames/`. 한국어 번역본 `report_ko.md`는 `config.yaml`의 `report.translate_ko`로 켠다(기본 off).
- 보고서 1건: LLM 호출 1 + 3 × 섹션 수, 생성 약 5–7분(기준 실행 9건 297–418초).
- 데이터
  - WorldMM 메모리(Video-MME long 50개 영상): `WorldMM/output/memory/videomme_long_qwen3vl-8b/` (그 폴더의 `README.md`, `MANIFEST.json`). 시험 구축한 8개 영상 메모리(`videomme_long_pilot8_qwen3vl-8b/`)도 보존한다.
  - 사전 인덱스(HippoRAG)는 **검증 영상 3개만** 있다(`-QuCz7kxBr8`, `0RxMZBLeqRI`, `54k2g9ddy4M`). 나머지 47개 영상은 사전 인덱싱 전이라 검색 서비스가 거부한다(C-7, 약 12,780회 OpenIE 호출, GPU 필요).

## 2. 확인 상태

| 항목 | 상태 |
|---|---|
| 실제 모델 실행 | 마지막: 2026-10-25 기준 실행 9건(`outputs/p9p19_check_20261025_141401/`, 9건 `passed`) |
| 2026-10-26 코드 수정(영상 끝 근거 txt0, 반복 경고 기준, 결말 검사 오탐) | CPU만 확인, GPU 미확인 |
| 2026-11-10–12 정리(경로·폴더·문서, References 형식, 번역 기본 off) | CPU 테스트 6종(새 clone 포함), `--dry-run`, 분석 재현으로 확인 |
| 2026-11-13 패키지 구조(`longvideo-report/`) | CPU 테스트 6종(검사 206개)이 이 저장소와 같은 결과, `--dry-run`·템플릿 검사 출력 바이트 동일, 패키지 빌드와 명령 4개 확인 |
| GPU로 새 구조 실행 | **미확인(P7)** |
| 품질 평가(Video-MME 문항 풀이, 자동 지표, 사람 검수) | 시작 안 함 |

## 3. 알려진 품질 한계 (기준 실행 9건, 상세: `internal/analysis/REPORT_TEXT_REVIEW.md`, `docs/REPORT_ISSUES_AND_FIXES.md`)

- 영상의 큰 구간 누락 9/9, 결말 오류 4/9, 같은 보고서 안 사실·시각 불일치, 섹션 사이 반복, 근거에 없는 해석·서사 덧씌우기.
- 같은 조건에서도 다루는 구간이 실행마다 크게 다르다(샘플링, seed 없음; `internal/analysis/SELF_CONSISTENCY_*.md`).
- 검증(`validation.json`)은 형식·인용·일부 규칙만 본다. 의미 수준 오류는 잡지 못해 9건 모두 `passed`였다.
- 확인된 원인 C1–C13(입력 자료, planning, 섹션 단위 독립 검색·작성, 후처리), 미확인 H1–H7.

## 4. 다음 작업 (위에서부터)

1. **P7 (GPU 필요)**: `longvideo-report/` 구조로 LLM 서버·검색 서비스를 띄워 보고서 1건 생성·검증. GPU는 사용자 허용 시에만. 패키지는 아직 `/opt/venv`에 설치하지 않았다(설치 전에는 `PYTHONPATH=<longvideo-report>/src`).
2. **미뤄 둔 정리** (2026-11-13 사용자 결정, 정리 작업이 끝난 뒤 시작, 대상은 `longvideo-report/`):
   설정 경로 기준을 config 파일 위치로, 시간 변환 함수 정리, 의존성 명시와 `/opt/venv` 설치, 한국어 문자열(한국어로 진행), 테스트의 pytest 전환,
   코드 주석의 내부 이슈 번호, 기존 pyflakes 경고 13개, `tests/gpu/gpu_e2e.py`의 고정 GPU 번호.
3. **사용자 결정 대기**: 원인 분리 실험 E1–E4(GPU), 평가 지표 조사·적용, 결정 7(근거 구성) 실험, C-7(47개 영상 사전 인덱싱).
4. (완료) 2026-11-12 옛 원본 삭제(목록 `internal/legacy/DELETED_20261112_originals.txt`), 2026-11-13 WorldMM·Deep-Report 안의 쓰지 않는 파일 정리(`DELETED_20261113_upstream_leftovers.txt`)와 커밋 이력의 공동 작성자 줄 제거(`REORG_LOG_20261110.md` §21).

## 5. 작업 규칙

- 세션 지침: `VideoRAG/CLAUDE.md`. 상세 규칙: `DESIGN_AND_STATUS.md` §13.1.
- 같은 작업 폴더에서 Claude 세션은 하나만 쓴다(I30). 2026-11-12에 남아 있던 다른 세션 7개를 종료했다.
- 커밋 메시지에 Claude 공동 작성자 줄(`Co-Authored-By`)을 넣지 않는다(2026-11-13 사용자 지시).
- 연구실 내부 문서(md)는 한국어로 쓴다.
