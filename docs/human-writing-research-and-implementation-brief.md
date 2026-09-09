# What Human Writing Should Mean for Not Ai

Not Ai should help a real person make a clear, well-supported point in a way
that fits their audience. It should not try to manufacture a statistical
impression of humanness or help someone defeat an authorship detector.

That distinction is the product's strongest idea. It is also the practical one.
Model habits change quickly, and a sentence can have a so-called AI signal while
still being exactly right for its writer, field, and purpose. A useful editor
therefore starts with intention, evidence, and voice, then uses linguistic
patterns as prompts for review.

## The short answer

Build an **editorial accountability tool**, not a humanizer.

The product should ask five quiet questions before it changes prose:

1. What does this writer need the reader to understand, feel, decide, or do?
2. Which facts, claims, quotations, and terms are protected?
3. Which sentence carries the writer's actual point of view or decision?
4. Which passages are generic enough to fit a hundred unrelated pieces?
5. Which change makes the text clearer without pretending the writer lived,
   felt, or proved something they did not?

The fourth question is especially valuable. Call it the **genericity
counterfactual**: *could this sentence survive unchanged if the names, setting,
and topic were swapped?* If yes, it deserves scrutiny. The answer is not always
"delete it." It may be the right bridge sentence. But it is where a human editor
usually looks first.

This moves the goal from "sound human" to "sound owned." Owned writing has a
reason to exist in this situation, makes choices, carries appropriate evidence,
and leaves the writer responsible for what it says.

## What the supplied sources actually establish

### The Reinhart et al. paper

The supplied arXiv paper is now a peer-reviewed 2025 PNAS article, [*Do LLMs
write like humans? Variation in grammatical and rhetorical
styles*](https://doi.org/10.1073/pnas.2422455122). It is the best foundation in
the current repository because it does not reduce the question to a list of
banned words.

The team created parallel human and model continuations across several genres.
It used 66 lexical, grammatical, and rhetorical features, not just word counts.
The study found that instruction-tuned GPT-4o and Llama 3 variants often use a
denser, more noun-heavy register than the human continuation, even when given a
substantial human sample to imitate. In the reported corpus, GPT-4o used present
participial clauses at 5.3 times the human rate, nominalizations at 2.1 times,
and phrasal coordination at 1.9 times. The direction matters more than those
exact numbers.

The important finding is not "avoid -tion words." It is **genre mismatch**.
Models can produce polished grammar while failing to loosen, focus, take a
position, or vary their rhetorical moves in the way a writer does for a specific
audience. The article itself frames the work as a way to find teachable revision
moments, not a reason to police students.

There are limits. The research covers English, particular 2024-era models,
roughly 500-word continuations, and its sampled genres. It found good
classification within controlled source-model pairs, but cross-corpus and
cross-model generalization was harder. Its feature rates are population results,
not individual style rules or universal targets.

### The Wikipedia field guide

[Wikipedia's Signs of AI Writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing)
is useful as a large, practical record of what editors encounter. It is not a
Wikipedia policy, it says it needs updating for recent models, and it repeatedly
warns that its observations are not proof. That framing is correct.

Its strongest lesson is to separate three things that are often mixed together:

| Kind of signal | Example | What it should trigger |
| --- | --- | --- |
| Process residue | broken markup, an internal citation token, a fabricated reference | Verify the artifact and source immediately. |
| Content failure | vague attribution, inflated importance, unsupported future claims | Repair the claim, source, or scope. |
| Style pattern | repeated stock vocabulary, rigid triads, generic headings, copula avoidance | Read in context. Revise only if it weakens the piece. |

That last category is not evidence of authorship. It is a way to notice prose
that may be flat, padded, sales-like, or poorly fitted to the job at hand. A
human can write it. A model can avoid it. The actual quality problem is still
the quality problem.

## The wider evidence points in the same direction

| Evidence | What it supports for Not Ai | What it does not support |
| --- | --- | --- |
| [Reinhart et al., PNAS, 2025](https://doi.org/10.1073/pnas.2422455122) | Review rhetorical and grammatical fit by genre. | Fixed quotas for participles, nominalizations, contractions, or plain verbs. |
| [Jiang and Hyland, 2025](https://doi.org/10.1177/07410883251328311) | In argumentative essays, reader engagement and personal asides can reveal whether an argument is genuinely interactive. | Forcing questions or first person into every genre. |
| [Kobak et al., Science Advances, 2025](https://doi.org/10.1126/sciadv.adt3813) | Clusters of "excess" vocabulary can reveal a shifting production pattern at corpus scale. | Calling a single word proof that one document was AI-written. |
| [Sadasivan et al., 2023](https://arxiv.org/abs/2303.11156) | Text-only detection is fragile when prose distributions overlap and text is changed. | Promising a reliable authorship verdict from a final paragraph. |
| [Liang et al., 2023](https://arxiv.org/abs/2304.02819) | Detector design can unfairly flag non-native English writers. Fairness must be a release condition. | Treating standard, concise, or second-language English as suspicious. |
| [OpenAI's retired classifier notice](https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/) and [Turnitin's guidance](https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report) | Never present a detector score as authorship proof or disciplinary evidence. | Building a feature whose success is measured by detector movement. |

The evidence also gives a better reading of the word "human." Human prose is
not random, incorrect, casual, or full of quirky punctuation. A careful human
can write a formal paper with nominalizations, straight logic, and no
contractions. A human writing in a second language may choose predictable,
precise vocabulary. A good product must not punish either writer.

## A better product model: the Writer Ownership Loop

The product needs one stable object of optimization: **writer ownership**.
Ownership has five independently reviewable parts:

| Dimension | Editorial question | Good outcome |
| --- | --- | --- |
| Intent | Why is this being said now, to this reader? | The opening and order serve a real purpose. |
| Evidence | What in the source supports this statement? | Facts and claim strength survive the edit. |
| Agency | Who saw, decided, built, measured, or believes this? | The text names an actor when that matters and the source supports it. |
| Situation | What makes this document specific to its context? | Concrete supplied detail does real work instead of generic praise. |
| Voice | What repeated choices belong to this writer and genre? | The edit preserves useful oddness, formality, and restraint. |

The loop is simple:

```text
writing brief -> source ledger -> selective revision -> revision receipt -> human review
```

The **revision receipt** is the missing product layer. Alongside final prose,
the system should be able to say, in compact plain language:

- kept: protected fact, quote, technical term, or stated position;
- moved: a detail brought forward because it carries the paragraph;
- cut: framing that added no claim or evidence;
- clarified: an actor, relationship, or request made explicit from the source;
- needs input: a moment where only the author can supply a detail or judgment.

This creates an audit trail without claiming to prove who typed the words. It
also makes the tool more useful to a serious writer: they can accept, reject, or
correct an editorial decision rather than simply receive a smoother block of
text.

## The Human Output Benchmark

Do not create a single "human score." It will become a detector score under a
friendlier name. Create a **Human Output Benchmark** with separate gates and
human preference tests.

### What each benchmark case contains

Each case should include a source pack, intended audience and genre, protected
facts, a clear purpose, source text, and when consented, a short sample of the
same writer's own work. The reference answer is not one supposedly perfect
rewrite. It is a set of allowed claims and a review rubric.

Include at least these groups before claiming broad performance:

- personal narrative, email, product update, README, technical explanation,
  student report, academic abstract, and opinion piece;
- already-good human writing, where the correct behavior is little or no edit;
- formal and second-language English, so clarity is never treated as a fault;
- drafts with sparse notes, so the tool must show a bracketed need instead of
  inventing a memory or conclusion;
- pieces with valid dashes, curly quotes, passive voice, or nominalization, so
  style rules are tested against legitimate exceptions.

### Scorecard

| Gate or study | How to assess it | Release rule |
| --- | --- | --- |
| Source fidelity | Claim-to-source review plus protected-fact checks | No unsupported fact, quote, number, or strengthened conclusion. |
| Editorial restraint | Compare change volume with a human editor's judgment | Already-strong passages may remain unchanged. |
| Intent and genre fit | Blind reviewers receive purpose and audience | Revised version is preferred over the input or baseline. |
| Voice continuity | Where a consented sample exists, reviewers compare high-level traits | It should not erase the writer's register or useful idiosyncrasy. |
| Specificity and accountability | Reviewers flag generic sentences and missing agency | More source-supported specificity, not fabricated detail. |
| Fairness | Break results out by genre, formality, and English variety | No group carries a higher false-warning or unwanted-rewrite rate. |
| Mechanical correctness | Deterministic checks for empty output, malformed links, quote loss, and protected literals | A hard failure must correspond to an objective deliverable error. |

Every human study should be blinded and pairwise: reviewers see two versions,
the stated task, and the source pack where fidelity is judged. They answer
"which needs less author correction?" not "which seems more human?" The latter
question is subjective, easy to stereotype, and exactly what this project
should avoid.

Report results by genre and condition, with disagreement and confidence ranges.
Do not publish one aggregate number that lets a strong technical result hide a
weak personal-writing result.

## What should change in this repository

The canonical `SKILL.md` already has the right safety position: preserve facts,
do not invent experience, and do not optimize for a detector. Some bundled
artifacts still conflict with it. Reconcile those before adding new features.

| Current area | Problem | Direction |
| --- | --- | --- |
| `reference/profile.md` | It turns population averages into ceilings and floors and instructs writers to restore particular forms. | Keep the research as background, remove targets and imperative substitution recipes. |
| `reference/mechanical-tells.md` | It makes typography and a few stylistic choices absolute rules. | Recast these as genre-aware prompts; preserve valid author or publication style. |
| `reference/why-word-swapping-fails.md` | It records detector-score movement as a success measure. | Replace score-based evidence with source fidelity and reader-task outcomes. |
| `tools/not_ai_core/gate.py` | It hard-fails em/en dashes and curly quotes even though they can be valid human and house style. | Hard-fail only objective breakage. Surface style as a non-blocking, configured review note. |
| `scripts/scan_prose.py` and related checks | The repository's own quality check treats a lexical list as a pass/fail constraint. | Limit it to obvious residue and optionally use it as a review report, never as a prose purity test. |
| `benchmarks/` | The framework is thoughtful but the corpus is empty and quality proxies can be mistaken for quality. | Add consented, source-backed cases and human review records before relying on metric deltas. |

This is not a request to make the writing more informal. It is a request to stop
confusing a model-era signature with an editorial defect.

## Implementation plan

### Phase 0: align the product contract

1. Write one short, public definition of success: clear, specific,
   source-grounded, voice-preserving prose for the intended reader.
2. Audit every shipped skill, reference, script, README claim, and test for a
   conflict with that definition.
3. Delete or demote detector-score language, fixed linguistic quotas, and
   categorical punctuation bans.
4. Add a clear taxonomy: objective errors can block; content risks and style
   patterns can only ask for editorial review.

**Done when:** a user cannot reasonably interpret any shipped instruction as
"make this pass an AI detector."

### Phase 1: make the source ledger executable

1. Define a small `WritingBrief` input: purpose, audience, genre, source text,
   protected facts, constraints, and optional voice sample.
2. Ask the model to create a private claim ledger before it edits.
3. Add a deterministic checker for protected facts, numbers, citations, links,
   and code spans. It should flag a possible loss, not claim semantic proof.
4. Produce an optional revision receipt that maps meaningful changes to the
   source or labels them `needs author input`.

**Done when:** every example can explain where its key claims came from and why
its major edit was made.

### Phase 2: replace the purity gate with a context gate

1. Keep empty output and malformed artifact checks as errors.
2. Make quotes, dashes, contractions, sentence shape, vocabulary, and
   nominalization non-blocking signals with a genre and locale explanation.
3. Group signals into an editorial question rather than a count target. For
   example: "These three sentences make the same generic promise. Which one has
   evidence?"
4. Rank risks in this order: fabricated or lost content, unclear action or
   attribution, genre mismatch, then stylistic repetition.

**Done when:** an academic abstract, a British-style essay, and a personal note
can all pass without being pushed toward the same voice.

### Phase 3: build the benchmark before tuning further

1. Create 80 to 120 consented cases spread across the eight conditions above.
2. Store each case's source pack, protected facts, genre, permitted AI use, and
   human review notes beside the before-and-after text.
3. Compare the current skill, the revised skill, and a minimal-edit baseline in
   blinded pairwise review.
4. Add regression tests for no-invention, protected-content preservation,
   already-natural restraint, and valid style exceptions.
5. Publish per-genre outcomes and failures. Keep examples where the tool should
   ask for missing information or leave the draft alone.

**Done when:** the revised system wins on fidelity and reader usefulness without
creating a fairness regression for formal or second-language writers.

### Phase 4: release slowly and learn from edits

1. Ship the revision receipt and context gate behind an opt-in mode.
2. Collect only consented before-and-after pairs, with a way to mark a suggested
   edit wrong or unwanted.
3. Review false warnings by genre and locale each release.
4. Update model-era observations as research notes, never as universal rules.

**Done when:** the product can show not merely that the prose changed, but that
writers retained more control and readers found the result clearer.

## Decisions to keep firm

- Do not claim the final text is human-written, detector-safe, or
  indistinguishable from human text.
- Do not fabricate roughness, slang, mistakes, memories, emotion, or personal
  perspective.
- Do not penalize formal writing, non-native English, disability-related style,
  or a publication's house style.
- Do not let a vocabulary list overrule a precise word.
- Do not let a quality metric outrank a source-backed human review.

## Sources

1. Reinhart, Alex, et al. [*Do LLMs write like humans? Variation in grammatical
   and rhetorical styles*](https://doi.org/10.1073/pnas.2422455122). *PNAS*,
   2025. Supersedes the supplied 2024 arXiv version.
2. [Wikipedia: Signs of AI Writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
   WikiProject AI Cleanup advice page, accessed 10 September 2026.
3. Jiang, Feng Kevin, and Ken Hyland. [*Does ChatGPT write like a student?
   Engagement markers in argumentative essays*](https://doi.org/10.1177/07410883251328311).
   *Written Communication*, 2025.
4. Kobak, Dmitry, et al. [*Delving into LLM-assisted writing in biomedical
   publications through excess vocabulary*](https://doi.org/10.1126/sciadv.adt3813).
   *Science Advances*, 2025.
5. Sadasivan, Vinu Sankar, et al. [*Can AI-Generated Text be Reliably
   Detected?*](https://arxiv.org/abs/2303.11156), 2023.
6. Liang, Weixin, et al. [*GPT detectors are biased against non-native English
   writers*](https://arxiv.org/abs/2304.02819). *Patterns*, 2023.
7. OpenAI. [*New AI classifier for indicating AI-written text*](https://openai.com/index/new-ai-classifier-for-indicating-ai-written-text/),
   retired 20 July 2023 because of low accuracy.
8. Turnitin. [*Using the AI Writing Report*](https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report),
   accessed 10 September 2026.
9. Cornell Center for Teaching Innovation. [*AI and Academic
   Integrity*](https://teaching.cornell.edu/generative-artificial-intelligence/ai-academic-integrity),
   accessed 10 September 2026.
