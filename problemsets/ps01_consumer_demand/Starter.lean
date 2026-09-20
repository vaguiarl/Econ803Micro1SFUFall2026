import Econ803.Consumer.Demand

/-!
# ECON 803 Problem Set 1 starter

This file states, but deliberately does not prove, the formal scale-up target.
Copy it to `work/PS01_ConsumerDemand.lean`, add your theorem below the target
definition, and compile from the `formal/` directory.
-/

set_option autoImplicit false

namespace Econ803.ProblemSets.PS01

open Econ803.Consumer

#check Econ803.Consumer.inBudget_scale_iff
#check Econ803.Consumer.utilityDemand_scale_iff
#check Econ803.Consumer.demanded_bundle_exhausts_budget

def TwoScaleClaim {L : ℕ} (u : Utility L)
    (a b : ℝ) (p : Bundle L) (w : ℝ) (x : Bundle L) : Prop :=
  0 < a → 0 < b →
    (UtilityDemand u (a • p) (a * w) x ↔
      UtilityDemand u (b • p) (b * w) x)

/-
Add a theorem proving `TwoScaleClaim u a b p w x` in your own work file.
The target is arbitrary in `L`; a proof by checking finitely many coordinates
or by specializing to two goods does not meet the assignment.
-/

end Econ803.ProblemSets.PS01
