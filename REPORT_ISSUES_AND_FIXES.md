# 문제점과 개선 이력

- 작성: 2026-10-22. 최종 갱신: 2026-10-26 (P8·P12 측정, P19 영상 끝 근거; 2026-10-25: P9·P19 대응과 확인, I28 수정; I4 정정, I22 검증 영상 해당 여부, I23 백업 범위 정정, I27 대기 실행·GPU 지시 갱신, C-1·C-2 결과로 I23·I24 GPU 검증, I28 추가). 시각은 컨테이너 시계(UTC) 기준이다(`DESIGN_AND_STATUS.md` §0.3).
- 범위: (1) 실제 모델(Qwen3-VL-8B)로 생성한 **보고서의 품질 문제** P1–P19, (2) 프레임워크를 만들면서 겪은 **파이프라인·개발 과정 문제** I1–I30.
- 문제마다 확인한 현상, 원인, 검토한 방법, 결정과 수정, 효과, 남은 한계를 정리했다.
- 관련 문서: 구조와 현재 상태는 `DESIGN_AND_STATUS.md`, 보고서 생성 단계는 `REPORT_PIPELINE.md`, 반복·근거 구성 분석은 `ANALYSIS_D4_D7.md`.

## 0. 읽는 법

### 0.1 표기

| 표기 | 의미 |
|---|---|
| (대조) | 사람이 근거 원문과 직접 대조해 확인 |
| (규칙 출력) | 규칙 근거 검사기의 출력을 그대로 옮김. 개별 대조는 하지 않음 |
| (코드) | 소스 코드를 읽어 확인 |
| (실측) | 실행 결과·로그·파일에서 측정 |
| (가설) | 원인을 확인하지 못한 추정 |
| ✅ 해결 / 🟡 부분 대응 / ⏳ 측정 대기 / ⛔ 미대응 | 대응 상태 |

### 0.2 대상 보고서

| | 보고서 A: 스모크 | 보고서 B: `run_report.py` 첫 실행 |
|---|---|---|
| 생성 경로 | `tests/gpu_report_smoke.py` (`run_report.py` 이전) | `tests/gpu_e2e.py` → `run_report.py` 전체 흐름 |
| 결과 위치 | 원본 `tests/_artifacts/gpu_report/` (`report.md`, `outline.json`, `llm_server.log`), 후처리본 `tests/_artifacts/pipeline_test/smoke_grounded/report.md` | `tests/_artifacts/gpu_e2e/outputs/report_run1/` (`report.md`, `report_ko.md`, `report.json`, `validation.json`), 로그 `tests/_artifacts/gpu_e2e/` |
| 적용된 템플릿 | videomme 템플릿. writer 규칙 4 **없음**, 결론 규칙 **없음** | 규칙 4 + 결론 섹션·섹션 상한 6(결정 5) + 번역(결정 6) |
| 이후 추가돼 **적용되지 않은** 것 | 위의 모든 개선 | 규칙 6·C0(결정 4), 부정 절 처리, 이미지 시간 기록, 번역 한자 감지·이름 보호 |
| 지표 | `tests/_artifacts/analysis/smoke_metrics.json` | `tests/_artifacts/analysis/e2e_run1_metrics.json` |

- 공통 조건: 영상 `-QuCz7kxBr8`(Video-MME, 약 32분, 농구 가젯 리뷰), Qwen3-VL-8B 로컬, L1 필터, **episodic 10sec 단위만**, Deep-Reporter filter off.
- 공통 query: `"Write a report describing what happens in this video: who takes part, what is tested, and how the tests turn out."`

### 0.3 해석할 때의 한계
- 보고서는 조건마다 1건뿐이다.
- 생성은 샘플링 방식(temperature 0.7, top_p 0.8, top_k 20; 모델 기본값)이라 같은 조건에서도 결과가 달라진다. 그래서 A와 B의 차이를 모두 수정 효과로 볼 수 없다. 아래 "효과"는 그 1회 실행에서 관측된 값이다.
- 10sec 단위만 썼으므로 4개 단위(10sec/30sec/3min/10min) 조건과 다를 수 있다.

---

## 1. 요약표

### 1.1 보고서 품질 문제

| # | 문제 | A | B | 대응 | 상태 |
|---|---|---|---|---|---|
| P1 | 이미지 인용을 텍스트 형식 `[citation:imgN]`으로 씀 | 14개 중 8개 | 19개 중 4개 | writer 규칙 4 + 후처리에서 그림으로 변환 | ✅ (변환은 계속 필요) |
| P2 | 이미지가 있는데도 넣지 않은 섹션 | S4, S5 | 결론 외 5개 섹션 모두 넣음 | 의무화하지 않음(결정 3) | ✅ 정책 결정 |
| P3 | 인용이 붙었지만 근거에 없는 수치·문구 | 4건 (대조) | 4건 (규칙 출력, 현재 규칙) | 규칙 근거 검사로 경고 | 🟡 감지만 |
| P4 | 다른 근거의 내용·시간을 인용 | 실제 오류 3건 (대조) | 3건 (규칙 출력) | 규칙 근거 검사로 경고 | 🟡 감지만 |
| P5 | planner 섹션 설명의 내용이 근거 없이 본문에 들어감 | `0/1`, `3/16` | "Flick Glove" | 경고. C0로 결론 쪽 완화 기대 | ⏳ |
| P6 | 다른 장면을 같은 사건으로 엮음 | S5 (대조) | 미확인 | 없음 | ⛔ 감지 안 됨 |
| P7 | 섹션 주제와 검색 근거가 맞지 않음 | S3 | "근거에 없다" 문장 10개 | 없음 (4개 단위 캐시 후 재측정) | ⛔ |
| P8 | 시간 순서가 섞임 | S3, S5 | 미측정 | 없음. 2026-10-26 측정(20건): 섹션 순서 역전 3건, 섹션 안 시각 역행 14건 | ⛔ 측정됨, 대응 없음 |
| P9 | 같은 단락·문장 반복, writer 반복 루프 | 최대 0.901 | 최대 0.235 | 규칙 6 + C0. C-5 루프 2/8건 → 2026-10-25 서버 상한 3,072 + 같은 문장 제거 + 경고. 수정 후 루프 2/9건이 130–134초에 끊기고 반복 문장 제거. 2026-10-26: "loop suspected" 기준을 5회 이상 또는 끊김으로 변경 | 🟡 루프 시간·노출 대응, 발생은 남음 |
| P10 | 결론 없음, query 일부만 다룸 | 결론 없음 | `Conclusion:` 244단어 | 결론 섹션 강제 + 상한 6(결정 5) | ✅ |
| P11 | 결론 섹션의 인용 불일치 | — | 결론 지적 7건 | C0로 완화 기대 | ⏳ |
| P12 | 근거 없는 추측·해석 표현 | 미측정 | 5문장 | 없음. 2026-10-26 측정: 다수가 30sec·3min·10min 요약 캡션의 해석 표현을 옮긴 것 | ⛔ 원인 확인, 대응 없음 |
| P13 | semantic 근거의 가치가 낮음 | 인용 11/20 | 인용 6/24 | 결정 7 보류 | ⏳ |
| P14 | 이미지와 텍스트 근거의 시간이 떨어져 있음 | 최대 1,415초 | 인용 이미지 최대 1,015초 | `validation.json`에 기록 | 🟡 기록만 |
| P15 | 번역 품질: 한자 혼입, 이름 표기 불일치, 제목 형식 | — | 확인 | 한자·가나 감지·재시도, 고유명사 보호 | ⏳ (제목 형식 ⛔) |
| P16 | 인용이 섹션 내 번호라 사람이 검증할 수 없음 | 해당 | 해결 | 후처리기(전역 번호, References, 그림) | ✅ |
| P17 | 조용한 실패 (fallback, `Call failed`, 섹션 16개 이상 시 소실) | 미발생 | 미발생 | 사전 확인·사후 검증 | ✅ |
| P18 | 규칙 검사가 부정문 속 토큰을 오류로 잡음 | — | 오탐 2건 | 부정 절(absence) 처리 | ✅ (한계 있음) |
| P19 | 구간 요약의 "the video closes/opens" 같은 표현이 영상 전체의 결말·시작으로 옮겨짐 | — | — (C-4 보고서 1: 18:29를 결말로 서술, 실제 37:37) | writer 규칙 7(실제 영상 끝 포함) + 결말·시작 서술 검사(경고). 2026-10-26: 영상 마지막 약 60초 캡션을 근거 txt0으로 제공, 소유격 오탐 수정(GPU 확인 전) | 🟡 검출, 발생은 남음 |

### 1.2 파이프라인·개발 과정 문제

| # | 문제 | 대응 | 상태 |
|---|---|---|---|
| I1 | 실행 환경을 `WorldMM/.venv`로 오인해 flask를 그쪽에 설치 | 실제 환경 `/opt/venv` 확인, 설치는 사용자 지시로 유지 | ✅ |
| I2 | `WorldMM/.venv`가 이름 변경 전 경로(`VAU_RAG`)를 가리킴 | 76개 파일 경로 치환 + `uv sync --frozen --inexact` | ✅ |
| I3 | 대상 지정 없는 `uv sync`가 `/opt/venv` 패키지 20여 개를 삭제함 | 금지 규칙, 대상·옵션 명시 | ✅ 규칙화 |
| I4 | 환경변수 `HF_HOME` 경로에 모델이 없음(2026-10-21 15:36 시점) | `paths.hf_home`을 `HF_HOME`에 설정 → **효과 없음**(컨테이너의 `HUGGINGFACE_HUB_CACHE`가 우선, 2026-10-25 확인). 이후 GPU 스모크가 그 경로에 모델을 내려받아 동작은 정상 | 🟡 정정 |
| I5 | 셸 `grep`이 ignore 파일을 따라 일부 경로를 건너뜀 | 전수 검색에 `/usr/bin/grep` 사용 | ✅ 규칙화 |
| I6 | Deep-Reporter 설정 dict가 키·URL을 버림 | 환경변수로 주입 + 라우팅 결과 확인 | ✅ |
| I7 | Deep-Reporter 순환 import, 모듈 이름이 함수로 가려짐 | `deep_reporter.api` 먼저 import, `__globals__`로 교체 대상 지정, `sys.modules` 사용 | ✅ |
| I8 | Deep-Reporter 프롬프트가 웹 리포트 전제 | 범위 한정 템플릿 교체(videomme) | ✅ |
| I9 | WorldMM이 HippoRAG 캐시 라벨을 `gpt-5-mini`로 남김 | `LabeledEpisodicMemory` | ✅ |
| I10 | HippoRAG OpenIE가 오류를 삼키고 빈 결과를 캐시에 저장 | 로드 전 완전성 검사(409), 빈 triple은 시드 제외 | 🟡 (재시도 소진분은 "완료"로 간주) |
| I11 | WorldMM episodic 검색이 쿼리당 LLM 최대 5회 | L1 설계(요청당 1회) | ✅ |
| I12 | WorldMM 검색 결과에 점수가 없음 | 순위 기반 병합(RRF) | ✅ |
| I13 | `visual.retrieve()`가 특정 질의를 시간 범위로 해석, 기존 프레임 함수는 구간 시작 프레임 | 유사도 검색 함수 직접 호출, decord로 구간 중앙 프레임 | ✅ |
| I14 | HippoRAG 그래프 검색이 assert로 실패할 수 있음 | dense passage retrieval로 대체 | ✅ |
| I15 | full 모드에서 쿼리별 결과가 겹치면 근거 수가 줄어듦 | 쿼리당 개수를 `max(설정값, ceil(n/쿼리 수))`로. C-3 실제 모델에서 4–8개(겹침 시 부족 남음) | 🟡 |
| I16 | L1 응답 파싱 실패로 RRF가 채워도 `llm`으로 표시 | 문서화 | ⛔ |
| I17 | Deep-Reporter `recursion_limit=50`: 16섹션부터 보고서 전체 소실("16개" 계산은 틀림) | 실측 후 `max_sections` 3–15로 제한 | ✅ |
| I18 | 사전 인덱싱이 GPU 1장에서 20GB를 넘음 | 결정 1 = A안(OpenIE를 LLM 서버 HTTP로) | ✅ 구현 (시험 중지) |
| I19 | `-`로 시작하는 영상 id를 argparse가 옵션으로 해석 | `--video-id=<id>` 형식 사용 | ✅ 규칙화 |
| I20 | 시험 인덱싱 첫 실행이 `logs/` 폴더 없음으로 실패 | 폴더 생성 후 재실행 | ✅ |
| I21 | 테스트 하네스 문제(`search_node` 실행 맥락, 구분 문구 변경, 테스트 기대값 오류) | 테스트 수정 | ✅ |
| I22 | 10min 캡션 232개 중 32개(영상 20개)가 전처리에서 2,048토큰에 잘림 | 원인 확인. 재생성은 보류(사용자 결정), 한계로 기록 | ⛔ 보류 |
| I23 | 10min 청크의 OpenIE 출력이 2,048토큰 상한을 넘어 JSON이 잘리고, 청크당 최대 15회 재시도 | 긴 청크 분할 OpenIE + 잘린 응답 구제 | ✅ 구현, GPU 검증(2026-10-25 C-1: 호출 = 계획, 구제 5건). 분할 기준 아래 입력에서도 잘림 3건 |
| I24 | OpenIE 열거 폭주(같은 주어·술어에 목적어만 바꿔 39–115회). 상한 전에 끝나면 그래프에 그대로 들어감 | 연속 15개 초과 절단. 디코딩 설정 변경은 실험 후 기각 | ✅ 구현, GPU 검증(C-1 절단 146개). 정당한 나열도 자름 |
| I25 | `local_llm_server`의 `finish_reason`이 잘린 응답을 `stop`으로 표시할 수 있음 | 구제 조건을 `finish_reason`이 아닌 파싱 실패로 정함. 서버는 미수정 | 🟡 우회 |
| I26 | 진행 보고·분석 중 집계 오류 3건(호출 수 2배, 실패 응답 13→14, M2 5→4), 2026-10-25 기록 오류 4건(I4 해결 주장, 대기 실행 종료 시각, 백업 범위, 실행 날짜) | 정정 | ✅ |
| I29 | 같은 영상을 서비스 2개가 동시에 불러오면 OpenIE 캐시 파일 읽기 실패(HippoRAG가 불러올 때마다 파일을 다시 씀) | 배치 스크립트에 영상별 불러오기 잠금. 캐시 무결성 확인 | ✅ (C-5) |
| I28 | LLM 서버 토크나이저 동시 사용 오류 `Already borrowed`(C-1 261건) | 2026-10-25 `count_tokens`를 생성 잠금 안으로(승인 후 수정) | ✅ 수정(실측 효과는 동시 요청이 많은 사전 인덱싱에서 확인 필요) |
| I27 | GPU 공유: 다른 사용자 메모리가 실행 중 크게 늘어 우리 실행이 중단됨(14:10), 대기 실행은 6시간 동안 시작 조건 미충족(16:05–00:06) | 메모리 감시·자동 중단, 대기 후 여유 확인 시작. 2026-10-25 GPU 4–7에서 C-1–C-5 실행(감시 중단 0회) | ✅ 해소(현재 GPU 4–7 비어 있음) |
| I30 | 같은 작업 폴더에서 Claude 세션 2개가 겹쳐 실행(2026-10-25 13:39–13:49), 이전 세션이 문서를 고치고 커밋 | 세션 하나만 쓰기, 실행은 `setsid`·결과 파일로 확인 | 🟡 운영 규칙 |

---

## 2. 보고서 품질 문제 상세

### P1. 이미지 인용 형식 오류 — ✅
- **현상 (A, 실측)**: 이미지 인용 14개 중 8개를 `![](citation:imgN)`이 아니라 `[citation:imgN]`으로 썼다. 섹션별 올바른/잘못된 형식은 S1 3/3, S2 3/1, S3 0/4, S4 0/0, S5 0/0이다. Deep-Reporter 이미지 정규식은 이 형식을 이미지로 세지 않고, Markdown에서도 그림이 보이지 않는다.
- **검토한 방법**: (a) 후처리에서 실제 그림으로 변환 / (b) "Figure k" 텍스트 참조로만 남김 / (c) 제거. 함께 writer 템플릿에 금지 규칙 추가.
- **결정**: 결정 3 = (a). 이미지는 의무화하지 않는다.
- **수정**
  - `domain_templates.py` writer Citation 규칙 4: "Never write [citation:imgN]: an image source is cited ONLY as ![](citation:imgN) on its own line, and [citation:...] is used ONLY for txt sources."
  - `grounding_postprocessor.py`: 잘못된 형식은 문장 안에서 `(Figure k)`로 바꾸고, 실제 그림은 그 단락 바로 뒤에 넣는다. 변환 수는 경고로 남긴다.
- **효과**
  - A를 후처리하면 8개가 모두 변환되고 그림 7개가 생긴다(CPU 테스트).
  - B에서는 잘못된 형식이 19개 중 4개(S3 3, 결론 1)로 줄었고, 4개 모두 그림으로 변환됐다. `[?]`·누락 프레임 0.
- **남은 한계**: 규칙 4만으로는 완전히 막지 못한다. 후처리 변환이 계속 필요하다.

### P2. 이미지를 넣지 않은 섹션 — ✅ 정책 결정
- **현상 (A)**: S4와 S5는 이미지 근거가 3개씩 있었는데도 하나도 넣지 않았다.
- **결정 3**: 섹션마다 이미지를 강제하지 않는다. 이미지 검색 정확도가 검증되지 않은 상태에서 강제하면 관련 없는 프레임이 들어갈 위험이 있기 때문이다.
- **B (실측)**: 결론을 뺀 5개 섹션이 모두 이미지 3장씩을 인용했다(중복 삽입 4개는 한 번만 넣어 그림 14개). 템플릿의 이미지 관련 변경은 규칙 4뿐이라 **이 변화의 원인은 확인할 수 없다**(샘플링 편차일 가능성 포함).
- **남은 한계**: 이미지가 늘었지만 텍스트 근거와 시간이 크게 떨어진 프레임도 인용됐다(P14).

### P3. 인용이 붙었지만 근거에 없는 수치·문구 — 🟡 감지만
- **현상 (A, 대조)**: S2 `"SCORE 10"`, S4 `0/1`·`3/16`, S5 `WOO`. 인용 번호는 유효했지만 그 섹션의 어떤 근거에도 없었다.
- **정정 이력**: 처음에는 "텍스트 인용 109개가 모두 범위 안"이라고 보고했다. 이는 인용 **번호**가 유효하다는 뜻이었지, 문장이 근거로 뒷받침된다는 뜻이 아니었다. 근거 원문과 대조해 이 문제를 찾았다.
- **검토한 방법** (결정 2)

  | 안 | LLM 추가 호출 | 잡는 것 | 놓치는 것 |
  |---|---|---|---|
  | 없음 | 0 | — | 전부 |
  | **규칙 기반** | 0 | 근거에 없는 따옴표 문구·숫자·시간 | 의미 수준의 오류 |
  | LLM 검증 | 섹션당 +1 | 일부 의미 오류 | 같은 8B 모델이 검증하므로 신뢰도 한계, 시간 증가 |

- **결정**: 규칙 기반.
- **수정**: `grounding_postprocessor.check_section_grounding()`. 문장의 따옴표 문구, 숫자, HH:MM:SS를 그 문장이 인용한 근거와 대조해 `unsupported` / `miscited` / `uncited`로 분류하고 경고로 남긴다(규칙 상세 `REPORT_PIPELINE.md` ⑥).
  - 첫 구현은 같은 뜻의 다른 표현("score of 5" ↔ "SCORE 5", "8 out of 10" ↔ "8/10")을 오탐했다. 두 규칙을 추가해 해결했다: 같은 근거 안에서 단어가 같은 순서로 가까이 나오면 인정, `a/b`는 `a out of b`도 인정.
  - "단어가 근거 어딘가에 있으면 인정"하는 느슨한 방식은 `SCORE 10`을 놓치기 때문에(근거에 "10"이 다른 맥락으로 있음) 채택하지 않았다.
- **효과**
  - A (대조): unsupported 4 + miscited 5 = 9건 중 실제 오류 7건(정밀도 약 78%). 오탐 2건은 `SCORE 6` ×2(근거: "a score of 5, which then changes to 6").
  - B (규칙 출력): 실행 당시 규칙으로 unsupported 6 / miscited 3 / uncited 14. 그중 `10:85`·`9:51`은 부정문 오탐(P18). 현재 규칙으로는 unsupported 4 / miscited 3 / uncited 12 / absence 3이며, unsupported·miscited 7건은 모두 결론 섹션이다(P11).
- **남은 한계**: 감지만 하고 고치지는 않는다. 의미 수준의 오류는 잡지 못한다. 재현율은 정답 데이터가 없어 측정하지 못했다.

### P4. 다른 근거의 내용·시간을 인용 (miscited) — 🟡 감지만
- **C-4 (2026-10-25, 대조)**: 보고서 1 "After the game, the man in the blue jersey ... 'I like it with the gadget on' [24]" — [24](00:09:00)에서는 검은 후드 남성이 한 말이고 시점도 게임(18:30) 이전이다. 규칙 검사는 잡지 못했다(의미 수준).
- **현상 (A, 대조)**: `1-0`(실제로는 00:31:10 다른 클립의 내용), `00:02:30`(인용한 근거는 00:02:10–20 구간), `00:08:20`(실제 "SCORE 7" 근거는 00:11:10·00:11:30).
- **대응**: P3와 같은 규칙 검사의 `miscited` 경고.
- **B (규칙 출력)**: 3건, 모두 결론 섹션. 예: `"SPORTS DRIBBLE SPECS"`가 인용한 txt3이 아니라 txt2에 있음. 각각을 사람이 대조하지는 않았다.

### P5. planner 섹션 설명의 내용이 본문에 들어감 — ⏳
- **현상 (A, 대조)**: S4의 `0/1`, `3/16`은 그 섹션 근거 어디에도 없고, planner가 10min 영상 개요로 쓴 **섹션 설명에만** 있었다.
- **원인 (코드)**: planner는 영상 개요를 보고 섹션 설명을 쓴다. writer는 섹션 설명과 검색된 근거를 함께 받으므로, 설명에만 있는 사실이 본문으로 넘어갈 수 있다. 또 Deep-Reporter가 다음 섹션에 넘기는 맥락도 섹션 설명 위주다(P9 원인 참고).
- **B (대조)**
  - S3 설명은 "Straight Shooter Strap and Flick Glove"를 다루라고 했지만 **어느 섹션 근거에도 "Flick Glove"가 없었다.** writer는 S3에서 "The “Flick Glove” is not directly described or shown in the retrieved footage, though it is mentioned in the section description"이라고 밝혔다.
  - 그러나 결론 섹션은 "Flick Glove"를 사실처럼 썼다(txt2 인용, unsupported).
  - S2의 `10:85`, `9:51`도 설명에서 온 값이다. A에서는 근거에 있었지만 B에서는 검색되지 않았고, writer는 "보이지 않는다"고 썼다.
- **대응**: 규칙 검사로 수치·문구 유형은 경고한다. C0(결정 4)로 결론 writer가 planner 설명 대신 앞 섹션의 실제 문장을 받게 했다.
- **남은 한계**: C0의 효과는 측정하지 않았다. 일반 섹션의 설명 유입에 대한 템플릿 대응(예: "설명에만 있는 사실은 쓰지 말 것")은 정하지 않았다.

### P6. 다른 장면을 같은 사건으로 엮음 — ⛔
- **현상 (A, 대조)**: S5(Flick Glove)는 규칙 설명(00:08:20)과 벌칙(00:10:40) 사이에 "Flick Glove 슛"으로 00:26:20·00:31:10 클립을 인용했다. 두 클립에는 flick glove 언급이 없고, 00:31:10은 패드로 수비하는 다른 드릴이다. 00:26:20 근거는 "0/1"인데 본문은 "ball goes through the hoop, 1-0"으로 썼다.
- **원인 (가설)**: 같은 사람, 같은 코트가 영상 내내 반복되어 유사도 검색이 다른 챌린지 장면을 가져오고, writer가 이를 하나의 이야기로 엮었다. 10sec 단위만 써서 "규칙 설명 → 결과" 같은 긴 맥락이 한 근거에 담기지 않은 것도 원인일 수 있다.
- **대응**: 없음. 규칙 검사는 숫자·문구가 없으면 잡지 못하고, LLM 검증안은 결정 2에서 채택하지 않았다.
- **다음 단계**: 4개 단위 캐시(결정 1) 이후 다시 확인한다. B는 문장 단위로 대조하지 않아 미확인이다.

### P7. 섹션 주제와 검색 근거 불일치 — ⛔
- **현상 (A, 대조)**: S3은 개요에 있는 "vertical obstacle, 30-second countdown"으로 섹션이 만들어졌지만 검색이 그 장면을 찾지 못했다. writer는 "없다"고 밝혔지만 나머지를 관련 없는 장면(00:02–00:31)으로 채웠다.
- **B (실측)**: "근거에 없다/보이지 않는다" 유형 문장이 S2 3, S3 3, S5 4개다(정규식 집계). 예: S5 "The video does not show any actual gameplay or test involving the “NEVER ENDING DEFENDER” device."
- **대응**: 없음. 근거가 없을 때 없다고 쓰는 것은 템플릿 지시(Grounding 규칙 4)대로다. 근본 원인으로 보이는 검색 범위(10sec만)는 결정 1 이후 다시 측정한다.

### P8. 시간 순서 섞임 — ⛔ (2026-10-26 측정)
- **현황 측정 (2026-10-26, `DESIGN_AND_STATUS.md` §9.17)**: 섹션마다 인용 근거 시점(구간 중앙값)으로 본 섹션 순서 역전 3/20건(모두 실제 역전 확인. 2건은 "Final …" 제목 섹션이 18–19분 내용), 섹션 안 "At HH:MM:SS" 서술이 1.3–11.7분 뒤로 가는 경우 14건(본문). 원인(코드 구조): planner가 섹션을 주제로 나누고 섹션마다 따로 검색하므로 근거 시간대가 섞인다.
- **C-4 (2026-10-25)**: 보고서 1에서 섹션 4(20–31분) 뒤에 섹션 5(18:30)가 와 순서가 뒤집혔다.
- **현상 (A)**: S3과 S5의 근거 시간이 00:02–00:31에 흩어져 있고, 본문도 시간을 오갔다. 템플릿에는 "시간순으로 서술" 규칙(Grounding 규칙 5)이 이미 있다.
- **대응**: 없음. B는 측정하지 않았다.

### P9. 반복 — 🟡 (writer 반복 루프: 2026-10-25 상한·제거·경고 적용)
- **C-5 (2026-10-25, `DESIGN_AND_STATUS.md` §9.14)**: 8건 중 2건(둘 다 C0 `written`)에서 writer가 같은 문장 묶음을 8,192토큰까지 되풀이했다(약 75회·25회 반복, 각 약 6분). 루프 출력이 보고서에 그대로 들어갔고 `validation.json`은 `passed`였다. 규칙 6(writer 프롬프트의 반복 금지)은 이런 생성 루프를 막지 못했다. `analysis/analyze_report.py`의 단락 유사도는 한 단락 안의 루프를 잡지 못한다(완전 중복 문장 295개, 0.5 이상 쌍 0). C0와의 관계는 표본(4 대 4)이 작아 판단할 수 없다.
  - 참고 자료(비교에는 미사용): C-4의 C0 켬 3건, C-5 첫 시도에서 완료된 4건(켬 3, 끔 1)에는 8,192토큰 도달이 0건이었다. 지금까지 C0 켬 보고서 10건 중 2건, 끔 5건 중 0건에서 루프가 났다.
- **현상 (A, 실측)**: S5의 마지막 두 단락이 거의 같은 내용을 반복했다.
  - 측정값이 두 가지다. 처음 보고한 0.711은 인용 표기를 포함한 원문 단락의 SequenceMatcher 값이고, `analysis/analyze_report.py`로 인용·이미지 표기와 제목 줄을 빼고 정규화하면 같은 쌍이 0.901이다.
  - 나머지 66개 단락 쌍은 0.118 이하였고, S5의 반복 8-gram 비율은 0.281(다른 섹션 0.011 이하)이었다.
  - 섹션 간 유사 문장 5쌍 중 4쌍은 S4↔S5의 마무리 상투 문장("… concludes …, and the group remains on the court …")이었다.
- **원인 분석 (코드·실측)**
  - 16회 호출 모두 `finish=stop`, 최대 출력 1,121토큰이라 잘림 때문은 아니다.
  - 생성은 샘플링이고 반복 억제 설정이 없다(repetition_penalty 1.0).
  - Deep-Reporter가 다음 섹션에 넘기는 맥락(`_update_context`)은 LLM 요약이 아니라 섹션 설명 + 본문 앞 100자(대부분 제목 줄) + 직전 섹션 마지막 3문장이다. writer는 앞 섹션에서 실제로 쓴 사실을 거의 모른다.
  - Deep-Reporter에는 생성 뒤 보고서 전체를 다듬는 refine/polishing 단계가 **없다**(코드·논문 확인).
- **검토한 방법** (상세 `ANALYSIS_D4_D7.md` §1.4)

  | 방법 | 판단 | 이유 |
  |---|---|---|
  | 감지 경고 | 측정 도구로 사용 | 출력 불변 |
  | **writer 규칙 (B안)** | **채택** | LLM 호출 증가 없음 |
  | **C0: 앞 섹션의 실제 문장 전달** | **채택** | B안이 섹션 간 반복에 작동하려면 필요. LLM 호출 증가 없음 |
  | 보고서 전체 LLM 재작성(R1) | 비권장 | 섹션별 근거 번호 체계와 규칙 근거 검사의 검증 고리가 끊김 |
  | "삭제만" refine(R2), 규칙 기반 근접 중복 제거(R3) | 후보 | B+C0 효과를 측정한 뒤 판단 |
  | `repetition_penalty` | 비권장 | HF 구현이 프롬프트 토큰까지 벌점을 줘서 근거의 이름·인용·시간 복사를 억제할 위험 |
  | `no_repeat_ngram_size` | 부적합 | 프롬프트를 포함한 n-gram을 금지 |
  | presence/frequency penalty | 불가 | transformers `generate`에 없음 |
  | 앞 섹션 요약을 LLM으로 생성 | 보류 | 섹션당 LLM +1회 |

- **결정**: 결정 4 = B안 + C0.
- **수정**
  - writer Grounding 규칙 6: "Do not repeat a fact, sentence, or paragraph you have already written in this section. If a fact was already covered in a previous section (see "Context from Previous Sections"), mention it in at most one short sentence and focus on what is new in this section. Exception: a conclusion section … restates earlier results briefly by design." 규칙이 빠지면 계약 검사가 실행 전에 막는다.
  - C0 `apply_written_context()`: Deep-Reporter `_update_context`를 실행 중에만 교체해, 앞 섹션의 제목과 단락 첫 문장(인용 번호 제거, 시간 유지, 전체 3,600자 상한)을 writer와 query 생성에 넘긴다. `report.previous_sections_context: written`(기본) / `deep_reporter`(원래 동작).
- **효과**
  - CPU 검증: 규칙 존재·누락 거부, 요약 형식, 교체·복원, Deep-Reporter 그래프에서 writer 2가 섹션 1의 실제 문장을 인용 없이 받는 것, LLM 호출 수 불변을 확인했다.
  - B(규칙 6·C0 **적용 전**)의 반복 지표는 섹션 안 최대 0.235, 0.5 이상 쌍 0개, 섹션 간 유사 문장 3쌍(모두 배경 묘사)이었다. **이 개선은 수정 효과가 아니다.** 샘플링 편차와 짧아진 writer 출력(A 614–1,121, B 374–794토큰)이 겹친 결과로 보인다(가설).
- **남은 한계**: 실제 모델 효과와 프롬프트 증가에 따른 지연(요약 최대 약 900토큰, 추정)을 측정하지 않았다. 측정 계획은 `ANALYSIS_D4_D7.md` §1.6에 있다.

- **2026-10-25 대응 (결정 16, `DESIGN_AND_STATUS.md` §8.12)**: (a) 서버가 요청 `max_tokens`를 3,072로 제한(`config.yaml` `max_tokens_cap`), (c) 후처리 전에 섹션 안에서 같은 문장의 두 번째 이후를 제거, (d) 제거·문장 중간 끝을 `validation.json` 경고로 표시. 상태(`passed`)는 바꾸지 않는다.
- **확인 (§9.16, 9건)**: 루프 2/9건(둘 다 `0RxMZBLeqRI` 섹션 5)이 130.5·133.9초에 끊김(수정 전 약 6분), 문장 37·39개 제거, "문장 중간 끝" 경고. 남은 한계: 끊긴 섹션은 문장 중간에서 끝나고 나머지 내용이 없다. 완전히 같지 않은 반복은 지워지지 않는다. "loop suspected"(최대 반복 ≥ 3) 경고가 3–4회 일반 반복에도 붙었다(3건). 루프 발생 자체는 줄지 않았다(수정 전 C0 켬 2/10, 후 2/9).
- **경고 기준 변경 (2026-10-26, §8.13)**: "loop suspected"는 같은 문장 5회 이상 반복 또는 문장 중간 끝(상한에 걸려 끊김)일 때만 붙는다. 반복 문장 제거 경고는 그대로 남는다. 위 9건의 validation.json `repetition`에 새 기준을 적용하면 경고 보고서가 5건에서 루프 2건(`0RxMZBLeqRI` r1·r2)으로 준다.

### P10. 결론 부재와 query 일부만 다룸 — ✅
- **현상 (A)**: 마지막 섹션이 개별 챌린지(Flick Glove)라서 "how the tests turn out"을 종합하는 부분이 없었다. 영상의 가젯 12개 중 일부만 다뤘다.
- **검토한 방법**: 결론 섹션 강제(섹션 1개만큼 시간 증가, 영상 전체에 흩어진 근거는 검색이 약함), 섹션 수 상한 조정(늘리면 더 많이 다루지만 시간과 중복 위험 증가).
- **결정**: 결정 5 = 가벼운 결론 섹션 강제 + 섹션 수 상한 **6**(사용자 확정).
- **수정**
  - planner 규칙 6: 마지막 섹션은 짧은 결론이고, 설명은 정확히 `Conclusion:`으로 시작하며, checklist는 2–3개다. 출력 예시에도 결론 섹션을 넣었다.
  - writer: `Conclusion:` 섹션은 100–250단어로 앞 결과만 종합한다.
  - `run_report.py` 경고: 상한 초과, 마지막 섹션이 결론이 아님, 중간 섹션에 `Conclusion:`, 결론 300단어 초과.
  - 상한 허용 범위 3–15(I17).
- **효과 (B, 실측)**: 6개 섹션, 마지막 설명이 `Conclusion:`으로 시작, 본문 244단어(지시 범위 안). 결론 관련 경고 0.
- **남은 한계**: 결론 섹션에서 인용 불일치(P11)가 새로 나타났다.

### P11. 결론 섹션의 인용 불일치 — ⏳
- **현상 (B, 규칙 출력)**: 근거 검사의 unsupported·miscited 7건이 모두 결론 섹션에서 나왔다.
- **대조 결과**: 결론이 언급한 "SKLZ Dribble Stick", "Straight Shooter Strap", "Shot Coach"는 결론 섹션 근거에는 없고 앞 섹션들의 근거에만 있다. "Flick Glove"는 어느 섹션 근거에도 없다(P5).
- **원인 (코드·실측)**
  - Deep-Reporter는 결론 섹션도 자기 검색어로 근거(text 12건 + 이미지 3건)를 새로 검색하고, writer는 그 근거로만 인용 번호를 붙일 수 있다.
  - B를 다시 계산해 보니 결론 writer가 받은 앞 섹션 맥락(2,212자)은 섹션 1–2는 설명만, 섹션 3–5는 설명 + 제목 줄 정도였다. 실제 본문의 사실은 거의 받지 못했다.
  - 그래서 planner 설명에 있던 이름을 결론 자신의 근거에 붙이게 된다.
- **대응**: C0로 결론 writer가 앞 섹션의 실제 문장을 받게 했다(인용 번호는 지움).
- **남은 한계**: 결론의 근거 목록에는 여전히 앞 섹션 근거가 없으므로, 인용 불일치가 얼마나 줄어들지는 측정해 봐야 한다. 남으면 결론 섹션의 인용 방식(예: 앞 섹션 참조)을 별도로 검토한다.

### P12. 근거 없는 추측 표현 — ⛔
- **현상 (B, 실측)**: writer Grounding 규칙 1(근거가 말하지 않는 추측 금지)이 있지만 "implies / likely / suggests / appears to / presumably / probably"가 들어간 문장이 5개 있었다(정규식 집계: S2 2, S4 1, S5 2).
  - 예: S5 "the context implies it is a defensive training tool, likely involving shot-blocking or reaction drills"
  - 예: S4 "as inferred from the context … likely to improve accuracy"
- A는 같은 방식으로 측정하지 않았다.
- **현황 측정 (2026-10-26, `DESIGN_AND_STATUS.md` §9.17, 보고서 20건)**: 추정·해석·평가 단서(possibly·suggesting·symbolizing·underscoring·reinforcing 등)가 수정 후 9건에서 434개(추정 24, 해석 151, 평가 259). 270개(62%)는 같은 어간이 인용 근거에 있고(옮김), 94개는 없고(writer가 추가), 70개는 인용이 없는 문장. "추가" 표본 12개를 근거와 대조하니 8개가 근거에 없는 해석·평가였다(예: "representing joy, freedom, or resistance", "visually reinforcing forced displacement").
- **원인 (자료·코드 확인)**: 검색되는 30sec·3min·10min 요약 캡션 자체에 해석 표현이 거의 다 들어 있다(3min 28/29, 10min 12/12, 30sec 81/98, 10sec 13/82). WorldMM 전처리 요약 프롬프트는 "Do not make assumptions or add interpretations"를 지시하지만(`gen_multiscale.py`), Qwen3-VL-8B가 지키지 않았다. writer는 그 표현을 옮기고 일부는 더한다.
- **대응**: 없음. 선택지(사용자 결정): 단서 표현 검출 경고, 다단위 요약 캡션의 해석 표현을 걸러낸 근거 제공, writer 규칙 강화.

### P13. semantic 근거의 가치가 낮음 — ⏳ (결정 7 보류)
- **현상 (실측)**
  - A: 20개 중 11개 인용. 사소하거나 중복된 triple이 많았다. 예: `(player, can dribble, basketball)`(S1·S3 중복), `(Flick Gloves, has colors, black/orange/white)` 3개.
  - B: 24개 중 6개만 인용. 예: `(basketball court, is played on, basketball court)`. 쓸모 있는 규칙 정보 `(challenge, penalizes least baskets with, 100 sit-ups)`도 있다.
- **결정**: 결정 7 보류. 10sec만 쓴 조건이라 4개 단위 캐시(결정 1) 이후 다시 측정한다. 선택지(k 축소, 사소한 술어 필터 등)와 한계는 `ANALYSIS_D4_D7.md` §2에 있다.

### P14. 이미지와 텍스트 근거의 시간 차이 — 🟡 기록만
- **C-4 (2026-10-25)**: 인용 이미지와 같은 단락 텍스트 근거의 시간 차 중앙값 665초(보고서 1, 최대 1,245초), 0초(보고서 2), 5초(보고서 3).
- **현상 (실측)**: 이미지 검색(VLM2Vec)은 섹션의 이미지 질의로 독립적으로 이루어져서 텍스트 근거의 시간대와 묶여 있지 않다(코드).
  - A: S4 이미지 3장은 그 섹션의 인용된 episodic 구간과 785–1,415초 떨어져 있었고, 하나도 인용되지 않았다.
  - B: 이미지 18장 중 16장이 인용됐지만, 인용된 이미지도 텍스트 근거와 최대 1,015초(S4 00:01:25) 떨어져 있었다.
  - **그림이 해당 문장의 장면과 실제로 맞는지는 사람이 확인하지 않았다.**
- **대응 (사용자 지시)**: 이미지마다 인용된 텍스트 근거와의 시간 차이를 `validation.json`에 기록한다(`image_time_alignment`). 같은 단락 기준과 섹션 전체 기준 두 가지이며, 경고는 내지 않는다.
- **검증**: 합성 사례(구간 안 0초, 직전 단락 기준 190초)와 보고서 B 인용 이미지 16개(섹션 기준 값이 분석 스크립트와 일치)로 확인했다.
- **남은 한계**: 출력을 바꾸는 대응(이미지를 텍스트 근거 구간 근처로 제한 등)은 결정 7 보류다.

### P15. 한국어 번역 품질 — ⏳ (제목 형식 ⛔)
- **배경**: 결정 6에 따라 영어 보고서를 정본으로 두고 섹션 단위로 번역한 `report_ko.md`를 추가한다. 인용·시간·`(Figure k)`·따옴표 문구는 `[[Pn]]` 자리표시로 보호하고, 그림 블록은 번역하지 않는다. 자리표시와 제목 수를 검사하고, 실패하면 1회 재시도 후 영어 원문을 유지한다.
- **B 결과 (실측)**
  - 6개 섹션 모두 첫 시도에 성공(재시도 0, 원문 유지 0). 섹션당 자리표시 17–30개.
  - 영어와 한국어의 `[n]` 수 72 = 72, HH:MM:SS 수 73 = 73.
  - 번역 시간 231.8초(6회, 섹션당 23.5–49.2초). 보고서 전체 494.4초 중 47%.
- **품질 문제 (대조)**
  - 한자 혼입: 결론 "햇**明媚**한", "미**歇尔**".
  - 이름 표기 불일치: "제이mes", 섹션 1 "재치" ↔ 결론 "자크", 섹션 1 "크리스·캐스·미첼"(한글) ↔ 일부 "Chris"(영문). 프롬프트의 "고유명사 원문 유지" 지시가 지켜지지 않았다.
  - 제목 형식 불일치: "섹션 1:", "2부:", 번호 없음.
- **대응 (사용자 지시)**
  - **한자·가나 감지**: 자리표시를 뺀 번역 출력에서 한자·가나를 찾으면 1회 재시도한다. 남으면 처음의 유효한 번역을 유지하고 `foreign_script`로 기록하며 경고한다. 보호된 따옴표 안의 한자는 검사하지 않는다.
  - **고유명사 보호**: 보고서 본문에서 문장 중간에 대문자로 나온 단어 묶음을 모아 자리표시로 보호한다. 보고서 B에서는 Chris, Zach, Cass, James, Mitchell, SKLZ, SKLZ Dribble Stick, Shot Coach 8개가 수집된다.
- **검증 (CPU)**: 한자가 있으면 재시도해 깨끗한 출력 사용, 계속 남으면 기록, 이름이 번역 후에도 원문 그대로, `run_report` 전체 흐름에서 경고.
- **남은 한계**
  - NER이 없어 사람과 제품·브랜드 이름을 구분하지 않는다(둘 다 영어로 남음). 문장 첫머리에만 나오는 이름은 수집되지 않는다.
  - 제목 형식 불일치는 대응하지 않았다.
  - 실제 모델 효과와, 늘어난 자리표시가 번역 실패율에 주는 영향은 측정하지 않았다. B의 `report_ko.md`는 이 보완 **이전**에 번역된 것이다.
- **실제 실행 (2026-10-25 C-4, `DESIGN_AND_STATUS.md` §9.13)**: 보완 후 처음 실행. 17개 섹션 중 **5개가 자리표시자 불일치로 실패**해 영어로 남았다(영상 2: 3/5 실패, 영상 3: 2/6 실패, 영상 1: 0/6). 재시도 후에도 한자·가나가 남은 섹션 3개(`龙`, `ロー`, `ル`). 자리표시자 수만으로는 설명되지 않고(성공 최대 78개, 실패 최소 29개), 실패는 고유명사가 많은 영상(보호 이름 9–32개)에서만 났다. 원인 미확정. B(보완 전)는 6/6 성공이었다.

### P16. 인용을 검증할 수 없는 출력 — ✅
- **현상 (A)**: Deep-Reporter 결과에는 섹션별 `[citation:txt3]`만 남고 실제 시간·프레임·출처가 없었다.
- **수정**: 후처리기가 보고서 전체 번호 `[n]`, References(episodic은 시간 구간, semantic은 "no timestamp"), 그림(프레임 복사 + 캡션)으로 바꾼다. 범위 밖이나 해석할 수 없는 인용은 `[?]`로 표시하고 오류로 처리한다.
- **효과 (실측)**: A 후처리 시 인용 109개 → 참조 46개, 남은 placeholder 0. B는 인용 72개 → 참조 35개, 그림 14개, `[?]` 0, 누락 프레임 0.

### P17. 조용한 실패 — ✅ (보고서에서는 미발생)
- **확인한 경로 (코드·실측)**
  - planner JSON 파싱 실패 → 섹션 1개로 대체(설명 = query)
  - query 파싱 실패 → 섹션 설명을 그대로 검색어로 사용
  - LLM 오류 → 본문에 `Call failed:` 또는 `[Section generation failed`
  - 검색 실패·시간 초과 → 근거 0건으로 계속 진행
  - 섹션 16개 이상 → 보고서 전체 소실(I17)
  - 앞의 네 경우는 `success=True`로 끝날 수 있다.
- **수정 (`run_report.py`)**
  - 사전 확인 실패(LLM·검색 서비스 health, 캐시 불완전 409, 템플릿 계약, 설정 범위) → exit 2
  - 사후 검증 오류(planner 대체, 실패 문자열, 빈 근거, `[?]`, 프레임 누락) → exit 1
  - query 대체 → 경고
- **효과**: CPU 테스트에서 각 실패를 만들어 감지되는 것을 확인했다. 실제 실행 A·B에서는 발생하지 않았다.

### P18. 규칙 검사가 부정문 속 토큰을 오류로 잡음 — ✅ (한계 있음)
- **현상 (B, 대조)**: S2 "no specific time stamps such as “10:85” or “9:51” are visible or mentioned in the retrieved footage"에서 `10:85`, `9:51`이 unsupported로 잡혔다. 근거에 없다고 말하는 문장이므로 오탐이다.
- **수정 (사용자 지시)**: "근거가 X를 보여주지 않는다"는 절을 찾아, 그 절 **안에만** 나오는 토큰은 검사하지 않고 `absence`로 기록한다.
  - 조건: 부정어(not/no/never/n't 등) 뒤 12단어 안에 show/visible/mention/state/specify 같은 동사, 그리고 문장 안에 footage/evidence/retrieved/video/clip/frame/source.
  - 절 범위: 부정어부터 다음 절 경계(`;`, `, but/though/while/which/and…`, 문장 끝)까지.
- **첫 구현의 문제와 수정**: 처음에는 조건에 맞는 문장 **전체**를 제외했다. 보고서 A에 돌려 보니 "his score improves to 3/16, though the exact time … is not specified in the evidence"처럼 사실 주장과 부정 절이 섞인 문장에서 실제 오류 `3/16`, `WOO`를 놓쳤다. 그래서 절 단위 제외로 고쳤다.
- **효과 (CPU, 실제 보고서 입력)**
  - A: 기존 unsupported·miscited 9건이 모두 그대로 검출된다. uncited 1건("The evidence does not show … from 0/1 to 3/16")만 absence로 바뀌었는데, 이 두 값은 같은 섹션의 다른 문장에서 unsupported로 여전히 검출된다.
  - B: `10:85`·`9:51`이 absence로 바뀌었고, 결론 섹션 지적은 그대로다.
  - 근거 명사가 없는 부정 사건("He did not make the shot, as shown on the scoreboard reading 0/1")과 부정 절 앞의 토큰은 계속 검사한다.
- **남은 한계**: 부정 절 안에 틀린 값이 전제로 들어간 경우(예: "the evidence does not confirm the progression from 0/1 to 3/16")는 검사에서 빠진다. 절 경계 판정은 규칙 기반이다.

---

### P19. 구간 요약의 종료·시작 표현이 영상 전체 서술로 옮겨짐 — 🟡 (2026-10-25 신규, 같은 날 규칙·검사 적용)
- **현상 (C-4 보고서 1, 대조)**: 섹션 5와 결론이 "The video closes with ... (00:18:29) ... close-up of the Shot Coach device [22]", "The video's climax occurs at 00:18:30"이라고 썼다. [22]는 18:00–21:00 3min 캡션이고, 그 캡션이 자기 구간을 "The video closes with a close-up of the Shot Coach device"라고 요약했다. 실제 영상은 37:37까지이며 엔드 스크린("Thank you for watching")으로 끝난다(10sec 캡션 `00373000`). 인용은 근거 문구와 일치하므로 규칙 검사로는 잡히지 않는다.
- **원인 (자료 확인)**: 30sec·3min·10min 캡션은 전처리에서 구간마다 따로 요약돼(`gen_multiscale`) 구간의 끝을 "the video closes/concludes"로 표현하는 경우가 있다. writer는 이 문장을 영상 전체 사실로 받아들였다. 10sec만 쓰던 보고서 A·B에서는 없던 유형이다.
- **관련**: 같은 보고서에서 섹션 순서가 시간과 어긋남(P8), 화자 뒤바뀜(P4 유형, `[24]`), 결론의 참가자 수 불일치("three men" vs 섹션 1 "six men")도 확인됐다.
- **2026-10-25 대응 (결정 16, §8.12)**: (1) writer 템플릿 Grounding Rule 7: 구간 요약의 "the video opens/closes…"는 그 구간의 시작·끝이며, 영상 전체(00:00:00–실제 끝, 10sec 캡션 기준)의 시작·끝은 처음·마지막 몇 분에 닿는 근거로만 서술. (3) `boundary_claims` 검사: 결말·시작 서술 문장의 인용 근거가 영상 끝·처음에서 120초 넘게 떨어지면 경고.
- **확인 (§9.16)**: 같은 검사를 수정 전 보고서에도 적용해 비교했다. `ending_early` 보고서당 수정 전 1.25–2.0, 후 1.22. 결론 섹션 결말 오인 수정 전 7/11, 후 4/9. writer는 규칙 7이 있어도 "The video closes with a close-up of the Shot Coach device"를 옮겼다(→ 규칙만으로는 부족). 결론이 실제 결말과 맞은 예: `-QuCz7kxBr8` r1("ends at 00:37:37 … Thank you for watching"). 검사 오탐 1건("final shot of the video’s opening montage").
- **추가 대응 (2026-10-26, `DESIGN_AND_STATUS.md` §8.13)**: writer 템플릿에 영상 마지막 약 60초의 10sec 캡션을 근거 txt0으로 보여 주고, 마지막 섹션만 결말 서술에 인용하게 했다. 인용되면 후처리가 그 섹션 근거 목록에 붙이고 번호를 바꾼다. 결말 검사의 소유격 오탐("final shot of the video’s opening montage")을 고쳤다. CPU 테스트만 했고 GPU 확인 전이다.
- **처음에 적었던 검토 방법(일부 적용됨)**: writer·결론 프롬프트에 "근거는 구간 요약이며 'the video closes'는 그 구간의 끝"이라는 규칙 추가, 결론 섹션에 영상 마지막 구간 근거를 넣기, 규칙 검사에서 결말 표현의 시각과 영상 길이 비교.

## 3. 파이프라인·개발 과정 문제 상세

### I1. 실행 환경 오인 — ✅
- **현상**: 처음에는 `WorldMM/.venv`를 실행 환경으로 보고 flask를 설치했다.
- **확인 (실측)**: 컨테이너의 `PATH`, `VIRTUAL_ENV`, `UV_PROJECT_ENVIRONMENT`가 모두 `/opt/venv`를 가리키고, worldmm·hipporag·merit editable 설치와 Deep-Reporter 의존성이 모두 `/opt/venv`에 있다.
- **조치**: 모든 스크립트를 `/opt/venv/bin/python`으로 실행한다. `WorldMM/.venv`의 flask는 해롭지 않아 사용자 지시로 유지했다.

### I2. `WorldMM/.venv` 경로 깨짐 — ✅
- **현상**: 디렉터리 이름이 `VAU_RAG`에서 `VideoRAG`로 바뀐 뒤 `.venv`의 activate, shebang, editable 경로가 옛 경로를 가리켰다.
- **조치**: 텍스트 파일 76개의 경로를 치환하고(백업 `backups/`), `UV_PROJECT_ENVIRONMENT=$PWD/.venv uv sync --frozen --inexact`로 확인했다.
- **결과**: `import worldmm, hipporag, decord, WorldMemory, HippoRAG` 성공, `/opt/venv` 변화 없음. `.pyc` 4,734개의 옛 경로는 동작에 영향이 없어 남겼다(`DESIGN_AND_STATUS.md` §10).

### I3. 대상 지정 없는 `uv sync`의 위험 — ✅ 규칙화
- **확인 (dry-run)**: 대상이 `/opt/venv`가 되고, exact 모드라 langgraph·langchain·flask·merit 등 20여 개를 삭제하고 openai를 2.54에서 2.29로 내린다.
- **조치**: 반드시 `UV_PROJECT_ENVIRONMENT`로 대상을 지정하고 `--frozen --inexact`를 붙인다는 규칙을 인수인계에 넣었다.

### I4. `HF_HOME` 경로에 모델 없음 — 🟡 정정 (2026-10-25)
- **현상 (2026-10-21 15:36 확인)**: 환경변수 `HF_HOME`(`/data1/jyheo/workspace/VideoRAG/.cache/huggingface`)이 가리키는 곳에는 모델이 없고, 실제 모델은 `/data1/jyheo/workspace/.cache/huggingface/hub`에 있었다.
- **처음 조치**: `config.yaml`의 `paths.hf_home`을 스크립트가 torch·transformers import 전에 `HF_HOME`에 설정한다(`local_llm_server.py`, `videorag_retriever_service.py`, `prebuild_episodic_index.py`, 테스트들).
- **정정 (2026-10-25, 실측·코드)**
  - 컨테이너에는 `HF_HOME` 외에 **`HUGGINGFACE_HUB_CACHE=/data1/jyheo/workspace/VideoRAG/.cache/huggingface/hub`**도 설정돼 있다(`Deep-Report/Docker/Makefile` `docker-run`의 `-e`). `huggingface_hub` 0.36.2는 모델 위치를 `HF_HUB_CACHE` → `HUGGINGFACE_HUB_CACHE` → `$HF_HOME/hub` 순서로 정한다(`huggingface_hub/constants.py:129-155`).
  - 그래서 처음 조치는 **모델 위치를 바꾸지 못한다.** 실험: `import torch` 뒤 `HF_HOME`을 `paths.hf_home`으로 바꾸고 `huggingface_hub.constants`를 처음 import해도 `HF_HUB_CACHE`는 `VideoRAG/.cache/huggingface/hub`였다.
  - 2026-10-21 16:24–16:31 GPU 스모크(`DESIGN_AND_STATUS.md` §9.2)와 LLM 서버가 모델 4개를 그 위치에 내려받았다(근거: `.locks/` 생성 16:26–16:31, Qwen3-VL-8B blob 16:28:41–16:31:14, 첫 Qwen3-Embedding 로드 90초 → 두 번째 15초). 그 뒤 모든 실제 모델 실행은 이 위치의 모델을 썼다. 두 위치의 모델은 snapshot 해시·바이트 수가 같아 결과에는 영향이 없다.
  - `local_llm_server.py`의 로그 `Loading ... (HF_HOME=...)`는 설정값을 출력할 뿐 실제 위치가 아니다.
- **남은 일**: 코드는 그대로 둔다(동작에 문제없음). 환경을 옮길 때는 모델을 `HUGGINGFACE_HUB_CACHE`(없으면 `$HF_HOME/hub`)가 가리키는 위치에 둔다(`MIGRATION_HANDOFF.md` §4.3).

### I5. 셸 `grep` 래퍼 — ✅ 규칙화
- **현상**: 셸의 `grep`은 ignore 파일을 따르는 래퍼라 `.venv` 내부(`.gitignore=*`) 같은 경로를 건너뛴다. `.venv` 경로 수리(I2)처럼 venv 안을 전수 검사할 때 결과가 빠질 수 있다.
- **조치**: 전수 검색에는 `/usr/bin/grep`을 쓴다.

### I6. Deep-Reporter 설정 dict가 키·URL을 버림 — ✅
- **현상 (실측)**: `BaseConfig.from_dict`는 `hasattr(cls, k)`로 키를 거르는데, `default_factory` 필드는 클래스 속성이 아니라서 `openai_api_key`, `qwen_base_url` 등이 버려진다. 기존 설계안의 "`openai_base_url`만 바꾸면 로컬 전환"은 `Missing credentials` 오류로 실패했다.
- **조치**: `run_report.py`가 `create_openai_api()` 전에 환경변수(`QWEN_BASE_URL`/`QWEN_API_KEY` 또는 `OPENAI_API_KEY`)를 설정하고, 실제로 라우팅된 base URL이 기대값과 같은지 확인한다(다르면 exit 2).

### I7. Deep-Reporter import 함정 — ✅
- **현상 (실측)**: `deep_reporter.nodes`를 먼저 import하면 순환 import로 실패한다. `import deep_reporter.nodes.section_writing_node as sw`는 같은 이름의 함수가 잡힌다.
- **조치**: `deep_reporter.api`를 먼저 import한다. 템플릿·함수 교체 대상은 그래프에 등록된 함수 객체의 `__globals__`에서 찾는다. 모듈이 필요하면 `sys.modules[...]`로 접근한다(테스트에도 적용).

### I8. Deep-Reporter 프롬프트의 웹 리포트 전제 — ✅
- **현상 (코드)**: 원래 image query 지시가 "diagrams, charts…"이고, writer에는 타임스탬프나 관찰 사실 위주 서술 지시가 없다.
- **조치**: `domain_templates.py`의 videomme 템플릿을 실행 중에만 적용한다. 실행 전에 placeholder(AST로 노드 코드에서 동적 추출), 필수 마커, `.format()` 시험 실행을 검사하고, 실패하면 웹 템플릿으로 몰래 돌아가지 않고 중단한다.

### I9. HippoRAG 캐시 라벨 — ✅
- **현상 (코드·실물)**: `EpisodicMemory._get_or_create_hipporag`가 `global_config`를 넘기지 않아 HippoRAG `llm_name`이 기본값 `gpt-5-mini`로 남는다. 실제 모델과 다른 이름으로 캐시가 저장된다.
- **조치**: `LabeledEpisodicMemory`가 `BaseConfig(llm_name=<실제 모델>)`을 넘긴다. 사전 인덱싱과 검색 서비스가 같은 클래스를 쓴다.

### I10. HippoRAG OpenIE의 오류 삼킴 — 🟡
- **현상 (코드)**: OpenIE는 재시도가 소진되면 예외를 삼키고 빈 결과를 반환하며, 그 결과도 캐시에 저장된다. 전처리 결과에도 빈 triple 1,252개가 있다.
- **조치**
  - 검색 서비스는 로드 전에 granularity마다 캐시가 완전한지 검사하고, 불완전하면 409로 거부한다(서비스가 몰래 OpenIE를 돌리거나 오염된 캐시를 쓰지 않음).
  - 사전 인덱싱 시드에서 빈 triple은 빼고 다시 계산하게 한다.
- **남은 한계 (실측)**: 시험 인덱싱 10sec에서 재계산 18개 중 2개가 재시도 소진으로 빈 결과가 됐다. 완료 판정은 캐시 키 존재만 보므로 이런 청크도 "완료"로 간주된다. 필요하면 빈 triple 비율을 별도로 기록한다.
- **갱신 (2026-10-22)**: 잘린 응답 구제(I23)로 재시도 소진이 줄어들 것으로 예상한다(미측정). 완료 표식에 단위별 빈 triple·빈 entity 수(`cache_empty`)를 기록한다.

### I11. WorldMM episodic 검색 비용 — ✅
- **현상 (코드)**: 쿼리마다 granularity 4개 × DSPy fact 필터 1회 + multiscale 필터 1회 = 최대 5회. 섹션당 쿼리 3–5개면 섹션당 15–25회다.
- **조치**: L1 설계. DSPy 필터를 빼고 그래프 검색 후보를 모은 뒤, 섹션의 검색 요청당 multiscale 필터를 1회만 호출한다. L0(0회)와 full(원본)도 설정으로 선택할 수 있다.

### I12. WorldMM 검색 결과에 점수가 없음 — ✅
- **현상 (코드)**: episodic·semantic `retrieve()`는 점수를 반환하지 않고, visual은 점수를 버린다. 출처별 척도도 다르다.
- **조치**: 순위 기반 병합(RRF, k=60). 응답의 `score`는 `score_type`과 함께 순위에서 유도한 값임을 밝힌다.

### I13. Visual 검색과 프레임 추출 — ✅
- **현상 (코드)**: `visual.retrieve()`는 질의가 `DAY X HH:MM:SS - …` 형태면 시간 범위 검색으로 바뀌어 다른 형식의 결과를 돌려준다. 기존 프레임 함수로 1장만 뽑으면 구간의 시작 프레임이 나온다.
- **조치**: 항상 유사도 검색만 하는 `_retrieve_by_similarity`를 호출하고, decord로 구간 **중앙** 프레임을 JPEG로 추출해 캐시한다. 같은 `start_time`의 10sec 캡션을 정확히 붙인다.

### I14. HippoRAG 그래프 검색의 assert 실패 — ✅
- **현상 (코드)**: `graph_search_with_fact_entities`에 `assert sum(node_weights) > 0`이 있고, 원본 `retrieve()`도 이 예외를 잡지 않는다.
- **조치**: DSPy를 뺀 그래프 검색이 예외로 실패하면 dense passage retrieval로 대체하고 경고 로그를 남긴다.

### I15. full 모드의 근거 부족 — 🟡 (겹침 시 부족 남음)
- **현상 (CPU 테스트)**: full 모드는 쿼리별 결과가 겹치면 병합 후 근거 수가 요청보다 적어졌다.
- **조치**: 쿼리당 개수를 `max(full_top_k_per_query, ceil(n/쿼리 수))`로 올렸다. LLM 호출 수는 그대로다.
- **참고**: 이후 테스트에서도 4건만 나온 것은 가짜 필터가 두 쿼리 모두 같은 10min 캡션 4개를 고르게 만든 탓으로, 서비스 문제가 아님을 확인했다.
- **실제 모델 확인 (2026-10-25 C-3)**: 4개 단위 캐시와 실제 LLM으로 full text 요청 9건의 episodic 근거가 4–8개(평균 6, 설정 8)였다. WorldMM 필터는 쿼리마다 `final_top_k`까지 채우지만 두 쿼리의 결과가 겹치면 병합 후 줄어든다. 조치는 겹침이 없을 때만 8개를 보장하는 부분 해결이다(남은 한계). 기본 모드는 L1이라 영향이 없다.

### I16. L1 필터 실패 표시 — ⛔
- **현상 (코드)**: L1에서 LLM 호출 자체가 실패하면 `meta.episodic_filter="fallback_rrf(llm_failed)"`로 표시한다. 그러나 호출은 성공했는데 응답 형식이 깨져 WorldMM이 RRF 순위로 빈자리를 채운 경우에는 `llm`으로 표시된다.
- **대응**: 문서화만 했다. 필요하면 서비스에서 선택 결과를 직접 파싱해 구분한다.

### I17. Deep-Reporter 섹션 수 한계 — ✅
- **현상**: 그래프 `recursion_limit=50` 때문에 섹션이 많으면 실패한다. 처음에는 계산으로 "16개"라고 적었다.
- **확인 (실측)**: 가짜 LLM으로 실제 그래프를 돌린 결과, 15섹션은 성공하고 16·17섹션은 `Recursion limit of 50 reached` → `success=False`, outline 0개로 **보고서 전체가 사라졌다**. "16개"는 틀렸고 15로 정정했다.
- **조치**: `report.max_sections`는 정수 3–15만 허용하고, 벗어나면 생성 전에 exit 2. planner 템플릿에도 상한을 지시한다.

### I18. 사전 인덱싱의 GPU 메모리 — ✅ 구현 (시험 중지)
- **현상 (실측)**: 기존 스크립트는 Qwen3-VL-8B(약 +17.9GB)와 Qwen3-Embedding-4B(약 +7.7GB)를 한 프로세스에 올려, GPU 1장에서 20GB 규칙을 넘는다.
- **검토**: A(OpenIE를 LLM 서버 HTTP로) / B(GPU가 빌 때 그대로) / C(10sec만 유지).
- **결정**: 결정 1 = A안.
- **수정**: `prebuild_episodic_index.py --llm-endpoints`(HTTP OpenIE, in-process와 같은 메시지·인자·파서·재시도 깊이), `--gpu-mem-cap-mib`, 실행 스크립트 `run_prebuild_http.sh`.
- **효과**: CPU 테스트 통과. 시험 실행에서 GPU 스냅샷 LLM 서버 약 17.4GB ×3, 인덱서 14.3GB로 GPU당 20GB 미만이었다. 10sec 완료 후 30sec 도중 사용자 지시로 중지했다(`DESIGN_AND_STATUS.md` §9.5).
- **갱신 (2026-10-22)**: 20GB 규칙 해제 후 LLM 서버 7개로 3영상 실행 → 영상 1 완료(668초), 영상 2의 10min에서 I23·I24로 중지. 이후 GPU 6·7만 쓰는 조건에서 I27로 중단.

### I19. `-`로 시작하는 영상 id — ✅ 규칙화
- **현상 (실측)**: 보고서 B 첫 시도에서 `--preload -QuCz7kxBr8`을 argparse가 값 없는 옵션으로 해석해 검색 서비스가 exit 2로 끝났다.
- **조치**: `--preload=<id>`, `--video-id=<id>`, `--videos=<id>` 형식으로 넘긴다. 테스트 스크립트를 고쳤고 인수인계 규칙에 넣었다.

### I20. 시험 인덱싱 로그 폴더 — ✅
- **현상**: 시험 인덱싱 첫 실행에서 셸 리디렉션 대상 `logs/`가 아직 없어 즉시 실패했다. 스크립트 안의 `mkdir`보다 셸 리디렉션이 먼저 처리됐기 때문이다. GPU는 쓰지 않았다.
- **조치**: 폴더를 만들고 다시 실행했다.

### I21. 테스트 하네스 문제 — ✅
- Deep-Reporter `search_node`는 LangGraph 실행 맥락이 있어야 동작해서, 한 노드짜리 그래프를 만들어 실행하도록 테스트를 구성했다.
- 결정 5로 planner 문구가 바뀌어, 가짜 LLM의 planner 프롬프트 구분 문구를 `"Design an outline of"`로 바꿨다.
- C0 테스트 작성 중 기대값 오류 1건(가짜 writer의 제목이 "Section"이라 요약이 "Section 1: Section"이 되는 것을 반대로 기대)과 모듈 가림(I7) 문제를 테스트 쪽에서 고쳤다.
- 집계 정정: `test_report_pipeline.py`의 통과 항목은 67개다(처음 "68개"로 보고한 것은 "RESULT" 줄까지 센 값).

### I22. 10min 캡션이 전처리에서 잘림 — ⛔ 보류
- **현상 (실측)**: 영상 50개의 10min 캡션 232개 중 32개(영상 20개)가 정확히 2,048토큰이고, 그중 30개는 마침표 없이 문장 중간에서 끝난다(예: "… This", "… the ominous,"). 30sec 1개, 10sec 2개도 2,048토큰이다. 3min은 최대 1,056토큰으로 잘린 것이 없다.
- **원인 (코드)**: 전처리 `process_one_video.sh:26`이 `worldmm.memory.episodic.multiscale --model qwen3vl-8b`로 30sec/3min/10min 캡션을 만든다. `gen_multiscale._summarize_batch`는 `llm.generate`에 `max_new_tokens`를 넘기지 않으므로 `Qwen3VLModel.generate`의 기본값 2,048이 적용된다. WorldMM의 기본 모델은 gpt-5-mini다.
- **영향 범위 (코드)**: 10min 캡션은 (1) 우리 episodic 10min 인덱스, (2) 보고서 planner 개요(`report.overview_granularity: 10min`), (3) 검색 결과로 나가는 근거 문장에 쓰인다. `build_memory.py`의 episodic·semantic·visual 단계는 10sec 캡션만 읽으므로 전처리 OpenIE, semantic, visual 메모리는 영향이 없다.
- **해결 방법 (검토)**: 기존 3min 캡션을 입력으로 10min 단계만 다시 생성한다. `LLMModel("qwen3vl-8b", max_new_tokens=4096)`처럼 인자만 바꾸는 래퍼로 가능하므로 WorldMM 코드는 고치지 않는다. 이후 10min episodic 캐시를 다시 만들고 보고서를 다시 생성한다.
  - 비용 (추정): 기존 10min 요약은 영상당 평균 260초(144–450초), 50개 합계 13,011초(약 3.6시간, 상한 2,048 기준, 로그 실측). 잘렸던 창은 더 길게 생성되므로 50개 전체 재생성은 프로세스 1개로 약 4–6시간, 잘린 영상 20개만이면 약 1.5–2.5시간. 프로세스당 GPU 약 18–19GB.
- **결정**: 이번 범위에서 제외(사용자 결정, 2026-10-22). 분할 OpenIE(I23)는 잘린 캡션에도 동작하지만, 잘린 뒷부분의 내용은 어떤 방법으로도 복구되지 않는다.
- **검증 영상 3개 해당 여부 (실측, 2026-10-25)**: `prebuild_episodic_index.count_tokens`로 세 영상의 4개 단위 캡션을 모두 쟀다. **`0RxMZBLeqRI`의 10min 4개 중 2개(0–10분, 10–20분)가 2,048토큰이고 각각 "… This", "… the ominous,"로 문장 중간에서 끝난다**(위 예시가 이 두 개다). 나머지 10min 2개는 1,776·379토큰이다. 같은 영상의 10sec(최대 229)·30sec(680)·3min(1,025)과 `-QuCz7kxBr8`(10min 최대 1,733), `54k2g9ddy4M`(10min 최대 1,491)에는 2,048토큰 캡션이 없다. 따라서 `0RxMZBLeqRI` 보고서는 planner 개요와 10min 근거에서 0–20분 구간 요약의 뒷부분이 빠진 상태로 만들어진다. 영상 3개 검증 결과를 해석할 때 이 차이를 분리해서 본다.

### I23. OpenIE 출력 상한 초과와 재시도 폭증 — ✅ 구현, GPU 검증 (2026-10-25)
- **현상 (실측, 2026-10-22 3영상 실행 `outputs/3videos_20261022_120438/`)**
  - 영상 1(`-QuCz7kxBr8`)은 668초에 완료됐다. 영상 2(`0RxMZBLeqRI`)는 10min 단계에서 2,048토큰 상한에 걸린 응답이 연속으로 나와 진행이 멈춘 것처럼 보였고, 사용자 지시로 중지했다(12:36).
  - 단위별 실측 (서버 로그)

    | 단계 | 호출 | 상한 도달 | 프롬프트 최대 |
    |---|---|---|---|
    | 영상 1·2의 10sec·30sec·3min | 333 | 0 | 1,848토큰 (입력 청크 최대 1,025토큰) |
    | 영상 1의 10min | 9 | 1 | 2,323토큰 |
    | 영상 2의 10min | 18 | 12 | 4,070토큰 |
  - 실패 응답은 14건이고 모두 JSON이 중간에 끊긴 형태다. 1건에 90–152초가 걸렸다(다른 요청과 서버를 같이 써서 대기 시간 포함).
- **원인 (코드·실측)**
  1. 10min 청크는 중앙값 1,373토큰, 최대 2,048토큰으로 길다(I22). 출력 길이가 입력 길이에 비례해 2,048토큰 상한을 넘는다.
  2. 넘는 응답은 두 유형이다. **M1 열거 폭주**(I24)와, 반복은 없지만 triple이 87–122개라 길어지는 **M2 정상인데 긴 출력**이다.
  3. `Qwen3VLModel._parse_structured_response`는 잘린 JSON을 통째로 버리고 예외를 던진다. WorldMM `OpenIE`에는 `max_retries` 속성이 없어 데코레이터 기본값 5회가 적용되고(`HippoRAG.py:16,96`, `openie.py`), 우리 HTTP 클라이언트(3회)와 곱해져 **청크당 최대 15회**를 재시도한다. 모두 실패하면 빈 triple이 캐시에 저장된다(I10).
  4. HTTP 방식 때문이 아니다. in-process 경로도 같은 출력 상한(2,048), 같은 샘플링, 같은 파서, 같은 재시도를 쓴다.
- **검토한 방법**
  - 디코딩 설정 변경: 기각(I24 실험).
  - 출력 상한 4,096: M2는 줄지만 M1이 일어나면 시간이 2배다.
  - 잘린 응답 구제만 적용: 재시도는 없어지지만 M2에서 매번 뒷부분 triple을 잃는다. 원인이 아닌 증상만 처리한다.
  - **긴 청크 분할(채택)**: 입력 1,025토큰 이하에서 잘림 0/333이라는 실측에 근거해, 입력을 그 수준으로 줄여 M2를 구조적으로 없앤다. 분할 기준 1,100토큰은 영상 50개 3min 캡션 최대값(1,056)보다 약간 크게 잡은 값이라, 1,026–1,100토큰 구간은 실측 범위 밖이다.
- **수정 (`prebuild_episodic_index.py`, 백업 `backups/prebuild_episodic_index.py.bak_20261022_split`)**
  - 1,100토큰(`SPLIT_MIN_TOKENS`)을 넘는 청크는 빈 줄 문단 단위로 700토큰(`SPLIT_PIECE_TOKENS`) 이하 조각으로 묶는다. 문단이 너무 길면 문장 단위로 나눈다. 토큰 수는 Qwen3-VL 토크나이저(`tokenizers`, torch 없이)로 센다.
  - 조각마다 WorldMM `OpenIE.ner` → `triple_extraction`을 그대로 호출하고, 청크 단위로 합친다(entity 순서 보존 합집합, triple은 `filter_invalid_triples`로 중복 제거). 결과는 기존 시드 방식으로 HippoRAG 캐시에 기록한다(기존 항목 보존). 그래프 구조(청크 1개 = passage 노드 1개)는 그대로다.
  - 안전장치(HTTP 경로): 파싱에 실패하면 완성된 목록 항목 중 형식이 맞는 것만 살리고(NER은 문자열, triple은 문자열 리스트), 하나도 없으면 기존처럼 재시도한다. 살린 NER은 중복 제거 후 최대 100개(`MAX_SALVAGED_ENTITIES`).
  - 완료 표식에 분할 통계(`split`), 단위별 빈 결과 수(`cache_empty`), 구제·절단 누계(`guard_cumulative`)를 기록한다. 완료 판정에 분할 대상 청크도 포함한다.
  - dry-run에 분할 청크·조각 수(`new/split(pc)`)를 표시한다. 영상 50개 기준 분할 청크 149개, 조각 450개, 추가 호출 602회(+4.7%)다.
- **원본과 달라지는 점**: 조각 경계를 넘는 대명사·문맥은 잃을 수 있다(10min 캡션은 "[Event N]" 문단 구조라 영향은 작을 것으로 예상, 미측정). in-process 경로(`--llm-endpoints` 없음)는 분할만 적용되고 구제·절단은 적용되지 않는다.
- **검증**
  - CPU (`tests/test_openie_split_guard.py`, 18개 통과): 실제 10min 캡션 분할(조각 ≤700토큰, 텍스트 손실·순서 변경 없음), **실제 실패 응답 14건 모두 구제**, 비문자열 항목 제거, 캐시 병합, 가짜 서버로 1회 호출 구제, 구제 불가 시 15회 재시도 유지, dry-run 호출 수. 기존 테스트 4종도 통과.
  - GPU: 2026-10-22 14:10 실행은 다른 사용자 메모리 증가로 시작 41초 만에 중단됐다(I27).
  - **GPU 검증 (2026-10-25 C-1, `DESIGN_AND_STATUS.md` §9.10)**: 영상 3개 호출 430회 = 계획(재시도 0), 분할 22조각 실패 0, 파싱 실패 5건 모두 1회에 구제(잘림 3, 스키마 오류 2), `failed_requests` 0. 10/22 영상 2의 10min에서 일어난 재시도 폭증·정체는 다시 나타나지 않았다.
  - **새로 확인한 한계**: 분할 기준(1,100토큰) 아래 입력에서도 잘림이 났다. 영상 1의 분할하지 않은 10min 청크 2건(875·932·965토큰 청크 3개 중 2개, 프롬프트 1,576·1,707토큰)과 영상 3의 분할 조각 1건(프롬프트 1,342토큰)이고, 세 건 모두 끝부분이 같은 주어의 나열이었다(I24 유형). 구제로 앞부분은 살지만 잘린 뒤의 triple은 없다. 10/22의 "입력 1,025토큰 이하 잘림 0건"은 10sec·30sec·3min 333회 기준이었다.
  - **분할 전후 비교 (C-2, §9.11)**: 분할 기준이 있는 영상 1의 10min에서 분할된 청크의 triple이 64 → 160개가 됐다. 다만 같은 입력을 다시 계산해도 triple 집합의 Jaccard가 0.2–0.3이라 차이를 분할 효과만으로 볼 수 없다.
- **캐시 조치 (사용자 승인)**: 영상 1의 10min 폴더와 완료 표식, 영상 2 폴더 전체를 삭제했다. 그래프·임베딩까지 지운 이유는, HippoRAG가 새 청크가 없으면 그래프를 다시 저장하지 않아 OpenIE 파일만 지우면 옛 triple이 그래프에 남기 때문이다(`HippoRAG.index`, 코드). 비교용으로 영상 1의 기존 10min OpenIE 결과와 완료 표식, 영상 2의 10sec·30sec·3min OpenIE 결과(184·62·11청크)를 `backups/cache_before_split_20261022/`에 보관했다(2026-10-25 정정: 처음에 "영상 2의 30sec·3min은 보관되지 않음"이라고 적었으나 파일이 있다). **현재 세 영상 모두 캐시가 미완성이라 검색 서비스가 409로 거부한다.** 남은 계산은 영상 1 12회, 영상 2 178회, 영상 3 240회(합계 430회)다.

### I24. OpenIE 열거 폭주 — ✅ 구현, GPU 검증 (2026-10-25)
- **현상 (실측)**: 실패 응답 14건을 분해했다. 앞부분 20–30개 triple은 정상(예: `Tiganiada – authored by – Ion Budai-Deleanu`)이지만, 그 뒤로 같은 주어·술어에 목적어만 바꿔 나열한다(예: `Roma – linked to – historical justice / truth / accuracy …`). 같은 (주어, 술어)가 연속 39–115회였다. 목적어가 모두 달라 중복 제거로는 걸러지지 않는다. NER에서도 같은 현상이 있었다(316개 나열, "historical memory / documentation …").
- **추가 위험 (실측)**: 반복이 상한 전에 끝나면 파싱이 성공해 폭주 triple이 그래프에 그대로 들어간다(디코딩 실험 base 1건, 연속 39회).
- **디코딩 설정 실험** (`analysis/openie_degeneration_exp.py`, 결과 `analysis/openie_exp/`, 문제 10min 청크 4개 × 2회 = 설정당 8건, NER+triple)

  | 설정 | 파싱 실패 / 호출 | 상한 도달 | 폭주 (연속 ≥4) | 생성 토큰 |
  |---|---|---|---|---|
  | base (모델 기본: T=0.7, top_p 0.8, top_k 20, 반복 억제 없음) | 7/16 | 7/16 | 2/8 | 22,771 |
  | rp105 (`repetition_penalty=1.05`, 프롬프트 포함) | 1/16 | 1/16 | 4/8 | 12,731 |
  | rp110gen (1.10, 생성 토큰에만) | 2/16 | 1/16 | 0/8 | 10,799 |

  - 실패했던 청크만 골라 시험한 값이라 전체 비율이 아니다. 설정당 8건이라 표본이 작다.
  - rp105는 폭주를 줄이지 못했다(54·115회). rp110gen은 폭주가 없었지만 2건에서 1,300–1,400토큰을 생성하고도 유효 triple이 2개였다. 원문 응답을 저장하지 않아 원인(형식 손상 추정)은 확인하지 못했다.
  - HF `repetition_penalty`는 프롬프트 토큰에도 적용된다(transformers `RepetitionPenaltyLogitsProcessor` 문서, 코드). 원문 이름을 그대로 옮겨야 하는 OpenIE에 불리할 수 있다.
- **결정**: 디코딩 설정은 바꾸지 않는다(모델 기본값, WorldMM과 동일). 대신 HTTP 클라이언트에서 triple 응답(파싱 성공 포함)의 같은 (주어, 술어) **연속 15개 초과분을 버린다**(`MAX_SAME_SUBJ_PRED_RUN`).
- **기준의 근거와 한계**: 기존 캐시의 정당한 나열(의상, 점수 변화, 장면 요소)은 연속 최대 14회, 폭주는 39–115회였다. 그 사이 값(3min의 `Romania – has` 26회 등)은 판단이 애매해 15로 느슨하게 잡았다. 경험적 기준이다.
- **GPU 검증 (2026-10-25 C-1·C-2)**: 절단 146개(영상 1 6, 영상 2 68, 영상 3 72). 새 캐시의 최대 연속은 15(절단 기준), 기준을 넘는 청크는 0. 영상 2 3min의 연속 26회(10/22 결과)는 이번 결과에서 15로 잘렸다. 절단에 걸린 예에 장면 요소 나열(`basketball court – features – hoop, trampoline, …`)과 반복 서술(`Joshua Liendo – is – …`)이 섞여 있어, 기준이 정당한 나열도 자른다는 것이 확인됐다. 50개 영상 결과로 기준을 다시 본다(C-8).

### I25. `finish_reason` 부정확 — 🟡 우회
- **현상 (실측·코드)**: `local_llm_server.py`는 생성된 텍스트를 다시 토큰화해 길이를 세고, 상한 이상일 때만 `length`로 표시한다. 그래서 잘린 응답이 `completion=2047 finish=stop`으로 기록된 사례가 있다(12:27:46 NER 응답, JSON이 끊김).
- **대응**: 구제 조건을 `finish_reason`이 아니라 "파싱 실패"로 정했다. 서버 코드는 고치지 않았다. 서버 로그의 `finish=length` 수는 잘림 수의 하한으로만 해석한다.

### I26. 진행 보고·분석 중 집계 오류 — ✅ 정정
- 서버 호출 수를 `grep "chat.completions"`로 셌는데, 정규식의 `.`이 `/`와도 맞아 HTTP 접근 로그 줄까지 세져 **2배(374건)**로 보고했다. 실제는 187건이다. 실행 스크립트의 집계(`"chat.completions:"` 문자열 비교)는 정확했다.
- 실패 응답을 **13건**으로 보고했으나 **14건**이다. 분석 스크립트가 로그 맨 끝의 마지막 응답(12:36:51)에서 오류로 멈춰 빠졌다. 테스트 작성 중 발견했다.
- 디코딩 실험 base에서 "정상인데 긴 출력(M2)"을 **5건**으로 보고했으나 **4건**이다(잘린 5건 중 1건은 폭주).
- "base 호출의 44%가 상한 도달"은 실패 청크만 고른 실험의 값으로, 전체 비율로 해석하면 안 된다(실제 실행: 영상 1의 10min 1/9, 영상 2의 10min 12/18).
- **2026-10-25 문서 정합성 점검에서 찾은 기록 오류** (파일·로그·대화 기록 시각으로 확인)
  - I4의 "`paths.hf_home` 설정으로 해결": 컨테이너의 `HUGGINGFACE_HUB_CACHE`가 우선해 효과가 없었다(I4 정정).
  - 대기 실행 종료를 "00:08"로 보고: 00:08은 확인한 시각이고 실제 종료는 00:06:06이다.
  - "영상 2의 30sec·3min OpenIE 결과는 백업되지 않음"(I23): 세 파일 모두 백업돼 있다.
  - 검색 스모크·보고서 A·`.venv` 수리 날짜를 2026-10-22로 적음: 컨테이너 시계(UTC) 기준 2026-10-21이다(`DESIGN_AND_STATUS.md` §0.3).

### I27. GPU 공유 환경에서의 실행 — ✅ 해소 (2026-10-25 GPU 4–7에서 C-1–C-5 실행)
- **경과**: 2026-10-22 사용 범위가 GPU 4–7 → (다른 사용자 점유) 여유 메모리 내 → **GPU 6·7만**으로 바뀌었다. 다른 사용자 프로세스는 절대 건드리지 않는다.
- **현상 (실측)**: 14:10 실행에서 LLM 서버를 GPU 7(상한 19,000 MiB), 인덱서를 GPU 6(상한 15,000 MiB)에 올렸다. 시작 시 다른 사용자 사용량은 GPU 7 23,017 MiB, GPU 6 18,365 MiB였다. 실행 중 GPU 7의 다른 사용자 프로세스가 **34.2GB**로 늘어 합계 48,446 MiB가 됐고, 감시 장치(합계 47,500 MiB 초과 시)가 **우리 프로세스만** 종료했다. 다른 사용자 프로세스는 살아 있다. 합계가 49,140 MiB의 약 98.6%까지 갔으므로 그 순간 다른 사용자 쪽 할당 실패가 있었는지는 확인할 수 없다.
- **원인**: 다른 사용자 사용량의 관측 범위가 GPU 6 18–30GB, GPU 7 18–34GB다. Qwen3-VL-8B는 가중치만 약 17GB로 프로세스당 18–19GB가 필요해, 관측 최대치와 더하면 두 GPU 모두 용량을 넘을 수 있다.
- **대응**: `tests/gpu_3videos.py`를 2-GPU 배치(한 GPU에 우리 프로세스 1개), 시작 전 여유 확인(상한 + 2,000 MiB), 감시·자동 중단으로 바꿨다. `tests/run_service_capped.py`는 상한을 환경변수 `GPU_MEM_CAP_MIB`(기본 19,000)로 받게 했다.
- **대기 후 자동 시작 (2026-10-22 16:05 – 10-23 00:06, 실측)**: 사용자 지시("2시간 있다가 영상 3개 검증, report 작성까지, GPU 6·7, 다른 user 작업 중단 금지")로 `tests/delayed_gpu_3videos.py`를 새로 만들어 실행했다. 2시간 대기 후 30초마다 GPU 6·7을 재서 최근 10분 최대 사용량에 우리 상한(LLM 19,000 / aux 15,000 MiB)과 margin 1,500 MiB를 더해도 47,500 MiB 이하일 때만 시작하게 했다. 18:15:21–00:05:36에 **698번 판단, 만족 0번**, 가장 큰 여유 −961 MiB(18:35–18:36). 10분 최대값은 GPU 6 30.4–38.2GB, GPU 7 28.5–39.2GB였다. 우리 GPU 프로세스는 띄우지 않았고 캐시도 바뀌지 않았다(`outputs/3videos_20261022_160548_gated/`, `DESIGN_AND_STATUS.md` §9.9).
- **이후 경과**: 사용자가 다른 서버로 옮길 준비를 했다(2026-10-23, `MIGRATION_HANDOFF.md`, 파일 복사·검증까지). 2026-10-25 사용자가 이 서버의 **GPU 4–7 사용을 허용**했다(11:44 확인 시 GPU 0–7 모두 0–3 MiB).
- **2026-10-25 결과**: GPU 4–7(시작 시 다른 사용자 0)에서 C-1·C-3·C-4·C-5를 실행했다. 감시 장치 중단 0회, GPU 최대 35–39GB, 실행마다 종료 후 원상 복귀. 13:47 확인 시 GPU 0–3에는 다른 사용자 프로세스 4개(각 약 40GB)가 새로 올라와 있고 GPU 4–7은 비어 있다.
- **남은 일**: 실행 직전 여유 확인과 감시·자동 중단은 그대로 쓴다. `tests/delayed_gpu_3videos.py`는 2026-10-25 `--gpus` 인자를 받도록 고쳤다(사용자 승인).

### I28. LLM 서버 토크나이저 동시 사용 오류 `Already borrowed` — ✅ 수정 (2026-10-25)
- **현상 (실측)**: C-1(2026-10-25) LLM 서버 로그에 `worldmm.llm.qwen3vl ERROR Qwen3VL generation error: Already borrowed`가 261건 있다. 같은 기간 500 응답, `Generation failed`, `Token counting failed`는 0건이고 모든 요청(430)이 200으로 끝났다. 10/22 실행 로그에도 있었다(`outputs/3videos_20261022_120438/` 229건, `logs/prebuild_llm_*.log` 76건). 지금까지 기록하지 않았다.
- **결과에 영향이 없는 이유 (코드)**: `Qwen3VLModel.generate`에 `dynamic_retry_decorator`(최대 5회, 대기 1–10초)가 붙어 있어 실패한 시도가 서버 안에서 다시 실행된다(`WorldMM/src/worldmm/llm/qwen3vl.py:345`, `utils.py`). `Already borrowed`는 Rust 토크나이저가 동시 사용을 막을 때 내는 예외라 결과를 조용히 바꾸지 않는다.
- **원인 (코드 근거, 가장 가능성 높음)**: `local_llm_server.py`는 생성(`llm.generate`)은 `generate_lock` 안에서 하지만, 응답 뒤 토큰 수를 세는 `count_tokens`는 잠금 밖에서 같은 토크나이저를 쓴다(130행·135행). Flask가 요청을 스레드로 처리하므로(`threaded=True`) 한 요청의 토큰 계산과 다른 요청의 생성 준비(채팅 템플릿·토크나이즈)가 겹치면 충돌한다.
- **비용**: 충돌마다 재시도 대기(1초 이상)가 생기고, 그동안 그 서버의 `generate_lock`이 잡혀 있다. C-1 전체로는 수 분 이내로 추정한다(측정하지 않음).
- **수정 (2026-10-25, 사용자 승인, `baf08d8`)**: `count_tokens` 호출을 `generate_lock` 안으로 옮겼다(`local_llm_server.py`). CPU 테스트(`tests/test_p9_p19.py`)로 위치 확인. 보고서 생성은 서버당 요청이 하나씩이라 수정 전에도 0건이어서, 실제 효과는 다음 사전 인덱싱(서버당 동시 요청 다수)에서 확인한다. 재시도 대기가 없어지고 `finish_reason` 계산도 같은 잠금 안에서 이뤄진다.

### I29. 같은 영상 동시 불러오기 시 OpenIE 캐시 읽기 실패 — ✅ 대응 (2026-10-25)
- **현상 (C-5 첫 시도)**: 묶음 4개가 영상 2개를 나눠 처리하면서 두 검색 서비스가 `54k2g9ddy4M`을 동시에 불러왔고, 한 서비스에서 `POST /load`가 HTTP 500(`json.decoder` 오류, `HippoRAG.load_existing_openie`)이 됐다. 해당 보고서는 exit 2.
- **원인 (코드)**: `HippoRAG.index()`는 새 청크가 없어도 매번 `save_openie_results`로 OpenIE 캐시 파일(`openie_results_ner_*.json`)을 다시 쓴다(`HippoRAG.py:206-207`, `save_openie` 기본값 True). 서비스의 `load`가 `episodic.index()`를 부르므로, 같은 영상을 동시에 불러오면 한쪽이 다시 쓰는 중인 파일을 다른 쪽이 읽는다. C-3에서도 서비스 3개가 시작 시 같은 영상을 동시에 미리 불러왔지만 그때는 충돌이 없었다.
- **영향 확인**: 우리 프로세스 그룹만 종료한 뒤, 다시 쓰인 파일은 OpenIE 캐시 12개뿐(그래프·임베딩 변화 없음)이고 12개 모두 정상적으로 읽히며 통계가 C-1 직후 기록과 같음을 확인했다. 두 프로세스가 쓰는 내용이 같아 손상 가능성은 낮지만, C-1 직후의 바이트 사본이 없어 완전 동일성은 확인하지 못했다. 확인 후 사본 `backups/cache_after_c1_verified_20261025/`.
- **대응**: `tests/gpu_report_batch.py`가 run_report 전에 영상별 잠금을 잡고 직접 불러온다(`bbceff6`). 서비스 코드는 고치지 않았다. 여러 서비스를 띄울 때 같은 영상을 동시에 불러오지 않는다는 규칙이 필요하다.

### I30. 같은 작업 폴더에서 Claude 세션 2개가 겹쳐 실행 — 🟡 운영 규칙 (2026-10-25)
- **현상 (실측)**: 2026-10-25 13:50 `ps`에 같은 작업 폴더(`/data1/jyheo/workspace/VideoRAG`)의 `claude` 프로세스가 3개 있었다(PID 251: 약 3일 23시간 전 시작, pts/0 / PID 57851: 약 2일 12시간 전, pts/1 / PID 180368: 13:39:44 시작, pts/3 = 새 세션). 새 세션이 13:47:46에 문서를 확인했을 때 `DESIGN_AND_STATUS.md` §9.14와 I29는 없었는데, 13:48:32–13:49:24에 문서 5종이 고쳐지고 커밋 `fbfb796`(13:49:24, "C-5: …")이 생겼고, 13:49:40에 Claude 메모리 파일이 고쳐졌다. 이전 세션(PID 251과 57851 중 하나, 어느 쪽인지는 확인하지 않음)이 C-5 기록을 마무리한 것이다.
- **영향**: 이번에는 두 세션의 수정 시점이 겹치지 않아 충돌이 없었다. 새 세션은 이전 세션의 C-5 기록을 직접 계산한 값과 대조해 핵심 수치가 일치함을 확인했다(writer 프롬프트 평균만 계산 방식 차이로 수십 토큰 다름).
- **위험**: 두 세션이 같은 파일을 동시에 고치면 한쪽 수정이 덮어써질 수 있고, GPU 작업을 두 세션이 각각 띄우면 자원·캐시 충돌(I29)이 생길 수 있다.
- **함께 확인한 것**: 새 세션 시작 시 이전 세션의 백그라운드 작업 2개(C-5 배치 대기, 5분 점검 타이머)가 "stopped"로 표시됐지만, `setsid`로 띄운 C-5 배치 자체는 13:46:00에 8건을 모두 끝냈다(`summary.json`).
- **대응**: 같은 작업 폴더에서는 세션 하나만 쓴다(사용자가 쓰지 않는 세션 종료). GPU 실행은 `setsid`로 띄우고 상태는 결과 파일과 `ps`로 확인한다.

---

## 4. 보고서 A와 B 비교 (측정값)

| 항목 | A: 스모크 | B: `run_report.py` 첫 실행 |
|---|---|---|
| 섹션 수 / 결론 | 5 / 없음 | 6 / `Conclusion:` 244단어 |
| 단어 수 | 2,962 | 2,549 |
| LLM 호출 | 16 | 생성 19 + 번역 6 = 25 |
| 시간 | 382초 | 생성 261.5초 + 번역 231.8초 = 494.4초 |
| writer 출력 토큰 | 614–1,121 | 374–794 |
| 텍스트 인용 → 참조 | 109 → 46 | 72 → 35 |
| 이미지 인용 (잘못된 형식) | 14 (8) | 19 (4) |
| 이미지를 넣은 섹션 | 2/5 (S3은 잘못된 형식만) | 5/6 (결론은 잘못된 형식 1개만) |
| 규칙 검사, 실행 당시 규칙 (unsupported / miscited / uncited) | 4 / 5 / 8 | 6 / 3 / 14 |
| 규칙 검사, 현재 규칙 (unsupported / miscited / uncited / absence) | 4 / 5 / 7 / 1 | 4 / 3 / 12 / 3 |
| 확인된 오탐 | `SCORE 6` ×2 | `10:85`, `9:51` (현재 규칙에서는 absence) |
| 섹션 안 단락 유사도 최대 | 0.901 | 0.235 |
| 섹션 간 유사 문장 (≥0.7) | 5 | 3 |
| episodic / semantic / image 인용 항목 | 38/40, 11/20, 7/15 | 34/48, 6/24, 16/18 |
| 실패 문자열, `[?]`, 누락 프레임 | 0 | 0 |
| `validation.json` 상태 | (해당 없음) | passed, exit 0 |

---

## 5. 남은 문제와 다음 단계

| 문제 | 현재 상태 | 다음 단계 |
|---|---|---|
| P9 반복, P11 결론 인용 불일치, P5 설명 유입 | 규칙 6 + C0. C-5(4 대 4): 효과 확인 안 됨. 루프는 2026-10-25 상한·제거·경고로 대응(§9.16: 루프 2/9건, 130–134초에 끊김) | (C-5 완료) writer 루프 대응(출력 상한 하향, 루프 감지 후 재생성·잘라내기, 검증 경고)과 C0 유지 여부는 사용자 결정 대기. 남으면 R2(삭제만), 설명 유입 금지 규칙, 결론 인용 방식 검토 |
| P19 결말 오인 | writer 규칙 7 + 결말·시작 서술 검사(§9.16). 2026-10-26: 영상 끝 근거(txt0) 제공, 오탐 수정(§8.13) | 다음 GPU 실행에서 효과 확인 |
| P15 번역 품질 | 한자 감지·이름 보호 구현. C-4 실측: 17섹션 중 5개 실패(자리표시자 불일치), 한자·가나 잔존 3 | 실패 원인 분석(미확정), 이름 보호 유지 여부, 제목 형식 통일은 사용자 결정 대기 |
| P12 추측·해석 표현 | 측정·원인 확인(§9.17): 다단위 요약 캡션의 해석 표현이 주된 출처 | 검출 경고, 요약 캡션 정제, writer 규칙 중 사용자 결정 |
| P6 장면 오인, P7 주제-근거 불일치, P8 시간 순서 | 대응 없음. C-4에서 P8(섹션 순서 뒤집힘) 재확인 | 표본을 늘려 측정. 대응 방식은 P19와 함께 검토 |
| P13·P14 근거 구성 | 결정 7 보류, 시간 차이는 기록 중 | 결정 1 완료 후 실험(`ANALYSIS_D4_D7.md` §3), 사용자에게 다시 질문 |
| P3·P4·P18 규칙 검사 | 감지 + absence 처리 | 표본을 늘려 정밀도·재현율 측정 |
| I10 빈 triple의 "완료" 판정, I16 L1 표시 | 문서화 | 필요 시 기록·구분 추가 |
| I18 사전 인덱싱 | 영상 3개 완료(2026-10-25 C-1) | 50개(C-7, 사용자 지시 전 미실행) |
| I23·I24 분할 OpenIE·구제·절단 | 구현, GPU 검증(C-1·C-2) | 50개 영상 결과로 분할 기준(1,100토큰)·절단 기준(15)을 다시 본다(C-8). 분할 기준 아래 잘림 3건, 정당한 나열 절단 확인 |
| I28 `Already borrowed` | 수정(2026-10-25) | 다음 사전 인덱싱에서 0건인지 확인 |
| I22 10min 캡션 잘림 | 보류. 검증 영상 `0RxMZBLeqRI`의 10min 2개 해당 | 사용자 결정 시 10min만 재생성(약 4–6시간/프로세스 1개). 검증 결과 해석 시 분리 |
| I27 GPU 공유 | 해소(2026-10-25 GPU 4–7에서 C-1–C-5 실행) | 실행 직전 여유 확인 유지 |
| I29 같은 영상 동시 불러오기 | 배치 스크립트 영상별 잠금 | 서비스를 여러 개 띄우는 다른 방식에서도 같은 규칙 적용 |
| I30 Claude 세션 중복 | 확인(2026-10-25) | 세션 하나만 쓰기 |
| 표본 수 | C-4 영상당 1건, C-5 조건당 2회 | 다중 실행·다중 영상 실험 |
