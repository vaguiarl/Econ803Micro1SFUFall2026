/-!
# Machine-checked book dependency map

This module checks only that the declared logical dependencies exist and
precede their consumers. It does not prove the economic content of a chapter.
-/

set_option autoImplicit false

namespace Econ803.BookNarrative

inductive VerificationLevel where
  | localLean | importedLean | theoremStar | textbookProof | citedTheorem
deriving DecidableEq, Repr

structure Step where
  logicalId : Nat
  label : String
  verification : VerificationLevel
  dependencies : List Nat
deriving Repr

def mainMap : List Step := [
  { logicalId := 1, label := "Relations and order theory",
    verification := .localLean, dependencies := [] },
  { logicalId := 2, label := "Choice and WARP",
    verification := .localLean, dependencies := [1] },
  { logicalId := 3, label := "Demand and revealed preference",
    verification := .importedLean, dependencies := [1, 2] },
  { logicalId := 4, label := "Consumer duality",
    verification := .theoremStar, dependencies := [3] },
  { logicalId := 5, label := "Choice under uncertainty",
    verification := .theoremStar, dependencies := [1] },
  { logicalId := 6, label := "Production and profit",
    verification := .theoremStar, dependencies := [1, 3] },
  { logicalId := 7, label := "Equilibrium welfare",
    verification := .theoremStar, dependencies := [2, 3, 6] },
  { logicalId := 8, label := "Existence, matching, and advanced representation",
    verification := .citedTheorem, dependencies := [1, 2, 3, 7] }
]

def containsId (steps : List Step) (id : Nat) : Bool :=
  steps.any (fun s => s.logicalId == id)

def dependenciesPrecede (steps : List Step) : Bool :=
  steps.all fun s =>
    s.dependencies.all fun d => containsId steps d && d < s.logicalId

def idsIncrease : List Step → Bool
  | [] | [_] => true
  | a :: b :: rest =>
      a.logicalId < b.logicalId && idsIncrease (b :: rest)

theorem mainMap_dependencies_precede : dependenciesPrecede mainMap = true := by
  decide

theorem mainMap_ids_increase : idsIncrease mainMap = true := by
  decide

end Econ803.BookNarrative
