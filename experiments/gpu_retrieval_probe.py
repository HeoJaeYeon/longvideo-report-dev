"""
C-3: retrieval check on the 4-granularity caches (real models). Reuses gpu_3videos' start/watchdog helpers.
  LLM server (L1/full filter)  --llm-gpu (4), port 18830, no cap
  services L0 / L1 / full      --svc-gpus (5,6,7), ports 18840-18842, no cap, one config copy per mode
For each video (the first is preloaded): POST /load (time, GPU memory after), then per mode the same text
requests (topk 20 = Deep-Reporter text_topk) and one image request; records meta (elapsed_sec, counts,
episodic_candidates, episodic_filter) and the granularity mix of the returned episodic evidence.
Outputs: <out>/probe.json, logs.  Usage: python experiments/gpu_retrieval_probe.py --out <dir>
"""
import argparse, copy, json, os, time
from collections import Counter
import requests, yaml
from gpu_3videos import PY, RF, VIDEOS, Watch, gpu_mem, start, stop_all, wait_health
from rf_config import load_config  # report_framework is on sys.path via gpu_3videos

LLM_PORT, SVC_PORT = 18830, 18840
MODES = ("L0", "L1", "full")
EXPECT_MIB = 19000
REQUESTS = [  # query_list per request, the same for every video (Deep-Reporter sends 2-3 queries per section)
    ["main people or subjects in the video", "who appears in the video"],
    ["key events in the order they occur", "what happens first and what happens next"],
    ["how the video concludes", "final scene and ending of the video"],
]


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--llm-gpu", type=int, default=4)
    ap.add_argument("--svc-gpus", default="5,6,7")
    ap.add_argument("--videos", default=",".join(VIDEOS))
    ap.add_argument("--abort-used-mib", type=int, default=47500)
    args = ap.parse_args()
    videos = [v for v in args.videos.split(",") if v]
    svc_gpus = [int(g) for g in args.svc_gpus.split(",")]
    assert len(svc_gpus) == len(MODES)
    os.makedirs(args.out, exist_ok=True)
    gpus = sorted(set([args.llm_gpu] + svc_gpus))
    base = gpu_mem(gpus)
    need = Counter([args.llm_gpu] + svc_gpus)
    for g in gpus:
        used, total = base[g]
        if total - used < need[g] * EXPECT_MIB + 2000:
            raise SystemExit(f"GPU {g}: free {total - used} MiB < need {need[g] * EXPECT_MIB} + 2000; not starting")
    result = {"videos": videos, "requests": REQUESTS, "gpus": {"llm": args.llm_gpu, "services": dict(zip(MODES, svc_gpus))},
              "gpu_baseline_used_mib": {i: u for i, (u, _) in base.items()}, "loads": [], "searches": []}
    procs = []
    watch = Watch(gpus, args.abort_used_mib, procs)
    cfg0 = load_config(os.path.join(RF, "config.yaml"))
    cfg0["llm"]["local"]["endpoint"]["port"] = LLM_PORT
    cfg0["service"]["frames_dir"] = os.path.join(args.out, "frames")
    try:
        llm = start([PY, "-B", os.path.join(RF, "local_llm_server.py"), "--config", os.path.join(RF, "config.yaml"),
                     "--port", str(LLM_PORT)], args.llm_gpu, os.path.join(args.out, "llm_server.log"))
        procs.append(llm)
        svcs = {}
        for i, (mode, g) in enumerate(zip(MODES, svc_gpus)):
            cfg = copy.deepcopy(cfg0)
            cfg["retrieval"]["episodic_filter"] = mode
            cfg["service"]["port"] = SVC_PORT + i
            path = os.path.join(args.out, f"config_{mode}.yaml")
            yaml.safe_dump(cfg, open(path, "w"), sort_keys=False, allow_unicode=True)
            svcs[mode] = start([PY, "-B", os.path.join(RF, "videorag_retriever_service.py"), "--config", path,
                                f"--preload={videos[0]}"], g, os.path.join(args.out, f"service_{mode}.log"))
            procs.append(svcs[mode])
        result["llm_ready_sec"] = wait_health(f"http://127.0.0.1:{LLM_PORT}/health", llm)
        result["service_ready_sec"] = {m: wait_health(f"http://127.0.0.1:{SVC_PORT + i}/health", svcs[m], timeout=1800)
                                       for i, m in enumerate(MODES)}
        print(f"[ready] llm {result['llm_ready_sec']}s services {result['service_ready_sec']}", flush=True)
        for vid in videos:
            for i, mode in enumerate(MODES):
                if watch.aborted:
                    raise SystemExit(f"watchdog: {watch.aborted}")
                url = f"http://127.0.0.1:{SVC_PORT + i}/videos/{vid}"
                t = time.time()
                r = requests.post(f"{url}/load", timeout=1800)
                load = {"video": vid, "mode": mode, "status": r.status_code, "sec": round(time.time() - t, 1),
                        "body": r.json(), "gpu_used_mib_after": gpu_mem([svc_gpus[i]])[svc_gpus[i]][0]}
                result["loads"].append(load)
                print(f"[load] {vid} {mode} {load['status']} {load['sec']}s gpu={load['gpu_used_mib_after']}", flush=True)
                if r.status_code != 200:
                    continue
                for kind, qs in [("text", q) for q in REQUESTS] + [("image", REQUESTS[1])]:
                    t = time.time()
                    r = requests.post(f"{url}/search", json={"query_list": qs, "type": kind, "topk": 20 if kind == "text" else 10},
                                      timeout=900)
                    body = r.json()
                    res = body.get("results", [])
                    rec = {"video": vid, "mode": mode, "type": kind, "queries": qs, "status": r.status_code,
                           "wall_sec": round(time.time() - t, 2), "meta": body.get("meta"), "total_hits": body.get("total_hits"),
                           "granularity_mix": dict(Counter(x.get("granularity") for x in res if x.get("source") == "worldmm-episodic")),
                           "evidence": [x.get("content") or x.get("caption") for x in res]}
                    result["searches"].append(rec)
                    print(f"[search] {vid} {mode} {kind} {r.status_code} {rec['wall_sec']}s mix={rec['granularity_mix']} "
                          f"meta={ {k: rec['meta'].get(k) for k in ('episodic_candidates', 'episodic_filter', 'counts', 'elapsed_sec')} if rec['meta'] else None}",
                          flush=True)
    finally:
        stop_all(procs)
        watch.stop.set()
        time.sleep(3)
        result["aborted"] = watch.aborted
        result["gpu_peak_used_mib"] = watch.peaks
        result["gpu_after_used_mib"] = {i: u for i, (u, _) in gpu_mem(gpus).items()}
        result["own_pids_alive_after"] = [p.pid for p in procs if p.poll() is None]
        json.dump(result, open(os.path.join(args.out, "probe.json"), "w"), indent=1, ensure_ascii=False)
        print(f"[done] aborted={watch.aborted} peaks={watch.peaks} alive_after={result['own_pids_alive_after']}", flush=True)


if __name__ == "__main__":
    main()
