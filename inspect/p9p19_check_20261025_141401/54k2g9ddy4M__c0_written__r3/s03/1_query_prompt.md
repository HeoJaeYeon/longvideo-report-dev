# Section 3 — query-generation prompt

- 739 prompt tokens

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

**Current section:** This section focuses on the misidentification tragedy at Montfort Hospital (00:20:00-00:30:00), where a grieving family mourned a deceased patient only to later learn he was not their son. It also transitions to Joshua Liendo’s gold medal win and personal reflections, showing the video’s emotional and athletic contrasts.

**Current section requirements:**
- State that Montfort Hospital confirmed a fatal misidentification on February 23, 2024
- Note the emotional interviews with grieving family members
- Confirm Liendo’s gold medal win in the Men’s 100m Butterfly at the Commonwealth Games

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
