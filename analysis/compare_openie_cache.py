"""
C-2: compare HippoRAG OpenIE caches before/after the long-passage split + output guards (read-only, no GPU).
  - per cache file: chunks, empty triples/entities, triples per chunk, longest run of the same (subject, predicate)
    (consecutive) and the largest count of one (subject, predicate) inside a chunk
  - per chunk present in both files: triples before/after and Jaccard of the normalized triple sets
Default set: video 1 10min (split target, baseline = backup before the split), video 2 10sec/30sec/3min
(not split targets: re-computation vs. backup = sampling variance), and the new-only caches (video 2 10min, video 3).
Usage: python analysis/compare_openie_cache.py [--out results/c2_openie_compare.json]
"""
import argparse, json, os, statistics, sys
from collections import Counter

RF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RF)
from rf_config import load_config  # noqa: E402
CACHE = load_config(os.path.join(RF, "config.yaml"))["paths"]["episodic_cache_root"]
BACKUP = os.path.join(RF, "backups", "cache_before_split_20261022")
NAME = "openie_results_ner_qwen3vl-8b.json"
RUN_CUT = 15   # prebuild_episodic_index.MAX_SAME_SUBJ_PRED_RUN


def load(path):
    return {d["idx"]: d for d in json.load(open(path))["docs"]}


def norm(t):
    return tuple(str(x).strip().lower() for x in t)


def max_run(triples):
    run = best = 0
    for i, t in enumerate(triples):
        run = run + 1 if i and norm(t)[:2] == norm(triples[i - 1])[:2] else 1
        best = max(best, run)
    return best


def stats(docs):
    n = [len(d["extracted_triples"]) for d in docs.values()]
    runs = [max_run(d["extracted_triples"]) for d in docs.values()]
    same = [max(Counter(norm(t)[:2] for t in d["extracted_triples"]).values(), default=0) for d in docs.values()]
    return {"chunks": len(docs),
            "empty_triples": sum(1 for x in n if x == 0),
            "empty_entities": sum(1 for d in docs.values() if not d["extracted_entities"]),
            "triples_total": sum(n), "triples_mean": round(statistics.mean(n), 1), "triples_median": statistics.median(n),
            "triples_max": max(n), "max_run": max(runs), "chunks_run_eq_cut": sum(1 for r in runs if r == RUN_CUT),
            "chunks_run_gt_cut": sum(1 for r in runs if r > RUN_CUT), "max_same_subj_pred_in_chunk": max(same)}


def compare(before, after):
    common = sorted(set(before) & set(after))
    rows = []
    for k in common:
        b, a = before[k]["extracted_triples"], after[k]["extracted_triples"]
        sb, sa = set(map(norm, b)), set(map(norm, a))
        rows.append({"idx": k, "passage_same": before[k]["passage"] == after[k]["passage"], "triples_before": len(b),
                     "triples_after": len(a), "run_before": max_run(b), "run_after": max_run(a),
                     "jaccard": round(len(sb & sa) / len(sb | sa), 3) if sb | sa else 1.0})
    identical = sum(1 for r in rows if r["jaccard"] == 1.0)
    return {"common": len(common), "only_before": len(set(before) - set(after)), "only_after": len(set(after) - set(before)),
            "identical_chunks": identical, "jaccard_mean": round(statistics.mean(r["jaccard"] for r in rows), 3) if rows else None,
            "rows": rows}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(RF, "results", "c2_openie_compare.json"))
    args = ap.parse_args()
    cur = lambda v, g: os.path.join(CACHE, v, "episodic_memory", g, NAME)
    result = {"pairs": {}, "new_only": {}}
    pairs = [("-QuCz7kxBr8/10min", os.path.join(BACKUP, "-QuCz7kxBr8_10min", NAME), cur("-QuCz7kxBr8", "10min"))]
    pairs += [(f"0RxMZBLeqRI/{g}", os.path.join(BACKUP, "0RxMZBLeqRI", f"{g}.{NAME}"), cur("0RxMZBLeqRI", g))
              for g in ("10sec", "30sec", "3min")]
    for label, b, a in pairs:
        before, after = load(b), load(a)
        result["pairs"][label] = {"before": stats(before), "after": stats(after), "compare": compare(before, after)}
    for v in ("-QuCz7kxBr8", "0RxMZBLeqRI", "54k2g9ddy4M"):
        for g in ("10sec", "30sec", "3min", "10min"):
            result["new_only"][f"{v}/{g}"] = stats(load(cur(v, g)))
    json.dump(result, open(args.out, "w"), indent=1, ensure_ascii=False)
    keys = ["chunks", "empty_triples", "empty_entities", "triples_total", "triples_mean", "triples_max", "max_run",
            "chunks_run_eq_cut", "chunks_run_gt_cut", "max_same_subj_pred_in_chunk"]
    print("label".ljust(26), " ".join(k[:12].rjust(12) for k in keys))
    for label, r in result["pairs"].items():
        for side in ("before", "after"):
            print(f"{label} {side}".ljust(26), " ".join(str(r[side][k]).rjust(12) for k in keys))
        c = r["compare"]
        print(f"  common={c['common']} only_before={c['only_before']} only_after={c['only_after']} "
              f"identical={c['identical_chunks']} jaccard_mean={c['jaccard_mean']}")
    for label, s in result["new_only"].items():
        print(label.ljust(26), " ".join(str(s[k]).rjust(12) for k in keys))
    print("saved", args.out)


if __name__ == "__main__":
    main()
