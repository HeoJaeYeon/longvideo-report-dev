"""
Read-only measurement of report flow errors and speculative/interpretive wording (2026-10-26).
Each report's section bodies are first passed through grounding_postprocessor.dedupe_repeated_sentences, so
reports made before the P9 fix (which still contain repetition loops) are measured the same way as later ones.
Checks (candidates; precision must be checked by hand):
  F1 section order: median cited episodic evidence midpoint per non-conclusion section; a section whose
     position is more than TOL_SEC before the previous section's is an inversion
  F2 in-section time order: explicit HH:MM:SS in the body, in text order; a jump back of more than TOL_SEC
  F3 conclusion counts: "<number> <people/team noun>" in the conclusion vs a different number for the same noun
     in earlier sections
  S  wording: hedge / interpretive / evaluative cue words per sentence; whether the same cue appears in the
     sentence's cited text evidence ("carried"), not ("added"), or the sentence cites nothing ("uncited")
Speaker attribution is not covered (needs semantic comparison).
Usage: python analysis/flow_speculation_check.py [--out results/flow_speculation_20261026.json]
"""
import argparse, glob, json, os, re, statistics, sys
from collections import Counter

RF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RF)
import grounding_postprocessor as G

TOL_SEC = 60
SETS = {
    "C-4": "outputs/c4_reports_20261025_130200/*__default__r1",
    "C-5 c0_written": "outputs/c5_c0_20261025_132851/*__c0_written__r*",
    "C-5 c0_off": "outputs/c5_c0_20261025_132851/*__c0_off__r*",
    "P9P19 c0_written": "outputs/p9p19_check_20261025_141401/*__c0_written__r*",
}
HMS_RE = re.compile(r"\b(\d{2}):(\d{2}):(\d{2})\b")
NUM = {"two": 2, "three": 3, "four": 4, "five": 5, "six": 6, "seven": 7, "eight": 8, "nine": 9, "ten": 10,
       "eleven": 11, "twelve": 12}
COUNT_RE = re.compile(r"\b(two|three|four|five|six|seven|eight|nine|ten|eleven|twelve|\d{1,2})\s+"
                      r"(?:[a-z-]+\s+)?(men|women|people|players|participants|teammates|teams|contestants|friends|"
                      r"hosts|boys|girls|guys|members|anchors|doctors)\b", re.I)
CUES = {
    "hedge": r"\b(?:possibly|possible|likely|perhaps|maybe|may|might|could|seemingly|apparently|presumably|"
             r"seems?|appears?\s+to|appearing\s+to)\b",
    "interpretive": r"\b(?:suggest(?:s|ing|ed)?|symboli[sz](?:e|es|ing|ed)|symbolic(?:ally)?|impl(?:y|ies|ying|ied)|"
                    r"reflect(?:s|ing|ed)?|convey(?:s|ing|ed)?|evok(?:e|es|ing|ed)|signal(?:s|ing|ed|ling|led)?|"
                    r"metaphor(?:ical)?|represent(?:s|ing|ed)?)\b",
    "evaluative": r"\b(?:underscor(?:e|es|ing|ed)|reinforc(?:e|es|ing|ed)|highlight(?:s|ing|ed)?|emphasi[sz](?:e|es|ing|ed)|"
                  r"powerful|poignant|striking|compelling|profound)\b",
}
CUE_RE = {k: re.compile(v, re.I) for k, v in CUES.items()}


def sec(x):
    try:
        return float(x)
    except (TypeError, ValueError):
        return None


def cited(sentence):
    return [i for g in G.CITE_GROUP_RE.findall(sentence) for kind, i in G.parse_tokens(g)[0] if kind == "txt"]


def section_position(content, texts):
    mids = []
    for i in cited(content):
        if 1 <= i <= len(texts):
            a, b = sec(texts[i - 1].get("start_sec")), sec(texts[i - 1].get("end_sec"))
            if a is not None and b is not None:
                mids.append((a + b) / 2)
    return statistics.median(mids) if mids else None


def analyze(path):
    r = json.load(open(os.path.join(path, "report.json")))
    outline = r["outline"]
    n = len(outline)
    rep = {"report": os.path.relpath(path, RF), "video": r["video_id"], "sections": n,
           "F1": [], "F2": [], "F3": [], "S": [], "sentences": 0}
    contents = [G.dedupe_repeated_sentences(s.get("content") or "")[0] for s in outline]
    positions = []
    for idx, (s, content) in enumerate(zip(outline, contents), 1):
        texts, _ = G.section_evidence(s, False)
        title = next((ln[2:].strip() for ln in content.split("\n") if ln.startswith("# ")), "")
        if idx < n:
            positions.append((idx, section_position(content, texts), title))
        last = None
        for sentence in G.split_sentences(content):
            rep["sentences"] += 1
            claim = G.CITE_GROUP_RE.sub(" ", sentence)
            for m in HMS_RE.finditer(claim):
                t = int(m.group(1)) * 3600 + int(m.group(2)) * 60 + int(m.group(3))
                if last is not None and t < last - TOL_SEC:
                    rep["F2"].append({"section": idx, "from": G.hms(last), "to": m.group(0), "sentence": sentence[:240]})
                last = t
            idxs = cited(sentence)
            ev = " ".join(str(texts[i - 1].get("text") or texts[i - 1].get("content") or "") for i in idxs if 1 <= i <= len(texts))
            for kind, rx in CUE_RE.items():
                for m in rx.finditer(claim):
                    word = m.group(0).lower()
                    # compare by stem (e.g. underscores ~ underscoring, reflecting ~ reflects)
                    stem = re.sub(r"(?:ing|ed|es|s|e)$", "", word.split()[0])[:7]
                    origin = "uncited" if not idxs else ("carried" if re.search(rf"\b{re.escape(stem)}", ev, re.I) else "added")
                    grans = sorted({texts[i - 1].get("granularity") or "semantic" for i in idxs if 1 <= i <= len(texts)
                                    and re.search(rf"\b{re.escape(stem)}", str(texts[i - 1].get("text") or ""), re.I)})
                    rep["S"].append({"section": idx, "kind": kind, "cue": word, "origin": origin, "sentence": sentence[:300],
                                     "cited": idxs, "cue_in_granularity": grans})
    known = [(i, p, t) for i, p, t in positions if p is not None]
    for (i0, p0, t0), (i1, p1, t1) in zip(known, known[1:]):
        if p1 < p0 - TOL_SEC:
            rep["F1"].append({"from_section": i0, "to_section": i1, "from_pos": G.hms(p0), "to_pos": G.hms(p1),
                              "from_title": t0[:90], "to_title": t1[:90]})
    earlier = {}
    for content in contents[:-1]:
        for m in COUNT_RE.finditer(G.CITE_GROUP_RE.sub(" ", content)):
            earlier.setdefault(m.group(2).lower(), set()).add(NUM.get(m.group(1).lower(), m.group(1)))
    for m in COUNT_RE.finditer(G.CITE_GROUP_RE.sub(" ", contents[-1])):
        noun, num = m.group(2).lower(), NUM.get(m.group(1).lower(), m.group(1))
        if noun in earlier and num not in earlier[noun]:
            rep["F3"].append({"noun": noun, "conclusion": num, "earlier": sorted(map(str, earlier[noun])), "phrase": m.group(0)})
    return rep


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", default=os.path.join(RF, "results", "flow_speculation_20261026.json"))
    a = ap.parse_args()
    result = {}
    for name, pattern in SETS.items():
        dirs = [d for d in sorted(glob.glob(os.path.join(RF, pattern))) if os.path.isdir(d)]
        result[name] = [analyze(d) for d in dirs]
    json.dump(result, open(a.out, "w"), indent=1, ensure_ascii=False)
    print(f"{'set':18} {'rep':>3} {'sent':>5} {'F1':>3} {'F2':>3} {'F3':>3} | S hedge/interp/eval | origin carried/added/uncited")
    for name, reps in result.items():
        s = [x for r in reps for x in r["S"]]
        kinds, origins = Counter(x["kind"] for x in s), Counter(x["origin"] for x in s)
        print(f"{name:18} {len(reps):>3} {sum(r['sentences'] for r in reps):>5} {sum(len(r['F1']) for r in reps):>3} "
              f"{sum(len(r['F2']) for r in reps):>3} {sum(len(r['F3']) for r in reps):>3} | "
              f"{kinds['hedge']}/{kinds['interpretive']}/{kinds['evaluative']} | "
              f"{origins['carried']}/{origins['added']}/{origins['uncited']}")
    print("saved", a.out)


if __name__ == "__main__":
    main()
