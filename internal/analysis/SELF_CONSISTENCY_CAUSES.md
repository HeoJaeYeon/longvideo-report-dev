# 같은 조건 반복 실행이 서로 다른 이유 — 현상과 원인 추적

- 작성: 2026-10-26 (컨테이너 시계 UTC). GPU 사용 없음. `SELF_CONSISTENCY_ANALYSIS.md`의 후속이다.
- 대상: `outputs/p9p19_check_20261025_141401/` 9건(영상 3개 × r1–r3).
- 도구
  - `analysis/divergence_trace.py` → `results/divergence_trace_20261026.json`
  - `analysis/self_consistency_check.py`
  - Deep-Reporter 세션 로그(각 LLM 호출의 입력·출력 전문)
- 표기: (코드) 코드에서 확인, (실측) 로그·출력에서 계산, (대조) 캡션과 직접 비교, (가설) 확인하지 못한 추정.

---

## 0. 질문에 대한 답

| 질문 | 답 | 근거 |
|---|---|---|
| temperature가 실행마다 **달라서** 생긴 차이인가? | **아니다.** 9건 모두 같은 설정(temperature 0.7, top_p 0.8, top_k 20)으로 **무작위 샘플링**했다. 차이는 temperature 값의 차이가 아니라 **샘플링의 무작위성**(seed 고정 없음)에서 나온다 | §1 (코드·설정 파일) |
| 무작위성 말고 다른 입력 차이가 있었나? | 없었다. 설정 파일은 포트·로그 폴더만 다르다. planner 프롬프트는 영상마다 3회가 **바이트 단위로 같았다**(MD5 일치). 같은 GPU에서 돈 실행끼리도 결과가 달랐다 | §2.1 (실측) |
| outline이 달라져서 이후 차이가 커지는가? | **맞다. 다만 그것만은 아니다.** ① planner 출력이 첫 섹션 설명 중간(74–179자 지점)부터 갈라진다. ② 섹션 구성과 다룰 범위가 달라진다. ③ 같은 섹션 설명을 받아도 **query 생성에서 가장 크게 달라진다**. ④ 근거가 거의 겹치지 않게 된다. ⑤ 앞 섹션 내용이 다음 섹션의 query·writer 입력으로 들어가 차이가 **연쇄적으로 누적된다** | §2–§3 (실측) |
| 결말이 실행마다 다른 이유는? | 결말 서술은 **planner가 결말을 계획에 넣었는지**와 **결론 섹션의 검색어가 무엇을 따라갔는지**로 정해졌다. 틀린 결말 4건은 두 유형이다: (a) planner checklist가 틀린 결말을 미리 적음(2건), (b) 결론 근거에 끝부분이 없는데 writer가 결말을 지어냄·잘못 인용(2건) | §4 (대조) |

---

## 1. 실제 생성 설정 (코드·설정 파일 확인)

| 위치 | 확인 내용 |
|---|---|
| Deep-Reporter `llms/factory.py` | primary LLM(`ReasoningOpenAI`)을 만들 때 `temperature`를 넘기지 않는다 → `temperature_val = None` |
| Deep-Reporter `llms/reasoning_openai.py` | `temperature_val`이 None이면 요청에 temperature를 넣지 않는다(155·340·388·461행 등). top_p·seed도 보내지 않는다 |
| 우리 `local_llm_server.py` 120–130행 | 요청에 temperature·top_p가 있을 때만 생성 인자로 넘긴다. 이번 요청에는 없어서 `max_new_tokens`만 넘어갔다. seed 설정 코드는 없다 |
| WorldMM `qwen3vl.py` `generate` | `{**self.kwargs, **kwargs}`로 `model.generate`를 호출한다. 서버가 `LLMModel(model_name=...)`만으로 만들므로 인스턴스 kwargs는 비어 있다. seed 설정 없음 |
| 모델 `generation_config.json` (두 HF 캐시 모두 같은 snapshot `0c351dd…`) | `do_sample: true`, `temperature: 0.7`, `top_p: 0.8`, `top_k: 20`, `repetition_penalty: 1.0` |
| 검색 서비스 L1 필터 `EndpointLLM.generate` | 같은 LLM 서버에 temperature 없이 요청한다 → 같은 샘플링 |

- 결론: **한 보고서의 LLM 호출 19회(planner 1, 섹션마다 query 1·L1 필터 1·writer 1)가 모두 temperature 0.7 샘플링이다.** 9건 모두 설정이 같다.
- 실행 위치: GPU 4–7의 묶음 4개. 설정 파일(`config_s0–s3.yaml`)은 LLM·검색 포트와 로그·프레임 폴더만 다르다(실측 diff).
  - `54k2g9ddy4M` r2·r3은 같은 묶음(GPU 4)에서, `0RxMZBLeqRI` r1·r3은 같은 묶음(GPU 5)에서 실행됐는데도 결과가 달랐다.
  - 그래서 GPU 차이를 주원인으로 볼 근거는 없다. GPU 연산의 미세한 비결정성이 따로 영향을 주는지는 측정하지 않았다.

---

## 2. 어디서 갈라지는가 (단계별 추적, 실측)

### 2.1 planner: 입력은 같고 출력이 첫 섹션 중간에서 갈라진다

| 영상 | planner 입력(3회) | 출력이 같았던 앞부분 | 처음 갈라진 곳 (예) |
|---|---|---|---|
| `-QuCz7kxBr8` | 동일(23,899자, MD5 `a447867c…`) | 175–179자 | "…Mitchell, and an unnamed sixth player—" 다음에 r1 "and establishes the setting", r2 "and the setting", r3 "who gather on a sunny…" |
| `0RxMZBLeqRI` | 동일(33,788자) | 104–169자 | "This section introduces the video's framing" 다음에 r1 ", including its disclaimer…", r2·r3 " of Roma identity through historical…"(r2·r3은 169자에서 다시 갈라짐) |
| `54k2g9ddy4M` | 동일(31,980자) | 74–166자 | "This section " 다음에 r1 "introduces the video's opening segments", r2·r3 "covers the opening of the video (00:00:00-00:10:00)" |

- 처음 갈라지는 지점은 뜻이 거의 같은 단어 선택이다. 그 뒤 토큰은 앞에서 고른 단어를 조건으로 생성되므로, 섹션 구성까지 달라진다.
- 같은 입력에서 이렇게 갈라지는 것은 샘플링 생성의 정상 동작이다.

planner 차이의 내용(대조)

| 영상 | 달라진 것 |
|---|---|
| `-QuCz7kxBr8` | 섹션을 나누는 **단위**가 달랐다. r1은 가젯 2개씩 묶고 마지막 섹션에 최종 점수·엔드 스크린을 넣었다. r2는 **가젯 하나에 섹션 하나**로 나눠, 상한 6(결론 포함) 안에서 앞쪽 가젯 4개(01:22–08:20 근거)만 다뤘다. r3은 그 중간이다. 세 실행 모두 섹션 설명에 시간 범위를 쓰지 않았다 |
| `0RxMZBLeqRI` | r2·r3은 섹션 설명에 10min 개요의 10분 창(00–10, 10–20, 20–30, 30–40은 섹션 4·5 두 개)을 시간 범위로 붙였다. r1은 시간 범위 없이 주제(면책 문구, 오분류, 기원…)로 나눠 섹션 1–4가 모두 첫 1.5분 근거에 몰렸다 |
| `54k2g9ddy4M` | 3회 모두 10분 창마다 섹션 하나다. 그러나 창 안의 어떤 꼭지를 고를지, 내용을 어느 창에 배정할지가 달랐다. 예: 학교 화재를 r1·r3은 "(00:40:00-00:50:00)"에, 개요는 30–40분 창 요약 안에 넣고 있다. 40–50분 창의 반려동물 심령술사는 r2만 골랐다 |

### 2.2 그 뒤 단계에서의 차이 (같은 위치의 섹션끼리 비교)

같은 위치의 섹션을 실행 쌍마다 비교했다.
- plan·검색어·본문: TF-IDF 코사인
- 근거: episodic uid Jaccard

| 섹션 | 단계 | `-QuCz7kxBr8` | `0RxMZBLeqRI` | `54k2g9ddy4M` |
|---|---|---|---|---|
| **첫 섹션** (3회 모두 "도입") | plan(설명+checklist) | 0.60–0.73 | 0.40–0.73 | 0.49–0.71 |
| | 검색어 | **0.06–0.59** | 0.29–0.40 | **0.06–0.22** |
| | 검색된 근거 | 0.14–0.46 | 0.23–0.46 | 0.07–0.23 |
| | 인용된 근거 | 0.18–0.44 | 0.40–0.80 | 0.08–0.30 |
| | 본문 | 0.52–0.72 | 0.55–0.59 | 0.43–0.61 |
| **결론 섹션** | plan(설명+checklist) | **1.00 (3회 동일)** | 0.67–0.72 | 0.69–0.73 |
| | 검색어 | **0.08–0.22** | 0.17–0.23 | 0.03–0.18 |
| | 검색된 근거 | 0.00–0.07 | 0.07–0.78 | 0.07–0.14 |
| | 인용된 근거 | **0** | 0–0.50 | 0–0.08 |
| | 본문 | 0.26–0.38 | 0.26–0.48 | 0.21–0.36 |

읽는 법
- **가장 크게 떨어지는 곳은 query 생성이다.** `-QuCz7kxBr8`의 결론은 설명과 checklist가 세 실행에서 글자까지 같았다. 그런데도 검색어 유사도는 0.08–0.22, 인용 근거 겹침은 0이었다.
  - 결론 query 생성의 입력 중 실행마다 다른 것은 **앞 섹션 요약(C0)** 하나뿐이다(코드: query 템플릿에 `previous_sections_summary`가 들어감).
  - 그리고 출력 샘플링이 있다.
- 검색어가 다르면 검색 근거도 달라진다. 검색 단계는 질의마다 그래프 검색(LLM 없음)을 하고, L1 필터(LLM 샘플링)가 8개를 고른다(코드). 같은 질의를 반복했을 때 L1 필터 결과가 얼마나 달라지는지는 로그에 없어 측정하지 못했다.
- 본문 유사도(0.21–0.72)는 근거 겹침보다 높다. 같은 영상이라 인물·사물·장소 이름을 공유하기 때문으로 보며(가설), 같은 내용을 말한다는 뜻은 아니다.
- 따라서 "planner 차이 → 이후 증폭"은 맞지만, 단조롭게 커지는 모양은 아니다.
  - **planner와 query 생성 두 곳의 샘플링이 차이의 출발점**이다.
  - 근거 단계에서 차이가 가장 커진다.

### 2.3 실행 안에서의 연쇄 (코드 + 실측)

- 섹션 k의 query 생성과 writer는 섹션 1…k−1에서 실제로 쓴 문장의 요약(C0)을 입력으로 받는다(코드).
- 앞 섹션이 달라지면 뒤 섹션의 입력이 달라지고, 그 차이가 다시 다음 섹션으로 넘어간다.
- 가장 뚜렷한 예가 결론 섹션의 검색어다. 실행마다 **그 실행의 앞 섹션 주제를 따라갔다**(실측).

| 영상 | 실행 | 앞 섹션 주제 | 결론 검색어 |
|---|---|---|---|
| `-QuCz7kxBr8` | r1 | …Silly String, 최종 점수·마무리 | "final score displayed as 3-1…", "video ends with blue and white static end screen" |
| | r2 | Dribble Specs, Dribble Stick, Straight Shooter, Flick Glove | "group rates SKLZ Dribble Stick…", "…Straight Shooter Strap", "Flick Glove challenge ends…" |
| | r3 | …Shot Coach, Never Ending Defender | "…Straight Shooter Strap…", "coach uses SHOT COACH…", "…NEVER ENDING DEFENDER drills" |
| `54k2g9ddy4M` | r1 | …Liendo, 학교 화재 | "video concludes with community recovery after school fire", … |
| | r2 | …심령술사·염소 | "video concludes with studio anchor wrapping up…", "…goat herd crossing road" |
| | r3 | …Liendo, 학교 화재 | "Joshua Liendo discusses…", "Montfort…", "Eabametoong…school fire aftermath…" |

- 그래서 결론은 영상 전체가 아니라 **그 실행이 앞에서 다룬 범위**를 다시 검색한다.
- 결론이 영상의 끝부분을 근거로 갖는 것은 앞 섹션이 끝부분을 다뤘을 때뿐이었다.

---

## 3. 차이가 커지는 구조적 이유 (코드 + 실측)

1. **섹션 수 상한 6과 섹션 단위 선택이 맞물린다.** 상한은 고정인데 섹션 하나에 얼마만큼을 담을지는 planner가 샘플링으로 정한다.
   - 잘게 나누면 영상 앞부분에서 섹션이 바닥난다(`-QuCz7kxBr8` r2).
   - 크게 나누면 영상 전체를 덮는다(`54k2g9ddy4M` 3회, `0RxMZBLeqRI` r2·r3).
2. **섹션마다 검색이 독립적이고 시간 제약이 없다.** 검색은 섹션 설명에서 만든 검색어로 영상 전체를 찾는다.
   - 섹션이 다룰 시간 범위를 지정하는 장치가 없다.
   - 같은 장면이 여러 섹션에 다시 나오고, 빠지는 구간이 생긴다.
3. **결론 섹션도 따로 검색한다.** 결론의 근거는 앞 섹션 요약에서 만든 검색어로 정해진다(§2.3). 영상의 실제 끝을 반드시 보는 장치는 10/25 실행에는 없었다. 10/26에 추가한 영상 끝 근거 `txt0`이 이 지점을 겨냥하며, GPU로는 아직 확인하지 않았다.
4. **planner는 10min 요약 개요만 본다.** 10분 창 안의 꼭지 순서와 경계를 잘못 배정할 수 있다(`54k2g9ddy4M` 학교 화재). 그 판단이 샘플링마다 달라진다.

---

## 4. 결말 서술이 갈린 원인 (사례별, 대조)

실제 결말은 10sec 캡션 기준이다(`SELF_CONSISTENCY_ANALYSIS.md` §4.3).

| 보고서 | 결말 | 원인 추적 |
|---|---|---|
| `-QuCz7kxBr8` r1 | 맞음 | planner 섹션 5 설명에 "the closing instructional segment …", "the video's end screen"이 있음 → 섹션 5·결론 검색어가 끝부분을 찾음 → 37:20–37:30 근거 인용 |
| `-QuCz7kxBr8` r2 | **틀림** | 결론 episodic 근거 8개 중 7개가 00:00–10:00 안, 1개가 30:30–31:00이다(끝부분 없음). writer가 "The video ends without declaring a winner or final score", "The final frames show the group still preparing for the next test"를 **인용 없이** 썼다(writer 규칙 7 위반). "POWERHANDZ" 마지막 시연은 00:00–10:00 10min 요약을 인용했다(실제 11:30 장면) |
| `-QuCz7kxBr8` r3 | **불완전·잘못된 인용** | "the video ends with them continuing the game under the "FIRST TO 3 WINS" rule [txt5][txt7]"이라고 썼다. txt5(19:50–20:00)와 txt7(10:00–20:00 10min)에는 이 문구가 없고, 규칙 검사가 `unsupported`로 표시했다. 실제 문구는 29:00 근거에 있다 |
| `0RxMZBLeqRI` r1 | 맞음 | planner 결론 checklist에 "Confirm that the video concludes with a global perspective and credits"가 있음 → 결론 검색어 "video concludes with global perspective and credits" → 끝부분 근거 |
| `0RxMZBLeqRI` r2·r3 | 맞음 | planner가 30–40분 창을 섹션 4·5로 계획 → 섹션 5가 개선문·지구본 근거를 다룸 |
| `54k2g9ddy4M` r1 | **틀림** | planner 결론 checklist가 "State that the video concludes with community recovery and athletic legacy as its final themes"라고 **미리 틀린 결말을 적었다**. writer 결론 첫 문장이 그대로 "ultimately concluding with themes of community recovery and athletic legacy" |
| `54k2g9ddy4M` r2 | 맞음 | planner가 40–50분 창에 심령술사·염소를 배정 → 섹션 5와 결론 검색어가 마지막 앵커 장면을 찾음 |
| `54k2g9ddy4M` r3 | **틀림** | planner 결론 checklist "Confirm the video's conclusion with Liendo's gold medal and community recovery stories" → writer "The video concludes with Liendo's gold medal and the community's recovery stories" |

정리
- 맞은 4건은 모두 **planner가 결말 구간을 계획(섹션 또는 checklist)에 넣은** 경우다.
- 틀린 4건은 두 유형이다.
  - (a) planner가 틀린 결말을 checklist에 넣고 writer가 따름: `54k2g9ddy4M` r1·r3. 개요만 보고 학교 화재를 마지막 꼭지로 오판한 결과다.
  - (b) 결론 근거에 끝부분이 없는데 writer가 결말을 서술함: `-QuCz7kxBr8` r2·r3. 하나는 인용 없이, 하나는 관련 없는 근거를 인용했다.
- 즉 결말의 정오는 샘플링으로 정해진 **planner의 계획**에 달려 있었고, writer 규칙 7은 (b)를 막지 못했다.

---

## 5. temperature를 낮추면 해결되는가 (확인한 것과 못 한 것)

- 확인한 것
  - 차이의 출발점은 같은 입력에 대한 샘플링 출력의 차이다(§2.1).
  - temperature 0(greedy) 또는 seed 고정이면 같은 입력에 같은 출력이 나올 것으로 **기대**된다. 이번 측정은 아니다.
  - GPU 연산의 비결정성이 남는지는 확인하지 않았다(가설).
- 바꾸려면: Deep-Reporter는 temperature를 보내지 않으므로 Deep-Reporter를 고치지 않는 방법은 우리 `local_llm_server.py`에서 기본 생성 설정을 바꾸는 것이다(기존 파일 수정이라 승인 필요). L1 필터와 번역도 같은 서버를 쓰므로 함께 바뀐다.
- 그래도 남는 문제(이번 결과에서 보이는 것)
  - **일관성이 정확성을 뜻하지 않는다.** 결정적 생성이면 3회가 같아지지만, 그 하나가 `-QuCz7kxBr8` r2나 `54k2g9ddy4M` r1처럼 틀린 결말·좁은 범위일 수 있다. 결말 정답은 샘플링 9건 중 5건(r1–r3 합계)이었다.
  - 구조적 원인(§3: 섹션 상한과 단위 선택, 시간 제약 없는 섹션별 검색, 결론의 독립 검색, 개요만 보는 planner)은 temperature와 무관하다.
  - greedy가 이 모델의 반복 루프(P9)를 늘리는지 줄이는지는 측정하지 않았다. 지금도 temperature 0.7에서 루프가 2/9건 있다.
- 원인을 분리하려면 필요한 실험(GPU 필요, 제안)

| 실험 | 확인하는 것 |
|---|---|
| E1. 같은 planner 프롬프트를 temperature 0.7로 5–10회, 0으로 2–3회 | planner 출력 분산의 크기, greedy의 재현성(GPU 비결정성 포함) |
| E2. outline을 고정(`without_planner`, 한 실행의 outline 재사용)하고 3회 | planner를 뺀 나머지 단계(query·L1 필터·writer)의 분산 |
| E3. 같은 검색어 목록으로 L1 필터 반복 | 검색 단계 자체의 분산 |
| E4. temperature 0으로 보고서 3회 | 보고서 전체 재현성, 반복 루프 발생 |

---

## 6. 요약

1. 9건의 설정과 planner 입력은 같았다. 차이는 **temperature 0.7 샘플링의 무작위성**(seed 없음)에서 시작한다. temperature 값이 달라서가 아니다.
2. planner 출력이 첫 섹션 설명 중간에서 갈라진다. 이것이 섹션 단위, 다룰 범위, 결말 계획의 차이로 이어진다.
3. 그 뒤 **query 생성**에서 차이가 가장 크게 벌어진다. 같은 결론 설명을 받아도 앞 섹션 요약과 샘플링 때문에 검색어가 달라지고, 근거가 거의 겹치지 않는다. 앞 섹션 내용이 다음 섹션 입력이 되는 구조라 차이가 연쇄된다.
4. 결말의 정오는 planner가 결말 구간을 계획에 넣었는지에 따라 정해졌다. 틀린 경우는 planner가 틀린 결말을 checklist에 적었거나(2건), 근거 없이 writer가 결말을 썼다(2건).
5. temperature를 낮추면 재현성은 좋아질 것으로 예상되지만, 정확성과 범위 문제는 구조적 원인이라 따로 다뤄야 한다. 분리 실험(E1–E4)은 GPU가 필요하다.
