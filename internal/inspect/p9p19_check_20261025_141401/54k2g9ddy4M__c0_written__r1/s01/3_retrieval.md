# Section 1 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:15:59): `{'video_id': '54k2g9ddy4M', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 18, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 9.87}`
- image request (2026-10-25 14:16:02): `{'video_id': '54k2g9ddy4M', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 1.5}`
- L1 filter LLM call: prompt 6205 tokens, output 69 tokens, 4.1 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 30sec | 00:02:00–00:02:30 | 1 / 0.048395 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_4` |
| txt2 | ✓ | worldmm-episodic | 10sec | 00:02:20–00:02:30 | 2 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_14` |
| txt3 | ✓ | worldmm-episodic | 10sec | 00:02:00–00:02:10 | 3 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_12` |
| txt4 | ✓ | worldmm-episodic | 30sec | 00:00:30–00:01:00 | 4 / 0.032787 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_1` |
| txt5 | ✓ | worldmm-episodic | 30sec | 00:01:30–00:02:00 | 5 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_3` |
| txt6 | ✓ | worldmm-episodic | 10sec | 00:02:40–00:02:50 | 6 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_16` |
| txt7 |  | worldmm-episodic | 10sec | 00:01:10–00:01:20 | 7 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_7` |
| txt8 |  | worldmm-episodic | 30sec | 00:04:00–00:04:30 | 8 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_8` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.031778 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_31` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.031498 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_29` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_40` |
| txt12 |  | worldmm-semantic | — | no timestamp | 4 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_10` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:02:00-00:02:30 | episodic 30sec] Measles is resurging in Canadian communities, prompting public health officials to investigate potential cases and trace transmission chains, as the virus—highly contagious and airborne—can linger in hospitals and waiting rooms, exposing new individuals. Dr. Earl Rubin from Montreal Children’s Hospital questions the outbreak’s origin and potential spread, while Dr. Anna Banerji, a pediatric infectious diseases specialist in Parry Sound, Ontario, explains the virus’s environmental persistence and the importance of vaccination. Footage shows healthcare workers administering the measles-mumps-rubella (MMR) vaccine and close-ups of measles rash, underscoring prevention efforts. Canada officially eliminated measles in 1998, but declining vaccination rates have contributed to its return.
```

**txt2** (cited)

```
[00:02:20-00:02:30 | episodic 10sec] Dr. Anna Banerji, a pediatric infectious diseases specialist, discusses how measles virus can linger in the air in hospital or waiting room environments, potentially exposing new individuals. The segment transitions to footage of a healthcare worker administering a vaccine to a patient, illustrating efforts to combat the disease. The on-screen text notes that Canada eliminated measles in 1998 but vaccination rates have since declined.
```

**txt3** (cited)

```
[00:02:00-00:02:10 | episodic 10sec] Dr. Earl Rubin from Montreal Children’s Hospital discusses the measles outbreak, questioning the origin of the virus and who else it may be spreading to. The segment cuts to a hospital scene where a medical professional in scrubs reviews paperwork near a patient cart. A news ticker at the bottom reads, “Officials say measles may be spreading in Canadian communities.”
```

**txt4** (cited)

```
[00:00:30-00:01:00 | episodic 30sec] Joshua Liendo, a Canadian swimmer, competes in a swimming race, showcasing his butterfly stroke technique across lanes, before transitioning to interview segments where he reflects on his journey as a trailblazer for Black swimmers and expresses the surreal nature of his rise to prominence. The footage captures his preparation, intense racing, and post-race moments poolside and in the water wearing a Canadian swim cap, all underscored by commentary highlighting his potential Olympic impact. The segment concludes with a cut to CBC News’ “The National,” hosted by Ian Henneman, where a female anchor delivers a report on the resurgence of measles in Canadian communities, supported by on-screen medical graphics including virus particles and vaccine vials.
```

**txt5** (cited)

```
[00:01:30-00:02:00 | episodic 30sec] A man in a black jacket and beanie gently swings a small child in a pink snowsuit at a Toronto playground, while a news ticker warns that measles may be spreading in Canadian communities — juxtaposing everyday family life with public health concern.

The scene shifts to Benjamin Dermer, a bearded parent in a beanie, speaking outdoors near bare trees, followed by shots of crowded streets in Montreal and a stadium crowd, all under the same warning ticker, as fragmented audio conveys public anxiety and uncertainty about the measles outbreak.

The video then cuts to outdoor ice skating and a close-up of Dr. Earl Rubin from Montreal Children’s Hospital, who addresses the camera, stating that the measles situation reflects only the tip of the iceberg and questions the origin of the outbreak — underscoring the scale and mystery of the spread.
```

**txt6** (cited)

```
[00:02:40-00:02:50 | episodic 10sec] A graphic displays a vial of the Priorix MMR vaccine alongside text stating that 95% of the population needs to be vaccinated to maintain herd immunity, citing the WHO. The scene then transitions to Dr. Christopher Labos, an epidemiologist in Montreal, speaking to the camera. He gestures as he explains that if community spread of measles begins, more cases will follow. A news ticker at the bottom reads, “Officials say measles may be spreading in Canadian communities.”
```

**txt7**

```
[00:01:10-00:01:20 | episodic 10sec] A news segment from CBC News discusses measles infections in Canada, showing a graphic of a map with two marked locations — one in Quebec and one in Ontario — indicating cases that are not linked to travel or other known cases. The on-screen text states "At least 13 infections" and "Officials say measles may be spreading in Canadian communities." The segment transitions to a news anchor speaking, with the same lower-third text visible, as he explains that doctors believe a massive outbreak is unlikely.
```

**txt8**

```
[00:04:00-00:04:30 | episodic 30sec] **Measles Vaccination Guidance and Outbreak Alert**  
A CBC News segment features a female anchor in a white top discussing measles vaccinations, noting that children can receive the shot as early as nine months and that schedules may be adjusted for higher-risk individuals. The on-screen graphic warns that “Officials say measles may be spreading in Canadian communities.” The segment transitions to a split-screen, where a male anchor in a suit listens as reporter Katie Nicholson, based in Toronto, elaborates on outbreak precautions, advising viewers to avoid locations with known measles cases. The segment concludes with Nicholson’s full-screen appearance as the anchor’s side fades.

**Quebec Hospital Waiting Room Death Under Coroner’s Review**  
A male news anchor in a suit and tie delivers a report against a cityscape backdrop, detailing a Quebec coroner’s investigation into the death of a patient who waited 45 minutes for an ambulance in a Montreal hospital. A lower-third graphic identifies the case as “Coroner investigating 3rd death in Quebec hospital waiting room,” highlighting ongoing scrutiny of emergency response protocols in the province.
```

**txt9**

```
[video-level knowledge | semantic] (Dr. Christopher Labos, warns of, potential hospitalizations)
```

**txt10**

```
[video-level knowledge | semantic] (Dr. Christopher Labos, discusses, risks of community spread of measles)
```

**txt11**

```
[video-level knowledge | semantic] (measles virus, can linger in, waiting room)
```

**txt12**

```
[video-level knowledge | semantic] (graphic, displays text, New measles infect)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:23:25 | 00:23:20–00:23:30 | `54k2g9ddy4M:visual:00232000` | `outputs/p9p19_check_20261025_141401/frames_s2/54k2g9ddy4M/00232000.jpg` |
| img2 |  | 00:20:05 | 00:20:00–00:20:10 | `54k2g9ddy4M:visual:00200000` | `outputs/p9p19_check_20261025_141401/frames_s2/54k2g9ddy4M/00200000.jpg` |
| img3 | ✓ | 00:04:25 | 00:04:20–00:04:30 | `54k2g9ddy4M:visual:00042000` | `outputs/p9p19_check_20261025_141401/frames_s2/54k2g9ddy4M/00042000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:23:20-00:23:30 | video frame at 1405.0s] A news anchor in a suit and tie speaks to the camera in a studio, with a graphic overlay reading "Why self-tapes are becoming more common for film & TV auditions." Behind him, a screen displays a man smiling while recording himself with a smartphone mounted on a ring light.
```

**img2**

```
[00:20:00-00:20:10 | video frame at 1205.0s] A news anchor in a suit and tie speaks in a studio, with a graphic of an "Emergency Urgent Care" building behind him. A lower third reads, "Family mourns son's death before realizing it was a stranger," and the CBC News logo is visible in the corner.
```

**img3** (cited)

```
[00:04:20-00:04:30 | video frame at 265.0s] A news anchor in a suit and tie speaks on a television set with a cityscape backdrop, delivering a report about a Quebec coroner’s investigation into a patient’s death after waiting 45 minutes for an ambulance in a Montreal hospital. A lower-third graphic reads, “Coroner investigating 3rd death in Quebec hospital waiting room.”
```
