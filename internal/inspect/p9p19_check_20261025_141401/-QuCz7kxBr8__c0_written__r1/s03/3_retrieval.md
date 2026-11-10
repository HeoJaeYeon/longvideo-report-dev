# Section 3 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:17:27): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 17, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 5.91}`
- image request (2026-10-25 14:17:31): `{'video_id': '-QuCz7kxBr8', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 1.09}`
- L1 filter LLM call: prompt 9058 tokens, output 70 tokens, 4.7 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 30sec | 00:08:00–00:08:30 | 1 / 0.04866 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_16` |
| txt2 | ✓ | worldmm-episodic | 3min | 00:06:00–00:09:00 | 2 / 0.032787 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_2` |
| txt3 | ✓ | worldmm-episodic | 10min | 00:00:00–00:10:00 | 3 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10min_0` |
| txt4 | ✓ | worldmm-episodic | 30sec | 00:19:30–00:20:00 | 4 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_39` |
| txt5 | ✓ | worldmm-episodic | 3min | 00:18:00–00:21:00 | 5 / 0.016393 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:3min_6` |
| txt6 | ✓ | worldmm-episodic | 10sec | 00:08:20–00:08:30 | 6 / 0.032258 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_50` |
| txt7 | ✓ | worldmm-episodic | 30sec | 00:10:00–00:10:30 | 7 / 0.016129 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:30sec_20` |
| txt8 |  | worldmm-episodic | 10sec | 00:18:20–00:18:30 | 8 / 0.015873 (rrf(order=llm_filter)) | `-QuCz7kxBr8:episodic:10sec_110` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.032018 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_34` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.031746 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_37` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.03101 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_32` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016393 (rrf) | `-QuCz7kxBr8:semantic:semantic_100373700_63` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:08:00-00:08:30 | episodic 30sec] Three men on an outdoor basketball court prepare for a shooting challenge involving the Flick Glove — a device designed to improve basketball shooting technique. One man in a black hoodie and white cap, holding a basketball and the glove, explains the rules while gesturing, as the other two — one in a red hoodie and another in a blue jersey — observe. A text overlay instructs participants to take three shots with the glove, then three without, with the person making the fewest baskets required to do 100 sit-ups. The man in the red hoodie expresses confusion about the glove’s orientation, prompting the man in the black hoodie to demonstrate its use. The video opens with a close-up of the glove’s design — featuring finger loops and a rectangular screen — and later displays the three available color options (white, black, orange) with the brand name “FLICK GLOVE” overlaid, establishing the product’s purpose and setup for the upcoming demonstration.
```

**txt2** (cited)

```
[00:06:00-00:09:00 | episodic 3min] A man in a white hoodie and patterned shorts shoots basketballs on a sunny court, with a score counter updating after each shot — from 0/0 to 3/5 — while a humorous voiceover references product ownership and investment. He praises the product as “great,” with a “#NOT SPONSORED” graphic. The scene cuts to another player resetting the score.

A second player makes a shot (1/2), but audio commentary criticizes the product’s performance, noting it “fell off” and “snaps” when extended. A shooting contest unfolds: a player in a red and white jersey (No. 2) makes a successful shot (2/5), celebrated with surprise and joy. Later, the tie-dye jersey player loses, prompting the white-shirted man to propose testing his jump shot without the strap to isolate the issue — a playful, lighthearted challenge.

His jump shot misses, sparking frustration and speculation about the strap. A teammate confirms the issue, and a forfeit of 30 jumping jacks is suggested. The man begins doing jumping jacks, arms raised, while two others watch and tease — one jokes about “bouncing titties,” another compares chest sizes. He deflects with humor, “Bro, I’m wearing a big shirt.” His movements become off-rhythm, drawing amused observation.

Three men discuss and humorously rate the product: the white-hoodie man (ZHYPE) calls it suitable for kids but suggests a better gadget for beginners, scoring it “1.” They escalate to exaggerated scoring — “1,” “2,” then “-3k” — ending with a playful “what’s the next invention?” 

A shooting challenge with the Flick Glove begins: one man in a black hoodie explains rules — three shots with the glove, then without — with the fewest baskets requiring 100 sit-ups. The red-hoodie man misunderstands the glove’s orientation, prompting a demonstration. The glove’s design (finger loops, screen) and color options (white, black, orange) are shown.

Three men demonstrate basketball drills under sunny skies, with the blue-jersey man explaining movement techniques. A shot by the black-hoodie man is debated — “too far,” “cheating.” Later, he makes another shot, celebrated with “Woo!” and “WHOOOOOO” graphics, emphasizing triumph and energy.
```

**txt3** (cited)

```
[00:00:00-00:10:00 | episodic 10min] **Six men—Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player—gather on a sunny outdoor basketball court to test 12 viral sports gadgets, splitting into two teams of three. Dressed in athletic wear, they introduce the challenge while holding basketballs near a hoop and trees. One man in a white hoodie addresses the camera, setting the tone with playful banter and audio cues like “Hands up, hands up” and “Mump is blinding me.” The scene transitions to a countdown and gear review, beginning with a close-up of black nylon straps, signaling the start of hands-on testing.**

The group begins evaluating gadgets, starting with “SPORTS DRIBBLE SPECS.” One player dons the goggles and prepares for a dribbling time trial, where participants must dribble through three cones and touch a pole to stop the clock. Rules are clarified near a pool under bright sunlight, with the man in the hoodie confirming the forfeit rule for the slowest time. The drill proceeds with players like Chris and Zach showcasing speed and control, with timers capturing times like 10:85 and 9:51 seconds. Commentary highlights frustrations (“handles were definitely off”) and praise (“He’s making great time”), emphasizing the competitive yet casual atmosphere.

Later, the group discusses the gadget’s usefulness, with the man in the white hoodie expressing discomfort with traditional basketballs forcing him to look down. A score graphic flashes from 5 to 6, then 4, as teammates react with thumbs-up approval. The segment ends with the introduction of the SKLZ Dribble Stick—a black training tool with adjustable yellow arms—where the blue-jerseyed player prepares to demonstrate its use. Rules are reviewed: players dribble while avoiding the stick; the first to touch it runs five laps. The group is ready to begin, setting up for the next round of testing.

**Three men gather on an outdoor basketball court, negotiating positions before settling into a shooting challenge. One man in a black hoodie and white cap adjusts a basketball on a training device while the others—wearing red and blue jerseys—observe, holding balls. A fourth person films the scene under clear skies, with trees and a fence in the background. The group transitions to a hoop with a vertical obstacle, where they take turns shooting under a 30-second countdown. Encouragement and light-hearted banter—such as “you might be safe just making it past that first one”—add to the casual yet competitive tone. The man in the black hoodie successfully makes his shot, smiling as he walks back, while the man in red watches amusedly. Their conversation hints at past forfeits and humorous self-deprecation.**

The group then evaluates the dribble stick, with the man in the blue jersey rating it an 8/10, followed by the man in the black shirt agreeing, and the man in the black hoodie giving it a 7—joking that anything helping him fail is “pretty good.” The conversation remains lighthearted and collaborative.

**Later, a man in a white hoodie demonstrates the “Straight Shooter Strap,” explaining how it stabilizes the elbow during shooting. He adjusts the strap on his arm while a third observer watches. The scene widens to show the full court, hoop, and surrounding hills under clear skies, setting up practical use of the device.**

A shooter in a white shirt and patterned shorts begins a shooting sequence, initially making one shot (0/1), then missing several, with the scoreboard climbing to 0/3. He pauses, inspecting his elbow, seemingly frustrated. As the sequence continues, he scores more shots, pushing the tally to 3/16, with teammates retrieving balls and commentary tracking each attempt. The scoreboard climbs steadily, accompanied by remarks like “Dude, 15,” and “Zach’s uses this thing, bro.” The player smiles at the camera as he approaches 15 successful shots, with the backdrop of a large house and trees under clear skies.

**A man in a white hoodie and patterned shorts shoots basketballs on a sunny court, with a score counter updating after each shot — from 0/0 to 3/5 — while a humorous voiceover references product ownership and investment. He praises the product as “great,” with a “#NOT SPONSORED” graphic. The scene cuts to another player resetting the score.**

A second player makes a shot (1/2), but audio commentary criticizes the product’s performance, noting it “fell off” and “snaps” when extended. A shooting contest unfolds: a player in a red and white jersey (No. 2) makes a successful shot (2/5), celebrated with surprise and joy. Later, the tie-dye jersey player loses, prompting the white-shirted man to propose testing his jump shot without the strap to isolate the issue — a playful, lighthearted challenge.

His jump shot misses, sparking frustration and speculation about the strap. A teammate confirms the issue, and a forfeit of 30 jumping jacks is suggested. The man begins doing jumping jacks, arms raised, while two others watch and tease — one jokes about “bouncing titties,” another compares chest sizes. He deflects with humor, “Bro, I’m wearing a big shirt.” His movements become off-rhythm, drawing amused observation.

**Three men discuss and humorously rate the product: the white-hoodie man (ZHYPE) calls it suitable for kids but suggests a better gadget for beginners, scoring it “1.” They escalate to exaggerated scoring — “1,” “2,” then “-3k” — ending with a playful “what’s the next invention?”**

**A shooting challenge with the Flick Glove begins: one man in a black hoodie explains rules — three shots with the glove, then without — with the fewest baskets requiring 100 sit-ups. The red-hoodie man misunderstands the glove’s orientation, prompting a demonstration. The glove’s design (finger loops, screen) and color options (white, black, orange) are shown.**

Three men demonstrate basketball drills under sunny skies, with the blue-jersey man explaining movement techniques. A shot by the black-hoodie man is debated — “too far,” “cheating.” Later, he makes another shot, celebrated with “Woo!” and “WHOOOOOO” graphics, emphasizing triumph and energy.

**A man in a black hoodie and white cap demonstrates a basketball drill on an outdoor court, successfully shooting and gesturing to explain technique, enhanced by animated graphics. He acknowledges tech-assisted visuals, praising a teammate in a blue jersey, then encourages another player in a red hoodie with “You look like you're hot right now, bro,” reinforcing camaraderie during a casual game.**

The player in the red hoodie makes a shot, humorously noting the ball nearly slipped off his pinky finger. He pauses, gestures while holding a wristband, removes it, and reflects on his performance. He critiques his flick motion, acknowledging lack of straightness, before preparing for another attempt, observed by two onlookers in black and blue attire.

Meanwhile, the player in the blue jersey makes three consecutive shots, confirmed by on-screen text “3 MADE BASKETS,” then later scores again, reaching “4 MADE BASKETS.” He celebrates while speaking casually, with graphics of basketballs and audio commentary referencing conditioning and sit-ups. The branded “HYPER” court and clear skies frame the scene.

**Separately, the man in the black hoodie performs sit-ups on a concrete court, with on-screen text “CASH LOST,” explained by voiceover as punishment for fewest flick shots. A blonde-bearded man in red watches and speaks animatedly. Later, the same man continues sit-ups beside a pool, where a graphic displays “SCORE 7” as he gestures and celebrates with two teammates — one in pink shorts, the other in a “SHY 2” jersey — in a lively, sunlit setting.**

The group, including a man in a “ZHYPE” jersey and hoodie, gathers for discussion, holding a basketball with a “POWERHANDZ Dribble Sleeve” overlay, preparing for a demonstration or game. The scene remains focused on strategy and play, with the score updating to “SCORE 7,” reinforcing the competitive yet casual tone.
```

**txt4** (cited)

```
[00:19:30-00:20:00 | episodic 30sec] A basketball coach in a black hoodie and white cap stands on an outdoor court, using an orange “SHOT COACH” training device to instruct two young players, with a text overlay directing them to “SHOOT FROM HALF COURT 5 TIMES WITH SHOT COACH.” He adjusts a wristband or device on one player’s wrist while the other observes, all under bright sunlight with a hoop and greenery in the background. The coach holds a clipboard and gestures as he explains the drill, emphasizing precision and repetition through the Shot Coach system. The scene briefly cuts to a scoreboard graphic showing "-2" then resetting to "0," followed by a third man in a blue jersey crossing his arms and smiling as the scoreboard shows "-1," suggesting a playful or competitive scoring context. The coach and the player in the blue jersey later move to a table, where the coach appears to write or draw, possibly documenting progress or adjusting the training plan. The video closes with a close-up of the Shot Coach device, reinforcing its role as a key tool in the structured, tech-assisted shooting drill.
```

**txt5** (cited)

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

**txt6** (cited)

```
[00:08:20-00:08:30 | episodic 10sec] Three men stand on an outdoor basketball court. A text overlay explains a challenge: take three shots with a flick glove, then three without, and the person making the least baskets must do 100 sit-ups. One man in a red hoodie reacts with surprise, while another in a blue jersey smiles. The third man, wearing a black hoodie and cap, holds a basketball and a black glove, examining it. The man in the red hoodie asks, “Bro, what are these? Which way does it even go?” as the man in the black hoodie holds up the glove.
```

**txt7** (cited)

```
[00:10:00-00:10:30 | episodic 30sec] Three people are on an outdoor basketball court under a clear blue sky. A player in a red hoodie attempts a shot but misses; the ball arcs toward the hoop and falls short. The player in the blue jersey then takes a shot and successfully makes it, holding the ball afterward while smiling. Text overlays appear stating “3 MADE BASKETS,” indicating a scoring milestone or game objective. The scene transitions to another moment where the same player in the blue sleeveless shirt misses a shot, retrieves the ball, and prepares to shoot again. A second player in a red shirt stands near the basket, while a third in a black shirt and white cap watches from the side. Audio commentary references missing the first shot and adjusting to a “flick” motion, followed by a mention of needing to make two shots. Later, the player in the blue jersey—now wearing a blue basketball jersey—shoots again, this time successfully, with the ball arcing cleanly into the hoop. He turns to face the camera, holding the ball and speaking casually. Overlaid graphics of basketballs appear, and the audio includes informal conversation about making shots and the need to do sit-ups for conditioning. The court features a blue-painted area with the word “HYPER” visible, reinforcing the setting as a branded or themed outdoor court.
```

**txt8**

```
[00:18:20-00:18:30 | episodic 10sec] The video begins with a product shot of three black basketball shooting aids, overlaid with the text "Pack of 3 Basketball Shooting Aid." The scene then transitions to an outdoor setting under a clear blue sky, where three men stand around a white table. One man, wearing a black t-shirt and holding a small object, appears to be explaining something to the other two. The man in the center wears a blue basketball jersey and smiles, while the man on the right, in a black hoodie and white cap, holds a basketball and listens attentively. At 00:18:29, a text overlay appears reading "FIRST MADE SHOT SHOOTS GILLY STRING AT 100%."
```

**txt9**

```
[video-level knowledge | semantic] (Flick Gloves, has colors, orange)
```

**txt10**

```
[video-level knowledge | semantic] (Flick Gloves, has text overlay, when man shoots)
```

**txt11**

```
[video-level knowledge | semantic] (Flick Gloves, has colors, white)
```

**txt12**

```
[video-level knowledge | semantic] (NEVER ENDING DEFENDER, has text, NEVER ENDING DEFENDER)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:14:55 | 00:14:50–00:15:00 | `-QuCz7kxBr8:visual:00145000` | `outputs/p9p19_check_20261025_141401/frames_s0/-QuCz7kxBr8/00145000.jpg` |
| img2 |  | 00:14:35 | 00:14:30–00:14:40 | `-QuCz7kxBr8:visual:00143000` | `outputs/p9p19_check_20261025_141401/frames_s0/-QuCz7kxBr8/00143000.jpg` |
| img3 |  | 00:14:45 | 00:14:40–00:14:50 | `-QuCz7kxBr8:visual:00144000` | `outputs/p9p19_check_20261025_141401/frames_s0/-QuCz7kxBr8/00144000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:14:50-00:15:00 | video frame at 895.0s] Three men stand outdoors near a table with basketball gear. One man in a blue jersey puts on a pair of gloves while the other two watch. The text overlay reads "20 LOW, MEDIUM, & HIGH DRIBBLES IN 60 SECONDS." The man in the blue jersey then says, "IT'S LIKE THE THICC WOMEN OF GLOVES."
```

**img2**

```
[00:14:30-00:14:40 | video frame at 875.0s] Three men are standing on an outdoor basketball court. The man on the left, wearing a tie-dye jersey, gestures while speaking. The man in the center, in a white hoodie with "2HYPE" on it, stands with his hands on his hips. The man on the right, in a white t-shirt, holds a basketball. A graphic overlay displays "SCORE 9". The scene then cuts to a different man in a blue jersey standing at a table, holding a smartphone. The video transitions to a close-up of a pair of gloves with a leopard print and tiger stripe pattern, with the text "POWER HANDZ" overlaid.
```

**img3**

```
[00:14:40-00:14:50 | video frame at 885.0s] A close-up shot displays a pair of black and orange "POWER HANDZ" gloves with a leopard print pattern, followed by a scene outdoors where three men stand around a table. One man in a blue sleeveless shirt is gesturing while speaking, while the other two watch. A text overlay appears, reading "20 LOW, MEDIUM, & HIGH DRIBBLES IN 60 SECONDS."
```
