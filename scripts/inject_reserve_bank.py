#!/usr/bin/env python3
"""Inject the question-only assessment reserve before the weekly plan."""

from __future__ import annotations

import argparse
import csv
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "problems" / "RESERVE_BANK.md"
MAP = ROOT / "problemsets" / "RESERVE_WEEKLY_MAP.tsv"
BOOK = ROOT / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"
START = "ECON803_RESERVE_START"
END = "ECON803_RESERVE_END"


@dataclass(frozen=True)
class ReserveProblem:
    identifier: str
    label: str
    title: str
    topic: str
    paragraphs: tuple[str, ...]


def normalize(text: str) -> str:
    return " ".join(text.split())


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


def ert_command(command: str) -> str:
    return (
        "\\begin_layout Standard\n"
        "\\begin_inset ERT\n"
        "status collapsed\n\n"
        "\\begin_layout Plain Layout\n\n"
        "\\backslash\n"
        f"{command}\n"
        "\\end_layout\n\n"
        "\\end_inset\n\n\n"
        "\\end_layout\n"
    )


def lyx_inline(text: str) -> str:
    parts: list[str] = []
    position = 0
    for match in re.finditer(r"\$(.+?)\$", text):
        parts.append(text[position:match.start()])
        parts.append(
            "\\begin_inset Formula $" + match.group(1) + "$\\end_inset\n"
        )
        position = match.end()
    parts.append(text[position:])
    return "".join(parts).strip()


def parse_bank() -> list[ReserveProblem]:
    problems: list[ReserveProblem] = []
    topic: str | None = None
    current: tuple[str, str, str] | None = None
    body: list[str] = []

    def finish() -> None:
        nonlocal current, body
        if current is None:
            return
        paragraphs = tuple(
            normalize(block)
            for block in re.split(r"\n\s*\n", "\n".join(body).strip())
            if block.strip()
        )
        if topic is None or not paragraphs:
            raise ValueError(f"reserve problem {current[0]} is incomplete")
        problems.append(ReserveProblem(*current, topic, paragraphs))
        current = None
        body = []

    for line in BANK.read_text(encoding="utf-8").splitlines():
        if line.startswith("# "):
            heading = line[2:].strip()
            if heading == "Additional practice reserve":
                continue
            finish()
            topic = heading
        elif line.startswith("## "):
            finish()
            fields = [value.strip() for value in line[3:].split("|", 2)]
            if len(fields) != 3:
                raise ValueError(f"malformed reserve heading: {line}")
            current = (fields[0], fields[1], fields[2])
        elif current is not None:
            body.append(line)
    finish()

    identifiers = [problem.identifier for problem in problems]
    if identifiers != [f"R{number:03d}" for number in range(1, len(problems) + 1)]:
        raise ValueError("reserve IDs must be consecutive R001, R002, ...")
    if len(identifiers) != len(set(identifiers)):
        raise ValueError("duplicate reserve ID")
    if any(problem.label not in {"Core", "Proof", "Applied"} for problem in problems):
        raise ValueError("unknown reserve problem label")
    for problem in problems:
        joined = " ".join(problem.paragraphs)
        if "**Part I — by hand.**" not in joined or "**Part II — verified scale-up.**" not in joined:
            raise ValueError(f"reserve problem {problem.identifier} lacks two-part structure")
    return problems


def parse_map(problem_ids: set[str]) -> dict[str, str]:
    with MAP.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        expected = ["set", "required_reserve_ids", "optional_reserve_ids"]
        if reader.fieldnames != expected:
            raise ValueError("unexpected reserve-map columns")
        rows = list(reader)
    if [row["set"] for row in rows] != [f"PS{i:02d}" for i in range(1, 14)]:
        raise ValueError("reserve map must contain consecutive PS01-PS13 rows")
    assignment: dict[str, str] = {}
    for row in rows:
        for field in ("required_reserve_ids", "optional_reserve_ids"):
            for identifier in (item.strip() for item in row[field].split(",")):
                if not identifier:
                    continue
                if identifier not in problem_ids:
                    raise ValueError(f"unknown reserve ID in weekly map: {identifier}")
                if identifier in assignment:
                    raise ValueError(f"reserve ID assigned more than once: {identifier}")
                assignment[identifier] = row["set"]
    missing = sorted(problem_ids - set(assignment))
    if missing:
        raise ValueError("unassigned reserve IDs: " + ", ".join(missing))
    return assignment


def pdf_metadata() -> str:
    return (
        "\\begin_layout Standard\n"
        "\\begin_inset ERT\n"
        "status collapsed\n\n"
        "\\begin_layout Plain Layout\n\n"
        "\\backslash\n"
        "markboth{ADDITIONAL PRACTICE RESERVE}{ADDITIONAL PRACTICE RESERVE}\n"
        "\\backslash\n"
        "addcontentsline{toc}{chapter}{Additional Practice Reserve}\n"
        "\\end_layout\n\n"
        "\\end_inset\n\n\n"
        "\\end_layout\n"
    )


def render(problems: list[ReserveProblem], weekly: dict[str, str]) -> str:
    parts = [
        layout("Chapter*", "Additional Practice Reserve"),
        marker(START),
        pdf_metadata(),
        layout(
            "Standard",
            "These question-only problems are cleaned and independently checked descendants of older Western/UWO and SFU assessments. Each begins with hand-solvable work and then supplies a controlled formal or computational scale-up. They supplement, rather than replace, the end-of-chapter problem sets. Solutions and source provenance are kept in the private instructor handbook.",
        ),
    ]
    previous_topic: str | None = None
    for problem in problems:
        if problem.topic != previous_topic:
            parts.append(layout("Section*", problem.topic))
            previous_topic = problem.topic
        heading = (
            "\\series bold\n"
            f"Problem {problem.identifier} [{problem.label}]. {problem.title}.\n"
            "\\series default"
        )
        parts.append(ert_command("begin{samepage}"))
        parts.append(layout("Exercise*", heading))
        parts.append(
            layout("Exercise*", f"Suggested weekly placement: {weekly[problem.identifier]}.")
        )
        parts.append(ert_command("end{samepage}"))
        for paragraph in problem.paragraphs:
            cleaned = paragraph.replace("**", "")
            parts.append(layout("Exercise*", lyx_inline(cleaned)))
    parts.append(marker(END))
    return "\n".join(parts)


def replace_or_insert(source: str, block: str) -> str:
    heading = "\\begin_layout Chapter*\nAdditional Practice Reserve\n\\end_layout\n"
    if START in source or END in source:
        if source.count(START) != 1 or source.count(END) != 1:
            raise ValueError("reserve markers are incomplete or duplicated")
        start = source.rfind(heading, 0, source.index(START))
        if start < 0:
            raise ValueError("reserve start marker has no chapter heading")
        end_marker = marker(END)
        end_start = source.find(end_marker, source.index(START))
        if end_start < 0:
            raise ValueError("reserve end marker is malformed")
        end = end_start + len(end_marker)
        return source[:start] + block + source[end:]

    anchor = "\\begin_layout Chapter*\nWeekly Problem Sets: Fall 2026\n\\end_layout\n"
    if source.count(anchor) != 1:
        raise ValueError("could not find the unique weekly-plan chapter")
    return source.replace(anchor, block + "\n" + anchor, 1)


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    problems = parse_bank()
    weekly = parse_map({problem.identifier for problem in problems})
    original = BOOK.read_text(encoding="utf-8")
    revised = replace_or_insert(original, render(problems, weekly))
    if args.check:
        if original != revised:
            raise SystemExit("additional practice reserve is not synchronized")
        print(f"Reserve matches {len(problems)} validated problems")
        return
    BOOK.write_text(revised, encoding="utf-8")
    print(f"Injected {len(problems)} reserve problems into {BOOK}")


if __name__ == "__main__":
    main()
