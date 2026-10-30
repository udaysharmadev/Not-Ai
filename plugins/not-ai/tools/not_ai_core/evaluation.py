"""Evaluation and benchmark statistics engine (Not-AI 4.0).

Provides deterministic, reproducible evaluation across:
1. Detector score stability under controlled transformations (from manual or
   permissioned CSV/JSON score imports — never scraped or fabricated).
2. Human-written false-positive rate (FPR) stratified by genre, length, and
   English variety.
3. Between-detector disagreement on identical passages.
4. 2x2 factorial decomposition (lexical/syntactic rewrite vs punctuation edit).
5. Factual preservation, grammatical integrity, edit distance, discourse
   coherence, voice similarity, and readability across short and long strata.
6. Minimum word-count eligibility guards (e.g. official Turnitin AI writing
   reports require >=300 words of long-form prose).
"""

from __future__ import annotations

import csv
from difflib import SequenceMatcher
import math
from pathlib import Path
import random
from statistics import median, pstdev
from typing import Iterable

from .cultural import detect_variety, preservation_check
from .discourse import cohesion
from .fidelity import check_fidelity
from .information_structure import given_new_flow
from .lexical import lexical_profile
from .plain_language import review as plain_language_review
from .punctuation import analyze_punctuation, compare_punctuation_voice
from .robustness import measure_variant_impact, tokens, verify_word_sequence
from .voice import compare as compare_voice


# Documented minimum word counts for commercial / institutional detectors.
VENDOR_MIN_WORDS: dict[str, int] = {
    "turnitin": 300,
    "turnitin_official": 300,
    "gptzero": 250,
    "crossplag": 250,
    "originality": 100,
    "zerogpt": 50,
    "third_party_aggregator": 50,
}


def length_stratum(word_count: int) -> str:
    """Classify passage length into short (<150), medium (150-299), or long (>=300)."""
    if word_count < 150:
        return "short_under_150"
    if word_count < 300:
        return "medium_150_299"
    return "long_300_plus"


def check_vendor_length_eligibility(word_count: int, detector_name: str = "") -> dict:
    """Check whether a passage meets the documented minimum length for a detector."""
    key = detector_name.strip().lower().replace(" ", "_")
    min_words = VENDOR_MIN_WORDS.get(key, 0)
    turnitin_eligible = word_count >= VENDOR_MIN_WORDS["turnitin"]
    eligible = word_count >= min_words if min_words else True
    caution = None
    if not eligible:
        caution = (
            f"Passage has {word_count} words, below {detector_name}'s documented "
            f"minimum of {min_words} words. Treat any reported score as out-of-spec."
        )
    elif not turnitin_eligible and "turnitin" in key:
        caution = (
            f"Passage has {word_count} words (<300); official Turnitin AI Writing Reports "
            "require at least 300 words of long-form prose."
        )
    return {
        "word_count": word_count,
        "stratum": length_stratum(word_count),
        "detector": detector_name or "unspecified",
        "documented_min_words": min_words,
        "eligible_for_detector": eligible,
        "eligible_for_official_turnitin": turnitin_eligible,
        "caution": caution,
    }


def word_edit_distance_ratio(text_a: str, text_b: str) -> dict:
    """Compute normalized word-sequence edit distance and character similarity."""
    toks_a = tokens(text_a)
    toks_b = tokens(text_b)
    word_matcher = SequenceMatcher(None, toks_a, toks_b)
    char_matcher = SequenceMatcher(None, text_a.strip(), text_b.strip())
    word_sim = word_matcher.ratio()
    char_sim = char_matcher.ratio()
    return {
        "word_sequence_similarity": round(word_sim, 4),
        "word_edit_distance_norm": round(1.0 - word_sim, 4),
        "char_similarity": round(char_sim, 4),
        "char_edit_distance_norm": round(1.0 - char_sim, 4),
        "words_identical": toks_a == toks_b,
    }


def bootstrap_ci(
    values: list[float],
    *,
    rounds: int = 400,
    seed: int = 42,
    stat: str = "mean",
) -> dict:
    """Compute deterministic percentile bootstrap 95% confidence interval."""
    clean = [float(v) for v in values if v is not None and not math.isnan(float(v))]
    n = len(clean)
    if n == 0:
        return {"n": 0, "estimate": None, "ci95_low": None, "ci95_high": None}
    fn = median if stat == "median" else (lambda xs: sum(xs) / len(xs))
    point = fn(clean)
    if n < 2:
        return {
            "n": n,
            "statistic": stat,
            "estimate": round(point, 3),
            "ci95_low": round(point, 3),
            "ci95_high": round(point, 3),
            "note": "single observation; CI collapses to point estimate",
        }
    rng = random.Random(seed)
    draws: list[float] = []
    for _ in range(rounds):
        sample = [rng.choice(clean) for _ in range(n)]
        draws.append(fn(sample))
    draws.sort()
    lo = draws[int(0.025 * rounds)]
    hi = draws[int(0.975 * rounds)]
    return {
        "n": n,
        "statistic": stat,
        "estimate": round(point, 3),
        "sd": round(pstdev(clean), 3),
        "ci95_low": round(lo, 3),
        "ci95_high": round(hi, 3),
    }


def evaluate_passage_pair(
    original: str,
    candidate: str,
    *,
    genre: str = "linkedin",
    reference_voice: str | None = None,
    protected_facts: Iterable[str] = (),
    true_origin: str = "unknown",
) -> dict:
    """Evaluate a (source, candidate) pair across all 10 quality, fidelity, and prosody dimensions."""
    impact = measure_variant_impact(original, candidate, genre=genre)
    fidelity = check_fidelity(original, candidate, list(protected_facts))
    cultural = preservation_check(original, candidate)
    orig_coh = cohesion(original)
    cand_coh = cohesion(candidate)
    orig_flow = given_new_flow(original)
    cand_flow = given_new_flow(candidate)
    orig_plain = plain_language_review(original, genre)
    cand_plain = plain_language_review(candidate, genre)
    orig_lex = lexical_profile(original)
    cand_lex = lexical_profile(candidate)
    edit_dist = word_edit_distance_ratio(original, candidate)
    length_info = check_vendor_length_eligibility(impact["word_count_after"])

    voice_eval = None
    if reference_voice and reference_voice.strip():
        voice_eval = {
            "stylometric": compare_voice(reference_voice, candidate),
            "punctuation_voice": compare_punctuation_voice(reference_voice, candidate, genre),
        }

    return {
        "genre": genre,
        "true_origin": true_origin,
        "length_stratum": length_info["stratum"],
        "turnitin_300w_eligible": length_info["eligible_for_official_turnitin"],
        "word_count": {
            "before": impact["word_count_before"],
            "after": impact["word_count_after"],
        },
        "factual_preservation": {
            "passed": fidelity["passed"],
            "violations": fidelity["violations"],
            "cultural_preservation_passed": cultural["passed"],
            "cultural_findings": cultural["findings"],
            "source_variety": cultural["source_variety"]["variety"],
        },
        "grammatical_integrity": {
            "passed": not impact["damages_grammar"],
            "damages_grammar": impact["damages_grammar"],
            "damages_clarity": impact["damages_clarity"],
            "boundary_anomalies": impact["boundary_anomalies"],
        },
        "edit_distance": edit_dist,
        "prosody_and_segmentation": {
            "sentences_before": impact["sentence_count_before"],
            "sentences_after": impact["sentence_count_after"],
            "sentence_cv_before": impact["sentence_cv_before"],
            "sentence_cv_after": impact["sentence_cv_after"],
            "sentence_cv_delta": impact["sentence_cv_delta"],
            "clause_cv_before": impact["clause_cv_before"],
            "clause_cv_after": impact["clause_cv_after"],
            "punctuation_entropy_before": impact["punctuation_entropy_before"],
            "punctuation_entropy_after": impact["punctuation_entropy_after"],
            "detector_sensitivity_mechanisms": impact["detector_sensitivity_mechanisms"],
        },
        "coherence_and_readability": {
            "adjacent_overlap_before": orig_coh.get("adjacent_mean_overlap", 0.0),
            "adjacent_overlap_after": cand_coh.get("adjacent_mean_overlap", 0.0),
            "cohesion_assessment_after": cand_coh.get("assessment", "unknown"),
            "given_new_breaks_before": orig_flow.get("count", 0),
            "given_new_breaks_after": cand_flow.get("count", 0),
            "mtld_before": orig_lex["mtld"].get("mtld", 0.0),
            "mtld_after": cand_lex["mtld"].get("mtld", 0.0),
            "hd_d_before": orig_lex["hd_d"].get("hd_d", 0.0),
            "hd_d_after": cand_lex["hd_d"].get("hd_d", 0.0),
            "plain_language_after": {
                k: cand_plain[k]["finding"]
                for k in ("relevant", "findable", "understandable", "usable")
            },
        },
        "voice_similarity": voice_eval,
    }


def _parse_float(val: object) -> float | None:
    if val is None:
        return None
    s = str(val).strip()
    if not s:
        return None
    try:
        return float(s)
    except ValueError:
        return None


def load_score_rows(path: str | Path) -> list[dict]:
    """Load manual or permissioned detector score records from CSV or JSON."""
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"Score file not found: {p}")
    text = p.read_text(encoding="utf-8")
    if p.suffix.lower() == ".json":
        import json
        data = json.loads(text)
        return list(data) if isinstance(data, list) else data.get("rows", [])
    rows: list[dict] = []
    reader = csv.DictReader(text.splitlines())
    for row in reader:
        rows.append(dict(row))
    return rows


def analyze_score_sheet(rows: list[dict], *, ai_flag_threshold: float = 50.0) -> dict:
    """Analyze imported detector scores for stability, reversals, false positives, and disagreement.

    Never fabricates scores: if a CSV has blank score columns (template sheet),
    it reports `scored_rows: 0` and explains how to populate manual observations.
    """
    scored: list[dict] = []
    eligibility_warnings: list[str] = []

    for row in rows:
        ai_score = _parse_float(row.get("ai_score"))
        human_score = _parse_float(row.get("human_score"))
        mixed_score = _parse_float(row.get("mixed_score"))
        if ai_score is None and human_score is None:
            continue
        # If only human_score is supplied, do not invent mixed_score; infer binary
        # complement only when mixed_score is absent.
        effective_ai = ai_score if ai_score is not None else (
            max(0.0, 100.0 - human_score - (mixed_score or 0.0))
            if human_score is not None else None
        )
        wc_raw = _parse_float(row.get("word_count"))
        wc = int(wc_raw) if wc_raw is not None else None
        detector = (row.get("detector") or "unspecified").strip()
        if wc is not None:
            elig = check_vendor_length_eligibility(wc, detector)
            if elig["caution"]:
                eligibility_warnings.append(elig["caution"])
        scored.append({
            "experiment": (row.get("experiment") or row.get("source") or "default").strip(),
            "condition": (row.get("condition") or "control").strip(),
            "detector": detector,
            "true_origin": (row.get("true_origin") or "unknown").strip().lower(),
            "word_count": wc,
            "repeat_index": (row.get("repeat_index") or "1").strip(),
            "ai_score": effective_ai,
            "human_score": human_score,
            "mixed_score": mixed_score,
            "notes": (row.get("notes") or "").strip(),
        })

    if not scored:
        return {
            "total_rows": len(rows),
            "scored_rows": 0,
            "status": "awaiting_manual_observations",
            "note": (
                "No detector scores are populated in this sheet. Fill ai_score/human_score "
                "from permissioned manual runs; Not-AI never fabricates or scrapes vendor scores."
            ),
        }

    # 1. Paired deltas vs baseline/control within each (experiment, detector).
    by_exp_det: dict[tuple[str, str], list[dict]] = {}
    for item in scored:
        by_exp_det.setdefault((item["experiment"], item["detector"]), []).append(item)

    paired_deltas: list[dict] = []
    reversals = 0
    paired_comparisons = 0

    for (exp, det), items in by_exp_det.items():
        # Find baseline (control / original / natural_rewrite)
        baseline = next(
            (x for x in items if x["condition"] in {"control", "original", "A_control"}),
            items[0],
        )
        base_ai = baseline["ai_score"]
        base_human = baseline["human_score"]
        for item in items:
            if item is baseline:
                continue
            ai_delta = (
                round(item["ai_score"] - base_ai, 2)
                if item["ai_score"] is not None and base_ai is not None
                else None
            )
            human_delta = (
                round(item["human_score"] - base_human, 2)
                if item["human_score"] is not None and base_human is not None
                else None
            )
            flipped = False
            if item["ai_score"] is not None and base_ai is not None:
                paired_comparisons += 1
                flipped = (base_ai >= ai_flag_threshold) != (item["ai_score"] >= ai_flag_threshold)
                if flipped:
                    reversals += 1
            paired_deltas.append({
                "experiment": exp,
                "detector": det,
                "baseline_condition": baseline["condition"],
                "variant_condition": item["condition"],
                "ai_score_baseline": base_ai,
                "ai_score_variant": item["ai_score"],
                "ai_score_delta": ai_delta,
                "human_score_baseline": base_human,
                "human_score_variant": item["human_score"],
                "human_score_delta": human_delta,
                "classification_flipped": flipped,
                "notes": item["notes"],
            })

    #Also compute direct punctuation-isolated deltas where natural_rewrite vs punctuation_revised exist.
    punctuation_isolated_deltas: list[dict] = []
    for (exp, det), items in by_exp_det.items():
        by_cond = {x["condition"]: x for x in items}
        for base_c, punct_c in (
            ("natural_rewrite", "punctuation_revised"),
            ("A_control", "B_punctuation_only"),
            ("C_lexical_syntactic", "D_combined_edits"),
            ("control", "replace_sentence_stop_with_ellipsis"),
            ("control", "drop_one_sentence_stop"),
        ):
            if base_c in by_cond and punct_c in by_cond:
                b_item, p_item = by_cond[base_c], by_cond[punct_c]
                punctuation_isolated_deltas.append({
                    "experiment": exp,
                    "detector": det,
                    "word_identical_pair": f"{base_c} -> {punct_c}",
                    "ai_score_delta": (
                        round(p_item["ai_score"] - b_item["ai_score"], 2)
                        if p_item["ai_score"] is not None and b_item["ai_score"] is not None
                        else None
                    ),
                    "human_score_delta": (
                        round(p_item["human_score"] - b_item["human_score"], 2)
                        if p_item["human_score"] is not None and b_item["human_score"] is not None
                        else None
                    ),
                })

    # 2. Human-written false positive rate (where true_origin == 'human').
    human_rows = [x for x in scored if x["true_origin"] in {"human", "human_verified"} and x["ai_score"] is not None]
    human_fp = [x for x in human_rows if x["ai_score"] >= ai_flag_threshold]
    fpr = round(len(human_fp) / len(human_rows), 3) if human_rows else None

    # 3. Between-detector disagreement on identical (experiment, condition).
    by_exp_cond: dict[tuple[str, str], list[dict]] = {}
    for item in scored:
        by_exp_cond.setdefault((item["experiment"], item["condition"]), []).append(item)

    disagreements: list[dict] = []
    for (exp, cond), items in by_exp_cond.items():
        det_scores = [x for x in items if x["ai_score"] is not None]
        if len(det_scores) >= 2:
            vals = [x["ai_score"] for x in det_scores]
            spread = round(max(vals) - min(vals), 2)
            labels = {x["ai_score"] >= ai_flag_threshold for x in det_scores}
            disagreements.append({
                "experiment": exp,
                "condition": cond,
                "detectors": [x["detector"] for x in det_scores],
                "ai_scores": vals,
                "max_spread": spread,
                "label_conflict": len(labels) > 1,
            })

    ai_deltas_numeric = [d["ai_score_delta"] for d in paired_deltas if d["ai_score_delta"] is not None]

    return {
        "total_rows": len(rows),
        "scored_rows": len(scored),
        "ai_flag_threshold": ai_flag_threshold,
        "paired_deltas": paired_deltas,
        "punctuation_isolated_deltas": punctuation_isolated_deltas,
        "ai_score_delta_summary": bootstrap_ci(ai_deltas_numeric, stat="median"),
        "reversal_rate": round(reversals / paired_comparisons, 3) if paired_comparisons else 0.0,
        "human_false_positive_rate": {
            "human_samples_scored": len(human_rows),
            "false_positives": len(human_fp),
            "fpr": fpr,
        },
        "between_detector_disagreement": disagreements,
        "eligibility_warnings": sorted(set(eligibility_warnings)),
        "scientific_caveat": (
            "Observed score differences measure detector sensitivity on specific inputs, "
            "not human authorship. Third-party aggregator percentages are not official "
            "Turnitin reports (which require >=300 words of long-form prose)."
        ),
    }
