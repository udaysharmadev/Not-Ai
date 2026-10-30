"""Controlled punctuation, segmentation, and rewriting robustness engine (Not-AI 4.0).

Rebuilds the preliminary punctuation lab into a rigorous experimental framework
for studying how surface typography, sentence segmentation, lexical/syntactic
rewriting, genre conventions, and author voice interact with text parsers and
external AI-text classifiers.

Scientific & safety invariants:
- Research probes (such as dropping sentence stops or removing periods) are
  experimental conditions for measuring detector fragility, NEVER writing
  recommendations for production prose.
- Punctuation-only variants (Condition B) strictly preserve the underlying
  lexical word sequence and protect decimals, thousand-separated numbers,
  dates, times, abbreviations, initials, citations, URLs, and code spans.
- Never introduces invisible Unicode characters (zero-width spaces, joiners,
  bidi/tag controls) or homoglyphs.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
from difflib import SequenceMatcher
import hashlib
import re
from typing import Callable

from .fidelity import check_fidelity
from .punctuation import analyze_punctuation, detect_boundary_anomalies
from .text import ABBREVIATIONS, sentences, sentence_stats, words
from .unicode_hygiene import scan as scan_unicode


# Tokenization for word-sequence verification: extracts lexical and numeric
# word tokens while treating punctuation (including `.` or `...` between words)
# as separators. Protected spans (decimals, comma-grouped numbers, URLs, code)
# are guarded before punctuation transformations so `3.14` never becomes `314`.
_LEXICAL_WORD_RE = re.compile(r"[A-Za-z0-9]+(?:['-][A-Za-z0-9]+)*", re.UNICODE)

# Spans that must be protected during punctuation-only perturbations so
# factual values, decimals, abbreviations, citations, URLs, and code stay intact.
_PROTECTED_SPAN_PATTERNS = (
    re.compile(r"```.*?```", re.DOTALL),
    re.compile(r"`[^`\n]+`"),
    re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE),
    re.compile(r"\b\d+(?:[.,:/-]\d+)+%?(?:\s*(?:a\.m\.|p\.m\.))?\b", re.IGNORECASE),
    re.compile(r"\b(?:a\.m\.|p\.m\.)", re.IGNORECASE),
    re.compile(
        r"\b(?:" + "|".join(re.escape(a) for a in ABBREVIATIONS) + r")\.",
        re.IGNORECASE,
    ),
    re.compile(r"(?:\b[A-Z]\.\s*){1,4}"),
    re.compile(r"\([^()\n]{1,80}\b(?:19|20)\d{2}[a-z]?\b[^()\n]{0,40}\)"),
    re.compile(r"\[\s*\d+(?:\s*[,–-]\s*\d+)*\s*\]"),
)


def tokens(text: str) -> list[str]:
    """Return case-folded lexical/alphanumeric word sequence.

    Splits across all punctuation including tight ellipses (`Gujarat...He` ->
    `['gujarat', 'he']`) while keeping contractions and hyphenated compounds.
    """
    return [m.group(0).casefold() for m in _LEXICAL_WORD_RE.finditer(text)]


def _with_protected_spans(text: str, transform: Callable[[str], str]) -> str:
    """Apply a punctuation transform while shielding non-prosodic spans."""
    vault: list[str] = []

    def _stash(match: re.Match[str]) -> str:
        idx = len(vault)
        vault.append(match.group(0))
        return f"__NOTAI_PROT_{idx}__"

    masked = text
    for pattern in _PROTECTED_SPAN_PATTERNS:
        masked = pattern.sub(_stash, masked)

    transformed = transform(masked)

    # Restore in reverse order in case patterns nested.
    for idx in range(len(vault) - 1, -1, -1):
        transformed = transformed.replace(f"__NOTAI_PROT_{idx}__", vault[idx])
    return transformed


def verify_word_sequence(original: str, candidate: str) -> dict:
    """Verify whether `candidate` preserves the exact lexical word sequence of `original`."""
    orig_tokens = tokens(original)
    cand_tokens = tokens(candidate)
    identical = orig_tokens == cand_tokens
    # Also check that decimal/comma numbers did not lose internal punctuation.
    orig_decimals = re.findall(r"\b\d+[.,]\d+\b", original)
    cand_decimals = re.findall(r"\b\d+[.,]\d+\b", candidate)
    decimals_intact = orig_decimals == cand_decimals
    unicode_clean = scan_unicode(candidate)["total"] == 0
    return {
        "words_identical": identical and decimals_intact,
        "lexical_tokens_identical": identical,
        "decimals_intact": decimals_intact,
        "original_word_count": len(orig_tokens),
        "candidate_word_count": len(cand_tokens),
        "unicode_clean": unicode_clean,
    }


def exact_diff(before: str, after: str) -> dict:
    """Compute character-level opcodes and human-readable diff summary."""
    a = before.strip()
    b = after.strip()
    matcher = SequenceMatcher(None, a, b)
    operations: list[dict] = []
    for tag, i1, i2, j1, j2 in matcher.get_opcodes():
        if tag != "equal":
            operations.append({
                "op": tag,
                "before_span": a[i1:i2],
                "after_span": b[j1:j2],
                "before_pos": [i1, i2],
                "after_pos": [j1, j2],
            })
    seq_check = verify_word_sequence(a, b)
    return {
        "changed": a != b,
        "similarity_ratio": round(matcher.ratio(), 4),
        "operation_count": len(operations),
        "operations": operations,
        "word_sequence_check": seq_check,
    }


def _drop_one_sentence_stop(text: str) -> str:
    """Drop a single internal sentence-ending period while preserving word spacing."""
    def _op(masked: str) -> str:
        # Prefer dropping a later internal stop (matching the Modi experiment pattern
        # where an earlier stop became an ellipsis and a later stop was dropped),
        # or the first available stop if only one exists.
        matches = list(re.finditer(r"(?<=[a-z0-9\"')])\.\s+(?=[A-Z])", masked))
        if not matches:
            return masked
        target = matches[-1] if len(matches) >= 2 else matches[0]
        return masked[:target.start()] + " " + masked[target.end():]
    return _with_protected_spans(text, _op)


def _replace_stop_with_ellipsis(text: str, tight: bool = False) -> str:
    """Replace one internal sentence-ending period with an ellipsis."""
    replacement = "..." if tight else "... "
    def _op(masked: str) -> str:
        matches = list(re.finditer(r"(?<=[a-z0-9\"')])\.\s+(?=[A-Z])", masked))
        if not matches:
            return masked
        # Pick the second sentence stop if 3+ exist (as in Modi passage sentence 3),
        # otherwise the first stop.
        idx = 2 if len(matches) >= 3 else 0
        target = matches[idx]
        return masked[:target.start()] + replacement + masked[target.end():]
    return _with_protected_spans(text, _op)


def _remove_all_sentence_periods(text: str) -> str:
    """Remove sentence periods while preserving decimals, abbreviations, and URLs."""
    def _op(masked: str) -> str:
        out = re.sub(r"\.(?=\s|$|[\"')\]] )", "", masked)
        out = out.replace(".", " ")
        out = re.sub(r" {2,}", " ", out).strip()
        return out
    return _with_protected_spans(text, _op)


def _modi_composite_perturbation(text: str) -> str:
    """Apply the exact 3-part punctuation perturbation observed in the Modi case study:
    1) Replace an early internal sentence period with a tight ellipsis (`...`),
    2) Drop a later internal sentence period,
    3) Remove the final document period.
    """
    def _op(masked: str) -> str:
        matches = list(re.finditer(r"(?<=[a-z0-9\"')])\.\s+(?=[A-Z])", masked))
        out = masked
        if len(matches) >= 2:
            # Replace earlier stop with tight ellipsis and drop last internal stop
            last_m = matches[-1]
            early_m = matches[2] if len(matches) >= 4 else matches[0]
            out = (
                out[:early_m.start()]
                + "..."
                + out[early_m.end():last_m.start()]
                + " "
                + out[last_m.end():]
            )
        elif len(matches) == 1:
            m = matches[0]
            out = out[:m.start()] + "..." + out[m.end():]
        out = re.sub(r"\.\s*$", "", out)
        return out
    return _with_protected_spans(text, _op)


def punctuation_variants(text: str) -> dict[str, str]:
    """Generate the 8 core word-preserving punctuation probes (compatible with ablation.py).

    Unlike the naive prototype, all transformations protect decimals (`3.14`),
    comma-grouped numbers (`1,000`), times (`2:14 a.m.`), abbreviations (`Dr.`,
    `U.S.`), initials, citations, URLs, and code spans so lexical and numeric
    tokens are never corrupted.
    """
    stripped = text.strip()
    return {
        "control": stripped,
        "delete_commas": _with_protected_spans(
            stripped,
            lambda m: re.sub(r",\s*", " ", m),
        ),
        "delete_terminal_period": _with_protected_spans(
            stripped,
            lambda m: re.sub(r"\.$", "", m),
        ),
        "double_terminal_period": _with_protected_spans(
            stripped,
            lambda m: re.sub(r"\.$", "..", m),
        ),
        "add_extra_spaces": _with_protected_spans(
            stripped,
            lambda m: re.sub(r"(?<=[.!?]) (?=[A-Z])", "  ", m),
        ),
        "replace_sentence_stop_with_ellipsis": _replace_stop_with_ellipsis(stripped, tight=False),
        "drop_one_sentence_stop": _drop_one_sentence_stop(stripped),
        "remove_all_periods": _remove_all_sentence_periods(stripped),
    }


def _default_lexical_syntactic_rewrite(text: str) -> str:
    """Deterministic lexical/syntactic cleanup retaining the source punctuation convention."""
    out = text.strip()
    replacements = (
        (r"\bIt is worth noting that\s+", ""),
        (r"\bIt is important to note that\s+", ""),
        (r"\bIn today's fast-paced world,\s*", ""),
        (r"\bFurthermore,\s+", ""),
        (r"\bMoreover,\s+", ""),
        (r"\bAdditionally,\s+", ""),
        (r"\bIn conclusion,\s+", ""),
        (r"\butilize\b", "use"),
        (r"\butilizes\b", "uses"),
        (r"\butilized\b", "used"),
        (r"\butilizing\b", "using"),
        (r"\bfacilitate\b", "help"),
        (r"\bfacilitates\b", "helps"),
        (r"\bserves as\b", "is"),
        (r"\bstands as\b", "is"),
        (r"\bfunctions as\b", "is"),
        (r"\ba big part of\b", "central to"),
        (r"\bmore needs to be done about\b", "policy should address"),
    )
    for pattern, repl in replacements:
        out = re.sub(pattern, repl, out, flags=re.IGNORECASE)
    # Fix capitalization at sentence starts if an opener was stripped.
    out = re.sub(
        r"(^|(?<=[.!?]\s))([a-z])",
        lambda m: m.group(1) + m.group(2).upper(),
        out,
    )
    return out


def _sentence_segmentation_variant(text: str) -> str:
    """Create a controlled sentence-segmentation variant (Condition F).

    Splits a long coordinated clause (`... and he/they/it/people ...`) into two
    sentences, or joins two adjacent short sentences with a semicolon, changing
    sentence segmentation boundaries while keeping the claims intact.
    """
    stripped = text.strip()
    # Try splitting a long coordinated sentence on `, and ` or ` and ` before a subject.
    split_match = re.search(
        r"(?<=[a-z]{3}),?\s+and\s+(?=(?:he|she|they|we|it|people|the|many|some|this)\b)",
        stripped,
    )
    if split_match:
        after = stripped[split_match.end():]
        if after:
            cap_after = after[0].upper() + after[1:]
            return stripped[:split_match.start()] + ". " + cap_after
    # Otherwise, join the first two sentences with a semicolon.
    join_match = re.search(r"(?<=[a-z])\.\s+(?=[A-Z][a-z]+\b)", stripped)
    if join_match:
        next_char = stripped[join_match.end():join_match.end() + 1]
        # Only lowercase if not 'I' or a proper noun heuristic
        word_after = re.match(r"[A-Za-z]+", stripped[join_match.end():])
        w_str = word_after.group(0) if word_after else ""
        if w_str in {"He", "She", "They", "We", "It", "This", "These", "Those", "Some", "Many", "But", "And"}:
            return (
                stripped[:join_match.start()]
                + "; "
                + next_char.lower()
                + stripped[join_match.end() + 1:]
            )
        return stripped[:join_match.start()] + "; " + stripped[join_match.end():]
    return stripped


def _genre_aware_editorial_variant(text: str, genre: str = "linkedin") -> str:
    """Produce a genre-aware editorial revision (Condition G).

    Repairs boundary damage (such as tight ellipses or missing terminal stops
    in formal genres) and applies clean clause punctuation without introducing
    artificial errors.
    """
    cleaned = _default_lexical_syntactic_rewrite(text.strip())
    # Repair tight ellipses (`Gujarat...He` -> `Gujarat. He`)
    cleaned = re.sub(r"(?<=[A-Za-z])(?:\.\.\.+|\u2026)\s*(?=[A-Z])", ". ", cleaned)
    # Repair double terminal periods
    cleaned = re.sub(r"(?<!\.)\.\.(?!\.)", ".", cleaned)
    # Repair fused sentence boundaries (`rising prices He has` -> `rising prices. He has`)
    cleaned = re.sub(
        r"\b([a-z]{4,})\s+(He|She|They|We|However|Moreover|Furthermore|Therefore)\s+(is|are|was|were|has|have|had)\b",
        r"\1. \2 \3",
        cleaned,
    )
    if genre.lower() not in {"social", "x"} and cleaned and cleaned[-1] not in ".!?\"')]}":
        cleaned += "."
    return cleaned


def generate_experimental_conditions(
    text: str,
    *,
    genre: str = "linkedin",
    lexical_rewrite: str | None = None,
    editorial_rewrite: str | None = None,
    voice_rewrite: str | None = None,
) -> dict[str, dict]:
    """Generate the full 8-condition experimental suite (Conditions A through H).

    Conditions:
    - A_control: Original unchanged text.
    - B_punctuation_only: Word-preserving punctuation modifications (includes
      individual probes B1..B6 plus B7_modi_composite).
    - C_lexical_syntactic: Lexical/syntactic rewrite maintaining equivalent
      punctuation convention.
    - D_combined_edits: Lexical/syntactic rewrite combined with punctuation
      perturbation (completing the 2x2 factorial design A/B/C/D).
    - E_whitespace_only: Controlled whitespace modification (double spaces after
      sentence stops) with words and punctuation unchanged.
    - F_sentence_segmentation: Sentence boundary segmentation variation.
    - G_genre_aware_editorial: Genre-aware editorial improvement (natural
      prosody, repaired boundaries, zero manufactured errors).
    - H_voice_matched: Real-author voice-matched revision (when supplied or
      derived from reference habits).
    """
    stripped = text.strip()
    b_probes = punctuation_variants(stripped)
    b_composite = _modi_composite_perturbation(stripped)
    c_text = (lexical_rewrite.strip() if lexical_rewrite else _default_lexical_syntactic_rewrite(stripped))
    d_text = _modi_composite_perturbation(c_text)
    e_text = b_probes["add_extra_spaces"]
    f_text = _sentence_segmentation_variant(stripped)
    g_text = (editorial_rewrite.strip() if editorial_rewrite else _genre_aware_editorial_variant(stripped, genre))
    h_text = (voice_rewrite.strip() if voice_rewrite else g_text)

    raw_conditions = {
        "A_control": {
            "condition_code": "A",
            "label": "Original unchanged text (Control)",
            "preserves_word_sequence_by_design": True,
            "is_production_safe": True,
            "text": stripped,
        },
        "B1_delete_commas": {
            "condition_code": "B1",
            "label": "Punctuation-only: remove clause commas (numbers protected)",
            "preserves_word_sequence_by_design": True,
            "is_production_safe": False,
            "text": b_probes["delete_commas"],
        },
        "B2_delete_terminal_period": {
            "condition_code": "B2",
            "label": "Punctuation-only: remove final document period",
            "preserves_word_sequence_by_design": True,
            "is_production_safe": genre.lower() in {"social", "x"},
            "text": b_probes["delete_terminal_period"],
        },
        "B3_double_terminal_period": {
            "condition_code": "B3",
            "label": "Punctuation-only: double terminal period (..)",
            "preserves_word_sequence_by_design": True,
            "is_production_safe": False,
            "text": b_probes["double_terminal_period"],
        },
        "B4_replace_stop_with_ellipsis": {
            "condition_code": "B4",
            "label": "Punctuation-only: replace one sentence stop with ellipsis",
            "preserves_word_sequence_by_design": True,
            "is_production_safe": False,
            "text": b_probes["replace_sentence_stop_with_ellipsis"],
        },
        "B5_drop_one_sentence_stop": {
            "condition_code": "B5",
            "label": "Punctuation-only: drop one internal sentence-ending period",
            "preserves_word_sequence_by_design": True,
            "is_production_safe": False,
            "text": b_probes["drop_one_sentence_stop"],
        },
        "B6_remove_all_periods": {
            "condition_code": "B6",
            "label": "Punctuation-only: remove all sentence periods (decimals protected)",
            "preserves_word_sequence_by_design": True,
            "is_production_safe": False,
            "text": b_probes["remove_all_periods"],
        },
        "B_punctuation_only": {
            "condition_code": "B",
            "label": "Punctuation-only composite (ellipsis + dropped stop + dropped terminal period)",
            "preserves_word_sequence_by_design": True,
            "is_production_safe": False,
            "text": b_composite,
        },
        "C_lexical_syntactic": {
            "condition_code": "C",
            "label": "Lexical/syntactic rewrite with equivalent punctuation convention",
            "preserves_word_sequence_by_design": False,
            "is_production_safe": True,
            "text": c_text,
        },
        "D_combined_edits": {
            "condition_code": "D",
            "label": "Combined lexical/syntactic rewrite + punctuation perturbation (2x2 cell)",
            "preserves_word_sequence_by_design": False,
            "is_production_safe": False,
            "text": d_text,
        },
        "E_whitespace_only": {
            "condition_code": "E",
            "label": "Controlled visible whitespace change (words and punctuation unchanged)",
            "preserves_word_sequence_by_design": True,
            "is_production_safe": True,
            "text": e_text,
        },
        "F_sentence_segmentation": {
            "condition_code": "F",
            "label": "Controlled sentence segmentation boundary variation",
            "preserves_word_sequence_by_design": False,
            "is_production_safe": True,
            "text": f_text,
        },
        "G_genre_aware_editorial": {
            "condition_code": "G",
            "label": "Genre-aware editorial improvement (Not-AI 4.0 natural prose)",
            "preserves_word_sequence_by_design": False,
            "is_production_safe": True,
            "text": g_text,
        },
        "H_voice_matched": {
            "condition_code": "H",
            "label": "Author voice-matched revision",
            "preserves_word_sequence_by_design": False,
            "is_production_safe": True,
            "text": h_text,
        },
    }

    enriched: dict[str, dict] = {}
    for name, item in raw_conditions.items():
        impact = measure_variant_impact(
            stripped,
            item["text"],
            genre=genre,
            expect_word_preservation=item["preserves_word_sequence_by_design"],
        )
        if item["preserves_word_sequence_by_design"] and not impact["word_sequence_preserved"]:
            raise ValueError(f"Word-preserving condition '{name}' altered lexical tokens.")
        enriched[name] = {
            **item,
            "sha256": hashlib.sha256(item["text"].encode("utf-8")).hexdigest(),
            "impact": impact,
        }
    return enriched


def measure_variant_impact(
    original: str,
    variant: str,
    *,
    genre: str = "linkedin",
    expect_word_preservation: bool = False,
) -> dict:
    """Measure how a variant alters sentence parsing, prosodic features, and grammatical integrity."""
    diff_info = exact_diff(original, variant)
    seq_check = diff_info["word_sequence_check"]

    orig_sents = sentences(original)
    var_sents = sentences(variant)
    orig_lengths = [len(words(s)) for s in orig_sents]
    var_lengths = [len(words(s)) for s in var_sents]
    orig_stats = sentence_stats(orig_lengths)
    var_stats = sentence_stats(var_lengths)

    orig_punct = analyze_punctuation(original, genre)
    var_punct = analyze_punctuation(variant, genre)
    var_bounds = detect_boundary_anomalies(variant, genre)
    fidelity = check_fidelity(original, variant)

    damages_grammar = bool(
        var_bounds["fused_sentences"]
        or var_bounds["tight_ellipsis_boundaries"]
        or var_bounds["double_periods"]
        or var_bounds["unbalanced_parentheses"]
        or (var_bounds["terminal_omission_status"] == "boundary_loss")
        or (orig_punct["counts"]["periods"] > 0 and var_punct["counts"]["periods"] == 0 and len(orig_sents) >= 2)
    )
    damages_clarity = bool(
        damages_grammar
        or (orig_punct["counts"]["commas"] >= 3 and var_punct["counts"]["commas"] == 0)
    )
    damages_meaning = not fidelity["passed"] or not seq_check["decimals_intact"]

    mechanisms: list[str] = []
    if len(var_sents) != len(orig_sents):
        mechanisms.append(
            f"sentence_segmentation_shift ({len(orig_sents)} -> {len(var_sents)} sentences)"
        )
    if abs(var_stats["cv"] - orig_stats["cv"]) >= 0.05:
        mechanisms.append(
            f"burstiness_cv_shift ({orig_stats['cv']:.3f} -> {var_stats['cv']:.3f})"
        )
    if var_bounds["tight_ellipsis_boundaries"]:
        mechanisms.append("subword_token_concatenation_at_tight_ellipsis")
    if var_bounds["fused_sentences"]:
        mechanisms.append("run_on_boundary_surprisal_spike")
    if orig_punct["counts"]["total_marks"] != var_punct["counts"]["total_marks"]:
        mechanisms.append(
            f"punctuation_mark_delta ({orig_punct['counts']['total_marks']} -> {var_punct['counts']['total_marks']})"
        )

    return {
        "changed": diff_info["changed"],
        "word_sequence_preserved": seq_check["words_identical"],
        "expect_word_preservation": expect_word_preservation,
        "word_count_before": seq_check["original_word_count"],
        "word_count_after": seq_check["candidate_word_count"],
        "punctuation_marks_before": orig_punct["counts"]["total_marks"],
        "punctuation_marks_after": var_punct["counts"]["total_marks"],
        "sentence_count_before": len(orig_sents),
        "sentence_count_after": len(var_sents),
        "sentence_lengths_before": orig_lengths,
        "sentence_lengths_after": var_lengths,
        "sentence_sd_before": orig_stats["sd"],
        "sentence_sd_after": var_stats["sd"],
        "sentence_cv_before": orig_stats["cv"],
        "sentence_cv_after": var_stats["cv"],
        "sentence_cv_delta": round(var_stats["cv"] - orig_stats["cv"], 3),
        "clause_cv_before": orig_punct["prosody"]["clause_length_cv"],
        "clause_cv_after": var_punct["prosody"]["clause_length_cv"],
        "punctuation_entropy_before": orig_punct["punctuation_entropy"],
        "punctuation_entropy_after": var_punct["punctuation_entropy"],
        "damages_grammar": damages_grammar,
        "damages_clarity": damages_clarity,
        "damages_meaning": damages_meaning,
        "fidelity_passed": fidelity["passed"],
        "fidelity_violations": fidelity["violations"],
        "boundary_anomalies": var_bounds,
        "detector_sensitivity_mechanisms": mechanisms,
        "diff": diff_info,
    }
