# -QuCz7kxBr8__c0_written__r1 — intermediate outputs

- Run `outputs/p9p19_check_20261025_141401`, stack 0 (GPU 4), session `report_-QuCz7kxBr8_1792937701_cc772df2` 2026-10-25T14:15:01 – 2026-10-25T14:20:20 (UTC)
- Query: Write a report describing what happens in this video: the main people or subjects, the key events in the order they occur, and how the video concludes.
- Checklist: []
- validation: passed, generation 319.7 s
- report.md reproduced from report.json by re-running ground_report: True

## Files

- `01_planner_prompt.md`, `02_planner_output.md`
- `sNN/1_query_prompt.md` … `sNN/6_postprocess.md` (see the table)

| section | description | text / image queries | text / image evidence | cited text / image | writer output tokens | folder |
|---|---|---|---|---|---|---|
| 1 | This section introduces the six main participants—Chris, Zach, Cass, James, Mitc… | 2 / 1 | 12 / 3 | 8 / 2 | 624 (stop) | `s01/` |
| 2 | This section details the testing of the SKLZ Dribble Stick and the subsequent sh… | 3 / 1 | 12 / 3 | 8 / 0 | 907 (stop) | `s02/` |
| 3 | This section covers the testing of the Flick Glove and the Shot Coach device, in… | 3 / 1 | 12 / 3 | 7 / 0 | 1102 (stop) | `s03/` |
| 4 | This section details the “First Made Shot Shoots Silly String” game, including t… | 3 / 1 | 12 / 3 | 8 / 1 | 1019 (stop) | `s04/` |
| 5 | This section focuses on the final scoring segment, including the 3-1 victory for… | 3 / 1 | 12 / 3 | 5 / 0 | 459 (stop) | `s05/` |
| 6 | Conclusion: This section briefly summarizes the main results shown in the video … | 3 / 1 | 12 / 3 | 4 / 0 | 365 (stop) | `s06/` |

## LLM calls (LLM server log, in call order)

| call | section | prompt tokens | output tokens | finish | seconds |
|---|---|---|---|---|---|
| planner | — | 5219 | 764 | stop | 35.4 |
| query | 1 | 438 | 84 | stop | 3.8 |
| L1 filter (in search) | 1 | 8661 | 66 | stop | 4.4 |
| writer | 1 | 5184 | 624 | stop | 28.6 |
| query | 2 | 566 | 96 | stop | 4.3 |
| L1 filter (in search) | 2 | 9055 | 69 | stop | 4.7 |
| writer | 2 | 5287 | 907 | stop | 39.8 |
| query | 3 | 673 | 88 | stop | 3.8 |
| L1 filter (in search) | 3 | 9058 | 70 | stop | 4.7 |
| writer | 3 | 6071 | 1102 | stop | 48.3 |
| query | 4 | 834 | 83 | stop | 3.8 |
| L1 filter (in search) | 4 | 10709 | 74 | stop | 5.2 |
| writer | 4 | 4577 | 1019 | stop | 44.1 |
| query | 5 | 1011 | 87 | stop | 4.5 |
| L1 filter (in search) | 5 | 9288 | 70 | stop | 4.9 |
| writer | 5 | 4840 | 459 | stop | 20.3 |
| query | 6 | 1103 | 81 | stop | 3.7 |
| L1 filter (in search) | 6 | 12112 | 70 | stop | 5.5 |
| writer | 6 | 6125 | 365 | stop | 16.9 |

## Validation warnings

- 1 image citation(s) written as [citation:imgN] were converted to figures
- rule-based evidence check: 5 miscited (see validation.json grounding_findings)
- rule-based evidence check: 12 uncited_claims (see validation.json grounding_findings)
- video start/end claim check: 2 ending_early, 3 ending_unverifiable (see validation.json boundary_findings)
