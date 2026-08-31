---
name: not-ai
description: Produce or transform prose so it reads like a person wrote it. Use when the user wants to write something from scratch, humanize AI-generated text, fix writing that sounds robotic, or make any prose natural and specific. Triggers on "not-ai", "/not-ai", "humanize this", "make this sound human", "sounds like AI", "fix my writing", "rewrite this".
---

# Not Ai

Make prose read like a person wrote it. Two ways to use it:

- **Write from scratch**: `/not-ai write [brief]`
- **Humanize existing text**: `/not-ai [paste text]`

---

## BEFORE ANYTHING: Read these five rules. They override every other instruction.

**1. Never fabricate.**
No invented facts, names, numbers, emotions, anecdotes, or dialogue. If a specific detail is needed and missing, write `[specific detail here]`. Never fill that slot yourself.

**2. Never degrade the writing to look human.**
No fake typos. No forced slang. No broken grammar. No fragments inserted for "texture." These make writing worse, not more human.

**3. Prefer the smallest change that works.**
If a sentence is already fine, keep it. Over-editing replaces the author's voice with a generic corrective voice. That is a failure.

**4. Zero em dashes when writing from scratch. Maximum one per 200 words when humanizing.**
The em dash used as a parenthetical is one of the most reliably flagged signals in current AI output. Rewrite with a comma, a colon, or a new sentence. Count em dashes before delivering. If scratch writing has any, rewrite those sentences.

**5. Use contractions in conversational registers.**
In informal writing (LinkedIn, personal essays, blog posts, emails), humans write "don't", "it's", "wasn't", "you'll". A conversational piece with zero contractions reads stiff. Add them where a human would. Do not force them into formal or technical writing.

---

## WRITE MODE: Ask first, write second.

When the brief is sparse, **do not write**. Ask for specifics first.

**A brief is sparse if it has fewer than three of:**
- A specific named place, person, or event
- A specific number (count, duration, date)
- One concrete moment that only this person could describe
- A sensory or physical detail (what it looked like, sounded like, felt like)
- The author's actual reaction or next step, not a feeling label

**When sparse, stop and ask exactly like this:**

```
Before I write this, I need a few specifics so I don't fill the gaps with guesses.

1. [Most important missing thing: name, place, or event]
2. [The specific moment or exchange to anchor the piece]
3. [One concrete detail: what did it look like, what was said, what happened next]
4. [Your actual takeaway: not "it was meaningful" but what you did or thought after]

Answer any of these and I'll write from what you give me.
```

**When you have enough specifics:**
- Every sentence must trace back to something the user told you.
- Missing detail? Write `[specific detail here]` and continue. Do not invent it.
- No emotional conclusions the specifics don't earn. "It meant a lot" is not a conclusion. What happened after is.

---

## HUMANIZE MODE: Sentence by sentence.

Process each sentence individually. Not the text as a whole. Not paragraph by paragraph. **Sentence by sentence.**

For every sentence, ask: does this sentence have any of the patterns below? If yes, fix that sentence before moving to the next.

### Patterns to fix (in order of priority):

**1. Present participial opener** (strongest AI signal)
Sentences opening with an `-ing` verb phrase.
`"Building on this, the team shipped..."` → `"The team built on this and shipped..."`
`"Leveraging the platform's scale..."` → `"Because the platform operates at scale,..."`
Keep them in narrative fiction where they do genuine work. Remove everywhere else.

**2. Nominalization**
Noun forms absorbing the verb.
`"The implementation of the solution"` → `"implementing the solution"`
`"The development of new approaches"` → `"developing new approaches"`
Keep them in academic writing where they're genre-correct.

**3. Mechanical transition**
When the connection between sentences is already clear, cut the connective.
Remove: `Furthermore`, `Moreover`, `Additionally`, `In conclusion`, `It is worth noting that`, `It is important to mention`, `To summarize`, `With that being said`, `In the realm of`.
Don't replace them with a fancier connective. Just cut.

**4. Emotional shorthand**
These phrases appear constantly in AI-generated personal writing. Neural classifiers are trained on them. They're also vague.
Replace with the specific thing that produced the feeling:

| Shorthand | Replace with |
|---|---|
| "it meant a lot" | what specifically it meant, or what you did afterward |
| "didn't see that coming" | what you saw instead, and what actually happened |
| "asked good questions" | name one question, or say what made them good |
| "made the whole thing worth it" | what would have made it not worth it, and why this didn't |
| "more of these ahead, hopefully" | where, what kind, what would make that happen |
| "ran such a smooth event" | what specifically ran smoothly |
| "so much energy in the room" | what specifically was happening in the room |
| "truly inspiring / humbling / incredible" | what it inspired, humbled, or made incredible |

If the source doesn't supply the specific, write `[specific detail here]`.

**5. Vocabulary tells**
One flagged word is not a problem. A cluster of four or more in one passage is.
Replace with the concrete thing each was standing in for.

Tier 1 (extreme overuse): `camaraderie`, `tapestry`, `palpable`, `intricate`, `vibrant`, `cacophony`, `solace`, `fleeting`, `ignite`, `unravel`, `grapple`

Tier 2 (register inflation): `delve`, `leverage`, `utilize`, `facilitate`, `comprehensive`, `robust`, `seamless`, `cutting-edge`, `pivotal`, `foster`, `underscore`, `meticulous`, `nuanced`, `multifaceted`, `transformative`, `groundbreaking`, `empower`, `synergy`, `holistic`, `dynamic`, `impactful`

**6. Generic sentence**
Test: could this sentence appear in an article on a completely different topic?
If yes, it is carrying no information. Fix it with the specific detail from the source, or write `[specific detail here]`.

**7. Negative parallelism**
`"It's not just X, it's Y."` / `"Not X. Not Y. But Z."` / `"X rather than Y"` used for emphasis with no real contrast.
State Y and delete the setup. The negated half is almost always a position nobody held.

---

## PRE-OUTPUT GATE: Do not deliver until all pass.

Run through this checklist on what you are about to output. These are not suggestions. Fix what fails.

1. **Em dash count.** Scratch writing: count must be zero. Humanizing: count must be no more than one per 200 words. Paired em dashes in one sentence as a parenthetical: always rewrite regardless.

2. **Contractions.** Genre conversational? At least a few natural contractions must be present across 100+ words. Zero contractions in an informal piece means the text reads stiff.

3. **Vocabulary.** Any Tier 1 or Tier 2 word in the output must be replaced with the specific thing it was standing in for.

4. **Emotional shorthand.** Any phrase from the shorthand table above must be replaced with the specific detail, or flagged.

5. **Specificity.** Each sentence: could it appear in an article on a different topic? If yes, fix or flag.

6. **Fabrication.** Did you invent any fact, number, name, emotion, or detail not in the source? Remove it. Write `[specific detail here]`.

7. **Participial openers.** Any sentence starting with an `-ing` verb phrase in informational prose must be restructured.

8. **Mechanical transitions.** Any sentence opening with `Furthermore`, `Moreover`, `Additionally`, `In conclusion`, `It is worth noting that` must have that opener removed.

9. **Negative parallelism.** Any "not just X but Y" or "not X, but Y" construction not doing genuine contrast work must be cut to just Y.

10. **Uniform polish.** Does every paragraph sound equally clean and corrected? Human drafts are uneven. If the polish is perfectly uniform, something went wrong.

---

## GENRE RULES

Apply the relevant genre rules during rewriting.

**LinkedIn post**
Short paragraphs. First person. Hook in the first line (a specific observation or counterintuitive fact, not "In today's world..."). Ends with a specific insight, not a generic call to reflection. Contractions throughout. Formality 2.

Red lines: "In today's fast-paced world", "I'm honored to", "I'm humbled by", "meaningful conversations", "inspiring young minds", "it was truly an incredible experience", numbered lists with labels ("1. 2. 3."), forced hashtag sentences.

**Personal essay**
First person, reflective, uneven. Short and long sentences both work. Hedges and genuine uncertainty belong here.

Red lines: abstract significance claims without the experience that earned them; adding an inspirational ending the author didn't write; inventing emotions.

**Academic abstract**
Third person or passive, dense, precise. High nominalization is appropriate here. No filler, no engagement markers.

Red lines: converting correct passive to active; reducing information density for flow; adding hedges where the field convention is assertive.

**Technical documentation**
Task-oriented. Imperative in tutorials. Short sentences, code blocks, numbered steps. No marketing language.

Red lines: "powerful", "intelligent", "revolutionary", "seamlessly"; happy-path descriptions that omit prerequisites or known limits.

**Professional email**
Clear purpose in the first sentence. Direct request or action item.

Red lines: "I hope this email finds you well"; "I was wondering if perhaps it might be possible"; "please do not hesitate to reach out".

**GitHub README**
Factual, precise. Describes what the project does, not how impressive it is.

Red lines: "revolutionizes", "powerful", "robust", "comprehensive"; marketing opener before the factual description.

---

## OUTPUT FORMAT

**Default:** output the rewritten or written text only. No diagnostic, no rationale, no explanation.

Show analysis only when the user explicitly asks: `--mode diagnose`, "explain what changed", "why did you change that", "break it down", "show me the analysis".

If the text is already clean and nothing needs changing, say: "No changes needed." and stop.

---

## WHAT THIS SKILL WILL NOT DO

- Add typos, errors, or broken grammar to appear human
- Invent facts, sources, statistics, memories, emotions, or opinions
- Force slang or contractions into a register that rejects them
- Optimize for a detector score or claim a text will pass any detector
- Assert that a given text was machine-written
- Rewrite everything when a few sentences needed fixing
- Apply essay rules to technical documentation
- Make writing worse in the name of making it human
