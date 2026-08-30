#!/usr/bin/env python3
"""
not-ai: metrics.py
Readability, information density, and writing quality metrics.

Usage:
    python scripts/metrics.py [input_file]
    python scripts/metrics.py [input_file] --json
    python scripts/metrics.py --stdin

Output: a human-readable report to stdout. Pass --json for the raw figures.
"""

import sys
import re
import json
import argparse
import math
from pathlib import Path

# Import the shared measurement primitives. Inserting this script's own
# directory first keeps the import working from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _shared import (  # noqa: E402
    get_sentences,
    tokenize_words,
    nominalization_stats,
    stance_balance,
)


# ─── Readability Metrics ─────────────────────────────────────────────────────

def count_syllables(word: str) -> int:
    """Rough syllable counter for English words."""
    word = word.lower().strip(".,!?;:'\"()")
    if not word:
        return 0
    
    # Remove trailing 'e' (usually silent)
    if word.endswith('e') and len(word) > 2:
        word = word[:-1]
    
    vowels = re.findall(r'[aeiou]+', word)
    count = len(vowels)
    
    # Minimum 1 syllable per word
    return max(1, count)


def count_complex_words(words: list[str]) -> int:
    """Count polysyllabic words (3 or more syllables), used for Gunning Fog."""
    return sum(1 for w in words if count_syllables(w) >= 3)


def flesch_kincaid_grade(text: str, sentences: list[str], words: list[str]) -> float:
    """
    Flesch-Kincaid Grade Level.
    Grade = 0.39 * (words/sentences) + 11.8 * (syllables/words) - 15.59
    
    Grade interpretation: roughly matches US school grade level.
    ~8-10: accessible general prose
    ~12-14: academic/technical prose
    ~16+: very dense academic
    """
    if not sentences or not words:
        return 0.0
    
    total_syllables = sum(count_syllables(w) for w in words)
    avg_sentence_length = len(words) / len(sentences)
    avg_syllables_per_word = total_syllables / len(words) if words else 0
    
    grade = 0.39 * avg_sentence_length + 11.8 * avg_syllables_per_word - 15.59
    return round(grade, 1)


def gunning_fog(text: str, sentences: list[str], words: list[str]) -> float:
    """
    Gunning Fog Index.
    FOG = 0.4 * ((words/sentences) + 100 * (complex_words/words))
    
    Interpretation:
    <8: easy
    8-12: ideal for general readability
    12-16: difficult (academic)
    >16: very difficult
    """
    if not sentences or not words:
        return 0.0
    
    avg_sentence_length = len(words) / len(sentences)
    complex_count = count_complex_words(words)
    pct_complex = complex_count / len(words) * 100 if words else 0
    
    fog = 0.4 * (avg_sentence_length + pct_complex)
    return round(fog, 1)


def flesch_reading_ease(text: str, sentences: list[str], words: list[str]) -> float:
    """
    Flesch Reading Ease score.
    206.835 - 1.015 * (words/sentences) - 84.6 * (syllables/words)
    
    100-90: very easy (5th grade)
    70-60: standard (8th-9th grade)
    50-30: difficult (college)
    <30: very confusing
    """
    if not sentences or not words:
        return 0.0
    
    total_syllables = sum(count_syllables(w) for w in words)
    avg_sentence_length = len(words) / len(sentences)
    avg_syllables = total_syllables / len(words) if words else 0
    
    ease = 206.835 - 1.015 * avg_sentence_length - 84.6 * avg_syllables
    return round(ease, 1)


# ─── Information Density ─────────────────────────────────────────────────────

def information_density_proxy(text: str, words: list[str]) -> dict:
    """
    Proxy for information density, combining:
    - preposition frequency, standing in for prepositional phrase density
    - copula and auxiliary frequency, which falls as density rises
    - nominalization rate from the shared heuristic proxy

    Dense informational prose scores high here and conversational prose scores
    low. Instruction-tuned models tend to write densely across every genre,
    including fiction, where a human writer would loosen up. A high score is
    therefore worth investigating, and it is not evidence of authorship.

    The bands are heuristic and calibrated for these proxies. See _shared.py.
    """

    # Common prepositions (marker of prepositional phrase density)
    prepositions = {'of', 'in', 'to', 'for', 'on', 'with', 'at', 'by', 'from',
                    'into', 'through', 'during', 'before', 'after', 'above', 'below',
                    'between', 'among', 'under', 'about', 'against', 'without', 'within',
                    'around', 'along', 'following', 'across', 'behind', 'beyond',
                    'including', 'throughout', 'regarding', 'concerning'}

    # Common copula and auxiliary verbs (low density markers)
    weak_verbs = {'is', 'are', 'was', 'were', 'be', 'been', 'being',
                  'have', 'has', 'had', 'do', 'does', 'did',
                  'will', 'would', 'could', 'should', 'may', 'might', 'can', 'shall'}

    words_lower = [w.lower() for w in words]

    prep_count = sum(1 for w in words_lower if w in prepositions)
    weak_verb_count = sum(1 for w in words_lower if w in weak_verbs)

    prep_rate = prep_count / len(words) if words else 0
    weak_verb_rate = weak_verb_count / len(words) if words else 0

    # Nominalization density comes from _shared.py so that this figure and the
    # one reported by analyze_structure.py are always the same number. They
    # used to be computed separately and disagreed.
    nom = nominalization_stats(text, words)
    nom_rate = nom["rate_per_1000_words"]

    # Composite density score. Higher means denser informational prose.
    density_score = (prep_rate * 200) + (nom_rate / 2)

    return {
        "preposition_rate": round(prep_rate, 3),
        "weak_verb_rate": round(weak_verb_rate, 3),
        "nominalization_rate_per_1000": nom_rate,
        "nominalization_assessment": nom["assessment"],
        "estimated_density_score": round(density_score, 1),
        "assessment": (
            "high density, characteristic of formal academic prose" if density_score > 50 else
            "moderate density" if density_score > 30 else
            "low density, conversational"
        )
    }


# ─── Sentiment & Tone Markers ─────────────────────────────────────────────────

def tone_markers(text: str) -> dict:
    """
    Detect stance and tone markers that research links to human vs AI writing.
    Based on Jiang & Hyland (2025) and Biber feature categories.
    """
    text_lower = text.lower()
    word_count = len(text.split())
    
    # Hedges
    hedge_patterns = [
        r'\bmight\b', r'\bcould\b', r'\bmay\b', r'\bperhaps\b', r'\bpossibly\b',
        r'\bappears? to\b', r'\bseems? to\b', r'\btends? to\b',
        r'\bi think\b', r'\bi believe\b', r'\bone might\b', r'\bargua\w+\b',
        r'\bsuggests?\b', r'\bindicates?\b', r'\bseems?\b',
    ]
    hedge_count = sum(len(re.findall(p, text_lower)) for p in hedge_patterns)
    
    # Boosters (certainty markers)
    booster_patterns = [
        r'\bclearly\b', r'\bobviously\b', r'\bcertainly\b', r'\bdefinitely\b',
        r'\bundoubtedly\b', r'\bwithout question\b', r'\bit is clear\b',
        r'\bof course\b', r'\bevident\w*\b',
    ]
    booster_count = sum(len(re.findall(p, text_lower)) for p in booster_patterns)
    
    # Engagement markers (questions, direct address)
    question_count = text.count('?')
    reader_address = len(re.findall(r'\byou\b|\byour\b', text_lower))
    
    # Personal stance
    first_person = len(re.findall(r'\bi\b|\bme\b|\bmy\b|\bwe\b|\bour\b', text_lower))
    
    return {
        "hedge_count": hedge_count,
        "hedge_rate_per_1000": round(hedge_count / word_count * 1000, 1) if word_count else 0,
        "booster_count": booster_count,
        "booster_rate_per_1000": round(booster_count / word_count * 1000, 1) if word_count else 0,
        "question_count": question_count,
        "reader_address_count": reader_address,
        "first_person_count": first_person,
        "first_person_rate_per_1000": round(first_person / word_count * 1000, 1) if word_count else 0,
        "stance_balance": stance_balance(hedge_count, booster_count, word_count),
    }


# ─── Main ─────────────────────────────────────────────────────────────────────

# Note on what is deliberately absent here.
#
# An earlier version of this file exposed compute_quality_score(), which
# returned a 0 to 100 "naturalness" number. It has been removed. A single score
# invites exactly the reading the skill is built to avoid: that a threshold
# separates machine text from human text, and that a rewrite is finished when
# the number moves. None of these measures supports that reading. Report the
# individual signals and let a reader weigh them.


def analyze(text: str) -> dict:
    sentences = get_sentences(text)
    words = tokenize_words(text)
    
    fk = flesch_kincaid_grade(text, sentences, words)
    fog = gunning_fog(text, sentences, words)
    ease = flesch_reading_ease(text, sentences, words)
    density = information_density_proxy(text, words)
    tone = tone_markers(text)
    
    readability = {
        "flesch_kincaid_grade": fk,
        "gunning_fog_index": fog,
        "flesch_reading_ease": ease,
        "readability_assessment": (
            "very easy" if ease > 80 else
            "easy" if ease > 70 else
            "standard" if ease > 60 else
            "difficult" if ease > 40 else
            "very difficult"
        )
    }
    
    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "readability": readability,
        "information_density": density,
        "tone_markers": tone,
    }


def human_readable_summary(result: dict) -> str:
    lines = []
    lines.append("NOT AI : METRICS")
    lines.append("─" * 40)
    
    r = result['readability']
    lines.append(f"\nREADABILITY")
    lines.append(f"  Flesch-Kincaid Grade:  {r['flesch_kincaid_grade']} (US grade level equivalent)")
    lines.append(f"  Gunning Fog Index:     {r['gunning_fog_index']} ({r['readability_assessment']})")
    lines.append(f"  Flesch Reading Ease:   {r['flesch_reading_ease']} / 100")
    
    d = result['information_density']
    lines.append(f"\nINFORMATION DENSITY")
    lines.append(f"  Density score: {d['estimated_density_score']}  |  {d['assessment']}")
    lines.append(f"  Preposition rate:  {d['preposition_rate']:.1%}")
    lines.append(f"  Nominalizations:   {d['nominalization_rate_per_1000']} per 1,000 words  |  {d['nominalization_assessment']}")
    lines.append(f"  (Proxy measure. Compare only against another run of this script.)")
    
    t = result['tone_markers']
    lines.append(f"\nEPISTEMIC STANCE")
    lines.append(f"  Hedges:     {t['hedge_count']} ({t['hedge_rate_per_1000']} per 1,000 words)")
    lines.append(f"  Boosters:   {t['booster_count']} ({t['booster_rate_per_1000']} per 1,000 words)")
    lines.append(f"  Balance:    {t['stance_balance']}")
    lines.append("  Models underuse hedges at 50% to 63% of the human rate, so"
                 " 'over-hedged' on a draft is worth checking before acting on.")
    lines.append("  'absent' means no stance marker was found at all, which some"
                 " genres do not need; it is a reading, not a fault.")
    lines.append(f"\nENGAGEMENT MARKERS")
    lines.append(f"  Questions:      {t['question_count']}")
    lines.append(f"  Reader address: {t['reader_address_count']}")
    lines.append(f"  First-person:   {t['first_person_count']} ({t['first_person_rate_per_1000']} per 1,000 words)")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Not Ai: writing metrics')
    parser.add_argument('input_file', nargs='?', help='Input text file')
    parser.add_argument('--stdin', action='store_true', help='Read from stdin')
    parser.add_argument('--json', action='store_true', help='Output raw JSON')
    args = parser.parse_args()
    
    if args.stdin or not args.input_file:
        text = sys.stdin.read()
    else:
        path = Path(args.input_file)
        if not path.exists():
            print(f"Error: file not found: {args.input_file}", file=sys.stderr)
            sys.exit(1)
        text = path.read_text(encoding='utf-8')

    if not text.strip():
        print("Error: no text provided", file=sys.stderr)
        sys.exit(1)

    result = analyze(text)
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(human_readable_summary(result))


if __name__ == '__main__':
    main()
