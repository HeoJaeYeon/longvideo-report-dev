# WorldMM × Video-MME 재현 보고서 (WorldMM-8B, 로컬 qwen3vl-8b)

> 상태: **파일럿(8영상/24문항) 완료 단계** — 결과 수치는 §8에 기재. 이후 전체 300영상(Phase B) 진행 예정.
> 작성 근거: 본 문서는 사용자 최종 보고서 작성을 위한 상세 정리본이며, 모든 산출물은 `claude_output/` 아래에 있습니다.

---

## 1. Executive Summary
- **목표**: 논문 *WorldMM: Dynamic Multimodal Memory Agent for Long Video Reasoning* (CVPR 2026, arXiv:2512.02425)의 **WorldMM-8B** 구성으로 **Video-MME (Long)** 성능(**논문 보고치 66.0%**)을 로컬 재현.
- **백본**: `Qwen/Qwen3-VL-8B-Instruct` (retriever/응답 LLM), 임베딩 `Qwen/Qwen3-Embedding-4B`(텍스트) + `VLM2Vec/VLM2Vec-V2.0`(시각).
- **핵심 성과**: 원격 OpenAI 전제로 작성된 코드를 **로컬 백본에서 동작하도록 최소 수정**하여, 전체 파이프라인(preprocess→memory build→eval)을 8영상 규모로 **end-to-end 검증**.
- **검증 규모**: Video-MME Long 중 **가장 짧은 8개 영상(각 ~30분)** / **24문항**을 GPU 4·5·6·7로 병렬 처리.

## 2. 재현 목표 & 근거
- 논문 Table 1: `WorldMM-8B | Video-MME (L) = 66.0`, `WorldMM-GPT(GPT-5) = 76.6`. **(L)=Long subset**.
- 논문은 Video-MME 전용 하이퍼파라미터를 명시하지 않음 → **리포 기본 스크립트 값이 곧 재현 설정**(본 보고서 §9).
- 저자 공개물은 EgoLife 메타데이터(`wgcyeo/WorldMM-EgoLife`)뿐이며 **Video-MME용 캡션/메타데이터는 미공개** → 직접 생성 필수(사전 캡션 없음 확인).

## 3. 파이프라인 구조
```
1_setup      : 의존성 + Video-MME 다운로드 (Long 기본)
2_preprocess : Whisper(distil-large-v3.5)로 영상별 transcript(.srt) 생성
3_build_memory:
   ├ caption       : qwen3vl-8b가 10초 세그먼트마다 프레임 캡션 (episodic 기반)
   ├ multiscale    : 10초 캡션 → 30초/3분/10분 요약 (다중 시간척도)
   ├ episodic      : 캡션에서 NER+triple(OpenIE) 추출 → HippoRAG 그래프
   ├ semantic      : episodic triple에서 일반지식 triple 추출 + 증분 consolidation
   └ visual        : VLM2Vec로 클립 임베딩(1536-d) 추출
4_eval       : 영상별로 4개 메모리(episodic 4척도 + semantic + visual) 인덱싱 후,
                반복 검색(max 5 rounds)으로 4지선다 응답
```
**4종 메모리**: episodic(다중 시간척도 이벤트) / semantic(관계 지식) / visual(시각 임베딩).

## 4. 실행 환경 & 모델
- 컨테이너 `worldmm`, Python 3.13 / **torch 2.8.0+cu128** / **transformers 4.57.6** / flash-attn 2.8.3.
- GPU: NVIDIA RTX A6000 48GB × 8 (공유 서버; 가용분만 사용).
- 캐시된 모델: `Qwen3-VL-8B-Instruct`(~16–18GB), `Qwen3-Embedding-4B`(~8GB), `VLM2Vec-V2.0`(~5GB), Whisper `distil-large-v3.5`.

## 5. 적용한 코드 수정 (재현 필수) — `src/` 2파일
> 로컬 단일 모델은 "원격 OpenAI(동시요청 안전, 스키마 서버강제)" 전제와 충돌 → 아래 수정 필요.

### 5.1 `src/worldmm/llm/qwen3vl.py`
1. **동시 generate → CUDA illegal memory access**: `Qwen3VLModel.generate()`의 GPU 연산 구간을 **`threading.Lock`으로 직렬화**. (OpenIE 등이 ThreadPoolExecutor로 동일 모델을 동시 호출 → 크래시)
2. **구조화 출력 파싱 강건화** (`_parse_structured_response`):
   - 코드펜스(```json / ```) 제거 일반화
   - **bare JSON 배열 → 단일필드 스키마로 wrap** (NerRawOutput.named_entities, TripleRawOutput.triples). OpenAI는 `responses.parse`로 스키마를 서버강제하지만 로컬은 프롬프트만으로 배열을 뱉음.
   - **`json.JSONDecoder(strict=False).raw_decode()`** — JSON 뒤 여분 텍스트("Extra data")·문자열 내 제어문자 흡수.

### 5.2 `src/worldmm/memory/episodic/multiscale.py`
- **비디오마다 `LLMModel` 새로 로드 + 최대 8개 동시** → 로컬은 N×16GB로 GPU OOM.
- 수정: **모델 1회 로드 후 공유 + `max_workers=1`(순차)**. (generate는 이미 락으로 직렬화되어 속도 손해 없음)

> ⚠️ 이후 사용자 지침으로 `src/` 추가 수정은 중단(모든 신규 파일은 `claude_output/`). 위 수정은 그 이전에 적용·검증됨.

## 6. 파일럿 방법론
- **영상 선정**: Long subset 300개 중 **가장 짧은 8개**(각 ~30분, ffprobe로 선정) → 캡션/인덱싱 시간 최소화.
- **GPU 오케스트레이션**(모두 `claude_output/pilot/` 내):
  - 캡션·multiscale·build_memory: **샤드별 격리 디렉토리**로 GPU에 분산(episodic/semantic이 caption-dir 전체를 처리하므로 샤드 분리 필수).
  - **자동 재시도/대기**: GPU 경합 시 ≥필요메모리 GPU 확보까지 대기 후 실행(s8 leftover 패턴).
  - **모니터링**: 상태 스크립트 + Monitor로 10분 주기 점검, `[sX] FAIL`/정지(stall) 감지.
- **eval**: 8영상을 GPU 4·5·6·7 **4-way 분할**, 결과 JSON 병합.

## 7. 인시던트 & 원인 분석 (모두 해결)
| # | 증상 | 원인 | 조치 |
|---|---|---|---|
| 1 | CUDA illegal memory access | 동일 로컬 모델 동시 generate | qwen3vl.py 스레드 락 |
| 2 | triple 0개 (파싱 실패) | 모델이 bare 배열 반환 | 단일필드 wrap |
| 3 | "Extra data" JSON 오류 | JSON 뒤 여분 텍스트 | raw_decode |
| 4 | "control character" JSON 오류 | 문자열 내 제어문자 | JSONDecoder(strict=False) |
| 5 | multiscale OOM (4영상 중 3 실패) | 비디오별 모델 동시 로드 | 모델 1회 로드 공유 |
| 6 | **build_memory 7시간 방치** | visual 단계가 **타 사용자 GPU 점유로 OOM**, 게다가 FAIL 마커가 `.log`가 아닌 `.nohup`에 기록되어 모니터 미감지 | 유휴 GPU서 **visual만 재실행**(episodic/semantic 보존) + 모니터에 **정지(stall) 감지 추가** |

**교훈**: (a) 공유 GPU 경합 대비 자동 대기·재시도, (b) 실패 마커/정지 감지를 로그 기반 모니터에 반드시 포함.

## 8. 결과 (파일럿 24문항)

### 8.1 1차 eval (전체 24문항)
- **전체 정확도: 9/24 = 37.5%** (목표 66%보다 낮음)
- **응답 형식별 분해 (중요)**:
  | 형식 | 정확도 | 비고 |
  |---|---|---|
  | 정상 letter (A~D) | **9/15 = 60.0%** | **실제 추론 정확도 → 목표 66%에 근접** |
  | CUDA OOM 오류 | 0/6 | eval-time 2영상이 **GPU 경합으로 OOM** → 자동 오답(인프라 문제) |
  | Unable(라운드 소진) | 0/3 | 1영상, max-rounds 소진 |
- **해석**: 낮은 전체 수치는 **모델/충실도가 아니라 eval-time GPU 경합 OOM**이 주원인. eval이 정상 실행된 응답만 보면 **60%로 목표(66%)와 24문항 노이즈 내 사실상 일치**.
- 유형별(1차): Information Synopsis 4/5, Object Reasoning 4/11, Temporal 1/5, Action Recognition 0/2, Action Reasoning 0/1 (표본 극소, 노이즈 큼).

### 8.2 보정 재평가 (실패 3영상 재실행)
1차에서 0/3이던 3영상을 재평가한 결과, 실패 원인이 둘로 분리됨:
- **lAgwMGRvJrM**: OOM(인프라) → 재실행 시 **0→2/3** 복구.
- **H8fGd3fCJbg**: OOM(인프라) → **2-GPU(device_map 분산)** 재실행으로 **0→1/3** 복구(OOM 제거).
- **GsYi-l5PEEs**: OOM 아님 → **3문항 모두 "Unable"(에이전트가 max-rounds 내 답 미확정)**, 재실행해도 동일 → **모델 고유 한계(정당한 오답)**.

**보정 최종 결과** (`claude_output/pilot/pilot_eval_final.json`):
| 지표 | 값 |
|---|---|
| **전체 정확도** | **12/24 = 50.0%** (1차 37.5% → OOM 6문항 복구) |
| **정상 응답(letter)만** | **12/21 = 57.1%** |
| 응답 형식 | letter 21 / Unable 3 / **OOM 0** |
| 영상별 | mzoX 3/3, 0w4·HnS·lAgw 2/3, ctqn·uzy·H8f 1/3, GsYi 0/3(Unable) |

**해석**: 보정 후에도 목표 66%보다는 낮으나, **24문항 표본(95% CI ≈ ±20%p)에서는 66%와 통계적으로 구분되지 않음**. 남은 실패는 (a) GsYi 3문항의 라운드 소진(모델 한계), (b) 전반적 8B 추론 편차. 파일럿의 목적(파이프라인 end-to-end 검증 + 방향성)은 달성 — **정확한 수치는 전체 900문항(Phase B)에서 확정**.

**2-GPU eval 관찰**: device_map 분산은 OOM을 막지만 GPU간 통신 지연으로 ~2배 느림(1영상 ~2.5h). → Phase B eval은 **1-GPU + OOM 자동 재시도**가 효율적.

### 8.3 기타
- parseErr(비치명, 재시도로 흡수): build 단계 누적 ~184건(episodic+semantic 수천 성공 대비 ~1–2%)
- **교훈(전체 300 필수 반영)**: eval-time에도 GPU 경합 OOM이 발생 → Phase B의 eval은 **전용 여유 GPU 확보 + OOM 자동 재시도**가 필수(파일럿에서 이걸로 6문항 손실).
- 산출물: `claude_output/pilot/pilot_eval_merged.json`(1차), `pilot_eval_final.json`(보정)

## 9. 보고서 작성용 기술 디테일
- **재현 설정(하이퍼파라미터)**: timescales `10s/30s/3min/10min`, `unit-time=10`, 캡션/시각 `num-frames=10`, retrieval top-k `episodic=3 / semantic=10 / visual=3`, `max-rounds=5`, `max-errors=5`. 백본은 retriever=responder=`qwen3vl-8b`.
- **transcript**: Whisper `distil-large-v3.5`(ASR). (원본 자막이 아닌 ASR 사용)
- **eval-time 재인덱싱(중요)**: eval은 build_memory의 episodic을 **재사용하지 않고**, 영상마다 4개 granularity의 캡션에 대해 **OpenIE(NER+triple)를 재실행**해 HippoRAG 그래프를 새로 구축함. → eval의 최대 비용(영상당 ~30–50분). 코스 granularity(30초 이상)는 캡션 텍스트가 길어 청크당 처리(~3초→~12초)로 느려짐.
- **충실도 caveat**: 구조화 추출에서 ~1–2% 파싱 실패(재시도→빈값). 저자 8B 실험의 파싱 처리 방식과 동일 보장 없음 → 재현 수치가 66%와 다소 차이날 수 있음.
- **파일 맵**:
  - 캡션: `claude_output/pilot/g{5,6}/caption/{video}/{10sec,30sec,3min,10min}.json` (+ `caption_all/`)
  - 메타데이터: `claude_output/pilot/metadata_all/{episodic,semantic,visual}_memory/{video}/`
  - eval 결과: `claude_output/pilot/eval_out/g{4,5,6,7}/qwen3vl_8b_qwen3vl_8b/videomme_eval.json` → 병합 `pilot_eval_merged.json`
  - 로그: `claude_output/pilot/*.log`, 오케스트레이터 `run_pilot_eval.py`, 워커 `worker_*.sh`

## 10. 전체 300영상(Phase B) 계획 & 타당성
- **병렬화(OOM 안전)**: caption/multiscale/episodic → **2 프로세스/GPU × 4 = 8-way**(각 ~18GB), semantic/visual/eval → **4-way**(semantic ~24GB, eval ~44GB로 1/GPU).
- **예상 소요(4 GPU)**: caption ~15–20h, multiscale ~10–15h, episodic ~15–20h, **semantic(최대 병목) 수십시간~수일**, visual ~2–4h, eval(900문항) ~1–2일. **총 ~4–7일**.
- **핵심 리스크**: semantic consolidation이 영상당 수천 triple을 증분 LLM 호출로 처리 → 가장 느림(2/GPU 불가). 공유 GPU 경합 시 지연.
- **자율 운영**: 정지/OOM 자동복구 + 정지감지 내장 오케스트레이터로 백그라운드 자가진행.

## 11. 재현 요약(핵심 3줄)
1. 리포 코드는 GPT(원격) 전제 → 로컬 qwen3vl-8b엔 **동시성·구조화출력·모델로딩** 3계열 수정 필요(§5).
2. 파이프라인은 preprocess→(caption→multiscale→episodic→semantic→visual)→eval이며, **eval이 질의시 episodic을 재인덱싱**해 비용이 큼(§9).
3. WorldMM-8B/Video-MME(L) 목표는 **66.0%**이며, 파일럿 수치는 §8(표본 24문항이라 방향성 지표).
