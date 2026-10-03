#!/usr/bin/env python3
"""Compare a draft against an author's reference voice profile.

Usage:
    python3 scripts/voice_profile.py --reference author.txt --draft draft.txt
    python3 scripts/voice_profile.py --reference author.txt --draft draft.txt --json

The reference should be genuine writing by the same author (300+ words for a
stable profile). The verdicts are editorial prompts, not authorship claims:
"drifted" means "read this dimension against the author's habits", nothing
more. A small reference produces tentative verdicts and says so.
"""

import argparse
import json
import sys
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parents[1] / "plugins/not-ai/tools"
sys.path.insert(0, str(TOOL_ROOT))

from not_ai_core.voice import compare  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--reference", required=True, help="Author's own reference text")
    parser.add_argument("--draft", help="Draft to compare (defaults to stdin)")
    parser.add_argument("--json", action="store_true", help="Emit structured JSON")
    args = parser.parse_args()

    reference = Path(args.reference).read_text(encoding="utf-8")
    if args.draft:
        draft = Path(args.draft).read_text(encoding="utf-8")
    else:
        draft = sys.stdin.read()
    if not reference.strip() or not draft.strip():
        print("Error: reference and draft must both be non-empty", file=sys.stderr)
        return 2

    result = compare(reference, draft)
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
        return 0

    print("NOT AI : VOICE COMPARISON")
    print("─" * 40)
    print(f"Reference: {result['reference_words']} words  |  Draft: {result['draft_words']} words")
    if result["caution"]:
        print(f"Caution: {result['caution']}")
    print(f"Overall: {result['overall']} ({result['drifted_dimensions']} drifted dimensions)")
    print("")
    for group in ("rhythm", "stance", "mechanics", "specificity"):
        print(group.upper())
        for key, item in result[group].items():
            mark = "✓" if item["verdict"] == "aligned" else "•" if "absent" in item["verdict"] or "introduced" in item["verdict"] else "⚠"
            print(f"  {mark} {key}: ref {item['reference']} → draft {item['draft']} ({item['verdict']})")
        print("")
    func = result["function_words"]
    mark = "✓" if func["verdict"] == "aligned" else "⚠"
    print(f"FUNCTION WORDS\n  {mark} mean gap {func['mean_abs_gap_per_1k']}/1k ({func['verdict']})")
    print(f"  opener entropy: ref {result['opener_entropy']['reference']} → draft {result['opener_entropy']['draft']}")
    if result["notes"]:
        print("\nREAD IN CONTEXT")
        for note in result["notes"]:
            print(f"  • {note}")
    print("\nDrift is a prompt to re-read, not a verdict on who wrote the draft.")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
