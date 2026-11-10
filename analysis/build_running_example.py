"""
Build a running-example trace document for one finished report: every stage's input and output, taken directly from
the recorded files (no LLM is called, CPU only, 2026-11-02).

Sources
  - Video-MME metadata (WorldMM/data/Video-MME/videomme/test.json) and the video file (decord: frames, fps)
  - WorldMM captions (10sec/30sec/3min/10min), semantic triples, visual embeddings; HippoRAG cache (graph, parquet,
    OpenIE results) under report_framework/cache/episodic/<vid>/
  - run outputs: report.json, validation.json, report.md, report_raw.md
  - Deep-Reporter session log (planner / query / writer prompts and raw outputs)
  - LLM server log (tokens / finish / seconds per call) and retrieval service log (per request)
  - grounding_postprocessor.ground_report re-run on report.json (checked to reproduce report.md exactly)
Hand-written observations are not generated here; the output keeps `<!-- OBS:<key> -->` markers for them.
Usage: python analysis/build_running_example.py --video=<vid> [--run outputs/p9p19_check_20261025_141401] [--repeat 1]
Output: internal/running_example/RUNNING_EXAMPLE_<vid>.md
"""
import argparse, collections, glob, json, os, pickle, re, shutil, sys, tempfile

RF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RF)
sys.path.insert(0, os.path.join(RF, "analysis"))
import yaml
import grounding_postprocessor as G
import domain_templates as D
from export_stages import load_jobs, log_lines, cited_txt, cited_img
from rf_config import load_config

_PATHS = load_config(os.path.join(RF, "config.yaml"))["paths"]
WM = _PATHS["worldmm_root"]
CAP = _PATHS["caption_dir"]
META = _PATHS["metadata_dir"]
EPI = _PATHS["episodic_cache_root"]   # report_framework HippoRAG index: <vid>/episodic_memory/<granularity>/
GRANS = ["10sec", "30sec", "3min", "10min"]
# 10sec caption used to illustrate the caption hierarchy and OpenIE (start_time HHMMSSFF)
EXAMPLE_10SEC = {"-QuCz7kxBr8": "00004000", "0RxMZBLeqRI": "00011000", "54k2g9ddy4M": "00043000"}


def sec(t):
    t = str(t).zfill(8)
    return int(t[0:2]) * 3600 + int(t[2:4]) * 60 + int(t[4:6])


def hms_s(s):
    return G.hms(s)


def cut(t, n):
    t = re.sub(r"\s+", " ", str(t)).strip()
    return t if len(t) <= n else t[:n].rstrip() + " …"


def cell(t):
    return t.replace("|", "/").replace("\n", " ")


def fence(text):
    ticks = "````" if "```" in text else "```"
    return f"{ticks}\n{text}\n{ticks}"


def details(summary, body):
    return f"<details><summary>{summary}</summary>\n\n{body}\n\n</details>"


def windows_10min(e3):
    """WorldMM _summarize_level grouping of 3min captions into 10min windows: (label_start, items)."""
    out, cur, b = [], None, []
    for x in sorted(e3, key=lambda x: sec(x["start_time"])):
        s = sec(x["start_time"])
        if cur is None:
            cur = s
        if s < cur + 600:
            b.append(x)
        else:
            out.append((cur, b))
            cur, b = (s // 600) * 600, [x]
    out.append((cur, b))
    return out


def main():
    ap = argparse.ArgumentParser()
    ap.add_argument("--video", required=True)
    ap.add_argument("--run", default=os.path.join(RF, "outputs", "p9p19_check_20261025_141401"))
    ap.add_argument("--repeat", type=int, default=1)
    a = ap.parse_args()
    vid, run = a.video, os.path.abspath(a.run)
    job = f"{vid}__c0_written__r{a.repeat}"
    rdir = os.path.join(run, job)
    rel = lambda p: os.path.relpath(p, RF)
    jobs = load_jobs(run)
    meta_job = jobs[job]
    rj = json.load(open(os.path.join(rdir, "report.json")))
    vj = json.load(open(os.path.join(rdir, "validation.json")))
    report_md = open(os.path.join(rdir, "report.md"), encoding="utf-8").read()
    cfg = yaml.safe_load(open(os.path.join(run, f"config_{job}.yaml")))
    sessions = {}
    for p in glob.glob(os.path.join(run, "dr_logs_s*", "*.jsonl")):
        for line in open(p):
            d = json.loads(line)
            sessions[d["session_id"]] = d
    ses = sessions[rj["session_id"]]
    t0, t1 = ses["start_time"][:19], ses["end_time"][:19]
    stack = meta_job["stack"]
    llm = log_lines(glob.glob(os.path.join(run, f"llm_server_s{stack}_gpu*.log"))[0],
                    r"(\S+ \S+),\d+ local_llm_server INFO chat\.completions: prompt=(\d+) completion=(\d+) finish=(\w+) ([\d.]+)s",
                    t0, t1)
    svc = log_lines(glob.glob(os.path.join(run, f"service_s{stack}_gpu*.log"))[0],
                    r"(\S+ \S+),\d+ videorag_retriever INFO search (\w+): (.*)", t0, t1)
    outline = rj["outline"]
    n = len(outline)
    assert len(llm) == 1 + 3 * n and len(svc) == 2 * n
    calls = ses["llm_calls"]
    q_calls = [c for c in calls if c["call_type"] == "query_generation"]
    w_calls = [c for c in calls if c["call_type"] == "section_writing"]
    tmp = tempfile.mkdtemp(prefix="running_example_")
    try:
        grounded = G.ground_report({"outline": outline}, False, tmp, header=None)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    body_md = report_md.split("\n\n", 1)[1] if report_md.startswith(">") else report_md
    assert grounded["markdown"] == body_md, "ground_report re-run does not reproduce report.md"
    uid2ref = {r["uid"]: r["n"] for r in grounded["references"]}
    uid2fig = {f["uid"]: f["k"] for f in grounded["figures"]}

    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3-VL-8B-Instruct")
    ntok = lambda s: len(tok(s).input_ids)

    L = []
    w = L.append
    # ------------------------------------------------------------------ header
    vm = [r for r in json.load(open(f"{WM}/data/Video-MME/videomme/test.json")) if r["video_id"] == vid]
    import decord
    vpath = f"{WM}/data/Video-MME/data/{vid}.mp4"
    vr = decord.VideoReader(vpath)
    fps, nfr = vr.get_avg_fps(), len(vr)
    caps = {g: json.load(open(f"{CAP}/{vid}/{g}.json")) for g in GRANS}
    end_sec = sec(caps["10sec"][-1]["end_time"])
    secs_words = [len((s["content"] or "").split()) for s in outline]
    w(f"# Running example — `{vid}` (보고서 {job.split('__')[-1]}) 단계별 입력·출력 추적")
    w("")
    w("- 이 문서는 한 영상의 보고서 1건이 만들어지는 과정을 **모든 단계의 실제 입력과 출력**으로 따라간다. 사실 부분은 `analysis/build_running_example.py`가 기록 파일에서 직접 생성했다(LLM 재호출 없음). `> 관찰` 블록은 사람이 근거와 대조해 쓴 해석이다.")
    w(f"- 실행: `{rel(rdir)}` (2026-10-25, 커밋 `baf08d8` 시점 코드). 2026-10-26 변경(영상 끝 근거 txt0, 경고 기준, 결말 검사 오탐 수정)은 이 실행에 없다.")
    w("- 표기: [확인] 코드·데이터로 확인 / [부분 확인] 존재는 확인했으나 영향 정도는 미측정 / [가설] 근거 부족·실험 없음.")
    w("- 전체 프롬프트·근거 원문: `internal/inspect/" + os.path.basename(run) + f"/{job}/` (`analysis/export_stages.py`로 생성).")
    w("")
    w("## 목차")
    w("0. 한눈에 · 1. 입력 · 2. 오프라인 메모리 · 3. 실행 준비 · 4. planner · 5. 섹션별 처리(query → 검색 → writer → 후처리) · 6. 최종 산출물·검증 · 7. 단계별 문제점·한계 요약")
    w("")
    # ------------------------------------------------------------------ 0
    w("## 0. 한눈에")
    w("")
    w("| 항목 | 값 |")
    w("|---|---|")
    w(f"| 영상 | `{vid}` ({vm[0]['domain']} / {vm[0]['sub_category']}, Video-MME duration `{vm[0]['duration']}`) |")
    w(f"| 길이 | 파일 {nfr:,}프레임 ÷ {fps:.3f} fps = {nfr / fps:,.1f}초, 10sec 캡션 끝 {hms_s(end_sec)} |")
    w(f"| 질의 | {rj['query']} (checklist {rj['checklist']}) |")
    w(f"| 결과 | 섹션 {n}개, 본문 {sum(secs_words):,}단어(인용 표기 포함), References {len(grounded['references'])}개, 그림 {len(grounded['figures'])}개, 검증 `{vj['status']}`, 생성 {vj['timings']['generation_sec']}초, LLM 호출 {len(llm)}회 |")
    w(f"| 실행 위치 | 묶음 {stack} (GPU {meta_job['gpu']}), 세션 `{rj['session_id']}` {t0} – {t1} UTC |")
    w("")
    w("```")
    w("[1 입력] 영상 + 질의")
    w("[2 오프라인] WorldMM 캡션 4단위 + semantic triple + visual 임베딩 → HippoRAG 그래프 4개 (사전 인덱싱)")
    w("[3 준비] 사전 확인 → 영상 개요(10min 캡션 전부) + 영상 끝 시각 → 템플릿 교체 + C0")
    w(f"[4 planner] LLM 1회 → outline {n}개 섹션")
    w(f"[5 섹션 × {n}] query 생성(LLM) → 검색(text: 그래프 검색 → RRF → L1 필터(LLM) + semantic / image: VLM2Vec) → writer(LLM) → 다음 섹션 맥락(C0)")
    w("[6 후처리] 반복 문장 제거 → 결말·시작 검사 → 인용 → References·그림 → 규칙 근거 검사 → 검증")
    w("```")
    w("")
    # ------------------------------------------------------------------ 1
    w("## 1. 입력")
    w("")
    w(f"- **영상 파일**: `{rel(vpath) if vpath.startswith(RF) else vpath}` ({os.path.getsize(vpath):,} bytes, {vr[0].shape[1]}×{vr[0].shape[0]}, {fps:.3f} fps). 보고서 생성 단계에서 영상 파일을 직접 읽는 곳은 image 검색의 프레임 추출뿐이다(코드: `extract_center_frame`).")
    w(f"- **Video-MME 메타**: domain `{vm[0]['domain']}`, sub_category `{vm[0]['sub_category']}`, URL {vm[0]['url']}. 이 영상의 QA {len(vm)}문항(보고서 생성에는 쓰지 않음):")
    for q in vm:
        w(f"  - {q['question']} (정답 {q['answer']})")
    w(f"- **질의(overall_query)**: `{rj['query']}`")
    w(f"- **checklist**: `{rj['checklist']}`")
    r_ = cfg["report"]; rt = cfg["retrieval"]; ep = cfg["llm"]["local"]["endpoint"]
    w("- **설정** (실행에 쓰인 `" + f"config_{job}.yaml" + "`)")
    w("")
    w("| 키 | 값 |")
    w("|---|---|")
    for k, v in [("llm.local.endpoint.model", ep["model"]), ("llm.local.endpoint.max_tokens_cap", ep.get("max_tokens_cap")),
                 ("retrieval.episodic_filter", rt["episodic_filter"]), ("retrieval.episodic_candidates_per_query", rt["episodic_candidates_per_query"]),
                 ("retrieval.episodic_k / semantic_k / image_k", f"{rt['episodic_k']} / {rt['semantic_k']} / {rt['image_k']}"),
                 ("retrieval.semantic_k_per_query / visual_k_per_query / rrf_k", f"{rt['semantic_k_per_query']} / {rt['visual_k_per_query']} / {rt['rrf_k']}"),
                 ("report.text_topk / image_topk / enable_filter", f"{r_['text_topk']} / {r_['image_topk']} / {r_['enable_filter']}"),
                 ("report.overview_granularity", r_["overview_granularity"]), ("report.max_sections", r_["max_sections"]),
                 ("report.previous_sections_context", r_["previous_sections_context"]), ("report.translate_ko", r_["translate_ko"])]:
        w(f"| `{k}` | `{v}` |")
    w("- 생성 방식: Deep-Reporter와 서버가 temperature를 보내지 않아 모델 기본값(do_sample, temperature 0.7, top_p 0.8, top_k 20)으로 샘플링한다. seed 없음. 같은 조건에서도 실행마다 결과가 다르다(`SELF_CONSISTENCY_CAUSES.md` §1).")
    w("")
    # ------------------------------------------------------------------ 2
    w("## 2. 오프라인 메모리 (WorldMM 전처리 + 사전 인덱싱, 보고서 생성 전에 만들어 둠)")
    w("")
    w("### 2.1 캡션 4단위")
    w("")
    w("| 단위 | 항목 수 | 단어 수 평균 / 최대 | 만드는 방법 (WorldMM) |")
    w("|---|---|---|---|")
    how = {"10sec": "프레임 + Whisper 자막 → VLM 캡션", "30sec": "10sec 캡션 묶음을 LLM 요약(L1 프롬프트)",
           "3min": "30sec 요약 묶음을 LLM 요약(L2, ≤300단어 지시)", "10min": "3min 요약 묶음을 LLM 요약(L3, ≤1500단어 지시, 출력 최대 2,048토큰)"}
    for g in GRANS:
        ws = [len(str(e["text"]).split()) for e in caps[g]]
        w(f"| {g} | {len(caps[g])} | {sum(ws) / len(ws):.0f} / {max(ws)} | {how[g]} |")
    w("- 상위 단위는 바로 아래 단위의 텍스트만 **시각 표기 없이** 이어 붙여(`\"All descriptions: …\"`) 요약한다(WorldMM `gen_multiscale.py`). 그래서 30sec·3min·10min 캡션 안에는 장면별 시각이 없다.")
    w("")
    # one 10sec caption traced up through the 30sec / 3min / 10min summaries that contain it
    ex = EXAMPLE_10SEC[vid]
    e10 = next(e for e in caps["10sec"] if str(e["start_time"]).zfill(8) == ex)
    t_ex = sec(ex)
    def containing(g):
        return next(e for e in caps[g] if sec(e["start_time"]) <= t_ex < sec(e["end_time"]))
    e30, e3m = containing("30sec"), containing("3min")
    blk = next((e for e, (ws_, items) in zip(caps["10min"], windows_10min(caps["3min"])) if any(i is e3m for i in items)), None)
    w(f"**예: 10sec 캡션 {G.hms_from_time_str(ex)} 하나가 상위 요약으로 올라가는 모습** (원문 그대로, 길면 앞부분만)")
    w("")
    w("| 단위 | 구간 | 텍스트 |")
    w("|---|---|---|")
    w(f"| 10sec | {G.hms_from_time_str(e10['start_time'])}–{G.hms_from_time_str(e10['end_time'])} | {cell(cut(e10['text'], 600))} |")
    w(f"| 30sec | {G.hms_from_time_str(e30['start_time'])}–{G.hms_from_time_str(e30['end_time'])} | {cell(cut(e30['text'], 600))} |")
    w(f"| 3min | {G.hms_from_time_str(e3m['start_time'])}–{G.hms_from_time_str(e3m['end_time'])} | {cell(cut(e3m['text'], 600))} |")
    if blk is not None:
        w(f"| 10min | 라벨 {G.hms_from_time_str(blk['start_time'])}–{G.hms_from_time_str(blk['end_time'])} | {cell(cut(blk['text'], 600))} |")
    w("")
    # 10min overview blocks
    w("### 2.2 10min 캡션 = planner가 보는 영상 개요")
    w("")
    w("| 블록 라벨 | 실제로 묶인 3min 캡션 (시작) → 내용 구간 | 토큰 | 2,048토큰 상한 도달 | 마지막 120자 |")
    w("|---|---|---|---|---|")
    wins = windows_10min(caps["3min"])
    for e, (ws_, items) in zip(caps["10min"], wins):
        tk = ntok(e["text"])
        lab = f"{G.hms_from_time_str(e['start_time'])}–{G.hms_from_time_str(e['end_time'])}"
        span = f"{', '.join(G.hms_from_time_str(i['start_time'])[3:] for i in items)} → {G.hms_from_time_str(items[0]['start_time'])}–{hms_s(min(sec(items[-1]['end_time']), end_sec))}"
        w(f"| {lab} | {span} | {tk:,} | {'**예**' if tk >= 2048 else '아니오'} | {cell(cut(e['text'][-120:], 120))} |")
    w("- 라벨은 `[시작, 시작+10분)`이지만, WorldMM은 시작 시각이 창 안인 3min 캡션을 그 창에 넣으므로 실제 내용 구간이 라벨과 다를 수 있다(위 표의 두 번째 열). [확인]")
    w("")
    # HippoRAG
    w("### 2.3 HippoRAG 그래프 (단위마다 1개, `" + os.path.relpath(EPI, os.path.dirname(RF)) + "/" + vid + "/episodic_memory/<단위>/`)")
    w("")
    w("| 단위 | passage(캡션) | entity | fact(triple) | fact 엣지 | synonym 엣지 | passage–entity 엣지 |")
    w("|---|---|---|---|---|---|---|")
    import pandas as pd
    base = os.path.join(EPI, vid, "episodic_memory")
    for g in GRANS:
        d_ = glob.glob(f"{base}/{g}/qwen3vl-8b_*")[0]
        Gr = pickle.load(open(f"{d_}/graph.pickle", "rb"))
        names = Gr.vs["name"]
        kinds = collections.Counter()
        for e, wt in zip(Gr.es, Gr.es["weight"]):
            a_, b_ = names[e.source], names[e.target]
            if a_.startswith("chunk") or b_.startswith("chunk"):
                kinds["pe"] += 1
            elif float(wt).is_integer() and wt >= 1:
                kinds["f"] += 1
            else:
                kinds["s"] += 1
        cnt = lambda sub: len(pd.read_parquet(glob.glob(f"{d_}/{sub}/*.parquet")[0]))
        w(f"| {g} | {cnt('chunk_embeddings'):,} | {cnt('entity_embeddings'):,} | {cnt('fact_embeddings'):,} | {kinds['f']:,} | {kinds['s']:,} | {kinds['pe']:,} |")
    w("- 엣지 수는 igraph 엣지 수 그대로다(fact 엣지는 두 방향이 각각 들어 있음). 종류는 passage 노드 포함 여부와 가중치가 정수인지로 나눴다. 임베딩은 Qwen3-Embedding-4B(instruction 없음, 정규화).")
    w("")
    oi = json.load(open(glob.glob(f"{base}/10sec/openie_results_ner_*.json")[0]))["docs"]
    doc = next((d_ for d_ in oi if d_["passage"].strip() == str(e10["text"]).strip()), None)
    w(f"**예: 위 10sec 캡션({G.hms_from_time_str(ex)})이 그래프에 들어간 모습** (10sec OpenIE 결과 원문)")
    w("")
    if doc:
        w(f"- NER(개체): " + ", ".join(f"`{x}`" for x in doc["extracted_entities"]))
        w(f"- triple {len(doc['extracted_triples'])}개: " + "; ".join(f"`({', '.join(map(str, t))})`" for t in doc["extracted_triples"]))
        ent0 = str(doc["extracted_triples"][0][0]) if doc["extracted_triples"] else ""
        norm0 = re.sub("[^A-Za-z0-9 ]", " ", ent0.lower()).strip()
        w(f"- 이 캡션은 passage 노드 1개가 되고, triple의 주어·목적어는 HippoRAG `text_processing`(소문자화, 영문·숫자·공백 외 문자를 공백으로)을 거쳐 entity 노드가 된다(예: `{ent0}` → `{norm0}`). 같은 entity를 공유하는 다른 캡션과 그래프로 이어진다.")
    else:
        w("- (OpenIE 결과에서 같은 passage를 찾지 못함)")
    w("")
    # semantic / visual
    sem = json.load(open(f"{META}/semantic_memory/{vid}/semantic_consolidation_results_qwen3vl-8b.json"))
    last_key = sorted(sem.keys())[-1]
    triples = sem[last_key]["consolidated_semantic_triples"]
    deg = collections.Counter()
    for s_, p_, o_ in triples:
        deg[s_] += 1
        deg[o_] += 1
    w("### 2.4 semantic triple (시간 정보 없음)")
    w("")
    w(f"- 검색에 쓰이는 마지막 묶음(`{last_key}`): triple {len(triples)}개, 개체 {len(deg)}개. 연결이 많은 개체: " + ", ".join(f"`{e}`({c})" for e, c in deg.most_common(5)) + ".")
    w("- 예: " + "; ".join(f"`({s_}, {p_}, {o_})`" for s_, p_, o_ in triples[:3]))
    vis = pickle.load(open(f"{META}/visual_memory/{vid}/visual_embeddings.pkl", "rb"))
    first = next(iter(vis.values()))
    w("")
    w("### 2.5 visual 임베딩")
    w("")
    w(f"- 10sec 구간마다 VLM2Vec-V2 비디오 임베딩 1개: {len(vis)}개, 차원 {getattr(first, 'shape', ['?'])[-1]}. 50개 영상 전처리 설정은 구간당 10프레임, 최대 360×420픽셀(`process_one_video.sh --num-frames 10`).")
    w("")
    # ------------------------------------------------------------------ 3
    w("## 3. 실행 준비 (`run_report.py`, LLM 0회)")
    w("")
    w(f"- 사전 확인(LLM·검색 서비스 health, 영상 불러오기, 템플릿 계약): {vj['timings']['preflight_sec']}초.")
    w(f"- 영상 끝 시각: `{vj['video_end']}` (10sec 캡션 마지막 `end_time`) → writer 규칙 7과 결말·시작 검사에 들어감.")
    w(f"- 영상 개요: 10min 캡션 {len(caps['10min'])}개를 `[HH:MM:SS-HH:MM:SS] 텍스트`로 이어 붙임 → planner 템플릿의 `<<VIDEO_OVERVIEW>>` 자리.")
    w(f"- 템플릿 교체: planner·query·writer 프롬프트를 videomme 템플릿으로 실행 중에만 교체. C0(`previous_sections_context: {vj['previous_sections_context']}`)로 다음 섹션 맥락 함수를 교체.")
    w("")
    # ------------------------------------------------------------------ 4
    pc = calls[0]
    pin = pc["input_messages"][0]["content"]
    i_ov, i_task = pin.find("**Video overview**"), pin.find("**Task:**")
    w("## 4. planner: outline 만들기 (LLM 1회)")
    w("")
    w("### 4.1 입력 (프롬프트 구성)")
    w("")
    w("| 부분 | 글자 수 | 내용 |")
    w("|---|---|---|")
    w(f"| 역할·질의·checklist | {i_ov:,} | 질의 원문, checklist(빈 값) |")
    w(f"| 영상 개요 | {i_task - i_ov:,} | 10min 캡션 {len(caps['10min'])}개 전부 (§2.2) |")
    w(f"| 규칙·출력 형식 | {len(pin) - i_task:,} | 섹션 3–{cfg['report']['max_sections']}개, 영상 근거만, 시간순, 설명 2–4문장·대략의 시간 범위, checklist 3–5개, 마지막은 `Conclusion:` |")
    w(f"| **합계** | **{len(pin):,}** | 서버 로그 프롬프트 {llm[0].group(2)}토큰 |")
    w("- 메시지는 user 1개(system 없음). 영상 프레임·세밀한 캡션·semantic은 들어가지 않는다. [확인]")
    w(f"- 전문: `internal/inspect/{os.path.basename(run)}/{job}/01_planner_prompt.md`")
    w("")
    w("### 4.2 출력")
    w("")
    w(f"- 출력 {llm[0].group(3)}토큰, `{llm[0].group(4)}`, {llm[0].group(5)}초. JSON 파싱 성공(fallback 없음).")
    w("")
    w("| 섹션 | section_description | sectional_checklist | 설명 속 시간 범위 |")
    w("|---|---|---|---|")
    for i, s in enumerate(outline, 1):
        rngs = re.findall(r"\d\d:\d\d:\d\d\s*[-–]\s*\d\d:\d\d:\d\d", s["section_description"])
        w(f"| S{i} | {cell(s['section_description'])} | {cell(' / '.join(s['sectional_checklist']))} | {', '.join(rngs) or '없음'} |")
    w("")
    w("<!-- OBS:planner -->")
    w("")
    # ------------------------------------------------------------------ 5
    w("## 5. 섹션별 처리")
    w("")
    w("각 섹션은 같은 4단계를 거친다: (a) query 생성(LLM) → (b) 검색(검색 서비스, text 요청 안에서 L1 필터 LLM 1회) → (c) writer(LLM) → (d) 후처리(LLM 0회). (a)·(c)의 앞 섹션 요약(C0)은 직전 섹션들의 writer 출력에서 만들어진다.")
    w("")
    for i, s in enumerate(outline, 1):
        q, f_, wl = llm[1 + 3 * (i - 1)], llm[2 + 3 * (i - 1)], llm[3 + 3 * (i - 1)]
        qc, wc = q_calls[i - 1], w_calls[i - 1]
        st, si = svc[2 * (i - 1)], svc[2 * (i - 1) + 1]
        texts, imgs = s["retrieved_texts"] or [], s["retrieved_images"] or []
        content = s["content"] or ""
        ct, ci = set(cited_txt(content)), set(cited_img(content))
        title = next((ln.lstrip("#").strip() for ln in content.split("\n") if ln.startswith("#")), "")
        w(f"### 5.{i} 섹션 {i}: {title}")
        w("")
        w(f"- planner 설명: {s['section_description']}")
        w(f"- checklist: " + " / ".join(s["sectional_checklist"]))
        w("")
        # (a)
        qin = qc["input_messages"][0]["content"]
        m = re.search(r"\*\*Previous sections \(summary\):\*\*\n([\s\S]*?)\n\n\*\*Current section:\*\*", qin)
        summ = m.group(1).strip() if m else "(찾지 못함)"
        w(f"**(a) query 생성** — 프롬프트 {q.group(2)}토큰, 출력 {q.group(3)}토큰, `{q.group(4)}`, {q.group(5)}초")
        w("")
        w("- 입력 중 앞 섹션 요약(C0) 부분:")
        w("")
        w(fence(summ))
        w("")
        w("- 출력(파싱 결과):")
        for k, x in enumerate(s["text_queries"] or [], 1):
            w(f"  - text {k}: `{x}`")
        for k, x in enumerate(s["image_queries"] or [], 1):
            w(f"  - image {k}: `{x}`")
        w("")
        # (b)
        stm = st.group(3)
        w(f"**(b) 검색** — text 요청 `{stm}`; image 요청 `{si.group(3)}`")
        w("")
        w(f"- 처리: text query {len(s['text_queries'])}개 × 4단위 그래프 검색(단위별 후보 3/3/2/1) → RRF 병합 → L1 필터 LLM(프롬프트 {f_.group(2)}토큰, 출력 {f_.group(3)}토큰, {f_.group(5)}초)이 episodic 8개 선택 + semantic 4개. image query {len(s['image_queries'])}개 → VLM2Vec 유사도 상위 3구간 → 중앙 프레임.")
        w("- L1 필터의 후보 목록과 응답 원문은 기록되지 않는다.")
        w("")
        w("| 근거 | 인용 | 전역 번호 | 출처 | 단위 | 시간 | 순위 | 내용 (앞 170자) |")
        w("|---|---|---|---|---|---|---|---|")
        for k, t in enumerate(texts, 1):
            tm = (f"{G.hms_from_time_str(t['start_time'])}–{G.hms_from_time_str(t['end_time'])}" if t.get("start_time") else "없음")
            w(f"| txt{k} | {'✓' if k in ct else ''} | {('[' + str(uid2ref[t['uid']]) + ']') if k in ct and t['uid'] in uid2ref else ''} | {t['source'].replace('worldmm-', '')} | {t.get('granularity') or '—'} | {tm} | {t.get('rank')} | {cell(cut(G.strip_label(t['content']), 170))} |")
        for k, m_ in enumerate(imgs, 1):
            fig = uid2fig.get(m_["uid"]) if k in ci else None
            w(f"| img{k} | {'✓' if k in ci else ''} | {('Figure ' + str(fig)) if fig else ''} | visual | 프레임 {G.hms(m_['frame_sec'])} | {G.hms_from_time_str(m_['start_time'])}–{G.hms_from_time_str(m_['end_time'])} | {m_.get('rank')} | {cell(cut(G.strip_label(m_['caption']), 170))} |")
        w("")
        w(f"- 프레임 파일: " + ", ".join(f"img{k} `{rel(m_['img_path'])}`" for k, m_ in enumerate(imgs, 1)))
        w("")
        # (c)
        win = wc["input_messages"][0]["content"]
        w(f"**(c) writer** — 프롬프트 {wl.group(2)}토큰({len(win):,}자), 출력 {wl.group(3)}토큰, `{wl.group(4)}`, {wl.group(5)}초" + (" — **서버 상한 3,072토큰에서 끊김**" if wl.group(4) == "length" else ""))
        w("")
        w(f"- 입력: 섹션 위치 `Section {i}/{n}`, 설명·checklist, 앞 섹션 요약(위와 같은 C0) + 직전 섹션 끝 3조각, 근거 text {len(texts)}개(`content` 전문) + image {len(imgs)}개(캡션 문자열만), 규칙(Grounding 1–7, Citation 1–4, 위치별, 결론, 형식). 전문: `internal/inspect/{os.path.basename(run)}/{job}/s{i:02d}/4_writer_prompt.md`")
        w("")
        w(details(f"writer 출력 원문 ({len(wc['output_content'].split())}단어, 후처리 전)", fence(wc["output_content"])))
        w("")
        # (d)
        rep = next(r for r in vj["repetition"] if r["index"] == i)
        bnd = [b for b in vj["boundary_findings"] if b["section"] == i]
        gf = [g for g in vj["grounding_findings"] if g["section"] == i]
        vs = next(x for x in vj["sections"] if x["index"] == i)
        w("**(d) 후처리·검사**")
        w("")
        w(f"- 반복 문장 제거: {rep['removed_sentences']}개 제거, 최대 반복 {rep['max_repeat']}회, 문장 중간 끝 {rep['ends_mid_sentence']} → 본문 {len(wc['output_content'].split())} → {len(content.split())}단어")
        w(f"- 인용 변환: 텍스트 인용 {vs['citations']['text_citations']}개 → 전역 번호, 그림 삽입 {vs['citations']['image_embeds']}개, 금지 형식 `[citation:imgN]` 변환 {vs['citations']['wrong_form_image_citations']}개, 잘못된 번호 {vs['citations']['invalid_citations']}개, 인용 안 된 텍스트 근거 {vs['unused_text_evidence']}/{len(texts)}")
        w(f"- 규칙 근거 검사: `{json.dumps(vs['grounding_stats'])}`")
        for g in gf:
            if g["status"] != "uncited":
                w(f"  - **{g['status']}** {g.get('kind', '')} `{g.get('token', g.get('tokens', ''))}` (인용 {g.get('cited')}" + (f", 다른 근거 {g['found_in_uncited']}에 있음" if g.get("found_in_uncited") else "") + f"): {cut(g['sentence'], 200)}")
        unc = [g for g in gf if g["status"] == "uncited"]
        if unc:
            w(f"  - uncited {len(unc)}건(인용 없이 수치·문구가 있는 문장), 예: {cut(unc[0]['sentence'], 160)}")
        w(f"- 결말·시작 서술 검사: " + ("; ".join(f"**{b['status']}** — {cut(b['sentence'], 160)}" + (f" (인용 근거 끝 {b['latest_cited_end']})" if b.get('latest_cited_end') else "") for b in bnd) if bnd else "해당 없음"))
        al = vs["image_time_alignment"]
        w(f"- 이미지-텍스트 시간 차: " + ("; ".join(f"{x['img']} 프레임 {x['frame']} → 같은 단락 텍스트와 {x['gap_to_local_text_sec']}초, 섹션 텍스트와 {x['gap_to_section_text_sec']}초" for x in al) if al else "인용 이미지 없음"))
        w("")
        w(details("최종 본문 (report.md의 이 섹션 그대로)", fence(grounded["section_bodies"][i - 1])))
        w("")
        w(f"<!-- OBS:s{i} -->")
        w("")
    # ------------------------------------------------------------------ 6
    w("## 6. 최종 산출물과 검증")
    w("")
    w("| 파일 | 내용 |")
    w("|---|---|")
    w(f"| `{rel(rdir)}/report.md` | 헤더 + 섹션 {n}개 + References {len(grounded['references'])}개, 그림 {len(grounded['figures'])}개 |")
    w(f"| `report_raw.md` | Deep-Reporter 원본({len(open(os.path.join(rdir, 'report_raw.md')).read().split()):,}단어, 반복 제거 전) |")
    w("| `report.json` | 섹션별 설명·checklist·검색어·근거 전체·본문(반복 제거 후), References, 그림 |")
    w("| `validation.json` | 상태, 경고, 시간, 반복, 결말·시작 검사, 규칙 검사, 이미지 시간 차 |")
    w(f"| `frames/` | 인용 프레임 {len(grounded['figures'])}장 |")
    w("")
    w(f"- 섹션별 단어 수(반복 제거 후): " + ", ".join(f"S{i} {c}" for i, c in enumerate(secs_words, 1)))
    w(f"- 인용 통계: `{json.dumps(vj['citation_stats'])}`")
    w(f"- 규칙 검사 합계: `{json.dumps(vj['grounding_stats'])}`")
    w(f"- 이미지-텍스트 시간 차 요약: `{json.dumps(vj['image_time_alignment'])}`")
    w(f"- 상태 `{vj['status']}`, 오류 {len(vj['errors'])}개. 경고:")
    for x in vj["warnings"]:
        w(f"  - {x}")
    w("")
    w("References 앞 5개 (전역 번호 → 근거):")
    w("")
    w(fence("\n".join(r["line"] for r in grounded["references"][:5])))
    w("")
    w("LLM 호출 (서버 로그, 호출 순서):")
    w("")
    w("| 호출 | 섹션 | 프롬프트 토큰 | 출력 토큰 | 종료 | 초 |")
    w("|---|---|---|---|---|---|")
    w(f"| planner | — | {llm[0].group(2)} | {llm[0].group(3)} | {llm[0].group(4)} | {llm[0].group(5)} |")
    for i in range(1, n + 1):
        for name, m in (("query", llm[1 + 3 * (i - 1)]), ("L1 필터", llm[2 + 3 * (i - 1)]), ("writer", llm[3 + 3 * (i - 1)])):
            w(f"| {name} | {i} | {m.group(2)} | {m.group(3)} | {m.group(4)} | {m.group(5)} |")
    tsum = lambda k: round(sum(float(llm[k + 3 * j].group(5)) for j in range(n)), 1)
    w(f"- 합계: planner {llm[0].group(5)}초, query {tsum(1)}초, L1 필터 {tsum(2)}초, writer {tsum(3)}초 / 생성 {vj['timings']['generation_sec']}초. 후처리 {vj['timings']['postprocess_sec']}초.")
    w("")
    w("<!-- OBS:summary -->")
    w("")
    out = os.path.join(RF, "internal", "running_example", f"RUNNING_EXAMPLE_{vid}.md")
    os.makedirs(os.path.dirname(out), exist_ok=True)
    open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote", out, len("\n".join(L)), "chars")


if __name__ == "__main__":
    main()
