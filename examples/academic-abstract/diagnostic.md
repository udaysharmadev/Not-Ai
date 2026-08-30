## Diagnostic: academic abstract

Produced at Stage 2 of the procedure in `SKILL.md`. This is the example where register does most of the work.

```
NOT AI DIAGNOSTIC
Genre:    Abstract for an NLP or ML paper. Inferred from content and structure.
Register: 5 of 5. Reviewers and researchers in the field. Correctly formal.

Working already:
  "the conventional assumption that larger models invariably outperform smaller
  counterparts is not universally applicable"
  This is the paper's actual finding and it is stated clearly. The abstract has a
  real result underneath the prose, which distinguishes it from
  examples/gen-ai-article/ and makes a genuine rewrite possible.

Patterns found:
  participial clause      "Leveraging a novel experimental framework that
                          systematically varies model architectures"
  mechanical transition   "Furthermore, the implications of these findings are
                          significant for practitioners"
  significance inflation  "the implications of these findings are significant"
  redundant closing       Sentence 5 restates the finding from sentence 2
  uniform sentence shape  5 sentences of 24, 27, 31, 20 and 36 words
  hedge stacking          "in certain task-specific contexts", "comparable or
                          superior", "particularly when", all in one sentence

Vocabulary in context:
  "nuanced" 2x            Problem. Twice in 140 words, and neither instance
                          specifies what the subtlety consists of.
  "comprehensive" 1x      Problem. "a comprehensive investigation into" is four
                          words that mean "we studied".
  "leveraging" 1x         Problem. Heads the participial clause.
  "utilization" 1x        Problem in "optimize resource utilization". "use less
                          compute" is the claim.
  "invariably"            Fine. Precise here, and the sentence needs it.
  "downstream performance", "task-specific", "training data"
                          Fine. Field-standard terms. Keep all of them.

Specificity, the critical issue:
  "diverse natural language processing tasks"   which tasks
  "certain task-specific contexts"              which contexts
  "models of moderate complexity"               moderate by what measure
  "training data is limited in scope"           limited below what threshold
  "comparable or superior performance metrics"  which metrics, and by how much
  Five unfilled specifics in a 140-word abstract. The author has all five values.

Intervention: moderate
```

### Measured

```
python3 scripts/analyze_structure.py examples/academic-abstract/input.md
python3 scripts/metrics.py examples/academic-abstract/input.md
```

| Measure | Value |
|---|---|
| Words / sentences | 140 / 5 |
| Mean sentence length | 27.6 words |
| Burstiness | 0.201, ⚠ low |
| Participial clause openers | 1 of 5, 20%, ⚠ high for this proxy |
| Nominalization density | 92.9 per 1,000 words, ⚠ high for this proxy |
| Mechanical transitions | 1 |
| AI-associated vocabulary | 4 unique |
| Flesch-Kincaid grade | 20.3 |
| Gunning Fog | 24.6 |
| Flesch Reading Ease | -0.5 out of 100 |
| Density score | 69.3, high |

### Reading the numbers against the genre

**This is the one input where the participial detector fires**, 1 of 5 sentences, because `Leveraging a novel experimental framework` puts the participle in the first word. Compare `examples/technical-passage/`, where two participial clauses beginning with `By` were missed entirely. The detector is not measuring participial clauses; it is measuring participles in sentence-initial position.

**Nominalization at 92.9 is high and mostly legitimate.** `Investigation`, `performance`, `assumption`, `utilization`, `consideration`, `requirements`. Academic abstracts nominalize because they describe methods and findings rather than actions by people, and the register expects it. The problem is not the density. It is that `a comprehensive investigation into the nuanced relationship between X and Y` conveys no more than `we tested whether X affects Y` while occupying three times the space.

Do not lower this number for its own sake. `rules/context.md` covers the register rule: in an academic abstract, nominalization is a feature.

**Reading ease of -0.5 is below zero**, which the Flesch scale permits and which means the sentences are long and the words are polysyllabic. In this genre that is close to normal and it is not by itself a finding.

**Burstiness of 0.201** is a genuine problem here, unlike in `examples/already-natural/` where the same figure was harmless. Five sentences between 20 and 36 words with no short one among them gives a reviewer nowhere to rest. The identical number means opposite things in the two texts, which is the argument for reading before concluding.
