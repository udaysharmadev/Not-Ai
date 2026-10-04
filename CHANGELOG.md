# Changelog

## 3.0.0

- Editorial system, not humanizer: 14-step pipeline (contract → source
  protection → claim map → genre → rhetorical/information-structure review →
  diagnostics → edit plan → rewrite → fidelity/voice/genre/mechanical verification).
- Rule taxonomy: every rule is INVARIANT, GENRE, VOICE, REGISTER,
  RESEARCH_SIGNAL, HOUSE_STYLE, USER_PREFERENCE, or UNSUPPORTED, with
  machine-readable metadata in `not_ai_core/rules.py` and provenance via
  `gate.py --explain <rule>` generated from `docs/research/evidence-registry`
  (md+json). Em-dash universal reclassified as HOUSE_STYLE (enforcement text kept).
- Research: gap analysis (`docs/research/not-ai-v3-gap-analysis.md`) plus
  12-entry evidence registry with DOI, effect, limits, permitted use, and using
  module. No population difference becomes a universal rule.
- New core (stdlib-only base, optional NLP adapter degrading cleanly):
  `text.py`, `lexical.py` (MTLD threshold 0.72 + HD-D draws 42 + phrase-pattern
  clusters), `syntax.py` (proxy/parses split naming), `discourse.py` (cohesion),
  `information_structure.py` (paragraph roles, given→new, document map),
  `fidelity.py` (negation/modality/scope/chronology/actor/condition invariants),
  `cultural.py` (variety preservation, negative controls), `plain_language.py`
  (ISO 24495-1 four dimensions, no score), `ste.py`, `intervention.py`
  (NONE…BLOCKED_BY_MISSING_INFORMATION), `nlp_adapter.py`, `evidence.py`.
- Voice: multidimensional fingerprint (tendencies, never phrases), bootstrap
  within-author CV band, `reference_quality` insufficient/weak/usable/strong,
  per-dimension minimums. Small samples report low confidence.
- Genres: composable dimensions; 9 original profiles unchanged plus `x`,
  `procedure`, `api`, `tutorial`, `abstract`, `proposal`, `executive`,
  `marketing`, `essay`.
- STE: `reference/asd-ste100.md` (general clarity vs technical control) plus
  `scripts/ste_check.py --mode inspired|verify`. Inspired is provisional;
  verify needs user `--dictionary` + `--glossary`; never claims compliance;
  no dictionary material bundled.
- Benchmarks: 12 new fixtures (17 total: Indian English, dense abstract,
  procedure, email, social, contradictory facts, citation-heavy,
  negation-modality, code-mixed, prompt-injection, README, STE-inspired).
  All `expected_action` matched. New `tests/test_v3.py` (39 tests):
  metamorphic invariants, MTLD/HD-D, cohesion, voice, cultural, STE,
  taxonomy, intervention, genres.
- Diagnose: MTLD/HD-D, phrase patterns, cohesion, plain-language, variety,
  information-structure layers plus `intervention_level`. Longdoc: document
  map + global pass (drift, duplicates, contradictions, heading mismatch).
- Examples: `contextual-judgment` (kept nominalization/passive/transition/
  em dash), `cultural-preservation` (kept Indian English), `ste-inspired`.
- Docs: README research table now finding→interpretation→limitation;
  18-genre list; new module/script inventory.

## Unreleased

- Detector literacy: new `reference/detector-literacy.md` (what vendor
  scores mean, base-rate math, bias, appeal evidence) plus
  `scripts/flag_response.py` for prevalence-conditioned flag math.
- Grade bands wired: policy `grade_low/high` now drive a
  `readability-mismatch` review in `scripts/diagnose.py` (100+ words only).
- Human review tooling: `scripts/pairwise.py` runs blinded X/Y pairwise
  review with sealed JSONL records.
- Corpus: `from-notes-sparse` (rewrite with bracketed gap) and
  `l2-formal-english` (preserve on constrained prose) fixtures; `preserve`
  mode has a measurable check (overlap above 0.5, length change under 20%).
- Multilingual scope appendix with contributor template for `lang-<code>.md`.
- Voice-match worked example under `examples/voice-match/`.
- Writer docs: CI template, always-on snippets, English-scope labels,
  repository-structure and install-method fixes.
- CI now also checks the `dist/` bundle, the `.skill` bundle, and the full
  benchmark corpus on every push.
- `scripts/package_skill.py` builds a deterministic, validated `.skill`
  bundle (`dist/not-ai.skill`) for skill-upload installs.
- Three-step quickstart and stale mode-label cleanup in the README.

## 2.2.0

- Gate v2: code/quote masking for counts, abbreviation-aware splitting,
  extended participial recall (prepositional openers, mid-sentence tails),
  vocabulary stemming, markdown-link exclusion from bracket slots,
  genre contraction floors, nominalization advisories, `--explain`.
- Analyzers in lockstep: identical fixes in `_shared.py`,
  `analyze_structure.py`, and the single-file `measure.py` (parity suite green).
- New tools: `scripts/diagnose.py` (Diagnose 2.0), `scripts/voice_profile.py`
  with `not_ai_core/voice.py`, `scripts/longdoc.py` (section-chunked review),
  `scripts/build_single_file.py` (generates `dist/`).
- Skill: anti-injection rule, voice-vs-purpose separation, persistent
  voice file, long-doc mode, two new references.
- Packaging: fixed `pyproject.toml`, dropped dead `fast` mode, fixed Codex
  prompts to match the source-grounded stance, corpus `preserve` coverage.
