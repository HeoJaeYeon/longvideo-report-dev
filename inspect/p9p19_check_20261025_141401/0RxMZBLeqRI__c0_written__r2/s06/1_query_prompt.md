# Section 6 — query-generation prompt

- 1102 prompt tokens

````
You generate search queries for retrieving evidence from ONE video's memory.

**Report topic:** Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.

**Overall requirements:**


**Previous sections (summary):**
Already written in earlier sections (title, then the first sentence of each paragraph; citation numbers removed - they do NOT refer to the evidence of the current section):
Section 1: Framing Roma Identity Through Historical and Cultural Context
- The video opens with a disclaimer displayed on a black screen, clarifying that the term “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s complicated history and affirming th
- The visual sequence continues with a text overlay introducing the historical and cultural presence of the Roma in the Balkans, while juxtaposing it with symbolic imagery.
- The video’s initial framing positions Roma as both marginalized and culturally significant.
- The visual and textual elements in this section collectively set up the video’s critical exploration of erasure and representation.

Section 2: Historical and Cultural Representation of Roma
- The video transitions from historical sepia-toned photographs of Roma families in traditional attire to a modern-day street parade featuring participants in colorful traditional clothing and contemporary attire, marching with flags includin
- At 00:02:10, the video presents a migration map illustrating routes across Europe from “before 650” to “ca.
- The transition from historical photos to the modern parade is deliberate and symbolic, visually contrasting Roma as both ancient and active participants in history.

Section 3: Institutionalized Persecution: From Bismarck-Era Surveillance to Post-War Acknowledgment
- The video transitions from its earlier portrayal of Roma cultural continuity to a stark depiction of institutionalized persecution, beginning with the establishment of state surveillance in late 19th-century Bavaria.
- At 00:21:50, the video presents the “Zigeuner-Buch” (Gypsy Book), a document used for racial categorization and surveillance, shown with its cover and an open page bearing a stamped seal — a bureaucratic tool enforcing systemic discriminati
- The video then explicitly documents the racial categorization codified under Nazi Germany.
- The persecution is further illustrated through archival imagery.
- The video concludes this section with a moment of modern reckoning.

Section 4: Roma Resilience Amid Systemic Hardship: Cultural Endurance and Personal Agency
- At 00:29:30, the video presents an animated woman in traditional attire standing with open arms against a cityscape, symbolizing cultural presence or welcome.
- The video then shifts to an aerial view of a residential area with cluttered balconies and debris piled at building bases, hinting at displacement, neglect, or aftermath of conflict.
- The segment concludes with an animated character superimposed over a real-world archway with traffic, blending symbolic representation with urban reality — possibly signifying cultural endurance or resistance within a modern setting.

Section 5: Global Perspective: From Paris to the World
- At 00:30:00, the video presents an anime-style girl standing before the Arc de Triomphe in Paris.
- The video then shifts to a stylized globe centered on Asia and Australia, encircled by a grid of national flags, symbolizing international scope or global unity.
- The anime girl’s recurring visual presence across different settings — from Paris to the global backdrop — underscores continuity and symbolic resonance, aligning with earlier portrayals of Roma cultural endurance.
- The transition to black after the stylized globe is abrupt and unaccompanied by text or sound, indicating an intentional pause rather than an error or technical glitch.

**Current section:** Conclusion: This section briefly summarizes the main results shown in the video and answers the user request at a high level, using only findings covered in the earlier sections.

**Current section requirements:**
- Summarize the video’s portrayal of Roma identity from erasure to resilience
- Confirm the video’s conclusion with a global, symbolic coda

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
