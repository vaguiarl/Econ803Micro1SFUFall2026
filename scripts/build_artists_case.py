#!/usr/bin/env python3
"""Generate the question-only artists handout from the public canonical bank."""

from __future__ import annotations

import argparse
import re
from pathlib import Path

from inject_problem_sets import lyx_inline, parse_problem_bank

ROOT = Path(__file__).resolve().parents[1]
TARGET = ROOT / "problems/case_studies/Artists_Music_and_Concerts.lyx"


def build() -> str:
    bank = parse_problem_bank(ROOT / "problems/PROBLEM_BANK.md")
    matches = [p for c in bank for p in c.problems if p.identifier == "10.4"]
    if len(matches) != 1:
        raise ValueError("artists problem 10.4 missing or ambiguous")
    problem = matches[0]
    book = (ROOT / "notes/Microeconomics_1_notes_by_Victor_Aguiar.lyx").read_text()
    header = book[:book.index("\\begin_body")]
    header = header.replace("\\textclass book", "\\textclass article")
    header = header.replace("theorems-chap\n", "")
    header = re.sub(r"\\begin_preamble.*?\\end_preamble", lambda _: "\\begin_preamble\n\\end_preamble", header, flags=re.S)
    header = header.replace("\\spacing double", "\\spacing onehalf")
    header = header.replace("\\secnumdepth 3", "\\secnumdepth 0")
    body = ["\\begin_body\n"]
    for kind, text in [
        ("Title", "The Economics of Superstars: Music Sales and Concerts"),
        ("Author", "Victor H. Aguiar"),
        ("Date", "ECON 803, Fall 2026"),
        ("Standard", "Problem 10.4 [Applied]. Questions only. Part I uses consumer theory from Chapter 1; Parts II through IV combine cost minimization and monopoly pricing. This handout uses the same questions as the textbook."),
    ]:
        body.append(f"\\begin_layout {kind}\n{text}\n\\end_layout\n\n")
    for paragraph in problem.paragraphs:
        if paragraph.startswith("Part "):
            part, title, paragraph = paragraph.split(". ", 2)
            body.append("\\begin_layout Section*\n" + part + ". " + title + "\n\\end_layout\n\n")
        body.append("\\begin_layout Standard\n" + lyx_inline(paragraph) + "\n\\end_layout\n\n")
    body.append("\\end_body\n\\end_document\n")
    return header + "\n" + "".join(body)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    source = build()
    if args.check:
        if not TARGET.exists() or TARGET.read_text() != source:
            raise SystemExit("artists handout is not synchronized with the bank")
        print("artists handout matches canonical Problem 10.4")
    else:
        TARGET.parent.mkdir(parents=True, exist_ok=True)
        TARGET.write_text(source)
        print(TARGET)


if __name__ == "__main__":
    main()
