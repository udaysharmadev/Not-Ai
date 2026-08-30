# Rules: Context

Writing that is natural in one context is inappropriate in another. Not Ai must infer or ask about context before applying any intervention. The same text processed without context awareness will produce wrong results.

---

## Context Dimensions

### Dimension 1: Genre

Genre is the category of document being written. Genre shapes:
- Expected level of formality
- Expected sentence length and complexity
- Expected use of engagement markers, hedging, first-person
- Expected tone and register
- Whether creativity and variation are valued or whether consistency is required

### Dimension 2: Audience

Who is reading this? Consider:
- **Expertise level**: Expert in the subject / informed non-expert / general public / complete novice
- **Relationship**: Colleague / employer / client / friend / stranger / professional community
- **Purpose of reading**: To learn / to make a decision / to be entertained / to evaluate / to be persuaded

### Dimension 3: Publication Context

Where will this appear?
- Private: email, direct message, internal document
- Semi-public: team communication, shared document, internal wiki
- Public: website, social media, published article, open-source README

Publication context affects what is appropriate to say, how directly to say it, and what expectations the reader brings.

### Dimension 4: Relationship Between Writer and Reader

Formal or informal? First contact or ongoing relationship? Peer or hierarchical? This affects register choices more than genre alone.

---

## Genre Profiles

Load the appropriate profile based on detected or stated genre.

---

### LinkedIn Post

**Typical characteristics**:
- First person, professional but personable
- Short paragraphs (2–4 sentences), often with single-sentence paragraphs for visual separation
- Hook opening (observation, question, or statement of the counterintuitive)
- Moderate engagement markers (reader address, questions)
- Ends with insight, question, or invitation to respond
- No em-dashes overload; some bullets acceptable; no academic citations
- Informal formality: level 2–3

**AI patterns to address in LinkedIn**:
- Generic "In today's fast-paced world..." openings → cut
- Excessive bullet lists → reduce to prose where natural
- Tricolon endings: "What have you noticed? Drop it in the comments. I'd love to hear." → genuine versions fine; formulaic versions → revise
- Inspirational platitudes without specific content → flag
- Excessive nominal openings

**Red lines**:
- Do not make it casual slang if the author's voice is professional
- Do not add hashtags unless author provided them

---

### GitHub README

**Typical characteristics**:
- Technical, precise, imperative
- Short clear sentences
- Code blocks, bullet lists are expected and appropriate
- Minimal first-person (unless project is personal)
- No hedging — the code either does or does not do something
- Formality: level 4

**AI patterns to address in README**:
- Inflated significance: "revolutionizes how developers" → "helps developers"
- Vague feature descriptions: "powerful functionality" → specific features
- Marketing-style opening paragraphs → factual project description
- Generic "comprehensive" / "robust" / "seamless" → specific claims

**Red lines**:
- Do not informalize technical documentation
- Do not remove precision for "naturalness"

---

### Academic Abstract

**Typical characteristics**:
- Third person or passive, dense, precise
- High nominalization is appropriate
- No engagement markers, no personal asides
- Every sentence carries information — no filler
- Formality: level 5

**AI patterns to address in academic abstracts**:
- Inflated significance: "This paper represents a landmark contribution" → "This paper presents/demonstrates/analyzes..."
- Vague methodology descriptions → specific method names
- Repetitive summary at the end (abstract already is a summary — do not summarize it again)
- Over-hedged conclusions: "Our results may perhaps suggest the possibility that..." → "Our results suggest that..."

**Red lines**:
- Do not add engagement markers — they don't belong here
- Do not reduce information density — it is appropriate here
- Do not convert passive to active if the field convention uses passive

---

### Personal Essay

**Typical characteristics**:
- First person, reflective, specific
- Voice and point of view are the primary value
- Specific personal details, observations, and experiences
- Sentence length varies widely — both very short and very long acceptable
- Rhetorical questions, reader address, personal asides all appropriate
- Formality: level 1–3

**AI patterns to address in personal essays**:
- Generalization replacing personal observation: "Many people feel..." → "I noticed..."
- Inflated significance without personal grounding → cut or ground it
- Abstract conclusions without the experience that earned them → flag
- Manufactured emotion (describing feelings not evidenced in the text) → remove

**Red lines**:
- NEVER invent personal experiences, emotions, or observations
- Do not sanitize distinctive personal voice into generic "human" voice
- Do not add inspirational endings if the author did not write one

---

### Professional Email

**Typical characteristics**:
- Varies widely by relationship and purpose
- Generally shorter than formal reports
- Clear opening statement of purpose
- Direct request or call to action
- Often conversational but professionally appropriate
- Formality: level 2–4 depending on relationship

**AI patterns to address in email**:
- Ceremonial opening: "I hope this email finds you well." → cut unless genuine
- Excessive hedge phrases: "I was wondering if perhaps it might be possible..." → "Could you..." or "I'd like to..."
- Over-formal closing: "Please do not hesitate to reach out" → "Feel free to reach out" or "Let me know"
- Padding: "As I mentioned in my previous correspondence..." → get to the point

**Red lines**:
- Match the existing relationship's tone — don't casualize a formal relationship
- Preserve important qualifications and caveats in professional communication

---

### Technical Documentation

**Typical characteristics**:
- Task-oriented, accurate, clear
- Second person ("you") common in tutorials; third person in reference
- Numbered lists, code examples, warnings appropriate
- Minimal hedging — either the feature works or it doesn't
- Formality: level 3–4

**AI patterns to address in technical docs**:
- Vague feature claims: "intelligent", "smart", "powerful" → specific capability descriptions
- Generic introductions: "In today's digital landscape..." → "This document explains..."
- Missing prerequisites and limitations — AI often only describes the happy path

**Red lines**:
- Do not reduce accuracy for "flow"
- Preserve all warnings, limitations, and edge cases

---

### Social Media (Twitter/X, Mastodon, short-form)

**Typical characteristics**:
- Very short
- High information per word
- Fragments, abbreviations acceptable
- Humor, irony, opinions all common
- Formality: level 1–2

**AI patterns to address in social media**:
- Excessive formality → simplify
- Long clausal sentences → break up or cut
- Generic takes → sharpen to specific observation

**Red lines**:
- Do not impose professional formality
- Do not add caveats that destroy the point

---

### Story / Narrative Writing

**Typical characteristics**:
- Shows rather than tells
- Specific sensory details
- Character perspective and voice
- Sentence rhythm mirrors scene tempo
- Formality: highly variable

**AI patterns to address in narratives**:
- Telling emotions instead of showing: "She felt devastated" → action/gesture/detail
- Abstract narrative summary: "Events unfolded rapidly" → show the events
- Flat event escalation (every scene has the same emotional weight) — from StoryScope research
- Over-explained themes: "This illustrates the theme of loss." → remove
- Single-track plots without moral ambiguity — flag for revision

**Red lines**:
- Do not invent plot events, dialogue, or character details
- Do not impose a tidy resolution if the author hasn't written one

---

## When Genre Is Unclear

If genre cannot be inferred from content and context, state the assumption in the diagnostic:
> "Genre assumed: professional email (please correct if wrong)"

Do not apply a genre profile without acknowledging the assumption.

## Multi-Genre Documents

Some documents mix genres: a README with a personal story in the intro, a LinkedIn post with technical content. Handle each section according to its sub-genre.

---

## The Key Principle

Context-appropriate humanization is **not the same intervention for every text**.

A LinkedIn post that reads like an academic abstract is a failure of genre. An academic abstract that reads like a LinkedIn post is a different failure. Not Ai must address both — which means different interventions for different contexts, not a single humanization template applied universally.
