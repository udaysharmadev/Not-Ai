## Example: Academic Abstract

---

### Input (AI-generated)

---

This paper presents a comprehensive investigation into the nuanced relationship between machine learning model complexity and downstream performance across diverse natural language processing tasks. Leveraging a novel experimental framework that systematically varies model architectures, we demonstrate that the conventional assumption that larger models invariably outperform smaller counterparts is not universally applicable. Our findings reveal that, in certain task-specific contexts, models of moderate complexity exhibit comparable or superior performance metrics relative to their larger counterparts, particularly when training data is limited in scope. Furthermore, the implications of these findings are significant for practitioners seeking to optimize resource utilization while maintaining competitive performance levels. We conclude that a more nuanced, context-dependent approach to model selection is warranted, one that takes into consideration the specific requirements of the task at hand rather than defaulting to scale as a proxy for quality.

---

### Not Ai Diagnostic

```
NOT AI DIAGNOSTIC
─────────────────────────────
Genre detected:        Academic abstract (NLP/ML paper)
Register:              Formal academic, third-person/passive
Overall quality:       54/100
Voice consistency:     N/A

Strengths:
  ✓ Describes a study
  ✓ Has a finding
  ✓ Has an implication

Structural patterns to address:
  • Nominalization overload: "investigation", "relationship", "assumption", "utilization",
    "consideration", "implications" — 6 nominalizations in one paragraph
  • Present participial: "Leveraging a novel experimental framework"
  • Summary sentence at end restates the finding already stated mid-paragraph

Vocabulary signals:
  • "comprehensive investigation", "nuanced relationship", "invariably", "novel experimental
    framework", "competitive performance levels", "warranted"
  • "nuanced" appears twice in one abstract
  • "Furthermore, the implications of these findings are significant" — vague significance
    inflation with no specifics

CRITICAL ISSUE — Specificity:
  • "diverse NLP tasks" — which tasks?
  • "certain task-specific contexts" — which contexts?
  • "moderate complexity" — what does this mean? Parameter count? Layer count?
  • "limited in scope" — limited how? What threshold?
  • "comparable or superior performance metrics" — which metrics? By how much?

Note on register:
  This is an academic abstract. High nominalization is appropriate here.
  The issue is not nominalization per se — it is nominalization covering absent specifics.
  "A comprehensive investigation into the nuanced relationship" sounds like an abstract
  but conveys no more information than "We studied X".

Recommended intervention: Moderate — specificity (if available), vocabulary reduction,
  remove redundant summary ending. Do NOT over-casualize. This is academic writing.
```

---

### Output

---

Larger language models do not always outperform smaller ones. This paper tests that assumption across [specific tasks — e.g., named entity recognition, text classification, and question answering], varying model architectures systematically under constrained training conditions.

We find that models below [X] parameters match or exceed larger models on [specific tasks] when training data is below [N] examples. The gap closes further when [specific condition].

These results suggest that model selection should account for data availability and task type, not scale alone. [Specific implication for practitioners — e.g., a practitioner choosing between a 7B and 70B model for a domain-specific task with fewer than 10K training examples may find the smaller model competitive.]

---

### What Changed

**Preserved**:
- Academic register (no contractions, formal vocabulary, third-person reporting)
- The paper's actual finding (smaller models can match larger ones under data constraints)
- Passive voice where appropriate to the genre
- Structure (hypothesis → experiment → finding → implication)

**Removed**:
- "comprehensive investigation into the nuanced relationship" → "tests that assumption"
- "Leveraging a novel experimental framework" → described in plain terms what the experiment does
- "Furthermore, the implications of these findings are significant for practitioners" → removed inflation; replaced with actual implication
- Final summary sentence that restated the finding → the finding was already stated

**Flagged for author to supply**:
- The specific NLP tasks
- The parameter threshold
- The training data threshold
- The specific practitioners' implication

**Note**: An academic abstract with these specificity flags is better than one without them. The author knows what the specific tasks, thresholds, and results were — Not Ai does not, and will not invent them.
