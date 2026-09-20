#!/usr/bin/env python3
"""Reorder the risk, stochastic-choice, attention, and aggregation chapters.

The script is deliberately narrow: it moves complete LyX blocks, so theorem
labels, citations, figures, and injected problem markers travel with their
original content.  Run with ``--check`` to verify whether the rewrite is still
needed and with ``--apply`` to update the canonical LyX source.
"""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"


def layout(kind: str, title: str) -> str:
    return f"\\begin_layout {kind}\n{title}\n\\end_layout"


OLD_PART_II = layout("Part", "Choice Beyond the Benchmark Model")
OLD_PART_III = layout("Part", "Aggregation and Random Choice")
PRODUCTION_PART = layout("Part", "Production and Equilibrium")

BEHAVIOR = layout(
    "Chapter", "Behavioral Economics: Sparse-Max and Rational Inattention"
)
UNCERTAINTY = layout("Chapter", "Choice under Uncertainty")
AGGREGATE = layout("Chapter", "Aggregate Demand")
RANDOM_UTILITY = layout("Chapter", "Discrete Choice and Random Utility")

NEW_PART_II = layout("Part", "Risk, Stochastic Choice, and Attention")
NEW_PART_III = layout("Part", "Aggregation and Markets")


def require_once(text: str, marker: str) -> int:
    count = text.count(marker)
    if count != 1:
        raise ValueError(f"expected one occurrence of {marker!r}, found {count}")
    return text.index(marker)


def section_title(block: str) -> str:
    prefix = "\\begin_layout Section\n"
    if not block.startswith(prefix):
        raise ValueError("section block does not begin with a Section layout")
    return block[len(prefix) : block.index("\n\\end_layout", len(prefix))]


def reorder_sections(chapter: str, desired: list[str]) -> str:
    marker = "\\begin_layout Section\n"
    first = chapter.find(marker)
    if first < 0:
        raise ValueError("chapter has no sections")
    header = chapter[:first]
    heading_starts: list[int] = []
    cursor = first
    while cursor >= 0:
        heading_starts.append(cursor)
        cursor = chapter.find(marker, cursor + len(marker))
    titles = [
        chapter[
            start + len(marker) : chapter.index("\n\\end_layout", start + len(marker))
        ]
        for start in heading_starts
    ]
    starts = list(heading_starts)
    for index, title in enumerate(titles):
        if title != "Problems":
            continue
        lower = heading_starts[index - 1] if index else 0
        marker_at = chapter.rfind("ECON803_PROBLEMS_START:", lower, heading_starts[index])
        if marker_at < 0:
            raise ValueError("Problems section is missing its generated START marker")
        outer = chapter.rfind("\\begin_layout Standard\n", lower, marker_at)
        if outer < 0:
            raise ValueError("cannot locate the problem START marker layout")
        starts[index] = outer
    blocks = [
        chapter[start : starts[i + 1] if i + 1 < len(starts) else len(chapter)]
        for i, start in enumerate(starts)
    ]
    by_title = dict(zip(titles, blocks, strict=True))
    if set(by_title) != set(desired):
        missing = sorted(set(desired) - set(by_title))
        extra = sorted(set(by_title) - set(desired))
        raise ValueError(f"section mismatch; missing={missing}, extra={extra}")
    return header + "".join(by_title[title] for title in desired)


def rewrite(text: str) -> str:
    if NEW_PART_II in text:
        if any(marker in text for marker in (OLD_PART_II, OLD_PART_III)):
            raise ValueError("source contains both old and new part structures")
        return text

    part_ii = require_once(text, OLD_PART_II)
    behavior = require_once(text, BEHAVIOR)
    uncertainty = require_once(text, UNCERTAINTY)
    part_iii = require_once(text, OLD_PART_III)
    aggregate = require_once(text, AGGREGATE)
    random_utility = require_once(text, RANDOM_UTILITY)
    production = require_once(text, PRODUCTION_PART)

    if not (
        part_ii < behavior < uncertainty < part_iii < aggregate < random_utility < production
    ):
        raise ValueError("unexpected chapter order in choice-extension block")

    behavior_block = text[behavior:uncertainty]
    uncertainty_block = text[uncertainty:part_iii]
    aggregate_block = text[aggregate:random_utility]
    random_block = text[random_utility:production]

    uncertainty_block = uncertainty_block.replace(
        UNCERTAINTY, layout("Chapter", "Expected Utility and Risk"), 1
    )
    uncertainty_block = reorder_sections(
        uncertainty_block,
        [
            "Primitives",
            "Model and expected utility",
            "Independence Axiom",
            "Representation Theorem",
            "Recoverability",
            "The Allais Paradox",
            "Attitudes towards Risk",
            "Stochastic dominance on a finite prize set",
            "Application:\n Demand for a Risky Asset\n",
            "Revealed Preference of Expected Utility under Concavity",
            "Experimental Evidence",
            "Measuring Risk Aversion in the Lab",
            "Expected Utility for Infinite Sets",
            "Stochastic dominance for general distributions",
            "Problems",
        ],
    )
    uncertainty_block = uncertainty_block.replace(
        layout("Section", "Application:\n Demand for a Risky Asset\n"),
        layout("Section", "Portfolio Choice: Demand for a Risky Asset"),
        1,
    )

    random_block = random_block.replace(
        RANDOM_UTILITY, layout("Chapter", "Stochastic Choice and Random Utility"), 1
    )
    random_block = reorder_sections(
        random_block,
        [
            "Choice from a finite menu",
            "Random utility",
            "Multinomial logit and IIA",
            "Random expected utility",
            "Attributes and consumer surplus",
            "Problems",
        ],
    )
    random_block = random_block.replace(
        layout("Section", "Choice from a finite menu"),
        layout("Section", "Stochastic Choice on a Finite Universe"),
        1,
    )

    behavior_block = behavior_block.replace(
        BEHAVIOR, layout("Chapter", "Limited Attention and Costly Information"), 1
    )
    behavior_block = behavior_block.replace(
        layout("Section", "Endogenizing Attention"),
        layout("Section", "A Gaussian Signal Example"),
        1,
    )

    aggregate_block = aggregate_block.replace(
        AGGREGATE,
        layout("Chapter", "Aggregate Demand and Representative Consumers"),
        1,
    )

    rebuilt = (
        NEW_PART_II
        + "\n\n"
        + uncertainty_block
        + random_block
        + behavior_block
        + NEW_PART_III
        + "\n\n"
        + aggregate_block
    )
    return text[:part_ii] + rebuilt + text[production:]


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    original = BOOK.read_text()
    revised = rewrite(original)
    changed = revised != original
    if args.check:
        if changed:
            raise SystemExit("choice-extension restructure is pending")
        print("choice-extension structure is current")
        return
    if changed:
        BOOK.write_text(revised)
        print(f"updated {BOOK}")
    else:
        print("no changes needed")


if __name__ == "__main__":
    main()
