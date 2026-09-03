# Why Word Swapping Fails

Background for judgment calls in the skill. Three things get measured, and vocabulary is the weakest.

1. **Token predictability and its variance.** How surprising each word is given the words before it, and how much that surprise fluctuates. Model prose is smooth at every position, and synonym swaps leave the smoothness intact. This is what stance, specificity, and broken canonical sequences act on.
2. **Morphosyntactic profile.** Rates of roughly 66 grammatical features. Reinhart et al. reached 93% to 98% accuracy on these alone, with no vocabulary input. The dominant signal, and what the two profile tables act on.
3. **Vocabulary distribution.** Real, but the smallest lever, and the one model makers already patch.

The profile runs in two directions. Instruction-tuned models overuse about fifteen features and underuse about twenty, so a rewrite that only deletes the overused half moves halfway and still classifies as machine. Hence suppress, restore, then break the smoothness, in that order. Rates were measured on GPT-4o and Llama 3, and the fingerprint comes from instruction tuning rather than scale or family: Llama 3 *base* sits at 94% to 102% of human on every feature while every instruct variant diverges sharply. Treat the numbers as direction plus magnitude, and verify by counting the draft.

## What each lever was worth

One passage, one lever added at a time, scored after each:

| Lever added | Score |
|---|---|
| None. Ordinary model output | 100% |
| Structural: openings, SD, paragraph ratio, one-sentence paragraph, `And` and `But` openers, word length | 38.9% |
| First two sentences off definition and superlative | 27.6% |
| Canonical sequences broken | 24.8% |
| Stance added to the recitation sentences | 16.2% |
| Per-paragraph variation fixed | 0% |

Read the shape of that, not just the endpoint. The structural block does the most work of any single lever and still leaves output classified as machine. The last two were worth 24.8 points between them, and they are the two a model is most likely to skip, because both require reading the draft rather than counting it. A draft that passes the count line and skips them lands in the twenties, which is where this file sat for three revisions.
