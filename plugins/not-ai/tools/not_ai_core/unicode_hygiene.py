"""Unicode hygiene for Not-AI diagnostics (canonical core module).

Defensive measurement-integrity layer, not a detector-bypass tool. This module
never inserts invisible characters and never promises lower detector scores.
It reveals characters that can make rendered text differ from the raw string,
then builds a conservative analysis-only view so style metrics are not skewed
by zero-width insertion or unusual spacing.

The original text is never mutated or overwritten by this module. Callers keep
the raw deliverable and measure a normalized working copy.

Design rules (see docs/research/unicode-zero-width.md):
- No blanket NFKC: compatibility normalization can change meaningful
  scientific/technical characters. Only separators are canonicalized and only
  invisible formatting that distorts English-facing measurements is removed.
- Contextual join controls: U+200C/U+200D are valid orthography in several
  scripts and ZWJ joins emoji sequences. Remove them only when hidden inside
  an ASCII token.
- Contextual zero-width space: U+200B is a legitimate break opportunity in
  Thai, Myanmar, Khmer, Lao, and Japanese. Strip all of it only for
  ASCII-dominant analysis; otherwise strip only ASCII-token splits.
- Presence is an encoding/tokenization fact, never evidence of authorship or
  malicious intent.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import unicodedata

ZERO_WIDTH = {
    "\u200b": "ZERO WIDTH SPACE",
    "\u2060": "WORD JOINER",
    "\ufeff": "ZERO WIDTH NO-BREAK SPACE / BOM",
    "\u00ad": "SOFT HYPHEN",
}
JOIN_CONTROLS = {
    "\u200c": "ZERO WIDTH NON-JOINER",
    "\u200d": "ZERO WIDTH JOINER",
}
BIDI_CONTROLS = {
    chr(cp): unicodedata.name(chr(cp), f"U+{cp:04X}")
    for cp in (
        0x061C, 0x200E, 0x200F,
        *range(0x202A, 0x202F),
        *range(0x2066, 0x206A),
    )
}
TAG_MIN = 0xE0000
TAG_MAX = 0xE007F


@dataclass(frozen=True)
class UnicodeFinding:
    index: int
    codepoint: str
    name: str
    kind: str
    risk: str
    embedded_in_ascii_token: bool


def _ascii_token_char(ch: str) -> bool:
    return bool(ch) and ch.isascii() and (ch.isalnum() or ch == "_")


def _embedded_in_ascii_token(text: str, index: int) -> bool:
    left = text[index - 1] if index > 0 else ""
    right = text[index + 1] if index + 1 < len(text) else ""
    return _ascii_token_char(left) and _ascii_token_char(right)


def _kind(ch: str) -> str | None:
    cp = ord(ch)
    if ch in ZERO_WIDTH:
        return "zero-width"
    if ch in JOIN_CONTROLS:
        return "join-control"
    if ch in BIDI_CONTROLS:
        return "bidi-control"
    if TAG_MIN <= cp <= TAG_MAX:
        return "tag-character"
    if ch != " " and unicodedata.category(ch) == "Zs":
        return "unicode-space"
    return None


def _ascii_dominant(text: str) -> bool:
    visible = [ch for ch in text if _kind(ch) is None and not ch.isspace()]
    if not visible:
        return False
    ascii_visible = sum(1 for ch in visible if ch.isascii())
    return ascii_visible / len(visible) >= 0.80


def scan(text: str) -> dict:
    """Return a transparent report of invisible/unusual Unicode.

    `risk` describes measurement integrity, never author intent or authorship.
    Join controls are contextual unless hidden inside an ASCII token because
    they are valid orthographic characters in several scripts and ZWJ is used
    in emoji sequences.
    """
    findings: list[UnicodeFinding] = []
    for index, ch in enumerate(text):
        kind = _kind(ch)
        if kind is None:
            continue
        embedded = _embedded_in_ascii_token(text, index)
        cp = ord(ch)

        if kind in {"bidi-control", "tag-character"}:
            risk = "review"
        elif kind == "join-control" and not embedded:
            risk = "contextual"
        elif kind == "unicode-space":
            risk = "contextual"
        else:
            risk = "warning" if embedded else "review"

        findings.append(UnicodeFinding(
            index=index,
            codepoint=f"U+{cp:04X}",
            name=unicodedata.name(
                ch,
                ZERO_WIDTH.get(ch, JOIN_CONTROLS.get(ch, "UNKNOWN")),
            ),
            kind=kind,
            risk=risk,
            embedded_in_ascii_token=embedded,
        ))

    by_kind: dict[str, int] = {}
    for item in findings:
        by_kind[item.kind] = by_kind.get(item.kind, 0) + 1

    suspicious = sum(
        1 for item in findings
        if item.risk in {"warning", "review"}
        and (
            item.embedded_in_ascii_token
            or item.kind in {"bidi-control", "tag-character"}
        )
    )
    return {
        "total": len(findings),
        "suspicious_for_analysis": suspicious,
        "by_kind": by_kind,
        "findings": [asdict(item) for item in findings],
    }


def normalize_for_analysis(text: str) -> str:
    """Build an analysis-only view resistant to invisible token splitting.

    Idempotent: normalizing an already-normalized view is a no-op. The user's
    original text is never changed; callers measure this copy.
    """
    out: list[str] = []
    ascii_dominant = _ascii_dominant(text)

    for index, ch in enumerate(text):
        kind = _kind(ch)
        if kind is None:
            out.append(ch)
            continue

        embedded = _embedded_in_ascii_token(text, index)

        if kind == "unicode-space":
            out.append(" ")
            continue

        if kind == "zero-width":
            # U+200B can be a legitimate word-break hint in languages such as
            # Thai. Strip all of it only for ASCII-dominant analysis; otherwise
            # strip only the cases hidden inside ASCII tokens.
            if (
                embedded
                or (ch == "\u200b" and ascii_dominant)
                or ch in {"\u2060", "\ufeff", "\u00ad"}
            ):
                continue
            out.append(ch)
            continue

        if kind == "join-control":
            # Preserve Persian/Arabic/Indic orthography and emoji ZWJ. Remove a
            # joiner only when it is hidden inside an ASCII identifier/word.
            if embedded:
                continue
            out.append(ch)
            continue

        if kind in {"bidi-control", "tag-character"}:
            # These affect presentation/encoding rather than visible lexical
            # content. Raw text is retained for delivery; style metrics use the
            # control-free analysis view.
            continue

        out.append(ch)

    return "".join(out)


def render_report(report: dict, *, as_json: bool = False) -> str:
    if as_json:
        return json.dumps(report, indent=2, ensure_ascii=False)

    if not report["total"]:
        return "No invisible or unusual Unicode controls found."

    lines = [
        f"Unicode findings: {report['total']} total; "
        f"{report['suspicious_for_analysis']} can distort analysis/token boundaries."
    ]
    for kind, count in sorted(report["by_kind"].items()):
        lines.append(f"  {kind}: {count}")

    for item in report["findings"][:20]:
        lines.append(
            f"  index {item['index']}: {item['codepoint']} {item['name']} "
            f"[{item['risk']}]"
        )

    if report["total"] > 20:
        lines.append(f"  ... {report['total'] - 20} more")

    return "\n".join(lines)


def main() -> int:
    import argparse
    import sys

    parser = argparse.ArgumentParser(
        description="Reveal invisible Unicode and show the analysis-normalized view."
    )
    parser.add_argument("input_file", nargs="?", help="Text file to inspect")
    parser.add_argument("--stdin", action="store_true", help="Read from stdin")
    parser.add_argument("--json", action="store_true", help="Emit JSON report")
    parser.add_argument(
        "--show-normalized",
        action="store_true",
        help="Also print the analysis-only normalized view; never overwrites input",
    )
    args = parser.parse_args()

    if args.stdin or not args.input_file:
        text = sys.stdin.read()
    else:
        with open(args.input_file, "r", encoding="utf-8") as handle:
            text = handle.read()

    report = scan(text)
    print(render_report(report, as_json=args.json))

    if args.show_normalized and not args.json:
        print("\nANALYSIS-ONLY NORMALIZED VIEW")
        print("─" * 40)
        print(normalize_for_analysis(text))

    return 0


if __name__ == "__main__":
    raise SystemExit(main())
