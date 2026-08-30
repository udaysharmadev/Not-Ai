## Example: Already Natural — No Significant Changes

This example demonstrates Not Ai detecting that text is already natural and making minimal or no changes.

---

### Input

The following is a paragraph written by a human (source: a developer's blog post about debugging a production incident).

---

I spent three days last month hunting a bug that only showed up under load. The issue was in how we handled connection timeouts — specifically, a race condition between the health check and the reconnection logic. I found it by adding more aggressive logging and watching the logs during a controlled load test. Not fun, but at least I know what to look for next time.

---

### Not Ai Diagnostic

```
NOT AI DIAGNOSTIC
─────────────────────────────
Genre detected:        Personal blog / developer reflection
Register:              Informal, personal, first-person
Overall quality:       91/100
Voice consistency:     N/A (no sample provided, but voice internally consistent)
Meaning preservation:  low risk

Strengths:
  ✓ Specific (three days, last month, health check, reconnection logic, load test)
  ✓ First-person throughout — author present in the text
  ✓ Sentence length varies naturally (25, 20, 18, 8 words)
  ✓ Fragment "Not fun" used deliberately for rhetorical weight
  ✓ Ends with genuine observation, not a generic summary
  ✓ No AI-associated vocabulary
  ✓ No mechanical transitions
  ✓ No nominalization overload

Structural patterns to address:
  None significant.

Vocabulary signals:
  None.

Recommended intervention: None — text is already natural.
  This text reads like a person wrote it because a person wrote it.
  The specific details (three days, the specific technical cause, the specific fix method)
  are doing the work. Not Ai should not touch it.
```

---

### Output

*(No changes made)*

I spent three days last month hunting a bug that only showed up under load. The issue was in how we handled connection timeouts — specifically, a race condition between the health check and the reconnection logic. I found it by adding more aggressive logging and watching the logs during a controlled load test. Not fun, but at least I know what to look for next time.

---

### Why Nothing Changed

This text has all the properties that make writing feel authored:

1. **Specific**: "three days", "last month", "health check and the reconnection logic", "controlled load test" — every claim is grounded in something particular.
2. **Personal presence**: "I spent", "I found it by" — the author is visible in the action.
3. **Natural rhythm**: The sentences vary from 25 words down to 2 words ("Not fun") deliberately.
4. **Genuine ending**: "at least I know what to look for next time" — a real conclusion drawn from a real experience, not a summary of what was just said.
5. **No inflation**: No claims about the "transformative impact" of debugging. Just: this happened, here's how I fixed it.

Not Ai's job is not to find something to change. It is to identify what is genuinely machine-like and address it. When text is already natural, the correct output is: nothing.

**Intervention rate**: 0%.

---

### What Over-humanization Would Look Like

A naive humanizer might "improve" this text to:

> So, I spent a solid three days last month tracking down this gnarly bug that only popped up under heavy load — super annoying! Turns out, it was a classic race condition lurking in how we handled connection timeouts between the health check and reconnect logic. I ended up cranking up the logging and ran a controlled load test, and boom, found it! Wasn't exactly fun, but hey, at least now I know what to watch for. 😅

This is worse. The original precision ("three days", specific technical terms) is preserved but buried in forced enthusiasm. The author's measured, wry tone ("Not fun, but at least...") has been replaced with performed excitement. This is the "over-humanization" failure — making writing louder, not better.

Not Ai explicitly forbids this.
