# Section 2 — query-generation prompt

- 671 prompt tokens

````
You generate search queries for retrieving evidence from ONE video's memory.

**Report topic:** Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.

**Overall requirements:**


**Previous sections (summary):**
Already written in earlier sections (title, then the first sentence of each paragraph; citation numbers removed - they do NOT refer to the evidence of the current section):
Section 1: Introduction to the Video’s Opening Segments (00:00:00-00:10:00)
- The video opens with a segment from CBC News’ “The National,” hosted by Ian Henneman, delivering a public health report on the resurgence of measles in Canadian communities.
- Within the first minute, the video transitions to footage of a Canadian swimmer, Joshua Liendo, competing in a butterfly stroke race, followed by interview segments where he reflects on his journey as a trailblazer for Black swimmers.
- At 00:01:30, the video juxtaposes everyday family life — a man swinging a child at a Toronto playground — with the ongoing public health concern, as the same news ticker continues to appear.
- The video introduces Dr.
- At 00:02:00, Dr.

**Current section:** This section covers the unfolding public health crisis (00:10:00-00:20:00), including a measles outbreak in the U.S. centered on a school, the death of a patient in Montreal, and systemic emergency response failures. Readers learn about parental concerns, coroner reviews, and the video’s juxtaposition of health emergencies with political and economic stories.

**Current section requirements:**
- Note the U.S. measles outbreak with 41 cases in 16 states, centered on Manatee Bay Elementary
- Identify the third patient death in a Montreal hospital waiting room under coroner’s review
- Confirm the on-screen alerts and visuals of hospital corridors and paramedics preparing ambulances

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
