"""
CPU tests for report_framework/domain_templates.py.
Part A: contract validation and scoped application (negative cases, restore, nesting).
Part B: Deep-Reporter generate_article end-to-end (real graph/nodes) with the videomme
        templates, a fake OpenAI-compatible LLM server and the CPU retrieval service
        (fake-embedding cache from test_retriever.py). Writes only to the scratchpad.
"""
import copy, json, os, re, sys, threading, time

RF = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
SCRATCH = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "_artifacts")   # tests/_artifacts
sys.path.insert(0, RF); sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))
from rf_config import load_config  # noqa: E402
VID = "-QuCz7kxBr8"


def check(cond, msg):
    print(("  PASS " if cond else "  FAIL ") + msg)
    if not cond:
        check.failed += 1
check.failed = 0


def expect_error(fn, exc, contains, msg):
    try:
        fn()
    except exc as e:
        check(contains in str(e), f"{msg} -> {type(e).__name__}: {str(e)[:110]}")
        return
    check(False, f"{msg} -> no error raised")


def part_a():
    import domain_templates as D
    from deep_reporter.prompts import templates as orig
    print("[A] contract validation / scoped application")
    targets = D.resolve_targets()
    good = D.build_templates("videomme", "[00:00:00-00:10:00] overview with {braces} and }{ stray")
    D.validate_templates(good, targets); check(True, "videomme set valid (overview containing braces is escaped)")

    bad = dict(good); bad["SECTION_WRITING_TEMPLATE"] = good["SECTION_WRITING_TEMPLATE"] + "\n{\"json\": 1}"
    expect_error(lambda: D.validate_templates(bad, targets), D.TemplateContractError, "SECTION_WRITING_TEMPLATE", "unescaped brace")
    bad = dict(good); bad["QUERY_GENERATION_TEMPLATE"] = good["QUERY_GENERATION_TEMPLATE"] + "{video_id}"
    expect_error(lambda: D.validate_templates(bad, targets), D.TemplateContractError, "not passed by", "unknown placeholder")
    bad = dict(good); bad["SECTION_WRITING_TEMPLATE"] = good["SECTION_WRITING_TEMPLATE"].replace("{retrieved_materials}", "")
    expect_error(lambda: D.validate_templates(bad, targets), D.TemplateContractError, "missing required placeholders", "missing required placeholder")
    bad = dict(good); bad["SECTION_WRITING_TEMPLATE"] = good["SECTION_WRITING_TEMPLATE"].replace("![](citation:img1)", "")
    expect_error(lambda: D.validate_templates(bad, targets), D.TemplateContractError, "missing output markers", "missing citation marker")
    expect_error(lambda: D.validate_templates(dict(D.TEMPLATE_SETS["videomme"]), targets), D.TemplateContractError, "unfilled", "unfilled overview slot")
    expect_error(lambda: D.build_templates("videomme", None), ValueError, "needs a video overview", "overview required")
    expect_error(lambda: D.build_templates("nope", "x"), KeyError, "Unknown template domain", "unknown domain")
    # decision 5: section cap slot and conclusion rules
    t4 = D.build_templates("videomme", "[00:00:00-00:10:00] o", max_sections=4)
    check("3-4 sections in total (never more than 4" in t4["OUTLINE_GENERATION_TEMPLATE"] and "<<MAX_SECTIONS>>" not in str(t4),
          "max_sections filled into the planner template")
    D.validate_templates(t4, targets); check(True, "max_sections=4 set valid")
    for bad_n in (2, 16, "6", True):
        expect_error(lambda: D.build_templates("videomme", "o", max_sections=bad_n), ValueError, "max_sections", f"max_sections={bad_n!r} rejected")
    check(D.build_templates("videomme", "o", max_sections=15) and True, "max_sections=15 (measured limit) accepted")
    check('"section_description": "Conclusion:' in good["OUTLINE_GENERATION_TEMPLATE"].format(overall_query="q", overall_checklist="c"),
          "planner example ends with a 'Conclusion:' section")
    bad = dict(good); bad["OUTLINE_GENERATION_TEMPLATE"] = good["OUTLINE_GENERATION_TEMPLATE"].replace('"Conclusion:', '"Summary:')
    expect_error(lambda: D.validate_templates(bad, targets), D.TemplateContractError, "missing output markers", "planner without conclusion rule rejected")
    raw = dict(D.TEMPLATE_SETS["videomme"]); raw["OUTLINE_GENERATION_TEMPLATE"] = raw["OUTLINE_GENERATION_TEMPLATE"].replace("<<VIDEO_OVERVIEW>>", "o")
    expect_error(lambda: D.validate_templates(raw, targets), D.TemplateContractError, "<<MAX_SECTIONS>>", "unfilled max-sections slot rejected")

    # decision 4-B: writer rule 6 (no repetition) is part of the contract
    check("6. Do not repeat a fact, sentence, or paragraph" in good["SECTION_WRITING_TEMPLATE"], "writer rule 6 present")
    bad = dict(good); bad["SECTION_WRITING_TEMPLATE"] = good["SECTION_WRITING_TEMPLATE"].replace("mention it in at most one short sentence", "mention it")
    expect_error(lambda: D.validate_templates(bad, targets), D.TemplateContractError, "missing output markers", "writer without rule 6 rejected")

    ns_vars = [(t["namespace"], t["var"]) for t in targets]
    originals = [ns[v] for ns, v in ns_vars]
    try:
        with D.apply_templates(good):
            check(all(ns[v] is good[v] for ns, v in ns_vars), "inside: node globals point to domain templates")
            expect_error(lambda: D.apply_templates(good).__enter__(), RuntimeError, "already applied", "nested apply rejected")
            raise ValueError("boom")
    except ValueError:
        pass
    check(all(ns[v] is o for (ns, v), o in zip(ns_vars, originals)), "restored after an exception inside the block")
    check(orig.SECTION_WRITING_TEMPLATE is originals[2], "prompts.templates module untouched")

    # decision 4-C0: written-content summary of previous sections
    sec1 = ("# Section 1: Opening\n\nAt 00:00:10 the players gather on the court [citation:txt1][citation:txt3]. They talk.\n"
            "![](citation:img1)\n\nThe host explains the goal of the video [citation: txt2]. More text here.\n\nShort.")
    s1 = D.written_context_summary("", sec1)
    check(s1.startswith(D.WRITTEN_CONTEXT_NOTE) and "Section 1: Opening" in s1, "summary: note + title (\"Section k:\" prefix not doubled)")
    check("- At 00:00:10 the players gather on the court." in s1 and "- The host explains the goal of the video." in s1,
          "summary: first sentence of each paragraph, time kept")
    check("citation" not in s1.split("\n", 1)[1] and "They talk" not in s1 and "Short." not in s1,
          "summary: citations/images removed, only first sentences, short paragraphs skipped")
    s2 = D.written_context_summary(s1, "# Gadgets\n\nThe first gadget is a pair of goggles [citation:txt4].")
    check("Section 2: Gadgets" in s2 and s2.count(D.WRITTEN_CONTEXT_NOTE) == 1 and "Section 1: Opening" in s2, "summary: appended entry, one note")
    big = ""
    for k in range(8):
        big = D.written_context_summary(big, f"# T{k}\n\n" + "\n\n".join(f"Paragraph {k}.{j} " + "word " * 40 + "end." for j in range(6)))
    entries = big.split("\n", 1)[1].split("\n\n")
    check(len(big) - len(D.WRITTEN_CONTEXT_NOTE) - 1 <= D.CONTEXT_TOTAL_CHARS and entries[0] == "Section 1: T0" and entries[-1].count("\n- ") >= 1,
          f"summary: capped at {D.CONTEXT_TOTAL_CHARS} chars by reducing oldest entries to titles (len={len(big)})")
    tgt = D.resolve_update_context()
    ns, original = tgt["namespace"], tgt["original"]
    try:
        with D.apply_written_context():
            swapped = ns["_update_context"]
            check(swapped is not original, "inside: section_writing_node reads the written-context function")
            new_sum, tail = swapped("", sec1, "desc")
            check(tail == original("", sec1, "desc")[1] and new_sum == s1, "tail identical to Deep-Reporter's; summary = written summary")
            expect_error(lambda: D.apply_written_context().__enter__(), RuntimeError, "already applied", "nested written-context rejected")
            raise ValueError("boom")
    except ValueError:
        pass
    check(ns["_update_context"] is original, "_update_context restored after an exception")


class FakeReportLLM:
    """Answers planner / query / writer prompts; records which template family each prompt came from."""
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
        p = messages[-1]["content"]
        FakeReportLLM.prompts.append(p)
        if "Design an outline of" in p or "generating article outlines" in p:
            return "```json\n" + json.dumps({"outline": [
                {"section_description": "Opening: participants and goal.", "sectional_checklist": ["Who appears", "Stated goal"]},
                {"section_description": "Gadget tests and results.", "sectional_checklist": ["Which gadgets", "Outcomes"]}]}) + "\n```"
        if "text_queries" in p:
            return json.dumps({"text_queries": ["basketball gadget test", "players introduced"],
                               "image_queries": ["man dribbling a basketball outdoors"]})
        mats = re.findall(r"\[Source (txt\d+) begin\]", p)
        imgs = re.findall(r"\[Source (img\d+):", p)
        return (f"# Section\nAt 00:00:10 the players gather [citation:{mats[0] if mats else 'txt1'}].\n"
                + (f"![](citation:{imgs[0]})\n" if imgs else "") + "They test gadgets [citation:txt2].")


def part_b():
    import domain_templates as D
    import local_llm_server as L
    import videorag_retriever_service as S
    import test_retriever as T
    print("[B] Deep-Reporter generate_article end-to-end (CPU, fake models)")
    cfg = load_config(os.path.join(RF, "config.yaml"))
    cfg["paths"]["episodic_cache_root"] = os.path.join(SCRATCH, "test_cache", "episodic")
    cfg["service"]["frames_dir"] = os.path.join(SCRATCH, "test_cache", "frames")
    cfg["worldmm"]["episodic_cache_label"] = T.LABEL
    cfg["retrieval"]["episodic_filter"] = "L0"
    if not os.path.isdir(os.path.join(cfg["paths"]["episodic_cache_root"], VID)):   # fresh checkout: no cache from test_retriever yet
        T.build_test_cache(cfg)
    retr = S.WorldMMRetriever(cfg, T.FakeEmbedding(), S.NoLLM())
    threading.Thread(target=lambda: S.create_app(retr).run(host="127.0.0.1", port=18220), daemon=True).start()
    threading.Thread(target=lambda: L.create_app(FakeReportLLM(), "qwen3vl-8b", 8192).run(host="127.0.0.1", port=18210), daemon=True).start()
    time.sleep(1.5)

    os.environ["QWEN_BASE_URL"] = "http://127.0.0.1:18210/v1"; os.environ["QWEN_API_KEY"] = "EMPTY"
    from deep_reporter.api import create_openai_api
    api = create_openai_api({"primary_model": "qwen3vl-8b", "log_dir": os.path.join(SCRATCH, "dr_logs")})
    overview = D.load_video_overview(os.path.join(cfg["paths"]["caption_dir"], VID, "10min.json"))
    kwargs = dict(overall_query="Write a report on what happens in this video.", overall_checklist=[],
                  generation_mode="with_planner", text_topk=20, image_topk=10, enable_filter=False,
                  retriever_url=f"http://127.0.0.1:18220/videos/{VID}/search", userid="templ_test")

    FakeReportLLM.prompts.clear()
    with D.apply_templates(D.build_templates("videomme", overview)):
        res = api.generate_article(**kwargs)
    pr = list(FakeReportLLM.prompts)
    check(res["success"], "generate_article success")
    check(len(res["outline"]) == 2, f"planner JSON parsed -> {len(res['outline'])} sections")
    check(pr and "Design an outline of 3-6 sections in total" in pr[0] and overview.split("\n")[0][:60] in pr[0], "planner prompt = videomme template with video overview")
    check(sum("You generate search queries for retrieving evidence from ONE video" in p for p in pr) == 2, "query prompts = videomme template (x2)")
    writer = [p for p in pr if "Retrieved Evidence from the Video" in p]
    check(len(writer) == 2, "writer prompts = videomme template (x2)")
    check(all("| episodic " in w and "[Source img1: [" in w for w in writer), "writer saw timestamped episodic + image evidence")
    secs = res["outline"]
    check(all(s["text_queries"] == ["basketball gadget test", "players introduced"] for s in secs), "queries parsed into sections")
    check(all(len(s["retrieved_texts"]) > 0 and len(s["retrieved_images"]) > 0 for s in secs), "evidence retrieved for every section")
    check("[citation:txt" in res["final_article"] and "![](citation:img" in res["final_article"], "final article carries citations")
    check(len(pr) == 5, f"LLM calls = 1 planner + 2x(query + writer) = 5 (got {len(pr)})")

    check("Content: # Section" in writer[1], "default (no C0): writer 2 sees Deep-Reporter summary (first 100 chars)")

    FakeReportLLM.prompts.clear()
    with D.apply_templates(D.build_templates("videomme", overview)), D.apply_written_context():
        res_c0 = api.generate_article(**kwargs)
    pr = list(FakeReportLLM.prompts)
    check(res_c0["success"] and len(pr) == 5, f"C0 run: success, LLM calls still 5 (got {len(pr)})")
    w2 = [p for p in pr if "Retrieved Evidence from the Video" in p][1]
    summ = w2.split("**Summary of previous sections:**", 1)[1].split("**End of previous section", 1)[0]
    check(D.WRITTEN_CONTEXT_NOTE in summ and "Section 1: Section\n" in summ and "- At 00:00:10 the players gather." in summ
          and "citation" not in summ.split(D.WRITTEN_CONTEXT_NOTE, 1)[1], "C0 run: writer 2 sees written sentences of section 1, no citations")
    q2 = [p for p in pr if "You generate search queries" in p][1]
    check(D.WRITTEN_CONTEXT_NOTE in q2, "C0 run: query generation of section 2 sees the same summary")
    check("6. Do not repeat a fact" in w2, "C0 run: writer prompt carries rule 6")

    FakeReportLLM.prompts.clear()
    api.generate_article(**kwargs)
    check(FakeReportLLM.prompts and "generating article outlines" in FakeReportLLM.prompts[0], "after the block: original web templates are used again")
    SW = sys.modules["deep_reporter.nodes.section_writing_node"]  # package attribute is shadowed by the function
    check(SW._update_context.__module__ == SW.__name__ and SW.section_writing_node.__globals__["_update_context"] is SW._update_context,
          "after the block: original _update_context is back")
    print("    final article (fake LLM):", res["final_article"][:160].replace("\n", " | "))


if __name__ == "__main__":
    import logging
    logging.basicConfig(level=logging.WARNING)
    import deep_reporter.api  # noqa: F401  (import order)
    part_a()
    part_b()
    print(f"\nRESULT: {'ALL PASS' if check.failed == 0 else f'{check.failed} FAILED'}")
