# Section 3 — query-generation prompt

- 743 prompt tokens

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

**Current section:** This section covers the video’s depiction of institutionalized persecution, from Bismarck-era state control to Nazi-era camps and post-war assimilation (00:20:00-00:30:00). It shows archival footage, official documents, and symbolic imagery of forced displacement and genocide, while also highlighting moments of resistance and modern acknowledgment. Readers learn how the video traces state-sanctioned oppression and its legacy across political regimes.

**Current section requirements:**
- Identify the display of the 'Zigeuner-Buch' and Nuremberg Laws
- Note the Gestapo mugshots and images of Auschwitz-Birkenau
- Observe the 2007 Romanian headline about government acknowledging pogroms

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
