#!/usr/bin/env python3
"""Blinded pairwise review for the Human Output Benchmark.

Usage:
    python3 scripts/pairwise.py --original orig.txt --a rewrite-a.txt --b rewrite-b.txt \\
        --purpose "..." --out results/round1.jsonl
    python3 scripts/pairwise.py --original orig.txt --a rewrite-a.txt --b rewrite-b.txt \\
        --out results/round1.jsonl --choice X --note "Y keeps the numbers exact"

The reviewer sees the source (labeled SOURCE, not a candidate), the stated
task, and the two candidates blinded as X and Y. The mapping of X/Y to A/B
is decided by --seed and recorded only in the output record, never on
screen. The review question is always "which needs less author correction?",
never "which seems more human?" -- the latter invites stereotyping and this
project avoids it.

Protected literals (--protect, repeatable) are shown as a present-in-X /
present-in-Y aid. That is factual assistance for fidelity review, not a
verdict: a present literal can still be used inaccurately.
"""

import argparse
import json
import random
import sys
from datetime import datetime, timezone
from pathlib import Path


def blind_pair(a_text: str, b_text: str, seed: int | None) -> tuple[dict, dict]:
    """Return ({X: text, Y: text}, {X: 'A'|'B', Y: ...}) with order by seed."""
    rng = random.Random(seed)
    order = ["A", "B"]
    rng.shuffle(order)
    texts = {"A": a_text, "B": b_text}
    labels = ["X", "Y"]
    shown = {label: texts[which] for label, which in zip(labels, order)}
    mapping = {label: which for label, which in zip(labels, order)}
    return shown, mapping


def protection_aid(text: str, protected: list[str]) -> dict[str, bool]:
    normalized = text.casefold()
    return {term: term.casefold() in normalized for term in protected}


def build_display(original: str, shown: dict, task: dict,
                  protected: list[str]) -> str:
    lines = ["NOT AI : BLIND PAIRWISE REVIEW", "─" * 40]
    if task.get("purpose"):
        lines.append(f"Purpose: {task['purpose']}")
    if task.get("audience"):
        lines.append(f"Audience: {task['audience']}")
    if task.get("genre"):
        lines.append(f"Genre: {task['genre']}")
    lines.append("")
    lines.append("SOURCE (not a candidate; judge fidelity against this):")
    lines.append(original.rstrip())
    lines.append("")
    for label in ("X", "Y"):
        lines.append(f"CANDIDATE {label}:")
        lines.append(shown[label].rstrip())
        lines.append("")
    if protected:
        lines.append("PROTECTED LITERALS (present? -- aid only, not a verdict):")
        aid_x = protection_aid(shown["X"], protected)
        aid_y = protection_aid(shown["Y"], protected)
        for term in protected:
            lines.append(f"  '{term}': X={'yes' if aid_x[term] else 'no'} "
                         f"Y={'yes' if aid_y[term] else 'no'}")
        lines.append("")
    lines.append("Which needs less author correction? Answer X, Y, tie, or flag.")
    return "\n".join(lines)


def append_record(path: Path, record: dict) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("a", encoding="utf-8") as handle:
        handle.write(json.dumps(record, ensure_ascii=False) + "\n")


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--original", required=True)
    parser.add_argument("--a", required=True, help="First candidate file")
    parser.add_argument("--b", required=True, help="Second candidate file")
    parser.add_argument("--purpose", default="")
    parser.add_argument("--audience", default="")
    parser.add_argument("--genre", default="")
    parser.add_argument("--protect", action="append", default=[],
                        help="Protected literal for the fidelity aid; repeatable")
    parser.add_argument("--seed", type=int, default=None)
    parser.add_argument("--choice", default=None, help="X, Y, tie, or flag (skips prompt)")
    parser.add_argument("--note", default="")
    parser.add_argument("--out", required=True, help="JSONL file to append the record to")
    args = parser.parse_args()

    try:
        original = Path(args.original).read_text(encoding="utf-8")
        a_text = Path(args.a).read_text(encoding="utf-8")
        b_text = Path(args.b).read_text(encoding="utf-8")
    except OSError as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    if not original.strip() or not a_text.strip() or not b_text.strip():
        print("Error: original and both candidates must be non-empty", file=sys.stderr)
        return 2

    shown, mapping = blind_pair(a_text, b_text, args.seed)
    task = {"purpose": args.purpose, "audience": args.audience, "genre": args.genre}
    print(build_display(original, shown, task, args.protect))

    choice = args.choice
    note = args.note
    if choice is None:
        try:
            choice = input("Choice [X/Y/tie/flag]: ").strip().lower()
            note = input("Note (optional): ").strip()
        except EOFError:
            print("Error: no choice given; pass --choice in scripts", file=sys.stderr)
            return 2
    choice = choice.strip().lower()
    if choice not in ("x", "y", "tie", "flag"):
        print("Error: choice must be X, Y, tie, or flag", file=sys.stderr)
        return 2

    append_record(Path(args.out), {
        "recorded_at": datetime.now(timezone.utc).isoformat(),
        "original": args.original,
        "candidates": {"A": args.a, "B": args.b},
        "seed": args.seed,
        "mapping": mapping,
        "task": task,
        "protected": args.protect,
        "choice": choice,
        "note": note,
    })
    print(f"Recorded {choice} -> {args.out} (mapping sealed in the record, not shown above)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
