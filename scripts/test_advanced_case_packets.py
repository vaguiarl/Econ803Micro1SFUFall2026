#!/usr/bin/env python3
"""Synthetic checks that standalone packets stay faithful to the public bank."""

from dataclasses import replace
import unittest

import build_advanced_case_packets as packets
from inject_problem_sets import ChapterProblems, Problem


HEADER = "\\begin_document\n\\textclass book\n\\begin_preamble\n\\newcommand{\\secret}{discard}\n\\end_preamble\n\\spacing double\n\\begin_modules\ntheorems-chap\n\\end_modules\n\\begin_body\n\\end_body\n\\end_document\n"


class AdvancedCasePackets(unittest.TestCase):
    def setUp(self):
        self.problems = (
            Problem("16.A1", "Advanced", "Theory", ("Part I. By hand.", "Unique seed $q>0$.", "Part II. Codex and verification.", "Check the seed.")),
            Problem("16.A2", "Advanced", "Case", ("Case prompt.",)),
        )
        self.chapters = (ChapterProblems("Synthetic chapter", self.problems),)

    def test_packet_preserves_selected_order_and_question_text(self):
        result = packets.build_packet(packets.PACKETS[0], self.chapters, HEADER)
        self.assertLess(result.index("Problem 16.A1."), result.index("Problem 16.A2."))
        self.assertIn("Unique seed \\begin_inset Formula $q>0$", result)
        self.assertIn("Case prompt.", result)
        self.assertEqual(result.count("Part I. By hand"), 1)
        self.assertEqual(result.count("Part II. Codex and verification"), 1)
        self.assertEqual(result.count("clearpage"), 1)

    def test_native_article_header_is_not_the_book_preamble(self):
        result = packets.article_header(HEADER)
        self.assertIn("\\textclass article", result)
        self.assertIn("\\spacing onehalf", result)
        self.assertNotIn("theorems-chap", result)
        self.assertNotIn("secret", result)

    def test_missing_duplicate_or_wrong_level_is_rejected(self):
        for problems in (
            self.problems[:1],
            self.problems + (self.problems[0],),
            (replace(self.problems[0], level="Core"), self.problems[1]),
        ):
            with self.subTest(problems=problems), self.assertRaises(ValueError):
                packets.select_problems((ChapterProblems("Synthetic", problems),), ("16.A1", "16.A2"))

    def test_unselected_question_is_excluded(self):
        packet = replace(packets.PACKETS[0], identifiers=("16.A2",))
        result = packets.build_packet(packet, self.chapters, HEADER)
        self.assertIn("Problem 16.A2.", result)
        self.assertNotIn("Unique seed", result)
        self.assertNotIn("clearpage", result)


if __name__ == "__main__":
    unittest.main(verbosity=2)
