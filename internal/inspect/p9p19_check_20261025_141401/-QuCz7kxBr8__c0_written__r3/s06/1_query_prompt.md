# Section 6 — query-generation prompt

- 1167 prompt tokens

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

Section 3: Testing the Straight Shooter Strap and Flick Glove
- At 00:04:30, a man in a white hoodie demonstrates the “Straight Shooter Strap,” a black elbow strap, on an outdoor basketball court.
- The shooting challenge begins with the strap in use.
- Three men then humorously rate the product: the white-hoodie man (ZHYPE) calls it suitable for kids but suggests a better gadget for beginners, scoring it “1.” They escalate to exaggerated scoring — “1,” “2,” then “-3k” — ending with a play
- The Flick Glove is introduced next.

Section 4: Synchronized Shooting Challenge and Shot Coach Training Drill
- At 00:18:00, three men gather on an outdoor basketball court under a clear blue sky to begin a playful shooting challenge governed by the rule: “FIRST MADE SHOT SHOOTS SILLY STRING AT LOSER.” The man in the blue jersey (No.
- As the countdown from three to one flashes on screen, all three men jump and shoot simultaneously — each ball arcs perfectly into the basket, triggering the next phase of the game.
- Following the game, a basketball coach in a black hoodie and white cap uses an orange “SHOT COACH” training device to guide two young players through a drill: “SHOOT FROM HALF COURT 5 TIMES WITH SHOT COACH.” He adjusts a wristband on one pl

Section 5: Never Ending Defender Training Device and Final Game Setup
- At 00:25:00, the “NEVER ENDING DEFENDER” training device is introduced on an outdoor basketball court under a clear sky.
- The shooting challenge begins with the man in the black t-shirt and pink shorts attempting his first shot, which misses.
- At 00:29:00, the video transitions to a larger group of six men on the outdoor court under a clear blue sky.
- Following the rules introduction, the group engages in a dynamic game using the padded training drills.
- At 00:28:00, three men engage in a casual discussion on the court.
- The video concludes with players continuing the game using the padded drills, with score overlays and player reactions emphasizing competitive energy.

**Current section:** Conclusion: This section briefly summarizes the main results shown in the video and answers the user request at a high level, using only findings covered in the earlier sections.

**Current section requirements:**
- Summarize the main outcomes shown in the video
- Answer the user request in one or two sentences

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
