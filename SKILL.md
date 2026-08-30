---
name: not-ai
description: >-
  Writing intelligence skill. Use this when the user wants to:
  (1) write something that sounds human and natural from scratch (e.g. "/not-ai write a 200 word article on Gen AI"),
  (2) humanize or fix existing AI-generated or AI-assisted text that sounds robotic, generic, or machine-like,
  (3) diagnose why a piece of writing sounds like AI,
  (4) make prose more natural, specific, or voice-consistent.
  Trigger phrases: "not-ai", "/not-ai", "humanize", "make this sound human", "sounds like AI", "fix my writing", "make this natural".
  Modes: --mode write | diagnose | rewrite | preserve | aggressive. --voice <sample> to match the author's style.
  This is NOT a detector-bypass tool. The goal is good writing for human readers.
---

# Not Ai

Writing intelligence skill. Two modes of use:

1. **Write from scratch** — `/not-ai write [topic/brief]` — produce writing on a topic that sounds human from the first word, applying every rule below
2. **Humanize existing text** — `/not-ai [paste text]` or `not-ai this: [text]` — diagnose and fix AI-generated or AI-assisted prose

**Core rule: produce writing that would be good even if no detector existed.**

Never fabricate facts, anecdotes, credentials, or emotions. If a specific detail is missing, use `[specific detail here]` — never invent it.

---

## When Writing From Scratch (`--mode write`)

Apply all rules below *during* generation. Do not write AI-flavored text and then clean it up — write naturally the first time.

1. Identify genre, audience, and register first (see Genre Profiles below)
2. Apply structural rules throughout — no participial openers, controlled nominalization, varied rhythm
3. Do not use vocabulary from the AI-associated list
4. Use specificity — concrete details, not abstract categories
5. Output the text directly. No diagnostic needed.

## When Humanizing Existing Text (default)

Run the full six-stage pipeline:

**Stage 0 — Context**: identify genre, audience, register, intent. State it. If unclear, say: "Genre assumed: [X] — correct if wrong."

**Stage 1 — Measure**: count or estimate the structural signals below.

**Stage 2 — Diagnostic**: output the diagnostic report with specific findings and quotes from the text.

**Stage 3 — Voice profile** (only with `--voice`): extract 10 dimensions from the sample.

**Stage 4 — Selective rewrite**: make the minimum changes needed. Valid actions per sentence: `KEEP · RESTRUCTURE · REPLACE · REMOVE · MERGE · SPLIT · MOVE · FLAG`

**Stage 5 — Self-review**: ask the 12 questions before outputting.

**Stage 6 — Output**: diagnostic + rewritten text + brief rationale.

---

## Structural Rules (apply always)

### 1. Present participial clauses — most important signal
Instruction-tuned LLMs open sentences with -ing verb phrases at 2–5× the human rate.
"Building on this..." / "Leveraging the power of..." / "Drawing from research..."

Fix: convert to subject-verb. "Building on this" → "This builds on". "Leveraging the platform's scale" → "Because the platform operates at scale,". Cut if decorative.
Keep in narrative flow: "Walking into the room, she noticed..." is fine.

### 2. Nominalization density
LLMs nominalize at 1.5–2× the human rate. Human norm: 25–40 per 1,000 words. LLMs: 45–70.
"the implementation of the solution" → "implementing the solution"
"the development of new approaches" → "developing new approaches"
Keep when: the nominalization is the thing being discussed, or the genre is academic.

### 3. Sentence rhythm
All sentences similar length = mechanical. Goal: motivated variation, not cycling.
Short sentences for: conclusions, reversals, key facts that need to land.
Do NOT cycle short-medium-long mechanically. Do NOT add fragments as fake variation ("And fast. Very fast.") — this is humanizer-voice cliché.

### 4. Opening word repetition
3+ sentences in a paragraph starting with "The", "This", "It", or "In" → reorder one.

### 5. Paragraph structure uniformity
Every paragraph: topic sentence + 3 supporting + closer = formulaic.
Vary: some paragraphs open with evidence. Some are 1–2 sentences. Some are long. Context-appropriate.

### 6. Mechanical transitions — remove when implicit
"Furthermore" / "Moreover" / "Additionally" → remove if the connection is already clear.
"In conclusion" / "To summarize" → remove if it restates what was just said.
"It is worth noting that" / "It is important to mention" / "In the realm of" → almost always cut.

### 7. Redundant closing sentences
If the last sentence of a section restates the sentences before it: remove it, or replace with a consequence/forward-looking observation.

---

## Rhetorical Rules (apply always)

### Epistemic stance
False hedges: "It is worth noting that [certain claim]" → just make the claim.
Restore genuine hedges where the author is actually uncertain: "it seems" / "evidence suggests" / "arguably".
Don't flatten everything to either hedged or certain — calibrate to the actual claim.

### Engagement markers (genre-dependent)
Essays, blogs, emails, social media: check if the text ever acknowledges the reader. A question, a direct address, an anticipation of objection can be added.
Academic abstracts, technical docs, legal, news: do NOT add engagement markers.
Never add forced questions like "So, what's the takeaway?" — that's its own cliché.

### Tricolons
Count before defaulting to three. Two genuine items → use two. Four → use four. Not every thought comes in threes.

---

## Specificity Rules (apply always)

The most persistent gap between AI and human writing is not vocabulary — it is specificity.

For each claim: "Could this sentence appear in an article about a completely different topic?" If yes, it's generic.

Fix only when evidence exists in the source. If missing, use `[specific detail here]`.

Never invent: no fabricated examples, statistics, names, anecdotes, or dialogue.

AI-generic patterns to flag:
- "This represents a paradigm shift..." → does the text actually show this?
- "Many experts agree..." → which experts? name them or hedge honestly
- "Studies have shown..." → which studies?
- "Various applications, including technology, healthcare, and education" → naming categories is not an example
- "In recent years..." → when exactly?
- "significantly" / "substantially" / "dramatically" without numbers

---

## AI-Associated Vocabulary (avoid or contextualize)

Words instruction-tuned models use at 10–100× the human rate. One occurrence is rarely a problem. A pattern of 5+ in one passage is a signal.

delve, leverage/leveraging, utilize/utilization, facilitate/facilitation, comprehensive, robust, seamless, cutting-edge, pivotal, crucial (when used generically), vital, paramount, foster, underscore, meticulous, nuanced (especially "nuanced understanding"), multifaceted, myriad, transformative, groundbreaking, revolutionary, paradigm shift, tapestry, camaraderie, palpable, intricate, vibrant, solace, empower, impactful, innovative, synergy, ecosystem (when used metaphorically), holistic, dynamic, diverse (used generically).

Note: these are not wrong words. They are wrong when used as padding to signal quality that the surrounding text doesn't demonstrate.

---

## Voice Profile (with --voice [sample])

Extract from the sample:
1. **Sentence length**: mean, std → `tight` (<12 words mean) / `expansive` (>25) / `variable`
2. **Paragraph length**: avg sentences → `compact` / `extended` / `mixed`
3. **Punctuation**: em-dash frequency (rare/occasional/frequent), parentheticals yes/no, semicolons yes/no
4. **Contractions**: per 1,000 words → `none` / `rare` / `moderate` / `frequent`
5. **First-person**: `absent` / `occasional` / `central`
6. **Hedging balance**: hedge vs. certainty markers → `cautious` / `assertive` / `calibrated`
7. **Formality**: 1 (very informal) to 5 (very formal)
8. **Reader address**: uses "you" / rhetorical questions? yes/no
9. **Example density**: `high` / `medium` / `low`
10. **Emotional intensity**: `flat` / `measured` / `engaged` / `passionate`

The voice profile is a **hard constraint**. If the author never uses em-dashes, don't insert them. If the author avoids first-person, don't add it.

Without a sample: apply neutral rewriting. State: "Voice profile: insufficient signal — voice-neutral rewrite applied."

---

## Genre Profiles

### LinkedIn Post
Natural: first person, professional but personable, short paragraphs, hook opening, ends with insight or question, formality 2–3.
Fix: "In today's fast-paced world..." (cut); excessive bullet lists (convert to prose); "1. 2. 3." labels on bullets (remove labels); platitudes without specific content (flag).
Don't: casualize the voice if the author's register is professional; add hashtags unless the author provided them.

### GitHub README
Natural: technical, precise, imperative, short sentences, code blocks appropriate, formality 4.
Fix: "revolutionizes how developers..." → "helps developers..."; "powerful/comprehensive/robust" → specific; marketing opening → factual description.
Don't: informalize technical precision; cut accurate caveats for "flow."

### Academic Abstract
Natural: third person or passive, dense, precise, no filler, high nominalization is appropriate, formality 5.
Fix: "landmark contribution" → "presents/demonstrates/analyzes"; vague method → specific method name; summary at the end of an abstract (cut — it's already a summary); "may perhaps suggest the possibility" → "suggests."
Don't: add engagement markers; reduce information density; convert passive to active if the field uses passive.

### Personal Essay
Natural: first person, reflective, specific personal details, sentence length varies widely, rhetorical questions appropriate, formality 1–3.
Fix: "Many people feel..." → "I noticed..."; inflated significance without grounding (cut); abstract conclusions without the experience (flag).
Don't: invent personal experiences or emotions; sanitize distinctive voice; add an inspirational ending the author didn't write.

### Professional Email
Natural: clear purpose in opening, direct request or call to action, formality 2–4.
Fix: "I hope this email finds you well" (cut unless genuine); "I was wondering if perhaps..." → "Could you..."; "Please do not hesitate to reach out" → "Let me know"; unnecessary preamble before the point.
Don't: casualize a formal relationship; cut important qualifications.

### Technical Documentation
Natural: task-oriented, second person in tutorials, numbered lists and code blocks appropriate, minimal hedging, formality 3–4.
Fix: "intelligent/smart/powerful" → specific capability; "In today's digital landscape..." → "This document explains..."; happy-path descriptions without prerequisites or limitations.
Don't: reduce accuracy for "flow"; cut warnings or edge cases.

### Social Media (short-form)
Natural: very short, high information per word, fragments acceptable, opinions common, formality 1–2.
Fix: excessive formality; long clausal sentences; generic takes → specific observation.
Don't: impose professional formality; add caveats that destroy the point.

### Narrative / Fiction
Natural: shows rather than tells, specific sensory details, character perspective, sentence rhythm mirrors scene tempo.
Fix: telling emotions ("She felt devastated") → action or gesture; abstract narrative summary → show the events; flat event escalation (every scene same weight); over-explained themes ("This illustrates the theme of loss" → remove).
Don't: invent plot events, dialogue, or character details; impose a tidy resolution.

---

## Self-Review (Stage 5 — always run after rewriting)

Before outputting, ask:
1. What still sounds generic?
2. What sounds like a template?
3. Where did I over-edit?
4. Did I remove personality that was working?
5. Did I introduce fake personality?
6. Did I invent anything?
7. Did I change the author's position on anything?
8. Is every paragraph now equally polished? (It shouldn't be.)
9. Does this now have its own mechanical rhythm?
10. Does this still sound like the same person?
11. Would a human actually choose these words here?
12. Does this sound like "humanizer writing" rather than the author?

Fix anything that fails before outputting.

---

## What Not Ai Will Never Do

- Add random typos or errors to "seem human"
- Force slang into the wrong register
- Invent memories, emotions, opinions, or facts
- Introduce deliberate grammar mistakes
- Force first-person where the author uses third
- Add excessive contractions to signal informality
- Optimize for a detector score
- Rewrite everything when selective edits are enough
- Apply essay rules to technical documentation
- Make writing worse in the name of making it "human"

---

## Quick Reference

```
/not-ai write a 200 word article on Gen AI        → writes from scratch, naturally
/not-ai [paste text]                              → diagnose + rewrite existing text
/not-ai --mode diagnose [text]                    → analysis only, no changes
/not-ai --mode preserve [text]                    → strict meaning/voice preservation
/not-ai --mode aggressive [text]                  → stronger structural changes
/not-ai --voice my-writing.txt [text]             → match to your voice sample
```

For detailed academic research behind these rules: [references/writing-research.md](./references/writing-research.md)
For structural measurement scripts: [scripts/](./scripts/)
