import Mathlib.Logic.Relation
import Mathlib.Order.Extension.Linear
import Mathlib.Data.Finset.Card

/-!
# Relations and order theory

The declarations in this file formalize the elementary core of Appendix A.
They use unbundled relations so the statements line up with the notation in
the textbook.
-/

set_option autoImplicit false

namespace Econ803.Foundations

variable {α : Type*}

abbrev Rel (α : Type*) := α → α → Prop

def Reflexive (r : Rel α) : Prop := ∀ x, r x x
def Symmetric (r : Rel α) : Prop := ∀ ⦃x y⦄, r x y → r y x
def Asymmetric (r : Rel α) : Prop := ∀ ⦃x y⦄, r x y → ¬ r y x
def Antisymmetric (r : Rel α) : Prop := ∀ ⦃x y⦄, r x y → r y x → x = y
def Transitive (r : Rel α) : Prop := ∀ ⦃x y z⦄, r x y → r y z → r x z
def Complete (r : Rel α) : Prop := ∀ x y, r x y ∨ r y x

def SymmetricPart (r : Rel α) : Rel α := fun x y => r x y ∧ r y x
def StrictPart (r : Rel α) : Rel α := fun x y => r x y ∧ ¬ r y x

theorem complete_implies_reflexive (r : Rel α) (hc : Complete r) : Reflexive r := by
  intro x
  exact (hc x x).elim id id

theorem symmetricPart_is_equivalence (r : Rel α)
    (hr : Reflexive r) (ht : Transitive r) :
    Reflexive (SymmetricPart r) ∧
      Symmetric (SymmetricPart r) ∧ Transitive (SymmetricPart r) := by
  refine ⟨?_, ?_, ?_⟩
  · intro x
    exact ⟨hr x, hr x⟩
  · intro x y hxy
    exact ⟨hxy.2, hxy.1⟩
  · intro x y z hxy hyz
    exact ⟨ht hxy.1 hyz.1, ht hyz.2 hxy.2⟩

theorem strictPart_asymmetric (r : Rel α) : Asymmetric (StrictPart r) := by
  intro x y hxy hyx
  exact hxy.2 hyx.1

theorem strictPart_transitive (r : Rel α) (ht : Transitive r) :
    Transitive (StrictPart r) := by
  intro x y z hxy hyz
  constructor
  · exact ht hxy.1 hyz.1
  · intro hzx
    exact hyz.2 (ht hzx hxy.1)

def Greatest (r : Rel α) (s : Set α) (x : α) : Prop :=
  x ∈ s ∧ ∀ ⦃y⦄, y ∈ s → r x y

def Maximal (r : Rel α) (s : Set α) (x : α) : Prop :=
  x ∈ s ∧ ∀ ⦃y⦄, y ∈ s → ¬ StrictPart r y x

theorem greatest_implies_maximal (r : Rel α) (s : Set α) {x : α}
    (hx : Greatest r s x) : Maximal r s x := by
  constructor
  · exact hx.1
  · intro y hy hyp
    exact hyp.2 (hx.2 hy)

theorem complete_maximal_implies_greatest (r : Rel α) (s : Set α)
    (hc : Complete r) {x : α} (hx : Maximal r s x) : Greatest r s x := by
  constructor
  · exact hx.1
  · intro y hy
    rcases hc x y with hxy | hyx
    · exact hxy
    · by_contra hxy
      exact hx.2 hy ⟨hyx, hxy⟩

theorem complete_maximal_iff_greatest (r : Rel α) (s : Set α)
    (hc : Complete r) {x : α} : Maximal r s x ↔ Greatest r s x := by
  exact ⟨complete_maximal_implies_greatest r s hc,
    greatest_implies_maximal r s⟩

/-- Every nonempty finite set has a greatest element for a complete,
transitive relation. This is the finite-existence proposition in Appendix A. -/
theorem finite_exists_greatest (r : Rel α) (ht : Transitive r) (hc : Complete r)
    (s : Finset α) (hs : s.Nonempty) :
    ∃ g, g ∈ s ∧ ∀ y ∈ s, r g y := by
  classical
  induction s using Finset.induction_on with
  | empty => simp at hs
  | @insert a s ha ih =>
      by_cases hsn : s.Nonempty
      · obtain ⟨g, hgs, hg⟩ := ih hsn
        rcases hc a g with hag | hga
        · refine ⟨a, by simp, ?_⟩
          intro y hy
          rcases Finset.mem_insert.mp hy with hya | hys
          · subst y
            exact (complete_implies_reflexive r hc) a
          · exact ht hag (hg y hys)
        · refine ⟨g, Finset.mem_insert_of_mem hgs, ?_⟩
          intro y hy
          rcases Finset.mem_insert.mp hy with rfl | hys
          · exact hga
          · exact hg y hys
      · have hsempty : s = ∅ := Finset.not_nonempty_iff_eq_empty.mp hsn
        subst s
        refine ⟨a, by simp, ?_⟩
        intro y hy
        have hya : y = a := by simpa using hy
        subst y
        exact (complete_implies_reflexive r hc) a

def TransitiveClosure (r : Rel α) : Rel α := Relation.TransGen r

theorem relation_subset_transitiveClosure (r : Rel α) :
    ∀ ⦃x y⦄, r x y → TransitiveClosure r x y := by
  intro x y hxy
  exact Relation.TransGen.single hxy

theorem transitiveClosure_transitive (r : Rel α) :
    Transitive (TransitiveClosure r) := by
  intro x y z hxy hyz
  exact hxy.trans hyz

/-- The transitive closure is contained in every transitive relation that
contains the original relation. -/
theorem transitiveClosure_least (r s : Rel α)
    (hrs : ∀ ⦃x y⦄, r x y → s x y) (hst : Transitive s) :
    ∀ ⦃x y⦄, TransitiveClosure r x y → s x y := by
  intro x y hxy
  induction hxy with
  | single h => exact hrs h
  | tail h hlast ih => exact hst ih (hrs hlast)

/-- Szpilrajn's theorem, delegated to Mathlib's Zorn-lemma construction and
re-exposed with the unbundled hypotheses used in the textbook. -/
theorem partialOrder_has_linearExtension (r : Rel α)
    (hr : Reflexive r) (ht : Transitive r) (ha : Antisymmetric r) :
    ∃ s : Rel α,
      Reflexive s ∧ Transitive s ∧ Antisymmetric s ∧ Complete s ∧
        (∀ ⦃x y⦄, r x y → s x y) := by
  letI : IsPartialOrder α r :=
    { refl := hr
      trans := ht
      antisymm := ha }
  obtain ⟨s, hs, hrs⟩ := extend_partialOrder r
  exact ⟨s, hs.refl, hs.trans, hs.antisymm, hs.total,
    fun {x y} h => hrs x y h⟩

end Econ803.Foundations
