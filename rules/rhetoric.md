# Rules: Rhetoric

Rhetoric is how writing positions itself in relation to its reader: how it argues, acknowledges uncertainty, engages, and signals the author's attitude. Research comparing LLM and human writing finds systematic rhetorical differences that are more diagnostic than vocabulary choices.

---

## Research Basis

From Jiang & Hyland (2025), comparing GPT-4 to student essays:
- LLM essays show "significantly lower frequency of interactional metadiscourse, such as hedges, boosters, and attitude markers, leading to a more impersonal and expository tone"
- Student essays demonstrate "higher rhetorical engagement, employing nuanced stance markers and personalised expressions to foster reader interaction"
- LLMs exhibit "fewer engagement markers, particularly questions and personal asides"
- LLM "bundles are more rigid and formulaic": noun and preposition-based, rather than epistemic stance markers

From Reinhart et al. (PNAS 2025):
- LLMs have measurably different rates of hedging phrases, phrasal coordination, and clausal coordination
- These patterns persist across genres; LLMs fail to adapt their rhetorical register to fiction, blogs, or conversation the way humans do

---

## Rhetorical Dimension 1: Epistemic Stance (Hedging and Certainty)

**What it is**: Epistemic stance markers indicate the writer's degree of confidence in a claim.

**Hedges** (soften commitment): might, could, may, perhaps, possibly, appears to, seems to, tends to, I think, one could argue, arguably, in many cases, it seems that, evidence suggests

**Boosters** (strengthen commitment): clearly, obviously, certainly, definitely, it is evident that, undoubtedly, without question, it is clear that

**How AI differs**:
- Instruction-tuned LLMs often drop hedges in favor of assertive declarations
- They also overuse certain hedge phrases at formulaic insertion points: "It's worth noting that", "It is important to mention", "It should be noted that"
- The natural human calibration, hedging where genuinely uncertain and asserting where confident, is replaced by a flat assertive tone with ceremonial hedge phrases dropped in periodically

**How to improve**:
- If a claim is genuinely uncertain, ensure the hedge is genuine (not formulaic): "It seems that" instead of "It is clear that"; "evidence suggests" instead of "evidence proves"
- Remove ceremonial hedges that don't soften anything: "It is worth noting that the sky is blue" → "The sky is blue" or cut it
- Restore certainty markers where the author is making a strong, well-supported claim
- Do not reduce all assertions to hedges; that is its own error

### Recognizing False Hedges

A false hedge is a hedge phrase that precedes a maximally certain claim:
- "It is worth noting that this represents a fundamental transformation..." (the hedge adds nothing; the claim is absolute)
- "Importantly, it should be recognized that this is clearly the best approach..." (hedging a certainty)

Remove the hedge phrase or soften the underlying claim, but not both.

---

## Rhetorical Dimension 2: Engagement Markers

**What it is**: Engagement markers invite the reader into the text: questions, direct address, anticipating objections, and acknowledgment that the reader has a perspective.

**Types**:
- **Questions**: "Why does this matter?" / "What does this mean in practice?"
- **Direct reader address**: "you'll notice", "consider your own experience", "if you've worked with..."
- **Inclusive 'we'**: "We can see that...", "Let's examine..."
- **Anticipating objections**: "One might argue that..." / "Critics have suggested..." / "A reasonable objection is..."
- **Personal asides**: "(I should mention...)", "for what it's worth"

**How AI differs**: LLMs produce engagement markers at significantly lower rates than humans in essay and argumentative writing. The result feels authoritative but impersonal, like a textbook rather than a conversation.

**How to improve**:
- Check whether the text ever directly acknowledges the reader
- If the genre permits (essay, blog, email, social media), add one or two engagement markers naturally
- Do NOT add engagement markers to genres where they are inappropriate: technical documentation, academic abstracts, formal reports
- Do NOT add forced questions to seem more human: "So, what's the takeaway?" is a humanizer cliché

---

## Rhetorical Dimension 3: Attitude Markers

**What it is**: Attitude markers convey the author's emotional or evaluative stance toward the content.

Examples: unfortunately, surprisingly, remarkably, disappointingly, crucially, importantly, interestingly, thankfully

**How AI differs**: LLMs use attitude markers, but often use them at high frequency in a way that feels evaluative without genuine feeling. "Importantly, this represents...", "Crucially, the system...", "Remarkably, results showed...": these become verbal tics that don't reflect genuine authorial judgment.

**How to improve**:
- Keep attitude markers that reflect the author's genuine position
- Remove attitude markers that function as rhetorical throat-clearing: "Importantly, X happened" → "X happened"
- If an attitude marker is present, ask: does the surrounding text support this attitude? If "remarkably" is used, is the thing actually remarkable in context?

---

## Rhetorical Dimension 4: Formulaic Transition Patterns

**What it is**: Transition phrases that indicate logical relationships between sentences or paragraphs.

**Common AI transition overuse**:
- "Furthermore," / "Moreover," / "Additionally,": used between sentences that don't require a formal bridge
- "On the other hand,": used without a genuine contrast preceding it
- "In addition to the above,": usually redundant
- "As a result," / "Consequently," / "Therefore,": overused even when causation is already clear from content
- "In conclusion," / "To summarize," / "In summary,": often redundant when the conclusion is obvious

**How AI differs**: LLMs have higher rates of explicit transition markers because they signal structure clearly, a behavior reinforced by RLHF feedback rewarding "well-organized" text. But human writers rely more on **implicit logical flow**, using transitions only when genuinely needed.

**How to improve**:
- If two sentences have a clear logical relationship without a transition, remove the transition
- If the transition names a relationship that isn't there (e.g., "Therefore," before a sentence that isn't a conclusion), either remove it or rewrite to create the actual relationship
- Reserve formal transitions for cases where the reader would otherwise miss the logical move

---

## Rhetorical Dimension 5: Repetitive Summaries

**What it is**: Ending a section or argument with a sentence that restates what was just said.

Common pattern:
> [Three paragraphs explaining X] → "In summary, X is important because [restate everything just said]."

**How AI differs**: LLMs are strongly trained to "conclude" and "summarize"; this pattern is reinforced by RLHF. The result is redundant summary sentences at the end of nearly every section.

**How to identify**: After reading a section, ask: "Does the final sentence add anything, or does it restate the previous sentences?" If restating, it's a candidate for removal.

**How to improve**:
- Remove the restatement if the content already made the point clearly
- If a summary is genuinely needed (long complex argument), make it add new value rather than restate: a consequence, a question, a forward-looking statement

---

## Rhetorical Dimension 6: The Tricolon Habit

**What it is**: A tricolon is a set of three parallel items: "X, Y, and Z." LLMs use tricolons compulsively because they feel balanced, complete, and literary.

**Problem**: Tricolons used for everything feel mechanical. Not every idea comes in threes. Sometimes two items is the right number. Sometimes four. Sometimes one.

**How to detect**: Count three-item lists in prose. More than one per paragraph is elevated.

**How to improve**:
- If you have three items and the third adds genuine value, keep it
- If the third item was added to reach three, remove it
- If you have four genuine items, use four; don't cut one to reach three
- Sometimes a two-item contrast ("X, not Y") is sharper than a tricolon

**Not a problem**: Tricolons in contexts where three genuinely is the right number. This is about compulsive use, not the pattern itself.

---

## Rhetorical Dimension 7: Negative Parallelism

**What it is**: A pattern of stating what something is not, often as a rhetorical setup: "Not X. Not Y. But Z."

**How AI uses it**: This pattern appears frequently in AI-generated motivational and professional writing. It has a rhetorical energy that LLMs learned from persuasive human writing, but its compulsive use is now recognizable.

**When to keep it**: When the contrast genuinely sharpens the argument and the author's voice uses it.

**When to remove it**: When it feels added for drama rather than serving a real rhetorical purpose.

---

## Rhetorical Dimension 8: Authorial Presence

**What it is**: The degree to which the author's own perspective, judgment, and experience are visible in the text, as opposed to purely reporting facts and arguments.

**How AI differs**: LLMs produce "expository tone": informational, organized, but detached. The author's presence is minimal.

**How to improve**:
- Only if the author's voice permits (check voice profile)
- In genres that benefit from authorial presence (essays, opinion pieces, personal writing), ensure the author's actual view appears, not just a neutral presentation of multiple views
- Do NOT invent an opinion; only restore or sharpen one that is present in the source but was smoothed away

---

## When Not to Change Rhetoric

Some genres deliberately minimize rhetorical engagement, hedging, and attitude markers:
- Legal documents
- Medical/scientific abstracts  
- Technical reference documentation
- News reporting
- Terms of service / policy documents

In these contexts, the apparent "lack of engagement" is a feature of the genre, not a deficiency. Do not impose engagement markers or attitude markers on writing that is correctly impersonal.
