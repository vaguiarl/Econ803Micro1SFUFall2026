#!/usr/bin/env python3
"""Insert the production bridge once, then preserve the live LyX version."""

from __future__ import annotations

import argparse

from inject_problem_sets import marker
from modern_production_material import STAMP, modern_production_blocks
from modernize_general_equilibrium import BOOK, heading


def validate(source: str) -> None:
    start = source.index(heading("Chapter", "Theory of the Firm"))
    stop = source.index(heading("Chapter", "Competitive Markets and Partial Equilibrium"), start)
    chapter = source[start:stop]
    for token in (STAMP, 'name "sec:production-identification"', 'key "aguiarkashaevallen2023"', 'key "gandhinavarrorivers2020"'):
        if chapter.count(token) != 1:
            raise ValueError(f"missing or repeated production bridge token: {token}")
    if "ECON803_PROBLEMS_START:theory-of-the-firm" in chapter:
        if chapter.index(STAMP) > chapter.index("ECON803_PROBLEMS_START:theory-of-the-firm"):
            raise ValueError("production exposition must precede chapter problems")


def rewrite(source: str) -> str:
    if STAMP in source:
        validate(source)
        return source
    start = source.index(heading("Chapter", "Theory of the Firm"))
    end = source.index(heading("Chapter", "Competitive Markets and Partial Equilibrium"), start)
    chapter = source[start:end]
    if "ECON803_PROBLEMS_START:theory-of-the-firm" in chapter:
        token = source.index("ECON803_PROBLEMS_START:theory-of-the-firm", start)
        end = source.rfind("\\begin_layout Standard\n", start, token)
    source = source[:end] + marker(STAMP) + "\n" + modern_production_blocks() + source[end:]
    validate(source)
    return source


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    old = BOOK.read_text(encoding="utf-8")
    new = rewrite(old)
    if args.check:
        if old != new:
            raise SystemExit("production modernization is pending")
        print("modern production bridge is present in the live LyX source")
    elif old != new:
        BOOK.write_text(new, encoding="utf-8")
        print(BOOK)


if __name__ == "__main__":
    main()
