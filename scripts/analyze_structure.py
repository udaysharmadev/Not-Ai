#!/usr/bin/env python3
"""
not-ai: analyze_structure.py
Deterministic structural analyzer for writing diagnostics.

Measures morphosyntactic and structural features that research identifies
as the primary fingerprints distinguishing LLM-generated text from human writing.
Based on Biber (1988) feature categories and Reinhart et al. (PNAS 2025).

Usage:
    python scripts/analyze_structure.py [input_file]
    python scripts/analyze_structure.py [input_file] --json
    python scripts/analyze_structure.py --stdin
    cat myfile.txt | python scripts/analyze_structure.py --stdin

Output: a human-readable report to stdout. Pass --json for the raw figures.
"""

import sys
import re
import json
import argparse
from pathlib import Path

# Import the shared measurement primitives. Inserting this script's own
# directory first keeps the import working from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _shared import (  # noqa: E402
    get_sentences,
    get_paragraphs,
    tokenize_words,
    nominalization_stats,
)


# ─── Feature Extraction ──────────────────────────────────────────────────────


def sentence_lengths(sentences: list[str]) -> dict:
    """Compute sentence length statistics."""
    if not sentences:
        return {"mean": 0, "median": 0, "std": 0, "min": 0, "max": 0, "burstiness": 0}

    lengths = [len(s.split()) for s in sentences]
    n = len(lengths)
    mean = sum(lengths) / n
    sorted_l = sorted(lengths)
    median = sorted_l[n // 2] if n % 2 else (sorted_l[n//2 - 1] + sorted_l[n//2]) / 2
    variance = sum((x - mean) ** 2 for x in lengths) / n
    std = variance ** 0.5

    # Burstiness: coefficient of variation. A high value means length varies,
    # a low value means the text is metrically uniform. Uniformity is worth
    # investigating; on its own it establishes nothing about authorship, and
    # some human genres (reference documentation, legal boilerplate) are
    # legitimately uniform.
    burstiness = std / mean if mean > 0 else 0
    
    return {
        "count": n,
        "mean": round(mean, 1),
        "median": round(median, 1),
        "std": round(std, 1),
        "min": min(lengths),
        "max": max(lengths),
        "burstiness": round(burstiness, 3),
        "distribution": {
            "very_short_under_8": sum(1 for l in lengths if l < 8),
            "short_8_to_15": sum(1 for l in lengths if 8 <= l < 16),
            "medium_16_to_25": sum(1 for l in lengths if 16 <= l < 26),
            "long_26_to_35": sum(1 for l in lengths if 26 <= l < 36),
            "very_long_over_35": sum(1 for l in lengths if l >= 36),
        }
    }


def paragraph_lengths(paragraphs: list[str]) -> dict:
    """Compute paragraph length statistics (in sentences)."""
    if not paragraphs:
        return {}
    
    para_sentence_counts = []
    for p in paragraphs:
        sents = get_sentences(p)
        para_sentence_counts.append(len(sents))
    
    n = len(para_sentence_counts)
    mean = sum(para_sentence_counts) / n if n > 0 else 0
    
    return {
        "count": n,
        "mean_sentences": round(mean, 1),
        "single_sentence_paragraphs": sum(1 for c in para_sentence_counts if c == 1),
        "distribution": {
            "1_sentence": sum(1 for c in para_sentence_counts if c == 1),
            "2_3_sentences": sum(1 for c in para_sentence_counts if 2 <= c <= 3),
            "4_5_sentences": sum(1 for c in para_sentence_counts if 4 <= c <= 5),
            "6_plus_sentences": sum(1 for c in para_sentence_counts if c >= 6),
        }
    }


def opening_word_analysis(sentences: list[str]) -> dict:
    """Analyze sentence opening patterns."""
    if not sentences:
        return {}
    
    openings = [s.split()[0].lower().rstrip('.,!?') for s in sentences if s.split()]
    
    # Count frequencies
    freq: dict[str, int] = {}
    for w in openings:
        freq[w] = freq.get(w, 0) + 1
    
    # Flag repeated openers
    repeated = {w: c for w, c in freq.items() if c >= 3}
    
    # Specific AI-associated openers
    ai_openers = [
        "furthermore", "moreover", "additionally", "however", "nevertheless",
        "therefore", "consequently", "in", "building", "leveraging", "utilizing",
        "by", "through", "this", "these", "such"
    ]
    ai_opener_hits = {w: c for w, c in freq.items() if w in ai_openers and c >= 2}
    
    # "The" dominance
    the_count = freq.get("the", 0)
    this_count = freq.get("this", 0)
    
    consecutive_same = 0
    max_consecutive = 0
    prev = None
    for o in openings:
        if o == prev:
            consecutive_same += 1
            max_consecutive = max(max_consecutive, consecutive_same)
        else:
            consecutive_same = 1
        prev = o
    
    return {
        "top_5_openers": sorted(freq.items(), key=lambda x: -x[1])[:5],
        "repeated_openers_3plus": repeated,
        "ai_associated_opener_hits": ai_opener_hits,
        "the_opener_count": the_count,
        "this_opener_count": this_count,
        "max_consecutive_same_opener": max_consecutive,
    }


def present_participial_clause_rate(text: str, sentences: list[str]) -> dict:
    """
    Proxy for present participial clause openers, the strongest single signal in
    Reinhart et al. (2025), where instruction-tuned models ran 2.2x to 5.3x the
    human rate of 1.7 per 1,000 tokens.

    KNOWN FALSE NEGATIVE, do not remove this note without fixing the cause.
    The pattern anchors with ^, so it only fires when the participle is the very
    first word. A sentence such as "By leveraging the power of caching, the team
    shipped" or "By thoughtfully implementing the change, latency fell" is a
    participial construction that this function reports as absent. Text that a
    reader would call saturated with participial openers can therefore score 0%
    here. Treat a 0% result as "none of the anchored forms", not as "none".

    Fixing this properly needs a dependency parse rather than a word list, which
    would add a spaCy dependency the toolkit deliberately avoids. Until then,
    read the SENTENCE OPENINGS section alongside this one.

    The bands below are heuristic and calibrated for this proxy, which counts
    sentences rather than tokens. They are not comparable to the per-1,000-token
    rates in the paper.
    """

    # Common participial openers used by LLMs
    participial_openers_pattern = re.compile(
        r'^\s*(Building|Leveraging|Utilizing|Combining|Considering|Recognizing|'
        r'Acknowledging|Addressing|Analyzing|Examining|Exploring|Implementing|'
        r'Integrating|Emphasizing|Highlighting|Enabling|Supporting|Providing|'
        r'Drawing|Creating|Developing|Working|Moving|Looking|Going|Taking|'
        r'Making|Having|Being|Using|Doing|Getting|Seeing|Knowing|Finding|'
        r'Understanding|Establishing|Ensuring|Focusing|Achieving|Delivering|'
        r'Bringing|Offering|Presenting|Demonstrating)\b',
        re.IGNORECASE
    )

    participial_count = sum(1 for s in sentences if participial_openers_pattern.match(s))
    rate = participial_count / len(sentences) if sentences else 0

    return {
        "participial_opener_count": participial_count,
        "participial_opener_rate": round(rate, 3),
        "sentences_analyzed": len(sentences),
        "assessment": (
            "high for this proxy" if rate > 0.15 else
            "elevated for this proxy" if rate > 0.08 else
            "normal for this proxy"
        ),
        "caveat": (
            "Anchored match only. Participles after an introductory preposition, "
            "for example 'By leveraging', are not counted."
        ),
    }


def nominalization_density(text: str, sentences: list[str]) -> dict:
    """
    Nominalization density, delegated to _shared.nominalization_stats so that
    this figure and the one metrics.py reports are always the same number.

    These two used to hold separate regexes that had drifted apart: one included
    plural suffixes and the other did not, so "opportunities" counted in one
    script and not the other, and the same input produced 91.3 and 90.6.

    Read the heuristic-proxy warning in _shared.py before quoting the number.
    """
    return nominalization_stats(text, tokenize_words(text))


def transition_word_density(text: str, sentences: list[str]) -> dict:
    """Detect overuse of transitions that instruction-tuned models favour."""
    
    mechanical_transitions = {
        "furthermore": r'\bfurthermore\b',
        "moreover": r'\bmoreover\b',
        "additionally": r'\badditionally\b',
        "in conclusion": r'\bin conclusion\b',
        "in summary": r'\bin summary\b',
        "to summarize": r'\bto summarize\b',
        "it is worth noting": r'\bit is worth noting\b',
        "it is important to": r'\bit is important to\b',
        "it should be noted": r'\bit should be noted\b',
        "with that being said": r'\bwith that being said\b',
        "having said that": r'\bhaving said that\b',
        "at the end of the day": r'\bat the end of the day\b',
        "last but not least": r'\blast but not least\b',
        "in the realm of": r'\bin the realm of\b',
        "when it comes to": r'\bwhen it comes to\b',
        "in today's world": r"\bin today'?s world\b",
        "in today's fast-paced": r"\bin today'?s fast.paced\b",
        "in the ever-evolving": r'\bin the ever.evolving\b',
    }
    
    hits = {}
    text_lower = text.lower()
    for phrase, pattern in mechanical_transitions.items():
        count = len(re.findall(pattern, text_lower))
        if count > 0:
            hits[phrase] = count
    
    total_hits = sum(hits.values())
    rate = (total_hits / len(sentences)) if sentences else 0
    
    return {
        "mechanical_transition_hits": hits,
        "total_mechanical_transitions": total_hits,
        "rate_per_sentence": round(rate, 3),
        "assessment": (
            "high for this proxy" if rate > 0.2 else
            "elevated" if rate > 0.1 else
            "normal"
        )
    }


def generic_vocabulary_hits(text: str) -> dict:
    """
    Detect AI-associated vocabulary at unusually high rates.

    The first group is the fourteen words Reinhart et al. measured at roughly
    84x to 171x the human rate in GPT-4o and GPT-4o Mini output. The rest are
    terms documented in Wikipedia's Signs of AI Writing and in corpus studies,
    with no measured multiplier attached to them.

    Two known limits. Matching is on word boundaries against the listed form,
    so inflections the list does not name are missed: 'grapple' is caught and
    'grappling' is not. And these hits require contextual interpretation. One
    occurrence is rarely a problem. A pattern of many is the signal.
    """

    ai_vocab = [
        # Extreme overrepresentation, Reinhart et al.: 84x to 171x human rate
        "camaraderie", "tapestry", "palpable", "intricate", "underscore",
        "unspoken", "amidst", "solace", "fleeting", "vibrant",
        "cacophony", "grapple", "ignite", "unravel",
        # Widely documented AI-associated terms, no measured multiplier
        "whirlwind",
        "delve", "delving", "delved",
        "leverage", "leveraging", "leveraged",
        "utilize", "utilizing", "utilized", "utilization",
        "facilitate", "facilitating", "facilitated", "facilitation",
        "comprehensive", "robust", "seamless", "streamline", "streamlined",
        "cutting-edge", "state-of-the-art", "groundbreaking", "revolutionary",
        "transformative", "paradigm shift", "paradigm-shifting",
        "crucial", "pivotal", "vital", "paramount",
        "foster", "fostering", "fostered",
        "underscoring", "underscored",
        "meticulous", "meticulously",
        "nuanced", "nuance",
        "multifaceted", "myriad",
        "evolving landscape", "ever-evolving",
        "rapidly evolving",
        "empower", "empowering", "empowered",
        "impactful", "meaningful",
    ]
    
    hits = {}
    text_lower = text.lower()
    for term in ai_vocab:
        pattern = r'\b' + re.escape(term) + r'\b'
        count = len(re.findall(pattern, text_lower))
        if count > 0:
            hits[term] = count
    
    return {
        "ai_vocabulary_hits": hits,
        "total_hit_count": sum(hits.values()),
        "unique_ai_terms": len(hits),
        "note": "Contextual interpretation required. Presence is a signal, not automatic proof of AI authorship."
    }


def passive_voice_estimate(sentences: list[str]) -> dict:
    """Rough estimate of passive voice usage."""
    passive_pattern = re.compile(
        r'\b(is|are|was|were|been|being|be)\s+\w+ed\b',
        re.IGNORECASE
    )
    
    passive_count = sum(1 for s in sentences if passive_pattern.search(s))
    rate = passive_count / len(sentences) if sentences else 0
    
    return {
        "passive_sentence_estimate": passive_count,
        "passive_rate": round(rate, 3),
        "note": "Rough estimate only. Not all -ed forms are passive voice."
    }


def list_density(text: str) -> dict:
    """Detect excessive list usage."""
    bullet_pattern = re.compile(r'^\s*[-•*]\s+', re.MULTILINE)
    numbered_pattern = re.compile(r'^\s*\d+[.)]\s+', re.MULTILINE)
    
    bullet_count = len(bullet_pattern.findall(text))
    numbered_count = len(numbered_pattern.findall(text))
    # Same denominator as every other per-1,000-words rate in the toolkit.
    total_words = len(tokenize_words(text))
    
    return {
        "bullet_items": bullet_count,
        "numbered_items": numbered_count,
        "total_list_items": bullet_count + numbered_count,
        "list_density_per_1000_words": round((bullet_count + numbered_count) / total_words * 1000, 1) if total_words > 0 else 0,
    }


def repetitive_phrase_detection(text: str) -> dict:
    """Detect repeated phrases (3-gram and 4-gram repetition)."""
    words = re.findall(r'\b\w+\b', text.lower())
    
    # Count 3-grams
    trigrams: dict[str, int] = {}
    for i in range(len(words) - 2):
        tg = ' '.join(words[i:i+3])
        if not all(w in {'the', 'a', 'an', 'of', 'in', 'to', 'is', 'are', 'and', 'or', 'but', 'for', 'that', 'this', 'it', 'on', 'at', 'by', 'as', 'with', 'from', 'be', 'was', 'were'} for w in words[i:i+3]):
            trigrams[tg] = trigrams.get(tg, 0) + 1
    
    repeated_trigrams = {k: v for k, v in trigrams.items() if v >= 3}
    
    return {
        "repeated_3grams": dict(sorted(repeated_trigrams.items(), key=lambda x: -x[1])[:10]),
        "high_repetition_phrase_count": len(repeated_trigrams),
    }


# ─── Main Analysis ────────────────────────────────────────────────────────────

def analyze(text: str) -> dict:
    """Run all structural analyses and return combined JSON report."""
    
    sentences = get_sentences(text)
    paragraphs = get_paragraphs(text)
    
    return {
        "word_count": len(tokenize_words(text)),
        "sentence_count": len(sentences),
        "paragraph_count": len(paragraphs),
        "sentence_lengths": sentence_lengths(sentences),
        "paragraph_structure": paragraph_lengths(paragraphs),
        "opening_analysis": opening_word_analysis(sentences),
        "participial_clauses": present_participial_clause_rate(text, sentences),
        "nominalization_density": nominalization_density(text, sentences),
        "transition_words": transition_word_density(text, sentences),
        "generic_vocabulary": generic_vocabulary_hits(text),
        "passive_voice": passive_voice_estimate(sentences),
        "list_density": list_density(text),
        "phrase_repetition": repetitive_phrase_detection(text),
    }


def human_readable_summary(result: dict) -> str:
    """Convert JSON analysis to a readable diagnostic summary."""
    
    lines = []
    lines.append("NOT AI : STRUCTURAL ANALYSIS")
    lines.append("─" * 40)
    lines.append(f"Words: {result['word_count']}  |  Sentences: {result['sentence_count']}  |  Paragraphs: {result['paragraph_count']}")
    lines.append("")
    
    # Sentence rhythm
    sl = result['sentence_lengths']
    lines.append("SENTENCE RHYTHM")
    lines.append(f"  Mean length:   {sl['mean']} words")
    lines.append(f"  Std deviation: {sl['std']} words  (burstiness: {sl['burstiness']})")
    dist = sl.get('distribution', {})
    lines.append(f"  Very short (<8):  {dist.get('very_short_under_8', 0)}  |  Short (8-15): {dist.get('short_8_to_15', 0)}  |  Medium (16-25): {dist.get('medium_16_to_25', 0)}")
    lines.append(f"  Long (26-35):  {dist.get('long_26_to_35', 0)}  |  Very long (35+): {dist.get('very_long_over_35', 0)}")
    
    if sl['burstiness'] < 0.30:
        lines.append("  ⚠ Low burstiness: sentence lengths are very uniform")
    elif sl['burstiness'] > 0.55:
        lines.append("  ✓ Good length variation")
    lines.append("")
    
    # Structural signals
    lines.append("STRUCTURAL SIGNALS")
    
    pc = result['participial_clauses']
    assessment_icon = "⚠" if pc['assessment'].startswith(("high", "elevated")) else "✓"
    lines.append(f"  {assessment_icon} Participial clause openers: {pc['participial_opener_count']} / {pc['sentences_analyzed']} sentences ({pc['participial_opener_rate']:.0%})  |  {pc['assessment']}")
    if pc['participial_opener_count'] == 0:
        lines.append("      Anchored match only. 'By leveraging...' style openers are not counted.")

    nd = result['nominalization_density']
    assessment_icon = "⚠" if nd['assessment'].startswith(("high", "elevated")) else "✓"
    lines.append(f"  {assessment_icon} Nominalization density: {nd['rate_per_1000_words']} per 1,000 words  |  {nd['assessment']}")
    lines.append("      Proxy measure. Compare only against another run of this script.")

    tw = result['transition_words']
    if tw['total_mechanical_transitions'] > 0:
        lines.append(f"  ⚠ Mechanical transitions: {tw['total_mechanical_transitions']} instances  |  {', '.join(tw['mechanical_transition_hits'].keys())}")
    else:
        lines.append("  ✓ No high-frequency mechanical transitions detected")
    lines.append("")
    
    # Opening patterns
    oa = result['opening_analysis']
    lines.append("SENTENCE OPENINGS")
    if oa.get('repeated_openers_3plus'):
        for w, c in oa['repeated_openers_3plus'].items():
            lines.append(f"  ⚠ '{w}' used to open {c} sentences")
    else:
        lines.append("  ✓ No highly repeated sentence openers")
    if oa.get('max_consecutive_same_opener', 0) >= 3:
        lines.append(f"  ⚠ {oa['max_consecutive_same_opener']} consecutive sentences with same opener")
    lines.append("")
    
    # Vocabulary
    #
    # The bullet list is capped at eight terms, and the cap used to be silent.
    # Two tables in examples/ were written by counting the bullets and reported
    # 8 unique terms for a text that contained 14. So the total is printed
    # whether or not anything was cut, and anything cut is named. A reader who
    # counts the bullets now gets contradicted on the next line instead of
    # months later. measure.py prints these same two lines verbatim.
    gv = result['generic_vocabulary']
    lines.append("AI-ASSOCIATED VOCABULARY")
    if gv['ai_vocabulary_hits']:
        ranked = sorted(gv['ai_vocabulary_hits'].items(), key=lambda x: -x[1])
        for term, count in ranked[:8]:
            lines.append(f"  • '{term}': {count}x")
        if len(ranked) > 8:
            rest = ', '.join(f"'{t}'" for t, _ in ranked[8:])
            lines.append(f"  ... {len(ranked) - 8} more not listed above: {rest}")
        lines.append(f"  Total: {gv['unique_ai_terms']} unique terms, "
                     f"{sum(gv['ai_vocabulary_hits'].values())} occurrences")
        lines.append(f"  Note: {gv['note']}")
    else:
        lines.append("  ✓ No high-frequency AI vocabulary detected")
    lines.append("")
    
    # Phrase repetition
    pr = result['phrase_repetition']
    if pr['repeated_3grams']:
        lines.append("REPEATED PHRASES")
        for phrase, count in list(pr['repeated_3grams'].items())[:5]:
            lines.append(f"  ⚠ '{phrase}': {count}x")
        lines.append("")
    
    return '\n'.join(lines)


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Not Ai: structural writing analyzer'
    )
    parser.add_argument('input_file', nargs='?', help='Input text file')
    parser.add_argument('--stdin', action='store_true', help='Read from stdin')
    parser.add_argument('--json', action='store_true', help='Output raw JSON (default: human-readable)')
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
