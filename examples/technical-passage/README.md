## Technical passage

An instruction-tuned model was asked to explain how a caching system works. The technical content is correct; the prose is dense, inflated and built to a template.

| File | |
|---|---|
| [input.md](input.md) | The generated text, 241 words |
| [diagnostic.md](diagnostic.md) | Source diagnostic and measured figures |
| [output.md](output.md) | The rewrite, 173 words |
| [rationale.md](rationale.md) | Sentence-level accounting, before and after numbers, and what the rewrite got wrong |

**What this example is for.** It was the clearest demonstration that the analysis scripts missed the strongest signal in the research. The reading finds four present participial clauses; `analyze_structure.py` used to report 0 of 12. Two of them, `By leveraging the power of...` and `By thoughtfully implementing...`, are sentence openers that the pattern missed because it was anchored to the first word and both begin with `By`. The other two, `ensuring that users receive responses in a timely manner` and `distributing the load across multiple layers`, sit mid-sentence, which the pattern did not look at at all.

**Update (v2.2.0).** The gap above is now closed without adding dependencies: the analyzer reports anchored, prepositional-variant (`By leveraging...`), and mid-sentence-tail counts separately. On this input it reports 0 anchored, 1 extended, and 6 mid-sentence tails across 12 sentences (8% opener rate, elevated for this proxy). The diagnostic below preserves the original 0-of-12 figures as the record of what the old code produced; rerun the scripts for current numbers.

It also shows a rewrite scoring worse on a metric while reading better. Burstiness fell from 0.471 to 0.415, and the rationale explains why that is the metric's problem rather than the rewrite's.
