# WorldMM local patches

The checked-out WorldMM (`https://github.com/wgcyeo/WorldMM`, commit `3a55b65`, 2026-07-30) carries two local
source changes that this project depends on. They were made in September 2026 so that WorldMM runs with a local
Qwen3-VL-8B instead of the OpenAI models it assumes (record: `WorldMM/claude_output/HANDOFF.md` §2).
The patch files here are exported with `git diff` from that checkout; applying them to a clean `3a55b65`
reproduces the current files byte for byte (checked 2026-11-10).

| Patch | File | Change | Who needs it |
|---|---|---|---|
| `0001-qwen3vl-generation-lock-and-json-parsing.patch` | `src/worldmm/llm/qwen3vl.py` | (1) a `threading.Lock` around the GPU part of `generate()` (concurrent calls on one model caused CUDA illegal memory access); (2) `_parse_structured_response`: strip any opening code fence, decode only the first JSON value (`raw_decode`, `strict=False`), wrap a bare JSON array into the schema's single field | Memory build (OpenIE, semantic extraction); `report_framework/prebuild_episodic_index.py` (its HTTP OpenIE client parses responses with this function); `local_llm_server.py` loads the model through this class |
| `0002-multiscale-load-llm-once.patch` | `src/worldmm/memory/episodic/multiscale.py` | load the LLM once and share it, one worker (per-video loading with up to 8 workers ran out of GPU memory) | Memory build step 3 (30sec/3min/10min summaries) |

Apply to a fresh clone:

```bash
git clone https://github.com/wgcyeo/WorldMM.git && cd WorldMM && git checkout 3a55b65
git apply /path/to/report_framework/patches/worldmm/*.patch
```

Not exported: the same checkout also changes `script/4_eval.sh` and `script/videomme/4_eval.sh`
(model names `gpt-5-mini`/`gpt-5` -> `qwen3vl`). This project does not use them, and `qwen3vl` is not a model
key of WorldMM's `MODEL_DICT` (`qwen3vl-2b/4b/8b`), so those scripts fail with the edited defaults.
