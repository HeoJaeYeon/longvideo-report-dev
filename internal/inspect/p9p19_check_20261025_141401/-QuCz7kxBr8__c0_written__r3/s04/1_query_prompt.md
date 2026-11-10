# Section 4 — query-generation prompt

- 879 prompt tokens

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

**Current section:** This section covers the synchronized shooting challenge using the Shot Coach device, including the ‘First Made Shot Shoots Silly String’ rule. Three men shoot simultaneously, and the winner is declared. The video shows the device’s use in training, including a drill with young players. Readers learn the game’s structure, the product’s role, and the celebratory outcome.

**Current section requirements:**
- Describe the synchronized shooting challenge and its rules
- Note the Shot Coach device’s demonstration and use
- List the winner and the silly string forfeit outcome

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
