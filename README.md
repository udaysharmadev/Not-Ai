<div align="center">

<h1>Not Ai</h1>

<p>A writing intelligence skill for AI-assisted agents.</p>

<p>
<em>Not Ai fixes the structural patterns that make AI writing feel like AI writing.<br>
Not the words. The structure.</em>
</p>

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](scripts/)
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

- Instruction-tuned LLMs open sentences with present participial clauses at **2 to 5 times the human rate** ("Leveraging the power of...", "Building on this...", "Drawing from...")
- Nominalization density runs **1.5 to 2 times higher** than human writing
- The information density stays high regardless of genre — fiction written by GPT-4o reads as dense as its academic writing
- GPT-4o uses "camaraderie", "palpable", "tapestry" at over **100 times the human rate**
- The root cause is instruction tuning. Base Llama 3 models write close to human rates. The RLHF process pushes them away.

Not Ai operates at that structural level. It measures clause type distributions, sentence burstiness, nominalization density, rhetorical engagement markers, and epistemic stance — then intervenes selectively.

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

Not Ai addresses what's underneath. Here's what the scripts caught when run on the README I wrote before the user flagged it:

```
⚠ Nominalization density: 61.9 per 1,000 words — high (AI-like)
   Human norm: 25–40

⚠ AI-associated vocabulary:
   • 'leveraging': 5x (in a README about how bad "leveraging" is)
   • 'pivotal': 4x
   • 'foster', 'delve', 'underscore', 'utilize': 1x each

⚠ Gunning Fog Index: 29.8 — classified: very difficult
   A technical README should be around 12–14.

⚠ Lexical diversity: 34% — low (AI-like)
```

The README that shipped with this project before this version had all of those problems. That's why this version exists.

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

| Signal | Measured as | AI vs. human baseline |
|--------|------------|----------------------|
| Present participial clause rate | % of sentences | Human: 5–8%. Instruction-tuned LLMs: 15–25% |
| Nominalization density | Per 1,000 words | Human: 25–40. LLMs: 45–70 |
| Sentence burstiness | Coefficient of variation | Low CV = uniform = AI-like |
| Mechanical transitions | Count per sentence | "Furthermore", "Moreover", "In conclusion", etc. |
| AI vocabulary | Hits from research-backed list | Includes 100x-overused GPT-4o words |
| Epistemic stance | Hedge vs. booster ratio | LLMs have fewer calibrated hedges |
| Engagement markers | Questions, reader address, first-person | LLMs score significantly lower in essays |
| Readability | Flesch-Kincaid, Gunning Fog | Genre-dependent — a blog at grade 17 is a problem |

### Stage 2: Produce a specific diagnostic

Not a score. Not a vibe. A specific report with examples from the text:

```
NOT AI DIAGNOSTIC
─────────────────────────────
Genre:     Technical explanation
Quality:   51/100

Structural patterns to address:
  • Participial clause openers: 4 in 4 paragraphs (25% rate — 3-5x human)
    — "By leveraging the power of", "By thoughtfully implementing"
  • Nominalization density: 91.3/1,000 words (human norm: 25–40)
    — "implementations", "invalidation", "consideration"
  • Mechanical transitions: "Furthermore", "In conclusion",
    "It is worth noting", "In the realm of"

Vocabulary (in context):
  • "pivotal", "fundamentally transforms", "indispensable"
  • These signal inflated significance — the surrounding text
    doesn't support the claims.

Recommended intervention: Moderate
```

### Stage 3: Voice profile (when a sample is provided)

With `--voice sample.txt`, Not Ai extracts 10 dimensions:

- Sentence length distribution (mean, std — is this a tight or expansive writer?)
- Paragraph length
- Punctuation habits (em-dash frequency, parenthetical use, semicolons)
- Contraction rate
- First-person frequency
- Hedging vs. certainty ratio
- Formality level (1–5)
- Reader address patterns
- Concrete example density
- Emotional intensity (flat / measured / engaged / passionate)

This profile becomes a hard constraint throughout the rewrite. If the author never uses em-dashes, Not Ai doesn't insert them.

### Stage 4: Selective rewrite

Eight possible actions per sentence:

`KEEP` `RESTRUCTURE` `REPLACE` `REMOVE` `MERGE` `SPLIT` `MOVE` `FLAG`

The minimum intervention that achieves the goal. If a sentence is fine, it stays. If a specific detail would improve it but isn't in the source, it gets a `[placeholder]` — never an invented fact.

Mode constraints:
- `--mode preserve`: only `RESTRUCTURE` and light `REPLACE`
- `--mode rewrite`: judgment-based (default)
- `--mode aggressive`: all actions available
- `--mode diagnose`: skips this stage entirely

### Stage 5: Adversarial self-review

After rewriting, Not Ai asks itself 12 questions about what might have gone wrong:

- What still sounds generic?
- Where did I over-edit?
- Did I invent anything?
- Did I change the author's position on anything?
- Did I make every paragraph equally polished? (Humans don't.)
- Does this now sound like "humanizer writing" rather than the author?

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
│  Stage 5             │   12 questions about what went wrong
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

### vs. commercial humanizers

| | Undetectable AI | WriteHuman | QuillBot | HIX Bypass | Not Ai |
|-|:-:|:-:|:-:|:-:|:-:|
| Works at structural level | ✗ | ✗ | ✗ | ✗ | ✓ |
| Voice preservation | ✗ | ✗ | ✗ | ✗ | ✓ |
| Genre-aware | ✗ | ✗ | ✗ | ✗ | ✓ |
| Specific diagnostic | ✗ | ✗ | ✗ | ✗ | ✓ |
| Fabrication prevention | ✗ | ✗ | ✗ | ✗ | ✓ |
| Meaning preservation check | ✗ | ✗ | ✗ | ✗ | ✓ |
| Open source | ✗ | ✗ | ✗ | ✗ | ✓ |
| Research basis | — | — | — | — | PNAS 2025 + |
| Converges to "humanizer voice" | ✓ | ✓ | ✓ | ✓ | ✗ |

### vs. open-source humanizer skills

| | blader/humanizer | Aboudjem/humanizer-skill | harshaneel/humanize | Not Ai |
|-|:-:|:-:|:-:|:-:|
| Signal level | Lexical | Lexical | Lexical | Morphosyntactic |
| Structural diagnosis | ✗ | ✗ | ✗ | ✓ |
| Author voice extraction | Basic | 5 fixed templates | ✗ | 10-dimension profile |
| Genre profiles | ✗ | ✗ | ✗ | 8 genres |
| Deterministic scripts | ✗ | ✗ | ✗ | 4 Python scripts |
| Adversarial self-review | ✗ | ✗ | ✗ | 12-question |
| Benchmark framework | ✗ | ✗ | ✗ | ✓ |
| Research basis | Wikipedia | Wikipedia | Unspecified | Reinhart et al., Jiang & Hyland, StoryScope |

---

## Installation

Not Ai uses the `SKILL.md` format — a plain filesystem convention that works with any agent that reads context files. Clone once, it works everywhere.

### Antigravity (Google)

```bash
# Global — works in all projects
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

Claude Desktop doesn't load files automatically, so add it to a Project:

1. Clone the repo locally
2. Create a Project in Claude Desktop
3. Upload `SKILL.md` and the `rules/` folder to Project Knowledge
4. Type: `Using the Not Ai skill, diagnose and rewrite this:`

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

**Option A — Copilot Instructions:**
```bash
cat /path/to/Not-Ai/SKILL.md >> .github/copilot-instructions.md
```

**Option B — Paste into Copilot Chat** as a system message before sending your text.

**Option C — Copilot Extension** using the Extensions API, with `SKILL.md` as the system prompt.

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

Same as Antigravity — the Gemini CLI reads from `~/.gemini/antigravity/skills/`:

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

The skill requires no dependencies beyond what the agent already has.

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
python3 scripts/benchmark.py --dry-run           # verify everything works

# Evaluate a before/after pair
python3 scripts/benchmark.py \
  --input original.txt \
  --output rewritten.txt

# JSON output for automation
python3 scripts/analyze_structure.py input.txt --json
```

---

## What the scripts measure

### analyze_structure.py

```
NOT AI — STRUCTURAL ANALYSIS
────────────────────────────────────────
Words: 263  |  Sentences: 12  |  Paragraphs: 7

SENTENCE RHYTHM
  Mean length:   21.9 words
  Burstiness:    0.533  (low = uniform = AI-like)

STRUCTURAL SIGNALS
  ✓ Participial clause openers: 0%  — normal
  ⚠ Nominalization density: 91.3/1,000 words — high (AI-like)
  ⚠ Mechanical transitions: 4 — "furthermore", "in conclusion", ...

AI-ASSOCIATED VOCABULARY
  • 'leveraging': 1x
  • 'crucial': 1x
  • 'pivotal': 1x
```

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
│
├── rules/
│   ├── structure.md            clause types, nominalization, density
│   ├── voice.md                10-dimension voice profile
│   ├── specificity.md          generic vs. specific, the evidence rule
│   ├── rhythm.md               sentence cadence, opening repetition
│   ├── rhetoric.md             epistemic stance, engagement markers
│   └── context.md              8 genre profiles
│
├── scripts/
│   ├── analyze_structure.py
│   ├── repetition.py
│   ├── metrics.py
│   └── benchmark.py
│
├── references/
│   ├── wikipedia-signs.md      11 AI writing signs, each annotated
│   ├── writing-research.md     12+ papers with findings and relevance
│   ├── style-research.md       measured differences by model and genre
│   └── methodology.md          design rationale
│
└── examples/
    ├── technical-passage/      input / diagnostic / output / rationale
    ├── linkedin-post/
    ├── academic-abstract/
    ├── personal-essay/
    └── already-natural/        zero changes — when not to intervene
```

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

---

## Limitations

- The structural signals reflect 2024–2025 model behavior. Models update; Not Ai's thresholds should too.
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
