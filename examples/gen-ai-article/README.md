## Gen AI article

A generated article opening about generative AI. Five sentences, 99 words, and no facts.

| File | |
|---|---|
| [input.md](input.md) | The generated paragraph, 99 words |
| [diagnostic.md](diagnostic.md) | Source diagnostic and measured figures |
| [output.md](output.md) | Two sentences and a flag block |
| [rationale.md](rationale.md) | The accounting, and the fabricated rewrite this repository used to ship |

**What this example is for.** It is the test case for rule 1, never fabricate. The input contains no checkable claim anywhere, so a rewrite cannot contain one either. The correct output is short, mostly slots, and it tells the author that there is no article here yet.

`rationale.md` reproduces what an earlier version of this repository shipped as the correct output: a well-paced, specific, readable paragraph in which every specific was invented. That version also claimed to have removed three em dashes while shipping two. Both failures are why the current quality gate checks source fidelity and requires the revision receipt to match the actual edit.

It also shows a measurement trap. Three flagged vocabulary terms survive into the output, all of them inside the flag block that quotes them as examples of what was cut. The script measures a file, not a deliverable.
