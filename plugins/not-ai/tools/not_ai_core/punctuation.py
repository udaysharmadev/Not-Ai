"""Punctuation and prosody analysis engine (Not-AI 4.0).

Analyzes how punctuation contributes to readable, natural prose and how
clause-level prosody interacts with sentence segmentation, genre conventions,
and author voice.

Core design rules:
- Natural writing is not deliberately broken writing. Never recommend deleting
  required terminal periods, introducing comma splices, or fusing sentences to
  manipulate a statistical metric.
- Protect non-prosodic punctuation (decimals, dates, times, URLs, code spans,
  abbreviations, initials, citations) before counting clause or sentence marks.
- Interpret punctuation relative to genre policy and supplied author voice:
  an informal social caption has different norms from an academic abstract or
  technical README.
"""

from __future__ import annotations

from dataclasses import asdict, dataclass
import math
import re
from statistics import pstdev
from typing import Iterable

from .policy import GenrePolicy, get_policy
from .text import ABBREVIATIONS, mask_for_counts, paragraphs, sentences, words
from .unicode_hygiene import normalize_for_analysis


# Non-prosodic patterns whose internal periods/commas/colons must not be
# misclassified as clause or sentence boundaries.
_URL_RE = re.compile(r"https?://\S+|www\.\S+", re.IGNORECASE)
_DECIMAL_OR_NUM_RE = re.compile(r"\b\d+(?:[.,:/-]\d+)+%?\b")
_TIME_RE = re.compile(r"\b\d{1,2}:\d{2}\s*(?:a\.m\.|p\.m\.|am|pm)?\b", re.IGNORECASE)
_CITATION_YEAR_RE = re.compile(r"\([^()\n]{1,80}\b(?:19|20)\d{2}[a-z]?\b[^()\n]{0,40}\)")
_BRACKET_CIT_RE = re.compile(r"\[\s*\d+(?:\s*[,–-]\s*\d+)*\s*\]")
_ABBR_TOKEN_RE = re.compile(
    r"\b(?:" + "|".join(re.escape(a) for a in ABBREVIATIONS) + r")\.",
    re.IGNORECASE,
)
_INITIALS_RE = re.compile(r"(?:\b[A-Z]\.\s*){1,4}")
_ELLIPSIS_RE = re.compile(r"\.\.\.+|\u2026")
_TIGHT_ELLIPSIS_BOUNDARY_RE = re.compile(r"(?<=[A-Za-z])(?:\.\.\.+|\u2026)(?=[A-Z])")
_DOUBLE_PERIOD_RE = re.compile(r"(?<!\.)\.\.(?!\.)")

# Fused sentence / missing-stop heuristic: a lowercase content word (not a
# title, determiner, preposition, conjunction, or common modifier before a
# proper noun) followed directly by a capitalized sentence-starter pronoun or
# determiner after a clause of at least 5 words.
_FUSED_STARTERS = {
    "He", "She", "They", "We", "It", "This", "These", "Those",
    "However", "Moreover", "Furthermore", "Therefore", "Meanwhile",
    "Nevertheless", "Consequently",
}
_PRE_CAPITAL_ALLOW = {
    "a", "an", "the", "in", "on", "at", "to", "for", "of", "from", "by",
    "with", "about", "like", "as", "and", "or", "but", "nor", "if", "when",
    "while", "before", "after", "since", "until", "into", "through", "over",
    "under", "between", "among", "against", "without", "within", "during",
    "including", "called", "named", "near", "visited", "met", "saw", "joined",
    "left", "told", "asked", "thanked", "hired", "helped", "is", "was", "are",
    "were", "be", "been", "being", "has", "have", "had", "said", "says",
    "wrote", "writes", "noted", "notes", "argued", "argues", "showed", "shows",
    "found", "finds", "king", "queen", "prince", "president", "minister",
    "senator", "governor", "mayor", "professor", "doctor", "general", "saint",
    "mount", "lake", "river", "new", "old", "north", "south", "east", "west",
    "central", "modern", "ancient", "early", "late",
}

_CLAUSE_SPLIT_RE = re.compile(r"[,;:\u2014\u2013()]|\s+--\s+")
_INTRO_COMMA_RE = re.compile(r"^\s*(?:[A-Za-z]+(?:\s+[A-Za-z']+){0,6}),\s+")
_COMMA_SPLICE_PROXY_RE = re.compile(
    r",\s+(?:he|she|they|we|it|this|that|these|those|there|however|therefore|moreover|furthermore|consequently|nevertheless)\s+"
    r"(?:is|are|was|were|has|have|had|will|would|can|could|should|must|may|might|"
    r"[a-z]+ed|[a-z]+s)\b",
    re.IGNORECASE,
)
_FINITE_VERB_PROXY_RE = re.compile(
    r"\b(?:am|is|are|was|were|be|been|being|have|has|had|do|does|did|"
    r"will|would|shall|should|can|could|may|might|must|"
    r"[a-z]{3,}ed|[a-z]{3,}(?:es|s))\b",
    re.IGNORECASE,
)

# Genre expectations for punctuation and prosody.
GENRE_PUNCTUATION_NORMS: dict[str, dict[str, object]] = {
    "academic": {
        "require_terminal_stops": True,
        "allow_ellipsis": False,
        "allow_exclamation": False,
        "semicolon_colon_welcome": True,
        "expected_clause_cv_min": 0.25,
        "register_style": "formal-analytic",
    },
    "abstract": {
        "require_terminal_stops": True,
        "allow_ellipsis": False,
        "allow_exclamation": False,
        "semicolon_colon_welcome": True,
        "expected_clause_cv_min": 0.20,
        "register_style": "formal-dense",
    },
    "student": {
        "require_terminal_stops": True,
        "allow_ellipsis": False,
        "allow_exclamation": False,
        "semicolon_colon_welcome": True,
        "expected_clause_cv_min": 0.25,
        "register_style": "natural-formal",
    },
    "technical": {
        "require_terminal_stops": True,
        "allow_ellipsis": False,
        "allow_exclamation": False,
        "semicolon_colon_welcome": True,
        "expected_clause_cv_min": 0.20,
        "register_style": "precise-technical",
    },
    "readme": {
        "require_terminal_stops": True,
        "allow_ellipsis": False,
        "allow_exclamation": False,
        "semicolon_colon_welcome": True,
        "expected_clause_cv_min": 0.20,
        "register_style": "direct-operational",
    },
    "procedure": {
        "require_terminal_stops": True,
        "allow_ellipsis": False,
        "allow_exclamation": False,
        "semicolon_colon_welcome": False,
        "expected_clause_cv_min": 0.15,
        "register_style": "imperative-stepwise",
    },
    "api": {
        "require_terminal_stops": True,
        "allow_ellipsis": False,
        "allow_exclamation": False,
        "semicolon_colon_welcome": True,
        "expected_clause_cv_min": 0.15,
        "register_style": "normative-reference",
    },
    "tutorial": {
        "require_terminal_stops": True,
        "allow_ellipsis": False,
        "allow_exclamation": False,
        "semicolon_colon_welcome": True,
        "expected_clause_cv_min": 0.25,
        "register_style": "guiding-instructional",
    },
    "proposal": {
        "require_terminal_stops": True,
        "allow_ellipsis": False,
        "allow_exclamation": False,
        "semicolon_colon_welcome": True,
        "expected_clause_cv_min": 0.25,
        "register_style": "accountable-professional",
    },
    "executive": {
        "require_terminal_stops": True,
        "allow_ellipsis": False,
        "allow_exclamation": False,
        "semicolon_colon_welcome": True,
        "expected_clause_cv_min": 0.20,
        "register_style": "concise-executive",
    },
    "email": {
        "require_terminal_stops": True,
        "allow_ellipsis": False,
        "allow_exclamation": True,
        "semicolon_colon_welcome": True,
        "expected_clause_cv_min": 0.25,
        "register_style": "direct-correspondence",
    },
    "linkedin": {
        "require_terminal_stops": True,
        "allow_ellipsis": True,
        "allow_exclamation": True,
        "semicolon_colon_welcome": True,
        "expected_clause_cv_min": 0.30,
        "register_style": "conversational-professional",
    },
    "personal": {
        "require_terminal_stops": True,
        "allow_ellipsis": True,
        "allow_exclamation": True,
        "semicolon_colon_welcome": True,
        "expected_clause_cv_min": 0.30,
        "register_style": "reflective-narrative",
    },
    "essay": {
        "require_terminal_stops": True,
        "allow_ellipsis": False,
        "allow_exclamation": False,
        "semicolon_colon_welcome": True,
        "expected_clause_cv_min": 0.30,
        "register_style": "argumentative-essay",
    },
    "marketing": {
        "require_terminal_stops": True,
        "allow_ellipsis": True,
        "allow_exclamation": True,
        "semicolon_colon_welcome": True,
        "expected_clause_cv_min": 0.25,
        "register_style": "persuasive-copy",
    },
    "fiction": {
        "require_terminal_stops": True,
        "allow_ellipsis": True,
        "allow_exclamation": True,
        "semicolon_colon_welcome": True,
        "expected_clause_cv_min": 0.30,
        "register_style": "literary-narrative",
    },
    "social": {
        "require_terminal_stops": False,
        "allow_ellipsis": True,
        "allow_exclamation": True,
        "semicolon_colon_welcome": False,
        "expected_clause_cv_min": 0.20,
        "register_style": "casual-social",
    },
    "x": {
        "require_terminal_stops": False,
        "allow_ellipsis": True,
        "allow_exclamation": True,
        "semicolon_colon_welcome": False,
        "expected_clause_cv_min": 0.20,
        "register_style": "microblog-casual",
    },
}


@dataclass(frozen=True)
class PunctuationFinding:
    rule: str
    severity: str  # "review" | "warning"
    category: str  # "boundary_integrity" | "prosody_rhythm" | "genre_fit" | "intentional_informality"
    message: str
    span: str | None = None
    sentence: int | None = None


def mask_non_prosodic_punctuation(text: str) -> str:
    """Mask URLs, decimals, times, abbreviations, initials, and citations.

    Replaces internal periods, commas, and colons inside protected spans with
    placeholder characters so prosodic punctuation counts and sentence-boundary
    checks never misfire on `3.14`, `2:14 a.m.`, `Dr.`, `U.S.`, or URLs.
    """
    masked = mask_for_counts(text)
    masked = _URL_RE.sub(" [url] ", masked)
    masked = _TIME_RE.sub(lambda m: m.group(0).replace(":", "_").replace(".", ""), masked)
    masked = _DECIMAL_OR_NUM_RE.sub(
        lambda m: re.sub(r"[.,:/-]", "_", m.group(0)),
        masked,
    )
    masked = _CITATION_YEAR_RE.sub(" (citation) ", masked)
    masked = _BRACKET_CIT_RE.sub(" [citation] ", masked)
    masked = _ABBR_TOKEN_RE.sub(lambda m: m.group(0)[:-1] + "_", masked)
    masked = _INITIALS_RE.sub(lambda m: m.group(0).replace(".", "_"), masked)
    return masked


def _punctuation_entropy(mark_counts: dict[str, int]) -> float:
    total = sum(mark_counts.values())
    if total <= 0:
        return 0.0
    ent = 0.0
    for count in mark_counts.values():
        if count > 0:
            p = count / total
            ent -= p * math.log2(p)
    return round(ent, 3)


def detect_boundary_anomalies(text: str, genre: str = "linkedin") -> dict:
    """Detect sentence-boundary anomalies vs intentional informality.

    Distinguishes:
    1. Fused sentence boundaries (e.g. 'rising prices He has been') where a
       sentence stop was dropped mid-paragraph.
    2. Tight ellipsis boundaries ('Gujarat...He') where an ellipsis joins two
       sentences without spacing.
    3. Double terminal periods ('today..').
    4. Missing paragraph-final terminal punctuation, classified as
       `intentional_informality` in casual social genres (`social`, `x`) and
       `boundary_loss` in formal/professional genres.
    5. Unbalanced parentheses or brackets.
    """
    norms = GENRE_PUNCTUATION_NORMS.get(genre.lower(), GENRE_PUNCTUATION_NORMS["linkedin"])
    prose = mask_non_prosodic_punctuation(text)

    fused_spans: list[str] = []
    for sent in sentences(text):
        toks = re.findall(r"\b[A-Za-z']+\b", sent)
        if len(toks) < 8:
            continue
        # Look for a lowercase word followed immediately by a capitalized
        # sentence-starter pronoun/adverbial with no intervening punctuation.
        for match in re.finditer(
            r"\b([a-z]{3,})\s+(" + "|".join(_FUSED_STARTERS) + r")\s+([a-z]{2,})\b",
            sent,
        ):
            prev_word = match.group(1).lower()
            if prev_word in _PRE_CAPITAL_ALLOW:
                continue
            fused_spans.append(match.group(0))

    tight_ellipses = [m.group(0) for m in _TIGHT_ELLIPSIS_BOUNDARY_RE.finditer(prose)]
    double_periods = [m.group(0) for m in _DOUBLE_PERIOD_RE.finditer(prose)]

    # Check paragraph-final terminal punctuation on non-heading, non-list paragraphs.
    paras = paragraphs(text)
    unterminated_paras: list[str] = []
    for para in paras:
        stripped = para.strip()
        if not stripped:
            continue
        if re.match(r"^(?:#{1,6}\s|[-*\u2022]\s|\d+[.)]\s|```|>|\|)", stripped):
            continue
        if len(words(stripped)) < 4:
            continue
        if not re.search(r"[.!?\"'\u201d\u2019\u2026)\]]\s*$", stripped):
            unterminated_paras.append(stripped[-60:])

    open_parens = prose.count("(") - prose.count(")")
    unbalanced_parens = open_parens != 0

    require_stops = bool(norms.get("require_terminal_stops", True))
    terminal_omission_status = (
        "none"
        if not unterminated_paras
        else "intentional_informality"
        if not require_stops
        else "boundary_loss"
    )

    has_damage = bool(
        fused_spans
        or tight_ellipses
        or double_periods
        or unbalanced_parens
        or (unterminated_paras and require_stops)
    )

    return {
        "fused_sentences": fused_spans,
        "tight_ellipsis_boundaries": tight_ellipses,
        "double_periods": double_periods,
        "unterminated_paragraphs": unterminated_paras,
        "terminal_omission_status": terminal_omission_status,
        "unbalanced_parentheses": unbalanced_parens,
        "has_boundary_damage": has_damage,
    }


def prosody_profile(text: str, genre: str = "linkedin") -> dict:
    """Measure clause-level prosody, sentence cadence, and structural rhythm."""
    policy: GenrePolicy = get_policy(genre)
    prose = mask_non_prosodic_punctuation(text)
    sents = sentences(text)
    paras = [
        p for p in paragraphs(text)
        if not re.match(r"^(?:#{1,6}\s|```)", p.strip())
    ]
    sent_lengths = [len(words(s)) for s in sents]

    # Clause segments: split each sentence on internal prosodic boundaries.
    clause_lengths: list[int] = []
    clauses_per_sentence: list[int] = []
    intro_comma_sentences = 0
    comma_splice_candidates: list[str] = []
    polysyndeton_sentences: list[str] = []
    fragments: list[str] = []

    for sent in sents:
        masked_sent = mask_non_prosodic_punctuation(sent)
        if _INTRO_COMMA_RE.search(masked_sent):
            intro_comma_sentences += 1
        if _COMMA_SPLICE_PROXY_RE.search(masked_sent):
            comma_splice_candidates.append(sent[:90])
        and_count = len(re.findall(r"\band\b", masked_sent, re.IGNORECASE))
        if and_count >= 3 and len(words(sent)) >= 18:
            polysyndeton_sentences.append(sent[:90])
        if len(words(sent)) < 6 and not _FINITE_VERB_PROXY_RE.search(masked_sent):
            fragments.append(sent[:80])

        raw_clauses = [c.strip() for c in _CLAUSE_SPLIT_RE.split(masked_sent) if words(c)]
        clauses_per_sentence.append(max(1, len(raw_clauses)))
        for cl in raw_clauses:
            w_len = len(words(cl))
            if w_len > 0:
                clause_lengths.append(w_len)

    sent_mean = sum(sent_lengths) / len(sent_lengths) if sent_lengths else 0.0
    sent_sd = pstdev(sent_lengths) if len(sent_lengths) > 1 else 0.0
    sent_cv = (sent_sd / sent_mean) if sent_mean else 0.0

    # Adjacent sentence-length delta (local rhythm contrast: |L_i - L_{i-1}|).
    adj_deltas = [
        abs(b - a) for a, b in zip(sent_lengths, sent_lengths[1:])
    ]
    mean_adj_delta = sum(adj_deltas) / len(adj_deltas) if adj_deltas else 0.0

    clause_mean = sum(clause_lengths) / len(clause_lengths) if clause_lengths else 0.0
    clause_sd = pstdev(clause_lengths) if len(clause_lengths) > 1 else 0.0
    clause_cv = (clause_sd / clause_mean) if clause_mean else 0.0

    para_sent_counts = [len(sentences(p)) for p in paras if sentences(p)]
    para_mean_sents = sum(para_sent_counts) / len(para_sent_counts) if para_sent_counts else 0.0
    para_sd_sents = pstdev(para_sent_counts) if len(para_sent_counts) > 1 else 0.0

    # Monotonous rhythm detection: 5+ sentences with low SD and no internal
    # clause punctuation variation.
    uniform_cadence = (
        len(sent_lengths) >= 6
        and sent_sd < 4.0
        and mean_adj_delta < 3.5
    )
    unpunctuated_long_sentences = [
        s[:90] for s in sents
        if len(words(s)) >= 22 and "," not in s and ";" not in s and ":" not in s
    ]

    return {
        "sentence_count": len(sents),
        "sentence_length_mean": round(sent_mean, 2),
        "sentence_length_sd": round(sent_sd, 2),
        "sentence_length_cv": round(sent_cv, 3),
        "adjacent_length_delta_mean": round(mean_adj_delta, 2),
        "clause_count": len(clause_lengths),
        "clauses_per_sentence_mean": round(
            sum(clauses_per_sentence) / len(clauses_per_sentence), 2
        ) if clauses_per_sentence else 0.0,
        "clause_length_mean": round(clause_mean, 2),
        "clause_length_sd": round(clause_sd, 2),
        "clause_length_cv": round(clause_cv, 3),
        "introductory_comma_rate": round(
            intro_comma_sentences / len(sents), 3
        ) if sents else 0.0,
        "paragraph_count": len(paras),
        "paragraph_sentences_mean": round(para_mean_sents, 2),
        "paragraph_sentences_sd": round(para_sd_sents, 2),
        "single_sentence_paragraph_rate": round(
            sum(1 for c in para_sent_counts if c == 1) / len(para_sent_counts), 3
        ) if para_sent_counts else 0.0,
        "unpunctuated_long_sentences": unpunctuated_long_sentences[:5],
        "comma_splice_candidates": comma_splice_candidates[:5],
        "polysyndeton_chains": polysyndeton_sentences[:5],
        "fragments": {
            "count": len(fragments),
            "spans": fragments[:5],
            "allowed_by_genre": policy.allow_fragments,
        },
        "uniform_cadence": uniform_cadence,
    }


def analyze_punctuation(text: str, genre: str = "linkedin") -> dict:
    """Comprehensive punctuation & prosody analysis for a document."""
    policy: GenrePolicy = get_policy(genre)
    norms = GENRE_PUNCTUATION_NORMS.get(policy.name, GENRE_PUNCTUATION_NORMS["linkedin"])
    clean_text = normalize_for_analysis(text)
    prose = mask_non_prosodic_punctuation(clean_text)
    toks = words(mask_for_counts(clean_text))
    total_words = len(toks)
    sents = sentences(clean_text)
    num_sents = len(sents)

    def per_1k(count: int) -> float:
        return round(count / total_words * 1000, 2) if total_words else 0.0

    ellipses_count = len(_ELLIPSIS_RE.findall(prose))
    prose_no_ellipsis = _ELLIPSIS_RE.sub(" ", prose)

    periods = prose_no_ellipsis.count(".")
    commas = prose_no_ellipsis.count(",")
    semicolons = prose_no_ellipsis.count(";")
    colons = prose_no_ellipsis.count(":")
    questions = prose_no_ellipsis.count("?")
    exclamations = prose_no_ellipsis.count("!")
    em_en_dashes = clean_text.count("\u2014") + clean_text.count("\u2013") + len(re.findall(r"\s--\s", clean_text))
    parentheses = prose_no_ellipsis.count("(")
    quotes = sum(clean_text.count(q) for q in ('"', "\u201c", "\u201d")) // 2

    mark_counts = {
        "periods": periods,
        "commas": commas,
        "semicolons": semicolons,
        "colons": colons,
        "questions": questions,
        "exclamations": exclamations,
        "dashes": em_en_dashes,
        "parentheses": parentheses,
        "ellipses": ellipses_count,
    }
    total_marks = sum(mark_counts.values())
    rates_per_1k = {k: per_1k(v) for k, v in mark_counts.items()}
    entropy = _punctuation_entropy(mark_counts)

    commas_per_sentence = round(commas / num_sents, 2) if num_sents else 0.0
    boundaries = detect_boundary_anomalies(clean_text, policy.name)
    prosody = prosody_profile(clean_text, policy.name)

    findings: list[PunctuationFinding] = []

    # 1. Boundary integrity checks (grammar damage vs intentional informality)
    if boundaries["fused_sentences"]:
        for span in boundaries["fused_sentences"][:3]:
            findings.append(PunctuationFinding(
                rule="punctuation-boundary-damage",
                severity="review",
                category="boundary_integrity",
                message=(
                    "Possible fused sentence boundary (missing period before a new clause). "
                    "Restore a clear sentence stop or conjunction rather than leaving a run-on."
                ),
                span=span,
            ))
    if boundaries["tight_ellipsis_boundaries"]:
        for span in boundaries["tight_ellipsis_boundaries"][:3]:
            findings.append(PunctuationFinding(
                rule="punctuation-boundary-damage",
                severity="review",
                category="boundary_integrity",
                message=(
                    "Ellipsis joins two sentences without spacing or clear boundary convention. "
                    "Use standard sentence punctuation unless matching a casual voice sample."
                ),
                span=span,
            ))
    if boundaries["double_periods"]:
        findings.append(PunctuationFinding(
            rule="punctuation-boundary-damage",
            severity="review",
            category="boundary_integrity",
            message="Double period ('..') detected; replace with a single period or a standard three-dot ellipsis.",
            span="..",
        ))
    if boundaries["unbalanced_parentheses"]:
        findings.append(PunctuationFinding(
            rule="punctuation-boundary-damage",
            severity="review",
            category="boundary_integrity",
            message="Unbalanced parentheses detected; verify every opening parenthesis closes cleanly.",
        ))
    if boundaries["terminal_omission_status"] == "boundary_loss":
        findings.append(PunctuationFinding(
            rule="punctuation-boundary-damage",
            severity="review",
            category="boundary_integrity",
            message=(
                f"Paragraph ends without terminal punctuation in '{policy.name}' genre. "
                "Keep terminal stops in formal, technical, and professional prose."
            ),
            span=boundaries["unterminated_paragraphs"][0],
        ))

    # 2. Genre fit checks
    if ellipses_count > 0 and not norms.get("allow_ellipsis", False):
        findings.append(PunctuationFinding(
            rule="punctuation-genre-mismatch",
            severity="review",
            category="genre_fit",
            message=(
                f"Ellipses appear in '{policy.name}' prose ({ellipses_count} found). "
                "In formal, technical, or academic writing, state the complete list or claim explicitly."
            ),
            span="...",
        ))
    if exclamations > 0 and not norms.get("allow_exclamation", False):
        findings.append(PunctuationFinding(
            rule="punctuation-genre-mismatch",
            severity="review",
            category="genre_fit",
            message=(
                f"Exclamation mark used in '{policy.name}' register. "
                "Let the evidence or instruction carry the emphasis."
            ),
            span="!",
        ))
    if prosody["fragments"]["count"] > 0 and not policy.allow_fragments:
        findings.append(PunctuationFinding(
            rule="punctuation-fragment-review",
            severity="review",
            category="genre_fit",
            message=(
                f"Sentence fragment candidate in '{policy.name}' prose, where complete clauses are expected."
            ),
            span=prosody["fragments"]["spans"][0],
        ))

    # 3. Prosody and rhythm checks
    if prosody["unpunctuated_long_sentences"]:
        findings.append(PunctuationFinding(
            rule="prosodic-cadence",
            severity="review",
            category="prosody_rhythm",
            message=(
                "Long sentence (22+ words) has no internal punctuation. Check whether a comma, "
                "clause break, or split would clarify the structure for the reader."
            ),
            span=prosody["unpunctuated_long_sentences"][0],
        ))
    if num_sents >= 6 and commas == 0 and total_words >= 75:
        findings.append(PunctuationFinding(
            rule="punctuation-uniformity",
            severity="review",
            category="prosody_rhythm",
            message=(
                "Multi-sentence passage uses only terminal periods with zero internal clause punctuation. "
                "Check whether clause relationships (contrast, qualification, subordination) are overly flattened."
            ),
        ))
    if prosody["comma_splice_candidates"]:
        findings.append(PunctuationFinding(
            rule="punctuation-boundary-damage",
            severity="review",
            category="boundary_integrity",
            message=(
                "Possible comma splice joining two independent clauses. "
                "Use a period, semicolon, or coordinating conjunction."
            ),
            span=prosody["comma_splice_candidates"][0],
        ))
    if prosody["introductory_comma_rate"] >= 0.5 and num_sents >= 5:
        findings.append(PunctuationFinding(
            rule="prosodic-cadence",
            severity="review",
            category="prosody_rhythm",
            message=(
                "Half or more of the sentences open with a front-loaded comma clause. "
                "Vary clause order so the subject and verb arrive earlier in some sentences."
            ),
        ))

    return {
        "genre": policy.name,
        "register_style": norms.get("register_style", "general"),
        "word_count": total_words,
        "sentence_count": num_sents,
        "counts": {
            **mark_counts,
            "quotes": quotes,
            "total_marks": total_marks,
        },
        "rates_per_1k": rates_per_1k,
        "commas_per_sentence": commas_per_sentence,
        "punctuation_entropy": entropy,
        "boundaries": boundaries,
        "prosody": prosody,
        "findings": [asdict(f) for f in findings],
        "note": (
            "Punctuation diagnostics evaluate readability, boundary reliability, and genre/voice fit. "
            "Never delete required punctuation or introduce run-ons to alter detector scores."
        ),
    }


def compare_punctuation_voice(reference_text: str, draft_text: str, genre: str = "linkedin") -> dict:
    """Compare writer-specific punctuation and prosodic tendencies between reference and draft."""
    ref = analyze_punctuation(reference_text, genre)
    drf = analyze_punctuation(draft_text, genre)

    notes: list[str] = []
    comparisons: dict[str, dict] = {}

    for key, label, tol in (
        ("commas", "comma rate", 0.50),
        ("semicolons", "semicolon rate", 0.75),
        ("colons", "colon rate", 0.75),
        ("parentheses", "parenthetical rate", 0.75),
        ("questions", "question mark rate", 0.65),
    ):
        r_val = ref["rates_per_1k"][key]
        d_val = drf["rates_per_1k"][key]
        if r_val == 0 and d_val == 0:
            verdict = "same (both absent)"
        elif r_val == 0:
            verdict = "introduced in draft" if d_val >= 2.0 else "aligned"
        else:
            change = abs(d_val - r_val) / r_val
            verdict = "aligned" if change <= tol else "drifted"
        if verdict == "drifted":
            notes.append(f"punctuation {label} drifted: reference {r_val}/1k, draft {d_val}/1k")
        comparisons[key] = {"reference_per_1k": r_val, "draft_per_1k": d_val, "verdict": verdict}

    ref_ent = ref["punctuation_entropy"]
    drf_ent = drf["punctuation_entropy"]
    ref_clause_cv = ref["prosody"]["clause_length_cv"]
    drf_clause_cv = drf["prosody"]["clause_length_cv"]

    drifted_count = sum(1 for item in comparisons.values() if item["verdict"] == "drifted")

    return {
        "reference_words": ref["word_count"],
        "draft_words": drf["word_count"],
        "rates_comparison": comparisons,
        "punctuation_entropy": {"reference": ref_ent, "draft": drf_ent},
        "clause_length_cv": {"reference": ref_clause_cv, "draft": drf_clause_cv},
        "drifted_marks": drifted_count,
        "overall": "aligned" if drifted_count <= 1 else "drifted",
        "notes": notes,
    }
