---
name: not-ai
description: Edit prose into a clear, specific, source-grounded version that preserves the author's meaning and voice. Use for humanizing stiff writing, removing generic phrasing, matching a supplied voice sample, diagnosing robotic prose, or drafting from the user's notes. Do not optimize for AI-detector scores or claim to prove authorship.
---

# Not Ai

Not Ai is an editorial skill, not an authorship test or detector-bypass tool. Its job is to make prose sound like a particular person with particular facts, not like a generic idea of "human writing."

## Non-negotiable rules

1. Preserve facts, names, numbers, citations, technical terms, and the author's actual position.
2. Never invent an experience, opinion, uncertainty, quote, source, result, name, number, or sensory detail if given.
3. Never add mistakes, slang, filler, fake emotion, or "imperfections" to simulate a person.
4. Never optimize against an AI detector, predict a detector score, or claim the result proves human authorship.
5. Do not force a rewrite. If the passage is already strong, return it unchanged or make only the edits that clearly help.
6. Keep code, equations, quotations, citations, table data, and required terminology intact unless the user asks otherwise.
7. If a missing personal detail would materially improve the piece, use a bracketed prompt or ask one concise question. Do not fill the gap yourself.
8. Never add Em Dashes

## Choose the mode

Default to the fullest useful result supported by the user's material. When the user supplies notes, facts, or a brief and asks for new prose, write a complete, detailed draft from scratch using only those supplied facts and views. When the user supplies a passage for revision, rewrite it to its full potential while preserving meaning and protected content. Do not ask for writing samples, build a personal profile, or add onboarding unless the user explicitly requests voice matching.

- `rewrite`: rewrite the whole submitted passage to its full potential while preserving meaning.
- `preserve`: make the fewest edits needed to remove stiffness or ambiguity.
- `diagnose`: identify issues and quote the relevant spans; do not rewrite.
- `from-notes`: write a complete, detailed draft from scratch using only the facts and views the user supplied.
- `voice-match`: use one or more genuine writing samples from the same author as the style reference.

Detector-focused requests do not change the method. Briefly state that detector scores are inconsistent and that the skill will optimize for clarity, specificity, fidelity, and voice instead.

## Establish the writing contract

Before editing, determine these five things from the prompt and text:

1. **Purpose:** what the piece must accomplish.
2. **Audience:** who will read it and what they already know.
3. **Genre:** LinkedIn, personal, email, social, fiction, README, technical, student report, or academic.
4. **Register evidence:** the level of formality and style already present in the draft.
5. **Protected content:** facts, claims, quotations, citations, terminology, formatting, and length constraints that must survive.

Do not interrogate the user when the contract is obvious. Infer the contract silently and use a neutral, direct register when the draft gives weak evidence.

Represent the contract internally as a writing brief:

```text
purpose: what the reader should understand, feel, decide, or do
audience: who the reader is and what they already know
genre: the closest supported profile
register: evidence from the draft or supplied voice sample
protected: facts, claims, quotes, citations, terms, code, and constraints
unknowns: details only the writer can supply
```

## Protect the source before rewriting

Create a private ledger with four columns:

| Type | What belongs here | Editing rule |
|---|---|---|
| Fact | names, dates, numbers, events, results | preserve exactly unless correcting an explicit error |
| Claim | conclusions, opinions, confidence level | preserve strength and direction |
| Voice | idioms, preferred words, humor, formality | retain when natural and intelligible |
| Structure | headings, order, required format | change only when it improves the stated purpose |

Mark unsupported gaps separately. Examples include `[specific result]`, `[what changed your mind]`, and `[example from your experience]`. A bracket is honest; a fabricated detail is not.

## The editorial pass

Work paragraph by paragraph, not with global synonym replacement.

### 1. Find the paragraph's job

Each paragraph should do something identifiable: make a claim, tell an event, explain a mechanism, give evidence, qualify a conclusion, or request an action. If it does none of these, cut it or combine it with the paragraph that does.

### 2. Put the useful information first

Replace broad scene-setting with the fact, action, or question the reader needs. Prefer "The deploy failed at 2:14 a.m." to a generic introduction about the importance of reliable systems.

### 3. Replace abstraction with supported detail

Use details already in the source ledger. Replace "results improved" with the supplied result. Replace emotional shorthand with the event that supports it. If the source does not contain the detail, leave a bracketed prompt instead of inventing one.

Use the genericity counterfactual when a sentence feels polished but empty:
could it survive unchanged if the names, setting, and subject were replaced? If
yes, inspect its job. Keep a necessary bridge, but cut or repair generic praise,
scene-setting, and conclusions with source-backed material.

### 4. Make agency clear

Name who decided, built, observed, or changed something when the source supports it. First person is welcome in personal writing and project reports, but it must reflect the author's real role. Passive voice is fine when the actor is unknown or irrelevant.

### 5. Remove empty framing

Cut phrases that delay the point without changing it, such as:

- `It is worth noting that`
- `In today's fast-paced world`
- `plays a crucial role in`
- `serves as a testament to`
- `This demonstrates the importance of`
- `In conclusion` when the final sentence can simply state the conclusion

Do not ban individual words. Keep any word that is precise, idiomatic for the author, or required by the field.

### 6. Repair rhythm by ear

Read the paragraph as spoken language. Split sentences that carry unrelated jobs. Join choppy sentences when the relationship is clearer together. Vary length only when meaning creates the variation; never manufacture a long sentence, fragment, contraction, or aside to satisfy a numeric target.

Three or more very short declarative sentences in a row often read like notes rather than finished prose. In reports, combine connected items under one controlling idea. Keep a short run only when the genre or emphasis earns it.

### 7. Keep logical transitions, remove mechanical ones

Transitions should name the relationship between ideas. `But` can mark a real contrast. `Because` can name a real cause. `For example` can introduce actual evidence. Delete `Moreover` or `Additionally` only when it is functioning as decoration.

### 8. Preserve uncertainty

Do not turn `may` into `will`, `suggests` into `proves`, or a personal impression into a fact. Keep genuine hedges. Remove ceremonial hedges that merely postpone the claim.

### 9. End on substance

Prefer the final consequence, decision, image, result, or next action. Avoid a summary sentence that repeats the paragraph without adding anything.

## Genre profiles

### LinkedIn and social

- Lead with the actual event, observation, or claim.
- Keep paragraphs easy to scan.
- Use first person only for the author's real experience.
- Avoid manufactured vulnerability, engagement bait, inflated lessons, and decorative emoji.

### Personal essay

- Preserve the author's odd, specific choices and emotional restraint.
- Keep chronology intelligible without sanding away digressions that reveal voice.
- Replace labels such as "inspiring" with supported moments when available.

### Professional email

- Put the purpose or request near the top.
- Match the relationship and level of formality.
- Make owners, dates, and next steps explicit.
- Do not add friendliness the sender did not express.

### Student project report

- First person is appropriate when the student actually did the work.
- Keep methods, datasets, results, limitations, and citations exact.
- Explain decisions using supplied constraints, not invented stories about confusion or discovery.
- Do not simplify technical terms merely to sound casual.
- Avoid forced casualness such as `without going crazy`, `mostly`, or staged fragments unless that register already exists in the source.
- Convert objective checklists into grammatical parallel lists, and combine repetitive one-clause sentences when they share one topic.
- Use `student` when running the bundled gate.

### Formal academic writing

- Preserve disciplinary terminology, cautious claims, citations, and necessary nominalization.
- Prefer precision over conversational tone.
- Do not add first person unless the venue or author uses it.
- Never strengthen causality or generalize beyond the evidence.

### Technical documentation and README files

- Optimize for correctness, navigation, and successful action.
- Use imperative steps where appropriate.
- Keep identifiers, commands, code, warnings, and prerequisites exact.
- Remove marketing language that obscures behavior.

### Fiction

- Preserve point of view, tense, characterization, and intentional repetition.
- Do not normalize dialect or unusual syntax unless asked.
- Add no sensory detail, motivation, or backstory absent from the source.

## Optional voice matching

Use this section only when the user explicitly requests `voice-match` and supplies genuine samples. It is never required for the default workflow. Infer style from repeated evidence rather than stereotypes. Record:

- typical sentence and paragraph shape;
- formality and contraction use;
- directness, humor, and emotional temperature;
- preferred transitions and recurring idioms;
- punctuation and formatting habits;
- how the author opens, qualifies, and closes ideas.

Copy tendencies, not memorable phrases. Never imitate a living author's voice unless the user is that author or has supplied their own text as the target voice. For third-party style requests, describe and use high-level traits instead.

## Quality gate

Review every deliverable against these checks:

1. **Fidelity:** every factual statement and claim is supported by the input or a cited source.
2. **No invention:** no new biography, result, quotation, feeling, stance, or concrete detail appears.
3. **Purpose:** the opening and organization serve the requested outcome.
4. **Specificity:** vague language is replaced only where the source supports something clearer.
5. **Voice:** diction and rhythm fit the available voice evidence and genre.
6. **Logic:** transitions reflect real relationships; references and pronouns are unambiguous.
7. **Restraint:** no needless framing, repeated conclusion, inflated significance, or padded list.
8. **Register:** formality, contractions, fragments, and technical vocabulary fit the audience.
9. **Protected content:** names, numbers, citations, quotations, code, and required terminology survive.
10. **Mechanics:** grammar and punctuation are correct unless the source intentionally departs from them.
11. **Em dashes:** before sending newly authored prose, check for the `—` character and replace every instance with punctuation that preserves the sentence's meaning. Do not alter protected source quotations solely to remove an existing em dash.

The bundled deterministic gate can support the last review:

```bash
python3 tools/gate.py draft.txt --genre linkedin
python3 tools/gate.py draft.txt --genre student --json
```

Its findings are editorial prompts. They do not determine authorship, factual fidelity, writing quality, or a detector outcome. Review every finding in context; do not obey it mechanically.

Use `--protect` once for each literal fact or term that must appear in the
deliverable. Use `--ascii-punctuation` only when the writer or publication has
explicitly requested that house style:

```bash
python3 tools/gate.py draft.txt --genre technical --protect "API v2"
python3 tools/gate.py draft.txt --genre readme --ascii-punctuation
```

## Optional revision receipt

Provide a short revision receipt when the user asks what changed, requests an
audit trail, or when a material ambiguity remains. Include only categories that
apply:

```text
Kept: protected fact, quote, term, or position
Moved: source detail brought forward, with the reader-facing reason
Cut: framing or repetition that added no claim or evidence
Clarified: actor, relationship, request, or qualification supported by source
Needs input: detail or judgment only the writer can supply
```

Do not claim the receipt proves authorship. It explains editorial decisions so
the writer can accept, reject, or correct them.

## Supporting references

Read only the reference relevant to the current problem:

- For cross-genre density or grammar questions, read [the linguistic profile](reference/profile.md).
- For formatting or copied chatbot residue, read [mechanical and presentation review](reference/mechanical-tells.md).
- When editing has collapsed into synonyms, read [why word swapping fails](reference/why-word-swapping-fails.md).
- For clusters of vague or inflated wording, read [vocabulary review](reference/vocabulary.md).
- When explaining the evidence or its limits, read [research sources](reference/research-sources.md).

## Output

For a normal rewrite, return the revised text without a long preamble. Add a short note only when needed to disclose:

- the assumed genre or audience;
- a bracketed fact the author must supply;
- a material ambiguity;
- a fidelity concern;
- that detector-score optimization was not performed.

For diagnosis, use:

```text
Genre: [genre]
Keep: [strong choices worth preserving]
Revise: [issue, quoted span, and reason]
Missing: [information needed for a stronger draft]
```

For an explanation request, summarize the few changes that most improved purpose, clarity, specificity, or voice. Do not report a fabricated quality score.
