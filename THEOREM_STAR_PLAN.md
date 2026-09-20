# Two-level theorem architecture

**Manuscript:** *Microeconomic Theory I*

**Authoritative source audited:** `notes/Microeconomics_1_notes_by_Victor_Aguiar.lyx`

**Inventory audited:** `formal/theorem_inventory.tsv`
**Purpose:** give the main text short, memorable theorem statements while preserving exact assumptions, complete arguments, citations, and formal-verification boundaries in a technical appendix.

**Implementation status (19 September 2026):** Appendix B and the paired reader statements are implemented for `TS-C03-WGARP-CMU` and `TS-C03-WARP-CMU`. The live ledger contains 24 pairs: 2 migrated, 19 planned, and 3 source-gated. The WGARP pair is delegated to a checked wrapper around the pinned external theorem; the WARP strict-CMU pair is cited only and has no Lean certificate. `formal/theorem_pairs.tsv` is authoritative for current status.

## Editorial decision

Adopt a paired result architecture:

1. A **reader-level theorem**, printed as `Theorem 3.4*`, states the economic content in the chapter where students need it.
2. A **full theorem**, printed in a new Appendix B, gives the exact domain, quantifiers, hypotheses, conclusion, and proof or an explicit proof-status record.
3. When a Lean theorem exists, the appendix entry links the mathematical statement to the exact module and declaration. The star by itself never means “Lean verified.”

The star means **compressed reader statement**, not “approximately true,” “unproved,” or “true under unspecified regularity conditions.” A reader theorem must remain mathematically true under assumptions that are visible in the theorem or in a clearly named assumption block immediately preceding it. Details may be deferred only when their omission does not change the claim's truth conditions.

This architecture should be introduced once in the preface:

> A starred theorem gives the reader-level form of a central result. Its exact hypotheses and full mathematical record appear in Appendix B under the linked result identifier. Verification status is reported separately.

For accessibility, the PDF text and bookmarks should say “Reader-level theorem,” not rely on the asterisk alone. In LaTeX/LyX, use a dedicated numbered environment such as `readerthm`; do not implement this with `\newtheorem*`, whose asterisk conventionally means “unnumbered.” The printed heading can nevertheless be `Theorem 3.4*`.

## What is confirmed about the Strzalecki model

The inspiration is Tomasz Strzalecki's *Stochastic Choice Theory*, but the proposed pairing is an adaptation rather than a reproduction of his system.

### Confirmed from primary and official sources

- In Strzalecki's [lecture slides](https://scholar.harvard.edu/files/tomasz/files/scslides34.pdf), the two symbols have distinct meanings: **`Theorem†`** means that some terms have not been defined, whereas **`Theorem‡`** means that additional technical conditions are needed.
- In the author's [November 2023 preprint](https://tomasz.scholars.harvard.edu/file_url/162), Strzalecki uses **`Theorem†`**, not `Theorem*`. The preface combines the slide deck's concerns by explaining that the dagger flags missing technical details or definitions and directs the reader to the original formal source.
- The same preprint uses the dagger locally on axioms as well as theorems. It also sends some ordinary, non-daggered propositions to its appendix for proofs. Thus the dagger is not a universal main-text/appendix pairing device.
- The official [Cambridge contents page](https://www.cambridge.org/core/books/stochastic-choice-theory/contents/C2D5EC7D39AAA0E4EAA9060750ECD481) confirms a 2025 Appendix A entitled “Additional Material and Proof Sketches.” The [author's book page](https://tomasz.scholars.harvard.edu/books) identifies the preprint as the manuscript for the Cambridge/Econometric Society monograph.

### Editorial adaptation for this book

Our system is deliberately stronger:

- every starred theorem has exactly one full counterpart in Appendix B;
- every full counterpart links back to the reader theorem;
- omitted assumptions are enumerated rather than hidden behind “usual conditions”;
- proof status and Lean status are separate fields;
- a deep theorem with only a citation is identified as such and is not described as having a complete proof in this book;
- no proof is copied from a copyrighted source. Standard arguments are either written independently, built from Mathlib or another licensed formal library, or delegated by precise citation.

## Audit of the current theorem surface

The prior inventory contained 245 rows, including 85 purported result rows: 67 `Proposition`, 11 `Theorem`, 3 `Lemma`, 2 `Corollary`, 1 `Fact`, and 1 `Claim`. Those were paragraph counts, not environment counts. After the grouping repair and the consumer restructure, the current inventory contains 230 records and 71 theorem-like environments:

| Environment | Current count |
|---|---:|
| Theorem | 14 |
| Proposition | 50 |
| Lemma | 3 |
| Corollary | 2 |
| Fact | 1 |
| Claim | 1 |

The repaired inventory also records all 23 proof environments and 57 generated problem environments; the prior version found only the 8 proofs written with a dedicated `Proof` layout.

The discrepancy has two causes:

1. the inventory counts successive LyX paragraphs inside one proposition as separate propositions (notably the numbered parts of the indirect-utility, expenditure, Hicksian-demand, and Afriat results);
2. some proofs and named results are ordinary prose rather than a dedicated LyX layout.

Before theorem migration, `formal_inventory.pl` needed to group a complete LyX theorem inset/environment as one record. That repair is now implemented: consecutive subparagraph layouts are grouped, raw-ERT proof blocks are recognized, and citations and subparts stay inside one record. Labels are deliberately left to the separate pairing ledger, where they can be checked as semantic identifiers rather than inferred from prose.

Important results currently invisible as theorem records include Roy's identity, the Slutsky equation, the Tarski--Seidenberg elimination principle, and the Brown--Matzkin result. The integrability section correctly refuses to state a global theorem without choosing a precise version; that restraint should be preserved.

## The three-layer contract

Every selected result receives a stable semantic identifier such as `TS-C03-AFRIAT`. Page and theorem numbers may change; the identifier may not. Several identifiers were assigned before the Fall 2026 reorganization, so their embedded `Cxx` segment is now historical. The `chapter` column of `formal/theorem_pairs.tsv`, rather than that segment, records the current chapter.

### Layer 1: reader theorem in the chapter

The reader theorem should contain:

- the economic environment in one sentence;
- the minimum assumptions a student must remember;
- the economically meaningful conclusion;
- a one- or two-sentence interpretation;
- a forward link: “Full statement and proof: Theorem B.x (`TS-...`).”

It should not contain proof machinery, alternative topologies, exceptional boundary cases, or a long list of equivalent formulations unless one of those is the economic lesson.

### Layer 2: full mathematical record in Appendix B

Each full entry should contain, in this order:

1. **Scope and primitives.** Domains, finiteness, topology, normalization, and whether maps are functions or correspondences.
2. **Full theorem.** All quantifiers and hypotheses; no phrases such as “the preceding assumptions” or “the usual regularity conditions.”
3. **Dependency list.** Earlier definitions, lemmas, and imported theorems.
4. **Proof.** A complete independent proof when feasible. If a research-scale proof is delegated, say “proof delegated” and give the exact theorem/page/DOI; do not label a sketch as a full proof.
5. **Boundary note.** Which conclusion fails if a salient assumption is removed.
6. **Formalization record.** `Lean-complete`, `Lean-core-only`, `external Lean`, `textbook proof`, or `cited theorem`, with exact module/declaration when applicable.

### Layer 3: Lean certificate

The Lean repository should formalize the **full** statement, or identify precisely the special case it proves. The mapping record should never infer equivalence merely because a declaration has a similar English name. A theorem receives a `Lean-complete` badge only when:

- the compiled declaration has no `sorry`, `admit`, or local axiom;
- its assumptions and conclusion match the appendix theorem under a documented encoding;
- all imported nonstandard libraries and versions are pinned;
- the build command is reproducible from a clean checkout.

## Proposed result-pair map

The following are the results that deserve the two-level treatment. Locations follow the Fall 2026 architecture; the live LyX inventory and `formal/theorem_pairs.tsv` control current locations and status. “Ready” means the audited manuscript already contained most of an independent proof. “Rebuild” means the result is central but its appendix proof must be consolidated or completed. “Source-gated” means an exact source theorem must first replace the present high-level summary.

| Pair ID | Audited or current location | Reader-level payload | Assumptions that must remain visible | Appendix B payload and proof boundary | Gate |
|---|---|---|---|---|---|
| `TS-C01-WARP-CLD` | Ch. 3, “Local Implications of WARP” | WARP plus budget exhaustion makes compensated demand slope downward; differentiability gives a negative-semidefinite symmetric Slutsky part. | Single-valued demand, strictly positive price/wealth domain, Walras' law, WARP; continuous differentiability only for the differential conclusion. | B.1 gives the finite-change CLD first, then the directional limit argument and the exact open-domain requirement for `p+ta`. | Ready |
| `TS-C02-RATIONAL-WARP` | Ch. 4, “Revealed Choice and WGARP”; `ChoiceTheory.lean` | Maximization of one complete and transitive preference cannot generate a strict revealed-preference reversal. | Nonempty menus, choice as the set of greatest elements, completeness and transitivity; state the set-valued WARP quantifiers. | B.2 proves the set-valued result and maps it to `rational_choice_satisfies_WARP` and `chosen_not_strictly_dominated`. | Ready / local Lean core |
| `TS-C03-CONTINUOUS-UTILITY` | Ch. 4, “Utility Representation” | A continuous total preorder on Euclidean commodity space admits a continuous utility representation. | `X=R_+^L`, total preorder, the exact continuity definition. | B.3 states the precise Debreu specialization, the topological lemma actually used, and either supplies a complete independent proof or delegates it exactly. The current paragraph is a proof sketch, not a full proof. | Rebuild / cited theorem |
| `TS-C03-DEMAND-CONTINUITY` | Ch. 1, utility maximization and demand correspondences | Continuous utility on a positive-price budget has maximizers; demand is nonempty, compact-valued and upper hemicontinuous, and indirect utility is continuous. | `X=R_+^L`, `p>>0`, `w>0`, continuous `u`; correspondence-valued demand. | B.4 merges the compact-budget argument and the Berge argument, including lower hemicontinuity at a binding budget. | Ready |
| `TS-C03-CONSUMER-DUALITY` | Ch. 2, indirect utility through the Slutsky equation | Utility and expenditure minimization are dual; envelope identities recover Marshallian and Hicksian demand; smooth duality yields Slutsky symmetry and negative semidefiniteness. | Continuous, locally nonsatiated preferences and positive prices for primal/dual equalities; attainable target above the baseline; uniqueness/differentiability and constraint qualifications only for Roy/Shephard; twice differentiability only for Hessian claims. | B.5 separates four claims: set-valued UMP/EMP duality, Roy, Shephard as a supergradient theorem, and smooth Slutsky. It must state exactly where equality is between correspondences. | Rebuild |
| `TS-C03-AFRIAT` | Ch. 3, “GARP and Afriat's Theorem”; external WGARP project | For finite price--quantity data, GARP, feasibility of Afriat inequalities, and rationalization by a continuous concave monotone utility are equivalent. | Finite `T`, `p^t>>0`, `x^t>=0`; expenditure exhaustion if wealth is separately observed; weak rationalization and the exact strict reverse edge. | B.6 gives all four implications, the finite feasibility lemma used in `(2)=>(3)`, the constructed utility, and an exact map to WGARP declarations. The current proof delegates the hardest implication and is not yet a complete proof. | Rebuild / external Lean |
| `TS-C03-WGARP-CMU` | Ch. 3, “WGARP and Coalitional Multi-Utility”; Appendix B | Finite budget data satisfy WGARP exactly when they admit the stated preference-function and coherent-CMU rationalizations. | Finite nonempty observations; at least two goods; strictly positive prices; nonzero nonnegative choices; distinguish the finite matrix/simplex normal forms from the book's broader compact-coalition formulation. | Appendix B records all six equivalent statements. `Econ803.Consumer.finite_wgarp_cmu_characterization` consumes `WGARP.theorem_one` at the pinned commit; the compact-coalition type bridge remains open. | Migrated / external Lean core |
| `TS-C03-WARP-CMU` | Ch. 3, “WGARP and Coalitional Multi-Utility”; Appendix B | Finite single-valued demand satisfies WARP exactly when it admits the corresponding strict coherent-CMU rationalization. | Finite nonempty observations; at least two goods; strictly positive prices; nonzero nonnegative choices; the cited theorem's exact strict star-concavity and strict-concavity clauses. | Appendix B gives the full mathematical record and delegates the representation theorem to the cited source. The pinned project has no matching WARP/strict-star-concavity declaration. | Migrated / cited theorem only |
| `TS-C05-EU-FINITE` | Ch. 5, “The Finite Expected-Utility Theorem” | On a finite prize set, rationality, independence, and mixture continuity characterize expected utility; Bernoulli utility is unique up to positive affine transformation. | Finite nonempty prize set, lotteries over it, complete/transitive preference, independence, mixture continuity. | B.7 combines the affine-representation lemma, finite-dimensional decomposition, and uniqueness proof. It must preserve “affine,” not silently replace it by “linear.” | Rebuild |
| `TS-C05-FOSD` | Ch. 5, finite-support and general-distribution FOSD | First-order stochastic dominance raises expected utility for every increasing Bernoulli utility. | State whether support is finite or distributions are general; measurability and integrability; precise conditions for strict inequality. | B.8 gives one general theorem and derives the finite theorem as a corollary. Replace “usual support conditions” with an exact strictness condition. | Rebuild |
| `TS-C05-RISK-DATA` | Ch. 5, “Revealed Expected Utility under Risk Aversion” | A finite dataset is rationalizable by risk-averse expected utility exactly when a finite system of first-order and monotonicity inequalities is feasible. | Finite states/observations, positive state probabilities, positive prices, interior observations; distinguish the boundary KKT version. | B.9 reproduces the full mathematical statement in the book's notation and gives an independent proof or a theorem-level proof delegation to Polisson--Quah--Renou. | Source-gated |
| `TS-C06-GORMAN` | Ch. 8, “Gorman Aggregation” | A common wealth slope in indirect utility makes aggregate demand depend on prices and total wealth, not the wealth distribution. | Differentiable indirect utilities, common positive slope `b(p)`, Roy's identity conditions, individual wealths summing to `W`. | B.10 gives the algebra and distinguishes a positive representative demand from a normative representative consumer. | Ready |
| `TS-C07-SURPLUS-ENVELOPE` | Ch. 6, “Attributes, Choice Probabilities, and Consumer Surplus” | Expected maximum utility is convex; under no ties its gradient is the choice-probability vector, and its Hessian has the associated symmetry/sign restrictions when it exists. | Finite alternatives, finite first moments, almost-sure unique maximizer; differentiability/C2 assumptions separated. | B.11 proves the envelope result. Call it the **expected-surplus envelope result**, not the full Williams--Daly--Zachary characterization theorem. | Rebuild |
| `TS-C08-FIRM-DUALITY` | Ch. 9, profit and cost | Profit and cost functions inherit homogeneity and curvature from optimization; differentiability recovers supply and conditional factor demand. | Nonempty technology, finiteness and attainment where needed; closed/convex/free-disposal or concavity assumptions attached only to the conclusions that use them. | B.12 uses a common support/value-function lemma and then states separate profit and cost specializations, including Hotelling and Shephard envelope results. | Rebuild |
| `TS-C09-PARTIAL-EQUILIBRIUM` | Ch. 10, partial equilibrium and welfare | In the maintained quasilinear market, a clearing price exists, is unique under strict monotonicity, and implements the planner allocation. | Put the curvature, endpoint, and tail conditions in a named “partial-market assumptions” box; do not say “the preceding assumptions.” | B.15 proves existence by continuity/endpoint signs, uniqueness by strict monotonicity, and states welfare as a corollary of B.13. Placing this entry after the welfare results removes a forward proof dependency. | Rebuild |
| `TS-C10-FIRST-WELFARE` | Ch. 11, “Welfare theorems” | Every competitive equilibrium allocation is Pareto efficient under local nonsatiation. | Finite consumers/firms, exact feasibility and ownership/budget equations, profit maximization, local nonsatiation; no convexity. | B.13 gives the value-comparison proof and records why local nonsatiation turns weak budget inequalities into the needed contradiction. | Ready |
| `TS-C10-SECOND-WELFARE` | Ch. 11, “Welfare theorems” | Under convexity and regularity, a Pareto-efficient allocation can be supported by prices and transfers. | Convex preferences and production sets, closed aggregate attainable set, continuity/local nonsatiation, the cheaper-bundle or properness condition, and conditions for positive rather than merely nonzero prices. | B.14 states the exact separation theorem used, proves support, and distinguishes price equilibrium with transfers from a Walrasian equilibrium with ownership income. | Rebuild |
| `TS-C11-EXISTENCE` | Ch. 12, “Existence” | A finite pure-exchange economy satisfying standard continuity, convexity, monotonicity, and endowment assumptions has a Walrasian equilibrium. | Spell out consumption sets, positive aggregate endowment, completeness/transitivity, continuity, convexity, strong monotonicity, and price normalization. Strict convexity is not an existence assumption. | B.16 gives the exact fixed-point version chosen for the book, boundary lemmas, and market-clearing step. | Rebuild / cited theorem |
| `TS-C11-GROSS-SUBSTITUTES` | Ch. 12, “Uniqueness and gross substitutes” | Strict gross substitutes makes the normalized equilibrium price vector unique. | Continuous aggregate excess demand, homogeneity, Walras' law, exact strict-GS/irreducibility condition, positive normalized prices; existence remains separate. | B.17 gives the maximum-relative-price proof and records the weak-GS counterboundary. | Ready after definition repair |
| `TS-C11-SMD` | Ch. 12, “What equilibrium theory does not identify” | Aggregate excess demand is highly flexible even when individual demand is rational. | The exact commodity dimension, price domain/normalization, regularity, Walras' law, homogeneity, boundary condition, and whether matching is global or only on compact subsets. | B.18 must select and state one precise Sonnenschein--Mantel--Debreu theorem from the original literature. The current phrase “essentially arbitrary shape” is perspective, not a formal theorem. | Source-gated |
| `TS-C12-BROWN-MATZKIN` | Ch. 13, “Brown--Matzkin theorem” | Fixed-preference equilibrium across finitely many observations imposes nontrivial semialgebraic restrictions on prices, incomes, and aggregate endowments. | Exact observables, latent allocations/endowments, model class, invariance and regularity assumptions, and the precise rationalizability notion. | B.19 must state the exact Brown--Matzkin theorem and its quantifier-elimination argument or delegate the proof at theorem level. The present “under their assumptions” wording is insufficient for a star. | Source-gated |
| `TS-C13-ARROW-RADNER` | Ch. 14, “Spot markets and sequential trade” | With complete asset markets and no arbitrage, sequential trading supports the same contingent-consumption allocations as Arrow--Debreu trade. | Finite states/goods/assets, `rank(R)=S`, no portfolio constraints, no arbitrage, positive state numeraires, continuous strictly monotone preferences; state that this is allocation equivalence, not existence. | B.20 gives the finite-dimensional state-price lemma and both budget-set mappings. | Rebuild |
| `TS-C14-GALE-SHAPLEY` | Ch. 15, “Deferred acceptance” | Deferred acceptance terminates, is stable, and is proposer-optimal among stable matchings. | Finite two-sided market; decide whether all partners are acceptable or allow unmatched agents and incomplete lists; strict preferences. | B.21 proves termination, the no-blocking lemma, and proposer optimality under the same acceptability convention as the chapter. | Rebuild |
| `TS-C14-TTC` | Ch. 15, “Housing markets and top trading cycles” | In a strict Shapley--Scarf housing market, TTC terminates and returns the unique core allocation, hence a Pareto-efficient competitive allocation. | Finite agents/houses, one initial owner per house, strict complete preferences, exact core/blocking convention. | B.22 gives the cycle/induction proof and separates ordinary core, strong core, and competitive-support conclusions. | Rebuild |

## Results that should not receive a star now

The star should remain scarce. The following material is important but should stay as a proposition, lemma, corollary, example, or roadmap.

| Material | Treatment | Reason |
|---|---|---|
| Walras-law derivative identities and `S(p,w)p=0` in Ch. 3 | Lemmas supporting `TS-C01-WARP-CLD` | They are proof components, not separate conceptual destinations. |
| Finite utility representation in Ch. 4 | Ordinary proposition with a complete short proof | Useful foundation but not one of the book's distinctive main results. |
| Ch. 4 abstract-choice rationalizability discussion | Keep as a preview linking back to `TS-C03-AFRIAT` | It must not duplicate the budget-specific Afriat theorem or claim that unrestricted selection from maximizers is informative. |
| Indirect-utility, expenditure, and Hicksian property lists | Lemmas in B.5 plus a synthesis table in Ch. 2 | Their current presentation inflates the theorem count and fragments one duality argument. |
| Global demand integrability | Keep as a roadmap until one precise theorem is chosen | The manuscript correctly notes that topology, rank, boundary behavior, and differential-system hypotheses vary across versions. |
| Sparse-max chain rule and optimal hiring threshold in Ch. 7 | Ordinary propositions | Model-specific derivations; the chapter does not yet contain one general representation or welfare theorem. |
| Local risk-premium approximation | Proposition/example | It is a second-order approximation, not an exact global theorem. |
| Aggregate-WARP sufficient condition in Ch. 8 | Proposition | Useful sufficient condition but secondary to Gorman aggregation. |
| Logit IIA in Ch. 6 | Proposition | Immediate model implication; retain as a diagnostic property. |
| Firm aggregation and supporting-price efficiency in Ch. 9 | Corollaries to B.12 and the separation theorem | Avoid a second proof of the same support-function logic. |
| Price normalization and Walras' law in Chs. 10 and 12 | Lemmas | They are dependencies of equilibrium theorems. |
| Local uniqueness from a nonsingular Jacobian | Proposition | A direct inverse-function corollary; not global uniqueness. |
| Walrasian allocations in the core | Proposition | Important, but a short consequence rather than the chapter's flagship theorem. |
| Order-theory results in Appendix A | Full theorems/lemmas, without stars | Appendix A is already the technical layer; a reader/full duplication inside it would add no value. |
| CGE accounting and calibration in Ch. 16 | Verification protocol, not theorem | The value is model closure, replication, units, and counterfactual validation rather than a universal analytic result. |

The infinite-lottery expected-utility theorem should remain a clearly labelled extension of `TS-C05-EU-FINITE` until its topology and proof are fully integrated. It should not be allowed to make the finite theorem's assumptions disappear from the reader's memory.

## Assumption bundles

Named assumption bundles make the reader theorem short without making it vague. Each bundle must be printed at first use and repeated in Appendix B; a bundle name is not a substitute for a definition.

| Bundle | Minimum contents | Used by |
|---|---|---|
| `CD` (observed demand) | Open domain in `R_{++}^L x R_{++}`, single-valued demand, Walras' law; differentiability added locally | Chapter 3 |
| `CT` (basic consumer) | `X=R_+^L`, `p>>0`, `w>0`, complete/transitive continuous locally nonsatiated preference with continuous representation | Chapters 1--2 |
| `SCT` (smooth consumer) | `CT` plus uniqueness and the exact differentiability/constraint qualification required by the envelope result | Chapter 2 Roy, Shephard, and Slutsky results |
| `FD` (finite revealed data) | Finite observations, positive prices, nonnegative bundles, observed expenditure exhaustion when wealth is separate, exact direct/strict relations | Afriat |
| `FEU` (finite expected utility) | Finite prize set, all lotteries, rational preference, independence, mixture continuity | finite EU |
| `GE` (general equilibrium) | Finite agents/goods/firms, explicit consumption/production sets, endowments and ownership, preference regularity, feasibility, normalized prices | welfare and existence |
| `HM` (housing market) | Finite agents/houses, bijective initial ownership, strict complete preferences | TTC |

Do not create one omnibus “regular economy” bundle. The first welfare theorem does not need convexity; the second welfare theorem does. Walrasian existence and uniqueness use different assumptions. Keeping those differences visible is part of the economic lesson.

## Duplication and cross-reference policy

The paired architecture will fail if a theorem is restated independently in several chapters. Apply the following ownership rules.

1. **Afriat belongs to Ch. 3.** Ch. 4 gives an unnumbered abstract-choice preview and links back. The eventual Appendix B entry owns the full technical statement and proof record.
2. **The two Slutsky appearances answer different questions.** Ch. 3 derives an observable negative-semidefinite restriction from WARP without utility. Ch. 2 derives symmetry and negative semidefiniteness from smooth utility duality. Cross-reference the two; do not merge their hypotheses or proofs.
3. **The Ch. 2 summary is a synthesis table, not another proposition.** It should point to the paired results for duality, envelope identities, and Slutsky restrictions.
4. **General FOSD owns the theorem.** The finite-prize result is a corollary/example, not a separately proved theorem.
5. **One convex-envelope lemma supports three applications.** Consumer expenditure, firm profit/cost, and expected random-utility surplus should reuse a common Appendix B lemma while preserving their different concavity/convexity signs.
6. **General welfare theorems belong to Ch. 11.** The Edgeworth-box and quasilinear statements become applications or corollaries. They must not carry separately maintained proofs.
7. **SMD and Brown--Matzkin remain explicitly contrasted.** SMD varies preferences/economies to show aggregate flexibility; Brown--Matzkin holds preferences fixed across observations to obtain testable restrictions.
8. **Core terminology is global.** Chs. 12 and 15 must use one definitions table distinguishing blocking, weak blocking, core, and strong core before any core theorem is paired.

## Chapter-by-chapter migration plan

### Chapter 1: Utility Maximization and Consumer Demand

Merge UMP existence and Berge continuity into `TS-C03-DEMAND-CONTINUITY`. Keep the utility representation primitive and its ordinal interpretation explicit; Chapter 4 owns the representation question.

### Chapter 2: Duality, Comparative Statics, and Welfare

Consolidate UMP--EMP duality, Roy, Shephard, and the smooth Slutsky result in `TS-C03-CONSUMER-DUALITY`. Keep set-valued results separate from the uniqueness and differentiability assumptions used by envelope formulas.

### Chapter 3: Revealed Preference and Recoverability

Make `TS-C03-AFRIAT` the sole owner of classical finite-budget rationalizability and retain integrability as an honest roadmap rather than a theorem without global hypotheses. Consolidate compensated demand in `TS-C01-WARP-CLD`. The WGARP--CMU and WARP--CMU reader/full pairs are already migrated; their external-proof boundaries must remain visible.

### Chapter 4: Choice Without Budget Geometry

Create `TS-C02-RATIONAL-WARP`. Keep finite utility representation unstarred and short. Pair continuous utility representation with a technical record only when the precise Debreu specialization and proof delegation are frozen. The abstract GARP discussion should point back to Chapter 3 rather than restate Afriat.

### Chapter 5: Expected Utility and Risk

Create the finite EU, FOSD, and finite-data risk-aversion pairs. Make affine uniqueness part of the finite EU pair. Treat the compact-metric lottery theorem as a technical extension with its own exact source and proof status. Merge finite and general FOSD proof logic.

### Chapter 6: Stochastic Choice and Random Utility

Pair the expected-surplus envelope theorem. Retain logit IIA as an easily checked implication. Do not call the book's envelope statement the full Williams--Daly--Zachary characterization.

### Chapter 7: Limited Attention and Costly Information

Do not add a star solely to balance chapters. Retain the sparse-max comparative statics and rational-inattention first-order conditions as ordinary propositions until a general behavioral or welfare theorem is frozen with a complete proof record.

### Chapter 8: Aggregate Demand and Representative Consumers

Make Gorman aggregation the sole star. Keep aggregate WARP as a sufficient-condition proposition. State explicitly that positive aggregation does not by itself justify interpersonal welfare comparisons.

### Chapter 9: Theory of the Firm

Pair profit/cost duality in one reader theorem with two clearly separated parts. Reuse a common Appendix B convex-envelope lemma rather than copying the consumer-duality proof. Keep technology aggregation and supporting-price efficiency as corollaries.

### Chapter 10: Competitive Markets and Partial Equilibrium

Pair existence and uniqueness for the explicit quasilinear model. Make its welfare claims corollaries of the general welfare theorems in Chapter 11. Replace “preceding assumptions” by a named block that can be read with the theorem in isolation.

### Chapter 11: General Equilibrium Theory

Create separate first- and second-welfare reader theorems; the difference in assumptions is pedagogically essential. Convert Edgeworth-box welfare statements to worked applications and keep the separating-hyperplane machinery in the technical appendix.

### Chapter 12: Positive Theory of Equilibrium

Pair existence and gross-substitutes uniqueness. Give the local-regularity result ordinary proposition status. Reserve the SMD star until a precise original theorem is chosen; the current wording is too elastic to be a full theorem. Keep core membership as a proposition with a precise blocking convention.

### Chapter 13: Testable Restrictions on the Equilibrium Manifold

The Brown--Matzkin result is conceptually central and ultimately deserves a pair, but it is not migration-ready. First extract the exact source theorem, align the observable and latent variables, and decide whether the book will prove quantifier elimination or delegate it.

### Chapter 14: Sequential Trade

Pair Arrow--Radner allocation equivalence. Surface completeness, no arbitrage, and the absence of portfolio constraints. The full record should make both budget mappings explicit and state that equilibrium existence is not part of the theorem.

### Chapter 15: Matching

Pair Gale--Shapley and TTC separately. Before doing so, choose one acceptability convention for deferred acceptance and one core convention for housing. Both proofs are finite and good candidates for Lean after the mathematical statements are frozen.

### Chapter 16: Computable General Equilibrium

Do not invent a flagship analytic theorem. Add a model-validation protocol: benchmark replication, accounting balance, homogeneity and numeraire invariance, complementarity residuals, and welfare-accounting checks. These are reproducibility obligations, not a theorem star.

### Appendix A: Order Theory

Retain it as the mathematical foundation. Complete the elementary proofs and keep the Szpilrajn result's dependence on choice/Zorn explicit. Because this is already the technical layer, do not repeat its statements in Appendix B.

### Appendix B: Technical Theorem Records

The appendix currently contains the exact WGARP--CMU and WARP--CMU records. Add future entries in dependency order and include chapter backlinks. Each entry must be readable independently of surrounding prose. Shared analysis or convexity lemmas may be reused, but every reader theorem still needs a direct link to the exact full theorem that uses them.

## Machine-readable pairing ledger

The implementation ledger is `formal/theorem_pairs.tsv`. Its columns are:

```text
pair_id	chapter	reader_label	full_label	reader_title	full_title	migration_status	proof_status	lean_status	lean_module	lean_decl	source_key	assumption_bundle	dependencies
```

`migration_status` records `planned`, `source_gated`, or `migrated`.
`proof_status` distinguishes `partial`, `draft_complete`, `delegated`, and
`source_gated` from the much stronger `complete`. `lean_status` distinguishes
`planned`, `core_only`, and `external_core` from `complete`. Two rows are
currently migrated: WGARP--CMU is delegated with a checked external core, and
WARP--strict-CMU is delegated without a Lean certificate. No row is marked
proof-complete or Lean-complete.
Semicolon-separated dependencies use the literal `none` when a pair has no
dependency in this 24-result graph.

The build should reject:

- a reader theorem without exactly one full target;
- a full theorem without a backlink;
- duplicate pair IDs or labels;
- `Lean-complete` without a compiled declaration;
- `proof complete` when the appendix contains only a sketch or citation;
- forbidden vague phrases in a full theorem (`usual assumptions`, `under regularity`, `the preceding conditions`, or `and so on`);
- a theorem inventory in which one LyX result environment becomes several result records.

## Formalization priorities

The two-level architecture should drive, rather than merely decorate, the Lean repository.

### Priority 1: reuse or complete existing finite cores

- `TS-C02-RATIONAL-WARP` from `ChoiceTheory.lean`;
- Appendix A relation parts and maximal/greatest results from `OrderTheory.lean`;
- `TS-C03-AFRIAT` through the existing WGARP project, with an exact theorem map;
- finite expected utility, finite FOSD, Gale--Shapley, and TTC after their statements are frozen.

### Priority 2: finite-dimensional algebra and convexity

- WARP to CLD;
- Gorman aggregation;
- expected-surplus envelope special cases;
- firm value-function curvature and homogeneity;
- partial-equilibrium monotonicity;
- Arrow--Radner spanning and budget equivalence;
- gross-substitutes uniqueness.

### Priority 3: library-intensive analysis

- Berge continuity and correspondence results;
- Roy, Shephard, and Slutsky under explicit smoothness;
- general-distribution FOSD;
- welfare separation and Walrasian existence.

### Statement-first, no verification claim yet

- Debreu continuous utility representation;
- the Polisson--Quah--Renou finite-data theorem;
- Sonnenschein--Mantel--Debreu;
- Brown--Matzkin.

For these results, a compiled Lean *statement* with imported hypotheses is not a proof. Do not add axioms or opaque placeholders to make the coverage table look complete.

## Acceptance checklist for each pair

A pair is complete only when all answers are “yes.”

1. Does the reader theorem state a true result under visible or explicitly named assumptions?
2. Can a reader locate its one full counterpart immediately?
3. Does the full theorem define every object and quantify every variable?
4. Are function/correspondence, weak/strict, local/global, and existence/uniqueness distinctions preserved?
5. Is the proof complete, or is its delegation labelled honestly and cited precisely?
6. Does the proof use only earlier dependencies, with no cycle or forward bridge hidden in prose?
7. If Lean is claimed, does the exact declaration compile from a pinned clean environment?
8. Has the old duplicate statement been converted to a preview, corollary, application, or cross-reference?
9. Does the theorem have a failure/boundary note for its economically salient assumptions?
10. Has an independent reader compared the reader theorem, full theorem, proof, and Lean declaration side by side?

## Recommended order of work

1. Repair the inventory so environments and proofs are counted correctly.
2. Add stable pair IDs, labels, and the Appendix B scaffold without rewriting theorem content.
3. Migrate the proof-ready spine: WARP/CLD, rational choice/WARP, demand continuity, consumer duality, Afriat, finite EU/FOSD, and Gorman.
4. Migrate production, partial equilibrium, Arrow--Radner, and matching.
5. Consolidate the two welfare theorems and Walrasian existence.
6. Freeze exact source-level statements for risk-data rationalization, SMD, and Brown--Matzkin before giving them stars.
7. Only after mathematical statements are frozen, connect the Lean repository and publish result-level badges.

This sequence gives students a useful reader layer early while preventing the star system from becoming a typographic promise that the technical layer cannot yet keep.
