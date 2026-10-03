#!/usr/bin/env python3
"""Diagnose prose in the Diagnose 2.0 shape used by examples/*/diagnostic.md.

Usage:
    python3 scripts/diagnose.py draft.txt --genre linkedin
    python3 scripts/diagnose.py draft.txt --genre academic --json
    cat draft.txt | python3 scripts/diagnose.py --stdin --genre technical
    python3 scripts/diagnose.py draft.txt --genre personal --reference author.txt

Output quotes the relevant spans, names the reader-facing reason, and prints
the measured figures behind each claim. It never rewrites and never claims
authorship or detector outcomes. Intervention level is a workload heuristic
(light/moderate/heavy) from finding counts, not a quality score.
"""

import argparse
import json
import re
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parent))
from _shared import get_sentences, tokenize_words  # noqa: E402

TOOL_ROOT = Path(__file__).resolve().parents[1] / "plugins/not-ai/tools"
sys.path.insert(0, str(TOOL_ROOT))

from not_ai_core.gate import evaluate  # noqa: E402
from not_ai_core.policy import POLICIES  # noqa: E402

try:
    from analyze_structure import analyze as analyze_structure
    _STRUCTURE_AVAILABLE = True
except ImportError:  # pragma: no cover
    _STRUCTURE_AVAILABLE = False

try:
    from metrics import analyze as analyze_metrics
    _METRICS_AVAILABLE = True
except ImportError:  # pragma: no cover
    _METRICS_AVAILABLE = False

# Grade bands wobble on short passages: one long sentence can move the whole
# figure. The readability prompt therefore needs a minimum word count before
# it means anything.
GRADE_MIN_WORDS = 100


def _keep_points(text: str, result) -> list[str]:
    """Strong choices worth preserving, derived from the text itself."""
    keeps: list[str] = []
    tokens = tokenize_words(text)
    if any("'" in sentence or "\u2019" in sentence for sentence in get_sentences(text)):
        keeps.append("Contractions present; the register commits to a voice.")
    numbers = [
        token.strip(".,;:()[]") for token in text.split()
        if any(char.isdigit() for char in token)
        and not re.fullmatch(r"\d+[.)]", token.strip())
    ]
    if numbers:
        keeps.append(f"Checkable detail present ({', '.join(numbers[:3])}); keep every figure exact.")
    if any(item.rule == "protected-content" for item in result.findings):
        keeps.append("Protected literals requested; those that survive must stay exact.")
    elif not result.findings:
        keeps.append("No gate findings; the passage may need no edit at all.")
    if not keeps:
        keeps.append("Quoted spans below name what to re-read; everything unquoted earned no flag.")
    void = [token for token in tokens if len(token) > 0]
    _ = void
    return keeps


def diagnose(text: str, genre: str, reference: str | None = None) -> dict:
    result = evaluate(text, genre)
    entry = {
        "genre": result.genre,
        "word_count": result.word_count,
        "keep": _keep_points(text, result),
        "revise": [
            {
                "rule": item.rule,
                "severity": item.severity,
                "span": item.span,
                "sentence": item.sentence,
                "reason": item.message,
            }
            for item in result.findings
        ],
        "missing": [
            {
                "rule": "bracket-slot",
                "span": item.span,
                "reason": "Detail only the writer can supply; fill from the source or ask.",
            }
            for item in result.findings if item.rule == "bracket-slot"
        ],
    }
    error_count = sum(1 for item in result.findings if item.severity == "error")
    entry["measured"] = {
        "sentences": result.counts.get("sentences"),
        "sentence_length_sd": result.counts.get("sentence_length_sd"),
        "sentence_length_cv": result.counts.get("sentence_length_cv"),
        "opener_entropy": result.counts.get("opener_entropy"),
        "max_same_opening": result.counts.get("max_same_opening"),
        "nominalizations_per_1000": result.counts.get("nominalizations_per_1000"),
        "contractions_per_1000": result.counts.get("contractions_per_1000"),
        "bracket_slots": result.counts.get("bracket_slots"),
    }
    if _STRUCTURE_AVAILABLE:
        try:
            structure = analyze_structure(text)
            entry["measured"]["burstiness"] = structure["sentence_lengths"]["burstiness"]
            entry["measured"]["participial_total"] = (
                structure["participial_clauses"]["participial_opener_count"]
                + structure["participial_clauses"].get("extended_opener_count", 0)
            )
            entry["measured"]["stock_terms_unique"] = structure["generic_vocabulary"]["unique_ai_terms"]
        except Exception:  # diagnostics must not crash the diagnosis
            pass
    if _METRICS_AVAILABLE and result.word_count >= GRADE_MIN_WORDS:
        try:
            from not_ai_core.policy import get_policy as _get_policy

            grade = analyze_metrics(text)["readability"]["flesch_kincaid_grade"]
            entry["measured"]["flesch_kincaid_grade"] = grade
            policy = _get_policy(genre)
            if grade < policy.grade_low or grade > policy.grade_high:
                entry["revise"].append({
                    "rule": "readability-mismatch",
                    "severity": "review",
                    "span": None,
                    "sentence": None,
                    "reason": (
                        f"Grade {grade} sits outside the {policy.grade_low}-{policy.grade_high} "
                        f"band usual for {genre}; check whether the density fits this reader. "
                        "Academic and technical writing legitimately run dense."
                    ),
                })
        except Exception:  # diagnostics must not crash the diagnosis
            pass
    review_count = len(entry["revise"]) - sum(
        1 for item in entry["revise"] if item["severity"] == "error"
    )
    if error_count:
        entry["intervention"] = "blocked: objective errors must be fixed first"
    elif review_count >= 7:
        entry["intervention"] = "heavy: several passages deserve a re-read"
    elif review_count >= 3:
        entry["intervention"] = "moderate: a few targeted edits"
    elif review_count >= 1:
        entry["intervention"] = "light: one or two prompts to check"
    else:
        entry["intervention"] = "none: no rewrite needed"
    if reference is not None:
        from not_ai_core.voice import compare as compare_voice

        voice = compare_voice(reference, text)
        entry["voice"] = {
            "overall": voice["overall"],
            "drifted_dimensions": voice["drifted_dimensions"],
            "notes": voice["notes"],
        }
        if voice.get("caution"):
            entry["voice"]["caution"] = voice["caution"]
    return entry


def human_report(entry: dict) -> str:
    lines = ["NOT AI : DIAGNOSIS (no rewrite performed)", "─" * 40]
    lines.append(f"Genre: {entry['genre']}  |  Words: {entry['word_count']}")
    lines.append(f"Intervention: {entry['intervention']}")
    lines.append("")
    lines.append("KEEP")
    for point in entry["keep"]:
        lines.append(f"  ✓ {point}")
    lines.append("")
    lines.append("REVISE")
    if entry["revise"]:
        for item in entry["revise"]:
            where = f" (sentence {item['sentence']})" if item["sentence"] else ""
            span = f" '{item['span']}'" if item["span"] else ""
            lines.append(f"  • [{item['severity']}] {item['rule']}{where}{span}")
            lines.append(f"    {item['reason']}")
    else:
        lines.append("  ✓ Nothing flagged.")
    lines.append("")
    lines.append("MISSING")
    if entry["missing"]:
        for item in entry["missing"]:
            lines.append(f"  • '{item['span']}': {item['reason']}")
    else:
        lines.append("  ✓ No bracketed gaps found. If a claim still lacks support, add a bracket.")
    lines.append("")
    lines.append("MEASURED")
    for key, value in entry["measured"].items():
        lines.append(f"  {key}: {value}")
    if "voice" in entry:
        voice = entry["voice"]
        lines.append("")
        lines.append(f"VOICE vs reference: {voice['overall']} ({voice['drifted_dimensions']} drifted)")
        for note in voice["notes"]:
            lines.append(f"  • {note}")
        if voice.get("caution"):
            lines.append(f"  Caution: {voice['caution']}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", nargs="?", help="Text file to diagnose")
    parser.add_argument("--stdin", action="store_true", help="Read text from stdin")
    parser.add_argument("--genre", default="linkedin", choices=sorted(POLICIES))
    parser.add_argument("--reference", default=None, help="Author reference text for voice comparison")
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
        print("Error: no text provided", file=sys.stderr)
        return 2

    reference = Path(args.reference).read_text(encoding="utf-8") if args.reference else None
    entry = diagnose(text, args.genre, reference)
    print(json.dumps(entry, indent=2, ensure_ascii=False) if args.json else human_report(entry))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
