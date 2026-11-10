"""
Read-only self-consistency analysis of repeated reports (same video, same settings, runs r1-r3) (2026-10-26).
Input: outputs/p9p19_check_20261025_141401/<vid>__c0_written__r{1,2,3}/report.json (+ validation.json), WorldMM captions.
For each video, pairwise over the 3 runs:
  outline   : section count, cited-evidence position (median midpoint) per section
  retrieval : Jaccard of retrieved / cited evidence uids (episodic, semantic, image)
  coverage  : 10-second bins of the video covered by cited episodic evidence (fine = 10sec/30sec/3min only, all = +10min)
              and 3-minute windows whose cited fine evidence midpoint falls inside (which runs cover each window)
  text      : TF-IDF cosine of whole reports and of conclusions (cross-video pairs as a reference floor)
  claims    : quoted strings, numbers, HH:MM:SS, capitalized names in the body (citations removed); how many runs
              state each one (1/2/3) and whether it occurs anywhere in the video's captions (all 4 granularities) or in
              any semantic evidence retrieved for that video ("supported"). Times are only counted, not checked.
              Note: "supported" is video-wide and turned out non-discriminative (almost every token occurs somewhere).
Report bodies are taken from report.json (repeated sentences already removed by run_report).
Usage: python analysis/self_consistency_check.py [--out results/self_consistency_20261026.json]
"""
import argparse, itertools, json, os, re, statistics, sys

RF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RF)
import grounding_postprocessor as G
from rf_config import load_config

RUN_DIR = os.path.join(RF, "outputs", "p9p19_check_20261025_141401")
CAPTIONS = load_config(os.path.join(RF, "config.yaml"))["paths"]["caption_dir"]
VIDEOS = ["-QuCz7kxBr8", "0RxMZBLeqRI", "54k2g9ddy4M"]
RUNS = (1, 2, 3)
NAME_RE = re.compile(r"(?<![.!?]\s)(?<!^)\b([A-Z][a-zA-Z’'\-]+(?:\s+(?:[A-Z][a-zA-Z’'\-]+|of|the|de|des))*\s*[A-Z]?[a-zA-Z’'\-]*)")
NAME_STOP = {"The", "This", "A", "An", "At", "In", "On", "As", "It", "He", "She", "They", "His", "Her", "Their", "One",
             "Two", "Three", "Four", "Five", "Six", "Section", "Conclusion", "Video", "After", "Before", "While", "During",
             "Later", "Then", "Finally", "Meanwhile", "Throughout", "Following", "Overall", "Together", "Each", "Both",
             "These", "Those", "Its", "Another", "Other", "Some", "From", "With", "By", "For", "Despite", "Although",
             "However", "Earlier", "Next", "When", "Once", "Here", "There", "Such", "No", "Not", "I", "We", "You"}


def jaccard(a, b):
    a, b = set(a), set(b)
    return round(len(a & b) / len(a | b), 3) if a | b else None


def load(vid, r):
    d = os.path.join(RUN_DIR, f"{vid}__c0_written__r{r}")
    return json.load(open(os.path.join(d, "report.json"))), json.load(open(os.path.join(d, "validation.json")))


def cited_idx(content):
    return sorted({i for g in G.CITE_GROUP_RE.findall(content) for kind, i in G.parse_tokens(g)[0] if kind == "txt"})


def cited_img(content):
    idx = {int(i) for i in G.IMG_EMBED_RE.findall(content)}
    idx |= {i for g in G.CITE_GROUP_RE.findall(content) for kind, i in G.parse_tokens(g)[0] if kind == "img"}
    return sorted(idx)


def body_text(content):
    lines = [ln for ln in content.split("\n") if ln.strip() and not ln.lstrip().startswith("#")]
    text = G.IMG_EMBED_RE.sub(" ", "\n".join(lines))
    return re.sub(r"\s+", " ", G.CITE_GROUP_RE.sub(" ", text)).strip()


def claims(text):
    out = set()
    for q in G.QUOTE_RE.findall(text):
        q = q.strip(" .,;:!?")
        if len(G.normalize(q)) >= 2:
            out.add(("quote", G.normalize(q)))
    rest = G.QUOTE_RE.sub(" ", text)
    out |= {("time", t) for t in G.TIMESTAMP_RE.findall(rest)}
    out |= {("number", n) for n in G.number_tokens(rest)}
    for sentence in re.split(r"(?<=[.!?])\s+", rest):
        words = sentence.split(" ", 1)
        tail = words[1] if len(words) > 1 else ""
        for m in re.finditer(r"\b[A-Z][a-zA-Z’'\-]+(?:\s+[A-Z][a-zA-Z’'\-]+)*", tail):
            name = m.group(0)
            if name.split()[0] in NAME_STOP or len(name) < 3:
                continue
            out.add(("name", name.replace("’", "'")))
    return out


def supported(kind, token, corpus, corpus_norm):
    if kind == "quote":
        return token in corpus_norm or G.quote_supported(token, corpus)
    if kind == "number":
        return G.number_supported(token, corpus)
    if kind == "name":
        return token.lower() in corpus.lower().replace("’", "'")
    return None


def video_corpus(vid, reports):
    texts = []
    for g in ("10sec", "30sec", "3min", "10min"):
        texts += [str(e.get("text", "")) for e in json.load(open(os.path.join(CAPTIONS, vid, f"{g}.json")))]
    for rj, _ in reports:
        for s in rj["outline"]:
            texts += [t.get("content", "") for t in s.get("retrieved_texts") or [] if t.get("source") == "worldmm-semantic"]
    corpus = "\n".join(texts)
    return corpus, G.normalize(corpus)


def video_end(vid):
    e = json.load(open(os.path.join(CAPTIONS, vid, "10sec.json")))
    t = str(e[-1]["end_time"]).zfill(8)
    return int(t[0:2]) * 3600 + int(t[2:4]) * 60 + int(t[4:6])


def bins(intervals, end):
    out = set()
    for a, b in intervals:
        out |= set(range(int(a) // 10, min(int(b), end) // 10 + (1 if int(b) % 10 else 0)))
    return out


def analyze_video(vid, tfidf_all):
    reports = [load(vid, r) for r in RUNS]
    end = video_end(vid)
    corpus, corpus_norm = video_corpus(vid, reports)
    runs = []
    for r, (rj, vj) in zip(RUNS, reports):
        sections, retrieved, cited, images, cited_images = [], set(), set(), set(), set()
        fine_iv, all_iv = [], []
        for i, s in enumerate(rj["outline"], 1):
            content = s.get("content") or ""
            texts, imgs = s.get("retrieved_texts") or [], s.get("retrieved_images") or []
            idx = [k for k in cited_idx(content) if 1 <= k <= len(texts)]
            retrieved |= {t["uid"] for t in texts}
            cited |= {texts[k - 1]["uid"] for k in idx}
            images |= {m["uid"] for m in imgs}
            cited_images |= {imgs[k - 1]["uid"] for k in cited_img(content) if 1 <= k <= len(imgs)}
            timed = [texts[k - 1] for k in idx if texts[k - 1].get("start_sec") is not None]
            all_iv += [(t["start_sec"], t["end_sec"]) for t in timed]
            fine_iv += [(t["start_sec"], t["end_sec"]) for t in timed if t.get("granularity") != "10min"]
            mids = [(t["start_sec"] + t["end_sec"]) / 2 for t in timed]
            title = next((ln.lstrip("#").strip() for ln in content.split("\n") if ln.startswith("#")), "")
            sections.append({"index": i, "title": title[:100], "words": len(content.split()),
                             "position": G.hms(statistics.median(mids)) if mids else None,
                             "position_sec": statistics.median(mids) if mids else None})
        windows = sorted({int((a + b) / 2) // 180 for a, b in fine_iv})
        text = body_text("\n\n".join(s.get("content") or "" for s in rj["outline"]))
        concl = body_text(rj["outline"][-1].get("content") or "")
        runs.append({"run": r, "sections": sections, "retrieved": retrieved, "cited": cited, "images": images,
                     "cited_images": cited_images, "windows_3min": windows, "fine_bins": bins(fine_iv, end), "all_bins": bins(all_iv, end),
                     "text": text, "conclusion": concl, "claims": claims(text),
                     "validation": {"generation_sec": vj["timings"]["generation_sec"],
                                    "grounding": vj["grounding_stats"],
                                    "removed_sentences": sum(x["removed_sentences"] for x in vj["repetition"]),
                                    "cut_sections": [x["index"] for x in vj["repetition"] if x["ends_mid_sentence"]],
                                    "boundary": [f["status"] for f in vj["boundary_findings"]]}})
        tfidf_all.append((vid, r, text, concl))

    def kind_of(uid):
        return uid.split(":")[1]
    pairs = {}
    for a, b in itertools.combinations(runs, 2):
        key = f"r{a['run']}-r{b['run']}"
        pairs[key] = {
            "retrieved_episodic": jaccard({u for u in a["retrieved"] if kind_of(u) == "episodic"},
                                          {u for u in b["retrieved"] if kind_of(u) == "episodic"}),
            "retrieved_semantic": jaccard({u for u in a["retrieved"] if kind_of(u) == "semantic"},
                                          {u for u in b["retrieved"] if kind_of(u) == "semantic"}),
            "cited_episodic": jaccard({u for u in a["cited"] if kind_of(u) == "episodic"},
                                      {u for u in b["cited"] if kind_of(u) == "episodic"}),
            "retrieved_images": jaccard(a["images"], b["images"]),
            "cited_images": jaccard(a["cited_images"], b["cited_images"]),
            "coverage_fine": jaccard(a["fine_bins"], b["fine_bins"]),
            "coverage_all": jaccard(a["all_bins"], b["all_bins"]),
            "claims": jaccard(a["claims"], b["claims"]),
        }
    nbins = end // 10 + 1
    fine_counts = [sum(b in r["fine_bins"] for r in runs) for b in range(nbins)]
    coverage = {f"runs_{k}": round(sum(c == k for c in fine_counts) / nbins, 3) for k in (0, 1, 2, 3)}
    coverage["per_run_fine"] = [round(len(r["fine_bins"]) / nbins, 3) for r in runs]
    coverage["per_run_all"] = [round(len(r["all_bins"]) / nbins, 3) for r in runs]
    # 3-minute windows (WorldMM 3min caption spans) whose cited 10sec/30sec/3min evidence midpoint falls inside
    nwin = (end - 1) // 180 + 1
    win_counts = [sum(w in r["windows_3min"] for r in runs) for w in range(nwin)]
    coverage["windows_3min"] = {"total": nwin, "per_run": [len(r["windows_3min"]) for r in runs],
                                "covered_by_runs": {str(k): sum(c == k for c in win_counts) for k in (0, 1, 2, 3)},
                                "per_window": {G.hms(w * 180): [r["run"] for r in runs if w in r["windows_3min"]]
                                               for w in range(nwin)}}
    # claim agreement and support
    by_claim = {}
    for r in runs:
        for c in r["claims"]:
            by_claim.setdefault(c, set()).add(r["run"])
    table = {}
    for (kind, token), rs in by_claim.items():
        n = len(rs)
        sup = supported(kind, token, corpus, corpus_norm)
        t = table.setdefault(kind, {1: [0, 0], 2: [0, 0], 3: [0, 0]})
        if sup is not None:
            t[n][0] += 1
            t[n][1] += int(sup)
        else:
            t[n][0] += 1
    claim_table = {k: {f"in_{n}_runs": {"claims": v[n][0], "supported": (v[n][1] if k != "time" else None)}
                       for n in (1, 2, 3)} for k, v in table.items()}
    unique = {f"r{r['run']}": sorted([f"{k}:{t}" for (k, t) in r["claims"] if len(by_claim[(k, t)]) == 1
                                      and k != "time" and supported(k, t, corpus, corpus_norm) is False])[:60]
              for r in runs}
    return {"video": vid, "video_end": G.hms(end),
            "runs": [{"run": r["run"], "sections": r["sections"], "n_claims": len(r["claims"]),
                      "retrieved_uids": len(r["retrieved"]), "cited_uids": len(r["cited"]),
                      "validation": r["validation"]} for r in runs],
            "pairs": pairs, "coverage": coverage, "claims": claim_table,
            "unsupported_unique_claims": unique,
            "conclusions": {f"r{r['run']}": r["conclusion"] for r in runs}}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(RF, "results", "self_consistency_20261026.json"))
    a = ap.parse_args()
    tfidf_all = []
    result = {v: analyze_video(v, tfidf_all) for v in VIDEOS}
    from sklearn.feature_extraction.text import TfidfVectorizer
    from sklearn.metrics.pairwise import cosine_similarity
    for field, pos in (("text", 2), ("conclusion", 3)):
        m = TfidfVectorizer(stop_words="english").fit_transform([x[pos] for x in tfidf_all])
        sim = cosine_similarity(m)
        cross = []
        for i, j in itertools.combinations(range(len(tfidf_all)), 2):
            vi, ri = tfidf_all[i][:2]
            vj, rj = tfidf_all[j][:2]
            if vi == vj:
                result[vi]["pairs"][f"r{ri}-r{rj}"][f"tfidf_{field}"] = round(float(sim[i, j]), 3)
            else:
                cross.append(float(sim[i, j]))
        result.setdefault("_cross_video", {})[f"tfidf_{field}"] = {"min": round(min(cross), 3), "max": round(max(cross), 3),
                                                                  "mean": round(statistics.mean(cross), 3)}
    json.dump(result, open(a.out, "w"), indent=1, ensure_ascii=False)
    for v in VIDEOS:
        r = result[v]
        print("=" * 20, v, "end", r["video_end"])
        for x in r["runs"]:
            print(f" r{x['run']}", [(s["position"], s["title"][:40]) for s in x["sections"]])
        for k, p in r["pairs"].items():
            print(" ", k, p)
        print("  coverage", r["coverage"])
        print("  claims", json.dumps(r["claims"]))
    print("cross-video", result["_cross_video"])
    print("saved", a.out)


if __name__ == "__main__":
    main()
