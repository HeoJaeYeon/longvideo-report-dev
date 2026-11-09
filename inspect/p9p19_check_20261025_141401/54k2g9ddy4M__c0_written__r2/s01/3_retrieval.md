# Section 1 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:21:17): `{'video_id': '54k2g9ddy4M', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 25, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 11.35}`
- image request (2026-10-25 14:21:20): `{'video_id': '54k2g9ddy4M', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 1.26}`
- L1 filter LLM call: prompt 9826 tokens, output 65 tokens, 4.7 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 10min | 00:00:00–00:10:00 | 1 / 0.032787 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10min_0` |
| txt2 | ✓ | worldmm-episodic | 3min | 00:00:00–00:03:00 | 2 / 0.032522 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:3min_0` |
| txt3 | ✓ | worldmm-episodic | 30sec | 00:01:30–00:02:00 | 3 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_3` |
| txt4 | ✓ | worldmm-episodic | 10sec | 00:02:00–00:02:10 | 4 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_12` |
| txt5 | ✓ | worldmm-episodic | 30sec | 00:02:30–00:03:00 | 5 / 0.015873 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_5` |
| txt6 |  | worldmm-episodic | 10sec | 00:00:20–00:00:30 | 6 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_2` |
| txt7 | ✓ | worldmm-episodic | 3min | 00:06:00–00:09:00 | 7 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:3min_2` |
| txt8 | ✓ | worldmm-episodic | 30sec | 00:00:30–00:01:00 | 8 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_1` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_7` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_459` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_95` |
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
[00:01:30-00:02:00 | episodic 30sec] A man in a black jacket and beanie gently swings a small child in a pink snowsuit at a Toronto playground, while a news ticker warns that measles may be spreading in Canadian communities — juxtaposing everyday family life with public health concern.

The scene shifts to Benjamin Dermer, a bearded parent in a beanie, speaking outdoors near bare trees, followed by shots of crowded streets in Montreal and a stadium crowd, all under the same warning ticker, as fragmented audio conveys public anxiety and uncertainty about the measles outbreak.

The video then cuts to outdoor ice skating and a close-up of Dr. Earl Rubin from Montreal Children’s Hospital, who addresses the camera, stating that the measles situation reflects only the tip of the iceberg and questions the origin of the outbreak — underscoring the scale and mystery of the spread.
```

**txt4** (cited)

```
[00:02:00-00:02:10 | episodic 10sec] Dr. Earl Rubin from Montreal Children’s Hospital discusses the measles outbreak, questioning the origin of the virus and who else it may be spreading to. The segment cuts to a hospital scene where a medical professional in scrubs reviews paperwork near a patient cart. A news ticker at the bottom reads, “Officials say measles may be spreading in Canadian communities.”
```

**txt5** (cited)

```
[00:02:30-00:03:00 | episodic 30sec] **Measles vaccination rates in Canada remain below herd immunity thresholds, prompting public health warnings about potential community spread.**  
A healthcare worker administers the measles vaccine to a child, followed by close-ups of the vaccine vial and syringe, visually reinforcing the topic. On-screen text cites the Public Health Agency of Canada and WHO, noting that in 2021, only 79% of seven-year-olds in Canada had received two doses — falling short of the 95% threshold required to maintain herd immunity. A persistent lower third warns that officials say measles may be spreading in Canadian communities.  
A graphic reinforces the 95% vaccination benchmark needed for herd immunity, featuring the Priorix MMR vaccine. The segment then introduces Dr. Christopher Labos, an epidemiologist in Montreal, who explains that once community transmission begins, outbreaks are likely to escalate. He warns of increased severity and hospitalizations, particularly among young children, unvaccinated individuals, and those with compromised immune systems. The segment concludes with a microscopic image of the measles virus, visually underscoring the threat.
```

**txt6**

```
[00:00:20-00:00:30 | episodic 10sec] A pro-Palestinian protest outside a building leads to the cancellation of a Prime Minister's event, as shown by footage of demonstrators and police, followed by scenes of the event's cancellation and a transition to "The National" news program.
```

**txt7** (cited)

```
[00:06:00-00:09:00 | episodic 3min] **Protesters outside the Art Gallery of Ontario and Musée des Beaux-Arts de Montréal escalate tensions**, drawing police in riot gear and mounted officers, forcing cancellation of a Prime Minister’s event. A man in a keffiyeh publicly accuses Minister Ahmed Housson of complicity in a family murder, filmed by CBC. The demonstrations, demanding an end to Canada’s involvement in Gaza, are met with heightened security — including Liberal MP Marco Mendocino’s secure transit — and an official police investigation. No arrests or injuries reported, but political backlash ensues, with Mendocino calling the protests a “loss of public support.” A community activist, Aisha Sherazi, and public safety expert Pierre-Yves Bourduas urge caution, warning of diplomatic fallout and escalating risks. Former Clerk of the Privy Council Michael Wernick highlights rising security costs — nearing $3 million monthly — as protests pressure the PM and prompt some politicians to reconsider candidacy. Meanwhile, **Donald Trump dominates Super Tuesday**, projected to win nearly all Republican primaries, with massive rallies in Greensboro and Richmond. Supporters wave “TRUMP 2024” flags, chant, and display unwavering loyalty. Nikki Haley campaigns in Vermont, energizing crowds with a “NIKKI HALEY FOR PRESIDENT” banner, as CBC continues to track Trump’s momentum amid national political volatility.
```

**txt8** (cited)

```
[00:00:30-00:01:00 | episodic 30sec] Joshua Liendo, a Canadian swimmer, competes in a swimming race, showcasing his butterfly stroke technique across lanes, before transitioning to interview segments where he reflects on his journey as a trailblazer for Black swimmers and expresses the surreal nature of his rise to prominence. The footage captures his preparation, intense racing, and post-race moments poolside and in the water wearing a Canadian swim cap, all underscored by commentary highlighting his potential Olympic impact. The segment concludes with a cut to CBC News’ “The National,” hosted by Ian Henneman, where a female anchor delivers a report on the resurgence of measles in Canadian communities, supported by on-screen medical graphics including virus particles and vaccine vials.
```

**txt9**

```
[video-level knowledge | semantic] (measles infections, not linked to, other known cases)
```

**txt10**

```
[video-level knowledge | semantic] (Joshua Liendo, is interviewed about, buildup to an event)
```

**txt11**

```
[video-level knowledge | semantic] (Police, investigating, Pro-Palestinian protest)
```

**txt12**

```
[video-level knowledge | semantic] (measles, may be spreading in, Canadian communities)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 | ✓ | 00:02:15 | 00:02:10–00:02:20 | `54k2g9ddy4M:visual:00021000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00021000.jpg` |
| img2 | ✓ | 00:03:55 | 00:03:50–00:04:00 | `54k2g9ddy4M:visual:00035000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00035000.jpg` |
| img3 | ✓ | 00:02:05 | 00:02:00–00:02:10 | `54k2g9ddy4M:visual:00020000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00020000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1** (cited)

```
[00:02:10-00:02:20 | video frame at 135.0s] Public health officials are tracking down potential measles cases, while doctors explain the virus's high contagiousness and ability to linger in the air in places like hospitals and waiting rooms. The segment shows medical professionals handling a measles-mumps-rubella vaccine, a close-up of measles rash on a child’s skin, and an interview with Dr. Anna Banerji, a pediatric infectious diseases specialist in Parry Sound, Ontario.
```

**img2** (cited)

```
[00:03:50-00:04:00 | video frame at 235.0s] A news anchor, Katie Nicholson of CBC News, speaks in a studio setting, discussing public health advice regarding measles vaccinations and maternal antibodies in infants. The on-screen text notes that officials say measles may be spreading in Canadian communities.
```

**img3** (cited)

```
[00:02:00-00:02:10 | video frame at 125.0s] Dr. Earl Rubin from Montreal Children’s Hospital discusses the measles outbreak, questioning the origin of the virus and who else it may be spreading to. The segment cuts to a hospital scene where a medical professional in scrubs reviews paperwork near a patient cart. A news ticker at the bottom reads, “Officials say measles may be spreading in Canadian communities.”
```
