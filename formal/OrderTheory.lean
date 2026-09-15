namespace Econ804.OrderTheory

abbrev Rel (α : Type) := α → α → Prop

def Reflexive (r : Rel α) : Prop := ∀ x, r x x
def Symmetric (r : Rel α) : Prop := ∀ ⦃x y⦄, r x y → r y x
def Asymmetric (r : Rel α) : Prop := ∀ ⦃x y⦄, r x y → ¬ r y x
def Transitive (r : Rel α) : Prop := ∀ ⦃x y z⦄, r x y → r y z → r x z
def Complete (r : Rel α) : Prop := ∀ x y, r x y ∨ r y x

def SymmetricPart (r : Rel α) : Rel α := fun x y => r x y ∧ r y x
def StrictPart (r : Rel α) : Rel α := fun x y => r x y ∧ ¬ r y x

theorem complete_implies_reflexive (r : Rel α) (hc : Complete r) : Reflexive r := by
  intro x
  exact (hc x x).elim id id

theorem symmetricPart_reflexive (r : Rel α) (hr : Reflexive r) :
    Reflexive (SymmetricPart r) := by
  intro x
  exact ⟨hr x, hr x⟩

theorem symmetricPart_symmetric (r : Rel α) : Symmetric (SymmetricPart r) := by
  intro x y hxy
  exact ⟨hxy.2, hxy.1⟩

theorem symmetricPart_transitive (r : Rel α) (ht : Transitive r) :
    Transitive (SymmetricPart r) := by
  intro x y z hxy hyz
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

def Greatest (r : Rel α) (s : α → Prop) (x : α) : Prop :=
  s x ∧ ∀ ⦃y⦄, s y → r x y

def Maximal (r : Rel α) (s : α → Prop) (x : α) : Prop :=
  s x ∧ ∀ ⦃y⦄, s y → ¬ StrictPart r y x

theorem greatest_implies_maximal (r : Rel α) (s : α → Prop) {x : α}
    (hx : Greatest r s x) : Maximal r s x := by
  constructor
  · exact hx.1
  · intro y hy hyp
    exact hyp.2 (hx.2 hy)

theorem complete_maximal_implies_greatest (r : Rel α) (s : α → Prop)
    (hc : Complete r) {x : α} (hx : Maximal r s x) : Greatest r s x := by
  constructor
  · exact hx.1
  · intro y hy
    cases hc x y with
    | inl hxy => exact hxy
    | inr hyx =>
        by_cases hxy : r x y
        · exact hxy
        · exact False.elim (hx.2 hy ⟨hyx, hxy⟩)

theorem complete_maximal_iff_greatest (r : Rel α) (s : α → Prop)
    (hc : Complete r) {x : α} : Maximal r s x ↔ Greatest r s x := by
  constructor
  · exact complete_maximal_implies_greatest r s hc
  · exact greatest_implies_maximal r s

end Econ804.OrderTheory
