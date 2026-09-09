#!/usr/bin/env python3
"""Repository entry point for the portable plugin pre-output gate."""

import runpy
import sys
from pathlib import Path

TOOL_ROOT = Path(__file__).resolve().parents[1] / "plugins/not-ai/tools"
sys.path.insert(0, str(TOOL_ROOT))
runpy.run_path(str(TOOL_ROOT / "gate.py"), run_name="__main__")
