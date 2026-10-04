"""Composable genre policies (Not-AI 3.0).

Keeps the 9 v2 profiles byte-compatible (same names, same gate behaviour) and
adds composable dimensions so new genres compose instead of duplicating rule sets.
`get_policy()` API is unchanged; unknown genres still raise.
"""

from __future__ import annotations

from dataclasses import dataclass


@dataclass(frozen=True)
class GenrePolicy:
    name: str
    conversational: bool
    require_contractions: bool
    allow_fragments: bool
    check_nominalizations: bool
    contraction_floor: int = 80
    grade_low: float = 0.0
    grade_high: float = 99.0
    # Composable dimensions (v3): purpose/reader/density/evidence/stance/scanability.
    purpose: str = ""
    reader_relationship: str = ""
    formality: str = ""
    interactivity: str = ""
    information_density: str = ""
    expected_evidence: str = ""
    acceptable_passive: str = ""
    acceptable_nominalization: str = ""
    personal_stance: str = ""
    paragraph_size: str = ""
    scanability: str = ""
    terminology_control: str = ""
    required_actionability: str = ""


def _p(name, conv, req_c, frag, chk_nom, floor=80, glo=0.0, ghi=99.0, **dims):
    return GenrePolicy(name, conv, req_c, frag, chk_nom, floor, glo, ghi,
                       purpose=dims.get("purpose", ""),
                       reader_relationship=dims.get("reader_relationship", ""),
                       formality=dims.get("formality", ""),
                       interactivity=dims.get("interactivity", ""),
                       information_density=dims.get("information_density", ""),
                       expected_evidence=dims.get("expected_evidence", ""),
                       acceptable_passive=dims.get("acceptable_passive", ""),
                       acceptable_nominalization=dims.get("acceptable_nominalization", ""),
                       personal_stance=dims.get("personal_stance", ""),
                       paragraph_size=dims.get("paragraph_size", ""),
                       scanability=dims.get("scanability", ""),
                       terminology_control=dims.get("terminology_control", ""),
                       required_actionability=dims.get("required_actionability", ""))


POLICIES = {
    "linkedin": _p("linkedin", True, True, True, True, 30, 5.0, 12.0,
                   purpose="share a specific observation/outcome", reader_relationship="weak-tie professional",
                   formality="conversational-professional", interactivity="medium", information_density="low",
                   expected_evidence="event or result", acceptable_passive="rare", acceptable_nominalization="low",
                   personal_stance="first-person for own experience only", paragraph_size="1-2 sentences",
                   scanability="high", terminology_control="low", required_actionability="low"),
    "personal": _p("personal", True, True, True, True, 40, 5.0, 12.0,
                   purpose="narrate/reflection", reader_relationship="reader as witness",
                   formality="own voice", interactivity="low", information_density="low",
                   expected_evidence="lived detail", acceptable_passive="when actor unknown",
                   acceptable_nominalization="low", personal_stance="welcome", paragraph_size="uneven",
                   scanability="medium", terminology_control="low", required_actionability="low"),
    "email": _p("email", True, True, False, True, 40, 5.0, 12.0,
                 purpose="request/decide", reader_relationship="known counterpart",
                 formality="match relationship", interactivity="high", information_density="medium",
                 expected_evidence="owners/dates/next steps", acceptable_passive="rare",
                 acceptable_nominalization="low", personal_stance="direct", paragraph_size="short",
                 scanability="high", terminology_control="medium", required_actionability="high"),
    "social": _p("social", True, False, True, True, 30, 3.0, 10.0,
                 purpose="note/react", reader_relationship="followers", formality="casual",
                 interactivity="high", information_density="low", expected_evidence="none required",
                 acceptable_passive="rare", acceptable_nominalization="low", personal_stance="free",
                 paragraph_size="fragments normal", scanability="very high", terminology_control="low",
                 required_actionability="low"),
    "x": _p("x", True, False, True, True, 30, 3.0, 10.0,
            purpose="note/react in very short form", reader_relationship="followers",
            formality="casual", interactivity="high", information_density="low",
            expected_evidence="none required", acceptable_passive="rare", acceptable_nominalization="low",
            personal_stance="free", paragraph_size="1-3 lines", scanability="very high",
            terminology_control="low", required_actionability="low"),
    "fiction": _p("fiction", True, False, True, True, 60, 3.0, 10.0,
                  purpose="scene/character", reader_relationship="reader as experiencer",
                  formality="voice-led", interactivity="low", information_density="low",
                  expected_evidence="sensory detail from source only", acceptable_passive="stylistic",
                  acceptable_nominalization="low", personal_stance="POV-bound", paragraph_size="varied",
                  scanability="low", terminology_control="low", required_actionability="low"),
    "readme": _p("readme", False, False, False, True, 80, 6.0, 14.0,
                 purpose="enable action", reader_relationship="user/operator",
                 formality="direct", interactivity="low", information_density="medium",
                 expected_evidence="commands/behaviour", acceptable_passive="when actor irrelevant",
                 acceptable_nominalization="medium", personal_stance="minimal", paragraph_size="short+lists",
                 scanability="high", terminology_control="high", required_actionability="high"),
    "technical": _p("technical", False, False, False, False, 80, 8.0, 16.0,
                    purpose="explain precisely", reader_relationship="practitioner",
                    formality="precise", interactivity="low", information_density="high",
                    expected_evidence="behaviour/constraints", acceptable_passive="when actor unknown/irrelevant",
                    acceptable_nominalization="keep when precise", personal_stance="minimal",
                    paragraph_size="medium", scanability="medium", terminology_control="high",
                    required_actionability="medium"),
    "procedure": _p("procedure", False, False, False, False, 80, 8.0, 16.0,
                    purpose="sequence safe action", reader_relationship="operator",
                    formality="imperative", interactivity="low", information_density="medium",
                    expected_evidence="steps/prereqs/warnings", acceptable_passive="avoid in steps",
                    acceptable_nominalization="low", personal_stance="none", paragraph_size="one-step-per-block",
                    scanability="high", terminology_control="very high", required_actionability="very high"),
    "api": _p("api", False, False, False, False, 80, 8.0, 16.0,
              purpose="specify interface behaviour", reader_relationship="developer",
              formality="normative", interactivity="low", information_density="high",
              expected_evidence="signatures/errors/examples", acceptable_passive="allowed for behaviour",
              acceptable_nominalization="keep", personal_stance="none", paragraph_size="short+tables",
              scanability="high", terminology_control="very high", required_actionability="high"),
    "tutorial": _p("tutorial", True, False, False, True, 60, 6.0, 14.0,
                   purpose="teach by doing", reader_relationship="learner",
                   formality="guiding", interactivity="medium", information_density="medium",
                   expected_evidence="worked steps", acceptable_passive="rare", acceptable_nominalization="low",
                   personal_stance="second-person welcome", paragraph_size="short", scanability="high",
                   terminology_control="medium", required_actionability="high"),
    "student": _p("student", False, False, False, True, 80, 8.0, 16.0,
                  purpose="show method/evidence/limits", reader_relationship="assessor",
                  formality="natural formal", interactivity="low", information_density="medium",
                  expected_evidence="methods/datasets/results/citations", acceptable_passive="methods-OK",
                  acceptable_nominalization="medium", personal_stance="first-person for own work",
                  paragraph_size="medium", scanability="medium", terminology_control="high",
                  required_actionability="low"),
    "academic": _p("academic", False, False, False, False, 80, 12.0, 22.0,
                   purpose="argue cautiously from evidence", reader_relationship="peers",
                   formality="formal", interactivity="low", information_density="high",
                   expected_evidence="citations/hedged claims", acceptable_passive="keep when needed",
                   acceptable_nominalization="keep when precise", personal_stance="venue-dependent",
                   paragraph_size="medium-long", scanability="low", terminology_control="very high",
                   required_actionability="low"),
    "abstract": _p("abstract", False, False, False, False, 80, 12.0, 22.0,
                   purpose="summarise hypothesis/method/finding", reader_relationship="peers/skimmers",
                   formality="formal dense", interactivity="low", information_density="very high",
                   expected_evidence="claims + scope", acceptable_passive="keep", acceptable_nominalization="keep",
                   personal_stance="third-person default", paragraph_size="single block",
                   scanability="low", terminology_control="very high", required_actionability="low"),
    "proposal": _p("proposal", False, False, False, True, 80, 8.0, 16.0,
                   purpose="request resources/approval", reader_relationship="decision-maker",
                   formality="professional", interactivity="medium", information_density="medium",
                   expected_evidence="scope/cost/risks", acceptable_passive="rare", acceptable_nominalization="medium",
                   personal_stance="accountable", paragraph_size="short", scanability="high",
                   terminology_control="medium", required_actionability="high"),
    "executive": _p("executive", False, False, False, True, 80, 8.0, 14.0,
                    purpose="enable a decision fast", reader_relationship="executive",
                    formality="concise professional", interactivity="low", information_density="medium",
                    expected_evidence="options/recommendation", acceptable_passive="rare",
                    acceptable_nominalization="medium", personal_stance="accountable", paragraph_size="very short",
                    scanability="very high", terminology_control="medium", required_actionability="high"),
    "marketing": _p("marketing", True, False, True, True, 60, 5.0, 12.0,
                    purpose="persuade", reader_relationship="prospect",
                    formality="brand voice", interactivity="medium", information_density="low",
                    expected_evidence="claims need support — cut unsupported praise", acceptable_passive="rare",
                    acceptable_nominalization="low", personal_stance="brand-constrained", paragraph_size="short",
                    scanability="high", terminology_control="medium", required_actionability="medium"),
    "essay": _p("essay", True, False, False, True, 60, 6.0, 14.0,
                purpose="argue for a reader", reader_relationship="general reader",
                formality="clear formal", interactivity="medium", information_density="medium",
                expected_evidence="reasons + engagement", acceptable_passive="as needed",
                acceptable_nominalization="medium", personal_stance="presence welcome", paragraph_size="medium",
                scanability="medium", terminology_control="medium", required_actionability="low"),
}


def get_policy(genre: str) -> GenrePolicy:
    try:
        return POLICIES[genre.lower()]
    except KeyError as error:
        options = ", ".join(sorted(POLICIES))
        raise ValueError(f"Unknown genre '{genre}'. Choose one of: {options}") from error


# Contextual baseline hierarchy: writer > publication > genre corpus > literature > heuristic.
BASELINE_PRIORITY = ("writer_sample", "publication_style", "genre_corpus", "literature", "heuristic")


def baseline_confidence(source: str) -> tuple[str, str]:
    """Map evidence source to (level, strength). Farther down = weaker recommendation."""
    mapping = {"writer_sample": ("writer", "high"),
               "publication_style": ("publication", "medium-high"),
               "genre_corpus": ("genre", "medium"),
               "literature": ("literature", "low-medium"),
               "heuristic": ("heuristic", "low")}
    return mapping.get(source, ("heuristic", "low"))
