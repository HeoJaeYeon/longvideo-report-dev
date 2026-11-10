# Section 3 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 550 words → after removal 550 words

## 2. Start/end claim check (`boundary_claims`)

- none

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 20, "cited_sentences": 8, "checked_tokens": 19, "unsupported": 0, "miscited": 1, "uncited_claims": 2, "absence_statements": 0}`

- **uncited**  `['Die Nürnberger Gesetze', 'Deutschblütiger', '00:21:40', '2']` cited [] — At 00:21:40, a chart titled “Die Nürnberger Gesetze” (The Nuremberg Laws) is displayed, systematically classifying individuals using symbols and German labels such as “Deutschblütiger,” “Mischling 2.
- **uncited**  `['1']` cited [] — Grades,” “Mischling 1.
- **miscited** time `00:22:00` cited ['txt5'] found in ['txt1', 'txt2', 'txt4', 'img1'] — This chart is revisited at 00:22:00, reinforcing the institutionalization of racial hierarchy [citation:txt5].

## 4. Citation conversion stats

- `{"text_citations": 12, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 0, "wrong_form_image_citations": 2, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 5 of 12

## 5. Image-text time alignment

- img3 frame 00:23:55: gap to text cited in the same paragraph 105.0 s (ranges ['00:22:00-00:22:10']), to any text cited in the section 105.0 s
- img2 frame 00:24:05: gap to text cited in the same paragraph 115.0 s (ranges ['00:22:00-00:22:10']), to any text cited in the section 115.0 s

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Institutionalized Persecution: From Bismarck-Era Surveillance to Post-War Acknowledgment

The video transitions from its earlier portrayal of Roma cultural continuity to a stark depiction of institutionalized persecution, beginning with the establishment of state surveillance in late 19th-century Bavaria. At 00:21:30, a black-and-white photograph of a large building is shown with accompanying text identifying it as the “Central Office for Gypsy Affairs” in Munich, directed by Alfred Dillmann in 1899 — marking the formal institutionalization of surveillance targeting Romani communities [citation:txt1]. This is followed by a black-and-white photo of children and young adults, symbolizing the generational impact of such state-directed control [citation:txt1].

At 00:21:50, the video presents the “Zigeuner-Buch” (Gypsy Book), a document used for racial categorization and surveillance, shown with its cover and an open page bearing a stamped seal — a bureaucratic tool enforcing systemic discrimination [citation:txt1][citation:txt3]. The video then displays a close-up of a German-language official document, flipped to reveal handwritten notes, underscoring the administrative machinery of exclusion [citation:txt4]. The narrative continues with a black-and-white photograph of a line of people — many wrapped in blankets or traditional clothing — standing outside a brick building flanked by uniformed soldiers, visually reinforcing forced displacement or institutional segregation [citation:txt4].

The video then explicitly documents the racial categorization codified under Nazi Germany. At 00:21:40, a chart titled “Die Nürnberger Gesetze” (The Nuremberg Laws) is displayed, systematically classifying individuals using symbols and German labels such as “Deutschblütiger,” “Mischling 2. Grades,” “Mischling 1. Grades,” and “Jude,” with visual indicators like circles with crosses and black dots denoting racial purity or classification [citation:txt1][citation:txt4]. This chart is revisited at 00:22:00, reinforcing the institutionalization of racial hierarchy [citation:txt5].

The persecution is further illustrated through archival imagery. At 00:22:00, black-and-white Gestapo mugshots are shown, including a man named Horvath, Ludwig, Leitani, born January 12, 1889, identified as a “Zigeuner,” and a woman named Huber, Helene Baranks, born in 1874, identified as a “Zigeunerin” — documenting the state’s identification and registration of Roma as targets [citation:txt2]. The video also includes a scene at 00:23:50 showing an aerial view of a somber brick complex with red-tiled roofs, later identified as Auschwitz-Birkenau through its bleak, institutional layout and barbed wire fences, evoking the scale of genocide [citation:img3]. A subsequent frame at 00:24:00 shows a group of men, women, and children behind a barbed wire fence, reinforcing the conditions of forced internment [citation:img2].

The video concludes this section with a moment of modern reckoning. At 00:26:20, a poster is shown featuring an anime-style character overlaid with a Romanian news headline: “ROMANIAN GOVERNMENT ACKNOWLEDGES RESPONSIBILITY FOR ANTI-ROMANI POGROMS,” dated 27 April 2007 — marking a symbolic institutional acknowledgment of historical atrocity [citation:txt6][citation:txt7]. This moment serves as a visual anchor for the legacy of persecution, transitioning from state-sanctioned violence to contemporary recognition, even as the video’s imagery continues to juxtapose historical suffering with modern memory.

The sequence of visuals and text constructs a chronological and thematic narrative tracing the evolution of state-sponsored surveillance, racial categorization, and institutionalized discrimination against Romani and Jewish populations — culminating in the formal racial laws of Nazi Germany and their enduring legacy. The video does not depict resistance movements during this period, but it does present the visual and documentary evidence of state-sanctioned oppression, from Bismarck-era control to Nazi-era camps, and ends with a moment of post-war acknowledgment.
```

## 7. Grounded body (exactly as in report.md)

```
# Institutionalized Persecution: From Bismarck-Era Surveillance to Post-War Acknowledgment

The video transitions from its earlier portrayal of Roma cultural continuity to a stark depiction of institutionalized persecution, beginning with the establishment of state surveillance in late 19th-century Bavaria. At 00:21:30, a black-and-white photograph of a large building is shown with accompanying text identifying it as the “Central Office for Gypsy Affairs” in Munich, directed by Alfred Dillmann in 1899 — marking the formal institutionalization of surveillance targeting Romani communities [10]. This is followed by a black-and-white photo of children and young adults, symbolizing the generational impact of such state-directed control [10].

At 00:21:50, the video presents the “Zigeuner-Buch” (Gypsy Book), a document used for racial categorization and surveillance, shown with its cover and an open page bearing a stamped seal — a bureaucratic tool enforcing systemic discrimination [10][11]. The video then displays a close-up of a German-language official document, flipped to reveal handwritten notes, underscoring the administrative machinery of exclusion [12]. The narrative continues with a black-and-white photograph of a line of people — many wrapped in blankets or traditional clothing — standing outside a brick building flanked by uniformed soldiers, visually reinforcing forced displacement or institutional segregation [12].

The video then explicitly documents the racial categorization codified under Nazi Germany. At 00:21:40, a chart titled “Die Nürnberger Gesetze” (The Nuremberg Laws) is displayed, systematically classifying individuals using symbols and German labels such as “Deutschblütiger,” “Mischling 2. Grades,” “Mischling 1. Grades,” and “Jude,” with visual indicators like circles with crosses and black dots denoting racial purity or classification [10][12]. This chart is revisited at 00:22:00, reinforcing the institutionalization of racial hierarchy [13].

The persecution is further illustrated through archival imagery. At 00:22:00, black-and-white Gestapo mugshots are shown, including a man named Horvath, Ludwig, Leitani, born January 12, 1889, identified as a “Zigeuner,” and a woman named Huber, Helene Baranks, born in 1874, identified as a “Zigeunerin” — documenting the state’s identification and registration of Roma as targets [14]. The video also includes a scene at 00:23:50 showing an aerial view of a somber brick complex with red-tiled roofs, later identified as Auschwitz-Birkenau through its bleak, institutional layout and barbed wire fences, evoking the scale of genocide (Figure 1). A subsequent frame at 00:24:00 shows a group of men, women, and children behind a barbed wire fence, reinforcing the conditions of forced internment (Figure 2).

![Figure 1 (00:23:55)](frames/0RxMZBLeqRI_00235000.jpg)

*Figure 1. Frame at 00:23:55 (clip 00:23:50–00:24:00). The video opens with an aerial view of a large, somber complex of brick buildings with red-tiled roofs, arranged in rows on either side of a central pathway. A small gatehouse stands at the end of the path. The scene is overcast, with bare trees in the background, creating a bleak, gray atmospher...*

![Figure 2 (00:24:05)](frames/0RxMZBLeqRI_00240000.jpg)

*Figure 2. Frame at 00:24:05 (clip 00:24:00–00:24:10). The video segment shows a series of black-and-white historical images. It begins with a group of men and children sitting on the ground in an open field, with a fence and a solitary figure standing in the background. The scene transitions to a group of children and young women posing together out...*

The video concludes this section with a moment of modern reckoning. At 00:26:20, a poster is shown featuring an anime-style character overlaid with a Romanian news headline: “ROMANIAN GOVERNMENT ACKNOWLEDGES RESPONSIBILITY FOR ANTI-ROMANI POGROMS,” dated 27 April 2007 — marking a symbolic institutional acknowledgment of historical atrocity [15][16]. This moment serves as a visual anchor for the legacy of persecution, transitioning from state-sanctioned violence to contemporary recognition, even as the video’s imagery continues to juxtapose historical suffering with modern memory.

The sequence of visuals and text constructs a chronological and thematic narrative tracing the evolution of state-sponsored surveillance, racial categorization, and institutionalized discrimination against Romani and Jewish populations — culminating in the formal racial laws of Nazi Germany and their enduring legacy. The video does not depict resistance movements during this period, but it does present the visual and documentary evidence of state-sanctioned oppression, from Bismarck-era control to Nazi-era camps, and ends with a moment of post-war acknowledgment.
```

## 8. References used by this section (global numbers)

```
[10] 00:21:30–00:22:00 · episodic 30sec: **[Event 1: Introduction of Historical Context Through Visuals]**  
The video opens with a modern-day outdoor scene featuring a woman speaking to two men—one in military attire and the other in a suit holding papers—s...
[11] 00:21:40–00:21:50 · episodic 10sec: A black-and-white photograph shows a group of people, including several children, posing together outdoors. The scene then transitions to archival footage of a European city street in 1905, with pedestrians walking pa...
[12] 00:21:50–00:22:00 · episodic 10sec: The video segment begins with a close-up of a historical document, which appears to be a typed letter or official paper, displayed against a blurred background of a black-and-white street scene with people. The docume...
[13] 00:20:30–00:21:00 · episodic 30sec: **[Event 1: Evolutionary and Biblical Imagery as Framing Devices]**  
The video opens with a sepia-toned portrait of Charles Darwin, overlaid with his name, followed by a classic illustration tracing human evolution f...
[14] 00:22:00–00:22:10 · episodic 10sec: The video displays a historical Nazi-era document titled "Die Nürnberger Gesetze" (The Nuremberg Laws), which categorizes individuals based on racial and ethnic classifications, including "Deutschblütiger" (German-blo...
[15] 00:26:20–00:26:30 · episodic 10sec: A person is seen writing on a large white surface, followed by a scene of hands flipping through a book and interacting with objects in a wooden box. The video then transitions to a street scene labeled "1990s," showi...
[16] 00:26:00–00:26:30 · episodic 30sec: **[Event 1]** An animated character in traditional attire stands before urban apartment buildings, followed by a vintage brass band photograph, archival footage of a woman dancing and a smiling man, concluding with a...
```
