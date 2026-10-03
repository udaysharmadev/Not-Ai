#!/usr/bin/env python3
"""Package the Not Ai skill as a portable .skill bundle for skill upload.

Usage:
    python3 scripts/package_skill.py
    python3 scripts/package_skill.py --out /tmp/not-ai.skill
    python3 scripts/package_skill.py --check   # fail when dist/ is stale or invalid

The bundle keeps the layout the skill text assumes: SKILL.md at the archive
root, reference/ beside it, and the portable tools/gate.py alongside. Repo
measurement scripts (scripts/diagnose.py and friends) stay in the
repository; the bundle covers the skill plus its deterministic gate.

Validation (Anthropic skill conventions, dependency-free):
frontmatter carries a name and description, the description fits the
trigger budget, the body stays under 500 lines, no README ships inside
the skill folder, and references stay one level deep.
"""

import argparse
import re
import sys
import zipfile
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
SKILL_DIR = ROOT / "plugins/not-ai/skills/not-ai"
TOOLS_DIR = ROOT / "plugins/not-ai/tools"
DIST = ROOT / "dist/not-ai.skill"

# Fixed timestamp so builds are byte-deterministic.
STAMP = (2026, 1, 1, 0, 0, 0)
MAX_BODY_LINES = 500
MAX_DESCRIPTION_CHARS = 1024


def read_frontmatter(skill_text: str) -> dict[str, str]:
    """Parse the --- delimited frontmatter without a YAML dependency."""
    match = re.match(r"^---\n(.*?)\n---\n", skill_text, re.DOTALL)
    if not match:
        raise ValueError("SKILL.md has no --- frontmatter block")
    fields: dict[str, str] = {}
    for line in match.group(1).splitlines():
        field = re.match(r"^([A-Za-z_]+):\s*(.*)$", line)
        if field:
            fields[field.group(1)] = field.group(2).strip()
    return fields


def validate() -> list[str]:
    """Return a list of problems; empty means the skill packages cleanly."""
    problems: list[str] = []
    skill_file = SKILL_DIR / "SKILL.md"
    if not skill_file.is_file():
        return ["canonical SKILL.md is missing"]
    text = skill_file.read_text(encoding="utf-8")
    try:
        frontmatter = read_frontmatter(text)
    except ValueError as error:
        return [str(error)]
    if not frontmatter.get("name"):
        problems.append("frontmatter has no name")
    description = frontmatter.get("description", "")
    if not description:
        problems.append("frontmatter has no description (the install-time trigger)")
    elif len(description) > MAX_DESCRIPTION_CHARS:
        problems.append(f"description is {len(description)} chars (limit {MAX_DESCRIPTION_CHARS})")
    body = text.split("---\n", 2)[-1] if text.startswith("---\n") else text
    body_lines = len(body.splitlines())
    if body_lines > MAX_BODY_LINES:
        problems.append(f"body is {body_lines} lines (limit {MAX_BODY_LINES})")
    if (SKILL_DIR / "README.md").exists():
        problems.append("README.md inside the skill folder (repo README is for humans)")
    reference = SKILL_DIR / "reference"
    if reference.is_dir():
        for path in sorted(reference.rglob("*")):
            if path.is_dir() and path != reference:
                problems.append(f"reference nested deeper than one level: {path.name}")
    if not (TOOLS_DIR / "gate.py").is_file():
        problems.append("portable tools/gate.py is missing")
    return problems


def bundle_bytes() -> bytes:
    import io

    files: list[tuple[str, Path]] = [("SKILL.md", SKILL_DIR / "SKILL.md")]
    reference = SKILL_DIR / "reference"
    if reference.is_dir():
        for path in sorted(reference.glob("*.md")):
            files.append((f"reference/{path.name}", path))
    for path in sorted((TOOLS_DIR / "not_ai_core").glob("*.py")):
        files.append((f"tools/not_ai_core/{path.name}", path))
    files.append(("tools/gate.py", TOOLS_DIR / "gate.py"))
    buffer = io.BytesIO()
    with zipfile.ZipFile(buffer, "w", zipfile.ZIP_DEFLATED) as archive:
        for arcname, path in files:
            info = zipfile.ZipInfo(arcname, STAMP)
            info.compress_type = zipfile.ZIP_DEFLATED
            archive.writestr(info, path.read_bytes())
    return buffer.getvalue()


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--out", default=str(DIST), help="Bundle destination")
    parser.add_argument("--check", action="store_true",
                        help="fail when dist/ is stale or the skill is invalid")
    args = parser.parse_args()

    problems = validate()
    if problems:
        for problem in problems:
            print(f"Invalid: {problem}", file=sys.stderr)
        return 1
    content = bundle_bytes()
    if args.check:
        out = Path(args.out)
        if not out.is_file() or out.read_bytes() != content:
            print("Skill bundle is stale. Run: python3 scripts/package_skill.py",
                  file=sys.stderr)
            return 1
        print("Skill bundle matches.")
        return 0
    out = Path(args.out)
    out.parent.mkdir(parents=True, exist_ok=True)
    out.write_bytes(content)
    print(f"Wrote {out.relative_to(ROOT)} ({len(content)} bytes)")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
