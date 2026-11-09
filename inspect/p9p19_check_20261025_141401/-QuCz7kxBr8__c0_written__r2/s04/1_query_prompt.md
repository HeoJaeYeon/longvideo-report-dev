# Section 4 — query-generation prompt

- 855 prompt tokens

````
You generate search queries for retrieving evidence from ONE video's memory.

**Report topic:** Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.

**Overall requirements:**


**Previous sections (summary):**
Already written in earlier sections (title, then the first sentence of each paragraph; citation numbers removed - they do NOT refer to the evidence of the current section):
Section 1: Introduction: Participants, Setting, and Initial Goal
- The video opens on a sunny outdoor basketball court where six men—Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player—are gathered, dressed in athletic wear and holding basketballs near a hoop and trees.
- The setting is an outdoor basketball court under bright sunlight, with visible elements such as a basketball hoop, trees, and a pool in the background.
- The video’s first gadget, the “SPORTS DRIBBLE SPECS,” is introduced with a close-up of its black nylon straps and buckles.
- The group discusses the gadget’s usefulness, with the man in the white hoodie expressing discomfort with traditional basketballs forcing him to look down.

Section 2: First Gadget Test: SPORTS DRIBBLE SPECS Time Trial
- The first gadget tested in the video is the “SPORTS DRIBBLE SPECS,” introduced with a close-up of its black nylon straps and buckles.
- Players Chris and Zach are explicitly shown performing the drill.
- After the completion of the dribbling time trial, the segment transitions to the next gadget, the SKLZ Dribble Stick.

Section 3: SKLZ Dribble Stick Test and Transition to Next Challenge
- At 00:02:30, three men gather on the outdoor basketball court to begin the SKLZ Dribble Stick challenge.
- The gameplay proceeds with players attempting to dribble while avoiding the stick.
- After the dribble stick challenge, the group transitions to the next gadget, the “Straight Shooter Strap.” The man in the white hoodie introduces the strap, explaining how it stabilizes the elbow during shooting by preventing it from flarin
- The group’s reaction to the SKLZ Dribble Stick is captured in their ratings.
- The transition to the next gadget is smooth and well-prepared, with the group assembling and ready to begin the “Straight Shooter Strap” challenge.

**Current section:** This section focuses on the ‘Straight Shooter Strap’ test, including its demonstration and use. It shows a player attempting shooting drills with the strap, with score updates (e.g., 3/16). The segment includes humorous commentary, a forfeit suggestion (jumping jacks), and playful banter among players.

**Current section requirements:**
- Describe the strap’s function and how it is demonstrated
- List the score progression during the shooting drill
- Note the forfeit challenge (jumping jacks) and player reactions

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
