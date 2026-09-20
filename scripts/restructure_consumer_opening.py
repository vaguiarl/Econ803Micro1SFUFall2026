#!/usr/bin/env python3
"""Mechanically regroup the opening consumer chapters in the canonical LyX file.

This is deliberately a *move-only* migration.  It replaces the current Part I
shell (three chapters) with the four-chapter shell approved in
``CONSUMER_RESTRUCTURE_PLAN.md`` and moves every existing Section block as an
opaque byte-for-byte unit.  It does not split mixed sections, deduplicate
definitions, rewrite prose, or redistribute generated problem blocks.  Those
are later editorial phases.

Safety properties
-----------------

* The default mode is ``--dry-run``; writing requires explicit ``--write``.
* Top-level LyX layouts are parsed with balanced layout/inset checks, so a
  heading inside a Note or another inset is never mistaken for manuscript
  structure.
* The legacy chapter and section inventory must match the frozen manifest
  below exactly.  A partially edited source is rejected rather than guessed at.
* Each source Section block, including every nested inset, is copied unchanged
  exactly once.
* Formal-layout counts and existing public-problem markers must be identical
  before and after transformation.
* Non-exported provenance markers make the operation idempotent.  Running the
  script again validates the transformed shell and leaves it unchanged.

Mode semantics
--------------

``--dry-run``
    Parse, transform in memory, check all invariants, and report the move plan.
    This is the default and never writes a file.

``--check``
    Return success only when the source already has one valid migration marker
    set and the planned four-chapter shell.  A valid legacy source is fully
    preflighted but returns status 1 because applying the migration would change
    it.  This makes the option suitable for CI after the migration is applied.

``--write``
    Apply the checked transformation atomically.  With ``--output`` the source
    remains untouched and the result is written to the requested path.
"""

from __future__ import annotations

import argparse
import difflib
import hashlib
import os
import re
import stat
import sys
import tempfile
from collections import Counter
from dataclasses import dataclass
from pathlib import Path
from typing import Iterable, Sequence


REPO_ROOT = Path(__file__).resolve().parents[1]
DEFAULT_SOURCE = (
    REPO_ROOT / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"
)

MIGRATION_VERSION = "1"
MARKER_PREFIX = "ECON803_CONSUMER_RESTRUCTURE"
START_MARKER = f"{MARKER_PREFIX}_START"
END_MARKER = f"{MARKER_PREFIX}_END"
VERSION_MARKER = f"{MARKER_PREFIX}_VERSION:{MIGRATION_VERSION}"
FORMAL_MARKER_PREFIX = f"{MARKER_PREFIX}_FORMAL_COUNTS:"
SOURCE_MARKER_PREFIX = f"{MARKER_PREFIX}_SOURCE"

LEGACY_PART = "Foundations of Choice and Demand"
TARGET_PART = "The Classical Rational Consumer"
# The extensions pass renames the following part before this migration runs.
NEXT_PART = "Risk, Stochastic Choice, and Attention"

FORMAL_LAYOUTS = frozenset(
    {
        "Axiom",
        "Claim",
        "Corollary",
        "Definition",
        "Example",
        "Exercise",
        "Exercise*",
        "Fact",
        "Lemma",
        "Proof",
        "Proposition",
        "Remark",
        "Remark*",
        "Theorem",
    }
)

PROBLEM_MARKER_RE = re.compile(
    r"ECON803_PROBLEMS_(?:START|END):[a-z0-9-]+"
)
LABEL_INSET_RE = re.compile(
    r"\\begin_inset CommandInset label\n.*?\n\\end_inset",
    re.DOTALL,
)
LABEL_NAME_RE = re.compile(
    r"\\begin_inset CommandInset label\n.*?\nname \"([^\"]+)\".*?\n\\end_inset",
    re.DOTALL,
)


class MigrationError(RuntimeError):
    """Raised when the source is not the exact legacy or migrated structure."""


@dataclass(frozen=True, order=True)
class SectionRef:
    chapter: str
    title: str


@dataclass(frozen=True)
class LayoutSpan:
    kind: str
    start: int
    end: int
    raw: str
    title: str


@dataclass(frozen=True)
class SourceSection:
    ref: SectionRef
    ordinal: int
    start: int
    end: int
    raw: str

    @property
    def digest(self) -> str:
        return hashlib.sha256(self.raw.encode("utf-8")).hexdigest()


@dataclass(frozen=True)
class SourcePrologue:
    chapter: str
    ordinal: int
    raw: str


@dataclass(frozen=True)
class SourceChapter:
    title: str
    labels: tuple[str, ...]
    prologues: tuple[SourcePrologue, ...]
    sections: tuple[SourceSection, ...]


@dataclass(frozen=True)
class LegacyPart:
    start: int
    end: int
    chapters: tuple[SourceChapter, ...]

    @property
    def sections(self) -> dict[SectionRef, SourceSection]:
        return {
            section.ref: section
            for chapter in self.chapters
            for section in chapter.sections
        }

    @property
    def prologues(self) -> tuple[SourcePrologue, ...]:
        return tuple(
            prologue
            for chapter in self.chapters
            for prologue in chapter.prologues
        )


@dataclass(frozen=True)
class TargetChapter:
    title: str
    labels: tuple[str, ...]
    question: str
    sections: tuple[SectionRef, ...]
    prologue_sources: tuple[str, ...] = ()


BASICS = "Basics of Consumer Theory"
ABSTRACT_CHOICE = "Preference and Choice"
UTILITY = "Consumer Theory: Utility Maximization"


def ref(chapter: str, title: str) -> SectionRef:
    return SectionRef(chapter, title)


# Frozen legacy inventory.  Its order is checked before any transformation.
LEGACY_SECTION_ORDER: dict[str, tuple[str, ...]] = {
    BASICS: (
        "Preliminaries",
        "Environment: Commodities and Budget Set",
        "Demand Functions",
        "Consistency in Consumption",
        "Comparative Statics and Slutsky Matrix",
        "Problems",
    ),
    ABSTRACT_CHOICE: (
        "From Choice Data to Preference",
        "Choice environments",
        "Preference relations",
        "Revealed choice and WGARP",
        "GARP on finite data",
        "Problems",
    ),
    UTILITY: (
        "Demand Correspondences",
        "Utility Representation",
        "The Utility Maximization Problem",
        "KKT Conditions for the UMP",
        "Properties of the Indirect Utility Function",
        "Roy's Identity",
        "Expenditure Minimization Problem (EMP)",
        "Hicksian Compensated Demand",
        "KKT Conditions for the EMP",
        "Shephard's Lemma",
        "Additional Properties",
        "Summary of Relationships between the EMP and UMP",
        "Slutsky Equation",
        "Summary of the Implications of Utility Maximization",
        "Integrability",
        "Examples and Applications of Demand Integrability",
        "Generalized Axiom of Revealed Preference (GARP)",
        "Revealed Preference and the Strong Axiom",
        "Forecasting with Varian's Support Set",
        "Upper Bounds for Welfare Analysis",
        "Experiments about Testing Rationality",
        "Results",
        "Afriat's Cost-Efficiency Index",
        "Measurement Error",
        "Welfare Evaluation",
        "Homothetic and Quasilinear Utility Functions",
        "Problems",
    ),
}

EXPECTED_LEGACY_LABELS: dict[str, tuple[str, ...]] = {
    BASICS: ("chap:basics",),
    ABSTRACT_CHOICE: ("chap:preference-choice",),
    UTILITY: ("chap:consumer-duality",),
}


# Phase-2, intact-block move plan.  Mixed sections are intentionally kept
# whole; the later editorial phase will split and merge them under the final
# headings described in CONSUMER_RESTRUCTURE_PLAN.md.
TARGET_CHAPTERS: tuple[TargetChapter, ...] = (
    TargetChapter(
        title="Utility Maximization and Consumer Demand",
        labels=("chap:utility-maximization-demand", "chap:basics"),
        question=(
            "Question: What is the benchmark model, and what behavior does it "
            "generate?"
        ),
        prologue_sources=(UTILITY,),
        sections=(
            ref(BASICS, "Preliminaries"),
            ref(BASICS, "Environment: Commodities and Budget Set"),
            ref(UTILITY, "The Utility Maximization Problem"),
            ref(UTILITY, "Demand Correspondences"),
            ref(UTILITY, "KKT Conditions for the UMP"),
            ref(UTILITY, "Homothetic and Quasilinear Utility Functions"),
            ref(BASICS, "Problems"),
        ),
    ),
    TargetChapter(
        title="Duality, Comparative Statics, and Welfare",
        labels=("chap:duality-welfare", "chap:consumer-duality"),
        question=(
            "Question: How do we compute the model's price responses and "
            "welfare implications?"
        ),
        sections=(
            ref(UTILITY, "Properties of the Indirect Utility Function"),
            ref(UTILITY, "Roy's Identity"),
            ref(UTILITY, "Expenditure Minimization Problem (EMP)"),
            ref(UTILITY, "Hicksian Compensated Demand"),
            ref(UTILITY, "KKT Conditions for the EMP"),
            ref(UTILITY, "Shephard's Lemma"),
            ref(UTILITY, "Additional Properties"),
            ref(UTILITY, "Summary of Relationships between the EMP and UMP"),
            ref(UTILITY, "Slutsky Equation"),
            ref(UTILITY, "Summary of the Implications of Utility Maximization"),
            ref(UTILITY, "Welfare Evaluation"),
        ),
    ),
    TargetChapter(
        title="Revealed Preference and Recoverability",
        labels=("chap:revealed-preference-recoverability",),
        question=(
            "Question: Could observed behavior have been generated by the "
            "benchmark model, and what can the data identify?"
        ),
        sections=(
            ref(BASICS, "Demand Functions"),
            ref(BASICS, "Consistency in Consumption"),
            ref(BASICS, "Comparative Statics and Slutsky Matrix"),
            ref(UTILITY, "Integrability"),
            ref(UTILITY, "Examples and Applications of Demand Integrability"),
            ref(UTILITY, "Generalized Axiom of Revealed Preference (GARP)"),
            ref(UTILITY, "Revealed Preference and the Strong Axiom"),
            ref(UTILITY, "Forecasting with Varian's Support Set"),
            ref(UTILITY, "Upper Bounds for Welfare Analysis"),
            ref(UTILITY, "Experiments about Testing Rationality"),
            ref(UTILITY, "Results"),
            ref(UTILITY, "Afriat's Cost-Efficiency Index"),
            ref(UTILITY, "Measurement Error"),
            ref(UTILITY, "Problems"),
        ),
    ),
    TargetChapter(
        title="Choice Without Budget Geometry",
        labels=("chap:choice-without-budget-geometry", "chap:preference-choice"),
        question=(
            "Question: Which conclusions are properties of choice itself, "
            "rather than of linear budget geometry?"
        ),
        sections=(
            ref(ABSTRACT_CHOICE, "From Choice Data to Preference"),
            ref(ABSTRACT_CHOICE, "Choice environments"),
            ref(ABSTRACT_CHOICE, "Preference relations"),
            ref(UTILITY, "Utility Representation"),
            ref(ABSTRACT_CHOICE, "Revealed choice and WGARP"),
            ref(ABSTRACT_CHOICE, "GARP on finite data"),
            ref(ABSTRACT_CHOICE, "Problems"),
        ),
    ),
)

# The frozen legacy source has one non-label chapter prologue, attached to the
# old utility-maximization chapter.  Keeping the count explicit lets the
# idempotence check detect a dropped or duplicated prologue marker later.
LEGACY_PROLOGUE_COUNTS: dict[str, int] = {UTILITY: 1}


def normalize_space(text: str) -> str:
    return " ".join(text.split())


def slug(text: str) -> str:
    return re.sub(r"[^a-z0-9]+", "-", text.lower()).strip("-")


def read_text_exact(path: Path) -> str:
    with path.open("r", encoding="utf-8", newline="") as handle:
        return handle.read()


def validate_balanced_lyx(source: str) -> None:
    """Check the two structural nestings needed by the mover."""

    layout_depth = 0
    inset_depth = 0
    token_re = re.compile(
        r"\\begin_layout\b|\\end_layout\b|\\begin_inset\b|\\end_inset\b"
    )
    for match in token_re.finditer(source):
        token = match.group(0)
        line_number = source.count("\n", 0, match.start()) + 1
        if token == "\\begin_layout":
            layout_depth += 1
        elif token == "\\end_layout":
            layout_depth -= 1
            if layout_depth < 0:
                raise MigrationError(
                    f"unmatched \\end_layout at source line {line_number}"
                )
        elif token == "\\begin_inset":
            inset_depth += 1
        elif token == "\\end_inset":
            inset_depth -= 1
            if inset_depth < 0:
                raise MigrationError(
                    f"unmatched \\end_inset at source line {line_number}"
                )
    if layout_depth:
        raise MigrationError(f"unclosed LyX layouts: final depth {layout_depth}")
    if inset_depth:
        raise MigrationError(f"unclosed LyX insets: final depth {inset_depth}")
    if source.count("\\begin_body") != 1 or source.count("\\end_body") != 1:
        raise MigrationError("expected exactly one LyX body")


def heading_text(raw_layout: str) -> str:
    """Extract ordinary top-level text from a heading layout."""

    text: list[str] = []
    inset_depth = 0
    for raw_line in raw_layout.splitlines()[1:]:
        line = raw_line.strip()
        if line.startswith("\\begin_inset "):
            inset_depth += 1
            continue
        if line == "\\end_inset":
            inset_depth -= 1
            continue
        if inset_depth:
            continue
        if not line or line.startswith("\\"):
            continue
        if line in {"status open", "status collapsed"}:
            continue
        text.append(line)
    return normalize_space(" ".join(text))


def top_level_layouts(source: str) -> list[LayoutSpan]:
    """Return body-level layouts, ignoring layouts nested in LyX insets."""

    validate_balanced_lyx(source)
    lines = source.splitlines(keepends=True)
    layouts: list[LayoutSpan] = []
    layout_depth = 0
    active_start: int | None = None
    active_kind: str | None = None
    offset = 0

    for raw_line in lines:
        line = raw_line.strip()
        if line.startswith("\\begin_layout "):
            if layout_depth == 0:
                active_start = offset
                active_kind = line[len("\\begin_layout ") :]
            layout_depth += 1
        elif line == "\\end_layout":
            if layout_depth == 1:
                if active_start is None or active_kind is None:
                    raise MigrationError("internal top-level layout parser error")
                end = offset + len(raw_line)
                raw = source[active_start:end]
                layouts.append(
                    LayoutSpan(
                        kind=active_kind,
                        start=active_start,
                        end=end,
                        raw=raw,
                        title=heading_text(raw),
                    )
                )
                active_start = None
                active_kind = None
            layout_depth -= 1
        offset += len(raw_line)

    if active_start is not None:
        raise MigrationError("unterminated top-level layout")
    return layouts


def find_unique_layout(
    layouts: Sequence[LayoutSpan], kind: str, title: str
) -> LayoutSpan:
    matches = [layout for layout in layouts if layout.kind == kind and layout.title == title]
    if len(matches) != 1:
        raise MigrationError(
            f"expected one {kind!r} layout titled {title!r}; found {len(matches)}"
        )
    return matches[0]


def extract_labels(raw: str) -> tuple[str, ...]:
    return tuple(LABEL_NAME_RE.findall(raw))


def formal_counts(source: str) -> Counter[str]:
    return Counter(
        layout.kind
        for layout in top_level_layouts(source)
        if layout.kind in FORMAL_LAYOUTS
    )


def formal_signature(counts: Counter[str]) -> str:
    return ",".join(f"{kind}={counts.get(kind, 0)}" for kind in sorted(FORMAL_LAYOUTS))


def parse_formal_signature(value: str) -> Counter[str]:
    counts: Counter[str] = Counter()
    if not value:
        raise MigrationError("empty formal-count signature")
    for field in value.split(","):
        if "=" not in field:
            raise MigrationError(f"malformed formal-count field {field!r}")
        kind, raw_count = field.split("=", 1)
        if kind not in FORMAL_LAYOUTS or not raw_count.isdigit():
            raise MigrationError(f"malformed formal-count field {field!r}")
        counts[kind] = int(raw_count)
    if set(counts) != set(FORMAL_LAYOUTS):
        missing = sorted(FORMAL_LAYOUTS - set(counts))
        extra = sorted(set(counts) - FORMAL_LAYOUTS)
        raise MigrationError(
            f"formal-count signature mismatch; missing={missing}, extra={extra}"
        )
    return counts


def extract_legacy_part(source: str) -> LegacyPart:
    layouts = top_level_layouts(source)
    old_part = find_unique_layout(layouts, "Part", LEGACY_PART)
    next_part = find_unique_layout(layouts, "Part", NEXT_PART)
    if old_part.start >= next_part.start:
        raise MigrationError("legacy Part I does not precede the next part")

    chapter_layouts = [
        layout
        for layout in layouts
        if layout.kind == "Chapter" and old_part.end <= layout.start < next_part.start
    ]
    expected_chapters = list(LEGACY_SECTION_ORDER)
    actual_chapters = [layout.title for layout in chapter_layouts]
    if actual_chapters != expected_chapters:
        raise MigrationError(
            "legacy chapter inventory changed:\n"
            f"  expected: {expected_chapters}\n"
            f"  actual:   {actual_chapters}"
        )

    source_chapters: list[SourceChapter] = []
    for chapter_index, chapter_layout in enumerate(chapter_layouts):
        chapter_end = (
            chapter_layouts[chapter_index + 1].start
            if chapter_index + 1 < len(chapter_layouts)
            else next_part.start
        )
        section_layouts = [
            layout
            for layout in layouts
            if layout.kind == "Section"
            and chapter_layout.end <= layout.start < chapter_end
        ]
        expected_sections = list(LEGACY_SECTION_ORDER[chapter_layout.title])
        actual_sections = [layout.title for layout in section_layouts]
        if actual_sections != expected_sections:
            raise MigrationError(
                f"section inventory changed in {chapter_layout.title!r}:\n"
                f"  expected: {expected_sections}\n"
                f"  actual:   {actual_sections}"
            )
        if not section_layouts:
            raise MigrationError(f"chapter {chapter_layout.title!r} has no sections")

        prologue_layouts = [
            layout
            for layout in layouts
            if chapter_layout.end <= layout.start < section_layouts[0].start
        ]
        labels: list[str] = []
        prologues: list[SourcePrologue] = []
        for layout in prologue_layouts:
            found_labels = extract_labels(layout.raw)
            if found_labels:
                labels.extend(found_labels)
                remainder = LABEL_INSET_RE.sub("", layout.raw)
                residual = heading_text(remainder)
                if residual:
                    raise MigrationError(
                        "a legacy chapter-label layout also contains prose; "
                        f"refusing to drop it in {chapter_layout.title!r}: {residual!r}"
                    )
                continue
            prologues.append(
                SourcePrologue(
                    chapter=chapter_layout.title,
                    ordinal=len(prologues) + 1,
                    raw=layout.raw,
                )
            )

        expected_labels = EXPECTED_LEGACY_LABELS[chapter_layout.title]
        if tuple(labels) != expected_labels:
            raise MigrationError(
                f"chapter labels changed in {chapter_layout.title!r}: "
                f"expected {expected_labels}, found {tuple(labels)}"
            )

        # The problem injector places its START note immediately before the
        # ``Problems`` heading.  Treat that note as part of the Problems block
        # rather than as the tail of the preceding substantive section; this
        # keeps START/END paired when the problem section moves to a different
        # target chapter.
        section_starts = [layout.start for layout in section_layouts]
        for section_index, section_layout in enumerate(section_layouts):
            if section_layout.title != "Problems":
                continue
            lower_bound = (
                section_layouts[section_index - 1].end if section_index else chapter_layout.end
            )
            marker_layouts = [
                layout
                for layout in layouts
                if layout.kind == "Standard"
                and lower_bound <= layout.start < section_layout.start
                and "ECON803_PROBLEMS_START:" in layout.raw
            ]
            if len(marker_layouts) != 1:
                raise MigrationError(
                    f"expected one problem START layout before {chapter_layout.title!r}; "
                    f"found {len(marker_layouts)}"
                )
            section_starts[section_index] = marker_layouts[0].start

        sections: list[SourceSection] = []
        for section_index, section_layout in enumerate(section_layouts):
            section_end = (
                section_starts[section_index + 1]
                if section_index + 1 < len(section_layouts)
                else chapter_end
            )
            sections.append(
                SourceSection(
                    ref=SectionRef(chapter_layout.title, section_layout.title),
                    ordinal=section_index + 1,
                    start=section_starts[section_index],
                    end=section_end,
                    raw=source[section_starts[section_index]:section_end],
                )
            )

        source_chapters.append(
            SourceChapter(
                title=chapter_layout.title,
                labels=tuple(labels),
                prologues=tuple(prologues),
                sections=tuple(sections),
            )
        )

    legacy = LegacyPart(
        start=old_part.start,
        end=next_part.start,
        chapters=tuple(source_chapters),
    )
    validate_move_manifest(legacy)
    return legacy


def all_planned_refs() -> tuple[SectionRef, ...]:
    return tuple(section for target in TARGET_CHAPTERS for section in target.sections)


def source_marker_for(section: SourceSection) -> str:
    return (
        f"{SOURCE_MARKER_PREFIX}:section:"
        f"{slug(section.ref.chapter)}:{section.ordinal:02d}:{slug(section.ref.title)}"
    )


def prologue_marker_for(prologue: SourcePrologue) -> str:
    return (
        f"{SOURCE_MARKER_PREFIX}:prologue:"
        f"{slug(prologue.chapter)}:{prologue.ordinal:02d}"
    )


def validate_move_manifest(legacy: LegacyPart) -> None:
    actual_refs = tuple(
        section.ref for chapter in legacy.chapters for section in chapter.sections
    )
    planned_refs = all_planned_refs()
    if Counter(actual_refs) != Counter(planned_refs):
        missing = sorted((Counter(actual_refs) - Counter(planned_refs)).elements())
        extra = sorted((Counter(planned_refs) - Counter(actual_refs)).elements())
        raise MigrationError(
            f"move manifest is not bijective; unmapped={missing}, unknown/duplicate={extra}"
        )
    duplicate_refs = [item for item, count in Counter(planned_refs).items() if count != 1]
    if duplicate_refs:
        raise MigrationError(f"duplicate section destinations: {duplicate_refs}")

    prologue_destinations = Counter(
        source
        for target in TARGET_CHAPTERS
        for source in target.prologue_sources
    )
    actual_prologue_sources = Counter(prologue.chapter for prologue in legacy.prologues)
    if prologue_destinations != actual_prologue_sources:
        raise MigrationError(
            "prologue move manifest is not bijective; "
            f"actual={actual_prologue_sources}, planned={prologue_destinations}"
        )

    problem_sections = [
        section
        for section in legacy.sections.values()
        if section.ref.title == "Problems"
    ]
    if len(problem_sections) != 3:
        raise MigrationError(
            f"expected three intact legacy problem sections; found {len(problem_sections)}"
        )
    for section in problem_sections:
        starts = re.findall(r"ECON803_PROBLEMS_START:[a-z0-9-]+", section.raw)
        ends = re.findall(r"ECON803_PROBLEMS_END:[a-z0-9-]+", section.raw)
        if len(starts) != 1 or len(ends) != 1:
            raise MigrationError(
                f"problem block markers are not unique in {section.ref}: "
                f"starts={starts}, ends={ends}"
            )


def note_marker(text: str) -> str:
    return (
        "\\begin_layout Standard\n"
        "\\begin_inset Note Note\n"
        "status collapsed\n\n"
        "\\begin_layout Plain Layout\n"
        f"{text}\n"
        "\\end_layout\n\n"
        "\\end_inset\n\n\n"
        "\\end_layout\n\n"
    )


def heading_layout(kind: str, title: str) -> str:
    return f"\\begin_layout {kind}\n{title}\n\\end_layout\n\n"


def label_layout(name: str) -> str:
    return (
        "\\begin_layout Standard\n"
        "\\begin_inset CommandInset label\n"
        "LatexCommand label\n"
        f'name "{name}"\n\n'
        "\\end_inset\n"
        "\\end_layout\n\n"
    )


def standard_layout(text: str) -> str:
    return f"\\begin_layout Standard\n{text}\n\\end_layout\n\n"


def render_target_part(source: str, legacy: LegacyPart) -> str:
    sections = legacy.sections
    prologues_by_source: dict[str, list[SourcePrologue]] = {}
    for prologue in legacy.prologues:
        prologues_by_source.setdefault(prologue.chapter, []).append(prologue)

    counts = formal_counts(source)
    pieces: list[str] = [
        note_marker(START_MARKER),
        note_marker(VERSION_MARKER),
        note_marker(FORMAL_MARKER_PREFIX + formal_signature(counts)),
        heading_layout("Part", TARGET_PART),
    ]

    for target in TARGET_CHAPTERS:
        pieces.append(heading_layout("Chapter", target.title))
        pieces.extend(label_layout(label) for label in target.labels)
        pieces.append(note_marker(f"{MARKER_PREFIX}_TARGET_CHAPTER:{slug(target.title)}"))
        pieces.append(standard_layout(target.question))

        for source_chapter in target.prologue_sources:
            for prologue in prologues_by_source.get(source_chapter, []):
                pieces.append(note_marker(prologue_marker_for(prologue)))
                pieces.append(prologue.raw)
                if not prologue.raw.endswith("\n\n"):
                    pieces.append("\n")

        for section_ref in target.sections:
            section = sections[section_ref]
            pieces.append(note_marker(source_marker_for(section)))
            pieces.append(section.raw)
            if not section.raw.endswith("\n\n"):
                pieces.append("\n")

    pieces.append(note_marker(END_MARKER))
    return "".join(pieces)


def count_exact(source: str, token: str) -> int:
    return source.count(token)


def expected_source_markers(legacy: LegacyPart) -> tuple[str, ...]:
    return tuple(
        [
            source_marker_for(section)
            for chapter in legacy.chapters
            for section in chapter.sections
        ]
        + [prologue_marker_for(prologue) for prologue in legacy.prologues]
    )


def validate_initial_transform(
    original: str, transformed: str, legacy: LegacyPart
) -> None:
    validate_balanced_lyx(transformed)
    if transformed[: legacy.start] != original[: legacy.start]:
        raise MigrationError("content before the replaced Part I changed")
    if not transformed.endswith(original[legacy.end :]):
        raise MigrationError("content after the replaced Part I changed")

    before_formal = formal_counts(original)
    after_formal = formal_counts(transformed)
    if before_formal != after_formal:
        raise MigrationError(
            f"formal-layout counts changed: before={before_formal}, after={after_formal}"
        )

    before_problem_markers = Counter(PROBLEM_MARKER_RE.findall(original))
    after_problem_markers = Counter(PROBLEM_MARKER_RE.findall(transformed))
    if before_problem_markers != after_problem_markers:
        raise MigrationError(
            "public problem marker inventory changed during transformation"
        )

    for chapter in legacy.chapters:
        for section in chapter.sections:
            occurrences = count_exact(transformed, section.raw)
            if occurrences != 1:
                raise MigrationError(
                    f"section {section.ref} was not preserved exactly once "
                    f"(sha256={section.digest}, occurrences={occurrences})"
                )
    for prologue in legacy.prologues:
        occurrences = count_exact(transformed, prologue.raw)
        if occurrences != 1:
            raise MigrationError(
                f"prologue from {prologue.chapter!r} was not preserved exactly once "
                f"(occurrences={occurrences})"
            )

    for marker in (
        START_MARKER,
        END_MARKER,
        VERSION_MARKER,
        *expected_source_markers(legacy),
    ):
        if count_exact(transformed, marker) != 1:
            raise MigrationError(f"migration marker is not unique: {marker!r}")

    validate_transformed(transformed)


def marker_region(source: str) -> tuple[int, int]:
    start = source.find(START_MARKER)
    end = source.find(END_MARKER)
    if start < 0 or end < 0 or start >= end:
        raise MigrationError("missing or misordered migration boundary markers")
    return start, end


def validate_problem_marker_pairs(source: str) -> None:
    starts = re.findall(r"ECON803_PROBLEMS_START:([a-z0-9-]+)", source)
    ends = re.findall(r"ECON803_PROBLEMS_END:([a-z0-9-]+)", source)
    if Counter(starts) != Counter(ends):
        raise MigrationError(
            f"unpaired generated problem markers: starts={Counter(starts)}, ends={Counter(ends)}"
        )
    duplicates = sorted(name for name, count in Counter(starts).items() if count != 1)
    if duplicates:
        raise MigrationError(f"duplicate generated problem blocks: {duplicates}")


def validate_transformed(source: str) -> None:
    validate_balanced_lyx(source)
    static_markers = (START_MARKER, END_MARKER, VERSION_MARKER)
    for marker in static_markers:
        if count_exact(source, marker) != 1:
            raise MigrationError(f"expected exactly one marker {marker!r}")
    if count_exact(source, FORMAL_MARKER_PREFIX) != 1:
        raise MigrationError("expected exactly one formal-count marker")

    signature_match = re.search(
        re.escape(FORMAL_MARKER_PREFIX) + r"([^\n]+)", source
    )
    if signature_match is None:
        raise MigrationError("formal-count signature is missing")
    # The recorded signature proves that the move itself preserved the formal
    # inventory (``validate_initial_transform`` compares before with after).
    # Later editorial passes are expected to add or consolidate theorem
    # environments, so an already-migrated manuscript must not be frozen to
    # the migration-time counts.
    parse_formal_signature(signature_match.group(1))

    region_start, region_end = marker_region(source)
    layouts = top_level_layouts(source)
    region_parts = [
        layout.title
        for layout in layouts
        if layout.kind == "Part" and region_start < layout.start < region_end
    ]
    if region_parts != [TARGET_PART]:
        raise MigrationError(
            f"migrated part shell changed: expected={[TARGET_PART]}, actual={region_parts}"
        )
    region_chapters = [
        layout.title
        for layout in layouts
        if layout.kind == "Chapter" and region_start < layout.start < region_end
    ]
    expected_chapters = [target.title for target in TARGET_CHAPTERS]
    if region_chapters != expected_chapters:
        raise MigrationError(
            "migrated chapter shell changed: "
            f"expected={expected_chapters}, actual={region_chapters}"
        )

    target_markers = [
        f"{MARKER_PREFIX}_TARGET_CHAPTER:{slug(target.title)}"
        for target in TARGET_CHAPTERS
    ]
    for marker in target_markers:
        if count_exact(source, marker) != 1:
            raise MigrationError(f"target-chapter marker is not unique: {marker!r}")

    expected_section_marker_count = sum(
        len(items) for items in LEGACY_SECTION_ORDER.values()
    )
    actual_section_marker_count = len(
        re.findall(re.escape(SOURCE_MARKER_PREFIX) + r":section:", source)
    )
    if actual_section_marker_count != expected_section_marker_count:
        raise MigrationError(
            "source-section marker count changed: "
            f"expected={expected_section_marker_count}, actual={actual_section_marker_count}"
        )

    # Every deterministic marker implied by the frozen manifest must remain
    # unique.  This catches accidental duplication without requiring the old
    # three-chapter source to remain available.
    legacy_ordinals = {
        SectionRef(chapter, title): ordinal
        for chapter, titles in LEGACY_SECTION_ORDER.items()
        for ordinal, title in enumerate(titles, start=1)
    }
    for section_ref, ordinal in legacy_ordinals.items():
        synthetic = SourceSection(section_ref, ordinal, 0, 0, "")
        marker = source_marker_for(synthetic)
        if count_exact(source, marker) != 1:
            raise MigrationError(f"source-section marker is not unique: {marker!r}")

    for chapter, count in LEGACY_PROLOGUE_COUNTS.items():
        for ordinal in range(1, count + 1):
            synthetic = SourcePrologue(chapter=chapter, ordinal=ordinal, raw="")
            marker = prologue_marker_for(synthetic)
            if count_exact(source, marker) != 1:
                raise MigrationError(
                    f"source-prologue marker is not unique: {marker!r}"
                )

    expected_labels = {
        label for target in TARGET_CHAPTERS for label in target.labels
    }
    label_counts = Counter(LABEL_NAME_RE.findall(source))
    for label in expected_labels:
        if label_counts[label] != 1:
            raise MigrationError(
                f"target chapter label is not unique: {label!r} "
                f"(count={label_counts[label]})"
            )

    validate_problem_marker_pairs(source)


def has_any_migration_marker(source: str) -> bool:
    return MARKER_PREFIX in source


def is_transformed(source: str) -> bool:
    return VERSION_MARKER in source


def transform(source: str) -> tuple[str, LegacyPart | None]:
    if is_transformed(source):
        validate_transformed(source)
        return source, None
    if has_any_migration_marker(source):
        raise MigrationError(
            "partial or unknown consumer-restructure markers found; refusing to guess"
        )

    validate_problem_marker_pairs(source)
    legacy = extract_legacy_part(source)
    new_part = render_target_part(source, legacy)
    transformed = source[: legacy.start] + new_part + source[legacy.end :]
    validate_initial_transform(source, transformed, legacy)
    return transformed, legacy


def atomic_write(path: Path, content: str, source_mode: int) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    descriptor, temporary_name = tempfile.mkstemp(
        prefix=f".{path.name}.", suffix=".tmp", dir=path.parent
    )
    temporary = Path(temporary_name)
    try:
        with os.fdopen(descriptor, "w", encoding="utf-8", newline="") as handle:
            handle.write(content)
            handle.flush()
            os.fsync(handle.fileno())
        os.chmod(temporary, source_mode)
        os.replace(temporary, path)
    except BaseException:
        temporary.unlink(missing_ok=True)
        raise


def print_plan() -> None:
    print(f"Part: {LEGACY_PART} -> {TARGET_PART}")
    for number, target in enumerate(TARGET_CHAPTERS, start=1):
        print(f"\nChapter {number}: {target.title}")
        for section_ref in target.sections:
            print(f"  <- {section_ref.chapter} / {section_ref.title}")
        for source_chapter in target.prologue_sources:
            print(f"  <- {source_chapter} / [chapter prologue]")


def print_dry_run_summary(legacy: LegacyPart | None, already_done: bool) -> None:
    if already_done:
        print("Consumer opening is already migrated; structural checks passed.")
        return
    if legacy is None:
        raise MigrationError("internal dry-run summary error")
    section_count = sum(len(chapter.sections) for chapter in legacy.chapters)
    problem_count = sum(
        section.ref.title == "Problems"
        for chapter in legacy.chapters
        for section in chapter.sections
    )
    print(
        "Dry run passed: "
        f"{len(legacy.chapters)} legacy chapters -> {len(TARGET_CHAPTERS)} target chapters; "
        f"{section_count} complete section blocks preserved; "
        f"{problem_count} problem sections retained intact."
    )
    print("No file was written.")


def unified_diff(before: str, after: str, path: Path) -> Iterable[str]:
    return difflib.unified_diff(
        before.splitlines(keepends=True),
        after.splitlines(keepends=True),
        fromfile=str(path),
        tofile=str(path) + " (planned)",
    )


def parse_args(argv: Sequence[str] | None = None) -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--source",
        type=Path,
        default=DEFAULT_SOURCE,
        help=f"canonical LyX source (default: {DEFAULT_SOURCE})",
    )
    modes = parser.add_mutually_exclusive_group()
    modes.add_argument(
        "--check",
        action="store_true",
        help="succeed only if the four-chapter migration is already applied",
    )
    modes.add_argument(
        "--dry-run",
        action="store_true",
        help="build and validate in memory without writing (default)",
    )
    modes.add_argument(
        "--write",
        action="store_true",
        help="atomically write the validated migration",
    )
    parser.add_argument(
        "--output",
        type=Path,
        help="write to this path instead of replacing --source (requires --write)",
    )
    parser.add_argument(
        "--diff",
        action="store_true",
        help="print the full unified diff in dry-run mode",
    )
    parser.add_argument(
        "--print-plan",
        action="store_true",
        help="print the frozen source-to-target section map",
    )
    args = parser.parse_args(argv)
    if not (args.check or args.dry_run or args.write):
        args.dry_run = True
    if args.output is not None and not args.write:
        parser.error("--output requires --write")
    if args.diff and not args.dry_run:
        parser.error("--diff is available only with --dry-run")
    return args


def main(argv: Sequence[str] | None = None) -> int:
    args = parse_args(argv)
    source_path = args.source.resolve()
    if not source_path.is_file():
        raise MigrationError(f"LyX source does not exist: {source_path}")

    original = read_text_exact(source_path)
    transformed, legacy = transform(original)
    already_done = legacy is None

    if args.print_plan:
        print_plan()

    if args.check:
        if already_done:
            print("Consumer opening migration is applied and structurally valid.")
            return 0
        print(
            "Consumer opening migration is valid but not yet applied; "
            "run with --dry-run for the move summary or --write to apply it.",
            file=sys.stderr,
        )
        return 1

    if args.dry_run:
        print_dry_run_summary(legacy, already_done)
        if args.diff and transformed != original:
            sys.stdout.writelines(unified_diff(original, transformed, source_path))
        return 0

    if transformed == original:
        print("Consumer opening already migrated; no file written.")
        return 0

    destination = (args.output or source_path).resolve()
    source_mode = stat.S_IMODE(source_path.stat().st_mode)
    atomic_write(destination, transformed, source_mode)
    print(f"Wrote validated consumer-opening migration to {destination}")
    return 0


if __name__ == "__main__":
    try:
        raise SystemExit(main())
    except MigrationError as error:
        print(f"error: {error}", file=sys.stderr)
        raise SystemExit(2)
