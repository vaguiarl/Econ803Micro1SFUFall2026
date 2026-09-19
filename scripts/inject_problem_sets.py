#!/usr/bin/env python3
"""Inject the public problem bank into the textbook LyX source.

The problem bank is deliberately separate from the solutions handbook.  This
script is idempotent: generated blocks are marked with non-exported LyX notes
and replaced on the next run.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


@dataclass(frozen=True)
class Problem:
    identifier: str
    level: str
    title: str
    paragraphs: tuple[str, ...]


@dataclass(frozen=True)
class ChapterProblems:
    chapter: str
    problems: tuple[Problem, ...]


def normalize_space(text: str) -> str:
    return " ".join(text.split())


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def parse_problem_bank(path: Path) -> list[ChapterProblems]:
    chapters: list[ChapterProblems] = []
    chapter_name: str | None = None
    problems: list[Problem] = []
    current_meta: tuple[str, str, str] | None = None
    current_lines: list[str] = []

    def finish_problem() -> None:
        nonlocal current_meta, current_lines
        if current_meta is None:
            return
        blocks = tuple(
            normalize_space(block)
            for block in re.split(r"\n\s*\n", "\n".join(current_lines).strip())
            if block.strip()
        )
        if not blocks:
            raise ValueError(f"problem {current_meta[0]} has no text")
        problems.append(Problem(*current_meta, paragraphs=blocks))
        current_meta = None
        current_lines = []

    def finish_chapter() -> None:
        nonlocal problems
        finish_problem()
        if chapter_name is not None:
            chapters.append(ChapterProblems(chapter_name, tuple(problems)))
        problems = []

    for raw_line in path.read_text(encoding="utf-8").splitlines():
        if raw_line.startswith("# "):
            heading = raw_line[2:].strip()
            if heading == "Publication problem bank":
                continue
            finish_chapter()
            chapter_name = heading
            continue
        if raw_line.startswith("## "):
            if chapter_name is None:
                raise ValueError("problem appears before a chapter heading")
            finish_problem()
            fields = [field.strip() for field in raw_line[3:].split("|", 2)]
            if len(fields) != 3:
                raise ValueError(f"malformed problem heading: {raw_line}")
            current_meta = (fields[0], fields[1], fields[2])
            continue
        if current_meta is not None:
            current_lines.append(raw_line)

    finish_chapter()
    if not chapters:
        raise ValueError("no chapter problem sets found")
    return chapters


def lyx_inline(text: str) -> str:
    pieces: list[str] = []
    position = 0
    for match in re.finditer(r"\$(.+?)\$", text):
        pieces.append(text[position : match.start()])
        # End the source line immediately after the inline formula inset.  LyX
        # keeps the preceding ordinary space, while later prose starts on the
        # next source line instead of being swallowed after ``\\end_inset``.
        pieces.append(
            "\\begin_inset Formula $"
            + match.group(1)
            + "$\\end_inset\n"
        )
        position = match.end()
    pieces.append(text[position:])
    return "".join(pieces).strip()


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


def separator() -> str:
    return (
        "\\begin_layout Standard\n"
        "\\begin_inset Separator parbreak\n"
        "\\end_inset\n\n\n"
        "\\end_layout\n"
    )


def problem_block(chapter: ChapterProblems) -> str:
    chapter_slug = slug(chapter.chapter)
    parts = [marker(f"ECON803_PROBLEMS_START:{chapter_slug}")]
    parts.extend(
        [
            "\\begin_layout Section\nProblems\n\\end_layout\n",
            "\\begin_layout Standard\n"
            "Problems are labelled Core, Proof, or Applied. Core problems consolidate essential techniques; Proof problems develop formal arguments; Applied problems connect the theory to measurement or policy.\n"
            "\\end_layout\n",
        ]
    )
    for problem in chapter.problems:
        heading = (
            "\\series bold\n"
            + f"Problem {problem.identifier} [{problem.level}]. {problem.title}.\n"
            + "\\series default"
        )
        for paragraph in (heading, *problem.paragraphs):
            parts.append(
                "\\begin_layout Exercise*\n"
                + lyx_inline(paragraph)
                + "\n\\end_layout\n"
            )
        parts.append(separator())
    parts.append(marker(f"ECON803_PROBLEMS_END:{chapter_slug}"))
    return "\n".join(parts)


def strip_generated_blocks(source: str, chapters: list[ChapterProblems]) -> str:
    for chapter in chapters:
        chapter_slug = slug(chapter.chapter)
        start_marker = marker(f"ECON803_PROBLEMS_START:{chapter_slug}")
        end_marker = marker(f"ECON803_PROBLEMS_END:{chapter_slug}")
        start = source.find(start_marker)
        if start < 0:
            continue
        end = source.find(end_marker, start)
        if end < 0:
            raise ValueError(f"missing end marker for {chapter.chapter}")
        # Canonicalize the whitespace at the insertion boundary.  Without this,
        # the wrapper newlines added by ``inject`` accumulate on every run and
        # make an otherwise unchanged generated block fail ``--check``.
        left = source[:start].rstrip("\n")
        right = source[end + len(end_marker) :].lstrip("\n")
        source = left + "\n\n" + right
    return source


def chapter_spans(source: str) -> list[tuple[str, int, int]]:
    matches = list(
        re.finditer(r"\\begin_layout Chapter\n(.*?)\n\\end_layout", source, re.S)
    )
    spans: list[tuple[str, int, int]] = []
    for index, match in enumerate(matches):
        title = normalize_space(match.group(1))
        candidates = [source.find("\\end_body", match.end())]
        next_chapter = matches[index + 1].start() if index + 1 < len(matches) else -1
        next_part = source.find("\\begin_layout Part\n", match.end())
        next_unnumbered_chapter = source.find(
            "\\begin_layout Chapter*\n", match.end()
        )
        next_appendix_command = source.find("\\backslash\nappendix", match.end())
        next_bibliography = source.find(
            "\\begin_inset CommandInset bibtex", match.end()
        )
        if next_chapter >= 0:
            candidates.append(next_chapter)
        if next_part >= 0:
            candidates.append(next_part)
        if next_unnumbered_chapter >= 0:
            candidates.append(next_unnumbered_chapter)
        if next_appendix_command >= 0:
            appendix_boundary = source.rfind(
                "\\begin_layout Standard\n", match.end(), next_appendix_command
            )
            if appendix_boundary >= 0:
                candidates.append(appendix_boundary)
        if next_bibliography >= 0:
            bibliography_boundary = source.rfind(
                "\\begin_layout Standard\n", match.end(), next_bibliography
            )
            if bibliography_boundary >= 0:
                candidates.append(bibliography_boundary)
        boundary = min(candidate for candidate in candidates if candidate >= 0)
        spans.append((title, match.start(), boundary))
    return spans


def inject(source: str, chapters: list[ChapterProblems]) -> str:
    source = strip_generated_blocks(source, chapters)
    spans = {title: (start, end) for title, start, end in chapter_spans(source)}
    missing = [chapter.chapter for chapter in chapters if chapter.chapter not in spans]
    if missing:
        raise ValueError("chapters not found in LyX source: " + ", ".join(missing))
    insertions = sorted(
        ((spans[chapter.chapter][1], problem_block(chapter)) for chapter in chapters),
        reverse=True,
    )
    for position, block in insertions:
        source = source[:position] + "\n" + block + "\n" + source[position:]
    return source


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lyx", type=Path)
    parser.add_argument("bank", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    chapters = parse_problem_bank(args.bank)
    original = args.lyx.read_text(encoding="utf-8")
    revised = inject(original, chapters)
    if args.check:
        if original != revised:
            raise SystemExit("problem sets are not synchronized with the bank")
        return
    args.lyx.write_text(revised, encoding="utf-8")


if __name__ == "__main__":
    main()
