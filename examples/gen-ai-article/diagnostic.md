## Diagnostic: gen AI article

Produced at Stage 2 of the procedure in `SKILL.md`.

```
NOT AI DIAGNOSTIC
Genre:    General-audience article opening, inferred. No genre was given.
Register: 4 of 5. Aimed at a general reader, pitched at a consulting report.

Working already:
  Nothing. This is the rare case where the honest answer to "quote a sentence that
  needs no change" is that there is no such sentence, because there is no sentence
  here that makes a claim a reader could check, agree with or dispute.

Patterns found:
  mechanical frame        "In today's rapidly evolving technological landscape"
  participial clause      "By leveraging the power of large language models"
  mechanical transition   "Furthermore, the implications of this transformative
                          technology are far-reaching and multifaceted."
  mechanical frame        "It is worth noting that while the benefits are substantial,
                          the challenges are equally significant."
  empty conclusion        "In conclusion, as we navigate this unprecedented era..."
  significance claim      "represents a paradigm shift"
  vague attribution       "organizations across various sectors"
  uniform sentence shape  5 sentences, 4 of them framing, none carrying a fact

Vocabulary in context:
  "paradigm shift" 1x     Problem. The shift is asserted, never described.
  "leveraging" 1x         Problem. Heads a participial clause.
  "transformative" 1x     Problem. Significance claim with no content.
  "groundbreaking" 1x     Problem. Second significance claim about the same thing.
  "multifaceted" 1x       Problem. Says the implications have facets. Name one.
  "nuanced" 1x            Problem. "a nuanced understanding" of nothing specified.
  "crucial" 1x            Problem.
  "foster" 1x             Problem.
  "rapidly evolving" 1x   Problem, and the ninth term the script counts. It sits
                          inside the opening frame quoted above.

Intervention: heavy, and the honest recommendation is to write the passage again
              from source material rather than to rewrite this text
```

### Measured

```
python3 scripts/analyze_structure.py examples/gen-ai-article/input.md
python3 scripts/metrics.py examples/gen-ai-article/input.md
```

| Measure | Value |
|---|---|
| Words / sentences / paragraphs | 99 / 5 / 1 |
| Nominalization density | 70.7 per 1,000 words, high for this proxy |
| Mechanical transitions | 3 |
| AI-associated vocabulary | 9 unique terms in 99 words |
| Burstiness | 0.388 |
| Flesch-Kincaid grade | 17.2 |
| Gunning Fog | 21.3 |
| Flesch Reading Ease | 7.3 out of 100 |
| Density score | 53.5, high |

Nine flagged terms in 99 words is about 91 per 1,000, second in this example set only to the LinkedIn post at 99 per 1,000. The reading ease of 7.3 is second lowest too, after the academic abstract at -0.5. Both figures agree with the reading, which is not always the case.

### The finding that determines the rewrite

**The passage contains no facts.** Not few. None.

Work through it. `Generative AI represents a paradigm shift`: an assertion, unsupported. `Organizations across various sectors are transforming their operational frameworks`: which organizations, which sectors, what changed. `The implications are far-reaching and multifaceted`: no implication is named. `The benefits are substantial and the challenges are equally significant`: neither is specified. `We must foster a nuanced understanding of the opportunities and the ethical considerations`: no opportunity and no consideration appears anywhere in the text.

This matters more than any structural pattern, because it bounds what a rewrite can legitimately do. Rule 1 in `SKILL.md` forbids inventing content. A passage with no content therefore cannot be rewritten into a passage with content. It can only be shortened to the two claims it does gesture at, with flags for what the author must supply.

Any tool that returns a confident, readable, specific paragraph from this input has fabricated the specifics. `rationale.md` shows one that did.
