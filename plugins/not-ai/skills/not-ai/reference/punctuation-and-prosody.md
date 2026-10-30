# Punctuation and prosody review

Read this reference when inspecting sentence boundaries, clause cadence,
monotonous period-only passages, informal social punctuation, or author-specific
punctuation habits.

## Core principle: natural variation is not broken grammar

Punctuation marks do structural and prosodic work: they show where clauses
start and stop, how claims relate to one another, and how a sentence sounds
when read aloud.

Controlled perturbation studies (Chen et al., EMNLP 2023; Huang et al., ACL
2024; Li et al., Findings of NAACL 2025) show that deleting periods or
inserting tight ellipses can shift external classifier scores on short texts
because missing stops cause sentence splitters to fuse adjacent sentences and
inflate measured sentence-length variance. However, dropping required periods
produces ungrammatical run-on sentences that damage reader comprehension.

Not-Ai never deletes required punctuation, introduces comma splices, or fuses
sentences to alter a statistical metric.

## What to review by layer

### 1. Boundary integrity vs intentional informality

- **Formal, academic, student, technical, and email genres** require reliable
  sentence-ending punctuation (`.`, `?`, `!`). Repair fused sentences (such as
  a lowercase word followed directly by a new capitalized clause), tight
  ellipses (`word...Next`), double periods (`..`), comma splices, and
  unbalanced parentheses.
- **Casual social and microblog genres (`social`, `x`)** legitimately omit the
  final paragraph period or use trailing ellipses when that matches the writer's
  register. Do not force academic punctuation onto casual notes.

### 2. Clause prosody and period-only monotony

- Instruction-tuned drafts often string together six or more medium-length
  declarative sentences separated only by periods, or open half their sentences
  with a front-loaded introductory comma clause (`In addition, ...`, `By
  leveraging X, ...`).
- When a passage reads flat, vary clause structure through meaning:
  - join two closely linked claims with a semicolon, colon, or coordinating
    conjunction when one explains or contrasts with the other;
  - split overloaded 25+ word sentences that lack internal punctuation when they
    carry two separate jobs;
  - let the grammatical subject and verb arrive early in most sentences rather
    than opening every sentence with a prepositional or participial phrase.

### 3. Protected non-prosodic punctuation

Never alter punctuation inside decimal numbers (`3.14`), comma-grouped figures
(`1,420`), timestamps (`2:14 a.m.`), abbreviations (`Dr.`, `e.g.`, `U.S.`),
initials, citations (`(Dugan et al., 2024)`), URLs, or code spans.

### 4. Writer-specific punctuation habits

Stylometric research (Grieve 2007; Lagutina et al. 2019; Darmon et al. 2021)
shows that punctuation distributions (comma density, semicolons, colons,
parentheticals, questions) are part of an author's stylistic fingerprint once a
reference sample reaches roughly 300+ words. When `voice-match` is requested,
run `scripts/punctuation_audit.py draft.txt --genre <genre> --reference author.txt`
to check whether the draft's punctuation habits align with the supplied sample.
