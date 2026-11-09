# Section 5 — query-generation prompt

- 1110 prompt tokens

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

Section 3: Shift to Personal Tragedy and Institutional Failure, Followed by Athletic Triumph
- At 00:20:00, the video transitions into a segment focused on a misidentification tragedy at Montfort Hospital, which occurred on February 23, 2024.
- Heather Insley, identified as a mother from Picton, Ontario, is shown in a CBC News interview recounting how her family mourned the death of their son before realizing he was a stranger.
- The emotional aftermath is further illustrated by a grieving woman in a red sweater and glasses, speaking to an interviewer in a living room, her sorrow evident as she reflects on the loss of her son — only to later discover he was a strang

Section 4: Liendo’s Journey and Legacy
- At 00:30:00, the video shifts focus to Joshua Liendo, Canada’s first Black swimmer to win international gold, as he reflects on his journey from Trinidad to global podiums.
- Liendo’s reflections on his relocation are detailed at 00:31:00, where he recounts spending much of his childhood in Trinidad after being born there, before moving to Canada in 2012 at age 10.
- The segment underscores Liendo’s status as a trailblazer, with on-screen text repeatedly declaring him “swims into the history books”.

**Current section:** This section covers the video’s coverage of community disaster and recovery (00:40:00-00:50:00), including the destruction of a First Nation school, federal rebuilding pledges, and the eventual reopening of new schools. Readers learn about the fire’s impact, the community’s grief, and the government’s delayed but eventual support.

**Current section requirements:**
- Identify the fire that destroyed the only school on Eabametoong First Nation
- Note the federal pledge of over $13 million for modular classrooms
- Confirm the grand opening of new schools in Pikangikum and Wapekeka First Nations

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
