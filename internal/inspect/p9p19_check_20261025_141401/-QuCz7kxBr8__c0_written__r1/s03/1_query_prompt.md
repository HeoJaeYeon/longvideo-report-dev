# Section 3 — query-generation prompt

- 673 prompt tokens

````
You generate search queries for retrieving evidence from ONE video's memory.

**Report topic:** Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.

**Overall requirements:**


**Previous sections (summary):**
Already written in earlier sections (title, then the first sentence of each paragraph; citation numbers removed - they do NOT refer to the evidence of the current section):
Section 1: Introduction to the Participants and Setting
- Six men—Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player—are introduced as the main participants in the video.
- The video’s goal is established early: to test and evaluate the gadgets in a hands-on, competitive, yet lighthearted manner.
- The group’s interaction remains informal and humorous, with teammates reacting to performance with thumbs-up approval and score graphics flashing from 5 to 6, then 4.

Section 2: Testing the SKLZ Dribble Stick and the Straight Shooter Strap
- The group prepares to test the SKLZ Dribble Stick, a black training device with adjustable yellow arms, at 00:02:30.
- Following the dribble stick test, the group transitions to evaluating the Straight Shooter Strap.
- Later, a second player makes a shot (1/2), but audio commentary criticizes the product’s performance, noting it “fell off” and “snaps” when extended.

**Current section:** This section covers the testing of the Flick Glove and the Shot Coach device, including rules, player attempts, and the scoring system tied to sit-ups. It highlights the competitive nature of the challenges and the camaraderie among players, especially during synchronized shooting and training drills. Readers learn how gadgets are integrated into structured gameplay with consequences.

**Current section requirements:**
- Describe the Flick Glove’s rules and how shots are scored
- Note the Shot Coach device’s use in training and its impact on performance
- Record the sit-up forfeit and the players’ reactions

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
