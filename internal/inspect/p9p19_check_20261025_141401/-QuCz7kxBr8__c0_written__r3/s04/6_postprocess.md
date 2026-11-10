# Section 4 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 753 words → after removal 753 words

## 2. Start/end claim check (`boundary_claims`)

- ending_early: The video closes with a close-up of the Shot Coach device, underscoring its role in enhancing shooting accuracy and enabling fun, structured practice [citation:txt1][citation:txt5]. (cited [1, 5], latest cited end 00:21:00)
- ending_early: The video closes with a close-up of the Shot Coach device, reinforcing its role as a key tool in the structured, tech-assisted shooting drill [citation:txt3][citation:txt5]. (cited [3, 5], latest cited end 00:20:00)
- ending_early: The video concludes with a close-up of the Shot Coach device, underscoring its role in the training drill and its performance claim [citation:txt1][citation:txt5]. (cited [1, 5], latest cited end 00:21:00)

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 24, "cited_sentences": 6, "checked_tokens": 11, "unsupported": 0, "miscited": 0, "uncited_claims": 0, "absence_statements": 0}`

- no findings

## 4. Citation conversion stats

- `{"text_citations": 54, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 0, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 6 of 12

## 5. Image-text time alignment

- no cited image

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Synchronized Shooting Challenge and Shot Coach Training Drill

At 00:18:00, three men gather on an outdoor basketball court under a clear blue sky to begin a playful shooting challenge governed by the rule: “FIRST MADE SHOT SHOOTS SILLY STRING AT LOSER.” The man in the blue jersey (No. 2) explains the rules while the others prepare, holding basketballs and standing in position [citation:txt1][citation:txt2][citation:txt7]. A product demonstration follows, showing three black basketball shooting aids with an overlay reading “Pack of 3 Basketball Shooting Aid,” reinforcing the product’s purpose in enhancing shooting accuracy and enabling fun, competitive play [citation:txt1][citation:txt2][citation:txt4].

As the countdown from three to one flashes on screen, all three men jump and shoot simultaneously — each ball arcs perfectly into the basket, triggering the next phase of the game [citation:txt1][citation:txt2][citation:txt7]. The man in the blue jersey is declared the winner via on-screen text and celebrates briefly before congratulating the man in the black hoodie and white cap [citation:txt1][citation:txt7]. The scene, set in a sunny backyard with a hoop, trampoline, and landscaping, emphasizes camaraderie and lighthearted competition [citation:txt1][citation:txt2][citation:txt7]. A text overlay at 00:18:29 declares: “FIRST MADE SHOT SHOOTS SILLY STRING AT 100%,” tying the product’s performance claim to the game’s outcome [citation:txt1][citation:txt4]. The video closes with a close-up of the Shot Coach device, underscoring its role in enhancing shooting accuracy and enabling fun, structured practice [citation:txt1][citation:txt5].

Following the game, a basketball coach in a black hoodie and white cap uses an orange “SHOT COACH” training device to guide two young players through a drill: “SHOOT FROM HALF COURT 5 TIMES WITH SHOT COACH.” He adjusts a wristband on one player while explaining precision and repetition, with a scoreboard graphic visible and a third man in a blue jersey observing [citation:txt3][citation:txt7]. The coach demonstrates a hand-restraint device with orange straps, securing it on his own wrist while two observers watch, then walks to the free-throw line to prepare to shoot [citation:txt1][citation:txt2]. Multiple shots follow, showing different players attempting shots while being observed, reinforcing the focus on technique and consistency [citation:txt1][citation:txt2]. The coach holds a clipboard and gestures as he explains the drill, emphasizing precision and repetition through the Shot Coach system [citation:txt3]. The video closes with a close-up of the Shot Coach device, reinforcing its role as a key tool in the structured, tech-assisted shooting drill [citation:txt3][citation:txt5].

The winner of the synchronized shooting challenge is the man in the blue jersey, who is declared the victor via on-screen text after all three players successfully make their shots simultaneously [citation:txt1][citation:txt7]. The “FIRST MADE SHOT SHOOTS SILLY STRING AT LOSER” rule is applied, and the winner is shown celebrating before congratulating the man in the black hoodie and white cap [citation:txt1][citation:txt7]. The forfeit outcome — shooting silly string at the loser — is implied by the product claim overlay at 00:18:29, which states “FIRST MADE SHOT SHOOTS SILLY STRING AT 100%,” though the actual act of shooting silly string is not shown in the retrieved evidence [citation:txt1][citation:txt4]. The video does not show the forfeit being performed, but the rule’s structure and the product’s performance claim are clearly demonstrated [citation:txt1][citation:txt2].

The Shot Coach device is demonstrated and used in a structured training environment, guiding young players through a half-court shooting drill and also being used by the coach for hand-restraint practice [citation:txt3][citation:txt1][citation:txt2]. The device is shown in close-up at the end of the video, reinforcing its role in enhancing shooting accuracy and enabling fun, structured practice [citation:txt1][citation:txt5]. The coach’s use of the device with young players and his own demonstration of the hand-restraint device highlight the product’s integration into real-game settings and its utility in both training and competitive play [citation:txt1][citation:txt2]. The video does not show the full execution of the forfeit, but the rule’s structure and the product’s performance claim are clearly demonstrated [citation:txt1][citation:txt4].

The synchronized shooting challenge and the Shot Coach training drill are both set on an outdoor basketball court under a clear blue sky, with surrounding trees, a hoop, and landscaping visible in the background [citation:txt1][citation:txt2][citation:txt3]. The video’s tone is lighthearted and competitive, emphasizing camaraderie and the fun of structured play [citation:txt1][citation:txt7]. The Shot Coach device is shown in multiple contexts — used by a coach to train young players, demonstrated by the coach himself, and featured in a close-up at the end of the video — reinforcing its role in enhancing shooting accuracy and enabling fun, structured practice [citation:txt1][citation:txt3][citation:txt5]. The video concludes with a close-up of the Shot Coach device, underscoring its role in the training drill and its performance claim [citation:txt1][citation:txt5].
```

## 7. Grounded body (exactly as in report.md)

```
# Synchronized Shooting Challenge and Shot Coach Training Drill

At 00:18:00, three men gather on an outdoor basketball court under a clear blue sky to begin a playful shooting challenge governed by the rule: “FIRST MADE SHOT SHOOTS SILLY STRING AT LOSER.” The man in the blue jersey (No. 2) explains the rules while the others prepare, holding basketballs and standing in position [20][21][22]. A product demonstration follows, showing three black basketball shooting aids with an overlay reading “Pack of 3 Basketball Shooting Aid,” reinforcing the product’s purpose in enhancing shooting accuracy and enabling fun, competitive play [20][21][23].

As the countdown from three to one flashes on screen, all three men jump and shoot simultaneously — each ball arcs perfectly into the basket, triggering the next phase of the game [20][21][22]. The man in the blue jersey is declared the winner via on-screen text and celebrates briefly before congratulating the man in the black hoodie and white cap [20][22]. The scene, set in a sunny backyard with a hoop, trampoline, and landscaping, emphasizes camaraderie and lighthearted competition [20][21][22]. A text overlay at 00:18:29 declares: “FIRST MADE SHOT SHOOTS SILLY STRING AT 100%,” tying the product’s performance claim to the game’s outcome [20][23]. The video closes with a close-up of the Shot Coach device, underscoring its role in enhancing shooting accuracy and enabling fun, structured practice [20][24].

Following the game, a basketball coach in a black hoodie and white cap uses an orange “SHOT COACH” training device to guide two young players through a drill: “SHOOT FROM HALF COURT 5 TIMES WITH SHOT COACH.” He adjusts a wristband on one player while explaining precision and repetition, with a scoreboard graphic visible and a third man in a blue jersey observing [25][22]. The coach demonstrates a hand-restraint device with orange straps, securing it on his own wrist while two observers watch, then walks to the free-throw line to prepare to shoot [20][21]. Multiple shots follow, showing different players attempting shots while being observed, reinforcing the focus on technique and consistency [20][21]. The coach holds a clipboard and gestures as he explains the drill, emphasizing precision and repetition through the Shot Coach system [25]. The video closes with a close-up of the Shot Coach device, reinforcing its role as a key tool in the structured, tech-assisted shooting drill [25][24].

The winner of the synchronized shooting challenge is the man in the blue jersey, who is declared the victor via on-screen text after all three players successfully make their shots simultaneously [20][22]. The “FIRST MADE SHOT SHOOTS SILLY STRING AT LOSER” rule is applied, and the winner is shown celebrating before congratulating the man in the black hoodie and white cap [20][22]. The forfeit outcome — shooting silly string at the loser — is implied by the product claim overlay at 00:18:29, which states “FIRST MADE SHOT SHOOTS SILLY STRING AT 100%,” though the actual act of shooting silly string is not shown in the retrieved evidence [20][23]. The video does not show the forfeit being performed, but the rule’s structure and the product’s performance claim are clearly demonstrated [20][21].

The Shot Coach device is demonstrated and used in a structured training environment, guiding young players through a half-court shooting drill and also being used by the coach for hand-restraint practice [25][20][21]. The device is shown in close-up at the end of the video, reinforcing its role in enhancing shooting accuracy and enabling fun, structured practice [20][24]. The coach’s use of the device with young players and his own demonstration of the hand-restraint device highlight the product’s integration into real-game settings and its utility in both training and competitive play [20][21]. The video does not show the full execution of the forfeit, but the rule’s structure and the product’s performance claim are clearly demonstrated [20][23].

The synchronized shooting challenge and the Shot Coach training drill are both set on an outdoor basketball court under a clear blue sky, with surrounding trees, a hoop, and landscaping visible in the background [20][21][25]. The video’s tone is lighthearted and competitive, emphasizing camaraderie and the fun of structured play [20][22]. The Shot Coach device is shown in multiple contexts — used by a coach to train young players, demonstrated by the coach himself, and featured in a close-up at the end of the video — reinforcing its role in enhancing shooting accuracy and enabling fun, structured practice [20][25][24]. The video concludes with a close-up of the Shot Coach device, underscoring its role in the training drill and its performance claim [20][24].
```

## 8. References used by this section (global numbers)

```
[20] 00:18:00–00:21:00 · episodic 3min: **[Event 1: Game Setup & Product Introduction]**  
Three men gather on an outdoor basketball court under a clear blue sky, initiating a playful game governed by the rule: “FIRST MADE SHOT SHOOTS SILLY STRING AT LOSER....
[21] 00:10:00–00:20:00 · episodic 10min: **[Event 1: Dribble Challenge Begins]**  
A man in a white t-shirt and patterned shorts initiates a timed dribbling challenge on a sunny outdoor court, with a countdown timer and on-screen text reading “MOST DRIBBLES...
[22] 00:18:30–00:19:00 · episodic 30sec: Three men gather on an outdoor basketball court under a clear blue sky, initiating a playful game governed by the rule “FIRST MADE SHOT SHOOTS SILLY STRING AT LOSER.” The man in the blue jersey (No. 2) leads the setup...
[23] 00:18:00–00:18:30 · episodic 30sec: **[Event 1: Introduction of Basketball Court Scene]**  
Three men are on an outdoor basketball court: one in a red and white jersey gestures while crouched, another in a white t-shirt bends and stands, and a third in...
[24] 00:19:50–00:20:00 · episodic 10sec: A basketball coach wearing a white cap and black hoodie stands on an outdoor court, holding a clipboard and an orange device, instructing two young players. A text overlay reads, “SHOOT FROM HALF COURT 5 TIMES WITH SH...
[25] 00:19:30–00:20:00 · episodic 30sec: A basketball coach in a black hoodie and white cap stands on an outdoor court, using an orange “SHOT COACH” training device to instruct two young players, with a text overlay directing them to “SHOOT FROM HALF COURT 5...
```
