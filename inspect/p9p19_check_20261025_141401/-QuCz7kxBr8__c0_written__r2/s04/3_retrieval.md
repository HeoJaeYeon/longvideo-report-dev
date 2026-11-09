# Section 4 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:18:09): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 22, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 6.17}`
- image request (2026-10-25 14:18:12): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 0.6}`
- L1 filter LLM call: prompt 9907 tokens, output 69 tokens, 5.0 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 3min | 00:03:00–00:06:00 | 1 / 0.032787 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_1` |
| txt2 | ✓ | worldmm-episodic | 3min | 00:06:00–00:09:00 | 2 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_2` |
| txt3 | ✓ | worldmm-episodic | 30sec | 00:07:00–00:07:30 | 3 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_14` |
| txt4 | ✓ | worldmm-episodic | 10sec | 00:07:20–00:07:30 | 4 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_44` |
| txt5 | ✓ | worldmm-episodic | 10sec | 00:07:10–00:07:20 | 5 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_43` |
| txt6 | ✓ | worldmm-episodic | 10sec | 00:07:00–00:07:10 | 6 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_42` |
| txt7 | ✓ | worldmm-episodic | 30sec | 00:04:30–00:05:00 | 7 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_9` |
| txt8 | ✓ | worldmm-episodic | 10sec | 00:04:30–00:04:40 | 8 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_27` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.032018 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_36` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_14` |
| txt11 | ✓ | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_17` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016129 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_60` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:03:00-00:06:00 | episodic 3min] Three men gather on an outdoor basketball court, negotiating positions before settling into a shooting challenge. One man in a black hoodie and white cap adjusts a basketball on a training device while the others—wearing red and blue jerseys—observe, holding balls. A fourth person films the scene under clear skies, with trees and a fence in the background. The group transitions to a hoop with a vertical obstacle, where they take turns shooting under a 30-second countdown. Encouragement and light-hearted banter—such as “you might be safe just making it past that first one”—add to the casual yet competitive tone. The man in the black hoodie successfully makes his shot, smiling as he walks back, while the man in red watches amusedly. Their conversation hints at past forfeits and humorous self-deprecation.

The group then evaluates a dribble stick, with the man in the blue jersey rating it an 8/10, followed by the man in the black shirt agreeing, and the man in the black hoodie giving it a 7—joking that anything helping him fail is “pretty good.” The conversation remains lighthearted and collaborative.

Later, a man in a white hoodie demonstrates the “Straight Shooter Strap,” explaining how it stabilizes the elbow during shooting. He adjusts the strap on his arm while a third observer watches. The scene widens to show the full court, hoop, and surrounding hills under clear skies, setting up practical use of the device.

A shooter in a white shirt and patterned shorts begins a shooting sequence, initially making one shot (0/1), then missing several, with the scoreboard climbing to 0/3. He pauses, inspecting his elbow, seemingly frustrated. As the sequence continues, he scores more shots, pushing the tally to 3/16, with teammates retrieving balls and commentary tracking each attempt. The scoreboard climbs steadily, accompanied by remarks like “Dude, 15,” and “Zach’s uses this thing, bro.” The player smiles at the camera as he approaches 15 successful shots, with the backdrop of a large house and trees under clear skies.
```

**txt2** (cited)

```
[00:06:00-00:09:00 | episodic 3min] A man in a white hoodie and patterned shorts shoots basketballs on a sunny court, with a score counter updating after each shot — from 0/0 to 3/5 — while a humorous voiceover references product ownership and investment. He praises the product as “great,” with a “#NOT SPONSORED” graphic. The scene cuts to another player resetting the score.

A second player makes a shot (1/2), but audio commentary criticizes the product’s performance, noting it “fell off” and “snaps” when extended. A shooting contest unfolds: a player in a red and white jersey (No. 2) makes a successful shot (2/5), celebrated with surprise and joy. Later, the tie-dye jersey player loses, prompting the white-shirted man to propose testing his jump shot without the strap to isolate the issue — a playful, lighthearted challenge.

His jump shot misses, sparking frustration and speculation about the strap. A teammate confirms the issue, and a forfeit of 30 jumping jacks is suggested. The man begins doing jumping jacks, arms raised, while two others watch and tease — one jokes about “bouncing titties,” another compares chest sizes. He deflects with humor, “Bro, I’m wearing a big shirt.” His movements become off-rhythm, drawing amused observation.

Three men discuss and humorously rate the product: the white-hoodie man (ZHYPE) calls it suitable for kids but suggests a better gadget for beginners, scoring it “1.” They escalate to exaggerated scoring — “1,” “2,” then “-3k” — ending with a playful “what’s the next invention?” 

A shooting challenge with the Flick Glove begins: one man in a black hoodie explains rules — three shots with the glove, then without — with the fewest baskets requiring 100 sit-ups. The red-hoodie man misunderstands the glove’s orientation, prompting a demonstration. The glove’s design (finger loops, screen) and color options (white, black, orange) are shown.

Three men demonstrate basketball drills under sunny skies, with the blue-jersey man explaining movement techniques. A shot by the black-hoodie man is debated — “too far,” “cheating.” Later, he makes another shot, celebrated with “Woo!” and “WHOOOOOO” graphics, emphasizing triumph and energy.
```

**txt3** (cited)

```
[00:07:00-00:07:30 | episodic 30sec] A player in a white shirt and patterned shorts attempts a jump shot that misses, prompting frustration and speculation about whether his shot is broken or if the strap caused the miss. His teammate confirms the issue, and another asks what the forfeit is, leading the player to suggest 30 jumping jacks as punishment. The group gathers near the hoop, holding basketballs and engaging in lighthearted banter.

The man in the white shirt begins doing jumping jacks, raising his arms with each bounce, while the other two—wearing a red and white jersey and a white hoodie—watch. Teasing ensues, with one observer joking, “Bounce some titties, boy,” and later comparing chest sizes, saying, “Jadil got a bigger chest than you.” The man in the white shirt deflects with humor, replying, “Bro, I'm wearing a big shirt.”

As he continues the jumping jacks, his movements become off-rhythm, with his feet moving out of sync with his hands, drawing amused observation from the two onlookers, one in a tie-dye jersey commenting on his shirt size and the other continuing the playful ribbing. The scene remains casual and humorous, centered on camaraderie and light-hearted teasing on the court.
```

**txt4** (cited)

```
[00:07:20-00:07:30 | episodic 10sec] Three men are on an outdoor basketball court. One man in a white t-shirt and patterned shorts is performing jumping jacks while two others watch. One of the watchers, in a tie-dye jersey, comments on the man’s shirt size, and another jokes about his chest. The man doing jumping jacks is off rhythm, with his feet moving out of sync with his hands, as noted by the observers.
```

**txt5** (cited)

```
[00:07:10-00:07:20 | episodic 10sec] Three men are on an outdoor basketball court. One man in a white shirt and patterned shorts begins doing jumping jacks, raising his arms with each bounce. The other two men, one in a red and white jersey and another in a white hoodie, watch him. The man doing the jumping jacks is jokingly teased about his chest size by the others, with one of them saying, “Bounce some titties, boy,” and later, “Jadil got a bigger chest than you.” The man in the white shirt responds, “Bro, I'm wearing a big shirt.”
```

**txt6** (cited)

```
[00:07:00-00:07:10 | episodic 10sec] On a sunny day at an outdoor basketball court, a player in a white shirt and patterned shorts attempts a jump shot, then turns to his teammates after the ball misses the basket. He expresses frustration, questioning whether his jump shot is broken or if it was the strap. A teammate responds affirmatively, and another asks what the forfeit is, prompting the player to suggest doing 30 jumping jacks. The group, including a player in a red and white jersey and another in a white jersey, gathers near the hoop, holding basketballs and engaging in conversation.
```

**txt7** (cited)

```
[00:04:30-00:05:00 | episodic 30sec] A man in a white hoodie demonstrates a black elbow strap called the “Straight Shooter Strap” on an outdoor basketball court, explaining how it stabilizes the elbow during shooting by preventing it from flaring outward. He gestures to the player’s arm and elbow while showing close-ups of the strap with on-screen text. A third observer watches closely as the demonstrator adjusts the strap on his own arm, then steps back to prepare for a shooting challenge with the other player holding the ball. The scene widens to reveal the full court, hoop, fence, and surrounding hills under a clear sky, setting up the practical application of the strap in a real-game context.
```

**txt8** (cited)

```
[00:04:30-00:04:40 | episodic 10sec] Three men are on an outdoor basketball court. One man in a white hoodie holds a basketball and demonstrates a black strap called the "Straight Shooter Strap," explaining its use while the other two watch. The strap is shown in close-up with text overlay.
```

**txt9**

```
[video-level knowledge | semantic] (challenge, penalizes least baskets with, 100 sit-ups)
```

**txt10**

```
[video-level knowledge | semantic] (player, uses, Straight Shooter Strap)
```

**txt11** (cited)

```
[video-level knowledge | semantic] (man doing jumping jacks, is teased about, chest size)
```

**txt12**

```
[video-level knowledge | semantic] (Table, has, Straight Shooter Strap)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:34:45 | 00:34:40–00:34:50 | `-QuCz7kxBr8:visual:00344000` | `outputs/p9p19_check_20261025_141401/frames_s3/-QuCz7kxBr8/00344000.jpg` |
| img2 |  | 00:32:05 | 00:32:00–00:32:10 | `-QuCz7kxBr8:visual:00320000` | `outputs/p9p19_check_20261025_141401/frames_s3/-QuCz7kxBr8/00320000.jpg` |
| img3 |  | 00:30:25 | 00:30:20–00:30:30 | `-QuCz7kxBr8:visual:00302000` | `outputs/p9p19_check_20261025_141401/frames_s3/-QuCz7kxBr8/00302000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:34:40-00:34:50 | video frame at 2085.0s] On an outdoor basketball court under a clear blue sky, a player in a white jersey and orange shoes, carrying large cylindrical training pads, prepares to defend against another player in a black shirt and pink shorts who is dribbling a basketball. The defender shuffles laterally, maintaining a low stance, while the dribbler moves around him. Several other people are visible in the background, some standing and watching, others engaged in their own activities. The court features a blue painted area with "HYPE" written on it, and a basketball hoop is visible at one end. Mountains can be seen in the distance behind a low wall.
```

**img2**

```
[00:32:00-00:32:10 | video frame at 1925.0s] On an outdoor basketball court under a clear blue sky, two players are engaged in a game. One player in a blue jersey dribbles the ball while being guarded by a player in a white shirt. The player in white attempts a shot, successfully making the basket. After the shot, both players celebrate, with the player in white raising his arms in triumph. Other individuals are visible on the sidelines, watching the game. The court features a blue painted area with the word "HYPE" written on it, and a basketball hoop stands at one end. Mountains are visible in the background.
```

**img3**

```
[00:30:20-00:30:30 | video frame at 1825.0s] A young man in a blue jersey is seen on an outdoor basketball court, looking down at his hands. The scene then shifts to show him in a white t-shirt and patterned shorts, dribbling a basketball while being guarded by a man in a black hoodie holding large foam pads. The man in the white shirt moves to shoot the ball as the defender raises his pads to block. Other individuals are present on the court, and the setting includes a residential house, a pool, and mountains in the background under a clear blue sky.
```
