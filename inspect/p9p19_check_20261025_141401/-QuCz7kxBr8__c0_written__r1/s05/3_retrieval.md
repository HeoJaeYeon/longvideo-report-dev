# Section 5 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:19:27): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 22, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 6.07}`
- image request (2026-10-25 14:19:30): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 1.01}`
- L1 filter LLM call: prompt 9288 tokens, output 70 tokens, 4.9 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 |  | worldmm-episodic | 3min | 00:09:00–00:12:00 | 1 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_3` |
| txt2 |  | worldmm-episodic | 3min | 00:03:00–00:06:00 | 2 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_1` |
| txt3 | ✓ | worldmm-episodic | 30sec | 00:36:30–00:37:00 | 3 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_73` |
| txt4 | ✓ | worldmm-episodic | 10sec | 00:36:50–00:37:00 | 4 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_221` |
| txt5 |  | worldmm-episodic | 3min | 00:06:00–00:09:00 | 5 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_2` |
| txt6 | ✓ | worldmm-episodic | 30sec | 00:37:00–00:37:30 | 6 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_74` |
| txt7 | ✓ | worldmm-episodic | 10sec | 00:37:30–00:37:37 | 7 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_225` |
| txt8 |  | worldmm-episodic | 30sec | 00:29:00–00:29:30 | 8 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_58` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.032002 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_103` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_36` |
| txt11 | ✓ | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_152` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_39` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1**

```
[00:09:00-00:12:00 | episodic 3min] A man in a black hoodie and white cap demonstrates a basketball drill on an outdoor court, successfully shooting and gesturing to explain technique, enhanced by animated graphics. He acknowledges tech-assisted visuals, praising a teammate in a blue jersey, then encourages another player in a red hoodie with “You look like you're hot right now, bro,” reinforcing camaraderie during a casual game. 

The player in the red hoodie makes a shot, humorously noting the ball nearly slipped off his pinky finger. He pauses, gestures while holding a wristband, removes it, and reflects on his performance. He critiques his flick motion, acknowledging lack of straightness, before preparing for another attempt, observed by two onlookers in black and blue attire.

Meanwhile, the player in the blue jersey makes three consecutive shots, confirmed by on-screen text “3 MADE BASKETS,” then later scores again, reaching “4 MADE BASKETS.” He celebrates while speaking casually, with graphics of basketballs and audio commentary referencing conditioning and sit-ups. The branded “HYPER” court and clear skies frame the scene.

Separately, the man in the black hoodie performs sit-ups on a concrete court, with on-screen text “CASH LOST,” explained by voiceover as punishment for fewest flick shots. A blonde-bearded man in red watches and speaks animatedly. Later, the same man continues sit-ups beside a pool, where a graphic displays “SCORE 7” as he gestures and celebrates with two teammates — one in pink shorts, the other in a “SHY 2” jersey — in a lively, sunlit setting.

The group, including a man in a “ZHYPE” jersey and hoodie, gathers for discussion, holding a basketball with a “POWERHANDZ Dribble Sleeve” overlay, preparing for a demonstration or game. The scene remains focused on strategy and play, with the score updating to “SCORE 7,” reinforcing the competitive yet casual tone.
```

**txt2**

```
[00:03:00-00:06:00 | episodic 3min] Three men gather on an outdoor basketball court, negotiating positions before settling into a shooting challenge. One man in a black hoodie and white cap adjusts a basketball on a training device while the others—wearing red and blue jerseys—observe, holding balls. A fourth person films the scene under clear skies, with trees and a fence in the background. The group transitions to a hoop with a vertical obstacle, where they take turns shooting under a 30-second countdown. Encouragement and light-hearted banter—such as “you might be safe just making it past that first one”—add to the casual yet competitive tone. The man in the black hoodie successfully makes his shot, smiling as he walks back, while the man in red watches amusedly. Their conversation hints at past forfeits and humorous self-deprecation.

The group then evaluates a dribble stick, with the man in the blue jersey rating it an 8/10, followed by the man in the black shirt agreeing, and the man in the black hoodie giving it a 7—joking that anything helping him fail is “pretty good.” The conversation remains lighthearted and collaborative.

Later, a man in a white hoodie demonstrates the “Straight Shooter Strap,” explaining how it stabilizes the elbow during shooting. He adjusts the strap on his arm while a third observer watches. The scene widens to show the full court, hoop, and surrounding hills under clear skies, setting up practical use of the device.

A shooter in a white shirt and patterned shorts begins a shooting sequence, initially making one shot (0/1), then missing several, with the scoreboard climbing to 0/3. He pauses, inspecting his elbow, seemingly frustrated. As the sequence continues, he scores more shots, pushing the tally to 3/16, with teammates retrieving balls and commentary tracking each attempt. The scoreboard climbs steadily, accompanied by remarks like “Dude, 15,” and “Zach’s uses this thing, bro.” The player smiles at the camera as he approaches 15 successful shots, with the backdrop of a large house and trees under clear skies.
```

**txt3** (cited)

```
[00:36:30-00:37:00 | episodic 30sec] Two men compete in a one-on-one basketball game on an outdoor court under clear skies, with the player in the white hoodie and blue shorts repeatedly shooting over a defender using a padded training pad. After successfully scoring, a graphic overlay displays “2-1,” and the shooter smiles at the camera before preparing for the next play. The game continues with the same player driving to the basket, elevating for a shot while the defender contests, and the ball swishing through the net as the shooter celebrates. The final sequence shows the player in the white hoodie and patterned shorts celebrating with arms outstretched as on-screen text announces “3-1” and “ZAK JESSE & KRIS WIN,” followed by interaction with another player in a tie-dye jersey, while spectators watch from the court and a nearby wall.
```

**txt4** (cited)

```
[00:36:50-00:37:00 | episodic 10sec] A man in a white hoodie and patterned shorts celebrates with arms outstretched on an outdoor basketball court, as text overlays announce “3-1” and “ZAK JESSE & KRIS WIN.” He then turns and interacts with another player in a tie-dye jersey, while others are visible in the background on the court and atop a wall.
```

**txt5**

```
[00:06:00-00:09:00 | episodic 3min] A man in a white hoodie and patterned shorts shoots basketballs on a sunny court, with a score counter updating after each shot — from 0/0 to 3/5 — while a humorous voiceover references product ownership and investment. He praises the product as “great,” with a “#NOT SPONSORED” graphic. The scene cuts to another player resetting the score.

A second player makes a shot (1/2), but audio commentary criticizes the product’s performance, noting it “fell off” and “snaps” when extended. A shooting contest unfolds: a player in a red and white jersey (No. 2) makes a successful shot (2/5), celebrated with surprise and joy. Later, the tie-dye jersey player loses, prompting the white-shirted man to propose testing his jump shot without the strap to isolate the issue — a playful, lighthearted challenge.

His jump shot misses, sparking frustration and speculation about the strap. A teammate confirms the issue, and a forfeit of 30 jumping jacks is suggested. The man begins doing jumping jacks, arms raised, while two others watch and tease — one jokes about “bouncing titties,” another compares chest sizes. He deflects with humor, “Bro, I’m wearing a big shirt.” His movements become off-rhythm, drawing amused observation.

Three men discuss and humorously rate the product: the white-hoodie man (ZHYPE) calls it suitable for kids but suggests a better gadget for beginners, scoring it “1.” They escalate to exaggerated scoring — “1,” “2,” then “-3k” — ending with a playful “what’s the next invention?” 

A shooting challenge with the Flick Glove begins: one man in a black hoodie explains rules — three shots with the glove, then without — with the fewest baskets requiring 100 sit-ups. The red-hoodie man misunderstands the glove’s orientation, prompting a demonstration. The glove’s design (finger loops, screen) and color options (white, black, orange) are shown.

Three men demonstrate basketball drills under sunny skies, with the blue-jersey man explaining movement techniques. A shot by the black-hoodie man is debated — “too far,” “cheating.” Later, he makes another shot, celebrated with “Woo!” and “WHOOOOOO” graphics, emphasizing triumph and energy.
```

**txt6** (cited)

```
[00:37:00-00:37:30 | episodic 30sec] A young basketball player in a "ZHYPE 2" jersey begins on an outdoor court, facing the camera before turning and walking toward the basket; other players are visible nearby, including one holding a ball, under a sunny sky with mountains in the background and “ZHYPE” painted on the court floor.

A tall player in a white and red “ZHYPE” jersey with the number 8 stands at the center of the court, gesturing as if giving instructions, flanked by teammates — one holding a basketball and another in a hoodie — while others move around the perimeter under a clear blue sky, with trees and hills in the background.

The scene concludes with the same player raising his arms in gesture, as two teammates stand beside him, one holding a basketball, before transitioning to a static end screen featuring a blue and white graphic, the text “Thank you for watching” and “DON’T FORGET TO SUBSCRIBE!”, alongside the “F1HYPE” logo.
```

**txt7** (cited)

```
[00:37:30-00:37:37 | episodic 10sec] The video displays a static end screen with a white background and blue geometric shapes. The text "Thank you for watching" and "DON'T FORGET TO SUBSCRIBE!" is centered, with arrows pointing to two black rectangular placeholders, likely for suggested videos or subscription buttons. The logo "F1HYPE" is visible in the top left corner. There is no audio or movement throughout the segment.
```

**txt8**

```
[00:29:00-00:29:30 | episodic 30sec] **Six men gather on an outdoor basketball court under a clear blue sky to begin a competitive game.** One man in a white hoodie and patterned shorts holds two large black training pads, gesturing as he explains the rules to the group; text on screen confirms the format: “FIRST TO 3 WINS” and “LOSER DOES FORFEIT.” The group, dressed in athletic wear, listens intently. The camera shifts to show a player in a white jersey preparing to throw one of the pads, while others observe. A brief video game-style overlay appears, showing a first-person perspective and a scoreboard, emphasizing the competitive nature of the game. Later, a player in a white and red “ZHYTE 2” jersey, still holding the pads, stretches his arms wide before lowering them to face a man in a black hoodie and white cap who holds a basketball. A third man in a blue jersey stands in the background with arms crossed, as mountains loom in the distance under the bright sun.
```

**txt9**

```
[video-level knowledge | semantic] (SCORE 8, is displayed, on graphic)
```

**txt10**

```
[video-level knowledge | semantic] (challenge, penalizes least baskets with, 100 sit-ups)
```

**txt11** (cited)

```
[video-level knowledge | semantic] (F1HYPE, appears in video, at top left corner)
```

**txt12**

```
[video-level knowledge | semantic] (on-screen text, reads, MOST DRIBBLES IN 15 SECONDS)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:00:25 | 00:00:20–00:00:30 | `-QuCz7kxBr8:visual:00002000` | `outputs/p9p19_check_20261025_141401/frames_s0/-QuCz7kxBr8/00002000.jpg` |
| img2 |  | 00:17:35 | 00:17:30–00:17:40 | `-QuCz7kxBr8:visual:00173000` | `outputs/p9p19_check_20261025_141401/frames_s0/-QuCz7kxBr8/00173000.jpg` |
| img3 |  | 00:16:35 | 00:16:30–00:16:40 | `-QuCz7kxBr8:visual:00163000` | `outputs/p9p19_check_20261025_141401/frames_s0/-QuCz7kxBr8/00163000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:00:20-00:00:30 | video frame at 25.0s] On an outdoor basketball court, a group of six men—Chris, Zach, Cass, James, and Mitchell—are introduced as they prepare to test 12 viral basketball gadgets. They are split into two teams, each assigned six gadgets to evaluate. The men, dressed in athletic wear, hold basketballs and gesture as they speak, with one man in a white hoodie and blue shorts speaking directly to the camera while the others stand around him. The setting is sunny, with a basketball hoop and surrounding trees visible in the background.
```

**img2**

```
[00:17:30-00:17:40 | video frame at 1055.0s] Three young men are standing on a basketball court in front of a large house. One man, wearing a white hoodie with "ZHYPE" printed on it, holds a basketball up with his right hand. He is smiling and looking toward the camera. The other two men stand beside him, one in a white t-shirt and the other in a tie-dye basketball jersey with the number 2. They are all looking in the same direction, seemingly posing for a photo or video. The scene is outdoors in bright daylight.
```

**img3**

```
[00:16:30-00:16:40 | video frame at 995.0s] Three men are on an outdoor basketball court under a clear sky. The man in the center, wearing a "ZHYPE" jersey, holds up a large Wilson basketball, smiling as he presents it to the camera. To his left, another man in a white t-shirt stands with his arms crossed, looking on. To the right, a third man in a white hoodie and patterned shorts also holds a basketball. The court is surrounded by a fence and a large house, with mountains visible in the background. There is no audible content in this segment.
```
