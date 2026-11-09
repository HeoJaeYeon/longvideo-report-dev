# Section 5 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:26:18): `{'video_id': '0RxMZBLeqRI', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 19, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 5.78}`
- image request (2026-10-25 14:26:21): `{'video_id': '0RxMZBLeqRI', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 0.57}`
- L1 filter LLM call: prompt 7262 tokens, output 75 tokens, 4.6 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 |  | worldmm-episodic | 3min | 00:30:00–00:33:00 | 1 / 0.04918 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:3min_10` |
| txt2 | ✓ | worldmm-episodic | 10min | 00:30:00–00:40:00 | 2 / 0.04918 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10min_3` |
| txt3 |  | worldmm-episodic | 30sec | 00:30:00–00:30:30 | 3 / 0.032787 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_60` |
| txt4 | ✓ | worldmm-episodic | 30sec | 00:30:30–00:31:00 | 4 / 0.032522 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_61` |
| txt5 | ✓ | worldmm-episodic | 10sec | 00:30:00–00:30:10 | 5 / 0.032266 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_180` |
| txt6 | ✓ | worldmm-episodic | 10sec | 00:30:20–00:30:30 | 6 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_182` |
| txt7 |  | worldmm-episodic | 10sec | 00:30:30–00:30:32 | 7 / 0.032258 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_183` |
| txt8 |  | worldmm-episodic | 30sec | 00:25:00–00:25:30 | 8 / 0.016129 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_50` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_393` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_397` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_70` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016129 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_335` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1**

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

**txt3**

```
[00:30:00-00:30:30 | episodic 30sec] An anime-style girl in a black hat with a red band, white shirt, red bow tie, and patterned skirt stands before the Arc de Triomphe in Paris, initially posing with one hand to her chin and a slight smile before spreading her arms wide in a cheerful gesture as cars pass behind her; at 00:30:08, credits appear on the right side of the screen in varied colors.

The scene then transitions to the same character gesturing in front of a backdrop listing names, followed by a shift to a rotating globe centered on a grid of international flags, which slowly turns to showcase continents—Asia, Africa, the Americas, and back to Europe and Asia—against a backdrop of national flags, with no audio present.
```

**txt4** (cited)

```
[00:30:30-00:31:00 | episodic 30sec] The screen opens with a global-themed visual: a stylized globe centered on Asia and Australia, encircled by a grid of national flags, symbolizing international scope or global unity. The scene then cuts abruptly to black, signaling a transition, pause, or intentional break in the visual narrative.
```

**txt5** (cited)

```
[00:30:00-00:30:10 | episodic 10sec] An anime-style girl in a black hat with a red band, a white shirt, a red bow tie, and a patterned skirt stands in front of the Arc de Triomphe in Paris. She begins with one hand raised to her chin and a slight smile, then transitions to spreading her arms wide with a cheerful expression. Cars pass by on the road behind her. At 00:30:08, credits appear on the right side of the screen, listing names in various colors.
```

**txt6** (cited)

```
[00:30:20-00:30:30 | episodic 10sec] A stylized globe rotates slowly against a background displaying numerous national flags. The globe begins facing Asia and gradually rotates to show Africa, then the Americas, before returning to focus on Europe and Asia again. No audio is present.
```

**txt7**

```
[00:30:30-00:30:32 | episodic 10sec] The screen displays a grid of various national flags surrounding a central, stylized globe showing the continents of Asia and Australia. The scene then abruptly transitions to complete blackness.
```

**txt8**

```
[00:25:00-00:25:30 | episodic 30sec] A muscular superhero in a red costume confronts a bald man in a suit, gesturing angrily before the scene cuts to black-and-white historical footage: first, a bustling marketplace, then a person on horseback near a wooden structure in a forest, with the History Channel logo visible.

The video shifts to a black-and-white scene of a horse-drawn wagon in a wooded area with people interacting, then transitions to a dimly lit workshop where a person hammers metal on an anvil, before moving to an outdoor mining site with heavy machinery and railcars transporting material.

The segment concludes with a black-and-white scene of crop harvesting, transitioning to a map of Bulgaria, followed by a man walking beside a horse-drawn cart on a road. Overlaid text explains that during Bulgaria’s “Process of Revival” (1984–1985), the government denied the existence of Gypsies, concealing their presence from public life and media.
```

**txt9**

```
[video-level knowledge | semantic] (Arc de Triomphe, is located in, Paris)
```

**txt10**

```
[video-level knowledge | semantic] (globe, returns to focus on, Asia)
```

**txt11**

```
[video-level knowledge | semantic] (clip from TV show, ends with, close-up shot)
```

**txt12**

```
[video-level knowledge | semantic] (animated character, stands in front of, modern weathered apartment buildings)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 | ✓ | 00:30:05 | 00:30:00–00:30:10 | `0RxMZBLeqRI:visual:00300000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00300000.jpg` |
| img2 | ✓ | 00:30:15 | 00:30:10–00:30:20 | `0RxMZBLeqRI:visual:00301000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00301000.jpg` |
| img3 | ✓ | 00:11:05 | 00:11:00–00:11:10 | `0RxMZBLeqRI:visual:00110000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00110000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1** (cited)

```
[00:30:00-00:30:10 | video frame at 1805.0s] An anime-style girl in a black hat with a red band, a white shirt, a red bow tie, and a patterned skirt stands in front of the Arc de Triomphe in Paris. She begins with one hand raised to her chin and a slight smile, then transitions to spreading her arms wide with a cheerful expression. Cars pass by on the road behind her. At 00:30:08, credits appear on the right side of the screen, listing names in various colors.
```

**img2** (cited)

```
[00:30:10-00:30:20 | video frame at 1815.0s] An anime-style character in a hat and bow tie gestures in front of a backdrop featuring a list of names, then the scene transitions to a rotating globe centered on a grid of international flags.
```

**img3** (cited)

```
[00:11:00-00:11:10 | video frame at 665.0s] The video segment begins with a historical illustration depicting a military procession, followed by a colorful manuscript-style scene showing a seated ruler interacting with a group of people in ornate attire. The audio discusses how Ottoman institutions incorporated Islamic doctrine, which granted Muslims the right to treat conquered non-Muslim subjects as property, noting that this affected groups beyond the Roma. The segment concludes with an animated character gesturing in front of a scenic view of the Hagia Sophia and surrounding architecture in Istanbul.
```
