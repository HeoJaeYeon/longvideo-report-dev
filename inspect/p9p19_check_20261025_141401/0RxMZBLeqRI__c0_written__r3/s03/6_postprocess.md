# Section 3 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 647 words → after removal 647 words

## 2. Start/end claim check (`boundary_claims`)

- ending_unverifiable: The video ends with a somber reflection on enduring suffering and loss, underscoring the continuity of systemic marginalization across regimes. (cited [])

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 24, "cited_sentences": 4, "checked_tokens": 13, "unsupported": 0, "miscited": 3, "uncited_claims": 6, "absence_statements": 0}`

- **uncited**  `['00:20:00', '00:30:00']` cited [] — The video transitions from earlier historical portrayals of Roma identity to a stark depiction of institutionalized persecution, focusing on state-sanctioned violence and racial categorization from 00:20:00 to 00:30:00.
- **uncited**  `['Deutschblütiger', '00:22:00', '2']` cited [] — At 00:22:00, the video displays the Nazi-era document *Die Nürnberger Gesetze* (The Nuremberg Laws), which categorizes individuals into racial groups such as “Deutschblütiger,” “Mischling 2.
- **uncited**  `['1']` cited [] — Grades,” “Mischling 1.
- **uncited**  `['00:22:30', '1935', '9']` cited [] — At 00:22:30, the video shows a black-and-white mugshot of Maria Bihari, a Roma girl born November 9, 1935, presented in three angles — frontal, three-quarter, and profile — before transitioning to an outdoor Roma camp setting.
- **uncited**  `['1942']` cited [] — The video then documents the 1942 deportation to Auschwitz-Birkenau.
- **uncited**  `['Process of Revival', '1984', '1985']` cited [] — In a thematic transition, the video shifts to modern-day Bulgaria, where text overlays reference the “Process of Revival” (1984–1985), a state-sponsored assimilation policy that forced Gypsies to adopt Bulgarian names and relocate.
- **miscited** number `000` cited ['txt4'] found in ['txt1'] — Resistance led to family separation; by 1985, nearly all 400,000 Muslim Gypsies had assimilated [citation:txt4].
- **miscited** number `1985` cited ['txt4'] found in ['txt1'] — Resistance led to family separation; by 1985, nearly all 400,000 Muslim Gypsies had assimilated [citation:txt4].
- **miscited** number `400` cited ['txt4'] found in ['txt1'] — Resistance led to family separation; by 1985, nearly all 400,000 Muslim Gypsies had assimilated [citation:txt4].

## 4. Citation conversion stats

- `{"text_citations": 12, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 0, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 5 of 12

## 5. Image-text time alignment

- no cited image

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Institutionalized Persecution of Roma under German and Eastern European Regimes

The video transitions from earlier historical portrayals of Roma identity to a stark depiction of institutionalized persecution, focusing on state-sanctioned violence and racial categorization from 00:20:00 to 00:30:00. Archival footage and documents reveal the systematic marginalization of Roma under both Nazi Germany and Bulgarian state policies, with visual contrasts between concentration camp imagery and modern-day protests underscoring the continuity of systemic exclusion.

At 00:22:00, the video displays the Nazi-era document *Die Nürnberger Gesetze* (The Nuremberg Laws), which categorizes individuals into racial groups such as “Deutschblütiger,” “Mischling 2. Grades,” “Mischling 1. Grades,” and “Jude,” each marked with symbolic annotations — a legal framework that codified racial hierarchy and explicitly targeted Sinti and Roma alongside Jews [citation:txt4]. Immediately following, black-and-white Gestapo mugshots appear, identifying Ludwig Horvath, born January 12, 1889, as a “Zigeuner,” and Helene Baranks Huber, born in 1874, as a “Zigeunerin” — visually documenting state surveillance and racial labeling [citation:txt4][citation:txt12]. These mugshots are presented in an archival style, emphasizing bureaucratic dehumanization [citation:txt4].

At 00:22:30, the video shows a black-and-white mugshot of Maria Bihari, a Roma girl born November 9, 1935, presented in three angles — frontal, three-quarter, and profile — before transitioning to an outdoor Roma camp setting. The camp features wooden trailers, a central fire pit, gathered adults and children, and laundry hanging nearby. Horses and wagons are also shown, with people interacting with them, including two men guiding a horse — one holding a whip — illustrating the lived conditions of forced displacement and institutionalized segregation under Nazi rule [citation:txt5][citation:txt6]. The camp imagery is juxtaposed with the earlier Gestapo documentation, reinforcing the state’s control over Roma lives.

The video then documents the 1942 deportation to Auschwitz-Birkenau. At 00:23:20, a black-and-white scene shows prisoners — including women and children — walking along a barbed-wire fence, with the year “1942” superimposed and the location identified as “Auschwitz-Birkenau.” Containers labeled “GIFTGAS ZYKLON B” are shown, followed by piles of clothing and personal belongings — visually conveying the scale and brutality of the extermination process [citation:txt7]. The footage is consistent with the earlier depiction of camp life and state mobilization, reinforcing the systematic nature of the genocide.

In a thematic transition, the video shifts to modern-day Bulgaria, where text overlays reference the “Process of Revival” (1984–1985), a state-sponsored assimilation policy that forced Gypsies to adopt Bulgarian names and relocate. Resistance led to family separation; by 1985, nearly all 400,000 Muslim Gypsies had assimilated [citation:txt4]. The video overlays this historical policy with footage of rural Bulgaria — horse-drawn carts, mahalas, and grainy settlements — contrasting the state’s erasure of Gypsy identity with moments of cultural endurance, such as color footage of men with oxen carts and a violinist in an outdoor gathering [citation:txt4]. This juxtaposition highlights the resilience of Roma culture despite state-imposed assimilation.

The video concludes this section with a powerful visual of a black-and-white historical photograph showing a group of men, women, and children sitting on the ground in a barren field, their worn clothing and exhausted expressions conveying despair. A man stands nearby near a simple fence, overseeing them — an image that encapsulates displacement, suffering, and the aftermath of historical atrocity [citation:txt8]. The final frames juxtapose this with dark thematic transitions — hooded figures, Mengele’s image, and concentration camp aerials — evoking trauma and historical reckoning [citation:txt8]. The video ends with a somber reflection on enduring suffering and loss, underscoring the continuity of systemic marginalization across regimes.

The video’s use of stark visual contrasts — from concentration camp imagery to modern-day protests — serves to illustrate how state-sanctioned violence, racial categorization, and forced assimilation have persisted across multiple regimes, leaving a legacy of trauma and resilience [citation:txt1]. The evidence presented here confirms the institutionalized persecution of Roma under German and Eastern European regimes, documenting state-sponsored violence, bureaucratic racialization, and the enduring consequences of historical erasure.
```

## 7. Grounded body (exactly as in report.md)

```
# Institutionalized Persecution of Roma under German and Eastern European Regimes

The video transitions from earlier historical portrayals of Roma identity to a stark depiction of institutionalized persecution, focusing on state-sanctioned violence and racial categorization from 00:20:00 to 00:30:00. Archival footage and documents reveal the systematic marginalization of Roma under both Nazi Germany and Bulgarian state policies, with visual contrasts between concentration camp imagery and modern-day protests underscoring the continuity of systemic exclusion.

At 00:22:00, the video displays the Nazi-era document *Die Nürnberger Gesetze* (The Nuremberg Laws), which categorizes individuals into racial groups such as “Deutschblütiger,” “Mischling 2. Grades,” “Mischling 1. Grades,” and “Jude,” each marked with symbolic annotations — a legal framework that codified racial hierarchy and explicitly targeted Sinti and Roma alongside Jews [10]. Immediately following, black-and-white Gestapo mugshots appear, identifying Ludwig Horvath, born January 12, 1889, as a “Zigeuner,” and Helene Baranks Huber, born in 1874, as a “Zigeunerin” — visually documenting state surveillance and racial labeling [10][11]. These mugshots are presented in an archival style, emphasizing bureaucratic dehumanization [10].

At 00:22:30, the video shows a black-and-white mugshot of Maria Bihari, a Roma girl born November 9, 1935, presented in three angles — frontal, three-quarter, and profile — before transitioning to an outdoor Roma camp setting. The camp features wooden trailers, a central fire pit, gathered adults and children, and laundry hanging nearby. Horses and wagons are also shown, with people interacting with them, including two men guiding a horse — one holding a whip — illustrating the lived conditions of forced displacement and institutionalized segregation under Nazi rule [12][13]. The camp imagery is juxtaposed with the earlier Gestapo documentation, reinforcing the state’s control over Roma lives.

The video then documents the 1942 deportation to Auschwitz-Birkenau. At 00:23:20, a black-and-white scene shows prisoners — including women and children — walking along a barbed-wire fence, with the year “1942” superimposed and the location identified as “Auschwitz-Birkenau.” Containers labeled “GIFTGAS ZYKLON B” are shown, followed by piles of clothing and personal belongings — visually conveying the scale and brutality of the extermination process [14]. The footage is consistent with the earlier depiction of camp life and state mobilization, reinforcing the systematic nature of the genocide.

In a thematic transition, the video shifts to modern-day Bulgaria, where text overlays reference the “Process of Revival” (1984–1985), a state-sponsored assimilation policy that forced Gypsies to adopt Bulgarian names and relocate. Resistance led to family separation; by 1985, nearly all 400,000 Muslim Gypsies had assimilated [10]. The video overlays this historical policy with footage of rural Bulgaria — horse-drawn carts, mahalas, and grainy settlements — contrasting the state’s erasure of Gypsy identity with moments of cultural endurance, such as color footage of men with oxen carts and a violinist in an outdoor gathering [10]. This juxtaposition highlights the resilience of Roma culture despite state-imposed assimilation.

The video concludes this section with a powerful visual of a black-and-white historical photograph showing a group of men, women, and children sitting on the ground in a barren field, their worn clothing and exhausted expressions conveying despair. A man stands nearby near a simple fence, overseeing them — an image that encapsulates displacement, suffering, and the aftermath of historical atrocity [15]. The final frames juxtapose this with dark thematic transitions — hooded figures, Mengele’s image, and concentration camp aerials — evoking trauma and historical reckoning [15]. The video ends with a somber reflection on enduring suffering and loss, underscoring the continuity of systemic marginalization across regimes.

The video’s use of stark visual contrasts — from concentration camp imagery to modern-day protests — serves to illustrate how state-sanctioned violence, racial categorization, and forced assimilation have persisted across multiple regimes, leaving a legacy of trauma and resilience [16]. The evidence presented here confirms the institutionalized persecution of Roma under German and Eastern European regimes, documenting state-sponsored violence, bureaucratic racialization, and the enduring consequences of historical erasure.
```

## 8. References used by this section (global numbers)

```
[10] 00:22:00–00:22:10 · episodic 10sec: The video displays a historical Nazi-era document titled "Die Nürnberger Gesetze" (The Nuremberg Laws), which categorizes individuals based on racial and ethnic classifications, including "Deutschblütiger" (German-blo...
[11] Video-level knowledge (semantic memory, no timestamp): (Horvath, Ludwig Leitani, is a Zigeuner, born on January 12, 1889, and appears in Gestapo mugshots)
[12] 00:22:00–00:22:30 · episodic 30sec: **[Event 1: Display of Nazi Racial Classification Document]**  
The video opens with a historical document titled *Die Nürnberger Gesetze* (The Nuremberg Laws), which systematically categorizes individuals into racial...
[13] 00:22:10–00:22:20 · episodic 10sec: The video segment begins with a black-and-white mugshot of a young girl, Maria Bihari, born on November 9, 1935, identified as a Roma (Zigeunerin). The image shows three views of the girl: frontal, three-quarter, and...
[14] 00:23:20–00:23:30 · episodic 10sec: A black-and-white historical segment begins with a woman in a headscarf looking out from behind a wooden door. The scene transitions to a group of men in striped prison uniforms standing in formation, with the year "1...
[15] 00:23:30–00:24:00 · episodic 30sec: **[Event 1: Present-day outdoor communal gathering]**  
A group of people in heavy clothing and head coverings are gathered in a rugged, outdoor settlement, suggesting cold or harsh conditions. One bearded man in a ha...
[16] 00:20:00–00:30:00 · episodic 10min: **[Event 1: Historical Roots of Romani Persecution]**  
The video opens with archival imagery—black-and-white footage, 19th-century illustrations, and portraits of military figures—to establish centuries of institutio...
```
