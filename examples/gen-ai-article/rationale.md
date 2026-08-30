## Rationale: gen AI article

The output is two sentences and a flag block. This file explains why that is the correct answer, and shows the wrong answer that an earlier version of this repository shipped.

### Actions taken

| Source | Action | Result |
|---|---|---|
| "In today's rapidly evolving technological landscape," | REMOVE | Pure framing. Carries no information at any level. |
| "Generative AI represents a paradigm shift in how we approach problem-solving and innovation." | REMOVE | An unsupported significance claim. Nothing survives it. |
| "By leveraging the power of large language models, organizations across various sectors are fundamentally transforming their operational frameworks." | REPLACE, FLAG | "Generative AI is in routine use at [organisations the author can name], for [what those organisations actually use it for]." The claim shape is kept; the vagueness becomes visible as two slots. |
| "Furthermore, the implications of this transformative technology are far-reaching and multifaceted." | REMOVE | Says the implications have implications. |
| "It is worth noting that while the benefits are substantial, the challenges are equally significant." | REPLACE, FLAG | "The gains and the costs are both real: [one specific gain, with evidence] set against [one specific cost, with evidence]." |
| "In conclusion, as we navigate this unprecedented era of technological advancement, it is crucial that we foster a nuanced understanding of both the opportunities and the ethical considerations that accompany this groundbreaking innovation." | REMOVE | 33 words, the longest sentence in the source. Restates sentence four, adds a call to understand things that were never named. |

Five sentences in, two out, four slots flagged. That ratio is the diagnosis.

### Measured before and after

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

### Reading these numbers correctly

**The word count barely moved, 99 to 93, and that is misleading.** Of the output's 93 words, 53 are the flag block, which is instruction to the author rather than part of the deliverable, and another 35 are the four bracketed slots. That leaves 18 words of finished prose. Word count is measuring the wrong thing here.

**Three flagged vocabulary terms remain, and all three are inside the flag block.** `paradigm shift`, `nuanced` and `multifaceted` appear in the output only because the flag quotes them as examples of what was removed. The script cannot tell the difference between a word being used and a word being cited. `references/wikipedia-signs.md` documents the same problem in reverse.

The repository handles it by convention rather than by fixing the scripts, which cannot be fixed. Every specimen sits inside one of four markers: a fenced code block, inline backticks, a `> ` blockquote line, or double quotation marks. A scanner that strips those four before counting finds no unquoted use of a flagged term anywhere in the repository outside the six `input.md` files, which are specimens end to end. The convention is what makes the claim checkable; without it, a file arguing against `leveraging` is indistinguishable from a file using it.

**Nominalization stayed high, 70.7 to 53.8.** Same cause. Of the five suffix matches the proxy finds in the output, `advancement` is quoted inside the flag as an example of what was cut, and the other four, `organisations` twice and `evidence` twice, are inside bracketed slots. Not one of them is in the finished prose.

The lesson is not that the scripts are broken. It is that they measure a file, and a file can contain both a deliverable and commentary about the deliverable. Read what you are measuring.

**Burstiness barely moved**, 0.388 to 0.380, which `benchmark.py` reports as `unchanged (-0.008)`. It is the one pair in this set where the measure says nothing either way, and that is the most honest reading available: the deliverable is two sentences and a flag block, so there is no rhythm here to measure.

### The wrong answer this repository used to ship

An earlier version of this example returned the following, presented as the correct output:

> Generative AI went mainstream quietly. Not with a product launch, with your colleagues starting to use it for first drafts, your inbox filling with emails that sound oddly similar, your company's job postings adding "AI literacy" to requirements. The shift happened in the daily routine before anyone declared it a shift.
>
> What it does well: it writes fast and reads passably. What it does badly: it has no idea when it's wrong. A model will state a fabricated statistic with the same confidence it states a verified one.

It reads well. It is specific, concrete, well-paced, and every single specific in it is invented. The source says nothing about first drafts, nothing about inboxes, nothing about job postings, nothing about fabricated statistics. A model wrote a better article than the input and attributed it to the author.

This is the failure this skill exists to avoid, and it is more dangerous than the vague original, because vagueness is visible and confident fabrication is not. An author who accepted that paragraph would be publishing claims they never made and cannot defend.

The old version also claimed in its own change table that it had removed "3 em dashes → 0" while the paragraph it shipped still contained two. That is the exact failure Stage 5 question 8 was added to catch: do the changes I am about to describe match the changes I actually made.

### What a legitimate rewrite would need

Source material. Specifically: which organisations, doing what, with what measured result, and one named cost with evidence. With those four facts the passage could become something worth reading in about 120 words. Without them there is no article, and saying so is more useful to the author than a polished paragraph that sounds like one.
