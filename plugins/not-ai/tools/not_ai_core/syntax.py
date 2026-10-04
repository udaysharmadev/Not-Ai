"""Syntax / density diagnostics with honest proxy naming (Not-AI 3.0).

- nominalization_suffix_proxy: stdlib suffix regex (over-counts ~5x).
- parsed_nominalization_count: only populated by the optional NLP adapter.
- Never compare the two numerically. Density is genre-relative (E01/E02).
"""

from __future__ import annotations

import re

from .text import mask_for_counts, sentences, words

NOM_SUFFIX = re.compile(r"\b\w+(?:tion|sion|ment|ness|ance|ence|ity|ization)\b", re.IGNORECASE)
PASSIVE_PROXY = re.compile(r"\b(am|is|are|was|were|be|been|being)\s+\w+(?:ed|en)\b", re.IGNORECASE)
PREPOSITIONS = {'of', 'in', 'to', 'for', 'on', 'with', 'at', 'by', 'from',
                'into', 'through', 'during', 'before', 'after', 'above', 'below',
                'between', 'among', 'under', 'about', 'against', 'without', 'within',
                'around', 'along', 'following', 'across', 'behind', 'beyond'}


def syntax_profile(text: str, parsed: dict | None = None) -> dict:
    prose = mask_for_counts(text)
    toks = words(prose)
    items = sentences(text)
    n = len(toks)
    nom_proxy = len(NOM_SUFFIX.findall(prose))
    nom_rate_proxy = round(nom_proxy / n * 1000, 1) if n else 0.0
    prep_rate = round(sum(1 for w in toks if w.lower() in PREPOSITIONS) / n, 3) if n else 0.0
    passive_n = sum(1 for s in items if PASSIVE_PROXY.search(s))
    # Attributive adjective density proxy: 2+ consecutive Capitalized/lowercase
    # adjectives before a noun is unparseable without POS; use Adj-Noun bigrams via suffix list.
    adjish = len(re.findall(r"\b(?:[a-z]+(?:al|ive|ous|ful|able|ible|ic|ical))\s+[a-z]+(?:tion|ment|ness|ity|ance|ence)?\w*\b", prose, re.IGNORECASE))
    long_np = len(re.findall(r"\b(?:[A-Z][a-z]*\s+){2,}[A-Z]?[a-z]+\b", prose))
    verbs = len(re.findall(r"\b(?:is|are|was|were|be|has|have|had|do|does|did|will|would|can|could|may|might|must|make|made|take|took|give|gave|use|used)\b", prose, re.IGNORECASE))
    nouns_proxy = nom_proxy + len(re.findall(r"\b[A-Z][a-z]+\b", prose))
    out = {
        "nominalization_suffix_proxy": nom_proxy,
        "nominalization_suffix_proxy_per_1000": nom_rate_proxy,
        "note_proxy": "Over-counts ~5x vs tagged rates (counts nation/moment). Compare only proxy-to-proxy.",
        "parsed_nominalization_count": (parsed or {}).get("nominalizations"),
        "note_parsed": "Populated only by optional NLP adapter; never compare numerically with the proxy.",
        "preposition_rate": prep_rate,
        "attributive_adjective_proxy": adjish,
        "long_noun_phrase_proxy": long_np,
        "noun_to_verb_balance_proxy": round(nouns_proxy / verbs, 2) if verbs else 0.0,
        "passive_proxy_sentences": passive_n,
        "passive_proxy_rate": round(passive_n / len(items), 3) if items else 0.0,
        "passive_note": "Models underuse agentless passives; low figure is not automatically good.",
    }
    # Genre-relative reading, not a reduction target.
    density_score = prep_rate * 200 + nom_rate_proxy / 2
    out["density_score_proxy"] = round(density_score, 1)
    out["assessment"] = ("dense for conversational genres; may be normal for academic/technical"
                         if density_score > 50 else "moderate" if density_score > 30 else "conversational range")
    out["question"] = "Is this amount and type of density appropriate for the current genre and reader?"
    return out
