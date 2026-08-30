## Diagnostic: already natural

Produced at Stage 2 of the procedure in `SKILL.md`. The source is human writing, a paragraph from a developer's post about a production incident.

```
NOT AI DIAGNOSTIC
Genre:    Developer blog, personal incident note. Inferred.
Register: 2 of 5. Peers who have debugged something similar.

Working already:
  "Not fun, but at least I know what to look for next time."
  A fragment used deliberately, an honest assessment, and an ending that draws a
  conclusion from the experience rather than summarising the paragraph. Nothing in
  this sentence could be swapped into a post on another topic.

Patterns found:
  none

Vocabulary in context:
  none flagged

Intervention: none
```

Stop here. `SKILL.md` Stage 2: where the text is already good, say so and stop. Finding nothing is a valid result.

### Measured

```
python3 scripts/analyze_structure.py examples/already-natural/input.md
python3 scripts/metrics.py examples/already-natural/input.md
```

| Measure | Value | Script verdict |
|---|---|---|
| Words / sentences | 66 / 4 | |
| Burstiness | 0.200 | ⚠ Low burstiness: sentence lengths are very uniform |
| Nominalization density | 45.5 per 1,000 words | ⚠ elevated for this proxy |
| Participial clause openers | 0 of 4 | ✓ |
| Mechanical transitions | 0 | ✓ |
| AI-associated vocabulary | 0 | ✓ |
| Flesch-Kincaid grade | 7.3 | |
| Density score | 47.0 | moderate |
| First-person | 4, at 59.7 per 1,000 words | |

### The scripts raise two warnings on human writing

This is the point of the example, and it is not a hypothetical. Run the commands above and the toolkit flags genuinely human prose twice.

**Low burstiness, 0.200.** Four sentences of 15, 22, 17 and 13 words. Little variation, so the coefficient of variation is small. The paragraph reads fine because a reader responds to the fragment that opens the last sentence and to the specificity, not to length variance.

The comparison that matters: the machine-written academic abstract in `examples/academic-abstract/` measures **0.201**. Effectively identical. And the machine-written LinkedIn post in `examples/linkedin-post/` measures **0.799** and earns a ✓ Good length variation. On this set of six, burstiness does not separate human from machine at all, and where it discriminates it points the wrong way.

**Elevated nominalization, 45.5 per 1,000 words.** Three suffix matches in 66 words: `connection`, `condition` and `reconnection`. These are the correct technical words for what happened. There is no rewrite that lowers this number without making the sentence worse.

### What follows

Two of nine measures fire on a text that needs no changes. That is why `SKILL.md` forbids reporting a score and forbids stating a conclusion about authorship: the numbers are inputs to a reading, not a verdict.

It is also why Stage 5 question 2 exists, "Where did I over-edit a sentence that was already working?" An agent that treats a ⚠ as an instruction will rewrite this paragraph, and every available edit makes it worse. `rationale.md` shows what that looks like.

### On the em dash in the source

The input contains one:

```
The issue was in how we handled connection timeouts — specifically, a race condition
between the health check and the reconnection logic.
```

A human wrote it. It is used correctly, as a single break introducing a clarification, and removing it would be an edit made to satisfy a detector rather than a reader. `references/wikipedia-signs.md` covers why em dash frequency has become a weak signal and why the paired parenthetical form is the part still worth noticing. This is not that form.
