# Section 1 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 361 words → after removal 361 words

## 2. Start/end claim check (`boundary_claims`)

- ending_early: These images are juxtaposed with the final shot of the video’s opening montage: a still image of Barack Obama superimposed over dilapidated buildings, overlaid with the text “POREKLOM SAM CIGANIN” (“I am a Gypsy by origin”), which fades to black [citation:txt1][citation:txt2][citation:txt3][citation (cited [1, 2, 3, 4], latest cited end 00:10:00)

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 12, "cited_sentences": 3, "checked_tokens": 6, "unsupported": 0, "miscited": 0, "uncited_claims": 0, "absence_statements": 0}`

- no findings

## 4. Citation conversion stats

- `{"text_citations": 30, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 2, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 8 of 12

## 5. Image-text time alignment

- img1 frame 00:00:15: gap to text cited in the same paragraph 0.0 s (ranges ['00:00:00-00:00:30', '00:00:00-00:03:00']), to any text cited in the section 0.0 s
- img2 frame 00:03:55: gap to text cited in the same paragraph 55.0 s (ranges ['00:00:00-00:00:30', '00:00:00-00:03:00']), to any text cited in the section 0.0 s

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Section 1: Framing the Video — Disclaimers, Visual Montage, and the Opening Narrative on Roma Identity

The video opens with a disclaimer clarifying that the term “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s contested history and affirming its non-slandrous intent [citation:txt1][citation:txt2][citation:txt3][citation:txt4]. This establishes the video’s tone and frames its approach to terminology, positioning the content as grounded in historical and cultural context rather than pejorative language. Immediately following, the screen transitions to a map of the Balkans, setting a geographic anchor for the narrative [citation:txt1][citation:txt2][citation:txt3][citation:txt4].

A visual montage then unfolds, blending internet memes and historical battle tables. Among these, a satirical image labeled “POV: TITO INVENTING MACEDONIANS” appears, underscoring the video’s thematic focus on political manipulation and ethnic erasure in the region [citation:txt1][citation:txt2][citation:txt3][citation:txt4]. The audio commentary during this montage highlights entrenched ethnic hatred, noting how certain groups are disproportionately targeted — a thematic thread that will recur throughout the video [citation:txt1][citation:txt2][citation:txt3][citation:txt4].

The narrative then pivots to Roma identity, with a text overlay introducing their historical and cultural presence in the Balkans. Visuals accompany this, including a person walking past a trash can and turning away — a symbolic gesture possibly representing marginalization — followed by scenes of social tension, such as a shirtless man shouting outdoors and a bearded man speaking in front of a lit background [citation:txt1][citation:txt2][citation:txt3][citation:txt4]. These images are juxtaposed with the final shot of the video’s opening montage: a still image of Barack Obama superimposed over dilapidated buildings, overlaid with the text “POREKLOM SAM CIGANIN” (“I am a Gypsy by origin”), which fades to black [citation:txt1][citation:txt2][citation:txt3][citation:txt4]. This visual serves to reinforce the themes of identity erasure and societal stigma, anchoring the video’s central concern — the Roma’s complex, often negative social portrayal — in a striking, symbolic image [citation:txt1][citation:txt2][citation:txt3][citation:txt4].

The segment concludes with a transition to sepia-toned historical photographs of Roma families in traditional attire, visually affirming their long-standing presence in the Balkans [citation:txt1][citation:txt3]. This sets the stage for the video’s broader exploration of Roma history, culture, and the systemic forces that have shaped their visibility — or lack thereof — in public discourse.

![](citation:img1)  
![](citation:img2)
```

## 7. Grounded body (exactly as in report.md)

```
# Section 1: Framing the Video — Disclaimers, Visual Montage, and the Opening Narrative on Roma Identity

The video opens with a disclaimer clarifying that the term “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s contested history and affirming its non-slandrous intent [1][2][3][4]. This establishes the video’s tone and frames its approach to terminology, positioning the content as grounded in historical and cultural context rather than pejorative language. Immediately following, the screen transitions to a map of the Balkans, setting a geographic anchor for the narrative [1][2][3][4].

A visual montage then unfolds, blending internet memes and historical battle tables. Among these, a satirical image labeled “POV: TITO INVENTING MACEDONIANS” appears, underscoring the video’s thematic focus on political manipulation and ethnic erasure in the region [1][2][3][4]. The audio commentary during this montage highlights entrenched ethnic hatred, noting how certain groups are disproportionately targeted — a thematic thread that will recur throughout the video [1][2][3][4].

The narrative then pivots to Roma identity, with a text overlay introducing their historical and cultural presence in the Balkans. Visuals accompany this, including a person walking past a trash can and turning away — a symbolic gesture possibly representing marginalization — followed by scenes of social tension, such as a shirtless man shouting outdoors and a bearded man speaking in front of a lit background [1][2][3][4]. These images are juxtaposed with the final shot of the video’s opening montage: a still image of Barack Obama superimposed over dilapidated buildings, overlaid with the text “POREKLOM SAM CIGANIN” (“I am a Gypsy by origin”), which fades to black [1][2][3][4]. This visual serves to reinforce the themes of identity erasure and societal stigma, anchoring the video’s central concern — the Roma’s complex, often negative social portrayal — in a striking, symbolic image [1][2][3][4].

The segment concludes with a transition to sepia-toned historical photographs of Roma families in traditional attire, visually affirming their long-standing presence in the Balkans [1][3]. This sets the stage for the video’s broader exploration of Roma history, culture, and the systemic forces that have shaped their visibility — or lack thereof — in public discourse.

![Figure 1 (00:00:15)](frames/0RxMZBLeqRI_00001000.jpg)

*Figure 1. Frame at 00:00:15 (clip 00:00:10–00:00:20). The video segment begins with a text overlay discussing the historical and cultural presence of the Roma, also known as Gypsies, in the Balkans, while simultaneously showing a person in a light blue shirt and dark pants walking past a trash can and then turning away. The scene cuts to a man in a...*

![Figure 2 (00:03:55)](frames/0RxMZBLeqRI_00035000.jpg)

*Figure 2. Frame at 00:03:55 (clip 00:03:50–00:04:00). A hand writes with a fountain pen on a piece of paper, with a magnifying glass nearby. The scene transitions to a close-up of a newspaper titled "Hannoversches Tageblatt, General-Anzeiger," dated October 24, 1865. The view then shifts to a topographical map of Europe, followed by a man with long...*
```

## 8. References used by this section (global numbers)

```
[1] 00:00:00–00:00:30 · episodic 30sec: **[Event 1: Introduction and Context Setting]**  
The video opens with a disclaimer clarifying that “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s c...
[2] 00:00:00–00:00:10 · episodic 10sec: A disclaimer appears on a black screen, explaining that the term “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s complicated history and clarifying t...
[3] 00:00:00–00:03:00 · episodic 3min: **[Event 1: Introduction and Context Setting]**  
The video opens with a disclaimer clarifying the use of “Gypsy” as a non-slandrous term for Roma/Romani, followed by a map of the Balkans and a montage of memes and hi...
[4] 00:00:00–00:10:00 · episodic 10min: **[Event 1: Introduction and Context Setting]**  
The video opens with a disclaimer clarifying the use of “Gypsy” as a non-slandrous term for Roma/Romani, followed by a map of the Balkans and a montage of memes and hi...
```
