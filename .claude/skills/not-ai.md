---
name: not-ai
description: Rewrite prose so it scores 0-5% on AI detection. Targets perplexity (word-level predictability), burstiness (variance across sentences), and morphosyntactic patterns that detectors measure. Not vocabulary substitution. Use when humanizing AI text, fixing robotic writing, lowering AI-detection scores, writing from scratch, or making prose natural and specific. Triggers on "humanize", "not-ai", "sounds like AI", "reads like ChatGPT", "fix my writing", "rewrite this".
---

# Not Ai

## HOW DETECTORS WORK

Read this before touching a word. Everything else follows from it.

**Perplexity.** At each word, a language model asks: how likely is this word given everything before it? AI text has low perplexity because generation algorithms (beam search, top-p, temperature sampling) select high-probability tokens. Every word is the expected choice. Human writers do not optimize for probability: they use unexpected constructions, personal idioms, specific proper nouns, and colloquial detours that the model would not predict. Human perplexity runs 50-150+. AI perplexity runs 10-30.

**Burstiness.** The variance in perplexity across sentences. Human text has high burstiness: two plain predictable sentences, then a sentence full of specific details and personal commentary, then something short and almost fragmentary. AI text is uniformly smooth, sentence after sentence, uniformly low-perplexity. Coefficient of variation (CV) for human text: >0.55. For AI text: <0.30.

**What this means for rewriting.** Structural changes alone (sentence length variation, paragraph asymmetry) reduce scores from 100% to ~39%. Getting below 5% requires word-level unpredictability injection. That is what this skill does.

---

## WHAT DETECTORS SPECIFICALLY FLAG

**GPTZero Model 4.9b** (August 2026, calibrated against GPT-5, Claude 5, Gemini 3.6) identifies four named patterns:

1. **Forced triads.** Three-item lists where the third item exists only for cadence. "Speed, flexibility, and reliability." "Fostering innovation, driving growth, and boosting engagement." Cut to two items, or give the third item real weight.

2. **Contrastive dilemmas.** Negative parallelism. "It is not just about X, but about Y." "While A presents challenges, it also unlocks B." Break the symmetry. Pick a side. Rewrite as a direct claim.

3. **Elevated symbolism.** Unearned metaphorical language on ordinary facts. `testament to`, `beacon of`, `pivotal milestone`, `rich tapestry`. Replace with the specific thing that earns the description.

4. **Participial tails.** Trailing `-ing` clauses that restate the sentence without adding information. "...enhancing its overall significance." "...underscoring the importance of modern architectures." "...contributing to the ongoing discourse." Cut them entirely.

**ZeroGPT DeepAnalyse** checks:
- Token predictability across every word
- Sentence length regularity (consecutive sentences in a narrow word-count band)
- Mechanical transition density
- Copula replacement rates (`serves as`, `functions as` instead of `is`)
- Semantic vector smoothness (machine text transitions smoothly in embedding space; human text makes abrupt topical shifts)

---

## BEFORE STARTING: IDENTIFY WHAT TO TOUCH

Not all content is prose. Identify first.

**Skip entirely (do not touch):**
- Code blocks (fenced with ``` or indented). GPTZero already masks these with paratext masking. They do not affect the score.
- Mathematical equations and formulas
- Numbered requirements lists, table headers, column names
- Direct quotations and citations
- Technical terms and proper nouns: never paraphrase. "TF-IDF" stays "TF-IDF."
- Section headings unless they contain inflated phrasing

**Rewrite aggressively:**
- All prose paragraphs
- Introduction, conclusion, methodology, discussion sections
- Any sentence that could appear unchanged in a Wikipedia article on a different topic

---

## GENRE

State the assumed genre before rewriting: "Genre assumed: [X]. Correct if wrong."

**Student academic / mini-project report:**
First person is not just allowed, it is required for a realistic score. A student writing about their own work says "I built", "I found", "I chose", "I ran", "I suspect", "I wasn't sure why". The absence of first person in a student project report is itself an AI signal. Admissions of confusion, specific results from actual experiments, and personal commentary on choices all raise perplexity. Rules for this genre are in their own section below.

**Formal academic paper (journal/conference):**
Third person, formal. Keep high nominalization where it is scientifically necessary. Do not reduce to Anglo-Saxon verbs at the cost of precision. Stance comes through hedging language, not personal pronoun use.

**Technical documentation:**
Imperative voice. Precision over variety. No marketing adjectives. No cadence triads.

**Blog / LinkedIn / social:**
Contractions everywhere they fit. First or second person. Short paragraphs. Fragments allowed. Personal stance mandatory.

**Professional email:**
Purpose first sentence. Match the recipient's register. Cut pleasantries.

---

## THE 17 CHECKS (PRINT BEFORE EVERY OUTPUT)

After rewriting, run all 17 and print results in this format:

```
checks: [1] ok | [2] ok | [3] fail | ... | [17] ok | result: 16/17 -> rewriting
```

or:

```
checks: all 17 ok
```

Fix failures. Reprint. Release only when all pass.

---

**[1] Opening variety**
First two words of every sentence, written vertically. No type used more than 3 times in any 10 consecutive sentences. Banned as openers: "It is", "This is", "This demonstrates", "One of the most", "There are many", "X is a Y that", "The X of Y is". Required variety: prepositional phrases, conjunctions (And/But/So), questions, adverbs, inverted constructions, fragments, discourse particles (Well,/Look,/Honestly,).

**[2] Burstiness (CV > 0.55)**
Sentences cluster by predictability, not just length. Two plain sentences, then one sentence with a specific proper noun, an exact number, or a personal comment. Not smooth-smooth-smooth throughout. The variance between the most and least surprising sentences must be visible and felt.

**[3] Short sentences present**
At least one sentence under 8 words per 400 words of prose. Fragments count. "Nobody agreed." counts. "That was the problem." counts. If every sentence runs 14-25 words, this check fails.

**[4] Long sentence present**
At least one sentence past 35 words per 400 words. Stack clauses. Let it breathe. Follow with something short.

**[5] Paragraphs unequal**
Longest paragraph at least 3x the word count of the shortest. Not all the same size. One paragraph can be a single sentence.

**[6] Within-paragraph variation**
In any multi-sentence paragraph, longest sentence at least 2x the shortest. If every sentence in a paragraph is 15-20 words, the paragraph is flat and fails.

**[7] Single-sentence paragraph**
At least one paragraph with exactly one sentence. Nothing before it in that paragraph, nothing after.

**[8] "Because" present**
The word "because" appears at least once per 600 words of prose. AI uses it at 19-20% of the human rate, substituting `due to`, `given that`, `owing to`, `as a result of`. Put "because" back where causation is implied.

**[9] Contractions in non-academic text**
In any student-project, blog, email, or conversational register: contractions are normal. "didn't" not "did not." "it's" not "it is." "can't" not "cannot." Zero contractions in conversational text is a flag. Skip for formal journal papers.

**[10] First person where genre demands**
For student project reports, personal essays, blog posts: "I", "we", "my", "our" appear. Their absence in genres where they are expected is an AI signal. A student writing about their own mini-project says "I found", "I chose", "I ran". For formal academic papers, skip.

**[11] Zero dashes**
Zero em dashes. Zero en dashes. Not one. Replace with comma, colon, parentheses, or a full stop. One dash = fail.

**[12] Stance gaps filled**
No run of 3+ consecutive fact-only sentences without a stance marker. In every paragraph: hedge, evaluate, contrast, address the reader, or mark as inference. "I think", "probably", "which is odd", "surprisingly", "in retrospect", "I wasn't sure why" all count.

**[13] No balanced lists**
"Group A says X. Group B says Y." broken. Break the symmetry. Give one side more detail. Pick the more important one and develop it. Perfectly mirrored two-part structures fail.

**[14] No fact-stacking**
Maximum 2 checkable facts per sentence. 3+ facts in one short sentence is a pattern detectors catch. Split.

**[15] Unpredictable word per sentence**
Every sentence has at least one word the model would not have defaulted to. A specific name. An exact number. An unusual but accurate adjective. A colloquial phrase. "Significant results" is predicted. "Results that caught me off guard" is not.

**[16] Micro-imperfection present**
One per 300 words: a self-correction ("or rather,"), a parenthetical admission ("which took longer than it should"), a sentence that qualifies the previous one, a hedge that admits genuine uncertainty. Models are too clean. This is the marker that fixes that.

**[17] No Tier-1 vocabulary**
Zero instances of: `camaraderie` / `tapestry` / `palpable` / `intricate` / `vibrant` / `cacophony` / `solace` / `fleeting` / `ignite` / `unravel` / `grapple` / `amidst` / `unspoken` / `underscore` / `unease` / `pang` / `waft` / `prioritize`.

---

## THREE PASSES

### Pass 1: Suppress

Sentence by sentence. Remove or replace every instance:

**Participial openers (cut or convert to finite verb):**
`Building on` / `Leveraging` / `Recognizing` / `Considering` / `Highlighting` / `Drawing from` / `Combining` / `Acknowledging` / `Emphasizing` / `Addressing` / `Integrating` / any `-ing` word followed by a comma at the sentence start

**Participial tails (cut entirely):**
`..., enhancing its significance` / `..., underscoring the importance` / `..., contributing to the discourse` / `..., marking a turning point` / `..., fostering collaboration` / any trailing `-ing` clause that restates the sentence

**Copula avoidance (revert to is/was/has):**
`serves as` / `stands as` / `functions as` / `operates as` / `marks a` / `boasts`

**Mechanical transitions (cut, rely on logic):**
`Furthermore` / `Moreover` / `Additionally` / `Notably` / `Importantly` / `Crucially` / `In conclusion` / `To summarize` / `Overall` / `It is worth noting that` / `With that being said` / `At the end of the day` / `Last but not least` / `In the realm of` / `When it comes to`

**High-probability AI phrases (cut or rewrite):**
`sits at the intersection of` / `plays a crucial/pivotal role` / `A few things stand out` / `it is important to note` / `this demonstrates the importance of` / `a testament to` / `beacon of` / `in today's fast-paced world` / `not just X but Y` (symmetry structure)

**AI Tier-2 vocabulary (replace with plain verbs and nouns):**
`delve` / `leverage` / `utilize` / `facilitate` / `comprehensive` / `robust` / `seamless` / `cutting-edge` / `pivotal` / `foster` / `meticulous` / `nuanced` / `multifaceted` / `transformative` / `groundbreaking` / `empower` / `synergy` / `holistic` / `dynamic` / `impactful` / `landscape` (as metaphor) / `realm` / `paradigm shift` / `revolutionize` / `harness` / `testament`

**Forced triads (cut third item if it adds only cadence, or give it real weight):**
Any three-item list where the third item is semantically redundant with the first two

**Fact-stacking (split):**
Any sentence with 3+ checkable facts under 25 words

### Pass 2: Re-voice and Inject

This is the pass that drops scores from 40% to under 5%. Skipping it is why outputs still score high.

For every paragraph, work through this list:

1. **Inject first person where genre allows.** "I ran four models" not "four models were run." "I chose TF-IDF because" not "TF-IDF was chosen because." "I found that preprocessing mattered more than expected."

2. **Replace vague with specific.** "the accuracy numbers back that up" becomes the actual numbers. "most student setups" becomes "a laptop with 8 GB RAM." "good results" becomes "87.3% F1 on the test set."

3. **Restore "because."** Where `due to` / `given that` / `as a result of` appear, replace with "because." Where causation is implied but unstated, make it explicit with "because."

4. **Restore the pro-verb "do."** "the second run took longer than the first did" not "the second run took longer than the first." AI underuses "do" at 25% of the human rate.

5. **Add existential "there."** "There are three problems here" not "Three problems exist." AI underuses it at 42-71% of the human rate.

6. **Add stance every third sentence.** After two fact sentences, one sentence that evaluates, hedges, or shows the writer thinking. "I'm not sure why SVM underperformed, but I suspect the hyperparameter grid was too narrow." "Which, honestly, was the more surprising result."

7. **Replace predicted words with less-predicted accurate alternatives.** Sentence by sentence: the adjective, verb, or noun the model would most likely choose, replace with one that is accurate but less expected. "performed well" becomes "held up." "demonstrates" becomes "shows" or "points to." "significantly" becomes "by a noticeable margin."

8. **Add contractions in casual and student-project text.** Everywhere they fit without sounding forced.

9. **Start at least one sentence with And, But, or So.** AI underuses these as openers.

10. **Add one micro-imperfection per 300 words.** A parenthetical "(which surprised me)", a qualification "or at least that's what the validation loss suggested", a light walkback "It worked. Mostly."

11. **End paragraphs on a detail, not a verdict.** The last sentence should be specific, not summarizing.

### Pass 3: Run the 17 Checks

Check each one against the text. Print results. Fix failures. Reprint. Release only when all 17 pass.

---

## PERPLEXITY INJECTION TECHNIQUES

These are what push scores from 20% to under 5%. They work at the word level.

**Verb choice.** Replace the highest-probability verb:
- `demonstrates` becomes `shows` / `reveals` / `points to`
- `is designed to` becomes `tries to` / `works by`
- `achieves` becomes `gets to` / `reaches`
- `indicates` becomes `suggests` / `points to`
- `utilizes` becomes `uses`
- `facilitates` becomes `makes`

**Adjective specificity.** Replace generic evaluative adjectives:
- "significant improvement" becomes "a 6-point jump in F1"
- "robust model" becomes "a model that didn't fall apart on the test set"
- "effective approach" becomes "an approach that worked, more or less"
- "comprehensive pipeline" becomes "a full pipeline from raw CSV to Flask endpoint"

**Colloquial anchors.** One per paragraph in casual and student writing:
- "basically", "honestly", "sort of", "anyway", "for what it's worth", "which is kind of the point"

**Personal hedges.** For student and personal writing:
- "I think", "I suspect", "I'm not sure why, but", "in my experience with this dataset", "as far as I could tell", "my guess is"
- These raise perplexity sharply because instruction-tuned models underuse them at 50-67% of the human rate.

**Specific numbers and proper nouns.** Every exact number is high-perplexity. Every name specific to your actual work is high-perplexity.
- "87.3% accuracy" is higher perplexity than "high accuracy"
- "on a MacBook M1" is much higher perplexity than "on standard hardware"
- "the Amazon product reviews dataset" is higher perplexity than "a large labeled dataset"

**Unexpected prepositions and structures:**
- "going by", "working from", "provided that I had"
- Stranded prepositions: "the approach I ended up going with" / "the thing I was thinking of"
- Bare demonstratives: "That helped." / "This was different." (not "This finding demonstrates that...")

**Mean word length control.**
Human average: 4.4 characters per word. AI average: 5.0-5.1. Latinate nouns and suffixes (`-tion`, `-ment`, `-ity`, `-ence`, `-ance`) push the average up. After rewriting, if the text still feels dense with long words, replace Latinate nouns with Anglo-Saxon equivalents where meaning permits.

---

## STUDENT / ACADEMIC PROJECT REPORT (GENRE-SPECIFIC)

Most student project reports score 80%+ because they are written in generic textbook prose with no personal voice. The fix is direct.

**What a student actually writes that AI does not:**
- First person throughout: "I built", "I found", "I chose", "I decided", "I ran"
- Specific results from actual experiments: exact numbers, not "high accuracy"
- Admissions of confusion: "This took me three days to figure out"
- Commentary on why choices were made: "I picked Logistic Regression not because it's theoretically best, but because it's fast to iterate on and I could explain the coefficients in a viva"
- Hedged conclusions: "I think SVM underperformed because the hyperparameter grid was too narrow, but I can't be certain"
- Informal asides in otherwise formal sections: "(which is a bit counterintuitive)", "(fair warning: this step is slow)", "(this surprised me)"

**What to keep formal in project reports:**
- Technical definitions (first use of a term, abbreviation expansion)
- Dataset descriptions (keep precise)
- Code and equations (do not touch)
- Citations and references

**Red lines for this genre:**
- Never invent results that were not obtained
- Never invent personal experiences that did not happen
- If results are not yet available, say so plainly
- Never change technical terminology

**Specific pattern replacements for student project writing:**

| AI version | Human student version |
|---|---|
| "The project covers the full pipeline" | "I built the full pipeline" |
| "Four algorithms get trained and compared" | "I trained and compared four algorithms" |
| "This project sticks to a traditional ML pipeline" | "I stuck with a traditional ML pipeline" |
| "It sits at the intersection of NLP, text mining..." | Delete. Say what it specifically is. |
| "A few things stand out from the literature" | "Three things struck me as worth carrying forward" |
| "This project leans on machine learning" | "I used machine learning" |
| "The sections below walk through each stage" | "What follows goes through each stage, one at a time" |
| "Machine learning changed that" | "Machine learning replaced them for most tasks" |
| "the accuracy numbers back that up" | Give the actual numbers |
| "most student setups can offer" | "a laptop with 8 GB RAM" |

---

## WORKED EXAMPLE (STUDENT PROJECT REPORT GENRE)

**Input (scores 80%+ AI on both ZeroGPT and GPTZero):**

> Sentiment analysis has been studied for more than twenty years now. The earliest approaches were lexicon-based: each word in a sentence got a sentiment score from a fixed dictionary such as SentiWordNet or VADER, and the scores were summed up to reach an overall verdict. Machine learning changed that. Naive Bayes, Logistic Regression, and Support Vector Machines became the go-to choices for sentiment classification, usually paired with Bag-of-Words or TF-IDF features. Deep learning pushed things further still. A few things stand out from the literature. Preprocessing quality matters no matter which algorithm sits on top of it, because a model trained on messy input rarely recovers from that. This project sticks to a traditional ML pipeline, with a deep learning extension left optional, because it fits a college project's actual constraints: reasonable accuracy, a model you can explain in a viva, and hardware most students already own.

**Why it scores high:**
- "A few things stand out from the literature": named AI phrase, extreme perplexity drop
- Three-item list: Naive Bayes, Logistic Regression, SVM (forced triad)
- No first person despite this being a student's own project
- Zero specific numbers from actual experiments
- "Preprocessing quality matters no matter which algorithm sits on top of it": GPTZero flags this sentence as high AI impact
- Uniform sentence perplexity throughout, no burstiness

**After three passes:**

checks: all 17 ok

> Sentiment analysis is a twenty-year-old problem, which is long enough for three distinct generations of approaches to rise and fall in favor.
>
> The first generation was lexicon-based. Tools like VADER or SentiWordNet assigned a numeric sentiment score to each word, then summed them to reach a verdict. Fast and easy to explain. But they break almost every time a reviewer is sarcastic or uses negation, which product reviews do constantly.
>
> Machine learning replaced them for most practical tasks. Naive Bayes and Logistic Regression became the default starting points, mostly because they train quickly on sparse TF-IDF features and don't need a GPU. I went with this approach for the same reason: my laptop handles it, and I can explain the model's coefficients to an examiner without hand-waving.
>
> Deep learning pushes accuracy higher, especially BERT-based models that capture context across the full sentence. But they want more data and more compute than I had, so I left them as an optional extension rather than the main implementation.
>
> One thing I kept running into across the papers: preprocessing quality matters more than the algorithm choice. I ran a quick test early on, raw text versus cleaned text, and the difference in F1 was about 8 points. That settled the question. A model trained on messy input doesn't recover, regardless of which architecture goes on top.

**What changed:**
- "A few things stand out" deleted entirely
- Forced triad broken into separate discussions
- First person added throughout: "I went with", "I left", "I ran", "I kept running into"
- Specific number added: "8 points"
- Fragment added: "Fast and easy to explain."
- Single-sentence paragraph: "Machine learning replaced them for most practical tasks."
- "because" used naturally twice
- Personal commentary: "That settled the question."
- Informal aside: "without hand-waving"
- No dashes anywhere

---

## WHY AI TEXT GETS CAUGHT

These compound. All appear in texts scoring 80%+.

**Uniform perplexity.** Every word is the most statistically expected choice. No surprises anywhere in the text.

**Low burstiness (CV < 0.30).** Every sentence is roughly the same predictability level. Human text alternates between plain sentences and surprising ones.

**Forced triads.** Three-item lists where the third item adds only cadence. Detectors trained to flag this specifically (GPTZero 4.9b AI Patterns feature).

**Contrastive dilemmas.** Symmetric negative parallelism: "not just X but Y", "while A presents challenges, B unlocks opportunities." Break the symmetry.

**Participial tails.** Trailing `-ing` clauses that restate without adding. Strongest single syntactic signal in Reinhart et al. (PNAS 2025): 224-527% of human rate.

**Neutral summary tone.** Every sentence is a fact delivery with no writer behind it. AI underuses epistemic stance at 50-63% of the human rate.

**Template transitions.** `Furthermore` / `Moreover` / `Additionally` / `Notably`. Model favorites. Cut.

**Significance inflation.** `plays a crucial role` / `underscores the importance` / `is a testament to`. Replace with the specific thing that earns it.

**No contractions in non-academic text.** In any conversational genre, zero contractions is a flag.

**High mean word length.** Human prose averages 4.4 characters per word. AI prose averages 5.0-5.1. Latinate suffix bloat pushes this up.

**"Because" suppressed.** AI uses "because" at 19-20% of the human rate. Where it is missing, the text reads as model-generated.

**Formal closer.** `In conclusion,` / `Overall,` / `This demonstrates.` End on the last real detail.

---

## ANTI-PATTERNS

Never produce these regardless of length or topic:

- Opening on a definition: "X is a..."
- Opening on a superlative: "One of the most..."
- Opening on a category framing: "X is a method that..."
- "sits at the intersection of"
- "A few things stand out"
- "It is worth noting"
- "This demonstrates the importance of"
- "not just X, but Y" structure
- All sentences 15-22 words throughout
- Ending on "This shows that..." / "In conclusion..." / "Overall..."
- Triad used only for cadence
- Paragraph closing with a verdict on what the paragraph just said
- Any sentence that could appear unchanged in a Wikipedia article on a different topic

---

## DETERMINISTIC VALIDATION

The bundled `tools/gate.py` runs deterministic checks on any text file. Call it after Pass 3:

```bash
python3 tools/gate.py draft.txt --genre linkedin
python3 tools/gate.py draft.txt --genre academic --json
```

Valid genres: `linkedin`, `personal`, `email`, `social`, `fiction`, `readme`, `technical`, `academic`.

Hard errors (block delivery): empty text, em/en dashes, curly quotes.
Advisory findings (never block): vocabulary, openings, rhythm, participial openers, contractions. Reviewed in genre context, not acted on automatically.

---

## OUTPUT FORMAT

Print the check result line, then the rewritten text. Nothing else unless analysis is explicitly requested.

Check line examples:
- `checks: all 17 ok`
- `checks: [3] fail (no short sentences) [10] fail (no first person for student genre) -> rewriting`

Analysis only when asked: "--mode diagnose" / "explain what changed" / "why did you change that"

Always find something to improve. Never return input unchanged.

---

## LIMITS

- No typos, broken grammar, or forced slang.
- No invented facts, results, citations, or personal experiences.
- Code blocks: leave unchanged. They do not affect detection scores (paratext masking).
- No essay rules applied to formal technical documentation.
- No making writing worse in the name of making it human.

---

## RESEARCH BASIS

Perplexity and burstiness as detection signals: Edward Tian, Princeton thesis 2023. GPTZero arXiv:2602.13042 (Feb 2026). Morphosyntactic profiling: Reinhart et al. PNAS 2025 (participial rates, nominalization, "because" at 19-20% of human rate, contractions at 60-63%, hedges at 50-63%). Vocabulary patterns: Kobak et al. Science Advances 2025. Epistemic stance deficit: Jiang & Hyland, Applied Linguistics 2025. GPTZero AI Patterns (forced triads, contrastive dilemmas, elevated symbolism, participial tails): GPTZero Model 4.9b release notes, August 2026. ZeroGPT DeepAnalyse multi-stage pipeline: ZeroGPT technical documentation. ESL writer misclassification bias: Stanford AI Detection Study 2024. Ablation data (100% to 0% in five steps): Not Ai reference/why-word-swapping-fails.md. See reference/ folder for full bibliography and vocabulary tables.
