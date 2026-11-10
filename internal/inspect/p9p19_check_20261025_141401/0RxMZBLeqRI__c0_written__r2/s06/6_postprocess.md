# Section 6 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 274 words → after removal 274 words

## 2. Start/end claim check (`boundary_claims`)

- none

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 9, "cited_sentences": 2, "checked_tokens": 2, "unsupported": 1, "miscited": 0, "uncited_claims": 0, "absence_statements": 0}`

- **unsupported** quote `Zigeuner-Buch` cited ['txt3', 'txt6'] — These episodes of erasure are visually underscored by archival footage, bureaucratic documents like the “Zigeuner-Buch,” and scenes of forced labor and state control [citation:txt3][citation:txt6].

## 4. Citation conversion stats

- `{"text_citations": 11, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 0, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 5 of 12

## 5. Image-text time alignment

- no cited image

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Conclusion

The video portrays Roma identity as one that has endured systematic erasure yet persists through cultural resilience, as demonstrated across its narrative arc. It begins by acknowledging the historical and cultural presence of Roma in the Balkans, juxtaposing this with moments of institutionalized persecution—from Bismarck-era surveillance to Nazi racial categorization and post-war repression under communism [citation:txt1][citation:txt2]. These episodes of erasure are visually underscored by archival footage, bureaucratic documents like the “Zigeuner-Buch,” and scenes of forced labor and state control [citation:txt3][citation:txt6]. Despite this, the video consistently returns to imagery of cultural endurance: an animated woman with open arms against a cityscape, a Roma woman asserting identity at a rally with the slogan “Én is cigány vagyok,” and symbolic overlays of animated characters onto urban and historical settings [citation:txt8][citation:txt12]. These visuals affirm Roma agency and continuity amid hardship.

The video’s global perspective is reinforced through its final sequence, which features an anime-style girl standing before the Arc de Triomphe in Paris, then transitioning to a rotating globe centered on international flags, symbolizing Roma presence and interconnectedness across continents [citation:txt1][citation:txt2]. This global imagery culminates in a stylized globe centered on Asia and Australia, encircled by national flags, before abruptly cutting to black—a visual pause that invites reflection rather than closure [citation:txt4]. The absence of audio during the globe sequence and the sudden transition emphasize the symbolic weight of the imagery, aligning with the video’s broader thematic arc from erasure to resilience. The video concludes not with a definitive statement but with this open-ended visual pause, reinforcing the idea that Roma identity, though historically marginalized, continues to exist, adapt, and assert itself across the world [citation:txt1][citation:txt2].
```

## 7. Grounded body (exactly as in report.md)

```
# Conclusion

The video portrays Roma identity as one that has endured systematic erasure yet persists through cultural resilience, as demonstrated across its narrative arc. It begins by acknowledging the historical and cultural presence of Roma in the Balkans, juxtaposing this with moments of institutionalized persecution—from Bismarck-era surveillance to Nazi racial categorization and post-war repression under communism [24][25]. These episodes of erasure are visually underscored by archival footage, bureaucratic documents like the “Zigeuner-Buch,” and scenes of forced labor and state control [26][33]. Despite this, the video consistently returns to imagery of cultural endurance: an animated woman with open arms against a cityscape, a Roma woman asserting identity at a rally with the slogan “Én is cigány vagyok,” and symbolic overlays of animated characters onto urban and historical settings [17][34]. These visuals affirm Roma agency and continuity amid hardship.

The video’s global perspective is reinforced through its final sequence, which features an anime-style girl standing before the Arc de Triomphe in Paris, then transitioning to a rotating globe centered on international flags, symbolizing Roma presence and interconnectedness across continents [24][25]. This global imagery culminates in a stylized globe centered on Asia and Australia, encircled by national flags, before abruptly cutting to black—a visual pause that invites reflection rather than closure [32]. The absence of audio during the globe sequence and the sudden transition emphasize the symbolic weight of the imagery, aligning with the video’s broader thematic arc from erasure to resilience. The video concludes not with a definitive statement but with this open-ended visual pause, reinforcing the idea that Roma identity, though historically marginalized, continues to exist, adapt, and assert itself across the world [24][25].
```

## 8. References used by this section (global numbers)

```
[17] 00:29:30–00:30:00 · episodic 30sec: An animated woman in traditional attire stands with open arms against a cityscape, symbolizing cultural presence or welcome, followed by a sepia-toned religious figure and snowy boots, evoking historical or spiritual...
[24] 00:30:00–00:33:00 · episodic 3min: An anime-style girl in a black hat with a red band, white shirt, red bow tie, and patterned skirt stands before the Arc de Triomphe in Paris, posing thoughtfully with one hand to her chin before spreading her arms wid...
[25] 00:30:00–00:40:00 · episodic 10min: **[Event 1: Parisian Pose and Transition to Credits]**  
An anime-style girl, dressed in a black hat with a red band, white shirt, red bow tie, and patterned skirt, stands before the Arc de Triomphe in Paris. She pose...
[26] 00:30:00–00:30:30 · episodic 30sec: An anime-style girl in a black hat with a red band, white shirt, red bow tie, and patterned skirt stands before the Arc de Triomphe in Paris, initially posing with one hand to her chin and a slight smile before spread...
[32] 00:30:30–00:31:00 · episodic 30sec: The screen opens with a global-themed visual: a stylized globe centered on Asia and Australia, encircled by a grid of national flags, symbolizing international scope or global unity. The scene then cuts abruptly to bl...
[33] 00:24:30–00:25:00 · episodic 30sec: **[Event 1: Historical Footage of Post-War Repression]**  
The video opens with a title card reading “Communism Chapter VII,” followed by black-and-white archival footage from 1945. Soldiers are shown atop a damaged b...
[34] Video-level knowledge (semantic memory, no timestamp): (video, displays, poster featuring anime-style character)
```
