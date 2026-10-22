import Econ803.Equilibrium.Welfare

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

This second map audits the niche consumption and product space chapter. It records the
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

/-!
## Unified general equilibrium chapter

The map below records the dependency architecture of Chapter 11 and its
technical appendix, not a literal page order or an existence formalization.
In particular, budget continuity, the capped demand theorem,
Brouwer, the clearing and uncapping step, and the Kakutani extension are
analytic results. Their proofs remain in the textbook or its cited sources.
Strict convexity is needed for the function proof, not the correspondence
extension. Regularity and gross substitutes are additional assumptions, not
consequences of existence. Finite observation restrictions characterize a
maintained model; they do not assert that arbitrary observations fit it.
-/

def generalEquilibriumMap : List NarrativeClaim := [
  { logicalId := 1,
    label := "Finite exchange economy with strictly positive individual endowments",
    kind := .modelAssumption, dependencies := [] },
  { logicalId := 2,
    label := "Continuous convex strongly monotone preferences",
    kind := .modelAssumption, dependencies := [1] },
  { logicalId := 3,
    label := "Strict convexity for the unique demand function branch",
    kind := .modelAssumption, dependencies := [2] },
  { logicalId := 4,
    label := "Compact capped budgets are continuous on the closed price simplex",
    kind := .analyticResult, dependencies := [1, 2] },
  { logicalId := 5,
    label := "Unique continuous capped demand by the maximum theorem",
    kind := .analyticResult, dependencies := [2, 3, 4] },
  { logicalId := 6,
    label := "Continuous price self map on the closed simplex",
    kind := .definition, dependencies := [1, 5] },
  { logicalId := 7,
    label := "The continuous simplex map has a fixed point by Brouwer",
    kind := .analyticResult, dependencies := [6] },
  { logicalId := 8,
    label := "Affordability gives feasibility; positivity and uncapping give equilibrium",
    kind := .analyticResult, dependencies := [1, 2, 5, 7] },
  { logicalId := 9,
    label := "Appendix Kakutani proof drops strict convexity and keeps convex demand values",
    kind := .analyticResult, dependencies := [1, 2, 4] },
  { logicalId := 10,
    label := "Competitive optimality and budget equalities give price support",
    kind := .analyticResult, dependencies := [1, 8] },
  { logicalId := 11,
    label := "The finite price support certificate implies Pareto efficiency",
    kind := .analyticResult, dependencies := [10] },
  { logicalId := 12,
    label := "Differentiable normalized excess demand and a nonsingular reduced Jacobian",
    kind := .modelAssumption, dependencies := [8] },
  { logicalId := 13,
    label := "Regularity gives local uniqueness, not global uniqueness",
    kind := .analyticResult, dependencies := [12] },
  { logicalId := 14,
    label := "A separately stated strict gross substitutes condition",
    kind := .modelAssumption, dependencies := [8] },
  { logicalId := 15,
    label := "Strict gross substitutes give normalized global price uniqueness",
    kind := .analyticResult, dependencies := [14] },
  { logicalId := 16,
    label := "Coalitions redistribute their own endowments under the strong blocking convention",
    kind := .definition, dependencies := [1] },
  { logicalId := 17,
    label := "Budget equalities and common price support rule out a strong coalition block",
    kind := .analyticResult, dependencies := [10, 16] },
  { logicalId := 18,
    label := "Finite equilibrium observations distinguish observed and latent quantities",
    kind := .definition, dependencies := [1, 8] },
  { logicalId := 19,
    label := "Fixed preference consistency and market clearing characterize finite data rationalization",
    kind := .analyticResult, dependencies := [2, 18] }
]

def claimRootsAreExplicit (steps : List NarrativeClaim) : Bool :=
  steps.all fun s =>
    !s.dependencies.isEmpty || s.kind == .economicPremise ||
      s.kind == .modelAssumption || s.kind == .empiricalInput

theorem generalEquilibriumMap_dependencies_precede :
    claimDependenciesPrecede generalEquilibriumMap = true := by
  decide

theorem generalEquilibriumMap_ids_increase :
    claimIdsIncrease generalEquilibriumMap = true := by
  decide

theorem generalEquilibriumMap_roots_explicit :
    claimRootsAreExplicit generalEquilibriumMap = true := by
  decide

theorem generalEquilibriumMap_theory_independent_of_evidence :
    theoryAvoidsEmpiricalInputs generalEquilibriumMap = true := by
  decide

/-- Abstract propositions used to lint the chapter's multi-premise argument.
These fields are not definitions of an economy or claims proved by this file.
The analytic implications are explicit proof obligations in `Links` below.
`priceSupportCertificate` includes market clearing, individual budget
equalities, and common weak and strict support inequalities. -/
structure GeneralEquilibriumClaims where
  exchangeModel : Prop
  continuousConvexPreferences : Prop
  strictConvexity : Prop
  continuousCompactBudgets : Prop
  continuousCappedDemand : Prop
  continuousSimplexMap : Prop
  cappedFixedPoint : Prop
  equilibrium : Prop
  priceSupportCertificate : Prop
  paretoEfficiency : Prop
  regularity : Prop
  localUniqueness : Prop
  strictGrossSubstitutes : Prop
  normalizedGlobalUniqueness : Prop
  strongCore : Prop
  finiteObservationModel : Prop
  finiteRationalizabilityCharacterization : Prop

structure GeneralEquilibriumCommonInputs (c : GeneralEquilibriumClaims) : Prop where
  exchangeModel : c.exchangeModel
  continuousConvexPreferences : c.continuousConvexPreferences

/-- Every analytic step is an input, not a concealed axiom or placeholder.
The final finite-data link is a characterization theorem conditional on its
observation model, not a claim that a given dataset is rationalizable. The
price support consequences can be instantiated by the concrete checked
certificate theorem below; deriving support from optimization is separate. -/
structure GeneralEquilibriumLinks (c : GeneralEquilibriumClaims) : Prop where
  budgetContinuity : c.exchangeModel → c.continuousConvexPreferences →
    c.continuousCompactBudgets
  cappedDemandContinuity : c.continuousCompactBudgets →
    c.continuousConvexPreferences → c.strictConvexity → c.continuousCappedDemand
  simplexMap : c.exchangeModel → c.continuousCappedDemand → c.continuousSimplexMap
  brouwer : c.continuousSimplexMap → c.cappedFixedPoint
  clearingAndUncapping : c.exchangeModel → c.continuousConvexPreferences →
    c.continuousCappedDemand → c.cappedFixedPoint → c.equilibrium
  optimizationGivesSupport : c.equilibrium → c.priceSupportCertificate
  priceSupportConsequences : c.priceSupportCertificate →
    c.paretoEfficiency ∧ c.strongCore
  regularityGivesLocalUniqueness : c.equilibrium → c.regularity → c.localUniqueness
  grossSubstitutesGiveGlobalUniqueness : c.equilibrium → c.strictGrossSubstitutes →
    c.normalizedGlobalUniqueness
  finiteDataCharacterization : c.exchangeModel → c.continuousConvexPreferences →
    c.finiteObservationModel → c.finiteRationalizabilityCharacterization

/-- The correspondence branch is independent of every unique demand or
Brouwer bridge. It does not require a proof of the function branch. -/
structure GeneralEquilibriumConvexLinks (c : GeneralEquilibriumClaims) : Prop where
  budgetContinuity : c.exchangeModel → c.continuousConvexPreferences →
    c.continuousCompactBudgets
  kakutani : c.exchangeModel → c.continuousConvexPreferences →
    c.continuousCompactBudgets → c.equilibrium

structure GeneralEquilibriumConclusions (c : GeneralEquilibriumClaims) : Prop where
  equilibrium : c.equilibrium
  welfare : c.paretoEfficiency
  core : c.strongCore
  localUniquenessUnderRegularity : c.regularity → c.localUniqueness
  globalUniquenessUnderGrossSubstitutes : c.strictGrossSubstitutes →
    c.normalizedGlobalUniqueness
  finiteDataCharacterization : c.finiteObservationModel →
    c.finiteRationalizabilityCharacterization

/-- Logical closure of the function-proof narrative. This theorem checks
composition of declared bridges; it does not prove Brouwer, continuity,
uncapping, equilibrium existence, or the finite-data characterization. -/
theorem generalEquilibrium_function_branch_closes
    (c : GeneralEquilibriumClaims) (i : GeneralEquilibriumCommonInputs c)
    (strict : c.strictConvexity) (links : GeneralEquilibriumLinks c) :
    GeneralEquilibriumConclusions c := by
  have budgets := links.budgetContinuity i.exchangeModel i.continuousConvexPreferences
  have demand := links.cappedDemandContinuity budgets i.continuousConvexPreferences strict
  have selfMap := links.simplexMap i.exchangeModel demand
  have fixedPoint := links.brouwer selfMap
  have equilibrium := links.clearingAndUncapping i.exchangeModel
    i.continuousConvexPreferences demand fixedPoint
  have consequences := links.priceSupportConsequences
    (links.optimizationGivesSupport equilibrium)
  exact {
    equilibrium := equilibrium
    welfare := consequences.1
    core := consequences.2
    localUniquenessUnderRegularity := links.regularityGivesLocalUniqueness equilibrium
    globalUniquenessUnderGrossSubstitutes :=
      links.grossSubstitutesGiveGlobalUniqueness equilibrium
    finiteDataCharacterization :=
      links.finiteDataCharacterization i.exchangeModel i.continuousConvexPreferences
  }

/-- The appendix branch has no strict convexity input. Kakutani remains an
explicit analytic bridge rather than a Lean-verified existence theorem. -/
theorem generalEquilibrium_convex_branch_closes
    (c : GeneralEquilibriumClaims) (i : GeneralEquilibriumCommonInputs c)
    (links : GeneralEquilibriumConvexLinks c) : c.equilibrium := by
  exact links.kakutani i.exchangeModel i.continuousConvexPreferences
    (links.budgetContinuity i.exchangeModel i.continuousConvexPreferences)

/-- Concrete, kernel-checked realization of the finite welfare and core
consequences. All price support, market clearing, and individual budget
equalities are hypotheses. This does not derive those hypotheses from an
equilibrium or prove an existence theorem. -/
theorem generalEquilibrium_priceSupport_consequences
    {I : Type*} [Fintype I] {L : Nat}
    (r : I → Econ803.Consumer.Bundle L → Econ803.Consumer.Bundle L → Prop)
    (p resources : Econ803.Consumer.Bundle L)
    (endowment x : I → Econ803.Consumer.Bundle L)
    (hclear : Econ803.Equilibrium.aggregate x = resources)
    (hbudget : ∀ i, Econ803.Consumer.expenditure p (x i) =
      Econ803.Consumer.expenditure p (endowment i))
    (hsupport : Econ803.Equilibrium.PriceSupportsAt r p x) :
    (¬ ∃ y : I → Econ803.Consumer.Bundle L,
      Econ803.Equilibrium.aggregate y = resources ∧
        Econ803.Equilibrium.ParetoDominates r y x) ∧
    (¬ ∃ (S : Finset I) (_hS : S.Nonempty) (y : I → Econ803.Consumer.Bundle L),
      Econ803.Equilibrium.aggregateOn S y =
        Econ803.Equilibrium.aggregateOn S endowment ∧
      (∀ i ∈ S, r i (y i) (x i)) ∧
        ∃ j ∈ S, Econ803.Foundations.StrictPart (r j) (y j) (x j)) := by
  exact ⟨Econ803.Equilibrium.priceSupport_rulesOut_paretoImprovement
    r p resources x hclear hsupport,
    Econ803.Equilibrium.priceSupport_rulesOut_strongCoalitionBlock
      r p endowment x hbudget hsupport⟩

end Econ803.BookNarrative
