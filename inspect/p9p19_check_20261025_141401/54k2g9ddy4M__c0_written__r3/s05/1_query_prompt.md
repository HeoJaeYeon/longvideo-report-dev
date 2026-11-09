# Section 5 — query-generation prompt

- 1071 prompt tokens

````
You generate search queries for retrieving evidence from ONE video's memory.

**Report topic:** Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.

**Overall requirements:**


**Previous sections (summary):**
Already written in earlier sections (title, then the first sentence of each paragraph; citation numbers removed - they do NOT refer to the evidence of the current section):
Section 1: Opening of the Video: Public Health, Politics, and Athletic Ascent
- The video opens with a public health alert concerning a measles resurgence in Canada and the U.S., establishing the first of its intersecting narratives.
- Simultaneously, the video introduces a political disruption: a large nighttime protest outside the Art Gallery of Ontario on March 2.
- Interwoven with these narratives is the athletic storyline of Canadian swimmer Joshua Liendo.
- The video’s opening frames also juxtapose these narratives with everyday life under threat.

Section 2: Measles Outbreak Escalates, Hospital Strain Mounts, and Broader Crises Emerge
- At 00:10:00, the video shifts focus from public health alerts to the unfolding consequences of the measles outbreak, particularly in Montreal.
- Simultaneously, CBC News anchors report on unrelated but thematically resonant developments.
- Elsewhere, a severe winter storm in California dumps up to two meters of snow, creating hazardous driving conditions and displacing residents.
- At 00:15:30, a news anchor in a studio reports on the California storm, with visuals of heavy snow blanketing trees and roads and a sign indicating that a gondola is closed.

Section 3: Misidentification Tragedy at Montfort Hospital and Joshua Liendo’s Gold Medal Triumph
- At 00:20:00, the video transitions to a CBC News report detailing a fatal misidentification at Montfort Hospital, confirmed on February 23, 2024.
- The narrative opens with a studio anchor delivering the somber news, framed against a graphic of an “Emergency Urgent Care” facility.
- Jennifer Zelmer of Healthcare Excellence Canada is interviewed in an office setting, standing in front of a bookshelf, offering institutional context to the event.
- At 00:21:00, the video abruptly transitions to a competitive swimming event, showcasing medalists and training sequences, before cutting to a title card for “The National”.

Section 4: Joshua Liendo’s Personal Journey and Historic Legacy
- At 00:31:00, Joshua Liendo, wearing a white Florida Gators t-shirt and a gold chain, reflects on his childhood in Trinidad, stating he was born there and moved to Canada in 2012 at age 10.
- Liendo’s journey to elite swimming is underscored by his historic gold medal win in the Men’s 100m Butterfly Final at the Doha World Championships.
- In his reflections, Liendo also addresses systemic underrepresentation in elite swimming, discussing cultural stereotypes that deter people of color from the sport.
- The segment concludes with Liendo smiling warmly at the CBC News anchor, reinforcing his pride and humility.

**Current section:** This section covers the aftermath of a devastating fire that destroyed the only school on Eabametoong First Nation (00:40:00-00:50:00), including community grief, federal aid, and the eventual reopening of new schools in Pikangikum and Wapekeka. It also briefly shows unrelated segments on pet psychics and goats crossing a street, illustrating the video’s thematic diversity.

**Current section requirements:**
- State that the school fire destroyed educational infrastructure in Eabametoong First Nation
- Confirm the federal government’s $13 million pledge for modular classrooms
- Note the grand openings of new schools in Pikangikum and Wapekeka First Nation

The video memory can be searched in two ways:
1. text_queries search timestamped descriptions of the video (what happens, who does what, what is said, which objects appear) and short facts extracted from the video. Write short keyword-style phrases that name concrete events, actions, people, objects, or spoken topics (e.g., "host explains the rules", "person unboxes the product").
2. image_queries search video clips by visual similarity. Write one sentence describing what the scene LOOKS like: people and their appearance and actions, objects, and the setting (e.g., "a woman in an apron stirring a pot in a bright kitchen"). Do not ask for charts, diagrams, infographics, or documents.

Cover the different requirements of the current section, avoid near-duplicate queries, and do not repeat what previous sections already covered unless it is needed.
Generate 2-3 text_queries and 1-2 image_queries.

**Output Format (JSON):**
```json
{
  "text_queries": ["query 1", "query 2"],
  "image_queries": ["scene description 1"]
}
```

Generate the queries now:

````
