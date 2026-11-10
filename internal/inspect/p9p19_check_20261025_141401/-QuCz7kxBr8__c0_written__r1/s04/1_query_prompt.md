# Section 4 — query-generation prompt

- 834 prompt tokens

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

Section 3: Testing the Flick Glove and Shot Coach: Rules, Performance, and Consequences
- At 00:08:00, a shooting challenge begins with the Flick Glove, a device featuring finger loops and a rectangular screen, as explained by a man in a black hoodie and white cap who holds the glove while two others observe.
- During the challenge, players attempt shots while wearing the glove.
- The scoring system is directly tied to performance: the fewest baskets result in a physical consequence.
- The Shot Coach device is used in a structured training drill.
- The Shot Coach is also used in a synchronized shooting drill.
- The Flick Glove and Shot Coach are both presented as tools that integrate into structured gameplay, with consequences tied to performance.

**Current section:** This section details the “First Made Shot Shoots Silly String” game, including the rules, synchronized shooting, and the winner’s celebration. It also covers the defensive drills with padded shields and the “Never Ending Defender” training challenge, showing how the group transitions between game modes. Readers learn how the video concludes with a mix of competition, humor, and product reinforcement.

**Current section requirements:**
- Describe the silly string game’s rules and outcome
- Note the defensive drills with padded shields and their setup
- Record the “Never Ending Defender” challenge and its scoring system

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
