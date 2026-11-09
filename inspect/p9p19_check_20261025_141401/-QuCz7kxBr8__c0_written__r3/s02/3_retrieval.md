# Section 2 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:22:20): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 2, 'episodic_candidates': 16, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 5.15}`
- image request (2026-10-25 14:22:23): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 0.82}`
- L1 filter LLM call: prompt 7375 tokens, output 70 tokens, 4.3 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 3min | 00:00:00–00:03:00 | 1 / 0.032787 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_0` |
| txt2 | ✓ | worldmm-episodic | 30sec | 00:02:30–00:03:00 | 2 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_5` |
| txt3 | ✓ | worldmm-episodic | 10sec | 00:02:50–00:03:00 | 3 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_17` |
| txt4 | ✓ | worldmm-episodic | 30sec | 00:33:00–00:33:30 | 4 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_66` |
| txt5 | ✓ | worldmm-episodic | 10sec | 00:01:10–00:01:20 | 5 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_7` |
| txt6 |  | worldmm-episodic | 30sec | 00:12:30–00:13:00 | 6 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_25` |
| txt7 | ✓ | worldmm-episodic | 10sec | 00:02:30–00:02:40 | 7 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_15` |
| txt8 | ✓ | worldmm-episodic | 10sec | 00:02:40–00:02:50 | 8 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_16` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.032787 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_36` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.032258 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_39` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.031746 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_44` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.03125 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_121` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:00:00-00:03:00 | episodic 3min] Six men—Chris, Zach, Cass, James, Mitchell, and a sixth unnamed player—gather on a sunny outdoor basketball court to test 12 viral sports gadgets, splitting into two teams of three. Dressed in athletic wear, they introduce the challenge while holding basketballs near a hoop and trees. One man in a white hoodie addresses the camera, setting the tone with playful banter and audio cues like “Hands up, hands up” and “Mump is blinding me.” The scene transitions to a countdown and gear review, beginning with a close-up of black nylon straps, signaling the start of hands-on testing.

The group begins evaluating gadgets, starting with “SPORTS DRIBBLE SPECS.” One player dons the goggles and prepares for a dribbling time trial, where participants must dribble through three cones and touch a pole to stop the clock. Rules are clarified near a pool under bright sunlight, with the man in the hoodie confirming the forfeit rule for the slowest time. The drill proceeds with players like Chris and Zach showcasing speed and control, with timers capturing times like 10:85 and 9:51 seconds. Commentary highlights frustrations (“handles were definitely off”) and praise (“He’s making great time”), emphasizing the competitive yet casual atmosphere.

Later, the group discusses the gadget’s usefulness, with the man in the white hoodie expressing discomfort with traditional basketballs forcing him to look down. A score graphic flashes from 5 to 6, then 4, as teammates react with thumbs-up approval. The segment ends with the introduction of the SKLZ Dribble Stick—a black training tool with adjustable yellow arms—where the blue-jerseyed player prepares to demonstrate its use. Rules are reviewed: players dribble while avoiding the stick; the first to touch it runs five laps. The group is ready to begin, setting up for the next round of testing.
```

**txt2** (cited)

```
[00:02:30-00:03:00 | episodic 30sec] Three men gather on an outdoor basketball court, preparing for a dribbling challenge using a SKLZ Dribble Stick. The man in the red hoodie introduces the game, asking if they want to see how the dribble stick works, while the man in the blue jersey prepares to demonstrate it. The device—a black training tool with adjustable yellow arms and “DRIBBLE STICK” branding—is shown in detail before the group assembles, each holding a basketball, to review the rules: players take turns dribbling while avoiding contact with the stick; the person who fails first must run five laps around the court. The group is ready to begin, with the blue-jerseyed player poised to lead the demonstration.
```

**txt3** (cited)

```
[00:02:50-00:03:00 | episodic 10sec] A close-up shot shows a black "Dribble Stick" device with a yellow logo. The scene then transitions to an outdoor basketball court where three men are gathered. One man in a red hoodie holds a basketball and a white device, while another in a blue jersey and a third in a black hoodie and white cap each hold basketballs. They appear to be reviewing rules or scores on the device, preparing for a dribbling challenge. The audio explains the game: participants take turns using the dribble stick to see who can go the longest without hitting it, and the person with the shortest time must run five laps around the court.
```

**txt4** (cited)

```
[00:33:00-00:33:30 | episodic 30sec] **[Event 1]** A one-on-one basketball game unfolds on an outdoor court under a clear blue sky, with the offensive player in a black shirt and pink shorts dribbling while being defended by a player in a white shirt wielding a padded training tool. After a brief defensive exchange, the offensive player successfully shoots and scores, triggering a scoreboard graphic that flashes “1-1,” indicating a tied game. Spectators and other players observe from around the court.

**[Event 2]** A player in a blue jersey prepares to shoot while being guarded by a player in a white shirt and patterned shorts, who holds a large padded training tool above his head. After the shot, the player in blue lowers the ball and begins dribbling, while the defender shifts the training tool dynamically to simulate defensive pressure. Background activity includes onlookers and other court users engaged in separate games or idle moments.

**[Event 3]** On the same court, a player in a red and white jersey dribbles while being closely guarded by an opponent holding a large black training pad. The defender attempts to block, prompting the dribbler to maneuver around him. The court features a blue-painted branded area, and distant mountains are visible beyond a fence, with other spectators or players watching or waiting nearby.
```

**txt5** (cited)

```
[00:01:10-00:01:20 | episodic 10sec] A basketball player in a white jersey dribbles through cones on an outdoor court, completing the drill as a timer displays “10:85 SECONDS.” He stops, turns, and interacts with another player holding a basketball. The second player comments, “Dude, I almost lost the ball in the middle cone,” while the first player says, “I got to warm up, man.” The scene takes place on a residential court beside a pool, with spectators and a house in the background.
```

**txt6**

```
[00:12:30-00:13:00 | episodic 30sec] A basketball player in a red and white jersey dribbles on a blue outdoor court under bright sunlight, maintaining a low athletic stance while shifting weight and controlling the ball with his right hand; numbers count down sequentially from 12 to 3 in the top right and 5 to 21 in the bottom left, suggesting a timed drill, while another player and a covered patio are visible in the background.

The scene transitions to a second player in a white hoodie and blue shorts taking his turn dribbling, while the first player watches; numbers now count down from 24 to 12, reinforcing the timed nature of the drill, with both players on the same court under the same bright conditions.

Later, the player in the white hoodie and patterned shorts dribbles while being closely guarded by the jersey-wearing player; numbers appear again—starting at 11 in the top right and 8 in the bottom left—and count down from 11 to 2 in the top right while increasing from 8 to 24 in the bottom left, indicating a dynamic, possibly dual-timed challenge; the defender maintains a consistent defensive stance as the dribbler maneuvers, with a house and trees visible in the background.
```

**txt7** (cited)

```
[00:02:30-00:02:40 | episodic 10sec] Three men are on an outdoor basketball court. One man in a red hoodie holds a basketball and gestures while speaking, another in a blue jersey bends over a dribble stick, and a third in a black hoodie stands nearby holding a basketball. The man in the red hoodie asks if they want to see how the dribble stick works, and the man in the blue jersey prepares to demonstrate it.
```

**txt8** (cited)

```
[00:02:40-00:02:50 | episodic 10sec] A man in a red hoodie holds a basketball while standing on a basketball court with two other men, one in a blue jersey and another in a black shirt and cap. The scene transitions to a close-up of a black training device labeled "DRIBBLE STICK" by SKLZ, showing its adjustable yellow arms and base. The camera pans around the device, highlighting its construction and branding.
```

**txt9**

```
[video-level knowledge | semantic] (challenge, penalizes least baskets with, 100 sit-ups)
```

**txt10**

```
[video-level knowledge | semantic] (on-screen text, reads, MOST DRIBBLES IN 15 SECONDS)
```

**txt11**

```
[video-level knowledge | semantic] (The text overlay, reads, 20 LOW, MEDIUM, & HIGH DRIBBLES IN 60 SECONDS)
```

**txt12**

```
[video-level knowledge | semantic] (player, can dribble, basketball)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:00:35 | 00:00:30–00:00:40 | `-QuCz7kxBr8:visual:00003000` | `outputs/p9p19_check_20261025_141401/frames_s2/-QuCz7kxBr8/00003000.jpg` |
| img2 |  | 00:00:25 | 00:00:20–00:00:30 | `-QuCz7kxBr8:visual:00002000` | `outputs/p9p19_check_20261025_141401/frames_s2/-QuCz7kxBr8/00002000.jpg` |
| img3 |  | 00:03:05 | 00:03:00–00:03:10 | `-QuCz7kxBr8:visual:00030000` | `outputs/p9p19_check_20261025_141401/frames_s2/-QuCz7kxBr8/00030000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:00:30-00:00:40 | video frame at 35.0s] On an outdoor basketball court, a group of men, one in a white hoodie and blue shorts holding a basketball, speaks to the camera, introducing a segment where teams will pick their favorite gadgets and determine the best one. As he gestures, the camera pans to another player in a jersey who is examining a small object, then cuts to a close-up of a pair of sports dribble specs in their packaging.
```

**img2**

```
[00:00:20-00:00:30 | video frame at 25.0s] On an outdoor basketball court, a group of six men—Chris, Zach, Cass, James, and Mitchell—are introduced as they prepare to test 12 viral basketball gadgets. They are split into two teams, each assigned six gadgets to evaluate. The men, dressed in athletic wear, hold basketballs and gesture as they speak, with one man in a white hoodie and blue shorts speaking directly to the camera while the others stand around him. The setting is sunny, with a basketball hoop and surrounding trees visible in the background.
```

**img3**

```
[00:03:00-00:03:10 | video frame at 185.0s] Three men are on an outdoor basketball court, each holding a basketball. One man in a red hoodie, another in a blue jersey with the number 2, and a third in a black hoodie and white cap. They appear to be deciding who gets which side of the court for a game, with one man declaring he’s taking a side and another saying he’ll go first. The man in the black hoodie then bends down, likely to set up or adjust something on the court.
```
