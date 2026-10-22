#!/usr/bin/env python3
"""One time native LyX relocation, preserving later live manuscript edits."""

from __future__ import annotations

import argparse
from pathlib import Path

from inject_problem_sets import marker, parse_problem_bank, strip_generated_blocks
from modernize_general_equilibrium import block, heading, label, p

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "notes/Microeconomics_1_notes_by_Victor_Aguiar.lyx"
STAMP = "ECON803_NICHE_CHAPTER_RELOCATED:1"
TITLE = "Niche Consumption and Product Space"

OLD_ROADMAP = "Part V treats sequential trade, matching and computable general equilibrium."
NEW_ROADMAP = "Part V begins with niche consumption and product space, connecting consumer theory to the preceding equilibrium analysis, then treats sequential trade, matching and computable general equilibrium."


def validate(source: str) -> None:
    tokens = (heading("Chapter", TITLE), 'name "chap:niche-consumption"', STAMP)
    for token in tokens:
        if source.count(token) != 1:
            raise ValueError(f"missing or repeated niche chapter token: {token}")
    ge = source.index(heading("Chapter", "General Equilibrium"))
    part = source.index(heading("Part", "Advanced Equilibrium Applications"))
    niche = source.index(heading("Chapter", TITLE))
    sequential = source.index(heading("Chapter", "Sequential Trade"))
    if not ge < part < niche < sequential:
        raise ValueError("niche chapter must follow GE and precede advanced applications")
    if source.count(heading("Section", "The Many-Product Consumer")) != 1:
        raise ValueError("the existing many product material must be preserved once")


def rewrite(source: str) -> str:
    if STAMP in source:
        validate(source)
        return source
    chapters = parse_problem_bank(ROOT / "problems/PROBLEM_BANK.md")
    source = strip_generated_blocks(source, chapters)
    start = source.index(heading("Section", "The Many-Product Consumer"))
    stop = source.index(heading("Part", "Production and Equilibrium"), start)
    material = source[start:stop].strip() + "\n\n"
    # Promote the existing subsections without changing their arguments,
    # notation anchors, citations or proofs.
    material = material.replace("\\begin_layout Subsection\n", "\\begin_layout Section\n")
    pointer = p("A representative consumer can hide an important distinction: spending may concentrate within each household while becoming less concentrated across the whole market. Chapter [[ref:chap:niche-consumption]] returns to this issue after general equilibrium, using product space, shopping baskets and capacity constrained assignment to connect the earlier consumer models.")
    source = source[:start] + pointer + source[stop:]
    chapter = "".join([
        block("Chapter", TITLE),
        label("chap:niche-consumption"),
        marker(STAMP),
        p("The preceding chapter connects households and firms through prices and resource constraints for a fixed finite list of commodities. We now ask how that description should change when products are numerous, differentiated and continually replaced. Neiman and Vavra's evidence motivates the question: household concentration and aggregate concentration need not move together. The task is to choose the right commodity and demand objects before drawing welfare or substitution conclusions."),
        p("This is a research synthesis, not another equilibrium existence theorem. A continuum of differentiated goods requires its own topological and economic assumptions; the finite commodity theorem in Chapter [[ref:chap:general-equilibrium]] does not automatically establish a continuum equilibrium. The chapter separates individual product choice, basket demand and assignment under capacity, then returns to the empirical evidence and its interpretation."),
        material,
        block("Section", "Reading and synthesis"),
        p("Begin with the distinction between the available catalog, consideration and positive purchases. Then compare the local diversion example with logit and recognize a finite basket as an atomic nonnegative measure within the broader formulation. The matching interpretation applies only after capacities or fixed supply marginals are imposed. These are different economic models, not interchangeable names for a large catalog."),
        p("This chapter creates no additional weekly assignment. The companion practice book connects the synthesis to existing exercises on revealed preference, logit, aggregation, redistribution, equilibrium data and matching. Finite computations can illustrate the continuum formulation, but they do not prove its analytic claims. Problem identifiers remain the permanent labels of the original bank."),
    ])
    target = heading("Chapter", "Sequential Trade")
    source = source.replace(target, chapter + target, 1)
    source = source.replace(OLD_ROADMAP, NEW_ROADMAP, 1)
    source = source.replace("Every substantive chapter ends with a two part problem program.", "Every core teaching chapter ends with a two part problem program. The research synthesis on niche consumption instead supplies a reading guide connecting existing exercises.", 1)
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
            raise SystemExit("niche chapter relocation is pending")
        print("niche consumption research chapter is correctly placed")
    elif old != new:
        BOOK.write_text(new, encoding="utf-8")
        print(BOOK)


if __name__ == "__main__":
    main()
