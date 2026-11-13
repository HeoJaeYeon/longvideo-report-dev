# 보고서 생성 파이프라인 (Video-RAG × Deep-Reporter)

- 2026-11-10 경로 정리(동작 변경 없음, `internal/status/REORG_LOG_20261110.md`): 사전 인덱싱 캐시 `cache/episodic/` → `WorldMM/output/memory/videomme_long_qwen3vl-8b/report_framework_index/`, WorldMM 메모리 `WorldMM/claude_output/full/` → 같은 폴더(`caption/`, `metadata/`, …). 메모리·캐시의 옛 경로 표기는 작성 당시 기준이다. 같은 날 폴더 재배치(P2): 스크립트·결과 경로(`tests/*` → `tests/unit/`·`tests/gpu/`·`experiments/`·`scripts/launch/`, `analysis/*.json` → `results/`, `inspect/`·`running_example/` → `internal/`)는 본문에서도 새 위치로 고쳐 적었다. 문서 위치는 `docs/README.md` 색인.
- 작성: 2026-10-22. 최종 갱신: 2026-10-26 — 단계별 중간 산출물(planner 프롬프트·outline, 섹션별 query 문장, 검색 결과, writer 프롬프트·출력, 후처리 결과)을 실제 실행 기록으로 정리했다. 모든 중간 산출물을 파일로 열어 볼 수 있도록 `analysis/export_stages.py`와 `internal/inspect/`를 추가했다. 같은 날 ④-2(b) 검색을 코드 기준으로 자세히 다시 썼다(그래프 구성, 그래프 검색 6단계, RRF, L1 필터, semantic, image). 이전 판은 `backups/REPORT_PIPELINE.md.bak_20261026_pipeline`, `backups/REPORT_PIPELINE.md.bak_20261026_retrieval`.
- 기준 코드: `report_framework/` (`run_report.py`, `videorag_retriever_service.py`, `local_llm_server.py`, `domain_templates.py`, `grounding_postprocessor.py`, `report_translator.py`, `prebuild_episodic_index.py`, `config.yaml`)와 Deep-Reporter `deep_reporter/` (읽기 전용).
- 이 문서는 **보고서 1건이 어떻게 만들어지는지**를 단계별로 설명하고, 단계마다 **실제로 들어간 입력과 나온 출력**을 보여 준다. 설계 배경·결정·검증 이력은 `DESIGN_AND_STATUS.md`, 문제와 개선 이력은 `REPORT_ISSUES_AND_FIXES.md`, 반복 실행 간 차이는 `SELF_CONSISTENCY_ANALYSIS.md`·`SELF_CONSISTENCY_CAUSES.md`에 있다.
- 표기: (코드) 소스에서 확인, (실측) 로그·출력에서 확인, (대조) 근거 원문·캡션과 사람이 비교, (가설) 확인하지 못한 추정.

### 예시로 쓰는 실행

| 항목 | 값 |
|---|---|
| 실행 | `outputs/p9p19_check_20261025_141401/` (2026-10-25 14:14–14:32 UTC, `DESIGN_AND_STATUS.md` §9.16) |
| 보고서 | 영상 3개 × 같은 조건 3회(r1–r3) = 9건. 예시는 주로 각 영상의 **r1** |
| 영상 | `-QuCz7kxBr8`(농구 가젯 12개 시험, 00:37:37), `0RxMZBLeqRI`(로마 역사, 00:30:32), `54k2g9ddy4M`(CBC 뉴스 모음, 00:45:14) |
| 질의 | `Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.` (checklist 없음) |
| 설정 | Qwen3-VL-8B 로컬 서버(출력 상한 3,072), 4개 단위 episodic 캐시, L1, filter 노드 끔, C0 켬, 섹션 상한 6, 번역 끔 |
| 코드 | 커밋 `b7a021d` 시점. **2026-10-26 변경(영상 끝 근거 txt0, "loop suspected" 기준, 결말 검사 오탐 수정)은 이 실행에 없다.** 해당 부분은 본문에 따로 표시 |

## 목차
0. 중간 산출물을 직접 보는 법 · 1. 한눈에 보기 · 2. 사전 준비 · 3. 단계별 흐름과 실제 중간 산출물(①–⑨) · 4. LLM 호출과 시간 · 5. 주요 설정 · 6. 실패 지점과 처리 · 7. 현재 한계 · 8. 확장 지점

---

## 0. 중간 산출물을 직접 보는 법

### 0.1 어디에 무엇이 남는가 (코드·실측)

| 단계 | 중간 산출물 | 원본 위치 |
|---|---|---|
| planner | 프롬프트 전문(영상 개요 포함), 출력 원문(JSON) | Deep-Reporter 세션 로그 `<deep_reporter_log_dir>/longgen_sessions_<날짜>.jsonl`의 `llm_calls[0]`(`call_type: outline_generation`)의 `input_messages`, `output_content` |
| 파싱된 outline | 섹션별 `section_description`, `sectional_checklist` | `report.json` `outline[i]` |
| query 생성 | 프롬프트 전문(앞 섹션 요약 포함), 출력 원문 | 세션 로그 `llm_calls`의 `call_type: query_generation`(섹션 순서) |
| 파싱된 query | `text_queries`, `image_queries` | `report.json` `outline[i]` |
| 검색 | 근거 전체(text 12개, image 3개)와 필드(uid, 단위, 시간, 순위, 점수, `content`/`caption`) | `report.json` `outline[i].retrieved_texts`, `retrieved_images` |
| 검색 요청 기록 | 후보 수, L1 필터 동작 여부, 근거 수, 시간 | 검색 서비스 로그 `search text: {...}`, `search image: {...}` |
| L1 필터 | 토큰 수·시간만 | LLM 서버 로그(호출 순서: planner 1 → 섹션마다 query, L1 필터, writer). **후보 목록과 필터 응답 원문은 기록되지 않는다** |
| writer | 프롬프트 전문(근거 목록 포함), 출력 원문(후처리 전) | 세션 로그 `llm_calls`의 `call_type: section_writing` |
| 후처리 후 섹션 본문 | 반복 문장 제거 후(인용은 아직 txtN) | `report.json` `outline[i].content` |
| 최종 본문 | 전역 번호 `[n]`, 그림, References | `report.md` (원본 이어 붙임은 `report_raw.md`) |
| 검사 결과 | 반복 제거, 결말·시작 검사, 규칙 근거 검사, 이미지 시간 차, 경고 | `validation.json` |
| 호출별 토큰·시간 | 프롬프트·출력 토큰, 종료 사유(`stop`/`length`), 초 | LLM 서버 로그 `chat.completions: prompt=… completion=… finish=… …s` |

### 0.2 한 번에 펼쳐 보기: `analysis/export_stages.py` → `internal/inspect/`

위 출처를 모아 보고서마다 단계별 파일로 펼친다. LLM을 다시 부르지 않는다. 최종 본문은 후처리기를 `report.json`에 다시 돌려 만들고, **`report.md`와 글자 단위로 같은지 확인**한다. 9건 모두 같았다(실측).

```bash
cd /data1/USER/workspace/VideoRAG/report_framework
python -B analysis/export_stages.py --run outputs/p9p19_check_20261025_141401   # GPU 불필요
```

```
inspect/p9p19_check_20261025_141401/
  COMPARE_<video>.md                 r1·r2·r3의 outline, query, 근거(인용 여부)를 나란히
  <video>__c0_written__r<k>/
    README.md                        섹션 표, LLM 호출별 토큰·시간·종료 사유, 검증 경고
    01_planner_prompt.md             planner 프롬프트 전문(영상 개요 포함)
    02_planner_output.md             planner 출력 원문 + 파싱된 outline
    s01/ … s06/
      1_query_prompt.md              query 생성 프롬프트 전문
      2_query_output.md              출력 원문 + 파싱된 text/image query
      3_retrieval.md                 검색 요청 기록 + text 근거 12개·image 근거 3개 전체(인용 여부 표시)
      4_writer_prompt.md             writer 프롬프트 전문(writer가 본 근거 그대로)
      5_writer_output_raw.md         writer 출력 원문(후처리 전)
      6_postprocess.md               반복 제거, 결말·시작 검사, 규칙 검사, 이미지 시간 차, 최종 본문, 쓰인 References
```

---

## 1. 한눈에 보기

```
[오프라인, 영상별 1회]  WorldMM 메모리 (50영상 구축 완료)        episodic HippoRAG 캐시 (4개 단위: 검증 영상 3개만 완성)
  캡션 10sec/30sec/3min/10min · semantic triple · visual 임베딩      cache/episodic/<vid>/episodic_memory/<g>/

[실행 중인 서비스 2개, GPU]
  (L) local_llm_server.py  :8010  OpenAI 호환 /v1/chat/completions, Qwen3-VL-8B   (또는 vLLM, 같은 주소)
  (R) videorag_retriever_service.py :8020  POST /videos/<vid>/search, 영상 1개씩 메모리 로드

[보고서 1건]  python run_report.py --config config.yaml --video-id=<vid> --query "<요청>"   (모델 로드 없음, CPU)
  ① 사전 확인 → ② LLM 라우팅 설정 → ③ 영상 개요·영상 끝 시각 + 템플릿 적용 + 앞 섹션 맥락 교체(C0)
  → ④ Deep-Reporter 그래프:  planner → [섹션마다: query 생성 → 검색(R, 안에서 L1 필터) → writer] → combine
  → ⑤ 후처리 (반복 문장 제거 → 결말·시작 검사 → 인용 → References·그림)  → ⑥ 규칙 기반 근거 검사 → ⑦ 사후 검증
  → ⑧ 한국어 번역 (설정 시) → ⑨ 산출물
```

단계별 입력과 출력 요약:

| 단계 | LLM | 입력 | 출력 |
|---|---|---|---|
| ④-1 planner | 1회 | 질의, checklist, 영상 개요(10min 캡션 전체) | outline JSON: 섹션마다 `section_description`(2–4문장), `sectional_checklist`(3–5개, 결론 2–3개) |
| ④-2(a) query 생성 | 섹션마다 1회 | 질의, checklist, **앞 섹션 요약(C0)**, 현재 섹션 설명·checklist | `text_queries` 2–3개(키워드형), `image_queries` 1–2개(장면 묘사 한 문장) |
| ④-2(b) 검색 | 섹션마다 1회(L1 필터) | text 질의 목록 / image 질의 목록 | text 근거 12개(episodic 8 + semantic 4), image 근거 3개(프레임 + 10sec 캡션) |
| ④-2(c) writer | 섹션마다 1회 | 섹션 위치, 설명, checklist, 앞 섹션 요약, 직전 섹션 끝, 근거(txt1–12, img1–3 캡션), 규칙 | 섹션 본문(`# 제목`, `[citation:txtN]`, `![](citation:imgN)`) |
| ④-3 combine | 0 | 섹션 본문 | `report_raw.md` |
| ⑤–⑦ 후처리·검사 | 0 | 섹션 본문 + 근거 | `report.md`, `validation.json` |

---

## 2. 사전 준비 (오프라인)

1. **WorldMM 메모리** (구축 완료, 50영상): `caption/<vid>/{10sec,30sec,3min,10min}.json`, `metadata/semantic_memory/<vid>/semantic_consolidation_results_qwen3vl-8b.json`, `metadata/visual_memory/<vid>/visual_embeddings.pkl`.
   - 10sec 캡션은 프레임과 Whisper 자막으로 만들었고, 30sec·3min·10min은 그것을 LLM으로 요약한 것이다(WorldMM 전처리).
   - 요약 캡션에는 "The video opens with…"처럼 **그 구간의** 시작·끝을 가리키는 표현과 해석·평가 표현이 많다(`REPORT_ISSUES_AND_FIXES.md` P12·P19).
2. **episodic HippoRAG 캐시** (`prebuild_episodic_index.py`)
   - 캡션마다 OpenIE(LLM)로 그래프를 만들어 `cache/episodic/<vid>/episodic_memory/<g>/`에 저장한다.
   - 10sec는 전처리 OpenIE 결과를 시드로 넣어 LLM 호출을 줄인다. 50영상 계획은 빈 캐시 기준 13,424회다(긴 청크 분할 포함).
   - **긴 청크 분할 OpenIE**: 1,100토큰을 넘는 청크(주로 10min)는 빈 줄 문단 단위의 700토큰 이하 조각으로 나눠 NER·triple을 뽑고 합친다. 파싱 실패 응답의 완성된 항목은 살리고(구제), 같은 (주어, 술어)가 연속 15개를 넘는 폭주 triple은 자른다(I23·I24).
   - 실행: `./run_prebuild_http.sh <LLM_GPUS> <INDEXER_GPU> [--videos=<vid>]`(결정 1 = A안, OpenIE를 LLM 서버 HTTP로). GPU 공유 시 `experiments/gpu_3videos.py`(실행 전 여유 확인, 실행 중 감시·자동 중단).
   - **현재 상태**: 2026-10-25 C-1에서 검증 영상 3개의 4개 단위 캐시를 완성했다(GPU 4–7, 1,643초, 호출 430회 = 계획, 실패 0). 나머지 47개 영상은 캐시가 없다(C-7 미실행).
   - 검색 서비스는 캐시가 불완전한 영상을 거부한다(409). 서비스 여러 개가 같은 영상을 동시에 불러오면 실패하므로(I29) 영상별로 차례로 불러온다.

예시 영상 3개의 메모리 규모(검색 서비스 로그, 실측):

| 영상 | 캡션 수 10sec/30sec/3min/10min | 10sec 그래프 노드 / 엣지 | semantic triple | visual 구간 |
|---|---|---|---|---|
| `-QuCz7kxBr8` | 226 / 76 / 13 / 4 | 1,277 / 10,596 | 153 | 226 |
| `0RxMZBLeqRI` | 184 / 62 / 11 / 4 | 2,290 / 11,507 | 405 | 184 |
| `54k2g9ddy4M` | 272 / 91 / 16 / 5 | 2,123 / 11,736 | 725 | 272 |

---

## 3. 단계별 흐름과 실제 중간 산출물

### ① 설정 확인과 사전 확인 (`run_report.run`, `run_report.preflight`)
- 설정 확인: LLM 백엔드와 모델명(local이면 이름에 `qwen`, openai면 `gpt`와 `OPENAI_API_KEY`), `report.max_sections`(정수 3–15), `report.previous_sections_context`(`written`/`deep_reporter`). 잘못되면 exit 2.
- 영상 개요 파일(`<caption_dir>/<vid>/10min.json`)이 있는지 확인한다.
- LLM 서버 `GET /health`(local 백엔드일 때), 검색 서비스 `GET /health`와 **`POST /videos/<vid>/load`**(캐시가 불완전하면 409).
- 템플릿 계약 검사(`domain_templates.resolve_targets`).
- 하나라도 실패하면 **exit 2**로 즉시 중단한다. 예시 실행에서는 1.1–1.2초 걸렸다.

### ② LLM 라우팅 설정과 생성 방식
- Deep-Reporter는 LLM 키와 URL을 **환경변수로만** 받는다(설정 dict의 키·URL은 `BaseConfig.from_dict`가 버린다).
  - **local**(기본): `QWEN_BASE_URL=http://127.0.0.1:8010/v1`, `QWEN_API_KEY=EMPTY`, 모델 `qwen3vl-8b`. 모델명에 `qwen`이 있어야 QWEN 설정으로 라우팅된다.
  - **openai**: `OPENAI_API_KEY`(필수), `OPENAI_BASE_URL`(선택), 모델 `gpt-5-mini`.
- `create_openai_api({primary_model, log_dir})` 후 **실제로 라우팅된 base URL이 기대값과 같은지 확인**한다. 다르면 exit 2.
- **생성 방식** (코드·설정 파일)
  - Deep-Reporter는 temperature·top_p·seed를 보내지 않는다(`llms/factory.py`가 temperature를 넘기지 않음).
  - 우리 서버도 요청에 값이 없으면 `max_new_tokens`만 넘긴다.
  - 그래서 모델 `generation_config.json`의 기본값(`do_sample: true`, temperature 0.7, top_p 0.8, top_k 20)으로 **샘플링**한다. 같은 입력이어도 실행마다 출력이 다르다(`SELF_CONSISTENCY_CAUSES.md`).
  - Deep-Reporter는 `max_tokens` 8,192를 보내고, 서버가 3,072로 자른다(`max_tokens_cap`, P9).

### ③ 영상 개요, 영상 끝, 템플릿 적용
- **개요**: 10min 캡션들을 `[HH:MM:SS-HH:MM:SS] 캡션` 블록으로 이어 붙인다(`domain_templates.load_video_overview`). 예시 영상은 4–5개 블록이다.
  - `0RxMZBLeqRI`의 0–10분·10–20분 블록은 전처리에서 2,048토큰에 잘린 캡션이다(I22).
- **영상 끝 시각**: 10sec 캡션 마지막 `end_time`(`load_video_end`). 10min 개요의 마지막 창 끝(40:00, 50:00 등)은 실제 끝보다 길어서 쓰지 않는다. 이 시각은 writer 규칙 7에 들어간다.
- **(2026-10-26 추가, 예시 실행에는 없음) 영상 끝 근거**: 마지막 약 60초의 10sec 캡션을 하나로 묶는다(`load_video_ending`). writer 프롬프트에 `[Source txt0 begin] … [Source txt0 end]`로 넣고, 마지막 섹션에서만 결말 서술에 인용하게 한다.
- **템플릿 교체**: `with apply_templates(build_templates("videomme", 개요, max_sections, video_end=…, video_ending=…)):` 블록 안에서만 Deep-Reporter의 planner·query·writer 프롬프트가 비디오용으로 바뀐다.
  - 실행 전에 placeholder, 출력 형식 마커, `.format()` 시험 실행을 검사한다. 블록이 끝나면 원래 템플릿으로 복원한다.
  - `max_sections`(기본 6)는 결론 포함 섹션 수 상한이다. 허용 범위 3–15인 이유: Deep-Reporter `recursion_limit=50` 때문에 16섹션부터 보고서 전체가 사라진다(실측).
- **C0 (결정 4)**: `previous_sections_context: written`(기본)이면 `apply_written_context()`로 Deep-Reporter `_update_context`를 실행 중에만 교체한다(④-2(d)).

### ④-1 planner: outline 만들기 (LLM 1회)

**입력 구성** (`domain_templates.VIDEOMME_OUTLINE`, 코드)

| 부분 | 내용 |
|---|---|
| 역할 | "You are planning a report about ONE specific video…" |
| 사용자 요청 | `{overall_query}` |
| 추가 요구사항 | `{overall_checklist}` (예시에서는 비어 있음) |
| 영상 개요 | 10min 캡션 전체(③) |
| 규칙 1–6 | 영상 근거로 뒷받침되는 섹션만, 개요에 없으면 지어내지 말 것, 대체로 시간순, 설명 2–4문장에 대략의 시간 범위, checklist 3–5개, **마지막은 `Conclusion:`으로 시작하는 짧은 결론**(checklist 2–3개) |
| 출력 형식 | `{"outline": [{"section_description", "sectional_checklist"}, …]}` 예시 |

**실제 프롬프트** (`-QuCz7kxBr8` r1, 전체 23,899자 = 5,219토큰. 개요 블록은 앞 260자만 싣고 나머지는 생략 표시. 전문: `internal/inspect/…/-QuCz7kxBr8__c0_written__r1/01_planner_prompt.md`)

````
You are planning a report about ONE specific video. Everything in the report must come from this video.

**User request (report topic):**
Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.

**Additional requirements from the user:**


**Video overview** (timestamped summaries of consecutive ~10-minute segments, generated from the video's frames and speech; use it only to learn what the video contains):
[00:00:00-00:10:00] **Six men—Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player—gather on a sunny outdoor basketball court to test 12 viral sports gadgets, splitting into two teams of three. Dressed in athletic wear, they introduce the challenge …   ⟨이하 생략, 이 블록 전체 8,001자⟩

[00:10:00-00:20:00] **[Event 1: Dribble Challenge Begins]**   A man in a white t-shirt and patterned shorts initiates a timed dribbling challenge on a sunny outdoor court, with a countdown timer and on-screen text reading “MOST DRIBBLES IN 15 SECONDS.” He main …   ⟨이하 생략, 이 블록 전체 4,375자⟩

[00:20:00-00:30:00] **[Event 1: Product Introduction and Setup]**   Under bright sunlight on a residential outdoor basketball court, three men gather around a white table displaying the “NEVER ENDING DEFENDER” training device. A man in a black t-shirt explains …   ⟨이하 생략, 이 블록 전체 4,352자⟩

[00:30:00-00:40:00] **[Event 1: Scoring Play and Defensive Engagement]**   Under a bright, open-air “HYPE”-branded court surrounded by hills and greenery, a player in a white hoodie and patterned shorts drives past a defender in a blue jersey and scores a layu …   ⟨이하 생략, 이 블록 전체 4,195자⟩

**Task:**
Design an outline of 3-6 sections in total (never more than 6, including the final conclusion section) that answers the user request using content that is actually present in this video.

Rules:
1. Every section must be supportable by evidence from the video (visible events, actions, people, objects, settings, on-screen text, speech). Do not plan sections that need outside knowledge, background research, statistics, predictions, or opinions that the video does not express.
2. If the request asks about something the overview does not show, do not invent it; plan at most one section that reports what the video does and does not show about it.
3. Order the sections so the report reads coherently; the chronological order of the video is usually best for describing what happens.
4. section_description: 2-4 sentences explaining what the section covers, which part(s) of the video it draws on (approximate time ranges from the overview), and what the reader learns.
5. sectional_checklist: 3-5 concrete, checkable items about observable content, not generic writing advice.
6. The LAST section must be a brief conclusion that summarizes the main results already covered by the earlier sections and answers the user request at a high level. Its section_description must start exactly with "Conclusion:", it must not introduce new topics, and its sectional_checklist has 2-3 items. No other section_description may start with "Conclusion:".

**Output Format (JSON):**
```json
{
  "outline": [
    {
      "section_description": "This section introduces the people and the setting shown at the beginning of the video (about 00:00:00-00:10:00). It covers how the participants are presented and what the video announces it will do. Readers learn who appears in the video and what its stated goal is.",
      "sectional_checklist": [
        "Identify the main people and how they are introduced",
        "Describe the setting where the video takes place",
        "State the goal or plan announced at the start"
      ]
    },
    ...
    {
      "section_description": "Conclusion: This section briefly summarizes the main results shown in the video and answers the user request at a high level, using only findings covered in the earlier sections.",
      "sectional_checklist": [
        "Summarize the main outcomes shown in the video",
        "Answer the user request in one or two sentences"
      ]
    }
  ]
}
```

Generate the outline now:

````

**출력**
- LLM이 위 형식의 JSON을 코드블록으로 돌려준다.
- Deep-Reporter `parse_json_output`이 코드블록 안 JSON(없으면 가장 바깥 중괄호)을 읽고 `outline` 키를 확인한다.
- 실패하면 **조용히 섹션 1개(설명 = 질의)로 대체**한다(⑦에서 오류로 잡음).
- 예시 9건은 모두 정상 파싱됐다.

**예시: 세 영상 r1의 outline 전문** (`report.json` `outline`의 `section_description`과 `sectional_checklist` 그대로. 출력 원문은 각 `02_planner_output.md`)

#### `-QuCz7kxBr8` r1

**S1.** This section introduces the six main participants—Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player—and establishes the setting: a sunny outdoor basketball court. It describes how they split into teams and begin testing 12 viral sports gadgets, starting with the SPORTS DRIBBLE SPECS. Readers learn the video’s goal is to test and evaluate these gadgets in a casual, competitive environment.

- List the six main participants and how they are introduced
- Describe the outdoor basketball court setting and weather
- Note the first gadget tested and the rules of its challenge

**S2.** This section details the testing of the SKLZ Dribble Stick and the subsequent shooting challenge with the Straight Shooter Strap. It covers the rules, player reactions, and scoring, including humorous commentary and a forfeit challenge involving jumping jacks. Readers learn how the group evaluates the gadgets’ usefulness and how the testing evolves into physical challenges.

- Describe the SKLZ Dribble Stick’s rules and how it is tested
- Note the Straight Shooter Strap’s demonstration and player feedback
- Record the forfeit challenge (jumping jacks) and its humorous context

**S3.** This section covers the testing of the Flick Glove and the Shot Coach device, including rules, player attempts, and the scoring system tied to sit-ups. It highlights the competitive nature of the challenges and the camaraderie among players, especially during synchronized shooting and training drills. Readers learn how gadgets are integrated into structured gameplay with consequences.

- Describe the Flick Glove’s rules and how shots are scored
- Note the Shot Coach device’s use in training and its impact on performance
- Record the sit-up forfeit and the players’ reactions

**S4.** This section details the “First Made Shot Shoots Silly String” game, including the rules, synchronized shooting, and the winner’s celebration. It also covers the defensive drills with padded shields and the “Never Ending Defender” training challenge, showing how the group transitions between game modes. Readers learn how the video concludes with a mix of competition, humor, and product reinforcement.

- Describe the silly string game’s rules and outcome
- Note the defensive drills with padded shields and their setup
- Record the “Never Ending Defender” challenge and its scoring system

**S5.** This section focuses on the final scoring segment, including the 3-1 victory for Zak Jesse & Kris, and the closing instructional segment featuring players in ZHYPE-branded gear. It concludes with the video’s end screen, thanking viewers and prompting subscriptions. Readers learn the final outcomes and how the video wraps up with branded content and social engagement.

- Identify the final winning team and their score
- Note the branded instructional segment and player attire
- Record the end screen’s text and call to action

**S6.** Conclusion: This section briefly summarizes the main results shown in the video and answers the user request at a high level, using only findings covered in the earlier sections.

- Summarize the main outcomes shown in the video
- Answer the user request in one or two sentences

#### `0RxMZBLeqRI` r1

**S1.** This section introduces the video’s framing, including its disclaimer about terminology, visual montage of historical and satirical imagery, and the opening narrative about Roma identity and systemic erasure. Readers learn that the video begins by setting a tone of historical complexity and cultural marginalization, using maps, memes, and symbolic overlays to establish its subject matter.

- Note the disclaimer about using 'Gypsy' as a non-slandrous term
- Identify the visual montage including the 'TITO INVENTING MACEDONIANS' meme
- Recognize the text overlay 'POREKLOM SAM CIGANIN' over Obama image

**S2.** This section traces the video’s historical and cultural framing of Roma identity, showing both marginalization and resilience through visual juxtapositions—from historical photos to modern parades with flags. Readers learn how the video counters earlier depictions of erasure by affirming Roma agency and cultural continuity across centuries.

- Identify the transition from sepia-toned historical photos to modern parade scenes
- Note the narration acknowledging historical invisibility due to stigma
- Recognize the visual contrast between exclusion and cultural celebration

**S3.** This section explores the video’s depiction of Roma as historically misclassified and systematically stigmatized, using imagery of scientific exclusion, cultural heritage overlays, and satirical fantasy scenes to critique how Roma are reduced to stereotypes. Readers learn how the video links Roma identity to geopolitical misreading and societal fear.

- Identify the lab-coated figure symbolizing scientific exclusion
- Note the 'UNWANTED' text superimposed over historical scenes
- Recognize the Minecraft mining scenes transitioning to fantasy combat

**S4.** This section details the video’s historical narrative of Roma origins and early misidentification, using maps, 13th-century battle imagery, and geopolitical framing to show how Roma were labeled by empires. Readers learn how the video positions Roma not as a distinct ethnic group but as a product of historical misreading and geopolitical conflict.

- Identify the 13th-century map anchoring Roma presence
- Note the 'VS' graphic depicting Seljuk Turks vs. Byzantine Empire
- Recognize the narration explaining Roma were mistaken for Turks by Byzantines

**S5.** This section covers the video’s depiction of Roma persecution under Nazi and communist regimes, including archival footage, Gestapo documentation, deportation scenes, and post-war institutional erasure. Readers learn how the video documents mass suffering, state-sponsored violence, and the ongoing struggle for recognition and justice.

- Identify the archival footage of Roma camps and Gestapo mugshots
- Note the text overlay stating 500,000–1,500,000 deaths
- Recognize the 1942 deportation to Auschwitz-Birkenau with striped uniforms

**S6.** Conclusion: This section briefly summarizes the main results shown in the video and answers the user request at a high level, using only findings covered in the earlier sections. It confirms the video’s focus on Roma identity, historical marginalization, systemic persecution, and cultural resilience.

- Summarize the video’s portrayal of Roma as both historically marginalized and culturally resilient
- Confirm that the video concludes with a global perspective and credits
- State that the video’s final moments transition to a stylized globe and credits

#### `54k2g9ddy4M` r1

**S1.** This section introduces the video’s opening segments (00:00:00-00:10:00), which focus on a measles resurgence in Canada and the U.S., featuring medical experts and public health alerts. Readers learn about the outbreak’s origin mystery, vaccination rates, and the risks to vulnerable populations, as well as the video’s initial framing as a public health report.

- Identify Dr. Earl Rubin, Dr. Anna Banerji, and Dr. Christopher Labos as key medical experts cited
- Note the on-screen text stating Canada eliminated measles in 1998 and current vaccination levels at 79%
- Confirm the video’s opening title card for 'The National' and its public health focus

**S2.** This section covers the unfolding public health crisis (00:10:00-00:20:00), including a measles outbreak in the U.S. centered on a school, the death of a patient in Montreal, and systemic emergency response failures. Readers learn about parental concerns, coroner reviews, and the video’s juxtaposition of health emergencies with political and economic stories.

- Note the U.S. measles outbreak with 41 cases in 16 states, centered on Manatee Bay Elementary
- Identify the third patient death in a Montreal hospital waiting room under coroner’s review
- Confirm the on-screen alerts and visuals of hospital corridors and paramedics preparing ambulances

**S3.** This section describes the video’s shift to personal tragedy and institutional failure (00:20:00-00:30:00), including the misidentification at Montfort Hospital and the emotional aftermath, followed by a transition to athletic triumph with Joshua Liendo’s gold medal win. Readers learn about the human cost of systemic errors and the contrast with athletic achievement.

- Identify Heather Insley as the grieving mother who learned her son was a stranger
- Note the CBC News coverage of the hospital’s official statement and formal review
- Confirm Joshua Liendo’s gold medal win in the Men’s 100m Butterfly at the Commonwealth Games

**S4.** This section details the video’s focus on Liendo’s journey and legacy (00:30:00-00:40:00), including his reflections on training, cultural roots, and the support of role models. Readers learn about his personal life, his connection to Trinidad, and his status as Canada’s first Black swimmer to win international gold.

- Note Liendo’s reflection on moving from Trinidad to Toronto at age 10
- Confirm his mention of role models like Dylan Carter and George Bevel
- Identify on-screen text declaring him 'swims into the history books'

**S5.** This section covers the video’s coverage of community disaster and recovery (00:40:00-00:50:00), including the destruction of a First Nation school, federal rebuilding pledges, and the eventual reopening of new schools. Readers learn about the fire’s impact, the community’s grief, and the government’s delayed but eventual support.

- Identify the fire that destroyed the only school on Eabametoong First Nation
- Note the federal pledge of over $13 million for modular classrooms
- Confirm the grand opening of new schools in Pikangikum and Wapekeka First Nations

**S6.** Conclusion: This section briefly summarizes the main results shown in the video and answers the user request at a high level, using only findings covered in the earlier sections.

- Summarize the video’s coverage of public health crises, institutional failures, and athletic triumph
- State that the video concludes with community recovery and athletic legacy as its final themes

| 영상 | planner 호출 | 섹션 수 |
|---|---|---|
| `-QuCz7kxBr8` r1 | 프롬프트 5,219 / 출력 764토큰, 35.4초 | 6 |
| `0RxMZBLeqRI` r1 | 6,966 / 811토큰, 37.4초 | 6 |
| `54k2g9ddy4M` r1 | 6,271 / 904토큰, 43.0초 | 6 |

**보이는 점** (대조)
- 섹션 나누는 방식이 영상마다 다르다.
  - `-QuCz7kxBr8`: 가젯·게임 단위로 나눴고, 시간 범위를 쓰지 않았다.
  - `54k2g9ddy4M`: 개요의 10분 창 하나에 섹션 하나씩 "(00:00:00-00:10:00)" 같은 범위를 붙였다.
  - `0RxMZBLeqRI` r1: 주제로 나눴고, 섹션 1–4가 모두 영상 앞부분 내용이다.
- planner가 개요의 세부를 설명·checklist에 옮긴다. 예: `54k2g9ddy4M` S1 checklist의 "current vaccination levels at 79%", `-QuCz7kxBr8` S5 설명의 "3-1 victory for Zak Jesse & Kris". 이 세부가 검색어와 본문으로 이어진다(P5).
- 시간 표기 오류가 있다. 예: `54k2g9ddy4M` S2 "(00:10:00-00:20:00)"의 내용(미국 홍역)은 개요 0–10분에 있다.
- 결론 섹션의 checklist가 결말을 미리 단정하기도 한다. `54k2g9ddy4M` r1 "State that the video concludes with community recovery and athletic legacy as its final themes"는 실제 결말(반려동물 심령술사·염소, 앵커, CBC 로고)과 다르고, 결론 본문이 그대로 따랐다(`SELF_CONSISTENCY_CAUSES.md` §4).
- 같은 영상의 r2·r3 outline은 `internal/inspect/…/COMPARE_<video>.md`에서 나란히 볼 수 있다.

### ④-2 섹션마다 반복 (섹션 수만큼)

#### (a) query 생성 (LLM 1회)

**입력 구성** (`domain_templates.VIDEOMME_QUERY`, 코드)

| 부분 | 내용 |
|---|---|
| Report topic / Overall requirements | 질의, checklist |
| **Previous sections (summary)** | 앞 섹션 요약. 첫 섹션은 "This is the first section". C0(기본)에서는 앞 섹션에서 실제로 쓴 제목과 단락 첫 문장(④-2(d)) |
| Current section / requirements | planner의 섹션 설명과 checklist |
| 검색 방식 설명 | text 질의 = 사건·행동·인물·물체·발화를 짧은 키워드형으로, image 질의 = 장면의 **겉모습**을 한 문장으로(차트·도표 금지) |
| 지시 | 섹션 요구사항을 고루 다루고, 비슷한 질의와 앞 섹션 반복을 피함. **text 2–3개, image 1–2개** |

**실제 프롬프트와 출력** (`-QuCz7kxBr8` r1 섹션 2, 566토큰. C0 요약에 섹션 1에서 쓴 문장이 들어 있다)

````
You generate search queries for retrieving evidence from ONE video's memory.

**Report topic:** Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.

**Overall requirements:**


**Previous sections (summary):**
Already written in earlier sections (title, then the first sentence of each paragraph; citation numbers removed - they do NOT refer to the evidence of the current section):
Section 1: Introduction to the Participants and Setting
- Six men—Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player—are introduced as the main participants in the video.
- The video’s goal is established early: to test and evaluate the gadgets in a hands-on, competitive, yet lighthearted manner.
- The group’s interaction remains informal and humorous, with teammates reacting to performance with thumbs-up approval and score graphics flashing from 5 to 6, then 4.

**Current section:** This section details the testing of the SKLZ Dribble Stick and the subsequent shooting challenge with the Straight Shooter Strap. It covers the rules, player reactions, and scoring, including humorous commentary and a forfeit challenge involving jumping jacks. Readers learn how the group evaluates the gadgets’ usefulness and how the testing evolves into physical challenges.

**Current section requirements:**
- Describe the SKLZ Dribble Stick’s rules and how it is tested
- Note the Straight Shooter Strap’s demonstration and player feedback
- Record the forfeit challenge (jumping jacks) and its humorous context

The video memory can be searched in two ways:
1. text_queries search timestamped descriptions of the video (what happens, who does what, what is said, which objects appear) and short facts extracted from the video. Write short keyword-style phrases that name concrete events, actions, people, objects, or spoken topics (e.g., "host explains the rules", "person unboxes the product").
2. image_queries search video clips by visual similarity. Write one sentence describing what the scene LOOKS like: people and their appearance and actions, objects, and the setting (e.g., "a woman in an apron stirring a pot in a bright kitchen"). Do not ask for charts, diagrams, infographics, or documents.

Cover the different requirements of the current section, avoid near-duplicate queries, and do not repeat what previous sections already covered unless it is needed.
Generate 2-3 text_queries and 1-2 image_queries.

**Output Format (JSON):**
```json
{
  "text_queries": ["query 1", "query 2"],
  "image_queries": ["scene description 1"]
}
```

Generate the queries now:

````

출력 원문:

````
```json
{
  "text_queries": [
    "players test SKLZ Dribble Stick by dribbling with stick attached to ball",
    "Straight Shooter Strap demonstrated with player shooting hoops while strapped",
    "group performs jumping jacks as forfeit challenge after failed shooting attempt"
  ],
  "image_queries": [
    "six men in athletic wear dribbling basketball with SKLZ Dribble Stick attached to ball on a court"
  ]
}
```
````

- 출력은 `parse_json_output`으로 읽는다(`text_queries`, `image_queries` 키 필수).
- 실패하면 섹션 설명을 그대로 검색어로 쓴다(⑦ 경고). 예시 9건에서는 실패가 없었다.

**예시: 세 영상 r1의 섹션별 query 전문** (`report.json` `text_queries`·`image_queries`)

#### `-QuCz7kxBr8` r1

| 섹션 | text_queries | image_queries |
|---|---|---|
| S1 Introduction to the Participants and Setting | 1. `six players introduced: Chris, Zach, Cass, James, Mitchell, and sixth unnamed player`<br>2. `first gadget tested: SPORTS DRIBBLE SPECS, rules explained for challenge` | `six people standing on a sunny outdoor basketball court, wearing casual sportswear, ready to play` |
| S2 Testing the SKLZ Dribble Stick and the Straig … | 1. `players test SKLZ Dribble Stick by dribbling with stick attached to ball`<br>2. `Straight Shooter Strap demonstrated with player shooting hoops while strapped`<br>3. `group performs jumping jacks as forfeit challenge after failed shooting attempt` | `six men in athletic wear dribbling basketball with SKLZ Dribble Stick attached to ball on a court` |
| S3 Testing the Flick Glove and Shot Coach: Rules … | 1. `players attempt shots using Flick Glove with sit-up scoring system`<br>2. `Shot Coach device used for guided shooting drills with feedback`<br>3. `player forfeits sit-ups after missing shot with Flick Glove` | `six men in athletic wear performing synchronized shooting drills with training gloves and devices in a gym setting` |
| S4 First Made Shot Shoots Silly String Game, Def … | 1. `players explain rules of First Made Shot Shoots Silly String`<br>2. `Never Ending Defender challenge scoring system explained`<br>3. `defensive drills with padded shields setup and execution` | `six men in athletic wear standing in a gym, one holding a silly string can while others aim basketballs` |
| S5 Final Scoring Segment and Closing Instruction … | 1. `Zak Jesse and Kris win 3-1 in final scoring segment`<br>2. `players wear ZHYPE-branded gear during instructional segment`<br>3. `end screen thanks viewers and prompts subscription` | `three men in ZHYPE-branded athletic wear standing in a gym holding basketballs, smiling at camera` |
| S6 Conclusion | 1. `final score displayed as 3-1 after one-on-one game`<br>2. `players wear ZHYPE branded gear during instructional segment`<br>3. `video ends with blue and white static end screen` | `three men on outdoor basketball court under blue sky, jumping simultaneously to shoot hoops` |

#### `0RxMZBLeqRI` r1

| 섹션 | text_queries | image_queries |
|---|---|---|
| S1 Section 1: Framing the Video — Disclaimers, V … | 1. `disclaimer about using 'Gypsy' as non-slandrous term`<br>2. `text overlay 'POREKLOM SAM CIGANIN' over Obama image`<br>3. `visual montage including 'TITO INVENTING MACEDONIANS' meme` | `montage of historical and satirical imagery with text overlays and meme visuals` |
| S2 Historical and Cultural Framing of Roma Ident … | 1. `narration acknowledges Roma historical invisibility due to stigma`<br>2. `transition from sepia photos to modern Roma parade with flags`<br>3. `visual contrast between exclusion and cultural celebration in narration` | `modern Roma parade with colorful flags and traditional costumes marching in public street` |
| S3 Depiction of Roma as Historically Misclassifi … | 1. `lab-coated figure appears with scientific exclusion imagery`<br>2. `text overlay 'UNWANTED' shown over historical Roma scenes`<br>3. `Minecraft mining scene transitions to fantasy combat sequence` | `a person in a lab coat standing before a screen displaying exclusion data, with Roma historical imagery in the background` |
| S4 Historical Narrative of Roma Origins and Earl … | 1. `narration explains Roma mistaken for Seljuk Turks by Byzantines`<br>2. `13th-century map showing Roma presence in Balkans`<br>3. `VS graphic depicting Seljuk Turks vs Byzantine Empire` | `a 13th-century style map with labeled regions showing Roma presence and battle lines between Seljuk Turks and Byzantine Empire` |
| S5 Depiction of Roma Persecution under Nazi and … | 1. `text overlay states 500,000–1,500,000 Roma deaths`<br>2. `archival footage of Roma deportation to Auschwitz-Birkenau`<br>3. `Gestapo mugshots of Roma individuals shown with identification tags` | `black-and-white archival footage of Roma prisoners in striped uniforms walking in a line through a camp gate` |
| S6 Conclusion | 1. `video concludes with global perspective and credits`<br>2. `Roma resilience highlighted through visual contrast of historical and modern imagery` | `stylized globe rotating with animated continents and credits rolling at the bottom` |

#### `54k2g9ddy4M` r1

| 섹션 | text_queries | image_queries |
|---|---|---|
| S1 Introduction to the Video’s Opening Segments … | 1. `Dr. Earl Rubin discusses measles resurgence origins`<br>2. `on-screen text shows Canada eliminated measles in 1998`<br>3. `Dr. Anna Banerji explains vaccination risks to vulnerable groups` | `medical experts in lab coats speaking to camera in a news studio setting` |
| S2 Unfolding Public Health Crisis: Measles Outbr … | 1. `U.S. measles outbreak with 41 cases reported in 16 states centered at Manatee Bay Elementary`<br>2. `third measles patient death in Montreal hospital waiting room under coroner review`<br>3. `on-screen alerts showing hospital corridors and paramedics preparing ambulances during outbreak` | `hospital corridor with paramedics in uniform loading patients into ambulances, fluorescent lighting and medical equipment visible` |
| S3 Shift to Personal Tragedy and Institutional F … | 1. `Heather Insley identifies her son as a stranger after hospital misidentification`<br>2. `CBC News reports Montfort Hospital’s official statement and review process`<br>3. `Joshua Liendo wins gold medal in Men’s 100m Butterfly at Commonwealth Games` | `A grieving mother holding her child’s hand in a hospital hallway, visibly distraught` |
| S4 Liendo’s Journey and Legacy | 1. `Joshua Liendo talks about moving from Trinidad to Toronto at age 10`<br>2. `Liendo mentions role models Dylan Carter and George Bevel in interview`<br>3. `on-screen text appears declaring 'swims into the history books'` | `Joshua Liendo in swimwear, smiling after a race, with Canadian flag background` |
| S5 Community Disaster and Recovery | 1. `fire destroys Eabametoong First Nation school`<br>2. `federal government pledges $13 million for modular classrooms`<br>3. `new schools reopen in Pikangikum and Wapekeka First Nations` | `a burned-out school building with smoke rising and First Nation community members gathered outside in grief` |
| S6 Conclusion | 1. `video concludes with community recovery after school fire`<br>2. `Joshua Liendo reflects on his legacy as Canada’s first Black Olympic gold medalist swimmer`<br>3. `public health crisis summary including measles outbreak and hospital misidentification tragedy` | `a modern school building with vehicles parked outside under snowy sky, symbolizing recovery` |

**보이는 점** (실측·대조)
- query는 checklist 문구를 거의 그대로 옮긴다. 예: checklist "Note the U.S. measles outbreak with 41 cases in 16 states, centered on Manatee Bay Elementary" → query "U.S. measles outbreak with 41 cases reported in 16 states centered at Manatee Bay Elementary". 그래서 planner가 개요에서 가져온 세부가 그대로 검색된다.
- image query는 한 섹션에 1개만 만들어졌다(9건 54섹션 모두, 실측). text query는 2–3개다.
- 결론 섹션의 query는 **그 실행이 앞에서 다룬 주제**를 따라간다. 예: `-QuCz7kxBr8` r1 결론은 "final score displayed as 3-1…", "video ends with blue and white static end screen"을 검색했다. 같은 영상 r2 결론은 앞 섹션의 Dribble Stick·Straight Shooter·Flick Glove를 검색했다(`SELF_CONSISTENCY_CAUSES.md` §2.3).
- 프롬프트 길이는 섹션이 뒤로 갈수록 C0 요약 때문에 늘어난다(`-QuCz7kxBr8` r1: 438 → 1,103토큰).

#### (b) 검색 (Deep-Reporter `search_node` → 검색 서비스, 섹션당 HTTP 2회)

Deep-Reporter가 만든 자연어 query는 **고쳐 쓰거나 키워드로 바꾸지 않고 문장 그대로** 검색에 쓰인다(검색 서비스는 빈 문자열만 뺀다, 코드).
- 검색 서비스(`videorag_retriever_service.py`)는 WorldMM의 추론 루프를 쓰지 않는다. 그 루프는 LLM이 어느 메모리를 볼지 정하고 질의를 다시 쓰는 에이전트다.
- 대신 WorldMM 안의 episodic(HippoRAG)·semantic·visual 검색 부품을 직접 호출한다.

```
Deep-Reporter search_node
  POST /videos/<vid>/search {"query_list": text_queries, "type": "text", "topk": 20}
  (2초 대기)
  POST /videos/<vid>/search {"query_list": image_queries, "type": "image", "topk": 10}
        │
        ▼ 검색 서비스 (영상 1개의 메모리가 올라가 있음)
  text  → episodic: (질의 × 4개 단위) 그래프 검색 → RRF 병합 → L1 필터(LLM 1회) → 8개
        → semantic: 질의마다 triple 검색(PPR) → RRF → 4개
  image → visual:   질의마다 VLM2Vec 유사도 → RRF → 최대 4개 → 구간 중앙 프레임 + 10sec 캡션
```

**요청** (코드)
- 응답 시간 제한은 600초다. 실패하면 근거 0건으로 계속 진행한다(⑦에서 오류).
- 근거 개수
  - text 요청: episodic `min(episodic_k 8, topk 20)` = 8개, semantic `min(semantic_k 4, 남은 topk)` = 4개.
  - image 요청: `min(image_k 4, topk 10)` = 최대 4개.

##### (b-0) 검색 전에 미리 만들어 둔 것: 단위마다 HippoRAG 그래프 1개 (사전 인덱싱, 코드·캐시 실측)

- **passage 노드**: 캡션 1개가 노드 1개다. 노드에 붙는 텍스트는 캡션 원문 그대로다.
- **OpenIE**: 캡션마다 LLM이 개체(NER)와 (주어, 술어, 목적어) triple을 뽑는다. 실제 예(`-QuCz7kxBr8` 10sec, 00:00:40):
  - 캡션: "A person puts on a pair of sports goggles labeled "SPORTS DRIBBLE SPECS" on an outdoor basketball court. …"
  - NER: `SPORTS DRIBBLE SPECS`, `basketball court`, `basketball`, `basketball hoop`, `time trial`
  - triple 8개: `(a person, puts on, SPORTS DRIBBLE SPECS)`, `(a person, holds, basketball)`, `(two men, stand near, basketball hoop)`, `(two men, prepare for, time trial)` 등
- **entity 노드**: triple의 주어·목적어. 소문자로 바꾸고 영문·숫자·공백 외 문자를 공백으로 바꾼다(`text_processing`, 예: `sports dribble specs`).
- **엣지 3종** (그래프는 무방향, `is_directed_graph=False`)

  | 엣지 | 무엇을 잇나 | 가중치 |
  |---|---|---|
  | fact | 같은 triple의 주어 entity – 목적어 entity | 그 쌍이 triple로 나온 횟수 |
  | passage–entity | 캡션 – 그 캡션 triple의 entity | 1.0 |
  | synonym | entity 임베딩 KNN에서 유사도 0.8 이상인 entity끼리(`synonymy_edge_sim_threshold`) | 그 유사도 |

- **임베딩**: Qwen3-Embedding-4B(SentenceTransformer, 2,560차원, 마지막 토큰 pooling, 정규화)로 세 가지를 따로 저장한다.
  - passage: 캡션 원문
  - entity: 개체 문자열
  - fact: triple을 문자열로 바꾼 것, 예: `"('a person', 'puts on', 'sports dribble specs')"`
  - 정규화된 벡터라 내적 = 코사인이다.
  - 모델 설정에 질의용 instruction 프롬프트("Instruct: Given a web search query…")가 있지만 `default_prompt_name`이 null이다. WorldMM은 `prompt_name` 없이 `encode`를 부르므로 **질의와 문서 모두 instruction 없이** 임베딩된다.
- `-QuCz7kxBr8`의 그래프 규모 (캐시 `graph.pickle`·parquet 실측. 엣지 수는 igraph 엣지 수 그대로다. fact 엣지는 (a, b)와 (b, a)가 각각 들어 있고, synonym 엣지도 두 개체 양쪽의 KNN에서 각각 추가될 수 있다. 종류는 passage 노드 포함 여부와 가중치가 정수인지로 나눴다)

  | 단위 | passage | entity | fact | fact / synonym / passage–entity 엣지 |
  |---|---|---|---|---|
  | 10sec | 226 | 1,051 | 2,194 | 3,560 / 3,682 / 3,354 |
  | 30sec | 76 | 1,033 | 1,598 | 2,876 / 3,032 / 1,980 |
  | 3min | 13 | 468 | 448 | 870 / 629 / 561 |
  | 10min | 4 | 320 | 299 | 560 / 369 / 353 |

##### (b-1) text query 하나 × 그래프 하나: 그래프 검색 (`_graph_search`, LLM 없음)

query 문장 하나를 4개 단위의 HippoRAG 그래프에서 따로따로 검색한다. 예: `"first gadget tested: SPORTS DRIBBLE SPECS, rules explained for challenge"`.

1. **query 임베딩**: 문장 전체를 Qwen3-Embedding-4B로 벡터 하나로 만든다(`get_query_embeddings`).
2. **fact 점수**: query 벡터와 그 단위의 **모든 fact 임베딩**의 내적(코사인)을 구하고, min-max 정규화로 0–1로 맞춘다(`get_fact_scores`).
   - 상대 점수라서 정말 관련 있는 fact가 없어도 가장 높은 fact는 1이 된다.
3. **상위 5 fact**: 점수 상위 5개(`linking_top_k=5`) triple을 고른다.
   - 원래 HippoRAG(`retrieve` → `rerank_facts`)는 여기서 LLM(DSPy)으로 fact를 한 번 더 거른다.
   - L0·L1 모드에서는 이 LLM 단계를 빼고 점수 상위 5개를 그대로 쓴다.
4. **PPR 출발점 만들기** (`graph_search_with_fact_entities`). PPR의 reset 벡터는 무작위 걷기가 다시 돌아가 시작하는 지점의 분포다.
   - **entity 쪽**: 5개 fact의 주어·목적어 entity마다 가중치 = fact 점수 ÷ (그 entity가 들어 있는 캡션 수).
     - 여러 캡션에 흔히 나오는 개체(예: `a person`)일수록 작아진다.
     - 같은 entity가 여러 fact에 나오면 평균을 낸다.
     - 그 가운데 상위 5개 entity만 남기고 나머지 entity는 0으로 둔다(`get_top_k_weights`).
   - **passage 쪽**: query 벡터와 **모든 캡션** 임베딩의 유사도를 min-max 정규화하고 × 0.05(`passage_node_weight`)를 출발 가중치로 준다(dense passage retrieval 점수). 모든 캡션이 작은 출발 가중치를 갖는다.
5. **PPR**: igraph `personalized_pagerank`
   - 설정: 무방향, 엣지 `weight` 사용, damping 0.5(HippoRAG 기본값, WorldMM이 바꾸지 않음), reset = 4의 가중치.
   - 출발점에서 fact·synonym·passage–entity 엣지를 따라 점수가 퍼진다.
   - 결과적으로 "query와 비슷한 fact의 개체에 연결된 캡션"과 "query와 직접 비슷한 캡션"이 높아진다.
6. **캡션 순위**: passage 노드의 PPR 점수로 정렬한다. 단위별 상위 10sec 3 / 30sec 3 / 3min 2 / 10min 1개를 후보로 가져온다(`episodic_candidates_per_query`).

- 예외 처리
  - fact가 하나도 없으면 4–5 없이 캡션 유사도(dense)만으로 정렬한다.
  - 출발점 합이 0이라 assert로 실패하는 등 그래프 검색이 예외로 끝나도 dense로 대체한다(경고 로그 `graph search failed`).
  - 예시 실행 9건의 서비스 로그에서는 대체가 0건이었다(실측).
- 4단계의 0.05와 5단계의 0.5는 HippoRAG 기본 설정이고, `config.yaml`로 바꾸지 않는다.

##### (b-2) 섹션 안의 병합: RRF (LLM 없음)

- 섹션의 query가 3개면 (3 질의 × 4 단위) = 최대 12개 순위 목록이 생긴다.
- 캡션 id마다 RRF 점수 = Σ 1 / (60 + 그 목록에서의 순위)로 합치고, 같은 캡션은 하나로 합친다(`rrf_k` = 60).
- 예시 18건(r1 3건 × 6섹션)의 병합 후보 수는 16–26개였다(서비스 로그 `episodic_candidates`, 실측).
- 후보가 8개 이하이면 L1 필터를 건너뛰고(`episodic_filter: "skipped(<=n)"`) RRF 순서를 그대로 쓴다.

##### (b-3) L1 필터: LLM이 8개 고르기 (섹션당 LLM 1회, WorldMM `_filter_with_llm`)

- **메시지** (3개, WorldMM `multiscale_filter` 템플릿 + 우리가 넘기는 질문)
  - system: "영상 캡션을 질의에 맞게 고르고 순위를 매기는 전문가" 역할 설명
  - user 1: 지시 6개
    - 질문 성격에 맞게 단위를 고를 것(특정 사건이면 세밀한 단위, 습관·관계·일반 질문이면 큰 단위)
    - 각 캡션의 시간 범위를 볼 것
    - 관련성을 판단할 것
    - 질문에 직접 도움이 되는 것만 고를 것
    - ID를 관련 순으로 낼 것
    - 정말 관련 있는 것만 넣을 것
  - user 2: 다음을 이어 붙인 것
    - `Question: <섹션의 text query들을 "; "로 이은 문자열>`
    - `Retrieved Captions:` + RRF 순서의 후보 JSON 배열. 항목 예: `{"id": "10sec_4", "granularity": "10sec", "start_time": "DAY1 00:00:40", "end_time": "DAY1 00:00:50", "text": <캡션 전문>}`
    - `Select the top 8 most relevant caption IDs to answer the question. Return ONLY a JSON array of caption IDs in order of relevance (most relevant first).`
- 캡션 **전문**이 들어가서 예시의 필터 프롬프트는 6,205–15,486토큰, 출력은 64–76토큰, 4.1–6.3초였다(실측). temperature 0.7 샘플링이다(②).
- **응답 처리** (코드)
  - 응답에서 첫 `[...]`를 JSON으로 읽고 실제 후보 ID만 남긴다. JSON을 못 읽으면 응답 문자열에 들어 있는 후보 ID를 찾는다.
  - 앞에서부터 8개를 **LLM이 낸 순서대로** 쓴다. 8개가 안 되면 RRF 순위로 채운다.
  - LLM 호출이 실패하면 RRF 상위 8개를 쓰고 `episodic_filter: "fallback_rrf(llm_failed)"`로 표시한다. 호출은 성공했지만 응답을 못 읽어 RRF로 채운 경우는 `llm`으로 표시된다(I16).
- 결과 항목의 `score`는 RRF 값 그대로이고, 순서만 LLM이 정한 순서다(`score_type: "rrf(order=llm_filter)"`).
- **기록되지 않는 것**: 후보 목록과 LLM 응답 원문은 로그에 남지 않는다. 그래서 무엇이 버려졌는지는 볼 수 없다(§7).

##### (b-4) semantic 검색 (LLM 없음, 시간 정보 없음, WorldMM `SemanticMemory`)

- **데이터**: WorldMM 전처리가 영상 전체에서 뽑아 통합한 triple 중 **마지막 시점 묶음**(검색 시각 `query_time` 이전의 가장 늦은 묶음)이다. `-QuCz7kxBr8`은 triple 153개, entity 173개다(실측).
- **색인** (영상을 불러올 때)
  - entity를 노드로 두고 triple마다 주어–목적어 엣지를 잇는다(무방향, 가중치 없음).
  - triple을 `"subject predicate object"` 문장으로 이어 Qwen3-Embedding으로 임베딩한다.
- **query 하나의 검색** (`retrieve`, `top_k = semantic_k_per_query = 5`)
  1. query 임베딩과 모든 triple 임베딩의 코사인을 구해 상위 5 triple을 고른다.
  2. 그 5개 triple의 주어·목적어 entity를 출발점으로 한다(균등 가중치).
  3. PPR(무방향, damping 0.85)을 돌린다.
  4. **모든 triple**의 점수 = PPR(주어) + PPR(목적어)로 매겨 상위 5개를 고른다.
- 질의들의 결과를 RRF로 합쳐 4개를 낸다.
- **최종 순위에 query 유사도가 직접 들어가지 않는다**(코드). 연결이 많은 개체가 들어간 triple이 쉽게 올라온다.
  - `-QuCz7kxBr8`에서 연결이 가장 많은 개체는 `player`(20개 triple), `man`(19), `basketball court`(9), `basketball`(7), `third man`(6)이다.
  - 3회 실행에서 검색된 semantic 72건 중 25건이 이 5개 개체(전체 173개 중 5개)를 포함했다(실측).
  - 아래 "보이는 점"의 사소한 semantic 근거가 나오는 이유로 보인다(가설).

##### (b-5) image 검색 (LLM 없음, WorldMM `VisualMemory`)

- **미리 만든 것**: 10sec 구간마다 VLM2Vec-V2 비디오 임베딩 1개(`visual_embeddings.pkl`, 키 = 구간 시작 시각).
  - 50개 영상 전처리 설정(`process_one_video.sh --num-frames 10`): 구간에서 10프레임, 최대 360×420픽셀(`max_pixels` 기본값), 프롬프트 "Represent the given video.", 정규화된 벡터.
- **query 하나의 검색** (`_retrieve_by_similarity`)
  1. image query 문장을 VLM2Vec **텍스트 임베딩**으로 바꾼다(`encode_vis_query`, instruction 없음).
  2. 모든 10초 구간 임베딩과 코사인 유사도를 구해 상위 3구간(`visual_k_per_query`)을 고른다.
  - WorldMM의 `retrieve()` 대신 이 함수를 직접 부른다. `retrieve()`는 "DAY X HH:MM:SS - …" 모양의 문자열을 시간 범위 질의로 해석해 다른 경로로 보내기 때문이다(I13).
- **결과 만들기**
  - 질의들의 결과를 RRF로 합쳐 최대 4개(`image_k`)를 낸다. 예시는 image query가 섹션마다 1개라 3개였다.
  - 구간 **중앙 시각**((시작 + 끝) / 2)의 프레임을 decord로 뽑아 `{frames_dir}/{vid}/{start_time}.jpg`로 저장한다. 이미 있으면 그대로 쓴다.
  - 같은 시작 시각의 10sec 캡션을 붙여 `caption = "[HH:MM:SS-HH:MM:SS | video frame at Xs] <10sec 캡션>"`을 만든다.
- 이미지는 텍스트 근거와 연결 없이 영상 전체에서 따로 찾는다. 이미지에는 LLM 필터가 없다(Deep-Reporter filter 노드 꺼짐).
- writer는 이미지 픽셀을 보지 않고 이 `caption` 문자열만 본다(④-2(c)).

##### (b-6) 응답에 담기는 순서와 요약

- text 응답은 episodic 8개(L1 필터 순서) 다음 semantic 4개 순서다. writer는 이 순서대로 txt1–txt12로 본다.
- image 응답은 RRF 순서이고, writer는 img1–img3으로 본다.

| 검색 | query 문장이 쓰이는 곳 | LLM | 최종 순위를 정하는 것 |
|---|---|---|---|
| episodic | fact 임베딩·캡션 임베딩과 비교 → PPR 출발점 | 섹션당 1회(L1 필터) | 단위별 그래프 PPR → RRF → **LLM이 고른 8개** |
| semantic | triple 임베딩과 비교 → 상위 5 triple의 개체가 PPR 출발점 | 0 | 개체 PPR 합(유사도 직접 미반영) → RRF → 4개 |
| image | VLM2Vec 텍스트 임베딩 ↔ 10초 구간 비디오 임베딩 코사인 | 0 | 유사도 상위 3 → RRF → 최대 4개 |

- 모드: L0은 L1 필터 없이 RRF 상위 8개(LLM 0회). full은 WorldMM 원본 `episodic_memory.retrieve`로, 질의마다 DSPy fact 필터와 multiscale 필터를 쓴다(질의당 최대 5회). 기본은 L1(`retrieval.episodic_filter`).

**근거 항목의 실제 모양** (`report.json`, `-QuCz7kxBr8` r1 섹션 1의 txt1·txt9·img1, 긴 값은 줄임)
```json
{"id": "-QuCz7kxBr8:episodic:3min_0", "uid": "-QuCz7kxBr8:episodic:3min_0", "source": "worldmm-episodic", "score": 0.032787,
 "score_type": "rrf(order=llm_filter)", "rank": 1, "video_id": "-QuCz7kxBr8", "type": "text",
 "content": "[00:00:00-00:03:00 | episodic 3min] Six men—Chris, Zach, Cass, James, Mitchell, and a sixth unnamed player—gather on …",
 "text": "Six men—Chris, Zach, …", "granularity": "3min", "start_time": "00000000", "end_time": "00030000",
 "start_sec": 0.0, "end_sec": 180.0, "video_path": "…/-QuCz7kxBr8.mp4"}
{"uid": "-QuCz7kxBr8:semantic:semantic_100373700_44", "source": "worldmm-semantic", "type": "text",
 "content": "[video-level knowledge | semantic] (The text overlay, reads, 20 LOW, MEDIUM, & HIGH DRIBBLES IN 60 SECONDS)",
 "start_time": null, "end_time": null, "time_grounded": false, …}
{"uid": "-QuCz7kxBr8:visual:00344000", "source": "worldmm-visual", "type": "image", "frame_sec": 2085.0,
 "img_path": "…/frames_s0/-QuCz7kxBr8/00344000.jpg",
 "caption": "[00:34:40-00:34:50 | video frame at 2085.0s] On an outdoor basketball court under a clear blue sky, a player …", …}
```

**예시 1: `-QuCz7kxBr8` r1 섹션 1 (도입)** — 요청 기록: 질의 2개, 후보 17개, 필터 `llm`, text 12.19초 / image 1.28초. 전체 원문은 `s01/3_retrieval.md`. "인용" = 이 섹션 본문(반복 제거 후)이 인용한 것.

text_queries: `six players introduced: Chris, Zach, Cass, James, Mitchell, and sixth unnamed player` / `first gadget tested: SPORTS DRIBBLE SPECS, rules explained for challenge`  
image_queries: `six people standing on a sunny outdoor basketball court, wearing casual sportswear, ready to play`

| 번호 | 인용 | 단위 | 시간 | 내용(앞부분) |
|---|---|---|---|---|
| txt1 | ✓ | 3min | 00:00:00–00:03:00 | Six men—Chris, Zach, Cass, James, Mitchell, and a sixth unnamed player—gather on a sunny outdoor basketball court to test 12 viral sports gadgets, splitting into two team … |
| txt2 | ✓ | 30sec | 00:00:00–00:00:30 | A group of six men—Chris, Zach, Cass, James, and Mitchell—gather on a sunny outdoor basketball court to test 12 viral basketball gadgets, splitting into two teams of thre … |
| txt3 | ✓ | 10min | 00:00:00–00:10:00 | **Six men—Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player—gather on a sunny outdoor basketball court to test 12 viral sports gadgets, splitting into two t … |
| txt4 | ✓ | 30sec | 00:00:30–00:01:00 | A group of men on an outdoor basketball court introduces a gadget challenge where teams will select and test their favorite sports gear. The segment kicks off with one ma … |
| txt5 |  | 10sec | 00:00:40–00:00:50 | A person puts on a pair of sports goggles labeled "SPORTS DRIBBLE SPECS" on an outdoor basketball court. Another person watches as the first person adjusts the goggles. T … |
| txt6 | ✓ | 30sec | 00:02:30–00:03:00 | Three men gather on an outdoor basketball court, preparing for a dribbling challenge using a SKLZ Dribble Stick. The man in the red hoodie introduces the game, asking if … |
| txt7 | ✓ | 30sec | 00:02:00–00:02:30 | Three young men stand on an outdoor basketball court, each holding a ball, engaged in a discussion about dribbling drills and the usefulness of a gadget that helps player … |
| txt8 | ✓ | 10sec | 00:01:40–00:01:50 | At an outdoor basketball court beside a pool, a man in a white hoodie and patterned shorts holds a basketball while talking to another player in a tie-dye jersey. The pla … |
| txt9 |  | semantic | 시간 없음 | (The text overlay, reads, 20 LOW, MEDIUM, & HIGH DRIBBLES IN 60 SECONDS) |
| txt10 |  | semantic | 시간 없음 | (player, can be defended by, another player) |
| txt11 |  | semantic | 시간 없음 | (challenge, penalizes least baskets with, 100 sit-ups) |
| txt12 | ✓ | semantic | 시간 없음 | (player, can gesture and talk to, another player) |
| img1 | ✓ | 프레임 | 00:34:45 (구간 00:34:40–00:34:50) | On an outdoor basketball court under a clear blue sky, a player in a white jersey and orange shoes, carrying large cylindrical training pads, prepares to defend against a … |
| img2 |  | 프레임 | 00:28:45 (구간 00:28:40–00:28:50) | Six men stand on an outdoor basketball court under a clear blue sky. One man in the center holds a basketball and slightly shifts his position, while the others remain mo … |
| img3 | ✓ | 프레임 | 00:28:55 (구간 00:28:50–00:29:00) | Six men are gathered on an outdoor basketball court under a clear blue sky. One man in the center, wearing a white hoodie and blue shorts, holds a basketball and gestures … |

**예시 2: `0RxMZBLeqRI` r1 섹션 5 (나치·공산 정권 박해)** — 질의 3개, 후보 20개, text 7.02초. 이 섹션은 writer가 상한에서 끊긴 섹션이다(④-2(c) 예시 3).

text_queries: `text overlay states 500,000–1,500,000 Roma deaths` / `archival footage of Roma deportation to Auschwitz-Birkenau` / `Gestapo mugshots of Roma individuals shown with identification tags`  
image_queries: `black-and-white archival footage of Roma prisoners in striped uniforms walking in a line through a camp gate`

| 번호 | 인용 | 단위 | 시간 | 내용(앞부분) |
|---|---|---|---|---|
| txt1 | ✓ | 3min | 00:21:00–00:24:00 | **[Event 1: Historical Roots of Romani Persecution]**   The video opens with archival visuals—black-and-white footage of Romani people, 1880s illustrations, and portraits … |
| txt2 | ✓ | 30sec | 00:24:00–00:24:30 | A black-and-white historical montage opens with a group of men and children seated in an open field, framed by a fence and a solitary figure in the distance, suggesting a … |
| txt3 | ✓ | 30sec | 00:23:00–00:23:30 | **[Event 1: Intimate Wedding Transition to Historical Ceremony]**   The segment opens with a black-and-white close-up of a bride and groom sharing an intimate moment, tra … |
| txt4 | ✓ | 10sec | 00:24:10–00:24:20 | The video shows a black-and-white historical segment featuring a group of people, many appearing distressed or emaciated, standing behind a fence. The camera zooms in on … |
| txt5 | ✓ | 30sec | 00:22:00–00:22:30 | **[Event 1: Display of Nazi Racial Classification Document]**   The video opens with a historical document titled *Die Nürnberger Gesetze* (The Nuremberg Laws), which sys … |
| txt6 | ✓ | 10sec | 00:23:20–00:23:30 | A black-and-white historical segment begins with a woman in a headscarf looking out from behind a wooden door. The scene transitions to a group of men in striped prison u … |
| txt7 | ✓ | 10sec | 00:23:40–00:23:50 | The video begins with a person in a dark hooded garment holding a knife, followed by a still image of Josef Mengele with his name displayed. The scene then transitions to … |
| txt8 |  | 10sec | 00:21:00–00:21:10 | A text overlay explains that German laws against Romani people had been in effect for hundreds of years before the Nazis came to power in 1933, and that persecution began … |
| txt9 |  | semantic | 시간 없음 | (poster, has news headline, ROMANIAN GOVERNMENT ACKNOWLEDGES RESPONSIBILITY FOR ANTI-ROMANI POGROMS) |
| txt10 |  | semantic | 시간 없음 | (poster, has text in, Romanian) |
| txt11 |  | semantic | 시간 없음 | (Video, begins with, title card reading GYPSIES) |
| txt12 |  | semantic | 시간 없음 | (final text overlay, cites, 400,000 Muslim Gypsies affected) |
| img1 |  | 프레임 | 00:24:05 (구간 00:24:00–00:24:10) | The video segment shows a series of black-and-white historical images. It begins with a group of men and children sitting on the ground in an open field, with a fence and … |
| img2 |  | 프레임 | 00:24:45 (구간 00:24:40–00:24:50) | The video transitions through several distinct scenes. It begins with a black-and-white shot of a large crowd of people, many in striped uniforms, walking in an outdoor a … |
| img3 |  | 프레임 | 00:24:25 (구간 00:24:20–00:24:30) | The video begins with a black-and-white shot of a group of people standing behind a barbed-wire fence, then cuts to a black screen before displaying the title "Communism, … |

**예시 3: `54k2g9ddy4M` r1 섹션 3 (Montfort 병원 + Liendo 금메달)** — 질의 3개, 후보 24개, text 6.24초.

text_queries: `Heather Insley identifies her son as a stranger after hospital misidentification` / `CBC News reports Montfort Hospital’s official statement and review process` / `Joshua Liendo wins gold medal in Men’s 100m Butterfly at Commonwealth Games`  
image_queries: `A grieving mother holding her child’s hand in a hospital hallway, visibly distraught`

| 번호 | 인용 | 단위 | 시간 | 내용(앞부분) |
|---|---|---|---|---|
| txt1 | ✓ | 30sec | 00:21:00–00:21:30 | A misidentification incident at Montfort Hospital, confirmed on February 23, 2024, involved a patient whose true identity was later verified — leading to the tragic reali … |
| txt2 | ✓ | 10min | 00:20:00–00:30:00 | **[Event 1: Misidentification Tragedy at Montfort Hospital]**   On February 23, 2024, Montfort Hospital confirmed a fatal misidentification: a deceased patient, mourned b … |
| txt3 | ✓ | 30sec | 00:20:30–00:21:00 | A grieving mother, Heather Insley from Picton, Ontario, recounts how her family mourned the death of their son—only to later discover he was a stranger—after his passing … |
| txt4 | ✓ | 10sec | 00:20:50–00:21:00 | Heather Insley, identified as a mother from Picton, Ontario, is shown in a CBC News interview discussing the tragic event where her family mourned the death of their son … |
| txt5 | ✓ | 10sec | 00:21:00–00:21:10 | A document from Montfort Hospital is displayed, detailing a statement regarding a misidentification incident. Text overlays highlight key points: “...misidentification... … |
| txt6 | ✓ | 30sec | 00:21:30–00:22:00 | A grieving woman in a red sweater and glasses speaks emotionally to an interviewer in a living room, her sorrow evident as she reflects on the loss of her son — only to l … |
| txt7 | ✓ | 10sec | 00:21:30–00:21:40 | A woman in a red sweater and glasses speaks emotionally to an interviewer in a living room, her expression conveying grief. The scene cuts to a man in a red plaid hoodie … |
| txt8 | ✓ | 10min | 00:10:00–00:20:00 | **[Event 1: Rising Airline Fees Amid Falling Fares]**   Canadian airfares dropped 14.3% from January 2023 to 2024, yet airline fees continue to climb, creating a financia … |
| txt9 | ✓ | semantic | 시간 없음 | (document, issued by, Montfort Hospital) |
| txt10 | ✓ | semantic | 시간 없음 | (on-screen text, reads, Family mourns son's death before realizing it was a stranger) |
| txt11 |  | semantic | 시간 없음 | (news story, is about, Coroner investigating 3rd death in Quebec hospital waiting room) |
| txt12 |  | semantic | 시간 없음 | (Joshua Liendo, swims, freestyle) |
| img1 | ✓ | 프레임 | 00:20:35 (구간 00:20:30–00:20:40) | The video shows a hospital scene where a person is lying in a bed with medical equipment, including an oxygen tube and a ventilator, suggesting they are critically ill or … |
| img2 |  | 프레임 | 00:22:15 (구간 00:22:10–00:22:20) | A woman in a red sweater and glasses speaks indoors, with a stained-glass lamp visible behind her. The scene cuts to a male reporter, Dan Taekema of CBC News, standing ou … |
| img3 |  | 프레임 | 00:20:25 (구간 00:20:20–00:20:30) | The video opens with an exterior shot of a hospital, showing a parking lot filled with cars and the building's facade under a clear blue sky. A black car drives past, and … |

**보이는 점** (실측·대조)
- 예시 1: 텍스트 근거는 모두 00:00–03:00 근처다(10min 1개 제외). 그런데 이미지 3장은 00:28:45, 00:28:55, 00:34:45다. 이미지는 image query로 영상 전체에서 따로 찾기 때문이다(P14).
- 예시 2: 30sec·3min 요약이 "The video opens with…", "The video begins with…"로 시작한다. 그 구간의 시작이라는 뜻인데, writer가 "At 00:23:40, the video begins with…"라고 옮겼다(결말·시작 검사 `opening_unverifiable`).
- 예시 3
  - Liendo 질의에 대응하는 episodic 근거는 20–30분 10min 요약(txt2) 하나뿐이고, 10–20분 10min 요약(txt8, 항공 요금 꼭지)이 함께 들어왔다.
  - writer는 Liendo 문장에 txt8과 Montfort 문서 triple(txt9)을 인용했다. 둘 다 Liendo 내용이 아니다.
  - 숫자·따옴표가 없는 문장이라 규칙 검사로는 잡히지 않는다.
- semantic 근거는 사소한 것이 많다. 예: `(player, can gesture and talk to, another player)`, `(Joshua Liendo, swims, freestyle)`. 최종 순위가 개체 PPR 합으로만 정해지는 방식과 관련이 있어 보인다((b-4), 가설).

#### (c) writer: 섹션 본문 쓰기 (LLM 1회)

**입력 구성** (Deep-Reporter `section_writing_node` + `domain_templates.VIDEOMME_SECTION`, 코드)

| 부분 | 내용 |
|---|---|
| Role | 영상 하나에 대한 보고서의 한 섹션을 근거로만 쓴다 |
| Overall Report Context | 질의, checklist |
| Current Section Information | `Section Position: Section k/N`, 섹션 설명, checklist("근거가 뒷받침하는 요구사항은 모두 다룰 것") |
| Context from Previous Sections | 앞 섹션 요약(C0), 직전 섹션 끝부분(tail: 본문을 `.`으로 나눈 마지막 3조각) |
| Retrieved Evidence | `[Source txtN begin]` + 근거 `content` + `[Source txtN end]` (N = 1–12), `[Source imgN: caption]` (N = 1–3). **이미지는 그림이 아니라 캡션 문자열로만 들어간다**(Deep-Reporter는 텍스트 메시지만 보냄) |
| How to read the evidence | episodic(시간·단위 표시), semantic(시간 없음), 이미지 근거 읽는 법 |
| (2026-10-26 추가) End of the Video | 영상 끝 근거 txt0과 "마지막 섹션에서만 인용" 지시 |
| Grounding Rules 1–7 | 근거에 있는 것만, 시간은 근거의 HH:MM:SS만, 충돌 시 세밀한 단위 우선, 없으면 없다고, 시간순, 반복 금지(규칙 6), 구간 요약의 "opens/closes"는 그 구간의 일(규칙 7, 실제 끝 시각 포함) |
| Citation Rules 1–4 | 문장마다 `[citation:txtN]`, 이미지는 단독 줄 `![](citation:imgN)`, 괄호 하나에 출처 하나, `[citation:imgN]` 금지 |
| Position-Aware | 첫·마지막 섹션 여부(`is_first_section`, `is_last_section`), 위치별 지시 |
| Conclusion Section | `Conclusion:` 섹션은 100–250단어, 앞 결과만 요약 |
| Format | `# 제목`으로 시작, 보통 250–700단어, 본문만 출력 |

**실제 writer 프롬프트** (`-QuCz7kxBr8` r1 섹션 2, 전체 23,002자 = 5,287토큰. 근거 블록은 앞 160자, 이미지 캡션은 앞 140자만 싣고 생략 표시. 전문: `s02/4_writer_prompt.md`)

```
# Role
You are an expert writer producing one section of a report about ONE specific video. The report must be grounded only in evidence retrieved from that video.

# Overall Report Context
**Report Topic:** Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.

**Overall Requirements:**


# Current Section Information
**Section Position:** Section 2/6
**Section Description:** This section details the testing of the SKLZ Dribble Stick and the subsequent shooting challenge with the Straight Shooter Strap. It covers the rules, player reactions, and scoring, including humorous commentary and a forfeit challenge involving jumping jacks. Readers learn how the group evaluates the gadgets’ usefulness and how the testing evolves into physical challenges.

**Section Requirements (address every requirement the evidence supports):**
- Describe the SKLZ Dribble Stick’s rules and how it is tested
- Note the Straight Shooter Strap’s demonstration and player feedback
- Record the forfeit challenge (jumping jacks) and its humorous context

# Context from Previous Sections
**Summary of previous sections:**
Already written in earlier sections (title, then the first sentence of each paragraph; citation numbers removed - they do NOT refer to the evidence of the current section):
Section 1: Introduction to the Participants and Setting
- Six men—Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player—are introduced as the main participants in the video.
- The video’s goal is established early: to test and evaluate the gadgets in a hands-on, competitive, yet lighthearted manner.
- The group’s interaction remains informal and humorous, with teammates reacting to performance with thumbs-up approval and score graphics flashing from 5 to 6, then 4.

**End of previous section (for a smooth transition):**
The group is ready to begin the next round, setting up for continued testing [citation:txt1][citation:txt6].  The video’s opening minutes establish the tone, participants, setting, and initial challenge, grounding the viewer in the context of the gadget testing. 

![](citation:img3)

# Retrieved Evidence from the Video
[Source txt1 begin]
[00:00:00-00:10:00 | episodic 10min] **Six men—Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player—gather on a sunny outdoor basketball court to tes …
[Source txt1 end]

[Source txt2 begin]
[00:03:00-00:06:00 | episodic 3min] Three men gather on an outdoor basketball court, negotiating positions before settling into a shooting challenge. One man in …
[Source txt2 end]

[Source txt3 begin]
[00:02:30-00:03:00 | episodic 30sec] Three men gather on an outdoor basketball court, preparing for a dribbling challenge using a SKLZ Dribble Stick. The man in …
[Source txt3 end]

[Source txt4 begin]
[00:02:50-00:03:00 | episodic 10sec] A close-up shot shows a black "Dribble Stick" device with a yellow logo. The scene then transitions to an outdoor basketbal …
[Source txt4 end]

[Source txt5 begin]
[00:02:40-00:02:50 | episodic 10sec] A man in a red hoodie holds a basketball while standing on a basketball court with two other men, one in a blue jersey and …
[Source txt5 end]

[Source txt6 begin]
[00:04:30-00:05:00 | episodic 30sec] A man in a white hoodie demonstrates a black elbow strap called the “Straight Shooter Strap” on an outdoor basketball court …
[Source txt6 end]

[Source txt7 begin]
[00:07:20-00:07:30 | episodic 10sec] Three men are on an outdoor basketball court. One man in a white t-shirt and patterned shorts is performing jumping jacks w …
[Source txt7 end]

[Source txt8 begin]
[00:07:00-00:07:30 | episodic 30sec] A player in a white shirt and patterned shorts attempts a jump shot that misses, prompting frustration and speculation abou …
[Source txt8 end]

[Source txt9 begin]
[video-level knowledge | semantic] (player, can dribble, basketball)
[Source txt9 end]

[Source txt10 begin]
[video-level knowledge | semantic] (on-screen text, reads, MOST DRIBBLES IN 15 SECONDS)
[Source txt10 end]

[Source txt11 begin]
[video-level knowledge | semantic] (player, uses, Straight Shooter Strap)
[Source txt11 end]

[Source txt12 begin]
[video-level knowledge | semantic] (Jadil, has bigger chest than, man doing jumping jacks)
[Source txt12 end]

[Source img1: [00:02:50-00:03:00 | video frame at 175.0s] A close-up shot shows a black "Dribble Stick" device with a yellow logo. The scene then transiti …

[Source img2: [00:15:30-00:15:40 | video frame at 935.0s] On an outdoor basketball court, a man with blonde hair wearing a black t-shirt and gloves dribbl …

[Source img3: [00:22:10-00:22:20 | video frame at 1335.0s] A man with blond hair, wearing a black t-shirt and pink shorts, is on an outdoor basketball cou …

## How to read the evidence
- Text sources starting with "[HH:MM:SS-HH:MM:SS | episodic <scale>]" describe that part of the video (built from its frames and speech). Scales 10sec and 30sec give fine details; 3min and 10min are summaries of longer spans.
- Text sources starting with "[video-level knowledge | semantic]" are facts inferred from the whole video, written as (subject, predicate, object). They have NO timestamp.
- Image sources "[Source imgN: [HH:MM:SS-HH:MM:SS | video frame at Xs] description]" are frames taken from the video at that moment, with a description of that moment.

# Grounding Rules (CRITICAL)
1. State only what the evidence supports. Do not add outside knowledge, assumptions, or speculation about intentions or feelings unless the evidence states them.
2. When describing an event, give its time from the evidence in HH:MM:SS form (e.g., "At 00:12:40, ..."). Never invent or estimate times that are not in the evidence. Do not attach times to video-level knowledge.
3. If sources conflict, prefer the finer-scale (10sec/30sec) description and mention the uncertainty.
4. If the evidence does not cover a requirement, say briefly that the retrieved footage does not show it instead of filling the gap. If no evidence was retrieved at all, write a short section that says so.
5. Describe events in chronological order unless the section needs another structure.
6. Do not repeat a fact, sentence, or paragraph you have already written in this section. If a fact was already covered in a previous section (see "Context from Previous Sections"), mention it in at most one short sentence and focus on what is new in this section. Exception: a conclusion section (see "Conclusion Section") restates earlier results briefly by design.
7. Each text source covers only its own time span. Words such as "the video opens", "begins", "closes", "ends" or "concludes" inside a 30sec, 3min or 10min summary refer to the start or end of THAT span, not of the whole video. The whole video runs from 00:00:00 to 00:37:37. Describe how the whole video begins or ends only with sources whose time range reaches its first or last minutes; otherwise do not claim how the video begins or ends.

# Citation Rules (CRITICAL)
1. Text citation: put [citation:txt1], [citation:txt2], ... at the end of each sentence or claim that uses a text source. Every factual sentence needs at least one citation.
2. Image citation: to show a frame, put ![](citation:img1), ![](citation:img2), ... on its own line right after the sentence describing that moment. Use only sources marked as images, and include the 1-3 most relevant frames when available.
3. Use exactly these formats with one source per bracket; for several sources write [citation:txt1][citation:txt3].
4. Never write [citation:imgN]: an image source is cited ONLY as ![](citation:imgN) on its own line, and [citation:...] is used ONLY for txt sources.

# Position-Aware Writing Instructions
**Is this the FIRST section?** no
**Is this the LAST section?** no
- FIRST section: open by introducing the video and what the report covers; do not conclude the report.
- MIDDLE section: start with a smooth transition; do not use concluding phrases such as "In conclusion", "To summarize", or "Overall, this report".
- LAST section: you may synthesize the main points of the whole report, using only evidence-supported statements.

# Conclusion Section
If the Section Description starts with "Conclusion:", write a brief conclusion of 100-250 words: summarize only the main results already covered by the previous sections and answer the report topic at a high level. Do not introduce new events or details, keep at most one short paragraph per checklist item, and still cite the evidence above for every factual statement. If you state how the video ends, follow Grounding Rule 7.

# Format
- Start with a section title written as "# Title"; use "##" for subsections if needed.
- Typically 250-700 words, depending on how much evidence is available (a conclusion section: 100-250 words).
- Output ONLY the section content, without meta-commentary.

Begin writing the section now:
```

**예시 1: `-QuCz7kxBr8` r1 섹션 1 writer 출력 원문** (624토큰, `stop`, 28.6초. `s01/5_writer_output_raw.md`)

```
# Introduction to the Participants and Setting

Six men—Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player—are introduced as the main participants in the video. They gather on a sunny outdoor basketball court, dressed in athletic wear and holding basketballs near a hoop and trees [citation:txt2]. One man, wearing a white hoodie and blue shorts, addresses the camera directly, setting a playful and competitive tone with audio cues such as “Hands up, hands up” and “Mump is blinding me” [citation:txt2]. The group splits into two teams of three, preparing to test 12 viral sports gadgets, with six assigned per team [citation:txt2]. The setting is clearly outdoors, under bright sunlight, with visible trees, a fence, and in some shots, a pool and hills in the background [citation:txt3][citation:txt4]. The court features a painted “HYPE” logo and a basketball hoop, reinforcing the casual, recreational environment [citation:txt12][citation:img1].

The video’s goal is established early: to test and evaluate the gadgets in a hands-on, competitive, yet lighthearted manner [citation:txt1]. The first gadget tested is the “SPORTS DRIBBLE SPECS,” introduced with a close-up of black nylon straps and buckles, signaling the start of the gear review [citation:txt2][citation:txt3]. The challenge begins with a dribbling time trial, where participants must dribble through three cones and touch a pole to stop the clock [citation:txt4]. The rules are clarified near the pool under bright sunlight, with the man in the white hoodie confirming that the slowest time results in a forfeit [citation:txt1][citation:txt4]. The first round features players like Chris and Zach showcasing speed and control, with timers capturing times such as 10:85 and 9:51 seconds [citation:txt1]. Commentary highlights both frustrations (“handles were definitely off”) and praise (“He’s making great time”), reinforcing the competitive yet casual atmosphere [citation:txt1][citation:txt8].

The group’s interaction remains informal and humorous, with teammates reacting to performance with thumbs-up approval and score graphics flashing from 5 to 6, then 4 [citation:txt7]. The segment concludes with the introduction of the next gadget: the SKLZ Dribble Stick—a black training tool with adjustable yellow arms—where the blue-jerseyed player prepares to demonstrate its use [citation:txt1][citation:txt6]. Rules for this challenge are reviewed: players dribble while avoiding the stick; the first to touch it must run five laps [citation:txt6]. The group is ready to begin the next round, setting up for continued testing [citation:txt1][citation:txt6]. The video’s opening minutes establish the tone, participants, setting, and initial challenge, grounding the viewer in the context of the gadget testing.

![](citation:img3)
```

- 첫 문장에 인용이 없다.
- "HYPE" 로고 문장의 `txt12`는 semantic `(player, can gesture and talk to, another player)`로 뒷받침이 되지 않는다.
- `[citation:img1]`은 금지 형식이고, 그 프레임은 00:34:45 수비 훈련 장면이다(대조).

**예시 2: `54k2g9ddy4M` r1 결론(섹션 6) writer 출력 원문** (475토큰, `stop`, 21.7초. `s06/5_writer_output_raw.md`)

```
# Conclusion

The video presents a layered narrative that intertwines public health crises, institutional failures, and athletic triumph, ultimately concluding with themes of community recovery and athletic legacy. Public health concerns are prominently featured, including a measles outbreak in the United States with 41 confirmed cases and a third patient death in a Montreal hospital, underscoring systemic vulnerabilities in emergency response and disease containment [citation:txt1][citation:txt2]. These crises are juxtaposed with institutional failures, such as the misidentification tragedy at Montfort Hospital, where a grieving family mourned the loss of a son only to later discover he was a stranger — a case that highlights profound systemic breakdowns in healthcare [citation:txt3]. The video also documents the devastating fire that destroyed the only school on Eabametoong First Nation, leaving behind charred ruins and triggering a community-wide crisis, with inadequate infrastructure and delayed government support compounding the trauma [citation:txt4][citation:txt5][citation:txt6]. Yet, the narrative pivots toward recovery, showing the eventual construction of new schools in Pikangikum and Wapekeka First Nations, symbolizing resilience and the fulfillment of long-delayed promises [citation:txt7][citation:txt8].

In parallel, the video celebrates athletic triumph through the story of Joshua Liendo, Canada’s first Black swimmer to win international gold in the 100-meter butterfly at the Doha World Championships. His journey — from Trinidad to Toronto, from childhood in a Caribbean community to global podiums — is framed as both personal achievement and a broader cultural milestone [citation:txt1]. Liendo’s reflections on role models, systemic underrepresentation, and the sacrifices of his family underscore his legacy not only as an athlete but as a symbol of progress and representation in elite swimming [citation:txt1]. His victory, captured in dynamic race footage and celebrated by a roaring Canadian crowd, marks a historic moment that contrasts sharply with the tragedies and institutional failures depicted earlier [citation:txt1]. The video concludes by returning to the themes of recovery and legacy: the rebuilding of schools and the enduring hope of First Nation communities, alongside Liendo’s enduring presence as a trailblazer, affirming that resilience and triumph can emerge even in the face of profound loss [citation:txt7][citation:txt8].
```

- 결론 지시(100–250단어)보다 길다(후처리 후 341단어, ⑦ 경고).
- 첫 문장의 결말 서술("ultimately concluding with themes of community recovery and athletic legacy")은 planner checklist를 따른 것이고 실제 결말과 다르다.
- "41 confirmed cases"는 결론 근거에 없다(⑥ `unsupported`).

**예시 3: `0RxMZBLeqRI` r1 섹션 5 writer 출력 원문의 처음과 끝** (3,072토큰 = 서버 상한, `finish=length`, 133.9초, 1,778단어. 전문 `s05/5_writer_output_raw.md`)

```
# Depiction of Roma Persecution under Nazi and Communist Regimes

At 00:21:00, the video presents archival visuals—black-and-white footage, 1880s illustrations, and portraits of military figures—to establish centuries of institutionalized marginalization in German-speaking territories, setting the stage for state-sanctioned discrimination predating Nazi rule [citation:txt1]. This is followed by portraits and formal assembly scenes of Otto von Bismarck transitioning into images of uniformed men marching, symbolizing early institutionalization of state control under unified Germany [citation:txt1]. The narrative then moves to photographs of uniformed officers, dehumanizing signage (“Zigeunerge

⟨…중략…⟩

itation:txt2]. The video does not show any footage of Roma persecution under communist regimes beyond the title card “Communism, Chapter VII” at 00:24:00 [citation:txt2]. The video does not show any footage of Roma persecution under communist regimes beyond the title card “Communism, Chapter VII” at 00:24:00 [citation:txt2]. The video does not show any footage of Roma persecution under communist regimes beyond the title card “Communism, Chapter VII” at 00:24:00 [citation:txt2]. The video does not show any footage of Roma persecution under communist regimes beyond the title card “Communism, Chapter VII” at 00:24:00 [citation:txt2]. The video does not show any footage of Roma persecution under
```

- 같은 문장("The video does not show any footage of Roma persecution under communist regimes…")을 38번 되풀이하다가 문장 중간에서 끊겼다(writer 반복 루프, P9).

#### (d) 다음 섹션용 맥락 갱신 (LLM 0회)
- 이 맥락은 다음 섹션의 query 생성(④-2(a))과 writer 프롬프트("Context from Previous Sections")에 함께 들어간다.
- **원래 Deep-Reporter**: `_update_context`가 `Section: <planner 설명>` + `Content: <본문 앞 100자>`를 요약으로 넘긴다. 앞 100자는 대부분 제목 줄이라 실제 내용이 거의 넘어가지 않는다.
- **C0(기본)**
  - 형식: 안내 문구 + `Section k: <제목>` + 단락 첫 문장(인용·이미지 표기 제거, 시간 유지).
  - 상한: 문장 240자, 섹션 700자, 전체 3,600자. 넘치면 오래된 섹션부터 제목만 남긴다.
  - 실제 모양은 위 query·writer 프롬프트 예시의 "Already written in earlier sections…" 부분이다.
- tail(직전 섹션 끝)은 원래 함수가 계산한다. tail에는 인용 표기(`[citation:txt1]`, `![](citation:img3)`)가 그대로 남아, 현재 섹션의 근거 번호와 같은 모양으로 들어간다(위 writer 프롬프트 예시, 실측).

#### ④-3 combine
섹션 본문을 `"\n\n"`으로 이어 붙인다(`report_raw.md`). 인용은 섹션 내 번호(txtN, imgN) 상태다. 보고서 전체를 다시 다듬는 refine 단계는 Deep-Reporter에 없다(코드·논문).

### ⑤ 후처리 (`run_report.py` → `grounding_postprocessor.py`, LLM 0회)

처리 순서(섹션마다, 코드):

| 순서 | 함수 | 하는 일 | 결과가 남는 곳 |
|---|---|---|---|
| 1 | `attach_ending_source` **(2026-10-26 추가, 예시 실행에는 없음)** | 본문이 `txt0`을 인용하면 영상 끝 근거를 그 섹션 근거 목록 끝에 붙이고 `txt0`을 새 번호로 바꿈 | `validation.json` `ending_source` |
| 2 | `dedupe_repeated_sentences` | 섹션 안에서 똑같은 문장의 두 번째 이후를 지움. 최대 반복 횟수와 "문장 중간 끝" 여부 기록 | `report.json` `content`(제거 후), `validation.json` `repetition` |
| 3 | `boundary_claims` | "the video ends/closes/opens…" 문장의 인용 근거 시간이 영상 끝·처음에서 120초 넘게 떨어지면 `ending_early`/`opening_late`, 시간 있는 근거가 없으면 `*_unverifiable` | `validation.json` `boundary_findings` |
| 4 | `ground_report` | 인용 변환(아래), 규칙 근거 검사(⑥), 이미지 시간 차 기록 | `report.md`, `validation.json` |

인용 변환 규칙(`ground_report`):
- 섹션마다 writer와 같은 근거 목록(filter off면 `retrieved_*`)으로 번호를 해석한다.
- `[citation:txtN]` → 보고서 전체 번호 `[n]`. 같은 근거(uid)는 같은 번호다. 끝에 `# References`를 붙인다(episodic: 시간 구간·단위·본문 앞 220자, semantic: "no timestamp" + triple).
- `![](citation:imgN)` → `Figure k`. 프레임을 `<out>/frames/`로 복사하고 이미지 줄과 캡션 줄(프레임 시각, 클립 구간, 10sec 캡션 앞 300자)을 넣는다.
- 금지 형식 `[citation:imgN]` → 그 자리에 `(Figure k)`, 그림은 단락 바로 뒤에 넣는다(경고).
- 범위 밖이거나 해석할 수 없는 인용 → `[?]`(오류).

**예시 1: 같은 섹션의 원문 → 최종** (`-QuCz7kxBr8` r1 섹션 1. 원문은 ④-2(c) 예시 1)

최종 본문 앞부분(`report.md`와 같음, `s01/6_postprocess.md` §7):

```
# Introduction to the Participants and Setting

Six men—Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player—are introduced as the main participants in the video. They gather on a sunny outdoor basketball court, dressed in athletic wear and holding basketballs near a hoop and trees [1]. One man, wearing a white hoodie and blue shorts, addresses the camera directly, setting a playful and competitive tone with audio cues such as “Hands up, hands up” and “Mump is blinding me” [1]. The group splits into two teams of three, preparing to test 12 viral sports gadgets, with six assigned per team [1]. The setting is clearly outdoors, under bright sunlight, with visible trees, a fence, and in some shots, a pool and hills in the background [2][3]. The court features a painted “HYPE” logo and a basketball hoop, reinforcing the casual, recreational environment [4](Figure 1).

![Figure 1 (00:34:45)](frames/-QuCz7kxBr8_00344000.jpg)

*Figure 1. Frame at 00:34:45 (clip 00:34:40–00:34:50). On an outdoor basketball court under a clear blue sky, a player in a white jersey and orange shoes, carrying large cylindrical training pads, prepares to defend against another player in a black shirt and pink shorts who is dribbling a basketball. The defender shuffles laterally, maintaining a lo...*

The video’s goal is established early: to test and evaluate the gadgets in a hands-on, competitive, yet lighthearted manner [5]. The first gadget tested is the “SPORTS DRIBBLE SPECS,” introduced with a close-up of black nylon straps and buckles, signaling the start of the gear review [1][2]. The challenge begins with a dribbling time trial, where participants must dribble through three cones and touch a pole to stop the clock [3]. The rules are clarified near the pool under bright sunlight, wi
```

이 섹션이 쓴 References(전역 번호, `s01/6_postprocess.md` §8):

```
[1] 00:00:00–00:00:30 · episodic 30sec: A group of six men—Chris, Zach, Cass, James, and Mitchell—gather on a sunny outdoor basketball court to test 12 viral basketball gadgets, splitting into two teams of three each, with six gadgets assigned per team. Dre...
[2] 00:00:00–00:10:00 · episodic 10min: **Six men—Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player—gather on a sunny outdoor basketball court to test 12 viral sports gadgets, splitting into two teams of three. Dressed in athletic wear, they i...
[3] 00:00:30–00:01:00 · episodic 30sec: A group of men on an outdoor basketball court introduces a gadget challenge where teams will select and test their favorite sports gear. The segment kicks off with one man in a white hoodie and blue shorts holding a b...
[4] Video-level knowledge (semantic memory, no timestamp): (player, can gesture and talk to, another player)
[5] 00:00:00–00:03:00 · episodic 3min: Six men—Chris, Zach, Cass, James, Mitchell, and a sixth unnamed player—gather on a sunny outdoor basketball court to test 12 viral sports gadgets, splitting into two teams of three. Dressed in athletic wear, they intr...
[6] 00:01:40–00:01:50 · episodic 10sec: At an outdoor basketball court beside a pool, a man in a white hoodie and patterned shorts holds a basketball while talking to another player in a tie-dye jersey. The player in the jersey stands with his hands on his...
[7] 00:02:00–00:02:30 · episodic 30sec: Three young men stand on an outdoor basketball court, each holding a ball, engaged in a discussion about dribbling drills and the usefulness of a gadget that helps players avoid looking down. The setting is a sunny ba...
[8] 00:02:30–00:03:00 · episodic 30sec: Three men gather on an outdoor basketball court, preparing for a dribbling challenge using a SKLZ Dribble Stick. The man in the red hoodie introduces the game, asking if they want to see how the dribble stick works, w...
```

- `[citation:txt2]` → `[1]`, `txt3` → `[2]`, `txt12`(semantic) → `[4]`.
- `[citation:img1]` → `(Figure 1)` + 단락 뒤 그림.

**예시 2: 반복 문장 제거** (`0RxMZBLeqRI` r1 섹션 5)
- 원문 1,778단어 → 제거 후 927단어. 문장 37개 제거, 최대 38회 반복, 문장 중간 끝 = true.
- 경고: "section 5: removed 37 repeated sentence(s), a sentence occurred up to 38 times (writer repetition loop suspected)", "section 5: ends mid-sentence (likely cut at the LLM max_tokens cap)".
- `report_raw.md`는 원문 그대로 남는다.

**예시 3: 결말·시작 서술 검사** (실측)

| 보고서·섹션 | 판정 | 문장 | 근거 |
|---|---|---|---|
| `-QuCz7kxBr8` r1 S3 | `ending_early` | "The video closes with a close-up of the Shot Coach device, reinforcing its role in tech-assisted training [citation:txt4][citation:txt5]." | 인용 근거의 끝 00:21:00, 영상 끝 00:37:37. 3min 요약의 구간 끝 표현을 옮긴 것(P19) |
| `0RxMZBLeqRI` r1 S5 | `opening_unverifiable` | "At 00:23:40, the video begins with a person in a dark hooded garment holding a knife, …" | 인용 없음. 10sec 캡션의 "The video begins with"를 옮긴 것 |
| `0RxMZBLeqRI` r1 S1 | `ending_early` (**오탐**) | "… the final shot of the video's opening montage …" | 소유격 표현. 2026-10-26에 수정(이후 실행에서는 잡히지 않음) |

### ⑥ 규칙 기반 근거 검사 (`check_section_grounding`, LLM 0회)
- 문장마다 **따옴표 문구, 숫자, HH:MM:SS**가 그 문장이 인용한 근거에 있는지 확인한다.
  - 문구: 그대로 일치하거나, 같은 근거 안에서 단어가 같은 순서로 가까이 나오면 인정.
  - 숫자: 정확히 일치, `a/b` ↔ `a out of b`, 작은 수는 영어 단어도 인정.
  - 시간: 인용 근거의 구간 안이면 인정.
- 분류
  - `unsupported`: 그 섹션의 어떤 근거에도 없음
  - `miscited`: 인용하지 않은 같은 섹션의 다른 근거에는 있음
  - `uncited`: 인용 없이 수치·문구를 담은 문장
  - `absence`: "근거에 X가 없다/보이지 않는다" 절 안의 토큰. 검사하지 않고 기록만 한다.
- **부정 절(absence)**
  - 조건: 부정어 뒤 12단어 안에 show/visible/mention/state/specify 같은 동사가 오고, 문장에 footage/evidence/retrieved/video/clip/frame/source가 있다.
  - 그 절 안에만 나오는 토큰을 제외한다. 같은 문장이라도 절 밖의 토큰은 계속 검사한다.
- 실제 결과 (예시 r1 3건, `validation.json` `grounding_findings`)

| 보고서·섹션 | 판정 | 토큰 | 문장(앞부분) |
|---|---|---|---|
| `54k2g9ddy4M` S1 | unsupported | `79` | "This is reinforced by another text overlay later in the segment, which states that current vaccination levels stand at 79% [citation:txt1]." — planner checklist에서 온 값(P5) |
| `54k2g9ddy4M` S6 | unsupported | `41` | "… a measles outbreak in the United States with 41 confirmed cases …" — 결론 근거에 없음(P11) |
| `-QuCz7kxBr8` S6 | miscited | `00:37:37` | "The video ends at 00:37:37 with a static screen …" — 인용한 근거(37:00–37:30, 37:20–37:30, semantic)의 구간 밖. 같은 섹션의 36:00–39:00 근거 구간에는 들어 있음 |
| `-QuCz7kxBr8` S4 | miscited | `FIRST MADE SHOT SHOOTS SILLY STRING AT 100%` | 인용한 txt2·txt6이 아니라 txt1에 있음 |

  - 합계: `-QuCz7kxBr8` 0/5/12/0, `0RxMZBLeqRI` 2/0/13/4, `54k2g9ddy4M` 2/1/4/0 (unsupported/miscited/uncited/absence).
- 의미 수준의 오류(다른 근거를 인용한 서술, 장면 오인)는 잡지 못한다. 예: ④-2(b) 예시 3의 Liendo 문장. 결과는 경고로만 쓴다.
- **이미지-텍스트 시간 기록**(`image_time_alignment`, 경고 없음): 인용 이미지마다 프레임 시각과, 같은 단락(또는 직전 텍스트 단락)·섹션 전체에서 인용된 텍스트 근거 구간 사이 거리. 예시 r1 중앙값은 `-QuCz7kxBr8` 1,485초, `0RxMZBLeqRI` 0초, `54k2g9ddy4M` 0초.

### ⑦ 사후 검증 (`run_report.validate`)

| 수준 | 조건 |
|---|---|
| 오류 → exit 1 (산출물은 저장) | `success=False` · 빈 outline · **planner fallback**(섹션 1개이고 설명 == 질의) · 본문의 `Call failed:` 또는 `[Section generation failed` · 빈 본문 · 텍스트 근거 0건인 섹션 · 잘못된 인용(`[?]`) · 프레임 파일 누락 |
| 경고 (exit 코드 영향 없음) | 반복 문장 제거 수. "loop suspected"는 2026-10-26부터 같은 문장 5회 이상 또는 문장 중간 끝일 때만(예시 실행 당시 기준은 최대 반복 ≥ 3) · 문장 중간 끝(서버 상한에서 끊김) · 결말·시작 검사 · txt0이 마지막이 아닌 섹션에서 인용됨(2026-10-26) · query 생성 fallback · 인용 없는 섹션 · 잘못된 이미지 형식 변환 수 · 규칙 검사 unsupported·miscited·uncited 수 · 섹션 수 상한 초과 · 마지막 섹션이 `Conclusion:`으로 시작하지 않음 · 결론이 아닌 섹션이 `Conclusion:`으로 시작 · 결론 300단어 초과 · 번역 실패·한자·가나 잔존 |

예시 r1 3건의 실제 경고(`validation.json` `warnings`, 상태는 모두 `passed`, exit 0):

| 보고서 | 경고 |
|---|---|
| `-QuCz7kxBr8` r1 | 이미지 형식 변환 1, miscited 5, uncited 12, 결말 검사 ending_early 2·ending_unverifiable 3 |
| `0RxMZBLeqRI` r1 | 이미지 형식 변환 2, unsupported 2, uncited 13, 섹션 5 반복 37개 제거(loop suspected), 섹션 5 문장 중간 끝, 결말 검사 ending_early 1(오탐)·ending_unverifiable 1·opening_unverifiable 1 |
| `54k2g9ddy4M` r1 | 결론 341단어, 이미지 형식 변환 5, unsupported 2, miscited 1, uncited 4, 섹션 1 반복 1개 제거, 결말 검사 ending_early 2 |

Deep-Reporter는 LLM 호출이 실패해도 예외 대신 `"Call failed: …"`를 본문에 넣고 `success=True`로 끝날 수 있어서 이 검증이 필요하다. 반대로 위처럼 품질 문제는 경고로만 남고 상태를 바꾸지 않는다.

### ⑧ 한국어 번역 (결정 6, `report_translator.translate_report`)
- 예시 실행에서는 꺼져 있었다(결정 16: 영어 보고서 품질 우선).
- **조건**: `report.translate_ko: true`이고 ⑦에서 **오류가 없을 때만** 실행한다. 오류가 있으면 `translation.status = skipped`.
- **영향 범위**: 영어 `report.md`가 정본이다. 번역 결과는 exit 코드와 영어 결과에 영향을 주지 않는다.
- **단위**: ⑤의 섹션별 본문을 하나씩 번역한다(섹션당 LLM 1회, 최대 출력 `translation_max_tokens: 4096`). LLM은 Deep-Reporter와 같은 엔드포인트와 모델이다.
- **근거 표기 보호**
  - 그림 블록: 번역하지 않고 자리표시로 바꿨다가 원문 그대로 되돌린다.
  - 인용 `[n]`·`[?]`, `(Figure k)`, `HH:MM:SS`, 따옴표 문구: `[[Pn]]`로 바꾸고 번역 후 되돌린다.
  - 고유명사: 본문에서 문장 중간에 대문자로 나온 단어 묶음을 모아 같은 방식으로 보호한다(NER 없음, 문장 첫머리에만 나오는 이름은 수집되지 않음).
- **검사**: 자리표시가 정확히 한 번씩 있어야 하고 제목 줄 수가 같아야 한다. 실패하면 1회 재시도하고, 그래도 실패하면 그 섹션은 영어 원문 유지 + 경고. 한자·가나가 있으면 같은 1회 재시도를 쓰고, 남으면 `foreign_script`로 기록하고 경고한다.
- **구성**: 한국어 헤더 + 번역된 섹션(그림은 제자리) + References 영어 원문.
- 실측: C-4(2026-10-25)에서 17섹션 중 5개가 자리표시 불일치로 실패했다(P15).

### ⑨ 산출물 (`report.outputs_dir/<vid>_<YYYYmmdd_HHMMSS>/`, 배치 실행은 `--out`의 하위 폴더)

| 파일 | 내용 |
|---|---|
| `report.md` | 헤더(영상, 요청, 모델, 검색 모드) + 근거가 연결된 본문 + 그림 + References (정본) |
| `report_ko.md` | 한국어 번역본 (번역이 실행된 경우) |
| `report_raw.md` | Deep-Reporter 원본(섹션 내 번호, **반복 제거 전**) |
| `report.json` | 요청, checklist, 모델, 검색 모드, `session_id`, 섹션별 설명·checklist·검색어·본문(반복 제거 후)·근거 전체, References와 그림 목록 |
| `validation.json` | 상태, 오류, 경고, 단계별 시간, `video_end`, `repetition`, `boundary_findings`, `ending_source`(2026-10-26), 인용 통계, 근거 검사 통계와 항목, 이미지-텍스트 시간 요약, 섹션별 결과, 번역 결과 |
| `frames/` | 인용된 프레임 사본 |

Deep-Reporter 세션 로그(JSONL, 프롬프트·출력 전문)는 `report.deep_reporter_log_dir`에 쌓인다. 단계별로 펼쳐 보려면 §0.2.

---

## 4. LLM 호출과 시간 (실측)

### 4.1 4개 단위 캐시, 현재 설정 (예시 실행 r1, LLM 서버·검색 서비스 로그)

| 단계 | 호출 | `-QuCz7kxBr8` | `0RxMZBLeqRI` | `54k2g9ddy4M` |
|---|---|---|---|---|
| planner | 1 | 35.4초 (5,219 / 764토큰) | 37.4초 (6,966 / 811) | 43.0초 (6,271 / 904) |
| query 생성 | 6 | 3.7–4.5초 (438–1,103 / 81–96) | 2.8–4.4초 (449–1,161 / 63–100) | 3.6–4.8초 (472–1,183 / 80–104) |
| L1 필터 | 6 | 4.4–5.5초 (8,661–12,112 / 66–74) | 4.8–6.3초 (10,063–15,486 / 64–76) | 4.1–5.2초 (6,205–10,544 / 68–75) |
| 검색 서비스 text 요청(필터 포함) | 6 | 5.86–12.19초 | 5.77–11.34초 | 5.31–9.87초 |
| 검색 서비스 image 요청 | 6 | 0.81–1.28초 | 0.86–0.98초 | 0.96–1.52초 |
| writer | 6 | 16.9–48.3초 (4,577–6,125 / 365–1,102) | 19.8–**133.9**초 (4,936–7,111 / 423–**3,072**, 상한) | 21.7–46.2초 (3,034–6,198 / 475–1,026) |
| 후처리·검사 | 0 | 0.04초 | 0.04초 | 0.03초 |
| **생성 합계** | **19** | **319.7초** (writer 62%) | **403.8초** (writer 69%) | **346.3초** (writer 63%) |

### 4.2 이전 측정 (10sec 단위만, 보고서 A·B)

| 단계 | A: 스모크(5섹션) | B: `run_report.py` 첫 실행(6섹션) |
|---|---|---|
| planner | 51.3초 (입력 5,050 / 출력 842토큰) | 36.8초 (입력 5,213 / 출력 849토큰) |
| query 생성 | 각 5.1–6.4초 | 각 3.0–4.1초 |
| L1 필터 | 각 4.6–5.4초 (입력 2,577–3,205토큰) | 각 3.3–4.1초 (입력 2,275–3,474토큰) |
| writer | 각 35.7–66.5초 (출력 614–1,121토큰) | 각 16.1–34.2초 (출력 374–794토큰) |
| 합계 | 16회, 382초 | 19회, 생성 261.5초 + 번역 6회 231.8초 = 494.4초 |

- L1 필터 입력은 10sec만 쓴 A·B(2,275–3,474토큰)보다 4개 단위에서 훨씬 길다(6,205–15,486토큰). 30sec·3min·10min 후보 텍스트가 길기 때문이다.
- 생성이 샘플링이라 같은 조건에서도 출력 길이와 시간이 달라진다. writer 시간은 주로 출력 길이에 비례한다.

---

## 5. 주요 설정 (`config.yaml`)

| 키 | 기본값 | 의미 |
|---|---|---|
| `llm.backend` | `local` | `local` (Qwen3-VL-8B 서버) / `openai` (`gpt-5-mini`, `OPENAI_API_KEY`) |
| `llm.local.endpoint.{host,port,model}` | `127.0.0.1`, `8010`, `qwen3vl-8b` | Deep-Reporter와 L1 필터가 쓰는 엔드포인트 |
| `llm.local.endpoint.max_tokens_cap` | 3072 | 서버가 요청 `max_tokens`(Deep-Reporter는 8,192)를 이 값으로 자름(P9) |
| `retrieval.episodic_filter` | `L1` | `L0` / `L1` / `full` |
| `retrieval.episodic_candidates_per_query` | `{10sec:3, 30sec:3, 3min:2, 10min:1}` | L0/L1 후보 수 |
| `retrieval.{episodic_k, semantic_k, image_k}` | 8, 4, 4 | 요청당 근거 수 (결정 7: 조정 보류) |
| `retrieval.{semantic_k_per_query, visual_k_per_query, rrf_k}` | 5, 3, 60 | 질의당 semantic·visual 후보 수, RRF 상수 |
| `service.{host,port,frames_dir}` | `127.0.0.1`, `8020`, `cache/frames` | 검색 서비스 |
| `report.{domain, text_topk, image_topk, enable_filter}` | `videomme`, 20, 10, false | Deep-Reporter 실행 옵션 |
| `report.overview_granularity` | `10min` | planner 영상 개요에 쓰는 캡션 단위 |
| `report.max_sections` | 6 | 결론 포함 섹션 수 상한 (허용 3–15) |
| `report.previous_sections_context` | `written` | C0: `written` = 앞 섹션에서 실제로 쓴 문장 전달 / `deep_reporter` = 원래 동작 |
| `report.{translate_ko, translation_max_tokens}` | true, 4096 | 한국어 번역본 생성 여부와 섹션당 최대 출력 토큰 |
| `report.{outputs_dir, deep_reporter_log_dir}` | `outputs/`, `logs/deep_reporter` | 산출물과 세션 로그 |
| `worldmm.episodic_cache_label` | `qwen3vl-8b` | 검색 서비스가 읽을 HippoRAG 캐시 라벨 |

---

## 6. 실패 지점과 처리

| 실패 | 어디서 드러나나 | 처리 |
|---|---|---|
| LLM 서버나 검색 서비스가 꺼져 있음 | ① 사전 확인 | exit 2 |
| 영상의 episodic 캐시가 불완전 | ① (`/load` 409) | exit 2. 사전 인덱싱 필요 |
| 모델명이 다른 엔드포인트로 라우팅됨 | ② 라우팅 확인 | exit 2 |
| 템플릿과 Deep-Reporter 코드 계약이 어긋남 | ①, ③ | 실행 전에 오류 (`TemplateContractError`) |
| planner 또는 query JSON 파싱 실패 | ⑦ | planner는 오류, query는 경고 |
| LLM 호출 실패 (본문에 `Call failed:`) | ⑦ | 오류 |
| 검색 실패나 시간 초과 (근거 0건) | ⑦ | 오류 |
| writer가 서버 상한에서 끊김 | ⑤, ⑦ | 반복 문장 제거, "문장 중간 끝" 경고. 끊긴 뒷부분은 생성되지 않음 |
| 잘못된 인용 번호 | ⑤, ⑦ | `[?]` 치환 + 오류 |
| 잘못된 이미지 인용 형식 | ⑤ | 그림으로 변환 + 경고 |
| 근거에 없는 수치·문구·시간 | ⑥ | 경고 (`grounding_findings`) |
| 구간 요약의 시작·끝 표현을 영상 전체로 옮김 | ⑤ | 경고 (`boundary_findings`) |
| `report.max_sections`가 3–15 밖, `previous_sections_context` 값 오류 | 시작 직후 | exit 2 (생성 전) |
| 영상 id가 `-`로 시작하는데 `--video-id <id>`로 넘김 | 시작 직후 (argparse) | exit 2. **`--video-id=<id>` 형식으로 넘긴다** |
| planner가 16개 이상 섹션 생성 | ④ (`GraphRecursionError`) | `success=False` → 오류 (보고서 전체 소실). 상한 지시로 예방 |
| 번역 자리표시 손실, 제목 변형, 빈 출력, LLM 오류, 한자·가나 | ⑧ | 1회 재시도 후 원문 유지 또는 기록 + 경고 |

---

## 7. 현재 한계

- **실행 근거**: 4개 단위 캐시로 보고서 20건(C-4 3, C-5 8, 수정 후 확인 9)을 만들었다. 검증 영상 3개만 캐시가 있다.
- **샘플링 편차**: 같은 조건 3회의 outline, 다룬 범위, 근거, 결말 서술이 크게 달랐다(`SELF_CONSISTENCY_ANALYSIS.md`). 1회 실행으로 설정 효과를 판단할 수 없다.
- **검증의 한계**: ⑤–⑦은 수치·문구·시간·시작/끝 표현·반복만 기계적으로 본다. 다른 근거를 인용한 서술, 장면 오인, 해석 표현, 범위 누락, planner에서 온 틀린 결말은 잡지 못하고, 모두 `passed`로 끝난다.
- **기록의 한계**: L1 필터의 후보 목록과 응답 원문은 남지 않는다. 그래서 검색 단계에서 무엇이 버려졌는지는 볼 수 없다.
- **확인 전**: 2026-10-26 변경(영상 끝 근거 txt0, 경고 기준, 결말 검사 오탐 수정)은 CPU 테스트만 했다.
- 품질 문제 목록과 대응은 `REPORT_ISSUES_AND_FIXES.md`. 보류된 결정: 근거 구성(결정 7, 후보 C·D), 번역(P15), 해석 표현(P12), 흐름(P8).

## 8. 확장 지점

- **LLM**: `vllm serve Qwen/Qwen3-VL-8B-Instruct --served-model-name qwen3vl-8b --port 8010` 후 `llm.local.endpoint.server: vllm`. vLLM은 아직 설치되지 않았다.
- **검색 백엔드**: MERIT를 같은 `/videos/<vid>/search` 형식의 별도 서비스로 만들고 `service.port`나 URL만 바꾼다.
- **도메인**: `domain_templates.TEMPLATE_SETS`에 `surveillance` 세트를 추가하고 `report.domain`을 바꾼다. 여러 날짜에 걸친 영상이면 근거 라벨과 시간 표기에 DAY를 넣어야 한다.
- **기록 보강(제안)**: L1 필터의 후보와 응답을 검색 서비스 로그나 응답 `meta`에 남기면, 검색 단계에서 버려진 근거까지 볼 수 있다(코드 수정 필요, 미구현).
