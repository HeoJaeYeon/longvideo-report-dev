"""
Report batch on real models (C-4, C-5): N independent stacks run jobs in parallel.
  stack i on GPU g_i: one local_llm_server (port 18850+i) + one retrieval service (port 18860+i), no cap,
                      each with its own config copy; jobs run one after another per stack (service loads the video)
  job = (video, variant, repeat): run_report.py with the stack config + the variant's report.* overrides
Variants (--variants): comma list of names from VARIANTS. Default: "default" (current config).
Watchdog and start/stop helpers come from gpu_3videos.py. Outputs: <out>/summary.json, <out>/<job>/..., logs.
Usage: python tests/gpu_report_batch.py --out <dir> [--stack-gpus 4,5,6] [--videos a,b] [--variants v1,v2] [--repeats 1]
"""
import argparse, copy, json, os, queue, subprocess, threading, time
import yaml
from gpu_3videos import PY, QUERY, RF, VIDEOS, Watch, count_calls, gpu_mem, start, stop_all, wait_health

LLM_PORT, SVC_PORT, EXPECT_MIB = 18850, 18860, 19000
VARIANTS = {
    "default": {},
    "c0_written": {"previous_sections_context": "written", "translate_ko": False},
    "c0_off": {"previous_sections_context": "deep_reporter", "translate_ko": False},
}


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--stack-gpus", default="4,5,6")
    ap.add_argument("--videos", default=",".join(VIDEOS))
    ap.add_argument("--variants", default="default")
    ap.add_argument("--repeats", type=int, default=1)
    ap.add_argument("--query", default=QUERY)
    ap.add_argument("--abort-used-mib", type=int, default=47500)
    args = ap.parse_args()
    gpus = [int(g) for g in args.stack_gpus.split(",")]
    videos = [v for v in args.videos.split(",") if v]
    variants = [v for v in args.variants.split(",") if v]
    jobs = [(v, var, r) for r in range(1, args.repeats + 1) for var in variants for v in videos]
    os.makedirs(args.out, exist_ok=True)
    base = gpu_mem(sorted(set(gpus)))
    for g in set(gpus):
        used, total = base[g]
        need = gpus.count(g) * 2 * EXPECT_MIB
        if total - used < need + 2000:
            raise SystemExit(f"GPU {g}: free {total - used} MiB < need {need} + 2000; not starting")
    summary = {"stack_gpus": gpus, "query": args.query, "jobs": [list(j) for j in jobs],
               "variants": {v: VARIANTS[v] for v in variants}, "gpu_baseline_used_mib": {i: u for i, (u, _) in base.items()},
               "results": []}
    procs = []
    watch = Watch(sorted(set(gpus)), args.abort_used_mib, procs)
    cfg0 = yaml.safe_load(open(os.path.join(RF, "config.yaml")))
    lock = threading.Lock()
    try:
        stacks = []
        for i, g in enumerate(gpus):
            cfg = copy.deepcopy(cfg0)
            cfg["llm"]["local"]["endpoint"]["port"] = LLM_PORT + i
            cfg["service"]["port"] = SVC_PORT + i
            cfg["service"]["frames_dir"] = os.path.join(args.out, f"frames_s{i}")
            cfg["report"]["deep_reporter_log_dir"] = os.path.join(args.out, f"dr_logs_s{i}")
            path = os.path.join(args.out, f"config_s{i}.yaml")
            yaml.safe_dump(cfg, open(path, "w"), sort_keys=False, allow_unicode=True)
            llm_log = os.path.join(args.out, f"llm_server_s{i}_gpu{g}.log")
            llm = start([PY, "-B", os.path.join(RF, "local_llm_server.py"), "--config", path], g, llm_log)
            svc = start([PY, "-B", os.path.join(RF, "videorag_retriever_service.py"), "--config", path], g,
                        os.path.join(args.out, f"service_s{i}_gpu{g}.log"))
            procs += [llm, svc]
            stacks.append({"i": i, "gpu": g, "cfg": cfg, "llm": llm, "svc": svc, "llm_log": llm_log})
        for s in stacks:
            s["ready_sec"] = [wait_health(f"http://127.0.0.1:{LLM_PORT + s['i']}/health", s["llm"]),
                              wait_health(f"http://127.0.0.1:{SVC_PORT + s['i']}/health", s["svc"], timeout=1800)]
        summary["ready_sec"] = {s["i"]: s["ready_sec"] for s in stacks}
        print(f"[ready] {summary['ready_sec']}", flush=True)

        q = queue.Queue()
        for j in jobs:
            q.put(j)

        def worker(s):
            while not watch.aborted:
                try:
                    vid, var, rep = q.get_nowait()
                except queue.Empty:
                    return
                name = f"{vid}__{var}__r{rep}"
                cfg = copy.deepcopy(s["cfg"])
                cfg["report"].update(VARIANTS[var])
                path = os.path.join(args.out, f"config_{name}.yaml")
                yaml.safe_dump(cfg, open(path, "w"), sort_keys=False, allow_unicode=True)
                n0, t = count_calls([s["llm_log"]]), time.time()
                rr = subprocess.run([PY, "-B", os.path.join(RF, "run_report.py"), "--config", path, f"--video-id={vid}",
                                     "--query", args.query, "--out-dir", os.path.join(args.out, name)],
                                    env=dict(os.environ, CUDA_VISIBLE_DEVICES="", PYTHONDONTWRITEBYTECODE="1"),
                                    capture_output=True, text=True, cwd=RF)
                open(os.path.join(args.out, f"run_report_{name}.log"), "w").write(rr.stdout + rr.stderr)
                rec = {"job": name, "video": vid, "variant": var, "repeat": rep, "stack": s["i"], "gpu": s["gpu"],
                       "exit": rr.returncode, "wall_sec": round(time.time() - t, 1), "llm_calls": count_calls([s["llm_log"]]) - n0}
                with lock:
                    summary["results"].append(rec)
                print(f"[report] {rec}", flush=True)

        threads = [threading.Thread(target=worker, args=(s,)) for s in stacks]
        for th in threads:
            th.start()
        for th in threads:
            th.join()
    finally:
        stop_all(procs)
        watch.stop.set()
        time.sleep(3)
        summary["aborted"] = watch.aborted
        summary["gpu_peak_used_mib"] = watch.peaks
        summary["gpu_after_used_mib"] = {i: u for i, (u, _) in gpu_mem(sorted(set(gpus))).items()}
        summary["own_pids_alive_after"] = [p.pid for p in procs if p.poll() is None]
        json.dump(summary, open(os.path.join(args.out, "summary.json"), "w"), indent=2, ensure_ascii=False)
        print(f"[done] aborted={watch.aborted} peaks={watch.peaks} alive_after={summary['own_pids_alive_after']}", flush=True)


if __name__ == "__main__":
    main()
