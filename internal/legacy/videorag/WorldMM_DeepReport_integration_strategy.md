# WorldMM(+MERIT) × Deep-Report 통합 전략 & 어댑터 사양 (코드 기반 확정)

> 목표: Video RAG(WorldMM 중심, MERIT 교체 가능)가 **비디오 근거 검색/분석**을 수행하고, retrieve된 evidence를 근거로 **Deep-Report의 agent orchestration**이 체계적 보고서를 작성하는 프레임워크.
> 본 문서는 **실제 구현 코드 정독**으로 양쪽 데이터 계약을 확정하고, **어댑터 사양(#2)을 먼저 확정**한다. 경로=`/data1/USER/workspace/VAU_RAG`. 기존 repo 무수정, 신규는 `claude_output/`에만.

---

## 1. 백엔드 구조 재확인 (코드 근거)

### 1.1 Deep-Report (보고서 생성; LangGraph)
- 그래프(`core/graph.py`): `planner → [섹션 루프: query_generation → search → filter → section_writing] → combine`. 모드 `with_planner`(자동 outline) / `without_planner`(외부 outline 주입).
- 상태(`core/state.py`): `MultimodalLongFormState{overall_query, generation_mode, overall_checklist, outline:[SectionInfo], current_section_index, previous_sections_summary, previous_section_tail, text_topk, image_topk, enable_filter}`. `SectionInfo{section_description, sectional_checklist, text_queries, image_queries, retrieved_texts, retrieved_images, filtered_texts, filtered_images, content}`.
- **검색은 순수 HTTP 노드**(`nodes/search_node.py`): POST `retriever_url` `{query_list, type('text'|'image'), topk}` → 응답 `{status:'success', results:[...]}` → `section.retrieved_texts/retrieved_images`에 저장. **retriever_url은 config로 주입**(코드에 하드코딩 아님).
- **writer**(`nodes/section_writing_node.py`)가 소비하는 **정확한 필드**:
  - 텍스트 item: **`content`**(없으면 `text`) → 프롬프트 `[Source txtN begin]...`. 로깅용 `uid`/`id`, `score`, `source`.
  - 이미지 item: **`caption`**(없으면 `description`) → 프롬프트 `[Source imgN: <caption>]`. **주의: 프롬프트엔 캡션 텍스트만 들어가고 픽셀은 안 들어감.** 렌더링/로깅용 `img_path`, `uid`/`id`, `score`.
  - 인용: 텍스트 `[citation:txtN]`, 이미지 `![](citation:imgN)` (소스 인덱스 기반).
- query_generation(`nodes/query_generation_node.py`): 섹션별 `text_queries`(3–5)/`image_queries`(2–4)를 overall_query+checklist+section_description로 생성 → search에 전달.

### 1.2 WorldMM (Video RAG; 중심)
- 메모리 3종 + **직접 검색 메서드**(`WorldMemory`, `src/worldmm/memory/memory.py`):
  - `retrieve_from_episodic(query, top_k)` → episodic 캡션. `CaptionEntry{text, start_time, end_time, date, video_path}`, `.format_with_time()`="[time]\n{text}".
  - `retrieve_from_semantic(query, top_k)` → `TripleEntry{subject,predicate,object,timestamp}`, `.format()`="(s,p,o)".
  - `retrieve_from_visual(query, top_k)` → `ClipEntry{video_path, start_time, end_time, clip_start_sec, clip_end_sec}`(+FrameEntry). **프레임 임베딩(VLM2Vec)로 검색**.
  - 반환은 "조인된 content 문자열 + retrieved_set"(agentic QA용). **어댑터는 per-item 엔트리가 필요** → 하위 memory 객체의 retrieve(엔트리 반환) 사용 또는 retrieved_set 파싱(구현 시 확정).
- top_k 기본: episodic 3 / semantic 10 / visual 3 (`set_retrieval_top_k`로 조정).
- 메모리 DB는 이미 구축됨: `claude_output/full/metadata/{episodic,semantic,visual}_memory/{video}/` (50영상). 캡션: `claude_output/full/caption/{video}/{10sec,30sec,3min,10min}.json`.

### 1.3 MERIT (Video RAG; 교체 후보)
- `MultiKeyMemory`(`src/merit/multikey_memory.py`): 30초 clip당 4키(event/dialogue/object/summary), **MaxSim** 검색 + inference-time neighbor(시간) 확장. `retrieve(query, top_k, return_dict=...)`.
- `CaptionEntry{id, text, start_time, end_time, date, video_path}` — **WorldMM episodic과 동일 구조** → 어댑터 매핑 동일.
- 증거 = retrieved 30초 clip(캡션+video_path+시간) + 이웃 확장 context. 세만틱/비주얼 임베딩 메모리는 없음(캡션 기반).

---

## 2. ★어댑터 사양 (확정) — "Video RAG Retriever Service"

### 2.1 통합 방식 결정: **HTTP 어댑터 서비스** (Deep-Report 무수정)
- Deep-Report의 `search_node`는 `retriever_url`(config 주입)로 POST만 하므로, **동일 계약을 지키는 신규 Flask 서비스**를 `claude_output/`에 세우고 `retriever_url`만 그쪽으로 지정하면 **Deep-Report 코드/그래프를 한 줄도 수정하지 않는다.** (대안: search_node 커스텀 노드 교체 = repo 수정 필요 → 지침상 비채택.)
- 서비스는 **대상 비디오 1개의 WorldMM 메모리(또는 MERIT)를 로드/인덱싱**한 상태로 질의를 받는다(Video RAG는 per-video).

### 2.2 요청/응답 계약 (Deep-Report와 1:1 호환)
**Request** (search_node가 보냄): `POST {retriever_url}`
```json
{ "query_list": ["...", "..."], "type": "text" | "image", "topk": 20 }
```
**Response** (서비스가 반환):
```json
{ "status": "success", "results": [ {<item>}, ... ] }
```
**text item** (writer가 `content` 사용):
```json
{ "content": "[DAY1 11:12:09 - 11:12:39]\n<caption 또는 (s,p,o)>",
  "uid": "episodic:DAY1_111209", "score": 0.73,
  "source": "episodic|semantic",
  "start_time": "...", "end_time": "...", "video_path": "..." }
```
**image item** (writer가 `caption`+`img_path` 사용):
```json
{ "caption": "<해당 clip 캡션 텍스트>", "img_path": "/abs/path/frame.png",
  "uid": "visual:DAY1_111230", "score": 0.68, "source": "visual",
  "start_time": "...", "end_time": "...", "video_path": "..." }
```
- 필수: text=`content`, image=`caption`+`img_path`. 나머지는 로깅/후처리/렌더링용.

### 2.3 매핑 규칙 (생산자 → 계약)
| Deep-Report type | WorldMM 호출 | MERIT 호출 | item 생성 |
|---|---|---|---|
| `text` | `retrieve_from_episodic` + `retrieve_from_semantic`(병합·중복제거·score 정렬·topk) | `retrieve`(캡션 clip) | episodic 캡션 `format_with_time()`→`content`; semantic `(s,p,o)`→`content`; `source` 표기 |
| `image` | `retrieve_from_visual`→ClipEntry | `retrieve`한 clip | **clip 대표 프레임 추출(decord, clip 중앙)→png 저장→`img_path`**; 해당 clip의 **캡션 텍스트→`caption`** |

- **핵심 변환 1(이미지)**: Deep-Report는 이미지의 "캡션 텍스트"만 프롬프트에 쓰고 파일은 `img_path`로 참조 → 어댑터가 (a) clip 프레임을 파일로 추출, (b) clip에 대응하는 episodic 캡션을 `caption`으로 채움. 프레임 저장 경로 예: `claude_output/full/report_frames/{video}/{uid}.png`.
- **핵심 변환 2(per-item)**: WorldMM `retrieve_from_*`가 문자열을 반환하므로, 어댑터는 하위 `episodic/semantic/visual` memory의 엔트리 단위 retrieve를 사용해 item 리스트를 만든다(구현 시 정확한 메서드 확정 필요 — §5 TODO).
- **백엔드 스위치**: `source_backend = "worldmm" | "merit"` 설정으로 동일 응답 계약 유지한 채 내부만 교체(MERIT는 semantic/visual 없음 → text=캡션, image=clip 프레임만).

### 2.4 서비스 초기화/상태
- 입력: `video_id`(대상), `metadata_dir`(=`claude_output/full/metadata`), `caption_dir`(=`claude_output/full/caption`), `backend`, GPU(6/7).
- 동작: 해당 video의 episodic(HippoRAG)·semantic·visual 메모리 로드 + 인덱싱(WorldMM `eval.py`의 로딩 루틴 재사용) → `/search` 대기.
- 임베딩 모델(Qwen3-Embedding/VLM2Vec)은 서비스가 1회 로드.

---

## 3. 전체 프레임워크 설계 (오케스트레이션)
```
(사전) WorldMM/MERIT로 비디오 DB indexing  →  claude_output/full/metadata (완료: 50영상)
                                   │
[A] Video-RAG Retriever Service (신규, claude_output)  ← 대상 video_id 메모리 로드
        POST /search {query_list,type,topk} → {results:[text/image items]}
                                   │  (retriever_url로 주입, Deep-Report 무수정)
                                   ▼
[B] Deep-Report 그래프 (기존, 무수정)
     planner(or 관제 outline/checklist 주입, without_planner)
       └ 섹션 루프: query_generation → search(→[A]) → filter(옵션 off) → section_writing → combine
                                   ▼
     근거기반 멀티모달 관제 보고서 (txt/img 인용, img_path=프레임)
     (옵션) qraft식 editorial refine 후처리
```
- **Deep-Report의 원래 survey/RAG(Milvus+Jina)는 [A]로 완전 대체.** `pymilvus/jina`·내장 retriever 불필요.
- **filter_node**: Video RAG가 이미 관련도 검색 → 초기엔 `enable_filter=False`(writer가 retrieved_* 직접 사용). 후에 video-aware 필터 선택 도입.
- **outline/checklist**: 관제 보고서 템플릿(예: 개요/타임라인/관측 이벤트/이상 징후/관련 객체·인물/결론)을 `without_planner`로 주입 → query_generation이 섹션별 질의 생성 → [A]가 비디오 근거 검색.
- **overall_query**: 보고서 요청(예: "이 영상의 관제 보고서를 작성하라" + 선택적 incident 포커스). per-report = 1 video.

## 4. WorldMM vs MERIT 교체 설계
- 공통 `CaptionEntry` 구조 덕에 **[A] 서비스의 backend 스위치**로 교체. WorldMM: episodic+semantic+visual(풍부, 멀티모달 image 지원). MERIT: 캡션 clip 단일(단순·빠름, image=clip 프레임). → 동일 Deep-Report 경로에 A/B 비교 가능.

## 5. 다음 단계 (어댑터 구현 전 확정 TODO)
1. **WorldMM per-item retrieve 확정**: `retrieve_from_*`의 문자열 대신 엔트리 리스트를 얻는 경로(하위 memory.retrieve 시그니처/반환) 코드 확인 → item dict 생성.
2. **프레임 추출 유틸**: decord로 ClipEntry(clip_start/end_sec, video_path) 중앙 프레임→png. (WorldMM visual feature 추출 코드 재사용 가능 확인.)
3. **메모리 로딩 재사용**: WorldMM `eval/eval.py`의 episodic/semantic/visual 로드·index 루틴을 서비스 init으로 포팅(claude_output).
4. 관제 보고서 **outline/checklist 템플릿** 확정.
5. PoC: [A] 단독 `/search` 동작(1 video) → Deep-Report `without_planner`로 1 보고서 end-to-end.

## 6. ★개선 검토 (Deep-Report 전체 정독 반영 — `Deep-Report/claude_output/Deep-Report_analysis.md`)
정독으로 **기존 전략에 빠졌던 중요 개선점**이 드러남:
1. **(신규 필수) 인용·이미지 전역 해소 후처리**: `combine_node`는 섹션을 단순 연결하고 `[citation:txtN]`/`![](citation:imgN)`를 **치환하지 않으며 번호가 섹션-로컬**임. 관제 보고서는 **프레임 이미지 삽입 + 타임스탬프/clip 근거**가 핵심이므로, **후처리기**(신규, claude_output)를 반드시 추가: 각 섹션의 `outline[idx].retrieved_texts/images`(+session log의 uid/img_path)로 로컬 txtN/imgN → 실제 프레임 파일·시간·출처로 치환하고 참고 목록 생성. → 어댑터 item에 `start_time/end_time/video_path/img_path/uid`를 반드시 실어야 함(이미 §2.2 반영됨, 후처리 전제로 확정).
2. **(신규) LLM 엔드포인트 결정**: writer/planner/query는 **OpenAI 호환 chat LLM**(기본 gpt-5-mini) 필요 — WorldMM 메모리용 qwen3vl-8b와 **별개**. 완전 로컬 시 **텍스트 LLM을 vLLM OpenAI 서버로 띄워 `primary_model`/`openai_base_url` 지정**. (OpenAI API 사용 시 과금.) 이미지 VLM 필터는 옵션.
3. **(보강) 이미지 캡션 품질이 이미지 활용을 좌우**: writer는 이미지의 **캡션 텍스트만** 봄 → 어댑터는 clip에 대응하는 **WorldMM episodic 캡션을 image `caption`으로** 반드시 채움(빈 값이면 'Image'로 퇴화).
4. **(보강) topk 합산 규칙 확정**: search는 `query_list` 전체를 한 번에 보냄 → 어댑터는 **쿼리별 retrieve 후 병합·중복제거·score 정렬·상위 topk** 반환(§2.3).
5. **(권장) `enable_filter=False`로 시작**: Video RAG가 이미 관련도 검색. 추후 filter 쓰려면 텍스트=DashScope/로컬LLM, 이미지=로컬 VLM 엔드포인트 필요(이미지 필터는 실제 `img_path` 파일 읽음 → 어댑터가 파일 생성 보장).
6. **(견고성) 증거 공백 방지**: 검색 실패 시 Deep-Report는 빈 리스트로 계속 진행 → writer가 "No materials"로 쓸 수 있음. 어댑터는 최소 1건 이상 보장/로그.

### 개선 반영 후 최종 파이프라인
```
비디오 DB(구축완료) → [A] Video-RAG Retriever Service(신규) --retriever_url--> [B] Deep-Report(무수정)
   → [C] 인용·이미지 전역 해소 후처리(신규): 섹션별 txtN/imgN → 실제 프레임·타임스탬프·출처 치환 + 참고목록
   → 관제 보고서(프레임 삽입·시간근거 포함)   (옵션: qraft식 editorial refine)
   [LLM] OpenAI 호환 chat 엔드포인트(로컬 vLLM or OpenAI) 필요
```

## 7. 요약 결론
- **통합 접합부 = Deep-Report `retriever_url`(HTTP) 한 점.** 신규 **Video-RAG Retriever Service**가 WorldMM/MERIT 검색을 Deep-Report `results` 계약(`content` / `caption`+`img_path` + 시간·출처 메타)으로 변환 → **Deep-Report·WorldMM·MERIT repo 모두 무수정**.
- **추가 신규 컴포넌트 2개 확정**: (A) Video-RAG Retriever Service, (C) 인용·이미지 전역 해소 후처리. + LLM 엔드포인트 결정 필요.
- 어댑터 사양(§2) 확정. 구현은 §5 TODO부터.
