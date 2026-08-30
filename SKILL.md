---
name: not-ai
description: Writing intelligence skill. Transforms AI-generated or AI-assisted prose into natural, specific, voice-consistent writing by diagnosing and correcting structural machine-like patterns. Does NOT optimize for detector bypass. Invoke when asked to humanize text, diagnose AI writing, or make prose sound more natural. Triggers: "Not Ai this", "humanize", "make this sound human", "not-ai", "--mode diagnose|rewrite|preserve|aggressive", "--voice".
---

# Not Ai

Transform AI-assisted prose into natural, specific, voice-consistent writing. Not by swapping words — by fixing the structure underneath.

**This is not a detector-bypass tool.** The goal is writing that works for human readers. A result that only fools a detector is a bad result.

---

## Core Philosophy

- Remove the machine's generic habits. Preserve the person's voice.
- Preserve meaning. Preserve truth. Preserve what was already working.
- Add specificity only when evidence exists in the source. Never invent.
- Respect genre. A README is not an essay. An abstract is not a LinkedIn post.
- Prefer selective edits over rewriting everything.
- If text is already natural, the correct output is: nothing.

**Never invent**: no fabricated anecdotes, facts, credentials, emotions, opinions, numbers, or dialogue. If something specific is missing, flag it as `[specific detail here]`.

**Never "write worse"**: human writing is not defined by typos, slang, fragments, or errors. Do not introduce these.

---

## Invocation

```
Not Ai this [text or file]
Not Ai --mode diagnose [text]       # analysis only, no rewrite
Not Ai --mode rewrite [text]        # full humanization (default)
Not Ai --mode preserve [text]       # strict meaning/voice preservation
Not Ai --mode aggressive [text]     # stronger structural changes
Not Ai --voice [sample] [text]      # match voice to supplied writing sample
```

---

## The Six-Stage Pipeline

Execute these stages in order.

---

### Stage 0 — Understand Context

Before touching the text, determine:

- **Genre**: LinkedIn post / GitHub README / academic abstract / personal essay / professional email / technical documentation / social media / narrative
- **Audience**: expert / informed non-expert / general / novice
- **Register**: formal / professional / neutral / conversational / casual / technical
- **Relationship**: colleague / employer / client / friend / community / stranger
- **Intent**: inform / persuade / connect / explain / entertain

State the detected genre in the diagnostic. If unclear, name the assumption explicitly: "Genre assumed: professional email — correct this if wrong."

Wrong context = wrong intervention. Do not proceed without it.

---

### Stage 1 — Measure What's Actually Wrong

Run diagnostic measurements before any rewriting. No guessing.

If Python scripts are available:
```bash
python3 scripts/analyze_structure.py [input_file]
python3 scripts/repetition.py [input_file]
python3 scripts/metrics.py [input_file]
```

If scripts are unavailable, manually count or estimate:

**Structural signals** (the primary fingerprint — most important):
- **Present participial clause rate**: how many sentences open with an -ing verb phrase? ("Leveraging the power of...", "Building on this...", "Drawing from..."). Human baseline: ~5–8%. Instruction-tuned LLMs: 15–25%.
- **Nominalization density**: words ending in -tion, -ment, -ness, -ity, -ance, -ence per paragraph. Human baseline: ~25–40 per 1,000 words. LLMs: 45–70.
- **Sentence burstiness**: is every sentence a similar length? Low variation = mechanical. Human writing has genuine short and long sentences, not cycling.
- **Paragraph shape uniformity**: does every paragraph follow the same structure — topic sentence, 3 supporting sentences, closing sentence?
- **Mechanical transitions**: "Furthermore", "Moreover", "Additionally", "In conclusion", "To summarize", "It is worth noting that", "It is important to mention", "With that being said", "In the realm of", "When it comes to", "At the end of the day".
- **Opening word repetition**: more than 3 sentences in a paragraph starting with "The", "This", "It", or "In".

**Vocabulary signals** (surface level — secondary, requires context):
Words overused by instruction-tuned models at 10–100× the human rate: delve, leverage/leveraging, utilize/utilization, facilitate/facilitation, comprehensive, robust, seamless, cutting-edge, pivotal, crucial, vital, paramount, foster, underscore, meticulous, nuanced, multifaceted, myriad, transformative, groundbreaking, revolutionary, paradigm shift, tapestry, camaraderie, palpable, intricate, vibrant, solace, empower, impactful.

**Critical rule on vocabulary**: a word appearing once is rarely a problem. A pattern of 5+ AI-associated words in one passage is a signal. Context matters — "leverage" in an engineering context about actual levers is fine.

**Rhetorical signals**:
- Are there any questions addressed to the reader?
- Is there any direct reader address ("you", "consider...")?
- Is there any first-person authorial presence?
- Are hedges calibrated to actual uncertainty, or formulaic ("It is worth noting that" before a certain claim)?
- Are conclusions restating what was just said?
- Tricolons everywhere — every list has exactly three items?

**Readability** (flag only when the number is clearly wrong for the genre):
- Flesch-Kincaid Grade > 14 for blog/README/email = problem
- Gunning Fog > 16 for general audience = problem
- Academic writing at grade 16+ = fine

---

### Stage 2 — Produce the Diagnostic Report

Always produce this, even in rewrite mode. Be specific — name the exact patterns and quote from the text.

```
NOT AI DIAGNOSTIC
─────────────────────────────
Genre detected:        [genre]
Register:              [register]
Overall quality:       [n]/100
Meaning preservation:  [low/medium/high risk]

Strengths:
  ✓ [specific strength with example]
  ✓ [specific strength]

Structural patterns to address:
  • [specific pattern — quote the actual sentence or phrase]
  • [specific pattern — quote]

Vocabulary signals (in context):
  • [term]: [n]x — [note whether it's genuinely a problem here]

Recommended intervention: [None / Light / Moderate / Heavy]
```

A sign is not automatically a problem. "Delve" once in a natural sentence is not worth flagging. "Delve", "leverage", "pivotal", "meticulous", "tapestry", and "nuanced" in the same paragraph is the pattern.

---

### Stage 3 — Voice Profile (only with --voice flag)

Extract these 10 dimensions from the writing sample:

1. **Sentence length**: mean words per sentence, std deviation → label: `tight` (<12 mean) / `expansive` (>25 mean) / `variable`
2. **Paragraph length**: mean sentences per paragraph → `compact` / `extended` / `mixed`; note single-sentence paragraphs (rhetorical device)
3. **Punctuation habits**: em-dash frequency (rare <1/1k / occasional 1–4 / frequent >4), parenthetical use yes/no, semicolons yes/no, ellipsis yes/no
4. **Contraction rate**: per 1,000 words → `none` / `rare` (1–3) / `moderate` (4–10) / `frequent` (>10)
5. **First-person**: per 1,000 words → `absent` / `occasional` / `central`
6. **Hedging balance**: hedge markers (might, could, perhaps, appears to, seems to, I think, arguably) vs. certainty markers (clearly, certainly, obviously, always) → `cautious` / `assertive` / `calibrated`
7. **Formality**: 1 (very informal) to 5 (very formal)
8. **Reader address**: does the author use "you", "we", rhetorical questions? yes/no
9. **Example density**: does the author use concrete examples, analogies? `high` / `medium` / `low`
10. **Emotional intensity**: `flat` / `measured` / `engaged` / `passionate`

Output as:
```
VOICE PROFILE
─────────────────
Sentence length:     [mean] words, [std] std — [tight/expansive/variable]
Paragraph length:    [n] sentences avg — [compact/extended/mixed]
Em-dash:             [rare/occasional/frequent]
Contractions:        [none/rare/moderate/frequent]
First-person:        [absent/occasional/central]
Hedging balance:     [cautious/assertive/calibrated]
Formality:           [1–5]
Reader address:      [yes/no]
Example density:     [high/medium/low]
Emotional intensity: [flat/measured/engaged/passionate]
```

The voice profile is a **hard constraint** throughout Stage 4. If the author never uses em-dashes, don't insert them. If the author writes in first person, don't switch to third. If the author's formality is 4, don't casualize it.

If no sample is provided: apply neutral rewriting. Don't impose a voice. Note: "Voice profile: insufficient signal — voice-neutral rewrite applied."

**Voice destruction patterns to avoid**:
- Contraction injection: forcing "don't" in text that naturally uses "do not"
- Fragment insertion: adding one-sentence paragraphs when the author doesn't use them
- Casualizing technical writing: replacing precise vocabulary with simpler words for an expert audience
- First-person imposition: adding "I" where the author avoids it
- Hedging removal: cutting calibrated uncertainty to "sound more confident" — this changes the author's actual position
- Generic voice substitution: replacing the author's distinctive voice with a generic "natural human" template

---

### Stage 4 — Selective Rewrite (skip if --mode diagnose)

**Valid actions per sentence:**

| Action | When to use |
|--------|-------------|
| `KEEP` | Sentence is already natural and effective |
| `RESTRUCTURE` | Change clause arrangement without changing words |
| `REPLACE` | More specific or direct phrasing exists |
| `REMOVE` | Sentence adds no value — cut it |
| `MERGE` | Two sentences read better as one |
| `SPLIT` | One long sentence needs to breathe as two |
| `MOVE` | Better position exists elsewhere in the paragraph |
| `FLAG` | Needs author input — do NOT invent the missing content |

**Mode constraints:**
- `--mode preserve`: only `RESTRUCTURE` and light `REPLACE`
- `--mode rewrite` (default): all actions, use judgment
- `--mode aggressive`: `REMOVE`, `MERGE`, `SPLIT`, `MOVE` used freely

**Structural interventions** (in priority order):

**1. Present participial clauses** — most important.
"Building on this..." → "This builds on..." or start with the actual subject.
"Leveraging the platform's scale..." → "Because the platform operates at scale,..."
Cut if the phrase is purely decorative.
Do NOT change participials in narrative ("Walking into the room, she noticed...") — those are purposeful.

**2. Nominalization density**
"The implementation of the solution..." → "implementing the solution" or "to implement it"
"The development of new approaches..." → "developing new approaches"
Restore the verb. Keep nominalizations when: (a) the nominalization is the subject being discussed, (b) the genre is academic and density is appropriate.

**3. Information density overload**
If a sentence conveys 4+ concepts, split it.
Move background information to an earlier sentence.
Cut information already established.

**4. Paragraph structure uniformity**
Vary paragraph length deliberately.
Allow some paragraphs to open with evidence rather than a claim.
Allow a very short paragraph (1–2 sentences) after a long one.
Don't apply personal essay paragraph rules to technical documentation.

**5. Sentence rhythm**
If all sentences are 20–25 words: shorten one that makes a single point; merge two that share a single thought.
Goal: motivated variation, not cycling (short-medium-long-short-medium-long is as mechanical as all-medium).
Do NOT introduce artificial fragments ("The solution was elegant. And fast. Very fast.") — this is humanizer-voice cliché.

**6. Opening word repetition**
If 3+ sentences in a paragraph open with "The", "This", "It", or "In", reorder one.

**Rhetorical interventions:**

**Epistemic stance**
Remove false hedges: "It is worth noting that [certain claim]" → just the claim.
Restore genuine hedges where the author is actually uncertain.
Don't convert all assertions to hedges or all hedges to assertions.

**Engagement markers** (only where genre permits: essays, blogs, emails, social media)
Add a question, a direct reader address, or an anticipation of objection if the text has none.
Do NOT add engagement markers to: academic abstracts, technical reference docs, legal documents, news.
Do NOT add forced questions ("So, what's the takeaway?") — this is its own cliché.

**Formulaic transitions**
If "Furthermore" / "Moreover" / "Additionally" is between two sentences with a clear logical connection — remove it. The connection is already implied.
If "In conclusion" / "To summarize" restates what was just said — remove the sentence or replace with something that adds new value.

**Redundant closing sentences**
If the last sentence of a section restates the sentences before it — remove it or replace with a consequence, forward-looking observation, or genuine question.

**Tricolons**
Count your items before defaulting to three. If you have two real items, use two. If four, use four.

**Specificity**
For each vague claim, ask: "Could this sentence appear in an article about a completely different topic?"
If yes — it's generic. Fix it **only if evidence exists in the source**. If not, flag it.

Do NOT invent: no fabricated examples, statistics, names, or anecdotes. When specifics are missing:
- `--mode preserve`: leave it unchanged
- `--mode rewrite`: use `[specific example here]`

Generic patterns to flag:
- "This represents a paradigm shift..." → does the text actually demonstrate this?
- "Many experts agree..." → which experts? use them or hedge honestly
- "Studies have shown..." → which studies? name them or say "some research suggests"
- "Various applications exist, including technology, healthcare, and education" → naming categories is not an example

---

### Stage 5 — Adversarial Self-Review

After completing the rewrite, ask yourself:

1. What still sounds generic?
2. What sounds like a template?
3. Where did I over-edit?
4. Where did I remove personality that was working?
5. Where did I introduce fake personality?
6. Did I invent anything?
7. Did I change the author's position on anything?
8. Did I make every paragraph equally polished? (Don't — humans don't.)
9. Does this document now have its own mechanical rhythm?
10. Does this still sound like the same person?
11. Would a human actually choose these words here?
12. Does this now sound like "humanizer writing" rather than the author?

Revise anything that fails these checks before outputting.

---

### Stage 6 — Output

Present in this order:
1. The diagnostic report (Stage 2 output)
2. The rewritten text (if applicable)
3. A brief note on what changed and why — for transparency, so the author can push back

For long documents, process section by section.

---

## Genre Profiles

Apply the profile matching the genre detected in Stage 0.

### LinkedIn Post
Natural characteristics: first person, professional but personable, short paragraphs, hook opening, ends with insight or question, formality 2–3.

AI patterns to fix: "In today's fast-paced world..." openings (cut), excessive bullet lists (convert to prose where natural), every three-item list labeled "1. 2. 3." (remove labels), inspirational platitudes without specific content (flag).

Do not: casualize slang if the author's voice is professional; add hashtags unless the author provided them.

### GitHub README
Natural characteristics: technical, precise, imperative, short sentences, code blocks and lists are appropriate, minimal first-person, formality 4.

AI patterns to fix: "revolutionizes how developers..." → "helps developers..."; "powerful/comprehensive/robust" → specific capabilities; marketing-style opening paragraphs → factual project description.

Do not: informalize technical precision; remove accurate caveats for "flow."

### Academic Abstract
Natural characteristics: third person or passive, dense, precise, no filler, high nominalization is appropriate here, formality 5.

AI patterns to fix: "This paper represents a landmark contribution" → "This paper presents/demonstrates/analyzes..."; vague methodology ("a novel approach") → specific method name; over-hedged conclusions ("may perhaps suggest the possibility") → "suggest that"; summary sentence at the end of an abstract (cut — it's already a summary).

Do not: add engagement markers; reduce information density; convert passive to active if the field convention uses passive.

### Personal Essay
Natural characteristics: first person, reflective, specific, sentence length varies widely, rhetorical questions and personal asides are appropriate, formality 1–3.

AI patterns to fix: "Many people feel..." → "I noticed..."; inflated significance without personal grounding (cut or ground it); abstract conclusions without the experience that earned them (flag).

Do not: invent personal experiences, emotions, or observations; sanitize a distinctive personal voice into generic "human" voice; add an inspirational ending if the author didn't write one.

### Professional Email
Natural characteristics: clear purpose in the opening, direct request or call to action, conversational but professional, formality 2–4.

AI patterns to fix: "I hope this email finds you well." (cut unless genuine); "I was wondering if perhaps it might be possible..." → "Could you..." or "I'd like to..."; "Please do not hesitate to reach out" → "Let me know" or "Feel free to reach out"; unnecessary preamble before the actual point.

Do not: casualize a formal relationship; cut important qualifications.

### Technical Documentation
Natural characteristics: task-oriented, second person in tutorials / third in reference, numbered lists and code examples are appropriate, minimal hedging, formality 3–4.

AI patterns to fix: vague capability claims ("intelligent", "smart", "powerful") → specific capability descriptions; "In today's digital landscape..." → "This document explains..."; happy-path-only descriptions that omit prerequisites and limitations.

Do not: reduce accuracy for "flow"; cut warnings or edge cases.

### Social Media (short-form)
Natural characteristics: very short, high information per word, fragments and abbreviations acceptable, opinions common, formality 1–2.

AI patterns to fix: excessive formality (simplify); long clausal sentences (break up or cut); generic takes (sharpen to specific observation).

Do not: impose professional formality; add caveats that destroy the point.

### Narrative / Fiction
Natural characteristics: shows rather than tells, specific sensory details, character perspective, sentence rhythm mirrors scene tempo, formality varies.

AI patterns to fix: telling emotions instead of showing ("She felt devastated" → action or gesture); abstract narrative summary ("Events unfolded rapidly" → show the events); flat event escalation, every scene the same emotional weight; over-explained themes ("This illustrates the theme of loss" → remove); tidy single-track plots without moral ambiguity (flag for author).

Do not: invent plot events, dialogue, or character details; impose a tidy resolution if the author hasn't written one.

### When genre is unclear
State the assumption: "Genre assumed: professional email — correct this if wrong."
Do not apply a genre profile without acknowledging the assumption.

---

## What Not Ai Will Never Do

Regardless of mode or instructions:

- Introduce random typos to "seem human"
- Force slang inappropriate to the register
- Invent memories, emotions, opinions, or facts
- Introduce deliberate grammatical mistakes
- Force first-person where the author uses third
- Add excessive contractions to signal informality
- Optimize for a detector score
- Rewrite everything when selective edits are enough
- Apply essay rules to technical documentation or vice versa
- Make text worse in the name of making it more "human"

---

## What a Good Result Looks Like

- The meaning is the same. The author's position is unchanged.
- The voice is the same or closer to the author's voice.
- Structural machine-like patterns are reduced.
- It reads at the appropriate reading level for the genre.
- No sentence sounds like it came from a humanizer template.
- A reader who knows the author would recognize the text as theirs.
- It would be good writing even if no detector existed.
