#!/usr/bin/env python3
"""
not-ai: scan_prose.py
Check this repository's own prose against the rules it teaches.

A file that argues against `leveraging` is indistinguishable from a file that
uses it, unless the citations are marked. This repository marks them: every
specimen sits inside one of four markers, a fenced code block, inline backticks,
a `> ` blockquote line, or double quotation marks. This script strips those four
and scans what is left, which is the repository speaking in its own voice.

Two exemptions, both narrow and both deliberate:
  * examples/*/input.md are specimens end to end, so they are skipped whole.
  * A single em dash in rules/structure.md is the worked example in the em dash
    rule, and it sits inside a blockquote, so the stripper already removes it.

Usage:
    python3 scripts/scan_prose.py                    # whole repository
    python3 scripts/scan_prose.py dist/SKILL.md      # named files

Exit code 0 means the repository does not do what it tells others not to do.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

SKIP_WHOLE_FILE = {"input.md"}

DASHES = (("—", "em dash"), ("–", "en dash"))

# Patterns, not substrings: \belevate would fire on the legitimate "elevated".
TELLS = [
    r"delve", r"tapestry", r"landscape of", r"navigat\w+ the", r"realm",
    r"multifaceted", r"myriad", r"leverag(?:e|es|ing)", r"holistic",
    r"paradigm shift", r"cutting-edge", r"seamless", r"unlock", r"harness",
    r"foster", r"embark", r"ever-evolving", r"at the forefront",
    r"shed light on", r"deep dive", r"elevate(?![d\b])|elevating",
    r"revolutionize", r"pave the way", r"testament to",
    r"underscores the importance", r"pivotal role", r"crucial role",
    r"it is important to note", r"in today's fast-paced", r"resonate with",
    r"profound impact", r"double-edged sword", r"the intersection of",
    r"a beacon", r"stark reminder", r"nuanced", r"comprehensive",
    r"utiliz(?:e|es|ing)", r"furthermore", r"moreover",
]


def strip_specimens(text):
    """Blank every span where the repository is quoting rather than writing.

    Lines are replaced rather than deleted so reported line numbers stay true.
    """
    out, fence = [], None
    for line in text.split("\n"):
        stripped = line.lstrip()
        marker = re.match(r"`{3,}", stripped)
        if marker:
            if fence is None:
                fence = marker.group(0)
            elif len(marker.group(0)) >= len(fence):
                fence = None
            out.append("")
            continue
        if fence is not None or stripped.startswith(">"):
            out.append("")
            continue
        line = re.sub(r"`[^`]*`", " ", line)
        line = re.sub(r'"[^"]*"', " ", line)
        line = re.sub(r"“[^”]*”", " ", line)
        out.append(line)
    return "\n".join(out)


def scan(path):
    if path.name in SKIP_WHOLE_FILE:
        return [], []
    rel = path.relative_to(REPO) if REPO in path.parents or path.parent == REPO else path
    dash_hits, tell_hits = [], []
    for i, line in enumerate(strip_specimens(path.read_text(encoding="utf-8")).split("\n"), 1):
        for ch, name in DASHES:
            if ch in line:
                dash_hits.append(f"{rel}:{i}  {name}: {line.strip()[:100]}")
        low = line.lower()
        for tell in TELLS:
            for m in re.finditer(r"\b(?:" + tell + r")", low):
                a, b = max(0, m.start() - 45), m.end() + 45
                tell_hits.append(f"{rel}:{i}  {m.group()}  ...{line[a:b].strip()}...")
    return dash_hits, tell_hits


def repo_markdown():
    """Every markdown file that belongs to the repository, in a stable order.

    `dist/` holds generated output, so only the built SKILL.md counts there: a
    scratch file left beside it should not change what this script reports.
    Empty files hold no prose to scan.
    """
    keep = []
    for path in sorted(REPO.rglob("*.md")):
        if ".git" in path.parts:
            continue
        if "dist" in path.parts and path.name != "SKILL.md":
            continue
        if path.stat().st_size == 0:
            continue
        keep.append(path)
    return keep


def main(argv):
    if argv:
        targets = [Path(a).resolve() for a in argv]
    else:
        targets = repo_markdown()

    dash_hits, tell_hits = [], []
    for path in targets:
        if not path.is_file():
            print(f"Error: not a file: {path}", file=sys.stderr)
            return 1
        d, t = scan(path)
        dash_hits += d
        tell_hits += t

    print(f"Files scanned: {len(targets)}")
    print(f"Dashes in prose: {len(dash_hits)}")
    for h in dash_hits:
        print("  " + h)
    print(f"AI-tell vocabulary in prose: {len(tell_hits)}")
    for h in tell_hits:
        print("  " + h)

    ok = not dash_hits and not tell_hits
    print("\nPROSE CLEAN" if ok else "\nPROSE SCAN FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
