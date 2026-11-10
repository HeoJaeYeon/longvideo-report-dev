# WorldMM × Deep-Reporter 통합 설계 — 비판적 재검토 & 개선 전략 (확정판)

> 목적: 지금까지의 분석(`VideoRAG_ReportGen_analysis_v2.md`, `WorldMM_DeepReport_integration_strategy.md`, `WorldMM/claude_output/WorldMM_analysis.md`, `Deep-Report/claude_output/Deep-Report_analysis.md`)을 **객관적·비판적으로 재검토**하고, 구체적 통합 설계와 개선책을 확정. 모든 주장은 코드 정독 근거. 신규 작성물은 `claude_output/`에만.
> 경로: `/data1/jyheo/workspace/VAU_RAG`. 작성 2026-10-16.

---

## 1. 통합의 본질 (한 문장)
Deep-Reporter의 **외부 검색 seam(`retriever_url` HTTP)** 을 **WorldMM 검색으로 치환**하고, Deep-Reporter가 생성한 **섹션-로컬 placeholder 인용**을 **후처리로 실제 프레임·타임스탬프·출처에 grounding**하면, 세 repo 무수정으로 "비디오 근거 보고서" 프레임워크가 성립한다.

## 2. 양측 접합부 재확인 (코드 사실)
- **Deep-Reporter가 기대하는 것**(소비 계약): `POST retriever_url {query_list, type:'text'|'image', topk}` → `{status:'success', results:[item]}`. writer는 text item의 `content`(없으면 `text`), image item의 `caption`(없으면 `description`→'Image')+`img_path`를 사용. 인용은 섹션-로컬 `[citation:txtN]`/`![](citation:imgN)`.
- **WorldMM이 제공하는 것**(per-item 검색): `episodic_memory.retrieve(query, final_top_k, as_context=False)`→`List[CaptionEntry{text,start_time,end_time,date,video_path,granularity}]`; `semantic_memory.retrieve(query, top_k, as_context=False)`→`List[SemanticTripleEntry{subject,predicate,object,timestamp}]`; `visual_memory.retrieve(query, top_k, as_context=True)`→`{display_time: [PIL.Image,...]}`. **주의: 검색 전 `index(until_time)` 필수.**

## 3. ★비판적 재검토 — 기존 전략의 약점/리스크 (객관적)
지금까지 "HTTP 어댑터 1개 + 후처리 1개"로 정리했으나, 코드를 다시 보면 **다음 리스크가 과소평가**되어 있었다:

### R1. WorldMM 검색은 "무겁고 상태적(stateful)"이다 — HTTP 서비스화의 실제 비용
- episodic `retrieve`는 내부에서 **HippoRAG 검색 + LLM(multiscale_filter) 호출**을 수행(쿼리당 LLM 1회). Deep-Reporter는 섹션마다 `text_queries`(3–5개)를 보냄 → **섹션당 episodic LLM 필터 3–5회 + semantic PPR + (이미지면) visual 프레임 추출**. 섹션 5개면 보고서 1건에 수십 회 LLM 호출. → **느림**. (이미 eval에서 영상당 수십 분 관측.)
- 게다가 `index(until_time)`는 **HippoRAG 그래프를 캡션으로 재구축**(OpenIE 재실행). per-video 서비스 기동 시 1회성이나 **수 분** 소요.
- **함의**: "retriever_url 하나 바꾸면 끝"은 데이터 계약상 맞지만, **성능/지연은 심각**. 설계에 **캐시·사전인덱싱·쿼리 배칭**을 반드시 포함해야 함.

### R2. "검색 쿼리를 LLM이 매 섹션 생성"하는 중복
- Deep-Reporter `query_generation_node`가 LLM으로 `text_queries/image_queries`를 만들고, WorldMM `answer()`의 reasoning agent도 원래 **자체적으로 memory_type+search_query를 생성**한다. 통합 시 **WorldMM의 agentic reasoning은 우회**되고 Deep-Reporter 쿼리를 그대로 memory 검색에 투입 → WorldMM의 "다중 라운드 적응 검색" 가치가 사라짐.
- **개선 선택지**: (a) 단순: Deep-Reporter 쿼리를 WorldMM 하위 메모리에 직접 질의(간단, WorldMM reasoning 미사용). (b) 고급: 섹션 쿼리를 WorldMM `answer()`류 다중라운드로 확장. → **1차는 (a), 품질 부족 시 (b)**.

### R3. 텍스트/이미지 메모리 매핑의 비대칭
- Deep-Reporter는 text/image **2스트림**. WorldMM은 **3메모리**(episodic/semantic=텍스트, visual=이미지). → `type='text'`는 episodic+semantic 병합, `type='image'`는 visual. **그런데 semantic triple `(s,p,o)`은 짧아 writer 근거로 약함** → text 결과는 **episodic 캡션 위주 + semantic 보조** 가중이 바람직.

### R4. 이미지 grounding의 이중 과제
- (1) writer 프롬프트엔 **캡션만** 들어가므로 visual clip에 **대응 캡션**(episodic 10sec/30sec)을 붙여야 하고, (2) 후처리로 `![](citation:imgN)`을 **실제 프레임 png**로 치환해야 함. → 어댑터는 **clip→(대표 프레임 png + 캡션 텍스트 + 시간)** 3종을 동시에 만들어야 함.

### R5. 평가/성공기준 부재
- 관제 보고서의 품질을 **무엇으로 측정**할지 미정. Deep-Reporter의 `evaluation/`(citation precision 등)은 M2LongBench 전용. Video-MME는 QA 정답이지 보고서 GT가 아님. → **1차 성공기준 = (i) 파이프라인 end-to-end 동작, (ii) 인용이 실제 프레임/시간에 grounding, (iii) 사람이 읽어 사건 서술이 영상과 일치**(정량 GT는 후속).

## 4. 개선된 통합 아키텍처 (확정)
```
사전: WorldMM DB(구축완료, metadata/{epi,sem,vis})  +  caption/{vid}/{10sec,30sec,3min,10min}.json
                                   │
[A] Video-RAG Retriever Service (신규, Flask; claude_output/report_framework/)
     init(video_id): WorldMemory 로드 + index(QUERY_TIME) 1회 (캐시)
     POST /search {query_list,type,topk}:
       type=text  → 쿼리별 episodic.retrieve(as_context=False)+semantic.retrieve → item{content,uid,score,source,start/end_time,video_path}
       type=image → 쿼리별 visual.retrieve → clip 대표 프레임 png 저장 → item{caption(=대응 episodic 캡션),img_path,uid,score,start/end_time,video_path}
       (쿼리별 top-k 후 병합·dedup(uid)·score 정렬·상위 topk)   # R-aggregation
                                   │ retriever_url
[B] Deep-Reporter 그래프 (무수정)
     planner(without_planner: 관제 outline/checklist 주입) → [query_gen → search(→A) → (filter off) → section_writing] → combine
                                   │ final_article + outline[*].retrieved_texts/images + session_log
[C] Grounding 후처리기 (신규, claude_output/report_framework/)
     섹션별 로컬 [citation:txtN]/![](citation:imgN) → 전역 근거 치환:
       txtN → "(DAYd HH:MM:SS, video_path)" + 참고목록 번호
       imgN → 실제 프레임 이미지 삽입(상대경로) + 캡션/시간
     + 보고서 말미 References(uid·시간·source) 생성
                                   ▼
     근거기반 멀티모달 관제 보고서(프레임 삽입·시간근거)  (옵션: qraft editorial refine)
[LLM] writer/planner/query = OpenAI 호환 chat 엔드포인트 (local↔openai 스위치, §12)
     기본(결정): 로컬 qwen3 계열(vLLM OpenAI 서버) → openai_base_url 지정 (무과금·완전로컬)
     대안: OpenAI gpt-5-mini (openai 경로 보존, 스위치로 선택)
```

## 5. 개선책 상세 (R1–R5 대응)
- **R1(성능)**: ① 서비스 init에서 `index(QUERY_TIME)` **1회**만(요청마다 X). ② episodic multiscale_filter LLM 호출이 병목 → 1차엔 **`final_top_k`를 작게(3)** + **쿼리 수 제한**(섹션당 text_queries 3). ③ 동일 (video, query) 결과 **캐시**. ④ 필요시 episodic 필터를 끄고 HippoRAG score 상위로 대체하는 옵션.
- **R2(쿼리 생성)**: 1차 = Deep-Reporter 쿼리 직투입(단순). WorldMM reasoning은 미사용(명시). 품질 부족 시 섹션 쿼리당 WorldMM 다중라운드 확장 PoC.
- **R3(text 병합)**: text 결과 = episodic 우선, semantic은 보조(예: episodic top-(k-2) + semantic top-2) — 설정화.
- **R4(이미지)**: visual clip → decord로 **대표 프레임(중앙) png** 저장(`report_frames/{vid}/{uid}.png`) + 동 clip 시간대의 episodic 캡션을 `caption`으로. (WorldMM visual feature 추출 코드의 프레임 로직 재사용 검토.)
- **R5(평가)**: 1차 정성(인용-프레임 일치, 서술-영상 일치) + 파이프라인 동작. 후속: Video-MME QA를 보고서에서 답 추출해 교차검증(보고서가 QA에 필요한 근거를 담았는지).

## 6. 신규 컴포넌트 확정 (claude_output/report_framework/)
1. **`videorag_retriever_service.py`** [A]: WorldMemory 로드/인덱싱 + Flask `/search`(Deep-Reporter 계약 준수). backend 스위치(worldmm|merit).
2. **`worldmm_evidence_adapter.py`**: per-item 검색 → Deep-Reporter item 매핑(§2 계약) + 프레임 png 생성 + topk 병합.
3. **`grounding_postprocessor.py`** [C]: final_article + outline 증거 → 인용/이미지 전역 치환 + References.
4. **`surveillance_outline.py`**: 관제 outline/checklist 템플릿(개요/타임라인/관측 이벤트/이상 징후/관련 객체·인물/결론).
5. **`run_report.py`**: 오케스트레이션(서비스 기동 → Deep-Reporter `generate_article(without_planner, retriever_url)` → 후처리 → 저장).
+ LLM 엔드포인트 설정(로컬 vLLM or OpenAI).

## 7. 결정 확정 (D1/D2/D3 — 사용자 승인됨 2026-10-19)
- **D1. LLM 엔드포인트 = 로컬 qwen3 계열 기본 + OpenAI 경로 보존(스위치)**. WorldMM 때처럼 OpenAI를 호출하지 않고 로컬 LLM/MLLM(qwen3 계열 최신)으로 보고서 작성. 단 OpenAI 경로를 **삭제하지 않고** local↔openai를 **설정 스위치**로 선택. 구현 세부 → §12.
- **D2. 작은 PoC 먼저**(1영상, outline 주입, filter off, 후처리 포함) → 동작 확인 후 전체 확장.
- **D3. WorldMM 최우선 + MERIT는 스위치 교체**: 지금 MERIT 코드를 분석(→§10)해 **공통 백엔드 추상화(§11)** 를 먼저 설계. 1차는 WorldMM만 구현하되, 나중에 MERIT 추가 시 **backend 스위치 변경 + MERIT 어댑터 1개 추가**로 끝나도록(기존 [A]/[B]/[C] 무수정).

## 8. 단계별 실행 계획 (TODO)
1. **[A/어댑터] WorldMM per-item 검색 스모크**: 1영상 로드→`index`→episodic/semantic/visual `retrieve` 반환 필드 실측(이미 코드 확인; 실런 1회).
2. **프레임 추출 유틸** 검증(decord, clip 중앙 프레임 png).
3. **[A] Flask `/search`** 최소 구현 + Deep-Reporter `search_node` 계약 적합성 테스트(curl).
4. **LLM 엔드포인트**(D1) 결정·기동 → Deep-Reporter `without_planner`로 1섹션 생성 PoC.
5. **[C] grounding 후처리** 구현 → placeholder 인용을 프레임/시간으로 치환.
6. 관제 outline/checklist 확정 → 1영상 end-to-end 보고서.
7. (후속) 평가·MERIT A/B·editorial refine.

## 9. 결론
- 6개 개선점(§v2.7) 전부 코드로 CONFIRMED → 전략 유지.
- **단, "HTTP 치환 1줄" 식 낙관을 교정**: 실제 비용은 (i) WorldMM 검색의 LLM/인덱싱 지연(R1), (ii) agentic reasoning 우회 트레이드오프(R2), (iii) 이미지 grounding 이중작업(R4)에 있음 → 설계에 캐시·사전인덱싱·프레임생성·후처리기를 **1급 컴포넌트**로 포함(§6).
- 세 repo 무수정 원칙 유지, 신규는 `claude_output/report_framework/`.

---

## 10. MERIT 코드 분석 (D3 — 스위치 교체 설계 근거, 코드 정독)
경로 `/data1/jyheo/workspace/VAU_RAG/MERIT`. 정독 파일: `src/merit/{types.py, merit_memory.py(563), multikey_memory.py(273)}`, `preprocess/extract_keys.py(175)`.

### 10.1 구조 (사실)
- **단일 메모리**: MultiKeyMemory(episodic 전용). WorldMM의 3메모리(episodic/semantic/visual)와 달리 **1종**.
- **데이터 단위**: 30초 clip. `CaptionEntry{id, text, start_time, end_time, date, video_path}` — **WorldMM `CaptionEntry`와 사실상 동일**(단 `granularity` 필드 없음).
- **4키**(clip당): `event_key`, `dialogue_key`, `object_key`, `sum_key`. key 파일 = **WorldMM 30초 캡션 JSON에 4키를 추가**한 `*_4_key.json`(`extract_keys.py`가 LLM `multikey_extract`로 생성). ⇒ **입력 데이터가 WorldMM 캡션과 호환**(재사용).
- `set_active_keys(["event","dialogue","object","summary"])`로 키 부분집합 선택 가능.

### 10.2 검색(핵심 seam) — `MultiKeyMemory.retrieve` / `MeritMemory`
- `index(until_time)`: `end<=until_time` clip의 각 키를 `encode_text`로 임베딩(키 타입별 텐서). **LLM 호출 없음**.
- `retrieve(query, top_k, as_context=False, return_dict=True, until_time, exclude_texts)`: **MaxSim** — 쿼리 임베딩 vs 각 활성 키 타입 cosine → clip별 **최대값**으로 스코어 → 중복(`exclude_texts`) 제외 top-k → `{retrieved_entries:[CaptionEntry], all_candidates:[{entry, key_type, score,...}]}`. **검색 시 LLM 호출 없음**(순수 임베딩).
- 프레임: `MeritMemory._extract_frames_from_video(video_path, num_frames)` = **decord 기반 깔끔한 추출기**(linspace, num=1이면 중앙 프레임). → 우리 어댑터 프레임 유틸로 **재사용 가능**(R4 해결).
- `MeritMemory.answer()`는 추가로 neighbor temporal expansion + LLM neighbor_filter + 멀티모달 QA를 함 → **보고서 통합에서는 우회**(WorldMM과 동일 정책, R2).

### 10.3 WorldMM vs MERIT 비교 (통합 관점)
| 항목 | WorldMM | MERIT |
|---|---|---|
| 메모리 종류 | episodic+semantic(텍스트) + visual(이미지) **3종** | multi-key episodic **1종** |
| 텍스트 근거 | episodic 캡션(HippoRAG+LLM filter) + semantic triple(PPR) | clip 캡션(MaxSim 4키) |
| 이미지 근거 | visual memory(VLM2Vec→프레임) | 동일 clip → decord 프레임 |
| **검색당 LLM** | episodic multiscale_filter LLM **1회/쿼리** | **없음**(MaxSim만) |
| index 비용 | HippoRAG 재구축(OpenIE) **수 분** | 키 임베딩 **수 초** |
| per-item seam | `episodic/semantic.retrieve(as_context=False)`, `visual.retrieve(as_context=True)` | `retriever.retrieve(as_context=False, return_dict=True)` |
| 데이터 | metadata/{epi,sem,vis}+captions | `*_4_key.json`(WorldMM 캡션+4키) |
| CaptionEntry | +granularity | granularity 없음 |
- **함의**: MERIT backend는 **R1(성능)에서 훨씬 유리**(검색 LLM 0, index 가볍다). 다만 semantic triple·VLM2Vec 유사도 같은 WorldMM 고유 근거는 없음.

## 11. ★백엔드 추상화 인터페이스 (D3 — 스위치 교체의 핵심)
[A] Retriever Service가 **backend 객체 하나**에만 의존하도록, 공통 프로토콜을 정의. WorldMM/MERIT가 각각 구현. 교체 = `backend=worldmm|merit` 설정 한 줄.

```python
# claude_output/report_framework/backend_base.py (신규)
@dataclass
class EvidenceItem:
    uid: str                 # 전역 유일 id (dedup/인용 해소용)
    modality: str            # "text" | "image"
    content: str             # text: 캡션/triple 문자열 ; image: caption(=대응 캡션)
    start_time: str          # "DAYd HH:MM:SS"
    end_time: str
    video_path: str
    score: float
    source: str              # "worldmm-episodic"|"worldmm-semantic"|"worldmm-visual"|"merit"
    img_path: Optional[str] = None  # image 전용(프레임 png 절대경로)

class VideoRAGBackend(Protocol):
    def load(self, video_id: str) -> None: ...
    def index(self, until_time: int) -> None: ...        # init시 1회
    def retrieve_text(self, queries: List[str], topk: int) -> List[EvidenceItem]: ...
    def retrieve_image(self, queries: List[str], topk: int) -> List[EvidenceItem]: ...
```
- **공통 규칙**(두 backend 동일): 쿼리별 retrieve → 병합 → `uid` dedup → `score` 정렬 → 상위 topk(§3 R-aggregation). 프레임 png는 `report_frames/{vid}/{uid}.png`(decord 중앙 프레임, MERIT 유틸 재사용).
- **WorldMMBackend**: `retrieve_text`=episodic.retrieve(as_context=False) 우선 + semantic.retrieve 보조(R3 가중) → EvidenceItem(source=worldmm-episodic/semantic). `retrieve_image`=visual.retrieve(as_context=True)로 프레임 확보 + 동 시간대 episodic 캡션을 content(caption)로.
- **MeritBackend**: `retrieve_text`=retriever.retrieve(return_dict=True).retrieved_entries → content=clip 캡션. `retrieve_image`=동일 clip entries → `_extract_frames_from_video(video_path,1)` 중앙 프레임 png + content=clip 캡션.
- [A] Flask `/search`는 `type`에 따라 backend.retrieve_text/image 호출 후 Deep-Reporter 계약(`{content|caption, img_path, ...}`)으로 직렬화. **→ Deep-Reporter·후처리기는 backend 불문 동일 동작.**
- 설계 원칙: EvidenceItem이 **두 backend의 최소공통 + 인용해소 필수필드**(uid/시간/video_path/img_path)를 모두 포함하므로, MERIT 추가 시 [A]/[B]/[C] 수정 0, **MeritBackend 클래스 1개만 추가**.

## 12. LLM 엔드포인트 스위치 구성 (D1)
Deep-Report의 작성 LLM은 코드상 이미 `ChatOpenAI`(OpenAI 호환) → **base_url만 바꾸면** 로컬/OpenAI 전환(코드 수정 0, 설정만).
- **로컬(기본)**: qwen3 계열 텍스트 LLM을 **vLLM OpenAI 서버**로 기동(`vllm serve <qwen3-instruct> --port 8000`) → Deep-Report config `primary_model=<모델명>`, `openai_base_url=http://localhost:8000/v1`, `openai_api_key=dummy`. 무과금·데이터 로컬.
- **OpenAI(대안, 보존)**: `openai_base_url` 미설정(기본) + 실제 `OPENAI_API_KEY` + `primary_model=gpt-5-mini`.
- **스위치**: `run_report.py`의 설정(`llm_backend: local|openai`)이 위 두 세트를 선택해 Deep-Report `generate_article(...)`에 주입. **OpenAI 경로 코드/설정은 삭제하지 않음**(요구사항).
- 이미지 VLM 필터(옵션, PoC에선 off): 켤 경우 로컬 **qwen3-VL**를 vLLM OpenAI-vision 서버로(별 엔드포인트). 1차 범위 밖.
- ⚠️ 자원: 로컬 작성 LLM 서버가 **GPU 추가 점유**. 메모리 구축/eval과 동시 실행 시 GPU 계획 필요(현 공유환경 제약).

### 통합 TODO 갱신 (D1/D2/D3 반영)
0. (설계) `backend_base.py`(EvidenceItem/Protocol) 확정 — §11.
1. **WorldMMBackend + per-item 검색 스모크**(1영상 load→index→retrieve_text/image 실측).
2. 프레임 유틸(decord 중앙 프레임; MERIT `_extract_frames_from_video` 이식).
3. [A] Flask `/search`(backend=worldmm) + Deep-Reporter `search_node` 계약 curl 테스트.
4. 로컬 qwen3 vLLM 서버 기동 → Deep-Report `without_planner`로 1섹션 PoC(스위치=local).
5. [C] grounding 후처리(placeholder→프레임/시간/출처).
6. 관제 outline/checklist → 1영상 end-to-end 보고서.
7. (후속) MeritBackend 추가(스위치 검증) · 평가 · VLM 필터 · editorial refine.
