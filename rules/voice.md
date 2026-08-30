# Rules: Voice

Voice is the set of consistent stylistic choices that make a piece of writing feel like it comes from a specific person. Not Ai's purpose is not to impose a generic "human" voice but to preserve or reconstruct the author's own voice.

---

## What Voice Is Not

Voice is not:
- A writing quality tier ("formal" vs. "casual")
- A set of superficial quirks to copy
- An excuse to invent personality where none existed
- Fixed — voice varies by context even for the same person

A researcher writing a paper and a message to a friend will have different surface styles, but consistent underlying patterns: their hedging habits, their tendency toward precision, their relationship to the reader.

---

## Voice Profile: What to Extract

When a writing sample is provided via `--voice`, extract the following dimensions:

### 1. Sentence Length Distribution
- Count word lengths of all sentences
- Compute: mean, median, standard deviation
- Identify: does the author write short punchy sentences (< 12 words mean), long complex sentences (> 25 words mean), or mixed?
- **Pattern label**: `tight` / `expansive` / `variable`

### 2. Paragraph Length Distribution
- Count sentences per paragraph
- Identify single-sentence paragraphs (rhetorical emphasis device)
- **Pattern label**: `compact` / `extended` / `mixed`

### 3. Punctuation Habits
- Em-dash frequency (per 1,000 words): `rare` (< 1) / `occasional` (1–4) / `frequent` (> 4)
- Parenthetical use: yes/no
- Colon use for lists vs. elaboration
- Semicolon use: yes/no
- Ellipsis use: yes/no
- Question marks (rhetorical questions in prose)

### 4. Contraction Rate
- Count contractions (don't, it's, I've, etc.) per 1,000 words
- `none` (0) / `rare` (1–3) / `moderate` (4–10) / `frequent` (> 10)

### 5. First-Person Usage
- Count I / me / my / we / our per 1,000 words
- `absent` / `occasional` / `central`
- Note: first-person absence in technical/academic writing is a valid choice, not a deficiency

### 6. Hedging vs. Certainty Balance
- Hedging markers: might, could, perhaps, possibly, appears to, seems to, I think, arguably, in some cases, it's worth noting
- Certainty markers: is, are, will, must, clearly, obviously, certainly, always, never
- **Balance**: `cautious` (hedging dominant) / `assertive` (certainty dominant) / `calibrated` (mixed with purpose)

### 7. Formality Level
Score 1–5:
- 1: Very informal (slang, incomplete sentences, direct reader address)
- 2: Informal (contractions, conversational vocab, occasional fragment)
- 3: Neutral (clear, accessible, no slang, minimal jargon)
- 4: Formal (no contractions, complex sentence structures, discipline vocabulary)
- 5: Very formal (passive constructions, nominalizations, impersonal tone)

### 8. Rhetorical Patterns
- Does the author use **questions** in prose? (genuine or rhetorical)
- Does the author use **direct reader address** ("you", "we")?
- Does the author use **analogies and concrete examples** or stay abstract?
- Does the author use **repetition for emphasis**?
- Does the author make **explicit personal observations** vs. cite external evidence?

### 9. Vocabulary Level
- Approximate reading grade level using Flesch-Kincaid or Gunning Fog
- Identify domain vocabulary (technical, academic, industry, colloquial)
- Note any distinctive personal vocabulary: recurring words or phrases the author favors

### 10. Emotional Intensity
- `flat` (purely informational, no emotional register)
- `measured` (calm, occasional expression of view)
- `engaged` (clearly invested, opinion visible)
- `passionate` (strong personal conviction)

---

## Voice Profile Format

Represent the profile as a structured note:

```
VOICE PROFILE
─────────────────
Source: [n] words from [description of source]

Sentence length:     [mean] words avg, [std] std — [tight/expansive/variable]
Paragraph length:    [n] sentences avg — [compact/extended/mixed]
Em-dash:             [rare/occasional/frequent]
Parentheticals:      [yes/no]
Contractions:        [none/rare/moderate/frequent]
First-person:        [absent/occasional/central]
Hedging balance:     [cautious/assertive/calibrated]
Formality:           [1–5]
Reader address:      [yes/no]
Analogy/example:     [high/medium/low]
Emotional intensity: [flat/measured/engaged/passionate]

Key vocabulary patterns:
  - [any recurring words or phrases]
  - [any distinctive syntactic preferences]
```

---

## Applying the Voice Profile

During Stage 4 (Selective Rewrite), the voice profile operates as a **constraint set**, not a template to copy.

For each rewrite decision, check:
- Does this sentence's length fit the author's distribution?
- Does this punctuation choice match the author's habits?
- Am I using the same hedging/certainty balance as the author?
- Am I matching formality level?
- If the author never uses em-dashes, am I inserting them? (Don't.)
- If the author writes in first person, am I switching to third? (Don't.)

### Voice Preservation vs. Voice Imitation

**Preservation** (default in `--mode preserve`): Keep all stylistic choices that are distinctive to this author, even if they diverge from generic "best practice". An author who writes long sentences should have long sentences after humanization.

**Imitation** (used in `--voice [sample]` mode): Apply the profile from the sample to a text that the author did not write — shape the rewrite to sound like the author would have written it.

**Critical boundary**: Do NOT invent opinions, positions, or specific experiences to fill out a voice. Imitate structure, rhythm, and vocabulary register — not content.

---

## Common Voice Destruction Patterns to Avoid

These are errors made by generic humanizers:

1. **Contraction injection**: Forcing "don't" instead of "do not" in writing that naturally uses the formal form
2. **Fragment insertion**: Adding one-sentence paragraphs to "feel more human" when the author's style doesn't use them
3. **Casualizing technical writing**: Replacing precise technical vocabulary with simpler words in text intended for expert readers
4. **First-person imposition**: Adding "I" where the author consistently avoids it
5. **Enthusiasm injection**: Adding exclamation points or enthusiasm markers where the author's register is measured
6. **Hedging removal**: Eliminating calibrated uncertainty to "sound more confident" — this changes the author's epistemological position
7. **Generic voice substitution**: Replacing a distinctive author voice with the humanizer's default "natural human" template

---

## When Voice Cannot Be Determined

If no sample is provided and the text itself doesn't provide enough signal (e.g., very short input), do not guess. Instead:
- Apply neutral rewriting: address structural patterns but do not impose a voice
- Note in the diagnostic: "Voice profile: insufficient signal — voice-neutral rewrite applied"
- The user can provide a sample and reinvoke with `--voice`
