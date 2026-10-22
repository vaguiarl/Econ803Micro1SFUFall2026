#!/usr/bin/env python3
"""Keep the research chapter aligned without changing released question IDs."""

from __future__ import annotations

import csv
import json
from pathlib import Path
import re
import unittest
from unittest.mock import patch

import build_practice_book as practice
import inject_problem_sets as inject
from validate_theorem_pairs import CURRENT_CHAPTER_BY_PAIR


ROOT = Path(__file__).resolve().parents[1]
CHAPTER_SEQUENCE = (
    "General Equilibrium",
    "Niche Consumption and Product Space",
    "Sequential Trade",
    "Matching",
    "Computable General Equilibrium",
)
PROBLEM_RE = r"\\series bold\nProblem ([A-Z0-9]+(?:\.A?[0-9]+)?) \["
GUIDE_REFERENCES = {
    "3.1": "A two-observation WARP test",
    "3.3": "Afriat inequalities by hand",
    "6.1": "Logit odds and IIA",
    "8.1": "Gorman aggregation",
    "8.2": "Aggregation under common homothetic preferences",
    "11.A4": "Redistribution moves prices but does not resize the box",
    "13.1": "Equilibrium Afriat feasibility",
    "15.1": "Deferred acceptance by hand",
}


class NicheChapterPlacement(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.chapters = inject.parse_problem_bank(practice.PROBLEM_BANK)
        cls.pathways = inject.parse_chapter_pathways(practice.PATHWAYS, cls.chapters)
        cls.groups = inject.parse_book_chapter_groups(practice.CHAPTER_GROUPS, cls.chapters)
        cls.reserve = practice.parse_reserve_bank()
        with patch.object(practice, "make_header", return_value="\\begin_document\n"):
            cls.source = practice.build()

    def test_practice_chapters_have_the_same_numbered_order_as_the_textbook(self):
        titles = re.findall(r"\\begin_layout Chapter\n(.*?)\n\\end_layout", self.source, re.S)
        self.assertEqual(tuple(titles[10:15]), CHAPTER_SEQUENCE)
        boundary = self.source.index(practice.layout("Part", "Advanced Equilibrium Applications"))
        self.assertLess(self.source.index("Problem 13.3 [Applied]"), boundary)
        self.assertLess(boundary, self.source.index(practice.layout("Chapter", practice.NICHE_CHAPTER)))
        self.assertEqual(self.source.count(practice.layout("Chapter", practice.NICHE_CHAPTER)), 1)

    def test_live_textbook_has_the_same_research_chapter_placement(self):
        source = practice.MAIN_BOOK.read_text(encoding="utf-8")
        titles = [title for title, _, _ in inject.chapter_spans(source)]
        self.assertEqual(tuple(titles[10:15]), CHAPTER_SEQUENCE)

    def test_all_91_canonical_and_10_reserve_ids_keep_their_existing_order(self):
        canonical = [
            identifier
            for chapter in self.chapters
            for identifier in inject.expected_problem_order(chapter, self.pathways[chapter.chapter])
        ]
        reserve = [problem.identifier for problem in self.reserve]
        self.assertEqual(len(canonical), 91)
        self.assertEqual(len(reserve), 10)
        self.assertEqual(re.findall(PROBLEM_RE, self.source), canonical + reserve)
        self.assertEqual(len(set(canonical + reserve)), 101)
        self.assertNotIn(practice.NICHE_CHAPTER, self.groups)

    def test_reading_guide_refers_only_to_existing_work_and_does_not_assign_more(self):
        guide = practice.render_niche_reading_guide()
        problems = {p.identifier: p for chapter in self.chapters for p in chapter.problems}
        for identifier, title in GUIDE_REFERENCES.items():
            self.assertEqual(problems[identifier].title, title)
            self.assertIn(identifier, guide)
        self.assertIn("research synthesis with no additional weekly assignment", guide)
        self.assertEqual(re.findall(PROBLEM_RE, guide), [])
        self.assertNotIn("solutions", guide.lower())
        self.assertNotIn("answer key", guide.lower())

    def test_validator_rejects_missing_or_displaced_research_chapter(self):
        guide = practice.render_niche_reading_guide()
        missing = self.source.replace(guide, "", 1)
        sequential = practice.layout("Chapter", "Sequential Trade")
        displaced = missing.replace(sequential, sequential + "\n" + guide, 1)
        for source in (missing, displaced):
            with self.subTest(source=source[:50]), self.assertRaisesRegex(ValueError, "printed chapter grouping"):
                practice.validate_source(source, self.chapters, self.reserve, self.groups)

    def test_formal_current_locations_shift_but_permanent_ids_do_not(self):
        expected = {
            "TS-C13-ARROW-RADNER": "13",
            "TS-C14-GALE-SHAPLEY": "14",
            "TS-C14-TTC": "14",
        }
        with (ROOT / "formal/theorem_pairs.tsv").open(encoding="utf-8", newline="") as handle:
            rows = {row["pair_id"]: row for row in csv.DictReader(handle, delimiter="\t")}
        coverage = json.loads((ROOT / "formal/coverage.json").read_text(encoding="utf-8"))
        targets = {item["id"]: item for item in coverage["targets"]}
        for identifier, chapter in expected.items():
            self.assertEqual(rows[identifier]["chapter"], chapter)
            self.assertEqual(CURRENT_CHAPTER_BY_PAIR[identifier], chapter)
            self.assertTrue(targets[identifier.removeprefix("TS-")]["book_ref"].startswith("Chapter " + chapter + ","))


if __name__ == "__main__":
    unittest.main(verbosity=2)
