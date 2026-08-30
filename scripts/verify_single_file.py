#!/usr/bin/env python3
"""
not-ai: verify_single_file.py
Check that dist/SKILL.md is a faithful and self-sufficient build.

A single-file build fails quietly. It loads, it looks complete, and three
paragraphs in it tells the agent to read a file that is not there. These are the
checks that catch that:

  1. Frontmatter parses, and carries a name and a description. The host rejects
     the skill outright without both.
  2. Every source file is present, matched on a distinctive line from each.
  3. Every backticked repository path resolves to a heading in the document, or
     is a path the build deliberately drops.
  4. Heading hierarchy is well formed: nothing past level 6, no skipped levels.
  5. Code fences balance, which is the failure mode of inlining files that
     contain fences into a file that contains fences.
  6. Prose passes the dash and vocabulary scan under the specimen convention.
  7. The embedded measurer extracts, runs, and still agrees with the originals.

Usage:
    python3 scripts/verify_single_file.py
    python3 scripts/verify_single_file.py --file dist/SKILL.md
"""

import argparse
import re
import subprocess
import sys
import tempfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

# Paths the build intentionally does not inline. Naming them here rather than
# ignoring unresolved paths wholesale keeps check 3 meaningful. The three
# original measurement scripts appear because the examples cite the exact
# commands that produced their figures, and those commands run in the multi-file
# repository, not here.
EXPECTED_ABSENT = {
    "scripts/analyze_structure.py", "scripts/metrics.py", "scripts/repetition.py",
    "scripts/benchmark.py", "scripts/_shared.py", "scripts/build_single_file.py",
    "scripts/verify_single_file.py", "scripts/verify_measure.py",
    "scripts/scan_prose.py", "scripts/verify_checks.py", "scan_prose.py",
    "analyze_structure.py", "metrics.py", "repetition.py", "benchmark.py",
    "_shared.py", "measure.py",
    "benchmarks/README.md", "README.md", "SKILL.md", "LICENSE",
    "input.md", "output.md", "sample.md",
    "dist/SKILL.md", "benchmarks/results", "voice.md",
}

results = []


def check(name, ok, detail=""):
    results.append((name, ok, detail))
    print(f"  {'PASS' if ok else 'FAIL'}  {name}")
    if detail and not ok:
        for line in detail.rstrip().split("\n")[:12]:
            print(f"          {line}")


def check_frontmatter(text):
    m = re.match(r"^---\n(.*?\n)---\n", text, re.DOTALL)
    if not m:
        check("frontmatter block present", False, "no leading --- ... --- block")
        return
    block = m.group(1)
    fields = dict(re.findall(r"^([a-zA-Z_]+):\s*(.+)$", block, re.M))
    check("frontmatter has name", "name" in fields, f"keys found: {list(fields)}")
    check("frontmatter has description", "description" in fields,
          f"keys found: {list(fields)}")
    if "name" in fields:
        check("frontmatter name is not-ai", fields["name"].strip() == "not-ai",
              f"got {fields['name']!r}")
    if "description" in fields:
        n = len(fields["description"].strip())
        check("description length under 1024", n < 1024, f"{n} characters")

    # The real hazard is not a second frontmatter block, which no parser reads,
    # but a --- line directly under a non-blank line: that is setext syntax and
    # silently turns the paragraph above it into a heading.
    body = text[m.end():]
    lines = body.split("\n")
    setext = []
    fence = None
    for i, line in enumerate(lines):
        marker = re.match(r"`{3,}", line.lstrip())
        if marker:
            if fence is None:
                fence = marker.group(0)
            elif len(marker.group(0)) >= len(fence):
                fence = None
            continue
        if fence is not None:
            continue
        if re.match(r"^-{3,}\s*$", line) and i > 0 and lines[i - 1].strip():
            setext.append(f"line {i}: {lines[i-1].strip()[:60]}")
    check("no accidental setext headings under --- rules", not setext,
          "\n".join(setext))


def check_completeness(text):
    sources = (sorted((REPO / "rules").glob("*.md"))
               + sorted((REPO / "references").glob("*.md")))
    for d in sorted((REPO / "examples").iterdir()):
        if d.is_dir():
            sources += sorted(d.glob("*.md"))
    sources.append(REPO / "scripts" / "measure.py")

    missing_heading, missing_body = [], []
    for src in sources:
        rel = src.relative_to(REPO).as_posix()
        if f"{rel}" not in text:
            missing_heading.append(rel)
            continue
        body = src.read_text(encoding="utf-8")
        # Longest non-heading, non-blank line is distinctive enough to prove the
        # body was carried over, and survives heading shifts and fencing.
        candidates = [l.strip() for l in body.split("\n")
                      if l.strip() and not l.lstrip().startswith(("#", "`", "|"))]
        if candidates and max(candidates, key=len) not in text:
            missing_body.append(rel)
    check(f"all {len(sources)} source files referenced", not missing_heading,
          "\n".join(missing_heading))
    check("all source bodies present", not missing_body, "\n".join(missing_body))


def check_paths_resolve(text):
    """A cited path resolves if some heading in the document names it.

    Headings carry a prefix in a few places, for example
    'Appendix D. scripts/measure.py', so this matches on containment. Bare
    filenames with no directory resolve against heading basenames, which is how
    the examples cite each other.
    """
    headings = [h.strip() for h in re.findall(r"^#{1,6}\s+(.+?)\s*$", text, re.M)]
    basenames = {h.rstrip("/").rsplit("/", 1)[-1] for h in headings}
    cited = set(re.findall(r"`([A-Za-z0-9_./-]+\.(?:md|py|json|txt))`", text))
    cited |= {m.rstrip("/") for m in re.findall(r"`(examples/[A-Za-z0-9_-]+/)`", text)}

    unresolved = []
    for p in sorted(cited):
        if p in EXPECTED_ABSENT:
            continue
        if any(p in h for h in headings):
            continue
        if "/" not in p and p in basenames:
            continue
        unresolved.append(p)
    check("every cited repository path resolves to a section", not unresolved,
          "\n".join(unresolved))

    # A relative markdown link points at a file that does not exist beside this
    # document. The build converts them to backticked paths; any survivor is dead.
    dangling, fence = [], None
    for i, line in enumerate(text.split("\n"), 1):
        marker = re.match(r"`{3,}", line.lstrip())
        if marker:
            if fence is None:
                fence = marker.group(0)
            elif len(marker.group(0)) >= len(fence):
                fence = None
            continue
        if fence is not None:
            continue
        for m in re.finditer(r"\[([^\]]+)\]\(([^)]+)\)", re.sub(r"`[^`]*`", " ", line)):
            target = m.group(2)
            if not target.startswith(("http://", "https://", "#", "mailto:")):
                dangling.append(f"line {i}: {m.group(0)[:70]}")
    check("no dangling relative markdown links", not dangling, "\n".join(dangling))


def check_headings(text):
    levels = []
    fence = None
    for line in text.split("\n"):
        marker = re.match(r"`{3,}", line.lstrip())
        if marker:
            if fence is None:
                fence = marker.group(0)
            elif len(marker.group(0)) >= len(fence):
                fence = None
            continue
        if fence is not None:
            continue
        m = re.match(r"^(#{1,7})\s", line)
        if m:
            levels.append((len(m.group(1)), line.strip()[:70]))
    too_deep = [h for lvl, h in levels if lvl > 6]
    check("no heading past level 6", not too_deep, "\n".join(too_deep))
    skips = []
    for i in range(1, len(levels)):
        if levels[i][0] > levels[i - 1][0] + 1:
            skips.append(f"{levels[i-1][1]}  ->  {levels[i][1]}")
    check("no skipped heading levels", not skips, "\n".join(skips))
    check("exactly one level-1 heading",
          sum(1 for lvl, _ in levels if lvl == 1) == 1,
          f"found {sum(1 for lvl, _ in levels if lvl == 1)}")


def check_fences(text):
    depth, opener, unclosed = 0, None, 0
    for line in text.split("\n"):
        m = re.match(r"`{3,}", line.lstrip())
        if not m:
            continue
        if depth == 0:
            depth, opener = 1, m.group(0)
        elif len(m.group(0)) >= len(opener):
            depth, opener = 0, None
    unclosed = depth
    check("code fences balance", unclosed == 0, f"{unclosed} unclosed fence")


def check_prose(path):
    proc = subprocess.run(
        [sys.executable, str(REPO / "scripts" / "scan_prose.py"), str(path)],
        capture_output=True, text=True)
    check("prose scan clean (dashes and AI vocabulary)", proc.returncode == 0,
          proc.stdout + proc.stderr)


def check_embedded_script(text):
    blocks = re.findall(r"^```python\n(.*?)^```", text, re.S | re.M)
    if not blocks:
        check("embedded python block found", False, "no ```python fence")
        return
    script = max(blocks, key=len)
    check("embedded python block found", True)
    with tempfile.TemporaryDirectory() as tmp:
        target = Path(tmp) / "measure.py"
        target.write_text(script, encoding="utf-8")
        sample = REPO / "examples" / "gen-ai-article" / "input.md"
        proc = subprocess.run([sys.executable, str(target), str(sample)],
                              capture_output=True, text=True)
        check("extracted measurer runs", proc.returncode == 0,
              proc.stderr or proc.stdout)
        if proc.returncode == 0:
            # The figures Appendix C quotes for this example. Chosen to span the
            # formulas: token count, sentence variance, the nominalization proxy,
            # the transition list, all three readability scores and the density
            # score. A change to any one of them breaks this check.
            expected = ["Words: 99", "Sentences: 5", "burstiness: 0.388",
                        "70.7 per 1,000 words", "Mechanical transitions: 3",
                        "Flesch-Kincaid Grade:  17.2", "Gunning Fog Index:     21.3",
                        "Flesch Reading Ease:   7.3", "Density score: 53.5"]
            absent = [e for e in expected if e not in proc.stdout]
            check("extracted measurer reproduces the quoted figures", not absent,
                  "absent: " + ", ".join(absent))
        identical = script.strip() == (
            REPO / "scripts" / "measure.py").read_text(encoding="utf-8").strip()
        check("embedded script matches scripts/measure.py", identical,
              "the build inlined a stale copy")


def main():
    ap = argparse.ArgumentParser(description="Verify the single-file build")
    ap.add_argument("--file", default="dist/SKILL.md")
    args = ap.parse_args()

    path = REPO / args.file
    if not path.is_file():
        print(f"Error: {args.file} not found. Run scripts/build_single_file.py first.",
              file=sys.stderr)
        return 1
    text = path.read_text(encoding="utf-8")

    # WORD_PATTERN from _shared.py, so this count matches the build script's.
    word_count = len(re.findall(r"\b[a-zA-Z]+\b", text))
    print(f"Verifying {args.file}")
    print(f"  {len(text.encode('utf-8')):,} bytes  |  "
          f"{word_count:,} words  |  "
          f"{len(text.splitlines()):,} lines\n")

    check_frontmatter(text)
    check_completeness(text)
    check_paths_resolve(text)
    check_headings(text)
    check_fences(text)
    check_prose(path)
    check_embedded_script(text)

    failed = [n for n, ok, _ in results if not ok]
    print(f"\n{len(results) - len(failed)} of {len(results)} checks passed")
    print("SINGLE FILE OK" if not failed else "SINGLE FILE FAILED")
    return 0 if not failed else 1


if __name__ == "__main__":
    sys.exit(main())
