# Section 2 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:16:35): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 22, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 5.86}`
- image request (2026-10-25 14:16:38): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 1.24}`
- L1 filter LLM call: prompt 9055 tokens, output 69 tokens, 4.7 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 10min | 00:00:00–00:10:00 | 1 / 0.04918 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10min_0` |
| txt2 | ✓ | worldmm-episodic | 3min | 00:03:00–00:06:00 | 2 / 0.048652 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_1` |
| txt3 | ✓ | worldmm-episodic | 30sec | 00:02:30–00:03:00 | 3 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_5` |
| txt4 | ✓ | worldmm-episodic | 10sec | 00:02:50–00:03:00 | 4 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_17` |
| txt5 | ✓ | worldmm-episodic | 10sec | 00:02:40–00:02:50 | 5 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_16` |
| txt6 | ✓ | worldmm-episodic | 30sec | 00:04:30–00:05:00 | 6 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_9` |
| txt7 | ✓ | worldmm-episodic | 10sec | 00:07:20–00:07:30 | 7 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_44` |
| txt8 | ✓ | worldmm-episodic | 30sec | 00:07:00–00:07:30 | 8 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_14` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.031258 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_121` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_39` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_14` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_20` |

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
[00:03:00-00:06:00 | episodic 3min] Three men gather on an outdoor basketball court, negotiating positions before settling into a shooting challenge. One man in a black hoodie and white cap adjusts a basketball on a training device while the others—wearing red and blue jerseys—observe, holding balls. A fourth person films the scene under clear skies, with trees and a fence in the background. The group transitions to a hoop with a vertical obstacle, where they take turns shooting under a 30-second countdown. Encouragement and light-hearted banter—such as “you might be safe just making it past that first one”—add to the casual yet competitive tone. The man in the black hoodie successfully makes his shot, smiling as he walks back, while the man in red watches amusedly. Their conversation hints at past forfeits and humorous self-deprecation.

The group then evaluates a dribble stick, with the man in the blue jersey rating it an 8/10, followed by the man in the black shirt agreeing, and the man in the black hoodie giving it a 7—joking that anything helping him fail is “pretty good.” The conversation remains lighthearted and collaborative.

Later, a man in a white hoodie demonstrates the “Straight Shooter Strap,” explaining how it stabilizes the elbow during shooting. He adjusts the strap on his arm while a third observer watches. The scene widens to show the full court, hoop, and surrounding hills under clear skies, setting up practical use of the device.

A shooter in a white shirt and patterned shorts begins a shooting sequence, initially making one shot (0/1), then missing several, with the scoreboard climbing to 0/3. He pauses, inspecting his elbow, seemingly frustrated. As the sequence continues, he scores more shots, pushing the tally to 3/16, with teammates retrieving balls and commentary tracking each attempt. The scoreboard climbs steadily, accompanied by remarks like “Dude, 15,” and “Zach’s uses this thing, bro.” The player smiles at the camera as he approaches 15 successful shots, with the backdrop of a large house and trees under clear skies.
```

**txt3** (cited)

```
[00:02:30-00:03:00 | episodic 30sec] Three men gather on an outdoor basketball court, preparing for a dribbling challenge using a SKLZ Dribble Stick. The man in the red hoodie introduces the game, asking if they want to see how the dribble stick works, while the man in the blue jersey prepares to demonstrate it. The device—a black training tool with adjustable yellow arms and “DRIBBLE STICK” branding—is shown in detail before the group assembles, each holding a basketball, to review the rules: players take turns dribbling while avoiding contact with the stick; the person who fails first must run five laps around the court. The group is ready to begin, with the blue-jerseyed player poised to lead the demonstration.
```

**txt4** (cited)

```
[00:02:50-00:03:00 | episodic 10sec] A close-up shot shows a black "Dribble Stick" device with a yellow logo. The scene then transitions to an outdoor basketball court where three men are gathered. One man in a red hoodie holds a basketball and a white device, while another in a blue jersey and a third in a black hoodie and white cap each hold basketballs. They appear to be reviewing rules or scores on the device, preparing for a dribbling challenge. The audio explains the game: participants take turns using the dribble stick to see who can go the longest without hitting it, and the person with the shortest time must run five laps around the court.
```

**txt5** (cited)

```
[00:02:40-00:02:50 | episodic 10sec] A man in a red hoodie holds a basketball while standing on a basketball court with two other men, one in a blue jersey and another in a black shirt and cap. The scene transitions to a close-up of a black training device labeled "DRIBBLE STICK" by SKLZ, showing its adjustable yellow arms and base. The camera pans around the device, highlighting its construction and branding.
```

**txt6** (cited)

```
[00:04:30-00:05:00 | episodic 30sec] A man in a white hoodie demonstrates a black elbow strap called the “Straight Shooter Strap” on an outdoor basketball court, explaining how it stabilizes the elbow during shooting by preventing it from flaring outward. He gestures to the player’s arm and elbow while showing close-ups of the strap with on-screen text. A third observer watches closely as the demonstrator adjusts the strap on his own arm, then steps back to prepare for a shooting challenge with the other player holding the ball. The scene widens to reveal the full court, hoop, fence, and surrounding hills under a clear sky, setting up the practical application of the strap in a real-game context.
```

**txt7** (cited)

```
[00:07:20-00:07:30 | episodic 10sec] Three men are on an outdoor basketball court. One man in a white t-shirt and patterned shorts is performing jumping jacks while two others watch. One of the watchers, in a tie-dye jersey, comments on the man’s shirt size, and another jokes about his chest. The man doing jumping jacks is off rhythm, with his feet moving out of sync with his hands, as noted by the observers.
```

**txt8** (cited)

```
[00:07:00-00:07:30 | episodic 30sec] A player in a white shirt and patterned shorts attempts a jump shot that misses, prompting frustration and speculation about whether his shot is broken or if the strap caused the miss. His teammate confirms the issue, and another asks what the forfeit is, leading the player to suggest 30 jumping jacks as punishment. The group gathers near the hoop, holding basketballs and engaging in lighthearted banter.

The man in the white shirt begins doing jumping jacks, raising his arms with each bounce, while the other two—wearing a red and white jersey and a white hoodie—watch. Teasing ensues, with one observer joking, “Bounce some titties, boy,” and later comparing chest sizes, saying, “Jadil got a bigger chest than you.” The man in the white shirt deflects with humor, replying, “Bro, I'm wearing a big shirt.”

As he continues the jumping jacks, his movements become off-rhythm, with his feet moving out of sync with his hands, drawing amused observation from the two onlookers, one in a tie-dye jersey commenting on his shirt size and the other continuing the playful ribbing. The scene remains casual and humorous, centered on camaraderie and light-hearted teasing on the court.
```

**txt9**

```
[video-level knowledge | semantic] (player, can dribble, basketball)
```

**txt10**

```
[video-level knowledge | semantic] (on-screen text, reads, MOST DRIBBLES IN 15 SECONDS)
```

**txt11**

```
[video-level knowledge | semantic] (player, uses, Straight Shooter Strap)
```

**txt12**

```
[video-level knowledge | semantic] (Jadil, has bigger chest than, man doing jumping jacks)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:02:55 | 00:02:50–00:03:00 | `-QuCz7kxBr8:visual:00025000` | `outputs/p9p19_check_20261025_141401/frames_s0/-QuCz7kxBr8/00025000.jpg` |
| img2 |  | 00:15:35 | 00:15:30–00:15:40 | `-QuCz7kxBr8:visual:00153000` | `outputs/p9p19_check_20261025_141401/frames_s0/-QuCz7kxBr8/00153000.jpg` |
| img3 |  | 00:22:15 | 00:22:10–00:22:20 | `-QuCz7kxBr8:visual:00221000` | `outputs/p9p19_check_20261025_141401/frames_s0/-QuCz7kxBr8/00221000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:02:50-00:03:00 | video frame at 175.0s] A close-up shot shows a black "Dribble Stick" device with a yellow logo. The scene then transitions to an outdoor basketball court where three men are gathered. One man in a red hoodie holds a basketball and a white device, while another in a blue jersey and a third in a black hoodie and white cap each hold basketballs. They appear to be reviewing rules or scores on the device, preparing for a dribbling challenge. The audio explains the game: participants take turns using the dribble stick to see who can go the longest without hitting it, and the person with the shortest time must run five laps around the court.
```

**img2**

```
[00:15:30-00:15:40 | video frame at 935.0s] On an outdoor basketball court, a man with blonde hair wearing a black t-shirt and gloves dribbles a basketball, then stops and holds it while conversing with a man in a black hoodie and white cap. A third man in a blue basketball jersey stands nearby, observing. The scene takes place on a sunny day with trees and a fence in the background.
```

**img3**

```
[00:22:10-00:22:20 | video frame at 1335.0s] A man with blond hair, wearing a black t-shirt and pink shorts, is on an outdoor basketball court. He holds a basketball, takes a shot, and watches it fly toward the hoop. After the shot, he turns and walks toward the camera, then stops to look down at his hands, which have a wristband. In the background, other people are visible on the court and in the surrounding area, which includes trees, a patio, and a house. The sky is blue with some clouds.
```
