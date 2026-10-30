"""Portable, dependency-free analysis primitives for the Not Ai plugin (Not-AI 4.0)."""

from .evaluation import (
    analyze_score_sheet,
    bootstrap_ci,
    check_vendor_length_eligibility,
    evaluate_passage_pair,
    load_score_rows,
)
from .gate import EXPLANATIONS, GateResult, evaluate
from .intervention import select_intervention
from .punctuation import analyze_punctuation, compare_punctuation_voice, prosody_profile
from .robustness import (
    exact_diff,
    generate_experimental_conditions,
    measure_variant_impact,
    punctuation_variants,
    tokens,
    verify_word_sequence,
)
from .voice import compare as compare_voice
from .voice import profile as voice_profile

__all__ = [
    "EXPLANATIONS",
    "GateResult",
    "analyze_punctuation",
    "analyze_score_sheet",
    "bootstrap_ci",
    "check_vendor_length_eligibility",
    "compare_punctuation_voice",
    "compare_voice",
    "evaluate",
    "evaluate_passage_pair",
    "exact_diff",
    "generate_experimental_conditions",
    "load_score_rows",
    "measure_variant_impact",
    "prosody_profile",
    "punctuation_variants",
    "select_intervention",
    "tokens",
    "verify_word_sequence",
    "voice_profile",
]
