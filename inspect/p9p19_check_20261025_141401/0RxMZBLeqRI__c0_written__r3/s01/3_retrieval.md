# Section 1 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:22:41): `{'video_id': '0RxMZBLeqRI', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 18, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 6.38}`
- image request (2026-10-25 14:22:44): `{'video_id': '0RxMZBLeqRI', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 0.88}`
- L1 filter LLM call: prompt 11786 tokens, output 68 tokens, 5.2 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 30sec | 00:00:00–00:00:30 | 1 / 0.04918 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_0` |
| txt2 | ✓ | worldmm-episodic | 10sec | 00:00:00–00:00:10 | 2 / 0.032787 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_0` |
| txt3 | ✓ | worldmm-episodic | 10sec | 00:00:10–00:00:20 | 3 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_1` |
| txt4 |  | worldmm-episodic | 30sec | 00:02:00–00:02:30 | 4 / 0.016129 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_4` |
| txt5 |  | worldmm-episodic | 30sec | 00:20:00–00:20:30 | 5 / 0.016129 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_40` |
| txt6 |  | worldmm-episodic | 30sec | 00:21:30–00:22:00 | 6 / 0.016129 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_43` |
| txt7 |  | worldmm-episodic | 3min | 00:21:00–00:24:00 | 7 / 0.016129 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:3min_7` |
| txt8 |  | worldmm-episodic | 30sec | 00:27:00–00:27:30 | 8 / 0.015873 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_54` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.032522 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_5` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.032002 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_29` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_318` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_370` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:00:00-00:00:30 | episodic 30sec] **[Event 1: Introduction and Context Setting]**  
The video opens with a disclaimer clarifying that “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s contested history and affirming its non-slandrous intent. The screen transitions to a map of the Balkans, followed by a montage of internet memes and historical battle tables — including a satirical image labeled “POV: TITO INVENTING MACEDONIANS” — while audio commentary underscores the entrenched ethnic hatred in the region, highlighting how certain groups are disproportionately targeted.

**[Event 2: Visual Montage and Narrated Commentary on Roma Perception]**  
A text overlay introduces the historical and cultural presence of the Roma in the Balkans, while visuals show a person walking past a trash can, then turning away — possibly symbolizing marginalization. The scene cuts to a man in a white suit and red tie seated beside a woman in a patterned top, followed by a shirtless man shouting outdoors — suggesting social tension or protest. A bearded man speaks in front of a lit background, likely delivering commentary or narration. The segment concludes with a still image of Barack Obama superimposed over dilapidated buildings, overlaid with the text “POREKLOM SAM CIGANIN” (“I am a Gypsy by origin”), fading to black — reinforcing the theme of identity, erasure, and societal perception. Throughout, narration emphasizes the Roma’s complex and often negative social portrayal.

**[Event 3: Historical and Cultural Representation of the Roma]**  
The video begins with a title card reading “GYPSIES,” followed by sepia-toned historical photographs of Roma families in traditional attire — some gathered around caravans, others posing formally — illustrating their long-standing presence. The scene transitions to a modern-day street parade featuring participants in colorful traditional clothing and contemporary attire, marching with flags including the Roma flag (red wheel on green), alongside Ukrainian and EU flags. Narration affirms the Roma’s integral role in Balkan culture and history, while acknowledging the lack of public knowledge due to generational stigma, prejudice, and insufficient scholarly research.
```

**txt2** (cited)

```
[00:00:00-00:00:10 | episodic 10sec] A disclaimer appears on a black screen, explaining that the term “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s complicated history and clarifying that it is not intended as a slur. The screen then transitions to a map of the Balkan region, followed by a montage of internet memes and historical battle tables, including a humorous image labeled “POV: TITO INVENTING MACEDONIANS.” Overlaid audio discusses ethnic hatred in the Balkans, noting that certain groups are often targeted more than others.
```

**txt3** (cited)

```
[00:00:10-00:00:20 | episodic 10sec] The video segment begins with a text overlay discussing the historical and cultural presence of the Roma, also known as Gypsies, in the Balkans, while simultaneously showing a person in a light blue shirt and dark pants walking past a trash can and then turning away. The scene cuts to a man in a white suit and red tie sitting beside a woman in a patterned top, followed by a shirtless man shouting outdoors. A man with a beard is then shown speaking in front of a lit background. The segment ends with a still image of Barack Obama superimposed over a backdrop of dilapidated buildings, with the text "POREKLOM SAM CIGANIN" displayed, before fading to black. Throughout, the narration discusses the Roma's complex and often negative perception in society.
```

**txt4**

```
[00:02:00-00:02:30 | episodic 30sec] **[Event 1: Introduction and Cultural Identity Framing]**  
The video opens with a visually symbolic shot of a bearded man with blue eyes gazing upward in awe against a blue-toned, rocky backdrop, setting a tone of wonder or historical reflection. It then cuts to two young men outdoors, one gesturing emphatically, with the word “Atsingani” overlaid — suggesting a cultural or linguistic identifier. The scene transitions to an animated map of the Balkans and Eastern Europe, where an anime-style girl in traditional attire gestures toward the region while speaking, visually anchoring the narrative in geographic and cultural context.

**[Event 2: Linguistic and Historical Context]**  
Text overlays sequentially display the words “CIGANI,” “CIGÁNYOK,” “TIGANI,” and “ZIGEUNER,” each paired with corresponding national flags, against a blurred European map — indicating the linguistic and ethnic variations of the term across regions. The video then presents a historical migration map showing routes across Europe from “before 650” to “ca. 1700,” with a key note emphasizing “One single migration,” framing the narrative around a unified historical origin.

**[Event 3: Scholarly Analysis and Visual Commentary]**  
A man in a dark jacket speaks and gestures, then turns to a whiteboard to draw a circle with a line through it — a symbolic representation likely indicating exclusion or redefinition. The scene shifts to a man in a dark suit writing on a whiteboard, discussing theories about the medieval origins of certain groups in the Adriatic coastal areas. This is followed by a topographical map of the Balkans and Adriatic region, with a red circle and arrow highlighting the coastal zones — visually reinforcing the geographical focus of the scholarly discussion.

**[Event 4: Satirical Visual Interlude]**  
The video concludes with a humorous visual interlude: a person in a suit with a rat’s head, followed by the same person speaking into a microphone — serving as a satirical or metaphorical commentary on the preceding narration, possibly alluding to stereotypes, historical perceptions, or the “rat” metaphor for Roma communities.

The video combines symbolic imagery, historical mapping, scholarly analysis, and satirical visuals to explore the origins, migration, and cultural representation of Roma communities in medieval Europe.
```

**txt5**

```
[00:20:00-00:20:30 | episodic 30sec] **[Event 1: Title and Historical Visual Introduction]**  
The video opens with a black screen displaying the stylized title “THE DEVOURING CHAPTER VI,” followed by a vibrant pointillist painting of a late 19th to mid-20th century park scene, dated “Late XIX-Mid XX.” This sets a visual tone before transitioning into darker, historically charged imagery.

**[Event 2: Racial Classification and Pseudoscientific Text]**  
The scene shifts to black-and-white illustrations depicting three racially labeled human profiles — “IRISH IBERIAN,” “ANGLO-TEUTONIC,” and “NEGRO” — accompanied by racist pseudoscientific text claiming racial hierarchies and origins, establishing a foundation of historical bigotry.

**[Event 3: Anatomical Comparisons and Satirical Commentary]**  
The visuals transition to a page from an old book showing comparative anatomical sketches of human and primate skulls, with a text overlay at 00:20:15 humorously likening the imagery to a “wojak shitpost,” juxtaposing historical pseudoscience with modern internet satire.

**[Event 4: Historical Street Scene and Scholarly References]**  
The video moves to a colorized street scene from the late 1800s, depicting period architecture, pedestrians, and horse-drawn carriages, before cutting to a black-and-white portrait of Ernst Haeckel and the cover of Theodor Tetzner’s 1835 book *Geschichte der Zigeuner: Ihre Herkunft, Natur, und Art*. A text overlay highlights Tetzner’s dehumanizing description of Roma as “the excrement of humanity” and Robert Knox’s similarly derogatory characterization of them as “the refuse of the human race,” reinforcing the video’s thematic focus on historical racism and pseudoscientific classification.
```

**txt6**

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

**txt7**

```
[00:21:00-00:24:00 | episodic 3min] **[Event 1: Historical Roots of Romani Persecution]**  
The video opens with archival visuals—black-and-white footage of Romani people, 1880s illustrations, and portraits of military figures—to establish centuries of institutionalized marginalization in German-speaking territories. This sets the stage for state-sanctioned discrimination predating Nazi rule.

**[Event 2: Bismarck’s State-Building and Militarization]**  
Portraits and formal assembly scenes of Otto von Bismarck transition into images of uniformed men marching, symbolizing the early institutionalization of state control and militarized social order under unified Germany.

**[Event 3: Institutionalization of Anti-Romani Policies]**  
Photographs of uniformed officers, dehumanizing signage (“Zigeunergeschmeiss”), and confrontational scenes with officials illustrate how state surveillance and public stigma escalated into formal policy—culminating in the 1899 “Central Office for Gypsy Affairs” in Bavaria under Alfred Dillmann.

**[Event 4: Racial Categorization and Surveillance]**  
Archival footage, the *Zigeuner-Buch* (Gypsy Book), and official documents reveal bureaucratic enforcement of racial classification. The Nuremberg Laws (1935) are displayed with symbolic racial markers, codifying hierarchy and targeting Sinti and Roma alongside Jews.

**[Event 5: Gestapo Documentation and Camp Life]**  
Gestapo mugshots of Roma individuals (Ludwig Horvath, Helene Baranks Huber, Maria Bihari) are juxtaposed with images of Roma camps—wooden trailers, fire pits, horses, and wagons—highlighting forced displacement and institutionalized segregation under Nazi rule.

**[Event 6: Mass Mobilization and Deportation]**  
Public rallies, military parades, and scenes of people boarding trains underscore state mobilization. The 1942 deportation to Auschwitz-Birkenau is documented through striped uniforms, barbed wire, Zyklon B containers, and stripped belongings—visually conveying the scale of genocide.

**[Event 7: Contemporary Reflection and Historical Memory]**  
Modern-day communal gatherings contrast with dark thematic transitions—hooded figures, Mengele’s image, and concentration camp aerials—to evoke trauma and historical reckoning. A final photograph of displaced victims in a barren field powerfully encapsulates enduring suffering and loss.

The video traces a chronological arc from centuries of marginalization to state-sponsored racial categorization, institutionalized persecution, and mass extermination—culminating in a somber reflection on memory, identity, and historical accountability.
```

**txt8**

```
[00:27:00-00:27:30 | episodic 30sec] A man holds a young child while standing with two other children in a rural, possibly impoverished, setting; a meme overlay appears featuring a muscular figure with the text “I made it up” and “Source?”, followed by cuts to a woman hanging laundry, and two men hammering metal — one seated with a metal rod beside him — all under the DW-TV logo.

The scene transitions to a person in a blue jacket and pink shirt hammering a metal disc, then to a kitchen where two women prepare food, followed by a dining room where a woman serves food to a man. A close-up shows her smiling as the man eats, concluding with a shot of an orange and white cat staring intently at food in a transparent bowl.

The video then shifts to an emotional outdoor confrontation at night, where one woman yells while being embraced by another who looks on with concern. It cuts to a daytime protest in Czechia, with participants holding flags and signs — including one reading “anti-gypsy protest in Czechia” — before ending with silhouettes of people and vehicles in a dimly lit outdoor nighttime scene.
```

**txt9**

```
[video-level knowledge | semantic] (Video, begins with, title card reading GYPSIES)
```

**txt10**

```
[video-level knowledge | semantic] (Video, begins with, title card reading GYPSIES)
```

**txt11**

```
[video-level knowledge | semantic] (text overlay, details, historical events)
```

**txt12**

```
[video-level knowledge | semantic] (Bonn, will expel, Gypsies)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 | ✓ | 00:00:05 | 00:00:00–00:00:10 | `0RxMZBLeqRI:visual:00000000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00000000.jpg` |
| img2 |  | 00:25:35 | 00:25:30–00:25:40 | `0RxMZBLeqRI:visual:00253000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00253000.jpg` |
| img3 |  | 00:11:15 | 00:11:10–00:11:20 | `0RxMZBLeqRI:visual:00111000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00111000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1** (cited)

```
[00:00:00-00:00:10 | video frame at 5.0s] A disclaimer appears on a black screen, explaining that the term “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s complicated history and clarifying that it is not intended as a slur. The screen then transitions to a map of the Balkan region, followed by a montage of internet memes and historical battle tables, including a humorous image labeled “POV: TITO INVENTING MACEDONIANS.” Overlaid audio discusses ethnic hatred in the Balkans, noting that certain groups are often targeted more than others.
```

**img2**

```
[00:25:30-00:25:40 | video frame at 1535.0s] The video segment displays historical footage and text overlays detailing Bulgaria’s policy toward Gypsies during the “Process of Revival” (1984–1985). Initially, text explains the government’s official stance to deny the existence of Gypsies in Bulgaria, leading to their concealment from public life and media. The visuals transition from archival images of a horse-drawn carriage to scenes of Gypsy mahalas — mobile homes — in a grassy field, with people and dogs present. A superimposed image of a man with a beard appears briefly. The footage then shifts to grainy black-and-white scenes of people moving through a settlement, followed by a close-up of a child. The final text overlay states that Gypsies who resisted name changes were sometimes separated from families and relocated; it notes that by 1985, nearly all Gypsies had adopted Bulgarian names, citing a figure of 400,000 Muslim Gypsies affected. The segment is presented in black and white, with logos for “PATHE” and “HISTORY” visible in the corners.
```

**img3**

```
[00:11:10-00:11:20 | video frame at 675.0s] An animated character stands in front of a scenic view of Istanbul, featuring the Hagia Sophia and surrounding mosques at sunset. The scene transitions to a map highlighting the Balkans and Eastern Europe, with flags of Serbia, Romania, Bulgaria, and Greece appearing sequentially over the region. The final frame is a historical illustration depicting a Roma settlement, showing people and animals around simple huts.
```
