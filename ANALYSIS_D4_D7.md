# 결정 4(반복 억제)·결정 7(근거 구성) 분석

- 작성일: 2026-10-22
- 이 문서는 이전 두 문서를 하나로 합친 것입니다: 기존 `ANALYSIS_D4_D7.md`(보고서 A 지표, 선택지 분석)와 `ANALYSIS_REFINE_D4_D7.md`(Deep-Reporter의 refine 단계 확인, 보고서 B 지표, C0/R1–R3, 결정 7의 설정과 한계).
- 문제 전체 목록과 개선 이력은 `REPORT_ISSUES_AND_FIXES.md`에 있습니다.

## 0. 결정 현황, 표기, 데이터

### 0.1 결정 현황

| 결정 | 상태 | 내용 |
|---|---|---|
| 결정 4 (반복) | **결정·구현 완료** (CPU 검증 ✔, 실제 모델 효과 측정 ✖) | **B안**: writer 규칙 6(반복 금지)<br>**C0**: 앞 섹션에서 실제로 쓴 문장을 writer와 query 생성에 전달 (§1.5) |
| 결정 7 (근거 구성) | **보류** | 설정과 한계를 정리함(§2). 결정 1(사전 인덱싱) 이후 실험해서 다시 질문 |

### 0.2 표기
- **(코드)** 소스에서 직접 확인
- **(논문)** Deep-Reporter 논문(arXiv 2604.10741) 본문에서 확인
- **(실측)** 실행 결과에서 측정
- **(추정)** 계산이나 가정에 기반한 값
- **(가설)** 확인되지 않은 원인

### 0.3 분석 대상

| | 보고서 A: 스모크 | 보고서 B: 수정 후 첫 실행 |
|---|---|---|
| 결과 위치 | `tests/_artifacts/gpu_report/` | `tests/_artifacts/gpu_e2e/outputs/report_run1/` |
| 템플릿 | 규칙 4(이미지 형식)·결론 규칙 **없음** | 규칙 4 + 결론 섹션·섹션 상한 6 + 번역. **규칙 6과 C0는 없음**(이후 구현) |
| 섹션 수 | 5 | 6 (마지막이 결론) |
| 지표 파일 | `tests/_artifacts/analysis/smoke_metrics.json` | `tests/_artifacts/analysis/e2e_run1_metrics.json` |
| 공통 조건 | 영상 `-QuCz7kxBr8`(농구 가젯 리뷰, 약 32분), 같은 query, Qwen3-VL-8B 로컬, L1 필터, **episodic 10sec 단위만**, Deep-Reporter filter off | |

- 지표 스크립트: `analysis/analyze_report.py`(읽기 전용)
- 문단 유사도는 SequenceMatcher로 계산합니다. 인용·이미지 표기와 제목 줄을 빼고 소문자 단어로 정규화한 뒤 비교합니다.

### 0.4 한계
- 조건마다 보고서가 1건뿐입니다.
- 생성은 샘플링입니다(§1.2-①). 같은 조건에서도 결과가 달라지므로, 아래 비율은 "그 실행에서 관측된 값"이고 일반화할 수 없습니다.
- 10sec 단위만 썼으므로 4개 단위 조건과 다를 수 있습니다.
- 그래서 결정 7과 결정 4의 효과 확인에는 §3의 다중 실행 실험이 필요합니다.

---

## 1. 결정 4: 반복

### 1.1 관측된 반복

**섹션 안** (실측)

| 지표 | A | B |
|---|---|---|
| 섹션 안 문단 쌍 수 | 67 | 섹션 6개 기준(지표 파일 참고) |
| 문단 유사도 최대 | **0.901** (S5 문단 5↔6) | 0.235 (S5 문단 4↔6) |
| 그다음으로 높은 쌍 | 0.118 (S5 3↔6), 0.113 (S5 1↔6) | 0.100 (S5 5↔7) |
| 유사도 ≥0.5인 문단 쌍 | 1 | 0 |
| A 분위수 (중앙값 / 90% / 99%) | 0.035 / 0.078 / 0.901 | — |
| 반복 8-gram 비율 | S5 **0.281**, 나머지 섹션 0.0–0.011 | 최대 0.036 (S5) |
| 문장 근접 중복(≥0.8) | S5에서만 5쌍 | 0 |

- A의 S5 문단 5와 6은 거의 같은 내용입니다. "The challenge concludes … group remains on the court …", "three shots with the glove, three without …", "CASH LOST …" 문장들이 같은 인용과 함께 다시 나옵니다.
- 같은 쌍을 처음에는 **0.711**로 보고했습니다. 이는 인용 표기를 포함한 원문 단락으로 잰 값입니다. 정규화하면 0.901로, 같은 현상을 다른 방식으로 잰 것입니다.

**섹션 사이** (실측)

| 지표 | A | B |
|---|---|---|
| 섹션 간 유사 문장 쌍(≥0.7) | 5 | 3 |
| 내용 | 4쌍은 S4↔S5 마무리 상투 문장("… concludes …, and the group remains on the court, with no further …"), 1쌍은 실제 사실 반복(S2↔S3, "man in a red hoodie asks … dribble stick", 00:02:30) | 3쌍 모두 S1/S3/S4의 배경 묘사("outdoor basketball court under a clear sky …") |
| 여러 섹션에 다시 검색된 근거 항목 | 7 / 67 uid | 18 / 67 uid |

**B의 개선은 수정 효과가 아닙니다.** B에는 반복을 막는 수정이 없었습니다. 샘플링 편차와 짧아진 writer 출력(A 614–1,121토큰, B 374–794토큰)이 겹친 결과로 보입니다(가설).

### 1.2 원인 분석

**① 생성 설정** (코드)
- Qwen3-VL-8B `generation_config`: `do_sample=true`, temperature 0.7, top_p 0.8, top_k 20, repetition_penalty 1.0.
- `local_llm_server.py`는 요청에서 max_tokens/temperature/top_p만 전달합니다. Deep-Reporter는 temperature를 보내지 않습니다.
- 따라서 **모든 호출이 모델 기본값으로 샘플링**되고, 결과는 재현되지 않습니다.

**② 잘림 아님** (실측): A의 16회 호출 모두 `finish=stop`이었습니다. 최대 출력은 1,121토큰으로 8,192보다 훨씬 작습니다.

**③ 앞 섹션 정보 전달 방식** (코드, 실측)
- 논문은 `m_global`을 "maintains a **recursive summary** of the narrative arc"라고 설명합니다.
- 코드의 `_update_context`(`deep_reporter/nodes/section_writing_node.py:214`)는 LLM 요약이 아닙니다.
  - 요약에 붙는 항목: `Section: <planner 섹션 설명>` + `Content: <본문 앞 100자>...`
  - 2,000자를 넘으면 앞쪽 섹션은 첫 줄(= 섹션 설명)만 남깁니다.
  - 따로 넘기는 것: 직전 섹션의 마지막 3문장(`previous_section_tail`, `.`으로 나눔)
- **본문 앞 100자는 대부분 제목 줄**이라, 실제로 쓴 사실은 거의 전달되지 않습니다.
- 같은 요약이 query 생성 노드(`previous_sections_summary`)에도 들어갑니다.

**실측: 보고서 B에서 writer가 받은 이전 섹션 요약** (`_update_context`를 B의 실제 섹션들로 다시 실행해 복원)

| writer | 요약 길이 | 내용 |
|---|---|---|
| 섹션 2 | 549자 | 섹션 1 설명 + "# Section 1: Introduction of Participants…" 앞 100자 |
| 섹션 6 (결론) | 2,212자 | 섹션 1–2는 **설명만**(압축됨). 섹션 3–5는 설명 + 예: `# Shooting Challenges: Straight Shooter Strap, Flick Glove, and Forfeits\n\nDuring the shooting challe...` |

- 결론 writer가 받은 앞 섹션 정보는 planner가 미리 쓴 설명뿐이었고, 실제 본문은 거의 받지 못했습니다.
- 이는 B의 결론 인용 불일치를 설명합니다(`REPORT_ISSUES_AND_FIXES.md` P11·P5).
  - 결론이 쓴 "Flick Glove"는 어느 섹션 근거에도 없고 섹션 3의 **설명**에만 있습니다.
  - "SKLZ Dribble Stick", "Shot Coach"도 섹션 2·4 설명에 있는 이름입니다.
- 우리 writer 템플릿에는 결정 4 이전까지 반복 금지 규칙이 없었습니다. 그런 지시는 query 템플릿에만 있었습니다.

### 1.3 Deep-Reporter에 전체 refine/polishing 단계가 있는가 → 없습니다

**코드** (코드)
- 그래프(`deep_reporter/core/graph.py`)의 노드는 `planner`, `query_generation`, `search`, `filter`, `section_writing`, `combine` 6개이고, 마지막 연결은 `combine → END`입니다.
- `combine_node`는 섹션 본문을 `"\n\n".join(...)`으로 이어 붙이기만 합니다. 빈 섹션에는 `[Section k content missing]`을 넣고 인용 수를 셉니다. **LLM 호출도, 내용 수정도 없습니다.**
- `deep_reporter/` 패키지에서 `refine|polish|revis`를 검색하면 일치하는 코드가 0건입니다.
- 저장소 전체에서 일치하는 곳은 두 곳뿐입니다.
  - 평가 프롬프트(`evaluation/prompts/eval_templates.py`, "Look past the polish" 등 채점 기준)
  - 기존 설계 메모(`Deep-Report/claude_output/INTEGRATION_CONTEXT.md` 96행 "(후속) … editorial refine"). 계획 항목일 뿐 구현은 없습니다.

**논문** (논문)
- §2.1의 구성은 Planner, Searcher-Filter, Reporter입니다. 생성은 섹션별 "Checklist-Guided Incremental Synthesis"이고, 섹션 사이의 일관성은 Recurrent Context Update로 맞춥니다. 생성 뒤 보고서 전체를 다시 다듬는 단계는 없습니다.
- 논문의 "refine"은 다음 세 가지 뜻뿐입니다.
  - 근거를 거르는 단계("refine/filter relevant evidence")
  - outline을 사람이 다듬을 수 있다는 선택 사항("optional human-in-the-loop refinement")
  - 벤치마크 정답인 "Expert-Refined Silver Reports"
- 반복은 **평가 지표**(Full Report의 Repetition Absence `S_Rep`)로만 다룹니다.

### 1.4 선택지 전체 비교

| ID | 방법 | LLM 추가 | 장점 | 단점·위험 (확인된 사실 위주) | 판단 |
|---|---|---|---|---|---|
| A | 감지만 (validation 경고, `analyze_report` 지표) | 0 | 출력 불변, 측정 도구로 사용 | 반복 자체는 남음 | 측정 도구로 계속 사용 |
| **B** | writer 템플릿 규칙: 반복 금지, 앞 섹션 사실은 한 문장만 | 0 | 구현 작음 | 8B 모델의 준수율 미측정. **writer가 앞 섹션 본문을 보지 못하면 섹션 간 반복에는 효과가 제한적**(§1.2-③) | **채택** |
| **C0** | `_update_context`를 실행 중에만 교체해 **실제로 쓴 문장**을 전달 | 0 (프롬프트만 증가) | B가 섹션 간 반복에 작동할 정보를 제공. 결론도 실제 본문을 보고 요약 가능. 설명 대신 본문을 전달하므로 P5·P11 완화 기대(미검증) | Deep-Reporter 내부 함수 교체(파일은 수정 안 함, 계약 검사·복원). 프롬프트가 늘어 writer·query 지연 증가 | **채택** |
| R1 | 생성 뒤 보고서 전체를 LLM이 다시 씀 | 1회, 출력 약 3,800토큰(B의 writer 출력 합 3,762) → 약 160초(추정, B 실측 처리 속도 약 23토큰/초 기준) | 통합·재서술 가능 | 8B 모델의 긴 출력에서 인용 누락·이동, 새 오류, 반복 위험. 섹션 간 내용을 섞으면 **섹션별 근거 번호 체계와 충돌**. 재서술이 근거와 맞는지 규칙으로 보장 불가 | 비권장 |
| R2 | 섹션별 "삭제만" refine: 앞 섹션 본문 + 현재 섹션의 번호 붙은 문장 → 이미 말한 문장 번호(JSON)만 받아 삭제 | 섹션 수 − 1회, 1회 약 4–5초(추정: 비슷한 형태인 L1 필터 실측 3.3–5.4초) | 결과가 원문의 부분집합임을 코드로 보장 | 고유한 사실을 지울 위험 → 안전장치 필요(그 문장만 가진 인용·숫자·시간이 있으면 삭제 금지 등). 이미지 줄 앞 문장 삭제 시 배치가 어색해짐 | 후보(B+C0 측정 후에도 반복이 남으면) |
| R3 | 규칙 기반 근접 중복 제거 (유사도 ≥ τ인 뒤쪽 문장·단락 삭제) | 0 | 결정적. A의 S5 사례에서는 차이가 큼(0.901 vs 다음 0.118) | τ의 근거가 보고서 2건뿐. B의 배경 묘사 쌍(0.73–0.79)을 지울지는 τ에 따라 다름. 삭제된 문단에만 있던 인용·그림이 사라짐. 의미 반복은 못 잡음 | 후보 |
| D | `repetition_penalty` > 1.0 | 0 | 구현 1줄 | HF `RepetitionPenaltyLogitsProcessor`는 **프롬프트 토큰도 벌점 대상**이라 근거의 이름·인용·시간·인용 토큰 복사를 억제함 → 근거 충실도와 형식 위험. 피하려면 프롬프트 이후 토큰만 벌점 주는 커스텀 processor 필요 | 비권장 |
| E | `no_repeat_ngram_size` | 0 | — | input_ids 전체(프롬프트 포함) 기준이라 근거 n-gram 복사를 금지함 | 부적합 |
| F | presence/frequency penalty | — | — | transformers `generate`에 없음 | 불가 |
| G | 앞 섹션 요약을 LLM으로 생성 | 섹션당 +1 | 의미 요약 | 무거움. Deep-Reporter 내부 함수 교체 필요 | 보류 (C0로 대체) |
| H | temperature를 낮추거나 greedy | 0 | 재현성 | greedy는 반복 루프를 늘릴 수 있다고 알려져 있음(이 시스템에서는 미측정) | 보류 |

**R1을 권장하지 않는 핵심 이유**: 이 파이프라인은 문장마다 **그 섹션의 근거 번호**를 인용하고, 후처리기와 규칙 근거 검사가 그 번호로 검증합니다. 보고서 전체를 다시 쓰면 이 검증 고리가 끊깁니다.

**refine을 넣는다면 위치**: 후처리기(`ground_report`) **전에**, outline의 섹션 본문(섹션별 `[citation:txtN]` 상태)에 적용해야 합니다. 그래야 삭제 뒤에도 전역 번호, References, 그림이 자동으로 다시 계산됩니다. 후처리 뒤에 적용하면 References와 그림을 다시 맞춰야 해서 더 위험합니다.

### 1.5 결정과 구현

**B안: writer 규칙 6** (`domain_templates.py`, videomme writer `# Grounding Rules (CRITICAL)`)
> 6. Do not repeat a fact, sentence, or paragraph you have already written in this section. If a fact was already covered in a previous section (see "Context from Previous Sections"), mention it in at most one short sentence and focus on what is new in this section. Exception: a conclusion section (see "Conclusion Section") restates earlier results briefly by design.

- 결론 섹션은 앞 결과를 요약하는 것이 목적이라(결정 5), 규칙 6과 충돌하지 않도록 예외를 명시했습니다.
- 계약 검사: `REQUIRED_MARKERS["SECTION_WRITING_TEMPLATE"]`에 `"mention it in at most one short sentence"`를 추가했습니다. 규칙이 빠진 템플릿은 실행 전에 `TemplateContractError`로 막힙니다.

**C0: 앞 섹션에서 실제로 쓴 문장 전달** (`domain_templates.apply_written_context()`, `run_report.py`, `config.yaml`)
- **동작**: `with` 블록 동안만 `section_writing_node.__globals__["_update_context"]`를 바꿉니다. 템플릿 교체와 같은 방식이며, Deep-Report 파일은 수정하지 않습니다.
- **실행 전 계약 검사**
  - 노드가 전역 `_update_context`를 호출하는지
  - 함수 시그니처가 `(previous_summary, new_content, section_desc)`인지
  - 반환값이 `(summary, tail)` 문자열 두 개인지(실제 호출로 확인)
  - 하나라도 어긋나면 실행 전에 중단합니다.
- **요약 형식** (LLM 0회, 결정적)
  ```
  Already written in earlier sections (title, then the first sentence of each paragraph; citation numbers removed - they do NOT refer to the evidence of the current section):
  Section 1: <제목, "Section k:" 접두어 제거>
  - <단락 1의 첫 문장, 인용·이미지 표기 제거, 시간 유지>
  - <단락 2의 첫 문장>
  ...
  ```
- **상한**
  - 문장당 240자, 섹션당 700자, 전체 3,600자
  - 전체 상한을 넘으면 오래된 섹션부터 제목 줄만 남깁니다.
  - 4단어 미만 단락은 건너뜁니다.
- **인용 번호를 지우는 이유**: 앞 섹션의 `[citation:txtN]`은 그 섹션의 근거 목록을 가리킵니다. 현재 섹션의 근거 번호와 섞이면 잘못된 인용이 생기므로 모두 제거하고, 안내 문구로 이 사실을 밝힙니다.
- **tail**: 원래 `_update_context`가 계산합니다(새 본문에만 의존하므로 결과가 같습니다).
- **영향 범위**: 같은 요약이 query 생성에도 들어갑니다(Deep-Reporter 구조).
- **설정과 기록**
  - `config.yaml`의 `report.previous_sections_context`: `written`(기본, C0) / `deep_reporter`(원래 동작, 비교 실험용). 다른 값이면 exit 2.
  - `validation.json`과 `report.json`에 사용한 모드를 기록합니다.
- **보고서 B로 재현한 C0 요약**: 섹션 1–5 합계 3,229자로, 각 섹션의 제목과 단락 첫 문장이 들어갑니다. 예: `- Following the dribbling trial, the video introduces the SKLZ Dribble Stick at 00:02:30.`

**CPU 검증** (✔ 2026-10-22)
- `tests/test_templates.py` 전부 통과
  - 규칙 6 존재, 규칙 6이 빠지면 거부
  - 요약 단위 테스트: 제목, 첫 문장, 인용 제거, 짧은 단락 제외, 누적, 3,600자 상한
  - 교체·복원: 예외 발생 시 복원, 중첩 거부, tail이 원래 함수와 같음
  - Deep-Reporter 전체 그래프(가짜 LLM)
    - C0 적용 시 LLM 호출 수는 그대로 5회
    - writer 2가 섹션 1의 실제 문장을 인용 없이 받음
    - query 생성도 같은 요약을 받음
    - 블록 밖에서는 원래 `_update_context`로 복원됨
- `test_report_pipeline.py`(C0 기본 적용 상태), `test_retriever.py` 회귀 통과

**미검증** ✖
- 실제 모델에서 반복이 줄어드는지, 결론 인용 불일치(P11)와 설명 유입(P5)이 줄어드는지
- writer·query 프롬프트 증가에 따른 지연 증가(요약 최대 3,600자 ≈ 900토큰 추정)

### 1.6 다음 측정
- GPU에서 C0 `written`과 `deep_reporter`를 같은 조건으로 각각 2회 이상 실행합니다(가능하면 4개 단위 캐시로).
- 측정 지표
  - 섹션 안 최대 단락 유사도
  - 섹션 간 유사 문장 수
  - 근거 검사 지적 수(특히 결론 섹션)
  - writer 입력 토큰과 지연
- 반복이 남으면 R2(삭제만)를, 근접 중복만 남으면 R3를 검토합니다.

### 1.7 측정 결과 (2026-10-25 C-5, `DESIGN_AND_STATUS.md` §9.14)
- 조건: 4개 단위 캐시, L1, 영상 2개(`-QuCz7kxBr8`, `54k2g9ddy4M`) × C0 `written` / `deep_reporter` × 2회, 번역 끔.
- 결과
  - writer가 8,192토큰까지 같은 문장 묶음을 되풀이한 루프: `written` 2/4, `deep_reporter` 0/4(C-4의 `written` 3건은 0/3). 루프 출력은 보고서에 그대로 들어갔고 검증은 통과했다.
  - 참고(비교 미사용): C-5 첫 시도에서 중단 전에 끝난 4건(`written` 3, `deep_reporter` 1)도 루프 0건이었다. 합치면 지금까지 `written` 10건 중 2건, `deep_reporter` 5건 중 0건이다.
  - 루프를 뺀 실행에서 섹션 안 단락 유사도 상위 1%(`written` 0.085·0.111 / `deep_reporter` 0.039–0.219), 섹션 간 유사 문장(1·0 / 0–2), 결론 섹션 지적 수(7·1 / 0–4)에 일관된 차이가 없다.
  - writer 프롬프트는 `written`이 평균 142토큰 길다(5,191 vs 5,049). 정상 출력의 writer 지연은 36.5초 vs 33.5초.
- 해석: 4 대 4 표본으로는 C0의 효과도, C0와 루프의 관계도 판단할 수 없다(루프 2/4 대 0/4, Fisher 정확검정 양측 p ≈ 0.43). 단락 유사도 지표는 한 단락 안의 루프를 잡지 못한다(영상 1 `written` r1: 완전 중복 문장 295개인데 0.5 이상 쌍 0).
- 다음에 검토할 것(사용자 결정 필요): writer 출력 상한을 낮추거나 반복 루프를 감지해 다시 생성·잘라내는 장치(R2와 비슷한 후처리), C0 유지 여부, 표본을 늘린 재측정.

---

## 2. 결정 7: 근거 구성 (보류, 다음에 다시 질문)

### 2.1 현재 설정 (코드: `config.yaml`, `videorag_retriever_service.py:384–400`)

| 항목 | 값 | 실제 동작 |
|---|---|---|
| Deep-Reporter `text_topk` / `image_topk` | 20 / 10 | 검색 서비스에 넘기는 상한 |
| `episodic_k` | 8 | text 요청당 episodic = min(8, topk) |
| `semantic_k` | 4 | min(4, topk − episodic) |
| `episodic_candidates_per_query` | 10sec 3, 30sec 3, 3min 2, 10min 1 (A·B 실험은 10sec 6) | L0/L1 그래프 검색 후보 수 |
| `semantic_k_per_query` | 5 | 쿼리별 후보를 RRF로 병합 |
| `visual_k_per_query` / `image_k` | 3 / 4 | image 질의가 1개면 결과 **3장**(A·B 모두 섹션당 3장, 실측) |
| L1 필터 | 요청당 1회 | episodic 후보 중 8개 선택 |

결과적으로 writer는 섹션당 **episodic 8 + semantic 4 + 이미지 3 = 15건**을 받습니다(A·B 실측).

### 2.2 관측된 영향 (실측)

**유형별 사용**

| 유형 | A: 검색 / 인용 항목 / 인용 횟수 | B: 검색 / 인용 항목 / 인용 횟수 | 항목당 평균 단어 (A / B) |
|---|---|---|---|
| episodic | 40 / 38 (95%) / 90 | 48 / 34 (71%) / 66 | 86.7 / 86.8 |
| semantic | 20 / 11 (55%) / 19 | 24 / 6 (25%) / 6 | 10.4 / 9.9 |
| image | 15 / 7 (47%) / 14 | 18 / 16 (89%) / 19 | 92.7 / 88.4 |

**검색 순위별 인용** (인용된 섹션 수 / 검색된 섹션 수)
- A episodic: 순위 1–8 모두 4–5/5. 순위가 낮은 항목도 거의 다 쓰였습니다.
- B episodic: 순위 1–5는 5–6/6, **순위 6–8은 2–3/6**. 이 1회 실행에서는 낮은 순위가 덜 쓰였습니다.
- semantic: A 순위 1–4에서 2–3/5, B 순위 1–4에서 0–4/6
- image: A 2–3/5, B 5–6/6

→ 두 실행의 경향이 다르므로, 이것만으로 k를 줄여도 된다는 근거는 되지 않습니다.

**규칙 근거 검사 지적(unsupported·miscited)의 인용 유형**
- A: episodic 11, semantic 1, image 1. 인용 수 대비 11/90, 1/19, 1/14로 유형 간 차이가 크지 않습니다(표본이 작음).
- B: episodic 7, semantic 1, image 2. 이 중 7건이 결론 섹션입니다.

**semantic triple의 질** (A 20개, B 24개 모두 확인)
- 사소하거나 중복된 triple이 많습니다.
  - A: `(player, can dribble, basketball)`(S1·S3 중복, 둘 다 미인용), `(player, wears, black hoodie)`, `(Flick Gloves, has colors, black/orange/white)` 3개(인용됨, "glove's colors" 문장을 만듦)
  - B: `(basketball court, is played on, basketball court)`, `(player, shoots, basketball)`(S2·S4), `(white object, is, device)`
- 쓸모 있는 것도 있습니다.
  - 규칙 정보: `(challenge, penalizes least baskets with, 100 sit-ups)`. A의 S3에서는 미인용, B에서는 S3·S5·S6에 반복 검색됨
  - 화면 문자: `MOST DRIBBLES IN 15 SECONDS`, `SCORE 8` 등. 인용되는 경우가 많음

**이미지와 텍스트 근거의 시간 차이** (섹션에서 인용된 episodic 구간 중 가장 가까운 것까지의 거리, 초; ✓ 인용됨, ✗ 미인용)

| 섹션 | A | B |
|---|---|---|
| S1 | 34:45 ✓ 335, 28:45 ✓ 5, 20:15 ✓ 495 | 25:55 ✓ 165, 21:35 ✓ 425, 21:45 ✓ 415 |
| S2 | 15:55 ✓ 75, 14:05 ✓ 25, 01:55 ✓ 0 | 00:35 ✓ 5, 00:45 ✓ 0, 20:05 ✓ 435 |
| S3 | 01:55 ✗ 35, 19:35 ✗ 385, 04:25 ✓ 5 | 34:45 ✓ 485, 21:35 ✓ 265, 28:45 ✓ 125 |
| S4 | 20:55 ✗ 805, 31:05 ✗ 1415, 20:35 ✗ 785 | 30:35 ✓ 635, 01:25 ✓ **1015**, 30:25 ✓ 625 |
| S5 | 32:05 ✗ 45, 30:25 ✗ 45, 00:15 ✗ 475 | 00:15 ✓ 5, 30:25 ✓ 315, 31:45 ✓ 335 |
| S6 (결론) | — | 06:55 ✗ 235, 00:15 ✗ 15, 18:55 ✓ 555 |

- 이미지 검색(VLM2Vec)은 섹션의 이미지 질의로 독립적으로 이루어져서 텍스트 근거의 시간대와 묶여 있지 않습니다(코드).
- B는 텍스트 근거와 10분 이상 떨어진 이미지도 인용했습니다. **인용됐다고 그림이 그 문장의 장면과 맞는다는 보장은 없으며, 사람이 확인하지 않았습니다.**

**프롬프트 크기**
- writer 입력: A 2,526–3,154토큰, B 2,547–3,217토큰
- writer 출력: A 614–1,121토큰(35.7–66.5초), B 374–794토큰
- 근거를 늘리면 프롬프트와 지연이 함께 늘어납니다.

### 2.3 선택지

| ID | 방법 | 장점 | 단점·위험 |
|---|---|---|---|
| A | 현행 유지 | 변경 없음 | 사소한 triple과 시간이 동떨어진 이미지가 프롬프트를 차지함 |
| B | semantic k 축소(예: 4→2) | 프롬프트 감소. 다만 항목당 ~10단어라 효과는 작음 | 유용한 규칙 triple도 잃을 수 있음 |
| C | semantic 경량 필터: 사소한 술어(`can`, `wears`, `has colors`, 동어반복 등) 제거 + 섹션 내 중복 제거 | LLM 호출 없음 | 규칙 목록이 도메인 의존적(관제 도메인에서 다시 정해야 함) |
| D | 이미지를 텍스트 근거 구간 근처로 제한(±Δ초) 또는 episodic 구간에서 프레임 직접 선택 | 그림과 문장의 시간이 맞음 | 시각적으로만 드러나는 장면을 놓칠 수 있음. Δ를 정해야 함 |
| E | 이미지 k 축소 | 프롬프트 감소(캡션 ~90단어) | 그림 수 감소(결정 3에서 그림은 필수가 아님) |
| F | 4개 단위 활성화 후 재측정 | 원래 설계 조건으로 평가 | 결정 1(사전 인덱싱) 선행 필요 |

### 2.4 한계 (결정 전에 알아야 할 것)
1. **10sec 단위만 썼습니다.** 30sec/3min/10min 근거가 들어가면 episodic의 구성과 길이가 바뀝니다. → 결정 1이 먼저 필요합니다.
2. **표본이 작습니다.** 영상 1개, 보고서 2건이고, 샘플링 생성이라 실행마다 다릅니다(§2.2에서 순위별 경향이 A와 B에서 달랐음).
3. **인용 = 유용성이 아닙니다.** 이미지 인용률은 47%에서 89%로 올랐지만, 시간이 크게 떨어진 이미지도 인용됐습니다.
4. **semantic triple에는 시간이 없어** 규칙 검사의 시간 검증 대상이 아닙니다.
5. **이미지 검색은 텍스트 근거와 독립적**이라 시간 정렬이 보장되지 않습니다.
6. **근거 수를 바꾸면 LLM 호출 수가 아니라 프롬프트 길이가 바뀝니다.** 검색의 LLM 호출(L1 1회)은 그대로이고, writer 입력 토큰과 지연이 변합니다.
7. **결론 섹션도 자기 근거를 새로 검색합니다.** 근거 구성을 바꿔도 결론의 인용 불일치(P11)는 해결되지 않습니다(C0로 일부 완화 기대).

### 2.5 권장
1. **결정 7은 결정 1(사전 인덱싱) 이후에 확정**하기를 권장합니다.
2. 그 전에 할 수 있는 저위험 작업: 이미지-텍스트 시간 거리를 validation 정보로 기록합니다(출력은 바꾸지 않음).
3. 실험 후 선택 후보: **D(이미지 시간 정렬)**와 **C(semantic 경량 필터)**. B·E는 프롬프트 절감 효과가 작습니다.

---

## 3. 실험 설계 (결정 4 효과 확인 + 결정 7 결정용)

| 항목 | 내용 |
|---|---|
| 대상 | Video-MME long 영상 3–5개 × 실행 2–3회(샘플링 편차 측정) |
| 조건 | 4개 단위 캐시(사전 인덱싱 후), L1, 현재 템플릿(규칙 4·5·6, 결론, 번역)<br>결정 4: C0 `written` vs `deep_reporter`<br>결정 7: §2.3의 (A) 현재 / (B) semantic 2 / (C) semantic 필터 / (D) 이미지 시간 제한 |
| 측정 | 섹션 안 최대 문단 유사도 분포(R3의 임계값 τ 근거), 섹션 간 유사 문장 수, 유형별·순위별 인용률, 이미지-텍스트 시간 거리, 근거 검사 지적 수(결론 별도), writer 입력 토큰과 지연, 사람이 표본으로 확인한 그림-문장 일치율 |
| 비용 (실측 기준) | 보고서 1건 = LLM 1 + 3×섹션 수 + 번역 섹션 수(6섹션이면 25회). B 실측 494.4초(생성 261.5 + 번역 231.8). 번역을 끄면 실험 시간을 줄일 수 있음 |
| 판정 기준 예 | 근접 중복 문단 쌍이 실행의 20% 이상에서 나오고, 정상 쌍 최댓값과 τ 사이에 0.3 이상 여유가 있으면 R3 도입. 결론 섹션 지적 수가 C0로 줄지 않으면 결론 처리 방식을 별도로 검토 |
