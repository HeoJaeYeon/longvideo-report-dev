# Section 3 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:17:39): `{'video_id': '54k2g9ddy4M', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 24, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 6.24}`
- image request (2026-10-25 14:17:42): `{'video_id': '54k2g9ddy4M', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 1.03}`
- L1 filter LLM call: prompt 9298 tokens, output 75 tokens, 5.0 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 30sec | 00:21:00–00:21:30 | 1 / 0.032787 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_42` |
| txt2 | ✓ | worldmm-episodic | 10min | 00:20:00–00:30:00 | 2 / 0.032787 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10min_2` |
| txt3 | ✓ | worldmm-episodic | 30sec | 00:20:30–00:21:00 | 3 / 0.015873 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_41` |
| txt4 | ✓ | worldmm-episodic | 10sec | 00:20:50–00:21:00 | 4 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_125` |
| txt5 | ✓ | worldmm-episodic | 10sec | 00:21:00–00:21:10 | 5 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_126` |
| txt6 | ✓ | worldmm-episodic | 30sec | 00:21:30–00:22:00 | 6 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_43` |
| txt7 | ✓ | worldmm-episodic | 10sec | 00:21:30–00:21:40 | 7 / 0.015873 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_129` |
| txt8 | ✓ | worldmm-episodic | 10min | 00:10:00–00:20:00 | 8 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10min_1` |
| txt9 | ✓ | worldmm-semantic | — | no timestamp | 1 / 0.031498 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_344` |
| txt10 | ✓ | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_359` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_87` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_454` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:21:00-00:21:30 | episodic 30sec] A misidentification incident at Montfort Hospital, confirmed on February 23, 2024, involved a patient whose true identity was later verified — leading to the tragic realization by grieving family members that the deceased was not their son but a stranger. The hospital issued an official statement addressed to “Daniel,” referencing the Office of the Chief Coroner of Ontario and the Ottawa Paramedic Service, and confirmed that affected families have been informed. A formal review is underway to address systemic failures. The CBC News report, illustrated with on-screen text and visuals including hospital exteriors and interviews with Jennifer Zelmer of Healthcare Excellence Canada and a grieving family, underscores the emotional toll and institutional response to the error.
```

**txt2** (cited)

```
[00:20:00-00:30:00 | episodic 10min] **[Event 1: Misidentification Tragedy at Montfort Hospital]**  
On February 23, 2024, Montfort Hospital confirmed a fatal misidentification: a deceased patient, mourned by grieving family as their son, was later verified to be a stranger. The hospital issued an official statement referencing the Office of the Chief Coroner of Ontario and Ottawa Paramedic Service, assuring families have been notified. A formal review is underway to address systemic failures. CBC News coverage, featuring interviews with Jennifer Zelmer of Healthcare Excellence Canada and emotional family members, highlights the human toll and institutional response.

**[Event 2: Emotional Aftermath and Institutional Response]**  
A grieving woman in a red sweater and glasses reflects on the loss of her son — only to later discover he was not her child. The video intercuts with a somber man in a red plaid hoodie cleaning his kitchen, underscoring the emotional weight. Footage of Sean Cox, identified as the son, contrasts with the family’s devastation. CBC anchors and reporters, including Dan Taekema, deliver the story, reinforcing the tragic misunderstanding with on-screen text and visual cues.

**[Event 3: Transition to Swimming and Fire Tragedy]**  
The narrative shifts to a competitive swimming event, showcasing medalists and training sequences, before abruptly cutting to a title card for “The National.” A scene of a building engulfed in flames, blanketed in snow, introduces a new segment. A man in winter gear stands before the wreckage, with a red fire hydrant nearby, as the camera pans over charred debris, establishing the aftermath of a destructive event.

**[Event 4: Self-Tape Audition Trend and Actor Insight]**  
A CBC News anchor introduces the growing trend of self-taping for film and TV auditions. Actor Joel Montgrand from Vancouver discusses his experience, filmed in a vanity-lit dressing room. The segment juxtaposes studio professionalism with outdoor snowy scenes, linking the topic to remote casting practices. A title card for “The National” and visuals of a snowy Alaskan village with eerie footprints suggest thematic contrast between modern auditions and cinematic extremes.

**[Event 5: Narrative Tension and Performance Context]**  
The video transitions to a remote, snow-covered cabin with a snowmobile, setting a tense, isolated tone. A police officer confronts Montgrand in what appears to be a kitchen, suggesting a narrative layer — possibly a film or TV project — grounding the self-tape discussion in high-stakes, atmospheric performance.

**[Event 6: Self-Tapes in Film & TV Auditions — Industry Expansion]**  
CBC News explores the growing adoption of self-tapes in casting, featuring interviews with industry figures like Deirdre Bowen (Toronto Casting Director) and ACTRA president Eleanor Noble. Visual demonstrations show actors recording themselves using smartphones on ring lights or green screens, emphasizing accessibility. The segment ties self-taping to broader industry shifts — including SAG-AFTRA negotiations, actor compensation debates, and the emotional stakes of roles — illustrated through dramatic film clips and on-camera testimonials. The narrative underscores how self-tapes have become a standard, replacing traditional in-person auditions.

**[Event 7: Fire Disaster & “The Breakdown” Segment — Thematic Contrast]**  
A dramatic aerial shot captures a large building engulfed in flames, followed by an on-site reporter in winter gear detailing the destruction. The segment, titled “The Breakdown,” uses the disaster as a thematic anchor, transitioning to swimmers in a pool — suggesting a contrast between chaos and resilience. The footage includes wide shots of wreckage and snow-covered ruins, reinforcing the gravity of the event.

**[Event 8: Joshua Liendo’s Gold Medal Triumph — Athletic Legacy]**  
Canadian swimmer Joshua Liendo, representing the Florida Gators, wins gold in the Men’s 100m Butterfly at the Commonwealth Games. The segment showcases his training, competition highlights, and medal celebration, including teammates waving the Canadian flag. A CBC News anchor frames his story as historic, concluding with on-screen text declaring him “swims into the history books.” The narrative blends athletic achievement with media coverage, highlighting his legacy.

**[Event 9: Liendo’s Personal Reflection — Balance Between Performance and Life]**  
In a CBC News segment, Liendo, seated poolside in a white Gators shirt and gold chain, discusses his breakthrough season, crediting the University of Florida’s training environment and the motivational power of past champions. He contrasts his high-stakes competition with a low-key personal life—watching sports, playing video games, and hanging out with friends—emphasizing the mental balance required for elite performance. The segment weaves race footage, studio commentary, and personal reflection to highlight his rise as Canada’s male swimmer of the year and his first international gold at the 2022 Commonwealth Games.

**[Event 10: Medal Ceremony and Legacy Solidification]**  
A young Canadian swimmer in a red jacket is shown receiving his gold medal on the podium at Birmingham 2022, holding it aloft beside silver-medalists from Australia and other nations, underscoring the emotional significance of his milestone. The video closes with Liendo’s legacy firmly anchored in both Canadian and American swimming history, as the CBC anchor reinforces his place among Olympic greats.

---

**[Summary of Events]**  
The video presents a fragmented yet thematically layered narrative that juxtaposes tragedy, resilience, and transformation across three distinct domains: institutional failure and human grief, the evolving landscape of media and performance, and athletic triumph. The opening tragedy at Montfort Hospital — a fatal misidentification that shattered a family’s grief — is contrasted with the controlled, emotional performances of actors and athletes. The segment on self-taping in casting, featuring Joel Montgrand and industry experts, frames the digital age’s democratization of opportunity — even as it mirrors the isolation and tension of cinematic storytelling. Meanwhile, the fire disaster and “The Breakdown” segment provide a visceral counterpoint to the calm of the pool, grounding the narrative in the fragility of human systems. Finally, Joshua Liendo’s gold medal win — captured with cinematic flair and personal reflection — serves as a triumphant arc, symbolizing not only athletic excellence but also the emotional resilience required to navigate life’s unpredictable turns. The video’s structure, while disjointed, creates a powerful emotional rhythm: from loss to performance, from chaos to clarity, and ultimately, from tragedy to triumph.
```

**txt3** (cited)

```
[00:20:30-00:21:00 | episodic 30sec] A grieving mother, Heather Insley from Picton, Ontario, recounts how her family mourned the death of their son—only to later discover he was a stranger—after his passing was reported in the news. The video opens with a somber hospital scene showing a critically ill patient connected to life-support equipment, followed by a healthcare worker in protective gear attending to them. The narrative then shifts to Insley, seated in a warmly lit home setting with a stained-glass lamp behind her, speaking candidly to a CBC News interviewer while holding a smartphone, her expression heavy with sorrow. On-screen text underscores the emotional gravity of the story: “Family mourns son’s death before realizing it was a stranger.” The footage juxtaposes the clinical reality of the hospital with the personal devastation experienced by the family, highlighting the tragic misunderstanding that unfolded after the boy’s death.
```

**txt4** (cited)

```
[00:20:50-00:21:00 | episodic 10sec] Heather Insley, identified as a mother from Picton, Ontario, is shown in a CBC News interview discussing the tragic event where her family mourned the death of their son before realizing he was a stranger. She is seen speaking in a warmly lit indoor setting, with a stained-glass lamp visible in the background. The camera alternates between close-ups of her face and wider shots showing her seated across from an interviewer.
```

**txt5** (cited)

```
[00:21:00-00:21:10 | episodic 10sec] A document from Montfort Hospital is displayed, detailing a statement regarding a misidentification incident. Text overlays highlight key points: “...misidentification...”, “True identity... has since been confirmed.”, “The families involved have been informed.”, and “A review... is underway...”. The document, dated February 23, 2024, is addressed to “Daniel” and references the Office of the Chief Coroner of Ontario and the Ottawa Paramedic Service. A news ticker at the bottom reads: “Family mourns son’s death before realizing it was a stranger” with the CBCNEWS logo.
```

**txt6** (cited)

```
[00:21:30-00:22:00 | episodic 30sec] A grieving woman in a red sweater and glasses speaks emotionally to an interviewer in a living room, her sorrow evident as she reflects on the loss of her son — only to later discover he was a stranger. The narrative shifts to a man in a red plaid hoodie and black cap, seen washing his hands and meticulously wiping down a stove in a kitchen, where a Pepsi bottle and cigarette box sit untouched; his somber demeanor underscores the weight of the revelation. The video intercuts between these scenes and includes footage of Sean Cox, identified as the son, speaking directly to the camera, before returning to the woman on the couch, still absorbed in her phone, as the on-screen text and CBC News logo reinforce the tragic misunderstanding: “Family mourns son’s death before realizing it was a stranger.”
```

**txt7** (cited)

```
[00:21:30-00:21:40 | episodic 10sec] A woman in a red sweater and glasses speaks emotionally to an interviewer in a living room, her expression conveying grief. The scene cuts to a man in a red plaid hoodie and a baseball cap washing his hands in a sink, suggesting a moment of personal reflection or cleansing. The on-screen text reads, "Family mourns son's death before realizing it was a stranger."
```

**txt8** (cited)

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

**txt9** (cited)

```
[video-level knowledge | semantic] (document, issued by, Montfort Hospital)
```

**txt10** (cited)

```
[video-level knowledge | semantic] (on-screen text, reads, Family mourns son's death before realizing it was a stranger)
```

**txt11**

```
[video-level knowledge | semantic] (news story, is about, Coroner investigating 3rd death in Quebec hospital waiting room)
```

**txt12**

```
[video-level knowledge | semantic] (Joshua Liendo, swims, freestyle)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 | ✓ | 00:20:35 | 00:20:30–00:20:40 | `54k2g9ddy4M:visual:00203000` | `outputs/p9p19_check_20261025_141401/frames_s2/54k2g9ddy4M/00203000.jpg` |
| img2 |  | 00:22:15 | 00:22:10–00:22:20 | `54k2g9ddy4M:visual:00221000` | `outputs/p9p19_check_20261025_141401/frames_s2/54k2g9ddy4M/00221000.jpg` |
| img3 |  | 00:20:25 | 00:20:20–00:20:30 | `54k2g9ddy4M:visual:00202000` | `outputs/p9p19_check_20261025_141401/frames_s2/54k2g9ddy4M/00202000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1** (cited)

```
[00:20:30-00:20:40 | video frame at 1235.0s] The video shows a hospital scene where a person is lying in a bed with medical equipment, including an oxygen tube and a ventilator, suggesting they are critically ill or unconscious. The person’s face is blurred for privacy. The camera then shifts to show a healthcare worker, wearing a yellow protective gown and glasses, attending to the patient. The final frame transitions to an interview with a woman in a red sweater and glasses, speaking in what appears to be a home setting, with a stained-glass lamp visible behind her. The on-screen text reads, “Family mourns son’s death before realizing it was a stranger,” indicating the emotional context of the story.
```

**img2**

```
[00:22:10-00:22:20 | video frame at 1335.0s] A woman in a red sweater and glasses speaks indoors, with a stained-glass lamp visible behind her. The scene cuts to a male reporter, Dan Taekema of CBC News, standing outdoors in front of a building with parked cars and bare trees under a clear sky. He speaks to the camera as the on-screen text reads, “Family mourns son’s death before realizing it was a stranger.”
```

**img3**

```
[00:20:20-00:20:30 | video frame at 1225.0s] The video opens with an exterior shot of a hospital, showing a parking lot filled with cars and the building's facade under a clear blue sky. A black car drives past, and the camera then zooms in on a red "URGENCE • EMERGENCY" sign on the hospital. The scene transitions to a blurred interior shot of a patient in a hospital bed, connected to medical equipment, with the on-screen text reading, "Family mourns son's death before realizing it was a stranger."
```
