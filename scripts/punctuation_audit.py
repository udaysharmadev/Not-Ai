#!/usr/bin/env python3
"""Run the Not-AI 4.0 Punctuation & Prosody Engine on a draft or voice pair.

Usage:
    python3 scripts/punctuation_audit.py draft.txt --genre linkedin
    python3 scripts/punctuation_audit.py draft.txt --genre academic --json
    python3 scripts/punctuation_audit.py draft.txt --genre personal --reference author.txt
    cat draft.txt | python3 scripts/punctuation_audit.py --stdin --genre technical
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path
import sys

TOOL_ROOT = Path(__file__).resolve().parents[1] / "plugins/not-ai/tools"
sys.path.insert(0, str(TOOL_ROOT))

from not_ai_core.policy import POLICIES  # noqa: E402
from not_ai_core.punctuation import (  # noqa: E402
    analyze_punctuation,
    compare_punctuation_voice,
)


def render_human(report: dict, voice_cmp: dict | None = None) -> str:
    prosody = report["prosody"]
    bounds = report["boundaries"]
    lines = [
        "NOT AI 4.0 : PUNCTUATION & PROSODY AUDIT",
        "─" * 44,
        f"Genre: {report['genre']} ({report['register_style']})  |  "
        f"Words: {report['word_count']}  |  Sentences: {report['sentence_count']}",
        "",
        "PUNCTUATION DISTRIBUTION (count | rate per 1k words)",
    ]
    for mark, count in report["counts"].items():
        if mark in ("quotes", "total_marks"):
            continue
        rate = report["rates_per_1k"].get(mark, 0.0)
        lines.append(f"  {mark:<14} {count:>4}  ({rate:>5.1f}/1k)")
    lines.append(f"  {'entropy':<14} {report['punctuation_entropy']:>4.3f} bits")
    lines.append(f"  {'commas/sent':<14} {report['commas_per_sentence']:>4.2f}")

    lines.extend([
        "",
        "PROSODY & CLAUSE CADENCE",
        f"  Sentence length: mean {prosody['sentence_length_mean']}w | "
        f"SD {prosody['sentence_length_sd']}w | CV {prosody['sentence_length_cv']}",
        f"  Adjacent sentence delta: {prosody['adjacent_length_delta_mean']}w",
        f"  Clauses per sentence:    {prosody['clauses_per_sentence_mean']} "
        f"(clause CV {prosody['clause_length_cv']})",
        f"  Introductory comma rate: {prosody['introductory_comma_rate']:.1%}",
        f"  Paragraphs: {prosody['paragraph_count']} "
        f"(single-sentence rate {prosody['single_sentence_paragraph_rate']:.1%})",
        "",
        "BOUNDARY RELIABILITY",
        f"  Boundary damage detected: {bounds['has_boundary_damage']}",
        f"  Terminal omission status: {bounds['terminal_omission_status']}",
    ])
    if bounds["fused_sentences"]:
        lines.append(f"  Fused sentence candidates: {bounds['fused_sentences']}")
    if bounds["tight_ellipsis_boundaries"]:
        lines.append(f"  Tight ellipsis boundaries: {bounds['tight_ellipsis_boundaries']}")

    lines.append("")
    lines.append("EDITORIAL FINDINGS")
    if report["findings"]:
        for item in report["findings"]:
            span = f" '{item['span']}'" if item.get("span") else ""
            lines.append(f"  • [{item['severity']}] {item['rule']} ({item['category']}){span}")
            lines.append(f"    {item['message']}")
    else:
        lines.append("  ✓ No punctuation or prosody findings.")

    if voice_cmp is not None:
        lines.extend([
            "",
            f"PUNCTUATION VOICE COMPARISON: {voice_cmp['overall']} "
            f"({voice_cmp['drifted_marks']} drifted)",
        ])
        for note in voice_cmp["notes"]:
            lines.append(f"  • {note}")

    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", nargs="?", help="Text file to analyze")
    parser.add_argument("--stdin", action="store_true", help="Read text from stdin")
    parser.add_argument("--genre", default="linkedin", choices=sorted(POLICIES))
    parser.add_argument("--reference", default=None, help="Author reference text for punctuation voice comparison")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    args = parser.parse_args()

    if args.stdin or not args.input_file:
        text = sys.stdin.read()
    else:
        path = Path(args.input_file)
        if not path.is_file():
            print(f"Error: file not found: {path}", file=sys.stderr)
            return 2
        text = path.read_text(encoding="utf-8")

    if not text.strip():
        print("Error: empty input text", file=sys.stderr)
        return 2

    report = analyze_punctuation(text, args.genre)
    voice_cmp = None
    if args.reference:
        ref_path = Path(args.reference)
        if not ref_path.is_file():
            print(f"Error: reference file not found: {ref_path}", file=sys.stderr)
            return 2
        voice_cmp = compare_punctuation_voice(
            ref_path.read_text(encoding="utf-8"),
            text,
            args.genre,
        )
        report["voice_comparison"] = voice_cmp

    if args.json:
        print(json.dumps(report, indent=2, ensure_ascii=False))
    else:
        print(render_human(report, voice_cmp))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
