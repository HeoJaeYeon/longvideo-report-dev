#!/usr/bin/env python3
"""
Video report generation entry point (report_framework [D]).

  preflight  : overview caption file, LLM endpoint /health (local backend), retrieval service
               /health + POST /videos/<vid>/load (fails early if the episodic cache is incomplete),
               domain-template contract check
  LLM env    : Deep-Reporter reads keys/URLs only from env vars (BaseConfig.from_dict drops them):
               local -> QWEN_BASE_URL / QWEN_API_KEY, openai -> OPENAI_API_KEY (+OPENAI_BASE_URL);
               the routed base URL is verified before generation
  generation : with apply_templates(<domain>, video overview) [+ apply_written_context() when
               report.previous_sections_context=written]: generate_article(with_planner)
  post       : grounding_postprocessor (references, figures, rule-based evidence check with
               "absence" clauses exempted, image-text time alignment recorded)
  validation : Deep-Reporter can return success=True after silent failures, so the result is
               checked (planner/query fallbacks, failure strings, empty evidence, invalid
               citations, missing frames; warnings for the section cap / conclusion rules)
  translation: report.translate_ko -> report_ko.md (report_translator, one LLM call per section;
               skipped when validation has errors; never changes the English report or exit code)

This script loads no model; it needs the running services (GPU):
  local_llm_server.py (or vLLM) and videorag_retriever_service.py.
Outputs (<out_dir>): report.md (grounded), report_raw.md (Deep-Reporter output), report.json,
validation.json, frames/, report_ko.md (if translated). Exit code: 0 passed, 1 validation errors
(outputs still written), 2 preflight / configuration failure.

Usage:
  python run_report.py --config config.yaml --video-id <vid> --query "<report request>" [--checklist "..."]...
"""

import argparse
import json
import logging
import os
import sys
import time
from contextlib import nullcontext
from datetime import datetime
from typing import Any, Dict, List, Optional, Tuple

import requests
import yaml

HERE = os.path.dirname(os.path.abspath(__file__))
if HERE not in sys.path:
    sys.path.insert(0, HERE)
import domain_templates as D  # noqa: E402
import grounding_postprocessor as G  # noqa: E402
import report_translator as RT  # noqa: E402

logger = logging.getLogger("run_report")
FAILURE_MARKERS = G.FAILURE_MARKERS


# ---------------------------------------------------------------------------
# Preflight and LLM routing
# ---------------------------------------------------------------------------

def llm_settings(cfg: Dict[str, Any]) -> Tuple[str, str, Dict[str, str]]:
    """(primary_model, expected_base_url, env_vars) for Deep-Reporter's primary LLM."""
    backend = cfg["llm"]["backend"]
    if backend == "local":
        ep = cfg["llm"]["local"]["endpoint"]
        base_url = f"http://{ep['host']}:{ep['port']}/v1"
        if "qwen" not in ep["model"].lower():
            raise ValueError(f"local model name {ep['model']!r} must contain 'qwen' (Deep-Reporter routes by name)")
        return ep["model"], base_url, {"QWEN_BASE_URL": base_url, "QWEN_API_KEY": str(ep["api_key"])}
    if backend == "openai":
        model = cfg["llm"]["openai"]["endpoint"]["model"]
        if "gpt" not in model.lower():
            raise ValueError(f"openai model name {model!r} must contain 'gpt' (Deep-Reporter routes by name)")
        if not os.environ.get("OPENAI_API_KEY"):
            raise ValueError("llm.backend=openai requires OPENAI_API_KEY in the environment")
        return model, os.environ.get("OPENAI_BASE_URL", "https://api.openai.com/v1"), {}
    raise ValueError(f"Unknown llm.backend: {backend}")


def preflight(cfg: Dict[str, Any], video_id: str, base_url: str) -> Tuple[List[str], Dict[str, Any]]:
    errors, info = [], {}
    overview_file = os.path.join(cfg["paths"]["caption_dir"], video_id, f"{cfg['report']['overview_granularity']}.json")
    if not os.path.isfile(overview_file):
        errors.append(f"overview caption file missing: {overview_file}")
    info["overview_file"] = overview_file

    if cfg["llm"]["backend"] == "local":
        root = base_url.rsplit("/v1", 1)[0]
        try:
            ok = requests.get(f"{root}/health", timeout=5).ok
        except requests.RequestException as e:
            ok, info["llm_health_error"] = False, str(e)
        if not ok:
            errors.append(f"LLM endpoint not healthy at {root}/health (start local_llm_server.py or vLLM)")

    svc = f"http://{cfg['service']['host']}:{cfg['service']['port']}"
    try:
        health = requests.get(f"{svc}/health", timeout=5)
        info["retrieval_service"] = health.json() if health.ok else {"status_code": health.status_code}
        load = requests.post(f"{svc}/videos/{video_id}/load", timeout=1800)
        if not load.ok:
            errors.append(f"retrieval service cannot load {video_id}: HTTP {load.status_code} {load.text[:500]}")
    except requests.RequestException as e:
        errors.append(f"retrieval service not reachable at {svc} ({e}); start videorag_retriever_service.py")
    info["retriever_url"] = f"{svc}/videos/{video_id}/search"

    try:
        D.resolve_targets()
    except Exception as e:
        errors.append(f"Deep-Reporter template contract check failed: {e}")
    return errors, info


def translation_llm(cfg: Dict[str, Any], model: str, base_url: str, env: Dict[str, str]):
    """Same endpoint/model as Deep-Reporter's primary LLM (OpenAI-compatible)."""
    from videorag_retriever_service import EndpointLLM
    max_tokens = int(cfg["report"].get("translation_max_tokens", 4096))
    if cfg["llm"]["backend"] == "local":
        return EndpointLLM(base_url, env["QWEN_API_KEY"], model, max_tokens, "max_tokens")
    return EndpointLLM(os.environ.get("OPENAI_BASE_URL"), os.environ["OPENAI_API_KEY"], model, max_tokens,
                       "max_completion_tokens")


# ---------------------------------------------------------------------------
# Validation
# ---------------------------------------------------------------------------

def validate(result: Dict[str, Any], grounded: Dict[str, Any], query: str, enable_filter: bool,
             max_sections: int, repetition: Optional[List[Dict[str, Any]]] = None,
             boundary: Optional[List[Dict[str, Any]]] = None) -> Tuple[List[str], List[str]]:
    errors, warnings = [], []
    if not result.get("success"):
        errors.append(f"generate_article failed: {result.get('error')}")
        return errors, warnings
    outline = result.get("outline") or []
    if not outline:
        errors.append("empty outline")
    planner_fallback = len(outline) == 1 and outline[0].get("section_description") == query
    if planner_fallback:
        errors.append("planner fallback: single section equal to the query (outline JSON was not parsed)")
    elif outline:
        # Decision 5 (prompt compliance; warnings): section cap and a final "Conclusion:" section.
        if len(outline) > max_sections:
            warnings.append(f"planner produced {len(outline)} sections, above report.max_sections={max_sections}")
        descriptions = [(s.get("section_description") or "").lstrip() for s in outline]
        if not descriptions[-1].startswith(D.CONCLUSION_PREFIX):
            warnings.append(f"last section is not a conclusion (description does not start with '{D.CONCLUSION_PREFIX}')")
        else:
            words = len((outline[-1].get("content") or "").split())
            if words > 300:
                warnings.append(f"conclusion section has {words} words (template asks for 100-250)")
        extra = [i for i, d in enumerate(descriptions[:-1], 1) if d.startswith(D.CONCLUSION_PREFIX)]
        if extra:
            warnings.append(f"non-final section(s) {extra} start with '{D.CONCLUSION_PREFIX}'")
    for idx, section in enumerate(outline, 1):
        content = section.get("content") or ""
        texts, _ = G.section_evidence(section, enable_filter)
        if not content.strip():
            errors.append(f"section {idx}: empty content")
        elif any(m in content for m in FAILURE_MARKERS):
            errors.append(f"section {idx}: LLM failure text in content: {content[:160]!r}")
        if not texts:
            errors.append(f"section {idx}: no text evidence retrieved")
        if section.get("text_queries") == [section.get("section_description")]:
            warnings.append(f"section {idx}: query-generation fallback (queries = section description)")
        if content and "[citation:" not in content and "(citation:" not in content:
            warnings.append(f"section {idx}: no citations")
    stats, gstats = grounded["citation_stats"], grounded["grounding_stats"]
    if stats["invalid_citations"]:
        errors.append(f"{stats['invalid_citations']} invalid citation(s) (index out of range or unparseable)")
    if stats["missing_frame_files"]:
        errors.append(f"{stats['missing_frame_files']} cited frame file(s) missing")
    if stats["wrong_form_image_citations"]:
        warnings.append(f"{stats['wrong_form_image_citations']} image citation(s) written as [citation:imgN] "
                        f"were converted to figures")
    for key in ("unsupported", "miscited", "uncited_claims"):
        if gstats.get(key):
            warnings.append(f"rule-based evidence check: {gstats[key]} {key} (see validation.json grounding_findings)")
    # P9: repeated sentences removed before grounding, and sections cut at the server max_tokens cap.
    for r in repetition or []:
        if r["removed_sentences"]:
            # 2026-10-26: label as a loop only when the section was cut at the max_tokens cap or a sentence repeats
            # >= 5 times (3-4 repeats were ordinary repetition in the 2026-10-25 check, DESIGN_AND_STATUS §9.16).
            loop = " (writer repetition loop suspected)" if r["max_repeat"] >= 5 or r["ends_mid_sentence"] else ""
            warnings.append(f"section {r['index']}: removed {r['removed_sentences']} repeated sentence(s), "
                            f"a sentence occurred up to {r['max_repeat']} times{loop}")
        if r["ends_mid_sentence"]:
            warnings.append(f"section {r['index']}: ends mid-sentence (likely cut at the LLM max_tokens cap)")
    # P19: claims about how the whole video ends/begins whose cited evidence does not reach the end/start.
    if boundary:
        counts: Dict[str, int] = {}
        for f in boundary:
            counts[f["status"]] = counts.get(f["status"], 0) + 1
        warnings.append("video start/end claim check: " + ", ".join(f"{n} {k}" for k, n in sorted(counts.items()))
                        + " (see validation.json boundary_findings)")
    return errors, warnings


# ---------------------------------------------------------------------------
# Main flow
# ---------------------------------------------------------------------------

def run(cfg: Dict[str, Any], video_id: str, query: str, checklist: List[str], out_dir: str) -> int:
    rcfg = cfg["report"]
    timings: Dict[str, float] = {}
    t0 = time.time()
    try:
        model, base_url, env = llm_settings(cfg)
        max_sections = D.check_max_sections(rcfg.get("max_sections", 6))
        context_mode = rcfg.get("previous_sections_context", "written")
        if context_mode not in ("written", "deep_reporter"):
            raise ValueError(f"report.previous_sections_context must be 'written' or 'deep_reporter', got {context_mode!r}")
    except ValueError as e:
        logger.error(str(e))
        return 2
    errors, info = preflight(cfg, video_id, base_url)
    timings["preflight_sec"] = round(time.time() - t0, 1)
    if errors:
        for e in errors:
            logger.error(f"preflight: {e}")
        return 2
    # P19: real video end from the last 10sec caption (the 10min overview ends at a window boundary).
    try:
        video_end, video_end_sec = D.load_video_end(os.path.join(cfg["paths"]["caption_dir"], video_id, "10sec.json"))
    except (OSError, ValueError, KeyError, IndexError) as e:
        logger.warning(f"video end unknown ({e}); writer rule 7 and the start/end claim check use no end time")
        video_end, video_end_sec = None, None
    # P19 (2026-10-26): last ~60 s of 10sec captions, shown to the writer as source txt0 (LAST section only).
    try:
        ending_block, ending_item = D.load_video_ending(os.path.join(cfg["paths"]["caption_dir"], video_id, "10sec.json"))
    except (OSError, ValueError, KeyError, IndexError) as e:
        logger.warning(f"end-of-video source unavailable ({e})")
        ending_block, ending_item = None, None

    os.environ.update(env)  # must precede create_openai_api (BaseConfig reads env at construction)
    from deep_reporter.api import create_openai_api
    from deep_reporter.llms.factory import get_primary_llm
    os.makedirs(rcfg["deep_reporter_log_dir"], exist_ok=True)
    api = create_openai_api({"primary_model": model, "log_dir": rcfg["deep_reporter_log_dir"]})
    routed = getattr(get_primary_llm("answer"), "base_url_val", None)
    if routed != base_url:
        logger.error(f"Deep-Reporter routed {model!r} to {routed!r}, expected {base_url!r}")
        return 2

    overview = D.load_video_overview(info["overview_file"])
    logger.info(f"Generating report for {video_id} (model={model}, domain={rcfg['domain']})")
    t1 = time.time()
    with D.apply_templates(D.build_templates(rcfg["domain"], overview, max_sections, video_end=video_end,
                                                 video_ending=ending_block)), \
            (D.apply_written_context() if context_mode == "written" else nullcontext()):
        result = api.generate_article(
            overall_query=query, overall_checklist=checklist, generation_mode="with_planner",
            text_topk=int(rcfg["text_topk"]), image_topk=int(rcfg["image_topk"]),
            enable_filter=bool(rcfg["enable_filter"]), retriever_url=info["retriever_url"],
            userid=f"report_{video_id}")
    timings["generation_sec"] = round(time.time() - t1, 1)

    os.makedirs(out_dir, exist_ok=True)
    mode = (info.get("retrieval_service") or {}).get("mode", "?")
    header = (f"> **Video**: `{video_id}` · **Request**: {query}  \n"
              f"> **Generated**: {datetime.now().isoformat(timespec='seconds')} · **LLM**: {model} "
              f"({cfg['llm']['backend']}) · **Retrieval**: WorldMM memories, episodic filter {mode}  \n"
              f"> Numbers in brackets refer to the References at the end; times are video timestamps (HH:MM:SS).")
    t2 = time.time()
    repetition: List[Dict[str, Any]] = []
    boundary: List[Dict[str, Any]] = []
    ending_cited: List[int] = []
    if result.get("success"):
        for idx, section in enumerate(result.get("outline") or [], 1):
            if section.get("content") and ending_item and G.attach_ending_source(section, ending_item, bool(rcfg["enable_filter"])):
                ending_cited.append(idx)
            if section.get("content"):
                section["content"], rep = G.dedupe_repeated_sentences(section["content"])
                repetition.append(dict(rep, index=idx))
                texts, _ = G.section_evidence(section, bool(rcfg["enable_filter"]))
                boundary += [dict(f, section=idx) for f in G.boundary_claims(section["content"], texts, video_end_sec)]
    grounded = G.ground_report(result, bool(rcfg["enable_filter"]), out_dir, header=header) if result.get("success") \
        else {"markdown": "", "references": [], "figures": [], "sections": [],
              "citation_stats": {k: 0 for k in ("invalid_citations", "missing_frame_files", "wrong_form_image_citations")},
              "grounding_stats": {}, "image_time_alignment": {}}
    timings["postprocess_sec"] = round(time.time() - t2, 2)
    errors, warnings = validate(result, grounded, query, bool(rcfg["enable_filter"]), max_sections, repetition, boundary)
    n_sections = len(result.get("outline") or [])
    if [i for i in ending_cited if i != n_sections]:
        warnings.append(f"end-of-video source (txt0) cited outside the last section: sections {[i for i in ending_cited if i != n_sections]}")

    translation: Dict[str, Any] = {"status": "disabled"}
    if rcfg.get("translate_ko") and result.get("success"):
        if errors:
            translation = {"status": "skipped", "reason": "validation errors (English report failed validation)"}
        else:
            t3 = time.time()
            header_ko = (f"> **영상**: `{video_id}` · **요청**: {query}  \n"
                         f"> **생성**: {datetime.now().isoformat(timespec='seconds')} · **LLM**: {model} "
                         f"({cfg['llm']['backend']}) · **검색**: WorldMM 메모리, episodic filter {mode}  \n"
                         f"> 이 문서는 영어 보고서(`report.md`, 정본)를 섹션 단위로 번역한 것입니다. 대괄호 번호는 마지막 "
                         f"References(근거 원문, 영어)를, 시간은 영상 타임스탬프(HH:MM:SS)를 가리킵니다. "
                         f"그림 캡션과 따옴표 안의 문구는 근거 원문 그대로입니다.")
            translated = RT.translate_report(grounded, header_ko, translation_llm(cfg, model, base_url, env))
            with open(os.path.join(out_dir, "report_ko.md"), "w", encoding="utf-8") as f:
                f.write(translated["markdown"])
            translation = {"status": translated["status"], "proper_nouns": translated["proper_nouns"],
                           "sections": translated["sections"]}
            timings["translation_sec"] = round(time.time() - t3, 1)
            for s in translated["sections"]:
                if s["status"] != "translated":
                    warnings.append(f"translation of section {s['index']} failed ({s['reason']}); English kept in report_ko.md")
                elif s.get("foreign_script"):
                    warnings.append(f"translation of section {s['index']} contains non-Hangul CJK characters after retry: "
                                    f"{s['foreign_script'][:5]} (kept; check report_ko.md)")
    timings["total_sec"] = round(time.time() - t0, 1)

    with open(os.path.join(out_dir, "report.md"), "w", encoding="utf-8") as f:
        f.write(grounded["markdown"])
    with open(os.path.join(out_dir, "report_raw.md"), "w", encoding="utf-8") as f:
        f.write(result.get("final_article", ""))
    keep = ("section_description", "sectional_checklist", "text_queries", "image_queries", "content",
            "retrieved_texts", "retrieved_images", "filtered_texts", "filtered_images")
    with open(os.path.join(out_dir, "report.json"), "w", encoding="utf-8") as f:
        json.dump({"video_id": video_id, "query": query, "checklist": checklist, "model": model,
                   "llm_backend": cfg["llm"]["backend"], "retrieval_mode": mode, "domain": rcfg["domain"],
                   "previous_sections_context": context_mode,
                   "session_id": result.get("session_id"), "success": result.get("success"),
                   "error": result.get("error"),
                   "outline": [{k: s.get(k) for k in keep} for s in result.get("outline") or []],
                   "references": grounded["references"], "figures": grounded["figures"]},
                  f, indent=2, ensure_ascii=False)
    status = "passed" if not errors else "failed"
    with open(os.path.join(out_dir, "validation.json"), "w", encoding="utf-8") as f:
        json.dump({"status": status, "errors": errors, "warnings": warnings, "timings": timings,
                   "max_sections": max_sections, "previous_sections_context": context_mode,
                   "video_end": video_end, "repetition": repetition, "boundary_findings": boundary,
                   "ending_source": {"available": bool(ending_item), "cited_in_sections": ending_cited,
                                     "span": (f"{G.hms_from_time_str(ending_item['start_time'])}-{video_end}" if ending_item else None)},
                   "translation": translation,
                   "citation_stats": grounded["citation_stats"], "grounding_stats": grounded["grounding_stats"],
                   "image_time_alignment": grounded["image_time_alignment"],
                   "sections": [{k: v for k, v in s.items() if k != "grounding"} | {"grounding_stats": s["grounding"]["stats"]}
                                for s in grounded["sections"]],
                   "grounding_findings": [dict(f, section=s["index"]) for s in grounded["sections"]
                                          for f in s["grounding"]["findings"]]},
                  f, indent=2, ensure_ascii=False)

    logger.info(f"Report: {os.path.join(out_dir, 'report.md')} | status={status} errors={len(errors)} "
                f"warnings={len(warnings)} | {timings}")
    for e in errors:
        logger.error(f"validation: {e}")
    for w in warnings:
        logger.warning(f"validation: {w}")
    return 0 if not errors else 1


def main() -> None:
    parser = argparse.ArgumentParser(description="Generate a grounded video report (WorldMM retrieval + Deep-Reporter)")
    parser.add_argument("--config", required=True)
    parser.add_argument("--video-id", required=True)
    parser.add_argument("--query", required=True, help="Report request (overall_query)")
    parser.add_argument("--checklist", action="append", default=[], help="Overall requirement (repeatable)")
    parser.add_argument("--out-dir", default=None, help="Default: {report.outputs_dir}/{video_id}_{timestamp}")
    args = parser.parse_args()
    logging.basicConfig(level=logging.INFO, format="%(asctime)s %(name)s %(levelname)s %(message)s")
    cfg = yaml.safe_load(open(args.config, encoding="utf-8"))
    out_dir = args.out_dir or os.path.join(cfg["report"]["outputs_dir"],
                                           f"{args.video_id}_{datetime.now().strftime('%Y%m%d_%H%M%S')}")
    sys.exit(run(cfg, args.video_id, args.query, args.checklist, out_dir))


if __name__ == "__main__":
    main()
