import WGARP.JustifiableDichotomy
import Mathlib.Tactic.Linarith

/-!
# Budgets and ordinary demand

The basic demand results are stated with the exact finite-dimensional objects
used by the pinned WGARP library. This avoids a second, incompatible notion of
a commodity bundle.
-/

set_option autoImplicit false

open scoped BigOperators

namespace Econ803.Consumer

abbrev Bundle (L : ℕ) := WGARP.Bundle L
abbrev Utility (L : ℕ) := WGARP.Utility L

abbrev expenditure {L : ℕ} := @WGARP.dot L
abbrev InBudget {L : ℕ} := @WGARP.InBudget L
abbrev UtilityDemand {L : ℕ} := @WGARP.UtilityDemand L

theorem expenditure_smul_price {L : ℕ} (a : ℝ)
    (p x : Bundle L) :
    expenditure (a • p) x = a * expenditure p x := by
  simp [expenditure, WGARP.dot, Finset.mul_sum, mul_assoc]

theorem inBudget_scale_iff {L : ℕ}
    (a : ℝ) (ha : 0 < a) (p : Bundle L) (w : ℝ) (x : Bundle L) :
    InBudget (a • p) (a * w) x ↔ InBudget p w x := by
  change
    (WGARP.Nonnegative x ∧ WGARP.dot (a • p) x ≤ a * w) ↔
      (WGARP.Nonnegative x ∧ WGARP.dot p x ≤ w)
  rw [show WGARP.dot (a • p) x = a * WGARP.dot p x from
    expenditure_smul_price a p x]
  constructor
  · rintro ⟨hx, hcost⟩
    exact ⟨hx, by nlinarith⟩
  · rintro ⟨hx, hcost⟩
    exact ⟨hx, by nlinarith⟩

/-- Marshallian demand is homogeneous of degree zero in prices and wealth.
No continuity, convexity, or uniqueness assumption is needed. -/
theorem utilityDemand_scale_iff {L : ℕ} (u : Utility L)
    (a : ℝ) (ha : 0 < a) (p : Bundle L) (w : ℝ) (x : Bundle L) :
    UtilityDemand u (a • p) (a * w) x ↔ UtilityDemand u p w x := by
  constructor
  · intro hx
    refine ⟨(inBudget_scale_iff a ha p w x).mp hx.1, ?_⟩
    intro y hy
    exact hx.2 y ((inBudget_scale_iff a ha p w y).mpr hy)
  · intro hx
    refine ⟨(inBudget_scale_iff a ha p w x).mpr hx.1, ?_⟩
    intro y hy
    exact hx.2 y ((inBudget_scale_iff a ha p w y).mp hy)

/-- A direct bridge to the imported, kernel-checked budget-exhaustion proof.
The assumptions are exactly positivity of prices, at least one good, strict
coordinatewise monotonicity, and utility maximization. -/
theorem demanded_bundle_exhausts_budget {L : ℕ}
    (u : Utility L) (p : Bundle L) (w : ℝ) (x : Bundle L)
    (hL : 0 < L) (hp : WGARP.PositivePrice p)
    (hu : WGARP.StrictlyIncreasing u)
    (hx : UtilityDemand u p w x) :
    expenditure p x = w := by
  exact WGARP.utilityDemand_expenditure_eq_wealth u p w x hL hp hu hx

end Econ803.Consumer
