# Section 2 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 322 words → after removal 322 words

## 2. Start/end claim check (`boundary_claims`)

- none

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 15, "cited_sentences": 6, "checked_tokens": 9, "unsupported": 0, "miscited": 0, "uncited_claims": 0, "absence_statements": 0}`

- no findings

## 4. Citation conversion stats

- `{"text_citations": 18, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 0, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 5 of 12

## 5. Image-text time alignment

- no cited image

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# First Gadget Test: SPORTS DRIBBLE SPECS Time Trial

The first gadget tested in the video is the “SPORTS DRIBBLE SPECS,” introduced with a close-up of its black nylon straps and buckles [citation:txt1]. The challenge is a dribbling time trial where participants must dribble through three cones and touch a pole to stop the clock [citation:txt2][citation:txt3]. The rules are clarified near a pool under bright sunlight, with the man in the white hoodie confirming that the slowest time results in a forfeit [citation:txt2][citation:txt3]. The drill is conducted on an outdoor basketball court, with players taking turns while timers capture their performance [citation:txt1].

Players Chris and Zach are explicitly shown performing the drill. Chris completes the trial in 10:85 seconds, as displayed on a timer during his run [citation:txt7]. Zach follows, finishing in 9:51 seconds, also captured by a visible timer [citation:txt1]. Commentary during the drill notes frustrations with the gadget’s handling, such as “handles were definitely off,” alongside praise for Zach’s performance, including “He’s making great time” [citation:txt1]. The group’s reactions include a score graphic flashing from 5 to 6, then 4, accompanied by teammates giving thumbs-up approval [citation:txt1].

After the completion of the dribbling time trial, the segment transitions to the next gadget, the SKLZ Dribble Stick. The transition is marked by a visual cut to the group preparing for the next test [citation:txt1]. The SKLZ Dribble Stick is introduced as a black training tool with adjustable yellow arms and “DRIBBLE STICK” branding [citation:txt4][citation:txt6]. The rules for this next challenge are reviewed: players take turns dribbling while avoiding contact with the stick; the person who fails first must run five laps around the court [citation:txt4][citation:txt5]. The blue-jerseyed player is shown preparing to demonstrate its use, while the group assembles, each holding a basketball, ready to begin [citation:txt4]. The setup for the next round of testing is complete, with the group positioned on the court and the device ready for use [citation:txt1][citation:txt4].
```

## 7. Grounded body (exactly as in report.md)

```
# First Gadget Test: SPORTS DRIBBLE SPECS Time Trial

The first gadget tested in the video is the “SPORTS DRIBBLE SPECS,” introduced with a close-up of its black nylon straps and buckles [1]. The challenge is a dribbling time trial where participants must dribble through three cones and touch a pole to stop the clock [7][2]. The rules are clarified near a pool under bright sunlight, with the man in the white hoodie confirming that the slowest time results in a forfeit [7][2]. The drill is conducted on an outdoor basketball court, with players taking turns while timers capture their performance [1].

Players Chris and Zach are explicitly shown performing the drill. Chris completes the trial in 10:85 seconds, as displayed on a timer during his run [8]. Zach follows, finishing in 9:51 seconds, also captured by a visible timer [1]. Commentary during the drill notes frustrations with the gadget’s handling, such as “handles were definitely off,” alongside praise for Zach’s performance, including “He’s making great time” [1]. The group’s reactions include a score graphic flashing from 5 to 6, then 4, accompanied by teammates giving thumbs-up approval [1].

After the completion of the dribbling time trial, the segment transitions to the next gadget, the SKLZ Dribble Stick. The transition is marked by a visual cut to the group preparing for the next test [1]. The SKLZ Dribble Stick is introduced as a black training tool with adjustable yellow arms and “DRIBBLE STICK” branding [9][10]. The rules for this next challenge are reviewed: players take turns dribbling while avoiding contact with the stick; the person who fails first must run five laps around the court [9][11]. The blue-jerseyed player is shown preparing to demonstrate its use, while the group assembles, each holding a basketball, ready to begin [9]. The setup for the next round of testing is complete, with the group positioned on the court and the device ready for use [1][9].
```

## 8. References used by this section (global numbers)

```
[1] 00:00:00–00:03:00 · episodic 3min: Six men—Chris, Zach, Cass, James, Mitchell, and a sixth unnamed player—gather on a sunny outdoor basketball court to test 12 viral sports gadgets, splitting into two teams of three. Dressed in athletic wear, they intr...
[2] 00:00:30–00:01:00 · episodic 30sec: A group of men on an outdoor basketball court introduces a gadget challenge where teams will select and test their favorite sports gear. The segment kicks off with one man in a white hoodie and blue shorts holding a b...
[7] 00:00:50–00:01:00 · episodic 10sec: Three men are standing outdoors near a pool, preparing for a basketball dribbling challenge. One man, wearing a white hoodie and patterned shorts, holds a basketball and speaks, while another in a white t-shirt stands...
[8] 00:01:10–00:01:20 · episodic 10sec: A basketball player in a white jersey dribbles through cones on an outdoor court, completing the drill as a timer displays “10:85 SECONDS.” He stops, turns, and interacts with another player holding a basketball. The...
[9] 00:02:30–00:03:00 · episodic 30sec: Three men gather on an outdoor basketball court, preparing for a dribbling challenge using a SKLZ Dribble Stick. The man in the red hoodie introduces the game, asking if they want to see how the dribble stick works, w...
[10] 00:02:40–00:02:50 · episodic 10sec: A man in a red hoodie holds a basketball while standing on a basketball court with two other men, one in a blue jersey and another in a black shirt and cap. The scene transitions to a close-up of a black training devi...
[11] 00:02:50–00:03:00 · episodic 10sec: A close-up shot shows a black "Dribble Stick" device with a yellow logo. The scene then transitions to an outdoor basketball court where three men are gathered. One man in a red hoodie holds a basketball and a white d...
```
