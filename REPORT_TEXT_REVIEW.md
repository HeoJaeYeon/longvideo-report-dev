# 보고서 9건 텍스트 분석 — 논리 정합성, 서사, 중복, 추상어, 영상 전체 서술, 섹션 구성과 원인

- 작성: 2026-10-26 (컨테이너 시계 UTC). GPU 사용 없음. 그림(이미지)은 보지 않고 **보고서 텍스트만** 분석했다.
- 이 문서는 이전의 `REPORT_TEXT_REVIEW_r1.md`(r1 3건)와 `REPORT_TEXT_REVIEW_r2r3.md`(r2·r3 6건과 종합)를 합쳐 다시 쓴 것이다. 이전 두 문서는 `backups/`로 옮겼다.

## 0. 범위와 방법

### 0.1 대상

`outputs/p9p19_check_20261025_141401/<영상>__c0_written__r{1,2,3}/report.md` 9건.

| 영상 | 내용 | 길이(10sec 캡션 끝) | 실제 마지막 장면(10sec 캡션) |
|---|---|---|---|
| `-QuCz7kxBr8` | 남성 6명이 농구 가젯 12개를 시험 | 00:37:37 | 36:50 "3-1", "ZAK JESSE & KRIS WIN" → 37:00 8번 선수 → 37:30 엔드 스크린 "Thank you for watching" |
| `0RxMZBLeqRI` | 로마(집시)의 기원·차별·박해 역사 | 00:30:32 | 30:00 개선문 앞 애니메이션 캐릭터, 30:08 크레딧 → 회전 지구본·국기 → 암전 |
| `54k2g9ddy4M` | CBC 뉴스 꼭지 모음(약 12개) | 00:45:14 | 42분 이후 반려동물 심령술사·염소 → 44:50 앵커 → 공항 → CBC 로고 검은 화면 |

- 설정은 9건이 같다: Qwen3-VL-8B, L1, C0 켬, 섹션 상한 6, 서버 출력 상한 3,072, 번역 끔, 커밋 `baf08d8` 시점 코드(`PIPELINE_WALKTHROUGH.md` §0.1).
- r1–r3은 같은 조건의 반복 실행이다. 생성이 샘플링이라 내용이 다르다(`SELF_CONSISTENCY_ANALYSIS.md`).

### 0.2 방법과 표기
- 9건의 본문을 처음부터 끝까지 읽었다. 지적한 사례는 보고서가 인용한 근거(`report.json`)와 WorldMM 캡션 원문(10sec/30sec/3min/10min)으로 대조했다.
- 영상 자체는 보지 않았다. "실제 장면"은 캡션 기준이다.
- 표기
  - (측정): 스크립트로 계산
  - (대조): 보고서 문장과 근거·캡션을 직접 비교
  - (확인된 원인): 원인 → 결과 경로를 코드·데이터로 확인
  - (가능성): 근거가 부분적이거나 실험으로 확인하지 않은 추정
- 측정 정의
  - **추상·평가어**: reinforce·underscore·highlight·emphasize·symbolize·juxtapose·resilience·integration·narrative·framing·tone·legacy·triumph·erasure·affirm·structured·lighthearted 등 고정 목록의 등장 수.
  - **메타 서술**: "This section…", "The video's framing/structure…", "The video highlights/underscores…"처럼 영상 내용이 아니라 영상·섹션 자체를 평하는 문장.
  - **문자열 근사 중복**: 같은 보고서 안 문장 쌍의 문자열 유사도(SequenceMatcher) 0.6 이상. 표현을 바꾼 반복은 잡지 못하므로, 중복은 읽으면서 확인한 사례를 함께 적었다.
  - **근거 복사**: 문장과 그 섹션 근거 문장의 최대 유사도가 0.8 이상이면 근거를 거의 그대로 옮긴 것으로 본다.
  - **다룬 3분 구간**: 그 구간에 중앙값이 있는 10sec·30sec·3min 근거를 인용한 구간 수(`SELF_CONSISTENCY_ANALYSIS.md` §2.1).

---

## 1. 9건 지표 (측정)

| 보고서 | 문장 / 단어 | 인용 없는 문장 | 추상·평가어 (100단어당) | 메타 서술 | 문자열 근사 중복 (섹션 간) | 근거를 거의 그대로 옮긴 문장 | 다룬 3분 구간 | 결말 서술 (대조) |
|---|---|---|---|---|---|---|---|---|
| `-QuCz7kxBr8` r1 | 123 / 3,004 | 33% | 2.8 | 6 | 10 (7) | 28% | 7/13 | 맞음 |
| `-QuCz7kxBr8` r2 | 101 / 2,432 | 22% | 1.6 | 1 | 6 (6) | 27% | 5/13 | **틀림** |
| `-QuCz7kxBr8` r3 | 129 / 3,104 | 21% | 2.4 | 2 | 12 (5) | 30% | 8/13 | **틀림(불완전)** |
| `0RxMZBLeqRI` r1 | 116 / 3,068 | 44% | 4.6 | 17 | 7 (1) | 34% | 5/11 | 맞음(인용 없음) |
| `0RxMZBLeqRI` r2 | 116 / 3,228 | 22% | 4.1 | 6 | 7 (1) | 12% | 6/11 | 맞음 |
| `0RxMZBLeqRI` r3 | 103 / 2,917 | 32% | 4.1 | 14 | 2 (0) | 28% | 8/11 | 맞음 |
| `54k2g9ddy4M` r1 | 122 / 3,164 | 20% | 3.7 | 9 | 2 (1) | 32% | 8/16 | **틀림** |
| `54k2g9ddy4M` r2 | 133 / 3,227 | 21% | 2.7 | 4 | 5 (4) | 38% | 11/16 | 맞음 |
| `54k2g9ddy4M` r3 | 161 / 3,744 | 19% | 3.2 | 10 | 11 (6) | 38% | 12/16 | **틀림** |

- 9건 모두 `validation.json` 상태는 `passed`이고 섹션은 6개다.
- 근거 복사율이 낮은 `0RxMZBLeqRI` r2(12%)는 근거가 적은 섹션에서 같은 해석을 바꿔 쓰며 늘린 보고서다(§2.2).

---

## 2. 보고서별 분석

### 2.1 `-QuCz7kxBr8` (농구 가젯 시험)

#### r1

**구성과 영상 전체 서술**

| 섹션 | 제목 | 인용 근거 시점(중앙값) |
|---|---|---|
| 1 | Introduction to the Participants and Setting | 01:45 |
| 2 | Testing the SKLZ Dribble Stick and the Straight Shooter Strap | 04:38 |
| 3 | Testing the Flick Glove and Shot Coach | 08:25 (근거 범위 00:00–21:00) |
| 4 | First Made Shot Shoots Silly String Game, Defensive Drills, Never Ending Defender | 18:40 |
| 5 | Final Scoring Segment and Closing Instructional Content | 37:05 |
| 6 | Conclusion | 37:25 |

- 섹션 순서는 대체로 시간순이다.
- 10:30–18:00과 25:30–36:00(약 10분)을 다루는 근거 인용이 없다(측정). 그래서 다음 내용이 없다(대조).
  - 12:00 이후 "MOST DRIBBLES IN 15 SECONDS" 챌린지
  - 29:00의 "FIRST TO 3 WINS / LOSER DOES FORFEIT" 최종 게임 규칙
  - 27–36분 패드 수비 훈련
- "12 viral sports gadgets", "two teams of three"를 소개하지만, 본문은 가젯 6–7개만 다루고 팀 대결의 진행·점수·최종 팀 결과를 추적하지 않는다.
  - 점수 표시("5 to 6, then 4", "SCORE 7")가 무엇의 점수인지 설명이 없다.
  - 영상이 팀 총점을 보여 주는지는 캡션만으로 확인하지 못했다.
- 결말 서술(섹션 5, 결론)은 엔드 스크린과 맞는다.

**논리 정합성 (대조)**

| 위치 | 문제 | 근거 |
|---|---|---|
| S2 | "initially making one shot (0/1), then missing several … 0/3 … pushing the tally to 3/16 … approaches 15 successful shots" | "making one shot (0/1)"이 그 자체로 모순이고, 3/16과 "15 successful shots"도 맞지 않는다. 근거 10min 요약의 문장 그대로다(캡션 자체 불일치) |
| S3 | "At 00:19:30, the man in the black hoodie performs sit-ups … "CASH LOST" … punishment for the fewest flick shots" | 캡션상 "CASH LOST" 윗몸일으키기는 **10:40–11:10**이다. 시간 없는 10min 요약 [2]를 인용했고, 19:30은 같은 섹션 다른 근거(Shot Coach, 19:30–20:00)의 시각이다. "SCORE 7"(캡션 11:28)도 19:30 뒤 일처럼 놓였다 |
| S3 | 윗몸일으키기 벌칙 문단에 "bouncing titties", "Bro, I'm wearing a big shirt", "off-rhythm during the jumping jacks"를 붙임 | 같은 농담을 S2에서 팔벌려뛰기 벌칙(약 07:20)의 장면으로 이미 서술했다. 두 벌칙 장면을 섞었다 |
| S3 ↔ S4 | 같은 사건(세 명이 동시에 점프해 슛, 파란 저지 승리)을 S3은 "Shot Coach synchronized shooting drill (00:18:00)", S4는 "Silly String 게임"으로 서술 | 둘 다 같은 3min 캡션(18:00–21:00, [20])과 그 하위 캡션을 인용한다. 그 3min 캡션은 Event 1–5로 게임, 동시 슛, Shot Coach 훈련, 제품 문구를 한 텍스트에 함께 요약한다 |
| S4 | 같은 게임 규칙을 "SILLY STRING AT LOSER"와 "SILLY STRING AT 100%"(00:18:29) 두 가지로 쓰고 맞추지 않음 | 10sec 캡션(18:20)이 화면 문구를 "GILLY STRING AT 100%"로 적었다. 30sec 요약은 이를 "performance claim tied to the product's functionality"로 해석했고, 3min 요약은 "SILLY STRING AT 100%, tying the product's performance claim to the game's outcome"으로 바꿨다. 보고서는 3min 문장을 그대로 옮겼다. 다른 10sec·30sec 캡션(18:30)은 "AT LOSER"다 |
| S3, S4 | "The video closes with a close-up of the Shot Coach device" 2회, "The video concludes with the Shot Coach…" 1회, "The video's final moments emphasize…" 1회 | 3min 캡션(18:00–21:00)이 자기 구간 끝을 "The video closes with…"로 요약한 문장이다. 실제 끝은 37:37이다(P19) |
| S4 | "a black training device, likely the harness", "a defensive training exercise, where a player can be defended by another player" | 앞 문장은 근거에 없는 추정이다. 뒤 문장은 semantic triple `(player, can be defended by, another player)`을 옮긴 것이라 내용이 없다 |
| S6 | "ZAK JESSE & KRIS"와 S1의 "Chris, Zach"의 관계를 설명하지 않음 | 화면 문구(10sec 36:50)와 다른 캡션의 표기가 다르다. 같은 인물인지는 확인하지 못했다 |

**서사·중복·추상어**
- 서사: 섹션 1–2는 가젯 → 규칙 → 시도 → 평가 순서로 흐름이 분명하다. 섹션 3–4는 8분, 10분, 18–20분, 25분의 사건을 한 섹션에 묶어 오간다.
- 중복: Shot Coach 훈련 단락("SHOOT FROM HALF COURT 5 TIMES WITH SHOT COACH", 손목 밴드 조정)이 S3과 S4에 거의 같게 두 번 나온다. S3 마지막 두 단락은 앞 단락의 규칙·벌칙을 다시 요약한다.
- 추상어: structured(10), reinforcing(9), competitive(7), lighthearted(7)가 많다(측정). 예: "reinforcing the structured, tech-assisted training environment"는 3min 캡션 문장을 그대로 옮긴 것이다.

#### r2

**구성과 영상 전체 서술**
- 섹션 구성: 도입 → Dribble Specs → Dribble Stick → Straight Shooter → Flick Glove → 결론. 가젯 하나에 섹션 하나다.
- 인용 근거는 거의 모두 00:00–11:30이다. 37분 영상의 앞 3분의 1만 다뤘다(3분 구간 5/13).
- Silly String 게임, Shot Coach, Never Ending Defender, 최종 게임, 엔드 스크린이 없다.

**논리 정합성 (대조)**

| 위치 | 문제 | 근거 |
|---|---|---|
| S1 ↔ S2 ↔ S3 | S1이 이미 Dribble Specs 기록(10:85, 9:51), 점수 5→6→4, Dribble Stick 소개·규칙을 다 서술했는데 S2가 같은 내용을 다시 씀. Dribble Stick 규칙("first to touch … five laps")은 S1·S2·S3에 4번 나옴 | 세 섹션 모두 같은 10min 요약 [1](00:00–10:00)을 주로 인용한다 |
| S2 | "Chris completes the trial in 10:85 seconds … Zach follows, finishing in 9:51" | 근거는 "players like Chris and Zach … times such as 10:85 and 9:51"이다. 누가 몇 초인지는 근거에 없다. 근거보다 구체적으로 단정했다 |
| S3 | "The gameplay proceeds…", "humorous self-deprecation from players who fail to avoid the stick", "The transition to the next gadget is smooth and well-prepared … seamless" | 결과·실패자 등 구체적 사실 없이 인용 없는 일반 서술로 채운 문장이다 |
| S4 | "initially makes one shot (1/1), then misses several, with the tally climbing to 0/3 … 3/16 … approaches 15 successful shots" | 성공 수가 1에서 0으로 줄고, 3/16과 15가 공존한다. 근거의 "(0/1)"을 "(1/1)"로까지 바꿨다 |
| S5 | Flick Glove 섹션 끝에 "The segment ends with a synchronized shot challenge"라며 1-0 일대일·패드 수비 장면을 서술 | 근거 [29]는 **30:30–31:00** 장면이다. 08:00–11:00 섹션에 20분 뒤 장면을 이어 붙였고, "synchronized shot challenge"라는 이름도 근거에 없다 |
| S6 결론 | "The video ends without declaring a winner or final score", "the group still preparing for the next test" | 인용 없다. 실제로는 36:50 "3-1, ZAK JESSE & KRIS WIN", 37:30 엔드 스크린이다 |

**서사·추상어**: 추상어 밀도 1.6/100단어로 9건 중 가장 낮다. 대신 "seamless", "smooth and well-prepared", "lighthearted and collaborative" 같은 내용 없는 상투 문장이 S3에 몰려 있다.

#### r3

**구성과 영상 전체 서술**
- 섹션 구성: 도입 → Dribble Specs·Dribble Stick → Straight Shooter·Flick Glove → 동시 슛·Shot Coach → Never Ending Defender·최종 게임 준비 → 결론.
- 3회 중 다룬 구간이 가장 넓다(8/13). 최종 결과(3-1)와 엔드 스크린은 없다.

**논리 정합성 (대조)**

| 위치 | 문제 | 근거 |
|---|---|---|
| S1 ↔ S2 | S1 마지막 단락("first gadget … donning the goggles … pool visible … rules are clarified")을 S2 첫 단락이 거의 그대로 반복 | 두 섹션 모두 10min 요약 [1] 인용 |
| S2 | "No numerical ratings like "8/10" or "7" are shown in the evidence" | 8/10·7은 이 섹션 checklist "List the ratings given (e.g., 8/10, 7)"에서 온 숫자다. 실제로는 Dribble Stick 평점이다(r1·r2는 근거로 서술). checklist 항목을 부정문으로 채웠다 |
| S2 | 점수 그래픽 5→6→4가 "suggests a rating or score adjustment" | 근거에 없는 추정 |
| S3 | "the blue-jersey man later makes a shot, celebrated with "Woo!" and "WHOOOOOO" graphics" | 10sec·30sec·3min 캡션 모두 **검은 후드 남성**의 슛이다. 인물을 잘못 붙였다 |
| S3 | "nor does it show the forfeit of sit-ups being performed" | 영상에는 윗몸일으키기 벌칙이 있다(10sec 10:40–11:10 "CASH LOST", r2가 서술). 검색 근거에 없는 것을 "영상에 없다"로 일반화했다 |
| S4 | "The video closes with a close-up of the Shot Coach device" 3번 + "The video concludes with a close-up…" 1번 | 3min 요약(18:00–21:00)의 구간 끝 표현을 4번 옮겼다 |
| S4 | 같은 사실(파란 저지 승리, 규칙, AT 100% 문구, Shot Coach의 쓰임)을 5개 단락 중 3–5에서 다시 서술 | 같은 3min 요약 [20] 인용 |
| S4 | "The forfeit outcome … is implied by the product claim overlay … "SILLY STRING AT 100%"" | 캡션 오독에서 시작된 "제품 주장"을 근거로 벌칙을 추론했다(r1의 AT 100% 사례와 같은 출처) |
| S5 | "takes a second shot, and the graphic updates to "1/2" as the ball swishes through the hoop" | 두 번째 슛이 들어갔다면 2/2여야 한다. 근거 3min 요약(24:00–27:00)의 문장 그대로다(캡션 자체 불일치) |
| S5 | 33:00 서술 다음 "At 00:28:00 … WHICH WAS YOUR FAVORITE PRODUCT?" | 섹션 안 시간 역행 |
| S5, S6 | "The video ends with players actively engaged in the game…", 결론 "the video ends with them continuing the game under the "FIRST TO 3 WINS" rule" | 실제 결말(3-1 결과, 엔드 스크린)과 다르다. 결론 인용 근거에 "FIRST TO 3 WINS"가 없다(규칙 검사 `unsupported`) |
| S6 결론 | "Overall, the video successfully demonstrates how these gadgets enhance skill development…" | S3은 같은 그룹이 Straight Shooter Strap에 "1", "-3k"를 줬다고 서술했다. 보고서 안에서 서로 맞지 않는다 |

### 2.2 `0RxMZBLeqRI` (로마 역사)

#### r1

**구성과 영상 전체 서술**

| 섹션 | 제목 | 인용 근거 시점(중앙값) |
|---|---|---|
| 1 | Section 1: Framing the Video — Disclaimers, Visual Montage… | 00:52 |
| 2 | Historical and Cultural Framing of Roma Identity | 00:25 |
| 3 | Depiction of Roma as Historically Misclassified… | 00:50 |
| 4 | Historical Narrative of Roma Origins and Early Misidentification | 01:20 |
| 5 | Depiction of Roma Persecution under Nazi and Communist Regimes | 23:25 |
| 6 | Conclusion | 04:30 |

- 본문 섹션 5개 중 4개가 영상 첫 약 1.5분을 다루고, 그다음이 21–24분이다.
- 다음 내용이 본문에 없다(3min 캡션 기준).
  - 6–9분 Ghaznavid 제국과 인도 기원
  - 9–12분 Vlad Zepes
  - 12–18분 15세기 노동·전쟁, 제국 시대
  - 18–21분 노예제 폐지(Article XIII)
  - 27–30분 현대의 빈곤
- "Section 1:"만 번호 표기가 있어 형식이 다르다.
- 결말 서술(지구본, 암전, 30:08 크레딧)은 캡션과 맞지만 인용이 없다.

**논리 정합성 (대조)**

| 위치 | 문제 | 근거 |
|---|---|---|
| S5 | 제목이 "…and **Communist** Regimes"인데 공산 정권 내용은 "Communism, Chapter VII" 제목 카드뿐 | planner의 섹션 설명·checklist가 정한 주제다. 검색 근거 12개 중 공산 정권 박해를 서술한 캡션이 없다 |
| S5 | "does not show any text overlay stating 500,000–1,500,000 deaths **beyond the one shown at 00:24:00**", "does not show any 1942 deportation … **beyond the footage shown at 00:23:20**" | 앞 문단에서 보여 준 내용을 "보이지 않는다"로 다시 쓴 자기모순 문장이다. "does not show" 문장 7개(마지막 1개는 끊긴 문장)가 checklist 3개와 설명 항목(Gestapo mugshots, 500,000–1,500,000, 1942 Auschwitz, post-war erasure, communist regimes)을 하나씩 짚는다 |
| S5 | "The video does not show any footage of Roma persecution under communist regimes…"가 38회 반복된 뒤 문장 중간("…under")에서 끊김 | writer 반복 루프가 서버 상한 3,072토큰에 걸렸다. 같은 문장 제거 뒤 1회만 남았다 |
| S5 | 21:00 → 22:00 → 23:00 → 24:00 → **23:20 → 23:40**. Auschwitz 장면(1942, 줄무늬 수용복, Zyklon B)을 23:00 단락과 23:20 단락에서 두 번 서술 | 섹션 안 시간 역행과 중복 |
| S4 | "positions Roma **not as a distinct ethnic group** but as a product of historical misreading" | S1이 인용한 면책 문구는 "Gypsy"를 민족 집단(ethnic group)의 이름으로 쓴다고 했다. 같은 보고서 안에서 어긋나는 해석이다. 인용 [4]는 시간 없는 10min 요약이다 |
| S6 결론 | Ghaznavid Empire, "I am also a Roma" 집회, 위성 안테나 건물 앞 소년, 애니메이션 캐릭터 | 본문 섹션 1–5에 없던 새 사실이다. 결론이 자기 검색 근거로 썼다 |

**서사·중복·추상어**
- 해석이 사실보다 앞선다. 메타 서술 17문장으로 9건 중 가장 많다. 예: "This visual framing does not merely document history but actively constructs a counter-narrative…"
- 해석 동사로 장면에 의미를 붙인다(Minecraft 채굴 = "labor or resource extraction").
- S2는 7개 단락 중 대부분이 같은 주장("배제 대 축하의 시각적 대비가 회복력·문화적 연속성을 보여 준다")을 표현만 바꿔 되풀이한다. 근거는 3개만 인용했고 셋째 단락부터는 인용이 없다.
- S4는 "Roma were not 'invented' but misclassified"를 2번, "historical misreading"을 2번 쓴다.
- 추상어 4.6/100단어로 9건 중 가장 높다(narrative 15, erasure 9, frames 8, resilience 6). 이 단어가 든 문장 60개 중 근거 문장과 유사도 0.6 이상은 20개다(측정).

#### r2

**구성과 영상 전체 서술**
- 섹션 구성: 도입 틀 → 역사·문화 재현 → 제도적 박해(21–26분) → 회복력(26–30분) → 지구적 관점(30:00–30:32) → 결론.
- 03:00–21:00이 거의 없다(02:10 이주 지도 1건 제외).
- 섹션 5는 32초짜리 마지막 장면 하나에 섹션 전체를 썼다. planner가 "30–40분" 창을 섹션 4·5 두 개에 배정했다(§5 C12).

**논리 정합성·중복 (대조)**

| 위치 | 문제 | 근거 |
|---|---|---|
| S5 | 같은 해석("검은 화면은 의도적 멈춤이고, 반성을 유도하며, 지역에서 세계로 가는 주제 흐름을 마무리한다")을 단락 8개 이상에서 표현만 바꿔 반복한 뒤 문장 중간("…emphasize the visual nature of the conclusion")에서 끊김 | writer가 서버 상한(130.5초)에서 끊겼다. 같은 문장 제거(39개)는 글자가 같은 문장만 지우므로 바꿔 쓴 반복이 남았다. 인용은 거의 [24][25] 두 개뿐이다 |
| S3 | 21:30 → 21:50 → **21:40** → 22:00. 제목 "From Bismarck-Era Surveillance…"인데 본문에 비스마르크 서술이 없음 | 섹션 안 시간 역행, 제목–본문 불일치 |
| S4 | 29:30 → "Earlier in the section, at 00:28:50" → 26:00. 애니메이션 캐릭터·브라스 밴드·춤추는 여성·붉은 두건 여성 장면을 한 단락 안에서 두 번 서술 | 시간 역행과 섹션 안 중복 |
| S4 | "the far-right rally and **the repatriation announcement**" | "repatriation announcement"는 보고서 어디에도 서술된 적이 없다 |
| S1 | "positioning it as academically and sensitively informed", "a foundation of academic rigor" | 근거(면책 문구, 지도)가 말하지 않는 평가다 |
| 결론 | "post-war repression under communism", "scenes of forced labor" | 본문에 없던 새 내용이다. 박해 서술을 지구본 근거([24][25])로 인용했다 |

#### r3

**구성과 영상 전체 서술**
- 3회 중 다룬 구간이 가장 넓다(8/11). 10–15분(Tiganiada, Vlad Cepish, 15세기 전쟁)과 불가리아 동화 정책을 다룬 유일한 실행이다.
- 1–10분(Ghaznavid 등)과 15–21분(노예제 폐지)은 없다.

**논리 정합성·중복 (대조)**

| 위치 | 문제 | 근거 |
|---|---|---|
| S2 | "a critique of power structures that reduce human value to economic exchange" 3번, "falling dollar bills over Ottoman maps" 4번, "commodification" 4번 | 같은 해석의 반복이다. 인용은 대부분 [5][6][9] |
| S2 | "metaphor for conquest, transformation, and resistance", "satirical yet analytical", "a narrative of agency and mythmaking" | 근거가 진술하지 않는 해석이다 |
| S2 | "At 00:12:40, the video opens with a portrait of Ion Budai-Deleanu…" | 캡션의 구간 시작 표현을 영상 시작처럼 썼다 |
| S3 | 첫 단락과 끝 단락이 "concentration camp imagery **to modern-day protests**"를 대비한다고 쓰지만 본문에 시위 서술이 없음. 1984–85년 불가리아 정책을 "modern-day Bulgaria"라고 씀 | 앞뒤 요약 문장이 본문과 맞지 않는다 |
| S3 | "The video ends with a somber reflection on enduring suffering" | 20–30분 근거의 섹션에서 영상 결말을 단정했다 |
| S4 | "The segment closes with an animated character…" 다음 "The section concludes with a scene at 00:29:30". 29:50 → 28:50 → 29:30 | 같은 섹션에 끝이 두 개이고 시간이 역행한다 |
| 결론 | "concentration camp marches from 1945", "the stylized animation of a Roma girl superimposed over a historical painting" | 본문에 없던 새 내용이다. Maria Bihari 머그샷을 "symbolic imagery … reinforce the group's enduring presence"로 해석했다 |

### 2.3 `54k2g9ddy4M` (CBC 뉴스 모음)

#### r1

**구성과 영상 전체 서술**

| 섹션 | 제목 (planner가 붙인 범위) | 인용 근거 시점(중앙값) |
|---|---|---|
| 1 | Introduction to the Video's Opening Segments (00:00:00-00:10:00) | 02:10 |
| 2 | Unfolding Public Health Crisis… (설명상 00:10:00-00:20:00) | 04:25 |
| 3 | Shift to Personal Tragedy and Institutional Failure, Followed by Athletic Triumph (20–30) | 21:10 |
| 4 | Liendo's Journey and Legacy (30–40) | 31:20 |
| 5 | Community Disaster and Recovery (40–50) | 39:05 |
| 6 | Conclusion | 38:35 |

- 다룬 꼭지는 5개다(캐나다 홍역, 미국 홍역, Montfort 병원, Liendo, 학교 화재).
- 빠진 꼭지: 시위, 트럼프 여론조사, 항공 요금, 캘리포니아 폭설, 폭풍·산불, 반려동물 심령술사, 염소 떼, 마지막 앵커·공항 장면. 오디션 셀프테이프는 한 문장으로 지나간다.
- 섹션 2는 "10–20분"으로 계획됐지만 근거는 03:00–05:00이다.
- 결론이 "ultimately concluding with themes of community recovery and athletic legacy"라고 쓴다. 결론 checklist가 이 결말을 미리 지정했고, 실제 결말과 다르다.

**논리 정합성 (대조)**

| 위치 | 문제 | 근거 |
|---|---|---|
| S1 | "current vaccination levels stand at 79%" | planner checklist에서 온 값이다. 이 섹션 근거에는 없다(규칙 검사 `unsupported 79`) |
| S3 | Liendo 금메달 문장이 txt8(10–20분 10min 요약, 항공 요금 꼭지)과 Montfort 문서 triple을 인용 | 인용 근거가 문장 내용과 다르다. 숫자·따옴표가 없어 규칙 검사로 잡히지 않는다 |
| S3 | "The video closes with Liendo's legacy firmly anchored…" | 20–30분 요약의 표현을 영상 결말로 썼다 |
| S3 ↔ 결론 | S3 "wins gold … at the **Commonwealth Games**" / 결론 "first Black swimmer to win international gold … at the **Doha World Championships**" | 캡션 자체가 두 대회를 모두 "first international gold"라고 쓴다(3min 27:00 Commonwealth 2022, 3min 33:00 Doha). 보고서는 이를 정리하지 않았다 |
| 결론 | 미국 홍역 "41 confirmed cases", 몬트리올 병원 사망을 학교 화재 근거([32][33])로 인용 | 결론 근거 목록에 홍역 근거가 없다(규칙 검사 `unsupported 41`) |

**서사·중복·추상어**
- 서로 독립된 뉴스를 하나의 이야기로 엮는다. 예: "The narrative arc moves from loss to performance, from chaos to clarity, and ultimately, from tragedy to triumph", "The emotional weight of the hospital error is balanced by Liendo's triumph". 근거 캡션이 진술하지 않는 해석이고, 인용이 없거나 무관한 근거를 인용한다.
- 내용 반복: S4 "hasn't returned since 2018" 2번, "swims into the history books" 4번.
- 인용 없는 문장 20%로 비교적 낮고, 사실 서술은 근거를 충실히 옮긴 편이다.

#### r2

**구성과 영상 전체 서술**
- 섹션 구성: 도입(홍역·시위·트럼프·Liendo 예고) → 홍역·병원 → Liendo(24–33분) → Montfort(21분)·학교 화재(36분) → 심령술사·염소·앵커 → 결론.
- 결말을 맞힌 실행이다.
- 섹션 3(Liendo) 다음 섹션 4(Montfort 21분)로 **시간 순서가 역전**되고, 섹션 4는 무관한 두 꼭지를 한 섹션에 묶었다.

**논리 정합성 (대조)**

| 위치 | 문제 | 근거 |
|---|---|---|
| S2 | "At 00:10:00, … a father swinging a child at a Toronto playground" | 같은 장면을 S1이 00:01:30으로 서술했다. 같은 장면에 시각이 두 개다 |
| S2 | "**At 00:15:00**, … the third patient death in a Montreal hospital waiting room" | 캡션상 04:30이다. 15:00은 어떤 근거에도 없다(규칙 검사 `unsupported 00:15:00`). planner 섹션 설명의 범위 "(00:10:00-00:20:00)" 안의 값이다 |
| S2 | "the escalating public health emergency, centering on the measles resurgence … and its cascading consequences" → 병원 대기실 사망 | 근거는 사망 원인을 구급차 지연으로 든다. 홍역의 결과라는 인과는 근거에 없다. planner 설명 "measles outbreak and its consequences … including … a third patient death"를 따랐다 |
| S2 | "the video's central thesis: the measles outbreak is … a symptom of deeper systemic failures" | 뉴스 모음에 근거 없는 "중심 논지"를 붙였다 |
| S1, 결론 | "tripartite narrative", "a fragmented yet interconnected narrative … recurring themes of systemic failure and community resilience" | 무관한 꼭지를 하나의 서사로 묶었다 |
| S4 | "The video opens with an exterior shot of Montfort Hospital" | 10sec 캡션의 구간 시작 표현을 옮겼다 |
| 결론 | "the Rev. Eleazar Winter Memorial School", "long-standing boil water advisory since 2002" | 본문에 없던 새 사실이다. 결말 문장을 10min 0–10분 근거 [1]로 인용했다 |

#### r3

**구성과 영상 전체 서술**
- 다룬 꼭지가 가장 많다(10/12, 3분 구간 12/16). 섹션 2(10–20분)는 항공 요금·폭설·산불을 다룬 유일한 실행이다.
- 결말은 틀렸다: 결론이 "concludes with Liendo's gold medal and the community's recovery stories"라고 쓴다. 결론 checklist가 정한 결말이다.

**논리 정합성·중복 (대조)**

| 위치 | 문제 | 근거 |
|---|---|---|
| S1 | "Opening" 섹션에 Liendo의 **Doha 금메달**(33분대 근거 [4][6])과 시위 상세(05:40–06:40)를 넣음. 시위를 같은 섹션에서 두 번 서술 | 10min 0–10분 요약 [1]과 다른 시점 근거를 섞었다 |
| S1 ↔ S2 | "third patient death … 45-minute ambulance delay … investigating systemic resource shortages … hospital corridors … Kamala Harris's Gaza ceasefire appeal" 단락이 두 섹션에 거의 그대로 반복 | S1은 [1], S2는 [11](3min 03:00–06:00) 인용. 같은 사건이 다른 단위의 근거로 두 섹션에 들어왔다 |
| S2 | "At 00:10:00, the video shifts focus … to the unfolding consequences of the measles outbreak … A third patient death…" | 사건은 04:30이다. 10:00은 planner 설명의 범위 값이다. 홍역과의 인과도 r2와 같은 문제다 |
| S2 | 11:30 → 12:30 → 15:30 → **14:50 → 10:50** | 섹션 안 시간 역행 |
| S3 | "At 00:31:40, … Liendo, who wins gold … at the **Commonwealth Games** [24]" | [24](31:40, 10sec)에는 대회 이름이 없다(원문 전체 확인). Commonwealth 금메달은 다른 요약에서 2022년 장면(25–27분)으로 나온다. 두 대회를 섞었다 |
| S3 ↔ S4 | S3 "his first international gold"(Commonwealth) / S4 "Doha … Canada's first Black swimmer to win international gold" | 같은 보고서 안에서 "첫 국제 금메달"이 두 대회다(캡션 자체의 불일치를 그대로 옮김) |
| S5 | 마지막 두 단락이 앞 내용($13M 공약, 신축 학교 개교, "thematic diversity")을 다시 요약 | 섹션 안 중복 |
| S5 ↔ 결론 | S5는 심령술사·염소 꼭지가 영상에 있다고 쓰는데, 결론은 Liendo와 학교 복구로 끝난다고 씀 | 보고서 안에서 서로 맞지 않는다 |
| 결론 | "which he achieved through disciplined training and cultural perseverance" | 근거 없는 인과 평가. Liendo 문장을 [36](학교·심령술사 섹션의 참조)로 인용했다 |

---

## 3. 같은 영상 3회 비교 (대조)

| 영상 | 3회 공통 | 실행마다 다른 것 |
|---|---|---|
| `-QuCz7kxBr8` | 도입(6명, 12개 가젯, 두 팀), Dribble Specs·Dribble Stick·Straight Shooter·Flick Glove를 서술. 팀 대결 점수·최종 팀 결과는 3회 모두 서술하지 않음. 점수 불일치(0/1·1/1 … 3/16 … 15)는 r1·r2 모두 근거에서 옮김 | 다룬 범위(r2는 앞 11분, r1·r3은 25–29분까지), 결말(r1만 맞음), 중복 위치 |
| `0RxMZBLeqRI` | 면책 문구·도입 몽타주, 나치 시대 박해(21–24분), 해석 위주 서술(추상어 4.1–4.6/100단어, 9건 중 상위 3개), 결론의 새 사실(3회 모두, 내용은 다름) | 1–21분을 다룬 정도(r3만 10–15분), 반복 루프(r1·r2 섹션 5) |
| `54k2g9ddy4M` | 홍역·Montfort·Liendo·학교 화재. 뉴스 모음을 하나의 서사로 엮음 | 다룬 꼭지 수(5/8/10), 결말(r2만 맞음), 섹션 순서(r2 역전), 시각 오류 위치 |

---

## 4. 9건 종합: 발견된 문제

빈도는 9건 중 그 문제가 대조로 확인된 보고서 수다.

| 분류 | 문제 | 빈도 | 대표 사례 |
|---|---|---|---|
| A. 영상 전체 서술 | 영상의 큰 구간(10분 이상)이 빠짐 | 9/9 | `-QuCz7kxBr8` r2 앞 11분만, `0RxMZBLeqRI` r1·r2 3–21분 없음, `54k2g9ddy4M` r1 꼭지 12개 중 5개 |
| | 결말 서술이 틀림 | 4/9 | `-QuCz7kxBr8` r2·r3, `54k2g9ddy4M` r1·r3 |
| | 구간 요약의 "the video closes/opens/ends"를 본문(결론 전) 섹션에서 영상 전체처럼 씀 | 6/9 (보고서당 1–4문장) | 3min 요약의 "The video closes with … Shot Coach", "At 00:23:40, the video begins with…" |
| | 섹션 분량이 내용과 맞지 않음(32초 장면에 섹션 하나) | 1/9 | `0RxMZBLeqRI` r2 S5 |
| B. 섹션 구성 | 섹션 순서 역전 | 1/9 | `54k2g9ddy4M` r2 |
| | 섹션 안 시간 역행 | 6/9 | `0RxMZBLeqRI` r1 S5, r2 S3·S4, r3 S4, `-QuCz7kxBr8` r1 S3, r3 S5, `54k2g9ddy4M` r3 S2 |
| | 무관한 사건·다른 시점 장면을 한 섹션에 묶음 | 4/9 | `-QuCz7kxBr8` r1 S3(8분+19분), r2 S5(10분+30분), `54k2g9ddy4M` r2 S4(병원+학교 화재), r3 S1(도입에 33분대 Doha 금메달) |
| | 섹션 제목·요약 문장과 본문이 다름 | 3/9 | `0RxMZBLeqRI` r1 S5(공산 정권), r2 S3(비스마르크), r3 S3(현대 시위) |
| C. 논리 정합성 | 시각을 잘못 붙임 | 4/9 | `-QuCz7kxBr8` r1 19:30(실제 10:40), `54k2g9ddy4M` r2 15:00·r3 10:00(실제 04:30), r3 31:40 Commonwealth |
| | 인물·사건 귀속 오류 | 3/9 | `-QuCz7kxBr8` r1 농담을 다른 벌칙에, r3 "Woo!"를 다른 인물에, r2 30:30 장면을 Flick Glove 섹션에 |
| | 같은 보고서 안의 사실 불일치 | 6/9 | "AT LOSER" vs "AT 100%"(`-QuCz7kxBr8` r1·r3), 점수 0/1·1/1 → 3/16 vs 15(r1·r2), 1/2(r3), r3 결론 vs 평점 1·-3k, Commonwealth vs Doha "첫 국제 금"(`54k2g9ddy4M` r1·r3), 민족 집단 해석(`0RxMZBLeqRI` r1) |
| | 근거보다 구체적으로 단정 | 1/9 이상 | `-QuCz7kxBr8` r2 "Chris 10:85, Zach 9:51" |
| | 근거가 없는 것을 "영상에 없다"로 단정하거나 checklist 항목을 부정문으로 채움 | 2/9 | `0RxMZBLeqRI` r1 S5(7문장, 자기모순), `-QuCz7kxBr8` r3 S2·S3(윗몸일으키기는 실제로 있음) |
| | 근거 없는 인과 연결 | 2/9 | `54k2g9ddy4M` r2·r3 "홍역의 결과로서의 병원 사망", r3 "disciplined training and cultural perseverance" |
| D. 서사 | 서로 무관한 꼭지를 하나의 서사·주제로 묶음 | 3/3 (`54k2g9ddy4M`) | "from tragedy to triumph", "tripartite narrative", "central thesis" |
| | 장면에 상징·비평 의미를 부여 | 3/3 (`0RxMZBLeqRI`) | "visual metaphor for marginalization", "critique of power structures…" |
| E. 중복 | 섹션 사이 반복(같은 사건·같은 단락) | 7/9 | `-QuCz7kxBr8` r2 Dribble Stick 규칙 4회, r3 S1↔S2, `54k2g9ddy4M` r3 S1↔S2 병원 단락 |
| | 섹션 안에서 같은 해석을 바꿔 쓰며 반복 | 5/9 | `0RxMZBLeqRI` r1 S2, r2 S5(8단락 이상), r3 S2, `-QuCz7kxBr8` r3 S4, `54k2g9ddy4M` r3 S5 |
| | writer 반복 루프 → 상한에서 끊김 | 2/9 | `0RxMZBLeqRI` r1·r2 S5(같은 문장 제거 후에도 r2는 바꿔 쓴 반복이 남음) |
| F. 추상어·메타 | 추상·평가어 1.6–4.6/100단어, 메타 서술 1–17문장 | 9/9 | `0RxMZBLeqRI` 3회가 4.1–4.6으로 가장 높음 |
| | 내용 없는 상투·메타 문장 | 9/9 | "The transition … is smooth and well-prepared", "The video does not explicitly conclude this section" |
| G. 결론 섹션 | 본문에 없던 새 사실 | 4/9 | `0RxMZBLeqRI` r1·r2·r3, `54k2g9ddy4M` r2 |
| | 결론 인용이 문장 내용과 맞지 않음 | 4/9 이상 | `54k2g9ddy4M` r1(홍역 → 학교 화재 참조), r2(결말 → 0–10분 참조), r3(Liendo → [36]), `0RxMZBLeqRI` r2(박해 → 지구본 참조) |

- 장점: 인용한 근거를 그대로 옮긴 사실 서술 부분은 대체로 근거와 맞는다. 형식(섹션 상한, 결론 섹션, 인용 번호)은 9건 모두 지켰다.

---

## 5. 원인

### 5.1 확인된 원인 (원인 → 결과 경로를 코드·데이터로 확인)

| # | 원인 | 결과(§4 분류) | 근거 |
|---|---|---|---|
| C1 | planner가 10min 요약 개요만 보고 섹션을 6개 이하로 정한다. 섹션 검색은 섹션의 시간 범위로 제한되지 않는다. 그래서 계획에 없는 구간은 어떤 섹션에서도 검색될 이유가 없다 | A 구간 누락, B 무관한 장면 묶기 | 코드(planner 입력, `search_node`). 9건의 빠진 구간이 모두 outline에 계획되지 않은 구간 |
| C2 | 개요의 0–10분 10min 캡션이 2,048토큰에서 잘려 6–12분 내용을 담지 못했다(`0RxMZBLeqRI`) | A: 3회 모두 3–9분이 거의 없음 | 10min 캡션 원문(Ghaznavid·Vlad 없음). 본문에 Ghaznavid가 없고 r1 결론에만 결론 자체 검색으로 나온다 |
| C3 | 3min·10min 요약은 시각 없이 여러 사건을 한 텍스트로 합친다(WorldMM 전처리 입력에 시각이 없음). writer는 그 사건에 같은 섹션 다른 근거의 시각을 붙인다 | C 시각 오류, B 다른 시점 장면 묶기 | `gen_multiscale.py`, `-QuCz7kxBr8` r1 19:30 사례(인용 [2]=10min, 10sec 캡션 10:40) |
| C4 | 섹션마다 독립 검색이라 같은 근거가 여러 섹션에 다시 들어온다. 한 요약에 여러 사건이 섞여 있으면 writer가 섹션 주제에 맞춰 다르게 묶는다 | E 섹션 사이 반복, C 같은 사건의 두 가지 서술 | `-QuCz7kxBr8` r1 S3·S4가 같은 [20] 인용, r2 S1–S3이 같은 [1] 인용, `54k2g9ddy4M` r3 S1·S2가 같은 사건을 다른 단위 근거로 인용, `0RxMZBLeqRI` r1의 30sec 00:00 캡션이 6개 섹션 중 5개 근거에 포함 |
| C5 | 근거 캡션(특히 30sec·3min·10min)에 구간 내부의 끝·시작 표현과 해석·평가 표현이 있다. writer가 문장의 12–38%를 근거와 거의 같게 옮긴다 | A "video closes", D·F 해석·추상어 | 3min 18:00 캡션 원문과 보고서 문장 대조, 복사율(측정), `DESIGN_AND_STATUS.md` §9.17(해석 단서가 든 근거: 3min 28/29, 10min 12/12) |
| C6 | 캡션 오류·불일치가 요약 단계를 거쳐 보고서까지 전파된다. 상위 요약은 하위 캡션만 보고 만들어져 바로잡을 수단이 없다 | C 같은 보고서 안의 사실 불일치 | "GILLY → SILLY STRING AT 100%", "0/1 … 3/16 … 15", "1/2 swishes", 두 대회의 "first international gold". 모두 캡션 원문에 있다 |
| C7 | planner checklist + writer 규칙 4("근거가 요구사항을 다루지 않으면 보이지 않는다고 쓸 것") | C checklist 항목을 부정문으로 채움 | `0RxMZBLeqRI` r1 S5 부정문 7개가 checklist·설명 항목과 대응. `-QuCz7kxBr8` r3 S2의 "8/10, 7"이 checklist "e.g., 8/10, 7"과 대응 |
| C8 | 결론도 자기 검색어로 따로 검색하고 그 근거로만 인용한다. planner 결론 checklist가 결말을 미리 지정하기도 한다 | G 새 사실·인용 불일치, A 틀린 결말 | 결론 검색어·checklist(`SELF_CONSISTENCY_CAUSES.md` §2.3·§4), 규칙 검사 결과 |
| C9 | planner가 개요의 세부를 설명·checklist에 넣고 그것이 본문으로 간다 | C 근거 없는 수치 | `54k2g9ddy4M` r1 `79%`(P5) |
| C10 | planner가 섹션 설명에 붙인 10분 창 범위를 writer가 사건 시각으로 쓴다 | C 시각 오류 | `54k2g9ddy4M` r2 "At 00:15:00", r3 "At 00:10:00": 사건은 04:30, 섹션 설명은 "(00:10:00-00:20:00)", 15:00은 어떤 근거에도 없음(규칙 검사 `unsupported`) |
| C11 | planner 설명이 서로 다른 사건을 인과로 묶는다("measles outbreak and its consequences … including … a third patient death") | C 근거 없는 인과 | `54k2g9ddy4M` r2·r3 섹션 2 설명 원문. 근거는 사망 원인을 구급차 지연으로 든다 |
| C12 | planner가 개요의 창 라벨("30–40분")을 실제 길이와 상관없이 섹션 배정에 쓴다 | A 섹션 분량 불균형 | `0RxMZBLeqRI` r2·r3 섹션 4·5가 모두 "(00:30:00-00:40:00)". 그 창의 실제 내용은 30:00–30:32(10min 캡션 284단어) |
| C13 | 반복 제거가 글자가 같은 문장만 지운다 | E 바꿔 쓴 루프가 보고서에 남음 | `0RxMZBLeqRI` r2 S5. 같은 문장 39개를 제거한 뒤에도 같은 내용 단락 8개 이상이 남음 |

C1–C13은 네 층으로 묶인다.

| 층 | 원인 |
|---|---|
| 입력 자료 | C2, C3, C5, C6 |
| planning | C1, C7, C9, C10, C11, C12 (C8의 결말 지정 포함) |
| 섹션 단위 독립 검색·작성 | C4, C8 |
| 후처리 | C13 |

### 5.2 가능성이 있지만 확인하지 못한 원인 (구분해서 둠)

| # | 현상 | 가능한 원인 | 확인하지 못한 이유 / 확인 방법 |
|---|---|---|---|
| H1 | 근거가 적은 섹션에서 같은 해석을 바꿔 쓰며 늘림(`0RxMZBLeqRI` r1 S2, r2 S5, r3 S2) | 템플릿 길이 지시("Typically 250–700 words") + 근거 부족 + 해석형 checklist(예: "Recognize the visual contrast between exclusion and cultural celebration") | 길이 지시·checklist를 바꾼 비교 실행이 없다(GPU 필요) |
| H2 | 뉴스 모음 영상에 하나의 서사를 덧씌움(`54k2g9ddy4M` 3회) | 질의 문구("key events in the order they occur, and how the video concludes")가 하나의 이야기를 전제하고, planner 설명·결론 checklist가 주제로 묶는다. 결론 템플릿("synthesize the main points")도 기여할 수 있다 | 영상 유형별 질의·템플릿 비교가 없다 |
| H3 | 섹션 안 시간 역행 | writer가 근거의 관련도 순서(L1 필터 순서)로 단락을 쓴다 | 근거를 시간순으로 바꾼 비교가 없다 |
| H4 | writer 반복 루프가 "does not show…" 같은 같은 틀의 문장에서 생김 | checklist 항목마다 같은 틀의 부정문을 만들다 같은 문장으로 수렴 | 같은 프롬프트를 여러 번 생성하는 실험이 필요(`SELF_CONSISTENCY_CAUSES.md` E1) |
| H5 | 섹션 사이 반복이 C0(앞 섹션 요약 전달)에도 남음 | C0는 앞 섹션의 단락 첫 문장만 넘기므로 세부 사실(점수, 규칙)의 반복을 막기 어렵다. 규칙 6("한 문장 이내")이 지켜지지 않았다 | 앞 섹션 근거를 다음 섹션에서 빼는 등의 비교가 필요 |
| H6 | 가젯·꼭지를 일부만 다루고, 팀 점수 같은 영상 전체에 걸친 상태를 서술하지 않음 | 섹션 상한 6과 planner의 섹션 단위 선택(샘플링). 섹션별 근거가 국소적이다. 캡션 자체에 팀 점수가 부족할 수도 있다 | 상한·지시를 바꾼 비교가 필요. 영상을 보지 않아 팀 점수가 화면에 있는지 확인하지 못했다 |
| H7 | 상투·메타 문장, 근거와 거리가 먼 해석·평가어(예: `0RxMZBLeqRI` r1의 60문장 중 40) | 근거가 부족할 때 길이를 채우는 8B 모델의 서술 습관, "expert writer" 역할 지시 | 문자열 유사도만으로는 "근거에 없음"을 확정할 수 없다(바꿔 쓴 근거 표현일 수 있음). 문장 단위 표본 대조가 필요 |

---

## 6. 정리

- 9건은 형식(섹션, 인용, 결론)을 지키고, 인용한 근거를 그대로 옮긴 사실 서술은 대체로 근거와 맞는다. 그러나 보고서 수준에서는 다음 문제가 모든 영상과 모든 실행에 나타났다.
  - 영상 전체 서술 실패: 큰 구간 누락 9/9, 결말 오류 4/9
  - 같은 보고서 안의 사실·시간·귀속 불일치
  - 섹션 사이·섹션 안의 반복
  - 근거 캡션에서 온 해석·평가 표현과 구간 내부 표현
  - 결론의 새 사실과 인용 불일치
- 확인된 원인(C1–C13)은 입력 자료, planning, 섹션 단위 독립 검색·작성, 후처리의 네 층에 걸쳐 있다.
  - C2·C10·C12처럼 데이터와 planner 출력으로 경로가 분명한 것이 있다.
  - H1–H7은 비교 실행(GPU)으로만 확인할 수 있다.
- 같은 조건 3회의 구성이 크게 달라(`SELF_CONSISTENCY_ANALYSIS.md`) 세부 사례는 실행마다 다르다. 빈도는 9건 표본의 값이다.
