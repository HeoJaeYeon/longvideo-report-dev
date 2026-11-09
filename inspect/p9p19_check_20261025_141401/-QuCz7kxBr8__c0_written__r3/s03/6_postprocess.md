# Section 3 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 481 words → after removal 481 words

## 2. Start/end claim check (`boundary_claims`)

- none

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 19, "cited_sentences": 8, "checked_tokens": 16, "unsupported": 0, "miscited": 0, "uncited_claims": 1, "absence_statements": 0}`

- **uncited**  `['Straight Shooter Strap', '00:04:30']` cited [] — At 00:04:30, a man in a white hoodie demonstrates the “Straight Shooter Strap,” a black elbow strap, on an outdoor basketball court.

## 4. Citation conversion stats

- `{"text_citations": 17, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 3, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 6 of 12

## 5. Image-text time alignment

- img1 frame 00:20:15: gap to text cited in the same paragraph 675.0 s (ranges ['00:06:00-00:09:00', '00:08:00-00:08:30', '00:08:20-00:08:30']), to any text cited in the section 675.0 s
- img2 frame 00:32:35: gap to text cited in the same paragraph 1415.0 s (ranges ['00:06:00-00:09:00', '00:08:00-00:08:30', '00:08:20-00:08:30']), to any text cited in the section 1415.0 s
- img3 frame 00:20:05: gap to text cited in the same paragraph 665.0 s (ranges ['00:06:00-00:09:00', '00:08:00-00:08:30', '00:08:20-00:08:30']), to any text cited in the section 665.0 s

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Testing the Straight Shooter Strap and Flick Glove

At 00:04:30, a man in a white hoodie demonstrates the “Straight Shooter Strap,” a black elbow strap, on an outdoor basketball court. He explains how the strap stabilizes the elbow during shooting by preventing it from flaring outward, gesturing to his own arm while close-ups of the strap appear on screen with on-screen text [citation:txt1]. He adjusts the strap on his arm, then steps back as another player holds a basketball, preparing for a shooting challenge [citation:txt1]. The scene widens to show the full court, hoop, fence, and surrounding hills under a clear sky, establishing a real-game context for the test [citation:txt1].

The shooting challenge begins with the strap in use. A player in a white shirt and patterned shorts shoots multiple times, with a score counter updating from 0/0 to 3/5 [citation:txt3]. A humorous voiceover references product ownership and investment, and the man praises the product as “great,” with a “#NOT SPONSORED” graphic [citation:txt3]. Another player in a tie-dye jersey loses the challenge, prompting the white-shirted man to suggest testing his jump shot without the strap to isolate whether the issue is the strap or his shot [citation:txt5]. His jump shot misses, sparking frustration and speculation among teammates [citation:txt3]. A teammate suggests a forfeit of 30 jumping jacks, which the man begins performing while two others watch and tease — one jokes about “bouncing titties,” another compares chest sizes; he deflects with humor, “Bro, I’m wearing a big shirt,” while his movements become off-rhythm, drawing amused observation [citation:txt3].

Three men then humorously rate the product: the white-hoodie man (ZHYPE) calls it suitable for kids but suggests a better gadget for beginners, scoring it “1.” They escalate to exaggerated scoring — “1,” “2,” then “-3k” — ending with a playful “what’s the next invention?” [citation:txt3].

The Flick Glove is introduced next. At 00:08:00, a man in a black hoodie and white cap explains the rules of the challenge: take three shots with the glove, then three without, and the person making the fewest baskets must do 100 sit-ups [citation:txt6]. A text overlay confirms this rule [citation:txt7]. The man in the red hoodie expresses confusion about the glove’s orientation, prompting the black-hoodie man to demonstrate its use [citation:txt7]. The glove’s design — featuring finger loops and a rectangular screen — is shown in close-up, along with color options (white, black, orange) and the brand name “FLICK GLOVE” [citation:txt6][citation:txt12]. The challenge begins with players preparing to shoot, and the blue-jersey man later makes a shot, celebrated with “Woo!” and “WHOOOOOO” graphics [citation:txt3]. The black-hoodie man also makes a shot, with teammates debating whether it was “too far” or “cheating,” but later celebrating his success [citation:txt3]. The video does not show the full execution of the challenge beyond setup and reactions, nor does it show the forfeit of sit-ups being performed [citation:txt3].

![](citation:img1)  
![](citation:img2)  
![](citation:img3)
```

## 7. Grounded body (exactly as in report.md)

```
# Testing the Straight Shooter Strap and Flick Glove

At 00:04:30, a man in a white hoodie demonstrates the “Straight Shooter Strap,” a black elbow strap, on an outdoor basketball court. He explains how the strap stabilizes the elbow during shooting by preventing it from flaring outward, gesturing to his own arm while close-ups of the strap appear on screen with on-screen text [14]. He adjusts the strap on his arm, then steps back as another player holds a basketball, preparing for a shooting challenge [14]. The scene widens to show the full court, hoop, fence, and surrounding hills under a clear sky, establishing a real-game context for the test [14].

The shooting challenge begins with the strap in use. A player in a white shirt and patterned shorts shoots multiple times, with a score counter updating from 0/0 to 3/5 [15]. A humorous voiceover references product ownership and investment, and the man praises the product as “great,” with a “#NOT SPONSORED” graphic [15]. Another player in a tie-dye jersey loses the challenge, prompting the white-shirted man to suggest testing his jump shot without the strap to isolate whether the issue is the strap or his shot [16]. His jump shot misses, sparking frustration and speculation among teammates [15]. A teammate suggests a forfeit of 30 jumping jacks, which the man begins performing while two others watch and tease — one jokes about “bouncing titties,” another compares chest sizes; he deflects with humor, “Bro, I’m wearing a big shirt,” while his movements become off-rhythm, drawing amused observation [15].

Three men then humorously rate the product: the white-hoodie man (ZHYPE) calls it suitable for kids but suggests a better gadget for beginners, scoring it “1.” They escalate to exaggerated scoring — “1,” “2,” then “-3k” — ending with a playful “what’s the next invention?” [15].

The Flick Glove is introduced next. At 00:08:00, a man in a black hoodie and white cap explains the rules of the challenge: take three shots with the glove, then three without, and the person making the fewest baskets must do 100 sit-ups [17]. A text overlay confirms this rule [18]. The man in the red hoodie expresses confusion about the glove’s orientation, prompting the black-hoodie man to demonstrate its use [18]. The glove’s design — featuring finger loops and a rectangular screen — is shown in close-up, along with color options (white, black, orange) and the brand name “FLICK GLOVE” [17][19]. The challenge begins with players preparing to shoot, and the blue-jersey man later makes a shot, celebrated with “Woo!” and “WHOOOOOO” graphics [15]. The black-hoodie man also makes a shot, with teammates debating whether it was “too far” or “cheating,” but later celebrating his success [15]. The video does not show the full execution of the challenge beyond setup and reactions, nor does it show the forfeit of sit-ups being performed [15].

![Figure 2 (00:20:15)](frames/-QuCz7kxBr8_00201000.jpg)

*Figure 2. Frame at 00:20:15 (clip 00:20:10–00:20:20). On a sunny day at an outdoor basketball court, a man in a black hoodie and white cap stands near the center, holding a basketball. He turns and walks toward the free-throw line as another player in a blue jersey stands nearby, posing with hands on hips. The camera pans to show the court’s marking...*

![Figure 3 (00:32:35)](frames/-QuCz7kxBr8_00323000.jpg)

*Figure 3. Frame at 00:32:35 (clip 00:32:30–00:32:40). A young man stands on an outdoor basketball court holding two large black training pads with red paw prints, as a large "1-0" graphic is superimposed over the scene. He turns to face another man in a black hoodie and white cap who is holding a basketball. The two men face each other on the court,...*

![Figure 4 (00:20:05)](frames/-QuCz7kxBr8_00200000.jpg)

*Figure 4. Frame at 00:20:05 (clip 00:20:00–00:20:10). On an outdoor basketball court, a man in a black hoodie and white cap demonstrates a device that appears to be used for hand restraint or training, showing it to two other men—one in a black t-shirt and another in a blue basketball jersey. The man in the hoodie holds the device, which has orange...*
```

## 8. References used by this section (global numbers)

```
[14] 00:04:30–00:05:00 · episodic 30sec: A man in a white hoodie demonstrates a black elbow strap called the “Straight Shooter Strap” on an outdoor basketball court, explaining how it stabilizes the elbow during shooting by preventing it from flaring outward...
[15] 00:06:00–00:09:00 · episodic 3min: A man in a white hoodie and patterned shorts shoots basketballs on a sunny court, with a score counter updating after each shot — from 0/0 to 3/5 — while a humorous voiceover references product ownership and investmen...
[16] 00:06:50–00:07:00 · episodic 10sec: On an outdoor basketball court, two players are engaged in a shooting contest. One player, wearing a white shirt and patterned shorts, holds a basketball and speaks, while the other, in a tie-dye jersey, adjusts his c...
[17] 00:08:00–00:08:30 · episodic 30sec: Three men on an outdoor basketball court prepare for a shooting challenge involving the Flick Glove — a device designed to improve basketball shooting technique. One man in a black hoodie and white cap, holding a bask...
[18] 00:08:20–00:08:30 · episodic 10sec: Three men stand on an outdoor basketball court. A text overlay explains a challenge: take three shots with a flick glove, then three without, and the person making the least baskets must do 100 sit-ups. One man in a r...
[19] Video-level knowledge (semantic memory, no timestamp): (Flick Gloves, has colors, white)
```
