## LinkedIn post

A generated LinkedIn post about distributed systems. 142 words, two emoji, three lessons, no facts.

| File | |
|---|---|
| [input.md](input.md) | The generated post, 142 words |
| [diagnostic.md](diagnostic.md) | Stage 2 diagnostic and the measured figures |
| [output.md](output.md) | The rewrite, nine bracketed slots |
| [rationale.md](rationale.md) | Per-sentence accounting, what the platform gets to keep, and the burstiness finding |

**What this example is for.** It is the counterpart to `examples/already-natural/`, and the pair is the most useful thing in this repository. There, a human paragraph drew two warnings. Here, generated text collects seven ticks: good length variation, no participial openers, no mechanical transitions, no repeated openings, no repeated phrases, 94% lexical diversity, four unique paragraph shapes. A structural scan comes back close to clean on a post nobody would mistake for human.

Everything that gives it away sits outside the structural analysis: fourteen flagged vocabulary terms in 142 words, the emoji used as structure, the listicle scaffolding, and a register pitched at journal difficulty for a feed. Read the two examples together and the argument for reading before concluding makes itself.

The burstiness case is the sharpest one in the set. This post scores 0.799 with an explicit `✓ Good length variation`, the highest figure of any file here, and the score comes from a segmentation artifact. The lengths are 20, 33, 69, 7 and 11 words. The 69-word one is the whole listicle, which never splits because it is held together by a colon and three bolded lead-ins, and the two short ones are the engagement question and the sign-off. The human paragraph in `already-natural` scores 0.200.

It is also the clearest demonstration that genre conventions are not tells. The rewrite keeps three lessons, bold lead-ins, short paragraphs and a closing question, because that is how the platform is written. What changes is that each lesson now reports an outcome instead of issuing an imperative.
