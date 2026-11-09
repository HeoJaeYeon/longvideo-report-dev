# Section 2 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 535 words → after removal 535 words

## 2. Start/end claim check (`boundary_claims`)

- none

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 23, "cited_sentences": 1, "checked_tokens": 2, "unsupported": 1, "miscited": 0, "uncited_claims": 1, "absence_statements": 0}`

- **uncited**  `['00:00:20']` cited [] — The video transitions from sepia-toned historical photographs of Roma families in traditional attire to modern parade scenes at approximately 00:00:20.
- **unsupported** quote `very little [public] knowledge` cited ['txt1', 'txt2'] — The narration during this transition acknowledges the historical invisibility of the Roma, attributing it to “generational stigma, prejudice, and a lack of research,” which has resulted in “very little [public] knowledge” about them [citation:txt1][citation:txt2].

## 4. Citation conversion stats

- `{"text_citations": 6, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 0, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 9 of 12

## 5. Image-text time alignment

- no cited image

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Historical and Cultural Framing of Roma Identity

The video transitions from sepia-toned historical photographs of Roma families in traditional attire to modern parade scenes at approximately 00:00:20. The historical images, some showing families gathered around caravans and others posing formally, visually affirm the Roma’s long-standing presence in the Balkans [citation:txt1][citation:txt3]. This visual sequence is followed by a cut to a modern-day street parade, where participants—women in colorful traditional clothing and men in contemporary attire—march while carrying flags, including the Roma flag (a red wheel on a green background), alongside the Ukrainian and European Union flags [citation:txt1][citation:txt2].

The narration during this transition acknowledges the historical invisibility of the Roma, attributing it to “generational stigma, prejudice, and a lack of research,” which has resulted in “very little [public] knowledge” about them [citation:txt1][citation:txt2]. This acknowledgment is framed as a counterpoint to earlier depictions of erasure, affirming Roma agency and cultural continuity across centuries. The juxtaposition of historical stills with vibrant, celebratory parade footage visually contrasts exclusion with cultural affirmation. The parade scenes, with their colorful attire and symbolic flags, represent a reclaiming of visibility and pride, directly opposing the earlier visual cues of marginalization.

The video’s visual contrast between exclusion and celebration is further reinforced by the inclusion of both archival and contemporary imagery. For instance, the transition from black-and-white historical depictions of Roma life to modern, color-saturated parade footage underscores a narrative arc of resilience. The Roma flag, prominently displayed among national and supranational symbols, signals both cultural identity and political assertion. This visual framing does not merely document history but actively constructs a counter-narrative to the erasure historically imposed upon Roma communities.

The narration’s recognition of stigma and lack of scholarly attention serves to contextualize the Roma’s historical invisibility, while the parade scenes affirm their enduring presence and agency. The juxtaposition of these elements—historical documentation and modern celebration—creates a powerful visual argument for cultural continuity. The video does not present a linear progression of history but rather a layered, interwoven narrative that acknowledges past marginalization while celebrating present-day visibility and cultural pride.

The transition from historical photos to parade scenes is not merely aesthetic but conceptual, marking a shift from passive documentation to active affirmation. The Roma flag, carried alongside national symbols, suggests integration and recognition within broader political frameworks. This visual strategy aligns with the video’s broader goal of countering erasure by affirming Roma agency and cultural continuity.

The visual contrast between exclusion and celebration is further emphasized by the use of both sepia-toned archival images and vibrant modern footage. The parade scenes, with their dynamic movement and symbolic flags, stand in stark contrast to the static, often somber historical photographs. This contrast visually reinforces the narrative of resilience and cultural endurance, challenging the historical invisibility acknowledged in the narration.

The video’s framing of Roma identity through visual juxtapositions—from historical photos to modern parades—serves to affirm both the historical depth and contemporary vitality of Roma culture. The transition from sepia-toned images to color-saturated parade scenes, accompanied by narration acknowledging historical invisibility, constructs a narrative of resilience and cultural continuity. The visual contrast between exclusion and celebration underscores the video’s central argument: that Roma identity, despite centuries of marginalization, remains vibrant, visible, and actively asserted.
```

## 7. Grounded body (exactly as in report.md)

```
# Historical and Cultural Framing of Roma Identity

The video transitions from sepia-toned historical photographs of Roma families in traditional attire to modern parade scenes at approximately 00:00:20. The historical images, some showing families gathered around caravans and others posing formally, visually affirm the Roma’s long-standing presence in the Balkans [5][3]. This visual sequence is followed by a cut to a modern-day street parade, where participants—women in colorful traditional clothing and men in contemporary attire—march while carrying flags, including the Roma flag (a red wheel on a green background), alongside the Ukrainian and European Union flags [5][1].

The narration during this transition acknowledges the historical invisibility of the Roma, attributing it to “generational stigma, prejudice, and a lack of research,” which has resulted in “very little [public] knowledge” about them [5][1]. This acknowledgment is framed as a counterpoint to earlier depictions of erasure, affirming Roma agency and cultural continuity across centuries. The juxtaposition of historical stills with vibrant, celebratory parade footage visually contrasts exclusion with cultural affirmation. The parade scenes, with their colorful attire and symbolic flags, represent a reclaiming of visibility and pride, directly opposing the earlier visual cues of marginalization.

The video’s visual contrast between exclusion and celebration is further reinforced by the inclusion of both archival and contemporary imagery. For instance, the transition from black-and-white historical depictions of Roma life to modern, color-saturated parade footage underscores a narrative arc of resilience. The Roma flag, prominently displayed among national and supranational symbols, signals both cultural identity and political assertion. This visual framing does not merely document history but actively constructs a counter-narrative to the erasure historically imposed upon Roma communities.

The narration’s recognition of stigma and lack of scholarly attention serves to contextualize the Roma’s historical invisibility, while the parade scenes affirm their enduring presence and agency. The juxtaposition of these elements—historical documentation and modern celebration—creates a powerful visual argument for cultural continuity. The video does not present a linear progression of history but rather a layered, interwoven narrative that acknowledges past marginalization while celebrating present-day visibility and cultural pride.

The transition from historical photos to parade scenes is not merely aesthetic but conceptual, marking a shift from passive documentation to active affirmation. The Roma flag, carried alongside national symbols, suggests integration and recognition within broader political frameworks. This visual strategy aligns with the video’s broader goal of countering erasure by affirming Roma agency and cultural continuity.

The visual contrast between exclusion and celebration is further emphasized by the use of both sepia-toned archival images and vibrant modern footage. The parade scenes, with their dynamic movement and symbolic flags, stand in stark contrast to the static, often somber historical photographs. This contrast visually reinforces the narrative of resilience and cultural endurance, challenging the historical invisibility acknowledged in the narration.

The video’s framing of Roma identity through visual juxtapositions—from historical photos to modern parades—serves to affirm both the historical depth and contemporary vitality of Roma culture. The transition from sepia-toned images to color-saturated parade scenes, accompanied by narration acknowledging historical invisibility, constructs a narrative of resilience and cultural continuity. The visual contrast between exclusion and celebration underscores the video’s central argument: that Roma identity, despite centuries of marginalization, remains vibrant, visible, and actively asserted.
```

## 8. References used by this section (global numbers)

```
[1] 00:00:00–00:00:30 · episodic 30sec: **[Event 1: Introduction and Context Setting]**  
The video opens with a disclaimer clarifying that “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s c...
[3] 00:00:00–00:03:00 · episodic 3min: **[Event 1: Introduction and Context Setting]**  
The video opens with a disclaimer clarifying the use of “Gypsy” as a non-slandrous term for Roma/Romani, followed by a map of the Balkans and a montage of memes and hi...
[5] 00:00:20–00:00:30 · episodic 10sec: The video begins with a title card reading "GYPSIES," followed by historical sepia-toned photographs showing Roma families in traditional attire, some gathered around a caravan and others posing formally. The scene tr...
```
