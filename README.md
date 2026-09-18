# Microeconomic Theory I — Fall 2026

This repository contains the public, book-only first edition of Victor Aguiar's graduate microeconomic theory text for Simon Fraser University. The book is designed for the role that *Microeconomic Theory* by Mas-Colell, Whinston, and Green has traditionally played: a rigorous common language for graduate theory, complemented by modern revealed-preference, behavioral, random-choice, and computational material.

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
- Mathematical verification ledger: [`formal/COVERAGE.md`](formal/COVERAGE.md)
- Backward editorial and formalization plan: [`EDITORIAL_AUDIT.md`](EDITORIAL_AUDIT.md)

The LyX file is the authoritative text. Generated LaTeX and temporary build products are intentionally excluded from version control. All figures required by the manuscript are stored under `notes/figures/`; building the book does not require Dropbox or another repository.

## Verify the release

With LyX, LaTeX, Perl, ripgrep, and Lean available, run:

```sh
bash scripts/check_book.sh
```

To include the separately maintained, already kernel-checked WGARP/Afriat library:

```sh
WGARP_LEAN_DIR=/path/to/wgarp_final_revision bash scripts/check_book.sh
```

The command rebuilds the PDF, compiles every local Lean module, optionally builds the external WGARP project, rejects proof placeholders and restricted assessment files, and regenerates the chapter, duplication, and theorem indexes.

## Assessment policy

This first public edition contains no problem sets, solutions, answer keys, or examinations. Those materials remain in the private Fall 2024 instructor repository. Student problem sets will be revised and released here one at a time; solutions and unreleased assessments will remain private.

## Status

This is the Fall 2026 version 0.1 baseline: a complete, buildable textbook manuscript with a unified editorial and verification framework. Subsequent releases can add citations, examples, and problem sets without changing the book's notation or logical spine silently.
