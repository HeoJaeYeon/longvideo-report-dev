# Section 3 — query-generation prompt

- 813 prompt tokens

````
You generate search queries for retrieving evidence from ONE video's memory.

**Report topic:** Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.

**Overall requirements:**


**Previous sections (summary):**
Already written in earlier sections (title, then the first sentence of each paragraph; citation numbers removed - they do NOT refer to the evidence of the current section):
Section 1: Framing Roma Identity Through Historical and Cultural Context
- The video opens with a disclaimer displayed on a black screen, clarifying that the term “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s contested history and affirming its 
- At 00:00:00, the video also features a text overlay that introduces the historical and cultural presence of the Roma in the Balkans, while visuals show a person walking past a trash can and then turning away — possibly symbolizing marginali
- The video further contextualizes Roma identity through visual and textual elements.

Section 2: Historical and Cultural Portrayal of Roma from 00:10:00–00:20:00
- At 00:10:00, the video shifts focus to 15th-century Eastern Europe, presenting a montage of historical visuals—sepia-toned photographs, paintings, and CGI animations—to depict Roma labor and warfare under Romanian rulers post-1471.
- The video deepens its symbolic layering by framing *Tiganiada* as a metaphor for conquest, transformation, and resistance.
- At 00:12:40, the video opens with a portrait of Ion Budai-Deleanu, the Romanian poet and author of *Tiganiada*, followed by a computer-generated medieval battle animation.

**Current section:** This section covers the institutionalized persecution of Roma under German and Eastern European regimes from 00:20:00-00:30:00, including archival footage of Nazi camps, Gestapo documentation, and state-sponsored assimilation policies in Bulgaria. It uses stark visual contrasts — from concentration camp imagery to modern-day protests — to show the continuity of systemic marginalization. Readers learn how the video documents state-sanctioned violence, racial categorization, and forced assimilation across multiple regimes.

**Current section requirements:**
- Identify Gestapo mugshots and camp imagery (e.g., Ludwig Horvath, Zyklon B)
- Note the 1942 deportation to Auschwitz-Birkenau
- Observe text overlays about Bulgaria’s ‘Process of Revival’ and name assimilation

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
