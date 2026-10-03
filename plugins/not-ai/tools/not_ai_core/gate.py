"""Deterministic pre-output gate.

This module distinguishes mechanical errors from editorial signals. It never
claims to determine authorship, factual truth, semantic equivalence, or whether
a sentence is sufficiently "human". Those questions need source context and
editorial review.

v2 notes (research-grounded, still stdlib-only):
- Counts run on prose with fenced code, inline code, and blockquote markers
  masked out, so identifiers and quoted chatbot residue do not inflate
  vocabulary or rhythm figures. Protected-literal checks still run on the
  full deliverable.
- Sentence splitting guards common abbreviations (e.g. Dr., U.S.) plus
  headings, list markers, and table rows.
- Participial detection reports anchored ("Leveraging X, ...") and extended
  ("By leveraging X, ...", mid-sentence ", ensuring ...") forms separately.
  The extended pass exists because the Reinhart et al. (PNAS 2025) signal the
  anchored regex missed most often was the prepositional variant.
- Vocabulary matching stems common inflections, so "grappling" counts with
  "grapple" and "delving" with "delve".
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import json
import math
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
# Prepositional participial openers the anchored regex misses:
# "By leveraging...", "Through combining...", "After reviewing..."
EXTENDED_OPENER_RE = re.compile(
    r"^(?:by|through|via|with|after|before|while|when)\s+[a-z]+ing\b",
    re.IGNORECASE,
)
# Mid-sentence participial tails: "..., ensuring ...", ", leveraging ..."
MID_PARTICIPLE_RE = re.compile(r",\s+(?:[a-z]+ing)\b[^.!?]{0,60}", re.IGNORECASE)
# Common abbreviations that must not end a sentence.
_ABBREVIATIONS = (
    "Mr", "Mrs", "Ms", "Dr", "Prof", "Sr", "Jr", "St",
    "e.g", "i.e", "vs", "etc", "Fig", "Eq", "Ref", "No",
    "U.S", "U.K", "U.N", "E.U",
)
_ABBR_RE = re.compile(
    r"\b(?:" + "|".join(re.escape(a) for a in _ABBREVIATIONS) + r")\.$"
)
NOMINALIZATION_RE = re.compile(
    r"\b\w+(?:tion|sion|ment|ness|ance|ence|ity|ization)\b", re.IGNORECASE
)
BRACKET_SLOT_RE = re.compile(r"\[[^\]\n]{1,80}\]")
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
# Inflected forms mapped to their listed base, so "delving" counts with
# "delve" and "grappling" with "grapple". Only unambiguous forms are listed;
# nouns that collide with common verbs (e.g. "testament") are left exact.
VOCAB_INFLECTIONS = {
    "delves": "delve", "delving": "delve", "delved": "delve",
    "leverages": "leverage", "leveraging": "leverage", "leveraged": "leverage",
    "utilizes": "utilize", "utilizing": "utilize", "utilized": "utilize",
    "facilitates": "facilitate", "facilitating": "facilitate",
    "facilitated": "facilitate",
    "fosters": "foster", "fostering": "foster", "fostered": "foster",
    "empowers": "empower", "empowering": "empower", "empowered": "empower",
    "showcases": "showcase", "showcasing": "showcase", "showcased": "showcase",
    "underscores": "underscore", "underscoring": "underscore",
    "underscored": "underscore",
    "harnesses": "harness", "harnessing": "harness", "harnessed": "harness",
    "unlocks": "unlock", "unlocking": "unlock", "unlocked": "unlock",
    "elevates": "elevate", "elevating": "elevate", "elevated": "elevate",
    "garners": "garner", "garnering": "garner", "garnered": "garner",
    "bolsters": "bolster", "bolstering": "bolster", "bolstered": "bolster",
    "enhances": "enhance", "enhancing": "enhance", "enhanced": "enhance",
    "ignites": "ignite", "igniting": "ignite", "ignited": "ignite",
    "unravels": "unravel", "unraveling": "unravel", "unravelling": "unravel",
    "unravelled": "unravel",
    "grapples": "grapple", "grappling": "grapple", "grappled": "grapple",
    "wafts": "waft", "wafting": "waft", "wafted": "waft",
    "prioritizes": "prioritize", "prioritizing": "prioritize",
    "prioritized": "prioritize", "prioritises": "prioritize",
    "prioritising": "prioritize", "prioritised": "prioritize",
}
MECHANICAL_PATTERNS = {
    "template-transition": r"\b(?:furthermore|moreover|additionally|in conclusion|to summarize)\b",
    "empty-frame": r"\b(?:it is (?:worth|important) to note that|in today's fast-paced world)\b",
    "copula-avoidance": r"\b(?:serves as|stands as|functions as|operates as|marks a)\b",
    "negative-parallelism": r"\bnot just\b[^.!?]{0,80}\bbut\b",
}

EXPLANATIONS = {
    "nonempty": "Empty output is an objective deliverable error.",
    "typography": "Dashes and curly quotes are valid house style in many "
    "publications. Keep them when the writer, locale, or genre earns them.",
    "protected-content": "A literal the caller marked as required is absent. "
    "Restore the exact text or confirm the requirement changed.",
    "tier-1-vocabulary": "Corpus studies (Reinhart et al., PNAS 2025; Kobak et "
    "al., Science Advances 2025) find this word at 80-170x the human rate. "
    "Keep it only when it is precise, characteristic, or required by the field.",
    "tier-2-vocabulary": "This term clusters in model output but also appears "
    "in human writing. Review what it does for this reader; do not ban it.",
    "template-transition": "Sentence-initial Moreover/Furthermore chains read "
    "as decoration. Keep the transition only if it names a real relationship.",
    "empty-frame": "This frame delays the point without changing it. Delete "
    "it if the sentence survives without it.",
    "copula-avoidance": "'Serves as' and 'stands as' usually hide a plain "
    "'is'. Prefer the plain verb unless the field requires the nominal form.",
    "negative-parallelism": "'Not just X but Y' is cadence, not argument. "
    "Say Y directly unless the denial of X does real work.",
    "participial-opener": "Present-participial openers run 2-5x the human "
    "rate in instruction-tuned output (Reinhart et al.). Check the opener has "
    "a clear subject and earns its complexity.",
    "participial-opener-extended": "Prepositional variant ('By leveraging...') "
    "the anchored check misses. Same review: clear subject, earned complexity.",
    "mid-sentence-participle": "A mid-sentence ', verb-ing' tail often stacks "
    "a second claim onto a finished sentence. Split it if it carries its own job.",
    "contractions": "This conversational genre has no contractions. Preserve "
    "formality only if it matches the author.",
    "sentence-openings": "Several sentences start alike; vary only where it "
    "improves the passage.",
    "sentence-rhythm": "Sentence lengths are unusually uniform; inspect the "
    "paragraph rhythm by ear, not by target.",
    "choppy-run": "Several very short sentences appear in a row; combine only "
    "those that express one connected idea.",
    "nominalization-density": "Noun-heavy packaging ('implementation of') "
    "runs ~2x the human rate. Unpack to verbs where the source supports it; "
    "academic and technical genres legitimately keep more.",
    "bracket-slot": "A bracketed prompt marks detail only the writer can "
    "supply. Fill it from the source or ask; never invent it.",
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


def mask_for_counts(text: str) -> str:
    """Return prose with code and quotation markup masked for measurement.

    Fenced code blocks become a single placeholder line, inline code spans
    become one token, and leading blockquote markers are removed. The goal
    is to keep identifiers, commands, and quoted chatbot residue from
    inflating vocabulary or rhythm figures. Protected-literal checks always
    run on the unmasked deliverable.
    """
    masked = re.sub(r"```.*?```", "\n[code block]\n", text, flags=re.DOTALL)
    masked = re.sub(r"`[^`\n]+`", " [code] ", masked)
    masked = re.sub(r"(?m)^\s*>\s?", "", masked)
    return masked


def _strip_layout_lines(text: str) -> str:
    """Drop markdown headings, table rows, and bare list markers line-wise.

    Post-split filtering alone fails on heading-led files: without a
    sentence boundary the whole document can merge into one item starting
    with `#` and get discarded entirely.
    """
    kept: list[str] = []
    for line in text.splitlines():
        stripped = line.strip()
        if not stripped:
            continue
        if re.match(r"^#{1,6}\s", stripped):
            continue
        if stripped.count("|") >= 2:
            continue
        if re.match(r"^(?:[-*\u2022]|\d+[.)])\s*$", stripped):
            continue
        kept.append(line)
    return "\n".join(kept)


def sentences(text: str) -> list[str]:
    normalized = re.sub(r"\s+", " ", _strip_layout_lines(mask_for_counts(text)).strip())
    candidates = SENTENCE_RE.split(normalized)
    merged: list[str] = []
    for candidate in candidates:
        candidate = candidate.strip()
        if not candidate:
            continue
        # Rejoin splits that break after a known abbreviation ("Dr. Smith"),
        # a single initial ("U. Smith"), or a list/table marker line.
        if merged and (
            _ABBR_RE.search(merged[-1])
            or re.search(r"\b[A-Z]\.$", merged[-1])
        ):
            merged[-1] = f"{merged[-1]} {candidate}"
            continue
        merged.append(candidate)
    filtered: list[str] = []
    for item in merged:
        stripped = item.strip()
        if not stripped:
            continue
        # Skip markdown headings, table rows, and bare list markers: they
        # are layout, not sentences, and counting them corrupts burstiness.
        if re.match(r"^#{1,6}\s", stripped):
            continue
        if "|" in stripped and stripped.count("|") >= 2:
            continue
        if re.match(r"^(?:[-*•]|\d+[.)])\s*$", stripped):
            continue
        if len(words(stripped)) >= 2:
            filtered.append(stripped)
    return filtered


def _find(pattern: str, text: str) -> Iterable[re.Match[str]]:
    return re.finditer(pattern, text, re.IGNORECASE)


def _opening_count(items: list[str]) -> tuple[int, int]:
    openings = [words(item)[0].lower() for item in items if words(item)]
    if not openings:
        return 0, 0
    return len(set(openings)), max(openings.count(opening) for opening in set(openings))


def _opener_entropy(items: list[str]) -> float:
    openings = [words(item)[0].lower() for item in items if words(item)]
    if not openings:
        return 0.0
    total = len(openings)
    entropy = 0.0
    for opening in set(openings):
        p = openings.count(opening) / total
        entropy -= p * math.log2(p)
    return round(entropy, 2)


def _max_consecutive_short(lengths: list[int], threshold: int = 8) -> int:
    """Return the longest run of sentences shorter than the threshold."""
    longest = current = 0
    for length in lengths:
        current = current + 1 if length < threshold else 0
        longest = max(longest, current)
    return longest


def bracket_slots(text: str) -> list[str]:
    """Bracketed prompts, excluding markdown links and images.

    `[specific result]` is a prompt only the writer can fill. `[label](url)`
    and `![alt](src)` are link markup, not missing detail, so they are
    skipped here rather than reported.
    """
    slots: list[str] = []
    for match in BRACKET_SLOT_RE.finditer(text):
        start, end = match.span()
        if start > 0 and text[start - 1] == "!":
            continue
        trailing = text[end:end + 1]
        if trailing == "(":
            continue
        slots.append(match.group(0))
    return slots


def _normalize_vocab_token(token: str) -> str:
    lowered = token.lower()
    if lowered in TIER_ONE or lowered in TIER_TWO:
        return lowered
    return VOCAB_INFLECTIONS.get(lowered, lowered)


def vocab_hits(text: str) -> dict[str, list[str]]:
    """Map tier-1/tier-2 hits with inflection stemming on prose text."""
    prose = mask_for_counts(text)
    # Quoted chatbot examples are residue to inspect, not the author's
    # diction: strip double-quoted spans before vocabulary review.
    prose = re.sub(r'"[^"\n]{1,200}"', " ", prose)
    prose = re.sub(r"\u201c[^\u201d\n]{1,200}\u201d", " ", prose)
    found: dict[str, list[str]] = {"tier-1-vocabulary": [], "tier-2-vocabulary": []}
    for token in WORD_RE.findall(prose):
        base = _normalize_vocab_token(token)
        if base in TIER_ONE:
            found["tier-1-vocabulary"].append(base)
        elif base in TIER_TWO:
            found["tier-2-vocabulary"].append(base)
    return found


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
    prose = mask_for_counts(text)
    tokens = words(prose)
    items = sentences(text)
    lengths = [len(words(item)) for item in items]
    distinct_openings, max_opening = _opening_count(items)
    max_short_run = _max_consecutive_short(lengths)
    contraction_count = len(CONTRACTION_RE.findall(prose))
    nominal_count = len(NOMINALIZATION_RE.findall(prose))
    nominal_rate = nominal_count / len(tokens) * 1000 if tokens else 0.0
    found_slots = bracket_slots(text)
    mean_len = sum(lengths) / len(lengths) if lengths else 0.0
    cv = (pstdev(lengths) / mean_len) if len(lengths) > 1 and mean_len else 0.0
    counts: dict[str, float | int] = {
        "dashes": text.count("\u2014") + text.count("\u2013"),
        "curly_quotes": sum(text.count(mark) for mark in "\u201c\u201d\u2018\u2019"),
        "contractions": contraction_count,
        "contractions_per_1000": round(contraction_count * 1000 / len(tokens), 1) if tokens else 0.0,
        "sentences": len(items),
        "short_under_8": sum(length < 8 for length in lengths),
        "max_consecutive_short": max_short_run,
        "long_over_30": sum(length > 30 for length in lengths),
        "sentence_length_sd": round(pstdev(lengths), 1) if len(lengths) > 1 else 0.0,
        "sentence_length_cv": round(cv, 3),
        "opener_entropy": _opener_entropy(items),
        "opening_types": distinct_openings,
        "max_same_opening": max_opening,
        "nominalizations": nominal_count,
        "nominalizations_per_1000": round(nominal_rate, 1),
        "bracket_slots": len(found_slots),
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
    hits = vocab_hits(text)
    for tier, severity in (("tier-1-vocabulary", "warning"), ("tier-2-vocabulary", "review")):
        for term in sorted(set(hits[tier])):
            findings.append(Finding(tier, severity, EXPLANATIONS[tier], span=term))
    for rule, pattern in MECHANICAL_PATTERNS.items():
        for match in _find(pattern, prose):
            findings.append(Finding(rule, "review", EXPLANATIONS[rule], span=match.group(0)))
    for index, item in enumerate(items, 1):
        stripped = item.strip()
        if PARTICIPIAL_OPENER_RE.search(stripped):
            findings.append(Finding("participial-opener", "review",
                                    EXPLANATIONS["participial-opener"],
                                    index, stripped[:120]))
        elif EXTENDED_OPENER_RE.search(stripped):
            findings.append(Finding("participial-opener-extended", "review",
                                    EXPLANATIONS["participial-opener-extended"],
                                    index, stripped[:120]))
        elif MID_PARTICIPLE_RE.search(stripped):
            findings.append(Finding("mid-sentence-participle", "review",
                                    EXPLANATIONS["mid-sentence-participle"],
                                    index, stripped[:120]))
    floor = getattr(policy, "contraction_floor", 80)
    if policy.require_contractions and len(tokens) >= floor and contraction_count == 0:
        findings.append(Finding("contractions", "review", EXPLANATIONS["contractions"], None))
    if len(items) >= 5 and (distinct_openings < 3 or max_opening >= 3):
        findings.append(Finding("sentence-openings", "review", EXPLANATIONS["sentence-openings"], None))
    if len(items) >= 6 and counts["sentence_length_sd"] < 4:
        findings.append(Finding("sentence-rhythm", "review", EXPLANATIONS["sentence-rhythm"], None))
    if len(items) >= 4 and max_short_run >= 3 and not policy.allow_fragments:
        findings.append(Finding(
            "choppy-run",
            "review",
            EXPLANATIONS["choppy-run"],
            None,
        ))
    if policy.check_nominalizations and tokens and nominal_rate > 50:
        findings.append(Finding(
            "nominalization-density",
            "review",
            EXPLANATIONS["nominalization-density"],
            None,
        ))
    for slot in found_slots[:5]:
        findings.append(Finding(
            "bracket-slot",
            "review",
            EXPLANATIONS["bracket-slot"],
            span=slot[:80],
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
