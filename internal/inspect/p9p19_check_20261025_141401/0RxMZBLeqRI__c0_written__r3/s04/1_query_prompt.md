# Section 4 — query-generation prompt

- 1000 prompt tokens

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

Section 3: Institutionalized Persecution of Roma under German and Eastern European Regimes
- The video transitions from earlier historical portrayals of Roma identity to a stark depiction of institutionalized persecution, focusing on state-sanctioned violence and racial categorization from 00:20:00 to 00:30:00.
- At 00:22:00, the video displays the Nazi-era document *Die Nürnberger Gesetze* (The Nuremberg Laws), which categorizes individuals into racial groups such as “Deutschblütiger,” “Mischling 2.
- At 00:22:30, the video shows a black-and-white mugshot of Maria Bihari, a Roma girl born November 9, 1935, presented in three angles — frontal, three-quarter, and profile — before transitioning to an outdoor Roma camp setting.

**Current section:** This section shows the video’s focus on Roma resilience and cultural endurance amid oppression, using scenes from rural life, personal testimony, and symbolic animation from 00:30:00-00:40:00. It juxtaposes archival hardship with moments of agency — such as a Roma woman asserting identity or a dancing boy in front of a satellite-dish-covered building — to highlight quiet resistance. Readers learn how the video ends by emphasizing human dignity and cultural continuity despite historical trauma.

**Current section requirements:**
- Identify the Roma woman speaking at a rally: ‘I am also a Roma’
- Note the dancing boy in front of a satellite-dish-covered building
- Observe the final scene of a man holding a child in a dilapidated rural setting

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
