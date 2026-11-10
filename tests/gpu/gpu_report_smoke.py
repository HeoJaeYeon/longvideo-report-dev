"""
Real-model mini report (GPU, per-process cap 19,000 MiB). Run with CUDA_VISIBLE_DEVICES=<gpu>, argv[1]=LLM port.
Retrieval: real Qwen3-Embedding + VLM2Vec, real 10sec-only HippoRAG cache (gpu_smoke.py), L1 via the LLM server.
Report: Deep-Reporter generate_article(with_planner) under the videomme domain templates, writer = Qwen3-VL-8B.
Checks how the real model follows the templates. Outputs go to the scratchpad.
"""
import copy, json, os, re, sys, threading, time
import torch
torch.cuda.set_per_process_memory_fraction(19000 / (torch.cuda.get_device_properties(0).total_memory / 2**20))
import requests

RF = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRATCH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_artifacts")   # tests/_artifacts
sys.path.insert(0, RF)
from rf_config import load_config  # noqa: E402
VID = "-QuCz7kxBr8"
PORT = int(sys.argv[1])


def main():
    import logging
    logging.basicConfig(level=logging.WARNING)
    cfg = load_config(os.path.join(RF, "config.yaml"))
    os.environ["HF_HOME"] = cfg["paths"]["hf_home"]
    cfg["paths"]["episodic_cache_root"] = os.path.join(SCRATCH, "gpu_test", "episodic")
    cfg["service"]["frames_dir"] = os.path.join(SCRATCH, "gpu_test", "frames")
    cfg["worldmm"]["granularities"] = ["10sec"]
    cfg["retrieval"]["episodic_candidates_per_query"] = {"10sec": 6}
    cfg["retrieval"]["episodic_filter"] = "L1"
    cfg["llm"]["local"]["endpoint"]["port"] = PORT

    import deep_reporter.api  # noqa: F401  (import order)
    from worldmm.embedding import EmbeddingModel
    import videorag_retriever_service as S
    import domain_templates as D
    emb = EmbeddingModel(text_model_name=cfg["worldmm"]["text_embedding_model"]); emb.load_model()
    llm = S.EndpointLLM.from_config(cfg)
    retr = S.WorldMMRetriever(cfg, emb, llm)
    threading.Thread(target=lambda: S.create_app(retr).run(host="127.0.0.1", port=18320), daemon=True).start()

    t = time.time()
    while True:
        try:
            if requests.get(f"http://127.0.0.1:{PORT}/health", timeout=2).ok:
                break
        except requests.RequestException:
            pass
        if time.time() - t > 900:
            raise SystemExit("LLM server not ready")
        time.sleep(5)
    print(f"[ready] LLM server after {time.time() - t:.0f}s", flush=True)

    os.environ["QWEN_BASE_URL"] = f"http://127.0.0.1:{PORT}/v1"; os.environ["QWEN_API_KEY"] = "EMPTY"
    from deep_reporter.api import create_openai_api
    api = create_openai_api({"primary_model": "qwen3vl-8b", "log_dir": os.path.join(SCRATCH, "dr_logs_gpu")})
    overview = D.load_video_overview(os.path.join(cfg["paths"]["caption_dir"], VID, "10min.json"))
    t = time.time()
    with D.apply_templates(D.build_templates("videomme", overview)):
        res = api.generate_article(
            overall_query="Write a report describing what happens in this video: who takes part, what is tested, and how the tests turn out.",
            overall_checklist=[], generation_mode="with_planner", text_topk=20, image_topk=10, enable_filter=False,
            retriever_url=f"http://127.0.0.1:18320/videos/{VID}/search", userid="gpu_template_smoke")
    print(f"[report] success={res['success']} sections={len(res.get('outline', []))} in {time.time() - t:.0f}s", flush=True)
    out_dir = os.path.join(SCRATCH, "gpu_report"); os.makedirs(out_dir, exist_ok=True)
    open(os.path.join(out_dir, "report.md"), "w").write(res.get("final_article", ""))
    json.dump(res.get("outline", []), open(os.path.join(out_dir, "outline.json"), "w"), indent=2, ensure_ascii=False)

    for i, s in enumerate(res.get("outline", [])):
        content = s.get("content") or ""
        texts, imgs = s.get("retrieved_texts") or [], s.get("retrieved_images") or []
        txt_ids = [int(x) for x in re.findall(r"\[citation:txt(\d+)\]", content)]
        img_ids = [int(x) for x in re.findall(r"!\[\]\(citation:img(\d+)\)", content)]
        loose = re.findall(r"\[citation:[^\]]*(?:,|\s)[^\]]*\]", content)
        evidence = " ".join([t.get("content", "") for t in texts] + [m.get("caption", "") for m in imgs])
        times = set(re.findall(r"\b\d\d:\d\d:\d\d\b", content))
        ungrounded = sorted(t for t in times if t not in evidence)
        print(f"\n[section {i + 1}] {s['section_description'][:120]}")
        print(f"  queries: text={s.get('text_queries')} image={s.get('image_queries')}")
        print(f"  evidence: texts={len(texts)} images={len(imgs)} | words={len(content.split())}"
              f" | failed_text={'Call failed' in content or 'Section generation failed' in content}")
        print(f"  citations: txt={len(txt_ids)} (out of range {[x for x in txt_ids if not 1 <= x <= len(texts)]})"
              f" img={len(img_ids)} (out of range {[x for x in img_ids if not 1 <= x <= len(imgs)]}) malformed={loose[:3]}")
        print(f"  timestamps in text: {len(times)} | not found in its evidence: {ungrounded[:6]}")
    print("\n[report head]\n" + res.get("final_article", "")[:1500])


if __name__ == "__main__":
    main()
