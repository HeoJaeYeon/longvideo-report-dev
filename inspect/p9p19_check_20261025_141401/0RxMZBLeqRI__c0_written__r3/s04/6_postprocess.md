# Section 4 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 404 words → after removal 404 words

## 2. Start/end claim check (`boundary_claims`)

- none

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 13, "cited_sentences": 4, "checked_tokens": 5, "unsupported": 0, "miscited": 1, "uncited_claims": 2, "absence_statements": 0}`

- **uncited**  `['00:29:50']` cited [] — At 00:29:50, a public rally unfolds where a woman speaks into a microphone while holding a sign.
- **miscited** time `00:29:30` cited ['txt8'] found in ['txt5'] — The section concludes with a scene at 00:29:30, showing a man holding a young child while two others stand nearby in a rural, dilapidated setting [citation:txt8].
- **uncited**  `['00:28:50', '00:30:00']` cited [] — The video’s focus on these scenes, particularly between 00:28:50 and 00:30:00, underscores a narrative of quiet resistance and enduring humanity, rooted in lived experience rather than political rhetoric.

## 4. Citation conversion stats

- `{"text_citations": 12, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 3, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 7 of 12

## 5. Image-text time alignment

- img1 frame 00:23:15: gap to text cited in the same paragraph 195.0 s (ranges ['00:26:30-00:27:00']), to any text cited in the section 195.0 s
- img2 frame 00:24:05: gap to text cited in the same paragraph 145.0 s (ranges ['00:26:30-00:27:00']), to any text cited in the section 145.0 s
- img3 frame 00:26:05: gap to text cited in the same paragraph 25.0 s (ranges ['00:26:30-00:27:00']), to any text cited in the section 25.0 s

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Roma Resilience and Cultural Endurance Amid Oppression

At 00:29:50, a public rally unfolds where a woman speaks into a microphone while holding a sign. Beside her, four individuals stand together, each holding a sign that reads “Én is cigány vagyok” — Hungarian for “I am also a Roma” — asserting collective identity and solidarity [citation:txt4][citation:txt5]. This moment of public declaration is visually anchored by the woman’s direct address and the unified stance of the group, contrasting institutional erasure with communal affirmation. The scene transitions to a man in a suit seated at a table, signing a document — an act that implies formal recognition or legal action, though the nature of the document is not specified — suggesting a moment of institutional reckoning or acknowledgment [citation:txt4][citation:txt5]. The segment closes with an animated character superimposed over a real-world image of a large archway with cars passing by, blending symbolic representation with urban reality — possibly signifying cultural endurance within a modern setting [citation:txt4][citation:txt5].

Earlier in the section, at 00:28:50, the video presents a young man in a yellow shirt and light pants dancing barefoot on a dirt ground in front of a large, weathered apartment building covered with numerous satellite dishes [citation:txt1][citation:txt3]. This image — juxtaposed against the preceding institutional and political imagery — offers a stark, humanizing contrast, emphasizing quiet resistance and cultural continuity through everyday joy and movement. The France 24 logo is visible in the bottom right corner, indicating the journalistic framing of the content [citation:txt1][citation:txt3].

The section concludes with a scene at 00:29:30, showing a man holding a young child while two others stand nearby in a rural, dilapidated setting [citation:txt8]. The environment suggests neglect or abandonment, yet the act of holding the child conveys care, resilience, and continuity — a quiet assertion of dignity amid hardship. The setting, with its worn structures and absence of modern amenities, reinforces the theme of enduring cultural presence despite historical trauma [citation:txt8].

These moments — from the public affirmation of Roma identity to the solitary dance before a satellite-dish-covered building and the tender act of holding a child in a rural ruin — collectively illustrate how Roma people assert agency, preserve cultural identity, and sustain dignity in the face of systemic oppression. The video’s focus on these scenes, particularly between 00:28:50 and 00:30:00, underscores a narrative of quiet resistance and enduring humanity, rooted in lived experience rather than political rhetoric.

![](citation:img1)  
![](citation:img2)  
![](citation:img3)
```

## 7. Grounded body (exactly as in report.md)

```
# Roma Resilience and Cultural Endurance Amid Oppression

At 00:29:50, a public rally unfolds where a woman speaks into a microphone while holding a sign. Beside her, four individuals stand together, each holding a sign that reads “Én is cigány vagyok” — Hungarian for “I am also a Roma” — asserting collective identity and solidarity [17][18]. This moment of public declaration is visually anchored by the woman’s direct address and the unified stance of the group, contrasting institutional erasure with communal affirmation. The scene transitions to a man in a suit seated at a table, signing a document — an act that implies formal recognition or legal action, though the nature of the document is not specified — suggesting a moment of institutional reckoning or acknowledgment [17][18]. The segment closes with an animated character superimposed over a real-world image of a large archway with cars passing by, blending symbolic representation with urban reality — possibly signifying cultural endurance within a modern setting [17][18].

Earlier in the section, at 00:28:50, the video presents a young man in a yellow shirt and light pants dancing barefoot on a dirt ground in front of a large, weathered apartment building covered with numerous satellite dishes [19][20]. This image — juxtaposed against the preceding institutional and political imagery — offers a stark, humanizing contrast, emphasizing quiet resistance and cultural continuity through everyday joy and movement. The France 24 logo is visible in the bottom right corner, indicating the journalistic framing of the content [19][20].

The section concludes with a scene at 00:29:30, showing a man holding a young child while two others stand nearby in a rural, dilapidated setting [21]. The environment suggests neglect or abandonment, yet the act of holding the child conveys care, resilience, and continuity — a quiet assertion of dignity amid hardship. The setting, with its worn structures and absence of modern amenities, reinforces the theme of enduring cultural presence despite historical trauma [21].

These moments — from the public affirmation of Roma identity to the solitary dance before a satellite-dish-covered building and the tender act of holding a child in a rural ruin — collectively illustrate how Roma people assert agency, preserve cultural identity, and sustain dignity in the face of systemic oppression. The video’s focus on these scenes, particularly between 00:28:50 and 00:30:00, underscores a narrative of quiet resistance and enduring humanity, rooted in lived experience rather than political rhetoric.

![Figure 2 (00:23:15)](frames/0RxMZBLeqRI_00231000.jpg)

*Figure 2. Frame at 00:23:15 (clip 00:23:10–00:23:20). The video segment opens with a wide shot of a large, densely packed crowd, many waving flags, suggesting a public gathering or rally. The scene cuts to a man speaking at a podium, flanked by uniformed individuals, indicating a formal address or ceremony. The footage then shifts to color footage o...*

![Figure 3 (00:24:05)](frames/0RxMZBLeqRI_00240000.jpg)

*Figure 3. Frame at 00:24:05 (clip 00:24:00–00:24:10). The video segment shows a series of black-and-white historical images. It begins with a group of men and children sitting on the ground in an open field, with a fence and a solitary figure standing in the background. The scene transitions to a group of children and young women posing together out...*

![Figure 4 (00:26:05)](frames/0RxMZBLeqRI_00260000.jpg)

*Figure 4. Frame at 00:26:05 (clip 00:26:00–00:26:10). An animated character in a traditional outfit with a black hat and red bow stands with arms outstretched in front of a backdrop of urban apartment buildings. The scene transitions to a vintage photograph of a brass band with adults and children holding instruments. Then, black-and-white archival...*
```

## 8. References used by this section (global numbers)

```
[17] 00:29:50–00:30:00 · episodic 10sec: The video segment begins with an aerial view of a densely packed, cluttered apartment building, followed by scenes of people walking down a narrow alleyway. The footage then transitions to a public gathering where a w...
[18] 00:29:30–00:30:00 · episodic 30sec: An animated woman in traditional attire stands with open arms against a cityscape, symbolizing cultural presence or welcome, followed by a sepia-toned religious figure and snowy boots, evoking historical or spiritual...
[19] 00:28:50–00:29:00 · episodic 10sec: A bar chart titled "Romania: Corruption Levels" is displayed, showing data from 1990 to 2007 with two categories: PRS Corruption and TI Corruption. An animated character with brown hair, wearing a black hat with a red...
[20] 00:28:30–00:29:00 · episodic 30sec: **[Event 1: Opening Visuals and Setting Introduction]**  
The video opens with a black-and-white close-up of a young child staring directly at the camera, followed by a shot of another child gazing out a window — esta...
[21] 00:26:30–00:27:00 · episodic 30sec: **[Event 1: Tense Physical Confrontation and Symbolic Imagery]**  
Two muscular men engage in a tense, hand-clasped standoff, one bleeding, suggesting a physical or emotional conflict. The scene transitions to a symbo...
```
