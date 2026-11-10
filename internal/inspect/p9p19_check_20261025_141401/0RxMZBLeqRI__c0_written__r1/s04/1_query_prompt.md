# Section 4 — query-generation prompt

- 848 prompt tokens

````
You generate search queries for retrieving evidence from ONE video's memory.

**Report topic:** Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.

**Overall requirements:**


**Previous sections (summary):**
Already written in earlier sections (title, then the first sentence of each paragraph; citation numbers removed - they do NOT refer to the evidence of the current section):
Section 1: Framing the Video — Disclaimers, Visual Montage, and the Opening Narrative on Roma Identity
- The video opens with a disclaimer clarifying that the term “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s contested history and affirming its non-slandrous intent.
- A visual montage then unfolds, blending internet memes and historical battle tables.
- The narrative then pivots to Roma identity, with a text overlay introducing their historical and cultural presence in the Balkans.
- The segment concludes with a transition to sepia-toned historical photographs of Roma families in traditional attire, visually affirming their long-standing presence in the Balkans.

Section 2: Historical and Cultural Framing of Roma Identity
- The video transitions from sepia-toned historical photographs of Roma families in traditional attire to modern parade scenes at approximately 00:00:20.
- The narration during this transition acknowledges the historical invisibility of the Roma, attributing it to “generational stigma, prejudice, and a lack of research,” which has resulted in “very little [public] knowledge” about them.
- The video’s visual contrast between exclusion and celebration is further reinforced by the inclusion of both archival and contemporary imagery.

Section 3: Depiction of Roma as Historically Misclassified and Systematically Stigmatized
- At 00:00:30, the video presents a man in a yellow lab coat carefully transferring liquid with a pipette, symbolizing scientific precision or experimentation.
- The video then transitions to a Minecraft gameplay scene where a player mines, symbolizing labor or resource extraction.
- The video’s depiction of scientific exclusion is further reinforced by the lab-coated figure and the red “X”-marked scientist, symbolizing how Roma have been systematically excluded from scholarly and institutional frameworks.

**Current section:** This section details the video’s historical narrative of Roma origins and early misidentification, using maps, 13th-century battle imagery, and geopolitical framing to show how Roma were labeled by empires. Readers learn how the video positions Roma not as a distinct ethnic group but as a product of historical misreading and geopolitical conflict.

**Current section requirements:**
- Identify the 13th-century map anchoring Roma presence
- Note the 'VS' graphic depicting Seljuk Turks vs. Byzantine Empire
- Recognize the narration explaining Roma were mistaken for Turks by Byzantines

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
