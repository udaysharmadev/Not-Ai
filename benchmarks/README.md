# Not Ai: Benchmarks

This directory contains the benchmark framework for evaluating Not Ai's performance on real text pairs.

---

## What the Benchmark Measures

The benchmark evaluates pairs of `(original AI-generated text, Not Ai rewritten text)` on:

| Metric | What it measures | How |
|--------|-----------------|-----|
| Semantic similarity | How much meaning was preserved | Token overlap (Jaccard) of content words |
| Number preservation | Were factual numbers preserved? | Set comparison |
| Word count change | Did the text grow or shrink significantly? | Word count delta |
| Structural delta | Did structural patterns improve? | Burstiness, participial rate, nominalization rate |
| Readability delta | Did readability change? | Flesch-Kincaid grade before/after |
| AI vocabulary delta | Were AI-associated terms reduced? | Count before/after |

**On semantic similarity**: Token overlap is a proxy, not ground truth. It measures whether the same content words appear, not whether the meaning is equivalent. For a production benchmark, replace with embedding-based cosine similarity (e.g., sentence-transformers).

---

## Running the Benchmark

### Verify the scripts are working

```bash
python scripts/benchmark.py --dry-run
```

### Evaluate a single pair

```bash
python scripts/benchmark.py \
  --input benchmarks/corpus/technical-blog/original.txt \
  --output benchmarks/corpus/technical-blog/rewritten.txt
```

### Evaluate all pairs in the corpus

```bash
python scripts/benchmark.py --corpus benchmarks/corpus/
```

### Get JSON output

```bash
python scripts/benchmark.py \
  --corpus benchmarks/corpus/ \
  --json > benchmarks/results/run-$(date +%Y%m%d).json
```

---

## Corpus Structure

Each subdirectory in `benchmarks/corpus/` should contain:

```
corpus/
├── my-example/
│   ├── original.txt      # The AI-generated or AI-assisted text
│   ├── rewritten.txt     # The Not Ai output
│   └── metadata.json     # Optional: genre, source model, intervention mode
└── another-example/
    ├── original.txt
    └── rewritten.txt
```

---

## Adding Your Own Pairs

To add a text pair to the benchmark:

1. Create a subdirectory in `benchmarks/corpus/` with a descriptive name
2. Add `original.txt` (the AI-generated text) and `rewritten.txt` (the Not Ai output)
3. Optionally add `metadata.json`:
```json
{
  "genre": "technical-blog",
  "source_model": "gpt-4o",
  "intervention_mode": "rewrite",
  "notes": "Any relevant context"
}
```

---

## Benchmark Integrity Rules

> **Do not fabricate performance numbers.**

All scores must come from running the script on real (original, rewritten) pairs. Do not manually edit results files. Do not cherry-pick pairs to make the numbers look better.

The benchmark is a tool for honest evaluation and improvement, not for marketing.

---

## Results Directory

Results are written to `benchmarks/results/`. These files are not committed by default (add to `.gitignore` if desired) because results depend on the specific corpus and rewrite quality at time of evaluation.

If you wish to commit results for reproducibility, name them with a date and describe the corpus used:
```
benchmarks/results/2026-09-01-technical-blog-corpus.json
```

---

## Public Domain Corpus Texts

The `corpus/` directory may include public domain texts from Project Gutenberg for testing. These are licensed for free use. Commercial text (news articles, academic papers, etc.) requires licensing and is not included.

To use copyrighted text for private benchmarking, add it locally and do not commit it.
