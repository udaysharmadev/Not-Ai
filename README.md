<div align="center">

<h1>Not Ai</h1>

<p>A writing intelligence skill for AI-assisted agents.</p>

<p>
<em>Not Ai fixes the structural patterns that make AI writing feel like AI writing.<br>
Not the words. The structure.</em>
</p>

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](scripts/)
[![Research-Backed](https://img.shields.io/badge/Research-PNAS%202025-green)](references/writing-research.md)
[![Cross-Agent](https://img.shields.io/badge/Cross--Agent-SKILL.md-purple)](SKILL.md)
[![No Dependencies](https://img.shields.io/badge/Dependencies-None-brightgreen)](scripts/)

<br>

> **Not Ai is not a detector-bypass tool.**
> The goal is good writing, by human standards, for human readers.
> A result that only fools a detector is a bad result.

</div>

---

## What This Is

Every major humanizer works the same way: find banned words, swap them out, optionally paraphrase. The output usually reads like a slightly different version of the same AI text.

The reason is simple. They fix the wrong thing.

A 2025 PNAS study ([Reinhart et al.](https://arxiv.org/abs/2410.16107)) measured how GPT-4o, Llama 3, and other instruction-tuned models actually differ from human writers. The differences weren't in vocabulary. They were structural:

- Instruction-tuned LLMs open sentences with present participial clauses at **2.2 to 5.3 times the human rate** ("Leveraging the power of...", "Building on this...", "Drawing from...")
- Nominalization density runs **roughly 2.1 times higher** than human writing
- The information density stays high regardless of genre: fiction written by GPT-4o reads as dense as its academic writing
- GPT-4o uses a group of words that includes "camaraderie", "palpable" and "tapestry" at **84 to 171 times the human rate**
- The root cause is instruction tuning. Base Llama 3 models write close to human rates. The RLHF process pushes them away.

Not Ai operates at that structural level. It measures clause type distributions, sentence burstiness, nominalization density, rhetorical engagement markers, and epistemic stance, then intervenes selectively.

---

## Why Not Just Swap Words

When you remove "delve" and "utilize" from a piece of AI writing, the text still has:

- The same present participle rate
- The same nominalization density
- The same paragraph shape on every paragraph
- The same absence of epistemic hedges
- The same missing engagement with the reader
- The same information density for a genre that shouldn't have it

Changing the cologne doesn't change the person.

Not Ai addresses what's underneath. The fair test of that claim is to point the scripts at this file. Here is that output, abridged to the lines worth arguing about, with the per-term vocabulary counts left out for the reason given below:

```
$ python3 scripts/analyze_structure.py README.md

Words: 6270  |  Sentences: 191  |  Paragraphs: 227
  Mean length: 33.8 words   Std deviation: 44.4  (burstiness: 1.316)
  ✓ Good length variation

  ⚠ Nominalization density: 49.1 per 1,000 words  |  elevated for this proxy
  ⚠ Mechanical transitions: 15 instances  |  furthermore, moreover,
      in conclusion, it is worth noting, in the realm of
  ⚠ 'the' used to open 41 sentences
  ⚠ 3 consecutive sentences with same opener
  • flagged vocabulary: leveraging, nuanced, delve, crucial, pivotal,
      camaraderie, tapestry, palpable, and 3 more the report names:
      underscore, utilize, meticulous
      Total: 11 unique terms, 44 occurrences

$ python3 scripts/metrics.py README.md

  Gunning Fog Index:     19.0 (very difficult)
  Flesch Reading Ease:   39.5 / 100
  Balance:               too sparse to judge

$ python3 scripts/repetition.py README.md

  • 'not ai skill': 13x
  • 'git clone https github com': 10x
  ⚠ PARAGRAPH STRUCTURE: 47 unique shapes for 227 paragraphs
  SENTENCE FRAMES: no back-to-back repeat ✓
  COORDINATED SERIES: 16 closing on 'and' or 'or'. No verdict
  LEXICAL DIVERSITY: 34% content-word TTR  |  low diversity for this proxy ⚠
```

These figures are a snapshot, and they are stale the moment a paragraph is added. Treat the three commands as the source of truth rather than the numbers printed above. The per-term vocabulary counts are omitted from the block for a reason worth stating: printing a count means writing the term one more time, so the count is wrong as soon as it is printed. A measurement quoted inside the thing it measures cannot settle, and there is no version of that block whose per-term counts are correct once written. Anyone who has watched a word count creep upward while writing about word counts has met the same problem. The unique-term total survives because adding an eleventh mention of a word already on the list does not change it.

Then read what the output is actually measuring, because most of it is not what it looks like.

Every appearance of `leveraging` in this file is the word being quoted rather than used. Same for `delve`, `crucial`, `pivotal`, `nuanced`, `utilize`, `underscore`, `camaraderie`, `tapestry`, `palpable` and `meticulous`, and for every one of the mechanical transitions: this file catalogues them. The two most repeated phrases are `not ai skill`, which is this skill's own name plus the packaged filename it ships as, and `git clone https github com`, the install command, written out in eight install blocks and twice more in the block above and this sentence. Lexical diversity below 40% is dragged down by the same repetition plus every block of quoted script output. `too sparse to judge` is a refusal rather than a finding: five hedges in a document of this length is too thin a base to read a ratio from, whatever the ratio works out to. An earlier version of that check reported the same file as `over-hedged`, and every file in the repository as something equally unfounded.

Two of the warnings are real and are not excused. A Gunning Fog index near 20 is too high for a page whose main job is explaining how to clone a repository, and under fifty distinct paragraph shapes across more than two hundred paragraphs is monotony however you read it. Both are on the list to fix, and neither is fixed yet.

The two newest checks come back clean, and the shape of that result is worth more than the result. No named sentence frame repeats in adjacent sentences anywhere in this file. Sixteen coordinated series are reported with no verdict attached, because a third item can carry content or can be there for cadence and a regular expression cannot tell which. The check hands a reader a list and stops.

One reading is worth more than either. The burstiness figure earns `✓ Good length variation` on a file whose variance comes from tables, one-line list items and shell commands being counted as sentences, while the human paragraph in `examples/already-natural/` scores 0.200 on the same measure and is flagged for it. `rules/context.md`, which is a list of genre profiles and barely prose at all, scores higher still. Every one of the six examples reaches the same conclusion from a different direction, and it is why nothing here treats the number as a target.

That split is the point, and it is the lesson every example in `examples/` arrives at: a script measures a file, a reader decides what the measurement means. This README is not exempt from its own scripts, and it is not convicted by them either.

---

## The Actual Approach

### Stage 0: Understand the context

Before touching the text, Not Ai figures out:

- What is this? (LinkedIn post, README, academic abstract, personal essay, email, documentation, narrative)
- Who is reading it?
- What register is appropriate?
- What does the author want to accomplish?

A LinkedIn post processed with the rules for an academic abstract becomes worse, not better.

### Stage 1: Measure what's actually wrong

Not Ai runs Python scripts before any rewriting. No LLM guessing, no vibes. Objective counts:

```bash
python3 scripts/analyze_structure.py input.txt
python3 scripts/repetition.py input.txt
python3 scripts/metrics.py input.txt
```

What gets measured:

| Signal | How the script measures it | When the script flags it |
|--------|---------------------------|--------------------------|
| Present participial clause openers | Regex on sentence-initial `-ing` clauses, as a share of sentences | Elevated above 8%, high above 15% |
| Nominalization density | Regex count of `-tion`, `-ment`, `-ness`, `-ity`, `-ance`, `-ence` endings per 1,000 words | Elevated above 35, high above 50 |
| Sentence burstiness | Coefficient of variation of sentence length | Low CV means uniform length, which reads mechanical |
| Mechanical transitions | Count against a fixed list | "Furthermore", "Moreover", "In conclusion" and their relatives |
| AI vocabulary | Hits against a research-derived list | Includes the group GPT-4o uses at 84 to 171 times the human rate |
| Epistemic stance | Hedge to booster ratio, with two floors under it | No verdict below 3 markers or below 2 per 1,000 words. Instruction-tuned models carry hedges at 50% to 63% of the human rate |
| Repeated sentence frames | Eight named frames, counted per sentence rather than per match | Flagged only where one frame lands in two consecutive sentences |
| Coordinated series | Three-item lists closing on `and` or `or` | Listed with no verdict. Flagged where all three items open on the same word |
| Engagement markers | Questions, reader address, first person | Lower in model-written essays than in student essays |
| Readability | Flesch-Kincaid, Gunning Fog | Genre-dependent. Grade 17 on a blog post is a problem |

**Those flag points are heuristics for the proxy, not research findings.** Reinhart et al. measured nominalization at 14.6 per 1,000 tokens in human writing, with instruction-tuned models running about 2.1 times higher, and present participial clause openers at 1.7 per 1,000 tokens in human writing against 2.2 to 5.3 times that in the models. Both figures come from a dependency parse with Biber's tagset. The scripts here use regular expressions instead, so `nominalization_density` counts every word ending in `-tion` or `-ment` and reports a much larger number on the same text. Compare a proxy figure against another proxy figure: the same text before and after, or a draft against the author's earlier work. Never read a proxy figure against the tagged research rate.

### Stage 2: Produce a specific diagnostic

Not a score, not a percentage, not a verdict on whether a machine wrote it. The skill has no way to establish authorship. What it produces is a named list of patterns, each with a quotation from the text, and a strength recorded first so the rewrite knows which register to hold.

Here is the diagnostic for `examples/technical-passage/input.md`, abridged. The full version, with all eleven patterns and the measured table, is in [examples/technical-passage/diagnostic.md](examples/technical-passage/diagnostic.md).

```
NOT AI DIAGNOSTIC
Genre:    Technical explanation, inferred from content. No genre was given.
Register: 4 of 5. Written for working developers, currently pitched at
          a journal.

Working already:
  "caching operates by storing frequently accessed data in a location
  that can be retrieved more rapidly than the original source"
  The technical content is correct and the definition is the right one.
  Nothing in this passage is factually wrong, which sets the constraint:
  this is a rewrite for density and framing, not for accuracy.

Patterns found:
  participial clause    "By leveraging the power of temporary storage
                        solutions"
  participial clause    "By thoughtfully implementing and managing
                        caching solutions"
  mechanical frame      "In the realm of modern software architecture"
  empty conclusion      "In conclusion, caching remains an indispensable
                        tool in the arsenal of modern software engineers"
  uniform paragraphs    4 paragraphs of 2, 5, 3 and 2 sentences, every
                        one of them opening with a claim and following
                        it with support
  (six further patterns in the full diagnostic)

Vocabulary in context:
  "pivotal" 1x       Problem. The claim is not supported and not needed.
  "crucial" 1x       Problem. Expiration policies matter; say why instead.
  "nuanced" 1x       Problem. "a nuanced decision" claims subtlety,
                     supplies none.
  "leveraging" 1x    Problem. Decorative, and it heads a participial
                     clause.
  "latency", "invalidation", "cache busting"
                     Fine. Domain terms doing real work. Keep all three.

Intervention: moderate
```

The measured figures behind that diagnostic: nominalization density 95.4 per 1,000 words on this proxy, which the script flags as high; 4 mechanical transitions; burstiness 0.471; Gunning Fog 20.5; and **0% participial clause openers**, which is wrong. The regex is anchored to the first word of the sentence, so both `By leveraging` and `By thoughtfully implementing` go uncounted. The strongest signal in the research is the one the script is worst at detecting, which is why the diagnostic quotes text rather than reporting numbers.

The finding worth reporting is three or more signals moving in the same direction. A single high number is not.

### Stage 3: Voice profile (when a sample is provided)

With `--voice sample.txt`, Not Ai extracts 10 dimensions:

- Sentence length distribution (mean and standard deviation, which separates a tight writer from an expansive one)
- Paragraph length distribution
- Punctuation habits (em-dash frequency, parenthetical use, semicolons)
- Contraction rate
- First-person usage
- Hedging vs. certainty balance
- Formality level (1-5)
- Rhetorical patterns (questions, direct reader address, analogies, repetition for emphasis)
- Vocabulary level (reading grade, domain vocabulary, phrases the author favours)
- Emotional intensity (flat / measured / engaged / passionate)

This profile becomes a hard constraint throughout the rewrite. If the author never uses em-dashes, Not Ai doesn't insert them.

### Stage 4: Selective rewrite

Eight possible actions per sentence:

`KEEP` `RESTRUCTURE` `REPLACE` `REMOVE` `MERGE` `SPLIT` `MOVE` `FLAG`

The minimum intervention that achieves the goal. If a sentence is fine, it stays. If a specific detail would improve it but isn't in the source, it gets a `[placeholder]`, never an invented fact.

Mode constraints:
- default, no flag: judgment across all eight actions
- `--mode preserve`: only `RESTRUCTURE` and light `REPLACE`
- `--mode aggressive`: `REMOVE`, `MERGE`, `SPLIT` and `MOVE` used freely
- `--mode diagnose`: skips this stage entirely

### Stage 5: Self-review

Two parts. First the scripts run again, on the text about to be delivered rather than on the input, and six conditions have to hold: no back-to-back repeat of a named sentence frame, no three-item series whose third item is there for cadence, nominalization not `high`, stance not `absent` in a genre that carries stance, no flagged vocabulary or em dash in anything written from scratch, and past roughly 120 words a burstiness figure at 0.30 or above with at least one sentence under 8 words and one over 25. Every one of those is a threshold the scripts already print.

That gate matters most in `write` mode, where nothing else in the run measures anything. A generated paragraph that nobody measured is how this skill would ship the exact output it exists to repair.

Then eight questions, answered before producing output, with whatever fails repaired. Six of them:

- What still reads as generic, and could it appear in an article on an unrelated topic?
- Where did I over-edit a sentence that was already working?
- Did I introduce any fact, number, name or feeling absent from the source?
- Did I change the author's position, hedge a claim they made firmly, or firm up a claim they hedged?
- Is every paragraph now equally polished? Human drafts are uneven, and uniform polish is itself a tell.
- Does this read as the author, or as generic corrective prose?

The last of the eight catches the most embarrassing failure: a rationale claiming an em dash was removed while the output still contains it. All eight are in [SKILL.md](SKILL.md).

### Stage 6: Output

Diagnostic report + rewritten text + change rationale. The rationale explains what changed and why, so the author can push back on anything.

---

## Architecture

```
INPUT TEXT
    │
    ▼
┌──────────────────────┐
│  Stage 0             │   genre / audience / register / intent
│  Context             │
└──────────┬───────────┘
           │  loads: rules/context.md
           ▼
┌────────────────────────────────────────────┐
│  Stage 1: Deterministic Analysis           │
│                                            │
│  analyze_structure.py ──┐                  │
│  repetition.py  ────────┼──► JSON report   │
│  metrics.py  ───────────┘                  │
│                                            │
│  No LLM. Objective counts.                 │
└──────────┬─────────────────────────────────┘
           │
           ▼
┌──────────────────────┐
│  Stage 2             │   specific findings with quotes from text
│  Diagnostic Report   │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐   (only if --voice flag)
│  Stage 3             │   10-dimension author voice profile
│  Voice Profile       │
└──────────┬───────────┘
           │
           ▼
┌────────────────────────────────────────────┐
│  Stage 4: Selective Rewrite                │
│                                            │
│  KEEP · RESTRUCTURE · REPLACE · REMOVE     │
│  MERGE · SPLIT · MOVE · FLAG               │
│                                            │
│  Voice profile + genre rules = hard        │
│  constraints. Never invent.                │
└──────────┬─────────────────────────────────┘
           │
           ▼
┌──────────────────────┐
│  Stage 5             │   8 questions about what went wrong
│  Self-Review         │
└──────────┬───────────┘
           │
           ▼
┌──────────────────────┐
│  Stage 6             │   diagnostic + rewrite + rationale
│  Output              │
└──────────────────────┘
```

---

## How It Compares

The useful question is not which tool scores better on a feature checklist. It is what level of the text each one changes. There are three, and they are not equivalent:

1. **Lexical substitution.** Find flagged words, swap in alternatives. The sentence keeps its shape.
2. **Paraphrase.** Send the text back through a model with an instruction to reword it. Sentence boundaries and clause choices move, but they move toward whatever the paraphrasing model's own defaults are.
3. **Morphosyntactic restructuring.** Change which clause types carry the information, how dense it is, and where the cadence breaks. This is the level at which the PNAS measurements were taken.

### Commercial humanizers

Each tool below advertises the same job: take AI-generated text and rewrite it so it reads as human. Most name getting past a detector as the benefit.

| Tool | Level its own public description points to |
|------|-------------------------------------------|
| Undetectable AI | An AI humanizer that rewords and rewrites AI output. Substitution plus paraphrase. |
| WriteHuman | Rewriting AI text to defeat detectors, marketed on detector outcomes. Substitution plus paraphrase. |
| QuillBot | A paraphrasing tool with selectable modes. Paraphrase, and it does not present itself as a humanizer. |
| HIX Bypass | Multi-pass rewriting aimed at detector outcomes. Paraphrase, repeated. |

None of the four publishes a list of the structural features it measures. That is a statement about their published descriptions, which anyone can check, and not a claim about code none of us can read.

The mechanism has a consequence worth stating plainly. Paraphrase moves text toward the paraphrasing model's own distribution, which is the distribution the problem came from. That is why paraphrase-based output tends to acquire a recognizable second accent of its own rather than losing the first one.

### Open-source humanizer skills

| Project | What its repository contains |
|---------|------------------------------|
| blader/humanizer | A list of AI tells drawn from the Wikipedia signs page, plus voice matching against a user sample. Word and phrase level. |
| Aboudjem/humanizer-skill | Around 55 patterns extended from the same Wikipedia list, five fixed voice modes, and a 0-100 AI-tell score. Word and phrase level, pure Markdown, no dependencies. |
| Not Ai | Python scripts that count clause openers, nominalization, burstiness, transitions, hedges and engagement markers before any rewriting. Eight genre profiles in `rules/context.md`, a ten-dimension voice profile in `rules/voice.md`, an eight-question self-review in `SKILL.md`, and a before-and-after evaluation framework in `benchmarks/`. |

The Wikipedia signs list is a good list and Not Ai carries its own annotated version of it in [references/wikipedia-signs.md](references/wikipedia-signs.md). The difference is what happens after the list. A lexical skill flags the word and offers a substitute. Not Ai's scripts report clause-type and density figures for the whole text first, and vocabulary is handled last, on the argument that a word swap inside a badly built sentence changes nothing a reader notices.

Not Ai produces no score at all, on purpose. A number implies a verdict on authorship that no method here can support. The evaluation framework in `benchmarks/` demonstrates the risk on its own terms: its meaning-preservation figure flags five of the six examples in this repository for `Major meaning drift`, including every rewrite considered correct here, and awards its highest score to the one pair where nothing was rewritten. That table is printed in [benchmarks/README.md](benchmarks/README.md) rather than buried, because a measure ranking the examples backwards is worth knowing about before anyone treats a benchmark figure as a verdict.

**How this comparison was made.** In August 2026, from each commercial product's own public description and from the published files of each open-source repository. Nothing here rests on running the tools side by side: the corpus in `benchmarks/` is empty, no head-to-head evaluation has been done, and the framework is there for anyone who wants to do one. Product capabilities change, so check the current documentation before relying on any row. The working notes behind this table are in [references/writing-research.md](references/writing-research.md).

---

## Installation

Not Ai uses the `SKILL.md` format, a plain filesystem convention that works with any agent that reads context files. Clone once, it works everywhere.

Some hosts will only accept a skill as one file. For those, install `dist/SKILL.md`. It is a generated file, kept in version control so a clone arrives with it; if your copy does not have it, run `python3 scripts/build_single_file.py` first. See [hosts that accept only one file](#hosts-that-accept-only-one-file) below.

### Antigravity (Google)

```bash
# Global install, works in all projects
git clone https://github.com/udaysharmadev/Not-Ai \
  ~/.gemini/antigravity/skills/not-ai

# Project-local
git clone https://github.com/udaysharmadev/Not-Ai \
  .gemini/skills/not-ai
```

Trigger: `Not Ai this`, `Not Ai --mode diagnose`, `Not Ai --voice sample.txt`

---

### Claude Code

```bash
git clone https://github.com/udaysharmadev/Not-Ai \
  ~/.claude/skills/not-ai

# Or project-local
git clone https://github.com/udaysharmadev/Not-Ai \
  .claude/skills/not-ai
```

Claude Code reads `SKILL.md` files at startup. Use it with `/not-ai` or just type `Not Ai this:`.

---

### Claude Desktop

The desktop app saves a skill as a single `SKILL.md` and refuses an upload that carries anything else, so install the built file rather than the repository. Both build products live in `dist/` and are kept in version control: `dist/SKILL.md` is the whole skill in one file, and `dist/not-ai.skill` is that same file in an archive holding one member, for hosts that take a `.skill` upload. Install either, then type `Using the Not Ai skill, diagnose and rewrite this:`. If your copy of `dist/` is empty, run `python3 scripts/build_single_file.py` to regenerate both.

After changing anything in the repository, rebuild before installing again:

```bash
python3 scripts/build_single_file.py
python3 scripts/verify_single_file.py
```

To use it in a Project instead, upload `SKILL.md` together with the `rules/` and `references/` folders. `SKILL.md` is a router and expects to be able to load both, so uploading it alone gives an agent the pipeline with none of the rules behind it.

---

### Hosts that accept only one file

The build script assembles the router, all seven rule files, all four references, all six worked examples and the measurement script into one document. Both products are committed, so this needs running only after an edit, or once if `dist/` is empty:

```bash
python3 scripts/build_single_file.py     # writes dist/SKILL.md and dist/not-ai.skill
python3 scripts/verify_single_file.py    # 18 checks, all must pass
```

The repository stays canonical. Nothing in `dist/` is edited by hand: every section is read from the file it names, so the only step needed after changing a rule is to run the build again. The generated file names each section after its repository path, so an agent that searches it for `rules/context.md` lands on the section that file became.

Two things differ in the single-file build, both of them noted inside it. The three measurement scripts become one embedded script, `scripts/measure.py`, which the agent writes to a temp file and runs. And the six `examples/*/input.md` specimens are fenced, because they are examples of the writing this skill repairs and their em dashes would otherwise be indistinguishable from the skill's own prose.

The embedded script reports the same figures as the three it replaces. `scripts/verify_measure.py` checks that claim file by file rather than asking anyone to trust it:

```bash
python3 scripts/verify_measure.py
```

---

### Cursor

```bash
# Cursor reads .mdc files from .cursor/rules/
cp /path/to/Not-Ai/SKILL.md .cursor/rules/not-ai.mdc

# Or full install
git clone https://github.com/udaysharmadev/Not-Ai \
  .cursor/skills/not-ai
```

Reference it in Cursor chat with `@not-ai` or trigger naturally.

---

### GitHub Copilot

Copilot doesn't load SKILL.md natively. Three options:

**Option A: Copilot Instructions**
```bash
cat /path/to/Not-Ai/SKILL.md >> .github/copilot-instructions.md
```

**Option B: Paste into Copilot Chat** as a system message before sending your text.

**Option C: Copilot Extension** using the Extensions API, with `SKILL.md` as the system prompt.

---

### OpenAI Codex CLI

```bash
git clone https://github.com/udaysharmadev/Not-Ai \
  ~/.codex/skills/not-ai

# Or append to AGENTS.md
cat /path/to/Not-Ai/SKILL.md >> AGENTS.md
```

```bash
codex "Not Ai this: [text]"
codex "Not Ai --mode diagnose: [text]"
```

---

### Gemini CLI

Same as Antigravity. The Gemini CLI reads from `~/.gemini/antigravity/skills/`:

```bash
git clone https://github.com/udaysharmadev/Not-Ai \
  ~/.gemini/antigravity/skills/not-ai
```

---

### ChatGPT

**Custom GPT:**
1. Go to ChatGPT → Create a GPT
2. Paste `SKILL.md` contents into the Instructions field
3. Upload `rules/` files as Knowledge
4. Save and use it directly

**ChatGPT Projects:**
Add `SKILL.md` and key rule files to Project Files.

**API (system prompt):**
```python
import openai
from pathlib import Path

skill = Path("SKILL.md").read_text()

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": skill},
        {"role": "user", "content": f"Not Ai this:\n\n{your_text}"}
    ]
)
```

---

### Windsurf / Codeium

```bash
cp /path/to/Not-Ai/SKILL.md .windsurfrules

# Or full install
git clone https://github.com/udaysharmadev/Not-Ai \
  .windsurf/skills/not-ai
```

---

### Aider

```bash
aider --read /path/to/Not-Ai/SKILL.md \
      --read /path/to/Not-Ai/rules/structure.md \
      --read /path/to/Not-Ai/rules/rhetoric.md
```

Or add to `.aider.conf.yml`:
```yaml
read:
  - /path/to/Not-Ai/SKILL.md
  - /path/to/Not-Ai/rules/
```

---

### Any other agent

If your agent loads context files, add `SKILL.md`. If it uses `AGENTS.md`, append `SKILL.md` to it. If it has a system prompt field, paste `SKILL.md` there.

The skill requires no dependencies beyond what the agent already has. The optional measurement scripts need Python 3.10 or later, standard library only, because they annotate with `list[str] | None`.

---

## Usage

```
Not Ai this: [text]                           default rewrite
Not Ai --mode diagnose [text]                 report only, no changes
Not Ai --mode preserve [text]                 strict meaning preservation
Not Ai --mode aggressive [text]               stronger structural changes
Not Ai --voice my-writing.txt [text]          match to your voice sample
```

Run the analysis scripts directly:

```bash
python3 scripts/analyze_structure.py input.txt   # structural fingerprint
python3 scripts/repetition.py input.txt          # phrase and pattern repetition
python3 scripts/metrics.py input.txt             # readability and density
python3 scripts/measure.py input.txt             # all three in one pass
python3 scripts/benchmark.py --dry-run           # verify everything works

# Evaluate a before/after pair
python3 scripts/benchmark.py \
  --input original.txt \
  --output rewritten.txt

# JSON output for automation
python3 scripts/analyze_structure.py input.txt --json
```

Check the repository against itself:

```bash
python3 scripts/scan_prose.py            # dashes and AI vocabulary in its own prose
python3 scripts/verify_measure.py        # measure.py agrees with the three originals
python3 scripts/verify_checks.py         # negative controls for the three newest checks
python3 scripts/verify_single_file.py    # the generated single file is sound
```

---

## What the scripts measure

### analyze_structure.py

Output for `examples/technical-passage/input.md`, verbatim except for two lines wrapped to fit:

```
NOT AI : STRUCTURAL ANALYSIS
────────────────────────────────────────
Words: 241  |  Sentences: 12  |  Paragraphs: 4

SENTENCE RHYTHM
  Mean length:   19.9 words
  Std deviation: 9.4 words  (burstiness: 0.471)
  Very short (<8):  1  |  Short (8-15): 4  |  Medium (16-25): 5
  Long (26-35):  1  |  Very long (35+): 1

STRUCTURAL SIGNALS
  ✓ Participial clause openers: 0 / 12 sentences (0%)  |  normal for this proxy
      Anchored match only. 'By leveraging...' style openers are not counted.
  ⚠ Nominalization density: 95.4 per 1,000 words  |  high for this proxy
      Proxy measure. Compare only against another run of this script.
  ⚠ Mechanical transitions: 4 instances  |  furthermore, in conclusion,
      it is worth noting, in the realm of

SENTENCE OPENINGS
  ✓ No highly repeated sentence openers

AI-ASSOCIATED VOCABULARY
  • 'leveraging': 1x
  • 'crucial': 1x
  • 'pivotal': 1x
  • 'nuanced': 1x
  Total: 4 unique terms, 4 occurrences
  Note: Contextual interpretation required. Presence is a signal, not
  automatic proof of AI authorship.
```

Three things in that output are worth reading closely.

**The 0% on participial openers is wrong, and the script says so on the next line.** Two of this passage's twelve sentences open with a participial clause headed by `By`: `By leveraging the power of temporary storage solutions` is the second sentence of the first paragraph, and `By thoughtfully implementing and managing caching solutions` is the last sentence of the passage. The regex requires the participle to be the first word, so a preposition in front of it defeats the match. The caveat line is printed with every run rather than buried in a docstring, because the strongest signal in the research is the one this proxy is worst at detecting. Replacing the regex with a real dependency parse is on the contributing list below.

**Every figure is labelled `for this proxy`.** 95.4 nominalizations per 1,000 words is not comparable to the 14.6 per 1,000 tokens that Reinhart et al. report for human writing, because that figure comes from a tagged parse and this one comes from counting suffixes. Compare proxy to proxy, or the number means nothing.

**Nothing in the output states a verdict.** No score, no percentage, no claim about who wrote it. `examples/already-natural/` shows the same script raising two warnings on a paragraph a human wrote about their own week, which is the reason.

### measure.py

The same measurements as the three scripts above, in one file with no sibling imports, written for the single-file build where an executable sibling cannot be shipped. It prints one combined report and takes `--json` and `--stdin` like the others.

Condensed does not mean re-derived. Every regex, threshold and formula is transplanted from the file it came from, because the figures in the worked examples were produced by the originals and a version that measured slightly differently would invalidate every table in the repository without saying so. `scripts/verify_measure.py` compares the two on every markdown file in the repository, the built single file included, and requires exact equality on every shared figure, down to the last decimal place:

```
Files checked: 45
Figure mismatches: 0

PARITY OK
```

That check earns its keep. Three plausible transcription slips were tried against it while it was being written: sample variance instead of population variance in burstiness, `tokenize_words` instead of `text.split()` as the denominator in the stance counts, and dropping the trailing-`e` rule from the syllable counter. They produced 88, 56 and 149 mismatches. None of the three would have been visible by reading the code side by side.

### verify_checks.py

Three checks have no negative control anywhere in this repository's own text, so their controls are written by hand.

`stance_balance` is the reason the file exists. Not one file here earns a real balance verdict, so `over-hedged`, `over-assertive` and `calibrated` are unreachable from repository text. An earlier version of that function compared the hedge and booster counts directly and returned one of three verdicts unconditionally. Because `0 > 0` is false in both branches, a text with no stance marker at all fell through to `calibrated`, which reads as a clean bill of health on the one signal where the research gives a specific underuse figure: instruction-tuned models carry hedges at 50% to 63% of the human rate. Every file in the repository got a verdict and not one of them was right. The breakdown is in the comment above `STANCE_MIN_MARKERS` in `scripts/_shared.py`. No test caught the bug, because no test existed.

The other two are the frame and series checks, whose warnings need input this repository does not contain: the same frame in two adjacent sentences, or three list items opening on the same word.

Each control declares which of three kinds it is, and the third kind does the most work:

```
MUST FIRE        the check is supposed to catch this
MUST STAY QUIET  the check is supposed to let this through
KNOWN LIMIT      the check gets this wrong, on the record
```

Six limits are pinned that way. A series written without the Oxford comma is missed entirely, because detection is comma-delimited. `Economically, India grew, and Bollywood thrived` is reported as a series although it is a compound sentence with an adverbial in front of it. `In conclusion, caching remains` matches the frame named `comma plus -ing word` although the word after the comma is a gerund subject and nothing has been appended to anything. Recording those as tests means a later edit cannot change the documented behaviour without a control turning red. The frames are named after the string they match for the same reason: calling the last one a participial tail would claim more than the regex delivers.

Writing the controls turned up one real bug and one bad specimen. The parallel-triple detector had been comparing the lead words of all three comma segments, and since the first segment carries the sentence stem, `The plan needed a bigger room, a longer window, and a second reviewer` came back as the, a, a and went unreported. Separately, the specimen written for the rate floor held 3 hedges in 552 words, which is 5.4 per 1,000 and above the floor, so it returned `over-hedged` and the specimen was at fault rather than the code. A control that fails for the wrong reason is worth as little as no control.

### benchmark.py

Evaluates before/after pairs. Produces:

| Metric | What it means |
|--------|--------------|
| Semantic similarity | Was meaning kept? (token overlap) |
| Number preservation | Were specific facts kept? |
| Burstiness delta | Did sentence variation improve? |
| Participial rate delta | Did clause structure improve? |
| Nominalization delta | Did density reduce? |
| FK grade delta | Did readability change? |
| AI vocabulary delta | Were AI-associated terms reduced? |

---

## Repository structure

```
not-ai/
├── SKILL.md                    core skill file
├── README.md
├── LICENSE
├── .gitignore
│
├── rules/
│   ├── context.md              8 genre profiles, audience, register
│   ├── structure.md            clause types, nominalization, density
│   ├── rhythm.md               sentence cadence, opening repetition
│   ├── specificity.md          generic vs. specific, the evidence rule
│   ├── rhetoric.md             epistemic stance, engagement markers
│   ├── vocabulary.md           word-level tells and what to do about each
│   └── voice.md                10-dimension voice profile
│
├── scripts/
│   ├── _shared.py              tokenizing, sentence splitting, shared counters
│   ├── analyze_structure.py    clause openers, nominalization, burstiness
│   ├── repetition.py           repeated phrases, lexical diversity
│   ├── metrics.py              readability, density, stance, engagement
│   ├── benchmark.py            before/after evaluation
│   ├── measure.py              all of the above in one stdlib-only file,
│   │                           for the single-file build
│   ├── verify_measure.py       proves measure.py matches the originals
│   ├── verify_checks.py        negative controls for stance, frames, series
│   ├── scan_prose.py           checks this repo against its own rules
│   ├── build_single_file.py    generates dist/
│   └── verify_single_file.py   18 checks on the generated file
│
├── references/
│   ├── wikipedia-signs.md      catalogue of observable AI writing signs,
│   │                           including the ones that produce false positives
│   ├── writing-research.md     source studies and what each supports
│   ├── style-research.md       measured feature rates by model and genre
│   └── methodology.md          design rationale and honest limits
│
├── benchmarks/
│   ├── README.md               how to run and read a before/after evaluation
│   ├── corpus/                 before/after pairs (empty; contributions welcome)
│   └── results/                JSON output, gitignored
│
├── dist/                       built by scripts/build_single_file.py,
│   │                           kept in the tree, not gitignored
│   ├── SKILL.md                the whole skill in one file
│   └── not-ai.skill            the same file, archived, one member
│
└── examples/                   each: README, input, diagnostic, output, rationale
    ├── technical-passage/      over-editing, and how far is too far
    ├── gen-ai-article/         a source with no facts in it
    ├── linkedin-post/          generated text that passes the structural scan
    ├── academic-abstract/      a warning that should be read and declined
    ├── personal-essay/         the line the skill refuses to rewrite
    └── already-natural/        zero changes, the case for not intervening
```

Every figure quoted in an example comes from an actual run of the scripts on the file in that folder. The commands are printed alongside the numbers so any of them can be checked in a few seconds.

---

## What Not Ai will not do

No matter the mode or instructions:

- Add random typos to seem human
- Force slang into the wrong register
- Invent memories, emotions, or opinions
- Fabricate facts, citations, or statistics
- Introduce deliberate grammar mistakes
- Force first-person where the author uses third
- Optimize for a detector score
- Rewrite everything when selective edits are enough
- Apply essay rules to technical documentation

If a specific detail would improve a sentence but isn't in the source, it gets flagged as `[specific detail here]`. Not invented.

---

## Research

The structural signals Not Ai measures come from these studies:

| Study | Finding used |
|-------|-------------|
| [Reinhart et al., PNAS 2025](https://arxiv.org/abs/2410.16107) | Present participial rates, nominalization density, instruction tuning as root cause |
| [Jiang & Hyland, 2025](https://www.sciencedirect.com/science/article/pii/S0889490624000978) | Engagement marker deficit, epistemic stance differences |
| [StoryScope, Russell et al. 2026](https://arxiv.org/abs/2604.03136) | AI stories cluster in shared narrative space; human writing is diverse |
| [Siler, PNAS 2026](https://www.pnas.org/doi/10.1073/pnas.2605754123) | "delve", "underscore", "meticulous" in 7.3M published academic papers |
| [Milicka et al., 2025](https://arxiv.org/abs/2509.10179) | All LLMs shift toward information-dense style regardless of genre |
| [Ming et al., 2026](https://journals.flvc.org/FLAIRS/article/view/136013) | RLHF induces Romance-origin vocabulary shift |

Full bibliography: [references/writing-research.md](references/writing-research.md)

**On the state of these citations.** The first row carries most of the weight. Reinhart et al. is the study the structural signals are actually derived from, it was read in full, and every figure taken from it appears with its exact value in [references/style-research.md](references/style-research.md). Jiang and Hyland and Milicka et al. supply the engagement and density findings and are cited for those findings only.

The remaining three rows are weaker and are marked as such rather than removed. Their bibliographic details reached this repository through secondary sources and have not been checked against the originals, so a title, venue or year may be wrong even where the finding is right. No rule in `rules/` depends on any of the three. Anyone building on them should verify the citation first, and a correction is a welcome contribution.

This note exists because unverified citations presented with confidence are one of the specific failures catalogued in [references/wikipedia-signs.md](references/wikipedia-signs.md). A repository about machine-writing tells should not ship one.

---

## Limitations

- The structural signals reflect 2024-2025 model behavior. Models update; Not Ai's thresholds should too.
- Fine-tuning on genre-specific data can reduce the fingerprint (Dawkins et al., 2025). Newer fine-tuned models may score differently.
- Token overlap is a proxy for semantic similarity, not a guarantee.
- Genre detection can be wrong. The user should confirm it.
- Voice profiles from short samples (under 200 words) are approximate.
- Not Ai cannot verify factual claims. It preserves errors that were in the original.
- Research is predominantly English. Cross-language behavior is unstudied.

---

## Contributing

The most useful contributions:

- Genre profiles for contexts not yet covered
- Updated vocabulary lists as new model behavior is documented
- Before/after benchmark pairs in any genre
- spaCy or NLTK integration for `analyze_structure.py` (replacing regex proxies with real morphosyntactic parsing)
- Sentence-transformer integration for `benchmark.py` (replacing token overlap with embedding similarity)
- Cross-language rule files

Read [references/methodology.md](references/methodology.md) before contributing rules. Everything needs a research rationale.

---

## License

MIT. See [LICENSE](LICENSE).

---

<div align="center">
<em>"Remove the machine's generic habits. Preserve the person's voice."</em>
</div>
