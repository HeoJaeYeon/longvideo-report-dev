"""CPU test: prebuild HttpLLMModel request contract + parsing + retry (fake OpenAI-compatible servers)."""
import json, os, sys, threading
os.environ.setdefault("CUDA_VISIBLE_DEVICES", "")
HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, os.path.dirname(HERE))
from flask import Flask, jsonify, request
from werkzeug.serving import make_server
import prebuild_episodic_index as P

seen, fails = [], {"n": 0}

def fake(port, reply):
    app = Flask(f"fake{port}")
    @app.get("/health")
    def h(): return jsonify({"status": "ok", "model": "qwen3vl-8b"})
    @app.post("/v1/chat/completions")
    def c():
        body = request.get_json(); seen.append((port, body))
        if fails["n"] > 0:
            fails["n"] -= 1
            return jsonify({"error": "boom"}), 500
        return jsonify({"choices": [{"message": {"content": reply(body)}, "finish_reason": "stop"}]})
    s = make_server("127.0.0.1", port, app, threaded=True)
    threading.Thread(target=s.serve_forever, daemon=True).start()
    return s

def reply(body):
    last = body["messages"][-1]["content"]
    return '```json\n["Chris", "court"]\n```' if "named_entities" not in last else '{"triples": [["Chris", "shoots", "ball"], ["bad"]]}'

servers = [fake(18791, reply), fake(18792, reply)]
eps = ["http://127.0.0.1:18791/v1", "http://127.0.0.1:18792/v1"]
ok = []
def check(name, cond): ok.append(cond); print(("PASS " if cond else "FAIL ") + name)

P.check_endpoints(eps, "qwen3vl-8b"); check("health/model check", True)
try:
    P.check_endpoints(eps, "other"); check("model mismatch rejected", False)
except SystemExit: check("model mismatch rejected", True)

llm = P.make_http_llm_model(eps, "qwen3vl-8b", "qwen3vl-8b")
from worldmm.memory.episodic.openie import OpenIE
oie = OpenIE(llm_model=llm)
ner = oie.ner("chunk-x", "Chris shoots a ball on the court.")
check("NER parsed via bare-array wrap", ner.unique_entities == ["Chris", "court"] and not ner.metadata)
body = seen[-1][1]
from worldmm.llm import PromptTemplateManager
expected = PromptTemplateManager(role_mapping={"system": "system", "user": "user", "assistant": "assistant"}).render(name="ner", passage="Chris shoots a ball on the court.")
check("messages identical to in-process prompt", body["messages"] == expected)
check("max_tokens=2048, no sampling override", body["max_tokens"] == 2048 and "temperature" not in body and "top_p" not in body)
tri = oie.triple_extraction("chunk-x", "Chris shoots a ball.", ["Chris"])
check("triples parsed + invalid filtered", tri.triples == [["Chris", "shoots", "ball"]])
check("round-robin over endpoints", {p for p, _ in seen} == {18791, 18792})
fails["n"] = 2
llm.failures = 0
ner2 = oie.ner("chunk-y", "Zach dribbles.")
check("HTTP 500 retried then success", ner2.unique_entities == ["Chris", "court"] and llm.failures == 2)
check("model_name label for OpenIE file name", llm.model_name == "qwen3vl-8b")
for s in servers: s.shutdown()
print("ALL PASS" if all(ok) else "SOME FAILED"); sys.exit(0 if all(ok) else 1)
