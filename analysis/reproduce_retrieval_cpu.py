"""
Re-run the retrieval of one finished report on CPU to recover what the service does not log:
per query x granularity graph-search results (with HippoRAG scores), the RRF-merged candidate
list, the exact L1 filter prompt, semantic per-query results, and visual similarity rankings
(2026-11-02, CPU only, no LLM call).

The service's own WorldMMRetriever class is used (videorag_retriever_service.py), with:
  - a COPY of cache/episodic/<vid> (loading a video rewrites HippoRAG OpenIE cache files; the real
    cache is md5-checked before/after and must be unchanged),
  - Qwen3-Embedding-4B (--dtype, default bfloat16) and VLM2Vec-V2.0 (bfloat16) on CPU with sdpa attention instead of
    flash_attention_2 (the GPU run used flash_attention_2; numbers can differ slightly),
  - NoLLM (any LLM call raises).
Reproduction checks against the recorded run, stored per section in the output (`checks`; nothing is assumed):
  - text_match: RRF candidate count = service log `episodic_candidates`, every recorded episodic item is in the
    reproduced candidates with the same RRF score (6 decimals), and the rebuilt L1 filter prompt has the token count
    the LLM server logged
  - semantic_match: same semantic ids, order and scores
  - visual_match: same image clips in the same order
A section whose check fails must not be presented as the run's internal state (only as a mismatch record).
Graph search keeps 2 ranks beyond k per list (within_k=False) so near-ties at the cut are visible.
The L1 filter's LLM response is not logged and is not reproduced.
Usage: python analysis/reproduce_retrieval_cpu.py --video=<vid> --work-dir <scratch dir> [--repeat 1]
Output: analysis/retrieval_repro_<vid>_r<repeat>.json
"""
import argparse, ast, copy, glob, hashlib, json, os, shutil, sys

RF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RF)
sys.path.insert(0, os.path.join(RF, "analysis"))
import numpy as np
import torch
import yaml
from export_stages import load_jobs, log_lines


def tree_md5(root):
    h = hashlib.md5()
    for d, _, fs in sorted(os.walk(root)):
        for f in sorted(fs):
            p = os.path.join(d, f)
            h.update(os.path.relpath(p, root).encode())
            h.update(open(p, "rb").read())
    return h.hexdigest()


class CPUQwen3Embedding:
    """Same as worldmm.embedding.qwen3_embedding.Qwen3EmbeddingModel, but CPU + sdpa."""

    def __init__(self, model_name, dtype):
        from sentence_transformers import SentenceTransformer
        self.model = SentenceTransformer(
            model_name, device="cpu",
            model_kwargs={"attn_implementation": "sdpa", "dtype": dtype},
            tokenizer_kwargs={"padding_side": "left"})

    def encode_text(self, texts, batch_size=256):
        if isinstance(texts, str):
            texts = [texts]
        return self.model.encode(texts, batch_size=batch_size)

    def encode(self, content, **kw):
        return self.encode_text(content, **kw)


def cpu_vlm2vec(model_name):
    """VLM2VecV2EmbeddingModel on CPU: its loader hard-codes flash_attention_2, so force sdpa while loading."""
    import transformers
    from worldmm.embedding import vlm2vecv2
    orig = transformers.PretrainedConfig.__setattr__

    def setattr_sdpa(self, k, v):
        if k == "_attn_implementation" and v == "flash_attention_2":
            v = "sdpa"
        orig(self, k, v)
    orig_fp = transformers.PreTrainedModel.from_pretrained.__func__

    def fp(cls, *a, **kw):
        if kw.get("attn_implementation") == "flash_attention_2":
            kw["attn_implementation"] = "sdpa"
        return orig_fp(cls, *a, **kw)
    transformers.PretrainedConfig.__setattr__ = setattr_sdpa
    transformers.PreTrainedModel.from_pretrained = classmethod(fp)
    try:
        return vlm2vecv2.VLM2VecV2EmbeddingModel(model_name=model_name, device="cpu")
    finally:
        transformers.PretrainedConfig.__setattr__ = orig
        transformers.PreTrainedModel.from_pretrained = classmethod(orig_fp)


def graph_search_scored(ret, g, query, k):
    """WorldMMRetriever._graph_search with HippoRAG scores kept (same code path)."""
    hipporag = ret.episodic.hipporag.get(g)
    if not hipporag.ready_to_retrieve:
        hipporag.prepare_retrieval_objects()
    hipporag.get_query_embeddings([query])
    fact_scores = hipporag.get_fact_scores(query)
    path, top_facts = "graph", []
    try:
        if len(fact_scores) == 0 or len(hipporag.fact_node_keys) == 0:
            path = "dense"
            doc_ids, doc_scores = hipporag.dense_passage_retrieval(query)
        else:
            link_top_k = hipporag.global_config.linking_top_k
            if len(fact_scores) <= link_top_k:
                fact_indices = np.argsort(fact_scores)[::-1].tolist()
            else:
                fact_indices = np.argsort(fact_scores)[-link_top_k:][::-1].tolist()
            fact_ids = [hipporag.fact_node_keys[i] for i in fact_indices]
            rows = hipporag.fact_embedding_store.get_rows(fact_ids)
            facts = [ast.literal_eval(rows[i]["content"]) for i in fact_ids]
            top_facts = [(list(f), float(fact_scores[i])) for f, i in zip(facts, fact_indices)]
            doc_ids, doc_scores = hipporag.graph_search_with_fact_entities(
                query=query, link_top_k=link_top_k, query_fact_scores=fact_scores,
                top_k_facts=facts, top_k_fact_indices=fact_indices,
                passage_node_weight=hipporag.global_config.passage_node_weight)
    except Exception as e:
        path = f"dense(fallback: {e})"
        doc_ids, doc_scores = hipporag.dense_passage_retrieval(query)
    out = []
    for idx, sc in zip(doc_ids, doc_scores):
        text = hipporag.chunk_embedding_store.get_row(hipporag.passage_node_keys[idx])["content"]
        entry = ret.text_to_entry[g].get(text)
        if entry is not None:
            out.append((entry, float(sc)))
            if len(out) >= k:
                break
    return out, path, top_facts


def ent(e):
    return {"id": e.id, "granularity": e.granularity, "start_time": e.start_time, "end_time": e.end_time, "text": e.text}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--run", default=os.path.join(RF, "outputs", "p9p19_check_20261025_141401"))
    ap.add_argument("--repeat", type=int, default=1)
    ap.add_argument("--work-dir", required=True)
    ap.add_argument("--dtype", default="bfloat16", choices=["bfloat16", "float32"], help="text embedding dtype on CPU")
    a = ap.parse_args()
    vid, run = a.video, os.path.abspath(a.run)
    job = f"{vid}__c0_written__r{a.repeat}"
    cfg = yaml.safe_load(open(os.path.join(run, f"config_{job}.yaml")))
    rj = json.load(open(os.path.join(run, job, "report.json")))
    sessions = {}
    for p in glob.glob(os.path.join(run, "dr_logs_s*", "*.jsonl")):
        for line in open(p):
            d = json.loads(line)
            sessions[d["session_id"]] = d
    ses = sessions[rj["session_id"]]
    t0, t1 = ses["start_time"][:19], ses["end_time"][:19]
    stack = load_jobs(run)[job]["stack"]
    llm = log_lines(glob.glob(os.path.join(run, f"llm_server_s{stack}_gpu*.log"))[0],
                    r"(\S+ \S+),\d+ local_llm_server INFO chat\.completions: prompt=(\d+) completion=(\d+) finish=(\w+) ([\d.]+)s",
                    t0, t1)
    svc = log_lines(glob.glob(os.path.join(run, f"service_s{stack}_gpu*.log"))[0],
                    r"(\S+ \S+),\d+ videorag_retriever INFO search (\w+): (.*)", t0, t1)
    outline = rj["outline"]
    n = len(outline)
    assert len(llm) == 1 + 3 * n and len(svc) == 2 * n

    real_cache = os.path.join(cfg["paths"]["episodic_cache_root"], vid)
    md5_before = tree_md5(real_cache)
    work_cache = os.path.join(os.path.abspath(a.work_dir), "episodic_cache")
    shutil.rmtree(work_cache, ignore_errors=True)
    shutil.copytree(real_cache, os.path.join(work_cache, vid))
    cfg2 = copy.deepcopy(cfg)
    cfg2["paths"]["episodic_cache_root"] = work_cache

    from worldmm.embedding import EmbeddingModel
    from worldmm.llm import PromptTemplateManager
    from transformers import AutoProcessor
    import videorag_retriever_service as S
    emb = EmbeddingModel(text_model_name=cfg["worldmm"]["text_embedding_model"], device="cpu")
    emb._text_model = CPUQwen3Embedding(cfg["worldmm"]["text_embedding_model"], getattr(torch, a.dtype))
    emb._vis_model = cpu_vlm2vec(emb.vis_model_name)
    ret = S.WorldMMRetriever(cfg2, emb, S.NoLLM())
    ret.load(vid)
    processor = AutoProcessor.from_pretrained("Qwen/Qwen3-VL-8B-Instruct")
    ptm = PromptTemplateManager()

    rr = ret.rcfg
    rrf_k = int(rr["rrf_k"])
    per_query = rr["episodic_candidates_per_query"]
    out = {"video_id": vid, "job": job, "run": os.path.relpath(run, RF),
           "settings": {"embedding": "Qwen3-Embedding-4B CPU bf16 sdpa", "visual": "VLM2Vec-V2.0 CPU bf16 sdpa",
                        "rrf_k": rrf_k, "episodic_candidates_per_query": per_query,
                        "linking_top_k": None, "semantic_k_per_query": rr["semantic_k_per_query"],
                        "visual_k_per_query": rr["visual_k_per_query"]},
           "sections": []}
    for i, s in enumerate(outline, 1):
        tq, iq = s["text_queries"], s["image_queries"]
        sec = {"index": i, "text_queries": tq, "image_queries": iq, "graph_search": [], "checks": {}}
        ck = sec["checks"]
        ranked = []
        for q in tq:
            for g in ret.wm["granularities"]:
                k = int(per_query.get(g, 0))
                scored, path, facts = graph_search_scored(ret, g, q, k + 2)   # 2 extra ranks: margin at the cut
                plain = ret._graph_search(g, q, k)
                assert [e.id for e, _ in scored[:k]] == [e.id for e in plain], (i, q, g)
                out["settings"]["linking_top_k"] = ret.episodic.hipporag[g].global_config.linking_top_k
                sec["graph_search"].append({"query": q, "granularity": g, "k": k, "path": path,
                                            "top_facts": facts,
                                            "results": [dict(ent(e), score=sc, within_k=r < k)
                                                        for r, (e, sc) in enumerate(scored)]})
                ranked.append(plain)
        merged = S.rrf_merge(ranked, key=lambda e: e.id, k=rrf_k)
        meta = ast.literal_eval(svc[2 * (i - 1)].group(3))
        ck["candidates"] = {"reproduced": len(merged), "recorded": meta["episodic_candidates"],
                            "ok": len(merged) == meta["episodic_candidates"]}
        sec["rrf"] = [dict(ent(e), rrf=round(sc, 6),
                           lists=[j for j, lst in enumerate(ranked) if any(x.id == e.id for x in lst)])
                      for e, sc in merged]
        score_of = {e.id: round(sc, 6) for e, sc in merged}
        rec_epi = [t for t in s["retrieved_texts"] if t["source"] == "worldmm-episodic"]
        bad = []
        for t in rec_epi:
            cid = t["uid"].split(":episodic:")[1]
            if cid not in score_of or abs(score_of[cid] - t["score"]) > 1e-6:
                bad.append({"id": cid, "recorded_rrf": t["score"], "reproduced_rrf": score_of.get(cid)})
        ck["episodic_rrf"] = {"mismatches": bad, "ok": not bad}
        sec["selected_by_l1"] = [t["uid"].split(":episodic:")[1] for t in rec_epi]
        # exact L1 filter prompt (WorldMM EpisodicMemory._filter_with_llm) and its token count
        caption_list = []
        for e, _ in merged:
            st, et = e.timestamp_int
            caption_list.append({"id": e.id, "granularity": e.granularity,
                                 "start_time": _tt(str(st)), "end_time": _tt(str(et)), "text": e.text})
        n_epi = min(int(rr["episodic_k"]), int(cfg["report"]["text_topk"]))
        prompt = ptm.render("multiscale_filter")
        prompt.append({"role": "user", "content": f"""Question: {"; ".join(tq)}

Retrieved Captions:
{json.dumps(caption_list, indent=2)}

Select the top {n_epi} most relevant caption IDs to answer the question.
Return ONLY a JSON array of caption IDs in order of relevance (most relevant first)."""})
        text_only = [{"role": m["role"], "content": [{"type": "text", "text": m["content"]}]} for m in prompt]
        ptxt = processor.apply_chat_template(text_only, tokenize=False, add_generation_prompt=True)
        ntok = len(processor.tokenizer(ptxt).input_ids)
        f_line = llm[2 + 3 * (i - 1)]
        ck["l1_prompt_tokens"] = {"reproduced": ntok, "recorded": int(f_line.group(2)), "ok": ntok == int(f_line.group(2))}
        sec["l1_prompt"] = prompt
        sec["l1_prompt_tokens"] = ntok
        sec["l1_log"] = {"prompt": int(f_line.group(2)), "completion": int(f_line.group(3)),
                         "finish": f_line.group(4), "sec": float(f_line.group(5))}
        # semantic
        sem_lists = [ret.semantic.retrieve(q, top_k=int(rr["semantic_k_per_query"]), as_context=False) for q in tq]
        sem = S.rrf_merge(sem_lists, key=lambda e: e.id, k=rrf_k)[:int(rr["semantic_k"])]
        rec_sem = [t for t in s["retrieved_texts"] if t["source"] == "worldmm-semantic"]
        same_ids = [f"{vid}:semantic:{e.id}" for e, _ in sem] == [t["uid"] for t in rec_sem]
        same_sc = same_ids and all(abs(round(sc, 6) - t["score"]) < 1e-6 for (e, sc), t in zip(sem, rec_sem))
        ck["semantic"] = {"reproduced": [e.id for e, _ in sem], "recorded": [t["uid"].split(":semantic:")[1] for t in rec_sem],
                          "ok": bool(same_sc)}
        sec["semantic_per_query"] = [{"query": q, "results": [{"id": e.id, "triple": e.triple} for e in lst]}
                                     for q, lst in zip(tq, sem_lists)]
        sec["semantic_rrf"] = [{"id": e.id, "triple": e.triple, "rrf": round(sc, 6)} for e, sc in sem]
        # visual: full similarity ranking per query (top 10 kept)
        vis = []
        for q in iq:
            q_emb = emb.encode_vis_query(q).reshape(1, -1)
            qt = torch.tensor(q_emb, dtype=torch.float32, device=ret.visual.embeddings.device)
            sims = torch.nn.functional.cosine_similarity(qt, ret.visual.embeddings, dim=1)
            order = torch.argsort(sims, descending=True)[:10].tolist()
            vis.append({"query": q, "top10": [{"start_time": ret.visual.indexed_entries[j].start_time,
                                               "end_time": ret.visual.indexed_entries[j].end_time,
                                               "cosine": round(float(sims[j]), 4)} for j in order]})
        rec_img = [m["start_time"] for m in s["retrieved_images"]]
        clips = ret.search_visual(iq, min(int(rr["image_k"]), int(cfg["report"]["image_topk"])))
        ck["visual"] = {"reproduced": [c.start_time for c, _ in clips], "recorded": rec_img,
                        "ok": [c.start_time for c, _ in clips] == rec_img}
        sec["visual"] = vis
        sec["text_match"] = ck["candidates"]["ok"] and ck["episodic_rrf"]["ok"] and ck["l1_prompt_tokens"]["ok"]
        sec["semantic_match"] = ck["semantic"]["ok"]
        sec["visual_match"] = ck["visual"]["ok"]
        out["sections"].append(sec)
        print(f"section {i}: text {'OK' if sec['text_match'] else 'MISMATCH'} {json.dumps({k: v['ok'] for k, v in ck.items()})}", flush=True)

    ret.release()
    assert tree_md5(real_cache) == md5_before, "real episodic cache changed"
    out["real_cache_md5_unchanged"] = md5_before
    p = os.path.join(RF, "analysis", f"retrieval_repro_{vid}_r{a.repeat}.json")
    json.dump(out, open(p, "w"), ensure_ascii=False, indent=1)
    print("wrote", p)


def _tt(ts):
    """worldmm.memory.episodic.memory._transform_timestamp"""
    return f"DAY{ts[0]} {ts[1:3]}:{ts[3:5]}:{ts[5:7]}"


if __name__ == "__main__":
    main()
