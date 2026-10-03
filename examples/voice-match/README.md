## Voice match

A corporate project update rewritten into its author's own voice, measured
against a persistent voice file. The only example in the set that uses
`voice-match`, and the one that shows what the mode is for.

| File | |
|---|---|
| [voice.md](voice.md) | The author's consented samples and preferences, 304 words |
| [input.md](input.md) | The generated update, 116 words |
| [diagnostic.md](diagnostic.md) | Source diagnostic, measured figures, and voice comparison |
| [output.md](output.md) | The rewrite, 39 words and one bracket |
| [rationale.md](rationale.md) | Per-sentence accounting and what the comparison still says |

**What this example is for.** Every other example matches the draft against
its genre. This one matches the draft against a person. The voice file
holds four past updates plus prefer/avoid lists, enough for a stable
profile (304 words, past the 300-word caution line). The comparison finds
the draft drifted on 6 dimensions: no contractions against 16.4 per 1k, no
short sentences against a 46% short rate, "the team" where the file says
"we when the team did it."

It also shows the mode's honest limit. The 39-word rewrite still reads
"drifted" on 5 dimensions, because a 39-word update cannot carry every
habit of a 304-word profile. The rewrite copies tendencies (short
sentences, "we," numbers first, no lesson) and stops there; padding the
draft to flip the remaining verdicts would be writing for the tool. The
`rationale.md` records this as a decision, not a failure.

Run it yourself:

```bash
python3 scripts/voice_profile.py --reference examples/voice-match/voice.md --draft examples/voice-match/input.md
python3 scripts/diagnose.py examples/voice-match/input.md --genre technical --reference examples/voice-match/voice.md
```
