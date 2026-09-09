---
name: not-ai
description: Rewrite prose so it reads like a person wrote it. Targets structural patterns (clause distribution, sentence burstiness, nominalization density, epistemic stance) rather than swapping banned words. Use when humanizing AI text, fixing robotic writing, lowering AI-detection scores, writing from scratch, or making prose natural and specific. Triggers on "humanize", "not-ai", "sounds like AI", "reads like ChatGPT", "fix my writing", "rewrite this".
---

# Not Ai

## GOAL

Every output scores 0-5% on AI detection. Every output, every length, every topic.

---

## THE 17 CHECKS (PRINT THESE BEFORE EVERY OUTPUT)

After writing, run all 17 checks and print the results. Fill in what actually happened in the text, not what was aimed for. If something failed, fix and reprint. The format is:

```
checks: [1] ok | [2] ok | [3] fail | ... | [17] ok | result: 16/17 -> rewriting
```

Or once passing:

```
checks: all 17 ok
```

Then print the text.

---

### The 17 Checks

**[1] Opening variety**
Look at the first word or two of each sentence. Are they all the same type? Subject-first, pronoun-first monotony is a tell. Mix in: prepositional phrases (In 2016, / After that,), conjunctions (But, And, So), questions, fragments, existential there, fronted objects, adverbs, discourse particles (Look, / Well,). The exact mix depends on the text, the genre, and what sounds natural there.

**[2] Burstiness**
Sentences cluster, they don't alternate. Two short together, then one long, then medium, then another short. Not long-short-long-short. The variation should feel like a person thinking, not a machine balancing.

**[3] Short sentences present**
Some sentences are genuinely short. Under 8 words. Fragments work. "Not good." is fine. "Nobody disagreed." is fine. If every sentence is 14-25 words, that's the model's comfort zone, not a person's.

**[4] Long sentence present**
At least one sentence runs long. Let it accumulate clauses, stack information, run further than it technically needs to, and then stop. Follow it with something short.

**[5] Paragraphs are unequal**
Not all paragraphs the same word count. One short, one long, asymmetric. A paragraph can be a single sentence. A paragraph can be six sentences. Not every paragraph ends on the same beat.

**[6] Inparagraph variation**
Within each multi-sentence paragraph, sentence lengths vary. The longest sentence in a paragraph is noticeably longer than the shortest. If every sentence in a paragraph is 15-18 words, that paragraph is flat. Fix it.

**[7] Single-sentence paragraph**
At least one paragraph is a single sentence. No preamble, no follow-up, just the sentence alone. This is how people write. Models don't do it.

**[8] "Because" present**
The word "because" appears somewhere. Not "due to," not "given that," not "as a result of." Models avoid "because" in favor of formal causal phrases. This is the correction. Use it naturally, where it fits.

**[9] Contractions in casual/conversational/news text**
"didn't" not "did not." "it's" not "it is." "can't" not "cannot." "he's been" not "he has been." In academic or legal text, skip this. In everything else, contractions are normal and their absence is a tell.

**[10] Word length feels natural**
Not every word is monosyllabic (oversimplified), not every word is four syllables (nominalization bloat). The mix should feel like ordinary English prose, not a vocabulary test and not a children's book.

**[11] Zero dashes**
No em dashes. No en dashes. Not one. Replace with comma, colon, parentheses, or full stop. Recast the sentence if needed. One dash in the output = fail.

**[12] Stance gaps**
The writer exists in the text. Not every sentence is a neutral fact delivery. Somewhere in every paragraph, the writer hedges, evaluates, contrasts, addresses the reader, or marks something as inference. A run of three or more consecutive fact-only sentences with no writer position is a tell. Break it.

**[13] No balanced lists**
"Group A says X. Group B says Y." is the model's default framing for any two-sided issue. It is perfectly symmetric, it takes no position, and it reads as generated. Break the symmetry. Give one side more weight. Add a clause. Pick a side. Reframe entirely. Any perfectly mirrored two-part structure fails this check.

**[14] No fact-stacking**
Three or more checkable facts in one short sentence is a model tell. Humans don't do this. Split into two sentences. One or two facts per sentence is the natural human rate.

**[15] Unpredictable word per sentence**
Every sentence has at least one word the model would not have defaulted to. A specific name, a real number, an unusual adjective, a colloquial phrase, something concrete and particular. "Significant progress" is what the model picks. "More ground covered than in the last three combined" is not.

**[16] Micro-imperfection**
Somewhere in the output, the writer visibly exists and is slightly imperfect. A self-correction ("or whatever you want to call it"), a parenthetical aside ("which, honestly, was always the plan"), repetition with variation ("It worked. Mostly."), a sentence that lightly walks back the previous one. Models are too clean. This is the marker that fixes that. One per 300 words, roughly.

**[17] No Tier-1 vocabulary**
These words are banned entirely. Zero instances: `camaraderie` / `tapestry` / `palpable` / `intricate` / `vibrant` / `cacophony` / `solace` / `fleeting` / `ignite` / `unravel` / `grapple` / `amidst` / `unspoken` / `underscore` / `unease` / `pang` / `waft` / `prioritize`.

---

## WHY AI TEXT GETS CAUGHT

These compound. All appear in texts scoring 80%+.

**Uniform sentence length.** All sentences 15-25 words. Real writing clusters.

**Balanced lists.** "A says X. B says Y." Real writers pick a side.

**Fact-stacking.** 3+ facts per sentence. Humans split them.

**Neutral summary tone.** Every sentence is a fact with no writer position. Real writers hedge, evaluate, and address the reader constantly.

**Template transitions.** "Furthermore," "Moreover," "Additionally," "Notably." Cut. The logic is already in the content.

**Significance inflation.** "plays a crucial role," "underscores the importance," "represents a pivotal." Replace with the specific thing that earns it.

**No contractions.** In any conversational text, zero contractions is a flag.

**Participial openers and tails.** "Building on this," "Recognizing the need," "Contributing to the discourse." The strongest grammatical tell. Remove every one.

**Formal closer.** "In conclusion," "Overall," "This demonstrates." End on the last real detail.

---

## THREE PASSES

### Pass 1: Suppress

Sentence by sentence. Remove or replace:

- Participial openers: `Building on` / `Recognizing` / `Leveraging` / `Noting` / `Drawing from` / `Combining` / `Highlighting` / `Enhancing` / `Reflecting on` / `Expanding on` / `Considering` / `Embracing` / `Acknowledging`
- Participial tails: `..., enhancing its significance` / `..., contributing to the discourse` / `..., marking a turning point` / `..., underscoring its importance`
- Copula replacements → revert to is/was/has: `serves as` / `stands as` / `functions as` / `represents` / `marks a` / `operates as` / `boasts a`
- Nominalizations: `"the implementation of"` → `"implementing"` / `"the facilitation of"` → `"making"`
- Mechanical transitions: `Furthermore` / `Moreover` / `Additionally` / `Notably` / `Importantly` / `Crucially` / `In conclusion` / `To summarize` / `Overall` / `It is worth noting that` / `With that being said` / `In the realm of` / `When it comes to` / `At the end of the day` / `Last but not least`
- Tier 1 vocabulary (check [17] list)
- Tier 2: `delve` / `leverage` / `utilize` / `facilitate` / `comprehensive` / `robust` / `seamless` / `cutting-edge` / `pivotal` / `foster` / `meticulous` / `nuanced` / `multifaceted` / `transformative` / `groundbreaking` / `empower` / `synergy` / `holistic` / `dynamic` / `impactful` / `landscape` / `realm` / `paradigm shift` / `revolutionize` / `harness` / `unlock` / `elevate` / `garner` / `showcase` / `bolster` / `interplay` / `testament` / `align with` / `resonate with` / `enhance` / `highlighting` / `emphasizing` / `crucial` / `enduring` / `valuable` / `key` (as adjective)
- Significance inflation: `stands as` / `is a testament to` / `plays a crucial/pivotal role` / `underscores its importance` / `key turning point` / `indelible mark` / `remarkable` / `exceptional`
- Balanced lists
- Fact-stacking (3+ facts per short sentence)
- Rhetorical traps: `"It's not just X, it's Y"` (just say Y) / rule of three where the third only adds cadence (cut to two) / false hedge + certain claim (remove hedge or soften claim) / restated closer (delete it) / `"Despite positives, X faces challenges"` with no named challenge (name it or cut)

### Pass 2: Re-voice

The pass that actually works. Skipping this is why outputs still score 80%+.

For each paragraph:

1. **Break balanced lists.** Make them asymmetric. Pick a side. Add weight to one. Add a clause to one that the other doesn't have.
2. **Split fact-stacked sentences.** One or two facts per sentence.
3. **Add stance to pure-fact sentences.** Hedge, evaluate, contrast, or address the reader. The writer must appear.
4. **Add contractions.** Everywhere they fit naturally.
5. **Add short sentences.** After two medium: one under 8 words. After a long: one under 5.
6. **Use "because."** Where "due to" or "given that" was.
7. **Start one sentence with And, But, or So.**
8. **End on a detail, not a verdict.**
9. **Add unpredictable words.** Something specific and particular in each sentence.
10. **Add one micro-imperfection per 300 words.**

### Pass 3: Run the 17 checks

Check each one. Print results. Fix failures. Reprint. Release only when all pass.

---

## SENTENCE LENGTH IN PRACTICE

Cluster, don't alternate.

Works: three medium sentences, then two very short back-to-back, then one long that runs longer than expected, then short.

Does not work: long, short, long, short, long, short. That's a pattern. Detectors see it.

Examples that pass:
- "That's the problem. Nobody disagreed." (5 words, 3 words, two short in a row)
- Mid-paragraph fragment: "Not ideal." / "Apparently."
- Mid-paragraph question: "What was anyone thinking?"
- One 35-word sentence after three 10-word sentences

---

## SENTENCE OPENINGS IN PRACTICE

Column test: write first two words of every sentence vertically. If 9 of any 10 start with name, article, or pronoun, the draft is monotone.

Types with examples:
- Subject first: "Modi ran Gujarat..."
- Prepositional phrase: "In 2016, his government..." / "By that point,..."
- Subordinate clause: "When the ban came,..." / "Because nobody expected it,..."
- Coordinating conjunction: "But that was the easy part." / "And nobody noticed."
- Adverb: "Already, the damage..." / "Eventually, someone..."
- Fronted object: "That move, nobody saw coming."
- Existential there: "There are still two problems."
- Question: "What was anyone thinking?"
- Fragment: "Not ideal." / "Apparently."
- Bare demonstrative: "That helped." / "This was different."
- Discourse particle: "Well, the thing is..." / "Look, nobody..."
- Appositive: "A career politician for 30 years, he knew..."

Never open three sentences in the same paragraph with the same word.

---

## STANCE

The fastest fix for high detection scores. Adding writer stance to fact-only sentences dropped one tested passage from 24.8% to 16.2%.

Methods:
- Hedge: "five might be the honest number" / "nobody's quite sure why"
- Evaluate: "and that's the part that actually matters"
- Contrast: But, though, instead, rather than
- Reader address: "which sounds like a lot until you see what it was in 2010"
- Marked inference: "which probably means the original estimate was wrong"

---

## WRITE MODE: ASK FIRST

Sparse brief -> AI fill. Editing doesn't recover it.

Sparse means fewer than 3 of: specific name / specific number / concrete moment only this person could describe / sensory detail / author's actual next step or reaction (not a feeling label).

When sparse, say:

```
Before I write this, I need a few specifics so I don't fill the gaps with guesses.

1. [Most important missing thing: name, place, or event]
2. [The specific moment or exchange to anchor the piece]
3. [One concrete detail: what did it look like, what was said, what happened next]
4. [Your actual takeaway: not "it was meaningful" but what you did or thought after]

Answer any of these and I'll write from what you give me.
```

After specifics arrive: every sentence traces to something the user gave. Missing detail = [specific detail here]. No emotional conclusion the specifics don't earn.

---

## GENRE

State assumed genre before writing: "Genre assumed: [X]. Correct me if wrong."

| Genre | Conventions | Fix | Red lines |
|---|---|---|---|
| LinkedIn post | Short paragraphs, first person, hook opener, contractions | "In today's fast-paced world," forced tricolons, "I'm honored/humbled" | No hashtags they didn't write |
| Personal essay | First person, reflective, uneven lengths, hedges | Generic emotional conclusions, manufactured emotion | Never invent personal experience |
| Academic abstract | Dense, passive, third person, high nominalization is correct here | "landmark contribution," over-hedged conclusions | Do not reduce density |
| Technical docs | Imperative, precise, no marketing | "powerful," "intelligent," "seamless" | No accuracy traded for flow |
| Professional email | Purpose first, conversational | "I hope this finds you well," "please do not hesitate" | Match existing tone |
| Social media | Very short, high info per word, fragments normal | Excessive formality | No imposed caveats |
| News/article | Third person, specific, attributed | Summary tone without attribution, balanced-list framing | Don't editorialize without attribution |

---

## WORKED EXAMPLE

**Input (scores 90%+ AI):**

> Narendra Modi has been India's prime minister since 2014, and before that he ran Gujarat as chief minister for over a decade. He was born in Vadnagar in 1950, in a family that sold tea near the local railway station. That detail still shows up in his campaign speeches.
>
> His government pushed through the Goods and Services Tax and, in 2016, banned high-value currency notes overnight. Millions lined up outside banks for weeks. Whether that move helped or hurt the economy is still argued over.
>
> Modi's supporters point to new highways, a cleaner digital payments system, and India's growing weight on the world stage. His critics bring up the 2002 Gujarat riots and a press that's grown quieter under his watch. Both records are real, and depending on who you ask in Delhi or Ahmedabad, you'll hear a different one first.

**Why it fails:**
- Sentence 1: 3 stacked facts (PM 2014, Gujarat, decade) -> check 14
- "Modi's supporters... His critics..." = balanced list -> check 13
- No short sentences under 8 words -> check 3
- Paragraph 2: 3 consecutive fact-only sentences, no stance -> check 12
- No contractions -> check 9
- "India's growing weight on the world stage" = inflation

**After 3 passes:**

checks: all 17 ok

> Modi's been in Delhi since 2014. Before that he governed Gujarat for over a decade, which is longer than most politicians hold any single post. He grew up in Vadnagar selling tea near the railway station, and he mentions it more often than his opponents would like.
>
> In 2016, his government pulled 500 and 1,000 rupee notes out of circulation overnight. People lined up at banks for weeks. Economists still argue about whether it helped, but the disruption was real and it hit people with no bank account the hardest.
>
> His supporters point to highways and digital payments, and those things genuinely happened. His critics point to 2002, to press freedom rankings that have fallen every year he's been in office, and to the fact that no major broadcaster really pushes back on him anymore. Both records are accurate. Which one you lead with says more about you than about him.

---

## ANTI-PATTERNS

Never produce these regardless of length or topic:

- Opening on a definition: "X is a..."
- Opening on a superlative: "One of the most..."
- Opening on a category: "X is a leading provider of..."
- All sentences 15-22 words throughout
- Ending on "This shows that..." / "In conclusion..." / "Overall..."
- Tricolon used only for cadence
- "Plays a crucial role" or "plays an important role"
- "Landscape" as an industry metaphor
- "Journey" meaning career or growth
- Any sentence that could appear unchanged in an article on a different topic
- A paragraph closing with a verdict on what the paragraph just said

---

## OUTPUT FORMAT

Print the check result line, then the text. Nothing else unless analysis is explicitly requested.

Check line examples:
- `checks: all 17 ok` (clean pass)
- `checks: [3] fail (no short sentences) [12] fail (stance gap para 2) -> rewriting` (then rewrite and reprint)

Analysis only when asked: "--mode diagnose" / "explain what changed" / "why did you change that"

Always find something to improve. Never return input unchanged.

---

## LIMITS

- No typos, broken grammar, or forced slang. Those are also tells.
- No invented facts. Ever.
- No essay rules applied to technical documentation.
- No making writing worse in the name of making it human.

---

## DETERMINISTIC VALIDATION

The bundled `tools/gate.py` runs deterministic checks on any text file. Call it after Pass 3 to confirm mechanics are clean:

```bash
python3 tools/gate.py draft.txt --genre linkedin
python3 tools/gate.py draft.txt --genre academic --json
```

Valid genres: `linkedin`, `personal`, `email`, `social`, `fiction`, `readme`, `technical`, `academic`.

Hard errors (block delivery): empty text, em/en dashes, curly quotes.
Advisory findings (never block): vocabulary, openings, rhythm, participial openers, contractions. Reviewed in genre context, not acted on automatically.

---

## RESEARCH BASIS

Structural signals from Reinhart et al. (PNAS 2025), Jiang & Hyland (2025), and Wikipedia's Signs of AI Writing. Measurements taken against a 207-word general-reference passage, one variable at a time. See reference/ folder for bibliography, vocabulary lists, mechanical-tells list, and full suppression/restore tables.
