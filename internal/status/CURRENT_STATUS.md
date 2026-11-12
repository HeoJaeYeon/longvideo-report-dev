# 현재 상태 (2026-11-12)

이 문서는 "지금 어디까지 됐고 다음에 무엇을 하나"만 짧게 적는다. 근거와 이력은 `DESIGN_AND_STATUS.md`(기록), 정리 작업 기록은 `REORG_LOG_20261110.md`, 문서 위치는 `docs/README.md`.
상태가 바뀌면 이 문서를 고쳐 쓴다(이력은 쌓지 않는다).

## 1. 무엇이 되는가

- 장편 영상 1개와 질의를 받아 근거 인용이 붙은 영어 보고서를 만든다: LLM 서버(`local_llm_server.py`, Qwen3-VL-8B) + 검색 서비스(`videorag_retriever_service.py`, WorldMM) + `run_report.py`.
- 출력: `report.md`(섹션 6개 이하, 결론 포함, 본문 인용 `[n]`, 그림, References), `report_raw.md`, `report.json`, `validation.json`, `frames/`. 한국어 번역본 `report_ko.md`는 `config.yaml`의 `report.translate_ko`로 켠다(기본 off).
- 보고서 1건: LLM 호출 1 + 3 × 섹션 수, 생성 약 5–7분(기준 실행 9건 297–418초).
- 데이터
  - WorldMM 메모리(Video-MME long 50개 영상): `WorldMM/output/memory/videomme_long_qwen3vl-8b/` (그 폴더의 `README.md`, `MANIFEST.json`).
  - 사전 인덱스(HippoRAG)는 **검증 영상 3개만** 있다(`-QuCz7kxBr8`, `0RxMZBLeqRI`, `54k2g9ddy4M`). 나머지 47개 영상은 사전 인덱싱 전이라 검색 서비스가 거부한다(C-7, 약 12,780회 OpenIE 호출, GPU 필요).

## 2. 확인 상태

| 항목 | 상태 |
|---|---|
| 실제 모델 실행 | 마지막: 2026-10-25 기준 실행 9건(`outputs/p9p19_check_20261025_141401/`, 9건 `passed`) |
| 2026-10-26 코드 수정(영상 끝 근거 txt0, 반복 경고 기준, 결말 검사 오탐) | CPU만 확인, GPU 미확인 |
| 2026-11-10–12 정리(경로·폴더·문서, References 형식, 번역 기본 off) | CPU 테스트 6종(새 clone 포함), `--dry-run`, 분석 재현으로 확인. **GPU로 새 경로 실행은 미확인(P7)** |
| 품질 평가(Video-MME 문항 풀이, 자동 지표, 사람 검수) | 시작 안 함 |

## 3. 알려진 품질 한계 (기준 실행 9건, 상세: `internal/analysis/REPORT_TEXT_REVIEW.md`, `docs/REPORT_ISSUES_AND_FIXES.md`)

- 영상의 큰 구간 누락 9/9, 결말 오류 4/9, 같은 보고서 안 사실·시각 불일치, 섹션 사이 반복, 근거에 없는 해석·서사 덧씌우기.
- 같은 조건에서도 다루는 구간이 실행마다 크게 다르다(샘플링, seed 없음; `internal/analysis/SELF_CONSISTENCY_*.md`).
- 검증(`validation.json`)은 형식·인용·일부 규칙만 본다. 의미 수준 오류는 잡지 못해 9건 모두 `passed`였다.
- 확인된 원인 C1–C13(입력 자료, planning, 섹션 단위 독립 검색·작성, 후처리), 미확인 H1–H7.

## 4. 다음 작업 (위에서부터)

1. **P7 (GPU 필요)**: 새 경로로 LLM 서버·검색 서비스를 띄워 보고서 1건 생성·검증. GPU는 사용자 허용 시에만.
2. (완료 2026-11-12) 옛 원본 삭제: `WorldMM/claude_output/full/`, `report_framework/cache/episodic/`, `Deep-Report/Docker/`, `backups/cache_after_c1_verified_20261025/`(모두 사본과 바이트 동일 확인 후, 목록 `internal/legacy/DELETED_20261112_originals.txt`).
3. **사용자 결정 대기**: (b) 단계 패키지 구조화(이름·시점), 외부 공개 방식(새 저장소·라이선스·데이터), 원인 분리 실험 E1–E4(GPU), 평가 지표 조사·적용, 결정 7(근거 구성) 실험, C-7(50개 영상 사전 인덱싱).

## 5. 작업 규칙

- 세션 지침: `VideoRAG/CLAUDE.md`. 상세 규칙: `DESIGN_AND_STATUS.md` §13.1.
- 같은 작업 폴더에서 Claude 세션은 하나만 쓴다(I30). 2026-11-12에 남아 있던 다른 세션 7개를 종료했다.
