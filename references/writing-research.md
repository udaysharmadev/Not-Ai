# Academic Writing Research Reference

Compiled research on structural, rhetorical, and stylistic differences between human and LLM-generated text. This is Not Ai's primary evidence base.

**Last updated**: August 2026

---

## Primary Studies

### Reinhart et al. (2025) — PNAS
**Citation**: Reinhart, A., Markey, B., Laudenbach, M., Pantusen, K., Yurko, R., Weinberg, G., & Brown, D. W. (2025). Do LLMs write like humans? Variation in grammatical and rhetorical styles. *Proceedings of the National Academy of Sciences*, 122(8), e2422455122. doi:10.1073/pnas.2422455122

**Preprint**: https://arxiv.org/html/2410.16107v1

**Method**: Constructed two parallel corpora (COCA AI Parallel, HAP-E) from 12,000 human texts + LLM continuations from GPT-4o, GPT-4o Mini, Llama 3 8B, Llama 3 70B, and instruction-tuned variants. Analyzed using Biber's 66-feature morphosyntactic tagset. Random forest classifier achieved 66% accuracy (vs. 14% random baseline) on 7-way classification.

**Key findings**:
1. Instruction-tuned LLMs use **present participial clauses at 2–5× the human rate**
2. **Nominalization rates at 1.5–2× human** across all registers
3. LLMs produce informationally dense, noun-heavy prose regardless of genre
4. GPT-4o uses "camaraderie", "palpable", "tapestry", "intricate" at **100× the human rate**
5. **Instruction tuning (RLHF) is the root cause** — Llama 3 base models match human rates; instruction-tuned variants diverge dramatically
6. Human writing has broader stylistic variation; all LLMs cluster in a narrower stylistic region
7. Model size does not reduce the fingerprint — Llama 70B and 8B show similar patterns
8. Generalization across corpora is difficult — classifiers trained on one LLM don't fully transfer to others

**Relevance to Not Ai**: This study provides the evidence base for Not Ai's structural intervention approach. The key insight: the primary fingerprint is morphosyntactic (clause types, information density), not lexical (word choice). Existing humanizers work at the lexical level; Not Ai works at the structural level.

**Data available**: https://huggingface.co/datasets/browndw/human-ai-parallel-corpus

---

### Jiang & Hyland (2025) — Multiple papers
**Citations**:
- Jiang, F., & Hyland, K. (2025). Rhetorical distinctions: Comparing metadiscourse in essays by ChatGPT and students. *English for Specific Purposes*, 79, 17–29.
- Jiang, F., & Hyland, K. (2025). Does ChatGPT write like a student? Engagement markers in argumentative essays. *Written Communication*.
- Jiang, F., & Hyland, K. (2025). Does ChatGPT argue like students? Bundles in argumentative essays. *Applied Linguistics*, 46(3), 375–391.

**Key findings**:
1. ChatGPT essays show "significantly lower frequency of interactional metadiscourse, such as hedges, boosters, and attitude markers" → more impersonal, expository tone
2. Student essays show higher "rhetorical engagement" including questions and personal asides
3. "ChatGPT-generated essays exhibited fewer engagement markers, particularly questions and personal asides"
4. LLM "bundles are more rigid and formulaic" — noun and preposition-based rather than epistemic stance markers
5. Student essays have "more epistemic stances and authorial presence"

**Relevance to Not Ai**: Validates the rhetorical dimension in `rules/rhetoric.md`. The engagement marker deficit is real and measurable. Not Ai addresses: hedging calibration, engagement marker addition (where genre permits), and epistemic stance restoration.

---

### StoryScope (2026)
**Citation**: Russell, J., Rajendhran, R., Iyyer, M., & Wieting, J. (2026). StoryScope: Investigating idiosyncrasies in AI fiction. arXiv. https://arxiv.org/abs/2604.03136

**Key findings**:
1. AI stories cluster in a **shared region of narrative space** while human-authored stories exhibit **greater diversity**
2. AI-specific narrative fingerprints:
   - **Claude**: notably flat event escalation
   - **GPT**: over-indexes on dream sequences
   - **Gemini**: defaults to external character description
3. AI stories over-explain themes; human stories have more moral ambiguity
4. Human stories have increased temporal complexity; AI stories favor "tidy, single-track plots"
5. Narrative construction differences, not just writing style, distinguish human from AI fiction

**Relevance to Not Ai**: The "shared narrative space" finding is the narrative equivalent of the "humanizer paradox" — all LLMs cluster. This means humanizers that aim for a single "human-like" narrative target create a new cluster. Not Ai's design principle of targeting a **distribution** rather than a point is supported by this research. Also informs `rules/rhetoric.md` narrative section.

---

### Milička et al. (2025)
**Citation**: Milička, J., Marklová, A., & Cvrček, V. (2025). Benchmark of stylistic variation in LLM-generated texts. arXiv. https://arxiv.org/abs/2509.10179

**Key findings**:
1. Compared lots of different LLMs (GPT versions, Gemini, Claude) to humans using Biber's six factor dimensions
2. LLMs shift toward Dimension 1 (Involved → Informational): more information-dense text
3. Shift varies by model — models have distinct stylistic fingerprints
4. Czech corpus analysis: LLMs much worse at matching native Czech style

**Relevance to Not Ai**: Confirms model-specific fingerprints. Supports the architecture that handles different source models differently. Also confirms cross-language limitations — Not Ai should acknowledge these.

---

### Goulart et al. (2024)
**Citation**: Goulart, L., et al. (2024). AI or student writing? Analyzing the situational and linguistic characteristics of undergraduate student writing and AI-generated assignments. *Journal of Second Language Writing*, 66, 101160.

**Key findings**:
1. "AI-generated texts are more informationally dense, explicit, and less involved than student-authored texts"
2. "EFL Students tend to integrate more personal references and features of involvement, making their writing more nuanced and contextually rich"
3. Uses Biber's MDA (Multi-Dimensional Analysis) — confirms Biber features are diagnostically effective

**Relevance to Not Ai**: Confirms the information density finding in student/essay contexts. "Personal references and involvement" is exactly what Not Ai's engagement and voice dimensions address.

---

### Siler (2026) — Academic slop in published papers
**Citation**: Siler, K. (2026). The diffusion of large language models in published academic articles. *PNAS*, 123(22), e2605754123.

**Key findings**:
1. Corpus of 7.3 million full-text articles (Elsevier, Frontiers, MDPI, PLoS) from 2020–2025
2. "LLM-likely words" spiking after 2023: "underscore", "delve", "meticulous", "foster", "comprehensive"
3. Higher rates in lower-ranked institutions and non-English-first-language countries
4. Higher in MDPI and Frontiers than Elsevier and PLoS

**Relevance to Not Ai**: Real-world evidence that AI vocabulary signals are measurable at scale in published academic papers. Validates the vocabulary signal list in `scripts/analyze_structure.py`.

---

### Dawkins et al. (2025) — Fine-tuning reduces differences
**Citation**: Dawkins, H., Fraser, K. C., & Kiritchenko, S. (2025). When detection fails: The power of fine-tuned models to generate human-like social media text. arXiv. https://arxiv.org/abs/2506.09975

**Key findings**:
1. Biber features show systematic differences in LLM-written tweets vs. human tweets
2. **Fine-tuning on genre-specific corpus dramatically reduces these differences**
3. Suggests instruction-tuned LLMs can be adapted to a genre

**Relevance to Not Ai**: Important limitation — the structural signals identified by Reinhart et al. may weaken as models are specifically fine-tuned on genre-appropriate data. Not Ai must be updated as the research landscape evolves.

---

### Toney et al. (2026) — Review of "humanness" studies
**Citation**: Toney, A., Bode, L., Ventura, T., Wilcox, E., & Singh, L. (2026). Comparing the humanness of machine-generated and human-authored text. *ACM Computing Surveys*. doi:10.1145/3806206

**Key findings**:
1. Review of 17 papers analyzing "humanness" up to 2024
2. Most studies did not explore prompt variation
3. Not enough studies compared multiple LLMs
4. "Humanness" may depend on the observer, change over time, and vary across linguistic groups

**Relevance to Not Ai**: Validates the "human writing as a distribution" design principle. Humanness is not a fixed target.

---

### Ming et al. (2026) — Romance vocabulary bias
**Citation**: Ming, X., Hernandez, J., & Juzek, T. S. (2026). Identifying LLM lexical bias: A curation-free triangulated metric for preference-state learning. *FLAIRS-39*.

**Key findings**:
1. Instruction tuning introduces a shift toward Romance-origin vocabulary
2. Romance words entered English "via the ruling class and acquired high socio-economic status"
3. RLHF may reward formal/prestigious vocabulary

**Relevance to Not Ai**: Explains *why* LLMs reach for "utilize" over "use", "facilitate" over "help", "leverage" over "use" — it's a learned prestige signal, not a semantic choice. The intervention is to restore the more direct Anglo-Saxon form when it serves communication better.

---

### LLM Review (2026) — Blind peer review for creative writing
**Citation**: arXiv:2601.08003 — LLM Review: Enhancing Creative Writing via Blind Peer Review Feedback

**Key finding**: Multi-agent frameworks that interact during generation can cause "content homogenization" — reducing creative diversity. Blind review (agents exchange feedback without seeing each other's drafts) preserves divergent trajectories.

**Relevance to Not Ai**: The homogenization problem is the AI-writing problem in miniature. This supports Not Ai's principle: target a diverse distribution of human styles, not a single "human-like" style.

---

### SurrogatePrompt (2023) — Representation mismatch
**Citation**: SurrogatePrompt: Bypassing the Safety Filter of Text-To-Image Models via Substitution. arXiv:2309.14122

**Key architectural insight (adapted)**:
The paper shows that safety filters and image generators operate in different "representation spaces" — a prompt can evade the filter by using surface-level substitutions that the filter doesn't associate with the problematic concept, while the image generator still produces the intended output.

**Relevance to Not Ai (carefully adapted)**:
This is analogous to the humanizer problem. Humanizers that operate at the word level (the "safety filter level") change surface features that detectors react to, while the underlying morphosyntactic representation (the "image generator level") — what makes the text actually feel like LLM output — remains unchanged.

**Not Ai's response**: Operate at the structural level, not the surface level. Change clause types, information density, and rhetorical patterns — the actual representation that constitutes "LLM writing style" — rather than swapping surface vocabulary.

**IMPORTANT CAVEAT**: The SurrogatePrompt paper is about adversarial attacks on safety systems. Not Ai does NOT draw on it for adversarial purposes. The architectural lesson — that surface and structural representations are different spaces — applies generally to the problem of meaningful transformation vs. surface disguise.

---

## Commercial Humanizer Analysis

### Research Methodology
- Studied marketing claims vs. actual output behaviors
- Investigated user reports, reviews, and independent tests
- Did not rely on marketing copy

### Summary of Findings

| Tool | Approach | Primary Weakness |
|------|----------|------------------|
| Undetectable AI | Word substitution + paraphrasing | Creates "humanizer voice"; doesn't address structure |
| WriteHuman | Synonym replacement + punctuation variation | Loses meaning; no genre awareness |
| QuillBot | Paraphrase modes | Meaning drift; voice destruction |
| Phrasly | Synonym swap + sentence restructuring | Over-casualization; structural patterns remain |
| StealthGPT | Substitution-focused | Surface-level only |
| HIX Bypass | Multi-pass paraphrase | Produces recognizable "bypass voice" |

**Common pattern across all commercial tools**:
1. Word-level intervention (synonyms, banned word removal)
2. No structural analysis
3. No voice preservation
4. No genre awareness
5. No meaning preservation checking
6. Outputs converge toward a "humanizer voice" (short-medium-long sentence cycling, forced contractions, injected fragments)

---

## Open-Source Humanizer Analysis

### Aboudjem/humanizer-skill
- 55 patterns (Wikipedia AI tells extended)
- 5 fixed voice modes
- 0-100 AI-tell score
- Pure Markdown, zero dependencies
- Weakness: all 5 voices are fixed templates, not user voice extraction; patterns are still primarily lexical

### blader/humanizer
- Focus on removing Wikipedia AI tells
- Voice matching via sample
- Good documentation
- Weakness: primarily lexical intervention; no structural diagnosis

### numen-tech/slopornot / agentic-humanizer
- Multi-pass workflow
- Multi-language support
- Weakness: convergence toward "humanizer output" pattern

### Common pattern across open-source tools
All implement some variant of: scan → flag → replace/rewrite → output. None implement:
- Biber-feature structural diagnosis
- Information density measurement
- Clause-type distribution analysis
- Genre-conditioned transformation
- Adversarial self-review
- Meaning preservation verification

---

## Limitations of Current Research

1. **Temporal decay**: LLM fingerprints change as models are updated. Research from 2024 may not apply to 2026 models.
2. **Fine-tuning escape**: Dawkins et al. show genre-specific fine-tuning can dramatically reduce structural fingerprints.
3. **Humanness is subjective**: Toney et al. note that "humanness" depends on the observer and may change over time.
4. **Cross-language gap**: Non-English research is limited. LLM behavior in other languages may differ significantly.
5. **Prompt sensitivity**: Style varies significantly with prompt — a highly constrained prompt may produce more human-like output.

---

## Future Research Directions

1. **Genre-specific fingerprint studies**: Most research focuses on academic and argumentative writing. Fiction, social media, and technical documentation need more study.
2. **Human diversity baseline**: Current research often uses a single "human" baseline. A broader human diversity model is needed.
3. **Post-humanization evaluation**: What happens to the structural fingerprint after humanization? Do commercial tools reduce it or just shift it?
4. **Voice preservation measurement**: No validated metric exists for voice preservation across transformations.
5. **Cross-agent evaluation**: How does humanizer output quality vary when applied through different agent systems?
