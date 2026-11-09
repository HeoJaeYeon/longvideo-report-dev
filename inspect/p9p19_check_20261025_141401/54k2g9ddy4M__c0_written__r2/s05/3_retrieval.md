# Section 5 — retrieval results

## Requests (retrieval service log)

- text  request (2026-10-25 14:24:48): `{'video_id': '54k2g9ddy4M', 'mode': 'L1', 'queries': 3, 'episodic_candidates': 24, 'episodic_filter': 'llm', 'counts': {'episodic': 8, 'semantic': 4}, 'elapsed_sec': 6.49}`
- image request (2026-10-25 14:24:52): `{'video_id': '54k2g9ddy4M', 'mode': 'L1', 'queries': 1, 'counts': {'visual_clips': 3, 'frames': 3}, 'elapsed_sec': 1.34}`
- L1 filter LLM call: prompt 9837 tokens, output 77 tokens, 5.3 s (its input candidates and raw output are not logged)

## Text evidence (12 items, in the order the writer saw them as txt1..txt12)

| txt | cited | source | granularity | time | rank / score | uid |
|---|---|---|---|---|---|---|
| txt1 | ✓ | worldmm-episodic | 3min | 00:42:00–00:45:00 | 1 / 0.048916 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:3min_14` |
| txt2 | ✓ | worldmm-episodic | 30sec | 00:43:30–00:44:00 | 2 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_87` |
| txt3 |  | worldmm-episodic | 10sec | 00:44:30–00:44:40 | 3 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_267` |
| txt4 | ✓ | worldmm-episodic | 30sec | 00:44:30–00:45:00 | 4 / 0.015873 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_89` |
| txt5 | ✓ | worldmm-episodic | 10sec | 00:44:00–00:44:10 | 5 / 0.016129 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_264` |
| txt6 | ✓ | worldmm-episodic | 30sec | 00:42:30–00:43:00 | 6 / 0.032258 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:30sec_85` |
| txt7 | ✓ | worldmm-episodic | 10sec | 00:42:50–00:43:00 | 7 / 0.015873 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_257` |
| txt8 | ✓ | worldmm-episodic | 10sec | 00:43:30–00:43:40 | 8 / 0.016393 (rrf(order=llm_filter)) | `54k2g9ddy4M:episodic:10sec_261` |
| txt9 |  | worldmm-semantic | — | no timestamp | 1 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_603` |
| txt10 |  | worldmm-semantic | — | no timestamp | 2 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_650` |
| txt11 |  | worldmm-semantic | — | no timestamp | 3 / 0.016393 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_709` |
| txt12 | ✓ | worldmm-semantic | — | no timestamp | 4 / 0.016129 (rrf) | `54k2g9ddy4M:semantic:semantic_100451400_626` |

### Full text of each item (`content` field, exactly what the writer received)

**txt1** (cited)

```
[00:42:00-00:45:00 | episodic 3min] **[Event 1: Pet Psychic Trend Preview]**  
CBC News opens with visuals of dogs in varied settings — a chocolate Labrador, a shaggy brown dog in a purple harness, and a small dog in plaid pants retrieving a ball — intercut with a woman in a beanie and sunglasses. The narrative shifts to a residential street where dog owners enter a storefront labeled “Psychic Readings,” reinforcing the theme. Interior shots feature a woman in a yellow sweater giving an interview amid eclectic decor, accompanied by close-ups of a beagle and a gray cat. On-screen text repeatedly reads: “Coming soon | Demand for pet psychics is on the rise,” framing the phenomenon as a cultural trend under journalistic investigation.

**[Event 2: Goats Cross Residential Street]**  
The segment transitions to a title card for “The Breakdown,” followed by first-person footage of a large herd of goats crossing a road under overcast skies. A police officer walks along the sidewalk, observing the animals, while police car lights flash. The scene, credited to Arlington PD and broadcast by CBC News, captures the herd moving from pavement to grassy terrain and settling into grazing among trees. The incident, presented as an unusual and humorous urban wildlife event, is framed as a lighthearted but official police response.

**[Event 3: Studio Report with Anchor]**  
A CBC News anchor in a gray suit and patterned purple tie delivers a studio report, seated at a desk with black-and-white city skyline imagery on dual screens behind him. He speaks directly to the camera, using deliberate hand gestures — open-handed motions transitioning to clasped hands — to emphasize key points. The CBC News logo remains visible in the bottom right corner, reinforcing branding. No audio or transcript accompanies the footage, relying solely on visual delivery for information.
```

**txt2** (cited)

```
[00:43:30-00:44:00 | episodic 30sec] A herd of goats, mostly white and brown with some black markings, unexpectedly crosses a residential street in Arlington, Texas, prompting a police response. Captured from a moving camera perspective with flashing police lights visible, the scene unfolds under overcast skies and bare trees, indicating a cold or late-season setting. The footage, credited to Arlington PD and broadcast by CBC News, documents the moment the goats trigger a brief police chase as they move quickly across the road and into a wooded area. The camera follows the herd as they transition from pavement to grassy terrain, eventually settling into grazing among trees, suggesting the situation de-escalated as the animals dispersed. The incident, framed as an unusual and humorous urban wildlife event, is presented as a lighthearted but official police response.
```

**txt3**

```
[00:44:30-00:44:40 | episodic 10sec] A news anchor in a gray suit and purple tie stands in front of a backdrop featuring black-and-white images of city buildings. He speaks directly to the camera, using hand gestures for emphasis as he delivers his report. The CBC News logo is visible in the bottom right corner.
```

**txt4** (cited)

```
[00:44:30-00:45:00 | episodic 30sec] A CBC News anchor in a gray suit and patterned purple tie delivers a studio report, seated at a desk with black-and-white city skyline imagery displayed on two large screens behind him. He speaks directly to the camera, using deliberate hand gestures—beginning with open-handed motions and transitioning to clasped hands—to emphasize key points. The CBC News logo remains visible in the bottom right corner throughout the segment, reinforcing the broadcast’s branding. No audio or transcript accompanies the footage, leaving the visual delivery as the sole source of information.
```

**txt5** (cited)

```
[00:44:00-00:44:10 | episodic 10sec] The video begins with close-up shots of goats in a wooded area, one white goat standing alert while another with brown and white markings grazes. The scene then transitions to a wider view showing a large herd of goats crossing a street, with a police officer and a police vehicle nearby. The perspective shifts to what appears to be a bodycam or dashcam view, showing the herd moving along the road, with trees lining the street and a cloudy sky overhead. A person's hand is briefly visible in the foreground in one of the later frames.
```

**txt6** (cited)

```
[00:42:30-00:43:00 | episodic 30sec] A woman holds a small, fluffy dog, then the scene shifts to a black, shaggy dog being gently petted, before ending with a CBC News promotional graphic for “Pet psychics are on the rise,” featuring a beagle.

The same promotional graphic for “The National” on CBC News fades into a title card for “The Breakdown,” followed by first-person footage of a large herd of goats crossing a road, with a police car nearby.

A large herd of goats crosses a residential street from right to left under a cloudy sky, with bare trees and houses in the background; a police officer walks along the sidewalk observing them, and the police car’s lights flash in the final frame.
```

**txt7** (cited)

```
[00:42:50-00:43:00 | episodic 10sec] A large herd of goats is seen crossing a street, moving from right to left. A police vehicle is parked on the left side of the road, and a police officer walks along the sidewalk, observing the herd. The scene takes place on a cloudy day in a residential area with bare trees and houses in the background. The police car’s lights are flashing in the final frame.
```

**txt8** (cited)

```
[00:43:30-00:43:40 | episodic 10sec] A police car with flashing lights is seen driving down a residential street lined with bare trees and houses. The camera pans to reveal a large herd of goats crossing the road. Text on screen identifies the location as Arlington, Texas, and credits the footage to Arlington PD. The caption reads, "The Moment a herd of goats set off a police chase."
```

**txt9**

```
[video-level knowledge | semantic] (lower third graphic, mentions, pet psychics)
```

**txt10**

```
[video-level knowledge | semantic] (footage, shows, herd of goats crossing road)
```

**txt11**

```
[video-level knowledge | semantic] (news anchor, is in, studio)
```

**txt12** (cited)

```
[video-level knowledge | semantic] (segment, has on-screen text, Coming soon | Demand for pet psychics is on the rise)
```

## Image evidence (3 items, img1..img3)

| img | cited | frame | clip | uid | file |
|---|---|---|---|---|---|
| img1 |  | 00:41:35 | 00:41:30–00:41:40 | `54k2g9ddy4M:visual:00413000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00413000.jpg` |
| img2 |  | 00:42:05 | 00:42:00–00:42:10 | `54k2g9ddy4M:visual:00420000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00420000.jpg` |
| img3 |  | 00:41:45 | 00:41:40–00:41:50 | `54k2g9ddy4M:visual:00414000` | `outputs/p9p19_check_20261025_141401/frames_s0/54k2g9ddy4M/00414000.jpg` |

### Caption of each image (what the writer received instead of the picture)

**img1**

```
[00:41:30-00:41:40 | video frame at 2495.0s] A fluffy, light-brown dog with a pink flower on its back walks on green artificial turf, carrying a purple object in its mouth. The scene cuts to a close-up of a wrinkled pug’s face, looking upward. The video then transitions to a woman with dark hair, glasses, and a pink scarf speaking outdoors in a park setting. The final shot shows a black dog wearing a patterned bandana, sitting on the grass with a red leash. Throughout the segment, a lower third graphic reads, “Coming soon | Demand for pet psychics is on the rise.”
```

**img2**

```
[00:42:00-00:42:10 | video frame at 2525.0s] A close-up of a chocolate Labrador’s face is shown, followed by shots of a woman in a beanie and sunglasses speaking outdoors. The scene transitions to a person running across a grassy field with a small dog wearing a jacket and plaid pants, who then picks up a ball. The video cuts back to the woman, then to another dog with shaggy brown fur wearing a purple harness, looking directly at the camera. A lower third graphic reads, “Coming soon | Demand for pet psychics is on the rise,” with the CBC News logo.
```

**img3**

```
[00:41:40-00:41:50 | video frame at 2505.0s] A black dog with a white muzzle and a patterned bandana sits on artificial turf, looking at the camera. The scene cuts to a woman in a blue jacket and pink scarf interacting with the dog, who raises a paw as if to shake hands. The video then shows close-ups of the dog's face before shifting to a man in a grey beanie with "PAC" on it, who appears to be speaking in an outdoor park setting. A lower third graphic reads, "Coming soon | Demand for pet psychics is on the rise" with the CBC News logo.
```
