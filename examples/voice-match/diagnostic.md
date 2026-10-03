## Diagnostic: voice match

A stiff project update measured against its author's own voice file before
rewriting. The reference (`voice.md`, 304 words) is stable; the draft (116
words) is not the author's.

```
NOT AI DIAGNOSTIC
Genre:    Technical update, inferred from the migration facts and the
          Friday decommission deadline.
Register: 0 of 5 expected, 5 of 5 delivered. Mira's file asks for short
          sentences, contractions, numbers before adjectives, and no
          lessons. The draft has none of the first two and ends on a
          warning phrased as a lesson.

Working already:
  "All 14 services were fully operational within four minutes"
  "The old cluster will be decommissioned on Friday."
  Two checkable claims with numbers and a date. Everything else in the
  draft is packaging around these two sentences.

Patterns found:
  empty frame          "It is worth noting that the team has successfully
                       completed" Opens by announcing that news follows.
  nominal stack        "The implementation of the migration methodology
                       leverages a robust orchestration framework, ensuring
                       a seamless transition" Three nominalizations, one
                       mid-sentence participle tail, and an orchestrator
                       that is never named.
  balanced pair        "pivotal milestone in our infrastructure evolution
                       journey" / "exceptional synergy ... collaborative
                       environment ... transformative initiative" Two
                       paragraphs of praise with no new fact between them.
  decoration           "Furthermore," + "underscores the meticulous planning"
                       Transition and verb both doing ceremony, not work.

Voice comparison (reference 304 words -> draft 116):
  CV              0.616 -> 0.283  drifted (no short sentences at all)
  short rate      0.458 -> 0.143  drifted
  self-mention   62.5 -> 8.6/1k   drifted ("team" where the file says "we")
  contractions   16.4 -> 0.0/1k   drifted
  function gap    5.21/1k         drifted
  specificity     aligned          numbers and names survive; the diction
                                  around them does not
  opener entropy  3.43 -> 2.13    "the" opens 3 of 7 sentences

Measured (analyze_structure + gate, technical):
  sentences 7, burstiness 0.287, participial total 0,
  nominalizations 77.6/1k, stock terms 9 unique / 10 hits
  (comprehensive, robust, seamless x2, transformative, pivotal,
  fostering, meticulous, facilitated, underscores),
  transitions "furthermore" + "it is worth noting", FK grade 16.2.
```

The comparison is the point of this example, so read its limits first:
every verdict above is a prompt to re-read, and with 116 words against 304
the function-word gap is noisier than it looks. What is not noisy is the
direction: zero contractions against 16.4, zero short sentences against a
46% short rate, and "the team" three times where the author's file says "we
when the team did it."
