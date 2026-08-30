## Diagnostic: technical passage

Produced at Stage 2 of the procedure in `SKILL.md`.

```
NOT AI DIAGNOSTIC
Genre:    Technical explanation, inferred from content. No genre was given.
Register: 4 of 5. Written for working developers, currently pitched at a journal.

Working already:
  "caching operates by storing frequently accessed data in a location that can be
  retrieved more rapidly than the original source"
  The technical content is correct and the definition is the right one. Nothing in
  this passage is factually wrong, which sets the constraint: this is a rewrite for
  density and framing, not for accuracy.

Patterns found:
  participial clause      "By leveraging the power of temporary storage solutions"
  participial clause      "By thoughtfully implementing and managing caching solutions"
  participial clause      "ensuring that users receive responses in a timely manner"
  participial clause      "distributing the load across multiple layers"
  mechanical frame        "In the realm of modern software architecture"
  mechanical frame        "It is worth noting that the selection of an appropriate..."
  mechanical frame        "Furthermore, modern caching implementations typically..."
  empty conclusion        "In conclusion, caching remains an indispensable tool in
                          the arsenal of modern software engineers"
  enumerated tricolon     "First... Second... Third..." across three real advantages
  uniform paragraphs      4 paragraphs of 2, 5, 3 and 2 sentences, every one of them
                          opening with a claim and following it with support
  overloaded paragraph    paragraph 3 carries expiration policy types, cache busting,
                          data freshness and strategy selection in three sentences

Vocabulary in context:
  "pivotal" 1x            Problem. The claim is not supported and not needed.
  "leveraging" 1x         Problem. Decorative, and it heads a participial clause.
  "nuanced" 1x            Problem. "a nuanced decision" claims subtlety, supplies none.
  "crucial" 1x            Problem. Expiration policies matter; say why instead.
  "indispensable", "remarkable improvements", "superior user experience"
                          Problem. Three significance claims in the closing paragraph.
  "including but not limited to"
                          Problem. Legal register, wrong genre.
  "latency", "invalidation", "cache busting"
                          Fine. Domain terms doing real work. Keep all three.

Intervention: moderate
```

### Measured

Run against `input.md`:

```
python3 scripts/analyze_structure.py examples/technical-passage/input.md
python3 scripts/metrics.py examples/technical-passage/input.md
```

| Measure | Value |
|---|---|
| Words / sentences / paragraphs | 241 / 12 / 4 |
| Nominalization density | 95.4 per 1,000 words, high for this proxy |
| Participial clause openers | 0 of 12, 0% |
| Mechanical transitions | 4 |
| Burstiness | 0.471 |
| Flesch-Kincaid grade | 16.4 |
| Gunning Fog | 20.5 |
| Density score | 74.3, high |
| AI-associated vocabulary | 4 unique terms |

### Where the script and the reading disagree

**The script reports 0 of 12 participial clause openers. The reading found four participial clauses.** The script is wrong here, and predictably so, for two separate reasons. Its pattern is anchored to the first word of the sentence, so `By leveraging the power of...` and `By thoughtfully implementing...` do not match, because both begin with `By` rather than with the participle. The other two, `ensuring that users receive responses in a timely manner` and `distributing the load across multiple layers`, are mid-sentence and the pattern never looks there. The docstring in `analyze_structure.py` documents the anchoring; the second gap follows from the measure being defined on openers only.

This is the single most important thing this example demonstrates. The strongest signal in the research is the one the script is worst at detecting. A 0% participial rate means "none of the anchored forms", not "none". Read the text.

**Burstiness of 0.471 does not trigger a warning**, and the reading still found uniform paragraph shape. Burstiness measures sentence length variation only. It is blind to four paragraphs built to the same template.
