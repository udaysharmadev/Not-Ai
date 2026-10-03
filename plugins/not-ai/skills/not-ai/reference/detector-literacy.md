# Detector literacy

Read this reference when a detector flag exists on genuine writing, or when
someone asks what a detector score means. It explains scores, their limits,
and how to respond to a flag with process evidence. It does not predict
scores, rewrite text to evade detection, or advise bypassing any detector.
For the skill's own stance, see the non-negotiable rules in SKILL.md.

## What the percentage means, per vendor

Vendor docs disagree with each other, so the same number means different
things in different reports:

- **Turnitin** reports the share of *qualifying* text (long-form prose
  sentences only; poetry, code, bullets, and tables do not qualify) its
  model considers possibly AI-generated or AI-paraphrased. Scores of 1-19%
  are suppressed behind an asterisk because false positives concentrate
  there. It is not a plagiarism similarity score.
  (https://guides.turnitin.com/hc/en-us/articles/22774058814093-Using-the-AI-Writing-Report)
- **GPTZero** reports its model's estimated probability that a document
  belongs to an AI class, e.g. "6% AI" means roughly 6 in 100 similar cases
  would look like this from AI. It is not the share of words written by AI.
  (https://support.gptzero.me/articles/7549392421-how-do-i-interpret-results-from-gptzero-s-advanced-sentence-scanning)
- **Originality.ai** reports confidence, not proportion: "60% Original"
  means 60% confident the content is human-written, not that 40% of it is
  AI-generated. Its plagiarism match score (hard source matches) is a
  different instrument from its AI confidence score.
  (https://originality.ai/blog/score-meaning)

Every vendor above states some version of the same limit: results are
probabilistic, must not be the sole basis for punishment or discipline, and
require human judgment alongside institutional policy.

## Why a flag is not proof: base rates

Accuracy on a balanced lab set is not trustworthiness in a classroom. When
AI use is rare, most flags are false. Worked example with a generous
detector (99% true-positive rate, 1% false-positive rate) over 1,000
submissions where 5% are truly AI-assisted:

- True positives: 50 x 0.99 = 49.5
- False positives: 950 x 0.01 = 9.5
- Of 59 flagged, 9.5 are innocent: **1 in 6 flags is wrong at "99%
  accurate."** At 1% prevalence it is 5 in 6.

`scripts/flag_response.py` computes this table for any stated rates; it
takes the rates as explicit arguments because lab figures do not transfer
to short, mixed, or second-language text.

## Who gets flagged wrongly, and why

- **Constrained style.** Liang et al. (2023) found 7 detectors misclassified
  61.3% of non-native TOEFL essays as AI versus ~5% of native 8th-grade
  essays, because limited lexical diversity means low perplexity, which the
  detectors read as machine-like. Formulaic writing (reviews, proposals,
  boilerplate) fails the same way.
  (https://arxiv.org/abs/2304.02819)
- **Memorized text.** Famous passages score as AI because the model has
  read them millions of times, so the next word is "obvious," not because
  they look machine-made. Independent tests repeatedly flag founding
  documents and scripture at 85-99% AI on free detectors.
- **Short and mixed text.** Vendors and independent benchmarks (RAID,
  Chicago Booth 2025, APT-Eval) agree accuracy collapses on short samples,
  paraphrased passages, and newer models. Several universities disabled
  detection after counting the false-flag arithmetic on their own
  submission volumes.

## If genuine writing was flagged

Detectors score the product; authorship lives in the process. Gather
process evidence, in this order:

1. Freeze everything: export the report with date and version, keep file
   metadata, name the current Docs version, preserve `git log` or
   Track Changes history. Do not edit after the accusation.
2. Process artifacts: notes, outlines, annotated readings, rough drafts
   with timestamps, library and citation-manager trails, prior samples
   showing stylistic continuity.
3. Comprehension: be ready to explain the thesis, sources, and each
   citation choice; offer a supervised rewrite or oral defense.
4. Procedure in writing: ask which tool, threshold, and false-positive
   rate were used; ask whether the score alone may count as evidence
   under institutional policy (most published policies say no); ask for a
   second reader blind to the score; file the appeal promptly.

## What this skill will and will not do

- Explain a score using vendor docs and public research. Yes.
- Compute prevalence-conditioned flag math. Yes, via the script.
- List process evidence for an appeal. Yes.
- Predict what a detector will say about a draft. No.
- Rewrite a passage to lower a detector score. No.
- Advise bypassing, humanizing past, or appealing a flag on
  machine-written text presented as human. No.

Improving prose for its readers (specific detail, real structure, the
author's own voice) is separate work with its own measures. It sometimes
moves statistical profiles as a side effect; that movement is never the
goal and never reported as one.
