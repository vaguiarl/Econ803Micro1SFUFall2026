# ECON 803 Practice Book

This directory contains the standalone, question-only practice book for Fall 2026.

- `ECON803_Practice_Book_Fall2026.pdf`: the student-facing edition.
- `ECON803_Practice_Book_Fall2026.lyx`: the editable native LyX source.

The book contains all 65 canonical chapter problems and all 10 additional-practice reserve problems. It begins with the thirteen-week practice map and preserves the stable identifiers used by the textbook and weekly handouts. Chapter use cases remain at the end of their chapters.

Question text is generated from `../../problems/PROBLEM_BANK.md` and `../../problems/RESERVE_BANK.md`; those banks remain the source of record. Solutions, answer keys, source provenance, and instructor notes are deliberately excluded and remain in the private instructor repository.

Regenerate the LyX source with:

```sh
python3 scripts/build_practice_book.py
```

Build and preflight the PDF with:

```sh
bash scripts/build_practice_book.sh
```
