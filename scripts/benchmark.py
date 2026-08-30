#!/usr/bin/env python3
"""
not-ai: benchmark.py
Benchmark runner for Not Ai.

Measures semantic preservation, structural change magnitude, readability delta,
and produces a reproducible report. Requires human-provided rewritten text to evaluate.

Usage:
    python scripts/benchmark.py --corpus benchmarks/corpus/ --dry-run
    python scripts/benchmark.py --input original.txt --output rewritten.txt
    python scripts/benchmark.py --help

Metrics computed:
    - Semantic similarity (token-overlap proxy; full version requires sentence-transformers)
    - Structural change delta (burstiness, nominalization, transition rate)
    - Readability delta (Flesch-Kincaid grade change)
    - Factual claim preservation (manual flag — cannot be automated reliably)
    - Word count change

Note on benchmark integrity:
    All scores require ground truth. Do not fabricate performance numbers.
    Run this script on real pairs of (original, rewritten) text to obtain real scores.
"""

import sys
import re
import json
import argparse
import math
from pathlib import Path


# ─── Import sibling scripts ───────────────────────────────────────────────────
# Allow running from project root or scripts/ directory
_script_dir = Path(__file__).parent
sys.path.insert(0, str(_script_dir))

try:
    from analyze_structure import analyze as analyze_structure, get_sentences
    from metrics import analyze as analyze_metrics
    from repetition import analyze as analyze_repetition
    _deps_available = True
except ImportError:
    _deps_available = False
    print("Warning: Could not import sibling scripts. Running in standalone mode.", file=sys.stderr)


# ─── Semantic Similarity (token overlap) ─────────────────────────────────────

STOPWORDS = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'to', 'of', 'in', 'for', 'on', 'with', 'at',
    'by', 'and', 'or', 'but', 'not', 'as', 'it', 'this', 'that', 'i',
    'you', 'he', 'she', 'we', 'they', 'do', 'does', 'did', 'will', 'would',
}


def token_overlap_similarity(text_a: str, text_b: str) -> float:
    """
    Jaccard similarity of content word sets.
    
    Approximates semantic similarity without requiring ML models.
    For production use, replace with sentence-transformers cosine similarity.
    
    Returns: 0.0 (no overlap) to 1.0 (identical content)
    """
    def content_words(text):
        words = re.findall(r'\b[a-z]+\b', text.lower())
        return set(w for w in words if w not in STOPWORDS and len(w) > 3)
    
    words_a = content_words(text_a)
    words_b = content_words(text_b)
    
    if not words_a and not words_b:
        return 1.0
    if not words_a or not words_b:
        return 0.0
    
    intersection = words_a & words_b
    union = words_a | words_b
    return len(intersection) / len(union)


def claim_count_proxy(text: str) -> int:
    """
    Rough proxy for number of factual claims (declarative sentences).
    A proper claim extractor would use NLP. This is a count-based approximation.
    """
    sentences = re.split(r'(?<=[.!?])\s+', text.strip())
    declarative = [s for s in sentences if s.strip() and not s.strip().endswith('?')]
    return len(declarative)


def number_preservation(text_a: str, text_b: str) -> dict:
    """
    Check whether numbers present in the original appear in the rewritten version.
    Numbers are high-value factual content — their disappearance indicates meaning drift.
    """
    numbers_a = set(re.findall(r'\b\d[\d,\.%]*\b', text_a))
    numbers_b = set(re.findall(r'\b\d[\d,\.%]*\b', text_b))
    
    missing = numbers_a - numbers_b
    added = numbers_b - numbers_a
    
    preservation_rate = len(numbers_a - missing) / len(numbers_a) if numbers_a else 1.0
    
    return {
        "numbers_in_original": sorted(numbers_a),
        "numbers_in_rewrite": sorted(numbers_b),
        "missing_numbers": sorted(missing),
        "added_numbers": sorted(added),
        "preservation_rate": round(preservation_rate, 3),
        "assessment": "⚠ Numbers lost" if missing else "✓ Numbers preserved"
    }


def word_count_change(text_a: str, text_b: str) -> dict:
    wc_a = len(text_a.split())
    wc_b = len(text_b.split())
    delta = wc_b - wc_a
    pct = (delta / wc_a * 100) if wc_a > 0 else 0
    
    return {
        "original_words": wc_a,
        "rewritten_words": wc_b,
        "delta": delta,
        "percent_change": round(pct, 1),
        "assessment": (
            "⚠ Significant expansion (+20%+)" if pct > 20 else
            "⚠ Significant reduction (-20%+)" if pct < -20 else
            "✓ Length roughly preserved"
        )
    }


# ─── Structural Delta ─────────────────────────────────────────────────────────

def structural_delta(orig_struct: dict, new_struct: dict) -> dict:
    """Measure how much the structural signature changed."""
    
    orig_burstiness = orig_struct.get('sentence_lengths', {}).get('burstiness', 0)
    new_burstiness = new_struct.get('sentence_lengths', {}).get('burstiness', 0)
    
    orig_pc = orig_struct.get('participial_clauses', {}).get('participial_opener_rate', 0)
    new_pc = new_struct.get('participial_clauses', {}).get('participial_opener_rate', 0)
    
    orig_nom = orig_struct.get('nominalization_density', {}).get('rate_per_1000_words', 0)
    new_nom = new_struct.get('nominalization_density', {}).get('rate_per_1000_words', 0)
    
    orig_tw = orig_struct.get('transition_words', {}).get('rate_per_sentence', 0)
    new_tw = new_struct.get('transition_words', {}).get('rate_per_sentence', 0)
    
    return {
        "burstiness_delta": round(new_burstiness - orig_burstiness, 3),
        "participial_rate_delta": round(new_pc - orig_pc, 3),
        "nominalization_delta": round(new_nom - orig_nom, 1),
        "transition_rate_delta": round(new_tw - orig_tw, 3),
        "direction_burstiness": "improved" if new_burstiness > orig_burstiness else "worsened" if new_burstiness < orig_burstiness - 0.05 else "unchanged",
        "direction_participial": "improved" if new_pc < orig_pc else "worsened" if new_pc > orig_pc + 0.02 else "unchanged",
        "direction_nominalization": "improved" if new_nom < orig_nom else "worsened" if new_nom > orig_nom + 3 else "unchanged",
        "direction_transitions": "improved" if new_tw < orig_tw else "worsened" if new_tw > orig_tw + 0.05 else "unchanged",
    }


# ─── Full Pair Evaluation ─────────────────────────────────────────────────────

def evaluate_pair(original: str, rewritten: str, pair_name: str = "unnamed") -> dict:
    """Evaluate one (original, rewritten) pair and return a benchmark report."""
    
    result = {
        "pair": pair_name,
        "semantic_similarity": round(token_overlap_similarity(original, rewritten), 3),
        "number_preservation": number_preservation(original, rewritten),
        "word_count_change": word_count_change(original, rewritten),
    }
    
    if _deps_available:
        orig_struct = analyze_structure(original)
        new_struct = analyze_structure(rewritten)
        orig_metrics = analyze_metrics(original)
        new_metrics = analyze_metrics(rewritten)
        
        result["structural_delta"] = structural_delta(orig_struct, new_struct)
        result["readability_delta"] = {
            "fk_grade_original": orig_metrics['readability']['flesch_kincaid_grade'],
            "fk_grade_rewritten": new_metrics['readability']['flesch_kincaid_grade'],
            "fk_delta": round(new_metrics['readability']['flesch_kincaid_grade'] - orig_metrics['readability']['flesch_kincaid_grade'], 1),
            "ease_original": orig_metrics['readability']['flesch_reading_ease'],
            "ease_rewritten": new_metrics['readability']['flesch_reading_ease'],
        }
        result["ai_vocabulary_delta"] = {
            "original_ai_terms": orig_struct['generic_vocabulary']['unique_ai_terms'],
            "rewritten_ai_terms": new_struct['generic_vocabulary']['unique_ai_terms'],
            "delta": new_struct['generic_vocabulary']['unique_ai_terms'] - orig_struct['generic_vocabulary']['unique_ai_terms'],
        }
    
    # Semantic similarity thresholds
    sim = result['semantic_similarity']
    result['semantic_assessment'] = (
        "⚠ Major meaning drift" if sim < 0.40 else
        "⚠ Moderate meaning change" if sim < 0.55 else
        "✓ Meaning largely preserved" if sim < 0.80 else
        "✓ High meaning preservation"
    )
    
    return result


def print_pair_report(result: dict):
    """Print a human-readable benchmark report."""
    print(f"\nNOT AI BENCHMARK — {result['pair'].upper()}")
    print("─" * 50)
    
    print(f"\nSEMANTIC PRESERVATION")
    print(f"  Token overlap similarity: {result['semantic_similarity']:.1%}")
    print(f"  {result['semantic_assessment']}")
    
    np = result['number_preservation']
    print(f"\nFACTUAL PRESERVATION (NUMBERS)")
    print(f"  {np['assessment']}")
    if np.get('missing_numbers'):
        print(f"  Missing: {', '.join(np['missing_numbers'])}")
    
    wc = result['word_count_change']
    print(f"\nWORD COUNT")
    print(f"  {wc['original_words']} → {wc['rewritten_words']} ({wc['percent_change']:+.1f}%)")
    print(f"  {wc['assessment']}")
    
    if 'structural_delta' in result:
        sd = result['structural_delta']
        print(f"\nSTRUCTURAL CHANGES")
        print(f"  Sentence burstiness:  {sd['direction_burstiness']} ({sd['burstiness_delta']:+.3f})")
        print(f"  Participial clauses:  {sd['direction_participial']} ({sd['participial_rate_delta']:+.3f})")
        print(f"  Nominalization:       {sd['direction_nominalization']} ({sd['nominalization_delta']:+.1f}/1k words)")
        print(f"  Mechanical transitions: {sd['direction_transitions']} ({sd['transition_rate_delta']:+.3f}/sentence)")
    
    if 'ai_vocabulary_delta' in result:
        avd = result['ai_vocabulary_delta']
        print(f"\nAI VOCABULARY")
        print(f"  Before: {avd['original_ai_terms']} AI-associated terms")
        print(f"  After:  {avd['rewritten_ai_terms']} AI-associated terms  ({avd['delta']:+d})")
    
    if 'readability_delta' in result:
        rd = result['readability_delta']
        print(f"\nREADABILITY")
        print(f"  Flesch-Kincaid grade: {rd['fk_grade_original']} → {rd['fk_grade_rewritten']} ({rd['fk_delta']:+.1f})")
        print(f"  Reading ease: {rd['ease_original']} → {rd['ease_rewritten']}")


# ─── CLI ─────────────────────────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(
        description='Not Ai — benchmark runner',
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Evaluate a single pair
  python scripts/benchmark.py --input original.txt --output rewritten.txt

  # Evaluate all pairs in a directory (expects original.txt + rewritten.txt in each subdir)
  python scripts/benchmark.py --corpus benchmarks/corpus/

  # Dry run — check that scripts are working
  python scripts/benchmark.py --dry-run

IMPORTANT: Do not fabricate scores. All numbers must come from real evaluations.
        """
    )
    parser.add_argument('--input', help='Original text file')
    parser.add_argument('--output', help='Rewritten text file')
    parser.add_argument('--corpus', help='Corpus directory (expects subdirs with original.txt + rewritten.txt)')
    parser.add_argument('--dry-run', action='store_true', help='Test that scripts are working')
    parser.add_argument('--json', action='store_true', help='Output raw JSON')
    args = parser.parse_args()
    
    if args.dry_run:
        sample = "This is a test sentence to verify that the benchmark script is working correctly. It has multiple sentences of varying lengths. Some are short. Others extend longer to test the sentence length distribution analysis. The script should run without errors."
        result = evaluate_pair(sample, sample, "dry-run")
        print("✓ Benchmark script loaded and running correctly.")
        print(f"  Dependencies available: {_deps_available}")
        print_pair_report(result)
        return
    
    if args.input and args.output:
        original = Path(args.input).read_text(encoding='utf-8')
        rewritten = Path(args.output).read_text(encoding='utf-8')
        name = Path(args.input).stem
        result = evaluate_pair(original, rewritten, name)
        
        if args.json:
            print(json.dumps(result, indent=2))
        else:
            print_pair_report(result)
        return
    
    if args.corpus:
        corpus_dir = Path(args.corpus)
        results = []
        for subdir in sorted(corpus_dir.iterdir()):
            if not subdir.is_dir():
                continue
            orig_file = subdir / 'original.txt'
            rew_file = subdir / 'rewritten.txt'
            if not orig_file.exists() or not rew_file.exists():
                print(f"Skipping {subdir.name}: missing original.txt or rewritten.txt", file=sys.stderr)
                continue
            original = orig_file.read_text(encoding='utf-8')
            rewritten = rew_file.read_text(encoding='utf-8')
            result = evaluate_pair(original, rewritten, subdir.name)
            results.append(result)
            if args.json:
                pass  # collect and print at end
            else:
                print_pair_report(result)
        
        if results:
            avg_sim = sum(r['semantic_similarity'] for r in results) / len(results)
            print(f"\n{'─'*50}")
            print(f"AGGREGATE RESULTS — {len(results)} pairs")
            print(f"  Mean semantic similarity: {avg_sim:.1%}")
        
        if args.json:
            print(json.dumps(results, indent=2))
        return
    
    parser.print_help()


if __name__ == '__main__':
    main()
