#!/usr/bin/env python3
"""Build the standalone, question-only ECON 803 practice-book LyX source.

The public problem banks remain the source of record.  This generator reuses
their validated parsers and writes a native LyX book containing the weekly
map, all 65 chapter problems, and all 10 additional-practice problems.
"""

from __future__ import annotations

import argparse
import csv
import re
from collections import Counter
from dataclasses import dataclass
from datetime import date
from pathlib import Path

from inject_problem_sets import (
    ChapterPathway,
    ChapterProblems,
    Problem,
    lyx_inline,
    parse_chapter_pathways,
    parse_problem_bank,
    separator,
)
from inject_reserve_bank import ReserveProblem, parse_bank as parse_reserve_bank


ROOT = Path(__file__).resolve().parents[1]
MAIN_BOOK = ROOT / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"
PROBLEM_BANK = ROOT / "problems" / "PROBLEM_BANK.md"
PATHWAYS = ROOT / "problems" / "CHAPTER_PATHWAYS.tsv"
WEEKLY_PLAN = ROOT / "problemsets" / "WEEKLY_RELEASE_PLAN.tsv"
RESERVE_MAP = ROOT / "problemsets" / "RESERVE_WEEKLY_MAP.tsv"
TARGET = (
    ROOT
    / "problemsets"
    / "practice_book"
    / "ECON803_Practice_Book_Fall2026.lyx"
)
TARGET_PDF = TARGET.with_suffix(".pdf")


@dataclass(frozen=True)
class WeeklySet:
    identifier: str
    meeting_date: str
    due_date: str
    topic: str
    required_ids: tuple[str, ...]
    extension_ids: tuple[str, ...]
    reserve_ids: tuple[str, ...]


def ascii_dashes(text: str) -> str:
    """Use TeX-friendly ASCII source without changing mathematical meaning."""

    return (
        text.replace("closed-form firm solutions", "closed-form firm expressions")
        .replace("\N{EM DASH}", "--")
        .replace("\N{EN DASH}", "--")
        .replace("\N{NON-BREAKING HYPHEN}", "-")
        .replace("\N{MINUS SIGN}", "-")
    )


def inline(text: str) -> str:
    return lyx_inline(ascii_dashes(text))


def layout(kind: str, text: str) -> str:
    return f"\\begin_layout {kind}\n{ascii_dashes(text)}\n\\end_layout\n"


def ert(command: str) -> str:
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


def toc() -> str:
    return (
        "\\begin_layout Standard\n"
        "\\begin_inset CommandInset toc\n"
        "LatexCommand tableofcontents\n\n"
        "\\end_inset\n\n\n"
        "\\end_layout\n"
    )


def chapter_star(title: str, *, add_to_toc: bool = True) -> str:
    block = layout("Chapter*", title)
    if add_to_toc:
        block += ert(f"addcontentsline{{toc}}{{chapter}}{{{ascii_dashes(title)}}}")
    block += ert(
        f"markboth{{{ascii_dashes(title).upper()}}}{{{ascii_dashes(title).upper()}}}"
    )
    return block


def make_header() -> str:
    source = MAIN_BOOK.read_text(encoding="utf-8")
    header = source[: source.index("\\begin_body")]
    preamble = r"""\begin_preamble
\usepackage{float}
\providecommand{\assumptionname}{Assumption}
\providecommand{\axiomname}{Axiom}
\providecommand{\claimname}{Claim}
\providecommand{\definitionname}{Definition}
\providecommand{\lemmaname}{Lemma}
\providecommand{\propositionname}{Proposition}
\providecommand{\remarkname}{Remark}
\providecommand{\corollaryname}{Corollary}
\providecommand{\theoremname}{Theorem}
\providecommand{\exercisename}{Problem}
\providecommand{\notationfirst}[2]{#2}
\providecommand{\notationdef}[2]{#2}
\definecolor{practiceblue}{rgb}{0.08,0.24,0.46}
\AtBeginDocument{%
  \renewenvironment{xca*}{\begin{trivlist}\item[]\normalfont}{\end{trivlist}}%
  \renewcommand{\contentsname}{Practice Book Contents}%
  \hypersetup{linkcolor=practiceblue,urlcolor=practiceblue,citecolor=practiceblue}%
}
\emergencystretch=2em
\raggedbottom
\let\cleardoublepage\clearpage
\end_preamble"""
    header = re.sub(
        r"\\begin_preamble.*?\\end_preamble",
        lambda _: preamble,
        header,
        flags=re.S,
    )
    replacements = {
        "\\spacing double": "\\spacing onehalf",
        "\\pdf_bookmarksnumbered false": "\\pdf_bookmarksnumbered true",
        "\\pdf_colorlinks false": "\\pdf_colorlinks true",
        "\\pdf_pdfborder true": "\\pdf_pdfborder false",
        "\\secnumdepth 3": "\\secnumdepth 2",
        "\\tocdepth 3": "\\tocdepth 2",
    }
    for old, new in replacements.items():
        if old not in header:
            raise ValueError(f"expected LyX header field is missing: {old}")
        header = header.replace(old, new, 1)
    return header


def split_ids(value: str) -> tuple[str, ...]:
    value = value.strip().strip('"')
    return tuple(item.strip() for item in value.split(",") if item.strip())


def pretty_date(value: str) -> str:
    parsed = date.fromisoformat(value)
    return f"{parsed.strftime('%b.')} {parsed.day}"


def parse_weekly_plan(
    problem_ids: set[str], reserve_ids: set[str]
) -> tuple[WeeklySet, ...]:
    with RESERVE_MAP.open(encoding="utf-8", newline="") as handle:
        reserve_reader = csv.DictReader(handle, delimiter="\t")
        expected_reserve_fields = [
            "set",
            "required_reserve_ids",
            "optional_reserve_ids",
        ]
        if reserve_reader.fieldnames != expected_reserve_fields:
            raise ValueError("unexpected reserve weekly-map columns")
        reserve_rows = list(reserve_reader)
    reserve_by_set: dict[str, tuple[str, ...]] = {}
    seen_reserve: list[str] = []
    for row in reserve_rows:
        identifiers = split_ids(row["required_reserve_ids"]) + split_ids(
            row["optional_reserve_ids"]
        )
        reserve_by_set[row["set"]] = identifiers
        seen_reserve.extend(identifiers)
    if Counter(seen_reserve) != Counter(reserve_ids):
        raise ValueError("reserve weekly map must assign every reserve ID once")

    required_fields = [
        "set",
        "meeting_date",
        "due_date",
        "topic",
        "required_ids",
        "extension_ids",
        "archive_sources",
        "status",
    ]
    with WEEKLY_PLAN.open(encoding="utf-8", newline="") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if reader.fieldnames != required_fields:
            raise ValueError("unexpected weekly-plan columns")
        rows = list(reader)
    if [row["set"] for row in rows] != [f"PS{i:02d}" for i in range(1, 14)]:
        raise ValueError("weekly plan must contain PS01 through PS13")

    sets: list[WeeklySet] = []
    seen_canonical: list[str] = []
    for row in rows:
        required = split_ids(row["required_ids"])
        extensions = split_ids(row["extension_ids"])
        unknown = (set(required) | set(extensions)) - problem_ids
        if unknown:
            raise ValueError("unknown problem IDs in weekly plan: " + ", ".join(sorted(unknown)))
        seen_canonical.extend(required)
        seen_canonical.extend(extensions)
        sets.append(
            WeeklySet(
                identifier=row["set"],
                meeting_date=pretty_date(row["meeting_date"]),
                due_date=pretty_date(row["due_date"]),
                topic=row["topic"].strip(),
                required_ids=required,
                extension_ids=extensions,
                reserve_ids=reserve_by_set.get(row["set"], ()),
            )
        )
    if len(seen_canonical) != len(set(seen_canonical)):
        raise ValueError("a canonical weekly problem is assigned more than once")
    return tuple(sets)


def rendered_problem(problem: Problem) -> str:
    heading = (
        "\\series bold\n"
        f"Problem {problem.identifier} [{problem.level}]. {ascii_dashes(problem.title)}.\n"
        "\\series default"
        "\n\\begin_inset ERT\nstatus collapsed\n\n"
        "\\begin_layout Plain Layout\n\n\\backslash\npar"
        "\\backslash\nnopagebreak[4]\n\\end_layout\n\n\\end_inset\n"
    )
    pieces = [layout("Exercise*", heading)]
    for paragraph in problem.paragraphs:
        part_match = re.match(r"^(Part [IVX]+)\. ([^.]+)\.\s*(.*)$", paragraph)
        if part_match:
            part, title, remainder = part_match.groups()
            pieces.append(layout("Subsection*", f"{part}. {title}"))
            pieces.append(layout("Exercise*", inline(remainder)))
        else:
            pieces.append(layout("Exercise*", inline(paragraph)))
    pieces.append(separator())
    return "\n".join(pieces)


def ordered_chapter_problems(
    chapter: ChapterProblems, pathway: ChapterPathway
) -> tuple[tuple[Problem, ...], tuple[Problem, ...], Problem]:
    hand = tuple(
        problem
        for problem in chapter.problems
        if problem.level == "Core" and problem.identifier != pathway.case_id
    )
    bridges = tuple(
        problem
        for problem in chapter.problems
        if problem.level != "Core" and problem.identifier != pathway.case_id
    )
    case = next(
        problem for problem in chapter.problems if problem.identifier == pathway.case_id
    )
    if not hand:
        raise ValueError(f"chapter has no hand benchmark: {chapter.chapter}")
    return hand, bridges, case


def render_chapter(chapter: ChapterProblems, pathway: ChapterPathway) -> str:
    hand, bridges, case = ordered_chapter_problems(chapter, pathway)
    pieces = [layout("Chapter", chapter.chapter)]
    pieces.append(layout("Section*", "Part I: By hand"))
    pieces.extend(rendered_problem(problem) for problem in hand)

    pieces.append(layout("Section*", "Part II: Formal and applied extensions"))
    if bridges:
        pieces.extend(rendered_problem(problem) for problem in bridges)
    else:
        pieces.append(
            layout(
                "Standard",
                "This chapter moves directly from the hand benchmark to its chapter use case.",
            )
        )

    pieces.append(layout("Section*", pathway.case_title))
    seed_word = "Problem" if len(pathway.seed_ids) == 1 else "Problems"
    pieces.append(
        layout(
            "Standard",
            "\\series bold\nChapter use case.\\series default\n "
            + inline(
                f"Seed: {seed_word} {', '.join(pathway.seed_ids)}. "
                "Fixed: all unlisted primitives and assumptions. "
                f"Scaled: {pathway.scale_axis}. Tool: {pathway.tool}. "
                f"Verification: {pathway.verification}"
            ),
        )
    )
    pieces.append(rendered_problem(case))
    return "\n".join(pieces)


def reserve_paragraph(paragraph: str) -> str:
    match = re.match(r"\*\*(.+?)\*\*\s*(.*)", paragraph)
    if not match:
        return inline(paragraph)
    label, remainder = match.groups()
    return (
        "\\series bold\n"
        + ascii_dashes(label)
        + "\\series default\n "
        + inline(remainder)
    )


def rendered_reserve_problem(problem: ReserveProblem, weekly_set: str) -> str:
    heading = (
        "\\series bold\n"
        f"Problem {problem.identifier} [{problem.label}]. {ascii_dashes(problem.title)}.\n"
        "\\series default"
        "\n\\begin_inset ERT\nstatus collapsed\n\n"
        "\\begin_layout Plain Layout\n\n\\backslash\npar"
        "\\backslash\nnopagebreak[4]\n\\end_layout\n\n\\end_inset\n"
    )
    pieces = [layout("Exercise*", heading)]
    pieces.append(layout("Exercise*", f"Suggested weekly placement: {weekly_set}."))
    for paragraph in problem.paragraphs:
        pieces.append(layout("Exercise*", reserve_paragraph(paragraph)))
    pieces.append(separator())
    return "\n".join(pieces)


def render_weekly_map(sets: tuple[WeeklySet, ...]) -> str:
    pieces = [chapter_star("Fall 2026 Weekly Practice Map")]
    pieces.append(
        layout(
            "Standard",
            "This map organizes the non-case chapter problems into thirteen weekly sets. "
            "Chapter use cases remain a separate case-study stream. Reserve problems are "
            "optional additional practice. The stable identifiers below refer to the full "
            "questions later in this book.",
        )
    )
    for weekly in sets:
        pieces.append(layout("Section*", f"{weekly.identifier}: {weekly.topic}"))
        pieces.append(
            layout(
                "Standard",
                f"Class meeting: {weekly.meeting_date}, 2026. Due: {weekly.due_date}, 2026.",
            )
        )
        required = ", ".join(weekly.required_ids) or "None"
        extensions = ", ".join(weekly.extension_ids) or "None"
        reserve = ", ".join(weekly.reserve_ids) or "None"
        pieces.append(
            layout(
                "Standard",
                f"Required: {required}. Formal or applied extension: {extensions}. "
                f"Optional reserve: {reserve}.",
            )
        )
    return "\n".join(pieces)


def render_reserve(
    reserve: list[ReserveProblem], weekly_sets: tuple[WeeklySet, ...]
) -> str:
    weekly_lookup = {
        identifier: weekly.identifier
        for weekly in weekly_sets
        for identifier in weekly.reserve_ids
    }
    pieces = [ert("backmatter"), chapter_star("Additional Practice Reserve")]
    pieces.append(
        layout(
            "Standard",
            "These ten question-only problems are corrected and independently checked "
            "descendants of earlier course assessments. Each combines a hand-solvable "
            "benchmark with a controlled computational or formal scale-up.",
        )
    )
    previous_topic: str | None = None
    for problem in reserve:
        if problem.topic != previous_topic:
            pieces.append(layout("Section", problem.topic))
            previous_topic = problem.topic
        pieces.append(rendered_reserve_problem(problem, weekly_lookup[problem.identifier]))
    return "\n".join(pieces)


def build() -> str:
    chapters = parse_problem_bank(PROBLEM_BANK)
    pathways = parse_chapter_pathways(PATHWAYS, chapters)
    reserve = parse_reserve_bank()
    canonical_ids = {
        problem.identifier for chapter in chapters for problem in chapter.problems
    }
    reserve_ids = {problem.identifier for problem in reserve}
    weekly_sets = parse_weekly_plan(canonical_ids, reserve_ids)

    body = [
        "\\begin_body\n",
        ert("hypersetup{pageanchor=false}"),
        layout("Title", "ECON 803 Microeconomic Theory I"),
        layout("Author", "Victor H. Aguiar"),
        layout("Date", "Question-only Practice Book - Fall 2026"),
        ert("hypersetup{pageanchor=true}"),
        ert("frontmatter"),
        toc(),
        chapter_star("How to Use This Practice Book"),
        layout(
            "Standard",
            "This volume collects the complete student-facing problem program for ECON 803. "
            "It contains 65 chapter problems and 10 additional-practice problems.",
        ),
        layout(
            "Standard",
            "Part I problems are compact benchmarks intended for derivation and discussion "
            "by hand. Part II problems develop proofs, applications, and one named use case "
            "for each chapter. Labels identify Core, Proof, and Applied work; they are not "
            "difficulty rankings.",
        ),
        layout(
            "Standard",
            "Before using Codex, Python, or Lean, record four lines: Seed identifies the hand "
            "result being extended; Fixed records the assumptions that remain unchanged; "
            "Scaled names the single enlarged dimension or strengthened claim; Risk states "
            "the new failure mode. The resulting artifact must reproduce the hand case and "
            "include a boundary or deliberately failing test.",
        ),
        layout(
            "Standard",
            "A successful computation or compilation verifies only the statement encoded in "
            "the artifact. Students remain responsible for the economic assumptions, the "
            "interpretation, and the distinction between numerical evidence and proof.",
        ),
        render_weekly_map(weekly_sets),
        ert("mainmatter"),
    ]

    part_starts = {
        "Utility Maximization and Consumer Demand": "The Classical Rational Consumer",
        "Expected Utility and Risk": "Risk, Stochastic Choice, and Attention",
        "Aggregate Demand and Representative Consumers": "Aggregation and Markets",
        "Theory of the Firm": "Production and Equilibrium",
        "Testable Restrictions on the Equilibrium Manifold": "Advanced Equilibrium Applications",
    }
    for chapter in chapters:
        if chapter.chapter == "Order Theory":
            body.append(ert("appendix"))
        elif chapter.chapter in part_starts:
            body.append(layout("Part", part_starts[chapter.chapter]))
        body.append(render_chapter(chapter, pathways[chapter.chapter]))
    body.append(render_reserve(reserve, weekly_sets))
    body.extend(["\\end_body\n", "\\end_document\n"])
    source = make_header() + "\n" + "\n".join(body)
    validate_source(source, chapters, reserve)
    return source


def validate_source(
    source: str, chapters: list[ChapterProblems], reserve: list[ReserveProblem]
) -> None:
    pathways = parse_chapter_pathways(PATHWAYS, chapters)
    expected_ids: list[str] = []
    for chapter in chapters:
        hand, bridges, case = ordered_chapter_problems(
            chapter, pathways[chapter.chapter]
        )
        expected_ids.extend(problem.identifier for problem in hand)
        expected_ids.extend(problem.identifier for problem in bridges)
        expected_ids.append(case.identifier)
    expected_ids.extend(problem.identifier for problem in reserve)
    headings = re.findall(r"\\series bold\nProblem ([A-Z0-9]+(?:\.[0-9]+)?) \[", source)
    if headings != expected_ids:
        raise ValueError("practice-book problem order or coverage is incorrect")
    if len(expected_ids) != 75 or len(set(expected_ids)) != 75:
        raise ValueError("practice book must contain exactly 75 unique problems")
    forbidden = ("instructor solution", "answer key follows", "SOURCE_LEDGER")
    lowered = source.lower()
    found = [token for token in forbidden if token.lower() in lowered]
    if found:
        raise ValueError("private-material marker in practice book: " + ", ".join(found))
    if source.count("\\begin_body") != 1 or source.count("\\end_body") != 1:
        raise ValueError("malformed LyX body")


def check_pdf(
    chapters: list[ChapterProblems], reserve: list[ReserveProblem]
) -> None:
    if not TARGET_PDF.exists():
        raise SystemExit(f"practice-book PDF does not exist: {TARGET_PDF}")
    try:
        from pypdf import PdfReader
    except ImportError as exc:  # pragma: no cover - environment diagnostic
        raise SystemExit("pypdf is required for practice-book PDF checks") from exc
    reader = PdfReader(TARGET_PDF)
    if len(reader.pages) < 30:
        raise SystemExit("practice-book PDF is unexpectedly short")
    text = "\n".join(page.extract_text() or "" for page in reader.pages)
    expected_ids = [
        problem.identifier for chapter in chapters for problem in chapter.problems
    ] + [problem.identifier for problem in reserve]
    missing = [identifier for identifier in expected_ids if f"Problem {identifier} [" not in text]
    if missing:
        raise SystemExit("practice-book PDF omits problem headings: " + ", ".join(missing))
    if "ECON 803 Microeconomic Theory I" not in text:
        raise SystemExit("practice-book PDF title is missing")
    if "Question-only Practice Book" not in text:
        raise SystemExit("practice-book PDF question-only label is missing")
    print(f"Practice-book PDF contains {len(reader.pages)} pages and all 75 problem headings")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true", help="fail if the LyX source is stale")
    parser.add_argument("--check-pdf", action="store_true", help="check the compiled PDF")
    args = parser.parse_args()
    chapters = parse_problem_bank(PROBLEM_BANK)
    reserve = parse_reserve_bank()
    if args.check_pdf:
        check_pdf(chapters, reserve)
        return
    source = build()
    if args.check:
        if not TARGET.exists() or TARGET.read_text(encoding="utf-8") != source:
            raise SystemExit("practice-book LyX source is not synchronized")
        print("Practice-book LyX source matches all 75 canonical questions")
        return
    TARGET.parent.mkdir(parents=True, exist_ok=True)
    TARGET.write_text(source, encoding="utf-8")
    print(TARGET)


if __name__ == "__main__":
    main()
