# Evidence Registry — Not-AI 3.0

Every research-backed diagnostic must trace to an entry here. Each entry records
what the finding legitimately supports inside Not-AI, what it does NOT justify,
and which module uses it. Population differences never become universal rules
for individual texts.

Conventions: `effect` quotes the reported direction/magnitude; `supports` is the
only permitted product use; `does_not_justify` is normative. `confidence` reflects
our verification level (verified = primary source or DOI landing page checked
2026-10-04; secondary = credible summary, full text not re-verified).

## E01 — Reinhart et al. 2025, PNAS

- source: Reinhart, A., Markey, B., Laudenbach, M., Pantusen, K., Yurko, R.,
  Weinberg, G., & Brown, D. W. (2025). Do LLMs write like humans? Variation in
  grammatical and rhetorical styles. PNAS 122(8), e2422455122.
- doi: 10.1073/pnas.2422455122
- research_question: Do instruction-tuned LLMs match human grammatical/rhetorical
  style variation across genres when continuing the same prompt?
- corpus_size: parallel human + model continuations; ~500-word continuations per prompt
- language: English
- genres: multiple (incl. academic, speech-like, narrative); genre-conditioned comparison
- models: GPT-4o / GPT-4o Mini, Llama 3 variants (base vs instruction-tuned)
- features: 66 Biber lexical/grammatical/rhetorical features; present participial
  clauses, nominalizations, phrasal/clausal coordination, agentless passives,
  hedges, downtoners, word length, pronouns, tense, stance, genre interaction
- main_finding: Instruction-tuned models write in an informationally dense,
  noun-heavy style and adapt less to genre. Reported directions: present participial
  clauses ~2–5× human rate; nominalizations ~1.5–2.1×; phrasal coordination ~1.4–1.9×;
  agentless passives underused (~half human rate for GPT-4o); distinctive vocabulary
  (14 words at ~84–171× human rate); contractions/hedges below human rate.
- effect_size: as above (population rates in studied corpora; exact figures vary by
  model/genre; direction matters more than decimals)
- limitations: English only; 2024-era models; ~500-word continuations; per-1,000-token
  tagged rates not comparable to regex proxies; cross-model/cross-corpus generalisation harder
- supports: genre-relative review prompts for density, participial packaging,
  nominal actor-hiding, coordination stacking, stance gaps (NOT-AI modules:
  `gate.py`, `lexical.py`, `syntax.py`, `discourse.py`, `policy.py` genre caveats)
- does_not_justify: quotas, bans, authorship verdicts, detector optimisation,
  comparing regex-proxy counts to paper rates, universal "human CV > 0.4" targets
- module: not_ai_core.gate / lexical / syntax / policy
- confidence: verified (DOI + PNAS abstract + CMU summary checked 2026-10-04)

## E02 — Biber multidimensional analysis (1988; 1995; Conrad & Biber)

- source: Biber, D. (1988). Variation Across Speech and Writing. CUP; Biber (1995)
  Dimensions of Register Variation; Conrad & Biber (2001, 2009).
- research_question: Along which co-occurring feature dimensions do registers vary?
- corpus_size: multi-register corpora (LOB/London-Lund lineage; ~1M words core)
- language: English (cross-linguistic extensions exist; Not-AI uses English dimensions)
- genres: speech vs writing across registers (conversation, fiction, academic, official…)
- features: factor-analysed clusters: D1 involved vs informational; D2 narrative vs
  non-narrative; D3 explicit vs situation-dependent; D4 overt persuasion;
  D5 abstract vs non-abstract; D6 online elaboration
- main_finding: No single formal/informal axis; registers occupy positions in a
  multidimensional space; features work in clusters with functional underpinnings
  (purpose + production circumstances).
- limitations: English-calibrated; dimension scores need sufficient text; Not-AI has
  no factor-analysis implementation — uses dimensions interpretively
- supports: cluster-aware reading (density + pronouns + stance together), composable
  genre dimensions, refusing single-axis formality rules (modules: `policy.py`, `diagnose.py`)
- does_not_justify: scoring a document on one dimension; formal-vs-informal rewrite targets
- module: not_ai_core.policy
- confidence: verified (core dimensions widely documented; checked 2026-10-04)

## E03 — Jiang & Hyland 2025, Written Communication

- source: Jiang, F. K., & Hyland, K. (2025). Does ChatGPT write like a student?
  Engagement markers in argumentative essays. Written Communication 42(3), 463–492.
- doi: 10.1177/07410883251328311
- research_question: Can ChatGPT mimic student reader-engagement in argumentative essays?
- corpus_size: 145 ChatGPT + 145 student essays (British undergraduates / A-level lineage)
- language: English; genre: argumentative essays
- features: Hyland engagement model — reader pronouns, directives, questions,
  personal asides, appeals to shared knowledge; plus companion metadiscourse work
  (hedges, boosters, self-mentions, attitude/frame/transition markers)
- main_finding: Student essays richer in quantity and variety of engagement,
  especially questions and personal asides; ChatGPT fewer interactional markers,
  more shared-knowledge appeals and structural transitions.
- limitations: one task/genre/population; peer-reviewed but paywalled (abstract +
  repository record verified; full effect tables not re-verified here)
- supports: engagement review ONLY in argumentative/student genres; never insert
  questions/asides to hit targets (modules: `lexical.py` stance/engagement, `policy.py`)
- does_not_justify: universal "use X questions per 1k words"; forcing first person
  into technical/README prose
- module: not_ai_core.lexical / policy
- confidence: verified-abstract (DOI + abstract + UEA record 2026-10-04)

## E04 — Jiang & Hyland metadiscourse companion (2024–2025)

- source: Jiang & Hyland companion studies (Applied Linguistics bundles 2024;
  English for Specific Purposes metadiscourse 2025; stance-markers review 2026).
- research_question: How do stance/metadiscourse repertoires differ (ChatGPT vs students)?
- corpus_size: same essay lineage (hundreds of essays)
- features: hedges, boosters, self-mentions, attitude markers, frame markers,
  transitions; lexical bundles (noun/preposition-heavy in ChatGPT)
- main_finding: AI texts fewer stance expressions, narrower repertoire, more noun/
  preposition bundles for abstract description and structuring.
- limitations: same genre bounds; secondary synthesis here
- supports: stance-variety review in student/argumentative genres (module: `lexical.py`)
- does_not_justify: numerical hedge/booster quotas per document
- module: not_ai_core.lexical
- confidence: secondary

## E05 — Kobak et al. 2025, Science Advances

- source: Kobak, D., González-Márquez, R., Horvát, E.-A., & Lause, J. (2025).
  Delving into LLM-assisted writing in biomedical publications through excess
  vocabulary. Science Advances 11(27), eadt3813.
- doi: 10.1126/sciadv.adt3813
- research_question: How widespread is LLM-assisted writing in biomedical literature?
- corpus_size: >15M PubMed abstracts 2010–2024
- language: English; genre: biomedical abstracts
- features: excess-vocabulary analysis (style-word frequency shifts post-ChatGPT)
- main_finding: Abrupt post-LLM rise in style words (e.g. delves r≈28, underscores
  r≈13.8, showcasing r≈10.7 with inflections); lower-bound estimate ≥13.5% of 2024
  abstracts LLM-processed (up to ~40% in subcorpora).
- limitations: corpus-level inference; lower bound; biomedical abstracts only;
  cannot classify individual documents; marker list shifts with models
- supports: cluster-level vocabulary review (repeated style-word clusters worth
  reading), never single-word document verdicts or blacklists (module: `lexical.py`, gate tiers)
- does_not_justify: word bans, "AI vocabulary" labels as authorship proof
- module: not_ai_core.lexical / gate
- confidence: verified (PubMed + Science Advances pages 2026-10-04)

## E06 — McCarthy & Jarvis 2010, Behavior Research Methods

- source: McCarthy, P. M., & Jarvis, S. (2010). MTLD, vocd-D, and HD-D: a validation
  study. Behavior Research Methods 42(2), 381–392.
- doi: 10.3758/BRM.42.2.381
- research_question: Which lexical-diversity indices are valid and length-robust?
- corpus_size: validation study across varied texts (see paper for N)
- features: MTLD (mean length of TTR≥0.72 factor strings), vocd-D, HD-D (hypergeometric,
  draws=42), TTR, Maas, Yule's K
- main_finding: MTLD only index not varying with text length in their tests; HD-D
  viable vocd-D alternative; MTLD + vocd-D/HD-D + Maas capture partly unique information —
  use more than one index.
- limitations: validation contexts differ from Not-AI genres; implementation choices
  (threshold 0.72, draws 42) must be reported; short texts still unstable
- supports: stdlib MTLD + HD-D alongside TTR with length caveats (module: `lexical.py`)
- does_not_justify: diversity targets ("good writing has MTLD > X")
- module: not_ai_core.lexical
- confidence: verified (abstract + publisher record 2026-10-04; full text not re-extracted)

## E07 — Agarwal, Naaman & Vashistha, CHI 2025

- source: Agarwal, D., Naaman, M., & Vashistha, A. (2025). AI Suggestions Homogenize
  Writing Toward Western Styles and Diminish Cultural Nuances. CHI 2025, Art. 1117.
- doi: 10.1145/3706598.3713564
- research_question: What happens when Western-centric AI suggestions meet non-Western writers?
- corpus_size: 118 participants (India + US), controlled cross-cultural writing tasks
- language: English (Indian English vs American English)
- features: within/cross-culture similarity, style adoption, cultural-nuance retention
  (food/festival descriptions, rhetorical habits)
- main_finding: AI suggestions led Indian participants to write more like Americans;
  homogenisation of both what and how; greater efficiency gains for Americans;
  erosion of culture-specific expression.
- limitations: one model family/tasks; lab tasks; India/US only — do not generalise
  to all varieties mechanically
- supports: cultural-preservation principle (infer variety from evidence; never
  normalise to US English; negative controls for L2/formal English) (modules:
  `cultural.py`, benchmarks, SKILL.md)
- does_not_justify: nationality stereotyping; treating any L2 pattern as defect
- module: not_ai_core.cultural
- confidence: verified (ACM + arXiv record 2026-10-04)

## E08 — Moon, Green & Kushlev 2025, CHB Artificial Humans

- source: Moon, K., Green, A. E., & Kushlev, K. (2025). Homogenizing effect of LLMs
  on creative diversity. Computers in Human Behavior: Artificial Humans 6, 100207.
- doi: 10.1016/j.chbah.2025.100207
- research_question: Do LLMs reduce collective creative diversity even when helping individuals?
- corpus_size: human vs GPT-4 essays; collective-diversity growth-rate metric
- features: individual DSI diversity vs collective diversity growth rate
- main_finding: Human essays higher collective diversity growth; GPT-4 homogenises
  across users even when individual outputs look diverse (prompt/parameter tweaks
  did not remove the effect).
- limitations: specific tasks/models; metric-novel; effect sizes task-dependent
- supports: anti-homogenisation design — no single "good writer" personality;
  preserve author tendencies; pairwise/collective evaluation thinking (modules:
  SKILL.md, `voice.py`, benchmarks)
- does_not_justify: claiming any single edit "increases diversity" measurably
- module: skill design / voice
- confidence: verified-abstract (DOI landing + abstract 2026-10-04)

## E09 — ISO 24495-1:2023 Plain Language

- source: ISO 24495-1:2023 Plain language — Part 1: Governing principles and guidelines.
- research_question: What makes documents work for readers? (standard, not a study)
- features: 4 principles — Relevant (readers get what they need), Findable,
  Understandable, Usable — with guidelines; explicitly NOT mechanical readability scores
- limitations: examples English-only; applies to text documents; translation/accessibility
  need companion guidance
- supports: document-level review dimensions with separate findings, no single plain-language
  score (module: `plain_language.py`)
- does_not_justify: "short sentences + easy words = plain language"; universal score
- module: not_ai_core.plain_language
- confidence: verified (ISO catalogue + preview TOC 2026-10-04)

## E10 — ASD-STE100 Issue 9 (2025-01-15)

- source: ASD Simplified Technical English Maintenance Group. ASD-STE100 Simplified
  Technical English, Issue 9 (Standard for Technical Documentation), 2025-01-15.
- research_question: Controlled language for safe, translatable technical documentation
  (standard, not an empirical study)
- features: ~900 approved words (one meaning, one part of speech) + ~1200 non-approved
  with alternatives; 53 writing rules (9 sections); technical nouns/verbs; active voice;
  procedural imperatives; conditions-before-actions for safety; -ing restrictions;
  warnings/cautions placement; terminology control
- limitations: proprietary dictionary (request free official copy from STEMG; do NOT
  redistribute); technical-docs scope only; AI output can look STE-like without complying
  (STEMG warning)
- supports: `technical-ste-inspired` (public principles) vs `technical-ste-verified`
  (user-supplied dictionary+glossary required; never claim compliance without them)
  (modules: `ste.py`, `scripts/ste_check.py`, reference)
- does_not_justify: default STE style for all writing; "STE-compliant" claims from heuristics
- module: not_ai_core.ste
- confidence: verified (asd-ste100.org Issue 9 pages 2026-10-04; dictionary not reproduced)

## E11 — Liang et al. 2023, Patterns (detector bias)

- source: Liang, W., et al. (2023). GPT detectors are biased against non-native English
  writers. Patterns. DOI 10.1016/j.patter.2023.100779.
- research_question: Do detectors misclassify non-native writing?
- corpus_size: TOEFL vs native 8th-grade essays across 7 detectors (as reported)
- main_finding: Severe false-positive bias on evaluated non-native samples (~61% vs ~5%).
- limitations: evaluated detectors/models era-bound; do not transfer rates to new tools
- supports: fairness release condition; constrained style is never a defect (modules:
  `cultural.py`, benchmarks, detector-literacy)
- does_not_justify: treating any detector rate as transferable; L2 normalisation
- module: not_ai_core.cultural / detector-literacy
- confidence: secondary (well-documented; primary numbers from existing repo brief)

## E12 — Sadasivan et al. 2023 (detection limits)

- source: Sadasivan, V. S., et al. (2023). Can AI-generated text be reliably detected?
  arXiv:2303.11156.
- research_question: Theoretical/practical limits of text-only detection under overlap + paraphrase.
- main_finding: Detection fragile when distributions overlap and text is edited.
- supports: never promise authorship verdicts or detector outcomes (skill-wide)
- does_not_justify: any detection feature
- module: skill stance
- confidence: secondary

## E13 — Dugan et al. 2024, ACL (RAID robustness benchmark)

- source: Dugan, L., Hwang, A., Trhlik, F., Zhu, A., Ludan, J. M., Xu, H.,
  Ippolito, D., & Callison-Burch, C. (2024). RAID: A Shared Benchmark for
  Robust Evaluation of Machine-Generated Text Detectors. ACL 2024 (long papers),
  pp. 12463-12492.
- doi: 10.18653/v1/2024.acl-long.674
- research_question: Are detectors robust across models, domains, decoding
  strategies, and adversarial attacks?
- corpus_size: 6M+ generations (11 models, 8 domains, 11 attacks, 4 decoding
  strategies); 12 detectors (8 open, 4 closed)
- language: English
- features: one attack inserts U+200B zero-width space around visible characters
- main_finding: Current detectors are easily fooled by adversarial attacks and
  sampling variations.
- limitations: detector-era bound; benchmark attack strength is fixed
  ("every other character"); do not transfer exact fool rates to new detectors
- supports: defensive Unicode hygiene (analysis-normalized measurement);
  never an evasion exporter (modules: `unicode_hygiene.py`, gate, diagnose)
- does_not_justify: inserting invisible characters; any detector-score promise
- module: not_ai_core.unicode_hygiene
- confidence: verified (ACL Anthology record + paper PDF checked 2026-10-04)

## E14 — Mady et al. 2026 (DeBERTa-ConPara attack-aware detection)

- source: Mady, M., Li, Y., Reschke, J., & Schuller, B. W. (2026).
  DeBERTa-ConPara: Attack-Aware and Deployment-Realistic Detection of
  AI-Generated Text. AACL-IJCNLP 2026. arXiv:2610.00883 (posted 2026-10-01).
- research_question: Can a deployment-oriented detector stay robust under
  distribution shift and adversarial surface perturbations?
- corpus_size: 1.55M-document leakage-free training corpus (per project page);
  trained over HC3 Plus, M4, MAGE, RAID
- features: homoglyph, zero-width, whitespace, typographic attacks; Unicode
  preprocessing placement (train-time vs inference-time)
- main_finding (directional): Unicode normalization helps at inference time
  and harms at training time (reportedly deduplicates adversarial supervision;
  project reports 35.4% of RAID rows collapsing). Full effect tables not
  independently re-verified here.
- limitations: very recent preprint (3 days old at verification); do not quote
  precise restoration numbers from this registry; homoglyph handling is out of
  scope for Not-AI's current patch
- supports: inference-time (analysis-time) normalization as defense; never
  train-time/bundled evasion (modules: `unicode_hygiene.py`)
- does_not_justify: detector claims for Not-AI; homoglyph promises
- module: not_ai_core.unicode_hygiene
- confidence: verified-abstract (arXiv landing + Hugging Face model page +
  project page checked 2026-10-04)

## E15 — Unicode Standard (ZWSP) + UTS #39 / #55 (contextual handling)

- source: The Unicode Standard (Chapter 16, Southeast Asian scripts; Chapter 23,
  Special Areas and Format Characters); UTS #39 (security mechanisms), UTS #55.
- research_question: Standards guidance (not an empirical study).
- features: U+200B ZERO WIDTH SPACE as legitimate break opportunity in Thai,
  Myanmar, Khmer, Lao, Japanese; ZWJ/ZWNJ orthographic and emoji roles
- main_finding: ZWSP is Format category, normally zero width; invisible
  controls and confusables require contextual handling.
- limitations: standard describes correct use, not detector outcomes
- supports: contextual preservation (Thai breaks, Persian/Arabic ZWNJ, emoji
  ZWJ) inside hygiene normalization (modules: `unicode_hygiene.py`)
- does_not_justify: blanket stripping; authorship or intent inferences
- module: not_ai_core.unicode_hygiene
- confidence: verified (Unicode code charts, UAX #14, version chapters checked
  2026-10-04)

## How to cite inside Not-AI

Rule metadata carries `evidence_ids` (e.g. `["E01","E05"]`). `gate --explain <rule>`
renders finding → evidence → limitation → genre caveat from this registry via
`not_ai_core/evidence.py`. Do not hand-copy summaries into new docs; import them.
