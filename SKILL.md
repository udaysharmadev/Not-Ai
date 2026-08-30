---
name: not-ai
description: Writing intelligence skill. Transforms AI-assisted drafts into natural, specific, voice-consistent prose by diagnosing and correcting structural machine-like patterns. Does NOT optimize for detector bypass. Invoke when asked to humanize text, diagnose AI writing, or make prose more natural. Triggers: "Not Ai this", "humanize", "make this sound human", "not-ai", "--mode diagnose|rewrite|preserve|aggressive", "--voice".
---

# Not Ai

**Not Ai** is a writing intelligence layer. Its goal is not to hide that a machine was involved — it is to remove the machine's generic habits, restore specificity and voice, and produce writing appropriate to its audience and context.

## Core Philosophy

> Do not hide the machine. Remove the machine's generic habits.
> Preserve the person's meaning. Preserve the person's voice.
> Add specificity only when evidence exists in the source text.
> Respect context. Respect genre. Preserve truth.
> Prefer selective edits over rewriting everything.
> Optimize for human readers, not a detector.

**Never invent**: no fabricated anecdotes, facts, credentials, emotions, experiences, or opinions. Human-sounding fiction is still falsehood.

**Never "write worse"**: human writing is not synonymous with bad grammar, typos, or forced slang.

## Invocation

```
Not Ai this [text or file]
Not Ai --mode diagnose [text]       # Report only, no rewrite
Not Ai --mode rewrite [text]        # Full humanization
Not Ai --mode preserve [text]       # Strict meaning/voice preservation
Not Ai --mode aggressive [text]     # Stronger structural changes
Not Ai --voice [sample] [text]      # Match voice to supplied sample
```

## Pipeline

When invoked, execute these stages **in sequence**:

### Stage 0 — Understand Context
Before touching the text, determine:
- **Who is writing?** (infer or ask)
- **Who is reading?** (infer from content and user context)
- **What is the genre?** (LinkedIn post / README / academic abstract / email / essay / documentation / social media / other)
- **What is the register?** (formal / professional / conversational / casual / technical)
- **What is the intent?** (inform / persuade / connect / explain / entertain)
- **What relationship exists between writer and reader?**

Load `rules/context.md` for genre profiles.

### Stage 1 — Run Deterministic Analysis
If Python is available, run:
```bash
python scripts/analyze_structure.py [input_file]
python scripts/repetition.py [input_file]
python scripts/metrics.py [input_file]
```
Parse the JSON output. This gives you objective measurements to interpret — do not rely on LLM intuition alone for countable patterns.

If scripts are unavailable, perform manual analysis of:
- Sentence length distribution (are all sentences 20–25 words?)
- Paragraph length uniformity (are all paragraphs the same size?)
- Opening word repetition (do multiple sentences start with the same word?)
- Transition word density ("Furthermore", "Moreover", "Additionally", "In conclusion")
- Nominalization density (words ending in -tion, -ment, -ness, -ity per paragraph)
- Present participle clause rate ("Building on this", "Leveraging the power of")
- Generic AI vocabulary hits (see `references/wikipedia-signs.md` for list with context)

### Stage 2 — Produce Diagnostic Report (always, even in rewrite mode)

Format:
```
NOT AI DIAGNOSTIC
─────────────────────────────
Genre detected:        [genre]
Register:              [register]
Overall quality:       [n]/100
Voice consistency:     [n]/100
Meaning preservation:  [risk level: low/medium/high]

Strengths:
  ✓ [specific strength]
  ✓ [specific strength]

Structural patterns to address:
  • [specific pattern with example from text]
  • [specific pattern with example from text]

Vocabulary signals (in context):
  • [specific word/phrase — note whether it's genuinely a problem here]

Recommended intervention: [None / Light / Moderate / Heavy]
```

**Critical rule**: A sign is not automatically the underlying problem. Do not flag "delve" as a problem if the surrounding text is otherwise natural. Flag it only if it signals a deeper issue — inflated register, false formality, borrowed prestige vocabulary.

### Stage 3 — Voice Profile (if --voice flag or sample provided)

Build a voice profile from the sample. Load `rules/voice.md` for the procedure. Extract:
- Sentence length distribution (mean, std)
- Paragraph length distribution
- Punctuation habits (em-dash frequency, parenthetical use, colon use)
- Contraction rate
- First-person frequency
- Hedging vs. certainty ratio
- Formality markers
- Question usage
- Vocabulary level

Apply this profile as a constraint throughout Stage 4.

### Stage 4 — Selective Rewrite (skip if --mode diagnose)

Load the relevant rule files based on the diagnostic:
- Structural patterns → `rules/structure.md`
- Rhythm/cadence issues → `rules/rhythm.md`
- Rhetorical patterns → `rules/rhetoric.md`
- Generic or abstract content → `rules/specificity.md`
- Voice mismatch → `rules/voice.md`

**Rewrite selectively**. For each sentence, the valid actions are:
- **Keep** (sentence is fine)
- **Restructure** (change clause arrangement, not words)
- **Replace** (find a more specific or natural phrasing)
- **Remove** (sentence adds no value — cut it)
- **Merge** (two adjacent sentences would read better as one)
- **Split** (one long sentence should breathe as two)
- **Move** (reorder within paragraph for better flow)
- **Flag** (requires author context to improve — do not invent)

In `--mode preserve`: only **restructure** and light **replace** are permitted.
In `--mode aggressive`: **remove**, **merge**, **split**, and **move** are all available freely.
In `--mode rewrite` (default): use judgment.

### Stage 5 — Adversarial Self-Review

After completing the rewrite, check:
1. What still sounds generic?
2. What sounds like a template?
3. Where did I over-edit?
4. Where did I remove personality?
5. Where did I introduce fake personality?
6. Did I invent anything?
7. Did I change the author's position on anything?
8. Did I make every paragraph equally polished? (Don't — humans don't)
9. Did I accidentally give the whole document the same rhythm?
10. Does this still sound like the same person?
11. Would a human actually choose these words here?
12. Does this now sound like "humanizer writing" rather than the author?

Revise based on this review. The final output should pass all 12 checks.

### Stage 6 — Output

Present:
1. The diagnostic report (Stage 2)
2. The rewritten text (if applicable)
3. A brief note on what was changed and why, for transparency

For long documents, process section by section rather than all at once.

## What Not Ai Explicitly Forbids

- Random typos as "humanization"
- Forced slang inappropriate to the register
- Unnecessary sentence fragments as "variety"
- Invented memories, emotions, or opinions
- Deliberate grammatical mistakes
- Forcing first-person language where the original is third-person
- Excessive contractions to signal informality
- Superficial synonym replacement without structural reasoning

## Reference Files (load when needed)

| File | When to load |
|------|-------------|
| `rules/structure.md` | Structural clause/density issues detected |
| `rules/voice.md` | Voice matching or preservation needed |
| `rules/specificity.md` | Generic/abstract content detected |
| `rules/rhythm.md` | Uniform cadence or sentence repetition detected |
| `rules/rhetoric.md` | Rhetorical pattern issues (transitions, stance, engagement) |
| `rules/context.md` | Genre or audience ambiguous |
| `references/wikipedia-signs.md` | Need list of AI tells with context |
| `references/writing-research.md` | Need academic backing for a diagnostic |
| `references/methodology.md` | Need to explain Not Ai's approach |

## Cross-Agent Installation

```bash
# Claude Code / Codex / Cursor / compatible agents
git clone https://github.com/[username]/not-ai ~/.claude/skills/not-ai

# Antigravity
git clone https://github.com/[username]/not-ai ~/.gemini/antigravity/skills/not-ai

# Project-local (any agent)
git clone https://github.com/[username]/not-ai .agents/skills/not-ai
```

The core skill requires no dependencies. Python scripts in `scripts/` require Python 3.8+ with `spacy` and `nltk` for full analysis. All scripts degrade gracefully — the skill works without them.
