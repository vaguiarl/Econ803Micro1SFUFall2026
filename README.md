# Microeconomic Theory I — Fall 2026

This repository contains the public, student-facing first edition of Victor Aguiar's graduate microeconomic theory text for Simon Fraser University. The book is designed for the role that *Microeconomic Theory* by Mas-Colell, Whinston, and Green has traditionally played: a rigorous common language for graduate theory, complemented by modern revealed-preference, behavioral, random-choice, and computational material.

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
- Reader/full theorem-pair plan: [`THEOREM_STAR_PLAN.md`](THEOREM_STAR_PLAN.md)
- Figure, provenance, and rights audit: [`FIGURE_AUDIT.md`](FIGURE_AUDIT.md)
- Canonical question-only problem bank: [`problems/PROBLEM_BANK.md`](problems/PROBLEM_BANK.md)
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

This public edition contains 55 question-only end-of-chapter problems, each with a stable identifier and a **Core**, **Proof**, or **Applied** label. The canonical prompts live in `problems/PROBLEM_BANK.md` and are injected reproducibly into the LyX manuscript. Solutions, answer keys, examinations, and unreleased weekly handouts remain in the private instructor repository. Standalone student sheets will be released one at a time from the same stable problem bank.

## Status

This is the Fall 2026 public baseline: a complete, buildable textbook manuscript with unified notation, references, end-of-chapter problems, vector artwork, and a reproducible Lean verification layer. The proposed starred reader-theorem/full-appendix architecture is mapped and mechanically validated, but the 22 theorem pairs have not yet been migrated into the LyX manuscript. Later releases should preserve stable problem and theorem identifiers and must not change the book's notation or logical spine silently.
