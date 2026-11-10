"""
GPU smoke test (real models, per-GPU budget < 20 GB). Run with CUDA_VISIBLE_DEVICES=<one GPU>.
Stage 1: real 10sec HippoRAG cache (Qwen3-Embedding-4B + preprocess OpenIE seed incl. empty triples; no LLM)
Stage 2: retrieval service L0 with real Qwen3-Embedding + VLM2Vec (text/image, frames)
Stage 4: L1 via a separately started local_llm_server (port from argv) + Deep-Reporter search_node over HTTP
All outputs go to the scratchpad.
"""
import copy, json, os, sys, threading, time

import torch
BUDGET_MIB = 19000
torch.cuda.set_per_process_memory_fraction(BUDGET_MIB / (torch.cuda.get_device_properties(0).total_memory / 2**20))

RF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
SCRATCH = os.path.join(os.path.dirname(os.path.abspath(__file__)), "_artifacts")
sys.path.insert(0, RF)
from rf_config import load_config  # noqa: E402
VID = "-QuCz7kxBr8"
LLM_PORT = int(sys.argv[1]) if len(sys.argv) > 1 else 0


def mem(tag):
    print(f"  [gpu] {tag}: allocated={torch.cuda.memory_allocated() / 2**20:.0f} MiB "
          f"peak_reserved={torch.cuda.max_memory_reserved() / 2**20:.0f} MiB", flush=True)


def main():
    import logging
    logging.basicConfig(level=logging.WARNING)
    cfg = load_config(os.path.join(RF, "config.yaml"))
    os.environ["HF_HOME"] = cfg["paths"]["hf_home"]
    cfg["paths"]["episodic_cache_root"] = os.path.join(SCRATCH, "gpu_test", "episodic")
    cfg["service"]["frames_dir"] = os.path.join(SCRATCH, "gpu_test", "frames")
    cfg["worldmm"]["granularities"] = ["10sec"]
    cfg["retrieval"]["episodic_candidates_per_query"] = {"10sec": 6}
    label = cfg["worldmm"]["episodic_cache_label"]

    from worldmm.embedding import EmbeddingModel
    from worldmm.llm import PromptTemplateManager
    import videorag_retriever_service as S
    from prebuild_episodic_index import make_labeled_episodic_memory_class, indexed_texts, chunk_id, openie_cache_path

    t = time.time()
    emb = EmbeddingModel(text_model_name=cfg["worldmm"]["text_embedding_model"])
    emb.load_model(model_type="text")
    print(f"[load] Qwen3-Embedding-4B {time.time() - t:.0f}s"); mem("after text model")

    # ---- Stage 1: real 10sec cache (seed all preprocess OpenIE, incl. empty triples -> no LLM) ----
    cache_file = openie_cache_path(cfg["paths"]["episodic_cache_root"], VID, "10sec", label)
    if not os.path.isfile(cache_file):
        texts = indexed_texts(os.path.join(cfg["paths"]["caption_dir"], VID, "10sec.json"), cfg["worldmm"]["query_time"])
        pre = json.load(open(os.path.join(cfg["paths"]["metadata_dir"], "episodic_memory", VID, "openie_results_qwen3vl-8b.json")))
        docs, seen = [], set()
        for text in texts:
            k = chunk_id(text)
            if k not in seen:
                seen.add(k)
                docs.append({"idx": k, "passage": text, "extracted_entities": pre["ner_results"][k], "extracted_triples": pre["triple_results"][k]})
        os.makedirs(os.path.dirname(cache_file), exist_ok=True)
        json.dump({"docs": docs}, open(cache_file, "w"))
        t = time.time()
        Cls = make_labeled_episodic_memory_class()
        m = Cls(embedding_model=emb, llm_model=S.NoLLM(), prompt_template_manager=PromptTemplateManager(), granularities=["10sec"],
                save_dir_root=os.path.join(cfg["paths"]["episodic_cache_root"], VID, "episodic_memory"), llm_label=label)
        m.load_captions_from_files({"10sec": os.path.join(cfg["paths"]["caption_dir"], VID, "10sec.json")})
        m.index(cfg["worldmm"]["query_time"])   # NoLLM raises if OpenIE were needed
        print(f"[stage1] real 10sec HippoRAG cache built in {time.time() - t:.0f}s ({len(docs)} chunks, 0 LLM calls)")
        del m
    mem("after stage1")

    # ---- Stage 2: L0 with real models ----
    emb.load_model(model_type="vision")
    mem("after VLM2Vec")
    c = copy.deepcopy(cfg); c["retrieval"]["episodic_filter"] = "L0"
    r = S.WorldMMRetriever(c, emb, S.NoLLM())
    t = time.time(); r.load(VID); print(f"[stage2] load {time.time() - t:.1f}s")
    queries = ["testing viral basketball gadgets", "dribbling speed time trial with goggles"]
    for dtype, qs, k in [("text", queries, 20), ("image", ["man dribbling a basketball on an outdoor court"], 10)]:
        t = time.time(); res = r.search(VID, qs, dtype, k)
        print(f"[stage2] {dtype}: {res['total_hits']} hits in {time.time() - t:.2f}s meta={res['meta']}")
        for x in res["results"][:5 if dtype == "text" else 4]:
            body = x["content"] if dtype == "text" else x["caption"]
            print(f"    {x['rank']:>2} {x['source']:<17} {body[:150]}")
            if dtype == "image":
                print(f"       img={x['img_path']} exists={os.path.isfile(x['img_path'])}")
        sem = [x for x in res["results"] if x["source"] == "worldmm-semantic"]
        for x in sem[:2]:
            print(f"    sem {x['content'][:120]}")
    mem("after stage2")

    if not LLM_PORT:
        return
    # ---- Stage 3: wait for local_llm_server, then a real Deep-Reporter client round trip ----
    import requests
    t = time.time()
    while True:
        try:
            if requests.get(f"http://127.0.0.1:{LLM_PORT}/health", timeout=2).ok:
                break
        except requests.RequestException:
            pass
        if time.time() - t > 900:
            raise SystemExit("local_llm_server not ready after 15 min")
        time.sleep(5)
    print(f"[stage3] local_llm_server ready (waited {time.time() - t:.0f}s)")
    os.environ["QWEN_BASE_URL"] = f"http://127.0.0.1:{LLM_PORT}/v1"; os.environ["QWEN_API_KEY"] = "EMPTY"
    import deep_reporter.api  # noqa: F401  (import order)
    from deep_reporter.api import create_openai_api
    from deep_reporter.llms.factory import get_primary_llm
    from deep_reporter.utils.llm_utils import LLMCaller
    create_openai_api({"primary_model": "qwen3vl-8b"})
    t = time.time()
    content, _ = LLMCaller.call_llm(get_primary_llm("answer"), [{"role": "user", "content":
        "Write a one-sentence section title (start with '# ') for a report about testing viral basketball gadgets."}])
    print(f"[stage3] Deep-Reporter client -> Qwen3-VL-8B ({time.time() - t:.1f}s): {content[:200]!r}")

    # ---- Stage 4: L1 (real Qwen3-VL-8B filter) + Deep-Reporter search_node ----
    c = copy.deepcopy(cfg); c["retrieval"]["episodic_filter"] = "L1"; c["llm"]["local"]["endpoint"]["port"] = LLM_PORT
    llm = S.EndpointLLM.from_config(c)
    r1 = S.WorldMMRetriever(c, emb, llm); r1.load(VID)
    t = time.time(); res = r1.search(VID, queries, "text", 20)
    print(f"[stage4] L1 text: {res['total_hits']} hits in {time.time() - t:.1f}s meta={res['meta']} llm_calls={llm.calls} failures={llm.failures}")
    for x in [y for y in res["results"] if y["source"] == "worldmm-episodic"][:4]:
        print(f"    {x['rank']:>2} {x['content'][:140]}")

    app = S.create_app(r1)
    threading.Thread(target=lambda: app.run(host="127.0.0.1", port=18120), daemon=True).start(); time.sleep(1.5)
    import deep_reporter.api  # noqa: F401
    from deep_reporter.nodes.search_node import search_node
    from deep_reporter.core.state import MultimodalLongFormState
    from langgraph.graph import StateGraph, END
    g = StateGraph(MultimodalLongFormState); g.add_node("search", search_node); g.set_entry_point("search"); g.add_edge("search", END)
    state = {"current_section_index": 0, "text_topk": 20, "image_topk": 10,
             "outline": [{"section_description": "d", "sectional_checklist": [], "text_queries": queries,
                          "image_queries": ["man dribbling a basketball on an outdoor court"]}]}
    t = time.time()
    out = g.compile().invoke(state, {"configurable": {"retriever_url": f"http://127.0.0.1:18120/videos/{VID}/search"}})
    sec = out["outline"][0]
    print(f"[stage4] Deep-Reporter search_node: texts={len(sec['retrieved_texts'])} images={len(sec['retrieved_images'])} "
          f"({time.time() - t:.1f}s incl. 2s sleep in search_node)")
    mem("final")


if __name__ == "__main__":
    main()
