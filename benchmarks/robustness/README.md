# Not-AI 4.0 Punctuation & Detector Robustness Lab

This directory contains the controlled experimental framework for studying how
punctuation, sentence segmentation, whitespace, lexical/syntactic rewriting,
genre conventions, and author voice interact with text parsers and external
AI-text classifiers.

It replaces the standalone prototype (`not_ai_punctuation_lab`) with a
deterministic, token-safe, multi-condition benchmark integrated with
`not_ai_core.punctuation`, `not_ai_core.robustness`, and `not_ai_core.evaluation`.

---

## Scientific Stance & Core Invariants

1. **Research probes are not writing recommendations.** Conditions `B1` through `B6`
   and `B_punctuation_only` deliberately perturb punctuation (such as dropping an
   internal sentence stop or inserting a tight ellipsis) to measure how external
   classifiers respond to word-preserving typography changes. They are **never**
   applied by Not-AI in production editing.
2. **Word-sequence invariance with literal protection.** Unlike naive string
   replacement, all word-preserving punctuation probes in `not_ai_core.robustness`
   shield decimal numbers (`3.14`), comma-grouped figures (`1,000`), timestamps
   (`09:30 a.m.`), URLs, citations (`(Dugan et al., 2024)`), inline/fenced code,
   initials, and abbreviations (`Dr.`, `U.S.`, `Fig.`) before modifying clause or
   sentence punctuation. Every generated probe is verified by `verify_word_sequence()`.
3. **Zero invisible characters.** No condition ever inserts zero-width spaces
   (`U+200B`), joiners (`U+200C`/`U+200D`), bidirectional controls, tag characters,
   or homoglyphs. Every generated variant is checked with `not_ai_core.unicode_hygiene.scan()`.
4. **Vendor minimum word-count gates.** Official institutional Turnitin AI Writing
   Reports require **at least 300 words of qualifying long-form prose** and suppress
   scores between 1% and 19% due to false-positive concentration
   ([Turnitin file requirements](https://guides.turnitin.com/hc/en-us/articles/28234943089933-File-requirements-for-an-AI-Writing-Report)).
   Third-party web dashboards displaying "human / mixed / AI" percentages on
   100-word snippets are not official Turnitin reports.

---

## Experimental Conditions (A through H)

For any source passage, `scripts/robustness_lab.py` generates and evaluates:

| Code | Condition | Preserves Word Sequence? | Production Editorial Safe? | Purpose |
|---|---|---|---|---|
| **A** | `A_control` | Yes | Yes | Unchanged baseline text |
| **B** | `B_punctuation_only` (plus `B1`–`B6`) | Yes (verified) | No (probe only, except `B2` in casual `social`/`x`) | Isolates punctuation-only sensitivity while holding lexical tokens identical |
| **C** | `C_lexical_syntactic` | No | Yes | Lexical/syntactic rewrite retaining the baseline punctuation convention |
| **D** | `D_combined_edits` | No | No (probe only) | Combines Condition C wording with Condition B punctuation perturbation (completing the 2x2 factorial design) |
| **E** | `E_whitespace_only` | Yes | Yes | Controlled visible whitespace variation with identical words and punctuation marks |
| **F** | `F_sentence_segmentation` | No | Yes | Controlled clause splitting or semicolon joining to test segmentation sensitivity |
| **G** | `G_genre_aware_editorial` | No | **Yes (Not-AI 4.0)** | Full Not-AI 4.0 genre-aware editorial revision (clear agency, specific detail, natural prosody, intact grammar) |
| **H** | `H_voice_matched` | No | **Yes (Not-AI 4.0)** | Revision aligned to a genuine 300+ word author reference sample when available |

---

## Case Study: The 100-Word Modi Passage (`modi_case_study/`)

In the preliminary observation (`modi_case_study/observed_scores.csv`), two
versions of a 100-word biography of Narendra Modi (`modi_70_human.txt` and
`modi_80_human.txt`) had the exact same 100 lexical words in the same order,
differing only in three punctuation positions:

1. `Gujarat. He` → `Gujarat...He` (period + space replaced by tight ellipsis)
2. `rising prices. He` → `rising prices He` (internal period removed)
3. `him today.` → `him today` (final period removed)

Running `python3 scripts/robustness_lab.py compare` reveals the exact mechanism:

```bash
python3 scripts/robustness_lab.py compare \
  benchmarks/robustness/modi_case_study/modi_70_human.txt \
  benchmarks/robustness/modi_case_study/modi_80_human.txt \
  --genre student
```

- **Lexical tokens identical:** `True` (100 words before, 100 words after)
- **Sentence segmentation shift:** `8 sentences -> 6 sentences`
- **Sentence lengths before:** `[8, 7, 10, 12, 20, 7, 13, 20]` (SD = `5.0`, CV = `0.411`)
- **Sentence lengths after:** `[8, 7, 22, 20, 7, 33]` (SD = `9.7`, CV = `0.601`, delta = `+0.190`)
- **Damages grammar:** `True` (`rising prices He has been` is a fused run-on sentence; `Gujarat...He` lacks spacing)

**Why the score shifted:** Removing two sentence boundaries caused rule-based and
statistical sentence splitters to fuse four sentences into two long ones (22 and
33 words), nearly doubling the sentence-length standard deviation (`5.0` → `9.7`)
and inflating the burstiness coefficient of variation by `+46%` (`0.411` → `0.601`),
while creating high-surprisal subword transitions at `Gujarat...He` and
`prices He`. Not-AI 4.0 diagnoses this mechanism explicitly and **refuses** to
use ungrammatical punctuation deletion in production editing.

---

## Running the Lab

### 1. Compare two variants of a passage

```bash
python3 scripts/robustness_lab.py compare \
  benchmarks/robustness/modi_case_study/modi_70_human.txt \
  benchmarks/robustness/modi_case_study/modi_80_human.txt \
  --genre student
```

### 2. Generate all experimental conditions (A–H) and a blank score sheet

```bash
python3 scripts/robustness_lab.py generate \
  benchmarks/robustness/modi_case_study/modi_70_human.txt \
  --out benchmarks/robustness/modi_case_study/variants \
  --genre student \
  --true-origin ai_rewritten \
  --editorial-rewrite benchmarks/robustness/corpus/01-modi-case-study-short/editorial.txt
```

### 3. Analyze manual or permissioned detector score sheets

```bash
python3 scripts/robustness_lab.py analyze-scores \
  benchmarks/robustness/modi_case_study/observed_scores.csv
```

### 4. Evaluate the full 14-fixture multi-genre robustness corpus

```bash
python3 scripts/robustness_lab.py evaluate-corpus \
  --corpus benchmarks/robustness/corpus \
  --scores benchmarks/robustness/modi_case_study/observed_scores.csv \
  --out-report benchmarks/robustness/corpus_evaluation_report.json
```
