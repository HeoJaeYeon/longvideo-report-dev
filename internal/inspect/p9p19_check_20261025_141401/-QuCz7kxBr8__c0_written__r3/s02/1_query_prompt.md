# Section 2 — query-generation prompt

- 608 prompt tokens

````
You generate search queries for retrieving evidence from ONE video's memory.

**Report topic:** Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.

**Overall requirements:**


**Previous sections (summary):**
Already written in earlier sections (title, then the first sentence of each paragraph; citation numbers removed - they do NOT refer to the evidence of the current section):
Section 1: Introduction of Participants, Setting, and Tone
- Six men—Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player—gather on an outdoor basketball court to test 12 viral sports gadgets.
- The setting is an outdoor basketball court under a clear, sunny sky.
- The man in the white hoodie plays a central role in setting the tone.
- The video opens with this group introduction, transitioning shortly into a countdown and gear review, beginning with a close-up of black nylon straps, signaling the start of hands-on testing.

**Current section:** This section covers the first gadget tested: the SPORTS DRIBBLE SPECS, including the dribbling time trial and the SKLZ Dribble Stick challenge. Players like Chris and Zach compete, with timers recording their times, and the group discusses the gadgets’ usefulness. Readers learn the rules, performance outcomes, and reactions to the first two gadgets, including score graphics and team feedback.

**Current section requirements:**
- Note the dribbling time trial rules and recorded times (e.g., 10:85, 9:51)
- Describe the SKLZ Dribble Stick rules and how it is tested
- List the ratings given (e.g., 8/10, 7) and humorous commentary

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
