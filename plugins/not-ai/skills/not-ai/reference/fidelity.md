# Semantic fidelity: relations, not just literals

Read this reference when comparing source and output. Protected literals
(numbers, URLs, quotes, identifiers) are necessary but not sufficient. Meaning
lives in relations:

people, organisations, products, dates, measurements, percentages, currencies,
versions, citations, quoted text, code identifiers, technical terms, comparison
direction, negation, modality, confidence, causality, conditions, exceptions,
scope, chronology, who acted vs who observed, reported vs asserted information.

## Non-equivalences (never allow)

- may improve / improves; associated with / causes
- did not fail / failed; more than / less than; before / after
- some users / all users; we observed / research proves

`not_ai_core/fidelity.py` checks these deterministically where markers are
explicit (negation families, modal/temporal/scope flips, condition loss, number/
URL/quote/code loss, prompt-injection payloads). Everything subtler requires the
agent's explicit source-vs-output comparison before delivery — regex is not
semantic understanding. Build the internal ledger (fact/claim/actor/action/
object/qualifier/modality/negation/quantity/time/cause/condition/source/
protection) privately; expose only the receipt unless asked.
