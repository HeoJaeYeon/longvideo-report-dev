# Section 4 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:18:29): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 25, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 6.48}`
- image request (2026-10-25 14:18:32): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 0.81}`
- L1 filter LLM call: prompt 10709 tokens, output 74 tokens, 5.2 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 3min | 00:18:00–00:21:00 | 1 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_6` |
| txt2 | ✓ | worldmm-episodic | 30sec | 00:18:00–00:18:30 | 2 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_36` |
| txt3 | ✓ | worldmm-episodic | 10sec | 00:18:30–00:18:40 | 3 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_111` |
| txt4 | ✓ | worldmm-episodic | 30sec | 00:25:00–00:25:30 | 4 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_50` |
| txt5 | ✓ | worldmm-episodic | 30sec | 00:18:30–00:19:00 | 5 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_37` |
| txt6 | ✓ | worldmm-episodic | 10sec | 00:18:20–00:18:30 | 6 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_110` |
| txt7 |  | worldmm-episodic | 30sec | 00:08:00–00:08:30 | 7 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_16` |
| txt8 |  | worldmm-episodic | 10sec | 00:08:20–00:08:30 | 8 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_50` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.032787 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_63` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.032258 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_36` |
| txt11 | ✓ | worldmm-semantic | — | no timestamp | 3 / 0.031754 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_62` |
| txt12 | ✓ | worldmm-semantic | — | no timestamp | 4 / 0.031746 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_123` |

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
[00:18:00-00:18:30 | episodic 30sec] **[Event 1: Introduction of Basketball Court Scene]**  
Three men are on an outdoor basketball court: one in a red and white jersey gestures while crouched, another in a white t-shirt bends and stands, and a third in a white hoodie holds a basketball. A graphic overlay reads “SCORE 8,” establishing a scoring context. The scene then cuts to a different spot on the same court, where a man in a black t-shirt examines a piece of paper while standing beside a man in a black hoodie holding a basketball; a third man in a blue jersey observes from behind.

**[Event 2: Product Demonstration Setup]**  
The scene transitions to three men gathered around a white table outdoors under a clear blue sky. The man in the black t-shirt holds and inspects a small white object, likely a product component, while the man in the blue jersey watches with a smile and the man in the black hoodie and white cap holds a basketball, listening attentively. The video then cuts to a product shot of three black basketball shooting aids, with an overlay reading “Pack of 3 Basketball Shooting Aid,” clearly introducing the product being demonstrated.

**[Event 3: Product Claim Announcement]**  
At timestamp 00:18:29, a text overlay appears stating “FIRST MADE SHOT SHOOTS GILLY STRING AT 100%,” signaling a performance claim tied to the product’s functionality — likely indicating the shooting aid enables a perfect shot using a gilly string (a type of projectile or training tool). This marks the culmination of the product introduction and setup, reinforcing the product’s intended use and effectiveness.
```

**txt3** (cited)

```
[00:18:30-00:18:40 | episodic 10sec] Three men stand on an outdoor basketball court under a clear blue sky. A text overlay reads, "FIRST MADE SHOT SHOOTS SILLY STRING AT LOSER." The man in the center, wearing a blue basketball jersey with the number 2, holds a small object and gestures with his hand while speaking. The man on the left, in a black t-shirt, looks down at his hands, appearing to prepare something. The man on the right, in a black hoodie and white cap, holds a basketball and listens. The camera then focuses on the man in the blue jersey as he continues to gesture and speak. The scene shifts to show all three men standing together, each now holding a basketball, with a house and a basketball hoop visible in the background.
```

**txt4** (cited)

```
[00:25:00-00:25:30 | episodic 30sec] **[Event 1: Product Introduction and Setup]**  
The video opens with a close-up of the “NEVER ENDING DEFENDER” product on a table outdoors, setting the stage for a basketball-themed challenge. Three men gather around the table on a sunny court: one in a black t-shirt and pink shorts, another in a gray hoodie and cap, and a third in a blue basketball jersey. The man in the black t-shirt begins explaining the rules, with text overlays appearing that read “TAKE 2 SHOTS FROM TOP OF THE KEY” and “EACH SHOT MADE = BURPEE FORFEIT,” establishing the challenge’s structure. The man in the hoodie holds basketball net equipment, while the man in the jersey listens attentively, occasionally adjusting his stance or hair.

**[Event 2: Product Unboxing and Demonstration]**  
The man in the black t-shirt opens a box and reveals the “Basketball Training Harness,” showing its packaging featuring a basketball player in the harness. The man in the blue jersey watches with amusement, adjusting his jersey, while the third man observes closely. The man in the black t-shirt then begins to put on the harness himself, adjusting the straps while the others watch, indicating the product’s intended use for training and performance enhancement. The scene maintains a casual, outdoor setting with a pool, trees, and clear sky in the background, reinforcing the recreational and athletic context of the event.
```

**txt5** (cited)

```
[00:18:30-00:19:00 | episodic 30sec] Three men gather on an outdoor basketball court under a clear blue sky, initiating a playful game governed by the rule “FIRST MADE SHOT SHOOTS SILLY STRING AT LOSER.” The man in the blue jersey (No. 2) leads the setup, gesturing and explaining the rules while the others prepare—his left-hand counterpart in a black t-shirt readies an item, and the man in the black hoodie and white cap holds a basketball, listening attentively. The camera then cuts to all three holding basketballs, signaling readiness, with a house and hoop visible in the background.

As the countdown from three to one flashes on screen, all three jump simultaneously and shoot their basketballs toward the hoop. Each ball arcs perfectly into the basket, marking a synchronized success that triggers the game’s next phase.

The man in the blue jersey is declared the winner via on-screen text, and he celebrates briefly before approaching the man in the black hoodie and white cap. The latter gestures toward him, appearing to congratulate or acknowledge his victory. The scene remains set in a sunny backyard, with the hoop, landscaping, and a trampoline visible, underscoring the casual, competitive, and lighthearted nature of the event.
```

**txt6** (cited)

```
[00:18:20-00:18:30 | episodic 10sec] The video begins with a product shot of three black basketball shooting aids, overlaid with the text "Pack of 3 Basketball Shooting Aid." The scene then transitions to an outdoor setting under a clear blue sky, where three men stand around a white table. One man, wearing a black t-shirt and holding a small object, appears to be explaining something to the other two. The man in the center wears a blue basketball jersey and smiles, while the man on the right, in a black hoodie and white cap, holds a basketball and listens attentively. At 00:18:29, a text overlay appears reading "FIRST MADE SHOT SHOOTS GILLY STRING AT 100%."
```

**txt7**

```
[00:08:00-00:08:30 | episodic 30sec] Three men on an outdoor basketball court prepare for a shooting challenge involving the Flick Glove — a device designed to improve basketball shooting technique. One man in a black hoodie and white cap, holding a basketball and the glove, explains the rules while gesturing, as the other two — one in a red hoodie and another in a blue jersey — observe. A text overlay instructs participants to take three shots with the glove, then three without, with the person making the fewest baskets required to do 100 sit-ups. The man in the red hoodie expresses confusion about the glove’s orientation, prompting the man in the black hoodie to demonstrate its use. The video opens with a close-up of the glove’s design — featuring finger loops and a rectangular screen — and later displays the three available color options (white, black, orange) with the brand name “FLICK GLOVE” overlaid, establishing the product’s purpose and setup for the upcoming demonstration.
```

**txt8**

```
[00:08:20-00:08:30 | episodic 10sec] Three men stand on an outdoor basketball court. A text overlay explains a challenge: take three shots with a flick glove, then three without, and the person making the least baskets must do 100 sit-ups. One man in a red hoodie reacts with surprise, while another in a blue jersey smiles. The third man, wearing a black hoodie and cap, holds a basketball and a black glove, examining it. The man in the red hoodie asks, “Bro, what are these? Which way does it even go?” as the man in the black hoodie holds up the glove.
```

**txt9**

```
[video-level knowledge | semantic] (NEVER ENDING DEFENDER, has text, NEVER ENDING DEFENDER)
```

**txt10**

```
[video-level knowledge | semantic] (challenge, penalizes least baskets with, 100 sit-ups)
```

**txt11** (cited)

```
[video-level knowledge | semantic] (NEVER ENDING DEFENDER, is, black training device)
```

**txt12** (cited)

```
[video-level knowledge | semantic] (player, can be defended by, another player)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:00:15 | 00:00:10–00:00:20 | `-QuCz7kxBr8:visual:00001000` | `outputs/p9p19_check_20261025_141401/frames_s0/-QuCz7kxBr8/00001000.jpg` |
| img2 | ✓ | 00:18:25 | 00:18:20–00:18:30 | `-QuCz7kxBr8:visual:00182000` | `outputs/p9p19_check_20261025_141401/frames_s0/-QuCz7kxBr8/00182000.jpg` |
| img3 |  | 00:14:55 | 00:14:50–00:15:00 | `-QuCz7kxBr8:visual:00145000` | `outputs/p9p19_check_20261025_141401/frames_s0/-QuCz7kxBr8/00145000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:00:10-00:00:20 | video frame at 15.0s] On an outdoor basketball court, a group of men gather with basketballs. One man in a blue jersey crouches near a training device, then stands up and looks upward. The camera shifts to show a man in a black hoodie and cap, holding a basketball and speaking animatedly to the group. The scene transitions to a close-up of three black nylon straps with buckles, laid out on a white surface. Audio includes a greeting, a countdown, an exclamation, and an introduction to a video segment about testing viral basketball gadgets.
```

**img2** (cited)

```
[00:18:20-00:18:30 | video frame at 1105.0s] The video begins with a product shot of three black basketball shooting aids, overlaid with the text "Pack of 3 Basketball Shooting Aid." The scene then transitions to an outdoor setting under a clear blue sky, where three men stand around a white table. One man, wearing a black t-shirt and holding a small object, appears to be explaining something to the other two. The man in the center wears a blue basketball jersey and smiles, while the man on the right, in a black hoodie and white cap, holds a basketball and listens attentively. At 00:18:29, a text overlay appears reading "FIRST MADE SHOT SHOOTS GILLY STRING AT 100%."
```

**img3**

```
[00:14:50-00:15:00 | video frame at 895.0s] Three men stand outdoors near a table with basketball gear. One man in a blue jersey puts on a pair of gloves while the other two watch. The text overlay reads "20 LOW, MEDIUM, & HIGH DRIBBLES IN 60 SECONDS." The man in the blue jersey then says, "IT'S LIKE THE THICC WOMEN OF GLOVES."
```
