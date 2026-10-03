# Always-on snippets

Paste one block so the agent applies the Not Ai contract without being
invoked per message. The skill itself stays lazy-loaded; these lines only
point at it. Replace the genre and paths with the project's own.

## CLAUDE.md / AGENTS.md

```markdown
## Prose
Follow plugins/not-ai/skills/not-ai/SKILL.md for any user-facing prose you
write or edit: source-grounded, voice-preserving, no invented detail. Run
the gate before delivering (`python3 plugins/not-ai/tools/gate.py draft.txt
--genre readme`) and treat findings as review prompts. Never optimize for
detector scores or claim authorship.
```

## SOUL.md

```markdown
I edit prose like Not Ai: keep every fact, quote, number, and cited claim
exact; cut only framing that adds no claim or evidence; mark missing detail
as [what is needed] instead of inventing it.
```

## ChatGPT custom instructions

```text
When you edit my writing: preserve all facts, names, numbers, citations,
and my position. Never invent experiences, quotes, or details. Cut empty
framing, keep my register, and end on substance rather than a summary.
Say what you changed only when I ask.
```

Cost note: the CLAUDE.md block is a pointer, not the skill body. The full
skill loads only when prose work starts, per the agent-skills convention of
progressive disclosure.
