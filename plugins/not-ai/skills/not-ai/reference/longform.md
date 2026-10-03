# Long-form review

Read this reference when the document runs over roughly 500 words. Long
documents fail differently from paragraphs: sections drift in register,
transitions go missing between headings, and a phrase that is fine twice
becomes a loop the fifth time.

## Method

1. Split on markdown headings into sections of at most 500 words. Never split
   a heading inside a fenced code block; code is not prose structure.
2. Run the gate per section with the document's single genre. The genre does
   not change per section; a methods section and a discussion section in one
   paper share one contract.
3. Check repetition across sections, not just within them. A trigram that
   appears in three or more sections is worth one look even when each local
   occurrence reads fine.
4. Keep one voice for the whole document. Compare the full draft against the
   author reference once, not per section.

`scripts/longdoc.py` automates steps 1-3:

```bash
python3 scripts/longdoc.py doc.md --genre technical
python3 scripts/longdoc.py doc.md --genre academic --json --max-words 400
```

## What to watch

- Section-order logic: does each section earn its place, or do two sections
  make the same claim?
- Heading honesty: does the section deliver what the heading promises?
- Cross-section loops: the same framing sentence opening three sections.
- Register drift: contractions and fragments appearing in one section of a
  formal document but not the others.
- Masked measurement: code fences, inline code, blockquotes, link markup,
  and URLs are excluded from counts so identifiers and quoted examples do
  not read as the author's diction.

Advisory throughout: a flagged repeat across sections may be intentional
(a refrain, a defined term). Keep intentional repetition; cut the rest.
