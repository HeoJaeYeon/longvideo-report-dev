# Section 4 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 449 words → after removal 449 words

## 2. Start/end claim check (`boundary_claims`)

- none

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 18, "cited_sentences": 8, "checked_tokens": 12, "unsupported": 1, "miscited": 0, "uncited_claims": 1, "absence_statements": 0}`

- **uncited**  `['Straight Shooter Strap']` cited [] — The “Straight Shooter Strap” is demonstrated by a man in a white hoodie on an outdoor basketball court under clear skies.
- **unsupported** number `1/1` cited ['txt1'] — The scoreboard updates after each shot: the player initially makes one shot (1/1), then misses several, with the tally climbing to 0/3 [citation:txt1].

## 4. Citation conversion stats

- `{"text_citations": 17, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 0, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 3 of 12

## 5. Image-text time alignment

- no cited image

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Straight Shooter Strap Test: Demonstration, Shooting Drill, and Forfeit Challenge

The “Straight Shooter Strap” is demonstrated by a man in a white hoodie on an outdoor basketball court under clear skies. He explains its function as stabilizing the elbow during shooting to prevent it from flaring outward, gesturing to his arm and adjusting the black strap on his own forearm while a third observer watches closely [citation:txt7][citation:txt8]. The strap’s design is visible in close-up with on-screen text, and the scene widens to show the full court, hoop, fence, and surrounding hills, emphasizing its practical application in a real-game context [citation:txt7].

Following the demonstration, a player in a white shirt and patterned shorts begins a shooting sequence using the strap. The scoreboard updates after each shot: the player initially makes one shot (1/1), then misses several, with the tally climbing to 0/3 [citation:txt1]. As the drill continues, he scores more shots, pushing the score to 3/16 [citation:txt1]. Commentary tracks each attempt, with remarks such as “Dude, 15” and “Zach’s uses this thing, bro,” indicating active engagement from teammates [citation:txt1]. The player smiles at the camera as he approaches 15 successful shots, with the backdrop of a large house and trees under clear skies [citation:txt1].

After the shooting sequence, the player attempts a jump shot that misses. He expresses frustration, questioning whether his shot is broken or if the strap caused the miss. A teammate confirms the issue, and another asks what the forfeit is, prompting the player to suggest 30 jumping jacks as punishment [citation:txt6]. The group gathers near the hoop, holding basketballs and engaging in lighthearted banter [citation:txt6].

The man in the white shirt begins performing jumping jacks, raising his arms with each bounce, while two others—wearing a red and white jersey and a white hoodie—watch [citation:txt5][citation:txt3]. Teasing ensues, with one observer joking, “Bounce some titties, boy,” and later comparing chest sizes, saying, “Jadil got a bigger chest than you” [citation:txt5][citation:txt11]. The man in the white shirt deflects with humor, replying, “Bro, I'm wearing a big shirt.” His movements become off-rhythm, with his feet moving out of sync with his hands, drawing amused observation from the two onlookers [citation:txt3][citation:txt4]. The scene remains casual and humorous, centered on camaraderie and light-hearted teasing on the court [citation:txt3].

Three men then discuss and humorously rate the product: the white-hoodie man (ZHYPE) calls it suitable for kids but suggests a better gadget for beginners, scoring it “1.” They escalate to exaggerated scoring — “1,” “2,” then “-3k” — ending with a playful “what’s the next invention?” [citation:txt2]. The segment concludes with the group transitioning to the next challenge, the Flick Glove, though the exact transition is not detailed in this section’s evidence.
```

## 7. Grounded body (exactly as in report.md)

```
# Straight Shooter Strap Test: Demonstration, Shooting Drill, and Forfeit Challenge

The “Straight Shooter Strap” is demonstrated by a man in a white hoodie on an outdoor basketball court under clear skies. He explains its function as stabilizing the elbow during shooting to prevent it from flaring outward, gesturing to his arm and adjusting the black strap on his own forearm while a third observer watches closely [13][14]. The strap’s design is visible in close-up with on-screen text, and the scene widens to show the full court, hoop, fence, and surrounding hills, emphasizing its practical application in a real-game context [13].

Following the demonstration, a player in a white shirt and patterned shorts begins a shooting sequence using the strap. The scoreboard updates after each shot: the player initially makes one shot (1/1), then misses several, with the tally climbing to 0/3 [12]. As the drill continues, he scores more shots, pushing the score to 3/16 [12]. Commentary tracks each attempt, with remarks such as “Dude, 15” and “Zach’s uses this thing, bro,” indicating active engagement from teammates [12]. The player smiles at the camera as he approaches 15 successful shots, with the backdrop of a large house and trees under clear skies [12].

After the shooting sequence, the player attempts a jump shot that misses. He expresses frustration, questioning whether his shot is broken or if the strap caused the miss. A teammate confirms the issue, and another asks what the forfeit is, prompting the player to suggest 30 jumping jacks as punishment [15]. The group gathers near the hoop, holding basketballs and engaging in lighthearted banter [15].

The man in the white shirt begins performing jumping jacks, raising his arms with each bounce, while two others—wearing a red and white jersey and a white hoodie—watch [16][17]. Teasing ensues, with one observer joking, “Bounce some titties, boy,” and later comparing chest sizes, saying, “Jadil got a bigger chest than you” [16][18]. The man in the white shirt deflects with humor, replying, “Bro, I'm wearing a big shirt.” His movements become off-rhythm, with his feet moving out of sync with his hands, drawing amused observation from the two onlookers [17][19]. The scene remains casual and humorous, centered on camaraderie and light-hearted teasing on the court [17].

Three men then discuss and humorously rate the product: the white-hoodie man (ZHYPE) calls it suitable for kids but suggests a better gadget for beginners, scoring it “1.” They escalate to exaggerated scoring — “1,” “2,” then “-3k” — ending with a playful “what’s the next invention?” [20]. The segment concludes with the group transitioning to the next challenge, the Flick Glove, though the exact transition is not detailed in this section’s evidence.
```

## 8. References used by this section (global numbers)

```
[12] 00:03:00–00:06:00 · episodic 3min: Three men gather on an outdoor basketball court, negotiating positions before settling into a shooting challenge. One man in a black hoodie and white cap adjusts a basketball on a training device while the others—wear...
[13] 00:04:30–00:05:00 · episodic 30sec: A man in a white hoodie demonstrates a black elbow strap called the “Straight Shooter Strap” on an outdoor basketball court, explaining how it stabilizes the elbow during shooting by preventing it from flaring outward...
[14] 00:04:30–00:04:40 · episodic 10sec: Three men are on an outdoor basketball court. One man in a white hoodie holds a basketball and demonstrates a black strap called the "Straight Shooter Strap," explaining its use while the other two watch. The strap is...
[15] 00:07:00–00:07:10 · episodic 10sec: On a sunny day at an outdoor basketball court, a player in a white shirt and patterned shorts attempts a jump shot, then turns to his teammates after the ball misses the basket. He expresses frustration, questioning w...
[16] 00:07:10–00:07:20 · episodic 10sec: Three men are on an outdoor basketball court. One man in a white shirt and patterned shorts begins doing jumping jacks, raising his arms with each bounce. The other two men, one in a red and white jersey and another i...
[17] 00:07:00–00:07:30 · episodic 30sec: A player in a white shirt and patterned shorts attempts a jump shot that misses, prompting frustration and speculation about whether his shot is broken or if the strap caused the miss. His teammate confirms the issue,...
[18] Video-level knowledge (semantic memory, no timestamp): (man doing jumping jacks, is teased about, chest size)
[19] 00:07:20–00:07:30 · episodic 10sec: Three men are on an outdoor basketball court. One man in a white t-shirt and patterned shorts is performing jumping jacks while two others watch. One of the watchers, in a tie-dye jersey, comments on the man’s shirt s...
[20] 00:06:00–00:09:00 · episodic 3min: A man in a white hoodie and patterned shorts shoots basketballs on a sunny court, with a score counter updating after each shot — from 0/0 to 3/5 — while a humorous voiceover references product ownership and investmen...
```
