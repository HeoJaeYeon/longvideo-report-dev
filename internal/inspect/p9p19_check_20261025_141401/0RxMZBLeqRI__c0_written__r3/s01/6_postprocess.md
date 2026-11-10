# Section 1 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 497 words → after removal 497 words

## 2. Start/end claim check (`boundary_claims`)

- none

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 16, "cited_sentences": 6, "checked_tokens": 10, "unsupported": 0, "miscited": 2, "uncited_claims": 0, "absence_statements": 0}`

- **miscited** time `00:00:00` cited ['txt3'] found in ['txt1', 'txt2', 'img1'] — At 00:00:00, the video also features a text overlay that introduces the historical and cultural presence of the Roma in the Balkans, while visuals show a person walking past a trash can and then turning away — possibly symbolizing marginalization [citation:txt3].
- **miscited** quote `I am a Gypsy by origin` cited ['txt3'] found in ['txt1'] — The segment concludes with a still image of Barack Obama superimposed over dilapidated buildings, overlaid with the text “POREKLOM SAM CIGANIN” (“I am a Gypsy by origin”), fading to black — reinforcing the theme of identity, erasure, and societal perception [citation:txt3].

## 4. Citation conversion stats

- `{"text_citations": 16, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 1, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 9 of 12

## 5. Image-text time alignment

- img1 frame 00:00:05: gap to text cited in the same paragraph 0.0 s (ranges ['00:00:00-00:00:30', '00:00:10-00:00:20']), to any text cited in the section 0.0 s

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Framing Roma Identity Through Historical and Cultural Context

The video opens with a disclaimer displayed on a black screen, clarifying that the term “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s contested history and affirming its non-slandrous intent [citation:txt2]. This disclaimer sets the tone for the video’s approach to terminology, positioning the narrative within a context of historical sensitivity and intentional linguistic framing [citation:txt1]. Immediately following, the screen transitions to a map of the Balkan region, establishing geographic context for the Roma’s historical presence [citation:txt2]. This is followed by a montage of internet memes and historical battle tables — including a satirical image labeled “POV: TITO INVENTING MACEDONIANS” — which introduces a tone of irony and critique toward entrenched ethnic hatred in the region, as underscored by the accompanying audio commentary [citation:txt1][citation:txt2].

At 00:00:00, the video also features a text overlay that introduces the historical and cultural presence of the Roma in the Balkans, while visuals show a person walking past a trash can and then turning away — possibly symbolizing marginalization [citation:txt3]. The scene cuts to a man in a white suit and red tie seated beside a woman in a patterned top, followed by a shirtless man shouting outdoors — suggesting social tension or protest [citation:txt3]. A bearded man is then shown speaking in front of a lit background, likely delivering commentary or narration [citation:txt3]. The segment concludes with a still image of Barack Obama superimposed over dilapidated buildings, overlaid with the text “POREKLOM SAM CIGANIN” (“I am a Gypsy by origin”), fading to black — reinforcing the theme of identity, erasure, and societal perception [citation:txt3]. Throughout, narration emphasizes the Roma’s complex and often negative social portrayal [citation:txt3].

The video further contextualizes Roma identity through visual and textual elements. At 00:00:30, a title card reading “GYPSIES” appears, followed by sepia-toned historical photographs of Roma families in traditional attire — some gathered around caravans, others posing formally — illustrating their long-standing presence [citation:txt1][citation:txt3]. The scene transitions to a modern-day street parade featuring participants in colorful traditional clothing and contemporary attire, marching with flags including the Roma flag (red wheel on green), alongside Ukrainian and EU flags [citation:txt1]. Narration affirms the Roma’s integral role in Balkan culture and history, while acknowledging the lack of public knowledge due to generational stigma, prejudice, and insufficient scholarly research [citation:txt1].

The video’s opening montage and textual overlays collectively establish the Roma as a historically marginalized group, using maps, memes, and symbolic imagery to set up the theme of erasure and systemic exclusion [citation:txt1]. The disclaimer about terminology, the Balkans map, and satirical memes all serve to frame the video’s exploration of Roma identity within a context of historical complexity, social stigma, and contested representation. The overlay “POREKLOM SAM CIGANIN” over Obama’s image further underscores the theme of identity and societal perception, suggesting the Roma’s historical erasure and the ways in which their identity is often misunderstood or misrepresented [citation:txt3].

![](citation:img1)
```

## 7. Grounded body (exactly as in report.md)

```
# Framing Roma Identity Through Historical and Cultural Context

The video opens with a disclaimer displayed on a black screen, clarifying that the term “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s contested history and affirming its non-slandrous intent [1]. This disclaimer sets the tone for the video’s approach to terminology, positioning the narrative within a context of historical sensitivity and intentional linguistic framing [2]. Immediately following, the screen transitions to a map of the Balkan region, establishing geographic context for the Roma’s historical presence [1]. This is followed by a montage of internet memes and historical battle tables — including a satirical image labeled “POV: TITO INVENTING MACEDONIANS” — which introduces a tone of irony and critique toward entrenched ethnic hatred in the region, as underscored by the accompanying audio commentary [2][1].

At 00:00:00, the video also features a text overlay that introduces the historical and cultural presence of the Roma in the Balkans, while visuals show a person walking past a trash can and then turning away — possibly symbolizing marginalization [3]. The scene cuts to a man in a white suit and red tie seated beside a woman in a patterned top, followed by a shirtless man shouting outdoors — suggesting social tension or protest [3]. A bearded man is then shown speaking in front of a lit background, likely delivering commentary or narration [3]. The segment concludes with a still image of Barack Obama superimposed over dilapidated buildings, overlaid with the text “POREKLOM SAM CIGANIN” (“I am a Gypsy by origin”), fading to black — reinforcing the theme of identity, erasure, and societal perception [3]. Throughout, narration emphasizes the Roma’s complex and often negative social portrayal [3].

The video further contextualizes Roma identity through visual and textual elements. At 00:00:30, a title card reading “GYPSIES” appears, followed by sepia-toned historical photographs of Roma families in traditional attire — some gathered around caravans, others posing formally — illustrating their long-standing presence [2][3]. The scene transitions to a modern-day street parade featuring participants in colorful traditional clothing and contemporary attire, marching with flags including the Roma flag (red wheel on green), alongside Ukrainian and EU flags [2]. Narration affirms the Roma’s integral role in Balkan culture and history, while acknowledging the lack of public knowledge due to generational stigma, prejudice, and insufficient scholarly research [2].

The video’s opening montage and textual overlays collectively establish the Roma as a historically marginalized group, using maps, memes, and symbolic imagery to set up the theme of erasure and systemic exclusion [2]. The disclaimer about terminology, the Balkans map, and satirical memes all serve to frame the video’s exploration of Roma identity within a context of historical complexity, social stigma, and contested representation. The overlay “POREKLOM SAM CIGANIN” over Obama’s image further underscores the theme of identity and societal perception, suggesting the Roma’s historical erasure and the ways in which their identity is often misunderstood or misrepresented [3].

![Figure 1 (00:00:05)](frames/0RxMZBLeqRI_00000000.jpg)

*Figure 1. Frame at 00:00:05 (clip 00:00:00–00:00:10). A disclaimer appears on a black screen, explaining that the term “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s complicated history and clarifying that it is not intended as a slur. The screen then transitions to a map of the Ba...*
```

## 8. References used by this section (global numbers)

```
[1] 00:00:00–00:00:10 · episodic 10sec: A disclaimer appears on a black screen, explaining that the term “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s complicated history and clarifying t...
[2] 00:00:00–00:00:30 · episodic 30sec: **[Event 1: Introduction and Context Setting]**  
The video opens with a disclaimer clarifying that “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s c...
[3] 00:00:10–00:00:20 · episodic 10sec: The video segment begins with a text overlay discussing the historical and cultural presence of the Roma, also known as Gypsies, in the Balkans, while simultaneously showing a person in a light blue shirt and dark pan...
```
