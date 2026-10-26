#!/usr/bin/env python3
"""
Domain prompt templates for Deep-Reporter, applied with a scoped and verified override.

Deep-Reporter's planner / query-generation / section-writing nodes read their prompt
template from a module-level global at call time and fill it with `.format(**kwargs)`.
No repo file is modified; instead, inside `apply_templates(...)`:
  1. targets are resolved from the function objects the graph registers
     (`deep_reporter.core.graph.<node>.__globals__`), i.e. the dict the node really reads;
  2. every template is checked against the node's contract before anything is changed:
     placeholders must be a subset of the node's `.format()` keywords (parsed from the
     node source with `ast`), required placeholders and output/citation markers must be
     present, and a dry-run `.format()` must succeed (catches stray braces);
  3. the globals are swapped only for the duration of the `with` block and the original
     objects are restored in `finally`. One application per process at a time.
Any contract violation raises before the run, so the pipeline never silently falls back
to Deep-Reporter's web-report templates.

Usage:
  from domain_templates import apply_templates, build_templates, load_video_overview
  overview = load_video_overview(".../caption/<vid>/10min.json")
  with apply_templates(build_templates("videomme", overview, max_sections=6)), apply_written_context():
      api.generate_article(...)

Previous-section context (decision 4, C0): Deep-Reporter's `_update_context` passes later
nodes only "Section: <planned description>" + the first 100 characters of each written
section (mostly its title). `apply_written_context()` swaps it, for the duration of the
block and with the same contract checks/restore, for a deterministic LLM-free summary of
what was actually written (title + first sentence of each paragraph, citations removed,
character-capped). The section tail is still computed by the original function.
  python domain_templates.py --check [--domain videomme] [--overview-file <10min.json>] [--max-sections N]
"""

import argparse
import ast
import inspect
import json
import os
import re
import string
import sys
import threading
from contextlib import contextmanager
from typing import Any, Dict, List, Optional, Set, Tuple

DEEP_REPORT_ROOT = "/data1/jyheo/workspace/VideoRAG/Deep-Report"

# Deep-Reporter graph node -> module-level template variable it formats at call time.
NODE_TEMPLATE_VARS = {
    "planner_node": "OUTLINE_GENERATION_TEMPLATE",
    "query_generation_node": "QUERY_GENERATION_TEMPLATE",
    "section_writing_node": "SECTION_WRITING_TEMPLATE",
}

# Placeholders a domain template must contain (each must also be a node .format() keyword).
REQUIRED_PLACEHOLDERS = {
    "OUTLINE_GENERATION_TEMPLATE": {"overall_query", "overall_checklist"},
    "QUERY_GENERATION_TEMPLATE": {"overall_query", "section_description", "sectional_checklist",
                                  "previous_sections_summary"},
    "SECTION_WRITING_TEMPLATE": {"overall_query", "section_description", "sectional_checklist",
                                 "previous_sections_summary", "previous_section_tail", "retrieved_materials",
                                 "position_info", "is_first_section", "is_last_section"},
}

# Literal strings that Deep-Reporter's parsers / citation regexes / run_report checks rely on.
REQUIRED_MARKERS = {
    "OUTLINE_GENERATION_TEMPLATE": ['"outline"', '"section_description"', '"sectional_checklist"', '"Conclusion:'],
    "QUERY_GENERATION_TEMPLATE": ['"text_queries"', '"image_queries"'],
    "SECTION_WRITING_TEMPLATE": ["[citation:txt1]", "![](citation:img1)", "# Title", '"Conclusion:"',
                                 "mention it in at most one short sentence"],
}

# Pre-filled slots (not .format placeholders): filled by build_templates().
VIDEO_OVERVIEW_SLOT = "<<VIDEO_OVERVIEW>>"
MAX_SECTIONS_SLOT = "<<MAX_SECTIONS>>"
VIDEO_END_SLOT = "<<VIDEO_END>>"   # P19: real end of the video (last 10sec caption), not the 10min window boundary
VIDEO_ENDING_SLOT = "<<VIDEO_ENDING>>"   # P19 (2026-10-26): last ~60 s of 10sec captions as citable source txt0
SLOT_RE = re.compile(r"<<[A-Z_]+>>")

# The last outline section must start with this (planner rule 6; checked by run_report).
CONCLUSION_PREFIX = "Conclusion:"

# Deep-Reporter runs planner + 3 nodes per section + combine under recursion_limit=50.
# Measured with the real graph (fake LLM, 2026-10-22): 15 sections succeed, 16 raise
# GraphRecursionError and the whole report is lost.
MIN_SECTIONS, MAX_SECTIONS_LIMIT = 3, 15


class TemplateContractError(RuntimeError):
    """A domain template does not satisfy a Deep-Reporter node contract."""


# ---------------------------------------------------------------------------
# Video-MME (general long video) templates
# ---------------------------------------------------------------------------

VIDEOMME_OUTLINE = """You are planning a report about ONE specific video. Everything in the report must come from this video.

**User request (report topic):**
{overall_query}

**Additional requirements from the user:**
{overall_checklist}

**Video overview** (timestamped summaries of consecutive ~10-minute segments, generated from the video's frames and speech; use it only to learn what the video contains):
<<VIDEO_OVERVIEW>>

**Task:**
Design an outline of 3-<<MAX_SECTIONS>> sections in total (never more than <<MAX_SECTIONS>>, including the final conclusion section) that answers the user request using content that is actually present in this video.

Rules:
1. Every section must be supportable by evidence from the video (visible events, actions, people, objects, settings, on-screen text, speech). Do not plan sections that need outside knowledge, background research, statistics, predictions, or opinions that the video does not express.
2. If the request asks about something the overview does not show, do not invent it; plan at most one section that reports what the video does and does not show about it.
3. Order the sections so the report reads coherently; the chronological order of the video is usually best for describing what happens.
4. section_description: 2-4 sentences explaining what the section covers, which part(s) of the video it draws on (approximate time ranges from the overview), and what the reader learns.
5. sectional_checklist: 3-5 concrete, checkable items about observable content, not generic writing advice.
6. The LAST section must be a brief conclusion that summarizes the main results already covered by the earlier sections and answers the user request at a high level. Its section_description must start exactly with "Conclusion:", it must not introduce new topics, and its sectional_checklist has 2-3 items. No other section_description may start with "Conclusion:".

**Output Format (JSON):**
```json
{{
  "outline": [
    {{
      "section_description": "This section introduces the people and the setting shown at the beginning of the video (about 00:00:00-00:10:00). It covers how the participants are presented and what the video announces it will do. Readers learn who appears in the video and what its stated goal is.",
      "sectional_checklist": [
        "Identify the main people and how they are introduced",
        "Describe the setting where the video takes place",
        "State the goal or plan announced at the start"
      ]
    }},
    ...
    {{
      "section_description": "Conclusion: This section briefly summarizes the main results shown in the video and answers the user request at a high level, using only findings covered in the earlier sections.",
      "sectional_checklist": [
        "Summarize the main outcomes shown in the video",
        "Answer the user request in one or two sentences"
      ]
    }}
  ]
}}
```

Generate the outline now:
"""

VIDEOMME_QUERY = """You generate search queries for retrieving evidence from ONE video's memory.

**Report topic:** {overall_query}

**Overall requirements:**
{overall_checklist}

**Previous sections (summary):**
{previous_sections_summary}

**Current section:** {section_description}

**Current section requirements:**
{sectional_checklist}

The video memory can be searched in two ways:
1. text_queries search timestamped descriptions of the video (what happens, who does what, what is said, which objects appear) and short facts extracted from the video. Write short keyword-style phrases that name concrete events, actions, people, objects, or spoken topics (e.g., "host explains the rules", "person unboxes the product").
2. image_queries search video clips by visual similarity. Write one sentence describing what the scene LOOKS like: people and their appearance and actions, objects, and the setting (e.g., "a woman in an apron stirring a pot in a bright kitchen"). Do not ask for charts, diagrams, infographics, or documents.

Cover the different requirements of the current section, avoid near-duplicate queries, and do not repeat what previous sections already covered unless it is needed.
Generate 2-3 text_queries and 1-2 image_queries.

**Output Format (JSON):**
```json
{{
  "text_queries": ["query 1", "query 2"],
  "image_queries": ["scene description 1"]
}}
```

Generate the queries now:
"""

VIDEOMME_SECTION = """# Role
You are an expert writer producing one section of a report about ONE specific video. The report must be grounded only in evidence retrieved from that video.

# Overall Report Context
**Report Topic:** {overall_query}

**Overall Requirements:**
{overall_checklist}

# Current Section Information
**Section Position:** {position_info}
**Section Description:** {section_description}

**Section Requirements (address every requirement the evidence supports):**
{sectional_checklist}

# Context from Previous Sections
**Summary of previous sections:**
{previous_sections_summary}

**End of previous section (for a smooth transition):**
{previous_section_tail}

# Retrieved Evidence from the Video
{retrieved_materials}

## How to read the evidence
- Text sources starting with "[HH:MM:SS-HH:MM:SS | episodic <scale>]" describe that part of the video (built from its frames and speech). Scales 10sec and 30sec give fine details; 3min and 10min are summaries of longer spans.
- Text sources starting with "[video-level knowledge | semantic]" are facts inferred from the whole video, written as (subject, predicate, object). They have NO timestamp.
- Image sources "[Source imgN: [HH:MM:SS-HH:MM:SS | video frame at Xs] description]" are frames taken from the video at that moment, with a description of that moment.

# End of the Video (reference for the LAST section)
<<VIDEO_ENDING>>
- This source shows how the whole video actually ends. Use it and cite it as [citation:txt0] ONLY in the LAST section, and only when you describe how the video ends. Other sections must not use or cite it.

# Grounding Rules (CRITICAL)
1. State only what the evidence supports. Do not add outside knowledge, assumptions, or speculation about intentions or feelings unless the evidence states them.
2. When describing an event, give its time from the evidence in HH:MM:SS form (e.g., "At 00:12:40, ..."). Never invent or estimate times that are not in the evidence. Do not attach times to video-level knowledge.
3. If sources conflict, prefer the finer-scale (10sec/30sec) description and mention the uncertainty.
4. If the evidence does not cover a requirement, say briefly that the retrieved footage does not show it instead of filling the gap. If no evidence was retrieved at all, write a short section that says so.
5. Describe events in chronological order unless the section needs another structure.
6. Do not repeat a fact, sentence, or paragraph you have already written in this section. If a fact was already covered in a previous section (see "Context from Previous Sections"), mention it in at most one short sentence and focus on what is new in this section. Exception: a conclusion section (see "Conclusion Section") restates earlier results briefly by design.
7. Each text source covers only its own time span. Words such as "the video opens", "begins", "closes", "ends" or "concludes" inside a 30sec, 3min or 10min summary refer to the start or end of THAT span, not of the whole video. The whole video runs from 00:00:00 to <<VIDEO_END>>. Describe how the whole video begins or ends only with sources whose time range reaches its first or last minutes; otherwise do not claim how the video begins or ends. To describe how the whole video ends, use the "End of the Video" source above and cite it as [citation:txt0] (LAST section only).

# Citation Rules (CRITICAL)
1. Text citation: put [citation:txt1], [citation:txt2], ... at the end of each sentence or claim that uses a text source. Every factual sentence needs at least one citation.
2. Image citation: to show a frame, put ![](citation:img1), ![](citation:img2), ... on its own line right after the sentence describing that moment. Use only sources marked as images, and include the 1-3 most relevant frames when available.
3. Use exactly these formats with one source per bracket; for several sources write [citation:txt1][citation:txt3].
4. Never write [citation:imgN]: an image source is cited ONLY as ![](citation:imgN) on its own line, and [citation:...] is used ONLY for txt sources.

# Position-Aware Writing Instructions
**Is this the FIRST section?** {is_first_section}
**Is this the LAST section?** {is_last_section}
- FIRST section: open by introducing the video and what the report covers; do not conclude the report.
- MIDDLE section: start with a smooth transition; do not use concluding phrases such as "In conclusion", "To summarize", or "Overall, this report".
- LAST section: you may synthesize the main points of the whole report, using only evidence-supported statements.

# Conclusion Section
If the Section Description starts with "Conclusion:", write a brief conclusion of 100-250 words: summarize only the main results already covered by the previous sections and answer the report topic at a high level. Do not introduce new events or details, keep at most one short paragraph per checklist item, and still cite the evidence above for every factual statement. If you state how the video ends, follow Grounding Rule 7.

# Format
- Start with a section title written as "# Title"; use "##" for subsections if needed.
- Typically 250-700 words, depending on how much evidence is available (a conclusion section: 100-250 words).
- Output ONLY the section content, without meta-commentary.

Begin writing the section now:"""

TEMPLATE_SETS: Dict[str, Dict[str, str]] = {
    "videomme": {
        "OUTLINE_GENERATION_TEMPLATE": VIDEOMME_OUTLINE,
        "QUERY_GENERATION_TEMPLATE": VIDEOMME_QUERY,
        "SECTION_WRITING_TEMPLATE": VIDEOMME_SECTION,
    },
}


# ---------------------------------------------------------------------------
# Building templates
# ---------------------------------------------------------------------------

def _hms(time_str: str) -> str:
    t = str(time_str).zfill(8)
    return f"{t[0:2]}:{t[2:4]}:{t[4:6]}"


def load_video_overview(caption_file: str) -> str:
    """WorldMM caption JSON (e.g. 10min.json) -> '[HH:MM:SS-HH:MM:SS] text' blocks."""
    with open(caption_file, "r", encoding="utf-8") as f:
        entries = json.load(f)
    blocks = [f"[{_hms(e['start_time'])}-{_hms(e['end_time'])}] {str(e.get('text', '')).strip()}" for e in entries]
    if not blocks:
        raise ValueError(f"No captions in {caption_file}")
    return "\n\n".join(blocks)


def load_video_end(caption_file: str) -> Tuple[str, int]:
    """End of the video from the last entry of a fine caption JSON (10sec.json): ('HH:MM:SS', seconds).
    The 10min file is not used because its last window ends at the window boundary, after the real end."""
    with open(caption_file, "r", encoding="utf-8") as f:
        last = str(json.load(f)[-1]["end_time"]).zfill(8)
    return _hms(last), int(last[0:2]) * 3600 + int(last[2:4]) * 60 + int(last[4:6])


def load_video_ending(caption_file: str, window_sec: int = 60) -> Tuple[str, Dict[str, Any]]:
    """P19: the 10sec captions of the last `window_sec` seconds as one text source.
    Returns (block for the writer template, shown as source txt0; evidence item in the retrieval service's text-item
    format, appended by run_report to a section that cites txt0)."""
    with open(caption_file, "r", encoding="utf-8") as f:
        entries = json.load(f)
    def sec(t):
        t = str(t).zfill(8)
        return int(t[0:2]) * 3600 + int(t[2:4]) * 60 + int(t[4:6])
    end = sec(entries[-1]["end_time"])
    tail = [e for e in entries if sec(e["end_time"]) > end - window_sec]
    start_time, end_time = str(tail[0]["start_time"]).zfill(8), str(entries[-1]["end_time"]).zfill(8)
    text = " ".join(str(e.get("text", "")).strip() for e in tail)
    label = f"[{_hms(start_time)}-{_hms(end_time)} | episodic 10sec, end of video]"
    block = f"[Source txt0 begin]\n{label} {text}\n[Source txt0 end]"
    item = {"content": f"{label} {text}", "text": text, "type": "text", "source": "worldmm-episodic",
            "granularity": "10sec", "start_time": start_time, "end_time": end_time,
            "start_sec": float(sec(start_time)), "end_sec": float(end),
            "uid": f"{os.path.basename(os.path.dirname(caption_file))}:episodic:end_of_video", "rank": 0}
    return block, item


def _escape_format(text: str) -> str:
    return text.replace("{", "{{").replace("}", "}}")


def check_max_sections(max_sections: int) -> int:
    if isinstance(max_sections, bool) or not isinstance(max_sections, int) \
            or not MIN_SECTIONS <= max_sections <= MAX_SECTIONS_LIMIT:
        raise ValueError(f"max_sections must be an integer in [{MIN_SECTIONS}, {MAX_SECTIONS_LIMIT}] "
                         f"(Deep-Reporter recursion_limit=50 allows at most {MAX_SECTIONS_LIMIT}), got {max_sections!r}")
    return max_sections


def build_templates(domain: str, video_overview: Optional[str] = None, max_sections: int = 6,
                    video_end: Optional[str] = None, video_ending: Optional[str] = None) -> Dict[str, str]:
    """Template set for `domain` with the video overview, the section cap and the video end time (HH:MM:SS;
    "the end of the video" when unknown) filled into their slots."""
    if domain not in TEMPLATE_SETS:
        raise KeyError(f"Unknown template domain: {domain} (available: {sorted(TEMPLATE_SETS)})")
    check_max_sections(max_sections)
    templates = dict(TEMPLATE_SETS[domain])
    for var, template in templates.items():
        if VIDEO_OVERVIEW_SLOT in template:
            if not video_overview:
                raise ValueError(f"{domain}/{var} needs a video overview")
            template = template.replace(VIDEO_OVERVIEW_SLOT, _escape_format(video_overview))
        template = template.replace(VIDEO_END_SLOT, video_end or "the end of the video")
        template = template.replace(VIDEO_ENDING_SLOT, _escape_format(video_ending) if video_ending
                                    else "(No end-of-video source is available for this video; do not cite txt0.)")
        templates[var] = template.replace(MAX_SECTIONS_SLOT, str(max_sections))
    return templates


# ---------------------------------------------------------------------------
# Contract resolution and validation
# ---------------------------------------------------------------------------

def _import_deep_reporter_graph():
    try:
        import deep_reporter.api  # noqa: F401  (must come first: importing deep_reporter.nodes first is circular)
    except ImportError:
        sys.path.insert(0, DEEP_REPORT_ROOT)
        import deep_reporter.api  # noqa: F401
    from deep_reporter.core import graph
    return graph


def _format_keywords(source_file: str, var: str) -> List[Set[str]]:
    """Keyword sets of every `<var>.format(...)` call in a module's source."""
    with open(source_file, "r", encoding="utf-8") as f:
        tree = ast.parse(f.read())
    calls = []
    for node in ast.walk(tree):
        if (isinstance(node, ast.Call) and isinstance(node.func, ast.Attribute) and node.func.attr == "format"
                and isinstance(node.func.value, ast.Name) and node.func.value.id == var):
            if node.args or any(k.arg is None for k in node.keywords):
                raise TemplateContractError(f"{source_file}: {var}.format() uses positional or **kwargs arguments")
            calls.append({k.arg for k in node.keywords})
    return calls


def resolve_targets() -> List[Dict[str, Any]]:
    """For each node: the namespace it reads its template from and the allowed placeholders."""
    graph = _import_deep_reporter_graph()
    targets = []
    for fn_name, var in NODE_TEMPLATE_VARS.items():
        fn = getattr(graph, fn_name, None)
        if fn is None or not callable(fn):
            raise TemplateContractError(f"deep_reporter.core.graph has no node function {fn_name}")
        if var not in fn.__code__.co_names:
            raise TemplateContractError(f"{fn_name} does not read global {var}")
        namespace = fn.__globals__
        if not isinstance(namespace.get(var), str):
            raise TemplateContractError(f"{fn.__module__}.{var} is missing or not a str")
        calls = _format_keywords(inspect.getsourcefile(fn), var)
        if len(calls) != 1:
            raise TemplateContractError(f"{fn.__module__}: expected exactly one {var}.format() call, found {len(calls)}")
        targets.append({"node": fn_name, "var": var, "module": fn.__module__,
                        "namespace": namespace, "allowed": calls[0]})
    return targets


def validate_templates(templates: Dict[str, str], targets: List[Dict[str, Any]]) -> None:
    """Raise TemplateContractError if any template breaks its node contract."""
    problems = []
    unknown = set(templates) - {t["var"] for t in targets}
    if unknown:
        problems.append(f"templates for unknown variables: {sorted(unknown)}")
    for target in targets:
        var, allowed = target["var"], target["allowed"]
        if var not in templates:
            problems.append(f"{var}: missing from template set")
            continue
        template = templates[var]
        unfilled = sorted(set(SLOT_RE.findall(template)) & {VIDEO_OVERVIEW_SLOT, MAX_SECTIONS_SLOT, VIDEO_END_SLOT, VIDEO_ENDING_SLOT})
        if unfilled:
            problems.append(f"{var}: unfilled {', '.join(unfilled)}")
        try:
            fields = {f for _, f, _, _ in string.Formatter().parse(template) if f is not None}
        except ValueError as e:
            problems.append(f"{var}: invalid format string ({e})")
            continue
        if not fields <= allowed:
            problems.append(f"{var}: placeholders not passed by {target['node']}: {sorted(fields - allowed)}")
        missing = REQUIRED_PLACEHOLDERS[var] - fields
        if missing:
            problems.append(f"{var}: missing required placeholders {sorted(missing)}")
        missing_markers = [m for m in REQUIRED_MARKERS[var] if m not in template.format(**{k: "" for k in allowed})] \
            if fields <= allowed else []
        if missing_markers:
            problems.append(f"{var}: missing output markers {missing_markers}")
        try:
            template.format(**{k: "x" for k in allowed})
        except (KeyError, IndexError, ValueError) as e:
            problems.append(f"{var}: dry-run format failed ({type(e).__name__}: {e})")
    if problems:
        raise TemplateContractError("; ".join(problems))


# ---------------------------------------------------------------------------
# Scoped application
# ---------------------------------------------------------------------------

_apply_lock = threading.Lock()


@contextmanager
def apply_templates(templates: Dict[str, str]):
    """Swap Deep-Reporter's node templates for the duration of the block (validated, restored)."""
    targets = resolve_targets()
    validate_templates(templates, targets)
    if not _apply_lock.acquire(blocking=False):
        raise RuntimeError("Domain templates are already applied in this process (nested/concurrent use)")
    originals = [(t["namespace"], t["var"], t["namespace"][t["var"]]) for t in targets]
    try:
        for target in targets:
            target["namespace"][target["var"]] = templates[target["var"]]
        yield targets
    finally:
        for namespace, var, original in originals:
            namespace[var] = original
        _apply_lock.release()
        if any(namespace[var] is not original for namespace, var, original in originals):
            raise RuntimeError("Failed to restore Deep-Reporter templates")


# ---------------------------------------------------------------------------
# Previous-section context (decision 4, C0)
# ---------------------------------------------------------------------------

UPDATE_CONTEXT_VAR = "_update_context"
UPDATE_CONTEXT_PARAMS = ["previous_summary", "new_content", "section_desc"]
WRITTEN_CONTEXT_NOTE = ("Already written in earlier sections (title, then the first sentence of each paragraph; "
                        "citation numbers removed - they do NOT refer to the evidence of the current section):")
SENTENCE_CHARS, SECTION_CONTEXT_CHARS, CONTEXT_TOTAL_CHARS = 240, 700, 3600
_CITATION_RE = re.compile(r"!?\[[^\]]*\]\(\s*citation:[^)]*\)|\[\s*citation:[^\]]*\]", re.IGNORECASE)
_ENTRY_SPLIT_RE = re.compile(r"\n\n(?=Section \d+: )")


def written_context_entry(index: int, content: str) -> str:
    """'Section k: <title>' + first sentence of each paragraph (citations removed), capped."""
    title = next((l.strip().lstrip("#").strip() for l in (content or "").splitlines() if l.strip().startswith("#")), "")
    title = re.sub(r"^section\s+\d+\s*[:.\-–—]\s*", "", title, flags=re.IGNORECASE)
    lines, used = [], 0
    for paragraph in re.split(r"\n\s*\n", content or ""):
        text = " ".join(l.strip() for l in paragraph.splitlines() if l.strip() and not l.strip().startswith("#"))
        text = re.sub(r"\s+([.,;:!?])", r"\1", re.sub(r"\s+", " ", _CITATION_RE.sub(" ", text))).strip()
        if len(text.split()) < 4:
            continue
        sentence = re.split(r"(?<=[.!?])\s+", text)[0][:SENTENCE_CHARS]
        if used + len(sentence) > SECTION_CONTEXT_CHARS:
            break
        lines.append(f"- {sentence}")
        used += len(sentence)
    return "\n".join([f"Section {index}: {title or '(untitled)'}"] + lines)


def written_context_summary(previous_summary: str, new_content: str) -> str:
    """Append the new section; if over CONTEXT_TOTAL_CHARS, reduce the oldest entries to their title line."""
    body = (previous_summary or "")
    if body.startswith(WRITTEN_CONTEXT_NOTE):
        body = body[len(WRITTEN_CONTEXT_NOTE):].lstrip("\n")
    entries = [e for e in _ENTRY_SPLIT_RE.split(body) if e.strip()] if body.strip() else []
    entries.append(written_context_entry(len(entries) + 1, new_content))
    for i in range(len(entries) - 1):
        if len("\n\n".join(entries)) <= CONTEXT_TOTAL_CHARS:
            break
        entries[i] = entries[i].split("\n", 1)[0]
    return WRITTEN_CONTEXT_NOTE + "\n" + "\n\n".join(entries)


def resolve_update_context() -> Dict[str, Any]:
    """The namespace section_writing_node reads `_update_context` from, with its contract checked."""
    graph = _import_deep_reporter_graph()
    fn = getattr(graph, "section_writing_node", None)
    if fn is None or UPDATE_CONTEXT_VAR not in fn.__code__.co_names:
        raise TemplateContractError(f"section_writing_node does not call global {UPDATE_CONTEXT_VAR}")
    original = fn.__globals__.get(UPDATE_CONTEXT_VAR)
    if not callable(original) or list(inspect.signature(original).parameters) != UPDATE_CONTEXT_PARAMS:
        raise TemplateContractError(f"{fn.__module__}.{UPDATE_CONTEXT_VAR} has an unexpected signature "
                                    f"(expected {UPDATE_CONTEXT_PARAMS})")
    probe = original("", "# T\n\nOne. Two. Three. Four.", "d")
    if not (isinstance(probe, tuple) and len(probe) == 2 and all(isinstance(x, str) for x in probe)):
        raise TemplateContractError(f"{UPDATE_CONTEXT_VAR} must return (summary, tail) strings")
    return {"namespace": fn.__globals__, "original": original, "module": fn.__module__}


_context_lock = threading.Lock()


@contextmanager
def apply_written_context():
    """Swap section_writing_node's `_update_context` for the written-content summary (restored on exit)."""
    target = resolve_update_context()
    namespace, original = target["namespace"], target["original"]

    def update_context(previous_summary: str, new_content: str, section_desc: str):
        _, tail = original("", new_content, section_desc)   # tail depends only on new_content
        return written_context_summary(previous_summary, new_content), tail

    if not _context_lock.acquire(blocking=False):
        raise RuntimeError("Written-context override is already applied in this process (nested/concurrent use)")
    try:
        namespace[UPDATE_CONTEXT_VAR] = update_context
        yield target
    finally:
        namespace[UPDATE_CONTEXT_VAR] = original
        _context_lock.release()
        if namespace[UPDATE_CONTEXT_VAR] is not original:
            raise RuntimeError(f"Failed to restore Deep-Reporter {UPDATE_CONTEXT_VAR}")


def main() -> None:
    parser = argparse.ArgumentParser(description="Validate domain templates against Deep-Reporter node contracts")
    parser.add_argument("--check", action="store_true", required=True)
    parser.add_argument("--domain", default="videomme")
    parser.add_argument("--overview-file", default=None, help="WorldMM 10min caption JSON for the planner overview")
    parser.add_argument("--max-sections", type=int, default=6)
    args = parser.parse_args()

    overview = load_video_overview(args.overview_file) if args.overview_file else "[00:00:00-00:10:00] sample {overview}"
    templates = build_templates(args.domain, overview, args.max_sections)
    targets = resolve_targets()
    validate_templates(templates, targets)
    for t in targets:
        print(f"OK {t['node']:<22} {t['var']:<28} module={t['module']} allowed={sorted(t['allowed'])}")
    print(f"domain={args.domain}: all templates satisfy the node contracts")


if __name__ == "__main__":
    main()
