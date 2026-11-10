# Section 3 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 764 words → after removal 764 words

## 2. Start/end claim check (`boundary_claims`)

- ending_early: The video closes with a close-up of the Shot Coach device, reinforcing its role in tech-assisted training [citation:txt4][citation:txt5]. (cited [4, 5], latest cited end 00:21:00)
- ending_unverifiable: The video concludes with the Shot Coach being used in a training drill and a synchronized shooting challenge, highlighting the integration of technology into basketball training and play. (cited [])

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 31, "cited_sentences": 11, "checked_tokens": 19, "unsupported": 0, "miscited": 1, "uncited_claims": 1, "absence_statements": 0}`

- **miscited** time `00:19:30` cited ['txt3'] found in ['txt4', 'txt5'] — At 00:19:30, the man in the black hoodie performs sit-ups on a concrete court, with on-screen text “CASH LOST” explained by voiceover as punishment for the fewest flick shots [citation:txt3].
- **uncited**  `['100']` cited [] — The Flick Glove’s rules are straightforward: three shots with the glove, then three without; the person making the fewest baskets must do 100 sit-ups.

## 4. Citation conversion stats

- `{"text_citations": 23, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 0, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 5 of 12

## 5. Image-text time alignment

- no cited image

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Testing the Flick Glove and Shot Coach: Rules, Performance, and Consequences

At 00:08:00, a shooting challenge begins with the Flick Glove, a device featuring finger loops and a rectangular screen, as explained by a man in a black hoodie and white cap who holds the glove while two others observe [citation:txt1]. A text overlay clarifies the rules: participants take three shots using the glove, followed by three without it; the person making the fewest baskets is required to complete 100 sit-ups [citation:txt1][citation:txt6]. The man in the red hoodie expresses confusion about the glove’s orientation, prompting a demonstration from the man in the black hoodie [citation:txt1][citation:txt6]. The glove is shown in three color options — white, black, and orange — with the brand name “FLICK GLOVE” overlaid [citation:txt1].

During the challenge, players attempt shots while wearing the glove. The man in the red hoodie makes a shot, humorously noting the ball nearly slipped off his pinky finger, and later critiques his flick motion for lacking straightness before preparing for another attempt [citation:txt3]. The player in the blue jersey makes three consecutive shots, confirmed by on-screen text “3 MADE BASKETS,” and later scores again, reaching “4 MADE BASKETS,” celebrating while speaking casually [citation:txt3][citation:txt7]. The man in the black hoodie also makes shots, one of which is debated by teammates — “too far,” “cheating” — but he later scores again, celebrated with “Woo!” and “WHOOOOOO” graphics [citation:txt2].

The scoring system is directly tied to performance: the fewest baskets result in a physical consequence. At 00:19:30, the man in the black hoodie performs sit-ups on a concrete court, with on-screen text “CASH LOST” explained by voiceover as punishment for the fewest flick shots [citation:txt3]. He later continues sit-ups beside a pool, with a graphic displaying “SCORE 7” as he gestures and celebrates with teammates [citation:txt3]. The forfeit is presented as a lighthearted consequence, with teammates reacting with humor and approval — one jokes about “bouncing titties,” another compares chest sizes, and the man deflects with “Bro, I’m wearing a big shirt” [citation:txt2]. His movements become off-rhythm during the jumping jacks, drawing amused observation from onlookers [citation:txt2].

The Shot Coach device is used in a structured training drill. At 00:19:30, a basketball coach in a black hoodie and white cap uses an orange Shot Coach device to instruct two young players, directing them to “SHOOT FROM HALF COURT 5 TIMES WITH SHOT COACH” [citation:txt4]. He adjusts a wristband on one player while explaining precision and repetition, emphasizing the device’s role in enhancing shooting accuracy [citation:txt4][citation:txt5]. The coach holds a clipboard and gestures while explaining, and the scene includes a scoreboard graphic showing “-2” then resetting to “0,” followed by “-1,” suggesting a playful or competitive scoring context [citation:txt4]. The video closes with a close-up of the Shot Coach device, reinforcing its role in tech-assisted training [citation:txt4][citation:txt5].

The Shot Coach is also used in a synchronized shooting drill. At 00:18:00, three men jump and shoot simultaneously — each ball arcs perfectly into the basket — and the man in the blue jersey is declared the winner via on-screen text [citation:txt5]. The coach later demonstrates a hand-restraint device with orange straps, securing it on his own wrist while two observers watch, then walks to the free-throw line to shoot [citation:txt5]. The device is shown as a tool for improving technique and consistency, integrated into real-game settings [citation:txt5].

The Flick Glove and Shot Coach are both presented as tools that integrate into structured gameplay, with consequences tied to performance. The Flick Glove’s scoring system links shot outcomes to physical challenges, while the Shot Coach is used in training drills to enhance accuracy and repetition. The camaraderie among players is evident throughout, with humor and light-hearted teasing accompanying both challenges and training sessions. The video highlights how gadgets are embedded into gameplay with clear rules, measurable outcomes, and social reinforcement — whether through forfeits, scoring graphics, or celebratory animations.

The Flick Glove’s rules are straightforward: three shots with the glove, then three without; the person making the fewest baskets must do 100 sit-ups. The Shot Coach is used in training to improve shooting technique through structured drills, with a focus on precision and repetition. The sit-up forfeit is a direct consequence of poor performance, met with humor and camaraderie, reinforcing the lighthearted competitive nature of the challenges. The devices are shown as integral to structured gameplay, with consequences tied to performance and social reinforcement. The video concludes with the Shot Coach being used in a training drill and a synchronized shooting challenge, highlighting the integration of technology into basketball training and play.
```

## 7. Grounded body (exactly as in report.md)

```
# Testing the Flick Glove and Shot Coach: Rules, Performance, and Consequences

At 00:08:00, a shooting challenge begins with the Flick Glove, a device featuring finger loops and a rectangular screen, as explained by a man in a black hoodie and white cap who holds the glove while two others observe [15]. A text overlay clarifies the rules: participants take three shots using the glove, followed by three without it; the person making the fewest baskets is required to complete 100 sit-ups [15][16]. The man in the red hoodie expresses confusion about the glove’s orientation, prompting a demonstration from the man in the black hoodie [15][16]. The glove is shown in three color options — white, black, and orange — with the brand name “FLICK GLOVE” overlaid [15].

During the challenge, players attempt shots while wearing the glove. The man in the red hoodie makes a shot, humorously noting the ball nearly slipped off his pinky finger, and later critiques his flick motion for lacking straightness before preparing for another attempt [2]. The player in the blue jersey makes three consecutive shots, confirmed by on-screen text “3 MADE BASKETS,” and later scores again, reaching “4 MADE BASKETS,” celebrating while speaking casually [2][17]. The man in the black hoodie also makes shots, one of which is debated by teammates — “too far,” “cheating” — but he later scores again, celebrated with “Woo!” and “WHOOOOOO” graphics [18].

The scoring system is directly tied to performance: the fewest baskets result in a physical consequence. At 00:19:30, the man in the black hoodie performs sit-ups on a concrete court, with on-screen text “CASH LOST” explained by voiceover as punishment for the fewest flick shots [2]. He later continues sit-ups beside a pool, with a graphic displaying “SCORE 7” as he gestures and celebrates with teammates [2]. The forfeit is presented as a lighthearted consequence, with teammates reacting with humor and approval — one jokes about “bouncing titties,” another compares chest sizes, and the man deflects with “Bro, I’m wearing a big shirt” [18]. His movements become off-rhythm during the jumping jacks, drawing amused observation from onlookers [18].

The Shot Coach device is used in a structured training drill. At 00:19:30, a basketball coach in a black hoodie and white cap uses an orange Shot Coach device to instruct two young players, directing them to “SHOOT FROM HALF COURT 5 TIMES WITH SHOT COACH” [19]. He adjusts a wristband on one player while explaining precision and repetition, emphasizing the device’s role in enhancing shooting accuracy [19][20]. The coach holds a clipboard and gestures while explaining, and the scene includes a scoreboard graphic showing “-2” then resetting to “0,” followed by “-1,” suggesting a playful or competitive scoring context [19]. The video closes with a close-up of the Shot Coach device, reinforcing its role in tech-assisted training [19][20].

The Shot Coach is also used in a synchronized shooting drill. At 00:18:00, three men jump and shoot simultaneously — each ball arcs perfectly into the basket — and the man in the blue jersey is declared the winner via on-screen text [20]. The coach later demonstrates a hand-restraint device with orange straps, securing it on his own wrist while two observers watch, then walks to the free-throw line to shoot [20]. The device is shown as a tool for improving technique and consistency, integrated into real-game settings [20].

The Flick Glove and Shot Coach are both presented as tools that integrate into structured gameplay, with consequences tied to performance. The Flick Glove’s scoring system links shot outcomes to physical challenges, while the Shot Coach is used in training drills to enhance accuracy and repetition. The camaraderie among players is evident throughout, with humor and light-hearted teasing accompanying both challenges and training sessions. The video highlights how gadgets are embedded into gameplay with clear rules, measurable outcomes, and social reinforcement — whether through forfeits, scoring graphics, or celebratory animations.

The Flick Glove’s rules are straightforward: three shots with the glove, then three without; the person making the fewest baskets must do 100 sit-ups. The Shot Coach is used in training to improve shooting technique through structured drills, with a focus on precision and repetition. The sit-up forfeit is a direct consequence of poor performance, met with humor and camaraderie, reinforcing the lighthearted competitive nature of the challenges. The devices are shown as integral to structured gameplay, with consequences tied to performance and social reinforcement. The video concludes with the Shot Coach being used in a training drill and a synchronized shooting challenge, highlighting the integration of technology into basketball training and play.
```

## 8. References used by this section (global numbers)

```
[2] 00:00:00–00:10:00 · episodic 10min: **Six men—Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player—gather on a sunny outdoor basketball court to test 12 viral sports gadgets, splitting into two teams of three. Dressed in athletic wear, they i...
[15] 00:08:00–00:08:30 · episodic 30sec: Three men on an outdoor basketball court prepare for a shooting challenge involving the Flick Glove — a device designed to improve basketball shooting technique. One man in a black hoodie and white cap, holding a bask...
[16] 00:08:20–00:08:30 · episodic 10sec: Three men stand on an outdoor basketball court. A text overlay explains a challenge: take three shots with a flick glove, then three without, and the person making the least baskets must do 100 sit-ups. One man in a r...
[17] 00:10:00–00:10:30 · episodic 30sec: Three people are on an outdoor basketball court under a clear blue sky. A player in a red hoodie attempts a shot but misses; the ball arcs toward the hoop and falls short. The player in the blue jersey then takes a sh...
[18] 00:06:00–00:09:00 · episodic 3min: A man in a white hoodie and patterned shorts shoots basketballs on a sunny court, with a score counter updating after each shot — from 0/0 to 3/5 — while a humorous voiceover references product ownership and investmen...
[19] 00:19:30–00:20:00 · episodic 30sec: A basketball coach in a black hoodie and white cap stands on an outdoor court, using an orange “SHOT COACH” training device to instruct two young players, with a text overlay directing them to “SHOOT FROM HALF COURT 5...
[20] 00:18:00–00:21:00 · episodic 3min: **[Event 1: Game Setup & Product Introduction]**  
Three men gather on an outdoor basketball court under a clear blue sky, initiating a playful game governed by the rule: “FIRST MADE SHOT SHOOTS SILLY STRING AT LOSER....
```
