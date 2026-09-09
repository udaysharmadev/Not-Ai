# Not Ai: Benchmarks

This directory contains the benchmark framework for evaluating Not Ai's performance on real text pairs.

---

## What the Benchmark Measures

The benchmark evaluates pairs of `(original AI-generated text, Not Ai rewritten text)` on:

| Metric | What it measures | How |
|--------|-----------------|-----|
| Surface wording overlap | How much source wording remains | Token overlap (Jaccard) of content words |
| Number preservation | Were factual numbers preserved? | Set comparison |
| Word count change | Did the text grow or shrink significantly? | Word count delta |
| Structural delta | Did structural patterns improve? | Burstiness, participial rate, nominalization rate, mechanical transition rate |
| Readability delta | Did readability change? | Flesch-Kincaid grade before/after |
| AI vocabulary delta | Were AI-associated terms reduced? | Count before/after |

**On surface wording overlap**: Token overlap is not a meaning check. It measures whether the same content words appear, which is useful for inspecting how far a draft moved from its source. A structural rewrite can preserve meaning while using few source words. Human fidelity review is required before treating a rewrite as correct.

That caveat is usually where such a note stops. Here it does not, because the proxy has been run against the six pairs in `examples/` and it fails on them in a specific and instructive way. Every figure in the table below comes from this loop:

```bash
for d in examples/*/; do
  python3 scripts/benchmark.py --input "$d/input.md" --output "$d/output.md"
done
```

The `examples/` directories do not follow the `original.txt` and `rewritten.txt` layout that `--corpus` expects, so they are run a pair at a time. The `pair` key reads `input` on every one of these runs, because it is taken from the input filename rather than the directory; the row labels below are the directory names.

| Pair | Token overlap | What it indicates | Word count | What the rewrite actually did |
|---|---|---|---|---|
| `already-natural` | 100.0% | No surface rewrite | 0.0% | Nothing. The benchmark extracts the fenced deliverable and excludes its explanatory wrapper. |
| `personal-essay` | low | Surface wording changed | inspect | Abstract nouns replaced with what happened. |
| `academic-abstract` | low | Surface wording changed | inspect | Hypothesis, method and finding preserved; padding cut. |
| `gen-ai-article` | low | Surface wording changed | inspect | Reduced to the two claims the source actually made. |
| `technical-passage` | low | Surface wording changed | inspect | `sophisticated expiration policies to ensure data freshness` became `deciding when a cached copy has gone stale`. |
| `linkedin-post` | low | Surface wording changed | inspect | Three abstract lessons became three specific ones. |

The unchanged pair correctly has 100% overlap after the benchmark extracts its
fenced deliverable. The other pairs still demonstrate the limit of the metric:
token overlap rewards keeping the same words, while a structural rewrite often
replaces abstractions with concrete verbs and named things. A low score records
surface change, not meaning loss.

So read the figure as a similarity of surface wording, which is what it is, and never as a meaning check.

The other columns hold up better, with one caveat each.

`word_count_change` is exact after the benchmark removes a single fenced
deliverable, diagnostic count lines, and a trailing `[FLAG: ...]` note. It is
still a reading prompt, not a quality verdict: a faithful abstract may become
shorter and a useful explanation may become longer.

`number_preservation` catches a dropped figure, and it also catches things that are not figures. On `linkedin-post` it prints `⚠ Numbers lost` followed by `Missing: 1, 2, 3`, which are the `1.` `2.` `3.` markers of a numbered list the rewrite turned into prose. No fact was lost. Read the missing values before believing the warning.

`ai_vocabulary_delta` is useful for finding candidates to review. It does not
decide whether a word is wrong, because quoted material, technical terms, and
deliberate authorial choices can all be legitimate. Editorial wrappers are
removed before this measure runs.

`structural_delta` is four sub-measures with different reliabilities, so read
them separately rather than as a single score. The benchmark now removes common
editorial wrappers before computing them, but nominalization, burstiness, and
participial figures remain heuristic signals. Compare drafts within the same
genre and inspect the underlying text before calling any direction an
improvement.

`readability_delta` prints numbers and no verdict, which is the correct design for it, because the target grade level depends entirely on genre. It earns its place on one pair: the 16.4 to 6.0 fall on `technical-passage` is the clearest signal in the whole report that the rewrite over-corrected, and that example's rationale says so.

This is also the reason the repository ships no aggregate score and no leaderboard. A single number over columns that behave like this would be actively misleading.

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

**Note**: with `--corpus --json` the aggregate summary is suppressed and stdout carries the JSON array only, so the redirect above parses without editing. Per-pair skip notices go to stderr. A single-pair run (`--input` and `--output` with `--json`) emits one JSON object.

Each object has the keys `pair`, `surface_wording_overlap`, `surface_assessment`, `number_preservation`, `word_count_change`, `structural_delta`, `readability_delta` and `ai_vocabulary_delta`. Low overlap is not a failure or a semantic-fidelity verdict.

The script accepts five flags and no others: `--input`, `--output`, `--corpus`, `--dry-run`, `--json`. It exits 1 and prints a one-line reason if a path is missing, if `--corpus` points at a file, or if no pair in the corpus could be evaluated.

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
  "intervention_mode": "default",
  "notes": "Any relevant context"
}
```

`intervention_mode` should record which mode produced the rewrite: `diagnose`, `preserve`, `edit`, or `aggressive`. `benchmark.py` includes valid metadata in corpus JSON output, but it does not derive a quality verdict from it.

Add `protected_facts` when reviewing a pair. This is a human-maintained list of
names, dates, quantities, negations, and causal claims that a rewrite must not
lose. In corpus mode the script reports any protected string that disappears
literally. A missing string requires human review because a valid paraphrase
can preserve the fact. The script cannot determine semantic equivalence or
truth from text alone.

Use [metadata.schema.json](metadata.schema.json) as the shared schema. A
reviewer may also record 1 to 5 ratings for fidelity, clarity, voice fit, and
specificity. Keep these reviews blinded to intervention mode when practical;
they are quality evidence, not a leaderboard.

---

## Benchmark Integrity Rules

> **Do not fabricate performance numbers.**

All scores must come from running the script on real (original, rewritten) pairs. Do not manually edit results files. Do not cherry-pick pairs to make the numbers look better.

The benchmark is a tool for honest evaluation and improvement, not for marketing.

---

## Results Directory

Results are written to `benchmarks/results/`. `.gitignore` already excludes `benchmarks/results/*.json`, because results depend on the specific corpus and on the rewrite quality at the time of evaluation, and a stale committed result is worse than none.

If you wish to commit results for reproducibility, name them with a date and describe the corpus used:
```
benchmarks/results/2026-09-01-technical-blog-corpus.json
```

---

## Public Domain Corpus Texts

The `corpus/` directory may include public domain texts from Project Gutenberg for testing. These are licensed for free use. Commercial text (news articles, academic papers, etc.) requires licensing and is not included.

To use copyrighted text for private benchmarking, add it locally and do not commit it.
