"""Deterministic pre-output gate.

This module distinguishes mechanical errors from editorial signals. It never
claims to determine authorship, factual truth, semantic equivalence, or whether
a sentence is sufficiently "human". Those questions need source context and
editorial review.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import re
from statistics import pstdev
from typing import Iterable

from .policy import GenrePolicy, get_policy


WORD_RE = re.compile(r"\b[A-Za-z]+(?:'[A-Za-z]+)?\b")
SENTENCE_RE = re.compile(r"(?<=[.!?])\s+(?=[A-Z\"'])")
CONTRACTION_RE = re.compile(
    r"\b(?:[A-Za-z]+n't|[A-Za-z]+'(?:re|ve|ll|d|m|s))\b", re.IGNORECASE
)
PARTICIPIAL_OPENER_RE = re.compile(r"^(?:[A-Za-z]+ing)\b[^.!?]{0,100},")
TIER_ONE = {
    "camaraderie", "tapestry", "palpable", "intricate", "vibrant",
    "cacophony", "solace", "fleeting", "ignite", "unravel", "grapple",
    "amidst", "unspoken", "underscore", "unease", "pang", "waft", "prioritize",
}
TIER_TWO = {
    "delve", "leverage", "utilize", "facilitate", "comprehensive", "robust",
    "seamless", "pivotal", "foster", "meticulous", "nuanced", "multifaceted",
    "transformative", "groundbreaking", "empower", "synergy", "holistic",
    "dynamic", "impactful", "landscape", "realm", "revolutionize", "harness",
    "unlock", "elevate", "garner", "showcase", "bolster", "interplay",
    "testament", "boasts", "enhance", "crucial", "enduring", "valuable",
}
MECHANICAL_PATTERNS = {
    "template-transition": r"\b(?:furthermore|moreover|additionally|in conclusion|to summarize)\b",
    "empty-frame": r"\b(?:it is (?:worth|important) to note that|in today's fast-paced world)\b",
    "copula-avoidance": r"\b(?:serves as|stands as|functions as|operates as|marks a)\b",
    "negative-parallelism": r"\bnot just\b[^.!?]{0,80}\bbut\b",
}


@dataclass(frozen=True)
class Finding:
    rule: str
    severity: str
    message: str
    sentence: int | None = None
    span: str | None = None


@dataclass(frozen=True)
class GateResult:
    genre: str
    word_count: int
    counts: dict[str, float | int]
    findings: tuple[Finding, ...]

    @property
    def passed(self) -> bool:
        return not any(finding.severity == "error" for finding in self.findings)

    def as_dict(self) -> dict:
        return {
            "genre": self.genre,
            "passed": self.passed,
            "word_count": self.word_count,
            "counts": self.counts,
            "findings": [asdict(finding) for finding in self.findings],
        }


def words(text: str) -> list[str]:
    return WORD_RE.findall(text)


def sentences(text: str) -> list[str]:
    normalized = re.sub(r"\s+", " ", text.strip())
    return [sentence.strip() for sentence in SENTENCE_RE.split(normalized) if len(words(sentence)) >= 2]


def _find(pattern: str, text: str) -> Iterable[re.Match[str]]:
    return re.finditer(pattern, text, re.IGNORECASE)


def _opening_count(items: list[str]) -> tuple[int, int]:
    openings = [words(item)[0].lower() for item in items if words(item)]
    if not openings:
        return 0, 0
    return len(set(openings)), max(openings.count(opening) for opening in set(openings))


def _max_consecutive_short(lengths: list[int], threshold: int = 8) -> int:
    """Return the longest run of sentences shorter than the threshold."""
    longest = current = 0
    for length in lengths:
        current = current + 1 if length < threshold else 0
        longest = max(longest, current)
    return longest


def evaluate(
    text: str,
    genre: str = "linkedin",
    *,
    ascii_punctuation: bool = False,
    protected_terms: Iterable[str] = (),
) -> GateResult:
    """Evaluate text with deterministic, genre-aware checks.

    Empty output and explicitly missing protected terms are errors. Typography
    becomes an error only when the caller requests an ASCII house style.
    Everything else directs editorial attention without demanding a rewrite.
    """
    policy: GenrePolicy = get_policy(genre)
    tokens = words(text)
    items = sentences(text)
    lengths = [len(words(item)) for item in items]
    distinct_openings, max_opening = _opening_count(items)
    max_short_run = _max_consecutive_short(lengths)
    contraction_count = len(CONTRACTION_RE.findall(text))
    counts: dict[str, float | int] = {
        "dashes": text.count("—") + text.count("–"),
        "curly_quotes": sum(text.count(mark) for mark in "“”‘’"),
        "contractions": contraction_count,
        "contractions_per_1000": round(contraction_count * 1000 / len(tokens), 1) if tokens else 0.0,
        "sentences": len(items),
        "short_under_8": sum(length < 8 for length in lengths),
        "max_consecutive_short": max_short_run,
        "long_over_30": sum(length > 30 for length in lengths),
        "sentence_length_sd": round(pstdev(lengths), 1) if len(lengths) > 1 else 0.0,
        "opening_types": distinct_openings,
        "max_same_opening": max_opening,
    }
    findings: list[Finding] = []
    if not text.strip():
        findings.append(Finding("nonempty", "error", "Text is empty."))
        return GateResult(policy.name, 0, counts, tuple(findings))
    punctuation_severity = "error" if ascii_punctuation else "review"
    punctuation_context = (
        "The requested ASCII house style does not allow this punctuation."
        if ascii_punctuation
        else "Keep it when it matches the writer, locale, or publication style."
    )
    if counts["dashes"]:
        findings.append(Finding(
            "typography",
            punctuation_severity,
            f"The text contains em or en dashes. {punctuation_context}",
        ))
    if counts["curly_quotes"]:
        findings.append(Finding(
            "typography",
            punctuation_severity,
            f"The text contains curly quotes or apostrophes. {punctuation_context}",
        ))
    normalized = text.casefold()
    for term in dict.fromkeys(protected_terms):
        if not isinstance(term, str) or not term.strip():
            raise ValueError("protected terms must be non-empty strings")
        if term.casefold() not in normalized:
            findings.append(Finding(
                "protected-content",
                "error",
                "Expected protected text is missing from the deliverable.",
                span=term,
            ))
    lowered = [token.lower() for token in tokens]
    for tier, vocabulary, severity in (("tier-1-vocabulary", TIER_ONE, "warning"), ("tier-2-vocabulary", TIER_TWO, "review")):
        for term in sorted(set(lowered) & vocabulary):
            findings.append(Finding(tier, severity, "Review whether this word is precise and needed.", span=term))
    for rule, pattern in MECHANICAL_PATTERNS.items():
        for match in _find(pattern, text):
            findings.append(Finding(rule, "review", "Read this pattern in context; rewrite only if it adds no meaning.", span=match.group(0)))
    for index, item in enumerate(items, 1):
        if PARTICIPIAL_OPENER_RE.search(item):
            findings.append(Finding("participial-opener", "review", "Check whether this opener has a clear subject and earns its complexity.", index, item[:120]))
    if policy.require_contractions and len(tokens) >= 80 and contraction_count == 0:
        findings.append(Finding("contractions", "review", "This conversational genre has no contractions; preserve formality only if it matches the author.", None))
    if len(items) >= 5 and (distinct_openings < 3 or max_opening >= 3):
        findings.append(Finding("sentence-openings", "review", "Several sentences start alike; vary only where it improves the passage.", None))
    if len(items) >= 6 and counts["sentence_length_sd"] < 4:
        findings.append(Finding("sentence-rhythm", "review", "Sentence lengths are unusually uniform; inspect the paragraph rhythm.", None))
    if len(items) >= 4 and max_short_run >= 3 and not policy.allow_fragments:
        findings.append(Finding(
            "choppy-run",
            "review",
            "Several very short sentences appear in a row; combine only those that express one connected idea.",
            None,
        ))
    return GateResult(policy.name, len(tokens), counts, tuple(findings))


def render(result: GateResult, as_json: bool = False) -> str:
    if as_json:
        return json.dumps(result.as_dict(), indent=2, ensure_ascii=False)
    count = result.counts
    status = "pass" if result.passed else "fail"
    lines = [
        f"gate: {status} | genre {result.genre} | words {result.word_count}",
        "counts: " + " | ".join(f"{key} {value}" for key, value in count.items()),
    ]
    if result.findings:
        lines.append("findings:")
        lines.extend(f"- [{item.severity}] {item.rule}: {item.message}" + (f" ({item.span})" if item.span else "") for item in result.findings)
    else:
        lines.append("findings: none")
    return "\n".join(lines)
