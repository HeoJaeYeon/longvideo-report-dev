# Section 6 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 213 words → after removal 213 words

## 2. Start/end claim check (`boundary_claims`)

- none

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 6, "cited_sentences": 2, "checked_tokens": 2, "unsupported": 0, "miscited": 0, "uncited_claims": 0, "absence_statements": 0}`

- no findings

## 4. Citation conversion stats

- `{"text_citations": 9, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 0, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 6 of 12

## 5. Image-text time alignment

- no cited image

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Conclusion

The video portrays Roma as historically marginalized through visual depictions of institutionalized persecution under German and Eastern European regimes, including archival footage of forced labor and concentration camp marches from 1945, as well as Nazi-era racial categorization documents [citation:txt8]. These scenes, juxtaposed with symbolic imagery such as the mugshot of Maria Bihari and the stylized animation of a Roma girl superimposed over a historical painting, reinforce the group’s enduring presence despite systemic erasure [citation:txt5][citation:txt7]. The video further illustrates cultural resilience through scenes of community gathering, public rallies asserting identity (“I am also a Roma”), and animated figures dancing or standing with open arms in urban and rural settings — all suggesting continuity amid hardship [citation:txt5][citation:txt7]. Globally, the video connects Roma experience across continents, culminating in a stylized globe centered on Asia and Australia, encircled by national flags, which visually symbolizes international scope and unity [citation:txt2][citation:txt4]. The video concludes not with a narrative resolution but with symbolic imagery: an anime-style girl posing before the Arc de Triomphe, followed by a rotating globe and a final black screen, inviting reflection without offering closure [citation:txt1][citation:txt4]. This visual pause aligns with the video’s thematic emphasis on Roma identity as both historically burdened and globally interconnected, leaving the viewer with a sense of ongoing, unresolved presence.
```

## 7. Grounded body (exactly as in report.md)

```
# Conclusion

The video portrays Roma as historically marginalized through visual depictions of institutionalized persecution under German and Eastern European regimes, including archival footage of forced labor and concentration camp marches from 1945, as well as Nazi-era racial categorization documents [26]. These scenes, juxtaposed with symbolic imagery such as the mugshot of Maria Bihari and the stylized animation of a Roma girl superimposed over a historical painting, reinforce the group’s enduring presence despite systemic erasure [18][27]. The video further illustrates cultural resilience through scenes of community gathering, public rallies asserting identity (“I am also a Roma”), and animated figures dancing or standing with open arms in urban and rural settings — all suggesting continuity amid hardship [18][27]. Globally, the video connects Roma experience across continents, culminating in a stylized globe centered on Asia and Australia, encircled by national flags, which visually symbolizes international scope and unity [28][23]. The video concludes not with a narrative resolution but with symbolic imagery: an anime-style girl posing before the Arc de Triomphe, followed by a rotating globe and a final black screen, inviting reflection without offering closure [22][23]. This visual pause aligns with the video’s thematic emphasis on Roma identity as both historically burdened and globally interconnected, leaving the viewer with a sense of ongoing, unresolved presence.
```

## 8. References used by this section (global numbers)

```
[18] 00:29:30–00:30:00 · episodic 30sec: An animated woman in traditional attire stands with open arms against a cityscape, symbolizing cultural presence or welcome, followed by a sepia-toned religious figure and snowy boots, evoking historical or spiritual...
[22] 00:30:00–00:30:10 · episodic 10sec: An anime-style girl in a black hat with a red band, a white shirt, a red bow tie, and a patterned skirt stands in front of the Arc de Triomphe in Paris. She begins with one hand raised to her chin and a slight smile,...
[23] 00:30:00–00:40:00 · episodic 10min: **[Event 1: Parisian Pose and Transition to Credits]**  
An anime-style girl, dressed in a black hat with a red band, white shirt, red bow tie, and patterned skirt, stands before the Arc de Triomphe in Paris. She pose...
[26] 00:24:30–00:25:00 · episodic 30sec: **[Event 1: Historical Footage of Post-War Repression]**  
The video opens with a title card reading “Communism Chapter VII,” followed by black-and-white archival footage from 1945. Soldiers are shown atop a damaged b...
[27] 00:04:50–00:05:00 · episodic 10sec: The video begins with a wide shot of a desert landscape featuring sand dunes, scattered vegetation, and distant rock formations under a clear sky. It then cuts to a close-up of a man with a shaved head and beard, wear...
[28] 00:30:00–00:30:30 · episodic 30sec: An anime-style girl in a black hat with a red band, white shirt, red bow tie, and patterned skirt stands before the Arc de Triomphe in Paris, initially posing with one hand to her chin and a slight smile before spread...
```
