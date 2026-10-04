# ASD-STE100 and Not-AI: two different kinds of clarity

Read this reference only for technical documentation where safety, translation,
and repeatable action matter. STE is not the default style for Not-AI.

## The distinction (do not conflate)

- **General editorial clarity** (Not-AI default): the writing contract decides.
  Purpose, audience, genre, and the writer's own voice govern every edit.
  Nominalization, passive voice, long sentences, and field terms stay when they
  serve the reader.
- **ASD-STE100 technical control** (opt-in): a controlled language for technical
  documentation where ambiguity can injure, strand, or mistranslate. Authority:
  ASD Simplified Technical English Maintenance Group (STEMG), ASD-STE100
  Simplified Technical English, **Issue 9, 15 January 2025** (now titled
  *Standard for Technical Documentation*). The official standard and its
  dictionary remain the authority. This file is a map, not the standard.

The STEMG specifically warns that AI output can *look* STE-like without
actually complying. Not-AI preserves that warning everywhere.

## What STE controls (public principles, Issue 9 structure)

- **Approved vocabulary:** ~900 approved words, each with one approved meaning
  and one approved part of speech (one word / one meaning / one POS).
  ~1200 non-approved words with approved alternatives. Do not redistribute the
  dictionary here; request the free official copy from asd-ste100.org.
- **Technical nouns / technical verbs:** project- or field-specific terms the
  dictionary cannot list. They must be declared in a project glossary and used
  consistently (terminology control, ISO 1087-1:2019-aligned in Issue 9).
- **Synonym control:** pick one approved term per concept; do not rotate synonyms
  for variety in procedures.
- **Active voice and procedural imperatives** for instructions; descriptive vs
  procedural writing kept distinct.
- **Conditions before actions where safety requires it** (warnings/cautions
  before the dangerous step, prerequisites before the procedure).
- **Ambiguity reduction:** restricted `-ing` forms, restricted participles,
  controlled sentence complexity, one instruction per sentence in procedures,
  no phrasal-verb ambiguity, consistent technical terminology.
- **Translation consistency:** short, explicit sentences; defined terms; stable
  structure so translations stay aligned.

## Two Not-AI modes (safe architecture)

- `technical-ste-inspired`: applies publicly documented principles above as
  review prompts. Output language must say **"STE-inspired"** or
  **"provisional STE review"**. Never claim compliance.
- `technical-ste-verified`: requires user-supplied `--dictionary PATH`
  (authorised ASD-STE100 Issue 9 reference) AND `--glossary PATH`
  (approved technical nouns/verbs). Only then may the report speak of
  verification *against those supplied resources*, still not "ASD-STE100
  compliant" unless the user's own STE authority signs off.

Without both resources, Not-AI must NEVER print "ASD-STE100 compliant".

```bash
python3 scripts/ste_check.py file.txt --mode inspired
python3 scripts/ste_check.py file.txt --mode verify \
  --dictionary PATH --glossary PATH
```

## Inspired-mode checks (heuristics, not compliance)

Long sentences in procedures, passive in action steps, `-ing` openers,
unapproved-synonym candidates (small public stop-list only, never the full
dictionary), missing condition-before-action order, warnings after the action,
terminology drift across sections. Each finding says what to check against the
official standard, with the rule section family, not a verdict.

## Verify-mode checks (against supplied resources)

Dictionary membership (approved / non-approved + suggested alternative from the
user's own file), one-POS violations the dictionary declares, technical-noun
consistency against the project glossary, synonym drift. Findings quote the
user's dictionary entry, never an embedded copy.

## Licensing boundary

Never bundle copyrighted/restricted dictionary material to make the checker
look complete. The checker ships with principles and a tiny illustrative
stop-list; completeness comes from the user's authorised copy.
