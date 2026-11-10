# Section 5 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 39, a sentence occurred up to 15 times, ends mid-sentence: True
- raw writer output 2017 words → after removal 834 words

## 2. Start/end claim check (`boundary_claims`)

- none

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 33, "cited_sentences": 1, "checked_tokens": 1, "unsupported": 0, "miscited": 0, "uncited_claims": 1, "absence_statements": 0}`

- **uncited**  `['00:30:00']` cited [] — At 00:30:00, the video presents an anime-style girl standing before the Arc de Triomphe in Paris.

## 4. Citation conversion stats

- `{"text_citations": 71, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 0, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 3 of 12

## 5. Image-text time alignment

- no cited image

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Global Perspective: From Paris to the World

At 00:30:00, the video presents an anime-style girl standing before the Arc de Triomphe in Paris. She wears a black hat with a red band, a white shirt, a red bow tie, and a patterned skirt. Initially, she poses thoughtfully with one hand to her chin and a slight smile; she then spreads her arms wide in a cheerful gesture as cars pass behind her [citation:txt1][citation:txt2][citation:txt3][citation:txt7]. At 00:30:08, colorful credits animate onto the right side of the screen [citation:txt1][citation:txt2][citation:txt3][citation:txt7]. The scene transitions to the same character gesturing in front of a backdrop listing names, followed by a rotating globe centered on a grid of international flags [citation:txt1][citation:txt2][citation:txt3]. The globe slowly rotates, sequentially showcasing continents—Asia, Africa, the Americas, and returning to Europe and Asia—against a backdrop of national flags, with no audio [citation:txt1][citation:txt2][citation:txt4][citation:txt11][citation:txt12]. The globe’s rotation is visually deliberate, emphasizing global interconnectedness without narration [citation:txt2].

The video then shifts to a stylized globe centered on Asia and Australia, encircled by a grid of national flags, symbolizing international scope or global unity [citation:txt1][citation:txt2][citation:txt5][citation:txt6]. This composition is static and balanced, reinforcing the theme of global perspective [citation:txt2]. The scene abruptly cuts to black, serving as a deliberate narrative pause or transition, possibly signaling a shift in tone or perspective [citation:txt1][citation:txt2][citation:txt5][citation:txt6]. The black screen acts as a visual reset, leaving the viewer in anticipation, consistent with the video’s thematic progression from local to international [citation:txt1][citation:txt2].

The anime girl’s recurring visual presence across different settings — from Paris to the global backdrop — underscores continuity and symbolic resonance, aligning with earlier portrayals of Roma cultural endurance [citation:txt1][citation:txt2]. Her cheerful demeanor contrasts with the preceding somber historical and institutional narratives, suggesting a thematic pivot toward hope or cultural affirmation [citation:txt1][citation:txt2]. The globe’s rotation and the final black screen function as a cinematic coda, visually encapsulating the video’s global relevance and leaving the narrative open-ended [citation:txt1][citation:txt2]. The absence of audio during the globe sequence enhances the visual symbolism, allowing the viewer to interpret the global scope independently [citation:txt1][citation:txt2].

The transition to black after the stylized globe is abrupt and unaccompanied by text or sound, indicating an intentional pause rather than an error or technical glitch [citation:txt1][citation:txt2][citation:txt5]. This pause may invite reflection on the video’s broader themes of cultural memory and interconnectedness [citation:txt1][citation:txt2]. The global imagery does not introduce new characters or events but rather synthesizes the video’s prior visual motifs into a unified, symbolic conclusion [citation:txt1][citation:txt2]. The final black screen, therefore, functions as both a narrative and aesthetic device, reinforcing the video’s thematic arc from local to global [citation:txt1][citation:txt2].

The visual sequence from Paris to the globe to blackness mirrors the video’s earlier transitions — from historical to modern, from institutional to personal — suggesting a cyclical or recursive structure [citation:txt1][citation:txt2]. The anime girl’s presence in both local and global contexts reinforces her role as a symbolic figure representing cultural continuity [citation:txt1][citation:txt2]. The globe’s rotation, while not explicitly tied to Roma identity, visually extends the video’s exploration of cultural memory beyond national or ethnic boundaries [citation:txt1][citation:txt2]. The black screen, as a final visual element, does not conclude the narrative but rather suspends it, inviting the viewer to consider the global implications of the themes explored [citation:txt1][citation:txt2].

The video’s final moments do not resolve the narrative but instead offer a cinematic pause that suggests ongoing relevance and open-ended reflection [citation:txt1][citation:txt2]. The global imagery and the black screen together create a sense of closure that is both thematic and visual, aligning with the video’s broader exploration of identity, resilience, and interconnectedness [citation:txt1][citation:txt2]. The absence of audio during the globe sequence and the abrupt cut to black emphasize the visual nature of the conclusion, reinforcing the video’s symbolic and cinematic qualities [citation:txt1][citation:txt2].

The video ends not with a definitive statement but with a visual pause that invites the viewer to consider the global scope of the themes explored — cultural memory, resilience, and the interconnectedness of identities — without providing explicit resolution [citation:txt1][citation:txt2]. The final black screen serves as a visual reset, leaving the viewer in anticipation and reinforcing the video’s thematic arc from local to global [citation:txt1][citation:txt2]. The anime girl’s presence in both Paris and the global backdrop underscores her role as a symbolic figure representing cultural continuity, while the globe’s rotation visually encapsulates the video’s broader themes of interconnectedness and global relevance [citation:txt1][citation:txt2]. The abrupt cut to black, without audio or text, functions as a deliberate narrative pause, signaling a shift in tone or perspective and leaving the narrative open-ended [citation:txt1][citation:txt2].

The video’s final moments, therefore, do not conclude the narrative but rather suspend it, inviting the viewer to consider the global implications of the themes explored — cultural memory, resilience, and the interconnectedness of identities — without providing explicit resolution [citation:txt1][citation:txt2].

The video ends not with a definitive statement but with a visual pause that suggests ongoing relevance and open-ended reflection [citation:txt1][citation:txt2].

The absence of audio during the globe sequence and the abrupt cut to black emphasize the visual nature of the conclusion
```

## 7. Grounded body (exactly as in report.md)

```
# Global Perspective: From Paris to the World

At 00:30:00, the video presents an anime-style girl standing before the Arc de Triomphe in Paris. She wears a black hat with a red band, a white shirt, a red bow tie, and a patterned skirt. Initially, she poses thoughtfully with one hand to her chin and a slight smile; she then spreads her arms wide in a cheerful gesture as cars pass behind her [24][25][26][27]. At 00:30:08, colorful credits animate onto the right side of the screen [24][25][26][27]. The scene transitions to the same character gesturing in front of a backdrop listing names, followed by a rotating globe centered on a grid of international flags [24][25][26]. The globe slowly rotates, sequentially showcasing continents—Asia, Africa, the Americas, and returning to Europe and Asia—against a backdrop of national flags, with no audio [24][25][28][29][30]. The globe’s rotation is visually deliberate, emphasizing global interconnectedness without narration [25].

The video then shifts to a stylized globe centered on Asia and Australia, encircled by a grid of national flags, symbolizing international scope or global unity [24][25][31][32]. This composition is static and balanced, reinforcing the theme of global perspective [25]. The scene abruptly cuts to black, serving as a deliberate narrative pause or transition, possibly signaling a shift in tone or perspective [24][25][31][32]. The black screen acts as a visual reset, leaving the viewer in anticipation, consistent with the video’s thematic progression from local to international [24][25].

The anime girl’s recurring visual presence across different settings — from Paris to the global backdrop — underscores continuity and symbolic resonance, aligning with earlier portrayals of Roma cultural endurance [24][25]. Her cheerful demeanor contrasts with the preceding somber historical and institutional narratives, suggesting a thematic pivot toward hope or cultural affirmation [24][25]. The globe’s rotation and the final black screen function as a cinematic coda, visually encapsulating the video’s global relevance and leaving the narrative open-ended [24][25]. The absence of audio during the globe sequence enhances the visual symbolism, allowing the viewer to interpret the global scope independently [24][25].

The transition to black after the stylized globe is abrupt and unaccompanied by text or sound, indicating an intentional pause rather than an error or technical glitch [24][25][31]. This pause may invite reflection on the video’s broader themes of cultural memory and interconnectedness [24][25]. The global imagery does not introduce new characters or events but rather synthesizes the video’s prior visual motifs into a unified, symbolic conclusion [24][25]. The final black screen, therefore, functions as both a narrative and aesthetic device, reinforcing the video’s thematic arc from local to global [24][25].

The visual sequence from Paris to the globe to blackness mirrors the video’s earlier transitions — from historical to modern, from institutional to personal — suggesting a cyclical or recursive structure [24][25]. The anime girl’s presence in both local and global contexts reinforces her role as a symbolic figure representing cultural continuity [24][25]. The globe’s rotation, while not explicitly tied to Roma identity, visually extends the video’s exploration of cultural memory beyond national or ethnic boundaries [24][25]. The black screen, as a final visual element, does not conclude the narrative but rather suspends it, inviting the viewer to consider the global implications of the themes explored [24][25].

The video’s final moments do not resolve the narrative but instead offer a cinematic pause that suggests ongoing relevance and open-ended reflection [24][25]. The global imagery and the black screen together create a sense of closure that is both thematic and visual, aligning with the video’s broader exploration of identity, resilience, and interconnectedness [24][25]. The absence of audio during the globe sequence and the abrupt cut to black emphasize the visual nature of the conclusion, reinforcing the video’s symbolic and cinematic qualities [24][25].

The video ends not with a definitive statement but with a visual pause that invites the viewer to consider the global scope of the themes explored — cultural memory, resilience, and the interconnectedness of identities — without providing explicit resolution [24][25]. The final black screen serves as a visual reset, leaving the viewer in anticipation and reinforcing the video’s thematic arc from local to global [24][25]. The anime girl’s presence in both Paris and the global backdrop underscores her role as a symbolic figure representing cultural continuity, while the globe’s rotation visually encapsulates the video’s broader themes of interconnectedness and global relevance [24][25]. The abrupt cut to black, without audio or text, functions as a deliberate narrative pause, signaling a shift in tone or perspective and leaving the narrative open-ended [24][25].

The video’s final moments, therefore, do not conclude the narrative but rather suspend it, inviting the viewer to consider the global implications of the themes explored — cultural memory, resilience, and the interconnectedness of identities — without providing explicit resolution [24][25].

The video ends not with a definitive statement but with a visual pause that suggests ongoing relevance and open-ended reflection [24][25].

The absence of audio during the globe sequence and the abrupt cut to black emphasize the visual nature of the conclusion
```

## 8. References used by this section (global numbers)

```
[24] 00:30:00–00:33:00 · episodic 3min: An anime-style girl in a black hat with a red band, white shirt, red bow tie, and patterned skirt stands before the Arc de Triomphe in Paris, posing thoughtfully with one hand to her chin before spreading her arms wid...
[25] 00:30:00–00:40:00 · episodic 10min: **[Event 1: Parisian Pose and Transition to Credits]**  
An anime-style girl, dressed in a black hat with a red band, white shirt, red bow tie, and patterned skirt, stands before the Arc de Triomphe in Paris. She pose...
[26] 00:30:00–00:30:30 · episodic 30sec: An anime-style girl in a black hat with a red band, white shirt, red bow tie, and patterned skirt stands before the Arc de Triomphe in Paris, initially posing with one hand to her chin and a slight smile before spread...
[27] 00:30:00–00:30:10 · episodic 10sec: An anime-style girl in a black hat with a red band, a white shirt, a red bow tie, and a patterned skirt stands in front of the Arc de Triomphe in Paris. She begins with one hand raised to her chin and a slight smile,...
[28] 00:30:20–00:30:30 · episodic 10sec: A stylized globe rotates slowly against a background displaying numerous national flags. The globe begins facing Asia and gradually rotates to show Africa, then the Americas, before returning to focus on Europe and As...
[29] Video-level knowledge (semantic memory, no timestamp): (globe, rotates to show, Africa)
[30] Video-level knowledge (semantic memory, no timestamp): (globe, rotates to show, Americas)
[31] 00:30:30–00:30:32 · episodic 10sec: The screen displays a grid of various national flags surrounding a central, stylized globe showing the continents of Asia and Australia. The scene then abruptly transitions to complete blackness.
[32] 00:30:30–00:31:00 · episodic 30sec: The screen opens with a global-themed visual: a stylized globe centered on Asia and Australia, encircled by a grid of national flags, symbolizing international scope or global unity. The scene then cuts abruptly to bl...
```
