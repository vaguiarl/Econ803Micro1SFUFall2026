# Microeconomic Theory I — Fall 2026

This repository contains the public, student-facing first edition of Victor Aguiar's graduate microeconomic theory text for Simon Fraser University. The book is designed for the role that *Microeconomic Theory* by Mas-Colell, Whinston, and Green has traditionally played: a rigorous common language for graduate theory, complemented by modern revealed-preference, behavioral, random-choice, and computational material.

The Fall 2026 course runs from September 9 through December 7. Class meets Fridays from 9:30 a.m. to 12:20 p.m. in WMC 4602.

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
- Chapter use-case and verification map: [`problems/CHAPTER_PATHWAYS.tsv`](problems/CHAPTER_PATHWAYS.tsv)
- Two-part chapter release views: [`problemsets/README.md`](problemsets/README.md)
- Artists case study, Problem 10.4: [Music Sales and Concerts (PDF)](problems/case_studies/Artists_Music_and_Concerts.pdf) ([LyX](problems/case_studies/Artists_Music_and_Concerts.lyx))
- Publication-baseline review: [`EDITORIAL_REVIEW.md`](EDITORIAL_REVIEW.md)
- Backward editorial and formalization plan: [`EDITORIAL_AUDIT.md`](EDITORIAL_AUDIT.md)

The LyX file is the authoritative text, including the notation definitions and link placements. In the built PDF, a tracked symbol at its first use links to its entry in the final glossary, and the symbol in that glossary entry links back to the first use. The TSV ledger records stable semantic IDs for validation; it is not a second manuscript. Generated LaTeX and temporary build products are intentionally excluded from version control. All five live figures are reproducible vector PDFs: their TikZ/PGFPlots sources and checked data live in `figures_tikz/`, and passing exports live in `notes/figures/tikz/`. Building the book does not require Dropbox or another repository.

## Verify the release

With LyX, LaTeX (including TikZ/PGFPlots), Poppler, Python 3 with `pypdf`, Perl, ripgrep, and Lean/Lake available, run:

```sh
bash scripts/check_book.sh
```

The command rebuilds and preflights all vector figures before exporting LyX, verifies the notation ledger against the canonical LyX source, compiles the PDF, checks every bidirectional first-use/glossary destination and link in that PDF, rejects raster images and unsafe fonts, builds the pinned Lean project together with the exact WGARP dependency, audits kernel assumptions and proof placeholders, validates the theorem-pair ledger, rejects restricted assessment files, and regenerates the chapter, duplication, and theorem indexes.

## Assessment policy

This public edition contains 65 question-only end-of-chapter problems, each with a stable identifier and a **Core**, **Proof**, or **Applied** label. Every chapter closes with **Part I: By hand** and **Part II: a named chapter use case and verified scale-up**; the designated case is always the final problem. The canonical prompts live in `problems/PROBLEM_BANK.md`, the 17 case pathways live in `problems/CHAPTER_PATHWAYS.tsv`, and both are injected reproducibly into the LyX manuscript. The music-and-concerts case is Problem 10.4 and is also available as the standalone handout linked above. Its fan-demand part uses Chapter 1; the complete case combines consumer demand, production costs, and concert pricing. Solutions, answer keys, examinations, and unreleased weekly handouts remain in the private instructor repository. Standalone student sheets are released as teaching views of the same stable chapter architecture.

The workhorse-demand material now includes CES derivations, elasticities, calibration, limiting cases, and compensated welfare comparisons, plus a translog expenditure model with explicit regularity checks. Eleven worked examples connect those families to Cobb-Douglas, linear, Leontief, Stone-Geary, and quasilinear demand. Problems 1.2--1.5 and 2.4--2.6 provide further practice.

## Status

This is the Fall 2026 public baseline: a complete, buildable textbook manuscript with unified notation, references, end-of-chapter problems, vector artwork, and a reproducible Lean verification layer. The book now begins with utility maximization, develops duality and welfare, and then treats revealed preference as the observable content and extension of the benchmark model. Abstract choice, risk, stochastic choice, costly attention, and aggregation follow in that order. The theorem-pair ledger tracks 24 reader/full pairs: the WGARP and WARP coalitional multi-utility pairs are migrated, 19 pairs remain planned, and 3 remain source-gated. The WGARP pair has a checked wrapper around the pinned external theorem; the WARP strict-CMU result is cited only and carries no Lean-verification claim. Later releases should preserve stable problem and theorem identifiers and must not change the book's notation or logical spine silently.
