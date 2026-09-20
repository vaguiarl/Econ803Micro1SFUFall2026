# Formal and mathematical coverage

This is a verification ledger, not a claim that the entire textbook has been
re-proved in Lean. The authoritative machine-readable record is
`coverage.json`; this page summarizes it for readers.

Coverage and theorem-pair IDs remain stable across chapter moves. An embedded
`Cxx` segment may therefore record the chapter where an item was first
registered; the `book_ref` and `chapter` fields record its current location.

## Status meanings

| Status | Meaning |
|---|---|
| Verified locally | The exact displayed Lean declaration is proved in this repository and passes the kernel trust audit. |
| Verified through a pinned import | A local declaration consumes an exact theorem from the pinned public WGARP project; both projects compile in one Lake build. |
| Core verified | A precise downstream theorem is proved, while a named analytic, representation, or model-encoding bridge remains. |
| Future target | The target and weakest intended assumptions are recorded, but no trusted proof declaration is claimed. |
| Cited only | The book delegates the research-scale result; exact source selection may still be a gate. |

## Current verified frontier

| Topic | Status | Exact declarations or boundary |
|---|---|---|
| Appendix order theory | Verified locally | `symmetricPart_is_equivalence`, `strictPart_asymmetric`, `strictPart_transitive`, `finite_exists_greatest`, `relation_subset_transitiveClosure`, `transitiveClosure_transitive`, `transitiveClosure_least`, `partialOrder_has_linearExtension` |
| Rational choice and WARP | Verified locally | `rational_choice_satisfies_WARP`, `rationalization_implies_WARP` |
| Demand homogeneity | Verified locally | `utilityDemand_scale_iff`; it needs only a positive common scale |
| Budget exhaustion | Verified through a pinned import | `demanded_bundle_exhausts_budget` consumes `WGARP.utilityDemand_expenditure_eq_wealth` |
| Compensated demand | Verified through a pinned import | `compensated_law_of_demand` requires positivity only of the original price vector; positivity of the compensated/new price is not used. The manuscript's strict single-valued WARP form still needs an encoding bridge. |
| Finite GARP and Afriat | Verified through a pinned import | `finite_GARP_iff_Afriat_inequalities`, `finite_Afriat_theorem`, `finite_Afriat_constructive` |
| Finite WGARP and coherent CMU | Verified through a pinned import | `finite_wgarp_cmu_characterization` consumes the pinned six-statement Theorem 1 using explicit finite and matrix/simplex CMU normal forms. Connecting those types to the book's broader compact-coalition hyperspace formulation remains an explicit bridge. |
| WARP and strict coherent CMU | Cited only | The pinned dependency has no WARP/strict-star-concavity theorem; no Lean verification is claimed. |
| Expenditure duality | Core verified | On a nonempty explicit admissible price set `P`, `expenditure_homogeneous`, `expenditure_concave`, and `hicksian_bundle_is_supergradient` require attainment only at prices in `P`; scaled-price or mixture membership is assumed only where used. Analytic attainment and smooth Roy/Slutsky bridges remain. |
| Finite stochastic dominance | Core verified | `monotoneCoupling_implies_expectedUtility_order`; CDF dominance to monotone coupling and general-measure FOSD remain |
| Multinomial logit | Verified locally | `logit_odds_ratio` is the economic statement and requires `0 < μ`; `logit_odds_ratio_algebraic` records the underlying identity separately |
| Firm duality | Core verified | On a nonempty explicit admissible price set `P`, `profit_homogeneous`, `profit_convex`, and `profit_maximizer_is_subgradient` require maximization only at prices in `P`; `profit_maximizer_is_efficient` separately uses a positive price. Existence and differentiable envelope bridges remain. |
| First welfare theorem | Core verified | `priceSupport_rulesOut_paretoImprovement` proves only the price-support summation contradiction; deriving support from equilibrium optimization and local nonsatiation remains |
| Walrasian allocation and strong core | Core verified | `priceSupport_rulesOut_strongCoalitionBlock` proves the exact finite-coalition summation contradiction for Problem 12.4: all coalition members weakly improve, at least one strictly improves, coalition resources balance exactly, individual equilibrium budgets hold, and one common price supports weak and strict improvements. Deriving that support from Walrasian optimization and local nonsatiation remains. |

## Pinned WGARP certificates

The Lake project pins `vaguiarl/wgarp-lean` at commit
`d874dab846e28928f2a75b2359a0c2a8766a7b93`. Important consumed interfaces
include:

| Textbook material | Upstream certificate |
|---|---|
| GARP and Afriat inequalities | `WGARP.garp_iff_exists_afriatInequalities` |
| Constructive regular Afriat utility | `WGARP.garp_iff_hasRegularUtilityRationalization` and `WGARP.garp_iff_exists_afriatCertificate_and_regularUtility` |
| Six-way finite WGARP--CMU characterization | `WGARP.theorem_one` |
| Budget exhaustion | `WGARP.utilityDemand_expenditure_eq_wealth` |
| Compensated law of demand | `WGARP.demand_cross_expenditure`, followed by local algebra |

Because the upstream commit is a normal Lake dependency, these are no longer
conditional on an environment variable. A clean build fetches and compiles the
recorded source.

## Main future targets

No Lean-complete claim is made for continuous utility representation, Berge
demand continuity, the full smooth consumer-duality chain, finite expected
utility, the WARP--strict-CMU characterization, general-distribution FOSD,
Gorman aggregation, the expected-surplus
envelope, partial-equilibrium existence, the second welfare theorem,
Walrasian existence, regularity and gross-substitutes uniqueness,
Sonnenschein--Mantel--Debreu, Brown--Matzkin, Arrow--Radner equivalence,
Gale--Shapley, or top trading cycles.

`coverage.json` records the exact target, weakest intended assumptions, and
missing bridge for each. `ARCHITECTURE.md` compares alternative proof routes
for the hardest targets. `theorem_pairs.tsv` separately controls the proposed
reader-theorem/full-theorem editorial pairing.

## Trust audit

Run:

```bash
bash formal/scripts/check.sh
```

The command builds the project, rejects unchecked declarations, validates and
typechecks every verified coverage declaration, and requires each one to have
an entry in `TrustAudit.lean`. It then checks every reported dependency against
the explicit whitelist `propext`, `Classical.choice`, and `Quot.sound`.
`Econ803.BookNarrative` checks dependency metadata only and does not prove
economic claims.
