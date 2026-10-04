"""Discourse and cohesion analysis (Not-AI 3.0).

A sentence can be grammatical and still badly connected. Measures:
adjacent content overlap, topic continuity, abrupt subject shifts, pronoun
antecedent ambiguity, connective function/variety/repetition, paragraph topic
concentration, paragraph-to-paragraph transitions, repeated conclusions.

Connectives classified by relation (additive/contrastive/causal/temporal/
conditional/exemplifying/reformulating/conclusive); the question is always
whether the relation is real, never "more connectives = better".
"""

from __future__ import annotations

import re
from collections import Counter

from .text import mask_for_counts, paragraphs, sentences, words

CONNECTIVES: dict[str, list[str]] = {
    "additive": ["moreover", "furthermore", "additionally", "in addition", "also", "besides"],
    "contrastive": ["however", "but", "nevertheless", "nonetheless", "on the other hand", "yet", "although", "though"],
    "causal": ["because", "therefore", "consequently", "as a result", "thus", "hence", "so"],
    "temporal": ["then", "afterwards", "meanwhile", "subsequently", "finally", "earlier", "later"],
    "conditional": ["if", "unless", "provided", "otherwise"],
    "exemplifying": ["for example", "for instance", "such as", "including"],
    "reformulating": ["in other words", "that is", "namely", "i.e."],
    "conclusive": ["in conclusion", "to summarize", "in summary", "overall"],
}

_STOP = {"the", "a", "an", "of", "in", "to", "is", "are", "and", "or", "but",
        "for", "that", "this", "it", "on", "at", "by", "as", "with", "from",
        "be", "was", "were", "we", "you", "they", "i", "he", "she", "it"}


def _content_set(sent: str) -> set[str]:
    return {w.lower() for w in words(sent) if w.lower() not in _STOP and len(w) > 3}


def _subjects(sent: str) -> str:
    toks = words(sent)
    return toks[0].lower() if toks else ""


_PRONOUNS = {"he", "she", "it", "they", "this", "these", "that", "those", "which", "who"}


def cohesion(text: str) -> dict:
    items = sentences(text)
    paras = paragraphs(text)
    if not items:
        return {"sentences": 0, "note": "no sentences to connect"}
    sets = [_content_set(s) for s in items]
    overlaps = []
    for a, b in zip(sets, sets[1:]):
        union = a | b
        overlaps.append(round(len(a & b) / len(union), 3) if union else 0.0)
    abrupt = 0
    subj_shifts = []
    for i in range(1, len(items)):
        if not (sets[i] & sets[i - 1]) and _subjects(items[i]) != _subjects(items[i - 1]):
            # No shared content and new subject with zero overlap: abrupt.
            if len(sets[i]) and len(sets[i - 1]):
                abrupt += 1
                subj_shifts.append(i + 1)  # 1-indexed sentence number
    # Pronoun antecedent ambiguity: sentence opens with pronoun, previous
    # sentence has 2+ properish candidates.
    ambiguous = []
    proper_re = re.compile(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}\b")
    for i, s in enumerate(items):
        toks = words(s)
        if toks and toks[0].lower() in _PRONOUNS and i > 0:
            cands = proper_re.findall(items[i - 1])
            if len(set(cands)) >= 2:
                ambiguous.append({"sentence": i + 1, "span": s[:80]})
    # Connective function + variety.
    low = mask_for_counts(text).lower()
    conn_hits: dict[str, dict[str, int]] = {}
    total_conn = 0
    for rel, markers in CONNECTIVES.items():
        for m in markers:
            c = len(re.findall(r"\b" + re.escape(m) + r"\b", low))
            if c:
                conn_hits.setdefault(rel, {})[m] = c
                total_conn += c
    variety = len([m for rel in conn_hits.values() for m in rel])
    repeated_conn = {rel: dict(m) for rel, m in conn_hits.items()
                     if sum(m.values()) >= 3}
    # Paragraph topic drift: first-sentence content sets across paragraphs.
    para_firsts = []
    for p in paras:
        ss = sentences(p)
        if ss:
            para_firsts.append(_content_set(ss[0]))
    drift = 0
    for a, b in zip(para_firsts, para_firsts[1:]):
        union = a | b
        if not (a & b) and union:
            drift += 1
    # Repeated conclusions: same content trigram in final sentences.
    finals = []
    for p in paras:
        ss = sentences(p)
        if ss:
            finals.append(" ".join(sorted(_content_set(ss[-1]))[:6]))
    repeated_conclusion = len(finals) - len(set(finals)) if finals else 0
    avg_overlap = round(sum(overlaps) / len(overlaps), 3) if overlaps else 0.0
    return {
        "sentences": len(items),
        "paragraphs": len(paras),
        "adjacent_mean_overlap": avg_overlap,
        "zero_overlap_adjacent": sum(1 for o in overlaps if o == 0.0),
        "abrupt_subject_shifts": {"count": abrupt, "sentences": subj_shifts[:10]},
        "pronoun_ambiguous": ambiguous[:5],
        "connectives": {"by_relation": conn_hits, "total": total_conn,
                        "variety": variety, "repeated_relations": repeated_conn,
                        "note": "A connective is bad only when the relation is absent or obvious without it."},
        "paragraph_drift": drift,
        "repeated_conclusions": repeated_conclusion,
        "assessment": ("fragmented" if avg_overlap == 0.0 and len(items) >= 4
                       else "review connections" if abrupt >= 2 or drift >= 2
                       else "connected"),
    }
