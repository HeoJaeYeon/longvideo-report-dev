# Section 1 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:15:53): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 2, 'episodic_candidates': 17, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 12.19}`
- image request (2026-10-25 14:15:56): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 1.28}`
- L1 filter LLM call: prompt 8661 tokens, output 66 tokens, 4.4 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 3min | 00:00:00–00:03:00 | 1 / 0.032787 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_0` |
| txt2 | ✓ | worldmm-episodic | 30sec | 00:00:00–00:00:30 | 2 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_0` |
| txt3 | ✓ | worldmm-episodic | 10min | 00:00:00–00:10:00 | 3 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10min_0` |
| txt4 | ✓ | worldmm-episodic | 30sec | 00:00:30–00:01:00 | 4 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_1` |
| txt5 |  | worldmm-episodic | 10sec | 00:00:40–00:00:50 | 5 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_4` |
| txt6 | ✓ | worldmm-episodic | 30sec | 00:02:30–00:03:00 | 6 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_5` |
| txt7 | ✓ | worldmm-episodic | 30sec | 00:02:00–00:02:30 | 7 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_4` |
| txt8 | ✓ | worldmm-episodic | 10sec | 00:01:40–00:01:50 | 8 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_10` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.031498 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_44` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_123` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_36` |
| txt12 | ✓ | worldmm-semantic | — | no timestamp | 4 / 0.016129 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_129` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:00:00-00:03:00 | episodic 3min] Six men—Chris, Zach, Cass, James, Mitchell, and a sixth unnamed player—gather on a sunny outdoor basketball court to test 12 viral sports gadgets, splitting into two teams of three. Dressed in athletic wear, they introduce the challenge while holding basketballs near a hoop and trees. One man in a white hoodie addresses the camera, setting the tone with playful banter and audio cues like “Hands up, hands up” and “Mump is blinding me.” The scene transitions to a countdown and gear review, beginning with a close-up of black nylon straps, signaling the start of hands-on testing.

The group begins evaluating gadgets, starting with “SPORTS DRIBBLE SPECS.” One player dons the goggles and prepares for a dribbling time trial, where participants must dribble through three cones and touch a pole to stop the clock. Rules are clarified near a pool under bright sunlight, with the man in the hoodie confirming the forfeit rule for the slowest time. The drill proceeds with players like Chris and Zach showcasing speed and control, with timers capturing times like 10:85 and 9:51 seconds. Commentary highlights frustrations (“handles were definitely off”) and praise (“He’s making great time”), emphasizing the competitive yet casual atmosphere.

Later, the group discusses the gadget’s usefulness, with the man in the white hoodie expressing discomfort with traditional basketballs forcing him to look down. A score graphic flashes from 5 to 6, then 4, as teammates react with thumbs-up approval. The segment ends with the introduction of the SKLZ Dribble Stick—a black training tool with adjustable yellow arms—where the blue-jerseyed player prepares to demonstrate its use. Rules are reviewed: players dribble while avoiding the stick; the first to touch it runs five laps. The group is ready to begin, setting up for the next round of testing.
```

**txt2** (cited)

```
[00:00:00-00:00:30 | episodic 30sec] A group of six men—Chris, Zach, Cass, James, and Mitchell—gather on a sunny outdoor basketball court to test 12 viral basketball gadgets, splitting into two teams of three each, with six gadgets assigned per team. Dressed in athletic wear and holding basketballs, they introduce themselves and the challenge while standing near a hoop and trees. One man in a white hoodie and blue shorts addresses the camera directly, while others gesture and prepare for the evaluations. The scene opens with a brief highlight of a player in a white jersey (number 3) dunking, followed by a close-up of a “FLEX” finger trainer tool and a shot of a player dribbling near a cone, with teammates nearby. Audio snippets like “Hands up, hands up,” “Mump is blinding me,” and “All right, bro” underscore the playful, competitive tone. The video transitions to a man in a black hoodie and cap speaking animatedly to the group, while a countdown and introduction to the gadget-testing segment are heard. A close-up of three black nylon straps with buckles on a white surface is shown, signaling the start of the gear review. The group prepares to evaluate the gadgets, setting the stage for a hands-on, action-packed testing session.
```

**txt3** (cited)

```
[00:00:00-00:10:00 | episodic 10min] **Six men—Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player—gather on a sunny outdoor basketball court to test 12 viral sports gadgets, splitting into two teams of three. Dressed in athletic wear, they introduce the challenge while holding basketballs near a hoop and trees. One man in a white hoodie addresses the camera, setting the tone with playful banter and audio cues like “Hands up, hands up” and “Mump is blinding me.” The scene transitions to a countdown and gear review, beginning with a close-up of black nylon straps, signaling the start of hands-on testing.**

The group begins evaluating gadgets, starting with “SPORTS DRIBBLE SPECS.” One player dons the goggles and prepares for a dribbling time trial, where participants must dribble through three cones and touch a pole to stop the clock. Rules are clarified near a pool under bright sunlight, with the man in the hoodie confirming the forfeit rule for the slowest time. The drill proceeds with players like Chris and Zach showcasing speed and control, with timers capturing times like 10:85 and 9:51 seconds. Commentary highlights frustrations (“handles were definitely off”) and praise (“He’s making great time”), emphasizing the competitive yet casual atmosphere.

Later, the group discusses the gadget’s usefulness, with the man in the white hoodie expressing discomfort with traditional basketballs forcing him to look down. A score graphic flashes from 5 to 6, then 4, as teammates react with thumbs-up approval. The segment ends with the introduction of the SKLZ Dribble Stick—a black training tool with adjustable yellow arms—where the blue-jerseyed player prepares to demonstrate its use. Rules are reviewed: players dribble while avoiding the stick; the first to touch it runs five laps. The group is ready to begin, setting up for the next round of testing.

**Three men gather on an outdoor basketball court, negotiating positions before settling into a shooting challenge. One man in a black hoodie and white cap adjusts a basketball on a training device while the others—wearing red and blue jerseys—observe, holding balls. A fourth person films the scene under clear skies, with trees and a fence in the background. The group transitions to a hoop with a vertical obstacle, where they take turns shooting under a 30-second countdown. Encouragement and light-hearted banter—such as “you might be safe just making it past that first one”—add to the casual yet competitive tone. The man in the black hoodie successfully makes his shot, smiling as he walks back, while the man in red watches amusedly. Their conversation hints at past forfeits and humorous self-deprecation.**

The group then evaluates the dribble stick, with the man in the blue jersey rating it an 8/10, followed by the man in the black shirt agreeing, and the man in the black hoodie giving it a 7—joking that anything helping him fail is “pretty good.” The conversation remains lighthearted and collaborative.

**Later, a man in a white hoodie demonstrates the “Straight Shooter Strap,” explaining how it stabilizes the elbow during shooting. He adjusts the strap on his arm while a third observer watches. The scene widens to show the full court, hoop, and surrounding hills under clear skies, setting up practical use of the device.**

A shooter in a white shirt and patterned shorts begins a shooting sequence, initially making one shot (0/1), then missing several, with the scoreboard climbing to 0/3. He pauses, inspecting his elbow, seemingly frustrated. As the sequence continues, he scores more shots, pushing the tally to 3/16, with teammates retrieving balls and commentary tracking each attempt. The scoreboard climbs steadily, accompanied by remarks like “Dude, 15,” and “Zach’s uses this thing, bro.” The player smiles at the camera as he approaches 15 successful shots, with the backdrop of a large house and trees under clear skies.

**A man in a white hoodie and patterned shorts shoots basketballs on a sunny court, with a score counter updating after each shot — from 0/0 to 3/5 — while a humorous voiceover references product ownership and investment. He praises the product as “great,” with a “#NOT SPONSORED” graphic. The scene cuts to another player resetting the score.**

A second player makes a shot (1/2), but audio commentary criticizes the product’s performance, noting it “fell off” and “snaps” when extended. A shooting contest unfolds: a player in a red and white jersey (No. 2) makes a successful shot (2/5), celebrated with surprise and joy. Later, the tie-dye jersey player loses, prompting the white-shirted man to propose testing his jump shot without the strap to isolate the issue — a playful, lighthearted challenge.

His jump shot misses, sparking frustration and speculation about the strap. A teammate confirms the issue, and a forfeit of 30 jumping jacks is suggested. The man begins doing jumping jacks, arms raised, while two others watch and tease — one jokes about “bouncing titties,” another compares chest sizes. He deflects with humor, “Bro, I’m wearing a big shirt.” His movements become off-rhythm, drawing amused observation.

**Three men discuss and humorously rate the product: the white-hoodie man (ZHYPE) calls it suitable for kids but suggests a better gadget for beginners, scoring it “1.” They escalate to exaggerated scoring — “1,” “2,” then “-3k” — ending with a playful “what’s the next invention?”**

**A shooting challenge with the Flick Glove begins: one man in a black hoodie explains rules — three shots with the glove, then without — with the fewest baskets requiring 100 sit-ups. The red-hoodie man misunderstands the glove’s orientation, prompting a demonstration. The glove’s design (finger loops, screen) and color options (white, black, orange) are shown.**

Three men demonstrate basketball drills under sunny skies, with the blue-jersey man explaining movement techniques. A shot by the black-hoodie man is debated — “too far,” “cheating.” Later, he makes another shot, celebrated with “Woo!” and “WHOOOOOO” graphics, emphasizing triumph and energy.

**A man in a black hoodie and white cap demonstrates a basketball drill on an outdoor court, successfully shooting and gesturing to explain technique, enhanced by animated graphics. He acknowledges tech-assisted visuals, praising a teammate in a blue jersey, then encourages another player in a red hoodie with “You look like you're hot right now, bro,” reinforcing camaraderie during a casual game.**

The player in the red hoodie makes a shot, humorously noting the ball nearly slipped off his pinky finger. He pauses, gestures while holding a wristband, removes it, and reflects on his performance. He critiques his flick motion, acknowledging lack of straightness, before preparing for another attempt, observed by two onlookers in black and blue attire.

Meanwhile, the player in the blue jersey makes three consecutive shots, confirmed by on-screen text “3 MADE BASKETS,” then later scores again, reaching “4 MADE BASKETS.” He celebrates while speaking casually, with graphics of basketballs and audio commentary referencing conditioning and sit-ups. The branded “HYPER” court and clear skies frame the scene.

**Separately, the man in the black hoodie performs sit-ups on a concrete court, with on-screen text “CASH LOST,” explained by voiceover as punishment for fewest flick shots. A blonde-bearded man in red watches and speaks animatedly. Later, the same man continues sit-ups beside a pool, where a graphic displays “SCORE 7” as he gestures and celebrates with two teammates — one in pink shorts, the other in a “SHY 2” jersey — in a lively, sunlit setting.**

The group, including a man in a “ZHYPE” jersey and hoodie, gathers for discussion, holding a basketball with a “POWERHANDZ Dribble Sleeve” overlay, preparing for a demonstration or game. The scene remains focused on strategy and play, with the score updating to “SCORE 7,” reinforcing the competitive yet casual tone.
```

**txt4** (cited)

```
[00:00:30-00:01:00 | episodic 30sec] A group of men on an outdoor basketball court introduces a gadget challenge where teams will select and test their favorite sports gear. The segment kicks off with one man in a white hoodie and blue shorts holding a basketball and addressing the camera, while the camera pans to another player examining a small object—revealed to be a pair of “SPORTS DRIBBLE SPECS” in packaging. One participant then puts on the goggles, adjusts them, and prepares for a dribbling time trial alongside a teammate near a hoop. The scene transitions to three men near a pool, where the rules of the “dribble time trial” are explained: players must dribble through three cones and touch a pole to stop the clock, with the slowest time resulting in a forfeit. The man in the hoodie confirms the rule, and the others listen attentively under bright, sunny conditions with the pool and greenery in the background.
```

**txt5**

```
[00:00:40-00:00:50 | episodic 10sec] A person puts on a pair of sports goggles labeled "SPORTS DRIBBLE SPECS" on an outdoor basketball court. Another person watches as the first person adjusts the goggles. The person wearing the goggles then holds a basketball, and the two men stand near a basketball hoop, preparing for a time trial.
```

**txt6** (cited)

```
[00:02:30-00:03:00 | episodic 30sec] Three men gather on an outdoor basketball court, preparing for a dribbling challenge using a SKLZ Dribble Stick. The man in the red hoodie introduces the game, asking if they want to see how the dribble stick works, while the man in the blue jersey prepares to demonstrate it. The device—a black training tool with adjustable yellow arms and “DRIBBLE STICK” branding—is shown in detail before the group assembles, each holding a basketball, to review the rules: players take turns dribbling while avoiding contact with the stick; the person who fails first must run five laps around the court. The group is ready to begin, with the blue-jerseyed player poised to lead the demonstration.
```

**txt7** (cited)

```
[00:02:00-00:02:30 | episodic 30sec] Three young men stand on an outdoor basketball court, each holding a ball, engaged in a discussion about dribbling drills and the usefulness of a gadget that helps players avoid looking down. The setting is a sunny backyard with a pool and house in the background; on-screen text displays “9:51 SECONDS.” The man in the center, wearing a white hoodie and sunglasses, gestures while speaking, expressing personal discomfort with the basketballs he’s using — claiming they force him to tilt his head down more. As the conversation progresses, a score graphic briefly flashes from 5 to 6, and later shows 4, while the man on the right, in a white t-shirt, responds with a thumbs-up after a rating of 5 is mentioned, indicating agreement or approval of the gadget’s effectiveness. The group remains casually engaged, with the man in the red and white jersey listening attentively.
```

**txt8** (cited)

```
[00:01:40-00:01:50 | episodic 10sec] At an outdoor basketball court beside a pool, a man in a white hoodie and patterned shorts holds a basketball while talking to another player in a tie-dye jersey. The player in the jersey stands with his hands on his hips, listening. In the background, another person dribbles a basketball. The conversation includes comments about handles being off and making it harder to dribble, with a mention that "Zach is off" and "He's making great time." The scene shifts to a wider view of the court, showing the players in position for a drill or game.
```

**txt9**

```
[video-level knowledge | semantic] (The text overlay, reads, 20 LOW, MEDIUM, & HIGH DRIBBLES IN 60 SECONDS)
```

**txt10**

```
[video-level knowledge | semantic] (player, can be defended by, another player)
```

**txt11**

```
[video-level knowledge | semantic] (challenge, penalizes least baskets with, 100 sit-ups)
```

**txt12** (cited)

```
[video-level knowledge | semantic] (player, can gesture and talk to, another player)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 | ✓ | 00:34:45 | 00:34:40–00:34:50 | `-QuCz7kxBr8:visual:00344000` | `outputs/p9p19_check_20261025_141401/frames_s0/-QuCz7kxBr8/00344000.jpg` |
| img2 |  | 00:28:45 | 00:28:40–00:28:50 | `-QuCz7kxBr8:visual:00284000` | `outputs/p9p19_check_20261025_141401/frames_s0/-QuCz7kxBr8/00284000.jpg` |
| img3 | ✓ | 00:28:55 | 00:28:50–00:29:00 | `-QuCz7kxBr8:visual:00285000` | `outputs/p9p19_check_20261025_141401/frames_s0/-QuCz7kxBr8/00285000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1** (cited)

```
[00:34:40-00:34:50 | video frame at 2085.0s] On an outdoor basketball court under a clear blue sky, a player in a white jersey and orange shoes, carrying large cylindrical training pads, prepares to defend against another player in a black shirt and pink shorts who is dribbling a basketball. The defender shuffles laterally, maintaining a low stance, while the dribbler moves around him. Several other people are visible in the background, some standing and watching, others engaged in their own activities. The court features a blue painted area with "HYPE" written on it, and a basketball hoop is visible at one end. Mountains can be seen in the distance behind a low wall.
```

**img2**

```
[00:28:40-00:28:50 | video frame at 1725.0s] Six men stand on an outdoor basketball court under a clear blue sky. One man in the center holds a basketball and slightly shifts his position, while the others remain mostly stationary, facing him. The court has visible markings and a hoop in the background, with trees and hills visible beyond a fence. There is no audible content in this segment.
```

**img3** (cited)

```
[00:28:50-00:29:00 | video frame at 1735.0s] Six men are gathered on an outdoor basketball court under a clear blue sky. One man in the center, wearing a white hoodie and blue shorts, holds a basketball and gestures while speaking. The others stand around him, listening; some have their hands on their hips or heads, while one adjusts his hair. The camera briefly zooms in on a man in a black hoodie and white cap as he speaks, then returns to a wide shot of the group. The court has a painted logo, and a basketball hoop is visible in the background.
```
