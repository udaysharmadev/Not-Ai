# Not Ai

**A writing intelligence skill for AI-assisted agents.**

Not Ai transforms AI-generated or AI-assisted prose into writing that is natural, specific, context-aware, and faithful to the author's intended meaning — by addressing the actual structural patterns that make AI writing feel machine-like, not by swapping out banned words.

---

## What Not Ai Is

Not Ai is a cross-agent skill (compatible with Antigravity, Claude Code, Cursor, Codex CLI, and any agent that supports the `SKILL.md` format). It gives your agent the capability to:

- **Diagnose** AI writing patterns with objective structural measurements
- **Rewrite** selectively at the morphosyntactic level, not just the lexical level
- **Preserve** the author's voice and the original meaning
- **Apply** genre-appropriate transformations (LinkedIn ≠ academic abstract ≠ personal essay)
- **Flag** missing specifics rather than inventing them

## What Not Ai Is Not

Not Ai is **not** a detector-bypass tool. It does not optimize for evading AI detectors, gaming perplexity scores, or fooling any specific classifier. Its output is designed to be good writing — by human standards, for human readers — whether or not a detector is involved.

---

## The Problem With Existing Humanizers

Every major humanizer (commercial or open-source) operates at the word level:
1. Scan for AI-associated vocabulary ("delve", "leverage", "furthermore")
2. Substitute synonyms or paraphrase
3. Inject arbitrary sentence length variation
4. Apply a fixed voice template ("casual", "professional", "academic")

This treats the symptoms while leaving the disease. Research shows the actual fingerprint is **morphosyntactic**:

- Instruction-tuned LLMs use present participial clauses at **2–5× the human rate** (Reinhart et al., PNAS 2025)
- Nominalization density runs **1.5–2× the human rate** across all genres
- AI writing clusters in a narrow stylistic region; human writing is diverse
- GPT-4o uses "camaraderie", "palpable", "tapestry" at **100× the human rate**

Replacing words while leaving these structures intact is like changing someone's cologne and calling it a disguise.

Not Ai works at the structural level because that's where the actual difference is.

---

## Architecture

```
not-ai/
├── SKILL.md                    # Core skill — agent loads this first
├── rules/
│   ├── structure.md            # Clause types, nominalization, density (research-backed)
│   ├── voice.md                # Voice profile extraction and application
│   ├── specificity.md          # Generic/abstract language — when and how to address it
│   ├── rhythm.md               # Sentence/paragraph cadence diagnosis
│   ├── rhetoric.md             # Epistemic stance, engagement markers, transitions
│   └── context.md              # Genre profiles: LinkedIn, README, essay, email, etc.
├── scripts/
│   ├── analyze_structure.py    # Deterministic morphosyntactic analyzer
│   ├── repetition.py           # Phrase/opening/structure repetition detector
│   ├── metrics.py              # Readability and density metrics
│   └── benchmark.py            # Pair evaluation for (original, rewritten) texts
├── references/
│   ├── wikipedia-signs.md      # Annotated Wikipedia AI writing signs
│   ├── writing-research.md     # 12+ academic papers, key findings
│   ├── style-research.md       # Structural differences by LLM and genre
│   └── methodology.md          # Design rationale
├── examples/
│   ├── technical-passage/      # Complete before/after with full rationale
│   ├── linkedin-post/
│   ├── academic-abstract/
│   ├── personal-essay/
│   └── already-natural/        # Example where Not Ai changes nothing
└── benchmarks/
    ├── README.md               # How to run
    └── corpus/                 # Public domain benchmark texts
```

---

## Installation

**Antigravity (Google)**
```bash
git clone https://github.com/[username]/not-ai \
  ~/.gemini/antigravity/skills/not-ai
```

**Claude Code**
```bash
git clone https://github.com/[username]/not-ai \
  ~/.claude/skills/not-ai
```

**Project-local (any compatible agent)**
```bash
git clone https://github.com/[username]/not-ai \
  .agents/skills/not-ai
```

The core skill requires **no dependencies**. Python scripts in `scripts/` work with the standard library only (Python 3.8+). No API keys, no external services, no internet required.

---

## Usage

Invoke Not Ai naturally through your agent:

```
Not Ai this: [paste text]
Not Ai --mode diagnose [text or file path]
Not Ai --mode rewrite [text]
Not Ai --mode preserve [text]        # Stricter meaning/voice preservation
Not Ai --mode aggressive [text]      # Stronger structural changes
Not Ai --voice [sample.txt] [text]   # Match to supplied writing sample
```

### Run the scripts directly
```bash
# Structural analysis
python scripts/analyze_structure.py myfile.txt

# Repetition detection
python scripts/repetition.py myfile.txt

# Readability and density metrics
python scripts/metrics.py myfile.txt

# Benchmark a before/after pair
python scripts/benchmark.py --input original.txt --output rewritten.txt

# Verify everything is working
python scripts/benchmark.py --dry-run
```

---

## Pipeline

When invoked, Not Ai executes six stages:

1. **Understand context** — genre, audience, register, intent
2. **Run deterministic analysis** — objective measurements from Python scripts
3. **Produce diagnostic report** — specific findings with examples from the text
4. **Build voice profile** — if a sample was provided
5. **Selective rewrite** — restructure, replace, remove, merge, split, flag (never invent)
6. **Adversarial self-review** — 12-question check on what might have gone wrong

---

## Core Principles

**Operate structurally, not lexically.** Target clause types, density, and rhetorical patterns — not vocabulary.

**Voice is a hard constraint.** Voice preservation is built into the pipeline, not added at the end.

**Never invent.** If specifics are missing, flag them with `[placeholder]`. Do not fabricate facts, anecdotes, emotions, or opinions.

**Human writing is a distribution.** Don't converge toward a single "human-like" target — that creates a new cluster. Target the space of plausible human diversity.

**Selective edits over wholesale rewriting.** Keep what works. Change only what is actually machine-like.

**The right amount of intervention is the minimum that achieves the goal.** If text is already natural, the output is: nothing.

---

## Research Basis

Not Ai's design is grounded in peer-reviewed linguistics research:

| Study | Finding |
|-------|---------|
| Reinhart et al. (PNAS 2025) | Present participial clauses 2–5× elevated; nominalizations 1.5–2× elevated; instruction tuning (RLHF) is the root cause |
| Jiang & Hyland (2025) | LLMs have significantly fewer engagement markers, hedges, and attitude markers in essays |
| StoryScope (2026) | AI stories cluster in a "shared narrative space"; human stories are diverse |
| Milička et al. (2025) | LLMs shift toward information-dense style (Biber Dimension 1) across models |
| Siler (PNAS 2026) | "delve", "underscore", "meticulous" spiking in 7.3M published academic articles post-2022 |
| Ming et al. (2026) | RLHF induces Romance-origin vocabulary bias ("utilize" over "use") |

Full citations and key findings in [`references/writing-research.md`](references/writing-research.md).

---

## Limitations

- The structural fingerprints documented by current research reflect 2024–2025 models. As models update, patterns will shift.
- Cross-language support is limited — research is predominantly English-focused.
- Fine-tuning on genre-specific data can reduce the structural signals (Dawkins et al., 2025) — this means Not Ai's diagnostics may be less sensitive on post-fine-tuned outputs.
- Not Ai cannot verify factual claims. If the original text contains an error, Not Ai preserves it.
- Voice profiles are approximations from short samples.

---

## What Not Ai Will Never Do

- Introduce random errors or typos to "seem human"
- Inject forced slang or contractions inappropriate to the register
- Invent facts, experiences, emotions, or opinions
- Claim to guarantee any detection score
- Reduce writing quality in the name of humanization
- Apply the same intervention to all text regardless of context

---

## License

MIT. See [LICENSE](LICENSE).

---

*Research-driven. Cross-agent compatible. Open source.*
