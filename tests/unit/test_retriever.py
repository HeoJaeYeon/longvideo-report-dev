"""
CPU-only integration test for report_framework/videorag_retriever_service.py.

Real data (captions, semantic triples, visual embeddings, video file) of one video +
real WorldMM/HippoRAG code; only the models are fakes (no GPU):
  - FakeEmbedding: hashed bag-of-words text vectors, seeded random 1536-d visual query vectors
  - FakeOpenIE LLM: builds the test HippoRAG cache (NER/triples from capitalized words)
  - fake OpenAI-compatible filter server (local_llm_server.create_app + FakeFilterLLM)
All writes go to the scratchpad directory.
"""
import copy, hashlib, json, os, re, sys, threading, time
import numpy as np, requests

RF = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRATCH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_artifacts")   # tests/_artifacts
sys.path.insert(0, RF)
from rf_config import load_config  # noqa: E402
VID = "-QuCz7kxBr8"
LABEL = "fake-llm"


class FakeEmbedding:
    dim = 512

    def _vec(self, text):
        v = np.full(self.dim, 1e-3)
        for w in re.findall(r"[a-z0-9]+", str(text).lower()):
            v[int(hashlib.md5(w.encode()).hexdigest(), 16) % self.dim] += 1.0
        return v / np.linalg.norm(v)

    def encode_text(self, texts, **kw):
        texts = [texts] if isinstance(texts, str) else list(texts)
        return np.stack([self._vec(t) for t in texts]).astype(np.float32)

    def encode(self, content, modality="text", **kw):
        return self.encode_text(content)

    def encode_vis_query(self, texts, **kw):
        texts = [texts] if isinstance(texts, str) else list(texts)
        out = [np.random.default_rng(int(hashlib.md5(t.encode()).hexdigest()[:8], 16)).standard_normal(1536) for t in texts]
        return np.stack(out).astype(np.float32)


class FakeOpenIE:
    model_name = LABEL

    def generate(self, messages, text_format=None, **kw):
        text = messages[-1]["content"]
        m = re.search(r"```\n(.*?)\n```", text, re.S)
        passage = m.group(1) if m else text
        ents = list(dict.fromkeys(re.findall(r"\b[A-Z][a-zA-Z]{2,}\b", passage)))[:6] or ["scene"]
        if text_format.__name__ == "NerRawOutput":
            return text_format(named_entities=ents)
        triples = [[ents[i], "appears with", ents[i + 1]] for i in range(len(ents) - 1)] or [[ents[0], "is in", "video"]]
        return text_format(triples=triples)


class FakeFilterLLM:
    """Serves WorldMM multiscale_filter (returns caption ids) and DSPy fact filter prompts."""
    class model:
        class processor:
            @staticmethod
            def apply_chat_template(msgs, tokenize=False, add_generation_prompt=True):
                return " ".join(m["content"] if isinstance(m["content"], str) else "" for m in msgs)
            class tokenizer:
                def __call__(self, text, add_special_tokens=True):
                    class R: pass
                    r = R(); r.input_ids = text.split(); return r
            tokenizer = tokenizer()
    prompts = []

    def generate(self, messages, **kw):
        user = messages[-1]["content"]
        FakeFilterLLM.prompts.append(user)
        if "fact_before_filter" in user:
            facts = json.loads(user.split("[[ ## fact_before_filter ## ]]\n", 1)[1].split("\n\nRespond", 1)[0])["fact"]
            return "[[ ## fact_after_filter ## ]]\n" + json.dumps({"fact": facts[:2]}) + "\n\n[[ ## completed ## ]]"
        ids = re.findall(r'"id": "([^"]+)"', user)
        return json.dumps(list(reversed(ids))[:20])   # deterministic, different from RRF order


def build_test_cache(cfg):
    from prebuild_episodic_index import make_labeled_episodic_memory_class
    from worldmm.llm import PromptTemplateManager
    Cls = make_labeled_episodic_memory_class()
    mem = Cls(embedding_model=FakeEmbedding(), llm_model=FakeOpenIE(), prompt_template_manager=PromptTemplateManager(),
              granularities=cfg["worldmm"]["granularities"],
              save_dir_root=os.path.join(cfg["paths"]["episodic_cache_root"], VID, "episodic_memory"), llm_label=LABEL)
    cap = os.path.join(cfg["paths"]["caption_dir"], VID)
    mem.load_captions_from_files({g: os.path.join(cap, f"{g}.json") for g in cfg["worldmm"]["granularities"]})
    mem.index(cfg["worldmm"]["query_time"])


def check(cond, msg):
    print(("  PASS " if cond else "  FAIL ") + msg)
    if not cond:
        check.failed += 1
check.failed = 0


def main():
    import logging
    logging.basicConfig(level=logging.WARNING)
    cfg = load_config(os.path.join(RF, "config.yaml"))
    cfg["paths"]["episodic_cache_root"] = os.path.join(SCRATCH, "test_cache", "episodic")
    cfg["service"]["frames_dir"] = os.path.join(SCRATCH, "test_cache", "frames")
    cfg["worldmm"]["episodic_cache_label"] = LABEL

    t = time.time()
    if not os.path.isdir(os.path.join(cfg["paths"]["episodic_cache_root"], VID)):
        build_test_cache(cfg)
    print(f"[setup] test HippoRAG cache ready ({time.time() - t:.1f}s)")

    import local_llm_server as L
    threading.Thread(target=lambda: L.create_app(FakeFilterLLM(), "qwen3vl-8b", 512).run(host="127.0.0.1", port=18010),
                     daemon=True).start()
    cfg["llm"]["local"]["endpoint"]["port"] = 18010
    time.sleep(1.0)

    import videorag_retriever_service as S
    emb = FakeEmbedding()
    q_text = ["basketball dribbling gadget test", "players introduce the challenge"]
    q_img = ["man dribbling a basketball on an outdoor court"]

    # ---- precheck refuses incomplete cache (different label -> nothing cached) ----
    bad = copy.deepcopy(cfg); bad["worldmm"]["episodic_cache_label"] = "no-such-label"
    probs = S.WorldMMRetriever(bad, emb, S.NoLLM()).check_inputs(VID)
    print("[precheck]"); check(any("episodic cache incomplete" in p for p in probs), f"incomplete cache refused: {probs[0][:90]}...")

    for mode in ["L0", "L1", "full"]:
        c = copy.deepcopy(cfg); c["retrieval"]["episodic_filter"] = mode
        llm = S.NoLLM() if mode == "L0" else S.EndpointLLM.from_config(c)
        r = S.WorldMMRetriever(c, emb, llm)
        n_prompts = len(FakeFilterLLM.prompts)
        t = time.time(); res = r.search(VID, q_text, "text", 20); dt = time.time() - t
        epi = [x for x in res["results"] if x["source"] == "worldmm-episodic"]
        sem = [x for x in res["results"] if x["source"] == "worldmm-semantic"]
        llm_calls = len(FakeFilterLLM.prompts) - n_prompts
        print(f"[{mode}] text: {len(epi)} episodic + {len(sem)} semantic, meta={res['meta']}, llm_calls={llm_calls}, {dt:.1f}s")
        if mode == "full":  # per-query results overlap, so merged count can be below episodic_k
            check(res["status"] == "success" and 0 < len(epi) <= cfg["retrieval"]["episodic_k"] and len(sem) == cfg["retrieval"]["semantic_k"], f"counts: episodic {len(epi)} (<= episodic_k) + semantic_k")
        else:
            check(res["status"] == "success" and len(epi) == cfg["retrieval"]["episodic_k"] and len(sem) == cfg["retrieval"]["semantic_k"], "counts = episodic_k + semantic_k")
        check(len({x["uid"] for x in res["results"]}) == len(res["results"]), "uids unique")
        check(all(re.match(r"^\[\d\d:\d\d:\d\d-\d\d:\d\d:\d\d \| episodic \w+\] ", x["content"]) for x in epi), "episodic content has [HH:MM:SS-HH:MM:SS | episodic g] prefix")
        check(all(x["content"].startswith("[video-level knowledge | semantic] (") and x["start_time"] is None for x in sem), "semantic: video-level label, no time")
        check(all(os.path.isabs(x["video_path"]) and os.path.isfile(x["video_path"]) for x in epi), "episodic video_path absolute & exists")
        expected_calls = {"L0": 0, "L1": 1}.get(mode)
        if expected_calls is not None:
            check(llm_calls == expected_calls, f"LLM calls per request = {expected_calls}")
        else:
            check(llm_calls >= len(q_text), f"full mode calls LLM per query (got {llm_calls})")
        if mode == "L1":
            check(res["meta"]["episodic_filter"] == "llm", "L1 filter ran through the endpoint")
            print("    L1 order (granularity:id):", [x["uid"].split(":")[-1] for x in epi])
        if mode == "L0":
            print("    sample:", epi[0]["content"][:110], "|", sem[0]["content"][:80])

    # ---- image ----
    c = copy.deepcopy(cfg); c["retrieval"]["episodic_filter"] = "L0"
    r = S.WorldMMRetriever(c, emb, S.NoLLM())
    res = r.search(VID, q_img + ["scoreboard close-up"], "image", 10)
    imgs = res["results"]
    print(f"[image] {len(imgs)} frames, meta={res['meta']}")
    check(len(imgs) == cfg["retrieval"]["image_k"], "image count = image_k")
    check(all(os.path.isfile(x["img_path"]) for x in imgs), "frame files exist")
    from PIL import Image
    check(all(Image.open(x["img_path"]).size[0] > 0 for x in imgs), "frames decodable")
    cap10 = {c["start_time"]: c["text"] for c in json.load(open(os.path.join(cfg["paths"]["caption_dir"], VID, "10sec.json")))}
    check(all(x["caption"].endswith(cap10[x["start_time"]]) for x in imgs), "caption = exact 10sec caption of the clip")
    check(all(x["start_sec"] <= x["frame_sec"] <= x["end_sec"] for x in imgs), "frame time inside clip interval")
    print("    sample:", imgs[0]["img_path"], "|", imgs[0]["caption"][:100])

    # ---- HTTP + Deep-Reporter contract ----
    app = S.create_app(r)
    threading.Thread(target=lambda: app.run(host="127.0.0.1", port=18020), daemon=True).start(); time.sleep(1.0)
    base = "http://127.0.0.1:18020"
    print("[http]")
    check(requests.post(f"{base}/videos/NOPE/search", json={"query_list": ["x"], "type": "text"}).status_code == 404, "unknown video -> 404")
    check(requests.post(f"{base}/videos/{VID}/search", json={"query_list": ["x"], "type": "audio"}).status_code == 400, "bad type -> 400")
    check(requests.post(f"{base}/videos/{VID}/search", json={"query_list": []}).status_code == 400, "empty query_list -> 400")
    other = sorted(os.listdir(cfg["paths"]["caption_dir"]))[1]
    check(requests.post(f"{base}/videos/{other}/load").status_code == 409, f"video without cache ({other}) -> 409")

    # Deep-Reporter's real search_node against the service
    import deep_reporter.api  # noqa: F401  (import order: avoids circular import)
    from deep_reporter.nodes.search_node import search_node
    state = {"current_section_index": 0, "text_topk": 20, "image_topk": 10,
             "outline": [{"section_description": "d", "sectional_checklist": [], "text_queries": q_text, "image_queries": q_img}]}
    try:
        # search_node uses LangGraph's get_stream_writer(), so run it inside a one-node graph (as in production).
        from langgraph.graph import StateGraph, END
        from deep_reporter.core.state import MultimodalLongFormState
        g = StateGraph(MultimodalLongFormState); g.add_node("search", search_node)
        g.set_entry_point("search"); g.add_edge("search", END)
        out = g.compile().invoke(state, {"configurable": {"retriever_url": f"{base}/videos/{VID}/search"}})
        sec = out["outline"][0]
        print(f"  Deep-Reporter search_node: retrieved_texts={len(sec['retrieved_texts'])} retrieved_images={len(sec['retrieved_images'])}")
        check(len(sec["retrieved_texts"]) > 0 and len(sec["retrieved_images"]) > 0, "search_node stored text and image evidence")
        mats = [f"[Source txt{i}] {t.get('content', t.get('text', ''))[:60]}" for i, t in enumerate(sec["retrieved_texts"][:2], 1)]
        mats += [f"[Source img{i}: {m.get('caption', m.get('description', 'Image'))[:60]}]" for i, m in enumerate(sec["retrieved_images"][:1], 1)]
        print("  writer would see:\n    " + "\n    ".join(mats))
    except Exception as e:
        check(False, f"search_node call failed: {type(e).__name__}: {e}")

    print(f"\nRESULT: {'ALL PASS' if check.failed == 0 else f'{check.failed} FAILED'}")


if __name__ == "__main__":
    main()
