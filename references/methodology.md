# Not Ai: design methodology

Why the skill is built this way, what has already been tried by others, and what it cannot do. Read this before proposing a rule.

## The problem

Text produced by an instruction-tuned language model carries a measurable stylistic signature. The signature is not a set of words. It is a distribution over clause types, information density, cadence and stance, and Reinhart et al. measured it directly across parallel human and model corpora using Biber's 66-feature tagset. Full figures are in `references/style-research.md`.

The practical consequence is prose that reads as produced rather than composed: generic where it should be specific, confident without evidence, smooth without a person in it, organised without an argument. None of this is a moral failing of the text. It is a communication failure. The writing is less effective at reaching a particular reader for a particular purpose.

The goal of this skill is not to conceal that a model was involved. It is to remove the generic habits and restore what authorship supplies: specificity, judgment, register, and the author's own voice.

## What has been tried, and where each approach stops

**Word blacklisting.** Find the flagged terms, `delve`, `leverage`, `furthermore`, `comprehensive`, and substitute.

The word is not the problem. `Delve` is not incorrect. `Leverage` is the right word in a finance context. What the research measures is a co-occurrence: elevated participial clause rate together with elevated nominalization, uniform cadence, and absent epistemic hedging. Remove the words and the morphosyntactic profile is unchanged, because none of the six features that separate the distributions is lexical. Removing someone's cologne does not change their gait.

`examples/personal-essay/` shows the failure quantitatively. The vocabulary scanner finds two flagged terms in a 213-word generated essay, fewer than in any other input here except the human paragraph. It misses `embarked`, `journey`, `acculturation` and `unparalleled` because the list is tuned to a different register. The tells in that draft were a nominalization rate of 84.5 and a grade level of 15.0 on a first-person essay about renting a flat.

**Paraphrase rewriting.** Send the text back through a model with an instruction to reword it. This is what most commercial humanizers do.

Four problems. Claims, qualifications and specifics drift under paraphrase, so the text no longer says what it said. The output sounds like a person and no longer sounds like the author. Every paraphrase tool trained on similar feedback converges on the same corrective register, which is itself now a recognisable pattern. And the underlying clause distributions do not improve, because the paraphrasing model's own defaults are the distribution the problem came from.

**Surface variation injection.** Add fragments. Break long sentences. Insert contractions and slang. Vary punctuation.

Human writing is not defined by imperfection, and deliberately introduced roughness produces a caricature rather than a person. `examples/already-natural/` reproduces one of these outputs against a human original: the specifics survive, buried under performed enthusiasm the original writer plainly does not feel. This approach also makes the writing worse, which is never the goal.

**Fixed voice templates.** Offer three to five presets, `casual`, `professional`, `academic`, and apply the selected one.

`Casual` and `professional` are register targets, not voices. Two professional writers in the same field have entirely different professional voices, and a preset captures neither. The result replaces one generic pattern with another.

## Eight design principles

**1. Operate structurally, not lexically.** The signals the skill measures and acts on are clause type, nominalization density, information density, engagement markers, epistemic stance, paragraph shape and length distribution. Vocabulary is handled last, on the argument that a word swap inside a badly built sentence changes nothing a reader notices.

Exact figures, from Reinhart et al. and measured with a dependency parse:

| Feature | Human rate per 1,000 tokens | Instruction-tuned models |
|---|---|---|
| Present participial clauses | 1.7 | 224% to 527% of human |
| `that` clause as subject | 2.1 | 263% to 331% |
| Past participial clauses | see note | 273% to 307% |
| Nominalizations | 14.6 | 209% to 214% |
| Agentless passives | see note | 51% to 53% for the GPT models |
| Hedges | see note | 50% to 63% |
| Existential `there` | see note | 59% to 71% |

Four human rates are left out rather than filled with a plausible number. `references/style-research.md` carries the relative figure for past participial clauses, agentless passives, hedges and existential `there` because that is what was taken from the source; the absolute rates were not, and inventing them here would breach principle 7 in a file arguing for it.

Note the direction of the last three. Instruction-tuned models do not simply add features; they also avoid features that style guides discourage, more consistently than humans do. This is why blanket passive-to-active conversion moves text away from the human distribution rather than toward it.

**2. Deterministic measurement precedes reasoning.** The scripts run before any rewriting, so the diagnostic is a set of counts rather than an impression, the reasoning does not have to guess at frequencies, and any figure in the output can be reproduced by rerunning one command.

**3. Voice is a constraint, not a finishing pass.** When a sample is supplied, the profile bounds every rewrite decision: sentence length distribution, formality, punctuation habits. Where the sample uses no semicolons, the rewrite introduces none. Without a sample the skill rewrites neutrally and records `Voice profile: insufficient signal` rather than imposing a voice it cannot justify.

**4. Genre conditions everything.** The same measurement means opposite things in different genres, and this is not a hedge. `examples/academic-abstract/` and `examples/technical-passage/` both arrive at Stage 2 with nominalization flagged high. In the technical passage the correct response took it from 95.4 to 17.3. In the abstract the correct response was to take it from 92.9 to 83.3 and leave it flagged, because academic abstracts nominalize by convention and lowering the figure further would mean writing a worse abstract.

`examples/linkedin-post/` completes the picture from the other side. Its Gunning Fog index is 21.2 and that is a finding, because the audience is a scrolling feed. The abstract in this set reads 24.6 and the fog index is not what is wrong with it, because the audience is a reviewer. Neither number can be read without the genre.

**5. Human writing is a distribution, not a target.** Human prose varies enormously across individuals, genres, registers and languages. The goal is output that could plausibly exist somewhere in that space, not convergence on a single humanized style. Convergence is what produces the recognisable humanizer accent.

**6. Selective edits over wholesale rewriting.** The permitted actions are `KEEP`, `RESTRUCTURE`, `REPLACE`, `REMOVE`, `MERGE`, `SPLIT`, `MOVE` and `FLAG`. Rewriting everything is not among them, and `KEEP` should be the most frequent action in most texts. Over-editing is a failure mode of the same order as under-editing: it discards the author's phrasing that was already working.

**7. Never invent.** Where a specific detail would strengthen a sentence and is absent from the source, the skill writes `[specific detail here]` and leaves it. It does not supply facts, numbers, sources, anecdotes, emotions or dialogue.

This principle is load-bearing and it is under constant pressure. `examples/gen-ai-article/` records what an earlier version of this repository shipped as a correct output: a well-paced, specific, readable paragraph in which every specific was invented, generated from an input containing no facts at all. It reads better than the source and it attributes claims to an author who never made them. That is a worse outcome than a vague paragraph, because vagueness is visible and confident fabrication is not.

`examples/personal-essay/` documents the same pressure in a milder form, two inferred passages declared as additions in a 255-word rewrite, and states plainly that a draft this empty pushes any rewrite toward invention.

**8. Self-review before output.** Eight questions, listed in full in `SKILL.md`, covering what still reads as generic, where the rewrite over-edited, whether anything was invented, whether the author's position moved, whether the polish is suspiciously even, whether the voice survived, whether the genre rules were the right ones, and whether the change list matches the changes actually made.

The eighth question exists because of a specific failure in this repository's own history: a rationale that claimed to have removed three em dashes while the output it shipped still contained two.

## What this skill does not claim

It does not claim that a text is human, that it will pass a detector, that it cannot be detected, or any bypass rate. Those claims are indefensible. Detection systems change, models change, and no measurement here establishes authorship.

It also does not produce a score. An earlier version of `scripts/metrics.py` exposed a `compute_quality_score()` function; it was removed rather than improved. A single number invites an agent to optimise it, and `examples/already-natural/` shows exactly what optimising it costs: to raise burstiness on a human paragraph an agent must invent a fact, and to lower nominalization it must delete the term `race condition`, which is the phrase another engineer would search for. Both edits improve a number and damage the writing.

The honest claim is narrower and checkable: meaning preserved, voice preserved, structural features moved in a stated direction, generic patterns named with quotations.

## How this differs from existing tools

| Dimension | Typical humanizer | Not Ai |
|---|---|---|
| Intervention level | Lexical | Clause structure and density |
| Diagnostic | Absent or vague | Deterministic counts, with quotations |
| Voice model | Fixed presets | Profile extracted from a sample, or declared absent |
| Genre awareness | None | Eight explicit profiles in `rules/context.md` |
| Meaning preservation | Implicit | Number preservation in `benchmark.py`, plus a token-overlap figure that is labelled a proxy and shown to fail |
| Over-edit protection | None | Eight-question self-review, and `KEEP` as the default action |
| Fabrication prevention | None | Explicit prohibition plus a flag mechanism |
| Model of human writing | Single target | A distribution |
| Portability | Closed product | Plain files, any agent that reads context |
| Basis | Marketing claims | Published linguistics, cited per finding |

The row on meaning preservation deserves more than the caveat it carries. `benchmark.py` compares token overlap and checks that numerals survive. Run it on the six pairs in `examples/` and it flags `Major meaning drift` on five of them, including every rewrite this repository considers correct, while awarding its highest score, 65.5%, to `already-natural`, the one pair where the text was left alone. The ranking is inverted, and the cause is structural rather than a tuning error: token overlap rewards keeping the same words, and replacing abstract nouns with concrete verbs necessarily changes the words. The full table is in `benchmarks/README.md`. An embedding-based measure would fix it and is on the contributing list. Until then the figure means surface wording similarity and nothing more.

## Honest limits

**The scripts produce false positives on human writing, and this is demonstrated rather than hypothesised.** Run `analyze_structure.py` on `examples/already-natural/input.md`, 66 words a developer wrote about a production incident, and it raises two warnings: burstiness 0.200 flagged low, nominalization 45.5 flagged elevated. The correct intervention on that paragraph is none. The report prints six verdict lines on it and two of them are wrong.

**Burstiness does not do what its name suggests.** Across the six examples here, the human paragraph scores 0.200 and a generated LinkedIn post scores 0.799 with an explicit `Good length variation`. The post earns it on a segmentation artifact: its listicle is held together by a colon and three bolded lead-ins, so 69 words never split, and that one block against a 7-word engagement question produces the spread. The measure fell in three of the five rewrites and rose in two, while the writing improved in all five. `benchmark.py` compounds this by attaching a direction to the delta: it labels `already-natural` `improved (+0.345)`, a pair where not one word of the paragraph changed, and labels two good rewrites `worsened`, so its verdict is wrong on three of the six pairs.

The measure is kept, because sentence length distribution is a real signal in the research and the raw figure is worth seeing. Its verdicts are kept too, under 0.30 and over 0.55, but for a reason worth being explicit about: they are retained as evidence rather than as guidance. `⚠ Low burstiness` on a human paragraph and `✓ Good length variation` on a listicle are the two clearest demonstrations in this repository that a metric can be confidently wrong, and `examples/already-natural/` and `examples/linkedin-post/` are built on them. Nothing in `SKILL.md` acts on either verdict, and no stage treats raising burstiness as an objective.

**The meaning-preservation proxy is inverted on this repository's own examples.** Token overlap flags five of the six pairs for `Major meaning drift`, including every rewrite considered correct here, and awards its highest score to the one pair where the text was left alone. A measure that ranks the examples backwards cannot be used as a gate, so nothing in `SKILL.md` consults it. Details in `benchmarks/README.md`.

**The participial clause detector has a known false negative.** Its pattern is anchored to the first word of the sentence, so `By leveraging the power of...` does not match. It is also defined on openers only, so a participial clause in the middle of a sentence is outside its scope by construction. The strongest single signal in the research is the one this proxy is worst at detecting. The reading of `examples/technical-passage/` finds four present participial clauses, two of them sentence-initial behind `By` and two mid-sentence, and the script scores the passage 0 of 12. The report prints the anchoring caveat under the figure whenever the count is 0, which is every file in this repository except `examples/academic-abstract/input.md`, and carries it in the `caveat` key on every `--json` run.

**A stance verdict now requires a floor under it, and the version without one was wrong on every file here.** `stance_balance` compared the hedge and booster counts directly and returned one of three verdicts unconditionally, so a text with neither fell through to `calibrated`, because `0 > 0` is false in both branches. Seventeen files in this repository got a verdict out of that function and not one of them was right, including twelve that carried no stance marker at all and were told they were calibrated. The fix reports `absent` and `too sparse to judge` as themselves, and holds a balance verdict back until 3 markers and 2.0 per 1,000 words. Both floors are heuristics on this proxy's scale. No paper reports them, and absent stance is not a defect on its own: a passage explaining how a cache works has nothing to hedge. Whether the gap matters is genre judgment, which is why the scripts report it and `SKILL.md` rules on it.

**The two newest checks are this repository's own, with no research multiplier behind either.** Repeated sentence frames and three-item series are both listed as observable signs in `references/wikipedia-signs.md`, and neither has a measured human rate anywhere in the literature cited here. So the frame check warns on the narrowest condition available, one frame in two adjacent sentences, because a rate threshold would have to be invented and any figure chosen would have been fitted to the text in front of whoever chose it. The series check warns on nothing except anaphora across all three items, and otherwise prints its list for a reader to run the deletion test on.

**Both of those checks have false positives, and they are held as tests rather than described in passing.** A comma followed by an `-ing` word matches a gerund subject, so `In conclusion, caching remains an indispensable tool` counts as a frame. A series needs the Oxford comma to be seen at all, so `a room, a window and a reviewer` is missed entirely. An opening adverbial in front of a compound sentence yields three comma segments, so `Economically, India grew, and Bollywood thrived` is reported as a series when it is not one. A pipe is not a sentence terminator, so a table cell ending in a comma series gets joined to the paragraph below it and the third item is collected from prose that has nothing to do with the list. A heading is not a sentence terminator either, so two matches separated by a heading are read as adjacent. Fenced blocks and quoted specimens are prose to both checks, so a file that cites a frame inherits a warning for it, which is why the example inputs, the tables that discuss them and the rule page that names the frames all report frames they only quote. Every one of those cases is pinned in `scripts/verify_checks.py` as a `KNOWN LIMIT`, so none of the behaviour can change without a control failing.

**Running the two checks over this repository is the use they were built for, and the result belongs on the record.** The frame check reports seven adjacent pairs across five files, and every one of them lands in a class named above. Two are in `examples/technical-passage/input.md`, machine-written and the exact material the check exists to catch, so those are the check succeeding. Three more are pages charged for a specimen they quote, two in `rules/rhythm.md` and one in `references/style-research.md`, and in one of those the `> ` line after a colon is read as part of the sentence that introduced it. One is in `examples/personal-essay/rationale.md`, where a table cell quoting a specimen sits beside a blockquote quoting another.

The seventh is the only one drawn from prose this repository wrote in its own voice, and both halves of it are wrong. It matches `including` in one sentence, a preposition rather than a participle, and `existing` in the next, which belongs to a different section of `references/wikipedia-signs.md`. A level-3 heading stands between the two. A heading carries no terminal punctuation, so the sentence splitter runs the end of one section, the heading and the body of the next into one sentence, and the adjacency the warning rests on does not exist on the rendered page. `dist/SKILL.md` reports those seven pairs and no others, inherited from the sections it inlines.

The anaphora warning fires six times across the source markdown, and reading each one clears all six. One is the table artifact above. The other five are enumerations of three, four, five and eight items in which every item carries a figure, a reading or a step that cutting it would lose: three burstiness scores in `examples/already-natural/README.md`, the three stages of the study's two-chunk design in `references/style-research.md`, and the eight self-review questions summarised in this file. That is the division of labour working as designed. The script found the parallelism, and a reader decided case by case that the parallelism was the shape of the content rather than a cadence laid over it. `dist/SKILL.md` reports those six and one more, `a bigger room, a longer window, and a second reviewer`, which sits in a comment inside the embedded measurer: the check firing on the fixture written to demonstrate it.

**Proxy figures and research figures are different measures.** The scripts count suffixes with regular expressions; the research parsed dependencies and applied Biber's tagset. Across the five model-generated inputs in `examples/` the proxy averages 80.0 per 1,000 words against the tagged 14.6, about five and a half times, and the per-file figures are in `references/style-research.md`. Compare a proxy figure only against another run of the same script.

**A script measures a file, not a deliverable.** Where an output contains flags and bracketed slots addressed to the author, those words are counted as prose. In `examples/gen-ai-article/` three flagged vocabulary terms survive into the output solely because the flag quotes them as examples of what was removed. In `examples/personal-essay/` five separate readings, including the file's only stance marker, come from editorial notes rather than from the essay. No script can tell citation from use.

**The measurements reflect 2024 and 2025 model behaviour.** Reinhart et al. sampled models of that period. Em dash frequency has already shifted: as of mid-2026 only Claude exceeds professional human writers on it, ChatGPT uses fewer than it did, and GPT-5.1 suppresses them further. Rules and thresholds here need revisiting as models change, and fine-tuning on genre-specific data can reduce the fingerprint substantially.

**Genre detection is imperfect.** Stage 0 states its inference explicitly and invites correction, because a genre error propagates through every later stage in the same direction.

**Short voice samples give thin profiles.** Under roughly 200 words the profile is approximate at best, and the skill says so rather than overfitting to a paragraph.

**The skill cannot verify facts.** A factual error in the source survives the rewrite. Fact-checking is the author's.

**The evidence base is predominantly English.** The structural patterns differ in other languages and the cross-language behaviour of these rules is unstudied.

**This is not a route around academic or professional honesty rules.** Using the skill to pass model-written work off as your own where that is prohibited is a misuse of it. The purpose is writing that communicates, and the best writing still comes from someone who knows what they want to say. The skill can help with presentation. It cannot supply substance, and `examples/gen-ai-article/` is here to show what it does when asked to.
