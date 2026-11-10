"""
Summarize an experiments/gpu_report_batch.py output folder (read-only): per job exit, generation time, LLM calls and
max_tokens hits in the job's time window (server log), repeated-sentence removal and mid-sentence ends (P9),
start/end claim findings (P19), rule-check counts, and the conclusion section's last sentence.
Usage: python analysis/summarize_batch.py <batch_out_dir> [--json out.json]
"""
import argparse, datetime as dt, json, os, re


def ts(s):
    return dt.datetime.strptime(s, "%Y-%m-%d %H:%M:%S,%f")


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("out")
    ap.add_argument("--json", default=None)
    a = ap.parse_args()
    summary = json.load(open(os.path.join(a.out, "summary.json")))
    rows = []
    for r in sorted(summary["results"], key=lambda x: x["job"]):
        job = r["job"]
        d = os.path.join(a.out, job)
        row = {"job": job, "exit": r.get("exit"), "wall_sec": r.get("wall_sec")}
        if r.get("exit") != 0 or not os.path.isfile(os.path.join(d, "validation.json")):
            rows.append(row)
            continue
        v = json.load(open(os.path.join(d, "validation.json")))
        log = open(os.path.join(a.out, f"run_report_{job}.log"), errors="replace").read()
        t = [ts(x) for x in re.findall(r"^(\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d+)", log, re.M)]
        calls = []
        if t:
            for line in open(os.path.join(a.out, f"llm_server_s{r['stack']}_gpu{r['gpu']}.log"), errors="replace"):
                m = re.match(r"(\S+ \S+) local_llm_server INFO chat.completions: prompt=(\d+) completion=(\d+) finish=(\w+) ([\d.]+)s", line)
                if m and min(t) <= ts(m.group(1)) <= max(t):
                    calls.append((int(m.group(2)), int(m.group(3)), m.group(4), float(m.group(5))))
        rep = v.get("repetition", [])
        g = v.get("grounding_stats", {})
        outline = json.load(open(os.path.join(d, "report.json")))["outline"]
        concl = (outline[-1].get("content") or "").strip() if outline else ""
        row.update({
            "status": v["status"], "sections": len(v.get("sections", [])), "generation_sec": v["timings"].get("generation_sec"),
            "llm_calls": len(calls), "cap_hits": sum(c[2] == "length" for c in calls),
            "cap_hit_sec": [c[3] for c in calls if c[2] == "length"],
            "removed_sentences": sum(x["removed_sentences"] for x in rep),
            "max_repeat": max((x["max_repeat"] for x in rep), default=0),
            "loop_sections": [x["index"] for x in rep if x["max_repeat"] >= 3],
            "mid_sentence_sections": [x["index"] for x in rep if x["ends_mid_sentence"]],
            "boundary": [(f["section"], f["status"], f.get("latest_cited_end") or f.get("earliest_cited_start")) for f in v.get("boundary_findings", [])],
            "video_end": v.get("video_end"),
            "rule_check": {k: g.get(k) for k in ("sentences", "cited_sentences", "unsupported", "miscited", "uncited_claims")},
            "conclusion_last_sentence": re.split(r"(?<=[.!?])\s+", re.sub(r"\[citation:[^\]]*\]", "", concl))[-1][:300] if concl else "",
        })
        rows.append(row)
    for row in rows:
        print(json.dumps(row, ensure_ascii=False))
    if a.json:
        json.dump(rows, open(a.json, "w"), indent=1, ensure_ascii=False)


if __name__ == "__main__":
    main()
