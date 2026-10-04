# Zero-width Unicode: what the viral "bypass" really does

## Verdict

The viral screenshot technique is equivalent to:

```python
stealth_text = "\u200b".join(raw_text)
```

`U+200B ZERO WIDTH SPACE` is inserted between every visible code point. The
rendered prose can look unchanged while the raw string is different and many
tokenizers and regexes see different boundaries. Reproduced locally: a normal
60-character sample became 119 raw characters, and a word regex went from 8
words to 52 fragments.

This is **not humanization**. No wording, syntax, evidence, voice, or meaning
is improved. Not-AI must never ship a mode that inserts hidden characters or
promises lower detector scores.

It can affect weak or unnormalized classifiers, which is why Not-AI learns the
*defensive* lesson instead: Unicode-aware analysis that cannot be trivially
skewed by invisible token-boundary perturbations.

## Sources

- Dugan et al. (ACL 2024), **RAID: A Shared Benchmark for Robust Evaluation
  of Machine-Generated Text Detectors**, DOI `10.18653/v1/2024.acl-long.674`.
  RAID spans 6M+ generations across 11 models, 8 domains, 11 adversarial
  attacks, and 4 decoding strategies, evaluated against 12 detectors. One
  attack inserts `U+200B` around visible characters ("every other character"
  in the paper's attack description). Finding: current detectors are easily
  fooled by adversarial attacks and sampling variations. (Verified against the
  ACL Anthology record and paper PDF, 2026-10-04.)
- Mady et al. (2026), **DeBERTa-ConPara: Attack-Aware and
  Deployment-Realistic Detection of AI-Generated Text**, arXiv `2610.00883`
  (posted 2026-10-01). A deployment-oriented detector trained over HC3 Plus,
  M4, MAGE, and RAID, hardened against homoglyph, zero-width, whitespace, and
  typographic attacks. Its central reported finding is directional: Unicode
  normalization acts in opposite directions depending on where it is applied.
  Normalizing the training corpus silently deduplicates adversarial supervision
  (the project reports 35.4% of RAID rows collapsing), while normalizing at
  inference time is an effective defense. (Abstract, Hugging Face model page,
  and project page verified 2026-10-04; full-paper effect tables not
  independently re-verified here. Do not quote precise restoration numbers
  from this note.)
- Unicode Standard: `U+200B ZERO WIDTH SPACE` is a legitimate break
  opportunity used in writing systems without visible word spacing, including
  Thai, Myanmar, Khmer, Lao, and Japanese (see Chapter 16, Southeast Asian
  scripts). General category Format; normally no width.
- Unicode UTS #39 / UTS #55: invisible controls and confusables require
  contextual handling. `U+200C`/`U+200D` are legitimately required by some
  orthographies, and ZWJ occurs in emoji sequences.

## Not-AI design decision

Add Unicode hygiene, not evasion:

1. Reveal zero-width, bidi, tag, and unusual-space characters with code point,
   position, category, and analysis risk.
2. Create an analysis-only canonical view before style measurements; the
   writer's source text is never overwritten.
3. Never add invisible characters and never optimize detector scores.
4. Preserve legitimate ZWNJ/ZWJ use in non-Latin scripts and emoji.
5. Preserve `U+200B` in non-ASCII-dominant text unless it is actually
   splitting an ASCII token.
6. Treat presence as an encoding/tokenization fact, not evidence of authorship
   or malicious intent.
7. Use the normalized view for every bundled metric (gate, voice, lexical,
   cohesion, benchmark overlap) so one viral perturbation cannot corrupt word
   counts, rhythm, lexical diversity, or voice measurements.

## Why blanket NFKC is not enough

The implementation deliberately avoids blanket NFKC normalization.
Compatibility normalization can change characters that matter in
technical/scientific text, while default-ignorable format characters need
explicit handling. Not-AI's source-fidelity principle is more important than
aggressive canonicalization.

## Scope

`plugins/not-ai/tools/not_ai_core/unicode_hygiene.py` is the canonical
dependency-free implementation (scan + analysis-only normalization + CLI
report). `scripts/unicode_hygiene.py` is a thin wrapper. `scripts/_shared.py`
and `scripts/measure.py` carry behavior-identical mirrors because the latter
runs standalone inside the single-file bundle; `tests/test_unicode_hygiene.py`
asserts all three agree. Gate, diagnose, long-document review, and benchmark
overlap all measure the normalized view and report hygiene separately.
Homoglyph substitution is explicitly out of scope for this patch.
