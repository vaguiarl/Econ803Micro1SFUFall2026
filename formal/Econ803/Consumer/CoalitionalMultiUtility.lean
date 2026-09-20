import WGARP.TheoremOne

set_option autoImplicit false

/-!
# WGARP and coalitional multi-utility

This module exposes the pinned WGARP project's exact finite-data Theorem 1
through the textbook namespace.  The imported theorem uses two explicit CMU
normal forms: a finite coherent coalition system and a compact
matrix/simplex construction.  It does not by itself identify those types with
the manuscript's more general hyperspace presentation of compact coalitions.
-/

namespace Econ803.Consumer

variable {L : ℕ} {T : Type*}

/--
The six conditions in the pinned finite WGARP theorem are equivalent in
paper order.  The conditions are:

1. continuous, strictly increasing, asymmetric preference-function
   rationalization;
2. a finite coherent-CMU rationalization;
3. a skew-symmetric matrix/simplex CMU rationalization with continuous,
   strictly increasing, concave component utilities;
4. WGARP;
5. pairwise Afriat feasibility; and
6. pairwise Varian feasibility.

Keeping the upstream statement aliases visible makes the scope of the
machine-checked result auditable and prevents the wrapper from silently
strengthening the theorem.
-/
theorem finite_wgarp_cmu_characterization
    [Fintype T] [Nonempty T] (D : WGARP.Dataset L T) :
    (WGARP.StatementI D ↔ WGARP.StatementII D) ∧
    (WGARP.StatementII D ↔ WGARP.StatementIII D) ∧
    (WGARP.StatementIII D ↔ WGARP.StatementIV D) ∧
    (WGARP.StatementIV D ↔ WGARP.StatementV D) ∧
    (WGARP.StatementV D ↔ WGARP.StatementVI D) := by
  exact WGARP.theorem_one D

end Econ803.Consumer
