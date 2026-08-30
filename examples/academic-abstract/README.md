## Academic abstract

A generated abstract for an NLP paper. 140 words, five sentences, formal register that is entirely correct for the genre.

| File | |
|---|---|
| [input.md](input.md) | The generated abstract, 140 words |
| [diagnostic.md](diagnostic.md) | Stage 2 diagnostic and the measured figures |
| [output.md](output.md) | The rewrite, 108 words, six bracketed slots |
| [rationale.md](rationale.md) | Per-sentence accounting, the declared addition, and the metric that should be ignored |

**What this example is for.** Register discipline. Every other example in this set gets shorter, plainer and more conversational; this one must stay formal or it becomes unpublishable. The rewrite keeps third person, keeps the passive where the genre uses it, keeps `classification` and `availability` rather than reaching for verbs, and lands at grade 14.9 rather than the grade 6.0 that `examples/technical-passage/` reached.

It is also the example where a warning should be read and then declined. Nominalization density falls only from 92.9 to 83.3 and stays flagged as high, because academic abstracts nominalize by design. Compare `examples/technical-passage/`, where the same measure fell from 95.4 to 17.3 and the drop was the right outcome. Identical warning, opposite correct response, decided by genre.

Two smaller observations. This is the only input in the set where the participial-clause detector fires, because `Leveraging a novel experimental framework` puts the participle in the first word; the two `By ...ing` clauses in `examples/technical-passage/` were missed entirely. And burstiness rose here, 0.201 to 0.604, the only rewrite in the set where it moved in the expected direction.
