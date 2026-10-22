#!/usr/bin/env python3
"""Read only and in memory tests for permanent IDs and physical GE grouping."""

from __future__ import annotations

from dataclasses import replace
from pathlib import Path
import re
import tempfile
import unittest
from unittest.mock import patch

import build_practice_book as practice
import inject_problem_sets as inject


ROOT = Path(__file__).resolve().parents[1]
GE_TOPICS = (
    "General Equilibrium Theory",
    "Positive Theory of Equilibrium",
    "Testable Restrictions on the Equilibrium Manifold",
)
PROBLEM_RE = r"\\series bold\nProblem ([A-Z0-9]+\.A?[0-9]+) \["


class GeneralEquilibriumGroupingTests(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapters = inject.parse_problem_bank(practice.PROBLEM_BANK)
        cls.pathways = inject.parse_chapter_pathways(practice.PATHWAYS, cls.chapters)
        cls.groups = inject.parse_book_chapter_groups(practice.CHAPTER_GROUPS, cls.chapters)
        cls.physical = inject.printed_chapter_groups(cls.chapters, cls.groups)
        cls.reserve = practice.parse_reserve_bank()

    def manuscript(self):
        pieces = ["\\begin_document\n\\begin_body\n"]
        for title, topics in self.physical:
            if title == "Sequential Trade":
                pieces.append(practice.layout("Part", "Advanced Equilibrium Applications"))
            if title == "Order Theory":
                pieces.append(practice.ert("appendix"))
            pieces.append(practice.layout("Chapter", title))
            pieces.extend(
                practice.layout("Standard", "Preserved narrative for " + topic.chapter + ".")
                for topic in topics
            )
        pieces.append("\\end_body\n\\end_document\n")
        return "\n".join(pieces)

    def injected(self):
        return inject.inject(self.manuscript(), self.chapters, self.pathways, self.groups)

    def test_full_ledger_is_ordered_and_groups_only_three_ge_topics(self):
        self.assertEqual(list(self.groups), [chapter.chapter for chapter in self.chapters])
        combined = [(title, topics) for title, topics in self.physical if len(topics) > 1]
        self.assertEqual(len(combined), 1)
        self.assertEqual(combined[0][0], "General Equilibrium")
        self.assertEqual(tuple(topic.chapter for topic in combined[0][1]), GE_TOPICS)
        self.assertEqual(len(self.physical), len(self.chapters) - 2)
        for title, topics in self.physical:
            if title != "General Equilibrium":
                self.assertEqual(len(topics), 1)
                self.assertEqual(title, topics[0].chapter)

    def test_injection_is_idempotent_and_all_91_ids_remain_exact(self):
        once = self.injected()
        twice = inject.inject(once, self.chapters, self.pathways, self.groups)
        self.assertEqual(once, twice)
        self.assertEqual(once.count("Preserved narrative for "), len(self.chapters))
        expected = [
            identifier
            for chapter in self.chapters
            for identifier in inject.expected_problem_order(chapter, self.pathways[chapter.chapter])
        ]
        self.assertEqual(len(expected), 91)
        self.assertEqual(re.findall(PROBLEM_RE, once), expected)
        self.assertEqual(once.count("ECON803_PROBLEMS_START:"), len(self.chapters))
        self.assertEqual(len(self.reserve), 10)

    def test_one_problems_section_at_end_of_physical_ge_chapter(self):
        source = self.injected()
        _, start, end = next(span for span in inject.chapter_spans(source) if span[0] == "General Equilibrium")
        body = source[start:end]
        problems_start = body.index(practice.layout("Section", "Problems"))
        self.assertNotIn("Preserved narrative", body[problems_start:])
        self.assertEqual(body.count(practice.layout("Section", "Problems")), 1)
        for name in GE_TOPICS:
            self.assertEqual(body.count(practice.layout("Subsection*", self.groups[name].topic_heading)), 1)
        self.assertEqual(body.count(practice.layout("Subsubsection*", "Part I: By hand")), 3)
        self.assertEqual(body.count("\\begin_layout Chapter\n"), 1)

    def test_each_group_keeps_exact_order_and_its_case_last(self):
        source = self.injected()
        for chapter in self.chapters:
            start, _ = inject.marker_span(source, "ECON803_PROBLEMS_START:" + inject.slug(chapter.chapter))
            _, end = inject.marker_span(source, "ECON803_PROBLEMS_END:" + inject.slug(chapter.chapter))
            headings = re.findall(PROBLEM_RE, source[start:end])
            self.assertEqual(tuple(headings), inject.expected_problem_order(chapter, self.pathways[chapter.chapter]))
            self.assertEqual(headings[-1], self.pathways[chapter.chapter].case_id)

    def test_validator_rejects_narrative_between_grouped_blocks(self):
        source = self.injected()
        _, end = inject.marker_span(source, "ECON803_PROBLEMS_END:" + inject.slug(GE_TOPICS[0]))
        broken = source[:end] + "\n\n" + practice.layout("Standard", "Misplaced chapter narrative.") + source[end:]
        with self.assertRaisesRegex(ValueError, "not consecutive"):
            inject.validate_generated_source(broken, self.chapters, self.pathways, self.groups)

    def test_validator_rejects_a_second_midchapter_problems_section(self):
        source = self.injected()
        broken = source.replace(
            "Preserved narrative for General Equilibrium Theory.",
            "Preserved narrative for General Equilibrium Theory.\n\\end_layout\n"
            + practice.layout("Section", "Problems") + "\\begin_layout Standard\n",
            1,
        )
        with self.assertRaisesRegex(ValueError, "invalid Problems section"):
            inject.validate_generated_source(broken, self.chapters, self.pathways, self.groups)

    def test_ledger_rejects_missing_out_of_order_and_nonconsecutive_topics(self):
        missing = dict(self.groups)
        del missing[GE_TOPICS[1]]
        out_of_order = dict(reversed(list(self.groups.items())))
        nonconsecutive = dict(self.groups)
        name = "Matching"
        nonconsecutive[name] = replace(nonconsecutive[name], printed_chapter="General Equilibrium")
        for groups in (missing, out_of_order, nonconsecutive):
            with self.subTest(groups=groups), self.assertRaises(ValueError):
                inject.printed_chapter_groups(self.chapters, groups)

    def test_ledger_parser_rejects_duplicate_rows_and_unsafe_fields(self):
        canonical = practice.CHAPTER_GROUPS.read_text(encoding="utf-8")
        duplicate = canonical + canonical.splitlines()[1] + "\n"
        unsafe = canonical.replace("Exchange, production and welfare", "Exchange\\begin_layout")
        for content in (duplicate, unsafe):
            with tempfile.TemporaryDirectory(prefix="econ803-grouping-test-") as directory:
                target = Path(directory) / "groups.tsv"
                target.write_text(content, encoding="utf-8")
                with self.assertRaises(ValueError):
                    inject.parse_book_chapter_groups(target, self.chapters)

    def test_practice_build_has_one_ge_chapter_91_ids_and_10_reserve_ids(self):
        # Build only in memory. Never read or rewrite the manuscript being
        # edited, and never touch generated LyX or PDF artifacts.
        with patch.object(practice, "make_header", return_value="\\begin_document\n"):
            source = practice.build()
        self.assertEqual(source.count(practice.layout("Chapter", "General Equilibrium")), 1)
        for title in GE_TOPICS:
            self.assertNotIn(practice.layout("Chapter", title), source)
            self.assertEqual(source.count(practice.layout("Section", self.groups[title].topic_heading)), 1)
        self.assertEqual(len(re.findall(PROBLEM_RE, source)), 91)
        reserve_ids = re.findall(r"\\series bold\nProblem (R[0-9]+) \[", source)
        self.assertEqual(len(reserve_ids), 10)
        self.assertEqual(len(set(reserve_ids)), 10)
        self.assertIn("Problem identifiers are permanent catalog labels.", source)
        self.assertNotIn("solutions", source.lower())

    def test_practice_part_boundary_moves_after_entire_ge_chapter(self):
        with patch.object(practice, "make_header", return_value="\\begin_document\n"):
            source = practice.build()
        boundary = source.index(practice.layout("Part", "Advanced Equilibrium Applications"))
        self.assertLess(source.index("Problem 13.3 [Applied]"), boundary)
        self.assertLess(boundary, source.index(practice.layout("Chapter", "Sequential Trade")))
        for topic in GE_TOPICS:
            case_id = self.pathways[topic].case_id
            self.assertLess(source.index("Problem " + case_id + " ["), boundary)


if __name__ == "__main__":
    unittest.main(verbosity=2)
