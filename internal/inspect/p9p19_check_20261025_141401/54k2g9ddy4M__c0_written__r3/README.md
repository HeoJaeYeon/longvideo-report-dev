# 54k2g9ddy4M__c0_written__r3 — intermediate outputs

- Run `outputs/p9p19_check_20261025_141401`, stack 0 (GPU 4), session `report_54k2g9ddy4M_1792938362_9546cde4` 2026-10-25T14:26:02 – 2026-10-25T14:32:04 (UTC)
- Query: Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.
- Checklist: []
- validation: passed, generation 361.7 s
- report.md reproduced from report.json by re-running ground_report: True

## Files

- `01_planner_prompt.md`, `02_planner_output.md`
- `sNN/1_query_prompt.md` … `sNN/6_postprocess.md` (see the table)

| section | description | text / image queries | text / image evidence | cited text / image | writer output tokens | folder |
|---|---|---|---|---|---|---|
| 1 | This section covers the opening of the video (00:00:00-00:10:00), which introduc… | 3 / 1 | 12 / 3 | 10 / 3 | 1709 (stop) | `s01/` |
| 2 | This section details the unfolding of the measles outbreak and its consequences … | 3 / 1 | 12 / 3 | 6 / 3 | 1156 (stop) | `s02/` |
| 3 | This section focuses on the misidentification tragedy at Montfort Hospital (00:2… | 3 / 1 | 12 / 3 | 9 / 3 | 810 (stop) | `s03/` |
| 4 | This section details Joshua Liendo’s personal journey and legacy (00:30:00-00:40… | 3 / 1 | 12 / 3 | 7 / 1 | 651 (stop) | `s04/` |
| 5 | This section covers the aftermath of a devastating fire that destroyed the only … | 3 / 1 | 12 / 3 | 7 / 0 | 1053 (stop) | `s05/` |
| 6 | Conclusion: This section briefly summarizes the main results shown in the video … | 3 / 1 | 12 / 3 | 7 / 0 | 306 (stop) | `s06/` |

## LLM calls (LLM server log, in call order)

| call | section | prompt tokens | output tokens | finish | seconds |
|---|---|---|---|---|---|
| planner | — | 6271 | 907 | stop | 39.5 |
| query | 1 | 460 | 77 | stop | 3.4 |
| L1 filter (in search) | 1 | 8269 | 68 | stop | 4.6 |
| writer | 1 | 5032 | 1709 | stop | 72.0 |
| query | 2 | 595 | 75 | stop | 3.2 |
| L1 filter (in search) | 2 | 9235 | 67 | stop | 4.6 |
| writer | 2 | 4993 | 1156 | stop | 49.0 |
| query | 3 | 739 | 99 | stop | 4.4 |
| L1 filter (in search) | 3 | 7561 | 75 | stop | 4.5 |
| writer | 3 | 5130 | 810 | stop | 34.7 |
| query | 4 | 897 | 108 | stop | 4.6 |
| L1 filter (in search) | 4 | 7925 | 73 | stop | 4.6 |
| writer | 4 | 4257 | 651 | stop | 28.3 |
| query | 5 | 1071 | 99 | stop | 4.3 |
| L1 filter (in search) | 5 | 6710 | 76 | stop | 4.5 |
| writer | 5 | 5494 | 1053 | stop | 45.4 |
| query | 6 | 1164 | 91 | stop | 4.0 |
| L1 filter (in search) | 6 | 11066 | 69 | stop | 5.1 |
| writer | 6 | 7060 | 306 | stop | 14.1 |

## Validation warnings

- 9 image citation(s) written as [citation:imgN] were converted to figures
- rule-based evidence check: 4 miscited (see validation.json grounding_findings)
- rule-based evidence check: 8 uncited_claims (see validation.json grounding_findings)
- section 1: removed 2 repeated sentence(s), a sentence occurred up to 3 times (writer repetition loop suspected)
- video start/end claim check: 1 ending_early, 1 opening_unverifiable (see validation.json boundary_findings)
