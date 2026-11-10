"""
Where do repeated runs (same video, same settings, r1-r3) start to differ, and how does the difference propagate?
Read-only, CPU only (2026-10-26). Input: outputs/p9p19_check_20261025_141401 (report.json + Deep-Reporter session logs).
  planner : is the planner prompt byte-identical across runs; common prefix of the planner outputs (first divergence)
  stages  : for the first section (same topic in every run) and the conclusion section, pairwise similarity at each
            stage: plan (description + checklist, TF-IDF cosine), text queries (TF-IDF cosine), retrieved / cited
            episodic evidence (Jaccard), written body (TF-IDF cosine, citations removed)
  concl   : conclusion checklist and queries, to see which earlier content they follow
Usage: python analysis/divergence_trace.py [--out results/divergence_trace_20261026.json]
"""
import argparse, glob, hashlib, itertools, json, os, re, sys

RF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RF)
import grounding_postprocessor as G

RUN_DIR = os.path.join(RF, "outputs", "p9p19_check_20261025_141401")
VIDEOS = ["-QuCz7kxBr8", "0RxMZBLeqRI", "54k2g9ddy4M"]


def jaccard(a, b):
    a, b = set(a), set(b)
    return round(len(a & b) / len(a | b), 3) if a | b else None


def common_prefix(a, b):
    n = 0
    for x, y in zip(a, b):
        if x != y:
            break
        n += 1
    return n


def episodic_uids(section, cited_only):
    texts = section.get("retrieved_texts") or []
    if not cited_only:
        return [t["uid"] for t in texts if ":episodic:" in t["uid"]]
    idx = {i for g in G.CITE_GROUP_RE.findall(section.get("content") or "") for k, i in G.parse_tokens(g)[0] if k == "txt"}
    return [texts[i - 1]["uid"] for i in idx if 1 <= i <= len(texts) and ":episodic:" in texts[i - 1]["uid"]]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(RF, "results", "divergence_trace_20261026.json"))
    a = ap.parse_args()
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    sessions = {}
    for p in glob.glob(os.path.join(RUN_DIR, "dr_logs_s*", "*.jsonl")):
        for line in open(p):
            d = json.loads(line)
            sessions[d["session_id"]] = d
    result = {}
    for vid in VIDEOS:
        reps = [json.load(open(os.path.join(RUN_DIR, f"{vid}__c0_written__r{r}", "report.json"))) for r in (1, 2, 3)]
        ses = [sessions[r["session_id"]] for r in reps]
        p_in = [s["llm_calls"][0]["input_messages"][0]["content"] for s in ses]
        p_out = [s["llm_calls"][0]["output_content"] for s in ses]
        planner = {"input_md5": [hashlib.md5(x.encode()).hexdigest() for x in p_in],
                   "input_identical": len(set(p_in)) == 1, "output_chars": [len(x) for x in p_out], "first_divergence": {}}
        for i, j in itertools.combinations(range(3), 2):
            n = common_prefix(p_out[i], p_out[j])
            planner["first_divergence"][f"r{i + 1}-r{j + 1}"] = {
                "common_prefix_chars": n, "context": p_out[i][max(0, n - 60):n],
                f"r{i + 1}": p_out[i][n:n + 40], f"r{j + 1}": p_out[j][n:n + 40]}
        stages = {}
        for label, k in (("first_section", 0), ("conclusion", -1)):
            secs = [r["outline"][k] for r in reps]
            plans = [s["section_description"] + " " + " ".join(s["sectional_checklist"]) for s in secs]
            queries = [" ".join(s["text_queries"] or []) for s in secs]
            bodies = [G.CITE_GROUP_RE.sub(" ", s.get("content") or "") for s in secs]
            vec = TfidfVectorizer(stop_words="english").fit(plans + queries + bodies)
            def cos(docs, i, j):
                return round(float(cosine_similarity(vec.transform([docs[i], docs[j]]))[0, 1]), 3)
            stages[label] = {f"r{i + 1}-r{j + 1}": {
                "plan": cos(plans, i, j), "queries": cos(queries, i, j),
                "retrieved_episodic": jaccard(episodic_uids(secs[i], False), episodic_uids(secs[j], False)),
                "cited_episodic": jaccard(episodic_uids(secs[i], True), episodic_uids(secs[j], True)),
                "body": cos(bodies, i, j)} for i, j in itertools.combinations(range(3), 2)}
        concl = [{"run": n, "checklist": r["outline"][-1]["sectional_checklist"], "text_queries": r["outline"][-1]["text_queries"],
                  "earlier_section_titles": [next((ln.lstrip("#").strip() for ln in (s.get("content") or "").split("\n")
                                                   if ln.startswith("#")), "")[:90] for s in r["outline"][:-1]]}
                 for n, r in enumerate(reps, 1)]
        result[vid] = {"planner": planner, "stages": stages, "conclusion": concl}
        print("=" * 10, vid, "planner input identical:", planner["input_identical"])
        for k, v in planner["first_divergence"].items():
            print(f"  {k}: same first {v['common_prefix_chars']} chars")
        for label, pairs in stages.items():
            for k, v in pairs.items():
                print(f"  {label:13} {k} {v}")
    json.dump(result, open(a.out, "w"), indent=1, ensure_ascii=False)
    print("saved", a.out)


if __name__ == "__main__":
    main()
