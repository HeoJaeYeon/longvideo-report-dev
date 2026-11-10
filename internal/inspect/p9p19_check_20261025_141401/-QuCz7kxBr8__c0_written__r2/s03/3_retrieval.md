# Section 3 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:17:10): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 16, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 5.23}`
- image request (2026-10-25 14:17:12): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 0.68}`
- L1 filter LLM call: prompt 7287 tokens, output 67 tokens, 4.1 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 30sec | 00:02:30–00:03:00 | 1 / 0.032787 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_5` |
| txt2 | ✓ | worldmm-episodic | 10sec | 00:02:40–00:02:50 | 2 / 0.032002 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_16` |
| txt3 | ✓ | worldmm-episodic | 10sec | 00:02:50–00:03:00 | 3 / 0.032522 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_17` |
| txt4 | ✓ | worldmm-episodic | 3min | 00:00:00–00:03:00 | 4 / 0.032787 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_0` |
| txt5 | ✓ | worldmm-episodic | 3min | 00:03:00–00:06:00 | 5 / 0.048652 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_1` |
| txt6 |  | worldmm-episodic | 10sec | 00:00:30–00:00:40 | 6 / 0.032266 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_3` |
| txt7 | ✓ | worldmm-episodic | 30sec | 00:04:30–00:05:00 | 7 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_9` |
| txt8 | ✓ | worldmm-episodic | 10sec | 00:04:30–00:04:40 | 8 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_27` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.032522 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_39` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.032002 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_44` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.03125 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_121` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.030769 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_122` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:02:30-00:03:00 | episodic 30sec] Three men gather on an outdoor basketball court, preparing for a dribbling challenge using a SKLZ Dribble Stick. The man in the red hoodie introduces the game, asking if they want to see how the dribble stick works, while the man in the blue jersey prepares to demonstrate it. The device—a black training tool with adjustable yellow arms and “DRIBBLE STICK” branding—is shown in detail before the group assembles, each holding a basketball, to review the rules: players take turns dribbling while avoiding contact with the stick; the person who fails first must run five laps around the court. The group is ready to begin, with the blue-jerseyed player poised to lead the demonstration.
```

**txt2** (cited)

```
[00:02:40-00:02:50 | episodic 10sec] A man in a red hoodie holds a basketball while standing on a basketball court with two other men, one in a blue jersey and another in a black shirt and cap. The scene transitions to a close-up of a black training device labeled "DRIBBLE STICK" by SKLZ, showing its adjustable yellow arms and base. The camera pans around the device, highlighting its construction and branding.
```

**txt3** (cited)

```
[00:02:50-00:03:00 | episodic 10sec] A close-up shot shows a black "Dribble Stick" device with a yellow logo. The scene then transitions to an outdoor basketball court where three men are gathered. One man in a red hoodie holds a basketball and a white device, while another in a blue jersey and a third in a black hoodie and white cap each hold basketballs. They appear to be reviewing rules or scores on the device, preparing for a dribbling challenge. The audio explains the game: participants take turns using the dribble stick to see who can go the longest without hitting it, and the person with the shortest time must run five laps around the court.
```

**txt4** (cited)

```
[00:00:00-00:03:00 | episodic 3min] Six men—Chris, Zach, Cass, James, Mitchell, and a sixth unnamed player—gather on a sunny outdoor basketball court to test 12 viral sports gadgets, splitting into two teams of three. Dressed in athletic wear, they introduce the challenge while holding basketballs near a hoop and trees. One man in a white hoodie addresses the camera, setting the tone with playful banter and audio cues like “Hands up, hands up” and “Mump is blinding me.” The scene transitions to a countdown and gear review, beginning with a close-up of black nylon straps, signaling the start of hands-on testing.

The group begins evaluating gadgets, starting with “SPORTS DRIBBLE SPECS.” One player dons the goggles and prepares for a dribbling time trial, where participants must dribble through three cones and touch a pole to stop the clock. Rules are clarified near a pool under bright sunlight, with the man in the hoodie confirming the forfeit rule for the slowest time. The drill proceeds with players like Chris and Zach showcasing speed and control, with timers capturing times like 10:85 and 9:51 seconds. Commentary highlights frustrations (“handles were definitely off”) and praise (“He’s making great time”), emphasizing the competitive yet casual atmosphere.

Later, the group discusses the gadget’s usefulness, with the man in the white hoodie expressing discomfort with traditional basketballs forcing him to look down. A score graphic flashes from 5 to 6, then 4, as teammates react with thumbs-up approval. The segment ends with the introduction of the SKLZ Dribble Stick—a black training tool with adjustable yellow arms—where the blue-jerseyed player prepares to demonstrate its use. Rules are reviewed: players dribble while avoiding the stick; the first to touch it runs five laps. The group is ready to begin, setting up for the next round of testing.
```

**txt5** (cited)

```
[00:03:00-00:06:00 | episodic 3min] Three men gather on an outdoor basketball court, negotiating positions before settling into a shooting challenge. One man in a black hoodie and white cap adjusts a basketball on a training device while the others—wearing red and blue jerseys—observe, holding balls. A fourth person films the scene under clear skies, with trees and a fence in the background. The group transitions to a hoop with a vertical obstacle, where they take turns shooting under a 30-second countdown. Encouragement and light-hearted banter—such as “you might be safe just making it past that first one”—add to the casual yet competitive tone. The man in the black hoodie successfully makes his shot, smiling as he walks back, while the man in red watches amusedly. Their conversation hints at past forfeits and humorous self-deprecation.

The group then evaluates a dribble stick, with the man in the blue jersey rating it an 8/10, followed by the man in the black shirt agreeing, and the man in the black hoodie giving it a 7—joking that anything helping him fail is “pretty good.” The conversation remains lighthearted and collaborative.

Later, a man in a white hoodie demonstrates the “Straight Shooter Strap,” explaining how it stabilizes the elbow during shooting. He adjusts the strap on his arm while a third observer watches. The scene widens to show the full court, hoop, and surrounding hills under clear skies, setting up practical use of the device.

A shooter in a white shirt and patterned shorts begins a shooting sequence, initially making one shot (0/1), then missing several, with the scoreboard climbing to 0/3. He pauses, inspecting his elbow, seemingly frustrated. As the sequence continues, he scores more shots, pushing the tally to 3/16, with teammates retrieving balls and commentary tracking each attempt. The scoreboard climbs steadily, accompanied by remarks like “Dude, 15,” and “Zach’s uses this thing, bro.” The player smiles at the camera as he approaches 15 successful shots, with the backdrop of a large house and trees under clear skies.
```

**txt6**

```
[00:00:30-00:00:40 | episodic 10sec] On an outdoor basketball court, a group of men, one in a white hoodie and blue shorts holding a basketball, speaks to the camera, introducing a segment where teams will pick their favorite gadgets and determine the best one. As he gestures, the camera pans to another player in a jersey who is examining a small object, then cuts to a close-up of a pair of sports dribble specs in their packaging.
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
[video-level knowledge | semantic] (on-screen text, reads, MOST DRIBBLES IN 15 SECONDS)
```

**txt10**

```
[video-level knowledge | semantic] (The text overlay, reads, 20 LOW, MEDIUM, & HIGH DRIBBLES IN 60 SECONDS)
```

**txt11**

```
[video-level knowledge | semantic] (player, can dribble, basketball)
```

**txt12**

```
[video-level knowledge | semantic] (player, shoots, basketball)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:34:45 | 00:34:40–00:34:50 | `-QuCz7kxBr8:visual:00344000` | `outputs/p9p19_check_20261025_141401/frames_s3/-QuCz7kxBr8/00344000.jpg` |
| img2 |  | 00:21:35 | 00:21:30–00:21:40 | `-QuCz7kxBr8:visual:00213000` | `outputs/p9p19_check_20261025_141401/frames_s3/-QuCz7kxBr8/00213000.jpg` |
| img3 |  | 00:28:45 | 00:28:40–00:28:50 | `-QuCz7kxBr8:visual:00284000` | `outputs/p9p19_check_20261025_141401/frames_s3/-QuCz7kxBr8/00284000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:34:40-00:34:50 | video frame at 2085.0s] On an outdoor basketball court under a clear blue sky, a player in a white jersey and orange shoes, carrying large cylindrical training pads, prepares to defend against another player in a black shirt and pink shorts who is dribbling a basketball. The defender shuffles laterally, maintaining a low stance, while the dribbler moves around him. Several other people are visible in the background, some standing and watching, others engaged in their own activities. The court features a blue painted area with "HYPE" written on it, and a basketball hoop is visible at one end. Mountains can be seen in the distance behind a low wall.
```

**img2**

```
[00:21:30-00:21:40 | video frame at 1295.0s] A man in a blue star-patterned basketball jersey stands on an outdoor court, holding a basketball. He takes a shot, launching the ball toward the hoop. The ball arcs through the air and goes through the net. Other people are visible on the court and in the background, and the scene is set under a bright, sunny sky with trees and hills in the distance.
```

**img3**

```
[00:28:40-00:28:50 | video frame at 1725.0s] Six men stand on an outdoor basketball court under a clear blue sky. One man in the center holds a basketball and slightly shifts his position, while the others remain mostly stationary, facing him. The court has visible markings and a hoop in the background, with trees and hills visible beyond a fence. There is no audible content in this segment.
```
