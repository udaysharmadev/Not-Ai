"""Deterministic voice profiling for the Not Ai plugin.

A voice profile measures repeated, mostly unconscious choices in a writer's
own reference text: sentence rhythm, function-word habits, stance markers,
specificity, and opening variety. Comparing a draft against the author's
profile surfaces drift ("this draft hedges half as often as you usually do")
without claiming anything about authorship. Stylometry's robust signal lives
in very frequent words and sequences, not rare vocabulary, which is why this
module counts function words and shapes rather than content nouns.

Everything here is stdlib-only and heuristic. Profiles need roughly 300+
words of reference to mean anything; below that the module says so instead
of guessing.
"""

from __future__ import annotations

import re
from statistics import pstdev

from .gate import _opener_entropy, mask_for_counts, sentences, words

FUNCTION_WORDS = (
    "the a an and or but if then of in on at to for with by from as"
    " i we you he she it they my our your his her its their me us him them"
    " is are was were be been being have has had do does did will would can"
    " could may might shall should must not no very so too just only".split()
)

HEDGES = {
    "may", "might", "could", "would", "seem", "appear", "suggest", "indicate",
    "likely", "possible", "perhaps", "maybe", "tend", "around", "generally",
    "often",
}
BOOSTERS = {
    "clearly", "obviously", "definitely", "undoubtedly", "demonstrate",
    "show", "prove", "always", "never", "must", "certainly", "indeed",
}
SELF_WORDS = {"i", "me", "my", "we", "us", "our"}
ENGAGE_WORDS = {"you", "your", "consider", "note", "see", "imagine"}

MIN_REFERENCE_WORDS = 300


def profile(text: str) -> dict:
    """Measure a voice profile from reference or draft prose."""
    prose = mask_for_counts(text)
    tokens = words(prose)
    lowered = [token.lower() for token in tokens]
    total = len(tokens)
    items = sentences(text)
    lengths = [len(words(item)) for item in items]

    def per_1k(count: int) -> float:
        return round(count / total * 1000, 1) if total else 0.0

    counts = {}
    for word in lowered:
        counts[word] = counts.get(word, 0) + 1
    function_profile = {word: per_1k(counts.get(word, 0)) for word in FUNCTION_WORDS}

    mean_len = sum(lengths) / len(lengths) if lengths else 0.0
    cv = (pstdev(lengths) / mean_len) if len(lengths) > 1 and mean_len else 0.0
    contraction_hits = len(re.findall(
        r"\b(?:[A-Za-z]+n't|[A-Za-z]+'(?:re|ve|ll|d|m|s))\b", prose, re.IGNORECASE
    ))
    numbers = len(re.findall(r"\b\d+(?:\.\d+)?%?", prose))
    properish = len(re.findall(
        r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}\b", prose
    ))
    openings = [words(item)[0].lower() for item in items if words(item)]

    return {
        "word_count": total,
        "sentences": len(items),
        "reference_sufficient": total >= MIN_REFERENCE_WORDS,
        "rhythm": {
            "mean": round(mean_len, 1),
            "sd": round(pstdev(lengths), 1) if len(lengths) > 1 else 0.0,
            "cv": round(cv, 3),
            "short_rate": round(
                sum(1 for length in lengths if length < 10) / len(lengths), 3
            ) if lengths else 0.0,
            "long_rate": round(
                sum(1 for length in lengths if length > 30) / len(lengths), 3
            ) if lengths else 0.0,
        },
        "function_profile": function_profile,
        "stance": {
            "hedge_per_1k": per_1k(sum(1 for word in lowered if word in HEDGES)),
            "booster_per_1k": per_1k(sum(1 for word in lowered if word in BOOSTERS)),
            "self_per_1k": per_1k(sum(1 for word in lowered if word in SELF_WORDS)),
            "engage_per_1k": per_1k(sum(1 for word in lowered if word in ENGAGE_WORDS)),
            "questions_per_1k": per_1k(prose.count("?")),
        },
        "specificity": {
            "numbers_per_1k": per_1k(numbers),
            "properish_per_1k": per_1k(properish),
        },
        "mechanics": {
            "contraction_per_1k": per_1k(contraction_hits),
            "avg_word_len": round(
                sum(len(token) for token in tokens) / total, 2
            ) if total else 0.0,
        },
        "openings": {
            "entropy": _opener_entropy(items),
            "top": sorted(
                {opening: openings.count(opening) for opening in set(openings)}.items(),
                key=lambda pair: -pair[1],
            )[:5],
        },
    }


def _verdict(reference: float, draft: float, tolerance: float) -> str:
    if reference == 0 and draft == 0:
        return "same (both absent)"
    if reference == 0:
        return "introduced in draft"
    change = abs(draft - reference) / reference
    return "aligned" if change <= tolerance else "drifted"


def compare(reference_text: str, draft_text: str) -> dict:
    """Compare a draft against the author's reference profile.

    Returns per-dimension verdicts with the raw figures behind them. The
    verdicts are editorial prompts ("contraction use drifted: reference 12.4
    per 1k, draft 0.0"), never authorship claims.
    """
    reference = profile(reference_text)
    draft = profile(draft_text)
    notes: list[str] = []

    def check(label: str, ref_value: float, draft_value: float,
              tolerance: float, unit: str = "") -> dict:
        verdict = _verdict(ref_value, draft_value, tolerance)
        if verdict == "drifted":
            notes.append(
                f"{label} drifted: reference {ref_value}{unit}, draft {draft_value}{unit}"
            )
        return {"reference": ref_value, "draft": draft_value, "verdict": verdict}

    rhythm = {
        "cv": check("rhythm variation (CV)", reference["rhythm"]["cv"],
                    draft["rhythm"]["cv"], 0.30),
        "short_rate": check("short-sentence rate", reference["rhythm"]["short_rate"],
                            draft["rhythm"]["short_rate"], 0.60),
    }
    stance = {
        key: check(f"stance {key}", reference["stance"][key], draft["stance"][key], 0.60, "/1k")
        for key in ("hedge_per_1k", "booster_per_1k", "self_per_1k", "engage_per_1k")
    }
    mechanics = {
        "contraction_per_1k": check(
            "contraction use",
            reference["mechanics"]["contraction_per_1k"],
            draft["mechanics"]["contraction_per_1k"], 0.60, "/1k"),
    }
    specificity = {
        key: check(f"specificity {key}", reference["specificity"][key],
                   draft["specificity"][key], 0.60, "/1k")
        for key in ("numbers_per_1k", "properish_per_1k")
    }
    # Function-word distance: mean absolute gap over the shared list.
    ref_func = reference["function_profile"]
    draft_func = draft["function_profile"]
    distance = round(
        sum(abs(ref_func[word] - draft_func[word]) for word in FUNCTION_WORDS)
        / len(FUNCTION_WORDS), 2,
    )
    function_words = {
        "mean_abs_gap_per_1k": distance,
        "verdict": "aligned" if distance < 3.0 else "drifted",
    }
    if function_words["verdict"] == "drifted":
        notes.append(
            f"function-word habits drifted (mean gap {distance}/1k across "
            f"{len(FUNCTION_WORDS)} common words)"
        )

    drifted = sum(
        1 for group in (rhythm, stance, mechanics, specificity)
        for item in group.values() if item["verdict"] == "drifted"
    ) + (1 if function_words["verdict"] == "drifted" else 0)

    return {
        "reference_words": reference["word_count"],
        "draft_words": draft["word_count"],
        "reference_sufficient": reference["reference_sufficient"],
        "caution": (
            None if reference["reference_sufficient"]
            else f"Reference has {reference['word_count']} words; "
                  f"{MIN_REFERENCE_WORDS}+ are needed for a stable profile. "
                  "Treat every verdict below as tentative."
        ),
        "rhythm": rhythm,
        "stance": stance,
        "mechanics": mechanics,
        "specificity": specificity,
        "function_words": function_words,
        "opener_entropy": {
            "reference": reference["openings"]["entropy"],
            "draft": draft["openings"]["entropy"],
        },
        "drifted_dimensions": drifted,
        "overall": "aligned" if drifted <= 1 else "mostly aligned" if drifted <= 3 else "drifted",
        "notes": notes,
    }
