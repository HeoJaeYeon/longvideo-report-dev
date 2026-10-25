#!/usr/bin/env python3
"""
Grounding post-processor for Deep-Reporter output (report_framework [C]) and a rule-based
evidence consistency check.

Deep-Reporter writes section-local placeholder citations: [citation:txtN] refers to the
N-th text source and ![](citation:imgN) to the N-th image source of that section
(1-based; `filtered_*` when the filter node ran, else `retrieved_*`, exactly like
section_writing_node). This module turns them into a readable, verifiable report:

  - text citations  -> global reference numbers [n]; a References list gives each source's
                       time range / granularity (episodic) or "no timestamp" (semantic)
  - image citations -> numbered figures (frame copied into <out_dir>/frames/, caption with time)
  - the wrong form [citation:imgN] (observed from Qwen3-VL-8B) is converted to the figure:
    "(Figure k)" in the sentence and the image inserted after the paragraph
  - invalid citations become "[?]" and are counted; the same source/frame is numbered once

check_section_grounding() is the rule-based check (no LLM): for every sentence it verifies
that quoted strings, numbers and HH:MM:SS times appear in the evidence that sentence cites
(times may also fall inside a cited evidence interval). It cannot judge meaning, so its
findings are warnings, not proof of an error. Sentences that state that the evidence does NOT
show something ("no times such as "10:85" are visible in the retrieved footage") are recorded
as "absence" statements: tokens inside the negated clause (from the negation to the end of that
clause) are not checked, because they are by design not in the evidence. Tokens elsewhere in the
same sentence (e.g. "his score improves to 3/16, though the time is not specified in the
evidence") are still checked.

Each section also records image_time_alignment: for every figure cited in the section, the
distance between the frame time and the text evidence cited near it (same paragraph, else the
previous text paragraph) and in the whole section (0 = inside a cited interval).
"""

import os
import re
import shutil
from typing import Any, Dict, List, Optional, Tuple

CITE_GROUP_RE = re.compile(r"\[\s*citation\s*:\s*([^\[\]]*?)\s*\]", re.I)
IMG_EMBED_RE = re.compile(r"!\[[^\[\]]*\]\(\s*citation\s*:\s*img\s*(\d+)\s*\)", re.I)
SOURCE_TOKEN_RE = re.compile(r"^(txt|img)\s*(\d+)$", re.I)
TIMESTAMP_RE = re.compile(r"\b\d{1,2}:\d{2}:\d{2}\b")
QUOTE_RE = re.compile(r"[\"“”]([^\"“”\n]{2,300}?)[\"“”]")
NUMBER_RE = re.compile(r"(?<![\w:./-])\d+(?:[:./-]\d+)*(?![\w:/-]|\.\d)")
SENTENCE_SPLIT_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"“\[(])")
LEADING_CITES_RE = re.compile(r"^((?:\s*\[\s*citation\s*:[^\[\]]*\])+)", re.I)
FAILURE_MARKERS = ("Call failed:", "[Section generation failed")

# "Absence" statements: a negation followed within a few words by a show/mention-type verb, in a
# sentence that talks about the evidence itself (footage / evidence / retrieved / video / clip /
# frame / source). Example: "no specific times such as "10:85" are visible or mentioned in the
# retrieved footage". A plain negated event ("He did not make the shot, as shown on the
# scoreboard") has no evidence noun and is still checked.
ABSENCE_NEG_RE = re.compile(
    r"(?:\b(?:not|no|never|none|neither|nor|without)\b|n['’]t\b)(?:\W+\w+){0,12}?\W+"
    r"(?:show|shows|shown|showing|visible|seen|mention(?:s|ed)?|state[sd]?|depict(?:s|ed)?|describe[sd]?|"
    r"demonstrate[sd]?|display(?:s|ed)?|provide[sd]?|confirm(?:s|ed)?|indicate[sd]?|specif(?:y|ies|ied)|"
    r"detail(?:s|ed)?|capture[sd]?|include[sd]?|contain(?:s|ed)?|reveal(?:s|ed)?|appear(?:s|ed)?|"
    r"present(?:s|ed)?|record(?:s|ed)?|explicitly|available)\b", re.I)
ABSENCE_SUBJECT_RE = re.compile(r"\b(?:footage|evidence|retrieved|video|clips?|frames?|sources?)\b", re.I)
CLAUSE_END_RE = re.compile(r"[;]|,\s*(?:but|though|although|while|whereas|which|and|so|yet)\b|\.\s|\.$", re.I)


def absence_clause(claim: str) -> Optional[Tuple[int, int]]:
    """(start, end) of a negated "the evidence does not show X" clause in the sentence, or None.
    The clause runs from the negation to the next clause boundary after the show-type verb."""
    if not ABSENCE_SUBJECT_RE.search(claim):
        return None
    m = ABSENCE_NEG_RE.search(claim)
    if not m:
        return None
    end = CLAUSE_END_RE.search(claim, m.end())
    return m.start(), (end.start() if end else len(claim))


def _claim_tokens(text: str) -> List[Tuple[str, str]]:
    quotes = [q.strip(" .,;:!?") for q in QUOTE_RE.findall(text)]
    quotes = [q for q in quotes if len(normalize(q)) >= 2]
    rest = QUOTE_RE.sub(" ", text)
    return ([("quote", q) for q in quotes] + [("time", t) for t in TIMESTAMP_RE.findall(rest)]
            + [("number", n) for n in sorted(number_tokens(rest))])

NUMBER_WORDS = {0: "zero", 1: "one", 2: "two", 3: "three", 4: "four", 5: "five", 6: "six", 7: "seven",
                8: "eight", 9: "nine", 10: "ten", 11: "eleven", 12: "twelve", 13: "thirteen", 14: "fourteen",
                15: "fifteen", 16: "sixteen", 17: "seventeen", 18: "eighteen", 19: "nineteen", 20: "twenty",
                30: "thirty", 40: "forty", 50: "fifty", 60: "sixty", 100: "hundred"}


# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------

def section_evidence(section: Dict[str, Any], enable_filter: bool) -> Tuple[List[Dict], List[Dict]]:
    """The exact source lists section_writing_node numbered (txtN, imgN)."""
    if enable_filter and section.get("filtered_texts") is not None:
        return section.get("filtered_texts") or [], section.get("filtered_images") or []
    return section.get("retrieved_texts") or [], section.get("retrieved_images") or []


def parse_tokens(group: str) -> Tuple[List[Tuple[str, int]], List[str]]:
    """'txt1, img2' -> ([('txt', 1), ('img', 2)], malformed_tokens)."""
    parsed, malformed = [], []
    for raw in re.split(r"[,;\s]+(?=(?:txt|img))|[,;]", group, flags=re.I):
        token = raw.strip()
        if not token:
            continue
        m = SOURCE_TOKEN_RE.match(token)
        if m:
            parsed.append((m.group(1).lower(), int(m.group(2))))
        else:
            malformed.append(token)
    return parsed, malformed


def hms(seconds: Optional[float]) -> str:
    if seconds is None:
        return "?"
    s = int(round(float(seconds)))
    return f"{s // 3600:02d}:{s % 3600 // 60:02d}:{s % 60:02d}"


def hms_from_time_str(time_str: Optional[str]) -> str:
    if not time_str:
        return "?"
    t = str(time_str).zfill(8)
    return f"{t[0:2]}:{t[2:4]}:{t[4:6]}"


def to_seconds(hhmmss: str) -> int:
    h, m, s = (int(x) for x in hhmmss.split(":"))
    return h * 3600 + m * 60 + s


def strip_label(text: str) -> str:
    """Remove the leading '[... | ...]' evidence label added by the retrieval service."""
    return re.sub(r"^\s*\[[^\]]*\|[^\]]*\]\s*", "", text or "").strip()


def normalize(text: str) -> str:
    text = (text or "").lower().replace("’", "'").replace("‘", "'")
    return re.sub(r"\s+", " ", re.sub(r"[^a-z0-9':./ -]", " ", text)).strip()


def evidence_text(item: Dict[str, Any], kind: str) -> str:
    if kind == "img":
        text = item.get("caption", item.get("description", ""))
        if item.get("frame_sec") is not None:
            text += f" {hms(item['frame_sec'])}"
        return text
    return item.get("content", item.get("text", ""))


def number_tokens(text: str) -> set:
    return set(NUMBER_RE.findall(TIMESTAMP_RE.sub(" ", text)))


def _words(text: str) -> List[str]:
    return re.findall(r"[a-z0-9']+", normalize(TIMESTAMP_RE.sub(" ", text)).replace("/", " "))


def quote_supported(quote: str, text: str) -> bool:
    """Literal match, or the quote's words in the same order within a short window of one
    evidence text (e.g. "SCORE 5" vs "a score of 5"). Not a bag-of-words match, so a word that
    appears elsewhere in the evidence does not count."""
    if normalize(quote) in normalize(text):
        return True
    q, words = _words(quote), _words(text)
    if not q:
        return False
    window = len(q) + 3
    for start, w in enumerate(words):
        if w != q[0]:
            continue
        pos, ok = start, True
        for token in q[1:]:
            try:
                pos = words.index(token, pos + 1, start + window)
            except ValueError:
                ok = False
                break
        if ok:
            return True
    return False


def number_supported(token: str, text: str) -> bool:
    """Exact number token; 'a/b' also as 'a out of b'; small integers also as words."""
    if token in number_tokens(text):
        return True
    if re.fullmatch(r"\d+/\d+", token):
        a, b = token.split("/")
        return bool(re.search(rf"\b{a}\s+out\s+of\s+{b}\b", text, re.I))
    word = NUMBER_WORDS.get(int(token)) if token.isdigit() else None
    return bool(word) and bool(re.search(rf"\b{word}\b", text, re.I))


# ---------------------------------------------------------------------------
# Rule-based grounding check
# ---------------------------------------------------------------------------

def split_sentences(content: str) -> List[str]:
    """Sentences of a section body (headings and image-embed lines skipped); leading
    citation groups are attached to the previous sentence."""
    sentences: List[str] = []
    for paragraph in re.split(r"\n\s*\n", content):
        lines = [ln for ln in paragraph.split("\n")
                 if ln.strip() and not ln.lstrip().startswith("#") and not IMG_EMBED_RE.fullmatch(ln.strip())]
        text = " ".join(ln.strip() for ln in lines)
        if not text:
            continue
        for part in SENTENCE_SPLIT_RE.split(text):
            lead = LEADING_CITES_RE.match(part)
            if lead and sentences:
                sentences[-1] += " " + lead.group(1).strip()
                part = part[lead.end():].strip()
            if part:
                sentences.append(part)
    return sentences


def dedupe_repeated_sentences(content: str) -> Tuple[str, Dict[str, Any]]:
    """P9: drop exact repeats of a sentence already written earlier in the same section (keeps the first one).
    A writer repetition loop repeats the same few sentences until max_tokens; headings and image-embed lines are
    kept as they are. Also reports whether the section ends without terminal punctuation (cut at max_tokens)."""
    seen: Dict[str, int] = {}
    removed = 0
    out_lines: List[str] = []
    for line in content.split("\n"):
        text = line.strip()
        if not text or text.startswith("#") or IMG_EMBED_RE.fullmatch(text):
            out_lines.append(line)
            continue
        kept = []
        for part in SENTENCE_SPLIT_RE.split(text):
            key = re.sub(r"\s+", " ", part).strip()
            if not key:
                continue
            seen[key] = seen.get(key, 0) + 1
            if seen[key] == 1:
                kept.append(part)
            else:
                removed += 1
        if kept:
            out_lines.append(" ".join(kept))
    new = re.sub(r"\n{3,}", "\n\n", "\n".join(out_lines)).strip()
    body = [ln.strip() for ln in new.split("\n") if ln.strip() and not ln.strip().startswith("#")
            and not IMG_EMBED_RE.fullmatch(ln.strip())]
    last = CITE_GROUP_RE.sub("", body[-1]).strip() if body else ""
    return new, {"removed_sentences": removed, "max_repeat": max(seen.values(), default=0),
                 "ends_mid_sentence": bool(last) and last[-1] not in ".!?\"”'\u2019)"}


ENDING_RE = re.compile(r"\b(?:the\s+)?video\s+(?:closes|ends|concludes|wraps\s+up|finishes)\b"
                       r"(?!\s+(?:this|that|the)\s+(?:section|segment|part|portion|sequence))|"
                       r"\b(?:final|closing|last)\s+(?:scene|shot|moments?|frames?|segment)\s+of\s+the\s+video\b", re.I)
OPENING_RE = re.compile(r"\b(?:the\s+)?video\s+(?:opens|begins|starts)\b|"
                        r"\b(?:first|opening)\s+(?:scene|shot|moments?|frames?|segment)\s+of\s+the\s+video\b", re.I)


def boundary_claims(content: str, texts: List[Dict], video_end_sec: Optional[float],
                    margin_sec: float = 120.0) -> List[Dict[str, Any]]:
    """P19: sentences that say how the whole video ends (or begins), checked against the time range of their
    cited text evidence. 'ending_early': the latest cited evidence ends more than margin_sec before the video end;
    'opening_late': the earliest cited evidence starts more than margin_sec after 00:00:00; '*_unverifiable': the
    sentence cites no timed text evidence."""
    findings = []
    for sentence in split_sentences(content):
        claim = CITE_GROUP_RE.sub(" ", sentence)
        idxs = [i for g in CITE_GROUP_RE.findall(sentence) for kind, i in parse_tokens(g)[0] if kind == "txt"]
        timed = [texts[i - 1] for i in idxs if 1 <= i <= len(texts) and texts[i - 1].get("end_sec") is not None]
        if ENDING_RE.search(claim) and video_end_sec:
            if not timed:
                findings.append({"status": "ending_unverifiable", "sentence": sentence[:300], "cited": idxs})
            else:
                latest = max(float(t["end_sec"]) for t in timed)
                if video_end_sec - latest > margin_sec:
                    findings.append({"status": "ending_early", "sentence": sentence[:300], "cited": idxs,
                                     "latest_cited_end": hms(latest), "video_end": hms(video_end_sec)})
        if OPENING_RE.search(claim):
            if not timed:
                findings.append({"status": "opening_unverifiable", "sentence": sentence[:300], "cited": idxs})
            else:
                earliest = min((float(t["start_sec"]) for t in timed if t.get("start_sec") is not None), default=None)
                if earliest is not None and earliest > margin_sec:
                    findings.append({"status": "opening_late", "sentence": sentence[:300], "cited": idxs,
                                     "earliest_cited_start": hms(earliest)})
    return findings


def check_section_grounding(content: str, texts: List[Dict], images: List[Dict]) -> Dict[str, Any]:
    """Check quoted strings / numbers / HH:MM:SS of each sentence against its cited evidence."""
    sources = {("txt", i): t for i, t in enumerate(texts, 1)}
    sources.update({("img", i): m for i, m in enumerate(images, 1)})
    findings, stats = [], {"sentences": 0, "cited_sentences": 0, "checked_tokens": 0,
                           "unsupported": 0, "miscited": 0, "uncited_claims": 0, "absence_statements": 0}
    for sentence in split_sentences(content):
        stats["sentences"] += 1
        cited = []
        for group in CITE_GROUP_RE.findall(sentence):
            cited += [t for t in parse_tokens(group)[0] if t in sources]
        claim = CITE_GROUP_RE.sub(" ", sentence)
        tokens = _claim_tokens(claim)
        if not tokens:
            continue
        span = absence_clause(claim)
        if span:
            inside = set(_claim_tokens(claim[span[0]:span[1]]))
            outside = set(_claim_tokens(claim[:span[0]] + " . " + claim[span[1]:]))
            exempt = [t for t in tokens if t in inside and t not in outside]
            if exempt:
                stats["absence_statements"] += 1
                findings.append({"status": "absence", "sentence": sentence[:300], "tokens": [t for _, t in exempt],
                                 "cited": [f"{k}{i}" for k, i in cited]})
                tokens = [t for t in tokens if t not in exempt]
                if not tokens:
                    continue
        if not cited:
            stats["uncited_claims"] += 1
            findings.append({"status": "uncited", "sentence": sentence[:300],
                             "tokens": [t for _, t in tokens], "cited": []})
            continue
        stats["cited_sentences"] += 1

        def supports(keys, kind, token) -> bool:
            texts_ = [evidence_text(sources[k], k[0]) for k in keys]
            if kind == "quote":
                return any(quote_supported(token, t) for t in texts_)
            if kind == "time":
                if any(token in t for t in texts_):
                    return True
                sec = to_seconds(token)
                return any(sources[k].get("start_sec") is not None and sources[k].get("end_sec") is not None
                           and float(sources[k]["start_sec"]) <= sec <= float(sources[k]["end_sec"]) for k in keys)
            return any(number_supported(token, t) for t in texts_)

        others = [k for k in sources if k not in cited]
        for kind, token in tokens:
            stats["checked_tokens"] += 1
            if supports(cited, kind, token):
                continue
            found_in = [f"{k[0]}{k[1]}" for k in others if supports([k], kind, token)]
            status = "miscited" if found_in else "unsupported"
            stats[status] += 1
            findings.append({"status": status, "kind": kind, "token": token, "sentence": sentence[:300],
                             "cited": [f"{k}{i}" for k, i in cited], "found_in_uncited": found_in})
    return {"stats": stats, "findings": findings}


# ---------------------------------------------------------------------------
# Image time alignment (recorded only; no warning)
# ---------------------------------------------------------------------------

def _cited_txt(text: str) -> List[int]:
    return [i for g in CITE_GROUP_RE.findall(text) for kind, i in parse_tokens(g)[0] if kind == "txt"]


def _interval_gap(sec: float, intervals: List[Tuple[float, float]]) -> Optional[float]:
    if not intervals:
        return None
    return round(min(0.0 if a <= sec <= b else min(abs(sec - a), abs(sec - b)) for a, b in intervals), 1)


def image_time_alignment(content: str, texts: List[Dict], images: List[Dict]) -> List[Dict[str, Any]]:
    """For each image cited in the section (![](citation:imgN) or the wrong form [citation:imgN]):
    frame time vs. the time ranges of text evidence cited (a) in the same paragraph before/after the
    image, or in the previous text paragraph if the image stands alone, and (b) anywhere in the section.
    Semantic evidence has no time and is ignored. gap_sec = 0 means the frame is inside a cited range."""
    def intervals(idxs):
        out = []
        for i in sorted(set(idxs)):
            if 1 <= i <= len(texts):
                t = texts[i - 1]
                if t.get("start_sec") is not None and t.get("end_sec") is not None:
                    out.append((float(t["start_sec"]), float(t["end_sec"])))
        return out

    section_iv = intervals(_cited_txt(content))
    paragraphs = re.split(r"\n\s*\n", content)
    seen, rows = set(), []
    for p_idx, paragraph in enumerate(paragraphs):
        img_idxs = [int(i) for i in IMG_EMBED_RE.findall(paragraph)]
        img_idxs += [i for g in CITE_GROUP_RE.findall(paragraph) for kind, i in parse_tokens(g)[0] if kind == "img"]
        if not img_idxs:
            continue
        text_part = IMG_EMBED_RE.sub(" ", paragraph)
        local = _cited_txt(text_part)
        j = p_idx - 1
        while not local and j >= 0:          # stand-alone image line: use the previous text paragraph
            local = _cited_txt(IMG_EMBED_RE.sub(" ", paragraphs[j]))
            j -= 1
        local_iv = intervals(local)
        for idx in img_idxs:
            if idx in seen or not 1 <= idx <= len(images):
                continue
            seen.add(idx)
            item = images[idx - 1]
            if item.get("frame_sec") is None:
                continue
            sec = float(item["frame_sec"])
            rows.append({"img": f"img{idx}", "uid": item.get("uid"), "frame": hms(sec), "frame_sec": sec,
                         "local_text_ranges": [f"{hms(a)}-{hms(b)}" for a, b in local_iv],
                         "gap_to_local_text_sec": _interval_gap(sec, local_iv),
                         "gap_to_section_text_sec": _interval_gap(sec, section_iv)})
    return rows


# ---------------------------------------------------------------------------
# Citation grounding (placeholder -> references / figures)
# ---------------------------------------------------------------------------

class _Registry:
    def __init__(self, out_dir: str, frames_subdir: str):
        self.out_dir, self.frames_subdir = out_dir, frames_subdir
        self.refs: Dict[str, Dict[str, Any]] = {}
        self.figures: Dict[str, Dict[str, Any]] = {}

    @staticmethod
    def _key(item: Dict[str, Any]) -> str:
        return str(item.get("uid") or item.get("id") or item.get("img_path") or item.get("content") or id(item))

    def ref(self, item: Dict[str, Any]) -> int:
        key = self._key(item)
        if key not in self.refs:
            self.refs[key] = {"n": len(self.refs) + 1, "item": item}
        return self.refs[key]["n"]

    def figure(self, item: Dict[str, Any]) -> Tuple[Dict[str, Any], bool]:
        """(figure record, is_new)."""
        key = self._key(item)
        if key in self.figures:
            return self.figures[key], False
        src = item.get("img_path") or ""
        rel, missing = None, not (src and os.path.isfile(src))
        if not missing:
            os.makedirs(os.path.join(self.out_dir, self.frames_subdir), exist_ok=True)
            name = f"{item.get('video_id', 'video')}_{os.path.basename(src)}"
            shutil.copy2(src, os.path.join(self.out_dir, self.frames_subdir, name))
            rel = f"{self.frames_subdir}/{name}"
        record = {"k": len(self.figures) + 1, "item": item, "rel_path": rel, "missing": missing, "src": src}
        self.figures[key] = record
        return record, True


def _figure_block(fig: Dict[str, Any]) -> str:
    item, k = fig["item"], fig["k"]
    start, end = hms_from_time_str(item.get("start_time")), hms_from_time_str(item.get("end_time"))
    caption = strip_label(item.get("caption", item.get("description", "")))
    if len(caption) > 300:
        caption = caption[:297].rstrip() + "..."
    at = hms(item.get("frame_sec"))
    if fig["missing"]:
        return f"*[Figure {k}: frame file missing ({fig['src']})] {start}–{end}*"
    return (f"![Figure {k} ({at})]({fig['rel_path']})\n\n"
            f"*Figure {k}. Frame at {at} (clip {start}–{end}). {caption}*")


def _reference_line(n: int, item: Dict[str, Any]) -> str:
    source = item.get("source", "")
    body = strip_label(item.get("text") or item.get("content", ""))
    if len(body) > 220:
        body = body[:217].rstrip() + "..."
    if source == "worldmm-semantic" or item.get("time_grounded") is False:
        triple = item.get("triple")
        fact = f"({', '.join(triple)})" if triple else body
        return f"[{n}] Video-level knowledge (semantic memory, no timestamp): {fact}"
    start, end = hms_from_time_str(item.get("start_time")), hms_from_time_str(item.get("end_time"))
    gran = item.get("granularity", "")
    if item.get("type") == "image":
        return f"[{n}] Frame {start}–{end}: {strip_label(item.get('caption', ''))[:220]}"
    return f"[{n}] {start}–{end} · episodic {gran}: {body}"


def _rewrite_section(content: str, texts: List[Dict], images: List[Dict], reg: _Registry, stats: Dict[str, int]) -> str:
    out_paragraphs = []
    for paragraph in re.split(r"\n\s*\n", content):
        pending: List[str] = []

        def embed(m):
            idx = int(m.group(1))
            stats["image_embeds"] += 1
            if not 1 <= idx <= len(images):
                stats["invalid_citations"] += 1
                return "[?]"
            fig, new = reg.figure(images[idx - 1])
            if new:
                pending.append(_figure_block(fig))
            else:
                stats["duplicate_image_embeds"] += 1
            return ""

        def group(m):
            tokens, malformed = parse_tokens(m.group(1))
            stats["malformed_tokens"] += len(malformed)
            parts = []
            for kind, idx in tokens:
                if kind == "txt":
                    stats["text_citations"] += 1
                    if 1 <= idx <= len(texts):
                        parts.append(f"[{reg.ref(texts[idx - 1])}]")
                    else:
                        stats["invalid_citations"] += 1
                        parts.append("[?]")
                else:
                    stats["wrong_form_image_citations"] += 1
                    if 1 <= idx <= len(images):
                        fig, new = reg.figure(images[idx - 1])
                        if new:
                            pending.append(_figure_block(fig))
                        parts.append(f"(Figure {fig['k']})")
                    else:
                        stats["invalid_citations"] += 1
                        parts.append("[?]")
            if malformed and not tokens:
                stats["invalid_citations"] += 1
                return "[?]"
            return "".join(p if p.startswith("[") else f" {p}" for p in parts).strip()

        text = IMG_EMBED_RE.sub(embed, paragraph)
        text = CITE_GROUP_RE.sub(group, text)
        text = re.sub(r"\)\(Figure", ") (Figure", text)
        text = "\n".join(ln.rstrip() for ln in text.split("\n") if ln.strip())
        blocks = ([text] if text else []) + pending
        if blocks:
            out_paragraphs.append("\n\n".join(blocks))
    return "\n\n".join(out_paragraphs)


def ground_report(result: Dict[str, Any], enable_filter: bool, out_dir: str,
                  header: Optional[str] = None, frames_subdir: str = "frames") -> Dict[str, Any]:
    """Grounded markdown + references/figures + citation stats + rule-based check per section."""
    reg = _Registry(out_dir, frames_subdir)
    totals = {k: 0 for k in ("text_citations", "invalid_citations", "malformed_tokens", "image_embeds",
                             "wrong_form_image_citations", "duplicate_image_embeds")}
    bodies, sections = [], []
    for idx, section in enumerate(result.get("outline") or [], 1):
        texts, images = section_evidence(section, enable_filter)
        content = section.get("content") or ""
        stats = {k: 0 for k in totals}
        failed = (not content.strip()) or any(m in content for m in FAILURE_MARKERS)
        grounding = check_section_grounding(content, texts, images) if content else {"stats": {}, "findings": []}
        body = _rewrite_section(content, texts, images, reg, stats) if content else f"[Section {idx} content missing]"
        bodies.append(body)
        for k in totals:
            totals[k] += stats[k]
        cited_txt = {int(i) for g in CITE_GROUP_RE.findall(content) for kind, i in parse_tokens(g)[0] if kind == "txt"}
        sections.append({
            "index": idx, "section_description": section.get("section_description", ""),
            "text_queries": section.get("text_queries"), "image_queries": section.get("image_queries"),
            "evidence": {"texts": len(texts), "images": len(images)},
            "unused_text_evidence": len([i for i in range(1, len(texts) + 1) if i not in cited_txt]),
            "failed_marker": failed, "words": len(content.split()), "citations": stats,
            "grounding": grounding,
            "image_time_alignment": image_time_alignment(content, texts, images) if content else [],
        })

    refs = sorted(reg.refs.values(), key=lambda r: r["n"])
    figures = sorted(reg.figures.values(), key=lambda f: f["k"])
    rows = [r for s in sections for r in s["image_time_alignment"]]
    local = [r["gap_to_local_text_sec"] for r in rows if r["gap_to_local_text_sec"] is not None]
    whole = [r["gap_to_section_text_sec"] for r in rows if r["gap_to_section_text_sec"] is not None]
    alignment = {"cited_images": len(rows),
                 "without_local_text_time": len(rows) - len(local),
                 "local_gap_sec": {"zero": sum(g == 0 for g in local), "max": max(local) if local else None,
                                   "median": sorted(local)[len(local) // 2] if local else None},
                 "section_gap_sec": {"zero": sum(g == 0 for g in whole), "max": max(whole) if whole else None,
                                     "median": sorted(whole)[len(whole) // 2] if whole else None}}
    parts = ([header.strip()] if header else []) + bodies
    if refs:
        parts.append("# References\n\n" + "\n".join(_reference_line(r["n"], r["item"]) for r in refs))
    totals.update({"references": len(refs), "figures": len(figures),
                   "missing_frame_files": sum(f["missing"] for f in figures)})
    return {
        "markdown": "\n\n".join(parts) + "\n",
        "section_bodies": bodies,          # grounded markdown per section (used by report_translator)
        "references": [{"n": r["n"], "uid": r["item"].get("uid"), "source": r["item"].get("source"),
                        "start_time": r["item"].get("start_time"), "end_time": r["item"].get("end_time"),
                        "line": _reference_line(r["n"], r["item"])} for r in refs],
        "figures": [{"k": f["k"], "uid": f["item"].get("uid"), "rel_path": f["rel_path"], "src": f["src"],
                     "missing": f["missing"], "frame_sec": f["item"].get("frame_sec")} for f in figures],
        "citation_stats": totals,
        "image_time_alignment": alignment,
        "sections": sections,
        "grounding_stats": {k: sum(s["grounding"]["stats"].get(k, 0) for s in sections)
                            for k in ("sentences", "cited_sentences", "checked_tokens", "unsupported",
                                      "miscited", "uncited_claims", "absence_statements")},
    }
