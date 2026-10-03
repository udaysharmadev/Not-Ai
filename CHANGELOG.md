# Changelog

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
