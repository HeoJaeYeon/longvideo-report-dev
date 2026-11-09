# Section 3 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:23:07): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 18, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 5.58}`
- image request (2026-10-25 14:23:10): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 1.18}`
- L1 filter LLM call: prompt 7528 tokens, output 71 tokens, 4.4 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 30sec | 00:04:30–00:05:00 | 1 / 0.048395 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_9` |
| txt2 |  | worldmm-episodic | 30sec | 00:10:00–00:10:30 | 2 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_20` |
| txt3 | ✓ | worldmm-episodic | 3min | 00:06:00–00:09:00 | 3 / 0.032522 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_2` |
| txt4 |  | worldmm-episodic | 10sec | 00:04:50–00:05:00 | 4 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_29` |
| txt5 | ✓ | worldmm-episodic | 10sec | 00:06:50–00:07:00 | 5 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_41` |
| txt6 | ✓ | worldmm-episodic | 30sec | 00:08:00–00:08:30 | 6 / 0.032266 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_16` |
| txt7 | ✓ | worldmm-episodic | 10sec | 00:08:20–00:08:30 | 7 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_50` |
| txt8 |  | worldmm-episodic | 30sec | 00:20:00–00:20:30 | 8 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_40` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.032018 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_14` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.03101 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_1` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_4` |
| txt12 | ✓ | worldmm-semantic | — | no timestamp | 4 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_32` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:04:30-00:05:00 | episodic 30sec] A man in a white hoodie demonstrates a black elbow strap called the “Straight Shooter Strap” on an outdoor basketball court, explaining how it stabilizes the elbow during shooting by preventing it from flaring outward. He gestures to the player’s arm and elbow while showing close-ups of the strap with on-screen text. A third observer watches closely as the demonstrator adjusts the strap on his own arm, then steps back to prepare for a shooting challenge with the other player holding the ball. The scene widens to reveal the full court, hoop, fence, and surrounding hills under a clear sky, setting up the practical application of the strap in a real-game context.
```

**txt2**

```
[00:10:00-00:10:30 | episodic 30sec] Three people are on an outdoor basketball court under a clear blue sky. A player in a red hoodie attempts a shot but misses; the ball arcs toward the hoop and falls short. The player in the blue jersey then takes a shot and successfully makes it, holding the ball afterward while smiling. Text overlays appear stating “3 MADE BASKETS,” indicating a scoring milestone or game objective. The scene transitions to another moment where the same player in the blue sleeveless shirt misses a shot, retrieves the ball, and prepares to shoot again. A second player in a red shirt stands near the basket, while a third in a black shirt and white cap watches from the side. Audio commentary references missing the first shot and adjusting to a “flick” motion, followed by a mention of needing to make two shots. Later, the player in the blue jersey—now wearing a blue basketball jersey—shoots again, this time successfully, with the ball arcing cleanly into the hoop. He turns to face the camera, holding the ball and speaking casually. Overlaid graphics of basketballs appear, and the audio includes informal conversation about making shots and the need to do sit-ups for conditioning. The court features a blue-painted area with the word “HYPER” visible, reinforcing the setting as a branded or themed outdoor court.
```

**txt3** (cited)

```
[00:06:00-00:09:00 | episodic 3min] A man in a white hoodie and patterned shorts shoots basketballs on a sunny court, with a score counter updating after each shot — from 0/0 to 3/5 — while a humorous voiceover references product ownership and investment. He praises the product as “great,” with a “#NOT SPONSORED” graphic. The scene cuts to another player resetting the score.

A second player makes a shot (1/2), but audio commentary criticizes the product’s performance, noting it “fell off” and “snaps” when extended. A shooting contest unfolds: a player in a red and white jersey (No. 2) makes a successful shot (2/5), celebrated with surprise and joy. Later, the tie-dye jersey player loses, prompting the white-shirted man to propose testing his jump shot without the strap to isolate the issue — a playful, lighthearted challenge.

His jump shot misses, sparking frustration and speculation about the strap. A teammate confirms the issue, and a forfeit of 30 jumping jacks is suggested. The man begins doing jumping jacks, arms raised, while two others watch and tease — one jokes about “bouncing titties,” another compares chest sizes. He deflects with humor, “Bro, I’m wearing a big shirt.” His movements become off-rhythm, drawing amused observation.

Three men discuss and humorously rate the product: the white-hoodie man (ZHYPE) calls it suitable for kids but suggests a better gadget for beginners, scoring it “1.” They escalate to exaggerated scoring — “1,” “2,” then “-3k” — ending with a playful “what’s the next invention?” 

A shooting challenge with the Flick Glove begins: one man in a black hoodie explains rules — three shots with the glove, then without — with the fewest baskets requiring 100 sit-ups. The red-hoodie man misunderstands the glove’s orientation, prompting a demonstration. The glove’s design (finger loops, screen) and color options (white, black, orange) are shown.

Three men demonstrate basketball drills under sunny skies, with the blue-jersey man explaining movement techniques. A shot by the black-hoodie man is debated — “too far,” “cheating.” Later, he makes another shot, celebrated with “Woo!” and “WHOOOOOO” graphics, emphasizing triumph and energy.
```

**txt4**

```
[00:04:50-00:05:00 | episodic 10sec] Two men are on an outdoor basketball court, one demonstrating a black elbow strap while holding a basketball. He explains how the strap will pull the elbow in and prevent it from flaring out. A third man joins them, and the demonstrator adjusts the strap on his arm. The scene then widens to show the full court as the men prepare for a challenge involving the strap.
```

**txt5** (cited)

```
[00:06:50-00:07:00 | episodic 10sec] On an outdoor basketball court, two players are engaged in a shooting contest. One player, wearing a white shirt and patterned shorts, holds a basketball and speaks, while the other, in a tie-dye jersey, adjusts his clothing. A scoreboard overlay shows their shooting stats, indicating the player in the jersey lost. The player in the white shirt suggests shooting without a strap to determine if his jump shot is broken or if the strap was the issue. The scene takes place in front of a large house on a sunny day.
```

**txt6** (cited)

```
[00:08:00-00:08:30 | episodic 30sec] Three men on an outdoor basketball court prepare for a shooting challenge involving the Flick Glove — a device designed to improve basketball shooting technique. One man in a black hoodie and white cap, holding a basketball and the glove, explains the rules while gesturing, as the other two — one in a red hoodie and another in a blue jersey — observe. A text overlay instructs participants to take three shots with the glove, then three without, with the person making the fewest baskets required to do 100 sit-ups. The man in the red hoodie expresses confusion about the glove’s orientation, prompting the man in the black hoodie to demonstrate its use. The video opens with a close-up of the glove’s design — featuring finger loops and a rectangular screen — and later displays the three available color options (white, black, orange) with the brand name “FLICK GLOVE” overlaid, establishing the product’s purpose and setup for the upcoming demonstration.
```

**txt7** (cited)

```
[00:08:20-00:08:30 | episodic 10sec] Three men stand on an outdoor basketball court. A text overlay explains a challenge: take three shots with a flick glove, then three without, and the person making the least baskets must do 100 sit-ups. One man in a red hoodie reacts with surprise, while another in a blue jersey smiles. The third man, wearing a black hoodie and cap, holds a basketball and a black glove, examining it. The man in the red hoodie asks, “Bro, what are these? Which way does it even go?” as the man in the black hoodie holds up the glove.
```

**txt8**

```
[00:20:00-00:20:30 | episodic 30sec] A man in a black hoodie and white cap demonstrates a hand-restraint device with orange straps on an outdoor basketball court, showing it to two observers—one in a black t-shirt and another in a blue jersey—while the text “HE TIED HIS HANDS” appears on screen; he then secures the device on his own wrist as the camera pans to reveal the surrounding landscape of trees, hills, and clear sky.

Later, the same man, now holding a basketball, walks toward the free-throw line, pausing to prepare for a shot, while another player in a blue jersey stands nearby posing with hands on hips; the camera pans across the court’s markings and surrounding scenery before returning to the shooter as he raises the ball above his head to aim.

In the background, a third person in a black shirt stands near the basket, and the blue-jerseyed observer enters the frame from the right, watching; the court features a painted logo and blue key area, with trees and a fence visible beyond the perimeter under a clear blue sky.
```

**txt9**

```
[video-level knowledge | semantic] (player, uses, Straight Shooter Strap)
```

**txt10**

```
[video-level knowledge | semantic] (Straight Shooter Strap, is shown in, close-up)
```

**txt11**

```
[video-level knowledge | semantic] (demonstrator, adjusts, black elbow strap)
```

**txt12** (cited)

```
[video-level knowledge | semantic] (Flick Gloves, has colors, white)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 | ✓ | 00:20:15 | 00:20:10–00:20:20 | `-QuCz7kxBr8:visual:00201000` | `outputs/p9p19_check_20261025_141401/frames_s2/-QuCz7kxBr8/00201000.jpg` |
| img2 | ✓ | 00:32:35 | 00:32:30–00:32:40 | `-QuCz7kxBr8:visual:00323000` | `outputs/p9p19_check_20261025_141401/frames_s2/-QuCz7kxBr8/00323000.jpg` |
| img3 | ✓ | 00:20:05 | 00:20:00–00:20:10 | `-QuCz7kxBr8:visual:00200000` | `outputs/p9p19_check_20261025_141401/frames_s2/-QuCz7kxBr8/00200000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1** (cited)

```
[00:20:10-00:20:20 | video frame at 1215.0s] On a sunny day at an outdoor basketball court, a man in a black hoodie and white cap stands near the center, holding a basketball. He turns and walks toward the free-throw line as another player in a blue jersey stands nearby, posing with hands on hips. The camera pans to show the court’s markings and surrounding landscape, including trees and hills, before focusing back on the man with the ball as he prepares to shoot.
```

**img2** (cited)

```
[00:32:30-00:32:40 | video frame at 1955.0s] A young man stands on an outdoor basketball court holding two large black training pads with red paw prints, as a large "1-0" graphic is superimposed over the scene. He turns to face another man in a black hoodie and white cap who is holding a basketball. The two men face each other on the court, which has "HYPE" painted on the blue key area, with a basketball hoop in the background and mountains visible in the distance under a clear blue sky. Another person is visible sitting on the sideline.
```

**img3** (cited)

```
[00:20:00-00:20:10 | video frame at 1205.0s] On an outdoor basketball court, a man in a black hoodie and white cap demonstrates a device that appears to be used for hand restraint or training, showing it to two other men—one in a black t-shirt and another in a blue basketball jersey. The man in the hoodie holds the device, which has orange straps, and the text “HE TIED HIS HANDS” appears on screen as he adjusts it. The two other men watch, one with his arms crossed, while the camera pans to show the man in the hoodie holding the device on his wrist. In the background, other people are visible on the court, and the setting includes trees, hills, and a clear sky.
```
