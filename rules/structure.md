# Rules: Structure

These rules address the structural patterns that research identifies as the primary morphosyntactic fingerprints distinguishing LLM-generated text from human writing. Source: Reinhart et al. (2025), Biber tagset analysis of GPT-4o and Llama 3.

---

## 1. Present Participial Clause Overuse

**What it is**: Sentences that open or are modified with present participial clauses — "Building on this", "Leveraging the power of", "Drawing from extensive research", "Combining these elements".

**How AI differs**: Instruction-tuned LLMs use present participial clauses at **2–5× the human rate** across all registers including fiction, blogs, and news.

**Healthy human variation**: Participial clauses exist in human writing but are used purposefully for simultaneity, causation, or narrative compression — not as default sentence-openers.

**How to detect**: Count sentences opening with -ing verb phrases. If more than 1 in 5 sentences does this, the rate is elevated.

**How to improve**:
- Convert to a subject-verb structure: "Building on this" → "This builds on" or start fresh with the actual subject
- Convert to a causal clause: "Leveraging the platform's scale" → "Because the platform operates at scale,"
- Cut if the participial clause is merely decorative

**When NOT to modify**: Participial clauses are natural in narrative flow and vivid description. "Walking into the room, she noticed the empty chair" is fine. The problem is their use as generic connective tissue in informational prose.

---

## 2. Nominalization Density

**What it is**: Nominalizations are nouns formed by adding suffixes to verbs or adjectives: *justification* (justify), *development* (develop), *robustness* (robust), *implementation* (implement), *optimization* (optimize), *enhancement* (enhance), *facilitation* (facilitate).

**How AI differs**: Instruction-tuned LLMs use nominalizations at **1.5–2× the human rate**, contributing to what researchers call "informationally dense, noun-heavy prose" — text that feels formal and abstract even when discussing concrete things.

**Healthy human variation**: Technical and academic writing legitimately uses nominalizations. The problem is using them where a simpler verb form would be clearer and more direct.

**How to detect**: Flag strings of nouns where a verb existed: "the implementation of the solution" vs. "implementing the solution"; "the achievement of the goal" vs. "achieving the goal".

**How to improve**:
- Restore the verb: "the *optimization* of the system" → "optimizing the system" or "to optimize the system"
- Use the active form: "the *development* of new approaches" → "developing new approaches"
- Cut the nominalized phrase entirely if the concept is already clear

**When NOT to modify**:
- When the nominalization IS the subject being discussed ("The *implementation* was flawed" — here we're discussing the implementation itself)
- In genuinely technical contexts where the noun form carries precise meaning
- When the text is academic writing targeting an academic audience

---

## 3. 'That'-Clause as Sentence Subject

**What it is**: Sentences where a 'that'-clause serves as the grammatical subject: "That the system works effectively demonstrates...", "That these patterns persist shows...", "That progress has been made is evident..."

**How AI differs**: LLMs use this construction at significantly elevated rates. It produces a formal, legalistic quality that rarely appears in natural conversation or informal writing.

**How to improve**:
- Invert: "That X is true" → "X is true" or "It is clear that X"
- Reframe: "That the approach succeeds demonstrates..." → "The approach succeeds, which demonstrates..."
- Use a noun phrase subject instead: "That results improved surprised researchers" → "The improved results surprised researchers"

---

## 4. Agentless Passive Voice

**What it is**: Passive voice without naming the agent: "Results were obtained", "It was determined that", "The analysis was conducted", "Improvements were made".

**How AI differs**: GPT-4o uses agentless passive at roughly **half the human rate** (surprisingly low — it overcompensates toward active voice), while some other LLMs overuse it. The issue is not passive voice itself but its deployment without purpose.

**Healthy human variation**: Passive voice is genuinely useful when: the agent is unknown, the agent is unimportant, the action matters more than who performed it, or stylistic variety is desirable. Academic and technical writing legitimately uses passive voice.

**How to detect**: Look for passive constructions where the agent is clear from context and the active form would be more direct.

**How to improve** (only when passive is unclear or evasive):
- Restore the agent: "The analysis was conducted" → "We conducted the analysis" or "The team conducted..."
- Only when the agent is known and relevant

**When NOT to modify**: Do not convert all passive to active. That is itself an AI-humanizer cliché. Use judgment.

---

## 5. Information Density Overload

**What it is**: Packing too many concepts into each sentence, producing prose that is dense but reads as mechanical rather than thoughtful.

**Research basis**: LLMs tend toward "informationally dense" prose across all registers — even when writing fiction or blog posts, they default to an academic-adjacent information density.

**Signs**:
- Multiple nominalized phrases in one sentence
- Stacked prepositional phrases
- Compound subjects + compound predicates + embedded clauses
- Sentences that convey 4+ concepts at once

**How to improve**:
- Split into two or three sentences
- Move background information to a separate sentence earlier
- Cut information that was already established

**When NOT to modify**: Technical documentation, legal writing, and academic abstracts are legitimately dense. Density is only a problem when it exceeds audience expectations.

---

## 6. Symmetrical Paragraph Structure

**What it is**: Every paragraph follows the same shape: topic sentence → three supporting sentences of similar length → closing sentence. When every paragraph uses this structure, the writing feels formulaic.

**How AI differs**: LLMs are trained on well-structured text and tend to produce the academic "paragraph model" regardless of genre or intent.

**Healthy human variation**: Human paragraphs vary in length, shape, and density. A paragraph might be a single sentence. A paragraph might open with an example rather than a claim. A paragraph might have no topic sentence at all.

**How to improve**:
- Vary paragraph length deliberately
- Allow some paragraphs to open with evidence rather than claim
- Allow some paragraphs to have no explicit topic sentence when the flow is clear
- Allow a very short paragraph (1–2 sentences) after a long one for rhythm

**When NOT to modify**: Instructional content and certain formal genres benefit from consistent paragraph structure. Do not introduce arbitrary variation.

---

## 7. Structural Parallelism Overdrive

**What it is**: Every list item follows the exact same grammatical form. Every bullet point is the same length. Every section header follows the same template. Every example is introduced with the same phrase.

**Healthy use**: Parallelism improves readability in lists and comparisons. The problem is when it extends uniformly across an entire document, removing natural variation.

**How to improve**:
- Allow one or two list items to be longer or shorter than the others
- Vary the sentence structure of section-opening sentences
- Allow different types of evidence (statistic, example, quote, analogy) rather than repeating one type

---

## Summary: Structural Priority Order

When choosing which structural issues to address, prioritize:
1. Present participial clause overuse (strongest signal, easiest to fix)
2. Nominalization density (second strongest signal)
3. Information density overload (affects readability most)
4. Symmetrical paragraph structure (affects naturalness most)
5. 'That'-clause subjects (context-dependent)
6. Structural parallelism (only when extreme)
7. Passive voice (only when genuinely evasive or unclear)
