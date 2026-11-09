# 영상 3개로 따라가 보는 보고서 생성 파이프라인 — 단계별 결과와 이슈 이력

- 작성: 2026-10-26 (컨테이너 시계 UTC). 미팅 보고와 튜토리얼용.
- 목적: 질의 하나가 들어와 보고서가 나오기까지 각 단계(planning → query 생성 → retrieval → writer → 합성·후처리·검증)에서 **실제로 무엇이 들어가고 무엇이 나왔는지**를 영상 3개의 실제 실행 기록으로 보여 주고, 지금까지의 이슈와 대응 결과를 정리한다.
- 근거: 이 문서의 수치와 예시는 모두 아래 파일을 직접 읽거나 다시 계산한 값이다. 코드에서 확인한 사실은 (코드), 로그·출력에서 잰 값은 (실측), 근거 원문과 사람이 대조한 것은 (대조), 확인하지 못한 추정은 (가설)로 표시한다.
- 더 자세한 문서: 구조와 상태는 `DESIGN_AND_STATUS.md`, 단계별 설명은 `REPORT_PIPELINE.md`, 이슈 상세는 `REPORT_ISSUES_AND_FIXES.md`.

---

## 0. 먼저 알아 둘 것

### 0.1 예시로 쓴 실행

| 항목 | 값 |
|---|---|
| 실행 | `outputs/p9p19_check_20261025_141401/` (2026-10-25 14:14–14:32, P9·P19 수정 확인 실행, `DESIGN_AND_STATUS.md` §9.16) |
| 보고서 | 영상 3개 × 같은 조건 3회(r1–r3) = 9건. 이 문서는 **각 영상의 r1**을 단계별 예시로 쓰고, 9건 전체 값은 따로 표시한다 |
| 코드 상태 | 커밋 `baf08d8`(2026-10-25 14:14:01) 시점. **2026-10-26 변경(`61f3286`: 영상 끝 근거 txt0, "loop suspected" 기준, 결말 검사 오탐 수정)은 이 실행에 들어 있지 않다** |
| 질의 | `Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.` (checklist 없음) |
| LLM | Qwen3-VL-8B-Instruct, `local_llm_server.py`(transformers), 서버 출력 상한 `max_tokens_cap` 3,072. 샘플링 생성이라 같은 조건에서도 결과가 달라진다(temperature 0.7, top_p 0.8, top_k 20, 모델 기본값) |
| 검색 | `videorag_retriever_service.py`, episodic 필터 **L1**, 4개 단위(10sec/30sec/3min/10min) 캐시 |
| 보고서 설정 | `text_topk` 20, `image_topk` 10, Deep-Reporter filter 노드 **끔**, 앞 섹션 맥락 C0(`written`), 섹션 상한 6, 번역 끔 |
| 배치 | GPU 4–7에 묶음 4개(묶음마다 LLM 서버 1 + 검색 서비스 1). r1 세 건은 묶음 0·1·2(GPU 4·5·6)에서 동시에 실행 |

출력 파일(보고서 폴더마다):

| 파일 | 내용 |
|---|---|
| `report_raw.md` | Deep-Reporter가 돌려준 원본(섹션별 `[citation:txtN]` 그대로, 반복 제거 전) |
| `report.md` | 최종 보고서(전역 번호 `[n]`, References, 그림. 반복 문장 제거 후) |
| `report.json` | 섹션별 설명·checklist·검색어·검색 근거 전체·본문(반복 제거 후), References, 그림 |
| `validation.json` | 상태(passed/failed), 오류·경고, 시간, 규칙 근거 검사, 반복 제거, 결말·시작 검사, 이미지-텍스트 시간 차 |
| `frames/` | 인용된 프레임 이미지 |

단계별 원자료: Deep-Reporter 세션 로그 `dr_logs_s<i>/longgen_sessions_20261025.jsonl`(planner·query·writer의 입력 프롬프트와 출력 전문), LLM 서버 로그 `llm_server_s<i>_gpu<g>.log`(호출마다 프롬프트·출력 토큰, 종료 사유, 시간), 검색 서비스 로그 `service_s<i>_gpu<g>.log`(요청마다 후보 수, 필터 동작, 근거 수, 시간).

### 0.2 영상 3개

| 영상 | 내용(10min 캡션 기준) | 길이(10sec 캡션 끝) | 실제 마지막 장면(10sec 캡션) |
|---|---|---|---|
| `-QuCz7kxBr8` | 남성 6명이 야외 농구장에서 바이럴 스포츠 가젯 12개를 시험 | 00:37:37 | 37:30–37:37 엔드 스크린 "Thank you for watching", "DON'T FORGET TO SUBSCRIBE!" |
| `0RxMZBLeqRI` | 로마(집시)의 기원·차별·박해 역사 영상 | 00:30:32 | 회전하는 지구본과 국기 격자 후 암전 |
| `54k2g9ddy4M` | CBC 뉴스 꼭지 모음(홍역, 항공 요금, Montfort 병원 신원 오인, 수영선수 Liendo, First Nation 학교 화재, 반려동물 심령술사 등) | 00:45:14 | 공항 체크인 장면 후 CBC 로고 검은 화면 |

### 0.3 용어: actor / critic / synthesis는 코드의 어디인가

Deep-Reporter와 우리 코드에는 `actor`, `critic`이라는 이름의 모듈이 **없다**(전체 트리 검색 (코드)). Deep-Reporter README는 자신을 "planning, multimodal retrieval, relevance filtering, and incremental synthesis"를 맡는 에이전트들로 설명한다. 질문에 쓰인 용어를 실제 구성요소에 대응시키면 다음과 같다.

| 질문의 용어 | 실제 구성요소 | 이번 실행에서 |
|---|---|---|
| planning (outlining) | Deep-Reporter `planner_node` + 우리 planner 템플릿(영상 개요 포함) | LLM 1회 |
| query 작성 | `query_generation_node` + 우리 query 템플릿 | 섹션당 LLM 1회 |
| retrieval | `search_node`(HTTP) → 우리 검색 서비스(WorldMM episodic·semantic·visual) | 섹션당 text·image 요청 각 1회. text 요청 안에서 **L1 필터 LLM 1회** |
| actor | 섹션 본문을 쓰는 `section_writing_node`(writer) | 섹션당 LLM 1회 |
| critic | ① Deep-Reporter `filter_node`(LLM이 근거의 쓸모를 판정) — **꺼 둠**(D9). ② 그 역할은 검색 단계의 WorldMM L1 필터(후보 중 관련 근거 8개를 LLM이 고름)가 대신한다. ③ 생성 뒤의 규칙 검사(근거 대조, 반복, 결말·시작)는 **LLM을 쓰지 않고 경고만** 남긴다. writer에게 되돌려 고치게 하는 비평-수정 고리는 없다 | ①은 0회, ②는 섹션당 1회, ③은 0회 |
| synthesis | 섹션을 차례로 쓰며 앞 섹션 맥락을 넘기는 것(`_update_context`, 우리는 C0로 교체) + `combine_node`(섹션을 `\n\n`으로 이어 붙임) + 우리 후처리(인용 → References·그림) | LLM 0회. 보고서 전체를 다시 다듬는 refine 단계는 Deep-Reporter에 **없다**(코드·논문) |

---

## 1. 전체 흐름

```
[사전 준비, 영상마다 1회]
  WorldMM 전처리(이미 완료): 10sec 캡션 → 30sec/3min/10min 요약, semantic triple, visual 임베딩
  prebuild_episodic_index.py: 4개 단위 HippoRAG 그래프 → cache/episodic/<vid>/

[보고서 1건 = run_report.py]
  ① 사전 확인(LLM·검색 서비스 health, 영상 불러오기, 템플릿 계약)
  ② 템플릿 교체(planner·query·writer) + C0 맥락 교체   ← domain_templates.py
  ③ Deep-Reporter 그래프(파일 수정 없음)
       planner ─→ [ query 생성 → search(text, image) → (filter: 끔) → writer ] × 섹션 수 ─→ combine
                              │
                              └→ 검색 서비스: episodic(L1 필터) + semantic + visual
  ④ 후처리: 반복 문장 제거 → 결말·시작 검사 → 인용 → References·그림 → 규칙 근거 검사
  ⑤ 사후 검증 → validation.json, report.md
```

LLM 호출 수는 섹션 수 N일 때 **1 + 3N**이다(planner 1, 섹션마다 query 1 · L1 필터 1 · writer 1). 세 보고서 모두 N = 6이라 19회였다(서버 로그 (실측)).

| 영상 (r1) | 생성 시간 | planner | query 6회 합 | L1 필터 6회 합 | writer 6회 합 (생성 시간 중 비율) | 검색 서비스 text 6회 합 / image 6회 합 |
|---|---|---|---|---|---|---|
| `-QuCz7kxBr8` | 319.7초 | 35.4초 | 23.9초 | 29.4초 | 198.0초 (62%) | 43.2초 / 6.5초 |
| `0RxMZBLeqRI` | 403.8초 | 37.4초 | 23.2초 | 33.5초 | 280.4초 (69%) — 1회가 상한에 걸려 133.9초 | 44.7초 / 5.4초 |
| `54k2g9ddy4M` | 346.3초 | 43.0초 | 25.4초 | 28.0초 | 217.6초 (63%) | 39.8초 / 7.6초 |

- L1 필터 시간은 검색 서비스 text 시간 안에 포함된다.
- 후처리·검증은 0.03–0.04초다.
- 시간의 대부분은 writer다.

---

## 2. 단계 0 — 사전 준비: 영상 메모리

검색이 읽는 메모리는 보고서 생성 전에 만들어 둔다(LLM 사용, GPU).

| 메모리 | 만드는 방법 | 검색 방법 | 시간 정보 |
|---|---|---|---|
| episodic | 10sec 캡션(프레임 + Whisper 자막) → LLM 요약으로 30sec/3min/10min 생성(WorldMM 전처리). 단위마다 OpenIE triple로 HippoRAG 그래프 구성(`prebuild_episodic_index.py`) | 그래프 검색(fact 점수 → PPR) | 있음 |
| semantic | 10sec OpenIE triple을 묶어 영상 전체 수준의 triple로 통합(WorldMM) | 임베딩·PPR | **없음** |
| visual | 10초 구간마다 VLM2Vec 비디오 임베딩(WorldMM) | 텍스트 질의와 cosine 유사도 | 있음(10초 구간) |

세 영상의 규모(검색 서비스 로그 (실측)):

| 영상 | 캡션 수 10sec/30sec/3min/10min | 10sec 그래프 노드 / 엣지 | semantic triple | visual 구간 |
|---|---|---|---|---|
| `-QuCz7kxBr8` | 226 / 76 / 13 / 4 | 1,277 / 10,596 | 153 | 226 |
| `0RxMZBLeqRI` | 184 / 62 / 11 / 4 | 2,290 / 11,507 | 405 | 184 |
| `54k2g9ddy4M` | 272 / 91 / 16 / 5 | 2,123 / 11,736 | 725 | 272 |

- 4개 단위 캐시는 이 세 영상만 있다(2026-10-25 C-1, LLM 호출 430회, 27.4분). 나머지 47개 영상은 아직 없다(C-7, 사용자 지시 전 미실행).
- `0RxMZBLeqRI`의 10min 캡션 중 00:00–10:00과 10:00–20:00 두 개는 전처리에서 2,048토큰에 잘렸다(I22, 재생성 보류). 이 캡션들은 planner 개요와 검색 근거로 쓰인다.

---

## 3. 단계 1 — 실행 준비

`run_report.py`가 Deep-Reporter를 부르기 전에 하는 일이다(코드).

1. **사전 확인**: LLM 서버와 검색 서비스의 `/health`를 확인하고, 검색 서비스에 영상을 불러오게 한다(캐시가 불완전하면 409로 거부 → exit 2). 템플릿 계약도 검사한다. 이번 실행에서는 1.1–1.2초 걸렸다.
2. **LLM 라우팅**: Deep-Reporter는 설정 dict의 키·URL을 버리므로(I6) 환경변수 `QWEN_BASE_URL`·`QWEN_API_KEY`로 넣고, 실제로 그 주소로 연결됐는지 확인한다.
3. **템플릿 교체**(`domain_templates.apply_templates`): Deep-Reporter의 웹 리포트용 프롬프트 3개(planner·query·writer)를 영상용 템플릿으로 **실행 중에만** 바꾸고 끝나면 되돌린다. Deep-Reporter 파일은 고치지 않는다. 템플릿에 필요한 자리표시자와 출력 마커가 없으면 실행 전에 멈춘다.
4. **C0 맥락 교체**(`apply_written_context`): 다음 섹션에 넘기는 "앞 섹션 요약"을, 원래의 "섹션 설명 + 본문 앞 100자" 대신 **앞 섹션에서 실제로 쓴 문장**(제목 + 단락 첫 문장, 인용 번호 제거, 전체 3,600자 상한)으로 바꾼다. LLM 호출은 늘지 않는다.
5. **실제 영상 끝 시각**: 10sec 캡션의 마지막 `end_time`을 읽어 writer 규칙 7에 넣는다(10min 캡션은 구간 경계 40:00, 40:00, 50:00에서 끝나므로 쓰지 않는다).

---

## 4. 단계 2 — Planning (outline 생성)

### 4.1 입력

- 사용자 질의 + checklist(이번에는 없음).
- **영상 개요**: 그 영상의 10min 캡션 전체를 `[HH:MM:SS-HH:MM:SS] 요약` 형태로 넣는다(D3). planner가 영상 내용을 모르면 근거 없는 섹션을 만들기 때문이다.
- 규칙(우리 템플릿 요약): 섹션 3–6개(결론 포함), 영상에 있는 내용만, 대체로 시간 순서, 섹션 설명 2–4문장에 대략의 시간 범위 포함, checklist 3–5개, **마지막 섹션은 `Conclusion:`으로 시작하는 짧은 결론**.

입력 예(`-QuCz7kxBr8`, 프롬프트 23,899자 = 5,219토큰):
```
**Video overview** (timestamped summaries of consecutive ~10-minute segments, ...):
[00:00:00-00:10:00] **Six men—Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player—gather on a sunny
outdoor basketball court to test 12 viral sports gadgets, splitting into two teams of three. ...
```

### 4.2 출력

JSON `{"outline": [{"section_description", "sectional_checklist"}, ...]}`. 예(`-QuCz7kxBr8` 섹션 1):
```json
{"section_description": "This section introduces the six main participants—Chris, Zach, Cass, James, Mitchell, and an
  unnamed sixth player—and establishes the setting: a sunny outdoor basketball court. It describes how they split into
  teams and begin testing 12 viral sports gadgets, starting with the SPORTS DRIBBLE SPECS. ...",
 "sectional_checklist": ["List the six main participants and how they are introduced",
                         "Describe the outdoor basketball court setting and weather",
                         "Note the first gadget tested and the rules of its challenge"]}
```

### 4.3 세 영상의 결과

| 영상 | 프롬프트 / 출력 토큰, 시간 | 섹션 | 섹션 주제(순서대로) |
|---|---|---|---|
| `-QuCz7kxBr8` | 5,219 / 764, 35.4초 | 6 | 참가자·장소 → Dribble Stick·Straight Shooter Strap → Flick Glove·Shot Coach → Silly String 게임·수비 훈련 → 최종 점수·마무리 → 결론 |
| `0RxMZBLeqRI` | 6,966 / 811, 37.4초 | 6 | 도입부(면책 문구, 몽타주) → 역사·문화적 틀 → 과학적 배제·낙인 → 기원·오인(13세기 지도) → 나치·공산 정권의 박해 → 결론 |
| `54k2g9ddy4M` | 6,271 / 904, 43.0초 | 6 | 홍역 재유행 → 미국 홍역·몬트리올 사망 → Montfort 병원 신원 오인 + Liendo 금메달 → Liendo의 여정 → First Nation 학교 화재·복구 → 결론 |

### 4.4 관찰

- **형식은 지켰다** (실측): 세 영상 모두 섹션 6개이고 마지막이 `Conclusion:`이다. planner 파싱 실패로 섹션 1개가 되는 fallback은 없었다.
- **planner의 시간 표기가 개요와 맞지 않는 경우가 있다** (대조, `54k2g9ddy4M`):
  - 섹션 2 설명은 "(00:10:00-00:20:00)"이라고 했지만 다루는 내용(미국 홍역, 몬트리올 사망)은 개요 00:00–10:00에 있다. 개요의 10:00–20:00 꼭지는 항공 요금이다.
  - 항공 요금(10:00–20:00 개요)과 반려동물 심령술사(3min 캡션 기준 41:30 이후) 꼭지는 outline에 없다. 학교 화재·복구 내용은 3min 캡션 기준 36:00–42:00에 있어, 섹션 5의 "(00:40:00-00:50:00)"은 일부만 맞다.
- **planner가 개요의 세부를 섹션 설명·checklist에 넣고, 그것이 본문으로 넘어간다** (P5):
  - `54k2g9ddy4M` 섹션 1 checklist의 "current vaccination levels at 79%"는 10min 개요("79% of seven-year-olds vaccinated by 2021")에서 왔다.
  - 그 섹션의 검색 근거에는 79가 없는데도 본문이 "79% [citation:txt1]"로 썼고, 규칙 검사가 `unsupported`로 표시했다.
- **섹션이 영상 앞부분에 몰릴 수 있다** (실측, `0RxMZBLeqRI`): 섹션 1–4가 인용한 근거 구간의 중앙값이 모두 00:00:25–00:01:20이다. 10sec·30sec·3min 근거로는 03:00–06:00, 09:00–21:00, 24:30–27:00을 어느 섹션도 인용하지 않았다(§8.2). 이 영상은 10min 개요 두 개가 잘려 있어(I22) 영향이 있을 수 있다(가설).

---

## 5. 단계 3 — Query 생성

### 5.1 입력과 규칙

- 질의, 현재 섹션 설명과 checklist, 앞 섹션 요약(C0)을 넣는다.
- 템플릿 지시
  - `text_queries` 2–3개: 사건·행동·인물·물체·발화를 짧은 키워드형으로 쓴다.
  - `image_queries` 1–2개: 장면의 **겉모습**을 한 문장으로 쓰고, 차트·도표는 요청하지 않는다.
  - 앞 섹션과 겹치는 질의는 피한다.

### 5.2 출력 예와 결과

`-QuCz7kxBr8` 섹션 1:
```json
{"text_queries": ["six players introduced: Chris, Zach, Cass, James, Mitchell, and sixth unnamed player",
                  "first gadget tested: SPORTS DRIBBLE SPECS, rules explained for challenge"],
 "image_queries": ["six people standing on a sunny outdoor basketball court, wearing casual sportswear, ready to play"]}
```

| 영상 | 프롬프트 토큰(섹션 1 → 6) | 출력 토큰 | 시간 | 질의 수 |
|---|---|---|---|---|
| `-QuCz7kxBr8` | 438 → 1,103 | 81–96 | 3.7–4.5초 | text 2–3, image 1 |
| `0RxMZBLeqRI` | 449 → 1,161 | 63–100 | 2.8–4.4초 | text 2–3, image 1 |
| `54k2g9ddy4M` | 472 → 1,183 | 80–104 | 3.6–4.8초 | text 3, image 1 |

- 프롬프트가 뒤 섹션으로 갈수록 길어지는 것은 C0 요약이 쌓이기 때문이다.
- 질의 파싱 실패로 섹션 설명을 그대로 검색어로 쓴 경우(fallback)는 없었다(검증 경고 없음).
- 관찰: 질의는 checklist 문구를 거의 그대로 옮긴다. 예: `"U.S. measles outbreak with 41 cases reported in 16 states centered at Manatee Bay Elementary"`. 그래서 planner가 개요에서 가져온 세부(수치·이름)가 검색어에도 들어간다.

---

## 6. 단계 4 — Retrieval

Deep-Reporter `search_node`는 섹션마다 우리 검색 서비스에 두 번 요청한다: `{query_list: text_queries, type: "text", topk: 20}`, 2초 쉬고 `{query_list: image_queries, type: "image", topk: 10}`. 응답의 `results`를 그 섹션의 근거로 그대로 저장한다(코드).

### 6.1 text 요청: episodic 8개 + semantic 4개

| 단계 | 하는 일 | LLM |
|---|---|---|
| ① 후보 모으기 | (질의 × 단위)마다 HippoRAG 그래프 검색(fact 점수 → PPR). 단위별 후보 수 10sec 3 / 30sec 3 / 3min 2 / 10min 1. WorldMM의 DSPy fact 필터는 뺀다(L1) | 0 |
| ② 병합 | 순위 기반 병합(RRF, k = 60). WorldMM 검색은 점수를 돌려주지 않기 때문이다(I12) | 0 |
| ③ **L1 필터** | 후보 전체를 WorldMM `multiscale_filter` 프롬프트에 넣고 "질문에 답하는 데 가장 관련 있는 캡션 ID 8개를 순서대로 JSON 배열로" 받는다. 질문은 그 섹션의 질의들을 `; `로 이은 것 | **1회** |
| ④ semantic | 질의마다 semantic triple 상위 5개 → RRF → 4개 | 0 |

| 영상 | 후보 수(섹션 1 → 6) | L1 필터 프롬프트 / 출력 토큰 | L1 필터 시간 | text 요청 시간 |
|---|---|---|---|---|
| `-QuCz7kxBr8` | 17, 22, 17, 25, 22, 26 | 8,661–12,112 / 66–74 | 4.4–5.5초 | 5.86–12.19초 |
| `0RxMZBLeqRI` | 19, 22, 23, 16, 20, 17 | 10,063–15,486 / 64–76 | 4.8–6.3초 | 5.77–11.34초 |
| `54k2g9ddy4M` | 18, 19, 24, 23, 18, 25 | 6,205–10,544 / 68–75 | 4.1–5.2초 | 5.31–9.87초 |

- 18건 모두 `episodic_filter: llm`(필터가 실제로 실행됨), 근거는 매번 episodic 8 + semantic 4 = 12개였다.
- 첫 요청이 가장 느리다(9.87–12.19초).

근거 항목 형식(writer는 `content`를 본다):
```
[00:00:00-00:00:30 | episodic 30sec] A group of six men—Chris, Zach, Cass, James, and Mitchell—gather on a sunny ...
[video-level knowledge | semantic] (challenge, penalizes least baskets with, 100 sit-ups)
```

episodic 근거 48개(섹션 6개 × 8)의 단위 구성 (실측):

| 영상 | 10sec | 30sec | 3min | 10min |
|---|---|---|---|---|
| `-QuCz7kxBr8` | 13 | 20 | 10 | 5 |
| `0RxMZBLeqRI` | 13 | 25 | 6 | 4 |
| `54k2g9ddy4M` | 17 | 20 | 6 | 5 |

관찰 (실측·대조)
- **같은 근거가 여러 섹션에 다시 나온다.**
  - `0RxMZBLeqRI`의 30sec 캡션 00:00:00–00:00:30은 6개 섹션 중 5개(1·2·3·4·6)의 근거에 들어 있다.
  - `-QuCz7kxBr8`의 10min 00:00–10:00은 섹션 1·2·3에 들어 있다.
- **30sec·3min·10min 요약에는 구간 내부 표현과 해석 표현이 많다.**
  - `0RxMZBLeqRI` 근거의 다수가 "The video opens with …"로 시작한다. 그 30초·3분 구간의 시작이라는 뜻인데, 영상 전체의 시작으로 옮겨지는 문제가 있다(P19).
  - 해석 단서(suggesting, symbolizing, underscoring 등)가 든 근거의 비율은 수정 후 9건 기준 3min 28/29, 10min 12/12, 30sec 81/98, 10sec 13/82, semantic 1/128이다(P12, `DESIGN_AND_STATUS.md` §9.17).
- **semantic 근거는 사소한 것이 많다.** 예: `(player, can dribble, basketball)`, `(player, can gesture and talk to, another player)`. 쓸모 있는 것도 있다. 예: `(First Gypsy arrivals, mistaken for, Seljuk Turks by Byzantines)`.
  - 섹션별 인용 수(semantic 4개 중): `-QuCz7kxBr8` 1·0·0·2·1·1, `0RxMZBLeqRI` 0·0·0·1·0·1, `54k2g9ddy4M` 0·1·2·1·0·0.

### 6.2 image 요청: 프레임 3개

- 질의마다 VLM2Vec 유사도 상위 3구간을 RRF로 합치고(최대 4개), 구간 **중앙 프레임**을 jpg로 뽑는다.
- 캡션으로 같은 시각의 10sec 캡션을 붙인다. 이번에는 image 질의가 1개라 섹션마다 3장이었다. 요청당 0.81–1.52초.
- **이미지는 텍스트 근거와 따로 검색된다**(코드). 그래서 시간이 크게 떨어질 수 있다.
  - `-QuCz7kxBr8` 섹션 1(도입, 텍스트 근거 00:00–03:00)의 프레임은 00:34:45, 00:28:45, 00:28:55였다.
  - 세 보고서에서 인용된 이미지와 같은 단락 텍스트 근거의 시간 차 중앙값은 `-QuCz7kxBr8` 1,485초(최대 1,555), `0RxMZBLeqRI` 0초(최대 55), `54k2g9ddy4M` 0초(최대 95)였다(`validation.json` `image_time_alignment`).
- **writer는 이미지 픽셀을 보지 않는다.** Deep-Reporter writer는 텍스트 메시지만 보내고(`llm_utils.py`), 이미지는 `[Source imgN: <시간과 10sec 캡션>]` 문자열로만 들어간다(코드).

---

## 7. 단계 5 — Writer (actor)

### 7.1 입력

섹션 위치(예: `Section 2/6`, 첫·마지막 여부), 섹션 설명과 checklist, 앞 섹션 요약(C0)과 직전 섹션 마지막 부분, 근거 목록(`[Source txt1 begin] … [Source txt12 end]`, `[Source img1: …]` 3개), 그리고 우리 템플릿 규칙이 들어간다.

C0 요약 예(`-QuCz7kxBr8` 섹션 2의 writer 입력):
```
Already written in earlier sections (title, then the first sentence of each paragraph; citation numbers removed - they do
NOT refer to the evidence of the current section):
Section 1: Introduction to the Participants and Setting
- Six men—Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player—are introduced as the main participants in the video.
- The video's goal is established early: to test and evaluate the gadgets in a hands-on, competitive, yet lighthearted manner.
- The group's interaction remains informal and humorous, ...
```

writer 템플릿의 핵심 규칙(`domain_templates.py` `VIDEOMME_SECTION`):

| 구분 | 규칙 |
|---|---|
| Grounding 1–5 | 근거가 말하는 것만 쓴다(추측 금지). 사건 시각을 HH:MM:SS로 쓰되 지어내지 않는다. 충돌하면 세밀한 단위를 우선한다. 근거가 없으면 없다고 쓴다. 대체로 시간 순서로 쓴다 |
| Grounding 6 | 같은 섹션에서 반복하지 않는다. 앞 섹션에서 다룬 사실은 한 문장 이내로 쓴다(결론은 예외) |
| Grounding 7 | 30sec·3min·10min 요약 속 "the video opens/closes"는 **그 구간의** 시작·끝이다. 영상 전체는 00:00:00–<실제 끝>이고, 처음·마지막 몇 분에 닿는 근거로만 시작·결말을 쓴다 |
| 인용 | 문장마다 `[citation:txtN]`을 붙인다. 이미지는 `![](citation:imgN)`을 단독 줄로 쓰고, `[citation:imgN]`은 금지한다 |
| 결론 | `Conclusion:` 섹션은 100–250단어로, 앞 섹션 결과만 요약한다 |

- 이번 실행 뒤 2026-10-26에 writer 템플릿에 "End of the Video" 블록이 추가됐다(영상 마지막 약 60초의 10sec 캡션을 `txt0`으로 보여 주고 마지막 섹션만 인용). 이 블록은 GPU 실행으로 아직 확인하지 않았다(§10.1 P19).

### 7.2 출력 예

`-QuCz7kxBr8` 섹션 1의 `report_raw.md` 원문:
```
# Introduction to the Participants and Setting

Six men—Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player—are introduced as the main participants in the
video. They gather on a sunny outdoor basketball court, dressed in athletic wear and holding basketballs near a hoop and
trees [citation:txt2]. ... The court features a painted "HYPE" logo and a basketball hoop, reinforcing the casual,
recreational environment [citation:txt12][citation:img1].
```

이 예에서 확인되는 것(대조):
- 첫 문장에 인용이 없다.
- 마지막 문장의 `txt12`는 semantic triple `(player, can gesture and talk to, another player)`로, "HYPE" 로고를 뒷받침하지 않는다.
- `img1`은 금지된 `[citation:imgN]` 형식이고(P1), 가리키는 프레임은 00:34:45의 수비 훈련 장면이다(P14).

### 7.3 세 영상의 writer 결과

| 영상 | 프롬프트 토큰 | 출력 토큰 | 섹션별 단어 수(반복 제거 후, 1 → 6) | 인용한 텍스트 근거 수(12개 중, 섹션 1 → 6) |
|---|---|---|---|---|
| `-QuCz7kxBr8` | 4,577–6,125 | 365–1,102 | 403, 585, 764, 727, 329, 253 | 8, 8, 7, 8, 5, 4 |
| `0RxMZBLeqRI` | 4,936–7,111 | 423–**3,072(상한)** | 361, 535, 529, 483, 927, 294 | 4, 3, 4, 5, 7, 5 |
| `54k2g9ddy4M` | 3,034–6,198 | 475–1,026 | 491, 623, 716, 439, 602, 341 | 6, 6, 10, 9, 8, 8 |

- **반복 루프** (실측, `0RxMZBLeqRI` 섹션 5)
  - writer가 "The video does not show any footage of Roma persecution under communist regimes beyond the title card "Communism, Chapter VII" at 00:24:00 [citation:txt2]." 한 문장을 **38번** 되풀이하다가 서버 상한 3,072토큰에서 133.9초 만에 문장 중간에서 끊겼다.
  - 원본 섹션 1,778단어 → 같은 문장 제거 후 927단어.
  - 상한이 없던 C-5에서는 같은 유형의 루프가 8,192토큰까지 약 6분 갔다(P9).
- **결론 길이**: `54k2g9ddy4M` 결론이 341단어로 지시(100–250)를 넘어 경고가 났다.
- **이미지 인용 형식 오류** `[citation:imgN]`: 1 / 2 / 5개. 후처리가 모두 그림으로 바꿨다.

---

## 8. 단계 6 — Synthesis, 후처리, 검증

### 8.1 Deep-Reporter 안에서

- 섹션을 하나 쓸 때마다 `_update_context`가 다음 섹션용 요약을 만든다(우리는 C0로 교체).
- 모든 섹션이 끝나면 `combine_node`가 섹션 본문을 `\n\n`으로 이어 `final_article`(= `report_raw.md`)을 만든다. 다듬기·재작성은 없다(코드).

### 8.2 우리 후처리 (`run_report.py` → `grounding_postprocessor.py`, LLM 0회)

| 순서 | 처리 | 결과 예(r1 세 건) |
|---|---|---|
| 1 | (2026-10-26 추가, 이번 실행에는 없음) 섹션이 `txt0`을 인용하면 영상 끝 근거를 그 섹션 근거 목록에 붙이고 번호를 바꾼다 | — |
| 2 | **같은 문장 제거**: 섹션 안에서 똑같은 문장의 두 번째 이후를 지우고, 섹션이 문장 중간에서 끝나는지 기록한다 | `0RxMZBLeqRI` 섹션 5: 37개 제거, 문장 중간 끝. `54k2g9ddy4M` 섹션 1: 1개 제거 |
| 3 | **결말·시작 서술 검사**: "the video ends/closes/opens…" 문장의 인용 근거가 영상 끝·처음에서 120초 넘게 떨어지면 `ending_early`/`opening_late`, 시간 있는 근거가 없으면 `*_unverifiable` | 아래 §8.3 |
| 4 | **인용 변환**: `[citation:txtN]` → 보고서 전체 번호 `[n]` + References(episodic은 시간 구간, semantic은 "no timestamp"). `![](citation:imgN)`·`[citation:imgN]` → 그림(프레임 복사 + 시간 + 캡션). 같은 근거·프레임은 번호 하나 | References 35 / 22 / 42개, 그림 3 / 7 / 5개, 잘못된 번호 `[?]` 0 |
| 5 | **규칙 근거 검사**: 문장의 따옴표 문구·숫자·HH:MM:SS가 그 문장이 인용한 근거에 있는지 본다. 없으면 `unsupported`, 같은 섹션의 다른 근거에 있으면 `miscited`, 인용이 없으면 `uncited`. "근거가 X를 보여 주지 않는다"는 절 안의 토큰은 `absence`로 제외 | 아래 표 |
| 6 | **이미지-텍스트 시간 차** 기록(경고 없음) | §6.2 |
| 7 | **사후 검증**: 오류(LLM 실패 문자열, 빈 근거, `[?]`, 프레임 누락, planner fallback)가 있으면 `failed`/exit 1. 품질 지적은 **경고**로만 | 세 건 모두 `passed`, exit 0 |

변환 예(`report.md`):
```
... The court features a painted "HYPE" logo and a basketball hoop, reinforcing the casual, recreational environment [4](Figure 1).

![Figure 1 (00:34:45)](frames/-QuCz7kxBr8_00344000.jpg)
*Figure 1. Frame at 00:34:45 (clip 00:34:40–00:34:50). On an outdoor basketball court ... prepares to defend ...*
...
# References
[1] 00:00:00–00:00:30 · episodic 30sec: A group of six men—Chris, Zach, Cass, James, and Mitchell—gather on a sunny ...
[4] Video-level knowledge (semantic memory, no timestamp): (player, can gesture and talk to, another player)
```

### 8.3 검사 결과 (r1 세 건, `validation.json`)

| 항목 | `-QuCz7kxBr8` | `0RxMZBLeqRI` | `54k2g9ddy4M` |
|---|---|---|---|
| 문장 | 123 | 116 | 122 |
| 검사 토큰이 있고 인용이 붙은 문장 | 39 | 27 | 26 |
| unsupported / miscited / uncited / absence | 0 / 5 / 12 / 0 | 2 / 0 / 13 / 4 | 2 / 1 / 4 / 0 |
| 결말·시작 검사 | ending_early 2, ending_unverifiable 3 | ending_early 1(**오탐**, 10/26 수정), opening_unverifiable 1, ending_unverifiable 1 | ending_early 2 |
| 해석·추정 단서(추정/해석/평가), 근거에서 옮김/writer 추가/인용 없음 (§9.17 도구) | 3/5/20, 18/5/5 | 4/28/28, 28/14/18 | 1/9/45, 36/11/8 |
| 섹션 순서 역전(F1) / 섹션 안 시각 역행(F2) | 0 / 1 (섹션 3, 19:30 → 18:00) | 0 / 0 | 0 / 0 |
| 10sec·30sec·3min 근거로 어느 섹션도 인용하지 않은 3분 이상 구간 | 10:30–18:00, 21:00–25:00, 25:30–36:00 | 03:00–06:00, 09:00–21:00, 24:30–27:00 | 04:50–20:30, 22:00–28:30, 33:00–36:00, 42:00–45:14 |

마지막 행은 각 섹션이 실제로 인용한 근거 구간의 합집합에서 계산했다. 10min 요약을 포함하면 `-QuCz7kxBr8`은 10:30–18:00, 21:00–25:00, 25:30–36:00, `0RxMZBLeqRI`는 10:00–21:00, 24:30–27:00, `54k2g9ddy4M`은 42:00–45:14만 남는다.

검사가 잡은 실제 문제 예(대조)
- **결말 오인 (P19)**
  - `-QuCz7kxBr8` 섹션 3·4: "The video closes with a close-up of the Shot Coach device …". 인용 근거는 18:00–21:00 3min 요약이 **자기 구간의 끝**을 그렇게 쓴 것이고, 실제 영상은 37:37 엔드 스크린으로 끝난다. → `ending_early`
  - `54k2g9ddy4M` 결론: "The video concludes by returning to the themes of recovery and legacy …". 인용 근거가 40:00에서 끝나고, 실제 끝은 45:14의 공항 장면과 CBC 로고다. → `ending_early`
- **결말을 맞게 쓴 예**: `-QuCz7kxBr8` 결론 마지막 문장 "The video ends at 00:37:37 with a static screen displaying "Thank you for watching" …"은 10sec 캡션과 맞는다. 다만 이 문장이 인용한 근거(37:00–37:30, 37:20–37:30, semantic)의 구간에 37:37이 들어 있지 않아 `miscited`로 표시됐다(같은 섹션의 36:00–39:00·30:00–40:00 근거에는 들어 있음).
- **시작 표현 오인**: `0RxMZBLeqRI` 섹션 5 "At 00:23:40, the video begins with a person in a dark hooded garment holding a knife …". 10sec 캡션의 "The video begins with"를 옮긴 것이다. → `opening_unverifiable`
- **검사 오탐**: `0RxMZBLeqRI` 섹션 1 "the final shot of the video's opening montage"(소유격)를 결말 서술로 잡았다. 2026-10-26에 고쳤다(CPU 테스트).
- **planner 설명에서 온 수치 (P5)**: `54k2g9ddy4M` 섹션 1 "79%"(§4.4). 결론 "41 confirmed cases"도 결론 근거에는 없어 `unsupported`다(P11).

### 8.4 같은 조건 9건 전체 (r1–r3, `batch_summary.json`)

| 영상 | 생성 시간 | 상한에 걸려 끊김 | 제거된 반복 문장 | ending_early | 규칙 검사 unsupported / miscited / uncited |
|---|---|---|---|---|---|
| `-QuCz7kxBr8` r1·r2·r3 | 319.7 / 296.9 / 331.5초 | 0 / 0 / 0 | 0 / 10 / 0 | 2 / 0 / 4 | 0/5/12, 1/1/3, 1/2/7 |
| `0RxMZBLeqRI` r1·r2·r3 | 403.8 / 417.5 / 325.4초 | **133.9초 / 130.5초** / 0 | 37 / 39 / 0 | 1(오탐) / 0 / 0 | 2/0/13, 1/1/3, 1/6/12 |
| `54k2g9ddy4M` r1·r2·r3 | 346.3 / 335.7 / 361.7초 | 0 / 0 / 0 | 1 / 3 / 2 | 2 / 1 / 1 | 2/1/4, 1/1/7, 0/4/8 |

9건 모두 `passed`, exit 0이다. 같은 조건이라도 결과가 크게 다르다(샘플링). 상한 도달 2건은 모두 `0RxMZBLeqRI` 섹션 5다.

---

## 9. 지금 파이프라인이 하는 것과 못 하는 것 (세 영상에서 확인)

| 잘 되는 것 | 근거 |
|---|---|
| 질의 → outline → 섹션별 검색 → 본문 → References·그림까지 자동으로 끝난다(영상당 약 5–7분, LLM 19회) | 9/9 `passed` |
| 형식 요구(섹션 상한, 결론 섹션, 인용 번호 유효성)를 지킨다 | `[?]` 0, planner·query fallback 0 |
| 모든 인용을 시간 구간·프레임으로 되짚을 수 있다 | References, 그림 |
| 루프가 나도 시간이 묶이고(약 6분 → 약 2분), 반복 문장이 보고서에서 빠지며 경고가 남는다 | §7.3, §8.4 |

| 남은 문제 | 세 영상에서의 모습 |
|---|---|
| 영상 전체의 흐름(결말·시작·시간 순서)을 틀리게 쓴다 | 구간 요약의 "closes/begins"를 영상 전체로 옮김, planner 시간 표기 오류, 큰 구간이 보고서에서 빠짐 |
| 해석·평가 표현이 많다 | 보고서당 28–60개(r1 기준). 다수는 30sec·3min·10min 요약 캡션에서 옮겨 온 것 |
| 인용이 붙어도 문장이 근거와 맞지 않을 수 있다 | semantic triple을 엉뚱한 문장에 인용, 이미지가 다른 시각의 장면 |
| writer 반복 루프가 여전히 생긴다 | 9건 중 2건(같은 영상의 같은 섹션) |
| 검증은 경고만 하고 고치지 않는다 | 9건 모두 `passed` |

---

## 10. 이슈 이력: 무엇이 문제였고 어떻게 다뤘고 결과는 어땠나

표기: ✅ 해결 / 🟡 부분 대응 / ⏳ 측정 대기 / ⛔ 미대응. 상세는 `REPORT_ISSUES_AND_FIXES.md`.

### 10.1 보고서 품질 문제 (P1–P19)

보고서 A(10/21 스모크, 10sec만), B(10/22 `run_report.py` 첫 실행, 10sec만), C-4(10/25, 4개 단위, 3건), C-5(10/25, C0 켬·끔 8건), 수정 후 확인(10/25, 9건), 현황 측정(10/26, 20건)에서 나온 것이다.

| # | 문제 | 대응 | 결과 (실측) | 상태 |
|---|---|---|---|---|
| P1 | 이미지 인용을 `[citation:imgN]`으로 씀 | writer 규칙 4 + 후처리에서 그림으로 변환(결정 3) | A 14개 중 8개 → B 19개 중 4개. 이번 r1 1/2/5개, 모두 변환 | ✅ (변환은 계속 필요) |
| P2 | 이미지가 있는데 안 넣은 섹션 | 의무화하지 않음(결정 3) | — | ✅ 정책 |
| P3 | 인용은 있으나 근거에 없는 수치·문구 | 규칙 근거 검사(LLM 0회, 결정 2) | A 대조 정밀도 약 78%(9건 중 7건 실제 오류). 재현율 미측정 | 🟡 감지만 |
| P4 | 다른 근거의 내용·시간을 인용 | 같은 검사의 `miscited` | 화자 뒤바뀜 같은 의미 오류는 못 잡음(C-4) | 🟡 감지만 |
| P5 | planner 설명의 세부가 근거 없이 본문으로 | 검사 경고, C0 | 이번에도 발생(`54k2g9ddy4M` "79%") | ⏳ |
| P6 | 다른 장면을 같은 사건으로 엮음 | 없음 | 감지 수단 없음 | ⛔ |
| P7 | 섹션 주제와 검색 근거가 안 맞음 | 없음 | "근거에 없다" 문장으로 나타남 | ⛔ |
| P8 | 시간 순서 섞임 | 측정 도구(2026-10-26) | 20건 중 섹션 순서 역전 3건(모두 실제), 섹션 안 시각 역행 14건 | ⛔ 측정됨 |
| P9 | 반복, **writer 반복 루프** | 규칙 6 + C0(결정 4) → 루프 발견 후 서버 상한 3,072 + 같은 문장 제거 + 경고(결정 16). 10/26 "loop suspected" 기준을 5회 이상 또는 끊김으로 | 루프 발생은 그대로(C-5 2/8, 수정 후 2/9). 루프 시간 약 6분 → 130–134초, 반복 문장 37·39개 제거, 경고 표시. 새 기준이면 경고 보고서 5 → 2건(9건 기준) | 🟡 |
| P10 | 결론 없음, 질의 일부만 다룸 | 결론 섹션 강제 + 상한 6(결정 5) | 이후 모든 보고서에 `Conclusion:` | ✅ |
| P11 | 결론이 앞 섹션 사실을 자기 근거에 붙임 | C0 | C-5 켬·끔 사이 일관된 차이 없음. 이번에도 발생 | ⏳ |
| P12 | 근거 없는 추측·해석 표현 | 측정 도구(2026-10-26) | 수정 후 9건 434개, 62%는 근거 캡션에서 옮김. "추가" 표본 12개 중 8개는 근거에 없는 해석. 출처는 WorldMM 30sec·3min·10min 요약(전처리 프롬프트가 해석을 금지했지만 지켜지지 않음) | ⛔ 원인 확인 |
| P13 | semantic 근거의 가치가 낮음 | 결정 7 보류(후보 C: semantic 경량 필터) | 이번에도 섹션당 0–2개만 인용 | ⏳ |
| P14 | 이미지와 텍스트 근거의 시간 차 | `validation.json`에 기록(후보 D: 이미지를 텍스트 근거 시간 근처로 제한) | `-QuCz7kxBr8` 중앙값 1,485초 | 🟡 기록만 |
| P15 | 번역(한자 혼입, 이름 표기, 자리표시자) | 한자 감지·재시도, 고유명사 보호 | C-4 17섹션 중 5개 실패. 이후 번역은 보류(결정 16: 영어 품질 우선) | ⏳ 보류 |
| P16 | 섹션 내부 인용 번호라 검증 불가 | 후처리기(전역 번호, References, 그림) | `[?]` 0, 프레임 누락 0 | ✅ |
| P17 | 조용한 실패(fallback, `Call failed`, 16섹션 이상 시 소실) | 사전 확인·사후 검증, 섹션 상한 3–15 | CPU 테스트로 감지 확인. 실제 실행에서는 미발생 | ✅ |
| P18 | 검사가 부정문 속 토큰을 오류로 잡음 | 부정 절(absence) 제외 | 오탐 2건 해소, 실제 오류는 계속 검출 | ✅ (한계 있음) |
| P19 | 구간 요약의 "the video closes/opens"를 영상 전체 결말·시작으로 씀 | 10/25: writer 규칙 7(실제 끝 시각) + 결말·시작 검사. 10/26: 영상 마지막 약 60초를 근거 `txt0`으로 제공, 소유격 오탐 수정 | 10/25 수정 후 결론 결말 오인 7/11 → 4/9(표본 작음), 규칙만으로는 막지 못함. 10/26 변경은 GPU 미확인 | 🟡 |

### 10.2 파이프라인·개발 과정 문제 (I1–I30, 묶어서)

| 묶음 | 문제 | 대응과 결과 |
|---|---|---|
| 환경 | 실행 환경 오인(I1), 옛 venv 경로(I2), 대상 없는 `uv sync`가 패키지 20여 개 삭제(I3), `HF_HOME`이 아닌 `HUGGINGFACE_HUB_CACHE`가 모델 경로를 정함(I4), 셸 `grep`이 일부 파일을 건너뜀(I5), `-`로 시작하는 영상 id(I19), 로그 폴더 없음(I20) | 실제 환경 `/opt/venv` 확인, 경로 치환, 금지·사용 규칙으로 정리. ✅ (I4는 정정 기록) |
| Deep-Reporter 통합 | 설정 dict가 키·URL을 버림(I6), 순환 import(I7), 웹 리포트 전제 프롬프트(I8), `recursion_limit` 50 → 16섹션부터 보고서 전체 소실(I17), 테스트 하네스(I21) | 환경변수 주입 + 라우팅 확인, import 순서 고정, 범위 한정 템플릿 교체(실행 중에만, 계약 검사), 섹션 상한 3–15(실측 15 성공·16 실패). ✅ |
| WorldMM·HippoRAG 통합 | 캐시 라벨 고정(I9), OpenIE가 오류를 삼키고 빈 결과 저장(I10), 검색이 질의당 LLM 최대 5회(I11), 점수 없음(I12), visual 검색이 질의를 시간 범위로 해석(I13), 그래프 검색 assert(I14), full 모드 근거 부족(I15), L1 파싱 실패 표시(I16) | 라벨 지정 클래스, 불러오기 전 완전성 검사(409), **L1 설계(요청당 1회)**, RRF 병합, 유사도 함수 직접 호출 + 구간 중앙 프레임, dense 검색으로 대체. I10·I15 🟡, I16 ⛔(문서화) |
| 사전 인덱싱 | GPU 1장 20GB 초과(I18), 10min 캡션 32/232개가 전처리에서 잘림(I22), 10min OpenIE 출력 잘림·청크당 최대 15회 재시도(I23), triple 열거 폭주(I24), 서버 `finish_reason` 표시(I25), 토크나이저 동시 사용 오류 `Already borrowed` 261건(I28) | OpenIE를 LLM 서버 HTTP로(결정 1), **긴 청크 분할 + 잘린 응답 구제 + 연속 15개 초과 절단**(결정 9) → C-1에서 호출 430회 = 계획, 재시도 0, 실패 0. I22 재생성 보류 ⛔, I25 우회 🟡, I28 수정(효과는 다음 사전 인덱싱에서 확인) |
| 운영 | 집계·기록 오류(I26), GPU 공유로 실행 중단·6시간 대기 미시작(I27), 같은 영상을 서비스 2개가 동시에 불러오면 캐시 읽기 실패(I29), Claude 세션 2개 겹침(I30) | 정정 기록, 메모리 감시·자동 중단·우리 PID만 종료, 영상별 불러오기 잠금(C-5 재실행 성공), 세션 하나만 쓰기. I27·I29 ✅, I30 🟡 |

### 10.3 실행 이력 (실제 모델)

| 일시 (UTC) | 실행 | 결과 |
|---|---|---|
| 10/21 | 검색 스모크, 보고서 A(10sec만) | 정상, 382초. 품질 문제를 처음 확인(P1–P10, P13, P14, P16) |
| 10/22 | 보고서 B(`run_report.py` 첫 실행, 번역 포함) | exit 0, 494.4초. 결론 강제(P10) 확인, P11·P12·P15·P18 새로 확인 |
| 10/22 | 사전 인덱싱 시험·영상 3개 | 사용자 지시로 중지. 10min OpenIE 잘림·재시도 폭증 발견(I22–I24) |
| 10/22 | OpenIE 디코딩 비교 실험 | 디코딩 변경 기각, 분할·구제·절단 채택 |
| 10/22–23 | 분할 적용 후 재실행, 대기 후 자동 시작 | 다른 사용자 GPU 사용으로 41초 만에 감시 종료, 6시간 대기 중 시작 조건 미충족(I27) |
| 10/25 12:15 | **C-1** 영상 3개 사전 인덱싱(GPU 4–7) | 완주, 27.4분, 호출 430회 = 계획 |
| 10/25 12:52 | **C-3** 4개 단위 검색 확인 | 36건 성공. text 지연 L0 0.7–1.4초, L1 4.4–7.9초, full 29.7–38.8초 |
| 10/25 13:02 | **C-4** 보고서 3건(번역 포함) | 3건 `passed`. P19(결말 오인) 새로 발견, 번역 실패 5/17 |
| 10/25 13:21 / 13:28 | **C-5** C0 켬·끔 8건 | 첫 시도 I29로 중단 → 잠금 추가 후 8건 `passed`. writer 반복 루프 2건 발견(P9), C0 효과 확인 안 됨 |
| 10/25 14:14 | **P9·P19 수정 후 확인** 9건(이 문서의 예시) | 9건 `passed`. 루프 2건이 130–134초에 끊김, 결말 오인은 검사로 표시되지만 규칙만으로 못 막음 |
| 10/26 | GPU 없이: 흐름·추측 표현 측정(20건), P19 영상 끝 근거·검사 오탐·경고 기준 수정 | CPU 테스트 통과(6종). GPU 확인 대기 |

---

## 11. 결정이 필요한 것과 다음 단계

| 항목 | 내용 | 필요 자원 |
|---|---|---|
| 10/26 변경 확인 | 영상 끝 근거 `txt0`이 결말 오인을 줄이는지, 새 경고 기준 | GPU |
| 결정 7 후보 C·D | C: semantic 근거 경량 필터, D: 이미지를 텍스트 근거 시간 근처로 제한 → 기존(A)과 비교 | 코드 수정 승인 + GPU |
| 상한에 끊긴 섹션 | 그대로 둘지, 그 섹션만 다시 생성할지 | 결정 |
| P12 해석 표현 | 검출 경고 / 다단위 요약 캡션의 해석 표현 정제 / writer 규칙 강화 | 결정 |
| P8 흐름·커버리지 | 섹션 순서·빠진 구간 대응(예: planner 시간 범위 검증, 섹션별 검색 시간 제한) — 아직 설계 전 | 결정 |
| C0 재측정 | 표본을 늘려 효과 측정 | GPU |
| 보류 | C-7(50개 영상 사전 인덱싱, 약 12.5–15시간 추정), I22(10min 재생성), I25, 번역(P15) | 사용자 지시 |
| 이후 | 평가(Video-MME 150문항을 보고서만으로 풀기, 사람 검수), MERIT 검색 서비스, 관제 도메인 템플릿 | — |

---

## 12. 따라 해 보기 (재현)

GPU 없이 이 문서의 단계별 값을 다시 볼 수 있다.

```bash
cd /data1/jyheo/workspace/VideoRAG/report_framework
R=outputs/p9p19_check_20261025_141401
# 단계별 출력: report.json의 outline[i] (section_description, sectional_checklist, text_queries, image_queries,
#              retrieved_texts, retrieved_images, content)
python -c "import json; r=json.load(open('$R/-QuCz7kxBr8__c0_written__r1/report.json')); s=r['outline'][0]; print(s['text_queries'], len(s['retrieved_texts']))"
# planner·query·writer의 입력 프롬프트와 출력 전문: Deep-Reporter 세션 로그 (session_id는 report.json에 있음)
#   $R/dr_logs_s<i>/longgen_sessions_20261025.jsonl → llm_calls[k].input_messages / output_content
# LLM 호출별 토큰·시간: $R/llm_server_s<i>_gpu<g>.log 의 "chat.completions: prompt=… completion=… finish=…"
# 검색 요청별 후보·필터·시간: $R/service_s<i>_gpu<g>.log 의 "search text: {...}" / "search image: {...}"
# 흐름·추측 표현 측정: python analysis/flow_speculation_check.py
```

새 보고서를 만들려면 GPU가 필요하다(LLM 서버 + 검색 서비스 + `run_report.py`, 명령은 `DESIGN_AND_STATUS.md` §13.2).
