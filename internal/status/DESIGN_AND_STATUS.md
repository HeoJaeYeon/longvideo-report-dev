# Video-RAG × Deep-Reporter 장편 비디오 보고서 프레임워크 — 분석·설계·구현 현황

- 작성: 2026-10-21~22 (Claude Code, 사용자 지시와 승인에 따라 작성). 최종 갱신: 2026-10-26 (흐름 오류·추측 표현 측정 §9.17, P19 영상 끝 근거·반복 경고 기준·검사 오탐 수정 §8.13. 2026-10-25: P9·P19·I28 §8.12·§9.16, 결정 16, C-1–C-5 §9.10–§9.14, 재시도 이력 §9.15, I29·I30)
- 위치: `report_framework/internal/status/DESIGN_AND_STATUS.md` (2026-11-10 이전: `report_framework/DESIGN_AND_STATUS.md`). 2026-11-12: §2.5(10-26–11-12 진행)와 §13.3 (2-2) 추가.
- **처음 이어받는 사람은 §2(현재 상태)와 §13(인수인계)부터 읽는다.**
- **2026-11-10 경로 정리** (동작 변경 없음, 상세 `internal/status/REORG_LOG_20261110.md`): WorldMM 메모리 `WorldMM/claude_output/full/` → `WorldMM/output/memory/videomme_long_qwen3vl-8b/`, 사전 인덱싱 캐시 `report_framework/cache/episodic/` → 같은 폴더의 `report_framework_index/`(둘 다 복사, md5 동일. 원본은 2026-11-12 삭제). `config.yaml`의 경로는 `report_framework/` 기준 상대 경로이고 `rf_config.load_config()`가 해석한다. 메모리 구축 스크립트는 `scripts/memory_build/`, Docker 정의 사본은 `docker/`, WorldMM 로컬 수정 patch는 `patches/worldmm/`에 있다. 메모리·캐시의 옛 경로 표기는 당시 기록이다. 같은 날 폴더 재배치(P2): 스크립트·결과 경로(`tests/*` → `tests/unit/`·`tests/gpu/`·`experiments/`·`scripts/launch/`, `analysis/*.json` → `results/`, `inspect/`·`running_example/` → `internal/`)는 본문에서도 새 위치로 고쳐 적었다. 문서 위치는 `docs/README.md` 색인.

## 0. 문서 안내

### 0.1 목적
코드, 논문, 디스크 상태를 직접 확인해 얻은 사실과 그에 따른 설계 결정, 구현 내용, 검증 결과, 남은 위험을 한 곳에 정리한다. 다음 작업자가 이 문서만으로 현재 상태를 파악하고 작업을 이어갈 수 있게 하는 것이 목표다.

### 0.2 관련 문서

| 문서 | 내용 |
|---|---|
| `DESIGN_AND_STATUS.md` (이 문서, 2026-11-10부터 `internal/status/`) | 목표, 분석 결과, 설계 결정, 구현 상세, 검증 기록, 위험, 인수인계 |
| `REPORT_PIPELINE.md` | 보고서 1건이 만들어지는 과정(①–⑨ 단계), 시간, 설정, 실패 처리 |
| `REPORT_ISSUES_AND_FIXES.md` | 실제 보고서와 개발 과정에서 나온 문제, 검토한 방법, 수정 내용과 효과 |
| `ANALYSIS_D4_D7.md` | 결정 4(반복)·결정 7(근거 구성) 분석 자료 |
| `FRAMEWORK_OVERVIEW.md` | 팀·지도교수 보고용 전체 설명(구조, 동작, 이슈, 한계) |
| `REPORT_AND_SLIDES_DRAFT.md` | 보고서 초안과 슬라이드 구성안 |
| (2026-11-10) 문서 위치 | 아래 문서들은 `docs/`·`internal/{status,analysis,meetings}/`로 옮겼다. 위치 색인: `docs/README.md` |
| `MIGRATION_HANDOFF.md` | 다른 서버(`/home/USER/workspace/VideoRAG`)로의 이전 준비 기록: 복사 범위·검증, 새 서버에서 할 일(경로 수정 13개 파일, 모델 위치, Docker 마운트) |

### 0.3 표기

| 표기 | 의미 |
|---|---|
| ✔ | 코드를 직접 읽었거나 명령으로 실측해 확인함 |
| ◇ | 기존 기록 문서(예: `WorldMM/claude_output/REPORT.md`)에서 인용, 이번에 재측정하지 않음 |
| ✖ | 아직 검증되지 않음 |
| (추정) | 계산이나 가정에 기반한 값 |

코드 위치는 `파일:줄`로 적는다. 줄 번호는 2026-10-21~22 시점 기준이다. 보고서 A·B는 §9.3·§9.4의 실제 실행 결과를 가리킨다.

**시각 표기**: 이 문서와 로그의 시각은 모두 컨테이너 시계 기준이다. 컨테이너는 `TZ=Asia/Seoul`이지만 `/usr/share/zoneinfo/Asia/Seoul`이 없어 실제로는 **UTC**로 동작한다(✔ 2026-10-25: `date`와 `date -u`가 같은 시각, 파일 시각 `+0000`). 한국 시간은 9시간을 더한다. 처음 작성할 때 일부 실행 날짜를 2026-10-22로 적었으나 실제로는 UTC 2026-10-21 실행이었던 것(`.venv` 수리, 검색 스모크, 보고서 A)을 2026-10-25에 파일 시각·대화 기록 시각으로 확인해 고쳤다(§2.3, §3, §10). 결정 시점(§6.2)처럼 시각 기록이 없는 날짜는 고치지 않았다.

---

## 1. 목표, 범위, 원칙

- **최종 목표**: 장편 영상에 대한 질의(query)를 받아 보고서 outline을 구상하고, 섹션마다 Video-RAG(WorldMM 중심, MERIT 교체 가능)로 근거를 검색해 Deep-Reporter 방식으로 **근거 인용이 붙은 보고서**를 생성하는 통합 프레임워크.
- **1차 대상**: Video-MME long subset (메모리 구축이 끝난 50개 영상). 이후 관제(surveillance) 영상으로 도메인을 전환한다.
- **원칙 (사용자 지시)**
  - 기존 repo(WorldMM, MERIT, Deep-Report) 코드는 삭제·수정하지 않는다. 신규 코드는 `VideoRAG/report_framework/`에만 둔다. Deep-Reporter 동작을 바꿀 때는 실행 중에만 적용하고 끝나면 되돌리는 검증된 교체(§7.4)만 쓴다.
  - LLM 기본값은 로컬 Qwen 계열(Qwen3-VL-8B)이다. 외부 API(OpenAI) 경로는 보존하고 설정으로 선택한다.
  - LLM 호출 수가 많은 무거운 설계는 피한다.
  - 분석과 보고에는 추측이나 거짓을 넣지 않는다. 확인하지 않은 것은 미확인이라고 쓴다.
  - GPU는 사용자가 허용할 때만, 허용된 GPU에서, 다른 사용자의 프로세스를 절대 침범하지 않는 범위에서 쓴다. 허용 범위는 사용자 지시로 바뀌어 왔다(최신 2026-10-25: 이 서버의 **GPU 4–7 사용 가능**, §13.1).

---

## 2. 현재 상태 요약 (2026-10-25)

- 2026-10-26 이후의 진행은 §2.5, 현재 상태의 짧은 요약은 `internal/status/CURRENT_STATUS.md`(2026-11-12).

### 2.1 구성요소별 상태

| 구성요소 | 파일 | 상태 | 검증 수준 |
|---|---|---|---|
| 설정 | `config.yaml` | 완료 | — |
| 오프라인 사전 인덱싱 | `prebuild_episodic_index.py`, `run_prebuild.sh`, `run_prebuild_http.sh` | 완료. 결정 1 = A안(OpenIE를 LLM 서버 HTTP로) + **긴 청크 분할 OpenIE·응답 구제·폭주 절단**(2026-10-22, §8.3) | dry-run ✔ / CPU ✔ / 실제 실행: 영상 1개 완주(분할 적용 전, §9.6) / **분할·구제 적용 후 영상 3개 완주 ✔**(2026-10-25 C-1, §9.10) |
| 로컬 LLM 서버 | `local_llm_server.py` | 완료 (2026-10-25: `max_tokens_cap` 3,072, 토큰 계산을 생성 잠금 안으로, §8.12) | GPU 실검증 ✔ / 상한 동작 ✔(§9.16) |
| [A] 검색 서비스 | `videorag_retriever_service.py` | 완료 | CPU 통합 ✔ / GPU ✔ 10sec(§9.2) / **4개 단위 ✔**(C-3, §9.12: L0·L1·full, 영상 3개, 요청 36건 성공) / 같은 영상을 서비스 2개가 동시에 불러오면 실패(I29, §9.14) |
| 템플릿·맥락 교체 | `domain_templates.py` | 완료 (videomme 템플릿, 결론·상한, 규칙 4·6, C0) | CPU ✔ / 실제 보고서: A·B(규칙 6·C0 추가 전), C-4 3건(§9.13), C-5 8건(C0 켬 4·끔 4, §9.14). C0 효과 확인 안 됨, writer 반복 루프 2건(P9) |
| [C] 후처리기·규칙 근거 검사 | `grounding_postprocessor.py` | 완료 (absence 처리, 이미지 시간 기록 포함) | CPU ✔ / 실제 실행: B 1회(absence·시간 기록 추가 전), C-4 3건·C-5 8건(현재 판). 결말 오인(P19)·writer 루프(P9)는 잡지 못함 |
| [D] 보고서 생성 진입점 | `run_report.py` | 완료 | CPU end-to-end ✔ / 실제 모델: B(§9.4), C-4 3건, C-5 8건 모두 exit 0·`passed`. C-5 첫 시도 1건은 서비스 불러오기 실패로 exit 2(I29) |
| 한국어 번역 | `report_translator.py` | 완료 (한자·가나 감지, 고유명사 보호 포함) | CPU ✔ / 실제: B 6/6(감지·보호 추가 전), **C-4 17섹션 중 12 성공·5 실패(자리표시자 불일치, 영어 유지)**(§9.13, P15). C-5는 번역 끔 |
| 분석 도구 | `analysis/analyze_report.py`, `analysis/openie_degeneration_exp.py`, `analysis/compare_openie_cache.py` | 완료 | A·B·C-4·C-5 보고서에 적용 ✔ / OpenIE 디코딩 실험 ✔(§9.7) / OpenIE 캐시 비교 ✔(§9.11). `analyze_report.py`의 단락 유사도는 한 단락 안의 반복 루프를 잡지 못함(§9.14) |
| GPU 실행 스크립트 | `experiments/gpu_3videos.py`, `experiments/delayed_gpu_3videos.py`, `experiments/gpu_retrieval_probe.py`, `experiments/gpu_report_batch.py` | 완료 (여러 LLM 서버, 상한 선택, 메모리 감시·자동 중단 / 대기 후 시작 / 검색 점검 / 보고서 병렬, 영상별 불러오기 잠금) | 감시 장치 실동작 ✔(§9.8) / **C-1 완주 ✔**(§9.10) / C-3·C-4·C-5 실행 ✔ / 대기 시작은 조건 미충족으로 미시작(§9.9) |
| 평가, MERIT backend, 관제 도메인 | — | 이후 | — |

### 2.2 지금 할 수 있는 것과 아직 안 되는 것

- **할 수 있는 것**: LLM 서버와 검색 서비스를 띄우고 `run_report.py`를 실행하면 다음이 나온다.
  - 근거가 연결된 영어 보고서(`report.md`, References·그림 포함)
  - 한국어 번역본(`report_ko.md`, `report.translate_ko: true`일 때. 2026-11-12부터 기본 off)
  - 원본(`report_raw.md`), 전체 기록(`report.json`), 검증 결과(`validation.json`)
- **아직 안 되는 것**
  - **4개 단위(10sec/30sec/3min/10min) episodic 캐시는 검증 영상 3개(`-QuCz7kxBr8`, `0RxMZBLeqRI`, `54k2g9ddy4M`)만 완성됐다**(2026-10-25 C-1, §9.10). 나머지 47개 영상은 없다(C-7, 미실행).
  - 4개 단위 캐시로 검색(C-3, §9.12)과 보고서 생성(C-4 3건 §9.13, C-5 8건 §9.14)은 했다. 그 결과 **보고서 품질 문제가 남아 있다**: writer 반복 루프(P9, C-5 8건 중 2건), 구간 요약의 "the video closes"를 영상 결말로 옮김(P19), 섹션 시간 순서 뒤집힘·화자 뒤바뀜(P8·P4), 번역 실패 증가(P15). 지금의 검증(`validation.json`)은 이 문제들을 막지도 표시하지도 못한다. 대응 방향은 사용자 결정 대기다(§13.3).
  - 결정 4(C0)의 효과는 C-5 4 대 4 표본으로 확인되지 않았다(§9.14). 결정 7(근거 구성)은 질문 전이다.
  - 분할 OpenIE·응답 구제·폭주 절단은 GPU 실행으로 동작을 확인했다(§9.10). 분할 전후 비교는 §9.11.
  - 품질 평가(Video-MME 문항 풀이, 사람 검수)는 시작하지 않았다.
- **GPU**
  - 2026-10-22: **GPU 6·7만**, 다른 사용자 프로세스 절대 침범 금지. 다른 사용자가 그 GPU들을 크게 오르내리며 써서(§9.8 시점 GPU 6 약 18–30GB, GPU 7 약 18–34GB, §9.9 18시 이후 10분 최대값 30–39GB) 실행하지 못했다. §9.8은 감시 장치가 우리 프로세스만 종료했고, §9.9는 6시간 동안 시작 조건을 한 번도 만족하지 못해 시작하지 않았다.
  - 2026-10-23: 다른 서버로 옮기는 준비를 했다(`MIGRATION_HANDOFF.md`). 프로젝트 파일 758MB를 새 서버에 복사·검증했고, 새 서버에서의 Docker 빌드·모델 다운로드·경로 수정은 아직 하지 않았다. 새 서버에서는 호스트 GPU 3·4를 다른 사용자와 같이 쓰는 계획이다(사용자).
  - **2026-10-25 (최신): 이 서버에서 GPU 4–7 네 개를 모두 사용할 수 있다**(사용자 지시). 같은 날 11:44 확인 시 GPU 0–7 모두 사용량 0–3 MiB였다. 다른 사용자 프로세스를 침범하지 않는다는 원칙과 감시는 그대로 지킨다(§13.1). 사용자 지시로 C 단계의 우리 프로세스에는 메모리 상한을 걸지 않았다(§6.2 결정 14).
  - 2026-10-25 13:47 확인: **GPU 0–3에 다른 사용자 프로세스 4개**(각 약 40GB, 사용률 100%)가 새로 올라와 있다. GPU 4–7은 비어 있다(0/0/0/3 MiB). 우리는 GPU 4–7만 쓰므로 영향은 없지만, 다음 실행 전에도 GPU 4–7 여유를 다시 확인한다.

### 2.3 실제 모델 실행 기록

| 실행 | 일시 | 내용 | 결과 | 상세 |
|---|---|---|---|---|
| 검색 스모크 | 2026-10-21 16:24–16:31 | 10sec 실제 캐시, L0·L1, Deep-Reporter `search_node` 연결 | 정상 | §9.2 |
| 보고서 A (스모크) | 2026-10-21 | `tests/gpu/gpu_report_smoke.py`, 5섹션 | 성공, 382초 | §9.3 |
| 보고서 B (`run_report.py` 첫 실행) + full 모드 | 2026-10-22 (06:17 보고서 저장) | `tests/gpu/gpu_e2e.py`, 6섹션, 번역 포함 | exit 0, 494.4초 | §9.4 |
| 사전 인덱싱 시험 (A안) | 2026-10-22 06:31 | 영상 1개, LLM 서버 3 + 인덱서 1 | 10sec 완료, 30sec 도중 **중지** | §9.5 |
| 영상 3개 사전 인덱싱 + 보고서 | 2026-10-22 12:04 | LLM 서버 7(GPU 4–7) + 인덱서. 분할 적용 전 코드 | 영상 1 완료(668초). 영상 2의 10min에서 OpenIE 잘림·재시도로 정체 → **사용자 지시로 중지**. 보고서 단계 미실행 | §9.6 |
| OpenIE 디코딩 비교 실험 | 2026-10-22 12:41–13:26 | 문제 10min 청크 4개 × 2회 × 설정 3개(GPU 5·6·7) | 디코딩 변경 기각, 분할 + 구제·절단 채택 근거 | §9.7 |
| 영상 3개 재실행 (분할·구제 적용) | 2026-10-22 14:10 | GPU 6·7만, LLM 서버 1 + 인덱서 1 | **41초 만에 감시 장치가 우리 프로세스 종료**(다른 사용자 메모리 증가). OpenIE 호출 0회, 캐시 변경 없음 | §9.8 |
| 영상 3개 대기 후 자동 시작 | 2026-10-22 16:05 – 10-23 00:06 | GPU 6·7만. 2시간 대기 후 10분 최대 사용량으로 여유 판단 | **시작 조건을 698번 판단 중 한 번도 만족하지 못해 시작하지 않음**(가장 큰 여유 −961 MiB). 우리 GPU 프로세스 0개, 캐시 변경 없음 | §9.9 |
| 영상 3개 사전 인덱싱 C-1 (분할·구제 적용) | 2026-10-25 12:15–12:45 | GPU 4–7, LLM 서버 7 + 인덱서, 메모리 상한 없음 | **완주.** 호출 430회(계획과 같음), 1,643초, 실패 요청 0, 완료 표식 3개 | §9.10 |
| C-3 검색 확인 (4개 단위) | 2026-10-25 12:52–13:00 | LLM 서버 1(GPU 4) + 서비스 L0/L1/full(GPU 5/6/7) | 요청 36건 성공. text 지연 L0 0.7–1.4초, L1 4.4–7.9초, full 29.7–38.8초 | §9.12 |
| C-4 보고서 3건 (4개 단위) | 2026-10-25 13:02–13:17 | 묶음 3개(GPU 4/5/6), 영상당 1건, 번역 포함 | 3건 exit 0·`passed`. 결말 오인(P19)·흐름 오류·번역 실패 5/17 확인 | §9.13 |
| C-5 첫 시도 (C0 켬/끔 8건) | 2026-10-25 13:21–13:27 | 묶음 4개(GPU 4–7) | 1건 서비스 불러오기 실패(HTTP 500, I29) → Claude가 중단하고 사후 보고, 완료된 4건은 비교에 미사용 | §9.14 |
| C-5 재실행 | 2026-10-25 13:28–13:46 | 같은 조건 + 영상별 불러오기 잠금 | 8건 exit 0·`passed`. C0 효과 확인 안 됨, writer 반복 루프 2건(P9) | §9.14 |
| P9·P19 수정 후 확인 | 2026-10-25 14:14–14:32 | 영상 3개 × C0 켬 × 3회, 번역 끔, GPU 4–7 | 9건 exit 0·`passed`. 상한 도달 2건(130–134초에 끊김, 문장 37·39개 제거). 결말 오인은 검사로 표시되지만 writer 규칙만으로 막지 못함 | §9.16 |

### 2.4 알려진 품질 문제 (요약, 상세는 `REPORT_ISSUES_AND_FIXES.md`)

| 문제 | 대응 상태 |
|---|---|
| 인용이 붙은 문장의 근거 없는 수치·문구, 다른 근거 인용 | 규칙 검사로 경고(의미 수준 오류는 미검출) |
| 다른 장면을 같은 사건으로 엮음 | 감지 안 됨 |
| planner 섹션 설명의 내용이 근거 없이 본문에 들어감 | 경고만. C0의 완화 효과는 C-5에서 확인되지 않음 |
| 결론 섹션이 앞 섹션의 사실을 자기 근거에 붙임 | C0의 완화 효과는 C-5에서 확인되지 않음(결론 지적 수: 켬 7·1·1·1, 끔 4·4·0·0) |
| 반복 단락, **writer 반복 루프** | 규칙 6 + C0. C-5에서 루프 2/8건. 2026-10-25 대응(§8.12): 서버 상한 3,072, 같은 문장 제거, 경고. 확인(§9.16): 루프 2/9건이 130–134초에 끊기고 반복 문장이 보고서에서 빠짐. 끊긴 섹션은 문장 중간에서 끝남 |
| 근거 없는 추측 표현 | 대응 없음 |
| 번역의 한자 혼입·이름 표기 불일치 | 감지·재시도, 이름 보호 구현. C-4 실측: 17섹션 중 5개 자리표시자 불일치로 실패(영어 유지), 한자·가나 잔존 3섹션(§9.13). 제목 형식 불일치는 미대응 |
| 구간 요약의 "the video closes" 표현이 영상 전체 결말로 옮겨짐(P19), 섹션 시간 순서 뒤집힘, 화자 뒤바뀜 | P19 대응(§8.12): writer 규칙 7(실제 영상 끝 시각 포함), 결말·시작 서술 검사. 확인(§9.16): 검사가 표시하지만 writer 규칙만으로 오인이 줄었다고 단정할 수 없음(보고서당 1.22건, 수정 전 1.25–2.0). 순서·화자 오류는 대응 없음 |
| 이미지와 텍스트 근거의 시간 차이 | `validation.json`에 기록. 출력 변경은 결정 7 보류 |
| (인덱스 품질) 10min 캡션 32/232개가 전처리에서 2,048토큰에 잘림. **검증 영상 3개 중 `0RxMZBLeqRI`의 10min 0–10분·10–20분 캡션이 여기에 해당**(§11) | 원인 확인, 재생성은 보류(I22) |
| (인덱스 품질) 10min OpenIE 출력 잘림·재시도 폭증, 열거 폭주 triple | 분할 OpenIE + 구제 + 연속 15개 초과 절단, GPU 검증(C-1: 호출 = 계획, 구제 5건, 절단 146개). 분할 기준 아래 입력의 잘림 3건, 정당한 나열 절단 확인(I23·I24) |


### 2.5 2026-10-26 – 11-12 진행 (분석·정리, GPU 사용 없음)

현재 상태의 짧은 요약은 `internal/status/CURRENT_STATUS.md`가 맡는다. 이 절은 그 기간의 결과와 근거 문서만 적는다.

- **보고서 9건 텍스트 분석** (`internal/analysis/REPORT_TEXT_REVIEW.md`, 2026-10-26. 대상: §9.16의 9건, 근거·캡션과 대조, 영상은 보지 않음)
  - 형식(섹션 상한, 결론, 인용 번호)은 9/9 지켰고, 인용한 근거를 그대로 옮긴 사실 서술은 대체로 근거와 맞는다.
  - 문제 빈도(9건 중): 큰 구간(10분 이상) 누락 9/9, 결말 오류 4/9, 구간 요약의 "the video closes/opens"를 본문에서 영상 전체처럼 씀 6/9, 섹션 안 시간 역행 6/9, 시각 잘못 붙임 4/9, 같은 보고서 안 사실 불일치 6/9, 섹션 사이 반복 7/9, writer 반복 루프 2/9, 결론의 새 사실 4/9. 해석·서사 덧씌우기는 뉴스 영상 3/3, 로마 영상 3/3.
  - 확인된 원인 C1–C13(입력 자료·planning·섹션 단위 독립 검색·작성·후처리의 네 층), 확인하지 못한 원인 H1–H7(GPU 비교 실행 필요).
- **같은 조건 3회의 실행 간 차이** (`internal/analysis/SELF_CONSISTENCY_ANALYSIS.md`, `SELF_CONSISTENCY_CAUSES.md`, 2026-10-26)
  - 형식과 핵심 주체는 3회가 같고, 다루는 구간은 크게 다르다: 3회가 모두 다룬 3분 구간 13개 중 3(`-QuCz7kxBr8`), 11개 중 4(`0RxMZBLeqRI`), 16개 중 8(`54k2g9ddy4M`). 실행 쌍의 episodic 근거 Jaccard 0.19–0.41.
  - 결말 정답 5/9(`0RxMZBLeqRI` 3/3, `-QuCz7kxBr8` 1/3, `54k2g9ddy4M` 1/3). 맞은 5건은 모두 planner가 결말 구간을 섹션이나 checklist에 넣은 경우이고, 틀린 4건은 planner가 틀린 결말을 checklist에 적었거나(`54k2g9ddy4M` r1·r3) 결론 근거에 끝부분이 없었다(`-QuCz7kxBr8` r2·r3, `SELF_CONSISTENCY_CAUSES.md` §4).
  - 차이는 같은 입력에 대한 planner 출력(샘플링, seed 없음)에서 시작해 query·검색·본문으로 커진다. 원인 분리 실험 E1–E4(GPU 필요)는 `SELF_CONSISTENCY_CAUSES.md` §5.
- **흐름 오류·추측 표현 측정**: §9.17.
- **단계별 원문과 running example**
  - `analysis/export_stages.py` → `internal/inspect/<run>/`: 9건의 planner·query·writer 프롬프트와 원문, 근거, 후처리 결과(후처리 재실행이 `report.md`를 그대로 재현함을 확인).
  - `internal/running_example/RUNNING_EXAMPLE.md`(2026-11-02–03): 영상 3개 r1의 단계별 실제 입력·출력. §10은 농구 영상 심층 자료다. 사전 구축 메모리의 실제 내용으로 semantic 추출 23묶음 중 11묶음이 0개(로그의 실패 응답 36건 중 35건이 출력 2,048토큰에서 끊긴 JSON), 검색에 쓰이는 semantic triple 153개, 10sec OpenIE triple이 0개인 캡션 18/226개를 확인했다.
  - CPU 검색 재현(`analysis/reproduce_retrieval_cpu.py`, 결과 `results/retrieval_repro_-QuCz7kxBr8_r1.json`): 섹션별로 실행 기록과 맞춰 보고 맞은 항목만 싣는다. 2026-11-10 대조 실험에서 같은 코드·데이터로도 일치 항목이 실행마다 달라짐을 확인했다(`internal/status/REORG_LOG_20261110.md` §9).
  - visual 임베딩은 구간당 10프레임으로 만들어졌다: 저장된 벡터와의 cosine이 10프레임 재계산 0.9965–0.9987, 16프레임 0.887–0.953(구간 4개, `analysis/verify_visual_nframes.py`, `results/visual_nframes_check_-QuCz7kxBr8.json`).
  - 미팅 구성안: `internal/meetings/MEETING_ISSUES_DECK_PLAN.md`(이슈 ①–⑧, 원인 지도).
- **코드·폴더 정리** (2026-11-10–12, `internal/status/REORG_LOG_20261110.md`, 동작 변경 없음은 CPU로 확인)
  - WorldMM 메모리와 사전 인덱스를 `WorldMM/output/memory/videomme_long_qwen3vl-8b/`로 옮겼다(복사, md5 동일). 설정 경로는 `report_framework/` 기준 상대 경로(`rf_config.py`).
  - 폴더 재배치: `tests/{unit,gpu,fixtures}`, `experiments/`, `scripts/{launch,memory_build}`, `results/`, `docs/`, `internal/`. 새 clone에서 CPU 테스트 6종 통과.
  - 2026-11-12: References를 번호마다 문단으로 나눔, 한국어 번역 기본 off(`report.translate_ko`), CPU 테스트 실패 시 종료 코드 1, 추적 파일에서 사용자명 제거.
- 품질 평가(Video-MME 문항 풀이, 자동 지표, 사람 검수)는 아직 시작하지 않았다.

---

## 3. 실행 환경 사실 (✔)

| 항목 | 사실 |
|---|---|
| 컨테이너 기본 venv | **`/opt/venv`** (Docker 이미지에 구워져 있음). `PATH`, `VIRTUAL_ENV`, `UV_PROJECT_ENVIRONMENT`가 모두 `/opt/venv`를 가리킨다. Python 3.13.9 |
| `/opt/venv` 내용 | torch 2.8.0+cu128, transformers 4.57.6, flash_attn 2.8.3, sentence-transformers 5.3.0, decord 0.6.0, igraph 1.0.0, flask 3.1.3, langgraph 1.2.16, langchain-core 1.6.12, langchain-openai 1.4.3, openai 2.54.0, qwen-vl-utils 0.0.14 |
| `/opt/venv`의 editable 설치 | worldmm → `VideoRAG/WorldMM/src`, hipporag → `VideoRAG/WorldMM/src/HippoRAG/src`, merit → `VideoRAG/MERIT/src` (모두 올바른 경로) |
| `PYTHONPATH` | `/data1/USER/workspace/VideoRAG/Deep-Report` (`deep_reporter` 패키지를 import할 수 있음) |
| `WorldMM/.venv` | 9월에 만든 예전 venv. 이름 변경 전 경로(`VAU_RAG`)를 가리키던 문제를 2026-10-21 15:47에 수리했다(§10). Deep-Reporter 의존성(langgraph 등)과 merit는 없다 |
| HF 모델 캐시 (**2026-10-25 정정**) | 컨테이너 환경변수는 `HF_HOME=/data1/USER/workspace/VideoRAG/.cache/huggingface`와 **`HUGGINGFACE_HUB_CACHE=/data1/USER/workspace/VideoRAG/.cache/huggingface/hub`** 두 개다(Makefile `docker-run`의 `-e`). `huggingface_hub`는 모델 저장 위치를 `HF_HUB_CACHE` → `HUGGINGFACE_HUB_CACHE` → `$HF_HOME/hub` 순서로 정하므로(`huggingface_hub/constants.py:129-155`, 0.36.2), 우리 스크립트가 `HF_HOME`을 `paths.hf_home`으로 바꿔도 **모델 저장 위치는 바뀌지 않는다**(✔ 실험: `HF_HOME` 변경 후 `HF_HUB_CACHE`가 그대로 `VideoRAG/.cache/huggingface/hub`). 경위: 2026-10-21 15:36 확인 때 `VideoRAG/.cache/huggingface/hub`에는 모델이 없었고(I4), 16:24–16:31 GPU 스모크(§9.2)와 LLM 서버가 모델을 그 위치에 내려받았다(근거: `.locks/` 생성 시각 16:26–16:31, Qwen3-VL-8B blob 16:28:41–16:31:14, 첫 Qwen3-Embedding 로드 90초 → 두 번째 15초). 그 뒤 모든 실제 모델 실행은 이 위치의 모델을 썼다. 모델 4개(`Qwen3-VL-8B-Instruct`, `Qwen3-Embedding-4B`, `VLM2Vec-V2.0`, `Qwen2-VL-2B-Instruct`)는 `/data1/USER/workspace/.cache/huggingface/hub`에도 있고 snapshot 해시·바이트 수가 같다(✔ 2026-10-23). 로그의 `HF_HOME=...` 표시(`local_llm_server.py`)는 실제 저장 위치가 아니다 |
| vLLM | `/opt/venv`, `WorldMM/.venv` 어디에도 설치돼 있지 않다 |
| GPU | A6000 48GB(49,140 MiB) × 8. 2026-10-22 사용 이력: GPU 4–7(20,000 MiB 규칙) → 중지 지시 → GPU 4–7 전부 사용 허용(20,000 MiB 규칙 해제, 12:04 실행) → "다른 사용자 프로세스를 침범하지 않는 여유 메모리 안에서"(12:41 실험) → **GPU 6·7만**(14:10 실행, 16:05 대기 실행). 다른 사용자 사용량 관측: §9.8 시점 GPU 6 약 18–30GB, GPU 7 약 18–34GB, §9.9(18:15–00:05) 10분 최대값 GPU 6 30.4–38.2GB, GPU 7 28.5–39.2GB. **2026-10-25: GPU 4–7 사용 가능**(사용자 지시, 11:44 확인 시 GPU 0–7 모두 0–3 MiB) |
| CPU | 8코어 (`nproc`). OpenIE의 `ThreadPoolExecutor` 기본 동시성은 min(32, 8+4) = 12 |
| 검색 도구 주의 | 셸의 `grep`은 ignore 파일을 따르는 래퍼라 `.venv` 내부(`.gitignore=*`) 등을 건너뛴다. 전수 검사에는 `/usr/bin/grep`을 쓴다 |

---

## 4. 구성요소 분석 요약

### 4.1 WorldMM (CVPR 2026, arXiv 2512.02425)

**메모리 3종과 검색 방식** (✔ 코드)

| 메모리 | 구축 | 검색 | 검색 시 LLM |
|---|---|---|---|
| Episodic | 10sec 캡션(프레임+Whisper 자막) → LLM 요약으로 30sec/3min/10min 생성 | granularity마다 HippoRAG 그래프 → fact 점수 → DSPy fact 필터(LLM) → PPR → `multiscale_filter`(LLM) | 쿼리당 최대 5회 (§5.1) |
| Semantic | 10sec OpenIE triple을 10개씩 묶어 semantic triple 추출 → 임베딩 유사도 ≥0.6인 것끼리 LLM consolidation | 마지막 snapshot으로 igraph 구성, PPR, triple 점수 = 주어 PPR + 목적어 PPR | 0 |
| Visual | VLM2Vec-V2로 10초 구간 비디오 임베딩 (Video-MME, 키=`start_time`) | 텍스트 질의 cosine top-k → 구간 프레임. 또는 `DAY X HH:MM:SS - …` 시간 범위 질의 | 0 |

**추론 루프** (`memory.py:408`): 매 라운드 respond LLM이 `search`(메모리 종류 + 질의) 또는 `answer`를 결정한다. 최대 5라운드 후 MCQ 답을 생성한다.

**코드에서 확인한 주의점** (✔)
- 아이템 단위 검색은 하위 메모리 객체를 직접 써야 한다.
  - `episodic_memory.retrieve(as_context=False)` → `List[CaptionEntry]` (id, text, start/end_time, date, granularity, video_path). **점수 없음**.
  - `semantic_memory.retrieve(as_context=False)` → `List[SemanticTripleEntry]`. **점수 없음**.
  - `visual_memory.retrieve(as_context=False)` (텍스트 질의) → `List[VideoClipEntry]` (id, video_path, clip_start_sec, clip_end_sec, start_time). **점수는 버려짐** (`visual/memory.py:389-391`).
  - `as_context=True`는 `{표시용 시간 문자열: [PIL]}`만 반환해 클립 정보가 사라진다.
- `WorldMemory.retrieve_from_*`는 에이전트 QA용으로 결과를 합친 문자열이나 dict를 반환한다.
- QA 단계에서 visual 결과는 **타임스탬프 라벨 없이 이미지만** 들어간다(`memory.py:248-272`). 추론 LLM은 visual 결과를 `"[N images from M clips]"` 문자열로만 본다(`memory.py:522`).
- Semantic triple에는 **시간 근거가 없다**. `consolidate_semantic_memory.py`가 evidence를 `[[] for _ in current_triples]`로 버리고, `SemanticTripleEntry.timestamp`는 snapshot 키일 뿐이다.
- Visual의 시간 범위 질의는 `until_time` 인덱스가 아니라 `self.clips` 전체를 대상으로 한다.
- 캡션 JSON의 `video_path`는 상대경로(`data/Video-MME/data/X.mp4`, WorldMM 루트 기준)다.
- preprocess가 만든 `episodic_triple_results_*.json`은 eval에서 읽지 않는다. `openie_results_*.json`만 semantic 추출의 입력이 된다.
- WorldMM에는 로컬 수정이 있다(`git diff`): `qwen3vl.py`(생성 lock 추가, JSON 파싱 보강), `multiscale.py`(LLM 1회 로드, worker 1개), `script/4_eval.sh`·`script/videomme/4_eval.sh`(모델명 `qwen3vl`). 이 중 **`qwen3vl`은 `MODEL_DICT` 키(`qwen3vl-2b/4b/8b`)가 아니어서 기본값으로 실행하면 `ValueError`가 난다**. `eval.py`는 semantic 파일을 `semantic_consolidation_results_{retriever_model}.json`으로 찾으므로 `--retriever-model qwen3vl-8b`로 실행해야 한다.
- `Qwen3VLModel`은 `max_retries=3`, 기본 `max_new_tokens=2048`이고, 구조화 응답을 `_parse_structured_response`로 파싱한다(코드블록 제거, 첫 JSON 값만 디코드, 필드가 1개인 스키마의 bare 배열은 그 필드로 감쌈). OpenIE는 그 위에 별도 재시도(기본 5회)를 건다.

**구축된 데이터** (✔): `WorldMM/claude_output/full/` (2026-11-10부터 사본 `WorldMM/output/memory/videomme_long_qwen3vl-8b/`를 쓴다. 목록은 `lists/`, 진행 표식은 `build_state/` 아래로 옮겼다)
- 50개 영상 모두 캡션 4종, `episodic_memory/openie_results_qwen3vl-8b.json`, `semantic_consolidation_results_qwen3vl-8b.json`, `visual_embeddings.pkl`을 갖췄다. `done/` 표식 50개, `failed/` 비어 있음.
- Video-MME `test.json`은 2,700행이고, 그중 이 50개 영상의 QA는 150문항(영상당 3문항)이다.

| 캡션 통계 (50개 영상) | 10sec | 30sec | 3min | 10min |
|---|---|---|---|---|
| 영상당 항목 수 (평균) | 251.0 | 84.0 | 14.5 | 4.6 |
| 단어 수 평균 / 최댓값 | 75 / 1,855 | 153 / 1,522 | 292 / 849 | 940 / 1,630 |

- **10min 캡션 잘림** (✔ 실측·코드, `REPORT_ISSUES_AND_FIXES.md` I22): 10min 캡션 232개 중 32개(영상 20개)가 정확히 2,048토큰이고 30개는 문장 중간에서 끝난다. 30sec 1개, 10sec 2개도 2,048토큰이다. 전처리 multiscale(`process_one_video.sh:26`, `--model qwen3vl-8b`)이 `gen_multiscale._summarize_batch`에서 `max_new_tokens` 없이 `llm.generate`를 불러 `Qwen3VLModel` 기본값 2,048이 적용됐기 때문이다. 10min 캡션은 episodic 10min 인덱스, planner 개요, 검색 근거에만 쓰이고, `build_memory.py`의 episodic·semantic·visual 단계는 10sec만 읽는다.

**논문 수치** (✔ 논문 원문): Video-MME(Long) 정확도는 WorldMM-8B 66.0, WorldMM-GPT 76.6이다. Video-MME 설정은 granularity 10s/30s/3m/10m, semantic consolidation 임계값 0.6, semantic top-10, 최대 5라운드다.

**기존 pilot 기록** (◇ `WorldMM/claude_output/REPORT.md`)
- 8개 영상, 24문항의 보정 결과가 12/24 = 50.0%로 기록돼 있다.
- eval 시 episodic 재인덱싱이 영상당 약 30–50분, eval 프로세스가 GPU 약 44GB를 쓴다고 기록돼 있다.

### 4.2 MERIT (ECCV 2026, arXiv 2608.07663) — 아직 통합하지 않음

- **메모리**: 30초 클립의 dense caption마다 키 4개(event, dialogue, object, summary)를 붙인 flat key–value 구조. 검색은 Qwen3-Embedding-4B로 임베딩한 키들과의 cosine 중 최댓값(MaxSim)으로 top-N(기본 10)을 고른다. 검색 자체에 LLM은 쓰지 않는다(✔).
- **추론**: 라운드마다 LLM 2회(결정 1, neighbor filter 1)와 최종 QA 1회. Neighbor filtering은 검색된 클립 앞뒤 ±2 클립 캡션을 LLM이 한 번에 요약한다(✔ 코드·논문).
- **최종 QA 프레임 수**: 1라운드는 클립당 6장, 2라운드는 상위 5개 클립만 6장, 3라운드부터는 1장(`merit_memory.py:182`, 논문 부록 A).
- **논문 수치**: Video-MME(L) GPT-5 77.7. 같은 30초 캡션 기준으로 WorldMM 대비 메모리 구축 입력 토큰 8.4배, 출력 토큰 8.6배 절감. Neighbor filtering ablation(Table 3)에서 성능 차이가 크다.
- **통합 시 주의점** (✔)
  - core `MeritMemory._extract_frames_from_video`는 **파일 전체**에서 균등 샘플링한다(`merit_memory.py:154`). Video-MME처럼 영상이 mp4 하나면 클립 구간이 아니라 영상 전체에서 프레임을 뽑는다.
  - core `MultiKeyMemory`의 임베딩 캐시 파일명(`{cache_dir}/30sec_{key}_key_embeddings.pt`)에 영상 구분이 없다. 영상별 `cache_dir`을 지정하지 않으면 행 수만 같은 다른 영상의 캐시를 불러올 수 있다.
  - `MultiKeyMemory.index(until_time)`는 전체를 임베딩하고, 시간 필터는 `retrieve(until_time=…)`에서 한다.
  - Video-MME용 `*_4_key.json`은 로컬에 없다. WorldMM의 `30sec.json`은 10sec 캡션 3개를 LLM으로 요약한 것이라 논문의 "30초 클립 dense caption" 설정과 다르다.
  - `benchmarks/videomme` 변형은 시간 형식이 `HHMMSS`이고, 미리 뽑은 프레임 디렉터리를 사용한다.

### 4.3 Deep-Reporter (arXiv 2604.10741, `Deep-Report/`)

- **LangGraph 흐름**: `planner → query_generation → search → (filter) → section_writing →` 남은 섹션이 있으면 `query_generation`으로, 없으면 `combine` (`core/graph.py`). 그래프 실행 `recursion_limit=50`(`api.py:105`).
- **생성 뒤 보고서 전체를 다듬는 refine/polishing 단계는 없다** (✔ 코드·논문). `combine_node`는 섹션을 `"\n\n"`으로 이어 붙이기만 한다. 논문의 "refine"은 근거 필터링, outline을 사람이 다듬는 선택 사항, 벤치마크용 전문가 참조 보고서를 뜻한다. 반복은 평가 지표(`S_Rep`)로만 다룬다.
- **Search 계약** (✔)
  - 요청: `POST retriever_url {query_list, type: text|image, topk}`. 응답 `status=="success"`일 때 `results`를 그대로 저장하고 `img_base64`만 지운다(`search_node.py:97`).
  - HTTP 타임아웃은 600초이고, 예외가 나면 빈 결과로 계속 진행한다. text 요청과 image 요청 사이에 2초 대기한다(`search_node.py:74`).
  - 원래 retriever는 모든 query의 hit을 합친 뒤 전체에서 topk만 남긴다(`retriever_app.py:717`).
- **Writer 입력** (✔)
  - text: `content`, 없으면 `text`.
  - image: `caption`, 없으면 `description`, 둘 다 없으면 `'Image'`. **키가 없을 때만** 대체되고 빈 문자열은 그대로 들어간다.
  - 근거 형식 `[Source txtN begin]…`, `[Source imgN: …]`은 **노드 코드**가 만든다(`section_writing_node.py:59`).
  - Writer는 **텍스트만** 받는다. `LLMCaller`가 user 메시지 텍스트만 전달한다(`llm_utils.py:36`).
- **인용**: 섹션 단위 `[citation:txtN]`, `![](citation:imgN)`. 최종 반환값의 `outline[i]`에 `retrieved_texts/images`와 `content`가 들어 있다.
- **Recurrent context** (✔ 코드·실측): 논문은 `m_global`을 "recursive summary"라고 하지만, 코드의 `_update_context`(`section_writing_node.py:214`)는 LLM을 쓰지 않는 휴리스틱이다.
  - 요약: `Section: <planner 섹션 설명>` + `Content: <본문 앞 100자>`. 2,000자를 넘으면 앞쪽 섹션은 첫 줄(섹션 설명)만 남긴다.
  - tail: 본문을 `.`으로 나눈 마지막 3조각.
  - 본문 앞 100자는 대부분 제목 줄이라, 다음 섹션은 앞 섹션에서 실제로 쓴 사실을 거의 받지 못한다(보고서 B로 복원해 확인, `ANALYSIS_D4_D7.md` §1.2).
  - 이 요약은 query 생성과 writer 프롬프트에 함께 들어간다.
- **LLM 라우팅** (✔ 실측)
  - 모델명에 `deepseek`가 있으면 DEEPSEEK 설정, `gpt`가 있으면 OPENAI 설정, 그 외는 QWEN 설정(`qwen_api_key`/`qwen_base_url`)을 쓴다.
  - 이름에 `qwen`이 있고 base_url이 localhost/127.0.0.1/0.0.0.0/:8000이면 `extra_body={"chat_template_kwargs":{"enable_thinking":False}}`를 붙인다.
  - Deep-Reporter는 temperature를 보내지 않는다. 그래서 로컬 서버에서는 모델 기본 생성 설정(Qwen3-VL-8B: `do_sample=true`, temperature 0.7, top_p 0.8, top_k 20, repetition_penalty 1.0)으로 샘플링된다. 결과는 실행마다 달라진다.
- **설정 dict의 함정** (✔ 실측)
  - `BaseConfig.from_dict`는 `hasattr(cls, k)`로 키를 거른다. `default_factory`로 선언된 필드는 클래스 속성이 아니라서 걸러진다.
  - 거부되는 키: `openai_api_key`, `openai_base_url`, `qwen_api_key`, `qwen_base_url`, `auxiliary_*`.
  - **키와 URL은 환경변수로만 넣을 수 있고, `create_openai_api()` 호출 전에 설정해야 한다.**
  - `retriever_url`은 config가 아니라 `generate_article(retriever_url=…)` 인자로 전달된다.
- **조용한 실패** (✔)
  - LLM 호출 실패 시 예외 없이 `"Call failed: …"` 문자열을 반환한다(`llm_utils.py:82`).
  - planner JSON 파싱이 실패하면 섹션 1개(설명 = query)로 대체하고, query 파싱이 실패하면 섹션 설명을 검색어로 쓴다.
  - Writer 예외가 나면 본문에 `"[Section generation failed: …]"`가 들어간다.
  - 위 경우들은 `success=True`로 끝날 수 있다.
  - 섹션이 16개 이상이면 `GraphRecursionError`로 `success=False`, outline 0개가 되어 보고서 전체가 사라진다(가짜 LLM으로 실측, 15개는 성공).
- **import 순서** (✔ 실측)
  - `deep_reporter.nodes`를 먼저 import하면 순환 import로 `ImportError`가 난다. `deep_reporter.api`를 먼저 import해야 한다.
  - `import deep_reporter.nodes.section_writing_node as sw`는 `nodes/__init__.py`가 이름을 함수로 다시 묶어 두어서 함수 객체가 잡힌다. 모듈이 필요하면 `sys.modules["deep_reporter.nodes.section_writing_node"]`를 쓴다.
- **템플릿 계약** (✔ AST 실측). 노드는 모듈 전역 변수를 호출 시점마다 읽는다.

  | 노드 | 템플릿 | `.format()` 키 |
  |---|---|---|
  | `planner_node` | `OUTLINE_GENERATION_TEMPLATE` | `overall_query`, `overall_checklist` |
  | `query_generation_node` | `QUERY_GENERATION_TEMPLATE` | 위 2개 + `previous_sections_summary`, `section_description`, `sectional_checklist` |
  | `section_writing_node` | `SECTION_WRITING_TEMPLATE` | 위 5개 + `previous_section_tail`, `retrieved_materials`, `position_info`, `is_first_section`, `is_last_section` |

- **웹 도메인 전제**: 원래 image query 지시는 "diagrams, charts, figures, or visualizations"이고, writer 프롬프트에는 타임스탬프나 관찰 사실 위주 서술 지시가 없다.
- **논문 사실** (✔)
  - 실험에서는 planner를 끄고 고정 checklist를 썼다(B.2).
  - Filter를 제거하면 Section Content가 41.7에서 27.6으로, recurrent context를 제거하면 Full Report가 32.3에서 19.8로 떨어졌다(Qwen3-32B SFT).
  - Filter가 전체 지연의 약 70%를 차지한다.

---

## 5. 핵심 분석 결과

### 5.1 WorldMM episodic 검색의 LLM 호출 수 (✔)

```
episodic_memory.retrieve(query)                          episodic/memory.py:247
 ├ for g in [10sec, 30sec, 3min, 10min]:                 그래프 4개
 │    hipporag[g].retrieve([query])                      HippoRAG.py:327
 │      ├ get_fact_scores (임베딩 내적)                   LLM 없음
 │      ├ rerank_facts → DSPyFilter.llm_call             ★ LLM 1회 (rerank.py:95)
 │      └ graph_search_with_fact_entities (PPR)          LLM 없음
 └ _filter_with_llm (후보 > final_top_k이면 항상)         ★ LLM 1회 (episodic/memory.py:398)
```

- 쿼리당 최대 5회다. HippoRAG에서 LLM을 부르는 곳은 OpenIE(인덱싱)와 `rerank_filter`(검색) 두 곳뿐이다.
- 필터 후보: granularity별 기본 top-k는 10sec 5(dict에 없어 기본값) / 30sec 10 / 3min 5 / 10min 5. 10min 항목이 영상당 4–6개라 실제 후보는 약 24개다.
- 필터 입력: 캡션 평균 길이로 계산하면 약 7,700단어다.
- Deep-Reporter의 섹션당 text query 3–5개에 그대로 연결하면 섹션당 15–25회가 든다.
- 실측: granularity가 10sec 1개뿐인 full 모드에서 질의 2개에 LLM 4회(질의당 DSPy 1 + multiscale 1)였다(§9.4).

### 5.2 Episodic 인덱싱 비용과 캐시 (✔)

- `HippoRAG.index`는 새 청크마다 NER 1회와 triple 1회, LLM 2회를 부른다.
- HippoRAG는 OpenIE JSON, embedding parquet(이미 있는 hash는 건너뜀), `graph.pickle`을 디스크에 저장하고 재사용한다. `force_*_from_scratch`의 기본값은 False다. 따라서 **오프라인에서 한 번 사전 인덱싱하면 서비스 시작 시 LLM 호출은 0회**다.
- **10sec OpenIE 재사용**
  - 전처리 결과 `metadata/episodic_memory/{vid}/openie_results_qwen3vl-8b.json`이 10sec 캡션 **12,551개 전부**를 덮는다.
  - 해시 방식(`"chunk-"+md5(text)`), OpenIE 클래스(HippoRAG가 `worldmm.memory.episodic.openie.OpenIE`를 import), 모델(qwen3vl-8b)이 모두 같다.
  - triple이 빈 항목이 1,252개(영상당 약 25개) 있다. 오류였는지 구분할 수 없어 시드에 넣지 않고 다시 계산하게 한다.
- **계획된 호출 수** (✔ dry-run, 빈 캐시 기준): 50개 영상 총 12,818회(영상당 평균 256회). **긴 청크 분할(§8.3)을 적용하면 13,424회**(10sec 2,504 / 30sec 8,410 / 3min 1,446 / 10min 1,064. 분할 청크 150개(10min 149, 30sec 1), 조각 453개, +606회). 현재 캐시 상태 기준으로는 13,044회다. 10sec를 시드로 넣지 않으면 약 35,400회다.
- **캐시 라벨 문제**: `EpisodicMemory._get_or_create_hipporag`가 `global_config`를 넘기지 않아 HippoRAG `llm_name`이 기본값 `gpt-5-mini`로 남는다. 디렉터리는 `gpt-5-mini_Qwen_Qwen3-Embedding-4B/`, 파일은 `openie_results_ner_gpt-5-mini.json`이 된다(pilot 캐시에서 실물 확인). 신규 코드의 `LabeledEpisodicMemory`로 해결했다(§8.3).
- **OpenIE 오류 처리**: HippoRAG/WorldMM OpenIE는 재시도가 소진되면 예외를 삼키고 빈 결과를 반환하며, 그 결과도 캐시에 저장된다. 그래서 캐시 키가 있다고 해서 내용이 정상이라는 보장은 없다(시험 인덱싱에서 2건 확인, §9.5). 완료 표식에 단위별 빈 triple·빈 entity 수를 기록한다(§8.3).
- **그래프 재저장 조건** (✔ 코드 `HippoRAG.index`): 새 passage 노드가 생길 때만 그래프를 다시 저장한다. 그래서 OpenIE 캐시 파일만 지우고 다시 인덱싱하면 옛 triple이 그래프에 남는다. **캐시를 다시 만들 때는 그 granularity 폴더 전체(OpenIE 파일, 임베딩, `graph.pickle`)를 지운다.**

### 5.2.1 긴 passage의 OpenIE 출력 상한 문제 (✔ 실측, 상세 `REPORT_ISSUES_AND_FIXES.md` I23·I24)

- 2026-10-22 3영상 실행(§9.6)에서 10sec·30sec·3min 호출 333회는 잘림 0건(입력 최대 1,025토큰)이었다. 10min에서는 영상 1이 9회 중 1회, 영상 2가 18회 중 12회 출력 상한(2,048토큰)에 걸렸다. 실패 응답 14건은 모두 JSON이 중간에 끊긴 형태다.
- 유형: (M1) 같은 (주어, 술어)에 목적어만 바꿔 39–115회 나열하는 **열거 폭주**, (M2) 반복은 없지만 triple이 87–122개라 길어지는 **정상인데 긴 출력**.
- 잘린 JSON은 파서가 통째로 버리고, WorldMM `OpenIE`(데코레이터 기본 5회) × 클라이언트(3회)로 **청크당 최대 15회** 재시도한다. 모두 실패하면 빈 triple이 저장된다. in-process 경로도 같은 설정이라 HTTP 방식 고유의 문제가 아니다.
- 디코딩 설정 변경(반복 억제)은 실험(§9.7)에서 효과가 없거나 원인 불명의 이상이 있어 기각했다. 입력을 줄이는 **분할 OpenIE**와, 안전장치로 **응답 구제·폭주 절단**을 채택했다(§8.3).

### 5.2.2 50개 영상 사전 인덱싱 소요 시간 추정 (2026-10-22, (추정))

**입력 (✔ 실측)**
- 호출 수(빈 캐시, 분할 포함 dry-run): 10sec 2,504 / 30sec 8,410 / 3min 1,446 / 10min 1,064, 합계 **13,424회**. 10min은 조각 449개(평균 543토큰, 최대 700)와 분할하지 않는 청크 83개(평균 691토큰)다.
- 호출당 출력 토큰 평균(서버 로그): 10sec 재계산 20–86(§9.6 영상 2 / §9.5 시험 실행), 30sec 228–278, 3min 373–398, 10min 873(분할 전, 영상 1). 10min 조각은 입력 크기가 3min과 비슷해 3min 수준(373–500)으로 가정했다(가정).
- → 총 출력 **약 290만–370만 토큰**.
- 처리 속도
  - LLM 서버 7개(GPU 4,4,5,5,6,6,7, 다른 사용자 없음, 동시성 12): 단계 전체 합산 68–91토큰/초, 호출 기준 3.55–3.66초/호출(영상 1 188회 668초, 영상 2 10sec–3min 154회 563초). 단위 끝부분에 긴 응답 몇 개만 남아 GPU가 노는 구간이 포함된 값이다.
  - 서버 1개가 GPU를 혼자 쓸 때: 출력 300토큰 이상 호출 기준 17–24토큰/초(보고서 A·B 실행 로그). 요청은 한 번에 하나씩 처리된다.
  - 서버 1개가 다른 사용자와 GPU를 같이 쓸 때(상대 사용률 100%): 약 8.6토큰/초(§9.7 실험).

**추정 (LLM 생성 시간 기준. 임베딩·그래프 저장은 영상당 수십 초 수준으로 보이나 따로 재지 않았다)**

| 배치 | 근거 | 50개 영상 | 영상 3개(430회) |
|---|---|---|---|
| LLM 서버 7개, GPU 4개 단독 사용 (§9.6 배치) | 호출 기준 3.55–3.66초 / 토큰 기준 68–91토큰/초 | **약 13시간** (토큰 기준 9–15시간) | 약 25–30분 |
| 서버 2개, GPU 2개 단독(GPU 6·7이 비어 있을 때) | 서버 1개 속도 × 2 | 약 17–30시간 | 약 1시간 |
| 서버 1개, GPU 단독 | 17–24토큰/초 | 약 34–60시간 | 약 1.5–2시간 |
| 서버 1개, 다른 사용자와 공유 | 약 8.6토큰/초 | 약 94–120시간 (4–5일) | 약 4시간 |

- 영상 3개 행은 430회 × 평균 출력 약 300토큰(가정)으로 계산했다.
- **GPU 메모리**: LLM 서버 1개 17.4–18.8GB(실측). 인덱서는 §9.6에서 GPU 7 최대 35,782 MiB − 서버 약 18GB ≈ 18GB까지 잡았다(상한 26,000 MiB, 할당자 캐시 포함). §9.8에서는 15,000 MiB 상한으로 시작 41초 동안 약 8GB였다. 15,000 MiB 상한으로 끝까지 돌 수 있는지는 확인하지 않았다.
- **줄이는 방법**
  - 서버를 GPU당 2개 두는 것은 §9.6에서 동작했다(GPU당 최대 36.7–37.2GB).
  - vLLM은 한 서버가 여러 요청을 묶어 처리하므로 이 작업에 유리할 것으로 보지만, 설치돼 있지 않고 측정하지 않았다(§11).
  - 다른 사용자와 GPU를 같이 쓰면 생성 속도가 절반 이하로 떨어진다(24 → 8.6토큰/초).
- **기존 캐시**: pilot 8개 영상에만 있다(`WorldMM/claude_output/pilot/eval_cache`, 합계 145MB, 영상 1개 약 25MB). 50개 중 겹치는 것은 `0w4OTD4L0GQ` 1개다.

### 5.3 기존 설계 문서 검토 결과 (C1–C9)

| ID | 내용 | 반영 |
|---|---|---|
| C1 | "`openai_base_url`만 바꾸면 로컬 전환"은 틀림 (라우팅은 모델명 기준, 키·URL은 env로만 가능). 실측으로 `Missing credentials` 오류 확인 | D4, `run_report.py`의 env 설정과 라우팅 확인 |
| C2 | "score로 병합·정렬"은 WorldMM에서 불가능 (점수를 반환하지 않고, 출처별 점수 척도도 다름) | 순위 기반 병합(RRF) |
| C3 | MERIT 프레임 함수 재사용은 Video-MME에서 오류. visual은 `as_context=False`를 써야 함. 상대경로 문제 | 구간 중앙 프레임 직접 추출, 절대경로 변환 |
| C4 | Semantic에는 시간 근거가 없음 | "video-level knowledge"로 표기, 시간·프레임 미부여 |
| C5 | 검색 LLM 비용 과소평가, 사전 인덱싱 누락 | L1 + 오프라인 사전 인덱싱 |
| C6 | 조용한 실패 (`Call failed`, 섹션 실패 문자열, 검색 0건) | `run_report.py` 사전 확인·사후 검증 |
| C7 | 프롬프트가 웹 도메인 기준, 관제 템플릿과 Video-MME 불일치 | 범위 한정 템플릿 교체 + videomme 템플릿 |
| C8 | MERIT backend 세부 오류 (캐시 충돌 등, §4.2) | MERIT 추가 시 반영 |
| C9 | 후처리기 명세 부족 | `grounding_postprocessor.py` |

기존 문서의 사실 오류(정정 완료)
- `format_with_time()`, `TripleEntry.format()`, `ClipEntry`는 존재하지 않는다. 실제 이름은 `to_display_str()`, `SemanticTripleEntry`, `VideoClipEntry`다.
- Visual은 "프레임 임베딩"이 아니라 10초 구간 비디오 임베딩이다.
- Writer는 `ChatOpenAI`가 아니라 `ReasoningOpenAI`다.
- "쿼리당 LLM 1회"가 아니라 최대 5회다.
- 경로는 `VAU_RAG`가 아니라 `VideoRAG`다.

### 5.4 작업 중 Claude가 정정한 자신의 진술

| 처음 진술 | 정정 |
|---|---|
| "`failed/`에 3개가 있다" | 실제로는 비어 있다. 그 3개 ID는 같은 명령에서 출력된 `claims/` 목록이었다 |
| `WorldMM/.venv`가 실행 환경이라 보고 flask를 설치 | 실제 기본 환경은 `/opt/venv`다. 설치는 해롭지 않아 사용자 지시로 유지한다 |
| 검색 기본값 L0(LLM 0회) 제안 | Deep-Reporter 논문의 filter ablation 근거로 L1로 수정, 사용자가 확정 |
| "텍스트 인용 109개가 모두 범위 안"을 근거 정확성처럼 보고 | 인용 **번호**가 유효하다는 뜻이었다. 근거 원문과 대조하자 내용 오류가 있었다(`REPORT_ISSUES_AND_FIXES.md` P3) |
| 섹션 수 한계 "16개"(계산값) | 실측 결과 15개까지 성공, 16개부터 보고서 전체 소실 |
| writer 시간 "36–60초"(섹션 1–3 로그만 봄) | 로그 16건 전체 기준 35.7–66.5초(출력 614–1,121토큰) |
| 반복 단락 유사도 "0.71" | 인용 표기를 포함한 원문으로 잰 값(0.711). 정규화해서 재면 같은 쌍이 0.901이다. 두 값 모두 문서에 측정 방식과 함께 적었다 |
| 부정문 처리 첫 구현(문장 전체 제외) | 실제 오류 `3/16`, `WOO`를 놓쳐서 절 단위 제외로 고쳤다(§8.7) |
| `test_report_pipeline.py` 통과 항목 "68개" | "RESULT" 줄까지 센 값이었다. 실제 통과 항목은 67개다 |
| 3영상 실행 중 "서버 호출 374건" | `grep "chat.completions"`의 `.`이 `/`와도 맞아 접근 로그까지 셌다. 실제 187건이다 |
| OpenIE 실패 응답 "13건" | 분석 스크립트가 로그 끝의 마지막 응답에서 멈춰 1건이 빠졌다. 14건이다(테스트 작성 중 발견) |
| 디코딩 실험 base의 "정상인데 긴 출력 5건" | 4건이다(잘린 5건 중 1건은 폭주) |
| "base 호출의 44%가 상한 도달" | 실패 청크만 고른 실험의 값이다. 실제 실행의 비율은 영상 1의 10min 1/9, 영상 2의 10min 12/18이다 |
| "입력 1,056토큰 이하에서 잘림 0건" | 1,056은 50개 영상 3min 캡션 최대값이고, 실측 333회의 입력 최대값은 1,025토큰이다 |
| rp110gen 설정이 "형식을 깨뜨림" | 원문 응답을 저장하지 않아 확인하지 못했다. 확인된 사실은 "1,300–1,400토큰 생성에 유효 triple 2개"인 이상 2건이다 |
| 처음 수정안(잘린 응답 구제 + 폭주 절단만) | 증상만 처리하는 안이었다. 재검토 후 긴 청크 분할을 핵심으로 바꿨다. 또 구제 조건으로 쓰려던 `finish_reason`은 서버가 잘린 응답을 `stop`으로 표시할 수 있어 쓰지 않았다(I25) |
| (2026-10-25 정정) "환경변수 `HF_HOME` 경로에는 모델이 없다", "`paths.hf_home`을 torch import 전에 설정해 해결" | 앞 문장은 2026-10-21 15:36 시점에만 맞았다. 16:26–16:31에 GPU 스모크가 그 경로(`HUGGINGFACE_HUB_CACHE`)에 모델을 내려받았다. 뒷 문장은 효과가 없다: 컨테이너가 설정한 `HUGGINGFACE_HUB_CACHE`가 `HF_HOME`보다 우선한다(§3) |
| (2026-10-25 정정) 대기 실행이 "00:08에 종료" | 00:08은 종료를 확인한 시각이다. 실제 종료는 00:06:06(`gate.json`·`gate_run.log` 파일 시각) |
| (2026-10-25 정정) "영상 2의 30sec·3min OpenIE 결과는 백업되지 않았다" | `backups/cache_before_split_20261022/0RxMZBLeqRI/`에 10sec·30sec·3min 세 파일이 모두 있다(184·62·11청크) |
| (2026-10-25 정정) 검색 스모크·보고서 A·`.venv` 수리 날짜 "2026-10-22" | 컨테이너 시계(UTC) 기준 2026-10-21이다(파일 시각, 대화 기록 시각) |
| (2026-10-25 C-5 후 정정) §2.1·§2.2·§2.4·§6.2·§13.3과 I27의 상태 문장 | C-3–C-5를 기록하면서 상태 요약 절을 함께 고치지 않아 "C-3·C-4 아직 하지 않았다", "결정 4·번역 보완 실제 모델 미실행", "GPU 미검증" 등 지난 문장이 남아 있었다. 2026-10-25 C-5 후 점검에서 고쳤다 |

---

## 6. 설계 결정

### 6.1 아키텍처 결정 (D1–D10)

| ID | 결정 | 근거 / 비고 |
|---|---|---|
| D1 | 1차 도메인 = Video-MME(일반 영상 보고서 템플릿). 관제는 이후 템플릿 세트 교체로 적용 | 관제 템플릿을 일반 영상에 쓰면 없는 내용을 지어낼 위험 |
| D2 | 통합 접합점 = Deep-Reporter `retriever_url`(HTTP). 검색 서비스가 Deep-Reporter 계약을 구현 | Deep-Reporter 코드 무수정, 환경 분리 |
| D3 | Outline = `with_planner`(질의 → outline 구상). planner 프롬프트에 그 영상의 10min 캡션 개요를 넣음 | planner가 영상 내용을 모르면 근거 없는 섹션이 생김. 추가 LLM 호출 없음 |
| D4 | LLM: 기본 로컬 `qwen3vl-8b`(Qwen3-VL-8B-Instruct), 외부는 `gpt-5-mini`. 설정 `llm.backend: local\|openai`. Deep-Reporter에는 **환경변수**로 주입 | §4.3 라우팅·설정 함정 |
| D5 | 로컬 LLM 제공 = 소형 HF 서버(`local_llm_server.py`, OpenAI 호환). 나중에 vLLM을 같은 주소로 교체 가능 | vLLM 미설치, 새 패키지 없이 검증된 래퍼 재사용 |
| D6 | Episodic 검색 기본 = **L1** (검색 요청당 multiscale 필터 1회). L0와 full은 옵션 | §7.3 |
| D7 | Semantic 근거 포함. "video-level knowledge"로 표기하고 시간·프레임 미부여 | §4.1 시간 근거 없음 |
| D8 | Episodic 그래프는 오프라인 사전 인덱싱해 영구 캐시. 사전 인덱싱 방식은 사용자 결정 1(A안: OpenIE를 LLM 서버 HTTP로) | §5.2. 영상 1개 완주(§9.6), 분할·구제 적용 후 재실행은 중단(§9.8) |
| D9 | Deep-Reporter filter 노드 = off (`enable_filter=False`) | 검색 단계의 L1 필터가 대신하고, Deep-Reporter filter는 웹 이미지 기준 |
| D10 | MERIT은 이후 **별도 검색 서비스**(다른 `retriever_url`)로 교체 가능하게 | 프로세스 분리가 단순하고 충돌 위험이 적음 |

### 6.2 사용자 결정 (2026-10-22 – 10-25)

| # | 주제 | 결정 | 상태 |
|---|---|---|---|
| 1 | 사전 인덱싱 방식 (A: OpenIE를 LLM 서버 HTTP로 / B: GPU가 빌 때 현재 스크립트 / C: 10sec만 유지) | 처음 보류(GPU 불가) → **A안**, GPU 4–7 사용 | ✅ 구현(§8.3). 시험 실행 중지(§9.5) → 영상 1개 완주(§9.6) → 분할·구제 적용 후 재실행 중단(§9.8) |
| 2 | 근거 일치 검사 방식 | **규칙 기반** (LLM 0회) | ✅ 구현(§8.7). 부정 절 처리 보완 |
| 3 | 이미지 정책 | 잘못된 형식 `[citation:imgN]`은 **후처리에서 실제 그림으로 변환**. 섹션별 이미지는 **의무화하지 않음** | ✅ 구현(§8.7) |
| 4 | 반복 억제 | 분석 후 **B안**(writer 규칙 6) 채택. 중복 관련 refine 전략은 **C0**(앞 섹션에서 실제로 쓴 문장을 writer에 전달, LLM 호출 증가 없음, Deep-Reporter 내부 함수를 실행 중에만 교체) | ✅ 구현(§8.6). 실제 모델 효과 ✖ |
| 5 | 보고서 구조 | **가벼운 결론 섹션을 planner에 강제**. **섹션 수 상한 6**(사용자 확정) | ✅ 구현(§8.6). 허용 3–15. 실제 1회 준수 ✔ |
| 6 | 보고서 언어 | **영어로 작성한 뒤 한국어로 번역해 추가** | ✅ 구현(§8.9). 실제 1회 ✔, 품질 보완 구현 |
| 7 | 근거 구성 (episodic/semantic/image 개수) | **보류**. "구체적인 세팅 및 한계점을 분석해서 나중에 다시 물어봐 달라" | 설정·한계 정리 완료(`ANALYSIS_D4_D7.md` §2). 결정 1 완료 후 실험해서 다시 질문 |
| 8 | 작업 순서 | 후처리기 → `run_report.py` → 규칙 기반 검사 먼저 | ✅ 완료 |
| — | 보완 지시 | 번역 한자 혼입 감지, 사람 이름 보호, 부정문 오탐 처리, 이미지-텍스트 시간 기록 | ✅ 구현(§8.7, §8.9) |
| 9 | OpenIE 출력 상한 문제 대응 | 디코딩 변경 기각. **긴 청크 분할 OpenIE + 응답 구제 + 폭주 절단** 적용(사용자 승인, 전략 수립 후 진행 지시) | ✅ 구현(§8.3), CPU ✔, GPU ✔(2026-10-25 C-1, §9.10) |
| 10 | 기존 캐시 처리 | `-QuCz7kxBr8`의 10min과 완료 표식, `0RxMZBLeqRI` 전체를 **삭제 후 재계산**(사용자 승인) | 삭제 ✅(비교용 일부 백업), 재계산 ✅(2026-10-25 C-1, §9.10) |
| 11 | 10min 캡션 재생성(I22) | **이번 범위에서 제외(보류)**. 소요 시간·GPU 정리만 | 보류. 추정은 `REPORT_ISSUES_AND_FIXES.md` I22 |
| 12 | GPU 사용 범위 | 20,000 MiB 규칙 해제·GPU 4–7 → 다른 사용자 침범 금지·여유 메모리 안 → **GPU 6·7만** | 2026-10-25 결정 13으로 바뀜 |
| 13 | GPU 사용 범위 (2026-10-25) | "지금 gpu 4~7번 4개를 모두 사용할 수 있어" | 적용(C-1–C-5) |
| 14 | C 단계 실행 방식 (2026-10-25) | "서버당 memory 상한 20000으로 제한하지 않고, 사용 가능한 메모리를 모두 사용", "골고루 작업을 gpu 4-7번에 분배", "C-1부터 순차적으로", "아직 C-7은 수행하지 마". `experiments/gpu_3videos.py` 수정(여러 서버·상한 선택·`--skip-reports`), GPU 배치, 새 스크립트 3개 승인 | C-1–C-5 실행 ✅, C-6 질문 전, C-7 ✖ |
| 15 | 정합성·관리 (2026-10-25) | 문서·기록 정합성 정리(B 항목) 지시. `experiments/delayed_gpu_3videos.py`에 `--gpus`, 루트 `CLAUDE.md` 갱신, `report_framework` git 관리 승인 | ✅ |
| 16 | 보고서 품질 대응 (2026-10-25) | P9: "(a) + (c) + (d)로 적용". C0: "앞 문단의 문장은 전달하자. 나중에 표본을 늘려서 재측정". P19: "1,3을 추가 적용". 번역: "지금 신경쓰지 않을게. 영어 report의 품질을 집중적으로". 결정 7: "D와 C를 후보로, 결정 1·3을 적용한 뒤 실험해서 비교 결과로 다시 물어봐줘". I28 "승인". GPU: "gpu 4-7을 1시간만 더", "당장 실행해야 하는것만 수행하고 보류" | P9·P19·I28 구현·확인 ✅(§8.12, §9.16). C/D 실험은 코드 수정·GPU 필요로 보류. C-7 보류 |

---

## 7. 아키텍처

### 7.1 구성

```
[0] 오프라인 사전 인덱싱 (영상별 1회, GPU)
    prebuild_episodic_index.py (+ run_prebuild_http.sh)
      캡션 4종 → HippoRAG 그래프 (granularity별) → cache/episodic/{vid}/episodic_memory/{g}/
      OpenIE LLM: [LLM] 서버들을 HTTP로 호출 (결정 1 = A안), 10sec는 전처리 OpenIE를 시드로 사용
      1,100토큰 초과 청크는 문단 조각(≤700토큰)으로 OpenIE 후 청크 단위로 병합해 캐시에 기록, 응답 구제·폭주 절단

[LLM] local_llm_server.py  :8010  OpenAI 호환 /v1/chat/completions, Qwen3-VL-8B 1회 로드 (또는 vLLM, 같은 주소)
         ▲ Deep-Reporter(env 라우팅) · L1 필터 · 번역 · (사전 인덱싱 OpenIE)

[A] videorag_retriever_service.py  :8020  POST /videos/<vid>/search, /load, GET /health
      text : episodic(L0/L1/full) + semantic(시간 없음) → RRF 병합, id 중복 제거
      image: VLM2Vec 유사도 → RRF → 구간 중앙 프레임 jpg + 같은 시각의 10sec 캡션

[D] run_report.py (CPU, 모델 로드 없음)
      ① 사전 확인 → ② env 라우팅 → ③ 템플릿 교체 + C0 맥락 교체 (domain_templates.py)
      → ④ Deep-Reporter 그래프 [B] (파일 무수정): planner → (query → search[A] → write) × N → combine
      → ⑤⑥ [C] grounding_postprocessor.py: 인용 → 참조·그림, 규칙 근거 검사, 이미지 시간 기록
      → ⑦ 사후 검증 → ⑧ report_translator.py (한국어) → ⑨ 산출물
```

단계별 상세는 `REPORT_PIPELINE.md` §3에 있다.

### 7.2 LLM 호출 예산 (섹션 수 N)

| 단계 | 원본 그대로 연결했을 때 (N=5) | 현재 설계 (L1) |
|---|---|---|
| planner | 1 | 1 |
| query 생성 | 5 | N |
| 검색 | 75–125 (쿼리 3–5개 × 5회 × 섹션) | N (요청당 L1 필터 1회) |
| 작성 | 5 | N |
| 영어 보고서 합계 | 약 86–136 | **1 + 3N** (A: 16, B: 19) |
| 한국어 번역 | — | N (재시도 시 최대 2N) |

후처리, 규칙 근거 검사, C0 요약, 이미지 시간 기록은 LLM을 쓰지 않는다.

### 7.3 검색 단계 L0 / L1 / full

| 모드 | 사용하지 않는 부분 | 검색 LLM 호출 | 특징 |
|---|---|---|---|
| full | 없음 (WorldMM 원본 `episodic_memory.retrieve`) | 쿼리당 최대 5회 | 논문과 같지만 무거움 |
| **L1 (기본)** | DSPy fact 필터 | 검색 요청당 1회 | 섹션의 모든 쿼리 후보를 모아 `multiscale_filter`를 1회 실행 → 시간 규모 선택과 잡음 제거 유지 |
| L0 | DSPy fact 필터와 multiscale 필터 | 0 | 규칙(granularity별 상한 + RRF)으로만 병합 |

- **L0와 L1에서도 유지되는 것**: 다중 스케일 지식그래프, fact 임베딩 점수, PPR 확산, semantic PPR, visual VLM2Vec.
- **DSPy 필터를 빼는 방법**: `prepare_retrieval_objects` → `get_query_embeddings` → `get_fact_scores` → 점수 상위 `linking_top_k`(5)개 fact → `graph_search_with_fact_entities`를 직접 조합한다(HippoRAG 코드 무수정, ✔ 메서드·시그니처 확인). 그래프 검색이 예외(assert 등)로 실패하면 dense passage retrieval로 대체한다.
- **영향**: WorldMM 논문에 이 필터들만 뺀 ablation은 없어 품질 영향은 알 수 없다(✖). 4개 단위 캐시가 생기면 같은 영상·질의로 비교한다.
- **L1 프롬프트 크기 관리**: 쿼리당 granularity별 후보를 10sec 3 / 30sec 3 / 3min 2 / 10min 1로 줄였다. 쿼리 3개를 합치고 중복을 빼면 후보는 최대 27개, 평균 길이 기준 약 6,600단어(추정)다. 실측(10sec만): L1 필터 입력 2,275–3,474토큰.
- 후보가 요청 개수 이하이면 L1 필터를 건너뛴다(`meta.episodic_filter="skipped(<=n)"`).

### 7.4 Deep-Reporter 동작 변경 방식 (범위 한정 + 사전 검증)

repo 파일은 수정하지 않는다. 바꾸는 대상은 두 가지다.

| 대상 | 무엇으로 | 함수 |
|---|---|---|
| 노드 3개의 프롬프트 템플릿(`OUTLINE_GENERATION_TEMPLATE`, `QUERY_GENERATION_TEMPLATE`, `SECTION_WRITING_TEMPLATE`) | videomme 템플릿 | `apply_templates()` |
| `section_writing_node`가 호출하는 `_update_context` | 앞 섹션에서 실제로 쓴 문장 요약(C0) | `apply_written_context()` |

1. `import deep_reporter.api`를 가장 먼저 한다(순환 import 회피).
2. 대상 namespace는 그래프가 실제로 등록한 함수 객체의 `__globals__`에서 찾는다(`deep_reporter.core.graph.<node>.__globals__`). 함수가 실제로 읽는 dict라서 패키지 속성 가림 문제를 피한다.
3. 실행 전에 계약을 검사하고, 실패하면 즉시 중단한다(웹용 템플릿으로 몰래 돌아가지 않는다).
   - 템플릿: 함수가 그 이름을 전역으로 읽는지(`co_names`), placeholder ⊆ 노드가 넘기는 키(AST로 동적 추출), 필수 placeholder와 출력·규칙 마커 존재, `.format()` 시험 실행.
   - `_update_context`: 노드가 호출하는지, 시그니처 `(previous_summary, new_content, section_desc)`, 반환이 `(summary, tail)` 문자열인지(실제 호출로 확인).
4. `with` 블록 동안만 교체하고 `finally`에서 원래 객체로 복원한 뒤 복원 여부를 확인한다. 프로세스 lock으로 중첩·동시 적용을 거부한다.

---

## 8. 구현 상세 (현재 동작 기준)

### 8.1 `report_framework/` 파일

| 파일 | 역할 | 검증 |
|---|---|---|
| `config.yaml` | 경로, WorldMM, LLM, 검색, 서비스, 보고서 설정 | — |
| `prebuild_episodic_index.py` | 오프라인 episodic 사전 인덱싱 (in-process 또는 HTTP OpenIE, 긴 청크 분할, 응답 구제·폭주 절단) | dry-run ✔, CPU ✔, 영상 1개 완주(분할 적용 전) |
| `run_prebuild.sh` | in-process 방식 실행: `./run_prebuild.sh <GPU> [--videos a,b] [--shard K/N]` | 문법 ✔ |
| `run_prebuild_http.sh` | A안 실행: `./run_prebuild_http.sh <LLM_GPUS> <INDEXER_GPU> [--videos=a,b]` (감시 장치 없음) | 시험 실행(§9.5, 중지) |
| `local_llm_server.py` | OpenAI 호환 LLM 서버 (Qwen3-VL-8B) | GPU ✔ |
| `videorag_retriever_service.py` | [A] 검색 서비스 | CPU ✔, GPU ✔ (10sec만) |
| `domain_templates.py` | [B 교체] videomme 템플릿, 계약 검사, `apply_templates`, C0 `apply_written_context` | CPU ✔, 실제 2건(규칙 6·C0 전) |
| `grounding_postprocessor.py` | [C] 인용 치환·그림·References, 규칙 근거 검사, 이미지 시간 기록 | CPU ✔ |
| `run_report.py` | [D] 보고서 생성 진입점 | CPU ✔, 실제 1회 |
| `report_translator.py` | 한국어 번역 (결정 6) | CPU ✔, 실제 1회 |
| `analysis/analyze_report.py` | 반복·근거 구성 지표 (읽기 전용) | 보고서 A·B 적용 |
| `analysis/summarize_batch.py` | 보고서 배치 결과 요약(읽기 전용, §8.12) | 실행 ✔(§9.16) |
| `analysis/compare_openie_cache.py`, `results/c2_openie_compare.json` | C-2 분할 전후·재계산 OpenIE 캐시 비교(읽기 전용) | 실행 ✔(§9.11) |
| `analysis/openie_degeneration_exp.py`, `results/openie_exp/` | OpenIE 디코딩 설정 비교 실험과 결과(건별 `.json`, `.log`, 요약 `summarize.py`) | 실행 ✔(§9.7) |
| `tests/` | CPU 테스트 5종, GPU 실행 스크립트 5종, 메모리 상한 래퍼 2종 (§8.11) | — |
| `outputs/3videos_<시각>/` | `experiments/gpu_3videos.py` 실행 결과(로그, `summary.json`) | §9.6, §9.8 |
| `outputs/3videos_20261022_160548_gated/` | `experiments/delayed_gpu_3videos.py` 실행 기록(`gate_run.log`, `gate.json`). 시작하지 않아 `summary.json`·보고서 없음 | §9.9 |
| `migration/` | 서버 이전용: rsync 규칙 2개(`videorag_transfer_nomodels.filter` 사용, `videorag_transfer.filter`는 모델 포함본·미사용), 영상 50개 md5(`videos50.md5`), `/opt/venv` 패키지 목록(`opt_venv_freeze.txt`) | 이전 복사에 사용 ✔ |
| `MIGRATION_HANDOFF.md` | 서버 이전 인수인계 메모 | — |
| `.git/`, `.gitignore` | 2026-10-25 사용자 승인으로 만든 git 저장소(브랜치 `main`). 코드·문서·설정·테스트 코드·`analysis/`·`migration/`을 추적하고, 생성물·대용량인 `cache/`, `logs/`, `outputs/`, `tests/_artifacts/`, `backups/`, `__pycache__/`는 추적하지 않는다(디스크에는 그대로 있음). `tests/unit/test_openie_split_guard.py`의 입력 로그(`outputs/3videos_20261022_120438/prebuild_indexer.log`)도 추적 대상이 아니다 | — |
| `backups/` | `.venv` 수리 전 원본 76개 파일, 2026-10-22 수정 전 파일(`*.bak_20261022*`), 2026-10-25 수정 전 문서(`*.bak_20261025_b`), 삭제 전 캐시 일부(`cache_before_split_20261022/`) | — |

### 8.2 `config.yaml`

| 절 | 주요 값 |
|---|---|
| `paths` | `hf_home`(실제 모델 캐시), `caption_dir`·`metadata_dir`(WorldMM 산출물), `episodic_cache_root`(`report_framework/cache/episodic`; 2026-11-10부터 `../WorldMM/output/memory/videomme_long_qwen3vl-8b/report_framework_index`), `log_dir`. 2026-11-10부터 상대 경로는 `report_framework/` 기준(`rf_config.py`) |
| `worldmm` | `granularities: [10sec, 30sec, 3min, 10min]`, `query_time: 123595999`(DAY1 23:59:59, 전체), `metadata_model: qwen3vl-8b`, `text_embedding_model: Qwen/Qwen3-Embedding-4B`, `episodic_cache_label: qwen3vl-8b` |
| `llm` | `backend: local`. local: `worldmm_model: qwen3vl-8b`, 엔드포인트 `server: hf`, `127.0.0.1:8010`, `model: qwen3vl-8b`, `api_key: EMPTY`, `default_max_tokens: 8192`. openai: `gpt-5-mini` |
| `retrieval` | `episodic_filter: L1`, `rrf_k: 60`, 후보 `{10sec:3, 30sec:3, 3min:2, 10min:1}`, `full_top_k_per_query: 3`, `episodic_k: 8`, `semantic_k_per_query: 5`, `semantic_k: 4`, `visual_k_per_query: 3`, `image_k: 4`, `filter_max_tokens: 512` |
| `service` | `127.0.0.1:8020`, `frames_dir`(`report_framework/cache/frames`) |
| `report` | `domain: videomme`, `text_topk: 20`, `image_topk: 10`, `enable_filter: false`, `overview_granularity: 10min`, `outputs_dir`, `deep_reporter_log_dir`, `previous_sections_context: written`, `max_sections: 6`, `translate_ko: true`, `translation_max_tokens: 4096` |

### 8.3 사전 인덱싱 `prebuild_episodic_index.py`

- **`LabeledEpisodicMemory`**: WorldMM `EpisodicMemory`를 상속해 `_get_or_create_hipporag`만 재정의하고, `BaseConfig(llm_name=<실제 모델>)`을 넘겨 캐시 라벨을 바로잡는다. 검색 서비스도 같은 클래스를 써서 같은 캐시를 찾는다.
- **10sec 시드**: 현재 캡션에 있는 passage만, 해시 기준 중복 제거, 빈 triple 제외. HippoRAG `index`의 `len(chunk_to_rows)==len(ner_results_dict)` assert와 맞추기 위해서다. 인덱싱 LLM이 전처리 모델과 같을 때만, 캐시 파일이 없을 때만 넣는다.
- **진행 관리**: 영상 단위 완료 표식(`cache/episodic/_done/{vid}.{label}.json`, `llm_mode` 포함). 실패해도 다음 영상으로 계속하고, 인덱싱 후 캐시가 빠짐없이 채워졌는지 검증한다. 로그는 `logs/prebuild_<시각>.log`.
- **`--dry-run`**: 모델 로드도 파일 쓰기도 하지 않는다(토크나이저 파일만 읽음). 빈 캐시 기준 50개 영상 13,424회(분할 포함, ✔). 분할 전 코드로는 12,818회였다.
- **`--llm-endpoints URL1,URL2,…` (결정 1 = A안)**
  - `HttpLLMModel`을 쓴다. HippoRAG/OpenIE가 쓰는 `.generate(messages, text_format=…)`와 `.model_name`만 제공하고, 여러 서버에 순서대로 돌아가며 요청한다.
  - in-process 경로와 같게 맞춘 점(✔ 코드): 같은 chat 메시지, `max_tokens=2048`(Qwen3VLModel 기본 `max_new_tokens`), temperature/top_p 미전송(모델 기본 샘플링), 같은 파서(`Qwen3VLModel._parse_structured_response`), 같은 재시도 깊이(클라이언트 3회 × OpenIE 5회).
  - 실행 전 각 서버 `/health`의 모델명이 `qwen3vl-8b`인지 확인한다. 다르면 중단한다. `llm.backend=local`이고 엔드포인트 모델명이 `worldmm_model`과 같아야 한다.
  - 종료 시 HTTP 요청 수와 실패 수를 로그에 남긴다. 인자를 주지 않으면 기존처럼 in-process로 LLM을 올린다.
- **`--gpu-mem-cap-mib`**: torch import 직후 `set_per_process_memory_fraction`을 적용한다.
- **`run_prebuild_http.sh`**: LLM 서버를 GPU마다 1개(`scripts/launch/run_llm_server_capped.py`, 19,000 MiB 상한, 포트 18710부터) 띄우고 `/health`를 기다린 뒤, 인덱서를 `--gpu-mem-cap-mib 19000`으로 실행한다. 끝나면(오류 포함) trap으로 자기가 띄운 서버만 종료한다. 같은 GPU 번호를 두 번 넣으면 로그 파일 이름이 겹쳐(`prebuild_llm_<시각>_gpu<g>.log`) 로그가 섞인다. GPU당 서버 여러 개는 `experiments/gpu_3videos.py` 방식으로 띄운다.
- **긴 청크 분할 OpenIE** (2026-10-22, 결정 9)
  - `plan_video`가 캐시·시드에 없는 청크 중 토큰 수가 `SPLIT_MIN_TOKENS`(1,100)를 넘는 것을 `split`으로 분류하고, `split_passage`로 빈 줄 문단을 `SPLIT_PIECE_TOKENS`(700) 이하 조각으로 묶는다(문단이 길면 문장 단위, 한 문장이 길면 그대로 1조각). 토큰 수는 Qwen3-VL 토크나이저(`tokenizers` + HF 캐시의 `tokenizer.json`, torch 미사용)로 센다. 그래서 `HF_HOME`을 dry-run 전에 설정한다.
  - 영상마다 인덱싱 전에 `openie_split_docs`가 조각별로 WorldMM `OpenIE.ner` → `triple_extraction`을 병렬(기본 `ThreadPoolExecutor`, OpenIE와 같은 동시성)로 호출하고, 청크 단위로 합친다(entity는 순서 보존 합집합, triple은 `filter_invalid_triples`로 중복 제거). `write_cache_docs`가 기존 캐시 항목을 보존하면서 새 항목만 추가한다. 이후 HippoRAG는 이 청크를 캐시된 것으로 보고 다시 계산하지 않는다. 그래프 구조(청크 1개 = passage 노드 1개)는 그대로다.
  - 경계: 조각 경계를 넘는 대명사·문맥을 잃을 수 있다(미측정). 1,026–1,100토큰 구간은 실측 범위 밖이다.
- **응답 구제·폭주 절단** (HTTP 경로만)
  - 파싱이 실패하면 `salvage_structured`가 `json_list_items`로 완성된 목록 항목만 꺼내고, 형식이 맞는 것만 남긴다(NER: 문자열, 중복 제거 후 최대 `MAX_SALVAGED_ENTITIES`=100 / triple: 문자열 리스트). 하나도 없으면 예외 → 기존 재시도.
  - triple 응답(파싱 성공 포함)에서 같은 (주어, 술어)가 연속 `MAX_SAME_SUBJ_PRED_RUN`(15)개를 넘는 부분을 `cut_long_runs`로 버린다. 경험적 기준이다(정당한 연속 최대 14, 폭주 39–115).
  - 구제·절단 횟수를 `HttpLLMModel.guard`에 센다. in-process 경로에는 적용되지 않는다.
- **완료 표식 필드 추가**: `split`(단위별 분할 청크·조각·실패 조각 수), `cache_empty`(단위별 빈 triple·빈 entity 수), `guard_cumulative`(프로세스 누계 구제·절단 수). 완료 판정은 `to_compute`와 `split`이 모두 0이어야 한다.
- **dry-run 표시**: `chunk/cache/seed/new/split(조각 수)`.

### 8.4 로컬 LLM 서버 `local_llm_server.py`

- 경로: `POST /v1/chat/completions`, `GET /v1/models`, `GET /health`.
- WorldMM `LLMModel("qwen3vl-8b")`를 한 번 로드한다. 입력은 텍스트와 `image_url`(data URL 또는 절대경로만)을 받는다.
- `max_tokens`(또는 `max_completion_tokens`) → `max_new_tokens`. `temperature`와 `top_p`는 값이 올 때만 반영하고(`temperature=0`이면 greedy), `chat_template_kwargs`는 무시하며, `stream=true`는 400을 반환한다.
- 생성은 lock으로 하나씩 처리한다. `usage`는 생성된 **텍스트를 다시 토큰화해** 센 값이고, `finish_reason`은 그 값이 `max_tokens` 이상이면 `length`다. 그래서 실제로 잘린 응답이 `completion=2047 finish=stop`으로 기록될 수 있다(실측, `REPORT_ISSUES_AND_FIXES.md` I25). 로그의 `finish=length` 수는 잘림 수의 하한으로만 본다. 로그의 시간은 요청 수신부터 측정하므로 서버 안 대기 시간이 포함된다.
- vLLM 교체: `vllm serve Qwen/Qwen3-VL-8B-Instruct --served-model-name qwen3vl-8b --port 8010` 후 `config.yaml`의 `server: vllm`. 모델 이름에 `qwen`이 있어야 Deep-Reporter 라우팅이 유지된다.

### 8.5 검색 서비스 `videorag_retriever_service.py`

- **엔드포인트**: `POST /videos/<video_id>/search`(Deep-Reporter 계약), `POST /videos/<video_id>/load`, `GET /health`. 요청 본문에 영상 id가 없어서 URL에 넣는다.
- **구성**: WorldMM `WorldMemory`를 쓰지 않고 `LabeledEpisodicMemory`(캐시 라벨 = `episodic_cache_label`), `SemanticMemory`, `VisualMemory`를 직접 조합한다. 한 번에 영상 1개를 로드하고, 다른 영상 요청이 오면 교체한다. 요청은 lock으로 직렬 처리한다.
- **로드 전 검사**: granularity마다 episodic 캐시가 완전한지(`plan_video`로 cached == chunks), semantic·visual 파일이 있는지. 불완전하면 **409**로 거부한다(캐시 오염 방지, §5.2). 분할 OpenIE(§8.3) 이후에도 판정 기준(캐시된 청크 수)은 같다. 캐시가 불완전한 영상을 검사할 때는 `plan_video`가 토크나이저를 읽는다.
- **text**
  - episodic L0/L1: (쿼리, granularity)마다 DSPy를 뺀 그래프 검색으로 후보를 모으고 RRF로 병합한다. L1은 병합 후보 전체에 WorldMM `_filter_with_llm`을 1회 호출한다(질문은 섹션 쿼리들을 `"; "`로 이은 문자열).
  - episodic full: 쿼리마다 `episodic_memory.retrieve`. 쿼리별 결과가 겹쳐 근거가 모자라지 않도록 쿼리당 개수를 `max(full_top_k_per_query, ceil(n/쿼리 수))`로 둔다.
  - semantic: 쿼리마다 PPR 검색 → RRF.
  - 개수: episodic `min(episodic_k, topk)`, semantic `min(semantic_k, 남은 topk)`.
- **image**: `VisualMemory._retrieve_by_similarity(as_context=False)` → RRF → 구간 **중앙** 프레임 JPEG(`{frames_dir}/{vid}/{start_time}.jpg`, decord, 캐시) → 같은 `start_time`의 10sec 캡션을 `caption`으로 붙인다. `visual.retrieve()`는 질의가 `DAY X HH:MM:SS - …` 형태면 시간 범위 검색으로 바뀌므로 쓰지 않는다.
- **응답 항목**
  - episodic: `content="[HH:MM:SS-HH:MM:SS | episodic <g>] 캡션"`.
  - semantic: `content="[video-level knowledge | semantic] (s, p, o)"`, 시간 필드 None, `time_grounded: False`.
  - image: `caption="[HH:MM:SS-HH:MM:SS | video frame at Xs] 캡션"`, `img_path`, `frame_sec`.
  - 공통 메타: `uid`, `score`(RRF), `score_type`, `rank`, `start/end_time`, `start/end_sec`, 절대 `video_path`. 응답 최상위 `meta`에 모드, 후보 수, 필터 실행 결과(`llm` / `fallback_rrf(llm_failed)` / `skipped(<=n)` / `none`), 소요 시간을 둔다. Deep-Reporter는 `status`와 `results`만 읽는다.
- **LLM 객체**: L0는 `NoLLM`(호출되면 예외). L1/full은 `EndpointLLM`(openai SDK. local은 `max_tokens`, openai는 `max_completion_tokens`, 호출·실패 횟수 집계). 구조화 생성(OpenIE) 요청은 거부한다.
- **알려진 한계**: L1에서 LLM 응답 형식이 깨져 WorldMM이 RRF 순위로 빈자리를 채워도 `meta.episodic_filter`는 `llm`으로 표시된다(호출 자체는 성공했기 때문, ✔ 코드).

### 8.6 템플릿·맥락 교체 `domain_templates.py`

- **API**
  - `load_video_overview(10min.json)`: `[HH:MM:SS-HH:MM:SS] 캡션` 블록을 이어 붙인 영상 개요.
  - `build_templates("videomme", overview, max_sections=6)`: `<<VIDEO_OVERVIEW>>`(중괄호 escape)와 `<<MAX_SECTIONS>>` 자리를 채운다. `max_sections`는 정수 3–15만 허용한다(문자열·bool 거부).
  - `apply_templates(templates)`, `apply_written_context()`: context manager(§7.4).
  - `python domain_templates.py --check [--overview-file …] [--max-sections N]`: 계약 검사만 한다.
- **planner 템플릿**
  - 영상 개요를 근거로 **총 3–N개 섹션**(N = `max_sections`, 결론 포함)을 만들고, 영상에 없는 내용(외부 지식, 통계, 예측)의 섹션은 만들지 않는다. 질의 내용이 영상에 없으면 "보여주는 것과 보여주지 않는 것" 섹션을 최대 1개만 둔다.
  - 섹션 설명에는 대략적인 시간 범위를, checklist에는 관찰 가능한 항목을 쓴다.
  - 규칙 6(결정 5): 마지막 섹션은 앞에서 다룬 결과를 요약하는 짧은 결론이다. 설명은 정확히 `Conclusion:`으로 시작하고, 새 주제를 넣지 않으며, checklist는 2–3개다. 다른 섹션은 `Conclusion:`으로 시작하지 않는다. 출력 예시 JSON에도 결론 섹션이 있다.
- **query 템플릿**: text 질의는 사건·인물·대사·물체 키워드 2–3개, image 질의는 장면의 생김새를 묘사하는 문장 1–2개. 차트·다이어그램 요청 금지. 앞 섹션에서 다룬 내용은 필요할 때만 다시 검색한다.
- **writer 템플릿**
  - 근거 라벨의 의미 설명(episodic 10sec/30sec는 세부, 3min/10min은 요약, video-level knowledge는 시간 없음, video frame은 그 순간의 프레임).
  - Grounding 규칙: (1) 근거가 말하는 것만 쓰고 추측 금지 (2) 근거의 시간만 HH:MM:SS로, semantic에는 시간 금지 (3) 충돌 시 세밀한 단위 우선 (4) 근거가 없으면 없다고 씀 (5) 시간순 서술 (6) **반복 금지(결정 4-B)**: 이 섹션에서 쓴 사실·문장·단락을 반복하지 않고, 앞 섹션에서 다룬 사실은 한 문장 이하로만 언급한다. 결론 섹션은 예외.
  - Citation 규칙: (1) 사실 문장마다 `[citation:txtN]` (2) 이미지는 별도 줄 `![](citation:imgN)`, 있으면 1–3장 (3) 괄호 하나에 출처 하나 (4) **`[citation:imgN]` 금지**(보고서 A의 문제를 보고 추가).
  - 위치별 지시(첫/중간/마지막 섹션)와 결론 섹션 규칙: 설명이 `Conclusion:`으로 시작하면 100–250단어로 앞 결과만 종합하고 새 사건을 넣지 않으며, 사실 문장은 근거를 인용한다.
- **계약 검사 마커**: planner `"outline"`, `"section_description"`, `"sectional_checklist"`, `"Conclusion:`. query `"text_queries"`, `"image_queries"`. writer `[citation:txt1]`, `![](citation:img1)`, `# Title`, `"Conclusion:"`, `mention it in at most one short sentence`(규칙 6).
- **C0 `apply_written_context()`** (결정 4)
  - 원래 `_update_context`가 만드는 요약(섹션 설명 + 본문 앞 100자)을, 앞 섹션에서 **실제로 쓴 문장 요약**으로 바꾼다. LLM은 쓰지 않는다.
  - 형식: 안내 문구(인용 번호를 지웠고 현재 섹션 근거를 가리키지 않는다는 설명) + 섹션마다 `Section k: <제목>`(제목 앞의 "Section k:"는 제거) + 단락마다 첫 문장. 인용·이미지 표기는 지우고 시간은 남긴다. 4단어 미만 단락은 건너뛴다.
  - 상한: 문장 240자, 섹션 700자, 전체 3,600자. 넘치면 오래된 섹션부터 제목만 남긴다.
  - tail은 원래 함수가 계산한다(새 본문에만 의존하므로 결과가 같다). 같은 요약이 query 생성에도 들어간다.
  - 보고서 B의 섹션 1–5로 재현하면 3,229자다.
  - `config.yaml`의 `report.previous_sections_context`: `written`(기본, C0) / `deep_reporter`(원래 동작, 비교 실험용).

### 8.7 후처리기·규칙 근거 검사 `grounding_postprocessor.py`

- **입력**: `generate_article()` 결과. 섹션마다 writer와 같은 근거 목록을 고른다(`enable_filter`이고 `filtered_*`가 있으면 그것, 아니면 `retrieved_*`, 1부터 번호).
- **인용 치환**
  - 인식 형식: `[citation:txtN]`, 변형(`[citation: txt3]`, `[citation:txt1, txt3]`, 대소문자 무관), `![](citation:imgN)`(alt 허용), 잘못된 형식 `[citation:imgN]`.
  - 텍스트 인용 → 전역 번호 `[n]`(같은 uid는 같은 번호) + `# References`(episodic: `HH:MM:SS–HH:MM:SS · episodic <g>: 캡션`, semantic: `Video-level knowledge (semantic memory, no timestamp): (s, p, o)`).
  - 이미지 → `![Figure k (프레임 시각)](frames/<vid>_<start_time>.jpg)` + 캡션(클립 구간 포함). 프레임 파일을 `<out_dir>/frames/`로 복사하고, 같은 프레임은 한 번만 넣는다.
  - 잘못된 형식 `[citation:imgN]`(결정 3): 문장 안의 자리는 `(Figure k)`로 바꾸고 실제 그림은 그 단락 뒤에 넣는다.
  - 범위 밖·해석 불가 인용 → `[?]`(집계). 실패하거나 빈 섹션 → `[Section k content missing]`.
  - 통계: 텍스트 인용, 잘못된 인용, 형식 오류 토큰, 이미지 삽입, 잘못된 형식 변환, 중복 삽입, 참조 수, 그림 수, 프레임 누락, 섹션별 미사용 근거 수.
- **규칙 근거 검사 `check_section_grounding()`** (결정 2, LLM 0회)
  - 문장 단위(제목·이미지 줄 제외, 문장 앞에 붙은 인용은 앞 문장에 붙임)로 **따옴표 문구, 숫자, HH:MM:SS**를 그 문장이 인용한 근거와 대조한다.
    - 따옴표: 그대로 일치하거나, 같은 근거 안에서 단어가 같은 순서로 가까이(문구 길이 + 3단어 이내) 나오면 지지.
    - 숫자: 정확히 일치, `a/b` ↔ `a out of b`, 20 이하 등 작은 정수는 영어 단어도 인정.
    - 시간: 근거 텍스트에 있거나 인용한 근거 구간 안이면 지지.
  - 분류: `unsupported`(어떤 근거에도 없음), `miscited`(인용하지 않은 다른 근거에만 있음), `uncited`(인용 없이 토큰이 있는 문장), `absence`(아래). 결과는 경고이며 오류가 아니다.
  - **부정 절 처리(absence)**: 부정어(not/no/never/n't 등) 뒤 12단어 안에 show/visible/mention/state/specify 같은 동사가 오고, 문장에 footage/evidence/retrieved/video/clip/frame/source가 있으면, 부정어부터 다음 절 경계(`;`, `, but/though/while/which/and…`, 문장 끝)까지를 "근거에 없다는 진술"로 본다. 그 절 **안에만** 나오는 토큰은 검사하지 않고 `absence`로 기록하며, 절 밖의 토큰은 계속 검사한다.
  - 한계: 의미 수준의 오류(장면 오인)는 잡지 못한다. 부정 절 안에 틀린 값이 전제로 들어간 경우(예: "the evidence does not confirm the progression from 0/1 to 3/16")는 검사에서 빠진다. 재현율은 정답 데이터가 없어 측정하지 못했다.
- **이미지-텍스트 시간 기록 `image_time_alignment()`** (경고 없음)
  - 섹션에서 인용된 이미지(올바른 형식과 잘못된 형식 모두)마다 프레임 시각과 인용된 텍스트 근거 구간 사이 거리(초, 구간 안이면 0)를 기록한다. semantic은 시간이 없어 제외한다.
  - `gap_to_local_text_sec`: 같은 단락에서 인용된 텍스트(이미지만 있는 단락이면 직전 텍스트 단락). `gap_to_section_text_sec`: 섹션 전체에서 인용된 텍스트.
  - 결과: 섹션별 `image_time_alignment` 목록과 보고서 요약(인용 이미지 수, 텍스트 시간이 없는 이미지 수, 0초 수, 최대·중앙값).

### 8.8 보고서 생성 진입점 `run_report.py`

- 사용법: `python run_report.py --config config.yaml --video-id=<vid> --query "<요청>" [--checklist "..."]... [--out-dir DIR]`. 모델을 올리지 않으며 LLM 서버와 검색 서비스가 실행 중이어야 한다.
- **순서**
  1. 설정 확인: LLM 백엔드(local이면 모델명에 `qwen`, openai면 `gpt`와 `OPENAI_API_KEY`), `max_sections`(3–15), `previous_sections_context`(`written`/`deep_reporter`). 잘못되면 exit 2.
  2. 사전 확인: 개요 캡션 파일, LLM `/health`(local), 검색 서비스 `/health`와 `POST /videos/<vid>/load`(캐시 불완전 시 409), 템플릿 계약 검사. 하나라도 실패하면 exit 2.
  3. 환경변수 설정 → `create_openai_api({primary_model, log_dir})` → 실제 라우팅된 base URL이 기대값인지 확인(다르면 exit 2).
  4. `apply_templates(build_templates(domain, 개요, max_sections))`와 (`written`이면) `apply_written_context()` 안에서 `generate_article(with_planner, enable_filter=False, retriever_url=…/videos/<vid>/search)`.
  5. 후처리(⑤⑥) → 사후 검증(⑦) → 번역(⑧, 검증 오류가 없을 때만) → 산출물(⑨).
- **사후 검증**
  - 오류 → exit 1(산출물은 저장): `success=False`, 빈 outline, planner fallback(섹션 1개이고 설명 == query), 본문의 `Call failed:`·`[Section generation failed`, 빈 본문, 텍스트 근거 0건인 섹션, 잘못된 인용(`[?]`), 프레임 누락.
  - 경고: query fallback, 인용 없는 섹션, 잘못된 이미지 형식 변환 수, 규칙 검사 unsupported·miscited·uncited 수, 섹션 수 상한 초과, 마지막 섹션이 결론이 아님, 결론이 아닌 섹션에 `Conclusion:`, 결론 300단어 초과, 섹션 번역 실패(영어 유지), 번역에 한자·가나가 재시도 후에도 남음.
- **산출물** (`report.outputs_dir/<vid>_<YYYYmmdd_HHMMSS>/`): `report.md`, `report_ko.md`, `report_raw.md`, `report.json`(요청·outline·근거·참조·그림·`previous_sections_context`), `validation.json`(상태, 오류, 경고, 단계별 시간, `max_sections`, `previous_sections_context`, 인용 통계, 근거 검사 통계와 항목, `image_time_alignment`, 섹션별 결과, 번역 결과), `frames/`.
- **exit 코드**: 0 통과, 1 검증 오류(산출물 저장), 2 사전 확인·설정 실패(생성 안 함).

### 8.9 한국어 번역 `report_translator.py` (결정 6)

- 영어 `report.md`가 정본이고 `report_ko.md`는 추가 결과물이다. 번역 결과는 영어 결과와 exit 코드에 영향을 주지 않는다. 영어 보고서가 사후 검증에서 오류면 번역을 건너뛴다.
- 단위는 섹션이다(섹션당 LLM 1회, 최대 출력 4,096토큰). LLM은 Deep-Reporter와 같은 엔드포인트·모델이다(`EndpointLLM` 재사용).
- **보호(자리표시 `[[Pn]]`)**
  - 그림 블록(이미지 줄, 캡션 줄): 통째로 보호해 원문 그대로 둔다.
  - 인용 `[n]`·`[?]`, `(Figure k)`, `HH:MM:SS`, 따옴표 문구.
  - **고유명사**: 보고서 본문에서 문장 중간에 한 번이라도 대문자로 나온 단어 묶음을 모아(문장 첫 단어, 제목 줄, 그림, 이미 보호된 부분, 흔한 단어 제외) 보고서 전체(제목 포함)에서 보호한다. NER이 없어 사람과 제품·브랜드 이름을 구분하지 않으며, 문장 첫머리에만 나오는 이름은 수집되지 않는다. 보고서 B에서는 Chris, Zach, Cass, James, Mitchell, SKLZ, SKLZ Dribble Stick, Shot Coach가 수집된다.
- **검사**: 모든 자리표시가 정확히 한 번씩 있고 제목 줄 수가 같아야 한다(코드 블록 출력은 벗겨서 인정). 실패하면 1회 재시도하고, 그래도 실패하면 그 섹션은 영어 원문 유지 + 안내 문구.
- **한자·가나 감지**: 자리표시를 뺀 번역 출력에 한자나 가나가 있으면 같은 1회 재시도를 쓴다. 재시도에도 남거나 재시도가 자리표시 검사에 실패하면 처음의 유효한 번역을 유지하고 `foreign_script`로 기록한다(경고).
- **구성**: 한국어 헤더(영어 정본의 번역본 안내) + 번역 섹션 + References 영어 원문.
- **기록**: `validation.json`의 `translation`에 전체 상태(complete/partial/failed/skipped/disabled), `proper_nouns`, 섹션별 상태·시도 횟수·자리표시 수·`protected_names`·`foreign_script`·시간·실패 이유.

### 8.10 분석 도구 `analysis/analyze_report.py`

- 보고서 1건(`outline.json` 또는 `report.json`)을 읽어 지표를 계산한다. 파일을 바꾸지 않는다.
- 반복: 섹션 안 단락 쌍 유사도(인용·이미지 표기와 제목 제외, 정규화), 근접 중복 문장, 반복 8-gram 비율, 섹션 간 유사 문장, 섹션 사이에 다시 검색된 근거.
- 근거 구성: 유형별·순위별 인용률, 근거 검사 지적의 인용 유형, semantic triple 목록, 이미지와 인용된 episodic 구간의 시간 차이, 근거 크기.
- 선택: LLM 서버 로그에서 호출별 토큰·시간.
- 결과: `tests/_artifacts/analysis/smoke_metrics.json`(A), `e2e_run1_metrics.json`(B).

### 8.11 테스트

| 파일 | 종류 | 내용 | 결과 (2026-10-22) |
|---|---|---|---|
| `tests/unit/test_retriever.py` | CPU | 실제 데이터 + 실제 WorldMM·HippoRAG 코드, 가짜 모델. L0/L1/full, 이미지, 오류 응답(404·400·409), 실제 `search_node` 연결 | ALL PASS (30개) |
| `tests/unit/test_templates.py` | CPU | 템플릿 계약(거부 사례), 결정 5 상한·결론, 규칙 6, C0 요약·교체·복원, Deep-Reporter 그래프 통합 | ALL PASS (50개) |
| `tests/unit/test_report_pipeline.py` | CPU | [1] 후처리기(보고서 A 입력, 경계 사례) [2] `run_report` 전체 흐름(가짜 LLM: 정상, 서버 꺼짐, 캐시 없음, planner 실패, 결론 없음, 상한 초과, 번역 재시도·실패·한자) [3] 번역기(보고서 A 입력) [4] absence, 이미지 시간, 한자, 이름 보호(보고서 A·B 입력) | ALL PASS (67개) |
| `tests/unit/test_prebuild_http.py` | CPU | HTTP OpenIE 클라이언트: 메시지 동일성, 인자, 파싱, 서버 순환, 재시도, 모델명 확인 | ALL PASS (9개) |
| `tests/unit/test_openie_split_guard.py` | CPU | 실제 10min 캡션 분할(조각 ≤700토큰, 텍스트 손실·순서 변경 없음), **실제 실패 응답 14건 구제**, 비문자열 항목 제거, 폭주 절단, 캐시 병합, 가짜 서버로 1회 구제·구제 불가 시 15회 재시도, 분할 병합, dry-run 호출 수. 입력으로 `outputs/3videos_20261022_120438/prebuild_indexer.log`가 필요하다 | ALL PASS (18개) |
| `tests/gpu/gpu_smoke.py` | GPU | 검색 스모크(§9.2) | 실행함 |
| `tests/gpu/gpu_report_smoke.py` | GPU | 보고서 A(§9.3) | 실행함 |
| `tests/gpu/gpu_e2e.py` | GPU | 보고서 B + full 모드(§9.4) | 실행함 |
| `experiments/gpu_3videos.py` | GPU | 영상 3개 사전 인덱싱 → 보고서. LLM 서버 1개(`--llm-gpu`) 또는 여러 개(`--llm-gpus 4,4,5,…`, 포트 18810+i, 사전 인덱싱은 전부 순환 사용, 보고서는 첫 서버), 서버 상한 `--llm-cap-mib`(기본 19,000, 0 = 상한 없음) + 인덱서·검색 서비스(`--aux-gpu`, `--aux-cap-mib` 기본 15,000, 0 = 상한 없음), `--skip-reports`(사전 인덱싱만). 2026-10-25 사용자 승인으로 여러 서버·상한 선택·`--skip-reports` 추가(사본 `backups/gpu_3videos.py.bak_20261025`). 시작 전 여유 확인: GPU마다 그 GPU에 올릴 프로세스들의 상한 합(상한이 없으면 프로세스당 19,000 MiB) + 2,000 MiB. 감시: 합계 > `--abort-used-mib` 47,500이면 우리 프로세스만 종료 | §9.6(이전 판), §9.8, §9.10 |
| `experiments/delayed_gpu_3videos.py` | GPU | `--delay-sec`(기본 7,200) 대기 → GPU를 30초마다 재서 최근 `--hold-sec`(600초)의 최대 사용량을 구함 → `최대[llm] + 19,000 + margin ≤ --abort-used-mib`과 `최대[aux] + --aux-cap-mib + margin ≤ --abort-used-mib`(margin `--margin-mib` 1,500)을 만족하면 `gpu_3videos.py`를 1회 실행. 두 배치(LLM·aux를 `--gpus`의 두 GPU에 이 순서 또는 반대 순서로) 중 두 GPU의 남는 여유 가운데 작은 값이 더 큰 배치를 고른다. `--max-wait-sec`(6시간) 안에 못 맞추면 exit 2. 자동 재시도 없음. 대상 GPU 2개는 `--gpus`(기본 `6,7`)로 지정한다(2026-10-25 사용자 승인으로 고정값 `GPUS = (6, 7)`을 인자로 바꿈, 수정 전 사본 `backups/delayed_gpu_3videos.py.bak_20261025`. `--gpus 4,5`·잘못된 입력 거부를 GPU 미사용 조건으로 확인) | §9.9 (시작 안 함) |
| `scripts/launch/run_llm_server_capped.py`, `scripts/launch/run_service_capped.py` | 래퍼 | 상한을 건 LLM 서버(19,000 MiB)·검색 서비스(환경변수 `GPU_MEM_CAP_MIB`, 기본 19,000) 실행 | — |
| `tests/unit/test_p9_p19.py` | CPU | 2026-10-25 P9·P19·I28 수정: 같은 문장 제거(합성 루프, 실제 C-5 루프 섹션), 결말·시작 서술 검사(early/late/unverifiable, "concludes this section" 제외), `load_video_end`(10sec 기준 00:37:37), writer 규칙 7과 `<<VIDEO_END>>` 채움, 경고 문구, 서버 상한(3,072 / 없음)과 `count_tokens` 잠금 위치 | ALL PASS (16개) |

CPU 테스트는 `CUDA_VISIBLE_DEVICES=""`로 실행하고, 산출물은 `tests/_artifacts/`에 쓴다.

### 8.12 P9·P19·I28 수정 (2026-10-25, 사용자 승인, 수정 전 사본 `backups/*.bak_20261025_p9p19`, 커밋 `b7a021d`)

| 대상 | 파일 / 함수 | 내용 |
|---|---|---|
| P9 (a) 출력 상한 | `local_llm_server.py` `create_app(..., max_tokens_cap)`, `config.yaml` `llm.local.endpoint.max_tokens_cap: 3072` | 요청 `max_tokens`를 3,072로 자른다(Deep-Reporter는 항상 8,192 요청). 값 근거: C-3–C-5 정상 출력 최대 2,182토큰(번역), writer 정상 최대 1,766. 비우면 상한 없음 |
| P9 (c) 같은 문장 제거 | `grounding_postprocessor.dedupe_repeated_sentences`, `run_report.run` | 후처리(인용 치환) 전에 섹션마다 같은 문장(공백 정규화 후 완전 일치)의 두 번째 이후를 지운다. 제목·이미지 줄은 그대로. 섹션이 문장 부호 없이 끝나는지도 기록. `report_raw.md`는 원본(Deep-Reporter 출력) 그대로, `report.md`·`report.json`은 제거 후 |
| P9 (d) 검증 표시 | `run_report.validate` | 제거가 있으면 경고 "section i: removed N repeated sentence(s), a sentence occurred up to K times"(K ≥ 3이면 "writer repetition loop suspected"), 문장 중간 끝이면 "ends mid-sentence (likely cut at the LLM max_tokens cap)". 상태(`passed`/`failed`)는 바꾸지 않는다. `validation.json`에 `repetition`(섹션별) 추가 |
| P19 (1) writer 규칙 | `domain_templates.py` writer 템플릿 Grounding Rule 7, `VIDEO_END_SLOT`, `build_templates(..., video_end)`, `load_video_end` | "구간 요약의 'the video opens/closes…'는 그 구간의 시작·끝이다. 영상 전체는 00:00:00–<실제 끝>이다. 영상 전체의 시작·끝은 처음·마지막 몇 분에 닿는 근거로만 서술". 결론 섹션 지시에 "결말을 쓰면 규칙 7을 따름" 추가. 실제 끝은 10sec 캡션 마지막 `end_time`(10min 개요의 마지막 구간은 40:00·50:00처럼 창 경계라 실제 끝 37:37·30:32·45:14보다 길다) |
| P19 (3) 결말·시작 서술 검사 | `grounding_postprocessor.boundary_claims`, `run_report` | "the video closes/ends/concludes/wraps up/finishes", "final/closing/last scene/shot/moments of the video"("…concludes this section/segment" 제외)와 "opens/begins/starts" 문장의 인용 근거 시간을 본다. 가장 늦은 인용 근거 끝이 영상 끝보다 120초 넘게 이르면 `ending_early`, 가장 이른 시작이 120초보다 늦으면 `opening_late`, 시간 있는 근거가 없으면 `*_unverifiable`. 경고 1줄 + `validation.json` `boundary_findings`, `video_end` |
| I28 | `local_llm_server.py` | `count_tokens`를 `generate_lock` 안으로 옮김 |
| 분석 도구 | `analysis/summarize_batch.py`(새 파일) | 배치 결과 폴더 요약(작업별 상한 도달, 제거 문장, 결말·시작 서술, 규칙 검사, 결론 마지막 문장) |


### 8.13 P19 영상 끝 근거·반복 경고 기준·검사 오탐 수정 (2026-10-26, 사용자 지시, 수정 전 사본 `backups/*.bak_20261026_p19b`, 커밋 `d8005b3`)

| 대상 | 파일 / 함수 | 내용 |
|---|---|---|
| P19 영상 끝 근거 | `domain_templates.load_video_ending`, writer 템플릿 "# End of the Video" 블록(`<<VIDEO_ENDING>>`), Grounding Rule 7 | 10sec 캡션 중 끝에서 60초 안에 끝나는 것들을 한 근거로 묶어 writer에 `[Source txt0 begin] … [Source txt0 end]`로 보여 준다. 규칙: 마지막 섹션에서 영상 결말을 서술할 때만 `[citation:txt0]`으로 인용. 실제 구간: `-QuCz7kxBr8` 00:36:30–00:37:37, `0RxMZBLeqRI` 00:29:30–00:30:32, `54k2g9ddy4M` 00:44:10–00:45:14. writer 프롬프트가 호출마다 517–708토큰 늘어난다 |
| txt0 처리 | `grounding_postprocessor.attach_ending_source`, `run_report.run` | 섹션이 txt0을 인용하면 그 근거를 섹션 근거 목록 끝에 붙이고 txt0을 새 번호로 바꾼다. 이후 References·규칙 검사·결말 검사는 보통 근거와 같이 처리. 마지막 섹션이 아닌 곳에서 인용하면 경고. `validation.json` `ending_source`(사용 가능 여부, 인용 섹션, 구간) |
| 설계 근거 | (코드 확인) | Deep-Reporter 그래프는 `create_openai_api` 때 노드 함수 객체를 잡아 두므로 노드 함수 교체는 효과가 없다. writer는 섹션의 `retrieved_texts`를 txtN으로 번호 매기고, 결론 섹션의 검색 질의는 결말을 항상 묻지 않으며 묻더라도 중간 구간의 "video concludes" 캡션을 찾아온다(§9.16 보고서들의 결론 질의 확인). 그래서 검색이 아니라 템플릿 블록 + 후처리 번호 변환을 택했다. Deep-Reporter 기록(`used_sources`)에는 txt0이 빠지지만(번호 범위 밖) 보고서 본문에는 그대로 남아 후처리가 변환한다 |
| P9 경고 기준 | `run_report.validate` | "writer repetition loop suspected"를 최대 반복 ≥ 5 또는 섹션이 문장 중간에서 끝날 때만 붙인다(§9.16에서 3–4회 일반 반복에 붙던 문제) |
| P19 검사 오탐 | `grounding_postprocessor.ENDING_RE`, `OPENING_RE` | "final/first … of the video’s …"(소유격) 제외 |
| 테스트 | `tests/unit/test_p9_p19.py` | 25개(경고 기준 2, 영상 끝 근거·txt0 변환·결말 검사 통과·오탐 5 추가) ALL PASS. 기존 5종 30/50/67/9/18 통과 |

- **GPU 실제 확인은 하지 않았다**(2026-10-26 GPU 사용 불가). 영상 끝 근거가 실제로 결말 오인을 줄이는지는 다음 GPU 실행에서 확인한다.

---

## 9. 검증 기록 (실제 모델)

§9.2–9.5와 §9.7은 프로세스마다 19,000 MiB 상한을 걸었다. §9.6은 20,000 MiB 규칙 해제 후라 LLM 서버 19,000 MiB, 인덱서 26,000 MiB, §9.8은 LLM 서버 19,000 MiB, 인덱서 15,000 MiB 상한이다. 모든 실행에서 자기가 띄운 PID만 종료했고, 종료 후 GPU 사용량이 실행 전 수준(다른 사용자 사용량)으로 돌아온 것을 확인했다.

### 9.1 공통 조건

- 영상 `-QuCz7kxBr8`(Video-MME, 약 32분, 농구 가젯 리뷰).
- query: `"Write a report describing what happens in this video: who takes part, what is tested, and how the tests turn out."`
- episodic 캐시: **10sec 단위만** 있는 실제 캐시(`tests/_artifacts/gpu_test`). 전처리 OpenIE를 빈 triple 18개까지 포함해 시드로 넣고, 실제 Qwen3-Embedding-4B로 만들었다(226청크, 15초, LLM 0회). 테스트 전용이며 정식 사전 인덱싱 결과가 아니다.

### 9.2 검색 스모크 (`tests/gpu/gpu_smoke.py`)

- L0(GPU 6): text 12건 0.47초, image 3건 0.04초(프레임 캐시 이후). 결과가 질의 주제(농구 가젯 테스트, 드리블 고글)와 일치했다.
- 로컬 LLM 서버(GPU 4): 로드 115초. Deep-Reporter 실제 클라이언트로 생성 2.4초.
- L1: 실제 LLM 필터 1회(프롬프트 2,396토큰, 4.4초), 검색 요청 전체 5.5초, `episodic_filter=llm`.
- Deep-Reporter `search_node` → 서비스(HTTP) → text 12건, image 3건 저장.
- 메모리 증가량: 검색 프로세스 최대 +13,743 MiB, LLM 서버 최대 +17,879 MiB.
- 참고: 첫 단계(캐시 생성, L0)는 "GPU 4–7 사용" 지시를 받기 전에 GPU 0에서 실행했다(+13,929 MiB, 20GB 미만, 종료 후 원복). 이후는 GPU 4·6만 썼다.

### 9.3 보고서 A: 스모크 (`tests/gpu/gpu_report_smoke.py`, 결과 `tests/_artifacts/gpu_report/`)

- 조건: Qwen3-VL-8B(GPU 4), 검색 L1(GPU 6). 템플릿: videomme, **규칙 4·결론 규칙 없음**. `run_report.py` 이전이라 후처리·검증은 나중에 따로 적용했다(`tests/_artifacts/pipeline_test/smoke_grounded/`).
- 결과: **성공. 5개 섹션, 2,962단어, 382초.** LLM 16회, LLM 시간 합계 361초. planner 51.3초, query 5.1–6.4초, L1 필터 4.6–5.4초(입력 2,577–3,205토큰), writer 35.7–66.5초(출력 614–1,121토큰). 16회 모두 `finish=stop`.
- GPU 최대 +18,757 MiB(LLM) / +13,737 MiB(검색).
- 관찰(상세 `REPORT_ISSUES_AND_FIXES.md`)
  - planner JSON 파싱 성공, 검색어가 영상 내용에 맞게 구체적임.
  - 텍스트 인용 109개 모두 번호 범위 안. 본문의 HH:MM:SS 23개가 모두 해당 섹션 근거에 존재.
  - 이미지 인용 14개 중 8개가 잘못된 형식, 섹션 4·5는 이미지 없음, 결론 섹션 없음.
  - 근거 원문 대조로 내용 오류 확인: 규칙 검사 unsupported 4 + miscited 5 중 실제 오류 7(오탐 `SCORE 6` ×2), 장면 오인, 섹션 설명 유입, 반복 단락.

### 9.4 보고서 B: `run_report.py` 첫 실행 + full 모드 (`tests/gpu/gpu_e2e.py`, 결과 `tests/_artifacts/gpu_e2e/`)

- 배치: LLM 서버 GPU 4, L1 검색 서비스 GPU 6, full 검색 서비스 GPU 7.
- 템플릿: 규칙 4 + 결정 5·6. **규칙 6·C0, absence 처리, 이미지 시간 기록, 번역 한자 감지·이름 보호는 이 실행 뒤에 구현했다.**
- 첫 시도는 영상 id가 `-`로 시작해서 argparse가 `--preload -QuCz7kxBr8`을 값 없는 옵션으로 해석하는 바람에 실패했다(exit 2). `--preload=<id>`, `--video-id=<id>` 형식으로 해결했다.
- **결과**: `validation.json` passed, exit 0.
  - 시간: 사전 확인 1.0초, 생성 261.5초, 후처리 0.02초, 번역 231.8초, 전체 494.4초.
  - 섹션 6개(상한 6 이내), 마지막이 `Conclusion:` 244단어, 결론 관련 경고 0.
  - LLM: 생성 19회(planner 36.8초, query 3.0–4.1초, L1 필터 3.3–4.1초·입력 2,275–3,474토큰, writer 16.1–34.2초·출력 374–794토큰) + 번역 6회(섹션당 23.5–49.2초, 재시도 0).
  - 텍스트 인용 72개 → 참조 35개, 그림 14개, `[?]` 0, 누락 프레임 0. 잘못된 이미지 형식 19개 중 4개(모두 변환).
  - 규칙 검사(실행 당시 규칙): unsupported 6 / miscited 3 / uncited 14. 이 중 `10:85`·`9:51` 2건은 부정문 오탐(대조), 7건은 결론 섹션. 현재 규칙(absence 포함)으로 다시 계산하면 unsupported 4 / miscited 3 / uncited 12 / absence 3이다.
  - 번역: 인용 `[n]` 72=72, HH:MM:SS 73=73 보존. 한자 혼입("햇明媚한", "미歇尔")과 이름 표기 불일치("제이mes", "재치"↔"자크") 확인.
  - 새로 확인한 문제: 결론 섹션의 인용 불일치, 근거 없는 추측 표현 5문장.
- **full 모드 실제 LLM** (10sec만): 질의 2개 → LLM 4회, 9.5초, 결과 12건(episodic 8, semantic 4).
- GPU 최대: GPU 4 18,811 / GPU 6 13,749 / GPU 7 13,747 MiB. 종료 후 0 / 0 / 3 MiB.

### 9.5 사전 인덱싱 시험 (A안, **사용자 지시로 중지**)

- 실행: `./run_prebuild_http.sh 4,5,6 7 --videos=-QuCz7kxBr8` (LLM 서버 GPU 4·5·6, 인덱서 GPU 7).
- 첫 시도는 출력 리디렉션 대상 `logs/` 폴더가 없어 즉시 실패했다(스크립트가 폴더를 만들기 전에 셸이 리디렉션을 처리했기 때문, GPU 미사용). 폴더를 만들고 다시 실행했다.
- 06:31:20 시작, 서버 로드 약 20초. 계획 OpenIE 호출 222회(10sec 시드 208개, 재계산 18개).
- **10sec 완료** (06:32:03–06:34:39, 약 2.6분)
  - OpenIE 캐시 226 docs 저장. 재계산 18개 중 2개는 재시도 소진 오류(`RetryError`, pydantic 검증 실패)로 빈 결과.
  - 캐시 전체에서 빈 triple 12개, 빈 entity 13개(✔ 파일 확인). 이 18개는 전처리 결과에서 triple이 비어 있거나 없어서 시드에서 제외했던 청크다.
  - 응답 파싱 실패 로그("Input should be a valid string … None/True" 등)가 반복됐다. in-process 경로도 같은 파서와 재시도를 쓰므로 HTTP 방식 고유의 문제는 아니다(✔ 코드). 다만 in-process 결과와 직접 비교하지는 않았다.
- **30sec 진행 중 중지**: 청크 76개 임베딩 저장, NER 완료, triple 추출 도중 사용자 지시("gpu 작업 당장 중지해")로 중지했다. 자기 PID 6개만 종료했고, GPU 4–7은 0/0/0/3 MiB로 돌아왔다. 중지 시점까지 서버 요청 수는 59/57/58회(재시도 포함, 마지막 06:39:54)다.
- GPU 스냅샷(06:34, 최대값 아님): LLM 서버 17,395 / 17,369 / 17,401 MiB, 인덱서 14,295 MiB.
- **남은 상태**: `cache/episodic/-QuCz7kxBr8/episodic_memory/10sec/`(완료), `30sec/`(임베딩만, OpenIE 결과 없음), `_done` 표식 없음. 다시 실행하면 10sec OpenIE 캐시를 재사용하고 30sec부터 계산한다. 불완전한 캐시이므로 검색 서비스가 409로 거부한다.
- **측정하지 못한 것**: 영상 1개 전체 소요 시간(따라서 50개 영상 예상 시간), 3min·10min 처리, 완성된 4개 단위 캐시로 검색·보고서 생성. → §9.6에서 영상 1개 전체를 측정했다.

### 9.6 영상 3개 사전 인덱싱 + 보고서 (분할 적용 전 코드, **사용자 지시로 중지**)

- 결과 위치: `outputs/3videos_20261022_120438/` (`prebuild_indexer.log`, `prebuild_llm_<i>_gpu<g>.log` 7개, `summary.json`). 실행 스크립트는 당시 판 `experiments/gpu_3videos.py`(현재 판은 §8.11).
- 영상: `-QuCz7kxBr8`(Sports/Basketball), `0RxMZBLeqRI`(Knowledge/Humanity & History), `54k2g9ddy4M`(Film & Television/News Report). 서로 다른 도메인으로 골랐다(`long_test.json`의 domain·sub_category). query는 세 영상 공통 `"Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes."`.
- 배치: 20,000 MiB 규칙 해제(사용자 지시) 후, LLM 서버 7개를 GPU 4,4,5,5,6,6,7에(각 19,000 MiB 상한, 포트 18710–18716) 띄우고, 인덱서를 GPU 7에 26,000 MiB 상한으로 실행. 서버 준비 25.0초. OpenIE 동시성 12(기본 `ThreadPoolExecutor`)를 7개 서버에 순환 배분.
- 단계별 실측 (서버 로그 `chat.completions:` 줄 기준)

  | 영상/단위 | 시간 | 호출 | 상한 도달 | 비고 |
  |---|---|---|---|---|
  | 영상 1 30sec | 12:05:21–12:11:44 (6.4분) | 153 | 0 | 계획 152 + 재시도 1 (pydantic `True` 오류) |
  | 영상 1 3min | 12:11:44–12:13:41 (2.0분) | 26 | 0 | |
  | 영상 1 10min | 12:13:41–12:16:29 (2.8분) | 9 | 1 | 잘린 1건은 재시도에서 성공 |
  | **영상 1 전체** | **668초** (10sec는 시험 실행 캐시 재사용) | 188 | 1 | 완료 표식 생성 |
  | 영상 2 10sec | 12:16:29–12:16:49 | 8 | 0 | 시드 180, 재계산 4 |
  | 영상 2 30sec | 12:16:49–12:23:43 (6.9분) | 124 | 0 | |
  | 영상 2 3min | 12:23:43–12:25:52 (2.2분) | 22 | 0 | |
  | 영상 2 10min | 12:25:52– (중지 시점까지) | 18 | 12 | 열거 폭주·긴 출력으로 잘림 반복 |
- 완성된 영상 1 캐시: 빈 triple 10sec 12 / 30sec 0 / 3min 0 / 10min 0. 청크당 평균 triple 12.3 / 22.2 / 34.5 / 70.2. 같은 (주어, 술어) 연속 최대 7.
- 중지: 영상 2의 10min에서 재시도가 이어져 사용자에게 보고했고, 사용자가 중단·원인 분석을 지시했다. 12:36에 인덱서만 SIGTERM으로 끝내 스크립트가 자기 서버 7개를 정리하게 했다(인덱서 exit −15, 1,938.7초). 서버별 호출 52/52/52/51/51/51/51(합계 360). 보고서 단계는 시작하지 않았다.
- GPU 최대(우리 프로세스만, 다른 사용자 없음): GPU 4 36,662 / 5 37,192 / 6 36,700 / 7 35,782 MiB. 종료 후 0/0/0/3 MiB.
- 원인 분석과 대응은 §5.2.1, §9.7, `REPORT_ISSUES_AND_FIXES.md` I22–I24.

### 9.7 OpenIE 디코딩 비교 실험 (`analysis/openie_degeneration_exp.py`, 결과 `results/openie_exp/`)

- 목적: 출력 상한 초과(§5.2.1)가 디코딩 설정(반복 억제)으로 해결되는지 확인.
- 조건: 12:41:18–13:25:52, GPU 5·6·7에 설정마다 1개 프로세스(19,000 MiB 상한, 다른 사용자와 GPU 공유라 생성 속도 약 9토큰/초). WorldMM `Qwen3VLModel`과 같은 chat 템플릿·모델 기본 생성 설정을 재현한 텍스트 전용 생성. 대상: `0RxMZBLeqRI` 10min 청크 0·1·2(실패 청크)와 `-QuCz7kxBr8` 10min 청크 0, 각 2회, NER → triple.
- 결과 (설정당 8건, NER+triple 16회)

  | 설정 | 파싱 실패 | 상한 도달 | 폭주(연속 ≥4) | 생성 토큰 | 종료 |
  |---|---|---|---|---|---|
  | base (모델 기본) | 7 | 7 | 2 | 22,771 | 13:25:52 |
  | rp105 (`repetition_penalty=1.05`, 프롬프트 포함) | 1 | 1 | 4 | 12,731 | 13:06:07 |
  | rp110gen (1.10, 생성 토큰에만) | 2 | 1 | 0 | 10,799 | 13:02:17 |
- 해석: 실패 청크만 골라 시험한 값이라 전체 비율이 아니고 표본이 작다. rp105는 폭주를 못 막았다(54·115회). rp110gen은 폭주가 없었지만 2건에서 1,300–1,400토큰을 생성하고도 유효 triple이 2개였다(원문 미저장, 원인 미확인). HF `repetition_penalty`는 프롬프트 토큰에도 적용된다(✔ transformers 코드). → 디코딩 변경 기각(결정 9).

### 9.8 영상 3개 재실행 (분할·구제 적용, GPU 6·7만, **감시 장치로 중단**)

- 결과 위치: `outputs/3videos_20261022_141051/` (`config.yaml`, `llm_server.log`, `prebuild_indexer.log`, `summary.json`). 실행 전 dry-run: 영상 1 12회, 영상 2 178회, 영상 3 240회(합계 430회).
- 배치: LLM 서버 1개 GPU 7(19,000 MiB), 인덱서 GPU 6(15,000 MiB). 시작 전 다른 사용자 사용량 GPU 6 18,365 / GPU 7 23,017 MiB, 여유 확인 통과.
- 경과: LLM 서버 준비 20.0초 → 인덱서 시작, 14:11:26 영상 1 인덱싱 시작(분할 OpenIE 진입) → GPU 7의 다른 사용자 프로세스가 약 34.2GB로 늘어 합계 48,446 MiB가 감시 기준(47,500 MiB)을 넘음 → **우리 프로세스 2개만 종료**(인덱서 exit −15, 41.2초).
- 영향: LLM 호출 0회, 캐시 파일 변경 없음(✔ 파일 시각 확인). 종료 후 GPU 6 18,365 / GPU 7 32,661 MiB(다른 사용자만), 우리 PID 잔존 0. 다른 사용자 프로세스는 살아 있었다. 합계가 49,140 MiB의 약 98.6%까지 갔던 순간 다른 사용자 쪽 할당 실패가 있었는지는 확인할 수 없다.
- 판단: 다른 사용자 사용량 관측 범위(GPU 6 약 18–30GB, GPU 7 약 18–34GB)에 Qwen3-VL-8B 프로세스(18–19GB)를 더하면 두 GPU 모두 용량을 넘을 수 있다. 재개 방식은 사용자 결정 대기였다(`REPORT_ISSUES_AND_FIXES.md` I27). 이후 경과는 §9.9와 §2.2(2026-10-25 GPU 4–7 허용).

### 9.9 영상 3개 대기 후 자동 시작 (GPU 6·7만, **시작 조건 미충족으로 시작하지 않음**)

- 사용자 지시(2026-10-22): "2시간 있다가 영상 3개에 대해서 검증 수행, report 작성까지. gpu 6,7 사용, 다른 user의 작업을 중단하지 않도록."
- 실행: `experiments/delayed_gpu_3videos.py`(§8.11)를 16:05:48에 `setsid nohup`으로 시작. 인자는 모두 기본값(`gate.json`: `delay_sec` 7200, `hold_sec` 600, `max_wait_sec` 21600, `margin_mib` 1500, `aux_cap_mib` 15000, `abort_used_mib` 47500). 시작 전 CPU 점검으로 판단·기록 동작만 확인했다(margin 99,999로 시작 불가 조건, 결과 exit 2).
- 결과 위치: `outputs/3videos_20261022_160548_gated/` (`gate_run.log`, `gate.json`의 `choice: null`).
- 경과: 18:05:48까지 대기 → 18:15:21부터 00:05:36까지 **698번 판단, 시작 조건(남는 여유 ≥ 1,500 MiB) 만족 0번** → 00:06:06 `no safe headroom within max wait; not starting`으로 종료(`gate.json`·`gate_run.log` 파일 시각). 가장 큰 여유는 18:35–18:36의 **−961 MiB**(LLM GPU 7, aux GPU 6). 판단 시 고른 배치는 LLM GPU 6이 382번, GPU 7이 316번.
- 다른 사용자 사용량(판단 시점의 최근 10분 최대값, `gate_run.log`에서 집계):

| 시간대 | GPU 6 | GPU 7 | 가장 큰 여유 |
|---|---|---|---|
| 18시 | 30.4–35.1 GB | 29.0–34.2 GB | −961 MiB |
| 19시 | 32.2–36.1 GB | 28.5–35.6 GB | −2,221 MiB |
| 20시 | 35.3–37.4 GB | 33.0–37.0 GB | −4,453 MiB |
| 21시 | 32.3–37.5 GB | 33.7–37.2 GB | −3,777 MiB |
| 22시 | 31.8–37.6 GB | 34.4–38.1 GB | −5,009 MiB |
| 23시 | 32.6–38.2 GB | 37.3–39.2 GB | −5,715 MiB |
| 00시 | 36.3–37.4 GB | 38.7–39.0 GB | −7,825 MiB |

- 영향: 우리 GPU 프로세스는 하나도 띄우지 않았다(대기 스크립트 PID 46718만, GPU 미사용). 캐시 변경 없음.
- 판단: 다른 사용자가 37–39GB를 쓰는 동안에는 남는 메모리가 10–12GB라 LLM 서버(19,000 MiB 상한)도 인덱서·검색 서비스(15,000 MiB 상한)도 들어갈 수 없다. 조건을 느슨하게 했다면 감시 장치가 곧 중단시켰거나 다른 사용자 프로세스의 메모리 할당이 실패했을 수 있다. 이 결과로 사용자가 서버 이전을 준비했다(`MIGRATION_HANDOFF.md`). 이후 2026-10-25에 이 서버의 GPU 4–7 사용이 허용됐다(§2.2).


### 9.10 C-1 영상 3개 사전 인덱싱 (분할·구제 적용, GPU 4–7, **완주**)

- 사용자 지시(2026-10-25): GPU 4–7 사용, 서버 메모리 상한 없이 사용 가능한 메모리를 쓰고, 작업을 GPU 4–7에 고르게 분배.
- 결과 위치: `outputs/c1_prebuild_20261025_121542/` (`summary.json`, `gpu_3videos.out`, `prebuild_indexer.log`, `llm_server_<i>_gpu<g>.log` 7개, `monitor.log`, `guard2.log`, `run_c1.sh`).
- 배치: `experiments/gpu_3videos.py --llm-gpus 4,4,5,5,6,6,7 --aux-gpu 7 --llm-cap-mib 0 --aux-cap-mib 0 --skip-reports`. LLM 서버 7개(GPU 4·5·6에 2개씩, GPU 7에 1개, 포트 18810–18816), 인덱서 GPU 7. 감시 기준 47,500 MiB. 시작 전 GPU 4–7 사용량 0/0/0/3 MiB, 다른 사용자 프로세스 0개.
- 실행 전 점검: CPU 테스트 5종 30/50/67/9/18개 통과, dry-run 430회(12/178/240), 캐시 사본 `backups/cache_before_c1_20261025/`, git 커밋 `4a52b82`.
- **실행 중 발견한 감시 스크립트 결함**: `run_c1.sh`의 중단 조건(호출 > 645 또는 90분)은 백그라운드 python에 SIGINT를 보내는데, 비대화형 bash가 `&`로 띄운 프로세스는 SIGINT를 무시하도록 시작된다(✔ `/proc/<pid>/status` `SigIgn`). 그래서 같은 조건으로 우리 프로세스 그룹에 SIGTERM을 보내는 감시를 따로 붙였다(`guard2.log`). 실제로 발동하지는 않았다.
- 결과 (`summary.json`, 완료 표식, 서버·인덱서 로그)

| 항목 | 값 |
|---|---|
| 전체 | exit 0, 1,643.3초(서버 로드 120초 포함), **호출 430회 = 계획**, `failed_requests` 0, 감시 중단 없음, 종료 후 GPU 사용량 0/0/0/3 MiB, 우리 PID 잔존 0 |
| 영상별 | `-QuCz7kxBr8` 199.7초(12회), `0RxMZBLeqRI` 731.1초(178회), `54k2g9ddy4M` 678.4초(240회) |
| 분할 | 영상 1: 10min 1청크 3조각, 영상 2: 3청크 11조각, 영상 3: 3청크 8조각. 실패 조각 0. 분할 단계는 영상마다 85–117초 걸렸고 그동안 7개 서버 중 일부만 일했다(서버 사용률이 낮음) |
| 파싱 실패와 구제 | 5건, 모두 1회 호출로 구제(`salvaged_triples` 5, `salvaged_ner` 0, 재시도 0). 3건은 출력 상한 2,048토큰에서 잘림(`finish=length`: 영상 1의 분할하지 않은 10min 청크 2건(프롬프트 1,707·1,576토큰), 영상 3의 분할 조각 1건(1,342토큰)), 2건은 스키마 검증 오류(영상 3 10min·30sec triple). 잘린 3건의 끝은 같은 주어의 나열이었다 |
| 폭주 절단 | 146개(영상 1 6, 영상 2 68, 영상 3 72; 완료 표식의 누적값 차이) |
| 빈 결과 (`cache_empty`) | 10sec만: 영상 1 triple 12·entity 13(이전 실행의 캐시 그대로), 영상 2 2·2, 영상 3 1·0. 30sec·3min·10min은 0 |
| 출력량·속도 | 생성 114,208토큰(호출 평균 266, 최대 2,048), 호출당 평균 48.5초·최대 209.7초. 인덱싱 구간 기준 약 75토큰/초(추정: 로드 120초를 뺀 1,523초로 나눔) |
| 메모리 | GPU별 최대 35,466 / 35,758 / 35,436 / 35,826 MiB(4/5/6/7). LLM 서버 1개 약 17.0–17.5GB(12:18 `nvidia-smi`), 인덱서는 시작 시 약 8.0GB |
| 서버 오류 로그 | `Qwen3VL generation error: Already borrowed` 261건. 모두 WorldMM 생성 함수의 재시도(최대 5회)로 성공했고 500 응답·`Generation failed`·`Token counting failed`는 0건(`REPORT_ISSUES_AND_FIXES.md` I28) |

- 완전성: 실행 후 dry-run에서 세 영상 모두 남은 호출 0회, 단위별 캐시 청크 수 = 캡션 수(226/76/13/4, 184/62/11/4, 272/91/16/5).
- 시간 추정과 비교: 계획 단계 추정 30–40분, 실제 27.4분. §5.2.2의 서버 7개 실측(10/22)과 같은 수준이다.

### 9.11 C-2 분할 전후 OpenIE 비교 (`analysis/compare_openie_cache.py`, 결과 `results/c2_openie_compare.json`)

- 기준: `backups/cache_before_split_20261022/`(10/22 12:04 실행의 결과). 분할이 적용되는 단위는 1,100토큰 넘는 청크가 있는 10min뿐이므로, **분할 전후 비교는 영상 1의 10min 4청크가 유일**하다. 영상 2의 10sec·30sec·3min은 분할 대상이 아니라 다시 계산했을 때의 편차를 본다. 영상 2의 10min은 분할 전 실행이 끝나지 않아 기준이 없다.

| 대상 | 전: triple 합 / 최대 연속 | 후: triple 합 / 최대 연속 | 같은 청크 | Jaccard 평균 |
|---|---|---|---|---|
| 영상 1 10min (4청크) | 281 / 7 | 303 / 15 | 0/4 | 0.033 |
| 영상 2 10sec (184) | 2,235 / 6 (빈 triple 4) | 2,265 / 6 (빈 triple 2) | 182/184 | 0.989 |
| 영상 2 30sec (62) | 1,638 / 9 | 1,576 / 15 | 0/62 | 0.27 |
| 영상 2 3min (11) | 351 / **26** | 372 / 15 | 0/11 | 0.216 |

- 영상 1 10min 청크별 triple(전 → 후): 분할된 청크(1,733토큰) 64 → **160**, 나머지 59 → 59, 68 → 25, 90 → 59(이 청크는 연속 15에서 절단됨).
- 영상 2 10sec: 182청크는 전처리 시드라 같다. 다시 계산한 4청크 중 2개는 전에 비었다가 16·14개가 됐고, 2개는 여전히 비었다(NER 결과가 비어 있음).
- 절단에 걸린 청크의 예: `basketball court – features – hoop, trampoline, landscaping, …`(장면 요소 나열), `Joshua Liendo – is – …`, `Roma – are portrayed in – …`(같은 주어 반복 서술).
- 해석
  - 분할로 확인된 효과: 10min 긴 청크에서 출력이 잘려 청크당 최대 15회 재시도하던 문제(§9.6)가 없어졌다(호출 수 = 계획, 실패 조각 0). 분할된 청크의 triple이 64 → 160개로 늘어 더 많은 내용이 그래프에 들어갔다(표본 1청크).
  - 다시 계산하면 같은 입력이라도 triple 집합이 크게 다르다(Jaccard 0.2–0.3). 그래서 영상 1 10min의 전후 차이를 분할 효과만으로 볼 수 없다.
  - 폭주 절단은 비정상 반복과 정당한 나열을 구분하지 못한다(§11).
- 새로 만든 캐시 전체 통계(빈 결과, triple 수, 최대 연속)는 `results/c2_openie_compare.json`의 `new_only`에 있다. 30sec·3min·10min의 빈 triple은 0이다.

### 9.12 C-3 4개 단위 캐시로 검색 확인 (`experiments/gpu_retrieval_probe.py`, 결과 `outputs/c3_probe_20261025_125223/`)

- 배치: LLM 서버 1개 GPU 4(L1·full 필터용, 포트 18830), 검색 서비스 L0/L1/full을 GPU 5/6/7(포트 18840–18842), 메모리 상한 없음. 서비스마다 config 사본(`config_<mode>.yaml`)에서 `retrieval.episodic_filter`만 다르다.
- 방법: 영상 3개 각각 `POST /load` 후, 모드마다 같은 text 요청 3개(쿼리 2개씩, topk 20 = Deep-Reporter `text_topk`)와 image 요청 1개. 질의는 영상과 무관한 일반 질의(주요 인물, 사건 순서, 결말)이고 한 요청 안의 두 쿼리는 서로 비슷하게 만들었다.
- 결과 (`probe.json`): 불러오기·검색 36건 모두 200, 감시 중단 없음, 종료 후 GPU 0/0/0/3 MiB, 우리 PID 잔존 0.

| 항목 | L0 | L1 | full |
|---|---|---|---|
| text 지연 (서비스 `elapsed_sec`, 9건) | 0.72–1.36초, 평균 0.87 | 4.41–7.85초, 평균 5.32 | 29.68–38.75초, 평균 34.17 |
| image 지연 (3건) | 1.67–2.48초(프레임 첫 추출) | 0.06초 | 0.05–0.06초 |
| episodic 근거 수 (설정 8) | 9건 모두 8 | 9건 모두 8 | 4–8(평균 6) |
| 단위 구성 합계 (10sec/30sec/3min/10min) | 26/18/15/13 | 14/33/18/7 | 11/18/6/19 |

- 불러오기: 첫 영상은 시작 때 미리 불러옴(45초, 모델 로드 포함), 이후 영상 전환은 2.0–2.4초. 서비스 GPU 사용량 13,739 → 16,223 → 14,697 MiB로 세 번째 영상에서 줄어, 영상 전환 때 이전 영상 메모리가 풀린다(누적 증가 없음).
- LLM 서버: 호출 99회(L1 9 + full 90), `Already borrowed` 0건(요청이 하나씩 들어온 실행). GPU 4 최대 23,779 MiB(상한 없는 서버 1개, full 모드의 긴 프롬프트).
- Deep-Reporter 타임아웃(600초) 대비: 가장 느린 full도 39초 이하라 여유가 크다.
- full 모드 근거 부족(I15 잔여 한계): WorldMM `_filter_with_llm`은 쿼리마다 `final_top_k`(4)까지 채우지만(`episodic/memory.py:405-418`), 서비스가 두 쿼리의 결과를 합치며 중복을 빼므로 겹치면 8개보다 적다. 이번 질의는 일부러 비슷하게 만들어 겹침이 컸다.
- 단위 구성: L0는 후보 수 설정(3/3/2/1)대로 고르게, L1은 30sec·3min 위주, full은 10min 비중이 크다(19/54). full이 고른 10min에는 `0RxMZBLeqRI`의 잘린 캡션(I22)이 들어갈 수 있다.
- 근거 내용의 관련성 평가는 하지 않았다(C-4 보고서 분석에서 근거 원문 대조로 본다).

### 9.13 C-4 4개 단위 캐시로 보고서 3건 (`experiments/gpu_report_batch.py`, 결과 `outputs/c4_reports_20261025_130200/`)

- 배치: 묶음 3개(GPU 4/5/6에 LLM 서버 + 검색 서비스 각 1개, 상한 없음)가 영상 1개씩 병렬로 처리. GPU 7은 일이 없어 쓰지 않았다. query는 `experiments/gpu_3videos.py`의 `QUERY`("main people or subjects, key events in order, how the video concludes"). 현재 기본 설정(L1, 규칙 4·6, C0 `written`, 결론, 상한 6, 번역).
- 실행: 3건 모두 exit 0, `validation.json` status `passed`(오류 0). 688–836초(생성 270–333초 + 번역 414–532초). LLM 호출 24/27/30회, 출력 잘림 0, 500 응답 0. GPU 최대 34.5/38.7/36.2GB, 감시 중단 없음, 종료 후 원상 복귀.
- 측정 (`validation.json`, `metrics.json` = `analysis/analyze_report.py`)

| 항목 | B (10sec, §9.4) | `-QuCz7kxBr8` | `0RxMZBLeqRI` | `54k2g9ddy4M` |
|---|---|---|---|---|
| 섹션 / 문장 / 인용 문장 | 6 / 107 / 32 | 6 / 142 / 38 | 5 / 87 / 23 | 6 / 113 / 31 |
| 규칙 검사 unsupported / miscited / uncited | 6 / 3 / 14 | 4 / 1 / **25** | 1 / 0 / 7 | 0 / 0 / 1 |
| 단락 유사도 상위 1% / 0.5 이상 쌍 | 0.235 / 0 | 0.085 / 0 | 0.068 / 0 | 0.067 / 0 |
| 섹션 간 유사 문장 | 3 | 4 | 1 | 1 |
| 인용된 근거 episodic / semantic / image | 34 / 6 / 16 | 27 / 3 / 7 | 30 / 0 / 12 | 36 / 3 / 9 |
| 이미지-텍스트 시간 차 중앙값 / 최대 | (미기록) | **665 / 1,245초** | 0 / 1,135초 | 5 / 605초 |
| 번역 성공 섹션 | 6/6 | 6/6(한자·가나 잔존 2) | **2/5** | **4/6**(잔존 1) |
| LLM 호출 프롬프트 최대(대부분 L1 필터) | L1 필터 입력 2,275–3,474토큰(§9.4) | 11,570 | 15,125 | 12,807 |

- 근거 원문 대조 (캡션 파일의 전체 원문과 비교. 보고서 1은 의심 문장을 골라 본 것이고, 2·3은 숫자·인용부호가 있는 인용 문장에서 무작위 4개)
  - 보고서 2: 4문장 모두 근거와 일치.
  - 보고서 3: 4문장 중 2개 일치, 1개 **근거 없음**("The video concludes with the reopening of schools and Liendo's gold medal victory [30]" — [30](39:00–39:30)에는 Liendo·금메달이 없고 실제 마지막은 45:10의 CBC 로고 화면), 1개는 근거 없는 해석 추가.
  - 보고서 1: 1개 일치(섹션 1은 3min 캡션 문장을 거의 그대로 옮김), 1개 **결말 오인**("The video closes with ... 00:18:29 ... Shot Coach [22]" — [22]는 18:00–21:00 3min 캡션이 자기 구간을 "The video closes with a close-up of the Shot Coach device"라고 요약한 문장이다. 실제 영상은 37:37까지이고 엔드 스크린으로 끝난다), 1개 **화자·시점 오류**("After the game, the man in the blue jersey ... 'I like it with the gadget on' [24]" — [24](00:09:00)에서는 검은 후드 남성이 파란 저지 남성에게 한 말).
- 결론 섹션: 보고서 1은 "climax at 00:18:30", 참가자 "three men"(섹션 1은 six men)으로 틀렸다. 보고서 2·3은 주제 요약이고 실제 마지막 장면(2: 국기와 회전 지구본 후 암전, 3: 공항 장면 후 CBC 로고)은 서술하지 않았다.
- 구조: 보고서 1의 섹션 4(20–31분) 뒤에 섹션 5 "Final Game Dynamics"(18:30)가 와 시간 순서가 뒤집혔다. 섹션 3은 긴 단락 여러 개에 인용이 없다(uncited 25의 대부분).
- 번역 실패(자리표시자 불일치)는 자리표시자 수만으로 설명되지 않는다(성공 섹션 최대 78개, 실패 섹션 최소 29개). 실패는 고유명사가 많은 영상 2·3에서만 났다. 원인 미확정.
- 해석 요약: 근거와 문장이 맞는 비율은 표본에서 높지만(11문장 중 근거 일치 7), 영상 전체 흐름(결말, 시간 순서, 화자)에서 오류가 나왔다. 4개 단위 근거 중 3min·10min 요약의 "the video closes/opens" 같은 구간 내부 표현이 영상 전체 서술로 옮겨지는 새 유형을 확인했다(`REPORT_ISSUES_AND_FIXES.md` P19). 표본이 작아 비율로 일반화하지 않는다.

### 9.14 C-5 결정 4(C0) 효과 측정 (`experiments/gpu_report_batch.py`, 결과 `outputs/c5_c0_20261025_132851/`)

- 조건: 영상 1(`-QuCz7kxBr8`)·영상 3(`54k2g9ddy4M`)(10min 캡션 잘림 없음) × C0 켬(`previous_sections_context: written`, 변형 `c0_written`) / 끔(`deep_reporter`, `c0_off`) × 2회 = 8건. 번역 끔. 묶음 4개(GPU 4–7, 각 LLM 서버 + 검색 서비스, 상한 없음). query는 C-4와 같다.
- **첫 시도 중단(13:21–13:27, `outputs/c5_c0_20261025_132130/`)**: 두 서비스가 같은 영상을 동시에 불러오다 HippoRAG가 다시 쓰는 중인 OpenIE 캐시 파일을 읽어 HTTP 500(`json.decoder` 오류)이 났다(I29). 실패는 `54k2g9ddy4M__c0_off__r1` 1건(exit 2, 1.7초)이고, 중단 전에 4건이 exit 0으로 끝났다(영상 1 켬 r1·r2, 영상 1 끔 r1, 영상 3 켬 r1). 이 4건은 조건을 맞추기 위해 비교에 쓰지 않는다. 참고로 그 4건(켬 3, 끔 1)의 서버 로그에 출력 8,192토큰 도달은 0건이다. 우리 프로세스 그룹만 종료하고, 캐시 12개 파일이 정상이며 통계가 C-1 직후와 같음을 확인했다(사본 `backups/cache_after_c1_verified_20261025/`). 영상별 불러오기 잠금을 넣고(`402d6f3`) 8건을 다시 실행했다. 첫 시도 결과는 쓰지 않는다(`outputs/c5_c0_20261025_132130/ABORTED.txt`).
- 실행: 8건 모두 exit 0, `validation.json` status `passed`. 감시 중단 없음, GPU 최대 35.3–36.6GB.
- 측정 (작업별 LLM 호출은 Deep-Reporter 세션 시작·끝 시각으로 서버 로그를 잘라 계산. 두 작업은 경계에서 1건이 섞여 20건으로 셌다)

| 작업 | 섹션 | 문장 | 완전 중복 문장 | 단락 유사도 상위 1% / 0.5 이상 쌍 | 결론 섹션 지적 | writer 프롬프트 평균 | writer 지연 평균(정상) | 출력 8,192 도달 |
|---|---|---|---|---|---|---|---|---|
| 영상 1 끔 r1 | 4 | 82 | 0 | 0.039 / 0 | 4 | 4,673 | 34.2초 | 0 |
| 영상 1 끔 r2 | 6 | 125 | 1 | 0.155 / 0 | 4 | 4,727 | 32.5초 | 0 |
| 영상 3 끔 r1 | 6 | 105 | 0 | 0.052 / 0 | 0 | 5,124 | 28.5초 | 0 |
| 영상 3 끔 r2 | 6 | 157 | 4 | 0.219 / 1 | 0 | 5,523 | 38.5초 | 0 |
| 영상 1 켬 r1 | 6 | 424 | **295** | 0.139 / 0 | 1 | 5,263 | 36.8초 | **1** |
| 영상 1 켬 r2 | 6 | 107 | 0 | 0.085 / 0 | 7 | 4,765 | 28.6초 | 0 |
| 영상 3 켬 r1 | 6 | 310 | **194** | 1.0 / **900** | 1 | 5,897 | 29.1초 | **1** |
| 영상 3 켬 r2 | 6 | 189 | 2 | 0.111 / 0 | 1 | 4,837 | 50.2초 | 0 |

- **writer 반복 루프**: C0 켬 r1 두 건에서 writer 출력이 8,192토큰(Deep-Reporter가 보내는 `max_tokens`)까지 같은 문장 묶음을 되풀이했다(영상 1 섹션 2: 4문장 묶음 약 75회, 영상 3 섹션 3: 3문장 묶음 약 25회, 각 약 6분). 이 출력이 그대로 보고서에 들어갔고 검증은 `passed`였다(반복 검출 없음). 영상 1 켬 r1은 반복이 한 단락 안에 있어 단락 유사도 지표로도 잡히지 않았다(0.5 이상 쌍 0).
- 요약: 루프는 C0 켬 2/4, 끔 0/4(C-4의 C0 켬 3건은 0/3). writer 프롬프트는 켬이 평균 142토큰 길다(5,191 vs 5,049). 루프를 뺀 단락 유사도·섹션 간 유사 문장·결론 지적 수는 켬과 끔 사이에 일관된 차이가 없다.
- 판단: 표본 4 대 4로는 C0가 루프의 원인인지, 반복·결론 지적을 줄이는지 판단할 수 없다(2/4 대 0/4의 Fisher 정확검정 양측 p ≈ 0.43, 계산값). C0의 기대 효과(반복·결론 인용 불일치 감소)는 이 표본에서 확인되지 않았다. 확실한 것은 (1) writer가 상한까지 반복하는 루프가 실제로 생기고 (2) 지금의 검증·지표가 그것을 막지도 표시하지도 못한다는 것이다(`REPORT_ISSUES_AND_FIXES.md` P9).

### 9.15 재시도·수정 이력 요약 (2026-10-22 – 10-25)

실행이 중단·실패·미시작된 뒤 무엇을 바꿔 다시 했는지를 한 곳에 모았다. 상세는 각 절과 `REPORT_ISSUES_AND_FIXES.md`.

| # | 시도 | 왜 멈췄나 / 무엇이 문제였나 | 무엇을 어떻게 바꿨나 | 결과 |
|---|---|---|---|---|
| 1 | 사전 인덱싱 시험 첫 실행 (10/22 06:31, §9.5) | 출력 리디렉션 대상 `logs/` 폴더가 없어 즉시 실패(셸이 스크립트보다 먼저 리디렉션 처리) | 폴더를 만들고 같은 명령 재실행(I20) | 10sec 완료 후 사용자 지시("gpu 작업 당장 중지해")로 30sec 도중 중지 |
| 2 | 영상 3개 사전 인덱싱 (10/22 12:04, §9.6) | 영상 2의 10min에서 OpenIE 출력이 2,048토큰에 잘려 청크당 최대 15회 재시도, 정체 → 사용자 지시로 중지 | 원인 분석(I22–I24), 디코딩 설정 비교 실험(§9.7, 기각), **긴 청크 분할 OpenIE + 잘린 응답 구제 + 연속 15개 초과 절단** 구현(결정 9), 영향 받은 캐시 삭제(결정 10) | → #3, #5 |
| 3 | 분할·구제 적용 후 재실행 (10/22 14:10, GPU 6·7, §9.8) | 다른 사용자 프로세스가 34.2GB로 늘어 GPU 7 합계 48,446 MiB > 감시 기준 47,500 → 41초 만에 우리 프로세스만 종료 | 대기 후 여유 확인 시작 스크립트 `experiments/delayed_gpu_3videos.py` 작성(최근 10분 최대 사용량 + 상한 + margin 판단) | → #4 |
| 4 | 대기 후 자동 시작 (10/22 16:05 – 10/23 00:06, §9.9) | 698번 판단 중 시작 조건 만족 0번(다른 사용자 10분 최대 30–39GB) | 사용자가 서버 이전 준비(`MIGRATION_HANDOFF.md`), 10/25 이 서버 GPU 4–7 사용 허용 | → #5 |
| 5 | C-1 사전 인덱싱 (10/25 12:15, GPU 4–7, §9.10) | (중단 없음) 실행 중 발견: `run_c1.sh`의 자동 중단 조건이 SIGINT를 보내는데 백그라운드 python이 SIGINT를 무시하도록 시작돼 동작하지 않는 상태 | 같은 조건으로 우리 프로세스 그룹에 SIGTERM을 보내는 감시를 따로 붙임(`guard2.log`). 이후 실행은 `setsid`로 별도 세션에 띄워 그룹 단위로 멈출 수 있게 함 | **완주**: 호출 430회 = 계획, 재시도 0, 실패 0. 감시 발동 없음 |
| 6 | C-3 검색 확인 (10/25 12:52, §9.12) | (실패 없음) 나중에 확인: 서비스 3개가 시작하며 같은 영상을 동시에 미리 불러와 I29 충돌이 날 수 있는 구성이었음 | (사후) I29 기록 | 36건 성공. 충돌은 일어나지 않았음 |
| 7 | C-5 첫 시도 (10/25 13:21, §9.14) | 두 서비스가 `54k2g9ddy4M`을 동시에 불러와 OpenIE 캐시 파일 읽기 실패(HTTP 500) → 1건 exit 2 | 우리 프로세스 그룹만 종료, 캐시 12개 파일 무결성 확인(통계 = C-1 직후), 사본 `backups/cache_after_c1_verified_20261025/`. `experiments/gpu_report_batch.py`가 run_report 전에 영상별 잠금을 잡고 직접 불러오게 수정(`402d6f3`) | → #8 |
| 8 | C-5 재실행 (10/25 13:28, §9.14) | (중단 없음) | — | 8건 모두 exit 0·`passed`, 불러오기 실패 0. 대신 writer 반복 루프 2건(P9)이 새로 드러남 |

- 사전 인덱싱의 OpenIE 문제(#2)는 #5에서 해결이 확인됐다. 운영상 실패(#1, #3, #4, #7)는 각각 원인을 확인하고 바꾼 뒤 다시 실행했다.
- 아직 해결되지 않은 것은 보고서 품질 문제다(P9 writer 루프, P19 결말 오인, P8·P4 흐름 오류, P15 번역 실패). 대응은 사용자 결정 대기다(§13.3).

### 9.16 P9·P19 수정 후 실제 모델 확인 (`outputs/p9p19_check_20261025_141401/`, 요약 `batch_summary.json`)

- 조건: 영상 3개 × C0 켬(`written`, 결정 16에서 유지) × 3회 = 9건, 번역 끔(결정 16: 영어 보고서 품질 우선), 묶음 4개(GPU 4–7, 상한 없음, 서버 `max_tokens_cap` 3,072). 14:14–14:32. 사용자가 허용한 GPU 시간(약 15:08까지) 안에 끝나도록 15:00 강제 종료 감시를 걸었고 발동하지 않았다. GPU 최대 37.1/40.3/37.1/39.2GB(4/5/6/7), 감시 중단 없음, 종료 후 GPU 4–7 0/0/0/3 MiB, 우리 PID 잔존 0. GPU 0–3의 다른 사용자 프로세스는 건드리지 않았다.
- 실행: 9건 모두 exit 0·`passed`. 생성 296.9–417.5초.
- **P9 (a)(c)(d)**
  - 상한 도달 2/9(둘 다 `0RxMZBLeqRI`, 섹션 5): 130.5초·133.9초에 끊김(수정 전 C-5 루프는 8,192토큰까지 약 6분). 그 두 보고서의 생성은 403.8·417.5초, 나머지 7건은 296.9–361.7초.
  - 같은 문장 제거: 상한 도달 섹션에서 37개(최대 38회 반복)·39개(최대 15회) 제거, 두 섹션 모두 "문장 중간 끝" 경고. 그 밖에 `-QuCz7kxBr8` r2 섹션 3에서 10개(최대 3회), `54k2g9ddy4M` r1–r3에서 1–3개(최대 2–4회) 제거.
  - 경고 기준(최대 반복 ≥ 3이면 "loop suspected")은 3–4회 반복인 일반 반복에도 붙었다(9건 중 3건). 실제 루프(상한 도달)와 구분하려면 기준을 올리거나 상한 도달과 묶어야 한다(사용자 결정 필요).
- **P19 (1)(3)**: 같은 검사 함수(`boundary_claims`)를 수정 전 보고서에도 적용해 비교했다.

| 기준 | 보고서 | `ending_early` 문장(보고서당) | 결론 섹션의 `ending_early` | `ending_unverifiable` |
|---|---|---|---|---|
| C-4 (수정 전, 번역 포함) | 3 | 6 (2.0) | 2/3 | 0 |
| C-5 C0 켬 (수정 전) | 4 | 5 (1.25) | 3/4 | 2 |
| C-5 C0 끔 (수정 전) | 4 | 7 (1.75) | 2/4 | 4 |
| **수정 후** | 9 | 11 (1.22) | 4/9 | 8 |

  - writer는 규칙 7이 있어도 3min 캡션의 "The video closes with a close-up of the Shot Coach device"(18:00–21:00 구간 요약) 같은 문장을 그대로 옮겼다(`-QuCz7kxBr8` r1 섹션 3·4에서 각 1번, r3 섹션 4에서 3번, 인용 근거 끝 20:00–21:00). 결론 섹션의 결말 오인 비율은 표본상 줄었지만(수정 전 7/11, 후 4/9) 표본이 작아 효과로 단정할 수 없다.
  - 결론 마지막 문장을 실제 결말(10sec 캡션)과 대조: `-QuCz7kxBr8` r1은 "The video ends at 00:37:37 with a static screen displaying 'Thank you for watching' …"로 정확했다. `54k2g9ddy4M` r2("pet psychics and goats on the road")는 41:30 개·44:20 염소 장면과 맞는다. `54k2g9ddy4M` r1·r3("concludes … Liendo's gold medal")은 틀렸고 검사가 `ending_early`(인용 근거 끝 40:00 < 45:14)로 표시했다.
  - 검사 오탐 1건: "the final shot of the video’s opening montage"(`0RxMZBLeqRI` r1 섹션 1)가 결말 서술로 잡혔다("of the video’s …" 소유격 표현).
- 규칙 검사 합계(9건, 문장 1,104): unsupported 9, miscited 21, uncited 69.
- I28: 이번 실행에서 `Already borrowed` 0건. 다만 보고서 생성은 서버당 요청이 한 번에 하나라 수정 전(C-4·C-5)에도 0건이었으므로 이 실행으로 효과를 판단할 수는 없다(코드와 CPU 테스트로만 확인).
- 판단: (a)는 루프 시간을 줄였고 (c)는 루프 문장을 보고서에서 없앴으며 (d)는 그 사실을 표시한다. 다만 상한에서 끊긴 섹션은 문장 중간에서 끝나고 그 섹션의 나머지 내용은 생성되지 않는다. P19는 검사(3)가 결말 오인을 잡아 표시하지만, writer 규칙(1)만으로는 오인을 막지 못했다.

### 9.17 흐름 오류·추측 표현 현황 측정 (2026-10-26, GPU 없음, `analysis/flow_speculation_check.py`, 결과 `results/flow_speculation_20261026.json`)

- 대상: 보고서 20건(C-4 3, C-5 C0 켬 4, C-5 끔 4, §9.16 수정 후 9). 수정 전 보고서의 반복 루프가 결과를 부풀리지 않도록 모든 보고서에 같은 문장 제거(§8.12)를 먼저 적용했다. 검출은 후보이고, 정밀도는 아래처럼 직접 확인했다. 화자 뒤바뀜은 의미 비교가 필요해 측정하지 않았다.
- 검출 정의: F1 섹션 순서(결론 제외 섹션마다 인용 episodic 근거 구간 중앙값, 다음 섹션이 60초 넘게 앞서면 역전), F2 섹션 안 시각 역행(본문 HH:MM:SS가 60초 넘게 뒤로), F3 결론 수량 불일치("숫자 + 사람·팀 명사"가 앞 섹션과 다름), S 단서 표현 3종(추정: possibly·likely·may 등 / 해석: suggesting·symbolizing·implies·reflecting·representing 등 / 평가: underscoring·reinforcing·highlighting·profound 등)과 그 단서 어간이 문장의 인용 근거에 있는지(옮김) 없는지(추가) 인용이 없는지.

| 묶음 | 보고서 | 문장 | F1 | F2 | F3 | S 추정/해석/평가 | 옮김/추가/인용 없음 |
|---|---|---|---|---|---|---|---|
| C-4 | 3 | 339 | 1 | 1 | 1 | 10/56/79 | 99/15/31 |
| C-5 C0 켬 | 4 | 539 | 1 | 8 | 0 | 14/35/131 | 131/28/21 |
| C-5 C0 끔 | 4 | 466 | 0 | 1 | 0 | 7/34/101 | 105/15/22 |
| 수정 후(§9.16) | 9 | 1,104 | 1 | 5 | 0 | 24/151/259 | 270/94/70 |

- 직접 확인
  - F1 3건 모두 실제 시간 순서 역전: C-4 `-QuCz7kxBr8` 섹션 4(25:00) → 5 "Final Game Dynamics"(18:45), C-5 `-QuCz7kxBr8` 켬 r2 섹션 4(25:25) → 5 "Final Competitive Games and Drills"(19:30), 수정 후 `54k2g9ddy4M` r2 섹션 3 Liendo(31:45) → 4 Montfort 병원(22:30). 앞의 둘은 "Final" 제목의 섹션이 18–19분 내용을 다뤄 결말 오인(P19)과도 겹친다.
  - F2 15건: 14건은 본문 섹션에서 "At HH:MM:SS" 서술이 앞 문장보다 1.3–11.7분 뒤로 가는 경우(예: C-5 `54k2g9ddy4M` 켬 r2 섹션 4에서 33:00 → 26:00, 31:30 → 26:30, 30:30 → 25:50, 34:20 → 29:00 4건), 1건은 결론 섹션의 회상(오류 아님).
  - F3는 쓸모없다: 알려진 오류(C-4 결론 "three men" vs 섹션 1 "six men")를 놓쳤다(앞 섹션에 장면 단위 "three men"도 있어서). 표시된 1건("three participants" vs "two participants")은 장면별 인원이라 모순이 아니다.
  - S: 수정 후 9건에서 "추가"로 분류된 문장 12개를 무작위로 골라 근거 원문과 대조(이때는 단어 그대로 비교한 판). 8개는 근거에 없는 해석·평가(예: "visually reinforcing forced displacement", "representing joy, freedom, or resistance", "This juxtaposition highlights how national priorities … intersect"), 3개는 근거에 같은 뜻이 있음(2개는 underscores/underscoring처럼 단어 형태 차이), 1개 경계. 이후 어간 비교로 고쳐 위 표의 값이 됐다(수정 후 묶음 "추가" 140 → 94).
- **원인 확인: 해석 표현의 출처는 근거 캡션이다.**
  - 수정 후 묶음에서 단서 434개 중 270개(62%)는 같은 어간이 인용 근거에 있었다. 그 근거의 단위는 30sec 131, 10min 109, 3min 100, 10sec 13, semantic 2.
  - 이 묶음에서 검색된 고유 근거 중 해석·평가 단서가 들어 있는 비율: 3min 28/29, 10min 12/12, 30sec 81/98, 10sec 13/82, semantic 1/128.
  - WorldMM 전처리 요약 프롬프트(`gen_multiscale.py` `_PROMPTS["general"]`)에는 "Do not make assumptions or add interpretations"가 있지만, Qwen3-VL-8B가 만든 30sec·3min·10min 요약에 해석 표현이 거의 다 들어 있다. writer는 그것을 옮기고(옮김), 일부는 스스로 더한다(추가 94, 인용 없음 70).
  - "옮김"은 단서 어간이 근거에 있다는 뜻일 뿐, 그 문장의 해석이 근거와 같은 대상을 가리킨다는 보장은 아니다.
- 결론: 흐름 오류는 섹션 순서 역전 3/20건, 섹션 안 시각 역행 14건(본문)으로 꾸준히 있다. 추측·해석 표현은 보고서당 수십 개이고 다수가 다단위 요약 캡션에서 온다. 대응(검출 경고, 요약 캡션 정제, writer 규칙 등)은 사용자 결정 대상이다.
---

## 10. 환경 변경 이력

| 일시 | 변경 | 결과 |
|---|---|---|
| 2026-10-21 | `WorldMM/.venv`에 `flask==3.1.3` 설치 (+werkzeug 3.1.9, itsdangerous 2.2.0, blinker 1.9.0) | 기존 패키지 변화 없음. 실제 실행 환경이 `/opt/venv`라 불필요했으나 사용자 지시로 유지 |
| 2026-10-21 15:47 | (a) `WorldMM/.venv` 텍스트 파일 76개의 `/data1/USER/workspace/VAU_RAG` → `/data1/USER/workspace/VideoRAG` 치환 (bin 72개: activate·shebang, site-packages 4개: `worldmm.pth`, `__editable__.hipporag-2.0.0a4.pth`, `direct_url.json` 2개) | 남은 항목 0, 권한 그대로 (755×67, 644×9), 백업 보관 |
| 2026-10-21 15:47 | (b) `UV_PROJECT_ENVIRONMENT=$PWD/.venv uv sync --frozen --inexact` | (a) 이후라 decord 0.6.0만 같은 버전으로 재설치 |
| 2026-10-21 16:26–16:31 | (의도하지 않은 변경, 2026-10-25 확인) GPU 스모크(§9.2)와 LLM 서버가 모델 4개를 환경변수 `HUGGINGFACE_HUB_CACHE` 위치(`VideoRAG/.cache/huggingface/hub`)에 내려받음. 우리 스크립트의 `HF_HOME` 설정은 이 위치를 바꾸지 못한다(§3, `REPORT_ISSUES_AND_FIXES.md` I4) | 약 30GB(snapshot 기준 17.5G + 8.1G + 4.4G + 53M) 추가. `/data1/USER/workspace/.cache/huggingface/hub`와 같은 내용 |
| 검증 | — | `uv.lock`·`pyproject.toml` 해시 동일. `/opt/venv` 패키지 목록 변화 없음. `.venv` 패키지 목록은 worldmm·hipporag 경로만 바뀜. flask 유지. `import worldmm, hipporag, decord, WorldMemory, HippoRAG` 성공. `activate` → `VIRTUAL_ENV=/data1/.../WorldMM/.venv` |

- **남은 사항**: `.venv` 안의 `.pyc` 4,734개에는 컴파일 당시 경로(`VAU_RAG`)가 남아 있다. Python은 `.pyc`를 소스의 수정 시각과 크기로 검증하므로 동작에는 영향이 없고, 예외 traceback에 옛 경로가 보일 수 있을 뿐이다. 문자열 길이가 달라 텍스트 치환으로 고치면 파일이 손상되므로 제외했다.
- **⚠️ 주의**: 이 컨테이너에서 그냥 `uv sync`를 실행하면 대상이 `/opt/venv`가 되고, 기본(exact) 모드라 langgraph·langchain·flask·merit 등 20여 개를 삭제하고 openai를 2.54에서 2.29로 내린다(✔ dry-run). **반드시 `UV_PROJECT_ENVIRONMENT`로 대상을 지정하고 `--frozen --inexact`를 붙인다.**
- 기존 repo(WorldMM, MERIT, Deep-Report)의 코드는 수정하지 않았다.

---

## 11. 미검증 사항과 위험

| 항목 | 상태 | 대응 |
|---|---|---|
| 4개 granularity 실제 캐시로 검색·보고서 생성 | ✔ 검증 영상 3개: 검색 C-3(§9.12), 보고서 C-4 3건·C-5 8건·P9/P19 확인 9건(§9.13, §9.14, §9.16) (2026-11-10 표 갱신) | 나머지 47개 영상은 사전 인덱싱(C-7) 후 |
| 사전 인덱싱 영상 1개 전체 시간과 메모리 | 일부 ✔ (10sec 재계산 18개 약 2.6분, GPU 스냅샷 §9.5) / ✖ 전체 (◇ 기존 기록: 재인덱싱 영상당 30–50분) | 다시 허용되면 영상 1개를 끝까지 측정 |
| HTTP OpenIE와 in-process OpenIE 결과 비교 | ✖ (같은 메시지·인자·파서임은 코드로 ✔. 샘플링이라 완전 일치는 기대할 수 없음) | 필요하면 소수 청크로 빈 triple 비율 비교 |
| OpenIE 재시도 소진 시 빈 triple이 캐시에 저장되고 "완료"로 판정됨 | ✔ 2건 확인 (§9.5) | 완료 판정은 캐시 키만 본다. 완료 표식에 빈 triple·entity 수 기록(§8.3). 응답 구제로 소진이 줄 것으로 기대(✖ 미측정) |
| 분할 OpenIE·응답 구제·폭주 절단의 실제 효과 | ✔ 영상 3개(§9.10): 호출 430회 = 계획, 분할 조각 실패 0, 파싱 실패 5건 모두 1회에 구제, 절단 146개 | 50개 영상 실행 후 분포로 재검토(C-8) |
| 분할 기준(1,100토큰) 아래 입력의 출력 잘림 | ✔ C-1에서 3건(영상 1의 분할하지 않은 10min 청크 2건, 영상 3의 분할 조각 1건). 끝부분이 같은 주어의 나열 형태 | 구제로 처리되지만 잘린 뒤의 triple은 없다. 10/22의 "입력 1,025토큰 이하 잘림 0건"은 10sec·30sec·3min 333회 기준이었다. 기준 조정 여부는 50개 실행 분포로 판단 |
| 폭주 절단이 정당한 나열도 자른다 | ✔ C-2(§9.11): 절단에 걸린 예에 `basketball court – features – hoop, trampoline, …` 같은 장면 요소 나열과 `Joshua Liendo – is – …` 같은 반복 서술이 섞여 있다 | 경험적 기준(15)의 한계. C-8에서 검토 |
| OpenIE 결과의 실행 간 편차 | ✔ C-2: 같은 입력(분할 대상 아님)을 다시 계산하면 청크별 triple 집합 Jaccard 평균 0.27(30sec)·0.22(3min), 같은 청크 0개 | 샘플링 생성(T=0.7) 때문. 캐시를 다시 만들면 그래프 내용이 달라진다. 비교·평가 때 감안 |
| LLM 서버 토크나이저 동시 사용 오류 `Already borrowed` | ✔ C-1 261건(10/22 실행에도 229건 + 76건). WorldMM 생성 함수의 재시도로 모두 성공(500 응답 0) | 원인은 `local_llm_server.py`가 생성 잠금 밖에서 `count_tokens`로 같은 토크나이저를 쓰는 것(코드 근거). 2026-10-25 수정: 토큰 계산을 생성 잠금 안으로(커밋 `b7a021d`, §8.12). 보고서 생성은 요청이 하나씩이라 효과는 사전 인덱싱에서만 확인할 수 있다(§9.16) (2026-11-10 표 갱신) |
| writer 반복 루프(P9) | ✔ C-5 2/8건, 수정 후 2/9건(§9.16) | 서버 상한 3,072로 130–134초에 끊기고 같은 문장 제거·경고(§8.12). 남은 위험: 끊긴 섹션이 문장 중간에서 끝나고 나머지 내용이 없음, 비슷하지만 완전히 같지 않은 반복은 지워지지 않음, "loop suspected" 경고가 3–4회 일반 반복에도 붙던 문제는 2026-10-26 기준 변경(§8.13) |
| 구간 요약의 "the video closes"가 영상 결말로 옮겨짐(P19) | ✔ C-4, 수정 후에도 9건 중 결론 4건(§9.16) | writer 규칙 7 + 결말·시작 서술 검사(§8.12). 검사는 경고만 하고 문장을 고치지 않는다. 2026-10-26: 영상 끝 근거(txt0)를 writer에 제공, 오탐(소유격) 수정(§8.13). **GPU 미확인** |
| 같은 영상 동시 불러오기(I29) | ✔ C-5 첫 시도 1건 실패 | `experiments/gpu_report_batch.py` 영상별 잠금. 서비스 코드 자체는 그대로라 다른 실행 방식에서는 다시 생길 수 있다 |
| 같은 작업 폴더의 Claude 세션 중복(I30) | ✔ 2026-10-25 13:39–13:49 두 세션이 겹쳐 실행, 이전 세션이 문서 5종을 고치고 커밋(`dd0039b`) | 동시에 같은 파일을 고치면 서로 덮어쓸 수 있다. 세션 하나만 쓰기 |
| 세션이 바뀌면 백그라운드 작업 추적이 끊김 | ✔ 2026-10-25: 새 세션 시작 시 이전 세션의 백그라운드 작업 2개가 "stopped"로 표시됐지만, `setsid`로 띄운 C-5 배치는 끝까지 돌아 8건을 완료했다 | 실행은 `setsid`로 띄우고, 상태는 결과 파일(`summary.json`, 로그)과 `ps`로 확인한다 |
| 분할 경계에서 문맥 손실, 기준 1,100토큰의 실측 범위 밖 구간(1,026–1,100) | ✖ | 분할 전후 triple 비교 시 함께 확인 |
| 폭주 절단 기준(연속 15)과 NER 구제 상한(100) | 경험적 기준, 표본 작음 | 50개 영상 실행 후 `guard_cumulative`와 캐시 분포로 재검토 |
| 10min 캡션 잘림(32/232개, 영상 20개) | ✔ 확인, 보류(결정 11) | 잘린 뒷부분 내용은 인덱스·근거에 없음. 필요 시 10min만 재생성 |
| **검증 영상 3개 중 잘린 캡션** (✔ 2026-10-25, `prebuild_episodic_index.count_tokens`로 4개 단위 전부 측정) | `0RxMZBLeqRI` 10min 4개 중 2개가 2,048토큰이고 문장 중간에서 끝남: 0–10분 "… This", 10–20분 "… the ominous,"(I22의 예시가 이 두 개다). 나머지 단위(10sec 최대 229, 30sec 680, 3min 1,025토큰)와 `-QuCz7kxBr8`(10min 최대 1,733), `54k2g9ddy4M`(10min 최대 1,491)은 2,048토큰 캡션 없음 | `0RxMZBLeqRI` 보고서는 planner 개요와 10min 근거의 0–20분 구간 뒷부분이 빠진 상태로 만들어진다. 영상 3개 검증 결과를 해석할 때 이 차이를 분리해서 본다 |
| 모델 캐시 위치(§3 정정) | ✔ 컨테이너에서는 `HUGGINGFACE_HUB_CACHE`가 우선해 `paths.hf_home` 설정이 효과 없음 | 이 서버에서는 두 위치에 같은 모델이 있어 동작에 문제없음. 다른 환경(새 서버, 컨테이너 밖)에서는 모델이 `HF_HUB_CACHE` → `HUGGINGFACE_HUB_CACHE` → `$HF_HOME/hub` → `~/.cache/huggingface/hub` 순서(`huggingface_hub/constants.py:129-155`)로 정해지는 위치에 있어야 한다. 없으면 첫 로드 때 내려받는다(인터넷 필요) |
| 디코딩 실험 rp110gen의 이상 결과 2건 | 원인 ✖ (원문 미저장) | 반복 억제를 다시 검토할 때 원문 저장 후 재현 |
| GPU 공유: 다른 사용자 메모리 변동 | ✔ §9.8에서 중단, §9.9에서 6시간 동안 시작 불가 | 감시·자동 중단 유지. 2026-10-25 GPU 4–7 사용 허용(11:44 확인 시 비어 있음). 실행 직전 여유 확인은 계속 한다 |
| `local_llm_server`의 `finish_reason`(텍스트 재토큰화 기준) | ✔ 부정확 사례 확인 | 구제 조건에 쓰지 않음. 서버 수정은 미승인 |
| 결정 4(규칙 6 + C0)의 실제 효과와 지연 | C-5 8건(C0 켬 4·끔 4, §9.14) 측정: 표본이 작아 효과 판단 불가 (2026-11-10 표 갱신) | `previous_sections_context` written vs deep_reporter 다중 실행 비교 (`ANALYSIS_D4_D7.md` §1.6) |
| 번역 보완(한자 재시도, 이름 보호)의 실제 효과, 늘어난 자리표시가 번역 실패율에 주는 영향 | ✔ C-4 실측: 17섹션 중 12 성공·5 실패(자리표시자 불일치, 영어 유지), 한자·가나 잔존 3섹션(§9.13, P15) (2026-11-10 표 갱신) | 결정 16에 따라 번역은 보류(영어 보고서 품질 우선) |
| 인용이 붙은 문장의 내용 오류 | ✔ 실보고서에서 확인 | 규칙 검사로 수치·문구·시간 유형만 경고. 의미 수준 오류는 미검출 |
| 결론 섹션의 인용 불일치, planner 설명 유입 | ✔ 실보고서에서 확인 | C0로 완화 기대(✖ 미측정) |
| 근거 없는 추측 표현 | ✔ 보고서 B 5문장 | 대응 없음 |
| 규칙 검사의 재현율, 다른 영상으로의 일반화 | ✖ (보고서 2건, A 정밀도 약 78%) | 평가 단계에서 표본 확대 |
| 같은 조건 다중 실행의 편차 | ✔ 영상 3개 × 3회(P9/P19 확인 9건) 분석(2026-10-26, `internal/analysis/SELF_CONSISTENCY_ANALYSIS.md`·`SELF_CONSISTENCY_CAUSES.md`): 실행 쌍의 episodic 근거 Jaccard 0.19–0.41 (2026-11-10 표 갱신) | 원인 분리 실험 E1–E4 (GPU 필요) |
| L1 응답 파싱 실패 시 RRF로 채워져도 `meta.episodic_filter="llm"` 표시 | ✔ 코드 확인 | 필요하면 서비스에서 선택 결과를 직접 파싱해 구분 |
| L1과 L0·full의 품질 차이 | ✖ (지연·단위 구성만 측정, §9.12) | 4개 단위 캐시로 비교 |
| 검색 요청 지연 vs Deep-Reporter 타임아웃 600초 | ✔ 10sec만: L1 text 5.5초, full 9.5초 / ✔ 4개 단위(§9.12): L0 0.7–1.4초, L1 4.4–7.9초, full 29.7–38.8초 | 여유 충분 |
| 근거가 긴 프롬프트(10min 요약 포함)의 컨텍스트 길이와 GPU 메모리 | ✖ | 근거 수와 granularity 상한 조정 |
| 한 GPU에 여러 모델(검색 서비스의 Qwen3-Embedding·VLM2Vec과 LLM 서버) | ✖ | 프로세스·GPU 배정 계획 필요 (◇ eval 프로세스 약 44GB) |
| 영상 여러 개 연속 처리 시 검색 서비스의 영상 교체(메모리 해제) | ✔ §9.12: 전환 2.0–2.4초, 메모리 누적 없음 | 다중 영상 실행에서 확인(현재 `experiments/gpu_3videos.py`는 검색 서비스 1개로 영상을 차례로 교체한다) |
| `llm.backend=openai` 경로 (`gpt-5-mini`의 `max_completion_tokens` 등) | ✖ | 외부 경로를 처음 쓸 때 실호출로 확인 |
| vLLM 교체 | ✖ (미설치) | — |
| Deep-Reporter `recursion_limit=50` | ✔ 실측: 15섹션 성공, 16섹션부터 보고서 전체 소실 | `max_sections`를 3–15로 제한 |
| Deep-Reporter `ReasoningOpenAI`의 모델명 판정(`'r1' in name`이면 DeepSeek-R1 경로) | ✔ `qwen3vl-8b`, `gpt-5-mini`는 해당 없음 | 모델명을 바꿀 때 주의 |

---

## 12. 주요 코드 위치

**기존 repo (읽기 전용)**

| 내용 | 위치 |
|---|---|
| WorldMM 추론 루프 / QA 렌더링 | `WorldMM/src/worldmm/memory/memory.py:408`, `:248-272`, `:522` |
| Episodic 검색 / LLM 필터 / HippoRAG 생성 | `WorldMM/src/worldmm/memory/episodic/memory.py:247`, `:398`, `:120` |
| OpenIE (NER·triple, 오류 시 빈 결과) | `WorldMM/src/worldmm/memory/episodic/openie.py` |
| Qwen3VL 생성·구조화 파싱 | `WorldMM/src/worldmm/llm/qwen3vl.py` (`generate`, `_parse_structured_response`) |
| HippoRAG 검색 / rerank / OpenIE 경로 / 라벨 | `WorldMM/src/HippoRAG/src/hipporag/HippoRAG.py:327`, `:1179-1216`, `:119`, `:83-85` |
| DSPy 필터 LLM 호출 | `WorldMM/src/HippoRAG/src/hipporag/rerank.py:95` |
| Visual 검색 / 프레임 추출 | `WorldMM/src/worldmm/memory/visual/memory.py:293`, `:344-409`, `:554` |
| Semantic evidence 버림 | `WorldMM/preprocess/semantic_memory/consolidate_semantic_memory.py` (`transformed_current_evidence`) |
| Video-MME eval 설정 | `WorldMM/eval/eval.py` (`VIDEOMME_GRANULARITIES`, `QUERY_TIME`) |
| Deep-Reporter 그래프 / recursion_limit | `Deep-Report/deep_reporter/core/graph.py`, `api.py:105` |
| Deep-Reporter search / writer / context | `Deep-Report/deep_reporter/nodes/search_node.py:56,74,89,97`, `section_writing_node.py:59,214` |
| combine | `Deep-Report/deep_reporter/nodes/combine_node.py` |
| LLM 호출 / 실패 문자열 | `Deep-Report/deep_reporter/utils/llm_utils.py:36,82` |
| LLM 라우팅 / 설정 | `Deep-Report/deep_reporter/llms/factory.py`, `llms/reasoning_openai.py`, `config/base_config.py` |
| 템플릿을 읽는 노드 / 출력 파싱 | `Deep-Report/deep_reporter/nodes/planner_node.py:98`, `query_generation_node.py:67`, `section_writing_node.py:141-142`(인용 정규식) |
| 원래 retriever topk 절단 | `Deep-Report/retriever/retriever_app.py:717` |
| MERIT 프레임 / 프레임 수 | `MERIT/src/merit/merit_memory.py:154`, `:182` |

**`report_framework/` (함수 이름 기준)**

| 내용 | 위치 |
|---|---|
| 캐시 계획·완전성 판정 / 시드 / 라벨 클래스 / HTTP OpenIE | `prebuild_episodic_index.py`: `plan_video`, `build_seed_docs`, `make_labeled_episodic_memory_class`, `make_http_llm_model`, `check_endpoints` |
| 긴 청크 분할 / 응답 구제 / 폭주 절단 / 캐시 병합 | `prebuild_episodic_index.py`: `count_tokens`, `split_passage`, `openie_split_docs`, `json_list_items`, `salvage_structured`, `cut_long_runs`, `write_cache_docs`, 상수 `SPLIT_MIN_TOKENS`, `SPLIT_PIECE_TOKENS`, `MAX_SAME_SUBJ_PRED_RUN`, `MAX_SALVAGED_ENTITIES` |
| 10min 캡션 생성(잘림 원인) | `WorldMM/src/worldmm/memory/episodic/gen_multiscale.py` (`_summarize_batch`), `WorldMM/claude_output/full/process_one_video.sh:26` (2026-11-10에 옮긴 사본: `report_framework/scripts/memory_build/process_one_video.sh`의 3) multiscale 단계) |
| 검색 로드 검사 / DSPy 없는 그래프 검색 / episodic 병합·L1 | `videorag_retriever_service.py`: `check_inputs`, `_graph_search`, `search_episodic` |
| 템플릿 / 계약 / 교체 / C0 | `domain_templates.py`: `VIDEOMME_*`, `build_templates`, `resolve_targets`, `validate_templates`, `apply_templates`, `written_context_summary`, `apply_written_context` |
| 인용 치환 / 규칙 검사 / absence / 이미지 시간 | `grounding_postprocessor.py`: `ground_report`, `check_section_grounding`, `absence_clause`, `image_time_alignment` |
| 사전 확인 / 검증 / 실행 | `run_report.py`: `preflight`, `validate`, `run` |
| 번역 / 고유명사 / 보호 | `report_translator.py`: `translate_report`, `collect_proper_nouns`, `mask`, `translate_section` |
| GPU 실행 / 감시 / 대기 후 시작 | `experiments/gpu_3videos.py`: `main`, `Watch`, `stop_all`, 상수 `LLM_CAP`; `experiments/delayed_gpu_3videos.py`: `main`(인자 `--gpus`) |

---

## 13. 인수인계

### 13.1 반드시 지킬 규칙

- **GPU 사용 범위(2026-10-25 최신 지시)**: 이 서버에서 **GPU 4–7 네 개를 사용할 수 있다.** 이전 지시 이력: GPU 4–7(20,000 MiB 규칙) → 규칙 해제 → 여유 메모리 안에서 → GPU 6·7만(2026-10-22, §9.8·§9.9). 새 서버로 옮기면 호스트 GPU 3·4(다른 사용자와 공유, 컨테이너 안 번호 0·1)를 쓸 계획이다(`MIGRATION_HANDOFF.md`).
- **어느 GPU든 다른 사용자의 동작 중인 프로세스를 절대 침범하지 않는다.** 이미 돌고 있는 작업은 중단하지 않고, 자기가 띄운 PID만 종료한다. 실행 직전에 여유 메모리를 확인하고, 실행 중에는 메모리 감시·자동 중단(`experiments/gpu_3videos.py`의 `Watch`, 기준 47,500 MiB)을 쓴다. 프로세스별 메모리 상한(`scripts/launch/run_*_capped.py`, `GPU_MEM_CAP_MIB`, `--gpu-mem-cap-mib`, `--llm-cap-mib`)은 기본으로 걸되, **2026-10-25 C 단계는 사용자 지시로 상한 없이 실행했다(결정 14)**. 다음 실행에서 상한을 쓸지는 사용자 지시를 따른다.
- **같은 영상을 검색 서비스 2개 이상이 동시에 불러오지 않는다**(I29). 여러 서비스를 띄울 때는 `experiments/gpu_report_batch.py`처럼 영상별 잠금으로 불러온다.
- **같은 작업 폴더에서 Claude 세션을 하나만 쓴다**(I30). 실행은 `setsid`로 띄워 세션이 바뀌어도 끝까지 돌고, 결과는 파일로 확인한다.
- 사용자가 GPU 작업 중지를 지시하면 즉시 자기 프로세스만 종료한다. CPU 테스트는 `CUDA_VISIBLE_DEVICES=""`로 실행한다.
- **repo 규칙**: WorldMM, MERIT, Deep-Report 코드는 수정하지 않는다. 신규 파일은 `report_framework/`에만 둔다. Deep-Reporter 동작 변경은 §7.4의 범위 한정 교체로만 한다. `report_framework/`의 기존 파일도 수정 전에 대상·위치·내용을 보고하고 승인을 받으며, 수정 전 사본을 `backups/`에 둔다.
- **episodic 캐시를 다시 만들 때**는 해당 granularity 폴더 전체를 지운다(OpenIE 파일만 지우면 옛 그래프가 남음, §5.2). 캐시 삭제는 사용자 승인 후에만 한다.
- **`-`로 시작하는 영상 id**(예: `-QuCz7kxBr8`)는 항상 `--video-id=<id>`, `--preload=<id>`, `--videos=<id>` 형식으로 넘긴다.
- **실행 환경은 `/opt/venv`**다. **대상 지정 없이 `uv sync`를 실행하지 않는다**(§10).
- **모델 캐시**: 이 컨테이너에서 실제로 쓰이는 위치는 환경변수 `HUGGINGFACE_HUB_CACHE`(`/data1/USER/workspace/VideoRAG/.cache/huggingface/hub`)다. `config.yaml`의 `paths.hf_home`으로 `HF_HOME`을 바꿔도 이 위치는 바뀌지 않는다(§3 정정). 두 위치 모두에 같은 모델 4개가 있다.
- 전수 검색에는 `/usr/bin/grep`을 쓴다. Deep-Reporter는 `deep_reporter.api`를 먼저 import한다.

### 13.2 실행 방법

```bash
cd /data1/USER/workspace/VideoRAG/report_framework
# --- GPU 불필요 ---
python -B prebuild_episodic_index.py --config config.yaml --dry-run
python -B domain_templates.py --check --overview-file <caption_dir>/<vid>/10min.json
CUDA_VISIBLE_DEVICES="" python -B tests/unit/test_retriever.py        # 검색 서비스
CUDA_VISIBLE_DEVICES="" python -B tests/unit/test_templates.py        # 템플릿·규칙 6·C0 + Deep-Reporter 통합
CUDA_VISIBLE_DEVICES="" python -B tests/unit/test_report_pipeline.py  # 후처리·근거 검사·run_report·번역
CUDA_VISIBLE_DEVICES="" python -B tests/unit/test_prebuild_http.py    # HTTP OpenIE 클라이언트
CUDA_VISIBLE_DEVICES="" python -B tests/unit/test_openie_split_guard.py  # 긴 청크 분할·응답 구제·폭주 절단
python -B analysis/analyze_report.py --outline <out>/report.json --out <metrics.json>
# --- GPU 필요 (허용될 때만) ---
python -B experiments/gpu_3videos.py --llm-gpu <A> --aux-gpu <B> [--videos=a,b,c] [--skip-prebuild]  # 사전 인덱싱 → 보고서 (감시 포함, LLM 서버 1개). 인자 생략 시 기본 7·6
python -B experiments/delayed_gpu_3videos.py --out <dir> --gpus <A>,<B> [--delay-sec 7200]  # 대기 후 여유 확인 → gpu_3videos (§8.11)
./run_prebuild_http.sh <LLM_GPUS> <INDEXER_GPU> --videos=<vid>                        # 사전 인덱싱만 (A안, 감시 없음)
python local_llm_server.py --config config.yaml --gpu <A>                            # LLM 서버 (:8010)
python videorag_retriever_service.py --config config.yaml --gpu <B> --preload=<vid>  # 검색 서비스 (:8020)
python run_report.py --config config.yaml --video-id=<vid> --query "<요청>"           # 보고서 생성
python -B tests/gpu/gpu_e2e.py                                                            # 10sec 테스트 캐시로 전체 흐름 + full
```

- 실제 GPU 실행에서는 위 서버들 대신 상한 래퍼(`scripts/launch/run_llm_server_capped.py <port>`, `scripts/launch/run_service_capped.py <config> --preload=<vid>`)를 쓴다.
- 사전 인덱싱 캐시가 없거나 불완전한 영상은 검색 서비스가 409로 거부한다 → `run_report.py`가 exit 2.
- **완성된 실제 캐시**는 `tests/_artifacts/gpu_test/`의 영상 1개(`-QuCz7kxBr8`), 10sec 단위만 있다(테스트 전용). 이것으로 실행하려면 config 사본에서 `paths.episodic_cache_root`를 그 경로로, `worldmm.granularities`를 `[10sec]`으로, `retrieval.episodic_candidates_per_query`를 `{10sec: 6}`으로 바꿔 검색 서비스와 `run_report.py`에 함께 넘긴다. `tests/gpu/gpu_e2e.py`가 이 설정을 자동으로 만든다.
- (2026-11-12 이 원본은 삭제됨) `report_framework/cache/episodic/`에는 검증 영상 3개의 4개 단위 캐시와 완료 표식 3개가 있었다(2026-10-25 C-1, dry-run 남은 호출 0회 ✔). 2026-11-10부터 설정은 그 사본 `WorldMM/output/memory/videomme_long_qwen3vl-8b/report_framework_index/`를 쓴다(md5 동일, dry-run 출력 동일 ✔). C-1 직전 캐시 사본은 `backups/cache_before_c1_20261025/`다. 나머지 47개 영상은 캐시가 없어 검색 서비스가 409로 거부한다.

### 13.3 다음 작업

**(1) GPU 불필요**
- 사용자 결정 대기: 근거 없는 추측 표현(P12) 감지, 번역본 제목 형식 통일, `local_llm_server` `finish_reason` 수정(I25), 10min 캡션 재생성용 래퍼(I22, 보류. 검증 영상 `0RxMZBLeqRI`도 해당, §11).
- (완료 2026-10-25, 사용자 승인) 루트 `VideoRAG/CLAUDE.md`를 현재 프로젝트·규칙으로 갱신(이전 판 `backups/ROOT_CLAUDE.md.bak_20261025`). `report_framework/`를 git 저장소로 만듦(§8.1). `experiments/delayed_gpu_3videos.py`에 `--gpus` 인자 추가.
- (완료 2026-10-22) 다른 문서 3종에 분할 OpenIE·GPU 공유 내용 반영. (완료 2026-10-25) 대기 실행 기록, HF 캐시 정정, 날짜 표기 정정 반영.
- 서버 이전(`MIGRATION_HANDOFF.md`): 파일 복사·검증까지 완료. 이 서버에서 계속 작업하는 동안 바뀐 파일은 이전할 때 다시 동기화해야 한다.

**(2) GPU 작업 (2026-10-25 GPU 4–7 허용)**
1. **(C-1–C-5 완료 2026-10-25, §9.10–§9.14)** **영상 3개 사전 인덱싱 + 보고서**: `experiments/gpu_3videos.py`. 먼저 영상 1·2로 분할·구제 효과를 확인한다(잘림·구제·절단·빈 결과 수는 완료 표식과 로그, 시간). 분할 전후 triple 비교(`backups/cache_before_split_20261022/`). 백업은 영상 1의 10min(4청크)과 영상 2의 10sec(184)·30sec(62)·3min(11) OpenIE 결과다. **분할이 적용되는 단위는 1,100토큰을 넘는 청크가 있는 10min뿐**이라 분할 전후 비교가 가능한 것은 영상 1의 10min이다. 영상 2의 10min은 분할 전 실행이 끝나지 않아 비교 기준이 없고, 영상 2의 10sec·30sec·3min 백업은 재계산 결과와의 차이(샘플링 편차) 확인에 쓸 수 있다. 이상이 없으면 영상 3과 보고서 3건으로 넘어간다. `0RxMZBLeqRI`는 10min 캡션 2개가 잘린 상태임을 감안한다(§11).
2. **(완료 C-3, §9.12)** **완성 캐시로 검색 확인**: 서비스 `/load`(409 없음), L0/L1/full 지연과 Deep-Reporter 600초 타임아웃 여유.
3. **(완료 C-4, §9.13)** **현재 코드로 보고서 생성·분석**: 규칙 6·C0, absence, 이미지 시간 기록, 번역 보완이 반영된 첫 실제 실행. 영상 3개 보고서를 `analysis/analyze_report.py`와 근거 원문 대조로 검증한다.
4. **(C-7, 사용자 지시 전 미실행)** **50개 영상 사전 인덱싱**: 13,424회(분할 포함, 빈 캐시 기준). 소요 시간 추정은 §5.2.2(서버 7개·GPU 4개 단독이면 약 13시간, 서버 1개·GPU 공유면 4–5일).
5. **(완료 C-5, §9.14: 효과 확인 안 됨, writer 루프 발견)** **결정 4 효과 측정**: 같은 영상·query로 `previous_sections_context` written vs deep_reporter를 각 2회 이상 실행(`analysis/analyze_report.py`).
6. **결정 7 실험**(`ANALYSIS_D4_D7.md` §3) 후 사용자에게 다시 질문한다(C-6, 질문 전).

**(2-1) 2026-10-25 결정 16 이후 상태**
1. (완료 §8.12·§9.16) P9 (a)(c)(d), P19 (1)(3), I28.
2. (유지) C0 켬. 나중에 표본을 늘려 재측정.
3. (보류) 번역(P15) — 영어 보고서 품질 우선.
4. (다음, 코드 수정 승인·GPU 필요) 결정 7 후보 C(semantic 경량 필터)·D(이미지를 텍스트 근거 시간 근처로 제한) 구현 → A/C/D 비교 실험 → 사용자에게 질문. 구현 계획은 이번 보고에 정리.
5. (완료 2026-10-26, §8.13, GPU 미확인) "loop suspected" 기준 변경(최대 반복 ≥ 5 또는 문장 중간 끝), P19 영상 끝 근거(txt0), 검사 오탐 수정. (사용자 결정 필요) 상한에 끊긴 섹션 처리(그대로 둘지·그 섹션만 다시 생성할지).
5-1. (측정 완료 2026-10-26, §9.17) 흐름 오류·추측 표현 현황. 대응 방향(검출 경고, 다단위 요약 캡션의 해석 표현 정제, writer 규칙)은 사용자 결정 대상.
5-2. (다음 GPU 실행에서 확인) §8.13의 영상 끝 근거 효과, I28 효과(사전 인덱싱 시).
6. (보류) C-7 50개 영상 사전 인덱싱(12,780회, 약 12.5–15시간 추정), I22, P12, I25, 번역 제목 형식.

**(2-2) 2026-10-26 – 11-12 이후 상태** (현재 우선순위는 `internal/status/CURRENT_STATUS.md`)
1. (완료, GPU 없음) 보고서 9건 텍스트 분석, 실행 간 차이 분석, 흐름·추측 측정, running example, 단계별 원문 — §2.5.
2. (완료) 코드·폴더 정리와 문서화 — `internal/status/REORG_LOG_20261110.md`.
3. (다음, GPU 필요) 새 경로로 LLM 서버·검색 서비스·보고서 1건 실행 확인(P7). 그 뒤 옛 원본 삭제(P8).
4. (사용자 결정 대기) 패키지 구조화((b) 단계), 외부 공개 방식, 원인 분리 실험 E1–E4, 평가 지표.

**(3) 이후**
- 평가: Video-MME 150문항을 보고서만 보고 풀기, 자동 지표, 사람 검수.
- MERIT 별도 검색 서비스(§4.2 주의점 반영).
- 관제 도메인 템플릿과 데이터(여러 날짜 영상이면 근거 라벨과 시간 표기에 DAY 추가).

### 13.4 미검증 체크리스트

- [x] `run_report.py` 실제 실행 (1회, 10sec 캐시)
- [x] writer 규칙 4의 실제 효과 (8/14 → 4/19, 1회)
- [x] 결정 5: 결론 섹션과 섹션 수 상한 준수 (1회)
- [x] 결정 6: 실제 번역 (6/6 성공, 표기 보존, 품질 문제 확인)
- [x] full 모드 실제 LLM (10sec만)
- [x] 결정 4(규칙 6 + C0)의 실제 효과와 지연 (§9.14: 4 대 4로 효과 확인 안 됨, 켬에서 writer 반복 루프 2건)
- [x] 번역 보완(한자 재시도, 이름 보호)의 실제 효과 (§9.13: 실패 5/17, 잔존 3)
- [x] 사전 인덱싱 영상 1개 전체 (분할 적용 전 코드, 668초, §9.6)
- [x] 분할 OpenIE·응답 구제·폭주 절단의 GPU 실행 효과 (영상 3개, §9.10)
- [x] 분할 전후 triple 비교 (§9.11. 분할 기준이 있는 것은 영상 1의 10min뿐이라 표본이 작다)
- [x] 4개 granularity 캐시로 검색 (L0/L1/full), 타임아웃 여유 (§9.12, 지연만. 품질 비교는 미실시)
- [ ] HTTP OpenIE와 in-process OpenIE 결과 비교
- [ ] 규칙 근거 검사의 재현율·일반화
- [x] 같은 조건 다중 실행의 편차 (2026-10-26: 영상 3개 × 3회 분석, §2.5. C-5는 조건당 2회. OpenIE 재계산 편차는 §9.11에서 Jaccard 0.2–0.3)
- [x] 여러 영상 연속 처리 시 검색 서비스 영상 교체 (§9.12: 2.0–2.4초, 메모리 누적 없음)
- [ ] `llm.backend=openai` 경로
- [ ] vLLM 교체
- [ ] 검색 결과·보고서 품질의 정량 평가

### 13.5 산출물과 백업 위치

| 위치 | 내용 |
|---|---|
| `report_framework/*.py`, `config.yaml`, `run_prebuild*.sh` | 코드와 설정 (2026-11-10: 구성 전체는 `README.md`) |
| `docs/`, `internal/` | 문서 (2026-11-10 이전에는 루트의 `*.md`, 색인 `docs/README.md`) |
| `tests/_artifacts/gpu_test/` | 실제 10sec 캐시와 프레임 (테스트 전용) |
| `tests/_artifacts/gpu_report/` | 보고서 A 원본 `report.md`, `outline.json`, `llm_server.log` |
| `tests/_artifacts/pipeline_test/smoke_grounded/` | 보고서 A를 후처리한 결과 (`report.md`, `frames/`) |
| `tests/_artifacts/gpu_e2e/outputs/report_run1/` | 보고서 B 전체 산출물 (`report.md`, `report_ko.md`, `report_raw.md`, `report.json`, `validation.json`, `frames/`) |
| `tests/_artifacts/gpu_e2e/` | B 실행 설정(`config_l1.yaml`, `config_full.yaml`), 서버·서비스 로그, `summary.json` |
| `tests/_artifacts/analysis/` | `smoke_metrics.json`(A), `e2e_run1_metrics.json`(B) |
| `tests/_artifacts/pipeline_test/{ok, bad_planner, no_conclusion, too_many, translate_*, edge}` | CPU 테스트 출력 |
| `tests/_artifacts/test_cache/`, `dr_logs*` | 가짜 모델 캐시, Deep-Reporter 세션 로그(테스트) |
| `cache/episodic/` | 사전 인덱싱 캐시: 검증 영상 3개의 4단위 캐시, `_done/` 표식 3개(2026-10-25 C-1). 2026-11-10에 `WorldMM/output/memory/videomme_long_qwen3vl-8b/report_framework_index/`로 복사했고 설정은 그쪽을 쓴다. 이 원본은 2026-11-12 삭제(목록 `internal/legacy/DELETED_20261112_originals.txt`) |
| `WorldMM/output/memory/videomme_long_qwen3vl-8b/` | (report_framework 밖) 50개 영상 메모리와 사전 인덱싱 캐시. `README.md`, `MANIFEST.json`(파일별 md5) |
| `scripts/memory_build/`, `docker/`, `patches/worldmm/`, `rf_config.py` | 2026-11-10 추가: 메모리 구축 스크립트, 컨테이너 정의 사본, WorldMM 로컬 수정 patch, 설정 로더 |
| `outputs/3videos_20261022_120438/`, `outputs/3videos_20261022_141051/` | 영상 3개 실행 기록(§9.6, §9.8). 보고서는 없음 |
| `outputs/3videos_20261022_160548_gated/` | 대기 후 자동 시작 기록(§9.9, `gate_run.log`, `gate.json`). 시작하지 않음 |
| `migration/`, `MIGRATION_HANDOFF.md` | 서버 이전 준비(rsync 규칙, 영상 md5, 패키지 목록, 인수인계 메모) |
| `outputs/c1_prebuild_20261025_121542/` | C-1 사전 인덱싱 기록(§9.10) |
| `outputs/c3_probe_20261025_125223/` | C-3 검색 확인(`probe.json`, §9.12) |
| `outputs/c4_reports_20261025_130200/` | C-4 보고서 3건(§9.13) |
| `outputs/c5_c0_20261025_132130/` | C-5 첫 시도(중단, `ABORTED.txt`, 비교에 미사용) |
| `outputs/c5_c0_20261025_132851/` | C-5 재실행 8건(§9.14, 각 폴더 `metrics.json`) |
| `results/c2_openie_compare.json` | C-2 비교 결과(§9.11) |
| `backups/cache_before_c1_20261025/`, `backups/cache_after_c1_verified_20261025/` | C-1 직전 캐시, I29 확인 후 캐시 사본 (뒤의 것은 현재 인덱스와 같아 2026-11-12 삭제) |
| `results/openie_exp/` | OpenIE 디코딩 실험 결과(§9.7) |
| `logs/` | 사전 인덱싱 로그(`prebuild_*.log`, `prebuild_http_pilot.out`, `prebuild_llm_*_gpu{4,5,6}.log`), 3영상 실행 콘솔 출력(`gpu_3videos.out`, `gpu_3videos_2gpu.out`) |
| `backups/` | `.venv` 수리 전 원본, 2026-10-22 수정 전 파일(`prebuild_episodic_index.py.bak_20261022_split`, `run_service_capped.py.bak_20261022`, `REPORT_ISSUES_AND_FIXES.md.bak_20261022_i22`, `DESIGN_AND_STATUS.md.bak_20261022_split`), 2026-10-25 문서 정합성 수정 전 문서 6종(`*.md.bak_20261025_b`), 삭제 전 캐시 일부(`cache_before_split_20261022/`: 영상 1의 10min OpenIE 결과와 완료 표식, 영상 2의 10sec·30sec·3min OpenIE 결과. 2026-10-25 파일로 재확인) |

- 설정 기본값의 `logs/deep_reporter/`, `cache/frames/`는 아직 만들어지지 않았다. 지금까지의 실제 실행은 테스트 스크립트가 출력 위치를 `tests/_artifacts/`나 `outputs/3videos_*` 아래로 지정했기 때문이다.
- Claude 세션 scratchpad(`/tmp/claude-1000/...`)의 사본은 임시라 사라질 수 있다. `tests/`가 정본이다.
