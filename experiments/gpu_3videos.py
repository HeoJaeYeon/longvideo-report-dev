"""
3-video run of the improved pipeline on real models, one or more LLM servers plus one aux GPU. GPUs may be shared
with another user's processes, which must never be disturbed.
  LLM servers  --llm-gpus (default: --llm-gpu 7): one local_llm_server per entry (a GPU may repeat), ports 18810+i,
               cap --llm-cap-mib per server (default 19,000 MiB; 0 = no cap). Prebuild OpenIE uses all of them
               (round-robin); reports use the first one.
  aux GPU      --aux-gpu (6): phase 1 prebuild_episodic_index.py (embedding only), then phase 2 the retrieval service
               (L1), cap --aux-cap-mib (default 15,000 MiB; 0 = no cap)
  Phase 1  pre-indexing (decision 1 = A, long-passage split + output guards) -> paths.episodic_cache_root
  Phase 2  run_report.py for each video, one after another (the service loads each video on preflight);
           skipped with --skip-reports
Watchdog: if a used GPU's total memory exceeds --abort-used-mib, only our processes are stopped.
Before starting, each used GPU must have free >= sum(per-process need) + 2,000 MiB, where the need of a process is
its cap, or EXPECT_MIB (measured peak of one Qwen3-VL-8B server / indexer / service, rounded up) when uncapped.
Outputs: outputs/3videos_<stamp>/
Usage: python experiments/gpu_3videos.py [--llm-gpus 4,4,5,5,6,6,7 --aux-gpu 7] [--skip-prebuild] [--skip-reports] [--videos a,b,c]
"""
import argparse, json, os, signal, subprocess, sys, threading, time
from collections import Counter
import requests, yaml

HERE = os.path.dirname(os.path.abspath(__file__))
RF = os.path.dirname(HERE)
sys.path.insert(0, RF)
from rf_config import load_config  # noqa: E402
PY = os.environ.get("RF_PYTHON", "/opt/venv/bin/python")   # Python with worldmm/hipporag (container venv)
WORLDMM = load_config(os.path.join(RF, "config.yaml"))["paths"]["worldmm_root"]
VIDEOS = ["-QuCz7kxBr8", "0RxMZBLeqRI", "54k2g9ddy4M"]
QUERY = ("Write a report describing what happens in this video: the main people or subjects, "
         "the key events in the order they occur, and how the video concludes.")
LLM_PORT, SVC_PORT, LLM_CAP = 18810, 18820, 19000
EXPECT_MIB = 19000


def start(cmd, gpu, log, cwd=HERE, extra_env=None):
    env = dict(os.environ, CUDA_VISIBLE_DEVICES=str(gpu), PYTHONDONTWRITEBYTECODE="1", **(extra_env or {}))
    return subprocess.Popen(cmd, env=env, stdout=open(log, "w"), stderr=subprocess.STDOUT, cwd=cwd)


def wait_health(url, proc, timeout=900):
    t = time.time()
    while time.time() - t < timeout:
        if proc.poll() is not None:
            raise RuntimeError(f"process exited ({proc.returncode}) before {url} was ready")
        try:
            if requests.get(url, timeout=2).ok:
                return round(time.time() - t, 1)
        except requests.RequestException:
            pass
        time.sleep(5)
    raise RuntimeError(f"{url} not ready after {timeout}s")


def gpu_mem(gpus):
    out = subprocess.run(["nvidia-smi", "--query-gpu=index,memory.used,memory.total", "--format=csv,noheader,nounits",
                          "-i", ",".join(map(str, gpus))], capture_output=True, text=True, timeout=10).stdout
    return {int(a): (int(b), int(c)) for a, b, c in (l.split(",") for l in out.strip().splitlines())}


def stop_all(procs):
    for p in procs:
        if p.poll() is None:
            p.send_signal(signal.SIGTERM)
    for p in procs:
        try:
            p.wait(timeout=30)
        except subprocess.TimeoutExpired:
            p.kill()


class Watch:
    """Peak memory per GPU; stops our processes if a GPU's total use exceeds the abort threshold."""
    def __init__(self, gpus, abort_mib, procs):
        self.gpus, self.abort_mib, self.procs = gpus, abort_mib, procs
        self.peaks, self.aborted, self.stop = {}, None, threading.Event()
        threading.Thread(target=self.run, daemon=True).start()

    def run(self):
        while not self.stop.is_set():
            try:
                for i, (used, _) in gpu_mem(self.gpus).items():
                    self.peaks[i] = max(self.peaks.get(i, 0), used)
                    if used > self.abort_mib and not self.aborted:
                        self.aborted = f"GPU {i} used {used} MiB > {self.abort_mib}"
                        print(f"[watchdog] {self.aborted}: stopping our processes", flush=True)
                        stop_all(self.procs)
            except Exception:
                pass
            self.stop.wait(2)


def count_calls(logs):
    return sum(sum(1 for l in open(f, errors="replace") if "chat.completions:" in l) for f in logs if os.path.isfile(f))


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--skip-prebuild", action="store_true")
    ap.add_argument("--skip-reports", action="store_true")
    ap.add_argument("--videos", default=",".join(VIDEOS))
    ap.add_argument("--llm-gpu", type=int, default=7)
    ap.add_argument("--llm-gpus", default="", help="comma-separated GPU per LLM server, e.g. 4,4,5,5,6,6,7")
    ap.add_argument("--llm-cap-mib", type=int, default=LLM_CAP, help="per-server cap; 0 = no cap")
    ap.add_argument("--aux-gpu", type=int, default=6)
    ap.add_argument("--aux-cap-mib", type=int, default=15000, help="indexer/service cap; 0 = no cap")
    ap.add_argument("--abort-used-mib", type=int, default=47500)
    ap.add_argument("--out", default=None)
    args = ap.parse_args()
    videos = [v for v in args.videos.split(",") if v]
    llm_gpus = [int(g) for g in args.llm_gpus.split(",") if g] or [args.llm_gpu]
    out = args.out or os.path.join(RF, "outputs", "3videos_" + time.strftime("%Y%m%d_%H%M%S"))
    os.makedirs(out, exist_ok=True)
    gpus = sorted(set(llm_gpus + [args.aux_gpu]))
    base = gpu_mem(gpus)
    summary = {"videos": videos, "query": QUERY, "gpus": {"llm": llm_gpus, "aux": args.aux_gpu},
               "caps_mib": {"llm": args.llm_cap_mib, "aux": args.aux_cap_mib}, "gpu_baseline_used_mib": {i: u for i, (u, _) in base.items()}}
    print(f"[start] out={out} baseline={summary['gpu_baseline_used_mib']}", flush=True)
    need = Counter()
    for g in llm_gpus:
        need[g] += args.llm_cap_mib or EXPECT_MIB
    need[args.aux_gpu] += args.aux_cap_mib or EXPECT_MIB
    for g in gpus:
        used, total = base[g]
        if total - used < need[g] + 2000:
            raise SystemExit(f"GPU {g}: free {total - used} MiB < need {need[g]} + 2000; not starting")
    procs = []
    watch = Watch(gpus, args.abort_used_mib, procs)
    cfg_path = os.path.join(out, "config.yaml")
    cfg = load_config(os.path.join(RF, "config.yaml"))
    cfg["llm"]["local"]["endpoint"]["port"] = LLM_PORT
    cfg["service"]["port"] = SVC_PORT
    cfg["report"].update({"outputs_dir": os.path.join(out, "reports"), "deep_reporter_log_dir": os.path.join(out, "dr_logs")})
    yaml.safe_dump(cfg, open(cfg_path, "w"), sort_keys=False, allow_unicode=True)
    llm_logs = [os.path.join(out, f"llm_server_{i}_gpu{g}.log") for i, g in enumerate(llm_gpus)]
    try:
        servers = []
        for i, g in enumerate(llm_gpus):
            if args.llm_cap_mib:
                cmd = [PY, "-B", os.path.join(RF, "scripts", "launch", "run_llm_server_capped.py"), str(LLM_PORT + i)]
            else:
                cmd = [PY, "-B", os.path.join(RF, "local_llm_server.py"), "--config", cfg_path, "--port", str(LLM_PORT + i)]
            servers.append(start(cmd, g, llm_logs[i]))
            procs.append(servers[-1])
        summary["llm_ready_sec"] = [wait_health(f"http://127.0.0.1:{LLM_PORT + i}/health", s) for i, s in enumerate(servers)]
        print(f"[llm] {len(servers)} server(s) ready in {summary['llm_ready_sec']}s", flush=True)

        if not args.skip_prebuild:
            t0 = time.time()
            endpoints = ",".join(f"http://127.0.0.1:{LLM_PORT + i}/v1" for i in range(len(servers)))
            idx = start([PY, "-B", os.path.join(RF, "prebuild_episodic_index.py"), "--config", os.path.join(RF, "config.yaml"),
                         f"--videos={','.join(videos)}", "--llm-endpoints", endpoints,
                         "--gpu-mem-cap-mib", str(args.aux_cap_mib)],
                        args.aux_gpu, os.path.join(out, "prebuild_indexer.log"), cwd=WORLDMM,
                        extra_env={"PYTORCH_CUDA_ALLOC_CONF": "expandable_segments:True"})
            procs.append(idx)
            rc = idx.wait()
            summary["prebuild"] = {"exit": rc, "wall_sec": round(time.time() - t0, 1), "llm_calls": count_calls(llm_logs)}
            print(f"[prebuild] {summary['prebuild']}", flush=True)
        done = os.path.join(cfg["paths"]["episodic_cache_root"], "_done")
        summary["done_markers"] = {v: os.path.isfile(os.path.join(done, f"{v}.qwen3vl-8b.json")) for v in videos}
        if watch.aborted or not all(summary["done_markers"].values()):
            print(f"[stop] prebuild incomplete or aborted: {summary['done_markers']} {watch.aborted}", flush=True)
            return
        if args.skip_reports:
            print("[stop] --skip-reports: prebuild only", flush=True)
            return

        if args.aux_cap_mib:
            svc_cmd = [PY, "-B", os.path.join(RF, "scripts", "launch", "run_service_capped.py"), cfg_path, f"--preload={videos[0]}"]
        else:
            svc_cmd = [PY, "-B", os.path.join(RF, "videorag_retriever_service.py"), "--config", cfg_path, f"--preload={videos[0]}"]
        svc = start(svc_cmd, args.aux_gpu, os.path.join(out, "service.log"), extra_env={"GPU_MEM_CAP_MIB": str(args.aux_cap_mib)})
        procs.append(svc)
        summary["service_ready_sec"] = wait_health(f"http://127.0.0.1:{SVC_PORT}/health", svc)
        print(f"[service] ready in {summary['service_ready_sec']}s", flush=True)
        summary["reports"] = {}
        for vid in videos:
            if watch.aborted:
                break
            od = os.path.join(out, "reports", vid)
            n0, t = count_calls(llm_logs), time.time()
            rr = subprocess.run([PY, "-B", os.path.join(RF, "run_report.py"), "--config", cfg_path, f"--video-id={vid}",
                                 "--query", QUERY, "--out-dir", od],
                                env=dict(os.environ, CUDA_VISIBLE_DEVICES="", PYTHONDONTWRITEBYTECODE="1"),
                                capture_output=True, text=True, cwd=RF)
            open(os.path.join(out, f"run_report_{vid}.log"), "w").write(rr.stdout + rr.stderr)
            summary["reports"][vid] = {"exit": rr.returncode, "wall_sec": round(time.time() - t, 1), "out_dir": od,
                                       "llm_calls": count_calls(llm_logs) - n0}
            print(f"[report] {vid} {summary['reports'][vid]}", flush=True)
    finally:
        stop_all(procs)
        watch.stop.set()
        time.sleep(3)
        summary["aborted"] = watch.aborted
        summary["gpu_peak_used_mib"] = watch.peaks
        summary["gpu_after_used_mib"] = {i: u for i, (u, _) in gpu_mem(gpus).items()}
        summary["own_pids"] = [p.pid for p in procs]
        summary["own_pids_alive_after"] = [p.pid for p in procs if p.poll() is None]
        json.dump(summary, open(os.path.join(out, "summary.json"), "w"), indent=2, ensure_ascii=False)
        print("[summary]", json.dumps(summary, ensure_ascii=False), flush=True)


if __name__ == "__main__":
    main()
