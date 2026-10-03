# Voice persistence

Read this reference when a project keeps an author voice file across sessions,
or when `voice-match` output needs to survive beyond one conversation.

## The file

Keep one `voice.md` at the project root. It holds consented material only:
short samples of the author's own writing, preferred terms, and phrases to
avoid. Two or three paragraphs are enough to start; around 300 words makes
the deterministic comparison stable, and below that
`scripts/voice_profile.py` marks its verdicts tentative rather than guessing.

```markdown
# Voice: [author]
## Samples
[2-3 genuine passages, unedited]
## Prefer
[terms and constructions the author actually uses]
## Avoid
[phrases the author has rejected before]
```

## Using it

Load the file instead of asking for samples again. Compare the draft with:

```bash
python3 scripts/voice_profile.py --reference voice.md --draft draft.txt
```

The report covers rhythm variation, short-sentence rate, stance markers,
contraction use, specificity, function-word habits, and opening variety.
Each dimension reads `aligned`, `drifted`, or `introduced in draft`, with the
raw figures beside it.

## Rules

- Drift is a prompt to re-read, never evidence about who wrote the draft.
- Copy tendencies (contraction rate, opener variety), not memorable phrases.
- Never imitate a living author's voice unless the user is that author or
  supplied their own text as the target.
- Do not "upgrade" plain or second-language English into idiomatic slang
  unsolicited. Detector design already penalizes constrained style unfairly
  (Liang et al., 2023); the skill must not repeat that penalty as editing.
- When the reference is thin, say so and weigh the draft's genre fit more
  heavily than the comparison.
