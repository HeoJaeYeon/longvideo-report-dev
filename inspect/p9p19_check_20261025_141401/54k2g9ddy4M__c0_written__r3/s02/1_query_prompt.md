# Section 2 — query-generation prompt

- 595 prompt tokens

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

**Current section:** This section details the unfolding of the measles outbreak and its consequences (00:10:00-00:20:00), including public health warnings, hospital strain, and a patient death in Montreal. It also shows the contrast with unrelated events like airline fee hikes and wildfire preparedness, illustrating the video’s fragmented yet thematic structure.

**Current section requirements:**
- Confirm the report of a third patient death in a Montreal hospital waiting room (00:10:00-00:20:00)
- Note the CBC anchor’s mention of rising airline fees and winter storm impacts
- Identify the wildfire threat in Texas and Canada’s disaster preparedness concerns

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
