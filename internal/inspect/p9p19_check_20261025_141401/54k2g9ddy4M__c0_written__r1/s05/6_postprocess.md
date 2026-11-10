# Section 5 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 602 words → after removal 602 words

## 2. Start/end claim check (`boundary_claims`)

- none

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 24, "cited_sentences": 6, "checked_tokens": 7, "unsupported": 0, "miscited": 0, "uncited_claims": 0, "absence_statements": 0}`

- no findings

## 4. Citation conversion stats

- `{"text_citations": 53, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 0, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 4 of 12

## 5. Image-text time alignment

- no cited image

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Community Disaster and Recovery

At 00:36:00, a devastating fire destroyed the only school on Eabametoong First Nation, located in Northwestern Ontario, leaving behind charred ruins blanketed in snow [citation:txt1][citation:txt2]. The blaze overwhelmed local firefighting efforts due to inadequate water infrastructure, forcing children to relocate for education and deepening grief among residents [citation:txt1][citation:txt2]. Four teenagers have been charged in connection with the arson [citation:txt1]. Community members, including teacher Mary Okeese and student Owen Slipperjack, shared emotional testimonies contrasting joyful school memories with the current devastation [citation:txt1][citation:txt2]. Chief Solomon Atlookan emphasized systemic vulnerabilities in emergency response for remote Indigenous communities [citation:txt1][citation:txt2]. Aerial and ground footage underscored the isolation of the community, 360 km from Winnipeg, near Thunder Bay [citation:txt1][citation:txt2]. The Canadian and First Nations flags fly at half-mast as the community mourns and begins the long road to recovery [citation:txt1][citation:txt2].

In response to the crisis, the federal government pledged over $13 million to construct five modular classrooms as temporary solutions, aiming to restore educational continuity for affected children [citation:txt1][citation:txt2][citation:txt5][citation:txt6]. This pledge was confirmed after the Federal Minister of Indigenous Services met with the chief in Thunder Bay [citation:txt5][citation:txt6]. The government’s commitment was reiterated in a CBC News segment, where officials vowed to stand with the community in constructing a new permanent school [citation:txt3][citation:txt4]. The video shows the aftermath of the fire, with footage of the collapsed metal roof under a cloudy sky, alongside Canadian and First Nation flags [citation:txt3][citation:txt4][citation:txt5][citation:txt6]. A memorial ceremony was held in a gymnasium, followed by footage of the “Rev. Eleazar Winter Memorial School” sign and a large nighttime fire, confirming the school’s destruction [citation:txt1][citation:txt4].

By June 2023, Pikangikum First Nation unveiled its newly built school — a modern facility with vehicles parked outside — symbolizing a decade-long wait for replacement after the original school was lost to fire [citation:txt3][citation:txt8]. The narration underscores the urgency of the rebuild, highlighting the community’s prolonged struggle for educational infrastructure [citation:txt3][citation:txt8]. In September 2023, Wapekeka First Nation celebrated the grand opening of its new school — a colorful, modern building adorned with festive decorations, balloons, and banners [citation:txt3][citation:txt7]. The event marked the end of an eight-year wait following the fire, showcasing community resilience and the government’s eventual fulfillment of long-delayed promises [citation:txt3][citation:txt7]. The video shows the exterior and interior of the new school building at Wapekeka First Nation, with numerous vehicles parked in front and people seated at long tables in a gymnasium-like space decorated with balloons and banners [citation:txt7]. The narration mentions that the community waited eight years for this new school after its previous one was destroyed by fire [citation:txt7].

The video also highlights the ongoing water crisis in remote First Nation communities, with footage of a snowy landscape and people walking through snow with a child’s sled [citation:txt1][citation:txt4]. On-screen text reads: “Remote First Nation feels heavy loss after fire destroys school,” while narration emphasizes the community’s long-standing boil water advisory since 2002, and their determination to sustain education despite inadequate fire, water, and housing services [citation:txt1][citation:txt4]. A CBC News segment features reporter Sarah Law in studio discussing the school fire with correspondent details, highlighting cleanup operations, arrival of supplies via winter road, and logistical strategies using the cold snap to transport materials for a temporary school [citation:txt3][citation:txt4]. The segment also covers repurposing community facilities — extending a hall for education and installing artificial ice in an arena for youth recreation — while underscoring Ontario’s Minister of Indigenous Affairs’ involvement and the community’s cautious optimism [citation:txt3][citation:txt4]. The video’s coverage of the fire’s impact, the community’s grief, and the government’s delayed but eventual support is grounded in these visual and narrative elements [citation:txt1][citation:txt2][citation:txt3][citation:txt4][citation:txt5][citation:txt6][citation:txt7][citation:txt8].
```

## 7. Grounded body (exactly as in report.md)

```
# Community Disaster and Recovery

At 00:36:00, a devastating fire destroyed the only school on Eabametoong First Nation, located in Northwestern Ontario, leaving behind charred ruins blanketed in snow [32][33]. The blaze overwhelmed local firefighting efforts due to inadequate water infrastructure, forcing children to relocate for education and deepening grief among residents [32][33]. Four teenagers have been charged in connection with the arson [32]. Community members, including teacher Mary Okeese and student Owen Slipperjack, shared emotional testimonies contrasting joyful school memories with the current devastation [32][33]. Chief Solomon Atlookan emphasized systemic vulnerabilities in emergency response for remote Indigenous communities [32][33]. Aerial and ground footage underscored the isolation of the community, 360 km from Winnipeg, near Thunder Bay [32][33]. The Canadian and First Nations flags fly at half-mast as the community mourns and begins the long road to recovery [32][33].

In response to the crisis, the federal government pledged over $13 million to construct five modular classrooms as temporary solutions, aiming to restore educational continuity for affected children [32][33][34][35]. This pledge was confirmed after the Federal Minister of Indigenous Services met with the chief in Thunder Bay [34][35]. The government’s commitment was reiterated in a CBC News segment, where officials vowed to stand with the community in constructing a new permanent school [36][37]. The video shows the aftermath of the fire, with footage of the collapsed metal roof under a cloudy sky, alongside Canadian and First Nation flags [36][37][34][35]. A memorial ceremony was held in a gymnasium, followed by footage of the “Rev. Eleazar Winter Memorial School” sign and a large nighttime fire, confirming the school’s destruction [32][37].

By June 2023, Pikangikum First Nation unveiled its newly built school — a modern facility with vehicles parked outside — symbolizing a decade-long wait for replacement after the original school was lost to fire [36][38]. The narration underscores the urgency of the rebuild, highlighting the community’s prolonged struggle for educational infrastructure [36][38]. In September 2023, Wapekeka First Nation celebrated the grand opening of its new school — a colorful, modern building adorned with festive decorations, balloons, and banners [36][39]. The event marked the end of an eight-year wait following the fire, showcasing community resilience and the government’s eventual fulfillment of long-delayed promises [36][39]. The video shows the exterior and interior of the new school building at Wapekeka First Nation, with numerous vehicles parked in front and people seated at long tables in a gymnasium-like space decorated with balloons and banners [39]. The narration mentions that the community waited eight years for this new school after its previous one was destroyed by fire [39].

The video also highlights the ongoing water crisis in remote First Nation communities, with footage of a snowy landscape and people walking through snow with a child’s sled [32][37]. On-screen text reads: “Remote First Nation feels heavy loss after fire destroys school,” while narration emphasizes the community’s long-standing boil water advisory since 2002, and their determination to sustain education despite inadequate fire, water, and housing services [32][37]. A CBC News segment features reporter Sarah Law in studio discussing the school fire with correspondent details, highlighting cleanup operations, arrival of supplies via winter road, and logistical strategies using the cold snap to transport materials for a temporary school [36][37]. The segment also covers repurposing community facilities — extending a hall for education and installing artificial ice in an arena for youth recreation — while underscoring Ontario’s Minister of Indigenous Affairs’ involvement and the community’s cautious optimism [36][37]. The video’s coverage of the fire’s impact, the community’s grief, and the government’s delayed but eventual support is grounded in these visual and narrative elements [32][33][36][37][34][35][39][38].
```

## 8. References used by this section (global numbers)

```
[32] 00:30:00–00:40:00 · episodic 10min: **[Event Summary]**  
Joshua Liendo, Canada’s first Black swimmer to reach elite milestones, reflects on his journey from Trinidad to global podiums, framed by personal memories, cultural roots, and athletic triumph....
[33] 00:36:00–00:39:00 · episodic 3min: **[Event Summary]**  
A devastating fire in late January destroyed the only school on Eabametoong First Nation, Northwestern Ontario, leaving charred ruins blanketed in snow and triggering a community-wide crisis. The...
[34] 00:38:30–00:39:00 · episodic 30sec: **[Event 1: Aerial and Ground Views of Fire-Damaged School]**  
The video opens with an aerial shot from an airplane, revealing a snowy landscape dotted with dark water patches and a small snow-covered island, with th...
[35] 00:38:50–00:39:00 · episodic 10sec: The video shows the aftermath of a fire that destroyed a school in a remote First Nation community, with shots of the charred and collapsed structure, including twisted metal roofing and debris scattered across snow-c...
[36] 00:39:00–00:39:30 · episodic 30sec: **[Event Summary]**  
A fire destroyed a school at a remote First Nation community, leaving behind charred ruins and prompting widespread grief — as captured in footage showing the collapsed metal roof under a cloudy...
[37] 00:39:00–00:42:00 · episodic 3min: **[Event Summary]**  
A devastating fire destroyed a remote First Nation school, leaving behind charred ruins and triggering widespread grief — captured in footage of the collapsed roof under a cloudy sky, alongside C...
[38] 00:39:10–00:39:20 · episodic 10sec: The video shows the aftermath of a fire that destroyed a school, with the charred remains visible under a cloudy sky, alongside Canadian and First Nation flags. The scene then transitions to a modern, newly constructe...
[39] 00:39:20–00:39:30 · episodic 10sec: The video shows the exterior and interior of a new school building at Wapekeka First Nation, which held a grand opening ceremony in September 2023. Outside, numerous vehicles are parked in a dirt lot in front of the m...
```
