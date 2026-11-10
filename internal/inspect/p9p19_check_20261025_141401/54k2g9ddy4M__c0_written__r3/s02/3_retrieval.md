# Section 2 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:28:16): `{'video_id': '54k2g9ddy4M', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 25, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 5.75}`
- image request (2026-10-25 14:28:19): `{'video_id': '54k2g9ddy4M', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 1.34}`
- L1 filter LLM call: prompt 9235 tokens, output 67 tokens, 4.6 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 3min | 00:12:00–00:15:00 | 1 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:3min_4` |
| txt2 | ✓ | worldmm-episodic | 10min | 00:10:00–00:20:00 | 2 / 0.032787 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10min_1` |
| txt3 |  | worldmm-episodic | 3min | 00:00:00–00:03:00 | 3 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:3min_0` |
| txt4 | ✓ | worldmm-episodic | 3min | 00:03:00–00:06:00 | 4 / 0.032522 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:3min_1` |
| txt5 | ✓ | worldmm-episodic | 30sec | 00:11:30–00:12:00 | 5 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_23` |
| txt6 | ✓ | worldmm-episodic | 30sec | 00:12:30–00:13:00 | 6 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_25` |
| txt7 | ✓ | worldmm-episodic | 30sec | 00:15:30–00:16:00 | 7 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_31` |
| txt8 |  | worldmm-episodic | 30sec | 00:16:00–00:16:30 | 8 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_32` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_192` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_74` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_270` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016129 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_193` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:12:00-00:15:00 | episodic 3min] **[Event 1: Rising Airline Fees Amid Falling Fares]**  
The segment opens with visuals of airport luggage and on-screen text highlighting a 14.3% drop in Canadian airfares from January 2023 to 2024, juxtaposed with rising airline fees. Professor Karl Moore at McGill University and CBC’s Sophia Harris in Vancouver frame the issue, emphasizing how hidden charges inflate travel costs. Travel writer Anshul Singh adds context, while real-world examples — including a man named GECA who bought unused tickets — illustrate the financial trap. Footage of passengers and airport scenes reinforces the growing complexity of air travel economics in Canada.

**[Event 2: MH370 Anniversary Commemoration and Aviation Safety Push]**  
The video shifts to Malaysia’s 10th-anniversary commemoration of MH370’s disappearance. Transport Minister Anthony Loke speaks at a press conference and public gathering in Subang Jaya, flanked by grieving families. Emotional tributes, commemorative shirts, and a central sign declaring “IT’S NOT HISTORY, IT’S THE FUTURE OF AVIATION SAFETY” underscore the unresolved nature of the tragedy and the ongoing push for aviation safety reforms. The event blends personal grief with national responsibility.

**[Event 3: California Winter Storm and Its Dual Impact]**  
The segment transitions to a CBC News report on a severe winter storm in California, dumping up to two meters of snow and causing hazardous driving conditions. Interviews with residents — including a woman fearing her husband’s inability to drive — highlight personal risk. Meteorologists Sara Purdue and Brian Brong analyze the storm’s intensity and its ecological role in replenishing snowpack for summer water supply, contrasting its destructive force with its environmental necessity. The report ties aviation safety concerns with broader climate and weather disruptions.
```

**txt2** (cited)

```
[00:10:00-00:20:00 | episodic 10min] **[Event 1: Rising Airline Fees Amid Falling Fares]**  
Canadian airfares dropped 14.3% from January 2023 to 2024, yet airline fees continue to climb, creating a financial trap for travelers. Professor Karl Moore and CBC’s Sophia Harris highlight how hidden charges inflate total travel costs, while travel writer Anshul Singh provides context. Real-world examples — including GECA, who purchased unused tickets — illustrate the growing complexity and economic burden of air travel. Airport footage and passenger scenes reinforce the disconnect between advertised fares and actual costs, exposing systemic inefficiencies in the industry.

**[Event 2: MH370 Anniversary Commemoration and Aviation Safety Push]**  
On the 10th anniversary of MH370’s disappearance, Malaysia’s Transport Minister Anthony Loke addresses grieving families and the public in Subang Jaya. Emotional tributes, commemorative shirts, and a central sign reading “IT’S NOT HISTORY, IT’S THE FUTURE OF AVIATION SAFETY” underscore the unresolved nature of the tragedy and the urgent call for safety reforms. The event merges personal grief with national responsibility, emphasizing that aviation safety must evolve to prevent future tragedies.

**[Event 3: California Winter Storm and Its Dual Impact]**  
A severe winter storm in California dumped up to two meters of snow, creating hazardous driving conditions and displacing residents. Interviews with locals — including a woman fearing her husband’s inability to drive — highlight personal risk. Meteorologists Sara Purdue and Brian Brong analyze the storm’s intensity and its ecological role in replenishing snowpack for summer water supply. The report contrasts the storm’s destructive force with its environmental necessity, visually supported by scenes of snow-covered streets, outdoor activities, and weather maps.

**[Event 4: Wildfires and Disaster Preparedness Across Canada and the U.S.]**  
Meanwhile, Texas faces its largest wildfire in history, fueled by extreme winds and claiming lives and livestock. Flames consume highways, skies turn smoke-choked, and firefighting efforts struggle for containment at just 15%. Canadian communities — including Cranbrook and Yellowknife — brace for similar threats, with officials reviewing emergency plans and investing in communication upgrades. However, funding remains critically short. Mayors Don McCormick and Rebecca Alty stress the urgent need for federal support in landscape management and disaster preparedness. Yellowknife’s post-evacuation recovery includes new coordination staff and tech upgrades, yet municipal resource gaps persist. CBC News reporter Marina von Stackelberg sets the stage for a press conference with Harjit Sajjan, Minister of Emergency Preparedness, who outlines Ottawa’s role in coordinating provincial and municipal disaster readiness. Expert commentary further contextualizes the federal response. The segment closes with dramatic coastal wave footage, symbolizing the escalating urgency of natural disaster preparedness across North America.

**[Event 5: Misidentification Tragedy in Picton, Ontario]**  
A grieving mother, Heather Insley from Picton, recounts how her family mourned the death of their son — only to later learn he was a stranger. The story juxtaposes hospital scenes of critical care with intimate home interviews, highlighting the emotional devastation and systemic failure in identification protocols. Visuals of emergency signage and medical equipment underscore the gravity of the error, exposing vulnerabilities in emergency response systems.

**[Event 6: Global Reproductive Rights Movements and Judicial Symbolism]**  
In Paris, demonstrators rally near the Eiffel Tower, demanding constitutional enshrinement of abortion rights. The U.S. Supreme Court and Palace of Versailles are shown under overcast skies — visually linking global legal battles over bodily autonomy. A CBC News anchor anchors the segment, with a ticker reinforcing France’s historic legislative shift, framing the story within a broader international context of reproductive rights advocacy.

**[Event 7: Behind-the-Scenes Production and Branding of CBC News’ “The National”]**  
The video includes brief glimpses of CBC News’ “The National” production: a woman filming in a home studio with umbrella lights, a man adjusting camera gear, and a blurred transition to a snowy nighttime scene — all reinforcing the broadcast’s professional yet human-centered approach to news storytelling. These moments highlight the human effort behind delivering timely, impactful journalism.

---  
*Note: Events are presented in chronological and thematic order, with each summary capturing core actions, key participants, and visual or contextual elements. The segment closes with symbolic imagery — a cracked smartphone — hinting at systemic fragility amid escalating crises.*
```

**txt3**

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

**txt4** (cited)

```
[00:03:00-00:06:00 | episodic 3min] **Measles Outbreak Alert Across U.S. and Canada**  
A measles outbreak in the U.S., with 41 confirmed cases across 16 states, centers on Manatee Bay Elementary near Fort Lauderdale, posing heightened risk to unvaccinated and immunocompromised children under one year. Parent Demi Cavanaugh expresses concern for her unvaccinated son, while her vaccinated daughter remains protected. Public health officials warn of potential spread into Canadian communities, prompting CBC News to issue urgent vaccination advisories. Anchors and medical experts stress the importance of early vaccination (as early as nine months) and maternal antibodies for infant protection, urging consultation with healthcare providers. Visuals include vaccine administration, school aerial shots, and community anxiety, reinforced by persistent on-screen alerts.

**Quebec Hospital Waiting Room Tragedy Under Investigation**  
A third patient death in a Montreal hospital waiting room is under coroner’s review, following a prior fatality caused by a 45-minute ambulance delay. Authorities are probing systemic resource shortages, with medical professionals warning that without increased emergency vehicle deployment, similar tragedies are inevitable. Footage shows hospital corridors, triage areas, and paramedics preparing ambulances, underscoring strained emergency response. This domestic crisis is juxtaposed with international coverage of U.S. Vice President Kamala Harris’s Gaza ceasefire appeal, broadcast alongside footage of conflict and aid deployment.

**Protest Disrupts Prime Minister’s Toronto Event**  
A large nighttime protest outside the Art Gallery of Ontario on March 2, featuring Palestinian flags and demands for political action, led to the cancellation of a scheduled Prime Minister’s event. Police were present, and media coverage highlighted the disruption and ongoing investigation into the incident. Footage captured the scale and tension of the demonstration, emphasizing its impact on high-profile political scheduling and public discourse.
```

**txt5** (cited)

```
[00:11:30-00:12:00 | episodic 30sec] Fernando Chicas, a Flair Airlines customer, reacts with shock to unexpectedly high cancellation fees—$84 on a $667.21 total bill—highlighting the financial burden of airline charges. The video then shifts to show Air Canada and WestJet aircraft, illustrating that both carriers have raised economy baggage fees by $5 to $35, while fares in Canada continue to decline. The footage of travelers and ground crew loading luggage underscores the ongoing reality of rising fees amid falling base fares, with the voiceover noting airlines are increasing ancillary charges to offset declining ticket prices.
```

**txt6** (cited)

```
[00:12:30-00:13:00 | episodic 30sec] Airline fees in Canada are rising despite falling base fares, as carriers independently set pricing for optional services — a policy affirmed by Transport Canada. This trend forces travelers to reconsider seemingly cheap tickets, as hidden costs can significantly increase total travel expenses. The issue is illustrated through real-world examples, including a man named GECA who purchased four unused tickets, learning the hard way that low initial prices don’t always reflect true value. The segment visually reinforces the theme with footage of passengers navigating airports and interview clips of individuals reflecting on their travel experiences, underscoring the growing financial complexity of air travel in Canada.
```

**txt7** (cited)

```
[00:15:30-00:16:00 | episodic 30sec] **Heavy snow blankets California as storm brings record snowfall and dangerous winds.**  
A woman with glasses speaks into a microphone amid falling snow, expressing hope she’ll survive the storm, while another woman in a beanie smiles outdoors in the wintry conditions. Footage shows a snow-covered pickup truck and people braving deep snow, concluding with icicles hanging from a snow-laden roof. A news ticker confirms the storm is dropping up to two metres of snow across California.

**Meanwhile, Texas wildfires rage under high winds fueled by extreme weather.**  
A news anchor in a studio reports on a massive wildfire in Canadian, Texas, with visuals of flames consuming a highway, firefighters battling smoke-filled conditions, and a tractor moving through the affected farmland. On-screen text identifies the blaze as the largest in Texas’s history, with high winds accelerating its spread. The anchor notes the fire is only 15% contained, has claimed two lives and numerous livestock, and crews are working to control spot fires. The segment credits Yvette Bren, CBC News, Vancouver.
```

**txt8**

```
[00:16:00-00:16:30 | episodic 30sec] A wildfire is actively burning through dry brush and trees near a residential area, with thick smoke obscuring visibility and a cow briefly visible through the trees. The fire has caused significant devastation, killing people and livestock and destroying hundreds of structures. Meanwhile, Canadian communities, including those in British Columbia, are preparing for extreme weather and potential wildfires. Officials in Cranbrook are reviewing emergency management plans on a large map, while smoke blankets a nearby parking lot and distant flames rage on the mountainside. A firefighting helicopter is seen overhead, indicating active response efforts as cities and provinces look to Ottawa for coordinated disaster preparedness strategies.
```

**txt9**

```
[video-level knowledge | semantic] (Air Canada, increased fees for, checked bags on economy fares)
```

**txt10**

```
[video-level knowledge | semantic] (3rd death in Quebec hospital waiting room, occurred in, hospital waiting room)
```

**txt11**

```
[video-level knowledge | semantic] (wildfire, is caused by, high winds)
```

**txt12**

```
[video-level knowledge | semantic] (WestJet, increased fees for, checked bags on economy fares)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 | ✓ | 00:14:25 | 00:14:20–00:14:30 | `54k2g9ddy4M:visual:00142000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00142000.jpg` |
| img2 | ✓ | 00:14:55 | 00:14:50–00:15:00 | `54k2g9ddy4M:visual:00145000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00145000.jpg` |
| img3 | ✓ | 00:10:55 | 00:10:50–00:11:00 | `54k2g9ddy4M:visual:00105000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00105000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1** (cited)

```
[00:14:20-00:14:30 | video frame at 865.0s] A news report shows scenes of a severe winter storm in California, with heavy snow blanketing trees and roads, and a sign indicating that a gondola is closed. The segment transitions to a meteorologist, Sara Purdue in Sacramento, California, who provides commentary on the storm’s impact, including high winds and significant snowfall.
```

**img2** (cited)

```
[00:14:50-00:15:00 | video frame at 895.0s] A meteorologist, identified as Brian Brong from the U.S. National Weather Service in Reno, Nevada, speaks in an office setting, with a weather map visible on a monitor behind him. The segment cuts to footage of a snow-covered forest, showing thick snow blanketing the ground and trees under a blizzard-like sky. The visuals emphasize the significant snowfall, which the meteorologist explains is crucial for replenishing the region’s snowpack, as this snow will melt in the summer to provide vital water for rivers and streams. A news ticker at the bottom of the screen reads, “California storm with high winds drops up to two metres of snow.”
```

**img3** (cited)

```
[00:10:50-00:11:00 | video frame at 655.0s] A news anchor in a suit and tie speaks to the camera in a studio, with a graphic behind him showing travelers at an airport check-in counter. The on-screen text reads, "Airline fees keep climbing as fares drop in Canada." The segment begins with a female anchor, Katie Simpson, in Washington, discussing airfare trends.
```
