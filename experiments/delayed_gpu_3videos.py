"""
Delayed, headroom-gated start of experiments/gpu_3videos.py on two GPUs (--gpus, default 6,7; may be shared with
another user's processes).
  1. sleep --delay-sec
  2. poll both GPUs every 30 s; keep the max used memory of the last --hold-sec per GPU
  3. start only when an assignment (llm, aux) keeps both GPUs below gpu_3videos' abort threshold with margin:
       max_used[llm] + 19,000 + margin <= abort  and  max_used[aux] + aux_cap + margin <= abort
     (of the two assignments, the one with the larger min slack is used); give up after --max-wait-sec
  4. run gpu_3videos.py once (no automatic retry: an aborted prebuild is inspected by hand)
Writes gate decisions to <out>/gate.json.  Usage: python experiments/delayed_gpu_3videos.py --out <dir> [--gpus 4,5]
"""
import argparse, json, os, subprocess, sys, time
from collections import deque

HERE = os.path.dirname(os.path.abspath(__file__))
sys.path.insert(0, HERE)
from gpu_3videos import LLM_CAP, PY, gpu_mem


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--out", required=True)
    ap.add_argument("--gpus", default="6,7", help="exactly two physical GPU indices: one for the LLM server, one for aux")
    ap.add_argument("--delay-sec", type=int, default=7200)
    ap.add_argument("--hold-sec", type=int, default=600)
    ap.add_argument("--max-wait-sec", type=int, default=6 * 3600)
    ap.add_argument("--margin-mib", type=int, default=1500)
    ap.add_argument("--aux-cap-mib", type=int, default=15000)
    ap.add_argument("--abort-used-mib", type=int, default=47500)
    args = ap.parse_args()
    gpus = tuple(int(g) for g in args.gpus.split(","))
    if len(gpus) != 2 or gpus[0] == gpus[1]:
        raise SystemExit(f"--gpus needs two different GPU indices, got {args.gpus!r}")
    os.makedirs(args.out, exist_ok=True)
    gate = {"planned_start": time.strftime("%Y-%m-%d %H:%M:%S", time.localtime(time.time() + args.delay_sec)),
            "args": vars(args)}
    print(f"[gate] sleeping {args.delay_sec}s until {gate['planned_start']}", flush=True)
    time.sleep(args.delay_sec)

    t0, window = time.time(), deque()
    need = args.hold_sec // 30
    choice = None
    while time.time() - t0 < args.max_wait_sec:
        used = {i: u for i, (u, _) in gpu_mem(gpus).items()}
        window.append(used)
        if len(window) > need:
            window.popleft()
        if len(window) == need:
            peak = {g: max(s[g] for s in window) for g in gpus}
            options = []
            for llm, aux in (gpus, gpus[::-1]):
                slack = min(args.abort_used_mib - peak[llm] - LLM_CAP, args.abort_used_mib - peak[aux] - args.aux_cap_mib)
                options.append((slack, llm, aux))
            slack, llm, aux = max(options)
            print(f"[gate] {time.strftime('%H:%M:%S')} peak{args.hold_sec}s={peak} best llm={llm} aux={aux} slack={slack}", flush=True)
            if slack >= args.margin_mib:
                choice = {"llm_gpu": llm, "aux_gpu": aux, "slack_mib": slack, "window_peak_mib": peak,
                          "start": time.strftime("%Y-%m-%d %H:%M:%S"), "waited_sec": round(time.time() - t0)}
                break
        time.sleep(30)
    gate["choice"] = choice
    json.dump(gate, open(os.path.join(args.out, "gate.json"), "w"), indent=2)
    if not choice:
        print("[gate] no safe headroom within max wait; not starting", flush=True)
        sys.exit(2)
    print(f"[gate] starting gpu_3videos {choice}", flush=True)
    rc = subprocess.run([PY, "-B", os.path.join(HERE, "gpu_3videos.py"), "--llm-gpu", str(choice["llm_gpu"]),
                         "--aux-gpu", str(choice["aux_gpu"]), "--aux-cap-mib", str(args.aux_cap_mib),
                         "--abort-used-mib", str(args.abort_used_mib), "--out", args.out], cwd=HERE).returncode
    sys.exit(rc)


if __name__ == "__main__":
    main()
