# Cultural and language variation: preserve, do not normalise

Read this reference whenever the draft carries a consistent English variety,
regional idiom, code-switching, or L2-formal register. The edit question is:
"Will the intended reader understand this, and is this how this writer actually
communicates?" — never "Would an American copy editor write this?"

## Preservation principle (Agarwal et al. CHI 2025; Liang et al. 2023)

Western-centric AI suggestions homogenise non-Western writing toward American
norms, changing both *what* is written and *how* it is written, and detectors
disproportionately flag constrained/L2 English. Not-AI must not repeat either
harm. Concretely, Not-AI must not equate:

- American English = natural English
- native English = good English
- casual English = human English
- grammatical imperfection = human English
- Western rhetorical structure = universal writing quality

## What to infer, and how

Infer variety only from repeated evidence in the supplied text (spelling,
lexicon, address forms, discourse habits). Never stereotype from nationality,
name, or topic. `not_ai_core/cultural.py:detect_variety()` reports evidence
(spelling counts, lexicon markers, formality signals) with confidence, or
"insufficient evidence" — never a nationality label.

## Preserve unless the contract says otherwise

Spelling (`organise/organize`, `behaviour/behavior`), idioms, address forms
(`kindly`, `do the needful` where the reader understands it), code-switching,
formality and relationship language, local terminology and examples, rhetorical
directness, humour, sentence patterns, author punctuation. Normalise only when:

1. the intended reader will misunderstand, or
2. the genre/task explicitly requires another variety (house style, publisher
   brief), or
3. the writer explicitly asks for normalisation.

Otherwise keep the variety and say so in the receipt ("Kept: Indian English
spelling/idiom — intelligible to the stated reader").

## Negative controls (release condition)

Formal L2 English, Indian English, and British English fixtures must pass
without unwanted rewrites. `benchmarks/corpus/l2-formal-english` and the new
`indian-english` fixture encode this: expected action `preserve`, and any
normalisation toward US casual style is a failure. Constrained style is a
writer's reality, not a defect.

## Code-switching and local references

Do not translate, italicise-away, or explain away code-switched spans the
reader is expected to know. If the reader likely lacks the reference, add a
bracketed gloss question for the author rather than replacing the reference
with a Western equivalent.
