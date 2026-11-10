"""
CPU tests (no GPU) for grounding_postprocessor.py and run_report.py.
Part 1: post-processor + rule-based check on the real Qwen3-VL-8B smoke report and synthetic edge cases.
Part 2: run_report.run() end-to-end with a fake OpenAI-compatible LLM server and the CPU retrieval
        service (fake-embedding cache from test_retriever.py): normal run + failure paths.
Outputs go to tests/_artifacts/.
"""
import copy, json, os, re, sys, threading, time

HERE = os.path.dirname(os.path.abspath(__file__))
RF = os.path.dirname(os.path.dirname(HERE))
ART = os.path.join(os.path.dirname(HERE), "_artifacts")   # tests/_artifacts
sys.path.insert(0, RF); sys.path.insert(0, HERE)
from rf_config import load_config  # noqa: E402
VID = "-QuCz7kxBr8"


def check(cond, msg):
    print(("  PASS " if cond else "  FAIL ") + msg)
    if not cond:
        check.failed += 1
check.failed = 0


def part1():
    import grounding_postprocessor as G
    print("[1] post-processor on the real smoke report")
    outline = json.load(open(os.path.join(ART, "gpu_report", "outline.json")))
    for s in outline:
        for m in s["retrieved_images"]:
            m["img_path"] = os.path.join(ART, "gpu_test", "frames", m["video_id"], os.path.basename(m["img_path"]))
    out = os.path.join(ART, "pipeline_test", "smoke_grounded")
    r = G.ground_report({"outline": outline}, enable_filter=False, out_dir=out)
    open(os.path.join(out, "report.md"), "w").write(r["markdown"])
    cs, gs = r["citation_stats"], r["grounding_stats"]
    check("[citation:" not in r["markdown"] and "(citation:" not in r["markdown"], "no placeholder citations left")
    check(cs["text_citations"] == 109 and cs["invalid_citations"] == 0, f"109 text citations mapped ({cs})")
    check(cs["wrong_form_image_citations"] == 8 and cs["figures"] == 7 and cs["missing_frame_files"] == 0,
          "8 wrong-form image citations converted, 7 unique figures, frames copied")
    check(len([f for f in os.listdir(os.path.join(out, "frames"))]) == 7, "7 frame files in <out>/frames")
    check(cs["references"] == 46 and "# References" in r["markdown"], "46 unique references listed")
    tok = {(f["status"], f.get("token")) for s in r["sections"] for f in s["grounding"]["findings"]}
    for status, token in [("unsupported", "SCORE 10"), ("unsupported", "0/1"), ("unsupported", "3/16"),
                          ("unsupported", "WOO"), ("miscited", "1-0"), ("miscited", "00:02:30"), ("miscited", "00:08:20")]:
        check((status, token) in tok, f"rule check flags {status} {token!r} (manually verified true positive)")
    check(("unsupported", "SCORE 5") not in tok and ("unsupported", "8/10") not in tok,
          "paraphrases 'score of 5' / '8 out of 10' are not flagged")
    print(f"    grounding_stats={gs}")

    print("[1b] synthetic edge cases")
    texts = [{"uid": "v:episodic:a", "type": "text", "source": "worldmm-episodic", "granularity": "10sec",
              "content": "[00:00:10-00:00:20 | episodic 10sec] Host says \"Welcome back\" and shows 3 cones.",
              "text": "Host says \"Welcome back\" and shows 3 cones.", "start_time": "00001000", "end_time": "00002000",
              "start_sec": 10.0, "end_sec": 20.0},
             {"uid": "v:semantic:b", "type": "text", "source": "worldmm-semantic", "time_grounded": False,
              "content": "[video-level knowledge | semantic] (host, likes, cones)", "triple": ["host", "likes", "cones"],
              "start_time": None, "end_time": None, "start_sec": None, "end_sec": None}]
    frame = os.path.join(ART, "gpu_test", "frames", VID, sorted(os.listdir(os.path.join(ART, "gpu_test", "frames", VID)))[0])
    imgs = [{"uid": "v:visual:c", "type": "image", "video_id": "v", "img_path": frame, "frame_sec": 15.0,
             "caption": "[00:00:10-00:00:20 | video frame at 15.0s] Host with cones", "start_time": "00001000", "end_time": "00002000",
             "start_sec": 10.0, "end_sec": 20.0}]
    content = ("# Intro\nAt 00:00:15 the host says \"Welcome back\" [citation: txt1, txt2]. He shows 5 cones [citation:txt1]. "
               "A frame shows him [citation:img1]. Bad ref [citation:txt9]. Junk [citation:foo].\n\n![](citation:img1)\n![](citation:img7)")
    sec = {"content": content, "retrieved_texts": texts, "retrieved_images": imgs, "section_description": "d"}
    filt = {"content": "Filtered source [citation:txt1].", "retrieved_texts": [], "retrieved_images": [],
            "filtered_texts": texts, "filtered_images": imgs, "section_description": "f"}
    out2 = os.path.join(ART, "pipeline_test", "edge")
    r = G.ground_report({"outline": [sec, {"content": "[Section generation failed: boom]"}, {"content": None}]},
                        enable_filter=False, out_dir=out2)
    md, cs = r["markdown"], r["citation_stats"]
    check("[1][2]" in md and "(Figure 1)" in md, "variant '[citation: txt1, txt2]' -> [1][2]; wrong-form img -> (Figure 1)")
    check(cs["invalid_citations"] == 3 and md.count("[?]") == 3, f"txt9, foo, img7 -> [?] and counted ({cs['invalid_citations']})")
    check(cs["duplicate_image_embeds"] == 1 and md.count("![Figure 1") == 1, "same frame embedded once")
    check("no timestamp): (host, likes, cones)" in md and "00:00:10–00:00:20 · episodic 10sec" in md,
          "references: semantic without time, episodic with time range")
    check(r["sections"][1]["failed_marker"] and "[Section 3 content missing]" in md, "failure text detected; missing content placeholder")
    f = {(x["status"], x.get("token")) for x in r["sections"][0]["grounding"]["findings"]}
    check(("unsupported", "5") in f and ("unsupported", "00:00:15") not in f and ("unsupported", "Welcome back") not in f,
          "rule check: '5 cones' unsupported (evidence says 3); 00:00:15 inside cited interval and quote ok")
    r2 = G.ground_report({"outline": [filt]}, enable_filter=True, out_dir=out2)
    check(r2["citation_stats"]["invalid_citations"] == 0 and "[1]" in r2["markdown"], "enable_filter=True uses filtered_* lists")


def fake_translate(masked: str) -> str:
    """'Translation' that keeps headings, placeholder-only lines and blank lines, and marks other lines."""
    return "\n".join(line if (line.startswith("#") or re.fullmatch(r"\s*\[\[P\d+\]\]\s*", line) or not line.strip())
                     else "(KO) " + line for line in masked.split("\n"))


def citations(text: str):
    return sorted(re.findall(r"\[(?:\d+|\?)\]|\(Figure \d+\)", text))


class FakeLLM:
    """OpenAI-compatible fake for local_llm_server.create_app. Modes: ok, bad_planner, no_conclusion,
    too_many (8 sections), translate_flaky (first translation attempt per section drops a placeholder),
    translate_drop (always drops one)."""
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
    mode = "ok"
    translations = 0

    def generate(self, messages, **kw):
        p = messages[-1]["content"]
        if "Translate the following Markdown section" in p:
            body = p.split("<<<\n", 1)[1].rsplit("\n>>>", 1)[0]
            FakeLLM.translations += 1
            if FakeLLM.mode == "translate_drop" or (FakeLLM.mode == "translate_flaky" and FakeLLM.translations % 2 == 1):
                body = body.replace("[[P1]]", "", 1)
            if FakeLLM.mode == "translate_han":
                return fake_translate(body) + "\n\n햇明媚한 날"
            return fake_translate(body)
        if "Design an outline of" in p:
            if FakeLLM.mode == "bad_planner":
                return "Sorry, I cannot produce JSON."
            n = 8 if FakeLLM.mode == "too_many" else 2
            sections = [{"section_description": f"Part {i + 1} of the video.", "sectional_checklist": ["Who appears"]}
                        for i in range(n - 1)]
            last = "Results summary." if FakeLLM.mode == "no_conclusion" else "Conclusion: Brief summary of the results."
            return "```json\n" + json.dumps({"outline": sections + [{"section_description": last,
                                                                     "sectional_checklist": ["Outcomes"]}]}) + "\n```"
        if "text_queries" in p:
            return json.dumps({"text_queries": ["basketball gadget test"], "image_queries": ["man dribbling outdoors"]})
        if "Retrieved Evidence from the Video" in p:
            t = re.search(r"\[Source txt1 begin\]\n\[(\d\d:\d\d:\d\d)", p)
            return (f"# Section\nAt {t.group(1) if t else '00:00:00'}, players gather [citation:txt1].\n"
                    "The frame shows the court [citation:img1].\n\n![](citation:img1)")
        return "[]"


def part2():
    import local_llm_server as L
    import videorag_retriever_service as S
    import run_report as R
    import test_retriever as T
    print("[2] run_report end-to-end (CPU, fake LLM + CPU retrieval service)")
    cfg = load_config(os.path.join(RF, "config.yaml"))
    cfg["paths"]["episodic_cache_root"] = os.path.join(ART, "test_cache", "episodic")
    cfg["service"].update({"frames_dir": os.path.join(ART, "test_cache", "frames"), "port": 18420})
    cfg["worldmm"]["episodic_cache_label"] = T.LABEL
    cfg["retrieval"]["episodic_filter"] = "L0"
    cfg["llm"]["local"]["endpoint"]["port"] = 18410
    cfg["report"]["deep_reporter_log_dir"] = os.path.join(ART, "dr_logs_pipeline")
    if not os.path.isdir(os.path.join(cfg["paths"]["episodic_cache_root"], VID)):
        T.build_test_cache(cfg)
    retr = S.WorldMMRetriever(cfg, T.FakeEmbedding(), S.NoLLM())
    threading.Thread(target=lambda: S.create_app(retr).run(host="127.0.0.1", port=18420), daemon=True).start()
    time.sleep(1.0)

    # LLM server not running yet -> preflight failure
    code = R.run(cfg, VID, "Report what happens.", [], os.path.join(ART, "pipeline_test", "no_llm"))
    check(code == 2, f"LLM endpoint down -> exit 2 (got {code})")

    threading.Thread(target=lambda: L.create_app(FakeLLM(), "qwen3vl-8b", 8192).run(host="127.0.0.1", port=18410), daemon=True).start()
    time.sleep(1.0)
    other = sorted(os.listdir(cfg["paths"]["caption_dir"]))[1]
    code = R.run(cfg, other, "Report what happens.", [], os.path.join(ART, "pipeline_test", "no_cache"))
    check(code == 2, f"video without episodic cache ({other}) -> exit 2 (got {code})")

    out = os.path.join(ART, "pipeline_test", "ok")
    code = R.run(cfg, VID, "Report what happens in this video.", ["Mention the participants"], out)
    v = json.load(open(os.path.join(out, "validation.json")))
    md = open(os.path.join(out, "report.md")).read()
    check(code == 0 and v["status"] == "passed", f"normal run -> exit 0, status passed (got {code}, errors={v['errors']})")
    check(all(os.path.isfile(os.path.join(out, f)) for f in ("report.md", "report_raw.md", "report.json", "validation.json")),
          "report.md / report_raw.md / report.json / validation.json written")
    check("# References" in md and "![Figure 1" in md and "[citation:" not in md and os.listdir(os.path.join(out, "frames")),
          "grounded report has references, a figure and copied frames; no placeholders")
    check(any("converted to figures" in w for w in v["warnings"]), "wrong-form image citation reported as warning")
    check(v["grounding_stats"]["checked_tokens"] > 0 and "timings" in v, "grounding stats and timings recorded")
    rj = json.load(open(os.path.join(out, "report.json")))
    check(rj["checklist"] == ["Mention the participants"] and len(rj["outline"]) == 2 and rj["retrieval_mode"] == "L0",
          "report.json keeps query/checklist/outline/evidence and retrieval mode")
    # decision 5: compliant outline -> no cap/conclusion warnings
    check(rj["outline"][-1]["section_description"].startswith("Conclusion:") and v["max_sections"] == 6
          and not any("conclusion" in w.lower() or "max_sections" in w for w in v["warnings"]),
          "conclusion-last outline within the cap -> no decision-5 warnings")
    # decision 6: translation
    ko = open(os.path.join(out, "report_ko.md")).read()
    en_body, ko_body = md.split("# References")[0], ko.split("# References")[0]
    check(v["translation"]["status"] == "complete" and "(KO)" in ko and "**요청**" in ko, "report_ko.md written, all sections translated")
    check(citations(en_body) == citations(ko_body), f"citations/figure refs identical after translation ({len(citations(en_body))})")
    check([l for l in md.splitlines() if l.startswith("![Figure")] == [l for l in ko.splitlines() if l.startswith("![Figure")],
          "figure image lines kept verbatim")
    check(md.split("# References")[1].strip() in ko, "References kept in English")

    for mode, msg in [("no_conclusion", "last section is not a conclusion"), ("too_many", "above report.max_sections=6")]:
        FakeLLM.mode = mode
        out = os.path.join(ART, "pipeline_test", mode)
        code = R.run(cfg, VID, "Report what happens in this video.", [], out)
        v = json.load(open(os.path.join(out, "validation.json")))
        check(code == 0 and any(msg in w for w in v["warnings"]), f"{mode}: warning '{msg}' (exit {code})")

    FakeLLM.mode, FakeLLM.translations = "translate_flaky", 0
    out = os.path.join(ART, "pipeline_test", "translate_flaky")
    code = R.run(cfg, VID, "Report what happens in this video.", [], out)
    v = json.load(open(os.path.join(out, "validation.json")))
    check(code == 0 and v["translation"]["status"] == "complete" and all(s["attempts"] == 2 for s in v["translation"]["sections"]),
          "translation retried once per section after a dropped placeholder -> complete")

    FakeLLM.mode = "translate_drop"
    out = os.path.join(ART, "pipeline_test", "translate_drop")
    code = R.run(cfg, VID, "Report what happens in this video.", [], out)
    v = json.load(open(os.path.join(out, "validation.json")))
    ko = open(os.path.join(out, "report_ko.md")).read()
    check(code == 0 and v["status"] == "passed" and v["translation"]["status"] == "failed"
          and "번역 검증에 실패" in ko and any("translation of section" in w for w in v["warnings"]),
          "persistent placeholder loss -> English kept with notice, warning only, exit 0")

    FakeLLM.mode = "translate_han"
    out = os.path.join(ART, "pipeline_test", "translate_han")
    code = R.run(cfg, VID, "Report what happens in this video.", [], out)
    v = json.load(open(os.path.join(out, "validation.json")))
    check(code == 0 and v["translation"]["status"] == "complete"
          and all(s["attempts"] == 2 and s["foreign_script"] == ["明媚"] for s in v["translation"]["sections"])
          and any("non-Hangul CJK characters" in w for w in v["warnings"]),
          "Han characters in translation -> retried once, kept, reported in validation (warning, exit 0)")
    check("image_time_alignment" in v and v["image_time_alignment"]["cited_images"] >= 1
          and "absence_statements" in v["grounding_stats"] and "proper_nouns" in v["translation"],
          f"validation.json records image_time_alignment {v['image_time_alignment']}, absence stats, proper nouns")

    FakeLLM.mode = "bad_planner"
    out = os.path.join(ART, "pipeline_test", "bad_planner")
    code = R.run(cfg, VID, "Report what happens in this video.", [], out)
    v = json.load(open(os.path.join(out, "validation.json")))
    check(code == 1 and any("planner fallback" in e for e in v["errors"]), f"planner fallback detected -> exit 1 ({v['errors'][:1]})")
    check(v["translation"]["status"] == "skipped" and not os.path.exists(os.path.join(out, "report_ko.md")),
          "validation errors -> translation skipped")
    FakeLLM.mode = "ok"

    bad_cfg = copy.deepcopy(cfg); bad_cfg["report"]["max_sections"] = 16
    check(R.run(bad_cfg, VID, "q", [], os.path.join(ART, "pipeline_test", "cap16")) == 2, "report.max_sections=16 -> exit 2 before generation")
    print("    sample grounded report:\n      " + md[:600].replace("\n", "\n      "))


def part3():
    import grounding_postprocessor as G
    import report_translator as RT
    print("[3] translator on the real smoke report (fake translation LLMs)")
    outline = json.load(open(os.path.join(ART, "gpu_report", "outline.json")))
    for s in outline:
        for m in s["retrieved_images"]:
            m["img_path"] = os.path.join(ART, "gpu_test", "frames", m["video_id"], os.path.basename(m["img_path"]))
    g = G.ground_report({"outline": outline}, enable_filter=False, out_dir=os.path.join(ART, "pipeline_test", "translate_unit"))

    class Echo:
        def __init__(self, transform): self.transform, self.calls = transform, 0
        def generate(self, messages, **kw):
            self.calls += 1
            body = messages[0]["content"].split("<<<\n", 1)[1].rsplit("\n>>>", 1)[0]
            return self.transform(body)

    ok = RT.translate_report(g, "> header", Echo(fake_translate))
    check(ok["status"] == "complete" and len(ok["sections"]) == 5, "5 real sections translated")
    en = "\n\n".join(g["section_bodies"])
    ko_body = ok["markdown"].split("# References")[0]
    check(citations(en) == citations(ko_body), f"all {len(citations(en))} citations / figure refs preserved")
    check(all(line in ko_body for line in en.splitlines() if line.startswith("![Figure") or line.startswith("*Figure")),
          "figure image and caption lines preserved verbatim")
    quotes_en = re.findall(r"[\"“][^\"“”\n]{1,300}[\"”]", en)
    check(all(q in ko_body for q in quotes_en), f"all {len(quotes_en)} quoted strings preserved verbatim")
    check(ok["sections"][0]["placeholders"] > 0, f"placeholders per section e.g. {[s['placeholders'] for s in ok['sections']]}")

    fenced = RT.translate_section(g["section_bodies"][0], Echo(lambda b: "```markdown\n" + fake_translate(b) + "\n```"))
    check(fenced["status"] == "translated", "code-fenced model output accepted")
    cases = [("dropped placeholder", lambda b: b.replace("[[P2]]", "")),
             ("duplicated placeholder", lambda b: b + " [[P1]]"),
             ("heading removed", lambda b: re.sub(r"^#+\s", "", b, flags=re.M)),
             ("empty output", lambda b: "")]
    for name, fn in cases:
        llm = Echo(fn)
        r = RT.translate_section(g["section_bodies"][0], llm)
        check(r["status"] == "fallback_english" and r["attempts"] == 2 and llm.calls == 2
              and g["section_bodies"][0] in r["text"] and RT.FALLBACK_NOTICE in r["text"],
              f"{name} -> retried once, then English kept with notice ({r['reason'][:60]})")

    class Boom:
        def generate(self, *a, **k): raise ConnectionError("down")
    r = RT.translate_section(g["section_bodies"][0], Boom())
    check(r["status"] == "fallback_english" and "LLM call failed" in r["reason"], "LLM exception -> fallback")


def part4():
    """Absence clauses, image-text time alignment, Han detection, proper-noun protection."""
    import grounding_postprocessor as G
    import report_translator as RT
    sys.path.insert(0, os.path.join(RF, "analysis"))
    import analyze_report as AR
    print("[4] absence clauses / image time alignment / Han detection / proper nouns")
    # real report B (first run_report execution)
    b_path = os.path.join(ART, "gpu_e2e", "outputs", "report_run1", "report.json")
    b = json.load(open(b_path))["outline"]
    find = [(i, f) for i, s in enumerate(b, 1)
            for f in G.check_section_grounding(s["content"], s["retrieved_texts"], s["retrieved_images"])["findings"]]
    flagged = {(f["status"], f.get("token")) for _, f in find}
    absent = [t for _, f in find if f["status"] == "absence" for t in f["tokens"]]
    check(("unsupported", "10:85") not in flagged and ("unsupported", "9:51") not in flagged and {"10:85", "9:51"} <= set(absent),
          "report B: negated '10:85'/'9:51' (\"…are not visible in the retrieved footage\") recorded as absence, not unsupported")
    s6 = {f.get("token") for i, f in find if i == 6 and f["status"] in ("unsupported", "miscited")}
    check({"SKLZ Dribble Stick", "Straight Shooter Strap", "Flick Glove", "Shot Coach"} <= s6,
          "report B: conclusion-section findings unchanged")
    # report A: all 9 earlier unsupported/miscited findings kept
    a = json.load(open(os.path.join(ART, "gpu_report", "outline.json")))
    fa = [f for s in a for f in G.check_section_grounding(s["content"], s["retrieved_texts"], s["retrieved_images"])["findings"]]
    fl = sorted(f["token"] for f in fa if f["status"] in ("unsupported", "miscited"))
    check(fl == sorted(["SCORE 10", "0/1", "3/16", "WOO", "1-0", "00:02:30", "00:08:20", "SCORE 6", "SCORE 6"]),
          f"report A: the same 9 unsupported/miscited tokens as before ({fl})")
    # synthetic: negation without an evidence noun, and a token before the negated clause, are still checked
    texts = [{"content": "[00:00:10-00:00:20 | episodic 10sec] He shoots and misses; the scoreboard reads 1/2.",
              "start_sec": 10.0, "end_sec": 20.0}]
    r = G.check_section_grounding("He did not make the shot, as shown on the scoreboard reading 0/1 [citation:txt1].", texts, [])
    check([(f["status"], f.get("token")) for f in r["findings"]] == [("unsupported", "0/1")],
          "plain negated event ('did not make the shot, as shown ... 0/1') is still checked")
    r = G.check_section_grounding("His score improves to 7, though the exact time is not specified in the evidence [citation:txt1].", texts, [])
    check(("unsupported", "7") in {(f["status"], f.get("token")) for f in r["findings"]},
          "token before the negated clause is still checked ('improves to 7, though … not specified in the evidence')")
    r = G.check_section_grounding("No scores such as \"9:51\" are shown in the retrieved footage [citation:txt1].", texts, [])
    check(r["stats"]["absence_statements"] == 1 and not r["stats"]["unsupported"], "token inside the negated clause -> absence")
    # image time alignment: synthetic
    tx = [{"content": "a", "start_sec": 10.0, "end_sec": 20.0}, {"content": "b", "start_sec": 100.0, "end_sec": 110.0}]
    im = [{"frame_sec": 15.0, "uid": "i1"}, {"frame_sec": 300.0, "uid": "i2"}]
    rows = G.image_time_alignment("At 00:00:12 x [citation:txt1].\n![](citation:img1)\n\nLater y [citation:txt2].\n\n![](citation:img2)", tx, im)
    check([(r_["img"], r_["gap_to_local_text_sec"], r_["gap_to_section_text_sec"]) for r_ in rows] == [("img1", 0.0, 0.0), ("img2", 190.0, 190.0)],
          f"alignment: frame inside cited range -> 0; stand-alone image uses previous paragraph -> 190 s ({rows})")
    # image time alignment on report B equals the analysis script (section-level, cited images)
    comp = AR.composition_metrics(b)["images"]
    ana = sorted((x["section"], x["frame"], x["gap_to_nearest_cited_episodic_sec"]) for x in comp if x["cited"])
    ours = sorted((i, r_["frame"], r_["gap_to_section_text_sec"]) for i, s in enumerate(b, 1)
                  for r_ in G.image_time_alignment(s["content"], s["retrieved_texts"], s["retrieved_images"]))
    check(ana == ours and len(ours) == 16, f"report B: section-level gaps of the 16 cited images match analyze_report.py")
    # translation: Han retry / persistence / protected spans
    body = "# Title\n\nChris meets Zach at 00:00:10 [1]. They test the “明媚 Box” gadget [2]."
    class Seq:
        def __init__(self, outs): self.outs, self.calls = list(outs), 0
        def generate(self, messages, **kw):
            self.calls += 1
            masked = messages[0]["content"].split("<<<\n", 1)[1].rsplit("\n>>>", 1)[0]
            return self.outs.pop(0)(masked)
    names = RT.collect_proper_nouns([body])
    check(names == ["Zach"], f"proper nouns: only mid-sentence runs are collected ({names}); sentence-initial 'Chris' alone is not")
    names = RT.collect_proper_nouns([body, "Later, Chris returns [3]."])
    check(set(names) == {"Chris", "Zach"}, f"a name seen mid-sentence anywhere in the report is collected ({names})")
    llm = Seq([lambda m: fake_translate(m) + " 明媚", fake_translate])
    r = RT.translate_section(body, llm, proper_nouns=names)
    check(r["status"] == "translated" and r["attempts"] == 2 and r["foreign_script"] == [] and "明媚 Box" in r["text"],
          "Han in output -> retried, clean second output used; Han inside a protected quote is not flagged")
    llm = Seq([lambda m: fake_translate(m) + " 明媚", lambda m: fake_translate(m) + " 明"])
    r = RT.translate_section(body, llm, proper_nouns=names)
    check(r["status"] == "translated" and r["foreign_script"] == ["明媚"], "Han persists -> first translation kept, characters reported")
    llm = Seq([lambda m: m.replace("Chris", "크리스").replace("Zach", "재치")])
    r = RT.translate_section(body, llm, proper_nouns=names)
    check(r["status"] == "translated" and "Chris" in r["text"] and "Zach" in r["text"] and r["protected_names"] == 2,
          "names are masked before translation and restored verbatim")
    bb = [p for p in re.split(r"(?m)^(?=# )", open(os.path.join(ART, "gpu_e2e", "outputs", "report_run1", "report.md")).read().split("# References")[0]) if p.startswith("# ")]
    nb = RT.collect_proper_nouns(bb)
    check({"Chris", "Zach", "Cass", "James", "Mitchell"} <= set(nb), f"report B: participant names collected ({nb})")


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.WARNING)
    import deep_reporter.api  # noqa: F401  (import order)
    part1()
    part2()
    part3()
    part4()
    print(f"\nRESULT: {'ALL PASS' if check.failed == 0 else f'{check.failed} FAILED'}")
