# Section 1 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:15:47): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 18, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 7.02}`
- image request (2026-10-25 14:15:51): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 1.25}`
- L1 filter LLM call: prompt 8090 tokens, output 65 tokens, 4.3 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 3min | 00:00:00–00:03:00 | 1 / 0.032787 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_0` |
| txt2 | ✓ | worldmm-episodic | 30sec | 00:00:30–00:01:00 | 2 / 0.032522 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_1` |
| txt3 |  | worldmm-episodic | 10sec | 00:00:30–00:00:40 | 3 / 0.032522 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_3` |
| txt4 |  | worldmm-episodic | 3min | 00:03:00–00:06:00 | 4 / 0.032258 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_1` |
| txt5 | ✓ | worldmm-episodic | 30sec | 00:01:00–00:01:30 | 5 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_2` |
| txt6 | ✓ | worldmm-episodic | 10sec | 00:01:40–00:01:50 | 6 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_10` |
| txt7 | ✓ | worldmm-episodic | 30sec | 00:02:00–00:02:30 | 7 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_4` |
| txt8 | ✓ | worldmm-episodic | 10sec | 00:00:40–00:00:50 | 8 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_4` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.048147 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_44` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.032002 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_52` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.031498 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_31` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.03101 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_28` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:00:00-00:03:00 | episodic 3min] Six men—Chris, Zach, Cass, James, Mitchell, and a sixth unnamed player—gather on a sunny outdoor basketball court to test 12 viral sports gadgets, splitting into two teams of three. Dressed in athletic wear, they introduce the challenge while holding basketballs near a hoop and trees. One man in a white hoodie addresses the camera, setting the tone with playful banter and audio cues like “Hands up, hands up” and “Mump is blinding me.” The scene transitions to a countdown and gear review, beginning with a close-up of black nylon straps, signaling the start of hands-on testing.

The group begins evaluating gadgets, starting with “SPORTS DRIBBLE SPECS.” One player dons the goggles and prepares for a dribbling time trial, where participants must dribble through three cones and touch a pole to stop the clock. Rules are clarified near a pool under bright sunlight, with the man in the hoodie confirming the forfeit rule for the slowest time. The drill proceeds with players like Chris and Zach showcasing speed and control, with timers capturing times like 10:85 and 9:51 seconds. Commentary highlights frustrations (“handles were definitely off”) and praise (“He’s making great time”), emphasizing the competitive yet casual atmosphere.

Later, the group discusses the gadget’s usefulness, with the man in the white hoodie expressing discomfort with traditional basketballs forcing him to look down. A score graphic flashes from 5 to 6, then 4, as teammates react with thumbs-up approval. The segment ends with the introduction of the SKLZ Dribble Stick—a black training tool with adjustable yellow arms—where the blue-jerseyed player prepares to demonstrate its use. Rules are reviewed: players dribble while avoiding the stick; the first to touch it runs five laps. The group is ready to begin, setting up for the next round of testing.
```

**txt2** (cited)

```
[00:00:30-00:01:00 | episodic 30sec] A group of men on an outdoor basketball court introduces a gadget challenge where teams will select and test their favorite sports gear. The segment kicks off with one man in a white hoodie and blue shorts holding a basketball and addressing the camera, while the camera pans to another player examining a small object—revealed to be a pair of “SPORTS DRIBBLE SPECS” in packaging. One participant then puts on the goggles, adjusts them, and prepares for a dribbling time trial alongside a teammate near a hoop. The scene transitions to three men near a pool, where the rules of the “dribble time trial” are explained: players must dribble through three cones and touch a pole to stop the clock, with the slowest time resulting in a forfeit. The man in the hoodie confirms the rule, and the others listen attentively under bright, sunny conditions with the pool and greenery in the background.
```

**txt3**

```
[00:00:30-00:00:40 | episodic 10sec] On an outdoor basketball court, a group of men, one in a white hoodie and blue shorts holding a basketball, speaks to the camera, introducing a segment where teams will pick their favorite gadgets and determine the best one. As he gestures, the camera pans to another player in a jersey who is examining a small object, then cuts to a close-up of a pair of sports dribble specs in their packaging.
```

**txt4**

```
[00:03:00-00:06:00 | episodic 3min] Three men gather on an outdoor basketball court, negotiating positions before settling into a shooting challenge. One man in a black hoodie and white cap adjusts a basketball on a training device while the others—wearing red and blue jerseys—observe, holding balls. A fourth person films the scene under clear skies, with trees and a fence in the background. The group transitions to a hoop with a vertical obstacle, where they take turns shooting under a 30-second countdown. Encouragement and light-hearted banter—such as “you might be safe just making it past that first one”—add to the casual yet competitive tone. The man in the black hoodie successfully makes his shot, smiling as he walks back, while the man in red watches amusedly. Their conversation hints at past forfeits and humorous self-deprecation.

The group then evaluates a dribble stick, with the man in the blue jersey rating it an 8/10, followed by the man in the black shirt agreeing, and the man in the black hoodie giving it a 7—joking that anything helping him fail is “pretty good.” The conversation remains lighthearted and collaborative.

Later, a man in a white hoodie demonstrates the “Straight Shooter Strap,” explaining how it stabilizes the elbow during shooting. He adjusts the strap on his arm while a third observer watches. The scene widens to show the full court, hoop, and surrounding hills under clear skies, setting up practical use of the device.

A shooter in a white shirt and patterned shorts begins a shooting sequence, initially making one shot (0/1), then missing several, with the scoreboard climbing to 0/3. He pauses, inspecting his elbow, seemingly frustrated. As the sequence continues, he scores more shots, pushing the tally to 3/16, with teammates retrieving balls and commentary tracking each attempt. The scoreboard climbs steadily, accompanied by remarks like “Dude, 15,” and “Zach’s uses this thing, bro.” The player smiles at the camera as he approaches 15 successful shots, with the backdrop of a large house and trees under clear skies.
```

**txt5** (cited)

```
[00:01:00-00:01:30 | episodic 30sec] Two men are on an outdoor basketball court; one in a white t-shirt gestures as if giving instructions while the other, in a basketball jersey and sunglasses, holds a basketball. The scene transitions to show the jersey-wearing player dribbling around orange cones, maneuvering with focus as the camera follows his movement. Other people are visible in the background, suggesting a casual, communal setting.

The same player, now in a white jersey, completes a cone drill as a timer reads “10:85 SECONDS.” He stops, turns, and engages with another player holding a ball. The second player remarks, “Dude, I almost lost the ball in the middle cone,” to which the first replies, “I got to warm up, man.” The setting is a residential court beside a pool, with spectators and a house in the background, reinforcing the informal, neighborhood vibe.

A young man in a white shirt and patterned shorts dribbles rapidly toward the basket, showcasing speed and control. Nearby, a person in a tie-dye jersey stands with hands on hips, observing, while another in a white hoodie holds a basketball. The sunny backyard, complete with a pool and large house, frames the scene. Audio captures the commentary: “Chris went fast,” “Yes,” and “It's blinding me,” highlighting the intensity and pace of the play.
```

**txt6** (cited)

```
[00:01:40-00:01:50 | episodic 10sec] At an outdoor basketball court beside a pool, a man in a white hoodie and patterned shorts holds a basketball while talking to another player in a tie-dye jersey. The player in the jersey stands with his hands on his hips, listening. In the background, another person dribbles a basketball. The conversation includes comments about handles being off and making it harder to dribble, with a mention that "Zach is off" and "He's making great time." The scene shifts to a wider view of the court, showing the players in position for a drill or game.
```

**txt7** (cited)

```
[00:02:00-00:02:30 | episodic 30sec] Three young men stand on an outdoor basketball court, each holding a ball, engaged in a discussion about dribbling drills and the usefulness of a gadget that helps players avoid looking down. The setting is a sunny backyard with a pool and house in the background; on-screen text displays “9:51 SECONDS.” The man in the center, wearing a white hoodie and sunglasses, gestures while speaking, expressing personal discomfort with the basketballs he’s using — claiming they force him to tilt his head down more. As the conversation progresses, a score graphic briefly flashes from 5 to 6, and later shows 4, while the man on the right, in a white t-shirt, responds with a thumbs-up after a rating of 5 is mentioned, indicating agreement or approval of the gadget’s effectiveness. The group remains casually engaged, with the man in the red and white jersey listening attentively.
```

**txt8** (cited)

```
[00:00:40-00:00:50 | episodic 10sec] A person puts on a pair of sports goggles labeled "SPORTS DRIBBLE SPECS" on an outdoor basketball court. Another person watches as the first person adjusts the goggles. The person wearing the goggles then holds a basketball, and the two men stand near a basketball hoop, preparing for a time trial.
```

**txt9**

```
[video-level knowledge | semantic] (The text overlay, reads, 20 LOW, MEDIUM, & HIGH DRIBBLES IN 60 SECONDS)
```

**txt10**

```
[video-level knowledge | semantic] (blue and black fingerless gloves, has text, ANTI GRIP DIBBLING ASSISTANT)
```

**txt11**

```
[video-level knowledge | semantic] (device, is on, table)
```

**txt12**

```
[video-level knowledge | semantic] (white object, is, device)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 | ✓ | 00:00:15 | 00:00:10–00:00:20 | `-QuCz7kxBr8:visual:00001000` | `outputs/p9p19_check_20261025_141401/frames_s3/-QuCz7kxBr8/00001000.jpg` |
| img2 | ✓ | 00:00:25 | 00:00:20–00:00:30 | `-QuCz7kxBr8:visual:00002000` | `outputs/p9p19_check_20261025_141401/frames_s3/-QuCz7kxBr8/00002000.jpg` |
| img3 | ✓ | 00:28:45 | 00:28:40–00:28:50 | `-QuCz7kxBr8:visual:00284000` | `outputs/p9p19_check_20261025_141401/frames_s3/-QuCz7kxBr8/00284000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1** (cited)

```
[00:00:10-00:00:20 | video frame at 15.0s] On an outdoor basketball court, a group of men gather with basketballs. One man in a blue jersey crouches near a training device, then stands up and looks upward. The camera shifts to show a man in a black hoodie and cap, holding a basketball and speaking animatedly to the group. The scene transitions to a close-up of three black nylon straps with buckles, laid out on a white surface. Audio includes a greeting, a countdown, an exclamation, and an introduction to a video segment about testing viral basketball gadgets.
```

**img2** (cited)

```
[00:00:20-00:00:30 | video frame at 25.0s] On an outdoor basketball court, a group of six men—Chris, Zach, Cass, James, and Mitchell—are introduced as they prepare to test 12 viral basketball gadgets. They are split into two teams, each assigned six gadgets to evaluate. The men, dressed in athletic wear, hold basketballs and gesture as they speak, with one man in a white hoodie and blue shorts speaking directly to the camera while the others stand around him. The setting is sunny, with a basketball hoop and surrounding trees visible in the background.
```

**img3** (cited)

```
[00:28:40-00:28:50 | video frame at 1725.0s] Six men stand on an outdoor basketball court under a clear blue sky. One man in the center holds a basketball and slightly shifts his position, while the others remain mostly stationary, facing him. The court has visible markings and a hoop in the background, with trees and hills visible beyond a fence. There is no audible content in this segment.
```
