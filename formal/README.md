# Formal verification

This directory is a reproducible Lean 4 project for the mathematical core of
*Microeconomic Theory I*. It does not claim that every theorem in the book is
formalized.

## One-command check

From the repository root:

```bash
bash formal/scripts/check.sh
```

The first run fetches the pinned dependencies and may take several minutes.
Later runs use Lake's local cache. The checker:

1. verifies the exact dependency revisions in `lake-manifest.json`;
2. rejects unchecked declarations in the textbook Lean source;
3. validates the machine-readable coverage ledger, including semicolon-separated
   declaration lists, and requires every verified declaration to appear in the
   kernel trust audit;
4. builds the local library together with the consumed slice of the pinned
   WGARP dependency and typechecks every verified coverage declaration by its
   fully qualified name;
5. runs `#print axioms` on every audited result and accepts only `propext`,
   `Classical.choice`, and `Quot.sound`.

The complete book build calls this same checker:

```bash
bash scripts/check_book.sh
```

## Pinned environment

- Lean: `leanprover/lean4:v4.32.0-rc1`
- WGARP: `vaguiarl/wgarp-lean` commit
  `d874dab846e28928f2a75b2359a0c2a8766a7b93`
- Mathlib: the exact transitive revision recorded in `lake-manifest.json`

The WGARP source is fetched by Lake and remains a separate public project. It
is not copied into this repository. The local Afriat declarations are typed
consumers of exact upstream theorems, so an incompatible upstream interface
causes the build to fail.

## Modules

| Module | Checked content |
|---|---|
| `Econ803.Foundations.Relations` | relation parts, finite greatest elements, transitive closure, Szpilrajn extension |
| `Econ803.Choice.WARP` | greatest-element choice and set-valued WARP |
| `Econ803.Consumer.Demand` | budget scaling, demand homogeneity, imported budget exhaustion |
| `Econ803.Consumer.RevealedPreference` | imported finite GARP/Afriat and compensated-demand certificates |
| `Econ803.Consumer.Duality` | expenditure homogeneity, concavity, and relative-supergradient Shephard core on an explicit nonempty admissible price domain |
| `Econ803.Uncertainty.FiniteDominance` | monotone-coupling implication for finite stochastic dominance |
| `Econ803.DiscreteChoice.Logit` | multinomial-logit odds/IIA identity with a strictly positive economic scale, plus its algebraic core |
| `Econ803.Firm.Profit` | profit homogeneity, convexity, relative subgradient, and efficiency core on an explicit nonempty admissible price domain |
| `Econ803.Equilibrium.Welfare` | finite price-support summation lemmas consumed by later welfare and core theorems |
| `Econ803.BookNarrative` | dependency-order metadata only, not economic proofs |
| `Econ803.TrustAudit` | kernel axiom reports for coverage-listed and selected supporting declarations |

`OrderTheory.lean`, `ChoiceTheory.lean`, and `BookNarrativeLogic.lean` are the
original small standalone checks retained for history. New formal work belongs
in the `Econ803/` library.

## What “theorem star” means

A reader-level theorem star is an editorial compression device. It does not
mean “Lean verified.” Each reader theorem has a full mathematical target in
`theorem_pairs.tsv`; Lean status is reported separately.

- `verified-local`: the stated Lean declaration is proved here;
- `verified-imported`: it compiles against an exact pinned upstream proof;
- `verified-core`: a named, reusable core is proved, but a documented bridge to
  the book's full theorem remains;
- `future-target` or `cited-only`: no local proof is claimed.

See `ARCHITECTURE.md` for competing proof routes and `coverage.json` for exact
declarations, weakest assumptions, and missing bridges.

## Trust boundary

The project permits only `propext`, `Classical.choice`, and `Quot.sound` in the
kernel reports, including classical choice where Mathlib's Zorn construction
is used. The checker fails if a verified ledger declaration is absent, omitted
from `TrustAudit.lean`, has no axiom report, or depends on any other axiom. It
does not permit unchecked proof placeholders or locally postulated economic facts.
Narrative dependency checks and statement inventories are metadata; they do
not upgrade a theorem's verification status.
