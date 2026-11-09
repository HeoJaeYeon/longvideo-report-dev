# Section 3 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:17:24): `{'video_id': '0RxMZBLeqRI', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 23, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 7.43}`
- image request (2026-10-25 14:17:27): `{'video_id': '0RxMZBLeqRI', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 0.89}`
- L1 filter LLM call: prompt 15486 tokens, output 69 tokens, 6.3 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 30sec | 00:00:30–00:01:00 | 1 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_1` |
| txt2 | ✓ | worldmm-episodic | 10sec | 00:00:50–00:01:00 | 2 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_5` |
| txt3 | ✓ | worldmm-episodic | 10sec | 00:00:30–00:00:40 | 3 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_3` |
| txt4 |  | worldmm-episodic | 30sec | 00:00:00–00:00:30 | 4 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_0` |
| txt5 | ✓ | worldmm-episodic | 10min | 00:00:00–00:10:00 | 5 / 0.032787 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10min_0` |
| txt6 |  | worldmm-episodic | 30sec | 00:20:30–00:21:00 | 6 / 0.016129 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_41` |
| txt7 |  | worldmm-episodic | 30sec | 00:20:00–00:20:30 | 7 / 0.015873 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_40` |
| txt8 |  | worldmm-episodic | 30sec | 00:14:30–00:15:00 | 8 / 0.015873 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_29` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_144` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_318` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_34` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016129 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_143` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:00:30-00:01:00 | episodic 30sec] **[Event 1: Scientific Experimentation and Historical Stigmatization]**  
A man in a yellow lab coat carefully transfers liquid using a pipette, symbolizing scientific precision or experimentation. The scene abruptly shifts to a black-and-white image of a man in a lab coat marked with a red “X,” suggesting rejection or exclusion from scientific or societal norms. This is followed by a man in a red sweater gesturing before a group in traditional clothing—some dancing—implying cultural expression or performance. The montage continues with black-and-white imagery: a band playing traditional instruments and a family with children holding instruments seated before a wagon, evoking heritage and communal life. These images transition into a historical montage showing diverse groups—families, children, and gatherings in front of tents—culminating in the word “UNWANTED” superimposed over the final frame, accompanied by a voiceover explaining how the vast majority have been historically stigmatized and labeled as unwanted nuisances.

**[Event 2: Fantasy Conflict and Societal Stereotypes]**  
The video transitions to a Minecraft gameplay scene where a player mines, symbolizing labor or resource extraction. It then cuts to a menacing, horned humanoid character declaring “Your money or your life,” evoking themes of coercion or economic exploitation. The scene shifts to a dark fantasy setting with robed figures in combat, followed by a surreal image of a black, hooded figure with glowing dollar signs, suggesting corruption or the commodification of power. The tone shifts to vibrancy with scenes of dance—on stage and in public squares—representing joy, freedom, or resistance. The video concludes with a somber black-and-white photograph of displaced people sitting on the ground, underscoring suffering and loss. Throughout, a voiceover traces the tragic history behind stereotypes of thieves and black magic casters, framing them as products of societal fear and misunderstanding.
```

**txt2** (cited)

```
[00:00:50-00:01:00 | episodic 10sec] The video transitions through various scenes: it begins with a Minecraft gameplay shot showing a player mining, then cuts to a close-up of a menacing, horned humanoid character from a video game declaring, "Your money or your life." The scene shifts to a dark, fantasy setting with robed figures engaged in combat, followed by a surreal image of a black, hooded figure with glowing dollar signs. The video then shows vibrant dance performances, both on a stage and in a public square, before concluding with a somber black-and-white photograph of a large group of displaced people sitting on the ground. Throughout, a voiceover discusses uncovering the complex and tragic history behind stereotypes of thieves and black magic casters.
```

**txt3** (cited)

```
[00:00:30-00:00:40 | episodic 10sec] A man in a yellow lab coat carefully uses a pipette to transfer liquid into a beaker. The scene then transitions to a black-and-white image of a man in a lab coat, marked with a large red "X". Next, a man in a red sweater is shown gesturing in front of a group of people in traditional clothing, some dancing. The video then cuts to a black-and-white photo of a band playing traditional instruments, and finally to a black-and-white photo of a family, including children holding musical instruments, seated in front of a wagon.
```

**txt4**

```
[00:00:00-00:00:30 | episodic 30sec] **[Event 1: Introduction and Context Setting]**  
The video opens with a disclaimer clarifying that “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s contested history and affirming its non-slandrous intent. The screen transitions to a map of the Balkans, followed by a montage of internet memes and historical battle tables — including a satirical image labeled “POV: TITO INVENTING MACEDONIANS” — while audio commentary underscores the entrenched ethnic hatred in the region, highlighting how certain groups are disproportionately targeted.

**[Event 2: Visual Montage and Narrated Commentary on Roma Perception]**  
A text overlay introduces the historical and cultural presence of the Roma in the Balkans, while visuals show a person walking past a trash can, then turning away — possibly symbolizing marginalization. The scene cuts to a man in a white suit and red tie seated beside a woman in a patterned top, followed by a shirtless man shouting outdoors — suggesting social tension or protest. A bearded man speaks in front of a lit background, likely delivering commentary or narration. The segment concludes with a still image of Barack Obama superimposed over dilapidated buildings, overlaid with the text “POREKLOM SAM CIGANIN” (“I am a Gypsy by origin”), fading to black — reinforcing the theme of identity, erasure, and societal perception. Throughout, narration emphasizes the Roma’s complex and often negative social portrayal.

**[Event 3: Historical and Cultural Representation of the Roma]**  
The video begins with a title card reading “GYPSIES,” followed by sepia-toned historical photographs of Roma families in traditional attire — some gathered around caravans, others posing formally — illustrating their long-standing presence. The scene transitions to a modern-day street parade featuring participants in colorful traditional clothing and contemporary attire, marching with flags including the Roma flag (red wheel on green), alongside Ukrainian and EU flags. Narration affirms the Roma’s integral role in Balkan culture and history, while acknowledging the lack of public knowledge due to generational stigma, prejudice, and insufficient scholarly research.
```

**txt5** (cited)

```
[00:00:00-00:10:00 | episodic 10min] **[Event 1: Introduction and Context Setting]**  
The video opens with a disclaimer clarifying the use of “Gypsy” as a non-slandrous term for Roma/Romani, followed by a map of the Balkans and a montage of memes and historical battle tables — including a satirical “TITO INVENTING MACEDONIANS” image — underscoring entrenched ethnic hatred in the region. This sets a tone of historical and cultural complexity, framing Roma identity within a landscape of political manipulation, ethnic erasure, and systemic marginalization.

**[Event 2: Visual Montage and Narrated Commentary on Roma Perception]**  
A text overlay introduces Roma presence in the Balkans, juxtaposed with visuals of marginalization (a person turning away from a trash can) and social tension (shirtless man shouting, bearded speaker). The segment ends with a still of Obama over dilapidated buildings, overlaid with “POREKLOM SAM CIGANIN,” fading to black — reinforcing identity erasure and societal stigma. The imagery deliberately contrasts modern political symbolism with the lived reality of Roma exclusion, highlighting how identity is weaponized and erased.

**[Event 3: Historical and Cultural Representation of the Roma]**  
Sepia-toned historical photos of Roma families in traditional attire transition to a modern parade with Roma, Ukrainian, and EU flags — affirming their cultural role. Narration acknowledges their historical invisibility due to stigma and lack of scholarly attention. This segment counters the earlier depictions of erasure by asserting Roma agency and cultural continuity, visually and narratively grounding their presence as both ancient and contemporary.

**[Event 1: Scientific Experimentation and Historical Stigmatization]**  
A lab-coated figure transfers liquid, symbolizing scientific precision, cuts to a black-and-white “X”-marked scientist — suggesting exclusion. Montage of cultural heritage (band, family with instruments) transitions to “UNWANTED” superimposed over historical scenes — highlighting systemic stigmatization. The juxtaposition of scientific imagery with exclusionary symbols critiques how Roma have been studied, categorized, and dismissed as “other” — even within academic frameworks.

**[Event 2: Fantasy Conflict and Societal Stereotypes]**  
Minecraft mining scenes transition to a horned figure declaring “Your money or your life,” followed by dark fantasy combat and a hooded figure with dollar signs — symbolizing corruption. Joyful dance scenes contrast with black-and-white images of displaced people — framing stereotypes as products of fear and misunderstanding. The surreal, game-based visuals serve as allegory for how Roma are often reduced to archetypes of “danger” or “criminality,” despite their rich cultural contributions.

**[Event 1: Introduction and Origin Mystery]**  
A title card asks “Who are the Gypsies?” followed by a map animation tracing migration from Middle East/South Asia to Europe. A 3D figure with a question mark symbolizes the enduring mystery of their origins since the 13th century. The video opens with a historical and existential question, positioning Roma identity as both enigmatic and deeply rooted in centuries of movement and adaptation.

**[Event 2: Historical Context and Early Misidentification]**  
A 13th-century map anchors Roma presence. A “VS” graphic depicts Seljuk Turks vs. Byzantine Empire — narrated as geopolitical tensions shaping early misidentification of Roma as Turks. The segment frames Roma not as a distinct ethnic group but as a product of historical misreading — caught between empires and labeled by the victors.

**[Event 3: Arrival and Misidentification]**  
A man in a fez walks along migration arrows. Historical battle scenes reinforce Christian-Muslim conflict. Narration explains Roma were first mistaken for Seljuk Turks by Byzantines — embedding their identity in historical geopolitics. The visual narrative reinforces how Roma were not “invented” but rather misclassified — their arrival coinciding with the collapse of empires and the rise of new identities.

**[Event 1: Medieval Battle Depiction and Historical Framing]**  
A medieval battle painting with knights and flags transitions to “SARACEN = HEATHENS” — framing conflict through polemical lens. The video uses religious and cultural binaries to illustrate how Roma were categorized as “foreign” and “dangerous,” reinforcing the idea that their presence was always a threat to the dominant order.

**[Event 2: Modern Commentary and Symbolic Representation]**  
A young person looks at camera, followed by two men at a laptop with flags — suggesting commentary. A cartoon Greek figure screams “ATSINGANI” — a slur against non-Christians — implying political critique. The segment uses satire and caricature to expose how Roma are still targeted through language and ideology — even in modern times.

**[Event 3: Battle in Middle Eastern City and Google Translate Interlude]**  
A chaotic Crusader battle scene in a Middle Eastern city transitions to a “DON’T TOUCH” Google Translate warning — cautioning against misinterpretation. Ends with a bearded man’s face shifting from awe to distress — symbolizing human cost. The video critiques how historical narratives are often mistranslated or misunderstood, and how this misinterpretation continues to harm Roma identity.

**[Event 1: Introduction and Cultural Identity Framing]**  
A bearded man gazes upward against rocky backdrop, setting reflective tone. Two young men outdoors with “Atsingani” overlay transition to an anime girl in traditional attire gesturing over Balkan map — anchoring cultural context. The video opens with a meditative, almost spiritual tone, inviting viewers to consider Roma identity as something both ancient and deeply personal.

**[Event 2: Linguistic and Historical Context]**  
Words “CIGANI,” “CIGÁNYOK,” “TIGANI,” “ZIGEUNER” appear with flags — showing linguistic variations. Migration map from “before 650” to “ca. 1700” emphasizes “One single migration” — framing unified origin. The segment emphasizes the linguistic diversity of Roma while asserting their shared historical roots — a unifying narrative amid fragmentation.

**[Event 3: Scholarly Analysis and Visual Commentary]**  
A man draws a circle with line through it — symbolizing exclusion. Scholarly discussion on medieval Adriatic origins is paired with a topographical map highlighting coastal zones — reinforcing geographical focus. The video uses academic imagery to ground its claims in scholarly research, while visually reinforcing how Roma were excluded from the historical record.

**[Event 4: Satirical Visual Interlude]**  
A rat-headed figure in a suit speaks into mic — satirical commentary. Meme juxtapositions (“AVERAGE GREEK BE LIKE:”) and surreal desert scenes culminate in a green upward-trending graph — symbolizing absurd success or growth. Ends with “GYPSY = EGYPTIAN” and a Europe-North Africa map — closing on semantic and geographic ambiguity. The segment uses humor and absurdity to critique how Roma are constantly redefined — often as “Egyptian,” “Turkish,” or “foreign” — despite their complex, multi-layered identity.

**[Event 1: Symbolic National Imagery & Cultural Juxtaposition]**  
The video opens with symbolic overlays of national flags — North Macedonia (“GJUPCI”), Spain (“GITANO”), and Greece (“Γύφτος”) — paired with a map of Europe, suggesting cultural or historical ties across the Balkans and Mediterranean. A dramatic fall of a man in a hanging chair, titled “THE PHARAOH’S CURSE,” sets a tone of impending disruption or mythic danger. The scene shifts to a surreal, smoke-filled room and a bearded man behind a watermelon, reinforcing the video’s absurdist, dreamlike aesthetic. This segment frames Roma as a thread connecting disparate nations — both mythic and real.

**[Event 2: Thematic Contrasts & Surreal Transitions]**  
A gameplay interlude featuring Mario in a desert level introduces a playful, game-based break before a sharp tonal pivot: a chemistry lecture with chalkboard diagrams and the word “Chiral,” followed by a split-screen of a tanker truck and a car, overlaid with the humorous text “WHOOPS! Can't show that in a Christian manga!” — a self-referential nod to censorship. The segment ends with a blurry blue image resolving into “1760,” anchoring the narrative in a specific historical moment. The surreal transitions serve as both comedic relief and thematic device — highlighting how history is often distorted or censored.

**[Event 3: Historical & Cultural Layering]**  
The video transitions through a surreal montage: a cartoon character in a fur hat appears over shifting backdrops — Dutch canals, Minecraft villages, European bridges — before settling into a pub scene with a quill-writing hand. This is followed by a newspaper clipping (“Hannoversches Tageblatt, 1865”), a topographical map, and a man with tattoos shouting dramatically before a map — suggesting a historical or political commentary. The tone shifts again to a pixelated Mario scene, then to SpongeBob falling in a bathroom, juxtaposed with a screaming man in glasses — blending absurdity with cultural reference. The video uses pop culture and historical imagery to blur the lines between past and present, reality and fantasy.

**[Event 4: National Identity & Symbolic Exchange]**  
The video returns to national symbolism: Germany’s flag over its map, then Greece’s, before transitioning to Carthage with a Simpsons character, hinting at historical or satirical narrative. Religious imagery follows — a cartoon character with a Bible, animal sacrifice paintings, and a stark desert — evoking spiritual or historical desolation. The tone shifts to a grounded human moment: a smiling man in a car, an anime girl superimposed over a historical painting, ending with a reverent shot of an empty cathedral — blending modernity with ancient themes. This
```

**txt6**

```
[00:20:30-00:21:00 | episodic 30sec] **[Event 1: Evolutionary and Biblical Imagery as Framing Devices]**  
The video opens with a sepia-toned portrait of Charles Darwin, overlaid with his name, followed by a classic illustration tracing human evolution from apelike ancestors to modern humans — visually framing the theme of biological progression. The scene then shifts to an aged, vintage aesthetic, showing an open book labeled “GENESIS,” accompanied by imagery of Adam and Eve and God creating the world, suggesting a contrast or tension between scientific evolution and religious creation narratives.

**[Event 2: Darwin’s Racist Remarks and Historical Context]**  
A black-and-white illustration of Darwin seated in a chair is shown, with a text overlay quoting him as referring to Jews and Gypsies as “not culturally advanced” compared to “territorially settled” peoples — directly linking his scientific legacy to racial prejudice. The scene transitions to archival black-and-white footage of a person pushing a wheeled cart along a cobblestone street, with the History Channel logo visible, indicating the segment’s documentary context and grounding the content in historical presentation.

**[Event 3: Nazi Racial Laws and Systematic Persecution of Roma]**  
The video begins with a black-and-white shot of a covered wagon on a dirt road, symbolizing migration or displacement. It then cuts to a static image of “Die Nürnberger Gesetze,” a Nazi racial law document displaying a chart categorizing people by race and “impurity,” with symbols indicating degrees of Jewish ancestry — illustrating the institutionalization of racial hierarchy. The scene transitions to a black-and-white outdoor shot of people, including children, gathered near wooden barracks in a wooded area, evoking the conditions of forced settlement or concentration. The final frame overlays text stating that when the Nazis came to power in 1933, anti-Roma laws in German-speaking lands had already existed for centuries, and persecution intensified immediately — highlighting the historical continuity of systemic discrimination.
```

**txt7**

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

**txt8**

```
[00:14:30-00:15:00 | episodic 30sec] **[Event 1: Historical Visuals and Symbolic Equations]**  
The video opens with a blurry historical painting featuring a figure in red headwear holding a child, transitioning to a close-up of an old Romanian document advertising the sale of slaves from Tiganesti, detailing men, women, and children. The scene shifts to a scenic stone church atop a pine forest, followed by a stark white screen displaying a person icon, which is visually equated to a pig. Three identical person icons appear aligned horizontally, suggesting a symbolic or statistical representation.

**[Event 2: Abstract Visual Equations]**  
A sequence of minimalist icon-based equations unfolds: three male figures equal a bull; a couple holding hands equals three wooden barrels; a female figure equals two copper pots. The sequence ends with a wheelchair accessibility symbol followed by an equals sign, implying an incomplete or pending equation.

**[Event 3: Symbolic Transition to Game Scene]**  
The wheelchair symbol is equated to a jar of honey, followed by a blank screen. A pregnant woman icon joins a child icon, then abruptly cuts to a video game scene where an armored character confronts the viewer, demanding payment or imprisonment for stolen goods — a stark shift from symbolic abstraction to narrative confrontation.
```

**txt9**

```
[video-level knowledge | semantic] (black-and-white illustration, shows, large dense crowd)
```

**txt10**

```
[video-level knowledge | semantic] (text overlay, details, historical events)
```

**txt11**

```
[video-level knowledge | semantic] (pixelated video game scene, features, Mario)
```

**txt12**

```
[video-level knowledge | semantic] (black-and-white illustration, shows, lone figure)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:11:55 | 00:11:50–00:12:00 | `0RxMZBLeqRI:visual:00115000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00115000.jpg` |
| img2 | ✓ | 00:01:45 | 00:01:40–00:01:50 | `0RxMZBLeqRI:visual:00014000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00014000.jpg` |
| img3 | ✓ | 00:01:55 | 00:01:50–00:02:00 | `0RxMZBLeqRI:visual:00015000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00015000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:11:50-00:12:00 | video frame at 715.0s] The video segment begins with a black-and-white historical photo of a group of men on horseback in a rugged, rocky landscape. It then transitions to a close-up of a religious icon depicting a crowned figure in ornate robes holding a cross. The scene shifts to a map showing the location of "Stefan cel Mare St" in Moldova, followed by a zoomed-in view of the street on a map. The final frames display a dramatic historical painting of a battle scene, featuring a central figure on horseback amidst chaos and combat. Overlaid audio discusses "Athlete of Christ," Moldova's favorite person to name things after, and references a highly esteemed ruler in Romanian history who brought in a large batch of something, likely alluding to the historical and cultural significance of the figure depicted.
```

**img2** (cited)

```
[00:01:40-00:01:50 | video frame at 105.0s] Two men in blue shirts are shown seated at a laptop, with national flags superimposed on their chests. One man gestures emphatically while speaking, and the other listens. The scene transitions to a cartoon depiction of a man with a Greek flag on his shirt, screaming with an angry expression against a backdrop of ancient Athens. The word "ATSINGANI" appears over the image. The video then cuts to a historical painting depicting a chaotic battle scene with knights, soldiers, and civilians in a Middle Eastern city, featuring a prominent domed building and smoke rising in the background.
```

**img3** (cited)

```
[00:01:50-00:02:00 | video frame at 115.0s] The video begins with a historical painting depicting a chaotic battle scene featuring Crusaders and local figures, followed by a transition to a blurred background with the Google Translate logo. The text "DON'T TOUCH" appears prominently. The scene then shifts to a close-up of a man with a beard, lying on the ground and looking upward, his expression shifting from awe to distress as he closes his eyes.
```
