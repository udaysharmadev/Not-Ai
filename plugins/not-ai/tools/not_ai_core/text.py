"""Canonical text primitives (Not-AI 3.0).

Single home for masking, sentence splitting, and tokenisation so the gate,
scripts, and new modules cannot drift apart (see SESSION_FAILURES parity lesson).
`scripts/_shared.py` re-exports these names; new code imports from here.
"""

from __future__ import annotations

import math
import re

WORD_RE = re.compile(r"\b[A-Za-z]+(?:'[A-Za-z]+)?\b")
WORD_PATTERN = re.compile(r"\b[a-zA-Z]+\b")
SENTENCE_SPLIT = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'])")

ABBREVIATIONS = (
    "Mr", "Mrs", "Ms", "Dr", "Prof", "Sr", "Jr", "St",
    "e.g", "i.e", "vs", "etc", "Fig", "Eq", "Ref", "No",
    "U.S", "U.K", "U.N", "E.U",
)
_ABBR_END_RE = re.compile(r"\b(?:" + "|".join(re.escape(a) for a in ABBREVIATIONS) + r")\.$")
_SINGLE_INITIAL_RE = re.compile(r"\b[A-Z]\.$")
FENCED_CODE_RE = re.compile(r"```.*?```", re.DOTALL)
INLINE_CODE_RE = re.compile(r"`[^`\n]+`")


def mask_for_counts(text: str) -> str:
    masked = FENCED_CODE_RE.sub("\n[code block]\n", text)
    masked = INLINE_CODE_RE.sub(" [code] ", masked)
    masked = re.sub(r"(?m)^\s*>\s?", "", masked)
    return masked


def strip_layout_lines(text: str) -> str:
    kept: list[str] = []
    for line in text.splitlines():
        s = line.strip()
        if not s:
            continue
        if re.match(r"^#{1,6}\s", s):
            continue
        if s.count("|") >= 2:
            continue
        if re.match(r"^(?:[-*\u2022]|\d+[.)])\s*$", s):
            continue
        kept.append(line)
    return "\n".join(kept)


def sentences(text: str) -> list[str]:
    normalized = re.sub(r"\s+", " ", strip_layout_lines(mask_for_counts(text)).strip())
    candidates = SENTENCE_SPLIT.split(normalized)
    merged: list[str] = []
    for cand in candidates:
        cand = cand.strip()
        if not cand:
            continue
        if merged and (_ABBR_END_RE.search(merged[-1]) or _SINGLE_INITIAL_RE.search(merged[-1])):
            merged[-1] = f"{merged[-1]} {cand}"
            continue
        merged.append(cand)
    out = []
    for item in merged:
        s = item.strip()
        if not s or len(words(s)) < 2:
            continue
        if re.match(r"^#{1,6}\s", s) or s.count("|") >= 2:
            continue
        if re.match(r"^(?:[-*\u2022]|\d+[.)])\s*$", s):
            continue
        out.append(s)
    return out


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def tokenize_words(text: str) -> list[str]:
    return WORD_PATTERN.findall(text)


def paragraphs(text: str) -> list[str]:
    return [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]


def opener_entropy(items: list[str]) -> float:
    openings = [words(i)[0].lower() for i in items if words(i)]
    if not openings:
        return 0.0
    total = len(openings)
    ent = 0.0
    for o in set(openings):
        p = openings.count(o) / total
        ent -= p * math.log2(p)
    return round(ent, 2)


def sentence_stats(lengths: list[int]) -> dict:
    if not lengths:
        return {"mean": 0.0, "median": 0.0, "sd": 0.0, "cv": 0.0,
                "min": 0, "max": 0}
    n = len(lengths)
    mean = sum(lengths) / n
    srt = sorted(lengths)
    median = float(srt[n // 2]) if n % 2 else (srt[n // 2 - 1] + srt[n // 2]) / 2
    var = sum((x - mean) ** 2 for x in lengths) / n
    sd = var ** 0.5
    return {"mean": round(mean, 1), "median": round(median, 1),
            "sd": round(sd, 1), "cv": round(sd / mean, 3) if mean else 0.0,
            "min": min(lengths), "max": max(lengths)}
