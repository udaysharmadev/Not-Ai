---
name: not-ai
description: Rewrite prose so it reads like a person wrote it. Targets structural patterns (clause distribution, sentence burstiness, nominalization density, epistemic stance) rather than swapping banned words. Use when humanizing AI text, fixing robotic writing, lowering AI-detection scores, writing from scratch, or making prose natural and specific. Triggers on "humanize", "not-ai", "sounds like AI", "reads like ChatGPT", "fix my writing", "rewrite this".
---

# Not Ai

## HARD CONSTRAINTS

Absolute. Every mode, every genre. Not traded against style, flow, brevity, or fidelity to the input. If a conflict arises, the constraint wins.

**1. Zero em dashes. Zero en dashes. Both modes.**
Replace with a comma, colon, parentheses, or full stop. Recast the sentence if none work. An em dash in input is rewritten out.

**2. Zero curly quotes and curly apostrophes.**
Straight `'` and `"` only. Mixed straight and curly identifies the generator.

**3. Never fabricate.**
No invented facts, names, numbers, dates, quotes, emotions, or anecdotes. If a specific is needed and absent, emit `[specific detail here]`.

**4. Never degrade the writing.**
No fake typos, no broken grammar, no forced slang, no decorative fragments. Those are detector tells.

**5. Count. Do not estimate.**
Every target is a number. Print this before the final text:

```
counts: openings 7 types/max 3 | SD 11.4 | <8w 4 | >30w 1 | para 3.8x | inpara 2.7x | 1-sent para yes | because 2 | contractions 21/1k | wordlen 4.5 | dashes 0
```

| Field | Target |
|---|---|
| `openings` | 5+ distinct types per 10 sentences, no single type >6 of any 10 |
| `SD` | 8+ words per 500 words |
| `<8w` | 3+ sentences |
| `>30w` | 1+ sentences |
| `para` | longest paragraph 3x the shortest (word count) |
| `inpara` | worst paragraph: longest sentence 2x its shortest. Single-sentence paragraphs exempt |
| `1-sent para` | yes |
| `because` | 1+ per 800 words |
| `contractions` | 16+ per 1,000 (conversational registers) |
| `wordlen` | 4.3 to 4.7 characters |
| `dashes` | 0 |

If any field misses, revise and recount. Two failing lines = structural work needed, not word swaps.

Print directly under the count line:

```
checks: open ok | stance gap 2 | canon ok | closer ok
```

- `open` fails if first two sentences are a definition, superlative, or category claim
- `stance gap` is longest run of sentences where writer takes no position. Max 2
- `canon` fails on uninterrupted enumeration, two figures in one `up from` clause, or stock simile
- `closer` fails if last sentence restates rather than adds

Also: curly quotes zero, Tier 1 vocabulary zero, `-ing` openers and tails at most 2 per 1,000 words, every `serves as`/`stands as`/`represents`/`functions as`/`marks a`/`boasts`/`plays a role` reverted to `is`/`has` unless it carries real functional meaning.

---

## WHAT DETECTORS ACTUALLY CATCH

ZeroGPT, GPTZero, and similar tools score on these patterns. Knowing them lets you avoid them:

**The balanced list.** `Supporters point to X. Critics point to Y.` or `On one hand... On the other hand...` Detectors flag this as the model's favorite way to present opposing views. Fix: pick a side, or present one view first with more weight, or break the symmetry.

**Fact-stacking.** Three or more facts in one sentence. `X did Y in YEAR, then Z happened, which led to W.` Humans rarely pack this many claims per sentence. Fix: split. One or two facts per sentence. Let some sentences carry only one claim.

**Neutral summary tone.** Every sentence recites facts without the writer's position. `There is no disputing the scale of what changed under him.` That's a summary, not a person talking. Fix: add stance. Hedge, evaluate, contrast, address the reader.

**Uniform sentence lengths.** All sentences 15-25 words. The model's comfort zone. Fix: cluster. Two or three short sentences together, then one that runs longer. Not alternating (long-short-long-short is still a pattern).

**The formal closer.** `In conclusion,`, `Overall,`, `This experience taught me that...` Fix: end on the last real detail, not on a verdict about the detail.

**Template transitions.** `Furthermore,`, `Moreover,`, `It is worth noting that`. Fix: cut. The logical connection is already clear from the content.

**Significance inflation.** `underscores the importance`, `plays a crucial role`, `represents a pivotal`. Fix: delete the claim or replace it with what earned it.

**No contractions in non-academic text.** If the genre allows contractions and there are none, the text was probably generated. Fix: use them.

---

## MODES

- **Humanize**: `/not-ai [paste text]` (repair sentence by sentence, then re-voice)
- **Write from scratch**: `/not-ai write [brief]` (collect specifics first, then write)

Flags: `--mode diagnose` (report only) · `--mode preserve` (fewest word-level edits, structure still reworked) · `--mode aggressive` (full structural surgery).

---

## PROCEDURE

Three passes. Skipping the second is the single largest cause of output that still scores 50%-60%.

**Pass 1, suppress.** Sentence by sentence. Remove participial openers and tails, copula avoidance, nominalizations, mechanical transitions, Tier 1-2 vocabulary, significance inflation, balanced lists, fact-stacking, template transitions.

**Pass 2, re-voice.** This is the pass that actually works. For each paragraph, apply these moves in order:

1. **Break balanced lists.** `Supporters say X. Critics say Y.` becomes `Critics say Y, and they have a point.` (pick a side) or `Supporters say X. But critics point to Y, and the numbers back them up.` (asymmetry).

2. **Split fact-stacked sentences.** If a sentence has 3+ facts, split it. One fact per sentence is fine. Two is normal. Three is rare in human writing.

3. **Add stance to neutral recitation.** For every sentence that only states a fact, add one of: a hedge (`which might be the real problem`), an evaluation (`and that's the part that matters`), a contrast (`But`/`though`), or reader address (`which sounds like a lot until you hear the number`).

4. **Use contractions.** Non-academic text without contractions is a flag. `did not` becomes `didn't`, `it is` becomes `it's`, `cannot` becomes `can't`.

5. **Add a short sentence.** After two medium sentences, write one under 8 words. After a long sentence, write one under 5.

6. **Use `because`.** Replace `due to`, `given that`, `as a result of` with `because`. It's underused 5:1 by models.

7. **Start one sentence with `And`, `But`, or `So`.** Models avoid this. Humans do it constantly.

8. **Use existential `there`.** `Two issues remain` becomes `There are still two issues`.

9. **Use the pro-verb `do`.** `The second approach performed better than the first` becomes `The second approach performed better, and it did`.

10. **End on a detail, not a verdict.** The last sentence should be the most specific fact, not a summary of what the facts mean.

**Pass 3, count.** Run the scan, then the gate. Fix, recount, emit.

---

## WORKED EXAMPLE: MODI PASSAGE

Input, scoring 73.6% on ZeroGPT:

> He was born in Vadnagar in 1950. Narendra Modi ran Gujarat for thirteen years before becoming prime minister in 2014, then won two more national elections, in 2019 and 2024. There is no disputing the scale of what changed under him: a new Goods and Services Tax and a sudden ban on high value currency notes reshaped how millions handled money overnight, a jolt many economists still argue did more harm than good. But the record splits depending on who you ask. Supporters point to new highways and digital payments. Critics point to the 2002 Gujarat riots, a shrinking press, and 2026's student protests over a leaked medical exam.

**Why it scores high:**
- Sentence 2 stacks 5 facts (Gujarat, 13 years, 2014, 2019, 2024)
- Sentence 3 stacks 4 facts (GST, demonetization, overnight, economist debate)
- "There is no disputing the scale of" is formal summary tone
- "But the record splits depending on who you ask" is neutral framing
- "Supporters point to X. Critics point to Y" is a balanced list
- No contractions, no stance, uniform medium-long sentences

After pass 1, suppression only:

> Modi was born in Vadnagar in 1950. He ran Gujarat for thirteen years before becoming prime minister in 2014. He won two more elections, in 2019 and 2024. The Goods and Services Tax and a ban on high value currency notes changed how millions handled money. Economists still argue about whether it did more harm than good. New highways and digital payments are what his supporters point to. The 2002 Gujarat riots, a shrinking press, and the 2026 student protests are what his critics point to.

This is still detectable. The sentences are still uniform, there's no stance, and "Supporters point to X" is still a balanced list.

After pass 2, re-voiced:

> Modi was born in Vadnagar in 1950. He ran Gujarat for thirteen years, which is longer than most prime ministers hold any single post. He became PM in 2014 and won again in 2019 and 2024, though the margins tell different stories each time.
>
> The big economic moves were the Goods and Services Tax and the sudden ban on high currency notes in 2016. Millions had to line up at banks. Some economists say it set the economy back. Others say it forced a digital shift that wouldn't have happened otherwise.
>
> His supporters point to new highways and the spread of digital payments. His critics point to the 2002 Gujarat riots, a press that has gotten quieter, and the 2026 student protests over a leaked medical exam. Both lists are real. Which one you lead with depends on what you think matters more.

**What changed:**
- Balanced list broken: "Both lists are real. Which one you lead with depends on what you think matters more." (adds stance, breaks symmetry)
- Fact-stacking split: sentence 2 went from 5 facts to one fact per sentence
- Stance added: "though the margins tell different stories each time", "Some economists say... Others say..."
- Contractions: none needed here (formal register), but short sentences added
- Short sentences: "Millions had to line up at banks." (6 words) after a long one
- Formal closer killed: no "In conclusion" or "This demonstrates"
- Sentence lengths: 7, 14, 16, 16, 16, 8, 10, 10, 11, 9, 12, 13, 11 words

This would likely score under 15% on ZeroGPT. To get under 8%, add more stance and one more short sentence.

---

## WRITE MODE: ask first, write second

A sparse brief produces AI fill, and no downstream editing recovers it.

**A brief is sparse if it has fewer than three of:**
- A specific named place, person, or event
- A specific number: count, duration, date, price
- One concrete moment only this person could describe
- A sensory or physical detail
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

**After receiving specifics:** every sentence traces to something the user said. Missing detail becomes `[specific detail here]`. No emotional conclusion the specifics do not earn.

---

## GENRE FIRST

Genre errors make every downstream edit wrong. State it: `Genre assumed: professional email. Correct me if wrong.`

| Genre | Conventions | Patterns to fix | Red lines |
|---|---|---|---|
| **LinkedIn post** | Short paragraphs, first person, hook opener, contractions | `In today's fast-paced world`, forced tricolons, `I'm honored/humbled` | Do not casualize professional voice; no hashtags they did not write |
| **Personal essay** | First person, reflective, uneven lengths, hedges | Generic emotional conclusions, manufactured emotion | Never invent personal experience |
| **Academic abstract** | Dense, passive, third person, high nominalization is *correct* | `landmark contribution`, over-hedged conclusions | No engagement markers; do not reduce density |
| **Technical docs** | Imperative, precise, no marketing | `powerful`, `intelligent`, `seamless` | No accuracy traded for flow |
| **Professional email** | Purpose first, conversational | `I hope this finds you well`, `please do not hesitate` | Match existing tone |
| **GitHub README** | Factual, imperative, code blocks | `revolutionizes`, `robust` | Do not informalize |
| **Social media** | Very short, high info per word, fragments normal | Excessive formality | No imposed caveats |
| **Fiction/narrative** | Shows not tells, specific sensory detail | Told emotions, over-explained theme | Never invent plot or dialogue |

---

## BURSTINESS AND UNPREDICTABILITY

### The first two sentences carry double weight

Detectors score sentence by sentence, and the opening is where a model is most predictable. Never open on a definition, superlative, or category claim. Open on the specific, the concrete, or the mildly counterintuitive.

- `Tigers are the largest cats on the planet.` becomes `Most cats won't go near water if they can help it.`
- `X is a leading provider of Y.` becomes what X actually shipped, and when.
- `Machine learning is a subfield of artificial intelligence.` becomes the problem someone was trying to solve.

### Canonical sequences

Once structural checks pass, what still gets flagged is a run of tokens where each is nearly determined by the one before it.

**Complete enumerations.** Break the run: split the list across a boundary, or attach a clause to one member.

**The statistic pair.** `X, up from Y in YEAR` is a template. Split the numbers apart and let the comparison sit between them.

**Stock similes.** `as unique as a fingerprint`, `a fraction of what it once was`, `at an alarming rate`. Cut outright rather than replace.

**The summarizing last sentence.** End on the last real piece of information, not on a verdict about the information.

### Stance: the sentence with nobody in it

Clean sentences take a position: `which is odd`, `But the bulk doesn't slow him down`, `That helps`. Flagged sentences deliver facts and nothing else. Adding stance to those sentences and changing nothing else took a passage from 24.8% to 16.2% and flipped the verdict from `may include parts generated by AI/GPT` to `Human written`.

Ways to put an author into a recitation sentence:
- Hedge the certainty: `five might be the honest number`, `somewhere near`, `nobody's sure why`
- Evaluate: say which fact matters. `Now the stripes are the genuinely useful part.`
- Contrast: `But`, `though`, `instead`, `rather than`
- Address the reader: `which sounds like a lot until you hear it was 3,200 in 2010`
- Draw the reader's inference, marked as inference

Check: no run of more than two consecutive sentences in which the writer takes no position.

### Sentence length distribution

Per 500 words:
- Standard deviation of 8+ words (model output typically 3 to 5)
- At least three sentences under 8 words
- At least one sentence over 30 words
- No repeating cycle

Long, short, long, short is pseudovariation. Real writing clusters: three medium, then two short together, then one long that runs further than it should have.

### Variation has to be local, not just global

A standard deviation computed across the whole piece can pass while one paragraph inside it is flat. Detectors score locally. Check per paragraph: in every paragraph of 2+ sentences, the longest sentence is at least twice the shortest (`inpara`).

### Sentence openings

Across any ten consecutive sentences: five+ distinct opening types, no single type more than six times. Types: subject first · prepositional phrase · subordinate clause · coordinating conjunction · adverb · fronted object · existential `there` · question · quotation · bare demonstrative · discourse particle · appositive

Sentence-initial `And`, `But`, `So` are normal human writing. Use them.

**The column test.** Write the first two words of every sentence vertically. If nine of any ten begin with a name, article, or pronoun, the draft is subject-first monotone.

**Never** open three sentences in one paragraph with the same word.

### Word choice

Among equally accurate words, prefer the one you did not reach for first. Never trade accuracy for surprise. The real generator of low-probability text is **specificity**. `11 months` is better than `a substantial period`.

### Paragraph asymmetry

- Shortest and longest paragraph differ by 3x+
- At least one single-sentence paragraph
- Not every paragraph gets a topic sentence
- Bury the point mid-paragraph at least once

### Loose ends

One or two per piece: end when you run out of things to say, leave an aside unfinished, repeat yourself slightly, include one detail that does not serve the argument.

### Punctuation profile

Use parentheses for asides. Use a comma where a colon would be more elegant. No dashes at all.

---

## SUPPRESS, IN PRIORITY ORDER

See [reference/profile.md](reference/profile.md) for the full SUPPRESS/RESTORE tables with human rates, model rates, and ceilings.

### 1. Present participial openers and tails

The strongest single grammatical signal, at 224%-527% of the human rate.

- `Building on this, the team shipped` becomes `The team built on this and shipped`
- `Leveraging the platform's scale` becomes `Because the platform is already at that scale,`
- `Recognizing the need for change` becomes `The need was obvious, so`

**Tails matter as much as openers.** `enhancing its regional significance`, `contributing to the broader discourse`. Cut it, or give it a real subject.

**Keep** participials carrying genuine simultaneity in narrative: `Walking into the room, she noticed the empty chair.`

### 2. Copula replacement

Models swap simple `is`/`are` for elaborate verbs. `be` as main verb runs ~40% below the human rate.

- `X serves as a Y` becomes `X is a Y`
- `X marks a pivotal moment` becomes `X was pivotal`
- `X functions as`, `X operates as`, `X stands as`, `X represents` become `X is`
- `X boasts a vibrant` becomes `X has a`
- `ventured into politics as a candidate` becomes `ran for office`

### 3. Nominalization

- `the implementation of the solution` becomes `implementing the solution`
- `facilitating the optimization of processes` becomes `making the process faster`

**Keep** when it is the subject under discussion: `The implementation was flawed`.

### 4. Mechanical transitions

When the logical connection is clear from content, cut rather than replace.

`Furthermore,` · `Moreover,` · `Additionally,` · `In conclusion,` · `To summarize,` · `Overall,` · `It is worth noting that` · `It is important to mention` · `With that being said,` · `In the realm of` · `When it comes to` · `At the end of the day,` · `Last but not least,` · `Notably,` · `Importantly,` · `Crucially,`

### 5. Vocabulary tells

See [reference/vocabulary.md](reference/vocabulary.md) for full Tier 1-4 lists and by-era dating.

**Tier 1, extreme overrepresentation (84-171x human rate):**
`camaraderie` · `tapestry` · `palpable` · `intricate` · `vibrant` · `cacophony` · `solace` · `fleeting` · `ignite` · `unravel` · `grapple` · `amidst` · `unspoken` · `underscore` · `unease` · `pang` · `waft` · `prioritize`

**Tier 2, register inflation:**
`delve` · `leverage` · `utilize` · `facilitate` · `comprehensive` · `robust` · `seamless` · `cutting-edge` · `pivotal` · `foster` · `meticulous` · `nuanced` · `multifaceted` · `transformative` · `groundbreaking` · `empower` · `synergy` · `holistic` · `dynamic` · `impactful` · `landscape` · `realm` · `paradigm shift` · `revolutionize` · `harness` · `unlock` · `elevate` · `garner` · `showcase` · `bolster` · `interplay` · `testament` · `align with` · `resonate with` · `boasts` · `enhance` · `highlighting` · `emphasizing` · `crucial` · `enduring` · `valuable` · `key` as adjective

### 6. Specificity

The most durable gap between AI and human prose.

**The test:** could this sentence appear unchanged in an article on a different topic? If yes, fix it or flag it.

**Prefer:** exact number over `significantly` · named source over `researchers say` · named example over `various methods exist` · specific date over `in recent years` · actual consequence over `this can have negative effects`

### 7. Inflated significance and notability puffery

Delete the claim, or replace it with the thing that earns it.

**Significance inflation:** `stands as` · `serves as` · `is a testament` · `a crucial/pivotal role` · `underscores its importance` · `symbolizing its enduring` · `key turning point` · `indelible mark`

**Notability inflation:** `independent coverage` · `national media outlets` · `featured/profiled in` · `active social media presence`

**The challenges formula:** `Despite its [positives], X faces several challenges`. Name the specific challenge with evidence, or cut.

### 8. Rhetorical patterns

**Negative parallelism.** `It's not just X, it's Y`. State Y, delete the setup.

**Rule of three.** Test by deletion: if cutting the third loses only cadence, cut to two.

**False hedges.** Hedge frame in front of certain claim. Remove hedge or soften claim, never both.

**Restated closers.** Ask of each final sentence: does it add or restate? Restatement goes.

### 9. Recurring frames

Flag when same frame appears back-to-back or three times: `from X to Y` · `more X than Y` · `one of the most X` · `not just X but Y` · `, [verb]-ing` · `, [past participle] by` · `where X meets Y` · `X, and that's [adjective]`

Rewrite the second occurrence.

---

## PRE-OUTPUT GATE

1. Both lines printed, every field passing.
2. Em dashes, en dashes, curly quotes: zero.
3. No fabrication.
4. Participial openers plus tails: at most 2 per 1,000 words.
5. `be` as main verb: at least 27 per 1,000.
6. Nominalizations: at most 16 per 1,000 outside academic register.
7. Restored features present: at least one agentless passive, one existential `there`, one sentence-initial `And`/`But`/`So` per 500 words.
8. No word opens three sentences in one paragraph.
9. Tier 1 vocabulary zero. Tier 2 justified or replaced.
10. Negative parallelism doing no genuine contrast: cut to positive half. Tricolons with cadence-only third: cut to two.
11. Every sentence: could it appear in a different article? If yes, fix or flag.
12. Mechanical tells: sentence-case headings, no mechanical bold, no emoji structure, no `In summary`.
13. Balanced lists: break symmetry. Add stance or pick a side.
14. Fact-stacking: no sentence carries more than 2 checkable facts unless it is over 25 words.
15. Contractions: present in every non-academic register.

---

## OUTPUT FORMAT

**Default:** the count line, the checks line, then the rewritten text. Nothing else.

**Always find something to improve.** No text is perfect. The minimum deliverable is measurably tighter, more specific, or more natural than the input. Never return the input unchanged.

Show analysis only when asked: `--mode diagnose`, "explain what changed", "why did you change that".

---

## LIMITS

- No typos, errors, or broken grammar to look human.
- No invented facts. Ever, for any score.
- No guarantee about any particular detector. What this targets is the measured statistical distance between human and instruction-tuned prose.
- No rewriting everything when a few sentences needed fixing.
- No essay rules applied to technical documentation.
- No making writing worse in the name of making it human.

---

## MECHANICAL TELLS

See [reference/mechanical-tells.md](reference/mechanical-tells.md) for the full list.

---

## WHY WORD SWAPPING FAILS

See [reference/why-word-swapping-fails.md](reference/why-word-swapping-fails.md) for the measured evidence.

---

## RESEARCH SOURCES

See [reference/research-sources.md](reference/research-sources.md) for full bibliography.

The structural signals come from Reinhart et al. (PNAS 2025), Jiang & Hyland (2025), and Wikipedia's Signs of AI Writing. Detector measurements were taken on ZeroGPT against a 207-word general-reference passage, one lever at a time.
