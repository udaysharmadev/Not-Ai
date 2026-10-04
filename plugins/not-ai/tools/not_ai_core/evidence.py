"""Evidence registry loader for Not-AI 3.0.

Rule explanations are generated from shared rule/evidence metadata instead of
being hand-duplicated. The JSON registry at docs/research/evidence-registry.json
is the machine-readable source; this module provides a stdlib-only fallback so
the plugin works without the docs tree (e.g. inside the .skill bundle).
"""

from __future__ import annotations

import json
from pathlib import Path

_FALLBACK = {
    "E01": {"cite": "Reinhart et al. 2025, PNAS, DOI 10.1073/pnas.2422455122",
            "finding": "Instruction-tuned LLMs showed elevated nominalization, participial clauses, phrasal coordination and distinctive vocabulary at population level across studied corpora.",
            "limit": "Population-level difference; tagged per-1k-token rates are not comparable to regex proxies; English, 2024-era models."},
    "E02": {"cite": "Biber 1988; Conrad & Biber — multidimensional register variation",
            "finding": "Features work in clusters along dimensions (involved/informational, narrative, explicit/situated, persuasion, abstract, online elaboration).",
            "limit": "No single formal/informal axis; interpret dimensions, do not score them."},
    "E03": {"cite": "Jiang & Hyland 2025, DOI 10.1177/07410883251328311",
            "finding": "In 145+145 argumentative essays, students used richer engagement (questions, asides); ChatGPT fewer interactional markers.",
            "limit": "Argumentative-essay genre only; never insert engagement to hit targets."},
    "E05": {"cite": "Kobak et al. 2025, Sci. Adv., DOI 10.1126/sciadv.adt3813",
            "finding": "Corpus-level excess vocabulary in 15M+ biomedical abstracts; >=13.5% of 2024 abstracts LLM-processed (lower bound).",
            "limit": "Corpus-level inference; cannot classify individual documents; no word blacklist."},
    "E06": {"cite": "McCarthy & Jarvis 2010, DOI 10.3758/BRM.42.2.381",
            "finding": "MTLD is length-robust; HD-D viable vocd-D alternative; use more than one index.",
            "limit": "Short texts still unstable; report threshold (0.72) and draws (42)."},
    "E07": {"cite": "Agarwal, Naaman & Vashistha, CHI 2025, DOI 10.1145/3706598.3713564",
            "finding": "Western-centric suggestions homogenised Indian writing toward US norms (118 participants).",
            "limit": "India/US tasks; never stereotype; preserve evidenced variety."},
    "E08": {"cite": "Moon, Green & Kushlev 2025, DOI 10.1016/j.chbah.2025.100207",
            "finding": "LLMs homogenise collective creative diversity even when individual outputs look diverse.",
            "limit": "Task/model-specific; design against one 'good writer' personality."},
    "E09": {"cite": "ISO 24495-1:2023 Plain language (Relevant/Findable/Understandable/Usable)",
            "finding": "Document-level reader-task success, not mechanical scores.",
            "limit": "No universal plain-language score."},
    "E10": {"cite": "ASD-STE100 Issue 9 (2025-01-15), STEMG",
            "finding": "Controlled technical language; AI can look STE-like without complying.",
            "limit": "Proprietary dictionary; technical scope only; never claim compliance without user resources."},
    "E11": {"cite": "Liang et al. 2023, Patterns, DOI 10.1016/j.patter.2023.100779",
            "finding": "Detectors severely misflagged evaluated non-native English samples.",
            "limit": "Era-bound; constrained style is never a defect."},
    "E12": {"cite": "Sadasivan et al. 2023, arXiv:2303.11156",
            "finding": "Text-only detection is fragile under overlap and paraphrase.",
            "limit": "Never promise authorship/detector outcomes."},
    "E13": {"cite": "Dugan et al. 2024, ACL, DOI 10.18653/v1/2024.acl-long.674 (RAID)",
            "finding": "6M+ generations; 11 adversarial attacks incl. U+200B zero-width-space; current detectors easily fooled by adversarial/sampling shifts.",
            "limit": "Detector-era bound; do not transfer fool rates; defense only, never evasion."},
    "E14": {"cite": "Mady et al. 2026, arXiv:2610.00883 (DeBERTa-ConPara, verified-abstract)",
            "finding": "Inference-time Unicode normalization defends against zero-width/homoglyph classes; training-time normalization deduplicates supervision.",
            "limit": "Very recent preprint; full effect tables not re-verified; no precise numbers quoted."},
    "E15": {"cite": "The Unicode Standard (Ch. 16, 23); UTS #39 / #55",
            "finding": "U+200B is a legitimate break opportunity (Thai, Myanmar, Khmer, Lao, Japanese); ZWJ/ZWNJ have orthographic/emoji roles; invisible controls need contextual handling.",
            "limit": "Standard describes correct use, not detector outcomes; preserve legitimate uses."},
}


def load_registry() -> dict:
    """Return {evidence_id: entry}. Prefers docs JSON, falls back to builtin."""
    candidates = [
        Path(__file__).resolve().parents[4] / "docs" / "research" / "evidence-registry.json",
        Path(__file__).resolve().parents[3] / "docs" / "research" / "evidence-registry.json",
    ]
    for path in candidates:
        try:
            if path.is_file():
                data = json.loads(path.read_text(encoding="utf-8"))
                entries = data.get("entries", []) if isinstance(data, dict) else []
                out = {}
                for entry in entries:
                    eid = entry.get("id")
                    if eid:
                        out[eid] = entry
                if out:
                    return out
        except (OSError, ValueError):
            continue
    return dict(_FALLBACK)


def cite(evidence_id: str) -> str:
    reg = load_registry()
    entry = reg.get(evidence_id, {})
    if not entry:
        return evidence_id
    if "cite" in entry:
        return str(entry["cite"])
    authors = ", ".join(entry.get("authors", []))
    year = entry.get("year") or ""
    venue = entry.get("venue", "")
    doi = entry.get("doi") or ""
    base = f"{authors} ({year}). {venue}".strip() if year else f"{authors}. {venue}".strip()
    return f"{base}. DOI {doi}" if doi else base
