# Lean architecture for the textbook

## Contract and trust boundary

The terminal goal is not “put theorem names in Lean.” It is a reproducible
kernel check of the exact mathematical layer that later full theorem records
consume. The immutable acceptance conditions are:

- the public project builds with the pinned toolchain and dependency revisions;
- no textbook declaration uses an unchecked placeholder or a local axiom;
- every verified claim names an exact Lean declaration;
- a core-only proof records the missing bridge to the book's full statement;
- imported results compile against an immutable upstream revision;
- theorem-narrative metadata is never presented as mathematical verification.

`coverage.json` is the machine-readable implementation ledger.
`theorem_pairs.tsv` is the editorial reader-theorem/full-theorem pairing
ledger. The two ledgers answer different questions and must agree before a
result receives a “Lean complete” badge.

## Backward slice and priority

The main economic consumers, in dependency order, are:

```text
relations/order
  -> rational choice -> WARP
  -> finite budgets -> demand homogeneity / exhaustion
       -> compensated demand -> GARP / Afriat
       -> expenditure envelope -> Shephard / Slutsky targets
  -> finite risk order -> FOSD target
  -> production support -> profit/cost duality
       -> common price support -> welfare / core
       -> excess demand -> existence / uniqueness targets
  -> finite algorithms -> deferred acceptance / TTC targets
```

Priority 1 is the reusable finite core: order, WARP, observed demand, Afriat,
value-function algebra, welfare price summation, finite stochastic order, and
finite algorithms. Priority 2 is finite-dimensional analysis and linear
algebra. Priority 3 is correspondence topology, separation/fixed points, and
general probability. Source-gated representation results come only after an
exact theorem version is selected.

## Selected architecture: full theorem plus verified core

The project uses a two-level result interface.

1. A reader theorem states the economic conclusion and visible assumptions.
2. The full record freezes domains, quantifiers, hypotheses, dependencies,
   proof status, and the exact Lean mapping.
3. Lean verifies the full theorem when feasible. Otherwise it verifies the
   weakest independently meaningful core and names the missing bridge.

The star in a reader theorem means “compressed reader statement,” never
“approximately true” or “Lean verified.” Verification status is a separate
field. This adopts the pedagogical idea behind Strzalecki's marked theorems
while using a stricter local rule: every marked result has one full target and
an explicit proof-status record.

## Competing proof architectures

### Finite Afriat theorem

**Route A — rebuild locally.** Define budgets, graph reachability, Afriat
inequalities, construct the lower envelope, and prove all four implications.

- Terminal theorem reached: GARP iff regular utility rationalization.
- Largest missing interface: a second complete finite revealed-preference API.
- Estimated proof surface: large and almost entirely duplicated.
- Acceptance risk: high risk of notation drift from the existing project.

**Route B — pin and consume the public WGARP project (selected).** Compile the
exact upstream commit and expose theorem-exact downstream declarations.

- Lean bridge: `finite_Afriat_theorem` and `finite_Afriat_constructive`.
- Required leaves: upstream `WGARP.GARP` and `WGARP.GlobalAfriat`.
- Largest missing interface: manuscript-dataset to `WGARP.Dataset` encoding.
- Acceptance risk: low; the dependency and Mathlib revisions are in the Lake
  manifest and checked by the build script.

The selected route removes duplication while preserving the full kernel proof.

### First welfare theorem

**Route A — formalize the complete analytic economy.** Build preferences,
consumption and production correspondences, local nonsatiation, ownership,
profit maximization, and derive every price-support inequality internally.

- Terminal theorem reached: the full competitive-equilibrium theorem.
- Largest missing interface: topology plus the “weak improvement cannot be
  strictly cheaper” lemma in the exact production economy.
- Estimated proof surface: medium-to-large and sensitive to model conventions.

**Route B — prove the exact downstream price-support contradiction (selected
first).** Treat the weak/strict price-support inequalities as the immutable
intermediate contract and kernel-check the aggregate-price contradiction.

- Lean bridge: `priceSupport_rulesOut_paretoImprovement`.
- Required leaves: market clearing, finite summation, support inequalities.
- Verified frontier: the complete downstream economic contradiction.
- Structural blocker for the full theorem: derive support from the final
  manuscript definitions of optimality and local nonsatiation.

Route B is not labeled a complete first welfare theorem. It is the smallest
core that the full theorem will consume regardless of the chosen analytic API.

### Finite expected utility

**Route A — simplex/affine architecture (preferred future route).** Represent
lotteries as a finite simplex, prove an affine representation from independence
and mixture continuity, then evaluate the affine functional on Dirac lotteries.

- Terminal theorem reached: finite expected utility and affine uniqueness.
- Largest missing interface: the mixture-continuity-to-affine-representation
  theorem on the simplex.
- Reusable code: Mathlib finite sums and convex sets.

**Route B — quotient order plus mixture calibration.** Quotient lotteries by
indifference, choose best/worst prizes, calibrate each lottery by its mixture
with the extremes, and use the calibration as utility.

- Terminal theorem reached: the same representation under explicit best/worst
  and Archimedean lemmas.
- Largest missing interface: existence and uniqueness of the calibration.
- Acceptance risk: the proof becomes tied to extra nondegeneracy cases.

No declaration is installed merely to make this row look complete. Route A is
recorded as a future target until its expensive leaf is proved.

### Deferred acceptance

**Route A — executable state machine (preferred future route).** Implement
proposals and held matches, prove a decreasing finite measure, an invariant,
stability, and the rejection lemma for proposer optimality.

**Route B — relational existence proof.** Specify a terminal relation over
states and prove all maximal runs end in a stable matching.

Route A has the larger initial implementation cost but a smaller missing proof
cone for termination and produces executable examples. Work begins only after
the book freezes its acceptability and unmatched-agent convention.

## Current verified frontier

- **END-TO-END VERIFIED:** Appendix order parts, finite greatest element,
  transitive closure, Szpilrajn extension, rational-choice WARP, demand HD0,
  logit odds, and the stated finite monotone-coupling theorem.
- **CONSUMER VERIFIED THROUGH PINNED DEPENDENCY:** budget exhaustion,
  compensated demand, finite GARP/Afriat inequalities, and constructive regular
  Afriat rationalization.
- **CORE VERIFIED:** expenditure curvature/supergradient and profit
  curvature/subgradient on explicit nonempty admissible price domains (with
  scale or mixture membership assumed only by the result that uses it), profit
  efficiency at positive prices, the price-support summation lemma consumed by
  a first-welfare theorem, and the price-support no-blocking lemma consumed by
  the Walrasian core argument.
- **FUTURE OR CITED:** continuous utility representation, finite expected
  utility, Berge demand continuity, smooth Roy/Shephard/Slutsky, general FOSD,
  second welfare, equilibrium existence/SMD, Brown--Matzkin, Arrow--Radner,
  deferred acceptance, and TTC.

The exact declarations and missing bridges are in `coverage.json`; this prose
summary cannot upgrade their status.

## Replanning rule

If three proof attempts fail at the same absent interface, stop local tactic
search and reconsider the nearest architectural branch. In particular, do not
rebuild a theorem already available at the pinned WGARP interface, and do not
formalize a source-gated theorem before its exact mathematical statement is
frozen.
