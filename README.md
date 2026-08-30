<div align="center">

<h1>Not Ai</h1>

<p><strong>A writing intelligence skill for AI-assisted agents.</strong></p>

<p>
  <em>Not Ai transforms AI-generated prose into natural, specific, voice-consistent writing<br>
  by diagnosing and correcting structural machine-like patterns —<br>
  not by swapping words or gaming a detector.</em>
</p>

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.8%2B-blue?logo=python&logoColor=white)](scripts/)
[![Research-Backed](https://img.shields.io/badge/Research-PNAS%202025-green)](references/writing-research.md)
[![Cross-Agent](https://img.shields.io/badge/Cross--Agent-SKILL.md-purple)](SKILL.md)
[![No Dependencies](https://img.shields.io/badge/Dependencies-None-brightgreen)](scripts/)

<br>

> **Not Ai is not a detector-bypass tool.**
> It is a writing quality layer grounded in peer-reviewed linguistics research.
> A good result should still be good writing even when no detector is involved.

</div>

---

## Table of Contents

- [The Problem](#the-problem)
- [Research Foundation](#research-foundation)
- [Why Existing Humanizers Fail](#why-existing-humanizers-fail)
- [Not Ai's Technical Thesis](#not-ais-technical-thesis)
- [Architecture](#architecture)
- [The Six-Stage Pipeline](#the-six-stage-pipeline)
- [Comparison: Not Ai vs. Everything Else](#comparison-not-ai-vs-everything-else)
- [Installation](#installation)
  - [Antigravity (Google)](#antigravity-google)
  - [Claude Code](#claude-code)
  - [Claude Desktop (MCP)](#claude-desktop-mcp)
  - [Cursor](#cursor)
  - [GitHub Copilot](#github-copilot)
  - [OpenAI Codex CLI](#openai-codex-cli)
  - [Gemini CLI](#gemini-cli)
  - [ChatGPT (Custom GPT / Projects)](#chatgpt-custom-gpt--projects)
  - [Windsurf / Codeium](#windsurf--codeium)
  - [Any Agent (Universal)](#any-agent-universal)
- [Usage](#usage)
- [Deterministic Analysis Scripts](#deterministic-analysis-scripts)
- [Repository Structure](#repository-structure)
- [Core Rules](#core-rules)
- [What Not Ai Explicitly Forbids](#what-not-ai-explicitly-forbids)
- [Benchmark](#benchmark)
- [Examples](#examples)
- [Limitations and Honest Caveats](#limitations-and-honest-caveats)
- [Contributing](#contributing)
- [License](#license)

---

## The Problem

AI-assisted writing is pervasive. The problem is not that AI was involved — it is that AI-generated prose exhibits a recognizable set of structural machine-like patterns that make writing feel:

- **Produced** rather than composed
- **Generic** rather than specific
- **Confident without evidence**, smooth without personality
- **Organized without argument**, technically correct but uncommunicative

These patterns persist across content type, topic, and length. They are not random. They are systematic — and they are measurable.

---

## Research Foundation

Not Ai's design is grounded in peer-reviewed linguistics research, primarily the use of **Biber's 66-feature morphosyntactic tagset** applied to large corpora of human-authored and LLM-generated text.

### Primary Source

**Reinhart et al. (2025), PNAS** — *"Do LLMs write like humans? Variation in grammatical and rhetorical styles"*
> doi:10.1073/pnas.2422455122 · [arXiv:2410.16107](https://arxiv.org/abs/2410.16107)

Method: 12,000 human texts + LLM continuations from GPT-4o, GPT-4o Mini, Llama 3 8B/70B (base and instruction-tuned), analyzed using Biber's tagset. Random forest classifier: **66% accuracy on 7-way classification** (vs. 14% random baseline).

#### Key Findings

| Feature | Human baseline | Instruction-tuned LLMs |
|---------|---------------|------------------------|
| Present participial clause rate | ~5–8% of sentences | **2–5× elevated (15–25%)** |
| Nominalization density | ~25–40 per 1,000 words | **1.5–2× elevated (45–70/1k)** |
| Passive voice (agentless) | ~12–15% of sentences | ~6–8% (GPT-4o *under*uses it) |
| Information density (Biber Dim. 1) | Genre-adapted | **Stays high regardless of genre** |
| Vocabulary cluster | Broad distribution | **Narrow "prestige" cluster** |

**Critical insight**: Base Llama 3 models write at rates close to humans. **Instruction tuning (RLHF) is the root cause.** It is not the training data — it is the reward signal.

### Supporting Research

| Study | Key Finding | Relevance |
|-------|------------|-----------|
| Jiang & Hyland (2025), *English for Specific Purposes* | LLMs have significantly fewer engagement markers, hedges, and attitude markers in essays | Validates `rules/rhetoric.md` |
| StoryScope — Russell et al. (2026) | AI stories cluster in a shared narrative space; Claude=flat escalation, GPT=dream sequences, Gemini=external description | Human writing = distribution, not a target |
| Milička et al. (2025) | All LLMs shift toward Biber Dimension 1 (informational/dense) regardless of genre | Information density as universal fingerprint |
| Siler (2026), *PNAS* | "delve", "underscore", "meticulous", "foster" spiking in 7.3M academic articles post-2022 | Vocabulary signal is real and large-scale |
| Ming et al. (2026), *FLAIRS-39* | RLHF induces Romance-origin vocabulary bias ("utilize">"use", "facilitate">"help") | Explains the prestige-vocabulary over-selection |
| Dawkins et al. (2025) | Genre-specific fine-tuning dramatically reduces Biber feature divergence | Future models will shift; Not Ai must evolve |
| Goulart et al. (2024) | AI texts are more informationally dense and less personally involved than student writing | Validates engagement marker gap |

---

## Why Existing Humanizers Fail

Every major humanizer — commercial or open-source — shares the same fundamental architecture:

```
INPUT → Scan for banned words → Substitute synonyms → Optional paraphrase → OUTPUT
```

This is called **surface-level intervention**. It changes what the text *says at the word level* without changing how the text *is structured at the morphosyntactic level*.

### The Representation Mismatch

Inspired by SurrogatePrompt (arXiv:2309.14122), which shows that safety filters and image generators operate in different representation spaces:

> A prompt can fool a filter operating at the surface level while the underlying generator still produces the same output — because the two components work at different levels of abstraction.

The analogous flaw in humanizers: they optimize against a surface signal (word identity) while the underlying morphosyntactic representation — present participial rates, nominalization density, information density — remains completely unchanged.

```
Humanizer (current):     word1 → word2       (surface level)
                         ↓
                         Structural fingerprint: UNCHANGED

Not Ai:                  word1 → word2       (surface, secondary)
                         clause type dist → restructured  (structural level)
                         nominalization rate → reduced
                         information density → genre-calibrated
                         ↓
                         Structural fingerprint: ADDRESSED
```

### The Humanizer Paradox

Current humanizers create a recognizable "humanizer voice" that is distinct from both raw AI output *and* authentic human writing:

- Same rhythm: short-medium-long cycling
- Same vocabulary substitutions from the same banned-word list
- Same forced contractions and pseudo-casual register
- Same fragment injection for "variety"
- Same structure, different words

**This "synthetic naturalness" is now itself a detectable pattern.**

### Comparison with Open-Source Skills

| Tool | Primary approach | Voice model | Genre-aware | Structural analysis | Research basis |
|------|-----------------|-------------|-------------|--------------------|----|
| [blader/humanizer](https://github.com/blader/humanizer) | Wikipedia AI tells → remove | Sample-based | No | No | Wikipedia article |
| [Aboudjem/humanizer-skill](https://github.com/Aboudjem/humanizer-skill) | 55 patterns → remove/replace | 5 fixed templates | No | No | Wikipedia article |
| [harshaneel/humanize](https://github.com/harshaneel/humanize) | LLM rewrite | None | No | No | Unspecified |
| numen-tech/slopornot | Multi-pass LLM rewrite | None | No | No | Wikipedia article |
| **Not Ai** | Biber-feature structural analysis + selective intervention | Author-extracted (10 dimensions) | Yes (8 genres) | Yes (4 Python scripts) | 12+ peer-reviewed papers |

---

## Not Ai's Technical Thesis

> **Existing humanizers remove surface-level AI signals while leaving the underlying morphosyntactic and rhetorical fingerprint intact. Not Ai operates at the structural level: it diagnoses and selectively restructures information density, clause type distribution, stance marker frequency, rhetorical engagement, and narrative pattern — the actual features research identifies as distinguishing human from LLM writing across all registers — rather than swapping words or removing banned phrases. It treats human writing as a distribution of diverse styles, not a single target, and preserves voice, genre, and meaning as hard constraints throughout.**

Three consequences:

1. **Not Ai does not converge toward a fixed "human-like" target** — it moves the text toward the diverse space of plausible human writing for this genre, register, and author
2. **Not Ai's output diversity increases** rather than collapsing toward a new cluster
3. **Not Ai is honest about what it cannot do** — it flags missing specifics rather than inventing them

---

## Architecture

```
┌──────────────────────────────────────────────────────────────────┐
│                        NOT AI PIPELINE                           │
├──────────────────────────────────────────────────────────────────┤
│                                                                  │
│  INPUT TEXT                                                      │
│       │                                                          │
│       ▼                                                          │
│  ┌─────────────────────┐                                         │
│  │  Stage 0: Context   │ ← genre / audience / register / intent  │
│  │  Identification     │                                         │
│  └──────────┬──────────┘                                         │
│             │  loads: rules/context.md                           │
│             ▼                                                    │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Stage 1: Deterministic Analysis (Python scripts)       │     │
│  │                                                         │     │
│  │  analyze_structure.py ──┐                               │     │
│  │  repetition.py  ────────┼──► JSON report                │     │
│  │  metrics.py  ───────────┘                               │     │
│  │                                                         │     │
│  │  Measures: burstiness, participial rate, nominalization │     │
│  │  density, transition frequency, AI vocabulary, passive  │     │
│  │  rate, FK grade, Gunning Fog, engagement markers        │     │
│  └──────────┬──────────────────────────────────────────────┘     │
│             │                                                    │
│             ▼                                                    │
│  ┌─────────────────────┐                                         │
│  │  Stage 2: Diagnostic│ ← specific findings with text examples  │
│  │  Report             │   not vague summaries                   │
│  └──────────┬──────────┘                                         │
│             │                                                    │
│             ▼                                                    │
│  ┌─────────────────────┐   (only if --voice flag)                │
│  │  Stage 3: Voice     │ ← 10-dimension profile extraction:      │
│  │  Profile            │   sentence length dist, punctuation,    │
│  └──────────┬──────────┘   contractions, hedging ratio,          │
│             │              formality, reader address...           │
│             ▼                                                    │
│  ┌─────────────────────────────────────────────────────────┐     │
│  │  Stage 4: Selective Rewrite (skip if --mode diagnose)   │     │
│  │                                                         │     │
│  │  Rules loaded based on diagnostic:                      │     │
│  │  structure.md / rhythm.md / rhetoric.md                 │     │
│  │  specificity.md / voice.md / context.md                 │     │
│  │                                                         │     │
│  │  Per-sentence actions:                                  │     │
│  │  KEEP │ RESTRUCTURE │ REPLACE │ REMOVE │ MERGE │        │     │
│  │  SPLIT │ MOVE │ FLAG                                    │     │
│  │                                                         │     │
│  │  Hard constraints: voice profile + genre rules           │     │
│  └──────────┬──────────────────────────────────────────────┘     │
│             │                                                    │
│             ▼                                                    │
│  ┌─────────────────────┐                                         │
│  │  Stage 5: Adversarial│ ← 12-question self-review:            │
│  │  Self-Review         │   over-edit? voice lost? invented?     │
│  └──────────┬──────────┘   new mechanical pattern? etc.          │
│             │                                                    │
│             ▼                                                    │
│  ┌─────────────────────┐                                         │
│  │  Stage 6: Output    │ ← diagnostic + rewritten text +         │
│  │                     │   change rationale (transparency)        │
│  └─────────────────────┘                                         │
│                                                                  │
└──────────────────────────────────────────────────────────────────┘
```

### Intervention Decision Tree

```
For each sentence:
       │
       ├─ Is it already natural? ────────────────────────────► KEEP
       │
       ├─ Does it have a structural problem?
       │     ├─ Clause arrangement ──────────────────────────► RESTRUCTURE
       │     ├─ Word choice with no semantic loss ───────────► REPLACE
       │     └─ Information density too high ────────────────► SPLIT
       │
       ├─ Does it add no value? ────────────────────────────► REMOVE
       │
       ├─ Is it better as one with the adjacent sentence? ──► MERGE
       │
       ├─ Would it flow better elsewhere? ──────────────────► MOVE
       │
       └─ Does it need a specific detail Not Ai cannot supply? ► FLAG [placeholder]
                                                                  (NEVER invent)
```

---

## The Six-Stage Pipeline

### Stage 0 — Context Identification

Before touching the text, Not Ai determines:

| Dimension | What it determines |
|-----------|-------------------|
| **Genre** | LinkedIn / README / academic abstract / personal essay / email / docs / social media / narrative |
| **Register** | Formal / professional / neutral / conversational / casual / technical |
| **Audience** | Expert / informed non-expert / general / novice |
| **Relationship** | Colleague / employer / client / friend / community |
| **Intent** | Inform / persuade / connect / explain / entertain |

Wrong context = wrong intervention. A README processed as a personal essay would be wrecked. A personal essay processed as technical documentation would be sterilized.

### Stage 1 — Deterministic Analysis

**No LLM guessing. Objective measurements from Python scripts.**

The scripts measure what Reinhart et al. measured — the same Biber-category features the PNAS study used to achieve 66% 7-way classification accuracy:

```bash
python3 scripts/analyze_structure.py input.txt
python3 scripts/repetition.py input.txt
python3 scripts/metrics.py input.txt
```

Metrics computed:
- Sentence length distribution (mean, std, burstiness coefficient)
- Present participial clause opener rate
- Nominalization density (per 1,000 words)
- Mechanical transition word frequency
- AI-associated vocabulary with context notes
- Passive voice estimate
- Repeated n-grams and sentence openings
- Paragraph structural shape distribution
- Flesch-Kincaid Grade, Gunning Fog, Reading Ease
- Information density proxy
- Epistemic stance markers (hedges vs. boosters)
- Engagement markers (questions, reader address, first-person)

### Stage 2 — Diagnostic Report

**Specific, not vague.** The diagnostic names the exact patterns found and quotes from the text:

```
NOT AI DIAGNOSTIC
─────────────────────────────
Genre detected:        Technical explanation
Register:              Professional/neutral
Overall quality:       51/100
Meaning preservation:  low risk

Strengths:
  ✓ Accurate technical content
  ✓ Logical structure

Structural patterns to address:
  • Present participials: 4 in 4 paragraphs (25% — 3-5x human baseline)
    — "By leveraging the power of", "By thoughtfully implementing"
  • Nominalization overload: 91.3/1,000 words (human norm: 25-40)
    — "implementations", "invalidation", "consideration"
  • Mechanical transitions: "Furthermore", "In conclusion",
    "It is worth noting", "In the realm of"

Vocabulary signals (in context):
  • "pivotal", "fundamentally transforms", "leveraging", "indispensable"
  • Inflated significance — text doesn't support these claims

Recommended intervention: Moderate
```

### Stage 3 — Voice Profile

When `--voice sample.txt` is provided, a 10-dimension profile is extracted:

| Dimension | What's measured |
|-----------|----------------|
| Sentence length | Mean, std — `tight` / `expansive` / `variable` |
| Paragraph length | Mean sentences per paragraph |
| Punctuation | Em-dash, parentheticals, semicolons, ellipsis |
| Contractions | Rate per 1,000 words |
| First-person | Frequency — `absent` / `occasional` / `central` |
| Hedging balance | Hedge vs. booster ratio — `cautious` / `assertive` / `calibrated` |
| Formality | 1–5 scale |
| Reader address | Uses "you" / "we"? |
| Example density | Concrete examples rate |
| Emotional intensity | `flat` / `measured` / `engaged` / `passionate` |

### Stage 4 — Selective Rewrite

Valid actions per sentence: `KEEP` · `RESTRUCTURE` · `REPLACE` · `REMOVE` · `MERGE` · `SPLIT` · `MOVE` · `FLAG`

Mode constraints:
- `--mode preserve`: only `RESTRUCTURE` and light `REPLACE`
- `--mode rewrite` (default): judgment-driven
- `--mode aggressive`: all actions available freely
- `--mode diagnose`: skip Stage 4 entirely

### Stage 5 — Adversarial Self-Review

12-question self-check after completing the rewrite:

1. What still sounds generic?
2. What sounds like a template?
3. Where did I over-edit?
4. Where did I remove personality?
5. Where did I introduce fake personality?
6. Did I invent anything?
7. Did I change the author's position on anything?
8. Did I make every paragraph equally polished? (Don't — humans don't)
9. Does this now have its own mechanical rhythm?
10. Does this still sound like the same person?
11. Would a human actually choose these words here?
12. Does this now sound like "humanizer writing" rather than the author?

### Stage 6 — Output

1. The diagnostic report
2. The rewritten text (if applicable)
3. Change rationale — what changed and why, for transparency

---

## Comparison: Not Ai vs. Everything Else

### vs. Commercial Humanizers

| Feature | Undetectable AI | WriteHuman | QuillBot | HIX Bypass | **Not Ai** |
|---------|----------------|-----------|----------|-----------|-----------|
| Approach | Word substitution | Paraphrase | Paraphrase modes | Multi-pass rewrite | Morphosyntactic structural analysis |
| Voice preservation | ✗ | ✗ | ✗ | ✗ | ✓ Author-extracted profile |
| Genre awareness | ✗ | ✗ | ✗ | ✗ | ✓ 8 genre profiles |
| Structural analysis | ✗ | ✗ | ✗ | ✗ | ✓ Biber-feature measurement |
| Fabrication prevention | ✗ | ✗ | ✗ | ✗ | ✓ Explicit prohibition + flagging |
| Diagnostic report | ✗ | ✗ | ✗ | ✗ | ✓ Specific with text examples |
| Research basis | Marketing claims | Marketing claims | Marketing claims | Marketing claims | 12+ peer-reviewed papers |
| Open source | ✗ | ✗ | ✗ | ✗ | ✓ MIT |
| API/subscription required | Yes | Yes | Yes (free tier) | Yes | ✗ None |
| Meaning preservation check | ✗ | ✗ | ✗ | ✗ | ✓ Number preservation + semantic similarity |
| Convergence to "humanizer voice" | ✓ | ✓ | ✓ | ✓ | ✗ Explicitly prevented |

### vs. Open-Source Humanizer Skills

| Feature | blader/humanizer | Aboudjem/humanizer-skill | harshaneel/humanize | **Not Ai** |
|---------|-----------------|--------------------------|---------------------|-----------|
| Signal level | Lexical | Lexical | Lexical | **Morphosyntactic + rhetorical** |
| Structural diagnosis | ✗ | ✗ | ✗ | ✓ |
| Voice extraction | Sample-based (basic) | 5 fixed templates | ✗ | ✓ 10-dimension profile |
| Genre profiles | ✗ | ✗ | ✗ | ✓ 8 profiles |
| Deterministic scripts | ✗ | ✗ | ✗ | ✓ 4 Python scripts |
| Adversarial self-review | ✗ | ✗ | ✗ | ✓ 12-question |
| Research foundation | Wikipedia article | Wikipedia article | Unspecified | ✓ PNAS 2025, Jiang & Hyland, StoryScope |
| Fabrication prevention | ✗ | ✗ | ✗ | ✓ |
| Benchmark framework | ✗ | ✗ | ✗ | ✓ |
| Examples with rationale | ✗ | ✗ | ✗ | ✓ 5 examples |

### What Not Ai Uniquely Addresses

| Capability | How |
|-----------|-----|
| Present participial overuse detection | Python regex + rate comparison vs. human baseline from Reinhart et al. |
| Nominalization density measurement | Suffix-based detection, rate per 1,000 words |
| Sentence burstiness coefficient | Coefficient of variation of sentence lengths |
| Engagement marker deficit | Count questions, reader address, first-person in output vs. input |
| Epistemic stance calibration | Hedge vs. booster ratio measurement |
| Paragraph structural monotony | Shape distribution analysis |
| Author voice profile (10 dimensions) | Extracted from any writing sample |
| Adversarial self-review | Post-rewrite 12-question quality check |
| Meaning-preserving benchmark | Number preservation + token overlap + structural delta |

---

## Installation

Not Ai follows the **SKILL.md** format — a filesystem-based, agent-agnostic skill standard. Once installed, your agent reads `SKILL.md` and the skill activates.

### Antigravity (Google)

```bash
# Global install (available in all projects)
git clone https://github.com/udaysharmadev/Not-Ai \
  ~/.gemini/antigravity/skills/not-ai

# Or project-local
git clone https://github.com/udaysharmadev/Not-Ai \
  .gemini/skills/not-ai
```

Trigger in chat: `Not Ai this`, `Not Ai --mode diagnose`, `Not Ai --voice sample.txt`

---

### Claude Code

```bash
# Global (~/.claude/skills/ or ~/.claude/commands/)
git clone https://github.com/udaysharmadev/Not-Ai \
  ~/.claude/skills/not-ai

# Project-local (.claude/skills/ in project root)
git clone https://github.com/udaysharmadev/Not-Ai \
  .claude/skills/not-ai
```

Claude Code reads `SKILL.md` files in its skills directories at startup. After installation, use:

```
/not-ai this: [your text]
Not Ai --mode diagnose [text]
Not Ai --voice [sample_file] [text]
```

---

### Claude Desktop (MCP)

For Claude Desktop without Claude Code, use as a prompt attachment:

1. Clone the repo: `git clone https://github.com/udaysharmadev/Not-Ai`
2. In Claude Desktop, start a Project
3. Add `SKILL.md` and the relevant `rules/` files to Project Knowledge
4. Invoke by typing: `Using the Not Ai skill, diagnose and rewrite the following...`

For automated use, configure an MCP server that reads the SKILL.md and exposes it as a tool via the Model Context Protocol.

---

### Cursor

```bash
# Place in .cursor/rules/ (Cursor reads .mdc and .md files here)
mkdir -p .cursor/rules
cp -r path/to/Not-Ai/rules/ .cursor/rules/not-ai-rules/
cp path/to/Not-Ai/SKILL.md .cursor/rules/not-ai.mdc
```

Or clone the full skill:

```bash
git clone https://github.com/udaysharmadev/Not-Ai \
  .cursor/skills/not-ai
```

In Cursor chat: `@not-ai humanize this text`, or reference `SKILL.md` directly in your prompt.

---

### GitHub Copilot

Copilot does not natively load `SKILL.md` files. To use Not Ai with Copilot:

**Option A — Copilot Instructions file** (`.github/copilot-instructions.md`):
```bash
cat path/to/Not-Ai/SKILL.md >> .github/copilot-instructions.md
```

**Option B — Copilot Chat custom prompt**:
Paste the content of `SKILL.md` as a system message in Copilot Chat, then send your text.

**Option C — VS Code Extension**:
Use the [Copilot Extensions](https://github.com/features/copilot/extensions) API to wrap Not Ai as an extension. The `SKILL.md` serves as the extension's system prompt.

---

### OpenAI Codex CLI

```bash
# Clone to Codex skill directory
git clone https://github.com/udaysharmadev/Not-Ai \
  ~/.codex/skills/not-ai

# Or add to AGENTS.md in your project
cat path/to/Not-Ai/SKILL.md >> AGENTS.md
```

Invoke in Codex CLI:
```bash
codex "Not Ai this text: [paste text]"
codex "Not Ai --mode diagnose: [paste text]"
```

---

### Gemini CLI

```bash
# Via Antigravity (Google's Gemini CLI)
git clone https://github.com/udaysharmadev/Not-Ai \
  ~/.gemini/antigravity/skills/not-ai

# Or project-local
mkdir -p .gemini/skills
git clone https://github.com/udaysharmadev/Not-Ai \
  .gemini/skills/not-ai
```

The Gemini CLI (Antigravity) reads skills from both `~/.gemini/antigravity/skills/` (global) and `.gemini/skills/` (project-local). The `SKILL.md` frontmatter (`name:`, `description:`) is read at startup for fast matching; the full file is loaded when the skill is invoked.

---

### ChatGPT (Custom GPT / Projects)

**Custom GPT**:
1. Go to [ChatGPT → Explore GPTs → Create](https://chatgpt.com/gpts/editor)
2. In the **Instructions** field, paste the contents of `SKILL.md`
3. Upload the `rules/` files as Knowledge files
4. Name: "Not Ai — Writing Intelligence"
5. Description: "Transform AI-generated prose into natural, voice-consistent writing"

**ChatGPT Projects**:
1. Create a new Project
2. Add `SKILL.md` and key `rules/` files as Project Files
3. Set the custom instructions to reference Not Ai

**ChatGPT API (system prompt)**:
```python
import openai

with open("SKILL.md") as f:
    skill_prompt = f.read()

response = openai.chat.completions.create(
    model="gpt-4o",
    messages=[
        {"role": "system", "content": skill_prompt},
        {"role": "user", "content": f"Not Ai this:\n\n{your_text}"}
    ]
)
```

---

### Windsurf / Codeium

```bash
# Windsurf reads .windsurfrules and skill files
cp path/to/Not-Ai/SKILL.md .windsurfrules

# Or full install
git clone https://github.com/udaysharmadev/Not-Ai \
  .windsurf/skills/not-ai
```

In Windsurf Chat: `@not-ai` or simply trigger with `Not Ai this:`.

---

### Aider

```bash
# Add SKILL.md to your aider read-only context
aider --read path/to/Not-Ai/SKILL.md --read path/to/Not-Ai/rules/

# Or add to .aider.conf.yml
cat >> .aider.conf.yml << 'EOF'
read:
  - path/to/Not-Ai/SKILL.md
  - path/to/Not-Ai/rules/structure.md
  - path/to/Not-Ai/rules/rhetoric.md
EOF
```

---

### Any Agent (Universal)

Not Ai follows the universal **SKILL.md** skill format. For any agent that loads context files:

1. Point the agent at `SKILL.md` as a system/context file
2. Optionally add `rules/` files for deeper guidance
3. Trigger with: `Not Ai this`, `Not Ai --mode diagnose`, or `humanize this text`

For agents that use `AGENTS.md`:
```bash
cat path/to/Not-Ai/SKILL.md >> AGENTS.md
```

---

## Usage

### Basic Humanization

```
Not Ai this: [paste your text here]
```

### Analysis Only (no rewrite)

```
Not Ai --mode diagnose [text or file path]
```

### Strict Meaning/Voice Preservation

```
Not Ai --mode preserve [text]
```

Use this when you want structural improvements but minimal changes to the actual wording. Only `RESTRUCTURE` and light `REPLACE` operations are permitted.

### Stronger Structural Changes

```
Not Ai --mode aggressive [text]
```

All rewrite operations available: `REMOVE`, `MERGE`, `SPLIT`, `MOVE` used freely.

### Match to Your Voice

```
Not Ai --voice my-writing-sample.txt [text to humanize]
```

Extracts a 10-dimension voice profile from your sample and applies it as a hard constraint throughout the rewrite.

---

## Deterministic Analysis Scripts

**No LLM required. No API keys. No internet. Pure Python 3 stdlib.**

### analyze_structure.py

Measures the primary structural fingerprints:

```bash
python3 scripts/analyze_structure.py input.txt

# Example output:
NOT AI — STRUCTURAL ANALYSIS
────────────────────────────────────────
Words: 263  |  Sentences: 12  |  Paragraphs: 7

SENTENCE RHYTHM
  Mean length:   21.9 words
  Std deviation: 11.7 words  (burstiness: 0.533)
  Very short (<8):  1  |  Short (8-15): 4  |  Medium (16-25): 4

STRUCTURAL SIGNALS
  ✓ Participial clause openers: 0 / 12 sentences (0%) — normal
  ⚠ Nominalization density: 91.3 per 1,000 words — high (AI-like)
  ⚠ Mechanical transitions: 4 instances — furthermore, in conclusion...

AI-ASSOCIATED VOCABULARY
  • 'leveraging': 1x
  • 'crucial': 1x
  • 'pivotal': 1x
```

### repetition.py

Detects repeated phrases, sentence openings, and structural patterns:

```bash
python3 scripts/repetition.py input.txt
```

Measures: repeated 3–5-grams, repeated sentence openings (2 and 3-word), paragraph shape distribution, transition phrase repetition, lexical diversity (type-token ratio).

### metrics.py

Readability and tone analysis:

```bash
python3 scripts/metrics.py input.txt
```

Measures: Flesch-Kincaid Grade, Gunning Fog Index, Flesch Reading Ease, information density proxy, epistemic stance (hedge vs. booster counts and rates), engagement markers.

### benchmark.py

Evaluate a (original, rewritten) pair:

```bash
# Single pair
python3 scripts/benchmark.py --input original.txt --output rewritten.txt

# All pairs in a corpus directory
python3 scripts/benchmark.py --corpus benchmarks/corpus/

# Verify everything is working
python3 scripts/benchmark.py --dry-run

# JSON output for automation
python3 scripts/benchmark.py --corpus benchmarks/corpus/ --json > results.json
```

Metrics: semantic similarity (token overlap), number preservation, word count delta, structural delta across all 4 dimensions, readability delta, AI vocabulary reduction.

### JSON output for integration

```bash
python3 scripts/analyze_structure.py input.txt --json
python3 scripts/metrics.py input.txt --json
```

Pipe the JSON into your own tools, workflows, or pre-commit hooks.

---

## Repository Structure

```
not-ai/
├── SKILL.md                    # Core skill — agent loads this first
│                               # ~60 lines, fast to load, progressive disclosure
├── README.md                   # This file
├── LICENSE                     # MIT
├── .gitignore
│
├── rules/                      # Detailed rule files (loaded on demand)
│   ├── structure.md            # Clause types, nominalization, density
│   │                           # Based on: Reinhart et al. PNAS 2025
│   ├── voice.md                # 10-dimension voice profile system
│   ├── specificity.md          # Generic vs. specific — with evidence constraint
│   ├── rhythm.md               # Sentence/paragraph cadence diagnosis
│   ├── rhetoric.md             # Epistemic stance, engagement, transitions
│   │                           # Based on: Jiang & Hyland 2025
│   └── context.md              # 8 genre profiles with specific AI patterns
│
├── scripts/                    # Deterministic analyzers (Python 3, stdlib only)
│   ├── analyze_structure.py    # Primary structural fingerprint analyzer
│   ├── repetition.py           # Phrase/opening/structure repetition
│   ├── metrics.py              # Readability + density + stance metrics
│   └── benchmark.py            # Pair evaluation framework
│
├── references/                 # Research documentation
│   ├── wikipedia-signs.md      # Annotated AI writing signs (11 categories)
│   ├── writing-research.md     # 12+ papers with findings and relevance notes
│   ├── style-research.md       # Measured structural differences by LLM/genre
│   └── methodology.md          # Design rationale — why this approach, not others
│
├── examples/                   # Before/after examples with full rationale
│   ├── technical-passage/      # input.md / diagnostic.md / output.md / rationale.md
│   ├── linkedin-post/          # Generic → specific with placeholders
│   ├── academic-abstract/      # Preserves formal register, removes inflation
│   ├── personal-essay/         # Voice restoration from sparse notes
│   └── already-natural/        # Zero changes — when not to intervene
│
└── benchmarks/
    ├── README.md               # How to run and interpret
    └── corpus/                 # Add your own (original.txt, rewritten.txt) pairs
```

---

## Core Rules

Each rule file is loaded **on demand** — only when the diagnostic identifies a relevant issue. This keeps context consumption minimal.

| Rule file | What it addresses | Research basis |
|-----------|------------------|----------------|
| [`rules/structure.md`](rules/structure.md) | Present participial clauses, nominalization, 'that'-clause subjects, information density, paragraph monotony | Reinhart et al. PNAS 2025 |
| [`rules/voice.md`](rules/voice.md) | 10-dimension voice profile extraction and application | — |
| [`rules/specificity.md`](rules/specificity.md) | Inflated significance, vague quantification, anonymous authority, generic examples | Wikipedia AI signs |
| [`rules/rhythm.md`](rules/rhythm.md) | Sentence length uniformity, opening repetition, transition overload, paragraph shape | Biber dimension analysis |
| [`rules/rhetoric.md`](rules/rhetoric.md) | Epistemic stance, engagement markers, attitude markers, formulaic transitions, repetitive summaries, tricolons | Jiang & Hyland 2025 |
| [`rules/context.md`](rules/context.md) | 8 genre profiles: LinkedIn, GitHub README, academic abstract, personal essay, professional email, technical docs, social media, narrative | — |

---

## What Not Ai Explicitly Forbids

Not Ai is opinionated about what it will never do, regardless of mode or instructions:

| Forbidden action | Why |
|-----------------|-----|
| Random typos as "humanization" | Humans aren't defined by errors |
| Forced slang inappropriate to register | Register is a property of context, not of "humanness" |
| Invented memories, emotions, or opinions | Fake humanity is still falsehood |
| Fabricated facts, citations, or credentials | Never |
| Deliberate grammatical mistakes | Human writing is not bad writing |
| Forcing first-person where author uses third | That changes the voice |
| Excessive contractions to signal informality | Contractions are a habit, not a universal human trait |
| Optimizing for a specific detector score | Not the goal |
| Wholesale rewriting when selective edits suffice | Over-editing is a failure mode |
| Ignoring genre when applying interventions | A README is not a personal essay |

---

## Benchmark

### Running Your Own Benchmark

```bash
# Corpus structure
benchmarks/corpus/
├── my-example/
│   ├── original.txt      # AI-generated text
│   ├── rewritten.txt     # Not Ai output
│   └── metadata.json     # Optional: genre, source model, mode
└── another-example/
    ├── original.txt
    └── rewritten.txt

# Run
python3 scripts/benchmark.py --corpus benchmarks/corpus/
```

### Benchmark Metrics Explained

| Metric | What it tells you | What's healthy |
|--------|------------------|----------------|
| Semantic similarity | Was meaning preserved? | > 0.55 (token overlap) |
| Number preservation | Were specific facts kept? | 100% ideally |
| Word count change | Did text grow significantly? | ±15% |
| Burstiness delta | Did sentence variation improve? | Positive |
| Participial rate delta | Did participial overuse reduce? | Negative |
| Nominalization delta | Did density reduce? | Negative |
| FK grade delta | Did readability improve? | Lower is more accessible |
| AI vocabulary delta | Were AI-associated terms reduced? | Negative |

### Integrity Rule

> **Do not fabricate scores. All benchmark numbers must come from running the script on real (original, rewritten) pairs.**

---

## Examples

### Technical Passage

**Before** (AI-generated):
> "In the realm of modern software architecture, caching represents a pivotal mechanism that fundamentally transforms how applications manage and retrieve data. By leveraging the power of temporary storage solutions, systems can significantly enhance their overall performance metrics..."

**After** (Not Ai):
> "Caching is how you avoid doing the same work twice. When a user requests data, the system checks the cache first. If the data is there, it skips the database entirely. If not, it fetches, stores it in the cache, and serves it."

**Changes**: Removed "In the realm of", "pivotal mechanism that fundamentally transforms", "leveraging the power of", participial opener. Restored direct technical explanation. FK grade: 16.9 → 8.1. Nominalization: 91.3/1k → 22.4/1k.

→ Full example: [examples/technical-passage/](examples/technical-passage/)

### Already Natural — Zero Changes

Not Ai explicitly detects when text is already natural and makes no changes:

> "I spent three days last month hunting a bug that only showed up under load. The issue was in how we handled connection timeouts — specifically, a race condition between the health check and the reconnection logic."

Diagnostic: **91/100. Recommended intervention: None.**

→ Full example: [examples/already-natural/](examples/already-natural/)

---

## Limitations and Honest Caveats

Not Ai does not make claims it cannot support.

| Limitation | Detail |
|-----------|--------|
| **Structural fingerprints change** | Research reflects 2024–2025 models. As models update, Not Ai's thresholds must be updated too. |
| **Fine-tuning reduces signals** | Dawkins et al. (2025) showed genre-specific fine-tuning can dramatically reduce Biber feature divergence. Future models may show smaller differences. |
| **Semantic similarity is a proxy** | Token overlap ≠ semantic equivalence. For production, use embedding-based similarity. |
| **Genre detection is imperfect** | Auto-detected genre should be confirmed by the user. |
| **Voice profiles need sufficient samples** | A 50-word sample gives an approximate profile. 500+ words gives a reliable one. |
| **Fact-checking is out of scope** | Not Ai preserves factual errors if they exist in the original. |
| **English-first** | Research is predominantly English. Cross-language behavior may differ significantly. |
| **No guaranteed detection bypass** | None claimed. The goal is writing quality, not gaming a classifier. |

---

## Contributing

Contributions welcome. Areas that would most benefit from help:

- **Additional genre profiles** in `rules/context.md`
- **Updated AI vocabulary lists** as new models are released
- **New benchmark corpus pairs** (original + rewritten, any genre)
- **Cross-language rule files** (the framework is language-agnostic; the research is English-centric)
- **spaCy / NLTK integration** for `analyze_structure.py` to replace regex-based proxies with proper morphosyntactic parsing
- **Sentence-transformer integration** for `benchmark.py` to replace token-overlap similarity with embedding-based semantic similarity
- **New research findings** as the linguistics literature evolves

Please read [`references/methodology.md`](references/methodology.md) before contributing rules — all interventions must have a research rationale, not just intuition or convention.

---

## Research Citations

If you use Not Ai or its methodology in your work:

```
Reinhart, A., et al. (2025). Do LLMs write like humans? Variation in grammatical
and rhetorical styles. PNAS, 122(8), e2422455122. doi:10.1073/pnas.2422455122

Jiang, F., & Hyland, K. (2025). Rhetorical distinctions: Comparing metadiscourse
in essays by ChatGPT and students. English for Specific Purposes, 79, 17–29.

Russell, J., et al. (2026). StoryScope: Investigating idiosyncrasies in AI fiction.
arXiv:2604.03136.

Siler, K. (2026). The diffusion of large language models in published academic
articles. PNAS, 123(22), e2605754123.
```

Full bibliography: [`references/writing-research.md`](references/writing-research.md)

---

## License

MIT — see [LICENSE](LICENSE).

---

<div align="center">

**Not Ai** · Research-driven · Cross-agent · No dependencies · Open source

*"Remove the machine's generic habits. Preserve the person's voice."*

</div>
