## Rationale: personal essay

The events are real and almost none of them are in the draft. The rewrite recovers what is there, opens slots for what is not, and refuses to carry the conclusion.

### Actions taken

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

### The line that gets a flag instead of a rewrite

> The experience has taught me that adaptation is not merely a passive response to environmental change but an active, ongoing process of self-reinvention.

Three separate problems converge here. It is negative parallelism, `not merely X but Y`, which `references/wikipedia-signs.md` lists among the most reliable signs. It is abstract to the point of vacancy. And it is a claim about what the author personally learned from their own life.

The third is the one that matters. A rewrite can make a vague sentence specific when the source supplies the specifics. Nothing in this draft supplies what the author concluded, so any rewrite here invents a belief and attributes it to them. Every other flag in this file marks a missing fact. This one marks a missing position, which is worse, because an essay is largely a position.

So it is quoted back with the reason, and the note says the essay can end on the previous paragraph without supplying a moral. Many good essays do.

### Two declared additions

**"In Nagpur there were people who had known me long enough that I never had to explain myself."**

The draft says `the absence of an established social network created feelings of isolation`. The rewrite says what absence of a social network consists of. Nothing in the source states that anyone in Nagpur had known the author a long time, or that explaining themselves was the friction, so this is inference and it is flagged as an addition rather than presented as a recovery.

It is a defensible inference and it is still an inference. An author who reads it and thinks `that is not what I missed` should cut it.

**"the food, the way the office ran, what a weekend was supposed to look like"**

Three items standing in for `the familiar comforts of my hometown`, the vaguest phrase in the draft. They are the kind of thing people compare between cities, which is precisely the problem: they are plausible rather than true. They belong in the same category as the bracketed slots and should be replaced with what the author actually caught themselves comparing.

Stage 4 of `SKILL.md` requires additions to be declared, and this is the declaration for both. Two inferred passages in a 255-word rewrite is more than this skill should be comfortable with, and the honest reading is that a draft this empty pushes any rewrite toward invention. That pressure is the reason rule 1 is stated as an absolute rather than a preference.

### Measured before and after

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

### What went wrong, and what is still wrong

**The first version of this rewrite broke the skill's own rule 2.** Where the output now reads `I kept measuring the new place against the old one: the food, the way the office ran, what a weekend was supposed to look like`, the earlier version ran the three items as separate fragments: `The food. The way the office ran. What a weekend was supposed to look like.` It read well. It was also three fragments in parallel, a rule-of-three shape built out of exactly the decorative fragmenting that rule 2 prohibits, and it pushed the repeated-`the` opener count from 3 to 5, making the output worse than the input on that measure. Burstiness fell from 0.742 to 0.600 when it was fixed, which is the correct direction for a metric that was rewarding fragments.

Stage 5 question 5 is what caught it, and the fragment version is recorded here rather than quietly discarded.

**`the` still opens 3 sentences and the warning still fires.** Two of the three are in the deliverable, `The first year was hard` and `The bigger problem was`, and both are load-bearing. The third is in a bracketed note. The warning is correct that the pattern exists and wrong that it needs fixing, and forcing a different opener onto either sentence would cost more than the repetition does.

**Five of the output's readings are artifacts of the bracket text.** Reader address 8, questions 1, the stance verdict moving off `absent` on the strength of one `certainly`, the repeated phrase `when you noticed`, and the surviving `meaningful` all come from editorial notes to the author rather than from the essay. `examples/gen-ai-article/` documents the same effect; this file quantifies it. The three slots and the flag hold 132 of the output's 255 words, so 51.8% of the measurable surface is instruction rather than deliverable, and no script can tell the difference.

The `certainly` sits in `almost certainly not how you would put it`, inside a note, and the essay proper carries no stance marker at all. One marker is under the three-marker floor, so the verdict is `too sparse to judge` rather than `over-assertive`. A single adverb in an editorial aside cannot support a claim that the essay is over-confident, and the earlier version of the check made exactly that claim.

Read what you are measuring. That is the recurring lesson of the whole example set, and it applies as much to the rewrite as to the draft.

### What the finished essay needs

Four things, all of which the author has and none of which a tool can supply: the rent figure and what it displaced, when in year two they noticed and what they were doing, what they think actually changed, and either a position worth stating at the end or the confidence to stop without one.

With those, this is a good essay in about 300 words. Without them it is a form, and the form is more honest than the polished version.
