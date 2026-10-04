# Not-AI v3 Gap Analysis

Date: 2026-10-04. Baseline: v2.2.0 (55 tests green). Author: upgrade audit for Not-AI 3.0.

## 1. What already works (keep untouched)

- **Source-grounded contract.** SKILL.md non-negotiables (preserve facts/claims/citations,
  no invention, no detector optimisation, restraint, bracketed gaps, prompt-injection
  resistance) are correct and tested (`test_plugin_payload.py`). Do not weaken.
- **Small hard-fail surface.** `not_ai_core/gate.py:evaluate()` fails only on empty
  output and missing `--protect` literals. Typography is advisory by default,
  `HOUSE_STYLE` ASCII opt-in. This taxonomy instinct is right; v3 makes it explicit.
- **Masked measurement.** `mask_for_counts()` (fenced/inline code, blockquotes),
  abbreviation-aware splitter, markdown-link exclusion from bracket slots, quoted-span
  exclusion from vocab. Correct; preserve in `text.py`.
- **Parity discipline.** `_shared.py` canonical primitives + `verify_measure.py` parity
  suite. SESSION_FAILURES.md lessons (analyzer drift, scan return-type, validator
  runtimes) are institutional memory. Keep.
- **Voice comparison as prompt, not verdict.** `voice.py` function-word + rhythm +
  stance model with 300-word sufficiency caution is the right stance. Needs confidence
  tiers, not replacement.
- **Benchmark honesty.** `benchmark.py` token-overlap proxy explicitly NOT semantic
  similarity, per-pair worked caveats in `benchmarks/README.md`, no aggregate score,
  no leaderboard, `expected_action` + `protected_facts` + blinded `pairwise.py`
  asking "which needs less author correction?". Keep and expand.
- **Detector literacy.** `reference/detector-literacy.md` + `flag_response.py` base-rate
  math correctly refuse authorship verdicts and score optimisation.
- **Packaging determinism.** `sync_skill.py`, `build_single_file.py`, `package_skill.py`
  byte-deterministic bundles, CI checks. Keep.

## 2. What is heuristic (useful, but must be labelled as such)

| Area | Current state | Risk |
|---|---|---|
| Nominalization suffix regex (`_shared.py`, `gate.py`) | Counts `nation/moment` as nominalizations; ~90/1k vs Reinhart tagged 14.6/1k | Numbers look authoritative; cross-paper comparison is invalid. Already warned in comments but not in rule metadata. |
| Participial opener lists | Fixed -ing word lists + prepositional/mid-sentence extensions | Recall unknown; no parser; misses reduced relatives, mislabels gerund subjects (`comma plus -ing` note admits this). |
| Passive proxy (`be + -ed/-en`) | Rough estimate | False positives/negatives; paper shows models *underuse* agentless passives, so low figure is not automatically good (correctly noted, weakly surfaced). |
| Tier-1/2 vocab + inflections | Stemming map, quoted-span exclusion | Corpus-scale excess ≠ document signal; single occurrence rarely matters. Currently review/warning severities — correct — but no phrase-cluster model. |
| Sentence rhythm (SD<4, CV, burstiness) | Uniformity prompt | Human genres (docs, legal) are legitimately uniform; thresholds are proxy-scale heuristics. `diagnose.py` correctly refuses to act on burstiness verdicts in `measure.py` report, but `gate.py` still fires `sentence-rhythm` at SD<4. |
| Contraction floors (30–80 tokens) | Per-genre floors | Heuristic; no writer baseline. Correctly advisory but presented without confidence. |
| Stance balance (`_shared.stance_balance`) | Absent/sparse/calibrated split with floors | Fixed 3-marker/2.0-per-1k floors are heuristics on proxy scale. Correctly refuses verdict below floor. |
| Readability bands (`policy.grade_low/high`) | Flesch-Kincaid per genre | 100-word minimum correctly added; still formula-based, English-only. |
| Choppy-run (3× <8 words) | Advisory except fragment-allowing genres | Heuristic; reports combine into one idea — reasonable. |
| `expected_action preserve` (overlap>0.5, <20%) | Heuristic on overlap proxy | Documented as heuristic. Fine. |

None of these should be deleted. All need `category: RESEARCH_SIGNAL` or
`HEURISTIC` labels, proxy-vs-parsed naming (`nominalization_suffix_proxy`),
and confidence downgrading with distance from writer/genre evidence.

## 3. What is research-grounded (and how far it legitimately reaches)

- **Reinhart et al. 2025 (PNAS, DOI 10.1073/pnas.2422455122).** 66 Biber features,
  parallel human/model continuations, instruction-tuned noun-heavy density,
  participial 2–5×, nominalization 1.5–2×, vocabulary 84–171× on 14 words.
  Supports *review prompts by genre*, never quotas, bans, or authorship claims.
  Paper's own framing: teachable revision moments. Current code respects this
  except README table risks being read as targets — v3 adds "do not use as targets" guard.
- **Jiang & Hyland 2025 (DOI 10.1177/07410883251328311).** 145+145 argumentative
  essays; students richer engagement (questions, asides). Supports engagement review
  in argumentative genres only. Current `tone_markers` counts hedges/boosters/questions/
  reader-address but has no genre-conditional interpretation — v3 adds it.
- **Kobak et al. 2025 (DOI 10.1126/sciadv.adt3813).** 15M+ PubMed abstracts,
  excess-vocabulary lower bound ≥13.5% 2024 abstracts LLM-processed. Supports
  *corpus-level* cluster review, never single-word document verdicts. Current code
  correctly avoids blacklist language; v3 adds phrase-pattern layer.
- **Agarwal/Naaman/Vashistha CHI 2025 (DOI 10.1145/3706598.3713564).** 118 US/India
  participants; Western-centric suggestions homogenise Indian writing toward US norms.
  Currently only implicitly covered ("never flag L2 as suspicious"). v3 makes it a
  first-class cultural-preservation principle with negative controls.
- **Moon/Green/Kushlev 2025 (DOI 10.1016/j.chbah.2025.100207).** Diversity-growth-rate
  homogenisation of collective creativity. Supports anti-homogenisation design
  (no single "good writer" personality). Currently absent — v3 adds.
- **McCarthy & Jarvis 2010 (DOI 10.3758/BRM.42.2.381).** MTLD length-invariant,
  HD-D viable vocd-D alternative. Currently only plain TTR/content-TTR — v3 implements
  MTLD + HD-D stdlib.
- **ISO 24495-1:2023.** Relevant/findable/understandable/usable at document level.
  Currently readability formulas only — v3 adds 4-dimension document review.
- **ASD-STE100 Issue 9 (2025-01-15).** Controlled language for technical docs.
  Currently absent — v3 adds inspired/verified split, never default style.
- **Biber MDA (1988 etc.).** 6 dimensions (involved/informational, narrative,
  explicit/situated, persuasion, abstract, online elaboration); features work in
  clusters. Currently single-axis formal/informal + isolated feature flags — v3 adds
  cluster-aware interpretation.

## 4. What is currently missing (v3 scope)

1. Explicit rule taxonomy (INVARIANT/GENRE/VOICE/REGISTER/RESEARCH_SIGNAL/
   HOUSE_STYLE/USER_PREFERENCE/UNSUPPORTED) with machine-readable metadata.
2. Semantic fidelity beyond literal strings (modality, negation, causality,
   chronology, actor/observer, scope, conditions/exceptions).
3. MTLD/HD-D; parsed-vs-proxy naming; optional parser adapter with clean degrade.
4. Discourse/cohesion layer (overlap, referential chains, connective function,
   topic drift) — `cohesion.py` absent.
5. Information-structure review (given→new, topic-comment, paragraph roles).
6. Voice confidence tiers (insufficient/weak/usable/strong) + bootstrap variation;
   per-metric minimum samples; no phrase copying.
7. Cultural-preservation reference + fixtures + negative controls.
8. Document-level plain-language review (4 ISO dimensions, no single score).
9. Phrase-pattern vocabulary review (significance inflation, ceremonial conclusion…).
10. Density as multidimensional genre-relative property, not reduction target.
11. Explicit anti-fake-humanisation prohibitions (already in SKILL non-negotiables,
    missing as tested code + benchmark negative controls).
12. Contextual baselines hierarchy (writer → publication → genre corpus → literature
    → heuristic) with confidence.
13. Composable genre policies (dimensions, not 9 isolated hard-codes); new genres
    (x/social split, abstract vs paper, procedure, API docs, tutorial, proposal,
    executive summary, marketing).
14. Intervention planner (NONE/LIGHT/MODERATE/HEAVY/RESTRUCTURE/BLOCKED) as tested module.
15. Human Output Benchmark expansion (Indian English, procedure, contradictory facts,
    citation-heavy, code-mixed, prompt-injection, voice sufficiency splits, STE).
16. Metamorphic/invariant tests (may→will, negation flip, chronology, exception loss…).
17. Long-document global map (claims, terminology, chronology, cross-refs) + post-pass.
18. Provenance `gate --explain <rule>` from shared metadata (currently static dict,
    no evidence_ids/limitations/genre caveats).
19. STE-inspired/verified architecture + `ste_check.py`.
20. SKILL.md 14-step pipeline (contract→…→final output) with paragraph roles.

## 5. What should be replaced vs remain untouched

- **Replace:** universal "Never add Em Dashes" as scientific principle → HOUSE_STYLE
  opt-in (keep project house style + SKILL enforcement text tests rely on, but label
  honestly); any residual quota-like reading of profile.md (already fixed, keep guard);
  single-axis formality; plain-TTR-only diversity; literal-only fidelity.
- **Keep untouched:** hard-fail surface, masking, parity suite, benchmark honesty
  language, pairwise question, detector-literacy stance, deterministic packaging,
  zero-dependency base install.
- **Quarantine as UNSUPPORTED if found:** any rule without evidence or editorial
  rationale. Audit found none currently shipped as hard rules — the gate's advisories
  all have at least heuristic rationale. The em-dash universal is the one case
  reclassified HOUSE_STYLE, not deleted, because tests + skill text normatively
  require it and the repo may keep it as its own house style.

## 6. Where metrics are too fragile for strong conclusions

- Nominalization proxy vs tagged rates (5–6× over-count). Never compare numerically.
- Participial/passive proxies vs parsed counts. Separate names required.
- TTR on short texts; burstiness/CV on <6 sentences; grade bands <100 words
  (already gated); stance ratios below floors (already refused); opener entropy on
  few sentences; function-word distance on short drafts.
- Token-overlap as fidelity (benchmark correctly disclaims; keep disclaiming).
- Number preservation on list markers (`1. 2. 3.` false "lost numbers" — documented;
  v3 adds list-marker guard).
- Cross-model/cross-corpus generalisation of all 2024-era rates to 2026 models.
- Any single-figure "naturalness/human %" — never build (none exists; keep absence).

## 7. Consistency audit (README / skill / examples / code)

- **Consistent:** "not a detector-bypass tool", source-grounded, voice-preserving,
  advisory gate, no authorship claims. README, SKILL.md, plugin.jsons, Codex prompts
  all match after v2 fixes (tests enforce: no "does not sound like AI", no score
  promises, Codex prompts contain "preserving").
- **To fix in v3:** README research table needs finding→interpretation→limitation
  columns (currently finding-only, risks target-reading); SKILL.md em-dash rule needs
  HOUSE_STYLE label while keeping enforcement text; examples need "kept intentionally"
  cases (flagged word remains) to demonstrate contextual judgment; skill description
  "humanizing stiff writing" is acceptable (task, not bypass promise) but README
  positioning should prefer "source-grounded editing" line per spec §25.
- **Remote metadata:** do not modify GitHub repo description/fields from here;
  report recommended wording only.

## 8. Baseline evidence (2026-10-04)

- `python3 -m unittest discover -s tests`: 55 tests OK.
- `benchmark.py --corpus benchmarks/corpus --json`: 5 fixtures evaluate; preserve/
  rewrite/no-change matched.
- `benchmark.py --dry-run`: OK. `sync_skill.py --check`, `package_skill.py` validate: OK.
