# THE PROFILE: SUPPRESS THESE

Rates per 1,000 words. "Human" is the measured baseline. "Model" is the instruction-tuned rate as a percentage of human. "Ceiling" is the target.

| Feature | Human | Model | Ceiling |
|---|---|---|---|
| Present participial clause, as in `Building on this, we shipped` | 1.7 | **224-527%** | 2 |
| `That` clause as sentence subject | 2.1 | **173-331%** | 2 |
| Past participial clause, as in `Built in a week, the house stood` | 0.3 | **150-307%** | 0.5 |
| Present participial postnominal, as in `the event causing this` | 1.3 | **124-293%** | 1.5 |
| Past participial postnominal, as in `the solution produced by` | 1.5 | **75-257%** | 2 |
| Nominalizations, the `-tion` `-ment` `-ness` `-ity` family | 14.6 | **145-214%** | 16 |
| `seem` and `appear` as verbs | 0.7 | **128-179%** | 1 |
| Gerunds | 3.0 | **119-156%** | 3.5 |
| Phrasal coordination, as in `the nouns and verbs` | 6.1 | **144-194%** | 7 |
| Attributive adjectives, as in `the big horse` | 43.8 | **100-150%** | 46 |
| Demonstratives as determiners, `this` and `these` | 6.5 | **77-137%** | 7 |
| Place adverbials | 3.4 | **99-146%** | 4 |
| Prepositional phrases | 98 | **100-118%** | 102 |
| Mean word length in characters | 4.4 | **114-116%** | 4.3 to 4.7 |

Mean word length is the cheapest check here and one of the most reliable. Model prose runs 5.0 to 5.1 characters. Two extra long words per sentence, sustained across a page, is a fingerprint by itself.

To bring it down, swap Latinate abstractions for their Anglo-Saxon equivalents: `populations` becomes `numbers`, `confirmed` becomes `seen`, `sufficient` becomes `enough`, `approximately` becomes `about`, `additional` becomes `more`, `initial` becomes `first`, `residence` becomes `home`, `purchase` becomes `buy`, `demonstrate` becomes `show`. The average moves fast, because the words being replaced are the long ones.

---

# THE PROFILE: RESTORE THESE

The half that most rewrites miss. Features humans use and instruction-tuned models suppress. "Floor" is the target.

| Feature | Human | Model | Floor |
|---|---|---|---|
| `because` | 1.5 | **19-20%** | 1.2 |
| Pro-verb `do`, as in `it does` or `she didn't` | 3.2 | **25-26%** | 2.5 |
| `Wh-` relative as object, as in `the man who Sally likes` | 0.3 | **13-20%** | 0.25 |
| Synthetic negation, as in `no answer is good enough` | 1.3 | **36-51%** | 1 |
| Amplifiers: `absolutely`, `extremely`, `really` | 2.1 | **46-63%** | 1.8 |
| Demonstrative pronouns, as in `That is the problem` | 6.1 | **50-55%** | 5 |
| Sentence relatives, as in `which is the odd part` | 1.0 | **50-51%** | 0.8 |
| Hedges: `almost`, `something like`, `at about` | 1.3 | **50-63%** | 1 |
| Agentless passive, as in `the model was fitted` | 7.8 | **51-53%** | 6.5 |
| Second-person pronouns | 15.7 | **52-63%** | register |
| Public verbs: `said`, `told`, `announced`, `admitted` | 6.8 | **53-63%** | 5.5 |
| Clausal coordination, as in `long, but I read it anyway` | 12.4 | **59-63%** | 11 |
| Existential `there`, as in `there is a` or `there were` | 2.1 | **42-71%** | 1.8 |
| Discourse particles, sentence-initial `well` `now` `anyway` | 1.0 | **60%** | 0.8 |
| Perfect aspect, as in `has written` or `had gone` | 7.2 | **60-62%** | 6 |
| Contractions | 18.1 | **60-63%** | 16 if conversational |
| `be` as main verb: `is`, `are`, `was` | 30.0 | **61-63%** | 27 |
| Analytic negation: `isn't`, `don't`, `not` | 9.7 | **61-73%** | 8 |
| First-person pronouns | 35.3 | **62-81%** | 30 if first person |
| `That` verb complement, as in `I said that he went` | 2.5 | **55-70%** | 2 |
| Emphatics: `a lot`, `for sure`, `really` | 9.2 | **68-75%** | 8 |
| `That` deletion, as in `I think he went` | 0.8 | **66-75%** | 0.7 |
| Stranded prepositions, as in `the thing I was thinking of` | 0.9 | **66%** | 0.7 |
| Adverbs, all types | 71.8 | **73-86%** | 65 |
| Past tense | 41.9 | **77-83%** | register |
| Infinitives | 16.5 | **83-87%** | 15 |

## How to actually restore them

**Use `because`, not its formal substitutes.** Models reach for `as`, `due to`, `given that`, `owing to`, `in light of`. A fivefold underuse of the plain word is one of the largest single gaps in the data.
`Given the latency constraints, we cached the result.` becomes `We cached the result because it was too slow otherwise.`

**Use the pro-verb `do`.** Models restate the full verb where a person substitutes.
`The second approach reduced load more than the first approach reduced load.` becomes `The second approach cut load more than the first one did.`

**Use the agentless passive.** The advice to avoid the passive voice pushes prose toward the model profile. GPT uses agentless passives at roughly half the human rate. Where the agent does not matter, use the passive.
`Someone deployed the fix on Thursday.` becomes `The fix was deployed Thursday.`

**Coordinate clauses.** Join two independent clauses with `and`, `but`, or `so`. Models prefer subordination or a full stop.
`The test passed. However, the underlying bug remained.` becomes `The test passed, but the bug was still there.`

**Use existential `there`.** Models rewrite these out because style guides call them weak. Humans use them 2.1 times per 1,000 words.
`Two unresolved issues remain in the parser.` becomes `There are still two things wrong with the parser.`

**Use bare demonstrative subjects.** Models write `this approach`, `this finding`, `this result`. Humans often write just `this` or `that`.
`This finding was the surprising part.` becomes `That was the surprising part.`

**Use sentence relatives.** A trailing `which` clause commenting on the whole preceding clause.
`The deploy ran twice. The duplicate charges followed from that.` becomes `The deploy ran twice, which is how we got the duplicate charges.`

**Delete `that`, and strand prepositions.** Both correct, both informal, both suppressed by a model chasing formality.
`the candidate about whom I was thinking` becomes `the candidate I was thinking of`.
`I believe that he left` becomes `I think he left`.

**Use plain speech verbs.** `said` and `told`, not `noted`, `emphasized`, `highlighted`, `underscored`. The interpretive verb inflates the nominalization count and the Tier 2 count at once.

**Keep adverbs.** Models strip them by 15% to 27% because "adverbs are weak." The result is a measurable hole. Keep the adverb that carries information.

**Keep real hedges, cut ceremonial ones.** Keep `almost`, `something like`, `about`, `really`, `pretty much`. Cut `it is worth noting that`. Both moves point the same direction.
