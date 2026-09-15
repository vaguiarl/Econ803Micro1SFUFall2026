/-!
This module checks the architecture of the book, not the mathematical truth of
the economic claims. Logical order and physical reading order are deliberately
separate: Order Theory is a logical root but appears as Appendix A.
-/

namespace Econ804.BookNarrative

inductive ClaimKind where
  | foundation | definition | model | analyticResult | application
deriving DecidableEq, Repr

inductive VerificationLevel where
  | localLean | externalLean | textbookProof | citedTheorem | expository
deriving DecidableEq, Repr

structure NarrativeStep where
  logicalId : Nat
  readingPosition : Nat
  label : String
  kind : ClaimKind
  verification : VerificationLevel
  dependencies : List Nat
deriving Repr

def mainMap : List NarrativeStep := [
  { logicalId := 1, readingPosition := 16,
    label := "Relations, orders, closures, and extensions",
    kind := .foundation, verification := .localLean, dependencies := [] },
  { logicalId := 2, readingPosition := 1,
    label := "Commodity, budget, choice, and demand primitives",
    kind := .definition, verification := .textbookProof, dependencies := [1] },
  { logicalId := 3, readingPosition := 2,
    label := "Preference rationalization and WARP",
    kind := .analyticResult, verification := .localLean, dependencies := [1, 2] },
  { logicalId := 4, readingPosition := 3,
    label := "Utility representation and observed-demand restrictions",
    kind := .analyticResult, verification := .citedTheorem, dependencies := [2, 3] },
  { logicalId := 5, readingPosition := 3,
    label := "Consumer duality, integrability, GARP, and Afriat",
    kind := .analyticResult, verification := .externalLean, dependencies := [3, 4] },
  { logicalId := 6, readingPosition := 4,
    label := "Sparse-max deviations from benchmark demand",
    kind := .model, verification := .expository, dependencies := [4, 5] },
  { logicalId := 7, readingPosition := 5,
    label := "Expected utility, risk attitudes, and dominance",
    kind := .analyticResult, verification := .citedTheorem, dependencies := [1, 3, 4] },
  { logicalId := 8, readingPosition := 6,
    label := "Aggregation restrictions and representative demand",
    kind := .analyticResult, verification := .textbookProof, dependencies := [4, 5] },
  { logicalId := 9, readingPosition := 7,
    label := "Random-utility and random-expected-utility representation",
    kind := .analyticResult, verification := .citedTheorem, dependencies := [3, 7] },
  { logicalId := 10, readingPosition := 8,
    label := "Production, profit, cost, and efficiency",
    kind := .analyticResult, verification := .textbookProof, dependencies := [1, 2] },
  { logicalId := 11, readingPosition := 9,
    label := "Competitive equilibrium and partial-equilibrium welfare",
    kind := .analyticResult, verification := .textbookProof, dependencies := [4, 5, 10] },
  { logicalId := 12, readingPosition := 10,
    label := "General equilibrium and welfare",
    kind := .analyticResult, verification := .citedTheorem, dependencies := [4, 5, 10, 11] },
  { logicalId := 13, readingPosition := 11,
    label := "Excess demand, existence, regularity, and uniqueness",
    kind := .analyticResult, verification := .citedTheorem, dependencies := [8, 12] },
  { logicalId := 14, readingPosition := 12,
    label := "Revealed-equilibrium testability",
    kind := .analyticResult, verification := .citedTheorem, dependencies := [5, 13] },
  { logicalId := 15, readingPosition := 13,
    label := "Sequential trade and contingent commodities",
    kind := .analyticResult, verification := .citedTheorem, dependencies := [7, 12] },
  { logicalId := 16, readingPosition := 14,
    label := "Matching stability, the core, and TTC",
    kind := .analyticResult, verification := .citedTheorem, dependencies := [1, 3] },
  { logicalId := 17, readingPosition := 15,
    label := "CGE calibration and counterfactuals",
    kind := .application, verification := .expository, dependencies := [10, 12, 13] }
]

def hasLogicalId (steps : List NarrativeStep) (id : Nat) : Bool :=
  steps.any (fun s => s.logicalId == id)

def dependenciesExistAndPrecede (steps : List NarrativeStep) : Bool :=
  steps.all fun s =>
    s.dependencies.all fun d => hasLogicalId steps d && d < s.logicalId

def logicalIdsStrictlyIncrease : List NarrativeStep → Bool
  | [] | [_] => true
  | a :: b :: rest =>
      a.logicalId < b.logicalId && logicalIdsStrictlyIncrease (b :: rest)

def explicitRoot (step : NarrativeStep) : Bool :=
  !step.dependencies.isEmpty || step.kind == .foundation

def rootsAreFoundations (steps : List NarrativeStep) : Bool :=
  steps.all explicitRoot

def validReadingPosition (step : NarrativeStep) : Bool :=
  1 <= step.readingPosition && step.readingPosition <= 16

def readingPositionsValid (steps : List NarrativeStep) : Bool :=
  steps.all validReadingPosition

theorem mainMap_dependencies_valid :
    dependenciesExistAndPrecede mainMap = true := by
  decide

theorem mainMap_logical_ids_ordered :
    logicalIdsStrictlyIncrease mainMap = true := by
  decide

theorem mainMap_roots_are_foundations :
    rootsAreFoundations mainMap = true := by
  decide

theorem mainMap_reading_positions_valid :
    readingPositionsValid mainMap = true := by
  decide

end Econ804.BookNarrative
