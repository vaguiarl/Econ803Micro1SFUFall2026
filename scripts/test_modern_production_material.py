#!/usr/bin/env python3
"""Exact regression checks for the original production teaching examples.

These tests check finite algebra and source contracts.  They do not certify
the analytic identification theorems or replace their assumptions.
"""

from fractions import Fraction as F
import unittest

import modern_production_material as modern
import modernize_production as migration


def technology_b(z: F) -> F:
    return min(2 * z, F(2, 3) * z + F(4, 3), F(4))


class ModernProductionMaterialTests(unittest.TestCase):
    def test_live_lyx_bridge_precedes_problems_and_preserves_core(self):
        source = migration.BOOK.read_text(encoding="utf-8")
        migration.validate(source)
        start = source.index(migration.heading("Chapter", "Theory of the Firm"))
        stop = source.index(migration.heading("Chapter", "Competitive Markets and Partial Equilibrium"), start)
        chapter = source[start:stop]
        for title in ("Production sets", "Production functions and input substitution", "Profit maximization", "Cost minimization"):
            self.assertIn(migration.heading("Section", title), chapter)
        self.assertEqual(chapter.count('name "sec:production-identification"'), 1)
        self.assertLess(chapter.index(modern.STAMP), chapter.index("ECON803_PROBLEMS_START:theory-of-the-firm"))

    def test_migration_preserves_subsequent_live_edits(self):
        source = migration.BOOK.read_text(encoding="utf-8")
        self.assertEqual(migration.rewrite(source), source)
        edited = source.replace("Empirical production theory asks the reverse question", "Empirical production theory asks the inverse question", 1)
        self.assertNotEqual(edited, source)
        self.assertEqual(migration.rewrite(edited), edited)

    def test_material_is_native_and_does_not_write_main_source(self):
        material = modern.modern_production_blocks()
        self.assertIsInstance(material, str)
        self.assertEqual(material.count("\\begin_layout Section\n"), 1)
        self.assertEqual(material.count("\\begin_layout Subsection\n"), 7)
        self.assertIn('name "sec:production-identification"', material)
        self.assertIn('key "aguiarkashaevallen2023"', material)
        self.assertIn('key "gandhinavarrorivers2020"', material)
        self.assertNotIn("\\begin_layout Chapter\n", material)
        self.assertNotIn("\\begin_inset ERT", material)
        self.assertNotIn("\\n$Y=", material)

    def test_dual_and_set_productivity_precede_scalar_specialization(self):
        source = migration.BOOK.read_text(encoding="utf-8")
        for material in (modern.MODERN_PRODUCTION, source):
            dual = material.index('name "sec:production-dual-measurement"')
            productivity = material.index('name "sec:production-set-productivity"')
            scalar = material.index('Now specialize to one physical output')
            self.assertLess(dual, productivity)
            self.assertLess(productivity, scalar)
            for phrase in (
                'scalar value, not a scalar physical output',
                'partial order on technologies',
                'common prices and common restrictions',
                'strict expansion need not raise value strictly',
                'does not make an ill defined commodity well defined',
                'all supporting prices',
            ):
                self.assertIn(phrase.lower(), material.lower())

    def test_multioutput_expansion_equality_and_unique_choice_switch(self):
        # Each Q is the convex hull of these vertices, so support values
        # are exactly the maximum of three vertex values.
        origin = (F(0), F(0))
        vertices_a = (origin, (F(1), F(0)), (F(0), F(1)))
        vertices_b = (origin, (F(1), F(0)), (F(0), F(2)))
        for q1, q2 in vertices_a:
            self.assertLessEqual(q1 + q2 / 2, 1)
        self.assertGreater(vertices_b[-1][0] + vertices_b[-1][1], 1)

        def values(vertices, prices):
            return tuple(prices[0] * q1 + prices[1] * q2 for q1, q2 in vertices)

        for prices in ((F(0), F(1)), (F(1), F(0)), (F(3), F(1)), (F(3, 2), F(1))):
            self.assertEqual(max(values(vertices_a, prices)), max(prices))
            self.assertEqual(max(values(vertices_b, prices)), max(prices[0], 2 * prices[1]))
            self.assertLessEqual(max(values(vertices_a, prices)), max(values(vertices_b, prices)))
        prices = (F(3), F(1))
        self.assertEqual(max(values(vertices_a, prices)), 3)
        self.assertEqual(max(values(vertices_b, prices)), 3)
        prices = (F(3, 2), F(1))
        va, vb = values(vertices_a, prices), values(vertices_b, prices)
        self.assertEqual([q for q, v in zip(vertices_a, va) if v == max(va)], [(F(1), F(0))])
        self.assertEqual([q for q, v in zip(vertices_b, vb) if v == max(vb)], [(F(0), F(2))])
        self.assertEqual((max(va), max(vb)), (F(3, 2), F(2)))

    def test_multioutput_specialization_reverses_value_rankings(self):
        # B has intercepts (1,2), C has intercepts (2,1).
        # Neither contains the other: use the exclusive axis vertices.
        self.assertGreater(F(2) + F(0) / 2, 1)  # (2,0) not in B
        self.assertGreater(F(0) / 2 + F(2), 1)  # (0,2) not in C
        for p1, p2, vb, vc in ((F(3), F(1), F(3), F(6)), (F(1), F(3), F(6), F(3))):
            self.assertEqual(max(p1, 2 * p2), vb)
            self.assertEqual(max(2 * p1, p2), vc)

    def test_power_technology_profit_share_and_global_gap(self):
        # f(z)=a sqrt(z), use z=u^2 so the global profit gap is a square.
        for price in (F(1, 2), F(1), F(3, 2), F(2)):
            for wage in (F(1, 2), F(1), F(3)):
                for productivity in (F(1), F(2), F(4)):
                    u_star = price * productivity / (2 * wage)
                    z_star = u_star**2
                    q_star = productivity * u_star
                    profit = price * q_star - wage * z_star
                    self.assertEqual(wage * z_star, price * q_star / 2)
                    self.assertEqual(profit, price * q_star / 2)
                    for u in (F(0), F(1, 3), F(1), F(3), F(5)):
                        difference = profit - (price * productivity * u - wage * u**2)
                        self.assertEqual(difference, wage * (u - u_star)**2)

    def test_two_concave_technologies_fit_same_observed_profits(self):
        # Piecewise linear B has slopes 2, 2/3, 0 at knots 0, 1, 4.
        knots = (F(0), F(1), F(4))
        for price, value in ((F(1), F(1)), (F(2), F(4)), (F(3, 2), F(2))):
            profits = [price * technology_b(z) - z for z in knots]
            self.assertEqual(max(profits), value)
            for z in (F(0), F(1, 4), F(1), F(3, 2), F(2), F(4), F(7)):
                self.assertLessEqual(price * technology_b(z) - z, value)
        self.assertEqual(technology_b(F(0)), 0)
        self.assertEqual(technology_b(F(1)), 2)
        self.assertEqual(technology_b(F(4)), 4)
        # A's exact sqrt benchmark is p^2; hence it disagrees at 3/2.
        self.assertEqual(F(3, 2)**2, F(9, 4))
        self.assertLess(F(2), F(9, 4))

    def test_counterfactual_bounds_and_expenditure_inequalities(self):
        counterfactual_price = F(3, 2)
        plans = ((F(1), F(2)), (F(4), F(4)))
        lower = max(counterfactual_price * q - z for z, q in plans)
        upper = (F(1) + F(4)) / 2
        self.assertEqual(lower, F(2))
        self.assertEqual(upper, F(5, 2))
        self.assertLessEqual(lower, F(9, 4))
        self.assertLessEqual(F(9, 4), upper)
        for z, q in plans:
            self.assertLessEqual(q - z, 1)
            self.assertLessEqual(2 * q - z, 4)

    def test_support_scope_and_observation_limits_are_explicit(self):
        material = modern.MODERN_PRODUCTION
        for phrase in (
            "closed, convex and freely disposable",
            "all supporting prices statement",
            "support function cannot distinguish",
            "Homogeneity adds rays",
            "with only profit values",
            "already been identified",
            "not a general identification theorem",
            "is not an endowment",
            "not the same object as a proxy",
            "set both shocks",
        ):
            self.assertIn(phrase.lower(), material.lower())

    def test_one_price_proxy_euler_algebra(self):
        # pi(p,w)=p^2/w, g(v)=v^2: the displayed ratio equals 2/v.
        for price in (F(1, 2), F(1), F(3)):
            for proxy in (F(1, 2), F(1), F(2), F(3)):
                reduced_profit = price**2 / proxy**2
                derivative_price = 2 * price / proxy**2
                derivative_proxy = -2 * price**2 / proxy**3
                denominator = reduced_profit - price * derivative_price
                self.assertLess(denominator, 0)
                self.assertEqual(derivative_proxy / denominator, 2 / proxy)

    def test_two_shock_share_recovery_and_capacity_wedge(self):
        # exp(eps) is 2 or 1/2 with equal probabilities, so E eps=0.
        # Avoid numerical logs: exp(h) is the exact geometric mean.
        level_shocks = (F(2), F(1, 2))
        kappa = sum(level_shocks) / 2
        self.assertEqual(kappa, F(5, 4))
        price, wage, scale = F(4), F(5), F(4)
        root_z = price * scale * kappa / (2 * wage)
        self.assertEqual(root_z**2, 4)
        shares = tuple(wage * root_z**2 / (price * scale * root_z * shock)
                       for shock in level_shocks)
        self.assertEqual(shares, (F(5, 16), F(5, 4)))
        exp_h = F(5, 8)
        self.assertEqual(exp_h**2, shares[0] * shares[1])
        self.assertEqual(tuple(exp_h / s for s in shares), level_shocks)
        self.assertEqual(sum(exp_h / s for s in shares) / 2, kappa)
        self.assertEqual(exp_h / kappa, F(1, 2))
        # At z=1 the omitted capacity multiplier is strictly positive.
        capacity, root_capacity = F(1), F(1)
        multiplier = price * scale * kappa / (2 * root_capacity) - wage
        self.assertEqual(multiplier, 5)
        capped_shares = tuple(wage * capacity / (price * scale * root_capacity * shock)
                              for shock in level_shocks)
        self.assertEqual(capped_shares, (F(5, 32), F(5, 8)))
        capped_exp_h = F(5, 16)
        self.assertEqual(capped_exp_h**2, capped_shares[0] * capped_shares[1])
        self.assertEqual(capped_exp_h / kappa, F(1, 4))
        expected_revenue = price * scale * root_capacity * kappa
        self.assertEqual((wage + multiplier) * capacity, expected_revenue / 2)


if __name__ == "__main__":
    unittest.main()
