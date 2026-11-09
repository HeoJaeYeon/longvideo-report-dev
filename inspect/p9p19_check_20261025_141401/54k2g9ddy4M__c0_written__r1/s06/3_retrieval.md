# Section 6 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:20:23): `{'video_id': '54k2g9ddy4M', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 25, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 6.44}`
- image request (2026-10-25 14:20:26): `{'video_id': '54k2g9ddy4M', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 0.96}`
- L1 filter LLM call: prompt 10544 tokens, output 73 tokens, 5.2 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 10min | 00:30:00–00:40:00 | 1 / 0.032787 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10min_3` |
| txt2 | ✓ | worldmm-episodic | 3min | 00:36:00–00:39:00 | 2 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:3min_12` |
| txt3 | ✓ | worldmm-episodic | 3min | 00:39:00–00:42:00 | 3 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:3min_13` |
| txt4 | ✓ | worldmm-episodic | 30sec | 00:36:30–00:37:00 | 4 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_73` |
| txt5 | ✓ | worldmm-episodic | 10sec | 00:39:10–00:39:20 | 5 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_235` |
| txt6 | ✓ | worldmm-episodic | 30sec | 00:38:00–00:38:30 | 6 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_76` |
| txt7 | ✓ | worldmm-episodic | 10sec | 00:38:50–00:39:00 | 7 / 0.015873 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_233` |
| txt8 | ✓ | worldmm-episodic | 30sec | 00:39:30–00:40:00 | 8 / 0.015873 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_79` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_550` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_453` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_29` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016129 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_564` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:30:00-00:40:00 | episodic 10min] **[Event Summary]**  
Joshua Liendo, Canada’s first Black swimmer to reach elite milestones, reflects on his journey from Trinidad to global podiums, framed by personal memories, cultural roots, and athletic triumph. The CBC News segment, titled “Joshua Liendo swims into the history books,” traces his evolution from childhood in Trinidad to competing in the Men’s 100m Butterfly Final, where he secured victory amid roaring Canadian fan support. Wearing a Florida Gators shirt, Liendo credits intentional coaching, rising role models like Dylan Carter and George Bevel, and a growing Caribbean swimming culture for his success. He contrasts the warmth of Florida with the cold winters of Toronto, where he relocated at age 10, and expresses deep nostalgia for Trinidad’s community and lifestyle — a connection he hasn’t revisited since 2018. The narrative also confronts systemic underrepresentation in elite swimming, as Liendo speaks candidly about cultural stereotypes and the sacrifices of his parents that fueled his career. Alternating between dynamic race footage, studio interviews, and nostalgic visuals — including childhood photos and family portraits — the segment positions Liendo not just as an athlete, but as a symbol of progress and representation. His historic win, underscored by on-screen graphics and enthusiastic crowds, marks a milestone in both his personal legacy and the broader story of diversity in competitive swimming.

**[Event Summary]**  
Joshua Liendo, dressed in a white Florida Gators shirt and gold chain, reflects on his journey as a rising Olympic swimmer while standing in an indoor pool facility, framed by CBC News’ headline “Joshua Liendo swims into the history books.” He draws inspiration from athletes like Allen Iverson, acknowledging their influence on his athletic and personal development. The segment intercuts his reflections with archival footage of Iverson, highlighting his iconic dunks and tattoos, while also weaving in his parents’ basketball passion and his interest in a documentary — all reinforcing his evolving identity as both athlete and role model.

**[Event Summary]**  
Liendo speaks candidly with a suited interviewer in the pool facility, discussing gender disparities in swimming and his own path to Olympic qualification. He references past relay finals and a missed individual final, expressing cautious optimism about the unpredictable nature of elite competition. The narrative emphasizes his focus on the present, urging himself and his team to maintain control over immediate goals rather than prematurely anticipating future milestones.

**[Event Summary]**  
The video alternates between Liendo’s reflections and race footage, showcasing his historic first international gold in the 100-meter butterfly at the Doha World Championships. Scenes capture him mid-stroke, adjusting goggles post-race, and emerging triumphant from the pool — his cap bearing Yakult and Speedo logos, with Omega branding visible. A Canadian coach in a red “CANADA” shirt raises his fist in celebration, underscoring the national victory and building momentum toward the Paris Olympics.

**[Event Summary]**  
The segment concludes with Liendo smiling warmly at the anchor, reinforcing his pride and humility. A brief, unrelated graphic of a burning building appears, serving as a dramatic visual transition — though its thematic connection remains unexplained. Throughout, the narrative blends personal narrative, athletic achievement, and public responsibility, cementing Liendo’s emergence as a historic figure in Canadian swimming.

---

**[Event Summary]**  
A devastating fire in late January destroyed the only school on Eabametoong First Nation, Northwestern Ontario, leaving charred ruins blanketed in snow and triggering a community-wide crisis. The blaze, which overwhelmed local firefighting efforts due to inadequate water infrastructure, forced children to relocate for education and deepened grief among residents. Four teenagers have been charged in connection with the arson. Community members, including teacher Mary Okeese and student Owen Slipperjack, shared emotional testimonies contrasting joyful school memories with the current devastation. Chief Solomon Atlookan emphasized systemic vulnerabilities in emergency response for remote Indigenous communities. Aerial and ground footage underscored the isolation of the community, 360 km from Winnipeg, near Thunder Bay. In response, the federal government pledged over $13 million to construct five modular classrooms as temporary solutions, aiming to restore educational continuity for affected children. The Canadian and First Nations flags fly at half-mast as the community mourns and begins the long road to recovery.

**[Event Summary]**  
A devastating fire destroyed a remote First Nation school, leaving behind charred ruins and triggering widespread grief — captured in footage of the collapsed roof under a cloudy sky, alongside Canadian and First Nation flags. The federal government pledged full support for rebuilding, with officials vowing to stand with the community in constructing a new permanent school.

**[Event Summary]**  
By June 2023, Pikangikum First Nation unveiled its newly built school — a modern facility with vehicles parked outside — symbolizing a decade-long wait for replacement after the original school was lost to fire. The narration underscores the urgency of the rebuild and the community’s prolonged struggle for educational infrastructure.

**[Event Summary]**  
In September 2023, Wapekeka First Nation celebrated the grand opening of its new school — a colorful, modern building adorned with festive decorations, balloons, and banners. The event marked the end of an eight-year wait following the fire, showcasing community resilience and the government’s eventual fulfillment of long-delayed promises.

**[Event 1: School Destruction and Community Ceremony]**  
A memorial ceremony was held in a gymnasium, followed by footage of the “Rev. Eleazar Winter Memorial School” sign and a large nighttime fire, confirming the school’s destruction. The scene reflects the community’s grief and resilience amid profound loss.

**[Event 2: Ongoing Water Crisis in Remote First Nation]**  
Footage of a snowy, remote First Nation highlights infrastructure challenges. A yellow pedestrian crossing sign and people walking through snow with a child’s sled are shown. On-screen text reads: “Remote First Nation feels heavy loss after fire destroys school,” while narration emphasizes the community’s long-standing boil water advisory since 2002, and their determination to sustain education despite inadequate fire, water, and housing services.

**[Event 3: CBC News Report on Community Recovery]**  
A CBC News segment features reporter Sarah Law in studio discussing the school fire with correspondent details. The segment opens with exterior shots of the snowy community, showing the damaged school and a vehicle passing the wreckage. The report highlights cleanup operations, arrival of supplies via winter road, and logistical strategies using the cold snap to transport materials for a temporary school. It also covers repurposing community facilities — extending a hall for education and installing artificial ice in an arena for youth recreation — while underscoring Ontario’s Minister of Indigenous Affairs’ involvement and the community’s cautious optimism.

**[Event 4: Pet Psychic Trend Segment]**  
The segment transitions to footage of various dogs in park-like settings, paired with human interaction and expressive close-ups — including a fluffy light-brown dog with a pink flower, a wrinkled pug, and a chocolate Labrador — while a lower third graphic and news ticker announce rising demand for pet psychics, branded with the CBC News logo. The footage alternates between playful and contemplative moments, framed with a journalistic tone suggesting an upcoming report on the growing trend of pet psychic services.
```

**txt2** (cited)

```
[00:36:00-00:39:00 | episodic 3min] **[Event Summary]**  
A devastating fire in late January destroyed the only school on Eabametoong First Nation, Northwestern Ontario, leaving charred ruins blanketed in snow and triggering a community-wide crisis. The blaze, which overwhelmed local firefighting efforts due to inadequate water infrastructure, forced children to relocate for education and deepened grief among residents. Four teenagers have been charged in connection with the arson. Community members, including teacher Mary Okeese and student Owen Slipperjack, shared emotional testimonies contrasting joyful school memories with the current devastation. Chief Solomon Atlookan emphasized systemic vulnerabilities in emergency response for remote Indigenous communities. Aerial and ground footage underscored the isolation of the community, 360 km from Winnipeg, near Thunder Bay. In response, the federal government pledged over $13 million to construct five modular classrooms as temporary solutions, aiming to restore educational continuity for affected children. The Canadian and First Nations flags fly at half-mast as the community mourns and begins the long road to recovery.
```

**txt3** (cited)

```
[00:39:00-00:42:00 | episodic 3min] **[Event Summary]**  
A devastating fire destroyed a remote First Nation school, leaving behind charred ruins and triggering widespread grief — captured in footage of the collapsed roof under a cloudy sky, alongside Canadian and First Nation flags. The federal government pledged full support for rebuilding, with officials vowing to stand with the community in constructing a new permanent school.

**[Event Summary]**  
By June 2023, Pikangikum First Nation unveiled its newly built school — a modern facility with vehicles parked outside — symbolizing a decade-long wait for replacement after the original school was lost to fire. The narration underscores the urgency of the rebuild and the community’s prolonged struggle for educational infrastructure.

**[Event Summary]**  
In September 2023, Wapekeka First Nation celebrated the grand opening of its new school — a colorful, modern building adorned with festive decorations, balloons, and banners. The event marked the end of an eight-year wait following the fire, showcasing community resilience and the government’s eventual fulfillment of long-delayed promises.

**[Event 1: School Destruction and Community Ceremony]**  
A memorial ceremony was held in a gymnasium, followed by footage of the “Rev. Eleazar Winter Memorial School” sign and a large nighttime fire, confirming the school’s destruction. The scene reflects the community’s grief and resilience amid profound loss.

**[Event 2: Ongoing Water Crisis in Remote First Nation]**  
Footage of a snowy, remote First Nation highlights infrastructure challenges. A yellow pedestrian crossing sign and people walking through snow with a child’s sled are shown. On-screen text reads: “Remote First Nation feels heavy loss after fire destroys school,” while narration emphasizes the community’s long-standing boil water advisory since 2002, and their determination to sustain education despite inadequate fire, water, and housing services.

**[Event 3: CBC News Report on Community Recovery]**  
A CBC News segment features reporter Sarah Law in studio discussing the school fire with correspondent details. The segment opens with exterior shots of the snowy community, showing the damaged school and a vehicle passing the wreckage. The report highlights cleanup operations, arrival of supplies via winter road, and logistical strategies using the cold snap to transport materials for a temporary school. It also covers repurposing community facilities — extending a hall for education and installing artificial ice in an arena for youth recreation — while underscoring Ontario’s Minister of Indigenous Affairs’ involvement and the community’s cautious optimism.

**[Event 4: Pet Psychic Trend Segment]**  
The segment transitions to footage of various dogs in park-like settings, paired with human interaction and expressive close-ups — including a fluffy light-brown dog with a pink flower, a wrinkled pug, and a chocolate Labrador — while a lower third graphic and news ticker announce rising demand for pet psychics, branded with the CBC News logo. The footage alternates between playful and contemplative moments, framed with a journalistic tone suggesting an upcoming report on the growing trend of pet psychic services.
```

**txt4** (cited)

```
[00:36:30-00:37:00 | episodic 30sec] The video documents the aftermath of a devastating school fire in Eabametoong First Nation, Northwestern Ontario, showing charred ruins under snow and flags flown at half-mast as the community mourns. A news anchor in studio coverage highlights the community’s grief and uncertainty over rebuilding, while footage transitions between solemn exterior shots of the damaged school and interior scenes of students in hoodies attentively engaged in class — a stark contrast to the destruction outside. The narrative underscores the community’s resilience and the urgent need to restore their educational infrastructure, with visuals reinforcing the loss and the hope for renewal.
```

**txt5** (cited)

```
[00:39:10-00:39:20 | episodic 10sec] The video shows the aftermath of a fire that destroyed a school, with the charred remains visible under a cloudy sky, alongside Canadian and First Nation flags. The scene then transitions to a modern, newly constructed school building at Pikangikum First Nation in June 2023, with numerous vehicles parked in front. The accompanying narration discusses the urgency for action, noting that the community waited a decade for a new school after the previous one was destroyed.
```

**txt6** (cited)

```
[00:38:00-00:38:30 | episodic 30sec] **[Event 1: On-the-ground aftermath and community loss]**  
A man and a woman stand near the snow-covered ruins of a burned building, discussing the devastation of a school fire. The man gestures toward the wreckage, underscoring the scale of destruction. The scene shifts to a person carrying a black storage bin into the building, while two dogs observe from outside — suggesting ongoing cleanup or recovery efforts. The segment closes with a close-up of a person in a red backpack near a chain-link fence, accompanied by on-screen text emphasizing the community’s profound loss following the fire.

**[Event 2: Geographic context and community identification]**  
The video transitions to a map showing Eabametoong First Nation in Ontario, 360 km from Winnipeg and near Thunder Bay, highlighting its remote location. This is followed by an interview with Paul Holcroft, identified as a parent, speaking in front of a blue metal building. On-screen text reinforces the theme: “Remote First Nation feels heavy loss after fire destroys school.”

**[Event 3: Visual documentation of destruction and isolation]**  
Paul Holcroft continues speaking to the camera, emphasizing the community’s grief. The video then cuts to an aerial view of the snow-covered, charred remains of the school, with debris scattered across the landscape. A final shot from an airplane window reveals the vast, remote, snowy terrain — punctuated by forests and water — underscoring the geographic isolation of the community. The on-screen text reiterates: “Remote First Nation feels heavy loss after fire destroys school.”
```

**txt7** (cited)

```
[00:38:50-00:39:00 | episodic 10sec] The video shows the aftermath of a fire that destroyed a school in a remote First Nation community, with shots of the charred and collapsed structure, including twisted metal roofing and debris scattered across snow-covered ground. The accompanying narration explains that after leaving Iyabmikam, the Federal Minister of Indigenous Services met with the chief in Thunder Bay to confirm the government’s plan to spend over $13 million on five modular buildings to serve as temporary classrooms for the community.
```

**txt8** (cited)

```
[00:39:30-00:40:00 | episodic 30sec] **[Event 1: School Destruction and Community Ceremony]**  
A ceremony is held in a gymnasium, followed by footage of the “Rev. Eleazar Winter Memorial School” sign and a large nighttime fire, confirming the school’s destruction. The scene underscores the community’s grief and resilience in the face of loss.

**[Event 2: Ongoing Water Crisis in Remote First Nation]**  
Footage of a snowy, remote First Nation community highlights infrastructure challenges. A yellow pedestrian crossing sign and people walking through snow with a child’s sled are shown. On-screen text reads: “Remote First Nation feels heavy loss after fire destroys school,” while narration and audio emphasize the community’s long-standing boil water advisory since 2002, and their determination to sustain education despite lacking adequate fire and water services and housing.

**[Event 3: CBC News Report on Community Recovery]**  
A CBC News segment features a reporter in studio speaking with a female correspondent about the school fire. The correspondent states she has spoken with Chief Lukin. The segment opens with exterior shots of the snowy community, showing the damaged school and a vehicle passing the wreckage, underscoring the community’s ongoing struggle and recovery efforts.
```

**txt9**

```
[video-level knowledge | semantic] (former school, is being cleaned up, after fire destruction)
```

**txt10**

```
[video-level knowledge | semantic] (Joshua Liendo, is a, Canadian male elite swimmer)
```

**txt11**

```
[video-level knowledge | semantic] (Dr. Christopher Labos, discusses, risks of community spread of measles)
```

**txt12**

```
[video-level knowledge | semantic] (Eabametoong First Nation, feels, heavy loss)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:39:15 | 00:39:10–00:39:20 | `54k2g9ddy4M:visual:00391000` | `outputs/p9p19_check_20261025_141401/frames_s2/54k2g9ddy4M/00391000.jpg` |
| img2 |  | 00:39:35 | 00:39:30–00:39:40 | `54k2g9ddy4M:visual:00393000` | `outputs/p9p19_check_20261025_141401/frames_s2/54k2g9ddy4M/00393000.jpg` |
| img3 |  | 00:39:45 | 00:39:40–00:39:50 | `54k2g9ddy4M:visual:00394000` | `outputs/p9p19_check_20261025_141401/frames_s2/54k2g9ddy4M/00394000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:39:10-00:39:20 | video frame at 2355.0s] The video shows the aftermath of a fire that destroyed a school, with the charred remains visible under a cloudy sky, alongside Canadian and First Nation flags. The scene then transitions to a modern, newly constructed school building at Pikangikum First Nation in June 2023, with numerous vehicles parked in front. The accompanying narration discusses the urgency for action, noting that the community waited a decade for a new school after the previous one was destroyed.
```

**img2**

```
[00:39:30-00:39:40 | video frame at 2375.0s] The video segment shows scenes related to the destruction of a school in Wapakika First Nation and the ongoing water issues in Iyabmatan First Nation. It begins with a shot of people seated in a gymnasium, likely attending a ceremony. The video then cuts to the sign for "The Rev. Eleazar Winter Memorial School," followed by footage of a large fire at night, illustrating the school's destruction. The segment transitions to a snowy street scene in a remote community, and concludes with shots of a sign for the "Eabametoong First Nation Water Treatment Plant," highlighting the long-standing boil water advisory affecting the community. The accompanying narration references the school's rebuilding after being destroyed and the ongoing water advisory.
```

**img3**

```
[00:39:40-00:39:50 | video frame at 2385.0s] The video shows a snowy, remote First Nation community, with shots of buildings and a road covered in snow. A yellow pedestrian crossing sign is visible, and in one frame, two people are walking through the snow, one pulling a child’s sled. The on-screen text reads, “Remote First Nation feels heavy loss after fire destroys school,” while the accompanying audio discusses the community’s long-standing challenges with infrastructure, including a boil water advisory since 2002, and their determination to ensure youth continue receiving education despite lacking proper fire and water services and housing.
```
