#!/usr/bin/env python3
"""Unicode hygiene CLI (thin wrapper around the canonical core module).

Canonical logic lives in `plugins/not-ai/tools/not_ai_core/unicode_hygiene.py`
so the portable `.skill` bundle and every bundled analysis share one
implementation. This wrapper only exposes it from `scripts/` and keeps the
`from unicode_hygiene import scan, normalize_for_analysis` import path working.
"""

import sys
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parents[1] / "plugins/not-ai/tools"
sys.path.insert(0, str(TOOL_ROOT))

from not_ai_core.unicode_hygiene import (  # noqa: E402
    BIDI_CONTROLS,
    JOIN_CONTROLS,
    TAG_MAX,
    TAG_MIN,
    ZERO_WIDTH,
    UnicodeFinding,
    normalize_for_analysis,
    render_report,
    scan,
)

__all__ = [
    "BIDI_CONTROLS",
    "JOIN_CONTROLS",
    "TAG_MAX",
    "TAG_MIN",
    "ZERO_WIDTH",
    "UnicodeFinding",
    "normalize_for_analysis",
    "render_report",
    "scan",
]


def main() -> int:
    from not_ai_core.unicode_hygiene import main as core_main

    return core_main()


if __name__ == "__main__":
    raise SystemExit(main())
