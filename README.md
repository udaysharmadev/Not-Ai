<div align="center">

<h1>Not Ai</h1>

<p>The only humanizer backed by peer-reviewed linguistics research.</p>

<p>
<em>Every other humanizer swaps words.<br>
Not Ai restructures sentences.</em>
</p>

<br>

[![License: MIT](https://img.shields.io/badge/License-MIT-blue.svg)](LICENSE)
[![Python](https://img.shields.io/badge/Python-3.10%2B-blue?logo=python&logoColor=white)](scripts/)
[![Research-Backed](https://img.shields.io/badge/Research-PNAS%202025-green)](plugins/not-ai/skills/not-ai/SKILL.md)
[![Cross-Agent](https://img.shields.io/badge/Cross--Agent-SKILL.md-purple)](plugins/not-ai/skills/not-ai/SKILL.md)

<br>

> **Not Ai is not a detector-bypass tool.**
> The goal is good writing, by human standards, for human readers.

</div>

---

## Why this exists

Every major humanizer works the same way: find banned words, swap them, optionally paraphrase. The output still reads like AI text because the structure was never touched.

A 2025 PNAS study ([Reinhart et al.](https://arxiv.org/abs/2410.16107)) measured how GPT-4o, Llama 3, and other instruction-tuned models differ from human writers. The differences weren't in vocabulary. They were structural:

- Instruction-tuned LLMs open sentences with present participial clauses at **2.2 to 5.3 times the human rate**
- Nominalization density runs **roughly 2.1x higher** than human writing
- GPT-4o uses words like "camaraderie", "palpable" and "tapestry" at **84 to 171 times the human rate**
- The root cause is instruction tuning. Base Llama 3 models write close to human rates.

**Not Ai operates at that structural level.** It measures clause type distributions, sentence burstiness, nominalization density, rhetorical engagement markers, and epistemic stance, then intervenes selectively.

---

## How it works

### Three passes, not one

1. **Suppress** - Remove the structural patterns that betray AI generation (participial openers, nominalizations, mechanical transitions, copula avoidance)
2. **Re-voice** - Rewrite as if speaking to someone who knows the background. Restore `because`, contractions, existential `there`, sentence-initial `And`/`But`
3. **Count** - Run deterministic measurement scripts. Print counted values before emitting text. If any target misses, revise and recount.

### What gets measured

| Signal | How | Why |
|--------|-----|-----|
| Participial clause openers | Regex on sentence-initial `-ing` | 224-527% of human rate in LLMs |
| Nominalization density | Suffix counting (`-tion`, `-ment`, `-ness`) | 145-214% of human rate |
| Sentence burstiness | Coefficient of variation | Model output typically 3-5, humans 8+ |
| Epistemic stance | Hedge/booster ratio | Models use hedges at 50-63% of human rate |
| Mechanical transitions | Fixed list matching | "Furthermore", "Moreover", etc. |
| AI vocabulary | Research-derived wordlist | Tier 1: 84-171x overrepresentation |
| Syntactic frame repetition | 8 named patterns, consecutive check | Same move in back-to-back sentences |

### Eight genre profiles

A LinkedIn post processed with academic rules becomes worse, not better. Not Ai detects genre first:

| Genre | Key adaptation |
|-------|---------------|
| LinkedIn post | Keep hook opener, contractions, short paragraphs |
| Academic abstract | Keep passive, nominalization, third person |
| Technical docs | Keep imperative, precision, warnings |
| Professional email | Match existing relationship tone |
| Personal essay | First person, hedges, uneven lengths |
| GitHub README | Factual, imperative, no marketing |
| Social media | Very short, fragments normal |
| Fiction/narrative | Shows not tells, sensory detail |

---

## Install

### Claude Code

```bash
claude plugin marketplace add udaysharmadev/Not-Ai && claude plugin install not-ai@not-ai
```

### Codex

```bash
codex plugin marketplace add udaysharmadev/Not-Ai && codex plugin add not-ai@not-ai
```

### Claude Desktop

Upload `plugins/not-ai/skills/not-ai/SKILL.md` directly. It is self-contained.

### Other agents

```bash
git clone https://github.com/udaysharmadev/Not-Ai /tmp/not-ai
cp /tmp/not-ai/plugins/not-ai/skills/not-ai/SKILL.md ~/.claude/skills/not-ai/SKILL.md
```

Works with: Cursor, Windsurf, GitHub Copilot, Aider, ChatGPT, Gemini CLI, and any agent that reads context files.

---

## Usage

```
/not-ai [paste text]                    default rewrite
/not-ai --mode diagnose [text]          report only, no changes
/not-ai --mode preserve [text]          fewest word-level edits
/not-ai --mode aggressive [text]        full structural surgery
/not-ai write [brief]                   write from scratch
```

### Measurement scripts

```bash
python3 scripts/analyze_structure.py input.txt   # structural fingerprint
python3 scripts/repetition.py input.txt          # phrase and pattern repetition
python3 scripts/metrics.py input.txt             # readability, density, stance
python3 scripts/measure.py input.txt             # all three in one pass
```

---

## What makes this different

| | Not Ai | blader/humanizer | Commercial tools |
|---|---|---|---|
| **Approach** | Structural (clause types, burstiness, stance) | Pattern-matching (35 Wikipedia patterns) | Paraphrase engine |
| **Measures before rewriting** | Yes (Python scripts) | No | No |
| **Research basis** | PNAS 2025, Jiang & Hyland 2025 | Wikipedia Signs of AI Writing | Proprietary |
| **Genre-aware** | 8 profiles with red lines | No | Some |
| **Never fabricates** | Hard constraint with bracket placeholders | No explicit constraint | Varies |
| **Pre-output gate** | Counted values printed before text | No | No |
| **Price** | Free, MIT license | Free | $9-20/month |
| **Agent skill** | Yes (Claude, Codex, Cursor, etc.) | Yes | No (SaaS only) |

---

## Architecture

```
INPUT TEXT
    │
    ▼
┌──────────────────────┐
│  Genre Detection     │   8 profiles
└──────────┬───────────┘
           │
           ▼
┌────────────────────────────────────────────┐
│  Deterministic Analysis (Python scripts)   │
│  No LLM. Objective counts.                │
└──────────┬─────────────────────────────────┘
           │
           ▼
┌──────────────────────┐
│  Diagnostic Report   │   patterns with quotes from text
└──────────┬───────────┘
           │
           ▼
┌────────────────────────────────────────────┐
│  Selective Rewrite                         │
│  Suppress → Re-voice → Count               │
│  Never fabricate. Never degrade.           │
└──────────┬─────────────────────────────────┘
           │
           ▼
┌──────────────────────┐
│  Output              │   count line + checks line + text
└──────────────────────┘
```

---

## What Not Ai will not do

- Add random typos to seem human
- Force slang into the wrong register
- Invent memories, emotions, or opinions
- Fabricate facts, citations, or statistics
- Optimize for a detector score
- Rewrite everything when selective edits are enough

---

## Repository structure

```
Not-Ai/
├── plugins/not-ai/
│   ├── .claude-plugin/plugin.json
│   ├── .codex-plugin/plugin.json
│   └── skills/not-ai/
│       ├── SKILL.md              the skill (363 lines)
│       └── reference/
│           ├── profile.md        suppress/restore tables
│           ├── vocabulary.md     Tier 1-4 wordlists
│           ├── mechanical-tells.md
│           ├── why-word-swapping-fails.md
│           └── research-sources.md
│
├── scripts/                      Python measurement tools
├── examples/                     6 worked before/after pairs
├── benchmarks/                   evaluation framework
├── README.md
└── LICENSE
```

---

## Research

| Study | Finding used |
|-------|-------------|
| [Reinhart et al., PNAS 2025](https://arxiv.org/abs/2410.16107) | Present participial rates, nominalization density, instruction tuning as root cause |
| [Jiang & Hyland, 2025](https://www.sciencedirect.com/science/article/pii/S0889490624000978) | Engagement marker deficit, epistemic stance differences |
| [Wikipedia: Signs of AI Writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing) | Copula avoidance, negative parallelism, rule of three, mechanical tells |

---

## Contributing

Most useful contributions:
- Genre profiles for contexts not yet covered
- Before/after benchmark pairs in any genre
- Updated vocabulary lists as new model behavior is documented
- spaCy or NLTK integration for real morphosyntactic parsing

---

## License

MIT. See [LICENSE](LICENSE).

---

<div align="center">
<em>"Remove the machine's generic habits. Preserve the person's voice."</em>
</div>
