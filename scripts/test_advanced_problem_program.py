#!/usr/bin/env python3
"""Regression tests for Advanced chapter practice and LyX generation.

Run with ``python3 scripts/test_advanced_problem_program.py``. No real bank,
manuscript, weekly assignment, solution file or student record is modified.
"""

from __future__ import annotations

import csv
from dataclasses import replace
from pathlib import Path
import re
import tempfile
import unittest

import build_practice_book as practice
import inject_problem_sets as inject


CHAPTER_TITLE = "Theory of the Firm"
PROBLEM_PATTERN = r"\\series bold\nProblem ([A-Z0-9]+\.A?[0-9]+) \["


def sample_chapter(prefix: str = "9", title: str = CHAPTER_TITLE):
    """Scramble categories so a source order shortcut cannot pass the tests."""
    return inject.ChapterProblems(
        title,
        (
            inject.Problem(f"{prefix}.4", "Applied", "Final use case", ("Case text.",)),
            inject.Problem(f"{prefix}.A1", "Advanced", "Capacity regimes", ("Check $q\\geq0$.",)),
            inject.Problem(f"{prefix}.1", "Core", "Hand benchmark", ("Benchmark text.",)),
            inject.Problem(f"{prefix}.2", "Proof", "Global verification", ("Proof text.",)),
            inject.Problem(f"{prefix}.A2", "Advanced", "Technology change", ("Counterfactual text.",)),
        ),
    )


def sample_pathway(prefix: str = "9", title: str = CHAPTER_TITLE):
    return inject.ChapterPathway(
        chapter=title,
        case_id=f"{prefix}.4",
        seed_ids=(f"{prefix}.1", f"{prefix}.2"),
        case_title="A synthetic manufacturer",
        tool="Optional exact arithmetic",
        scale_axis="Number of production units",
        verification="Check feasibility and all excluded activities.",
    )


def bank_text(chapters):
    chunks = ["# Publication problem bank\n"]
    for chapter in chapters:
        chunks.append(f"# {chapter.chapter}\n")
        for problem in chapter.problems:
            chunks.append(
                f"## {problem.identifier} | {problem.level} | {problem.title}\n\n"
                + "\n\n".join(problem.paragraphs)
                + "\n\n"
            )
    return "\n".join(chunks)


def manuscript(chapters):
    chunks = ["\\begin_document\n\\begin_body\n"]
    for chapter in chapters:
        chunks.append(
            f"\\begin_layout Chapter\n{chapter.chapter}\n\\end_layout\n\n"
            "\\begin_layout Standard\nPreserved teaching text.\n\\end_layout\n\n"
        )
    chunks.append("\\end_body\n\\end_document\n")
    return "".join(chunks)


class AdvancedProblemProgramTests(unittest.TestCase):
    def test_code_spans_are_native_typewriter_with_literal_command_options(self):
        value = inject.lyx_inline("Run `python3 work/blp_case.py --check` and compare $s_1$.")
        self.assertEqual(value.count("\\family typewriter\n"), 1)
        self.assertEqual(value.count("\\family default\n"), 1)
        self.assertIn("python3 work/blp_case.py --check", value)
        self.assertNotIn("`", value)
        self.assertIn("\\begin_inset Formula $s_1$\\end_inset", value)

    def test_live_catalog_covers_each_advanced_question_and_resolves_sources(self):
        bank = inject.parse_problem_bank(practice.PROBLEM_BANK)
        advanced = {p.identifier: p for chapter in bank for p in chapter.problems if p.level == "Advanced"}
        directory = practice.PROBLEM_BANK.parent
        with (directory / "ADVANCED_PROBLEM_CATALOG.tsv").open(encoding="utf-8", newline="") as handle:
            catalog = list(csv.DictReader(handle, delimiter="\t"))
        with (directory / "ADVANCED_SOURCE_CATALOG.tsv").open(encoding="utf-8", newline="") as handle:
            sources = list(csv.DictReader(handle, delimiter="\t"))
        source_ids = [row["reference_id"] for row in sources]
        self.assertEqual(len(source_ids), len(set(source_ids)))
        self.assertEqual(len(catalog), len(advanced))
        self.assertEqual({row["id"] for row in catalog}, set(advanced))
        for row in catalog:
            with self.subTest(identifier=row["id"]):
                self.assertEqual(row["title"], advanced[row["id"]].title)
                self.assertGreater(int(row["minutes"]), 0)
                self.assertTrue(row["relationship"].strip())
                for reference in row["reference_ids"].split(","):
                    self.assertIn(reference.strip(), source_ids)

    def test_archive_difficulty_notes_require_actual_restored_id(self):
        chapter = sample_chapter()
        self.assertIsNone(inject.advanced_difficulty_note(chapter.problems))
        for identifier, phrase in (
            ("9.A5", "Western 2017"),
            ("10.A5", "Western 2019"),
            ("11.A7", "Western 2018"),
        ):
            with self.subTest(identifier=identifier):
                restored = inject.Problem(identifier, "Advanced", "Restored", ("Question.",))
                self.assertIn(phrase, inject.advanced_difficulty_note((restored,)))

    def test_both_books_share_the_same_archive_difficulty_note(self):
        chapter = sample_chapter()
        restored = inject.Problem("9.A5", "Advanced", "Restored", ("Question.",))
        chapter = replace(chapter, problems=chapter.problems + (restored,))
        note = inject.advanced_difficulty_note(chapter.problems)
        self.assertIn(note, inject.problem_block(chapter, sample_pathway()))
        self.assertIn(note, practice.render_chapter(chapter, sample_pathway()))

    def parse(self, content):
        with tempfile.TemporaryDirectory(prefix="econ803-advanced-tests-") as directory:
            path = Path(directory) / "synthetic_bank.md"
            path.write_text(content, encoding="utf-8")
            return inject.parse_problem_bank(path)

    def parse_advanced_plan(self, content, chapters=None):
        with tempfile.TemporaryDirectory(prefix="econ803-advanced-plan-tests-") as directory:
            path = Path(directory) / "synthetic_advanced_plan.tsv"
            path.write_text(content, encoding="utf-8")
            return inject.parse_advanced_plan(path, chapters or [sample_chapter()])

    def test_parser_accepts_native_advanced_ids_and_preserves_bank_order(self):
        chapters = [
            sample_chapter("9", "Production"),
            sample_chapter("10", "Partial Equilibrium"),
            sample_chapter("11", "General Equilibrium"),
        ]
        parsed = self.parse(bank_text(chapters))
        self.assertEqual(parsed, chapters)
        for prefix, chapter in zip(("9", "10", "11"), parsed):
            with self.subTest(prefix=prefix):
                advanced = [p.identifier for p in chapter.problems if p.level == "Advanced"]
                self.assertEqual(advanced, [f"{prefix}.A1", f"{prefix}.A2"])

    def test_parser_rejects_duplicate_advanced_identifier(self):
        chapter = sample_chapter()
        duplicate = inject.ChapterProblems(
            chapter.chapter, chapter.problems + (chapter.problems[1],)
        )
        with self.assertRaisesRegex(ValueError, "duplicate problem identifier"):
            self.parse(bank_text([duplicate]))

    def test_parser_rejects_unknown_level_instead_of_silently_grouping_it(self):
        chapter = sample_chapter()
        invalid = inject.ChapterProblems(
            chapter.chapter,
            chapter.problems
            + (inject.Problem("9.A3", "Advance", "Misspelled label", ("Text.",)),),
        )
        with self.assertRaisesRegex(ValueError, "unknown level.*9.A3.*Advance"):
            self.parse(bank_text([invalid]))

    def test_expected_order_is_hand_advanced_bridge_then_existing_case(self):
        self.assertEqual(
            inject.expected_problem_order(sample_chapter(), sample_pathway()),
            ("9.1", "9.A1", "9.A2", "9.2", "9.4"),
        )

    def test_advanced_section_is_between_hand_practice_and_part_two(self):
        block = inject.problem_block(sample_chapter(), sample_pathway())
        tokens = [
            "Part I: By hand",
            "Problem 9.1 [Core]",
            "Advanced exam practice",
            "Problem 9.A1 [Advanced]",
            "Problem 9.A2 [Advanced]",
            "Part II:",
            "Problem 9.2 [Proof]",
            "Chapter use case",
            "Problem 9.4 [Applied]",
        ]
        positions = [block.index(token) for token in tokens]
        self.assertEqual(positions, sorted(positions))
        self.assertEqual(block.count("Advanced exam practice"), 1)
        self.assertEqual(
            re.findall(PROBLEM_PATTERN, block),
            ["9.1", "9.A1", "9.A2", "9.2", "9.4"],
        )
        self.assertIn("before using tools", block)

    def test_existing_case_remains_last_even_if_it_has_core_level(self):
        original = sample_chapter()
        problems = tuple(
            inject.Problem(p.identifier, "Core", p.title, p.paragraphs)
            if p.identifier == "9.4" else p
            for p in original.problems
        )
        chapter = inject.ChapterProblems(original.chapter, problems)
        block = inject.problem_block(chapter, sample_pathway())
        self.assertEqual(re.findall(PROBLEM_PATTERN, block)[-1], "9.4")
        self.assertEqual(block.count("Problem 9.4 [Core]"), 1)

    def test_advanced_designated_case_is_rendered_once_and_last(self):
        chapter = sample_chapter()
        pathway = replace(sample_pathway(), case_id="9.A2")
        expected = ("9.1", "9.A1", "9.4", "9.2", "9.A2")
        self.assertEqual(inject.expected_problem_order(chapter, pathway), expected)
        hand, advanced, bridges, case = practice.ordered_chapter_problems(chapter, pathway)
        self.assertEqual([p.identifier for p in advanced], ["9.A1"])
        self.assertEqual(case.identifier, "9.A2")
        for rendered in (
            inject.problem_block(chapter, pathway),
            practice.render_chapter(chapter, pathway),
        ):
            with self.subTest(renderer=rendered.splitlines()[0]):
                self.assertEqual(tuple(re.findall(PROBLEM_PATTERN, rendered)), expected)
                self.assertEqual(rendered.count("Problem 9.A2 [Advanced]"), 1)
        source = inject.inject(manuscript([chapter]), [chapter], {chapter.chapter: pathway})
        inject.validate_generated_source(source, [chapter], {chapter.chapter: pathway})
        self.assertEqual(
            source,
            inject.inject(source, [chapter], {chapter.chapter: pathway}),
        )

    def test_advanced_plan_maps_every_id_once_across_both_columns(self):
        result = self.parse_advanced_plan(
            "set\trecommended_ids\tfurther_practice_ids\n"
            "PS08\t9.A1\t\n"
            "PS09\t\t9.A2\n"
        )
        self.assertEqual(result, {"PS08": ("9.A1", ""), "PS09": ("", "9.A2")})

    def test_advanced_plan_rejects_missing_identifier(self):
        with self.assertRaisesRegex(ValueError, "every Advanced ID exactly once"):
            self.parse_advanced_plan(
                "set\trecommended_ids\tfurther_practice_ids\nPS08\t9.A1\t\n"
            )

    def test_advanced_plan_rejects_duplicate_identifier(self):
        for rows in (
            "PS08\t9.A1,9.A1\t9.A2\n",
            "PS08\t9.A1\t9.A2\nPS09\t9.A1\t\n",
            "PS08\t9.A1,9.A2\t9.A2\n",
        ):
            with self.subTest(rows=rows):
                with self.assertRaisesRegex(ValueError, "every Advanced ID exactly once"):
                    self.parse_advanced_plan("set\trecommended_ids\tfurther_practice_ids\n" + rows)

    def test_advanced_plan_rejects_nonadvanced_identifier(self):
        with self.assertRaisesRegex(ValueError, "every Advanced ID exactly once"):
            self.parse_advanced_plan(
                "set\trecommended_ids\tfurther_practice_ids\n"
                "PS08\t9.A1,9.A2\t9.1\n"
            )

    def test_advanced_plan_rejects_duplicate_or_unknown_week(self):
        for rows in (
            "PS08\t9.A1\t\nPS08\t9.A2\t\n",
            "PS99\t9.A1\t9.A2\n",
        ):
            with self.subTest(rows=rows):
                with self.assertRaisesRegex(ValueError, "duplicate or unknown advanced practice week"):
                    self.parse_advanced_plan("set\trecommended_ids\tfurther_practice_ids\n" + rows)

    def test_no_advanced_heading_when_chapter_has_no_advanced_problems(self):
        original = sample_chapter()
        chapter = inject.ChapterProblems(
            original.chapter, tuple(p for p in original.problems if p.level != "Advanced")
        )
        block = inject.problem_block(chapter, sample_pathway())
        self.assertNotIn("Advanced exam practice", block)
        self.assertEqual(re.findall(PROBLEM_PATTERN, block), ["9.1", "9.2", "9.4"])
        self.assertNotIn("Advanced exam practice", practice.render_chapter(chapter, sample_pathway()))

    def test_injection_is_idempotent_and_keeps_each_chapter_case_last(self):
        chapters = [
            sample_chapter("9", "Production"),
            sample_chapter("10", "Partial Equilibrium"),
            sample_chapter("11", "General Equilibrium"),
        ]
        pathways = {
            chapter.chapter: sample_pathway(prefix, chapter.chapter)
            for prefix, chapter in zip(("9", "10", "11"), chapters)
        }
        initial = manuscript(chapters)
        once = inject.inject(initial, chapters, pathways)
        twice = inject.inject(once, chapters, pathways)
        self.assertEqual(once, twice)
        inject.validate_generated_source(once, chapters, pathways)
        self.assertEqual(once.count("Preserved teaching text."), 3)
        for prefix, chapter in zip(("9", "10", "11"), chapters):
            with self.subTest(prefix=prefix):
                self.assertEqual(once.count(f"Problem {prefix}.A1 [Advanced]"), 1)
                self.assertEqual(once.count(f"Problem {prefix}.A2 [Advanced]"), 1)
                start, end = next(
                    (start, end)
                    for title, start, end in inject.chapter_spans(once)
                    if title == chapter.chapter
                )
                self.assertEqual(re.findall(PROBLEM_PATTERN, once[start:end])[-1], f"{prefix}.4")

    def test_validator_detects_duplicate_problem_outside_generated_block(self):
        chapter = sample_chapter()
        pathways = {chapter.chapter: sample_pathway()}
        source = inject.inject(manuscript([chapter]), [chapter], pathways)
        source = source.replace(
            "Preserved teaching text.",
            "Preserved teaching text.\n\\series bold\nProblem 9.A1 [Advanced]. Stale copy.",
            1,
        )
        with self.assertRaisesRegex(ValueError, "outside the generated chapter blocks"):
            inject.validate_generated_source(source, [chapter], pathways)

    def test_practice_grouping_retains_advanced_category_and_case_identity(self):
        hand, advanced, bridges, case = practice.ordered_chapter_problems(
            sample_chapter(), sample_pathway()
        )
        self.assertEqual([p.identifier for p in hand], ["9.1"])
        self.assertEqual([p.identifier for p in advanced], ["9.A1", "9.A2"])
        self.assertEqual([p.identifier for p in bridges], ["9.2"])
        self.assertEqual(case.identifier, "9.4")

    def test_practice_renderer_includes_advanced_sections_once_before_case(self):
        rendered = practice.render_chapter(sample_chapter(), sample_pathway())
        self.assertIn("\\begin_layout Section*\nAdvanced exam practice", rendered)
        self.assertIn("not extra weekly", rendered)
        self.assertIn("before using tools", rendered)
        self.assertEqual(rendered.count("Advanced exam practice"), 1)
        self.assertEqual(
            re.findall(PROBLEM_PATTERN, rendered),
            ["9.1", "9.A1", "9.A2", "9.2", "9.4"],
        )
        self.assertLess(rendered.index("Advanced exam practice"), rendered.index("Part II:"))
        self.assertLess(rendered.index("Problem 9.A2"), rendered.index("Problem 9.4"))
        self.assertIn("\\begin_inset Formula $q\\geq0$", rendered)


if __name__ == "__main__":
    unittest.main(verbosity=2)
