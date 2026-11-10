# Section 4 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:23:55): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 21, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 6.07}`
- image request (2026-10-25 14:23:58): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 1.14}`
- L1 filter LLM call: prompt 8105 tokens, output 73 tokens, 4.9 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 3min | 00:18:00–00:21:00 | 1 / 0.04918 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_6` |
| txt2 | ✓ | worldmm-episodic | 10min | 00:10:00–00:20:00 | 2 / 0.04918 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10min_1` |
| txt3 | ✓ | worldmm-episodic | 30sec | 00:19:30–00:20:00 | 3 / 0.032787 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_39` |
| txt4 | ✓ | worldmm-episodic | 30sec | 00:18:00–00:18:30 | 4 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_36` |
| txt5 | ✓ | worldmm-episodic | 10sec | 00:19:50–00:20:00 | 5 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_119` |
| txt6 |  | worldmm-episodic | 30sec | 00:08:30–00:09:00 | 6 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_17` |
| txt7 | ✓ | worldmm-episodic | 30sec | 00:18:30–00:19:00 | 7 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_37` |
| txt8 |  | worldmm-episodic | 10sec | 00:19:40–00:19:50 | 8 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_118` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.031258 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_121` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_69` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_36` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_123` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:18:00-00:21:00 | episodic 3min] **[Event 1: Game Setup & Product Introduction]**  
Three men gather on an outdoor basketball court under a clear blue sky, initiating a playful game governed by the rule: “FIRST MADE SHOT SHOOTS SILLY STRING AT LOSER.” The man in the blue jersey (No. 2) explains the rules while the others prepare. A product demonstration follows, showing three black basketball shooting aids with an overlay reading “Pack of 3 Basketball Shooting Aid.” The scene reinforces the product’s purpose: enhancing shooting accuracy and enabling fun, competitive play.

**[Event 2: Synchronized Shot & Victory]**  
As the countdown from three to one flashes, all three men jump and shoot simultaneously — each ball arcs perfectly into the basket, triggering the game’s next phase. The man in the blue jersey is declared the winner via on-screen text and celebrates briefly before congratulating the man in the black hoodie and white cap. The scene, set in a sunny backyard with a hoop, trampoline, and landscaping, emphasizes camaraderie and lighthearted competition.

**[Event 3: Training Drill with Shot Coach]**  
A basketball coach in a black hoodie and white cap uses an orange “SHOT COACH” training device to guide two young players through a drill: “SHOOT FROM HALF COURT 5 TIMES WITH SHOT COACH.” He adjusts a wristband on one player while explaining precision and repetition. The scene includes a scoreboard graphic and a third man in a blue jersey observing, reinforcing the structured, tech-assisted training environment.

**[Event 4: Hand-Restraint Demonstration & Free-Throw Practice]**  
The same coach demonstrates a hand-restraint device with orange straps, securing it on his own wrist while two observers watch. He then walks to the free-throw line, preparing to shoot. The scene captures the court’s markings, surrounding trees, and a clear sky, highlighting the integration of training tools into real-game settings. Multiple shots follow, showing different players attempting shots while being observed, reinforcing the focus on technique and consistency.

**[Event 5: Product Claim Reinforcement]**  
A text overlay at 00:18:29 declares: “FIRST MADE SHOT SHOOTS SILLY STRING AT 100%,” tying the product’s performance claim to the game’s outcome. The video closes with a close-up of the Shot Coach device, underscoring its role in enhancing shooting accuracy and enabling fun, structured practice.
```

**txt2** (cited)

```
[00:10:00-00:20:00 | episodic 10min] **[Event 1: Dribble Challenge Begins]**  
A man in a white t-shirt and patterned shorts initiates a timed dribbling challenge on a sunny outdoor court, with a countdown timer and on-screen text reading “MOST DRIBBLES IN 15 SECONDS.” He maintains control of the ball throughout, while two observers — one in a white hoodie and another in a red-and-white jersey — watch. His final count is displayed as “18,” marking the completion of the first drill.

**[Event 2: Defensive Drills & Role Assignment]**  
The same player transitions into defensive drills, shifting laterally and adopting a low stance. Court markings and countdown numbers (12–3, 4–13) suggest a timed progression. Later, a role is formally assigned via text: “WATER BOY FOR REST OF THE VIDEO,” given to the man in the white hoodie. He is then assisted by another player to drink water from a bottle, while a third in a red-and-white jersey observes — reinforcing a casual, communal atmosphere.

**[Event 3: Challenge Continues & Intensifies]**  
The dribbling challenge evolves into a dual-timed drill: one player dribbles while being guarded, with countdowns from 11–2 (top right) and 8–24 (bottom left). The defender maintains a low stance as the dribbler maneuvers. The scene then shifts to a new participant in a blue jersey, who begins a 60-second challenge: “20 LOW, MEDIUM, & HIGH DRIBBLES.” He declares, “IT’S LIKE THE THICC WOMEN OF GLOVES,” adding humor as he dons “POWER HANDZ” gloves with leopard and tiger patterns before starting. A “SCORE 9” graphic appears, indicating ongoing game metrics.

**[Event 4: Social Interaction & Game Dynamics]**  
Three men engage in conversation around the court — one holding the ball, another sipping water, the third gesturing. The setting remains consistent: blue court, house, patio, and distant mountains. The video ends with the blue-jerseyed player preparing for his drill, surrounded by teammates and the playful energy of the challenge.

**[Event 5: Game Setup & Product Introduction]**  
Three men gather on an outdoor basketball court under a clear blue sky, initiating a playful game governed by the rule: “FIRST MADE SHOT SHOOTS SILLY STRING AT LOSER.” The man in the blue jersey (No. 2) explains the rules while the others prepare. A product demonstration follows, showing three black basketball shooting aids with an overlay reading “Pack of 3 Basketball Shooting Aid.” The scene reinforces the product’s purpose: enhancing shooting accuracy and enabling fun, competitive play.

**[Event 6: Synchronized Shot & Victory]**  
As the countdown from three to one flashes, all three men jump and shoot simultaneously — each ball arcs perfectly into the basket, triggering the game’s next phase. The man in the blue jersey is declared the winner via on-screen text and celebrates briefly before congratulating the man in the black hoodie and white cap. The scene, set in a sunny backyard with a hoop, trampoline, and landscaping, emphasizes camaraderie and lighthearted competition.

**[Event 7: Training Drill with Shot Coach]**  
A basketball coach in a black hoodie and white cap uses an orange “SHOT COACH” training device to guide two young players through a drill: “SHOOT FROM HALF COURT 5 TIMES WITH SHOT COACH.” He adjusts a wristband on one player while explaining precision and repetition. The scene includes a scoreboard graphic and a third man in a blue jersey observing, reinforcing the structured, tech-assisted training environment.

**[Event 8: Hand-Restraint Demonstration & Free-Throw Practice]**  
The same coach demonstrates a hand-restraint device with orange straps, securing it on his own wrist while two observers watch. He then walks to the free-throw line, preparing to shoot. The scene captures the court’s markings, surrounding trees, and a clear sky, highlighting the integration of training tools into real-game settings. Multiple shots follow, showing different players attempting shots while being observed, reinforcing the focus on technique and consistency.

**[Event 9: Product Claim Reinforcement]**  
A text overlay at 00:18:29 declares: “FIRST MADE SHOT SHOOTS SILLY STRING AT 100%,” tying the product’s performance claim to the game’s outcome. The video closes with a close-up of the Shot Coach device, underscoring its role in enhancing shooting accuracy and enabling fun, structured practice.
```

**txt3** (cited)

```
[00:19:30-00:20:00 | episodic 30sec] A basketball coach in a black hoodie and white cap stands on an outdoor court, using an orange “SHOT COACH” training device to instruct two young players, with a text overlay directing them to “SHOOT FROM HALF COURT 5 TIMES WITH SHOT COACH.” He adjusts a wristband or device on one player’s wrist while the other observes, all under bright sunlight with a hoop and greenery in the background. The coach holds a clipboard and gestures as he explains the drill, emphasizing precision and repetition through the Shot Coach system. The scene briefly cuts to a scoreboard graphic showing "-2" then resetting to "0," followed by a third man in a blue jersey crossing his arms and smiling as the scoreboard shows "-1," suggesting a playful or competitive scoring context. The coach and the player in the blue jersey later move to a table, where the coach appears to write or draw, possibly documenting progress or adjusting the training plan. The video closes with a close-up of the Shot Coach device, reinforcing its role as a key tool in the structured, tech-assisted shooting drill.
```

**txt4** (cited)

```
[00:18:00-00:18:30 | episodic 30sec] **[Event 1: Introduction of Basketball Court Scene]**  
Three men are on an outdoor basketball court: one in a red and white jersey gestures while crouched, another in a white t-shirt bends and stands, and a third in a white hoodie holds a basketball. A graphic overlay reads “SCORE 8,” establishing a scoring context. The scene then cuts to a different spot on the same court, where a man in a black t-shirt examines a piece of paper while standing beside a man in a black hoodie holding a basketball; a third man in a blue jersey observes from behind.

**[Event 2: Product Demonstration Setup]**  
The scene transitions to three men gathered around a white table outdoors under a clear blue sky. The man in the black t-shirt holds and inspects a small white object, likely a product component, while the man in the blue jersey watches with a smile and the man in the black hoodie and white cap holds a basketball, listening attentively. The video then cuts to a product shot of three black basketball shooting aids, with an overlay reading “Pack of 3 Basketball Shooting Aid,” clearly introducing the product being demonstrated.

**[Event 3: Product Claim Announcement]**  
At timestamp 00:18:29, a text overlay appears stating “FIRST MADE SHOT SHOOTS GILLY STRING AT 100%,” signaling a performance claim tied to the product’s functionality — likely indicating the shooting aid enables a perfect shot using a gilly string (a type of projectile or training tool). This marks the culmination of the product introduction and setup, reinforcing the product’s intended use and effectiveness.
```

**txt5** (cited)

```
[00:19:50-00:20:00 | episodic 10sec] A basketball coach wearing a white cap and black hoodie stands on an outdoor court, holding a clipboard and an orange device, instructing two young players. A text overlay reads, “SHOOT FROM HALF COURT 5 TIMES WITH SHOT COACH.” The coach interacts with one player, adjusting a wristband or device on his wrist, while the other player watches. The scene takes place on a sunny day, with a basketball hoop and surrounding greenery visible in the background.
```

**txt6**

```
[00:08:30-00:09:00 | episodic 30sec] Three men are on an outdoor basketball court, engaging in a dynamic discussion and demonstration of basketball drills under sunny skies, with trees and a trampoline in the background. The man in the blue jersey leads the demonstration, using hand motions to explain movement techniques—such as “over the top of your hand” or “under”—while the other two men observe and interact. Their conversation touches on coaching methods, with one remarking that trainers sometimes “do way too much,” indicating a critical or reflective tone toward training intensity.

Later, the man in the black hoodie takes a shot at the hoop, and the ball is shown successfully going through the net. The group discusses the shot, with one noting it was “too far” and possibly “cheating,” suggesting a playful or analytical critique of the attempt.

In a subsequent sequence, the same man in the black hoodie and white cap shoots again, and each successful shot is visually reinforced with graphic overlays of basketballs multiplying on screen. He celebrates with a “Woo!” as the ball goes in, and the word “WHOOOOOO” flashes on screen as he raises his arms triumphantly, emphasizing the joy and energy of the moment.
```

**txt7** (cited)

```
[00:18:30-00:19:00 | episodic 30sec] Three men gather on an outdoor basketball court under a clear blue sky, initiating a playful game governed by the rule “FIRST MADE SHOT SHOOTS SILLY STRING AT LOSER.” The man in the blue jersey (No. 2) leads the setup, gesturing and explaining the rules while the others prepare—his left-hand counterpart in a black t-shirt readies an item, and the man in the black hoodie and white cap holds a basketball, listening attentively. The camera then cuts to all three holding basketballs, signaling readiness, with a house and hoop visible in the background.

As the countdown from three to one flashes on screen, all three jump simultaneously and shoot their basketballs toward the hoop. Each ball arcs perfectly into the basket, marking a synchronized success that triggers the game’s next phase.

The man in the blue jersey is declared the winner via on-screen text, and he celebrates briefly before approaching the man in the black hoodie and white cap. The latter gestures toward him, appearing to congratulate or acknowledge his victory. The scene remains set in a sunny backyard, with the hoop, landscaping, and a trampoline visible, underscoring the casual, competitive, and lighthearted nature of the event.
```

**txt8**

```
[00:19:40-00:19:50 | episodic 10sec] A man in a black hoodie and white cap stands at an outdoor basketball court, holding a piece of paper and an orange "SHOT COACH" training device. He appears to be giving instructions, with a young man in a blue jersey standing nearby. The video transitions to a close-up of the orange Shot Coach device, highlighting its branding, before returning to the man as a text overlay reads "SHOOT FROM HALF COURT."
```

**txt9**

```
[video-level knowledge | semantic] (player, can dribble, basketball)
```

**txt10**

```
[video-level knowledge | semantic] (man, is on, outdoor basketball court)
```

**txt11**

```
[video-level knowledge | semantic] (challenge, penalizes least baskets with, 100 sit-ups)
```

**txt12**

```
[video-level knowledge | semantic] (player, can be defended by, another player)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:03:35 | 00:03:30–00:03:40 | `-QuCz7kxBr8:visual:00033000` | `outputs/p9p19_check_20261025_141401/frames_s2/-QuCz7kxBr8/00033000.jpg` |
| img2 |  | 00:03:15 | 00:03:10–00:03:20 | `-QuCz7kxBr8:visual:00031000` | `outputs/p9p19_check_20261025_141401/frames_s2/-QuCz7kxBr8/00031000.jpg` |
| img3 |  | 00:34:45 | 00:34:40–00:34:50 | `-QuCz7kxBr8:visual:00344000` | `outputs/p9p19_check_20261025_141401/frames_s2/-QuCz7kxBr8/00344000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:03:30-00:03:40 | video frame at 215.0s] On an outdoor basketball court, three men are engaged in a game. One man in a blue jersey is preparing to shoot a basketball, while another in a red hoodie bends down to pick up a ball near a measuring device on the court. A third man in a black hoodie stands nearby, holding a basketball. The man in red appears to be setting up for a shot or measuring his performance, while the man in blue prepares to shoot. The man in black watches and interacts with the others, with audible dialogue indicating encouragement and instructions about the challenge.
```

**img2**

```
[00:03:10-00:03:20 | video frame at 195.0s] On an outdoor basketball court, a man in a black hoodie and white cap is interacting with a basketball placed on a training device. He bends down, adjusts the ball, and then steps back, appearing to prepare for a shot or drill. Two other men stand nearby, one in a red hoodie and the other in a blue basketball jersey, both holding basketballs and observing. A fourth person, holding a camera, films the activity from the side. The scene is set under clear skies with trees and a fence in the background. The audio includes repeated “ah” sounds, possibly indicating surprise or commentary.
```

**img3**

```
[00:34:40-00:34:50 | video frame at 2085.0s] On an outdoor basketball court under a clear blue sky, a player in a white jersey and orange shoes, carrying large cylindrical training pads, prepares to defend against another player in a black shirt and pink shorts who is dribbling a basketball. The defender shuffles laterally, maintaining a low stance, while the dribbler moves around him. Several other people are visible in the background, some standing and watching, others engaged in their own activities. The court features a blue painted area with "HYPE" written on it, and a basketball hoop is visible at one end. Mountains can be seen in the distance behind a low wall.
```
