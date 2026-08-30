# Not Ai: Design Methodology

This document explains *why* Not Ai is designed the way it is. It answers: what are we trying to solve, what have others already tried, why those approaches fall short, and what we do differently.

---

## The Problem Being Solved

AI-assisted writing is now pervasive. The problem is not that AI was involved — it is that AI-generated prose exhibits a recognizable set of generic machine-like patterns that make writing feel:

- Produced rather than composed
- Generic rather than specific
- Confident without evidence
- Smooth without personality
- Organized without argument
- Technically correct but not communicative

These patterns make the writing less effective at its actual goal — communicating with a particular person, in a particular context, for a particular purpose.

The goal of Not Ai is not to hide AI involvement. It is to remove the generic machine habits and restore genuine human authorship: specificity, judgment, voice, context, and appropriate variation.

---

## What Has Been Tried and Why It Falls Short

### Approach 1: Word Blacklisting

The most common approach. Identify words and phrases associated with AI writing ("delve", "leverage", "furthermore", "comprehensive", etc.) and replace or remove them.

**Why it fails**:

A word is not the problem. "Delve" is not incorrect. "Leverage" is appropriate in many contexts. The problem is the *pattern* of these words appearing together with elevated nominalization, uniform sentence length, excessive transitions, and absent rhetorical engagement.

Removing words while leaving the structural pattern produces text that reads like AI writing with a few words changed. The underlying morphosyntactic fingerprint — what Reinhart et al. (PNAS 2025) measured using Biber's 66-feature tagset — remains completely unchanged.

The analogy: removing a person's cologne doesn't change their gait, posture, or way of speaking. A word blacklist changes the cologne.

### Approach 2: Paraphrase Rewriting

Pass the text through an LLM with instructions to "paraphrase" or "make more natural." Most commercial humanizers use this approach.

**Why it fails**:

1. **Meaning drift**: Paraphrase operations frequently alter claims, qualifications, and specifics in ways that change what the text actually says.
2. **Voice destruction**: The new text sounds "human" but no longer sounds like the author.
3. **Humanizer voice creation**: All paraphrase-based humanizers trained on similar feedback converge toward the same "humanizer voice" — a recognizable rhythm and vocabulary that is now itself a detectable pattern.
4. **No structural improvement**: The underlying clause distributions, information density, and rhetorical patterns remain the same or get worse.

### Approach 3: Surface Variation Injection

Add fragments. Break long sentences arbitrarily. Insert contractions. Add slang. Vary punctuation randomly.

**Why it fails**:

Human writing is not defined by imperfection. Deliberately introducing errors and artificial variation does not produce human writing — it produces a caricature of human writing. The result is recognizable as "humanizer output" to any careful reader.

Additionally, this approach destroys writing quality in the process. "Make it sound human" should never mean "make it worse."

### Approach 4: Fixed Voice Templates

Offer 3–5 preset voice modes ("casual", "professional", "academic") and apply whichever the user selects.

**Why it fails**:

"Casual" and "professional" are not author voices. They are generic register targets. The result is text that might match a register but definitely doesn't sound like the person who asked for the rewrite.

Human writing diversity is much richer than any set of fixed modes can capture. Different professional writers have completely different professional voices. The fixed-template approach replaces one generic pattern (AI writing) with another generic pattern (template humanization).

---

## Not Ai's Approach

### Principle 1: Operate at the structural level, not the surface level

The primary fingerprints of LLM-generated text are morphosyntactic and rhetorical, not lexical. Not Ai measures and addresses:
- Present participial clause rate (2–5× elevated in instruction-tuned LLMs)
- Nominalization density (1.5–2× elevated)
- Information density (systematically higher than human text in same genre)
- Rhetorical engagement markers (significantly lower than human writing in essays)
- Epistemic stance calibration (differently calibrated than humans)
- Paragraph structure variety
- Sentence length distribution (burstiness)

These are the actual differences. Addressing them produces actual improvement.

### Principle 2: Deterministic analysis precedes LLM reasoning

Not Ai runs Python scripts to measure structural features before invoking LLM reasoning. This means:
- Objective measurements inform the intervention strategy
- The LLM does not have to guess or hallucinate counts
- Results are reproducible and explainable
- The diagnostic is specific, not vague

### Principle 3: Voice is a hard constraint, not an afterthought

Voice preservation is built into the pipeline from the start, not applied as a final check. When a voice profile is available:
- It constrains every rewrite decision
- Sentence length changes must fit the author's distribution
- Formality level is fixed
- Punctuation habits are preserved

When no voice profile is available, the skill applies neutral interventions that don't impose a voice — and tells the user this.

### Principle 4: Genre and context condition the intervention

The same text processed as a LinkedIn post and as an academic abstract requires different interventions. Not Ai explicitly identifies genre before doing anything else, and applies genre-appropriate rules.

This means:
- High nominalization in an academic abstract is not a problem — it's appropriate
- Engagement markers in technical documentation are not needed — they'd be inappropriate
- Fragments in social media are fine — they're expected

### Principle 5: Human writing is a distribution, not a target

Not Ai does not define "human writing" as a single style or voice. Research shows that human writing varies enormously across:
- Individuals (researchers vs. novelists vs. engineers vs. teenagers)
- Genres (essay vs. email vs. documentation vs. fiction)
- Languages (the structural patterns are different in Czech, Japanese, etc.)
- Registers (formal vs. casual vs. technical)

The goal is to produce output that could plausibly exist in the space of human writing, not to converge on a single "humanized" target. This explicitly counters the humanizer paradox.

### Principle 6: Selective edits over wholesale rewriting

Not Ai's valid rewrite actions are: keep, restructure, replace, remove, merge, split, move, or flag. Rewriting everything is not on the list.

Over-editing is as much a failure mode as under-editing. Text that gets rewritten wholesale loses the author's original phrasing that was already working.

### Principle 7: Never invent

If a specific detail would improve a sentence but that detail doesn't exist in the source, Not Ai:
- Flags the location
- Asks the author to supply the detail
- In aggressive mode: uses a placeholder `[specific detail here]`

Never fabricates facts, anecdotes, credentials, or experiences.

### Principle 8: Adversarial self-review

After rewriting, Not Ai asks itself 12 diagnostic questions about what might have gone wrong in the rewrite (over-editing, voice loss, invented content, new mechanical patterns). This catches problems that forward-pass reasoning misses.

---

## What Not Ai Does Not Claim

**Not Ai does not claim**:
- "This text is guaranteed human."
- "This bypasses every detector."
- "This cannot be detected."
- Any specific bypass rate or detection score.

These claims are scientifically indefensible. Detection systems evolve. Models evolve. The only honest claim is about writing quality properties: meaning preserved, voice preserved, structure improved, generic patterns reduced.

---

## How Not Ai Differs from Existing Systems

| Dimension | Typical Humanizer | Not Ai |
|-----------|-------------------|--------|
| Primary intervention level | Lexical (words) | Structural (clause types, density) |
| Diagnostic | Vague or absent | Specific, deterministic measurement |
| Voice model | Fixed templates (5 modes) | Author-extracted profile |
| Genre awareness | None | Explicit genre profiles |
| Meaning preservation | Implicit | Verified (number check, semantic similarity) |
| Over-edit protection | None | Adversarial self-review |
| Fabrication prevention | None | Explicit prohibition + flag mechanism |
| Human writing model | Single target | Distribution across styles |
| Open architecture | Closed | Open source, cross-agent portable |
| Research basis | Marketing claims | Peer-reviewed linguistics research |

---

## Limitations and Honest Caveats

1. **Not Ai is a skill, not a replacement for human authorship.** The best writing comes from a person who knows what they want to say and has something specific to say. Not Ai helps with the presentation; it cannot supply the substance.

2. **The structural fingerprints change as models evolve.** Research from 2025 reflects 2024–2025 model behavior. As models are updated and fine-tuned, the specific measurements may shift. Not Ai's scripts and rules should be updated accordingly.

3. **Genre classification is imperfect.** Automatic genre detection will sometimes be wrong. The user can and should correct genre assumptions.

4. **The voice profile is approximate.** With a short writing sample, the voice profile captures less than with a long one. The system notes uncertainty when the sample is small.

5. **Semantic similarity measures are proxies.** Token overlap is not the same as semantic equivalence. The benchmark uses it as a cheap proxy; for production evaluation, embedding-based similarity is more reliable.

6. **Not Ai cannot verify external facts.** If the original text contains a factual error, Not Ai will preserve it. Fact-checking is the author's responsibility.

7. **Not Ai is not for academic dishonesty.** Using Not Ai to disguise AI-written work as human-written work for submission in contexts where this is prohibited is a misuse. The tool's purpose is legitimate writing improvement.
