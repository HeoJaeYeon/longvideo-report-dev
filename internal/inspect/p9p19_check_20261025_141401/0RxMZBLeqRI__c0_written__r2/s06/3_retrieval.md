# Section 6 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:26:40): `{'video_id': '0RxMZBLeqRI', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 24, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 7.68}`
- image request (2026-10-25 14:26:42): `{'video_id': '0RxMZBLeqRI', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 0.03}`
- L1 filter LLM call: prompt 14601 tokens, output 73 tokens, 6.4 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 3min | 00:30:00–00:33:00 | 1 / 0.032787 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:3min_10` |
| txt2 | ✓ | worldmm-episodic | 10min | 00:30:00–00:40:00 | 2 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10min_3` |
| txt3 | ✓ | worldmm-episodic | 30sec | 00:30:00–00:30:30 | 3 / 0.015873 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_60` |
| txt4 | ✓ | worldmm-episodic | 30sec | 00:30:30–00:31:00 | 4 / 0.032787 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_61` |
| txt5 |  | worldmm-episodic | 10sec | 00:30:00–00:30:10 | 5 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_180` |
| txt6 | ✓ | worldmm-episodic | 30sec | 00:24:30–00:25:00 | 6 / 0.016129 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_49` |
| txt7 |  | worldmm-episodic | 10sec | 00:04:50–00:05:00 | 7 / 0.016129 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_29` |
| txt8 | ✓ | worldmm-episodic | 30sec | 00:29:30–00:30:00 | 8 / 0.015873 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_59` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_330` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_357` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_174` |
| txt12 | ✓ | worldmm-semantic | — | no timestamp | 4 / 0.016129 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_355` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:30:00-00:33:00 | episodic 3min] An anime-style girl in a black hat with a red band, white shirt, red bow tie, and patterned skirt stands before the Arc de Triomphe in Paris, posing thoughtfully with one hand to her chin before spreading her arms wide in a cheerful gesture as cars pass behind her. At 00:30:08, colorful credits appear on the right side of the screen. The scene then transitions to the same character gesturing in front of a backdrop listing names, followed by a rotating globe centered on a grid of international flags. The globe slowly turns, showcasing continents—Asia, Africa, the Americas, and returning to Europe and Asia—against a backdrop of national flags, with no audio. The screen then opens with a stylized globe centered on Asia and Australia, encircled by national flags, symbolizing global unity or international scope. The scene abruptly cuts to black, signaling a narrative pause or intentional transition.
```

**txt2** (cited)

```
[00:30:00-00:40:00 | episodic 10min] **[Event 1: Parisian Pose and Transition to Credits]**  
An anime-style girl, dressed in a black hat with a red band, white shirt, red bow tie, and patterned skirt, stands before the Arc de Triomphe in Paris. She poses thoughtfully with one hand to her chin, then spreads her arms wide in a cheerful gesture as cars pass behind her, establishing a lighthearted, cinematic tone. At 00:30:08, colorful credits animate onto the right side of the screen, marking the conclusion of the scene. The transition is smooth and visually deliberate, suggesting a narrative pause or thematic coda.

**[Event 2: Global Backdrop and Rotating Globe]**  
The scene shifts to the same character gesturing in front of a backdrop listing names, likely signifying contributors or collaborators. This is immediately followed by a rotating globe centered on a grid of international flags. The globe slowly turns, sequentially showcasing continents—Asia, Africa, the Americas, and returning to Europe and Asia—against a backdrop of national flags. The absence of audio emphasizes the visual symbolism of global interconnectedness, reinforcing themes of international scope or unity.

**[Event 3: Stylized Globe and Narrative Pause]**  
The screen opens on a stylized globe centered on Asia and Australia, encircled by national flags, visually reinforcing the global theme. The composition is balanced and symbolic, suggesting a unifying vision or international perspective. The scene abruptly cuts to black, serving as a deliberate narrative pause or transition, possibly signaling a shift in tone, perspective, or storyline. The black screen acts as a visual reset, leaving the viewer in anticipation of what follows.

Each event is visually distinct yet thematically connected, progressing from a localized Parisian moment to a global perspective, culminating in a pause that invites reflection or transition.
```

**txt3** (cited)

```
[00:30:00-00:30:30 | episodic 30sec] An anime-style girl in a black hat with a red band, white shirt, red bow tie, and patterned skirt stands before the Arc de Triomphe in Paris, initially posing with one hand to her chin and a slight smile before spreading her arms wide in a cheerful gesture as cars pass behind her; at 00:30:08, credits appear on the right side of the screen in varied colors.

The scene then transitions to the same character gesturing in front of a backdrop listing names, followed by a shift to a rotating globe centered on a grid of international flags, which slowly turns to showcase continents—Asia, Africa, the Americas, and back to Europe and Asia—against a backdrop of national flags, with no audio present.
```

**txt4** (cited)

```
[00:30:30-00:31:00 | episodic 30sec] The screen opens with a global-themed visual: a stylized globe centered on Asia and Australia, encircled by a grid of national flags, symbolizing international scope or global unity. The scene then cuts abruptly to black, signaling a transition, pause, or intentional break in the visual narrative.
```

**txt5**

```
[00:30:00-00:30:10 | episodic 10sec] An anime-style girl in a black hat with a red band, a white shirt, a red bow tie, and a patterned skirt stands in front of the Arc de Triomphe in Paris. She begins with one hand raised to her chin and a slight smile, then transitions to spreading her arms wide with a cheerful expression. Cars pass by on the road behind her. At 00:30:08, credits appear on the right side of the screen, listing names in various colors.
```

**txt6** (cited)

```
[00:24:30-00:25:00 | episodic 30sec] **[Event 1: Historical Footage of Post-War Repression]**  
The video opens with a title card reading “Communism Chapter VII,” followed by black-and-white archival footage from 1945. Soldiers are shown atop a damaged building, suggesting post-war conflict or occupation. The scene transitions to a civilian man being escorted by a uniformed officer, followed by large groups of people—many in striped uniforms—marching in lines toward a concentration camp, with barbed wire fences and watchtowers visible. This sequence visually conveys systemic repression and forced labor under authoritarian regimes.

**[Event 2: Formal Proceedings and Judicial Setting]**  
The video cuts to a formal indoor conference, where men in suits sit at a long table with microphones, implying a political or judicial hearing. The scene then shifts to a courtroom where a man in a light-colored uniform addresses seated individuals, some wearing headphones, while soldiers in helmets stand guard. This suggests a legal or administrative process under state control, possibly involving trials or interrogations under authoritarian governance.

**[Event 3: Animated Transition and Symbolic Imagery]**  
The video abruptly transitions to an animated sequence featuring a stylized female character in a hat and bow tie, superimposed over a sepia-toned historical street scene with horse-drawn carriages. The scene then zooms out to reveal a large ornate clock on a stone building, followed by the word “COMMUNISM” in bold white letters over a black-and-white aerial view of a town. The final frame shifts to an animated bald man in a suit clasping his hands as he looks up at a person with curly red hair—possibly symbolizing ideological confrontation or historical reflection.

**[Event 4: Thematic Closure]**  
The video concludes with a stark juxtaposition of historical imagery and stylized animation, suggesting a thematic exploration of communism’s legacy. The use of symbolic visuals, such as the clock, the word “COMMUNISM,” and the animated characters, implies a commentary on historical memory, ideological conflict, or the enduring impact of communist systems. The abrupt tonal shift from grim historical footage to stylized animation may signal a transition from documentation to interpretation or critique.
```

**txt7**

```
[00:04:50-00:05:00 | episodic 10sec] The video begins with a wide shot of a desert landscape featuring sand dunes, scattered vegetation, and distant rock formations under a clear sky. It then cuts to a close-up of a man with a shaved head and beard, wearing a blue shirt, smiling and speaking while seated inside a car. The scene transitions to an animated image of a cheerful anime-style girl in a traditional outfit, superimposed over a historical painting depicting two figures in a struggle, with sheep visible in the background. The video concludes with a wide shot of the interior of a grand, empty cathedral, showcasing its tall stone pillars, arched ceilings, and rows of wooden pews.
```

**txt8** (cited)

```
[00:29:30-00:30:00 | episodic 30sec] An animated woman in traditional attire stands with open arms against a cityscape, symbolizing cultural presence or welcome, followed by a sepia-toned religious figure and snowy boots, evoking historical or spiritual themes. The scene closes with a family gathered indoors, television on, suggesting domestic normalcy or quiet resilience.

A far-right rally in a Hungarian town is shown, with men in dark clothing standing in formation — some arms crossed — underscoring tension and intimidation. The rally has stirred fear within the Roma community, as indicated by on-screen text. The video then shifts to an aerial view of a residential area, revealing cluttered balconies and debris piled at building bases, hinting at displacement, neglect, or aftermath of conflict.

The segment opens with an aerial shot of a densely packed, cluttered apartment building, transitioning to narrow alleyways where people walk — suggesting urban hardship or confinement. It then cuts to a public rally where a woman speaks into a microphone while holding a sign, joined by four individuals holding signs that read “Én is cigány vagyok” (“I am also a Roma”), asserting identity and solidarity. A man in a suit signs a document, implying institutional recognition or legal action. The final frame overlays an animated character onto a real-world archway with traffic, blending symbolic representation with urban reality — possibly signifying cultural endurance or resistance within a modern setting.
```

**txt9**

```
[video-level knowledge | semantic] (anime-style character, is in front of, urban backdrop)
```

**txt10**

```
[video-level knowledge | semantic] (poster, has news headline, ROMANIAN GOVERNMENT ACKNOWLEDGES RESPONSIBILITY FOR ANTI-ROMANI POGROMS)
```

**txt11**

```
[video-level knowledge | semantic] (historical map, depicts, migration routes)
```

**txt12** (cited)

```
[video-level knowledge | semantic] (video, displays, poster featuring anime-style character)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:30:15 | 00:30:10–00:30:20 | `0RxMZBLeqRI:visual:00301000` | `outputs/p9p19_check_20261025_141401/frames_s3/0RxMZBLeqRI/00301000.jpg` |
| img2 |  | 00:30:05 | 00:30:00–00:30:10 | `0RxMZBLeqRI:visual:00300000` | `outputs/p9p19_check_20261025_141401/frames_s3/0RxMZBLeqRI/00300000.jpg` |
| img3 |  | 00:11:05 | 00:11:00–00:11:10 | `0RxMZBLeqRI:visual:00110000` | `outputs/p9p19_check_20261025_141401/frames_s3/0RxMZBLeqRI/00110000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:30:10-00:30:20 | video frame at 1815.0s] An anime-style character in a hat and bow tie gestures in front of a backdrop featuring a list of names, then the scene transitions to a rotating globe centered on a grid of international flags.
```

**img2**

```
[00:30:00-00:30:10 | video frame at 1805.0s] An anime-style girl in a black hat with a red band, a white shirt, a red bow tie, and a patterned skirt stands in front of the Arc de Triomphe in Paris. She begins with one hand raised to her chin and a slight smile, then transitions to spreading her arms wide with a cheerful expression. Cars pass by on the road behind her. At 00:30:08, credits appear on the right side of the screen, listing names in various colors.
```

**img3**

```
[00:11:00-00:11:10 | video frame at 665.0s] The video segment begins with a historical illustration depicting a military procession, followed by a colorful manuscript-style scene showing a seated ruler interacting with a group of people in ornate attire. The audio discusses how Ottoman institutions incorporated Islamic doctrine, which granted Muslims the right to treat conquered non-Muslim subjects as property, noting that this affected groups beyond the Roma. The segment concludes with an animated character gesturing in front of a scenic view of the Hagia Sophia and surrounding architecture in Istanbul.
```
