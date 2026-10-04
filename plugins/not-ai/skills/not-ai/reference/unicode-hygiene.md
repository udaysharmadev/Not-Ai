# Unicode hygiene: measure what the reader sees

Read this reference when diagnostics look wrong for clean-looking prose, or
before trusting any count on pasted text.

## What it is

A defensive preflight, not a detector trick. Not-AI reveals invisible or
unusual Unicode (zero-width spaces, word joiners, soft hyphens, bidi controls,
tag characters, non-breaking and other Unicode spaces), then measures an
analysis-only normalized copy. The writer's source text is never changed, and
Not-AI never inserts invisible characters.

```bash
python3 scripts/unicode_hygiene.py draft.txt
python3 scripts/unicode_hygiene.py draft.txt --show-normalized
```

## How to read a report

- `warning` (embedded in an ASCII token): can split words and corrupt counts.
  Clean the deliverable.
- `review` (bidi/tag controls, lone zero-width): inspect; analysis excludes
  them, delivery keeps raw bytes.
- `contextual` (join controls in non-Latin text or emoji, Thai break hints,
  ordinary non-breaking spaces): usually legitimate. Preserve unless an
  ASCII-token split is actually present.

Presence is an encoding fact, never evidence of who wrote the text or why the
characters are there.

## What stays

Persian/Arabic ZWNJ, emoji ZWJ sequences, Thai `U+200B` break opportunities,
and meaningful non-breaking spaces survive normalization. Only ASCII-token
splits, control presentations, and separator canonicalization (unusual space
to ASCII space) are touched — and only in the analysis copy.

## Skill behavior

The gate adds a `unicode-hygiene` review finding (never an error, never an
authorship claim) when suspicious characters are present, and all counts
already reflect the normalized view. Diagnose, long-document review, and
benchmark overlap do the same. If hygiene fires, clean the pasted text and
re-run; do not "fix" it by rewriting sentences.
