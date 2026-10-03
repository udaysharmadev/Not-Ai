## Rationale: voice match

The draft's facts are fine; its voice belongs to nobody. The rewrite keeps
every checkable claim and returns the author's habits: short sentences,
"we" for team work, numbers first, no lesson at the end.

### Actions taken

| Source | Action | Result |
|---|---|---|
| "It is worth noting that the team has successfully completed a comprehensive migration to Atlas." | REMOVE frame, KEEP fact | "We've finished the Atlas migration." The contraction and "we" are the author's, from the voice file, and the team did the work so "we" is earned. |
| "The implementation of the migration methodology leverages a robust orchestration framework, ensuring a seamless transition with zero customer impact." | UNPACK, FLAG | "We cut over on [orchestrator or runbook link]." Three nominalizations become one verb. The orchestrator is never named in the draft, so the bracket marks the gap instead of inventing a tool. |
| "All 14 services were fully operational within four minutes of the cutover" | KEEP | "All 14 services were healthy within four minutes" survives almost word for word. It was the strongest sentence in the draft. |
| "which underscores the meticulous planning undertaken by the team." | REMOVE | Praise for the team, by the team, in a status update. Cut. |
| "Furthermore, the migration represents a pivotal milestone in our infrastructure evolution journey." | REMOVE | A milestone with no new fact attached. The first sentence already said the migration finished. |
| "The team demonstrated exceptional synergy throughout the process, fostering a collaborative environment that facilitated the seamless execution of this transformative initiative." | REMOVE | Nine review-list terms, zero facts. The whole sentence is packaging. |
| "The old cluster will be decommissioned on Friday. Team members should ensure that any remaining dependencies are migrated prior to the decommissioning deadline..." | RESTRUCTURE | "The old cluster goes away Friday, so move anything still on it before then." The deadline and the ask survive; the warning tone does not. |

### What the voice comparison says after the rewrite

Against the same 304-word reference, the 39-word output still reads
"drifted" on 5 dimensions, down from 6, with contractions and
self-mention now aligned. The remaining drift (hedges absent, number
density high, function-word gap noisy) is a length artifact: a 39-word
update cannot carry every habit of a 304-word profile, and it should not
try. Voice-match copies tendencies into the sentences the draft needs; it
does not pad the draft to satisfy a comparison. Chasing the remaining
verdicts would mean adding words for the tool's sake, which is exactly
what the skill refuses to do anywhere else.

### What was not done

- No orchestrator was named. "Robust orchestration framework" hides a
  missing noun, and the bracket says so.
- No lesson was added. The draft's closing warning became a direct ask,
  not a moral.
- No phrase was lifted from the voice file. "Boring, which is exactly how
  I like them" stays where it belongs. Tendencies travel; memorable lines
  do not.
- No third-party voice was imitated. The samples are the author's own,
  supplied for this purpose.

### Measured change

Nominalizations 77.6 to 25.6 per 1k (gate counts; the analyzer's own
denominator reads 25.0 on the output). Stock terms 9 unique to 0.
Transitions 2 to 0. Contractions 0.0 to 25.6 per 1k. Gate on the output:
pass, with only the bracket-slot review remaining.
