#!/usr/bin/env python3
"""Synchronize the native LyX notation glossary from the canonical TSV ledger.

The generated material is ordinary LyX content.  It therefore remains editable
in LyX, while this script makes the repetitive entries reproducible and keeps
their PDF destinations synchronized with ``editorial/notation/glossary.tsv``.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import OrderedDict
from pathlib import Path


START_MARKER = "ECON803_NOTATION_GLOSSARY_START"
END_MARKER = "ECON803_NOTATION_GLOSSARY_END"

CATEGORY_ORDER = (
    "Sets and indices",
    "Operators",
    "Optimization",
    "Choice and preference",
    "Revealed preference",
    "Consumer theory",
    "Behavioral demand",
    "Choice under uncertainty",
    "Probability",
    "Aggregation",
    "Discrete choice",
    "Firm theory",
    "Equilibrium",
    "Sequential trade",
    "Matching",
    "Order theory",
)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--lyx", required=True, type=Path)
    parser.add_argument("--ledger", required=True, type=Path)
    return parser.parse_args()


def marker_note(marker: str) -> str:
    return f"""\\begin_layout Standard
\\begin_inset Note Note
status collapsed

\\begin_layout Plain Layout
{marker}
\\end_layout

\\end_inset


\\end_layout
"""


def inline_lyx(text: str) -> str:
    """Convert ``$...$`` spans in ledger prose to native LyX formula insets."""

    pieces: list[str] = []
    cursor = 0
    for match in re.finditer(r"\$([^$]+)\$", text):
        pieces.append(text[cursor : match.start()])
        # LyX ignores ordinary prose that follows an inline ``\\end_inset``
        # on the same source line.  End the source line here so punctuation,
        # later formulae, and the generated scope clause all survive export.
        pieces.append(
            f"\\begin_inset Formula ${match.group(1)}$\\end_inset\n"
        )
        cursor = match.end()
    pieces.append(text[cursor:])
    return "".join(pieces)


def entry(row: dict[str, str]) -> str:
    symbol = row["symbol"]
    if not (symbol.startswith("$") and symbol.endswith("$")):
        raise ValueError(f"symbol for {row['id']} must be enclosed in $...$: {symbol}")
    symbol_body = symbol[1:-1]
    scope = row["scope"]
    definition = inline_lyx(row["definition"])
    return f"""\\begin_layout Description
\\begin_inset Formula $\\notationdef{{{row['id']}}}{{{symbol_body}}}$
\\end_inset

 {definition} Scope: {scope}.
\\end_layout

"""


def glossary_block(rows: list[dict[str, str]]) -> str:
    categories: OrderedDict[str, list[dict[str, str]]] = OrderedDict()
    for row in rows:
        categories.setdefault(row["category"], []).append(row)

    unknown_categories = set(categories).difference(CATEGORY_ORDER)
    if unknown_categories:
        raise ValueError(
            "unregistered glossary categories: "
            + ", ".join(sorted(unknown_categories))
        )

    chunks = [
        """\\begin_layout Chapter
Glossary of Symbols
\\end_layout

""",
        marker_note(START_MARKER),
        """\\begin_layout Standard

\\begin_inset CommandInset label
LatexCommand label
name "app:notation-glossary"

\\end_inset
\\end_layout

\\begin_layout Standard
This glossary records the book's persistent notation.  Each blue symbol links back to its first substantive use in the text.  There, the blue first use links here.  A symbol described as scoped may be reused only after the new local meaning is stated explicitly.
\\end_layout

""",
    ]
    for category in CATEGORY_ORDER:
        category_rows = categories.get(category)
        if not category_rows:
            continue
        chunks.append(f"\\begin_layout Section\n{category}\n\\end_layout\n\n")
        chunks.extend(entry(row) for row in category_rows)
    chunks.append(marker_note(END_MARKER))
    return "".join(chunks)


def load_rows(path: Path) -> list[dict[str, str]]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = list(csv.DictReader(handle, delimiter="\t"))
    if not rows:
        raise ValueError("notation ledger is empty")
    return rows


def main() -> int:
    args = parse_args()
    source = args.lyx.read_text(encoding="utf-8")
    generated = glossary_block(load_rows(args.ledger))

    start = source.find(START_MARKER)
    end = source.find(END_MARKER)
    if (start == -1) != (end == -1):
        raise ValueError("only one notation-glossary marker is present")

    # Repair the legacy ordering used by the first generator revision.  That
    # revision put START before the Glossary chapter, so the problem injector
    # could place the Appendix A exercises between the two markers.  Remove
    # only the detached START note and the old glossary-to-bibliography tail;
    # the exercises between them remain untouched.
    if start != -1:
        preceding_chapter = source.rfind("\\begin_layout Chapter\n", 0, start)
        glossary_title = "\\begin_layout Chapter\nGlossary of Symbols\n\\end_layout"
        glossary_chapter = source.find(glossary_title, start)
        if (
            preceding_chapter != -1
            and not source.startswith(glossary_title, preceding_chapter)
            and glossary_chapter != -1
        ):
            detached_start = marker_note(START_MARKER)
            detached_at = source.find(detached_start)
            if detached_at == -1:
                raise ValueError("cannot delimit the detached legacy START marker")
            source = (
                source[:detached_at]
                + source[detached_at + len(detached_start) :]
            )
            glossary_chapter = source.find(glossary_title)
            bibliography = source.find("\\begin_inset CommandInset bibtex")
            bibliography_layout = source.rfind(
                "\\begin_layout Standard", glossary_chapter, bibliography
            )
            if glossary_chapter == -1 or bibliography_layout == -1:
                raise ValueError("cannot delimit the legacy glossary tail")
            source = source[:glossary_chapter] + source[bibliography_layout:]
            start = end = -1

    if start != -1:
        block_start = source.rfind("\\begin_layout Chapter\n", 0, start)
        end_note = marker_note(END_MARKER)
        end_note_start = source.find(end_note, start)
        if block_start == -1 or end_note_start == -1:
            raise ValueError("cannot delimit the existing notation glossary")
        block_end = end_note_start + len(end_note)
        if block_end < len(source) and source[block_end] == "\n":
            block_end += 1
        updated = source[:block_start] + generated + source[block_end:]
    else:
        bibliography = source.find("\\begin_inset CommandInset bibtex")
        if bibliography == -1:
            raise ValueError("cannot find the bibliography inset")
        insert_at = source.rfind("\\begin_layout Standard", 0, bibliography)
        if insert_at == -1:
            raise ValueError("cannot find the bibliography layout")
        updated = source[:insert_at] + generated + "\n" + source[insert_at:]

    args.lyx.write_text(updated, encoding="utf-8")
    print(f"synchronized {len(load_rows(args.ledger))} notation entries")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
