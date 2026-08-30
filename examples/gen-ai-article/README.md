## Gen AI article

A generated article opening about generative AI. Five sentences, 99 words, and no facts.

| File | |
|---|---|
| [input.md](input.md) | The generated paragraph, 99 words |
| [diagnostic.md](diagnostic.md) | Stage 2 diagnostic and the measured figures |
| [output.md](output.md) | Two sentences and a flag block |
| [rationale.md](rationale.md) | The accounting, and the fabricated rewrite this repository used to ship |

**What this example is for.** It is the test case for rule 1, never fabricate. The input contains no checkable claim anywhere, so a rewrite cannot contain one either. The correct output is short, mostly slots, and it tells the author that there is no article here yet.

`rationale.md` reproduces what an earlier version of this repository shipped as the correct output: a well-paced, specific, readable paragraph in which every specific was invented. That version also claimed to have removed three em dashes while shipping two. Both failures are why Stage 5 of `SKILL.md` ends with the question "do the changes I am about to describe match the changes I actually made".

It also shows a measurement trap. Three flagged vocabulary terms survive into the output, all of them inside the flag block that quotes them as examples of what was cut. The script measures a file, not a deliverable.
