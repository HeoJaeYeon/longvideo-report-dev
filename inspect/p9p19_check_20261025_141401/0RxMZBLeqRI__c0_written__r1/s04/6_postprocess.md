# Section 4 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 483 words → after removal 483 words

## 2. Start/end claim check (`boundary_claims`)

- none

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 16, "cited_sentences": 5, "checked_tokens": 8, "unsupported": 0, "miscited": 0, "uncited_claims": 1, "absence_statements": 0}`

- **uncited**  `['00:01:00']` cited [] — At 00:01:00, the video introduces the enigma of Roma origins, opening with a map animation tracing migration from the Middle East and South Asia into Europe.

## 4. Citation conversion stats

- `{"text_citations": 17, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 1, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 7 of 12

## 5. Image-text time alignment

- img3 frame 00:01:15: gap to text cited in the same paragraph 0.0 s (ranges ['00:00:00-00:10:00']), to any text cited in the section 0.0 s

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Historical Narrative of Roma Origins and Early Misidentification

At 00:01:00, the video introduces the enigma of Roma origins, opening with a map animation tracing migration from the Middle East and South Asia into Europe. This visual anchors the Roma’s presence in the Balkans since the 13th century, while a 3D figure holding a red question mark symbolizes the enduring mystery surrounding their origins [citation:txt1]. The narrative then transitions to a stylized 13th-century map of Europe and the Balkans, featuring a dancing woman in traditional attire — visually anchoring Roma cultural presence in the region [citation:txt3]. This map is followed by a depiction of a faceless crowd and a red arrow pointing toward the Balkans, indicating movement or migration [citation:txt3].

At 00:01:10, the video presents a “VS” graphic, introducing a symbolic conflict between the Seljuk Turks — represented by an illustrated figure wearing a red fez — and the Byzantine Empire, symbolized by a crowned figure [citation:txt3][citation:txt11]. The narration explicitly frames this as a geopolitical tension of the era, setting the stage for how Roma would later be misidentified [citation:txt3]. The scene transitions to a map highlighting the Balkans again, overlaid by a man in a red shirt, white shorts, and fez, seemingly walking along the arrow’s path — visually suggesting migration [citation:txt2]. This is followed by a historical battle scene with mounted soldiers, blue banners, and fallen warriors, reinforcing the context of warfare between Christian and Muslim forces [citation:txt2].

The narration explains that the first Gypsy arrivals were mistaken for Seljuk Turks by the Byzantines, due to the ongoing conflicts between Christian Europe and Muslim Turks [citation:txt1][citation:txt2]. The video thus positions Roma not as a distinct ethnic group but as a product of historical misreading and geopolitical conflict — their arrival coinciding with the collapse of empires and the rise of new identities [citation:txt5]. The visual narrative reinforces how Roma were not “invented” but rather misclassified, their identity embedded in the historical and political landscape of the time [citation:txt5]. The imagery of the battle, combined with the “VS” graphic, underscores how Roma were labeled by empires caught in the crossfire of imperial rivalry [citation:txt3].

The video further frames this misidentification as part of a broader pattern of historical erasure, where Roma were categorized as “foreign” and “dangerous” through religious and cultural binaries — as seen in the transition to a medieval battle painting with the text “SARACEN = HEATHENS” [citation:txt5]. This visual and narrative framing positions Roma as a product of historical misreading, shaped by the victors’ geopolitical narratives [citation:txt5]. The use of symbolic figures, maps, and battle imagery serves to show how Roma were labeled by empires — not as an ethnic group, but as a consequence of historical conflict and misreading [citation:txt5]. The video thus concludes this section by reinforcing that Roma were not “invented” but misclassified — their identity forged in the crucible of empire and war [citation:txt5].

![](citation:img3)
```

## 7. Grounded body (exactly as in report.md)

```
# Historical Narrative of Roma Origins and Early Misidentification

At 00:01:00, the video introduces the enigma of Roma origins, opening with a map animation tracing migration from the Middle East and South Asia into Europe. This visual anchors the Roma’s presence in the Balkans since the 13th century, while a 3D figure holding a red question mark symbolizes the enduring mystery surrounding their origins [9]. The narrative then transitions to a stylized 13th-century map of Europe and the Balkans, featuring a dancing woman in traditional attire — visually anchoring Roma cultural presence in the region [10]. This map is followed by a depiction of a faceless crowd and a red arrow pointing toward the Balkans, indicating movement or migration [10].

At 00:01:10, the video presents a “VS” graphic, introducing a symbolic conflict between the Seljuk Turks — represented by an illustrated figure wearing a red fez — and the Byzantine Empire, symbolized by a crowned figure [10][11]. The narration explicitly frames this as a geopolitical tension of the era, setting the stage for how Roma would later be misidentified [10]. The scene transitions to a map highlighting the Balkans again, overlaid by a man in a red shirt, white shorts, and fez, seemingly walking along the arrow’s path — visually suggesting migration [12]. This is followed by a historical battle scene with mounted soldiers, blue banners, and fallen warriors, reinforcing the context of warfare between Christian and Muslim forces [12].

The narration explains that the first Gypsy arrivals were mistaken for Seljuk Turks by the Byzantines, due to the ongoing conflicts between Christian Europe and Muslim Turks [9][12]. The video thus positions Roma not as a distinct ethnic group but as a product of historical misreading and geopolitical conflict — their arrival coinciding with the collapse of empires and the rise of new identities [4]. The visual narrative reinforces how Roma were not “invented” but rather misclassified, their identity embedded in the historical and political landscape of the time [4]. The imagery of the battle, combined with the “VS” graphic, underscores how Roma were labeled by empires caught in the crossfire of imperial rivalry [10].

The video further frames this misidentification as part of a broader pattern of historical erasure, where Roma were categorized as “foreign” and “dangerous” through religious and cultural binaries — as seen in the transition to a medieval battle painting with the text “SARACEN = HEATHENS” [4]. This visual and narrative framing positions Roma as a product of historical misreading, shaped by the victors’ geopolitical narratives [4]. The use of symbolic figures, maps, and battle imagery serves to show how Roma were labeled by empires — not as an ethnic group, but as a consequence of historical conflict and misreading [4]. The video thus concludes this section by reinforcing that Roma were not “invented” but misclassified — their identity forged in the crucible of empire and war [4].

![Figure 5 (00:01:15)](frames/0RxMZBLeqRI_00011000.jpg)

*Figure 5. Frame at 00:01:15 (clip 00:01:10–00:01:20). An animated map of Europe and the Balkans from the 13th century is shown, featuring a stylized woman in traditional attire dancing. The scene transitions to a depiction of a large, faceless crowd, followed by a map highlighting a red arrow pointing toward the Balkans. This is followed by a “VS” g...*
```

## 8. References used by this section (global numbers)

```
[4] 00:00:00–00:10:00 · episodic 10min: **[Event 1: Introduction and Context Setting]**  
The video opens with a disclaimer clarifying the use of “Gypsy” as a non-slandrous term for Roma/Romani, followed by a map of the Balkans and a montage of memes and hi...
[9] 00:01:00–00:01:30 · episodic 30sec: **[Event 1: Introduction and Origin Mystery]**  
The video opens with a title card posing the question “Who are the Gypsies?” and immediately sets the tone by presenting a map animation tracing the historical spread f...
[10] 00:01:10–00:01:20 · episodic 10sec: An animated map of Europe and the Balkans from the 13th century is shown, featuring a stylized woman in traditional attire dancing. The scene transitions to a depiction of a large, faceless crowd, followed by a map hi...
[11] Video-level knowledge (semantic memory, no timestamp): (Seljuk Turks, symbolized by, illustrated figure wearing red fez)
[12] 00:01:20–00:01:30 · episodic 10sec: A graphic depicts a stylized face of a Seljuk Turk on the left and a Byzantine emperor on the right, separated by a large "VS" symbol, illustrating conflict. The scene transitions to a map of the region showing a red...
```
