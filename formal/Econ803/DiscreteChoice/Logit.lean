import Mathlib.Analysis.SpecialFunctions.Exp
import Mathlib.Tactic.FieldSimp
import Mathlib.Tactic.Ring

/-!
# Multinomial logit

This module verifies the algebra behind independence of irrelevant
alternatives. The available set is the finite type `J`; restricting or
expanding it changes the common denominator but not the odds of two retained
alternatives.
-/

set_option autoImplicit false

open scoped BigOperators

namespace Econ803.DiscreteChoice

variable {J : Type*}

noncomputable def logitDenominator [Fintype J] (V : J → ℝ) (μ : ℝ) : ℝ :=
  ∑ k, Real.exp (V k / μ)

noncomputable def logitProbability [Fintype J]
    (V : J → ℝ) (μ : ℝ) (j : J) : ℝ :=
  Real.exp (V j / μ) / logitDenominator V μ

theorem logitDenominator_pos [Fintype J] [Nonempty J]
    (V : J → ℝ) (μ : ℝ) :
    0 < logitDenominator V μ := by
  unfold logitDenominator
  exact Finset.sum_pos (fun i _hi => Real.exp_pos (V i / μ)) Finset.univ_nonempty

/-- The algebraic odds-ratio identity. It remains true at Lean's formal value
`μ = 0`, but that case is not an economically meaningful logit scale. -/
theorem logit_odds_ratio_algebraic [Fintype J] [Nonempty J]
    (V : J → ℝ) (μ : ℝ) (j k : J) :
    logitProbability V μ j / logitProbability V μ k =
      Real.exp ((V j - V k) / μ) := by
  have hden : logitDenominator V μ ≠ 0 :=
    ne_of_gt (logitDenominator_pos V μ)
  have hexp : Real.exp (V k / μ) ≠ 0 := (Real.exp_pos _).ne'
  unfold logitProbability
  field_simp
  rw [← Real.exp_add]
  congr 1
  ring

/-- Economic IIA in odds-ratio form, with a strictly positive logit scale. -/
theorem logit_odds_ratio [Fintype J] [Nonempty J]
    (V : J → ℝ) (μ : ℝ) (hμ : 0 < μ) (j k : J) :
    logitProbability V μ j / logitProbability V μ k =
      Real.exp ((V j - V k) / μ) := by
  exact logit_odds_ratio_algebraic V μ j k

end Econ803.DiscreteChoice
