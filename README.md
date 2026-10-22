# Microeconomic Theory I — Fall 2026

This repository contains the public, student-facing first edition of Victor Aguiar's graduate microeconomic theory text for Simon Fraser University. The book is designed for the role that *Microeconomic Theory* by Mas-Colell, Whinston, and Green has traditionally played: a rigorous common language for graduate theory, complemented by modern revealed-preference, behavioral, random-choice, and computational material.

The Fall 2026 course runs from September 9 through December 7. Class meets Fridays from 9:30 a.m. to 12:20 p.m. in WMC 4602.

## Student quick links

- [Midterm 1 worked solutions (October 16, 2026; PDF)](course/released_assessments/2026-10-16/ECON803_Midterm1_Fall2026_Worked_Solutions.pdf) ([study guide and editable LyX source](course/released_assessments/2026-10-16/README.md))
- [Download the current course notes (PDF)](https://raw.githubusercontent.com/vaguiarl/Econ803Micro1SFUFall2026/main/notes/Microeconomics_1_notes_by_Victor_Aguiar.pdf)
- [Download the question-only practice book (PDF)](https://raw.githubusercontent.com/vaguiarl/Econ803Micro1SFUFall2026/main/problemsets/practice_book/ECON803_Practice_Book_Fall2026.pdf)
- [Download the Economic KKT Cookbook (PDF)](course/handouts/kkt_economics_cookbook/ECON803_Economic_KKT_Cookbook.pdf)
- [Browse the canonical problem bank](problems/PROBLEM_BANK.md)
- [Gravity, Trade and Transport practice set (PDF)](problemsets/gravity_trade/Gravity_Trade_Practice.pdf) ([LyX](problemsets/gravity_trade/Gravity_Trade_Practice.lyx))
- [Galor KKT and general equilibrium practice set (PDF)](problemsets/galor_general_equilibrium/Galor_KKT_General_Equilibrium.pdf) ([LyX](problemsets/galor_general_equilibrium/Galor_KKT_General_Equilibrium.lyx))
- [Read the course outline](COURSE_OUTLINE.md)
- [See the weekly release structure](problemsets/README.md)

These links always point to the public `main` branch. Only explicitly released assessment solutions appear under `course/released_assessments/`; instructor rubrics, student records, other solutions and unreleased assessments remain private.

The Fall 2026 baseline has four commitments:

1. every mathematical statement is written with its objects and hypotheses visible;
2. notation has one book-wide default, with local exceptions announced explicitly;
3. repeated material is either consolidated or retained only when it serves a distinct logical purpose; and
4. formal verification is reported honestly, result by result, with no claim that a structural lint is a proof of an economic theorem.

## Read and edit the book

- Course outline: [`COURSE_OUTLINE.md`](COURSE_OUTLINE.md) ([DOCX version](course/ECON_803_Fall_2026_Course_Outline.docx))
- Student PDF: [`notes/Microeconomics_1_notes_by_Victor_Aguiar.pdf`](notes/Microeconomics_1_notes_by_Victor_Aguiar.pdf)
- Authoritative LyX source: [`notes/Microeconomics_1_notes_by_Victor_Aguiar.lyx`](notes/Microeconomics_1_notes_by_Victor_Aguiar.lyx)
- Chapter and duplication map: [`BOOK_MAP.md`](BOOK_MAP.md)
- House notation: [`NOTATION.md`](NOTATION.md)
- Notation link-validation ledger: [`editorial/notation/glossary.tsv`](editorial/notation/glossary.tsv)
- Mathematical verification ledger: [`formal/COVERAGE.md`](formal/COVERAGE.md)
- Lean proof architecture: [`formal/ARCHITECTURE.md`](formal/ARCHITECTURE.md)
- Reader/full theorem architecture and migration record: [`THEOREM_STAR_PLAN.md`](THEOREM_STAR_PLAN.md)
- Figure, provenance, and rights audit: [`FIGURE_AUDIT.md`](FIGURE_AUDIT.md)
- Canonical question-only problem bank: [`problems/PROBLEM_BANK.md`](problems/PROBLEM_BANK.md)
- Standalone question-only Practice Book: [`problemsets/practice_book/ECON803_Practice_Book_Fall2026.pdf`](problemsets/practice_book/ECON803_Practice_Book_Fall2026.pdf) ([editable LyX source](problemsets/practice_book/ECON803_Practice_Book_Fall2026.lyx))
- Economic KKT Cookbook: [`course/handouts/kkt_economics_cookbook/ECON803_Economic_KKT_Cookbook.pdf`](course/handouts/kkt_economics_cookbook/ECON803_Economic_KKT_Cookbook.pdf) ([editable LyX source](course/handouts/kkt_economics_cookbook/ECON803_Economic_KKT_Cookbook.lyx))
- Chapter use-case and verification map: [`problems/CHAPTER_PATHWAYS.tsv`](problems/CHAPTER_PATHWAYS.tsv)
- Two-part chapter release views: [`problemsets/README.md`](problemsets/README.md)
- Artists case study, Problem 10.4: [Music Sales and Concerts (PDF)](problems/case_studies/Artists_Music_and_Concerts.pdf) ([LyX](problems/case_studies/Artists_Music_and_Concerts.lyx))
- Publication-baseline review: [`EDITORIAL_REVIEW.md`](EDITORIAL_REVIEW.md)
- Backward editorial and formalization plan: [`EDITORIAL_AUDIT.md`](EDITORIAL_AUDIT.md)

The LyX file is the authoritative text, including the notation definitions and link placements. In the built PDF, a tracked symbol at its first use links to its entry in the final glossary, and the symbol in that glossary entry links back to the first use. The TSV ledger records stable semantic IDs for validation; it is not a second manuscript. Generated LaTeX and temporary build products are intentionally excluded from version control. All nineteen live figures are reproducible vector PDFs: their TikZ/PGFPlots sources and checked data live in `figures_tikz/`, and passing exports live in `notes/figures/tikz/`. Building the book does not require Dropbox or another repository.

## Verify the release

With LyX, LaTeX (including TikZ/PGFPlots), Poppler, Python 3 with `pypdf`, Perl, ripgrep, and Lean/Lake available, run:

```sh
bash scripts/check_book.sh
```

The command rebuilds and preflights all vector figures before exporting LyX, verifies the notation ledger against the canonical LyX source, compiles the PDF, checks every bidirectional first-use/glossary destination and link in that PDF, rejects raster images and unsafe fonts, builds the pinned Lean project together with the exact WGARP dependency, audits kernel assumptions and proof placeholders, validates the theorem-pair ledger, rejects restricted assessment files, and regenerates the chapter, duplication, and theorem indexes.

## Assessment policy

This public edition contains 91 chapter problems and 10 reserve problems, each with a stable identifier.
Problem labels are Core, Proof, Applied and Advanced. Each topic group closes with Part I: By hand and Part II: a named case and computational or formal extension; its designated case remains the final problem in that group. The unified General Equilibrium chapter contains three topic groups and all three original cases. Permanent problem identifiers can differ from printed chapter numbers after consolidation. The canonical prompts live in `problems/PROBLEM_BANK.md`, the 17 case pathways in `problems/CHAPTER_PATHWAYS.tsv`, and the printed chapter grouping in `problems/BOOK_CHAPTER_GROUPS.tsv`. Both student books use these same sources. Gravity Problems 16.A1 and 16.A2 and the Galor extension 16.A3 keep their released identifiers in the Advanced problems of the computable equilibrium topic. Student questions contain no private keys. Only explicitly authorized completed assessment solutions listed in `PUBLIC_RELEASES.json` may appear under `course/released_assessments/`. All instructor rubrics, student records, other solutions and unreleased assessments remain private.

Chapter 11 now unifies exchange geometry, production and welfare, excess demand, existence, equilibrium behavior, coalitions and empirical restrictions. The main existence proof constructs a continuous price map and applies Brouwer under unique demand assumptions. Appendix B gives the boundary and cap removal details and the Kakutani extension under convex preferences. The former consumer technical records are now Appendix C. Four original TikZ Edgeworth diagrams distinguish complementary bundles, gains from trade, efficiency, affordability and redistribution. Neither the analytic existence proof nor the fixed point theorems are claimed as locally Lean verified; Lean separately checks the declared argument dependencies and the existing welfare certificates.

Chapter 12, Niche Consumption and Product Space, now follows General Equilibrium and precedes Sequential Trade and Matching. It preserves the Neiman and Vavra discussion, ideal point choice, neighborhood substitution, measure valued baskets and the continuum Afriat argument. A reading guide in both student books connects it to existing problems without adding a weekly assignment or changing any released identifier. The finite commodity existence theorem is not asserted to establish equilibrium for a continuum of goods.

The production chapter now connects classical firm theory to [Aguiar, Kashaev and Allen's value function approach](https://doi.org/10.1016/j.jeconom.2022.06.007) and [Gandhi, Navarro and Rivers' flexible input approach](https://doi.org/10.1086/707736). It distinguishes quantities from revenue, productivity from output surprises, and technology identification from fitting data. Worked examples develop input shares, recovery from supporting prices, finite price counterfactual bounds and the conditional use of price proxies. The analytic identification results are cited and explained, not claimed as locally Lean verified.

Advanced Problem 9.A6 develops housing production, latent housing prices and land rents, inspired by [Epple, Gordon and Sieg](https://doi.org/10.1257/aer.100.3.905) and the housing application in Prices, Profits, Proxies, and Production. The original teaching model connects developer optimization, price proxy recovery and a closed competitive economy. It is timed practice, not an announced future examination. Its worked solution and rubric remain in the private handbook.

Problem 10.A7 restores the instructor's historical supply and demand estimation exercise, correcting the excluded shifter and distinguishing a slope from an elasticity. A labelled time series extension separates simultaneous determination from serial correlation. Problem 10.A8 connects discrete choice demand, equilibrium pricing and endogenous prices through a hand solvable logit benchmark and an optional BLP style share inversion exercise. Neither finite simulation nor share inversion alone is presented as an identification proof.

The workhorse-demand material now includes CES derivations, elasticities, calibration, limiting cases, and compensated welfare comparisons, plus a translog expenditure model with explicit regularity checks. Eleven worked examples connect those families to Cobb-Douglas, linear, Leontief, Stone-Geary, and quasilinear demand. Problems 1.2--1.6 and 2.4--2.6 provide further practice.

## Status

This is the Fall 2026 public baseline: a complete, buildable textbook manuscript with unified notation, references, end-of-chapter problems, vector artwork, and a reproducible Lean verification layer. The book now begins with utility maximization, develops duality and welfare, and then treats revealed preference as the observable content and extension of the benchmark model. Abstract choice, risk, stochastic choice, costly attention, and aggregation follow in that order. The theorem-pair ledger tracks 24 reader/full pairs: the WGARP and WARP coalitional multi-utility pairs are migrated, 19 pairs remain planned, and 3 remain source-gated. The WGARP pair has a checked wrapper around the pinned external theorem; the WARP strict-CMU result is cited only and carries no Lean-verification claim. Later releases should preserve stable problem and theorem identifiers and must not change the book's notation or logical spine silently.
