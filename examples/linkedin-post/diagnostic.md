## Diagnostic: LinkedIn post

Produced at Stage 2 of the procedure in `SKILL.md`. This is the example where the structural metrics come back with seven ticks and a single warning, and the text is still unmistakably machine-written.

```
NOT AI DIAGNOSTIC
Genre:    LinkedIn post, given by the platform conventions in the text itself.
Register: 2 of 5 intended, 5 of 5 delivered. That mismatch is the finding.

Working already:
  "I've spent the last several months working with distributed systems"
  The only clause in the post that reports something the author did. It is
  concrete about duration and domain, and it uses a contraction. No change
  needed. Everything attached to it after the comma is the problem.

Patterns found:
  emoji as structure      "🚀" opening, "🌟" closing, neither carrying meaning
  mechanical frame        "In today's rapidly evolving digital landscape"
  significance inflation  "more crucial than ever before"
  abstract-noun pivot     "the key to success lies in fostering a culture of
                          continuous improvement and meticulous attention to
                          detail"
  listicle announcement   "Here are 3 key lessons I've learned:"
  bolded inline headers   "**Embrace the complexity.**" and two more, each
                          followed by one sentence of abstraction
  rule of three           Exactly three lessons, imperative-verb titles,
                          near-identical sentence shape under each
  engagement bait         "What strategies have you found most impactful?
                          I'd love to hear your thoughts in the comments below!"

Vocabulary in context:
  "leverage" 2x           Problem. Once per lesson body, both times replacing a
  "leveraging" 1x         verb that would have specified an action.
  "cutting-edge" 1x       Problem. In "cutting-edge technologies", naming none.
  "comprehensive" 1x      Problem. "a comprehensive approach that takes multiple
                          factors into consideration" is nine words for nothing.
  "transformative" 1x     Problem. "transformative outcomes", unspecified.
  "robust" 1x             Problem here. Standard in systems writing, but
                          "building robust systems" is the whole claim and no
                          system is named.
  "crucial" 1x            Problem.
  "foster" 1x             Problem. Also the title of lesson 2.
  "nuanced intricacies"   Problem, and a tautology. Intricacies are nuanced.
  "distributed systems"   Fine. Domain term, correctly used.
  "cross-functional"      Fine. Ordinary at work, not a tell.
  "I've", "I'd"           Fine. Contractions belong on this platform. Keep.
  five more flagged       "fostering", "meticulous", "rapidly evolving",
                          "impactful", "meaningful". Each is cut or replaced with
                          the sentence it sits in, quoted above. The script
                          counts 14 unique terms and 15 occurrences in total.

Intervention: heavy
```

### Measured

```
python3 scripts/analyze_structure.py examples/linkedin-post/input.md
python3 scripts/metrics.py examples/linkedin-post/input.md
python3 scripts/repetition.py examples/linkedin-post/input.md
```

| Measure | Value |
|---|---|
| Words / sentences / paragraphs | 142 / 5 / 7 |
| Mean sentence length | 28.0 words |
| Burstiness | 0.799, ✓ Good length variation |
| Participial clause openers | 0 of 5, 0%, ✓ normal |
| Mechanical transitions | 0, ✓ none detected |
| Repeated openings | None, ✓ |
| Repeated phrases | None, ✓ |
| Lexical diversity | 94% content-word TTR, ✓ high |
| Nominalization density | 56.3 per 1,000 words, ⚠ high for this proxy |
| AI-associated vocabulary | 14 unique terms, 15 occurrences |
| Flesch-Kincaid grade | 17.3 |
| Gunning Fog | 21.2, very difficult |
| Flesch Reading Ease | 21.9 out of 100 |
| Density score | 52.1, high, characteristic of formal academic prose |

### Seven ticks and one warning on text nobody would mistake for human

Count the passes. Good length variation. No participial openers. No mechanical transitions. No repeated openings. No repeated phrases. High lexical diversity. Four unique paragraph shapes. A structural scan of this post comes back close to clean.

The text is still obviously generated, and everything that gives it away sits outside the structural analysis: the vocabulary list, the emoji, the listicle scaffolding, and the register.

Put this next to `examples/already-natural/`, where a human paragraph drew two warnings. The two examples fail in opposite directions on the same instruments. Neither result is a bug to be patched, because no threshold adjustment fixes both. This pair is what Stage 1 of `SKILL.md` means by `direction beats magnitude`: the scripts locate candidates and a reader decides.

**Burstiness of 0.799 is the sharpest case.** It is the highest figure in the example set and it earns an explicit `✓ Good length variation`. It is also an artifact of the scaffolding rather than of rhythm. The segmenter finds five sentences of 20, 33, 69, 7 and 11 words. The 69-word one is the entire listicle: `Here are 3 key lessons I've learned:` runs on into all three bolded lessons, because neither a colon nor a `**` ends a sentence. So the spread that earns the tick is produced by one unsplittable block of scaffolding at one end and the engagement question at the other, which are the two least human things in the post. The human paragraph in `examples/already-natural/` scores 0.200 on the same measure.

**Nominalization at 56.3 is the one warning, and it is the right one.** `Ability`, `improvement`, `attention`, `complexity`, `consideration`, `collaboration`, `improvements`, `comments`. Eight suffix matches in 142 words. Two of them survive the rewrite because they sit in lesson titles the platform's conventions earn, and one is the engagement bait; the proxy cannot tell those from the rest, which is why the reader has to look. What the reader finds is abstract nouns doing the work that verbs should do in a first-person post about something the author personally did.

**The register mismatch is the actual finding.** Gunning Fog of 21.2 and reading ease of 21.9 put this post in the same difficulty band as a journal article. The density score labels it `characteristic of formal academic prose`. It is a LinkedIn post. `examples/academic-abstract/` has almost the same profile, Fog 24.6 and ease -0.5, and there the numbers are appropriate. Same instruments, same readings, opposite verdicts, decided entirely by where the text is going.

**Zero hedges and zero boosters**, which the script reports as `absent`. An earlier version of the check called that `calibrated`, a clean bill of health on a post with no claim specific enough to hedge.

### What the rewrite is bounded by

The post reports no fact. Three lessons, none attached to a system, a change, a number or an outcome. As in `examples/gen-ai-article/`, rule 1 means the specifics cannot be supplied, so they become slots.

What can be kept is the shape. Three lessons, bold lead-ins, short paragraphs and a closing question are all native to the platform, and `rules/context.md` says genre conventions survive a rewrite. The emoji and the phrase `I'd love to hear your thoughts in the comments below` do not survive, not because they breach the platform's conventions but because they are the generic version of them.
