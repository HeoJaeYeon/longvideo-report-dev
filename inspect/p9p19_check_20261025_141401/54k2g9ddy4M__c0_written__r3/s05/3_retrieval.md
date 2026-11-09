# Section 5 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:30:48): `{'video_id': '54k2g9ddy4M', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 17, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 5.71}`
- image request (2026-10-25 14:30:51): `{'video_id': '54k2g9ddy4M', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 0.87}`
- L1 filter LLM call: prompt 6710 tokens, output 76 tokens, 4.5 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 10min | 00:30:00–00:40:00 | 1 / 0.04918 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10min_3` |
| txt2 | ✓ | worldmm-episodic | 30sec | 00:39:00–00:39:30 | 2 / 0.032522 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_78` |
| txt3 | ✓ | worldmm-episodic | 30sec | 00:38:30–00:39:00 | 3 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_77` |
| txt4 | ✓ | worldmm-episodic | 30sec | 00:36:30–00:37:00 | 4 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_73` |
| txt5 | ✓ | worldmm-episodic | 30sec | 00:37:30–00:38:00 | 5 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_75` |
| txt6 | ✓ | worldmm-episodic | 10sec | 00:38:50–00:39:00 | 6 / 0.032522 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_233` |
| txt7 |  | worldmm-episodic | 10sec | 00:39:00–00:39:10 | 7 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_234` |
| txt8 | ✓ | worldmm-episodic | 10sec | 00:39:10–00:39:20 | 8 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_235` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.04918 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_499` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.048387 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_570` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.047619 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_579` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.046875 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_564` |

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
[00:39:00-00:39:30 | episodic 30sec] **[Event Summary]**  
A fire destroyed a school at a remote First Nation community, leaving behind charred ruins and prompting widespread grief — as captured in footage showing the collapsed metal roof under a cloudy sky, alongside Canadian and First Nation flags. In response, the federal government pledged full support for rebuilding, with a senior official stating the commitment to stand with the community in constructing a new permanent school.  

**[Event Summary]**  
In June 2023, Pikangikum First Nation unveiled its newly constructed school — a modern facility with vehicles parked outside — symbolizing a decade-long wait for replacement after the original school was lost to fire. The narration underscores the urgency of the rebuild, highlighting the community’s prolonged struggle for educational infrastructure.  

**[Event Summary]**  
By September 2023, Wapekeka First Nation celebrated the grand opening of its new school — a colorful, modern building with festive decorations inside, including balloons and banners. The event marked the culmination of an eight-year wait following the destruction of its prior school by fire, showcasing the community’s resilience and the government’s eventual delivery on long-delayed promises.
```

**txt3** (cited)

```
[00:38:30-00:39:00 | episodic 30sec] **[Event 1: Aerial and Ground Views of Fire-Damaged School]**  
The video opens with an aerial shot from an airplane, revealing a snowy landscape dotted with dark water patches and a small snow-covered island, with the plane’s wing visible. The scene cuts to ground level, where a man in a dark jacket and red cap stands before the charred ruins of a burned building, gesturing as he speaks to an off-camera interviewer. A red fire hydrant is nearby. On-screen text reads: “Remote First Nation feels heavy loss after fire destroys school.” The man’s somber tone and gestures emphasize the devastation, as the audio includes his voiceover: “an emergency and a crisis for our children.”

**[Event 2: Reporter Joins Interview and Scene Expands]**  
A female reporter in a grey beanie and dark coat joins the man, and they walk together across the snow-covered terrain, passing a playground structure in the background. The scene reinforces the emotional weight of the loss, with visuals of the collapsed building, twisted metal roofing, and scattered debris. The on-screen caption reiterates: “Remote First Nation feels heavy loss after fire destroys school.”

**[Event 3: Government Response and Reconstruction Plan Announced]**  
The video transitions to narration explaining that after leaving Iyabmikam, the Federal Minister of Indigenous Services met with the chief in Thunder Bay to confirm the government’s plan to allocate over $13 million to construct five modular buildings as temporary classrooms for the community. This marks the official response to the crisis, aimed at restoring educational services for the affected First Nation children.
```

**txt4** (cited)

```
[00:36:30-00:37:00 | episodic 30sec] The video documents the aftermath of a devastating school fire in Eabametoong First Nation, Northwestern Ontario, showing charred ruins under snow and flags flown at half-mast as the community mourns. A news anchor in studio coverage highlights the community’s grief and uncertainty over rebuilding, while footage transitions between solemn exterior shots of the damaged school and interior scenes of students in hoodies attentively engaged in class — a stark contrast to the destruction outside. The narrative underscores the community’s resilience and the urgent need to restore their educational infrastructure, with visuals reinforcing the loss and the hope for renewal.
```

**txt5** (cited)

```
[00:37:30-00:38:00 | episodic 30sec] A devastating fire destroyed a school on the Eabametong First Nation, overwhelming the community’s capacity to respond despite the presence of a fire truck. The blaze left behind charred ruins blanketed in snow, prompting a somber reflection on the loss. A woman, likely a community member or reporter, speaks to the camera in front of the wreckage, while on-screen text notes that four teenagers have been charged in connection with the fire. The scene shifts to an interview with Chief Solomon Atlookan, who stands beside a red fire hydrant, emphasizing that even with operational firefighting equipment, the lack of adequate water infrastructure severely limited their ability to contain the fire — a critical factor in the building’s destruction. The chief’s remarks underscore the systemic challenges faced by remote Indigenous communities in emergency response.
```

**txt6** (cited)

```
[00:38:50-00:39:00 | episodic 10sec] The video shows the aftermath of a fire that destroyed a school in a remote First Nation community, with shots of the charred and collapsed structure, including twisted metal roofing and debris scattered across snow-covered ground. The accompanying narration explains that after leaving Iyabmikam, the Federal Minister of Indigenous Services met with the chief in Thunder Bay to confirm the government’s plan to spend over $13 million on five modular buildings to serve as temporary classrooms for the community.
```

**txt7**

```
[00:39:00-00:39:10 | episodic 10sec] The video shows the aftermath of a fire that destroyed a school, with frames displaying the charred and collapsed metal roof of the building. The scene then cuts to a woman with white hair and glasses speaking. On-screen text from the Office of the Minister of Indigenous Services quotes her saying, “...wholeheartedly with the community and will be there to support them in building their new permanent school.” The lower third of the screen reads, “Remote First Nation feels heavy loss after fire destroys school | CBCNEWS.”
```

**txt8** (cited)

```
[00:39:10-00:39:20 | episodic 10sec] The video shows the aftermath of a fire that destroyed a school, with the charred remains visible under a cloudy sky, alongside Canadian and First Nation flags. The scene then transitions to a modern, newly constructed school building at Pikangikum First Nation in June 2023, with numerous vehicles parked in front. The accompanying narration discusses the urgency for action, noting that the community waited a decade for a new school after the previous one was destroyed.
```

**txt9**

```
[video-level knowledge | semantic] (Eabametoong First Nation, is a, First Nation)
```

**txt10**

```
[video-level knowledge | semantic] (First Nation, experienced, heavy loss)
```

**txt11**

```
[video-level knowledge | semantic] (First Nation, experienced, heavy loss)
```

**txt12**

```
[video-level knowledge | semantic] (Eabametoong First Nation, feels, heavy loss)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:36:45 | 00:36:40–00:36:50 | `54k2g9ddy4M:visual:00364000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00364000.jpg` |
| img2 |  | 00:36:55 | 00:36:50–00:37:00 | `54k2g9ddy4M:visual:00365000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00365000.jpg` |
| img3 |  | 00:06:45 | 00:06:40–00:06:50 | `54k2g9ddy4M:visual:00064000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00064000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:36:40-00:36:50 | video frame at 2205.0s] A news anchor in a studio speaks about the challenges faced by a First Nation in Northwestern Ontario to restore their school, with images of flags and a damaged building shown. The segment transitions to footage of three flags flying above a building in Eabametoong First Nation, with a lower third identifying the location and noting the community’s heavy loss after a fire destroyed the school.
```

**img2**

```
[00:36:50-00:37:00 | video frame at 2215.0s] The video opens with an exterior shot of a school building in Eabametoong First Nation, where flags fly against a clear blue sky. The scene then transitions to the interior of a classroom, where students in hoodies are seated at desks, attentively watching a presentation on a large screen. A teacher stands at the front of the room, guiding the lesson, while another adult in an orange shirt moves around the classroom. The on-screen text indicates the story is about the community’s heavy loss following a fire that destroyed the school.
```

**img3**

```
[00:06:40-00:06:50 | video frame at 405.0s] Police on horseback are seen on a city street at night, with a CBC News banner at the bottom reading, “Police investigating after protest forces PM to cancel event.” The camera pans to show parked vehicles and orange traffic cones near a brick building. The scene then shifts to a crowd of protesters gathered outside the “MUSÉE DES BEAUX ARTS DE MONTRÉAL,” holding signs and Palestinian flags. A text overlay appears, stating, “People want to show,” followed by “Ghassan, Protest organizer.” The audio includes a voiceover: “Toronto police say no one was injured or arrested, but they are investigating. ABC News. He would only give his first name, Kazan. People want to show the Canadian government that it needs to end its complicity in this genocide.”
```
