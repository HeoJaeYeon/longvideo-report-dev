# -QuCz7kxBr8__c0_written__r3 — intermediate outputs

- Run `outputs/p9p19_check_20261025_141401`, stack 2 (GPU 6), session `report_-QuCz7kxBr8_1792938051_b2419ba8` 2026-10-25T14:20:51 – 2026-10-25T14:26:22 (UTC)
- Query: Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.
- Checklist: []
- validation: passed, generation 331.5 s
- report.md reproduced from report.json by re-running ground_report: True

## Files

- `01_planner_prompt.md`, `02_planner_output.md`
- `sNN/1_query_prompt.md` … `sNN/6_postprocess.md` (see the table)

| section | description | text / image queries | text / image evidence | cited text / image | writer output tokens | folder |
|---|---|---|---|---|---|---|
| 1 | This section introduces the six main participants—Chris, Zach, Cass, James, Mitc… | 3 / 1 | 12 / 3 | 7 / 1 | 598 (stop) | `s01/` |
| 2 | This section covers the first gadget tested: the SPORTS DRIBBLE SPECS, including… | 2 / 1 | 12 / 3 | 7 / 0 | 767 (stop) | `s02/` |
| 3 | This section details the testing of the Straight Shooter Strap and the Flick Glo… | 3 / 1 | 12 / 3 | 6 / 3 | 745 (stop) | `s03/` |
| 4 | This section covers the synchronized shooting challenge using the Shot Coach dev… | 3 / 1 | 12 / 3 | 6 / 0 | 1193 (stop) | `s04/` |
| 5 | This section focuses on the Never Ending Defender training device and the final … | 3 / 1 | 12 / 3 | 5 / 0 | 1156 (stop) | `s05/` |
| 6 | Conclusion: This section briefly summarizes the main results shown in the video … | 3 / 1 | 12 / 3 | 4 / 0 | 288 (stop) | `s06/` |

## LLM calls (LLM server log, in call order)

| call | section | prompt tokens | output tokens | finish | seconds |
|---|---|---|---|---|---|
| planner | — | 5219 | 816 | stop | 37.7 |
| query | 1 | 446 | 78 | stop | 3.5 |
| L1 filter (in search) | 1 | 9308 | 71 | stop | 4.8 |
| writer | 1 | 3540 | 598 | stop | 27.1 |
| query | 2 | 608 | 83 | stop | 3.9 |
| L1 filter (in search) | 2 | 7375 | 70 | stop | 4.3 |
| writer | 2 | 3771 | 767 | stop | 34.5 |
| query | 3 | 765 | 83 | stop | 4.0 |
| L1 filter (in search) | 3 | 7528 | 71 | stop | 4.4 |
| writer | 3 | 4124 | 745 | stop | 34.4 |
| query | 4 | 879 | 85 | stop | 3.8 |
| L1 filter (in search) | 4 | 8105 | 73 | stop | 4.9 |
| writer | 4 | 5375 | 1193 | stop | 52.6 |
| query | 5 | 1049 | 79 | stop | 3.6 |
| L1 filter (in search) | 5 | 11237 | 71 | stop | 5.5 |
| writer | 5 | 5434 | 1156 | stop | 51.4 |
| query | 6 | 1167 | 77 | stop | 3.6 |
| L1 filter (in search) | 6 | 12347 | 69 | stop | 5.6 |
| writer | 6 | 5536 | 288 | stop | 13.8 |

## Validation warnings

- rule-based evidence check: 1 unsupported (see validation.json grounding_findings)
- rule-based evidence check: 2 miscited (see validation.json grounding_findings)
- rule-based evidence check: 7 uncited_claims (see validation.json grounding_findings)
- video start/end claim check: 4 ending_early, 1 ending_unverifiable (see validation.json boundary_findings)
