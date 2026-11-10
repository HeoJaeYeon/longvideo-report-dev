# -QuCz7kxBr8__c0_written__r2 — intermediate outputs

- Run `outputs/p9p19_check_20261025_141401`, stack 3 (GPU 7), session `report_-QuCz7kxBr8_1792937702_b3a13102` 2026-10-25T14:15:02 – 2026-10-25T14:19:59 (UTC)
- Query: Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.
- Checklist: []
- validation: passed, generation 296.9 s
- report.md reproduced from report.json by re-running ground_report: True

## Files

- `01_planner_prompt.md`, `02_planner_output.md`
- `sNN/1_query_prompt.md` … `sNN/6_postprocess.md` (see the table)

| section | description | text / image queries | text / image evidence | cited text / image | writer output tokens | folder |
|---|---|---|---|---|---|---|
| 1 | This section introduces the six main participants—Chris, Zach, Cass, James, Mitc… | 3 / 1 | 12 / 3 | 6 / 3 | 715 (stop) | `s01/` |
| 2 | This section covers the first gadget test, the ‘SPORTS DRIBBLE SPECS,’ including… | 3 / 1 | 12 / 3 | 7 / 0 | 491 (stop) | `s02/` |
| 3 | This section details the SKLZ Dribble Stick test, including its rules (dribble w… | 3 / 1 | 12 / 3 | 7 / 0 | 1015 (stop) | `s03/` |
| 4 | This section focuses on the ‘Straight Shooter Strap’ test, including its demonst… | 3 / 1 | 12 / 3 | 9 / 0 | 678 (stop) | `s04/` |
| 5 | This section covers the Flick Glove challenge, including its rules (three shots … | 3 / 1 | 12 / 3 | 10 / 0 | 848 (stop) | `s05/` |
| 6 | Conclusion: This section briefly summarizes the main results shown in the video … | 3 / 1 | 12 / 3 | 4 / 0 | 326 (stop) | `s06/` |

## LLM calls (LLM server log, in call order)

| call | section | prompt tokens | output tokens | finish | seconds |
|---|---|---|---|---|---|
| planner | — | 5219 | 737 | stop | 33.8 |
| query | 1 | 435 | 92 | stop | 4.2 |
| L1 filter (in search) | 1 | 8090 | 65 | stop | 4.3 |
| writer | 1 | 3813 | 715 | stop | 32.7 |
| query | 2 | 603 | 91 | stop | 4.1 |
| L1 filter (in search) | 2 | 7550 | 68 | stop | 4.4 |
| writer | 2 | 3728 | 491 | stop | 23.4 |
| query | 3 | 698 | 107 | stop | 4.8 |
| L1 filter (in search) | 3 | 7287 | 67 | stop | 4.1 |
| writer | 3 | 3845 | 1015 | stop | 47.0 |
| query | 4 | 855 | 86 | stop | 3.9 |
| L1 filter (in search) | 4 | 9907 | 69 | stop | 5.0 |
| writer | 4 | 4320 | 678 | stop | 30.5 |
| query | 5 | 971 | 94 | stop | 4.3 |
| L1 filter (in search) | 5 | 9001 | 71 | stop | 4.7 |
| writer | 5 | 5969 | 848 | stop | 37.1 |
| query | 6 | 1066 | 66 | stop | 3.1 |
| L1 filter (in search) | 6 | 8637 | 68 | stop | 4.5 |
| writer | 6 | 6424 | 326 | stop | 15.1 |

## Validation warnings

- 2 image citation(s) written as [citation:imgN] were converted to figures
- rule-based evidence check: 1 unsupported (see validation.json grounding_findings)
- rule-based evidence check: 1 miscited (see validation.json grounding_findings)
- rule-based evidence check: 3 uncited_claims (see validation.json grounding_findings)
- section 3: removed 10 repeated sentence(s), a sentence occurred up to 3 times (writer repetition loop suspected)
- video start/end claim check: 2 ending_unverifiable (see validation.json boundary_findings)
