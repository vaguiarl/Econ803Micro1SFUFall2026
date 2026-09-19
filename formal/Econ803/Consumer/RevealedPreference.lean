import WGARP.CompensatedDemand
import WGARP.GlobalAfriat

/-!
# Revealed preference and Afriat

These declarations are theorem-exact bridges to the public `wgarp-lean`
project pinned by `lakefile.toml`. The proofs are not copied or restated as
local work: Lake compiles the upstream source at the recorded commit and the
Lean kernel checks these downstream consumers against its interfaces.
-/

set_option autoImplicit false

namespace Econ803.Consumer

/-- Finite GARP is equivalent to feasibility of the Afriat inequalities with
strictly positive multipliers. -/
theorem finite_GARP_iff_Afriat_inequalities
    {L : ℕ} {T : Type*} [Fintype T]
    (D : WGARP.Dataset L T) :
    WGARP.GARP D ↔
      ∃ U lam, WGARP.PositiveMultipliers lam ∧
        WGARP.AfriatInequalities U lam D.price D.choice := by
  exact WGARP.garp_iff_exists_afriatInequalities D

/-- Full finite Afriat theorem at the strength proved upstream: GARP is
equivalent to rationalization by a continuous, concave, strictly increasing
utility on finite-dimensional bundles. -/
theorem finite_Afriat_theorem
    {L : ℕ} {T : Type*} [Fintype T] [Nonempty T]
    (D : WGARP.Dataset L T) :
    WGARP.GARP D ↔ WGARP.HasRegularUtilityRationalization D := by
  exact WGARP.garp_iff_hasRegularUtilityRationalization D

/-- The constructive form records both the numerical Afriat certificate and
the regular lower-envelope utility generated from it. -/
theorem finite_Afriat_constructive
    {L : ℕ} {T : Type*} [Fintype T] [Nonempty T]
    (D : WGARP.Dataset L T) :
    WGARP.GARP D ↔
      (∃ U lam,
        WGARP.PositiveMultipliers lam ∧
        WGARP.AfriatInequalities U lam D.price D.choice ∧
        Continuous (WGARP.globalAfriatUtility U lam D.price D.choice) ∧
        ConcaveOn ℝ Set.univ
          (WGARP.globalAfriatUtility U lam D.price D.choice) ∧
        WGARP.StrictlyIncreasing
          (WGARP.globalAfriatUtility U lam D.price D.choice) ∧
        WGARP.UtilityRationalizes D
          (WGARP.globalAfriatUtility U lam D.price D.choice)) := by
  exact WGARP.garp_iff_exists_afriatCertificate_and_regularUtility D

/-- Compensated price changes have a nonpositive price-demand inner product
under the precise monotonicity and asymmetry hypotheses in the upstream
consumer model. -/
theorem compensated_law_of_demand
    {L : ℕ}
    (r : WGARP.PreferenceFunction L)
    (p p' : WGARP.Bundle L) (w : ℝ) (x x' : WGARP.Bundle L)
    (hp : WGARP.PositivePrice p) (hL : 0 < L)
    (hasym : WGARP.Asymmetric r)
    (hinc : WGARP.StrictlyIncreasingFirst r)
    (hx : WGARP.PreferenceDemand r p w x)
    (hx' : WGARP.PreferenceDemand r p' (WGARP.dot p' x) x') :
    WGARP.dot (p' - p) (x' - x) ≤ 0 := by
  have hp_cross : WGARP.dot p x ≤ WGARP.dot p x' :=
    WGARP.demand_cross_expenditure r p p' w x x'
      hp hL hasym hinc hx hx'
  have hp'_cross : WGARP.dot p' x' ≤ WGARP.dot p' x := hx'.1.2
  rw [WGARP.dot_sub, WGARP.dot_sub_left, WGARP.dot_sub_left]
  linarith

end Econ803.Consumer
