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
| Structural delta | Did structural patterns improve? | Burstiness, participial rate, nominalization rate, mechanical transition rate |
| Readability delta | Did readability change? | Flesch-Kincaid grade before/after |
| AI vocabulary delta | Were AI-associated terms reduced? | Count before/after |

**On semantic similarity**: Token overlap is a proxy, not ground truth. It measures whether the same content words appear, not whether the meaning is equivalent. For a production benchmark, replace it with an embedding-based cosine similarity.

That caveat is usually where such a note stops. Here it does not, because the proxy has been run against the six pairs in `examples/` and it fails on them in a specific and instructive way. Every figure in the table below comes from this loop:

```bash
for d in examples/*/; do
  python3 scripts/benchmark.py --input "$d/input.md" --output "$d/output.md"
done
```

The `examples/` directories do not follow the `original.txt` and `rewritten.txt` layout that `--corpus` expects, so they are run a pair at a time. The `pair` key reads `input` on every one of these runs, because it is taken from the input filename rather than the directory; the row labels below are the directory names.

| Pair | Token overlap | Verdict printed | Word count | What the rewrite actually did |
|---|---|---|---|---|
| `already-natural` | 65.5% | ✓ Meaning largely preserved | ⚠ +62.1% | Nothing. `output.md` reproduces the input verbatim inside a fence and adds 41 words saying why it was left alone. |
| `personal-essay` | 18.5% | ⚠ Major meaning drift | ✓ +19.7% | Abstract nouns replaced with what happened. |
| `academic-abstract` | 15.8% | ⚠ Major meaning drift | ⚠ -22.9% | Hypothesis, method and finding preserved; padding cut. |
| `gen-ai-article` | 11.8% | ⚠ Major meaning drift | ✓ -6.1% | Reduced to the two claims the source actually made. |
| `technical-passage` | 8.1% | ⚠ Major meaning drift | ⚠ -28.2% | `sophisticated expiration policies to ensure data freshness` became `deciding when a cached copy has gone stale`. |
| `linkedin-post` | 7.0% | ⚠ Major meaning drift | ⚠ +29.6% | Three abstract lessons became three specific ones. |

The ranking is inverted. The highest score in the set goes to the one pair that was never rewritten, and every rewrite this repository considers correct is flagged for meaning drift. The mechanism is simple: token overlap rewards keeping the same words, and the whole point of a structural rewrite is to replace abstract nouns with concrete verbs and named things. A rewrite that scores well on this measure has probably only swapped adjectives.

So read the figure as a similarity of surface wording, which is what it is, and never as a meaning check.

The other columns hold up better, with one caveat each.

`word_count_change` is the column whose failures are easiest to read, because the figure is exact and the cause is always inspectable. It fires on three of the six pairs and not one of them is a bad rewrite. On `already-natural` it reports a 62.1% expansion on a pair where the text was not touched at all: every one of those 41 words is `output.md`'s own wrapper, and on the same pair the structural delta calls burstiness `improved` by 0.345 for the same reason. On `academic-abstract` at -22.9% and `linkedin-post` at +29.6% it fires on rewrites that are correct, and in the LinkedIn case most of the growth is the flag block and the bracketed slots rather than the post. Any change past 20% in either direction deserves a reading, which is the most this column can be used for.

`number_preservation` catches a dropped figure, and it also catches things that are not figures. On `linkedin-post` it prints `⚠ Numbers lost` followed by `Missing: 1, 2, 3`, which are the `1.` `2.` `3.` markers of a numbered list the rewrite turned into prose. No fact was lost. Read the missing values before believing the warning.

`ai_vocabulary_delta` moves the right way on every pair here: it falls on all five rewrites, from 14 to 0 on `linkedin-post` and 9 to 3 on `gen-ai-article`, and it stays at 0 on the pair that needed no changes. Its one blind spot is the same one `references/methodology.md` records under honest limits. The 3 terms it still finds in the `gen-ai-article` output are `paradigm shift`, `nuanced` and `multifaceted`, all three quoted inside that output's own flag as examples of what was cut. The column is counting the editorial note, not the prose.

`structural_delta` is four sub-measures with three different reliabilities, so read them separately rather than as a block. `nominalization_delta` is the strongest thing in the report: across these six pairs it says `improved` on all five rewrites without exception and never says `worsened` at all. On `already-natural` it reads `unchanged (+1.2/1k words)`, because the wrapper contributes `measurements` and `Intervention` to the paragraph's three existing suffixes and the added words dilute the rate almost exactly as much. `transition_rate_delta` never points the wrong way either, though it reads `unchanged` twice on texts that had no mechanical transitions to begin with, so it is doing less work than it appears to. `burstiness_delta` is wrong on three of the six. It reports `improved (+0.345)` on the pair where the text was not rewritten, and `worsened` on `technical-passage` and `linkedin-post`, both of which are better prose after the change. `participial_rate_delta` reads `unchanged (+0.000)` on five of six pairs, which is the anchored-pattern false negative described in `references/methodology.md`, not five texts without participials.

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

Each object has the keys `pair`, `semantic_similarity`, `semantic_assessment`, `number_preservation`, `word_count_change`, `structural_delta`, `readability_delta` and `ai_vocabulary_delta`.

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

`intervention_mode` should record which of the skill's modes produced the rewrite: `default`, `diagnose`, `preserve` or `aggressive`. The field is descriptive only; `benchmark.py` does not read it.

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
