# Wikipedia: Signs of AI Writing — Annotated Reference

**Source**: https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing
**Retrieved**: August 2026
**Purpose**: Reference guide for Not Ai. Each sign is annotated with: what it is, why it appears, what the underlying problem actually is, and the correct intervention.

> **Critical principle from the source itself**: *A sign is not the underlying problem. Simply treating surface indicators as the problem can merely obscure the underlying issue.*

Not Ai follows this principle. This document records each sign, but also explains why a naive "remove it" response often fails.

---

## Category 1: Inflated Significance

**Signs**: Sentences claiming the topic is uniquely important, a "paradigm shift", "groundbreaking", "transformative", "revolutionary", "unprecedented".

**Why AI produces it**: Models are trained on writing that often frames topics positively to maintain engagement. RLHF reinforces text that sounds confident and impressive.

**Underlying problem**: Absent or underspecified evidence. The claim exceeds what the surrounding text actually demonstrates.

**Correct intervention**: Don't just remove "groundbreaking" — ask whether the text actually supports the significance claim. If not, soften or remove the claim. If yes, the word may be appropriate.

**When NOT to intervene**: Genuine breakthrough announcements, editorial commentary, opinion pieces where the author is entitled to their judgment.

---

## Category 2: Generic Claims

**Signs**: "Many experts agree", "research has shown", "studies indicate", "it is widely acknowledged", "industries are increasingly", "the world is changing".

**Why AI produces it**: Generalizations work across many contexts and require no specific knowledge. They are statistically safe.

**Underlying problem**: Missing specificity. The author knows something; the LLM does not. The generic form covers this gap.

**Correct intervention**: If the source contains specific information, use it. If not, use an honest hedge ("some researchers suggest") or remove the claim. Never invent specifics.

**When NOT to intervene**: Genuine high-level framing in introductions, where specifics follow in the same document.

---

## Category 3: Repetitive Structure

**Signs**: Every paragraph following the same shape. Every section beginning with a topic sentence followed by three supporting sentences and a concluding sentence.

**Why AI produces it**: Academic paragraph structure is heavily represented in training data and reinforced by RLHF feedback rewarding "organized" text.

**Underlying problem**: The writing is structurally monotonous. Each individual paragraph may be fine; the pattern across all paragraphs is mechanical.

**Correct intervention**: Vary paragraph length and shape. Some paragraphs can be one sentence. Some can open with evidence. Some need no explicit topic sentence.

---

## Category 4: Formulaic Transitions

**Signs**: "Furthermore", "Moreover", "Additionally", "In conclusion", "To summarize", "Last but not least", "Having said that", "With that being said", "It is worth noting that".

**Why AI produces it**: These transitions are common in formal writing and are strongly reinforced as markers of "well-organized" text.

**Underlying problem**: The transitions often indicate structure that doesn't need to be labeled — the logical relationship is already clear from content. Using them mechanically creates a hollow bureaucratic rhythm.

**Correct intervention**: Remove the transition word and see if the relationship between sentences is still clear. If yes, the transition was unnecessary. If not, keep a simpler version or rewrite the connection.

**IMPORTANT**: Do not ban transition words. They are appropriate when they signal a genuine logical move. The problem is their compulsive use at high frequency.

---

## Category 5: AI-Associated Vocabulary

**Signs**: "delve", "leverage", "utilize", "facilitate", "comprehensive", "robust", "seamless", "cutting-edge", "pivotal", "crucial", "vital", "foster", "underscore", "meticulous", "nuanced", "multifaceted", "myriad", "tapestry", "camaraderie", "palpable", "whirlwind", "intricate", "vibrant".

**Research basis**: Reinhart et al. (PNAS 2025) measured that GPT-4o and GPT-4o Mini use words like "camaraderie", "palpable", "tapestry", and "intricate" at more than **100× the human rate** across diverse genres. Siler (2026) found "delve", "underscore", "meticulous", and "foster" spiking sharply in academic publications post-2022.

**Why AI produces it**: These words appear in RLHF training data associated with positive human feedback — they sound "sophisticated". Instruction tuning appears to introduce a Romance-origin vocabulary bias (Ming et al., 2026).

**Underlying problem**: These words are surface signals of a deeper issue — the text is optimized for appearing high-quality rather than communicating effectively.

**Correct intervention**: Do NOT simply ban these words. Ask why the word is here. "Leverage" is fine in a literal context ("we can leverage the existing infrastructure"). It is a signal when used as a generic intensifier ("leveraging the power of collaboration"). Replace when the word is doing no semantic work.

**CRITICAL WARNING**: Creating a word blacklist is itself a shallow intervention. It removes the surface signal while leaving the underlying structural patterns intact. Not Ai must never reduce to a word blacklist.

---

## Category 6: Negative Parallelism

**Signs**: "Not X. Not Y. But Z." — used as a rhetorical device, especially in professional and motivational writing.

**Why AI produces it**: LLMs learned this pattern from persuasive human writing. It creates rhetorical energy that feels compelling.

**Underlying problem**: Its compulsive use in nearly every piece of professional AI writing makes it recognizable as a humanizer cliché.

**Correct intervention**: Keep when it serves a genuine rhetorical purpose for this specific author in this specific context. Remove when it was added for drama.

---

## Category 7: Excessive Tricolons

**Signs**: Every list has exactly three items. Every argument has three parts. Every conclusion has three takeaways.

**Why AI produces it**: Tricolons feel complete, balanced, and literary. They are overrepresented in training data's formal and persuasive writing.

**Underlying problem**: Ideas don't naturally come in threes. Forcing tricolons removes genuine complexity (four items, or two, or one).

**Correct intervention**: Count to the right number. If you have two genuine items, use two. If four, use four.

---

## Category 8: Formatting Overuse

**Signs**: Excessive use of bold text, bullet points, headers, sub-headers — in prose that doesn't need structure formatting.

**Why AI produces it**: RLHF feedback rewards "scannable", "organized" text. Formatting is interpreted as a quality signal.

**Underlying problem**: Formatting replaces argument. A paragraph that makes a point clearly doesn't need a bold header. A list can replace the thinking that would go into a connecting argument.

**Correct intervention**: Convert bullet points to prose when they describe a flowing argument. Remove headers from short passages that don't need navigation. Bold only what is genuinely critical.

**When NOT to intervene**: Technical documentation, README files, structured reports — these legitimately use formatting.

---

## Category 9: Unnatural Communication Patterns

**Signs**: Responding to a simple question with a lengthy preamble ("That's a great question. I'd be happy to help you explore..."), excessive caveats, over-explanation of obvious things, refusals framed as offers to help.

**Relevance to Not Ai**: These patterns appear in conversational AI outputs. When humanizing chat responses or emails, this category is directly applicable.

**Correct intervention**: Remove the preamble. Answer the question. Trust the reader.

---

## Category 10: Repetitive Summaries

**Signs**: Ending every section with a sentence that restates what was just said. Ending an essay with a paragraph that summarizes the preceding paragraphs. Using "In conclusion..." to introduce content that isn't a conclusion but merely a restatement.

**Underlying problem**: LLMs are strongly trained to summarize. This produces redundant closings that add length without adding value.

**Correct intervention**: Read the closing sentence of each section. If it restates what the section already said clearly, remove it or replace it with a forward-looking consequence or question.

---

## Category 11: Stylistic Regularity

**Signs**: Every sentence in the "correct" format. No run-ons, no fragments, no sentence that breaks convention. Perfect grammar throughout.

**Why it signals AI**: Human writing — even expert human writing — contains controlled imperfections: deliberate fragments for emphasis, run-ons that mirror thought, comma splices that feel right in context. Perfect consistency is itself a signal.

**Important nuance**: Not Ai does NOT introduce errors to "seem human". That is "over-humanization" and produces bad writing.

**Correct intervention**: Not to add errors, but to allow the text to have natural rhetorical shapes that happen to break strict grammatical convention when they serve the writing (deliberate fragment for emphasis, rhetorical question, direct address).

---

## Patterns Not Covered by Wikipedia's List (from research)

### Present Participial Clause Overuse
The most statistically significant structural signal found by Reinhart et al. — not covered by Wikipedia's list. LLMs open sentences with -ing clauses at 2–5× the human rate. See `rules/structure.md`.

### Nominalization Density
Second strongest structural signal. LLMs use noun forms of verbs and adjectives at 1.5–2× the human rate. See `rules/structure.md`.

### Information Density Mismatch
LLMs default to academically dense prose regardless of genre — producing information-dense blog posts and fiction, which reads as unnatural. See `rules/structure.md`.

### Rhetorical Engagement Deficit
LLMs produce significantly fewer questions, reader address moves, and personal asides than human writers in argumentative genres. See `rules/rhetoric.md`.

### Narrative Structure Flatness
AI fiction: flat event escalation, over-explained themes, single-track plots, external character description defaults. (StoryScope, 2026). See `rules/rhetoric.md`.

---

## What This Reference Is Not

This is not a checklist for automatic flagging. It is a guide for informed human-AI collaborative judgment.

Every item on this list requires context to interpret correctly. "delve" in a recipe blog is different from "delve" in an academic abstract. A tricolon in a speech is different from a tricolon in every paragraph of a sales email.

Not Ai's job is to interpret these signals intelligently, not to execute a checklist.
