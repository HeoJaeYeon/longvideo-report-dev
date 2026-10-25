#!/usr/bin/env python3
"""
Read-only analysis of one generated report for decision 4 (repetition) and decision 7
(evidence composition). Input: the Deep-Reporter outline (list of sections with `content`,
`retrieved_texts`, `retrieved_images`), e.g. tests/_artifacts/gpu_report/outline.json or
report.json["outline"] from run_report.py. Optional: local_llm_server log for token counts.

  python analysis/analyze_report.py --outline <outline.json|report.json> [--server-log <log>] [--out <metrics.json>]

Decision 4 metrics: paragraph similarity within sections (all pairs), near-duplicate sentences
within / across sections, repeated word 8-grams, evidence reused across sections, LLM finish reasons.
Decision 7 metrics: citations by memory type and by retrieval rank, unused evidence, grounding
findings by cited memory type, semantic triples (all, with cited flag), image time vs. the
section's cited episodic times, evidence size per type.
"""

import argparse
import difflib
import itertools
import json
import os
import re
import sys
from collections import Counter, defaultdict
from typing import Any, Dict, List

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
import grounding_postprocessor as G  # noqa: E402

WORD_RE = re.compile(r"[a-z0-9']+")


def norm_words(text: str) -> List[str]:
    return WORD_RE.findall(G.CITE_GROUP_RE.sub(" ", G.IMG_EMBED_RE.sub(" ", text or "")).lower())


def ratio(a: str, b: str) -> float:
    return difflib.SequenceMatcher(None, " ".join(norm_words(a)), " ".join(norm_words(b))).ratio()


def paragraphs(content: str) -> List[str]:
    out = []
    for p in re.split(r"\n\s*\n", content or ""):
        lines = [l for l in p.split("\n") if l.strip() and not l.lstrip().startswith("#")
                 and not G.IMG_EMBED_RE.fullmatch(l.strip())]
        if lines and len(norm_words(" ".join(lines))) >= 5:
            out.append(" ".join(l.strip() for l in lines))
    return out


def load_outline(path: str) -> List[Dict[str, Any]]:
    data = json.load(open(path, encoding="utf-8"))
    return data["outline"] if isinstance(data, dict) else data


def repetition_metrics(outline: List[Dict[str, Any]]) -> Dict[str, Any]:
    sections, all_pairs, sentences = [], [], []
    for i, s in enumerate(outline, 1):
        paras = paragraphs(s.get("content", ""))
        pairs = sorted(((round(ratio(a, b), 3), x + 1, y + 1) for (x, a), (y, b)
                        in itertools.combinations(enumerate(paras), 2)), reverse=True)
        all_pairs += [(r, i, x, y) for r, x, y in pairs]
        sents = [t for t in G.split_sentences(s.get("content", "")) if len(norm_words(t)) >= 6]
        sentences += [(i, t) for t in sents]
        near = [(round(ratio(a, b), 3)) for a, b in itertools.combinations(sents, 2) if ratio(a, b) >= 0.8]
        words = norm_words(s.get("content", ""))
        grams = Counter(tuple(words[k:k + 8]) for k in range(len(words) - 7))
        repeated = sum(c for c in grams.values() if c > 1)
        sections.append({"section": i, "paragraphs": len(paras), "words": len(words),
                         "top_paragraph_pairs": [{"ratio": r, "p": x, "q": y} for r, x, y in pairs[:3]],
                         "near_duplicate_sentence_pairs": len(near),
                         "repeated_8gram_share": round(repeated / max(sum(grams.values()), 1), 3)})
    cross = []
    for (i, a), (j, b) in itertools.combinations(sentences, 2):
        if i != j:
            r = ratio(a, b)
            if r >= 0.7:
                cross.append({"ratio": round(r, 3), "sections": [i, j], "a": a[:160], "b": b[:160]})
    cross.sort(key=lambda x: -x["ratio"])
    uid_sections = defaultdict(set)
    for i, s in enumerate(outline, 1):
        for item in (s.get("retrieved_texts") or []) + (s.get("retrieved_images") or []):
            uid_sections[item.get("uid")].add(i)
    reused = {u: sorted(v) for u, v in uid_sections.items() if u and len(v) > 1}
    dist = sorted(r for r, *_ in all_pairs)
    return {"sections": sections, "within_section_paragraph_pairs": len(all_pairs),
            "paragraph_ratio_quantiles": {q: dist[min(int(q * len(dist)), len(dist) - 1)] for q in (0.5, 0.9, 0.99)} if dist else {},
            "paragraph_pairs_ge": {t: sum(r >= t for r in dist) for t in (0.5, 0.6, 0.7, 0.8)},
            "top_paragraph_pairs": [{"ratio": r, "section": i, "p": x, "q": y} for r, i, x, y in sorted(all_pairs, reverse=True)[:5]],
            "cross_section_similar_sentences": cross[:10], "cross_section_similar_sentence_count": len(cross),
            "evidence_reused_across_sections": len(reused), "evidence_items_total": len(uid_sections)}


def composition_metrics(outline: List[Dict[str, Any]]) -> Dict[str, Any]:
    by_type = defaultdict(lambda: {"retrieved": 0, "cited_items": 0, "citations": 0})
    by_rank = defaultdict(lambda: [0, 0])          # (type, rank) -> [retrieved, cited]
    findings_by_type, semantic, images, sizes = Counter(), [], [], defaultdict(list)
    for i, s in enumerate(outline, 1):
        content = s.get("content") or ""
        texts, imgs = s.get("retrieved_texts") or [], s.get("retrieved_images") or []
        cites = Counter()
        for g in G.CITE_GROUP_RE.findall(content):
            for kind, idx in G.parse_tokens(g)[0]:
                cites[(kind, idx)] += 1
        for idx in G.IMG_EMBED_RE.findall(content):
            cites[("img", int(idx))] += 1
        for kind, items in (("txt", texts), ("img", imgs)):
            for idx, item in enumerate(items, 1):
                t = {"worldmm-episodic": "episodic", "worldmm-semantic": "semantic"}.get(item.get("source"), "image")
                n = cites[(kind, idx)]
                by_type[t]["retrieved"] += 1
                by_type[t]["cited_items"] += int(n > 0)
                by_type[t]["citations"] += n
                rank = item.get("rank", idx)
                by_rank[(t, rank)][0] += 1
                by_rank[(t, rank)][1] += int(n > 0)
                sizes[t].append(len((item.get("content") or item.get("caption") or "").split()))
                if t == "semantic":
                    semantic.append({"section": i, "triple": item.get("triple"), "cited": n > 0})
        cited_times = [(float(t["start_sec"]), float(t["end_sec"])) for idx, t in enumerate(texts, 1)
                       if t.get("start_sec") is not None and cites[("txt", idx)] > 0]
        for idx, m in enumerate(imgs, 1):
            f = float(m.get("frame_sec") or 0)
            gap = min((0 if a <= f <= b else min(abs(f - a), abs(f - b)) for a, b in cited_times), default=None)
            images.append({"section": i, "frame": G.hms(f), "cited": cites[("img", idx)] > 0,
                           "gap_to_nearest_cited_episodic_sec": gap})
        gr = G.check_section_grounding(content, texts, imgs)
        for f in gr["findings"]:
            if f["status"] in ("unsupported", "miscited"):
                for c in f["cited"]:
                    kind, idx = c[:3], int(c[3:])
                    item = (texts if kind == "txt" else imgs)[idx - 1]
                    findings_by_type[{"worldmm-episodic": "episodic", "worldmm-semantic": "semantic"}.get(item.get("source"), "image")] += 1
    return {"by_type": dict(by_type),
            "by_rank": {f"{t}#{r}": {"retrieved": v[0], "cited": v[1]} for (t, r), v in sorted(by_rank.items())},
            "findings_by_cited_type": dict(findings_by_type),
            "semantic_triples": semantic, "images": images,
            "evidence_words": {t: {"items": len(v), "mean": round(sum(v) / len(v), 1), "max": max(v)} for t, v in sizes.items()}}


def server_log_metrics(path: str) -> List[Dict[str, Any]]:
    out = []
    for line in open(path, encoding="utf-8", errors="ignore"):
        m = re.search(r"prompt=(\d+) completion=(\d+) finish=(\w+) ([\d.]+)s", line)
        if m:
            out.append({"prompt": int(m.group(1)), "completion": int(m.group(2)), "finish": m.group(3), "sec": float(m.group(4))})
    return out


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__.split("\n")[1])
    ap.add_argument("--outline", required=True)
    ap.add_argument("--server-log", default=None)
    ap.add_argument("--out", default=None)
    a = ap.parse_args()
    outline = load_outline(a.outline)
    result = {"repetition": repetition_metrics(outline), "composition": composition_metrics(outline)}
    if a.server_log:
        result["llm_calls"] = server_log_metrics(a.server_log)
    text = json.dumps(result, indent=2, ensure_ascii=False)
    if a.out:
        os.makedirs(os.path.dirname(os.path.abspath(a.out)), exist_ok=True)
        open(a.out, "w", encoding="utf-8").write(text)
    print(text)


if __name__ == "__main__":
    main()
