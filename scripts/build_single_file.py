#!/usr/bin/env python3
"""Build the single-file skill bundle in dist/.

The combined skill lets an agent work with one file: the canonical
plugins/not-ai/skills/not-ai/SKILL.md followed by scripts/measure.py embedded
verbatim in a fenced block, as measure.py's own docstring describes. The agent
loading the bundle writes the fenced script to a temp path and runs it.

Usage:
    python3 scripts/build_single_file.py
    python3 scripts/build_single_file.py --check   # fail when dist/ is stale

The build is byte-deterministic: same inputs, same output.
"""

import argparse
import sys
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL = ROOT / "plugins/not-ai/skills/not-ai/SKILL.md"
MEASURE = ROOT / "scripts/measure.py"
DIST = ROOT / "dist/SKILL.md"


def build() -> str:
    skill = SKILL.read_text(encoding="utf-8").rstrip() + "\n"
    measure = MEASURE.read_text(encoding="utf-8").rstrip() + "\n"
    return (
        skill
        + "\n---\n\n"
        + "## Bundled measurement script\n\n"
        + "The stdlib-only `measure.py` below is embedded verbatim. Write the "
        + "fenced block to a temporary file and run it with "
        + "`python3 measure.py FILE` or `python3 measure.py FILE --json`.\n\n"
        + "```python\n"
        + measure
        + "```\n"
    )


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail when dist/ is stale")
    args = parser.parse_args()
    content = build()
    if args.check:
        if not DIST.is_file() or DIST.read_text(encoding="utf-8") != content:
            print("dist/ bundle is stale. Run: python3 scripts/build_single_file.py", file=sys.stderr)
            return 1
        print("dist/ bundle matches.")
        return 0
    DIST.parent.mkdir(parents=True, exist_ok=True)
    DIST.write_text(content, encoding="utf-8")
    print(f"Wrote {DIST.relative_to(ROOT)}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
