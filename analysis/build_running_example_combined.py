"""
Build ONE integrated running-example document for the three videos, organised by pipeline stage (2026-11-02).
Same sources and the same computations as analysis/build_running_example.py (no LLM call, CPU only); hand-written
observations come from analysis/running_example_observations.py, with their section references rewritten to the
numbering of this document (every rewrite is asserted to occur exactly once).
Checks done while building: ground_report re-run reproduces report.md exactly; LLM calls = 1 + 3 x sections;
search requests = 2 x sections; the three runs used the same values for every setting shown in §2.2.
§10 (deep dive into -QuCz7kxBr8 r1: memories, frames, every module input/output) comes from
analysis/build_running_example_deep.py, which needs results/retrieval_repro_-QuCz7kxBr8_r1.json
(analysis/reproduce_retrieval_cpu.py) and writes the images under internal/running_example/assets/-QuCz7kxBr8/.
Usage: python analysis/build_running_example_combined.py
Output: internal/running_example/RUNNING_EXAMPLE.md
"""
import collections, glob, json, os, pickle, re, shutil, sys, tempfile

RF = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, RF)
sys.path.insert(0, os.path.join(RF, "analysis"))
import yaml
import grounding_postprocessor as G
from export_stages import load_jobs, log_lines, cited_txt, cited_img
from build_running_example import (WM, CAP, META, EPI, GRANS, EXAMPLE_10SEC, sec, hms_s, cut, cell, fence, details,
                                   windows_10min)
from running_example_observations import OBS

RUN = os.path.join(RF, "outputs", "p9p19_check_20261025_141401")
VIDEOS = ["-QuCz7kxBr8", "0RxMZBLeqRI", "54k2g9ddy4M"]
SHORT = {"-QuCz7kxBr8": "농구 가젯 시험", "0RxMZBLeqRI": "로마 역사", "54k2g9ddy4M": "CBC 뉴스 모음"}
VNUM = {v: i for i, v in enumerate(VIDEOS, 1)}          # section 6.<VNUM>
rel = lambda p: os.path.relpath(p, RF)

# Section references inside the hand-written observations (written for the per-video documents) -> this document.
# (video, observation key, old text, new text); each old text must occur exactly once in that observation.
REF_MAP = [
    ("-QuCz7kxBr8", "planner", "(§4.2 마지막 열)", "(§5.2 마지막 열)"),
    ("-QuCz7kxBr8", "planner", "실제로는 12–21분 내용이다(§2.2)", "실제로는 12–21분 내용이다(§3.3)"),
    ("-QuCz7kxBr8", "planner", "이 구간을 인용한 섹션도 없다(§7)", "이 구간을 인용한 섹션도 없다(§8.1)"),
    ("0RxMZBLeqRI", "planner", "10–20분 블록도 2,048토큰에서 끊겼다(§2.2)", "10–20분 블록도 2,048토큰에서 끊겼다(§3.3)"),
    ("0RxMZBLeqRI", "planner", "공산 정권 박해를 서술한 캡션이 없다(§5.5)", "공산 정권 박해를 서술한 캡션이 없다(§6.2.5)"),
    ("0RxMZBLeqRI", "planner", "이 항목이 결론 검색어로 이어졌다(§5.6)", "이 항목이 결론 검색어로 이어졌다(§6.2.6)"),
    ("0RxMZBLeqRI", "s4", "§2.1 예시의 10sec 01:10 캡션", "§3.2 예시의 10sec 01:10 캡션"),
    ("54k2g9ddy4M", "planner", "(§4.2 마지막 열)", "(§5.2 마지막 열)"),
    ("54k2g9ddy4M", "planner", "에서 왔다(§5.1)", "에서 왔다(§6.3.1)"),
    ("54k2g9ddy4M", "planner", "다른 결말을 미리 지정했다(§5.6)", "다른 결말을 미리 지정했다(§6.3.6)"),
    ("54k2g9ddy4M", "s2", "(§2.1 예시 표)", "(§3.2 예시 표)"),
    ("54k2g9ddy4M", "s5", "(§4 관찰)", "(§5.3)"),
]


EXTERNAL_REF_RE = re.compile(r"\.md`\s*§[\d.]+(?:·§[\d.]+)*")   # e.g. `DESIGN_AND_STATUS.md` §9.17, `X.md` §2.3·§4


def obs(vid, key):
    original = OBS[vid][key]
    text = original
    replaced = 0
    for v, k, old, new in REF_MAP:
        if v == vid and k == key:
            assert text.count(old) == 1, (vid, key, old)
            text = text.replace(old, new)
            replaced += old.count("§")
    # every § reference of the original that is not a reference into another document must have been rewritten
    internal = len(re.findall(r"§\d", EXTERNAL_REF_RE.sub("", original)))
    assert internal == replaced, (vid, key, internal, replaced, original)
    return text


def load(vid):
    job = f"{vid}__c0_written__r1"
    rdir = os.path.join(RUN, job)
    jobs = load_jobs(RUN)
    rj = json.load(open(os.path.join(rdir, "report.json")))
    vj = json.load(open(os.path.join(rdir, "validation.json")))
    report_md = open(os.path.join(rdir, "report.md"), encoding="utf-8").read()
    cfg = yaml.safe_load(open(os.path.join(RUN, f"config_{job}.yaml")))
    sessions = {}
    for p in glob.glob(os.path.join(RUN, "dr_logs_s*", "*.jsonl")):
        for line in open(p):
            d = json.loads(line)
            sessions[d["session_id"]] = d
    ses = sessions[rj["session_id"]]
    t0, t1 = ses["start_time"][:19], ses["end_time"][:19]
    stack = jobs[job]["stack"]
    llm = log_lines(glob.glob(os.path.join(RUN, f"llm_server_s{stack}_gpu*.log"))[0],
                    r"(\S+ \S+),\d+ local_llm_server INFO chat\.completions: prompt=(\d+) completion=(\d+) finish=(\w+) ([\d.]+)s",
                    t0, t1)
    svc = log_lines(glob.glob(os.path.join(RUN, f"service_s{stack}_gpu*.log"))[0],
                    r"(\S+ \S+),\d+ videorag_retriever INFO search (\w+): (.*)", t0, t1)
    outline = rj["outline"]
    n = len(outline)
    assert len(llm) == 1 + 3 * n and len(svc) == 2 * n, vid
    calls = ses["llm_calls"]
    tmp = tempfile.mkdtemp(prefix="running_example_")
    try:
        grounded = G.ground_report({"outline": outline}, False, tmp, header=None)
    finally:
        shutil.rmtree(tmp, ignore_errors=True)
    body_md = report_md.split("\n\n", 1)[1] if report_md.startswith(">") else report_md
    assert grounded["markdown"] == body_md, vid
    caps = {g: json.load(open(f"{CAP}/{vid}/{g}.json")) for g in GRANS}
    import decord
    vpath = f"{WM}/data/Video-MME/data/{vid}.mp4"
    vr = decord.VideoReader(vpath)
    return dict(vid=vid, job=job, rdir=rdir, rj=rj, vj=vj, cfg=cfg, ses=ses, t0=t0, t1=t1, stack=stack, gpu=jobs[job]["gpu"],
                llm=llm, svc=svc, outline=outline, n=n, calls=calls,
                q_calls=[c for c in calls if c["call_type"] == "query_generation"],
                w_calls=[c for c in calls if c["call_type"] == "section_writing"],
                grounded=grounded, uid2ref={r["uid"]: r["n"] for r in grounded["references"]},
                uid2fig={f["uid"]: f["k"] for f in grounded["figures"]}, caps=caps,
                end_sec=sec(caps["10sec"][-1]["end_time"]), vpath=vpath, fps=vr.get_avg_fps(), nfr=len(vr),
                shape=vr[0].shape,
                vm=[r for r in json.load(open(f"{WM}/data/Video-MME/videomme/test.json")) if r["video_id"] == vid])


SETTING_KEYS = [
    ("llm.local.endpoint.model", lambda c: c["llm"]["local"]["endpoint"]["model"]),
    ("llm.local.endpoint.max_tokens_cap", lambda c: c["llm"]["local"]["endpoint"].get("max_tokens_cap")),
    ("retrieval.episodic_filter", lambda c: c["retrieval"]["episodic_filter"]),
    ("retrieval.episodic_candidates_per_query", lambda c: c["retrieval"]["episodic_candidates_per_query"]),
    ("retrieval.episodic_k / semantic_k / image_k", lambda c: f"{c['retrieval']['episodic_k']} / {c['retrieval']['semantic_k']} / {c['retrieval']['image_k']}"),
    ("retrieval.semantic_k_per_query / visual_k_per_query / rrf_k", lambda c: f"{c['retrieval']['semantic_k_per_query']} / {c['retrieval']['visual_k_per_query']} / {c['retrieval']['rrf_k']}"),
    ("report.text_topk / image_topk / enable_filter", lambda c: f"{c['report']['text_topk']} / {c['report']['image_topk']} / {c['report']['enable_filter']}"),
    ("report.overview_granularity", lambda c: c["report"]["overview_granularity"]),
    ("report.max_sections", lambda c: c["report"]["max_sections"]),
    ("report.previous_sections_context", lambda c: c["report"]["previous_sections_context"]),
    ("report.translate_ko", lambda c: c["report"]["translate_ko"]),
]


def main():
    from transformers import AutoTokenizer
    tok = AutoTokenizer.from_pretrained("Qwen/Qwen3-VL-8B-Instruct")
    ntok = lambda s: len(tok(s).input_ids)
    import pandas as pd
    C = {v: load(v) for v in VIDEOS}
    # settings identical across the three runs (asserted)
    for k, f in SETTING_KEYS:
        vals = {str(f(C[v]["cfg"])) for v in VIDEOS}
        assert len(vals) == 1, (k, vals)
    L = []
    w = L.append
    tt = lambda v: f"`{v}` ({SHORT[v]})"

    # ================================================================== 0
    w("# Running example — 영상 3개로 추적하는 보고서 생성 파이프라인 (통합본)")
    w("")
    w("## 0. 문서 안내")
    w("")
    w("- **목적**: 프레임워크의 구조·모듈 동작·중간 산출물을 보여 주는 발표 자료의 근거 문서다. 같은 질의·같은 설정으로 만든 보고서 3건(영상별 r1)이 입력 → 오프라인 메모리 → 실행 준비 → planner → 섹션별 query·검색·writer·후처리 → 최종 산출물·검증을 거치는 동안의 **실제 입력과 출력**을 단계별로 보여 준다.")
    w("- **구성**")
    w("  - §2–§5와 §7은 단계별로 세 영상을 나란히 둔다.")
    w("  - §6(섹션별 처리)은 영상별로 섹션 6개를 모두 따라간다.")
    w("  - §8은 단계별 문제점·한계, §9는 재생성 방법과 발표 활용이다.")
    w("  - §10은 발표 예시 영상 `-QuCz7kxBr8`(농구) 한 건의 심층 자료다: 사전 구축 메모리(캡션 계층·OpenIE·그래프·semantic·visual)의 실제 내용, 캡션·임베딩 모델이 받은 프레임 그림, 섹션별 모든 모듈의 입력·출력 원문과 검색 내부 과정(CPU 재현).")
    w(f"- **대상**: `{rel(RUN)}/<영상>__c0_written__r1/` 3건. 2026-10-25 실행, 커밋 `baf08d8` 시점 코드. 2026-10-26 변경(영상 끝 근거 txt0, 반복 경고 기준, 결말 검사 오탐 수정)은 들어 있지 않고 GPU 확인 전이다.")
    w("- **만든 방법** (재생성 가능, GPU 불필요, LLM 재호출 없음)")
    w("  - 사실 부분: `analysis/build_running_example_combined.py`가 기록 파일에서 직접 생성했다.")
    w("    - Deep-Reporter 세션 로그(planner·query·writer 프롬프트와 출력 원문)")
    w("    - `report.json`·`validation.json`·`report.md`")
    w("    - LLM 서버·검색 서비스 로그")
    w("    - WorldMM 캡션·semantic·visual 파일, HippoRAG 캐시, Video-MME 메타, 영상 파일")
    w("  - 생성할 때 자동으로 확인한 것")
    w("    - 후처리기를 `report.json`에 다시 돌린 결과가 `report.md`와 글자 단위로 같다.")
    w("    - 로그의 LLM 호출 수가 1 + 3 × 섹션 수, 검색 요청 수가 섹션 수 × 2다.")
    w("    - 세 실행의 설정값(§2.2 표)이 같다.")
    w("  - `> 관찰` 블록과 §8: `analysis/running_example_observations.py`에 있다. 근거·캡션·로그·코드와 대조해 사람이 썼다.")
    w("- **표시**: [확인] 코드·데이터로 확인 / [대조] 근거·캡션과 직접 비교 / [측정] 계산값 / [부분 확인] 존재는 확인했으나 영향 정도는 미측정 / [가설] 근거 부족·실험 없음.")
    w(f"- **원문 위치**: 전체 프롬프트·근거 원문은 `internal/inspect/{os.path.basename(RUN)}/<보고서>/`(`analysis/export_stages.py`)에 있다. 영상별 분리본(이 문서 이전 판)은 `backups/running_example_split_20261102/`에 보관했고 `analysis/build_running_example.py`로 다시 만들 수 있다.")
    w("- **주의**")
    w("  - 세 보고서는 각 영상의 r1 한 건이다. 생성이 샘플링(temperature 0.7, seed 없음)이라 같은 조건의 r2·r3은 outline부터 다르다(`SELF_CONSISTENCY_ANALYSIS.md`, `REPORT_TEXT_REVIEW.md`).")
    w("  - \"실제 장면\"은 WorldMM 캡션 기준이다. 영상을 직접 보고 확인하지는 않았다.")
    w("")
    # ================================================================== 1
    w("## 1. 한눈에")
    w("")
    w("### 1.1 파이프라인")
    w("")
    w("```")
    w("[2 입력]      영상 + 질의")
    w("[3 오프라인]  WorldMM 캡션 4단위 + semantic triple + visual 임베딩 → HippoRAG 그래프 4개 (사전 인덱싱)")
    w("[4 준비]      사전 확인 → 영상 개요(10min 캡션 전부) + 영상 끝 시각 → 템플릿 교체 + C0")
    w("[5 planner]   LLM 1회 → outline (섹션 6개)")
    w("[6 섹션 × 6]  query 생성(LLM) → 검색(text: 그래프 검색 → RRF → L1 필터(LLM) + semantic / image: VLM2Vec)")
    w("              → writer(LLM) → 다음 섹션 맥락(C0)")
    w("[7 후처리]    반복 문장 제거 → 결말·시작 검사 → 인용 → References·그림 → 규칙 근거 검사 → 검증")
    w("```")
    w("")
    w("- 보고서 1건의 LLM 호출 = planner 1 + 섹션마다(query 1 + L1 필터 1 + writer 1) = 19회(섹션 6개).")
    w("")
    w("### 1.2 영상 3개 비교 (이 문서의 값)")
    w("")
    w("| 단계 | 항목 | " + " | ".join(f"`{v}`" for v in VIDEOS) + " |")
    w("|---|---|---|---|---|")
    row = lambda stage, item, vals: w(f"| {stage} | {item} | " + " | ".join(vals) + " |")
    row("입력", "내용 (Video-MME 분류)", [f"{SHORT[v]} ({C[v]['vm'][0]['domain']} / {C[v]['vm'][0]['sub_category']})" for v in VIDEOS])
    row("", "길이 (10sec 캡션 끝)", [hms_s(C[v]["end_sec"]) for v in VIDEOS])
    row("오프라인 메모리", "캡션 수 10sec/30sec/3min/10min", ["/".join(str(len(C[v]["caps"][g])) for g in GRANS) for v in VIDEOS])
    trunc = {v: sum(ntok(e["text"]) >= 2048 for e in C[v]["caps"]["10min"]) for v in VIDEOS}
    row("", "2,048토큰에서 잘린 10min 개요 블록", [(f"**{trunc[v]}/{len(C[v]['caps']['10min'])}**" if trunc[v] else f"0/{len(C[v]['caps']['10min'])}") for v in VIDEOS])
    row("planner", "프롬프트 / 출력 토큰", [f"{int(C[v]['llm'][0].group(2)):,} / {C[v]['llm'][0].group(3)}" for v in VIDEOS])
    def ranges(v):
        k = sum(bool(re.findall(r"\d\d:\d\d:\d\d\s*[-–]\s*\d\d:\d\d:\d\d", s["section_description"])) for s in C[v]["outline"])
        return "없음" if k == 0 else f"{k}개 섹션에 표기"
    row("", "섹션 설명의 시간 범위", [ranges(v) for v in VIDEOS])
    def rng(v, k):
        xs = [int(C[v]["llm"][k + 3 * j].group(2 if k == 2 else 3)) for j in range(C[v]["n"])]
        return f"{min(xs):,}–{max(xs):,}"
    row("검색", "L1 필터 프롬프트 토큰 (6회)", [rng(v, 2) for v in VIDEOS])
    def wout(v):
        xs = [(int(C[v]["llm"][3 + 3 * j].group(3)), C[v]["llm"][3 + 3 * j].group(4)) for j in range(C[v]["n"])]
        s_ = f"{min(x for x, _ in xs):,}–{max(x for x, _ in xs):,}"
        return s_ + (" (**상한에서 끊김 1회**)" if any(f == "length" for _, f in xs) else "")
    row("writer", "출력 토큰 (6회)", [wout(v) for v in VIDEOS])
    row("결과", "생성 시간", [f"{C[v]['vj']['timings']['generation_sec']}초" for v in VIDEOS])
    row("", "References / 그림", [f"{len(C[v]['grounded']['references'])} / {len(C[v]['grounded']['figures'])}" for v in VIDEOS])
    row("", "규칙 검사 unsupported / miscited / uncited", [f"{C[v]['vj']['grounding_stats']['unsupported']} / {C[v]['vj']['grounding_stats']['miscited']} / {C[v]['vj']['grounding_stats']['uncited_claims']}" for v in VIDEOS])
    sc = json.load(open(os.path.join(RF, "results", "self_consistency_20261026.json")))
    row("", "다룬 3분 구간 (`self_consistency_20261026.json`)", [f"{sc[v]['coverage']['windows_3min']['per_run'][0]}/{sc[v]['coverage']['windows_3min']['total']}" for v in VIDEOS])
    row("", "결말 서술 (캡션 대조, §8)", ["맞음", "맞음(인용 없음)", "틀림"])
    row("", "검증 상태", [C[v]["vj"]["status"] for v in VIDEOS])
    w("")

    # ================================================================== 2
    w("## 2. 입력")
    w("")
    w("### 2.1 영상 파일과 Video-MME 메타")
    w("")
    w("| 영상 | 파일 | 크기 | 해상도 / fps | 프레임 수 → 길이 | Video-MME domain / sub_category / duration | URL |")
    w("|---|---|---|---|---|---|---|")
    for v in VIDEOS:
        c = C[v]
        w(f"| `{v}` | `{os.path.relpath(c['vpath'], os.path.dirname(RF))}` | {os.path.getsize(c['vpath']):,} bytes | {c['shape'][1]}×{c['shape'][0]} / {c['fps']:.3f} | {c['nfr']:,} → {c['nfr'] / c['fps']:,.1f}초 (10sec 캡션 끝 {hms_s(c['end_sec'])}) | {c['vm'][0]['domain']} / {c['vm'][0]['sub_category']} / `{c['vm'][0]['duration']}` | {c['vm'][0]['url']} |")
    w("- 보고서 생성 단계에서 영상 파일을 직접 읽는 곳은 image 검색의 프레임 추출뿐이다(코드: `extract_center_frame`).")
    w("- 영상마다 Video-MME QA가 3문항 있다(보고서 생성에는 쓰지 않음).")
    for v in VIDEOS:
        w(f"  - `{v}`: " + " / ".join(f"{q['question']} (정답 {q['answer']})" for q in C[v]["vm"]))
    w("")
    w("### 2.2 질의와 설정 (세 실행 공통)")
    w("")
    w(f"- **질의(overall_query)**: `{C[VIDEOS[0]]['rj']['query']}` — 세 영상 모두 같음{' (확인)' if len({C[v]['rj']['query'] for v in VIDEOS}) == 1 else ''}")
    w(f"- **checklist**: `{C[VIDEOS[0]]['rj']['checklist']}`")
    w("- **설정** (각 실행의 `config_<보고서>.yaml`. 아래 값은 세 실행이 같음을 생성 시 확인했다. 실행마다 다른 것은 포트·로그·프레임 폴더뿐이다)")
    w("")
    w("| 키 | 값 |")
    w("|---|---|")
    for k, f in SETTING_KEYS:
        w(f"| `{k}` | `{f(C[VIDEOS[0]]['cfg'])}` |")
    w("")
    w("- **생성 방식**: Deep-Reporter와 서버가 temperature를 보내지 않아 모델 기본값(do_sample, temperature 0.7, top_p 0.8, top_k 20)으로 샘플링한다. seed 없음(`SELF_CONSISTENCY_CAUSES.md` §1).")
    w("- **실행 위치**")
    w("")
    w("| 영상 | 묶음 (GPU) | 세션 | 시작 – 끝 (UTC) |")
    w("|---|---|---|---|")
    for v in VIDEOS:
        c = C[v]
        w(f"| `{v}` | {c['stack']} (GPU {c['gpu']}) | `{c['rj']['session_id']}` | {c['t0']} – {c['t1']} |")
    w("")

    # ================================================================== 3
    w("## 3. 오프라인 메모리 (WorldMM 전처리 + 사전 인덱싱, 보고서 생성 전에 만들어 둠)")
    w("")
    w("### 3.1 캡션 4단위")
    w("")
    how = {"10sec": "프레임 + Whisper 자막 → VLM 캡션", "30sec": "10sec 캡션 묶음을 LLM 요약(L1 프롬프트)",
           "3min": "30sec 요약 묶음을 LLM 요약(L2, ≤300단어 지시)", "10min": "3min 요약 묶음을 LLM 요약(L3, ≤1500단어 지시, 출력 최대 2,048토큰)"}
    w("| 단위 | 만드는 방법 (WorldMM) | " + " | ".join(f"`{v}` 항목 수 · 단어 평균/최대" for v in VIDEOS) + " |")
    w("|---|---|---|---|---|")
    for g in GRANS:
        cellv = []
        for v in VIDEOS:
            ws = [len(str(e["text"]).split()) for e in C[v]["caps"][g]]
            cellv.append(f"{len(ws)} · {sum(ws) / len(ws):.0f}/{max(ws)}")
        w(f"| {g} | {how[g]} | " + " | ".join(cellv) + " |")
    w("- 상위 단위는 바로 아래 단위의 텍스트만 **시각 표기 없이** 이어 붙여(`\"All descriptions: …\"`) 요약한다(WorldMM `gen_multiscale.py`). 그래서 30sec·3min·10min 캡션 안에는 장면별 시각이 없다. [확인]")
    w("")
    w("### 3.2 캡션 계층 예시: 10sec 캡션 하나가 상위 요약으로 올라가는 모습")
    w("")
    w("원문 그대로이며, 길면 앞 600자만 싣는다. 10min은 WorldMM 규칙상 그 3min 캡션이 묶인 블록이다(§3.3).")
    w("")
    for v in VIDEOS:
        caps = C[v]["caps"]
        ex = EXAMPLE_10SEC[v]
        t_ex = sec(ex)
        e10 = next(e for e in caps["10sec"] if str(e["start_time"]).zfill(8) == ex)
        cont = lambda g: next(e for e in caps[g] if sec(e["start_time"]) <= t_ex < sec(e["end_time"]))
        e30, e3m = cont("30sec"), cont("3min")
        blk = next((e for e, (_, items) in zip(caps["10min"], windows_10min(caps["3min"])) if any(i is e3m for i in items)), None)
        C[v]["e10"] = e10
        w(f"**{tt(v)} — 10sec {G.hms_from_time_str(ex)}**")
        w("")
        w("| 단위 | 구간 | 텍스트 |")
        w("|---|---|---|")
        w(f"| 10sec | {G.hms_from_time_str(e10['start_time'])}–{G.hms_from_time_str(e10['end_time'])} | {cell(cut(e10['text'], 600))} |")
        w(f"| 30sec | {G.hms_from_time_str(e30['start_time'])}–{G.hms_from_time_str(e30['end_time'])} | {cell(cut(e30['text'], 600))} |")
        w(f"| 3min | {G.hms_from_time_str(e3m['start_time'])}–{G.hms_from_time_str(e3m['end_time'])} | {cell(cut(e3m['text'], 600))} |")
        if blk is not None:
            w(f"| 10min | 라벨 {G.hms_from_time_str(blk['start_time'])}–{G.hms_from_time_str(blk['end_time'])} | {cell(cut(blk['text'], 600))} |")
        w("")
    w("### 3.3 10min 캡션 = planner가 보는 영상 개요")
    w("")
    w("- 라벨은 `[시작, 시작+10분)`이다. 그러나 WorldMM은 시작 시각이 창 안인 3min 캡션을 그 창에 넣으므로 실제 내용 구간이 라벨과 다를 수 있다(두 번째 열). [확인]")
    w("- 2,048토큰에 도달한 블록은 전처리 출력 상한에서 잘린 것이다(요약이 시간순으로 진행되므로 창의 뒷부분이 빠진다).")
    w("")
    for v in VIDEOS:
        caps = C[v]["caps"]
        w(f"**{tt(v)}**")
        w("")
        w("| 블록 라벨 | 실제로 묶인 3min 캡션 (시작) → 내용 구간 | 토큰 | 2,048토큰 상한 도달 | 마지막 120자 |")
        w("|---|---|---|---|---|")
        for e, (_, items) in zip(caps["10min"], windows_10min(caps["3min"])):
            tk = ntok(e["text"])
            span = f"{', '.join(G.hms_from_time_str(i['start_time'])[3:] for i in items)} → {G.hms_from_time_str(items[0]['start_time'])}–{hms_s(min(sec(items[-1]['end_time']), C[v]['end_sec']))}"
            w(f"| {G.hms_from_time_str(e['start_time'])}–{G.hms_from_time_str(e['end_time'])} | {span} | {tk:,} | {'**예**' if tk >= 2048 else '아니오'} | {cell(cut(e['text'][-120:], 120))} |")
        w("")
    w(f"### 3.4 HippoRAG 그래프 (단위마다 1개, `{os.path.relpath(EPI, os.path.dirname(RF))}/<영상>/episodic_memory/<단위>/`)")
    w("")
    w("- 그래프 구성: 캡션 1개 = passage 노드 1개. 캡션의 OpenIE triple에서 주어·목적어가 entity 노드가 된다. 엣지는 세 종류다: fact(entity–entity, 가중치 = 횟수), passage–entity(1.0), synonym(entity 임베딩 유사도 ≥ 0.8).")
    w("- 임베딩은 Qwen3-Embedding-4B(instruction 없음, 정규화)로 만든다(`REPORT_PIPELINE.md` ④-2(b-0)).")
    w("- 엣지 수는 igraph 엣지 수 그대로다(fact 엣지는 두 방향이 각각 들어 있음). 종류는 passage 노드 포함 여부와 가중치가 정수인지로 나눴다.")
    w("")
    w("| 영상 | 단위 | passage(캡션) | entity | fact(triple) | fact 엣지 | synonym 엣지 | passage–entity 엣지 |")
    w("|---|---|---|---|---|---|---|---|")
    for v in VIDEOS:
        base = os.path.join(EPI, v, "episodic_memory")
        C[v]["base"] = base
        for g in GRANS:
            d_ = glob.glob(f"{base}/{g}/qwen3vl-8b_*")[0]
            Gr = pickle.load(open(f"{d_}/graph.pickle", "rb"))
            names = Gr.vs["name"]
            kinds = collections.Counter()
            for e, wt in zip(Gr.es, Gr.es["weight"]):
                if names[e.source].startswith("chunk") or names[e.target].startswith("chunk"):
                    kinds["pe"] += 1
                elif float(wt).is_integer() and wt >= 1:
                    kinds["f"] += 1
                else:
                    kinds["s"] += 1
            cnt = lambda sub: len(pd.read_parquet(glob.glob(f"{d_}/{sub}/*.parquet")[0]))
            w(f"| `{v}` | {g} | {cnt('chunk_embeddings'):,} | {cnt('entity_embeddings'):,} | {cnt('fact_embeddings'):,} | {kinds['f']:,} | {kinds['s']:,} | {kinds['pe']:,} |")
    w("")
    w("**OpenIE 예: §3.2의 10sec 캡션이 그래프에 들어간 모습** (10sec OpenIE 결과 원문)")
    w("")
    for v in VIDEOS:
        oi = json.load(open(glob.glob(f"{C[v]['base']}/10sec/openie_results_ner_*.json")[0]))["docs"]
        doc = next((d_ for d_ in oi if d_["passage"].strip() == str(C[v]["e10"]["text"]).strip()), None)
        assert doc is not None, v
        ent0 = str(doc["extracted_triples"][0][0])
        w(f"- {tt(v)} 10sec {G.hms_from_time_str(EXAMPLE_10SEC[v])}")
        w(f"  - NER(개체): " + ", ".join(f"`{x}`" for x in doc["extracted_entities"]))
        w(f"  - triple {len(doc['extracted_triples'])}개: " + "; ".join(f"`({', '.join(map(str, t))})`" for t in doc["extracted_triples"]))
        w(f"  - entity 정규화 예(HippoRAG `text_processing`: 소문자화, 영문·숫자·공백 외 문자를 공백으로): `{ent0}` → `{re.sub('[^A-Za-z0-9 ]', ' ', ent0.lower()).strip()}`")
    w("")
    w("### 3.5 semantic triple과 visual 임베딩")
    w("")
    w("| 영상 | semantic 묶음 (검색에 쓰는 마지막 것) | triple / 개체 | 연결이 많은 개체 | triple 예 | visual 임베딩 (10sec 구간마다) |")
    w("|---|---|---|---|---|---|")
    for v in VIDEOS:
        sem = json.load(open(f"{META}/semantic_memory/{v}/semantic_consolidation_results_qwen3vl-8b.json"))
        lk = sorted(sem.keys())[-1]
        tr = sem[lk]["consolidated_semantic_triples"]
        deg = collections.Counter()
        for s_, _, o_ in tr:
            deg[s_] += 1
            deg[o_] += 1
        vis = pickle.load(open(f"{META}/visual_memory/{v}/visual_embeddings.pkl", "rb"))
        first = next(iter(vis.values()))
        w(f"| `{v}` | `{lk}` | {len(tr)} / {len(deg)} | " + ", ".join(f"`{e}`({c_})" for e, c_ in deg.most_common(5)) + " | " + cell("; ".join(f"`({s_}, {p_}, {o_})`" for s_, p_, o_ in tr[:3])) + f" | {len(vis)}개, 차원 {getattr(first, 'shape', ['?'])[-1]} |")
    w("- semantic triple에는 시간 정보가 없다. visual 임베딩은 VLM2Vec-V2로 만들었고, 50개 영상 전처리 설정은 구간당 10프레임, 최대 360×420픽셀이다(`process_one_video.sh --num-frames 10`).")
    w("")

    # ================================================================== 4
    w("## 4. 실행 준비 (`run_report.py`, LLM 0회)")
    w("")
    w("| 영상 | 사전 확인 | 영상 끝 시각 (10sec 마지막 `end_time`) | 영상 개요 | C0 |")
    w("|---|---|---|---|---|")
    for v in VIDEOS:
        c = C[v]
        w(f"| `{v}` | {c['vj']['timings']['preflight_sec']}초 | `{c['vj']['video_end']}` | 10min 캡션 {len(c['caps']['10min'])}개 | `{c['vj']['previous_sections_context']}` |")
    w("- 사전 확인: LLM·검색 서비스 health, 영상 불러오기, 템플릿 계약.")
    w("- 영상 끝 시각은 writer 규칙 7과 결말·시작 검사에 들어간다.")
    w("- 영상 개요는 10min 캡션을 `[HH:MM:SS-HH:MM:SS] 텍스트`로 이어 붙여 planner 템플릿의 `<<VIDEO_OVERVIEW>>` 자리에 넣는다.")
    w("- 템플릿 교체: planner·query·writer 프롬프트를 videomme 템플릿으로 실행 중에만 바꾼다. C0로 다음 섹션 맥락 함수를 바꾼다.")
    w("")

    # ================================================================== 5
    w("## 5. planner: outline 만들기 (LLM 1회)")
    w("")
    w("### 5.1 입력 (프롬프트 구성)")
    w("")
    w("| 영상 | 역할·질의·checklist | 영상 개요 (10min 캡션 전부) | 규칙·출력 형식 | 합계 | 서버 로그 프롬프트 토큰 |")
    w("|---|---|---|---|---|---|")
    for v in VIDEOS:
        pin = C[v]["calls"][0]["input_messages"][0]["content"]
        i_ov, i_task = pin.find("**Video overview**"), pin.find("**Task:**")
        w(f"| `{v}` | {i_ov:,}자 | {i_task - i_ov:,}자 ({len(C[v]['caps']['10min'])}개) | {len(pin) - i_task:,}자 | {len(pin):,}자 | {int(C[v]['llm'][0].group(2)):,} |")
    w(f"- 규칙: 섹션 3–{C[VIDEOS[0]]['cfg']['report']['max_sections']}개, 영상 근거만, 시간순, 설명 2–4문장·대략의 시간 범위, checklist 3–5개, 마지막은 `Conclusion:`.")
    w("- 메시지는 user 1개다(system 없음). 영상 프레임·세밀한 캡션·semantic은 들어가지 않는다. [확인]")
    w("- 프롬프트 전문은 `internal/inspect/…/<보고서>/01_planner_prompt.md`에 있다.")
    w("")
    w("### 5.2 출력 (outline 전문)")
    w("")
    for v in VIDEOS:
        l0 = C[v]["llm"][0]
        w(f"**{tt(v)}** — 출력 {l0.group(3)}토큰, `{l0.group(4)}`, {l0.group(5)}초. JSON 파싱 성공(fallback 없음).")
        w("")
        w("| 섹션 | section_description | sectional_checklist | 설명 속 시간 범위 |")
        w("|---|---|---|---|")
        for i, s in enumerate(C[v]["outline"], 1):
            rngs = re.findall(r"\d\d:\d\d:\d\d\s*[-–]\s*\d\d:\d\d:\d\d", s["section_description"])
            w(f"| S{i} | {cell(s['section_description'])} | {cell(' / '.join(s['sectional_checklist']))} | {', '.join(rngs) or '없음'} |")
        w("")
    w("### 5.3 관찰")
    w("")
    for v in VIDEOS:
        w(f"**{tt(v)}**")
        w("")
        w(obs(v, "planner"))
        w("")

    # ================================================================== 6
    w("## 6. 섹션별 처리")
    w("")
    w("### 6.0 공통 처리 (모든 섹션)")
    w("")
    w("| 단계 | 하는 일 | LLM |")
    w("|---|---|---|")
    w("| (a) query 생성 | 질의, checklist, **앞 섹션 요약(C0)**, 섹션 설명·checklist를 넣어 text query 2–3개(키워드형)와 image query 1–2개(장면 묘사)를 JSON으로 받음 | 1회 |")
    w("| (b) 검색 | text: query × 4단위 HippoRAG 그래프 검색(단위별 후보 3/3/2/1) → RRF 병합 → **L1 필터**(LLM이 episodic 8개 선택) + semantic 4개. image: VLM2Vec 텍스트→비디오 유사도 상위 3구간 → 구간 중앙 프레임 + 같은 시작 시각의 10sec 캡션 | 1회(L1 필터) |")
    w("| (c) writer | 섹션 위치, 설명·checklist, C0 요약 + 직전 섹션 끝 3조각, 근거(text `content` 전문 txt1–12, image는 캡션 문자열만 img1–3), 규칙(Grounding 1–7, Citation 1–4, 위치별, 결론, 형식) → 섹션 본문 | 1회 |")
    w("| (d) 후처리 | 반복 문장 제거, 결말·시작 서술 검사, 인용 → 전역 번호·그림, 규칙 근거 검사, 이미지-텍스트 시간 차 기록 | 0회 |")
    w("- (a)와 (c)에 들어가는 앞 섹션 요약(C0)은 직전 섹션들의 writer 출력으로 만든다. 같은 시점의 같은 요약이 두 단계에 들어간다.")
    w("- L1 필터의 후보 목록과 응답 원문은 기록되지 않는다(토큰·시간만 서버 로그에 있음).")
    w("- 근거 표의 \"전역 번호\"는 최종 `report.md`의 References 번호이고, 그림은 Figure 번호다. 인용 여부는 반복 제거 후 본문 기준이다.")
    w("")
    for v in VIDEOS:
        c = C[v]
        vn = VNUM[v]
        w(f"### 6.{vn} {tt(v)}")
        w("")
        for i, s in enumerate(c["outline"], 1):
            q, f_, wl = c["llm"][1 + 3 * (i - 1)], c["llm"][2 + 3 * (i - 1)], c["llm"][3 + 3 * (i - 1)]
            qc, wc = c["q_calls"][i - 1], c["w_calls"][i - 1]
            st, si = c["svc"][2 * (i - 1)], c["svc"][2 * (i - 1) + 1]
            texts, imgs = s["retrieved_texts"] or [], s["retrieved_images"] or []
            content = s["content"] or ""
            ct, ci = set(cited_txt(content)), set(cited_img(content))
            title = next((ln.lstrip("#").strip() for ln in content.split("\n") if ln.startswith("#")), "")
            w(f"#### 6.{vn}.{i} 섹션 {i}: {title}")
            w("")
            w(f"- planner 설명: {s['section_description']}")
            w("- checklist: " + " / ".join(s["sectional_checklist"]))
            w("")
            qin = qc["input_messages"][0]["content"]
            m = re.search(r"\*\*Previous sections \(summary\):\*\*\n([\s\S]*?)\n\n\*\*Current section:\*\*", qin)
            assert m, (v, i)
            w(f"**(a) query 생성** — 프롬프트 {q.group(2)}토큰, 출력 {q.group(3)}토큰, `{q.group(4)}`, {q.group(5)}초")
            w("")
            w("- 입력 중 앞 섹션 요약(C0):")
            w("")
            w(fence(m.group(1).strip()))
            w("")
            w("- 출력(파싱 결과):")
            for k, x in enumerate(s["text_queries"] or [], 1):
                w(f"  - text {k}: `{x}`")
            for k, x in enumerate(s["image_queries"] or [], 1):
                w(f"  - image {k}: `{x}`")
            w("")
            w(f"**(b) 검색** — text 요청 `{st.group(3)}`; image 요청 `{si.group(3)}`")
            w("")
            w(f"- text query {len(s['text_queries'])}개 × 4단위 그래프 검색 → RRF → L1 필터(프롬프트 {f_.group(2)}토큰, 출력 {f_.group(3)}토큰, {f_.group(5)}초) → episodic 8개 + semantic 4개. image query {len(s['image_queries'])}개 → 프레임 {len(imgs)}장.")
            w("")
            w("| 근거 | 인용 | 전역 번호 | 출처 | 단위 | 시간 | 순위 | 내용 (앞 170자) |")
            w("|---|---|---|---|---|---|---|---|")
            for k, t in enumerate(texts, 1):
                tm = (f"{G.hms_from_time_str(t['start_time'])}–{G.hms_from_time_str(t['end_time'])}" if t.get("start_time") else "없음")
                w(f"| txt{k} | {'✓' if k in ct else ''} | {('[' + str(c['uid2ref'][t['uid']]) + ']') if k in ct and t['uid'] in c['uid2ref'] else ''} | {t['source'].replace('worldmm-', '')} | {t.get('granularity') or '—'} | {tm} | {t.get('rank')} | {cell(cut(G.strip_label(t['content']), 170))} |")
            for k, m_ in enumerate(imgs, 1):
                fig = c["uid2fig"].get(m_["uid"]) if k in ci else None
                w(f"| img{k} | {'✓' if k in ci else ''} | {('Figure ' + str(fig)) if fig else ''} | visual | 프레임 {G.hms(m_['frame_sec'])} | {G.hms_from_time_str(m_['start_time'])}–{G.hms_from_time_str(m_['end_time'])} | {m_.get('rank')} | {cell(cut(G.strip_label(m_['caption']), 170))} |")
            w("")
            w("- 프레임 파일: " + ", ".join(f"img{k} `{rel(m_['img_path'])}`" for k, m_ in enumerate(imgs, 1)))
            w("")
            win = wc["input_messages"][0]["content"]
            w(f"**(c) writer** — 프롬프트 {wl.group(2)}토큰({len(win):,}자), 출력 {wl.group(3)}토큰, `{wl.group(4)}`, {wl.group(5)}초" + (" — **서버 상한 3,072토큰에서 끊김**" if wl.group(4) == "length" else ""))
            w("")
            w(f"- 입력: `Section {i}/{c['n']}`, 위 C0 요약 + 직전 섹션 끝, 근거 text {len(texts)}개 + image {len(imgs)}개(캡션). 전문: `internal/inspect/{os.path.basename(RUN)}/{c['job']}/s{i:02d}/4_writer_prompt.md`")
            w("")
            w(details(f"writer 출력 원문 ({len(wc['output_content'].split())}단어, 후처리 전)", fence(wc["output_content"])))
            w("")
            vj = c["vj"]
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
            w("- 결말·시작 서술 검사: " + ("; ".join(f"**{b['status']}** — {cut(b['sentence'], 160)}" + (f" (인용 근거 끝 {b['latest_cited_end']})" if b.get('latest_cited_end') else "") for b in bnd) if bnd else "해당 없음"))
            al = vs["image_time_alignment"]
            w("- 이미지-텍스트 시간 차: " + ("; ".join(f"{x['img']} 프레임 {x['frame']} → 같은 단락 텍스트와 {x['gap_to_local_text_sec']}초, 섹션 텍스트와 {x['gap_to_section_text_sec']}초" for x in al) if al else "인용 이미지 없음"))
            w("")
            w(details("최종 본문 (report.md의 이 섹션 그대로)", fence(c["grounded"]["section_bodies"][i - 1])))
            w("")
            w(obs(v, f"s{i}"))
            w("")

    # ================================================================== 7
    w("## 7. 최종 산출물과 검증")
    w("")
    w("| 영상 | report.md (References / 그림) | report_raw.md (반복 제거 전) | 섹션별 단어 수 (반복 제거 후, 인용 표기 포함) | 상태 / 오류 |")
    w("|---|---|---|---|---|")
    for v in VIDEOS:
        c = C[v]
        words = [len((s["content"] or "").split()) for s in c["outline"]]
        w(f"| `{v}` | {len(c['grounded']['references'])} / {len(c['grounded']['figures'])} | {len(open(os.path.join(c['rdir'], 'report_raw.md')).read().split()):,}단어 | " + ", ".join(f"S{i} {x}" for i, x in enumerate(words, 1)) + f" (합 {sum(words):,}) | `{c['vj']['status']}` / {len(c['vj']['errors'])} |")
    w(f"- 파일 위치: `{rel(RUN)}/<보고서>/` 아래 `report.md`(헤더 + 섹션 + References), `report_raw.md`, `report.json`(설명·checklist·검색어·근거 전체·본문), `validation.json`(상태·경고·시간·반복·결말 검사·규칙 검사·이미지 시간 차), `frames/`(인용 프레임).")
    w("")
    for v in VIDEOS:
        c = C[v]
        vj = c["vj"]
        w(f"### 7.{VNUM[v]} {tt(v)}")
        w("")
        w(f"- 인용 통계: `{json.dumps(vj['citation_stats'])}`")
        w(f"- 규칙 검사 합계: `{json.dumps(vj['grounding_stats'])}`")
        w(f"- 이미지-텍스트 시간 차 요약: `{json.dumps(vj['image_time_alignment'])}`")
        w("- 경고:")
        for x in vj["warnings"]:
            w(f"  - {x}")
        w("")
        w("References 앞 5개:")
        w("")
        w(fence("\n".join(r["line"] for r in c["grounded"]["references"][:5])))
        w("")
        w("LLM 호출 (서버 로그, 호출 순서):")
        w("")
        w("| 호출 | 섹션 | 프롬프트 토큰 | 출력 토큰 | 종료 | 초 |")
        w("|---|---|---|---|---|---|")
        l0 = c["llm"][0]
        w(f"| planner | — | {l0.group(2)} | {l0.group(3)} | {l0.group(4)} | {l0.group(5)} |")
        for i in range(1, c["n"] + 1):
            for name, m in (("query", c["llm"][1 + 3 * (i - 1)]), ("L1 필터", c["llm"][2 + 3 * (i - 1)]), ("writer", c["llm"][3 + 3 * (i - 1)])):
                w(f"| {name} | {i} | {m.group(2)} | {m.group(3)} | {m.group(4)} | {m.group(5)} |")
        tsum = lambda k: round(sum(float(c["llm"][k + 3 * j].group(5)) for j in range(c["n"])), 1)
        w(f"- 합계: planner {l0.group(5)}초, query {tsum(1)}초, L1 필터 {tsum(2)}초, writer {tsum(3)}초 / 생성 {vj['timings']['generation_sec']}초. 후처리 {vj['timings']['postprocess_sec']}초.")
        w("")

    # ================================================================== 8
    w("## 8. 단계별 문제점·한계")
    w("")
    for v in VIDEOS:
        summ = OBS[v]["summary"]
        body = summ.split("\n", 1)[1].strip()            # drop the per-video "## 7." heading
        w(f"### 8.{VNUM[v]} {tt(v)}")
        w("")
        w(body)
        w("")
    w("### 8.4 세 영상 공통")
    w("")
    w("세 영상의 §8.1–§8.3과 §5.3·§6 관찰에서 반복해 확인된 것만 모았다.")
    w("")
    w("| 단계 | 공통으로 확인된 동작·문제 | 사례 위치 | 표시 |")
    w("|---|---|---|---|")
    w("| 입력 자료 | 10min 개요 블록의 라벨이 실제 내용 구간과 다르다(0–12분, 12–21분 등). 30sec·3min 요약에 구간 내부의 끝·시작 표현과 해석 표현이 있다. 캡션 오류·불일치가 상위 요약으로 전파된다 | §3.3, §6.1.4, §6.2.3, §6.3.2 | [확인] |")
    w("| 입력 자료 | 10min 개요 블록이 2,048토큰에서 잘려 개요에 빈 구간이 생긴다(`0RxMZBLeqRI` 0–10·10–20분 블록) | §3.3, §5.3 | [확인] |")
    w("| planner | 개요만 보고 섹션 6개를 정한다. 세 영상 모두 계획되지 않은 구간이 있다. checklist에 개요의 세부·해석·결말을 미리 적는다 | §5.2, §5.3 | [확인] |")
    w("| query 생성 | checklist 문구를 거의 그대로 검색어로 쓴다. 결론 검색어는 앞 섹션 요약을 따라간다 | §6.x (a), §8.1–§8.3 | [확인] |")
    w("| 검색 | 섹션마다 독립 검색이라 같은 근거가 여러 섹션에 들어온다. 이미지는 텍스트 근거와 따로 찾는다. L1 필터의 중간 결과는 기록되지 않는다 | §6.1.1, §6.1.4, §6.2.2 | [확인] |")
    w("| writer | 근거 문장을 옮기고(구간 끝 표현·해석 포함), 다른 근거의 시각을 붙이거나 무관한 근거를 인용한다. 근거가 적으면 같은 주장을 늘리고, checklist 항목을 \"does not show\"로 채운다 | §6.1.3, §6.2.2, §6.2.5, §6.3.3 | [확인]·[대조] |")
    w("| writer | 근거가 적을 때 길이 지시와 해석형 checklist가 반복을 키울 가능성 | §6.2.2 | [가설] |")
    w("| 결론 | 결론도 따로 검색해, 본문에 없던 사실을 넣거나 문장과 맞지 않는 근거를 인용한다. 결말의 정오는 planner가 결말 구간을 계획했는지와 함께 움직였다 | §6.1.6, §6.2.6, §6.3.6 | [확인]·[부분 확인] |")
    w("| 후처리·검증 | 세 보고서 모두 `passed`. 규칙 검사·결말 검사는 경고만 남긴다. 무관한 근거 인용·장면 섞기·덧씌운 서사 같은 의미 수준 오류는 검사 대상이 아니다. 같은 문장 반복만 지운다 | §7, §6.2.5 | [확인] |")
    w("")
    w("이슈별 상세 원인 분석은 `REPORT_TEXT_REVIEW.md`(9건 텍스트 분석), `SELF_CONSISTENCY_CAUSES.md`(실행 간 차이), `MEETING_ISSUES_DECK_PLAN.md`(발표용 이슈·원인 정리)에 있다.")
    w("")

    # ================================================================== 9
    w("## 9. 재생성 방법과 발표 활용")
    w("")
    w("```bash")
    w("cd report_framework")
    w("python -B analysis/build_running_example_combined.py          # 이 문서 (internal/running_example/RUNNING_EXAMPLE.md)")
    w("# (선택) 영상별 분리본: build_running_example.py --video=<vid> 후 running_example_observations.py")
    w("python -B analysis/export_stages.py                         # internal/inspect/: 프롬프트·근거 원문 전체")
    w("# §10의 검색 내부 과정 (CPU 8코어, 약 10분): 결과 results/retrieval_repro_-QuCz7kxBr8_r1.json")
    w("CUDA_VISIBLE_DEVICES= python -B analysis/reproduce_retrieval_cpu.py --video=-QuCz7kxBr8 --work-dir <임시 폴더>")
    w("```")
    w("")
    w("| 보여 줄 것 | 위치 |")
    w("|---|---|")
    w("| 파이프라인 전체와 영상 3개 비교 | §1 |")
    w("| 캡션 4단계가 쌓이는 모습 (10sec 하나 → 30sec → 3min → 10min) | §3.2 |")
    w("| planner가 실제로 보는 개요와 한계(라벨 어긋남, 2,048토큰 잘림) | §3.3 (`0RxMZBLeqRI`가 잘림 사례) |")
    w("| 캡션 하나가 그래프에 들어가는 모습(NER, triple) | §3.4 OpenIE 예 |")
    w("| outline 전문과 planner 관찰 | §5.2, §5.3 |")
    w("| 한 섹션의 query → 근거 15개(인용 여부·전역 번호) → writer 원문 → 최종 본문 | §6.1.1 (`-QuCz7kxBr8` 섹션 1), §6.3.3 (`54k2g9ddy4M` 섹션 3) |")
    w("| 반복 루프와 후처리 (3,072토큰에서 끊김, 1,778 → 927단어) | §6.2.5 |")
    w("| 구간 끝 표현이 결말로 옮겨지는 경로 | §6.1.3, §6.1.4 관찰 |")
    w("| 틀린 결말이 planner checklist에서 오는 경로 | §5.3 (`54k2g9ddy4M`), §6.3.6 |")
    w("| 단계별 문제점·한계 | §8 |")
    w("| 캡션 모델·VLM2Vec이 실제로 받은 프레임, 검색된 프레임 (그림) | §10.2, §10.6, §10.7, 파일 목록 §10.10 |")
    w("| 사전 구축 episodic memory 실제 내용 (캡션 계층 원문, OpenIE, 그래프 이웃) | §10.3, §10.4 |")
    w("| 사전 구축 semantic memory 실제 내용 (추출 실패 11/23, 통합 추이, 최종 153개) | §10.5 |")
    w("| 한 섹션의 query → 그래프 검색 → RRF → L1 필터 → semantic·image → writer → 후처리 전 과정 | §10.9.1–§10.9.6 (그래프 검색·RRF·L1 프롬프트까지 재현이 기록과 맞은 섹션: §10.9.0 표) |")
    w("")

    from build_running_example_deep import render as render_deep
    L += render_deep()
    L = add_toc(L)
    out = os.path.join(RF, "internal", "running_example", "RUNNING_EXAMPLE.md")
    open(out, "w", encoding="utf-8").write("\n".join(L) + "\n")
    print("wrote", out, len("\n".join(L)), "chars")


# ---------------------------------------------------------------------------------------------- table of contents
# Detailed TOC placed right under the title (2026-11-03). Every numbered heading (## N. / ### N.N / #### N.N.N, outside
# code fences) gets an anchor line and exactly one TOC entry, in document order (asserted). Each description is
# checked against its section: the listed `must` strings have to occur in that section's text, and the counts in
# brackets (tables / images / folded originals) are counted from the section body itself.
HEAD_RE = re.compile(r"^(#{2,4}) (\d+(?:\.\d+)*)\.? (.*)$")
VID_SHORT = {"1": ("-QuCz7kxBr8", "농구 가젯 시험"), "2": ("0RxMZBLeqRI", "로마 역사"), "3": ("54k2g9ddy4M", "CBC 뉴스 모음")}
TOC_DESC = {
    "0": ("목적, 대상 보고서 3건(영상별 r1), 만든 방법과 생성 중 자동 확인 항목, 표시 기호([확인]·[대조]·[측정]·[부분 확인]·[가설]), 주의", ["**목적**", "**표시**"]),
    "1": ("파이프라인 전체와 영상 3개 비교", []),
    "1.1": ("단계 흐름도(입력 → 오프라인 메모리 → 준비 → planner → 섹션 × 6 → 후처리), 보고서 1건의 LLM 호출 19회 구성", ["19회"]),
    "1.2": ("단계별 주요 값의 세 영상 비교표: 캡션 수, 잘린 10min 블록, planner·L1·writer 토큰, 생성 시간, References/그림, 규칙 검사, 결말 정오, 검증 상태", ["| 단계 | 항목 |"]),
    "2": ("영상·질의·설정", []),
    "2.1": ("영상 파일 경로·크기·해상도·fps·길이·Video-MME 분류·URL 표, 영상별 Video-MME QA 3문항(보고서 생성에는 안 씀)", ["Video-MME"]),
    "2.2": ("질의 원문, checklist, 실행 설정값 표(세 실행 공통), 샘플링 방식, 실행 위치(GPU·세션·시각) 표", ["**질의(overall_query)**", "**설정**", "**실행 위치**"]),
    "3": ("WorldMM 전처리와 사전 인덱싱으로 미리 만든 메모리(세 영상 비교)", []),
    "3.1": ("캡션 4단위(10sec·30sec·3min·10min)를 만드는 방법과 영상별 항목 수·단어 수", ["| 단위 | 만드는 방법"]),
    "3.2": ("영상별 10sec 캡션 1개가 30sec → 3min → 10min 요약으로 올라가는 원문 비교", ["| 단위 | 구간 | 텍스트 |"]),
    "3.3": ("planner가 보는 10min 개요 블록: 라벨과 실제 구간의 어긋남, 토큰 수, 2,048토큰 잘림 여부", ["2,048토큰 상한 도달"]),
    "3.4": ("영상 × 단위별 HippoRAG 그래프 통계(passage·entity·fact·엣지), §3.2 캡션의 OpenIE(NER·triple) 예", ["**OpenIE 예"]),
    "3.5": ("영상별 semantic triple 수·개체·예와 visual 임베딩 수·차원", ["visual 임베딩"]),
    "4": ("영상별 사전 확인 시간, 영상 끝 시각, 개요 구성, 템플릿 교체·C0", ["영상 끝 시각"]),
    "5": ("outline 만들기(LLM 1회)", []),
    "5.1": ("planner 프롬프트의 부분별 글자 수와 서버 로그 토큰", ["| 영상 | 역할·질의·checklist"]),
    "5.2": ("영상별 outline 전문: 섹션 설명·checklist·설명 속 시간 범위, 출력 토큰·시간", ["| 섹션 | section_description"]),
    "5.3": ("영상별 planner 관찰(섹션 나누기, 다루지 않은 구간, 결말 계획 여부)", ["**관찰 — planner**"]),
    "6": ("섹션마다 query 생성 → 검색 → writer → 후처리 (영상별 섹션 1–6)", []),
    "6.0": ("(a)–(d) 단계가 하는 일과 LLM 호출 수의 공통 표, 표 읽는 법", ["| (a) query 생성"]),
    "6.v": ("{vid} ({short}) 보고서의 섹션 6개", []),
    "6.v.k": ("(a) query 생성과 입력된 앞 섹션 요약(C0) · (b) 검색 요청과 근거 표(txt·img, 인용 여부·References 번호) · (c) writer 입력 설명·출력 원문 · (d) 반복 제거·인용 변환·규칙 검사·결말 검사·이미지 시간 차, 최종 본문 · `> 관찰`",
              ["**(a) query 생성**", "**(b) 검색**", "**(c) writer**", "**(d) 후처리·검사**", "> **관찰"]),
    "7": ("세 보고서의 산출 파일·단어 수·상태 요약표와 파일 위치", ["| 영상 | report.md"]),
    "7.v": ("{vid} ({short}): 인용 통계, 규칙 검사 합계, 이미지-텍스트 시간 차, 경고, References 앞 5개, LLM 호출 19회 표와 시간 합계", ["- 인용 통계:", "References 앞 5개", "LLM 호출 (서버 로그"]),
    "8": ("단계별 문제점·한계(관찰 정리)", []),
    "8.v": ("{vid} ({short})에서 확인된 단계별 동작·문제 표", ["| 단계 | 이 영상에서 확인된 동작·문제"]),
    "8.4": ("세 영상 공통 문제 표(사례 위치 포함)와 관련 문서", ["| 단계 | 공통으로 확인된"]),
    "9": ("이 문서·inspect·§10 검색 재현을 다시 만드는 명령, \"보여 줄 것 → 위치\" 표", ["```bash", "| 보여 줄 것 | 위치 |"]),
    "10": ("농구 영상 보고서 r1의 사전 구축 메모리 실제 내용, 모듈이 받은 프레임 그림, 모듈별 입력·출력 원문", []),
    "10.0": ("§10의 대상·만든 방법·자동 확인 항목·표시 기호", ["**만든 방법**", "**생성 중 자동 확인(assert)한 것**"]),
    "10.1": ("영상 파일·해상도·fps·프레임 수, Whisper 자막, 10초 구간 나누기 표, 자막 앞 12줄 원문", ["자막 앞 12줄"]),
    "10.2": ("캡션 모델(Qwen3-VL-8B) system 프롬프트, 4개 구간 각각의 입력 프레임 10장 그림·프레임 번호·user 메시지 원문·출력 캡션", ["캡션 system 프롬프트 원문", "caption_input_"]),
    "10.3": ("캡션 계층을 묶는 규칙과 단위별 항목 수·단어 수·덮는 개수", ["다시 묶어 본 결과"]),
    "10.3.1": ("00:00:00–00:03:00의 3min 1개, 30sec 6개, 10sec 18개 원문 전체", ["**3min 00:00:00–00:03:00**"]),
    "10.3.2": ("10min 캡션 4개 전문(묶인 3min, 단어·토큰 수)", ["10min 라벨"]),
    "10.3.3": ("3min·30sec·10sec 캡션 전체 목록", ["캡션 13개 전문", "캡션 76개 전문", "캡션 226개 전문"]),
    "10.4": ("NER·triple 추출 프롬프트, OpenIE 통계와 triple 0개 캡션 18개의 원인, 00:00–01:00 캡션별 NER·triple, HippoRAG 그래프 규칙·단위별 통계, `sports dribble specs` 노드의 이웃, synonym 엣지 예",
             ["NER 프롬프트", "**triple이 0개인 캡션 18개**", "**HippoRAG 그래프 구성 규칙**", "synonym 엣지 예"]),
    "10.5": ("semantic 추출 규칙·프롬프트, 23묶음 표(11묶음 실패, 실패 응답 토큰 분석), 한 묶음의 입력→출력 원문, 통합 규칙·프롬프트·추이 표·변경 예, 검색에 쓰는 최종 153개 전체",
             ["**① 추출**", "23묶음 중 11묶음이 0개", "**② 통합**", "**③ 검색에 쓰이는 semantic memory**", "최종 semantic triple 153개 전체"]),
    "10.6": ("visual 임베딩 파일 구조, 구간당 10장 확인(10장·16장 재임베딩 비교), 프레임 범위·크기, 4개 구간의 VLM2Vec 입력 프레임 10장 그림", ["프레임 수 확인", "vlm2vec_input_"]),
    "10.7": ("섹션별 image 근거 18개(구간·중앙 프레임·cosine·인용) 썸네일 표, 최종 보고서 Figure 1–3과 캡션", ["**최종 보고서의 그림"]),
    "10.8": ("planner 서버 로그 값, 프롬프트 원문·출력 원문", ["planner 프롬프트 원문", "planner 출력 원문"]),
    "10.9": ("섹션 1–6마다 모든 모듈의 입력·출력", []),
    "10.9.0": ("검색 재현 방법, 섹션별 일치 판정표(text·semantic·image), 어긋남의 성격과 원인, 일치 판정의 한계", ["| 섹션 | RRF 후보 수", "**일치 판정의 한계**"]),
    "10.9.k": ("", []),
    "10.10": ("PPT용 그림 파일 목록(`internal/running_example/assets/-QuCz7kxBr8/`)", ["| 파일 | 내용 |"]),
}


def _numbered_headings(L):
    out, fence_ = [], None
    for i, l in enumerate(L):
        m = re.match(r"^(`{3,})", l)
        if m:
            fence_ = m.group(1) if fence_ is None else (None if l.strip() == fence_ else fence_)
            continue
        if fence_ is None:
            h = HEAD_RE.match(l)
            if h:
                out.append((i, len(h.group(1)), h.group(2), l.lstrip("#").strip()))
    return out


def _body_counts(lines):
    fence_, tables, imgs = None, 0, 0
    for l in lines:
        m = re.match(r"^(`{3,})", l)
        if m:
            fence_ = m.group(1) if fence_ is None else (None if l.strip() == fence_ else fence_)
            continue
        if fence_ is None:
            tables += l.startswith("|---")
            imgs += len(re.findall(r"!\[[^\]]*\]\([^)]+\)", l))
    det = sum(l.startswith("<details>") for l in lines)
    parts = [f"표 {tables}" if tables else "", f"그림 {imgs}" if imgs else "", f"접힌 원문 {det}" if det else ""]
    parts = [p for p in parts if p]
    return f" 〔{' · '.join(parts)}〕" if parts else ""


def add_toc(L):
    L = "\n".join(L).split("\n")          # elements may hold several lines (fenced blocks): work on real lines
    heads = _numbered_headings(L)
    nums = [h[2] for h in heads]
    assert len(nums) == len(set(nums)), "duplicate section numbers"
    entries = []
    for j, (i, lvl, num, text) in enumerate(heads):
        nxt_same = next((h[0] for h in heads[j + 1:] if h[1] <= lvl), len(L))
        nxt_any = heads[j + 1][0] if j + 1 < len(heads) else len(L)
        block = "\n".join(L[i:nxt_same])
        p = num.split(".")
        if num in TOC_DESC:
            key = num
        elif p[0] in ("6", "7", "8") and len(p) == 2:
            key = f"{p[0]}.v"
        elif p[0] == "6" and len(p) == 3:
            key = "6.v.k"
        elif p[:2] == ["10", "9"] and len(p) == 3:
            key = "10.9.k"
        else:
            raise AssertionError(f"no TOC description for §{num}")
        desc, must = TOC_DESC[key]
        if key in ("6.v", "7.v", "8.v"):
            vid, short = VID_SHORT[p[1]]
            assert vid in text, (num, text)
            desc = desc.format(vid=f"`{vid}`", short=short)
        if key == "10.9.k":
            text_ok = "**③ 그래프 검색 (질의 × 단위)**" in block
            assert text_ok != ("**③·④ 그래프 검색·RRF·L1 필터 — 재현 불가**" in block), num
            sem_ok = "**⑤ semantic 검색** —" in block
            assert sem_ok != ("**⑤ semantic 검색 — 재현 불가**" in block), num
            img_ok = "**⑥ image 검색** —" in block
            assert img_ok != ("**⑥ image 검색 — 재현 불가**" in block), num
            desc = ("① query 프롬프트·출력 원문 · ② 검색 요청과 서비스 로그 · "
                    + ("③ 질의×단위 그래프 검색 결과·fact 상위 5 · ④ RRF 후보 전체와 L1 선택 순위, L1 필터 프롬프트 원문 [재현이 기록과 일치]"
                       if text_ok else "③·④ 검색 내부 과정 **재현 불가**: 기록된 L1 선택 8개·RRF 점수와 어긋난 지점만")
                    + " · ⑤ semantic " + ("질의별·RRF 결과 [재현 일치]" if sem_ok else "기록된 4개만(재현 불가)")
                    + " · ⑥ image " + ("cosine 상위 10 [재현 일치]" if img_ok else "기록된 3개만(재현 불가)")
                    + " · ⑦ writer가 받은 근거 전문 · ⑧ writer 프롬프트·출력 원문 · ⑨ 후처리·인용 번호 대응·최종 본문")
            must = ["**① query 생성**", "**② 검색 요청**", "**⑦ writer가 받은 근거 전문**", "**⑧ writer**", "**⑨ 후처리**"]
        for m_ in must:
            assert m_ in block, (num, m_)
        counts = _body_counts(L[i + 1:nxt_any]) if lvl > 2 else ""
        anchor = "s" + num.replace(".", "-")
        entries.append((lvl, num, text, anchor, desc, counts))
    toc = ["## 목차", "",
           "- 장(##)·절(###)·하위 절(####)을 문서 순서대로 모두 실었다. 제목을 누르면 그 위치로 간다.",
           "- 〔 〕 안의 숫자는 그 절 본문(하위 절 제외)에 있는 표·그림·접힌 원문(`<details>`)의 개수다. 접힌 원문은 눌러야 펼쳐진다.",
           "- §2–§5와 §7은 세 영상을 나란히 비교하고, §6은 영상별로 섹션 6개를 따라간다. §10은 농구 영상(`-QuCz7kxBr8`) 한 건의 심층 자료다.",
           ""]
    for lvl, num, text, anchor, desc, counts in entries:
        ind = "  " * (lvl - 2)
        toc.append(f"{ind}- [{text}](#{anchor}) — {desc}{counts}" if desc else f"{ind}- [{text}](#{anchor}){counts}")
    toc.append("")
    # anchors: one line + blank line right before each numbered heading (outside fences)
    starts = {i: a for (i, _, _, _), (_, _, _, a, _, _) in zip(heads, entries)}
    out = []
    for i, l in enumerate(L):
        if i in starts:
            if out and out[-1].strip():
                out.append("")
            out += [f'<a id="{starts[i]}"></a>', ""]
        out.append(l)
    assert out[0].startswith("# Running example") and out[1] == ""
    out = out[:2] + toc + out[2:]
    # every TOC link has exactly one anchor; every numbered heading is in the TOC once, in order
    links = re.findall(r"\]\(#(s[\d-]+)\)", "\n".join(toc))
    ids = re.findall(r'^<a id="(s[\d-]+)"></a>$', "\n".join(out), re.M)
    assert links == ids == [e[3] for e in entries] and len(set(ids)) == len(ids)
    assert [h[2] for h in _numbered_headings(out)] == nums
    assert {"0", "6.3.6", "9", "10.9.6", "10.10"} <= set(nums), "heading scan incomplete"
    return out


if __name__ == "__main__":
    main()
