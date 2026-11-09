# Section 5 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:18:53): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 20, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 5.78}`
- image request (2026-10-25 14:18:55): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 0.61}`
- L1 filter LLM call: prompt 9001 tokens, output 71 tokens, 4.7 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 30sec | 00:08:00–00:08:30 | 1 / 0.04918 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_16` |
| txt2 | ✓ | worldmm-episodic | 10min | 00:00:00–00:10:00 | 2 / 0.04918 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10min_0` |
| txt3 | ✓ | worldmm-episodic | 3min | 00:06:00–00:09:00 | 3 / 0.032787 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_2` |
| txt4 | ✓ | worldmm-episodic | 10sec | 00:08:20–00:08:30 | 4 / 0.032522 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_50` |
| txt5 | ✓ | worldmm-episodic | 10sec | 00:08:10–00:08:20 | 5 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_49` |
| txt6 | ✓ | worldmm-episodic | 30sec | 00:30:30–00:31:00 | 6 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_61` |
| txt7 | ✓ | worldmm-episodic | 30sec | 00:10:30–00:11:00 | 7 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_21` |
| txt8 | ✓ | worldmm-episodic | 10sec | 00:10:40–00:10:50 | 8 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_64` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.032787 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_36` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.032258 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_44` |
| txt11 | ✓ | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_35` |
| txt12 | ✓ | worldmm-semantic | — | no timestamp | 4 / 0.016129 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_32` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:08:00-00:08:30 | episodic 30sec] Three men on an outdoor basketball court prepare for a shooting challenge involving the Flick Glove — a device designed to improve basketball shooting technique. One man in a black hoodie and white cap, holding a basketball and the glove, explains the rules while gesturing, as the other two — one in a red hoodie and another in a blue jersey — observe. A text overlay instructs participants to take three shots with the glove, then three without, with the person making the fewest baskets required to do 100 sit-ups. The man in the red hoodie expresses confusion about the glove’s orientation, prompting the man in the black hoodie to demonstrate its use. The video opens with a close-up of the glove’s design — featuring finger loops and a rectangular screen — and later displays the three available color options (white, black, orange) with the brand name “FLICK GLOVE” overlaid, establishing the product’s purpose and setup for the upcoming demonstration.
```

**txt2** (cited)

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

**txt3** (cited)

```
[00:06:00-00:09:00 | episodic 3min] A man in a white hoodie and patterned shorts shoots basketballs on a sunny court, with a score counter updating after each shot — from 0/0 to 3/5 — while a humorous voiceover references product ownership and investment. He praises the product as “great,” with a “#NOT SPONSORED” graphic. The scene cuts to another player resetting the score.

A second player makes a shot (1/2), but audio commentary criticizes the product’s performance, noting it “fell off” and “snaps” when extended. A shooting contest unfolds: a player in a red and white jersey (No. 2) makes a successful shot (2/5), celebrated with surprise and joy. Later, the tie-dye jersey player loses, prompting the white-shirted man to propose testing his jump shot without the strap to isolate the issue — a playful, lighthearted challenge.

His jump shot misses, sparking frustration and speculation about the strap. A teammate confirms the issue, and a forfeit of 30 jumping jacks is suggested. The man begins doing jumping jacks, arms raised, while two others watch and tease — one jokes about “bouncing titties,” another compares chest sizes. He deflects with humor, “Bro, I’m wearing a big shirt.” His movements become off-rhythm, drawing amused observation.

Three men discuss and humorously rate the product: the white-hoodie man (ZHYPE) calls it suitable for kids but suggests a better gadget for beginners, scoring it “1.” They escalate to exaggerated scoring — “1,” “2,” then “-3k” — ending with a playful “what’s the next invention?” 

A shooting challenge with the Flick Glove begins: one man in a black hoodie explains rules — three shots with the glove, then without — with the fewest baskets requiring 100 sit-ups. The red-hoodie man misunderstands the glove’s orientation, prompting a demonstration. The glove’s design (finger loops, screen) and color options (white, black, orange) are shown.

Three men demonstrate basketball drills under sunny skies, with the blue-jersey man explaining movement techniques. A shot by the black-hoodie man is debated — “too far,” “cheating.” Later, he makes another shot, celebrated with “Woo!” and “WHOOOOOO” graphics, emphasizing triumph and energy.
```

**txt4** (cited)

```
[00:08:20-00:08:30 | episodic 10sec] Three men stand on an outdoor basketball court. A text overlay explains a challenge: take three shots with a flick glove, then three without, and the person making the least baskets must do 100 sit-ups. One man in a red hoodie reacts with surprise, while another in a blue jersey smiles. The third man, wearing a black hoodie and cap, holds a basketball and a black glove, examining it. The man in the red hoodie asks, “Bro, what are these? Which way does it even go?” as the man in the black hoodie holds up the glove.
```

**txt5** (cited)

```
[00:08:10-00:08:20 | episodic 10sec] The video displays three colored Flick Gloves — white, black, and orange — arranged on a white surface, with the text "FLICK GLOVE" overlaid. The scene then transitions to an outdoor basketball court where three men stand, one holding a basketball. A text overlay instructs viewers to "TAKE 3 SHOT WITH FLICK GLOVE THEN 3 SHOTS WITHOUT," indicating an upcoming demonstration of the glove's use for improving shooting technique.
```

**txt6** (cited)

```
[00:30:30-00:31:00 | episodic 30sec] **[Event 1: Play Initiation and Celebration]**  
Under a clear blue sky with mountains in the background, three men are on an outdoor basketball court. The man in the white “2HYPE” hoodie and blue shorts laughs, then performs a high kick while dribbling a basketball. His teammate in the tie-dye “2HYPE” jersey raises his arm in celebration, while the third man in a black shirt observes. A “1-0” graphic appears as the white-hoodie player attempts a shot, drawing the attention of a defender in a black hoodie with a protective pad on his arm.

**[Event 2: Shot Execution and Defensive Engagement]**  
The white-hoodie player successfully makes the shot, and the defender in the black hoodie walks away. The scene shifts to another play: the white-shirted shooter attempts a shot while the black-hoodie defender, equipped with large padded training shields, moves in to contest. Other players observe from around the court, which features a blue “HYPE” painted area, surrounded by trees, a fence, and distant hills.

**[Event 3: Training Segment and Score Display]**  
The black-hoodie player, wearing a white cap and carrying training pads, turns to the camera and smiles. The white-hoodie player, now in patterned shorts, steps forward holding pads and a basketball, preparing to shoot. The black-hoodie player watches. The “1-0” graphic remains on screen, reinforcing the score. Background figures, some holding cameras, suggest this is a filmed training session or game.
```

**txt7** (cited)

```
[00:10:30-00:11:00 | episodic 30sec] A young man in a blue jersey successfully makes two consecutive basketball shots on an outdoor court, then celebrates as on-screen text reads “4 MADE BASKETS,” while two observers—one in a red shirt and another in a black shirt—watch nearby.

Separately, a man in a black hoodie, grey pants, white cap, and black sneakers performs sit-ups on the same court under bright sunlight, with the text “CASH LOST” overlaid. The scene includes a grassy background with rocks and outdoor equipment, and a voiceover explains that “cash made the least amount of flick shots therefore he has to do sit-ups.”

In a related scene, the same man continues sit-ups on a concrete court, while a blonde-bearded man in a red hoodie stands nearby and speaks animatedly, his expressive face captured in close-up, against a backdrop of clear blue skies and greenery.
```

**txt8** (cited)

```
[00:10:40-00:10:50 | episodic 10sec] A man in a black hoodie and grey pants is performing sit-ups on a basketball court, with the text "CASH LOST" overlaid on the video. He is wearing a white cap and black sneakers. In the background, there is a grassy area with rocks, a hose, and some outdoor equipment. The scene is outdoors under bright sunlight, and the court has blue and grey painted sections. The audio includes a voiceover stating, "ah so cash made the least amount of flick shots therefore he has to do sit-ups."
```

**txt9**

```
[video-level knowledge | semantic] (challenge, penalizes least baskets with, 100 sit-ups)
```

**txt10**

```
[video-level knowledge | semantic] (The text overlay, reads, 20 LOW, MEDIUM, & HIGH DRIBBLES IN 60 SECONDS)
```

**txt11** (cited)

```
[video-level knowledge | semantic] (Flick Gloves, displayed on, white surface)
```

**txt12** (cited)

```
[video-level knowledge | semantic] (Flick Gloves, has colors, white)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:11:05 | 00:11:00–00:11:10 | `-QuCz7kxBr8:visual:00110000` | `outputs/p9p19_check_20261025_141401/frames_s3/-QuCz7kxBr8/00110000.jpg` |
| img2 |  | 00:08:25 | 00:08:20–00:08:30 | `-QuCz7kxBr8:visual:00082000` | `outputs/p9p19_check_20261025_141401/frames_s3/-QuCz7kxBr8/00082000.jpg` |
| img3 |  | 00:00:15 | 00:00:10–00:00:20 | `-QuCz7kxBr8:visual:00001000` | `outputs/p9p19_check_20261025_141401/frames_s3/-QuCz7kxBr8/00001000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:11:00-00:11:10 | video frame at 665.0s] A man in a black hoodie and grey sweatpants is doing sit-ups on a concrete court outdoors. He starts lying on his back with his hands behind his head, then sits up and lowers himself back down. Another man in a blue basketball jersey with the word "SHY" and the number "2" stands nearby, smiling. The setting includes a grassy area, rocks, and a basketball hoop.
```

**img2**

```
[00:08:20-00:08:30 | video frame at 505.0s] Three men stand on an outdoor basketball court. A text overlay explains a challenge: take three shots with a flick glove, then three without, and the person making the least baskets must do 100 sit-ups. One man in a red hoodie reacts with surprise, while another in a blue jersey smiles. The third man, wearing a black hoodie and cap, holds a basketball and a black glove, examining it. The man in the red hoodie asks, “Bro, what are these? Which way does it even go?” as the man in the black hoodie holds up the glove.
```

**img3**

```
[00:00:10-00:00:20 | video frame at 15.0s] On an outdoor basketball court, a group of men gather with basketballs. One man in a blue jersey crouches near a training device, then stands up and looks upward. The camera shifts to show a man in a black hoodie and cap, holding a basketball and speaking animatedly to the group. The scene transitions to a close-up of three black nylon straps with buckles, laid out on a white surface. Audio includes a greeting, a countdown, an exclamation, and an introduction to a video segment about testing viral basketball gadgets.
```
