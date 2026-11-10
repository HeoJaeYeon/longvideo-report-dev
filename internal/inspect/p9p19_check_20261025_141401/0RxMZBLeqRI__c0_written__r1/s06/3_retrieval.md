# Section 6 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:21:23): `{'video_id': '0RxMZBLeqRI', 'mode': 'L1', 'queries': 2, 'episodic_candidates': 17, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 5.77}`
- image request (2026-10-25 14:21:26): `{'video_id': '0RxMZBLeqRI', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 0.89}`
- L1 filter LLM call: prompt 11164 tokens, output 64 tokens, 5.0 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 |  | worldmm-episodic | 30sec | 00:04:30–00:05:00 | 1 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_9` |
| txt2 |  | worldmm-episodic | 10sec | 00:04:50–00:05:00 | 2 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_29` |
| txt3 | ✓ | worldmm-episodic | 3min | 00:27:00–00:30:00 | 3 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:3min_9` |
| txt4 | ✓ | worldmm-episodic | 30sec | 00:00:00–00:00:30 | 4 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_0` |
| txt5 | ✓ | worldmm-episodic | 3min | 00:00:00–00:03:00 | 5 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:3min_0` |
| txt6 |  | worldmm-episodic | 10sec | 00:00:20–00:00:30 | 6 / 0.016129 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_2` |
| txt7 |  | worldmm-episodic | 30sec | 00:02:00–00:02:30 | 7 / 0.016129 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_4` |
| txt8 | ✓ | worldmm-episodic | 3min | 00:06:00–00:09:00 | 8 / 0.016129 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:3min_2` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_70` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_8` |
| txt11 | ✓ | worldmm-semantic | — | no timestamp | 3 / 0.016129 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_402` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016129 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_7` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1**

```
[00:04:30-00:05:00 | episodic 30sec] The video opens with symbolic national imagery—first overlaying Germany’s flag on its map, then Greece’s flag on its map—before shifting to a historical context by highlighting Carthage with a cartoon figure beside it, culminating in a surreal visual of a Simpsons character with a thought bubble, suggesting thematic or narrative transition.

Next, the video juxtaposes religious and historical imagery: a cartoon character with glasses and a Bible in his thought bubble, followed by classical paintings of animal sacrifices and a muscular man in struggle, ending with a stark, wide desert landscape—possibly symbolizing isolation, history, or spiritual desolation.

The narrative then moves to a grounded, human-centered scene: a man with a shaved head and beard, smiling while seated in a car, followed by an anime-style girl superimposed over a historical painting of a struggle with sheep in the background—a blend of modernity and ancient themes. The video closes with a wide, reverent shot of an empty cathedral, emphasizing scale, silence, and perhaps spiritual or historical reflection.

Throughout, the video uses layered visual transitions to connect national identity, historical memory, religious symbolism, and personal or cultural moments, concluding with a sense of solemn grandeur.
```

**txt2**

```
[00:04:50-00:05:00 | episodic 10sec] The video begins with a wide shot of a desert landscape featuring sand dunes, scattered vegetation, and distant rock formations under a clear sky. It then cuts to a close-up of a man with a shaved head and beard, wearing a blue shirt, smiling and speaking while seated inside a car. The scene transitions to an animated image of a cheerful anime-style girl in a traditional outfit, superimposed over a historical painting depicting two figures in a struggle, with sheep visible in the background. The video concludes with a wide shot of the interior of a grand, empty cathedral, showcasing its tall stone pillars, arched ceilings, and rows of wooden pews.
```

**txt3** (cited)

```
[00:27:00-00:30:00 | episodic 3min] **[Event 1: Marginalized Lives and Systemic Struggle]**  
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

**txt4** (cited)

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
[00:00:00-00:03:00 | episodic 3min] **[Event 1: Introduction and Context Setting]**  
The video opens with a disclaimer clarifying the use of “Gypsy” as a non-slandrous term for Roma/Romani, followed by a map of the Balkans and a montage of memes and historical battle tables — including a satirical “TITO INVENTING MACEDONIANS” image — underscoring entrenched ethnic hatred in the region.

**[Event 2: Visual Montage and Narrated Commentary on Roma Perception]**  
A text overlay introduces Roma presence in the Balkans, juxtaposed with visuals of marginalization (a person turning away from a trash can) and social tension (shirtless man shouting, bearded speaker). The segment ends with a still of Obama over dilapidated buildings, overlaid with “POREKLOM SAM CIGANIN,” fading to black — reinforcing identity erasure and societal stigma.

**[Event 3: Historical and Cultural Representation of the Roma]**  
Sepia-toned historical photos of Roma families in traditional attire transition to a modern parade with Roma, Ukrainian, and EU flags — affirming their cultural role. Narration acknowledges their historical invisibility due to stigma and lack of scholarly attention.

**[Event 1: Scientific Experimentation and Historical Stigmatization]**  
A lab-coated figure transfers liquid, symbolizing scientific precision, cuts to a black-and-white “X”-marked scientist — suggesting exclusion. Montage of cultural heritage (band, family with instruments) transitions to “UNWANTED” superimposed over historical scenes — highlighting systemic stigmatization.

**[Event 2: Fantasy Conflict and Societal Stereotypes]**  
Minecraft mining scenes transition to a horned figure declaring “Your money or your life,” followed by dark fantasy combat and a hooded figure with dollar signs — symbolizing corruption. Joyful dance scenes contrast with black-and-white images of displaced people — framing stereotypes as products of fear and misunderstanding.

**[Event 1: Introduction and Origin Mystery]**  
A title card asks “Who are the Gypsies?” followed by a map animation tracing migration from Middle East/South Asia to Europe. A 3D figure with a question mark symbolizes the enduring mystery of their origins since the 13th century.

**[Event 2: Historical Context and Early Misidentification]**  
A 13th-century map anchors Roma presence. A “VS” graphic depicts Seljuk Turks vs. Byzantine Empire — narrated as geopolitical tensions shaping early misidentification of Roma as Turks.

**[Event 3: Arrival and Misidentification]**  
A man in a fez walks along migration arrows. Historical battle scenes reinforce Christian-Muslim conflict. Narration explains Roma were first mistaken for Seljuk Turks by Byzantines — embedding their identity in historical geopolitics.

**[Event 1: Medieval Battle Depiction and Historical Framing]**  
A medieval battle painting with knights and flags transitions to “SARACEN = HEATHENS” — framing conflict through polemical lens.

**[Event 2: Modern Commentary and Symbolic Representation]**  
A young person looks at camera, followed by two men at a laptop with flags — suggesting commentary. A cartoon Greek figure screams “ATSINGANI” — a slur against non-Christians — implying political critique.

**[Event 3: Battle in Middle Eastern City and Google Translate Interlude]**  
A chaotic Crusader battle scene in a Middle Eastern city transitions to a “DON’T TOUCH” Google Translate warning — cautioning against misinterpretation. Ends with a bearded man’s face shifting from awe to distress — symbolizing human cost.

**[Event 1: Introduction and Cultural Identity Framing]**  
A bearded man gazes upward against rocky backdrop, setting reflective tone. Two young men outdoors with “Atsingani” overlay transition to an anime girl in traditional attire gesturing over Balkan map — anchoring cultural context.

**[Event 2: Linguistic and Historical Context]**  
Words “CIGANI,” “CIGÁNYOK,” “TIGANI,” “ZIGEUNER” appear with flags — showing linguistic variations. Migration map from “before 650” to “ca. 1700” emphasizes “One single migration” — framing unified origin.

**[Event 3: Scholarly Analysis and Visual Commentary]**  
A man draws a circle with line through it — symbolizing exclusion. Scholarly discussion on medieval Adriatic origins is paired with a topographical map highlighting coastal zones — reinforcing geographical focus.

**[Event 4: Satirical Visual Interlude]**  
A rat-headed figure in a suit speaks into mic — satirical commentary. Meme juxtapositions (“AVERAGE GREEK BE LIKE:”) and surreal desert scenes culminate in a green upward-trending graph — symbolizing absurd success or growth. Ends with “GYPSY = EGYPTIAN” and a Europe-North Africa map — closing on semantic and geographic ambiguity.
```

**txt6**

```
[00:00:20-00:00:30 | episodic 10sec] The video begins with a title card reading "GYPSIES," followed by historical sepia-toned photographs showing Roma families in traditional attire, some gathered around a caravan and others posing formally. The scene transitions to a modern-day street parade where participants, including women in colorful traditional clothing and men in contemporary attire, march while carrying flags — one of which is the Roma flag featuring a red wheel on a green background, alongside the Ukrainian and European Union flags. Overlaid narration discusses the Roma as an integral part of Balkan culture and history, yet notes that due to generational stigma, prejudice, and a lack of research, very little is known about them.
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

**txt8** (cited)

```
[00:06:00-00:09:00 | episodic 3min] **[Event 1: Ghaznavid Empire’s Rise and Expansion]**  
The video opens with a symbolic map of South Asia, silhouetted figures in turbans marking regional influence, narrowing to the Ghaznavid Empire’s territory across modern Afghanistan, Pakistan, and northern India. Key cities are labeled, establishing its geopolitical reach. Visuals shift to a detailed map including Iran, followed by an illustrated military procession — a central figure on an elephant flanked by cavalry — evoking imperial power. The fragmented audio “they are... they are...” underscores thematic ambiguity and historical echo.

**[Event 2: Conquest, Flight, and Cultural Displacement]**  
The narrative transitions to battlefield imagery and courtly diplomacy, underscored by narration on enduring bloodshed post-Ghaznavid era. A map visualizes eastward expansion into India, marked by flames at Lahore, Mathura, and Kannauj, reinforced by siege scenes. A man in sunglasses stands before a mural, lifting a clock as narration describes mass exodus westward through the Hindu Kush. A solitary figure in a blue robe walks through a desert, examining a globe card — a journey framed by arid terrain.

**[Event 3: Silk Road and Trade Networks]**  
The scene shifts to a vibrant river and serene mountain valley, setting a contrast to prior desolation. An animated map traces the Silk Road’s route from Khorasan through Central Asia to Trebizond, marked with time indicators (900–1200). An animated character guides viewers through key waypoints, emphasizing commerce and cultural exchange before fading to black.

**[Event 4: Byzantium, Seljuks, and Anatolian Conflict]**  
The video opens with “Byzantium & the Seljuks, Chapter III” and “LEAVING INDIA,” transitioning to a mountainous valley. A topographical map highlights Anatolia, followed by Hagia Sophia under blue skies. Animated flames erupt, symbolizing decline, then a battle sequence depicts Byzantine-Seljuk conflict — a warrior holding a crowned face amid clashing armies and siege engines.

**[Event 5: Social Change and Marginalization in Byzantium]**  
Animated battle scenes transition to a map of Byzantium’s eastern territories. A cartoon carpenter symbolizes labor, concluding with a lone figure in a crowd — representing social exclusion. Narration contextualizes Byzantium’s weakening, Muslim Turkic rise, and Romani arrival as traders, underscoring cultural adaptation and marginalization.

**[Event 6: Romani Migration and Turkic Expansion]**  
A montage of symbolic imagery — anonymous crowds, horse riders, forges, craftsmen, and a modern man with a pizza box — juxtaposes historical and contemporary labor. Narration links Romani migration routes (1200–1850) to their arrival in Europe after 200 years, ending with ancient script symbolizing enduring legacy. A hand writes “EGYPTIANS,” followed by an animated map showing Turkic expansion into Balkans and Anatolia, linking migration to territorial conquest.

**[Event 7: Military Identity and Historical Gaps]**  
Workers and machinery symbolize labor, transitioning to soldiers with Turkish and Azerbaijani flags — hinting at conflict or alliance. A large army marches with flags, reinforcing military identity. A handshake over bars suggests negotiation. Soldiers march forward, followed by scenes of historical battles and file-sorting hands — visually representing missing records. Narration notes Gypsy migration via 14th-century military campaigns, linking movement to conflict and integration.
```

**txt9**

```
[video-level knowledge | semantic] (clip from TV show, ends with, close-up shot)
```

**txt10**

```
[video-level knowledge | semantic] (Roma families, pose formally, in photographs)
```

**txt11** (cited)

```
[video-level knowledge | semantic] (credits, appear at time, 00:30:08)
```

**txt12**

```
[video-level knowledge | semantic] (Roma families, gather around, caravan)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 | ✓ | 00:30:25 | 00:30:20–00:30:30 | `0RxMZBLeqRI:visual:00302000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00302000.jpg` |
| img2 | ✓ | 00:30:31 | 00:30:30–00:30:32 | `0RxMZBLeqRI:visual:00303000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00303000.jpg` |
| img3 |  | 00:30:15 | 00:30:10–00:30:20 | `0RxMZBLeqRI:visual:00301000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00301000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1** (cited)

```
[00:30:20-00:30:30 | video frame at 1825.0s] A stylized globe rotates slowly against a background displaying numerous national flags. The globe begins facing Asia and gradually rotates to show Africa, then the Americas, before returning to focus on Europe and Asia again. No audio is present.
```

**img2** (cited)

```
[00:30:30-00:30:32 | video frame at 1831.0s] The screen displays a grid of various national flags surrounding a central, stylized globe showing the continents of Asia and Australia. The scene then abruptly transitions to complete blackness.
```

**img3**

```
[00:30:10-00:30:20 | video frame at 1815.0s] An anime-style character in a hat and bow tie gestures in front of a backdrop featuring a list of names, then the scene transitions to a rotating globe centered on a grid of international flags.
```
