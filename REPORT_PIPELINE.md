# 보고서 생성 파이프라인 (Video-RAG × Deep-Reporter)

- 작성: 2026-10-22. 최종 갱신: 2026-10-25 (대기 실행 결과, GPU 4–7 허용, 검증 영상의 10min 캡션 잘림, C-1–C-5 결과)
- 기준 코드: `report_framework/` (`run_report.py`, `videorag_retriever_service.py`, `local_llm_server.py`, `domain_templates.py`, `grounding_postprocessor.py`, `report_translator.py`, `prebuild_episodic_index.py`, `config.yaml`)
- 이 문서는 **보고서 1건이 어떻게 만들어지는지**를 단계별로 설명한다. 설계 배경·결정·검증 이력·인수인계는 `DESIGN_AND_STATUS.md`, 문제와 개선 이력은 `REPORT_ISSUES_AND_FIXES.md`에 있다.
- 별도 표시가 없으면 기본 설정(4개 단위 episodic, L1)을 기준으로 설명한다.
- 예시와 시간은 실제 실행 2건에서 가져왔다. 두 실행 모두 영상 `-QuCz7kxBr8`, Qwen3-VL-8B, **10sec 단위 캐시만** 사용했다.

  | | 보고서 A: 스모크 | 보고서 B: `run_report.py` 첫 실행 |
  |---|---|---|
  | 섹션 | 5 | 6 (결론 포함) |
  | 적용된 단계 | ③④(템플릿 적용, 생성)만 실제 실행. ⑤⑥은 나중에 CPU로 따로 적용, ⑦⑧ 없음 | ①–⑨ 전체 |
  | 이후 추가돼 실제 모델로는 아직 돌려 보지 않은 것 | — | 규칙 6, C0, absence 처리, 이미지 시간 기록, 번역 한자 감지·이름 보호 |

## 목차
1. 한눈에 보기 · 2. 사전 준비 · 3. 단계별 흐름(①–⑨) · 4. LLM 호출과 시간 · 5. 주요 설정 · 6. 실패 지점과 처리 · 7. 현재 한계 · 8. 확장 지점

---

## 1. 한눈에 보기

```
[오프라인, 영상별 1회]  WorldMM 메모리 (구축 완료: 50영상)          episodic HippoRAG 캐시 (prebuild A안 + 분할 OpenIE 구현, 완성 캐시 없음)
  캡션 10sec/30sec/3min/10min · semantic triple · visual 임베딩      cache/episodic/<vid>/episodic_memory/<g>/

[실행 중인 서비스 2개, GPU]
  (L) local_llm_server.py  :8010  OpenAI 호환 /v1/chat/completions, Qwen3-VL-8B   (또는 vLLM, 같은 주소)
  (R) videorag_retriever_service.py :8020  POST /videos/<vid>/search, 영상 1개씩 메모리 로드

[보고서 1건]  python run_report.py --config config.yaml --video-id=<vid> --query "<요청>"   (모델 로드 없음, CPU)
  ① 사전 확인 → ② LLM 라우팅 설정 → ③ 영상 개요 + 템플릿 적용 (섹션 수 상한, 결론 규칙, 반복 금지 규칙 6)
     + 앞 섹션 맥락 교체 (C0: 앞 섹션에서 실제로 쓴 문장 전달)
  → ④ Deep-Reporter 그래프:  planner → [섹션마다: query 생성 → 검색(R) → 작성] → combine
  → ⑤ 후처리 (인용 → 참조·그림)  → ⑥ 규칙 기반 근거 검사 → ⑦ 사후 검증
  → ⑧ 한국어 번역 (검증 통과 시, 섹션 단위, LLM) → ⑨ 산출물
```

| 구성요소 | 파일 | 역할 | 실행 위치 |
|---|---|---|---|
| WorldMM 메모리 | `WorldMM/claude_output/full/{caption,metadata}` | 영상의 캡션, semantic triple, visual 임베딩 (기존 산출물) | 디스크 |
| 사전 인덱싱 | `prebuild_episodic_index.py`, `run_prebuild_http.sh`, `tests/gpu_3videos.py` | 캡션 → granularity별 HippoRAG 그래프 캐시. OpenIE LLM은 LLM 서버를 HTTP로 호출(결정 1 = A안). 1,100토큰 초과 청크는 조각으로 나눠 OpenIE | GPU, 1회 (LLM 서버 1개 이상 + 인덱서 1개, 프로세스마다 메모리 상한) |
| LLM 서버 (L) | `local_llm_server.py` | planner, query, writer, L1 필터, 번역(그리고 사전 인덱싱 OpenIE)이 쓰는 LLM | GPU 1장 (+약 18GB) |
| 검색 서비스 (R) | `videorag_retriever_service.py` | Deep-Reporter 검색 요청 → WorldMM 메모리 검색 결과 | GPU 1장 (+약 14GB) |
| 템플릿 | `domain_templates.py` | Deep-Reporter 프롬프트 3개와 앞 섹션 맥락 함수(`_update_context`, C0)를 비디오용으로 범위 한정 교체 | `run_report` 프로세스 안 |
| 후처리기 | `grounding_postprocessor.py` | 인용 치환, 그림, References, 규칙 기반 근거 검사, 이미지-텍스트 시간 기록 | `run_report` 프로세스 안 |
| 번역기 | `report_translator.py` | 영어 보고서 → 한국어 `report_ko.md` (근거 표기 보호, 실패 시 원문 유지) | `run_report` 프로세스 안 (LLM은 (L) 호출) |
| 진입점 | `run_report.py` | 위 전부를 순서대로 실행하고 검증·저장 | CPU |

---

## 2. 사전 준비 (오프라인)

1. **WorldMM 메모리** (구축 완료, 50영상): `caption/<vid>/{10sec,30sec,3min,10min}.json`, `metadata/semantic_memory/<vid>/semantic_consolidation_results_qwen3vl-8b.json`, `metadata/visual_memory/<vid>/visual_embeddings.pkl`.
2. **episodic HippoRAG 캐시** (`prebuild_episodic_index.py`)
   - 캡션마다 OpenIE(LLM)로 그래프를 만들어 `cache/episodic/<vid>/episodic_memory/<g>/`에 저장한다.
   - 10sec는 전처리 OpenIE 결과를 시드로 넣어 LLM 호출을 줄인다. 50영상 계획은 빈 캐시 기준 13,424회다(긴 청크 분할 포함. 분할 전 코드로는 12,818회).
   - **긴 청크 분할 OpenIE** (2026-10-22): 1,100토큰을 넘는 청크(주로 10min, 50영상에 150개)는 빈 줄 문단 단위의 700토큰 이하 조각으로 나눠 조각마다 NER·triple을 뽑고, 청크 단위로 합쳐 캐시에 넣는다. 10min 청크의 OpenIE 출력이 2,048토큰 상한을 넘어 JSON이 잘리고 청크당 최대 15회 재시도하던 문제 때문이다. HTTP 경로에서는 파싱 실패 응답의 완성된 항목을 살리고(구제), 같은 (주어, 술어)가 연속 15개를 넘는 폭주 triple을 잘라낸다. 상세는 `REPORT_ISSUES_AND_FIXES.md` I23·I24.
   - **결정 1 = A안**: `./run_prebuild_http.sh <LLM_GPUS> <INDEXER_GPU> [--videos=<vid>]`
     - LLM 서버(`local_llm_server.py`)를 GPU마다 1개씩 띄운다.
     - 인덱서는 임베딩 모델만 올리고 OpenIE를 서버들에 HTTP로 순서대로 돌아가며 보낸다.
     - 요청은 in-process 호출과 같은 메시지, `max_tokens=2048`, 샘플링 인자 없음, 같은 JSON 파서, 같은 재시도 깊이를 쓴다.
     - GPU 프로세스에는 기본으로 메모리 상한을 건다(LLM 서버 19,000 MiB, 인덱서 `--gpu-mem-cap-mib`). 2026-10-25 C 단계는 사용자 지시로 상한 없이 실행했다(`tests/gpu_3videos.py --llm-cap-mib 0 --aux-cap-mib 0`).
     - GPU를 다른 사용자와 같이 쓸 때는 `tests/gpu_3videos.py`(실행 전 여유 확인, 실행 중 감시·자동 중단)를 쓴다.
   - **현재 상태** (`DESIGN_AND_STATUS.md` §9.5–9.15)
     - 10/22에는 분할 적용 전 영상 1개만 완주했고, 분할 적용 후 실행은 GPU 공유 문제로 중단·미시작이었다(§9.8·§9.9).
     - **2026-10-25 C-1에서 검증 영상 3개(`-QuCz7kxBr8`, `0RxMZBLeqRI`, `54k2g9ddy4M`)의 4개 단위 캐시를 완성했다**(GPU 4–7, LLM 서버 7개, 1,643초, 호출 430회 = 계획, 실패 0). 나머지 47개 영상은 캐시가 없다.
     - 이 캐시로 검색(C-3)과 보고서 생성(C-4 3건, C-5 8건)을 했다. 서비스 여러 개가 같은 영상을 동시에 불러오면 실패하므로(I29) 영상별로 차례로 불러온다. 보고서 품질 문제는 `REPORT_ISSUES_AND_FIXES.md` P9·P19·P15.
   - 다시 실행하면 저장된 OpenIE 결과는 재사용되고, 완료한 영상은 `_done` 표식으로 건너뛴다.
   - 검색 서비스는 캐시가 불완전한 영상을 거부한다(409). HippoRAG의 OpenIE가 LLM 오류를 삼키고 빈 결과를 캐시에 저장하는 것을 막기 위해서다. 다만 재시도 후에도 파싱에 실패한 청크는 빈 triple로 저장되고 "완료"로 간주된다(HippoRAG·WorldMM 동작, 시험 실행 10sec에서 2건).

---

## 3. 단계별 흐름

### ① 설정 확인과 사전 확인 (`run_report.run`, `run_report.preflight`)
- 설정 확인: LLM 백엔드와 모델명(local이면 이름에 `qwen`, openai면 `gpt`와 `OPENAI_API_KEY`), `report.max_sections`(정수 3–15), `report.previous_sections_context`(`written`/`deep_reporter`). 잘못되면 exit 2.
- 영상 개요 파일(`<caption_dir>/<vid>/10min.json`)이 있는지 확인한다.
- LLM 서버 `GET /health` (local 백엔드일 때).
- 검색 서비스 `GET /health`와 **`POST /videos/<vid>/load`** (메모리 로드, 캐시가 불완전하면 409).
- 템플릿 계약 검사(`domain_templates.resolve_targets`).
- 하나라도 실패하면 **exit 2**로 즉시 중단하고, 보고서 생성은 시작하지 않는다.

### ② LLM 라우팅 설정
- Deep-Reporter는 LLM 키와 URL을 **환경변수로만** 받는다(설정 dict의 키·URL은 `BaseConfig.from_dict`가 버린다).
- **local** (기본): `QWEN_BASE_URL=http://127.0.0.1:8010/v1`, `QWEN_API_KEY=EMPTY`, 모델 `qwen3vl-8b`.
  - 모델명에 `qwen`이 있어야 QWEN 설정으로 라우팅된다.
  - URL이 127.0.0.1이면 Deep-Reporter가 `chat_template_kwargs`(thinking off)를 붙이고, 서버는 이를 무시한다.
- **openai**: `OPENAI_API_KEY`(필수), `OPENAI_BASE_URL`(선택), 모델 `gpt-5-mini` (`gpt`가 있어야 OPENAI 설정으로 라우팅).
- `create_openai_api({primary_model, log_dir})` 후 **실제로 라우팅된 base URL이 기대값과 같은지 확인**한다. 다르면 exit 2.

### ③ 영상 개요와 템플릿 적용
- 개요: 10min 캡션들을 `[HH:MM:SS-HH:MM:SS] 캡션` 블록으로 이어 붙인다. 예시 영상은 4개 블록이고, planner 프롬프트는 A 5,050토큰, B 5,213토큰이었다.
  - 주의: 50영상 중 20영상의 10min 캡션 32개가 전처리에서 2,048토큰에 잘려 문장 중간에서 끝난다. 그 영상들은 개요에 잘린 뒷부분이 빠진다(재생성은 보류, `REPORT_ISSUES_AND_FIXES.md` I22). 예시 영상 `-QuCz7kxBr8`은 해당하지 않는다(10min 최대 1,733토큰). 검증 영상 3개 중에서는 `0RxMZBLeqRI`의 0–10분·10–20분 캡션이 해당한다(2026-10-25 확인).
- `with apply_templates(build_templates("videomme", 개요, max_sections)):` 블록 안에서만 Deep-Reporter의 planner, query, writer 프롬프트가 비디오용으로 바뀐다.
  - `max_sections`(`report.max_sections`, 기본 6)는 결론을 포함한 전체 섹션 수 상한이다.
  - 허용 범위는 3–15이고, 범위를 벗어나면 생성 전에 exit 2로 끝난다.
  - 상한이 필요한 이유: Deep-Reporter `recursion_limit=50` 때문에 **16섹션부터는 그래프가 오류로 멈추고 보고서 전체가 사라진다**(가짜 LLM으로 실측).
  - 실행 전에 placeholder, 출력 형식 마커(결론 규칙, 반복 금지 규칙 6 포함), `.format()` 시험 실행을 검사한다.
  - 블록이 끝나면 원래 템플릿으로 복원한다.
- **C0 (결정 4)**: `report.previous_sections_context: written`(기본)이면 같은 블록에서 `apply_written_context()`도 적용한다.
  - Deep-Reporter `section_writing_node`가 다음 섹션용 맥락을 만들 때 쓰는 `_update_context`를 실행 중에만 교체한다(④-2(c)).
  - 실행 전에 노드가 이 함수를 호출하는지, 시그니처, 반환 형식을 검사한다. 끝나면 복원한다.
  - `deep_reporter`로 두면 원래 동작이다(비교 실험용). 다른 값이면 exit 2.

### ④ Deep-Reporter 그래프 (`generate_article`, `with_planner`, `enable_filter=False`)

**④-1 planner (LLM 1회)**
- 입력: 사용자 요청(query), 추가 요구사항(checklist), 영상 개요.
- 지시: 영상에 실제로 있는 내용으로 **총 3–N개**(N = `max_sections`, 결론 포함) 섹션을 만들고, 섹션 설명에 시간 범위를 넣고, checklist는 관찰 가능한 항목으로 쓴다.
- **결론 섹션 (결정 5)**: 마지막 섹션은 앞에서 다룬 결과를 요약하는 짧은 결론이다. 설명은 정확히 `Conclusion:`으로 시작하고, 새 주제를 넣지 않으며, checklist는 2–3개다. 다른 섹션은 `Conclusion:`으로 시작하지 않는다. 프롬프트 지시이므로, 지켜졌는지는 ⑦에서 경고로 확인한다.
- 출력: `{"outline": [{"section_description", "sectional_checklist"}, ...]}` JSON.
  - 파싱이 실패하면 Deep-Reporter가 **조용히 섹션 1개(설명 = query)로 대체**한다 → ⑦에서 오류로 잡는다.
- 예: 요청 "Write a report describing what happens in this video: who takes part, what is tested, and how the tests turn out."
  - A(결론 규칙 전) → 5개 섹션(참가자와 첫 가젯 / 드리블 고글·드리블 스틱 / 장애물 슛 / Straight Shooter Strap / Flick Glove), 51.3초.
  - B → 6개 섹션(참가자 / SPORTS DRIBBLE SPECS·SKLZ Dribble Stick / 슈팅 챌린지 / "FIRST MADE SHOT…" 게임 / NEVER ENDING DEFENDER·마무리 / `Conclusion:`), 36.8초.

**④-2 섹션마다 반복** (섹션 수만큼, 섹션당 그래프 3단계)

(a) **query 생성** (LLM 1회, A 5.1–6.4초 / B 3.0–4.1초)
- text query는 사건·인물·대사·물체 키워드 2–3개, image query는 장면 생김새를 묘사하는 문장 1–2개.
- 파싱이 실패하면 섹션 설명이 그대로 검색어가 된다 → ⑦에서 경고.
- 예(A): text `"man in white hoodie demonstrates Straight Shooter Strap on elbow"`, image `"a man in a white hoodie wearing an elbow strap while shooting a basketball on an outdoor court"`.

(b) **검색** (Deep-Reporter `search_node` → 검색 서비스 HTTP 2회, text와 image 사이 2초 대기)
- 요청: `POST /videos/<vid>/search {"query_list": [...], "type": "text"|"image", "topk": 20|10}`. 응답 시간 제한은 600초이고, 실패하면 근거 0건으로 계속 진행된다(⑦에서 오류로 잡음).
- **text 경로** (기본 L1)
  1. 쿼리마다, granularity마다 HippoRAG 그래프 검색으로 후보를 모은다(LLM 없음).
     - 후보 수: 10sec 3 / 30sec 3 / 3min 2 / 10min 1.
     - 과정: 쿼리 임베딩 → fact 점수 → 상위 5 fact → PPR.
     - 원본 `HippoRAG.retrieve`에서 DSPy LLM fact 필터만 뺀 것이다.
  2. 모든 (쿼리, 단위) 순위 목록을 RRF(k=60)로 병합하고 id로 중복을 제거한다.
  3. **L1 필터**: 병합 후보 전체(질문은 섹션 쿼리들을 `"; "`로 이은 문자열)를 WorldMM `multiscale_filter` 프롬프트로 LLM에 1회 보내 8개를 고른다. 입력 A 2,577–3,205토큰·4.6–5.4초, B 2,275–3,474토큰·3.3–4.1초. 후보가 8개 이하이면 건너뛴다.
     - LLM 호출이 실패하면 RRF 순위로 채우고 `meta.episodic_filter="fallback_rrf(llm_failed)"`로 표시한다. 호출은 성공했지만 응답 형식이 깨져 WorldMM이 RRF로 채운 경우에는 `llm`으로 표시된다(알려진 한계).
  4. semantic: 쿼리마다 PPR 검색 → RRF → 4개.
  5. 개수: episodic `min(8, topk)`, semantic `min(4, 남은 topk)`.
- 모드: L0(필터 없음, LLM 0회) / L1(요청당 1회, 기본) / full(WorldMM 원본 검색, 쿼리당 최대 5회). full은 쿼리별 결과가 겹쳐도 근거가 모자라지 않게 쿼리당 개수를 `max(3, ceil(8/쿼리 수))`로 둔다.
- **image 경로**: 쿼리마다 VLM2Vec 텍스트→비디오 유사도 상위 3개 클립 → RRF → 최대 4개 → 각 클립 구간 **중앙 프레임**을 jpg로 저장(캐시됨) → 같은 시작 시각의 10sec 캡션을 붙인다.
- 응답 항목 예 (Deep-Reporter는 `content`/`caption`만 프롬프트에 쓰고, 나머지 필드는 결과에 그대로 보존된다)
  ```json
  {"type": "text", "source": "worldmm-episodic", "uid": "-QuCz7kxBr8:episodic:10sec_<idx>",
   "content": "[00:00:40-00:00:50 | episodic 10sec] A person puts on a pair of sports goggles labeled \"SPORTS DRIBBLE SPECS\" ...",
   "granularity": "10sec", "start_time": "00004000", "end_time": "00005000", "start_sec": 40.0, "end_sec": 50.0,
   "score": 0.0328, "score_type": "rrf(order=llm_filter)", "rank": 1, "video_path": "/abs/.../-QuCz7kxBr8.mp4"}
  {"type": "text", "source": "worldmm-semantic", "content": "[video-level knowledge | semantic] (player, can dribble, basketball)",
   "start_time": null, "time_grounded": false, ...}
  {"type": "image", "source": "worldmm-visual", "img_path": ".../frames/-QuCz7kxBr8/00205000.jpg", "frame_sec": 1255.0,
   "caption": "[00:20:50-00:21:00 | video frame at 1255.0s] On an outdoor basketball court ...", ...}
  ```
  (`score` 값은 형식을 보여주기 위한 예시다.)

(c) **섹션 작성** (LLM 1회, A 35.7–66.5초 / B 16.1–34.2초, 시간은 주로 출력 길이에 비례)
- Deep-Reporter가 근거를 `[Source txtN begin]…[Source txtN end]`, `[Source imgN: caption]` 형태로 넣는다. writer는 **텍스트만** 보고, 이미지는 캡션으로만 안다.
- 비디오 템플릿 규칙
  - 근거에 있는 사실과 시간만 쓰고 시간을 지어내지 않는다. semantic에는 시간을 붙이지 않는다. 근거가 없으면 없다고 쓴다. 시간순으로 쓴다.
  - 인용은 `[citation:txtN]`, 이미지는 별도 줄에 `![](citation:imgN)`. 괄호 하나에 출처 하나, `[citation:imgN]` 금지.
  - 섹션 설명이 `Conclusion:`으로 시작하면(결정 5): 100–250단어로 짧게 종합하고, 새 사건·세부를 넣지 않으며, 사실 문장에는 근거를 인용한다. 위치상 마지막 섹션이므로 Deep-Reporter도 `is_last_section=yes`를 넘긴다.
  - **규칙 6 (결정 4-B)**: 이 섹션에서 이미 쓴 사실·문장·단락을 반복하지 않는다. 앞 섹션에서 다룬 사실은 한 문장 이하로만 언급하고 새 내용에 집중한다. 결론 섹션은 앞 결과를 요약하는 것이 목적이라 예외다.
- **다음 섹션용 맥락 갱신** (LLM 0회). 이 맥락은 다음 섹션의 query 생성과 writer 프롬프트("Context from Previous Sections")에 함께 들어간다.
  - **원래 Deep-Reporter**: `_update_context`가 섹션 설명 + 본문 앞 100자(대부분 제목 줄)를 요약으로, 마지막 3문장을 tail로 넘긴다. 요약이 2,000자를 넘으면 앞 섹션은 설명만 남는다. 그래서 writer는 앞 섹션에서 실제로 쓴 사실을 거의 모른다(보고서 B의 결론 writer는 planner 설명만 받았다).
  - **C0 (기본)**: 요약을 앞 섹션에서 **실제로 쓴 문장**으로 바꾼다.
    - 내용: 안내 문구 + 섹션마다 `Section k: <제목>` + 단락 첫 문장. 인용·이미지 표기는 제거하고 시간은 남긴다.
    - 상한: 문장 240자, 섹션 700자, 전체 3,600자. 넘치면 오래된 섹션부터 제목만 남긴다.
    - 인용 번호를 지우는 이유: 앞 섹션의 번호는 그 섹션의 근거 목록을 가리키므로, 현재 섹션 근거와 섞이면 안 된다.
    - tail은 원래 함수가 그대로 계산한다.
- Deep-Reporter에는 보고서 전체를 생성 뒤에 다듬는 refine/polishing 단계가 없다(코드·논문 확인, `ANALYSIS_D4_D7.md` §1.3).

**④-3 combine**: 섹션 본문을 `"\n\n"`으로 이어 붙인다. 인용은 아직 섹션 내 번호(placeholder) 상태다.

### ⑤ 후처리 (`grounding_postprocessor.ground_report`)
- 섹션마다 writer와 같은 근거 목록(filter off면 `retrieved_*`)으로 번호를 해석한다.
- 텍스트 인용 → 전역 번호 `[n]` (같은 근거는 같은 번호) + 끝에 `# References`.
- 이미지 → `Figure k`로 번호를 매기고, 프레임을 `<out>/frames/`로 복사해 이미지와 캡션(프레임 시각, 클립 구간)을 넣는다.
- 잘못된 형식 `[citation:imgN]` → 그 자리에 `(Figure k)`, 이미지는 단락 바로 뒤에 넣는다.
- 범위 밖이거나 해석할 수 없는 인용 → `[?]`(개수 집계).
- 보고서 A의 실제 변환 예
  ```
  [원본]  At 00:00:40, a person is shown putting on the goggles, which are labeled “SPORTS DRIBBLE SPECS,” while another individual watches [citation:txt3].
  [변환]  At 00:00:40, a person is shown putting on the goggles, which are labeled “SPORTS DRIBBLE SPECS,” while another individual watches [5].
  [References]  [5] 00:00:40–00:00:50 · episodic 10sec: A person puts on a pair of sports goggles labeled "SPORTS DRIBBLE SPECS" on an outdoor basketball court. ...
  ```
  - A 전체: 텍스트 인용 109개 → 참조 46개, 이미지 인용 14개(정상 6 + 잘못된 형식 8) → 그림 7개, 잘못된 인용 0개.
  - B 전체: 텍스트 인용 72개 → 참조 35개, 이미지 인용 19개(잘못된 형식 4) → 그림 14개, 잘못된 인용·누락 프레임 0개.

### ⑥ 규칙 기반 근거 검사 (`check_section_grounding`, LLM 0회)
- 문장마다 **따옴표 문구, 숫자, HH:MM:SS**가 그 문장이 인용한 근거에 있는지 확인한다.
  - 문구: 그대로 일치하거나, 같은 근거 안에서 단어가 같은 순서로 가까이 나오면 인정.
  - 숫자: 정확히 일치, `a/b` ↔ `a out of b`, 작은 수는 영어 단어도 인정.
  - 시간: 인용 근거의 구간 안이면 인정.
- 분류
  - `unsupported`: 어떤 근거에도 없음
  - `miscited`: 인용하지 않은 다른 근거에는 있음
  - `uncited`: 인용 없이 수치·문구를 담은 문장
  - `absence`: "근거에 X가 없다/보이지 않는다" 절 안의 토큰. 검사하지 않고 기록만 한다(아래).
- **부정문(absence) 처리** (2026-10-22 추가)
  - 조건: 부정어(not/no/never/n't 등) 뒤 12단어 안에 show/visible/mention/state/specify 같은 동사가 오고, 문장에 footage/evidence/retrieved/video/clip/frame/source가 있다.
  - 그 **절**(부정어부터 다음 절 경계 `;` 또는 `, but/though/while/which/and…` 또는 문장 끝까지) 안에만 나오는 토큰은 검사하지 않는다. 같은 문장이라도 절 밖의 토큰은 그대로 검사한다.
  - 예: "his score improves to 3/16, though … is not specified in the evidence"에서 `3/16`은 계속 검사한다.
  - 부정 동사나 근거 명사가 없는 부정문은 계속 검사한다. 예: "He did not make the shot, as shown on the scoreboard reading 0/1".
  - 실보고서 적용 결과
    - A: 기존 unsupported·miscited 9건이 모두 그대로 검출된다. uncited 1건("The evidence does not show … from 0/1 to 3/16")이 absence로 바뀌었는데, 이 두 값은 같은 섹션의 다른 문장에서 unsupported로 여전히 검출된다.
    - B: 부정문 오탐 2건(`10:85`, `9:51`)이 absence로 바뀌었다.
  - 한계
    - 부정 절 안에 실제 오류 값이 전제로 들어간 경우(예: "the evidence does not confirm the progression from 0/1 to 3/16")는 검사에서 빠진다.
    - 절 경계 판정은 규칙 기반이다.
- 실보고서 결과(현재 규칙)
  - A: unsupported 4 + miscited 5 중 실제 오류 7(사람 대조, 정밀도 약 78%, 오탐 `SCORE 6` ×2), uncited 7, absence 1.
  - B: unsupported 4 / miscited 3(7건 모두 결론 섹션) / uncited 12 / absence 3.
- 의미 수준의 장면 오인은 잡지 못한다. 결과는 경고로만 쓴다(absence는 경고 없음). 재현율은 정답 데이터가 없어 측정하지 못했다.
- **이미지-텍스트 시간 기록** (`image_time_alignment`, 경고 없음)
  - 섹션에서 인용된 이미지마다 프레임 시각과 인용된 텍스트 근거의 시간 구간 사이 거리를 기록한다(구간 안이면 0, semantic은 시간이 없어 제외).
  - 두 가지 기준
    - `gap_to_local_text_sec`: 같은 단락에서 인용된 텍스트. 이미지만 있는 단락이면 직전 텍스트 단락.
    - `gap_to_section_text_sec`: 섹션 전체에서 인용된 텍스트.
  - 보고서 전체 요약(인용 이미지 수, 0초 수, 최대·중앙값)은 `validation.json`의 `image_time_alignment`에, 이미지별 값은 `sections[*].image_time_alignment`에 남긴다.
  - 섹션 기준 값은 `analysis/analyze_report.py`의 계산과 같다(보고서 B의 인용 이미지 16개로 확인).

### ⑦ 사후 검증 (`run_report.validate`)
| 수준 | 조건 |
|---|---|
| 오류 → exit 1 (산출물은 저장) | `success=False` · 빈 outline · **planner fallback**(섹션 1개이고 설명 == query) · 본문의 `Call failed:` 또는 `[Section generation failed` · 빈 본문 · 텍스트 근거 0건인 섹션 · 잘못된 인용(`[?]`) · 프레임 파일 누락 |
| 경고 (exit 코드 영향 없음) | query 생성 fallback · 인용 없는 섹션 · 잘못된 이미지 형식을 변환한 수 · 규칙 검사 unsupported·miscited·uncited 수 · **(결정 5)** 섹션 수가 `max_sections` 초과 · 마지막 섹션이 `Conclusion:`으로 시작하지 않음 · 결론이 아닌 섹션이 `Conclusion:`으로 시작 · 결론 본문 300단어 초과 · **(결정 6)** 섹션 번역 실패(영어 원문 유지) · 번역에 한자·가나가 재시도 후에도 남음 |

Deep-Reporter는 LLM 호출이 실패해도 예외 대신 `"Call failed: …"` 문자열을 본문에 넣고 `success=True`로 끝날 수 있다. 그래서 이 검증이 필요하다.

### ⑧ 한국어 번역 (결정 6, `report_translator.translate_report`)
- **조건**: `report.translate_ko: true`이고 ⑦에서 **오류가 없을 때만** 실행한다. 오류가 있으면 `translation.status = skipped`로 기록한다.
- **영향 범위**: 영어 `report.md`가 정본이다. 번역 결과는 exit 코드와 영어 결과에 영향을 주지 않는다.
- **단위**: ⑤의 섹션별 본문을 하나씩 번역한다(섹션당 LLM 1회, 최대 출력 `translation_max_tokens: 4096`). LLM은 Deep-Reporter와 같은 엔드포인트와 모델이다.
- **근거 표기 보호**
  - 그림 블록(이미지 줄과 캡션 줄): 번역하지 않고 자리표시로 바꿨다가 원문 그대로 되돌린다.
  - 인용 `[n]`·`[?]`, `(Figure k)`, `HH:MM:SS`, 따옴표 문구: 번역 전에 `[[Pn]]`로 바꾸고 번역 후 되돌린다.
  - **고유명사(사람 이름 포함)** (2026-10-22 추가)
    - 보고서 본문에서 문장 중간에 한 번이라도 대문자로 나온 단어 묶음(예: `Chris`, `SKLZ Dribble Stick`)을 모은다. 문장 첫 단어, 제목 줄, 그림, 이미 보호된 부분, 흔한 단어(The, Section, Video 등)는 제외한다.
    - 모은 목록을 보고서 전체에서(제목 포함) 같은 방식의 자리표시로 보호한다.
    - NER이 없어 사람 이름과 제품·브랜드 이름을 구분하지 못한다. 그래서 둘 다 원문 표기로 남는다(프롬프트 규칙 4와 같은 방향).
    - 문장 첫머리에만 나오는 이름은 수집되지 않는다.
    - 보고서 B에서는 8개가 수집됐다: Chris, Zach, Cass, James, Mitchell, SKLZ, SKLZ Dribble Stick, Shot Coach.
  - 프롬프트에서 자리표시를 그대로 두고, 고유명사는 원문 표기로, 내용 추가나 삭제 없이 번역하라고 지시한다.
- **검사**: 모든 자리표시가 정확히 한 번씩 있어야 하고 제목 줄 수가 같아야 한다(코드 블록으로 감싼 출력은 벗겨서 인정). 실패하면 1회 재시도하고, 그래도 실패하면 그 섹션은 **영어 원문 유지 + 안내 문구** 처리 후 경고를 남긴다.
- **한자·가나 혼입 감지** (2026-10-22 추가)
  - 번역 출력(자리표시로 보호된 원문 제외)에 한자나 가나가 있으면 같은 1회 재시도를 쓴다.
  - 재시도 결과가 깨끗하면 그것을 쓴다.
  - 재시도에도 남아 있거나 재시도가 자리표시 검사에 실패하면, 처음의 유효한 번역을 유지한다. 해당 문자는 `foreign_script`로 기록하고 경고를 남긴다(영어로 되돌리지 않음).
- **구성**: 한국어 헤더(영어 정본의 번역본이라는 안내) + 번역된 섹션(그림은 제자리) + **References 영어 원문 그대로**(근거 원문 인용).
- **상태 기록**: `validation.json`의 `translation`에 다음이 남는다.
  - 전체 상태(complete/partial/failed/skipped/disabled)
  - 보호한 고유명사 목록(`proper_nouns`)
  - 섹션별 상태·시도 횟수·자리표시 수·보호한 이름 수(`protected_names`)·`foreign_script`·시간·실패 이유

### ⑨ 산출물 (`report.outputs_dir/<vid>_<YYYYmmdd_HHMMSS>/`)
| 파일 | 내용 |
|---|---|
| `report.md` | 헤더(영상, 요청, 모델, 검색 모드) + 근거가 연결된 본문 + 그림 + References (정본) |
| `report_ko.md` | ⑧의 한국어 번역본 (번역이 실행된 경우) |
| `report_raw.md` | Deep-Reporter 원본 (placeholder 인용 상태) |
| `report.json` | 요청, checklist, 모델, 검색 모드, 섹션별 설명·검색어·본문·근거 전체, 참조와 그림 목록 |
| `validation.json` | 상태(passed/failed), 오류, 경고, 단계별 시간, `max_sections`, `previous_sections_context`, 인용 통계, 근거 검사 통계(`absence_statements` 포함)와 항목, 이미지-텍스트 시간 요약(`image_time_alignment`), 섹션별 결과(이미지별 시간 차이 포함), 번역 결과(`translation`) |
| `frames/` | 인용된 프레임 사본 (보고서를 옮겨도 이미지가 보이도록) |

Deep-Reporter 세션 로그(JSONL)는 `report.deep_reporter_log_dir`에 쌓인다.

---

## 4. LLM 호출과 시간 (실측)

| 단계 | 호출 | A: 스모크(5섹션) | B: `run_report.py` 첫 실행(6섹션) |
|---|---|---|---|
| planner | 1 | 51.3초 (입력 5,050 / 출력 842토큰) | 36.8초 (입력 5,213 / 출력 849토큰) |
| query 생성 | 섹션 수 | 각 5.1–6.4초 | 각 3.0–4.1초 |
| L1 필터 | 섹션 수 (text 요청당 1) | 각 4.6–5.4초 (입력 2,577–3,205토큰) | 각 3.3–4.1초 (입력 2,275–3,474토큰) |
| writer | 섹션 수 | 각 35.7–66.5초 (입력 2,526–3,154 / 출력 614–1,121토큰) | 각 16.1–34.2초 (입력 2,547–3,217 / 출력 374–794토큰) |
| 후처리·검사 | 0 | 1초 미만 (CPU) | 0.02초 |
| **합계 (영어 보고서)** | **1 + 3 × 섹션 수** | 16회, **382초** | 19회, 생성 **261.5초** |
| 한국어 번역 (결정 6) | 섹션 수 (재시도 시 최대 2 × 섹션 수) | (번역 구현 전) | 6회, 섹션당 23.5–49.2초, **231.8초** (재시도 0) |
| **전체** | | 382초 | **494.4초** |

- WorldMM 원본 검색(full)을 그대로 쓰면 검색에만 쿼리당 최대 5회가 든다(4개 단위 기준). 섹션당 쿼리가 3개면 섹션당 15회 정도 추가된다. 10sec만 쓴 실측에서는 질의 2개에 4회, 9.5초였다.
- 위 수치는 모두 **10sec 단위만** 쓴 조건이다. 4개 단위를 쓰면 L1 필터 입력이 길어지므로 다시 측정해야 한다.
- 생성이 샘플링이라 같은 조건에서도 출력 길이와 시간이 달라진다. A·B의 writer 시간 차이는 주로 출력 길이 차이다.
- **C0 적용 후**에는 query·writer 입력이 늘어난다(요약 최대 3,600자 ≈ 900토큰, 추정). 아직 실제로 측정하지 않았다.
- 번역 시간은 B에서 전체의 47%였다. 실험에서 시간을 줄이려면 `report.translate_ko: false`로 끌 수 있다.

---

## 5. 주요 설정 (`config.yaml`)

| 키 | 기본값 | 의미 |
|---|---|---|
| `llm.backend` | `local` | `local` (Qwen3-VL-8B 서버) / `openai` (`gpt-5-mini`, `OPENAI_API_KEY`) |
| `llm.local.endpoint.{host,port,model}` | `127.0.0.1`, `8010`, `qwen3vl-8b` | Deep-Reporter와 L1 필터가 쓰는 엔드포인트. vLLM으로 바꿔도 같은 주소 |
| `retrieval.episodic_filter` | `L1` | `L0` / `L1` / `full` |
| `retrieval.episodic_candidates_per_query` | `{10sec:3, 30sec:3, 3min:2, 10min:1}` | L0/L1 후보 수 |
| `retrieval.{episodic_k, semantic_k, image_k}` | 8, 4, 4 | 요청당 근거 수 (결정 7: 조정 보류) |
| `service.{host,port,frames_dir}` | `127.0.0.1`, `8020`, `cache/frames` | 검색 서비스 |
| `report.{domain, text_topk, image_topk, enable_filter}` | `videomme`, 20, 10, false | Deep-Reporter 실행 옵션 |
| `report.overview_granularity` | `10min` | planner 영상 개요에 쓰는 캡션 단위 |
| `report.{outputs_dir, deep_reporter_log_dir}` | `outputs/`, `logs/deep_reporter` | 산출물과 세션 로그 |
| `report.max_sections` | 6 | 결정 5: 결론 포함 전체 섹션 수 상한 (허용 3–15) |
| `report.previous_sections_context` | `written` | 결정 4 C0: `written` = 앞 섹션에서 실제로 쓴 문장 전달 / `deep_reporter` = 원래 동작 |
| `report.{translate_ko, translation_max_tokens}` | true, 4096 | 결정 6: 한국어 번역본 생성 여부와 섹션당 최대 출력 토큰 |
| `worldmm.episodic_cache_label` | `qwen3vl-8b` | 검색 서비스가 읽을 HippoRAG 캐시 라벨 (= 사전 인덱싱 LLM 이름) |

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
| 잘못된 인용 번호 | ⑤, ⑦ | `[?]` 치환 + 오류 |
| 잘못된 이미지 인용 형식 | ⑤ | 그림으로 변환 + 경고 |
| 근거에 없는 수치·문구·시간 | ⑥ | 경고 (`validation.json`의 `grounding_findings`) |
| `report.max_sections`가 3–15 밖, `report.previous_sections_context`가 `written`/`deep_reporter`가 아님 | 시작 직후 | exit 2 (생성 전) |
| Deep-Reporter `_update_context` 계약이 어긋남 (C0) | ③ | 실행 전에 오류 (`TemplateContractError`) |
| 영상 id가 `-`로 시작하는데 `--video-id <id>`로 넘김 | 시작 직후 (argparse) | exit 2. **`--video-id=<id>` 형식으로 넘긴다** |
| planner가 16개 이상 섹션 생성 | ④ (`GraphRecursionError`) | `success=False` → 오류 (보고서 전체 소실). 상한 지시로 예방 |
| planner가 상한 초과(15 이하) 또는 결론 규칙 위반 | ⑦ | 경고 |
| 번역 자리표시 손실, 제목 변형, 빈 출력, LLM 오류 | ⑧ | 1회 재시도 후 해당 섹션 영어 원문 유지 + 경고 (exit 코드 영향 없음) |
| 번역에 한자·가나 혼입 | ⑧ | 1회 재시도. 남으면 번역 유지 + `foreign_script` 기록 + 경고 |

---

## 7. 현재 한계와 미구현

- **실제 실행은 10sec 테스트 캐시로 1회**(보고서 B, exit 0)다. 완성된 4개 단위 캐시가 아직 없다(§2 현재 상태). 영상 3개 보고서 실행은 사전 인덱싱 단계에서 멈춰 보고서 단계까지 가지 못했다.
- **사전 인덱싱의 분할 OpenIE·응답 구제·폭주 절단은 CPU로만 검증했다**(실제 실패 응답 14건 구제 포함). 실제 효과와 시간은 GPU 실행에서 확인해야 한다.
- **10min 캡션 잘림**(20영상, 32개): 개요·10min 인덱스·근거에서 잘린 부분이 빠진다. 재생성은 보류.
- **결정 5·6은 실제 1회 확인**했다. 결론 `Conclusion:` 244단어, 6섹션, 번역 6/6 성공, 표기 보존.
- **CPU로만 검증한 것**: 결정 4(규칙 6 + C0), absence 처리, 이미지 시간 기록, 번역 한자 감지·이름 보호. 실제 모델에서의 효과와 지연은 GPU가 다시 허용된 뒤 측정해야 한다.
- 실보고서 2건에서 확인한 품질 문제 (상세 `REPORT_ISSUES_AND_FIXES.md`)
  - 근거 없는 수치나 문구
  - 다른 장면을 엮은 서술
  - 섹션 설명의 내용이 본문에 유입
  - 결론 섹션이 앞 섹션 근거의 사실을 자기 근거에 붙임
  - 근거 없는 추측 표현
  - 번역의 한자 혼입·이름 표기 불일치
  - 반복 단락(A)
  - 이미지와 텍스트 근거의 시간 차이(기록만 함)
  - 규칙 검사는 이 중 수치·문구·시간 유형만 경고한다. 부정 절 처리로 "근거에 없다" 문장의 오탐은 줄였지만, 부정 절 안에 전제로 들어간 오류 값은 검사에서 빠진다.
- **보류된 결정**: 근거 구성(7). 설정과 한계는 `ANALYSIS_D4_D7.md` §2에 정리했다.

## 8. 확장 지점

- **LLM**: `vllm serve Qwen/Qwen3-VL-8B-Instruct --served-model-name qwen3vl-8b --port 8010` 후 `llm.local.endpoint.server: vllm`. vLLM은 아직 설치되지 않았다.
- **검색 백엔드**: MERIT를 같은 `/videos/<vid>/search` 형식의 별도 서비스로 만들고 `service.port`나 URL만 바꾼다.
- **도메인**: `domain_templates.TEMPLATE_SETS`에 `surveillance` 세트를 추가하고 `report.domain`을 바꾼다. 여러 날짜에 걸친 영상이면 근거 라벨과 시간 표기에 DAY를 넣어야 한다.
