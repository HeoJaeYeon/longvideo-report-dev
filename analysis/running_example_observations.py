"""
Hand-written observations for the running-example documents (checked against evidence, captions, logs and code;
see REPORT_TEXT_REVIEW.md, SELF_CONSISTENCY_CAUSES.md, REPORT_PIPELINE.md). Inserted at the `<!-- OBS:<key> -->`
markers that analysis/build_running_example.py leaves. Labels: [확인] / [부분 확인] / [가설] / [대조] / [측정].
Usage: python analysis/running_example_observations.py   (after build_running_example.py for all three videos)
"""
import os

RF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))


def block(title, items):
    return "\n".join([f"> **관찰 — {title}**", ">"] + [f"> - {x}" for x in items])


OBS = {
"-QuCz7kxBr8": {
"planner": block("planner", [
    "[확인] 6개 섹션 모두 설명에 시간 범위가 없고, 가젯·게임 단위로 나뉘었다(§4.2 마지막 열).",
    "[확인] S3은 08:00의 Flick Glove와 18–20분의 Shot Coach를, S4는 18–25분의 여러 게임을 한 섹션에 묶었다. 서로 다른 시점의 사건이 한 섹션에 들어간다.",
    "[확인] 10:30–18:00(\"MOST DRIBBLES IN 15 SECONDS\" 챌린지 등)과 25:30–36:00(29:00 \"FIRST TO 3 WINS\" 최종 게임 규칙, 패드 수비 훈련)을 다루는 섹션이 계획되지 않았다. 이 구간을 인용한 섹션도 없다(§7).",
    "[확인] 개요의 둘째 블록은 라벨이 10–20분이지만 실제로는 12–21분 내용이다(§2.2). planner는 라벨만 본다.",
    "[부분 확인] S5 설명에 최종 점수(3-1)와 엔드 스크린이 들어 있어 결말을 다루는 섹션이 계획됐고, 이 보고서의 결말 서술은 맞았다. 9건 중 결말을 맞힌 5건은 모두 planner가 결말 구간을 섹션이나 checklist에 넣은 경우였다(표본 9건, 인과 미확정).",
]),
"s1": block("섹션 1", [
    "[확인] 텍스트 근거는 00:00–03:00에 모여 있다(10min 1개 제외). 그런데 이미지 3장은 00:28:45–00:34:45다. image 검색은 image query 하나로 영상 전체에서 따로 찾고, 텍스트 근거 시간과 연결하는 장치가 없다(코드). 그래서 Figure 1(34:45, 패드 수비 훈련 장면)이 도입부의 \"HYPE 로고\" 문장에 붙었다.",
    "[대조] 같은 문장의 [4]는 semantic triple `(player, can gesture and talk to, another player)`로, 문장 내용을 뒷받침하지 않는다. 숫자·따옴표가 없어 규칙 검사로는 잡히지 않는다.",
    "[확인] writer가 img1을 금지 형식 `[citation:img1]`로 써서 후처리가 `(Figure 1)`과 그림 블록으로 바꿨다.",
    "[대조] 첫 문장(6명 소개)에는 인용이 없다.",
]),
"s2": block("섹션 2", [
    "[확인] \"initially making one shot (0/1), then missing several … 0/3 … pushing the tally to 3/16 … approaches 15 successful shots\"는 서로 맞지 않는다. 근거 10min 요약의 문장 그대로라, 캡션 자체의 불일치를 옮긴 것이다.",
    "[대조] 02:30–07:30 근거(그 밖에 10min 00:00–10:00 요약 1개)로 Dribble Stick → Straight Shooter Strap → 팔벌려뛰기 벌칙(10sec 07:20) 순서를 시간순으로 서술했다. 6개 섹션 중 흐름이 가장 분명한 섹션이다.",
]),
"s3": block("섹션 3", [
    "[확인] \"At 00:19:30, the man in the black hoodie performs sit-ups … 'CASH LOST'\": 10sec 캡션상 이 장면은 **10:40–11:10**이다. 문장이 인용한 [2]는 시각이 없는 10min 요약이고, 19:30은 같은 섹션의 다른 근거(Shot Coach, 30sec 19:30–20:00)의 시각이다. 규칙 검사가 `miscited 00:19:30`으로 표시했다.",
    "[대조] 윗몸일으키기 벌칙 문단에 S2의 팔벌려뛰기 장면 농담(\"bouncing titties\", \"Bro, I'm wearing a big shirt\")을 다시 붙였다. 두 벌칙 장면을 섞었다.",
    "[확인] \"The video closes with a close-up of the Shot Coach device…\"는 근거 3min 캡션(18:00–21:00)이 **자기 구간의 끝**을 요약한 문장을 옮긴 것이다. 결말 검사가 `ending_early`로 표시했다.",
    "[대조] 세 명의 동시 슛을 \"The Shot Coach is also used in a synchronized shooting drill. At 00:18:00…\"로 썼다. S4는 같은 사건을 Silly String 게임으로 서술한다.",
    "[측정] 근거 범위가 00:00–21:00이다(08:00 Flick Glove, 10:40 벌칙, 18–20분 Shot Coach). 섹션 안에서 시각이 19:30 → 18:00으로 역행한다. 마지막 두 단락은 앞 내용을 다시 요약한다.",
]),
"s4": block("섹션 4", [
    "[확인] 근거 3min 캡션(18:00–21:00)은 Event 1–5로 게임 규칙, 동시 슛, Shot Coach 훈련, 손목 보조 장치, 화면 문구를 한 텍스트에 묶어 요약했다. 이 섹션은 그 문장들을 거의 그대로 옮겼다. 예: \"reinforcing the structured, tech-assisted training environment\", \"underscoring its role in enhancing shooting accuracy and enabling fun, structured practice\".",
    "[확인] 같은 게임 규칙이 \"AT LOSER\"(10sec·30sec 18:30)와 \"AT 100%\"(00:18:29) 두 가지로 나온다. 오류가 전파된 경로: 10sec 18:20 캡션의 화면 문구 오독 \"GILLY STRING AT 100%\" → 30sec 요약의 \"performance claim\" 해석 → 3min 요약의 \"SILLY STRING AT 100%, tying the product's performance claim to the game's outcome\" → 보고서. 규칙 검사는 이 문구가 인용한 근거가 아니라 다른 근거(txt1)에 있다며 `miscited`로 표시했다(문구 자체의 오류는 검사 대상이 아님).",
    "[대조] Shot Coach 훈련 단락(\"SHOOT FROM HALF COURT 5 TIMES WITH SHOT COACH\", 손목 밴드 조정)이 S3([19])과 S4([20])에 거의 같게 반복된다. 섹션마다 독립 검색이라 같은 내용의 근거가 두 섹션에 들어왔다.",
    "[대조] \"a black training device, likely the harness\"는 근거에 없는 추정이다. \"a player can be defended by another player\"는 semantic triple을 옮긴 것이라 정보가 없다. \"The video's final moments emphasize…\"는 18–25분 섹션의 문장이다.",
]),
"s5": block("섹션 5", [
    "[확인] S4의 마지막 근거(25:00) 다음 이 섹션이 36:30으로 넘어간다. 그 사이의 29:00 최종 게임 규칙과 27–36분 패드 수비 훈련은 어느 섹션에도 없다.",
    "[대조] 36:30–37:37 근거로 쓴 결말(\"2-1\" → \"3-1\", \"ZAK JESSE & KRIS WIN\", 8번 선수, 엔드 스크린)이 10sec 캡션과 맞는다. 다만 \"The video concludes with a static end screen…\" 문장은 인용이 없어 `ending_unverifiable`로 표시됐다.",
    "[대조] \"ZAK JESSE & KRIS\"와 S1의 \"Chris, Zach\"가 같은 인물인지 설명하지 않는다. 화면 문구와 다른 캡션의 표기가 다르고, 영상을 보지 않아 확인하지 못했다.",
]),
"s6": block("섹션 6 (결론)", [
    "[확인] 결론의 검색어(\"final score displayed as 3-1…\", \"video ends with blue and white static end screen\")가 앞 섹션 5를 따라가 끝부분 근거를 얻었다. 결론 검색어는 앞 섹션 요약(C0)을 입력으로 만들어진다(코드).",
    "[확인] \"The video ends at 00:37:37 with a static screen…\"은 맞는 내용이다. 그러나 인용한 근거(37:00–37:30, 37:20–37:30, semantic)의 구간 밖이라 `miscited 00:37:37`로 표시됐다. 같은 결말을 \"The video concludes with…\"로 한 번 더 쓴다.",
    "[대조] 가젯 4개(SKLZ Dribble Stick, Straight Shooter Strap, Flick Glove, Shot Coach)를 요약하지만 결론 근거에는 이 가젯들의 근거가 없다. 결론은 자기 검색 근거로만 인용할 수 있다(Deep-Reporter 구조).",
]),
"summary": "\n".join([
    "## 7. 단계별 문제점·한계 요약 (이 영상)",
    "",
    "| 단계 | 이 영상에서 확인된 동작·문제 | 표시 |",
    "|---|---|---|",
    "| 입력 자료 (WorldMM 캡션) | 10min 개요 블록 라벨과 실제 구간이 어긋남(0–12, 12–21분). 3min 캡션의 구간 끝 표현(\"The video closes with…\")과 해석어. 10sec 캡션의 화면 문구 오독(GILLY) → 상위 요약에서 해석이 덧붙음. 10min 요약 안의 점수 불일치 | [확인] |",
    "| planner | 시간 범위 없이 가젯·게임 단위로 섹션을 정함. 서로 다른 시점의 사건을 한 섹션에 묶음(S3·S4). 10:30–18:00, 25:30–36:00을 계획하지 않음. 결말 구간(S5)은 계획됨 | [확인] |",
    "| query 생성 | checklist 문구를 거의 그대로 검색어로 씀(예: S5 \"Zak Jesse and Kris win 3-1 in final scoring segment\"). 결론 검색어는 앞 섹션을 따라감 | [확인] |",
    "| 검색 | 섹션마다 독립 검색이라 같은 3min 근거(18:00–21:00)가 S3·S4에 들어옴. 이미지는 텍스트 근거와 1,135–1,555초 떨어짐(S1). L1 필터의 후보·응답은 기록되지 않음 | [확인] |",
    "| writer | 다른 근거의 시각을 붙임(19:30), 장면의 농담을 섞음, 구간 끝 표현을 영상 끝처럼 옮김, 근거 문장 복사(문장의 28%가 근거와 거의 같음) | [확인]·[측정] |",
    "| 후처리·검증 | 규칙 검사 miscited 5·uncited 12, 결말 검사 ending_early 2·unverifiable 3, 이미지 형식 변환 1. 경고만 남고 상태는 `passed`. 의미 수준의 오류(장면 섞기, 동시 슛의 두 가지 서술)는 검사 대상이 아님 | [확인] |",
    "| 생성 방식 | 같은 조건 r2는 앞 11분만 다루고 결말이 틀렸고, r3은 결말이 불완전했다(`REPORT_TEXT_REVIEW.md` §2.1) | [확인] |",
]),
},
"0RxMZBLeqRI": {
"planner": block("planner", [
    "[확인] 개요의 0–10분 블록이 2,048토큰에서 잘려, 3–6분 내용을 쓰던 중 끝난다. 이 블록에 묶인 6–12분 내용(Ghaznavid 제국 6:00, Vlad Zepes 9:00)이 개요에 없다. 10–20분 블록도 2,048토큰에서 끊겼다(§2.2).",
    "[확인] 섹션 1–4가 모두 0–10분 블록의 앞부분 세부로 계획됐다: 면책 문구·몽타주, 세피아 사진과 퍼레이드, 실험복 인물과 \"UNWANTED\", 13세기 지도와 \"VS\" 그래픽. 10–21분을 다루는 섹션이 없고, 섹션 설명에 시간 범위도 없다.",
    "[확인] S5 설명이 \"persecution under Nazi **and communist** regimes … post-war institutional erasure\"를 지정했다. 이후 검색 근거 12개에는 공산 정권 박해를 서술한 캡션이 없다(§5.5).",
    "[확인] S2 checklist의 \"Recognize the visual contrast between exclusion and cultural celebration\"처럼 해석형 항목이 있다.",
    "[확인] 결론 checklist에 \"Confirm that the video concludes with a global perspective and credits\"가 있다. 이 항목이 결론 검색어로 이어졌다(§5.6).",
]),
"s1": block("섹션 1", [
    "[측정] 12문장 중 7문장이 txt1–txt4 네 개를 함께 인용한다. txt1–4는 모두 00:00에서 시작하는 30sec·10sec·3min·10min 캡션으로, 같은 구간을 다른 세밀도로 요약한 근거다.",
    "[확인] \"…the final shot of the video's opening montage…\"를 결말 검사가 `ending_early`로 잡은 것은 오탐(소유격)이다. 2026-10-26에 검사 정규식을 고쳤다(GPU 실행 확인 전).",
    "[대조] \"a symbolic gesture possibly representing marginalization\", \"underscoring the video's thematic focus on political manipulation\" 같은 해석이 사실 서술과 섞여 있다.",
]),
"s2": block("섹션 2", [
    "[측정] 근거 12개 중 3개만 인용하고 535단어를 썼다. 7개 단락 중 셋째 단락부터는 인용이 없고, 같은 주장(\"배제 대 축하의 시각적 대비가 회복력·문화적 연속성을 보여 준다\")을 표현만 바꿔 되풀이한다.",
    "[확인] 이 섹션 checklist에 해석형 항목(\"Recognize the visual contrast between exclusion and cultural celebration\")이 있다. [가설] 근거가 적은 상태에서 이 항목과 길이 지시(\"Typically 250-700 words\")가 함께 작용해 같은 해석을 늘렸을 수 있다. 길이 지시를 바꾼 비교가 없다.",
    "[확인] 규칙 검사 `unsupported`: 따옴표 문구 \"very little [public] knowledge\". writer가 인용 문구 안에 `[public]`을 끼워 넣어 근거 문구와 달라졌다.",
    "[측정] 30sec 00:00–00:30 캡션은 6개 섹션 중 5개(S1·S2·S3·S4·S6)의 근거에 들어 있다. 섹션마다 독립적으로 검색하기 때문이다.",
]),
"s3": block("섹션 3", [
    "[확인] 이 섹션의 해석 표현(symbolizing, suggesting, coercion, allegory, critique, commodification, exploitation)은 모두 이 섹션의 근거 캡션에도 들어 있다. writer가 근거 캡션의 해석을 옮긴 것이다. WorldMM 요약 프롬프트는 해석을 금지하지만 요약 캡션에 해석이 들어 있다(`DESIGN_AND_STATUS.md` §9.17).",
    "[측정] 근거는 00:30–01:00(실험복 인물, \"UNWANTED\", Minecraft 장면)에 모여 있다(인용 근거 중앙값 00:50).",
]),
"s4": block("섹션 4", [
    "[대조] \"positions Roma **not as a distinct ethnic group** but as a product of historical misreading\"은 S1이 인용한 면책 문구(\"Gypsy\"를 민족 집단의 이름으로 쓴다)와 어긋나는 해석이다. 인용 [4]는 시각 없는 10min 요약이다.",
    "[측정] \"not 'invented' but misclassified\"가 2번, \"historical misreading\"이 2번 나온다.",
    "[대조] 01:00–01:30 근거(13세기 지도, Seljuk vs Byzantine 그래픽, §2.1 예시의 10sec 01:10 캡션)의 사실 서술은 근거와 맞는다.",
]),
"s5": block("섹션 5", [
    "[확인] writer 출력이 서버 상한 3,072토큰에서 끊겼다(133.9초, `finish=length`). 마지막에 \"The video does not show any footage of Roma persecution under communist regimes…\"가 38번 반복됐다. 후처리가 같은 문장 37개를 지워 1,778 → 927단어가 됐지만, 마지막 문장은 \"…under\"에서 끝난다.",
    "[확인] \"does not show\" 문장 7개(마지막 1개는 끊긴 문장)가 이 섹션 설명·checklist의 항목(communist regimes, Gestapo mugshots, 500,000–1,500,000, 1942 Auschwitz, post-war erasure)을 하나씩 짚는다. 그중 \"…does not show any text overlay stating 500,000–1,500,000 deaths **beyond the one shown at 00:24:00**\"처럼 앞에서 보여 준 것을 부정하는 자기모순 문장이 있다. writer 규칙 4(\"근거가 요구사항을 다루지 않으면 보이지 않는다고 쓸 것\")와 checklist가 결합한 결과다.",
    "[확인] 섹션 안 시각이 21:00 → 22:00 → 23:00 → 24:00 → 23:20 → 23:40으로 역행하고, Auschwitz 장면(1942, 줄무늬 수용복, Zyklon B)을 23:00 단락과 23:20 단락에서 두 번 서술한다.",
    "[확인] \"At 00:23:40, the video begins with a person in a dark hooded garment…\"는 10sec 캡션의 \"The video begins with\"(그 10초의 시작)를 옮긴 것이다. 결말·시작 검사가 `opening_unverifiable`로 표시했다.",
]),
"s6": block("섹션 6 (결론)", [
    "[확인] 결론에 Ghaznavid Empire, \"I am also a Roma\" 집회, 위성 안테나 건물 앞 소년, 애니메이션 캐릭터가 나온다. 모두 본문 섹션 1–5에 없던 사실이다. 결론의 근거 목록(txt8 = 3min 06:00–09:00 등)에서 온 것으로, 결론은 자기 검색 근거로 쓴다.",
    "[확인] 결론 검색어 \"video concludes with global perspective and credits\"는 planner 결론 checklist에서 왔다. 결말 서술(지구본, 암전, 30:08 크레딧)이 캡션과 맞는다. 다만 결말 문장은 인용이 없어 `ending_unverifiable`이다.",
    "[대조] \"…bureaucratic 'Zigeuner' labels … [3][3]\": writer가 같은 근거를 `[citation:txt5][citation:txt5]`로 두 번 연달아 인용했다.",
]),
"summary": "\n".join([
    "## 7. 단계별 문제점·한계 요약 (이 영상)",
    "",
    "| 단계 | 이 영상에서 확인된 동작·문제 | 표시 |",
    "|---|---|---|",
    "| 입력 자료 (WorldMM 캡션) | 10min 개요 블록 0–10분·10–20분이 2,048토큰에서 잘림 → 6–12분 내용이 개요에 없음. 요약 캡션에 해석 표현이 많음. 30sec 캡션 다수가 \"The video opens with…\"로 시작 | [확인] |",
    "| planner | 본문 섹션 5개 중 4개를 영상 첫 약 1.5분 세부로 계획. 10–21분 미계획. 근거가 없는 주제(공산 정권) 지정. 해석형 checklist. 결론 checklist에 결말을 넣음(이번에는 맞음) | [확인] |",
    "| query 생성 | checklist 문구를 검색어로 옮김(예: S5 \"text overlay states 500,000–1,500,000 Roma deaths\") | [확인] |",
    "| 검색 | 같은 30sec 00:00 캡션이 5개 섹션 근거에 들어감. 세밀도만 다른 같은 구간 요약(txt1–4)이 함께 검색됨 | [측정] |",
    "| writer | 해석 표현 옮김·추가, 근거가 적은 섹션에서 같은 주장 반복(S2), checklist 항목을 \"does not show\"로 채움(S5), 반복 루프로 상한에서 끊김(S5) | [확인]·[측정] |",
    "| 후처리·검증 | 같은 문장 37개 제거, \"문장 중간 끝\" 경고. 결말 검사 오탐 1(2026-10-26 수정). unsupported 2·uncited 13. 상태 `passed` | [확인] |",
    "| 생성 방식 | 같은 조건 r2도 같은 섹션 5에서 상한에 걸려 끊겼다. r3은 10–15분을 다뤘다(`REPORT_TEXT_REVIEW.md` §2.2) | [확인] |",
]),
},
"54k2g9ddy4M": {
"planner": block("planner", [
    "[확인] 본문 섹션 5개에 개요의 10분 창을 하나씩 \"(00:00:00-00:10:00)\" 형태로 배정했다(§4.2 마지막 열).",
    "[확인] S2 \"(00:10:00-00:20:00)\" 설명의 내용(미국 홍역, 몬트리올 병원 사망)은 개요 0–10분 블록에 있는 내용이다. 개요 10–20분 블록(실제 12–21분: 항공 요금, 캘리포니아 폭설, 폭풍·산불)을 다루는 섹션은 계획되지 않았다.",
    "[확인] S5 \"(00:40:00-00:50:00)\"의 학교 화재는 3min 캡션 기준 36:00–42:00에 있다(개요의 \"30–40분\" 블록은 실제 30–42분 내용). 42분 이후의 반려동물 심령술사·염소·마지막 앵커 장면을 다루는 섹션이 없다.",
    "[확인] S1 checklist의 \"current vaccination levels at 79%\"는 개요 문구(\"79% of seven-year-olds vaccinated by 2021\")에서 왔다(§5.1).",
    "[확인] 결론 checklist \"State that the video concludes with community recovery and athletic legacy as its final themes\"가 실제 결말과 다른 결말을 미리 지정했다(§5.6).",
]),
"s1": block("섹션 1", [
    "[확인] \"…current vaccination levels stand at 79% [citation:txt1]\": 79는 이 섹션 근거 어디에도 없어 규칙 검사가 `unsupported 79`로 표시했다. planner checklist에서 온 수치다(P5).",
    "[대조] \"Within the first minute, … Joshua Liendo\"는 30sec 00:30–01:00 근거(예고 장면)와 맞다.",
    "[측정] 근거는 00:30–02:50이다. 개요 0–10분 블록에 있는 시위(6분대)와 트럼프 여론조사(9분대)는 이 섹션에서 다루지 않았다.",
]),
"s2": block("섹션 2", [
    "[측정] 근거가 03:00–05:00이다(미국 홍역, 퀘벡 병원 사망). planner 라벨(10–20분)과 관계없는 구간이다.",
    "[확인] 근거 3min 캡션(03:00–06:00)이 \"Measles Outbreak Alert Across U.S. and Canada\" 제목 아래 미국 홍역과 퀘벡 병원 대기실 사망을 한 요약에 담고 있다(§2.1 예시 표). 섹션 제목 \"Unfolding Public Health Crisis: Measles Outbreak, Hospital Tragedy…\"가 이 둘을 하나의 위기로 묶었다. 근거는 사망 원인을 구급차 지연으로 든다.",
    "[측정] \"Footage shows hospital corridors, triage areas, and paramedics preparing ambulances…\"와 \"Visuals of hospital corridors and paramedics preparing ambulances are repeatedly shown…\"이 같은 섹션에서 반복된다(문자열 유사도 0.67).",
    "[대조] \"reinforcing the video's narrative of intersecting national and global crises\", \"the video's central theme: the fragility of public health systems\"는 근거가 진술하지 않는 해석이다.",
]),
"s3": block("섹션 3", [
    "[확인] Liendo 금메달 문장들이 txt8(10min 10:00–20:00, 항공 요금 꼭지 요약)과 txt9(semantic `(document, issued by, Montfort Hospital)`)를 인용한다. 문장 내용과 다른 근거다. 숫자·따옴표가 없어 규칙 검사로 잡히지 않는다.",
    "[확인] \"The video closes with Liendo's legacy firmly anchored…\": 20–30분 근거의 섹션에서 영상 결말을 단정했다. 결말 검사가 `ending_early`로 표시했다.",
    "[대조] \"The narrative arc moves from loss to performance, from chaos to clarity, and ultimately, from tragedy to triumph\", \"The emotional weight of the hospital error is balanced by Liendo's triumph\"는 서로 무관한 뉴스 꼭지를 하나의 서사로 엮은 해석이다. 근거에 이런 연결은 없다.",
    "[대조] 오디션 셀프테이프 꼭지(24분대)는 한 문장으로만 지나간다(근거 [14][18]).",
]),
"s4": block("섹션 4", [
    "[측정] \"hasn't revisited/returned since 2018\"이 2번, \"swims into the history books\"가 이 섹션에서 3번 나온다(S3 포함 4번).",
    "[확인] 규칙 검사 `miscited 00:31:30`: \"At 00:31:30, Liendo reflects…\"의 시각이 인용 근거(txt7) 구간 밖이고 다른 근거에 있다.",
]),
"s5": block("섹션 5", [
    "[대조] 36:00–42:00 근거(학교 화재, 1,300만 달러 공약, Pikangikum·Wapekeka 신축 학교)로 쓴 사실 서술은 근거와 대체로 맞는다.",
    "[확인] 42분 이후 꼭지(심령술사·염소·마지막 앵커·공항·CBC 로고)를 다루지 않았다. planner가 학교 화재를 마지막 창에 배정했기 때문이다(§4 관찰).",
]),
"s6": block("섹션 6 (결론)", [
    "[확인] 결론 첫 문장 \"…ultimately concluding with themes of community recovery and athletic legacy\"는 planner 결론 checklist를 그대로 따른 것이다. 실제 결말(10sec 캡션: 44:50 앵커 → 공항 → CBC 로고 검은 화면)과 다르다. 결말 검사가 `ending_early`(인용 근거 끝 40:00)로 표시했다.",
    "[확인] 결론 검색어(\"video concludes with community recovery after school fire\" 등)가 앞 섹션을 따라가서, 결론 근거에 40분 이후 근거가 없다.",
    "[확인] \"…a measles outbreak in the United States with 41 confirmed cases and a third patient death in a Montreal hospital … [32][33]\": [32]는 30–40분 10min 요약, [33]은 36–39분 3min 요약으로 홍역·병원 내용이 아니다. 규칙 검사 `unsupported 41`. 결론은 앞 섹션의 근거를 갖지 않는다.",
    "[대조] 결론의 \"Canada's first Black swimmer to win international gold … at the **Doha World Championships**\"와 S3의 \"wins gold … at the **Commonwealth Games**\"가 맞춰지지 않았다. 캡션 자체가 두 대회를 모두 \"first international gold\"라고 쓴다(3min 27:00, 33:00).",
]),
"summary": "\n".join([
    "## 7. 단계별 문제점·한계 요약 (이 영상)",
    "",
    "| 단계 | 이 영상에서 확인된 동작·문제 | 표시 |",
    "|---|---|---|",
    "| 입력 자료 (WorldMM 캡션) | 10min 블록 라벨과 실제 구간 어긋남. 3min 요약이 서로 다른 꼭지(홍역, 병원 사망)를 한 제목 아래 묶음. 캡션끼리 \"first international gold\"가 두 대회 | [확인] |",
    "| planner | 10분 창마다 섹션 1개를 배정하고 범위 표기. 라벨과 맞지 않는 내용 배정(S2). 10–21분·42분 이후 꼭지 미계획. checklist에 개요 수치(79%)와 틀린 결말을 넣음 | [확인] |",
    "| query 생성 | checklist 문구를 그대로 검색어로(예: \"U.S. measles outbreak with 41 cases reported in 16 states centered at Manatee Bay Elementary\"). 결론 검색어가 앞 섹션을 따라감 | [확인] |",
    "| 검색 | Liendo 섹션에 항공 요금 10min 요약이 근거로 들어옴(L1 필터가 선택). 결론 근거에 40분 이후 근거 없음 | [확인] |",
    "| writer | 무관한 근거를 인용(S3), 구간 끝 표현을 영상 끝처럼 씀, 무관한 꼭지를 하나의 서사로 엮음, checklist 수치·결말을 그대로 씀 | [확인]·[대조] |",
    "| 후처리·검증 | 규칙 검사 unsupported 2(79, 41)·miscited 1·uncited 4, 결말 검사 ending_early 2, 결론 341단어 경고. 상태 `passed`. 무관한 근거 인용과 덧씌운 서사는 검사 대상이 아님 | [확인] |",
    "| 생성 방식 | 같은 조건 r2는 결말을 맞혔지만 섹션 순서가 역전됐고, r3은 꼭지를 가장 많이(10/12) 다뤘지만 결말이 틀렸다(`REPORT_TEXT_REVIEW.md` §2.3) | [확인] |",
]),
},
}


def main():
    for vid, obs in OBS.items():
        p = os.path.join(RF, "running_example", f"RUNNING_EXAMPLE_{vid}.md")
        s = open(p, encoding="utf-8").read()
        for key, text in obs.items():
            marker = f"<!-- OBS:{key} -->"
            assert s.count(marker) == 1, (vid, key)
            s = s.replace(marker, text)
        assert "<!-- OBS:" not in s
        open(p, "w", encoding="utf-8").write(s)
        print("filled", p)


if __name__ == "__main__":
    main()
