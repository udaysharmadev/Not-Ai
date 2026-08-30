---
name: not-ai
description: Diagnose and repair the structural patterns that make prose read as machine-written, or write from scratch without them. Use when the user wants text humanized, asks why their writing sounds robotic or like AI, wants AI patterns removed from a draft, or wants something written that will not read as model output. Triggers on "not-ai", "/not-ai", "humanize this", "make this sound human", "sounds like AI", "does this read as AI", "fix my writing".
---

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

Load a file when its stage calls for it. Do not read them all up front.

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

Run the scripts. They are deterministic and dependency-free, and they keep the diagnostic from becoming an impression.

```bash
python3 scripts/analyze_structure.py input.md
python3 scripts/repetition.py input.md
python3 scripts/metrics.py input.md
```

Where the scripts cannot run, count by hand. Signals in priority order:

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

Run the scripts on the output, not only on the input.

```bash
python3 scripts/analyze_structure.py output.md
python3 scripts/repetition.py output.md
python3 scripts/metrics.py output.md
python3 scripts/scan_prose.py output.md
```

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

Diagnostic, then rewritten text, then a short note on what changed and why. The note lets the author reject any individual edit, so it names specific changes rather than summarising the general approach.

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
