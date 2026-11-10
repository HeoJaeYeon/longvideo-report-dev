# Deep-Report (Deep-Reporter) 구현 분석 — 전체 구조·모듈·동작 (코드 정독 기반)

> 목적: 사용자가 Deep-Report의 전체 구조/핵심 모듈/동작을 **정확히 이해하고 결정**할 수 있도록, 실제 소스(`deep_reporter/`, `retriever/`)를 **전부 정독**해 정리. 추측 없음, 누락 없음 지향. 중요 주의사항(§8)은 반드시 확인 필요.
> 분석 경로: `/data1/jyheo/workspace/VAU_RAG/Deep-Report`. 기존 파일 무수정, 본 문서는 신규(`Deep-Report/claude_output/`).
> **근거(references)**: 논문 = *Deep-Reporter: Deep Research for Grounded Multimodal Long-Form Generation* (ACL 2026 Long #1909 / arXiv:2604.10741) — **arXiv HTML 전문**(https://arxiv.org/html/2604.10741)에서 발췌(PDF 2종은 10MB 초과로 직접 파싱 불가 → HTML 전문 사용). 코드 = `deep_reporter/`, `retriever/`, `evaluation/` 직접 정독. 논문 주장과 코드 사실을 구분 표기.

---

## 0. 논문 프레임워크 (사실 근거: ACL 2026 Long #1909 / arXiv:2604.10741)
- **문제·기여**: *Grounded Multimodal Long-Form Generation*. 기여 = (a) 3-에이전트 추론 프레임워크, (b) **M2LongBench** 벤치마크 + 정적 멀티모달 sandbox, (c) 학습(SFT/DPO, 8K agentic traces).
- **3 에이전트(순차 실행)** — 논문 표기:
  - **Planner Agent (π_plan)**: 사용자 입력 𝒰 → 구조화 global blueprint. 각 섹션 **S_k=(D_k, C_k)**. D_k = coarse-grained 설명(범위/핵심 주제), C_k={c_{k,1..m}} = **fine-grained semantic anchors**(다룰 사실·논거 = 체크리스트).
  - **Searcher–Filter (π_search, π_filter)**: "**Decomposed Information Retrieval**" — 섹션 (D_k,C_k)에 조건화한 **이중 쿼리 스트림**: **Narrative Queries 𝒬_txt**(사실 passage·통계), **Visual Queries 𝒬_img**(차트·도표·인포그래픽). 검색예산 쿼리당 **text top-20 / image top-10**. "**Relevance-Aware Filtering**" ℰ_k = {d∈𝒟_raw | 𝕀_ver(d, D_k, C_k)=1}: 텍스트 = LLM **semantic entailment**, 이미지 = **VLM informativeness**(장식 이미지 제거, 정보밀도 높은 figure 우선). 이미지는 **caption-based transcription**(이미지→상세 텍스트 설명)로 변환해 생성에 사용.
  - **Reporter Agent (π_report)**: "**Multimodal Incremental Synthesis**" — 섹션별 상태조건 생성 **R_k ∼ P_θ(· | S_k[Plan], ℰ_k[Evidence], M_{k-1}[Memory], ρ_k[Position])**. 생성 중 인용 삽입(논문 예시 표기 `![](cite:img1)`).
- **Recurrent Context Update**: **M_{k-1}=(m_global, m_local)**. m_global = 내러티브 아크의 재귀적 요약(전역 일관성), m_local = 직전 섹션의 **verbatim tail**(매끄러운 전환). 갱신 **M_k ← Φ(M_{k-1}, R_k)**.
- **M2LongBench**: **247 tasks, 9 domains**, sandbox = **95K images + 108M text chunks**(45K webpages, 6.4K PDFs), task당 GT ~**102 images + 168 text chunks**.
- **모델·학습·지표**: 테스트 모델 **Qwen3-8B/32B, Llama3.3-70B-Instruct, GPT-4.1**. 학습 **Base(ICL)/SFT(8K traces)/DPO**. 주지표 **Relative Quality Score = (S_anchor + S_content + S_full)/3**(구조 준수 / 섹션 grounding / 전체 일관성) + image selection precision 등. 한계 명시: 온라인 RL 미사용(SFT/DPO 한정), English-only, sandbox는 static.

## 0.5 논문 ↔ 공개 구현 매핑 (코드 확인)
| 논문 구성 | 코드 모듈/필드 | 비고 |
|---|---|---|
| Planner π_plan, S_k=(D_k,C_k) | `planner_node`; `SectionInfo{section_description=D_k, sectional_checklist=C_k}` | with/without planner |
| 이중 쿼리 𝒬_txt/𝒬_img | `query_generation_node` → `text_queries`/`image_queries` | |
| Decomposed Retrieval (top-20/top-10) | `search_node`(type='text'/'image'); `text_topk=20`,`image_topk=10` 기본 | 외부 HTTP |
| Relevance-Aware Filtering (LLM entailment / VLM) | `filter_node`: `FILTER_TEMPLATE`(텍스트), `IMAGE_FILTER_TEMPLATE`(VLM) | `enable_filter` |
| caption-based transcription | 이미지 item `caption`을 writer 프롬프트에 사용(픽셀 X) | |
| Reporter π_report 상태조건 합성 | `section_writing_node`(`SECTION_WRITING_TEMPLATE`: checklist+context+position ρ_k) | |
| M=(m_global, m_local), Φ | `previous_sections_summary`(=m_global) + `previous_section_tail`(=m_local); `_update_context`(=Φ) | |
| 인용 표기 | **코드 = `[citation:txt1]` / `![](citation:img1)`** | 논문 예시는 `cite:img1` → **코드 형식이 구현 기준** |
| M2LongBench sandbox retriever | `retriever/`(Flask + Milvus + Jina `jina-embeddings-v4`) | **Video RAG로 대체 대상** |
| 평가(Relative Quality Score, citation precision) | `evaluation/`(`evaluator.py`,`citation_precision_evaluator.py`,`score_calculator.py`,`prompts/`) | LLM-judge |

**★사실(repo 범위)**: 공개 repo에는 **추론 프레임워크 + sandbox retriever + 평가**만 포함. 논문의 **학습 파이프라인(SFT/DPO)·학습 데이터(8K traces)·학습 가중치는 미포함**(`train/` 디렉토리·SFT/DPO 스크립트 없음 확인). → 공개 프레임워크는 **임의의 OpenAI 호환 LLM**으로 추론(π_report 등은 프롬프트 기반, 비학습 모델로도 동작).

---

## 1. 한 줄 요약
Deep-Report = **LangGraph StateGraph 기반 멀티모달 long-form 리포트 생성기**. `planner → [섹션 루프: query_generation → search → filter → section_writing] → combine`. 검색은 **외부 HTTP 서비스**로 분리(교체 지점), writer는 **섹션 단위 점증 생성 + checklist + recurrent context + 소스인덱스 인용**. LLM은 전부 **OpenAI 호환 chat API**.

## 2. 디렉토리 구조 (실측)
```
Deep-Report/
├── start.py                     # 최상위 실행 예(1 리포트)
├── deep_reporter/
│   ├── api.py                   # LongGenAPI.generate_article(...) 진입점 ★
│   ├── core/
│   │   ├── state.py             # MultimodalLongFormState, SectionInfo (상태=데이터계약) ★
│   │   └── graph.py             # StateGraph 배선/라우팅 ★
│   ├── nodes/                   # 6개 노드
│   │   ├── planner_node.py          # outline 생성/검증
│   │   ├── query_generation_node.py # 섹션별 text/image 쿼리 생성
│   │   ├── search_node.py           # HTTP 검색 호출(교체지점) ★
│   │   ├── filter_node.py           # (옵션) 텍스트 LLM / 이미지 VLM 필터
│   │   ├── section_writing_node.py  # 섹션 작성(writer 코어) ★
│   │   └── combine_node.py          # 섹션 연결 → 최종본
│   ├── prompts/templates.py     # outline/query/writing/filter 프롬프트 ★
│   ├── llms/factory.py          # OpenAI 호환 LLM 팩토리(primary/aux/filter/vlm)
│   ├── llms/reasoning_openai.py # ChatOpenAI 래퍼
│   ├── config/{base_config,runtime_config}.py  # 설정(모델/URL/키/topk)
│   └── utils/{common_utils,llm_utils,session_logger,stream_formatter}.py
├── retriever/retriever_app.py   # 원래 내장 retriever(Flask+Milvus+Jina) — Video RAG로 대체 대상
└── evaluation/                  # 다차원 평가(citation precision 등)
```

## 3. 진입점 & 입력 계약 (`api.py`)
`LongGenAPI.generate_article(...)` 인자(= 우리가 제어하는 전부):
| 인자 | 의미 | 기본 |
|---|---|---|
| `overall_query` | 리포트 주제/요청 | — |
| `overall_checklist: List[str]` | 전체 요구사항(완성도 기준) | — |
| `generation_mode` | `"with_planner"`(자동 outline) / `"without_planner"`(외부 outline) | with_planner |
| `outline: List[{section_description, sectional_checklist}]` | without_planner 시 필수 | None |
| `text_topk` / `image_topk` | 검색 top-k | 20 / 10 |
| `enable_filter` | filter 노드 on/off | False |
| `retriever_url` | **검색 서비스 URL(교체 지점★)** | http://localhost:5555/search |
| `userid` | 세션/로그 join key | default_user |
- 반환: `{success, final_article, total_sections, outline, session_id}`. `outline`에는 섹션별 `content`, `retrieved_texts/images`, `text_queries/image_queries`가 모두 남음(후처리에 중요 §8-3).
- 내부: `initial_state` 구성 → `config={"configurable":{implementation, llm_config, retriever_url}, "recursion_limit":50}` → `graph.run/stream`.

## 4. 상태 정의 (`core/state.py`) — 데이터 계약
```python
SectionInfo = { section_description:str, sectional_checklist:List[str], content:str|None,
                text_queries:List[str]|None, image_queries:List[str]|None,
                retrieved_texts:List[Dict]|None, retrieved_images:List[Dict]|None,
                filtered_texts:List[Dict]|None, filtered_images:List[Dict]|None }
MultimodalLongFormState = { overall_query, overall_checklist, generation_mode,
                outline:List[SectionInfo], current_section_index,
                previous_sections_summary, previous_section_tail,
                text_topk, image_topk, enable_filter, final_article,
                session_id, session_logger }
```

## 5. 그래프 흐름 (`core/graph.py`)
```
entry→ planner ──(outline 있음)→ query_generation → search ──(enable_filter?)
                 └(비었으면)→ combine                         ├yes→ filter → section_writing
                                                               └no → section_writing
section_writing ──(남은 섹션?)→ yes: query_generation(다음 섹션)   /  no: combine → END
```
- **섹션 루프**: `query_generation → search → (filter) → section_writing`를 섹션마다 반복. `current_section_index`가 section_writing에서 +1.
- `recursion_limit=50`: 섹션수 × ~4노드 < 50 (≤~10섹션 안전).

## 6. 노드별 동작 (정독 요약)
1. **planner_node**: `without_planner`면 주어진 outline 검증(필드 보정)·사용. `with_planner`면 `OUTLINE_GENERATION_TEMPLATE`로 3–7 섹션 outline(JSON) 생성. 실패 시 단일 섹션 fallback.
2. **query_generation_node**: 섹션별 `text_queries`(3–5)/`image_queries`(2–4)를 overall_query+checklist+직전요약+섹션설명으로 LLM 생성(JSON). 실패 시 섹션설명을 쿼리로.
3. **search_node**: `POST retriever_url {query_list, type:'text'|'image', topk}` **두 번**(text/image) → 응답 `results`를 `section.retrieved_texts/retrieved_images`에 저장. **이미지 결과의 `img_base64`는 제거(용량)**. 실패해도 그래프는 계속(빈 리스트).
4. **filter_node**: `enable_filter=False`면 retrieved→filtered 복사(무필터). True면 (a) 텍스트: `FILTER_TEMPLATE`로 유용 인덱스 선별, (b) 이미지: **VLM이 실제 `img_path` 파일을 base64로 읽어** YES/NO. VLM 불가 시 score 상위 5개 fallback.
5. **section_writing_node**: filtered(or retrieved) 자료를 `txt1..`, `img1..`로 번호화 → `SECTION_WRITING_TEMPLATE`(overall/sectional checklist + 직전요약/tail + position)로 섹션 작성. 생성 후 `_update_context`로 요약/tail 갱신(2000자 초과 시 앞부분 압축). 사용된 인용 소스를 session_logger에 기록.
6. **combine_node**: 섹션 `content`를 `"\n\n"`로 **단순 연결** → `final_article`. 인용 개수만 카운트.

## 7. 데이터 계약 — writer가 실제로 읽는 필드 (★어댑터가 맞춰야 할 것)
`section_writing_node`/`filter_node` 코드 기준:
- **텍스트 item**: `content` (없으면 `text`) → 프롬프트 `[Source txtN begin]\n{content}\n[Source txtN end]`. (로깅: `uid`|`id`, `score`, `source`)
- **이미지 item**: `caption` (없으면 `description`, 없으면 문자열 'Image') → 프롬프트 `[Source imgN: {caption}]`. **파일 경로 `img_path`**(VLM 필터·최종 렌더링용). (로깅: `uid`|`id`, `score`)
- 원래 내장 retriever(`retriever_app.py`) 반환 item = `{id, type, text, img_path, score}` (Milvus 필드 id/type/text/img_path). → writer가 text는 `text`로도 읽지만 **이미지 `caption`은 비어서 'Image'로 뜸**(원본의 약점). **우리 어댑터는 `content`와 `caption`을 명시적으로 채워 이 약점을 제거**.
- **인용 형식**: 텍스트 `[citation:txt1]`, 이미지 `![](citation:img1)`. **번호는 "그 섹션의" 로컬 인덱스**(txt1 = 해당 섹션 retrieved_texts[0]).

## 8. ★중요 주의사항 (반드시 확인 — 설계 결정에 직결)
1. **LLM 의존성**: 모든 생성(outline/query/writer)은 **OpenAI 호환 chat LLM**(기본 `gpt-5-mini`, `OPENAI_API_KEY`/`OPENAI_BASE_URL`). 텍스트 필터는 qwen/DashScope(`AUXILIARY_*`), 이미지 필터는 로컬 VLM(`vlm_base_url` 기본 `localhost:9000/v1`). → **완전 로컬화하려면 텍스트 LLM을 vLLM OpenAI 서버로 띄워 `primary_model`/`base_url`을 지정**해야 함(WorldMM의 qwen3vl-8b는 메모리 구축용이고 별개).
2. **이미지는 생성 시 "캡션 텍스트만" 반영**: writer 프롬프트엔 이미지 픽셀이 안 들어가고 `[Source imgN: {caption}]`만 들어감. 픽셀을 보는 건 (옵션) VLM **필터**뿐. → **프레임 캡션 품질이 이미지 활용 품질을 좌우**.
3. **인용/이미지 전역 해소 없음(중요 GAP)**: `combine_node`는 섹션을 **그대로 이어붙일 뿐**, `[citation:txtN]`/`![](citation:imgN)`를 실제 출처/이미지로 **치환하지 않음**. 게다가 번호가 **섹션-로컬**이라 섹션2의 txt1과 섹션3의 txt1은 다른 소스. → **최종본은 placeholder 인용 상태**. 실제 근거(프레임 이미지 삽입, 타임스탬프/clip 표기, 참고문헌)로 바꾸려면 **별도 후처리**가 필요(각 섹션의 `retrieved_texts/images`가 `outline[idx]`에 남아 있어 섹션별로 매핑 가능; session_logger에도 섹션별 used source의 `uid`/`img_path`/`score`가 기록됨).
4. **filter는 선택**: `enable_filter=False`가 가장 단순(retrieved 직접 사용). True면 DashScope(텍스트)+로컬 VLM(이미지) 엔드포인트 필요.
5. **topk 의미**: search_node는 `query_list` 전체를 한 번에 보내고 `topk` 지정 → **어댑터가 "query_list에 대해 top-k를 어떻게 합산/정렬할지" 정의해야 함**(쿼리별 top-k 후 병합·중복제거 권장).
6. **검색 장애 내성**: 검색 실패해도 빈 리스트로 계속 진행(견고) → 증거 0이면 writer가 "No materials"로 쓸 수 있음(주의).
7. **원래 corpus는 전역(Milvus)인데 Video RAG는 per-video**: overall_query/outline은 **한 비디오**에 대한 리포트. 어댑터 서비스는 대상 video의 메모리를 로드해 섹션 쿼리에 응답.

## 9. 평가 모듈(참고)
`evaluation/`: citation precision/recall 등 다차원 평가(M2LongBench 용). 우리 과제(관제 보고서)엔 직접 쓰진 않되, **citation 기반 grounding 평가 아이디어**는 참고 가치.

## 10. 우리 과제에 대한 함의 (요약)
- **그대로 쓸 것**: planner/query_generation/section_writing/combine + state 계약 + `retriever_url` seam.
- **대체**: 내장 retriever(Milvus+Jina) → Video RAG(WorldMM/MERIT) 어댑터.
- **추가 필요**: (a) 로컬/OpenAI LLM 엔드포인트, (b) **인용·이미지 전역 해소 후처리**(관제 보고서 grounding 핵심), (c) 관제용 outline/checklist 템플릿, (d) 프레임 캡션 소스(WorldMM episodic 캡션 활용).
