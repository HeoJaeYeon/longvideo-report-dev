"""CPU test for the 2026-10-25 fixes: P9 (server max_tokens cap, repeated-sentence removal, warnings),
P19 (writer rule 7 with the real video end, start/end claim check), I28 (token counting inside the lock).
Uses real C-5 loop outputs when present. No GPU, no network."""
import json, os, sys
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
HERE = os.path.dirname(os.path.abspath(__file__))
RF = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, RF)
import domain_templates as D
import grounding_postprocessor as G
import local_llm_server as L
import run_report as R
from rf_config import load_config

ok = []
def check(name, cond): ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

CAP = load_config(os.path.join(RF, "config.yaml"))["paths"]["caption_dir"]

# --- P9 (c): repeated-sentence removal -----------------------------------------------------------
loop = "# Title\n\nA happens [citation:txt1]. B happens [citation:txt2]. " + "C repeats [citation:txt3]. D repeats [citation:txt3]. " * 20 + "C rep"
new, st = G.dedupe_repeated_sentences(loop)
check("loop: 38 repeats removed, max repeat 20, mid-sentence end", st == {"removed_sentences": 38, "max_repeat": 20, "ends_mid_sentence": True})
check("loop: heading kept, each sentence once", new.startswith("# Title") and new.count("C repeats") == 1 and new.count("D repeats") == 1)
clean = "# T\n\nOne [citation:txt1]. Two.\n\n![](citation:img1)\n\nThree [citation:txt2]."
new2, st2 = G.dedupe_repeated_sentences(clean)
check("clean section unchanged", new2 == clean and st2 == {"removed_sentences": 0, "max_repeat": 1, "ends_mid_sentence": False})
c5 = os.path.join(RF, "outputs", "c5_c0_20261025_132851", "-QuCz7kxBr8__c0_written__r1", "report.json")
if os.path.isfile(c5):
    sec = json.load(open(c5))["outline"][1]["content"]
    new3, st3 = G.dedupe_repeated_sentences(sec)
    check(f"real C-5 loop section: {len(sec)} -> {len(new3)} chars, removed {st3['removed_sentences']}, max {st3['max_repeat']}",
          st3["removed_sentences"] > 200 and st3["max_repeat"] >= 50 and len(new3) < len(sec) / 5)

# --- P19 (3): start/end claim check --------------------------------------------------------------
texts = [{"start_sec": 1080.0, "end_sec": 1260.0}, {"start_sec": 2250.0, "end_sec": 2257.0}, {"start_sec": None, "end_sec": None}]
f = G.boundary_claims("The video closes with a close-up of the device [citation:txt1].", texts, 2257)
check("ending cited at 21:00 of 37:37 -> ending_early", len(f) == 1 and f[0]["status"] == "ending_early")
check("ending cited at the last seconds -> no finding", G.boundary_claims("The video ends with an end screen [citation:txt2].", texts, 2257) == [])
check("ending with only semantic evidence -> unverifiable",
      [x["status"] for x in G.boundary_claims("The video concludes with a message [citation:txt3].", texts, 2257)] == ["ending_unverifiable"])
check("'concludes this section' is not an ending claim", G.boundary_claims("The video concludes this section with a drill [citation:txt1].", texts, 2257) == [])
check("opening cited at 18:00 -> opening_late",
      [x["status"] for x in G.boundary_claims("The video opens with a rule card [citation:txt1].", texts, 2257)] == ["opening_late"])

# --- P19 (1): writer rule 7 with the real video end ----------------------------------------------
end, end_sec = D.load_video_end(f"{CAP}/-QuCz7kxBr8/10sec.json")
check(f"real video end from 10sec.json ({end}, {end_sec}s), not the 10min boundary 00:40:00", end == "00:37:37" and end_sec == 2257)
t = D.build_templates("videomme", "[00:00:00-00:10:00] o", 6, video_end=end)
w = t["SECTION_WRITING_TEMPLATE"]
check("writer template has rule 7 with 00:37:37 and no unfilled slot", "7. Each text source covers only its own time span" in w
      and "00:37:37" in w and "<<" not in w)
check("unknown end -> 'the end of the video'", "to the end of the video" in D.build_templates("videomme", "[x] o")["SECTION_WRITING_TEMPLATE"])

# --- P9 (d): validation warnings -----------------------------------------------------------------
result = {"success": True, "outline": [{"section_description": "Conclusion: x", "content": "# C\n\nDone [citation:txt1].",
                                         "text_queries": ["q"], "retrieved_texts": [{"content": "x"}]}]}
grounded = {"citation_stats": {"invalid_citations": 0, "missing_frame_files": 0, "wrong_form_image_citations": 0},
            "grounding_stats": {}}
rep = [{"index": 1, "removed_sentences": 38, "max_repeat": 20, "ends_mid_sentence": True}]
bnd = [{"status": "ending_early", "section": 1}]
_, warns = R.validate(result, grounded, "q", False, 6, rep, bnd)
check("warnings: removal + loop suspected + mid-sentence + start/end check",
      any("removed 38 repeated sentence(s)" in x and "loop suspected" in x for x in warns)
      and any("ends mid-sentence" in x for x in warns) and any("1 ending_early" in x for x in warns))

_, warns2 = R.validate(result, grounded, "q", False, 6,
                      [{"index": 1, "removed_sentences": 3, "max_repeat": 4, "ends_mid_sentence": False}], [])
check("2026-10-26: 4 repeats without a cut -> removal warning but no 'loop suspected'",
      any("removed 3 repeated" in x for x in warns2) and not any("loop suspected" in x for x in warns2))
_, warns3 = R.validate(result, grounded, "q", False, 6,
                      [{"index": 1, "removed_sentences": 2, "max_repeat": 2, "ends_mid_sentence": True}], [])
check("2026-10-26: cut section (mid-sentence end) -> 'loop suspected'", any("loop suspected" in x for x in warns3))

# --- P19 (2026-10-26): end-of-video source txt0 + possessive false positive ----------------------
block, item = D.load_video_ending(f"{CAP}/-QuCz7kxBr8/10sec.json")
check(f"end-of-video source spans the last 60 s ({item['start_time']}-{item['end_time']})",
      block.startswith("[Source txt0 begin]") and item["end_sec"] == 2257.0 and 2257 - item["start_sec"] <= 70
      and "Thank you for watching" in item["text"])
t2 = D.build_templates("videomme", "[x] o", 6, video_end=end, video_ending=block)["SECTION_WRITING_TEMPLATE"]
check("writer template shows txt0 block, LAST-section rule, no unfilled slot",
      "[Source txt0 begin]" in t2 and "cite it as [citation:txt0] ONLY in the LAST section" in t2 and "<<" not in t2)
check("no ending -> 'do not cite txt0'", "do not cite txt0" in D.build_templates("videomme", "[x] o")["SECTION_WRITING_TEMPLATE"])
sec_ = {"content": "# C\n\nThe video ends with an end screen [citation:txt0]. Earlier [citation:txt1, txt0].",
        "retrieved_texts": [{"content": "[00:10:00-00:10:10 | episodic 10sec] a", "start_sec": 600, "end_sec": 610}]}
check("txt0 cited -> item appended as txt2 and citations rewritten",
      G.attach_ending_source(sec_, item, False) and len(sec_["retrieved_texts"]) == 2
      and "[citation:txt2]" in sec_["content"] and "[citation:txt1, txt2]" in sec_["content"] and "txt0" not in sec_["content"])
check("rewritten ending claim passes the start/end check",
      G.boundary_claims(sec_["content"], sec_["retrieved_texts"], 2257) == [])
check("no txt0 -> section untouched", not G.attach_ending_source({"content": "A [citation:txt1].", "retrieved_texts": []}, item, False))
check("'final shot of the video’s opening montage' is not an ending claim",
      G.boundary_claims("This is the final shot of the video’s opening montage [citation:txt1].", texts, 2257) == [])

# --- P9 (a) + I28: server cap and token counting inside the lock ---------------------------------
class Tok:
    def __call__(self, text, add_special_tokens=True):
        return type("E", (), {"input_ids": text.split()})()
class Proc:
    tokenizer = Tok()
    def apply_chat_template(self, messages, tokenize=False, add_generation_prompt=True):
        return " ".join(str(m["content"]) for m in messages)
class FakeLLM:
    def __init__(self): self.model = type("M", (), {"processor": Proc()})(); self.kw = None
    def generate(self, messages, **kw): self.kw = kw; return "word " * 5
for cap, want in ((3072, 3072), (None, 8192)):
    llm = FakeLLM()
    client = L.create_app(llm, "qwen3vl-8b", 8192, cap).test_client()
    r = client.post("/v1/chat/completions", json={"messages": [{"role": "user", "content": "hi"}], "max_tokens": 8192})
    check(f"server cap {cap}: max_new_tokens = {want}, usage counted", r.status_code == 200 and llm.kw["max_new_tokens"] == want
          and r.get_json()["usage"]["completion_tokens"] == 5)
src = open(os.path.join(RF, "local_llm_server.py")).read()
check("count_tokens is called inside generate_lock", "with generate_lock:\n                content = llm.generate(messages, **gen_kwargs)" in src
      and src.index("usage = count_tokens(") < src.index("except Exception as e:\n            logger.exception(\"Generation failed\")"))

print("ALL PASS" if all(ok) else "SOME FAILED"); sys.exit(0 if all(ok) else 1)
