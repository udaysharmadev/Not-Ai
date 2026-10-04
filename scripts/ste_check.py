#!/usr/bin/env python3
"""STE-inspired / verified technical review (Not-AI 3.0).

Usage:
    python3 scripts/ste_check.py file.txt --mode inspired
    python3 scripts/ste_check.py file.txt --mode verify --dictionary PATH --glossary PATH

`inspired` applies publicly documented principles and always reports
"STE-inspired / provisional". `verify` checks against the user's own authorised
ASD-STE100 Issue 9 dictionary + project glossary and never claims compliance —
only consistency with the supplied resources. The official STEMG standard remains
the authority; no dictionary material is bundled here.
"""

import argparse
import json
import sys
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parents[1] / "plugins/not-ai/tools"
sys.path.insert(0, str(TOOL_ROOT))

from not_ai_core.ste import check_inspired, check_verify  # noqa: E402


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("input_file", help="Technical text to review")
    parser.add_argument("--mode", default="inspired", choices=["inspired", "verify"])
    parser.add_argument("--dictionary", default=None, help="Authorised Issue 9 dictionary file (verify mode)")
    parser.add_argument("--glossary", default=None, help="Project glossary: approved technical nouns/verbs (verify mode)")
    parser.add_argument("--json", action="store_true")
    args = parser.parse_args()

    path = Path(args.input_file)
    if not path.is_file():
        print(f"Error: file not found: {path}", file=sys.stderr)
        return 2
    text = path.read_text(encoding="utf-8")
    if not text.strip():
        print("Error: no text provided", file=sys.stderr)
        return 2
    try:
        entry = check_verify(text, args.dictionary, args.glossary) if args.mode == "verify" else check_inspired(text)
    except (FileNotFoundError, ValueError) as error:
        print(f"Error: {error}", file=sys.stderr)
        return 2
    if args.json:
        print(json.dumps(entry, indent=2, ensure_ascii=False))
        return 0
    print(f"NOT AI : STE {entry['mode'].upper()} REVIEW (provisional — not compliance)")
    print("─" * 50)
    if not entry["findings"]:
        print("No findings. This is not an ASD-STE100 compliance claim.")
    for item in entry["findings"]:
        where = f" (sentence {item['sentence']})" if item.get("sentence") else ""
        print(f"  • [{item['rule']}]{where} '{item.get('span','')}'")
        print(f"    {item.get('note','')}")
    print(f"\n{entry.get('disclaimer','')}")
    if entry["mode"] == "verify":
        print(f"Checked against: {entry.get('checked_against', {})}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
