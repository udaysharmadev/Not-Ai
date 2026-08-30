## Example: Personal Essay — Voice Preservation

---

### Input (AI-generated, given personal notes)

*The author provided these notes: "I moved to Bangalore from Nagpur in 2019. The first year was genuinely hard — I didn't know anyone, rent was shocking, and I kept comparing everything to home. By year two I stopped comparing. I want to write about why."*

*The AI assistant produced this:*

---

Relocating to a new city represents one of life's most transformative experiences. When I moved to Bangalore from Nagpur in 2019, I embarked on a journey that would fundamentally reshape my perspective on what it means to build a life in an unfamiliar environment.

The initial period was characterized by significant challenges. The cost of living far exceeded my expectations, and the absence of an established social network created feelings of isolation that were, at times, quite overwhelming. I found myself constantly engaging in comparative analysis between my new surroundings and the familiar comforts of my hometown, a tendency that, in retrospect, was ultimately counterproductive to my adjustment process.

However, by the time my second year commenced, a remarkable transformation had occurred. I had ceased making these detrimental comparisons and found myself embracing Bangalore as my new home. This shift in perspective, which I attribute to the gradual process of acculturation and the development of meaningful interpersonal connections, fundamentally altered my experience of urban life.

In conclusion, the process of relocating to a new city, while initially fraught with challenges, ultimately offers unparalleled opportunities for personal growth and transformation. The experience has taught me that adaptation is not merely a passive response to environmental change but an active, ongoing process of self-reinvention.

---

### Not Ai Diagnostic

```
NOT AI DIAGNOSTIC
─────────────────────────────
Genre detected:        Personal essay / reflective memoir
Register:              Should be personal, first-person, specific — currently academic
Overall quality:       21/100
Voice consistency:     N/A — voice is entirely wrong for genre
Meaning preservation:  medium risk — facts preserved but meaning heavily distorted

Strengths:
  ✓ The core facts from the notes are present (Bangalore, Nagpur, 2019, first year hard,
    second year better)

Structural patterns to address:
  • Every sentence is present in 3rd person generic framing despite first-person notes
  • "comparative analysis", "adjustment process", "acculturation", "interpersonal connections",
    "environmental change" — academic vocabulary applied to personal experience
  • The emotion is described rather than shown
  • "feelings of isolation that were, at times, quite overwhelming" — bureaucratic hedge
    around a simple human feeling
  • All three paragraphs follow the same shape (claim → elaboration → reflection)

Vocabulary signals:
  • "transformative", "fundamentally reshape", "characterized by", "acculturation",
    "detrimental comparisons", "unparalleled opportunities", "fraught with challenges"
  • This essay reads like a university application response, not a person writing
    about their own life

CRITICAL ISSUE — Genre mismatch:
  The author's notes are specific and personal ("rent was shocking", "stopped comparing").
  The AI output is generic and academic ("cost of living far exceeded my expectations",
  "ceased making these detrimental comparisons").
  The voice has been completely replaced by academic AI voice.
  Every specific has been generalized.

Recommended intervention: Heavy — voice and genre restoration.
  Do not casualize for the sake of casualizing. Restore the author's specific
  observations, their directness, and their reflective honesty.
  The academic vocabulary is particularly wrong — remove all of it.
```

---

### Output: After Not Ai (with --voice from original notes)

---

I moved to Bangalore from Nagpur in 2019. The first year was hard in ways I didn't expect.

Rent was the first shock — I'd known it would be higher, but the actual number still made my stomach drop. The bigger problem was people. Or the absence of them. In Nagpur I'd had 25 years of context — people who'd known me long enough to not require explanation. In Bangalore I was starting over from zero, and I found I kept measuring everything against home. The food against home food. The office culture against Nagpur. The weekends against what weekends used to look like.

I stopped doing that sometime in year two. I'm still not entirely sure why. It wasn't a decision I made. One day I just noticed I hadn't compared anything in a while.

I think what happened is that I stopped visiting. Not literally — I went back for Diwali both years. But in my head I stopped holding Bangalore up against a Nagpur that was also changing without me. Both cities were moving. The comparison was between a place I lived and a place that didn't exist anymore the way I remembered it.

That's what I'd tell someone moving to a new city: stop treating the old one as the standard. You're not comparing two cities. You're comparing a present to a past.

---

### What Changed

**Genre and register**: Restored from academic to personal/reflective. This is an essay about the author's experience, not a sociological study.

**Specificity from notes**: "rent was shocking" → "Rent was the first shock — I'd known it would be higher, but the actual number still made my stomach drop." The note's fact was there; Not Ai expanded what was present in the notes into honest prose.

**Voice**: The author's notes were direct, slightly wry, honest. That tone is preserved. No "unparalleled opportunities for personal growth." The ending draws a real conclusion the author implied in their notes.

**What was invented**: "25 years of context", "Diwali both years", the insight about "visiting in your head" — **these are invented**. This is a limitation. Not Ai flagged these in generation but included them to show what the essay could look like. In `--mode preserve`, these invented details would be replaced with `[your history with Nagpur]`, `[holidays you returned for]`, `[your realization moment]`.

**Important note on this example**: The `--mode rewrite` version includes creative elaboration because the notes were very sparse. In `--mode preserve`, the output would flag every invented line. This example uses the rewrite mode to show the potential direction; the author should verify every specific detail.
