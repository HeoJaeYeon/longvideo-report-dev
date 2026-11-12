# Video RAG → 관제 보고서 생성 프레임워크: 구성요소 분석 및 보고서 생성 방법론 선정

작성일: 2026-10-13
대상 코드: `/data1/USER/workspace/VideoRAG/{WorldMM, MERIT, qraft, Deep-Report}`
목표: WorldMM/MERIT로 retrieve한 영상 evidence를 활용해 long-form 보고서를 자동 생성.
근단기 타깃: Video-MME 등 Long Video Understanding QA. (CCTV 쿼리는 추후)

---

## 0. 결론 (TL;DR)

- **보고서 생성 백본은 Deep-Report를 채택**하는 것이 적절하다.
- 이유 요약: (1) task 형태가 "grounded multimodal long-form generation"으로 우리 목표와 정확히 일치, (2) 영상 evidence의 **멀티모달(캡션+프레임)** 을 native로 소비, (3) retrieval이 서비스 인터페이스로 **완전히 디커플링**되어 WorldMM/MERIT evidence를 그대로 주입 가능, (4) **clip/timestamp 단위 citation grounding**, (5) checklist 기반 섹션화 + 재귀 context로 긴 출력의 일관성 확보.
- **QRAFT는 fact-checking article 전용**(claim + veracity verdict + 고정 3단 구조, text-only, document-URL citation)으로, 우리 task에 쓰려면 장르 가정과 계속 싸워야 한다. 다만 QRAFT의 **"cite-or-remove"(근거 없으면 문장 삭제) 검증 패스**와 **editor↔writer 교정 루프**는 hallucination 제어 아이디어로 Deep-Report 위에 선택적으로 이식할 가치가 있다.

---

## 1. Retrieval 측 (WorldMM / MERIT) — retrieve→generate 경계 분석

두 시스템은 사실상 같은 골격이다 (MERIT README가 명시: "MERIT builds on WorldMM, our baseline"). 핵심 공통점:

- **agentic 반복 루프**: reasoning LLM이 매 라운드 `search` / `answer`를 결정 → search면 memory type + query 생성 → retrieve → 결과를 `retrieved_items`에 누적 → `answer`면 종료.
- **최종 QA 단계**: 누적된 `retrieved_items`로 멀티모달 `qa_content`(텍스트+이미지)를 만들어 `respond_llm_model.generate()` 1회 호출 → 객관식 정답(A/B/C/D) 생성.

### 1.1 WorldMM (`src/worldmm/memory/memory.py: WorldMemory.answer()`)
- 3개 메모리: **episodic**(HippoRAG/OpenIE triple + 캡션), **semantic**(엔티티 그래프 PPR), **visual**(임베딩 유사도 기반 클립 프레임).
- 라운드마다 reasoning이 `memory_type`(episodic/semantic/visual) + `search_query`를 고름.
- 누적 단위 `RetrievedItem(memory_type, content, query, round_num)`:
  - episodic/semantic → `content`는 텍스트(캡션/triple 문자열)
  - visual → `content`는 `List[PIL.Image]` (클립 프레임)
- 최종: `_render_retrieved_items_for_qa()`가 text/image를 섞은 메시지로 변환 → `generate()`.

### 1.2 MERIT (`src/merit/merit_memory.py: MeritMemory.answer()`)
- 단일 flat **multi-key episodic memory**(클립당 4키), MaxSim 검색.
- 라운드마다 reasoning이 키워드형 `search_query` 생성 → top-k 클립 retrieve → **neighbor filter**(±2 클립으로 시간 확장 후 query 관련 정보만 distill).
- 누적 단위 `RetrievedItem(content: List[ClipContext], query, round_num)`:
  - `ClipContext(original_caption="top{r}: [start - end]\n{text}", filtered_info, frames: List[PIL.Image], video_path, start/end_time, rank)`
- 최종: `_build_qa_content()`가 캡션+distilled info+프레임을 메시지로 → `generate()`.

### 1.3 공통 handoff(splice) 지점 — 보고서 모듈에 넘길 것
두 시스템 모두 최종 evidence는 **"시간구간이 찍힌 evidence 조각들의 리스트"** 형태로 동일하게 수렴한다:

```
evidence item = {
  timestamp range (start-end)  ← 자연스러운 citation/source id
  caption / triple text        ← 텍스트 근거
  (MERIT) distilled relevant info
  (optional) frames: PIL images ← 시각 근거
}
```

→ **보고서 생성으로의 교체 방법: 최종 `answer()`의 "QA 1회 generate" 부분을, `retrieved_items`를 evidence pool로 받는 보고서 생성 모듈로 치환**한다. 각 evidence item의 timestamp가 곧 citation source가 된다. WorldMM↔MERIT 교체 가능성 요구사항도, 이 handoff 스키마(timestamp+text+frames 리스트)로 어댑터를 통일하면 충족된다.

---

## 2. 생성 측 (QRAFT / Deep-Report) — 세부 구성 분석

### 2.1 QRAFT (`qraft/src/`) — Fact-Checking Article Writer
입력: 단일 **claim** + **veracity 라벨** + 사전확보된 evidence 문서들(dict: url→text).

- **Stage A (`qraft_a.py`)**: LangChain `ChatOpenAI`(gpt-4o-mini) 기반.
  - `planner.make_notes`: 문서별 top-3 노트 추출
  - `set_preferences`: 조직 가이드라인(아래 PREFERENCES) 세팅
  - `plan_outline`: 번호형 문단 아웃라인(= 문단별 상세 내용)
  - `writer.write_article`: 노트+아웃라인으로 초안 작성
  - `polish_article`: planner(=editor 역할)↔writer 교정 ×4
  - `cite_or_remove`: **모든 factual statement에 `(Source: URL)` 부착, 근거 못 찾으면 문장 삭제**
- **Stage B (`qraft_b.py`)**: editor↔writer **대화형 QA 10턴** → editor가 edit 리스트 생성 → writer 반영, ×5 → cite_or_remove.
- **PREFERENCES (prompts.py)** 가 장르를 하드코딩: "claim을 누가/언제/어디서 퍼뜨렸는가", "veracity를 명시", **3단 구조(배경→근거논증→판정 결론)**, "추측 금지", "모든 문장은 source URL 인용".

특성 정리:
- **text-only** (멀티모달 없음), **retrieval 없음**(evidence는 통째로 사전 주입), citation = **문서 URL**(span/timestamp 아님).
- 구조는 단일 기사(문단들) 수준, "iteration"은 구조 확장이 아니라 **편집 교정**.
- claim–verdict 중심 장르에 강하게 특화.

### 2.2 Deep-Report (`Deep-Report/deep_reporter/`) — Grounded Multimodal Long-Form Generation
LangGraph `StateGraph`: `planner → (섹션 루프: query_generation → search → [filter] → section_writing) → combine`.

- **planner_node**: outline 생성. 섹션마다 `section_description` + `sectional_checklist`(완결성 보장용 semantic anchor). `generation_mode="without_planner"`면 **외부 아웃라인 그대로 사용**.
- **query_generation_node**: 섹션별 `text_queries`(3–5) + `image_queries`(2–4) 생성.
- **search_node**: `retriever_url`(기본 `http://localhost:5555/search`)로 **HTTP POST**, `{query_list, type:text|image, topk}` → `retrieved_texts`/`retrieved_images`(dict 리스트: content/caption/score/uid/img_path...). **retrieval이 서비스 뒤로 완전 분리됨.**
- **filter_node** (옵션): 텍스트는 LLM relevance, 이미지는 **VLM YES/NO** 필터(미가용 시 score top-K fallback).
- **section_writing_node (핵심)**: `SECTION_WRITING_TEMPLATE`로 섹션 작성.
  - **엄격 citation**: 텍스트 `[citation:txt1]`, 이미지 `![](citation:img1)` → source id로 grounding.
  - **position-aware**: first/middle/last 분기(중간 섹션 조기결론 금지 등).
  - **recurrent context**: `previous_sections_summary`(2000자 초과 시 압축) + `previous_section_tail`로 섹션 간 연속성.
- **combine_node**: 섹션 content 이어붙여 `final_article`.
- **진입점(`api.py: LongGenAPI.generate_article`)**: `overall_query`, `overall_checklist`, `generation_mode`, `outline`, `text_topk/image_topk`, `enable_filter`, `retriever_url` 파라미터. state의 `retrieved_texts`/`retrieved_images`만 writer가 소비.

특성 정리:
- **멀티모달 native**(text+image, 이미지 citation/필터 포함).
- retrieval **pluggable**(HTTP 서비스) + `without_planner`로 아웃라인/evidence 주입 유연.
- citation이 **source-id 단위로 grounding** → 검증 가능한 보고서.
- checklist 기반 섹션화 + 재귀 context → **긴 멀티섹션 출력에 설계됨**.

---

## 3. 비교 및 선정 논리 (QRAFT vs Deep-Report)

| 기준 | QRAFT | Deep-Report | 우리 task 적합 |
|---|---|---|---|
| Task 형태 | fact-check 기사(claim+verdict, 고정 3단) | grounded multimodal long-form report | **Deep-Report** |
| 멀티모달 | text-only | text+image native | **Deep-Report** (영상 프레임 활용 필수) |
| Retrieval 결합 | 없음(evidence 통째 주입) | 서비스로 디커플링 + 주입 가능 | **Deep-Report** (agentic video memory와 정합) |
| Citation grounding | 문서 URL | source-id(txt/img) → clip/timestamp 매핑 | **Deep-Report** (시간 grounding) |
| 긴 출력 구조/일관성 | 단일 기사 + 편집 교정 | checklist 섹션화 + position-aware + 재귀 context | **Deep-Report** |
| 아키텍처 정합 | LangChain 대화메모리(경직) | LangGraph nodes+LLM factory+prompt templates | **Deep-Report** (WorldMM/MERIT와 동형) |
| 고유 강점 | cite-or-remove 검증, editor QA 루프 | — | QRAFT 아이디어 선택적 이식 |

### 선정: **Deep-Report**

핵심 논거 6가지:
1. **Task 형태 일치**: 우리는 "긴 영상에서 retrieve한 근거로 long-form 보고서 생성". Deep-Report가 바로 그 문제다. QRAFT는 claim–verdict 전용이라 open-ended 영상 보고/요약에 억지로 끼워 맞춰야 한다.
2. **멀티모달**: WorldMM(visual memory 프레임)·MERIT(ClipContext.frames) evidence는 본질적으로 캡션+프레임. Deep-Report는 이미지 근거/citation/VLM 필터를 native 지원. QRAFT는 text-only라 Video RAG의 핵심인 시각 근거를 버린다.
3. **Retrieval 디커플링 = 명확한 splice point**: Deep-Report는 retrieval이 서비스 뒤로 분리 + `without_planner`/materials 주입 지원. WorldMM/MERIT의 `retrieved_items`(timestamp+text+frames)를 Deep-Report의 `retrieved_texts`/`retrieved_images`에 그대로 매핑 가능. QRAFT는 섹션별 타깃 retrieval 개념 자체가 없다.
4. **Grounding/citation**: `[citation:txtN]`/`![](citation:imgN)`가 각 문장을 특정 evidence(=특정 클립/시간)로 연결 → 시간적으로 검증가능한 보고서(관제용 핵심). QRAFT의 URL citation은 clip/timestamp에 안 맞고 이미지 citation도 없음.
5. **긴 출력 구조/일관성**: checklist 완결성, position-aware(조기결론 방지), context 압축이 멀티섹션 장문용으로 설계됨. QRAFT는 단문 기사 + 교정 중심.
6. **아키텍처 정합**: WorldMM/MERIT 둘 다 "agentic 반복 + PromptTemplateManager + LLM wrapper" 구조. Deep-Report도 "LangGraph nodes + LLM factory + prompt templates"로 동형이라 통합이 자연스럽다.

### QRAFT에서 가져올 만한 것 (선택적 이식)
- **cite-or-remove 패스**: Deep-Report 생성 후, 각 `[citation:*]`가 실제 evidence로 뒷받침되는지 검증하고 근거 없는 문장은 삭제/수정하는 post-hoc grounding 체크. (hallucination 제어)
- **editor↔writer 교정 루프**: 보고서 품질/완결성 향상용 선택 단계.

---

## 4. 통합 설계 메모 & 열린 이슈 (구현 전 결정 필요)

1. **retrieval 주입 방식 2안**
   - (a) **evidence pre-collection**: WorldMM/MERIT로 먼저 evidence를 모아 Deep-Report에 `without_planner` + materials로 주입(섹션별 search 생략). 단순/결정적. **초기 권장.**
   - (b) **per-section 어댑터**: Deep-Report의 `retriever_url`을 WorldMM/MERIT retrieve를 감싼 로컬 서비스로 교체 → 섹션 쿼리마다 video memory 검색. agentic 성격 보존, 구현 복잡.
2. **Deep-Report 기본 retriever(Milvus+Jina/InternVL sandbox)는 사용하지 않음** — 영상 evidence로 완전 대체.
3. **Video-MME(객관식)와 보고서 목적의 불일치(중요)**: Deep-Report 출력은 보고서지 A/B/C/D가 아니다. Video-MME 정확도를 근단기 성공지표로 쓰려면,
   - (a) "보고서→정답 추출" reading step을 추가하거나,
   - (b) 보고서를 중간 reasoning으로 두고 기존 QA head를 유지하는 하이브리드,
   - 중 선택 필요. 즉 **"보고서 품질"과 "MC-QA 정확도"는 다른 목적**임을 명확히 하고 평가 프로토콜을 먼저 정해야 한다.
4. **frame → image citation 매핑**: Deep-Report image item 스키마(`img_path`/`caption`/`score`/`uid`)에 맞춰, video frame(PIL)을 파일로 덤프하거나 base64 경로를 채우는 어댑터 필요(특히 VLM 필터는 `img_path` 파일 존재를 가정).
5. **citation id ↔ timestamp 매핑 테이블**을 보고서와 함께 산출하면 관제/검증에 바로 쓰임.

---

## 5. 분석에 참조한 핵심 파일
- WorldMM: `src/worldmm/memory/memory.py`(answer 루프/handoff), `llm/templates/{memory_reasoning,qa}.py`
- MERIT: `src/merit/merit_memory.py`(ClipContext/neighbor filter/handoff), `llm/templates/*`
- QRAFT: `src/qraft_a.py`, `src/qraft_b.py`, `src/agents/{planner,writer,editor}.py`, `src/utils/prompts.py`
- Deep-Report: `deep_reporter/core/{graph,state}.py`, `nodes/{planner,query_generation,search,filter,section_writing,combine}_node.py`, `prompts/templates.py`, `api.py`

---
---

# PART II. WorldMM + Deep-Report 통합 전략 (Video 보고서 생성 baseline)

작성일: 2026-10-14

## II-0. 확정된 설계 결정 (사용자 승인)
1. **retrieval 주입 = evidence 선수집 + 주입** (per-section 라이브 검색 아님). 단순/결정적 baseline.
2. **Deep-Report 기본 retriever(Milvus+Jina/InternVL sandbox) 미사용** → WorldMM 영상 evidence로 대체.
3. **Video-MME 다지선다 평가는 1차 목표 아님.** Video-MME의 "영상+쿼리"만 사용하여 **쿼리 기반 영상 보고서**를 먼저 잘 생성. CCTV 이상상황 관제는 추후 확장. 단, **보조 지표로 Video-MME 정확도**를 "보고서→정답 추출" 방식으로 측정.
4. **frame→이미지 스키마 어댑터의 VLM은 Qwen/InternVL 계열 중 객관적 선정** → (아래 II-5) **Qwen3-VL-8B-Instruct** 선정.
5. **citation id ↔ timestamp 매핑 테이블**을 보고서와 함께 산출(일단 포함, 추후 출력에서 분리 가능).

---

## II-1. 통합 관점 재분석 (핵심 사실만, 근거 코드 라인 기준)

### (A) WorldMM — Video-MME 구동/검색 경계 (`eval/eval.py`, `memory/memory.py`)
- Video-MME는 **영상 1개 단위**로 처리: `reset()` → 캡션 4-granularity(`10sec/30sec/3min/10min`) + semantic triples + visual embeddings 로드 → `index(QUERY_TIME)` → 쿼리마다 `world_memory.answer(query, choices, until_time)`.
- `answer()` → `QAResult(answer, retrieved_items, round_history, num_rounds)`.
  - `retrieved_items: List[RetrievedItem]`: episodic/semantic = **텍스트**, visual = **`List[PIL.Image]`**.
  - **splice point**: `answer()`가 최종 MC generate 하기 직전에 모은 `retrieved_items`가 곧 보고서용 evidence. (= 최종 QA를 보고서 생성으로 치환하거나, retrieved_items만 뽑아 외부로 전달)
- **LLM 실행 방식**: WorldMM은 **in-process Qwen3-VL(transformers)** (`llm/qwen3vl.py`, `MODEL_DICT`: qwen3vl-2b/4b/8b). 통합 래퍼 `LLMModel`가 provider 자동감지(gpt→openai, qwen3→qwen3vl). 프롬프트 = `{role, content:[{type:text|image|video}]}` 메시지 리스트. GPU generate는 lock 직렬화.
- **캡션 생성기**(`preprocess/.../generate_fine_caption.py`)도 동일 `LLMModel`(Qwen3-VL)로 frames+transcript→dense caption. → **Qwen3-VL이 이미 WorldMM 전반의 표준 VLM**.

### (B) Deep-Report — 생성 파이프라인/주입 경계 (`core/graph.py`, `nodes/*`, `llms/factory.py`, `config/*`, `api.py`)
- LangGraph: `planner → (섹션 루프: query_generation → search → [filter] → section_writing) → combine`.
- **중요 1 — writer는 text-only**: `section_writing_node`는 이미지 재료를 **텍스트 설명** `"[Source img{idx}: {caption}]"`로만 넣는다(픽셀 X). 실제 이미지 픽셀은 **filter_node(enable_filter=True)** 의 VLM 판정에서만 사용. → **보고서 writer는 텍스트 LLM이면 충분**, VLM은 (i) 업스트림 캡션 생성, (ii) 선택적 image filter에만 필요.
- **중요 2 — without_planner여도 search는 실행됨**: 그래프가 섹션마다 `search_node`를 돌며 `retrieved_texts`를 **덮어쓴다**. 따라서 "evidence 주입"은 **outline에 미리 넣는 방식으로는 유지 불가** → **`retriever_url`(:5555) 엔드포인트로 evidence를 서빙**해야 함. (이게 결정 #1a를 Deep-Report 무수정으로 구현하는 유일하게 깔끔한 길)
- **중요 3 — LLM은 전부 OpenAI-호환 HTTP**: `factory.py`에서 `primary_model` 이름에 `gpt`/`deepseek`가 **없으면** `qwen_api_key`/`qwen_base_url`로 라우팅. VLM filter는 `vlm_base_url`(기본 `:9000`, internvl35-38b). → **모델명/ base_url만 바꾸면 로컬 Qwen vLLM으로 전면 교체 가능(코드 무수정)**.
- `search_node` I/O: POST `{query_list, type:"text"|"image", topk}` → `{status:"success", results:[{content|text, caption, score, uid, img_path, ...}]}`.
- `api.generate_article(overall_query, overall_checklist, generation_mode, outline, text_topk, image_topk, enable_filter, retriever_url, userid)`.
- session_logger가 **섹션별 사용 citation(txtN/imgN)과 그 source uid**를 이미 기록 → citation↔timestamp 역매핑의 토대.

### (C) 두 시스템의 임피던스 차이와 해소
| 항목 | WorldMM | Deep-Report | 해소책 |
|---|---|---|---|
| 모델 실행 | in-process transformers | OpenAI-호환 HTTP | **Qwen3-VL-8B를 vLLM(OpenAI 호환)로 1회 서빙**; Deep-Report가 호출 |
| evidence 전달 | `retrieved_items`(메모리 객체) | `retriever_url` HTTP 응답 | **Evidence Adapter + Retriever Shim(:5555)** (신규, /claude_output) |
| 이미지 | PIL frames | `img_path`+caption | 프레임을 파일로 덤프 → img_path, caption=WorldMM 클립 캡션 |
| source id | timestamp 구간 | `uid` 필드 | **uid = `video_id@start-end`** 로 설정 → 자동 grounding |

---

## II-2. 타깃 아키텍처 & 데이터 흐름

```
Video-MME (video + query)
  │  WorldMM 전처리(기존): captions(10/30s,3/10min)+semantic triples+visual emb
  ▼  WorldMM 검색(기존 answer()의 retrieval 루프 재사용)
retrieved_items  =  [ {timestamp, caption/triple text},  {timestamp, PIL frames} ... ]
  │
  ▼  [신규] Evidence Adapter          (retrieved_items → 표준 pool)
pool.text  = [{content, uid=video@start-end, score, source}]
pool.image = [{img_path(프레임 덤프), caption, uid=video@start-end, score}]
  │
  ▼  [신규] Retriever Shim  HTTP :5555 /search   (pool 서빙; Deep-Report 무수정)
  │
  ▼  Deep-Report  api.generate_article(retriever_url=shim, LLM=Qwen vLLM)
   planner → (query_gen → search(shim) → [filter:Qwen-VL] → section_writing:Qwen-text) → combine
  │
  ├─► report.md  (멀티섹션 + [citation:txtN] / ![](citation:imgN))
  ├─► [신규] Citation Resolver → citation_map.json  (txtN/imgN → timestamp)
  └─► [신규] (보조지표) Report→Answer Extractor → Video-MME 정확도
```

**핵심 설계 선택**: 결정 #1a를 "쿼리-불가지(query-agnostic) 고정 pool"로 구현. 즉 WorldMM으로 그 영상+쿼리에 대한 evidence를 한 번 모아, **모든 섹션에 동일 pool을 서빙**하고 섹션별 세분화는 Deep-Report의 `query_generation`(writer 집중용) + 선택적 `filter_node`에 맡긴다. (라이브 per-section 검색=결정 #1b는 shim을 "쿼리 민감"으로 바꾸는 확장으로 추후 전환 가능.)

---

## II-3. 어댑터 / 심(shim) 상세 설계
- **Evidence Adapter**
  - 입력: `QAResult.retrieved_items`(+ round_history). WorldMM↔MERIT 교체 대비해 **공통 입력 스키마**(timestamp, text, optional frames)로 정규화.
  - 텍스트 item: `{"content": <caption/triple>, "uid": f"{video_id}@{start}-{end}", "score": <rank/sim>, "source": "episodic|semantic"}`.
  - 이미지 item: visual frames(PIL)를 `run_dir/frames/{uid}_{k}.jpg`로 저장 → `{"img_path", "caption": <clip caption>, "uid", "score"}`.
- **Retriever Shim** (FastAPI/Flask, :5555) — Deep-Report `search_node` 계약 그대로 구현.
  - `/search {query_list,type,topk}` → baseline: 해당 type pool의 상위 `topk` 반환(쿼리 무시). 확장: 쿼리로 재랭크(임베딩/lexical).
  - Deep-Report 코드는 **한 줄도 수정하지 않음**(결정 #2 + CLAUDE.md 준수).
- **Citation Resolver**: 최종 article의 `[citation:txtN]`/`![](citation:imgN)`를 섹션별 재료 순서(= session_logger가 기록한 uid 리스트)와 조인 → `citation_map.json = [{citation:"txt3", section:2, uid:"video@00:12:30-00:13:00"}]`.

---

## II-4. 보조 지표 설계 — Video-MME 정확도 (결정 #3)
세 가지 후보 중 **"Report→Answer(보고서 closed-book) 추출"** 을 1차 보조지표로 채택.

| 방식 | 측정하는 것 | 채택 |
|---|---|---|
| **Report→Answer** (보고서만 보고 judge LLM이 A/B/C/D) | **보고서의 커버리지/유용성/근거성** (우리 목표와 정합) | ✅ 1차 보조지표 |
| WorldMM-native MC head 유지 | retrieval+추론 성능(보고서 품질과 무관) | ◻ 참조용 상한(upper-bound)으로 병기 |
| 둘 다(hybrid) | 둘의 gap = 보고서 작성 중 손실 정보량 | ✅ gap 분석용 |

- **프로토콜**: 보고서 생성 시 **choices는 주지 않음**(open-ended 쿼리 보고서 유지). 추출기만 question+choices+보고서를 받아 정답 1자 선택 → gold와 비교(기존 `eval.py`의 `evaluate_prediction` 재사용).
- **gap 분석**: `WorldMM-native MC acc` − `Report-based acc`. gap이 크면 보고서가 정보를 잃는다는 신호 → outline/topk/filter 튜닝 포인트.
- 주의: 이 지표는 judge 의존 → judge 모델/프롬프트 고정, 두 수치 모두 리포트.

---

## II-5. LLM / VLM 선정 (결정 #4) — 객관적 분석

### 사용처별 요구
- (a) **보고서 writer / planner / query_gen** = **텍스트 LLM**(Deep-Report writer는 픽셀 안 봄).
- (b) **캡션 생성기**(WorldMM 전처리, frames→caption) = **VLM**.
- (c) **image filter**(선택, enable_filter) = **VLM(YES/NO 관련성)**.

### VLM 후보 비교 (하드웨어: 8× RTX A6000 48GB, sm_86)
| 기준 | **Qwen3-VL-8B-Instruct** | InternVL3.5-38B |
|---|---|---|
| 기존 통합 | ✅ WorldMM `qwen3vl.py`+기존 캡션 전부 | ❌ 래퍼/서빙 신규 |
| VRAM(bf16) | ~16–20GB, **1 GPU** | ~76GB, **2–3 GPU** |
| 영상/멀티프레임 | ✅ video+timestamp 네이티브 설계 | 멀티이미지 가능, video 상대적 약 |
| 1회 서빙 재사용(writer/filter/caption) | ✅ vLLM 1개로 통합 | 무거움 |
| 단일이미지 OCR/문서 상한 | 강함(충분) | 더 높음 |

### 선정 — **Qwen3-VL-8B-Instruct** (캡션 + image filter)
결정적(검증 가능한) 근거: **① 이미 통합·검증됨**(코드/캡션 일관성, 신규 래퍼 0), **② A6000 1장에 bf16 적재**(InternVL-38B는 2–4장 + VRAM 4×) → 임베딩/WorldMM와 병렬 여지 확보, **③ 영상·타임스탬프 네이티브**, **④ vLLM 1회 서빙으로 writer/filter/caption 공용** → 운영/VRAM 최소. YES/NO 필터와 캡션엔 8B급으로 충분하여 38B의 한계이득이 4× 비용을 정당화 못 함.
- **writer(텍스트)는 VLM과 독립 분리**: 품질 필요 시 `primary_model`만 더 큰 텍스트 모델(예: Qwen3-32B-text 또는 gpt-*)로 **엔드포인트 교체(코드 무수정)**.
- 추후 벤치마크 선두 VLM이 필요하면 **vLLM 모델 id만 교체** → 전체 코드 변경 0.

### 서빙/배선
- **vLLM(OpenAI 호환) 로 Qwen3-VL-8B 1회 서빙** @ `:8000/v1`.
- Deep-Report config(`create_openai_api({...})`)에 주입:
  `primary_model="qwen3vl-8b"`(이름에 gpt/deepseek 없음 → `qwen_base_url` 경로), `qwen_base_url="http://localhost:8000/v1"`, `qwen_api_key="EMPTY"`, `vlm_base_url` 동일, `vlm_model="qwen3vl-8b"`. → **Deep-Report 무수정**.
- WorldMM: baseline은 **기존 in-process Qwen3-VL 유지**(검증된 경로). (최적화: WorldMM openai provider를 vLLM로 지향해 가중치 중복적재 제거 — 추후.)

---

## II-6. 신규 코드 배치 (전부 `/claude_output`, 기존 repo 무수정)
```
claude_output/report_framework/
├── evidence_adapter.py     # QAResult.retrieved_items → 표준 pool(+프레임 덤프, uid=timestamp)
├── retriever_shim.py       # FastAPI :5555 /search  (Deep-Report 계약 서빙)
├── run_report_videomme.py  # 드라이버: video+query→WorldMM 검색→pool→shim→generate_article→저장
├── citation_resolver.py    # [citation:*] ↔ uid(timestamp) → citation_map.json
├── answer_extractor.py     # Report→Answer 보조지표 + native-MC 참조 → accuracy
├── serve_qwen_vllm.sh      # vLLM OpenAI 서버(qwen3vl-8b)
└── configs/videomme.yaml   # topk, enable_filter, 모델/URL, outline 모드
```

---

## II-7. 단계별 구현 계획 + 검증 기준 (측정가능)
- **P0 서빙**: vLLM Qwen3-VL-8B 기동. ✅ `curl :8000/v1/chat/completions` 텍스트 응답 + 이미지 입력 응답.
- **P1 어댑터+심**: 1개 영상+쿼리로 WorldMM 검색→pool. ✅ pool 비어있지 않음, frames 덤프 존재, `:5555/search` 가 스키마대로 results 반환(단위 점검).
- **P2 생성**: `generate_article(retriever_url=shim, Qwen vLLM, with_planner)`. ✅ `report.md` 생성, 섹션 존재, `[citation:txtN]`가 **실제 pool uid**를 가리킴.
- **P3 citation 매핑**: `citation_resolver`. ✅ 모든 citation이 timestamp로 해석됨, 샘플 수동검증에서 시간 타당.
- **P4 보조지표**: Video-MME 부분집합(예 50문항) Report→Answer 정확도 + native-MC gap. ✅ 수치 산출, WorldMM baseline 대비 sanity.
- **P5 스케일/튜닝**: duration(short/medium/long)별, `text_topk/image_topk`, `enable_filter`, outline 모드(with/without_planner) 비교.

---

## II-8. 열린 리스크 & 대응
- **쿼리-불가지 pool**이 다면적 섹션에 부족할 수 있음 → `filter_node`로 섹션별 정제, 필요 시 결정 #1b(쿼리 민감 shim)로 전환.
- **보조지표의 judge 의존** → judge 모델/프롬프트 고정, Report-based·native-MC 두 수치 병기.
- **writer가 픽셀 미사용** → 시각 근거는 캡션/필터 경유. 픽셀 수준 보고가 필요하면 `section_writing_node`에 이미지 주입 필요(기존 수정 유발 → 추후, 현 단계 지양).
- **Qwen 가중치 2회 적재**(WorldMM in-process + vLLM) VRAM 사용 → 8×A6000에서 수용 가능, 추후 단일화.
- **without_planner의 search 재실행** → shim 서빙으로 해결(이미 반영).

