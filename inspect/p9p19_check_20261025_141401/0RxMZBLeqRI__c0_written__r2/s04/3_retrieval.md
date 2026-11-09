# Section 4 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:23:16): `{'video_id': '0RxMZBLeqRI', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 24, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 7.71}`
- image request (2026-10-25 14:23:19): `{'video_id': '0RxMZBLeqRI', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 0.88}`
- L1 filter LLM call: prompt 15106 tokens, output 79 tokens, 6.6 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 30sec | 00:29:30–00:30:00 | 1 / 0.032002 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_59` |
| txt2 | ✓ | worldmm-episodic | 10sec | 00:29:50–00:30:00 | 2 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_179` |
| txt3 | ✓ | worldmm-episodic | 30sec | 00:28:30–00:29:00 | 3 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_57` |
| txt4 | ✓ | worldmm-episodic | 10sec | 00:28:50–00:29:00 | 4 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_173` |
| txt5 |  | worldmm-episodic | 10sec | 00:29:20–00:29:30 | 5 / 0.015873 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_176` |
| txt6 | ✓ | worldmm-episodic | 30sec | 00:26:00–00:26:30 | 6 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_52` |
| txt7 | ✓ | worldmm-episodic | 10sec | 00:25:50–00:26:00 | 7 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_155` |
| txt8 | ✓ | worldmm-episodic | 10sec | 00:26:00–00:26:10 | 8 / 0.016129 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_156` |
| txt9 | ✓ | worldmm-semantic | — | no timestamp | 1 / 0.03101 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_330` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_389` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_368` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_82` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:29:30-00:30:00 | episodic 30sec] An animated woman in traditional attire stands with open arms against a cityscape, symbolizing cultural presence or welcome, followed by a sepia-toned religious figure and snowy boots, evoking historical or spiritual themes. The scene closes with a family gathered indoors, television on, suggesting domestic normalcy or quiet resilience.

A far-right rally in a Hungarian town is shown, with men in dark clothing standing in formation — some arms crossed — underscoring tension and intimidation. The rally has stirred fear within the Roma community, as indicated by on-screen text. The video then shifts to an aerial view of a residential area, revealing cluttered balconies and debris piled at building bases, hinting at displacement, neglect, or aftermath of conflict.

The segment opens with an aerial shot of a densely packed, cluttered apartment building, transitioning to narrow alleyways where people walk — suggesting urban hardship or confinement. It then cuts to a public rally where a woman speaks into a microphone while holding a sign, joined by four individuals holding signs that read “Én is cigány vagyok” (“I am also a Roma”), asserting identity and solidarity. A man in a suit signs a document, implying institutional recognition or legal action. The final frame overlays an animated character onto a real-world archway with traffic, blending symbolic representation with urban reality — possibly signifying cultural endurance or resistance within a modern setting.
```

**txt2** (cited)

```
[00:29:50-00:30:00 | episodic 10sec] The video segment begins with an aerial view of a densely packed, cluttered apartment building, followed by scenes of people walking down a narrow alleyway. The footage then transitions to a public gathering where a woman speaks into a microphone while holding a sign, and a group of four individuals stand together holding signs that read "Én is cigány vagyok" (I am also a Roma). The scene shifts to a man in a suit seated at a table, signing a document. The final frames show an animated character superimposed over a real-world image of a large archway, with cars passing by in the background.
```

**txt3** (cited)

```
[00:28:30-00:29:00 | episodic 30sec] **[Event 1: Opening Visuals and Setting Introduction]**  
The video opens with a black-and-white close-up of a young child staring directly at the camera, followed by a shot of another child gazing out a window — establishing an emotional or observational tone. The scene then shifts to color footage of a group of men — some in casual clothes, others in uniforms — walking outdoors near a large white truck marked “EUROPA,” suggesting a logistical or institutional operation in an urban setting with trees and buildings visible.

**[Event 2: Formal Stance and Repatriation Announcement]**  
A man and woman stand in a parking lot, arms crossed and looking seriously at the camera, signaling a moment of authority or confrontation. The scene then cuts to a woman in a red headscarf standing among a group outdoors, followed by a text overlay announcing: “Bonn to Expel Thousands of Romanians, Gypsies: Repatriation: Bucharest will take back its citizens who don't qualify for asylum under German law.” This frames the video’s central theme — forced repatriation under legal or political pressure.

**[Event 3: Archival Footage and Symbolic Labor]**  
The video transitions to archival footage of two men moving a large flat object — possibly a table or panel — near a pile of bricks and a white bus, implying manual labor or dismantling, perhaps symbolizing displacement or institutional dismantling.

**[Event 4: Data Visualization and Animated Commentary]**  
A bar chart titled “Romania: Corruption Levels” (1990–2007) is displayed, comparing PRS and TI corruption metrics. An animated character — brown-haired, wearing a black hat with a red band, white shirt, and red bow tie — appears thoughtfully touching their chin, visually underscoring the theme of corruption or critical analysis.

**[Event 5: Cultural Contrast and Closing Visual]**  
The video ends with a young man in a yellow shirt and light pants dancing barefoot on dirt ground in front of a weathered apartment building covered in satellite dishes — a stark, humanizing contrast to the preceding institutional and political imagery. The France 24 logo appears in the corner, indicating the source and journalistic framing of the content.

---

This sequence combines emotional, political, archival, analytical, and cultural elements to construct a layered narrative around Romanian repatriation, institutional critique, and human resilience.
```

**txt4** (cited)

```
[00:28:50-00:29:00 | episodic 10sec] A bar chart titled "Romania: Corruption Levels" is displayed, showing data from 1990 to 2007 with two categories: PRS Corruption and TI Corruption. An animated character with brown hair, wearing a black hat with a red band, a white shirt, and a red bow tie, appears on the right side of the chart, touching their chin thoughtfully. The scene then transitions to an outdoor shot of a young man in a yellow shirt and light pants dancing barefoot on a dirt ground in front of a large, weathered apartment building covered with numerous satellite dishes. The France 24 logo is visible in the bottom right corner.
```

**txt5**

```
[00:29:20-00:29:30 | episodic 10sec] The video opens with a shot of a massive landfill labeled "Pata Rat," followed by an aerial view of a rural settlement adjacent to the waste site. The scene then transitions to an office environment where several people are working at computer stations; a subtitle reads, "Teodora has just found a job with an IT giant." The final frames feature an animated character in traditional attire, posing cheerfully against a backdrop of a cityscape.
```

**txt6** (cited)

```
[00:26:00-00:26:30 | episodic 30sec] **[Event 1]** An animated character in traditional attire stands before urban apartment buildings, followed by a vintage brass band photograph, archival footage of a woman dancing and a smiling man, concluding with a woman in a red headscarf speaking outdoors in front of a blue building — establishing a visual narrative blending cultural memory and personal testimony.

**[Event 2]** The video transitions to a woman in a red headscarf speaking with children nearby, then cuts to another woman holding white sticks in a market, followed by a still of Nicolae and Elena Ceaușescu, archival footage of Nicolae Ceaușescu at a rally with a red-outfit figure in a picture-in-picture, then a woman holding a child indoors, ending with a low-resolution shot of an arm reaching toward a wall with writing — weaving personal and political imagery with historical figures.

**[Event 3]** A person writes on a large white surface, followed by hands flipping through a book and interacting with objects in a wooden box — suggesting reflection or archival research — then transitions to a 1990s street scene with pedestrians and vehicles — grounding the narrative in a specific era — concluding with a poster of an anime-style character overlaid with a Romanian news headline: “ROMANIAN GOVERNMENT ACKNOWLEDGES RESPONSIBILITY FOR ANTI-ROMANI POGROMS,” dated 27 April 2007 — marking a moment of institutional reckoning with historical injustice.
```

**txt7** (cited)

```
[00:25:50-00:26:00 | episodic 10sec] The video segment begins with a black-and-white scene of a man playing a violin in a group, followed by a close-up of a bride and groom sharing an intimate moment. The scene then transitions to a traffic light with a blue arrow sign, panning out to show a street with vintage cars and pedestrians in front of tall apartment buildings. The final frames overlay an anime-style character in front of the same urban backdrop.
```

**txt8** (cited)

```
[00:26:00-00:26:10 | episodic 10sec] An animated character in a traditional outfit with a black hat and red bow stands with arms outstretched in front of a backdrop of urban apartment buildings. The scene transitions to a vintage photograph of a brass band with adults and children holding instruments. Then, black-and-white archival footage shows a woman dancing with large hoop earrings, followed by a man in a hat smiling. The video ends with a woman in a red headscarf speaking to the camera outdoors in front of a blue building.
```

**txt9** (cited)

```
[video-level knowledge | semantic] (anime-style character, is in front of, urban backdrop)
```

**txt10**

```
[video-level knowledge | semantic] (Én is cigány vagyok, is part of, video segment)
```

**txt11**

```
[video-level knowledge | semantic] (person from behind, standing in, dimly lit colorful environment)
```

**txt12**

```
[video-level knowledge | semantic] (animated character, appears on, map)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:28:55 | 00:28:50–00:29:00 | `0RxMZBLeqRI:visual:00285000` | `outputs/p9p19_check_20261025_141401/frames_s3/0RxMZBLeqRI/00285000.jpg` |
| img2 |  | 00:26:05 | 00:26:00–00:26:10 | `0RxMZBLeqRI:visual:00260000` | `outputs/p9p19_check_20261025_141401/frames_s3/0RxMZBLeqRI/00260000.jpg` |
| img3 |  | 00:26:15 | 00:26:10–00:26:20 | `0RxMZBLeqRI:visual:00261000` | `outputs/p9p19_check_20261025_141401/frames_s3/0RxMZBLeqRI/00261000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:28:50-00:29:00 | video frame at 1735.0s] A bar chart titled "Romania: Corruption Levels" is displayed, showing data from 1990 to 2007 with two categories: PRS Corruption and TI Corruption. An animated character with brown hair, wearing a black hat with a red band, a white shirt, and a red bow tie, appears on the right side of the chart, touching their chin thoughtfully. The scene then transitions to an outdoor shot of a young man in a yellow shirt and light pants dancing barefoot on a dirt ground in front of a large, weathered apartment building covered with numerous satellite dishes. The France 24 logo is visible in the bottom right corner.
```

**img2**

```
[00:26:00-00:26:10 | video frame at 1565.0s] An animated character in a traditional outfit with a black hat and red bow stands with arms outstretched in front of a backdrop of urban apartment buildings. The scene transitions to a vintage photograph of a brass band with adults and children holding instruments. Then, black-and-white archival footage shows a woman dancing with large hoop earrings, followed by a man in a hat smiling. The video ends with a woman in a red headscarf speaking to the camera outdoors in front of a blue building.
```

**img3**

```
[00:26:10-00:26:20 | video frame at 1575.0s] The video segment transitions through various scenes: it begins with a woman in a red headscarf speaking outdoors in front of a blue building, with children nearby. The scene then shifts to another woman holding white sticks in what appears to be a market setting. Next, there is a still image of Nicolae and Elena Ceaușescu, followed by archival footage of Nicolae Ceaușescu speaking at a rally, with a person in a red outfit and sunglasses visible in a picture-in-picture overlay. The segment then cuts to a woman holding a young child indoors, and concludes with a blurry, low-resolution shot of a person’s arm reaching toward a wall with writing on it.
```
