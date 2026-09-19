import Econ803.Foundations.Relations

/-!
# Choice, rationalization, and WARP

This module checks the finite-menu logic behind the necessity of WARP. It
deliberately makes no topological or numerical-representation assumptions.
-/

set_option autoImplicit false

namespace Econ803.Choice

open Econ803.Foundations

variable {α ι : Type*}

abbrev Menu (α : Type*) := Set α

def IsChosen (r : Rel α) (menu : Menu α) (x : α) : Prop :=
  x ∈ menu ∧ ∀ ⦃y⦄, y ∈ menu → r x y

/-- If `x` maximizes a transitive relation in `A`, and `y` maximizes it in
`B`, then the cross-feasibility assumptions force `x` also to maximize in
`B`. This is the set-valued WARP implication used in the text. -/
theorem rational_choice_satisfies_WARP
    (r : Rel α) (ht : Econ803.Foundations.Transitive r)
    (A B : Menu α) {x y : α}
    (hxA : IsChosen r A x) (hyA : y ∈ A)
    (hyB : IsChosen r B y) (hxB : x ∈ B) : IsChosen r B x := by
  constructor
  · exact hxB
  · intro z hzB
    exact ht (hxA.2 hyA) (hyB.2 hzB)

/-- A maximizer cannot be strictly dominated by another feasible object. -/
theorem chosen_not_strictly_dominated
    (r : Rel α) (menu : Menu α) {x y : α}
    (hx : IsChosen r menu x) (hy : y ∈ menu) :
    ¬ StrictPart r y x := by
  intro hyx
  exact hyx.2 (hx.2 hy)

def DirectlyRevealed (menus : ι → Menu α) (choice : ι → Set α)
    (x y : α) : Prop :=
  ∃ i, x ∈ choice i ∧ y ∈ menus i

def StrictlyDirectlyRevealed (menus : ι → Menu α) (choice : ι → Set α)
    (x y : α) : Prop :=
  ∃ i, x ∈ choice i ∧ y ∈ menus i ∧ y ∉ choice i

def Rationalizes (r : Rel α) (menus : ι → Menu α)
    (choice : ι → Set α) : Prop :=
  ∀ i x, x ∈ choice i ↔ IsChosen r (menus i) x

/-- Exact revealed-preference necessity: a complete and transitive
rationalization rules out a direct weak comparison in one direction together
with a direct strict comparison in the reverse direction. -/
theorem rationalization_implies_WARP
    (r : Rel α) (ht : Econ803.Foundations.Transitive r)
    (menus : ι → Menu α) (choice : ι → Set α)
    (hrat : Rationalizes r menus choice) :
    ∀ {x y}, DirectlyRevealed menus choice x y →
      ¬ StrictlyDirectlyRevealed menus choice y x := by
  intro x y hxy hyx
  obtain ⟨i, hxc, hyA⟩ := hxy
  obtain ⟨j, hyc, hxB, hnot⟩ := hyx
  have hxAi : IsChosen r (menus i) x := (hrat i x).mp hxc
  have hyBj : IsChosen r (menus j) y := (hrat j y).mp hyc
  have hxBj : IsChosen r (menus j) x :=
    rational_choice_satisfies_WARP r ht (menus i) (menus j)
      hxAi hyA hyBj hxB
  exact hnot ((hrat j x).mpr hxBj)

end Econ803.Choice
