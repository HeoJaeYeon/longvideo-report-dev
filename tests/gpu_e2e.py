"""
GPU end-to-end validation (real models; GPUs 4/6/7; every model process capped at 19,000 MiB).
  1. local_llm_server (Qwen3-VL-8B) on GPU 4, retrieval service (L1) on GPU 6
     -- real 10sec-only cache of -QuCz7kxBr8 (tests/_artifacts/gpu_test), same as the smoke run
  2. run_report.py with the smoke query  -> outputs, validation, translation (decisions 5/6, rule 4)
  3. retrieval service in `full` mode on GPU 7 -> one real text search (LLM calls, latency)
Only the processes started here are terminated. Outputs: tests/_artifacts/gpu_e2e/
"""
import copy, json, os, signal, subprocess, sys, threading, time
import requests, yaml

HERE = os.path.dirname(os.path.abspath(__file__))
RF = os.path.dirname(HERE)
OUT = os.path.join(HERE, "_artifacts", "gpu_e2e")
PY = "/opt/venv/bin/python"
VID = "-QuCz7kxBr8"
QUERY = "Write a report describing what happens in this video: who takes part, what is tested, and how the tests turn out."
LLM_PORT, SVC_PORT, FULL_PORT = 18610, 18620, 18630


def make_config(path, port, mode):
    cfg = yaml.safe_load(open(os.path.join(RF, "config.yaml")))
    cfg["paths"]["episodic_cache_root"] = os.path.join(HERE, "_artifacts", "gpu_test", "episodic")
    cfg["worldmm"]["granularities"] = ["10sec"]
    cfg["retrieval"]["episodic_candidates_per_query"] = {"10sec": 6}
    cfg["retrieval"]["episodic_filter"] = mode
    cfg["llm"]["local"]["endpoint"]["port"] = LLM_PORT
    cfg["service"].update({"port": port, "frames_dir": os.path.join(OUT, "frames_cache")})
    cfg["report"].update({"outputs_dir": os.path.join(OUT, "outputs"), "deep_reporter_log_dir": os.path.join(OUT, "dr_logs")})
    yaml.safe_dump(cfg, open(path, "w"), sort_keys=False, allow_unicode=True)
    return cfg


def start(cmd, gpu, log):
    env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(gpu), PYTHONDONTWRITEBYTECODE="1")
    return subprocess.Popen(cmd, env=env, stdout=open(log, "w"), stderr=subprocess.STDOUT, cwd=HERE)


def wait_health(url, proc, timeout=900):
    t = time.time()
    while time.time() - t < timeout:
        if proc.poll() is not None:
            raise RuntimeError(f"process exited ({proc.returncode}) before {url} was ready")
        try:
            if requests.get(url, timeout=2).ok:
                return time.time() - t
        except requests.RequestException:
            pass
        time.sleep(5)
    raise RuntimeError(f"{url} not ready after {timeout}s")


def gpu_poll(stop, peaks):
    while not stop.is_set():
        try:
            out = subprocess.run(["nvidia-smi", "--query-gpu=index,memory.used", "--format=csv,noheader,nounits", "-i", "4,6,7"],
                                 capture_output=True, text=True, timeout=10).stdout
            for line in out.strip().splitlines():
                i, m = (int(x) for x in line.split(","))
                peaks[i] = max(peaks.get(i, 0), m)
        except Exception:
            pass
        stop.wait(2)


def main():
    os.makedirs(OUT, exist_ok=True)
    cfg_l1 = os.path.join(OUT, "config_l1.yaml"); make_config(cfg_l1, SVC_PORT, "L1")
    cfg_full = os.path.join(OUT, "config_full.yaml"); make_config(cfg_full, FULL_PORT, "full")
    base = subprocess.run(["nvidia-smi", "--query-gpu=index,memory.used", "--format=csv,noheader,nounits", "-i", "4,6,7"],
                          capture_output=True, text=True).stdout
    print("[gpu baseline]", base.replace("\n", " | "), flush=True)
    stop, peaks = threading.Event(), {}
    threading.Thread(target=gpu_poll, args=(stop, peaks), daemon=True).start()
    procs, summary = [], {}
    try:
        llm = start([PY, "-B", "run_llm_server_capped.py", str(LLM_PORT)], 4, os.path.join(OUT, "llm_server.log")); procs.append(llm)
        svc = start([PY, "-B", "run_service_capped.py", cfg_l1, f"--preload={VID}"], 6, os.path.join(OUT, "service_l1.log")); procs.append(svc)
        print(f"[start] llm pid={llm.pid} (GPU4), service L1 pid={svc.pid} (GPU6)", flush=True)
        summary["llm_ready_sec"] = round(wait_health(f"http://127.0.0.1:{LLM_PORT}/health", llm), 1)
        summary["service_ready_sec"] = round(wait_health(f"http://127.0.0.1:{SVC_PORT}/health", svc), 1)
        print(f"[ready] llm {summary['llm_ready_sec']}s, service {summary['service_ready_sec']}s", flush=True)

        out_dir = os.path.join(OUT, "outputs", "report_run1")
        t = time.time()
        rr = subprocess.run([PY, "-B", os.path.join(RF, "run_report.py"), "--config", cfg_l1, f"--video-id={VID}",
                             "--query", QUERY, "--out-dir", out_dir],
                            env=dict(os.environ, CUDA_VISIBLE_DEVICES="", PYTHONDONTWRITEBYTECODE="1"),
                            capture_output=True, text=True, cwd=RF)
        open(os.path.join(OUT, "run_report.log"), "w").write(rr.stdout + rr.stderr)
        summary["run_report"] = {"exit": rr.returncode, "wall_sec": round(time.time() - t, 1), "out_dir": out_dir}
        print(f"[run_report] exit={rr.returncode} wall={summary['run_report']['wall_sec']}s", flush=True)

        full = start([PY, "-B", "run_service_capped.py", cfg_full, f"--preload={VID}"], 7, os.path.join(OUT, "service_full.log")); procs.append(full)
        summary["full_service_ready_sec"] = round(wait_health(f"http://127.0.0.1:{FULL_PORT}/health", full), 1)
        n0 = sum(1 for l in open(os.path.join(OUT, "llm_server.log")) if "chat.completions:" in l)
        t = time.time()
        r = requests.post(f"http://127.0.0.1:{FULL_PORT}/videos/{VID}/search",
                          json={"query_list": ["testing viral basketball gadgets", "dribbling speed time trial with goggles"],
                                "type": "text", "topk": 20}, timeout=1800)
        n1 = sum(1 for l in open(os.path.join(OUT, "llm_server.log")) if "chat.completions:" in l)
        body = r.json()
        summary["full_mode_search"] = {"status_code": r.status_code, "sec": round(time.time() - t, 1), "llm_calls": n1 - n0,
                                       "meta": body.get("meta"), "hits": body.get("total_hits"),
                                       "top": [x.get("content", "")[:120] for x in body.get("results", [])[:3]]}
        print(f"[full] {summary['full_mode_search']}", flush=True)
    finally:
        for p in procs:
            if p.poll() is None:
                p.send_signal(signal.SIGTERM)
        for p in procs:
            try:
                p.wait(timeout=30)
            except subprocess.TimeoutExpired:
                p.kill()
        stop.set()
        time.sleep(3)
        after = subprocess.run(["nvidia-smi", "--query-gpu=index,memory.used", "--format=csv,noheader,nounits", "-i", "4,6,7"],
                               capture_output=True, text=True).stdout
        summary["gpu_peak_mib"] = peaks
        summary["gpu_after"] = after.strip().replace("\n", " | ")
        summary["own_pids"] = [p.pid for p in procs]
        summary["own_pids_alive_after"] = [p.pid for p in procs if p.poll() is None]
        json.dump(summary, open(os.path.join(OUT, "summary.json"), "w"), indent=2, ensure_ascii=False)
        print("[summary]", json.dumps(summary, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
