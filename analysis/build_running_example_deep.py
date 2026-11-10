"""
§10 of internal/running_example/RUNNING_EXAMPLE.md: presentation-grade deep dive into ONE report (-QuCz7kxBr8 r1, basketball)
(2026-11-02, CPU only, no LLM call). Called by analysis/build_running_example_combined.py (render()); running this file
alone only (re)writes the image assets.

What it adds beyond §2-§7, all read from the recorded files or recomputed with WorldMM's own code:
  - source inputs: video, Whisper transcript, the 226 10-second segments (WorldMM build_segments, checked against
    10sec.json start/end times)
  - caption generation: the exact frames (decord, one per integer second) and prompt text the captioner received
    for 4 segments, as image files
  - episodic memory: caption hierarchy windows (WorldMM _summarize_level grouping, checked against every level),
    full texts, OpenIE (NER, triples) incl. empty results and their logged causes, HippoRAG graph neighbourhood
  - semantic memory: 23 extraction groups (input/output counts, failures from the preprocessing log, truncation
    token counts), one group's input -> output, consolidation trajectory and diffs, final 153 triples
  - visual memory: embedding store, the 10 frames VLM2Vec embedded per segment (frame ranges from the preprocessing
    log, linspace as in qwen_vl_utils), resize size, as image files
  - per section: query prompt/output, graph search per query x granularity with HippoRAG scores, RRF list, exact L1
    filter prompt, semantic and visual rankings (from results/retrieval_repro_<vid>_r1.json, made by
    analysis/reproduce_retrieval_cpu.py, whose checks against the run must have passed), writer prompt/output,
    citation mapping and final body
Assets: internal/running_example/assets/-QuCz7kxBr8/ (referenced by relative path from the document).
"""
import collections, glob, hashlib, importlib.util, json, math, os, pickle, re, shutil, sys, tempfile

RF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RF)
sys.path.insert(0, os.path.join(RF, "analysis"))
import numpy as np
import yaml
import grounding_postprocessor as G
from export_stages import load_jobs, log_lines, cited_txt, cited_img
from build_running_example import WM, CAP, META, EPI, GRANS, sec, cut, cell, fence, details

VID = "-QuCz7kxBr8"
REPEAT = 1
RUN = os.path.join(RF, "outputs", "p9p19_check_20261025_141401")
JOB = f"{VID}__c0_written__r{REPEAT}"
ASSET_REL = f"assets/{VID}"                                  # relative to internal/running_example/
ASSET_DIR = os.path.join(RF, "internal", "running_example", ASSET_REL)
WMF = os.path.dirname(CAP)   # WorldMM memory folder (parent of caption/): transcript/, logs/
PRE_LOG = f"{WMF}/logs/{VID}.log"
VIDEO = f"{WM}/data/Video-MME/data/{VID}.mp4"
# 10sec segments shown frame by frame: the §3.2 example + the three segments whose center frames became Figure 1-3
FRAME_SEGMENTS = ["00004000", "00344000", "00285000", "00182000"]
HIER_END = 180          # caption hierarchy shown in full for [0, 180) s
OPENIE_ROWS_END = 60    # per-caption NER/triple table for [0, 60) s
ENTITY = "sports dribble specs"
SEM_GROUP = "100050000"  # semantic extraction example group
rel = lambda p: os.path.relpath(p, RF)


def load_module(name, path):
    spec = importlib.util.spec_from_file_location(name, path)
    m = importlib.util.module_from_spec(spec)
    sys.modules[name] = m
    spec.loader.exec_module(m)
    return m


def md5(t):
    return "chunk-" + hashlib.md5(t.encode("utf-8")).hexdigest()


def tt(ts):
    return G.hms_from_time_str(ts)


def windows(items, size):
    """WorldMM gen_multiscale._summarize_level grouping (one date): [(window_start_sec, items)]."""
    out, cur, b = [], None, []
    for x in sorted(items, key=lambda x: sec(x["start_time"])):
        s = sec(x["start_time"])
        if cur is None:
            cur = s
        if s < cur + size:
            b.append(x)
        else:
            out.append((cur, b))
            cur, b = (s // size) * size, [x]
    out.append((cur, b))
    return out


def clock(t):
    """seconds -> HH:MM:SS.mmm (truncated to ms, no rounding into the next second)"""
    ms = int(t * 1000)
    return f"{ms // 3600000:02d}:{ms // 60000 % 60:02d}:{ms // 1000 % 60:02d}.{ms % 1000:03d}"


def md_img(name, alt):
    return f"![{alt}]({ASSET_REL}/{name})"


# ---------------------------------------------------------------------------------------------- assets
def contact_sheet(images, labels, out, cols=5, tw=384):
    from PIL import Image, ImageDraw, ImageFont
    font = ImageFont.truetype("/usr/share/fonts/truetype/dejavu/DejaVuSans.ttf", 15)
    w0, h0 = images[0].size
    th = round(tw * h0 / w0)
    rows = math.ceil(len(images) / cols)
    sheet = Image.new("RGB", (cols * tw + (cols + 1) * 4, rows * (th + 24) + (rows + 1) * 4), "white")
    d = ImageDraw.Draw(sheet)
    for k, (im, lab) in enumerate(zip(images, labels)):
        r, c = divmod(k, cols)
        x, y = 4 + c * (tw + 4), 4 + r * (th + 28)
        sheet.paste(im.resize((tw, th)), (x, y))
        d.text((x + 2, y + th + 3), lab, fill="black", font=font)
    sheet.save(out, quality=90)


def build_assets(ctx):
    from PIL import Image
    import decord
    os.makedirs(os.path.join(ASSET_DIR, "frames"), exist_ok=True)
    vr = decord.VideoReader(VIDEO)
    fps = vr.get_avg_fps()
    made = []
    for st in FRAME_SEGMENTS:
        for kind, idx in (("caption", ctx["cap_frames"][st]["idx"]), ("vlm2vec", ctx["vis_frames"][st]["idx"])):
            arr = vr.get_batch(idx).asnumpy()
            ims = [Image.fromarray(a) for a in arr]
            for j, (im, fi) in enumerate(zip(ims, idx)):
                p = os.path.join(ASSET_DIR, "frames", f"{kind}_{st}_{j:02d}_f{fi}.jpg")
                im.save(p, quality=90)
            labels = [f"{clock(fi / fps)}  #{fi}" for fi in idx]
            name = f"{kind}_input_{st}.jpg"
            contact_sheet(ims, labels, os.path.join(ASSET_DIR, name))
            made.append(name)
    # center frames used by the run (copied, not re-extracted), plus a decord re-extraction check
    for s in ctx["outline"]:
        for m in s["retrieved_images"]:
            dst = os.path.join(ASSET_DIR, f"center_{m['start_time']}.jpg")
            shutil.copyfile(m["img_path"], dst)
            fi = min(int(m["frame_sec"] * fps), len(vr) - 1)
            a = vr[fi].asnumpy().astype(np.float32)
            b = np.asarray(Image.open(dst).convert("RGB"), dtype=np.float32)
            assert a.shape == b.shape and np.abs(a - b).mean() < 3.0, (m["start_time"], np.abs(a - b).mean())
    return made


# ---------------------------------------------------------------------------------------------- data
def load_ctx():
    c = {}
    c["cfg"] = yaml.safe_load(open(os.path.join(RUN, f"config_{JOB}.yaml")))
    rdir = os.path.join(RUN, JOB)
    rj = json.load(open(os.path.join(rdir, "report.json")))
    c["rj"], c["outline"] = rj, rj["outline"]
    c["vj"] = json.load(open(os.path.join(rdir, "validation.json")))
    c["report_md"] = open(os.path.join(rdir, "report.md"), encoding="utf-8").read()
    for p in glob.glob(os.path.join(RUN, "dr_logs_s*", "*.jsonl")):
        for line in open(p):
            d = json.loads(line)
            if d["session_id"] == rj["session_id"]:
                c["ses"] = d
    ses = c["ses"]
    t0, t1 = ses["start_time"][:19], ses["end_time"][:19]
    stack = load_jobs(RUN)[JOB]["stack"]
    c["llm"] = log_lines(glob.glob(os.path.join(RUN, f"llm_server_s{stack}_gpu*.log"))[0],
                         r"(\S+ \S+),\d+ local_llm_server INFO chat\.completions: prompt=(\d+) completion=(\d+) finish=(\w+) ([\d.]+)s",
                         t0, t1)
    c["svc"] = log_lines(glob.glob(os.path.join(RUN, f"service_s{stack}_gpu*.log"))[0],
                         r"(\S+ \S+),\d+ videorag_retriever INFO search (\w+): (.*)", t0, t1)
    n = len(c["outline"])
    assert len(c["llm"]) == 1 + 3 * n and len(c["svc"]) == 2 * n
    calls = ses["llm_calls"]
    assert [x["call_type"] for x in calls] == ["outline_generation"] + ["query_generation", "section_writing"] * n
    c["planner_call"] = calls[0]
    c["q_calls"] = [x for x in calls if x["call_type"] == "query_generation"]
    c["w_calls"] = [x for x in calls if x["call_type"] == "section_writing"]
    assert len(ses["search_calls"]) == n
    c["search_calls"] = ses["search_calls"]
    tmp = tempfile.mkdtemp(prefix="running_example_deep_")
    try:
        c["grounded"] = G.ground_report({"outline": c["outline"]}, False, tmp, header=None)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    body = c["report_md"].split("\n\n", 1)[1] if c["report_md"].startswith(">") else c["report_md"]
    assert c["grounded"]["markdown"] == body
    c["uid2ref"] = {r["uid"]: r["n"] for r in c["grounded"]["references"]}
    c["uid2fig"] = {f["uid"]: f["k"] for f in c["grounded"]["figures"]}
    rp = os.path.join(RF, "results", f"retrieval_repro_{VID}_r{REPEAT}.json")
    c["repro"] = json.load(open(rp))
    c["repro_path"] = rp
    assert c["repro"]["job"] == JOB and len(c["repro"]["sections"]) == n
    # WorldMM memories
    c["caps"] = {g: json.load(open(f"{CAP}/{VID}/{g}.json")) for g in GRANS}
    c["openie"] = json.load(open(f"{META}/episodic_memory/{VID}/openie_results_qwen3vl-8b.json"))
    c["etrip"] = json.load(open(f"{META}/episodic_memory/{VID}/episodic_triple_results_qwen3vl-8b.json"))
    c["sem_ext"] = json.load(open(f"{META}/semantic_memory/{VID}/semantic_extraction_results_qwen3vl-8b.json"))["semantic_triples"]
    c["sem_con"] = json.load(open(f"{META}/semantic_memory/{VID}/semantic_consolidation_results_qwen3vl-8b.json"))
    c["vis"] = pickle.load(open(f"{META}/visual_memory/{VID}/visual_embeddings.pkl", "rb"))
    c["pre_log"] = open(PRE_LOG, encoding="utf-8", errors="replace").read().split("\n")
    # caption-generation code (WorldMM, read-only import)
    gfc = load_module("wm_generate_fine_caption", f"{WM}/preprocess/episodic_memory/generate_fine_caption.py")
    c["gfc"] = gfc
    import decord
    vr = decord.VideoReader(VIDEO)
    dur, fps = gfc.get_video_duration(vr)
    c["dur"], c["fps"], c["nfr"], c["wh"] = dur, fps, len(vr), (vr[0].shape[1], vr[0].shape[0])
    from pathlib import Path
    c["transcript"] = gfc.parse_transcript(Path(f"{WMF}/transcript/{VID}.srt"))
    c["segments"] = gfc.build_segments(dur, c["transcript"], 10)
    assert len(c["segments"]) == len(c["caps"]["10sec"])
    for s_, e in zip(c["segments"], c["caps"]["10sec"]):
        assert gfc.format_caption_time(s_.start_seconds, round_up=False) == str(e["start_time"]).zfill(8)
        assert gfc.format_caption_time(s_.end_seconds, round_up=True) == str(e["end_time"]).zfill(8)
    c["cap_frames"] = {}
    for st in FRAME_SEGMENTS:
        k = next(i for i, e in enumerate(c["caps"]["10sec"]) if str(e["start_time"]).zfill(8) == st)
        seg = c["segments"][k]
        secs = gfc.compute_sample_seconds(seg.start_seconds, seg.end_seconds)
        idx = [min(max(int(round(s * fps)), 0), len(vr) - 1) for s in secs]
        c["cap_frames"][st] = {"k": k, "seg": seg, "secs": secs, "idx": idx}
    # VLM2Vec frame ranges from the successful visual run in the preprocessing log
    qvu = load_module("wm_vlm2vec_qwen_vl_utils",
                      f"{WM}/src/worldmm/embedding/VLM2Vec/src/model/vlm_backbone/qwen2_vl/qwen_vl_utils.py")
    c["qvu"] = qvu
    last_start = max(i for i, ln in enumerate(c["pre_log"]) if ln.startswith(f"[{VID}] START"))
    rng = {}
    pat = re.compile(r"calculate video frame range: start_frame=(\d+), end_frame=(\d+), total_frames=(\d+) "
                     r"from video_start=([\d.]+), video_end=([\d.]+), video_fps=([\d.]+)")
    for ln in c["pre_log"][last_start:]:
        m = pat.search(ln)
        if m:
            rng[float(m.group(4))] = (int(m.group(1)), int(m.group(2)), float(m.group(5)))
    c["vis_ranges"] = rng
    c["vis_backend"] = sorted({m.group(1) for ln in c["pre_log"][last_start:]
                               for m in [re.search(r"qwen-vl-utils using (\w+) to read video", ln)] if m})
    assert len(rng) == len(c["caps"]["10sec"]) == len(c["vis"])
    import torch
    c["vis_frames"] = {}
    for e in c["caps"]["10sec"]:
        s0, s1 = float(sec(e["start_time"])), float(sec(e["end_time"]))
        sf, ef, _ = qvu.calculate_video_frame_range({"video_start": s0, "video_end": s1}, c["nfr"], fps)
        assert (sf, ef) == rng[s0][:2], (e["start_time"], (sf, ef), rng[s0])
    for st in FRAME_SEGMENTS:
        sf, ef, _ = rng[float(sec(st))]
        nfr = qvu.smart_nframes({"nframes": 10}, total_frames=ef - sf + 1, video_fps=fps)
        idx = torch.linspace(sf, ef, nfr).round().long().tolist()
        c["vis_frames"][st] = {"range": (sf, ef), "idx": idx}
    factor = 14 * qvu.SPATIAL_MERGE_SIZE
    min_px = qvu.VIDEO_MIN_TOKEN_NUM * factor * factor
    max_px = min(max(min(qvu.VIDEO_MAX_TOKEN_NUM * factor * factor,
                         qvu.MODEL_SEQ_LEN * factor * factor * 0.9 / 10 * qvu.FRAME_FACTOR), int(min_px * 1.05)), 360 * 420)
    c["vis_resize"] = qvu.smart_resize(c["wh"][1], c["wh"][0], factor=factor, min_pixels=min_px, max_pixels=max_px)
    return c


# ---------------------------------------------------------------------------------------------- render
def render():
    c = load_ctx()
    made = build_assets(c)
    L = []
    w = L.append
    outline, n = c["outline"], len(c["outline"])
    c10, c30, c3m, c10m = (c["caps"][g] for g in GRANS)
    fps = c["fps"]
    repro = c["repro"]

    w(f"## 10. 발표용 심층 예시: `{VID}` (농구 가젯 시험) 보고서 r1의 모든 중간 산출물")
    w("")
    w("### 10.0 이 절의 범위와 읽는 법")
    w("")
    w(f"- **대상**: §6.1의 보고서와 같은 건(`{rel(os.path.join(RUN, JOB))}`). §2–§7이 세 영상을 비교했다면, 이 절은 한 영상에 대해 **사전 구축 메모리의 실제 내용, 모듈이 실제로 받은 프레임, 모듈별 입력·출력 원문**을 모두 펼친다.")
    w("- **만든 방법**: `analysis/build_running_example_deep.py`가 아래 원본에서 직접 생성했다(LLM 재호출 없음, CPU).")
    w(f"  - WorldMM 전처리 결과: `{os.path.relpath(WMF, os.path.dirname(RF))}/` 아래 caption·transcript·metadata, 전처리 로그 `logs/{VID}.log`")
    w("  - WorldMM 코드를 수정 없이 불러와 다시 계산: 10초 구간 분할·캡션 입력 프레임(`preprocess/episodic_memory/generate_fine_caption.py`), VLM2Vec 프레임 범위·리사이즈(`VLM2Vec/.../qwen_vl_utils.py`), 캡션 계층 묶음(`gen_multiscale._summarize_level`과 같은 규칙)")
    w("  - 재사용한 WorldMM 코드는 전처리 당시 코드와 같다고 본다. 전처리 로그의 경로는 이름 변경 전 `VAU_RAG/WorldMM`인데, 같은 디렉터리가 `VideoRAG`로 이름만 바뀌었다(`DESIGN_AND_STATUS.md` §10). 재사용한 파일들의 마지막 수정 시각은 모두 2026-09-20 이전으로, 메모리 생성(2026-09-21–22)보다 앞선다. [확인: 파일 수정 시각]")
    w("  - 보고서 실행 기록: `report.json`·`validation.json`·`report.md`, Deep-Reporter 세션 로그, LLM 서버·검색 서비스 로그")
    w(f"  - 검색 내부 과정: `{rel(c['repro_path'])}` (`analysis/reproduce_retrieval_cpu.py`가 검색 서비스의 클래스를 CPU에서 다시 돌린 결과, §10.9.0)")
    w(f"- **그림 파일**: `internal/running_example/{ASSET_REL}/` ({len(made)}개 묶음 이미지 + 검색 중앙 프레임 + `frames/` 낱장). PPT에는 이 파일을 그대로 쓰면 된다. 목록은 §10.10.")
    w("- **생성 중 자동 확인(assert)한 것**")
    w("  - WorldMM 분할 코드로 만든 10초 구간 226개의 시작·끝이 `10sec.json`과 모두 같다.")
    w("  - 캡션 계층(10sec→30sec→3min→10min) 묶음 규칙으로 다시 묶은 창의 수·시작·끝이 세 단계 모두 파일과 같다.")
    w("  - VLM2Vec 프레임 범위를 코드로 다시 계산한 값이 전처리 로그 226줄과 모두 같다.")
    w("  - 검색 때 저장된 중앙 프레임 17장을 영상에서 다시 읽은 프레임과 비교해 같은 장면이다(픽셀 평균 차 < 3, JPEG 손실 허용).")
    w("  - 검색 재현(§10.9.0)은 섹션·항목(text / semantic / image)마다 실행 기록과 맞춰 보고, 맞은 것만 내부 과정으로 싣는다.")
    w("- **표시**: [확인] 코드·데이터·로그로 확인 / [측정] 계산값 / [부분 확인] 일부만 확인 / [가설] 근거 부족. \"장면\"은 WorldMM 캡션 기준이며 영상을 사람이 보고 확인하지는 않았다(프레임 이미지는 실제 영상에서 뽑은 것).")
    w("")
    # ============================================================== 10.1
    w("### 10.1 원천 입력: 영상, 자막, 10초 구간")
    w("")
    w("| 항목 | 값 | 근거 |")
    w("|---|---|---|")
    w(f"| 영상 파일 | `{VIDEO}` ({os.path.getsize(VIDEO):,} bytes) | 파일 |")
    w(f"| 해상도·fps·프레임 | {c['wh'][0]}×{c['wh'][1]}, {fps:.6f} fps, {c['nfr']:,}프레임 → {c['dur']:.3f}초 ({G.hms(c['dur'])}) | decord, WorldMM `get_video_duration` |")
    w(f"| 자막 | Whisper → `transcript/{VID}.srt`, {len(c['transcript'])}줄. 모델은 `process_one_video.sh` 1단계의 `distil-large-v3.5` (이 스크립트는 2026-10-21에 수정됐고 로그에 모델명이 없어 당시 값인지는 [부분 확인]) | srt 파일, 스크립트 |")
    w(f"| 10초 구간 | {len(c['segments'])}개 = ⌈{c['dur']:.3f} / 10⌉, 마지막 구간 {c['segments'][-1].start_seconds:.0f}–{c['segments'][-1].end_seconds:.3f}초({G.hms(c['segments'][-1].start_seconds)}–영상 끝) | WorldMM `build_segments` |")
    w(f"| 구간 시각 표기 | 시작은 내림, 끝은 올림한 `HHMMSS00` (예: 마지막 구간 끝 {c['segments'][-1].end_seconds:.3f}초 → `{c10[-1]['end_time']}`) | `format_caption_time` |")
    w("")
    w(f"자막 앞 12줄 (원문 그대로):")
    w("")
    w("| # | 시작 | 끝 | 텍스트 |")
    w("|---|---|---|---|")
    for k, t in enumerate(c["transcript"][:12], 1):
        w(f"| {k} | {t.start_timestamp} | {t.end_timestamp} | {cell(t.text)} |")
    w("")
    cross = next(t for t in c["transcript"] if int(t.start_seconds // 10) != int((t.end_seconds - 1e-9) // 10))
    n_multi = sum(1 for t in c["transcript"] if int(t.start_seconds // 10) != int((t.end_seconds - 1e-9) // 10))
    w(f"- 구간마다 \"구간과 겹치는 자막 줄\"(`entry.end > 구간 시작 and entry.start < 구간 끝`)이 캡션 프롬프트에 들어간다. 10초 경계에 걸친 줄은 두 구간 모두에 들어간다: {len(c['transcript'])}줄 중 {n_multi}줄(첫 예: {cross.start_timestamp}–{cross.end_timestamp} \"{cross.text}\"). [확인]")
    w("")
    # ============================================================== 10.2
    gfc = c["gfc"]
    w("### 10.2 10sec 캡션 생성: 캡션 모델이 실제로 받은 프레임과 프롬프트")
    w("")
    w("- 모델: Qwen3-VL-8B-Instruct (`--model qwen3vl-8b`), 최대 출력 2,048토큰(`qwen3vl.py` 기본값). [확인]")
    w("- 프레임: 구간 안의 **매 정수 초마다 1장**(`compute_sample_seconds`), 프레임 번호 = round(초 × fps). 10초 구간이면 10장. 원본 1280×720 프레임을 PIL 이미지로 그대로 넘긴다(모델 안의 리사이즈는 `qwen_vl_utils`·processor 기본값이며 여기서는 측정하지 않음). [확인]")
    w("- 메시지: system(아래 프롬프트) + user[구간 시각, 겹치는 자막 줄, 그리고 프레임마다 `Frame timestamp: …` 문자열 + 이미지]. [확인]")
    w("")
    w(details("캡션 system 프롬프트 원문 (`generate_fine_caption.py` SYSTEM_PROMPT)", fence(gfc.SYSTEM_PROMPT)))
    w("")
    from PIL import Image as _Im
    for st in FRAME_SEGMENTS:
        cf = c["cap_frames"][st]
        seg = cf["seg"]
        msgs = gfc.build_segment_prompt(seg, [gfc.FrameSample(timestamp_seconds=s, image=_Im.new("RGB", (1, 1))) for s in cf["secs"]])
        parts = []
        for p in msgs[1]["content"]:
            parts.append(p["text"] if p["type"] == "text" else "<이미지: 1280×720 프레임>")
        e10 = c10[cf["k"]]
        fig = [f["k"] for f in c["grounded"]["figures"] if f["uid"].endswith(":" + st)]
        tag = f" — 보고서 Figure {fig[0]}의 구간" if fig else " — §3.2 예시 구간"
        w(f"**구간 {tt(st)}–{tt(e10['end_time'])}{tag}**")
        w("")
        w(md_img(f"caption_input_{st}.jpg", f"caption input frames {tt(st)}"))
        w("")
        w(f"- 입력 프레임 10장: 초 {', '.join(str(int(s)) for s in cf['secs'])} → 프레임 번호 {', '.join(map(str, cf['idx']))} (그림 파일 `{ASSET_REL}/caption_input_{st}.jpg`, 낱장 `{ASSET_REL}/frames/caption_{st}_*.jpg`)")
        w("")
        w(details("user 메시지 (텍스트 부분 원문, 이미지 자리는 표시만)", fence("\n".join(parts))))
        w("")
        w("- 출력(= `10sec.json`의 text):")
        w("")
        w(fence(e10["text"]))
        w("")
    # ============================================================== 10.3
    w("### 10.3 episodic memory ①: 캡션 4단위 계층의 실제 내용")
    w("")
    w("- 만드는 방법(`worldmm.memory.episodic.gen_multiscale`, perspective `general`) [확인]")
    w("  - 30sec ← 10sec, 3min ← 30sec, 10min ← 3min. 바로 아래 단위의 캡션을 시작 시각 순으로 창(30/180/600초)에 묶는다. 첫 창은 첫 캡션 시각에서, 다음 창은 `(시작 // 창) × 창`에서 시작한다.")
    w("  - 묶인 캡션 text를 줄바꿈으로 이어 `All descriptions: …` 한 덩어리로 LLM에 준다(**시각 표기 없음**). system 프롬프트는 단계별 L1/L2/L3이며, 출력 형식 문장의 단어 제한만 다르다(없음 / 300단어 / 1,500단어).")
    w("  - 결과의 start/end는 창의 시작·끝(창 크기 그대로)이다. 그래서 마지막 창의 끝은 영상 끝보다 뒤일 수 있다.")
    lv = [("10sec", "30sec", 30), ("30sec", "3min", 180), ("3min", "10min", 600)]
    for lo, hi, size in lv:
        ws = windows(c["caps"][lo], size)
        assert len(ws) == len(c["caps"][hi]), (lo, hi)
        for (s0, items), e in zip(ws, c["caps"][hi]):
            assert s0 == sec(e["start_time"]) and s0 + size == sec(e["end_time"]), (hi, e["start_time"])
    w(f"- 다시 묶어 본 결과: 10sec {len(c10)} → 30sec {len(c30)} → 3min {len(c3m)} → 10min {len(c10m)}. 창 개수·시작·끝이 파일과 모두 같다. [확인]")
    w("")
    w("| 단위 | 항목 수 | 단어 수 평균 / 최소 / 최대 | 한 항목이 덮는 아래 단위 개수 |")
    w("|---|---|---|---|")
    for g, (lo, size) in zip(GRANS, [(None, None), ("10sec", 30), ("30sec", 180), ("3min", 600)]):
        ws_ = [len(str(e["text"]).split()) for e in c["caps"][g]]
        cov = "—" if lo is None else ", ".join(f"{k}개×{v}" for k, v in sorted(collections.Counter(len(it) for _, it in windows(c["caps"][lo], size)).items()))
        w(f"| {g} | {len(c['caps'][g])} | {sum(ws_) / len(ws_):.0f} / {min(ws_)} / {max(ws_)} | {cov} |")
    w("")
    w(f"#### 10.3.1 00:00:00–{G.hms(HIER_END)} 전체 계층 (원문 그대로)")
    w("")
    e3 = c3m[0]
    w(f"**3min {tt(e3['start_time'])}–{tt(e3['end_time'])}** ({len(e3['text'].split())}단어)")
    w("")
    w(fence(e3["text"]))
    w("")
    for s0, kids in windows(c10, 30):
        if s0 >= HIER_END:
            break
        e30 = next(e for e in c30 if sec(e["start_time"]) == s0)
        w(f"**30sec {tt(e30['start_time'])}–{tt(e30['end_time'])}** ({len(e30['text'].split())}단어)")
        w("")
        w(fence(e30["text"]))
        w("")
        w("| 10sec | 텍스트 |")
        w("|---|---|")
        for e in kids:
            w(f"| {tt(e['start_time'])}–{tt(e['end_time'])} | {cell(e['text'])} |")
        w("")
    w("#### 10.3.2 10min 캡션 4개 전문 (planner가 보는 영상 개요)")
    w("")
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3-VL-8B-Instruct")
    for (s0, items), e in zip(windows(c3m, 600), c10m):
        ntok = len(tok(e["text"]).input_ids)
        w(details(f"10min 라벨 {tt(e['start_time'])}–{tt(e['end_time'])} · 묶인 3min {len(items)}개(시작 {', '.join(tt(i['start_time'])[3:] for i in items)}) · {len(e['text'].split())}단어 · {ntok:,}토큰" + (" · 2,048토큰 상한 도달" if ntok >= 2048 else ""), fence(e["text"])))
        w("")
    w("#### 10.3.3 전체 목록")
    w("")
    for g in ("3min", "30sec", "10sec"):
        rows = ["| 구간 | 단어 | 텍스트 |", "|---|---|---|"] + [f"| {tt(e['start_time'])}–{tt(e['end_time'])} | {len(e['text'].split())} | {cell(e['text'])} |" for e in c["caps"][g]]
        w(details(f"{g} 캡션 {len(c['caps'][g])}개 전문", "\n".join(rows)))
        w("")
    # ============================================================== 10.4
    oi = c["openie"]
    ner, tri = oi["ner_results"], oi["triple_results"]
    w("### 10.4 episodic memory ②: OpenIE triple과 HippoRAG 그래프")
    w("")
    w("- **10sec OpenIE**(WorldMM 전처리, `build_memory.py --step episodic`): 10sec 캡션마다 LLM 2회 — NER(개체 목록) → NER을 조건으로 triple 추출. 각 호출은 최대 3회 재시도(`dynamic_retry_decorator`), 끝내 실패하면 빈 목록을 저장한다(`openie.py`). [확인]")
    w("- **다른 단위(30sec·3min·10min)**: 보고서 프레임워크의 사전 인덱싱(`prebuild_episodic_index.py`)이 같은 프롬프트로 OpenIE를 돌렸다. 10sec은 위 전처리 결과를 그대로 옮겨 썼다(seeding). [확인]")
    w("")
    from worldmm.llm.templates import ner as T_ner, triple_extraction as T_tri
    w(details("NER 프롬프트 (system + one-shot 예시 + 캡션)", fence(json.dumps(T_ner.prompt_template, ensure_ascii=False, indent=1))))
    w("")
    w(details("triple 추출 프롬프트 (system + one-shot 예시 + 캡션·NER 결과)", fence(json.dumps([{"role": m["role"], "content": m["content"] if isinstance(m["content"], str) else str(m["content"])} for m in T_tri.prompt_template], ensure_ascii=False, indent=1))))
    w("")
    n_ent = sum(len(v) for v in ner.values())
    n_tri = sum(len(v) for v in tri.values())
    assert len(ner) == len(tri) == len(c10)
    empty = [e for e in c10 if not tri.get(md5(e["text"]))]
    log_ep = c["pre_log"]
    fail_chunks = sorted({m.group(1) for ln in log_ep for m in [re.search(r"Exception for chunk (chunk-[0-9a-f]+): RetryError", ln)] if m})
    fail_set = set(fail_chunks)
    w(f"- 결과(`openie_results_qwen3vl-8b.json`): 캡션 {len(c10)}개, 개체 {n_ent:,}개, triple {n_tri:,}개(전처리 로그의 `Total unique entities extracted: {n_ent}`, `Total triples extracted: {n_tri}`와 같음). [확인]")
    assert f"Total unique entities extracted: {n_ent}" in "\n".join(log_ep) and f"Total triples extracted: {n_tri}" in "\n".join(log_ep)
    n_empty_ner = sum(1 for e in empty if not ner.get(md5(e["text"])))
    w(f"- **triple이 0개인 캡션 {len(empty)}개** [확인]")
    i_ep0 = next(i for i, ln in enumerate(log_ep) if "Loaded" in ln and "caption entries from" in ln)
    i_ep1 = next(i for i, ln in enumerate(log_ep) if "Total episodic triples" in ln)
    vtypes = collections.Counter(m.group(1) for ln in log_ep[i_ep0:i_ep1]
                                 for m in [re.search(r"Input should be a valid string \[type=string_type, input_value=.*, input_type=(\w+)\]", ln)] if m)
    w(f"  - {len(fail_set)}개: NER은 됐지만 triple 추출이 3회 모두 실패(로그 `Exception for chunk … RetryError`). 이 단계 로그의 triple 형식 오류는 모두 \"triple 원소가 문자열이 아님\" 유형이다(" + ", ".join(f"{k} {v}건" for k, v in vtypes.most_common()) + "; 재시도 중 성공한 호출 포함, 두 캡션과의 짝은 로그로 알 수 없음).")
    w(f"  - {n_empty_ner}개: NER 결과부터 빈 목록이다. 로그에 이 캡션들에 대한 오류가 없다 → 모델이 빈 목록을 낸 것으로 보이나 응답 원문이 기록되지 않아 이유는 확인할 수 없다. [부분 확인]")
    w("  - 결과: 이 캡션들은 10sec 그래프에서 개체와 연결되지 않은 passage 노드가 된다(dense 유사도로만 검색됨). 캡션 내용 자체는 정상이다.")
    w("")
    w("| 10sec | 단어 | NER 개수 | triple | 원인 |")
    w("|---|---|---|---|---|")
    for e in empty:
        h = md5(e["text"])
        why = "triple 추출 RetryError" if h in fail_set else "NER 빈 목록(오류 기록 없음)"
        w(f"| {tt(e['start_time'])} | {len(e['text'].split())} | {len(ner.get(h, []))} | 0 | {why} |")
    w("")
    et = c["etrip"]
    k0 = "1" + str(c10[4]["end_time"]).zfill(8)
    w(f"- `episodic_triple_results_qwen3vl-8b.json`: 같은 triple을 캡션 끝 시각 키(`date` 숫자 + `end_time`, 예: 00:00:40–00:00:50 → `{k0}`)로 다시 정리한 파일. {len(et['episodic_triples'])}개 키. semantic 추출의 입력이 아니라 기록용이다(semantic은 OpenIE 파일을 직접 읽음, §10.5). [확인]")
    assert et["episodic_triples"][k0] == tri[md5(c10[4]["text"])]
    w("")
    w(f"**10sec 캡션 00:00:00–{G.hms(OPENIE_ROWS_END)}의 NER·triple 원문**")
    w("")
    w("| 10sec | NER (개체) | triple |")
    w("|---|---|---|")
    for e in c10:
        if sec(e["start_time"]) >= OPENIE_ROWS_END:
            break
        h = md5(e["text"])
        w(f"| {tt(e['start_time'])} | {cell(', '.join(ner.get(h, [])) or '(없음)')} | {cell('; '.join('(' + ', '.join(map(str, t)) + ')' for t in tri.get(h, [])) or '(없음)')} |")
    w("")
    # HippoRAG graphs
    import pandas as pd
    base = os.path.join(EPI, VID, "episodic_memory")
    w("**HippoRAG 그래프 구성 규칙** (`hipporag/HippoRAG.py`, 기본 설정) [확인]")
    w("")
    w("- 노드: passage(캡션 1개 = 1노드, id `chunk-<md5>`) + entity(triple 주어·목적어, 소문자화 등 정규화 후, id `entity-<md5>`).")
    w("- 엣지: ① fact 엣지 = triple 하나마다 주어↔목적어(양방향, 가중치는 등장 횟수) ② passage↔entity 엣지(가중치 1) ③ synonym 엣지 = entity 임베딩 cosine ≥ 0.8인 쌍(가중치 = cosine, 영문·숫자 3자 이하 entity 제외).")
    w("- 임베딩: Qwen3-Embedding-4B, 2,560차원. 검색 설정: `linking_top_k` 5, `passage_node_weight` 0.05, PPR damping 0.5.")
    w("")
    w("| 단위 | passage | entity | 빈 문자열 entity | 빈 문자열이 든 triple(OpenIE) | fact(고유 triple) | fact 엣지 | synonym 엣지 | passage–entity 엣지 |")
    w("|---|---|---|---|---|---|---|---|---|")
    graphs = {}
    for g in GRANS:
        d_ = glob.glob(f"{base}/{g}/qwen3vl-8b_*")[0]
        Gr = pickle.load(open(f"{d_}/graph.pickle", "rb"))
        graphs[g] = (Gr, d_)
        names = Gr.vs["name"]
        kinds = collections.Counter()
        for e_, wt in zip(Gr.es, Gr.es["weight"]):
            a_, b_ = names[e_.source], names[e_.target]
            kinds["pe" if a_.startswith("chunk") or b_.startswith("chunk") else ("f" if float(wt).is_integer() and wt >= 1 else "s")] += 1
        ents = pd.read_parquet(glob.glob(f"{d_}/entity_embeddings/*.parquet")[0])
        cnt = lambda sub: len(pd.read_parquet(glob.glob(f"{d_}/{sub}/*.parquet")[0]))
        docs = json.load(open(glob.glob(f"{base}/{g}/openie_results_ner_*.json")[0]))["docs"]
        n_blank = sum(1 for x in docs for t in x["extracted_triples"] if "" in [str(y).strip() for y in t])
        w(f"| {g} | {cnt('chunk_embeddings'):,} | {len(ents):,} | {int((ents['content'] == '').sum())} | {n_blank} | {cnt('fact_embeddings'):,} | {kinds['f']:,} | {kinds['s']:,} | {kinds['pe']:,} |")
    w("- 엣지 수는 igraph 엣지 수 그대로다(fact·synonym 엣지는 같은 쌍이 두 방향으로 각각 들어 있음).")
    w("- \"빈 문자열 entity\": 주어나 목적어가 빈 문자열인 triple에서 생긴 노드다(HippoRAG는 빈 문자열도 entity로 만든다). [확인]")
    w("")
    Gr, d_ = graphs["10sec"]
    names = Gr.vs["name"]
    ent_df = pd.read_parquet(glob.glob(f"{d_}/entity_embeddings/*.parquet")[0])
    ch_df = pd.read_parquet(glob.glob(f"{d_}/chunk_embeddings/*.parquet")[0])
    id2txt = dict(zip(ent_df["hash_id"], ent_df["content"]))
    ch2txt = dict(zip(ch_df["hash_id"], ch_df["content"]))
    txt2cap = {e["text"]: e for e in c10}
    eid = "entity-" + hashlib.md5(ENTITY.encode()).hexdigest()
    assert eid in names, ENTITY
    v = names.index(eid)
    nb_p, nb_f, nb_s = [], [], []
    for e_ in Gr.es[Gr.incident(v)]:
        o = e_.target if e_.source == v else e_.source
        on = names[o]
        if on.startswith("chunk"):
            nb_p.append(txt2cap[ch2txt[on]])
        elif float(e_["weight"]).is_integer() and e_["weight"] >= 1:
            nb_f.append((id2txt[on], e_["weight"]))
        else:
            nb_s.append((id2txt[on], e_["weight"]))
    nb_p.sort(key=lambda e: sec(e["start_time"]))
    w(f"**예: 10sec 그래프에서 entity `{ENTITY}` 노드의 이웃** (graph.pickle 원본)")
    w("")
    up = sorted({e["start_time"] for e in nb_p})
    uf = sorted({x for x, _ in nb_f})
    us = sorted(set(nb_s), key=lambda z: (-z[1], z[0]))
    w(f"- passage 이웃 {len(up)}개(이 개체가 triple에 나온 10sec 캡션): " + ", ".join(tt(x) for x in up))
    w(f"- fact 이웃 {len(uf)}개: " + ", ".join(f"`{x}`" for x in uf))
    w(f"- synonym 이웃 {len(us)}개(cosine): " + (", ".join(f"`{x}`({wt:.3f})" for x, wt in us) or "없음"))
    w(f"- (igraph에는 같은 쌍의 엣지가 두 방향으로 각각 들어 있어, 이 노드에 붙은 엣지 수는 passage {len(nb_p)} / fact {len(nb_f)} / synonym {len(nb_s)}개다.)")
    w("- 검색 때 질의와 비슷한 fact가 이 개체를 가리키면, PPR이 이 엣지들을 따라 위 passage들(과 synonym으로 이어진 개체의 passage)에 점수를 준다.")
    w("")
    syn_all = []
    for e_, wt in zip(Gr.es, Gr.es["weight"]):
        a_, b_ = names[e_.source], names[e_.target]
        if not (a_.startswith("chunk") or b_.startswith("chunk")) and not (float(wt).is_integer() and wt >= 1):
            syn_all.append((wt, id2txt[a_], id2txt[b_]))
    syn_pairs = sorted({(round(wt, 6), *sorted((a_, b_))) for wt, a_, b_ in syn_all})
    lo_ = syn_pairs[:8]
    w(f"**synonym 엣지 예: 10sec 그래프에서 cosine이 가장 낮은(0.8에 가까운) 8쌍** (고유 쌍 {len(syn_pairs):,}개 = igraph synonym 엣지 {len(syn_all):,}개) — 같은 뜻이 아닌 개체도 이어지는 사례")
    w("")
    w("| cosine | entity A | entity B |")
    w("|---|---|---|")
    for wt, a_, b_ in lo_:
        w(f"| {wt:.3f} | `{cell(a_)}` | `{cell(b_)}` |")
    w("")
    # ============================================================== 10.5
    w("### 10.5 semantic memory: 추출 → 통합 → 검색에 쓰이는 153개")
    w("")
    from worldmm.llm.templates import semantic_extraction as T_se, semantic_consolidation as T_sc
    w("**① 추출** (`preprocess/semantic_memory/extract_semantic_triples.py`, `memory/semantic/semantic_extraction.py`) [확인]")
    w("")
    w("- 10sec 캡션을 순서대로 **10개씩 묶어**(23묶음), 묶음의 10sec OpenIE triple을 모두 이어 `\"<번호>. [주어, 술어, 목적어]\"` 목록으로 LLM에 준다. 묶음 키 = `date` 숫자 + 묶음 마지막 캡션의 `end_time`.")
    w("- LLM은 `semantic_triples`와 각 triple의 근거 번호 `episodic_evidence`를 JSON으로 낸다. **저장할 때 `episodic_evidence`는 버린다**(코드에서 주석 처리). 그래서 semantic triple에는 시간·근거 연결이 없다.")
    w("- 최대 출력 2,048토큰, 3회 재시도 후 실패하면 그 묶음은 빈 목록이 된다.")
    w("")
    w(details("semantic 추출 프롬프트 원문 (system + one-shot + 입력)", fence(json.dumps(T_se.prompt_template, ensure_ascii=False, indent=1))))
    w("")
    se = c["sem_ext"]
    keys = list(se.keys())
    assert len(keys) == math.ceil(len(c10) / 10)
    groups = []
    for gi, k in enumerate(keys):
        chunk = c10[gi * 10:(gi + 1) * 10]
        assert k == chunk[-1]["date"][-1] + str(chunk[-1]["end_time"]).zfill(8)
        n_in = sum(len(tri[md5(e["text"])]) for e in chunk)
        groups.append((k, chunk, n_in, len(se[k])))
    retry = [ln for ln in log_ep if "worldmm.memory.semantic.semantic_extraction:RetryError" in ln]
    n_fail = sum(1 for g_ in groups if g_[3] == 0)
    assert len(retry) == n_fail, (len(retry), n_fail)
    # failed raw responses logged by qwen3vl: token counts
    i0 = next(i for i, ln in enumerate(log_ep) if "semantic_memory.extract_semantic_triples:Grouping" in ln or "Created 23 caption groups" in ln)
    i1 = next(i for i, ln in enumerate(log_ep) if "Total semantic triples extracted" in ln)
    blob = "\n".join(log_ep[i0:i1])
    bodies = []
    for p in blob.split("Failed to parse response as JSON: ")[1:]:
        b = re.split(r"\n(?:WARNING|ERROR|INFO):|Extracting semantic triples:", p)[0]
        if b.lstrip().startswith(("{", "[", "`")):
            bodies.append(b)
    btok = [len(tok(b).input_ids) for b in bodies]
    n_cap = sum(1 for t in btok if t >= 2047)
    n_in_ev = sum(1 for b in bodies if '"episodic_evidence"' in b)
    w(f"- **결과: 23묶음 중 {n_fail}묶음이 0개**, 나머지 {len(groups) - n_fail}묶음에서 {sum(g_[3] for g_ in groups)}개. [확인]")
    w(f"  - 전처리 로그의 semantic 추출 RetryError가 {len(retry)}건으로 0개 묶음 수와 같다. 실패한 묶음만 0개가 되므로 0개 묶음 = 실패 묶음이다.")
    w(f"  - 로그에 남은 파싱 실패 응답 원문 {len(bodies)}건 중 {n_cap}건이 2,047–2,048토큰에서 끊긴 JSON이다(최대 출력 2,048토큰). {n_in_ev}건은 `episodic_evidence` 목록을 쓰다가 끊겼다. → 출력 상한에 걸려 JSON이 완성되지 못한 것이 주원인. [측정]")
    w(f"  - 영향: 실패 묶음의 10sec 캡션 {n_fail * 10}개(전체 {len(c10)}개 중) 구간은 semantic memory에 아무것도 남기지 못했다(아래 표의 구간). [확인]")
    w("")
    w("| 묶음 키 | 덮는 10sec 구간 | 입력 episodic triple | 출력 semantic triple | 상태 |")
    w("|---|---|---|---|---|")
    for k, chunk, n_in, n_out in groups:
        w(f"| `{k}` | {tt(chunk[0]['start_time'])}–{tt(chunk[-1]['end_time'])} | {n_in} | {n_out} | {'**실패(RetryError)**' if n_out == 0 else '성공'} |")
    w("")
    gi = keys.index(SEM_GROUP)
    k, chunk, n_in, n_out = groups[gi]
    trip_in = [t for e in chunk for t in tri[md5(e["text"])]]
    w(f"**예: 묶음 `{SEM_GROUP}` ({tt(chunk[0]['start_time'])}–{tt(chunk[-1]['end_time'])})의 입력 → 출력**")
    w("")
    w(details(f"입력: episodic triple {len(trip_in)}개 (LLM이 받은 형식 그대로)", fence("\n".join(f"{i}. {t}" for i, t in enumerate(trip_in)))))
    w("")
    w(details(f"출력: semantic triple {n_out}개", fence("\n".join(f"{i}. {t}" for i, t in enumerate(se[SEM_GROUP])))))
    w("")
    w("**② 통합** (`consolidate_semantic_memory.py`, `semantic_consolidation.py`) [확인]")
    w("")
    w("- 묶음 키 순서대로 누적한다. 새 triple마다 기존 누적 triple과 임베딩 cosine을 계산해 **0.6 이상인 것(최대 20개)** 이 있으면 LLM에 \"새 triple + 관련 기존 triple\"을 주고, ① 새 triple을 어떻게 고칠지 ② 기존 것 중 무엇을 지울지를 받는다. 관련 기존 triple이 없으면 그대로 추가한다.")
    w("- 각 시점의 누적 결과 전체를 저장한다(`semantic_consolidation_results_qwen3vl-8b.json`, 23개 키).")
    w("")
    w(details("semantic 통합 프롬프트 원문", fence(json.dumps(T_sc.prompt_template, ensure_ascii=False, indent=1))))
    w("")
    sc = c["sem_con"]
    assert list(sc.keys()) == keys
    w("| 시점 키 | 새 triple | 이전 누적 | 이후 누적 | 지워진 기존 triple |")
    w("|---|---|---|---|---|")
    prev = []
    diffs = {}
    for k in keys:
        cur = sc[k]["consolidated_semantic_triples"]
        new_n = len(se[k])
        removed = len(prev) + new_n - len(cur)
        assert removed >= 0
        kept = cur[:len(cur) - new_n]
        it = iter(map(tuple, prev))
        assert all(t in it for t in map(tuple, kept)), k        # kept = previous list minus removed, order preserved
        if new_n:
            rem = collections.Counter(map(tuple, prev)) - collections.Counter(map(tuple, kept))
            diffs[k] = {"removed": list(rem.elements()), "added": [list(t) for t in cur[len(cur) - new_n:]], "raw": se[k]}
        w(f"| `{k}` | {new_n} | {len(prev)} | {len(cur)} | {removed} |")
        prev = cur
    w("")
    ex_k = max(diffs, key=lambda k: len(diffs[k]["removed"]))
    dx = diffs[ex_k]
    changed = [(r, a) for r, a in zip(dx["raw"], dx["added"]) if list(r) != list(a)]
    w(f"**예: 시점 `{ex_k}`의 통합** (지워진 기존 triple이 가장 많은 시점: {len(dx['removed'])}개)")
    w("")
    w(f"- 이 시점 새 triple {len(dx['raw'])}개 중 LLM이 고친 것 {len(changed)}개. 앞 8개(추출 원문 → 통합 후):")
    for r, a in changed[:8]:
        w(f"  - `{tuple(r)}` → `{tuple(a)}`")
    w(f"- 지워진 기존 triple 앞 8개: " + "; ".join(f"`{t}`" for t in dx["removed"][:8]))
    w("- 지운 이유(LLM 응답)는 기록되지 않는다. 위 짝은 파일 비교로만 얻은 것이다. [확인]")
    w("")
    final_k = keys[-1]
    final = sc[final_k]["consolidated_semantic_triples"]
    qt = int(c["cfg"]["worldmm"]["query_time"])
    avail = sorted(int(k) for k in keys if sc[k]["consolidated_semantic_triples"])
    used = max(t for t in avail if t <= qt)
    assert str(used) == final_k
    ents = [x for t in final for x in (t[0], t[2]) if x]
    deg = collections.Counter(ents)
    edges = sum(1 for t in final if t[0] and t[2] and t[0] != t[2])
    w(f"**③ 검색에 쓰이는 semantic memory** — `query_time` {qt} 이하의 마지막 시점 `{final_k}`의 누적 {len(final)}개만 쓴다(`SemanticMemory.index`). 검색 서비스 로그 `semantic 153`과 같다. [확인]")
    w("")
    w(f"- 개체 그래프: 개체(주어·목적어, 빈 문자열 제외) {len(deg)}개, 엣지 {edges}개(주어≠목적어인 triple). 목적어가 빈 triple {sum(1 for t in final if not t[2])}개.")
    kq, ks = c["cfg"]["retrieval"]["semantic_k_per_query"], c["cfg"]["retrieval"]["semantic_k"]
    w(f"- 검색(`SemanticMemory.retrieve`, top_k = `semantic_k_per_query` {kq}): 질의 임베딩과 cosine 상위 {kq}개 triple → 그 triple들의 개체를 출발점으로 PPR(damping 0.85) → triple 점수 = 주어 PPR + 목적어 PPR → 상위 {kq}개. 질의 여러 개의 목록을 RRF(k=60)로 합쳐 `semantic_k` {ks}개를 writer에 준다.")
    w("- 연결이 많은 개체 상위 10: " + ", ".join(f"`{e}`({n_})" for e, n_ in deg.most_common(10)))
    w("")
    rows = ["| id | 주어 | 술어 | 목적어 |", "|---|---|---|---|"] + [f"| `semantic_{final_k}_{i}` | {cell(t[0])} | {cell(t[1])} | {cell(t[2]) if t[2] else '(빈 문자열)'} |" for i, t in enumerate(final)]
    w(details(f"최종 semantic triple {len(final)}개 전체", "\n".join(rows)))
    w("")
    # ============================================================== 10.6
    vis = c["vis"]
    v0 = next(iter(vis.values()))
    w("### 10.6 visual memory: 10sec 구간마다 VLM2Vec 비디오 임베딩 1개")
    w("")
    w(f"- 파일 `visual_embeddings.pkl`: dict, 키 = 10sec `start_time`({len(vis)}개), 값 = numpy {v0.dtype} 벡터 {v0.shape}. [확인]")
    nf = json.load(open(os.path.join(RF, "results", f"visual_nframes_check_{VID}.json")))["rows"]
    by = collections.defaultdict(dict)
    for r_ in nf:
        by[r_["segment"]][r_["nframes"]] = r_["cosine_to_stored"]
    assert all(v[10] > 0.99 and v[16] < v[10] for v in by.values())
    w(f"- 프레임 수 확인: 저장된 임베딩을 CPU에서 10장·16장(WorldMM 기본값)으로 다시 만들어 비교했다(`analysis/verify_visual_nframes.py`). cosine은 " + "; ".join(f"{tt(k)} 10장 {v[10]} / 16장 {v[16]}" for k, v in by.items()) + " → **10장**으로 만든 것이다. [확인]")
    w(f"- 입력 프레임: 구간마다 **10장**(`--num-frames 10`). 시작 프레임 = ⌈시작초 × fps⌉, 끝 프레임 = ⌊끝초 × fps⌋, 그 사이를 `linspace(시작, 끝, 10)` 반올림. 디코더는 전처리 당시 `{', '.join(c['vis_backend'])}`(로그). 프레임 범위는 로그 226줄과 코드 재계산이 모두 같다. [확인]")
    rh, rw_ = c["vis_resize"]
    w(f"- 크기: 프레임당 최대 360×420 = 151,200픽셀 제한으로 {c['wh'][0]}×{c['wh'][1]} → **{rw_}×{rh}**(28의 배수, `smart_resize`). 텍스트 지시문 `Represent the given video.`와 함께 임베딩. [확인]")
    w("- 캡션용 프레임(§10.2, 매 정수 초)과 visual 임베딩용 프레임(균등 10장)은 **서로 다른 프레임**이다. 아래 그림의 프레임 번호를 비교하면 보인다.")
    w("")
    for st in FRAME_SEGMENTS:
        vf = c["vis_frames"][st]
        fig = [f["k"] for f in c["grounded"]["figures"] if f["uid"].endswith(":" + st)]
        w(f"**구간 {tt(st)} — VLM2Vec 입력 10장** (프레임 {vf['range'][0]}–{vf['range'][1]} → {', '.join(map(str, vf['idx']))})" + (f" · 보고서 Figure {fig[0]}" if fig else ""))
        w("")
        w(md_img(f"vlm2vec_input_{st}.jpg", f"vlm2vec input frames {tt(st)}"))
        w("")
    w("- 검색 때: image query를 VLM2Vec 텍스트 인코더로 임베딩 → 226개 구간 임베딩과 cosine → 상위 3구간 → 구간 **중앙 시각**의 프레임 1장을 잘라 writer에 캡션과 함께 넘긴다(§10.7).")
    w("")
    # ============================================================== 10.7
    w("### 10.7 보고서 생성 중 검색된 프레임 (섹션별 image 근거 3장)")
    w("")
    w("| 섹션 | 순위 | 구간 | 중앙 프레임 | cosine(CPU 재현) | 인용 | 프레임 |")
    w("|---|---|---|---|---|---|---|")
    for i, (s, rs) in enumerate(zip(outline, repro["sections"]), 1):
        ci = set(cited_img(s["content"] or ""))
        cos = {x["start_time"]: x["cosine"] for x in rs["visual"][0]["top10"]} if len(rs["visual"]) == 1 and rs["visual_match"] else {}
        for k, m in enumerate(s["retrieved_images"], 1):
            fig = c["uid2fig"].get(m["uid"]) if k in ci else None
            w(f"| S{i} | {k} | {tt(m['start_time'])}–{tt(m['end_time'])} | {G.hms(m['frame_sec'])} | {cos.get(m['start_time'], '—')} | {('Figure ' + str(fig)) if fig else ('✓' if k in ci else '')} | {md_img('center_' + m['start_time'] + '.jpg', 'center ' + m['start_time'])} |")
    w("")
    allimg = [m["start_time"] for s in outline for m in s["retrieved_images"]]
    dup = [k for k, v in collections.Counter(allimg).items() if v > 1]
    w(f"- 표의 프레임은 실행 때 검색 서비스가 저장한 파일(`{rel(os.path.dirname(outline[0]['retrieved_images'][0]['img_path']))}/`)을 복사한 것이다. 검색 {len(allimg)}회 중 같은 구간이 다시 나온 것({', '.join(tt(x) for x in dup) or '없음'})이 있어 파일은 {len(set(allimg))}장이다.")
    w("")
    w("**최종 보고서의 그림 (report.md 그대로)**")
    w("")
    for f in c["grounded"]["figures"]:
        st = f["uid"].split(":visual:")[1]
        cap = next(b for b in re.split(r"\n\n", c["grounded"]["markdown"]) if b.startswith(f"*Figure {f['k']}."))
        w(f"- Figure {f['k']}: 구간 {tt(st)}, 프레임 {G.hms(f['frame_sec'])} — 파일 `{ASSET_REL}/center_{st}.jpg`")
        w("")
        w(md_img(f"center_{st}.jpg", f"Figure {f['k']}"))
        w("")
        w(f"> {cap}")
        w("")
    # ============================================================== 10.8 planner
    w("### 10.8 planner: 입력 프롬프트와 출력 원문")
    w("")
    pc = c["planner_call"]
    pl = c["llm"][0]
    w(f"- LLM 서버 로그: 프롬프트 {pl.group(2)}토큰, 출력 {pl.group(3)}토큰, `{pl.group(4)}`, {pl.group(5)}초. 메시지는 user 1개. [확인]")
    w("")
    w(details(f"planner 프롬프트 원문 ({len(pc['input_messages'][0]['content']):,}자)", fence(pc["input_messages"][0]["content"])))
    w("")
    w(details("planner 출력 원문", fence(pc["output_content"])))
    w("")
    # ============================================================== 10.9 sections
    w("### 10.9 섹션별 모듈 입력·출력 전부")
    w("")
    st_ = repro["settings"]
    w("#### 10.9.0 검색 재현 방법과 일치 확인")
    w("")
    w("- 실행 기록에는 질의 × 단위별 그래프 검색 결과, RRF 후보 목록, L1 필터 프롬프트가 없다. 그래서 `analysis/reproduce_retrieval_cpu.py`가 **검색 서비스의 `WorldMMRetriever` 클래스 그대로**, HippoRAG 캐시의 **복사본**으로, 임베딩 모델만 CPU(sdpa)에서 돌렸다. LLM은 호출하지 않는다(L1 필터 응답은 재현할 수 없음).")
    w(f"- 실행 당시에는 GPU(flash_attention_2)였다. 그래서 섹션마다 아래를 실행 기록과 맞춰 보고, **맞은 항목만 그 섹션의 내부 과정으로 싣는다.** 맞지 않은 항목은 \"재현 불가\"로 표시하고, 기록에 남은 사실(선택된 근거·점수)과 어긋난 지점만 보인다. [확인]")
    w("  - text: RRF 후보 수 = 검색 서비스 로그 `episodic_candidates` · 기록된 episodic 근거 8개가 재현 후보에 있고 RRF 점수(소수 6자리)가 같음 · 다시 만든 L1 필터 프롬프트의 토큰 수(서버와 같은 계산법) = LLM 서버 로그")
    w("  - semantic: 근거 4개의 id·순서·점수가 같음")
    w("  - image: 근거 3개의 구간·순서가 같음")
    w(f"  - 실제 캐시는 실행 전후 md5가 같다(`{repro['real_cache_md5_unchanged']}`).")
    w(f"- 설정: 질의당 후보 {json.dumps(st_['episodic_candidates_per_query'])}, RRF k={st_['rrf_k']}, HippoRAG `linking_top_k` {st_['linking_top_k']}, semantic 질의당 {st_['semantic_k_per_query']}개, visual 질의당 {st_['visual_k_per_query']}개. 텍스트 임베딩 `{st_['embedding']}`.")
    w("- HippoRAG 점수는 PPR 점수(그래프 경로) 또는 dense 유사도(fact가 없을 때)라 단위끼리 비교할 수 없다. 그래서 서비스는 점수 대신 순위로 RRF를 한다.")
    w("- **일치 판정의 한계**: 실행 기록에서 직접 맞춰 볼 수 있는 것은 위 값들뿐이다. text가 \"일치\"인 섹션의 고르지 않은 후보는 \"후보 수 + L1 프롬프트 토큰 수(후보 텍스트 전체가 들어감)\"가 같다는 것으로만 확인된다. 텍스트가 다른데 토큰 수만 우연히 같을 가능성까지 배제하지는 못한다. 또 RRF 점수가 같은 후보끼리의 순서(표의 순위, 재구성한 L1 프롬프트 안의 후보 순서)는 기록과 대조할 수 없다. [부분 확인]")
    w("")
    w("| 섹션 | RRF 후보 수 (재현 / 기록) | episodic 점수 불일치 | L1 프롬프트 토큰 (재현 / 기록) | semantic | image | 이 문서에 싣는 재현 결과 |")
    w("|---|---|---|---|---|---|---|")
    for i, rs in enumerate(repro["sections"], 1):
        ck = rs["checks"]
        show = [x for x, ok in (("text", rs["text_match"]), ("semantic", rs["semantic_match"]), ("image", rs["visual_match"])) if ok]
        w(f"| S{i} | {ck['candidates']['reproduced']} / {ck['candidates']['recorded']} | {len(ck['episodic_rrf']['mismatches'])}개 | {ck['l1_prompt_tokens']['reproduced']} / {ck['l1_prompt_tokens']['recorded']} | {'일치' if rs['semantic_match'] else '**불일치**'} | {'일치' if rs['visual_match'] else '**불일치**'} | {', '.join(show) or '없음'} |")
    w("")
    secs_ = repro["sections"]
    fmt = lambda f: ", ".join(f"S{x['index']}" for x in secs_ if f(x)) or "없음"
    w(f"- 맞은 섹션: text {fmt(lambda x: x['text_match'])} / semantic {fmt(lambda x: x['semantic_match'])} / image {fmt(lambda x: x['visual_match'])}.")
    w(f"- text가 어긋난 섹션: 기록된 근거의 RRF 점수가 다른 섹션({fmt(lambda x: not x['checks']['episodic_rrf']['ok'])})은 그 근거가 목록 하나에 더 들어가거나 빠지거나 순위가 한 칸 바뀐 값이다(각 섹션 ③의 근거). 점수는 모두 같은데 L1 프롬프트 토큰 수만 다른 섹션({fmt(lambda x: x['checks']['episodic_rrf']['ok'] and not x['checks']['l1_prompt_tokens']['ok'])})은 L1이 고르지 않은 후보 일부가 다르다. 모두 목록 **끝자리 근처의 순위 차이**다. [확인]")
    w("- 원인: 섹션 1·2를 CPU에서 float32와 bfloat16으로 따로 돌려 본 진단에서 text 후보는 두 정밀도가 서로 같았고, 둘 다 기록과 같은 지점에서 달랐다. 그래서 CPU와 GPU(flash_attention_2) 사이 질의 임베딩의 미세한 차이로 보인다. GPU로 다시 돌려 확인하지는 않았다. [부분 확인]")
    w("- 재현의 실행 간 차이: 이 표는 2026-11-02 CPU 재현 결과다. 2026-11-10에 같은 코드·같은 데이터(캐시 md5 동일)로 다시 돌린 두 번의 결과는 서로도, 이 표와도 달랐다(예: S1 text — 11-02 불일치, 11-10 한 번은 일치·한 번은 불일치). CPU 재현 자체가 실행마다 점수가 조금씩 달라(그래프 검색 점수 최대 차이 약 0.008) 점수가 비슷한 후보의 순위가 바뀐다. 그래서 \"맞은 섹션\" 목록은 고정된 값이 아니다. [확인: 대조 실험, `internal/status/REORG_LOG_20261110.md` 9절] 실행마다 달라지는 구체적 기제는 확인하지 않았다. [가설]")
    w("")
    for i, (s, rs) in enumerate(zip(outline, repro["sections"]), 1):
        content = s["content"] or ""
        title = next((ln.lstrip("#").strip() for ln in content.split("\n") if ln.startswith("#")), "")
        q, f_, wl = c["llm"][1 + 3 * (i - 1)], c["llm"][2 + 3 * (i - 1)], c["llm"][3 + 3 * (i - 1)]
        qc, wc, scall = c["q_calls"][i - 1], c["w_calls"][i - 1], c["search_calls"][i - 1]
        texts, imgs = s["retrieved_texts"], s["retrieved_images"]
        w(f"#### 10.9.{i} 섹션 {i}: {title}")
        w("")
        w(f"- planner 설명: {s['section_description']}")
        w(f"- checklist: " + " / ".join(s["sectional_checklist"]))
        w("")
        w(f"**① query 생성** — 프롬프트 {q.group(2)}토큰, 출력 {q.group(3)}토큰, `{q.group(4)}`, {q.group(5)}초")
        w("")
        w(details(f"query 프롬프트 원문 ({len(qc['input_messages'][0]['content']):,}자)", fence(qc["input_messages"][0]["content"])))
        w("")
        w("- 출력 원문:")
        w("")
        w(fence(qc["output_content"]))
        w("")
        assert scall["text_queries"] == s["text_queries"] and scall["image_queries"] == s["image_queries"] == rs["image_queries"]
        w(f"**② 검색 요청** (Deep-Reporter → 검색 서비스): text `{{\"query_list\": {json.dumps(s['text_queries'], ensure_ascii=False)}, \"type\": \"text\", \"topk\": {c['cfg']['report']['text_topk']}}}`, image `{{\"query_list\": {json.dumps(s['image_queries'], ensure_ascii=False)}, \"type\": \"image\", \"topk\": {c['cfg']['report']['image_topk']}}}`")
        w("")
        w(f"- 서비스 로그: text `{c['svc'][2 * (i - 1)].group(3)}` / image `{c['svc'][2 * (i - 1) + 1].group(3)}`")
        w("")
        qn = {qq: j for j, qq in enumerate(s["text_queries"], 1)}
        rec_epi = [t for t in texts if t["source"] == "worldmm-episodic"]
        ck = rs["checks"]
        if rs["text_match"]:
            w("**③ 그래프 검색 (질의 × 단위)** — 각 HippoRAG 그래프에서 상위 k개, 괄호는 k 밖 2개(경계 확인용) [CPU 재현, 기록과 일치]")
            w("")
            w("| 질의 | 단위 | k | 경로 | 결과 (id · 구간 · HippoRAG 점수) |")
            w("|---|---|---|---|---|")
            for gs in rs["graph_search"]:
                res = "<br>".join((f"`{r['id']}` {tt(r['start_time'])}–{tt(r['end_time'])} · {r['score']:.4f}" if r["within_k"] else f"({r['id']} · {r['score']:.4f})") for r in gs["results"])
                w(f"| q{qn[gs['query']]} | {gs['granularity']} | {gs['k']} | {gs['path']} | {res} |")
            w("")
            fact_rows = []
            for gs in rs["graph_search"]:
                for f, sc_ in gs["top_facts"]:
                    fact_rows.append(f"| q{qn[gs['query']]} | {gs['granularity']} | {cell(str(tuple(f)))} | {sc_:.4f} |")
            w(details("질의와 가장 비슷한 fact 상위 5개 (질의·단위별, 그래프 검색의 출발점)", "\n".join(["| 질의 | 단위 | fact | 유사도 |", "|---|---|---|---|"] + fact_rows)))
            w("")
            sel = {cid: r for r, cid in enumerate(rs["selected_by_l1"], 1)}
            lists = [(qn[gs["query"]], gs["granularity"]) for gs in rs["graph_search"]]
            w(f"**④ RRF 병합 → L1 필터** — 후보 {len(rs['rrf'])}개(로그와 같음) 중 L1 필터 LLM이 8개를 골라 순서를 정함")
            w("")
            w("| RRF 순위 | id | 구간 | RRF 점수 | 나온 목록 (질의·단위) | L1 선택 순위 | 텍스트 앞 120자 |")
            w("|---|---|---|---|---|---|---|")
            for r, x in enumerate(rs["rrf"], 1):
                src = ", ".join(f"q{a}·{b}" for a, b in (lists[j] for j in x["lists"]))
                w(f"| {r} | `{x['id']}` | {tt(x['start_time'])}–{tt(x['end_time'])} | {x['rrf']:.6f} | {src} | {('**' + str(sel[x['id']]) + '**') if x['id'] in sel else ''} | {cell(cut(x['text'], 120))} |")
            w("")
            lg = rs["l1_log"]
            w(f"- L1 필터 호출: 프롬프트 {lg['prompt']}토큰(재구성 프롬프트 {rs['l1_prompt_tokens']}토큰과 같음), 출력 {lg['completion']}토큰, `{lg['finish']}`, {lg['sec']}초. 응답 원문은 기록되지 않는다. 선택 순서(`report.json`) = " + " → ".join(f"`{x}`" for x in rs["selected_by_l1"]))
            w("")
            w(details("L1 필터 프롬프트 원문 (재구성, 토큰 수 일치 확인)", fence(json.dumps(rs["l1_prompt"], ensure_ascii=False, indent=1))))
            w("")
        else:
            w(f"**③·④ 그래프 검색·RRF·L1 필터 — 재현 불가** (후보 수 재현 {ck['candidates']['reproduced']} / 기록 {ck['candidates']['recorded']}, L1 프롬프트 토큰 재현 {ck['l1_prompt_tokens']['reproduced']} / 기록 {ck['l1_prompt_tokens']['recorded']})")
            w("")
            if ck["episodic_rrf"]["mismatches"]:
                w("- 기록과 RRF 점수가 다른 근거 (점수 1/61 = 0.016393은 한 목록 1위, 1/62 = 0.016129는 2위, 1/63 = 0.015873은 3위에 해당):")
                for m in ck["episodic_rrf"]["mismatches"]:
                    apps = [f"q{qn[gs['query']]}·{gs['granularity']} {r + 1}위({x['score']:.4f}{', k 밖' if not x['within_k'] else ''})"
                            for gs in rs["graph_search"] for r, x in enumerate(gs["results"]) if x["id"] == m["id"]]
                    w(f"  - `{m['id']}`: 기록 {m['recorded_rrf']} / 재현 {m['reproduced_rrf']} — 재현에서 나온 자리: " + ("; ".join(apps) or "상위 k+2 안에 없음"))
                w("- 위 근거가 나온 목록의 경계 점수 (재현, k위와 k+1위):")
                ids = {m["id"] for m in ck["episodic_rrf"]["mismatches"]}
                for gs in rs["graph_search"]:
                    if any(x["id"] in ids for x in gs["results"]):
                        kk = gs["k"]
                        rr_ = gs["results"]
                        if len(rr_) > kk:
                            w(f"  - q{qn[gs['query']]}·{gs['granularity']}: {kk}위 `{rr_[kk - 1]['id']}` {rr_[kk - 1]['score']:.5f} / {kk + 1}위 `{rr_[kk]['id']}` {rr_[kk]['score']:.5f} (차이 {rr_[kk - 1]['score'] - rr_[kk]['score']:.5f})")
            else:
                d_ = ck["l1_prompt_tokens"]["reproduced"] - ck["l1_prompt_tokens"]["recorded"]
                w(f"- 후보 수와 L1이 고른 8개의 RRF 점수는 기록과 모두 같다. L1 프롬프트 토큰 수만 {abs(d_)}개 다르다(재현이 {'많음' if d_ > 0 else '적음'}). 그러니 L1이 고르지 않은 후보 가운데 일부가 다르다. 어느 것인지는 기록으로 알 수 없다.")
            w("")
            w("- **기록에 남은 사실** (`report.json`): L1 필터가 고른 episodic 8개와 실행 당시 RRF 점수, LLM 서버 로그의 L1 호출")
            w("")
            w("| L1 선택 순위 | id | 단위 | 구간 | RRF 점수(실행 당시) |")
            w("|---|---|---|---|---|")
            for r, t in enumerate(rec_epi, 1):
                w(f"| {r} | `{t['uid'].split(':episodic:')[1]}` | {t['granularity']} | {tt(t['start_time'])}–{tt(t['end_time'])} | {t['score']} |")
            lg = rs["l1_log"]
            w(f"- L1 필터 호출: 프롬프트 {lg['prompt']}토큰, 출력 {lg['completion']}토큰, `{lg['finish']}`, {lg['sec']}초.")
            w("")
        rec_sem = [t for t in texts if t["source"] == "worldmm-semantic"]
        if rs["semantic_match"]:
            w(f"**⑤ semantic 검색** — 질의마다 PPR 상위 {st_['semantic_k_per_query']}개 → RRF {len(rs['semantic_rrf'])}개 [CPU 재현, 기록과 일치]")
            w("")
            w("| 질의 | 결과 |")
            w("|---|---|")
            for sq in rs["semantic_per_query"]:
                w(f"| q{qn[sq['query']]} | " + "<br>".join(f"`{x['id']}` ({cell(', '.join(x['triple']))})" for x in sq["results"]) + " |")
            w(f"| **RRF** | " + "<br>".join(f"`{x['id']}` ({cell(', '.join(x['triple']))}) · {x['rrf']:.6f}" for x in rs["semantic_rrf"]) + " |")
            w("")
        else:
            same_ids = ck["semantic"]["reproduced"] == ck["semantic"]["recorded"]
            w(f"**⑤ semantic 검색 — 재현 불가** (" + ("id·순서는 같으나 RRF 점수가 다름 → 질의별 목록이 다름" if same_ids else f"재현 {ck['semantic']['reproduced']} / 기록 {ck['semantic']['recorded']}") + "). 기록된 결과(`report.json`):")
            w("")
            for t in rec_sem:
                w(f"- `{t['uid'].split(':semantic:')[1]}` {t['text']} · RRF {t['score']}")
            w("")
        if rs["visual_match"]:
            w("**⑥ image 검색** — VLM2Vec cosine 상위 10 (상위 3개가 근거) [CPU 재현, 상위 3개 순서 기록과 일치]")
            w("")
            for vq in rs["visual"]:
                w(f"- 질의: `{vq['query']}`")
                w("")
                w("| 순위 | 구간 | cosine |")
                w("|---|---|---|")
                for r, x in enumerate(vq["top10"], 1):
                    w(f"| {r} | {tt(x['start_time'])}–{tt(x['end_time'])} | {x['cosine']} |")
                w("")
        else:
            w(f"**⑥ image 검색 — 재현 불가** (재현 {ck['visual']['reproduced']} / 기록 {ck['visual']['recorded']}). 기록된 근거는 §10.7 표.")
            w("")
        w("**⑦ writer가 받은 근거 전문** (txt 번호 = writer 프롬프트의 번호)")
        w("")
        ct, ci = set(cited_txt(content)), set(cited_img(content))
        rows = []
        for k, t in enumerate(texts, 1):
            ref = c["uid2ref"].get(t["uid"]) if k in ct else None
            rows.append(f"| txt{k} | {t['source'].replace('worldmm-', '')} | {t.get('granularity') or '—'} | {t['score']} | {('[' + str(ref) + ']') if ref else ''} | {cell(t['content'])} |")
        for k, m in enumerate(imgs, 1):
            fig = c["uid2fig"].get(m["uid"]) if k in ci else None
            rows.append(f"| img{k} | visual | 10sec | {m['score']} | {('Figure ' + str(fig)) if fig else ('✓' if k in ci else '')} | {cell(m['caption'])} |")
        w(details(f"근거 {len(texts)} + {len(imgs)}개 전문 (인용된 것은 전역 번호 표시)", "\n".join(["| 근거 | 출처 | 단위 | 점수(RRF) | 보고서 번호 | 내용 (writer에 들어간 문자열) |", "|---|---|---|---|---|---|"] + rows)))
        w("")
        w(f"**⑧ writer** — 프롬프트 {wl.group(2)}토큰, 출력 {wl.group(3)}토큰, `{wl.group(4)}`, {wl.group(5)}초")
        w("")
        w(details(f"writer 프롬프트 원문 ({len(wc['input_messages'][0]['content']):,}자)", fence(wc["input_messages"][0]["content"])))
        w("")
        w(details(f"writer 출력 원문 ({len(wc['output_content'].split())}단어)", fence(wc["output_content"])))
        w("")
        new, stt = G.dedupe_repeated_sentences(wc["output_content"])
        assert new == content
        vs = next(x for x in c["vj"]["sections"] if x["index"] == i)
        w("**⑨ 후처리** — 반복 문장 제거 → 인용 변환 → 그림 삽입")
        w("")
        w(f"- 반복 문장 제거: {stt['removed_sentences']}개(이 섹션은 writer 출력 = `report.json` 본문).")
        mp = [f"txt{k} → [{c['uid2ref'][texts[k - 1]['uid']]}]" for k in sorted(ct) if 1 <= k <= len(texts)]
        mi = [f"img{k} → Figure {c['uid2fig'][imgs[k - 1]['uid']]}" for k in sorted(ci) if 1 <= k <= len(imgs) and imgs[k - 1]["uid"] in c["uid2fig"]]
        w(f"- 인용 번호 대응: " + (", ".join(mp + mi) or "없음") + f". 인용 안 된 텍스트 근거 {vs['unused_text_evidence']}/{len(texts)}개.")
        w(f"- 인용 통계: `{json.dumps(vs['citations'])}`, 규칙 검사: `{json.dumps(vs['grounding_stats'])}`")
        w("")
        w(details("최종 본문 (report.md의 이 섹션 그대로)", fence(c["grounded"]["section_bodies"][i - 1])))
        w("")
    # ============================================================== 10.10 assets
    w("### 10.10 그림 파일 목록 (PPT용)")
    w("")
    w(f"위치: `report_framework/internal/running_example/{ASSET_REL}/`")
    w("")
    w("| 파일 | 내용 |")
    w("|---|---|")
    for st in FRAME_SEGMENTS:
        w(f"| `caption_input_{st}.jpg` | 10sec 캡션 {tt(st)} 생성 때 캡션 모델 입력 10장(매 정수 초) |")
        w(f"| `vlm2vec_input_{st}.jpg` | 같은 구간의 visual 임베딩 입력 10장(균등) |")
    w("| `center_<start_time>.jpg` | 보고서 생성 중 검색된 구간의 중앙 프레임(실행 때 저장 파일 복사, 17장) |")
    w("| `frames/caption_<start>_<NN>_f<프레임번호>.jpg`, `frames/vlm2vec_…` | 위 묶음 이미지의 낱장 원본 해상도(1280×720) |")
    w("")
    return L


if __name__ == "__main__":
    lines = render()
    print("rendered", len("\n".join(lines)), "chars; assets in", ASSET_DIR)
