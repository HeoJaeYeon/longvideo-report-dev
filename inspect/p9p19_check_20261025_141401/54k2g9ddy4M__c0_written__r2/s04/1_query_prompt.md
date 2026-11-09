# Section 4 — query-generation prompt

- 940 prompt tokens

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

Section 2: Unfolding Crisis: Measles Outbreak, Hospital Strain, and Third Patient Death in Montreal
- At 00:10:00, the video shifts focus to the escalating public health emergency, centering on the measles resurgence in Canada and its cascading consequences.
- The video then transitions to hospital settings, capturing the strain on emergency response systems.
- At 00:15:00, the video highlights a critical turning point: the third patient death in a Montreal hospital waiting room, currently under coroner’s review.
- The video also includes a man in a white shirt with a red collar, who warns that if patient transportation isn’t prioritized — through increased vehicle deployment — similar tragic events are certain to recur.

Section 3: Joshua Liendo’s Gold Medal Triumph and Personal Reflections
- At 00:24:00, the video shifts focus to Canadian swimmer Joshua Liendo, who is shown winning gold in the Men’s 100m Butterfly at the Commonwealth Games.
- Later, at 00:27:00, Liendo is shown in a white Florida Gators shirt and gold chain, seated poolside and discussing his training regimen and the influence of the University of Florida’s environment on his performance.
- At 00:31:30, Liendo competes in the Men’s 100m Butterfly Final, extending his lead to secure victory amid roaring Canadian fan support.

**Current section:** This section covers the tragic misidentification at Montfort Hospital and the fire disaster in Eabametoong First Nation (00:30:00-00:40:00), including family grief, institutional response, and community recovery. Readers learn about the human cost of systemic failure and the federal government’s role in rebuilding schools and restoring education.

**Current section requirements:**
- Show a grieving mother learning her son was misidentified
- Display footage of a school destroyed by fire in Eabametoong First Nation
- Include text stating the federal government pledged $13 million for modular classrooms

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
