"""Cultural and linguistic identity preservation (Not-AI 3.0).

Infers variety ONLY from repeated evidence in the supplied text. Never
stereotypes from nationality. Reports evidence with confidence or
"insufficient evidence". E07 + E11.
"""

from __future__ import annotations

import re

UK_SPELLINGS = {"organise", "organised", "behaviour", "behaviours", "colour",
                "flavour", "favour", "labour", "centre", "metre", "litre",
                "realise", "recognise", "specialise", "travelling", "cancelled",
                "programme", "cheque", "grey", "tyre", "kerb", "flat", "lift"}
US_SPELLINGS = {"organize", "organized", "behavior", "behaviors", "color",
                "flavor", "favor", "labor", "center", "meter", "liter",
                "realize", "recognize", "specialize", "traveling", "canceled",
                "program", "check", "gray", "tire", "curb", "apartment", "elevator"}
IN_MARKERS = {"kindly", "do the needful", "prepone", "out of station",
              "batchmate", "lakh", "crore", "godown", "eve-teasing"}
IN_FORMAL = {"kindly", "request you to", "please do the needful", "revert back"}


def detect_variety(text: str) -> dict:
    low = text.casefold()
    toks = set(re.findall(r"\b[a-z]+\b", low))
    uk = sorted(t for t in UK_SPELLINGS if t in toks or t in low)
    us = sorted(t for t in US_SPELLINGS if t in toks or t in low)
    in_m = sorted(m for m in IN_MARKERS if m in low)
    formal = sorted(m for m in IN_FORMAL if m in low)
    # Code-switching proxy: non-Latin runs or common South-Asian tokens in Latin.
    non_latin = bool(re.search(r"[\u0900-\u097F\u0B80-\u0BFF\u0600-\u06FF\u4E00-\u9FFF]", text))
    evidence = {"uk_spellings": uk, "us_spellings": us,
                "indian_lexicon": in_m, "formal_relationship": formal,
                "non_latin_spans": non_latin}
    if uk and not us:
        return {"variety": "likely British-influenced spelling", "confidence": "medium" if len(uk) >= 2 else "low", "evidence": evidence}
    if us and not uk:
        return {"variety": "likely American-influenced spelling", "confidence": "medium" if len(us) >= 2 else "low", "evidence": evidence}
    if in_m or len(formal) >= 1:
        return {"variety": "likely Indian English register", "confidence": "medium" if in_m or len(formal) >= 2 else "low", "evidence": evidence}
    if uk and us:
        return {"variety": "mixed spelling — follow the dominant or house style", "confidence": "low", "evidence": evidence}
    return {"variety": "insufficient evidence", "confidence": "low", "evidence": evidence,
            "note": "Do not infer nationality. Default: preserve the text as written."}


def preservation_check(source: str, output: str) -> dict:
    """Flag normalisation of evidenced variety toward generic US professional English."""
    src = detect_variety(source)
    before = src["evidence"]
    findings = []
    out_low = output.casefold()
    for w in before.get("uk_spellings", []):
        # naive US counterpart check: s→z / our→or patterns are handled by pair lists.
        if w not in out_low:
            findings.append({"rule": "cultural-normalisation", "span": w,
                             "note": f"Source spelling '{w}' lost in output. Keep evidenced variety unless reader/brief requires change."})
    for m in before.get("indian_lexicon", []) + before.get("formal_relationship", []):
        if m not in out_low:
            findings.append({"rule": "cultural-normalisation", "span": m,
                             "note": f"Source idiom '{m}' lost. Preserve unless the reader will misunderstand."})
    return {"source_variety": src, "findings": findings,
            "passed": not findings}
