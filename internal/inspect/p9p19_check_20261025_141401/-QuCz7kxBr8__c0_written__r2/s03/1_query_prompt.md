# Section 3 — query-generation prompt

- 698 prompt tokens

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

**Current section:** This section details the SKLZ Dribble Stick test, including its rules (dribble while avoiding the stick, touch = 5 laps). It shows players rating the gadget, with humorous commentary. The segment ends with the group preparing for the next challenge, the ‘Straight Shooter Strap.’

**Current section requirements:**
- Describe the SKLZ Dribble Stick’s rules and gameplay
- List the ratings given by players (e.g., 8/10, 7)
- Note the transition to the next gadget and the group’s reaction

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
