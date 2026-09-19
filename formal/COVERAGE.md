# Formal and mathematical audit coverage

This is an editorial verification ledger, not a claim that every theorem in the textbook has been re-proved in Lean. The policy is:

1. kernel-check the small logical core and the results for which an existing verified library is available;
2. give complete elementary proofs when they materially help students;
3. cite standard representation, equilibrium, and matching theorems instead of recreating research-scale proofs;
4. state every theorem with the hypotheses actually used.

## Verification levels

| Level | Meaning |
|---|---|
| Lean | Checked by the Lean kernel with no `sorry`, `admit`, or local `axiom` |
| External Lean | Checked by the separate WGARP Lean project when `WGARP_LEAN_DIR` is configured |
| Textbook proof | Formal argument audited line by line in the LyX source |
| Cited theorem | Statement and hypotheses audited; proof intentionally delegated to the cited source |
| Expository | Model derivation or example checked algebraically, but not presented as a general theorem |

## Current coverage by topic

| Topic | Level | Main checks |
|---|---|---|
| Order theory appendix | Lean + textbook proof | Lean checks relation parts and maximal-versus-greatest results; the quotient order, finite extrema, closures, and extension theorem currently rely on audited textbook arguments |
| Choice and WARP | Lean + textbook proof | maximizing choice implies set-valued WARP; strict-part logic |
| GARP and Afriat | External Lean + textbook proof | graph GARP, Afriat inequalities, direct and indirect revealed preference |
| Consumer duality | Textbook proof + cited theorem | UMP/EMP hypotheses, expenditure continuity, Shepard's lemma, Slutsky differentiation |
| Expected utility | Textbook proof + cited theorem | finite-mixture representation, affine versus linear terminology, weak-star theorem assumptions |
| Aggregate demand | Textbook proof | Gorman aggregation, weak ULD, symmetric Jacobian part, homothetic and uniform-wealth cases |
| Random utility | Textbook proof + cited theorem | logit signs/scales, finite random-utility matrix representation, representative mixture |
| Production and partial equilibrium | Textbook proof | free disposal, cone embedding, Kuhn--Tucker corner inequalities, equilibrium existence tails |
| General equilibrium | Cited theorem + textbook proof | welfare assumptions, excess demand, regularity, index conditions, and core convergence |
| Sequential trade and matching | Cited theorem | Arrow--Debreu/Radner equivalence, deferred acceptance, TTC/core results |
| CGE and behavioral applications | Expository | accounting identities, calibration equations, and model-specific comparative statics |

## Reused WGARP certificates

The external project is intentionally not copied into this public course repository. Its principal reusable certificates include:

| Textbook material | WGARP module/certificate |
|---|---|
| GARP as reachability plus no strict reverse edge | `WGARP.GARP`, `garp_dataset_iff` |
| GARP and Afriat inequalities | `WGARP.GARP`, `garp_iff_exists_afriatInequalities` |
| Direct/revealed-preference closure | `WGARP.GARP`, `revealedPref_refl`, `revealedPref_trans` |
| Demand and strict affordability | `WGARP.Demand`, `preferenceDemand_strictlyPreferred_of_strictlyAffordable` |
| WGARP finite rationalization | `WGARP.FiniteConstruction`, `wgarp_iff_hasFiniteCoherentCMURationalization` |
| Two-observation acyclicity and WGARP | `WGARP.TheoremTwo`, `kAcyclic_two_iff_wgarp` |

The one-command audit is `WGARP_LEAN_DIR=/path/to/project bash scripts/check_book.sh`.

## Trust boundary

`BookNarrativeLogic.lean` verifies the declared dependency ordering of the book's main claims; it does not prove the economic content of those claims. `theorem_inventory.tsv` inventories the complete formal surface so later passes can be incremental. `BOOK_MAP.md` records the pedagogical sequence and exact repeated section titles.
