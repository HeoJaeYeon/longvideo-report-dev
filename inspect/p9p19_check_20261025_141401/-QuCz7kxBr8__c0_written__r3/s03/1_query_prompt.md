# Section 3 — query-generation prompt

- 765 prompt tokens

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

Section 2: First Gadget Tested: SPORTS DRIBBLE SPECS and SKLZ Dribble Stick Challenge
- The first gadget tested is the “SPORTS DRIBBLE SPECS,” with one player donning the goggles and preparing for a dribbling time trial.
- After the time trial, the group discusses the gadget’s usefulness.
- The SKLZ Dribble Stick is tested in a separate challenge.
- The video does not show the actual execution of the SKLZ Dribble Stick challenge beyond the setup and rule review.
- Ratings for the SPORTS DRIBBLE SPECS are not explicitly stated in the retrieved evidence.
- The video transitions from the dribbling time trial to the SKLZ Dribble Stick challenge without showing the actual test, leaving the performance outcomes and reactions to the stick challenge unrecorded in the evidence.

**Current section:** This section details the testing of the Straight Shooter Strap and the Flick Glove. A man in a white hoodie demonstrates the strap’s elbow stabilization, followed by a shooting sequence with varying success. Later, the Flick Glove is introduced with rules involving sit-ups as forfeits. Readers learn how each gadget is tested, the players’ reactions, and the humorous consequences of failure.

**Current section requirements:**
- Describe the Straight Shooter Strap’s demonstration and scoring
- Note the Flick Glove’s rules and the forfeit (100 sit-ups)
- List the players’ performance and reactions (e.g., missed shots, forfeits)

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
