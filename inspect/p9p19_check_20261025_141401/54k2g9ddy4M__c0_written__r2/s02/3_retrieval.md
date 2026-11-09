# Section 2 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:22:25): `{'video_id': '54k2g9ddy4M', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 18, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 5.51}`
- image request (2026-10-25 14:22:29): `{'video_id': '54k2g9ddy4M', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 1.24}`
- L1 filter LLM call: prompt 6510 tokens, output 66 tokens, 4.3 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 10min | 00:00:00–00:10:00 | 1 / 0.04918 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10min_0` |
| txt2 | ✓ | worldmm-episodic | 3min | 00:00:00–00:03:00 | 2 / 0.032522 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:3min_0` |
| txt3 | ✓ | worldmm-episodic | 3min | 00:03:00–00:06:00 | 3 / 0.048916 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:3min_1` |
| txt4 |  | worldmm-episodic | 30sec | 00:02:00–00:02:30 | 4 / 0.032522 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_4` |
| txt5 | ✓ | worldmm-episodic | 10sec | 00:04:40–00:04:50 | 5 / 0.032522 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_28` |
| txt6 |  | worldmm-episodic | 30sec | 00:04:00–00:04:30 | 6 / 0.032002 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_8` |
| txt7 | ✓ | worldmm-episodic | 10sec | 00:04:50–00:05:00 | 7 / 0.032002 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_29` |
| txt8 | ✓ | worldmm-episodic | 30sec | 00:04:30–00:05:00 | 8 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_9` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_9` |
| txt10 | ✓ | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_77` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_74` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016129 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_10` |

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
[00:03:00-00:06:00 | episodic 3min] **Measles Outbreak Alert Across U.S. and Canada**  
A measles outbreak in the U.S., with 41 confirmed cases across 16 states, centers on Manatee Bay Elementary near Fort Lauderdale, posing heightened risk to unvaccinated and immunocompromised children under one year. Parent Demi Cavanaugh expresses concern for her unvaccinated son, while her vaccinated daughter remains protected. Public health officials warn of potential spread into Canadian communities, prompting CBC News to issue urgent vaccination advisories. Anchors and medical experts stress the importance of early vaccination (as early as nine months) and maternal antibodies for infant protection, urging consultation with healthcare providers. Visuals include vaccine administration, school aerial shots, and community anxiety, reinforced by persistent on-screen alerts.

**Quebec Hospital Waiting Room Tragedy Under Investigation**  
A third patient death in a Montreal hospital waiting room is under coroner’s review, following a prior fatality caused by a 45-minute ambulance delay. Authorities are probing systemic resource shortages, with medical professionals warning that without increased emergency vehicle deployment, similar tragedies are inevitable. Footage shows hospital corridors, triage areas, and paramedics preparing ambulances, underscoring strained emergency response. This domestic crisis is juxtaposed with international coverage of U.S. Vice President Kamala Harris’s Gaza ceasefire appeal, broadcast alongside footage of conflict and aid deployment.

**Protest Disrupts Prime Minister’s Toronto Event**  
A large nighttime protest outside the Art Gallery of Ontario on March 2, featuring Palestinian flags and demands for political action, led to the cancellation of a scheduled Prime Minister’s event. Police were present, and media coverage highlighted the disruption and ongoing investigation into the incident. Footage captured the scale and tension of the demonstration, emphasizing its impact on high-profile political scheduling and public discourse.
```

**txt4**

```
[00:02:00-00:02:30 | episodic 30sec] Measles is resurging in Canadian communities, prompting public health officials to investigate potential cases and trace transmission chains, as the virus—highly contagious and airborne—can linger in hospitals and waiting rooms, exposing new individuals. Dr. Earl Rubin from Montreal Children’s Hospital questions the outbreak’s origin and potential spread, while Dr. Anna Banerji, a pediatric infectious diseases specialist in Parry Sound, Ontario, explains the virus’s environmental persistence and the importance of vaccination. Footage shows healthcare workers administering the measles-mumps-rubella (MMR) vaccine and close-ups of measles rash, underscoring prevention efforts. Canada officially eliminated measles in 1998, but declining vaccination rates have contributed to its return.
```

**txt5** (cited)

```
[00:04:40-00:04:50 | episodic 10sec] A man in a white shirt with a red collar speaks during a video interview, warning that if patient transportation isn't prioritized by adding vehicles, similar tragic events are certain to recur in the future. The scene then cuts to a low-angle shot of a hospital hallway, where a gurney is visible and medical staff in scrubs walk in the background. A news banner at the bottom of the screen reads, "Coroner investigating 3rd death in Quebec hospital waiting room."
```

**txt6**

```
[00:04:00-00:04:30 | episodic 30sec] **Measles Vaccination Guidance and Outbreak Alert**  
A CBC News segment features a female anchor in a white top discussing measles vaccinations, noting that children can receive the shot as early as nine months and that schedules may be adjusted for higher-risk individuals. The on-screen graphic warns that “Officials say measles may be spreading in Canadian communities.” The segment transitions to a split-screen, where a male anchor in a suit listens as reporter Katie Nicholson, based in Toronto, elaborates on outbreak precautions, advising viewers to avoid locations with known measles cases. The segment concludes with Nicholson’s full-screen appearance as the anchor’s side fades.

**Quebec Hospital Waiting Room Death Under Coroner’s Review**  
A male news anchor in a suit and tie delivers a report against a cityscape backdrop, detailing a Quebec coroner’s investigation into the death of a patient who waited 45 minutes for an ambulance in a Montreal hospital. A lower-third graphic identifies the case as “Coroner investigating 3rd death in Quebec hospital waiting room,” highlighting ongoing scrutiny of emergency response protocols in the province.
```

**txt7** (cited)

```
[00:04:50-00:05:00 | episodic 10sec] The video segment begins with a view of a hospital room, showing medical equipment including a Philips ultrasound monitor, with a patient on a gurney in the background and a person standing nearby. The scene then cuts to a hospital hallway where a person in a purple uniform walks past hospital beds. The segment transitions to a news studio, where a male news anchor in a suit and tie speaks to the camera. Behind him, a screen displays footage of a woman speaking at a podium with the seal of the President of the United States. On-screen text identifies the news story as “Coroner investigating 3rd death in Quebec hospital waiting room” and later, “U.S. vice-president calls for ‘immediate ceasefire’ in Gaza.”
```

**txt8** (cited)

```
[00:04:30-00:05:00 | episodic 30sec] A Quebec hospital is under scrutiny after a third patient died while waiting in a waiting room, with authorities investigating the circumstances. The incident follows a prior death caused by a 45-minute delay in ambulance response due to insufficient resources, prompting warnings from medical professionals that without prioritizing patient transport—through increased vehicle deployment—similar tragedies are inevitable. Footage shows hospital corridors, triage signs, and paramedics preparing an ambulance, underscoring the systemic strain. Meanwhile, a U.S. vice-president calls for an immediate ceasefire in Gaza, as broadcasted in a separate news segment, while a Canadian news anchor reports on the Quebec case, juxtaposing domestic healthcare crises with international affairs.
```

**txt9**

```
[video-level knowledge | semantic] (child’s back, shows, measles rash)
```

**txt10** (cited)

```
[video-level knowledge | semantic] (man in white shirt with red collar, warns about, patient transportation prioritization)
```

**txt11**

```
[video-level knowledge | semantic] (3rd death in Quebec hospital waiting room, occurred in, hospital waiting room)
```

**txt12**

```
[video-level knowledge | semantic] (graphic, displays text, New measles infect)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 | ✓ | 00:00:55 | 00:00:50–00:01:00 | `54k2g9ddy4M:visual:00005000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00005000.jpg` |
| img2 | ✓ | 00:01:15 | 00:01:10–00:01:20 | `54k2g9ddy4M:visual:00011000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00011000.jpg` |
| img3 | ✓ | 00:00:05 | 00:00:00–00:00:10 | `54k2g9ddy4M:visual:00000000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00000000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1** (cited)

```
[00:00:50-00:01:00 | video frame at 55.0s] A news anchor in a suit and tie speaks on a television set, with graphics behind him showing medical imagery including virus particles and vaccine vials. The on-screen text identifies the program as "The National" and the network as CBC News. The anchor discusses signs that measles may be spreading in Canadian communities.
```

**img2** (cited)

```
[00:01:10-00:01:20 | video frame at 75.0s] A news segment from CBC News discusses measles infections in Canada, showing a graphic of a map with two marked locations — one in Quebec and one in Ontario — indicating cases that are not linked to travel or other known cases. The on-screen text states "At least 13 infections" and "Officials say measles may be spreading in Canadian communities." The segment transitions to a news anchor speaking, with the same lower-third text visible, as he explains that doctors believe a massive outbreak is unlikely.
```

**img3** (cited)

```
[00:00:00-00:00:10 | video frame at 5.0s] A news anchor in a suit speaks on a studio set with a cityscape backdrop, introducing a report on rising measles cases in Quebec. The segment transitions to a graphic for "The National" and then to a close-up of a child’s back showing measles rash, with the text "New measles infect" visible.
```
