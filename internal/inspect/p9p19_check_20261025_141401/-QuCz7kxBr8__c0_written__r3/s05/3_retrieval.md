# Section 5 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:25:01): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 25, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 6.74}`
- image request (2026-10-25 14:25:04): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 1.27}`
- L1 filter LLM call: prompt 11237 tokens, output 71 tokens, 5.5 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 30sec | 00:25:00–00:25:30 | 1 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_50` |
| txt2 | ✓ | worldmm-episodic | 3min | 00:24:00–00:27:00 | 2 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_8` |
| txt3 |  | worldmm-episodic | 10min | 00:20:00–00:30:00 | 3 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10min_2` |
| txt4 |  | worldmm-episodic | 30sec | 00:24:30–00:25:00 | 4 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_49` |
| txt5 | ✓ | worldmm-episodic | 30sec | 00:29:00–00:29:30 | 5 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_58` |
| txt6 |  | worldmm-episodic | 10sec | 00:24:50–00:25:00 | 6 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_149` |
| txt7 | ✓ | worldmm-episodic | 3min | 00:33:00–00:36:00 | 7 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_11` |
| txt8 | ✓ | worldmm-episodic | 30sec | 00:28:00–00:28:30 | 8 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_56` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.03101 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_128` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_36` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_31` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_44` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:25:00-00:25:30 | episodic 30sec] **[Event 1: Product Introduction and Setup]**  
The video opens with a close-up of the “NEVER ENDING DEFENDER” product on a table outdoors, setting the stage for a basketball-themed challenge. Three men gather around the table on a sunny court: one in a black t-shirt and pink shorts, another in a gray hoodie and cap, and a third in a blue basketball jersey. The man in the black t-shirt begins explaining the rules, with text overlays appearing that read “TAKE 2 SHOTS FROM TOP OF THE KEY” and “EACH SHOT MADE = BURPEE FORFEIT,” establishing the challenge’s structure. The man in the hoodie holds basketball net equipment, while the man in the jersey listens attentively, occasionally adjusting his stance or hair.

**[Event 2: Product Unboxing and Demonstration]**  
The man in the black t-shirt opens a box and reveals the “Basketball Training Harness,” showing its packaging featuring a basketball player in the harness. The man in the blue jersey watches with amusement, adjusting his jersey, while the third man observes closely. The man in the black t-shirt then begins to put on the harness himself, adjusting the straps while the others watch, indicating the product’s intended use for training and performance enhancement. The scene maintains a casual, outdoor setting with a pool, trees, and clear sky in the background, reinforcing the recreational and athletic context of the event.
```

**txt2** (cited)

```
[00:24:00-00:27:00 | episodic 3min] **[Event 1: Product Introduction and Setup]**  
The video opens on a sunny outdoor basketball court with three men gathered around a white table displaying the “NEVER ENDING DEFENDER” training device. A man in a black t-shirt explains the challenge rules via text overlays: “TAKE 2 SHOTS FROM TOP OF THE KEY” and “EACH SHOT MADE = BURPEE FORFEIT.” The man in a gray hoodie holds net equipment, while the third, in a blue jersey, observes attentively, adjusting his stance. The setting reinforces the recreational, athletic tone with a pool and trees in the background.

**[Event 2: Product Unboxing and Demonstration]**  
The black-t-shirted man unboxes the “Basketball Training Harness,” revealing its packaging with a basketball player in the harness. The blue-jerseyed man watches with amusement, adjusting his jersey, while the hoodie-wearing observer watches closely. The man then begins fitting the harness himself, demonstrating its use, as the group watches—establishing the product’s purpose for performance training.

**[Event 3: Shooting Challenge and Scoring]**  
The man in the black shirt and pink shorts attempts his first shot, missing it. The score counter reads “0/1.” He retrieves the ball, prepares for a second shot, and aims again, while the observer in the hoodie remains still. After missing again, he turns with a surprised expression as the camera blurs briefly before refocusing on the hoodie-wearing man laughing and gesturing. The scene cuts to him taking his own shot, missing, then turning to smile at the camera as he walks toward a player in a tie-dye jersey. The score remains “0/1.”

**[Event 4: Successful Shot and Transition]**  
The blue-jerseyed player steps up, takes a shot, and makes it—graphic updates to “1/1.” He retrieves another ball, takes a second shot, and the graphic updates to “1/2” as the ball swishes through the hoop. The scene ends with him turning to the camera, the scoreboard confirming his success, and the group’s attention shifting to the next participant.
```

**txt3**

```
[00:20:00-00:30:00 | episodic 10min] **[Event 1: Product Introduction and Setup]**  
Under bright sunlight on a residential outdoor basketball court, three men gather around a white table displaying the “NEVER ENDING DEFENDER” training device. A man in a black t-shirt explains the challenge rules via text overlays: “TAKE 2 SHOTS FROM TOP OF THE KEY” and “EACH SHOT MADE = BURPEE FORFEIT.” The man in a gray hoodie holds net equipment, while the third, in a blue jersey, observes attentively, adjusting his stance. The setting reinforces the recreational, athletic tone with a pool and trees in the background.

**[Event 2: Product Unboxing and Demonstration]**  
The black-t-shirted man unboxes the “Basketball Training Harness,” revealing its packaging with a basketball player in the harness. The blue-jerseyed man watches with amusement, adjusting his jersey, while the hoodie-wearing observer watches closely. The man then begins fitting the harness himself, demonstrating its use, as the group watches—establishing the product’s purpose for performance training.

**[Event 3: Shooting Challenge and Scoring]**  
The man in the black shirt and pink shorts attempts his first shot, missing it. The score counter reads “0/1.” He retrieves the ball, prepares for a second shot, and aims again, while the observer in the hoodie remains still. After missing again, he turns with a surprised expression as the camera blurs briefly before refocusing on the hoodie-wearing man laughing and gesturing. The scene cuts to him taking his own shot, missing, then turning to smile at the camera as he walks toward a player in a tie-dye jersey. The score remains “0/1.”

**[Event 4: Successful Shot and Transition]**  
The blue-jerseyed player steps up, takes a shot, and makes it—graphic updates to “1/1.” He retrieves another ball, takes a second shot, and the graphic updates to “1/2” as the ball swishes through the hoop. The scene ends with him turning to the camera, the scoreboard confirming his success, and the group’s attention shifting to the next participant.

**[Event 5: Game Setup and Rules Introduction]**  
Six men gather on an outdoor basketball court under bright sunlight, with mountains and trees in the background. A man in a white hoodie and patterned shorts leads the group, holding two large black training pads and explaining the rules — “FIRST TO 3 WINS” and “LOSER DOES FORFEIT.” The group listens attentively, some adjusting posture or hair. The camera zooms in on a speaker in a black hoodie and white cap before returning to a wide shot. A video game-style overlay briefly appears, reinforcing the competitive tone. The scene transitions from a smaller group to the full team assembled for a briefing.

**[Event 6: Synchronized Routine and Scoring Segment]**  
Two men perform a choreographed routine on the blue-painted “HYPE” court: alternating between push-ups and jumping with arms raised. A third man in a blue jersey observes from the sidelines. Later, one man in a black hoodie and grey pants celebrates with jumps and raised arms while his counterpart in a black t-shirt and pink shorts completes push-ups — a turn-based game with a visible “SCORE 8” graphic. The setting remains sunny, with a basketball hoop and fence in the background.

**[Event 7: Casual Discussion and Product Preference]**  
Three men engage in a relaxed conversation on the court. The man in the black hoodie and white cap gestures while asking, “WHICH WAS YOUR FAVORITE PRODUCT?” The man in the blue jersey with number 2 listens with hands on hips, while the man in the black t-shirt and pink shorts responds, gesturing upward — prompting a smile from the hoodie-wearer. A yellow measuring tape near a pole suggests setup activity. The scene is set in a grassy, tree-lined backyard environment.

**[Event 8: Defensive Drill and Play Execution]**  
A player in a red and white jersey dribbles past a defender in a black hoodie holding a padded training cylinder. The offensive player drives to the basket, leaps for a shot, and is contested by the defender who also jumps. Other players observe from the sidelines. The scene is set against greenery and a white wall, with distant mountains visible. The interaction is dynamic, with laughter and engagement from the group. The video ends with a player in a black shirt and pink shorts raising his hands in amusement.
```

**txt4**

```
[00:24:30-00:25:00 | episodic 30sec] Three men are gathered on an outdoor basketball court under a clear blue sky, engaging in a product demonstration. Initially, one man in a white t-shirt and patterned shorts holds a small device while another in a white hoodie examines a similar device; a third, in a red and white jersey, holds a basketball. A graphic overlay displays “SCORE 2,” indicating a scoring or performance metric. The scene transitions to a different area of the court where two men stand near a table holding various items, including an orange device and a black strap. One man, in a blue jersey with the number 2, gestures while speaking to the other, who holds the orange device; a third man in a hoodie and cap observes. The focus then shifts to a white table where a man in a black t-shirt gestures and presents a product box to the group. The second man, in a black hoodie and white cap, watches attentively, while the third, in a blue jersey, stands with hands on hips, observing. The camera zooms in on the product — a black training device labeled “NEVER ENDING DEFENDER,” featuring an image of a basketball player — highlighting its design and branding.
```

**txt5** (cited)

```
[00:29:00-00:29:30 | episodic 30sec] **Six men gather on an outdoor basketball court under a clear blue sky to begin a competitive game.** One man in a white hoodie and patterned shorts holds two large black training pads, gesturing as he explains the rules to the group; text on screen confirms the format: “FIRST TO 3 WINS” and “LOSER DOES FORFEIT.” The group, dressed in athletic wear, listens intently. The camera shifts to show a player in a white jersey preparing to throw one of the pads, while others observe. A brief video game-style overlay appears, showing a first-person perspective and a scoreboard, emphasizing the competitive nature of the game. Later, a player in a white and red “ZHYTE 2” jersey, still holding the pads, stretches his arms wide before lowering them to face a man in a black hoodie and white cap who holds a basketball. A third man in a blue jersey stands in the background with arms crossed, as mountains loom in the distance under the bright sun.
```

**txt6**

```
[00:24:50-00:25:00 | episodic 10sec] Three men stand around a white table outdoors on a basketball court under a clear blue sky. One man in a black t-shirt gestures with his hands while speaking, then picks up a product box and shows it to the others. The second man, wearing a black hoodie and white cap, watches him. The third man, in a blue basketball jersey, stands with his hands on his hips, looking at the product. The camera zooms in on the product, which is a black training device with the text "NEVER ENDING DEFENDER" prominently displayed over the image of a basketball player.
```

**txt7** (cited)

```
[00:33:00-00:36:00 | episodic 3min] A dynamic outdoor basketball session unfolds on a court marked “HYPE,” under clear blue skies and framed by hills and greenery. Players in varied jerseys—white, black, red-and-white, blue—engage in drills and one-on-one matchups, often using large padded training devices for defensive simulation. Key moments include a dunk by a #2 player triggering a “2-1” graphic, a successful shot by a white hoodie dribbler while defended by a black-shirted player, and multiple scoring plays amid shifting defensive pressure. Spectators, including a cameraman, observe from the perimeter, while coaches and teammates provide guidance or interact off-court. The sequence captures fluid transitions between offense, defense, and scoring, with score overlays and player reactions emphasizing competitive energy. The court’s branding, natural backdrop, and consistent sunny lighting unify the action, highlighting both athletic execution and the social, recreational atmosphere of the game.
```

**txt8** (cited)

```
[00:28:00-00:28:30 | episodic 30sec] Three men are gathered on an outdoor basketball court under a clear blue sky, engaging in a casual discussion. The man in the black hoodie and white cap gestures while speaking, with a text overlay asking, “WHICH WAS YOUR FAVORITE PRODUCT?” The man in the blue jersey with the number 2 stands with hands on hips, attentively listening, while the man in the black t-shirt and pink shorts holds a small object and responds, gesturing upward — prompting a smile from the hoodie-wearer. A yellow measuring tape is visible near a black pole, suggesting a possible measurement or setup activity. The setting includes grass, trees, and a fence, reinforcing the backyard or recreational court environment. The conversation appears focused on product preference, with active participation and visual cues indicating engagement and light interaction among the group.
```

**txt9**

```
[video-level knowledge | semantic] (player, can use, training pad to block)
```

**txt10**

```
[video-level knowledge | semantic] (challenge, penalizes least baskets with, 100 sit-ups)
```

**txt11**

```
[video-level knowledge | semantic] (device, is on, table)
```

**txt12**

```
[video-level knowledge | semantic] (The text overlay, reads, 20 LOW, MEDIUM, & HIGH DRIBBLES IN 60 SECONDS)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:31:15 | 00:31:10–00:31:20 | `-QuCz7kxBr8:visual:00311000` | `outputs/p9p19_check_20261025_141401/frames_s2/-QuCz7kxBr8/00311000.jpg` |
| img2 |  | 00:26:55 | 00:26:50–00:27:00 | `-QuCz7kxBr8:visual:00265000` | `outputs/p9p19_check_20261025_141401/frames_s2/-QuCz7kxBr8/00265000.jpg` |
| img3 |  | 00:33:55 | 00:33:50–00:34:00 | `-QuCz7kxBr8:visual:00335000` | `outputs/p9p19_check_20261025_141401/frames_s2/-QuCz7kxBr8/00335000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:31:10-00:31:20 | video frame at 1875.0s] On an outdoor basketball court under a clear blue sky, a player in a black hoodie and white cap dribbles the ball while being guarded by an opponent in a white shirt holding a large black pad. The player in black makes a move, shoots the ball, and it goes into the hoop. The camera then cuts to a close-up of the player in black, who smiles as a graphic overlay displays "1-0". He turns to face the court as the scene shifts to a new play, where a different player in a black shirt and orange sneakers prepares to dribble while being guarded by the same player with the pad. Other players stand nearby, watching the action unfold.
```

**img2**

```
[00:26:50-00:27:00 | video frame at 1615.0s] A man in a blue basketball jersey stands on an outdoor court, holding a basketball. He takes a shot, and the ball arcs toward the hoop. After the ball goes in, he turns to look at the camera, and a graphic appears on screen indicating "1/1". He then retrieves another ball, takes a second shot, and the graphic updates to "1/2" as he watches the ball go through the hoop.
```

**img3**

```
[00:33:50-00:34:00 | video frame at 2035.0s] On an outdoor basketball court under a clear blue sky, a young man in a white shirt and patterned shorts dribbles a basketball while being guarded by another man holding a large padded training pad. The guard moves laterally, attempting to block the dribbler’s path. Other individuals are present on the court, including a person with a camera filming the drill, and others standing by, observing. The court features a blue painted area with “HYPE” written on it, and a basketball hoop is visible in the background.
```
