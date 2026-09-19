import Econ803.Consumer.Demand
import Mathlib.Tactic.GCongr
import Mathlib.Tactic.Linarith

/-!
# Profit maximization

As in the duality module, analytic attainment is isolated in a small
interface. `IsProfitValue P Y π` requires a nonempty explicit admissible price
domain `P` and consumes exact maximization only at prices in that domain. This
does not impose finite attained profit at negative or otherwise inadmissible
price vectors.
-/

set_option autoImplicit false

namespace Econ803.Firm

open Econ803.Consumer

def IsProfitValue {L : ℕ}
    (P Y : Set (Bundle L)) (π : Bundle L → ℝ) : Prop :=
  P.Nonempty ∧
    ∀ p ∈ P, ∃ y ∈ Y,
      π p = expenditure p y ∧ ∀ z ∈ Y, expenditure p z ≤ π p

def IsSubgradientOn {L : ℕ}
    (P : Set (Bundle L)) (π : Bundle L → ℝ)
    (p y : Bundle L) : Prop :=
  ∀ q ∈ P, expenditure (q - p) y ≤ π q - π p

private theorem expenditure_add {L : ℕ}
    (p q y : Bundle L) :
    expenditure (p + q) y = expenditure p y + expenditure q y := by
  simp [expenditure, WGARP.dot, Finset.sum_add_distrib, add_mul]

private theorem expenditure_sub {L : ℕ}
    (p q y : Bundle L) :
    expenditure (p - q) y = expenditure p y - expenditure q y := by
  simp [expenditure, WGARP.dot, Finset.sum_sub_distrib, sub_mul]

/-- The profit function is homogeneous of degree one along an admissible
positive price ray. -/
theorem profit_homogeneous
    {L : ℕ} {P Y : Set (Bundle L)} {π : Bundle L → ℝ}
    (hπ : IsProfitValue P Y π)
    (p : Bundle L) (hp : p ∈ P)
    (a : ℝ) (ha : 0 < a) (hscale : a • p ∈ P) :
    π (a • p) = a * π p := by
  obtain ⟨y, hyY, hyp, hymax⟩ := hπ.2 p hp
  obtain ⟨z, hzY, hzap, hzmax⟩ := hπ.2 (a • p) hscale
  have hlower : a * π p ≤ π (a • p) := by
    calc
      a * π p = expenditure (a • p) y := by
        rw [hyp, expenditure_smul_price]
      _ ≤ π (a • p) := hzmax y hyY
  have hupper : π (a • p) ≤ a * π p := by
    rw [hzap, expenditure_smul_price]
    nlinarith [hymax z hzY]
  exact le_antisymm hupper hlower

/-- The profit function is convex along an admissible price segment. -/
theorem profit_convex
    {L : ℕ} {P Y : Set (Bundle L)} {π : Bundle L → ℝ}
    (hπ : IsProfitValue P Y π)
    (p q : Bundle L) (hp : p ∈ P) (hq : q ∈ P)
    (t : ℝ) (ht0 : 0 ≤ t) (ht1 : t ≤ 1)
    (hmix : t • p + (1 - t) • q ∈ P) :
    π (t • p + (1 - t) • q) ≤ t * π p + (1 - t) * π q := by
  obtain ⟨y, hyY, hymix, _hymax⟩ :=
    hπ.2 (t • p + (1 - t) • q) hmix
  obtain ⟨_yp, _hypY, _hype, hpmax⟩ := hπ.2 p hp
  obtain ⟨_yq, _hyqY, _hyqe, hqmax⟩ := hπ.2 q hq
  rw [hymix, expenditure_add, expenditure_smul_price,
    expenditure_smul_price]
  exact add_le_add
    (mul_le_mul_of_nonneg_left (hpmax y hyY) ht0)
    (mul_le_mul_of_nonneg_left (hqmax y hyY) (sub_nonneg.mpr ht1))

/-- Hotelling's envelope inequality: a profit-maximizing production vector is
a subgradient of the convex profit function relative to the admissible price
domain. -/
theorem profit_maximizer_is_subgradient
    {L : ℕ} {P Y : Set (Bundle L)} {π : Bundle L → ℝ}
    (hπ : IsProfitValue P Y π) (p y : Bundle L)
    (hp : p ∈ P) (hyY : y ∈ Y)
    (hπp : π p = expenditure p y) :
    IsSubgradientOn P π p y := by
  intro q hqP
  obtain ⟨z, hzY, hzq, hzmax⟩ := hπ.2 q hqP
  have hq : expenditure q y ≤ π q := hzmax y hyY
  rw [expenditure_sub]
  linarith

/-- Strictly positive prices make every profit maximizer technologically
efficient against coordinatewise strict improvements in the same set. -/
theorem profit_maximizer_is_efficient
    {L : ℕ} {Y : Set (Bundle L)} (p y : Bundle L)
    (hp : WGARP.PositivePrice p) (hyY : y ∈ Y)
    (hymax : ∀ z ∈ Y, expenditure p z ≤ expenditure p y) :
    ¬ ∃ z ∈ Y, WGARP.StrictDominates z y := by
  rintro ⟨z, hzY, hzy⟩
  have hstrict : expenditure p y < expenditure p z :=
    WGARP.dot_strictlyIncreasing_of_pos hp hzy
  exact (not_lt_of_ge (hymax z hzY)) hstrict

end Econ803.Firm
