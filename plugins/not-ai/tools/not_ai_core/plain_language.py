"""Document-level plain-language review (ISO 24495-1:2023, E09).

Four dimensions, reported separately. Never a single plain-language score.
"""

from __future__ import annotations

import re

from .text import paragraphs, sentences, words


def review(text: str, genre: str = "technical") -> dict:
    paras = paragraphs(text)
    items = sentences(text)
    # RELEVANT: does it answer the likely question? Proxy: generic scene-setting
    # vs checkable specifics (numbers, named entities, code).
    nums = len(re.findall(r"\b\d+(?:\.\d+)?%?", text))
    properish = len(re.findall(r"\b[A-Z][a-z]+(?:\s+[A-Z][a-z]+){0,2}\b", text))
    generic_open = sum(1 for s in items if re.match(
        r"^(in today|it is important|it is worth|plays a crucial|in the modern)", s, re.IGNORECASE))
    relevant = {"checkable_numbers": nums, "named_entities_proxy": properish,
                "generic_scene_setters": generic_open,
                "finding": ("background without specifics — answer the likely reader question first"
                             if nums == 0 and properish < 3 and len(items) >= 4 else "has checkable specifics")}
    # FINDABLE: headings, lists, buried key info.
    headings = sum(1 for line in text.splitlines() if re.match(r"^#{1,6}\s", line.strip()))
    lists = len(re.findall(r"(?m)^\s*(?:[-*\u2022]|\d+[.)])\s+\S", text))
    findable = {"headings": headings, "list_items": lists,
                "finding": ("no headings/lists in a long document — can the reader locate the answer?"
                             if len(items) >= 8 and headings == 0 and lists == 0 else "structure present or text short enough")}
    # UNDERSTANDABLE: actors, references, term definitions, order.
    passiveish = sum(1 for s in items if re.search(r"\b(am|is|are|was|were|be|been|being)\s+\w+(?:ed|en)\b", s, re.IGNORECASE))
    undefined_abbr = sorted(set(re.findall(r"\b[A-Z]{2,6}\b", text)))[:8]
    understandable = {"passive_estimate": passiveish,
                      "uppercase_terms": undefined_abbr,
                      "finding": ("define terms where needed; keep actors clear"
                                   if passiveish >= max(2, len(items) // 2) else "actors/terms look manageable")}
    # USABLE: next steps, prerequisites, warnings-before-actions.
    has_steps = bool(re.search(r"\b(step\s*\d|first,|next,|then,|1\.)", text, re.IGNORECASE))
    has_warning = bool(re.search(r"\b(warning|caution|danger|before you|prerequisite)\b", text, re.IGNORECASE))
    imperative = sum(1 for s in items if re.match(r"^(install|run|click|type|open|close|do|ensure|verify|check)\b", s.strip(), re.IGNORECASE))
    usable = {"has_steps": has_steps, "has_warnings": has_warning,
              "imperative_steps": imperative,
              "finding": ("procedural text without visible prerequisites/steps — add them" if genre in ("technical", "readme", "procedure") and not has_steps and len(items) >= 4
                          else "actionability looks adequate for genre")}
    return {"genre": genre, "relevant": relevant, "findable": findable,
            "understandable": understandable, "usable": usable,
            "note": "Dimensions reported separately per ISO 24495-1. No universal score."}
