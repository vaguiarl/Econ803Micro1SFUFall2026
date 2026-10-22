#!/usr/bin/env python3
"""Inject the public problem bank into the textbook LyX source.

The problem bank is deliberately separate from the solutions handbook.  This
script is idempotent: generated blocks are marked with non-exported LyX notes
and replaced on the next run.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
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


@dataclass(frozen=True)
class ChapterPathway:
    chapter: str
    case_id: str
    seed_ids: tuple[str, ...]
    case_title: str
    tool: str
    scale_axis: str
    verification: str


@dataclass(frozen=True)
class BookChapterGroup:
    """Keep permanent bank topics independent of printed book chapters."""

    topic: str
    printed_chapter: str
    topic_heading: str


def normalize_space(text: str) -> str:
    return " ".join(text.split())


def parse_book_chapter_groups(
    path: Path, chapters: list[ChapterProblems]
) -> dict[str, BookChapterGroup]:
    """Read an exhaustive, ordered topic to physical chapter ledger."""
    fields = ["topic", "printed_chapter", "topic_heading"]
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != fields:
            raise ValueError("book chapter grouping columns must be: " + ", ".join(fields))
        rows = list(reader)
    groups: dict[str, BookChapterGroup] = {}
    for line_number, row in enumerate(rows, start=2):
        if None in row or any(row.get(field) is None for field in fields):
            raise ValueError(f"malformed book chapter grouping row on line {line_number}")
        values = {field: normalize_space(row[field]) for field in fields}
        if any(not value for value in values.values()):
            raise ValueError(f"blank book chapter grouping field on line {line_number}")
        if any(re.search(r"[\x00-\x1f]|\\", row[field]) for field in fields):
            raise ValueError(f"unsafe book chapter grouping field on line {line_number}")
        if values["topic"] in groups:
            raise ValueError("duplicate topic in book chapter grouping: " + values["topic"])
        groups[values["topic"]] = BookChapterGroup(**values)
    printed_chapter_groups(chapters, groups)
    return groups


def printed_chapter_groups(
    chapters: list[ChapterProblems],
    groups: dict[str, BookChapterGroup] | None = None,
) -> tuple[tuple[str, tuple[ChapterProblems, ...]], ...]:
    """Return physical chapters without changing topic, case or problem order.

    The identity default intentionally preserves the public synthetic APIs used
    by existing generators and regression tests.
    """
    if groups is None:
        return tuple((chapter.chapter, (chapter,)) for chapter in chapters)
    if list(groups) != [chapter.chapter for chapter in chapters]:
        raise ValueError("book chapter grouping must match every bank topic in bank order")
    result: list[tuple[str, tuple[ChapterProblems, ...]]] = []
    seen: set[str] = set()
    for chapter in chapters:
        group = groups[chapter.chapter]
        if group.topic != chapter.chapter:
            raise ValueError("book chapter grouping topic key does not match its row")
        title = group.printed_chapter
        if result and result[-1][0] == title:
            result[-1] = (title, (*result[-1][1], chapter))
        else:
            if title in seen:
                raise ValueError("grouped bank topics must be consecutive: " + title)
            result.append((title, (chapter,)))
            seen.add(title)
    for title, topics in result:
        headings = [groups[topic.chapter].topic_heading for topic in topics]
        if len(headings) != len(set(headings)):
            raise ValueError("duplicate topic heading in printed chapter: " + title)
    return tuple(result)


def advanced_difficulty_note(problems: tuple[Problem, ...]) -> str | None:
    """Keep archive provenance and the practice tiers identical in both books."""
    identifiers = {problem.identifier for problem in problems}
    if "9.A5" in identifiers:
        note = (
            "Difficulty guide. Problems 9.A1 to 9.A4 provide new optimization and regime practice. "
            "Problem 9.A5 restores the Western 2017 final examination question on indivisible "
            "production, including its original endowments and global equilibrium reasoning."
        )
        if "9.A6" in identifiers:
            note += " Problem 9.A6 adds a simple housing production case connecting developer optimization, latent prices, land rents and general equilibrium."
        return note
    if "10.A5" in identifiers:
        note = (
            "Difficulty guide. Problems 10.A1 to 10.A4 are preparatory practice. "
            "Problems 10.A5 and 10.A6 restore the harder continuum questions from "
            "the Western 2019 final examination and the SFU 2024 Problem Set 7. "
            "Their source notes distinguish necessary corrections from new extensions. "
            "Use the restored questions as the main timed exam preparation."
        )
        if "10.A7" in identifiers:
            note += " Problem 10.A7 restores the historical equilibrium and demand estimation exercise, with explicit corrections and a labelled time series extension."
        if "10.A8" in identifiers:
            note += " Problem 10.A8 connects discrete choice demand to pricing and endogeneity before a BLP style computational extension."
        return note
    if "11.A7" in identifiers:
        return (
            "Difficulty guide. Problems 11.A1 to 11.A6 develop geometric and regime reasoning. "
            "Problem 11.A7 restores the Western 2018 final examination question on the "
            "empirical content of equilibrium with production. It requires a full mathematical "
            "certificate and both directions of a rationalization argument, not only a computed equilibrium."
        )
    if "16.A1" in identifiers:
        return (
            "Advanced case guide. Problems 16.A1 and 16.A2 restore both the theory and "
            "Arabasta and Baltigo modeling parts of the SFU 2024 final examination. "
            "Problem 16.A3 is a new general equilibrium and dynamic extension of the "
            "Galor household problem 1.6. Each separates hand benchmarks from computational "
            "verification and states its equilibrium closure explicitly. Separate student "
            "packets contain these same questions."
        )
    return None


def parse_advanced_plan(path: Path, chapters: list[ChapterProblems]) -> dict[str, tuple[str, str]]:
    """Keep optional exam preparation separate from weekly required work."""
    advanced = {
        problem.identifier for chapter in chapters for problem in chapter.problems
        if problem.level == "Advanced"
    }
    with path.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != ["set", "recommended_ids", "further_practice_ids"]:
            raise ValueError("invalid advanced practice plan columns")
        rows = list(reader)
    result: dict[str, tuple[str, str]] = {}
    assigned: list[str] = []
    for row in rows:
        if row["set"] in result or row["set"] not in {f"PS{i:02d}" for i in range(1, 14)}:
            raise ValueError("duplicate or unknown advanced practice week")
        result[row["set"]] = (row["recommended_ids"], row["further_practice_ids"])
        assigned.extend(item.strip() for field in result[row["set"]] for item in field.split(",") if item.strip())
    if Counter(assigned) != Counter(advanced):
        raise ValueError("advanced practice plan must include every Advanced ID exactly once")
    return result


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
    chapter_names = [chapter.chapter for chapter in chapters]
    if len(chapter_names) != len(set(chapter_names)):
        raise ValueError("duplicate chapter heading in problem bank")
    chapter_slugs = [slug(chapter.chapter) for chapter in chapters]
    if len(chapter_slugs) != len(set(chapter_slugs)):
        raise ValueError("two problem-bank chapters have the same slug")
    all_identifiers: list[str] = []
    allowed_levels = {"Core", "Proof", "Applied", "Advanced"}
    for chapter in chapters:
        if not chapter.problems:
            raise ValueError(f"chapter has no problems: {chapter.chapter}")
        prefix = chapter.problems[0].identifier.split(".", 1)[0] + "."
        for problem in chapter.problems:
            if problem.level not in allowed_levels:
                raise ValueError(
                    f"unknown level for {problem.identifier}: {problem.level}"
                )
            if not problem.identifier.startswith(prefix):
                raise ValueError(
                    f"problem {problem.identifier} has the wrong chapter prefix"
                )
            all_identifiers.append(problem.identifier)
    if len(all_identifiers) != len(set(all_identifiers)):
        raise ValueError("duplicate problem identifier in problem bank")
    return chapters


def parse_chapter_pathways(
    path: Path, chapters: list[ChapterProblems]
) -> dict[str, ChapterPathway]:
    required_fields = [
        "chapter",
        "case_id",
        "seed_ids",
        "case_title",
        "tool",
        "scale_axis",
        "verification",
    ]
    with path.open(encoding="utf-8-sig", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != required_fields:
            raise ValueError(
                "chapter pathway columns must be: " + ", ".join(required_fields)
            )
        rows = list(reader)

    chapter_names = [chapter.chapter for chapter in chapters]
    problem_ids = {
        problem.identifier
        for chapter in chapters
        for problem in chapter.problems
    }
    unsafe = re.compile(
        r"[\x00-\x08\x0b\x0c\x0e-\x1f]|\\(?:begin|end)_(?:layout|inset)"
    )
    pathways: dict[str, ChapterPathway] = {}
    pathway_order: list[str] = []
    case_ids: set[str] = set()
    for line_number, row in enumerate(rows, start=2):
        if None in row or any(row.get(field) is None for field in required_fields):
            raise ValueError(f"malformed chapter pathway row on line {line_number}")
        values = {field: normalize_space(row[field]) for field in required_fields}
        if any(not value for value in values.values()):
            raise ValueError(f"blank chapter pathway field on line {line_number}")
        if any(unsafe.search(value) for value in values.values()):
            raise ValueError(f"unsafe LyX content in pathway row {line_number}")

        chapter_name = values["chapter"]
        if chapter_name not in chapter_names:
            raise ValueError(f"unknown chapter in pathway ledger: {chapter_name}")
        if chapter_name in pathways:
            raise ValueError(f"duplicate pathway for chapter: {chapter_name}")
        chapter_problem_ids = {
            problem.identifier
            for chapter in chapters
            if chapter.chapter == chapter_name
            for problem in chapter.problems
        }
        case_id = values["case_id"]
        if case_id not in chapter_problem_ids:
            raise ValueError(
                f"case {case_id} is not a problem in chapter {chapter_name}"
            )
        if case_id in case_ids:
            raise ValueError(f"duplicate designated case: {case_id}")

        seed_ids = tuple(
            identifier.strip()
            for identifier in values["seed_ids"].split(",")
            if identifier.strip()
        )
        if not seed_ids or len(seed_ids) != len(set(seed_ids)):
            raise ValueError(
                f"seed IDs must be nonempty and unique for {chapter_name}"
            )
        unknown_seeds = [
            identifier for identifier in seed_ids if identifier not in problem_ids
        ]
        if unknown_seeds:
            raise ValueError(
                f"unknown seed IDs for {chapter_name}: " + ", ".join(unknown_seeds)
            )

        pathways[chapter_name] = ChapterPathway(
            chapter=chapter_name,
            case_id=case_id,
            seed_ids=seed_ids,
            case_title=values["case_title"],
            tool=values["tool"],
            scale_axis=values["scale_axis"],
            verification=values["verification"],
        )
        pathway_order.append(chapter_name)
        case_ids.add(case_id)

    if pathway_order != chapter_names:
        missing = [name for name in chapter_names if name not in pathways]
        extra = [name for name in pathway_order if name not in chapter_names]
        detail = []
        if missing:
            detail.append("missing " + ", ".join(missing))
        if extra:
            detail.append("extra " + ", ".join(extra))
        if not detail:
            detail.append("rows are not in problem-bank chapter order")
        raise ValueError("chapter pathway mismatch: " + "; ".join(detail))
    return pathways


def lyx_inline(text: str) -> str:
    pieces: list[str] = []
    position = 0
    for match in re.finditer(r"\$(?P<formula>.+?)\$|`(?P<code>[^`\n]+)`", text):
        pieces.append(text[position : match.start()])
        # End the source line immediately after the inline formula inset.  LyX
        # keeps the preceding ordinary space, while later prose starts on the
        # next source line instead of being swallowed after ``\\end_inset``.
        if match.group("formula") is not None:
            pieces.append(
                "\\begin_inset Formula $"
                + match.group("formula")
                + "$\\end_inset\n"
            )
        else:
            # Native typewriter avoids literal Markdown delimiters and keeps
            # command options as two ASCII hyphens in the exported PDF.
            pieces.append("\n\\family typewriter\n" + match.group("code") + "\n\\family default\n")
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


def marker_span(source: str, name: str) -> tuple[int, int]:
    """Return the outer LyX layout containing a generated note marker.

    LyX may reflow whitespace inside a Note inset when a user saves the book.
    Locating the semantic token first keeps regeneration idempotent without
    requiring the entire serialized marker to remain byte-for-byte identical.
    """

    if source.count(name) != 1:
        raise ValueError(f"generated marker is missing or duplicated: {name}")
    token = source.index(name)
    start = source.rfind("\\begin_layout Standard", 0, token)
    note = source.rfind("\\begin_inset Note Note", start, token)
    inset_end = source.find("\\end_inset", token)
    layout_end = source.find("\\end_layout", inset_end)
    if min(start, note, inset_end, layout_end) < 0 or note < start:
        raise ValueError(f"generated marker has malformed LyX structure: {name}")
    return start, layout_end + len("\\end_layout")


def separator() -> str:
    return (
        "\\begin_layout Standard\n"
        "\\begin_inset Separator parbreak\n"
        "\\end_inset\n\n\n"
        "\\end_layout\n"
    )


def problem_layout(problem: Problem) -> str:
    parts: list[str] = []
    heading = (
        "\\series bold\n"
        + f"Problem {problem.identifier} [{problem.level}]. {problem.title}.\n"
        + "\\series default"
        + "\n\\begin_inset ERT\nstatus collapsed\n\n"
        + "\\begin_layout Plain Layout\n\n\\backslash\npar"
        + "\\backslash\nnopagebreak[4]\n\\end_layout\n\n\\end_inset\n"
    )
    for paragraph in (heading, *problem.paragraphs):
        parts.append(
            "\\begin_layout Exercise*\n"
            + lyx_inline(paragraph)
            + "\n\\end_layout\n"
        )
    parts.append(separator())
    return "\n".join(parts)


def problem_block(
    chapter: ChapterProblems,
    pathway: ChapterPathway,
    *,
    topic_heading: str | None = None,
    include_problems_heading: bool = True,
) -> str:
    chapter_slug = slug(chapter.chapter)
    hand_problems = tuple(
        problem
        for problem in chapter.problems
        if problem.level == "Core" and problem.identifier != pathway.case_id
    )
    if not hand_problems:
        raise ValueError(f"chapter has no Part I Core problem: {chapter.chapter}")
    bridge_problems = tuple(
        problem
        for problem in chapter.problems
        if problem.level not in {"Core", "Advanced"} and problem.identifier != pathway.case_id
    )
    advanced_problems = tuple(
        problem
        for problem in chapter.problems
        if problem.level == "Advanced" and problem.identifier != pathway.case_id
    )
    case_problem = next(
        problem
        for problem in chapter.problems
        if problem.identifier == pathway.case_id
    )

    part_layout = "Subsubsection*" if topic_heading else "Subsection*"
    case_layout = "Paragraph*" if topic_heading else "Subsubsection*"
    parts = [marker(f"ECON803_PROBLEMS_START:{chapter_slug}")]
    if include_problems_heading:
        parts.append("\\begin_layout Section\nProblems\n\\end_layout\n")
    if topic_heading:
        parts.append(f"\\begin_layout Subsection*\n{topic_heading}\n\\end_layout\n")
    parts.append(f"\\begin_layout {part_layout}\nPart I: By hand\n\\end_layout\n")
    for problem in hand_problems:
        parts.append(problem_layout(problem))

    if advanced_problems:
        parts.append(
            f"\\begin_layout {part_layout}\nAdvanced exam practice\n\\end_layout\n"
        )
        parts.append(
            "\\begin_layout Standard\n"
            "These problems build toward integrated graduate exam arguments. "
            "The suggested time applies to the hand questions, not the optional tool extension. "
            "First draw a diagram or state a solution plan, define the feasible set, "
            "and identify possible corners. Explain why each candidate is globally optimal "
            "and check the economic accounting. Attempt the hand questions before using tools. "
            "For an optional extension, state Seed, Fixed, Scaled and Risk before coding "
            "and enlarge one feature at a time.\n"
            "\\end_layout\n"
        )
        difficulty_note = advanced_difficulty_note(advanced_problems)
        if difficulty_note:
            parts.append(
                "\\begin_layout Standard\n"
                + difficulty_note + "\n\\end_layout\n"
            )
        parts.extend(problem_layout(problem) for problem in advanced_problems)

    parts.extend(
        [
            f"\\begin_layout {part_layout}\n"
            + f"Part II: {pathway.case_title} — chapter use case and verified scale-up\n"
            + "\\end_layout\n",
        ]
    )
    for problem in bridge_problems:
        parts.append(problem_layout(problem))

    seed_label = (
        "Problem " if len(pathway.seed_ids) == 1 else "Problems "
    ) + ", ".join(pathway.seed_ids)
    if bridge_problems:
        parts.append(
            f"\\begin_layout {case_layout}\n"
            "Chapter use case\n"
            "\\end_layout\n"
        )
    parts.append(
        "\\begin_layout Standard\n"
        + lyx_inline(
            f"Seed: {seed_label}. Fixed: all unlisted primitives and assumptions. Scaled: {pathway.scale_axis}. Tool: {pathway.tool}. Verification: {pathway.verification}"
        )
        + "\n\\end_layout\n"
    )
    parts.append(problem_layout(case_problem))
    parts.append(marker(f"ECON803_PROBLEMS_END:{chapter_slug}"))
    return "\n".join(parts)


def strip_generated_blocks(source: str, chapters: list[ChapterProblems]) -> str:
    # Strip every generated block already present, including legacy chapter
    # slugs left by a chapter reorganization.  The paired marker format makes
    # this safe and lets one canonical bank migration replace old blocks
    # without duplicating them.
    marker_tokens = re.findall(
        r"ECON803_PROBLEMS_(START|END):([a-z0-9-]+)", source
    )
    if len(marker_tokens) % 2:
        raise ValueError("orphan generated problem marker")
    for index in range(0, len(marker_tokens), 2):
        start_token, end_token = marker_tokens[index : index + 2]
        if start_token[0] != "START" or end_token != ("END", start_token[1]):
            raise ValueError("crossed, nested, or mismatched generated problem markers")
    existing_slugs = [
        chapter_slug
        for marker_type, chapter_slug in marker_tokens
        if marker_type == "START"
    ]
    if len(existing_slugs) != len(set(existing_slugs)):
        raise ValueError("duplicate generated problem START markers")
    current_slugs = [slug(chapter.chapter) for chapter in chapters]
    chapter_slugs = list(dict.fromkeys([*existing_slugs, *current_slugs]))
    for chapter_slug in chapter_slugs:
        start_name = f"ECON803_PROBLEMS_START:{chapter_slug}"
        end_name = f"ECON803_PROBLEMS_END:{chapter_slug}"
        if start_name not in source:
            continue
        start, _ = marker_span(source, start_name)
        _, end = marker_span(source, end_name)
        if end <= start:
            raise ValueError(f"crossed markers for generated block {chapter_slug}")
        # Canonicalize the whitespace at the insertion boundary.  Without this,
        # the wrapper newlines added by ``inject`` accumulate on every run and
        # make an otherwise unchanged generated block fail ``--check``.
        left = source[:start].rstrip("\n")
        right = source[end:].lstrip("\n")
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


def expected_problem_order(
    chapter: ChapterProblems, pathway: ChapterPathway
) -> tuple[str, ...]:
    hand = [
        problem.identifier
        for problem in chapter.problems
        if problem.level == "Core" and problem.identifier != pathway.case_id
    ]
    bridge = [
        problem.identifier
        for problem in chapter.problems
        if problem.level not in {"Core", "Advanced"} and problem.identifier != pathway.case_id
    ]
    advanced = [
        problem.identifier
        for problem in chapter.problems
        if problem.level == "Advanced" and problem.identifier != pathway.case_id
    ]
    return tuple([*hand, *advanced, *bridge, pathway.case_id])


def validate_generated_source(
    source: str,
    chapters: list[ChapterProblems],
    pathways: dict[str, ChapterPathway],
    groups: dict[str, BookChapterGroup] | None = None,
) -> None:
    expected_markers = [
        token
        for chapter in chapters
        for token in (
            ("START", slug(chapter.chapter)),
            ("END", slug(chapter.chapter)),
        )
    ]
    actual_markers = re.findall(
        r"ECON803_PROBLEMS_(START|END):([a-z0-9-]+)", source
    )
    if actual_markers != expected_markers:
        raise ValueError("generated problem markers do not match the problem bank")

    span_list = chapter_spans(source)
    if len({title for title, _, _ in span_list}) != len(span_list):
        raise ValueError("duplicate numbered chapter title in LyX source")
    spans = {title: (start, end) for title, start, end in span_list}
    all_headings: list[str] = []
    for printed_title, topics in printed_chapter_groups(chapters, groups):
        if printed_title not in spans:
            raise ValueError("printed chapter not found in LyX source: " + printed_title)
        chapter_start, chapter_end = spans[printed_title]
        chapter_source = source[chapter_start:chapter_end]
        grouped = len(topics) > 1
        if chapter_source.count("\\begin_layout Section\nProblems\n\\end_layout") != 1:
            raise ValueError(f"invalid Problems section in {printed_title}")
        previous_end: int | None = None
        for topic_index, chapter in enumerate(topics):
            chapter_slug = slug(chapter.chapter)
            start_marker = marker(f"ECON803_PROBLEMS_START:{chapter_slug}")
            end_marker = marker(f"ECON803_PROBLEMS_END:{chapter_slug}")
            block_start = chapter_source.find(start_marker)
            block_end = chapter_source.find(end_marker, block_start)
            if block_start < 0 or block_end < 0:
                raise ValueError(f"generated block is outside chapter: {chapter.chapter}")
            if previous_end is not None and chapter_source[previous_end:block_start].strip():
                raise ValueError(f"grouped problem blocks are not consecutive in {printed_title}")
            previous_end = block_end + len(end_marker)
            block = chapter_source[block_start:previous_end]
            if block.count("\\begin_layout Section\nProblems\n\\end_layout") != int(topic_index == 0):
                raise ValueError(f"invalid Problems section in {chapter.chapter}")
            part_layout = "Subsubsection*" if grouped else "Subsection*"
            case_layout = "Paragraph*" if grouped else "Subsubsection*"
            if grouped:
                topic_heading = groups[chapter.chapter].topic_heading
                if block.count(f"\\begin_layout Subsection*\n{topic_heading}\n\\end_layout") != 1:
                    raise ValueError(f"invalid grouped topic heading in {chapter.chapter}")
            if block.count(f"\\begin_layout {part_layout}\nPart I: By hand\n\\end_layout") != 1:
                raise ValueError(f"invalid Part I heading in {chapter.chapter}")
            part_ii_prefix = (
                f"\\begin_layout {part_layout}\n"
                f"Part II: {pathways[chapter.chapter].case_title} — "
                "chapter use case and verified scale-up\n"
                "\\end_layout"
            )
            if block.count(part_ii_prefix) != 1:
                raise ValueError(f"invalid Part II heading in {chapter.chapter}")
            case_heading = (
                f"\\begin_layout {case_layout}\nChapter use case\n\\end_layout"
            )
            expected_case_heading_count = int(any(
                problem.level not in {"Core", "Advanced"}
                and problem.identifier != pathways[chapter.chapter].case_id
                for problem in chapter.problems
            ))
            if block.count(case_heading) != expected_case_heading_count:
                raise ValueError(f"invalid chapter-use-case heading in {chapter.chapter}")
            headings = re.findall(
                r"\\series bold\nProblem ([A-Z0-9]+\.A?[0-9]+) \[", block
            )
            expected_headings = list(expected_problem_order(chapter, pathways[chapter.chapter]))
            if headings != expected_headings:
                raise ValueError(f"problem order mismatch in {chapter.chapter}: " + ", ".join(headings))
            if headings[-1] != pathways[chapter.chapter].case_id:
                raise ValueError(f"chapter use case is not last in {chapter.chapter}")
            all_headings.extend(headings)
        if previous_end is None or chapter_source[previous_end:].strip():
            raise ValueError(f"generated problem block is not last in chapter: {printed_title}")

    bank_ids = [
        problem.identifier
        for chapter in chapters
        for problem in chapter.problems
    ]
    if sorted(all_headings) != sorted(bank_ids):
        raise ValueError("generated source omits or duplicates a bank problem")

    # The generated blocks may be internally perfect while stale copies of the
    # same exercises survive elsewhere in a chapter body.  Scan the complete
    # manuscript so the public bank remains the single question-only source of
    # record and every stable problem identifier appears exactly once.
    source_headings = re.findall(
        r"\\series bold\nProblem ([A-Z0-9]+\.A?[0-9]+) \[",
        source,
    )
    if Counter(source_headings) != Counter(bank_ids):
        expected = Counter(bank_ids)
        actual = Counter(source_headings)
        discrepancies = [
            f"{identifier}: expected {expected[identifier]}, found {actual[identifier]}"
            for identifier in sorted(expected.keys() | actual.keys())
            if expected[identifier] != actual[identifier]
        ]
        raise ValueError(
            "problem headings outside the generated chapter blocks: "
            + "; ".join(discrepancies)
        )


def inject(
    source: str,
    chapters: list[ChapterProblems],
    pathways: dict[str, ChapterPathway],
    groups: dict[str, BookChapterGroup] | None = None,
) -> str:
    source = strip_generated_blocks(source, chapters)
    span_list = chapter_spans(source)
    span_titles = [title for title, _, _ in span_list]
    if len(span_titles) != len(set(span_titles)):
        raise ValueError("duplicate numbered chapter title in LyX source")
    spans = {title: (start, end) for title, start, end in span_list}
    physical_chapters = printed_chapter_groups(chapters, groups)
    missing = [title for title, _ in physical_chapters if title not in spans]
    if missing:
        raise ValueError("chapters not found in LyX source: " + ", ".join(missing))
    insertions = sorted(
        (
            (
                spans[title][1],
                "\n".join(
                    problem_block(
                        chapter,
                        pathways[chapter.chapter],
                        topic_heading=(groups[chapter.chapter].topic_heading if len(topics) > 1 else None),
                        include_problems_heading=index == 0,
                    )
                    for index, chapter in enumerate(topics)
                ),
            )
            for title, topics in physical_chapters
        ),
        reverse=True,
    )
    for position, block in insertions:
        source = source[:position] + "\n" + block + "\n" + source[position:]
    validate_generated_source(source, chapters, pathways, groups)
    return source


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lyx", type=Path)
    parser.add_argument("bank", type=Path)
    parser.add_argument("--pathways", type=Path)
    parser.add_argument("--groups", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    chapters = parse_problem_bank(args.bank)
    pathway_path = args.pathways or args.bank.with_name("CHAPTER_PATHWAYS.tsv")
    pathways = parse_chapter_pathways(pathway_path, chapters)
    group_path = args.groups or args.bank.with_name("BOOK_CHAPTER_GROUPS.tsv")
    groups = parse_book_chapter_groups(group_path, chapters) if group_path.exists() else None
    original = args.lyx.read_text(encoding="utf-8")
    revised = inject(original, chapters, pathways, groups)
    if args.check:
        if original != revised:
            raise SystemExit("problem sets are not synchronized with the bank")
        return
    args.lyx.write_text(revised, encoding="utf-8")


if __name__ == "__main__":
    main()
