# Section 4 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 685 words → after removal 685 words

## 2. Start/end claim check (`boundary_claims`)

- none

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 23, "cited_sentences": 6, "checked_tokens": 10, "unsupported": 0, "miscited": 0, "uncited_claims": 0, "absence_statements": 0}`

- no findings

## 4. Citation conversion stats

- `{"text_citations": 46, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 0, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 4 of 12

## 5. Image-text time alignment

- no cited image

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Roma Resilience Amid Systemic Hardship: Cultural Endurance and Personal Agency

At 00:29:30, the video presents an animated woman in traditional attire standing with open arms against a cityscape, symbolizing cultural presence or welcome [citation:txt1]. This is followed by a sepia-toned religious figure and snowy boots, evoking historical or spiritual themes, before concluding with a family gathered indoors, television on — suggesting domestic normalcy or quiet resilience [citation:txt1]. The scene then transitions to a far-right rally in a Hungarian town, where men in dark clothing stand in formation with arms crossed, underscoring tension and intimidation [citation:txt1]. On-screen text indicates the rally has stirred fear within the Roma community [citation:txt1].

The video then shifts to an aerial view of a residential area with cluttered balconies and debris piled at building bases, hinting at displacement, neglect, or aftermath of conflict [citation:txt1]. This is followed by an aerial shot of a densely packed, cluttered apartment building, transitioning to narrow alleyways where people walk — suggesting urban hardship or confinement [citation:txt2]. The footage then cuts to a public rally where a woman speaks into a microphone while holding a sign, joined by four individuals holding signs that read “Én is cigány vagyok” (“I am also a Roma”), asserting identity and solidarity [citation:txt1][citation:txt2]. A man in a suit is shown seated at a table, signing a document — implying institutional recognition or legal action [citation:txt1].

The segment concludes with an animated character superimposed over a real-world archway with traffic, blending symbolic representation with urban reality — possibly signifying cultural endurance or resistance within a modern setting [citation:txt1]. Earlier in the section, at 00:28:50, a bar chart titled “Romania: Corruption Levels” (1990–2007) is displayed, with an animated character — brown-haired, wearing a black hat with a red band, white shirt, and red bow tie — appearing thoughtfully touching their chin [citation:txt3][citation:txt4]. The scene transitions to an outdoor shot of a young man in a yellow shirt and light pants dancing barefoot on dirt ground in front of a weathered apartment building covered with numerous satellite dishes — a stark, humanizing contrast to the preceding institutional imagery [citation:txt3][citation:txt4]. The France 24 logo is visible in the corner, indicating the source [citation:txt3][citation:txt4].

The video also features an animated character in traditional attire standing before urban apartment buildings, followed by archival footage of a woman dancing and a smiling man, concluding with a woman in a red headscarf speaking outdoors in front of a blue building — establishing a visual narrative blending cultural memory and personal testimony [citation:txt6][citation:txt8]. The animated character appears again in front of an urban backdrop, reinforcing the theme of cultural endurance [citation:txt7][citation:txt9]. At 00:26:00, the video shows an animated character in traditional attire with a black hat and red bow standing with arms outstretched in front of urban apartment buildings [citation:txt6][citation:txt8]. This is followed by a vintage photograph of a brass band with adults and children holding instruments, then black-and-white archival footage of a woman dancing with large hoop earrings, followed by a man in a hat smiling [citation:txt6][citation:txt8]. The segment ends with a woman in a red headscarf speaking to the camera outdoors in front of a blue building [citation:txt6][citation:txt8].

The video’s portrayal of Roma resilience is grounded in moments of cultural endurance, such as the dancing boy in front of a satellite-dish-covered building [citation:txt3][citation:txt4], and the animated character superimposed over urban architecture [citation:txt1][citation:txt9]. These images are juxtaposed with scenes of institutional exclusion, such as the far-right rally and the repatriation announcement, highlighting the tension between systemic hardship and personal agency [citation:txt1][citation:txt3]. The Roma woman at the rally saying “I am also a Roma” is a clear assertion of identity and solidarity, reinforcing the theme of resistance [citation:txt1][citation:txt2]. The video balances trauma with resistance, showing Roma as active agents in their own history, through both symbolic and documentary means [citation:txt1]. The animated character’s recurring presence across urban and archival settings underscores the continuity of Roma identity despite systemic exclusion [citation:txt1][citation:txt3][citation:txt4][citation:txt7][citation:txt8][citation:txt9]. The dancing boy, the animated character, and the Roma woman at the rally collectively illustrate how Roma culture persists and asserts itself in the face of institutional marginalization [citation:txt1][citation:txt3][citation:txt4][citation:txt6][citation:txt8].
```

## 7. Grounded body (exactly as in report.md)

```
# Roma Resilience Amid Systemic Hardship: Cultural Endurance and Personal Agency

At 00:29:30, the video presents an animated woman in traditional attire standing with open arms against a cityscape, symbolizing cultural presence or welcome [17]. This is followed by a sepia-toned religious figure and snowy boots, evoking historical or spiritual themes, before concluding with a family gathered indoors, television on — suggesting domestic normalcy or quiet resilience [17]. The scene then transitions to a far-right rally in a Hungarian town, where men in dark clothing stand in formation with arms crossed, underscoring tension and intimidation [17]. On-screen text indicates the rally has stirred fear within the Roma community [17].

The video then shifts to an aerial view of a residential area with cluttered balconies and debris piled at building bases, hinting at displacement, neglect, or aftermath of conflict [17]. This is followed by an aerial shot of a densely packed, cluttered apartment building, transitioning to narrow alleyways where people walk — suggesting urban hardship or confinement [18]. The footage then cuts to a public rally where a woman speaks into a microphone while holding a sign, joined by four individuals holding signs that read “Én is cigány vagyok” (“I am also a Roma”), asserting identity and solidarity [17][18]. A man in a suit is shown seated at a table, signing a document — implying institutional recognition or legal action [17].

The segment concludes with an animated character superimposed over a real-world archway with traffic, blending symbolic representation with urban reality — possibly signifying cultural endurance or resistance within a modern setting [17]. Earlier in the section, at 00:28:50, a bar chart titled “Romania: Corruption Levels” (1990–2007) is displayed, with an animated character — brown-haired, wearing a black hat with a red band, white shirt, and red bow tie — appearing thoughtfully touching their chin [19][20]. The scene transitions to an outdoor shot of a young man in a yellow shirt and light pants dancing barefoot on dirt ground in front of a weathered apartment building covered with numerous satellite dishes — a stark, humanizing contrast to the preceding institutional imagery [19][20]. The France 24 logo is visible in the corner, indicating the source [19][20].

The video also features an animated character in traditional attire standing before urban apartment buildings, followed by archival footage of a woman dancing and a smiling man, concluding with a woman in a red headscarf speaking outdoors in front of a blue building — establishing a visual narrative blending cultural memory and personal testimony [16][21]. The animated character appears again in front of an urban backdrop, reinforcing the theme of cultural endurance [22][23]. At 00:26:00, the video shows an animated character in traditional attire with a black hat and red bow standing with arms outstretched in front of urban apartment buildings [16][21]. This is followed by a vintage photograph of a brass band with adults and children holding instruments, then black-and-white archival footage of a woman dancing with large hoop earrings, followed by a man in a hat smiling [16][21]. The segment ends with a woman in a red headscarf speaking to the camera outdoors in front of a blue building [16][21].

The video’s portrayal of Roma resilience is grounded in moments of cultural endurance, such as the dancing boy in front of a satellite-dish-covered building [19][20], and the animated character superimposed over urban architecture [17][23]. These images are juxtaposed with scenes of institutional exclusion, such as the far-right rally and the repatriation announcement, highlighting the tension between systemic hardship and personal agency [17][19]. The Roma woman at the rally saying “I am also a Roma” is a clear assertion of identity and solidarity, reinforcing the theme of resistance [17][18]. The video balances trauma with resistance, showing Roma as active agents in their own history, through both symbolic and documentary means [17]. The animated character’s recurring presence across urban and archival settings underscores the continuity of Roma identity despite systemic exclusion [17][19][20][22][21][23]. The dancing boy, the animated character, and the Roma woman at the rally collectively illustrate how Roma culture persists and asserts itself in the face of institutional marginalization [17][19][20][16][21].
```

## 8. References used by this section (global numbers)

```
[16] 00:26:00–00:26:30 · episodic 30sec: **[Event 1]** An animated character in traditional attire stands before urban apartment buildings, followed by a vintage brass band photograph, archival footage of a woman dancing and a smiling man, concluding with a...
[17] 00:29:30–00:30:00 · episodic 30sec: An animated woman in traditional attire stands with open arms against a cityscape, symbolizing cultural presence or welcome, followed by a sepia-toned religious figure and snowy boots, evoking historical or spiritual...
[18] 00:29:50–00:30:00 · episodic 10sec: The video segment begins with an aerial view of a densely packed, cluttered apartment building, followed by scenes of people walking down a narrow alleyway. The footage then transitions to a public gathering where a w...
[19] 00:28:30–00:29:00 · episodic 30sec: **[Event 1: Opening Visuals and Setting Introduction]**  
The video opens with a black-and-white close-up of a young child staring directly at the camera, followed by a shot of another child gazing out a window — esta...
[20] 00:28:50–00:29:00 · episodic 10sec: A bar chart titled "Romania: Corruption Levels" is displayed, showing data from 1990 to 2007 with two categories: PRS Corruption and TI Corruption. An animated character with brown hair, wearing a black hat with a red...
[21] 00:26:00–00:26:10 · episodic 10sec: An animated character in a traditional outfit with a black hat and red bow stands with arms outstretched in front of a backdrop of urban apartment buildings. The scene transitions to a vintage photograph of a brass ba...
[22] 00:25:50–00:26:00 · episodic 10sec: The video segment begins with a black-and-white scene of a man playing a violin in a group, followed by a close-up of a bride and groom sharing an intimate moment. The scene then transitions to a traffic light with a...
[23] Video-level knowledge (semantic memory, no timestamp): (anime-style character, is in front of, urban backdrop)
```
