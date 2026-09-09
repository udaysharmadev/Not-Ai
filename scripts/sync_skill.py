#!/usr/bin/env python3
"""Synchronize the local Claude skill copy from the canonical plugin skill."""

import argparse
from pathlib import Path
import sys


ROOT = Path(__file__).resolve().parents[1]
SOURCE = ROOT / "plugins/not-ai/skills/not-ai/SKILL.md"
DESTINATION = ROOT / ".claude/skills/not-ai.md"


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail when the local copy is stale")
    args = parser.parse_args()
    source = SOURCE.read_text(encoding="utf-8")
    if args.check:
        if DESTINATION.read_text(encoding="utf-8") != source:
            print("Local Claude skill is stale. Run: python3 scripts/sync_skill.py", file=sys.stderr)
            return 1
        print("Skill copies match.")
        return 0
    DESTINATION.parent.mkdir(parents=True, exist_ok=True)
    DESTINATION.write_text(source, encoding="utf-8")
    print(f"Updated {DESTINATION.relative_to(ROOT)} from {SOURCE.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
