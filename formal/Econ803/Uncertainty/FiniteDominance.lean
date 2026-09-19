import Mathlib.Algebra.Order.BigOperators.Group.Finset
import Mathlib.Algebra.BigOperators.Ring.Finset
import Mathlib.Data.Real.Basic

/-!
# Finite stochastic dominance

For finite ordered prize spaces, a monotone coupling is a directly checkable
certificate for the expected-utility implication of first-order stochastic
dominance. The converse from cumulative-distribution inequalities to such a
coupling is intentionally a separate future target.
-/

set_option autoImplicit false

open scoped BigOperators

namespace Econ803.Uncertainty

variable {Z : Type*}

def ExpectedUtility [Fintype Z] (p : Z → ℝ) (u : Z → ℝ) : ℝ :=
  ∑ z, p z * u z

def HasMarginals [Fintype Z]
    (κ : Z → Z → ℝ) (p q : Z → ℝ) : Prop :=
  (∀ x, ∑ y, κ x y = p x) ∧ (∀ y, ∑ x, κ x y = q y)

def IsMonotoneCoupling [Fintype Z] [Preorder Z]
    (κ : Z → Z → ℝ) : Prop :=
  (∀ x y, 0 ≤ κ x y) ∧ (∀ x y, κ x y ≠ 0 → y ≤ x)

/-- A monotone coupling transports the pointwise monotonicity of Bernoulli
utility to the expected-utility inequality. -/
theorem monotoneCoupling_implies_expectedUtility_order
    [Fintype Z] [Preorder Z]
    (p q : Z → ℝ) (κ : Z → Z → ℝ)
    (hmarg : HasMarginals κ p q)
    (hκ : IsMonotoneCoupling κ)
    (u : Z → ℝ) (hu : Monotone u) :
    ExpectedUtility q u ≤ ExpectedUtility p u := by
  calc
    ExpectedUtility q u = ∑ y, ∑ x, κ x y * u y := by
      unfold ExpectedUtility
      apply Finset.sum_congr rfl
      intro y _hy
      rw [← hmarg.2 y, Finset.sum_mul]
    _ = ∑ x, ∑ y, κ x y * u y := by
      rw [Finset.sum_comm]
    _ ≤ ∑ x, ∑ y, κ x y * u x := by
      apply Finset.sum_le_sum
      intro x _hx
      apply Finset.sum_le_sum
      intro y _hy
      by_cases hzero : κ x y = 0
      · simp [hzero]
      · exact mul_le_mul_of_nonneg_left (hu (hκ.2 x y hzero)) (hκ.1 x y)
    _ = ExpectedUtility p u := by
      unfold ExpectedUtility
      apply Finset.sum_congr rfl
      intro x _hx
      rw [← hmarg.1 x, Finset.sum_mul]

end Econ803.Uncertainty
