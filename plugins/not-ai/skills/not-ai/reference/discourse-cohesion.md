# Discourse and cohesion: connections, not connectives

Read this reference when sentences are grammatical but the paragraph does not
flow. Cohesion is whether adjacent ideas share referents, chains, and real
relations — not how many connectives appear.

## What to measure (`not_ai_core/discourse.py`)

- Adjacent content overlap (zero-overlap neighbours are re-read candidates).
- Abrupt subject shifts (new subject + no shared content).
- Pronoun antecedent ambiguity (opening pronoun + 2+ properish candidates).
- Connective function by relation: additive, contrastive, causal, temporal,
  conditional, exemplifying, reformulating, conclusive.
- Connective variety vs repetition (one relation repeated 3+ times).
- Paragraph topic drift and repeated conclusions.

## Editorial rule

"Moreover / Furthermore / Additionally / Therefore / However" are not bad
words. They are bad only when the semantic relationship is absent or obvious
without them. Classify the relation, then ask whether it is real:

- `But/however` needs a real contrast.
- `Because/therefore` needs a real cause.
- `For example` needs actual evidence.
- `Moreover` needs an addition the reader could not infer.

Do not reward mechanical transitions. Do not assume more connectives = better.
A necessary bridge stays; decoration goes.
