# WorldMM 구현 분석 — 디렉토리·모듈·데이터 흐름 (코드 정독 기반, 전면 개정판)

> 목적: WorldMM의 전체 구조/핵심 모듈/연결/데이터 흐름을 **정확히(사실 기반)** 정리. 기존 분석의 오류를 바로잡음.
> **근거**: `src/worldmm/**`, `preprocess/**`, `eval/eval.py` 직접 정독 + 자체 50영상 DB 구축 경험. 참고: `claude_output/REPORT.md`, `claude_output/HANDOFF.md`. 경로=`/data1/USER/workspace/VideoRAG/WorldMM`.
> 표기: 파일:라인은 정독 시점 기준. 추측은 넣지 않음.

---

## 0. WorldMM이란 (사실)
- 논문: *WorldMM: Dynamic Multimodal Memory Agent for Long Video Reasoning* (CVPR 2026). 로컬 구현 백본 = `Qwen/Qwen3-VL-8B-Instruct`.
- **긴 비디오**를 **3종 멀티모달 메모리**(episodic/semantic/visual)로 구축하고, **에이전트가 다중 라운드로 메모리를 검색**해 질문에 답하는 Video-QA 시스템.
- **2단계 구성**: (A) **오프라인 메모리 구축**(preprocess, `build_memory.py`) → (B) **온라인 추론**(eval, `WorldMemory`)로 index→검색→QA.

## 1. 디렉토리 구조 (핵심)
```
WorldMM/
├── preprocess/                      # (A) 오프라인 메모리 구축
│   ├── build_memory.py              # 오케스트레이터(episodic/semantic/visual 단계)
│   ├── episodic_memory/
│   │   ├── generate_fine_caption.py # 10초 세그먼트 캡션(qwen3vl)
│   │   └── extract_episodic_triples.py # OpenIE(NER+triple) → openie/triple json
│   ├── semantic_memory/
│   │   ├── extract_semantic_triples.py   # episodic triple → semantic triple
│   │   └── consolidate_semantic_memory.py# 증분 consolidation
│   └── visual_memory/extract_visual_features.py # VLM2Vec clip 임베딩 pkl
├── src/worldmm/                     # 라이브러리
│   ├── memory/
│   │   ├── memory.py                # WorldMemory (오케스트레이터) ★
│   │   ├── episodic/{memory.py, multiscale.py, gen_multiscale.py, openie.py, utils.py}
│   │   ├── semantic/{memory.py, semantic_extraction.py, semantic_consolidation.py, utils.py}
│   │   ├── visual/memory.py
│   │   └── utils.py                 # QAResult, ReasoningOutput, RetrievedItem 등
│   ├── llm/{llm_wrapper.py(LLMModel), qwen3vl.py, openai_gpt.py, prompt_template_manager.py, templates/}
│   └── embedding/{embedding_wrapper.py(EmbeddingModel), qwen3_embedding.py, VLM2Vec/, vlm2vecv2.py}
├── eval/{eval.py(Video-MME), eval_egolife.py}
├── script/{1_setup,2_preprocess,3_build_memory,4_eval}.sh + script/videomme/*
└── (HippoRAG는 외부 패키지 `from hipporag import HippoRAG` — episodic이 사용)
```

## 2. 실행 스택 (REPORT/HANDOFF + 환경 확인)
Python 3.13 / torch 2.8.0+cu128 / transformers 4.57.6 / flash-attn 2.8.3 / hipporag 2.0.0a4 / igraph / decord. 백본 qwen3vl-8b, 텍스트 임베딩 `Qwen/Qwen3-Embedding-4B`, 시각 임베딩 `VLM2Vec/VLM2Vec-V2.0`.

---

## 3. (A) 오프라인 메모리 구축 파이프라인 (`preprocess/build_memory.py`)
`discover_videos`는 caption-dir에서 `{vid}/10sec.json`이 있는 영상을 처리. 단계(`--step episodic|semantic|visual|all`):

1. **caption (전제)**: `generate_fine_caption.py`가 10초 단위 프레임 캡션 → `caption/{vid}/10sec.json`. `multiscale`로 30sec/3min/10min.json 요약 생성. 각 caption 항목 = `{text, start_time, end_time, date, video_path}`.
2. **episodic** (`run_episodic` → `extract_episodic_triples.run_episodic_triples(10sec.json)`): OpenIE(NER+triple) 실행 → `metadata/episodic_memory/{vid}/openie_results_{model}.json`, `episodic_triple_results_{model}.json`. (이미 있으면 skip)
3. **semantic** (`run_semantic`): **입력 = `10sec.json` + 위 `openie_results_{model}.json`**(episodic 산출물!). `run_semantic_extraction`(캡션을 period로 묶고 OpenIE `triple_results`로 semantic triple 추출) → `semantic_extraction_results_{model}.json` → `run_semantic_consolidation`(증분 통합) → `semantic_consolidation_results_{model}.json`. **→ semantic은 episodic OpenIE 출력에 의존**(build_memory.py:87-89: openie 없으면 semantic skip).
4. **visual** (`run_visual`→`extract_visual_features`): VLM2Vec로 30초 clip 임베딩 → `metadata/visual_memory/{vid}/visual_embeddings.pkl`. (멀티 GPU 워커 split 지원; ⚠️ `--gpu` 토큰이 자식 `CUDA_VISIBLE_DEVICES`를 재설정 → HANDOFF §7.1 GPU-0 함정)

산출물 트리: `metadata/{episodic_memory,semantic_memory,visual_memory}/{vid}/...`, 캡션 `caption/{vid}/{10sec,30sec,3min,10min}.json`.

---

## 4. (B) 온라인 추론 — `WorldMemory` (`src/worldmm/memory/memory.py`, 646줄)
### 4.1 구성
- 서브시스템 3개: `EpisodicMemory`, `SemanticMemory`, `VisualMemory`.
- **LLM 2개**: `retriever_llm_model`(episodic OpenIE·multiscale 필터용) + `respond_llm_model`(추론 에이전트·QA용). eval에선 둘 다 qwen3vl-8b(응답측은 `fps=1`).
- 임베딩 1개(`EmbeddingModel`, 모든 메모리 공유). top_k 기본 episodic 3 / semantic 10 / visual 3 (`set_retrieval_top_k`).

### 4.2 적재(load) — eval.py 기준
영상마다: `load_episodic_captions(caption_files={g: caption/{vid}/g.json})`(4 granularity), `load_semantic_triples(semantic_consolidation_results_{model}.json)`, `load_visual_clips(embeddings_path=visual_embeddings.pkl, clips_data=10sec.json)`.

### 4.3 index(until_time) — 시간 경계까지 인덱싱
- **episodic**: granularity별 `end_time<=until_time` 캡션 텍스트 → **`hipporag.update(docs=caption_texts)`** (HippoRAG가 내부에서 OpenIE+그래프 구축; `episodic_cache_root/{granularity}`에 저장). **⇒ eval의 episodic 검색 그래프는 "캡션으로부터 index 시점에 새로 구축"**(preprocess의 episodic triple을 쓰지 않음).
- **semantic**: `until_time` 이하 **가장 가까운 timestamp 1개**의 consolidated triples로 **igraph(엔티티=정점, triple=간선) + triple 임베딩** 구축.
- **visual**: `end_time<=until_time` clip의 사전계산 임베딩 스택.
- Video-MME: `QUERY_TIME=123595999`(영상 끝) → 사실상 전체 인덱싱.

### 4.4 answer(query, choices, until_time) — 멀티라운드 에이전트
루프(`max_rounds=5`, `max_errors=5`): `memory_reasoning` 프롬프트로 respond_llm이 JSON `{decision: search|answer, selected_memory:{memory_type, search_query}, reason}` 생성 → `search`면 해당 메모리 검색, 누적(`retrieved_items`, `round_history`); `answer`면 종료. 종료 후 `qa`(또는 `qa_egolife`) 프롬프트로 **멀티모달 QA**(텍스트 context + **visual 프레임 이미지**를 함께 LLM에 전달) → 최종 답. 반환 `QAResult{question, answer, retrieved_items, round_history[{round_num,decision,memory_type,search_query,retrieved_content}], num_rounds}`.
- ⚠️ 실패 시 answer="Unable to generate answer".

---

## 5. 3종 메모리 상세 (사실)
### 5.1 EpisodicMemory (`episodic/memory.py`, HippoRAG 기반)
- `CaptionEntry{id, text, start_time, end_time, date, granularity, video_path}`; `to_display_str()`="[DAYd HH:MM:SS - ...]\n{text}". GRANULARITY_ORDER=["10sec","30sec","3min","10min","1h"].
- **granularity별 HippoRAG 인스턴스**(save_dir=`{cache}/{granularity}`, 동일 llm/embedding 공유).
- `retrieve(query, top_k_per_granularity, final_top_k, as_context)`: granularity별 HippoRAG.retrieve로 후보(CaptionEntry, score) 수집 → **LLM `multiscale_filter`**로 final_top_k 선별·랭킹 → CaptionEntry 리스트(또는 display str). 기본 top_k_per_granularity={30sec:10,3min:5,10min:5,1h:3}.
- `text_to_entry`로 HippoRAG가 돌려준 doc 텍스트 → CaptionEntry 역참조.

### 5.2 SemanticMemory (`semantic/memory.py`, PPR 기반, HippoRAG 아님)
- `SemanticTripleEntry{id, subject, predicate, object, timestamp}`; `to_display_str()`="(s, p, o)". 적재 포맷 `{timestamp: {consolidated_semantic_triples:[[s,p,o]...]}}`.
- `index`: `until_time` 이하 **가장 가까운 timestamp 1개**의 triples → **igraph**(엔티티 정점/triple 간선) + 임베딩(encode_text).
- `retrieve(query, top_k)`: **Personalized PageRank** — (1) 쿼리 임베딩 cosine로 유사 triple top-k → (2) 그 엔티티로 PPR personalization reset → (3) `graph.personalized_pagerank(damping=0.85, prpack)` → (4) triple 점수=subj+obj PPR 합 → (5) top-k. (igraph로 직접 구현; HippoRAG 미사용.)

### 5.3 VisualMemory (`visual/memory.py`, VLM2Vec 임베딩)
- `VideoClipEntry{id, video_path, start_time, end_time, date, clip_start_sec, clip_end_sec, embedding}`; `FrameEntry{video_path, frame_index, timestamp_sec, frame}`.
- 사전계산 clip 임베딩(pkl)을 `embedding_lookup`으로 적재.
- `retrieve(query, fps=1.0, max_frames=64, as_context=True)`: **두 모드** — (a) **time-range 쿼리**("DAY X HH:MM:SS - ...")면 해당 구간 비디오에서 1fps 프레임 추출(최대 64); (b) **텍스트 쿼리**면 VLM2Vec 텍스트 인코딩→clip 임베딩 cosine top-k 선택 후 프레임 추출. as_context=True → `{display_time: [PIL.Image,...]}`(프레임 이미지).

---

## 6. LLM / 임베딩 래퍼
- **LLMModel**(`llm/llm_wrapper.py`): model_name에 "gpt"→OpenAI, "qwen3"→Qwen3VLModel 자동 라우팅. `generate(prompt, text_format=…)` 통일 인터페이스(구조화 출력은 pydantic). (우리가 적용한 수정: 동시호출 락, 구조화 파서 강건화 — HANDOFF §2.)
- **EmbeddingModel**(`embedding/embedding_wrapper.py`): 텍스트=`Qwen/Qwen3-Embedding-4B`(`encode_text`), 시각=`VLM2Vec/VLM2Vec-V2.0`(`encode_image`/`encode_vis_query`/`encode_video`), lazy 로드.
- **HippoRAG**(외부 패키지): episodic이 granularity별로 사용(동일 LLMModel+EmbeddingModel 주입). OpenIE·엔티티/팩트 그래프·PPR 검색을 내부 수행.

---

## 7. ★핵심 데이터 흐름·주의 (정확히 — 흔한 오해 교정)
1. **episodic triple(preprocess)의 용도**: eval의 episodic **검색에는 쓰이지 않음**. 그것은 **semantic extraction의 입력**으로만 소비됨(§3-3). eval의 episodic 검색은 **캡션으로 HippoRAG 그래프를 index 시점에 재구축**(§4.3). → "episodic triple을 로드해 검색한다"는 오해 금지.
2. **semantic은 HippoRAG가 아니라 igraph+PPR 직접 구현**(§5.2). "HippoRAG로 semantic 검색"은 틀림.
3. **semantic은 쿼리시 1개 timestamp snapshot만 인덱싱**(가장 최근 consolidated ≤ until_time). 전체 누적이 아님.
4. **QA는 멀티모달**: visual 검색 결과(프레임 PIL 이미지)가 QA LLM에 **이미지로** 투입됨(episodic/semantic은 텍스트). → respond_llm은 VL 모델이어야 함(qwen3vl).
5. **메모리는 시간(until_time) 조건부**: EgoLife(day-scale) 설계. Video-MME는 QUERY_TIME=영상끝으로 전체 인덱싱.
6. **검색 증거 노출 지점**(통합용): `QAResult.round_history[*].retrieved_content`(텍스트는 문자열, visual은 "[N images from M clips]" 요약). **per-item 엔트리가 필요하면** 하위 `episodic_memory.retrieve(as_context=False)`→List[CaptionEntry], `semantic_memory.retrieve(as_context=False)`→List[SemanticTripleEntry], `visual_memory.retrieve(as_context=True)`→{time:[PIL]}를 직접 호출.
7. **2 LLM 역할 분리**: retriever_llm=episodic OpenIE/multiscale 필터, respond_llm=reasoning+QA. 혼동 금지.
8. **GPU-0 함정**(HANDOFF §7.1): visual 워커가 `--gpu` 토큰으로 자식 `CUDA_VISIBLE_DEVICES` 재설정 → `--gpu 0`이면 물리 GPU0. build 시 `env -u CUDA_VISIBLE_DEVICES ... --gpu $GPU` 필요.

## 8. 통합(보고서 프레임워크) 관점 요약
- **Video RAG 검색 seam** = `WorldMemory` 하위 메모리의 `retrieve(...)`(per-item) 또는 `answer()`의 round_history. Deep-Report 어댑터는 이들을 `retrieved_texts`(episodic 캡션 `to_display_str`, semantic `(s,p,o)`) / `retrieved_images`(visual 프레임→png + 캡션)로 매핑(별도 전략 문서 참조).
- **QA head 분기**: 보고서 생성은 `answer()`의 letter 대신, 검색 라운드로 모은 evidence를 generation으로 전달하는 경로가 필요.

## 9. 현 구축 상태(참고, HANDOFF)
- Video-MME Long 50영상 DB 구축 완료(episodic/semantic/visual 각 50, 전수 검증). 재현 목표 WorldMM-8B Video-MME(L) ≈ 66.0%(파일럿 8영상 50.0%). eval(50영상) 드라이버는 미작성.
L