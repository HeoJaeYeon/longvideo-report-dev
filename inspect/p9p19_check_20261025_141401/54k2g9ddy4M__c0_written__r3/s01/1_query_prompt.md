# Section 1 — query-generation prompt

- 460 prompt tokens

````
You generate search queries for retrieving evidence from ONE video's memory.

**Report topic:** Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.

**Overall requirements:**


**Previous sections (summary):**
This is the first section

**Current section:** This section covers the opening of the video (00:00:00-00:10:00), which introduces the main subjects and events: a measles outbreak in Canada and the U.S., a protest disrupting a Prime Minister’s event, and Canadian swimmer Joshua Liendo’s rise. Readers learn the video’s focus on intersecting public health, political, and athletic narratives.

**Current section requirements:**
- Identify the measles outbreak as a key public health concern mentioned at 00:00:00
- Note the protest outside the Art Gallery of Ontario on March 2 as a political event
- Highlight Joshua Liendo’s Olympic ascent and interview as the athletic storyline

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
