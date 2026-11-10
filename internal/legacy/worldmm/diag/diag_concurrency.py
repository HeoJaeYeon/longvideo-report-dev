"""Diagnose: is concurrent generate() on one qwen3vl-8b instance the cause of the
CUDA illegal memory access seen in OpenIE? Compare concurrent vs sequential."""
from concurrent.futures import ThreadPoolExecutor
from worldmm.llm import LLMModel

print("[diag] loading qwen3vl-8b ...", flush=True)
m = LLMModel(model_name="qwen3vl-8b")
prompts = [f"Extract entities from: 'Alice met Bob at cafe number {i}.' Reply briefly." for i in range(4)]

print("[diag] === concurrent (ThreadPoolExecutor, like batch_openie) ===", flush=True)
try:
    with ThreadPoolExecutor() as ex:
        out = list(ex.map(lambda p: m.generate(p), prompts))
    print("[diag] CONCURRENT OK:", [o[:40] for o in out], flush=True)
except Exception as e:
    print(f"[diag] CONCURRENT FAILED -> {type(e).__name__}: {str(e)[:120]}", flush=True)
print("[diag] CONCURRENT_DONE", flush=True)
