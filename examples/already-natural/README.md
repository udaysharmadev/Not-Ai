## Already natural

Human writing that needs no changes. A paragraph from a developer's post about a production incident.

| File | |
|---|---|
| [input.md](input.md) | The source paragraph, 66 words, human-written |
| [diagnostic.md](diagnostic.md) | Stage 2 diagnostic, and the two warnings the scripts raise on it |
| [output.md](output.md) | The input reproduced verbatim, plus a note on why nothing changed |
| [rationale.md](rationale.md) | Why nothing changed, and both ways an agent could get this wrong |

**What this example is for.** The scripts flag human writing. Run them and `analyze_structure.py` reports low burstiness at 0.200 and elevated nominalization at 45.5 per 1,000 words on a paragraph that a person wrote about their own week.

The burstiness comparison across this example set is worth the whole file: this human paragraph scores 0.200, the machine-written academic abstract scores 0.201, and the machine-written LinkedIn post scores 0.799 with a ✓ Good length variation. The metric does not separate the two populations here, and where it discriminates it points the wrong way.

`rationale.md` then shows the two failure modes in full: over-humanization, which buries the specifics in performed enthusiasm, and metric-chasing, which fabricates a fact to raise burstiness and removes the term `race condition` to lower nominalization. Both improve a number. Both damage the writing.
