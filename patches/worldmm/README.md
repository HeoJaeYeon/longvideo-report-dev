# WorldMM 로컬 수정 (patch)

이 프로젝트가 쓰는 WorldMM(`https://github.com/wgcyeo/WorldMM`, 커밋 `3a55b65`, 2026-07-30)에는 이 프레임워크가
의존하는 소스 수정 2개가 들어 있다. 2026-09에 WorldMM이 가정한 OpenAI 모델 대신 로컬 Qwen3-VL-8B로 돌리려고 고쳤다
(당시 기록: `internal/legacy/worldmm/HANDOFF.md` §2).
여기의 patch 파일은 그 checkout에서 `git diff`로 뽑은 것이다. 깨끗한 `3a55b65`에 적용하면 현재 파일과 바이트 단위로 같아진다
(2026-11-10 확인). 2026-11-13에는 현재 WorldMM 작업 트리에 두 patch가 그대로 적용되어 있음을 다시 확인했다(`git apply --check -R`).

| Patch | 파일 | 바꾼 내용 | 필요한 곳 |
|---|---|---|---|
| `0001-qwen3vl-generation-lock-and-json-parsing.patch` | `src/worldmm/llm/qwen3vl.py` | (1) `generate()`의 GPU 부분을 `threading.Lock`으로 감쌈(한 모델에 동시 호출하면 CUDA illegal memory access가 났음). (2) `_parse_structured_response`: 앞쪽 코드 펜스 제거, 첫 JSON 값만 해석(`raw_decode`, `strict=False`), 맨 JSON 배열을 스키마의 단일 필드로 감쌈 | 메모리 구축(OpenIE, semantic 추출), `prebuild_episodic_index.py`(HTTP OpenIE 클라이언트가 이 함수로 응답을 해석), `local_llm_server.py`(이 클래스로 모델을 불러옴) |
| `0002-multiscale-load-llm-once.patch` | `src/worldmm/memory/episodic/multiscale.py` | LLM을 한 번만 불러와 공유하고 worker는 1개(영상마다 불러오며 worker 최대 8개로 돌리면 GPU 메모리가 부족했음) | 메모리 구축 3단계(30sec·3min·10min 요약) |

새로 clone한 WorldMM에 적용하기:

```bash
git clone https://github.com/wgcyeo/WorldMM.git && cd WorldMM && git checkout 3a55b65
git apply /path/to/report_framework/patches/worldmm/*.patch
```

이력: 2026-11-10 정리 전까지는 같은 checkout의 `script/4_eval.sh`, `script/videomme/4_eval.sh`도 모델명이
`qwen3vl`로 바뀌어 있었다. 이 이름은 WorldMM `MODEL_DICT`의 키(`qwen3vl-2b/4b/8b`)가 아니라서 그 스크립트는 실행되지 않았고,
프레임워크도 쓰지 않는다. 2026-11-10에 원본으로 되돌렸고, 바뀌었던 내용은 `internal/legacy/worldmm/reverted_4_eval_model_names.patch`에
보존했다(`internal/status/REORG_LOG_20261110.md` §11). 이 문서는 되돌린 뒤에도 "그 수정이 남아 있다"고 적혀 있었고, 2026-11-13에 바로잡았다.

WorldMM은 Apache License 2.0이다. 이 patch들은 WorldMM 소스의 수정본이므로 같은 라이선스를 따른다.
