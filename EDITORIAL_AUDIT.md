# Backward editorial and formalization plan

## Terminal artifact

The target is a modern graduate microeconomics textbook with the breadth and navigational role of Mas-Colell, Whinston, and Green, but with contemporary revealed-preference, behavioral, random-choice, and computational material. A publishable release must satisfy this contract:

- one authoritative LyX manuscript and one reproducible student PDF;
- a smooth dependency order from primitives to applications, even when foundational material is placed in an appendix;
- explicit domains, quantifiers, regularity assumptions, and function-versus-correspondence distinctions;
- one canonical notation ledger, with visible local exceptions;
- no accidental duplication, lecture shorthand, dangling references, or hidden external assets;
- no student problems or solutions in the initial public release;
- a result-level verification ledger distinguishing local Lean proofs, external Lean proofs, audited textbook proofs, cited theorems, and exposition.

“Lean verified” is reserved for propositions accepted by the Lean kernel. The narrative dependency checker certifies organization only; it is not evidence for the truth of an economic theorem.

## Selected proof architecture

Three architectures were considered.

| Architecture | Benefit | Cost or failure mode | Decision |
|---|---|---|---|
| Formalize the entire book end to end | Strongest possible machine-checked claim | Rebuilds decades of analysis, topology, convexity, probability, and equilibrium theory before the book can be taught | Reject for this release |
| Verify a reusable logical core, reuse the WGARP library, audit elementary arguments, and cite deep standard theorems | High assurance where formalization has the greatest teaching and reuse value; feasible on the course timetable | Requires an explicit trust boundary and disciplined theorem ledger | **Selected** |
| Use Lean only as a chapter-order lint | Cheap and useful for prose organization | Does not verify any economics | Retain only as a supplementary check |

The weakest sufficient formal spine is therefore:

1. order-theoretic primitives and finite relation facts (`formal/OrderTheory.lean`);
2. preference maximization and WARP (`formal/ChoiceTheory.lean`);
3. GARP, Afriat inequalities, and revealed-preference closure (external WGARP project);
4. an explicit dependency and verification-status map (`formal/BookNarrativeLogic.lean`);
5. line-by-line textbook checking or authoritative citations for the remaining results.

## Logical map versus reading order

The book begins with economic primitives and places Order Theory in Appendix A. Logically, however, the appendix is a dependency root. The Lean narrative map records logical order separately from physical reading position. This avoids the false implication that an appendix is logically downstream merely because students encounter it later.

| Logical block | Pedagogical role | Main downstream use |
|---|---|---|
| Relations, orders, and closures | Mathematical appendix and reference vocabulary | preference, revealed preference, dominance, matching |
| Choice, preference, and observed demand | observable and behavioral foundations | utility representation, WARP, Afriat |
| Utility, duality, and integrability | optimization representation | welfare, aggregation, equilibrium |
| Risk and stochastic choice | uncertainty and heterogeneity | asset demand, random utility, sequential trade |
| Production and competitive allocation | supply, efficiency, and prices | welfare theorems and equilibrium |
| Aggregate excess demand and equilibrium | existence, regularity, and uniqueness | revealed equilibrium and computation |
| Matching and CGE | allocation without prices; quantitative application | advanced applications |

## Duplication policy

Repeated objects are retained only when the second appearance changes the question or level of abstraction.

| Repeated material | Distinct purpose | Required editorial treatment |
|---|---|---|
| Budget sets, Walras' law, WARP, and Slutsky restrictions | observed-demand restrictions first; derivation from utility and duality later | define once per domain, cross-reference, and label the change of lens |
| Abstract choice rationalization and finite price–quantity revealed preference | arbitrary feasible sets versus budget observations | announce the specialization and reuse common relation terminology |
| GARP/Afriat and SARP rationalization | weak versus strict revealed-preference tests | align hypotheses and proof template; do not merge the results |
| Individual and aggregate demand restrictions | aggregation may destroy individual restrictions | keep the contrast and state the aggregation assumptions explicitly |
| General Equilibrium and Positive Theory of Equilibrium | welfare/definitions versus existence/regularity/uniqueness | retain separate chapters with reciprocal roadmaps |
| Sparse-max demand and equilibrium with inattention | behavioral model versus equilibrium application | derive the model once and cross-reference it in equilibrium |
| Expected utility and random expected utility | individual preferences versus stochastic choice across observations or agents | retain both and state what is random in each model |
| Consumer Afriat and revealed-equilibrium restrictions | individual demand data versus market equilibrium data | begin each treatment with an observables/unobservables table |

Exact repeated headings are reported automatically in `BOOK_MAP.md` and must be resolved before a tagged release.

## Release gates

A public release passes only when:

1. `scripts/check_book.sh` succeeds, including the external WGARP build when available;
2. the generated PDF is visually inspected at the front matter, every chapter boundary, dense mathematics, figures, and the final appendix pages;
3. `BOOK_MAP.md` reports no generic repeated section titles;
4. `formal/theorem_inventory.tsv` is regenerated and every flagship theorem has an entry in `formal/COVERAGE.md`;
5. the public Git tree and its reachable history contain no unreleased assessments or solutions.

## Next increments after version 0.1

The next work should be additive and reviewable: stable labels and cross-references; authoritative citations; chapter objectives and summaries; carefully chosen examples; then weekly student problem sets. Solutions remain outside the public repository.
