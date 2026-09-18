namespace Econ803.ChoiceTheory

abbrev Rel (α : Type) := α → α → Prop
abbrev Menu (α : Type) := α → Prop

def Transitive (r : Rel α) : Prop := ∀ ⦃x y z⦄, r x y → r y z → r x z
def StrictPart (r : Rel α) : Rel α := fun x y => r x y ∧ ¬ r y x

def IsChosen (r : Rel α) (menu : Menu α) (x : α) : Prop :=
  menu x ∧ ∀ ⦃y⦄, menu y → r x y

/-- Maximization of a transitive weak preference satisfies the set-valued
    version of WARP used in the text. -/
theorem rational_choice_satisfies_WARP
    (r : Rel α) (ht : Transitive r)
    (A B : Menu α) {x y : α}
    (hxA : IsChosen r A x) (hyA : A y)
    (hyB : IsChosen r B y) (hxB : B x) : IsChosen r B x := by
  constructor
  · exact hxB
  · intro z hzB
    exact ht (hxA.2 hyA) (hyB.2 hzB)

/-- A chosen alternative cannot be strictly dominated by another feasible
    alternative under the same rationalizing relation. -/
theorem chosen_not_strictly_dominated
    (r : Rel α) (menu : Menu α) {x y : α}
    (hx : IsChosen r menu x) (hy : menu y) : ¬ StrictPart r y x := by
  intro hyx
  exact hyx.2 (hx.2 hy)

end Econ803.ChoiceTheory
