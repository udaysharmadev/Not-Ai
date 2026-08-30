## Personal essay

A generated personal essay about moving from Nagpur to Bangalore. 213 words about the author's own life, written at grade 15 in abstract nouns.

| File | |
|---|---|
| [input.md](input.md) | The generated essay, 213 words |
| [diagnostic.md](diagnostic.md) | Stage 2 diagnostic and the measured figures |
| [output.md](output.md) | The rewrite, three slots and a flag |
| [rationale.md](rationale.md) | Per-sentence accounting, two declared additions, and a rule the first draft broke |

**What this example is for.** The line the skill refuses to rewrite. The draft ends by telling the reader what the author learned: `adaptation is not merely a passive response to environmental change but an active, ongoing process of self-reinvention`. Every other flag in this repository marks a missing fact. This one marks a missing position, and inventing a position for someone and attributing it to their own life is a different order of error. The output quotes it back and says the essay can end without a moral.

The measurement lesson here is the pair of sentence-length figures. Mean length is 21.2 words before and 21.2 after, unchanged to the decimal, while burstiness goes from 0.375 to 0.600. The input's sentences run from 8 words to 31, ten of them bunched in the middle with nothing in the very short or very long band; the output runs from 5 to 53 and puts one sentence in each. Variation lives in the spread, and the average cannot see it.

Two smaller findings. The vocabulary scanner catches only two terms here, fewer than anywhere except the human paragraph in `examples/already-natural/`, because this draft is generated in academic register and the wordlist is tuned to business register: `embarked`, `journey`, `acculturation` and `unparalleled` all pass. And first-person markers fall from 14 to 12 while the essay becomes considerably more personal, which is the clearest evidence in the set that pronoun frequency is not disclosure.

`rationale.md` also records a rule the first version of this rewrite broke, and what fixing it cost on the metrics.
