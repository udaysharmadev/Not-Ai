"""Intervention planner and 7-layer natural-writing selector (Not-AI 4.0).

Determines editorial workload from actual need across seven layers:
  Layer 1: Source understanding & protected ledger
  Layer 2: Writing structure & discourse cohesion
  Layer 3: Lexical and syntactic quality
  Layer 4: Natural punctuation and prosody
  Layer 5: Author voice (when genuine reference samples exist)
  Layer 6: Meaning and fidelity verification
  Layer 7: Human-centered editorial review (ISO 24495-1 plain language)

Levels: NONE / LIGHT / MODERATE / HEAVY / RESTRUCTURE / BLOCKED_BY_MISSING_INFORMATION.
Regression fixtures with expected NONE must return the source unchanged.
"""

from __future__ import annotations

from typing import Iterable


LEVELS = ("NONE", "LIGHT", "MODERATE", "HEAVY", "RESTRUCTURE", "BLOCKED_BY_MISSING_INFORMATION")
MODES = ("rewrite", "preserve", "diagnose", "from-notes", "voice-match")


def plan(*, errors: int = 0, reviews: int = 0, missing_info_blocked: bool = False,
         global_restructure: bool = False, punctuation_damage: int = 0,
         cohesion_fragmented: bool = False, mode: str = "rewrite") -> dict:
    if missing_info_blocked or errors:
        level = "BLOCKED_BY_MISSING_INFORMATION" if missing_info_blocked else "HEAVY"
        if errors and not missing_info_blocked:
            # Objective errors must be fixed first, but that is not automatically
            # a restructure; keep HEAVY unless global signals say otherwise.
            level = "HEAVY" if not global_restructure else "RESTRUCTURE"
        return {
            "level": level,
            "short_level": "BLOCKED" if missing_info_blocked else level,
            "mode": mode,
            "reason": "objective errors or missing information block normal editing",
        }
    if global_restructure or cohesion_fragmented:
        return {
            "level": "RESTRUCTURE",
            "short_level": "RESTRUCTURE",
            "mode": mode,
            "reason": "global map or discourse review shows duplicated/contradicted sections, fragmented cohesion, or lost definitions",
        }
    effective_reviews = reviews + punctuation_damage
    if effective_reviews == 0:
        return {
            "level": "NONE",
            "short_level": "NONE",
            "mode": mode,
            "reason": "no findings; already-good writing stays unchanged",
        }
    if mode == "preserve":
        return {
            "level": "LIGHT" if effective_reviews <= 4 else "MODERATE",
            "short_level": "LIGHT" if effective_reviews <= 4 else "MODERATE",
            "mode": mode,
            "reason": "preserve mode: make only the minimum targeted edits needed for clarity and boundary repair",
        }
    if effective_reviews <= 2:
        return {"level": "LIGHT", "short_level": "LIGHT", "mode": mode, "reason": "one or two targeted prompts"}
    if effective_reviews <= 6:
        return {"level": "MODERATE", "short_level": "MODERATE", "mode": mode, "reason": "a few targeted edits"}
    return {"level": "HEAVY", "short_level": "HEAVY", "mode": mode, "reason": "several passages deserve re-reading"}


def diagnose_to_reviews(diagnose_entry: dict) -> int:
    return sum(1 for item in diagnose_entry.get("revise", [])
               if item.get("severity") != "error")


def select_intervention(
    text: str,
    *,
    genre: str = "linkedin",
    mode: str = "rewrite",
    reference: str | None = None,
    protected_terms: Iterable[str] = (),
) -> dict:
    """Run the 7-layer Not-AI 4.0 natural-writing assessment and select an intervention plan."""
    if mode not in MODES:
        raise ValueError(f"Unknown mode '{mode}'. Choose one of: {', '.join(MODES)}")

    from .cultural import detect_variety
    from .discourse import cohesion
    from .fidelity import extract_ledger
    from .gate import evaluate
    from .information_structure import document_map, editorial_questions
    from .lexical import lexical_profile, phrase_patterns
    from .plain_language import review as plain_review
    from .punctuation import analyze_punctuation
    from .syntax import syntax_profile
    from .unicode_hygiene import normalize_for_analysis, scan as scan_unicode

    hygiene = scan_unicode(text)
    clean_text = normalize_for_analysis(text)
    gate_res = evaluate(clean_text, genre, protected_terms=protected_terms)

    # Layer 1: Source understanding
    ledger = extract_ledger(text)
    variety = detect_variety(clean_text)
    bracket_count = int(gate_res.counts.get("bracket_slots", 0))

    # Layer 2: Writing structure & discourse
    coh = cohesion(clean_text)
    doc_map = document_map(clean_text)
    questions = editorial_questions(clean_text)

    # Layer 3: Lexical & syntactic quality
    lex = lexical_profile(clean_text)
    phrases = phrase_patterns(clean_text)
    syn = syntax_profile(clean_text)

    # Layer 4: Natural punctuation & prosody
    punct = analyze_punctuation(clean_text, genre)

    # Layer 5: Author voice
    voice_summary = None
    if reference and reference.strip():
        from .voice import compare as compare_voice
        from .punctuation import compare_punctuation_voice
        voice_summary = {
            "stylometric": compare_voice(normalize_for_analysis(reference), clean_text),
            "punctuation": compare_punctuation_voice(normalize_for_analysis(reference), clean_text, genre),
        }

    # Layer 6: Meaning & fidelity readiness
    errors = sum(1 for f in gate_res.findings if f.severity == "error")
    missing_blocked = (mode == "from-notes" and gate_res.word_count < 8) or (bracket_count >= 3)

    # Layer 7: Human-centered editorial review
    plain = plain_review(clean_text, genre)

    gate_reviews = sum(1 for f in gate_res.findings if f.severity != "error")
    punct_damage = sum(
        1 for f in punct["findings"]
        if f["category"] in {"boundary_integrity", "genre_fit"}
    )
    global_restructure = (
        coh.get("assessment") == "fragmented"
        or doc_map["roles"].count("conclusion") >= 2
        or coh.get("repeated_conclusions", 0) >= 1
    )

    selected = plan(
        errors=errors,
        reviews=gate_reviews,
        missing_info_blocked=missing_blocked,
        global_restructure=global_restructure,
        punctuation_damage=punct_damage,
        cohesion_fragmented=(coh.get("assessment") == "fragmented"),
        mode=mode,
    )

    return {
        "level": selected["level"],
        "short_level": selected["short_level"],
        "mode": mode,
        "genre": gate_res.genre,
        "word_count": gate_res.word_count,
        "reason": selected["reason"],
        "layers": {
            "layer_1_source": {
                "ledger": ledger,
                "variety": variety,
                "bracket_slots": bracket_count,
            },
            "layer_2_structure": {
                "cohesion": coh,
                "paragraph_roles": doc_map["roles"],
                "given_new_breaks": doc_map["flow"]["count"],
            },
            "layer_3_lexical_syntactic": {
                "lexical": lex,
                "phrase_patterns": phrases,
                "syntax": syn,
            },
            "layer_4_punctuation_prosody": punct,
            "layer_5_voice": voice_summary,
            "layer_6_fidelity_invariants": {
                "gate_passed": gate_res.passed,
                "protected_numbers": ledger["numbers"],
                "protected_quotes_count": len(ledger["quotes"]),
                "protected_citations_count": len(ledger["citations"]),
            },
            "layer_7_editorial_review": {
                "plain_language": plain,
                "editorial_questions": questions,
                "unicode_hygiene": hygiene,
            },
        },
    }
