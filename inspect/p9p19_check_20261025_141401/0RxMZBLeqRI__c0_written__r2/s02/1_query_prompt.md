# Section 2 — query-generation prompt

- 615 prompt tokens

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

**Current section:** This section details the video’s historical and cultural representation of Roma, using sepia-toned photos, parades, and scholarly imagery (00:10:00-00:20:00). It contrasts early misidentification with modern cultural assertion, showing Roma as both ancient and active participants in history. Readers learn how the video frames Roma as a people with enduring cultural continuity despite historical stigma.

**Current section requirements:**
- Identify the transition from historical photos to modern parade with flags
- Note the scholarly imagery of a man drawing a circle with line through it
- Observe the text 'One single migration' overlaid on a migration map

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
