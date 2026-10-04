"""Lexical analysis without word-policing (Not-AI 3.0).

- TTR is reported but never sufficient on its own.
- MTLD (threshold 0.72, McCarthy & Jarvis 2010) and HD-D (draws 42) are stdlib.
- vocd-D curve-fitting is NOT implemented (needs random sampling + fitting;
  HD-D is the supported alternative per E06).
- All proxy metrics carry `_proxy` suffixes where they differ from parsed research
  rates. Thresholds are proxy-scale heuristics, never human targets.

Decisions consider genre, field terminology, author habit, surrounding phrase,
and within-document frequency. One occurrence rarely triggers anything; clusters
and phrase patterns do.
"""

from __future__ import annotations

import math
import re
from collections import Counter

from .text import mask_for_counts, tokenize_words

MTLD_THRESHOLD = 0.72
HDD_DRAWS = 42
MIN_TOKENS_LEXDIV = 50

STOPWORDS = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'shall', 'can', 'to', 'of', 'in', 'for',
    'on', 'with', 'at', 'by', 'from', 'up', 'about', 'into', 'through',
    'and', 'or', 'but', 'not', 'as', 'so', 'if', 'it', 'its', 'this',
    'that', 'these', 'those', 'i', 'you', 'he', 'she', 'we', 'they',
    'my', 'your', 'his', 'her', 'our', 'their', 'me', 'him', 'us', 'them',
    'what', 'which', 'who', 'whom', 'when', 'where', 'why', 'how',
    'all', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
    'than', 'too', 'very', 's', 't', 'just', 'don', 'now',
}


def _alpha_tokens(text: str) -> list[str]:
    prose = mask_for_counts(text)
    return re.findall(r"\b[a-z]+\b", prose.lower())


def ttr(text: str) -> dict:
    toks = _alpha_tokens(text)
    if not toks:
        return {"ttr": 0.0, "tokens": 0, "types": 0, "note": "no tokens"}
    return {"ttr": round(len(set(toks)) / len(toks), 3),
            "tokens": len(toks), "types": len(set(toks)),
            "note": "Length-sensitive; never use alone (E06)."}


def content_ttr(text: str) -> dict:
    toks = _alpha_tokens(text)
    content = [w for w in toks if w not in STOPWORDS and len(w) > 3]
    if not content:
        return {"content_ttr": 0.0, "content_tokens": 0, "content_types": 0}
    return {"content_ttr": round(len(set(content)) / len(content), 3),
            "content_tokens": len(content), "content_types": len(set(content))}


def mtld(text: str, threshold: float = MTLD_THRESHOLD) -> dict:
    """Measure of Textual Lexical Diversity (McCarthy 2005; McCarthy & Jarvis 2010).

    Mean length of sequential word strings maintaining TTR >= threshold.
    Forward + backward passes averaged, as in the standard formulation.
    Stdlib, deterministic. Unstable below ~50 tokens — reported with caution.
    """
    toks = _alpha_tokens(text)
    n = len(toks)
    if n < 10:
        return {"mtld": 0.0, "factors": 0, "tokens": n,
                "caution": "too short for MTLD; needs 50+ tokens for stability"}

    def _factors(seq: list[str]) -> tuple[int, float]:
        factors = 0
        types: set[str] = set()
        run = 0
        for tok in seq:
            run += 1
            types.add(tok)
            if len(types) / run < threshold:
                factors += 1
                types, run = set(), 0
        partial = 0.0
        if run:
            partial = (1 - (len(types) / run)) / (1 - threshold) if threshold != 1 else 0.0
            partial = max(0.0, min(1.0, partial))
        return factors, partial

    f_f, p_f = _factors(toks)
    f_b, p_b = _factors(list(reversed(toks)))
    full = f_f + p_f + f_b + p_b
    # Standard MTLD can exceed token count on highly diverse short texts;
    # cap is not standard — report raw value with the factor count instead.
    value = (2 * n / full) if full else 0.0
    out: dict = {"mtld": round(value, 2), "factors_forward": f_f,
                 "factors_backward": f_b, "tokens": n, "threshold": threshold}
    if n < MIN_TOKENS_LEXDIV:
        out["caution"] = f"{n} tokens; MTLD unstable below ~{MIN_TOKENS_LEXDIV}"
    return out


def hd_d(text: str, draws: int = HDD_DRAWS) -> dict:
    """Hypergeometric Distribution Diversity (McCarthy & Jarvis 2007, 2010).

    For each type t with frequency f in N tokens: p = P(at least one t in a
    random sample of `draws` tokens) = 1 - C(N-f, draws)/C(N, draws).
    HD-D = sum_t p / draws. Exact combinatorics via log-factorials (stdlib).
    """
    toks = _alpha_tokens(text)
    n = len(toks)
    if n == 0:
        return {"hd_d": 0.0, "tokens": 0, "draws": draws}
    if draws >= n:
        draws = max(1, n - 1)
    freq = Counter(toks)

    from math import lgamma

    def _log_c(nn: int, kk: int) -> float:
        if kk < 0 or kk > nn:
            return float("-inf")
        return lgamma(nn + 1) - lgamma(kk + 1) - lgamma(nn - kk + 1)

    log_denom = _log_c(n, draws)
    total = 0.0
    for f in freq.values():
        if n - f < draws:
            p = 1.0
        else:
            p = 1.0 - math.exp(_log_c(n - f, draws) - log_denom)
        total += p
    return {"hd_d": round(total / draws, 4), "tokens": n, "draws": draws,
            "types": len(freq)}


def lexical_profile(text: str) -> dict:
    """All diversity indices together (E06: use more than one index)."""
    t = ttr(text)
    c = content_ttr(text)
    m = mtld(text)
    h = hd_d(text)
    toks = _alpha_tokens(text)
    avg_len = round(sum(len(w) for w in toks) / len(toks), 2) if toks else 0.0
    assessment = "report indices separately; no universal target"
    if toks and len(toks) < MIN_TOKENS_LEXDIV:
        assessment += f"; text has {len(toks)} tokens (<{MIN_TOKENS_LEXDIV}), treat as unstable"
    return {"ttr": t, "content_ttr": c, "mtld": m, "hd_d": h,
            "avg_word_len": avg_len, "assessment": assessment}


# --- Phrase patterns (structural categories, not word bans) ---

PHRASE_PATTERNS: tuple[tuple[str, str, str], ...] = (
    ("significance-inflation", r"\bplays?\s+a\s+crucial\s+role\b|\bserves?\s+as\s+a\s+testament\b|\bunderscores?\s+the\s+importance\b", "generic adjective + abstract noun + empty significance claim"),
    ("unsupported-praise", r"\bgroundbreaking\b|\brevolutionary\b|\btransformative\b|\bcutting-edge\b", "praise needs a supplied result"),
    ("empty-universality", r"\bin\s+today'?s\s+(fast-paced|ever-changing|rapidly\s+changing)\s+world\b|\beveryone\s+knows\b", "universal scene-setting with no claim"),
    ("abstract-stacking", r"\b(?:implementation|utilization|facilitation|optimization)\s+of\s+(?:the\s+)?\w+", "nominal packaging hiding actor/action"),
    ("ceremonial-conclusion", r"\bin\s+conclusion\b[,\s]+(?:it\s+is\s+clear\s+that\s+)?", "summary repeating the paragraph without adding anything"),
    ("copula-avoidance", r"\bserves?\s+as\b|\bstands?\s+as\b|\bfunctions?\s+as\b", "plain 'is' usually clearer"),
    ("mechanical-contrast", r"\bnot\s+(?:just|only|merely)\b[^.!?]{1,80}?\bbut\b", "cadence, not argument, unless denying X does work"),
    ("synthetic-vulnerability", r"\bI\s+(?:failed|cried|broke\s+down)\b[^.!?]{0,60}?\b(?:and\s+)?(?:here'?s\s+what\s+I\s+learned|lesson)\b", "staged confession + inflated lesson without supplied event"),
    ("listicle-padding", r"\b(?:firstly|secondly|thirdly)\b", "enumerators padding thin content"),
    ("generic-lesson", r"\b(?:the\s+)?lessons?\s+(?:we\s+can\s+)?learn\b|\bkey\s+takeaways?\b", "lesson label without the supplied specifics"),
)

_COMPILED_PATTERNS = tuple((n, re.compile(p, re.IGNORECASE), d) for n, p, d in PHRASE_PATTERNS)


def phrase_patterns(text: str) -> dict:
    prose = mask_for_counts(text)
    prose = re.sub(r'"[^"\n]{1,200}"', " ", prose)
    hits = []
    for name, pat, desc in _COMPILED_PATTERNS:
        for m in pat.finditer(prose):
            hits.append({"pattern": name, "span": m.group(0)[:80], "note": desc})
    # Within-document repetition matters more than single occurrence.
    toks = _alpha_tokens(text)
    counts = Counter(toks)
    repeated_stock = {w: c for w, c in counts.items() if c >= 3 and len(w) > 5}
    return {"hits": hits, "hit_count": len(hits),
            "repeated_content_words_3plus": dict(sorted(repeated_stock.items(), key=lambda kv: -kv[1])[:10]),
            "note": "One occurrence rarely matters. A cluster (generic adjective + abstract noun + empty claim) is the signal."}
