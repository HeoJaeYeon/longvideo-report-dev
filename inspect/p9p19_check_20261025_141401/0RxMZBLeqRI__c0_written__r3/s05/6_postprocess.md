# Section 5 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 384 words → after removal 384 words

## 2. Start/end claim check (`boundary_claims`)

- none

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 16, "cited_sentences": 1, "checked_tokens": 1, "unsupported": 0, "miscited": 0, "uncited_claims": 2, "absence_statements": 0}`

- **uncited**  `['00:30:00']` cited [] — At 00:30:00, the video shifts to a visually stylized scene featuring an anime-style girl standing before the Arc de Triomphe in Paris.
- **uncited**  `['00:30:00', '00:30:32']` cited [] — The sequence from 00:30:00 to 00:30:32 concludes the video’s visual narrative with a symbolic global perspective, transitioning from a localized Parisian moment to an international scope before ending in a stark black screen.

## 4. Citation conversion stats

- `{"text_citations": 14, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 3, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 8 of 12

## 5. Image-text time alignment

- img1 frame 00:30:05: gap to text cited in the same paragraph 0.0 s (ranges ['00:30:00-00:40:00']), to any text cited in the section 0.0 s
- img2 frame 00:30:15: gap to text cited in the same paragraph 0.0 s (ranges ['00:30:00-00:40:00']), to any text cited in the section 0.0 s
- img3 frame 00:11:05: gap to text cited in the same paragraph 1135.0 s (ranges ['00:30:00-00:40:00']), to any text cited in the section 1135.0 s

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Global and Symbolic Conclusion: A Reflective Pause Across Continents

At 00:30:00, the video shifts to a visually stylized scene featuring an anime-style girl standing before the Arc de Triomphe in Paris. She is dressed in a black hat with a red band, a white shirt, a red bow tie, and a patterned skirt. Initially, she poses thoughtfully with one hand to her chin and a slight smile, then transitions into a cheerful gesture by spreading her arms wide as cars pass behind her [citation:txt5]. At 00:30:08, colorful credits animate onto the right side of the screen, listing names in varied colors [citation:txt5][citation:txt2]. This moment, set against a recognizable Parisian landmark, serves as a lighthearted visual coda before the narrative expands beyond local context.

The scene then transitions to the same character gesturing in front of a backdrop listing names, suggesting acknowledgment of contributors or collaborators [citation:txt2]. Immediately following, the video presents a rotating globe centered on a grid of international flags. The globe slowly turns, sequentially showcasing continents—Asia, Africa, the Americas, and returning to Europe and Asia—against a backdrop of national flags, with no audio present [citation:txt2][citation:txt6]. This visual sequence emphasizes global interconnectedness and reinforces the international scope previously introduced in the video’s narrative [citation:txt2].

The video then opens on a stylized globe centered on Asia and Australia, encircled by a grid of national flags, symbolizing global unity or international perspective [citation:txt4]. The composition is balanced and symbolic, visually reinforcing the theme of global unity or scope [citation:txt2]. The scene then abruptly cuts to black, signaling a narrative pause or intentional transition [citation:txt2][citation:txt4]. This abrupt cut to black acts as a visual reset, leaving the viewer in a state of reflective anticipation, consistent with the thematic emphasis on Roma experiences across continents [citation:txt2].

The sequence from 00:30:00 to 00:30:32 concludes the video’s visual narrative with a symbolic global perspective, transitioning from a localized Parisian moment to an international scope before ending in a stark black screen. This final sequence does not resolve the historical or cultural themes explored earlier but instead invites broader consideration of Roma identity and experience across continents, aligning with the video’s global framing [citation:txt2]. The absence of audio during the globe sequence further underscores its symbolic function, allowing the visual imagery to carry thematic weight [citation:txt2].

![](citation:img1)  
![](citation:img2)  
![](citation:img3)
```

## 7. Grounded body (exactly as in report.md)

```
# Global and Symbolic Conclusion: A Reflective Pause Across Continents

At 00:30:00, the video shifts to a visually stylized scene featuring an anime-style girl standing before the Arc de Triomphe in Paris. She is dressed in a black hat with a red band, a white shirt, a red bow tie, and a patterned skirt. Initially, she poses thoughtfully with one hand to her chin and a slight smile, then transitions into a cheerful gesture by spreading her arms wide as cars pass behind her [22]. At 00:30:08, colorful credits animate onto the right side of the screen, listing names in varied colors [22][23]. This moment, set against a recognizable Parisian landmark, serves as a lighthearted visual coda before the narrative expands beyond local context.

The scene then transitions to the same character gesturing in front of a backdrop listing names, suggesting acknowledgment of contributors or collaborators [23]. Immediately following, the video presents a rotating globe centered on a grid of international flags. The globe slowly turns, sequentially showcasing continents—Asia, Africa, the Americas, and returning to Europe and Asia—against a backdrop of national flags, with no audio present [23][24]. This visual sequence emphasizes global interconnectedness and reinforces the international scope previously introduced in the video’s narrative [23].

The video then opens on a stylized globe centered on Asia and Australia, encircled by a grid of national flags, symbolizing global unity or international perspective [25]. The composition is balanced and symbolic, visually reinforcing the theme of global unity or scope [23]. The scene then abruptly cuts to black, signaling a narrative pause or intentional transition [23][25]. This abrupt cut to black acts as a visual reset, leaving the viewer in a state of reflective anticipation, consistent with the thematic emphasis on Roma experiences across continents [23].

The sequence from 00:30:00 to 00:30:32 concludes the video’s visual narrative with a symbolic global perspective, transitioning from a localized Parisian moment to an international scope before ending in a stark black screen. This final sequence does not resolve the historical or cultural themes explored earlier but instead invites broader consideration of Roma identity and experience across continents, aligning with the video’s global framing [23]. The absence of audio during the globe sequence further underscores its symbolic function, allowing the visual imagery to carry thematic weight [23].

![Figure 5 (00:30:05)](frames/0RxMZBLeqRI_00300000.jpg)

*Figure 5. Frame at 00:30:05 (clip 00:30:00–00:30:10). An anime-style girl in a black hat with a red band, a white shirt, a red bow tie, and a patterned skirt stands in front of the Arc de Triomphe in Paris. She begins with one hand raised to her chin and a slight smile, then transitions to spreading her arms wide with a cheerful expression. Cars pas...*

![Figure 6 (00:30:15)](frames/0RxMZBLeqRI_00301000.jpg)

*Figure 6. Frame at 00:30:15 (clip 00:30:10–00:30:20). An anime-style character in a hat and bow tie gestures in front of a backdrop featuring a list of names, then the scene transitions to a rotating globe centered on a grid of international flags.*

![Figure 7 (00:11:05)](frames/0RxMZBLeqRI_00110000.jpg)

*Figure 7. Frame at 00:11:05 (clip 00:11:00–00:11:10). The video segment begins with a historical illustration depicting a military procession, followed by a colorful manuscript-style scene showing a seated ruler interacting with a group of people in ornate attire. The audio discusses how Ottoman institutions incorporated Islamic doctrine, which gran...*
```

## 8. References used by this section (global numbers)

```
[22] 00:30:00–00:30:10 · episodic 10sec: An anime-style girl in a black hat with a red band, a white shirt, a red bow tie, and a patterned skirt stands in front of the Arc de Triomphe in Paris. She begins with one hand raised to her chin and a slight smile,...
[23] 00:30:00–00:40:00 · episodic 10min: **[Event 1: Parisian Pose and Transition to Credits]**  
An anime-style girl, dressed in a black hat with a red band, white shirt, red bow tie, and patterned skirt, stands before the Arc de Triomphe in Paris. She pose...
[24] 00:30:20–00:30:30 · episodic 10sec: A stylized globe rotates slowly against a background displaying numerous national flags. The globe begins facing Asia and gradually rotates to show Africa, then the Americas, before returning to focus on Europe and As...
[25] 00:30:30–00:31:00 · episodic 30sec: The screen opens with a global-themed visual: a stylized globe centered on Asia and Australia, encircled by a grid of national flags, symbolizing international scope or global unity. The scene then cuts abruptly to bl...
```
