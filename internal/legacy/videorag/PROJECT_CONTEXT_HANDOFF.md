# PROJECT CONTEXT HANDOFF — VideoRAG(WorldMM·MERIT) + Deep-Reporter 보고서 생성 프레임워크

> 목적: **다른 A6000 서버에서 새 Docker 컨테이너를 구축하고 Claude Code에 주입할 컨텍스트**. 작성 2026-10-20.
> 원칙: 아래 모든 사실은 **코드/파일시스템 직접 확인**으로 검증됨(추측 없음). 상세는 각 절이 가리키는 `*.md` 참조.
> 기준 경로(현 서버): `/data1/jyheo/workspace/VAU_RAG` (= 레포 루트, 이하 `$ROOT`). 새 서버에선 경로가 다를 수 있음(§9).

---

## 1. 프로젝트 목표 (현재 단계)
- **Long-video 보고서 자동 생성 프레임워크**: Video RAG(**WorldMM** 중심, **MERIT** 교체 가능)가 비디오 증거를 retrieve → **Deep-Reporter**(LangGraph)가 long-form 보고서를 생성. Video QA head를 **long-form generation**으로 대체.
- **1차 타깃**: Long Video Understanding QA 데이터셋(**Video-MME**). 감시/관제(CCTV, HolmesVAU)는 후속.
- **보고서 모듈 결정**: **Deep-Reporter 채택**(qraft 기각 — 근거: `$ROOT/claude_output/VideoRAG_ReportGen_analysis_v2.md`).

## 2. 레포 구성 (`$ROOT/`)
`WorldMM/`(VideoRAG 핵심), `MERIT/`(대체 VideoRAG), `Deep-Report/`(보고서 생성), `HolmesVAU/`·`AdaVideoRAG/`·`Vgent/`·`qraft/`(분석/후속용), `claude_output/`(분석·전략 문서).

## 3. WorldMM — 핵심 사실 (상세: `WorldMM/claude_output/WorldMM_analysis.md`)
- 논문: *WorldMM: Dynamic Multimodal Memory Agent for Long Video Reasoning* (CVPR 2026, arXiv:2512.02425). 로컬 백본 `Qwen/Qwen3-VL-8B-Instruct`.
- **2단계**: (A) 오프라인 메모리 구축(`preprocess/build_memory.py`) → (B) 온라인 추론(`src/worldmm/memory/memory.py`의 `WorldMemory`).
- **3종 메모리**:
  - **episodic**(`episodic/memory.py`): granularity별(10sec/30sec/3min/10min/1h) 캡션 → **HippoRAG** 그래프를 **index 시점에 캡션으로 재구축**(OpenIE 재실행) → 검색 = HippoRAG + **LLM multiscale_filter** 재랭크. ⚠️ preprocess가 만든 episodic triple은 **eval 검색에 안 쓰이고 semantic 추출 입력으로만** 소비됨.
  - **semantic**(`semantic/memory.py`): consolidated triple → **igraph(엔티티=정점)** + **Personalized PageRank**(HippoRAG 아님). 쿼리시 가장 가까운 timestamp 1개 snapshot만 인덱싱.
  - **visual**(`visual/memory.py`): VLM2Vec 30초 clip 임베딩 → 텍스트쿼리 유사도 또는 time-range → **프레임(PIL) 추출**.
- **LLM 2개**: `retriever_llm`(episodic OpenIE·필터) + `respond_llm`(reasoning+QA). **QA는 멀티모달**(visual 프레임을 이미지로 LLM에 투입) → respond_llm은 VL 모델 필수.
- **answer()** = 멀티라운드 에이전트(memory_reasoning으로 memory_type+search_query 스스로 생성). → **통합 시 이 answer 루프는 미사용**(§7).
- 임베딩: 텍스트 `Qwen/Qwen3-Embedding-4B`, 시각 `VLM2Vec/VLM2Vec-V2.0`.

## 4. ★WorldMM gpt→qwen 수정 + 50영상 메모리 구축 (직접 검증)
### 4.1 코드 수정 (git 미커밋 working-tree 변경 4개 파일)
`git status`로 확인된 수정 파일: `script/4_eval.sh`, `script/videomme/4_eval.sh`, `src/worldmm/llm/qwen3vl.py`, `src/worldmm/memory/episodic/multiscale.py`.
- **eval 스크립트**: 기본 모델을 `gpt-5-mini/gpt-5` → **`RET_MODEL="qwen3vl" RESP_MODEL="qwen3vl"`** 로 변경(로컬 백본 사용).
- **LLM 라우팅**(`llm/llm_wrapper.py` = **원본, 미수정**): `_detect_provider`가 모델명 `"gpt"`→OpenAI, `"qwen3"`→`Qwen3VLModel` 자동 선택. → 모델명만 qwen3vl로 주면 로컬로 동작.
- **`qwen3vl.py` 수정(검증됨)**: ① `import threading` + `self._gen_lock=threading.Lock()`(L94) + `with self._gen_lock`(L367)로 GPU generate 직렬화(동시호출 CUDA illegal memory access 해결). ② 구조화 출력 파서 강건화: 코드펜스 제거 + bare JSON list를 단일필드 스키마로 wrap(L533-535) + `json.JSONDecoder(strict=False).raw_decode`(L526).
- **`multiscale.py` 수정(검증됨)**: 영상별 모델 재로딩 OOM → **단일 LLMModel 공유** + `max_workers=1`.
> (앞 2개는 OpenAI 전제 코드를 로컬 qwen3vl에서 돌리기 위한 '최소 수정'. 커밋되지 않았으므로 새 서버 clone 시 재적용 필요 — 또는 이 working-tree째 복사.)

### 4.2 50영상 DB 구축 결과 (Video-MME Long, 모델 접미사 `qwen3vl-8b`)
- **메모리 저장 위치**: `WorldMM/claude_output/full/metadata/`
  - `episodic_memory/{video_id}/` → `openie_results_qwen3vl-8b.json`, `episodic_triple_results_qwen3vl-8b.json`
  - `semantic_memory/{video_id}/` → `semantic_extraction_results_qwen3vl-8b.json`, `semantic_consolidation_results_qwen3vl-8b.json`
  - `visual_memory/{video_id}/` → `visual_embeddings.pkl`
  - **각 타입 정확히 50개 영상**(전수 검증, done=50 / failed=0).
- **캡션 저장 위치**: `WorldMM/claude_output/full/caption/{video_id}/{10sec,30sec,3min,10min}.json` (50영상). ← episodic eval이 직접 로드.
- **오케스트레이션**: `WorldMM/claude_output/full/{process_one_video.sh, queue_worker.sh, full_status.sh}`, `video_list.json`(50), 마커 `done/`·`failed/`. 구축은 GPU 6·7 사용.
- **eval 입력 셋**: `WorldMM/data/Video-MME/videomme/test.json`.
- ⚠️ eval.py 기본 경로(`output/metadata/videomme`)에는 **없음**. 50영상 eval 시 `--metadata-dir claude_output/full/metadata --caption-dir claude_output/full/caption --retriever-model qwen3vl --respond-model qwen3vl` 지정 필요.

### 4.3 성능 현황 (상세: `WorldMM/claude_output/REPORT.md`, `HANDOFF.md`)
- **파일럿 eval = 8영상(가장 짧은 Long)/24문항**. 최종 **12/24 = 50.0%**(1차 9/24=37.5% → OOM 6문항 복구 후 50.0%; 정상 letter응답만 12/21=57.1%). **목표 WorldMM-8B Video-MME(L)=66.0%**.
- **50영상 eval 드라이버는 미작성**(DB만 구축 완료). GPU 메모리: eval는 2×qwen3vl-8b+임베딩 ≈45GB로 48GB에 빠듯 → OOM 주의.

## 5. MERIT — 핵심 사실 (상세: `$ROOT/claude_output/WorldMM_DeepReport_integration_design.md` §10)
- 논문: MERIT(Multi-key Episodic Retrieval + Inference-time Temporal expansion).
- **단일 멀티키 episodic 메모리**: clip(30초)당 4키(event/dialogue/object/sum) → **MaxSim**(쿼리 vs 활성키 최대) 검색. 검색 시 **LLM 호출 없음**(임베딩만) → WorldMM보다 가볍다.
- `CaptionEntry`가 WorldMM과 **거의 동일**(granularity만 없음). key 파일 = WorldMM 캡션 + 4키.
- **WorldMM과 실질 호환**: MERIT 실제 런타임 import 중 WorldMM venv에 **없는 것은 `opencv-python`(cv2) 하나뿐**. pyproject의 `torch2.6/tf4.57.3/openai2.8.1` ==핀은 "테스트 버전"일 뿐 → **`uv pip install --no-deps -e MERIT`** 로 WorldMM 스택 위에서 구동(§8 Docker).

## 6. Deep-Reporter — 핵심 사실 (상세: `Deep-Report/claude_output/Deep-Report_analysis.md`)
- 논문: *Deep-Reporter: Deep Research for Grounded Multimodal Long-Form Generation* (ACL 2026 Long, arXiv:2604.10741). **LangGraph StateGraph**.
- 그래프: `planner`(outline+섹션별 checklist 생성; `without_planner`면 주입 outline 사용) → **섹션마다** `query_generation`(LLM이 `text_queries`/`image_queries` 생성) → `search`(HTTP) → `filter`(옵션) → `section_writing` → `combine`.
- **외부 접합부 = `retriever_url` HTTP 하나**: `POST {query_list, type:text|image, topk}` → `{status, results:[...]}`. writer는 text의 `content`(없으면 `text`), image의 `caption`(없으면 `description`→'Image')+`img_path` 사용.
- **인용은 섹션-로컬** `[citation:txtN]`/`![](citation:imgN)` — `combine_node`가 **전역 치환하지 않음**(count만) → 통합 시 **후처리기 필수**.
- 작성 LLM = **OpenAI 호환 chat**(`ChatOpenAI`). `openai_base_url`만 바꾸면 로컬 vLLM↔OpenAI 전환(코드 수정 0). 기본 `primary_model=gpt-5-mini`(start.py).

## 7. 통합 설계 (상세: `$ROOT/claude_output/{VideoRAG_ReportGen_analysis_v2.md, WorldMM_DeepReport_integration_design.md})
- **구성**: `[A]` Video-RAG 검색서비스(신규; WorldMM/MERIT per-item retrieve를 `retriever_url` 계약으로 노출) → `[B]` Deep-Reporter(무수정) → `[C]` 인용·이미지 전역 grounding 후처리기(신규).
- **쿼리/검색 처리(코드 검증)**: Deep-Reporter가 자기 LLM으로 섹션별 쿼리 생성 → `[A]`가 **WorldMM/MERIT의 "순수 retrieve 프리미티브"에 직접 투입**. **WorldMM/MERIT의 agentic `answer()` 루프(스스로 쿼리생성+멀티라운드)는 미사용**(역할이 Deep-Reporter와 중복·충돌). text→episodic(+semantic), image→visual 매핑은 `[A]` 정책이 담당.
- **백엔드 추상화**: `EvidenceItem{uid,modality,content,start/end_time,video_path,score,source,img_path}` + `VideoRAGBackend` 프로토콜 → MERIT 교체 = 스위치+클래스 1개. 신규 구현물은 `report_framework/`(미착수).
- **검증된 개선점 6건**(인용 전역해소 후처리 필수, LLM 엔드포인트 분리, 이미지 캡션 필수, topk 병합 규칙, filter는 실제 img_path 파일 읽음, 증거공백 방지) — 전부 코드로 CONFIRMED(v2 §7).
- **트레이드오프(정직)**: (a) WorldMM episodic 검색은 쿼리당 조건부 LLM필터 비용, (b) WorldMM/MERIT의 멀티라운드 적응검색 상실.

## 8. Docker 통합 환경 (상세: `Deep-Report/claude_output/DOCKER_SETUP_REPORT.md`, `deepreporter_env_compat_checklist.md`)
- 위치: **`Deep-Report/claude_output/Docker/`** = `Makefile` + `docker/{base,user}.Dockerfile` + `envs/extras-integration.txt` + `check_port_used.py`. WorldMM/Docker 구조 미러, 전략 B(캐시 프리워밍 + 런타임 .venv).
- **단일 통합 venv**(= WorldMM/.venv, 세 repo 공유). 런타임 `intsetup`:
  `uv sync`(WorldMM) → `uv pip install -r extras-integration.txt`(langchain/langgraph/flask/opencv; openai 2.29→**2.54**) → `uv pip install --no-deps -e $MERIT_DIR`.
- 이미지 `worldmm-int:cu128-torch28-tf4576-ubuntu2204`, 컨테이너 `<user>_worldmm-int`, 포트 8817/8818. **기존 worldmm과 분리(동시가동)**.
- **색상 CLI 보장(실측)**: base image `/etc/skel/.bashrc`에 색상 블록 존재 + `useradd -m` 복사 + Makefile `-e TERM=xterm-256color` → worldmm과 동일하게 컬러 프롬프트(`ls/grep --color`). 흑백 아님.
- **엔드포인트**: 로컬 vLLM(OpenAI 호환) 기본 권장 + OpenAI 경로 보존(`OPENAI_API_KEY`/`OPENAI_BASE_URL` passthrough).
- 검증 상태: 정적·문법·상호참조 통과. **실제 `docker build` 미수행**. `--build-context`는 Docker 23+ 필요.

## 9. ★새 서버 이식 체크리스트 (Docker 디렉토리 복사 시)
1. **Docker 23+(BuildKit)** 필수(`--build-context`).
2. 빌드 컨텍스트 = WorldMM 루트 → 새 서버에도 **WorldMM repo + `.dockerignore`** 가 그 경로에 있어야 함(Docker 디렉토리 단독 복사로는 불충분).
3. 런타임 마운트에 **세 repo 모두** 존재(`{WORKSPACE}/VAU_RAG/{WorldMM,MERIT,Deep-Report}`).
4. 경로 하드코딩: `WORKSPACE=/data1/$(USER)/workspace`, 마운트 `/data`~`/data6`, `.claude`. 레이아웃 다르면 Makefile 변수 수정.
5. 빌드 시 인터넷(nvidia/cuda·uv·node·PyPI·npm). GPU A6000 sm_86 → `TORCH_CUDA_ARCH_LIST=8.6` 그대로.
6. **4.1의 WorldMM working-tree 수정 4개 파일**(qwen 전환/lock/파서/multiscale)이 새 clone에 반영됐는지 확인(미커밋).
7. **구축된 50영상 메모리/캡션**(`WorldMM/claude_output/full/{metadata,caption}`)을 쓰려면 함께 복사(용량 큼) 또는 재구축.

## 10. 미착수/다음 단계
- `report_framework/` 실구현: `[A]` 검색서비스(WorldMMBackend 먼저) · 프레임 추출 유틸(decord) · `[C]` grounding 후처리 · 관제/보고 outline·checklist · PoC(1영상·filter off).
- WorldMM 50영상 eval 드라이버(미작성).
- 로컬 qwen3 작성 LLM = **별도 vLLM 컨테이너**로 서빙(torch 핀 충돌 회피).
- langgraph 1.x `StateGraph(config_schema=)` 런타임 확정(빌드 후 import/compile 테스트).

## 11. 문서 인덱스 (현행/권위 = ✅)
- ✅ `WorldMM/claude_output/WorldMM_analysis.md` — WorldMM 구현 상세.
- ✅ `Deep-Report/claude_output/Deep-Report_analysis.md` — Deep-Reporter 상세.
- ✅ `$ROOT/claude_output/VideoRAG_ReportGen_analysis_v2.md` — VideoRAG×보고서 독립분석 + 개선점 6건 검증.
- ✅ `$ROOT/claude_output/WorldMM_DeepReport_integration_design.md` — 통합 설계 + MERIT 분석(§10) + 백엔드 추상화(§11).
- ✅ `Deep-Report/claude_output/DOCKER_SETUP_REPORT.md` + `deepreporter_env_compat_checklist.md` — Docker/의존성.
- ✅ `WorldMM/claude_output/REPORT.md`(파일럿 성능) · `HANDOFF.md`(WorldMM 파일럿 핸드오프, WorldMM 범위 한정).
- ⚠️ 구버전: `$ROOT/claude_output/VideoRAG_ReportGen_analysis.md`(v1) → v2로 대체됨.
