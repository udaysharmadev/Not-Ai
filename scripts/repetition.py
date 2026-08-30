#!/usr/bin/env python3
"""
not-ai: repetition.py
Detects repetitive language patterns at the phrase, sentence, and structural level.

Usage:
    python scripts/repetition.py [input_file]
    python scripts/repetition.py --stdin
    cat myfile.txt | python scripts/repetition.py --stdin
"""

import sys
import re
import json
import argparse
from pathlib import Path
from collections import Counter


STOPWORDS = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'shall', 'can', 'to', 'of', 'in', 'for',
    'on', 'with', 'at', 'by', 'from', 'up', 'about', 'into', 'through',
    'and', 'or', 'but', 'not', 'as', 'so', 'if', 'it', 'its', 'this',
    'that', 'these', 'those', 'i', 'you', 'he', 'she', 'we', 'they',
    'my', 'your', 'his', 'her', 'our', 'their', 'me', 'him', 'us', 'them',
    'what', 'which', 'who', 'whom', 'when', 'where', 'why', 'how',
    'all', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
    'than', 'too', 'very', 's', 't', 'can', 'just', 'don', 'now',
}


def get_sentences(text: str) -> list[str]:
    text = re.sub(r'\s+', ' ', text.strip())
    sentences = re.split(r'(?<=[.!?])\s+(?=[A-Z"\'])', text)
    return [s.strip() for s in sentences if s.strip() and len(s.split()) >= 2]


def get_paragraphs(text: str) -> list[str]:
    paras = re.split(r'\n\s*\n', text.strip())
    return [p.strip() for p in paras if p.strip()]


def extract_ngrams(words: list[str], n: int, stopword_filter: bool = True) -> Counter:
    """Extract n-grams, optionally filtering all-stopword grams."""
    grams = Counter()
    for i in range(len(words) - n + 1):
        gram = words[i:i + n]
        if stopword_filter:
            non_stop = [w for w in gram if w not in STOPWORDS]
            if len(non_stop) < max(1, n // 2):
                continue
        grams[' '.join(gram)] += 1
    return grams


def repeated_phrases(text: str) -> dict:
    """Find repeated significant n-grams (3-5 words)."""
    words = re.findall(r'\b[a-z]+\b', text.lower())
    
    results = {}
    for n in [3, 4, 5]:
        grams = extract_ngrams(words, n)
        repeated = {k: v for k, v in grams.items() if v >= 2}
        if repeated:
            top = dict(sorted(repeated.items(), key=lambda x: -x[1])[:10])
            results[f'{n}-grams'] = top
    
    return results


def repeated_sentence_openings(sentences: list[str]) -> dict:
    """Find sentences sharing the same 2-3 word opening."""
    two_word_openings = Counter()
    three_word_openings = Counter()
    
    for sent in sentences:
        words = sent.lower().split()
        if len(words) >= 2:
            two_word_openings[' '.join(words[:2])] += 1
        if len(words) >= 3:
            three_word_openings[' '.join(words[:3])] += 1
    
    return {
        "repeated_2word_openings": {k: v for k, v in two_word_openings.items() if v >= 3},
        "repeated_3word_openings": {k: v for k, v in three_word_openings.items() if v >= 2},
    }


def paragraph_structure_repetition(paragraphs: list[str]) -> dict:
    """Detect if paragraphs follow the same structural template."""
    structures = []
    for para in paragraphs:
        sents = get_sentences(para)
        lengths = [len(s.split()) for s in sents]
        # Normalize to a structural "shape"
        shape = tuple('S' if l < 12 else 'M' if l < 25 else 'L' for l in lengths)
        structures.append(shape)
    
    shape_counter = Counter(structures)
    repeated_shapes = {str(k): v for k, v in shape_counter.items() if v >= 2 and len(k) >= 2}
    
    return {
        "total_paragraphs": len(paragraphs),
        "unique_structural_shapes": len(shape_counter),
        "repeated_shapes": repeated_shapes,
        "structural_monotony_warning": len(shape_counter) < max(1, len(paragraphs) / 3),
    }


def transition_phrase_repetition(text: str) -> dict:
    """Detect repeated transition phrases."""
    transitions = [
        r'furthermore', r'moreover', r'additionally', r'however',
        r'therefore', r'consequently', r'as a result', r'in conclusion',
        r'to summarize', r'in summary', r'in addition', r'on the other hand',
        r'that said', r'with that said', r'having said that',
        r'it is worth noting', r'it is important to note', r'it should be noted',
        r'building on this', r'leveraging this', r'given this',
        r'this demonstrates', r'this shows', r'this highlights', r'this underscores',
        r'this illustrates', r'this reveals',
    ]
    
    hits = {}
    text_lower = text.lower()
    for phrase in transitions:
        count = len(re.findall(r'\b' + phrase + r'\b', text_lower))
        if count >= 2:
            hits[phrase] = count
    
    return {
        "repeated_transitions": hits,
        "warning": "High transition repetition creates mechanical rhythm" if len(hits) >= 3 else None,
    }


def lexical_diversity(text: str) -> dict:
    """Compute type-token ratio as a proxy for lexical diversity."""
    words = re.findall(r'\b[a-z]+\b', text.lower())
    if not words:
        return {}
    
    total_tokens = len(words)
    unique_types = len(set(words))
    ttr = unique_types / total_tokens
    
    # Content words only
    content_words = [w for w in words if w not in STOPWORDS and len(w) > 3]
    content_ttr = len(set(content_words)) / len(content_words) if content_words else 0
    
    return {
        "total_tokens": total_tokens,
        "unique_types": unique_types,
        "type_token_ratio": round(ttr, 3),
        "content_word_ttr": round(content_ttr, 3),
        "assessment": (
            "low diversity (AI-like)" if content_ttr < 0.55 else
            "moderate diversity" if content_ttr < 0.70 else
            "high diversity"
        )
    }


def analyze(text: str) -> dict:
    sentences = get_sentences(text)
    paragraphs = get_paragraphs(text)
    
    return {
        "repeated_phrases": repeated_phrases(text),
        "repeated_sentence_openings": repeated_sentence_openings(sentences),
        "paragraph_structure_repetition": paragraph_structure_repetition(paragraphs),
        "transition_phrase_repetition": transition_phrase_repetition(text),
        "lexical_diversity": lexical_diversity(text),
    }


def human_readable_summary(result: dict) -> str:
    lines = []
    lines.append("NOT AI — REPETITION ANALYSIS")
    lines.append("─" * 40)
    
    # Repeated phrases
    rp = result['repeated_phrases']
    if rp:
        lines.append("\nREPEATED PHRASES")
        for gram_type, phrases in rp.items():
            for phrase, count in list(phrases.items())[:5]:
                lines.append(f"  • '{phrase}': {count}x")
    else:
        lines.append("\nREPEATED PHRASES: None detected ✓")
    
    # Repeated openings
    ro = result['repeated_sentence_openings']
    rep3 = ro.get('repeated_3word_openings', {})
    rep2 = ro.get('repeated_2word_openings', {})
    if rep3 or rep2:
        lines.append("\nREPEATED SENTENCE OPENINGS")
        for phrase, count in {**rep3, **rep2}.items():
            if count >= 2:
                lines.append(f"  ⚠ '{phrase}': {count} sentences")
    else:
        lines.append("\nREPEATED OPENINGS: None detected ✓")
    
    # Paragraph structure
    psr = result['paragraph_structure_repetition']
    if psr.get('structural_monotony_warning'):
        lines.append(f"\n⚠ PARAGRAPH STRUCTURE: {psr['unique_structural_shapes']} unique shapes for {psr['total_paragraphs']} paragraphs — paragraphs may be structurally monotonous")
    else:
        lines.append(f"\nPARAGRAPH STRUCTURE: {psr['unique_structural_shapes']} unique shapes ✓")
    
    # Transition repetition
    tr = result['transition_phrase_repetition']
    if tr['repeated_transitions']:
        lines.append("\nREPEATED TRANSITIONS")
        for phrase, count in tr['repeated_transitions'].items():
            lines.append(f"  ⚠ '{phrase}': {count}x")
    else:
        lines.append("\nTRANSITIONS: No high-frequency repetition ✓")
    
    # Lexical diversity
    ld = result['lexical_diversity']
    if ld:
        icon = "✓" if "high" in ld['assessment'] else "⚠"
        lines.append(f"\nLEXICAL DIVERSITY: {ld['content_word_ttr']:.0%} content-word TTR — {ld['assessment']} {icon}")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Not Ai — repetition analyzer')
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
