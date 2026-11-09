# Section 4 — query-generation prompt

- 888 prompt tokens

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

**Current section:** This section focuses on the video’s portrayal of Roma resilience amid systemic hardship, using scenes of rural life, protest, and personal agency (00:30:00-00:40:00). It includes moments of cultural endurance, such as dancing children and identity assertion, juxtaposed with institutional exclusion. Readers learn how the video balances trauma with resistance, showing Roma as active agents in their own history.

**Current section requirements:**
- Identify the Roma woman at rally saying 'I am also a Roma'
- Note the dancing boy in front of a satellite-dish-covered building
- Observe the animated character superimposed over urban architecture

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
