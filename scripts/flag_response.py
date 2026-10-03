#!/usr/bin/env python3
"""Interpret a detector flag with prevalence-conditioned math.

Usage:
    python3 scripts/flag_response.py --tpr 0.99 --fpr 0.01
    python3 scripts/flag_response.py --tpr 0.95 --fpr 0.05 --prevalence 0.05
    python3 scripts/flag_response.py --tpr 0.99 --fpr 0.01 --json

A detector's lab accuracy is not the chance a flag is correct. That chance
depends on prevalence: how common AI-assisted submissions actually are in
the flagged cohort. This script takes the detector's stated true-positive
and false-positive rates as explicit arguments (lab figures do not transfer
to short, mixed, or second-language text) and reports, across plausible
prevalences, the probability that a flagged submission is truly AI-assisted
(PPV) and the share of flags expected to be wrong (FDR).

It predicts nothing about any draft, rewrites nothing, and scores nothing.
For what vendor percentages mean and how to answer a flag with process
evidence, see plugins/not-ai/skills/not-ai/reference/detector-literacy.md.
"""

import argparse
import json
import sys

PREVALENCES = (0.01, 0.05, 0.10, 0.20, 0.50)

CHECKLIST = [
    "Freeze everything: export the report with date and version, keep file metadata and version history. Do not edit after the accusation.",
    "Preserve process artifacts: notes, outlines, annotated readings, rough drafts with timestamps, library and citation-manager trails.",
    "Keep prior samples showing stylistic continuity with the flagged piece.",
    "Be ready to explain the thesis, sources, and each citation choice from memory.",
    "Offer a supervised rewrite or oral defense of the argument.",
    "Ask in writing which tool, threshold, and false-positive rate were used.",
    "Ask whether the score alone may count as evidence under institutional policy.",
    "Ask for a second reader blind to the score, and file the appeal promptly.",
]


def ppv(tpr: float, fpr: float, prevalence: float) -> float | None:
    """Probability a flagged item is truly AI-assisted, or None if undefined.

    PPV = TPR*p / (TPR*p + FPR*(1-p)). Returns None when no flags are
    expected at all (denominator zero), rather than inventing a number.
    """
    for name, value in (("tpr", tpr), ("fpr", fpr), ("prevalence", prevalence)):
        if not isinstance(value, (int, float)) or not 0 <= value <= 1:
            raise ValueError(f"{name} must be a number between 0 and 1")
    if not 0 < prevalence < 1:
        raise ValueError("prevalence must be strictly between 0 and 1 for flag math")
    flagged = tpr * prevalence + fpr * (1 - prevalence)
    if flagged == 0:
        return None
    return tpr * prevalence / flagged


def flag_table(tpr: float, fpr: float) -> list[dict]:
    """PPV/FDR rows across plausible prevalences, per 1000 submissions."""
    rows = []
    for prevalence in PREVALENCES:
        value = ppv(tpr, fpr, prevalence)
        true_positives = tpr * prevalence * 1000
        false_positives = fpr * (1 - prevalence) * 1000
        rows.append({
            "prevalence": prevalence,
            "ppv": round(value, 3) if value is not None else None,
            "fdr": round(1 - value, 3) if value is not None else None,
            "true_positives_per_1000": round(true_positives, 1),
            "false_positives_per_1000": round(false_positives, 1),
        })
    return rows


def human_report(tpr: float, fpr: float) -> str:
    lines = ["NOT AI : FLAG MATH (interpretation aid, not a verdict)", "─" * 40]
    lines.append(f"Stated rates: TPR {tpr}  |  FPR {fpr}  (lab figures; treat as optimistic)")
    lines.append("")
    lines.append("Share of flags expected CORRECT (PPV) at each prevalence:")
    for row in flag_table(tpr, fpr):
        share = f"{row['prevalence']:.0%} AI in cohort"
        if row["ppv"] is None:
            lines.append(f"  {share}: undefined (no flags expected)")
        else:
            lines.append(
                f"  {share}: PPV {row['ppv']:.1%} correct, "
                f"FDR {row['fdr']:.1%} wrong "
                f"({row['false_positives_per_1000']:.0f} innocents per 1000)"
            )
    lines.append("")
    lines.append("Read this before quoting any row: lab rates overstate real-world")
    lines.append("performance on short, paraphrased, or second-language text, and a")
    lines.append("single prevalence is a guess. The table exists to show how violently")
    lines.append("the meaning of a flag swings with prevalence, not to bless one row.")
    lines.append("")
    lines.append("IF GENUINE WRITING WAS FLAGGED: gather process, not product.")
    for index, item in enumerate(CHECKLIST, 1):
        lines.append(f"  {index}. {item}")
    return "\n".join(lines)


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--tpr", type=float, required=True, help="Stated true-positive rate, 0-1")
    parser.add_argument("--fpr", type=float, required=True, help="Stated false-positive rate, 0-1")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    args = parser.parse_args()
    try:
        table = flag_table(args.tpr, args.fpr)
    except ValueError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps({
            "tpr": args.tpr,
            "fpr": args.fpr,
            "rows": table,
            "checklist": CHECKLIST,
        }, indent=2))
    else:
        print(human_report(args.tpr, args.fpr))
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
