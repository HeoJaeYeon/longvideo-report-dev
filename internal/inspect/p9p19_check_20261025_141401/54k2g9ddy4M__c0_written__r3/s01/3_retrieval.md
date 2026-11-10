# Section 1 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:26:51): `{'video_id': '54k2g9ddy4M', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 24, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 5.76}`
- image request (2026-10-25 14:26:55): `{'video_id': '54k2g9ddy4M', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 1.46}`
- L1 filter LLM call: prompt 8269 tokens, output 68 tokens, 4.6 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 10min | 00:00:00–00:10:00 | 1 / 0.04918 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10min_0` |
| txt2 | ✓ | worldmm-episodic | 3min | 00:00:00–00:03:00 | 2 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:3min_0` |
| txt3 | ✓ | worldmm-episodic | 30sec | 00:03:30–00:04:00 | 3 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_7` |
| txt4 | ✓ | worldmm-episodic | 30sec | 00:00:30–00:01:00 | 4 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_1` |
| txt5 | ✓ | worldmm-episodic | 30sec | 00:05:30–00:06:00 | 5 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_11` |
| txt6 | ✓ | worldmm-episodic | 10sec | 00:05:40–00:05:50 | 6 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_34` |
| txt7 | ✓ | worldmm-episodic | 3min | 00:33:00–00:36:00 | 7 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:3min_11` |
| txt8 | ✓ | worldmm-episodic | 30sec | 00:34:00–00:34:30 | 8 / 0.015873 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_68` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_65` |
| txt10 | ✓ | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_113` |
| txt11 | ✓ | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_457` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016129 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_66` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:00:00-00:10:00 | episodic 10min] **Measles Resurgence Sparks Public Health Alarm Across Canada and U.S.**  
Confirmed measles cases in Quebec and Ontario — unlinked to travel or known outbreaks — signal potential community transmission. Though officials rule out a massive outbreak, the virus’s high contagiousness and airborne persistence raise urgent concern. Dr. Earl Rubin and Dr. Anna Banerji emphasize the mystery of the outbreak’s origin and the risks posed by declining vaccination rates. Canada eliminated measles in 1998, but current immunization levels — 79% of seven-year-olds vaccinated by 2021 — fall short of the 95% herd immunity threshold. Dr. Christopher Labos warns that once transmission begins, outbreaks escalate, particularly endangering young children and immunocompromised individuals. Visuals juxtapose vaccine administration, microscopic virus particles, and children in public spaces with on-screen alerts reinforcing the threat. The segment concludes with a CBC News title card for “The National,” underscoring the need for public health vigilance.

**Pro-Palestinian Protests Disrupt Prime Minister’s Event and Spark Political Fallout**  
A large nighttime protest outside the Art Gallery of Ontario on March 2, featuring Palestinian flags and demands for political action, led to the cancellation of a scheduled Prime Minister’s event. Demonstrators, including a man in a keffiyeh who publicly accused Minister Ahmed Housson of complicity in a family murder, drew police in riot gear and mounted officers. The demonstration, calling for an end to Canada’s involvement in Gaza, forced the cancellation and triggered an official police investigation. No arrests or injuries were reported, but the event’s disruption fueled political backlash, with Liberal MP Marco Mendocino calling it a “loss of public support.” Community activist Aisha Sherazi and public safety expert Pierre-Yves Bourduas urged caution, warning of diplomatic fallout and escalating security risks. Former Clerk of the Privy Council Michael Wernick highlighted rising security costs — nearing $3 million monthly — as protests pressure the PM and prompt some politicians to reconsider candidacy. Meanwhile, Donald Trump dominates Super Tuesday, projected to win nearly all Republican primaries, with massive rallies in Greensboro and Richmond. Supporters wave “TRUMP 2024” flags and chant, reinforcing his momentum.

**Joshua Liendo’s Olympic Ascent Amid Public Health and Political Turmoil**  
Canadian swimmer Joshua Liendo competes in a butterfly race, showcasing his technique across lanes. Post-race, he reflects on his trailblazing role for Black swimmers and the surreal nature of his rise. Footage includes his training, poolside moments, and interview segments, underscored by commentary on his Olympic potential. The segment cuts back to “The National,” where anchors report on measles, reinforcing the dual narrative of athletic achievement and public health urgency. The juxtaposition highlights how national priorities — sport, health, and politics — intersect in the public sphere.

**Everyday Life Under Measles Threat and Systemic Crisis**  
A father swings a child at a Toronto playground as a news ticker warns of measles spread — contrasting normalcy with urgency. Scenes shift to Montreal streets and stadium crowds, with fragmented audio reflecting public anxiety. Dr. Rubin’s statement that the situation reflects “only the tip of the iceberg” underscores the scale of the threat. Meanwhile, a third patient death in a Montreal hospital waiting room is under coroner’s review, following a prior fatality caused by a 45-minute ambulance delay. Authorities are probing systemic resource shortages, with medical professionals warning that without increased emergency vehicle deployment, similar tragedies are inevitable. Footage shows hospital corridors, triage areas, and paramedics preparing ambulances, underscoring strained emergency response. This domestic crisis is juxtaposed with international coverage of U.S. Vice President Kamala Harris’s Gaza ceasefire appeal, broadcast alongside footage of conflict and aid deployment.

**Measles Outbreak Alert Expands to U.S. and Canada**  
A measles outbreak in the U.S., with 41 confirmed cases across 16 states, centers on Manatee Bay Elementary near Fort Lauderdale, posing heightened risk to unvaccinated and immunocompromised children under one year. Parent Demi Cavanaugh expresses concern for her unvaccinated son, while her vaccinated daughter remains protected. Public health officials warn of potential spread into Canadian communities, prompting CBC News to issue urgent vaccination advisories. Anchors and medical experts stress the importance of early vaccination (as early as nine months) and maternal antibodies for infant protection, urging consultation with healthcare providers. Visuals include vaccine administration, school aerial shots, and community anxiety, reinforced by persistent on-screen alerts.

**Canada’s Airline Industry Faces Rising Costs Amid Falling Fares**  
Travelers face escalating ancillary fees despite falling fares. Flair Airlines charges cancellation fees exceeding ticket prices — such as $84 on a $667.21 bill — while Air Canada and WestJet raise economy baggage fees by $5–$35. Visuals of passengers, airport counters, and aircraft underscore the financial burden, contrasted with a family playing Uno at home, illustrating the ripple effect on everyday life. The report ends with CBC anchor Katie Simpson identifying herself and location, while the studio anchor continues the airfare trend discussion.

**Trump’s Super Tuesday Dominance and Legal Challenges**  
Donald Trump is shown at a rally under a large screen reading “FLORIDA IS TRUMP COUNTRY,” reinforcing his campaign narrative of dominance in key states. Polls from CBS News/YouGov and the New York Times/Siena College show Trump leading Biden (52% to 37–42%), with 73% of voters deeming Biden too old to be effective — a key perception gap. Visuals consistently reinforce Trump’s projected sweep of Super Tuesday primaries, including a split-screen comparison of the candidates and a news ticker repeating the narrative.  

Nikki Haley, at a campaign event, waves to supporters and poses for selfies amid flags, while a brief embrace with a man underscores the political moment. A CBC News segment features anchor Katie Simpson in Washington, reporting on legal challenges to Trump’s ballot eligibility in three states — tied to January 6 — noting judicial trends favor his inclusion, which is expected to energize his campaign. The segment includes a split-screen discussion on Supreme Court rulings potentially disqualifying him, with Simpson in an orange blazer against a blurred White House backdrop.
```

**txt2** (cited)

```
[00:00:00-00:03:00 | episodic 3min] **Measles resurgence in Canada sparks public health alarm.**  
Confirmed cases in Quebec and Ontario—unlinked to travel or known outbreaks—signal potential community spread. Though officials deem a massive outbreak unlikely, the virus’s high contagiousness and airborne persistence raise concern. Dr. Earl Rubin and Dr. Anna Banerji highlight the mystery of the outbreak’s origin and the risks posed by declining vaccination rates. Canada eliminated measles in 1998, but current rates—79% of seven-year-olds vaccinated by 2021—fall short of the 95% herd immunity threshold. Dr. Christopher Labos warns that once transmission begins, outbreaks escalate, particularly endangering young children and immunocompromised individuals. Visuals of vaccine administration, virus particles, and children in public spaces juxtapose daily life with looming health threats. The segment concludes with a microscopic view of the measles virus and a CBC News title card for “The National,” underscoring the urgency of public health vigilance.

**Pro-Palestinian protest halts Prime Minister’s event.**  
Demonstrators disrupt a scheduled event outside a building, forcing its cancellation. Footage captures tense scenes of protesters, police presence, and the abrupt termination of the event. The scene transitions to “The National,” where the measles outbreak report resumes, maintaining narrative continuity.

**Joshua Liendo’s Olympic journey.**  
Canadian swimmer Joshua Liendo competes in a butterfly race, showcasing his technique across lanes. Post-race, he reflects on his trailblazing role for Black swimmers and the surreal nature of his rise. Footage includes his training, poolside moments, and interview segments, underscored by commentary on his Olympic potential. The segment cuts to “The National,” where a CBC anchor reports on measles, reinforcing the segment’s dual focus on sport and public health.

**Everyday life amid public health warnings.**  
A father swings a child at a Toronto playground, while a news ticker warns of measles spread—contrasting normalcy with urgency. Scenes shift to Montreal streets and stadium crowds, with fragmented audio reflecting public anxiety. Dr. Rubin’s statement that the situation reflects “only the tip of the iceberg” underscores the scale of the threat.
```

**txt3** (cited)

```
[00:03:30-00:04:00 | episodic 30sec] **Measles outbreaks are raising public health concerns in Canadian communities, prompting CBC News to issue urgent vaccination advisories.** The segment features anchor Katie Nicholson in a studio setting, alongside field reporting from Toronto, where she and a medical expert discuss the evolving landscape of measles transmission and the importance of vaccination—particularly for vulnerable populations such as adults with compromised immune systems due to chemotherapy or chronic illness. The broadcast emphasizes the role of maternal antibodies in infant protection and urges viewers to consult healthcare providers about immunization status. A persistent lower third graphic reinforces the public health alert: “Officials say measles may be spreading in Canadian communities.” The segment alternates between studio interviews and on-the-ground visuals, including a playground scene with a child and adult, underscoring the real-world impact on families and communities.
```

**txt4** (cited)

```
[00:00:30-00:01:00 | episodic 30sec] Joshua Liendo, a Canadian swimmer, competes in a swimming race, showcasing his butterfly stroke technique across lanes, before transitioning to interview segments where he reflects on his journey as a trailblazer for Black swimmers and expresses the surreal nature of his rise to prominence. The footage captures his preparation, intense racing, and post-race moments poolside and in the water wearing a Canadian swim cap, all underscored by commentary highlighting his potential Olympic impact. The segment concludes with a cut to CBC News’ “The National,” hosted by Ian Henneman, where a female anchor delivers a report on the resurgence of measles in Canadian communities, supported by on-screen medical graphics including virus particles and vaccine vials.
```

**txt5** (cited)

```
[00:05:30-00:06:00 | episodic 30sec] **Protest Outside the Art Gallery of Ontario Leads to Cancellation of Prime Minister’s Event**  
A large-scale nighttime demonstration unfolds outside the Art Gallery of Ontario in Toronto on March 2, with protesters holding Palestinian flags and signs, demanding political action. Police are visibly present, engaging with the crowd as attendees record the event on their phones. The protest’s intensity reportedly prompted authorities to cancel a scheduled event featuring the Prime Minister, prompting media coverage. A news anchor in a studio reports on the incident, with on-screen graphics reinforcing the disruption and police investigation into the circumstances surrounding the cancellation. The footage captures the scale and tension of the demonstration, underscoring its impact on high-profile political scheduling.
```

**txt6** (cited)

```
[00:05:40-00:05:50 | episodic 10sec] A news anchor in a suit speaks on camera in a studio, with a split screen showing footage of a protest outside the Art Gallery of Ontario. The protest features a crowd of people holding signs and Palestinian flags. A lower third graphic reads, “Police investigating after protest forces PM to cancel event.” At 00:05:48, the view switches to a full-screen shot of the protest, and a location and date overlay appears: “Toronto March 2.”
```

**txt7** (cited)

```
[00:33:00-00:36:00 | episodic 3min] Joshua Liendo, dressed in a white Florida Gators shirt and gold chain, reflects on his journey as a rising Olympic swimmer while standing in an indoor pool facility, framed by CBC News’ headline “Joshua Liendo swims into the history books.” He draws inspiration from athletes like Allen Iverson, acknowledging their influence on his athletic and personal development. The segment intercuts his reflections with archival footage of Iverson, highlighting his iconic dunks and tattoos, while also weaving in his parents’ basketball passion and his interest in a documentary — all reinforcing his evolving identity as both athlete and role model.

Liendo speaks candidly with a suited interviewer in the pool facility, discussing gender disparities in swimming and his own path to Olympic qualification. He references past relay finals and a missed individual final, expressing cautious optimism about the unpredictable nature of elite competition. The narrative emphasizes his focus on the present, urging himself and his team to maintain control over immediate goals rather than prematurely anticipating future milestones.

The video alternates between Liendo’s reflections and race footage, showcasing his historic first international gold in the 100-meter butterfly at the Doha World Championships. Scenes capture him mid-stroke, adjusting goggles post-race, and emerging triumphant from the pool — his cap bearing Yakult and Speedo logos, with Omega branding visible. A Canadian coach in a red “CANADA” shirt raises his fist in celebration, underscoring the national victory and building momentum toward the Paris Olympics.

The segment concludes with Liendo smiling warmly at the anchor, reinforcing his pride and humility. A brief, unrelated graphic of a burning building appears, serving as a dramatic visual transition — though its thematic connection remains unexplained. Throughout, the narrative blends personal narrative, athletic achievement, and public responsibility, cementing Liendo’s emergence as a historic figure in Canadian swimming.
```

**txt8** (cited)

```
[00:34:00-00:34:30 | episodic 30sec] Joshua Liendo, dressed in a white Florida Gators shirt and gold chain, speaks emotionally in front of an indoor pool, reflecting on the personal and athletic challenges of stepping up to elite competition — particularly celebrating his son Finley’s historic first international gold medal. The on-screen text “Joshua Liendo swims into the history books” underscores the milestone, while the CBC News logo confirms the broadcast context. The scene transitions to race footage, showing swimmers in action with red lane dividers, then focuses on Liendo adjusting his goggles post-race — his cap bearing Yakult and Speedo logos, with an Omega logo visible on the pool wall — reinforcing the high-level, professional setting of the competition. Audio narration confirms this is Liendo’s first international gold at a high-level long-course championship. In the final shot, Liendo emerges from the pool with a wide, triumphant smile, as a Canadian coach in a red “CANADA” shirt raises his fist in celebration — signaling Canada’s gold medal victory at the Doha World Championships and building momentum toward the upcoming Olympics.
```

**txt9**

```
[video-level knowledge | semantic] (officials, say, measles may be spreading in Canadian communities)
```

**txt10** (cited)

```
[video-level knowledge | semantic] (PM, had event cancelled, due to protest)
```

**txt11** (cited)

```
[video-level knowledge | semantic] (Joshua Liendo, wears, gold chain)
```

**txt12**

```
[video-level knowledge | semantic] (measles, may be spreading in, Canadian communities)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 | ✓ | 00:05:55 | 00:05:50–00:06:00 | `54k2g9ddy4M:visual:00055000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00055000.jpg` |
| img2 | ✓ | 00:06:45 | 00:06:40–00:06:50 | `54k2g9ddy4M:visual:00064000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00064000.jpg` |
| img3 | ✓ | 00:05:45 | 00:05:40–00:05:50 | `54k2g9ddy4M:visual:00054000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00054000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1** (cited)

```
[00:05:50-00:06:00 | video frame at 355.0s] A nighttime protest unfolds in Toronto, with demonstrators gathered outside the Ontario Museum of Fine Arts, holding Palestinian flags and signs. Police officers are present, interacting with the crowd as people record the event on their phones. The scene captures the tension and activity of the protest, which reportedly led to the cancellation of a Prime Minister’s event.
```

**img2** (cited)

```
[00:06:40-00:06:50 | video frame at 405.0s] Police on horseback are seen on a city street at night, with a CBC News banner at the bottom reading, “Police investigating after protest forces PM to cancel event.” The camera pans to show parked vehicles and orange traffic cones near a brick building. The scene then shifts to a crowd of protesters gathered outside the “MUSÉE DES BEAUX ARTS DE MONTRÉAL,” holding signs and Palestinian flags. A text overlay appears, stating, “People want to show,” followed by “Ghassan, Protest organizer.” The audio includes a voiceover: “Toronto police say no one was injured or arrested, but they are investigating. ABC News. He would only give his first name, Kazan. People want to show the Canadian government that it needs to end its complicity in this genocide.”
```

**img3** (cited)

```
[00:05:40-00:05:50 | video frame at 345.0s] A news anchor in a suit speaks on camera in a studio, with a split screen showing footage of a protest outside the Art Gallery of Ontario. The protest features a crowd of people holding signs and Palestinian flags. A lower third graphic reads, “Police investigating after protest forces PM to cancel event.” At 00:05:48, the view switches to a full-screen shot of the protest, and a location and date overlay appears: “Toronto March 2.”
```
