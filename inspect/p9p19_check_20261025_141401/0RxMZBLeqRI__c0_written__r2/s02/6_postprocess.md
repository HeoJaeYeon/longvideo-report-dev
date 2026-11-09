# Section 2 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 455 words → after removal 455 words

## 2. Start/end claim check (`boundary_claims`)

- none

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 15, "cited_sentences": 3, "checked_tokens": 10, "unsupported": 0, "miscited": 0, "uncited_claims": 0, "absence_statements": 0}`

- no findings

## 4. Citation conversion stats

- `{"text_citations": 16, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 0, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 5 of 12

## 5. Image-text time alignment

- no cited image

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Historical and Cultural Representation of Roma

The video transitions from historical sepia-toned photographs of Roma families in traditional attire to a modern-day street parade featuring participants in colorful traditional clothing and contemporary attire, marching with flags including the Roma flag (red wheel on green), alongside Ukrainian and EU flags. This visual shift occurs at 00:00:30, following the initial display of historical imagery [citation:txt3]. The narration affirms the Roma’s integral role in Balkan culture and history, while acknowledging the lack of public knowledge due to generational stigma, prejudice, and insufficient scholarly research [citation:txt3].

At 00:02:10, the video presents a migration map illustrating routes across Europe from “before 650” to “ca. 1700,” with the text “One single migration” overlaid — framing the Roma as originating from a unified historical movement [citation:txt1]. This map is immediately followed by a scene of a bearded man in a dark jacket speaking and gesturing, then turning to a whiteboard to draw a circle with a line through it — a scholarly visual symbolizing exclusion or misclassification [citation:txt1][citation:txt7]. The scholarly imagery reinforces the video’s focus on historical misidentification and the academic framing of Roma origins, particularly in the context of medieval Adriatic coastal zones [citation:txt7].

The transition from historical photos to the modern parade is deliberate and symbolic, visually contrasting Roma as both ancient and active participants in history. The parade, which includes women in colorful traditional clothing and men in contemporary attire, affirms Roma cultural assertion and continuity [citation:txt2][citation:txt12]. The presence of multiple flags — including the Roma flag, the Ukrainian flag, and the EU flag — underscores their integration into broader national and supranational narratives [citation:txt2][citation:txt9]. This juxtaposition counters earlier depictions of erasure by highlighting Roma agency and cultural visibility [citation:txt4].

The scholarly imagery of the man drawing a circle with a line through it is not merely symbolic; it is paired with topographical maps and discussions of medieval Adriatic origins, grounding the video’s claims in academic research [citation:txt7]. The visual of the “One single migration” text on the migration map serves as a unifying narrative amid linguistic fragmentation, emphasizing Roma’s shared historical roots despite regional variations in terminology such as “CIGANI,” “CIGÁNYOK,” “TIGANI,” and “ZIGEUNER” [citation:txt1][citation:txt7].

The video frames Roma as a people with enduring cultural continuity, despite historical stigma and systemic exclusion. The parade, with its vibrant costumes and flags, serves as a visual assertion of Roma presence and participation in contemporary society — a direct contrast to earlier scenes of marginalization and erasure [citation:txt3]. The scholarly and historical imagery, including the migration map and the symbolic drawing, provides a foundation for understanding Roma as a group with deep historical roots, misclassified and excluded by dominant narratives, yet persistently active in shaping their own cultural identity [citation:txt7].
```

## 7. Grounded body (exactly as in report.md)

```
# Historical and Cultural Representation of Roma

The video transitions from historical sepia-toned photographs of Roma families in traditional attire to a modern-day street parade featuring participants in colorful traditional clothing and contemporary attire, marching with flags including the Roma flag (red wheel on green), alongside Ukrainian and EU flags. This visual shift occurs at 00:00:30, following the initial display of historical imagery [6]. The narration affirms the Roma’s integral role in Balkan culture and history, while acknowledging the lack of public knowledge due to generational stigma, prejudice, and insufficient scholarly research [6].

At 00:02:10, the video presents a migration map illustrating routes across Europe from “before 650” to “ca. 1700,” with the text “One single migration” overlaid — framing the Roma as originating from a unified historical movement [7]. This map is immediately followed by a scene of a bearded man in a dark jacket speaking and gesturing, then turning to a whiteboard to draw a circle with a line through it — a scholarly visual symbolizing exclusion or misclassification [7][2]. The scholarly imagery reinforces the video’s focus on historical misidentification and the academic framing of Roma origins, particularly in the context of medieval Adriatic coastal zones [2].

The transition from historical photos to the modern parade is deliberate and symbolic, visually contrasting Roma as both ancient and active participants in history. The parade, which includes women in colorful traditional clothing and men in contemporary attire, affirms Roma cultural assertion and continuity [4][8]. The presence of multiple flags — including the Roma flag, the Ukrainian flag, and the EU flag — underscores their integration into broader national and supranational narratives [4][9]. This juxtaposition counters earlier depictions of erasure by highlighting Roma agency and cultural visibility [5].

The scholarly imagery of the man drawing a circle with a line through it is not merely symbolic; it is paired with topographical maps and discussions of medieval Adriatic origins, grounding the video’s claims in academic research [2]. The visual of the “One single migration” text on the migration map serves as a unifying narrative amid linguistic fragmentation, emphasizing Roma’s shared historical roots despite regional variations in terminology such as “CIGANI,” “CIGÁNYOK,” “TIGANI,” and “ZIGEUNER” [7][2].

The video frames Roma as a people with enduring cultural continuity, despite historical stigma and systemic exclusion. The parade, with its vibrant costumes and flags, serves as a visual assertion of Roma presence and participation in contemporary society — a direct contrast to earlier scenes of marginalization and erasure [6]. The scholarly and historical imagery, including the migration map and the symbolic drawing, provides a foundation for understanding Roma as a group with deep historical roots, misclassified and excluded by dominant narratives, yet persistently active in shaping their own cultural identity [2].
```

## 8. References used by this section (global numbers)

```
[2] 00:00:00–00:03:00 · episodic 3min: **[Event 1: Introduction and Context Setting]**  
The video opens with a disclaimer clarifying the use of “Gypsy” as a non-slandrous term for Roma/Romani, followed by a map of the Balkans and a montage of memes and hi...
[4] 00:00:00–00:00:30 · episodic 30sec: **[Event 1: Introduction and Context Setting]**  
The video opens with a disclaimer clarifying that “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s c...
[5] 00:00:00–00:10:00 · episodic 10min: **[Event 1: Introduction and Context Setting]**  
The video opens with a disclaimer clarifying the use of “Gypsy” as a non-slandrous term for Roma/Romani, followed by a map of the Balkans and a montage of memes and hi...
[6] 00:00:20–00:00:30 · episodic 10sec: The video begins with a title card reading "GYPSIES," followed by historical sepia-toned photographs showing Roma families in traditional attire, some gathered around a caravan and others posing formally. The scene tr...
[7] 00:02:10–00:02:20 · episodic 10sec: The video begins with text overlays displaying the words "CIGANI," "CIGÁNYOK," "TIGANI," and "ZIGEUNER," each paired with corresponding national flags, set against a blurred map of Europe. The scene transitions to a h...
[8] Video-level knowledge (semantic memory, no timestamp): (Street parade, includes, women in colorful traditional clothing)
[9] Video-level knowledge (semantic memory, no timestamp): (Street parade, includes, flags including Roma flag)
```
