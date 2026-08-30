#!/usr/bin/env python3
"""
not-ai: measure.py
One-file measurement pass. Combines analyze_structure.py, metrics.py and
repetition.py into a single stdlib-only script with no sibling imports.

This file exists so the skill can work as a single SKILL.md. The build script
scripts/build_single_file.py embeds it verbatim in a fenced block, and an agent
loading the combined skill writes it to a temp path and runs it.

Every regex, threshold and formula here is copied from the three scripts it
replaces, not reimplemented. That is deliberate: the figures quoted in
examples/*/diagnostic.md and examples/*/rationale.md come from those scripts,
and a condensed version that measured slightly differently would silently
invalidate every table in the repository. scripts/verify_measure.py checks the
two agree on every shared figure.

Usage:
    python measure.py FILE
    python measure.py --stdin
    python measure.py FILE --json

Read before quoting any number:
  * Nominalization here is a regex over suffixes, with no part-of-speech
    information. It counts "nation" and "moment". On the five model-generated
    inputs in examples/ it averages 80.0 per 1,000 words against the tagged
    14.6, about 5.5 times, so compare it only against another run of this
    script, never against the 14.6 per 1,000 tokens in the research.
  * The participial detector is anchored to the first word of the sentence, so
    "By leveraging the power of..." is not counted. A 0% result means "none of
    the anchored forms", not "none".
  * Burstiness is a coefficient of variation. Its verdicts are wrong often
    enough that nothing in the skill acts on them. They are printed as evidence,
    not as guidance.
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

# ─── Primitives (from _shared.py) ────────────────────────────────────────────

NOMINALIZATION_SUFFIXES = (
    "tion", "tions", "ment", "ments", "ness", "nesses",
    "ity", "ities", "ance", "ances", "ence", "ences",
)
NOMINALIZATION_PATTERN = re.compile(
    r"\b\w+(" + "|".join(NOMINALIZATION_SUFFIXES) + r")\b", re.IGNORECASE)
HEURISTIC_NOMINALIZATION_BANDS = {"high": 50.0, "elevated": 35.0}
WORD_PATTERN = re.compile(r"\b[a-zA-Z]+\b")
SENTENCE_SPLIT_PATTERN = re.compile(r'(?<=[.!?])\s+(?=[A-Z"\'])')


def tokenize_words(text):
    """Canonical denominator for every per-1,000-words rate here."""
    return WORD_PATTERN.findall(text)


def get_sentences(text):
    text = re.sub(r"\s+", " ", text.strip())
    return [s.strip() for s in SENTENCE_SPLIT_PATTERN.split(text)
            if s.strip() and len(s.split()) >= 2]


def get_paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]


def nominalization_stats(text, words=None):
    if words is None:
        words = tokenize_words(text)
    total = len(words)
    count = len(NOMINALIZATION_PATTERN.findall(text))
    rate = (count / total * 1000) if total else 0.0
    if rate > HEURISTIC_NOMINALIZATION_BANDS["high"]:
        assessment = "high for this proxy"
    elif rate > HEURISTIC_NOMINALIZATION_BANDS["elevated"]:
        assessment = "elevated for this proxy"
    else:
        assessment = "normal for this proxy"
    return {"nominalization_count": count, "total_words": total,
            "rate_per_1000_words": round(rate, 1), "assessment": assessment}


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
    'than', 'too', 'very', 's', 't', 'just', 'don', 'now',
}

# ─── Structure (from analyze_structure.py) ───────────────────────────────────


def sentence_lengths(sentences):
    if not sentences:
        return {"count": 0, "mean": 0, "median": 0, "std": 0, "min": 0,
                "max": 0, "burstiness": 0, "distribution": {}}
    lengths = [len(s.split()) for s in sentences]
    n = len(lengths)
    mean = sum(lengths) / n
    srt = sorted(lengths)
    median = srt[n // 2] if n % 2 else (srt[n // 2 - 1] + srt[n // 2]) / 2
    std = (sum((x - mean) ** 2 for x in lengths) / n) ** 0.5
    return {
        "count": n, "mean": round(mean, 1), "median": round(median, 1),
        "std": round(std, 1), "min": min(lengths), "max": max(lengths),
        "burstiness": round(std / mean if mean else 0, 3),
        "distribution": {
            "very_short_under_8": sum(1 for l in lengths if l < 8),
            "short_8_to_15": sum(1 for l in lengths if 8 <= l < 16),
            "medium_16_to_25": sum(1 for l in lengths if 16 <= l < 26),
            "long_26_to_35": sum(1 for l in lengths if 26 <= l < 36),
            "very_long_over_35": sum(1 for l in lengths if l >= 36),
        },
    }


def paragraph_lengths(paragraphs):
    if not paragraphs:
        return {}
    counts = [len(get_sentences(p)) for p in paragraphs]
    n = len(counts)
    return {
        "count": n,
        "mean_sentences": round(sum(counts) / n if n else 0, 1),
        "single_sentence_paragraphs": sum(1 for c in counts if c == 1),
        "distribution": {
            "1_sentence": sum(1 for c in counts if c == 1),
            "2_3_sentences": sum(1 for c in counts if 2 <= c <= 3),
            "4_5_sentences": sum(1 for c in counts if 4 <= c <= 5),
            "6_plus_sentences": sum(1 for c in counts if c >= 6),
        },
    }


AI_OPENERS = ["furthermore", "moreover", "additionally", "however", "nevertheless",
              "therefore", "consequently", "in", "building", "leveraging",
              "utilizing", "by", "through", "this", "these", "such"]


def opening_word_analysis(sentences):
    if not sentences:
        return {}
    openings = [s.split()[0].lower().rstrip('.,!?') for s in sentences if s.split()]
    freq = {}
    for w in openings:
        freq[w] = freq.get(w, 0) + 1
    consecutive, max_consecutive, prev = 0, 0, None
    for o in openings:
        consecutive = consecutive + 1 if o == prev else 1
        if o == prev:
            max_consecutive = max(max_consecutive, consecutive)
        prev = o
    return {
        "top_5_openers": sorted(freq.items(), key=lambda x: -x[1])[:5],
        "repeated_openers_3plus": {w: c for w, c in freq.items() if c >= 3},
        "ai_associated_opener_hits": {w: c for w, c in freq.items()
                                      if w in AI_OPENERS and c >= 2},
        "the_opener_count": freq.get("the", 0),
        "this_opener_count": freq.get("this", 0),
        "max_consecutive_same_opener": max_consecutive,
    }


PARTICIPIAL_OPENERS = re.compile(
    r'^\s*(Building|Leveraging|Utilizing|Combining|Considering|Recognizing|'
    r'Acknowledging|Addressing|Analyzing|Examining|Exploring|Implementing|'
    r'Integrating|Emphasizing|Highlighting|Enabling|Supporting|Providing|'
    r'Drawing|Creating|Developing|Working|Moving|Looking|Going|Taking|'
    r'Making|Having|Being|Using|Doing|Getting|Seeing|Knowing|Finding|'
    r'Understanding|Establishing|Ensuring|Focusing|Achieving|Delivering|'
    r'Bringing|Offering|Presenting|Demonstrating)\b', re.IGNORECASE)


def participial_rate(sentences):
    count = sum(1 for s in sentences if PARTICIPIAL_OPENERS.match(s))
    rate = count / len(sentences) if sentences else 0
    return {
        "participial_opener_count": count,
        "participial_opener_rate": round(rate, 3),
        "sentences_analyzed": len(sentences),
        "assessment": ("high for this proxy" if rate > 0.15 else
                       "elevated for this proxy" if rate > 0.08 else
                       "normal for this proxy"),
        "caveat": ("Anchored match only. Participles after an introductory "
                   "preposition, for example 'By leveraging', are not counted."),
    }


MECHANICAL_TRANSITIONS = {
    "furthermore": r'\bfurthermore\b', "moreover": r'\bmoreover\b',
    "additionally": r'\badditionally\b', "in conclusion": r'\bin conclusion\b',
    "in summary": r'\bin summary\b', "to summarize": r'\bto summarize\b',
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


def transition_density(text, sentences):
    low = text.lower()
    hits = {}
    for phrase, pat in MECHANICAL_TRANSITIONS.items():
        c = len(re.findall(pat, low))
        if c:
            hits[phrase] = c
    total = sum(hits.values())
    rate = (total / len(sentences)) if sentences else 0
    return {"mechanical_transition_hits": hits,
            "total_mechanical_transitions": total,
            "rate_per_sentence": round(rate, 3),
            "assessment": ("high for this proxy" if rate > 0.2 else
                           "elevated" if rate > 0.1 else "normal")}


AI_VOCAB = [
    "camaraderie", "tapestry", "palpable", "intricate", "underscore",
    "unspoken", "amidst", "solace", "fleeting", "vibrant",
    "cacophony", "grapple", "ignite", "unravel",
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
    "meticulous", "meticulously", "nuanced", "nuance",
    "multifaceted", "myriad", "evolving landscape", "ever-evolving",
    "rapidly evolving", "empower", "empowering", "empowered",
    "impactful", "meaningful",
]


def generic_vocabulary(text):
    low = text.lower()
    hits = {}
    for term in AI_VOCAB:
        c = len(re.findall(r'\b' + re.escape(term) + r'\b', low))
        if c:
            hits[term] = c
    return {"ai_vocabulary_hits": hits, "total_hit_count": sum(hits.values()),
            "unique_ai_terms": len(hits),
            "note": "Contextual interpretation required. Presence is a signal, "
                    "not automatic proof of AI authorship."}


TRIGRAM_STOPWORDS = {'the', 'a', 'an', 'of', 'in', 'to', 'is', 'are', 'and',
                     'or', 'but', 'for', 'that', 'this', 'it', 'on', 'at', 'by',
                     'as', 'with', 'from', 'be', 'was', 'were'}


def repetitive_phrase_detection(text):
    words = re.findall(r'\b\w+\b', text.lower())
    trigrams = {}
    for i in range(len(words) - 2):
        gram = words[i:i + 3]
        if not all(w in TRIGRAM_STOPWORDS for w in gram):
            key = ' '.join(gram)
            trigrams[key] = trigrams.get(key, 0) + 1
    repeated = {k: v for k, v in trigrams.items() if v >= 3}
    return {"repeated_3grams": dict(sorted(repeated.items(), key=lambda x: -x[1])[:10]),
            "high_repetition_phrase_count": len(repeated)}


def passive_estimate(sentences):
    pat = re.compile(r'\b(is|are|was|were|been|being|be)\s+\w+ed\b', re.I)
    count = sum(1 for s in sentences if pat.search(s))
    return {"passive_sentence_estimate": count,
            "passive_rate": round(count / len(sentences) if sentences else 0, 3),
            "note": "Rough estimate only. Not all -ed forms are passive voice."}


def list_density(text):
    bullets = len(re.findall(r'^\s*[-•*]\s+', text, re.M))
    numbered = len(re.findall(r'^\s*\d+[.)]\s+', text, re.M))
    total_words = len(tokenize_words(text))
    return {"bullet_items": bullets, "numbered_items": numbered,
            "total_list_items": bullets + numbered,
            "list_density_per_1000_words":
                round((bullets + numbered) / total_words * 1000, 1) if total_words else 0}

# ─── Readability and stance (from metrics.py) ────────────────────────────────


def count_syllables(word):
    word = word.lower().strip(".,!?;:'\"()")
    if not word:
        return 0
    if word.endswith('e') and len(word) > 2:
        word = word[:-1]
    return max(1, len(re.findall(r'[aeiou]+', word)))


def readability(sentences, words):
    if not sentences or not words:
        return {"flesch_kincaid_grade": 0.0, "gunning_fog_index": 0.0,
                "flesch_reading_ease": 0.0, "readability_assessment": "n/a"}
    syl = sum(count_syllables(w) for w in words)
    asl = len(words) / len(sentences)
    aspw = syl / len(words)
    complex_pct = sum(1 for w in words if count_syllables(w) >= 3) / len(words) * 100
    ease = round(206.835 - 1.015 * asl - 84.6 * aspw, 1)
    return {
        "flesch_kincaid_grade": round(0.39 * asl + 11.8 * aspw - 15.59, 1),
        "gunning_fog_index": round(0.4 * (asl + complex_pct), 1),
        "flesch_reading_ease": ease,
        "readability_assessment": ("very easy" if ease > 80 else "easy" if ease > 70
                                   else "standard" if ease > 60 else
                                   "difficult" if ease > 40 else "very difficult"),
    }


PREPOSITIONS = {'of', 'in', 'to', 'for', 'on', 'with', 'at', 'by', 'from',
                'into', 'through', 'during', 'before', 'after', 'above', 'below',
                'between', 'among', 'under', 'about', 'against', 'without', 'within',
                'around', 'along', 'following', 'across', 'behind', 'beyond',
                'including', 'throughout', 'regarding', 'concerning'}
WEAK_VERBS = {'is', 'are', 'was', 'were', 'be', 'been', 'being',
              'have', 'has', 'had', 'do', 'does', 'did',
              'will', 'would', 'could', 'should', 'may', 'might', 'can', 'shall'}


def information_density(text, words):
    low = [w.lower() for w in words]
    prep_rate = sum(1 for w in low if w in PREPOSITIONS) / len(words) if words else 0
    weak_rate = sum(1 for w in low if w in WEAK_VERBS) / len(words) if words else 0
    nom = nominalization_stats(text, words)
    score = (prep_rate * 200) + (nom["rate_per_1000_words"] / 2)
    return {"preposition_rate": round(prep_rate, 3),
            "weak_verb_rate": round(weak_rate, 3),
            "nominalization_rate_per_1000": nom["rate_per_1000_words"],
            "nominalization_assessment": nom["assessment"],
            "estimated_density_score": round(score, 1),
            "assessment": ("high density, characteristic of formal academic prose"
                           if score > 50 else "moderate density" if score > 30
                           else "low density, conversational")}


HEDGES = [r'\bmight\b', r'\bcould\b', r'\bmay\b', r'\bperhaps\b', r'\bpossibly\b',
          r'\bappears? to\b', r'\bseems? to\b', r'\btends? to\b',
          r'\bi think\b', r'\bi believe\b', r'\bone might\b', r'\bargua\w+\b',
          r'\bsuggests?\b', r'\bindicates?\b', r'\bseems?\b']
BOOSTERS = [r'\bclearly\b', r'\bobviously\b', r'\bcertainly\b', r'\bdefinitely\b',
            r'\bundoubtedly\b', r'\bwithout question\b', r'\bit is clear\b',
            r'\bof course\b', r'\bevident\w*\b']


STANCE_MIN_MARKERS = 3
STANCE_MIN_RATE_PER_1000 = 2.0


def stance_verdict(hedge, boost, wc):
    """
    Mirror of stance_balance() in scripts/_shared.py. A balance verdict needs a
    minimum of signal to mean anything, so no-stance text reads "absent" rather
    than falling through to "calibrated", and a couple of markers in a long
    document reads "too sparse to judge". Absent stance is not a defect by
    itself; whether the gap matters is genre judgment, made in SKILL.md.
    """
    total = hedge + boost
    if total == 0:
        return "absent"
    rate = total / wc * 1000 if wc else 0.0
    if total < STANCE_MIN_MARKERS or rate < STANCE_MIN_RATE_PER_1000:
        return "too sparse to judge"
    if hedge > boost * 3:
        return "over-hedged"
    if boost > hedge * 2:
        return "over-assertive"
    return "calibrated"


def tone_markers(text):
    low = text.lower()
    wc = len(text.split())
    hedge = sum(len(re.findall(p, low)) for p in HEDGES)
    boost = sum(len(re.findall(p, low)) for p in BOOSTERS)
    first = len(re.findall(r'\bi\b|\bme\b|\bmy\b|\bwe\b|\bour\b', low))
    per_k = lambda n: round(n / wc * 1000, 1) if wc else 0
    return {"hedge_count": hedge, "hedge_rate_per_1000": per_k(hedge),
            "booster_count": boost, "booster_rate_per_1000": per_k(boost),
            "question_count": text.count('?'),
            "reader_address_count": len(re.findall(r'\byou\b|\byour\b', low)),
            "first_person_count": first, "first_person_rate_per_1000": per_k(first),
            "stance_balance": stance_verdict(hedge, boost, wc)}

# ─── Repetition (from repetition.py) ─────────────────────────────────────────


def extract_ngrams(words, n, stopword_filter=True):
    grams = Counter()
    for i in range(len(words) - n + 1):
        gram = words[i:i + n]
        if stopword_filter:
            if len([w for w in gram if w not in STOPWORDS]) < max(1, n // 2):
                continue
        grams[' '.join(gram)] += 1
    return grams


def repeated_phrases(text):
    words = re.findall(r'\b[a-z]+\b', text.lower())
    out = {}
    for n in (3, 4, 5):
        rep = {k: v for k, v in extract_ngrams(words, n).items() if v >= 2}
        if rep:
            out[f'{n}-grams'] = dict(sorted(rep.items(), key=lambda x: -x[1])[:10])
    return out


def repeated_sentence_openings(sentences):
    two, three = Counter(), Counter()
    for s in sentences:
        w = s.lower().split()
        if len(w) >= 2:
            two[' '.join(w[:2])] += 1
        if len(w) >= 3:
            three[' '.join(w[:3])] += 1
    return {"repeated_2word_openings": {k: v for k, v in two.items() if v >= 3},
            "repeated_3word_openings": {k: v for k, v in three.items() if v >= 2}}


def paragraph_shapes(paragraphs):
    shapes = []
    for p in paragraphs:
        lengths = [len(s.split()) for s in get_sentences(p)]
        shapes.append(tuple('S' if l < 12 else 'M' if l < 25 else 'L' for l in lengths))
    counter = Counter(shapes)
    return {"total_paragraphs": len(paragraphs),
            "unique_structural_shapes": len(counter),
            "repeated_shapes": {str(k): v for k, v in counter.items()
                                if v >= 2 and len(k) >= 2},
            "structural_monotony_warning":
                len(counter) < max(1, len(paragraphs) / 3)}


REPEATED_TRANSITIONS = [
    r'furthermore', r'moreover', r'additionally', r'however',
    r'therefore', r'consequently', r'as a result', r'in conclusion',
    r'to summarize', r'in summary', r'in addition', r'on the other hand',
    r'that said', r'with that said', r'having said that',
    r'it is worth noting', r'it is important to note', r'it should be noted',
    r'building on this', r'leveraging this', r'given this',
    r'this demonstrates', r'this shows', r'this highlights', r'this underscores',
    r'this illustrates', r'this reveals',
]


def transition_repetition(text):
    low = text.lower()
    hits = {}
    for phrase in REPEATED_TRANSITIONS:
        c = len(re.findall(r'\b' + phrase + r'\b', low))
        if c >= 2:
            hits[phrase] = c
    return {"repeated_transitions": hits,
            "warning": ("High transition repetition creates mechanical rhythm"
                        if len(hits) >= 3 else None)}


# Named sentence frames. Mirror of SYNTACTIC_FRAMES in scripts/repetition.py.
#
# These catch a repeat that no word-level check sees: two sentences with no
# shared phrase and no shared opening that nonetheless make the same move.
# Eight regexes, no parser, no part-of-speech information. Two names are
# mechanical on purpose: "comma plus -ing word" fires on a real participial tail
# in "shipped in six weeks, leveraging existing infrastructure" and equally on a
# gerund subject in "In conclusion, caching remains", so it is named after what
# it matches rather than what it usually means. Fenced blocks and quoted
# specimens are counted as prose, as everywhere else in this script.
#
# The single warning is the same frame in two consecutive sentences. Consecutive
# is the smallest window there is, so nothing here is tuned to a specimen.
SYNTACTIC_FRAMES = (
    ("range sweep",
     r"\bfrom\b[^.;:]{1,80}?\b(?:to|through|into)\b"),
    ("comparative than",
     r"\b(?:more|less|fewer|greater)\b[^.;:]{1,60}?\bthan\b"),
    ("superlative membership",
     r"\bone of the\b[^.;:]{0,40}?(?:\b\w+est\b|\bmost\b|\bleast\b)"),
    ("scale superlative",
     r"\b(?:world|nation|country|continent|planet|industry|region|market)(?:'s|s')"
     r"\s+(?:\w+\s+){0,3}?(?:most|largest|biggest|fastest|oldest|leading|greatest)\b"),
    ("not just X but Y",
     r"\bnot\s+(?:just|only|merely|simply)\b[^.;:]{1,80}?\b(?:but|it['’]s|it is)\b"),
    ("comma plus -ing word",
     r",\s+(?!and\b|but\b|or\b|which\b|who\b|whose\b|where\b|while\b|when\b)\w+ing\b"),
    ("comma plus -ed by",
     r",\s+\w+ed\s+by\b"),
    ("where X meets Y",
     r"\bwhere\b[^.;:]{1,50}?\bmeets?\b"),
)

FRAME_PATTERNS = tuple((name, re.compile(p, re.IGNORECASE)) for name, p in SYNTACTIC_FRAMES)


def syntactic_frames(sentences):
    per_sentence = []
    for i, s in enumerate(sentences):
        hits = sorted(name for name, pat in FRAME_PATTERNS if pat.search(s))
        if hits:
            per_sentence.append({"sentence_index": i, "frames": hits})

    counts = Counter()
    for e in per_sentence:
        for name in e["frames"]:
            counts[name] += 1

    by_index = {e["sentence_index"]: set(e["frames"]) for e in per_sentence}
    consecutive = []
    for i in range(len(sentences) - 1):
        for name in sorted(by_index.get(i, set()) & by_index.get(i + 1, set())):
            consecutive.append({"frame": name, "sentence_indices": [i, i + 1],
                                "first": sentences[i][:90], "second": sentences[i + 1][:90]})

    return {"total_sentences": len(sentences),
            "frame_counts": dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))),
            "sentences_using_a_frame": len(per_sentence),
            "consecutive_repeats": consecutive}


# Coordinated series of three. Mirror of coordinated_series in repetition.py.
#
# Requires the Oxford comma, so series without it are missed. Reports without
# ruling, because whether a third item carries content is not a regex question.
# The one warning is a lexically parallel triple, where all three items open with
# the same token, since that anaphora is a rhythm device by construction. It can
# still be legitimate: three distinct "whether" clauses are structure, not
# decoration. The test is whether cutting the third item loses information.
#
# The anaphora is established on items two and three, then confirmed inside the
# first segment, because the first segment also carries the sentence stem: in
# "The plan needed a bigger room, a longer window, and a second reviewer" the
# first item is "a bigger room" and reading the segment's first word gives "The".
SERIES_COORDINATOR = re.compile(r"^(?:and|or)\s+\S", re.IGNORECASE)
SERIES_LEAD_TOKEN = re.compile(r"^(?:and\s+|or\s+)?([a-zA-Z']+)", re.IGNORECASE)


def series_lead_word(segment):
    m = SERIES_LEAD_TOKEN.match(segment)
    return m.group(1).lower() if m else ""


def series_first_item(segment, lead):
    if not lead or not lead[0].isalpha():
        return ""
    for m in reversed(list(re.finditer(r"\b" + re.escape(lead) + r"\b",
                                       segment, re.IGNORECASE))):
        rest = segment[m.start():]
        if len(rest.split()) >= 2:
            return rest
    return ""


def coordinated_series(sentences, word_count):
    found, parallel = [], []
    for i, s in enumerate(sentences):
        segs = [seg.strip() for seg in s.split(",")]
        if len(segs) < 3 or not SERIES_COORDINATOR.match(segs[-1]):
            continue
        tail = segs[-3:]
        found.append({"sentence_index": i, "comma_segments": len(segs), "series_tail": tail})
        lead = series_lead_word(tail[1])
        if lead and lead == series_lead_word(tail[2]):
            first = series_first_item(tail[0], lead)
            if first:
                parallel.append({"sentence_index": i, "lead_word": lead,
                                 "items": [first, tail[1], tail[2]]})

    rate = (len(found) / word_count * 1000) if word_count else 0.0
    return {"series_count": len(found),
            "series_rate_per_1000_words": round(rate, 1),
            "series": found,
            "parallel_triples": parallel}


def lexical_diversity(text):
    words = re.findall(r'\b[a-z]+\b', text.lower())
    if not words:
        return {}
    content = [w for w in words if w not in STOPWORDS and len(w) > 3]
    cttr = len(set(content)) / len(content) if content else 0
    return {"total_tokens": len(words), "unique_types": len(set(words)),
            "type_token_ratio": round(len(set(words)) / len(words), 3),
            "content_word_ttr": round(cttr, 3),
            "assessment": ("low diversity for this proxy" if cttr < 0.55 else
                           "moderate diversity" if cttr < 0.70 else "high diversity")}

# ─── Combined report ─────────────────────────────────────────────────────────


def analyze(text):
    sentences = get_sentences(text)
    paragraphs = get_paragraphs(text)
    words = tokenize_words(text)
    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "paragraph_count": len(paragraphs),
        "sentence_lengths": sentence_lengths(sentences),
        "paragraph_structure": paragraph_lengths(paragraphs),
        "opening_analysis": opening_word_analysis(sentences),
        "participial_clauses": participial_rate(sentences),
        "nominalization_density": nominalization_stats(text, words),
        "transition_words": transition_density(text, sentences),
        "generic_vocabulary": generic_vocabulary(text),
        "passive_voice": passive_estimate(sentences),
        "list_density": list_density(text),
        "phrase_repetition": repetitive_phrase_detection(text),
        "readability": readability(sentences, words),
        "information_density": information_density(text, words),
        "tone_markers": tone_markers(text),
        "repeated_phrases": repeated_phrases(text),
        "repeated_sentence_openings": repeated_sentence_openings(sentences),
        "paragraph_structure_repetition": paragraph_shapes(paragraphs),
        "transition_phrase_repetition": transition_repetition(text),
        "repeated_syntactic_frames": syntactic_frames(sentences),
        "coordinated_series": coordinated_series(sentences, len(words)),
        "lexical_diversity": lexical_diversity(text),
    }


def report(r):
    L = []
    L.append("NOT AI : MEASUREMENT")
    L.append("─" * 44)
    L.append(f"Words: {r['word_count']}  |  Sentences: {r['sentence_count']}"
             f"  |  Paragraphs: {r['paragraph_count']}")

    sl = r['sentence_lengths']
    d = sl.get('distribution', {})
    L.append("\nSENTENCE RHYTHM")
    L.append(f"  Mean length:   {sl['mean']} words")
    L.append(f"  Std deviation: {sl['std']} words  (burstiness: {sl['burstiness']})")
    L.append(f"  Very short (<8):  {d.get('very_short_under_8', 0)}  |  "
             f"Short (8-15): {d.get('short_8_to_15', 0)}  |  "
             f"Medium (16-25): {d.get('medium_16_to_25', 0)}")
    L.append(f"  Long (26-35):  {d.get('long_26_to_35', 0)}  |  "
             f"Very long (35+): {d.get('very_long_over_35', 0)}")
    if sl['burstiness'] < 0.30:
        L.append("  ⚠ Low burstiness: sentence lengths are very uniform")
    elif sl['burstiness'] > 0.55:
        L.append("  ✓ Good length variation")
    L.append("  Burstiness verdicts are unreliable. Do not treat either as a target.")

    ps = r['paragraph_structure']
    if ps:
        pd = ps.get('distribution', {})
        L.append(f"  Paragraphs: {ps['count']}, mean {ps['mean_sentences']} sentences"
                 f"  |  1 sent: {pd.get('1_sentence', 0)}"
                 f"  |  2-3: {pd.get('2_3_sentences', 0)}"
                 f"  |  4-5: {pd.get('4_5_sentences', 0)}"
                 f"  |  6+: {pd.get('6_plus_sentences', 0)}")

    L.append("\nSTRUCTURAL SIGNALS")
    pc = r['participial_clauses']
    icon = "⚠" if pc['assessment'].startswith(("high", "elevated")) else "✓"
    L.append(f"  {icon} Participial clause openers: {pc['participial_opener_count']}"
             f" / {pc['sentences_analyzed']} sentences"
             f" ({pc['participial_opener_rate']:.0%})  |  {pc['assessment']}")
    if pc['participial_opener_count'] == 0:
        L.append("      Anchored match only. 'By leveraging...' style openers are not counted.")
    nd = r['nominalization_density']
    icon = "⚠" if nd['assessment'].startswith(("high", "elevated")) else "✓"
    L.append(f"  {icon} Nominalization density: {nd['rate_per_1000_words']}"
             f" per 1,000 words  |  {nd['assessment']}")
    L.append("      Proxy measure. Compare only against another run of this script.")
    tw = r['transition_words']
    if tw['total_mechanical_transitions']:
        L.append(f"  ⚠ Mechanical transitions: {tw['total_mechanical_transitions']}"
                 f" instances  |  {', '.join(tw['mechanical_transition_hits'])}")
    else:
        L.append("  ✓ No high-frequency mechanical transitions detected")
    pv = r['passive_voice']
    L.append(f"  Passive estimate: {pv['passive_sentence_estimate']} sentences"
             f" ({pv['passive_rate']:.0%}). Not all -ed forms are passive, and the"
             f" research shows models underuse agentless passives, so a low figure"
             f" is not automatically good.")

    oa = r['opening_analysis']
    L.append("\nSENTENCE OPENINGS")
    if oa.get('repeated_openers_3plus'):
        for w, c in oa['repeated_openers_3plus'].items():
            L.append(f"  ⚠ '{w}' used to open {c} sentences")
    else:
        L.append("  ✓ No highly repeated sentence openers")
    if oa.get('max_consecutive_same_opener', 0) >= 3:
        L.append(f"  ⚠ {oa['max_consecutive_same_opener']} consecutive sentences"
                 f" with same opener")
    ro = r['repeated_sentence_openings']
    for phrase, c in {**ro.get('repeated_3word_openings', {}),
                      **ro.get('repeated_2word_openings', {})}.items():
        L.append(f"  ⚠ '{phrase}': {c} sentences")

    gv = r['generic_vocabulary']
    L.append("\nAI-ASSOCIATED VOCABULARY")
    if gv['ai_vocabulary_hits']:
        # Cap of eight, disclosed. See the note in analyze_structure.py: these
        # two extra lines exist because a silent cap produced two wrong figures.
        ranked = sorted(gv['ai_vocabulary_hits'].items(), key=lambda x: -x[1])
        for term, c in ranked[:8]:
            L.append(f"  • '{term}': {c}x")
        if len(ranked) > 8:
            rest = ', '.join(f"'{t}'" for t, _ in ranked[8:])
            L.append(f"  ... {len(ranked) - 8} more not listed above: {rest}")
        L.append(f"  Total: {gv['unique_ai_terms']} unique terms, "
                 f"{sum(gv['ai_vocabulary_hits'].values())} occurrences")
        L.append(f"  Note: {gv['note']}")
        L.append("  A word being quoted counts the same as a word being used.")
    else:
        L.append("  ✓ No high-frequency AI vocabulary detected")

    pr = r['phrase_repetition']
    if pr['repeated_3grams']:
        L.append("\nREPEATED PHRASES (3+ occurrences)")
        for phrase, c in list(pr['repeated_3grams'].items())[:5]:
            L.append(f"  ⚠ '{phrase}': {c}x")

    rp = r['repeated_phrases']
    L.append("\nREPEATED PHRASES (2+ occurrences, 3 to 5 words)")
    if rp:
        for _, phrases in rp.items():
            for phrase, c in list(phrases.items())[:5]:
                L.append(f"  • '{phrase}': {c}x")
    else:
        L.append("  ✓ None detected")

    psr = r['paragraph_structure_repetition']
    if psr.get('structural_monotony_warning'):
        L.append(f"\n⚠ PARAGRAPH STRUCTURE: {psr['unique_structural_shapes']} unique"
                 f" shapes for {psr['total_paragraphs']} paragraphs, so paragraph"
                 f" shape may be monotonous")
    else:
        L.append(f"\nPARAGRAPH STRUCTURE: {psr['unique_structural_shapes']} unique shapes ✓")

    tr = r['transition_phrase_repetition']
    if tr['repeated_transitions']:
        L.append("\nREPEATED TRANSITIONS")
        for phrase, c in tr['repeated_transitions'].items():
            L.append(f"  ⚠ '{phrase}': {c}x")
    else:
        L.append("\nTRANSITIONS: No high-frequency repetition ✓")

    sf = r['repeated_syntactic_frames']
    if sf['consecutive_repeats']:
        L.append("\nREPEATED SENTENCE FRAMES")
        for rep in sf['consecutive_repeats']:
            a, b = rep['sentence_indices']
            L.append(f"  ⚠ '{rep['frame']}' in sentences {a + 1} and {b + 1}, back to back")
            L.append(f"      {rep['first']}")
            L.append(f"      {rep['second']}")
    elif sf['frame_counts']:
        listed = ', '.join(f"{k} x{v}" for k, v in list(sf['frame_counts'].items())[:5])
        L.append(f"\nSENTENCE FRAMES: no back-to-back repeat ✓  ({listed})")
    else:
        L.append("\nSENTENCE FRAMES: none of the eight named frames found ✓")

    cs = r['coordinated_series']
    if cs['parallel_triples']:
        L.append("\nCOORDINATED SERIES")
        for tri in cs['parallel_triples']:
            L.append(f"  ⚠ sentence {tri['sentence_index'] + 1}: three items all opening"
                     f" '{tri['lead_word']}'. Does cutting the third lose information,"
                     f" or only cadence?")
            L.append(f"      {', '.join(tri['items'])[:110]}")
    if cs['series_count']:
        flagged = {t['sentence_index'] for t in cs['parallel_triples']}
        plain = [s for s in cs['series'] if s['sentence_index'] not in flagged]
        if plain:
            if not cs['parallel_triples']:
                L.append("\nCOORDINATED SERIES")
            L.append(f"  {len(plain)} series closing on 'and' or 'or'  |  "
                     f"{cs['series_rate_per_1000_words']} per 1,000 words overall."
                     f" No verdict: read each one and ask whether the third item is"
                     f" there for content or for cadence.")
            for s in plain[:5]:
                L.append(f"      sentence {s['sentence_index'] + 1}:"
                         f" {', '.join(s['series_tail'])[:110]}")
    else:
        L.append("\nCOORDINATED SERIES: none found ✓")

    ld = r['lexical_diversity']
    if ld:
        icon = "✓" if "high" in ld['assessment'] else "⚠"
        L.append(f"\nLEXICAL DIVERSITY: {ld['content_word_ttr']:.0%} content-word TTR"
                 f"  |  {ld['assessment']} {icon}")

    rd = r['readability']
    L.append("\nREADABILITY")
    L.append(f"  Flesch-Kincaid Grade:  {rd['flesch_kincaid_grade']}"
             f" (US grade level equivalent)")
    L.append(f"  Gunning Fog Index:     {rd['gunning_fog_index']}"
             f" ({rd['readability_assessment']})")
    L.append(f"  Flesch Reading Ease:   {rd['flesch_reading_ease']} / 100")
    L.append("  Read these against the genre, not against a universal target.")

    idy = r['information_density']
    L.append("\nINFORMATION DENSITY")
    L.append(f"  Density score: {idy['estimated_density_score']}  |  {idy['assessment']}")
    L.append(f"  Preposition rate:  {idy['preposition_rate']:.1%}")
    L.append(f"  Nominalizations:   {idy['nominalization_rate_per_1000']}"
             f" per 1,000 words  |  {idy['nominalization_assessment']}")

    t = r['tone_markers']
    L.append("\nEPISTEMIC STANCE")
    L.append(f"  Hedges:     {t['hedge_count']} ({t['hedge_rate_per_1000']} per 1,000 words)")
    L.append(f"  Boosters:   {t['booster_count']} ({t['booster_rate_per_1000']} per 1,000 words)")
    L.append(f"  Balance:    {t['stance_balance']}")
    L.append("  Models underuse hedges at 50% to 63% of the human rate, so"
             " 'over-hedged' on a draft is worth checking before acting on."
             "\n  'absent' means no stance marker was found at all, which some"
             " genres do not need; it is a reading, not a fault.")
    L.append("\nENGAGEMENT MARKERS")
    L.append(f"  Questions:      {t['question_count']}")
    L.append(f"  Reader address: {t['reader_address_count']}")
    L.append(f"  First-person:   {t['first_person_count']}"
             f" ({t['first_person_rate_per_1000']} per 1,000 words)")

    L.append("\nA script measures a file, not a deliverable. Flags, editorial notes"
             "\nand bracketed slots are counted as prose.")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description='Not Ai: single-file measurement pass')
    ap.add_argument('input_file', nargs='?')
    ap.add_argument('--stdin', action='store_true')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    if args.stdin or not args.input_file:
        text = sys.stdin.read()
    else:
        path = Path(args.input_file)
        if not path.is_file():
            print(f"Error: file not found: {args.input_file}", file=sys.stderr)
            return 1
        text = path.read_text(encoding='utf-8')

    if not text.strip():
        print("Error: no text provided", file=sys.stderr)
        return 1

    result = analyze(text)
    print(json.dumps(result, indent=2, ensure_ascii=False) if args.json
          else report(result))
    return 0


if __name__ == '__main__':
    sys.exit(main())
