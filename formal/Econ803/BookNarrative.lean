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

/-!
## Product-space synthesis

This second map audits the new many-product-consumer section.  It records the
logical status and order of its claims; it does not prove the analytic or
empirical content named by those claims.
-/

inductive ClaimKind where
  | economicPremise | modelAssumption | definition | analyticResult
  | empiricalInput | empiricalFinding | interpretation
deriving DecidableEq, Repr

structure NarrativeClaim where
  logicalId : Nat
  label : String
  kind : ClaimKind
  dependencies : List Nat
deriving Repr

def productSpaceMap : List NarrativeClaim := [
  { logicalId := 1, label := "Nielsen household-product panel",
    kind := .empiricalInput, dependencies := [] },
  { logicalId := 2,
    label := "Household concentration rises while aggregate concentration falls",
    kind := .empiricalFinding, dependencies := [1] },
  { logicalId := 3,
    label := "Catalog, consideration set, and purchased support are distinct",
    kind := .economicPremise, dependencies := [] },
  { logicalId := 4, label := "Metric product space and ideal points",
    kind := .definition, dependencies := [3] },
  { logicalId := 5,
    label := "Conditional unit demand, Euclidean mismatch, and stable adjacency",
    kind := .modelAssumption, dependencies := [4] },
  { logicalId := 6, label := "Only active neighbors receive local diversion",
    kind := .analyticResult, dependencies := [5] },
  { logicalId := 7, label := "Baskets are positive measures over product space",
    kind := .definition, dependencies := [3, 4] },
  { logicalId := 8, label := "Finite-data Afriat envelope is dimension-free",
    kind := .analyticResult, dependencies := [7] },
  { logicalId := 9, label := "Neighborhood compensated elasticity",
    kind := .definition, dependencies := [7] },
  { logicalId := 10,
    label := "Metric locality is an extra restriction, not a consequence of rationality",
    kind := .interpretation, dependencies := [6, 9] },
  { logicalId := 11,
    label := "Fixed supply marginals turn assignment into transferable-utility matching",
    kind := .modelAssumption, dependencies := [4, 7] },
  { logicalId := 12,
    label := "Niche evidence supports selection but not metric locality",
    kind := .interpretation, dependencies := [2, 10] }
]

def claimContainsId (steps : List NarrativeClaim) (id : Nat) : Bool :=
  steps.any (fun s => s.logicalId == id)

def claimDependenciesPrecede (steps : List NarrativeClaim) : Bool :=
  steps.all fun s =>
    s.dependencies.all fun d => claimContainsId steps d && d < s.logicalId

def claimIdsIncrease : List NarrativeClaim → Bool
  | [] | [_] => true
  | a :: b :: rest =>
      a.logicalId < b.logicalId && claimIdsIncrease (b :: rest)

def empiricalFindingsAreGrounded (steps : List NarrativeClaim) : Bool :=
  steps.all fun s =>
    if s.kind == .empiricalFinding then
      s.dependencies.any fun d =>
        steps.any fun prior => prior.logicalId == d && prior.kind == .empiricalInput
    else true

def theoryAvoidsEmpiricalInputs (steps : List NarrativeClaim) : Bool :=
  steps.all fun s =>
    if s.kind == .modelAssumption || s.kind == .analyticResult then
      s.dependencies.all fun d =>
        steps.all fun prior =>
          prior.logicalId != d || prior.kind != .empiricalInput
    else true

theorem productSpaceMap_dependencies_precede :
    claimDependenciesPrecede productSpaceMap = true := by
  decide

theorem productSpaceMap_ids_increase : claimIdsIncrease productSpaceMap = true := by
  decide

theorem productSpaceMap_empirical_grounding :
    empiricalFindingsAreGrounded productSpaceMap = true := by
  decide

theorem productSpaceMap_theory_independent_of_evidence :
    theoryAvoidsEmpiricalInputs productSpaceMap = true := by
  decide

end Econ803.BookNarrative
