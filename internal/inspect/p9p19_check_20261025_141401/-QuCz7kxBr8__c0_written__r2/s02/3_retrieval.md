# Section 2 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:16:33): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 17, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 5.57}`
- image request (2026-10-25 14:16:36): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 0.98}`
- L1 filter LLM call: prompt 7550 tokens, output 68 tokens, 4.4 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 3min | 00:00:00–00:03:00 | 1 / 0.04918 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_0` |
| txt2 | ✓ | worldmm-episodic | 10sec | 00:00:50–00:01:00 | 2 / 0.032522 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_5` |
| txt3 | ✓ | worldmm-episodic | 30sec | 00:00:30–00:01:00 | 3 / 0.032266 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_1` |
| txt4 | ✓ | worldmm-episodic | 30sec | 00:02:30–00:03:00 | 4 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_5` |
| txt5 | ✓ | worldmm-episodic | 10sec | 00:02:50–00:03:00 | 5 / 0.032522 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_17` |
| txt6 | ✓ | worldmm-episodic | 10sec | 00:02:40–00:02:50 | 6 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_16` |
| txt7 | ✓ | worldmm-episodic | 10sec | 00:01:10–00:01:20 | 7 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_7` |
| txt8 |  | worldmm-episodic | 30sec | 00:12:30–00:13:00 | 8 / 0.032522 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_25` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.048916 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_39` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.048131 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_44` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.047371 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_121` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.046635 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_122` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:00:00-00:03:00 | episodic 3min] Six men—Chris, Zach, Cass, James, Mitchell, and a sixth unnamed player—gather on a sunny outdoor basketball court to test 12 viral sports gadgets, splitting into two teams of three. Dressed in athletic wear, they introduce the challenge while holding basketballs near a hoop and trees. One man in a white hoodie addresses the camera, setting the tone with playful banter and audio cues like “Hands up, hands up” and “Mump is blinding me.” The scene transitions to a countdown and gear review, beginning with a close-up of black nylon straps, signaling the start of hands-on testing.

The group begins evaluating gadgets, starting with “SPORTS DRIBBLE SPECS.” One player dons the goggles and prepares for a dribbling time trial, where participants must dribble through three cones and touch a pole to stop the clock. Rules are clarified near a pool under bright sunlight, with the man in the hoodie confirming the forfeit rule for the slowest time. The drill proceeds with players like Chris and Zach showcasing speed and control, with timers capturing times like 10:85 and 9:51 seconds. Commentary highlights frustrations (“handles were definitely off”) and praise (“He’s making great time”), emphasizing the competitive yet casual atmosphere.

Later, the group discusses the gadget’s usefulness, with the man in the white hoodie expressing discomfort with traditional basketballs forcing him to look down. A score graphic flashes from 5 to 6, then 4, as teammates react with thumbs-up approval. The segment ends with the introduction of the SKLZ Dribble Stick—a black training tool with adjustable yellow arms—where the blue-jerseyed player prepares to demonstrate its use. Rules are reviewed: players dribble while avoiding the stick; the first to touch it runs five laps. The group is ready to begin, setting up for the next round of testing.
```

**txt2** (cited)

```
[00:00:50-00:01:00 | episodic 10sec] Three men are standing outdoors near a pool, preparing for a basketball dribbling challenge. One man, wearing a white hoodie and patterned shorts, holds a basketball and speaks, while another in a white t-shirt stands with his arms crossed. The third man, in a red and white jersey, holds a basketball and gestures toward a pole, explaining the rules of the “dribble time trial” involving three cones and touching the pole to end the stopwatch. The man in the hoodie says, “Slowest time has to do a forfeit,” and the other two listen. The scene is bright and sunny, with the pool and surrounding greenery visible in the background.
```

**txt3** (cited)

```
[00:00:30-00:01:00 | episodic 30sec] A group of men on an outdoor basketball court introduces a gadget challenge where teams will select and test their favorite sports gear. The segment kicks off with one man in a white hoodie and blue shorts holding a basketball and addressing the camera, while the camera pans to another player examining a small object—revealed to be a pair of “SPORTS DRIBBLE SPECS” in packaging. One participant then puts on the goggles, adjusts them, and prepares for a dribbling time trial alongside a teammate near a hoop. The scene transitions to three men near a pool, where the rules of the “dribble time trial” are explained: players must dribble through three cones and touch a pole to stop the clock, with the slowest time resulting in a forfeit. The man in the hoodie confirms the rule, and the others listen attentively under bright, sunny conditions with the pool and greenery in the background.
```

**txt4** (cited)

```
[00:02:30-00:03:00 | episodic 30sec] Three men gather on an outdoor basketball court, preparing for a dribbling challenge using a SKLZ Dribble Stick. The man in the red hoodie introduces the game, asking if they want to see how the dribble stick works, while the man in the blue jersey prepares to demonstrate it. The device—a black training tool with adjustable yellow arms and “DRIBBLE STICK” branding—is shown in detail before the group assembles, each holding a basketball, to review the rules: players take turns dribbling while avoiding contact with the stick; the person who fails first must run five laps around the court. The group is ready to begin, with the blue-jerseyed player poised to lead the demonstration.
```

**txt5** (cited)

```
[00:02:50-00:03:00 | episodic 10sec] A close-up shot shows a black "Dribble Stick" device with a yellow logo. The scene then transitions to an outdoor basketball court where three men are gathered. One man in a red hoodie holds a basketball and a white device, while another in a blue jersey and a third in a black hoodie and white cap each hold basketballs. They appear to be reviewing rules or scores on the device, preparing for a dribbling challenge. The audio explains the game: participants take turns using the dribble stick to see who can go the longest without hitting it, and the person with the shortest time must run five laps around the court.
```

**txt6** (cited)

```
[00:02:40-00:02:50 | episodic 10sec] A man in a red hoodie holds a basketball while standing on a basketball court with two other men, one in a blue jersey and another in a black shirt and cap. The scene transitions to a close-up of a black training device labeled "DRIBBLE STICK" by SKLZ, showing its adjustable yellow arms and base. The camera pans around the device, highlighting its construction and branding.
```

**txt7** (cited)

```
[00:01:10-00:01:20 | episodic 10sec] A basketball player in a white jersey dribbles through cones on an outdoor court, completing the drill as a timer displays “10:85 SECONDS.” He stops, turns, and interacts with another player holding a basketball. The second player comments, “Dude, I almost lost the ball in the middle cone,” while the first player says, “I got to warm up, man.” The scene takes place on a residential court beside a pool, with spectators and a house in the background.
```

**txt8**

```
[00:12:30-00:13:00 | episodic 30sec] A basketball player in a red and white jersey dribbles on a blue outdoor court under bright sunlight, maintaining a low athletic stance while shifting weight and controlling the ball with his right hand; numbers count down sequentially from 12 to 3 in the top right and 5 to 21 in the bottom left, suggesting a timed drill, while another player and a covered patio are visible in the background.

The scene transitions to a second player in a white hoodie and blue shorts taking his turn dribbling, while the first player watches; numbers now count down from 24 to 12, reinforcing the timed nature of the drill, with both players on the same court under the same bright conditions.

Later, the player in the white hoodie and patterned shorts dribbles while being closely guarded by the jersey-wearing player; numbers appear again—starting at 11 in the top right and 8 in the bottom left—and count down from 11 to 2 in the top right while increasing from 8 to 24 in the bottom left, indicating a dynamic, possibly dual-timed challenge; the defender maintains a consistent defensive stance as the dribbler maneuvers, with a house and trees visible in the background.
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
| img1 |  | 00:02:55 | 00:02:50–00:03:00 | `-QuCz7kxBr8:visual:00025000` | `outputs/p9p19_check_20261025_141401/frames_s3/-QuCz7kxBr8/00025000.jpg` |
| img2 |  | 00:14:55 | 00:14:50–00:15:00 | `-QuCz7kxBr8:visual:00145000` | `outputs/p9p19_check_20261025_141401/frames_s3/-QuCz7kxBr8/00145000.jpg` |
| img3 |  | 00:14:45 | 00:14:40–00:14:50 | `-QuCz7kxBr8:visual:00144000` | `outputs/p9p19_check_20261025_141401/frames_s3/-QuCz7kxBr8/00144000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:02:50-00:03:00 | video frame at 175.0s] A close-up shot shows a black "Dribble Stick" device with a yellow logo. The scene then transitions to an outdoor basketball court where three men are gathered. One man in a red hoodie holds a basketball and a white device, while another in a blue jersey and a third in a black hoodie and white cap each hold basketballs. They appear to be reviewing rules or scores on the device, preparing for a dribbling challenge. The audio explains the game: participants take turns using the dribble stick to see who can go the longest without hitting it, and the person with the shortest time must run five laps around the court.
```

**img2**

```
[00:14:50-00:15:00 | video frame at 895.0s] Three men stand outdoors near a table with basketball gear. One man in a blue jersey puts on a pair of gloves while the other two watch. The text overlay reads "20 LOW, MEDIUM, & HIGH DRIBBLES IN 60 SECONDS." The man in the blue jersey then says, "IT'S LIKE THE THICC WOMEN OF GLOVES."
```

**img3**

```
[00:14:40-00:14:50 | video frame at 885.0s] A close-up shot displays a pair of black and orange "POWER HANDZ" gloves with a leopard print pattern, followed by a scene outdoors where three men stand around a table. One man in a blue sleeveless shirt is gesturing while speaking, while the other two watch. A text overlay appears, reading "20 LOW, MEDIUM, & HIGH DRIBBLES IN 60 SECONDS."
```
