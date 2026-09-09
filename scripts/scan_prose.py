#!/usr/bin/env python3
"""
not-ai: scan_prose.py
Check this repository's own prose for leaked generator residue.

The product treats vocabulary and punctuation as contextual editorial choices,
so this check does not police either. It catches tokens that belong to a model
interface or unfinished generated artifact rather than to reader-facing prose.
Quoted specimens are removed before scanning.

The one exemption is examples/*/input.md, whose files are specimens end to end.

Usage:
    python3 scripts/scan_prose.py                    # whole repository
    python3 scripts/scan_prose.py dist/SKILL.md      # named files

Exit code 0 means no unquoted residue was found.
"""

import re
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

SKIP_WHOLE_FILE = {"input.md"}

RESIDUE = {
    "OpenAI internal citation": r"\b(?:oaicite|oai_citation|contentReference)\b",
    "tool result reference": r"\bturn\d+(?:search|view|fetch)\d+\b",
    "uploaded-file payload": r"\b(?:attached_file|ppl-ai-file-upload)\b",
    "Grok render payload": r"\bgrok_(?:card|render_citation_card_json)\b",
    "unfinished writing wrapper": r":::writing\b",
}


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
        return []
    rel = path.relative_to(REPO) if REPO in path.parents or path.parent == REPO else path
    residue_hits = []
    for i, line in enumerate(strip_specimens(path.read_text(encoding="utf-8")).split("\n"), 1):
        for name, pattern in RESIDUE.items():
            for m in re.finditer(pattern, line, re.IGNORECASE):
                a, b = max(0, m.start() - 45), m.end() + 45
                residue_hits.append(
                    f"{rel}:{i}  {name}: {m.group()}  ...{line[a:b].strip()}..."
                )
    return residue_hits


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

    residue_hits = []
    for path in targets:
        if not path.is_file():
            print(f"Error: not a file: {path}", file=sys.stderr)
            return 1
        residue_hits += scan(path)

    print(f"Files scanned: {len(targets)}")
    print(f"Generator residue in prose: {len(residue_hits)}")
    for h in residue_hits:
        print("  " + h)

    ok = not residue_hits
    print("\nRESIDUE CLEAN" if ok else "\nRESIDUE SCAN FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main(sys.argv[1:]))
