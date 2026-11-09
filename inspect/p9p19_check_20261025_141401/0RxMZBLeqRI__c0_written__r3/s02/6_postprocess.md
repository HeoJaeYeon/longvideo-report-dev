# Section 2 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 828 words → after removal 828 words

## 2. Start/end claim check (`boundary_claims`)

- opening_unverifiable: At 00:12:40, the video opens with a portrait of Ion Budai-Deleanu, the Romanian poet and author of *Tiganiada*, followed by a computer-generated medieval battle animation. (cited [])

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 28, "cited_sentences": 4, "checked_tokens": 6, "unsupported": 1, "miscited": 0, "uncited_claims": 2, "absence_statements": 0}`

- **uncited**  `['00:10:00']` cited [] — At 00:10:00, the video shifts focus to 15th-century Eastern Europe, presenting a montage of historical visuals—sepia-toned photographs, paintings, and CGI animations—to depict Roma labor and warfare under Romanian rulers post-1471.
- **uncited**  `['00:12:40']` cited [] — At 00:12:40, the video opens with a portrait of Ion Budai-Deleanu, the Romanian poet and author of *Tiganiada*, followed by a computer-generated medieval battle animation.
- **unsupported** quote `couple = barrels` cited ['txt2', 'txt3', 'txt6'] — This imagery is juxtaposed with abstract equations, such as “person = pig,” “male = bull,” and “couple = barrels,” which encode social or economic value in minimalist icon-based visuals [citation:txt2][citation:txt3][citation:txt6].

## 4. Citation conversion stats

- `{"text_citations": 46, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 0, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 6 of 12

## 5. Image-text time alignment

- no cited image

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Historical and Cultural Portrayal of Roma from 00:10:00–00:20:00

At 00:10:00, the video shifts focus to 15th-century Eastern Europe, presenting a montage of historical visuals—sepia-toned photographs, paintings, and CGI animations—to depict Roma labor and warfare under Romanian rulers post-1471. The narrative highlights Moldavian and Wallachian rulers’ strategic use of Roma slave labor and warriors in military campaigns against Ottoman expansion. The epic *Tiganiada* by Ion Budai-Deleanu is referenced as both historical record and cultural myth, with animated battle scenes illustrating Gypsy-led armies under Vlad Cepish confronting Ottoman forces [citation:txt1][citation:txt2][citation:txt3]. These visuals are intercut with symbolic imagery, including falling dollar bills over Ottoman maps and the phrase “ITS OVER,” suggesting commentary on economic and geopolitical power shifts [citation:txt1][citation:txt2][citation:txt3][citation:txt4].

The video deepens its symbolic layering by framing *Tiganiada* as a metaphor for conquest, transformation, and resistance. Animated and live-action battle sequences depict Roma armies in combat with Ottoman forces, while visual metaphors—such as cartoonish figures and falling currency—layer economic critique onto historical conflict [citation:txt2]. The tone remains satirical yet analytical, using the epic as a lens to interrogate power structures, cultural identity, and the commodification of history [citation:txt2]. The video positions the Roma experience not merely as historical fact but as a narrative of agency and mythmaking [citation:txt2].

At 00:12:40, the video opens with a portrait of Ion Budai-Deleanu, the Romanian poet and author of *Tiganiada*, followed by a computer-generated medieval battle animation. The animation depicts a large-scale clash between two armies—one mounted on horseback and the other on foot—with soldiers wielding swords and shields. The narration identifies Vlad Cepish as the leader of the Roma army engaged in combat against the Ottoman Turks, directly inspired by the themes and characters in *Tiganiada* [citation:txt4]. The scene then transitions to a live-action-style battle with horseback soldiers clashing in a dusty field, reinforcing the epic’s martial imagery [citation:txt4]. The video cuts to a map of the Ottoman Empire, overlaid with the text “ITS OVER” and a cartoon image of a man with glasses, followed by a final frame showing dollar bills falling over a highlighted region on the map [citation:txt4][citation:txt7].

The video’s symbolic use of falling dollar bills over Ottoman maps appears as a recurring motif, visually linking economic power with geopolitical conflict and suggesting commentary on the commodification of historical narratives [citation:txt1][citation:txt2][citation:txt3][citation:txt4]. This imagery is juxtaposed with abstract equations, such as “person = pig,” “male = bull,” and “couple = barrels,” which encode social or economic value in minimalist icon-based visuals [citation:txt2][citation:txt3][citation:txt6]. The sequence culminates in a video game scene where an armored character demands payment or imprisonment for stolen goods, abruptly shifting from symbolic abstraction to direct confrontation [citation:txt2][citation:txt3][citation:txt6]. This transition suggests themes of exploitation, systemic control, and the commodification of labor, framing the narrative as a critique of power structures that reduce human value to economic exchange [citation:txt2][citation:txt3][citation:txt6].

The video’s abstract symbolism is further reinforced by visual equations, including a wheelchair accessibility symbol equated to a jar of honey, followed by a blank screen, and a pregnant woman icon joining a child icon before cutting to the video game confrontation [citation:txt6]. The juxtaposition of historical battle imagery with modern visual metaphors—such as falling money and the “ITS OVER” text—implies a layered interpretation: the epic’s legacy may be viewed as both a historical narrative and a commentary on power, conquest, and economic transformation [citation:txt4]. The tone remains playful yet informative, blending literary, historical, and satirical elements [citation:txt4].

The video’s final segment in this section employs minimalist icon-based equations to encode social or economic value, culminating in a video game scene where an armored character confronts the viewer, demanding payment or imprisonment for stolen goods—a stark shift from symbolic abstraction to narrative confrontation [citation:txt2][citation:txt3][citation:txt6]. This suggests themes of exploitation, justice, or systemic control, framing the narrative as a critique of power structures that reduce human value to economic exchange [citation:txt2][citation:txt3][citation:txt6].

The video’s symbolic use of falling dollar bills over Ottoman maps, abstract equations, and video game confrontations collectively frame Roma as agents of resistance and cultural continuity despite systemic oppression [citation:txt2]. The visual metaphors and symbolic layering underscore how historical narratives and visual representations are used to interrogate power structures, cultural identity, and the commodification of history [citation:txt2]. The video’s satirical yet analytical tone positions Roma not merely as historical subjects but as active participants in mythmaking and resistance [citation:txt2].

The video’s abstract symbolism and narrative confrontations serve to critique power structures that reduce human value to economic exchange, while its historical visuals and literary references ground the narrative in the lived experiences of Roma as both warriors and subjects of historical mythmaking [citation:txt2][citation:txt3][citation:txt6]. The video’s use of visual metaphors and symbolic layering highlights the complexity of Roma identity and the ways in which it has been historically represented and reinterpreted [citation:txt2]. The video’s conclusion in this section, marked by the video game confrontation, suggests a thematic pivot toward systemic violence or historical trauma, framing the narrative as a critique of power structures that reduce human value to economic exchange [citation:txt2][citation:txt3][citation:txt6].
```

## 7. Grounded body (exactly as in report.md)

```
# Historical and Cultural Portrayal of Roma from 00:10:00–00:20:00

At 00:10:00, the video shifts focus to 15th-century Eastern Europe, presenting a montage of historical visuals—sepia-toned photographs, paintings, and CGI animations—to depict Roma labor and warfare under Romanian rulers post-1471. The narrative highlights Moldavian and Wallachian rulers’ strategic use of Roma slave labor and warriors in military campaigns against Ottoman expansion. The epic *Tiganiada* by Ion Budai-Deleanu is referenced as both historical record and cultural myth, with animated battle scenes illustrating Gypsy-led armies under Vlad Cepish confronting Ottoman forces [4][5][6]. These visuals are intercut with symbolic imagery, including falling dollar bills over Ottoman maps and the phrase “ITS OVER,” suggesting commentary on economic and geopolitical power shifts [4][5][6][7].

The video deepens its symbolic layering by framing *Tiganiada* as a metaphor for conquest, transformation, and resistance. Animated and live-action battle sequences depict Roma armies in combat with Ottoman forces, while visual metaphors—such as cartoonish figures and falling currency—layer economic critique onto historical conflict [5]. The tone remains satirical yet analytical, using the epic as a lens to interrogate power structures, cultural identity, and the commodification of history [5]. The video positions the Roma experience not merely as historical fact but as a narrative of agency and mythmaking [5].

At 00:12:40, the video opens with a portrait of Ion Budai-Deleanu, the Romanian poet and author of *Tiganiada*, followed by a computer-generated medieval battle animation. The animation depicts a large-scale clash between two armies—one mounted on horseback and the other on foot—with soldiers wielding swords and shields. The narration identifies Vlad Cepish as the leader of the Roma army engaged in combat against the Ottoman Turks, directly inspired by the themes and characters in *Tiganiada* [7]. The scene then transitions to a live-action-style battle with horseback soldiers clashing in a dusty field, reinforcing the epic’s martial imagery [7]. The video cuts to a map of the Ottoman Empire, overlaid with the text “ITS OVER” and a cartoon image of a man with glasses, followed by a final frame showing dollar bills falling over a highlighted region on the map [7][8].

The video’s symbolic use of falling dollar bills over Ottoman maps appears as a recurring motif, visually linking economic power with geopolitical conflict and suggesting commentary on the commodification of historical narratives [4][5][6][7]. This imagery is juxtaposed with abstract equations, such as “person = pig,” “male = bull,” and “couple = barrels,” which encode social or economic value in minimalist icon-based visuals [5][6][9]. The sequence culminates in a video game scene where an armored character demands payment or imprisonment for stolen goods, abruptly shifting from symbolic abstraction to direct confrontation [5][6][9]. This transition suggests themes of exploitation, systemic control, and the commodification of labor, framing the narrative as a critique of power structures that reduce human value to economic exchange [5][6][9].

The video’s abstract symbolism is further reinforced by visual equations, including a wheelchair accessibility symbol equated to a jar of honey, followed by a blank screen, and a pregnant woman icon joining a child icon before cutting to the video game confrontation [9]. The juxtaposition of historical battle imagery with modern visual metaphors—such as falling money and the “ITS OVER” text—implies a layered interpretation: the epic’s legacy may be viewed as both a historical narrative and a commentary on power, conquest, and economic transformation [7]. The tone remains playful yet informative, blending literary, historical, and satirical elements [7].

The video’s final segment in this section employs minimalist icon-based equations to encode social or economic value, culminating in a video game scene where an armored character confronts the viewer, demanding payment or imprisonment for stolen goods—a stark shift from symbolic abstraction to narrative confrontation [5][6][9]. This suggests themes of exploitation, justice, or systemic control, framing the narrative as a critique of power structures that reduce human value to economic exchange [5][6][9].

The video’s symbolic use of falling dollar bills over Ottoman maps, abstract equations, and video game confrontations collectively frame Roma as agents of resistance and cultural continuity despite systemic oppression [5]. The visual metaphors and symbolic layering underscore how historical narratives and visual representations are used to interrogate power structures, cultural identity, and the commodification of history [5]. The video’s satirical yet analytical tone positions Roma not merely as historical subjects but as active participants in mythmaking and resistance [5].

The video’s abstract symbolism and narrative confrontations serve to critique power structures that reduce human value to economic exchange, while its historical visuals and literary references ground the narrative in the lived experiences of Roma as both warriors and subjects of historical mythmaking [5][6][9]. The video’s use of visual metaphors and symbolic layering highlights the complexity of Roma identity and the ways in which it has been historically represented and reinterpreted [5]. The video’s conclusion in this section, marked by the video game confrontation, suggests a thematic pivot toward systemic violence or historical trauma, framing the narrative as a critique of power structures that reduce human value to economic exchange [5][6][9].
```

## 8. References used by this section (global numbers)

```
[4] 00:06:00–00:09:00 · episodic 3min: **[Event 1: Ghaznavid Empire’s Rise and Expansion]**  
The video opens with a symbolic map of South Asia, silhouetted figures in turbans marking regional influence, narrowing to the Ghaznavid Empire’s territory across...
[5] 00:10:00–00:20:00 · episodic 10min: **[Event 1: Historical Labor and Warfare in 15th-Century Eastern Europe]**  
The video opens with a visual montage of 15th-century Eastern European warfare and Gypsy labor under Romanian rulers post-1471, blending sep...
[6] 00:12:00–00:15:00 · episodic 3min: **[Event 1: Historical Labor and Warfare in 15th-Century Eastern Europe]**  
The video opens with historical visuals—paintings, sepia photos, and CGI animations—depicting 15th-century Eastern European warfare and Gyps...
[7] 00:12:30–00:13:00 · episodic 30sec: **[Event 1: Introduction of Ion Budai-Deleanu and the Epic “Tiganiada”]**  
The video opens with a portrait of Ion Budai-Deleanu, the Romanian poet and author of the epic poem *Tiganiada*, written in the early 1800s....
[8] 00:12:50–00:13:00 · episodic 10sec: The video shows a battle scene with soldiers on horseback clashing in a dusty field, followed by a map of the Ottoman Empire. Text overlays appear, including "ITS OVER" accompanied by a cartoon image of a man with gla...
[9] 00:14:30–00:15:00 · episodic 30sec: **[Event 1: Historical Visuals and Symbolic Equations]**  
The video opens with a blurry historical painting featuring a figure in red headwear holding a child, transitioning to a close-up of an old Romanian document...
```
