# tests/fixtures — CPU 테스트가 읽는 실제 실행 기록 (2026-11-10)

`tests/unit/`의 CPU 테스트가 입력으로 쓰는, 실제 모델(Qwen3-VL-8B)로 만든 결과 일부다. 원래 git에서 제외된
`tests/_artifacts/`, `outputs/`에 있어서 새로 받은 사본에서는 테스트가 돌지 않았다. 같은 파일을 복사해 두었다(바이트 동일).

| 파일 | 원래 위치 | 쓰는 테스트 |
|---|---|---|
| `smoke_report_A/outline.json` | `tests/_artifacts/gpu_report/outline.json` (보고서 A, 2026-10-21 GPU smoke) | `test_report_pipeline.py` (후처리·규칙 검사·번역) |
| `smoke_report_A/frames/-QuCz7kxBr8/*.jpg` (14장) | `tests/_artifacts/gpu_test/frames/-QuCz7kxBr8/` (보고서 A가 인용한 프레임) | `test_report_pipeline.py` |
| `e2e_report_B/report.json`, `report.md` | `tests/_artifacts/gpu_e2e/outputs/report_run1/` (보고서 B, 첫 `run_report.py` 실행) | `test_report_pipeline.py` part 4 |
| `c5_loop_report/report.json` | `outputs/c5_c0_20261025_132851/-QuCz7kxBr8__c0_written__r1/report.json` (writer 반복 루프가 생긴 보고서) | `test_p9_p19.py` (반복 문장 제거) |
| `prebuild_indexer_20261022.log` | `outputs/3videos_20261022_120438/prebuild_indexer.log` (OpenIE 실패 응답 14건) | `test_openie_split_guard.py` |

- 테스트 출력은 계속 `tests/_artifacts/`(git 제외)에 쓴다.
- JSON·로그 안의 경로(`img_path`, `video_path` 등)는 실행 당시 절대 경로이고, 사용자명만 `USER`로 바꿨다(2026-11-12). `test_report_pipeline.py`는 그림 경로를 이 폴더로 바꿔 쓴다.
- 이 테스트들은 이 폴더 말고도 WorldMM 메모리(`config.yaml`의 `caption_dir`·`metadata_dir`)와 영상 파일(`worldmm_root` 아래 `data/Video-MME/data/`)을 읽는다.
- 프레임 이미지는 Video-MME 영상에서 뽑은 것이라 외부 공개 전에 재배포 조건을 확인해야 한다.
