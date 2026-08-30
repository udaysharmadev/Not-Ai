#!/usr/bin/env python3
"""
not-ai: build_single_file.py
Generate dist/SKILL.md, a single-file build of the whole skill.

The multi-file repository is canonical. This script exists because some hosts can
only save a skill as one SKILL.md, and a hand-maintained copy would drift from
the original within a week. Nothing here is written by hand: every section is
read from the file it names, so regenerating after any edit is the only step
needed to keep the two in sync.

What it does:
  * takes the frontmatter and body of SKILL.md unchanged, except for the three
    passages that only make sense with a filesystem (the reference map preamble,
    the Stage 1 command block, and one line that says "scripts" where the build
    has a single script)
  * appends every rules/ file, every references/ file and all six examples/
    verbatim, each under a heading that is literally its repository path, so an
    agent that searches the combined file for `rules/context.md` lands on it
  * shifts inlined headings down so the document keeps one hierarchy
  * fences the six examples/*/input.md files, which are specimens of the writing
    this skill repairs and would otherwise put unquoted em dashes and flagged
    vocabulary into the skill's own prose
  * embeds scripts/measure.py in a fenced block, since a single file cannot ship
    an executable sibling

Usage:
    python3 scripts/build_single_file.py
    python3 scripts/build_single_file.py --out some/other/SKILL.md

Run scripts/verify_single_file.py afterwards. The build is not finished until it
passes.
"""

import argparse
import re
import sys
import zipfile
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent

RULES = ["context", "structure", "rhythm", "specificity", "rhetoric",
         "vocabulary", "voice"]
REFERENCES = ["wikipedia-signs", "style-research", "writing-research", "methodology"]
EXAMPLES = ["gen-ai-article", "academic-abstract", "linkedin-post",
            "technical-passage", "personal-essay", "already-natural"]
EXAMPLE_FILES = ["README.md", "input.md", "diagnostic.md", "output.md", "rationale.md"]

# ─── SKILL.md body rewrites ──────────────────────────────────────────────────
# Each of these must match exactly once. A silent no-op here would ship a body
# telling the agent to run scripts that the single file does not contain.

BODY_SUBSTITUTIONS = [
    (
        "Load a file when its stage calls for it. Do not read them all up front.",
        "Load a section when its stage calls for it. Do not read them all up "
        "front.\n\nThis is the single-file build, so every file named below is a "
        "section of this document rather than a separate file. The section "
        "headings are the repository paths, so searching this file for "
        "`rules/context.md` finds the section that file became.",
    ),
    (
        "Run the scripts. They are deterministic and dependency-free, and they "
        "keep the diagnostic from becoming an impression.\n\n"
        "```bash\n"
        "python3 scripts/analyze_structure.py input.md\n"
        "python3 scripts/repetition.py input.md\n"
        "python3 scripts/metrics.py input.md\n"
        "```",
        "Measure before judging. The measurement is deterministic and "
        "dependency-free, and it keeps the diagnostic from becoming an "
        "impression.\n\n"
        "This build carries the measurement script as text, under "
        "`scripts/measure.py` below. Write that block to a file and run it:\n\n"
        "```bash\n"
        "python3 measure.py input.md\n"
        "python3 measure.py input.md --json\n"
        "```\n\n"
        "It needs Python 3.10 and nothing else. It reports the same figures as "
        "the three scripts in the multi-file repository, so the before-and-after "
        "tables in the examples below reproduce against it.",
    ),
    (
        "Where the scripts cannot run, count by hand.",
        "Where the script cannot run, count by hand.",
    ),
    (
        "Run the scripts on the output, not only on the input.\n\n"
        "```bash\n"
        "python3 scripts/analyze_structure.py output.md\n"
        "python3 scripts/repetition.py output.md\n"
        "python3 scripts/metrics.py output.md\n"
        "python3 scripts/scan_prose.py output.md\n"
        "```",
        "Run the measurement on the output, not only on the input.\n\n"
        "```bash\n"
        "python3 measure.py output.md\n"
        "```\n\n"
        "This build does not carry `scan_prose.py`, so the dash count and the "
        "flagged-vocabulary sweep of the delivered text are done by reading, "
        "against the list in the `rules/vocabulary.md` section below.",
    ),
]


def read(rel):
    path = REPO / rel
    if not path.is_file():
        raise SystemExit(f"Error: missing required file: {rel}")
    return path.read_text(encoding="utf-8")


def split_frontmatter(text):
    match = re.match(r"^---\n(.*?\n)---\n", text, re.DOTALL)
    if not match:
        raise SystemExit("Error: SKILL.md has no YAML frontmatter block")
    return match.group(0), text[match.end():].lstrip("\n")


def shift_headings(text, target_top):
    """Push every ATX heading down so the file's own top level lands on target_top."""
    levels = [len(m.group(1)) for m in re.finditer(r"^(#{1,6})\s", text, re.M)]
    if not levels:
        return text
    shift = target_top - min(levels)
    if shift <= 0:
        return text
    deepest = max(levels) + shift
    if deepest > 6:
        raise SystemExit(f"Error: heading shift would exceed level 6 (would reach "
                         f"{deepest}). Flatten the source headings first.")

    def bump(m):
        return "#" * (len(m.group(1)) + shift) + m.group(2)

    return re.sub(r"^(#{1,6})(\s)", bump, text, flags=re.M)


def fence(text, language="text"):
    """Wrap text in a fence long enough to survive any fence inside it."""
    longest = max((len(m.group(0)) for m in re.finditer(r"^`{3,}", text, re.M)),
                  default=0)
    bar = "`" * max(3, longest + 1)
    return f"{bar}{language}\n{text.rstrip()}\n{bar}"


def absolutize_links(text, directory):
    """Turn sibling markdown links into backticked repository paths.

    The example READMEs link to their siblings as [input.md](input.md). In one
    file those links point nowhere, so they become `examples/<name>/input.md`,
    which is the same convention the reference map uses and which the section
    headings answer to. Links inside inline code are left alone: one of them is a
    specimen of a Gemini citation artifact, not a link.
    """
    def replace(m):
        before = text[:m.start()]
        if before.count("`") % 2:
            return m.group(0)
        return f"`{directory}/{m.group(2)}`"

    return re.sub(r"\[([^\]]+)\]\(([A-Za-z0-9_.-]+\.md)\)", replace, text)


def section(path_label, body, fenced=False):
    out = [f"### {path_label}", ""]
    out.append(fence(body) if fenced else shift_headings(body.strip(), 4))
    out.append("")
    return "\n".join(out)


def build():
    parts = []

    frontmatter, body = split_frontmatter(read("SKILL.md"))
    for old, new in BODY_SUBSTITUTIONS:
        if body.count(old) != 1:
            raise SystemExit(
                f"Error: body substitution matched {body.count(old)} times, "
                f"expected exactly 1. SKILL.md changed and this script needs "
                f"updating. Passage begins: {old[:60]!r}")
        body = body.replace(old, new)

    parts.append(frontmatter.rstrip())
    parts.append("")
    parts.append(GENERATED_NOTE.strip())
    parts.append("")
    parts.append(body.rstrip())
    parts.append("")

    parts.append("## Appendix A. Rules")
    parts.append("")
    parts.append("Seven rule sections, loaded per stage. `rules/context.md` comes "
                 "first because a genre error makes every later judgment wrong in "
                 "the same direction.")
    parts.append("")
    for name in RULES:
        parts.append(section(f"rules/{name}.md", read(f"rules/{name}.md")))

    parts.append("## Appendix B. References")
    parts.append("")
    parts.append("Background rather than instruction. `references/methodology.md` "
                 "holds the honest limits, including the measures in this "
                 "repository that are known to point the wrong way.")
    parts.append("")
    for name in REFERENCES:
        parts.append(section(f"references/{name}.md", read(f"references/{name}.md")))

    parts.append("## Appendix C. Worked examples")
    parts.append("")
    parts.append(EXAMPLES_PREAMBLE.strip())
    parts.append("")
    for name in EXAMPLES:
        parts.append(f"### examples/{name}/")
        parts.append("")
        for filename in EXAMPLE_FILES:
            rel = f"examples/{name}/{filename}"
            text = read(rel)
            if filename == "input.md":
                parts.append(f"#### {rel}")
                parts.append("")
                parts.append("Specimen. Fenced so that its em dashes and flagged "
                             "vocabulary stay quoted rather than becoming this "
                             "document's own prose.")
                parts.append("")
                parts.append(fence(text))
                parts.append("")
            else:
                parts.append(f"#### {rel}")
                parts.append("")
                parts.append(shift_headings(
                    absolutize_links(text.strip(), f"examples/{name}"), 5))
                parts.append("")

    parts.append("## Appendix D. scripts/measure.py")
    parts.append("")
    parts.append(MEASURE_PREAMBLE.strip())
    parts.append("")
    parts.append(fence(read("scripts/measure.py"), "python"))
    parts.append("")

    return "\n".join(parts).rstrip() + "\n"


GENERATED_NOTE = """
> Generated file. This is the whole skill assembled into one document, built from
> the multi-file repository by `scripts/build_single_file.py`. Edit the source
> files and rebuild rather than editing this. The appendices below are the
> `rules/`, `references/` and `examples/` directories inlined, plus the
> measurement script as text.
"""

EXAMPLES_PREAMBLE = """
Six examples, each with the draft, the diagnostic, the rewrite and the reasoning.
Read `examples/gen-ai-article/` first: it shows both the correct output and the
plausible, well-written, entirely fabricated output that an earlier version of
this skill produced, which is the failure the three overriding rules exist to
prevent. Read `examples/already-natural/` second, because its correct answer is
to change nothing.

Commands quoted inside these examples refer to the multi-file repository. Every
figure they report reproduces under `scripts/measure.py` below.
"""

MEASURE_PREAMBLE = """
The measurement pass, as text. Write it to a file and run `python3 measure.py
FILE`. Python 3.10, standard library only.

It reports the same numbers as `analyze_structure.py`, `metrics.py` and
`repetition.py` in the multi-file repository, checked file by file by
`scripts/verify_measure.py`, so the before-and-after tables in Appendix C
reproduce against it.

Two things to hold in mind before quoting any figure it prints. Its
nominalization and participial measures are regex proxies, so they are
comparable to another run of this script and never to the tagged per-1,000-token
rates in Appendix B. And it measures a file, not a deliverable: a flag block or a
bracketed slot is counted as prose, which is why the `gen-ai-article` output
still reports flagged vocabulary it does not use.
"""


def main():
    ap = argparse.ArgumentParser(description="Build the single-file skill")
    ap.add_argument("--out", default="dist/SKILL.md",
                    help="Output path, relative to the repository root")
    ap.add_argument("--no-archive", action="store_true",
                    help="Skip dist/not-ai.skill")
    args = ap.parse_args()

    text = build()
    out = REPO / args.out
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_text(text, encoding="utf-8")

    # WORD_PATTERN from _shared.py, so this count matches every other word
    # count in the repository. len(text) is characters; bytes need the encode.
    words = len(re.findall(r"\b[a-zA-Z]+\b", text))
    print(f"Wrote {args.out}")
    print(f"  {len(text.encode('utf-8')):,} bytes  |  {words:,} words  |  "
          f"{len(text.splitlines()):,} lines")
    print(f"  {len(RULES)} rule sections, {len(REFERENCES)} references, "
          f"{len(EXAMPLES)} examples, 1 embedded script")

    if not args.no_archive:
        # A .skill archive holding exactly one file. A host that cannot save a
        # multi-file skill rejects the archive if anything else is in it, so
        # write the member directly rather than zipping a directory.
        archive = REPO / "dist" / "not-ai.skill"
        with zipfile.ZipFile(archive, "w", zipfile.ZIP_DEFLATED) as zf:
            zf.writestr("SKILL.md", text)
        with zipfile.ZipFile(archive) as zf:
            members = zf.namelist()
        if members != ["SKILL.md"]:
            raise SystemExit(f"Error: archive holds {members}, expected "
                             f"['SKILL.md'] only")
        print(f"Wrote dist/not-ai.skill  ({archive.stat().st_size:,} bytes, "
              f"1 member: SKILL.md)")

    print("\nNow run: python3 scripts/verify_single_file.py")
    return 0


if __name__ == "__main__":
    sys.exit(main())
