# Plain language at document level (ISO 24495-1)

Read this reference for documents where the reader must find, understand, and
use information. Do not reduce plain language to short sentences and easy words.

## Four dimensions (reported separately, never one score)

- **RELEVANT:** include what the reader needs; cut background that serves no
  reader task; answer the likely question first.
- **FINDABLE:** meaningful headings, appropriate lists/tables, key information
  not buried. Long documents without headings or lists fail here first.
- **UNDERSTANDABLE:** clear actors and references, defined terms, logical order,
  sentences as difficult as the audience needs — no harder.
- **USABLE:** next steps, prerequisites, warnings before dangerous actions,
  correctly sequenced instructions.

`not_ai_core/plain_language.py:review()` returns one finding per dimension.
A document can be relevant but unfindable, or understandable but unusable —
report each, fix what the task needs.
