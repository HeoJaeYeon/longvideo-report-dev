# Section 6 — query-generation prompt

- 1219 prompt tokens

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

Section 4: Roma Resilience and Cultural Endurance Amid Oppression
- At 00:29:50, a public rally unfolds where a woman speaks into a microphone while holding a sign.
- Earlier in the section, at 00:28:50, the video presents a young man in a yellow shirt and light pants dancing barefoot on a dirt ground in front of a large, weathered apartment building covered with numerous satellite dishes.
- The section concludes with a scene at 00:29:30, showing a man holding a young child while two others stand nearby in a rural, dilapidated setting.

Section 5: Global and Symbolic Conclusion: A Reflective Pause Across Continents
- At 00:30:00, the video shifts to a visually stylized scene featuring an anime-style girl standing before the Arc de Triomphe in Paris.
- The scene then transitions to the same character gesturing in front of a backdrop listing names, suggesting acknowledgment of contributors or collaborators.
- The video then opens on a stylized globe centered on Asia and Australia, encircled by a grid of national flags, symbolizing global unity or international perspective.
- The sequence from 00:30:00 to 00:30:32 concludes the video’s visual narrative with a symbolic global perspective, transitioning from a localized Parisian moment to an international scope before ending in a stark black screen.

**Current section:** Conclusion: This section briefly summarizes the main results shown in the video and answers the user request at a high level, using only findings covered in the earlier sections.

**Current section requirements:**
- Summarize the video’s depiction of Roma as historically marginalized, culturally resilient, and globally connected
- Confirm that the video concludes with symbolic imagery rather than a narrative resolution

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
