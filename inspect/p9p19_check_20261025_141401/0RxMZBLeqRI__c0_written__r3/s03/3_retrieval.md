# Section 3 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:24:39): `{'video_id': '0RxMZBLeqRI', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 20, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 6.48}`
- image request (2026-10-25 14:24:42): `{'video_id': '0RxMZBLeqRI', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 0.84}`
- L1 filter LLM call: prompt 11286 tokens, output 74 tokens, 5.4 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 10min | 00:20:00–00:30:00 | 1 / 0.04918 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10min_2` |
| txt2 |  | worldmm-episodic | 3min | 00:21:00–00:24:00 | 2 / 0.032787 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:3min_7` |
| txt3 |  | worldmm-episodic | 30sec | 00:23:00–00:23:30 | 3 / 0.032787 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_46` |
| txt4 | ✓ | worldmm-episodic | 10sec | 00:22:00–00:22:10 | 4 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_132` |
| txt5 | ✓ | worldmm-episodic | 30sec | 00:22:00–00:22:30 | 5 / 0.016129 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_44` |
| txt6 | ✓ | worldmm-episodic | 10sec | 00:22:10–00:22:20 | 6 / 0.015873 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_133` |
| txt7 | ✓ | worldmm-episodic | 10sec | 00:23:20–00:23:30 | 7 / 0.016129 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_140` |
| txt8 | ✓ | worldmm-episodic | 30sec | 00:23:30–00:24:00 | 8 / 0.015873 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_47` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_239` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_284` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_303` |
| txt12 | ✓ | worldmm-semantic | — | no timestamp | 4 / 0.016129 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_261` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:20:00-00:30:00 | episodic 10min] **[Event 1: Historical Roots of Romani Persecution]**  
The video opens with archival imagery—black-and-white footage, 19th-century illustrations, and portraits of military figures—to establish centuries of institutionalized marginalization of Romani people in German-speaking territories. This visual foundation underscores that state-sanctioned discrimination predates Nazi rule, laying the groundwork for later systemic persecution.

**[Event 2: Bismarck’s State-Building and Militarization]**  
Portraits and formal assembly scenes of Otto von Bismarck transition into images of uniformed men marching, symbolizing the early institutionalization of state control and militarized social order under unified Germany. This sets the stage for how state power would later be weaponized against minority groups.

**[Event 3: Institutionalization of Anti-Romani Policies]**  
Photographs of uniformed officers, dehumanizing signage (“Zigeunergeschmeiss”), and confrontational scenes with officials illustrate how state surveillance and public stigma escalated into formal policy. The 1899 creation of the “Central Office for Gypsy Affairs” in Bavaria under Alfred Dillmann marks a pivotal moment in bureaucratic racialization.

**[Event 4: Racial Categorization and Surveillance]**  
Archival footage, the *Zigeuner-Buch* (Gypsy Book), and official documents reveal the bureaucratic enforcement of racial classification. The Nuremberg Laws (1935) are displayed with symbolic racial markers, codifying hierarchy and explicitly targeting Sinti and Roma alongside Jews.

**[Event 5: Gestapo Documentation and Camp Life]**  
Gestapo mugshots of Roma individuals (Ludwig Horvath, Helene Baranks Huber, Maria Bihari) are juxtaposed with images of Roma camps—wooden trailers, fire pits, horses, and wagons—highlighting forced displacement and institutionalized segregation under Nazi rule.

**[Event 6: Mass Mobilization and Deportation]**  
Public rallies, military parades, and scenes of people boarding trains underscore state mobilization. The 1942 deportation to Auschwitz-Birkenau is documented through striped uniforms, barbed wire, Zyklon B containers, and stripped belongings—visually conveying the scale of genocide.

**[Event 7: Contemporary Reflection and Historical Memory]**  
Modern-day communal gatherings contrast with dark thematic transitions—hooded figures, Mengele’s image, and concentration camp aerials—to evoke trauma and historical reckoning. A final photograph of displaced victims in a barren field powerfully encapsulates enduring suffering and loss.

---

**[Event 1: Historical Repression and Mass Suffering]**  
The video opens with black-and-white archival footage from 1945, depicting soldiers atop a damaged building and civilians being escorted by uniformed officers, transitioning into mass marches toward concentration camps—visually conveying systemic repression under authoritarian regimes. Text overlays emphasize the scale of death (500,000–1,500,000), reinforcing the human cost. The “British Pathé” logo underscores the documentary tone, while the final title “Communism, Chapter VII” frames the footage as part of a broader ideological narrative.

**[Event 2: State Control and Judicial Mechanisms]**  
The scene shifts to a formal indoor conference and courtroom setting, where men in suits deliberate and a uniformed man addresses seated individuals under military guard. This suggests state-controlled legal or administrative processes, possibly trials or interrogations, highlighting mechanisms of authoritarian governance through institutionalized power.

**[Event 3: Symbolic Transition and Ideological Reflection]**  
An animated sequence introduces a stylized female figure over a sepia street, zooming out to reveal a clock and the word “COMMUNISM,” followed by an animated bald man clasping hands before a red-haired figure—symbolizing ideological confrontation or historical reckoning. The abrupt tonal shift from grim footage to stylized animation signals a move from documentation to interpretation.

**[Event 4: Bulgaria’s Erasure of Gypsy Identity]**  
Footage of rural Bulgaria during the “Process of Revival” (1984–1985) shows horse-drawn carts, mahalas, and grainy settlements, overlaid with text detailing state policies forcing Gypsies to adopt Bulgarian names and relocate. Resistance led to family separation; by 1985, nearly all 400,000 Muslim Gypsies had assimilated. Logos for “PATHE” and “HISTORY” appear, grounding the narrative in archival context.

**[Event 5: Cultural Continuity Amid Assimilation]**  
Color footage of men with oxen carts and a violinist in an outdoor gathering contrasts with earlier repression, suggesting cultural endurance despite state-imposed erasure. The scene ends with a surreal anime-style character superimposed over urban architecture, introducing a symbolic layer that may represent memory or narrative rupture.

**[Event 6: Personal Testimony and Political Legacy]**  
The video blends personal imagery—a bride, a woman in a red headscarf speaking to children—with archival shots of Nicolae Ceaușescu and his wife. A poster of an anime character overlaid with a 2007 Romanian headline (“Government acknowledges responsibility for anti-Romani pogroms”) marks institutional reckoning with historical injustice, grounding the narrative in contemporary accountability.

**[Event 7: Tension, Symbolism, and Resilience]**  
A muscular superhero confronts a bald man in a suit, bleeding and restrained—symbolizing ideological or physical conflict. A young girl faces a chaotic crowd with a looming cartoon figure, evoking oppression. The final frame of a cuffed individual in a vibrant setting implies imprisonment amid surreal or societal complexity.

**[Event 8: Collective Protest and Emotional Catharsis]**  
An animated *Simpsons* crowd marches with torches, conveying collective anger and unity. The camera pans across determined faces, emphasizing emotional intensity and organized resistance.

**[Event 9: Melancholy and Resilience in Rural Decay]**  
Homer Simpson gazes out a window, setting a somber tone. A crime scene tape frames a tense discussion, followed by a man at a piano with the caption “I’m gonna pretend I didn’t see that,” suggesting denial. The video closes with a man holding a child in a dilapidated rural setting—evoking care amid loss and resilience in forgotten places.

---

**[Event 1: Marginalized Lives and Systemic Struggle]**  
The video opens with rural and urban scenes of poverty — children in dilapidated settings, a man shoveling dirt, and a woman sorting documents — juxtaposed with archival footage of concentration camps and wartime migration, establishing a historical context of displacement and state control. A meme overlay mocking “source” and “I made it up” contrasts with real-world labor and surveillance, suggesting media distortion of systemic hardship.

**[Event 2: Forced Repatriation and Institutional Repression]**  
A formal announcement declares the expulsion of thousands of Romanians and Roma from Germany under asylum laws, framed by stern figures and a “EUROPA” truck. Archival labor footage and animated corruption charts reinforce institutionalized exclusion. A bald man labeled “Illegal work” and state confiscation of savings depict state-sanctioned punishment for economic success, while a girl peering from behind a curtain silently witnesses systemic injustice.

**[Event 3: Cultural Resilience Amid Crisis]**  
Despite institutional and economic oppression, the video highlights moments of human agency: a woman finding a job with an IT giant, a Roma woman asserting identity at a rally (“I am also a Roma”), and an animated character symbolizing cultural endurance. A dancing boy in front of a satellite-dish-covered building offers a humanizing counterpoint to the bleakness, framed by France 24’s journalistic lens.

**[Event 4: Visual and Political Juxtaposition]**  
The narrative blends realism with surrealism — from Smurf animations under a full moon to weather maps and pixelated visa denials — to critique power structures. A far-right rally in Hungary and cluttered urban decay underscore fear and neglect within marginalized communities. The final animated overlay on a real-world archway symbolizes cultural resistance persisting within modern urban frameworks.

**[Conclusion]**  
Through layered visuals — archival, documentary, and animated — the video constructs a narrative of systemic marginalization, state repression, and quiet resilience. It critiques institutional exclusion, economic collapse, and cultural erasure while highlighting moments of resistance, identity assertion, and human dignity amid adversity.
```

**txt2**

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

**txt3**

```
[00:23:00-00:23:30 | episodic 30sec] **[Event 1: Intimate Wedding Transition to Historical Ceremony]**  
The segment opens with a black-and-white close-up of a bride and groom sharing an intimate moment, transitioning to a wide shot of a large, crowded gathering — suggesting a celebratory public event. The scene then shifts to a formal assembly in a grand hall, marked by a large eagle emblem and the year “1938” superimposed, indicating a politically charged or state-sponsored ceremony. The segment concludes with a focus on a handwritten letter dated March 2, 1942, from the head of the Sicherheitspolizei und des SD, detailing policy implementation — underscoring the institutionalization of state-directed actions during this period. The History Channel logo is visible throughout.

**[Event 2: Public Rally and Military Mobilization]**  
The video opens with a wide shot of a densely packed crowd waving flags, indicating a public rally or mass demonstration. The scene cuts to a man speaking at a podium, flanked by uniformed individuals, suggesting a formal political address or state ceremony. It then transitions to color footage of soldiers marching along a dirt road, some smiling — a moment of apparent camaraderie or morale. The scene returns to black and white, showing people boarding or standing near a long train at a station, with a military officer present — implying mass mobilization or deportation. The final frames show a young girl peering out from a narrow opening in a wooden door, her expression conveying fear or concern — hinting at personal trauma amid broader systemic events.

**[Event 3: Prisoner Deportation and Auschwitz-Birkenau Documentation]**  
The segment begins with a woman in a headscarf looking out from behind a wooden door — a moment of quiet observation or dread. The scene transitions to a group of men in striped prison uniforms standing in formation, with “1942” superimposed, indicating the timeline of mass incarceration. The location is identified as “Auschwitz-Birkenau,” where prisoners — including women and children — are shown walking along a barbed-wire fence. The footage then displays containers labeled “GIFTGAS ZYKLON B,” followed by piles of clothing and personal belongings — documenting the systematic stripping and extermination process. The imagery collectively underscores the scale and brutality of the Holocaust infrastructure.
```

**txt4** (cited)

```
[00:22:00-00:22:10 | episodic 10sec] The video displays a historical Nazi-era document titled "Die Nürnberger Gesetze" (The Nuremberg Laws), which categorizes individuals based on racial and ethnic classifications, including "Deutschblütiger" (German-blooded), "Mischling 2. Grades" (Mischling of the second degree), "Mischling 1. Grades" (Mischling of the first degree), and "Jude" (Jew), with corresponding symbols and annotations. The scene then transitions to a series of black-and-white mugshots from the Gestapo, showing a man named Horvath, Ludwig, Leitani, born January 12, 1889, identified as a "Zigeuner" (Gypsy), followed by a woman named Huber, Helene Baranks, born in 1874, also identified as a "Zigeunerin" (Gypsy woman). The images are presented in a straightforward, archival style, with no accompanying audio or narration.
```

**txt5** (cited)

```
[00:22:00-00:22:30 | episodic 30sec] **[Event 1: Display of Nazi Racial Classification Document]**  
The video opens with a historical document titled *Die Nürnberger Gesetze* (The Nuremberg Laws), which systematically categorizes individuals into racial and ethnic groups — including “Deutschblütiger,” “Mischling 2. Grades,” “Mischling 1. Grades,” and “Jude” — each accompanied by symbolic markings. This visual establishes the legal framework of racial hierarchy enforced by the Nazi regime.

**[Event 2: Gestapo Mugshots of Roma Individuals]**  
The scene transitions to black-and-white Gestapo mugshots of two Roma individuals: Ludwig Horvath, born January 12, 1889, labeled “Zigeuner”; and Helene Baranks Huber, born in 1874, labeled “Zigeunerin.” The images are presented in a stark, archival style, underscoring state documentation and persecution under Nazi racial policy.

**[Event 3: Roma Child in Camp Setting]**  
A black-and-white mugshot of Maria Bihari, a Roma girl born November 9, 1935, is shown in three angles (frontal, three-quarter, profile). The scene then shifts to an outdoor Roma camp featuring wooden trailers, a central fire pit, gathered adults and children, and laundry hanging nearby. Later, horses and wagons are shown with people interacting with them, concluding with two men guiding a horse — one holding a whip — reinforcing the lived reality of Roma in forced or institutionalized settings.

**[Event 4: Historical Footage and Modern Overlay]**  
The video begins with a black-and-white scene of people near a large animal, followed by a title card reading “1925” over a dark background. It then shows people looking through a wire fence, suggesting confinement. The footage transitions to an exterior shot of a weathered train car on a railway track. The segment ends with a modern color image of a bald man in a gray suit gesturing, overlaid with the text “Security reasons,” while the History Channel logo remains visible — implying a contemporary editorial framing of historical material.
```

**txt6** (cited)

```
[00:22:10-00:22:20 | episodic 10sec] The video segment begins with a black-and-white mugshot of a young girl, Maria Bihari, born on November 9, 1935, identified as a Roma (Zigeunerin). The image shows three views of the girl: frontal, three-quarter, and profile. The scene then transitions to an outdoor camp setting with several wooden trailers or wagons. A group of people, including adults and children, are gathered around a central fire pit, with some standing and others seated on the ground. In the background, more trailers are visible, and laundry can be seen hanging nearby. The scene shifts again to show horses and wagons in the same camp area, with people interacting with the animals and equipment. The final frame shows two men guiding a horse, with one man holding a stick or whip.
```

**txt7** (cited)

```
[00:23:20-00:23:30 | episodic 10sec] A black-and-white historical segment begins with a woman in a headscarf looking out from behind a wooden door. The scene transitions to a group of men in striped prison uniforms standing in formation, with the year "1942" superimposed. The location is identified as "Auschwitz-Birkenau" as prisoners, including women and children, are shown walking along a barbed-wire fence. The footage then shows containers labeled "GIFTGAS ZYKLON B," followed by a shot of piles of clothing and personal belongings.
```

**txt8** (cited)

```
[00:23:30-00:24:00 | episodic 30sec] **[Event 1: Present-day outdoor communal gathering]**  
A group of people in heavy clothing and head coverings are gathered in a rugged, outdoor settlement, suggesting cold or harsh conditions. One bearded man in a hat is seated and engaged in conversation with others. The camera pans across the scene, revealing additional individuals near tents and makeshift shelters, indicating a temporary, communal living situation. The atmosphere is active and interactive, with visible social engagement among the group.

**[Event 2: Historical montage with dark thematic transition]**  
The video abruptly shifts to a person in a dark hooded garment holding a knife, followed by a still image of Josef Mengele with his name displayed. The scene transitions to black-and-white footage of medical personnel attending to patients in a hospital-like setting. The final frames show a wide, desolate view of a concentration camp, with rows of brick buildings flanking a central road leading to a gatehouse, as a solitary figure walks down the path — evoking themes of suffering, institutional control, and historical atrocity.

**[Event 3: Aerial view of former concentration camp]**  
An aerial shot reveals a large, somber complex of brick buildings with red-tiled roofs, arranged symmetrically along a central pathway. A small gatehouse stands at the end of the path. The overcast sky and bare trees create a bleak, gray atmosphere. The camera pans left, revealing the full scale of the sprawling compound, consistent with a former concentration camp or institutional facility.

**[Event 4: Historical photograph of displaced victims]**  
The video cuts to a black-and-white historical photograph showing a group of men, women, and children sitting on the ground in a barren field. Their worn clothing and exhausted expressions convey despair. A man stands nearby near a simple fence, overseeing them. The image powerfully evokes displacement, suffering, and the aftermath of historical atrocity — likely depicting refugees or victims of genocide or persecution.
```

**txt9**

```
[video-level knowledge | semantic] (Vlad Cepish, leads, gypsy army)
```

**txt10**

```
[video-level knowledge | semantic] (final text overlay, states, Gypsies were relocated)
```

**txt11**

```
[video-level knowledge | semantic] (black-and-white historical footage, shows, bustling marketplace)
```

**txt12** (cited)

```
[video-level knowledge | semantic] (Horvath, Ludwig Leitani, is a Zigeuner, born on January 12, 1889, and appears in Gestapo mugshots)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:22:05 | 00:22:00–00:22:10 | `0RxMZBLeqRI:visual:00220000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00220000.jpg` |
| img2 |  | 00:21:55 | 00:21:50–00:22:00 | `0RxMZBLeqRI:visual:00215000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00215000.jpg` |
| img3 |  | 00:22:35 | 00:22:30–00:22:40 | `0RxMZBLeqRI:visual:00223000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00223000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:22:00-00:22:10 | video frame at 1325.0s] The video displays a historical Nazi-era document titled "Die Nürnberger Gesetze" (The Nuremberg Laws), which categorizes individuals based on racial and ethnic classifications, including "Deutschblütiger" (German-blooded), "Mischling 2. Grades" (Mischling of the second degree), "Mischling 1. Grades" (Mischling of the first degree), and "Jude" (Jew), with corresponding symbols and annotations. The scene then transitions to a series of black-and-white mugshots from the Gestapo, showing a man named Horvath, Ludwig, Leitani, born January 12, 1889, identified as a "Zigeuner" (Gypsy), followed by a woman named Huber, Helene Baranks, born in 1874, also identified as a "Zigeunerin" (Gypsy woman). The images are presented in a straightforward, archival style, with no accompanying audio or narration.
```

**img2**

```
[00:21:50-00:22:00 | video frame at 1315.0s] The video segment begins with a close-up of a historical document, which appears to be a typed letter or official paper, displayed against a blurred background of a black-and-white street scene with people. The document is in German and features a stamp at the bottom. The view then transitions to show the document being flipped to reveal another page, which also contains German text and a handwritten notation.

The scene then shifts to a black-and-white historical photograph depicting a line of people, many wrapped in blankets or traditional clothing, standing outside a brick building. Two uniformed soldiers are visible, one standing prominently in the foreground and another near a bicycle on the right side.

Finally, the video displays a chart titled "Die Nürnberger Gesetze" (The Nuremberg Laws), which categorizes individuals based on racial criteria using symbols and text, including labels such as "Deutschblütiger," "Mischling 2. Grades," "Mischling 1. Grades," and "Jude." The chart uses circles with crosses and black dots to indicate different classifications, along with explanatory text in German.
```

**img3**

```
[00:22:30-00:22:40 | video frame at 1355.0s] A black-and-white family photograph from 1927 shows seven people standing in front of a wooden house. The scene transitions to a vintage identification card with handwritten details and a portrait of a man in a suit. The video then shifts to a pixelated video game interface where a character hands over an ID card, followed by a close-up of a visa and identity record for "Ryovski Forsing."
```
