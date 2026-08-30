#!/usr/bin/env python3
"""
not-ai: repetition.py
Detects repetitive language patterns at the phrase, sentence, and structural level.

Usage:
    python scripts/repetition.py [input_file]
    python scripts/repetition.py [input_file] --json
    python scripts/repetition.py --stdin
    cat myfile.txt | python scripts/repetition.py --stdin

Output: a human-readable report to stdout. Pass --json for the raw figures.
"""

import sys
import re
import json
import argparse
from pathlib import Path
from collections import Counter

# Import the shared measurement primitives. Inserting this script's own
# directory first keeps the import working from any working directory.
sys.path.insert(0, str(Path(__file__).resolve().parent))
from _shared import get_sentences, get_paragraphs, tokenize_words  # noqa: E402


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


# ─── Syntactic frames ────────────────────────────────────────────────────────
#
# Why this exists. Every other repetition check in this file works on words:
# repeated n-grams, repeated openings, repeated transitions. A text can pass all
# three and still repeat itself, because what repeats is the shape of the
# sentence rather than any word in it. The case that prompted this check:
#
#   Its history stretches from the Indus Valley cities of 2500 BCE through
#   Mughal architecture to independence in 1947. Geography here swings from
#   Himalayan peaks to tropical coastlines, deserts in Rajasthan to monsoon
#   forests in the northeast.
#
# Two consecutive sentences, no shared 3-gram, no shared opening, and the same
# move both times: name a domain, then sweep across its range. Every word-level
# check in this file reads that as clean.
#
# WHAT THIS IS NOT. It is not a parser and it has no part-of-speech
# information. It is a fixed list of eight named constructions, each a regex,
# each chosen because it is a shape rather than a phrase. A frame not on the
# list is not detected, and the list is not a claim about which frames matter
# most; it is the set that could be matched reliably without a parser. Frames
# absent by construction include the "X is not about Y, it is about Z" pivot,
# rhetorical-question openers, and any parallelism that spans sentences without
# a lexical anchor.
#
# Two names are deliberately mechanical, because two of these frames match more
# than their linguistic label would suggest. "comma plus -ing word" is the wider
# one: it fires on a genuine participial tail in `The team shipped in six weeks,
# leveraging existing infrastructure`, and equally on a gerund subject in `In
# conclusion, caching remains an indispensable tool`, where nothing is appended
# to anything. Calling that frame "participial tail" would have been a claim the
# regex cannot support, so it is named after what it matches. "comma plus -ed by"
# has the same shape of limit, matching any past participle before `by`.
#
# Frames are counted on the file as written, including fenced code blocks and
# quoted specimens. That is consistent with every other measurement here and it
# has a visible consequence: `references/style-research.md` carries specimen
# sentences chosen to demonstrate participial clauses, so it reports a
# back-to-back repeat on two lines that exist precisely to show one. Read the
# printed sentences before believing any warning. `scripts/scan_prose.py` is the
# script that understands the citation-versus-use convention; this one does not.
#
# The only warning this raises is the same frame in two consecutive sentences.
# That condition is deliberately not tunable: consecutive is the smallest
# possible window, so there is no threshold here to quietly fit to a specimen.
# A frame used four times across forty sentences is reported without a warning,
# because in a long piece that may be the right density and the script has no
# way to know.

SYNTACTIC_FRAMES = (
    (
        "range sweep",
        r"\bfrom\b[^.;:]{1,80}?\b(?:to|through|into)\b",
        "from X to Y: sweeps across a span instead of picking a point in it",
    ),
    (
        "comparative than",
        r"\b(?:more|less|fewer|greater)\b[^.;:]{1,60}?\bthan\b",
        "more X than Y: rates the subject against a foil rather than describing it",
    ),
    (
        "superlative membership",
        r"\bone of the\b[^.;:]{0,40}?(?:\b\w+est\b|\bmost\b|\bleast\b)",
        "one of the most X: a ranking claim with no rank in it",
    ),
    (
        "scale superlative",
        r"\b(?:world|nation|country|continent|planet|industry|region|market)(?:'s|s')"
        r"\s+(?:\w+\s+){0,3}?(?:most|largest|biggest|fastest|oldest|leading|greatest)\b",
        "the world's largest X: scale asserted by superlative",
    ),
    (
        "not just X but Y",
        r"\bnot\s+(?:just|only|merely|simply)\b[^.;:]{1,80}?\b(?:but|it['’]s|it is)\b",
        "not just X but Y: the pivot on the standing avoid-list",
    ),
    (
        "comma plus -ing word",
        r",\s+(?!and\b|but\b|or\b|which\b|who\b|whose\b|where\b|while\b|when\b)\w+ing\b",
        "..., doing Y: appends an action without saying how it relates",
    ),
    (
        "comma plus -ed by",
        r",\s+\w+ed\s+by\b",
        "..., driven by Y: names a cause in a form that hides who acts",
    ),
    (
        "where X meets Y",
        r"\bwhere\b[^.;:]{1,50}?\bmeets?\b",
        "where X meets Y: positions the subject between two abstractions",
    ),
)

_FRAME_PATTERNS = tuple(
    (name, re.compile(pattern, re.IGNORECASE), note)
    for name, pattern, note in SYNTACTIC_FRAMES
)


def repeated_syntactic_frames(sentences: list[str]) -> dict:
    """
    Which of the named frames each sentence uses, and where one recurs.

    `frame_counts` counts sentences, not matches, so a sentence using the range
    sweep twice counts once. `consecutive_repeats` is the only warning-bearing
    key: it lists frames that appear in two adjacent sentences.
    """
    per_sentence = []
    for i, sent in enumerate(sentences):
        hits = sorted(name for name, pattern, _ in _FRAME_PATTERNS if pattern.search(sent))
        if hits:
            per_sentence.append({"sentence_index": i, "frames": hits})

    counts = Counter()
    for entry in per_sentence:
        for name in entry["frames"]:
            counts[name] += 1

    frames_by_index = {e["sentence_index"]: set(e["frames"]) for e in per_sentence}
    consecutive = []
    for i in range(len(sentences) - 1):
        shared = frames_by_index.get(i, set()) & frames_by_index.get(i + 1, set())
        for name in sorted(shared):
            consecutive.append({
                "frame": name,
                "sentence_indices": [i, i + 1],
                "first": sentences[i][:90],
                "second": sentences[i + 1][:90],
            })

    return {
        "total_sentences": len(sentences),
        "frame_counts": dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))),
        "sentences_using_a_frame": len(per_sentence),
        "consecutive_repeats": consecutive,
    }


# ─── Coordinated series of three ─────────────────────────────────────────────
#
# The tricolon. Three items joined by a final "and" or "or", which reads as
# cadence whether or not the third item carries anything:
#
#   powered by a young workforce, a booming tech sector, and cities like
#   Bengaluru and Mumbai
#
# Whether a given series earns its third item is a judgment about content, and
# no regex can make it. So this reports and does not rule: it prints the series
# it found and leaves the reading to whoever is editing. The one exception is a
# lexically parallel triple, where all three items open with the same token
# ("a ..., a ..., and a ..."). That anaphora is a rhythm device by construction,
# not an accident of content, so it carries a warning.
#
# The warning is a prompt to look, not a finding. A parallel triple can be doing
# real work: `references/methodology.md` carries `whether the voice survived,
# whether the genre rules were the right ones, and whether the change` and those
# are three distinct questions, so the repeated `whether` is carrying the
# structure rather than decorating it. The test to apply is whether removing the
# third item loses information or only loses cadence.
#
# Detection is comma-delimited and requires the Oxford comma: a segment opening
# with "and" or "or", preceded by at least two other segments. Series written
# without the Oxford comma are missed entirely, which is a real gap and not a
# rounding error. Segment counts include sentence-initial adverbials, so
# "Economically, X, Y, and Z" reads as four segments for a three-item series;
# the printed span is there so that miscount is visible rather than silent. The
# same looseness means an opening adverbial in front of a compound sentence
# ("Economically, India grew, and Bollywood thrived") is reported as a series
# although it is not a list at all. That case is pinned in
# `scripts/verify_checks.py` as a known limit.
#
# One wrinkle worth spelling out, because the obvious implementation gets it
# wrong. The first item of a series shares its comma segment with the sentence
# stem: in "The plan needed a bigger room, a longer window, and a second
# reviewer" the first item is "a bigger room" and the segment is "The plan
# needed a bigger room". Reading the segment's first word gives "The", so a
# naive lead-word comparison finds the/a/a and misses a plainly parallel triple.
# The anaphora is therefore established on items two and three, which are whole
# segments, and confirmed by looking for the same word inside the first segment.

_SERIES_COORDINATOR = re.compile(r"^(?:and|or)\s+\S", re.IGNORECASE)
_LEAD_TOKEN = re.compile(r"^(?:and\s+|or\s+)?([a-zA-Z']+)", re.IGNORECASE)


def _segments(sentence: str) -> list[str]:
    return [seg.strip() for seg in sentence.split(",")]


def _lead_word(segment: str) -> str:
    """The segment's first word, ignoring a leading coordinator."""
    match = _LEAD_TOKEN.match(segment)
    return match.group(1).lower() if match else ""


def _first_item(segment: str, lead: str) -> str:
    """
    The slice of the stem segment that starts at the last whole-word occurrence
    of `lead` and still has a word after it, or "" if there is none. That slice
    is the first item of the series.
    """
    if not lead or not lead[0].isalpha():
        return ""
    for match in reversed(list(re.finditer(r"\b" + re.escape(lead) + r"\b",
                                           segment, re.IGNORECASE))):
        rest = segment[match.start():]
        if len(rest.split()) >= 2:
            return rest
    return ""


def coordinated_series(sentences: list[str], word_count: int) -> dict:
    """
    Comma-delimited series closing on "and" or "or", plus the subset whose three
    final items all open with the same word.

    In a series of more than three items only the last three are examined for
    anaphora, so "a W, a X, a Y, and a Z" reports one parallel triple rather
    than a parallel quartet.
    """
    found = []
    parallel = []

    for i, sent in enumerate(sentences):
        segs = _segments(sent)
        if len(segs) < 3:
            continue
        if not _SERIES_COORDINATOR.match(segs[-1]):
            continue

        tail = segs[-3:]
        found.append({
            "sentence_index": i,
            "comma_segments": len(segs),
            "series_tail": tail,
        })

        lead = _lead_word(tail[1])
        if lead and lead == _lead_word(tail[2]):
            first = _first_item(tail[0], lead)
            if first:
                parallel.append({
                    "sentence_index": i,
                    "lead_word": lead,
                    "items": [first, tail[1], tail[2]],
                })

    rate = (len(found) / word_count * 1000) if word_count else 0.0
    return {
        "series_count": len(found),
        "series_rate_per_1000_words": round(rate, 1),
        "series": found,
        "parallel_triples": parallel,
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
            "low diversity for this proxy" if content_ttr < 0.55 else
            "moderate diversity" if content_ttr < 0.70 else
            "high diversity"
        )
    }


def analyze(text: str) -> dict:
    sentences = get_sentences(text)
    paragraphs = get_paragraphs(text)
    word_count = len(tokenize_words(text))

    return {
        "repeated_phrases": repeated_phrases(text),
        "repeated_sentence_openings": repeated_sentence_openings(sentences),
        "paragraph_structure_repetition": paragraph_structure_repetition(paragraphs),
        "transition_phrase_repetition": transition_phrase_repetition(text),
        "repeated_syntactic_frames": repeated_syntactic_frames(sentences),
        "coordinated_series": coordinated_series(sentences, word_count),
        "lexical_diversity": lexical_diversity(text),
    }


def human_readable_summary(result: dict) -> str:
    lines = []
    lines.append("NOT AI : REPETITION ANALYSIS")
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
        lines.append(f"\n⚠ PARAGRAPH STRUCTURE: {psr['unique_structural_shapes']} unique shapes for {psr['total_paragraphs']} paragraphs, so paragraph shape may be monotonous")
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
    
    # Syntactic frames
    sf = result['repeated_syntactic_frames']
    if sf['consecutive_repeats']:
        lines.append("\nREPEATED SENTENCE FRAMES")
        for rep in sf['consecutive_repeats']:
            a, b = rep['sentence_indices']
            lines.append(f"  ⚠ '{rep['frame']}' in sentences {a + 1} and {b + 1}, back to back")
            lines.append(f"      {rep['first']}")
            lines.append(f"      {rep['second']}")
    elif sf['frame_counts']:
        listed = ', '.join(f"{k} x{v}" for k, v in list(sf['frame_counts'].items())[:5])
        lines.append(f"\nSENTENCE FRAMES: no back-to-back repeat ✓  ({listed})")
    else:
        lines.append("\nSENTENCE FRAMES: none of the eight named frames found ✓")

    # Coordinated series of three
    cs = result['coordinated_series']
    if cs['parallel_triples']:
        lines.append("\nCOORDINATED SERIES")
        for tri in cs['parallel_triples']:
            joined = ', '.join(tri['items'])
            lines.append(f"  ⚠ sentence {tri['sentence_index'] + 1}: three items all opening"
                         f" '{tri['lead_word']}'. Does cutting the third lose information,"
                         f" or only cadence?")
            lines.append(f"      {joined[:110]}")
    if cs['series_count']:
        plain = [s for s in cs['series']
                 if s['sentence_index'] not in {t['sentence_index'] for t in cs['parallel_triples']}]
        if plain:
            if not cs['parallel_triples']:
                lines.append("\nCOORDINATED SERIES")
            lines.append(f"  {len(plain)} series closing on 'and' or 'or'"
                         f"  |  {cs['series_rate_per_1000_words']} per 1,000 words overall."
                         f" No verdict: read each one and ask whether the third item is"
                         f" there for content or for cadence.")
            for s in plain[:5]:
                joined = ', '.join(s['series_tail'])
                lines.append(f"      sentence {s['sentence_index'] + 1}: {joined[:110]}")
    else:
        lines.append("\nCOORDINATED SERIES: none found ✓")

    # Lexical diversity
    ld = result['lexical_diversity']
    if ld:
        icon = "✓" if "high" in ld['assessment'] else "⚠"
        lines.append(f"\nLEXICAL DIVERSITY: {ld['content_word_ttr']:.0%} content-word TTR  |  {ld['assessment']} {icon}")
    
    return '\n'.join(lines)


def main():
    parser = argparse.ArgumentParser(description='Not Ai: repetition analyzer')
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
