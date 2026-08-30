#!/usr/bin/env python3
"""
not-ai: _shared.py

Measurement primitives used by more than one script. Anything defined here was
previously duplicated, and the duplicates had drifted apart. Keeping one
definition is the point of this module: two copies of the same metric that
disagree by a percent produce diagnostics that cannot be compared.

Import it from a sibling script with:

    from _shared import get_sentences, tokenize_words, nominalization_stats

The scripts insert their own directory onto sys.path before importing, so this
works whatever the current working directory is.
"""

import re

# ---------------------------------------------------------------------------
# Nominalization
# ---------------------------------------------------------------------------
#
# HEURISTIC PROXY. Read this before quoting any number it produces.
#
# This matches any word ending in a nominalizing suffix. It has no part of
# speech information, so it counts "nation", "moment" and "witness" as
# nominalizations because they end the right way. It over-counts substantially
# against a real morphosyntactic tagger.
#
# Concretely: Reinhart et al. 2025 (PNAS 122(8) e2422455122) measured 14.6
# nominalizations per 1,000 tokens for human writers, using dependency parses
# and Biber's tagset. This regex reports roughly 90 per 1,000 on ordinary
# English prose. The two numbers measure different things.
#
# So: compare a figure from this proxy only against another figure from this
# proxy, a draft against its own rewrite, or an author against their earlier
# work. Never compare it against the 14.6 figure or any other tagged rate.
#
# The bands in HEURISTIC_NOMINALIZATION_BANDS below are calibrated for this
# proxy's own scale. They are not research findings and no paper reports them.

NOMINALIZATION_SUFFIXES = (
    "tion", "tions",
    "ment", "ments",
    "ness", "nesses",
    "ity", "ities",
    "ance", "ances",
    "ence", "ences",
)

NOMINALIZATION_PATTERN = re.compile(
    r"\b\w+(" + "|".join(NOMINALIZATION_SUFFIXES) + r")\b",
    re.IGNORECASE,
)

# Thresholds on this proxy's scale, in matches per 1,000 words.
HEURISTIC_NOMINALIZATION_BANDS = {
    "high": 50.0,
    "elevated": 35.0,
}

WORD_PATTERN = re.compile(r"\b[a-zA-Z]+\b")

SENTENCE_SPLIT_PATTERN = re.compile(r'(?<=[.!?])\s+(?=[A-Z"\'])')

# Minimum stance signal before a balance verdict means anything.
#
# An earlier version compared hedge and booster counts directly and returned one
# of three verdicts unconditionally. Because `0 > 0` is false in both branches,
# a text with no hedges and no boosters fell through to "calibrated", which read
# as a clean bill of health on the one reading the research says matters most on
# the underuse side: instruction-tuned models carry hedges at 50% to 63% of the
# human rate. Every file in this repository was affected. Twelve reported
# "calibrated" on zero markers, four reported "over-hedged" on two to five
# hedges at rates under 1.1 per 1,000 words, and one reported "over-assertive"
# on a single `certainly`. Not one of those verdicts was correct.
#
# So a balance verdict now requires both an absolute floor and a rate floor, and
# the two states below the floor are reported as themselves rather than folded
# into "calibrated". Both numbers are heuristics on this proxy's scale. No paper
# reports them, and absent stance is not a defect on its own: a passage
# explaining how a cache works has nothing to hedge. Deciding whether the gap
# matters is genre judgment, which is why the scripts report it and SKILL.md
# rules on it.
STANCE_MIN_MARKERS = 3
STANCE_MIN_RATE_PER_1000 = 2.0


def stance_balance(hedge_count: int, booster_count: int, word_count: int) -> str:
    """
    Verdict on the hedge-to-booster balance, or a refusal to give one.

    Returns "absent" when there is no stance marker at all, "too sparse to
    judge" when there is too little to read a ratio from, and otherwise
    "over-hedged", "over-assertive" or "calibrated".
    """
    total = hedge_count + booster_count
    if total == 0:
        return "absent"
    rate = total / word_count * 1000 if word_count else 0.0
    if total < STANCE_MIN_MARKERS or rate < STANCE_MIN_RATE_PER_1000:
        return "too sparse to judge"
    if hedge_count > booster_count * 3:
        return "over-hedged"
    if booster_count > hedge_count * 2:
        return "over-assertive"
    return "calibrated"


def tokenize_words(text: str) -> list[str]:
    """
    Alphabetic word tokens. This is the canonical denominator for every
    per-1,000-words rate in this toolkit.

    Note it discards numerals and any token containing digits, so a table of
    figures reads as fewer words than a reader would count.
    """
    return WORD_PATTERN.findall(text)


def get_sentences(text: str) -> list[str]:
    """
    Split into sentences on terminal punctuation followed by a capital.

    Known limits: an abbreviation such as "e.g." or "Dr." followed by a capital
    splits incorrectly, and a sentence ending in a lowercase letter or a closing
    bracket may not split at all. Fragments under two words are dropped, which
    means headings and list labels do not count as sentences.
    """
    text = re.sub(r"\s+", " ", text.strip())
    sentences = SENTENCE_SPLIT_PATTERN.split(text)
    return [s.strip() for s in sentences if s.strip() and len(s.split()) >= 2]


def get_paragraphs(text: str) -> list[str]:
    """Split on blank lines."""
    paragraphs = re.split(r"\n\s*\n", text.strip())
    return [p.strip() for p in paragraphs if p.strip()]


def nominalization_stats(text: str, words: list[str] | None = None) -> dict:
    """
    Count nominalization-suffixed words and express the rate per 1,000 words.

    Pass `words` when the caller has already tokenized, so the denominator is
    guaranteed identical to the one used for the caller's other rates.

    The returned "assessment" describes where the figure sits on this proxy's
    heuristic scale. It is deliberately not phrased as a judgment about who or
    what wrote the text, because this measurement cannot establish that.
    """
    if words is None:
        words = tokenize_words(text)

    total_words = len(words)
    count = len(NOMINALIZATION_PATTERN.findall(text))
    rate = (count / total_words * 1000) if total_words else 0.0

    if rate > HEURISTIC_NOMINALIZATION_BANDS["high"]:
        assessment = "high for this proxy"
    elif rate > HEURISTIC_NOMINALIZATION_BANDS["elevated"]:
        assessment = "elevated for this proxy"
    else:
        assessment = "normal for this proxy"

    return {
        "nominalization_count": count,
        "total_words": total_words,
        "rate_per_1000_words": round(rate, 1),
        "assessment": assessment,
    }
