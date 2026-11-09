# Section 4 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:18:11): `{'video_id': '0RxMZBLeqRI', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 16, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 6.02}`
- image request (2026-10-25 14:18:14): `{'video_id': '0RxMZBLeqRI', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 0.89}`
- L1 filter LLM call: prompt 10063 tokens, output 68 tokens, 4.8 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 30sec | 00:01:00–00:01:30 | 1 / 0.032522 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_2` |
| txt2 | ✓ | worldmm-episodic | 10sec | 00:01:20–00:01:30 | 2 / 0.032266 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_8` |
| txt3 | ✓ | worldmm-episodic | 10sec | 00:01:10–00:01:20 | 3 / 0.032258 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_7` |
| txt4 |  | worldmm-episodic | 30sec | 00:00:00–00:00:30 | 4 / 0.032787 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_0` |
| txt5 | ✓ | worldmm-episodic | 10min | 00:00:00–00:10:00 | 5 / 0.04918 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10min_0` |
| txt6 |  | worldmm-episodic | 30sec | 00:07:30–00:08:00 | 6 / 0.016129 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_15` |
| txt7 |  | worldmm-episodic | 30sec | 00:02:00–00:02:30 | 7 / 0.016129 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_4` |
| txt8 |  | worldmm-episodic | 30sec | 00:09:00–00:09:30 | 8 / 0.031746 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_18` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.032522 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_15` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_175` |
| txt11 | ✓ | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_14` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016129 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_200` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:01:00-00:01:30 | episodic 30sec] **[Event 1: Introduction and Origin Mystery]**  
The video opens with a title card posing the question “Who are the Gypsies?” and immediately sets the tone by presenting a map animation tracing the historical spread from the Middle East and South Asia westward through the Balkans into Europe. A 3D figure holding a red question mark symbolizes the enduring mystery surrounding the Gypsies’ origins, despite their documented presence in the Balkans and Europe since the 13th century. The narration establishes this historical enigma as the central theme.

**[Event 2: Historical Context and Early Misidentification]**  
The video transitions to a stylized 13th-century map of Europe and the Balkans, featuring a dancing woman in traditional attire, visually anchoring the Gypsies’ cultural presence. This is followed by a depiction of a faceless crowd and a red arrow pointing toward the Balkans, indicating movement or migration. A “VS” graphic introduces a symbolic conflict between the Seljuk Turks (represented by a figure in a red fez) and the Byzantine Empire (represented by a crowned figure), as narrated. The scene then reinforces this with a graphic showing a Seljuk Turk and Byzantine emperor facing each other across a “VS” symbol, underscoring the geopolitical tensions of the era.

**[Event 3: Arrival and Misidentification]**  
The video continues with a map highlighting the Balkans again, overlaid by a man in a red shirt, white shorts, and fez, seemingly walking along the arrow’s path—visually suggesting migration. This is followed by a historical battle scene with mounted soldiers, blue banners, and fallen warriors, reinforcing the context of warfare between Christian and Muslim forces. The narration explains that the first Gypsy arrivals were mistaken for Seljuk Turks by the Byzantines, due to the ongoing conflicts between Christian Europe and Muslim Turks, thus embedding the Gypsies’ early identity within the historical and political landscape of the time.
```

**txt2** (cited)

```
[00:01:20-00:01:30 | episodic 10sec] A graphic depicts a stylized face of a Seljuk Turk on the left and a Byzantine emperor on the right, separated by a large "VS" symbol, illustrating conflict. The scene transitions to a map of the region showing a red arrow pointing toward the Balkans, indicating movement or invasion. A man dressed in a red shirt, white shorts, and a fez appears superimposed over the map, seemingly walking along the arrow’s path. The video then shifts to a historical painting depicting a battle scene with mounted soldiers, blue banners, and fallen warriors, suggesting warfare between Christian and Muslim forces. The accompanying narration discusses how the first Gypsy arrivals were mistaken for Seljuk Turks by the Byzantines amid ongoing wars between Christian Europe and Muslim Turks.
```

**txt3** (cited)

```
[00:01:10-00:01:20 | episodic 10sec] An animated map of Europe and the Balkans from the 13th century is shown, featuring a stylized woman in traditional attire dancing. The scene transitions to a depiction of a large, faceless crowd, followed by a map highlighting a red arrow pointing toward the Balkans. This is followed by a “VS” graphic, then two illustrated figures facing each other—one wearing a red fez and the other a decorated crown—symbolizing a conflict between the Seljuk Turks and the Byzantines, as described in the accompanying narration.
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
[00:07:30-00:08:00 | episodic 30sec] **[Event 1: Introduction and Setting]**  
The video opens with a title card reading “Byzantium & the Seljuks, Chapter III,” followed by a black screen and a dynamic shot of a man running across a field with the text “LEAVING INDIA” overlaid. The scene then transitions to a scenic, wide-angle view of a mountainous valley featuring snow-capped peaks, a winding river, and a road under a partly cloudy sky — establishing a geographic and atmospheric context for the historical narrative.

**[Event 2: Historical Context and Transition to Anatolia]**  
The video shifts to a topographical map highlighting the Anatolian region, followed by a clear view of the Hagia Sophia in Istanbul, its domes and minarets prominent under a blue sky. Animated flames suddenly engulf the foreground, symbolizing destruction or decline. The scene then transitions to an animated battle sequence — a warrior in a white turban holding a crowned figure’s face, with soldiers clashing and siege engines firing — visually representing the conflict between the Byzantine Empire and the rising Seljuk Turks.

**[Event 3: Expansion and Social Change in Byzantium]**  
The video continues with an animated depiction of a battle, then cuts to a map highlighting the easternmost territories of Byzantium, with an animated character pointing to the region — indicating territorial shifts due to Seljuk expansion. The scene then transitions to a cartoon carpenter performing various tasks — hammering, sawing, measuring, and nailing — symbolizing labor and craftsmanship. It concludes with a black-and-white image of a lone individual standing in the center of a large crowd, representing social marginalization. Accompanying narration contextualizes the weakening Byzantine Empire, the rise of Muslim Turks, and the arrival of gypsies who took on trade roles and were perceived as outsiders — underscoring themes of cultural change, economic adaptation, and social exclusion.
```

**txt7**

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

**txt8**

```
[00:09:00-00:09:30 | episodic 30sec] The video opens with animated depictions of medieval cavalry warfare, showcasing mounted soldiers wielding lances and bearing heraldic shields, followed by a historical map tracing migration routes marked with key dates—from 1322 to 1850—illustrating population movements driven by military campaigns and Ottoman slave labor into the Balkans and beyond.

The scene transitions to a title card reading “The Balkans Chapter IV,” introduced by a symbolic red heart revealing the phrase “Byzantine my beloved,” alongside a map of the Byzantine Empire, setting a thematic tone of historical and cultural legacy. The narrative then shifts to a historical tapestry portraying a lively medieval scene with soldiers and civilians amid urban and natural settings, grounding the viewer in the era’s social fabric.

The video continues with a map of the Ottoman Empire and its Balkan territories—including Wallachia and various pashaliks—accompanied by narration that contextualizes the widespread presence of Roma (Gypsies) in the region and characterizes Ottoman-controlled lands as predominantly agrarian societies. The segment concludes with a painting of a farmer plowing a field with oxen, visually reinforcing the agricultural foundation of these societies and underscoring the socio-economic structure of the time.
```

**txt9**

```
[video-level knowledge | semantic] (First Gypsy arrivals, mistaken for, Seljuk Turks by Byzantines)
```

**txt10**

```
[video-level knowledge | semantic] (historical map, is about, Balkans)
```

**txt11** (cited)

```
[video-level knowledge | semantic] (Seljuk Turks, symbolized by, illustrated figure wearing red fez)
```

**txt12**

```
[video-level knowledge | semantic] (Roma, mentioned in, narration)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:06:15 | 00:06:10–00:06:20 | `0RxMZBLeqRI:visual:00061000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00061000.jpg` |
| img2 |  | 00:16:05 | 00:16:00–00:16:10 | `0RxMZBLeqRI:visual:00160000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00160000.jpg` |
| img3 | ✓ | 00:01:15 | 00:01:10–00:01:20 | `0RxMZBLeqRI:visual:00011000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00011000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:06:10-00:06:20 | video frame at 375.0s] A map showing the Ghaznavid Empire is displayed, highlighting its territory across parts of modern-day Afghanistan, Pakistan, and Iran, with major cities marked. The scene then transitions to an illustrated depiction of a military procession, featuring a central figure seated on an elaborately decorated elephant, flanked by armored soldiers on horseback and holding spears. The audio includes fragmented, repetitive speech: “they are in they were they are they they are and they be they are.”
```

**img2**

```
[00:16:00-00:16:10 | video frame at 965.0s] The video segment begins with a historical illustration of people in traditional attire, accompanied by text discussing decrees limiting slavery in the Ottoman Empire, specifically mentioning a 1830 edict by Sultan Mahmud II. It then transitions to a black-and-white depiction of a large-scale battle, with the year "1826" superimposed. The scene shifts to a colorful painting of a chaotic cavalry battle in a mountainous landscape. The final frames display a political map of Eastern Europe highlighting the Ottoman Empire, Russia, and surrounding regions, with dates—24 May 1828, 10 July 1828, and 26 August 1828—appearing alongside portraits of Sultan Mahmud II and Tsar Nicolas I.
```

**img3** (cited)

```
[00:01:10-00:01:20 | video frame at 75.0s] An animated map of Europe and the Balkans from the 13th century is shown, featuring a stylized woman in traditional attire dancing. The scene transitions to a depiction of a large, faceless crowd, followed by a map highlighting a red arrow pointing toward the Balkans. This is followed by a “VS” graphic, then two illustrated figures facing each other—one wearing a red fez and the other a decorated crown—symbolizing a conflict between the Seljuk Turks and the Byzantines, as described in the accompanying narration.
```
