## Rationale: technical passage

Sentence-level accounting of the rewrite, then the measurements, then what the rewrite got wrong.

### Actions taken

| Source | Action | Result |
|---|---|---|
| "In the realm of modern software architecture, caching represents a pivotal mechanism that fundamentally transforms how applications manage and retrieve data." | REPLACE | "Caching keeps a copy of data somewhere faster to reach than the original." |
| "By leveraging the power of temporary storage solutions, systems can significantly enhance their overall performance metrics while simultaneously reducing the burden on primary data sources." | RESTRUCTURE, SPLIT | "A read that hits the cache skips the database entirely, so it returns faster and the database does less work." |
| "At its core, caching operates by storing frequently accessed data..." | MERGE | Folded into the opening definition, which now carries it. |
| "This approach offers several key advantages. First... Second... Third..." | RESTRUCTURE | Two effects stated once, without labels. The third advantage, scaling, was the same claim as the first two under load, so it became "Both effects compound under load." |
| "Furthermore, modern caching implementations typically incorporate sophisticated expiration policies to ensure data freshness." | REPLACE | "The hard part is deciding when a cached copy has gone stale." |
| "These policies, ranging from time-based invalidation to event-driven cache busting, play a crucial role in maintaining the delicate balance..." | SPLIT | Two sentences, one per policy type, each saying what the policy actually does. |
| "It is worth noting that the selection of an appropriate caching strategy is a nuanced decision that requires careful consideration of multiple factors, including but not limited to the nature of the data, access patterns, and the specific requirements of the application in question." | REPLACE | "Which one fits depends on how bad it is to serve a stale value, and that varies enormously between systems." |
| "In conclusion, caching remains an indispensable tool in the arsenal of modern software engineers. By thoughtfully implementing and managing caching solutions, development teams can achieve remarkable improvements in application performance, ultimately delivering a superior user experience to their end users." | REMOVE, REPLACE | Both sentences cut. Replaced with the point the passage had been circling: the decision is about tolerable staleness, not about caching. |

No technical claim was altered. Two terms did not survive as terms, and both substitutions are worth declaring, because `diagnostic.md` said to keep all three domain terms and the rewrite kept one of them as written. `latency` became `it returns faster`, which makes the same claim in the register the rest of the rewrite uses, and the source's `event-driven cache busting` became `event-driven invalidation`, which is what the mechanism is ordinarily called. `database`, `time-based expiry` and `event-driven` are intact. If either word matters for searchability, put it back; the sentences hold either way.

### Measured before and after

```
python3 scripts/analyze_structure.py examples/technical-passage/input.md
python3 scripts/analyze_structure.py examples/technical-passage/output.md
```

| Measure | Before | After |
|---|---|---|
| Words | 241 | 173 |
| Sentences | 12 | 14 |
| Mean sentence length | 19.9 | 12.2 |
| Nominalization density | 95.4, high | 17.3, normal |
| Mechanical transitions | 4 | 0 |
| AI-associated vocabulary | 4 unique | 0 |
| Flesch-Kincaid grade | 16.4 | 6.0 |
| Gunning Fog | 20.5 | 8.4 |
| Density score | 74.3, high | 21.4, low |
| Burstiness | 0.471 | 0.415 |

The nominalization figure is the one that moved most, from 95.4 to 17.3 per 1,000 words, and it moved because the abstractions were replaced with the actions underneath them rather than because words were swapped. `the selection of an appropriate caching strategy` became `which one fits`.

Both figures are from the regex proxy in this repository and are comparable only to each other. Neither is comparable to the 14.6 per 1,000 tokens that Reinhart et al. measured with a dependency parser. See `references/style-research.md`.

### What went wrong

**Burstiness fell, from 0.471 to 0.415.** The rewrite reads better and scores worse on this measure. Shortening the long sentences compressed the range, because burstiness is a coefficient of variation and cutting the outliers reduces it. Anyone treating burstiness as a target would reject this rewrite. It is a weak metric and this example is the proof.

**Three sentences now open with "A".** The script flags it. It is a real if minor regression, introduced by the parallel construction in the third paragraph.

**Grade level dropped from 16.4 to 6.0, which is further than intended.** The genre wants roughly grade 10 to 12. Grade 6 risks reading as condescending to the audience the passage names. This is over-correction and it is the failure mode `rules/context.md` warns about: applying the fix past the point where it helps.

**The benchmark flags this pair twice, and only one flag is fair.**

```
python3 scripts/benchmark.py --input examples/technical-passage/input.md \
                            --output examples/technical-passage/output.md
```

```
SEMANTIC PRESERVATION
  Token overlap similarity: 8.1%
  ⚠ Major meaning drift

FACTUAL PRESERVATION (NUMBERS)
  ✓ Numbers preserved

WORD COUNT
  241 → 173 (-28.2%)
  ⚠ Significant reduction (-20%+)
```

The word count warning is fair and agrees with the grade-level finding above: this rewrite cut harder than the genre needed. The similarity warning is not evidence of anything. It is 8.1% because the rewrite replaced `sophisticated expiration policies to ensure data freshness` with `deciding when a cached copy has gone stale`, which is the intervention working, and token overlap cannot tell that from meaning loss. The same measure rates `examples/already-natural/` at 65.5%, the highest in the set, on a pair where the paragraph was not touched. `benchmarks/README.md` has the full table.

### The one addition, declared

The output contains a sentence pair not present in the source:

> A stale follower count is a cosmetic problem. A stale account balance is not.

These are illustrations of a principle the source does state, not facts about any system. They were added because the source asserted that strategy choice "requires careful consideration of multiple factors" without naming a single one, and the abstraction is unreadable without an instance.

This is a judgment call and it sits close to the line that rule 1 in `SKILL.md` draws. Under `--mode preserve` it would not have been added; the sentence would have read `Which one fits depends on how bad it is to serve a stale value.` and stopped there.

Note also what was deliberately **not** added. Time-based expiry is described as holding a copy "for a fixed window" rather than for sixty seconds. A specific interval would have been an invented technical detail, and the source does not supply one.
