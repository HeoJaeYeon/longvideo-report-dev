# Section 5 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 329 words → after removal 329 words

## 2. Start/end claim check (`boundary_claims`)

- ending_unverifiable: The video concludes with a static end screen displaying a blue and white graphic. (cited [])

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 12, "cited_sentences": 2, "checked_tokens": 2, "unsupported": 0, "miscited": 0, "uncited_claims": 4, "absence_statements": 0}`

- **uncited**  `['2-1', '3-1', 'ZAK JESSE & KRIS WIN', '00:36:30']` cited [] — At 00:36:30, a one-on-one basketball game concludes with a score graphic overlay displaying “2-1,” followed by a subsequent play where the shooter successfully scores again, updating the score to “3-1.” The on-screen text explicitly announces “ZAK JESSE & KRIS WIN,” confirming the final victors and 
- **uncited**  `['ZHYPE 2']` cited [] — A young player in a “ZHYPE 2” jersey begins on the court, facing the camera before turning toward the basket, with teammates visible nearby under a sunny sky and mountains in the background.
- **uncited**  `['ZHYPE', '8']` cited [] — Another player, wearing a white and red “ZHYPE” jersey with the number 8, stands at the center of the court, gesturing as if giving instructions, flanked by teammates holding basketballs and wearing hoodies.
- **uncited**  `['Thank you for watching', 'DON’T FORGET TO SUBSCRIBE']` cited [] — Centered on the screen is the text “Thank you for watching” and “DON’T FORGET TO SUBSCRIBE!”, accompanied by arrows pointing to placeholders for suggested videos or subscription buttons.

## 4. Citation conversion stats

- `{"text_citations": 7, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 0, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 7 of 12

## 5. Image-text time alignment

- no cited image

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Final Scoring Segment and Closing Instructional Content

At 00:36:30, a one-on-one basketball game concludes with a score graphic overlay displaying “2-1,” followed by a subsequent play where the shooter successfully scores again, updating the score to “3-1.” The on-screen text explicitly announces “ZAK JESSE & KRIS WIN,” confirming the final victors and their score. This victory is celebrated by the player in the white hoodie and patterned shorts, who raises his arms in triumph while interacting with another player in a tie-dye jersey, as spectators observe from the court and a nearby wall [citation:txt3][citation:txt4].

Following the match, the video transitions to an instructional segment featuring players in branded ZHYPE attire. A young player in a “ZHYPE 2” jersey begins on the court, facing the camera before turning toward the basket, with teammates visible nearby under a sunny sky and mountains in the background. Another player, wearing a white and red “ZHYPE” jersey with the number 8, stands at the center of the court, gesturing as if giving instructions, flanked by teammates holding basketballs and wearing hoodies. The scene is set under a clear blue sky, with trees and hills visible in the background, reinforcing the branded, outdoor training environment [citation:txt6].

The video concludes with a static end screen displaying a blue and white graphic. Centered on the screen is the text “Thank you for watching” and “DON’T FORGET TO SUBSCRIBE!”, accompanied by arrows pointing to placeholders for suggested videos or subscription buttons. The “F1HYPE” logo is visible in the top left corner, consistent with branding seen throughout the video [citation:txt7][citation:txt11].

The final segment maintains a promotional tone, tying the instructional content to the branded gear worn by the players and encouraging viewer engagement through the subscription prompt. The end screen serves as the video’s formal closure, thanking viewers and prompting action without introducing new gameplay or events. The branded instructional content and closing call to action are the final elements presented before the video concludes at 00:37:37 [citation:txt6][citation:txt7].
```

## 7. Grounded body (exactly as in report.md)

```
# Final Scoring Segment and Closing Instructional Content

At 00:36:30, a one-on-one basketball game concludes with a score graphic overlay displaying “2-1,” followed by a subsequent play where the shooter successfully scores again, updating the score to “3-1.” The on-screen text explicitly announces “ZAK JESSE & KRIS WIN,” confirming the final victors and their score. This victory is celebrated by the player in the white hoodie and patterned shorts, who raises his arms in triumph while interacting with another player in a tie-dye jersey, as spectators observe from the court and a nearby wall [28][29].

Following the match, the video transitions to an instructional segment featuring players in branded ZHYPE attire. A young player in a “ZHYPE 2” jersey begins on the court, facing the camera before turning toward the basket, with teammates visible nearby under a sunny sky and mountains in the background. Another player, wearing a white and red “ZHYPE” jersey with the number 8, stands at the center of the court, gesturing as if giving instructions, flanked by teammates holding basketballs and wearing hoodies. The scene is set under a clear blue sky, with trees and hills visible in the background, reinforcing the branded, outdoor training environment [30].

The video concludes with a static end screen displaying a blue and white graphic. Centered on the screen is the text “Thank you for watching” and “DON’T FORGET TO SUBSCRIBE!”, accompanied by arrows pointing to placeholders for suggested videos or subscription buttons. The “F1HYPE” logo is visible in the top left corner, consistent with branding seen throughout the video [31][32].

The final segment maintains a promotional tone, tying the instructional content to the branded gear worn by the players and encouraging viewer engagement through the subscription prompt. The end screen serves as the video’s formal closure, thanking viewers and prompting action without introducing new gameplay or events. The branded instructional content and closing call to action are the final elements presented before the video concludes at 00:37:37 [30][31].
```

## 8. References used by this section (global numbers)

```
[28] 00:36:30–00:37:00 · episodic 30sec: Two men compete in a one-on-one basketball game on an outdoor court under clear skies, with the player in the white hoodie and blue shorts repeatedly shooting over a defender using a padded training pad. After success...
[29] 00:36:50–00:37:00 · episodic 10sec: A man in a white hoodie and patterned shorts celebrates with arms outstretched on an outdoor basketball court, as text overlays announce “3-1” and “ZAK JESSE & KRIS WIN.” He then turns and interacts with another playe...
[30] 00:37:00–00:37:30 · episodic 30sec: A young basketball player in a "ZHYPE 2" jersey begins on an outdoor court, facing the camera before turning and walking toward the basket; other players are visible nearby, including one holding a ball, under a sunny...
[31] 00:37:30–00:37:37 · episodic 10sec: The video displays a static end screen with a white background and blue geometric shapes. The text "Thank you for watching" and "DON'T FORGET TO SUBSCRIBE!" is centered, with arrows pointing to two black rectangular p...
[32] Video-level knowledge (semantic memory, no timestamp): (F1HYPE, appears in video, at top left corner)
```
