"""Portable, dependency-free analysis primitives for the Not Ai plugin."""

from .gate import EXPLANATIONS, GateResult, evaluate
from .voice import compare as compare_voice
from .voice import profile as voice_profile

__all__ = ["EXPLANATIONS", "GateResult", "compare_voice", "evaluate", "voice_profile"]
