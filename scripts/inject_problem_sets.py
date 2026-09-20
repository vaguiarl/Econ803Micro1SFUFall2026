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
    chapter_names = [chapter.chapter for chapter in chapters]
    if len(chapter_names) != len(set(chapter_names)):
        raise ValueError("duplicate chapter heading in problem bank")
    chapter_slugs = [slug(chapter.chapter) for chapter in chapters]
    if len(chapter_slugs) != len(set(chapter_slugs)):
        raise ValueError("two problem-bank chapters have the same slug")
    all_identifiers: list[str] = []
    allowed_levels = {"Core", "Proof", "Applied"}
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


def problem_block(chapter: ChapterProblems, pathway: ChapterPathway) -> str:
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
        if problem.level != "Core" and problem.identifier != pathway.case_id
    )
    case_problem = next(
        problem
        for problem in chapter.problems
        if problem.identifier == pathway.case_id
    )

    parts = [marker(f"ECON803_PROBLEMS_START:{chapter_slug}")]
    parts.extend(
        [
            "\\begin_layout Section\nProblems\n\\end_layout\n",
            "\\begin_layout Subsection*\nPart I: By hand\n\\end_layout\n",
        ]
    )
    for problem in hand_problems:
        parts.append(problem_layout(problem))

    parts.extend(
        [
            "\\begin_layout Subsection*\n"
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
            "\\begin_layout Subsubsection*\n"
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
        start_marker = marker(f"ECON803_PROBLEMS_START:{chapter_slug}")
        end_marker = marker(f"ECON803_PROBLEMS_END:{chapter_slug}")
        start = source.find(start_marker)
        if start < 0:
            continue
        end = source.find(end_marker, start)
        if end < 0:
            raise ValueError(f"missing end marker for generated block {chapter_slug}")
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
        if problem.level != "Core" and problem.identifier != pathway.case_id
    ]
    return tuple([*hand, *bridge, pathway.case_id])


def validate_generated_source(
    source: str,
    chapters: list[ChapterProblems],
    pathways: dict[str, ChapterPathway],
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

    spans = {title: (start, end) for title, start, end in chapter_spans(source)}
    all_headings: list[str] = []
    for chapter in chapters:
        chapter_start, chapter_end = spans[chapter.chapter]
        chapter_source = source[chapter_start:chapter_end]
        chapter_slug = slug(chapter.chapter)
        start_marker = marker(f"ECON803_PROBLEMS_START:{chapter_slug}")
        end_marker = marker(f"ECON803_PROBLEMS_END:{chapter_slug}")
        block_start = chapter_source.find(start_marker)
        block_end = chapter_source.find(end_marker, block_start)
        if block_start < 0 or block_end < 0:
            raise ValueError(f"generated block is outside chapter: {chapter.chapter}")
        after_block = chapter_source[block_end + len(end_marker) :]
        if after_block.strip():
            raise ValueError(
                f"generated problem block is not last in chapter: {chapter.chapter}"
            )
        block = chapter_source[block_start : block_end + len(end_marker)]
        if block.count("\\begin_layout Section\nProblems\n\\end_layout") != 1:
            raise ValueError(f"invalid Problems section in {chapter.chapter}")
        if block.count("\\begin_layout Subsection*\nPart I: By hand\n\\end_layout") != 1:
            raise ValueError(f"invalid Part I heading in {chapter.chapter}")
        part_ii_prefix = (
            "\\begin_layout Subsection*\n"
            f"Part II: {pathways[chapter.chapter].case_title} — "
            "chapter use case and verified scale-up\n"
            "\\end_layout"
        )
        if block.count(part_ii_prefix) != 1:
            raise ValueError(f"invalid Part II heading in {chapter.chapter}")
        case_heading = (
            "\\begin_layout Subsubsection*\n"
            "Chapter use case\n"
            "\\end_layout"
        )
        expected_case_heading_count = int(
            any(
                problem.level != "Core"
                and problem.identifier != pathways[chapter.chapter].case_id
                for problem in chapter.problems
            )
        )
        if block.count(case_heading) != expected_case_heading_count:
            raise ValueError(f"invalid chapter-use-case heading in {chapter.chapter}")

        headings = re.findall(
            r"\\series bold\nProblem ([A-Z0-9]+\.[0-9]+) \[",
            block,
        )
        expected_headings = list(
            expected_problem_order(chapter, pathways[chapter.chapter])
        )
        if headings != expected_headings:
            raise ValueError(
                f"problem order mismatch in {chapter.chapter}: "
                + ", ".join(headings)
            )
        if headings[-1] != pathways[chapter.chapter].case_id:
            raise ValueError(f"chapter use case is not last in {chapter.chapter}")
        all_headings.extend(headings)

    bank_ids = [
        problem.identifier
        for chapter in chapters
        for problem in chapter.problems
    ]
    if sorted(all_headings) != sorted(bank_ids):
        raise ValueError("generated source omits or duplicates a bank problem")


def inject(
    source: str,
    chapters: list[ChapterProblems],
    pathways: dict[str, ChapterPathway],
) -> str:
    source = strip_generated_blocks(source, chapters)
    span_list = chapter_spans(source)
    span_titles = [title for title, _, _ in span_list]
    if len(span_titles) != len(set(span_titles)):
        raise ValueError("duplicate numbered chapter title in LyX source")
    spans = {title: (start, end) for title, start, end in span_list}
    missing = [chapter.chapter for chapter in chapters if chapter.chapter not in spans]
    if missing:
        raise ValueError("chapters not found in LyX source: " + ", ".join(missing))
    insertions = sorted(
        (
            (
                spans[chapter.chapter][1],
                problem_block(chapter, pathways[chapter.chapter]),
            )
            for chapter in chapters
        ),
        reverse=True,
    )
    for position, block in insertions:
        source = source[:position] + "\n" + block + "\n" + source[position:]
    validate_generated_source(source, chapters, pathways)
    return source


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("lyx", type=Path)
    parser.add_argument("bank", type=Path)
    parser.add_argument("--pathways", type=Path)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()

    chapters = parse_problem_bank(args.bank)
    pathway_path = args.pathways or args.bank.with_name("CHAPTER_PATHWAYS.tsv")
    pathways = parse_chapter_pathways(pathway_path, chapters)
    original = args.lyx.read_text(encoding="utf-8")
    revised = inject(original, chapters, pathways)
    if args.check:
        if original != revised:
            raise SystemExit("problem sets are not synchronized with the bank")
        return
    args.lyx.write_text(revised, encoding="utf-8")


if __name__ == "__main__":
    main()
