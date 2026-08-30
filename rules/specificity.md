# Rules: Specificity

The most persistent quality gap between AI-generated prose and human writing is not vocabulary. It is **specificity**. LLMs generalize. Humans who know something specific say the specific thing.

---

## What Specificity Is

Specificity is the quality of referring to concrete, particular things rather than abstract categories. It manifests in:

- **Specific examples** instead of "for example, various methods exist"
- **Specific numbers** instead of "a significant portion"
- **Specific names** instead of "industry leaders"
- **Specific observations** instead of "many people have noted"
- **Specific consequences** instead of "this can have negative effects"
- **Specific time** instead of "in recent years"
- **Specific places** instead of "in many regions"

---

## How AI Generates Generic Text

LLMs are trained to produce text that is broadly applicable across many contexts. This creates a systematic bias toward generality:

- "This approach has been shown to improve outcomes" (whose outcomes? which approach? in which study?)
- "Organizations across various sectors have adopted this methodology" (which organizations? what methodology?)
- "The implications of this trend are significant" (what implications? significant how? for whom?)
- "Research suggests that..." (which research? who conducted it? when?)

This generalization is not malicious; it reflects the model's statistical tendencies. But it produces writing that reads as authoritative while conveying little actual information.

---

## The Specificity Test

For each claim, ask:
> "Could this sentence appear in an article about a completely different topic?"

If yes, it is generic. Generic sentences are candidates for improvement, **but only if evidence exists in the source text to make them specific**.

---

## Critical Rule: Evidence Must Already Exist

**Never invent specificity.**

If the source text says:
> "I attended the conference and learned a great deal."

Do not transform it into:
> "At the Tuesday morning session, I remember the speaker's point about distributed systems..."

Unless "Tuesday morning", "distributed systems" appear in the author's notes or context, you are inventing. This violates the core principle.

The correct action when specificity is missing and no evidence exists:
- **Flag** the generic statement in the diagnostic
- In `--mode preserve`: leave it unchanged
- In `--mode rewrite`: ask the author what specific detail they had in mind, or leave a placeholder: `[specific example here]`
- Never fabricate the detail

---

## Types of Generic Patterns to Flag

### Type 1: Inflated Significance
**Pattern**: Claims inflated beyond what the text demonstrates.

Examples:
- "This represents a paradigm shift in how we think about..."
- "This fundamentally transforms the landscape of..."
- "In an era of unprecedented change..."
- "This breakthrough has far-reaching implications..."

**The question to ask**: Does the surrounding text actually demonstrate this significance, or is this rhetorical inflation?

**Intervention**: If the evidence doesn't support the claim, soften it or remove it. If the evidence does support it, the sentence may be fine.

### Type 2: Vague Quantification
**Pattern**: Quantities without grounding.

Examples:
- "a significant number of users"
- "many experts agree"
- "studies have shown"
- "in recent years"
- "across multiple domains"
- "a growing body of evidence"

**Intervention**:
- If the source has a specific number, use it
- If no specific number exists, prefer the honest vague form ("some users", "a few studies") over the inflated form ("many", "numerous", "a growing body")
- Do not invent numbers

### Type 3: Anonymous Authority
**Pattern**: Citing unnamed authorities or vague consensus.

Examples:
- "experts say"
- "researchers have found"
- "studies indicate"
- "industry leaders note"
- "it is widely acknowledged that"

**Intervention**:
- If the source cites a specific person or study, ensure their name appears
- If no specific source exists in the text, use an honest hedge: "it is sometimes argued that" or remove the authority claim
- Do not fabricate specific names or citations

### Type 4: Abstract Summaries Without Evidence
**Pattern**: Drawing conclusions before presenting the evidence, or substituting summary for explanation.

Examples:
- "This demonstrates the power of collaborative approaches."
- "The results clearly illustrate the importance of careful planning."
- "This shows why innovation matters."

**Intervention**:
- If the preceding text contains actual evidence, the summary may be redundant; remove it
- If the preceding text does not contain the evidence the summary claims, flag it

### Type 5: Generic Examples
**Pattern**: Examples that aren't actually examples.

"For example, consider a situation where..." (no specific situation)
"This can be seen in fields such as technology, healthcare, and education." (naming categories, not examples)
"Various applications exist, including..." (then listing categories, not applications)

**Intervention**:
- Request or flag for actual examples
- If the source provides specific examples elsewhere, move them here
- Do not fabricate examples

### Type 6: Removed Concreteness
**Pattern**: AI rewrites sometimes abstract away specificity that existed in the original.

If the user's source says "I spent 11 months building this" and a previous AI rewrite produced "after a substantial development period", restore the original number.

Always check the source against the AI-generated text for **removed specificity**.

---

## Appropriate Generality

Not every general statement needs to be specific. Some situations call for generality:

- **Introductions** that frame a topic before diving into specifics
- **Conclusions** that draw general lessons from specific evidence
- **Abstracts** that summarize without repeating all detail
- **Audience-appropriate simplification** in writing for non-expert readers
- **Policy statements** that intentionally apply to broad contexts

The test: Is the generality serving the reader, or is it covering for absent knowledge?

---

## The Specificity Hierarchy

When improving a passage, prefer interventions in this order:

1. **Use a specific detail already in the source text**: always the first choice
2. **Use a specific detail from context the user has provided**: second choice
3. **Preserve the vague form with an honest hedge**: only when no specific detail exists
4. **Flag for the author to fill in**: in [bracket] form
5. **Remove the generic claim**: only when it adds no value even in general form

Never add specificity that has no basis in available evidence.
