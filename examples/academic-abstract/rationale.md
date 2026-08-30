## Rationale: academic abstract

The rewrite keeps the register and removes the padding. Formality was never the problem.

### Actions taken

| Source | Action | Result |
|---|---|---|
| "This paper presents a comprehensive investigation into the nuanced relationship between machine learning model complexity and downstream performance across diverse natural language processing tasks." | REPLACE, MOVE | The finding moves to the front: "Larger language models do not always outperform smaller ones." An abstract should open with the result, not with an announcement that a study occurred. |
| "Leveraging a novel experimental framework that systematically varies model architectures, we demonstrate that the conventional assumption that larger models invariably outperform smaller counterparts is not universally applicable." | RESTRUCTURE, SPLIT | Participial clause becomes a finite clause. "This paper tests that assumption on [tasks], varying architecture systematically while holding the training budget fixed." |
| "Our findings reveal that, in certain task-specific contexts, models of moderate complexity exhibit comparable or superior performance metrics relative to their larger counterparts, particularly when training data is limited in scope." | RESTRUCTURE, SPLIT, FLAG | "Models below [X] parameters matched or exceeded larger models on [which of those tasks] when training data fell below [N] examples." Three hedges removed, three slots opened. |
| "Furthermore, the implications of these findings are significant for practitioners seeking to optimize resource utilization while maintaining competitive performance levels." | REMOVE | Asserts that the implications are significant without naming one. |
| "We conclude that a more nuanced, context-dependent approach to model selection is warranted, one that takes into consideration the specific requirements of the task at hand rather than defaulting to scale as a proxy for quality." | REPLACE, FLAG | "Model selection should therefore account for data availability and task type rather than scale alone", plus a flag asking for the concrete implication the removed sentence gestured at. |

### What was deliberately preserved

Third person. No contractions. `Models below [X] parameters matched or exceeded` rather than `beat`. Passive constructions where the genre uses them. The hypothesis, method, finding, implication order.

The temptation with an abstract is to make it friendly. That would be a genre error, and it would get the paper desk-rejected. `rules/context.md` sets the constraint: reduce padding, keep formality.

### Measured before and after

```
python3 scripts/analyze_structure.py examples/academic-abstract/input.md
python3 scripts/analyze_structure.py examples/academic-abstract/output.md
```

| Measure | Before | After |
|---|---|---|
| Words | 140 | 108 |
| Sentences | 5 | 5 |
| Mean sentence length | 27.6 | 22.2 |
| Burstiness | 0.201, ⚠ low | 0.604, ✓ good variation |
| Participial clause openers | 1 of 5, 20%, ⚠ | 0 of 5, 0%, ✓ |
| Nominalization density | 92.9, ⚠ high | 83.3, ⚠ high |
| Mechanical transitions | 1 | 0 |
| AI-associated vocabulary | 4 unique | 0 |
| Flesch-Kincaid grade | 20.3 | 14.9 |
| Gunning Fog | 24.6 | 17.2 |
| Flesch Reading Ease | -0.5 | 26.7 |
| Density score | 69.3 | 63.9 |

**Burstiness tripled, 0.201 to 0.604.** The largest rise in the set, and one of only two rewrites where the measure moved in the direction its name implies. `examples/personal-essay/` is the other, 0.375 to 0.600. It rose because the rewrite has two short sentences, 9 words and 8, against a 44-word one, not because variation was engineered.

**Nominalization stayed high, 92.9 to 83.3, and that is correct.** A 10% reduction on a feature the genre requires. The proxy's matches in the output include `classification`, `question`, `selection` and `availability`, which are the right words. Pushing this figure toward the conversational band would mean writing a worse abstract, and the script's `high for this proxy` label is not a defect to be fixed.

This is the clearest case in the example set for reading the register before acting on a warning.

**Grade level 20.3 to 14.9**, which lands in the right place for the genre. Compare `examples/technical-passage/`, where the same instinct overshot to grade 6.

### One declared addition

The output contains a sentence that has no counterpart in the source:

> The gap narrowed further under [the specific condition].

Nothing in the input says the gap narrowed under any condition. The sentence exists because the input's `particularly when training data is limited in scope` implies the author measured an interaction and did not report it, and because the rewrite needed one short sentence to break a run of long ones. Both reasons are real and neither is sufficient: an author who does not have that result should delete the line rather than fill the slot.

Stage 4 of `SKILL.md` requires additions to be declared rather than slipped in. This is the declaration. It is also the weakest decision in this rewrite, and it is left in place so the example shows what a borderline call looks like instead of pretending none occur.

### The six flags

`[the specific tasks]`, `[X] parameters`, `[which of those tasks]`, `[N] examples`, `[the specific condition]`, and a closing slot asking for the concrete practitioner implication.

An abstract with six bracketed slots looks unfinished, and it is. But the author ran the experiments and knows five of the six values. The slots take a few minutes to fill and the result is an abstract a reviewer can evaluate. The alternative, a rewrite that invents plausible thresholds, would be a fabricated experimental result in a document submitted for publication. There is no version of this skill where that is an acceptable output.
