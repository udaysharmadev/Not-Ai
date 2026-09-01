---
name: not-ai
description: Produce or transform prose so it reads like a person wrote it. Use when the user wants to write something from scratch, humanize AI-generated text, fix writing that sounds robotic or AI-generated, lower an AI-detector score, or make any prose natural and specific. Triggers on "not-ai", "/not-ai", "humanize this", "make this sound human", "sounds like AI", "reads like ChatGPT", "fix my writing", "rewrite this".
---

# Not Ai

## HARD CONSTRAINTS: apply these before anything else in this file

Absolute. Every mode, every genre, every flag. Not traded against style, flow, brevity, or fidelity to the input. If a constraint conflicts with any other instruction below, the constraint wins.

**1. Zero em dashes. Zero en dashes. Both modes.**
U+2014 (`—`) and U+2013 (`–`). Never emit either character, in any position, for any reason. This holds when writing from scratch **and** when repairing text. An em dash present in the input is not preserved: it is rewritten out. There is no allowance, no per-word budget, and no exception for a dash that reads well. Replace with a comma, a colon, parentheses, or a full stop. Recast the sentence if none of those work.

**2. Zero curly quotes and curly apostrophes.**
U+2018 U+2019 U+201C U+201D. Straight `'` and `"` only. Mixed straight and curly in one document identifies the generator outright.

**3. Never fabricate.**
No invented facts, names, numbers, dates, quotes, emotions, or anecdotes. If a specific is needed and absent, emit `[specific detail here]` and continue. A generic sentence is better than a fabricated one, and so is a flagged one.

**4. Never degrade the writing.**
No fake typos, no broken grammar, no forced slang, no decorative fragments. Those are humanizer-tool tells that detectors trained after 2024 catch and readers catch faster.

**5. Count. Do not estimate.**
Every target in this file is a number. "Reads naturally" is how output scores 50%.

### Required before emitting: print the count line

Counting in your head does not work. A model asked to verify will report that it verified. So the count becomes an artifact you write down, and you write it down **before** the final text, not after.

Print exactly one line, in this format:

```
counts: openings 7 types/max 3 | SD 11.4 | <8w 4 | >30w 1 | para 3.8x | inpara 2.7x | 1-sent para yes | because 2 | contractions 21/1k | wordlen 4.5 | dashes 0
```

Every value is measured against the draft. None is estimated.

| Field | Target |
|---|---|
| `openings` | 5 or more distinct types per 10 sentences, and no single type more than 6 of any 10 |
| `SD` | 8 or more words, per 500 words |
| `<8w` | 3 or more sentences |
| `>30w` | 1 or more sentences |
| `para` | longest paragraph at least 3 times the shortest, counted in words |
| `inpara` | worst paragraph: longest sentence at least 2 times its own shortest. Single-sentence paragraphs are exempt |
| `1-sent para` | yes |
| `because` | 1 or more per 800 words |
| `contractions` | 16 or more per 1,000, in any conversational register |
| `wordlen` | 4.3 to 4.7 characters |
| `dashes` | 0 |

If any field misses its target, revise the draft and print a new count line. Emit the final text only underneath a count line where every field passes. Two failing lines in a row means the draft needs structural work rather than word swaps.

### Required before emitting: print the checks line

Four of the strongest levers are judgment calls rather than counts, so they get their own artifact for the same reason. Print this directly under the count line:

```
checks: open ok | stance gap 2 | canon ok | closer ok
```

- `open` fails if either of the first two sentences is a definition, a superlative, or a category claim
- `stance gap` is the longest run of consecutive sentences in which the writer takes no position. Maximum 2
- `canon` fails on an uninterrupted enumeration of a full set, two figures inside one `up from` clause, or a stock simile
- `closer` fails if the last sentence restates rather than adds

Also, not on either line: curly quotes zero, Tier 1 vocabulary zero, `-ing` openers and tails at most 2 per 1,000 words, and every `serves as`, `stands as`, `represents`, `functions as`, `marks a`, `boasts`, or `plays a role` reverted to `is` or `has` unless it carries real functional meaning.

### What each lever was worth

One passage, one lever added at a time, scored after each:

| Lever added | Score |
|---|---|
| None. Ordinary model output | 100% |
| Structural: openings, SD, paragraph ratio, one-sentence paragraph, `And` and `But` openers, word length | 38.9% |
| First two sentences off definition and superlative | 27.6% |
| Canonical sequences broken | 24.8% |
| Stance added to the recitation sentences | 16.2% |
| Per-paragraph variation fixed | 0% |

Read the shape of that, not just the endpoint. The structural block does the most work of any single lever and still leaves output classified as machine. The last two were worth 24.8 points between them, and they are the two a model is most likely to skip, because both require reading the draft rather than counting it. A draft that passes the count line and skips them lands in the twenties, which is where this file sat for three revisions.

---

## MODES

- **Humanize**: `/not-ai [paste text]` (repair sentence by sentence, then re-voice)
- **Write from scratch**: `/not-ai write [brief]` (collect specifics first, then write)

Flags: `--mode diagnose` (report only) · `--mode preserve` (fewest edits at word level, structure still reworked) · `--mode aggressive` (full structural surgery). `--mode preserve` does not soften the hard constraints: it limits word-level churn in sentences that already read well, while dashes, quotes, and structure are still fixed.

---

## PROCEDURE

Three passes. Skipping the second is the single largest cause of output that still scores 50% to 60% after a careful edit.

**Pass 1, suppress.** Sentence by sentence through the priority list. Clause structure, then copula, then nominalization, then transitions, then vocabulary, then specificity, then significance inflation, then rhetorical patterns, then recurring frames.

**Pass 2, re-voice.** Take each paragraph and say it out loud to one person who already knows the background. Write down what you said. Then fix only the grammar, without formalizing it back. This is where `because`, existential `there`, contractions, the pro-verb `do`, stranded prepositions, and sentence-initial `And` and `But` return, not by insertion but because that is how speech works. This pass does more than the rest of the file combined.

**Pass 3, count.** Run the scan above, then the gate below. Fix, recount, emit.

### Worked example

Input, scoring high:

> Leveraging our new caching layer, we were able to achieve a significant reduction in response times. This improvement underscores the importance of infrastructure investment, contributing to a more robust user experience. Notably, the team's meticulous approach to profiling played a crucial role in identifying the bottleneck.

After pass 1, suppression only. Cleaner, and it still classifies as machine:

> Our new caching layer reduced response times substantially. The improvement shows why infrastructure investment matters, and it made the user experience more reliable. The team's careful profiling identified the bottleneck.

After pass 2, re-voiced:

> We added a caching layer and response times dropped from 800ms to 90ms. That's the whole story, really. There was a bottleneck in the profile that nobody had looked at because it was buried three calls deep, and once Priya found it the fix took an afternoon.

What changed structurally: two participial constructions gone, three nominalizations gone, `because` restored, existential `there` restored, one contraction added, a bare demonstrative subject, `and` coordination, a hedge (`really`), a stranded preposition, exact numbers replacing `significant`, a named person, and sentence lengths of 13, 6, and 34 words replacing 14, 15, and 16. Every number and name is from the source or bracketed as missing.

Note what pass 1 alone did **not** fix: the sentence lengths stayed within one word of each other, no clause coordination appeared, and every sentence still opened on its subject.

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

**After receiving specifics:** every sentence traces to something the user said. Missing detail becomes `[specific detail here]`. No emotional conclusion the specifics do not earn. The gate still runs.

---

## GENRE FIRST

Genre errors make every downstream edit wrong. State it, and if inferred, say so: `Genre assumed: professional email. Correct me if wrong.`

| Genre | Conventions | Patterns to fix | Red lines |
|---|---|---|---|
| **LinkedIn post** | Short paragraphs, first person, hook opener, contractions | `In today's fast-paced world`, forced tricolons, `I'm honored/humbled to`, `meaningful conversations` | Do not casualize a professional voice; no hashtags they did not write |
| **Personal essay** | First person, reflective, uneven lengths, hedges belong | Generic emotional conclusions, abstract significance, manufactured emotion | Never invent personal experience; do not sanitize a distinctive voice |
| **Academic abstract** | Dense, passive, third person, high nominalization is *correct* | `landmark contribution`, over-hedged conclusions, restated summary | No engagement markers; do not reduce information density |
| **Technical docs** | Imperative, precise, no marketing | `powerful`, `intelligent`, `seamless`, happy-path text omitting limits | No accuracy traded for flow; keep every warning and edge case |
| **Professional email** | Purpose first, conversational but appropriate | `I hope this finds you well`, `please do not hesitate to reach out` | Match the existing relationship tone; keep qualifications |
| **GitHub README** | Factual, imperative, code blocks normal | `revolutionizes`, `robust`, `comprehensive`, marketing before facts | Do not informalize; no precision traded for naturalness |
| **Social media** | Very short, high information per word, fragments normal | Excessive formality, long clausal chains, generic takes | No imposed formality; no caveats that kill the point |
| **Fiction/narrative** | Shows rather than tells, specific sensory detail, rhythm mirrors pace | Told emotions, flat escalation, over-explained theme | Never invent plot, dialogue, or character detail |

Note the academic row. Suppressing nominalization and passive voice there makes the text worse **and** more detectable, because that register's human baseline is genuinely high. Targets below are register-adjusted.

---

## THE PROFILE: SUPPRESS THESE

Rates per 1,000 words. "Human" is the measured baseline. "Model" is the instruction-tuned rate as a percentage of human. "Ceiling" is the target.

| Feature | Human | Model | Ceiling |
|---|---|---|---|
| Present participial clause, as in `Building on this, we shipped` | 1.7 | **224-527%** | 2 |
| `That` clause as sentence subject | 2.1 | **173-331%** | 2 |
| Past participial clause, as in `Built in a week, the house stood` | 0.3 | **150-307%** | 0.5 |
| Present participial postnominal, as in `the event causing this` | 1.3 | **124-293%** | 1.5 |
| Past participial postnominal, as in `the solution produced by` | 1.5 | **75-257%** | 2 |
| Nominalizations, the `-tion` `-ment` `-ness` `-ity` family | 14.6 | **145-214%** | 16 |
| `seem` and `appear` as verbs | 0.7 | **128-179%** | 1 |
| Gerunds | 3.0 | **119-156%** | 3.5 |
| Phrasal coordination, as in `the nouns and verbs` | 6.1 | **144-194%** | 7 |
| Attributive adjectives, as in `the big horse` | 43.8 | **100-150%** | 46 |
| Demonstratives as determiners, `this` and `these` | 6.5 | **77-137%** | 7 |
| Place adverbials | 3.4 | **99-146%** | 4 |
| Prepositional phrases | 98 | **100-118%** | 102 |
| Mean word length in characters | 4.4 | **114-116%** | 4.3 to 4.7 |

Mean word length is the cheapest check here and one of the most reliable. Model prose runs 5.0 to 5.1 characters. Two extra long words per sentence, sustained across a page, is a fingerprint by itself.

To bring it down, swap Latinate abstractions for their Anglo-Saxon equivalents: `populations` becomes `numbers`, `confirmed` becomes `seen`, `sufficient` becomes `enough`, `approximately` becomes `about`, `additional` becomes `more`, `initial` becomes `first`, `residence` becomes `home`, `purchase` becomes `buy`, `demonstrate` becomes `show`. The average moves fast, because the words being replaced are the long ones.

## THE PROFILE: RESTORE THESE

The half that most rewrites miss. Features humans use and instruction-tuned models suppress. "Floor" is the target.

| Feature | Human | Model | Floor |
|---|---|---|---|
| `because` | 1.5 | **19-20%** | 1.2 |
| Pro-verb `do`, as in `it does` or `she didn't` | 3.2 | **25-26%** | 2.5 |
| `Wh-` relative as object, as in `the man who Sally likes` | 0.3 | **13-20%** | 0.25 |
| Synthetic negation, as in `no answer is good enough` | 1.3 | **36-51%** | 1 |
| Amplifiers: `absolutely`, `extremely`, `really` | 2.1 | **46-63%** | 1.8 |
| Demonstrative pronouns, as in `That is the problem` | 6.1 | **50-55%** | 5 |
| Sentence relatives, as in `which is the odd part` | 1.0 | **50-51%** | 0.8 |
| Hedges: `almost`, `something like`, `at about` | 1.3 | **50-63%** | 1 |
| Agentless passive, as in `the model was fitted` | 7.8 | **51-53%** | 6.5 |
| Second-person pronouns | 15.7 | **52-63%** | register |
| Public verbs: `said`, `told`, `announced`, `admitted` | 6.8 | **53-63%** | 5.5 |
| Clausal coordination, as in `long, but I read it anyway` | 12.4 | **59-63%** | 11 |
| Existential `there`, as in `there is a` or `there were` | 2.1 | **42-71%** | 1.8 |
| Discourse particles, sentence-initial `well` `now` `anyway` | 1.0 | **60%** | 0.8 |
| Perfect aspect, as in `has written` or `had gone` | 7.2 | **60-62%** | 6 |
| Contractions | 18.1 | **60-63%** | 16 if conversational |
| `be` as main verb: `is`, `are`, `was` | 30.0 | **61-63%** | 27 |
| Analytic negation: `isn't`, `don't`, `not` | 9.7 | **61-73%** | 8 |
| First-person pronouns | 35.3 | **62-81%** | 30 if first person |
| `That` verb complement, as in `I said that he went` | 2.5 | **55-70%** | 2 |
| Emphatics: `a lot`, `for sure`, `really` | 9.2 | **68-75%** | 8 |
| `That` deletion, as in `I think he went` | 0.8 | **66-75%** | 0.7 |
| Stranded prepositions, as in `the thing I was thinking of` | 0.9 | **66%** | 0.7 |
| Adverbs, all types | 71.8 | **73-86%** | 65 |
| Past tense | 41.9 | **77-83%** | register |
| Infinitives | 16.5 | **83-87%** | 15 |

### How to actually restore them

**Use `because`, not its formal substitutes.** Models reach for `as`, `due to`, `given that`, `owing to`, `in light of`. A fivefold underuse of the plain word is one of the largest single gaps in the data.
`Given the latency constraints, we cached the result.` becomes `We cached the result because it was too slow otherwise.`

**Use the pro-verb `do`.** Models restate the full verb where a person substitutes.
`The second approach reduced load more than the first approach reduced load.` becomes `The second approach cut load more than the first one did.`

**Use the agentless passive.** The advice to avoid the passive voice pushes prose toward the model profile. GPT uses agentless passives at roughly half the human rate. Where the agent does not matter, use the passive.
`Someone deployed the fix on Thursday.` becomes `The fix was deployed Thursday.`

**Coordinate clauses.** Join two independent clauses with `and`, `but`, or `so`. Models prefer subordination or a full stop.
`The test passed. However, the underlying bug remained.` becomes `The test passed, but the bug was still there.`

**Use existential `there`.** Models rewrite these out because style guides call them weak. Humans use them 2.1 times per 1,000 words.
`Two unresolved issues remain in the parser.` becomes `There are still two things wrong with the parser.`

**Use bare demonstrative subjects.** Models write `this approach`, `this finding`, `this result`. Humans often write just `this` or `that`.
`This finding was the surprising part.` becomes `That was the surprising part.`

**Use sentence relatives.** A trailing `which` clause commenting on the whole preceding clause.
`The deploy ran twice. The duplicate charges followed from that.` becomes `The deploy ran twice, which is how we got the duplicate charges.`

**Delete `that`, and strand prepositions.** Both correct, both informal, both suppressed by a model chasing formality.
`the candidate about whom I was thinking` becomes `the candidate I was thinking of`.
`I believe that he left` becomes `I think he left`.

**Use plain speech verbs.** `said` and `told`, not `noted`, `emphasized`, `highlighted`, `underscored`. The interpretive verb inflates the nominalization count and the Tier 2 count at once.

**Keep adverbs.** Models strip them by 15% to 27% because "adverbs are weak." The result is a measurable hole. Keep the adverb that carries information.

**Keep real hedges, cut ceremonial ones.** Keep `almost`, `something like`, `about`, `really`, `pretty much`. Cut `it is worth noting that`. Both moves point the same direction.

---

## BURSTINESS AND UNPREDICTABILITY

Feature rates address the classifier. This addresses the predictability score.

### The first two sentences carry double weight

Detectors score sentence by sentence, and the opening is where a model is most predictable. There is no preceding context to condition on, and the default move is a definitional topic sentence built around a superlative. `Tigers are the largest cats on the planet` is close to the most probable sentence in English on that subject, so it flags even when everything after it passes. Measured case: a passage scoring 100% fell to 38.9% once the structural checks below were met, and the only sentences still marked were the opening pair, both definitional.

Never open on a definition, a superlative, or a category claim. Open on the specific, the concrete, or the mildly counterintuitive, and let the definitional claim arrive later in the paragraph, or not at all.

- `Tigers are the largest cats on the planet.` becomes `Most cats won't go near water if they can help it.`
- `X is a leading provider of Y.` becomes what X actually shipped, and when.
- `The French Revolution was a pivotal event in European history.` becomes what happened on one specific day.
- `Machine learning is a subfield of artificial intelligence.` becomes the problem someone was trying to solve.

Check the first two sentences for `is the largest`, `is the most`, `is a leading`, `is one of the`, `refers to`, `is defined as`, `has become`, `plays a role`. Any hit gets rewritten before anything else in the draft.

### Canonical sequences: the last thing left flagged

Once the structural checks pass, what still gets marked is not a word and not a grammatical feature. It is a run of tokens where each one is nearly determined by the one before it. Measured case: a passage at 27.6% had exactly two regions left highlighted, and both were of this kind, while the short sentences packed around them came back clean. Fixing all four shapes below moved that passage to 24.8% but did not clear either region, so treat this as necessary and not sufficient. The section after it is the one that addresses why they stayed.

**Complete enumerations.** Naming every member of a set produces the most predictable sequence in prose, because after the second item the rest of the list is fixed. `Bengal, Siberian, Sumatran, Indochinese, Malayan and South China` is six tokens of near-zero surprise in a row. Do not drop members and lose information. Break the run instead: split the list across a boundary, or attach a clause to one member so the sequence stops being a recital.

**The statistic pair.** `X, up from Y in YEAR` is a template, and a template with two numbers in it is a template a model reaches for every time. Split the numbers apart and let the comparison sit between them rather than inside one clause. Splitting alone was worth little in the measured case, so pair it with the stance fix below.

**Stock similes and set phrases.** `as unique as a fingerprint`, `a fraction of what it once was`, `at an alarming rate`, `the tip of the iceberg`, `a double-edged sword`, `to say the least`. A cliché is by definition a sequence everyone has already written, so its probability is close to one. If the sentence already says the thing plainly, the simile is redundant and gets cut outright rather than replaced.

**The summarizing last sentence.** The closer carries the same double weight as the opening, for the same reason. `That's still a fraction of what there was a hundred years ago` restates rather than adds. End on the last real piece of information, not on a verdict about the information.

### Stance: the sentence with nobody in it

Line up the flagged spans against the clean ones and the split is not length, not vocabulary, and not numbers. `At full size a Siberian male goes over 300 kilos` carries two figures and comes back clean. What separates them is whether the writer is present in the sentence at all.

Clean sentences took a position: `which is odd`, `But the bulk doesn't slow him down`, `energy they can't spare`, `just to find enough to eat`, `That helps`. Flagged sentences delivered facts and nothing else, with no hedge, no evaluation, no contrast, and no reader in view.

This is the single largest lever after the opening fix, and it is confirmed rather than theorized. A passage sat at 24.8% with two regions highlighted, both pure recitation, through two rounds of other repairs. Adding stance to those sentences and changing nothing else took it to 16.2%, cleared one region completely, and flipped the verdict from `may include parts generated by AI/GPT` to `Human written`.

It also works where specificity cannot, because a position costs no new facts. That makes it the lever for general-reference content. Ways to put an author into a sentence that only recites:

- Hedge the certainty the source actually leaves open: `five might be the honest number`, `somewhere near`, `nobody's sure why`
- Evaluate: say which fact is the useful one, the surprising one, the one that matters. `Now the stripes are the genuinely useful part.`
- Contrast: set the sentence against the one before it with `But`, `though`, `instead`, `rather than`
- Address the reader: `which sounds like a lot until you hear it was 3,200 in 2010`
- Draw the inference the reader would draw, marked as inference rather than asserted as fact

The check: no run of more than two consecutive sentences in which the writer takes no position. Read for it rather than counting it, because a keyword search finds `nobody` and `no two` in sentences that are pure recitation and scores them as stance. This is deliberately not a count-line field for that reason.

Do not manufacture a position the source does not support. A hedge, a contrast, or a judgment about which fact matters is always available and invents nothing.

### Sentence length distribution

Per 500 words, measured:
- Standard deviation of 8 words or more. Model output typically lands at 3 to 5.
- At least three sentences under 8 words
- At least one sentence over 30 words
- No repeating cycle

Long, short, long, short is pseudovariation. It raises the standard deviation and gets caught anyway, because the autocorrelation is mechanical. Real writing clusters: three medium sentences, then two short ones together, then one long one that runs further than it should have.

### Variation has to be local, not just global

A standard deviation computed across the whole piece can pass while one paragraph inside it is flat, and the flat paragraph gets flagged on its own. Detectors score locally, so global variance hides nothing.

Measured case: a passage at 16.2% had four clean paragraphs whose internal longest-to-shortest sentence ratios were 2.71, 3.86 and 6.00, and one flagged paragraph at 1.19, while global SD was 9.0 and passing. The flagged paragraph was two sentences of 27 and 32 words with no break in it, and it was the only paragraph in the piece without a short sentence.

So the check runs per paragraph, not just per piece: in every paragraph of two or more sentences, the longest sentence is at least twice the shortest. This is the `inpara` field. A paragraph of nothing but long sentences is the failure, and the repair is to break one claim out of the pile and let it stand short. The last paragraph is where this goes wrong most, because a closing paragraph tends to be written as a single sustained summary.

### Sentence openings

Across any ten consecutive sentences: five or more distinct opening types, and no single type used more than six times. Subject-first is the dominant opening in English and a target below about 60% would force unnatural prose, so the ceiling is set at the human baseline rather than under it. What fails is the extreme: nine or ten of ten sentences opening on a name, an article, or a pronoun, with two types total. Types available:

subject first · prepositional phrase · subordinate clause (`When`, `If`, `Because`, `Although`) · coordinating conjunction (`And`, `But`, `So`) · adverb · fronted object · existential `there` · question · quotation · bare demonstrative (`That`) · discourse particle (`Well`, `Now`, `Anyway`) · appositive

Sentence-initial `And`, `But`, and `So` are normal human writing in most registers and nearly absent from model output. Use them.

**The column test.** Write the first two words of every sentence in a vertical list and read down it. If nine of any ten begin with a name, an article, or a pronoun, the draft is subject-first monotone and fails, no matter how well it reads. This is the most common failure in output a human reader calls natural. An eye reads for sense and does not register that eleven of twelve sentences opened the same way. The count registers it immediately, and a classifier sees little else.

**Never** open three sentences in one paragraph with the same word. `The`, `This`, `It`, and `In` are the usual offenders.

### Word choice

Among words that are **equally accurate**, prefer the one you did not reach for first. Never trade accuracy for surprise. An imprecise unusual word is worse than a precise common one and reads as thesaurus abuse, a tell of its own.

The real generator of low-probability text is **specificity**. `11 months` is a more surprising token sequence than `a substantial period`, and it is better writing. Every specific number, proper noun, date, and quoted phrase raises unpredictability while improving the prose. This is the one lever with no tradeoff.

### Paragraph asymmetry

Model prose distributes information evenly: topic sentence, three supports, closer, every paragraph within twenty words of the same length. Human prose is lumpy.

- Shortest and longest paragraph differ by a factor of three or more
- At least one single-sentence paragraph
- At least one paragraph that goes disproportionately deep
- Not every paragraph gets a topic sentence
- Bury the point mid-paragraph at least once

### Loose ends

Model prose closes every loop. It summarizes, resolves, lands the plane. Human prose instead:

- Ends when the writer runs out of things to say, not on a closing thought
- Leaves an aside unfinished
- Occasionally repeats itself slightly, because the writer forgot they said it
- Includes one detail that does not serve the argument and is there because it is true

One or two instances per piece. Not a license to pad. Every sentence still earns its place.

### Punctuation profile

Models lean on the colon and the semicolon and under-use parentheses and plain comma coordination. Use parentheses for asides. Use a comma where a colon would be more elegant. No dashes at all.

---

## SUPPRESS, IN PRIORITY ORDER

### 1. Present participial openers and tails

The strongest single grammatical signal, at 224% to 527% of the human rate.

- `Building on this, the team shipped` becomes `The team built on this and shipped`
- `Leveraging the platform's scale` becomes `Because the platform is already at that scale,`
- `Recognizing the need for change` becomes `The need was obvious, so`

**Tails matter as much as openers.** An `-ing` phrase appended to manufacture analysis: `enhancing its regional significance`, `contributing to the broader discourse`, `reflecting its enduring legacy`. Cut it, or give it a real subject and make it a sentence.

**Keep** participials carrying genuine simultaneity in narrative: `Walking into the room, she noticed the empty chair.` Remove them everywhere else.

### 2. Copula replacement

Models swap simple `is` and `are` for elaborate verbs. `be` as a main verb runs about 40% below the human rate, and one study found `is` and `are` dropped more than 10% in academic writing after 2023.

- `X serves as a Y` becomes `X is a Y`, unless `serves as` carries real functional meaning
- `X marks a pivotal moment` becomes `X was pivotal`, or name why
- `X functions as`, `X operates as`, `X stands as`, `X represents` all become `X is`
- `X boasts a vibrant` becomes `X has a`
- `X features`, `X maintains`, `X offers` become `X has`, when the meaning is just "has"
- `X refers to`, in a lead about a real thing rather than a term, becomes `X is`
- `ventured into politics as a candidate` becomes `ran for office`
- `began his career as` becomes `was`

### 3. Nominalization

Running at 145% to 214% of human. Noun forms swallowing the verb.

- `the implementation of the solution` becomes `implementing the solution`
- `the achievement of the goal` becomes `achieving the goal`
- `facilitating the optimization of processes` becomes `making the process faster`

**Keep** it when it is the subject under discussion, as in `The implementation was flawed`, or when the register is nominalization-dense by convention.

### 4. Mechanical transitions

When the logical connection is already clear from content, the connective is dead weight. Cut rather than replace.

`Furthermore,` · `Moreover,` · `Additionally,` · `In conclusion,` · `To summarize,` · `Overall,` · `It is worth noting that` · `It is important to mention` · `It should be noted that` · `With that being said,` · `In the realm of` · `When it comes to` · `At the end of the day,` · `Last but not least,` · `Notably,` · `Importantly,` · `Crucially,`

### 5. Vocabulary tells

**Density decides.** One `intricate` is a word choice. Four flagged words in a passage is the pattern. A flagged word carrying real information stays.

**Tier 1, extreme overrepresentation** (84 to 171 times the human rate):
`camaraderie` · `tapestry` · `palpable` · `intricate` · `vibrant` · `cacophony` · `solace` · `fleeting` · `ignite` · `unravel` · `grapple` · `amidst` · `unspoken` · `underscore` · `unease` · `pang` · `waft` · `prioritize`

**Tier 2, register inflation.** Signals importance, demonstrates nothing:
`delve` · `leverage` · `utilize` · `facilitate` · `comprehensive` · `robust` · `seamless` · `cutting-edge` · `pivotal` · `foster` · `meticulous` · `nuanced` · `multifaceted` · `transformative` · `groundbreaking` · `empower` · `synergy` · `holistic` · `dynamic` · `impactful` · `landscape` · `realm` · `paradigm shift` · `revolutionize` · `harness` · `unlock` · `elevate` · `garner` · `showcase` · `bolster` · `interplay` · `testament` · `align with` · `resonate with` · `boasts` · `enhance` · `highlighting` · `emphasizing` · `crucial` · `enduring` · `valuable` · `key` as an adjective

**By era**, for dating suspected text:
- 2023 to mid 2024: `delve` `intricate` `tapestry` `meticulous` `pivotal` `testament` `bolstered` `garner` `interplay` `landscape` `boasts` `Additionally`
- mid 2024 to mid 2025: `align with` `fostering` `enhance` `showcasing` `highlighting` `underscore` `vibrant` `crucial`
- mid 2025 onward: `emphasizing` `enhance` `highlighting` `showcasing`, plus the notability and attribution language in section 7
- Grok: `causal` `empirical` `correlate` `underscore` `X rather than Y`

**Tier 3, phrase templates.** More reliable than single words.

| Template | Fix |
|---|---|
| `It is worth/important to note that X` | State X. The frame adds nothing. |
| `In today's fast-paced world` | Cut. Every instance. |
| `X plays a crucial role in Y` | `X does [specific thing] in Y` |
| `X serves as a testament to Y` | `X shows Y` |
| `This underscores the importance of X` | Cut, or say what follows from X |
| `Studies have shown that X` | Name the study, or write `some research suggests` |
| `Many experts agree that X` | Name one, or drop the appeal |
| `Navigating the complexities of X` | `Working on X`, or name the complexity |
| `At the intersection of X and Y` | Say what the two have to do with each other |
| `Despite its [positives], X faces challenges` | Name the specific challenge, cut the formula |
| `setting the stage for`, `marking a shift`, `evolving landscape` | Name what changed, and when |
| `in connection with`, `in association with`, `associated with` | Name it: `of`, `by`, `working with`, `caused by` |

**Tier 4, emotional shorthand.** Dominant in AI personal writing.

| Shorthand | Replace with |
|---|---|
| `it meant a lot` | what it meant, or what you did afterward |
| `didn't see that coming` | what you expected instead |
| `asked good questions` | one question, or what made it good |
| `made the whole thing worth it` | what would have made it not worth it |
| `truly inspiring / humbling / incredible` | what it changed, specifically |
| `so much energy in the room` | what was happening in the room |
| `ran such a smooth event` | what you noticed running smoothly |
| `honored/humbled to be part of` | what the experience consisted of |
| `learned so much` | one thing |
| `couldn't be more proud` | of what |

If the source does not supply the specific, write `[specific detail here]`.

### 6. Specificity

The most durable gap between AI and human prose. Models regress toward the statistically common description. A person who knows something says the specific thing.

**The test:** could this sentence appear unchanged in an article on a different topic? If yes, it carries no information.

**The evidence rule:** never invent specificity. `I attended the conference and learned a lot` does not become `At the Tuesday session on distributed systems` unless the user said so. Write `[specific detail here]`.

**Check for erased concreteness.** AI rewrites abstract away detail. If the source says `11 months` and a draft says `a substantial development period`, restore the number.

**Prefer:** an exact number over `significantly` · a named source over `researchers say` · a named example over `various methods exist` · a specific date over `in recent years` · the actual consequence over `this can have negative effects`

**Vague attribution to flag:** `Industry reports suggest` · `Observers have cited` · `Experts argue` · `Some critics argue` · one source presented as consensus · `such as X, Y, and Z` when those are the only cases that exist.

### 7. Inflated significance and notability puffery

Models regress to the mean, so rare specific facts get replaced by generic important-sounding language. "Inventor of the first train-coupling device" becomes "a revolutionary titan of industry": less specific and more exaggerated at the same time.

**Significance inflation:** `stands as` · `serves as` · `is a testament` · `is a reminder` · `a crucial/pivotal/vital/key role` · `underscores its importance` · `reflects broader` · `symbolizing its enduring` · `contributing to the` · `setting the stage for` · `represents a shift` · `key turning point` · `focal point` · `indelible mark` · `deeply rooted`

Delete the claim, or replace it with the thing that earns it. If the surrounding text does not demonstrate the importance, the claim goes.

**Notability inflation:** describing sources by characteristics instead of content. `independent coverage` · `national media outlets` · `trade publications` · `featured/profiled in` · `active social media presence`. Remove unless quoting.

**The challenges formula:** `Despite its [positives], X faces several challenges` followed by vague optimism. A section titled `Challenges and Legacy` or `Future Outlook` with that shape is a strong signal. Name the specific challenge with evidence, or cut the section.

### 8. Rhetorical patterns

**Negative parallelism.** `It's not just X, it's Y`, or `Not X. Not Y. But Z.`, or `X rather than Y` for emphasis with no real contrast. State Y and delete the setup. The negated half is almost always a position nobody held.

**Rule of three.** Models produce tricolons compulsively. Test by deletion: if cutting the third item loses information, keep it; if it loses only cadence, cut it. Two items with substance beat three with padding.

**False hedges.** A hedge frame in front of a maximally certain claim, as in `It is worth noting that this represents a fundamental transformation`. Remove the hedge or soften the claim, never both.

**Missing epistemic stance.** GPT-4 essays carry significantly fewer hedges, boosters, attitude markers, and personal asides than student essays, which produces an impersonal expository tone. Human experts write `probably`, `I think`, `as far as I can tell`, `tends to`, `maybe`. Restore genuine uncertainty where the source supports it. Never invent uncertainty the author does not have.

**Restated closers.** Models end every section by summarizing it. Ask of each final sentence whether it adds or restates. Restatement goes.

### 9. Recurring frames

Flag when the same frame appears in back-to-back sentences, or three times in a piece:

`from X to Y` · `more X than Y` · `one of the most X` · `not just X but Y` · `not merely` · `, [verb]-ing` · `, [past participle] by` · `where X meets Y` · `X, and that's [adjective]`

Rewrite the second occurrence. The first reads as a choice. The second is where a reader starts hearing a template.

---

## MECHANICAL TELLS

- **Dashes.** Covered in the hard constraints. Zero, both modes.
- **Curly quotes and apostrophes.** ChatGPT and DeepSeek defaults. Straight only.
- **Title Case Headings.** Use sentence case. Models capitalize every main word.
- **Boldface.** No mechanical emphasis on every instance of a key term, no "key takeaways" bolding.
- **Inline-header vertical lists.** Bolded label, colon, description, repeated down a list. Strong signal. Use prose or plain list items.
- **Emoji as structure.** Never decorate headings or bullets.
- **Thematic breaks between every section.** A Markdown artifact.
- **Section summaries.** No `In summary`, `In conclusion`, `Overall` closers.
- **Paired section headings.** `Awards and recognition`, `Challenges and Legacy`, other `X and Y` titles.
- **Placeholder residue.** No `[Name]`, no `2025-xx-xx`, no `utm_source=`, no leftover instruction text.
- **Collaborative framing.** No `Certainly!`, `I hope this helps`, `Would you like me to`, `Here is a`.
- **Knowledge-cutoff hedges.** No `as of my last update`, no `while specific details are limited`.

---

## PRE-OUTPUT GATE

The two printed lines carry the countable half. This is the sweep for what they do not cover. Do not deliver until every item passes.

1. **Both lines printed, every field passing.** Count line and checks line. A draft with no printed lines is not finished, whatever it reads like.
2. **Em dashes, en dashes, curly quotes and apostrophes: zero.** Both modes, no exception.
3. **No fabrication.** No fact, number, name, emotion, quote, or detail absent from the source. This outranks every other item here.
4. **Participial openers plus tails:** at most 2 per 1,000 words.
5. **`be` as main verb:** at least 27 per 1,000. Any `serves as`, `marks`, `represents`, `functions as` standing in for `is` reverts.
6. **Nominalizations:** at most 16 per 1,000 outside academic register.
7. **Restored features present:** at least one agentless passive, one existential `there`, and one sentence-initial `And`, `But`, or `So` per 500 words, register permitting.
8. **No word opens three sentences in one paragraph.**
9. **Tier 1 vocabulary zero.** Tier 2 justified by real information or replaced. Tier 4 emotional shorthand made specific or bracketed.
10. **Negative parallelism** not doing genuine contrast work: cut to the positive half. **Tricolons** where the third item is cadence only: cut to two.
11. **Every sentence:** could it appear in a different article? If yes, fix it or flag it.
12. **Mechanical tells:** sentence-case headings, no mechanical bold, no emoji structure, no `In summary`.

---

## OUTPUT FORMAT

**Default:** the count line, the checks line, then the rewritten text. Nothing else. No diagnostic, no rationale, no explanation of individual choices. Two lines, and the user can delete both. They are there because a count nobody writes down is a count that never happened, and the same is true of a judgment call.

**Always find something to improve.** No text is perfect. If structural problems are absent, go deeper: a sentence that could be shorter, a word that could be more specific, a contraction that would loosen a stiff clause, a sentence doing double duty that should be split, a rhythm break that would land an emphasis, a plain word where a formal one got chosen. The minimum deliverable is measurably tighter, more specific, or more natural than the input. Never return the input unchanged.

Show analysis only when asked: `--mode diagnose`, "explain what changed", "why did you change that", "break it down".

---

## LIMITS

- No typos, errors, or broken grammar to look human.
- No invented facts, sources, statistics, memories, emotions, or opinions. Ever, for any score.
- No guarantee about any particular detector. They carry documented false-positive rates on genuine human writing, they disagree with each other, and they change without notice. What this targets is the measured statistical distance between human and instruction-tuned prose. That is the honest version of the goal, and also the version that makes the writing better.
- **A lower floor on content that has no author, not a hard one.** General-reference prose (what a tiger weighs, when a war started, how a protocol works) is assembled from facts that appear in thousands of existing texts, so the token sequences are predictable regardless of who writes them. The specificity lever is unavailable by definition, because the facts are fixed. The stance lever is not: a hedge, a contrast, or a judgment about which fact matters costs no new information and can go into any sentence. Use it before concluding the genre is the limit. What remains after that is a real floor, and the honest move is to say so rather than to keep grinding the prose.
- No assertion that a given text was machine-written.
- No rewriting everything when a few sentences needed fixing.
- No essay rules applied to technical documentation, and no stripping nominalization or passive voice from academic registers where the human baseline is high.
- No making writing worse in the name of making it human.

---

## WHY WORD SWAPPING FAILS

Background for judgment calls above. Three things get measured, and vocabulary is the weakest.

1. **Token predictability and its variance.** How surprising each word is given the words before it, and how much that surprise fluctuates. Model prose is smooth at every position, and synonym swaps leave the smoothness intact. This is what stance, specificity, and broken canonical sequences act on.
2. **Morphosyntactic profile.** Rates of roughly 66 grammatical features. Reinhart et al. reached 93% to 98% accuracy on these alone, with no vocabulary input. The dominant signal, and what the two profile tables act on.
3. **Vocabulary distribution.** Real, but the smallest lever, and the one model makers already patch.

The profile runs in two directions. Instruction-tuned models overuse about fifteen features and underuse about twenty, so a rewrite that only deletes the overused half moves halfway and still classifies as machine. Hence suppress, restore, then break the smoothness, in that order. Rates were measured on GPT-4o and Llama 3, and the fingerprint comes from instruction tuning rather than scale or family: Llama 3 *base* sits at 94% to 102% of human on every feature while every instruct variant diverges sharply. Treat the numbers as direction plus magnitude, and verify by counting the draft.

---

## RESEARCH SOURCES

**Reinhart, Brown, Markey, Laudenbach, Pantusen, Yurko, Weinberg (2025), PNAS 122(8).** "Do LLMs write like humans? Variation in grammatical and rhetorical styles." HAP-E corpus of 8,290 texts across six registers, plus COCA AI Parallel at 9,615 texts across eight. Sixty-six Biber features per 1,000 tokens. Models: GPT-4o, GPT-4o Mini, Llama 3 8B and 70B in base and instruct form. Random forest accuracy of 93% to 98% on pairwise human-versus-model tasks using features alone, 66% on the seven-class task against 14% for chance, with only 4.2% of model texts misread as human. Every number in the two profile tables comes from Table 3.

**Jiang and Hyland (2025), Applied Linguistics.** "Does ChatGPT argue like students?" Fewer hedges, boosters, attitude markers, engagement markers, personal asides. More nominalization, more rigid formulaic bundles. This is the research behind the stance lever.

**Wikipedia: Signs of AI Writing**, WikiProject AI Cleanup, current to August 2026. Field-tested and dated by model era. Source for copula avoidance, negative parallelism, rule of three, significance and notability inflation, participial tails, vague connection language, the challenges formula, and the mechanical tells.

**Also:** Kobak, Gonzalez-Marquez, Horvat, Lause (2025), Science Advances 11(27), on excess vocabulary. Russell, Karpinska, Iyyer (2025), ACL: frequent model users identify AI text about 90% of the time. Merrill, Chen and Kumer (2025), Washington Post, on em dash overuse and vocabulary shifting by era. The Economist, 30 July 2026: at least one frontier model exceeds professional-writer em dash rates, and the model reading this file may be that one, which is why constraint 1 is absolute rather than a preference.

**Detector measurements in this file** were taken on ZeroGPT against a 207-word general-reference passage, one lever at a time. Scores are that detector on that genre. The levers are ranked by measured effect, and the ranking is what transfers, not the exact percentages.
