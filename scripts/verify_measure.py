#!/usr/bin/env python3
"""
not-ai: verify_measure.py
Parity check between scripts/measure.py and the three scripts it condenses.

Why this exists: the single-file build of this skill embeds measure.py instead of
analyze_structure.py, metrics.py and repetition.py. Every figure quoted in
examples/*/rationale.md and in README.md came from the originals. If the
condensed version measured even slightly differently, every table in the
repository would stop reproducing, and the failure would be silent.

So this compares the full JSON output of measure.analyze() against the merged
JSON output of the three originals, on every markdown file in the repository.
measure.analyze() must be a strict superset: every key the originals emit must be
present with an identical value. Extra keys are allowed, since the condensed
script prints one combined report.

Usage:
    python3 scripts/verify_measure.py
    python3 scripts/verify_measure.py --verbose

Exit code 0 means every shared figure matches on every file.
"""

import argparse
import importlib.util
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = REPO / "scripts"


def load(name):
    spec = importlib.util.spec_from_file_location(name, SCRIPTS / f"{name}.py")
    module = importlib.util.module_from_spec(spec)
    sys.modules[name] = module
    spec.loader.exec_module(module)
    return module


def repo_markdown():
    """Every markdown file that belongs to the repository, in a stable order.

    Two exclusions keep the reported file count reproducible. `dist/` holds
    generated output, so only the built SKILL.md counts there: a scratch file
    left beside it should not change what this script reports. Empty files are
    skipped because there is nothing in them to measure.
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


def flatten(obj, prefix=""):
    """Flatten nested dicts to dotted paths so a diff names the exact figure."""
    flat = {}
    if isinstance(obj, dict):
        for k, v in obj.items():
            flat.update(flatten(v, f"{prefix}.{k}" if prefix else str(k)))
    elif isinstance(obj, (list, tuple)):
        flat[prefix] = repr(obj)
    else:
        flat[prefix] = obj
    return flat


def compare(expected, actual, source):
    """Every key in expected must exist in actual with an equal value."""
    mismatches = []
    exp, act = flatten(expected), flatten(actual)
    for key, want in exp.items():
        if key not in act:
            mismatches.append((source, key, want, "<missing>"))
        elif act[key] != want:
            mismatches.append((source, key, want, act[key]))
    return mismatches


def main():
    ap = argparse.ArgumentParser(description="Verify measure.py matches the originals")
    ap.add_argument("--verbose", action="store_true",
                    help="Print every file checked, not just failures")
    args = ap.parse_args()

    structure = load("analyze_structure")
    metrics = load("metrics")
    repetition = load("repetition")
    measure = load("measure")

    targets = repo_markdown()
    if not targets:
        print("Error: no markdown files found to check", file=sys.stderr)
        return 1

    all_mismatches = []
    checked = 0
    for path in targets:
        text = path.read_text(encoding="utf-8")
        if not text.strip():
            continue
        rel = path.relative_to(REPO)
        got = measure.analyze(text)
        for mod in (structure, metrics, repetition):
            want = mod.analyze(text)
            all_mismatches += compare(want, got, f"{rel} [{mod.__name__}]")
        checked += 1
        if args.verbose:
            print(f"  checked {rel}")

    # A report is only trustworthy if it also reproduces. Compare the combined
    # human-readable output against the three originals line by line, ignoring
    # lines the condensed script adds.
    sample = REPO / "examples" / "gen-ai-article" / "input.md"
    report_note = ""
    if sample.is_file():
        text = sample.read_text(encoding="utf-8")
        original_lines = set()
        for mod in (structure, metrics, repetition):
            original_lines |= {l.strip() for l in
                               mod.human_readable_summary(mod.analyze(text)).split("\n")
                               if l.strip()}
        combined = {l.strip() for l in
                    measure.report(measure.analyze(text)).split("\n") if l.strip()}
        # Header lines and section labels differ by design; figure lines must not.
        figure_lines = {l for l in original_lines
                        if any(c.isdigit() for c in l) and not l.startswith("─")}
        dropped = sorted(l for l in figure_lines if l not in combined)
        if dropped:
            report_note = (f"\n{len(dropped)} figure line(s) from the original reports "
                           f"are absent from the combined report:\n" +
                           "\n".join(f"  {l}" for l in dropped))

    print(f"Files checked: {checked}")
    print(f"Figure mismatches: {len(all_mismatches)}")
    for source, key, want, got in all_mismatches[:40]:
        print(f"  {source}\n    {key}: expected {want!r}, got {got!r}")
    if len(all_mismatches) > 40:
        print(f"  ... and {len(all_mismatches) - 40} more")
    if report_note:
        print(report_note)

    ok = not all_mismatches and not report_note
    print("\nPARITY OK" if ok else "\nPARITY FAILED")
    return 0 if ok else 1


if __name__ == "__main__":
    sys.exit(main())
