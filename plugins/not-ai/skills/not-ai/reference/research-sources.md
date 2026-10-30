# Research sources and limits

Read this reference when explaining why the skill reviews genre fit,
grammatical density, engagement, stock wording, or detector claims.

## Main sources

- Reinhart, Alex, et al. [*Do LLMs write like humans? Variation in grammatical
  and rhetorical styles*](https://doi.org/10.1073/pnas.2422455122). *PNAS*,
  2025. Parallel human and model continuations across several English genres,
  analyzed with 66 Biber features. The authors present the differences as
  revision and teaching opportunities, not an individual authorship test.
- Jiang, Feng Kevin, and Ken Hyland. [*Does ChatGPT write like a student?
  Engagement markers in argumentative essays*](https://doi.org/10.1177/07410883251328311).
  *Written Communication*, 2025. In that task and corpus, student essays used a
  richer range of reader-engagement features.
- Kobak, Dmitry, et al. [*Delving into LLM-assisted writing in biomedical
  publications through excess vocabulary*](https://doi.org/10.1126/sciadv.adt3813).
  *Science Advances*, 2025. A corpus-level study of vocabulary shifts in
  biomedical abstracts; not a verdict on individual documents.
- [Wikipedia: Signs of AI Writing](https://en.wikipedia.org/wiki/Wikipedia:Signs_of_AI_writing).
  A changing, context-specific field guide and not a Wikipedia policy. The page
  itself warns that its signs are descriptive and not proof.
- Sadasivan, Vinu Sankar, et al. [*Can AI-Generated Text be Reliably
  Detected?*](https://arxiv.org/abs/2303.11156), 2023. Shows practical and
  theoretical limits of text-only detection under distribution overlap and
  paraphrasing.
- Liang, Weixin, et al. [*GPT detectors are biased against non-native English
  writers*](https://doi.org/10.1016/j.patter.2023.100779). *Patterns*, 2023.
  Documents serious false positives for the evaluated non-native English
  samples and detectors.
- Dugan, Liam, et al. [*RAID: A Shared Benchmark for Robust Evaluation of
  Machine-Generated Text Detectors*](https://doi.org/10.18653/v1/2024.acl-long.674).
  *ACL*, 2024. Evaluates 12 detectors across 6M+ generations and adversarial
  perturbations, showing high sensitivity to surface and sampling shifts.
- Huang, Guanhua, et al. [*Are AI-Generated Text Detectors Robust to
  Adversarial Perturbations?*](https://doi.org/10.18653/v1/2024.acl-long.327).
  *ACL*, 2024. Shows minor character and boundary perturbations can reverse
  classifier labels without changing underlying authorship.
- Li, Xiang, et al. [*PRDetect: Perturbation-Robust LLM-generated Text
  Detection Based on Syntax Tree*](https://doi.org/10.18653/v1/2025.findings-naacl.464).
  *Findings of NAACL*, 2025. Shows surface perturbations degrade standard
  detectors while syntactic tree structures remain comparatively invariant.
- Chen, Yutian, et al. [*Token Prediction as Implicit Classification to
  Identify LLM-Generated Text*](https://doi.org/10.18653/v1/2023.emnlp-main.810).
  *EMNLP*, 2023. Demonstrates via punctuation ablation that removing ASCII
  punctuation disrupts learned clause and sentence structure in transformer
  detectors.
- Darmon, Alex, et al. [*Pull out all the stops: Textual analysis via
  punctuation sequences*](https://arxiv.org/abs/1901.00519), 2021; and
  Lagutina, Ksenia, et al. [*A Survey on Stylometric Text
  Features*](https://doi.org/10.23919/FRUCT48121.2019.8981504), 2019.
  Establish that punctuation mark distributions and sequences carry genre and
  authorial signatures in sufficiently long samples.

## Product interpretation

These sources justify contextual editorial review. They do not justify fixed
feature targets, word bans, claims of authorship, or detector optimization.
Findings depend on model, prompt, language, register, corpus, and time. Keep the
writer's source and reader's task above every proxy.
