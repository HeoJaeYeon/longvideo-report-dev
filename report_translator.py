#!/usr/bin/env python3
"""
Korean translation of the grounded English report (decision 6).

The English report.md stays the authoritative output; this adds report_ko.md. Each section is
translated with one LLM call. Everything that carries grounding is protected so the translation
cannot break it:
  - figure blocks (image line, caption line) are replaced by own-line placeholders and kept verbatim
    (captions are source evidence)
  - inline citations [n] / [?], figure references (Figure k), HH:MM:SS times and quoted strings
    ("on-screen text" / speech, source wording) are replaced by [[Pn]] placeholders
  - proper-noun runs (names of people, products, brands) are protected the same way. Without NER
    a person name cannot be told apart from another proper noun, so every capitalized run that
    appears mid-sentence somewhere in the report body (not at a sentence start, not a common word)
    is collected once per report and protected everywhere in that report, headings included.
After translation every placeholder must appear exactly once and the number of headings must be
unchanged; otherwise the call is retried once and, if it still fails, the English section is kept
with a notice. CJK characters other than Hangul (Han ideographs, kana) in the translated text
(protected spans excluded) also trigger the single retry; if they remain, the translation is kept
and the characters are reported (`foreign_script`). References stay in English (they quote source
evidence).
"""

import re
import time
from typing import Any, Dict, List, Tuple

PLACEHOLDER_RE = re.compile(r"\[\[\s*P\s*(\d+)\s*\]\]")
INLINE_PROTECT_RE = re.compile(
    r"[\"“][^\"“”\n]{1,300}[\"”]"          # quoted strings
    r"|(?:\[(?:\d+|\?)\])+"                # citation runs: [3][5], [?]
    r"|\(Figure \d+\)"                     # figure references
    r"|\b\d{1,2}:\d{2}:\d{2}\b"            # HH:MM:SS
)
HEADING_RE = re.compile(r"^#{1,6}\s", re.M)
FOREIGN_SCRIPT_RE = re.compile(r"[\u3040-\u30ff\u3400-\u4dbf\u4e00-\u9fff\uf900-\ufaff]+")   # kana, Han
NAME_TOKEN = r"(?:[A-Z][a-z]+(?:['’][a-z]+)?|[A-Z]{2,}|[A-Z][a-z]*[A-Z][A-Za-z]*)"
NAME_RUN_RE = re.compile(rf"(?<![\w\[])({NAME_TOKEN}(?:[ \-]{NAME_TOKEN})*)(?![\w\]])")
NAME_STOPWORDS = {
    "I", "A", "An", "The", "And", "Or", "But", "Nor", "So", "Yet", "In", "On", "At", "Of", "To", "For", "With",
    "As", "By", "From", "Into", "Over", "After", "Before", "During", "When", "While", "Then", "Although",
    "Though", "However", "Overall", "No", "Not", "This", "That", "These", "Those", "It", "Its", "He", "She",
    "They", "We", "You", "His", "Her", "Their", "Our", "Your", "There", "Here", "If", "Once", "Also", "Both",
    "Each", "All", "Some", "Any", "One", "Two", "Three", "First", "Second", "Third", "Final", "Next", "Later",
    "Section", "Sections", "Figure", "Figures", "Video", "Report", "References", "Conclusion", "Summary",
    "OK", "TV"}
SENTENCE_START_RE = re.compile(r"(?:^|[.!?:]\s+|\n)\s*[\"“(]*$")
FENCE_RE = re.compile(r"^\s*```[a-zA-Z]*\s*\n(.*?)\n\s*```\s*$", re.S)

PROMPT_HEAD = """Translate the following Markdown section of a video analysis report from English into natural, formal Korean.

Rules:
1. Keep every placeholder of the form [[P1]], [[P2]], ... exactly as written, exactly once, at the corresponding position. Never translate, renumber, merge, split, or drop a placeholder. A placeholder on its own line must stay on its own line.
2. Keep the Markdown structure: the same headings (# / ##) in the same order and the same paragraphs.
3. Translate faithfully: do not add, remove, summarize, or explain information.
4. Keep the names of people, products, brands, and on-screen labels in their original spelling.
5. Output only the translated Markdown, without comments or code fences.

Section:
<<<
"""
PROMPT_TAIL = "\n>>>"

FALLBACK_NOTICE = "> ⚠️ 이 섹션은 번역 검증에 실패하여 영어 원문을 그대로 유지했습니다."


def is_figure_paragraph(paragraph: str) -> bool:
    p = paragraph.lstrip()
    return p.startswith("![Figure") or p.startswith("*Figure ") or p.startswith("*[Figure ")


def _trim_run(run: str) -> str:
    """Drop leading/trailing common words from a capitalized run ("The Flick Glove" -> "Flick Glove")."""
    words = run.split(" ")
    while words and words[0] in NAME_STOPWORDS:
        words.pop(0)
    while words and words[-1] in NAME_STOPWORDS:
        words.pop()
    return " ".join(words)


def collect_proper_nouns(bodies: List[str]) -> List[str]:
    """Capitalized runs that occur at least once mid-sentence in a body paragraph (headings, figure
    blocks and already protected spans excluded). Longest first, for masking."""
    found = set()
    for body in bodies:
        for paragraph in re.split(r"\n\s*\n", body):
            if is_figure_paragraph(paragraph):
                continue
            text = "\n".join(l for l in paragraph.split("\n") if not l.lstrip().startswith("#"))
            text = INLINE_PROTECT_RE.sub(" . ", text)
            for m in NAME_RUN_RE.finditer(text):
                if SENTENCE_START_RE.search(text[:m.start()]):
                    continue
                run = _trim_run(m.group(1))
                if run and len(run) >= 2:
                    found.add(run)
    return sorted(found, key=lambda r: (-len(r), r))


def mask(body: str, proper_nouns: List[str] = ()) -> Tuple[str, List[str]]:
    """Replace protected spans with [[Pn]]; returns (masked_text, originals by index-1)."""
    originals: List[str] = []

    def keep(text: str) -> str:
        originals.append(text)
        return f"[[P{len(originals)}]]"

    name_re = re.compile(r"(?<![\w\[])(?:" + "|".join(re.escape(n) for n in proper_nouns) + r")(?![\w\]])") \
        if proper_nouns else None
    paragraphs = []
    for paragraph in re.split(r"\n\s*\n", body):
        if is_figure_paragraph(paragraph):
            paragraphs.append(keep(paragraph))
            continue
        masked = INLINE_PROTECT_RE.sub(lambda m: keep(m.group(0)), paragraph)
        if name_re:
            parts = re.split(r"(\[\[P\d+\]\])", masked)   # never touch existing placeholders
            masked = "".join(p if PLACEHOLDER_RE.fullmatch(p) else name_re.sub(lambda m: keep(m.group(0)), p)
                             for p in parts)
        paragraphs.append(masked)
    return "\n\n".join(paragraphs), originals


def clean_output(text: str) -> str:
    text = (text or "").strip()
    m = FENCE_RE.match(text)
    if m:
        text = m.group(1).strip()
    if text.startswith("<<<"):
        text = text[3:].lstrip()
    if text.endswith(">>>"):
        text = text[:-3].rstrip()
    return text


def check_and_unmask(translated: str, masked: str, originals: List[str]) -> Tuple[bool, str, str]:
    """(ok, unmasked_text, reason)."""
    if not translated.strip():
        return False, "", "empty translation"
    found = [int(i) for i in PLACEHOLDER_RE.findall(translated)]
    expected = list(range(1, len(originals) + 1))
    if sorted(found) != expected:
        missing = sorted(set(expected) - set(found))
        dup = sorted({i for i in found if found.count(i) > 1})
        extra = sorted(set(found) - set(expected))
        return False, "", f"placeholder mismatch (missing={missing[:10]}, duplicated={dup[:10]}, unknown={extra[:10]})"
    if len(HEADING_RE.findall(translated)) != len(HEADING_RE.findall(masked)):
        return False, "", "heading count changed"
    return True, PLACEHOLDER_RE.sub(lambda m: originals[int(m.group(1)) - 1], translated), ""


def translate_section(body: str, llm, max_attempts: int = 2, proper_nouns: List[str] = ()) -> Dict[str, Any]:
    masked, originals = mask(body, proper_nouns)
    protected_names = sum(1 for o in originals if o in set(proper_nouns))
    attempts, reason = 0, ""
    with_foreign = None          # first valid translation that still contains Han/kana (kept if no clean one)
    start = time.time()
    while attempts < max_attempts:
        attempts += 1
        try:
            raw = llm.generate([{"role": "user", "content": PROMPT_HEAD + masked + PROMPT_TAIL}])
        except Exception as e:
            reason = f"LLM call failed: {type(e).__name__}: {str(e)[:200]}"
            continue
        translated = clean_output(raw)
        ok, text, reason = check_and_unmask(translated, masked, originals)
        if not ok:
            continue
        foreign = FOREIGN_SCRIPT_RE.findall(PLACEHOLDER_RE.sub(" ", translated))   # protected spans excluded
        if not foreign:
            return {"status": "translated", "text": text, "attempts": attempts, "placeholders": len(originals),
                    "protected_names": protected_names, "foreign_script": [],
                    "seconds": round(time.time() - start, 1), "reason": ""}
        reason = f"non-Hangul CJK characters in translation: {foreign[:10]}"
        if with_foreign is None:
            with_foreign = (text, foreign)
    if with_foreign:
        return {"status": "translated", "text": with_foreign[0], "attempts": attempts, "placeholders": len(originals),
                "protected_names": protected_names, "foreign_script": with_foreign[1][:20],
                "seconds": round(time.time() - start, 1), "reason": reason}
    return {"status": "fallback_english", "text": FALLBACK_NOTICE + "\n\n" + body, "attempts": attempts,
            "placeholders": len(originals), "protected_names": protected_names, "foreign_script": [],
            "seconds": round(time.time() - start, 1), "reason": reason}


def translate_report(grounded: Dict[str, Any], header_ko: str, llm) -> Dict[str, Any]:
    """report_ko.md content + per-section status from ground_report() output."""
    proper_nouns = collect_proper_nouns(grounded["section_bodies"])
    results = [translate_section(body, llm, proper_nouns=proper_nouns) for body in grounded["section_bodies"]]
    parts = [header_ko.strip()] + [r["text"] for r in results]
    if grounded["references"]:
        parts.append("# References\n\n> 근거 원문(영어)을 그대로 둡니다. 본문의 대괄호 번호가 아래 항목을 가리킵니다.\n\n"
                     + "\n".join(r["line"] for r in grounded["references"]))
    translated = sum(r["status"] == "translated" for r in results)
    return {
        "markdown": "\n\n".join(parts) + "\n",
        "status": "complete" if translated == len(results) else ("partial" if translated else "failed"),
        "proper_nouns": proper_nouns,
        "sections": [{k: v for k, v in r.items() if k != "text"} | {"index": i}
                     for i, r in enumerate(results, 1)],
    }
