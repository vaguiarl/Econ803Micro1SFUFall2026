import Econ803.Consumer.Demand
import Mathlib.Tactic.Linarith

/-!
# Expenditure duality: the algebraic core

The textbook's analytic existence theorem and its algebraic consequences are
separated here. `IsExpenditureValue P F e` requires a nonempty explicit price
domain `P` and assumes an attained minimum only at prices in `P`. The theorems
then derive homogeneity, concavity, and the supergradient form of Shephard's
lemma on that domain. This avoids imposing attainment at economically
inadmissible price vectors.
-/

set_option autoImplicit false

open scoped BigOperators

namespace Econ803.Consumer

def IsExpenditureValue {L : ℕ}
    (P F : Set (Bundle L)) (e : Bundle L → ℝ) : Prop :=
  P.Nonempty ∧
    ∀ p ∈ P, ∃ x ∈ F,
      e p = expenditure p x ∧ ∀ y ∈ F, e p ≤ expenditure p y

def IsSupergradientOn {L : ℕ}
    (P : Set (Bundle L)) (e : Bundle L → ℝ)
    (p x : Bundle L) : Prop :=
  ∀ q ∈ P, e q - e p ≤ expenditure (q - p) x

private theorem expenditure_add {L : ℕ}
    (p q x : Bundle L) :
    expenditure (p + q) x = expenditure p x + expenditure q x := by
  simp [expenditure, WGARP.dot, Finset.sum_add_distrib, add_mul]

private theorem expenditure_smul {L : ℕ}
    (a : ℝ) (p x : Bundle L) :
    expenditure (a • p) x = a * expenditure p x := by
  exact expenditure_smul_price a p x

private theorem expenditure_sub {L : ℕ}
    (p q x : Bundle L) :
    expenditure (p - q) x = expenditure p x - expenditure q x := by
  simp [expenditure, WGARP.dot, Finset.sum_sub_distrib, sub_mul]

/-- The expenditure function is homogeneous of degree one along an admissible
positive price ray. -/
theorem expenditure_homogeneous
    {L : ℕ} {P F : Set (Bundle L)} {e : Bundle L → ℝ}
    (he : IsExpenditureValue P F e)
    (p : Bundle L) (hp : p ∈ P)
    (a : ℝ) (ha : 0 < a) (hscale : a • p ∈ P) :
    e (a • p) = a * e p := by
  obtain ⟨x, hxF, hxp, hxmin⟩ := he.2 p hp
  obtain ⟨z, hzF, hzap, hzmin⟩ := he.2 (a • p) hscale
  have hlower : a * e p ≤ e (a • p) := by
    rw [hzap, expenditure_smul]
    nlinarith [hxmin z hzF]
  have hupper : e (a • p) ≤ a * e p := by
    calc
      e (a • p) ≤ expenditure (a • p) x := hzmin x hxF
      _ = a * expenditure p x := expenditure_smul a p x
      _ = a * e p := by rw [hxp]
  exact le_antisymm hupper hlower

/-- An attained expenditure value is concave along an admissible price
segment. -/
theorem expenditure_concave
    {L : ℕ} {P F : Set (Bundle L)} {e : Bundle L → ℝ}
    (he : IsExpenditureValue P F e)
    (p q : Bundle L) (hp : p ∈ P) (hq : q ∈ P)
    (t : ℝ) (ht0 : 0 ≤ t) (ht1 : t ≤ 1)
    (hmix : t • p + (1 - t) • q ∈ P) :
    t * e p + (1 - t) * e q ≤ e (t • p + (1 - t) • q) := by
  obtain ⟨x, hxF, hxmix, _hxmin⟩ :=
    he.2 (t • p + (1 - t) • q) hmix
  obtain ⟨_xp, _hxpF, _hxpe, hpmin⟩ := he.2 p hp
  obtain ⟨_xq, _hxqF, _hxqe, hqmin⟩ := he.2 q hq
  have hp := hpmin x hxF
  have hq := hqmin x hxF
  calc
    t * e p + (1 - t) * e q ≤
        t * expenditure p x + (1 - t) * expenditure q x := by
      gcongr
    _ = expenditure (t • p + (1 - t) • q) x := by
      rw [expenditure_add, expenditure_smul, expenditure_smul]
    _ = e (t • p + (1 - t) • q) := hxmix.symm

/-- Shephard's inequality: every Hicksian minimizer is a supergradient of the
concave expenditure function relative to the admissible price domain.
Differentiability is not needed for this form. -/
theorem hicksian_bundle_is_supergradient
    {L : ℕ} {P F : Set (Bundle L)} {e : Bundle L → ℝ}
    (he : IsExpenditureValue P F e) (p x : Bundle L)
    (hp : p ∈ P) (hxF : x ∈ F)
    (hxe : e p = expenditure p x) :
    IsSupergradientOn P e p x := by
  intro q hqP
  obtain ⟨z, hzF, hzq, hzmin⟩ := he.2 q hqP
  have hq : e q ≤ expenditure q x := hzmin x hxF
  rw [expenditure_sub]
  linarith

end Econ803.Consumer
