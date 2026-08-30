# Style Research: Structural Differences by LLM and Genre

Detailed breakdown of measured stylistic differences between LLM-generated and human-generated text, organized by feature type. All measurements from peer-reviewed research.

---

## Feature Category 1: Present Participial Clauses

**Source**: Reinhart et al. (PNAS 2025), Biber Feature analysis

**Measurement method**: Biber's morphosyntactic tagset, `pseudobibeR` R package, applied to HAP-E and COCA AI Parallel corpora.

**Human baseline**: ~5–8% of sentences in human-authored text open with a present participial clause.

**LLM rates** (instruction-tuned):
- GPT-4o: ~15–25% of sentences (2–5× human)
- Llama 3 70B Instruct: ~15–20% of sentences
- Llama 3 8B Instruct: ~12–18% of sentences
- GPT-4o Mini: ~14–22% of sentences

**Base model rates** (not instruction-tuned):
- Llama 3 70B Base: ~6–9% (close to human)
- Llama 3 8B Base: ~5–8% (close to human)

**Genre variation**: The elevated rate persists across all genres — fiction, blogs, news, academic — for instruction-tuned models. Base models adapt to genre more naturally.

**Example from GPT-4o**: "Bryan, leaning on his agility, dances around the ring, evading Show's heavy blows." (Note: two present participles in one sentence)

---

## Feature Category 2: Nominalizations

**Source**: Reinhart et al. (PNAS 2025), Jiang & Hyland (2025), Goulart et al. (2024)

**What counts**: Nouns formed from verbs or adjectives via suffixes: -tion, -tions, -ment, -ments, -ness, -ity, -ance, -ence

**Human baseline**: ~25–40 nominalizations per 1,000 words (varies by genre; academic writing is at the high end)

**LLM rates**:
- GPT-4o: ~45–70 per 1,000 words (1.5–2× human baseline)
- Llama 3 Instruct: ~40–60 per 1,000 words
- Base models: closer to human baseline

**Example from Llama 3 70B Instruct**: "These schemes can help to reduce deforestation, habitat destruction, and pollution, while also promoting sustainable consumption patterns." (4 nominalizations: deforestation, destruction, pollution, consumption)

**Why it matters**: Nominalization makes text feel denser and more abstract. "The implementation of the solution" is weaker than "implementing the solution." LLMs default to nominalized forms because they appear more formal and are common in training data.

---

## Feature Category 3: Vocabulary Frequency Divergence

**Source**: Reinhart et al. (PNAS 2025), Siler (PNAS 2026), Leppänen et al. (2025)

### GPT-4o overused words (100× human rate or higher)
From Reinhart et al. Table 4:
- camaraderie, palpable, tapestry, intricate, vibrant, solace, cacophony, amidst

**Context**: These words appear across all genres — even when GPT-4o is writing about sports, it reaches for "camaraderie was palpable."

### Instruction-tuned model overuse (10–100× human rate)
From Siler (2026), Leppänen et al. (2025), and community corpus studies:
- delve, leverage (as generic intensifier), utilize, facilitate
- underscore, meticulous, nuanced, foster
- comprehensive, robust, seamless
- pivotal, crucial, vital, paramount
- transformative, revolutionary, groundbreaking
- multifaceted, myriad

### Words underused by instruction-tuned LLMs
- Obscenities and profanity (100× below human rate — RLHF effect)
- Colloquial contractions in formal text
- Domain-specific technical terms when the model lacks deep domain knowledge
- Hedges that express genuine uncertainty (replaced by formulaic hedge phrases)

**Etymology note**: Ming et al. (2026) found that instruction tuning shifts vocabulary toward Romance-origin words ("utilize" from Latin via French, "facilitate" from Latin, "leverage" from Anglo-French) because these words appear in high-prestige academic writing that RLHF raters reward.

---

## Feature Category 4: Rhetorical Engagement Markers

**Source**: Jiang & Hyland (2025)

**Measurement**: Comparison of GPT-4 output to student essays on the same prompts, using metadiscourse taxonomy.

**Human student baseline**: Higher rates of all engagement markers in argumentative writing.

**GPT-4 measured deficits** (relative to students):
- Questions in prose: significantly fewer
- Direct reader address ("you", "consider..."): significantly fewer
- Personal asides ("I should note...", "for what it's worth"): significantly fewer
- Anticipating objections ("one might argue"): different pattern — LLMs use formulaic objection statements but less genuine engagement

**The distinction**: Human engagement markers are responsive to the reader's possible perspective. LLM engagement markers tend to be formulaic hedges or rhetorical questions with obvious answers.

---

## Feature Category 5: Epistemic Stance

**Source**: Jiang & Hyland (2025), Goulart et al. (2024)

**Hedging** (true uncertainty markers): LLMs use hedging but in formulaic positions — "It is worth noting that" before a certain claim; "It is important to mention" at arbitrary points. Human hedging is calibrated: more hedging when genuinely uncertain, less when confident.

**Boosters**: LLMs overuse certainty markers ("clearly", "obviously", "certainly") even when the claim requires qualification.

**Attitude markers**: LLMs use attitude markers ("importantly", "crucially", "remarkably") at high frequency, but the attitude is often disproportionate to the content.

---

## Feature Category 6: Passive Voice

**Source**: Reinhart et al. (PNAS 2025)

**Counter-intuitive finding**: GPT-4o uses agentless passive voice at roughly **half the human rate**. This is the opposite of the popular belief that AI overuses passive voice.

**Why**: RLHF training data likely penalizes passive voice (following common writing advice to "use active voice"). This over-correction makes GPT-4o less varied in voice construction than human writers.

**Llama base models**: Close to human passive voice rates.

**Implication for Not Ai**: Don't convert passive to active as a blanket rule. This is itself an AI-humanizer cliché that may make the text less human, not more.

---

## Feature Category 7: Narrative Fingerprints (Fiction)

**Source**: StoryScope (2026), Russell et al.

**AI fiction structural features**:
- Claude: flat event escalation (every scene has similar emotional weight)
- GPT: over-indexes on dream sequences
- Gemini: defaults to external character description
- All: over-explain themes ("This illustrates the theme of loss")
- All: favor single-track plots over morally ambiguous ones
- All: cluster in shared narrative space; human fiction is diverse

**Measured features**:
- Plot structure (arc shape, escalation rate)
- Thematic explicitness (is the theme stated or shown?)
- Character perspective (external description vs. internal experience)
- Temporal complexity (flashbacks, non-linear)
- Moral ambiguity (protagonist choices framed as right/wrong vs. complex)

---

## Feature Category 8: Information Density

**Source**: Reinhart et al. (2025), Goulart et al. (2024), Milička et al. (2025)

**Biber Dimension 1**: The "Involved vs. Informational" dimension is the strongest axis distinguishing register in English. Academic writing is highly informational (high dimension 1). Conversation is highly involved (low dimension 1).

**Finding**: All instruction-tuned LLMs shift toward the informational end of Dimension 1 **regardless of genre**. Even when writing fiction, blogs, or conversation, they default to information-dense academic-adjacent prose.

**Human behavior**: Humans adapt their information density to genre. A blog post is markedly less dense than an academic paper. A text message is markedly less dense than a report.

**LLM failure**: Fiction written by GPT-4o has similar information density to GPT-4o academic writing. This is why LLM fiction often feels flat — it reads like a dense description rather than a story.

---

## Cross-Genre Summary

| Feature | Human behavior | LLM behavior |
|---------|---------------|-------------|
| Participial clause rate | ~5–8% of sentences, genre-adapted | ~15–25% across all genres |
| Nominalization | ~25–40/1000 words, genre-adapted | ~45–70/1000 words across all genres |
| Information density | Adapts to genre | Stays high regardless of genre |
| Rhetorical engagement | Varies by register and purpose | Systematically low in essays |
| Epistemic stance | Calibrated to claim certainty | Formulaic; hedges and boosters misapplied |
| Vocabulary | Broad, context-sensitive | Narrow cluster of "prestige" vocabulary |
| Passive voice | Varies naturally | Below human rate (GPT-4o) |
| Stylistic range | Wide distribution | Narrow cluster |

---

## Important Caveat: These Numbers Will Change

The measurements cited here reflect 2024–2025 model versions (GPT-4o, Llama 3). As models are updated, fine-tuned on more diverse data, or trained with different RLHF procedures, the specific numbers will shift.

Dawkins et al. (2025) showed that fine-tuning on a genre-specific corpus (tweets) dramatically reduces the structural fingerprint for that genre. This means future models fine-tuned on diverse human writing styles may show smaller structural differences.

Not Ai's rules and scripts should be updated as new research emerges. The diagnostic scripts use configurable thresholds for this reason.
