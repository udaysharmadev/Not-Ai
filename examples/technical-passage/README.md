## Technical passage

An instruction-tuned model was asked to explain how a caching system works. The technical content is correct; the prose is dense, inflated and built to a template.

| File | |
|---|---|
| [input.md](input.md) | The generated text, 241 words |
| [diagnostic.md](diagnostic.md) | Stage 2 diagnostic and the measured figures |
| [output.md](output.md) | The rewrite, 173 words |
| [rationale.md](rationale.md) | Sentence-level accounting, before and after numbers, and what the rewrite got wrong |

**What this example is for.** It is the clearest demonstration that the analysis scripts miss the strongest signal in the research. The reading finds four present participial clauses; `analyze_structure.py` reports 0 of 12. Two of them, `By leveraging the power of...` and `By thoughtfully implementing...`, are sentence openers that the pattern misses because it is anchored to the first word and both begin with `By`. The other two, `ensuring that users receive responses in a timely manner` and `distributing the load across multiple layers`, sit mid-sentence, which the pattern does not look at at all. So the count is short for two separate reasons and the printed figure is 0% either way.

It also shows a rewrite scoring worse on a metric while reading better. Burstiness fell from 0.471 to 0.415, and the rationale explains why that is the metric's problem rather than the rewrite's.
