# Example: Gen AI Article

## Input (AI-generated)

> In today's rapidly evolving technological landscape, Generative AI represents a paradigm shift in how we approach problem-solving and innovation. By leveraging the power of large language models, organizations across various sectors are fundamentally transforming their operational frameworks. Furthermore, the implications of this transformative technology are far-reaching and multifaceted. It is worth noting that while the benefits are substantial, the challenges are equally significant. In conclusion, as we navigate this unprecedented era of technological advancement, it is crucial that we foster a nuanced understanding of both the opportunities and the ethical considerations that accompany this groundbreaking innovation.

---

## Diagnostic

```
NOT AI DIAGNOSTIC
─────────────────────────────
Genre:    General article / blog
Register: Formal-general

Structural patterns found:
  • Nominalization density: 72.9/1,000 words — human norm is 25–40
    — "technological landscape", "operational frameworks", "implications",
       "considerations", "advancement"
  • Mechanical transitions: 3
    — "Furthermore," "It is worth noting that" "In conclusion,"
  • Burstiness: 0.388 — all sentences the same length, no variation

AI vocabulary (8 hits in 96 words — severe):
  • "paradigm shift" — generic claim not demonstrated
  • "leveraging" — decorative participial opener
  • "transformative", "groundbreaking", "multifaceted", "nuanced",
    "crucial", "foster" — none add meaning

Specificity failures:
  • "organizations across various sectors" — which organizations?
  • "far-reaching and multifaceted implications" — name one implication
  • "unprecedented era" — routine phrase
  • "opportunities and ethical considerations" — both vague

Intervention: Heavy
```

---

## Output (after Not Ai)

Generative AI went mainstream quietly. Not with a product launch — with your colleagues starting to use it for first drafts, your inbox filling with emails that sound oddly similar, your company's job postings adding "AI literacy" to requirements. The shift happened in the daily routine before anyone declared it a shift.

What it does well: it writes fast and reads passably. What it does badly: it has no idea when it's wrong. A model will state a fabricated statistic with the same confidence it states a verified one. That asymmetry — fluency without judgment — is the real problem, not the technology itself.

The harder question isn't whether to use it. Most people already have. It's how to catch the errors it doesn't know it's making.

---

## What changed

| Before | After | Why |
|--------|-------|-----|
| "In today's rapidly evolving technological landscape" | Cut entirely | Generic opener with zero information |
| "represents a paradigm shift" | "went mainstream quietly" | Specific claim instead of abstract label |
| "By leveraging the power of large language models" | Cut | Decorative participial opener |
| "organizations across various sectors are fundamentally transforming their operational frameworks" | "your colleagues starting to use it for first drafts" | Made concrete and specific |
| "Furthermore," | Cut | Connection was already clear |
| "It is worth noting that" | Cut | False hedge before obvious point |
| "In conclusion, as we navigate this unprecedented era" | Cut | Restated nothing |
| "nuanced understanding of opportunities and ethical considerations" | "catch the errors it doesn't know it's making" | Specific instead of abstract |
| 3 em dashes in one paragraph | 0 | Em dash as dramatic pause is an AI cliché |

Words: 96 → 107 (added specificity, not length)
Gunning Fog: 21.3 → ~10 (estimated)
AI vocabulary hits: 8 → 0
