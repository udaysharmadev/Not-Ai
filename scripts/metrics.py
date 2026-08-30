#!/usr/bin/env python3
"""
not-ai: metrics.py
Readability, information density, and writing quality metrics.

Usage:
    python scripts/metrics.py [input_file]
    python scripts/metrics.py --stdin
"""

import sys
import re
import json
import argparse
import math
from pathlib import Path


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
    """Count polysyllabic words (3+ syllables) — used for Gunning Fog."""
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
    Proxy for information density based on:
    - Noun-to-verb ratio (high ratio = denser, more AI-like)
    - Modifier density (adjectives and adverbs)
    - Prepositional phrase proxy (preposition frequency)
    
    High information density = AI-like academic prose.
    Low = more conversational.
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
    
    # Nominalization density (from analyze_structure.py, duplicated here for standalone use)
    nom_pattern = re.compile(r'\b\w+(tion|tions|ment|ments|ness|ity|ance|ence)\b', re.IGNORECASE)
    nom_count = len(nom_pattern.findall(text))
    nom_rate = nom_count / len(words) * 1000 if words else 0
    
    # Overall density score (higher = more AI-like dense)
    density_score = (prep_rate * 200) + (nom_rate / 2)
    
    return {
        "preposition_rate": round(prep_rate, 3),
        "weak_verb_rate": round(weak_verb_rate, 3),
        "nominalization_rate_per_1000": round(nom_rate, 1),
        "estimated_density_score": round(density_score, 1),
        "assessment": (
            "high density (AI-like academic style)" if density_score > 50 else
            "moderate density" if density_score > 30 else
            "low density (conversational)"
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
        "stance_balance": (
            "over-hedged" if hedge_count > booster_count * 3 else
            "over-assertive" if booster_count > hedge_count * 2 else
            "calibrated"
        )
    }


# ─── Overall Quality Score ───────────────────────────────────────────────────

def compute_quality_score(struct_result: dict, rep_result: dict, readability: dict, 
                           density: dict, tone: dict) -> dict:
    """
    Compute a rough 0-100 quality / naturalness score.
    This is a heuristic, not a scientifically validated measure.
    """
    score = 70  # Start at 70 (assume reasonable writing)
    
    penalties = []
    strengths = []
    
    # Burstiness check (if we have it)
    burstiness = struct_result.get('sentence_lengths', {}).get('burstiness', 0.4)
    if burstiness < 0.25:
        score -= 10
        penalties.append("Very uniform sentence length")
    elif burstiness > 0.45:
        score += 5
        strengths.append("Good sentence length variation")
    
    # Participial clause rate
    pc_rate = struct_result.get('participial_clauses', {}).get('participial_opener_rate', 0)
    if pc_rate > 0.20:
        score -= 10
        penalties.append("High participial clause rate")
    elif pc_rate < 0.08:
        score += 3
    
    # Transition word density
    tw_rate = struct_result.get('transition_words', {}).get('rate_per_sentence', 0)
    if tw_rate > 0.25:
        score -= 8
        penalties.append("Excessive mechanical transitions")
    
    # Repeated openings
    rep_openings = rep_result.get('repeated_sentence_openings', {})
    if rep_openings.get('repeated_2word_openings'):
        score -= 5
        penalties.append("Repeated sentence openings")
    
    # AI vocabulary
    ai_vocab_count = struct_result.get('generic_vocabulary', {}).get('unique_ai_terms', 0)
    if ai_vocab_count > 5:
        score -= 8
        penalties.append(f"Multiple AI-associated vocabulary terms ({ai_vocab_count})")
    elif ai_vocab_count == 0:
        score += 3
        strengths.append("No high-frequency AI vocabulary")
    
    # Readability
    fog = readability.get('gunning_fog', 12)
    if fog > 18:
        score -= 5
        penalties.append("Very high reading complexity")
    elif 8 <= fog <= 14:
        score += 3
        strengths.append("Appropriate readability level")
    
    # Tone
    if tone.get('stance_balance') == 'calibrated':
        score += 3
        strengths.append("Calibrated epistemic stance")
    
    score = max(0, min(100, score))
    
    return {
        "overall_score": score,
        "strengths": strengths,
        "penalties": penalties,
        "disclaimer": "Heuristic score. Requires human judgment to interpret."
    }


# ─── Main ─────────────────────────────────────────────────────────────────────

def get_sentences(text: str) -> list[str]:
    text = re.sub(r'\s+', ' ', text.strip())
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z"\'])', text)
    return [s.strip() for s in sentences if s.strip() and len(s.split()) >= 2]


def analyze(text: str) -> dict:
    sentences = get_sentences(text)
    words = re.findall(r'\b[a-zA-Z]+\b', text)
    
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
    lines.append("NOT AI — METRICS")
    lines.append("─" * 40)
    
    r = result['readability']
    lines.append(f"\nREADABILITY")
    lines.append(f"  Flesch-Kincaid Grade:  {r['flesch_kincaid_grade']} (US grade level equivalent)")
    lines.append(f"  Gunning Fog Index:     {r['gunning_fog_index']} ({r['readability_assessment']})")
    lines.append(f"  Flesch Reading Ease:   {r['flesch_reading_ease']} / 100")
    
    d = result['information_density']
    lines.append(f"\nINFORMATION DENSITY")
    lines.append(f"  Density score: {d['estimated_density_score']} — {d['assessment']}")
    lines.append(f"  Preposition rate:  {d['preposition_rate']:.1%}")
    lines.append(f"  Nominalizations:   {d['nominalization_rate_per_1000']} per 1,000 words")
    
    t = result['tone_markers']
    lines.append(f"\nEPISTEMIC STANCE")
    lines.append(f"  Hedges:     {t['hedge_count']} ({t['hedge_rate_per_1000']} per 1,000 words)")
    lines.append(f"  Boosters:   {t['booster_count']} ({t['booster_rate_per_1000']} per 1,000 words)")
    lines.append(f"  Balance:    {t['stance_balance']}")
    lines.append(f"\nENGAGEMENT MARKERS")
    lines.append(f"  Questions:      {t['question_count']}")
    lines.append(f"  Reader address: {t['reader_address_count']}")
    lines.append(f"  First-person:   {t['first_person_count']} ({t['first_person_rate_per_1000']} per 1,000 words)")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Not Ai — writing metrics')
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
    
    result = analyze(text)
    
    if args.json:
        print(json.dumps(result, indent=2, ensure_ascii=False))
    else:
        print(human_readable_summary(result))


if __name__ == '__main__':
    main()
