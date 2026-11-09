# Section 6 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 199 words → after removal 199 words

## 2. Start/end claim check (`boundary_claims`)

- ending_unverifiable: The video concludes with a dynamic, game-driven testing of 12 viral sports gadgets on an outdoor basketball court under clear, sunny conditions. (cited [])
- ending_early: The “NEVER ENDING DEFENDER” training device was also featured, with players actively using it in defensive drills, and the video ends with them continuing the game under the “FIRST TO 3 WINS” rule, reinforcing the gadget’s role in competitive play [citation:txt5][citation:txt7]. (cited [5, 7], latest cited end 00:20:00)

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 7, "cited_sentences": 3, "checked_tokens": 6, "unsupported": 1, "miscited": 2, "uncited_claims": 1, "absence_statements": 0}`

- **uncited**  `['12']` cited [] — The video concludes with a dynamic, game-driven testing of 12 viral sports gadgets on an outdoor basketball court under clear, sunny conditions.
- **miscited** quote `SHOT COACH` cited ['txt1'] found in ['txt4', 'txt5', 'txt6', 'txt7'] — Notably, the “Straight Shooter Strap” was tested in a shooting sequence where a player achieved 3/16 successful shots while using it, and the “SHOT COACH” training device was demonstrated in a half-court drill with young players, emphasizing structured, tech-assisted training [citation:txt1].
- **miscited** quote `NEVER ENDING DEFENDER` cited ['txt5', 'txt7'] found in ['txt8'] — The “NEVER ENDING DEFENDER” training device was also featured, with players actively using it in defensive drills, and the video ends with them continuing the game under the “FIRST TO 3 WINS” rule, reinforcing the gadget’s role in competitive play [citation:txt5][citation:txt7].
- **unsupported** quote `FIRST TO 3 WINS` cited ['txt5', 'txt7'] — The “NEVER ENDING DEFENDER” training device was also featured, with players actively using it in defensive drills, and the video ends with them continuing the game under the “FIRST TO 3 WINS” rule, reinforcing the gadget’s role in competitive play [citation:txt5][citation:txt7].

## 4. Citation conversion stats

- `{"text_citations": 4, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 0, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 8 of 12

## 5. Image-text time alignment

- no cited image

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Conclusion

The video concludes with a dynamic, game-driven testing of 12 viral sports gadgets on an outdoor basketball court under clear, sunny conditions. The main outcomes center on the practical application and performance of each device, with participants engaging in timed challenges, shooting drills, and competitive play. Notably, the “Straight Shooter Strap” was tested in a shooting sequence where a player achieved 3/16 successful shots while using it, and the “SHOT COACH” training device was demonstrated in a half-court drill with young players, emphasizing structured, tech-assisted training [citation:txt1]. The “NEVER ENDING DEFENDER” training device was also featured, with players actively using it in defensive drills, and the video ends with them continuing the game under the “FIRST TO 3 WINS” rule, reinforcing the gadget’s role in competitive play [citation:txt5][citation:txt7]. The video’s tone remains lighthearted and collaborative, with humor, camaraderie, and playful scoring systems like “FIRST MADE SHOT SHOOTS SILLY STRING AT LOSER” adding to the entertainment value [citation:txt6]. The final scenes show players deeply engaged in the game, underscoring the gadgets’ integration into real-time sports activity. Overall, the video successfully demonstrates how these gadgets enhance skill development, competitive play, and training efficiency in a casual, outdoor basketball setting.
```

## 7. Grounded body (exactly as in report.md)

```
# Conclusion

The video concludes with a dynamic, game-driven testing of 12 viral sports gadgets on an outdoor basketball court under clear, sunny conditions. The main outcomes center on the practical application and performance of each device, with participants engaging in timed challenges, shooting drills, and competitive play. Notably, the “Straight Shooter Strap” was tested in a shooting sequence where a player achieved 3/16 successful shots while using it, and the “SHOT COACH” training device was demonstrated in a half-court drill with young players, emphasizing structured, tech-assisted training [31]. The “NEVER ENDING DEFENDER” training device was also featured, with players actively using it in defensive drills, and the video ends with them continuing the game under the “FIRST TO 3 WINS” rule, reinforcing the gadget’s role in competitive play [24][21]. The video’s tone remains lighthearted and collaborative, with humor, camaraderie, and playful scoring systems like “FIRST MADE SHOT SHOOTS SILLY STRING AT LOSER” adding to the entertainment value [20]. The final scenes show players deeply engaged in the game, underscoring the gadgets’ integration into real-time sports activity. Overall, the video successfully demonstrates how these gadgets enhance skill development, competitive play, and training efficiency in a casual, outdoor basketball setting.
```

## 8. References used by this section (global numbers)

```
[20] 00:18:00–00:21:00 · episodic 3min: **[Event 1: Game Setup & Product Introduction]**  
Three men gather on an outdoor basketball court under a clear blue sky, initiating a playful game governed by the rule: “FIRST MADE SHOT SHOOTS SILLY STRING AT LOSER....
[21] 00:10:00–00:20:00 · episodic 10min: **[Event 1: Dribble Challenge Begins]**  
A man in a white t-shirt and patterned shorts initiates a timed dribbling challenge on a sunny outdoor court, with a countdown timer and on-screen text reading “MOST DRIBBLES...
[24] 00:19:50–00:20:00 · episodic 10sec: A basketball coach wearing a white cap and black hoodie stands on an outdoor court, holding a clipboard and an orange device, instructing two young players. A text overlay reads, “SHOOT FROM HALF COURT 5 TIMES WITH SH...
[31] 00:03:00–00:06:00 · episodic 3min: Three men gather on an outdoor basketball court, negotiating positions before settling into a shooting challenge. One man in a black hoodie and white cap adjusts a basketball on a training device while the others—wear...
```
