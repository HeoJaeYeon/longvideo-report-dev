# Section 3 — query-generation prompt

- 826 prompt tokens

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

Section 2: Unfolding Public Health Crisis: Measles Outbreak, Hospital Tragedy, and Emergency Response Failures
- At 00:03:00, the video shifts focus to a measles outbreak in the United States, with 41 confirmed cases across 16 states, centered on Manatee Bay Elementary near Fort Lauderdale, Florida.
- Simultaneously, the video documents a third patient death in a Montreal hospital waiting room, which is currently under coroner’s review.
- The video juxtaposes these domestic crises with international affairs.
- Visuals of hospital corridors and paramedics preparing ambulances are repeatedly shown, reinforcing the strain on emergency services.
- The video’s coverage of the measles outbreak and hospital deaths is framed within a broader context of public health alarm.

**Current section:** This section describes the video’s shift to personal tragedy and institutional failure (00:20:00-00:30:00), including the misidentification at Montfort Hospital and the emotional aftermath, followed by a transition to athletic triumph with Joshua Liendo’s gold medal win. Readers learn about the human cost of systemic errors and the contrast with athletic achievement.

**Current section requirements:**
- Identify Heather Insley as the grieving mother who learned her son was a stranger
- Note the CBC News coverage of the hospital’s official statement and formal review
- Confirm Joshua Liendo’s gold medal win in the Men’s 100m Butterfly at the Commonwealth Games

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
