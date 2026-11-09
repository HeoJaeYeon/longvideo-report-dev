# Section 2 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 585 words → after removal 585 words

## 2. Start/end claim check (`boundary_claims`)

- none

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 29, "cited_sentences": 10, "checked_tokens": 18, "unsupported": 0, "miscited": 0, "uncited_claims": 1, "absence_statements": 0}`

- **uncited**  `['00:02:30']` cited [] — The group prepares to test the SKLZ Dribble Stick, a black training device with adjustable yellow arms, at 00:02:30.

## 4. Citation conversion stats

- `{"text_citations": 29, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 0, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 4 of 12

## 5. Image-text time alignment

- no cited image

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Testing the SKLZ Dribble Stick and the Straight Shooter Strap

The group prepares to test the SKLZ Dribble Stick, a black training device with adjustable yellow arms, at 00:02:30. The man in the red hoodie introduces the challenge, while the man in the blue jersey prepares to demonstrate its use [citation:txt3]. The rules are reviewed: players take turns dribbling while avoiding contact with the stick; the first to touch it must run five laps around the court [citation:txt3][citation:txt4]. The device is shown in detail, including its branding and construction, with close-up shots highlighting its design [citation:txt5][citation:txt4]. The group assembles on the court, each holding a basketball, ready to begin [citation:txt4]. The man in the blue jersey leads the demonstration, dribbling while the others watch [citation:txt3]. After the demonstration, the group evaluates the stick. The man in the blue jersey rates it an 8/10, the man in the black shirt agrees, and the man in the black hoodie gives it a 7, joking that anything helping him fail is “pretty good” [citation:txt1][citation:txt2]. The conversation remains lighthearted and collaborative [citation:txt1].

Following the dribble stick test, the group transitions to evaluating the Straight Shooter Strap. A man in a white hoodie demonstrates the device, explaining how it stabilizes the elbow during shooting by preventing it from flaring outward [citation:txt6]. He adjusts the strap on his own arm while a third observer watches [citation:txt6]. The scene widens to show the full court, hoop, fence, and surrounding hills under a clear sky, setting up the practical application of the strap [citation:txt6]. The strap is then used in a shooting challenge. A shooter in a white shirt and patterned shorts begins a sequence, initially making one shot (0/1), then missing several, with the scoreboard climbing to 0/3 [citation:txt2]. He pauses, inspecting his elbow, seemingly frustrated [citation:txt2]. As the sequence continues, he scores more shots, pushing the tally to 3/16, with teammates retrieving balls and commentary tracking each attempt [citation:txt2]. The scoreboard climbs steadily, accompanied by remarks like “Dude, 15,” and “Zach’s uses this thing, bro” [citation:txt2]. The player smiles at the camera as he approaches 15 successful shots, with the backdrop of a large house and trees under clear skies [citation:txt2].

Later, a second player makes a shot (1/2), but audio commentary criticizes the product’s performance, noting it “fell off” and “snaps” when extended [citation:txt1]. A shooting contest unfolds: a player in a red and white jersey (No. 2) makes a successful shot (2/5), celebrated with surprise and joy [citation:txt1]. The tie-dye jersey player loses, prompting the white-shirted man to propose testing his jump shot without the strap to isolate the issue — a playful, lighthearted challenge [citation:txt1]. His jump shot misses, sparking frustration and speculation about the strap [citation:txt1]. A teammate confirms the issue, and a forfeit of 30 jumping jacks is suggested [citation:txt1]. The man in the white shirt begins doing jumping jacks, raising his arms with each bounce, while the other two—wearing a red and white jersey and a white hoodie—watch [citation:txt8]. Teasing ensues, with one observer joking, “Bounce some titties, boy,” and later comparing chest sizes, saying, “Jadil got a bigger chest than you” [citation:txt8]. The man in the white shirt deflects with humor, replying, “Bro, I’m wearing a big shirt” [citation:txt8]. As he continues the jumping jacks, his movements become off-rhythm, with his feet moving out of sync with his hands, drawing amused observation from the two onlookers [citation:txt7][citation:txt8]. The scene remains casual and humorous, centered on camaraderie and light-hearted teasing on the court [citation:txt8].
```

## 7. Grounded body (exactly as in report.md)

```
# Testing the SKLZ Dribble Stick and the Straight Shooter Strap

The group prepares to test the SKLZ Dribble Stick, a black training device with adjustable yellow arms, at 00:02:30. The man in the red hoodie introduces the challenge, while the man in the blue jersey prepares to demonstrate its use [8]. The rules are reviewed: players take turns dribbling while avoiding contact with the stick; the first to touch it must run five laps around the court [8][9]. The device is shown in detail, including its branding and construction, with close-up shots highlighting its design [10][9]. The group assembles on the court, each holding a basketball, ready to begin [9]. The man in the blue jersey leads the demonstration, dribbling while the others watch [8]. After the demonstration, the group evaluates the stick. The man in the blue jersey rates it an 8/10, the man in the black shirt agrees, and the man in the black hoodie gives it a 7, joking that anything helping him fail is “pretty good” [2][11]. The conversation remains lighthearted and collaborative [2].

Following the dribble stick test, the group transitions to evaluating the Straight Shooter Strap. A man in a white hoodie demonstrates the device, explaining how it stabilizes the elbow during shooting by preventing it from flaring outward [12]. He adjusts the strap on his own arm while a third observer watches [12]. The scene widens to show the full court, hoop, fence, and surrounding hills under a clear sky, setting up the practical application of the strap [12]. The strap is then used in a shooting challenge. A shooter in a white shirt and patterned shorts begins a sequence, initially making one shot (0/1), then missing several, with the scoreboard climbing to 0/3 [11]. He pauses, inspecting his elbow, seemingly frustrated [11]. As the sequence continues, he scores more shots, pushing the tally to 3/16, with teammates retrieving balls and commentary tracking each attempt [11]. The scoreboard climbs steadily, accompanied by remarks like “Dude, 15,” and “Zach’s uses this thing, bro” [11]. The player smiles at the camera as he approaches 15 successful shots, with the backdrop of a large house and trees under clear skies [11].

Later, a second player makes a shot (1/2), but audio commentary criticizes the product’s performance, noting it “fell off” and “snaps” when extended [2]. A shooting contest unfolds: a player in a red and white jersey (No. 2) makes a successful shot (2/5), celebrated with surprise and joy [2]. The tie-dye jersey player loses, prompting the white-shirted man to propose testing his jump shot without the strap to isolate the issue — a playful, lighthearted challenge [2]. His jump shot misses, sparking frustration and speculation about the strap [2]. A teammate confirms the issue, and a forfeit of 30 jumping jacks is suggested [2]. The man in the white shirt begins doing jumping jacks, raising his arms with each bounce, while the other two—wearing a red and white jersey and a white hoodie—watch [13]. Teasing ensues, with one observer joking, “Bounce some titties, boy,” and later comparing chest sizes, saying, “Jadil got a bigger chest than you” [13]. The man in the white shirt deflects with humor, replying, “Bro, I’m wearing a big shirt” [13]. As he continues the jumping jacks, his movements become off-rhythm, with his feet moving out of sync with his hands, drawing amused observation from the two onlookers [14][13]. The scene remains casual and humorous, centered on camaraderie and light-hearted teasing on the court [13].
```

## 8. References used by this section (global numbers)

```
[2] 00:00:00–00:10:00 · episodic 10min: **Six men—Chris, Zach, Cass, James, Mitchell, and an unnamed sixth player—gather on a sunny outdoor basketball court to test 12 viral sports gadgets, splitting into two teams of three. Dressed in athletic wear, they i...
[8] 00:02:30–00:03:00 · episodic 30sec: Three men gather on an outdoor basketball court, preparing for a dribbling challenge using a SKLZ Dribble Stick. The man in the red hoodie introduces the game, asking if they want to see how the dribble stick works, w...
[9] 00:02:50–00:03:00 · episodic 10sec: A close-up shot shows a black "Dribble Stick" device with a yellow logo. The scene then transitions to an outdoor basketball court where three men are gathered. One man in a red hoodie holds a basketball and a white d...
[10] 00:02:40–00:02:50 · episodic 10sec: A man in a red hoodie holds a basketball while standing on a basketball court with two other men, one in a blue jersey and another in a black shirt and cap. The scene transitions to a close-up of a black training devi...
[11] 00:03:00–00:06:00 · episodic 3min: Three men gather on an outdoor basketball court, negotiating positions before settling into a shooting challenge. One man in a black hoodie and white cap adjusts a basketball on a training device while the others—wear...
[12] 00:04:30–00:05:00 · episodic 30sec: A man in a white hoodie demonstrates a black elbow strap called the “Straight Shooter Strap” on an outdoor basketball court, explaining how it stabilizes the elbow during shooting by preventing it from flaring outward...
[13] 00:07:00–00:07:30 · episodic 30sec: A player in a white shirt and patterned shorts attempts a jump shot that misses, prompting frustration and speculation about whether his shot is broken or if the strap caused the miss. His teammate confirms the issue,...
[14] 00:07:20–00:07:30 · episodic 10sec: Three men are on an outdoor basketball court. One man in a white t-shirt and patterned shorts is performing jumping jacks while two others watch. One of the watchers, in a tie-dye jersey, comments on the man’s shirt s...
```
