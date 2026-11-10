# Section 3 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:22:22): `{'video_id': '0RxMZBLeqRI', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 18, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 6.45}`
- image request (2026-10-25 14:22:25): `{'video_id': '0RxMZBLeqRI', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 0.88}`
- L1 filter LLM call: prompt 10863 tokens, output 76 tokens, 5.3 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 30sec | 00:21:30–00:22:00 | 1 / 0.032258 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_43` |
| txt2 | ✓ | worldmm-episodic | 10sec | 00:22:00–00:22:10 | 2 / 0.032002 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_132` |
| txt3 | ✓ | worldmm-episodic | 10sec | 00:21:40–00:21:50 | 3 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_130` |
| txt4 | ✓ | worldmm-episodic | 10sec | 00:21:50–00:22:00 | 4 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_131` |
| txt5 | ✓ | worldmm-episodic | 30sec | 00:20:30–00:21:00 | 5 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_41` |
| txt6 | ✓ | worldmm-episodic | 10sec | 00:26:20–00:26:30 | 6 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_158` |
| txt7 | ✓ | worldmm-episodic | 30sec | 00:26:00–00:26:30 | 7 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_52` |
| txt8 |  | worldmm-episodic | 3min | 00:18:00–00:21:00 | 8 / 0.048387 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:3min_6` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.032002 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_357` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.03101 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_356` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_258` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_260` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:21:30-00:22:00 | episodic 30sec] **[Event 1: Introduction of Historical Context Through Visuals]**  
The video opens with a modern-day outdoor scene featuring a woman speaking to two men—one in military attire and the other in a suit holding papers—suggesting a contemporary framing or commentary. The scene then shifts to two men assisting a seated woman beside a suitcase, implying a narrative of movement or transition. This is followed by a painting of a man and woman walking on a beach with a dog, overlaid with the year “1899,” setting a visual anchor for historical reflection.

**[Event 2: Emergence of Institutionalized Surveillance in Bavaria]**  
A black-and-white photograph of a large building appears, accompanied by text explaining that in 1899, security police in Munich established the “Central Office for Gypsy Affairs,” directed by Alfred Dillmann—a pivotal moment in institutionalized surveillance targeting Romani communities. This is followed by a black-and-white photo of children and young adults, possibly symbolizing the affected population or the generational impact of such policies.

**[Event 3: Archival Footage and Documentation of Systematic Discrimination]**  
The video transitions to archival footage of a European city street in 1905, with pedestrians and historic architecture, overlaid with the year “1905,” situating the viewer in a specific historical moment. This is followed by the display of the cover and an open page of the “Zigeuner-Buch” (Gypsy Book), a document used for racial categorization and surveillance of Romani people, complete with a stamped seal, underscoring bureaucratic enforcement of discrimination.

**[Event 4: Examination of Official Records and Institutionalized Racial Classification]**  
A close-up of a German-language official document, likely a letter or report, is shown against a blurred street scene. The document is flipped to reveal another page with German text and handwritten notes, suggesting ongoing administrative record-keeping and enforcement of discriminatory policies.

**[Event 5: Visual Depiction of Forced Segregation and State Control]**  
A black-and-white photograph depicts a line of people—many wrapped in blankets or traditional clothing—standing outside a brick building, flanked by uniformed soldiers. This image visually reinforces state control, forced displacement, or institutionalized segregation, possibly referencing Romani internment or forced labor during this period.

**[Event 6: Presentation of the Nuremberg Laws and Racial Categorization]**  
The video concludes with a chart titled “Die Nürnberger Gesetze” (The Nuremberg Laws), which systematically classifies individuals based on racial criteria using symbols and German labels such as “Deutschblütiger,” “Mischling 2. Grades,” “Mischling 1. Grades,” and “Jude.” The chart uses visual indicators (circles with crosses and black dots) to denote racial purity or classification, highlighting the codification of racial hierarchy and the institutionalization of antisemitism and anti-Romani policies in Nazi Germany.

This sequence of visuals and text constructs a chronological and thematic narrative tracing the evolution of state-sponsored surveillance, racial categorization, and institutionalized discrimination against Romani and Jewish populations in late 19th- and early 20th-century Europe, culminating in the formal racial laws of Nazi Germany.
```

**txt2** (cited)

```
[00:22:00-00:22:10 | episodic 10sec] The video displays a historical Nazi-era document titled "Die Nürnberger Gesetze" (The Nuremberg Laws), which categorizes individuals based on racial and ethnic classifications, including "Deutschblütiger" (German-blooded), "Mischling 2. Grades" (Mischling of the second degree), "Mischling 1. Grades" (Mischling of the first degree), and "Jude" (Jew), with corresponding symbols and annotations. The scene then transitions to a series of black-and-white mugshots from the Gestapo, showing a man named Horvath, Ludwig, Leitani, born January 12, 1889, identified as a "Zigeuner" (Gypsy), followed by a woman named Huber, Helene Baranks, born in 1874, also identified as a "Zigeunerin" (Gypsy woman). The images are presented in a straightforward, archival style, with no accompanying audio or narration.
```

**txt3** (cited)

```
[00:21:40-00:21:50 | episodic 10sec] A black-and-white photograph shows a group of people, including several children, posing together outdoors. The scene then transitions to archival footage of a European city street in 1905, with pedestrians walking past historic buildings. An overlay of the year "1905" appears on screen. The footage then shifts to display the cover of a document titled "Zigeuner-Buch," followed by an open page from the book, which contains text and a stamped seal.
```

**txt4** (cited)

```
[00:21:50-00:22:00 | episodic 10sec] The video segment begins with a close-up of a historical document, which appears to be a typed letter or official paper, displayed against a blurred background of a black-and-white street scene with people. The document is in German and features a stamp at the bottom. The view then transitions to show the document being flipped to reveal another page, which also contains German text and a handwritten notation.

The scene then shifts to a black-and-white historical photograph depicting a line of people, many wrapped in blankets or traditional clothing, standing outside a brick building. Two uniformed soldiers are visible, one standing prominently in the foreground and another near a bicycle on the right side.

Finally, the video displays a chart titled "Die Nürnberger Gesetze" (The Nuremberg Laws), which categorizes individuals based on racial criteria using symbols and text, including labels such as "Deutschblütiger," "Mischling 2. Grades," "Mischling 1. Grades," and "Jude." The chart uses circles with crosses and black dots to indicate different classifications, along with explanatory text in German.
```

**txt5** (cited)

```
[00:20:30-00:21:00 | episodic 30sec] **[Event 1: Evolutionary and Biblical Imagery as Framing Devices]**  
The video opens with a sepia-toned portrait of Charles Darwin, overlaid with his name, followed by a classic illustration tracing human evolution from apelike ancestors to modern humans — visually framing the theme of biological progression. The scene then shifts to an aged, vintage aesthetic, showing an open book labeled “GENESIS,” accompanied by imagery of Adam and Eve and God creating the world, suggesting a contrast or tension between scientific evolution and religious creation narratives.

**[Event 2: Darwin’s Racist Remarks and Historical Context]**  
A black-and-white illustration of Darwin seated in a chair is shown, with a text overlay quoting him as referring to Jews and Gypsies as “not culturally advanced” compared to “territorially settled” peoples — directly linking his scientific legacy to racial prejudice. The scene transitions to archival black-and-white footage of a person pushing a wheeled cart along a cobblestone street, with the History Channel logo visible, indicating the segment’s documentary context and grounding the content in historical presentation.

**[Event 3: Nazi Racial Laws and Systematic Persecution of Roma]**  
The video begins with a black-and-white shot of a covered wagon on a dirt road, symbolizing migration or displacement. It then cuts to a static image of “Die Nürnberger Gesetze,” a Nazi racial law document displaying a chart categorizing people by race and “impurity,” with symbols indicating degrees of Jewish ancestry — illustrating the institutionalization of racial hierarchy. The scene transitions to a black-and-white outdoor shot of people, including children, gathered near wooden barracks in a wooded area, evoking the conditions of forced settlement or concentration. The final frame overlays text stating that when the Nazis came to power in 1933, anti-Roma laws in German-speaking lands had already existed for centuries, and persecution intensified immediately — highlighting the historical continuity of systemic discrimination.
```

**txt6** (cited)

```
[00:26:20-00:26:30 | episodic 10sec] A person is seen writing on a large white surface, followed by a scene of hands flipping through a book and interacting with objects in a wooden box. The video then transitions to a street scene labeled "1990s," showing pedestrians and vehicles. Finally, the video displays a poster featuring an anime-style character with text in Romanian, overlaid with a news headline stating, "ROMANIAN GOVERNMENT ACKNOWLEDGES RESPONSIBILITY FOR ANTI-ROMANI POGROMS," dated 27 April 2007.
```

**txt7** (cited)

```
[00:26:00-00:26:30 | episodic 30sec] **[Event 1]** An animated character in traditional attire stands before urban apartment buildings, followed by a vintage brass band photograph, archival footage of a woman dancing and a smiling man, concluding with a woman in a red headscarf speaking outdoors in front of a blue building — establishing a visual narrative blending cultural memory and personal testimony.

**[Event 2]** The video transitions to a woman in a red headscarf speaking with children nearby, then cuts to another woman holding white sticks in a market, followed by a still of Nicolae and Elena Ceaușescu, archival footage of Nicolae Ceaușescu at a rally with a red-outfit figure in a picture-in-picture, then a woman holding a child indoors, ending with a low-resolution shot of an arm reaching toward a wall with writing — weaving personal and political imagery with historical figures.

**[Event 3]** A person writes on a large white surface, followed by hands flipping through a book and interacting with objects in a wooden box — suggesting reflection or archival research — then transitions to a 1990s street scene with pedestrians and vehicles — grounding the narrative in a specific era — concluding with a poster of an anime-style character overlaid with a Romanian news headline: “ROMANIAN GOVERNMENT ACKNOWLEDGES RESPONSIBILITY FOR ANTI-ROMANI POGROMS,” dated 27 April 2007 — marking a moment of institutional reckoning with historical injustice.
```

**txt8**

```
[00:18:00-00:21:00 | episodic 3min] **[Event 1: Historical Reconciliation and Institutional Transition]**  
The video opens with symbolic imagery of labor and legal emancipation — a historical crop-processing scene, Article XIII abolishing slavery, and Romanian-EU flags united — transitioning to a handshake motif, signifying reconciliation and institutional partnership. This sets a thematic tone of legal and social transformation.

**[Event 2: National Identity and Historical Critique]**  
A split-screen of Romanian and French cultural symbols is juxtaposed with stark historical critique: “Barbaric Backwards Inhumane” overlays labor imagery, culminating in a 1837 portrait. This frames the nation’s past through a lens of moral and political reckoning, linking identity to historical critique.

**[Event 3: Emancipation and Institutional Legacy]**  
Alexandru Ghica (1837) is introduced as a key figure in Roma emancipation, contextualized within a timeline of abolition (1844–1856). The video transitions from historical unrest to a surreal video game setting, symbolizing the fragmented, contested legacy of emancipation.

**[Event 1: Fantasy to Historical Pivot]**  
A fantasy video game world abruptly transitions to a 19th-century rural village painting (1842), overlaid with text detailing the gradual abolition of slavery in Wallachia and Moldavia — establishing a narrative pivot from myth to historical record.

**[Event 2: Political Mobilization and Institutionalization]**  
The video depicts 19th-century political gatherings, battlefield scenes, and a constitutional rally, culminating in a collective oath — symbolizing the institutionalization of national sovereignty and the consolidation of political power.

**[Event 3: Religious, Rural, and Diplomatic Imagery]**  
Sepia-toned religious and rural scenes transition to formal diplomatic meetings, highlighting the interplay between faith, community, and statecraft in shaping national identity amid historical transformation.

**[Event 1: Cultural Heritage and Ritual]**  
Visual vignettes of Gypsy life — from tambourine-playing figures to candle-lit ceremonies — present cultural continuity without audio, emphasizing ritual and tradition as anchors of identity.

**[Event 2: Myth, Migration, and Nomadism]**  
A dramatic reenactment of Gypsy storytelling transitions to historical imagery of caravans and rural shelters, evoking migration and the persistence of nomadic heritage.

**[Event 3: Folklore and Title Transition]**  
A desert caravan scene shifts to a man confronting a bear, followed by card-shuffling and an elderly woman’s portrait — concluding with the stylized title “THE DEVOURING,” signaling a thematic pivot toward danger or mystery.

**[Event 1: Title and Historical Framing]**  
The title “THE DEVOURING CHAPTER VI” opens over a vibrant pointillist park scene (Late XIX–Mid XX), establishing a visual and temporal frame for the historical narrative to follow.

**[Event 2: Racial Pseudoscience and Textual Framing]**  
Black-and-white racial classifications (“IRISH IBERIAN,” “NEGRO”) are paired with pseudoscientific text, laying the groundwork for examining historical racism and its institutional roots.

**[Event 3: Satirical Juxtaposition]**  
Anatomical comparisons of skulls are humorously labeled “wojak shitpost,” contrasting historical pseudoscience with modern internet satire — highlighting the absurdity of racial hierarchies.

**[Event 4: Scholarly Documentation and Dehumanization]**  
A street scene from the late 1800s transitions to portraits of Ernst Haeckel and Tetzner’s *Geschichte der Zigeuner*, with text quoting dehumanizing descriptions of Roma — reinforcing the video’s focus on historical racism.

**[Event 1: Evolutionary and Biblical Framing]**  
Darwin’s portrait and evolutionary illustrations are paired with Genesis imagery, visually framing the tension between scientific and religious narratives of human origin.

**[Event 2: Darwin’s Racist Legacy]**  
Darwin’s quote on Gypsies and Jews is juxtaposed with archival footage, linking his scientific legacy to racial prejudice — contextualizing his work within a broader history of pseudoscientific racism.

**[Event 3: Nazi Persecution and Institutionalized Hate]**  
The video shows Nazi racial laws and concentration camp imagery, concluding with text noting that anti-Roma laws predated Nazi rule — emphasizing the historical continuity of systemic discrimination.
```

**txt9**

```
[video-level knowledge | semantic] (poster, has news headline, ROMANIAN GOVERNMENT ACKNOWLEDGES RESPONSIBILITY FOR ANTI-ROMANI POGROMS)
```

**txt10**

```
[video-level knowledge | semantic] (poster, has text in, Romanian)
```

**txt11**

```
[video-level knowledge | semantic] (Zigeuner-Buch, is a document, with cover and stamped seal)
```

**txt12**

```
[video-level knowledge | semantic] (Die Nürnberger Gesetze, uses visual symbols, such as circles with crosses and black dots)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:22:05 | 00:22:00–00:22:10 | `0RxMZBLeqRI:visual:00220000` | `outputs/p9p19_check_20261025_141401/frames_s3/0RxMZBLeqRI/00220000.jpg` |
| img2 | ✓ | 00:24:05 | 00:24:00–00:24:10 | `0RxMZBLeqRI:visual:00240000` | `outputs/p9p19_check_20261025_141401/frames_s3/0RxMZBLeqRI/00240000.jpg` |
| img3 | ✓ | 00:23:55 | 00:23:50–00:24:00 | `0RxMZBLeqRI:visual:00235000` | `outputs/p9p19_check_20261025_141401/frames_s3/0RxMZBLeqRI/00235000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:22:00-00:22:10 | video frame at 1325.0s] The video displays a historical Nazi-era document titled "Die Nürnberger Gesetze" (The Nuremberg Laws), which categorizes individuals based on racial and ethnic classifications, including "Deutschblütiger" (German-blooded), "Mischling 2. Grades" (Mischling of the second degree), "Mischling 1. Grades" (Mischling of the first degree), and "Jude" (Jew), with corresponding symbols and annotations. The scene then transitions to a series of black-and-white mugshots from the Gestapo, showing a man named Horvath, Ludwig, Leitani, born January 12, 1889, identified as a "Zigeuner" (Gypsy), followed by a woman named Huber, Helene Baranks, born in 1874, also identified as a "Zigeunerin" (Gypsy woman). The images are presented in a straightforward, archival style, with no accompanying audio or narration.
```

**img2** (cited)

```
[00:24:00-00:24:10 | video frame at 1445.0s] The video segment shows a series of black-and-white historical images. It begins with a group of men and children sitting on the ground in an open field, with a fence and a solitary figure standing in the background. The scene transitions to a group of children and young women posing together outdoors, with buildings visible behind them. The final frames depict a crowd of people, including men, women, and children, standing behind a barbed wire fence, with the "British Pathé" logo visible in the corner. There is no audible content in the segment.
```

**img3** (cited)

```
[00:23:50-00:24:00 | video frame at 1435.0s] The video opens with an aerial view of a large, somber complex of brick buildings with red-tiled roofs, arranged in rows on either side of a central pathway. A small gatehouse stands at the end of the path. The scene is overcast, with bare trees in the background, creating a bleak, gray atmosphere. The camera pans left, revealing more of the sprawling compound, which appears to be a former concentration camp or similar institutional facility.

The scene then abruptly cuts to a black-and-white historical photograph. It shows a group of men, women, and children sitting on the ground in a barren, open field. They are dressed in worn clothing, and their expressions convey exhaustion and despair. A man stands in the background near a simple fence, overseeing the group. The image evokes a sense of displacement and suffering, likely depicting refugees or victims of a historical atrocity.
```
