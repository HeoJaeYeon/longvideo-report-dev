# Section 6 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:20:00): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 26, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 6.7}`
- image request (2026-10-25 14:20:04): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 1.09}`
- L1 filter LLM call: prompt 12112 tokens, output 70 tokens, 5.5 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 3min | 00:36:00–00:39:00 | 1 / 0.032522 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_12` |
| txt2 |  | worldmm-episodic | 30sec | 00:36:30–00:37:00 | 2 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_73` |
| txt3 |  | worldmm-episodic | 10min | 00:30:00–00:40:00 | 3 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10min_3` |
| txt4 |  | worldmm-episodic | 3min | 00:09:00–00:12:00 | 4 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_3` |
| txt5 | ✓ | worldmm-episodic | 10sec | 00:37:20–00:37:30 | 5 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_224` |
| txt6 | ✓ | worldmm-episodic | 30sec | 00:37:00–00:37:30 | 6 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_74` |
| txt7 |  | worldmm-episodic | 10min | 00:20:00–00:30:00 | 7 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10min_2` |
| txt8 |  | worldmm-episodic | 30sec | 00:05:00–00:05:30 | 8 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_10` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.031778 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_138` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_152` |
| txt11 | ✓ | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_151` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016129 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_139` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:36:00-00:39:00 | episodic 3min] A basketball training session unfolds on an outdoor court under clear skies, featuring structured drills centered around defensive shields. A player in a black shirt maneuvers around a defender in a white hoodie labeled “2HYPE,” who uses large black training pads and low, reactive stances. A third player in a blue shirt receives passes and prepares to shoot, while spectators observe from the perimeter. The court features “2HYPE” branding and scenic mountain views beyond a low wall, emphasizing the physicality and focus of the drills.

The scene transitions to a one-on-one game where the player in the white hoodie and blue shorts repeatedly shoots over a padded defender. After scoring, a graphic displays “2-1,” and the shooter smiles before preparing for the next play. The game continues with the same player driving to the basket, elevating for a shot as the defender contests, culminating in a successful swish. The final sequence shows the player celebrating with arms outstretched as on-screen text announces “3-1” and “ZAK JESSE & KRIS WIN,” followed by interaction with another player in a tie-dye jersey, while spectators watch from the court and a nearby wall.

The video opens with a young player in a “ZHYPE 2” jersey facing the camera before walking toward the basket, with other players nearby under a sunny sky and “ZHYPE” painted on the court floor. A tall player in a white and red “ZHYPE” jersey with the number 8 stands at the center, gesturing as if giving instructions, flanked by teammates — one holding a basketball and another in a hoodie — while others move around the perimeter. The scene concludes with the player raising his arms, two teammates beside him, one holding a basketball, before transitioning to a static end screen with “Thank you for watching,” “DON’T FORGET TO SUBSCRIBE!,” and the “F1HYPE” logo.
```

**txt2**

```
[00:36:30-00:37:00 | episodic 30sec] Two men compete in a one-on-one basketball game on an outdoor court under clear skies, with the player in the white hoodie and blue shorts repeatedly shooting over a defender using a padded training pad. After successfully scoring, a graphic overlay displays “2-1,” and the shooter smiles at the camera before preparing for the next play. The game continues with the same player driving to the basket, elevating for a shot while the defender contests, and the ball swishing through the net as the shooter celebrates. The final sequence shows the player in the white hoodie and patterned shorts celebrating with arms outstretched as on-screen text announces “3-1” and “ZAK JESSE & KRIS WIN,” followed by interaction with another player in a tie-dye jersey, while spectators watch from the court and a nearby wall.
```

**txt3**

```
[00:30:00-00:40:00 | episodic 10min] **[Event 1: Scoring Play and Defensive Engagement]**  
Under a bright, open-air “HYPE”-branded court surrounded by hills and greenery, a player in a white hoodie and patterned shorts drives past a defender in a blue jersey and scores a layup. The defender reacts with visible engagement, and both players briefly celebrate the play. Spectators—including a tie-dye-jerseyed man and a black-hoodied observer—watch from the sidelines. The scene then shifts to the same shooter, now in a white shirt, preparing to shoot again as the blue-jerseyed defender, wearing padded arm sleeves, assumes a defensive stance, signaling the continuation of a competitive, structured session.

**[Event 2: Training Drill and Shot Execution]**  
The white-shirted shooter takes a clean shot while the blue-jerseyed defender, now equipped with large black training pads, attempts to contest. The shot goes in successfully, and the defender, still holding the pads, walks toward the camera while the shooter gestures and speaks to him, suggesting post-shot communication or feedback. A “1-1” graphic appears on screen, marking the score. The scene transitions to a new matchup: a black-shirted player in pink shorts dribbles past a white-shirted defender holding pads, with other players observing under the same sunny, mountainous backdrop, indicating a rotating drill format designed to simulate real-game defensive pressure.

**[Event 3: Defensive Transition and Post-Play Interaction]**  
The black-shirted player drives to the basket and scores over the defender, who reacts with a celebratory gesture as the ball swishes through the net. Three onlookers laugh and smile near a wall, observing the action. The video concludes with the white-hoodied shooter standing near the hoop, holding pads, as the blue-jerseyed defender walks away, reinforcing the ongoing training or game dynamic. The consistent setting—outdoor court, clear skies, mountains, and residential elements—remains throughout, with cameramen documenting the action.

**[Event 4: Dunk and Score Overlay]**  
A player wearing a #2 jersey executes a dunk, triggering a “2-1” graphic on screen. The play is followed by a brief interaction between the dunker and the defender, who appears to acknowledge the score. The scene transitions to another offensive play: a white hoodie dribbler, now defended by a black-shirted player, takes a shot that goes in. The defender reacts with a celebratory gesture, reinforcing the competitive and interactive nature of the session.

**[Event 5: Final Scoring and Team Celebration]**  
The white hoodie player celebrates with arms outstretched after scoring, as on-screen text announces “3-1” and “ZAK JESSE & KRIS WIN.” The player then interacts with another player in a tie-dye jersey, while spectators watch from the court and a nearby wall. The sequence emphasizes camaraderie and team success, with score overlays and player reactions highlighting the competitive energy and social atmosphere of the game.

**[Event 6: Instructional Segment and Closing]**  
The video opens with a young player in a “ZHYPE 2” jersey facing the camera before walking toward the basket, with other players nearby under a sunny sky and “ZHYPE” painted on the court floor. A tall player in a white and red “ZHYPE” jersey with the number 8 stands at the center, gesturing as if giving instructions, flanked by teammates—one holding a basketball and another in a hoodie—while others move around the perimeter. The scene concludes with the player raising his arms, two teammates beside him, one holding a basketball, before transitioning to a static end screen with “Thank you for watching,” “DON’T FORGET TO SUBSCRIBE!,” and the “F1HYPE” logo.

This sequence captures a dynamic, structured basketball training or game session under clear skies, featuring a mix of one-on-one matchups, defensive drills with padded shields, and score overlays that track progression. The consistent branding (“HYPE,” “ZHYPE,” “F1HYPE”) and scenic backdrop unify the action, while player interactions, score updates, and celebratory gestures emphasize both athletic execution and the social, recreational atmosphere of the event.
```

**txt4**

```
[00:09:00-00:12:00 | episodic 3min] A man in a black hoodie and white cap demonstrates a basketball drill on an outdoor court, successfully shooting and gesturing to explain technique, enhanced by animated graphics. He acknowledges tech-assisted visuals, praising a teammate in a blue jersey, then encourages another player in a red hoodie with “You look like you're hot right now, bro,” reinforcing camaraderie during a casual game. 

The player in the red hoodie makes a shot, humorously noting the ball nearly slipped off his pinky finger. He pauses, gestures while holding a wristband, removes it, and reflects on his performance. He critiques his flick motion, acknowledging lack of straightness, before preparing for another attempt, observed by two onlookers in black and blue attire.

Meanwhile, the player in the blue jersey makes three consecutive shots, confirmed by on-screen text “3 MADE BASKETS,” then later scores again, reaching “4 MADE BASKETS.” He celebrates while speaking casually, with graphics of basketballs and audio commentary referencing conditioning and sit-ups. The branded “HYPER” court and clear skies frame the scene.

Separately, the man in the black hoodie performs sit-ups on a concrete court, with on-screen text “CASH LOST,” explained by voiceover as punishment for fewest flick shots. A blonde-bearded man in red watches and speaks animatedly. Later, the same man continues sit-ups beside a pool, where a graphic displays “SCORE 7” as he gestures and celebrates with two teammates — one in pink shorts, the other in a “SHY 2” jersey — in a lively, sunlit setting.

The group, including a man in a “ZHYPE” jersey and hoodie, gathers for discussion, holding a basketball with a “POWERHANDZ Dribble Sleeve” overlay, preparing for a demonstration or game. The scene remains focused on strategy and play, with the score updating to “SCORE 7,” reinforcing the competitive yet casual tone.
```

**txt5** (cited)

```
[00:37:20-00:37:30 | episodic 10sec] A basketball player in a white and red jersey with the number 8 stands on an outdoor court, gesturing with his arms raised. Two other men stand beside him, one holding a basketball. In the background, other people are moving around the court. The scene then transitions to a static end screen with a blue and white graphic design, displaying the text “Thank you for watching” and “DON’T FORGET TO SUBSCRIBE!” along with the “F1HYPE” logo.
```

**txt6** (cited)

```
[00:37:00-00:37:30 | episodic 30sec] A young basketball player in a "ZHYPE 2" jersey begins on an outdoor court, facing the camera before turning and walking toward the basket; other players are visible nearby, including one holding a ball, under a sunny sky with mountains in the background and “ZHYPE” painted on the court floor.

A tall player in a white and red “ZHYPE” jersey with the number 8 stands at the center of the court, gesturing as if giving instructions, flanked by teammates — one holding a basketball and another in a hoodie — while others move around the perimeter under a clear blue sky, with trees and hills in the background.

The scene concludes with the same player raising his arms in gesture, as two teammates stand beside him, one holding a basketball, before transitioning to a static end screen featuring a blue and white graphic, the text “Thank you for watching” and “DON’T FORGET TO SUBSCRIBE!”, alongside the “F1HYPE” logo.
```

**txt7**

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

**txt8**

```
[00:05:00-00:05:30 | episodic 30sec] A player in a white shirt and patterned shorts shoots a basketball on an outdoor court, successfully making the shot as the ball arcs through the hoop; the camera captures the ball entering the net and cuts to the shooter looking on, while the scoreboard briefly shows “0/1” as a player in a white jersey walks toward them.

The same shooter attempts multiple more shots, missing several, with the scoreboard updating from 0/1 to 0/3. A person in a red and white jersey stands nearby holding a ball and observing, while another in a white shirt and blue shorts stands near the hoop. The shooter pauses, inspecting their elbow, seemingly questioning its positioning, before the segment ends.

Continuing on the same court, the shooter takes additional shots, with a score counter tracking each attempt. A person in a white hoodie stands nearby, reacting to the misses. Audio includes dialogue expressing frustration and self-deprecation, including phrases like “I’m just bad” and “It’s throwing me off, you know?”
```

**txt9**

```
[video-level knowledge | semantic] (graphic overlay, shows, close-up of player)
```

**txt10**

```
[video-level knowledge | semantic] (F1HYPE, appears in video, at top left corner)
```

**txt11** (cited)

```
[video-level knowledge | semantic] (video, has, static end screen with blue and white graphic design and subscription prompts)
```

**txt12**

```
[video-level knowledge | semantic] (graphic overlay, reads, reading '1-1')
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:32:05 | 00:32:00–00:32:10 | `-QuCz7kxBr8:visual:00320000` | `outputs/p9p19_check_20261025_141401/frames_s0/-QuCz7kxBr8/00320000.jpg` |
| img2 |  | 00:29:35 | 00:29:30–00:29:40 | `-QuCz7kxBr8:visual:00293000` | `outputs/p9p19_check_20261025_141401/frames_s0/-QuCz7kxBr8/00293000.jpg` |
| img3 |  | 00:36:25 | 00:36:20–00:36:30 | `-QuCz7kxBr8:visual:00362000` | `outputs/p9p19_check_20261025_141401/frames_s0/-QuCz7kxBr8/00362000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:32:00-00:32:10 | video frame at 1925.0s] On an outdoor basketball court under a clear blue sky, two players are engaged in a game. One player in a blue jersey dribbles the ball while being guarded by a player in a white shirt. The player in white attempts a shot, successfully making the basket. After the shot, both players celebrate, with the player in white raising his arms in triumph. Other individuals are visible on the sidelines, watching the game. The court features a blue painted area with the word "HYPE" written on it, and a basketball hoop stands at one end. Mountains are visible in the background.
```

**img2**

```
[00:29:30-00:29:40 | video frame at 1775.0s] On an outdoor basketball court under a clear blue sky, a player in a red and white jersey dribbles the ball while being guarded by a man in a black hoodie holding a large padded training cylinder. The player maneuvers around the defender, who lunges forward in an attempt to block. The scene progresses as the player drives toward the basket, leaps into the air, and attempts a shot over the defender, who also jumps to contest the shot. Other individuals are visible on the court, observing the play.
```

**img3**

```
[00:36:20-00:36:30 | video frame at 2185.0s] On an outdoor basketball court under a clear blue sky, a player in a black shirt dribbles a basketball while another player in a white shirt and blue shorts, carrying a large padded training shield, defends him. The dribbler moves around the court, and as the segment progresses, he passes the ball to a third player in a blue jersey who takes possession and prepares to shoot. Other people are visible in the background, some watching from the sidelines and others sitting on a wall. The court is marked with blue and white lines, and a basketball hoop stands at one end.
```
