# Section 6 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:25:34): `{'video_id': '54k2g9ddy4M', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 26, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 6.12}`
- image request (2026-10-25 14:25:37): `{'video_id': '54k2g9ddy4M', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 1.36}`
- L1 filter LLM call: prompt 9407 tokens, output 73 tokens, 4.9 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 10min | 00:00:00–00:10:00 | 1 / 0.032787 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10min_0` |
| txt2 | ✓ | worldmm-episodic | 10sec | 00:04:40–00:04:50 | 2 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_28` |
| txt3 | ✓ | worldmm-episodic | 10sec | 00:04:20–00:04:30 | 3 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_26` |
| txt4 | ✓ | worldmm-episodic | 10sec | 00:04:30–00:04:40 | 4 / 0.015873 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_27` |
| txt5 | ✓ | worldmm-episodic | 30sec | 00:05:00–00:05:30 | 5 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_10` |
| txt6 | ✓ | worldmm-episodic | 30sec | 00:20:00–00:20:30 | 6 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_40` |
| txt7 |  | worldmm-episodic | 30sec | 00:19:30–00:20:00 | 7 / 0.015873 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_39` |
| txt8 | ✓ | worldmm-episodic | 30sec | 00:39:30–00:40:00 | 8 / 0.015873 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_79` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_709` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_77` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_65` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016129 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_698` |

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
[00:04:40-00:04:50 | episodic 10sec] A man in a white shirt with a red collar speaks during a video interview, warning that if patient transportation isn't prioritized by adding vehicles, similar tragic events are certain to recur in the future. The scene then cuts to a low-angle shot of a hospital hallway, where a gurney is visible and medical staff in scrubs walk in the background. A news banner at the bottom of the screen reads, "Coroner investigating 3rd death in Quebec hospital waiting room."
```

**txt3** (cited)

```
[00:04:20-00:04:30 | episodic 10sec] A news anchor in a suit and tie speaks on a television set with a cityscape backdrop, delivering a report about a Quebec coroner’s investigation into a patient’s death after waiting 45 minutes for an ambulance in a Montreal hospital. A lower-third graphic reads, “Coroner investigating 3rd death in Quebec hospital waiting room.”
```

**txt4** (cited)

```
[00:04:30-00:04:40 | episodic 10sec] A news anchor speaks in a studio, followed by footage of people waiting in a hospital waiting room, signs for "Triage" and "Urgence," and paramedics preparing an ambulance. A man in a white shirt speaks via video call, saying, "If we do not prioritize," as the report details a man who died in a Quebec hospital waiting room after waiting 45 minutes for an ambulance due to insufficient resources.
```

**txt5** (cited)

```
[00:05:00-00:05:30 | episodic 30sec] U.S. Vice President Kamala Harris delivers a public address in Selma, Alabama, calling for an immediate ceasefire in Gaza, as broadcast by CBC News with a split-screen format showing her at a podium bearing the Vice Presidential seal. The segment transitions to visual evidence of conflict in Gaza, including explosions and smoke over the city, followed by an aerial view of a large crowd gathered around the rubble of a collapsed building. The footage then shifts to a military airfield, showing a large transport aircraft taxiing, before revealing its cargo hold filled with strapped bundles—implying military or humanitarian aid deployment. Throughout, a news ticker reinforces Harris’s call for ceasefire, underscoring the contrast between diplomatic appeals and ongoing destruction.
```

**txt6** (cited)

```
[00:20:00-00:20:30 | episodic 30sec] A CBC News report begins with a studio anchor delivering a somber story about a family who mourned the death of their son — only to later discover the deceased was a stranger. The anchor is framed against a graphic of an “Emergency Urgent Care” facility, with a lower third reinforcing the tragic misidentification. The narrative then cuts to a woman in a red sweater and glasses, seated in a home setting with a stained-glass lamp, speaking emotionally. She is later shown in a living room, conversing with a man in a plaid shirt, likely a family member or interviewer, as the on-screen text reiterates the story’s central revelation. The segment closes with an exterior shot of a hospital under a clear sky, featuring a black car passing by and a close-up of its red “URGENCE • EMERGENCY” sign, followed by a blurred interior shot of a patient in a hospital bed connected to medical equipment — visually underscoring the gravity of the misidentified death.
```

**txt7**

```
[00:19:30-00:20:00 | episodic 30sec] **[Event 1: Introduction and Branding]**  
The video opens with a serene natural scene featuring goats in a wooded area, followed by a title card displaying "The National" logo and the CBC News logo in the corner against a black screen. The logo reappears on a gray background, establishing the broadcast’s identity and setting a formal tone for the news segment.

**[Event 2: Protests in Paris for Abortion Rights]**  
In Paris, a crowd of demonstrators gathers near the Eiffel Tower, holding signs that assert abortion as a fundamental right — including “AVORTER EST UN DROIT FONDAMENTAL” and “MY BODY = MY DECISION.” The visuals underscore France’s imminent constitutional enshrinement of abortion rights, highlighting the social and political momentum behind the movement.

**[Event 3: Transition to U.S. Supreme Court and News Anchor Segment]**  
The segment shifts to exterior shots of the Palace of Versailles under an overcast sky, juxtaposed with scenes of people gathered outside the U.S. Supreme Court, where the inscription “EQUAL JUSTICE UNDER LAW” is prominently featured. The segment concludes with a news anchor in a studio, positioned before a screen showing a hospital with “Emergency Urgent” signage — reinforcing the segment’s focus on reproductive rights and healthcare access. A news ticker continuously displays: “France set to enshrine the right to abortion in constitution,” anchoring the narrative to the broader global context.
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
[video-level knowledge | semantic] (news anchor, is in, studio)
```

**txt10**

```
[video-level knowledge | semantic] (man in white shirt with red collar, warns about, patient transportation prioritization)
```

**txt11**

```
[video-level knowledge | semantic] (officials, say, measles may be spreading in Canadian communities)
```

**txt12**

```
[video-level knowledge | semantic] (news anchor, speaks to, camera)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 | ✓ | 00:44:55 | 00:44:50–00:45:00 | `54k2g9ddy4M:visual:00445000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00445000.jpg` |
| img2 |  | 00:04:25 | 00:04:20–00:04:30 | `54k2g9ddy4M:visual:00042000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00042000.jpg` |
| img3 | ✓ | 00:44:35 | 00:44:30–00:44:40 | `54k2g9ddy4M:visual:00443000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00443000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1** (cited)

```
[00:44:50-00:45:00 | video frame at 2695.0s] A news anchor in a gray suit and patterned purple tie sits at a desk, speaking directly to the camera. Behind him, two large screens display black-and-white images of city skyscrapers. The CBC News logo is visible in the bottom right corner of the screen.
```

**img2**

```
[00:04:20-00:04:30 | video frame at 265.0s] A news anchor in a suit and tie speaks on a television set with a cityscape backdrop, delivering a report about a Quebec coroner’s investigation into a patient’s death after waiting 45 minutes for an ambulance in a Montreal hospital. A lower-third graphic reads, “Coroner investigating 3rd death in Quebec hospital waiting room.”
```

**img3** (cited)

```
[00:44:30-00:44:40 | video frame at 2675.0s] A news anchor in a gray suit and purple tie stands in front of a backdrop featuring black-and-white images of city buildings. He speaks directly to the camera, using hand gestures for emphasis as he delivers his report. The CBC News logo is visible in the bottom right corner.
```
