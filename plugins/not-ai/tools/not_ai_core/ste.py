"""ASD-STE100-inspired / verified checks (Not-AI 3.0, E10).

- inspired: public-principle heuristics, always labelled provisional.
- verify: against user-supplied dictionary + glossary files. Never bundled.
- Never prints "ASD-STE100 compliant" without user authority sign-off; the
  strongest verify-mode language is "consistent with supplied dictionary+glossary".
"""

from __future__ import annotations

import re
from pathlib import Path

from .text import mask_for_counts, sentences, words

# Tiny illustrative stop-list. NOT the official dictionary (proprietary).
ILLUSTRATIVE_NON_APPROVED = {
    "utilize": "use", "utilizes": "uses", "utilizing": "use",
    "leverage": "use", "facilitate": "help", "prioritize": "give priority to",
    "commence": "begin", "terminate": "stop", "ascertain": "find out",
    "accomplish": "do", "endeavor": "try", "sufficient": "enough",
}

ING_OPENER = re.compile(r"^(?:[A-Za-z]+ing)\b[^.!?]{0,100},")
LONG_SENT = 25


def _load_list(path: str | None) -> dict[str, str]:
    """Load user dictionary/glossary: `term = alternative` or `term: meaning` per line; also JSON {term: entry}."""
    if not path:
        return {}
    p = Path(path)
    if not p.is_file():
        raise FileNotFoundError(f"dictionary/glossary file not found: {path}")
    text = p.read_text(encoding="utf-8")
    try:
        import json
        data = json.loads(text)
        if isinstance(data, dict):
            return {str(k).lower(): str(v) for k, v in data.items()}
    except ValueError:
        pass
    out: dict[str, str] = {}
    for line in text.splitlines():
        line = line.strip()
        if not line or line.startswith("#"):
            continue
        for sep in ("=", ":"):
            if sep in line:
                k, v = line.split(sep, 1)
                out[k.strip().lower()] = v.strip()
                break
        else:
            # Bare term per line (glossary style): approved as-is.
            out[line.lower()] = "approved technical term (from supplied glossary)"
    return out


def check_inspired(text: str) -> dict:
    prose = mask_for_counts(text)
    items = sentences(text)
    toks = [w.lower() for w in words(prose)]
    findings: list[dict] = []
    for w, alt in ILLUSTRATIVE_NON_APPROVED.items():
        if w in toks:
            findings.append({"rule": "ste-inspired", "span": w,
                             "note": f"Illustrative non-approved word; official dictionary suggests '{alt}'. Confirm against authorised Issue 9 copy."})
    for i, s in enumerate(items, 1):
        if len(words(s)) > LONG_SENT and i <= 20:
            findings.append({"rule": "ste-inspired", "span": s[:60], "sentence": i,
                             "note": f"Sentence is {len(words(s))} words (>~{LONG_SENT}). STE procedures prefer one instruction per short sentence."})
            break
    for i, s in enumerate(items, 1):
        if ING_OPENER.search(s.strip()):
            findings.append({"rule": "ste-inspired", "span": s[:60], "sentence": i,
                             "note": "Restricted -ing opener. Rewrite as an explicit condition or a separate imperative."})
            break
    if re.search(r"\b(is|are|was|were)\s+\w+(ed|en)\b", prose, re.IGNORECASE) and \
       re.search(r"\b(step|procedure|install|remove|torque|inspect)\b", prose, re.IGNORECASE):
        findings.append({"rule": "ste-inspired", "span": "passive in procedure",
                         "note": "Procedural steps prefer active imperatives ('Remove the cover', not 'The cover must be removed')."})
    warn_pos = prose.casefold().find("warning")
    step_m = re.search(r"\b(step\s*1|first,|install|remove)\b", prose, re.IGNORECASE)
    if warn_pos != -1 and step_m and warn_pos > step_m.start():
        findings.append({"rule": "ste-inspired", "span": "warning placement",
                         "note": "Warning appears after the action. STE places warnings/cautions BEFORE the dangerous step."})
    return {"mode": "inspired", "findings": findings,
            "disclaimer": "STE-inspired provisional review. Not ASD-STE100 compliant. Consult the official Issue 9 standard."}


def check_verify(text: str, dictionary: str, glossary: str) -> dict:
    dic = _load_list(dictionary)
    glo = _load_list(glossary)
    if not dic:
        raise ValueError("verify mode needs a non-empty --dictionary (authorised Issue 9 reference)")
    if not glo:
        raise ValueError("verify mode needs a non-empty --glossary (approved technical nouns/verbs)")
    low = mask_for_counts(text).lower()
    findings: list[dict] = []
    for term, alt in dic.items():
        if re.search(rf"\b{re.escape(term)}\b", low):
            findings.append({"rule": "ste-verified", "span": term,
                             "note": f"Dictionary entry: '{term}' → '{alt}' (from supplied dictionary)."})
    # Terminology drift: glossary term appears in variant casing/plural inconsistently.
    for term in glo:
        base = term.lower()
        variants = {base, base + "s", base.rstrip("s")}
        seen = {v for v in variants if re.search(rf"\b{re.escape(v)}\b", low)}
        if len(seen) > 1:
            findings.append({"rule": "ste-verified", "span": term,
                             "note": f"Term '{term}' appears in multiple forms {sorted(seen)}. Use one approved form consistently."})
    return {"mode": "verify", "findings": findings,
            "checked_against": {"dictionary_terms": len(dic), "glossary_terms": len(glo)},
            "disclaimer": "Verified against SUPPLIED dictionary+glossary only. Not an ASD-STE100 compliance claim."}
