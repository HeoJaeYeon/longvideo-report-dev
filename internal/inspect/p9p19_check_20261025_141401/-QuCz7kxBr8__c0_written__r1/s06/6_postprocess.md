# Section 6 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 253 words → after removal 253 words

## 2. Start/end claim check (`boundary_claims`)

- ending_unverifiable: The video concludes with a one-on-one game that ends in a 3-1 score, celebrated by players including Zak Jesse and Kris, followed by a branded instructional segment featuring players in ZHYPE attire and a static end screen encouraging viewers to subscribe. (cited [])

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 8, "cited_sentences": 2, "checked_tokens": 6, "unsupported": 0, "miscited": 1, "uncited_claims": 2, "absence_statements": 0}`

- **uncited**  `['ZHYPE', 'F1HYPE']` cited [] — Six main participants — Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player — engage in a series of activities that blend product evaluation with recreational play, consistently framed by branded “ZHYPE” and “F1HYPE” environments under clear skies and scenic outdoor backdrops.
- **uncited**  `['3-1']` cited [] — The video concludes with a one-on-one game that ends in a 3-1 score, celebrated by players including Zak Jesse and Kris, followed by a branded instructional segment featuring players in ZHYPE attire and a static end screen encouraging viewers to subscribe.
- **miscited** time `00:37:37` cited ['txt5', 'txt6', 'txt11'] found in ['txt1', 'txt3'] — The video ends at 00:37:37 with a static screen displaying “Thank you for watching” and “DON’T FORGET TO SUBSCRIBE!” alongside the “F1HYPE” logo [citation:txt5][citation:txt6][citation:txt11].

## 4. Citation conversion stats

- `{"text_citations": 6, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 0, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 8 of 12

## 5. Image-text time alignment

- no cited image

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Conclusion

The video presents a dynamic, lighthearted basketball experience centered around testing and demonstrating training gadgets, structured gameplay, and competitive drills. Six main participants — Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player — engage in a series of activities that blend product evaluation with recreational play, consistently framed by branded “ZHYPE” and “F1HYPE” environments under clear skies and scenic outdoor backdrops. The core outcomes include the evaluation of several training devices — such as the SKLZ Dribble Stick, Straight Shooter Strap, Flick Glove, and Shot Coach — each tested in context with gameplay, often tied to performance-based consequences or scoring systems. The video concludes with a one-on-one game that ends in a 3-1 score, celebrated by players including Zak Jesse and Kris, followed by a branded instructional segment featuring players in ZHYPE attire and a static end screen encouraging viewers to subscribe. The final moments show a player in a white and red “ZHYPE” jersey with the number 8 gesturing with teammates before transitioning to the closing graphic [citation:txt1][citation:txt5][citation:txt6]. The video’s tone remains casual and humorous, with teammates reacting to performance with approval and score graphics reinforcing progression and competition. The entire sequence, from gadget testing to final game and instructional wrap-up, serves as a promotional showcase for basketball training products and branded athletic culture, culminating in a clear call to action for viewer engagement. The video ends at 00:37:37 with a static screen displaying “Thank you for watching” and “DON’T FORGET TO SUBSCRIBE!” alongside the “F1HYPE” logo [citation:txt5][citation:txt6][citation:txt11].
```

## 7. Grounded body (exactly as in report.md)

```
# Conclusion

The video presents a dynamic, lighthearted basketball experience centered around testing and demonstrating training gadgets, structured gameplay, and competitive drills. Six main participants — Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player — engage in a series of activities that blend product evaluation with recreational play, consistently framed by branded “ZHYPE” and “F1HYPE” environments under clear skies and scenic outdoor backdrops. The core outcomes include the evaluation of several training devices — such as the SKLZ Dribble Stick, Straight Shooter Strap, Flick Glove, and Shot Coach — each tested in context with gameplay, often tied to performance-based consequences or scoring systems. The video concludes with a one-on-one game that ends in a 3-1 score, celebrated by players including Zak Jesse and Kris, followed by a branded instructional segment featuring players in ZHYPE attire and a static end screen encouraging viewers to subscribe. The final moments show a player in a white and red “ZHYPE” jersey with the number 8 gesturing with teammates before transitioning to the closing graphic [33][34][30]. The video’s tone remains casual and humorous, with teammates reacting to performance with approval and score graphics reinforcing progression and competition. The entire sequence, from gadget testing to final game and instructional wrap-up, serves as a promotional showcase for basketball training products and branded athletic culture, culminating in a clear call to action for viewer engagement. The video ends at 00:37:37 with a static screen displaying “Thank you for watching” and “DON’T FORGET TO SUBSCRIBE!” alongside the “F1HYPE” logo [34][30][35].
```

## 8. References used by this section (global numbers)

```
[30] 00:37:00–00:37:30 · episodic 30sec: A young basketball player in a "ZHYPE 2" jersey begins on an outdoor court, facing the camera before turning and walking toward the basket; other players are visible nearby, including one holding a ball, under a sunny...
[33] 00:36:00–00:39:00 · episodic 3min: A basketball training session unfolds on an outdoor court under clear skies, featuring structured drills centered around defensive shields. A player in a black shirt maneuvers around a defender in a white hoodie label...
[34] 00:37:20–00:37:30 · episodic 10sec: A basketball player in a white and red jersey with the number 8 stands on an outdoor court, gesturing with his arms raised. Two other men stand beside him, one holding a basketball. In the background, other people are...
[35] Video-level knowledge (semantic memory, no timestamp): (video, has, static end screen with blue and white graphic design and subscription prompts)
```
