# Observable signs of AI writing

A catalogue of surface features associated with machine-generated prose, adapted for general writing from the Wikipedia community's ongoing documentation of the problem (`Wikipedia:Signs of AI writing`, revision of 29 August 2026). Wikipedia editors review a very large volume of suspected machine text, which makes their list unusually empirical: entries earned their place by recurring across thousands of cases.

## How to use this file

**No single sign is proof.** Every item below appears in human writing. The catalogue exists to direct attention, not to deliver verdicts.

**Clusters carry the signal.** One canned phrase means little. A page with canned significance framing, a `Future Outlook` section, uniform paragraph shape and a broken citation is a different matter.

**Never state a conclusion about authorship.** This skill cannot establish who or what wrote a text, and neither can any tool it has access to. Report the patterns found and let the author decide what they mean. A diagnostic that says `this was written by ChatGPT` is wrong even when it happens to be correct, because the evidence does not support the claim.

**Markup artifacts are the exception.** A literal `oaicite` token or a `utm_source=chatgpt.com` parameter in a URL is not a stylistic impression. It is a residue of a specific interface, and it is close to conclusive that text passed through that interface. Everything else in this file is probabilistic.

### What detection tools are worth

Commercial classifiers report high accuracy on their own benchmarks and behave much worse on real text. Both error directions cause damage: false positives on human writing, and false negatives on lightly edited machine text. Non-native English writing draws false positives at elevated rates, which is a known and unresolved fairness problem.

Human judgment is also weaker than people expect, and more variable. Russell, Karpinska and Iyyer (2025) found that annotators who use language models heavily for their own writing reached roughly 90 percent accuracy, well above occasional users, which suggests the skill is acquired exposure rather than intuition. Work reported through the Wikipedia page as Fiedler and Döpke found untrained raters around 57 percent and trained raters around 64 percent, close enough to chance that an individual confident judgment should carry little weight. Full citations in `references/writing-research.md`.

A further complication compounds over time. Models were trained on human text and humans now read enormous quantities of model text, so vocabulary flows in both directions. Words documented as machine tells, `delve` being the standard example, have measurably risen in human speech and writing since 2023. The signals in this file will decay, and some already have.

---

## Content and framing

### Inflated significance

Text asserts that a subject matters, in general terms, rather than showing what it did. Common forms include claims about a lasting legacy, a place in a broader movement, an impact on a field, or a role in shaping something. The claim usually cannot be traced to any source in the text.

```
X has left a lasting impact on the field, reflecting broader trends
toward greater inclusivity and shaping the way future practitioners
would approach the discipline.
```

Repair: cut the claim, or replace it with the specific thing that happened.

### Canned emphasis on notability and coverage

Prose that argues for its subject's importance instead of describing it. Phrases that recur: `has garnered significant attention`, `has been widely recognised`, `received coverage in major outlets`, `is considered a leading figure`. Where a real source exists, name it. Where none does, the sentence is empty.

### Vague attribution

Authority invoked without a bearer. `Industry observers note`, `critics have argued`, `experts agree`, `it is widely believed`, `some have suggested`. The construction survives most editing passes because it contains no unusual vocabulary.

Repair: name the source, or downgrade the claim honestly to `some research suggests`, or cut it.

### Overgeneralised opinion

A judgment presented as consensus. `X is regarded as one of the most influential figures in the movement`, where the text supplies no evidence of regard.

### Superficial analysis via trailing participial phrase

A sentence states a fact, then appends an `-ing` clause that gestures at meaning without adding any:

```
The company opened three offices in 2021, reflecting its commitment
to growth and signalling a broader shift in the industry.
```

The tail is unfalsifiable and usually unsourced. It is also one of the more reliable structural tells, because it combines the participial-clause overuse measured in Reinhart et al. with the significance inflation above. Repair by deleting the tail. If the shift is real, it deserves its own sentence with evidence.

### Promotional register

Marketing language in text that should be neutral: `state-of-the-art`, `world-class`, `a must-see`, `unparalleled`, `stunning`, `rich cultural heritage`, `nestled in`. Travel and organisational descriptions attract this most.

### Challenges and outlook framing

Two closely related habits. A `faces challenges` paragraph that lists difficulties in the abstract, and a forward-looking closing section headed `Future Outlook`, `Looking Ahead`, `Challenges and Opportunities` or `Conclusion`, which speculates rather than reports.

These are outline artifacts. A model asked for a structured piece fills every slot in the structure, including slots the material does not support. In non-fiction that is not an essay, a `Future Outlook` heading is a strong signal on its own.

### Awards, recognition and legacy sections

Sections with these headings that contain no specific award, date or citation, existing because the outline called for them.

### Leads that mistake a description for a title

Where a piece is titled with a descriptive phrase, model output often opens by treating that phrase as a proper name:

```
The 2019 Regional Transport Review was a review of regional transport
conducted in 2019.
```

The sentence defines the title rather than introducing the subject.

---

## Language and grammar

### Copula avoidance

Instead of `is`, `are`, `was` or `has`, model output reaches for a heavier substitute: `serves as`, `stands as`, `functions as`, `represents`, `constitutes`, `embodies`, `boasts`, `features`, `refers to`, `is characterised by`.

```
The library serves as a resource for researchers and boasts a
collection of over 40,000 volumes.
```

Becomes: `The library holds over 40,000 volumes and is open to researchers.`

`Boasts` and `stands as` are the sharpest, since neutral human prose rarely uses either.

### Vague expression of connection

Two things are linked without the link being specified: `is closely tied to`, `is deeply connected with`, `is intertwined with`, `reflects`, `resonates with`, `speaks to`, `is emblematic of`, `aligns with`.

Repair: state the actual relationship, or drop it. Where the source does not establish a relationship, asserting one is fabrication.

### Negative parallelism

Three forms, all frequent:

```
It is not just a tool, it is a way of working.
Not a failure, but a redirection.
The design prioritises clarity rather than decoration.
```

The first two are the classic shapes. The third, `X rather than Y` used for emphasis where no genuine contrast exists, has been noted particularly in Grok output.

What makes this pattern worth its own entry: it contains no flagged vocabulary, so word-substitution humanizers leave it completely intact. The negated half is nearly always a position nobody held, inserted to give the affirmed half something to push against.

Repair: state the affirmative claim and delete the setup.

### Rule of three

Three parallel items where the third exists for cadence rather than content. Also three-part sentence rhythms and three-item section structures. Human writers use tricolons deliberately and sparingly; model output produces them by default.

### Uniform paragraph shape

Every paragraph opens with a claim, supplies two or three supports, closes with a restatement. The individual paragraph reads fine, which is why this survives review. The uniformity across a whole document is the tell.

---

## Style and formatting

### Em dash overuse

Long treated as the single most recognisable typographic signal, and now the most complicated entry in this file.

The pattern to look for is the paired em dash used as parenthetical framing:

> That gap — fluency without judgment — is where the work is.

Two in one sentence, setting off an aside, is the shape worth flagging. A single em dash used as a break is ordinary English punctuation that many strong writers favour.

Two developments matter. Measurement through mid-2026 found that among current models only Claude exceeds professional human writers in em dash frequency, while ChatGPT now uses them at a lower rate than it did, apparently in response to user complaint. GPT-5.1 suppresses them further. So em dash frequency is becoming a weaker signal, and in some comparisons it now points the wrong way.

Treat frequency as suggestive at best. Treat the paired parenthetical construction as the durable part of the signal. Do not treat any em dash as evidence on its own, and be aware that plenty of human writers, including editors and novelists, use them heavily by preference.

### Curly quotation marks and apostrophes

Typographic quotes (`"` `"` `'`) and apostrophes where a plain keyboard would produce straight ones. Worth noting only with several caveats, because the legitimate sources are numerous: Microsoft Word and Google Docs autocorrect to curly quotes by default, iOS and macOS do the same, many publishing systems substitute them, and material pasted from a professionally typeset source carries them. Curly quotes on their own mean nothing. Curly quotes appearing suddenly in a document that otherwise uses straight ones are worth a look.

### Heading and emphasis habits

Several related formatting tells:

- Headings in Title Case where the surrounding document uses sentence case
- Headings that restate the document title
- Headings with no content beneath them, or a single sentence
- Bold used for emphasis throughout body text rather than for defined terms
- Vertical lists where each item begins with a bolded inline header followed by a colon
- Skipped heading levels, for example a level 2 followed by a level 4
- Repeated level 1 headings inside a document that already has a title
- Horizontal rules between every section

The bolded-inline-header list deserves attention because it is so common in model output and so rare in human drafting. It appears when a model converts an outline into prose without collapsing the outline.

### Emoji as structure

Emoji used as section markers or bullet substitutes, particularly a check mark, a rocket, a warning sign or a pointing finger introducing each item in a list. Distinct from ordinary conversational emoji use.

### Tables that do not need to be tables

Two-column tables holding prose that would read better as sentences, or tables with a single row, or tables whose columns are `Aspect` and `Description`.

---

## Leaked interface artifacts

The strongest evidence in this file, because these are residues rather than impressions.

### Text addressed to the user

Output that still contains the model talking to whoever prompted it:

```
Certainly! Here is the revised section you requested.
I hope this helps! Let me know if you would like me to expand any part.
Would you like me to continue with the next section?
As an AI language model, I cannot verify this claim.
```

Also self-referential framing (`In this section, we will explore`), and offers to do more work.

### Knowledge cutoff and source disclaimers

```
As of my last update, the situation may have changed.
Based on the information available to me, ...
I could not find specific details about this in my sources.
Please verify this information independently.
```

### Speculation about missing information

Text that reasons aloud about gaps in its own sources rather than reporting facts: `it is unclear from the available information whether`, `details on this period are limited`, `no further information could be located`.

### Unfilled placeholders

Template scaffolding the author never completed:

```
[Insert date here]        [Add citation]         [Your name]
[Company Name]           [specific detail]       Accessed 2025-xx-xx
```

The `2025-xx-xx` access-date form is a documented recurring case, produced when a model generates a citation template and has no real date to fill in.

### Markdown surviving into a non-Markdown context

`**bold**`, `##` headings, or `- ` bullets pasted into a system that does not render Markdown, such as wikitext, a rich-text editor or a plain-text field. Also the reverse: broken markup where a model attempted a syntax it had partly memorised.

### Vendor-specific tokens

Literal strings that identify the interface a text passed through. Search for these directly; they are unambiguous.

| Source | Artifacts |
|---|---|
| ChatGPT | `contentReference`, `oaicite`, `oai_citation`, `turn0search0`, `turn0image0`, `attributableIndex` JSON fragments, `utm_source=chatgpt.com`, `utm_source=openai` |
| Gemini | `[cite: 1]`, `[span_1](start_span)`, similar span and cite wrappers |
| Grok | `grok_card`, `grok_render_citation_card_json`, `referrer=grok.com` |
| DeepSeek | Lenticular bracket citations such as `【85†L261-269】` |
| Perplexity | `[attached_file:1]`, `[web:1]`, `ppl-ai-file-upload` |
| Copilot | `utm_source=copilot.com` |
| Unclassified | `:::writing{variant="document" id=...}` |

A `utm_source` parameter naming a chat product inside a link is worth a note of its own: it means the link was copied out of that product's interface, which is not the same as the surrounding prose being machine-written, but it establishes that the interface was in the loop.

### Invented structures

References to categories, templates, tags or internal identifiers that do not exist in the target system. A model asked to format for an unfamiliar platform produces plausible names for things that were never created.

---

## Citation and sourcing failures

Machine-generated citations are frequently well-formed and wrong, which makes them more dangerous than obviously broken ones. Look for:

- Links that resolve to nothing, or to an unrelated page
- DOIs and ISBNs that are syntactically valid and do not exist
- A DOI that resolves to a real article with a different title and different authors from the one cited
- Book citations with no page numbers, or with page numbers outside the book's length
- Author names attached to work they did not produce
- Journal, volume and issue combinations that do not exist
- A stray `↩` character, left over from a footnote back-link in rendered output
- Named references declared and never used
- Real sources cited for claims they do not contain

The last is the hardest to catch and the most common. A citation that exists, is correctly formatted, and does not support the sentence attached to it will pass every automated check.

Any citation in text suspected of machine generation needs checking against the source itself. Format tells you nothing.

---

## Signals in collaborative and editing contexts

Relevant where text arrives through a review process rather than as a finished document.

**Style discontinuity.** A document whose register, sentence length and vocabulary shift abruptly partway through, particularly where the new section is more fluent and less specific than what surrounds it.

**Commentary that describes rather than argues.** Review comments that summarise a position at length, cover every side evenly, and commit to nothing.

**Formulaic process notes.** Summaries of one's own changes that read as generated: uniformly structured, describing intent in general terms, sometimes at odds with what actually changed.

**Prematurely applied boilerplate.** Maintenance notices, disclaimers or process templates added to a document before the condition they describe exists, because the model knew such templates exist.

**Generic self-description.** Profile and biography text assembled from stock phrases with no verifiable specifics.

**Volume mismatch.** Output arriving faster or in greater quantity than the apparent effort supports.

---

## Ineffective indicators

Things widely believed to indicate machine authorship that do not. Acting on these produces false accusations, and false accusations against a human writer are the worst failure mode this skill has.

**Perfect spelling, grammar and punctuation.** Careful writers, professional editors and anyone using a spell checker produce clean text. Cleanliness is not a tell.

**Any single flagged word.** `Delve`, `tapestry`, `intricate`, `underscore` and the rest are real words with real uses, and their frequency in human writing has risen since 2023 through ordinary exposure. Frequency and clustering carry information. A single occurrence does not.

**Formal or elevated register.** Some people write formally. Some subjects require it. Non-native English speakers often write in a more formal register than native speakers, and are already over-flagged by every automated detector.

**Long sentences, or short ones.** Neither length indicates anything by itself.

**Bulleted lists and headings.** Structural formatting is normal in documentation, reports and reference material.

**Curly quotes and other typographic punctuation** by themselves, given how many editors and platforms insert them automatically.

**A detector score.** Classifier output is not evidence. It should not appear in a diagnostic, and it should never be cited to a person as a reason to doubt their work.

**Em dashes alone.** Covered above. The signal is weakening, some models now use fewer than professional writers, and many human writers use them heavily by choice.

**An author denying or confirming it.** Neither settles anything, and asking turns a writing review into an interrogation.

**Confident factual errors.** Humans produce these in quantity. Models produce a characteristic kind, plausible and specific and wrong, but the category itself is shared.

---

## Signs of human writing

The counterweight. These features are difficult for a model to produce because they require access to something outside the text, and their presence should lower suspicion.

**Specific unglamorous detail.** A room number, a bus route, the name of a colleague, the price of a part, the exact wording on a sign. Model output supplies categories where humans supply particulars.

**Verifiable, checkable specifics.** Dates, figures and quotations that hold up when checked, especially where they are obscure enough that inventing them would be pointless.

**Idiosyncratic and asymmetric structure.** Sections of wildly different length. A subject the author clearly cares about, treated at four times the length of an equally important one. Machine output distributes attention evenly.

**Local or tacit knowledge.** Facts that come from having been present, and that no source states directly.

**Genuine and calibrated uncertainty.** `I am not sure this is right`, `as far as I can tell`, `I could not work out why`. Human experts hedge where they are actually uncertain, and models hedge uniformly or not at all.

**Opinion with a position.** A stance taken and defended, rather than a survey of views.

**Unevenness.** A strong opening and a weak middle. A paragraph that is clearly a first draft next to one that has been reworked. Uniform polish across a long document is itself worth noticing.

**Humour, particularly the kind that risks failing.** Jokes that depend on shared context, dry asides, an aside that does not quite land.

**Ordinary error.** A typo, a misremembered detail, an inconsistent spelling of a name.

None of this justifies adding these features to make text look human. Inserting a fake typo or a manufactured uncertainty is a fabrication and this skill does not do it. The list is here for reading, not for writing.

---

## Source and status

Adapted from `Wikipedia:Signs of AI writing` as of 29 August 2026, with structural findings cross-referenced against `references/style-research.md`.

That page is maintained by editors who assess suspected machine text at high volume, and it changes frequently as model behaviour changes. Anything in this file may be out of date, and the em dash entry is the clearest example of a signal that has already shifted within a year. Check the current revision before relying on any single entry.
