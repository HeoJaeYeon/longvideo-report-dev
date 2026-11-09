# Section 1 — query-generation prompt

- 438 prompt tokens

````
You generate search queries for retrieving evidence from ONE video's memory.

**Report topic:** Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.

**Overall requirements:**


**Previous sections (summary):**
This is the first section

**Current section:** This section introduces the six main participants—Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player—and establishes the setting: a sunny outdoor basketball court. It describes how they split into teams and begin testing 12 viral sports gadgets, starting with the SPORTS DRIBBLE SPECS. Readers learn the video’s goal is to test and evaluate these gadgets in a casual, competitive environment.

**Current section requirements:**
- List the six main participants and how they are introduced
- Describe the outdoor basketball court setting and weather
- Note the first gadget tested and the rules of its challenge

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
