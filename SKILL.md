---
name: not-ai
description: Writing intelligence skill that produces or transforms prose to sound natural, specific, and human. Use when the user wants to write something from scratch without AI patterns, humanize or fix existing AI-generated text, diagnose why writing sounds robotic, or make any prose more natural and voice-consistent. Triggers on "not-ai", "/not-ai", "humanize this", "make this sound human", "sounds like AI", "fix my writing".
---

# Not Ai

Produce or transform writing that sounds like a person wrote it — not a language model.

Two modes:
- **Write from scratch**: `/not-ai write [topic or brief]` — generate on a topic using every rule below, naturally, from the first word
- **Humanize existing text**: `/not-ai [paste text]` — diagnose and fix AI-generated or AI-assisted prose

The goal is writing that works for human readers. Not writing that fools a detector.

**Hard rule across both modes: never fabricate.** No invented facts, anecdotes, statistics, emotions, or dialogue. When a specific detail is missing, write `[specific detail here]` — never fill it in.

---

## How to Use

```
/not-ai write a 200 word article on burnout in tech
/not-ai write a LinkedIn post about what I learned launching a product
/not-ai [paste your AI-written text here]
/not-ai --mode diagnose [text]       — analysis only, no rewrite
/not-ai --mode preserve [text]       — minimum changes, strict meaning preservation
/not-ai --mode aggressive [text]     — stronger structural intervention
/not-ai --voice [sample file] [text] — match the author's voice from a writing sample
```

---

## Pipeline (for humanizing existing text)

Run these stages in order.

### Stage 0 — Identify context before touching anything

Determine: genre, audience, register, intent. State the genre in the diagnostic. If unsure: "Genre assumed: professional email — correct if wrong."

Genres: LinkedIn post / GitHub README / academic abstract / personal essay / professional email / technical documentation / social media / narrative

Getting genre wrong means every intervention that follows will also be wrong.

### Stage 1 — Measure structural signals

Count or estimate these before any rewriting. The structural signals are what actually distinguish AI from human writing — not vocabulary.

**Present participial clause rate** (most important signal)
How many sentences open with an -ing verb phrase?
"Building on this...", "Leveraging the platform...", "Drawing from research..."
Human baseline: 5–8% of sentences. Instruction-tuned LLMs: 15–25%.

**Nominalization density**
Nouns formed from verbs: implementation, development, facilitation, optimization, utilization
Human norm: 25–40 per 1,000 words. LLMs: 45–70.

**Sentence length uniformity**
All sentences similar length = mechanical. Natural writing has motivated variation — short sentences for emphasis, long sentences for elaboration, not cycling.

**Mechanical transitions**
"Furthermore", "Moreover", "Additionally", "In conclusion", "To summarize", "It is worth noting that", "It is important to mention", "In the realm of", "With that being said"

**Opening word repetition**
3+ consecutive sentences starting with "The", "This", "It", or "In" in the same paragraph.

**Paragraph structure uniformity**
Every paragraph: topic sentence + 3 supporting sentences + closing sentence = formulaic.

**Epistemic stance**
False hedges: "It is worth noting that [certain claim]" — the hedge adds nothing.
Missing genuine hedges: asserting something uncertain with full confidence.

**Redundant summary sentences**
Final sentence of a section restates everything just said. Cut or replace with something new.

If Python scripts are available, run them for objective counts:
- [scripts/analyze_structure.py](./scripts/analyze_structure.py)
- [scripts/repetition.py](./scripts/repetition.py)
- [scripts/metrics.py](./scripts/metrics.py)

### Stage 2 — Produce the diagnostic

Specific findings with quotes from the text. Not a score. Not "the text has some AI patterns." Name exactly what was found.

```
NOT AI DIAGNOSTIC
─────────────────────────────
Genre:    [genre]
Register: [register]

Strengths:
  ✓ [quote something that already works]

Patterns to address:
  • [exact pattern] — "[quote from the text]"
  • [exact pattern] — "[quote from the text]"

AI vocabulary (in context):
  • "[word]": Nx — [note whether it's actually a problem here]

Intervention: None / Light / Moderate / Heavy
```

### Stage 3 — Voice profile (only with --voice)

Extract from the writing sample. See [references/style-research.md](./references/style-research.md) for the full 10-dimension profile format. Short version:

- Sentence length: mean and spread — tight / expansive / variable
- Contractions: none / rare / moderate / frequent
- First-person: absent / occasional / central
- Hedging: cautious / assertive / calibrated
- Formality: 1 (very informal) to 5 (very formal)
- Reader address: yes or no
- Emotional intensity: flat / measured / engaged / passionate

The voice profile is a constraint, not a suggestion. If the author never uses em-dashes, don't insert them.

Without a sample: apply neutral rewriting, state "Voice profile: insufficient signal."

### Stage 4 — Selective rewrite (skip if --mode diagnose)

Valid actions per sentence: KEEP · RESTRUCTURE · REPLACE · REMOVE · MERGE · SPLIT · MOVE · FLAG

The minimum changes needed. If something is already natural, keep it.

**--mode preserve**: only RESTRUCTURE and light REPLACE
**--mode rewrite** (default): use judgment
**--mode aggressive**: REMOVE, MERGE, SPLIT, MOVE used freely

### Stage 5 — Self-review before output

Ask these before outputting:
1. What still sounds generic?
2. Where did I over-edit?
3. Did I invent anything?
4. Did I change the author's position?
5. Does every paragraph now sound equally polished? (It shouldn't.)
6. Does this now sound like "humanizer writing" rather than the author?

Fix anything that fails.

### Stage 6 — Output

Diagnostic + rewritten text + brief note on what changed and why.

---

## Structural Rules (apply in both write and humanize modes)

### 1. Present participial clauses — highest priority

"Building on this..." → "This builds on..."
"Leveraging the platform's scale..." → "Because the platform operates at scale,..."
"Drawing from extensive research..." → cut, or start with the actual subject.

Keep in narrative: "Walking into the room, she noticed..." — that's purposeful. The problem is using these as default connective tissue in informational prose.

### 2. Nominalization — second priority

Restore the verb where a noun form is weakening the sentence.
"The implementation of the solution" → "implementing the solution"
"The development of new approaches" → "developing new approaches"

Keep nominalizations when: the nominalization is the thing being discussed, or the writing is genuinely academic.

### 3. Sentence rhythm

Short sentences work for: conclusions, reversals, key facts that need to land.
Do not cycle short-medium-long mechanically — that is itself a mechanical pattern.
Do not add artificial fragments ("And fast. Very fast.") — this is the humanizer-voice cliché.

### 4. Transitions — remove when implicit

If the logical connection between two sentences is already clear, the transition word is dead weight.
"Furthermore, X is also true" → "X is also true."
"In conclusion, as we have seen..." → cut the whole sentence or replace with something that adds new value.

### 5. Paragraph variation

Vary length. Let some paragraphs open with evidence instead of a claim. Let some be one sentence. Don't apply essay paragraph rules to technical documentation.

---

## Specificity Rules

The most persistent gap between AI and human writing is not vocabulary — it is specificity.

Test: "Could this sentence appear in an article about a completely different topic?" If yes, it's generic.

Fix only when evidence exists in the source text. If a specific detail is missing: `[specific detail here]`.

AI-generic patterns to flag:
- "This represents a paradigm shift" — does the text actually demonstrate this?
- "Many experts agree" — which experts? Name them or hedge honestly: "some researchers argue"
- "Studies have shown" — which studies?
- "Various applications, including technology, healthcare, and education" — these are categories, not examples
- "In recent years" — when exactly?
- "significantly / substantially / dramatically" without a number

---

## Vocabulary

Words instruction-tuned models use at 10–100x the human rate. One is rarely a problem. A cluster of 5+ in one passage is a signal.

delve, leverage/leveraging, utilize, facilitate, comprehensive, robust, seamless, cutting-edge, pivotal, foster, underscore, meticulous, nuanced (especially "nuanced understanding"), multifaceted, myriad, transformative, groundbreaking, tapestry, camaraderie, palpable, intricate, vibrant, empower, impactful, synergy, holistic, dynamic

These are not wrong words. They are wrong as padding — used to signal quality the surrounding text doesn't demonstrate.

---

## Genre Profiles

### LinkedIn Post
Hook opening (question, counterintuitive statement, or specific observation). Short paragraphs. First person, professional but personable. Ends with insight or genuine question. Formality 2–3.

Fix: "In today's fast-paced world..." (cut); platitudes without specific content (flag and request the actual story); "1. 2. 3." labels in bullet lists (remove — the list itself shows structure).

Don't: casualize if the author's register is professional; add hashtags the author didn't include.

### GitHub README
Technical, precise, imperative. Short sentences. Code blocks and bullet lists are expected. Minimal first-person. Formality 4.

Fix: "revolutionizes how developers..." → "helps developers..."; "powerful/comprehensive/robust" → specific capabilities; marketing opening → factual description of what the project does.

Don't: informalize technical precision; cut accurate caveats for flow.

### Academic Abstract
Third person or passive, dense, precise. No filler. High nominalization is appropriate here. No engagement markers. Formality 5.

Fix: "This paper represents a landmark contribution" → "This paper presents / demonstrates / analyzes..."; vague method ("a novel approach") → specific method name; summary sentence at the end of an abstract (cut — the abstract is already a summary); "may perhaps suggest the possibility that" → "suggest that."

Don't: add engagement markers or questions; reduce information density; convert passive to active if the field convention uses passive.

### Personal Essay
First person, reflective, specific. Sentence length varies widely — both very short and very long are appropriate. Rhetorical questions and personal asides belong here. Formality 1–3.

Fix: "Many people feel..." → "I noticed..."; inflated significance without personal grounding (cut or ground it); abstract conclusions without the experience that earned them (flag).

Don't: invent personal experiences or emotions; sanitize a distinctive voice into generic "human" voice; add an inspirational ending the author didn't write.

### Professional Email
Clear purpose in the opening sentence. Direct request or call to action. Formality 2–4 depending on relationship.

Fix: "I hope this email finds you well" (cut unless genuine); "I was wondering if perhaps it might be possible to..." → "Could you..." or "I'd like to..."; "Please do not hesitate to reach out" → "Let me know" or "Feel free to reach out."

Don't: casualize a formal professional relationship; cut important qualifications.

### Technical Documentation
Task-oriented. Second person in tutorials, third in reference. Numbered steps and code examples are appropriate. Minimal hedging — the feature either works or it doesn't. Formality 3–4.

Fix: "intelligent / smart / powerful" → specific capability description; "In today's digital landscape..." → "This document explains..."; happy-path descriptions that omit prerequisites or known limitations.

Don't: reduce accuracy for flow; cut warnings or edge cases.

### Social Media (short-form)
Very short. High information per word. Fragments and abbreviations are fine. Opinions common. Formality 1–2.

Fix: excessive formality (simplify); long clausal sentences (break up or cut); generic takes → sharpen to a specific observation.

Don't: impose professional formality; add caveats that destroy the point.

### Narrative / Fiction
Shows rather than tells. Specific sensory details. Character perspective. Sentence rhythm mirrors scene tempo.

Fix: telling emotions ("She felt devastated") → action, gesture, or detail; abstract narrative summary ("Events unfolded rapidly") → show the events; over-explained themes ("This illustrates the theme of loss") → remove; flat event escalation where every scene carries the same emotional weight.

Don't: invent plot events, dialogue, or character details; impose a resolution the author hasn't written.

---

## What Not Ai Will Never Do

- Add typos or errors to "seem human"
- Force slang into the wrong register
- Invent facts, memories, emotions, or opinions
- Introduce deliberate grammatical mistakes
- Force first-person where the author uses third
- Optimize for a detector score
- Rewrite everything when selective edits are enough
- Apply essay rules to technical documentation
- Make writing worse in the name of making it more human

---

## Research basis

The structural signals measured here come from peer-reviewed linguistics research. Details in [references/writing-research.md](./references/writing-research.md) and [references/style-research.md](./references/style-research.md).

Key source: Reinhart et al., PNAS 2025 — present participials at 2–5x human rate, nominalizations at 1.5–2x, instruction tuning (RLHF) as root cause, base models close to human rates.
