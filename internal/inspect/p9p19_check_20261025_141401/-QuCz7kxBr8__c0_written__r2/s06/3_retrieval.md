# Section 6 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:19:41): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 21, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 5.63}`
- image request (2026-10-25 14:19:44): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 0.69}`
- L1 filter LLM call: prompt 8637 tokens, output 68 tokens, 4.5 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 10min | 00:00:00–00:10:00 | 1 / 0.04918 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10min_0` |
| txt2 | ✓ | worldmm-episodic | 3min | 00:00:00–00:03:00 | 2 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_0` |
| txt3 | ✓ | worldmm-episodic | 30sec | 00:04:30–00:05:00 | 3 / 0.032522 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_9` |
| txt4 |  | worldmm-episodic | 30sec | 00:08:00–00:08:30 | 4 / 0.032266 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_16` |
| txt5 | ✓ | worldmm-episodic | 3min | 00:06:00–00:09:00 | 5 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_2` |
| txt6 |  | worldmm-episodic | 30sec | 00:05:00–00:05:30 | 6 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_10` |
| txt7 |  | worldmm-episodic | 10sec | 00:08:20–00:08:30 | 7 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_50` |
| txt8 |  | worldmm-episodic | 30sec | 00:30:30–00:31:00 | 8 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_61` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_39` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_14` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_35` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016129 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_44` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

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

**txt2** (cited)

```
[00:00:00-00:03:00 | episodic 3min] Six men—Chris, Zach, Cass, James, Mitchell, and a sixth unnamed player—gather on a sunny outdoor basketball court to test 12 viral sports gadgets, splitting into two teams of three. Dressed in athletic wear, they introduce the challenge while holding basketballs near a hoop and trees. One man in a white hoodie addresses the camera, setting the tone with playful banter and audio cues like “Hands up, hands up” and “Mump is blinding me.” The scene transitions to a countdown and gear review, beginning with a close-up of black nylon straps, signaling the start of hands-on testing.

The group begins evaluating gadgets, starting with “SPORTS DRIBBLE SPECS.” One player dons the goggles and prepares for a dribbling time trial, where participants must dribble through three cones and touch a pole to stop the clock. Rules are clarified near a pool under bright sunlight, with the man in the hoodie confirming the forfeit rule for the slowest time. The drill proceeds with players like Chris and Zach showcasing speed and control, with timers capturing times like 10:85 and 9:51 seconds. Commentary highlights frustrations (“handles were definitely off”) and praise (“He’s making great time”), emphasizing the competitive yet casual atmosphere.

Later, the group discusses the gadget’s usefulness, with the man in the white hoodie expressing discomfort with traditional basketballs forcing him to look down. A score graphic flashes from 5 to 6, then 4, as teammates react with thumbs-up approval. The segment ends with the introduction of the SKLZ Dribble Stick—a black training tool with adjustable yellow arms—where the blue-jerseyed player prepares to demonstrate its use. Rules are reviewed: players dribble while avoiding the stick; the first to touch it runs five laps. The group is ready to begin, setting up for the next round of testing.
```

**txt3** (cited)

```
[00:04:30-00:05:00 | episodic 30sec] A man in a white hoodie demonstrates a black elbow strap called the “Straight Shooter Strap” on an outdoor basketball court, explaining how it stabilizes the elbow during shooting by preventing it from flaring outward. He gestures to the player’s arm and elbow while showing close-ups of the strap with on-screen text. A third observer watches closely as the demonstrator adjusts the strap on his own arm, then steps back to prepare for a shooting challenge with the other player holding the ball. The scene widens to reveal the full court, hoop, fence, and surrounding hills under a clear sky, setting up the practical application of the strap in a real-game context.
```

**txt4**

```
[00:08:00-00:08:30 | episodic 30sec] Three men on an outdoor basketball court prepare for a shooting challenge involving the Flick Glove — a device designed to improve basketball shooting technique. One man in a black hoodie and white cap, holding a basketball and the glove, explains the rules while gesturing, as the other two — one in a red hoodie and another in a blue jersey — observe. A text overlay instructs participants to take three shots with the glove, then three without, with the person making the fewest baskets required to do 100 sit-ups. The man in the red hoodie expresses confusion about the glove’s orientation, prompting the man in the black hoodie to demonstrate its use. The video opens with a close-up of the glove’s design — featuring finger loops and a rectangular screen — and later displays the three available color options (white, black, orange) with the brand name “FLICK GLOVE” overlaid, establishing the product’s purpose and setup for the upcoming demonstration.
```

**txt5** (cited)

```
[00:06:00-00:09:00 | episodic 3min] A man in a white hoodie and patterned shorts shoots basketballs on a sunny court, with a score counter updating after each shot — from 0/0 to 3/5 — while a humorous voiceover references product ownership and investment. He praises the product as “great,” with a “#NOT SPONSORED” graphic. The scene cuts to another player resetting the score.

A second player makes a shot (1/2), but audio commentary criticizes the product’s performance, noting it “fell off” and “snaps” when extended. A shooting contest unfolds: a player in a red and white jersey (No. 2) makes a successful shot (2/5), celebrated with surprise and joy. Later, the tie-dye jersey player loses, prompting the white-shirted man to propose testing his jump shot without the strap to isolate the issue — a playful, lighthearted challenge.

His jump shot misses, sparking frustration and speculation about the strap. A teammate confirms the issue, and a forfeit of 30 jumping jacks is suggested. The man begins doing jumping jacks, arms raised, while two others watch and tease — one jokes about “bouncing titties,” another compares chest sizes. He deflects with humor, “Bro, I’m wearing a big shirt.” His movements become off-rhythm, drawing amused observation.

Three men discuss and humorously rate the product: the white-hoodie man (ZHYPE) calls it suitable for kids but suggests a better gadget for beginners, scoring it “1.” They escalate to exaggerated scoring — “1,” “2,” then “-3k” — ending with a playful “what’s the next invention?” 

A shooting challenge with the Flick Glove begins: one man in a black hoodie explains rules — three shots with the glove, then without — with the fewest baskets requiring 100 sit-ups. The red-hoodie man misunderstands the glove’s orientation, prompting a demonstration. The glove’s design (finger loops, screen) and color options (white, black, orange) are shown.

Three men demonstrate basketball drills under sunny skies, with the blue-jersey man explaining movement techniques. A shot by the black-hoodie man is debated — “too far,” “cheating.” Later, he makes another shot, celebrated with “Woo!” and “WHOOOOOO” graphics, emphasizing triumph and energy.
```

**txt6**

```
[00:05:00-00:05:30 | episodic 30sec] A player in a white shirt and patterned shorts shoots a basketball on an outdoor court, successfully making the shot as the ball arcs through the hoop; the camera captures the ball entering the net and cuts to the shooter looking on, while the scoreboard briefly shows “0/1” as a player in a white jersey walks toward them.

The same shooter attempts multiple more shots, missing several, with the scoreboard updating from 0/1 to 0/3. A person in a red and white jersey stands nearby holding a ball and observing, while another in a white shirt and blue shorts stands near the hoop. The shooter pauses, inspecting their elbow, seemingly questioning its positioning, before the segment ends.

Continuing on the same court, the shooter takes additional shots, with a score counter tracking each attempt. A person in a white hoodie stands nearby, reacting to the misses. Audio includes dialogue expressing frustration and self-deprecation, including phrases like “I’m just bad” and “It’s throwing me off, you know?”
```

**txt7**

```
[00:08:20-00:08:30 | episodic 10sec] Three men stand on an outdoor basketball court. A text overlay explains a challenge: take three shots with a flick glove, then three without, and the person making the least baskets must do 100 sit-ups. One man in a red hoodie reacts with surprise, while another in a blue jersey smiles. The third man, wearing a black hoodie and cap, holds a basketball and a black glove, examining it. The man in the red hoodie asks, “Bro, what are these? Which way does it even go?” as the man in the black hoodie holds up the glove.
```

**txt8**

```
[00:30:30-00:31:00 | episodic 30sec] **[Event 1: Play Initiation and Celebration]**  
Under a clear blue sky with mountains in the background, three men are on an outdoor basketball court. The man in the white “2HYPE” hoodie and blue shorts laughs, then performs a high kick while dribbling a basketball. His teammate in the tie-dye “2HYPE” jersey raises his arm in celebration, while the third man in a black shirt observes. A “1-0” graphic appears as the white-hoodie player attempts a shot, drawing the attention of a defender in a black hoodie with a protective pad on his arm.

**[Event 2: Shot Execution and Defensive Engagement]**  
The white-hoodie player successfully makes the shot, and the defender in the black hoodie walks away. The scene shifts to another play: the white-shirted shooter attempts a shot while the black-hoodie defender, equipped with large padded training shields, moves in to contest. Other players observe from around the court, which features a blue “HYPE” painted area, surrounded by trees, a fence, and distant hills.

**[Event 3: Training Segment and Score Display]**  
The black-hoodie player, wearing a white cap and carrying training pads, turns to the camera and smiles. The white-hoodie player, now in patterned shorts, steps forward holding pads and a basketball, preparing to shoot. The black-hoodie player watches. The “1-0” graphic remains on screen, reinforcing the score. Background figures, some holding cameras, suggest this is a filmed training session or game.
```

**txt9**

```
[video-level knowledge | semantic] (on-screen text, reads, MOST DRIBBLES IN 15 SECONDS)
```

**txt10**

```
[video-level knowledge | semantic] (player, uses, Straight Shooter Strap)
```

**txt11**

```
[video-level knowledge | semantic] (Flick Gloves, displayed on, white surface)
```

**txt12**

```
[video-level knowledge | semantic] (The text overlay, reads, 20 LOW, MEDIUM, & HIGH DRIBBLES IN 60 SECONDS)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:34:45 | 00:34:40–00:34:50 | `-QuCz7kxBr8:visual:00344000` | `outputs/p9p19_check_20261025_141401/frames_s3/-QuCz7kxBr8/00344000.jpg` |
| img2 |  | 00:24:05 | 00:24:00–00:24:10 | `-QuCz7kxBr8:visual:00240000` | `outputs/p9p19_check_20261025_141401/frames_s3/-QuCz7kxBr8/00240000.jpg` |
| img3 |  | 00:17:25 | 00:17:20–00:17:30 | `-QuCz7kxBr8:visual:00172000` | `outputs/p9p19_check_20261025_141401/frames_s3/-QuCz7kxBr8/00172000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:34:40-00:34:50 | video frame at 2085.0s] On an outdoor basketball court under a clear blue sky, a player in a white jersey and orange shoes, carrying large cylindrical training pads, prepares to defend against another player in a black shirt and pink shorts who is dribbling a basketball. The defender shuffles laterally, maintaining a low stance, while the dribbler moves around him. Several other people are visible in the background, some standing and watching, others engaged in their own activities. The court features a blue painted area with "HYPE" written on it, and a basketball hoop is visible at one end. Mountains can be seen in the distance behind a low wall.
```

**img2**

```
[00:24:00-00:24:10 | video frame at 1445.0s] On an outdoor basketball court, three men are interacting. One man in a white t-shirt and patterned shorts holds a basketball and gestures while speaking. Another man in a white hoodie and blue shorts holds the ball up, then raises it above his head. A third man in a red and white basketball jersey stands nearby, watching and occasionally gesturing. The scene is set on a sunny day with mountains visible in the background and a residential building nearby. There is no audible dialogue in this segment.
```

**img3**

```
[00:17:20-00:17:30 | video frame at 1045.0s] Three men are standing on an outdoor basketball court in front of a large house. One man in a white hoodie and patterned shorts holds a basketball and gestures with it while speaking. Another man in a basketball jersey stands beside him, and a third man in a white t-shirt stands with his arms crossed, watching. The scene is bright and sunny, with a basketball hoop visible in the background.
```
