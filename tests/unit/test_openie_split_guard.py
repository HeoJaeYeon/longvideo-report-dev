"""CPU test: long-passage split OpenIE + output guards in prebuild_episodic_index.py (2026-10-22 fix).
Inputs: real 10min captions, the 14 real failed OpenIE responses of the stopped 3-video run (indexer log),
and fake OpenAI-compatible servers. No GPU, writes only under a temp dir."""
import json, os, re, sys, tempfile, threading
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
HERE = os.path.dirname(os.path.abspath(__file__))
RF = os.path.dirname(os.path.dirname(HERE))
sys.path.insert(0, RF)
from rf_config import load_config  # noqa: E402
CFG = load_config(os.path.join(RF, "config.yaml"))
os.environ["HF_HOME"] = CFG["paths"]["hf_home"]   # before importing torch/transformers (via worldmm)
from flask import Flask, jsonify, request
from werkzeug.serving import make_server
import prebuild_episodic_index as P
from worldmm.memory.episodic.utils import NerRawOutput, TripleRawOutput

ok = []
def check(name, cond): ok.append(bool(cond)); print(("PASS " if cond else "FAIL ") + name)

CAP = CFG["paths"]["caption_dir"]
LOG = os.path.join(os.path.dirname(HERE), "fixtures", "prebuild_indexer_20261022.log")   # = outputs/3videos_20261022_120438/prebuild_indexer.log

# --- split_passage on real 10min captions -------------------------------------------------------
long_caps = json.load(open(f"{CAP}/0RxMZBLeqRI/10min.json"))
for idx in (0, 1):
    text = long_caps[idx]["text"]
    pieces = P.split_passage(text)
    norm = lambda s: re.sub(r"\s+", " ", s).strip()
    check(f"split c{idx}: {P.count_tokens(text)} tok -> {len(pieces)} pieces, each <= {P.SPLIT_PIECE_TOKENS} tok",
          len(pieces) >= 2 and all(P.count_tokens(p) <= P.SPLIT_PIECE_TOKENS for p in pieces))
    check(f"split c{idx}: no text lost or reordered", norm(" ".join(pieces)) == norm(text))
one_para = "First sentence here. " * 400
pcs = P.split_passage(one_para)
check("single long paragraph split by sentences", len(pcs) >= 2 and all(P.count_tokens(p) <= P.SPLIT_PIECE_TOKENS for p in pcs))

# --- salvage on the 14 real failed responses ---------------------------------------------------
log = open(LOG, errors="replace").read()
bodies = []
for m in re.finditer(r"worldmm\.llm\.qwen3vl WARNING Failed to parse response as JSON:", log):
    nxt = re.search(r"\d{4}-\d\d-\d\d \d\d:\d\d:\d\d,\d+ |NER:|Extracting triples:", log[m.end():])
    bodies.append(log[m.end(): m.end() + (nxt.start() if nxt else len(log))])
check(f"14 real failed responses found in log (got {len(bodies)})", len(bodies) == 14)
n_ner = n_tri = 0
for b in bodies:
    if b.lstrip().startswith("["):
        r = P.salvage_structured(b, NerRawOutput); n_ner += 1
        assert 0 < len(r.named_entities) <= P.MAX_SALVAGED_ENTITIES and len(set(r.named_entities)) == len(r.named_entities)
    else:
        r = P.salvage_structured(b, TripleRawOutput); n_tri += 1
        cut = P.cut_long_runs(r.triples)
        run = best = 1
        for a, c in zip(cut, cut[1:]):
            run = run + 1 if a[:2] == c[:2] else 1; best = max(best, run)
        assert len(cut) > 0 and best <= P.MAX_SAME_SUBJ_PRED_RUN
check(f"all real failures salvaged (NER {n_ner}, triples {n_tri}), runs <= {P.MAX_SAME_SUBJ_PRED_RUN}, NER <= {P.MAX_SALVAGED_ENTITIES}", n_ner + n_tri == 14)

# --- salvage edge cases ------------------------------------------------------------------------
r = P.salvage_structured('{"triples": [["a", "b", "c"], ["d", "e", true], ["f", "g", "h"]]}', TripleRawOutput)
check("non-string items dropped (pydantic bool case)", r.triples == [["a", "b", "c"], ["f", "g", "h"]])
r = P.salvage_structured('```json\n{"named_entities": ["A", "B", "A", "C', NerRawOutput)
check("truncated fenced NER -> complete unique items", r.named_entities == ["A", "B"])
try:
    P.salvage_structured('{"triples": [["a", "b"', TripleRawOutput); check("nothing salvageable raises", False)
except ValueError:
    check("nothing salvageable raises", True)
check("cut_long_runs keeps first N of a run only",
      len(P.cut_long_runs([["s", "p", str(i)] for i in range(40)] + [["x", "p", "1"]])) == P.MAX_SAME_SUBJ_PRED_RUN + 1)
check("cut_long_runs keeps interleaved runs", len(P.cut_long_runs([["s", "p", str(i)] if i % 2 else ["t", "p", str(i)] for i in range(40)])) == 40)

# --- write_cache_docs ----------------------------------------------------------------------------
tmp = tempfile.mkdtemp()
cf = os.path.join(tmp, "g", "openie_results_ner_x.json")
P.write_cache_docs(cf, [{"idx": "chunk-1", "passage": "p1", "extracted_entities": [], "extracted_triples": [["a", "b", "c"]]}])
added = P.write_cache_docs(cf, [{"idx": "chunk-1", "passage": "CHANGED", "extracted_entities": [], "extracted_triples": []},
                                {"idx": "chunk-2", "passage": "p2", "extracted_entities": [], "extracted_triples": []}])
docs = json.load(open(cf))["docs"]
check("cache merge keeps existing, adds new only", added == 1 and [d["idx"] for d in docs] == ["chunk-1", "chunk-2"] and docs[0]["passage"] == "p1")

# --- HttpLLMModel guards + split OpenIE through fake servers -----------------------------------
mode = {"v": "ok"}
def reply(body):
    last = body["messages"][-1]["content"]
    if "named_entities" not in last:          # NER call
        return '["Roma", "Bucharest", "Roma", "Vienna'           # truncated
    if mode["v"] == "garbage":
        return "no json here"
    trip = [["Roma", "linked to", f"x{i}"] for i in range(30)] + [["Bucharest", "is in", "Romania"]]
    return '{"triples": ' + json.dumps(trip)[:-1] + ', ["Vienna", "is in'   # loop + truncated
calls = {"n": 0}
def fake(port):
    app = Flask(f"f{port}")
    @app.get("/health")
    def h(): return jsonify({"status": "ok", "model": "qwen3vl-8b"})
    @app.post("/v1/chat/completions")
    def c():
        calls["n"] += 1
        return jsonify({"choices": [{"message": {"content": reply(request.get_json())}, "finish_reason": "length"}]})
    s = make_server("127.0.0.1", port, app, threaded=True)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s
srv = fake(18793)
llm = P.make_http_llm_model(["http://127.0.0.1:18793/v1"], "qwen3vl-8b", "qwen3vl-8b")
from worldmm.memory.episodic.openie import OpenIE
oie = OpenIE(llm_model=llm)
ner = oie.ner("chunk-z", "Roma live in Bucharest and Vienna.")
check("truncated NER salvaged in 1 call", ner.unique_entities == ["Roma", "Bucharest"] and not ner.metadata and calls["n"] == 1)
tri = oie.triple_extraction("chunk-z", "Roma live in Bucharest.", ner.unique_entities)
check("truncated looping triples salvaged + cut", len(tri.triples) == P.MAX_SAME_SUBJ_PRED_RUN + 1 and not tri.metadata
      and llm.guard == {"salvaged_ner": 1, "salvaged_triples": 1, "cut_triples": 30 - P.MAX_SAME_SUBJ_PRED_RUN})
text = long_caps[0]["text"]
key = P.chunk_id(text)
split = {key: {"text": text, "pieces": P.split_passage(text)}}
docs, stats = P.openie_split_docs(oie, split)
check("split OpenIE merges pieces into one doc per chunk",
      len(docs) == 1 and docs[0]["idx"] == key and docs[0]["passage"] == text and stats["pieces"] == len(split[key]["pieces"])
      and stats["failed_pieces"] == 0 and docs[0]["extracted_entities"] == ["Roma", "Bucharest"]
      and len(docs[0]["extracted_triples"]) == P.MAX_SAME_SUBJ_PRED_RUN + 1)
mode["v"] = "garbage"; n0 = calls["n"]
tri2 = oie.triple_extraction("chunk-q", "x", ["Roma"])
check("unsalvageable output still retried (3 x 5 = 15) then empty with error",
      tri2.triples == [] and "error" in tri2.metadata and calls["n"] - n0 == 15)
srv.shutdown()

# --- plan_video counts split pieces -------------------------------------------------------------
cfg = load_config(os.path.join(RF, "config.yaml"))
cfg["paths"]["episodic_cache_root"] = tmp
plan = P.plan_video(cfg, "0RxMZBLeqRI", "qwen3vl-8b")
g = plan["granularities"]["10min"]
check(f"plan: 10min split {len(g['split'])} chunks / {g['split_pieces']} pieces, rest {g['to_compute']}",
      len(g["split"]) == 3 and g["to_compute"] == 1
      and plan["llm_calls"] == sum(2 * (s["to_compute"] + s["split_pieces"]) for s in plan["granularities"].values()))
print("ALL PASS" if all(ok) else "SOME FAILED"); sys.exit(0 if all(ok) else 1)
