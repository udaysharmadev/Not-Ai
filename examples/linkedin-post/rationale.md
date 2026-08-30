## Rationale: LinkedIn post

The platform conventions survive. The content does not, because there was none.

### Actions taken

| Source | Action | Result |
|---|---|---|
| "🚀 In today's rapidly evolving digital landscape, the ability to leverage cutting-edge technologies has become more crucial than ever before." | REMOVE | Emoji and frame together. The sentence names no technology and makes no claim. Nothing survives it. |
| "I've spent the last several months working with distributed systems, and I've come to realize that the key to success lies in fostering a culture of continuous improvement and meticulous attention to detail." | RESTRUCTURE, SPLIT, FLAG | Becomes "I spent the last few months on [the actual project, named]. Three things I got wrong going in." The reported experience is kept. The abstract-noun conclusion is cut, because a culture of continuous improvement is not what the author learned. |
| "Here are 3 key lessons I've learned:" | REMOVE | Announces a list that the formatting already announces. It is also what makes the listicle unsplittable: everything from this colon to the end of lesson 3 reads as one 69-word sentence, which is where the post's flattering burstiness score comes from. |
| "1. **Embrace the complexity.** Understanding the nuanced intricacies of distributed systems requires a comprehensive approach that takes multiple factors into consideration." | REPLACE, FLAG | "**The complexity was not the problem.** What kept breaking was [the specific cause] ... the fix was [what you actually did]." The lesson is inverted, because `embrace the complexity` is advice and the slot asks for an event. |
| "2. **Foster collaboration.** Building robust systems demands that we leverage the diverse perspectives of cross-functional teams to achieve transformative outcomes." | REPLACE, FLAG | "**Talking to the right people early beat talking to everyone often.**" The imperative becomes a claim with an edge to it, which is the difference between a lesson and a slogan. |
| "3. **Iterate relentlessly.** The most successful teams are those that continuously refine their processes, leveraging data-driven insights to drive meaningful improvements." | REPLACE, FLAG | "**One small change did most of the work.** Deployment time went from [X] to [Y] after [the specific change]. Nothing clever about it." |
| "What strategies have you found most impactful? I'd love to hear your thoughts in the comments below! 🌟" | REPLACE | "What is a systems problem you found was simpler than it looked?" The closing question is kept, because a question at the end is native to the platform. `impactful`, the comments-below instruction and the emoji are cut. |

### What was deliberately kept

Three lessons, in that order, with bold lead-ins and one short paragraph each. First person. Short paragraphs with blank lines between them. A closing question.

None of that is a machine pattern. It is how the platform is written, and `rules/context.md` protects genre conventions from being stripped as though they were tells. An agent that flattened this into three flowing paragraphs would have produced better prose and a worse LinkedIn post.

What changed inside the shape is that each lesson now states an outcome rather than issuing an imperative. `Embrace the complexity` tells the reader what to do. `The complexity was not the problem` tells them what happened, which they can disagree with.

### Measured before and after

```
python3 scripts/analyze_structure.py examples/linkedin-post/input.md
python3 scripts/analyze_structure.py examples/linkedin-post/output.md
python3 scripts/metrics.py examples/linkedin-post/output.md
```

| Measure | Before | After |
|---|---|---|
| Words | 142 | 184 |
| Sentences | 5 | 9 |
| Paragraphs | 7 | 6 |
| Mean sentence length | 28.0 | 20.3 |
| Burstiness | 0.799, ✓ good variation | 0.540 |
| Nominalization density | 56.3, ⚠ high | 16.3, ✓ normal |
| Mechanical transitions | 0 | 0 |
| AI-associated vocabulary | 14 unique, 15 occurrences | 0 |
| Lexical diversity | 94% | 92% |
| Flesch-Kincaid grade | 17.3 | 8.7 |
| Gunning Fog | 21.2, very difficult | 11.4, standard |
| Flesch Reading Ease | 21.9 | 68.8 |
| Density score | 52.1, high | 31.0, moderate |
| Hedges / boosters | 0 / 0, `absent` | 1 / 0, `too sparse to judge` |
| First-person markers | 5, 35.7 per 1,000 | 3, 16.4 per 1,000 |

**Nominalization 56.3 to 16.3 is the real change.** `Ability`, `improvement`, `attention`, `consideration`, `improvements` and `comments` are gone, and what replaced them are verbs with subjects: `what kept breaking`, `deployment time went from`, `I got wrong`. Three suffix matches remain, `complexity`, `collaboration` and `Deployment`, and all three are load-bearing: two are lesson titles the platform earns and the third names the thing that was measured. This is the measure most worth trusting across the whole example set, because it moved down in every one of the five rewrites and each time for the same reason.

**Grade level 17.3 to 8.7 and reading ease 21.9 to 68.8.** Both now match the platform. The abstract read at journal difficulty and should have; this post read at journal difficulty and should not have.

**Burstiness fell from 0.799 to 0.540, and the fall is an improvement.** The 0.799 came from the segmenter finding five sentences of 20, 33, 69, 7 and 11 words. The 69-word one was the whole listicle, held together by a colon and three bolded lead-ins so that nothing in it split; the 7 and the 11 were the engagement question and the sign-off. Break the listicle into real sentences and that spread collapses. The rewrite has nine sentences spread across one very short, two short, three medium, two long and one very long, which is real variation, and it scores lower.

Burstiness fell in three of the five rewrites in this set while the writing improved in all three. It rose in the other two, `examples/academic-abstract/` and `examples/personal-essay/`. A metric that moves in both directions on improvements, gives a human paragraph 0.200 and a generated post 0.799, is not measuring what its name suggests. One counterexample would be noise; this many is a finding about the instrument.

**The output is longer, 142 to 184 words.** Two causes. The 58-word flag block, which is instruction rather than deliverable, and the slots, which are verbose by design: `[how much rework, in whatever unit you measure it]` is nine words standing in for two. Between them the bracketed text is 96 of the output's 184 words, so more than half of what the scripts measure here is not the post. Filled in, the post lands near 120 words, shorter than the original.

**Hedges went from 0 to 1, and the balance verdict moved from `absent` to `too sparse to judge`.** The single marker is `could`, in `Once I could name that`, which is past ability rather than hedging. One marker sits below the three-marker floor, so the script declines to read a ratio from it. The refusal holds up on two counts: a single marker is too little to divide, and this marker is not doing the work its pattern implies. Both readings agree about the post itself, which makes no claim precise enough to need a hedge.

### Nine slots, and why the post is still worth delivering

`examples/gen-ai-article/` had four slots and the verdict was that no article existed yet. This post has nine and the verdict is different, because the author did the work. They spent months on a real project, something specific broke, someone should have been consulted earlier, and one change had an outsized effect. Those four facts exist in the author's memory and are absent from their draft. That is a retrieval problem, not an emptiness problem.

The generated version buried them under `fostering a culture of continuous improvement`, which is a phrase that fits any project in any industry in any decade. The rewrite is a form the author can fill in about fifteen minutes, and the filled version would be a post only they could have written.

If the slots cannot be filled, the same conclusion applies as in the gen AI article: there is no post here, and saying so is the useful answer.
