# Section 5 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:18:57): `{'video_id': '0RxMZBLeqRI', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 20, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 7.02}`
- image request (2026-10-25 14:19:00): `{'video_id': '0RxMZBLeqRI', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 0.86}`
- L1 filter LLM call: prompt 12804 tokens, output 76 tokens, 5.9 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 3min | 00:21:00–00:24:00 | 1 / 0.04918 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:3min_7` |
| txt2 | ✓ | worldmm-episodic | 30sec | 00:24:00–00:24:30 | 2 / 0.016393 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_48` |
| txt3 | ✓ | worldmm-episodic | 30sec | 00:23:00–00:23:30 | 3 / 0.016129 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_46` |
| txt4 | ✓ | worldmm-episodic | 10sec | 00:24:10–00:24:20 | 4 / 0.016129 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_145` |
| txt5 | ✓ | worldmm-episodic | 30sec | 00:22:00–00:22:30 | 5 / 0.031746 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:30sec_44` |
| txt6 | ✓ | worldmm-episodic | 10sec | 00:23:20–00:23:30 | 6 / 0.016129 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_140` |
| txt7 | ✓ | worldmm-episodic | 10sec | 00:23:40–00:23:50 | 7 / 0.015873 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_142` |
| txt8 |  | worldmm-episodic | 10sec | 00:21:00–00:21:10 | 8 / 0.015873 (rrf(order=llm_filter)) | `0RxMZBLeqRI:episodic:10sec_126` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.032266 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_357` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.031258 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_356` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.03101 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_5` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016393 (rrf) | `0RxMZBLeqRI:semantic:semantic_100303200_286` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

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

**txt2** (cited)

```
[00:24:00-00:24:30 | episodic 30sec] A black-and-white historical montage opens with a group of men and children seated in an open field, framed by a fence and a solitary figure in the distance, suggesting a rural or institutional setting. The scene shifts to children and young women posing outdoors, with buildings behind them, possibly indicating a moment of normalcy or daily life. The final frames show a crowd—men, women, and children—behind a barbed-wire fence, marked by the “British Pathé” logo, hinting at a controlled or confined environment.

The video then transitions to footage of emaciated individuals behind a fence, with close-ups of a bandaged man and an elderly woman wearing a head covering, emphasizing suffering. Text overlays state “500 000 - 1 500 000” followed by “killed,” underscoring the scale of mass casualties. The “British Pathé” logo remains visible, reinforcing the archival nature of the footage.

The segment concludes with a black screen, followed by the title “Communism, Chapter VII” in stark white text, framing the preceding imagery as part of a larger historical or ideological narrative. The absence of audio and the visual tone suggest a somber, documentary-style presentation focused on human suffering and historical consequence.
```

**txt3** (cited)

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
[00:24:10-00:24:20 | episodic 10sec] The video shows a black-and-white historical segment featuring a group of people, many appearing distressed or emaciated, standing behind a fence. The camera zooms in on individuals, including a man with a bandaged head and an elderly woman with a head covering. Text overlays appear, stating "500 000 - 1 500 000" and then "killed," indicating a somber context related to mass casualties. The footage bears the "British Pathé" logo in the upper right corner.
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
[00:23:20-00:23:30 | episodic 10sec] A black-and-white historical segment begins with a woman in a headscarf looking out from behind a wooden door. The scene transitions to a group of men in striped prison uniforms standing in formation, with the year "1942" superimposed. The location is identified as "Auschwitz-Birkenau" as prisoners, including women and children, are shown walking along a barbed-wire fence. The footage then shows containers labeled "GIFTGAS ZYKLON B," followed by a shot of piles of clothing and personal belongings.
```

**txt7** (cited)

```
[00:23:40-00:23:50 | episodic 10sec] The video begins with a person in a dark hooded garment holding a knife, followed by a still image of Josef Mengele with his name displayed. The scene then transitions to black-and-white footage of medical personnel attending to patients in what appears to be a hospital or medical facility. The final frames show a wide, desolate view of a concentration camp, with rows of brick buildings flanking a central road that leads toward a gatehouse, as a solitary figure walks down the path.
```

**txt8**

```
[00:21:00-00:21:10 | episodic 10sec] A text overlay explains that German laws against Romani people had been in effect for hundreds of years before the Nazis came to power in 1933, and that persecution began almost as soon as Romani people arrived in German-speaking lands. The video then transitions to black-and-white archival footage of people sitting on the ground with bowls, followed by a historical illustration of a bustling city street in the 1880s, and finally a portrait of a man in a military uniform.
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
[video-level knowledge | semantic] (Video, begins with, title card reading GYPSIES)
```

**txt12**

```
[video-level knowledge | semantic] (final text overlay, cites, 400,000 Muslim Gypsies affected)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:24:05 | 00:24:00–00:24:10 | `0RxMZBLeqRI:visual:00240000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00240000.jpg` |
| img2 |  | 00:24:45 | 00:24:40–00:24:50 | `0RxMZBLeqRI:visual:00244000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00244000.jpg` |
| img3 |  | 00:24:25 | 00:24:20–00:24:30 | `0RxMZBLeqRI:visual:00242000` | `outputs/p9p19_check_20261025_141401/frames_s1/0RxMZBLeqRI/00242000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:24:00-00:24:10 | video frame at 1445.0s] The video segment shows a series of black-and-white historical images. It begins with a group of men and children sitting on the ground in an open field, with a fence and a solitary figure standing in the background. The scene transitions to a group of children and young women posing together outdoors, with buildings visible behind them. The final frames depict a crowd of people, including men, women, and children, standing behind a barbed wire fence, with the "British Pathé" logo visible in the corner. There is no audible content in the segment.
```

**img2**

```
[00:24:40-00:24:50 | video frame at 1485.0s] The video transitions through several distinct scenes. It begins with a black-and-white shot of a large crowd of people, many in striped uniforms, walking in an outdoor area with barbed wire fences and buildings in the background. The scene then cuts to a formal indoor setting where several men in suits are seated at a long table with microphones, appearing to be in a conference or hearing. The camera then shifts to a courtroom where a man in a light-colored uniform stands at a podium addressing seated individuals, some wearing headphones, while soldiers in helmets stand guard. The final frame abruptly changes to a colorful, animated image of a stylized female character in a hat and bow tie, superimposed over a sepia-toned background showing people and horse-drawn carts on a street.
```

**img3**

```
[00:24:20-00:24:30 | video frame at 1465.0s] The video begins with a black-and-white shot of a group of people standing behind a barbed-wire fence, then cuts to a black screen before displaying the title "Communism, Chapter VII" in white text on a black background.
```
