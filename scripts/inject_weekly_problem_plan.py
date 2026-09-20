#!/usr/bin/env python3
"""Inject the dated, question-only weekly plan into the LyX book.

The actual question text remains in the generated end-of-chapter problem
blocks. This index appears at the end of the main text and points to stable
problem identifiers without duplicating questions or case studies.
"""

from __future__ import annotations

import argparse
import csv
import datetime as dt
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
PLAN = ROOT / "problemsets" / "WEEKLY_RELEASE_PLAN.tsv"
BOOK = ROOT / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"
BANK = ROOT / "problems" / "PROBLEM_BANK.md"
PATHWAYS = ROOT / "problems" / "CHAPTER_PATHWAYS.tsv"
START = "ECON803_WEEKLY_PLAN_START"
END = "ECON803_WEEKLY_PLAN_END"


def marker(name: str) -> str:
    return (
        "\\begin_layout Standard\n"
        "\\begin_inset Note Note\n"
        "status collapsed\n\n"
        "\\begin_layout Plain Layout\n"
        f"{name}\n"
        "\\end_layout\n\n"
        "\\end_inset\n\n\n"
        "\\end_layout\n"
    )


def layout(kind: str, value: str) -> str:
    return f"\\begin_layout {kind}\n{value}\n\\end_layout\n"


def schedule_pdf_metadata() -> str:
    return (
        "\\begin_layout Standard\n"
        "\\begin_inset ERT\n"
        "status collapsed\n\n"
        "\\begin_layout Plain Layout\n\n"
        "\\backslash\n"
        "markboth{WEEKLY PROBLEM SETS: FALL 2026}{WEEKLY PROBLEM SETS: FALL 2026}\n"
        "\\backslash\n"
        "addcontentsline{toc}{chapter}{Weekly Problem Sets: Fall 2026}\n"
        "\\end_layout\n\n"
        "\\end_inset\n\n\n"
        "\\end_layout\n"
    )


def read_plan() -> list[dict[str, str]]:
    with PLAN.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        expected = [
            "set",
            "meeting_date",
            "due_date",
            "topic",
            "required_ids",
            "extension_ids",
            "archive_sources",
            "status",
        ]
        if reader.fieldnames != expected:
            raise ValueError("unexpected weekly-plan columns")
        rows = list(reader)
    if len(rows) != 13:
        raise ValueError("the Fall 2026 plan must contain 13 weekly sets")
    assigned: list[str] = []
    for number, row in enumerate(rows, start=1):
        if row["set"] != f"PS{number:02d}":
            raise ValueError("weekly sets must be consecutive PS01-PS13")
        meeting = dt.date.fromisoformat(row["meeting_date"])
        due = dt.date.fromisoformat(row["due_date"])
        if meeting.weekday() != 4 or due <= meeting:
            raise ValueError(f"invalid meeting/due dates for {row['set']}")
        for field in ("required_ids", "extension_ids"):
            assigned.extend(
                item.strip() for item in row[field].split(",") if item.strip()
            )

    bank_ids = re.findall(
        r"^##\s+((?:[0-9]+|A)\.[0-9]+)\s+\|",
        BANK.read_text(encoding="utf-8"),
        flags=re.MULTILINE,
    )
    with PATHWAYS.open(encoding="utf-8", newline="") as handle:
        cases = {row["case_id"] for row in csv.DictReader(handle, delimiter="\t")}
    if len(assigned) != len(set(assigned)):
        raise ValueError("a problem is assigned to more than one weekly set")
    unknown = sorted(set(assigned) - set(bank_ids))
    if unknown:
        raise ValueError("unknown weekly problem IDs: " + ", ".join(unknown))
    assigned_cases = sorted(set(assigned) & cases)
    if assigned_cases:
        raise ValueError("weekly plan includes case IDs: " + ", ".join(assigned_cases))
    expected = set(bank_ids) - cases
    missing = sorted(expected - set(assigned))
    if missing:
        raise ValueError("unassigned non-case problem IDs: " + ", ".join(missing))
    return rows


def render(rows: list[dict[str, str]]) -> str:
    parts = [
        layout("Chapter*", "Weekly Problem Sets: Fall 2026"),
        marker(START),
        schedule_pdf_metadata(),
        layout(
            "Standard",
            "The end-of-chapter questions are the source of record. The weekly sets below are question-only release views for ECON 803; chapter case studies are assigned separately. Required problems are the board-scale core, while extensions supply a proof or formal/computational bridge. Solutions are not included in the public book.",
        ),
    ]
    for row in rows:
        meeting = dt.date.fromisoformat(row["meeting_date"])
        due = dt.date.fromisoformat(row["due_date"])
        parts.append(layout("Section*", f"{row['set']}: {row['topic']}"))
        parts.append(
            layout(
                "Standard",
                f"Meeting {meeting.strftime('%B')} {meeting.day}, {meeting.year}; due {due.strftime('%B')} {due.day}, {due.year}.",
            )
        )
        parts.append(layout("Description", f"Required {row['required_ids']}"))
        parts.append(
            layout("Description", f"Extension {row['extension_ids'] or 'None'}")
        )
    parts.extend(
        [
            layout(
                "Standard",
                "PS13 is formative because classes end on December 7. Order-theory exercises are referenced where useful but remain in the mathematical appendix.",
            ),
            marker(END),
        ]
    )
    return "\n".join(parts)


def replace_or_insert(source: str, block: str) -> str:
    if START in source or END in source:
        if source.count(START) != 1 or source.count(END) != 1:
            raise ValueError("weekly-plan markers are incomplete or duplicated")
        heading_block = (
            "\\begin_layout Chapter*\n"
            "Weekly Problem Sets: Fall 2026\n"
            "\\end_layout\n"
        )
        start = source.rfind(heading_block, 0, source.index(START))
        if start < 0:
            # One-time migration from the original marker-before-heading order.
            heading = source.find(heading_block, source.index(START))
            if heading < 0:
                raise ValueError("weekly-plan start marker has no chapter heading")
            start = source.rfind(
                "\\begin_layout Standard", 0, source.index(START)
            )
        end_marker = marker(END)
        end_marker_start = source.find(end_marker, source.index(START))
        if end_marker_start < 0:
            raise ValueError("weekly-plan end marker is malformed")
        end = end_marker_start + len(end_marker)
        # Migrate files written by the original replacement routine, which
        # stopped at the inner Plain Layout and could leave one or more outer
        # Note/Layout tails behind.
        duplicate_tail = "\n\\end_inset\n\n\n\\end_layout\n"
        while source.startswith(duplicate_tail, end):
            end += len(duplicate_tail)
        return source[:start] + block + source[end:]

    anchor = (
        "\\begin_layout Standard\n"
        "\\begin_inset ERT\n"
        "status open\n\n"
        "\\begin_layout Plain Layout\n\n"
        "\\backslash\n"
        "appendix"
    )
    if source.count(anchor) != 1:
        raise ValueError("could not find the unique appendix anchor")
    return source.replace(anchor, block + "\n" + anchor, 1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    rows = read_plan()
    source = BOOK.read_text(encoding="utf-8")
    revised = replace_or_insert(source, render(rows))
    if args.check:
        if source != revised:
            raise SystemExit("weekly problem-set plan is not synchronized")
        print(f"Weekly plan matches {len(rows)} validated sets")
        return
    BOOK.write_text(revised, encoding="utf-8")
    print(f"Injected {len(rows)} weekly sets into {BOOK}")


if __name__ == "__main__":
    main()
