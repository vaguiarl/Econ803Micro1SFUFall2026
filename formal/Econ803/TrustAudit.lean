import Econ803

/-!
# Kernel trust audit

The commands below ask Lean to report the axioms used by every coverage-listed
result and selected supporting declarations. The build script requires every
verified coverage declaration to occur here and accepts exactly
`Classical.choice`, `propext`, and `Quot.sound`; every other reported axiom is
rejected.
-/

#print axioms Econ803.Foundations.symmetricPart_is_equivalence
#print axioms Econ803.Foundations.strictPart_asymmetric
#print axioms Econ803.Foundations.strictPart_transitive
#print axioms Econ803.Foundations.finite_exists_greatest
#print axioms Econ803.Foundations.relation_subset_transitiveClosure
#print axioms Econ803.Foundations.transitiveClosure_transitive
#print axioms Econ803.Foundations.transitiveClosure_least
#print axioms Econ803.Foundations.partialOrder_has_linearExtension

#print axioms Econ803.Choice.rational_choice_satisfies_WARP
#print axioms Econ803.Choice.rationalization_implies_WARP

#print axioms Econ803.Consumer.utilityDemand_scale_iff
#print axioms Econ803.Consumer.demanded_bundle_exhausts_budget
#print axioms Econ803.Consumer.finite_GARP_iff_Afriat_inequalities
#print axioms Econ803.Consumer.finite_Afriat_theorem
#print axioms Econ803.Consumer.finite_Afriat_constructive
#print axioms Econ803.Consumer.compensated_law_of_demand
#print axioms Econ803.Consumer.finite_wgarp_cmu_characterization
#check Econ803.Consumer.IsExpenditureValue
#check Econ803.Consumer.IsSupergradientOn
#print axioms Econ803.Consumer.expenditure_homogeneous
#print axioms Econ803.Consumer.expenditure_concave
#print axioms Econ803.Consumer.hicksian_bundle_is_supergradient

#print axioms Econ803.Uncertainty.monotoneCoupling_implies_expectedUtility_order
#print axioms Econ803.DiscreteChoice.logit_odds_ratio_algebraic
#print axioms Econ803.DiscreteChoice.logit_odds_ratio

#check Econ803.Firm.IsProfitValue
#check Econ803.Firm.IsSubgradientOn
#print axioms Econ803.Firm.profit_homogeneous
#print axioms Econ803.Firm.profit_convex
#print axioms Econ803.Firm.profit_maximizer_is_subgradient
#print axioms Econ803.Firm.profit_maximizer_is_efficient

#print axioms Econ803.Equilibrium.priceSupport_rulesOut_paretoImprovement
#print axioms Econ803.Equilibrium.priceSupport_rulesOut_coalitionBlock
#print axioms Econ803.Equilibrium.priceSupport_rulesOut_strongCoalitionBlock

#print axioms Econ803.BookNarrative.mainMap_dependencies_precede
