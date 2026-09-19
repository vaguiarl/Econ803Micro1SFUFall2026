# Consumer block restructuring plan

**Status:** proposed architecture; no manuscript moves have been made.

**Authoritative manuscript:** `notes/Microeconomics_1_notes_by_Victor_Aguiar.lyx`

## Editorial decision

Rebuild the consumer block around a forward economic model and its inverse
problem:

```text
utility maximization
  -> Marshallian demand and indirect utility
  -> duality, comparative statics, and welfare
  -> observable restrictions and revealed preference
  -> abstract choice without budget geometry
  -> expected utility and risk
  -> stochastic choice and random utility
  -> limited attention and rational inattention
```

This ordering starts with the model students will use. Revealed preference is
then the empirical content of that model, rather than a free-standing set of
axioms encountered before the model. Abstract choice comes afterward as a
genuine generalization from linear budgets to arbitrary menus.

The manuscript may take a utility function as a primitive in Chapter 1. This
does not make the later representation theorem circular: that theorem explains
when a preference-first model admits such an ordinal index. A short opening box
must state that utility is ordinal and point forward to the full representation
result.

## Why the current opening is not tight

The current opening offers three competing primitives before relating them:

1. Chapter 1 takes observable demand as primitive and develops WARP and the
   Slutsky matrix.
2. Chapter 2 starts again from abstract menus and preference rationalization.
3. Chapter 3 finally introduces utility maximization, then also contains
   duality, integrability, Afriat, welfare, and empirical applications.

The result is not merely repetition. It creates forward dependencies and hides
the hierarchy of implications.

- Demand is first a single-valued primitive, later a correspondence, and only
  afterward an optimizer.
- Budget sets, Walras' law, homogeneity, WARP/GARP, and the Slutsky matrix are
  each introduced more than once.
- Local nonsatiation is used before it is defined.
- Negative semidefiniteness is used before its formal definition.
- Quasilinearity is used in the Roy example before it is defined.
- Chapter 1 problems invoke preference maximization before the UMP appears.
- Chapter 2 says prices and wealth have not yet been introduced, although they
  dominate Chapter 1.
- Chapter 3 has 26 substantive sections and is currently performing the work
  of at least three chapters.

### Mathematical issue to correct during migration

The current abstract-choice definition of weak rationalization asks only for

```text
c(A) subset of the set of preference-greatest elements of A.
```

Under that definition, universal indifference weakly rationalizes every choice
dataset. The early claim that GARP is equivalent merely to weak rationalization
by a complete and transitive relation is therefore non-substantive as written.
The valid, economically meaningful finite-budget result is the later Afriat
theorem, with monotonicity/local nonsatiation and the budget structure made
explicit. The early result should become a preview and cross-reference, not a
second theorem.

## Proposed table of contents

## Part I. The Benchmark Consumer

### Chapter 1. Utility Maximization and Consumer Demand

**Question:** What is the benchmark model, and what behavior does it generate?

1. The benchmark model on one page
2. Commodities, consumption sets, prices, wealth, and budgets
3. Utility as an ordinal index and the assumption dictionary
4. The utility-maximization problem and existence
5. Marshallian demand and indirect utility
6. What the assumptions buy
   - local nonsatiation: budget exhaustion;
   - budget geometry: homogeneity of degree zero;
   - convexity: convex-valued demand;
   - strict convexity: uniqueness.
7. KKT conditions, corners, and tangency
8. Running examples: Cobb--Douglas, perfect substitutes, and quasilinear demand
9. Problems

The opening display should be

\[
x_u(p,w)\in\arg\max_{x\in X}\{u(x):p\cdot x\leq w\},
\]

followed immediately by a plain-language description of every object. Demand
is introduced after this display, not before it.

### Chapter 2. Duality, Comparative Statics, and Welfare

**Question:** How do we compute the model's price responses and welfare
implications?

1. Expenditure minimization, Hicksian demand, and expenditure
2. UMP--EMP duality
3. Roy's identity and Shephard's lemma
4. The Slutsky equation
5. Compensated and Marshallian price effects; the Giffen mechanism
6. Symmetry, negative semidefiniteness, and homogeneity restrictions
7. Money-metric utility, equivalent variation, and compensating variation
8. Homothetic and quasilinear benchmark classes
9. Problems

The present EMP, Hicksian demand, EMP KKT, Shephard, additional-properties,
and duality-summary sections should become one sustained argument. The two
current summary sections should become one synthesis table rather than new
formal results.

### Chapter 3. Revealed Preference and Recoverability

**Question:** Could the behavior we observe have been generated by Chapter 1's
model, and what can the data identify?

1. Observables: full demand systems versus finite datasets
2. Demand functions, correspondences, and expenditure exhaustion
3. WARP/WGARP and direct revealed preference on budgets
4. Compensated demand and differential restrictions
5. What WARP, smooth utility maximization, and integrability each imply
6. Smooth-demand integrability
7. Finite data, GARP, and Afriat's theorem
8. SARP and strict rationalization
9. Counterfactual choice and welfare bounds
10. CCEI, rationality experiments, and measurement error: one case study
11. Problems

One comparison table should make the hierarchy explicit:

| Maintained structure | Observable implication |
|---|---|
| Walras' law + WARP | compensated law of demand; with differentiability, a negative-semidefinite symmetric Slutsky part |
| Regular smooth utility maximization | Walras, HD0, Slutsky symmetry and negative semidefiniteness |
| Smooth integrability hypotheses | sufficiency for utility generation on the stated domain |
| Finite budget data + GARP | Afriat inequalities and constructive rationalization |

Known-preference EV/CV belongs in Chapter 2. Revealed-preference welfare bounds
belong here.

### Chapter 4. Choice Without Budget Geometry

**Question:** Which parts of the benchmark are properties of choice itself,
rather than of linear budgets?

1. Alternatives, menus, and choice correspondences
2. Exact and weak rationalization
3. Preference relations, ties, greatest elements, and maximal elements
4. Finite and continuous utility representation: a representation ladder
5. Direct and indirect revealed choice
6. Consistency axioms on general menu domains
7. Budget demand as the specialization `x(p,w)=c(B(p,w))`
8. Roadmap to risk, stochastic choice, and attention
9. Problems

This chapter should not restate Afriat. It should include one translation table
between abstract-choice and budget-demand notation and link backward to the
single full finite-budget theorem.

## Part II. Risk, Stochastic Choice, and Attention

The organizing distinction is where probability enters:

| Model | What is random? | Observable object |
|---|---|---|
| Choice under risk | consequences | deterministic preference over lotteries |
| Stochastic choice | tastes, occasions, or decision errors | `P(a | A)` across menus |
| Rational inattention | information and the induced action | conditional action rule `P(a | state)` |

### Chapter 5. Expected Utility and Risk

**Question:** When can preferences over random consequences be represented by
expected utility, and what does the model imply?

1. Monetary outcomes, lotteries, mixtures, and preferences
2. Independence, mixture continuity, and the finite expected-utility theorem
3. Positive-affine uniqueness and its meaning
4. The empirical content of independence: Allais
5. Risk aversion, certainty equivalents, risk premia, and Arrow--Pratt measures
6. First-order stochastic dominance
7. Portfolio choice
8. Revealed expected utility and laboratory measurement
9. Problems

Editorial changes:

- Merge the current primitives and model sections.
- Put Allais immediately after independence and representation.
- Absorb the isolated recoverability section into the representation result.
- State one stochastic-dominance theorem and make the finite result a
  corollary.
- Move the sigma-algebra primer and infinite-lottery representation theorem to
  a technical appendix or advanced linked note.
- Introduce a monetary interval containing lottery support before defining
  means and certainty equivalents; do not patch the domain only when risk
  aversion appears.
- Combine the revealed-EU test, passing-rate evidence, and Holt--Laury material
  into one clearly marked empirical capstone.

### Chapter 6. Stochastic Choice and Random Utility

**Question:** When can probabilistic choice be represented by a distribution
over utility-maximizing types?

1. The stochastic-choice primitive `P(a | A)`
2. Interpretations: stable heterogeneity, preference shocks, and decision error
3. A fixed alternative universe and a menu-independent distribution over types
4. Finite random-utility rationalizability: `P = M lambda`
5. Existence versus identification of the type distribution
6. Additive random utility with attributes
7. Logit as a special case; IIA and red-bus/blue-bus
8. Random expected utility
9. Expected maximum utility and the Williams--Daly--Zachary envelope result
10. Problems

The generic model must precede logit. Let `mathcal X` be the fixed universe,
let menus satisfy `A subseteq mathcal X`, and restrict one random preference or
utility vector to each menu. The current use of `A` as both universe and menu is
not adequate for cross-menu rationalizability.

The finite feasibility statement `P=M lambda` should be elevated from prose to
a central theorem and must distinguish existence from uniqueness of `lambda`.
The random-expected-utility characterization must either be stated precisely
with its definitions and technical counterpart or reduced to an explicit
reading note.

### Chapter 7. Limited Attention and Costly Information

**Question:** How does behavior change when the agent misperceives the
environment or chooses costly information before acting?

1. Benchmark and taxonomy of departures
2. Reduced-form inattention: perceived prices and sparse max
3. Which demand and welfare conclusions can fail
4. Bayesian decision problems and the value of information
5. Shannon rational inattention
6. Binary-state/action example and generalized-logit connection
7. Gaussian costly precision as a special example
8. Hiring and attention discrimination
9. Problems

Sparse max, exogenous noisy perception, costly Gaussian precision, and Shannon
rational inattention have different primitives. They should be compared, not
presented as interchangeable labels. Reserve “rational inattention” for an
agent who chooses an information structure or conditional action rule, for
example

\[
\max_{P(a\mid\theta)}
\mathbb E[u(a,\theta)]-\kappa I(\Theta;A).
\]

The current Gaussian posterior calculation should appear once. The Shannon
model currently found only in a problem should be defined in the main text.

Aggregate demand should follow this complete individual-choice sequence; it
should not separate expected utility from random utility.

## Content relocation ledger

| Current material | Destination | Disposition |
|---|---|---|
| Commodity and budget environment | Ch. 1 | retain once |
| Primitive demand-function opening | Ch. 3 observables | move after generated demand |
| Demand correspondence, UMP, Berge, UMP KKT | Ch. 1 | consolidate |
| Utility representation results | Ch. 4 + technical record | representation ladder; forward pointer in Ch. 1 |
| Walras and HD0 | Ch. 1 | derive from the model under stated assumptions |
| Indirect utility, EMP, Hicksian demand, Roy, Shephard | Ch. 2 | one duality sequence |
| Slutsky material now split between Chs. 1 and 3 | Ch. 2, with observational contrast in Ch. 3 | define once |
| WARP to compensated demand | Ch. 3 | retain proof |
| Integrability, GARP, Afriat, SARP | Ch. 3 | retain; Afriat is sole full finite-data theorem |
| Varian support, welfare bounds, CCEI, measurement error | Ch. 3 | organize as recovery/diagnostics |
| Abstract menus, rationalization, WGARP | Ch. 4 | move intact, then tighten |
| Duplicate abstract finite-data theorem | Ch. 4 preview box | remove as theorem; link to Afriat |
| Sparse max and attention | Ch. 7 | move after probability/stochastic choice |
| Finite expected utility and risk attitudes | Ch. 5 | reorder around representation |
| Infinite expected utility and general-distribution details | technical appendix | preserve full mathematics |
| Generic random utility, random EU, logit, WDZ | Ch. 6 | generic before parametric |
| Aggregate demand | after Ch. 7 | preserve intact initially |

No valid substantive theorem is to be deleted. The two deliberate deduplications are
the invalid/non-substantive early weak-rationalization claim and the duplicate
finite/general FOSD statements. Their valid mathematical content remains in
the single full results.

## Reader theorem and full theorem policy

Use the already specified two-level theorem architecture:

1. A linked reader theorem in the chapter states the economic environment,
   minimum memorable assumptions, conclusion, and interpretation.
2. Its full counterpart records the exact domain, quantifiers, hypotheses,
   proof or precise proof delegation, boundary cases, and Lean status.

The marker means “compressed reader statement,” not “approximately true” and
not “Lean verified.” Formal-verification status remains a separate field. Use
stable semantic identifiers so chapter movement does not change a theorem's
identity.

Flagship results in this block are:

- demand existence and continuity;
- consumer duality, Roy, Shephard, and Slutsky;
- Afriat's theorem;
- rational choice implies the appropriate weak axiom;
- finite expected-utility representation;
- finite random-utility rationalizability;
- Williams--Daly--Zachary;
- a canonical finite rational-inattention result once its exact statement is
  frozen.

## Safe migration protocol

### Phase 0: Freeze and inventory

1. Preserve the current public release and PDF as the comparison baseline.
2. Work on an isolated `codex/consumer-restructure` branch/worktree.
3. Assign stable semantic IDs to every definition, theorem, proof, example,
   figure, and problem in the affected chapters.
4. Record current location, dependencies, destination, and merge status.
5. Add an old-to-new alias table for chapter-number-based theorem IDs and
   displayed problem numbers.

### Phase 1: Build the new shell

1. Create the new part/chapter/section headings in LyX.
2. Add one-paragraph chapter questions and dependency roadmaps.
3. Do not rewrite mathematical blocks yet.

### Phase 2: Move intact blocks

1. Move LyX blocks before editing them.
2. Compile after each chapter move.
3. Reconcile theorem, definition, proof, figure, example, and problem counts.
4. Compare normalized formal-statement text against the frozen registry.

### Phase 3: Consolidate and rewrite

1. Delete only registry-confirmed duplicate definitions or preview statements.
2. Replace repeated summaries with one implication table or dependency diagram.
3. Rewrite transitions, assumption scopes, and chapter openings.
4. Convert lecture-note fragments into examples, remarks, or case studies.
5. Ensure each formal assumption precedes its first use.

### Phase 4: Rebuild the modern extensions

1. Make expected utility a finite, directed core and move the intact
   infinite-space material to the technical layer.
2. Rebuild stochastic choice around a fixed universe and cross-menu data.
3. Separate reduced-form limited attention, costly precision, and Shannon
   rational inattention.
4. Add only the minimum new theorem needed to make each chapter conceptually
   complete.

### Phase 5: Regenerate and verify

Update and check:

- notation-first anchors and the glossary;
- chapter and theorem cross-references;
- `BOOK_MAP.md` and the theorem inventory;
- theorem-pair and Lean-coverage ledgers;
- public problem-bank placement and stable aliases;
- figures, bibliography, and PDF bookmarks;
- complete PDF and Lean release checks.

## Acceptance criteria

The restructuring is complete only if all of the following hold.

- Every old content ID has exactly one destination or an explicit merge record.
- Every preserved formal statement is textually reconciled after movement.
- No proof, figure, example, or problem disappears silently.
- Every theorem's assumptions and defined symbols precede its use.
- Every chapter answers one economic question and has roughly 6--8 substantive
  sections, apart from deliberately marked technical notes.
- Demand is introduced first as the solution of the benchmark model; its later
  treatment as observable data is explicitly announced as a change of lens.
- Risk, stochastic choice, and attention identify different sources of
  randomness and different welfare interpretations.
- No hard-coded chapter number is the sole identity of a theorem or problem.
- Notation validation, glossary links, problem synchronization, PDF preflight,
  theorem-pair checks, and Lean builds all pass.
- A human side-by-side review confirms the conceptual flow and the visual
  integrity of every moved chapter.

## Style and balance rules

Each chapter should open with four compact items:

1. economic question;
2. primitives and observables;
3. benchmark model or representation;
4. principal implication.

Each chapter should end with:

1. one synthesis table;
2. one “what is testable?” paragraph;
3. a problem set keyed to the chapter's dependency order.

Use running examples instead of repeated mini-introductions:

- Cobb--Douglas across utility maximization, duality, Slutsky, and recovery;
- one finite budget dataset across WARP, GARP, Afriat, and CCEI;
- one two-prize lottery across expected utility, Allais, and risk premia;
- red-bus/blue-bus only after the general random-utility model;
- one binary state/action problem across information value and rational
  inattention.

The governing editorial rule is: **move before rewriting, define once, state
each theorem once, and explain every later appearance as a new question rather
than a repeated introduction.**
