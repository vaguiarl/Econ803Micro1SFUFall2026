#!/usr/bin/env python3
"""Regression checks for the worked equilibrium illustrations, not a proof engine.

Analytical arguments remain in the LyX text. Exact finite identities guard the
figure coordinates and accounting; sampled inequalities are supplementary.
No private assessment solutions or student information belong in this file.
"""

from fractions import Fraction as F
from math import sqrt
import unittest


class EquilibriumIllustrations(unittest.TestCase):
    def test_edgeworth_opposite_origins_and_shared_budget(self):
        totals = (F(4), F(4))
        prices = (F(2), F(1))
        endowments = ((F(1), F(3)), (F(3), F(1)))
        wealth = tuple(sum(prices[j] * w[j] for j in range(2))
                       for w in endowments)
        self.assertEqual(wealth, (5, 7))
        for bundle1 in ((F(1, 2), F(4)), (F(1), F(3)),
                        (F(5, 2), F(0))):
            bundle2 = tuple(totals[j] - bundle1[j] for j in range(2))
            self.assertEqual(sum(prices[j] * bundle1[j] for j in range(2)), wealth[0])
            self.assertEqual(sum(prices[j] * bundle2[j] for j in range(2)), wealth[1])
        # Feasibility gives p*x2 = p*totals - p*x1. Thus the same
        # line bounds opposite affordable sides, not two identical budgets.
        for a, b in ((F(1), F(1)), (F(1), F(3)), (F(3), F(3))):
            cost1 = prices[0] * a + prices[1] * b
            cost2 = prices[0] * (4-a) + prices[1] * (4-b)
            self.assertEqual(cost1 + cost2, sum(wealth))
            self.assertEqual(cost2 <= wealth[1], cost1 >= wealth[0])
        self.assertEqual(-prices[0] / prices[1], -2)

    def test_edgeworth_redistribution_and_tangencies(self):
        original = ((F(1), F(3)), (F(3), F(1)))
        redistributed = ((F(1, 2), F(5, 2)), (F(7, 2), F(3, 2)))
        transfers = tuple(sum(redistributed[i]) - sum(original[i])
                          for i in range(2))
        self.assertEqual(transfers, (-1, 1))
        self.assertEqual(sum(transfers), 0)
        for endowments, expected in ((original, F(2)), (redistributed, F(3, 2))):
            self.assertEqual(tuple(sum(w[j] for w in endowments) for j in range(2)), (4, 4))
            wealth = tuple(sum(w) for w in endowments)
            bundles = tuple((m/2, m/2) for m in wealth)
            self.assertEqual(bundles[0], (expected, expected))
            self.assertEqual(tuple(sum(x[j] for x in bundles) for j in range(2)), (4, 4))
            a, b = bundles[0]
            product1, product2 = a*b, (4-a)*(4-b)
            self.assertEqual(product1/a, b)
            self.assertEqual(4-product2/(4-a), b)
            # Derivatives of the two plotted indifference curves agree with
            # the budget slope. Cobb Douglas demand supplies global optimality.
            self.assertEqual(-product1/a**2, -1)
            self.assertEqual(-product2/(4-a)**2, -1)
            # Exact plot domains keep both indifference curves in the box.
            blue_left = product1/4
            orange_right = 4-product2/4
            self.assertEqual(product1/blue_left, 4)
            self.assertEqual(4-product2/(4-orange_right), 0)
            self.assertTrue(0 <= blue_left <= a <= 4)
            self.assertTrue(0 <= a <= orange_right <= 4)
        self.assertEqual(F(9, 4)/4, F(9, 16))
        self.assertEqual(4-F(25, 4)/4, F(39, 16))

    def test_exchange_walras_and_price_iteration(self):
        for q in (F(1, 4), F(3, 4), F(1), F(3, 2), F(4)):
            z1, z2 = 2 / q - 2, 2 * q - 2
            self.assertEqual(q * z1 + z2, 0)
        step = lambda q: q + F(9, 8) * (2 / q - 2)
        self.assertEqual(step(F(3, 4)), F(3, 2))
        self.assertEqual(step(F(3, 2)), F(3, 4))

    def test_fixed_point_map(self):
        transform = lambda s: s + 1 / (16 * s) - F(1, 8)
        self.assertEqual(transform(F(1, 2)), F(1, 2))
        self.assertEqual(transform(F(1, 4)), F(3, 8))
        self.assertEqual(transform(F(9, 10)), F(38, 45))
        for n in range(10, 91):
            value = transform(F(n, 100))
            self.assertGreaterEqual(value, F(3, 8))
            self.assertLessEqual(value, F(38, 45))

    def test_multiple_root_slopes_and_resource_bounds(self):
        f = lambda q: -(q - 1) * (q - 2) * (q - 3) / (q * (1 + q*q))
        expected = ((F(1), F(-1)), (F(2), F(1, 10)), (F(3), F(-1, 15)))
        for q, slope in expected:
            self.assertEqual(f(q), 0)
            others = [r for r in (1, 2, 3) if r != q]
            self.assertEqual(-(q - others[0]) * (q - others[1]) / (q * (1 + q*q)), slope)
        # These samples check plotted data. The global bounds use the polynomial
        # inequalities proved in the text and are not inferred from this grid.
        for n in range(1, 1001):
            q = F(n, 100)
            self.assertGreater(f(q), -1)
            self.assertGreater(-q * f(q), -6)

    def test_continuum_masses_and_moments(self):
        cutoff = F(1, 2)
        original = F(2, 3)
        lost_mass = cutoff**2
        lost_moment = F(2, 3) * cutoff**3
        remaining = original - lost_moment
        replacement = remaining / (1 - lost_mass)
        self.assertEqual(lost_mass, F(1, 4))
        self.assertEqual(lost_moment, F(1, 12))
        self.assertEqual(remaining, F(7, 12))
        self.assertEqual(replacement, F(7, 9))
        self.assertLess(remaining, original)
        self.assertLess(original, replacement)

    def test_production_support_and_income(self):
        labor_endowment, firm_input, leisure, consumption = 3, 1, 2, 2
        output = 2 * sqrt(firm_input)
        profit = output - firm_input
        self.assertEqual(output, consumption)
        self.assertEqual(leisure + firm_input, labor_endowment)
        self.assertEqual(leisure + consumption, labor_endowment + profit)
        self.assertEqual(leisure * consumption, 4)

    def test_asset_span_and_price(self):
        bond, security = (-1, 2)
        self.assertEqual((bond + security, bond), (1, -1))
        for psi1, psi2 in ((F(1, 3), F(2, 3)), (F(3, 4), F(1, 5))):
            qb, qa = psi1 + psi2, psi1
            self.assertEqual(qb * bond + qa * security, psi1 - psi2)

    def test_replica_core_formula(self):
        for r in range(1, 12):
            s = 2 * r - 1
            radius = 9 / (2 * (5*s + sqrt(25*s*s - 9)))
            # Stable equivalent of (5s-sqrt(25s^2-9))/2.
            self.assertAlmostEqual(4*radius*radius - 20*s*radius + 9, 0)
            for sign in (-1, 1):
                t = 2.5 + sign * radius
                for m in range(r + 1):
                    for n in range(r + 1):
                        if m + n == 0:
                            continue
                        resources = (4*m + n) * (m + 4*n)
                        claim = m*t + n*(5-t)
                        self.assertLessEqual(resources - claim*claim, 1e-9)
        t = F(14, 5)
        # The explicit coalition is one A and two B, exactly exhausting (6,9).
        self.assertEqual(F(12, 5) + 2*F(9, 5), 6)
        self.assertEqual(F(18, 5) + 2*F(27, 10), 9)
        self.assertEqual(F(12, 5)*F(18, 5) - t*t, F(4, 5))
        self.assertEqual(F(9, 5)*F(27, 10) - (5-t)**2, F(1, 50))

    def test_closed_circular_flow(self):
        prices, outputs = (F(2), F(1)), (F(4), F(5))
        wage_bills, rental_bills = (F(4), F(2)), (F(2), F(3))
        profits = tuple(prices[j]*outputs[j] - wage_bills[j] - rental_bills[j] for j in range(2))
        demands = ((F(2), F(4)), (F(2), F(1)))
        household_incomes = (F(2)+F(4)+profits[0], F(4)+F(1)+profits[1])
        for h in range(2):
            self.assertEqual(sum(prices[j]*demands[h][j] for j in range(2)), household_incomes[h])
        for j in range(2):
            self.assertEqual(sum(demands[h][j] for h in range(2)), outputs[j])
        self.assertEqual(sum(prices[j]*outputs[j] for j in range(2)), sum(household_incomes))
        self.assertEqual(sum(wage_bills)+sum(rental_bills)+sum(profits), sum(household_incomes))
        self.assertNotEqual(sum(rental_bills), sum(profits))


if __name__ == "__main__":
    unittest.main(verbosity=2)
