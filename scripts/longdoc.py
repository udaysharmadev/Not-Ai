#!/usr/bin/env python3
"""Long-document mode: section-chunked gate review for documents over ~500 words.

Usage:
    python3 scripts/longdoc.py doc.md --genre technical
    python3 scripts/longdoc.py doc.md --genre academic --json
    python3 scripts/longdoc.py doc.md --genre readme --max-words 400

The document is split on markdown headings (or blank-line paragraphs when no
headings exist) into overlapping-window sections of at most --max-words each.
Every section gets its own gate review, and trigram repetition is checked
across sections to catch the cross-paragraph loops that single-paragraph
editing misses. Code fences and blockquotes are masked for measurement, as in
the gate itself.

This is an advisory review, not a rewrite and not an authorship verdict.
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parents[1] / "plugins/not-ai/tools"
sys.path.insert(0, str(TOOL_ROOT))
sys.path.insert(0, str(Path(__file__).resolve().parent))

from not_ai_core.gate import evaluate, mask_for_counts  # noqa: E402
from not_ai_core.policy import POLICIES  # noqa: E402
from not_ai_core.unicode_hygiene import (  # noqa: E402
    normalize_for_analysis,
    scan as scan_unicode,
)


def _without_fences(text: str) -> str:
    """Remove fenced code blocks so headings inside code do not split sections."""
    return re.sub(r"```.*?```", "\n", text, flags=re.DOTALL)


def split_sections(text: str, max_words: int) -> list[dict]:
    """Split on headings, then pack paragraphs into <= max_words windows."""
    chunks = re.split(r"(?m)^(#{1,6}\s+[^\n]+\n)", _without_fences(text))
    blocks: list[dict] = []
    pending_heading = None
    for chunk in chunks:
        if not chunk.strip():
            continue
        if re.match(r"^#{1,6}\s+", chunk):
            pending_heading = chunk.strip()
            continue
        paragraphs = [p for p in re.split(r"\n\s*\n", chunk) if p.strip()]
        if not paragraphs:
            continue
        current: list[str] = []
        current_words = 0
        current_heading = pending_heading
        for para in paragraphs:
            words = len(para.split())
            if current and current_words + words > max_words:
                blocks.append({"heading": current_heading, "text": "\n\n".join(current)})
                current, current_words = [], 0
                current_heading = None
            current.append(para)
            current_words += words
        if current:
            blocks.append({"heading": current_heading, "text": "\n\n".join(current)})
        pending_heading = None
    if not blocks and text.strip():
        words = text.split()
        for index in range(0, len(words), max_words):
            blocks.append({"heading": None, "text": " ".join(words[index:index + max_words])})
    return blocks


def cross_section_repeats(sections: list[dict], minimum: int = 3) -> list[dict]:
    """Trigrams repeated across different sections (not within one)."""
    STOP = {"the", "and", "for", "with", "from", "that", "this", "with"}
    seen: dict[str, set[int]] = {}
    for index, section in enumerate(sections):
        cleaned = mask_for_counts(section["text"])
        cleaned = re.sub(r"\[code block\]|\[code\]", " ", cleaned)
        cleaned = re.sub(r"https?://\S+|www\.\S+|[\w.-]+\.(?:com|org|io|ai|dev|md)\S*", " ", cleaned)
        tokens = re.findall(r"\b[a-z]+\b", cleaned.lower())
        for start in range(len(tokens) - 2):
            gram = tokens[start:start + 3]
            if all(word in STOP for word in gram):
                continue
            seen.setdefault(" ".join(gram), set()).add(index)
    repeats = [
        {"phrase": phrase, "sections": sorted(locations), "section_count": len(locations)}
        for phrase, locations in seen.items() if len(locations) >= minimum
    ]
    repeats.sort(key=lambda item: -item["section_count"])
    return repeats[:10]


def review(text: str, genre: str, max_words: int) -> dict:
    # Sectioning and per-section review run on the analysis-normalized copy so
    # invisible token splits cannot distort section budgets or gate counts.
    # The caller's raw document is never mutated.
    unicode_report = scan_unicode(text)
    text = normalize_for_analysis(text)
    sections = split_sections(text, max_words)
    section_reports = []
    for index, section in enumerate(sections, 1):
        result = evaluate(section["text"], genre)
        section_reports.append({
            "section": index,
            "heading": section["heading"],
            "words": result.word_count,
            "passed": result.passed,
            "findings": [
                {"rule": item.rule, "severity": item.severity, "span": item.span,
                 "sentence": item.sentence, "message": item.message}
                for item in result.findings
            ],
        })
    total_words = sum(section["words"] for section in section_reports)
    error_sections = sum(1 for section in section_reports if not section["passed"])
    entry: dict = {
        "genre": genre,
        "sections": len(section_reports),
        "total_words": total_words,
        "sections_with_errors": error_sections,
        "section_reports": section_reports,
        "cross_section_repeats": cross_section_repeats(sections),
        "unicode_hygiene": unicode_report,
    }
    # v3 global pass: document map before section edits, consistency after.
    try:
        from not_ai_core.information_structure import document_map as _docmap
        entry["document_map"] = _docmap(text)
    except Exception:
        pass
    try:
        entry["global_pass"] = _global_pass(text, sections)
    except Exception:
        pass
    return entry


def _global_pass(text: str, sections: list[dict]) -> dict:
    """Terminology drift, duplicates, contradictions, lost definitions, heading
    mismatch, repeated conclusions, broken refs, tone/voice drift."""
    import re
    from collections import Counter
    full = text
    # Defined terms: "X" means / X := / ## Term headings.
    defined = set(re.findall(r'"([^"\n]{2,40})"\s+(?:means|is|refers)', full))
    defined |= {h.strip("# ").strip().lower() for h in re.findall(r"(?m)^#{1,6}\s+([^\n]+)", full)}
    used_caps = Counter(re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,1}\b", full))
    drift = [t for t, c in used_caps.items() if c >= 3 and t.lower() not in defined and len(t) > 4][:8]
    # Duplicate explanations: same trigram in 2+ sections (reuse cross-section).
    repeats = cross_section_repeats(sections, minimum=2)[:5]
    # Contradictory claims proxy: both polarities present.
    contradictions = []
    low = full.casefold()
    for a, b in (("always", "never"), ("all users", "no users"), ("before", "after")):
        if a in low and b in low:
            contradictions.append(f"both '{a}' and '{b}' appear — verify they do not contradict")
    # Broken references: Figure/Table/Section N without a matching heading/caption.
    refs = sorted(set(re.findall(r"\b(?:Figure|Table|Section)\s+(\d+)", full)))
    broken = [f"Section/Figure {n} referenced" for n in refs if f"{n}" not in full][:5]
    # Heading mismatch: heading words absent from its section body.
    mismatches = []
    for sec in sections:
        h = (sec.get("heading") or "").strip("# ").lower()
        if h:
            hwords = [w for w in re.findall(r"[a-z]+", h) if len(w) > 4][:3]
            body = sec["text"].lower()
            if hwords and not any(w in body for w in hwords):
                mismatches.append(h[:60])
    return {"terminology_drift_candidates": drift,
            "duplicate_explanations": repeats,
            "contradiction_prompts": contradictions,
            "broken_reference_prompts": broken,
            "heading_mismatches": mismatches[:5],
            "note": "Global prompts after section edits; agent confirms each against source."}


def human_report(entry: dict) -> str:
    lines = ["NOT AI : LONG-DOCUMENT REVIEW", "─" * 40]
    lines.append(f"Genre: {entry['genre']}  |  Sections: {entry['sections']}  |  "
                 f"Words: {entry['total_words']}  |  Sections with errors: {entry['sections_with_errors']}")
    lines.append("")
    for section in entry["section_reports"]:
        heading = f" [{section['heading']}]" if section["heading"] else ""
        status = "pass" if section["passed"] else "FAIL"
        lines.append(f"Section {section['section']}{heading}: {status} ({section['words']} words)")
        for item in section["findings"][:6]:
            span = f" '{item['span']}'" if item["span"] else ""
            lines.append(f"  • [{item['severity']}] {item['rule']}{span}")
        if len(section["findings"]) > 6:
            lines.append(f"  ... and {len(section['findings']) - 6} more")
    if entry["cross_section_repeats"]:
        lines.append("")
        lines.append("CROSS-SECTION REPETITION (same phrase in 3+ sections)")
        for repeat in entry["cross_section_repeats"]:
            lines.append(f"  • '{repeat['phrase']}' in sections {repeat['sections']}")
    else:
        lines.append("")
        lines.append("No phrase repeats across 3+ sections.")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", help="Markdown or text document to review")
    parser.add_argument("--genre", default="technical", choices=sorted(POLICIES))
    parser.add_argument("--max-words", type=int, default=500)
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    path = Path(args.input_file)
    if not path.is_file():
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 2
    entry = review(path.read_text(encoding="utf-8"), args.genre, args.max_words)
    print(json.dumps(entry, indent=2, ensure_ascii=False) if args.json else human_report(entry))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
