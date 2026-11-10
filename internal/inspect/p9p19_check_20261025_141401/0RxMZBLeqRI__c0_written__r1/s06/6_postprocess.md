# Section 6 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 294 words → after removal 294 words

## 2. Start/end claim check (`boundary_claims`)

- ending_unverifiable: The video concludes not with a resolution but with a global perspective, transitioning to a stylized globe rotating against a backdrop of international flags, before fading to black — a visual that frames Roma experiences as part of a broader, interconnected global narrative [citation:img1][citation (cited [])

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 8, "cited_sentences": 4, "checked_tokens": 5, "unsupported": 1, "miscited": 0, "uncited_claims": 0, "absence_statements": 0}`

- **unsupported** quote `-marked scientist and the` cited ['txt4', 'txt5'] — From its opening disclaimer affirming the non-slandrous use of “Gypsy,” the video frames Roma identity as both deeply rooted in Balkan history — evidenced by sepia-toned photographs of families in traditional attire and modern parades featuring Roma flags alongside EU and Ukrainian banners — and per

## 4. Citation conversion stats

- `{"text_citations": 7, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 0, "wrong_form_image_citations": 2, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 7 of 12

## 5. Image-text time alignment

- img1 frame 00:30:25: gap to text cited in the same paragraph 25.0 s (ranges ['00:27:00-00:30:00', '00:00:00-00:00:30', '00:00:00-00:03:00', '00:06:00-00:09:00']), to any text cited in the section 25.0 s
- img2 frame 00:30:31: gap to text cited in the same paragraph 31.0 s (ranges ['00:27:00-00:30:00', '00:00:00-00:00:30', '00:00:00-00:03:00', '00:06:00-00:09:00']), to any text cited in the section 31.0 s

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Conclusion

The video portrays the Roma as a people marked by historical marginalization, yet enduring through systemic persecution with remarkable cultural resilience. From its opening disclaimer affirming the non-slandrous use of “Gypsy,” the video frames Roma identity as both deeply rooted in Balkan history — evidenced by sepia-toned photographs of families in traditional attire and modern parades featuring Roma flags alongside EU and Ukrainian banners — and persistently misunderstood, as shown by recurring visual motifs of exclusion, such as the “X”-marked scientist and the “UNWANTED” overlay on historical scenes [citation:txt4][citation:txt5]. The narrative traces their origins from South Asia through the Ghaznavid Empire and into Byzantine territories, where they were misidentified as Seljuk Turks, embedding their identity within geopolitical conflict [citation:txt8]. This historical misclassification and subsequent institutionalization under Nazi and communist regimes — though the latter is only referenced via a title card — are depicted as tools of erasure, with archival visuals of Gestapo mugshots and bureaucratic “Zigeuner” labels reinforcing state-sanctioned persecution [citation:txt5][citation:txt5]. Despite this, the video highlights moments of quiet resistance: a Roma woman asserting “I am also a Roma” at a rally, a dancing boy in front of a satellite-dish-covered building, and an animated character symbolizing cultural endurance — all underscoring resilience amid systemic oppression [citation:txt3]. The video concludes not with a resolution but with a global perspective, transitioning to a stylized globe rotating against a backdrop of international flags, before fading to black — a visual that frames Roma experiences as part of a broader, interconnected global narrative [citation:img1][citation:img2]. Credits appear at 00:30:08, marking the formal end of the video’s content [citation:txt11]. This final sequence confirms the video’s focus on Roma identity, historical marginalization, systemic persecution, and cultural resilience — all synthesized through layered visuals, historical context, and symbolic imagery.
```

## 7. Grounded body (exactly as in report.md)

```
# Conclusion

The video portrays the Roma as a people marked by historical marginalization, yet enduring through systemic persecution with remarkable cultural resilience. From its opening disclaimer affirming the non-slandrous use of “Gypsy,” the video frames Roma identity as both deeply rooted in Balkan history — evidenced by sepia-toned photographs of families in traditional attire and modern parades featuring Roma flags alongside EU and Ukrainian banners — and persistently misunderstood, as shown by recurring visual motifs of exclusion, such as the “X”-marked scientist and the “UNWANTED” overlay on historical scenes [1][3]. The narrative traces their origins from South Asia through the Ghaznavid Empire and into Byzantine territories, where they were misidentified as Seljuk Turks, embedding their identity within geopolitical conflict [20]. This historical misclassification and subsequent institutionalization under Nazi and communist regimes — though the latter is only referenced via a title card — are depicted as tools of erasure, with archival visuals of Gestapo mugshots and bureaucratic “Zigeuner” labels reinforcing state-sanctioned persecution [3][3]. Despite this, the video highlights moments of quiet resistance: a Roma woman asserting “I am also a Roma” at a rally, a dancing boy in front of a satellite-dish-covered building, and an animated character symbolizing cultural endurance — all underscoring resilience amid systemic oppression [21]. The video concludes not with a resolution but with a global perspective, transitioning to a stylized globe rotating against a backdrop of international flags, before fading to black — a visual that frames Roma experiences as part of a broader, interconnected global narrative (Figure 6) (Figure 7). Credits appear at 00:30:08, marking the formal end of the video’s content [22]. This final sequence confirms the video’s focus on Roma identity, historical marginalization, systemic persecution, and cultural resilience — all synthesized through layered visuals, historical context, and symbolic imagery.

![Figure 6 (00:30:25)](frames/0RxMZBLeqRI_00302000.jpg)

*Figure 6. Frame at 00:30:25 (clip 00:30:20–00:30:30). A stylized globe rotates slowly against a background displaying numerous national flags. The globe begins facing Asia and gradually rotates to show Africa, then the Americas, before returning to focus on Europe and Asia again. No audio is present.*

![Figure 7 (00:30:31)](frames/0RxMZBLeqRI_00303000.jpg)

*Figure 7. Frame at 00:30:31 (clip 00:30:30–00:30:32). The screen displays a grid of various national flags surrounding a central, stylized globe showing the continents of Asia and Australia. The scene then abruptly transitions to complete blackness.*
```

## 8. References used by this section (global numbers)

```
[1] 00:00:00–00:00:30 · episodic 30sec: **[Event 1: Introduction and Context Setting]**  
The video opens with a disclaimer clarifying that “Gypsy” will be used interchangeably with “Roma” and “Romani” to refer to an ethnic group, acknowledging the term’s c...
[3] 00:00:00–00:03:00 · episodic 3min: **[Event 1: Introduction and Context Setting]**  
The video opens with a disclaimer clarifying the use of “Gypsy” as a non-slandrous term for Roma/Romani, followed by a map of the Balkans and a montage of memes and hi...
[20] 00:06:00–00:09:00 · episodic 3min: **[Event 1: Ghaznavid Empire’s Rise and Expansion]**  
The video opens with a symbolic map of South Asia, silhouetted figures in turbans marking regional influence, narrowing to the Ghaznavid Empire’s territory across...
[21] 00:27:00–00:30:00 · episodic 3min: **[Event 1: Marginalized Lives and Systemic Struggle]**  
The video opens with rural and urban scenes of poverty — children in dilapidated settings, a man shoveling dirt, and a woman sorting documents — juxtaposed wit...
[22] Video-level knowledge (semantic memory, no timestamp): (credits, appear at time, 00:30:08)
```
