---
name: not-ai
description: Diagnose and repair the structural patterns that make prose read as machine-written, or write from scratch without them. Use when the user wants text humanized, asks why their writing sounds robotic or like AI, wants AI patterns removed from a draft, or wants something written that will not read as model output. Triggers on "not-ai", "/not-ai", "humanize this", "make this sound human", "sounds like AI", "does this read as AI", "fix my writing".
---

> Generated file. This is the whole skill assembled into one document, built from
> the multi-file repository by `scripts/build_single_file.py`. Edit the source
> files and rebuild rather than editing this. The appendices below are the
> `rules/`, `references/` and `examples/` directories inlined, plus the
> measurement script as text.

# Not Ai

Repair what makes prose read as machine-written, without making it worse.

The target is writing a human reader finds clear and specific. It is not a detector score. A rewrite that fools a classifier while reading worse than the original has failed.

The signals that matter are structural: clause types, information density, cadence, stance. Vocabulary is the smallest part of the problem and the easiest part to fix badly.

## Two modes

| Mode | Invocation | Behaviour |
|---|---|---|
| Humanize | `/not-ai [text]` | Full pipeline. Measure, diagnose, then rewrite selectively. |
| Write | `/not-ai write [brief]` | Stages 0, 4 and 5 only. Apply the rules from the first word rather than repairing afterwards, then measure the result at Stage 5. |

Flags: `--mode diagnose` for a report with no rewrite, `--mode preserve` for minimum edits under strict meaning preservation, `--mode aggressive` when structural surgery is authorised, `--voice sample.md` to match an author sample.

## Five rules that override everything else

1. **Never fabricate.** No invented facts, numbers, sources, anecdotes, emotions or dialogue. Where a specific detail would strengthen a sentence but is absent from the source, write `[specific detail here]` and leave it for the author. A fabricated detail is worse than a generic sentence.
2. **Never degrade the writing to look human.** No inserted typos, no forced slang, no broken grammar, no decorative sentence fragments. These are the marks of a bad humanizer, not of a person.
3. **Prefer the smallest intervention that works.** Sentences that already read well stay untouched. Rewriting everything is the most common failure in this task, and it replaces the author's voice with a uniform corrective voice.
4. **Zero em dashes when writing from scratch. Maximum one per 200 words when repairing.** The paired em dash used as a parenthetical is among the most recognisable signals in current model output. Rewrite with a comma, a colon, or a new sentence. Never use two em dashes in one sentence as parenthetical framing. Before delivering any output, count the em dashes. If writing from scratch and the count is above zero, rewrite those sentences.
5. **Use contractions in conversational registers.** A conversational piece where the model never writes "don't", "it's", "you'll", or "wasn't" reads stiff and formal. Instruction-tuned models underuse contractions at roughly the human rate in informal registers. When the genre is informal (blog, LinkedIn, personal essay, short-form), use contractions where a human would use them. Do not force contractions into formal or technical writing.

## Reference map

Load a section when its stage calls for it. Do not read them all up front.

This is the single-file build, so every file named below is a section of this document rather than a separate file. The section headings are the repository paths, so searching this file for `rules/context.md` finds the section that file became.

| Need | File |
|---|---|
| Genre, audience, register, per-genre red lines | `rules/context.md` |
| Clause structure, nominalization, information density | `rules/structure.md` |
| Cadence, opening repetition, repeated sentence frames, three-item series, length variation | `rules/rhythm.md` |
| Generic versus specific, the evidence rule | `rules/specificity.md` |
| Hedges, boosters, engagement, epistemic stance | `rules/rhetoric.md` |
| Word-level tells and what to do about each | `rules/vocabulary.md` |
| Extracting an author voice and holding it | `rules/voice.md` |
| Full catalogue of observable signs, and the ones that produce false positives | `references/wikipedia-signs.md` |
| Measured feature rates by model | `references/style-research.md` |
| Source studies and what each supports | `references/writing-research.md` |
| Design rationale and honest limits | `references/methodology.md` |

## Pipeline

### Stage 0. Context

Fix genre, audience, register and the author's purpose before looking for anything wrong. Load `rules/context.md`.

State the genre in the diagnostic. When it is inferred rather than given, say so: `Genre assumed: professional email. Correct me if wrong.`

Genre errors propagate through every later stage. Dense nominalization is correct in an academic abstract and wrong in a LinkedIn post. Reader address belongs in an essay and not in API reference documentation. Getting this wrong makes every subsequent edit wrong in the same direction.

### Stage 1. Measure

Measure before judging. The measurement is deterministic and dependency-free, and it keeps the diagnostic from becoming an impression.

This build carries the measurement script as text, under `scripts/measure.py` below. Write that block to a file and run it:

```bash
python3 measure.py input.md
python3 measure.py input.md --json
```

It needs Python 3.10 and nothing else. It reports the same figures as the three scripts in the multi-file repository, so the before-and-after tables in the examples below reproduce against it.

Where the script cannot run, count by hand. Signals in priority order:

| Signal | Direction in instruction-tuned models | Human rate |
|---|---|---|
| Present participial clause openers | 2.2x to 5.3x | 1.7 per 1,000 tokens |
| `that` clause as subject | 2.6x to 3.3x | 2.1 per 1,000 tokens |
| Past participial clauses | 2.7x to 3.1x | relative figure only |
| Nominalizations | about 2.1x | 14.6 per 1,000 tokens |
| Attributive adjectives, demonstratives, downtoners | 1.18x to 1.55x | relative figure only |
| Mean word length | 1.14x to 1.16x | relative figure only |
| Hedges | 0.50x to 0.63x | relative figure only |
| Existential `there` | 0.59x to 0.71x | relative figure only |
| Adverbs | 0.82x to 0.86x | relative figure only |
| Sentence length variation | lower than human | no single figure |

Three absolute human rates appear above because those are the three `references/style-research.md` carries. For the other signals the multiplier was taken from the source and the absolute rate was not, so the cell says so rather than holding a plausible number. Nothing downstream needs the absolute rate: the diagnosis runs on direction.

Two measurement caveats matter, and skipping them produces false diagnoses:

**The script figures and the research figures are different measures.** The human rates above come from Reinhart et al., who parsed dependencies and applied Biber's tagset. The scripts use regular expressions, so `nominalization_density` counts every word ending in `-tion`, `-ment`, `-ness`, `-ity`, `-ance` or `-ence` and reports a much larger number on the same text. Compare a script figure to another script figure, before against after or draft against the author's earlier work. Never compare a script figure to the tagged rate in the table.

**Direction beats magnitude.** A single elevated signal means little. Three or more moving together is the finding worth reporting.

**Two of the checks report without ruling.** `repetition.py` names eight recurring sentence frames, `from X to Y` and `not just X but Y` among them, and warns only where the same frame appears in two consecutive sentences. It also lists every three-item series closing on `and` or `or`, and warns on none of them, because a third item can carry content or can be there for cadence and only a reader can tell which. Neither check has a research multiplier behind it. Both come from the catalogue in `references/wikipedia-signs.md`.

### Stage 2. Diagnose

Name what is there, with quotations. Not a score, not a percentage, not a verdict on whether a machine wrote it. The skill has no way to establish authorship and should never claim to.

```
NOT AI DIAGNOSTIC
Genre:    [genre, and whether it was given or inferred]
Register: [formality 1 to 5, audience]

Working already:
  [quote a sentence that needs no change, and say why]

Patterns found:
  [pattern name]  "[quotation from the text]"
  [pattern name]  "[quotation from the text]"

Vocabulary in context:
  "[word]" Nx  [whether it is a problem here, or fine]

Intervention: none / light / moderate / heavy
```

Report a strength first. It is not politeness. It calibrates the rewrite, because it identifies the register to preserve.

Where the text is already good, say so and stop. `examples/already-natural/` shows this outcome. Finding nothing is a valid result and a common one.

### Stage 3. Voice profile

Only with `--voice`. Load `rules/voice.md` for the ten dimensions and the output block.

The profile is a constraint on the rewrite, not a description of it. Where the sample never uses semicolons, the rewrite introduces none. Where the author writes long unbroken sentences, they stay long.

Without a sample, rewrite neutrally and record `Voice profile: insufficient signal.` Samples under roughly 200 words give an approximate profile at best; say so rather than overfitting to a paragraph.

### Stage 4. Rewrite

Skip entirely under `--mode diagnose`.

One action per sentence: `KEEP` `RESTRUCTURE` `REPLACE` `REMOVE` `MERGE` `SPLIT` `MOVE` `FLAG`

`KEEP` is the default and should be the most frequent action in most texts. `FLAG` marks a sentence that needs a fact only the author holds.

Mode limits: `preserve` permits `RESTRUCTURE` and light `REPLACE`. The default permits judgment across all eight. `aggressive` permits `REMOVE`, `MERGE`, `SPLIT` and `MOVE` freely.

Priority when several problems overlap in one sentence: fix clause structure first, then specificity, then cadence, then vocabulary. Vocabulary last, because a word swap inside a badly built sentence changes nothing that a reader notices.

### Stage 5. Self-review

Two parts, and the first is a measurement rather than a question. A text can satisfy every question in 5b and still come back flagged the moment it is measured, which is the case `examples/linkedin-post/` documents in the other direction.

#### 5a. Measure what you are about to deliver

Run the measurement on the output, not only on the input.

```bash
python3 measure.py output.md
```

This build does not carry `scan_prose.py`, so the dash count and the flagged-vocabulary sweep of the delivered text are done by reading, against the list in the `rules/vocabulary.md` section below.

Under `write` mode this is the only measurement in the run, since there is no input to compare against. Skipping it is how a generated draft with an unexamined profile reaches a reader.

Six conditions, each of them a threshold the measurement already prints, so none was chosen to suit a particular text. A failure is a reason to look at the sentence, never a licence to break rules 1 to 3.

| Condition | Reported under | If it fails |
|---|---|---|
| No back-to-back repeat of a named sentence frame | `REPEATED SENTENCE FRAMES` | Rewrite the second occurrence. The first established the move, and the second is where a reader starts hearing a pattern. |
| Every three-item series has a third item carrying content rather than cadence | `COORDINATED SERIES` | Cut the weakest item and close the series on two. |
| Nominalization density not `high` | `STRUCTURAL SIGNALS` | Restore the verbs, unless dense nominalization is this genre's convention. |
| Stance not `absent`, in a genre that carries stance at all | `EPISTEMIC STANCE` | Mark where the claim is actually uncertain. Do not attach hedges to sentences that are not uncertain. |
| No flagged vocabulary and no em dash, in text written from scratch | `AI-ASSOCIATED VOCABULARY`, and `scan_prose.py` where it is available for the dash count | Replace the word with the thing it was standing in for. |
| Past roughly 120 words: burstiness at 0.30 or above, and at least one sentence under 8 words and one over 25 | `SENTENCE RHYTHM` | Split a sentence carrying two claims, or merge two that carry one between them. |

The word-count qualifier on the last condition is load-bearing. Four sentences cannot fill five length bands, so a short paragraph's burstiness figure is close to noise: the human-written control in `examples/already-natural/` scores 0.200 across 66 words and needs no repair. Below roughly 120 words, read the figure and do not act on it.

Two ways of satisfying that condition that make the text worse. Do not manufacture a short sentence by fragmenting a whole one, which rule 2 prohibits and `examples/personal-essay/rationale.md` records as a version that scored 0.742 and read worse. Do not pad a sentence with a subordinate clause that carries nothing, which trades one tell for another.

#### 5b. Ten-point pre-output checklist (fix anything that fails)

Do not deliver output until all ten pass. These are not suggestions.

1. **Em dash count.** Count the em dashes in what you are about to deliver. If writing from scratch and the count is above zero, rewrite those sentences. If humanizing and the count exceeds one per 200 words, rewrite the excess. Paired em dashes in one sentence as a parenthetical are always rewritten regardless of count.
2. **Contraction check.** If the genre is conversational (blog, LinkedIn, personal essay, short-form, email), does the text use at least a few natural contractions? If there are zero contractions across 100+ words of conversational prose, the text reads stiff. Add them where a human would.
3. **Vocabulary scan.** Read through the output word by word against the list in `rules/vocabulary.md`. Any Tier 1 or Tier 2 word that appears must be replaced with the specific thing it was standing in for.
4. **Negative parallelism.** Scan for "not just X but Y", "not X. Not Y. But Z." and "it's not about X, it's about Y" constructions. Remove them unless the contrast is genuinely doing structural work. This pattern is one of the most identifiable in current model output.
5. **Specificity test.** For each sentence: could it appear unchanged in an article on a different subject? If yes, it is generic. Fix it or flag it.
6. **Tricolon check.** Count three-item lists. If any third item exists for cadence rather than content, cut it to two.
7. **Over-editing.** Did you rewrite sentences that were already working? If so, restore the original.
8. **Fabrication.** Did you introduce any fact, number, name, emotion or detail absent from the source? If so, remove it and write `[specific detail here]`.
9. **Author position.** Did you change the author's stance, hedge a firm claim, or assert a hedged one? If so, restore the original stance.
10. **Voice consistency.** Does every paragraph sound like the same person? Uniform polish is itself a tell; human drafts are uneven.

### Stage 6. Output

**Default: output the rewritten text only.** No diagnostic, no explanation, no rationale. Just deliver the improved prose.

The user asked for the rewrite. Give them the rewrite. If the text is already clean and needs no changes, output it as-is with a single line: "No changes needed."

Show the diagnostic and explanation only when the user explicitly asks for it. Explicit requests include: `--mode diagnose`, "explain what changed", "show me the analysis", "why did you change", "what was wrong with it", "break it down".

Do not volunteer a rationale the user did not ask for. Do not show the stage-by-stage process. Run the pipeline internally, deliver the result externally.

## Structural priorities

Full treatment in `rules/structure.md`. The short version, in the order that matters:

**Present participial clause openers.** The strongest single signal. `Building on this, the team shipped` becomes `The team built on this and shipped`. Keep them in narrative, where `Walking into the room, she noticed the smell` is doing real work. Remove them where they serve as default connective tissue in informational prose.

**Nominalization.** Restore the verb where a noun form has absorbed it. `The implementation of the solution` becomes `implementing the solution`. Keep the noun where the noun is the subject under discussion, and in genres where dense nominalization is the convention.

**Mechanical transitions.** Where the logical link between two sentences is already clear, the connective is dead weight. Cut `Furthermore`, `Moreover`, `Additionally`, `It is worth noting that`, `In conclusion` and their relatives rather than substituting a livelier connective.

**Em dashes.** One of the most recognisable signals, and worth its own rule. Paired em dashes used for a parenthetical aside are close to diagnostic:

> That gap — fluency without judgment — is where the work is.

Rewrite with commas, or split the sentence. Ceiling of one em dash per 200 words when repairing existing text, and zero when writing from scratch. Never two in one sentence as parenthetical framing.

**Cadence.** Uniform sentence length reads mechanical. So does a short, medium, long cycle, which is pseudovariation and a signature of poor humanizing. Length should follow what the sentence is doing.

**Uniform paragraph shape.** Where every paragraph runs claim, three supports, summary, the shape itself is the tell. Let some paragraphs open on evidence. Let one be a single sentence.

## Specificity

The most durable difference between human and machine prose is specificity, not word choice. Load `rules/specificity.md`.

Test each sentence: could it appear unchanged in an article on a different subject? If yes, it is carrying no information.

Repair only where the source supplies the evidence. `Many experts agree` becomes a named source when the text has one, and `some researchers argue` when it does not. Where neither is available, `[specific detail here]`. Never invent the expert.

## What this skill will not do

- Add typos, errors or broken grammar to appear human
- Invent facts, sources, statistics, memories, emotions or opinions
- Force slang or contractions into a register that rejects them
- Force first person onto an author writing in third
- Optimise for a detector, or claim a text will pass one
- Assert that a given text was machine-written, which it cannot know
- Rewrite a whole text when a few sentences needed attention
- Apply essay rules to reference documentation
- Make writing worse in the name of making it human

## Research basis

Structural signals come from peer-reviewed work, principally Reinhart et al. 2025 in PNAS, which measured 66 Biber features across parallel human and model corpora and found the fingerprint originates in instruction tuning rather than scale. Base Llama 3 models sit at 94% to 102% of human rates on the features above; their instruction-tuned counterparts do not.

Figures, per-model tables and full citations: `references/style-research.md` and `references/writing-research.md`. Known limits: `references/methodology.md`.

## Appendix A. Rules

Seven rule sections, loaded per stage. `rules/context.md` comes first because a genre error makes every later judgment wrong in the same direction.

### rules/context.md

#### Rules: Context

Writing that is natural in one context is inappropriate in another. Not Ai must infer or ask about context before applying any intervention. The same text processed without context awareness will produce wrong results.

---

##### Context Dimensions

###### Dimension 1: Genre

Genre is the category of document being written. Genre shapes:
- Expected level of formality
- Expected sentence length and complexity
- Expected use of engagement markers, hedging, first-person
- Expected tone and register
- Whether creativity and variation are valued or whether consistency is required

###### Dimension 2: Audience

Who is reading this? Consider:
- **Expertise level**: Expert in the subject / informed non-expert / general public / complete novice
- **Relationship**: Colleague / employer / client / friend / stranger / professional community
- **Purpose of reading**: To learn / to make a decision / to be entertained / to evaluate / to be persuaded

###### Dimension 3: Publication Context

Where will this appear?
- Private: email, direct message, internal document
- Semi-public: team communication, shared document, internal wiki
- Public: website, social media, published article, open-source README

Publication context affects what is appropriate to say, how directly to say it, and what expectations the reader brings.

###### Dimension 4: Relationship Between Writer and Reader

Formal or informal? First contact or ongoing relationship? Peer or hierarchical? This affects register choices more than genre alone.

---

##### Genre Profiles

Load the appropriate profile based on detected or stated genre.

---

###### LinkedIn Post

**Typical characteristics**:
- First person, professional but personable
- Short paragraphs (2-4 sentences), often with single-sentence paragraphs for visual separation
- Hook opening (observation, question, or statement of the counterintuitive)
- Moderate engagement markers (reader address, questions)
- Ends with insight, question, or invitation to respond
- No em-dashes overload; some bullets acceptable; no academic citations
- Informal formality: level 2-3

**AI patterns to address in LinkedIn**:
- Generic "In today's fast-paced world..." openings → cut
- Excessive bullet lists → reduce to prose where natural
- Tricolon endings: "What have you noticed? Drop it in the comments. I'd love to hear." → genuine versions fine; formulaic versions → revise
- Inspirational platitudes without specific content → flag
- Excessive nominal openings

**Red lines**:
- Do not make it casual slang if the author's voice is professional
- Do not add hashtags unless author provided them

---

###### GitHub README

**Typical characteristics**:
- Technical, precise, imperative
- Short clear sentences
- Code blocks, bullet lists are expected and appropriate
- Minimal first-person (unless project is personal)
- No hedging: the code either does or does not do something
- Formality: level 4

**AI patterns to address in README**:
- Inflated significance: "revolutionizes how developers" → "helps developers"
- Vague feature descriptions: "powerful functionality" → specific features
- Marketing-style opening paragraphs → factual project description
- Generic "comprehensive" / "robust" / "seamless" → specific claims

**Red lines**:
- Do not informalize technical documentation
- Do not remove precision for "naturalness"

---

###### Academic Abstract

**Typical characteristics**:
- Third person or passive, dense, precise
- High nominalization is appropriate
- No engagement markers, no personal asides
- Every sentence carries information, with no filler
- Formality: level 5

**AI patterns to address in academic abstracts**:
- Inflated significance: "This paper represents a landmark contribution" → "This paper presents/demonstrates/analyzes..."
- Vague methodology descriptions → specific method names
- Repetitive summary at the end (abstract already is a summary; do not summarize it again)
- Over-hedged conclusions: "Our results may perhaps suggest the possibility that..." → "Our results suggest that..."

**Red lines**:
- Do not add engagement markers; they don't belong here
- Do not reduce information density; it is appropriate here
- Do not convert passive to active if the field convention uses passive

---

###### Personal Essay

**Typical characteristics**:
- First person, reflective, specific
- Voice and point of view are the primary value
- Specific personal details, observations, and experiences
- Sentence length varies widely: both very short and very long acceptable
- Rhetorical questions, reader address, personal asides all appropriate
- Formality: level 1-3

**AI patterns to address in personal essays**:
- Generalization replacing personal observation: "Many people feel..." → "I noticed..."
- Inflated significance without personal grounding → cut or ground it
- Abstract conclusions without the experience that earned them → flag
- Manufactured emotion (describing feelings not evidenced in the text) → remove

**Red lines**:
- NEVER invent personal experiences, emotions, or observations
- Do not sanitize distinctive personal voice into generic "human" voice
- Do not add inspirational endings if the author did not write one

---

###### Professional Email

**Typical characteristics**:
- Varies widely by relationship and purpose
- Generally shorter than formal reports
- Clear opening statement of purpose
- Direct request or call to action
- Often conversational but professionally appropriate
- Formality: level 2-4 depending on relationship

**AI patterns to address in email**:
- Ceremonial opening: "I hope this email finds you well." → cut unless genuine
- Excessive hedge phrases: "I was wondering if perhaps it might be possible..." → "Could you..." or "I'd like to..."
- Over-formal closing: "Please do not hesitate to reach out" → "Feel free to reach out" or "Let me know"
- Padding: "As I mentioned in my previous correspondence..." → get to the point

**Red lines**:
- Match the existing relationship's tone; don't casualize a formal relationship
- Preserve important qualifications and caveats in professional communication

---

###### Technical Documentation

**Typical characteristics**:
- Task-oriented, accurate, clear
- Second person ("you") common in tutorials; third person in reference
- Numbered lists, code examples, warnings appropriate
- Minimal hedging: either the feature works or it doesn't
- Formality: level 3-4

**AI patterns to address in technical docs**:
- Vague feature claims: "intelligent", "smart", "powerful" → specific capability descriptions
- Generic introductions: "In today's digital landscape..." → "This document explains..."
- Missing prerequisites and limitations: AI often only describes the happy path

**Red lines**:
- Do not reduce accuracy for "flow"
- Preserve all warnings, limitations, and edge cases

---

###### Social Media (Twitter/X, Mastodon, short-form)

**Typical characteristics**:
- Very short
- High information per word
- Fragments, abbreviations acceptable
- Humor, irony, opinions all common
- Formality: level 1-2

**AI patterns to address in social media**:
- Excessive formality → simplify
- Long clausal sentences → break up or cut
- Generic takes → sharpen to specific observation

**Red lines**:
- Do not impose professional formality
- Do not add caveats that destroy the point

---

###### Story / Narrative Writing

**Typical characteristics**:
- Shows rather than tells
- Specific sensory details
- Character perspective and voice
- Sentence rhythm mirrors scene tempo
- Formality: highly variable

**AI patterns to address in narratives**:
- Telling emotions instead of showing: "She felt devastated" → action/gesture/detail
- Abstract narrative summary: "Events unfolded rapidly" → show the events
- Flat event escalation (every scene has the same emotional weight), from StoryScope research
- Over-explained themes: "This illustrates the theme of loss." → remove
- Single-track plots without moral ambiguity: flag for revision

**Red lines**:
- Do not invent plot events, dialogue, or character details
- Do not impose a tidy resolution if the author hasn't written one

---

##### When Genre Is Unclear

If genre cannot be inferred from content and context, state the assumption in the diagnostic:
> "Genre assumed: professional email (please correct if wrong)"

Do not apply a genre profile without acknowledging the assumption.

##### Multi-Genre Documents

Some documents mix genres: a README with a personal story in the intro, a LinkedIn post with technical content. Handle each section according to its sub-genre.

---

##### The Key Principle

Context-appropriate humanization is **not the same intervention for every text**.

A LinkedIn post that reads like an academic abstract is a failure of genre. An academic abstract that reads like a LinkedIn post is a different failure. Not Ai must address both, which means different interventions for different contexts, not a single humanization template applied universally.

### rules/structure.md

#### Rules: Structure

These rules address the structural patterns that research identifies as the primary morphosyntactic fingerprints distinguishing LLM-generated text from human writing. Source: Reinhart et al. (2025), Biber tagset analysis of GPT-4o and Llama 3.

---

##### 1. Present Participial Clause Overuse

**What it is**: Sentences that open or are modified with present participial clauses: "Building on this", "Leveraging the power of", "Drawing from extensive research", "Combining these elements".

**How AI differs**: Instruction-tuned LLMs use present participial clauses at **2.2× to 5.3× the human rate**, 224% to 527% depending on the model, across all registers including fiction, blogs, and news.

**Healthy human variation**: Participial clauses exist in human writing but are used purposefully for simultaneity, causation, or narrative compression, not as default sentence-openers.

**How to detect**: Count sentences opening with -ing verb phrases. `analyze_structure.py` calls the rate elevated above 1 in 12 and high above 1 in 7. Counting by hand, treat anything past 1 in 12 as worth a look, and remember that the script misses participles behind an introductory preposition and any clause that is not an opener.

**How to improve**:
- Convert to a subject-verb structure: "Building on this" → "This builds on" or start fresh with the actual subject
- Convert to a causal clause: "Leveraging the platform's scale" → "Because the platform operates at scale,"
- Cut if the participial clause is merely decorative

**When NOT to modify**: Participial clauses are natural in narrative flow and vivid description. "Walking into the room, she noticed the empty chair" is fine. The problem is their use as generic connective tissue in informational prose.

---

##### 2. Nominalization Density

**What it is**: Nominalizations are nouns formed by adding suffixes to verbs or adjectives: *justification* (justify), *development* (develop), *robustness* (robust), *implementation* (implement), *optimization* (optimize), *enhancement* (enhance), *facilitation* (facilitate).

**How AI differs**: Instruction-tuned LLMs use nominalizations at **about 2.1× the human rate**, 209% to 214% across the models measured, contributing to what researchers call "informationally dense, noun-heavy prose": text that feels formal and abstract even when discussing concrete things.

**Healthy human variation**: Technical and academic writing legitimately uses nominalizations. The problem is using them where a simpler verb form would be clearer and more direct.

**How to detect**: Flag strings of nouns where a verb existed: "the implementation of the solution" vs. "implementing the solution"; "the achievement of the goal" vs. "achieving the goal".

**How to improve**:
- Restore the verb: "the *optimization* of the system" → "optimizing the system" or "to optimize the system"
- Use the active form: "the *development* of new approaches" → "developing new approaches"
- Cut the nominalized phrase entirely if the concept is already clear

**When NOT to modify**:
- When the nominalization IS the subject being discussed ("The *implementation* was flawed"; here we're discussing the implementation itself)
- In genuinely technical contexts where the noun form carries precise meaning
- When the text is academic writing targeting an academic audience

---

##### 3. 'That'-Clause as Sentence Subject

**What it is**: Sentences where a 'that'-clause serves as the grammatical subject: "That the system works effectively demonstrates...", "That these patterns persist shows...", "That progress has been made is evident..."

**How AI differs**: LLMs use this construction at significantly elevated rates. It produces a formal, legalistic quality that rarely appears in natural conversation or informal writing.

**How to improve**:
- Invert: "That X is true" → "X is true" or "It is clear that X"
- Reframe: "That the approach succeeds demonstrates..." → "The approach succeeds, which demonstrates..."
- Use a noun phrase subject instead: "That results improved surprised researchers" → "The improved results surprised researchers"

---

##### 4. Agentless Passive Voice

**What it is**: Passive voice without naming the agent: "Results were obtained", "It was determined that", "The analysis was conducted", "Improvements were made".

**How AI differs**: GPT-4o uses agentless passive at roughly **half the human rate** (surprisingly low; it overcompensates toward active voice), while some other LLMs overuse it. The issue is not passive voice itself but its deployment without purpose.

**Healthy human variation**: Passive voice is genuinely useful when: the agent is unknown, the agent is unimportant, the action matters more than who performed it, or stylistic variety is desirable. Academic and technical writing legitimately uses passive voice.

**How to detect**: Look for passive constructions where the agent is clear from context and the active form would be more direct.

**How to improve** (only when passive is unclear or evasive):
- Restore the agent: "The analysis was conducted" → "We conducted the analysis" or "The team conducted..."
- Only when the agent is known and relevant

**When NOT to modify**: Do not convert all passive to active. That is itself an AI-humanizer cliché. Use judgment.

---

##### 5. Information Density Overload

**What it is**: Packing too many concepts into each sentence, producing prose that is dense but reads as mechanical rather than thoughtful.

**Research basis**: LLMs tend toward "informationally dense" prose across all registers. Even when writing fiction or blog posts, they default to an academic-adjacent information density.

**Signs**:
- Multiple nominalized phrases in one sentence
- Stacked prepositional phrases
- Compound subjects + compound predicates + embedded clauses
- Sentences that convey 4+ concepts at once

**How to improve**:
- Split into two or three sentences
- Move background information to a separate sentence earlier
- Cut information that was already established

**When NOT to modify**: Technical documentation, legal writing, and academic abstracts are legitimately dense. Density is only a problem when it exceeds audience expectations.

---

##### 6. Symmetrical Paragraph Structure

**What it is**: Every paragraph follows the same shape: topic sentence → three supporting sentences of similar length → closing sentence. When every paragraph uses this structure, the writing feels formulaic.

**How AI differs**: LLMs are trained on well-structured text and tend to produce the academic "paragraph model" regardless of genre or intent.

**Healthy human variation**: Human paragraphs vary in length, shape, and density. A paragraph might be a single sentence. A paragraph might open with an example rather than a claim. A paragraph might have no topic sentence at all.

**How to improve**:
- Vary paragraph length deliberately
- Allow some paragraphs to open with evidence rather than claim
- Allow some paragraphs to have no explicit topic sentence when the flow is clear
- Allow a very short paragraph (1-2 sentences) after a long one for rhythm

**When NOT to modify**: Instructional content and certain formal genres benefit from consistent paragraph structure. Do not introduce arbitrary variation.

---

##### 7. Structural Parallelism Overdrive

**What it is**: Every list item follows the exact same grammatical form. Every bullet point is the same length. Every section header follows the same template. Every example is introduced with the same phrase.

**Healthy use**: Parallelism improves readability in lists and comparisons. The problem is when it extends uniformly across an entire document, removing natural variation.

**How to improve**:
- Allow one or two list items to be longer or shorter than the others
- Vary the sentence structure of section-opening sentences
- Allow different types of evidence (statistic, example, quote, analogy) rather than repeating one type

---

##### Summary: Structural Priority Order

When choosing which structural issues to address, prioritize:
1. Present participial clause overuse (strongest signal, easiest to fix)
2. Nominalization density (second strongest signal)
3. Information density overload (affects readability most)
4. Symmetrical paragraph structure (affects naturalness most)
5. 'That'-clause subjects (context-dependent)
6. Structural parallelism (only when extreme)
7. Passive voice (only when genuinely evasive or unclear)

### rules/rhythm.md

#### Rules: Rhythm

Rhythm is the felt pattern of movement through a piece of writing. It emerges from sentence length variation, sentence structure variation, and paragraph pacing. When rhythm is mechanical, when every sentence is the same length or alternates between two lengths in a predictable cycle, the writing reads as generated, not composed.

---

##### Why AI Writing Has Mechanical Rhythm

Two statistical forces create LLM rhythm problems:

**1. Uniformity**: Models trained to produce "good" text learn that medium-length sentences (18-28 words) are frequently rewarded. This produces prose where sentence length variance is low.

**2. Pseudovariation**: Humanizer tools (and RLHF feedback) teach models to alternate short-medium-long sentences in a detectable cycle. This produces the impression of variation while being statistically uniform at a higher level of analysis.

Both patterns are distinguishable from human writing, which has irregular, contextually-motivated length variation.

---

##### Diagnosing Rhythm Problems

###### Sentence Length Uniformity

Compute (or estimate) sentence lengths for the passage.

**Signs of mechanical rhythm**:
- Standard deviation < 5 words (all sentences nearly the same length)
- No sentence shorter than 10 words in a 500-word passage
- No sentence longer than 30 words in a 500-word passage
- A regular alternating pattern: long-short-long-short

**Signs of natural rhythm**:
- Standard deviation > 8-10 words
- Occasional very short sentences (5-8 words) for emphasis
- Occasional complex sentences (35+ words) for elaboration
- Irregular variation: long passages broken by a short punch, not cycling

###### Opening Word Repetition

Check the first word of each sentence. If 3 or more sentences in a paragraph begin with the same word (especially "The", "This", "It", or "In"), the rhythm is mechanical. `analyze_structure.py` warns at the same count of 3, but across the whole file rather than per paragraph, so on anything longer than a page its warning fires on texts whose paragraphs are fine.

Specifically watch for:
- Multiple consecutive sentences starting with "The"
- Multiple consecutive sentences starting with "This"
- Multiple consecutive sentences starting with "In" (In addition, In fact, In conclusion, In summary)
- Multiple consecutive sentences starting with a participial phrase ("Building", "Leveraging", "Using")

###### Sentence Frame Repetition

A first-word check catches the easy version of this problem. The hard version repeats the shape of the sentence while changing every word in it, so no repeated-opening and no repeated-phrase check fires:

> Its history stretches from the Indus Valley cities through the Mughal era to independence. Geography here swings from Himalayan peaks to tropical coastlines.

Two sentences, no shared phrase to count, the same move performed twice: a range swept end to end. `repetition.py` names eight such frames and warns only where one lands in two consecutive sentences. Adjacency is the smallest window available, which is what makes it the one window with no threshold to argue about.

The eight, with the name the script prints:

- `range sweep`: from X to Y, from X through Y
- `comparative than`: more X than Y, fewer X than Y
- `superlative membership`: one of the most X, one of the largest X
- `scale superlative`: the world's largest X, the industry's fastest X
- `not just X but Y`: also `not merely`, `not only`
- `comma plus -ing word`: a comma, then a word ending in -ing
- `comma plus -ed by`: a comma, then a past participle and `by`
- `where X meets Y`

Repair the second occurrence rather than the first. The first reads as a choice, and the second is where a reader starts hearing a template. Where both sentences need their range, keep one as a range and give the other its facts in plain order.

The last two names describe the string matched rather than the grammar, deliberately. `In conclusion, caching remains an indispensable tool` matches `comma plus -ing word` and contains no participial phrase at all, so a name like participial tail would claim more than the regex delivers.

###### Three-Item Series

Every book on style recommends the rule of three, which is why models produce it constantly. A three-item list becomes a problem when the third item exists to complete the cadence:

> powered by a young workforce, a booming tech sector, and cities like Bengaluru

Test it by deletion. If cutting the third item loses information, keep it. If cutting it loses only rhythm, cut it, and the sentence lands harder on two.

`repetition.py` lists every three-item series that closes on `and` or `or`, and warns on none of them, because that deletion test needs a reader. It does warn where all three items open on the same word, since anaphora across three items is a stronger signal than the list.

###### Transition Word Overload

High-frequency transition words break rhythm by signaling connections explicitly rather than allowing them to be felt:

**Mechanical connectives to reduce**:
- "Furthermore," / "Moreover," / "Additionally,"
- "In conclusion," / "To summarize," / "In summary,"
- "It is worth noting that" / "It is important to mention"
- "Having said that," / "With that being said,"
- "At the end of the day,"
- "Last but not least,"
- "In the realm of"
- "When it comes to"

Note: these words are not wrong. They are wrong when they appear at a density that creates a mechanical feel, with every other sentence beginning with one.

---

##### Improving Rhythm

###### Intervention 1: Break the Uniform Pattern

If every sentence is 20-25 words, look for:
- A sentence that makes a single strong point → shorten it to that point only
- Two sentences that are actually one complex thought → merge them
- A sentence with an embedded subordinate clause → pull the clause into its own sentence

The goal is **motivated variation**: length changes that reflect the content's weight, not arbitrary cycling.

###### Intervention 2: Place a Short Sentence for Emphasis

Short sentences work when:
- A conclusion is being stated
- A reversal is being introduced
- An important fact needs to land without noise

Example (before):
> "The results demonstrated that the approach was significantly more effective, producing a 40% improvement over the baseline methodology that had been in use for the previous three years."

After (with emphasis):
> "The results were decisive. The new approach outperformed the baseline by 40%, closing a gap that had been stable for three years."

###### Intervention 3: Vary Sentence Openings

A simple intervention with high impact:
- If several sentences start with "The [noun] [verb]", reorder one to start with a prepositional phrase
- If several sentences start with "This [verbs]", reorder one to start with the consequence
- Introduce occasional sentences starting with adverbs, conjunctions, or dependent clauses

###### Intervention 4: Vary Paragraph Length

If every paragraph is 4-5 sentences, introduce:
- One 2-sentence paragraph for emphasis or transition
- One longer paragraph for dense explanation
- Occasionally, a single-sentence paragraph for rhetorical effect (only when the author's voice permits)

---

##### What Not to Do

**Do not introduce artificial fragments for "variety".**
"The solution was elegant. And fast. Very fast." That is not natural human rhythm; it is humanizer-voice rhythm. Readers notice it.

**Do not cycle deliberately.**
Short-medium-long-short-medium-long is as mechanical as all-medium. True variation is irregular.

**Do not over-correct.**
If a piece of writing has a deliberate, measured, consistent rhythm appropriate to its register (a legal brief, a formal report), do not disrupt it. Rhythm improvement should never reduce the quality of writing that already has appropriate rhythm.

---

##### Genre-Appropriate Rhythm

Different genres have different natural rhythm profiles:

| Genre | Typical Rhythm |
|-------|----------------|
| Personal essay | High variation, short punchy statements mixed with long reflective sentences |
| Technical documentation | Medium-length uniform sentences (this is appropriate, not a problem) |
| Academic abstract | Dense, longer sentences: information packed |
| Social media / LinkedIn | Short punchy sentences, fragments acceptable |
| News | Inverted pyramid, front-loaded, varied length |
| Fiction | Highly contextual: mirrors character emotion and scene pace |
| Email | Varied, often shorter than formal prose |
| README | Concise, often imperative |

Do not apply personal essay rhythm to technical documentation, or technical documentation rhythm to personal essays.

---

##### Rhythm and Reading Aloud

A practical test: read the text aloud. If you find yourself breathing at exactly the same intervals throughout, the rhythm is mechanical. Natural prose creates varied breath patterns: some sentences make you rush forward, others slow you down.

If available, recommend this test to the author after rewriting.

### rules/specificity.md

#### Rules: Specificity

The most persistent quality gap between AI-generated prose and human writing is not vocabulary. It is **specificity**. LLMs generalize. Humans who know something specific say the specific thing.

---

##### What Specificity Is

Specificity is the quality of referring to concrete, particular things rather than abstract categories. It manifests in:

- **Specific examples** instead of "for example, various methods exist"
- **Specific numbers** instead of "a significant portion"
- **Specific names** instead of "industry leaders"
- **Specific observations** instead of "many people have noted"
- **Specific consequences** instead of "this can have negative effects"
- **Specific time** instead of "in recent years"
- **Specific places** instead of "in many regions"

---

##### How AI Generates Generic Text

LLMs are trained to produce text that is broadly applicable across many contexts. This creates a systematic bias toward generality:

- "This approach has been shown to improve outcomes" (whose outcomes? which approach? in which study?)
- "Organizations across various sectors have adopted this methodology" (which organizations? what methodology?)
- "The implications of this trend are significant" (what implications? significant how? for whom?)
- "Research suggests that..." (which research? who conducted it? when?)

This generalization is not malicious; it reflects the model's statistical tendencies. But it produces writing that reads as authoritative while conveying little actual information.

---

##### The Specificity Test

For each claim, ask:
> "Could this sentence appear in an article about a completely different topic?"

If yes, it is generic. Generic sentences are candidates for improvement, **but only if evidence exists in the source text to make them specific**.

---

##### Critical Rule: Evidence Must Already Exist

**Never invent specificity.**

If the source text says:
> "I attended the conference and learned a great deal."

Do not transform it into:
> "At the Tuesday morning session, I remember the speaker's point about distributed systems..."

Unless "Tuesday morning", "distributed systems" appear in the author's notes or context, you are inventing. This violates the core principle.

The correct action when specificity is missing and no evidence exists:
- **Flag** the generic statement in the diagnostic
- In `--mode preserve`: leave it unchanged
- In `--mode rewrite`: ask the author what specific detail they had in mind, or leave a placeholder: `[specific example here]`
- Never fabricate the detail

---

##### Types of Generic Patterns to Flag

###### Type 1: Inflated Significance
**Pattern**: Claims inflated beyond what the text demonstrates.

Examples:
- "This represents a paradigm shift in how we think about..."
- "This fundamentally transforms the landscape of..."
- "In an era of unprecedented change..."
- "This breakthrough has far-reaching implications..."

**The question to ask**: Does the surrounding text actually demonstrate this significance, or is this rhetorical inflation?

**Intervention**: If the evidence doesn't support the claim, soften it or remove it. If the evidence does support it, the sentence may be fine.

###### Type 2: Vague Quantification
**Pattern**: Quantities without grounding.

Examples:
- "a significant number of users"
- "many experts agree"
- "studies have shown"
- "in recent years"
- "across multiple domains"
- "a growing body of evidence"

**Intervention**:
- If the source has a specific number, use it
- If no specific number exists, prefer the honest vague form ("some users", "a few studies") over the inflated form ("many", "numerous", "a growing body")
- Do not invent numbers

###### Type 3: Anonymous Authority
**Pattern**: Citing unnamed authorities or vague consensus.

Examples:
- "experts say"
- "researchers have found"
- "studies indicate"
- "industry leaders note"
- "it is widely acknowledged that"

**Intervention**:
- If the source cites a specific person or study, ensure their name appears
- If no specific source exists in the text, use an honest hedge: "it is sometimes argued that" or remove the authority claim
- Do not fabricate specific names or citations

###### Type 4: Abstract Summaries Without Evidence
**Pattern**: Drawing conclusions before presenting the evidence, or substituting summary for explanation.

Examples:
- "This demonstrates the power of collaborative approaches."
- "The results clearly illustrate the importance of careful planning."
- "This shows why innovation matters."

**Intervention**:
- If the preceding text contains actual evidence, the summary may be redundant; remove it
- If the preceding text does not contain the evidence the summary claims, flag it

###### Type 5: Generic Examples
**Pattern**: Examples that aren't actually examples.

"For example, consider a situation where..." (no specific situation)
"This can be seen in fields such as technology, healthcare, and education." (naming categories, not examples)
"Various applications exist, including..." (then listing categories, not applications)

**Intervention**:
- Request or flag for actual examples
- If the source provides specific examples elsewhere, move them here
- Do not fabricate examples

###### Type 6: Removed Concreteness
**Pattern**: AI rewrites sometimes abstract away specificity that existed in the original.

If the user's source says "I spent 11 months building this" and a previous AI rewrite produced "after a substantial development period", restore the original number.

Always check the source against the AI-generated text for **removed specificity**.

---

##### Appropriate Generality

Not every general statement needs to be specific. Some situations call for generality:

- **Introductions** that frame a topic before diving into specifics
- **Conclusions** that draw general lessons from specific evidence
- **Abstracts** that summarize without repeating all detail
- **Audience-appropriate simplification** in writing for non-expert readers
- **Policy statements** that intentionally apply to broad contexts

The test: Is the generality serving the reader, or is it covering for absent knowledge?

---

##### The Specificity Hierarchy

When improving a passage, prefer interventions in this order:

1. **Use a specific detail already in the source text**: always the first choice
2. **Use a specific detail from context the user has provided**: second choice
3. **Preserve the vague form with an honest hedge**: only when no specific detail exists
4. **Flag for the author to fill in**: in [bracket] form
5. **Remove the generic claim**: only when it adds no value even in general form

Never add specificity that has no basis in available evidence.

### rules/rhetoric.md

#### Rules: Rhetoric

Rhetoric is how writing positions itself in relation to its reader: how it argues, acknowledges uncertainty, engages, and signals the author's attitude. Research comparing LLM and human writing finds systematic rhetorical differences that are more diagnostic than vocabulary choices.

---

##### Research Basis

From Jiang & Hyland (2025), comparing GPT-4 to student essays:
- LLM essays show "significantly lower frequency of interactional metadiscourse, such as hedges, boosters, and attitude markers, leading to a more impersonal and expository tone"
- Student essays demonstrate "higher rhetorical engagement, employing nuanced stance markers and personalised expressions to foster reader interaction"
- LLMs exhibit "fewer engagement markers, particularly questions and personal asides"
- LLM "bundles are more rigid and formulaic": noun and preposition-based, rather than epistemic stance markers

From Reinhart et al. (PNAS 2025):
- LLMs have measurably different rates of hedging phrases, phrasal coordination, and clausal coordination
- These patterns persist across genres; LLMs fail to adapt their rhetorical register to fiction, blogs, or conversation the way humans do

---

##### Rhetorical Dimension 1: Epistemic Stance (Hedging and Certainty)

**What it is**: Epistemic stance markers indicate the writer's degree of confidence in a claim.

**Hedges** (soften commitment): might, could, may, perhaps, possibly, appears to, seems to, tends to, I think, one could argue, arguably, in many cases, it seems that, evidence suggests

**Boosters** (strengthen commitment): clearly, obviously, certainly, definitely, it is evident that, undoubtedly, without question, it is clear that

**How AI differs**:
- Instruction-tuned LLMs often drop hedges in favor of assertive declarations
- They also overuse certain hedge phrases at formulaic insertion points: "It's worth noting that", "It is important to mention", "It should be noted that"
- The natural human calibration, hedging where genuinely uncertain and asserting where confident, is replaced by a flat assertive tone with ceremonial hedge phrases dropped in periodically

**How to improve**:
- If a claim is genuinely uncertain, ensure the hedge is genuine (not formulaic): "It seems that" instead of "It is clear that"; "evidence suggests" instead of "evidence proves"
- Remove ceremonial hedges that don't soften anything: "It is worth noting that the sky is blue" → "The sky is blue" or cut it
- Restore certainty markers where the author is making a strong, well-supported claim
- Do not reduce all assertions to hedges; that is its own error

###### Recognizing False Hedges

A false hedge is a hedge phrase that precedes a maximally certain claim:
- "It is worth noting that this represents a fundamental transformation..." (the hedge adds nothing; the claim is absolute)
- "Importantly, it should be recognized that this is clearly the best approach..." (hedging a certainty)

Remove the hedge phrase or soften the underlying claim, but not both.

---

##### Rhetorical Dimension 2: Engagement Markers

**What it is**: Engagement markers invite the reader into the text: questions, direct address, anticipating objections, and acknowledgment that the reader has a perspective.

**Types**:
- **Questions**: "Why does this matter?" / "What does this mean in practice?"
- **Direct reader address**: "you'll notice", "consider your own experience", "if you've worked with..."
- **Inclusive 'we'**: "We can see that...", "Let's examine..."
- **Anticipating objections**: "One might argue that..." / "Critics have suggested..." / "A reasonable objection is..."
- **Personal asides**: "(I should mention...)", "for what it's worth"

**How AI differs**: LLMs produce engagement markers at significantly lower rates than humans in essay and argumentative writing. The result feels authoritative but impersonal, like a textbook rather than a conversation.

**How to improve**:
- Check whether the text ever directly acknowledges the reader
- If the genre permits (essay, blog, email, social media), add one or two engagement markers naturally
- Do NOT add engagement markers to genres where they are inappropriate: technical documentation, academic abstracts, formal reports
- Do NOT add forced questions to seem more human: "So, what's the takeaway?" is a humanizer cliché

---

##### Rhetorical Dimension 3: Attitude Markers

**What it is**: Attitude markers convey the author's emotional or evaluative stance toward the content.

Examples: unfortunately, surprisingly, remarkably, disappointingly, crucially, importantly, interestingly, thankfully

**How AI differs**: LLMs use attitude markers, but often use them at high frequency in a way that feels evaluative without genuine feeling. "Importantly, this represents...", "Crucially, the system...", "Remarkably, results showed...": these become verbal tics that don't reflect genuine authorial judgment.

**How to improve**:
- Keep attitude markers that reflect the author's genuine position
- Remove attitude markers that function as rhetorical throat-clearing: "Importantly, X happened" → "X happened"
- If an attitude marker is present, ask: does the surrounding text support this attitude? If "remarkably" is used, is the thing actually remarkable in context?

---

##### Rhetorical Dimension 4: Formulaic Transition Patterns

**What it is**: Transition phrases that indicate logical relationships between sentences or paragraphs.

**Common AI transition overuse**:
- "Furthermore," / "Moreover," / "Additionally,": used between sentences that don't require a formal bridge
- "On the other hand,": used without a genuine contrast preceding it
- "In addition to the above,": usually redundant
- "As a result," / "Consequently," / "Therefore,": overused even when causation is already clear from content
- "In conclusion," / "To summarize," / "In summary,": often redundant when the conclusion is obvious

**How AI differs**: LLMs have higher rates of explicit transition markers because they signal structure clearly, a behavior reinforced by RLHF feedback rewarding "well-organized" text. But human writers rely more on **implicit logical flow**, using transitions only when genuinely needed.

**How to improve**:
- If two sentences have a clear logical relationship without a transition, remove the transition
- If the transition names a relationship that isn't there (e.g., "Therefore," before a sentence that isn't a conclusion), either remove it or rewrite to create the actual relationship
- Reserve formal transitions for cases where the reader would otherwise miss the logical move

---

##### Rhetorical Dimension 5: Repetitive Summaries

**What it is**: Ending a section or argument with a sentence that restates what was just said.

Common pattern:
> [Three paragraphs explaining X] → "In summary, X is important because [restate everything just said]."

**How AI differs**: LLMs are strongly trained to "conclude" and "summarize"; this pattern is reinforced by RLHF. The result is redundant summary sentences at the end of nearly every section.

**How to identify**: After reading a section, ask: "Does the final sentence add anything, or does it restate the previous sentences?" If restating, it's a candidate for removal.

**How to improve**:
- Remove the restatement if the content already made the point clearly
- If a summary is genuinely needed (long complex argument), make it add new value rather than restate: a consequence, a question, a forward-looking statement

---

##### Rhetorical Dimension 6: The Tricolon Habit

**What it is**: A tricolon is a set of three parallel items: "X, Y, and Z." LLMs use tricolons compulsively because they feel balanced, complete, and literary.

**Problem**: Tricolons used for everything feel mechanical. Not every idea comes in threes. Sometimes two items is the right number. Sometimes four. Sometimes one.

**How to detect**: Count three-item lists in prose. More than one per paragraph is elevated.

**How to improve**:
- If you have three items and the third adds genuine value, keep it
- If the third item was added to reach three, remove it
- If you have four genuine items, use four; don't cut one to reach three
- Sometimes a two-item contrast ("X, not Y") is sharper than a tricolon

**Not a problem**: Tricolons in contexts where three genuinely is the right number. This is about compulsive use, not the pattern itself.

---

##### Rhetorical Dimension 7: Negative Parallelism

**What it is**: A pattern of stating what something is not, often as a rhetorical setup: "Not X. Not Y. But Z."

**How AI uses it**: This pattern appears frequently in AI-generated motivational and professional writing. It has a rhetorical energy that LLMs learned from persuasive human writing, but its compulsive use is now recognizable.

**When to keep it**: When the contrast genuinely sharpens the argument and the author's voice uses it.

**When to remove it**: When it feels added for drama rather than serving a real rhetorical purpose.

---

##### Rhetorical Dimension 8: Authorial Presence

**What it is**: The degree to which the author's own perspective, judgment, and experience are visible in the text, as opposed to purely reporting facts and arguments.

**How AI differs**: LLMs produce "expository tone": informational, organized, but detached. The author's presence is minimal.

**How to improve**:
- Only if the author's voice permits (check voice profile)
- In genres that benefit from authorial presence (essays, opinion pieces, personal writing), ensure the author's actual view appears, not just a neutral presentation of multiple views
- Do NOT invent an opinion; only restore or sharpen one that is present in the source but was smoothed away

---

##### When Not to Change Rhetoric

Some genres deliberately minimize rhetorical engagement, hedging, and attitude markers:
- Legal documents
- Medical/scientific abstracts  
- Technical reference documentation
- News reporting
- Terms of service / policy documents

In these contexts, the apparent "lack of engagement" is a feature of the genre, not a deficiency. Do not impose engagement markers or attitude markers on writing that is correctly impersonal.

### rules/vocabulary.md

#### Vocabulary

Word-level tells and what to do about each.

Read this last. Vocabulary is the weakest of the signals this skill measures and the easiest to fix in a way that makes writing worse. A text with every flagged word swapped out and its clause structure untouched still reads as machine-written, because a reader responds to sentence shape before word choice. Fix structure first. See `rules/structure.md`.

##### Why word lists mislead

Every word below is a real English word that good writers use. None of them is evidence of anything on its own. Three properties decide whether a flagged word is a problem:

**Density.** One instance of `intricate` in 800 words is a word choice. Five instances alongside `tapestry` and `palpable` is a pattern.

**Load.** Does the word carry information, or does it signal quality the surrounding text has not earned? `A comprehensive review of 340 filings` is doing work. `A comprehensive understanding of the challenges` is not.

**Register fit.** `Utilize` is correct in an engineering specification where it means "put to use as a resource" and inflated in an email where `use` was the word.

A flagged word that passes all three stays. Removing it is over-editing.

##### Tier 1: measured extreme overrepresentation

Reinhart et al. compared word frequencies between human writers and instruction-tuned models on matched prompts. These appeared in GPT-4o and GPT-4o Mini output at roughly 84 to 171 times the human rate, which is the largest lexical gap in the study:

```
camaraderie   tapestry     palpable     intricate    underscore
unspoken      amidst       solace       fleeting     vibrant
cacophony     grapple      ignite       unravel
```

The concentration is the finding. Several of these words cluster in a single paragraph of model output in a way that essentially does not happen in the human corpus. `Camaraderie` and `cacophony` are the sharpest, because a human writer reaches for either perhaps once a year.

Repair: delete rather than substitute. `A palpable sense of camaraderie` almost always sits on top of a specific thing that the text has not said. Ask what actually happened, and if the source does not say, write `[specific detail here]`.

##### Tier 2: register inflation

These signal significance instead of demonstrating it. Common in model output across every genre:

```
delve            leverage / leveraging    utilize        facilitate
comprehensive    robust                   seamless       cutting-edge
pivotal          foster                   meticulous     multifaceted
myriad           transformative           groundbreaking empower
impactful        synergy                  holistic       dynamic
nuanced          realm                    landscape      elevate
harness          unlock                   revolutionize  paradigm shift
```

Repair by asking what the word is doing. `Leveraging the platform` becomes `using the platform`, or better, name what the platform did. `A robust solution` becomes the property that makes it robust: it retries, it survives a node loss, it has no single point of failure.

`Nuanced understanding` deserves separate mention. It is a construction that claims subtlety while supplying none, and it is nearly always deletable with no loss.

##### Tier 3: phrase templates

Longer patterns, and more reliable than single words because a human writer rarely produces them by accident:

| Template | Repair |
|---|---|
| `It is important to note that X` | State X. The frame adds nothing. |
| `It is worth noting that X` | Same. If X is worth noting, note it. |
| `In today's fast-paced world` | Cut. Every instance. |
| `In the realm of X` | `In X` |
| `Studies have shown that X` | Name the study, or write `some research suggests` |
| `Many experts agree that X` | Name an expert, or drop the appeal |
| `X plays a crucial role in Y` | `X does [specific thing] in Y` |
| `X serves as a testament to Y` | `X shows Y` |
| `This underscores the importance of X` | Cut, or say what follows from X |
| `Navigating the complexities of X` | `Working on X`, or name the complexity |
| `X is a double-edged sword` | Name both edges |
| `At the intersection of X and Y` | Say what the two have to do with each other |
| `Furthermore, / Moreover, / Additionally,` at paragraph start | Cut. The paragraph break already signals continuation. |
| `In conclusion, as we have seen` | Cut the sentence. Add something new or stop. |

##### The sentence shapes

Two constructions matter more than any word:

**Negative parallelism.** `It is not just X, it is Y`. Also `Not X, but Y`, and `X rather than Y` used for emphasis rather than contrast. This is among the most recognisable patterns in current model output, and it survives most humanizing passes because it contains no flagged vocabulary. Repair by stating Y and dropping the setup, since the negated half is usually a straw position nobody held.

**The rule of three.** Three parallel items where the third carries no information beyond the first two, chosen for cadence. `Faster, cheaper, and more reliable` where the text only supports speed. Cut to what the evidence supports. Two items with substance beat three with padding.

##### What models use less than humans

The gap runs both ways, and the underuse side is harder to fake:

**Contractions**, in registers where a human would contract. A conversational piece with no `don't` or `it's` reads stiff.

**Profanity and blunt language**, at over 100 times lower than the human rate in matched contexts. Not something to add, but worth noticing: heavily sanitised prose in a register that tolerates bluntness is itself a signal.

**`i.e.` and `e.g.`**, also over 100 times rarer in model output.

**Exact figures.** Models prefer `significantly`, `substantially` and `dramatically` where a human writer who knew the number would give the number. See `rules/specificity.md`.

**Hedges.** Instruction-tuned models hedge at roughly half to two thirds the human rate. Human experts write `probably`, `I think`, `as far as I can tell`. Adding a hedge that reflects real uncertainty in the source is a legitimate repair. Inventing uncertainty the author does not have is not.

##### Failure modes when repairing vocabulary

**Thesaurus voice.** Swapping each flagged word for a synonym produces text with the same skeleton and a stranger surface. `Utilize` to `employ` fixes nothing.

**Corrective uniformity.** Applying the same substitutions across a whole document flattens the author's variation and leaves a signature of its own.

**Genre blindness.** `Nominalization`, `implementation` and `utilization` are correct in an academic abstract. `Robust` is correct in systems engineering, where it has a technical meaning. Check `rules/context.md` before flagging.

**Chasing the list.** These lists describe models observed through 2025. Vendors adjust. A list treated as permanent truth will misfire on newer output and on human writers who happen to like a flagged word. Treat every entry as a prompt to look at the sentence, never as a verdict.

### rules/voice.md

#### Rules: Voice

Voice is the set of consistent stylistic choices that make a piece of writing feel like it comes from a specific person. Not Ai's purpose is not to impose a generic "human" voice but to preserve or reconstruct the author's own voice.

---

##### What Voice Is Not

Voice is not:
- A writing quality tier ("formal" vs. "casual")
- A set of superficial quirks to copy
- An excuse to invent personality where none existed
- Fixed: voice varies by context even for the same person

A researcher writing a paper and a message to a friend will have different surface styles, but consistent underlying patterns: their hedging habits, their tendency toward precision, their relationship to the reader.

---

##### Voice Profile: What to Extract

When a writing sample is provided via `--voice`, extract the following dimensions:

###### 1. Sentence Length Distribution
- Count word lengths of all sentences
- Compute: mean, median, standard deviation
- Identify: does the author write short punchy sentences (< 12 words mean), long complex sentences (> 25 words mean), or mixed?
- **Pattern label**: `tight` / `expansive` / `variable`

###### 2. Paragraph Length Distribution
- Count sentences per paragraph
- Identify single-sentence paragraphs (rhetorical emphasis device)
- **Pattern label**: `compact` / `extended` / `mixed`

###### 3. Punctuation Habits
- Em-dash frequency (per 1,000 words): `rare` (< 1) / `occasional` (1-4) / `frequent` (> 4)
- Parenthetical use: yes/no
- Colon use for lists vs. elaboration
- Semicolon use: yes/no
- Ellipsis use: yes/no
- Question marks (rhetorical questions in prose)

###### 4. Contraction Rate
- Count contractions (don't, it's, I've, etc.) per 1,000 words
- `none` (0) / `rare` (1-3) / `moderate` (4-10) / `frequent` (> 10)

###### 5. First-Person Usage
- Count I / me / my / we / our per 1,000 words
- `absent` / `occasional` / `central`
- Note: first-person absence in technical/academic writing is a valid choice, not a deficiency

###### 6. Hedging vs. Certainty Balance
- Hedging markers: might, could, perhaps, possibly, appears to, seems to, I think, arguably, in some cases, it's worth noting
- Certainty markers: clearly, obviously, certainly, definitely, undoubtedly, of course, always, never
- A bare `is`, `are`, `will` or `must` is not a certainty marker. Unmodalized assertion is the default in most prose, so counting it would make every source come back assertive.
- **Balance**: `absent` (no marker of either kind) / `too sparse to judge` (fewer than 3 markers, or fewer than 2 per 1,000 words) / `cautious` (hedging dominant) / `assertive` (certainty dominant) / `calibrated` (mixed with purpose)
- Never record `calibrated` on a source that carries no markers at all. That reading says the author balances hedging against assertion, which a source with nothing to hedge has not done. `scripts/metrics.py` enforces the same two floors and prints `over-hedged` and `over-assertive` where this profile says `cautious` and `assertive`.

###### 7. Formality Level
Score 1-5:
- 1: Very informal (slang, incomplete sentences, direct reader address)
- 2: Informal (contractions, conversational vocab, occasional fragment)
- 3: Neutral (clear, accessible, no slang, minimal jargon)
- 4: Formal (no contractions, complex sentence structures, discipline vocabulary)
- 5: Very formal (passive constructions, nominalizations, impersonal tone)

###### 8. Rhetorical Patterns
- Does the author use **questions** in prose? (genuine or rhetorical)
- Does the author use **direct reader address** ("you", "we")?
- Does the author use **analogies and concrete examples** or stay abstract?
- Does the author use **repetition for emphasis**?
- Does the author make **explicit personal observations** vs. cite external evidence?

###### 9. Vocabulary Level
- Approximate reading grade level using Flesch-Kincaid or Gunning Fog
- Identify domain vocabulary (technical, academic, industry, colloquial)
- Note any distinctive personal vocabulary: recurring words or phrases the author favors

###### 10. Emotional Intensity
- `flat` (purely informational, no emotional register)
- `measured` (calm, occasional expression of view)
- `engaged` (clearly invested, opinion visible)
- `passionate` (strong personal conviction)

---

##### Voice Profile Format

Represent the profile as a structured note:

```
VOICE PROFILE
─────────────────
Source: [n] words from [description of source]

Sentence length:     [mean] words avg, [std] std, [tight/expansive/variable]
Paragraph length:    [n] sentences avg, [compact/extended/mixed]
Em-dash:             [rare/occasional/frequent]
Parentheticals:      [yes/no]
Contractions:        [none/rare/moderate/frequent]
First-person:        [absent/occasional/central]
Hedging balance:     [absent/too sparse to judge/cautious/assertive/calibrated]
Formality:           [1-5]
Reader address:      [yes/no]
Analogy/example:     [high/medium/low]
Emotional intensity: [flat/measured/engaged/passionate]

Key vocabulary patterns:
  - [any recurring words or phrases]
  - [any distinctive syntactic preferences]
```

---

##### Applying the Voice Profile

During Stage 4 (Selective Rewrite), the voice profile operates as a **constraint set**, not a template to copy.

For each rewrite decision, check:
- Does this sentence's length fit the author's distribution?
- Does this punctuation choice match the author's habits?
- Am I using the same hedging/certainty balance as the author?
- Am I matching formality level?
- If the author never uses em-dashes, am I inserting them? (Don't.)
- If the author writes in first person, am I switching to third? (Don't.)

###### Voice Preservation vs. Voice Imitation

**Preservation** (default in `--mode preserve`): Keep all stylistic choices that are distinctive to this author, even if they diverge from generic "best practice". An author who writes long sentences should have long sentences after humanization.

**Imitation** (used in `--voice [sample]` mode): Apply the profile from the sample to a text that the author did not write; shape the rewrite to sound like the author would have written it.

**Critical boundary**: Do NOT invent opinions, positions, or specific experiences to fill out a voice. Imitate structure, rhythm, and vocabulary register, not content.

---

##### Common Voice Destruction Patterns to Avoid

These are errors made by generic humanizers:

1. **Contraction injection**: Forcing "don't" instead of "do not" in writing that naturally uses the formal form
2. **Fragment insertion**: Adding one-sentence paragraphs to "feel more human" when the author's style doesn't use them
3. **Casualizing technical writing**: Replacing precise technical vocabulary with simpler words in text intended for expert readers
4. **First-person imposition**: Adding "I" where the author consistently avoids it
5. **Enthusiasm injection**: Adding exclamation points or enthusiasm markers where the author's register is measured
6. **Hedging removal**: Eliminating calibrated uncertainty to "sound more confident", which changes the author's epistemological position
7. **Generic voice substitution**: Replacing a distinctive author voice with the humanizer's default "natural human" template

---

##### When Voice Cannot Be Determined

If no sample is provided and the text itself doesn't provide enough signal (e.g., very short input), do not guess. Instead:
- Apply neutral rewriting: address structural patterns but do not impose a voice
- Note in the diagnostic: "Voice profile: insufficient signal; voice-neutral rewrite applied"
- The user can provide a sample and reinvoke with `--voice`

## Appendix B. References

Background rather than instruction. `references/methodology.md` holds the honest limits, including the measures in this repository that are known to point the wrong way.

### references/wikipedia-signs.md

#### Observable signs of AI writing

A catalogue of surface features associated with machine-generated prose, adapted for general writing from the Wikipedia community's ongoing documentation of the problem (`Wikipedia:Signs of AI writing`, revision of 29 August 2026). Wikipedia editors review a very large volume of suspected machine text, which makes their list unusually empirical: entries earned their place by recurring across thousands of cases.

##### How to use this file

**No single sign is proof.** Every item below appears in human writing. The catalogue exists to direct attention, not to deliver verdicts.

**Clusters carry the signal.** One canned phrase means little. A page with canned significance framing, a `Future Outlook` section, uniform paragraph shape and a broken citation is a different matter.

**Never state a conclusion about authorship.** This skill cannot establish who or what wrote a text, and neither can any tool it has access to. Report the patterns found and let the author decide what they mean. A diagnostic that says `this was written by ChatGPT` is wrong even when it happens to be correct, because the evidence does not support the claim.

**Markup artifacts are the exception.** A literal `oaicite` token or a `utm_source=chatgpt.com` parameter in a URL is not a stylistic impression. It is a residue of a specific interface, and it is close to conclusive that text passed through that interface. Everything else in this file is probabilistic.

###### What detection tools are worth

Commercial classifiers report high accuracy on their own benchmarks and behave much worse on real text. Both error directions cause damage: false positives on human writing, and false negatives on lightly edited machine text. Non-native English writing draws false positives at elevated rates, which is a known and unresolved fairness problem.

Human judgment is also weaker than people expect, and more variable. Russell, Karpinska and Iyyer (2025) found that annotators who use language models heavily for their own writing reached roughly 90 percent accuracy, well above occasional users, which suggests the skill is acquired exposure rather than intuition. Work reported through the Wikipedia page as Fiedler and Döpke found untrained raters around 57 percent and trained raters around 64 percent, close enough to chance that an individual confident judgment should carry little weight. Full citations in `references/writing-research.md`.

A further complication compounds over time. Models were trained on human text and humans now read enormous quantities of model text, so vocabulary flows in both directions. Words documented as machine tells, `delve` being the standard example, have measurably risen in human speech and writing since 2023. The signals in this file will decay, and some already have.

---

##### Content and framing

###### Inflated significance

Text asserts that a subject matters, in general terms, rather than showing what it did. Common forms include claims about a lasting legacy, a place in a broader movement, an impact on a field, or a role in shaping something. The claim usually cannot be traced to any source in the text.

```
X has left a lasting impact on the field, reflecting broader trends
toward greater inclusivity and shaping the way future practitioners
would approach the discipline.
```

Repair: cut the claim, or replace it with the specific thing that happened.

###### Canned emphasis on notability and coverage

Prose that argues for its subject's importance instead of describing it. Phrases that recur: `has garnered significant attention`, `has been widely recognised`, `received coverage in major outlets`, `is considered a leading figure`. Where a real source exists, name it. Where none does, the sentence is empty.

###### Vague attribution

Authority invoked without a bearer. `Industry observers note`, `critics have argued`, `experts agree`, `it is widely believed`, `some have suggested`. The construction survives most editing passes because it contains no unusual vocabulary.

Repair: name the source, or downgrade the claim honestly to `some research suggests`, or cut it.

###### Overgeneralised opinion

A judgment presented as consensus. `X is regarded as one of the most influential figures in the movement`, where the text supplies no evidence of regard.

###### Superficial analysis via trailing participial phrase

A sentence states a fact, then appends an `-ing` clause that gestures at meaning without adding any:

```
The company opened three offices in 2021, reflecting its commitment
to growth and signalling a broader shift in the industry.
```

The tail is unfalsifiable and usually unsourced. It is also one of the more reliable structural tells, because it combines the participial-clause overuse measured in Reinhart et al. with the significance inflation above. Repair by deleting the tail. If the shift is real, it deserves its own sentence with evidence.

###### Promotional register

Marketing language in text that should be neutral: `state-of-the-art`, `world-class`, `a must-see`, `unparalleled`, `stunning`, `rich cultural heritage`, `nestled in`. Travel and organisational descriptions attract this most.

###### Challenges and outlook framing

Two closely related habits. A `faces challenges` paragraph that lists difficulties in the abstract, and a forward-looking closing section headed `Future Outlook`, `Looking Ahead`, `Challenges and Opportunities` or `Conclusion`, which speculates rather than reports.

These are outline artifacts. A model asked for a structured piece fills every slot in the structure, including slots the material does not support. In non-fiction that is not an essay, a `Future Outlook` heading is a strong signal on its own.

###### Awards, recognition and legacy sections

Sections with these headings that contain no specific award, date or citation, existing because the outline called for them.

###### Leads that mistake a description for a title

Where a piece is titled with a descriptive phrase, model output often opens by treating that phrase as a proper name:

```
The 2019 Regional Transport Review was a review of regional transport
conducted in 2019.
```

The sentence defines the title rather than introducing the subject.

---

##### Language and grammar

###### Copula avoidance

Instead of `is`, `are`, `was` or `has`, model output reaches for a heavier substitute: `serves as`, `stands as`, `functions as`, `represents`, `constitutes`, `embodies`, `boasts`, `features`, `refers to`, `is characterised by`.

```
The library serves as a resource for researchers and boasts a
collection of over 40,000 volumes.
```

Becomes: `The library holds over 40,000 volumes and is open to researchers.`

`Boasts` and `stands as` are the sharpest, since neutral human prose rarely uses either.

###### Vague expression of connection

Two things are linked without the link being specified: `is closely tied to`, `is deeply connected with`, `is intertwined with`, `reflects`, `resonates with`, `speaks to`, `is emblematic of`, `aligns with`.

Repair: state the actual relationship, or drop it. Where the source does not establish a relationship, asserting one is fabrication.

###### Negative parallelism

Three forms, all frequent:

```
It is not just a tool, it is a way of working.
Not a failure, but a redirection.
The design prioritises clarity rather than decoration.
```

The first two are the classic shapes. The third, `X rather than Y` used for emphasis where no genuine contrast exists, has been noted particularly in Grok output.

What makes this pattern worth its own entry: it contains no flagged vocabulary, so word-substitution humanizers leave it completely intact. The negated half is nearly always a position nobody held, inserted to give the affirmed half something to push against.

Repair: state the affirmative claim and delete the setup.

###### Rule of three

Three parallel items where the third exists for cadence rather than content. Also three-part sentence rhythms and three-item section structures. Human writers use tricolons deliberately and sparingly; model output produces them by default.

###### Uniform paragraph shape

Every paragraph opens with a claim, supplies two or three supports, closes with a restatement. The individual paragraph reads fine, which is why this survives review. The uniformity across a whole document is the tell.

---

##### Style and formatting

###### Em dash overuse

Long treated as the single most recognisable typographic signal, and now the most complicated entry in this file.

The pattern to look for is the paired em dash used as parenthetical framing:

> That gap — fluency without judgment — is where the work is.

Two in one sentence, setting off an aside, is the shape worth flagging. A single em dash used as a break is ordinary English punctuation that many strong writers favour.

Two developments matter. Measurement through mid-2026 found that among current models only Claude exceeds professional human writers in em dash frequency, while ChatGPT now uses them at a lower rate than it did, apparently in response to user complaint. GPT-5.1 suppresses them further. So em dash frequency is becoming a weaker signal, and in some comparisons it now points the wrong way.

Treat frequency as suggestive at best. Treat the paired parenthetical construction as the durable part of the signal. Do not treat any em dash as evidence on its own, and be aware that plenty of human writers, including editors and novelists, use them heavily by preference.

###### Curly quotation marks and apostrophes

Typographic quotes (`"` `"` `'`) and apostrophes where a plain keyboard would produce straight ones. Worth noting only with several caveats, because the legitimate sources are numerous: Microsoft Word and Google Docs autocorrect to curly quotes by default, iOS and macOS do the same, many publishing systems substitute them, and material pasted from a professionally typeset source carries them. Curly quotes on their own mean nothing. Curly quotes appearing suddenly in a document that otherwise uses straight ones are worth a look.

###### Heading and emphasis habits

Several related formatting tells:

- Headings in Title Case where the surrounding document uses sentence case
- Headings that restate the document title
- Headings with no content beneath them, or a single sentence
- Bold used for emphasis throughout body text rather than for defined terms
- Vertical lists where each item begins with a bolded inline header followed by a colon
- Skipped heading levels, for example a level 2 followed by a level 4
- Repeated level 1 headings inside a document that already has a title
- Horizontal rules between every section

The bolded-inline-header list deserves attention because it is so common in model output and so rare in human drafting. It appears when a model converts an outline into prose without collapsing the outline.

###### Emoji as structure

Emoji used as section markers or bullet substitutes, particularly a check mark, a rocket, a warning sign or a pointing finger introducing each item in a list. Distinct from ordinary conversational emoji use.

###### Tables that do not need to be tables

Two-column tables holding prose that would read better as sentences, or tables with a single row, or tables whose columns are `Aspect` and `Description`.

---

##### Leaked interface artifacts

The strongest evidence in this file, because these are residues rather than impressions.

###### Text addressed to the user

Output that still contains the model talking to whoever prompted it:

```
Certainly! Here is the revised section you requested.
I hope this helps! Let me know if you would like me to expand any part.
Would you like me to continue with the next section?
As an AI language model, I cannot verify this claim.
```

Also self-referential framing (`In this section, we will explore`), and offers to do more work.

###### Knowledge cutoff and source disclaimers

```
As of my last update, the situation may have changed.
Based on the information available to me, ...
I could not find specific details about this in my sources.
Please verify this information independently.
```

###### Speculation about missing information

Text that reasons aloud about gaps in its own sources rather than reporting facts: `it is unclear from the available information whether`, `details on this period are limited`, `no further information could be located`.

###### Unfilled placeholders

Template scaffolding the author never completed:

```
[Insert date here]        [Add citation]         [Your name]
[Company Name]           [specific detail]       Accessed 2025-xx-xx
```

The `2025-xx-xx` access-date form is a documented recurring case, produced when a model generates a citation template and has no real date to fill in.

###### Markdown surviving into a non-Markdown context

`**bold**`, `##` headings, or `- ` bullets pasted into a system that does not render Markdown, such as wikitext, a rich-text editor or a plain-text field. Also the reverse: broken markup where a model attempted a syntax it had partly memorised.

###### Vendor-specific tokens

Literal strings that identify the interface a text passed through. Search for these directly; they are unambiguous.

| Source | Artifacts |
|---|---|
| ChatGPT | `contentReference`, `oaicite`, `oai_citation`, `turn0search0`, `turn0image0`, `attributableIndex` JSON fragments, `utm_source=chatgpt.com`, `utm_source=openai` |
| Gemini | `[cite: 1]`, `[span_1](start_span)`, similar span and cite wrappers |
| Grok | `grok_card`, `grok_render_citation_card_json`, `referrer=grok.com` |
| DeepSeek | Lenticular bracket citations such as `【85†L261-269】` |
| Perplexity | `[attached_file:1]`, `[web:1]`, `ppl-ai-file-upload` |
| Copilot | `utm_source=copilot.com` |
| Unclassified | `:::writing{variant="document" id=...}` |

A `utm_source` parameter naming a chat product inside a link is worth a note of its own: it means the link was copied out of that product's interface, which is not the same as the surrounding prose being machine-written, but it establishes that the interface was in the loop.

###### Invented structures

References to categories, templates, tags or internal identifiers that do not exist in the target system. A model asked to format for an unfamiliar platform produces plausible names for things that were never created.

---

##### Citation and sourcing failures

Machine-generated citations are frequently well-formed and wrong, which makes them more dangerous than obviously broken ones. Look for:

- Links that resolve to nothing, or to an unrelated page
- DOIs and ISBNs that are syntactically valid and do not exist
- A DOI that resolves to a real article with a different title and different authors from the one cited
- Book citations with no page numbers, or with page numbers outside the book's length
- Author names attached to work they did not produce
- Journal, volume and issue combinations that do not exist
- A stray `↩` character, left over from a footnote back-link in rendered output
- Named references declared and never used
- Real sources cited for claims they do not contain

The last is the hardest to catch and the most common. A citation that exists, is correctly formatted, and does not support the sentence attached to it will pass every automated check.

Any citation in text suspected of machine generation needs checking against the source itself. Format tells you nothing.

---

##### Signals in collaborative and editing contexts

Relevant where text arrives through a review process rather than as a finished document.

**Style discontinuity.** A document whose register, sentence length and vocabulary shift abruptly partway through, particularly where the new section is more fluent and less specific than what surrounds it.

**Commentary that describes rather than argues.** Review comments that summarise a position at length, cover every side evenly, and commit to nothing.

**Formulaic process notes.** Summaries of one's own changes that read as generated: uniformly structured, describing intent in general terms, sometimes at odds with what actually changed.

**Prematurely applied boilerplate.** Maintenance notices, disclaimers or process templates added to a document before the condition they describe exists, because the model knew such templates exist.

**Generic self-description.** Profile and biography text assembled from stock phrases with no verifiable specifics.

**Volume mismatch.** Output arriving faster or in greater quantity than the apparent effort supports.

---

##### Ineffective indicators

Things widely believed to indicate machine authorship that do not. Acting on these produces false accusations, and false accusations against a human writer are the worst failure mode this skill has.

**Perfect spelling, grammar and punctuation.** Careful writers, professional editors and anyone using a spell checker produce clean text. Cleanliness is not a tell.

**Any single flagged word.** `Delve`, `tapestry`, `intricate`, `underscore` and the rest are real words with real uses, and their frequency in human writing has risen since 2023 through ordinary exposure. Frequency and clustering carry information. A single occurrence does not.

**Formal or elevated register.** Some people write formally. Some subjects require it. Non-native English speakers often write in a more formal register than native speakers, and are already over-flagged by every automated detector.

**Long sentences, or short ones.** Neither length indicates anything by itself.

**Bulleted lists and headings.** Structural formatting is normal in documentation, reports and reference material.

**Curly quotes and other typographic punctuation** by themselves, given how many editors and platforms insert them automatically.

**A detector score.** Classifier output is not evidence. It should not appear in a diagnostic, and it should never be cited to a person as a reason to doubt their work.

**Em dashes alone.** Covered above. The signal is weakening, some models now use fewer than professional writers, and many human writers use them heavily by choice.

**An author denying or confirming it.** Neither settles anything, and asking turns a writing review into an interrogation.

**Confident factual errors.** Humans produce these in quantity. Models produce a characteristic kind, plausible and specific and wrong, but the category itself is shared.

---

##### Signs of human writing

The counterweight. These features are difficult for a model to produce because they require access to something outside the text, and their presence should lower suspicion.

**Specific unglamorous detail.** A room number, a bus route, the name of a colleague, the price of a part, the exact wording on a sign. Model output supplies categories where humans supply particulars.

**Verifiable, checkable specifics.** Dates, figures and quotations that hold up when checked, especially where they are obscure enough that inventing them would be pointless.

**Idiosyncratic and asymmetric structure.** Sections of wildly different length. A subject the author clearly cares about, treated at four times the length of an equally important one. Machine output distributes attention evenly.

**Local or tacit knowledge.** Facts that come from having been present, and that no source states directly.

**Genuine and calibrated uncertainty.** `I am not sure this is right`, `as far as I can tell`, `I could not work out why`. Human experts hedge where they are actually uncertain, and models hedge uniformly or not at all.

**Opinion with a position.** A stance taken and defended, rather than a survey of views.

**Unevenness.** A strong opening and a weak middle. A paragraph that is clearly a first draft next to one that has been reworked. Uniform polish across a long document is itself worth noticing.

**Humour, particularly the kind that risks failing.** Jokes that depend on shared context, dry asides, an aside that does not quite land.

**Ordinary error.** A typo, a misremembered detail, an inconsistent spelling of a name.

None of this justifies adding these features to make text look human. Inserting a fake typo or a manufactured uncertainty is a fabrication and this skill does not do it. The list is here for reading, not for writing.

---

##### Source and status

Adapted from `Wikipedia:Signs of AI writing` as of 29 August 2026, with structural findings cross-referenced against `references/style-research.md`.

That page is maintained by editors who assess suspected machine text at high volume, and it changes frequently as model behaviour changes. Anything in this file may be out of date, and the em dash entry is the clearest example of a signal that has already shifted within a year. Check the current revision before relying on any single entry.

### references/style-research.md

#### Style research: measured feature-by-feature differences

Exact figures for the structural differences between instruction-tuned model output and human writing, drawn from Reinhart et al. (2025) and supporting studies. Full citations in `references/writing-research.md`.

##### How to read the numbers in this file

**Human rates are per 1,000 tokens**, measured on dependency-parsed text using Biber's 66-feature tagset via the `pseudobibeR` package. This matters more than it sounds. A rate per 1,000 tokens from a tagged parse is not comparable to a rate per 1,000 words from a regex, and it is not comparable to a percentage of sentences.

**Model figures are percentages of the human rate.** `527%` means the model produced the feature at 5.27 times the rate human writers did on the same prompts. `51%` means about half. 100% would be parity.

**The comparison is within-corpus and prompt-matched.** Both corpora use a two-chunk design: a human writer's text is split at roughly 500 words, the model receives chunk 1 as context and generates a continuation, and the model's continuation is compared against the human chunk 2. Same author, same topic, same point in the text. That design is what makes the percentages meaningful, and it is why figures from other studies are not directly comparable.

**Corpora.** HAP-E (Human AI Parallel English) contributed 8,290 valid texts across fiction, news, blogs and academic prose. COCA AI Parallel (CAP) contributed 9,615. Models tested: GPT-4o, GPT-4o Mini, Llama 3 8B and 70B in both base and instruction-tuned form.

**The scripts in this repository do not reproduce these numbers.** `scripts/analyze_structure.py` uses regular expressions, counts sentences rather than tokens, and reports nominalization figures roughly five and a half times higher, measured below. Its output is comparable only against another run of itself. Never quote a script figure as though it came from the paper, and never compare the two. See `scripts/_shared.py`.

---

##### The headline finding

Instruction tuning, not model scale, produces the fingerprint.

Base Llama 3 models sit at 94% to 102% of human rates on the features listed below. Their instruction-tuned counterparts diverge sharply on the same features, from the same prompts, at the same parameter count. Llama 3 70B and 8B show similar divergence to each other, so scaling up does not reduce it.

This is the single most consequential result in the literature for a skill like this one. It means the fingerprint is a product of the alignment process rather than of language modelling itself, and it means the pattern is a learned preference rather than a limitation. Preferences can be written around.

---

##### Overrepresented features

###### Present participial clauses

The strongest single structural signal in the study.

| | Rate |
|---|---|
| Human writers | 1.7 per 1,000 tokens |
| GPT-4o | 527% |
| GPT-4o Mini | 481% |
| Llama 3 70B Instruct | 261% |
| Llama 3 8B Instruct | 224% |

The construction is a clause headed by an `-ing` participle, most visibly at the start of a sentence but also appended at the end:

```
Leveraging existing infrastructure, the team shipped in six weeks.
The team shipped in six weeks, leveraging existing infrastructure.
Bryan, leaning on his agility, dances around the ring, evading Show's heavy blows.
```

The third example is real GPT-4o output from the study, and it carries two participles in one sentence about professional wrestling.

Why this feature and not another: the participial clause lets a writer attach a second action to a sentence without committing to how the two relate. It is grammatically economical and semantically vague, which is exactly the trade a model makes when it has fluency but no specific knowledge of the causal link. Repairing it forces a decision. See `rules/structure.md`.

###### That-clauses as subject

| | Rate |
|---|---|
| Human writers | 2.1 per 1,000 tokens |
| GPT-4o | 331% |
| GPT-4o Mini | 263% |

```
That the policy failed was evident to everyone involved.
```

A formal construction that fronts a proposition. Human writers use it sparingly, usually for emphasis.

###### Past participial clauses

Instruction-tuned models: 273% to 307% of the human rate.

```
Founded in 1923, the company relocated twice.
Written under a pseudonym, the report circulated widely.
```

Same mechanism as the present participial clause, and the same repair.

###### Nominalizations

| | Rate |
|---|---|
| Human writers | 14.6 per 1,000 tokens |
| Instruction-tuned models | roughly 209% to 214% |

Nouns derived from verbs and adjectives, typically through the suffixes `-tion`, `-ment`, `-ness`, `-ity`, `-ance` and `-ence`.

Real Llama 3 70B Instruct output from the study: `These schemes can help to reduce deforestation, habitat destruction, and pollution, while also promoting sustainable consumption patterns.` Four nominalizations in one sentence.

Nominalization hides the actor. `The implementation of the solution` does not say who implemented it. That is convenient for a model that does not know, and it is the reason the feature travels with the participial clause.

The 14.6 figure is the one most often misquoted. It is per 1,000 **tokens**, from a **tagged parse** that identifies genuine nominalizations. A suffix regex over raw words, which is what this repository's scripts run, reports several times that on the same kind of text, because it catches every word ending in those letters regardless of derivation. On the five model-generated inputs in `examples/` the proxy returns 56.3, 70.7, 84.5, 92.9 and 95.4 per 1,000 words, averaging 80.0, or about 5.5 times the tagged figure. Reproduce with:

```
for f in examples/*/input.md; do
  printf '%-42s ' "$f"
  python3 scripts/analyze_structure.py "$f" | grep 'Nominalization density'
done
```

The `printf` is there because `analyze_structure.py` does not print the filename, so the bare loop gives six unlabelled figures in glob order. The sixth figure, and the lowest, is 45.5 on `examples/already-natural/input.md`. It is left out of the average because that input is human-written.

###### Attributive adjectives, demonstratives and downtoners

Instruction-tuned models: 118% to 155% of the human rate across these three feature families.

Attributive adjectives sit before the noun (`a comprehensive review`) rather than after a copula (`the review was comprehensive`). Stacking them is how model prose acquires its characteristic density. Downtoners are hedging adverbs like `somewhat`, `slightly` and `relatively`.

###### Mean word length

Instruction-tuned models: 114% to 116% of the human figure.

A small multiplier on a feature with very low variance, which makes it a surprisingly stable signal. It reflects consistent preference for the longer Latinate option: `utilize` over `use`, `facilitate` over `help`, `demonstrate` over `show`.

###### Clausal coordination, for Llama only

Llama 3 Instruct models: 116% to 141%. GPT models run the other way, at 59% to 63%.

This is a useful reminder that the fingerprint is model-specific in its details even where the overall direction is shared. A rule written to reduce coordination would be correcting Llama output and damaging GPT output.

---

##### Underrepresented features

The gap runs in both directions, and the underuse side is the half most humanizer tools ignore entirely.

###### Agentless passives

GPT-4o and GPT-4o Mini: 51% to 53% of the human rate. Roughly half.

This contradicts the most widely repeated belief about AI writing. Models do not overuse the passive voice; the GPT family underuses it, almost certainly because "prefer the active voice" is among the most common pieces of writing advice in the training data and in the preferences of human raters.

The practical consequence is direct: **converting passive to active as a blanket rule moves text further from the human distribution, not closer.** That conversion is a staple of commercial humanizers and it is counterproductive. Llama base models sit near the human rate.

###### Hedges

Instruction-tuned models: 50% to 63% of the human rate.

Human experts write `probably`, `I think`, `as far as I can tell`, `it looks like`, and they write them where they are actually uncertain. Models hedge less overall, and when they do hedge they place it formulaically (`It is worth noting that`) in front of claims they are not uncertain about at all. The deficit is in calibration as much as in quantity.

Adding a hedge that reflects real uncertainty in the source is a legitimate repair. Inventing uncertainty the author does not have is fabrication, and this skill does not do it.

###### Existential `there`

Instruction-tuned models: 59% to 71%.

```
There were three objections to the proposal.
```

Another construction that writing advice discourages, and another case where following the advice absolutely produces a measurable divergence from how people actually write.

###### Adverbs

Instruction-tuned models: 82% to 86%.

Also consistent with prescriptive advice about adverbs being weak, absorbed through alignment and then applied with a uniformity no human writer sustains.

###### A note on what these four have in common

Agentless passives, existential `there`, adverbs, and to a degree hedges are all things style guides tell writers to avoid. Instruction-tuned models avoid them more consistently than the humans whose writing the guides describe. The fingerprint is partly the signature of advice followed too well.

This is the most useful single insight in the whole literature for anyone editing suspected machine text, because it inverts the intuitive move. The instinct is to apply writing advice harder. The measurement says the text already has writing advice applied harder than any human would.

---

##### Vocabulary divergence

###### Extreme overrepresentation

These appeared in GPT-4o and GPT-4o Mini output at roughly 84 to 171 times the human rate on matched prompts:

```
camaraderie   tapestry     palpable     intricate    underscore
unspoken      amidst       solace       fleeting     vibrant
cacophony     grapple      ignite       unravel
```

Two things about this list are worth holding onto. The multipliers are far larger than anything on the structural side, which is why vocabulary is the signal people notice. And it is nonetheless the weaker signal, because it is trivially removable: swap fourteen words and the morphosyntactic profile is completely unchanged. See `rules/vocabulary.md` for why the swap usually makes the writing worse.

The genre-independence is the sharper finding. GPT-4o reaches for `camaraderie was palpable` when writing about sports, about workplaces, about war. Human writers reach for it almost never.

###### Extreme underrepresentation

Over 100 times rarer in instruction-tuned output than in human writing:

- Profanity and blunt language, an unambiguous RLHF artifact
- `i.e.` and `e.g.`

Contractions are also depressed in registers where human writers contract freely.

The `i.e.` result is the most interesting of the three, because there is no plausible safety or preference reason for it. It suggests the models have absorbed a general register preference for spelled-out formal prose that goes beyond anything a rater explicitly asked for.

---

##### Classification results

How separable the two populations actually are, which bounds what any detector can claim.

| Task | Method | Accuracy |
|---|---|---|
| 7-way source identification | Random forest on Biber features | 66% (chance is 14%) |
| Pairwise human vs one model | Random forest | 93% to 98% |
| Pairwise, instruction-tuned models | Lasso | 91% to 96% |
| Pairwise, base models | Lasso | around 75% |
| Out-of-sample, M4 arXiv corpus | Trained classifier | 50% to 70% |

Error breakdown on the 7-way task: 4.2% of model texts were classified as human, and 9.8% of human texts were classified as model output.

Three conclusions follow, and all three constrain this skill.

**The separation is real.** 93% to 98% pairwise accuracy on morphosyntactic features alone, with no access to vocabulary, is a large effect. The structural fingerprint exists.

**Base models are much harder.** The drop from 91-96% to around 75% for base Llama is the instruction-tuning finding restated as a classification problem.

**Generalisation fails badly.** A classifier trained on these corpora and applied to a different corpus of arXiv abstracts fell to 50% to 70%, which at the low end is chance. Detection that works within a domain does not transfer out of it. Any product claiming a single reliable accuracy number across all text is describing something the research does not support.

And the false positive rate is the number that matters ethically. Nearly one human text in ten was flagged as machine-written by a carefully constructed research classifier on in-domain data. Commercial detectors operating out of domain do worse. This is why nothing in this skill outputs a verdict on authorship.

---

##### Genre and register

The Biber framework's first and strongest dimension runs from involved to informational. Conversation sits at the involved end; academic prose sits at the informational end.

Human writers move along this dimension with genre. A text message, a blog post and a journal article occupy visibly different positions.

Instruction-tuned models shift toward the informational end **and stay there regardless of genre**. Fiction generated by GPT-4o has information density close to its academic prose. This is the most likely explanation for why machine fiction reads flat: it is written in the register of a description of a story rather than the register of a story.

The practical rule: check register fit before flagging any individual feature. Nominalization in an academic abstract may be correct. The same density in dialogue is not. See `rules/context.md`.

---

##### Limits of everything above

**These are 2024 and 2025 model versions.** GPT-4o and Llama 3. Vendors have since adjusted, sometimes in direct response to public commentary about these exact tells. The em dash is the documented case: measurement through mid-2026 found ChatGPT using them less than it did, and GPT-5.1 suppressing them further. Any specific multiplier in this file should be read as a finding about a model generation, not a permanent property.

**Fine-tuning removes the fingerprint.** Dawkins et al. (2025) fine-tuned on a genre-specific corpus of tweets and substantially reduced the structural differences for that genre. A model tuned on target-genre human writing is much harder to distinguish, which caps how durable any of this can be.

**Vocabulary flows back.** Words documented here as machine markers have measurably risen in human usage since 2023. `Delve` is the standard example. The list decays through the ordinary mechanism of people reading a lot of model output.

**Human writing is a distribution, not a point.** Every percentage above compares against an aggregate. Individual human writers scatter widely, and some sit naturally where the models sit. A writer whose prose is dense, formal and participial is not writing badly and is not writing with a model. Aiming output at the human mean would produce a new cluster, which is the failure mode of every tool that treats humanness as a target rather than a range.

### references/writing-research.md

#### Academic Writing Research Reference

Compiled research on structural, rhetorical, and stylistic differences between human and LLM-generated text. This is Not Ai's primary evidence base.

**Last updated**: August 2026

---

##### Primary Studies

###### Reinhart et al. (2025): PNAS
**Citation**: Reinhart, A., Brown, D. W., Markey, B., Laudenbach, M., Pantusen, K., Yurko, R., & Weinberg, G. (2025). Do LLMs write like humans? Variation in grammatical and rhetorical styles. *Proceedings of the National Academy of Sciences*, 122(8), e2422455122. doi:10.1073/pnas.2422455122

**Preprint**: https://arxiv.org/abs/2410.16107

**Method**: Two prompt-matched parallel corpora, HAP-E (8,290 valid texts) and COCA AI Parallel (9,615). Each human text is split at roughly 500 words; the model receives chunk 1 and generates a continuation, which is compared against the human chunk 2. Same author, same topic, same position in the text. Models: GPT-4o, GPT-4o Mini, Llama 3 8B and 70B, each in base and instruction-tuned form. Analysis used Biber's 66-feature morphosyntactic tagset via the `pseudobibeR` package on dependency-parsed text.

**Key findings**:
1. Present participial clauses: human rate 1.7 per 1,000 tokens, GPT-4o at 527%, GPT-4o Mini 481%, Llama 3 70B Instruct 261%, Llama 3 8B Instruct 224%
2. Nominalizations: human rate 14.6 per 1,000 tokens, instruction-tuned models around 209% to 214%
3. `That`-clauses as subject: human 2.1 per 1,000 tokens, GPT-4o 331%
4. Instruction-tuned models **underuse** agentless passives (GPT at 51% to 53%), hedges (50% to 63%), existential `there` (59% to 71%) and adverbs (82% to 86%)
5. Fourteen words including `camaraderie`, `tapestry`, `palpable` and `intricate` appear at 84 to 171 times the human rate in GPT-4o output
6. Profanity and `i.e.` appear over 100 times less often than in human writing
7. **Instruction tuning is the root cause**: base Llama 3 models sit at 94% to 102% of human rates on these features; the instruction-tuned variants diverge sharply
8. Model size does not reduce the fingerprint: 70B and 8B diverge similarly
9. Classification: 66% on 7-way source identification against a 14% baseline, 93% to 98% pairwise human against one model, but only 50% to 70% out of sample on the M4 arXiv corpus
10. Error rates on the 7-way task: 4.2% of model texts read as human, 9.8% of human texts read as model output
11. All models cluster in a narrower stylistic region than human writers occupy

Feature-by-feature figures with the full tables are in `references/style-research.md`.

**Relevance to Not Ai**: This study provides the evidence base for Not Ai's structural intervention approach. The key insight: the primary fingerprint is morphosyntactic (clause types, information density), not lexical (word choice). Existing humanizers work at the lexical level; Not Ai works at the structural level.

**Data available**: https://huggingface.co/datasets/browndw/human-ai-parallel-corpus

---

###### Jiang & Hyland (2025): Multiple papers
**Citations**:
- Jiang, F., & Hyland, K. (2025). Rhetorical distinctions: Comparing metadiscourse in essays by ChatGPT and students. *English for Specific Purposes*, 79, 17-29.
- Jiang, F., & Hyland, K. (2025). Does ChatGPT write like a student? Engagement markers in argumentative essays. *Written Communication*.
- Jiang, F., & Hyland, K. (2025). Does ChatGPT argue like students? Bundles in argumentative essays. *Applied Linguistics*, 46(3), 375-391.

**Key findings**:
1. ChatGPT essays show "significantly lower frequency of interactional metadiscourse, such as hedges, boosters, and attitude markers" → more impersonal, expository tone
2. Student essays show higher "rhetorical engagement" including questions and personal asides
3. "ChatGPT-generated essays exhibited fewer engagement markers, particularly questions and personal asides"
4. LLM "bundles are more rigid and formulaic": they are noun and preposition-based rather than epistemic stance markers
5. Student essays have "more epistemic stances and authorial presence"

**Relevance to Not Ai**: Validates the rhetorical dimension in `rules/rhetoric.md`. The engagement marker deficit is real and measurable. Not Ai addresses: hedging calibration, engagement marker addition (where genre permits), and epistemic stance restoration.

---

###### StoryScope (2026)
**Citation**: Russell, J., Rajendhran, R., Iyyer, M., & Wieting, J. (2026). StoryScope: Investigating idiosyncrasies in AI fiction. arXiv. https://arxiv.org/abs/2604.03136

**Key findings**:
1. AI stories cluster in a **shared region of narrative space** while human-authored stories exhibit **greater diversity**
2. AI-specific narrative fingerprints:
   - **Claude**: notably flat event escalation
   - **GPT**: over-indexes on dream sequences
   - **Gemini**: defaults to external character description
3. AI stories over-explain themes; human stories have more moral ambiguity
4. Human stories have increased temporal complexity; AI stories favor "tidy, single-track plots"
5. Narrative construction differences, not just writing style, distinguish human from AI fiction

**Relevance to Not Ai**: The "shared narrative space" finding is the narrative equivalent of the "humanizer paradox": all LLMs cluster. This means humanizers that aim for a single "human-like" narrative target create a new cluster. Not Ai's design principle of targeting a **distribution** rather than a point is supported by this research. Also informs `rules/rhetoric.md` narrative section.

---

###### Milička et al. (2025)
**Citation**: Milička, J., Marklová, A., & Cvrček, V. (2025). Benchmark of stylistic variation in LLM-generated texts. arXiv. https://arxiv.org/abs/2509.10179

**Key findings**:
1. Compared lots of different LLMs (GPT versions, Gemini, Claude) to humans using Biber's six factor dimensions
2. LLMs shift toward Dimension 1 (Involved → Informational): more information-dense text
3. Shift varies by model: models have distinct stylistic fingerprints
4. Czech corpus analysis: LLMs much worse at matching native Czech style

**Relevance to Not Ai**: Confirms model-specific fingerprints. Supports the architecture that handles different source models differently. Also confirms cross-language limitations, which Not Ai should acknowledge.

---

###### Goulart et al. (2024)
**Citation**: Goulart, L., et al. (2024). AI or student writing? Analyzing the situational and linguistic characteristics of undergraduate student writing and AI-generated assignments. *Journal of Second Language Writing*, 66, 101160.

**Key findings**:
1. "AI-generated texts are more informationally dense, explicit, and less involved than student-authored texts"
2. "EFL Students tend to integrate more personal references and features of involvement, making their writing more nuanced and contextually rich"
3. Uses Biber's MDA (Multi-Dimensional Analysis): confirms Biber features are diagnostically effective

**Relevance to Not Ai**: Confirms the information density finding in student/essay contexts. "Personal references and involvement" is exactly what Not Ai's engagement and voice dimensions address.

---

###### Siler (2026): Academic slop in published papers
**Citation**: Siler, K. (2026). The diffusion of large language models in published academic articles. *PNAS*, 123(22), e2605754123.

**Key findings**:
1. Corpus of 7.3 million full-text articles (Elsevier, Frontiers, MDPI, PLoS) from 2020-2025
2. "LLM-likely words" spiking after 2023: "underscore", "delve", "meticulous", "foster", "comprehensive"
3. Higher rates in lower-ranked institutions and non-English-first-language countries
4. Higher in MDPI and Frontiers than Elsevier and PLoS

**Relevance to Not Ai**: Real-world evidence that AI vocabulary signals are measurable at scale in published academic papers. Validates the vocabulary signal list in `scripts/analyze_structure.py`.

---

###### Dawkins et al. (2025): Fine-tuning reduces differences
**Citation**: Dawkins, H., Fraser, K. C., & Kiritchenko, S. (2025). When detection fails: The power of fine-tuned models to generate human-like social media text. arXiv. https://arxiv.org/abs/2506.09975

**Key findings**:
1. Biber features show systematic differences in LLM-written tweets vs. human tweets
2. **Fine-tuning on genre-specific corpus dramatically reduces these differences**
3. Suggests instruction-tuned LLMs can be adapted to a genre

**Relevance to Not Ai**: This is an important limitation, because the structural signals identified by Reinhart et al. may weaken as models are specifically fine-tuned on genre-appropriate data. Not Ai must be updated as the research develops.

---

###### Toney et al. (2026): Review of "humanness" studies
**Citation**: Toney, A., Bode, L., Ventura, T., Wilcox, E., & Singh, L. (2026). Comparing the humanness of machine-generated and human-authored text. *ACM Computing Surveys*. doi:10.1145/3806206

**Key findings**:
1. Review of 17 papers analyzing "humanness" up to 2024
2. Most studies did not explore prompt variation
3. Not enough studies compared multiple LLMs
4. "Humanness" may depend on the observer, change over time, and vary across linguistic groups

**Relevance to Not Ai**: Validates the "human writing as a distribution" design principle. Humanness is not a fixed target.

---

###### Detection accuracy, human and automated

**Citation**: Russell, J., Karpinska, M., & Iyyer, M. (2025). People who frequently use ChatGPT for writing tasks are accurate and robust detectors of AI-generated text. arXiv:2501.15654

**Key findings**:
1. Annotators who use language models heavily for writing reached roughly 90% accuracy at identifying machine-generated text
2. Their accuracy held up against paraphrasing and humanizing attacks better than automated detectors did
3. Occasional users performed far worse, which indicates the skill is acquired through exposure rather than being a general intuition

A second line of work, cited through `Wikipedia:Signs of AI writing` and reported there as Fiedler and Döpke, found untrained raters at around 57% and trained raters at around 64%. The gap between that and the 90% figure is best explained by how much model output the rater reads day to day.

**Relevance to Not Ai**: two things. First, close reading by an experienced reader outperforms every automated detector tested, which is the argument for a skill that reports specific patterns to a human rather than producing a score. Second, the low end of these figures is close to chance, which means an individual confident judgment about a specific piece of writing is usually not warranted. Note that the exact bibliographic details of the second study were taken from a secondary source and have not been verified against the original.

---


**Citation**: Ming, X., Hernandez, J., & Juzek, T. S. (2026). Identifying LLM lexical bias: A curation-free triangulated metric for preference-state learning. *FLAIRS-39*.

**Key findings**:
1. Instruction tuning introduces a shift toward Romance-origin vocabulary
2. Romance words entered English "via the ruling class and acquired high socio-economic status"
3. RLHF may reward formal/prestigious vocabulary

**Relevance to Not Ai**: Explains *why* LLMs reach for "utilize" over "use", "facilitate" over "help", "leverage" over "use". The preference is a learned prestige signal, not a semantic choice. The intervention is to restore the more direct Anglo-Saxon form when it serves communication better.

---

###### LLM Review (2026): Blind peer review for creative writing
**Citation**: LLM Review: Enhancing Creative Writing via Blind Peer Review Feedback. arXiv:2601.08003

**Key finding**: Multi-agent frameworks that interact during generation can cause "content homogenization", which reduces creative diversity. Blind review (agents exchange feedback without seeing each other's drafts) preserves divergent trajectories.

**Relevance to Not Ai**: The homogenization problem is the AI-writing problem in miniature. This supports Not Ai's principle: target a diverse distribution of human styles, not a single "human-like" style.

---

###### SurrogatePrompt (2023): Representation mismatch
**Citation**: SurrogatePrompt: Bypassing the Safety Filter of Text-To-Image Models via Substitution. arXiv:2309.14122

**Key architectural insight (adapted)**:
The paper shows that safety filters and image generators operate in different "representation spaces". A prompt can evade the filter by using surface-level substitutions that the filter doesn't associate with the problematic concept, while the image generator still produces the intended output.

**Relevance to Not Ai (carefully adapted)**:
This is analogous to the humanizer problem. Humanizers that operate at the word level, the "safety filter level", change surface features that detectors react to. The underlying morphosyntactic representation, the "image generator level", remains unchanged, and that representation is what makes the text actually feel like LLM output.

**Not Ai's response**: Operate at the structural level, not the surface level. Change clause types, information density, and rhetorical patterns rather than swapping surface vocabulary. Those features are the actual representation that constitutes "LLM writing style".

**IMPORTANT CAVEAT**: The SurrogatePrompt paper is about adversarial attacks on safety systems. Not Ai does NOT draw on it for adversarial purposes. The architectural lesson, that surface and structural representations are different spaces, applies generally to the problem of meaningful transformation vs. surface disguise.

---

##### Commercial Humanizer Analysis

###### Research Methodology
- Studied marketing claims vs. actual output behaviors
- Investigated user reports, reviews, and independent tests
- Did not rely on marketing copy

###### Summary of Findings

| Tool | Approach | Primary Weakness |
|------|----------|------------------|
| Undetectable AI | Word substitution + paraphrasing | Creates "humanizer voice"; doesn't address structure |
| WriteHuman | Synonym replacement + punctuation variation | Loses meaning; no genre awareness |
| QuillBot | Paraphrase modes | Meaning drift; voice destruction |
| Phrasly | Synonym swap + sentence restructuring | Over-casualization; structural patterns remain |
| StealthGPT | Substitution-focused | Surface-level only |
| HIX Bypass | Multi-pass paraphrase | Produces recognizable "bypass voice" |

**Common pattern across all commercial tools**:
1. Word-level intervention (synonyms, banned word removal)
2. No structural analysis
3. No voice preservation
4. No genre awareness
5. No meaning preservation checking
6. Outputs converge toward a "humanizer voice" (short-medium-long sentence cycling, forced contractions, injected fragments)

---

##### Open-Source Humanizer Analysis

###### Aboudjem/humanizer-skill
- 55 patterns (Wikipedia AI tells extended)
- 5 fixed voice modes
- 0-100 AI-tell score
- Pure Markdown, zero dependencies
- Weakness: all 5 voices are fixed templates, not user voice extraction; patterns are still primarily lexical

###### blader/humanizer
- Focus on removing Wikipedia AI tells
- Voice matching via sample
- Good documentation
- Weakness: primarily lexical intervention; no structural diagnosis

###### numen-tech/slopornot / agentic-humanizer
- Multi-pass workflow
- Multi-language support
- Weakness: convergence toward "humanizer output" pattern

###### Common pattern across open-source tools
All implement some variant of: scan → flag → replace/rewrite → output. None implement:
- Biber-feature structural diagnosis
- Information density measurement
- Clause-type distribution analysis
- Genre-conditioned transformation
- Self-review against the changes actually made
- Meaning preservation verification

---

##### Limitations of Current Research

1. **Temporal decay**: LLM fingerprints change as models are updated. Research from 2024 may not apply to 2026 models.
2. **Fine-tuning escape**: Dawkins et al. show genre-specific fine-tuning can dramatically reduce structural fingerprints.
3. **Humanness is subjective**: Toney et al. note that "humanness" depends on the observer and may change over time.
4. **Cross-language gap**: Non-English research is limited. LLM behavior in other languages may differ significantly.
5. **Prompt sensitivity**: Style varies significantly with prompt; a highly constrained prompt may produce more human-like output.

---

##### Gaps in this evidence base that affect the skill directly

Named here rather than under a forward-looking heading, because `references/wikipedia-signs.md` flags speculative outlook sections as a machine-writing tell and this file should not contain one. These are specific things the skill currently does without research support.

**Genre coverage is thin outside academic and argumentative prose.** Most measurement uses student essays, journal articles and news. `rules/context.md` gives guidance for fiction, email, technical documentation and social posts that rests on much weaker evidence than the academic guidance does. The fiction guidance leans almost entirely on one study.

**There is no human diversity baseline.** Every percentage in `references/style-research.md` compares model output against an aggregate human rate. Nothing in the literature characterises the spread. Without it, the skill cannot answer the question that matters most in practice: is this particular writer unusual, or is this text machine-generated? It reports patterns instead, which is the correct response to not knowing.

**Nobody has measured what humanizing does to the structural fingerprint.** Commercial tools are evaluated against detector scores, which is circular. No published work measures Biber features before and after a humanizing pass. So the central claim behind this skill, that structural intervention outperforms lexical substitution, is argued from mechanism rather than demonstrated by measurement. `benchmarks/` exists to hold such a measurement and is currently empty.

**Voice preservation has no validated metric.** The skill claims to preserve an author's voice while changing structure. There is no accepted way to measure whether it did. `scripts/benchmark.py` reports token overlap as a proxy for meaning preservation, which is weaker still, and says so.

**Cross-language evidence is close to absent.** One Czech corpus study. The skill should be assumed unreliable outside English.

### references/methodology.md

#### Not Ai: design methodology

Why the skill is built this way, what has already been tried by others, and what it cannot do. Read this before proposing a rule.

##### The problem

Text produced by an instruction-tuned language model carries a measurable stylistic signature. The signature is not a set of words. It is a distribution over clause types, information density, cadence and stance, and Reinhart et al. measured it directly across parallel human and model corpora using Biber's 66-feature tagset. Full figures are in `references/style-research.md`.

The practical consequence is prose that reads as produced rather than composed: generic where it should be specific, confident without evidence, smooth without a person in it, organised without an argument. None of this is a moral failing of the text. It is a communication failure. The writing is less effective at reaching a particular reader for a particular purpose.

The goal of this skill is not to conceal that a model was involved. It is to remove the generic habits and restore what authorship supplies: specificity, judgment, register, and the author's own voice.

##### What has been tried, and where each approach stops

**Word blacklisting.** Find the flagged terms, `delve`, `leverage`, `furthermore`, `comprehensive`, and substitute.

The word is not the problem. `Delve` is not incorrect. `Leverage` is the right word in a finance context. What the research measures is a co-occurrence: elevated participial clause rate together with elevated nominalization, uniform cadence, and absent epistemic hedging. Remove the words and the morphosyntactic profile is unchanged, because none of the six features that separate the distributions is lexical. Removing someone's cologne does not change their gait.

`examples/personal-essay/` shows the failure quantitatively. The vocabulary scanner finds two flagged terms in a 213-word generated essay, fewer than in any other input here except the human paragraph. It misses `embarked`, `journey`, `acculturation` and `unparalleled` because the list is tuned to a different register. The tells in that draft were a nominalization rate of 84.5 and a grade level of 15.0 on a first-person essay about renting a flat.

**Paraphrase rewriting.** Send the text back through a model with an instruction to reword it. This is what most commercial humanizers do.

Four problems. Claims, qualifications and specifics drift under paraphrase, so the text no longer says what it said. The output sounds like a person and no longer sounds like the author. Every paraphrase tool trained on similar feedback converges on the same corrective register, which is itself now a recognisable pattern. And the underlying clause distributions do not improve, because the paraphrasing model's own defaults are the distribution the problem came from.

**Surface variation injection.** Add fragments. Break long sentences. Insert contractions and slang. Vary punctuation.

Human writing is not defined by imperfection, and deliberately introduced roughness produces a caricature rather than a person. `examples/already-natural/` reproduces one of these outputs against a human original: the specifics survive, buried under performed enthusiasm the original writer plainly does not feel. This approach also makes the writing worse, which is never the goal.

**Fixed voice templates.** Offer three to five presets, `casual`, `professional`, `academic`, and apply the selected one.

`Casual` and `professional` are register targets, not voices. Two professional writers in the same field have entirely different professional voices, and a preset captures neither. The result replaces one generic pattern with another.

##### Eight design principles

**1. Operate structurally, not lexically.** The signals the skill measures and acts on are clause type, nominalization density, information density, engagement markers, epistemic stance, paragraph shape and length distribution. Vocabulary is handled last, on the argument that a word swap inside a badly built sentence changes nothing a reader notices.

Exact figures, from Reinhart et al. and measured with a dependency parse:

| Feature | Human rate per 1,000 tokens | Instruction-tuned models |
|---|---|---|
| Present participial clauses | 1.7 | 224% to 527% of human |
| `that` clause as subject | 2.1 | 263% to 331% |
| Past participial clauses | see note | 273% to 307% |
| Nominalizations | 14.6 | 209% to 214% |
| Agentless passives | see note | 51% to 53% for the GPT models |
| Hedges | see note | 50% to 63% |
| Existential `there` | see note | 59% to 71% |

Four human rates are left out rather than filled with a plausible number. `references/style-research.md` carries the relative figure for past participial clauses, agentless passives, hedges and existential `there` because that is what was taken from the source; the absolute rates were not, and inventing them here would breach principle 7 in a file arguing for it.

Note the direction of the last three. Instruction-tuned models do not simply add features; they also avoid features that style guides discourage, more consistently than humans do. This is why blanket passive-to-active conversion moves text away from the human distribution rather than toward it.

**2. Deterministic measurement precedes reasoning.** The scripts run before any rewriting, so the diagnostic is a set of counts rather than an impression, the reasoning does not have to guess at frequencies, and any figure in the output can be reproduced by rerunning one command.

**3. Voice is a constraint, not a finishing pass.** When a sample is supplied, the profile bounds every rewrite decision: sentence length distribution, formality, punctuation habits. Where the sample uses no semicolons, the rewrite introduces none. Without a sample the skill rewrites neutrally and records `Voice profile: insufficient signal` rather than imposing a voice it cannot justify.

**4. Genre conditions everything.** The same measurement means opposite things in different genres, and this is not a hedge. `examples/academic-abstract/` and `examples/technical-passage/` both arrive at Stage 2 with nominalization flagged high. In the technical passage the correct response took it from 95.4 to 17.3. In the abstract the correct response was to take it from 92.9 to 83.3 and leave it flagged, because academic abstracts nominalize by convention and lowering the figure further would mean writing a worse abstract.

`examples/linkedin-post/` completes the picture from the other side. Its Gunning Fog index is 21.2 and that is a finding, because the audience is a scrolling feed. The abstract in this set reads 24.6 and the fog index is not what is wrong with it, because the audience is a reviewer. Neither number can be read without the genre.

**5. Human writing is a distribution, not a target.** Human prose varies enormously across individuals, genres, registers and languages. The goal is output that could plausibly exist somewhere in that space, not convergence on a single humanized style. Convergence is what produces the recognisable humanizer accent.

**6. Selective edits over wholesale rewriting.** The permitted actions are `KEEP`, `RESTRUCTURE`, `REPLACE`, `REMOVE`, `MERGE`, `SPLIT`, `MOVE` and `FLAG`. Rewriting everything is not among them, and `KEEP` should be the most frequent action in most texts. Over-editing is a failure mode of the same order as under-editing: it discards the author's phrasing that was already working.

**7. Never invent.** Where a specific detail would strengthen a sentence and is absent from the source, the skill writes `[specific detail here]` and leaves it. It does not supply facts, numbers, sources, anecdotes, emotions or dialogue.

This principle is load-bearing and it is under constant pressure. `examples/gen-ai-article/` records what an earlier version of this repository shipped as a correct output: a well-paced, specific, readable paragraph in which every specific was invented, generated from an input containing no facts at all. It reads better than the source and it attributes claims to an author who never made them. That is a worse outcome than a vague paragraph, because vagueness is visible and confident fabrication is not.

`examples/personal-essay/` documents the same pressure in a milder form, two inferred passages declared as additions in a 255-word rewrite, and states plainly that a draft this empty pushes any rewrite toward invention.

**8. Self-review before output.** Eight questions, listed in full in `SKILL.md`, covering what still reads as generic, where the rewrite over-edited, whether anything was invented, whether the author's position moved, whether the polish is suspiciously even, whether the voice survived, whether the genre rules were the right ones, and whether the change list matches the changes actually made.

The eighth question exists because of a specific failure in this repository's own history: a rationale that claimed to have removed three em dashes while the output it shipped still contained two.

##### What this skill does not claim

It does not claim that a text is human, that it will pass a detector, that it cannot be detected, or any bypass rate. Those claims are indefensible. Detection systems change, models change, and no measurement here establishes authorship.

It also does not produce a score. An earlier version of `scripts/metrics.py` exposed a `compute_quality_score()` function; it was removed rather than improved. A single number invites an agent to optimise it, and `examples/already-natural/` shows exactly what optimising it costs: to raise burstiness on a human paragraph an agent must invent a fact, and to lower nominalization it must delete the term `race condition`, which is the phrase another engineer would search for. Both edits improve a number and damage the writing.

The honest claim is narrower and checkable: meaning preserved, voice preserved, structural features moved in a stated direction, generic patterns named with quotations.

##### How this differs from existing tools

| Dimension | Typical humanizer | Not Ai |
|---|---|---|
| Intervention level | Lexical | Clause structure and density |
| Diagnostic | Absent or vague | Deterministic counts, with quotations |
| Voice model | Fixed presets | Profile extracted from a sample, or declared absent |
| Genre awareness | None | Eight explicit profiles in `rules/context.md` |
| Meaning preservation | Implicit | Number preservation in `benchmark.py`, plus a token-overlap figure that is labelled a proxy and shown to fail |
| Over-edit protection | None | Eight-question self-review, and `KEEP` as the default action |
| Fabrication prevention | None | Explicit prohibition plus a flag mechanism |
| Model of human writing | Single target | A distribution |
| Portability | Closed product | Plain files, any agent that reads context |
| Basis | Marketing claims | Published linguistics, cited per finding |

The row on meaning preservation deserves more than the caveat it carries. `benchmark.py` compares token overlap and checks that numerals survive. Run it on the six pairs in `examples/` and it flags `Major meaning drift` on five of them, including every rewrite this repository considers correct, while awarding its highest score, 65.5%, to `already-natural`, the one pair where the text was left alone. The ranking is inverted, and the cause is structural rather than a tuning error: token overlap rewards keeping the same words, and replacing abstract nouns with concrete verbs necessarily changes the words. The full table is in `benchmarks/README.md`. An embedding-based measure would fix it and is on the contributing list. Until then the figure means surface wording similarity and nothing more.

##### Honest limits

**The scripts produce false positives on human writing, and this is demonstrated rather than hypothesised.** Run `analyze_structure.py` on `examples/already-natural/input.md`, 66 words a developer wrote about a production incident, and it raises two warnings: burstiness 0.200 flagged low, nominalization 45.5 flagged elevated. The correct intervention on that paragraph is none. The report prints six verdict lines on it and two of them are wrong.

**Burstiness does not do what its name suggests.** Across the six examples here, the human paragraph scores 0.200 and a generated LinkedIn post scores 0.799 with an explicit `Good length variation`. The post earns it on a segmentation artifact: its listicle is held together by a colon and three bolded lead-ins, so 69 words never split, and that one block against a 7-word engagement question produces the spread. The measure fell in three of the five rewrites and rose in two, while the writing improved in all five. `benchmark.py` compounds this by attaching a direction to the delta: it labels `already-natural` `improved (+0.345)`, a pair where not one word of the paragraph changed, and labels two good rewrites `worsened`, so its verdict is wrong on three of the six pairs.

The measure is kept, because sentence length distribution is a real signal in the research and the raw figure is worth seeing. Its verdicts are kept too, under 0.30 and over 0.55, but for a reason worth being explicit about: they are retained as evidence rather than as guidance. `⚠ Low burstiness` on a human paragraph and `✓ Good length variation` on a listicle are the two clearest demonstrations in this repository that a metric can be confidently wrong, and `examples/already-natural/` and `examples/linkedin-post/` are built on them. Nothing in `SKILL.md` acts on either verdict, and no stage treats raising burstiness as an objective.

**The meaning-preservation proxy is inverted on this repository's own examples.** Token overlap flags five of the six pairs for `Major meaning drift`, including every rewrite considered correct here, and awards its highest score to the one pair where the text was left alone. A measure that ranks the examples backwards cannot be used as a gate, so nothing in `SKILL.md` consults it. Details in `benchmarks/README.md`.

**The participial clause detector has a known false negative.** Its pattern is anchored to the first word of the sentence, so `By leveraging the power of...` does not match. It is also defined on openers only, so a participial clause in the middle of a sentence is outside its scope by construction. The strongest single signal in the research is the one this proxy is worst at detecting. The reading of `examples/technical-passage/` finds four present participial clauses, two of them sentence-initial behind `By` and two mid-sentence, and the script scores the passage 0 of 12. The report prints the anchoring caveat under the figure whenever the count is 0, which is every file in this repository except `examples/academic-abstract/input.md`, and carries it in the `caveat` key on every `--json` run.

**A stance verdict now requires a floor under it, and the version without one was wrong on every file here.** `stance_balance` compared the hedge and booster counts directly and returned one of three verdicts unconditionally, so a text with neither fell through to `calibrated`, because `0 > 0` is false in both branches. Seventeen files in this repository got a verdict out of that function and not one of them was right, including twelve that carried no stance marker at all and were told they were calibrated. The fix reports `absent` and `too sparse to judge` as themselves, and holds a balance verdict back until 3 markers and 2.0 per 1,000 words. Both floors are heuristics on this proxy's scale. No paper reports them, and absent stance is not a defect on its own: a passage explaining how a cache works has nothing to hedge. Whether the gap matters is genre judgment, which is why the scripts report it and `SKILL.md` rules on it.

**The two newest checks are this repository's own, with no research multiplier behind either.** Repeated sentence frames and three-item series are both listed as observable signs in `references/wikipedia-signs.md`, and neither has a measured human rate anywhere in the literature cited here. So the frame check warns on the narrowest condition available, one frame in two adjacent sentences, because a rate threshold would have to be invented and any figure chosen would have been fitted to the text in front of whoever chose it. The series check warns on nothing except anaphora across all three items, and otherwise prints its list for a reader to run the deletion test on.

**Both of those checks have false positives, and they are held as tests rather than described in passing.** A comma followed by an `-ing` word matches a gerund subject, so `In conclusion, caching remains an indispensable tool` counts as a frame. A series needs the Oxford comma to be seen at all, so `a room, a window and a reviewer` is missed entirely. An opening adverbial in front of a compound sentence yields three comma segments, so `Economically, India grew, and Bollywood thrived` is reported as a series when it is not one. A pipe is not a sentence terminator, so a table cell ending in a comma series gets joined to the paragraph below it and the third item is collected from prose that has nothing to do with the list. A heading is not a sentence terminator either, so two matches separated by a heading are read as adjacent. Fenced blocks and quoted specimens are prose to both checks, so a file that cites a frame inherits a warning for it, which is why the example inputs, the tables that discuss them and the rule page that names the frames all report frames they only quote. Every one of those cases is pinned in `scripts/verify_checks.py` as a `KNOWN LIMIT`, so none of the behaviour can change without a control failing.

**Running the two checks over this repository is the use they were built for, and the result belongs on the record.** The frame check reports seven adjacent pairs across five files, and every one of them lands in a class named above. Two are in `examples/technical-passage/input.md`, machine-written and the exact material the check exists to catch, so those are the check succeeding. Three more are pages charged for a specimen they quote, two in `rules/rhythm.md` and one in `references/style-research.md`, and in one of those the `> ` line after a colon is read as part of the sentence that introduced it. One is in `examples/personal-essay/rationale.md`, where a table cell quoting a specimen sits beside a blockquote quoting another.

The seventh is the only one drawn from prose this repository wrote in its own voice, and both halves of it are wrong. It matches `including` in one sentence, a preposition rather than a participle, and `existing` in the next, which belongs to a different section of `references/wikipedia-signs.md`. A level-3 heading stands between the two. A heading carries no terminal punctuation, so the sentence splitter runs the end of one section, the heading and the body of the next into one sentence, and the adjacency the warning rests on does not exist on the rendered page. `dist/SKILL.md` reports those seven pairs and no others, inherited from the sections it inlines.

The anaphora warning fires six times across the source markdown, and reading each one clears all six. One is the table artifact above. The other five are enumerations of three, four, five and eight items in which every item carries a figure, a reading or a step that cutting it would lose: three burstiness scores in `examples/already-natural/README.md`, the three stages of the study's two-chunk design in `references/style-research.md`, and the eight self-review questions summarised in this file. That is the division of labour working as designed. The script found the parallelism, and a reader decided case by case that the parallelism was the shape of the content rather than a cadence laid over it. `dist/SKILL.md` reports those six and one more, `a bigger room, a longer window, and a second reviewer`, which sits in a comment inside the embedded measurer: the check firing on the fixture written to demonstrate it.

**Proxy figures and research figures are different measures.** The scripts count suffixes with regular expressions; the research parsed dependencies and applied Biber's tagset. Across the five model-generated inputs in `examples/` the proxy averages 80.0 per 1,000 words against the tagged 14.6, about five and a half times, and the per-file figures are in `references/style-research.md`. Compare a proxy figure only against another run of the same script.

**A script measures a file, not a deliverable.** Where an output contains flags and bracketed slots addressed to the author, those words are counted as prose. In `examples/gen-ai-article/` three flagged vocabulary terms survive into the output solely because the flag quotes them as examples of what was removed. In `examples/personal-essay/` five separate readings, including the file's only stance marker, come from editorial notes rather than from the essay. No script can tell citation from use.

**The measurements reflect 2024 and 2025 model behaviour.** Reinhart et al. sampled models of that period. Em dash frequency has already shifted: as of mid-2026 only Claude exceeds professional human writers on it, ChatGPT uses fewer than it did, and GPT-5.1 suppresses them further. Rules and thresholds here need revisiting as models change, and fine-tuning on genre-specific data can reduce the fingerprint substantially.

**Genre detection is imperfect.** Stage 0 states its inference explicitly and invites correction, because a genre error propagates through every later stage in the same direction.

**Short voice samples give thin profiles.** Under roughly 200 words the profile is approximate at best, and the skill says so rather than overfitting to a paragraph.

**The skill cannot verify facts.** A factual error in the source survives the rewrite. Fact-checking is the author's.

**The evidence base is predominantly English.** The structural patterns differ in other languages and the cross-language behaviour of these rules is unstudied.

**This is not a route around academic or professional honesty rules.** Using the skill to pass model-written work off as your own where that is prohibited is a misuse of it. The purpose is writing that communicates, and the best writing still comes from someone who knows what they want to say. The skill can help with presentation. It cannot supply substance, and `examples/gen-ai-article/` is here to show what it does when asked to.

## Appendix C. Worked examples

Six examples, each with the draft, the diagnostic, the rewrite and the reasoning.
Read `examples/gen-ai-article/` first: it shows both the correct output and the
plausible, well-written, entirely fabricated output that an earlier version of
this skill produced, which is the failure the three overriding rules exist to
prevent. Read `examples/already-natural/` second, because its correct answer is
to change nothing.

Commands quoted inside these examples refer to the multi-file repository. Every
figure they report reproduces under `scripts/measure.py` below.

### examples/gen-ai-article/

#### examples/gen-ai-article/README.md

##### Gen AI article

A generated article opening about generative AI. Five sentences, 99 words, and no facts.

| File | |
|---|---|
| `examples/gen-ai-article/input.md` | The generated paragraph, 99 words |
| `examples/gen-ai-article/diagnostic.md` | Stage 2 diagnostic and the measured figures |
| `examples/gen-ai-article/output.md` | Two sentences and a flag block |
| `examples/gen-ai-article/rationale.md` | The accounting, and the fabricated rewrite this repository used to ship |

**What this example is for.** It is the test case for rule 1, never fabricate. The input contains no checkable claim anywhere, so a rewrite cannot contain one either. The correct output is short, mostly slots, and it tells the author that there is no article here yet.

`rationale.md` reproduces what an earlier version of this repository shipped as the correct output: a well-paced, specific, readable paragraph in which every specific was invented. That version also claimed to have removed three em dashes while shipping two. Both failures are why Stage 5 of `SKILL.md` ends with the question "do the changes I am about to describe match the changes I actually made".

It also shows a measurement trap. Three flagged vocabulary terms survive into the output, all of them inside the flag block that quotes them as examples of what was cut. The script measures a file, not a deliverable.

#### examples/gen-ai-article/input.md

Specimen. Fenced so that its em dashes and flagged vocabulary stay quoted rather than becoming this document's own prose.

```text
In today's rapidly evolving technological landscape, Generative AI represents a paradigm shift in how we approach problem-solving and innovation. By leveraging the power of large language models, organizations across various sectors are fundamentally transforming their operational frameworks. Furthermore, the implications of this transformative technology are far-reaching and multifaceted. It is worth noting that while the benefits are substantial, the challenges are equally significant. In conclusion, as we navigate this unprecedented era of technological advancement, it is crucial that we foster a nuanced understanding of both the opportunities and the ethical considerations that accompany this groundbreaking innovation.
```

#### examples/gen-ai-article/diagnostic.md

##### Diagnostic: gen AI article

Produced at Stage 2 of the procedure in `SKILL.md`.

```
NOT AI DIAGNOSTIC
Genre:    General-audience article opening, inferred. No genre was given.
Register: 4 of 5. Aimed at a general reader, pitched at a consulting report.

Working already:
  Nothing. This is the rare case where the honest answer to "quote a sentence that
  needs no change" is that there is no such sentence, because there is no sentence
  here that makes a claim a reader could check, agree with or dispute.

Patterns found:
  mechanical frame        "In today's rapidly evolving technological landscape"
  participial clause      "By leveraging the power of large language models"
  mechanical transition   "Furthermore, the implications of this transformative
                          technology are far-reaching and multifaceted."
  mechanical frame        "It is worth noting that while the benefits are substantial,
                          the challenges are equally significant."
  empty conclusion        "In conclusion, as we navigate this unprecedented era..."
  significance claim      "represents a paradigm shift"
  vague attribution       "organizations across various sectors"
  uniform sentence shape  5 sentences, 4 of them framing, none carrying a fact

Vocabulary in context:
  "paradigm shift" 1x     Problem. The shift is asserted, never described.
  "leveraging" 1x         Problem. Heads a participial clause.
  "transformative" 1x     Problem. Significance claim with no content.
  "groundbreaking" 1x     Problem. Second significance claim about the same thing.
  "multifaceted" 1x       Problem. Says the implications have facets. Name one.
  "nuanced" 1x            Problem. "a nuanced understanding" of nothing specified.
  "crucial" 1x            Problem.
  "foster" 1x             Problem.
  "rapidly evolving" 1x   Problem, and the ninth term the script counts. It sits
                          inside the opening frame quoted above.

Intervention: heavy, and the honest recommendation is to write the passage again
              from source material rather than to rewrite this text
```

###### Measured

```
python3 scripts/analyze_structure.py examples/gen-ai-article/input.md
python3 scripts/metrics.py examples/gen-ai-article/input.md
```

| Measure | Value |
|---|---|
| Words / sentences / paragraphs | 99 / 5 / 1 |
| Nominalization density | 70.7 per 1,000 words, high for this proxy |
| Mechanical transitions | 3 |
| AI-associated vocabulary | 9 unique terms in 99 words |
| Burstiness | 0.388 |
| Flesch-Kincaid grade | 17.2 |
| Gunning Fog | 21.3 |
| Flesch Reading Ease | 7.3 out of 100 |
| Density score | 53.5, high |

Nine flagged terms in 99 words is about 91 per 1,000, second in this example set only to the LinkedIn post at 99 per 1,000. The reading ease of 7.3 is second lowest too, after the academic abstract at -0.5. Both figures agree with the reading, which is not always the case.

###### The finding that determines the rewrite

**The passage contains no facts.** Not few. None.

Work through it. `Generative AI represents a paradigm shift`: an assertion, unsupported. `Organizations across various sectors are transforming their operational frameworks`: which organizations, which sectors, what changed. `The implications are far-reaching and multifaceted`: no implication is named. `The benefits are substantial and the challenges are equally significant`: neither is specified. `We must foster a nuanced understanding of the opportunities and the ethical considerations`: no opportunity and no consideration appears anywhere in the text.

This matters more than any structural pattern, because it bounds what a rewrite can legitimately do. Rule 1 in `SKILL.md` forbids inventing content. A passage with no content therefore cannot be rewritten into a passage with content. It can only be shortened to the two claims it does gesture at, with flags for what the author must supply.

Any tool that returns a confident, readable, specific paragraph from this input has fabricated the specifics. `rationale.md` shows one that did.

#### examples/gen-ai-article/output.md

Generative AI is in routine use at [organisations the author can name], for [what those organisations actually use it for]. The gains and the costs are both real: [one specific gain, with evidence] set against [one specific cost, with evidence].

[FLAG: nothing else in the source survives. The remaining 66 words are only framing that makes claims without content: "paradigm shift", "far-reaching and multifaceted", "unprecedented era of technological advancement", "nuanced understanding". There is no fact underneath them to carry over, so there is nothing to rewrite. Supply the material or cut the passage.]

#### examples/gen-ai-article/rationale.md

##### Rationale: gen AI article

The output is two sentences and a flag block. This file explains why that is the correct answer, and shows the wrong answer that an earlier version of this repository shipped.

###### Actions taken

| Source | Action | Result |
|---|---|---|
| "In today's rapidly evolving technological landscape," | REMOVE | Pure framing. Carries no information at any level. |
| "Generative AI represents a paradigm shift in how we approach problem-solving and innovation." | REMOVE | An unsupported significance claim. Nothing survives it. |
| "By leveraging the power of large language models, organizations across various sectors are fundamentally transforming their operational frameworks." | REPLACE, FLAG | "Generative AI is in routine use at [organisations the author can name], for [what those organisations actually use it for]." The claim shape is kept; the vagueness becomes visible as two slots. |
| "Furthermore, the implications of this transformative technology are far-reaching and multifaceted." | REMOVE | Says the implications have implications. |
| "It is worth noting that while the benefits are substantial, the challenges are equally significant." | REPLACE, FLAG | "The gains and the costs are both real: [one specific gain, with evidence] set against [one specific cost, with evidence]." |
| "In conclusion, as we navigate this unprecedented era of technological advancement, it is crucial that we foster a nuanced understanding of both the opportunities and the ethical considerations that accompany this groundbreaking innovation." | REMOVE | 33 words, the longest sentence in the source. Restates sentence four, adds a call to understand things that were never named. |

Five sentences in, two out, four slots flagged. That ratio is the diagnosis.

###### Measured before and after

```
python3 scripts/analyze_structure.py examples/gen-ai-article/input.md
python3 scripts/analyze_structure.py examples/gen-ai-article/output.md
```

| Measure | Before | After |
|---|---|---|
| Words | 99 | 93 |
| Nominalization density | 70.7, high | 53.8, high |
| Mechanical transitions | 3 | 0 |
| AI-associated vocabulary | 9 unique | 3 unique |
| Flesch-Kincaid grade | 17.2 | 11.5 |
| Gunning Fog | 21.3 | 14.8 |
| Flesch Reading Ease | 7.3 | 46.0 |
| Burstiness | 0.388 | 0.380 |

###### Reading these numbers correctly

**The word count barely moved, 99 to 93, and that is misleading.** Of the output's 93 words, 53 are the flag block, which is instruction to the author rather than part of the deliverable, and another 35 are the four bracketed slots. That leaves 18 words of finished prose. Word count is measuring the wrong thing here.

**Three flagged vocabulary terms remain, and all three are inside the flag block.** `paradigm shift`, `nuanced` and `multifaceted` appear in the output only because the flag quotes them as examples of what was removed. The script cannot tell the difference between a word being used and a word being cited. `references/wikipedia-signs.md` documents the same problem in reverse.

The repository handles it by convention rather than by fixing the scripts, which cannot be fixed. Every specimen sits inside one of four markers: a fenced code block, inline backticks, a `> ` blockquote line, or double quotation marks. A scanner that strips those four before counting finds no unquoted use of a flagged term anywhere in the repository outside the six `input.md` files, which are specimens end to end. The convention is what makes the claim checkable; without it, a file arguing against `leveraging` is indistinguishable from a file using it.

**Nominalization stayed high, 70.7 to 53.8.** Same cause. Of the five suffix matches the proxy finds in the output, `advancement` is quoted inside the flag as an example of what was cut, and the other four, `organisations` twice and `evidence` twice, are inside bracketed slots. Not one of them is in the finished prose.

The lesson is not that the scripts are broken. It is that they measure a file, and a file can contain both a deliverable and commentary about the deliverable. Read what you are measuring.

**Burstiness barely moved**, 0.388 to 0.380, which `benchmark.py` reports as `unchanged (-0.008)`. It is the one pair in this set where the measure says nothing either way, and that is the most honest reading available: the deliverable is two sentences and a flag block, so there is no rhythm here to measure.

###### The wrong answer this repository used to ship

An earlier version of this example returned the following, presented as the correct output:

> Generative AI went mainstream quietly. Not with a product launch, with your colleagues starting to use it for first drafts, your inbox filling with emails that sound oddly similar, your company's job postings adding "AI literacy" to requirements. The shift happened in the daily routine before anyone declared it a shift.
>
> What it does well: it writes fast and reads passably. What it does badly: it has no idea when it's wrong. A model will state a fabricated statistic with the same confidence it states a verified one.

It reads well. It is specific, concrete, well-paced, and every single specific in it is invented. The source says nothing about first drafts, nothing about inboxes, nothing about job postings, nothing about fabricated statistics. A model wrote a better article than the input and attributed it to the author.

This is the failure this skill exists to avoid, and it is more dangerous than the vague original, because vagueness is visible and confident fabrication is not. An author who accepted that paragraph would be publishing claims they never made and cannot defend.

The old version also claimed in its own change table that it had removed "3 em dashes → 0" while the paragraph it shipped still contained two. That is the exact failure Stage 5 question 8 was added to catch: do the changes I am about to describe match the changes I actually made.

###### What a legitimate rewrite would need

Source material. Specifically: which organisations, doing what, with what measured result, and one named cost with evidence. With those four facts the passage could become something worth reading in about 120 words. Without them there is no article, and saying so is more useful to the author than a polished paragraph that sounds like one.

### examples/academic-abstract/

#### examples/academic-abstract/README.md

##### Academic abstract

A generated abstract for an NLP paper. 140 words, five sentences, formal register that is entirely correct for the genre.

| File | |
|---|---|
| `examples/academic-abstract/input.md` | The generated abstract, 140 words |
| `examples/academic-abstract/diagnostic.md` | Stage 2 diagnostic and the measured figures |
| `examples/academic-abstract/output.md` | The rewrite, 108 words, six bracketed slots |
| `examples/academic-abstract/rationale.md` | Per-sentence accounting, the declared addition, and the metric that should be ignored |

**What this example is for.** Register discipline. Every other example in this set gets shorter, plainer and more conversational; this one must stay formal or it becomes unpublishable. The rewrite keeps third person, keeps the passive where the genre uses it, keeps `classification` and `availability` rather than reaching for verbs, and lands at grade 14.9 rather than the grade 6.0 that `examples/technical-passage/` reached.

It is also the example where a warning should be read and then declined. Nominalization density falls only from 92.9 to 83.3 and stays flagged as high, because academic abstracts nominalize by design. Compare `examples/technical-passage/`, where the same measure fell from 95.4 to 17.3 and the drop was the right outcome. Identical warning, opposite correct response, decided by genre.

Two smaller observations. This is the only input in the set where the participial-clause detector fires, because `Leveraging a novel experimental framework` puts the participle in the first word; the two `By ...ing` clauses in `examples/technical-passage/` were missed entirely. And burstiness rose here, 0.201 to 0.604, the only rewrite in the set where it moved in the expected direction.

#### examples/academic-abstract/input.md

Specimen. Fenced so that its em dashes and flagged vocabulary stay quoted rather than becoming this document's own prose.

```text
This paper presents a comprehensive investigation into the nuanced relationship between machine learning model complexity and downstream performance across diverse natural language processing tasks. Leveraging a novel experimental framework that systematically varies model architectures, we demonstrate that the conventional assumption that larger models invariably outperform smaller counterparts is not universally applicable. Our findings reveal that, in certain task-specific contexts, models of moderate complexity exhibit comparable or superior performance metrics relative to their larger counterparts, particularly when training data is limited in scope. Furthermore, the implications of these findings are significant for practitioners seeking to optimize resource utilization while maintaining competitive performance levels. We conclude that a more nuanced, context-dependent approach to model selection is warranted, one that takes into consideration the specific requirements of the task at hand rather than defaulting to scale as a proxy for quality.
```

#### examples/academic-abstract/diagnostic.md

##### Diagnostic: academic abstract

Produced at Stage 2 of the procedure in `SKILL.md`. This is the example where register does most of the work.

```
NOT AI DIAGNOSTIC
Genre:    Abstract for an NLP or ML paper. Inferred from content and structure.
Register: 5 of 5. Reviewers and researchers in the field. Correctly formal.

Working already:
  "the conventional assumption that larger models invariably outperform smaller
  counterparts is not universally applicable"
  This is the paper's actual finding and it is stated clearly. The abstract has a
  real result underneath the prose, which distinguishes it from
  examples/gen-ai-article/ and makes a genuine rewrite possible.

Patterns found:
  participial clause      "Leveraging a novel experimental framework that
                          systematically varies model architectures"
  mechanical transition   "Furthermore, the implications of these findings are
                          significant for practitioners"
  significance inflation  "the implications of these findings are significant"
  redundant closing       Sentence 5 restates the finding from sentence 2
  uniform sentence shape  5 sentences of 24, 27, 31, 20 and 36 words
  hedge stacking          "in certain task-specific contexts", "comparable or
                          superior", "particularly when", all in one sentence

Vocabulary in context:
  "nuanced" 2x            Problem. Twice in 140 words, and neither instance
                          specifies what the subtlety consists of.
  "comprehensive" 1x      Problem. "a comprehensive investigation into" is four
                          words that mean "we studied".
  "leveraging" 1x         Problem. Heads the participial clause.
  "utilization" 1x        Problem in "optimize resource utilization". "use less
                          compute" is the claim.
  "invariably"            Fine. Precise here, and the sentence needs it.
  "downstream performance", "task-specific", "training data"
                          Fine. Field-standard terms. Keep all of them.

Specificity, the critical issue:
  "diverse natural language processing tasks"   which tasks
  "certain task-specific contexts"              which contexts
  "models of moderate complexity"               moderate by what measure
  "training data is limited in scope"           limited below what threshold
  "comparable or superior performance metrics"  which metrics, and by how much
  Five unfilled specifics in a 140-word abstract. The author has all five values.

Intervention: moderate
```

###### Measured

```
python3 scripts/analyze_structure.py examples/academic-abstract/input.md
python3 scripts/metrics.py examples/academic-abstract/input.md
```

| Measure | Value |
|---|---|
| Words / sentences | 140 / 5 |
| Mean sentence length | 27.6 words |
| Burstiness | 0.201, ⚠ low |
| Participial clause openers | 1 of 5, 20%, ⚠ high for this proxy |
| Nominalization density | 92.9 per 1,000 words, ⚠ high for this proxy |
| Mechanical transitions | 1 |
| AI-associated vocabulary | 4 unique |
| Flesch-Kincaid grade | 20.3 |
| Gunning Fog | 24.6 |
| Flesch Reading Ease | -0.5 out of 100 |
| Density score | 69.3, high |

###### Reading the numbers against the genre

**This is the one input where the participial detector fires**, 1 of 5 sentences, because `Leveraging a novel experimental framework` puts the participle in the first word. Compare `examples/technical-passage/`, where two participial clauses beginning with `By` were missed entirely. The detector is not measuring participial clauses; it is measuring participles in sentence-initial position.

**Nominalization at 92.9 is high and mostly legitimate.** `Investigation`, `performance`, `assumption`, `utilization`, `consideration`, `requirements`. Academic abstracts nominalize because they describe methods and findings rather than actions by people, and the register expects it. The problem is not the density. It is that `a comprehensive investigation into the nuanced relationship between X and Y` conveys no more than `we tested whether X affects Y` while occupying three times the space.

Do not lower this number for its own sake. `rules/context.md` covers the register rule: in an academic abstract, nominalization is a feature.

**Reading ease of -0.5 is below zero**, which the Flesch scale permits and which means the sentences are long and the words are polysyllabic. In this genre that is close to normal and it is not by itself a finding.

**Burstiness of 0.201** is a genuine problem here, unlike in `examples/already-natural/` where the same figure was harmless. Five sentences between 20 and 36 words with no short one among them gives a reviewer nowhere to rest. The identical number means opposite things in the two texts, which is the argument for reading before concluding.

#### examples/academic-abstract/output.md

Larger language models do not always outperform smaller ones. This paper tests that assumption on [the specific tasks, for example named entity recognition, text classification and extractive question answering], varying architecture systematically while holding the training budget fixed.

Models below [X] parameters matched or exceeded larger models on [which of those tasks] when training data fell below [N] examples. The gap narrowed further under [the specific condition].

Model selection should therefore account for data availability and task type rather than scale alone. [State the implication concretely: for a practitioner choosing between a 7B and a 70B model on a domain task with fewer than 10,000 labelled examples, the finding predicts what?]

#### examples/academic-abstract/rationale.md

##### Rationale: academic abstract

The rewrite keeps the register and removes the padding. Formality was never the problem.

###### Actions taken

| Source | Action | Result |
|---|---|---|
| "This paper presents a comprehensive investigation into the nuanced relationship between machine learning model complexity and downstream performance across diverse natural language processing tasks." | REPLACE, MOVE | The finding moves to the front: "Larger language models do not always outperform smaller ones." An abstract should open with the result, not with an announcement that a study occurred. |
| "Leveraging a novel experimental framework that systematically varies model architectures, we demonstrate that the conventional assumption that larger models invariably outperform smaller counterparts is not universally applicable." | RESTRUCTURE, SPLIT | Participial clause becomes a finite clause. "This paper tests that assumption on [tasks], varying architecture systematically while holding the training budget fixed." |
| "Our findings reveal that, in certain task-specific contexts, models of moderate complexity exhibit comparable or superior performance metrics relative to their larger counterparts, particularly when training data is limited in scope." | RESTRUCTURE, SPLIT, FLAG | "Models below [X] parameters matched or exceeded larger models on [which of those tasks] when training data fell below [N] examples." Three hedges removed, three slots opened. |
| "Furthermore, the implications of these findings are significant for practitioners seeking to optimize resource utilization while maintaining competitive performance levels." | REMOVE | Asserts that the implications are significant without naming one. |
| "We conclude that a more nuanced, context-dependent approach to model selection is warranted, one that takes into consideration the specific requirements of the task at hand rather than defaulting to scale as a proxy for quality." | REPLACE, FLAG | "Model selection should therefore account for data availability and task type rather than scale alone", plus a flag asking for the concrete implication the removed sentence gestured at. |

###### What was deliberately preserved

Third person. No contractions. `Models below [X] parameters matched or exceeded` rather than `beat`. Passive constructions where the genre uses them. The hypothesis, method, finding, implication order.

The temptation with an abstract is to make it friendly. That would be a genre error, and it would get the paper desk-rejected. `rules/context.md` sets the constraint: reduce padding, keep formality.

###### Measured before and after

```
python3 scripts/analyze_structure.py examples/academic-abstract/input.md
python3 scripts/analyze_structure.py examples/academic-abstract/output.md
```

| Measure | Before | After |
|---|---|---|
| Words | 140 | 108 |
| Sentences | 5 | 5 |
| Mean sentence length | 27.6 | 22.2 |
| Burstiness | 0.201, ⚠ low | 0.604, ✓ good variation |
| Participial clause openers | 1 of 5, 20%, ⚠ | 0 of 5, 0%, ✓ |
| Nominalization density | 92.9, ⚠ high | 83.3, ⚠ high |
| Mechanical transitions | 1 | 0 |
| AI-associated vocabulary | 4 unique | 0 |
| Flesch-Kincaid grade | 20.3 | 14.9 |
| Gunning Fog | 24.6 | 17.2 |
| Flesch Reading Ease | -0.5 | 26.7 |
| Density score | 69.3 | 63.9 |

**Burstiness tripled, 0.201 to 0.604.** The largest rise in the set, and one of only two rewrites where the measure moved in the direction its name implies. `examples/personal-essay/` is the other, 0.375 to 0.600. It rose because the rewrite has two short sentences, 9 words and 8, against a 44-word one, not because variation was engineered.

**Nominalization stayed high, 92.9 to 83.3, and that is correct.** A 10% reduction on a feature the genre requires. The proxy's matches in the output include `classification`, `question`, `selection` and `availability`, which are the right words. Pushing this figure toward the conversational band would mean writing a worse abstract, and the script's `high for this proxy` label is not a defect to be fixed.

This is the clearest case in the example set for reading the register before acting on a warning.

**Grade level 20.3 to 14.9**, which lands in the right place for the genre. Compare `examples/technical-passage/`, where the same instinct overshot to grade 6.

###### One declared addition

The output contains a sentence that has no counterpart in the source:

> The gap narrowed further under [the specific condition].

Nothing in the input says the gap narrowed under any condition. The sentence exists because the input's `particularly when training data is limited in scope` implies the author measured an interaction and did not report it, and because the rewrite needed one short sentence to break a run of long ones. Both reasons are real and neither is sufficient: an author who does not have that result should delete the line rather than fill the slot.

Stage 4 of `SKILL.md` requires additions to be declared rather than slipped in. This is the declaration. It is also the weakest decision in this rewrite, and it is left in place so the example shows what a borderline call looks like instead of pretending none occur.

###### The six flags

`[the specific tasks]`, `[X] parameters`, `[which of those tasks]`, `[N] examples`, `[the specific condition]`, and a closing slot asking for the concrete practitioner implication.

An abstract with six bracketed slots looks unfinished, and it is. But the author ran the experiments and knows five of the six values. The slots take a few minutes to fill and the result is an abstract a reviewer can evaluate. The alternative, a rewrite that invents plausible thresholds, would be a fabricated experimental result in a document submitted for publication. There is no version of this skill where that is an acceptable output.

### examples/linkedin-post/

#### examples/linkedin-post/README.md

##### LinkedIn post

A generated LinkedIn post about distributed systems. 142 words, two emoji, three lessons, no facts.

| File | |
|---|---|
| `examples/linkedin-post/input.md` | The generated post, 142 words |
| `examples/linkedin-post/diagnostic.md` | Stage 2 diagnostic and the measured figures |
| `examples/linkedin-post/output.md` | The rewrite, nine bracketed slots |
| `examples/linkedin-post/rationale.md` | Per-sentence accounting, what the platform gets to keep, and the burstiness finding |

**What this example is for.** It is the counterpart to `examples/already-natural/`, and the pair is the most useful thing in this repository. There, a human paragraph drew two warnings. Here, generated text collects seven ticks: good length variation, no participial openers, no mechanical transitions, no repeated openings, no repeated phrases, 94% lexical diversity, four unique paragraph shapes. A structural scan comes back close to clean on a post nobody would mistake for human.

Everything that gives it away sits outside the structural analysis: fourteen flagged vocabulary terms in 142 words, the emoji used as structure, the listicle scaffolding, and a register pitched at journal difficulty for a feed. Read the two examples together and the argument for reading before concluding makes itself.

The burstiness case is the sharpest one in the set. This post scores 0.799 with an explicit `✓ Good length variation`, the highest figure of any file here, and the score comes from a segmentation artifact. The lengths are 20, 33, 69, 7 and 11 words. The 69-word one is the whole listicle, which never splits because it is held together by a colon and three bolded lead-ins, and the two short ones are the engagement question and the sign-off. The human paragraph in `already-natural` scores 0.200.

It is also the clearest demonstration that genre conventions are not tells. The rewrite keeps three lessons, bold lead-ins, short paragraphs and a closing question, because that is how the platform is written. What changes is that each lesson now reports an outcome instead of issuing an imperative.

#### examples/linkedin-post/input.md

Specimen. Fenced so that its em dashes and flagged vocabulary stay quoted rather than becoming this document's own prose.

```text
🚀 In today's rapidly evolving digital landscape, the ability to leverage cutting-edge technologies has become more crucial than ever before.

I've spent the last several months working with distributed systems, and I've come to realize that the key to success lies in fostering a culture of continuous improvement and meticulous attention to detail.

Here are 3 key lessons I've learned:

1. **Embrace the complexity.** Understanding the nuanced intricacies of distributed systems requires a comprehensive approach that takes multiple factors into consideration.

2. **Foster collaboration.** Building robust systems demands that we leverage the diverse perspectives of cross-functional teams to achieve transformative outcomes.

3. **Iterate relentlessly.** The most successful teams are those that continuously refine their processes, leveraging data-driven insights to drive meaningful improvements.

What strategies have you found most impactful? I'd love to hear your thoughts in the comments below! 🌟
```

#### examples/linkedin-post/diagnostic.md

##### Diagnostic: LinkedIn post

Produced at Stage 2 of the procedure in `SKILL.md`. This is the example where the structural metrics come back with seven ticks and a single warning, and the text is still unmistakably machine-written.

```
NOT AI DIAGNOSTIC
Genre:    LinkedIn post, given by the platform conventions in the text itself.
Register: 2 of 5 intended, 5 of 5 delivered. That mismatch is the finding.

Working already:
  "I've spent the last several months working with distributed systems"
  The only clause in the post that reports something the author did. It is
  concrete about duration and domain, and it uses a contraction. No change
  needed. Everything attached to it after the comma is the problem.

Patterns found:
  emoji as structure      "🚀" opening, "🌟" closing, neither carrying meaning
  mechanical frame        "In today's rapidly evolving digital landscape"
  significance inflation  "more crucial than ever before"
  abstract-noun pivot     "the key to success lies in fostering a culture of
                          continuous improvement and meticulous attention to
                          detail"
  listicle announcement   "Here are 3 key lessons I've learned:"
  bolded inline headers   "**Embrace the complexity.**" and two more, each
                          followed by one sentence of abstraction
  rule of three           Exactly three lessons, imperative-verb titles,
                          near-identical sentence shape under each
  engagement bait         "What strategies have you found most impactful?
                          I'd love to hear your thoughts in the comments below!"

Vocabulary in context:
  "leverage" 2x           Problem. Once per lesson body, both times replacing a
  "leveraging" 1x         verb that would have specified an action.
  "cutting-edge" 1x       Problem. In "cutting-edge technologies", naming none.
  "comprehensive" 1x      Problem. "a comprehensive approach that takes multiple
                          factors into consideration" is nine words for nothing.
  "transformative" 1x     Problem. "transformative outcomes", unspecified.
  "robust" 1x             Problem here. Standard in systems writing, but
                          "building robust systems" is the whole claim and no
                          system is named.
  "crucial" 1x            Problem.
  "foster" 1x             Problem. Also the title of lesson 2.
  "nuanced intricacies"   Problem, and a tautology. Intricacies are nuanced.
  "distributed systems"   Fine. Domain term, correctly used.
  "cross-functional"      Fine. Ordinary at work, not a tell.
  "I've", "I'd"           Fine. Contractions belong on this platform. Keep.
  five more flagged       "fostering", "meticulous", "rapidly evolving",
                          "impactful", "meaningful". Each is cut or replaced with
                          the sentence it sits in, quoted above. The script
                          counts 14 unique terms and 15 occurrences in total.

Intervention: heavy
```

###### Measured

```
python3 scripts/analyze_structure.py examples/linkedin-post/input.md
python3 scripts/metrics.py examples/linkedin-post/input.md
python3 scripts/repetition.py examples/linkedin-post/input.md
```

| Measure | Value |
|---|---|
| Words / sentences / paragraphs | 142 / 5 / 7 |
| Mean sentence length | 28.0 words |
| Burstiness | 0.799, ✓ Good length variation |
| Participial clause openers | 0 of 5, 0%, ✓ normal |
| Mechanical transitions | 0, ✓ none detected |
| Repeated openings | None, ✓ |
| Repeated phrases | None, ✓ |
| Lexical diversity | 94% content-word TTR, ✓ high |
| Nominalization density | 56.3 per 1,000 words, ⚠ high for this proxy |
| AI-associated vocabulary | 14 unique terms, 15 occurrences |
| Flesch-Kincaid grade | 17.3 |
| Gunning Fog | 21.2, very difficult |
| Flesch Reading Ease | 21.9 out of 100 |
| Density score | 52.1, high, characteristic of formal academic prose |

###### Seven ticks and one warning on text nobody would mistake for human

Count the passes. Good length variation. No participial openers. No mechanical transitions. No repeated openings. No repeated phrases. High lexical diversity. Four unique paragraph shapes. A structural scan of this post comes back close to clean.

The text is still obviously generated, and everything that gives it away sits outside the structural analysis: the vocabulary list, the emoji, the listicle scaffolding, and the register.

Put this next to `examples/already-natural/`, where a human paragraph drew two warnings. The two examples fail in opposite directions on the same instruments. Neither result is a bug to be patched, because no threshold adjustment fixes both. This pair is what Stage 1 of `SKILL.md` means by `direction beats magnitude`: the scripts locate candidates and a reader decides.

**Burstiness of 0.799 is the sharpest case.** It is the highest figure in the example set and it earns an explicit `✓ Good length variation`. It is also an artifact of the scaffolding rather than of rhythm. The segmenter finds five sentences of 20, 33, 69, 7 and 11 words. The 69-word one is the entire listicle: `Here are 3 key lessons I've learned:` runs on into all three bolded lessons, because neither a colon nor a `**` ends a sentence. So the spread that earns the tick is produced by one unsplittable block of scaffolding at one end and the engagement question at the other, which are the two least human things in the post. The human paragraph in `examples/already-natural/` scores 0.200 on the same measure.

**Nominalization at 56.3 is the one warning, and it is the right one.** `Ability`, `improvement`, `attention`, `complexity`, `consideration`, `collaboration`, `improvements`, `comments`. Eight suffix matches in 142 words. Two of them survive the rewrite because they sit in lesson titles the platform's conventions earn, and one is the engagement bait; the proxy cannot tell those from the rest, which is why the reader has to look. What the reader finds is abstract nouns doing the work that verbs should do in a first-person post about something the author personally did.

**The register mismatch is the actual finding.** Gunning Fog of 21.2 and reading ease of 21.9 put this post in the same difficulty band as a journal article. The density score labels it `characteristic of formal academic prose`. It is a LinkedIn post. `examples/academic-abstract/` has almost the same profile, Fog 24.6 and ease -0.5, and there the numbers are appropriate. Same instruments, same readings, opposite verdicts, decided entirely by where the text is going.

**Zero hedges and zero boosters**, which the script reports as `absent`. An earlier version of the check called that `calibrated`, a clean bill of health on a post with no claim specific enough to hedge.

###### What the rewrite is bounded by

The post reports no fact. Three lessons, none attached to a system, a change, a number or an outcome. As in `examples/gen-ai-article/`, rule 1 means the specifics cannot be supplied, so they become slots.

What can be kept is the shape. Three lessons, bold lead-ins, short paragraphs and a closing question are all native to the platform, and `rules/context.md` says genre conventions survive a rewrite. The emoji and the phrase `I'd love to hear your thoughts in the comments below` do not survive, not because they breach the platform's conventions but because they are the generic version of them.

#### examples/linkedin-post/output.md

I spent the last few months on [the actual project, named]. Three things I got wrong going in.

**The complexity was not the problem.** What kept breaking was [the specific cause, for example unclear ownership of state across two services]. Once I could name that, the fix was [what you actually did].

**Talking to the right people early beat talking to everyone often.** Bringing [which team] in before [which decision] was locked would have saved [how much rework, in whatever unit you measure it]. Review after the fact is not collaboration.

**One small change did most of the work.** Deployment time went from [X] to [Y] after [the specific change]. Nothing clever about it.

What is a systems problem you found was simpler than it looked?

[FLAG: nine slots above need real content. The original post contained no specifics at all, so none of this can be filled in from the source. The structure and the three-lesson shape are preserved because both fit the platform. If the author cannot fill the slots, the honest conclusion is that there is no post here yet.]

#### examples/linkedin-post/rationale.md

##### Rationale: LinkedIn post

The platform conventions survive. The content does not, because there was none.

###### Actions taken

| Source | Action | Result |
|---|---|---|
| "🚀 In today's rapidly evolving digital landscape, the ability to leverage cutting-edge technologies has become more crucial than ever before." | REMOVE | Emoji and frame together. The sentence names no technology and makes no claim. Nothing survives it. |
| "I've spent the last several months working with distributed systems, and I've come to realize that the key to success lies in fostering a culture of continuous improvement and meticulous attention to detail." | RESTRUCTURE, SPLIT, FLAG | Becomes "I spent the last few months on [the actual project, named]. Three things I got wrong going in." The reported experience is kept. The abstract-noun conclusion is cut, because a culture of continuous improvement is not what the author learned. |
| "Here are 3 key lessons I've learned:" | REMOVE | Announces a list that the formatting already announces. It is also what makes the listicle unsplittable: everything from this colon to the end of lesson 3 reads as one 69-word sentence, which is where the post's flattering burstiness score comes from. |
| "1. **Embrace the complexity.** Understanding the nuanced intricacies of distributed systems requires a comprehensive approach that takes multiple factors into consideration." | REPLACE, FLAG | "**The complexity was not the problem.** What kept breaking was [the specific cause] ... the fix was [what you actually did]." The lesson is inverted, because `embrace the complexity` is advice and the slot asks for an event. |
| "2. **Foster collaboration.** Building robust systems demands that we leverage the diverse perspectives of cross-functional teams to achieve transformative outcomes." | REPLACE, FLAG | "**Talking to the right people early beat talking to everyone often.**" The imperative becomes a claim with an edge to it, which is the difference between a lesson and a slogan. |
| "3. **Iterate relentlessly.** The most successful teams are those that continuously refine their processes, leveraging data-driven insights to drive meaningful improvements." | REPLACE, FLAG | "**One small change did most of the work.** Deployment time went from [X] to [Y] after [the specific change]. Nothing clever about it." |
| "What strategies have you found most impactful? I'd love to hear your thoughts in the comments below! 🌟" | REPLACE | "What is a systems problem you found was simpler than it looked?" The closing question is kept, because a question at the end is native to the platform. `impactful`, the comments-below instruction and the emoji are cut. |

###### What was deliberately kept

Three lessons, in that order, with bold lead-ins and one short paragraph each. First person. Short paragraphs with blank lines between them. A closing question.

None of that is a machine pattern. It is how the platform is written, and `rules/context.md` protects genre conventions from being stripped as though they were tells. An agent that flattened this into three flowing paragraphs would have produced better prose and a worse LinkedIn post.

What changed inside the shape is that each lesson now states an outcome rather than issuing an imperative. `Embrace the complexity` tells the reader what to do. `The complexity was not the problem` tells them what happened, which they can disagree with.

###### Measured before and after

```
python3 scripts/analyze_structure.py examples/linkedin-post/input.md
python3 scripts/analyze_structure.py examples/linkedin-post/output.md
python3 scripts/metrics.py examples/linkedin-post/output.md
```

| Measure | Before | After |
|---|---|---|
| Words | 142 | 184 |
| Sentences | 5 | 9 |
| Paragraphs | 7 | 6 |
| Mean sentence length | 28.0 | 20.3 |
| Burstiness | 0.799, ✓ good variation | 0.540 |
| Nominalization density | 56.3, ⚠ high | 16.3, ✓ normal |
| Mechanical transitions | 0 | 0 |
| AI-associated vocabulary | 14 unique, 15 occurrences | 0 |
| Lexical diversity | 94% | 92% |
| Flesch-Kincaid grade | 17.3 | 8.7 |
| Gunning Fog | 21.2, very difficult | 11.4, standard |
| Flesch Reading Ease | 21.9 | 68.8 |
| Density score | 52.1, high | 31.0, moderate |
| Hedges / boosters | 0 / 0, `absent` | 1 / 0, `too sparse to judge` |
| First-person markers | 5, 35.7 per 1,000 | 3, 16.4 per 1,000 |

**Nominalization 56.3 to 16.3 is the real change.** `Ability`, `improvement`, `attention`, `consideration`, `improvements` and `comments` are gone, and what replaced them are verbs with subjects: `what kept breaking`, `deployment time went from`, `I got wrong`. Three suffix matches remain, `complexity`, `collaboration` and `Deployment`, and all three are load-bearing: two are lesson titles the platform earns and the third names the thing that was measured. This is the measure most worth trusting across the whole example set, because it moved down in every one of the five rewrites and each time for the same reason.

**Grade level 17.3 to 8.7 and reading ease 21.9 to 68.8.** Both now match the platform. The abstract read at journal difficulty and should have; this post read at journal difficulty and should not have.

**Burstiness fell from 0.799 to 0.540, and the fall is an improvement.** The 0.799 came from the segmenter finding five sentences of 20, 33, 69, 7 and 11 words. The 69-word one was the whole listicle, held together by a colon and three bolded lead-ins so that nothing in it split; the 7 and the 11 were the engagement question and the sign-off. Break the listicle into real sentences and that spread collapses. The rewrite has nine sentences spread across one very short, two short, three medium, two long and one very long, which is real variation, and it scores lower.

Burstiness fell in three of the five rewrites in this set while the writing improved in all three. It rose in the other two, `examples/academic-abstract/` and `examples/personal-essay/`. A metric that moves in both directions on improvements, gives a human paragraph 0.200 and a generated post 0.799, is not measuring what its name suggests. One counterexample would be noise; this many is a finding about the instrument.

**The output is longer, 142 to 184 words.** Two causes. The 58-word flag block, which is instruction rather than deliverable, and the slots, which are verbose by design: `[how much rework, in whatever unit you measure it]` is nine words standing in for two. Between them the bracketed text is 96 of the output's 184 words, so more than half of what the scripts measure here is not the post. Filled in, the post lands near 120 words, shorter than the original.

**Hedges went from 0 to 1, and the balance verdict moved from `absent` to `too sparse to judge`.** The single marker is `could`, in `Once I could name that`, which is past ability rather than hedging. One marker sits below the three-marker floor, so the script declines to read a ratio from it. The refusal holds up on two counts: a single marker is too little to divide, and this marker is not doing the work its pattern implies. Both readings agree about the post itself, which makes no claim precise enough to need a hedge.

###### Nine slots, and why the post is still worth delivering

`examples/gen-ai-article/` had four slots and the verdict was that no article existed yet. This post has nine and the verdict is different, because the author did the work. They spent months on a real project, something specific broke, someone should have been consulted earlier, and one change had an outsized effect. Those four facts exist in the author's memory and are absent from their draft. That is a retrieval problem, not an emptiness problem.

The generated version buried them under `fostering a culture of continuous improvement`, which is a phrase that fits any project in any industry in any decade. The rewrite is a form the author can fill in about fifteen minutes, and the filled version would be a post only they could have written.

If the slots cannot be filled, the same conclusion applies as in the gen AI article: there is no post here, and saying so is the useful answer.

### examples/technical-passage/

#### examples/technical-passage/README.md

##### Technical passage

An instruction-tuned model was asked to explain how a caching system works. The technical content is correct; the prose is dense, inflated and built to a template.

| File | |
|---|---|
| `examples/technical-passage/input.md` | The generated text, 241 words |
| `examples/technical-passage/diagnostic.md` | Stage 2 diagnostic and the measured figures |
| `examples/technical-passage/output.md` | The rewrite, 173 words |
| `examples/technical-passage/rationale.md` | Sentence-level accounting, before and after numbers, and what the rewrite got wrong |

**What this example is for.** It is the clearest demonstration that the analysis scripts miss the strongest signal in the research. The reading finds four present participial clauses; `analyze_structure.py` reports 0 of 12. Two of them, `By leveraging the power of...` and `By thoughtfully implementing...`, are sentence openers that the pattern misses because it is anchored to the first word and both begin with `By`. The other two, `ensuring that users receive responses in a timely manner` and `distributing the load across multiple layers`, sit mid-sentence, which the pattern does not look at at all. So the count is short for two separate reasons and the printed figure is 0% either way.

It also shows a rewrite scoring worse on a metric while reading better. Burstiness fell from 0.471 to 0.415, and the rationale explains why that is the metric's problem rather than the rewrite's.

#### examples/technical-passage/input.md

Specimen. Fenced so that its em dashes and flagged vocabulary stay quoted rather than becoming this document's own prose.

```text
In the realm of modern software architecture, caching represents a pivotal mechanism that fundamentally transforms how applications manage and retrieve data. By leveraging the power of temporary storage solutions, systems can significantly enhance their overall performance metrics while simultaneously reducing the burden on primary data sources.

At its core, caching operates by storing frequently accessed data in a location that can be retrieved more rapidly than the original source. This approach offers several key advantages. First, it dramatically reduces latency, ensuring that users receive responses in a timely manner. Second, it alleviates the computational overhead associated with repeated database queries. Third, it enables applications to scale more effectively by distributing the load across multiple layers of the system architecture.

Furthermore, modern caching implementations typically incorporate sophisticated expiration policies to ensure data freshness. These policies, ranging from time-based invalidation to event-driven cache busting, play a crucial role in maintaining the delicate balance between performance and consistency. It is worth noting that the selection of an appropriate caching strategy is a nuanced decision that requires careful consideration of multiple factors, including but not limited to the nature of the data, access patterns, and the specific requirements of the application in question.

In conclusion, caching remains an indispensable tool in the arsenal of modern software engineers. By thoughtfully implementing and managing caching solutions, development teams can achieve remarkable improvements in application performance, ultimately delivering a superior user experience to their end users.
```

#### examples/technical-passage/diagnostic.md

##### Diagnostic: technical passage

Produced at Stage 2 of the procedure in `SKILL.md`.

```
NOT AI DIAGNOSTIC
Genre:    Technical explanation, inferred from content. No genre was given.
Register: 4 of 5. Written for working developers, currently pitched at a journal.

Working already:
  "caching operates by storing frequently accessed data in a location that can be
  retrieved more rapidly than the original source"
  The technical content is correct and the definition is the right one. Nothing in
  this passage is factually wrong, which sets the constraint: this is a rewrite for
  density and framing, not for accuracy.

Patterns found:
  participial clause      "By leveraging the power of temporary storage solutions"
  participial clause      "By thoughtfully implementing and managing caching solutions"
  participial clause      "ensuring that users receive responses in a timely manner"
  participial clause      "distributing the load across multiple layers"
  mechanical frame        "In the realm of modern software architecture"
  mechanical frame        "It is worth noting that the selection of an appropriate..."
  mechanical frame        "Furthermore, modern caching implementations typically..."
  empty conclusion        "In conclusion, caching remains an indispensable tool in
                          the arsenal of modern software engineers"
  enumerated tricolon     "First... Second... Third..." across three real advantages
  uniform paragraphs      4 paragraphs of 2, 5, 3 and 2 sentences, every one of them
                          opening with a claim and following it with support
  overloaded paragraph    paragraph 3 carries expiration policy types, cache busting,
                          data freshness and strategy selection in three sentences

Vocabulary in context:
  "pivotal" 1x            Problem. The claim is not supported and not needed.
  "leveraging" 1x         Problem. Decorative, and it heads a participial clause.
  "nuanced" 1x            Problem. "a nuanced decision" claims subtlety, supplies none.
  "crucial" 1x            Problem. Expiration policies matter; say why instead.
  "indispensable", "remarkable improvements", "superior user experience"
                          Problem. Three significance claims in the closing paragraph.
  "including but not limited to"
                          Problem. Legal register, wrong genre.
  "latency", "invalidation", "cache busting"
                          Fine. Domain terms doing real work. Keep all three.

Intervention: moderate
```

###### Measured

Run against `input.md`:

```
python3 scripts/analyze_structure.py examples/technical-passage/input.md
python3 scripts/metrics.py examples/technical-passage/input.md
```

| Measure | Value |
|---|---|
| Words / sentences / paragraphs | 241 / 12 / 4 |
| Nominalization density | 95.4 per 1,000 words, high for this proxy |
| Participial clause openers | 0 of 12, 0% |
| Mechanical transitions | 4 |
| Burstiness | 0.471 |
| Flesch-Kincaid grade | 16.4 |
| Gunning Fog | 20.5 |
| Density score | 74.3, high |
| AI-associated vocabulary | 4 unique terms |

###### Where the script and the reading disagree

**The script reports 0 of 12 participial clause openers. The reading found four participial clauses.** The script is wrong here, and predictably so, for two separate reasons. Its pattern is anchored to the first word of the sentence, so `By leveraging the power of...` and `By thoughtfully implementing...` do not match, because both begin with `By` rather than with the participle. The other two, `ensuring that users receive responses in a timely manner` and `distributing the load across multiple layers`, are mid-sentence and the pattern never looks there. The docstring in `analyze_structure.py` documents the anchoring; the second gap follows from the measure being defined on openers only.

This is the single most important thing this example demonstrates. The strongest signal in the research is the one the script is worst at detecting. A 0% participial rate means "none of the anchored forms", not "none". Read the text.

**Burstiness of 0.471 does not trigger a warning**, and the reading still found uniform paragraph shape. Burstiness measures sentence length variation only. It is blind to four paragraphs built to the same template.

#### examples/technical-passage/output.md

Caching keeps a copy of data somewhere faster to reach than the original. That is the whole idea. Everything else is detail about where the copy lives and when you throw it away.

The payoff is real but bounded. A read that hits the cache skips the database entirely, so it returns faster and the database does less work. Both effects compound under load, which is when you need them.

The hard part is deciding when a cached copy has gone stale. Time-based expiry is simple: hold the copy for a fixed window, then fetch again. Event-driven invalidation is more precise and more work, because something has to notice the underlying data changed and say so. Which one fits depends on how bad it is to serve a stale value, and that varies enormously between systems. A stale follower count is a cosmetic problem. A stale account balance is not.

So the real decision is not about caching. It is about how much staleness the thing you are building can absorb.

#### examples/technical-passage/rationale.md

##### Rationale: technical passage

Sentence-level accounting of the rewrite, then the measurements, then what the rewrite got wrong.

###### Actions taken

| Source | Action | Result |
|---|---|---|
| "In the realm of modern software architecture, caching represents a pivotal mechanism that fundamentally transforms how applications manage and retrieve data." | REPLACE | "Caching keeps a copy of data somewhere faster to reach than the original." |
| "By leveraging the power of temporary storage solutions, systems can significantly enhance their overall performance metrics while simultaneously reducing the burden on primary data sources." | RESTRUCTURE, SPLIT | "A read that hits the cache skips the database entirely, so it returns faster and the database does less work." |
| "At its core, caching operates by storing frequently accessed data..." | MERGE | Folded into the opening definition, which now carries it. |
| "This approach offers several key advantages. First... Second... Third..." | RESTRUCTURE | Two effects stated once, without labels. The third advantage, scaling, was the same claim as the first two under load, so it became "Both effects compound under load." |
| "Furthermore, modern caching implementations typically incorporate sophisticated expiration policies to ensure data freshness." | REPLACE | "The hard part is deciding when a cached copy has gone stale." |
| "These policies, ranging from time-based invalidation to event-driven cache busting, play a crucial role in maintaining the delicate balance..." | SPLIT | Two sentences, one per policy type, each saying what the policy actually does. |
| "It is worth noting that the selection of an appropriate caching strategy is a nuanced decision that requires careful consideration of multiple factors, including but not limited to the nature of the data, access patterns, and the specific requirements of the application in question." | REPLACE | "Which one fits depends on how bad it is to serve a stale value, and that varies enormously between systems." |
| "In conclusion, caching remains an indispensable tool in the arsenal of modern software engineers. By thoughtfully implementing and managing caching solutions, development teams can achieve remarkable improvements in application performance, ultimately delivering a superior user experience to their end users." | REMOVE, REPLACE | Both sentences cut. Replaced with the point the passage had been circling: the decision is about tolerable staleness, not about caching. |

No technical claim was altered. Two terms did not survive as terms, and both substitutions are worth declaring, because `diagnostic.md` said to keep all three domain terms and the rewrite kept one of them as written. `latency` became `it returns faster`, which makes the same claim in the register the rest of the rewrite uses, and the source's `event-driven cache busting` became `event-driven invalidation`, which is what the mechanism is ordinarily called. `database`, `time-based expiry` and `event-driven` are intact. If either word matters for searchability, put it back; the sentences hold either way.

###### Measured before and after

```
python3 scripts/analyze_structure.py examples/technical-passage/input.md
python3 scripts/analyze_structure.py examples/technical-passage/output.md
```

| Measure | Before | After |
|---|---|---|
| Words | 241 | 173 |
| Sentences | 12 | 14 |
| Mean sentence length | 19.9 | 12.2 |
| Nominalization density | 95.4, high | 17.3, normal |
| Mechanical transitions | 4 | 0 |
| AI-associated vocabulary | 4 unique | 0 |
| Flesch-Kincaid grade | 16.4 | 6.0 |
| Gunning Fog | 20.5 | 8.4 |
| Density score | 74.3, high | 21.4, low |
| Burstiness | 0.471 | 0.415 |

The nominalization figure is the one that moved most, from 95.4 to 17.3 per 1,000 words, and it moved because the abstractions were replaced with the actions underneath them rather than because words were swapped. `the selection of an appropriate caching strategy` became `which one fits`.

Both figures are from the regex proxy in this repository and are comparable only to each other. Neither is comparable to the 14.6 per 1,000 tokens that Reinhart et al. measured with a dependency parser. See `references/style-research.md`.

###### What went wrong

**Burstiness fell, from 0.471 to 0.415.** The rewrite reads better and scores worse on this measure. Shortening the long sentences compressed the range, because burstiness is a coefficient of variation and cutting the outliers reduces it. Anyone treating burstiness as a target would reject this rewrite. It is a weak metric and this example is the proof.

**Three sentences now open with "A".** The script flags it. It is a real if minor regression, introduced by the parallel construction in the third paragraph.

**Grade level dropped from 16.4 to 6.0, which is further than intended.** The genre wants roughly grade 10 to 12. Grade 6 risks reading as condescending to the audience the passage names. This is over-correction and it is the failure mode `rules/context.md` warns about: applying the fix past the point where it helps.

**The benchmark flags this pair twice, and only one flag is fair.**

```
python3 scripts/benchmark.py --input examples/technical-passage/input.md \
                            --output examples/technical-passage/output.md
```

```
SEMANTIC PRESERVATION
  Token overlap similarity: 8.1%
  ⚠ Major meaning drift

FACTUAL PRESERVATION (NUMBERS)
  ✓ Numbers preserved

WORD COUNT
  241 → 173 (-28.2%)
  ⚠ Significant reduction (-20%+)
```

The word count warning is fair and agrees with the grade-level finding above: this rewrite cut harder than the genre needed. The similarity warning is not evidence of anything. It is 8.1% because the rewrite replaced `sophisticated expiration policies to ensure data freshness` with `deciding when a cached copy has gone stale`, which is the intervention working, and token overlap cannot tell that from meaning loss. The same measure rates `examples/already-natural/` at 65.5%, the highest in the set, on a pair where the paragraph was not touched. `benchmarks/README.md` has the full table.

###### The one addition, declared

The output contains a sentence pair not present in the source:

> A stale follower count is a cosmetic problem. A stale account balance is not.

These are illustrations of a principle the source does state, not facts about any system. They were added because the source asserted that strategy choice "requires careful consideration of multiple factors" without naming a single one, and the abstraction is unreadable without an instance.

This is a judgment call and it sits close to the line that rule 1 in `SKILL.md` draws. Under `--mode preserve` it would not have been added; the sentence would have read `Which one fits depends on how bad it is to serve a stale value.` and stopped there.

Note also what was deliberately **not** added. Time-based expiry is described as holding a copy "for a fixed window" rather than for sixty seconds. A specific interval would have been an invented technical detail, and the source does not supply one.

### examples/personal-essay/

#### examples/personal-essay/README.md

##### Personal essay

A generated personal essay about moving from Nagpur to Bangalore. 213 words about the author's own life, written at grade 15 in abstract nouns.

| File | |
|---|---|
| `examples/personal-essay/input.md` | The generated essay, 213 words |
| `examples/personal-essay/diagnostic.md` | Stage 2 diagnostic and the measured figures |
| `examples/personal-essay/output.md` | The rewrite, three slots and a flag |
| `examples/personal-essay/rationale.md` | Per-sentence accounting, two declared additions, and a rule the first draft broke |

**What this example is for.** The line the skill refuses to rewrite. The draft ends by telling the reader what the author learned: `adaptation is not merely a passive response to environmental change but an active, ongoing process of self-reinvention`. Every other flag in this repository marks a missing fact. This one marks a missing position, and inventing a position for someone and attributing it to their own life is a different order of error. The output quotes it back and says the essay can end without a moral.

The measurement lesson here is the pair of sentence-length figures. Mean length is 21.2 words before and 21.2 after, unchanged to the decimal, while burstiness goes from 0.375 to 0.600. The input's sentences run from 8 words to 31, ten of them bunched in the middle with nothing in the very short or very long band; the output runs from 5 to 53 and puts one sentence in each. Variation lives in the spread, and the average cannot see it.

Two smaller findings. The vocabulary scanner catches only two terms here, fewer than anywhere except the human paragraph in `examples/already-natural/`, because this draft is generated in academic register and the wordlist is tuned to business register: `embarked`, `journey`, `acculturation` and `unparalleled` all pass. And first-person markers fall from 14 to 12 while the essay becomes considerably more personal, which is the clearest evidence in the set that pronoun frequency is not disclosure.

`rationale.md` also records a rule the first version of this rewrite broke, and what fixing it cost on the metrics.

#### examples/personal-essay/input.md

Specimen. Fenced so that its em dashes and flagged vocabulary stay quoted rather than becoming this document's own prose.

```text
Relocating to a new city represents one of life's most transformative experiences. When I moved to Bangalore from Nagpur in 2019, I embarked on a journey that would fundamentally reshape my perspective on what it means to build a life in an unfamiliar environment.

The initial period was characterized by significant challenges. The cost of living far exceeded my expectations, and the absence of an established social network created feelings of isolation that were, at times, quite overwhelming. I found myself constantly engaging in comparative analysis between my new surroundings and the familiar comforts of my hometown, a tendency that, in retrospect, was ultimately counterproductive to my adjustment process.

However, by the time my second year commenced, a remarkable transformation had occurred. I had ceased making these detrimental comparisons and found myself embracing Bangalore as my new home. This shift in perspective, which I attribute to the gradual process of acculturation and the development of meaningful interpersonal connections, fundamentally altered my experience of urban life.

In conclusion, the process of relocating to a new city, while initially fraught with challenges, ultimately offers unparalleled opportunities for personal growth and transformation. The experience has taught me that adaptation is not merely a passive response to environmental change but an active, ongoing process of self-reinvention.
```

#### examples/personal-essay/diagnostic.md

##### Diagnostic: personal essay

Produced at Stage 2 of the procedure in `SKILL.md`. This is the example where the author's own experience is the missing content.

```
NOT AI DIAGNOSTIC
Genre:    Personal essay, inferred from first person and the retrospective frame.
Register: 2 of 5 expected, 5 of 5 delivered. A person describing their own move
          in the vocabulary of a sociology paper.

Working already:
  "When I moved to Bangalore from Nagpur in 2019"
  Two places and a year. The only clause in 213 words that could not have been
  written by someone who has never moved anywhere. Everything the essay needs
  is downstream of this clause and absent from the draft.

Patterns found:
  universalising opening  "Relocating to a new city represents one of life's most
                          transformative experiences." Opens on everyone rather
                          than on the writer.
  copula avoidance        "represents one of life's most transformative
                          experiences" for "is"
  journey metaphor        "I embarked on a journey that would fundamentally
                          reshape my perspective"
  agentless nominal       "The initial period was characterized by significant
                          challenges." Which challenges, and characterised by whom.
  nominalised feeling     "the absence of an established social network created
                          feelings of isolation"
  noun phrase for verb    "constantly engaging in comparative analysis between"
                          for "comparing"
  event with no agent     "a remarkable transformation had occurred"
  explanation that is not "which I attribute to the gradual process of
                          acculturation and the development of meaningful
                          interpersonal connections"
  mechanical transition   "However, by the time my second year commenced"
  mechanical transition   "In conclusion" in a four-paragraph personal essay
  negative parallelism    "not merely a passive response to environmental change
                          but an active, ongoing process of self-reinvention"
  restated opening        Paragraph 4 says what paragraph 1 said. The phrase
                          "relocating to a new city" appears in both.

Vocabulary in context:
  "transformative" 1x     Problem. Also "transformation" twice more.
  "meaningful" 1x         Problem. "meaningful interpersonal connections" is
                          three words for "friends".
  "embarked", "journey"   Problem, and the script does not flag either.
  "fundamentally" 2x      Problem. Both instances are intensifiers on claims
                          that carry no detail to intensify.
  "ultimately" 2x         Problem. Same.
  "unparalleled"          Problem. Unparalleled against what.
  "acculturation"         Problem. Correct word, wrong essay.
  "Bangalore", "Nagpur"   Fine. The two most useful words in the draft.
  "2019"                  Fine. Keep.
  "rent", "cost of living" Fine, and the only concrete nouns present.

Missing, and this is the whole diagnosis:
  no amount for the rent, no figure for what it exceeded
  no named person, no conversation, no place in either city
  no month or event for the shift in year two
  no sensory detail of any kind in 213 words about moving between two cities

Intervention: heavy
```

###### Measured

```
python3 scripts/analyze_structure.py examples/personal-essay/input.md
python3 scripts/metrics.py examples/personal-essay/input.md
python3 scripts/repetition.py examples/personal-essay/input.md
```

| Measure | Value |
|---|---|
| Words / sentences / paragraphs | 213 / 10 / 4 |
| Mean sentence length | 21.2 words |
| Burstiness | 0.375 |
| Sentence length spread | 0 very short, 3 short, 3 medium, 4 long, 0 very long |
| Participial clause openers | 0 of 10, 0%, ✓ |
| Nominalization density | 84.5 per 1,000 words, ⚠ high for this proxy |
| Mechanical transitions | 1, `in conclusion`, ⚠ |
| Repeated sentence openers | `the` opens 3 sentences, ⚠ |
| Repeated phrases | `relocating to a new city` 2x, and five of its substrings |
| Lexical diversity | 86% content-word TTR, ✓ high |
| AI-associated vocabulary | 2 unique terms |
| Flesch-Kincaid grade | 15.0 |
| Gunning Fog | 20.0, very difficult |
| Flesch Reading Ease | 25.5 out of 100 |
| Density score | 72.3, high, characteristic of formal academic prose |
| Hedges / boosters | 0 / 0, `absent` |
| First-person markers | 14, 66.0 per 1,000 words |

###### Two figures that mislead badly here

**Two flagged vocabulary terms in 213 words.** The lowest count in this set apart from the human paragraph in `examples/already-natural/`, which scores zero. The LinkedIn post, generated by the same class of system, collects fourteen. Nothing follows from that ordering. The wordlist is tuned to business and technology register, and this draft is generated in the register of an academic monograph, so it slips through with `transformative` and `meaningful` while `embarked`, `journey`, `acculturation`, `unparalleled`, `fundamentally` twice and `ultimately` twice all go uncounted.

Word counting cannot carry a diagnosis. The tells here are nominalization at 84.5, density at 72.3 and a grade level of 15.0 on a first-person essay about renting a flat.

**Fourteen first-person markers, 66.0 per 1,000 words, the highest rate in the set.** The draft says `I` constantly and reveals nothing. `I found myself constantly engaging in comparative analysis` uses two first-person constructions to report an activity that any person in any city might perform. First-person density measures grammar, not disclosure, and a rewrite that raised it would move away from the fix rather than toward it.

###### What the repeated phrase reveals

`relocating to a new city`, twice, in a 213-word essay. Once to open and once to conclude. Strip both sentences of their modifiers and they make the same claim: moving cities changes a person. Four paragraphs, and the last one returns to the first without having added anything a reader could not have supplied themselves.

This is why the intervention is heavy despite a clean participial score and no repeated openings beyond `the`. The structure is a loop.

###### What bounds the rewrite

The draft has one fact, the move itself, and one near-fact, that rent exceeded expectations. Everything else is a category: challenges, isolation, comparison, transformation, growth. Rule 1 in `SKILL.md` means these cannot be filled in.

Two things separate this from `examples/gen-ai-article/`, where the same emptiness led to a two-sentence output. First, the events are real and the author holds every missing detail, as in `examples/linkedin-post/`. Second, and specific to this genre, the draft's closing sentence states a conclusion about what the author learned from their own life. That is not a stylistic problem. An essay that tells a reader the author reinvented themselves, when the author never said so, has misrepresented them. It gets a flag rather than a rewrite.

#### examples/personal-essay/output.md

I moved to Bangalore from Nagpur in 2019. The first year was hard in ways I had not planned for.

Rent was the first shock. I had expected it to be higher than home. [How much higher, and what you cut to cover it.] The bigger problem was that I did not know anyone. In Nagpur there were people who had known me long enough that I never had to explain myself. Here I was starting from nothing, and I kept measuring the new place against the old one: the food, the way the office ran, what a weekend was supposed to look like.

Somewhere in the second year I stopped doing that. [When you noticed, and what you were doing when you noticed it.] It was not a decision I made. At some point I registered that I had not compared anything in a while.

[Why you think it stopped. The draft attributes it to "the gradual process of acculturation and the development of meaningful interpersonal connections", which explains nothing and is almost certainly not how you would put it. What actually changed?]

[FLAG: the draft closes by concluding that the experience taught you "adaptation is not merely a passive response to environmental change but an active, ongoing process of self-reinvention." That is the draft's conclusion, not yours, and it is the one line here that changes what the essay claims. Replace it with what you actually think, or cut it. The essay can end on the previous paragraph without supplying a moral.]

#### examples/personal-essay/rationale.md

##### Rationale: personal essay

The events are real and almost none of them are in the draft. The rewrite recovers what is there, opens slots for what is not, and refuses to carry the conclusion.

###### Actions taken

| Source | Action | Result |
|---|---|---|
| "Relocating to a new city represents one of life's most transformative experiences." | REMOVE | Opens on everyone. An essay about the author's move does not need a claim about relocation in general, and this sentence is restated as the conclusion, so cutting it also breaks the loop. |
| "When I moved to Bangalore from Nagpur in 2019, I embarked on a journey that would fundamentally reshape my perspective on what it means to build a life in an unfamiliar environment." | SPLIT, REPLACE | "I moved to Bangalore from Nagpur in 2019. The first year was hard in ways I had not planned for." The clause with the facts survives intact. The journey metaphor and the promise of reshaped perspective are cut. |
| "The initial period was characterized by significant challenges." | REMOVE | Announces that challenges follow, immediately before the challenges. |
| "The cost of living far exceeded my expectations" | RESTRUCTURE, FLAG | "Rent was the first shock. I had expected it to be higher than home. [How much higher, and what you cut to cover it.]" Cost of living becomes rent, which is what the author means and can quantify. |
| "the absence of an established social network created feelings of isolation that were, at times, quite overwhelming" | REPLACE | "The bigger problem was that I did not know anyone. In Nagpur there were people who had known me long enough that I never had to explain myself." The second sentence is the one addition in this rewrite and it is declared below. |
| "I found myself constantly engaging in comparative analysis between my new surroundings and the familiar comforts of my hometown, a tendency that, in retrospect, was ultimately counterproductive to my adjustment process." | RESTRUCTURE | "Here I was starting from nothing, and I kept measuring the new place against the old one: the food, the way the office ran, what a weekend was supposed to look like." Comparative analysis becomes measuring. The three items are inferred from `familiar comforts`, which is the vaguest phrase in the draft, and they are the sort of thing the author should replace with what they actually compared. |
| "However, by the time my second year commenced, a remarkable transformation had occurred. I had ceased making these detrimental comparisons and found myself embracing Bangalore as my new home." | RESTRUCTURE, FLAG | "Somewhere in the second year I stopped doing that. [When you noticed, and what you were doing when you noticed it.] It was not a decision I made. At some point I registered that I had not compared anything in a while." The transformation gets an agent. |
| "This shift in perspective, which I attribute to the gradual process of acculturation and the development of meaningful interpersonal connections, fundamentally altered my experience of urban life." | FLAG | Becomes a slot quoting the phrase back: acculturation and meaningful interpersonal connections explain nothing, and no reader learns anything from them. The author knows who they met and when. |
| "In conclusion, the process of relocating to a new city, while initially fraught with challenges, ultimately offers unparalleled opportunities for personal growth and transformation." | REMOVE | Paragraph 1 in different words, with `In conclusion` attached to a four-paragraph essay. |
| "The experience has taught me that adaptation is not merely a passive response to environmental change but an active, ongoing process of self-reinvention." | FLAG | Not rewritten. See below. |

###### The line that gets a flag instead of a rewrite

> The experience has taught me that adaptation is not merely a passive response to environmental change but an active, ongoing process of self-reinvention.

Three separate problems converge here. It is negative parallelism, `not merely X but Y`, which `references/wikipedia-signs.md` lists among the most reliable signs. It is abstract to the point of vacancy. And it is a claim about what the author personally learned from their own life.

The third is the one that matters. A rewrite can make a vague sentence specific when the source supplies the specifics. Nothing in this draft supplies what the author concluded, so any rewrite here invents a belief and attributes it to them. Every other flag in this file marks a missing fact. This one marks a missing position, which is worse, because an essay is largely a position.

So it is quoted back with the reason, and the note says the essay can end on the previous paragraph without supplying a moral. Many good essays do.

###### Two declared additions

**"In Nagpur there were people who had known me long enough that I never had to explain myself."**

The draft says `the absence of an established social network created feelings of isolation`. The rewrite says what absence of a social network consists of. Nothing in the source states that anyone in Nagpur had known the author a long time, or that explaining themselves was the friction, so this is inference and it is flagged as an addition rather than presented as a recovery.

It is a defensible inference and it is still an inference. An author who reads it and thinks `that is not what I missed` should cut it.

**"the food, the way the office ran, what a weekend was supposed to look like"**

Three items standing in for `the familiar comforts of my hometown`, the vaguest phrase in the draft. They are the kind of thing people compare between cities, which is precisely the problem: they are plausible rather than true. They belong in the same category as the bracketed slots and should be replaced with what the author actually caught themselves comparing.

Stage 4 of `SKILL.md` requires additions to be declared, and this is the declaration for both. Two inferred passages in a 255-word rewrite is more than this skill should be comfortable with, and the honest reading is that a draft this empty pushes any rewrite toward invention. That pressure is the reason rule 1 is stated as an absolute rather than a preference.

###### Measured before and after

```
python3 scripts/analyze_structure.py examples/personal-essay/input.md
python3 scripts/analyze_structure.py examples/personal-essay/output.md
python3 scripts/metrics.py examples/personal-essay/output.md
python3 scripts/repetition.py examples/personal-essay/output.md
```

| Measure | Before | After |
|---|---|---|
| Words | 213 | 255 |
| Sentences | 10 | 12 |
| Paragraphs | 4 | 5 |
| Mean sentence length | 21.2 | 21.2 |
| Burstiness | 0.375 | 0.600, ✓ good variation |
| Length spread | 0 / 3 / 3 / 4 / 0 | 1 / 4 / 2 / 4 / 1 |
| Nominalization density | 84.5, ⚠ high | 23.5, ✓ normal |
| Mechanical transitions | 1 | 0 |
| Repeated `the` openers | 3, ⚠ | 3, ⚠ |
| Repeated phrases | `relocating to a new city` 2x | `when you noticed` 2x |
| Paragraph shapes | 4 unique | 5 unique |
| Lexical diversity | 86% | 86% |
| AI-associated vocabulary | 2 unique | 1 unique |
| Flesch-Kincaid grade | 15.0 | 9.2 |
| Gunning Fog | 20.0, very difficult | 12.1, standard |
| Flesch Reading Ease | 25.5 | 66.8 |
| Density score | 72.3, high | 30.6, moderate |
| Hedges / boosters | 0 / 0, `absent` | 0 / 1, `too sparse to judge` |
| First-person | 14, 66.0 per 1,000 | 12, 47.2 per 1,000 |
| Reader address | 0 | 8 |

**Mean sentence length is identical, 21.2 both times, and burstiness went from 0.375 to 0.600.** The most informative pair of figures in this example. The average did not move at all; the distribution did. The input's ten sentences run from 8 words to 31, none of them in the very short band or the very long one. The output puts one sentence in each: 5 words at the shortest, 53 at the longest. Length variation is a property of the spread, and any summary statistic that reports the centre will miss it entirely.

**Nominalization 84.5 to 23.5, and this is where the register actually changed.** Eighteen suffix matches in 213 words: `experiences`, `environment`, `expectations`, `absence`, `isolation`, `adjustment`, `transformation` twice, `acculturation`, `development`, `connections`, `experience` twice, `opportunities`, `adaptation`, `reinvention`, and `city` twice, which the proxy counts for ending in `ity` and not for being abstract. An essay about a person's own life, written almost entirely in abstract nouns. What replaced them: `rent was the first shock`, `I did not know anyone`, `I kept measuring`, `I stopped doing that`.

The membership is worth looking at rather than trusting, because the reading finds more abstraction here than the proxy does. `Relocating`, `perspective`, `challenges`, `analysis`, `comforts` and `tendency` are all doing the same work in this draft and none of them ends in a suffix the regex knows. The figure points the right way; the list of words behind it is not the list a reader would write.

**Grade level 15.0 to 9.2 and density 72.3 to 30.6.** The input was labelled `characteristic of formal academic prose`. It is an essay about missing your friends.

**First-person fell, 14 to 12, and the essay is more personal.** The draft used `I found myself` twice as a way of reporting activity without reporting content. Personal writing is not produced by pronoun frequency, and a rewrite that chased this number upward would have moved away from the fix.

###### What went wrong, and what is still wrong

**The first version of this rewrite broke the skill's own rule 2.** Where the output now reads `I kept measuring the new place against the old one: the food, the way the office ran, what a weekend was supposed to look like`, the earlier version ran the three items as separate fragments: `The food. The way the office ran. What a weekend was supposed to look like.` It read well. It was also three fragments in parallel, a rule-of-three shape built out of exactly the decorative fragmenting that rule 2 prohibits, and it pushed the repeated-`the` opener count from 3 to 5, making the output worse than the input on that measure. Burstiness fell from 0.742 to 0.600 when it was fixed, which is the correct direction for a metric that was rewarding fragments.

Stage 5 question 5 is what caught it, and the fragment version is recorded here rather than quietly discarded.

**`the` still opens 3 sentences and the warning still fires.** Two of the three are in the deliverable, `The first year was hard` and `The bigger problem was`, and both are load-bearing. The third is in a bracketed note. The warning is correct that the pattern exists and wrong that it needs fixing, and forcing a different opener onto either sentence would cost more than the repetition does.

**Five of the output's readings are artifacts of the bracket text.** Reader address 8, questions 1, the stance verdict moving off `absent` on the strength of one `certainly`, the repeated phrase `when you noticed`, and the surviving `meaningful` all come from editorial notes to the author rather than from the essay. `examples/gen-ai-article/` documents the same effect; this file quantifies it. The three slots and the flag hold 132 of the output's 255 words, so 51.8% of the measurable surface is instruction rather than deliverable, and no script can tell the difference.

The `certainly` sits in `almost certainly not how you would put it`, inside a note, and the essay proper carries no stance marker at all. One marker is under the three-marker floor, so the verdict is `too sparse to judge` rather than `over-assertive`. A single adverb in an editorial aside cannot support a claim that the essay is over-confident, and the earlier version of the check made exactly that claim.

Read what you are measuring. That is the recurring lesson of the whole example set, and it applies as much to the rewrite as to the draft.

###### What the finished essay needs

Four things, all of which the author has and none of which a tool can supply: the rent figure and what it displaced, when in year two they noticed and what they were doing, what they think actually changed, and either a position worth stating at the end or the confidence to stop without one.

With those, this is a good essay in about 300 words. Without them it is a form, and the form is more honest than the polished version.

### examples/already-natural/

#### examples/already-natural/README.md

##### Already natural

Human writing that needs no changes. A paragraph from a developer's post about a production incident.

| File | |
|---|---|
| `examples/already-natural/input.md` | The source paragraph, 66 words, human-written |
| `examples/already-natural/diagnostic.md` | Stage 2 diagnostic, and the two warnings the scripts raise on it |
| `examples/already-natural/output.md` | The input reproduced verbatim, plus a note on why nothing changed |
| `examples/already-natural/rationale.md` | Why nothing changed, and both ways an agent could get this wrong |

**What this example is for.** The scripts flag human writing. Run them and `analyze_structure.py` reports low burstiness at 0.200 and elevated nominalization at 45.5 per 1,000 words on a paragraph that a person wrote about their own week.

The burstiness comparison across this example set is worth the whole file: this human paragraph scores 0.200, the machine-written academic abstract scores 0.201, and the machine-written LinkedIn post scores 0.799 with a ✓ Good length variation. The metric does not separate the two populations here, and where it discriminates it points the wrong way.

`rationale.md` then shows the two failure modes in full: over-humanization, which buries the specifics in performed enthusiasm, and metric-chasing, which fabricates a fact to raise burstiness and removes the term `race condition` to lower nominalization. Both improve a number. Both damage the writing.

#### examples/already-natural/input.md

Specimen. Fenced so that its em dashes and flagged vocabulary stay quoted rather than becoming this document's own prose.

```text
I spent three days last month hunting a bug that only showed up under load. The issue was in how we handled connection timeouts — specifically, a race condition between the health check and the reconnection logic. I found it by adding more aggressive logging and watching the logs during a controlled load test. Not fun, but at least I know what to look for next time.
```

#### examples/already-natural/diagnostic.md

##### Diagnostic: already natural

Produced at Stage 2 of the procedure in `SKILL.md`. The source is human writing, a paragraph from a developer's post about a production incident.

```
NOT AI DIAGNOSTIC
Genre:    Developer blog, personal incident note. Inferred.
Register: 2 of 5. Peers who have debugged something similar.

Working already:
  "Not fun, but at least I know what to look for next time."
  A fragment used deliberately, an honest assessment, and an ending that draws a
  conclusion from the experience rather than summarising the paragraph. Nothing in
  this sentence could be swapped into a post on another topic.

Patterns found:
  none

Vocabulary in context:
  none flagged

Intervention: none
```

Stop here. `SKILL.md` Stage 2: where the text is already good, say so and stop. Finding nothing is a valid result.

###### Measured

```
python3 scripts/analyze_structure.py examples/already-natural/input.md
python3 scripts/metrics.py examples/already-natural/input.md
```

| Measure | Value | Script verdict |
|---|---|---|
| Words / sentences | 66 / 4 | |
| Burstiness | 0.200 | ⚠ Low burstiness: sentence lengths are very uniform |
| Nominalization density | 45.5 per 1,000 words | ⚠ elevated for this proxy |
| Participial clause openers | 0 of 4 | ✓ |
| Mechanical transitions | 0 | ✓ |
| AI-associated vocabulary | 0 | ✓ |
| Flesch-Kincaid grade | 7.3 | |
| Density score | 47.0 | moderate |
| First-person | 4, at 59.7 per 1,000 words | |

###### The scripts raise two warnings on human writing

This is the point of the example, and it is not a hypothetical. Run the commands above and the toolkit flags genuinely human prose twice.

**Low burstiness, 0.200.** Four sentences of 15, 22, 17 and 13 words. Little variation, so the coefficient of variation is small. The paragraph reads fine because a reader responds to the fragment that opens the last sentence and to the specificity, not to length variance.

The comparison that matters: the machine-written academic abstract in `examples/academic-abstract/` measures **0.201**. Effectively identical. And the machine-written LinkedIn post in `examples/linkedin-post/` measures **0.799** and earns a ✓ Good length variation. On this set of six, burstiness does not separate human from machine at all, and where it discriminates it points the wrong way.

**Elevated nominalization, 45.5 per 1,000 words.** Three suffix matches in 66 words: `connection`, `condition` and `reconnection`. These are the correct technical words for what happened. There is no rewrite that lowers this number without making the sentence worse.

###### What follows

Two of nine measures fire on a text that needs no changes. That is why `SKILL.md` forbids reporting a score and forbids stating a conclusion about authorship: the numbers are inputs to a reading, not a verdict.

It is also why Stage 5 question 2 exists, "Where did I over-edit a sentence that was already working?" An agent that treats a ⚠ as an instruction will rewrite this paragraph, and every available edit makes it worse. `rationale.md` shows what that looks like.

###### On the em dash in the source

The input contains one:

```
The issue was in how we handled connection timeouts — specifically, a race condition
between the health check and the reconnection logic.
```

A human wrote it. It is used correctly, as a single break introducing a clarification, and removing it would be an edit made to satisfy a detector rather than a reader. `references/wikipedia-signs.md` covers why em dash frequency has become a weak signal and why the paired parenthetical form is the part still worth noticing. This is not that form.

#### examples/already-natural/output.md

The correct output for this input is the input, unchanged. Reproduced here so that the before and after measurements in `rationale.md` can be run against two real files.

```
I spent three days last month hunting a bug that only showed up under load. The issue was in how we handled connection timeouts — specifically, a race condition between the health check and the reconnection logic. I found it by adding more aggressive logging and watching the logs during a controlled load test. Not fun, but at least I know what to look for next time.
```

The fenced block above is byte-identical to `input.md`. Intervention rate 0%.

#### examples/already-natural/rationale.md

##### Rationale: already natural

Intervention rate 0%. The delivered text is the input, unchanged. This file explains why, and shows what the two available failure modes would have produced.

###### Why nothing changed

Four properties, each of which is difficult for a model to produce and easy for a person writing about their own week to produce without trying.

**Specificity that costs something to know.** `three days`, `last month`, `only showed up under load`, `a race condition between the health check and the reconnection logic`, `a controlled load test`. Every one of these is checkable and none is decorative. The technical cause is named precisely enough that another engineer could look for the same bug.

**The author is in the sentences.** `I spent`, `I found it by`. Not as a stylistic flourish; the first person is carrying the information about who did what.

**A fragment placed for weight.** `Not fun` opens the closing sentence after three sentences of 15, 22 and 17 words. It works because of what precedes it, and it is the kind of thing a writer does on instinct. Note that no script sees it: the segmenter counts the closing sentence at 13 words, comma and all, so the two-word beat that makes the paragraph land is invisible to every measure in this repository.

**An ending that is a conclusion rather than a summary.** `at least I know what to look for next time` adds something the paragraph had not yet said. Compare the closing sentence of `examples/technical-passage/input.md`, which restates the paragraph and then asserts that the topic is important.

###### Failure mode one: over-humanization

What a tool that must produce a change produces:

> So, I spent a solid three days last month tracking down this gnarly bug that only popped up under heavy load, super annoying! Turns out it was a classic race condition lurking in how we handled connection timeouts between the health check and reconnect logic. I ended up cranking up the logging and ran a controlled load test, and boom, found it! Wasn't exactly fun, but hey, at least now I know what to watch for. 😅

The specifics survive, buried. What is lost is the author's actual register: measured, slightly dry, unbothered. `Not fun, but at least I know what to look for next time` has been replaced with performed enthusiasm that the original writer plainly does not feel.

This is the standard humanizer output shape. `SKILL.md` rule 2 forbids it directly: never degrade writing to look human.

###### Failure mode two: chasing the warnings

The subtler failure, and the more likely one for an agent following the script output literally. Two measures fired, so an agent could try to satisfy both.

To raise burstiness from 0.200, split a sentence and pad another:

> I spent three days last month hunting a bug. It only showed up under load, which made it miserable to reproduce, and I burned most of the first day just getting a reliable repro at all. The issue was in how we handled connection timeouts, specifically a race condition between the health check and the reconnection logic. I found it by adding more aggressive logging and watching the logs during a controlled load test. Not fun, but at least I know what to look for next time.

Burstiness rises. The paragraph is now 20% longer, and the added clause invents a fact: the source never says the first day went to reproduction. Rule 1 violated to satisfy a metric.

To lower nominalization from 45.5, the proxy's three matches are `connection`, `condition` and `reconnection`. Two of them name the bug, so removing those two gives:

> The issue was in how we handled connection timeouts, specifically two parts of the system racing each other when one tried to reconnect while the other was checking health.

Longer, vaguer, and it no longer names the bug class. `Race condition` is the term an engineer searches for.

Both edits improve a number and damage the writing. That is the whole argument for reporting patterns to a person instead of optimising a score, and it is why `compute_quality_score` was removed from `scripts/metrics.py`.

###### Measured

The delivered text is the same on both sides, so every figure below is `input.md` measured once:

| Measure | Value |
|---|---|
| Words | 66 |
| Burstiness | 0.200 |
| Nominalization density | 45.5 |
| Mechanical transitions | 0 |
| AI vocabulary | 0 |
| Flesch-Kincaid grade | 7.3 |

Running the scripts on `output.md` instead gives different figures, and the difference is worth understanding rather than tidying away. That file wraps the paragraph in a fence and adds two lines of explanation, so it measures 107 words, burstiness 0.545 and nominalization 46.7. `benchmark.py`, which compares the two files, therefore reports a 62.1% expansion and a burstiness improvement of 0.345 on a pair where not one word of the paragraph changed. Its nominalization delta reads `unchanged (+1.2/1k words)`: the wrapper adds `measurements` and `Intervention` to the paragraph's three suffix matches, and the words it adds dilute the rate by almost the same amount. This is the cleanest case in the repository of a measure describing a file rather than a deliverable, and `benchmarks/README.md` uses it as such.

The correct output was available in the diagnostic and required no rewrite at all.

## Appendix D. scripts/measure.py

The measurement pass, as text. Write it to a file and run `python3 measure.py
FILE`. Python 3.10, standard library only.

It reports the same numbers as `analyze_structure.py`, `metrics.py` and
`repetition.py` in the multi-file repository, checked file by file by
`scripts/verify_measure.py`, so the before-and-after tables in Appendix C
reproduce against it.

Two things to hold in mind before quoting any figure it prints. Its
nominalization and participial measures are regex proxies, so they are
comparable to another run of this script and never to the tagged per-1,000-token
rates in Appendix B. And it measures a file, not a deliverable: a flag block or a
bracketed slot is counted as prose, which is why the `gen-ai-article` output
still reports flagged vocabulary it does not use.

```python
#!/usr/bin/env python3
"""
not-ai: measure.py
One-file measurement pass. Combines analyze_structure.py, metrics.py and
repetition.py into a single stdlib-only script with no sibling imports.

This file exists so the skill can work as a single SKILL.md. The build script
scripts/build_single_file.py embeds it verbatim in a fenced block, and an agent
loading the combined skill writes it to a temp path and runs it.

Every regex, threshold and formula here is copied from the three scripts it
replaces, not reimplemented. That is deliberate: the figures quoted in
examples/*/diagnostic.md and examples/*/rationale.md come from those scripts,
and a condensed version that measured slightly differently would silently
invalidate every table in the repository. scripts/verify_measure.py checks the
two agree on every shared figure.

Usage:
    python measure.py FILE
    python measure.py --stdin
    python measure.py FILE --json

Read before quoting any number:
  * Nominalization here is a regex over suffixes, with no part-of-speech
    information. It counts "nation" and "moment". On the five model-generated
    inputs in examples/ it averages 80.0 per 1,000 words against the tagged
    14.6, about 5.5 times, so compare it only against another run of this
    script, never against the 14.6 per 1,000 tokens in the research.
  * The participial detector is anchored to the first word of the sentence, so
    "By leveraging the power of..." is not counted. A 0% result means "none of
    the anchored forms", not "none".
  * Burstiness is a coefficient of variation. Its verdicts are wrong often
    enough that nothing in the skill acts on them. They are printed as evidence,
    not as guidance.
"""

import argparse
import json
import re
import sys
from collections import Counter
from pathlib import Path

# ─── Primitives (from _shared.py) ────────────────────────────────────────────

NOMINALIZATION_SUFFIXES = (
    "tion", "tions", "ment", "ments", "ness", "nesses",
    "ity", "ities", "ance", "ances", "ence", "ences",
)
NOMINALIZATION_PATTERN = re.compile(
    r"\b\w+(" + "|".join(NOMINALIZATION_SUFFIXES) + r")\b", re.IGNORECASE)
HEURISTIC_NOMINALIZATION_BANDS = {"high": 50.0, "elevated": 35.0}
WORD_PATTERN = re.compile(r"\b[a-zA-Z]+\b")
SENTENCE_SPLIT_PATTERN = re.compile(r'(?<=[.!?])\s+(?=[A-Z"\'])')


def tokenize_words(text):
    """Canonical denominator for every per-1,000-words rate here."""
    return WORD_PATTERN.findall(text)


def get_sentences(text):
    text = re.sub(r"\s+", " ", text.strip())
    return [s.strip() for s in SENTENCE_SPLIT_PATTERN.split(text)
            if s.strip() and len(s.split()) >= 2]


def get_paragraphs(text):
    return [p.strip() for p in re.split(r"\n\s*\n", text.strip()) if p.strip()]


def nominalization_stats(text, words=None):
    if words is None:
        words = tokenize_words(text)
    total = len(words)
    count = len(NOMINALIZATION_PATTERN.findall(text))
    rate = (count / total * 1000) if total else 0.0
    if rate > HEURISTIC_NOMINALIZATION_BANDS["high"]:
        assessment = "high for this proxy"
    elif rate > HEURISTIC_NOMINALIZATION_BANDS["elevated"]:
        assessment = "elevated for this proxy"
    else:
        assessment = "normal for this proxy"
    return {"nominalization_count": count, "total_words": total,
            "rate_per_1000_words": round(rate, 1), "assessment": assessment}


STOPWORDS = {
    'the', 'a', 'an', 'is', 'are', 'was', 'were', 'be', 'been', 'being',
    'have', 'has', 'had', 'do', 'does', 'did', 'will', 'would', 'could',
    'should', 'may', 'might', 'shall', 'can', 'to', 'of', 'in', 'for',
    'on', 'with', 'at', 'by', 'from', 'up', 'about', 'into', 'through',
    'and', 'or', 'but', 'not', 'as', 'so', 'if', 'it', 'its', 'this',
    'that', 'these', 'those', 'i', 'you', 'he', 'she', 'we', 'they',
    'my', 'your', 'his', 'her', 'our', 'their', 'me', 'him', 'us', 'them',
    'what', 'which', 'who', 'whom', 'when', 'where', 'why', 'how',
    'all', 'both', 'each', 'few', 'more', 'most', 'other', 'some', 'such',
    'than', 'too', 'very', 's', 't', 'just', 'don', 'now',
}

# ─── Structure (from analyze_structure.py) ───────────────────────────────────


def sentence_lengths(sentences):
    if not sentences:
        return {"count": 0, "mean": 0, "median": 0, "std": 0, "min": 0,
                "max": 0, "burstiness": 0, "distribution": {}}
    lengths = [len(s.split()) for s in sentences]
    n = len(lengths)
    mean = sum(lengths) / n
    srt = sorted(lengths)
    median = srt[n // 2] if n % 2 else (srt[n // 2 - 1] + srt[n // 2]) / 2
    std = (sum((x - mean) ** 2 for x in lengths) / n) ** 0.5
    return {
        "count": n, "mean": round(mean, 1), "median": round(median, 1),
        "std": round(std, 1), "min": min(lengths), "max": max(lengths),
        "burstiness": round(std / mean if mean else 0, 3),
        "distribution": {
            "very_short_under_8": sum(1 for l in lengths if l < 8),
            "short_8_to_15": sum(1 for l in lengths if 8 <= l < 16),
            "medium_16_to_25": sum(1 for l in lengths if 16 <= l < 26),
            "long_26_to_35": sum(1 for l in lengths if 26 <= l < 36),
            "very_long_over_35": sum(1 for l in lengths if l >= 36),
        },
    }


def paragraph_lengths(paragraphs):
    if not paragraphs:
        return {}
    counts = [len(get_sentences(p)) for p in paragraphs]
    n = len(counts)
    return {
        "count": n,
        "mean_sentences": round(sum(counts) / n if n else 0, 1),
        "single_sentence_paragraphs": sum(1 for c in counts if c == 1),
        "distribution": {
            "1_sentence": sum(1 for c in counts if c == 1),
            "2_3_sentences": sum(1 for c in counts if 2 <= c <= 3),
            "4_5_sentences": sum(1 for c in counts if 4 <= c <= 5),
            "6_plus_sentences": sum(1 for c in counts if c >= 6),
        },
    }


AI_OPENERS = ["furthermore", "moreover", "additionally", "however", "nevertheless",
              "therefore", "consequently", "in", "building", "leveraging",
              "utilizing", "by", "through", "this", "these", "such"]


def opening_word_analysis(sentences):
    if not sentences:
        return {}
    openings = [s.split()[0].lower().rstrip('.,!?') for s in sentences if s.split()]
    freq = {}
    for w in openings:
        freq[w] = freq.get(w, 0) + 1
    consecutive, max_consecutive, prev = 0, 0, None
    for o in openings:
        consecutive = consecutive + 1 if o == prev else 1
        if o == prev:
            max_consecutive = max(max_consecutive, consecutive)
        prev = o
    return {
        "top_5_openers": sorted(freq.items(), key=lambda x: -x[1])[:5],
        "repeated_openers_3plus": {w: c for w, c in freq.items() if c >= 3},
        "ai_associated_opener_hits": {w: c for w, c in freq.items()
                                      if w in AI_OPENERS and c >= 2},
        "the_opener_count": freq.get("the", 0),
        "this_opener_count": freq.get("this", 0),
        "max_consecutive_same_opener": max_consecutive,
    }


PARTICIPIAL_OPENERS = re.compile(
    r'^\s*(Building|Leveraging|Utilizing|Combining|Considering|Recognizing|'
    r'Acknowledging|Addressing|Analyzing|Examining|Exploring|Implementing|'
    r'Integrating|Emphasizing|Highlighting|Enabling|Supporting|Providing|'
    r'Drawing|Creating|Developing|Working|Moving|Looking|Going|Taking|'
    r'Making|Having|Being|Using|Doing|Getting|Seeing|Knowing|Finding|'
    r'Understanding|Establishing|Ensuring|Focusing|Achieving|Delivering|'
    r'Bringing|Offering|Presenting|Demonstrating)\b', re.IGNORECASE)


def participial_rate(sentences):
    count = sum(1 for s in sentences if PARTICIPIAL_OPENERS.match(s))
    rate = count / len(sentences) if sentences else 0
    return {
        "participial_opener_count": count,
        "participial_opener_rate": round(rate, 3),
        "sentences_analyzed": len(sentences),
        "assessment": ("high for this proxy" if rate > 0.15 else
                       "elevated for this proxy" if rate > 0.08 else
                       "normal for this proxy"),
        "caveat": ("Anchored match only. Participles after an introductory "
                   "preposition, for example 'By leveraging', are not counted."),
    }


MECHANICAL_TRANSITIONS = {
    "furthermore": r'\bfurthermore\b', "moreover": r'\bmoreover\b',
    "additionally": r'\badditionally\b', "in conclusion": r'\bin conclusion\b',
    "in summary": r'\bin summary\b', "to summarize": r'\bto summarize\b',
    "it is worth noting": r'\bit is worth noting\b',
    "it is important to": r'\bit is important to\b',
    "it should be noted": r'\bit should be noted\b',
    "with that being said": r'\bwith that being said\b',
    "having said that": r'\bhaving said that\b',
    "at the end of the day": r'\bat the end of the day\b',
    "last but not least": r'\blast but not least\b',
    "in the realm of": r'\bin the realm of\b',
    "when it comes to": r'\bwhen it comes to\b',
    "in today's world": r"\bin today'?s world\b",
    "in today's fast-paced": r"\bin today'?s fast.paced\b",
    "in the ever-evolving": r'\bin the ever.evolving\b',
}


def transition_density(text, sentences):
    low = text.lower()
    hits = {}
    for phrase, pat in MECHANICAL_TRANSITIONS.items():
        c = len(re.findall(pat, low))
        if c:
            hits[phrase] = c
    total = sum(hits.values())
    rate = (total / len(sentences)) if sentences else 0
    return {"mechanical_transition_hits": hits,
            "total_mechanical_transitions": total,
            "rate_per_sentence": round(rate, 3),
            "assessment": ("high for this proxy" if rate > 0.2 else
                           "elevated" if rate > 0.1 else "normal")}


AI_VOCAB = [
    "camaraderie", "tapestry", "palpable", "intricate", "underscore",
    "unspoken", "amidst", "solace", "fleeting", "vibrant",
    "cacophony", "grapple", "ignite", "unravel",
    "whirlwind",
    "delve", "delving", "delved",
    "leverage", "leveraging", "leveraged",
    "utilize", "utilizing", "utilized", "utilization",
    "facilitate", "facilitating", "facilitated", "facilitation",
    "comprehensive", "robust", "seamless", "streamline", "streamlined",
    "cutting-edge", "state-of-the-art", "groundbreaking", "revolutionary",
    "transformative", "paradigm shift", "paradigm-shifting",
    "crucial", "pivotal", "vital", "paramount",
    "foster", "fostering", "fostered",
    "underscoring", "underscored",
    "meticulous", "meticulously", "nuanced", "nuance",
    "multifaceted", "myriad", "evolving landscape", "ever-evolving",
    "rapidly evolving", "empower", "empowering", "empowered",
    "impactful", "meaningful",
]


def generic_vocabulary(text):
    low = text.lower()
    hits = {}
    for term in AI_VOCAB:
        c = len(re.findall(r'\b' + re.escape(term) + r'\b', low))
        if c:
            hits[term] = c
    return {"ai_vocabulary_hits": hits, "total_hit_count": sum(hits.values()),
            "unique_ai_terms": len(hits),
            "note": "Contextual interpretation required. Presence is a signal, "
                    "not automatic proof of AI authorship."}


TRIGRAM_STOPWORDS = {'the', 'a', 'an', 'of', 'in', 'to', 'is', 'are', 'and',
                     'or', 'but', 'for', 'that', 'this', 'it', 'on', 'at', 'by',
                     'as', 'with', 'from', 'be', 'was', 'were'}


def repetitive_phrase_detection(text):
    words = re.findall(r'\b\w+\b', text.lower())
    trigrams = {}
    for i in range(len(words) - 2):
        gram = words[i:i + 3]
        if not all(w in TRIGRAM_STOPWORDS for w in gram):
            key = ' '.join(gram)
            trigrams[key] = trigrams.get(key, 0) + 1
    repeated = {k: v for k, v in trigrams.items() if v >= 3}
    return {"repeated_3grams": dict(sorted(repeated.items(), key=lambda x: -x[1])[:10]),
            "high_repetition_phrase_count": len(repeated)}


def passive_estimate(sentences):
    pat = re.compile(r'\b(is|are|was|were|been|being|be)\s+\w+ed\b', re.I)
    count = sum(1 for s in sentences if pat.search(s))
    return {"passive_sentence_estimate": count,
            "passive_rate": round(count / len(sentences) if sentences else 0, 3),
            "note": "Rough estimate only. Not all -ed forms are passive voice."}


def list_density(text):
    bullets = len(re.findall(r'^\s*[-•*]\s+', text, re.M))
    numbered = len(re.findall(r'^\s*\d+[.)]\s+', text, re.M))
    total_words = len(tokenize_words(text))
    return {"bullet_items": bullets, "numbered_items": numbered,
            "total_list_items": bullets + numbered,
            "list_density_per_1000_words":
                round((bullets + numbered) / total_words * 1000, 1) if total_words else 0}

# ─── Readability and stance (from metrics.py) ────────────────────────────────


def count_syllables(word):
    word = word.lower().strip(".,!?;:'\"()")
    if not word:
        return 0
    if word.endswith('e') and len(word) > 2:
        word = word[:-1]
    return max(1, len(re.findall(r'[aeiou]+', word)))


def readability(sentences, words):
    if not sentences or not words:
        return {"flesch_kincaid_grade": 0.0, "gunning_fog_index": 0.0,
                "flesch_reading_ease": 0.0, "readability_assessment": "n/a"}
    syl = sum(count_syllables(w) for w in words)
    asl = len(words) / len(sentences)
    aspw = syl / len(words)
    complex_pct = sum(1 for w in words if count_syllables(w) >= 3) / len(words) * 100
    ease = round(206.835 - 1.015 * asl - 84.6 * aspw, 1)
    return {
        "flesch_kincaid_grade": round(0.39 * asl + 11.8 * aspw - 15.59, 1),
        "gunning_fog_index": round(0.4 * (asl + complex_pct), 1),
        "flesch_reading_ease": ease,
        "readability_assessment": ("very easy" if ease > 80 else "easy" if ease > 70
                                   else "standard" if ease > 60 else
                                   "difficult" if ease > 40 else "very difficult"),
    }


PREPOSITIONS = {'of', 'in', 'to', 'for', 'on', 'with', 'at', 'by', 'from',
                'into', 'through', 'during', 'before', 'after', 'above', 'below',
                'between', 'among', 'under', 'about', 'against', 'without', 'within',
                'around', 'along', 'following', 'across', 'behind', 'beyond',
                'including', 'throughout', 'regarding', 'concerning'}
WEAK_VERBS = {'is', 'are', 'was', 'were', 'be', 'been', 'being',
              'have', 'has', 'had', 'do', 'does', 'did',
              'will', 'would', 'could', 'should', 'may', 'might', 'can', 'shall'}


def information_density(text, words):
    low = [w.lower() for w in words]
    prep_rate = sum(1 for w in low if w in PREPOSITIONS) / len(words) if words else 0
    weak_rate = sum(1 for w in low if w in WEAK_VERBS) / len(words) if words else 0
    nom = nominalization_stats(text, words)
    score = (prep_rate * 200) + (nom["rate_per_1000_words"] / 2)
    return {"preposition_rate": round(prep_rate, 3),
            "weak_verb_rate": round(weak_rate, 3),
            "nominalization_rate_per_1000": nom["rate_per_1000_words"],
            "nominalization_assessment": nom["assessment"],
            "estimated_density_score": round(score, 1),
            "assessment": ("high density, characteristic of formal academic prose"
                           if score > 50 else "moderate density" if score > 30
                           else "low density, conversational")}


HEDGES = [r'\bmight\b', r'\bcould\b', r'\bmay\b', r'\bperhaps\b', r'\bpossibly\b',
          r'\bappears? to\b', r'\bseems? to\b', r'\btends? to\b',
          r'\bi think\b', r'\bi believe\b', r'\bone might\b', r'\bargua\w+\b',
          r'\bsuggests?\b', r'\bindicates?\b', r'\bseems?\b']
BOOSTERS = [r'\bclearly\b', r'\bobviously\b', r'\bcertainly\b', r'\bdefinitely\b',
            r'\bundoubtedly\b', r'\bwithout question\b', r'\bit is clear\b',
            r'\bof course\b', r'\bevident\w*\b']


STANCE_MIN_MARKERS = 3
STANCE_MIN_RATE_PER_1000 = 2.0


def stance_verdict(hedge, boost, wc):
    """
    Mirror of stance_balance() in scripts/_shared.py. A balance verdict needs a
    minimum of signal to mean anything, so no-stance text reads "absent" rather
    than falling through to "calibrated", and a couple of markers in a long
    document reads "too sparse to judge". Absent stance is not a defect by
    itself; whether the gap matters is genre judgment, made in SKILL.md.
    """
    total = hedge + boost
    if total == 0:
        return "absent"
    rate = total / wc * 1000 if wc else 0.0
    if total < STANCE_MIN_MARKERS or rate < STANCE_MIN_RATE_PER_1000:
        return "too sparse to judge"
    if hedge > boost * 3:
        return "over-hedged"
    if boost > hedge * 2:
        return "over-assertive"
    return "calibrated"


def tone_markers(text):
    low = text.lower()
    wc = len(text.split())
    hedge = sum(len(re.findall(p, low)) for p in HEDGES)
    boost = sum(len(re.findall(p, low)) for p in BOOSTERS)
    first = len(re.findall(r'\bi\b|\bme\b|\bmy\b|\bwe\b|\bour\b', low))
    per_k = lambda n: round(n / wc * 1000, 1) if wc else 0
    return {"hedge_count": hedge, "hedge_rate_per_1000": per_k(hedge),
            "booster_count": boost, "booster_rate_per_1000": per_k(boost),
            "question_count": text.count('?'),
            "reader_address_count": len(re.findall(r'\byou\b|\byour\b', low)),
            "first_person_count": first, "first_person_rate_per_1000": per_k(first),
            "stance_balance": stance_verdict(hedge, boost, wc)}

# ─── Repetition (from repetition.py) ─────────────────────────────────────────


def extract_ngrams(words, n, stopword_filter=True):
    grams = Counter()
    for i in range(len(words) - n + 1):
        gram = words[i:i + n]
        if stopword_filter:
            if len([w for w in gram if w not in STOPWORDS]) < max(1, n // 2):
                continue
        grams[' '.join(gram)] += 1
    return grams


def repeated_phrases(text):
    words = re.findall(r'\b[a-z]+\b', text.lower())
    out = {}
    for n in (3, 4, 5):
        rep = {k: v for k, v in extract_ngrams(words, n).items() if v >= 2}
        if rep:
            out[f'{n}-grams'] = dict(sorted(rep.items(), key=lambda x: -x[1])[:10])
    return out


def repeated_sentence_openings(sentences):
    two, three = Counter(), Counter()
    for s in sentences:
        w = s.lower().split()
        if len(w) >= 2:
            two[' '.join(w[:2])] += 1
        if len(w) >= 3:
            three[' '.join(w[:3])] += 1
    return {"repeated_2word_openings": {k: v for k, v in two.items() if v >= 3},
            "repeated_3word_openings": {k: v for k, v in three.items() if v >= 2}}


def paragraph_shapes(paragraphs):
    shapes = []
    for p in paragraphs:
        lengths = [len(s.split()) for s in get_sentences(p)]
        shapes.append(tuple('S' if l < 12 else 'M' if l < 25 else 'L' for l in lengths))
    counter = Counter(shapes)
    return {"total_paragraphs": len(paragraphs),
            "unique_structural_shapes": len(counter),
            "repeated_shapes": {str(k): v for k, v in counter.items()
                                if v >= 2 and len(k) >= 2},
            "structural_monotony_warning":
                len(counter) < max(1, len(paragraphs) / 3)}


REPEATED_TRANSITIONS = [
    r'furthermore', r'moreover', r'additionally', r'however',
    r'therefore', r'consequently', r'as a result', r'in conclusion',
    r'to summarize', r'in summary', r'in addition', r'on the other hand',
    r'that said', r'with that said', r'having said that',
    r'it is worth noting', r'it is important to note', r'it should be noted',
    r'building on this', r'leveraging this', r'given this',
    r'this demonstrates', r'this shows', r'this highlights', r'this underscores',
    r'this illustrates', r'this reveals',
]


def transition_repetition(text):
    low = text.lower()
    hits = {}
    for phrase in REPEATED_TRANSITIONS:
        c = len(re.findall(r'\b' + phrase + r'\b', low))
        if c >= 2:
            hits[phrase] = c
    return {"repeated_transitions": hits,
            "warning": ("High transition repetition creates mechanical rhythm"
                        if len(hits) >= 3 else None)}


# Named sentence frames. Mirror of SYNTACTIC_FRAMES in scripts/repetition.py.
#
# These catch a repeat that no word-level check sees: two sentences with no
# shared phrase and no shared opening that nonetheless make the same move.
# Eight regexes, no parser, no part-of-speech information. Two names are
# mechanical on purpose: "comma plus -ing word" fires on a real participial tail
# in "shipped in six weeks, leveraging existing infrastructure" and equally on a
# gerund subject in "In conclusion, caching remains", so it is named after what
# it matches rather than what it usually means. Fenced blocks and quoted
# specimens are counted as prose, as everywhere else in this script.
#
# The single warning is the same frame in two consecutive sentences. Consecutive
# is the smallest window there is, so nothing here is tuned to a specimen.
SYNTACTIC_FRAMES = (
    ("range sweep",
     r"\bfrom\b[^.;:]{1,80}?\b(?:to|through|into)\b"),
    ("comparative than",
     r"\b(?:more|less|fewer|greater)\b[^.;:]{1,60}?\bthan\b"),
    ("superlative membership",
     r"\bone of the\b[^.;:]{0,40}?(?:\b\w+est\b|\bmost\b|\bleast\b)"),
    ("scale superlative",
     r"\b(?:world|nation|country|continent|planet|industry|region|market)(?:'s|s')"
     r"\s+(?:\w+\s+){0,3}?(?:most|largest|biggest|fastest|oldest|leading|greatest)\b"),
    ("not just X but Y",
     r"\bnot\s+(?:just|only|merely|simply)\b[^.;:]{1,80}?\b(?:but|it['’]s|it is)\b"),
    ("comma plus -ing word",
     r",\s+(?!and\b|but\b|or\b|which\b|who\b|whose\b|where\b|while\b|when\b)\w+ing\b"),
    ("comma plus -ed by",
     r",\s+\w+ed\s+by\b"),
    ("where X meets Y",
     r"\bwhere\b[^.;:]{1,50}?\bmeets?\b"),
)

FRAME_PATTERNS = tuple((name, re.compile(p, re.IGNORECASE)) for name, p in SYNTACTIC_FRAMES)


def syntactic_frames(sentences):
    per_sentence = []
    for i, s in enumerate(sentences):
        hits = sorted(name for name, pat in FRAME_PATTERNS if pat.search(s))
        if hits:
            per_sentence.append({"sentence_index": i, "frames": hits})

    counts = Counter()
    for e in per_sentence:
        for name in e["frames"]:
            counts[name] += 1

    by_index = {e["sentence_index"]: set(e["frames"]) for e in per_sentence}
    consecutive = []
    for i in range(len(sentences) - 1):
        for name in sorted(by_index.get(i, set()) & by_index.get(i + 1, set())):
            consecutive.append({"frame": name, "sentence_indices": [i, i + 1],
                                "first": sentences[i][:90], "second": sentences[i + 1][:90]})

    return {"total_sentences": len(sentences),
            "frame_counts": dict(sorted(counts.items(), key=lambda kv: (-kv[1], kv[0]))),
            "sentences_using_a_frame": len(per_sentence),
            "consecutive_repeats": consecutive}


# Coordinated series of three. Mirror of coordinated_series in repetition.py.
#
# Requires the Oxford comma, so series without it are missed. Reports without
# ruling, because whether a third item carries content is not a regex question.
# The one warning is a lexically parallel triple, where all three items open with
# the same token, since that anaphora is a rhythm device by construction. It can
# still be legitimate: three distinct "whether" clauses are structure, not
# decoration. The test is whether cutting the third item loses information.
#
# The anaphora is established on items two and three, then confirmed inside the
# first segment, because the first segment also carries the sentence stem: in
# "The plan needed a bigger room, a longer window, and a second reviewer" the
# first item is "a bigger room" and reading the segment's first word gives "The".
SERIES_COORDINATOR = re.compile(r"^(?:and|or)\s+\S", re.IGNORECASE)
SERIES_LEAD_TOKEN = re.compile(r"^(?:and\s+|or\s+)?([a-zA-Z']+)", re.IGNORECASE)


def series_lead_word(segment):
    m = SERIES_LEAD_TOKEN.match(segment)
    return m.group(1).lower() if m else ""


def series_first_item(segment, lead):
    if not lead or not lead[0].isalpha():
        return ""
    for m in reversed(list(re.finditer(r"\b" + re.escape(lead) + r"\b",
                                       segment, re.IGNORECASE))):
        rest = segment[m.start():]
        if len(rest.split()) >= 2:
            return rest
    return ""


def coordinated_series(sentences, word_count):
    found, parallel = [], []
    for i, s in enumerate(sentences):
        segs = [seg.strip() for seg in s.split(",")]
        if len(segs) < 3 or not SERIES_COORDINATOR.match(segs[-1]):
            continue
        tail = segs[-3:]
        found.append({"sentence_index": i, "comma_segments": len(segs), "series_tail": tail})
        lead = series_lead_word(tail[1])
        if lead and lead == series_lead_word(tail[2]):
            first = series_first_item(tail[0], lead)
            if first:
                parallel.append({"sentence_index": i, "lead_word": lead,
                                 "items": [first, tail[1], tail[2]]})

    rate = (len(found) / word_count * 1000) if word_count else 0.0
    return {"series_count": len(found),
            "series_rate_per_1000_words": round(rate, 1),
            "series": found,
            "parallel_triples": parallel}


def lexical_diversity(text):
    words = re.findall(r'\b[a-z]+\b', text.lower())
    if not words:
        return {}
    content = [w for w in words if w not in STOPWORDS and len(w) > 3]
    cttr = len(set(content)) / len(content) if content else 0
    return {"total_tokens": len(words), "unique_types": len(set(words)),
            "type_token_ratio": round(len(set(words)) / len(words), 3),
            "content_word_ttr": round(cttr, 3),
            "assessment": ("low diversity for this proxy" if cttr < 0.55 else
                           "moderate diversity" if cttr < 0.70 else "high diversity")}

# ─── Combined report ─────────────────────────────────────────────────────────


def analyze(text):
    sentences = get_sentences(text)
    paragraphs = get_paragraphs(text)
    words = tokenize_words(text)
    return {
        "word_count": len(words),
        "sentence_count": len(sentences),
        "paragraph_count": len(paragraphs),
        "sentence_lengths": sentence_lengths(sentences),
        "paragraph_structure": paragraph_lengths(paragraphs),
        "opening_analysis": opening_word_analysis(sentences),
        "participial_clauses": participial_rate(sentences),
        "nominalization_density": nominalization_stats(text, words),
        "transition_words": transition_density(text, sentences),
        "generic_vocabulary": generic_vocabulary(text),
        "passive_voice": passive_estimate(sentences),
        "list_density": list_density(text),
        "phrase_repetition": repetitive_phrase_detection(text),
        "readability": readability(sentences, words),
        "information_density": information_density(text, words),
        "tone_markers": tone_markers(text),
        "repeated_phrases": repeated_phrases(text),
        "repeated_sentence_openings": repeated_sentence_openings(sentences),
        "paragraph_structure_repetition": paragraph_shapes(paragraphs),
        "transition_phrase_repetition": transition_repetition(text),
        "repeated_syntactic_frames": syntactic_frames(sentences),
        "coordinated_series": coordinated_series(sentences, len(words)),
        "lexical_diversity": lexical_diversity(text),
    }


def report(r):
    L = []
    L.append("NOT AI : MEASUREMENT")
    L.append("─" * 44)
    L.append(f"Words: {r['word_count']}  |  Sentences: {r['sentence_count']}"
             f"  |  Paragraphs: {r['paragraph_count']}")

    sl = r['sentence_lengths']
    d = sl.get('distribution', {})
    L.append("\nSENTENCE RHYTHM")
    L.append(f"  Mean length:   {sl['mean']} words")
    L.append(f"  Std deviation: {sl['std']} words  (burstiness: {sl['burstiness']})")
    L.append(f"  Very short (<8):  {d.get('very_short_under_8', 0)}  |  "
             f"Short (8-15): {d.get('short_8_to_15', 0)}  |  "
             f"Medium (16-25): {d.get('medium_16_to_25', 0)}")
    L.append(f"  Long (26-35):  {d.get('long_26_to_35', 0)}  |  "
             f"Very long (35+): {d.get('very_long_over_35', 0)}")
    if sl['burstiness'] < 0.30:
        L.append("  ⚠ Low burstiness: sentence lengths are very uniform")
    elif sl['burstiness'] > 0.55:
        L.append("  ✓ Good length variation")
    L.append("  Burstiness verdicts are unreliable. Do not treat either as a target.")

    ps = r['paragraph_structure']
    if ps:
        pd = ps.get('distribution', {})
        L.append(f"  Paragraphs: {ps['count']}, mean {ps['mean_sentences']} sentences"
                 f"  |  1 sent: {pd.get('1_sentence', 0)}"
                 f"  |  2-3: {pd.get('2_3_sentences', 0)}"
                 f"  |  4-5: {pd.get('4_5_sentences', 0)}"
                 f"  |  6+: {pd.get('6_plus_sentences', 0)}")

    L.append("\nSTRUCTURAL SIGNALS")
    pc = r['participial_clauses']
    icon = "⚠" if pc['assessment'].startswith(("high", "elevated")) else "✓"
    L.append(f"  {icon} Participial clause openers: {pc['participial_opener_count']}"
             f" / {pc['sentences_analyzed']} sentences"
             f" ({pc['participial_opener_rate']:.0%})  |  {pc['assessment']}")
    if pc['participial_opener_count'] == 0:
        L.append("      Anchored match only. 'By leveraging...' style openers are not counted.")
    nd = r['nominalization_density']
    icon = "⚠" if nd['assessment'].startswith(("high", "elevated")) else "✓"
    L.append(f"  {icon} Nominalization density: {nd['rate_per_1000_words']}"
             f" per 1,000 words  |  {nd['assessment']}")
    L.append("      Proxy measure. Compare only against another run of this script.")
    tw = r['transition_words']
    if tw['total_mechanical_transitions']:
        L.append(f"  ⚠ Mechanical transitions: {tw['total_mechanical_transitions']}"
                 f" instances  |  {', '.join(tw['mechanical_transition_hits'])}")
    else:
        L.append("  ✓ No high-frequency mechanical transitions detected")
    pv = r['passive_voice']
    L.append(f"  Passive estimate: {pv['passive_sentence_estimate']} sentences"
             f" ({pv['passive_rate']:.0%}). Not all -ed forms are passive, and the"
             f" research shows models underuse agentless passives, so a low figure"
             f" is not automatically good.")

    oa = r['opening_analysis']
    L.append("\nSENTENCE OPENINGS")
    if oa.get('repeated_openers_3plus'):
        for w, c in oa['repeated_openers_3plus'].items():
            L.append(f"  ⚠ '{w}' used to open {c} sentences")
    else:
        L.append("  ✓ No highly repeated sentence openers")
    if oa.get('max_consecutive_same_opener', 0) >= 3:
        L.append(f"  ⚠ {oa['max_consecutive_same_opener']} consecutive sentences"
                 f" with same opener")
    ro = r['repeated_sentence_openings']
    for phrase, c in {**ro.get('repeated_3word_openings', {}),
                      **ro.get('repeated_2word_openings', {})}.items():
        L.append(f"  ⚠ '{phrase}': {c} sentences")

    gv = r['generic_vocabulary']
    L.append("\nAI-ASSOCIATED VOCABULARY")
    if gv['ai_vocabulary_hits']:
        # Cap of eight, disclosed. See the note in analyze_structure.py: these
        # two extra lines exist because a silent cap produced two wrong figures.
        ranked = sorted(gv['ai_vocabulary_hits'].items(), key=lambda x: -x[1])
        for term, c in ranked[:8]:
            L.append(f"  • '{term}': {c}x")
        if len(ranked) > 8:
            rest = ', '.join(f"'{t}'" for t, _ in ranked[8:])
            L.append(f"  ... {len(ranked) - 8} more not listed above: {rest}")
        L.append(f"  Total: {gv['unique_ai_terms']} unique terms, "
                 f"{sum(gv['ai_vocabulary_hits'].values())} occurrences")
        L.append(f"  Note: {gv['note']}")
        L.append("  A word being quoted counts the same as a word being used.")
    else:
        L.append("  ✓ No high-frequency AI vocabulary detected")

    pr = r['phrase_repetition']
    if pr['repeated_3grams']:
        L.append("\nREPEATED PHRASES (3+ occurrences)")
        for phrase, c in list(pr['repeated_3grams'].items())[:5]:
            L.append(f"  ⚠ '{phrase}': {c}x")

    rp = r['repeated_phrases']
    L.append("\nREPEATED PHRASES (2+ occurrences, 3 to 5 words)")
    if rp:
        for _, phrases in rp.items():
            for phrase, c in list(phrases.items())[:5]:
                L.append(f"  • '{phrase}': {c}x")
    else:
        L.append("  ✓ None detected")

    psr = r['paragraph_structure_repetition']
    if psr.get('structural_monotony_warning'):
        L.append(f"\n⚠ PARAGRAPH STRUCTURE: {psr['unique_structural_shapes']} unique"
                 f" shapes for {psr['total_paragraphs']} paragraphs, so paragraph"
                 f" shape may be monotonous")
    else:
        L.append(f"\nPARAGRAPH STRUCTURE: {psr['unique_structural_shapes']} unique shapes ✓")

    tr = r['transition_phrase_repetition']
    if tr['repeated_transitions']:
        L.append("\nREPEATED TRANSITIONS")
        for phrase, c in tr['repeated_transitions'].items():
            L.append(f"  ⚠ '{phrase}': {c}x")
    else:
        L.append("\nTRANSITIONS: No high-frequency repetition ✓")

    sf = r['repeated_syntactic_frames']
    if sf['consecutive_repeats']:
        L.append("\nREPEATED SENTENCE FRAMES")
        for rep in sf['consecutive_repeats']:
            a, b = rep['sentence_indices']
            L.append(f"  ⚠ '{rep['frame']}' in sentences {a + 1} and {b + 1}, back to back")
            L.append(f"      {rep['first']}")
            L.append(f"      {rep['second']}")
    elif sf['frame_counts']:
        listed = ', '.join(f"{k} x{v}" for k, v in list(sf['frame_counts'].items())[:5])
        L.append(f"\nSENTENCE FRAMES: no back-to-back repeat ✓  ({listed})")
    else:
        L.append("\nSENTENCE FRAMES: none of the eight named frames found ✓")

    cs = r['coordinated_series']
    if cs['parallel_triples']:
        L.append("\nCOORDINATED SERIES")
        for tri in cs['parallel_triples']:
            L.append(f"  ⚠ sentence {tri['sentence_index'] + 1}: three items all opening"
                     f" '{tri['lead_word']}'. Does cutting the third lose information,"
                     f" or only cadence?")
            L.append(f"      {', '.join(tri['items'])[:110]}")
    if cs['series_count']:
        flagged = {t['sentence_index'] for t in cs['parallel_triples']}
        plain = [s for s in cs['series'] if s['sentence_index'] not in flagged]
        if plain:
            if not cs['parallel_triples']:
                L.append("\nCOORDINATED SERIES")
            L.append(f"  {len(plain)} series closing on 'and' or 'or'  |  "
                     f"{cs['series_rate_per_1000_words']} per 1,000 words overall."
                     f" No verdict: read each one and ask whether the third item is"
                     f" there for content or for cadence.")
            for s in plain[:5]:
                L.append(f"      sentence {s['sentence_index'] + 1}:"
                         f" {', '.join(s['series_tail'])[:110]}")
    else:
        L.append("\nCOORDINATED SERIES: none found ✓")

    ld = r['lexical_diversity']
    if ld:
        icon = "✓" if "high" in ld['assessment'] else "⚠"
        L.append(f"\nLEXICAL DIVERSITY: {ld['content_word_ttr']:.0%} content-word TTR"
                 f"  |  {ld['assessment']} {icon}")

    rd = r['readability']
    L.append("\nREADABILITY")
    L.append(f"  Flesch-Kincaid Grade:  {rd['flesch_kincaid_grade']}"
             f" (US grade level equivalent)")
    L.append(f"  Gunning Fog Index:     {rd['gunning_fog_index']}"
             f" ({rd['readability_assessment']})")
    L.append(f"  Flesch Reading Ease:   {rd['flesch_reading_ease']} / 100")
    L.append("  Read these against the genre, not against a universal target.")

    idy = r['information_density']
    L.append("\nINFORMATION DENSITY")
    L.append(f"  Density score: {idy['estimated_density_score']}  |  {idy['assessment']}")
    L.append(f"  Preposition rate:  {idy['preposition_rate']:.1%}")
    L.append(f"  Nominalizations:   {idy['nominalization_rate_per_1000']}"
             f" per 1,000 words  |  {idy['nominalization_assessment']}")

    t = r['tone_markers']
    L.append("\nEPISTEMIC STANCE")
    L.append(f"  Hedges:     {t['hedge_count']} ({t['hedge_rate_per_1000']} per 1,000 words)")
    L.append(f"  Boosters:   {t['booster_count']} ({t['booster_rate_per_1000']} per 1,000 words)")
    L.append(f"  Balance:    {t['stance_balance']}")
    L.append("  Models underuse hedges at 50% to 63% of the human rate, so"
             " 'over-hedged' on a draft is worth checking before acting on."
             "\n  'absent' means no stance marker was found at all, which some"
             " genres do not need; it is a reading, not a fault.")
    L.append("\nENGAGEMENT MARKERS")
    L.append(f"  Questions:      {t['question_count']}")
    L.append(f"  Reader address: {t['reader_address_count']}")
    L.append(f"  First-person:   {t['first_person_count']}"
             f" ({t['first_person_rate_per_1000']} per 1,000 words)")

    L.append("\nA script measures a file, not a deliverable. Flags, editorial notes"
             "\nand bracketed slots are counted as prose.")
    return "\n".join(L)


def main():
    ap = argparse.ArgumentParser(description='Not Ai: single-file measurement pass')
    ap.add_argument('input_file', nargs='?')
    ap.add_argument('--stdin', action='store_true')
    ap.add_argument('--json', action='store_true')
    args = ap.parse_args()

    if args.stdin or not args.input_file:
        text = sys.stdin.read()
    else:
        path = Path(args.input_file)
        if not path.is_file():
            print(f"Error: file not found: {args.input_file}", file=sys.stderr)
            return 1
        text = path.read_text(encoding='utf-8')

    if not text.strip():
        print("Error: no text provided", file=sys.stderr)
        return 1

    result = analyze(text)
    print(json.dumps(result, indent=2, ensure_ascii=False) if args.json
          else report(result))
    return 0


if __name__ == '__main__':
    sys.exit(main())
```
