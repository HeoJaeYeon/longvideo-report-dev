# Section 1 — query-generation prompt

- 472 prompt tokens

````
You generate search queries for retrieving evidence from ONE video's memory.

**Report topic:** Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.

**Overall requirements:**


**Previous sections (summary):**
This is the first section

**Current section:** This section introduces the video’s opening segments (00:00:00-00:10:00), which focus on a measles resurgence in Canada and the U.S., featuring medical experts and public health alerts. Readers learn about the outbreak’s origin mystery, vaccination rates, and the risks to vulnerable populations, as well as the video’s initial framing as a public health report.

**Current section requirements:**
- Identify Dr. Earl Rubin, Dr. Anna Banerji, and Dr. Christopher Labos as key medical experts cited
- Note the on-screen text stating Canada eliminated measles in 1998 and current vaccination levels at 79%
- Confirm the video’s opening title card for 'The National' and its public health focus

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
