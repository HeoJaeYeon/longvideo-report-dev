# Section 3 — post-processing

## 1. Repeated-sentence removal (`dedupe_repeated_sentences`)

- removed sentences: 0, a sentence occurred up to 1 times, ends mid-sentence: False
- raw writer output 529 words → after removal 529 words

## 2. Start/end claim check (`boundary_claims`)

- none

## 3. Rule-based evidence check (`check_section_grounding`)

- stats: `{"sentences": 19, "cited_sentences": 3, "checked_tokens": 3, "unsupported": 0, "miscited": 0, "uncited_claims": 2, "absence_statements": 0}`

- **uncited**  `['00:00:30']` cited [] — At 00:00:30, the video presents a man in a yellow lab coat carefully transferring liquid with a pipette, symbolizing scientific precision or experimentation.
- **uncited**  `['danger', 'criminality']` cited [] — These fantasy scenes serve as allegory for how Roma are often reduced to archetypes of “danger” or “criminality,” despite their rich cultural contributions.

## 4. Citation conversion stats

- `{"text_citations": 13, "invalid_citations": 0, "malformed_tokens": 0, "image_embeds": 2, "wrong_form_image_citations": 0, "duplicate_image_embeds": 0}`
- text evidence not cited in this section: 8 of 12

## 5. Image-text time alignment

- img2 frame 00:01:45: gap to text cited in the same paragraph 0.0 s (ranges ['00:00:30-00:01:00', '00:00:50-00:01:00', '00:00:30-00:00:40', '00:00:00-00:10:00']), to any text cited in the section 0.0 s
- img3 frame 00:01:55: gap to text cited in the same paragraph 0.0 s (ranges ['00:00:30-00:01:00', '00:00:50-00:01:00', '00:00:30-00:00:40', '00:00:00-00:10:00']), to any text cited in the section 0.0 s

## 6. Section body after removal (input to the conversion, still with txtN/imgN)

```
# Depiction of Roma as Historically Misclassified and Systematically Stigmatized

At 00:00:30, the video presents a man in a yellow lab coat carefully transferring liquid with a pipette, symbolizing scientific precision or experimentation. This image is immediately followed by a black-and-white depiction of a man in a lab coat marked with a large red “X,” suggesting exclusion from scientific or societal norms [citation:txt3]. The juxtaposition of these two figures—scientifically engaged yet rejected—visually critiques how Roma have been subjected to exclusionary frameworks even within academic and institutional domains. The scene then transitions to cultural imagery: a man in a red sweater gesturing before a group in traditional clothing, some dancing, followed by black-and-white photos of a band playing traditional instruments and a family with children holding instruments seated before a wagon, evoking heritage and communal life [citation:txt3]. These images culminate in the word “UNWANTED” superimposed over historical scenes, accompanied by a voiceover explaining how the vast majority of Roma have been historically stigmatized and labeled as unwanted nuisances [citation:txt1]. This visual and auditory combination underscores the systemic erasure and dehumanization embedded in historical narratives.

The video then transitions to a Minecraft gameplay scene where a player mines, symbolizing labor or resource extraction [citation:txt2]. This is followed by a cut to a menacing, horned humanoid character declaring “Your money or your life,” evoking themes of coercion or economic exploitation [citation:txt2]. The tone shifts to a dark fantasy setting with robed figures in combat, followed by a surreal image of a black, hooded figure with glowing dollar signs, suggesting corruption or the commodification of power [citation:txt2]. These fantasy scenes serve as allegory for how Roma are often reduced to archetypes of “danger” or “criminality,” despite their rich cultural contributions. The video contrasts this with vibrant dance performances—on stage and in public squares—representing joy, freedom, or resistance [citation:txt2]. The segment concludes with a somber black-and-white photograph of displaced people sitting on the ground, underscoring suffering and loss [citation:txt2]. Throughout, the voiceover traces the tragic history behind stereotypes of thieves and black magic casters, framing them as products of societal fear and misunderstanding [citation:txt2]. This sequence effectively links Roma identity to geopolitical misreading and societal fear, using satirical fantasy and cultural imagery to critique how they are reduced to stereotypes.

The video’s depiction of scientific exclusion is further reinforced by the lab-coated figure and the red “X”-marked scientist, symbolizing how Roma have been systematically excluded from scholarly and institutional frameworks [citation:txt3]. The “UNWANTED” text superimposed over historical scenes directly references the video’s central argument: that Roma have been historically misclassified and stigmatized, not as a result of inherent traits, but as a product of societal fear and geopolitical misreading [citation:txt1]. The transition from Minecraft mining to fantasy combat and back to dance and displacement illustrates the video’s thematic arc: from labor and exploitation to cultural resistance and enduring suffering [citation:txt2]. The use of fantasy and game-based visuals, juxtaposed with historical and cultural imagery, serves to highlight the absurdity and harm of reducing Roma identity to simplistic, often violent, stereotypes [citation:txt5]. This section thus critiques how Roma are not only misclassified but also rendered invisible, feared, and commodified within historical and contemporary narratives.

![](citation:img2)  
![](citation:img3)
```

## 7. Grounded body (exactly as in report.md)

```
# Depiction of Roma as Historically Misclassified and Systematically Stigmatized

At 00:00:30, the video presents a man in a yellow lab coat carefully transferring liquid with a pipette, symbolizing scientific precision or experimentation. This image is immediately followed by a black-and-white depiction of a man in a lab coat marked with a large red “X,” suggesting exclusion from scientific or societal norms [6]. The juxtaposition of these two figures—scientifically engaged yet rejected—visually critiques how Roma have been subjected to exclusionary frameworks even within academic and institutional domains. The scene then transitions to cultural imagery: a man in a red sweater gesturing before a group in traditional clothing, some dancing, followed by black-and-white photos of a band playing traditional instruments and a family with children holding instruments seated before a wagon, evoking heritage and communal life [6]. These images culminate in the word “UNWANTED” superimposed over historical scenes, accompanied by a voiceover explaining how the vast majority of Roma have been historically stigmatized and labeled as unwanted nuisances [7]. This visual and auditory combination underscores the systemic erasure and dehumanization embedded in historical narratives.

The video then transitions to a Minecraft gameplay scene where a player mines, symbolizing labor or resource extraction [8]. This is followed by a cut to a menacing, horned humanoid character declaring “Your money or your life,” evoking themes of coercion or economic exploitation [8]. The tone shifts to a dark fantasy setting with robed figures in combat, followed by a surreal image of a black, hooded figure with glowing dollar signs, suggesting corruption or the commodification of power [8]. These fantasy scenes serve as allegory for how Roma are often reduced to archetypes of “danger” or “criminality,” despite their rich cultural contributions. The video contrasts this with vibrant dance performances—on stage and in public squares—representing joy, freedom, or resistance [8]. The segment concludes with a somber black-and-white photograph of displaced people sitting on the ground, underscoring suffering and loss [8]. Throughout, the voiceover traces the tragic history behind stereotypes of thieves and black magic casters, framing them as products of societal fear and misunderstanding [8]. This sequence effectively links Roma identity to geopolitical misreading and societal fear, using satirical fantasy and cultural imagery to critique how they are reduced to stereotypes.

The video’s depiction of scientific exclusion is further reinforced by the lab-coated figure and the red “X”-marked scientist, symbolizing how Roma have been systematically excluded from scholarly and institutional frameworks [6]. The “UNWANTED” text superimposed over historical scenes directly references the video’s central argument: that Roma have been historically misclassified and stigmatized, not as a result of inherent traits, but as a product of societal fear and geopolitical misreading [7]. The transition from Minecraft mining to fantasy combat and back to dance and displacement illustrates the video’s thematic arc: from labor and exploitation to cultural resistance and enduring suffering [8]. The use of fantasy and game-based visuals, juxtaposed with historical and cultural imagery, serves to highlight the absurdity and harm of reducing Roma identity to simplistic, often violent, stereotypes [4]. This section thus critiques how Roma are not only misclassified but also rendered invisible, feared, and commodified within historical and contemporary narratives.

![Figure 3 (00:01:45)](frames/0RxMZBLeqRI_00014000.jpg)

*Figure 3. Frame at 00:01:45 (clip 00:01:40–00:01:50). Two men in blue shirts are shown seated at a laptop, with national flags superimposed on their chests. One man gestures emphatically while speaking, and the other listens. The scene transitions to a cartoon depiction of a man with a Greek flag on his shirt, screaming with an angry expression agai...*

![Figure 4 (00:01:55)](frames/0RxMZBLeqRI_00015000.jpg)

*Figure 4. Frame at 00:01:55 (clip 00:01:50–00:02:00). The video begins with a historical painting depicting a chaotic battle scene featuring Crusaders and local figures, followed by a transition to a blurred background with the Google Translate logo. The text "DON'T TOUCH" appears prominently. The scene then shifts to a close-up of a man with a bear...*
```

## 8. References used by this section (global numbers)

```
[4] 00:00:00–00:10:00 · episodic 10min: **[Event 1: Introduction and Context Setting]**  
The video opens with a disclaimer clarifying the use of “Gypsy” as a non-slandrous term for Roma/Romani, followed by a map of the Balkans and a montage of memes and hi...
[6] 00:00:30–00:00:40 · episodic 10sec: A man in a yellow lab coat carefully uses a pipette to transfer liquid into a beaker. The scene then transitions to a black-and-white image of a man in a lab coat, marked with a large red "X". Next, a man in a red swe...
[7] 00:00:30–00:01:00 · episodic 30sec: **[Event 1: Scientific Experimentation and Historical Stigmatization]**  
A man in a yellow lab coat carefully transfers liquid using a pipette, symbolizing scientific precision or experimentation. The scene abruptly...
[8] 00:00:50–00:01:00 · episodic 10sec: The video transitions through various scenes: it begins with a Minecraft gameplay shot showing a player mining, then cuts to a close-up of a menacing, horned humanoid character from a video game declaring, "Your money...
```
