#!/usr/bin/env python3
"""Structural and exact finite regression checks for the GE exposition.

These tests do not prove a topological fixed point theorem. The analytic proof
is written in the LyX manuscript; the existing Lean project audits its declared
dependency structure separately.
"""

from fractions import Fraction as F
from pathlib import Path
import re
import unittest

import modernize_general_equilibrium as ge


class GeneralEquilibriumRevision(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.source = ge.BOOK.read_text()

    def test_rewrite_preserves_live_lyx_edits_after_migration(self):
        self.assertEqual(ge.rewrite(self.source), self.source)
        edited = self.source.replace("General equilibrium connects individual choices", "General equilibrium links individual choices", 1)
        self.assertEqual(ge.rewrite(edited), edited)

    def test_one_ge_chapter_and_an_explicit_existence_appendix(self):
        ge.validate(self.source)
        start = self.source.index(ge.heading("Chapter", "General Equilibrium"))
        end = self.source.index(ge.heading("Part", "Advanced Equilibrium Applications"), start)
        body = self.source[start:end]
        self.assertEqual(body.count("\\begin_layout Chapter\n"), 1)
        self.assertEqual(body.count(ge.heading("Section", "Problems")), 1)
        self.assertIn("Brouwer fixed point theorem", body)
        self.assertNotIn("Add a price player", body)
        self.assertLess(body.index("Existence through a continuous price map"), body.index("One consumer and one producer"))
        self.assertLess(body.index("What equilibrium observations can reveal"), body.index(ge.heading("Section", "Problems")))

    def test_all_stable_ge_problems_live_at_chapter_end(self):
        start = self.source.index(ge.heading("Chapter", "General Equilibrium"))
        end = self.source.index(ge.heading("Part", "Advanced Equilibrium Applications"), start)
        body = self.source[start:end]
        ids = re.findall(r"\\series bold\nProblem ((?:11|12|13)\.A?[0-9]+) \[", body)
        self.assertEqual(len(ids), 19)
        self.assertEqual(len(ids), len(set(ids)))
        self.assertNotIn("Problem 16.A", body)

    def test_main_and_appendix_assumption_scopes_are_separate(self):
        self.assertIn("strictly convex and strongly monotone", ge.EXISTENCE)
        self.assertIn("continuous, convex and strongly monotone", ge.APPENDIX)
        self.assertIn("Demand need not be unique", ge.APPENDIX)
        self.assertIn("not claimed as locally Lean verified", ge.APPENDIX)
        self.assertIn("app:ge-existence", ge.EXISTENCE)
        for token in ("thmstar:walrasian-existence", "thmfull:walrasian-existence", "thm:ge-existence-kakutani"):
            position = self.source.index('name "' + token + '"')
            layout = self.source.rfind("\\begin_layout ", 0, position)
            self.assertTrue(self.source[layout:].startswith("\\begin_layout Proposition\n"))
        for asset in ("edgeworth_coordinates", "edgeworth_redistribution"):
            self.assertEqual(self.source.count("filename figures/tikz/" + asset + ".pdf"), 1)

    def test_price_map_simplex_and_affordability_sign_identity(self):
        for prices in ((F(1), F(0)), (F(1, 2), F(1, 2)), (F(1, 3), F(2, 3))):
            for imbalance in ((F(0), F(0)), (F(2), F(-1)), (F(-1), F(2))):
                positive = tuple(max(z, 0) for z in imbalance)
                total = sum(positive)
                update = tuple((p+a)/(1+total) for p,a in zip(prices, positive))
                self.assertEqual(sum(update), 1)
                self.assertTrue(all(p >= 0 for p in update))
            # A hypothetical positive S fixed point forces z_l=S*p_l
            # on the positive price support, hence positive expenditure.
            for total in (F(1, 3), F(2)):
                z = tuple(total*p if p else F(-1) for p in prices)
                value = sum(p*v for p,v in zip(prices,z))
                self.assertEqual(value, total*sum(p*p for p in prices))
                self.assertGreater(value, 0)


if __name__ == "__main__":
    unittest.main(verbosity=2)
