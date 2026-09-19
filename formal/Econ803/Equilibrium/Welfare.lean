import Econ803.Consumer.Demand
import Econ803.Foundations.Relations

/-!
# Welfare and the core: price-support arguments

These are the exact algebraic consumers of the separating-price step in the
welfare theorems. They are suitable as starred theorems in the main text: the
economic argument is transparent, while the analytic lemma deriving price
support from local nonsatiation and optimization remains an explicitly
identified appendix target.
-/

set_option autoImplicit false

open scoped BigOperators

namespace Econ803.Equilibrium

open Econ803.Consumer
open Econ803.Foundations

variable {I : Type*}

def aggregate [Fintype I] {L : ℕ}
    (x : I → Bundle L) : Bundle L :=
  fun ℓ => ∑ i, x i ℓ

def aggregateOn {I : Type*} {L : ℕ}
    (S : Finset I) (x : I → Bundle L) : Bundle L :=
  fun ℓ => ∑ i ∈ S, x i ℓ

theorem expenditure_aggregate [Fintype I] {L : ℕ}
    (p : Bundle L) (x : I → Bundle L) :
    expenditure p (aggregate x) = ∑ i, expenditure p (x i) := by
  unfold expenditure WGARP.dot aggregate
  simp only [Finset.mul_sum]
  rw [Finset.sum_comm]

theorem expenditure_aggregateOn {I : Type*} {L : ℕ}
    (p : Bundle L) (S : Finset I) (x : I → Bundle L) :
    expenditure p (aggregateOn S x) = ∑ i ∈ S, expenditure p (x i) := by
  unfold expenditure WGARP.dot aggregateOn
  simp only [Finset.mul_sum]
  rw [Finset.sum_comm]

def ParetoDominates [Fintype I] {L : ℕ}
    (r : I → Bundle L → Bundle L → Prop)
    (y x : I → Bundle L) : Prop :=
  (∀ i, r i (y i) (x i)) ∧
    ∃ i, StrictPart (r i) (y i) (x i)

def PriceSupportsAt [Fintype I] {L : ℕ}
    (r : I → Bundle L → Bundle L → Prop)
    (p : Bundle L) (x : I → Bundle L) : Prop :=
  (∀ i y, r i y (x i) → expenditure p (x i) ≤ expenditure p y) ∧
    (∀ i y, StrictPart (r i) y (x i) →
      expenditure p (x i) < expenditure p y)

/-- If a common price supports every consumer's weak and strict upper contour
at a market-clearing allocation, no other market-clearing allocation Pareto
dominates it. This is the finite price-summing core later consumed by a first
welfare theorem; it is not itself the full equilibrium theorem. -/
theorem priceSupport_rulesOut_paretoImprovement
    [Fintype I] {L : ℕ}
    (r : I → Bundle L → Bundle L → Prop)
    (p resources : Bundle L) (x : I → Bundle L)
    (hclear : aggregate x = resources)
    (hsupport : PriceSupportsAt r p x) :
    ¬ ∃ y : I → Bundle L,
      aggregate y = resources ∧ ParetoDominates r y x := by
  rintro ⟨y, hcleary, hpareto⟩
  have hall : ∀ i, expenditure p (x i) ≤ expenditure p (y i) :=
    fun i => hsupport.1 i (y i) (hpareto.1 i)
  obtain ⟨j, hjstrict⟩ := hpareto.2
  have hj : expenditure p (x j) < expenditure p (y j) :=
    hsupport.2 j (y j) hjstrict
  have hsum : (∑ i, expenditure p (x i)) <
      ∑ i, expenditure p (y i) := by
    apply Finset.sum_lt_sum
    · intro i _hi
      exact hall i
    · exact ⟨j, Finset.mem_univ j, hj⟩
  have heqx : expenditure p resources = ∑ i, expenditure p (x i) := by
    rw [← hclear, expenditure_aggregate]
  have heqy : expenditure p resources = ∑ i, expenditure p (y i) := by
    rw [← hcleary, expenditure_aggregate]
  linarith

/-- A finite coalition cannot satisfy its resource equality while every member
must finance a strict improvement at a common supporting price. This is the
price-summing core of the competitive-allocation/core argument. -/
theorem priceSupport_rulesOut_coalitionBlock
    [Fintype I] {L : ℕ}
    (r : I → Bundle L → Bundle L → Prop)
    (p : Bundle L) (endowment x : I → Bundle L)
    (hbudget : ∀ i, expenditure p (x i) = expenditure p (endowment i))
    (hstrict : ∀ i y, StrictPart (r i) y (x i) →
      expenditure p (x i) < expenditure p y) :
    ¬ ∃ (S : Finset I) (hS : S.Nonempty) (y : I → Bundle L),
      aggregateOn S y = aggregateOn S endowment ∧
        ∀ i ∈ S, StrictPart (r i) (y i) (x i) := by
  rintro ⟨S, hS, y, hresources, hbetter⟩
  have hall : ∀ i ∈ S,
      expenditure p (endowment i) < expenditure p (y i) := by
    intro i hi
    rw [← hbudget i]
    exact hstrict i (y i) (hbetter i hi)
  have hsum : (∑ i ∈ S, expenditure p (endowment i)) <
      ∑ i ∈ S, expenditure p (y i) := by
    exact Finset.sum_lt_sum_of_nonempty hS hall
  have heq : (∑ i ∈ S, expenditure p (y i)) =
      ∑ i ∈ S, expenditure p (endowment i) := by
    rw [← expenditure_aggregateOn, hresources, expenditure_aggregateOn]
  linarith

end Econ803.Equilibrium
