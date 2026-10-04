"""Information-structure review (Not-AI 3.0).

Paragraph roles: claim, evidence, mechanism, example, qualification, contrast,
setup, request, instruction, warning, transition, reflection, conclusion.
A paragraph with no useful role is a deletion/merger candidate.

Reviews given→new progression, topic-comment flow, referential continuity,
paragraph focus, and sentence-to-sentence information flow. Pragmatic lens
(relevance/quantity/clarity/ambiguity/reader inference burden) is converted
into concrete editorial questions, not slogans.
"""

from __future__ import annotations

import re

from .text import paragraphs, sentences, words

ROLE_CUES: dict[str, list[str]] = {
    "request": ["please", "could you", "would you", "need", "by friday", "deadline", "action required"],
    "instruction": ["step", "first,", "next,", "then ", "install", "run ", "click", "type "],
    "warning": ["warning", "caution", "danger", "do not", "never ", "must not", "before you"],
    "example": ["for example", "for instance", "e.g.", "such as"],
    "evidence": ["data", "result", "measured", "observed", "study", "survey", "%", "figure"],
    "mechanism": ["because", "since ", "due to", "caused by", "through ", "by "],
    "qualification": ["however", "although", "though", "except", "unless", "despite", "while "],
    "contrast": ["but ", "however", "on the other hand", "in contrast", "whereas"],
    "conclusion": ["in conclusion", "overall", "therefore", "thus ", "in short"],
    "transition": ["moreover", "furthermore", "additionally", "meanwhile"],
    "reflection": ["i think", "i feel", "in my experience", "i learned"],
    "claim": ["we ", "our ", "the ", "this "],
    "setup": [],
}


def paragraph_role(para: str) -> dict:
    low = para.casefold()
    scores: dict[str, int] = {}
    for role, cues in ROLE_CUES.items():
        scores[role] = sum(1 for c in cues if c in low)
    # Structural roles override weak lexical cues.
    if re.match(r"^#{1,6}\s", para.strip()):
        return {"role": "setup", "confidence": "low", "note": "heading"}
    if "?" in para[:200]:
        return {"role": "request" if any(w in low for w in ("please", "could", "would", "need")) else "setup",
                "confidence": "medium", "note": "question-led paragraph"}
    best = max(scores, key=lambda k: scores[k])
    if scores[best] == 0:
        # No cue: claim by default only if it asserts; else no-role candidate.
        sents = sentences(para)
        if len(sents) >= 2:
            return {"role": "claim", "confidence": "low",
                    "note": "no cue words; verify it asserts something checkable"}
        return {"role": "none", "confidence": "medium",
                "note": "No identifiable job (claim/evidence/mechanism/example/qualification/contrast/setup/request/instruction/warning/transition/reflection/conclusion). Consider deletion or merger."}
    return {"role": best, "confidence": "medium" if scores[best] >= 2 else "low",
            "note": "cue-based proxy; agent confirms against purpose"}


def given_new_flow(text: str) -> dict:
    """Check given-before-new: does each sentence reuse something known before adding new?"""
    items = sentences(text)
    seen: set[str] = set()
    findings = []
    stop = {"the", "a", "an", "of", "in", "to", "is", "are", "and", "or", "but",
            "for", "that", "this", "it", "on", "at", "by", "as", "with", "from"}
    for i, s in enumerate(items, 1):
        content = [w.lower() for w in words(s) if w.lower() not in stop and len(w) > 3]
        if not content:
            continue
        if i == 1:
            seen.update(content)
            continue
        if not (set(content) & seen):
            findings.append({"sentence": i, "span": s[:80],
                             "note": "Introduces only new referents; consider linking to prior sentence (given→new)."})
        seen.update(content)
    return {"sentences": len(items), "given_new_breaks": findings[:8],
            "count": len(findings)}


def document_map(text: str) -> dict:
    """Global map for long documents: purpose, claims, terminology, chronology."""
    paras = paragraphs(text)
    roles = [paragraph_role(p) for p in paras]
    # Defined terminology: ALLCAPS or quoted introductions ("X" means...).
    defined = sorted(set(re.findall(r'"([^"\n]{2,40})"\s+(?:means|is|refers)', text)))[:10]
    # Chronology markers.
    chrono = re.findall(r"\b(?:19|20)\d{2}\b|\b\d{1,2}:\d{2}\s*(?:a\.m\.|p\.m\.)?\b|\b(?:before|after|then|next|finally)\b", text, re.IGNORECASE)[:10]
    # Repeated concepts (candidate terminology drift).
    toks = [w.lower() for w in words(text) if len(w) > 5]
    from collections import Counter
    repeated = dict(Counter(toks).most_common(10))
    return {"paragraphs": len(paras), "roles": [r["role"] for r in roles],
            "role_details": roles, "defined_terms": defined,
            "chronology_markers": chrono, "top_content_words": repeated,
            "flow": given_new_flow(text)}


def editorial_questions(text: str) -> list[str]:
    """Pragmatic lens as concrete questions (relevance/quantity/clarity/burden)."""
    q = []
    flow = given_new_flow(text)
    if flow["count"] >= 2:
        q.append(f"Relevance/clarity: {flow['count']} sentences introduce all-new referents — which prior idea does each continue?")
    roles = [paragraph_role(p)["role"] for p in paragraphs(text)]
    if "none" in roles:
        q.append("Quantity: a paragraph has no identifiable job — delete or merge it?")
    if roles.count("conclusion") >= 2:
        q.append("Quantity: repeated conclusions — keep the one with the consequence/decision, cut the rest?")
    if "warning" in roles:
        q.append("Usability/safety: is every warning placed BEFORE its dangerous action with prerequisites visible?")
    q.append("Inference burden: are actors, pronouns, and term references unambiguous to this reader?")
    return q
