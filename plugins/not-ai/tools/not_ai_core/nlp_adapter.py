"""Optional enriched NLP adapter (Not-AI 3.0).

Base installation stays stdlib-only and offline. If spaCy (or another parser)
is installed, `try_enhance()` returns deeper measurements; otherwise it reports
unavailability and callers degrade cleanly. Never pretend a regex approximation
is equivalent — parsed metrics have distinct names.
"""

from __future__ import annotations


def available() -> dict:
    try:
        import spacy  # noqa: F401
        return {"spacy": True}
    except ImportError:
        return {"spacy": False}


def try_enhance(text: str) -> dict:
    """Return {'available': bool, 'measurements': {...} | 'reason': str}."""
    try:
        import spacy
    except ImportError:
        return {"available": False,
                "reason": "spaCy not installed. Install optional not-ai[nlp] for parsed metrics. Regex proxies remain available and are NOT equivalent."}
    try:
        nlp = spacy.load("en_core_web_sm")
    except OSError:
        return {"available": False,
                "reason": "spaCy installed but model en_core_web_sm not downloaded. Run: python -m spacy download en_core_web_sm. No network use otherwise."}
    doc = nlp(text[:50000])
    depths = []
    for sent in doc.sents:
        depths.append(max((len(list(tok.ancestors)) for tok in sent), default=0))
    pos = {}
    for tok in doc:
        pos[tok.pos_] = pos.get(tok.pos_, 0) + 1
    passives = sum(1 for tok in doc if tok.dep_ in ("nsubjpass", "auxpass"))
    nominal = sum(1 for tok in doc if tok.text.lower().endswith(
        ("tion", "sion", "ment", "ness", "ance", "ence", "ity", "ization")) and tok.pos_ == "NOUN")
    return {"available": True, "measurements": {
        "parsed_dependency_max_depth_mean": round(sum(depths) / len(depths), 2) if depths else 0.0,
        "parsed_pos_distribution": pos,
        "parsed_passive_count": passives,
        "parsed_nominalization_count": nominal,
        "parsed_entities": [(e.text[:60], e.label_) for e in doc.ents][:20],
    }}
