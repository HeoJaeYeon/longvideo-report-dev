# Section 2 — query-generation prompt

- 634 prompt tokens

````
You generate search queries for retrieving evidence from ONE video's memory.

**Report topic:** Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.

**Overall requirements:**


**Previous sections (summary):**
Already written in earlier sections (title, then the first sentence of each paragraph; citation numbers removed - they do NOT refer to the evidence of the current section):
Section 1: Opening of the Video: Public Health, Political Disruption, and Athletic Achievement
- The video opens with a public health alert concerning a measles resurgence in Canada and the U.S., setting the tone for a segment focused on urgent medical concerns.
- Simultaneously, the video introduces a political disruption: a large nighttime protest outside the Art Gallery of Ontario on March 2, featuring Palestinian flags and demands for political action, which led to the cancellation of a scheduled
- Interwoven with these themes is the athletic achievement of Canadian swimmer Joshua Liendo.
- The video’s opening also includes scenes of everyday life under the measles threat, contrasting normalcy with urgency.
- At 00:02:00, Dr.
- The segment concludes with a focus on vaccination gaps.

**Current section:** This section details the unfolding of the measles outbreak and its consequences (00:10:00-00:20:00), including public health warnings, hospital system strain, and a third patient death in Montreal. Readers learn about the systemic crisis in emergency response and the video’s juxtaposition of health threats with political and travel-related issues.

**Current section requirements:**
- Show footage of a father swinging a child at a playground with a measles warning ticker
- Include visuals of hospital corridors and paramedics preparing ambulances
- Cite the third patient death in a Montreal hospital waiting room under coroner’s review

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
