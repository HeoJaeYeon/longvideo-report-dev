# Section 6 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:26:06): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 25, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 6.81}`
- image request (2026-10-25 14:26:08): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 0.43}`
- L1 filter LLM call: prompt 12347 tokens, output 69 tokens, 5.6 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 3min | 00:03:00–00:06:00 | 1 / 0.032258 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_1` |
| txt2 |  | worldmm-episodic | 30sec | 00:04:30–00:05:00 | 2 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_9` |
| txt3 |  | worldmm-episodic | 10sec | 00:04:30–00:04:40 | 3 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_27` |
| txt4 |  | worldmm-episodic | 30sec | 00:19:30–00:20:00 | 4 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_39` |
| txt5 | ✓ | worldmm-episodic | 10sec | 00:19:50–00:20:00 | 5 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_119` |
| txt6 | ✓ | worldmm-episodic | 3min | 00:18:00–00:21:00 | 6 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_6` |
| txt7 | ✓ | worldmm-episodic | 10min | 00:10:00–00:20:00 | 7 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10min_1` |
| txt8 |  | worldmm-episodic | 30sec | 00:24:30–00:25:00 | 8 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_49` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.032002 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_123` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.031498 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_129` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.03101 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_133` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_14` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:03:00-00:06:00 | episodic 3min] Three men gather on an outdoor basketball court, negotiating positions before settling into a shooting challenge. One man in a black hoodie and white cap adjusts a basketball on a training device while the others—wearing red and blue jerseys—observe, holding balls. A fourth person films the scene under clear skies, with trees and a fence in the background. The group transitions to a hoop with a vertical obstacle, where they take turns shooting under a 30-second countdown. Encouragement and light-hearted banter—such as “you might be safe just making it past that first one”—add to the casual yet competitive tone. The man in the black hoodie successfully makes his shot, smiling as he walks back, while the man in red watches amusedly. Their conversation hints at past forfeits and humorous self-deprecation.

The group then evaluates a dribble stick, with the man in the blue jersey rating it an 8/10, followed by the man in the black shirt agreeing, and the man in the black hoodie giving it a 7—joking that anything helping him fail is “pretty good.” The conversation remains lighthearted and collaborative.

Later, a man in a white hoodie demonstrates the “Straight Shooter Strap,” explaining how it stabilizes the elbow during shooting. He adjusts the strap on his arm while a third observer watches. The scene widens to show the full court, hoop, and surrounding hills under clear skies, setting up practical use of the device.

A shooter in a white shirt and patterned shorts begins a shooting sequence, initially making one shot (0/1), then missing several, with the scoreboard climbing to 0/3. He pauses, inspecting his elbow, seemingly frustrated. As the sequence continues, he scores more shots, pushing the tally to 3/16, with teammates retrieving balls and commentary tracking each attempt. The scoreboard climbs steadily, accompanied by remarks like “Dude, 15,” and “Zach’s uses this thing, bro.” The player smiles at the camera as he approaches 15 successful shots, with the backdrop of a large house and trees under clear skies.
```

**txt2**

```
[00:04:30-00:05:00 | episodic 30sec] A man in a white hoodie demonstrates a black elbow strap called the “Straight Shooter Strap” on an outdoor basketball court, explaining how it stabilizes the elbow during shooting by preventing it from flaring outward. He gestures to the player’s arm and elbow while showing close-ups of the strap with on-screen text. A third observer watches closely as the demonstrator adjusts the strap on his own arm, then steps back to prepare for a shooting challenge with the other player holding the ball. The scene widens to reveal the full court, hoop, fence, and surrounding hills under a clear sky, setting up the practical application of the strap in a real-game context.
```

**txt3**

```
[00:04:30-00:04:40 | episodic 10sec] Three men are on an outdoor basketball court. One man in a white hoodie holds a basketball and demonstrates a black strap called the "Straight Shooter Strap," explaining its use while the other two watch. The strap is shown in close-up with text overlay.
```

**txt4**

```
[00:19:30-00:20:00 | episodic 30sec] A basketball coach in a black hoodie and white cap stands on an outdoor court, using an orange “SHOT COACH” training device to instruct two young players, with a text overlay directing them to “SHOOT FROM HALF COURT 5 TIMES WITH SHOT COACH.” He adjusts a wristband or device on one player’s wrist while the other observes, all under bright sunlight with a hoop and greenery in the background. The coach holds a clipboard and gestures as he explains the drill, emphasizing precision and repetition through the Shot Coach system. The scene briefly cuts to a scoreboard graphic showing "-2" then resetting to "0," followed by a third man in a blue jersey crossing his arms and smiling as the scoreboard shows "-1," suggesting a playful or competitive scoring context. The coach and the player in the blue jersey later move to a table, where the coach appears to write or draw, possibly documenting progress or adjusting the training plan. The video closes with a close-up of the Shot Coach device, reinforcing its role as a key tool in the structured, tech-assisted shooting drill.
```

**txt5** (cited)

```
[00:19:50-00:20:00 | episodic 10sec] A basketball coach wearing a white cap and black hoodie stands on an outdoor court, holding a clipboard and an orange device, instructing two young players. A text overlay reads, “SHOOT FROM HALF COURT 5 TIMES WITH SHOT COACH.” The coach interacts with one player, adjusting a wristband or device on his wrist, while the other player watches. The scene takes place on a sunny day, with a basketball hoop and surrounding greenery visible in the background.
```

**txt6** (cited)

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

**txt7** (cited)

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

**txt8**

```
[00:24:30-00:25:00 | episodic 30sec] Three men are gathered on an outdoor basketball court under a clear blue sky, engaging in a product demonstration. Initially, one man in a white t-shirt and patterned shorts holds a small device while another in a white hoodie examines a similar device; a third, in a red and white jersey, holds a basketball. A graphic overlay displays “SCORE 2,” indicating a scoring or performance metric. The scene transitions to a different area of the court where two men stand near a table holding various items, including an orange device and a black strap. One man, in a blue jersey with the number 2, gestures while speaking to the other, who holds the orange device; a third man in a hoodie and cap observes. The focus then shifts to a white table where a man in a black t-shirt gestures and presents a product box to the group. The second man, in a black hoodie and white cap, watches attentively, while the third, in a blue jersey, stands with hands on hips, observing. The camera zooms in on the product — a black training device labeled “NEVER ENDING DEFENDER,” featuring an image of a basketball player — highlighting its design and branding.
```

**txt9**

```
[video-level knowledge | semantic] (player, can be defended by, another player)
```

**txt10**

```
[video-level knowledge | semantic] (player, can gesture and talk to, another player)
```

**txt11**

```
[video-level knowledge | semantic] (player, can be guarded by, another player)
```

**txt12**

```
[video-level knowledge | semantic] (player, uses, Straight Shooter Strap)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:34:45 | 00:34:40–00:34:50 | `-QuCz7kxBr8:visual:00344000` | `outputs/p9p19_check_20261025_141401/frames_s2/-QuCz7kxBr8/00344000.jpg` |
| img2 |  | 00:14:55 | 00:14:50–00:15:00 | `-QuCz7kxBr8:visual:00145000` | `outputs/p9p19_check_20261025_141401/frames_s2/-QuCz7kxBr8/00145000.jpg` |
| img3 |  | 00:33:55 | 00:33:50–00:34:00 | `-QuCz7kxBr8:visual:00335000` | `outputs/p9p19_check_20261025_141401/frames_s2/-QuCz7kxBr8/00335000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:34:40-00:34:50 | video frame at 2085.0s] On an outdoor basketball court under a clear blue sky, a player in a white jersey and orange shoes, carrying large cylindrical training pads, prepares to defend against another player in a black shirt and pink shorts who is dribbling a basketball. The defender shuffles laterally, maintaining a low stance, while the dribbler moves around him. Several other people are visible in the background, some standing and watching, others engaged in their own activities. The court features a blue painted area with "HYPE" written on it, and a basketball hoop is visible at one end. Mountains can be seen in the distance behind a low wall.
```

**img2**

```
[00:14:50-00:15:00 | video frame at 895.0s] Three men stand outdoors near a table with basketball gear. One man in a blue jersey puts on a pair of gloves while the other two watch. The text overlay reads "20 LOW, MEDIUM, & HIGH DRIBBLES IN 60 SECONDS." The man in the blue jersey then says, "IT'S LIKE THE THICC WOMEN OF GLOVES."
```

**img3**

```
[00:33:50-00:34:00 | video frame at 2035.0s] On an outdoor basketball court under a clear blue sky, a young man in a white shirt and patterned shorts dribbles a basketball while being guarded by another man holding a large padded training pad. The guard moves laterally, attempting to block the dribbler’s path. Other individuals are present on the court, including a person with a camera filming the drill, and others standing by, observing. The court features a blue painted area with “HYPE” written on it, and a basketball hoop is visible in the background.
```
