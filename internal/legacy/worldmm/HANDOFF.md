# WorldMM × Video-MME 재현 — 인수인계 보고서 (HANDOFF)

> 목적: 이 문서만 읽고 다른 Claude Code가 작업을 **오류·추측 없이 이어서** 수행할 수 있도록 정리.
> 작성 시각 기준 모든 수치는 **실측값**. 최초 작성 2026-09-22, **최종 갱신 2026-09-28 04:17 (Asia)**.
> ⚠️ 아래 **§0-A(최신 상태)** 가 가장 최신이며 우선. (그 아래 일부 섹션의 옛 수치는 이력으로 남겨둠.)

---

## 0-A. 최신 상태 (2026-09-28 04:17) — ★이 섹션 우선★
- **지금 build_memory(50영상 DB indexing)가 GPU 6,7에서 실행 중**(정지 아님). 워커: `queue_worker.sh 6`, `queue_worker.sh 7`.
- **진척(실측): done 44/50, failed 0.** episodic 46 / semantic 46 / visual 44. (claims 40개는 완료분 포함 누적 — cosmetic, 재개 시 삭제.)
- **44개 done 영상 전수 검증 통과**(단순 마커 아님, 내용 유효): episodic triples 평균 2,445(1,400~4,239) / semantic triples 평균 6,533(2,439~17,067) / visual clips 평균 251개(1536-d)(182~357). 누락·0값·오류 0건.
- **남은 6영상**:
  - `7TydWUguPRU`, `7tLtu3QT2OI`: caption+episodic+semantic 완료, **visual만 남음**(현재 처리 중, 곧 done).
  - `8IZvEF4Ui10`, `8UQFaVCV8S8`, `8UxGzDeRIJk`, `9aGgBzToUz4`: **미착수**(caption부터 전체 필요).
- **완료 예상**: 남은 6영상 → 약 4~6시간(무거운 semantic ~2h/영상, 2-GPU) → 09-28 오전 중 done 50 예상.
- **GPU 정책(현행)**: **GPU 6,7만 사용**(사용자 최신 지시). GPU 0~5 미접촉. 실행 시 `CUDA_VISIBLE_DEVICES`/`--gpu`가 물리 6,7에 붙는지 확인(§7.1).

## 0. 한눈에 보는 목표/배경
- **최종 목표**: 논문 *WorldMM*(CVPR 2026, arXiv:2512.02425)의 **WorldMM-8B** 구성으로 **Video-MME (Long)** 재현. 논문 보고치 = **66.0%**. 백본 = 로컬 `Qwen/Qwen3-VL-8B-Instruct`.
- **파일럿(8영상/24문항) 완료**: 보정 최종 **12/24 = 50.0%** (정상 letter 응답만 12/21 = 57.1%). 상세 `claude_output/REPORT.md`.
- **본작업(Phase B)**: 사용자 지시로 300 → **50영상**으로 축소(`video_list.json`, 원본 300은 `video_list_300.json`). 900문항 중 50영상분 ≈ 150문항.
- **산출물은 전부 `claude_output/` 아래**에만 생성. `claude_output/` 밖 파일 수정·삭제 금지(단, `src/` 2파일은 §2의 필수 수정이 이미 적용됨).

---

## 1. 실행 환경 (사실)
- 컨테이너 `worldmm`, 작업경로 `/data1/jyheo/workspace/VideoRAG/WorldMM`, 가상환경 `.venv`(uv).
- Python 3.13 / torch 2.8.0+cu128 / transformers 4.57.6 / flash-attn 2.8.3.
- GPU: NVIDIA RTX A6000 48GB × 8. **공유 서버** — 타 사용자가 GPU 0·2·3 등에서 대형 VLLM(~40GB) 상시 점유. 가용 GPU만 사용해야 함.
- 데이터: `data/Video-MME/data/*.mp4`(900개, Long 300 포함), `data/Video-MME/videomme/test.json`(2700문항). Video-MME용 사전 캡션은 없음(직접 생성).
- 모델(HF 캐시됨): `Qwen/Qwen3-VL-8B-Instruct`(~16–18GB), `Qwen/Qwen3-Embedding-4B`(~8GB), `VLM2Vec/VLM2Vec-V2.0`(~5GB), Whisper `distil-large-v3.5`.

---

## 2. 적용한 소스 코드 수정 (⚠️ 재현 필수, `src/` 2파일)
`git status --short src/` = `M src/worldmm/llm/qwen3vl.py`, `M src/worldmm/memory/episodic/multiscale.py`.
원격 OpenAI 전제 코드를 로컬 백본에서 동작하게 한 수정. **되돌리면 파이프라인이 깨짐.**

### 2.1 `src/worldmm/llm/qwen3vl.py`
1. **동시 generate → CUDA illegal memory access** 방지: `Qwen3VLModel.__init__`에 `self._gen_lock = threading.Lock()` 추가, `generate()`의 GPU 연산 구간을 `with self._gen_lock:`으로 직렬화. (OpenIE 등이 ThreadPoolExecutor로 동일 모델을 동시 호출)
2. **구조화 출력 파서 강건화** (`_parse_structured_response`):
   - 코드펜스(```` ```json ````/```` ``` ````) 제거 일반화.
   - bare JSON 배열 → 단일필드 스키마로 wrap(NerRawOutput.named_entities, TripleRawOutput.triples).
   - `json.loads` → **`json.JSONDecoder(strict=False).raw_decode()`** (JSON 뒤 여분 텍스트 "Extra data" + 문자열 내 제어문자 흡수).

### 2.2 `src/worldmm/memory/episodic/multiscale.py`
- 기존: `_process_video_dir`가 **비디오마다 `LLMModel` 새로 로드** + `generate_multiscale_memory`가 최대 8개 **동시** 처리 → 로컬은 N×16GB로 **GPU OOM**.
- 수정: `generate_multiscale_memory`에서 **모델 1회 로드 후 공유**, `_process_video_dir`가 `llm`을 인자로 받음, `max_workers = 1`(순차).

---

## 3. 파일럿 결과 (8영상/24문항, 사실)
- 사용 영상: Long subset에서 가장 짧은 8개. 설정 = 리포 기본값(§6).
- **1차 eval**: 9/24 = 37.5%. 분해 시 실패의 상당수가 **eval-time GPU OOM(6문항)** 과 **에이전트 라운드소진 "Unable"(3문항)**.
- **보정(실패 영상 재평가) 최종**: `claude_output/pilot/pilot_eval_final.json` = **12/24 = 50.0%**.
  - 정상 letter 응답만: **12/21 = 57.1%**. OOM 0, Unable 3(GsYi-l5PEEs 영상 3문항, 재실행해도 동일 → 모델 한계).
  - 영상별: mzoX 3/3, 0w4·HnS·lAgw 2/3, ctqn·uzy·H8f 1/3, GsYi 0/3.
- **해석(사실 기반)**: 24문항 표본(95% CI ≈ ±20%p)이라 66%와 통계적으로 구분 불가. 파이프라인 end-to-end는 검증됨.
- 파일럿 산출물 전부 `claude_output/pilot/`에 보존(캡션·metadata_all·eval_out·pilot_eval_final.json). 상세 분석은 `claude_output/REPORT.md`.

---

## 4. Phase B (본작업) — 경로/구조 참고 (⚠️ 아래 표의 수치는 2026-09-22 시점 **이력**; 최신 수치는 §0-A)
목표 리스트: `video_list.json` = **50영상**(원본 300은 `video_list_300.json`에 백업). 50영상 = 300 정렬 리스트의 앞 50개.

| 산출물 | 경로 | 개수 |
|---|---|---|
| transcript(.srt) | `full/transcript/` | 36 |
| caption(10sec.json) | `full/caption/{vid}/` | 35 |
| multiscale(10min.json 존재) | `full/caption/{vid}/` | 35 |
| episodic_memory | `full/metadata/episodic_memory/{vid}/` | 35 |
| semantic_memory | `full/metadata/semantic_memory/{vid}/` | 34 |
| visual_memory(visual_embeddings.pkl) | `full/metadata/visual_memory/{vid}/` | 6 |
| **done(완전완료 마커)** | `full/done/{vid}/` | **6** |
| failed 마커 | `full/failed/` | 0 |
| claims(중단시 처리중, **재개 전 삭제**) | `full/claims/` | 10 |

**정확한 남은 작업 분해(합 50)**:
- 6영상: 완전완료(done).
- 28영상: semantic까지 완료 → **visual만** 필요(빠름).
- 1영상: episodic만 완료 → semantic+visual 필요.
- 15영상: **미착수**(caption 없음) → transcribe→caption→multiscale→episodic→semantic→visual 전체 필요.
→ 즉 **무거운 semantic이 남은 영상 = 16개**(1+15), visual만 남은 영상 = 28개.

### 4.1 Phase B 이력 (왜 done이 낮은가 — 사실)
- 2026-09-21 07:11 최초 **300영상**으로 워커 4개 가동. 이후 ~22시간 동안 episodic/semantic을 34영상까지 구축.
- 그러나 **모든 영상이 visual 단계에서 실패**(done 0). 원인 = §7.1의 GPU-0 함정(visual 워커가 물리 GPU 0에서 돌아 OOM). 초기엔 "GPU 경합"으로 오판했다가, 사용자가 GPU 0 사용을 지적해 근본원인(코드의 `env["CUDA_VISIBLE_DEVICES"]=gpu_id`)을 규명.
- 2026-09-22 목표를 **50영상으로 축소**, visual을 `env -u CUDA_VISIBLE_DEVICES ... --gpu $GPU`로 수정 → visual 정상 완료(done 6까지 오름) 확인 후, 사용자 요청으로 전체 정지.
- **교훈**: (a) 자식 프로세스의 `CUDA_VISIBLE_DEVICES` 재설정 주의, (b) 워커 실패 마커가 로그에 안 남으면 모니터가 정지(stall)를 못 잡음 → 정지 감지 필수(초기 파일럿에서 visual 실패로 ~7시간 방치된 전례 있음).

### 4.2 파일럿과 본작업은 별개 디렉토리
- 파일럿 산출물: `claude_output/pilot/`(8영상, `caption_all/`·`metadata_all/`). 본작업: `claude_output/full/`(50영상, `caption/`·`metadata/`).
- 파일럿 8영상(가장 짧은 Long)과 본작업 50영상(정렬 앞 50)은 **교집합이 보장되지 않음** → 메타데이터 재사용하지 말고 각 트리 독립 사용.

---

## 5. Phase B 실행 구조 & 스크립트 (경로 `claude_output/full/`)
- **`queue_worker.sh <GPU>`**: `video_list.json`을 순회, `mkdir claims/{vid}`로 원자적 claim(중복 방지), `done/{vid}` 있으면 skip. GPU에 `MIN_FREE=28000`MiB 이상 확보될 때까지 대기 후 `process_one_video.sh` 호출. 성공 시 `done/{vid}` 마킹, 실패 시 `failed/{vid}` 마킹.
- **`process_one_video.sh <GPU> <VID>`**: 한 영상의 전체 파이프라인. `export CUDA_VISIBLE_DEVICES=$GPU`. 단계별 멱등(이미 있으면 skip):
  1. transcribe(Whisper) → `full/transcript/{vid}.srt`
  2. caption(qwen3vl-8b, unit-time 10) → `full/caption/{vid}/10sec.json`
  3. multiscale → `full/caption/{vid}/{30sec,3min,10min}.json`
  4. build_memory `--step episodic`, `--step semantic` (각각 별도 프로세스; `--step all`은 쓰지 말 것 — §7.1)
  5. build_memory `--step visual` — **⚠️ 반드시 `env -u CUDA_VISIBLE_DEVICES python ... --step visual --gpu $GPU`** (§7.1). 여유대기+최대 15회 재시도 내장.
- **`full_status.sh`**: 한 줄 진척(`done=N/TARGET`), 전 워커 종료/완료 시 알림. TARGET은 `video_list.json` 길이(=50).

---

## 6. 재현 설정(하이퍼파라미터, 리포 기본값 = 논문 Video-MME 설정)
- timescales/granularities: `10sec, 30sec, 3min, 10min` (windows `30,180,600`, unit-time 10).
- 캡션/시각 `num-frames 10`. retrieval top-k: episodic 3 / semantic 10 / visual 3. `max-rounds 5`, `max-errors 5`.
- 백본: retriever = responder = `qwen3vl-8b`. transcript = Whisper `distil-large-v3.5`(ASR).
- **eval의 중요 특성**: eval은 build한 episodic을 재사용하지 않고, 영상마다 4개 granularity 캡션에 대해 **HippoRAG로 OpenIE(NER+triple) 재인덱싱** 후 질의 → 영상당 비용 큼(코스 granularity는 텍스트가 길어 느림).

---

## 7. 알려진 이슈 & 함정 (⚠️ 반드시 숙지)
### 7.1 visual 단계 GPU-0 함정 (해결됨, 재발 주의)
- `build_memory --step visual`은 자식 워커에 **`CUDA_VISIBLE_DEVICES=<--gpu 토큰>`을 새로 설정**한다. 부모가 `CUDA_VISIBLE_DEVICES=4`여도 자식이 `--gpu 0`을 받으면 **물리 GPU 0**에서 돈다. → GPU0 사용 + OOM의 원인이었음.
- **해결**: visual은 `env -u CUDA_VISIBLE_DEVICES python ... --step visual --gpu $GPU`(물리 4~7). episodic/semantic은 서브프로세스가 없어 `--gpu 0`+`CUDA_VISIBLE_DEVICES=$GPU`로도 정상(물리 $GPU에서 동작).
- 결론: **`--step all` 금지**. episodic/semantic/visual을 위처럼 분리 호출.

### 7.2 semantic이 가장 느림
- semantic consolidation이 영상당 수천 triple을 증분 LLM 호출로 처리 → **영상당 ~2시간**. 전체 시간의 지배 요인. 2-per-GPU 불가(메모리).

### 7.3 eval OOM
- `eval/eval.py`는 qwen3vl-8b **2개**(retriever+responder ~32GB)+임베딩 2종(~13GB)=~45GB를 로드 → 단일 48GB GPU에 빠듯. 무거운 영상/경합 시 OOM.
- 파일럿 대응: 실패 영상 재평가. 2-GPU(device_map 분산)는 OOM 막지만 ~2배 느림.
- **권장**: eval은 1-GPU + **OOM 시 자동 재시도**(빈 GPU에서 재실행). 전용 여유 GPU 확보 후 실행.

### 7.4 GPU 경합 & 셸
- 타 사용자 VLLM이 GPU를 상시 점유·변동 → 워커의 `MIN_FREE` 대기가 필요. GPU 0~3 사용 금지.
- 이 세션에서 `pkill`/복합 bash가 간헐적으로 exit 코드 오류(144/1)로 중단된 사례 있음 → **PID를 직접 `kill -9`** 하는 방식이 확실.

---

## 8. 작업 재개 방법 (정확한 명령)
### 8.1 Phase B(50영상) build 재개 — **GPU 6,7만 사용**
※ 지금(09-28)은 이미 GPU 6,7 워커가 돌고 있음. **아래는 중단됐을 때 재개용.** 먼저 `bash claude_output/full/full_status.sh`로 워커 생존 확인 후, 안 돌면 재개.
```bash
cd /data1/jyheo/workspace/VideoRAG/WorldMM
# 0) 우리 워커가 이미 돌면 재개 불필요:
ps -eo cmd | grep "queue_worker.sh [67]" | grep -v grep
# 1) (재개 시) stale claims 제거 — 안 하면 미완료 영상이 skip됨
rm -rf claude_output/full/claims; mkdir -p claude_output/full/claims
# 2) 워커 2개 재가동 (GPU 6,7 전용). done/ 있는 영상 skip, 나머지 이어서.
for g in 6 7; do
  nohup bash claude_output/full/queue_worker.sh $g >> claude_output/full/logs/w$g.log 2>&1 &
done
disown -a
# 3) 진척 확인 + GPU 할당 검증(물리 6,7인지 — 매우 중요)
bash claude_output/full/full_status.sh
for p in $(pgrep -f preprocess/build_memory.py); do tr '\0' ' ' </proc/$p/environ | grep -oE 'CUDA_VISIBLE_DEVICES=[0-9,]+'; done
nvidia-smi --query-gpu=index,memory.used,utilization.gpu --format=csv,noheader   # 6,7만 사용, 0~5는 0이어야
```
- 09-28 04:17 기준 **남은 6영상**: `7TydWUguPRU`,`7tLtu3QT2OI`(visual만) / `8IZvEF4Ui10`,`8UQFaVCV8S8`,`8UxGzDeRIJk`,`9aGgBzToUz4`(전체).
- **예상 시간**: 남은 6영상, 무거운 semantic ~2h/영상, 2-GPU → **약 4~6시간**.

### 8.2 정지 방법(우리 것만 — 타 사용자 미접촉)
```bash
for p in $(ps -eo pid,cmd | grep -E "queue_worker.sh|process_one_video.sh|claude_output/full|generate_fine_caption.py|episodic.multiscale|Video-MME/utils/transcribe.py" | grep -v grep | awk '{print $1}' | sort -u); do kill -9 "$p"; done
# (모니터도 있으면) TaskStop 사용. pkill이 exit코드로 중단될 수 있으니 PID 직접 kill 권장.
```

### 8.3 eval (build 50/50 완료 후) — ⚠️ **50영상용 드라이버 아직 없음(신규 작성 필요)**
- 참고 구현: `claude_output/pilot/run_pilot_eval.py`(파일럿 8영상용 — GPU 리스트 분할, subprocess로 eval.py 병렬 실행, 결과 병합·정확도·응답형식 집계).
- 50영상 eval 드라이버는 이를 복제해 아래로 변경:
  - eval-json: `data/Video-MME/videomme/test.json`에서 `full/video_list.json`의 50영상 문항만 필터(≈150문항).
  - `--caption-dir claude_output/full/caption`, `--metadata-dir claude_output/full/metadata`.
  - `--output-dir claude_output/full/eval_out`, `--episodic-cache-dir claude_output/full/eval_cache`.
  - **GPU 6,7만** 사용. eval은 프로세스당 ~45GB(§7.3) → **GPU당 1개**(6,7에 각 1개 = 2-way). **OOM 시 자동 재시도** 로직 포함(파일럿서 6문항 OOM 손실 전례).
  - GPU 할당 검증 필수(§7.1의 함정은 eval엔 없지만, `CUDA_VISIBLE_DEVICES=6`/`7`로 각 프로세스 핀).
- eval 예상: 영상당 인덱싱 ~30–50분, 50영상 2-way → 대략 **10–15시간**.
- 완료 후 정확도(≈150문항, 95% CI ±~8%p)를 66% 목표와 비교, `claude_output/REPORT.md`에 반영.

---

## 9. 남은 작업 (To-Do) — 2026-09-28 04:17 기준
1. **[build] 진행 중, done 44/50.** 남은 6영상 완료 대기(§0-A, §8.1). GPU 6,7. done=50/50이 목표. (중단 시 §8.1로 재개, GPU 할당 6,7 검증 필수.)
2. **[검증]** build 50 완료 시 44검증과 동일 방식으로 나머지 6영상도 episodic/semantic/visual 내용 유효성 확인(§검증 방법은 이 문서 작성 대화의 검증 스크립트 참조: episodic는 `episodic_triples[timestamp]` 아래를 카운트해야 함 — 최상위 values 카운트 시 0으로 오판함).
3. **[eval]** 50영상 eval 드라이버 작성·실행(§8.3) → ≈150문항 정확도 산출(66% 대비, CI ±~8%p). GPU 6,7, OOM 재시도.
4. **[report]** 결과를 `claude_output/REPORT.md`에 반영(최종 수치·유형별·OOM/Unable 집계).
5. **[선택]** 전체 300 확대 시 `video_list.json`을 `video_list_300.json`으로 교체 후 §8.1 재개(수일, semantic 병목).
4. **[선택]** 전체 300으로 확대 시 `video_list_300.json`으로 교체 후 재개(수일 소요, semantic 병목).

---

## 10. 핵심 파일 맵
- 소스 수정: `src/worldmm/llm/qwen3vl.py`, `src/worldmm/memory/episodic/multiscale.py`.
- 파일럿: `claude_output/pilot/`(worker_*.sh, run_pilot_eval.py, run_reeval.py, pilot_status.sh, visual_recover.sh, caption_all/, metadata_all/, eval_out/, pilot_eval_final.json).
- 본작업: `claude_output/full/`(queue_worker.sh, process_one_video.sh, full_status.sh, video_list.json(50), video_list_300.json, transcript/, caption/, metadata/{episodic,semantic,visual}_memory/, done/, failed/, claims/, logs/).
- 보고서: `claude_output/REPORT.md`(분석), `claude_output/HANDOFF.md`(본 문서).
- 프로젝트 지침: `WorldMM/CLAUDE.md`(신규 파일은 claude_output에만, src 외부 수정·삭제 금지).
