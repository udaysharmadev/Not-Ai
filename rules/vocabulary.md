# Vocabulary

Word-level tells and what to do about each.

Read this last. Vocabulary is the weakest of the signals this skill measures and the easiest to fix in a way that makes writing worse. A text with every flagged word swapped out and its clause structure untouched still reads as machine-written, because a reader responds to sentence shape before word choice. Fix structure first. See `rules/structure.md`.

## Why word lists mislead

Every word below is a real English word that good writers use. None of them is evidence of anything on its own. Three properties decide whether a flagged word is a problem:

**Density.** One instance of `intricate` in 800 words is a word choice. Five instances alongside `tapestry` and `palpable` is a pattern.

**Load.** Does the word carry information, or does it signal quality the surrounding text has not earned? `A comprehensive review of 340 filings` is doing work. `A comprehensive understanding of the challenges` is not.

**Register fit.** `Utilize` is correct in an engineering specification where it means "put to use as a resource" and inflated in an email where `use` was the word.

A flagged word that passes all three stays. Removing it is over-editing.

## Tier 1: measured extreme overrepresentation

Reinhart et al. compared word frequencies between human writers and instruction-tuned models on matched prompts. These appeared in GPT-4o and GPT-4o Mini output at roughly 84 to 171 times the human rate, which is the largest lexical gap in the study:

```
camaraderie   tapestry     palpable     intricate    underscore
unspoken      amidst       solace       fleeting     vibrant
cacophony     grapple      ignite       unravel
```

The concentration is the finding. Several of these words cluster in a single paragraph of model output in a way that essentially does not happen in the human corpus. `Camaraderie` and `cacophony` are the sharpest, because a human writer reaches for either perhaps once a year.

Repair: delete rather than substitute. `A palpable sense of camaraderie` almost always sits on top of a specific thing that the text has not said. Ask what actually happened, and if the source does not say, write `[specific detail here]`.

## Tier 2: register inflation

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

## Tier 3: phrase templates

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

## The sentence shapes

Two constructions matter more than any word:

**Negative parallelism.** `It is not just X, it is Y`. Also `Not X, but Y`, and `X rather than Y` used for emphasis rather than contrast. This is among the most recognisable patterns in current model output, and it survives most humanizing passes because it contains no flagged vocabulary. Repair by stating Y and dropping the setup, since the negated half is usually a straw position nobody held.

**The rule of three.** Three parallel items where the third carries no information beyond the first two, chosen for cadence. `Faster, cheaper, and more reliable` where the text only supports speed. Cut to what the evidence supports. Two items with substance beat three with padding.

## Tier 4: Emotional shorthand

These are not AI vocabulary words. They are AI emotional vocabulary: short, clean phrases that models produce when asked to write personal, first-person content. They appear constantly in AI-generated LinkedIn posts, personal essays, and reflective writing. Classifiers trained on those outputs recognize the pattern even when no individual word is flagged.

They are also bad writing, independently of any detector: they name an emotional effect without showing what produced it.

```
it meant a lot           didn't see that coming       more of these ahead
asked good questions     made the whole thing worth it  ran such a smooth event
learned a lot            grateful for the experience    so much energy in the room
showed up                gave it their all              truly inspiring
what a session           what an experience             couldn't be more proud
honored to be part of    humbled by the response
```

The repair is always the same: replace the emotional shorthand with the specific thing that produced the feeling.

| Shorthand | Repair direction |
|---|---|
| `it meant a lot` | What specifically did it mean, or what did you do with it after? |
| `didn't see that coming` | What did you see instead, and when did the thing happen? |
| `asked good questions` | Name one question, or name what made them good. |
| `made the whole thing worth it` | What would the thing not have been worth without it? |
| `more of these ahead, hopefully` | Where, what kind, what would make them happen? |
| `ran such a smooth event` | What specifically ran smoothly that you noticed? |

If the source does not supply the specific, write `[specific detail here]` and leave it. Do not invent what the emotional experience actually was.

## What models use less than humans

The gap runs both ways, and the underuse side is harder to fake:

**Contractions**, in registers where a human would contract. A conversational piece with no `don't` or `it's` reads stiff.

**Profanity and blunt language**, at over 100 times lower than the human rate in matched contexts. Not something to add, but worth noticing: heavily sanitised prose in a register that tolerates bluntness is itself a signal.

**`i.e.` and `e.g.`**, also over 100 times rarer in model output.

**Exact figures.** Models prefer `significantly`, `substantially` and `dramatically` where a human writer who knew the number would give the number. See `rules/specificity.md`.

**Hedges.** Instruction-tuned models hedge at roughly half to two thirds the human rate. Human experts write `probably`, `I think`, `as far as I can tell`. Adding a hedge that reflects real uncertainty in the source is a legitimate repair. Inventing uncertainty the author does not have is not.

## Failure modes when repairing vocabulary

**Thesaurus voice.** Swapping each flagged word for a synonym produces text with the same skeleton and a stranger surface. `Utilize` to `employ` fixes nothing.

**Corrective uniformity.** Applying the same substitutions across a whole document flattens the author's variation and leaves a signature of its own.

**Genre blindness.** `Nominalization`, `implementation` and `utilization` are correct in an academic abstract. `Robust` is correct in systems engineering, where it has a technical meaning. Check `rules/context.md` before flagging.

**Chasing the list.** These lists describe models observed through 2025. Vendors adjust. A list treated as permanent truth will misfire on newer output and on human writers who happen to like a flagged word. Treat every entry as a prompt to look at the sentence, never as a verdict.
