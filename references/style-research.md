# Style research: measured feature-by-feature differences

Exact figures for the structural differences between instruction-tuned model output and human writing, drawn from Reinhart et al. (2025) and supporting studies. Full citations in `references/writing-research.md`.

## How to read the numbers in this file

**Human rates are per 1,000 tokens**, measured on dependency-parsed text using Biber's 66-feature tagset via the `pseudobibeR` package. This matters more than it sounds. A rate per 1,000 tokens from a tagged parse is not comparable to a rate per 1,000 words from a regex, and it is not comparable to a percentage of sentences.

**Model figures are percentages of the human rate.** `527%` means the model produced the feature at 5.27 times the rate human writers did on the same prompts. `51%` means about half. 100% would be parity.

**The comparison is within-corpus and prompt-matched.** Both corpora use a two-chunk design: a human writer's text is split at roughly 500 words, the model receives chunk 1 as context and generates a continuation, and the model's continuation is compared against the human chunk 2. Same author, same topic, same point in the text. That design is what makes the percentages meaningful, and it is why figures from other studies are not directly comparable.

**Corpora.** HAP-E (Human AI Parallel English) contributed 8,290 valid texts across fiction, news, blogs and academic prose. COCA AI Parallel (CAP) contributed 9,615. Models tested: GPT-4o, GPT-4o Mini, Llama 3 8B and 70B in both base and instruction-tuned form.

**The scripts in this repository do not reproduce these numbers.** `scripts/analyze_structure.py` uses regular expressions, counts sentences rather than tokens, and reports nominalization figures roughly five and a half times higher, measured below. Its output is comparable only against another run of itself. Never quote a script figure as though it came from the paper, and never compare the two. See `scripts/_shared.py`.

---

## The headline finding

Instruction tuning, not model scale, produces the fingerprint.

Base Llama 3 models sit at 94% to 102% of human rates on the features listed below. Their instruction-tuned counterparts diverge sharply on the same features, from the same prompts, at the same parameter count. Llama 3 70B and 8B show similar divergence to each other, so scaling up does not reduce it.

This is the single most consequential result in the literature for a skill like this one. It means the fingerprint is a product of the alignment process rather than of language modelling itself, and it means the pattern is a learned preference rather than a limitation. Preferences can be written around.

---

## Overrepresented features

### Present participial clauses

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

### That-clauses as subject

| | Rate |
|---|---|
| Human writers | 2.1 per 1,000 tokens |
| GPT-4o | 331% |
| GPT-4o Mini | 263% |

```
That the policy failed was evident to everyone involved.
```

A formal construction that fronts a proposition. Human writers use it sparingly, usually for emphasis.

### Past participial clauses

Instruction-tuned models: 273% to 307% of the human rate.

```
Founded in 1923, the company relocated twice.
Written under a pseudonym, the report circulated widely.
```

Same mechanism as the present participial clause, and the same repair.

### Nominalizations

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

### Attributive adjectives, demonstratives and downtoners

Instruction-tuned models: 118% to 155% of the human rate across these three feature families.

Attributive adjectives sit before the noun (`a comprehensive review`) rather than after a copula (`the review was comprehensive`). Stacking them is how model prose acquires its characteristic density. Downtoners are hedging adverbs like `somewhat`, `slightly` and `relatively`.

### Mean word length

Instruction-tuned models: 114% to 116% of the human figure.

A small multiplier on a feature with very low variance, which makes it a surprisingly stable signal. It reflects consistent preference for the longer Latinate option: `utilize` over `use`, `facilitate` over `help`, `demonstrate` over `show`.

### Clausal coordination, for Llama only

Llama 3 Instruct models: 116% to 141%. GPT models run the other way, at 59% to 63%.

This is a useful reminder that the fingerprint is model-specific in its details even where the overall direction is shared. A rule written to reduce coordination would be correcting Llama output and damaging GPT output.

---

## Underrepresented features

The gap runs in both directions, and the underuse side is the half most humanizer tools ignore entirely.

### Agentless passives

GPT-4o and GPT-4o Mini: 51% to 53% of the human rate. Roughly half.

This contradicts the most widely repeated belief about AI writing. Models do not overuse the passive voice; the GPT family underuses it, almost certainly because "prefer the active voice" is among the most common pieces of writing advice in the training data and in the preferences of human raters.

The practical consequence is direct: **converting passive to active as a blanket rule moves text further from the human distribution, not closer.** That conversion is a staple of commercial humanizers and it is counterproductive. Llama base models sit near the human rate.

### Hedges

Instruction-tuned models: 50% to 63% of the human rate.

Human experts write `probably`, `I think`, `as far as I can tell`, `it looks like`, and they write them where they are actually uncertain. Models hedge less overall, and when they do hedge they place it formulaically (`It is worth noting that`) in front of claims they are not uncertain about at all. The deficit is in calibration as much as in quantity.

Adding a hedge that reflects real uncertainty in the source is a legitimate repair. Inventing uncertainty the author does not have is fabrication, and this skill does not do it.

### Existential `there`

Instruction-tuned models: 59% to 71%.

```
There were three objections to the proposal.
```

Another construction that writing advice discourages, and another case where following the advice absolutely produces a measurable divergence from how people actually write.

### Adverbs

Instruction-tuned models: 82% to 86%.

Also consistent with prescriptive advice about adverbs being weak, absorbed through alignment and then applied with a uniformity no human writer sustains.

### A note on what these four have in common

Agentless passives, existential `there`, adverbs, and to a degree hedges are all things style guides tell writers to avoid. Instruction-tuned models avoid them more consistently than the humans whose writing the guides describe. The fingerprint is partly the signature of advice followed too well.

This is the most useful single insight in the whole literature for anyone editing suspected machine text, because it inverts the intuitive move. The instinct is to apply writing advice harder. The measurement says the text already has writing advice applied harder than any human would.

---

## Vocabulary divergence

### Extreme overrepresentation

These appeared in GPT-4o and GPT-4o Mini output at roughly 84 to 171 times the human rate on matched prompts:

```
camaraderie   tapestry     palpable     intricate    underscore
unspoken      amidst       solace       fleeting     vibrant
cacophony     grapple      ignite       unravel
```

Two things about this list are worth holding onto. The multipliers are far larger than anything on the structural side, which is why vocabulary is the signal people notice. And it is nonetheless the weaker signal, because it is trivially removable: swap fourteen words and the morphosyntactic profile is completely unchanged. See `rules/vocabulary.md` for why the swap usually makes the writing worse.

The genre-independence is the sharper finding. GPT-4o reaches for `camaraderie was palpable` when writing about sports, about workplaces, about war. Human writers reach for it almost never.

### Extreme underrepresentation

Over 100 times rarer in instruction-tuned output than in human writing:

- Profanity and blunt language, an unambiguous RLHF artifact
- `i.e.` and `e.g.`

Contractions are also depressed in registers where human writers contract freely.

The `i.e.` result is the most interesting of the three, because there is no plausible safety or preference reason for it. It suggests the models have absorbed a general register preference for spelled-out formal prose that goes beyond anything a rater explicitly asked for.

---

## Classification results

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

## Genre and register

The Biber framework's first and strongest dimension runs from involved to informational. Conversation sits at the involved end; academic prose sits at the informational end.

Human writers move along this dimension with genre. A text message, a blog post and a journal article occupy visibly different positions.

Instruction-tuned models shift toward the informational end **and stay there regardless of genre**. Fiction generated by GPT-4o has information density close to its academic prose. This is the most likely explanation for why machine fiction reads flat: it is written in the register of a description of a story rather than the register of a story.

The practical rule: check register fit before flagging any individual feature. Nominalization in an academic abstract may be correct. The same density in dialogue is not. See `rules/context.md`.

---

## Limits of everything above

**These are 2024 and 2025 model versions.** GPT-4o and Llama 3. Vendors have since adjusted, sometimes in direct response to public commentary about these exact tells. The em dash is the documented case: measurement through mid-2026 found ChatGPT using them less than it did, and GPT-5.1 suppressing them further. Any specific multiplier in this file should be read as a finding about a model generation, not a permanent property.

**Fine-tuning removes the fingerprint.** Dawkins et al. (2025) fine-tuned on a genre-specific corpus of tweets and substantially reduced the structural differences for that genre. A model tuned on target-genre human writing is much harder to distinguish, which caps how durable any of this can be.

**Vocabulary flows back.** Words documented here as machine markers have measurably risen in human usage since 2023. `Delve` is the standard example. The list decays through the ordinary mechanism of people reading a lot of model output.

**Human writing is a distribution, not a point.** Every percentage above compares against an aggregate. Individual human writers scatter widely, and some sit naturally where the models sit. A writer whose prose is dense, formal and participial is not writing badly and is not writing with a model. Aiming output at the human mean would produce a new cluster, which is the failure mode of every tool that treats humanness as a target rather than a range.
