#!/usr/bin/env python3
"""Run the Not Ai deterministic, genre-aware pre-output gate."""

import argparse
from pathlib import Path
import sys

from not_ai_core.gate import EXPLANATIONS, evaluate, render
from not_ai_core.policy import POLICIES


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", nargs="?", help="Text file to evaluate")
    parser.add_argument("--stdin", action="store_true", help="Read text from standard input")
    parser.add_argument("--genre", default="linkedin", choices=sorted(POLICIES))
    parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    parser.add_argument(
        "--ascii-punctuation",
        action="store_true",
        help="Enforce an explicitly requested ASCII-only house style",
    )
    parser.add_argument(
        "--protect",
        action="append",
        default=[],
        metavar="TEXT",
        help="Require this literal text in the deliverable; may be repeated",
    )
    parser.add_argument(
        "--explain",
        nargs="?",
        const=True,
        default=False,
        metavar="RULE",
        help="Append research notes (all reported rules), or explain one RULE: --explain nominalization-review",
    )
    args = parser.parse_args()
    # Provenance mode: `gate.py draft.txt --explain <rule>` prints the shared
    # rule/evidence block without needing findings on the input text.
    if isinstance(args.explain, str):
        from not_ai_core.rules import explain as explain_rule
        print(explain_rule(args.explain))
        return 0
    if args.stdin or not args.input_file:
        text = sys.stdin.read()
    else:
        path = Path(args.input_file)
        if not path.is_file():
            print(f"Error: file not found: {path}", file=sys.stderr)
            return 2
        text = path.read_text(encoding="utf-8")
    result = evaluate(
        text,
        args.genre,
        ascii_punctuation=args.ascii_punctuation,
        protected_terms=args.protect,
    )
    print(render(result, args.json))
    if args.explain and not args.json and result.findings:
        from not_ai_core.rules import explain as explain_rule
        print("\nrule notes (provenance from shared rule/evidence metadata):")
        for rule in dict.fromkeys(item.rule for item in result.findings):
            print(f"\n{explain_rule(rule)}")
    return 0 if result.passed else 1


if __name__ == "__main__":
    raise SystemExit(main())
