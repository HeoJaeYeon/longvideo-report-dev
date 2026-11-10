# CONTEXT PROMPT — Video RAG(WorldMM·MERIT) + Deep-Reporter 통합 프레임워크 (이어서 작업)

> 새 서버/새 Claude Code 세션에 **그대로 붙여넣거나 "먼저 이 파일을 읽어라"** 로 제공할 컨텍스트.
> 아래 사실은 전부 **코드 정독 근거**(추측 아님). 더 깊은 상세는 §8 문서 참조.
> 작성 2026-10-21. 기준 경로(컨테이너): `/workspace/VAU_RAG/{WorldMM,MERIT,Deep-Report}`.

---

## 0. 목표와 현재 단계
- **목표**: Video RAG(**WorldMM** 중심, **MERIT** 교체 가능)가 비디오 증거를 retrieve → **Deep-Reporter**(LangGraph)가 **근거기반 long-form 보고서**(프레임 삽입·타임스탬프 근거)를 생성. 1차 타깃 = Long Video(Video-MME 계열), 이후 관제/CCTV.
- **현재 단계**: 분석·설계 **확정 완료**, Docker 통합환경 **구축 완료(빌드 미실행)**. 다음 = **`report_framework/` 실구현 PoC**(§5 TODO).
- **원칙**: 세 repo(WorldMM/MERIT/Deep-Report) **코드 무수정**. 신규 산출물은 `Deep-Report/claude_output/report_framework/` 에만.

## 1. 저장소·환경 (컨테이너 기준)
- 통합 venv = 이미지 `/opt/venv`(자동활성). worldmm/hipporag/merit 는 마운트 editable, deep_reporter 는 PYTHONPATH. (상세 §8 DOCKER_SETUP_REPORT.md)
- 세 repo: `/workspace/VAU_RAG/{WorldMM, MERIT, Deep-Report}` (= 호스트 VAU_RAG 마운트). 최초 1회 `intsetup` → `intcheck`("integration imports OK") 로 준비 확인.
- 작성 LLM(Deep-Reporter writer/planner/query) = **OpenAI 호환 엔드포인트**. 로컬 qwen3(vLLM) 기본, OpenAI 스위치 보존(§4 D1).

## 2. 세 시스템 핵심 사실 (코드 근거)

### 2.1 WorldMM (`WorldMM/src/worldmm`, 상세 WorldMM/claude_output/WorldMM_analysis.md)
- 3메모리: **episodic**(캡션→HippoRAG + LLM `multiscale_filter`), **semantic**(triple→igraph **Personalized PageRank**, HippoRAG 아님), **visual**(VLM2Vec clip→프레임).
- **per-item 검색 seam**(통합이 쓰는 저수준 API; `answer()` 에이전트는 미사용):
  - `episodic_memory.retrieve(query, final_top_k, as_context=False)` → `List[CaptionEntry{text,start_time,end_time,date,video_path,granularity}]`
  - `semantic_memory.retrieve(query, top_k, as_context=False)` → `List[SemanticTripleEntry{subject,predicate,object,timestamp}]`
  - `visual_memory.retrieve(query, top_k, as_context=True)` → `{display_time: [PIL.Image,...]}` (프레임)
  - ★검색 전 `world_memory.index(until_time)` 필수. Video-MME는 `QUERY_TIME=int("1"+"23595999")=123595999`(영상끝).
- 2 LLM(retriever=OpenIE/multiscale filter, respond=reasoning+QA). QA는 멀티모달(프레임 이미지 투입).
- **gpt→qwen 로컬화 수정(git 미커밋, 4파일)**: `script/4_eval.sh`·`script/videomme/4_eval.sh`(기본 `RET_MODEL=RESP_MODEL=qwen3vl`), `src/worldmm/llm/qwen3vl.py`(generate에 `threading.Lock` + 구조화출력 파서 강건화), `src/worldmm/memory/episodic/multiscale.py`(단일 LLM 공유 + `max_workers=1`). 라우팅 `llm/llm_wrapper.py`: "gpt"→OpenAI, "qwen3"→로컬 Qwen3VL.

### 2.2 MERIT (`MERIT/src/merit`, 상세 아래 §3 백엔드·설계문서 §10)
- **단일 멀티키 episodic 메모리**(clip당 4키 event/dialogue/object/sum), 검색 = **MaxSim**(쿼리 vs 활성키 최대), **검색 시 LLM 0**.
- per-item seam: `MeritMemory.retriever.retrieve(query, top_k, as_context=False, return_dict=True)` → `{retrieved_entries:[CaptionEntry], all_candidates}`.
- `CaptionEntry` 는 WorldMM과 사실상 동일(granularity만 없음). key파일 = WorldMM 캡션 + 4키. **decord 프레임 추출기 내장**: `MeritMemory._extract_frames_from_video(video_path, num_frames)`(num=1=중앙프레임) → 재사용.
- WorldMM venv에 없는 런타임 의존은 **opencv(headless) 하나**뿐(나머지 충족) → `--no-deps -e` 로 설치.

### 2.3 Deep-Reporter (`Deep-Report/deep_reporter`, 상세 Deep-Report/claude_output/Deep-Report_analysis.md)
- LangGraph: planner(outline+섹션 checklist) → 섹션마다 `query_generation`(LLM→`text_queries`/`image_queries`) → **`search`(HTTP `retriever_url`)** → filter(옵션) → section_writing → combine.
- **유일한 외부 접합 = `retriever_url`**: `POST {query_list, type:'text'|'image', topk}` → `{status:'success', results:[item]}`. writer는 text item의 `content`(없으면 `text`), image item의 `caption`(없으면 `description`→'Image') + `img_path` 사용.
- **인용은 섹션-로컬** `[citation:txtN]` / `![](citation:imgN)` — `combine_node` 가 **전역 치환하지 않음**(count만) → 통합에 **후처리기 필수**.
- 작성 LLM = `ChatOpenAI`(`get_primary_llm`), `openai_base_url` 만 바꾸면 로컬/OpenAI 전환(코드 수정 0).
- 진입점 `deep_reporter/api.py::generate_article(overall_query, overall_checklist, generation_mode, outline, text_topk=20, image_topk=10, enable_filter=False, retriever_url, userid)`. `generation_mode="without_planner"` 면 주입 outline 사용.

## 3. 통합 아키텍처 (확정; 상세 WorldMM_DeepReport_integration_design.md)
```
사전: WorldMM DB(metadata/{epi,sem,vis}) + caption/{vid}/{10sec,30sec,3min,10min}.json   (§7 위치)
  │
[A] Video-RAG Retriever Service (신규, Flask)
     init(video_id): WorldMemory 로드 + index(QUERY_TIME) 1회(캐시)
     POST /search {query_list,type,topk}:
       type=text  → episodic.retrieve(as_context=False)(+semantic 보조) → item{content,uid,score,source,start/end_time,video_path}
       type=image → visual.retrieve → clip 대표 프레임 png 저장 → item{caption(=대응 episodic 캡션),img_path,uid,...}
       쿼리별 retrieve→병합→uid dedup→score 정렬→상위 topk
  │ retriever_url
[B] Deep-Reporter 그래프 (무수정): without_planner(관제 outline/checklist 주입) → query_gen→search(→A)→(filter off)→section_writing→combine
  │ final_article + outline[*].retrieved_texts/images + session_log
[C] Grounding 후처리기 (신규): 섹션-로컬 [citation:txtN]/![](citation:imgN) → 실제 프레임·타임스탬프·출처로 전역 치환 + References
  ▼  근거기반 멀티모달 보고서
[LLM] writer/planner/query = 로컬 qwen3 vLLM(OpenAI 호환, 기본) / OpenAI(스위치)
```

### 3.1 백엔드 추상화 (WorldMM↔MERIT 스위치 핵심)
`[A]` 가 **backend 객체 하나**에만 의존. `backend=worldmm|merit` 한 줄로 교체.
```python
# Deep-Report/claude_output/report_framework/backend_base.py (신규)
@dataclass
class EvidenceItem:
    uid: str; modality: str        # "text"|"image"
    content: str                   # text=캡션/triple ; image=caption(=대응 캡션)
    start_time: str; end_time: str; video_path: str
    score: float; source: str      # worldmm-episodic|worldmm-semantic|worldmm-visual|merit
    img_path: str | None = None    # image 전용(프레임 png 절대경로)
class VideoRAGBackend(Protocol):
    def load(self, video_id)->None: ...
    def index(self, until_time)->None: ...
    def retrieve_text(self, queries:list[str], topk:int)->list[EvidenceItem]: ...
    def retrieve_image(self, queries:list[str], topk:int)->list[EvidenceItem]: ...
```
- WorldMMBackend: text=episodic(+semantic 보조), image=visual 프레임 + 동 시간대 episodic 캡션을 content.
- MeritBackend: text=clip 캡션(MaxSim), image=동 clip `_extract_frames_from_video(…,1)` 중앙 프레임 + content=clip 캡션.
- EvidenceItem이 두 backend 최소공통 + 인용해소 필수필드(uid/시간/video_path/img_path) 포함 → MERIT 추가 = **MeritBackend 1개만**, [A]/[B]/[C] 무수정.

## 4. 결정사항 (사용자 승인)
- **D1 LLM**: 로컬 qwen3 계열(vLLM OpenAI 서버) **기본**, OpenAI 경로 **보존(스위치)**. `run_report.py` 설정 `llm_backend: local|openai` → Deep-Report `openai_base_url`/`primary_model` 주입. ⚠️ vLLM은 **별도 컨테이너**로 서빙(이 통합 이미지와 torch 핀 충돌 회피).
- **D2 범위**: 작은 PoC 먼저(1영상, outline 주입, filter off, 후처리 포함) → 확장.
- **D3 백엔드**: WorldMM 최우선 구현, MERIT는 스위치+MeritBackend 1개로 교체(지금 추상화 설계 반영됨).

## 5. 구현 TODO (순서)
0. `report_framework/backend_base.py`(EvidenceItem/Protocol) 확정.
1. **WorldMMBackend + per-item 검색 스모크**: 1영상 load→index→retrieve_text/image 반환 실측.
2. 프레임 유틸(decord 중앙 프레임; MERIT `_extract_frames_from_video` 이식) → `report_frames/{vid}/{uid}.png`.
3. **[A] `videorag_retriever_service.py`**(Flask `/search`, backend=worldmm) + Deep-Reporter `search_node` 계약 curl 테스트.
4. 로컬 qwen3 **vLLM 서버 기동**(별도) → Deep-Report `generate_article(generation_mode="without_planner", retriever_url=…)` 로 **1섹션 PoC**.
5. **[C] `grounding_postprocessor.py`**: placeholder 인용 → 프레임/시간/출처 치환 + References.
6. **`surveillance_outline.py`**(개요/타임라인/관측이벤트/이상징후/관련객체·인물/결론) → 1영상 **end-to-end 보고서**(`run_report.py` 오케스트레이션).
7. (후속) MeritBackend 추가(스위치 검증) · 평가 · 이미지 VLM 필터 · editorial refine.

## 6. 주의점/리스크 (코드 근거)
- **R1 성능**: WorldMM episodic `retrieve` 는 쿼리당 조건부 LLM(multiscale_filter) + `index`는 HippoRAG 재구축(수 분). → init에서 `index` 1회만, `final_top_k` 작게(3), 섹션당 쿼리 제한, (video,query) 캐시. MERIT backend는 검색 LLM 0으로 훨씬 가벼움.
- **R2 쿼리**: WorldMM/MERIT의 agentic `answer()`(자체 쿼리생성·멀티라운드)는 **미사용** — Deep-Reporter 쿼리를 per-item retrieve에 직투입(1차 단순안). 적응검색 이점은 포기(트레이드오프).
- **R3 text 비대칭**: text = episodic 캡션 우선 + semantic 보조(semantic `(s,p,o)` 짧음). image = visual만.
- **R4 이미지 grounding 이중작업**: clip → (대표 프레임 png + 대응 캡션 + 시간) 동시 생성 + 후처리 전역 치환.
- **R5 평가 부재**: 1차 성공기준 = 파이프라인 동작 + 인용-프레임/시간 일치 + 서술-영상 일치(정성). 정량 GT는 후속.
- **런타임 import 전제**: `intsetup` 후에만 worldmm/merit/hipporag/deep_reporter import 가능.
- **langgraph 1.x**: Deep-Report가 쓰는 `StateGraph(config_schema=…)` 실제 호출은 빌드 후 1회 확인 권장(`python -c "from deep_reporter.core.graph import MultimodalLongFormGraph; MultimodalLongFormGraph()"`).

## 7. WorldMM 50영상 DB 위치 & ★새 서버 주의
- **현재 서버 기준** 구축 완료: `WorldMM/claude_output/full/metadata/{episodic,semantic,visual}_memory/{vid}/`(파일 접미사 `qwen3vl-8b`), 캡션 `WorldMM/claude_output/full/caption/{vid}/{10sec,30sec,3min,10min}.json` (각 50영상, 전수 검증). eval 입력 `WorldMM/data/Video-MME/videomme/test.json`.
- ★**새 서버에는 이 DB가 없습니다**(fresh clone). [A] 서비스 PoC를 돌리려면 최소 1영상의 **WorldMM DB(metadata+caption)를 복사하거나 재구축** 필요. (재구축: `WorldMM/preprocess/build_memory.py`, 상세 WorldMM_analysis.md §3 + REPORT.md.)
- 파일럿 성능(참고): Video-MME Long 8영상/24문항 최종 12/24=50.0%(1차 37.5%→OOM복구). 목표 WorldMM-8B(L)=66.0%.

## 8. 참고 문서 (상세 — 깊이 필요할 때)
> ⚠️ 아래 중 `VAU_RAG/claude_output/*` 는 최상위라 git clone으로 안 따라올 수 있음 → 새 서버로 **별도 복사** 필요.
- `WorldMM_DeepReport_integration_design.md` (통합 설계 전체 + MERIT 분석§10 + 백엔드 추상화§11 + LLM 스위치§12) ★1순위
- `VideoRAG_ReportGen_analysis_v2.md` (독립분석 + 개선점 6건 코드검증§7)
- `WorldMM/claude_output/WorldMM_analysis.md` (WorldMM 구현 상세) · `REPORT.md`/`HANDOFF.md`(50영상·성능)
- `Deep-Report/claude_output/Deep-Report_analysis.md` (Deep-Reporter 상세) · `DOCKER_SETUP_REPORT.md`(환경)
- `VAU_RAG/claude_output/PROJECT_CONTEXT_HANDOFF.md` (전 범위 핸드오프)

## 9. 코딩 제약 (프로젝트 규칙)
- WorldMM/MERIT/Deep-Report **기존 코드 수정·삭제 금지**(사전 승인 없이). 수정 필요 시 파일·위치·변경안 보고 후 승인 대기.
- 신규 파일은 `Deep-Report/claude_output/report_framework/` 에만.
- 추측 금지 — 코드/파일 직접 확인 후 사실 기반으로.
