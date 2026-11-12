# Video RAG × 보고서 생성 프레임워크 — 독립 분석 (코드 기반)

> 작성: Claude Code 직접 조사(논문 README + 구현 코드 분석). 기존 `claude_output/VideoRAG_ReportGen_analysis.md`는 신뢰하지 않고 **독립·비판적으로 재분석**함.
> 분석 대상 실제 경로: **`/data1/USER/workspace/VAU_RAG`** (사용자가 말한 `/home/...`는 존재하지 않음 — 실제는 `/data1`).
> 목표: **Video RAG가 retrieve한 video evidence로 관제(surveillance) 보고서를 자동 생성**하는 프레임워크. Video QA head를 **long-form generation**으로 교체. WorldMM 중심, MERIT 교체 가능 고려. 1차 타깃 = Video-MME 등 Long Video QA 계열.

---

## 1. 결론 요약 (TL;DR)
- **보고서 "문서 작성" 모듈 = `Deep-Report` 채택** (qraft 아님). 근거는 §4.
  - Deep-Report의 writer는 **도메인 비결합 범용 long-form 리포트 생성기**이고, **증거가 state의 `retrieved_texts/retrieved_images`로 주입**되며 검색이 **외부 HTTP 노드로 완전 분리**되어 있어, Video RAG 증거를 그대로 꽂을 수 있음. **멀티모달(프레임)·checklist·per-section 점증·소스인덱스 인용** 모두 관제 보고서에 적합.
  - qraft는 **fact-checking 전용**(모든 프롬프트가 `claim`+`veracity` 결합, URL 인용, 3-part 검증 구조, 텍스트 전용) → 장르·모달리티 불일치, 핵심 프롬프트가 전이 불가.
- **Video RAG = WorldMM 중심**, 필요 시 **MERIT 교체 가능**. 둘 다 "retrieve된 evidence"를 노출하는 접합부가 있어, **Deep-Report writer에 공통 어댑터로 연결** 가능(§3, §5).

---

## 2. 네 방법론 구성·구현 분석

### 2.1 WorldMM [CVPR 2026] — Video RAG (중심)
- **메모리 3종**: episodic(다중 시간척도 10s/30s/3min/10min 캡션+OpenIE triple→HippoRAG 그래프), semantic(관계 triple 증분 consolidation), visual(VLM2Vec 클립 임베딩 1536-d).
- **검색→QA**: `WorldMemory.answer(query, choices, until_time) -> QAResult`
  (`src/worldmm/memory/memory.py:408`). 에이전트가 round마다 `decision=search`로 memory_type 선택→검색, `decision=answer`로 종료.
- **증거 노출 지점(접합부)**: `QAResult.round_history`(`utils.py:35`)의 각 항목 = `{round_num, decision, memory_type, search_query, retrieved_content}` (`memory.py:548`). episodic/semantic은 텍스트, visual은 이미지(프레임). → **retrieve된 evidence가 round_history에 그대로 남음** → 보고서 생성에 재사용 가능.
- **QA head 교체 지점**: 현재 `answer()`는 4지선다 letter를 반환. 보고서용으로는 "검색 라운드로 증거 수집 → letter 대신 evidence 묶음을 generation 모듈로 전달".

### 2.2 MERIT [ECCV 2026] — Video RAG (교체 후보)
- **단일 flat key-value 메모리**: 30초 clip당 **4키**(event/dialogue/object/summary) (`src/merit/multikey_memory.py:92-95`, `*_4_key.json`).
- **검색**: 키별 **MaxSim**로 clip 스코어(`multikey_memory.py:18`), inference-time **neighbor filtering(시간적 확장)**으로 주변 context 확장 후 질의-관련 evidence 증류(distill).
- **캡션 재사용**: WorldMM의 30초 dense caption을 그대로 사용(README) → **WorldMM과 입력 캡션 호환**(교체 용이).
- **특징**: WorldMM보다 단순(그래프/의미 메모리 없음), day-scale 특화. 증거 = retrieved clips + distilled evidence(→ 프레임/캡션).

### 2.3 qraft [TACL 2026] — 보고서 생성 후보 A (fact-checking article)
- 구조(작음, 깔끔): `src/qraft_a.py`(증거 nuggets→notes→outline→draft) + `src/qraft_b.py`(editorial QA review→edits→refine). 에이전트 `agents/{planner,writer,editor}.py`, 프롬프트 `utils/prompts.py`.
- **입력 핵심 = `claim` + `veracity`(판정)**: `writer.write_article(claim, veracity, notes, outline)` (`writer.py:35`). 모든 프롬프트가 "fact-check article" 하드코딩(`prompts.py`: "claim", "its veracity", "WHO spread the claim, WHEN/WHERE").
- **증거**: 텍스트 문서 dict(`{url: text}`), URL 인용(`(Source: <URL>)`). 멀티모달 없음.
- **장르**: 특정 주장의 진위 검증 기사(배경→veracity 논거→판정). 관제 보고서(사건 서술·요약)와 다름.

### 2.4 Deep-Report (Deep-Reporter) [ACL 2026] — 보고서 생성 후보 B (grounded multimodal long-form)
- **LangGraph StateGraph**(`core/graph.py`): planner → (per section) query_generation → search → filter → **section_writing** → combine. `with_planner`/`without_planner`(외부 outline 주입) 2모드.
- **상태=증거 인터페이스**(`core/state.py`): `SectionInfo{section_description, sectional_checklist, image_queries, retrieved_texts: List[Dict], retrieved_images: List[Dict], filtered_*}`, `MultimodalLongFormState{overall_checklist, outline, current_section_index, previous_sections_summary, previous_section_tail, image_topk, retriever_url}`.
- **writer(`nodes/section_writing_node.py`)**: 증거를 state의 `filtered_texts/images` 또는 `retrieved_texts/images`에서 읽어(`:37-44`), checklist(overall+sectional) + recurrent context(요약+직전 tail)로 섹션 작성. **인용 = 소스 인덱스**: 텍스트 `[citation:txt1]`, 이미지 `![](citation:img1)`(`:141-142`, `templates.py:145-160`). 프롬프트는 **범용 long-form writer**(도메인 비결합).
- **검색 분리도**: `nodes/search_node.py`는 순수 HTTP(`requests.post(retriever_url, {queries})→results`, `:38-61`)로 `retrieved_texts/images`를 채움 → **retriever를 Video RAG로 교체하기만 하면 writer 무수정**.
- **의존성**: writer 코어 = langgraph/langchain/openai. milvus/jina는 **내장 retriever 전용**(우리는 교체하므로 불필요).

---

## 3. Video RAG → generation 접합 (공통)
| | retrieve 증거 노출 | 텍스트 증거 | 이미지 증거 |
|---|---|---|---|
| WorldMM | `QAResult.round_history[*].retrieved_content` | episodic/semantic 검색결과(캡션·triple) | visual clip 프레임 |
| MERIT | retrieved clips + distilled evidence | clip 캡션/키 | clip 프레임 |
→ 둘 다 **Deep-Report의 `retrieved_texts`(List[Dict]) / `retrieved_images`(List[Dict])에 어댑터로 매핑** 가능. 접합부가 명확해 **WorldMM↔MERIT 스왑**도 어댑터만 교체.

---

## 4. qraft vs Deep-Report — 코드 기반 판단 (★결정)

| 기준 | qraft | Deep-Report | 우위 |
|---|---|---|---|
| 장르 | fact-check **기사**(claim+veracity 판정) 하드코딩 | **범용 grounded long-form 리포트**(도메인 비결합 프롬프트) | **Deep-Report** |
| 증거 인터페이스 | `{url:text}`, claim 스코프, 코드에 파일경로 결합 | state `retrieved_texts/images`(List[Dict]), **검색 노드 완전 분리** | **Deep-Report** |
| 멀티모달 | 없음(텍스트 전용) | **텍스트+이미지** 통합(`![](citation:img)`) → 비디오 프레임 적합 | **Deep-Report** |
| 장문 구조 | 짧은 3-part 기사 | **checklist + per-section 점증 + recurrent context** → 장문 확장 | **Deep-Report** |
| 인용/그라운딩 | URL 인용(웹문서 전제) | **소스 인덱스 인용**(txt/img) → 비디오 clip ID에 자연 매핑 | **Deep-Report** |
| Video RAG 연결 비용 | 프롬프트 전면 재작성 필요(핵심가치 상실) | **search 노드만 교체**(writer 무수정) | **Deep-Report** |
| 단순성/의존성 | 더 작고 가벼움(milvus 불필요) | LangGraph 등 약간 무거움(단 retriever 제외 가능) | qraft |
| 차용 가치 | **editorial QA refine(qraft_b)** 아이디어는 선택적 차용 가능 | — | (qraft 부분차용) |

**판단: Deep-Report 채택.** 관제 보고서는 "주장 진위 검증"이 아니라 **영상에서 관측된 사건의 근거기반 장문 서술**이므로, Deep-Report의 (1) 범용 리포트 writer, (2) 멀티모달 프레임 통합, (3) 외부 증거 주입형 state 인터페이스, (4) checklist/recurrent 장문 구조가 결정적으로 부합. qraft의 핵심(=fact-check 전용 프롬프트)은 전이 불가하여 채택 시 사실상 전면 재작성이 필요.
**단, qraft의 `editorial review(qraft_b)` 단계(에이전트 QA로 초안 정제)는 품질 향상용 선택적 후처리로 차용 검토 가치 있음.**

---

## 5. 제안 통합 아키텍처
```
[Video] → Video RAG (WorldMM 중심 / MERIT 교체 가능)
            └─ 검색 라운드로 evidence 수집 (round_history / retrieved clips)
                     │  ← 어댑터(claude_output): evidence → {retrieved_texts[], retrieved_images[]}
                     ▼
         Deep-Report writer 경로 (search_node를 어댑터로 대체)
            planner(or 외부 outline/checklist) → [per section] filter → section_writing → combine
                     ▼
            근거기반 멀티모달 관제 보고서 (txt/img 인용)
            (선택) qraft-style editorial QA refine 후처리
```
- **핵심 작업**: Deep-Report `search_node` 대체 어댑터(`claude_output/`에 신규) — WorldMM/MERIT 검색 호출 → `retrieved_texts`(캡션·triple) + `retrieved_images`(clip 프레임) 반환. writer/planner/combine은 거의 무수정.
- **outline/checklist**: 관제 보고서 템플릿(예: 개요/타임라인/이상행동/관련객체/결론)을 `without_planner`로 주입하거나 planner 프롬프트만 관제용으로 조정.
- **Video QA → long-form 전환**: WorldMM `answer()`의 letter 반환 대신, 검색 라운드로 모은 evidence를 generation으로 넘김(QA 평가는 유지하되 보고서 경로 분기).

## 6. 미해결/다음 단계
1. Deep-Report writer 코어를 **retriever 없이(증거 직접 주입)** 단독 구동 PoC — milvus/jina 미설치로 돌아가는지 확인.
2. WorldMM evidence→`retrieved_texts/images` 어댑터 사양 확정(프레임 파일 경로·캡션·triple 매핑).
3. 관제 보고서 outline/checklist 템플릿 설계.
4. (선택) MERIT 경로 어댑터 + WorldMM과 A/B.

---

## 7. 통합 개선점 6건 — 코드 재검증 결과 (2026-10-16, 전부 CONFIRMED)
`WorldMM_DeepReport_integration_strategy.md §6`의 개선점을 Deep-Report 코드로 1건씩 재검증. **6건 모두 사실(과장/오류 없음) 확인.** 근거 파일:라인 명시.

| # | 개선점 | 검증 | 코드 근거 |
|---|---|---|---|
| 1 | **인용·이미지 전역 해소 없음 → 후처리기 필수** | ✅ CONFIRMED | `combine_node.py:25-32` citation을 **count만** 하고 `"\n\n".join`으로 단순 연결(치환 X). `section_writing_node.py:50,56` 인덱싱이 **섹션마다 `start=1`**(섹션-로컬 확정). 섹션 결과는 `outline[idx].retrieved_texts/images`(`search_node.py:114-115`) + `content`(`section_writing_node.py:116`)에 잔존 → 후처리 입력 가능. session_logger에 섹션별 used source `uid/img_path/score` 기록(`section_writing_node.py:157-172`). |
| 2 | **writer/planner/query = OpenAI 호환 chat LLM(별도 엔드포인트)** | ✅ CONFIRMED | 3노드 모두 `get_primary_llm`(`planner_node.py:74`, `query_generation_node.py:34`, `section_writing_node.py:35`). factory가 `ChatOpenAI`(OpenAI 호환), `openai_base_url` 주입 가능(`base_config.py`). `start.py:8` 기본 `gpt-5-mini`. → WorldMM 메모리용 qwen3vl-8b와 **별개**. |
| 3 | **이미지 캡션 비면 'Image'로 퇴화** | ✅ CONFIRMED | `section_writing_node.py:58` `img_item.get('caption', img_item.get('description', 'Image'))`. 어댑터가 `caption`을 반드시 채워야 함. |
| 4 | **topk 합산 규칙은 어댑터가 정의** | ✅ CONFIRMED | `search_node.py:49-52,82-85` `query_list`(복수)+`topk`(단일) 전송. 원래 retriever는 `rerank_results(hits, query_list)`(`retriever_app.py:570`)로 **여러 쿼리 결과를 score로 rerank**. → 어댑터가 "쿼리별 retrieve→병합·dedup·정렬·top-k"를 구현해야 함. |
| 5 | **enable_filter=False 권장; filter 시 VLM이 실제 img_path 파일 읽음** | ✅ CONFIRMED | `filter_node.py:136` `os.path.exists(img_path)`, `:146` `open(img_path,'rb')`→base64→VLM. `start.py:26` 기본 `enable_filter=False`. → 어댑터가 프레임 png 파일을 반드시 생성해야 필터 가능. |
| 6 | **검색 실패 시 빈 리스트로 계속 → 증거 공백 위험** | ✅ CONFIRMED | `search_node.py:69,105` `except`로 빈 리스트 유지 후 진행. 증거 0이면 writer가 "No materials retrieved"로 작성(`section_writing_node.py:64`). → 어댑터가 최소 증거 보장/로그 필요. |

**결론**: 6건 모두 코드 사실에 부합 → 전략에 그대로 유지. 특히 **#1(후처리기)**, **#2(LLM 엔드포인트)**는 신규 컴포넌트/의사결정으로 확정. 상세 통합 설계는 → `claude_output/WorldMM_DeepReport_integration_design.md`.
