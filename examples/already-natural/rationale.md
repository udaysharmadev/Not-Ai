## Rationale: already natural

Intervention rate 0%. The delivered text is the input, unchanged. This file explains why, and shows what the two available failure modes would have produced.

### Why nothing changed

Four properties, each of which is difficult for a model to produce and easy for a person writing about their own week to produce without trying.

**Specificity that costs something to know.** `three days`, `last month`, `only showed up under load`, `a race condition between the health check and the reconnection logic`, `a controlled load test`. Every one of these is checkable and none is decorative. The technical cause is named precisely enough that another engineer could look for the same bug.

**The author is in the sentences.** `I spent`, `I found it by`. Not as a stylistic flourish; the first person is carrying the information about who did what.

**A fragment placed for weight.** `Not fun` opens the closing sentence after three sentences of 15, 22 and 17 words. It works because of what precedes it, and it is the kind of thing a writer does on instinct. Note that no script sees it: the segmenter counts the closing sentence at 13 words, comma and all, so the two-word beat that makes the paragraph land is invisible to every measure in this repository.

**An ending that is a conclusion rather than a summary.** `at least I know what to look for next time` adds something the paragraph had not yet said. Compare the closing sentence of `examples/technical-passage/input.md`, which restates the paragraph and then asserts that the topic is important.

### Failure mode one: over-humanization

What a tool that must produce a change produces:

> So, I spent a solid three days last month tracking down this gnarly bug that only popped up under heavy load, super annoying! Turns out it was a classic race condition lurking in how we handled connection timeouts between the health check and reconnect logic. I ended up cranking up the logging and ran a controlled load test, and boom, found it! Wasn't exactly fun, but hey, at least now I know what to watch for. 😅

The specifics survive, buried. What is lost is the author's actual register: measured, slightly dry, unbothered. `Not fun, but at least I know what to look for next time` has been replaced with performed enthusiasm that the original writer plainly does not feel.

This is the standard humanizer output shape. `SKILL.md` rule 2 forbids it directly: never degrade writing to look human.

### Failure mode two: chasing the warnings

The subtler failure, and the more likely one for an agent following the script output literally. Two measures fired, so an agent could try to satisfy both.

To raise burstiness from 0.200, split a sentence and pad another:

> I spent three days last month hunting a bug. It only showed up under load, which made it miserable to reproduce, and I burned most of the first day just getting a reliable repro at all. The issue was in how we handled connection timeouts, specifically a race condition between the health check and the reconnection logic. I found it by adding more aggressive logging and watching the logs during a controlled load test. Not fun, but at least I know what to look for next time.

Burstiness rises. The paragraph is now 20% longer, and the added clause invents a fact: the source never says the first day went to reproduction. Rule 1 violated to satisfy a metric.

To lower nominalization from 45.5, the proxy's three matches are `connection`, `condition` and `reconnection`. Two of them name the bug, so removing those two gives:

> The issue was in how we handled connection timeouts, specifically two parts of the system racing each other when one tried to reconnect while the other was checking health.

Longer, vaguer, and it no longer names the bug class. `Race condition` is the term an engineer searches for.

Both edits improve a number and damage the writing. That is the whole argument for reporting patterns to a person instead of optimising a score, and it is why `compute_quality_score` was removed from `scripts/metrics.py`.

### Measured

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
