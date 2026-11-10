# Section 1 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 478 words → after removal 478 words

## 2. Start/end claim check (`boundary_claims`)

- none

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 16, "cited_sentences": 6, "checked_tokens": 9, "unsupported": 0, "miscited": 0, "uncited_claims": 0, "absence_statements": 0}`

- no findings

## 4. Citation conversion stats

- `{"text_citations": 11, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 0, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 7 of 12

## 5. Image-text time alignment

- no cited image

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Section 1: Framing Roma Identity Through Historical and Cultural Context

The video opens with a disclaimer displayed on a black screen, clarifying that the term “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s complicated history and affirming that it is not intended as a slur [citation:txt1]. This disclaimer sets the tone for the video’s approach to terminology, positioning it as academically and sensitively informed. Immediately following, the screen transitions to a map of the Balkan region, visually anchoring the narrative in geography [citation:txt1]. This is followed by a montage of internet memes and historical battle tables, including a satirical image labeled “POV: TITO INVENTING MACEDONIANS,” which underscores the video’s thematic focus on ethnic hatred and political manipulation in the region [citation:txt1][citation:txt4].

The visual sequence continues with a text overlay introducing the historical and cultural presence of the Roma in the Balkans, while juxtaposing it with symbolic imagery. One such image shows a person walking past a trash can and then turning away — a visual metaphor for marginalization [citation:txt2]. The montage continues with scenes of social tension, including a shirtless man shouting outdoors and a bearded man speaking in front of a lit background, suggesting protest or commentary [citation:txt2]. The segment concludes with a still image of Barack Obama superimposed over dilapidated buildings, overlaid with the text “POREKLOM SAM CIGANIN” (“I am a Gypsy by origin”), before fading to black — a powerful visual that frames identity erasure and societal stigma [citation:txt2][citation:txt3].

The video’s initial framing positions Roma as both marginalized and culturally significant. While the disclaimer and historical maps establish a scholarly context, the use of memes and satirical imagery introduces a critical, often humorous, lens. The overlay “POREKLOM SAM CIGANIN” over Obama’s image, in particular, serves as a symbolic intervention — it juxtaposes global political symbolism with the lived reality of Roma exclusion, highlighting how identity is weaponized and erased [citation:txt5]. The montage of battle tables and memes, including the “TITO INVENTING MACEDONIANS” image, reinforces the video’s focus on systemic exclusion and the historical construction of ethnic boundaries [citation:txt1].

The visual and textual elements in this section collectively set up the video’s critical exploration of erasure and representation. The opening disclaimer and historical maps establish a foundation of academic rigor, while the memes and symbolic imagery introduce a tone of critique and irony. The video’s initial focus on identity, history, and systemic exclusion is clearly evident, as the montage of images — from the trash can to the Obama superimposition — visually narrates the Roma experience as one of marginalization, cultural invisibility, and political manipulation. The section concludes with the fading black screen, leaving the viewer with the lingering image of “POREKLOM SAM CIGANIN,” a phrase that encapsulates the video’s central theme: the erasure of Roma identity despite their enduring presence and cultural significance [citation:txt3].
```

## 7. Grounded body (exactly as in report.md)

```
# Section 1: Framing Roma Identity Through Historical and Cultural Context

The video opens with a disclaimer displayed on a black screen, clarifying that the term “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s complicated history and affirming that it is not intended as a slur [1]. This disclaimer sets the tone for the video’s approach to terminology, positioning it as academically and sensitively informed. Immediately following, the screen transitions to a map of the Balkan region, visually anchoring the narrative in geography [1]. This is followed by a montage of internet memes and historical battle tables, including a satirical image labeled “POV: TITO INVENTING MACEDONIANS,” which underscores the video’s thematic focus on ethnic hatred and political manipulation in the region [1][2].

The visual sequence continues with a text overlay introducing the historical and cultural presence of the Roma in the Balkans, while juxtaposing it with symbolic imagery. One such image shows a person walking past a trash can and then turning away — a visual metaphor for marginalization [3]. The montage continues with scenes of social tension, including a shirtless man shouting outdoors and a bearded man speaking in front of a lit background, suggesting protest or commentary [3]. The segment concludes with a still image of Barack Obama superimposed over dilapidated buildings, overlaid with the text “POREKLOM SAM CIGANIN” (“I am a Gypsy by origin”), before fading to black — a powerful visual that frames identity erasure and societal stigma [3][4].

The video’s initial framing positions Roma as both marginalized and culturally significant. While the disclaimer and historical maps establish a scholarly context, the use of memes and satirical imagery introduces a critical, often humorous, lens. The overlay “POREKLOM SAM CIGANIN” over Obama’s image, in particular, serves as a symbolic intervention — it juxtaposes global political symbolism with the lived reality of Roma exclusion, highlighting how identity is weaponized and erased [5]. The montage of battle tables and memes, including the “TITO INVENTING MACEDONIANS” image, reinforces the video’s focus on systemic exclusion and the historical construction of ethnic boundaries [1].

The visual and textual elements in this section collectively set up the video’s critical exploration of erasure and representation. The opening disclaimer and historical maps establish a foundation of academic rigor, while the memes and symbolic imagery introduce a tone of critique and irony. The video’s initial focus on identity, history, and systemic exclusion is clearly evident, as the montage of images — from the trash can to the Obama superimposition — visually narrates the Roma experience as one of marginalization, cultural invisibility, and political manipulation. The section concludes with the fading black screen, leaving the viewer with the lingering image of “POREKLOM SAM CIGANIN,” a phrase that encapsulates the video’s central theme: the erasure of Roma identity despite their enduring presence and cultural significance [4].
```

## 8. References used by this section (global numbers)

```
[1] 00:00:00–00:00:10 · episodic 10sec: A disclaimer appears on a black screen, explaining that the term “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s complicated history and clarifying t...
[2] 00:00:00–00:03:00 · episodic 3min: **[Event 1: Introduction and Context Setting]**  
The video opens with a disclaimer clarifying the use of “Gypsy” as a non-slandrous term for Roma/Romani, followed by a map of the Balkans and a montage of memes and hi...
[3] 00:00:10–00:00:20 · episodic 10sec: The video segment begins with a text overlay discussing the historical and cultural presence of the Roma, also known as Gypsies, in the Balkans, while simultaneously showing a person in a light blue shirt and dark pan...
[4] 00:00:00–00:00:30 · episodic 30sec: **[Event 1: Introduction and Context Setting]**  
The video opens with a disclaimer clarifying that “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s c...
[5] 00:00:00–00:10:00 · episodic 10min: **[Event 1: Introduction and Context Setting]**  
The video opens with a disclaimer clarifying the use of “Gypsy” as a non-slandrous term for Roma/Romani, followed by a map of the Balkans and a montage of memes and hi...
```
