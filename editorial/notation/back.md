# Back-third notation audit

## Scope and method

This audit covers the Theory of the Firm through the end of the Order Theory
appendix in Microeconomics_1_notes_by_Victor_Aguiar.lyx (source lines
8998--13457). The inspected LyX SHA-256 is
4042efb9bd579196640fcd36e049b778377eb46e4459298d8a719574e3e1cc76.
Line numbers are evidence for this source snapshot; the proposed semantic
anchors, rather than line numbers, should be the durable identifiers.

The machine-readable inventory is back.tsv. It records 192 substantive
symbols, operators, sets, functions, and persistent indexing conventions.
Variables bound only inside one display were excluded. Exercise-specific model
objects were retained when they persist across a whole problem. In the
defined_before_use column, “yes” means that prose or a defining display
introduces the object at or before its first substantive occurrence; “no”
includes late, implicit, conventional, or missing definitions.

Status meanings:

- OK: explicit, stable use.
- LOCAL_OK: safely confined to one worked example or problem.
- STANDARD: conventional notation that would still benefit from one global convention.
- OVERLOADED: the glyph is defined, but has materially different types or meanings elsewhere.
- CONFLICT or INCONSISTENT: nearby uses can be misread as the same object.
- LATE_DEFINED, UNDEFINED, or UNDERDEFINED: the declaration is late, absent, or incomplete.
- AMBIGUOUS or NOTATION_DRIFT: the intended meaning is recoverable but the convention changes.

## Critical findings

1. **The Pareto definition has an unbound strict-improver index.** At line
   10002 the text says $x_j'\succ_jx_j$ after quantifying the weak comparison
   with $i$ and saying “for at least one consumer.” Replace this by an explicit
   existential statement, $\exists i\in\{1,2\}$ such that
   $x_i'\succ_i x_i$. Anchor: not:pareto-strict-improver.

2. **Supply alternates between a set and a vector.** Line 9115 defines
   $y(p)$ as an argmax correspondence, line 9132 writes
   $\nabla\pi(p)=y(p)$ as though it were a vector, and line 9150 returns to
   membership notation. Line 9255 similarly displays $y_Y(p)=\sum_jy_j(p)$
   before prose explains that this is equality of attainable supply sets.
   Use $\mathcal Y(p)$ for the correspondence and $y(p)$ only for a declared
   singleton selection. Anchors: not:supply-correspondence and
   not:aggregate-supply.

3. **Two optimization blocks use missing primitives.** The one-consumer model
   introduces neither $X$ nor $u$ before maximizing over them at line 10069.
   The private-ownership section introduces preferences $\succeq_i$ but then
   maximizes an unintroduced representation $u_i$ at line 10153. State the
   domain and representation assumptions, or formulate choice directly using
   the preference relation. Anchors: not:one-consumer-primitives and
   not:ge-utility-representation.

4. **Sequential Trade never declares its consumer population.** The allocation
   at line 11306 already contains $x_I^*$, but the chapter only says
   “consumer $i$.” Declare $\mathcal I=\{1,\dots,I\}$ before the contingent
   endowment. Anchor: not:sequential-consumers.

5. **The CGE closure is not yet symbol-complete.** Aggregate labor $N$ is
   declared at line 11917, but the CES technology uses undeclared $N_j$ at
   line 11928. Household demand changes from $Q_{h,j}^D$ at line 11986 to
   $x_{hj}$ at line 12015. Household income $Y_h$, households $h$, world
   prices $P_j^W$, and the exchange rate are used before their declarations;
   $P$ is never defined; and the resource-balance symbols at line 12022 are
   mapped only by word order. This is the largest notation barrier to an
   independently reproducible model. The canonical anchors are the
   not:cge-* rows in the TSV.

6. **The order appendix uses the diagonal before defining it.** The example at
   line 12888 uses $\Delta_S$; the first definition of a diagonal relation is
   $\Delta_X$ at line 13011. Move the generic definition earlier. Problem A.2
   also changes the canonical $I_R$ to bare $I$ at line 13299 and then writes
   $X/I$. Anchors: not:diagonal-relation and
   not:problem-a2-indifference.

## Major findings

- **Index order changes across chapters.** The Edgeworth section uses
  $\omega_{\ell i}$ and $x_{\ell i}$ (lines 9934 and 9972), while Sequential
  Trade uses $\omega_{is}$ and $x_{is}$ (lines 11293 and 11297). Adopt
  entity-first indexing: $x_{i\ell}$ for consumer-good and $x_{is\ell}$ when
  a state coordinate is needed.

- **The same short glyphs carry incompatible types.** The most damaging are:
  $z$ for physical inputs, a numeraire input, scalar and vector excess demand,
  labor, and asset portfolios; $q$ for output, a supporting commodity price,
  and asset prices; $w/W$ for input prices, wage, wealth/income, and a matching
  side; $R$ for an asset-payoff matrix and a binary relation; $M$ for number of
  outputs, attention, men, and imports; $S$ for a coalition, state count, and
  feasible subset; $\Delta$ for the price simplex and diagonal relation; and
  $I$ for the consumer count, identity matrix, and indifference. The TSV
  supplies typed replacements and distinct anchors for every occurrence.

- **Ownership and endowment symbols arrive after they are needed.**
  $\theta_{ij}$ first occurs inside the budget at line 9554 and is explained
  only at line 9560. The numeraire endowment $\omega_{mi}$ at line 9672 is
  never defined. Move both declarations before the consumer problem.

- **The inattention model is not type-stable.** $M_i$ at line 10244 is called
  an attention parameter without admissible domain, sign, or rank conditions;
  $D_i(p,M_i)$ then reuses the ordinary-demand symbol with a different
  signature. Use $D_i^A(p;M_i)$ versus $D_i^W(p,m)$ and state exactly what
  $M_i$ acts on.

- **Core conventions change without a named mathematical object.** The main
  definition at line 10739 requires every coalition member to be strictly
  better off. Problem 11.4 at line 10918 uses all weakly better and one
  strictly better and calls the result the strong core. Both are legitimate,
  but they should be denoted separately, for example
  $\operatorname{Core}^{\mathrm{strict}}$ and
  $\operatorname{Core}^{\mathrm{strong}}$.

- **Several multipliers share $\lambda$ or $\mu$.** The cost KKT multiplier,
  price-scale factor, planner multiplier, Pareto-support multipliers,
  attention multipliers, Afriat multipliers, and the matching map are
  recoverable only from context. Use semantic superscripts/subscripts in the
  full theorem statements even if prose later suppresses them.

- **Relation composition needs an orientation convention.** Line 12990 writes
  $R^{n+1}=R^n\circ R$, but authors use opposite orders for relational
  composition. The glossary should give the quantified definition before
  defining powers.

- **Matching notation needs a typed signature.** At line 11647, $\mu$ is
  described verbally but its domain, cross-side restriction, and unmatched
  convention are not stated formally; $\succ_m,\succ_w$ first appear at line
  11662 without a symbolic preference-domain declaration. The TSV proposes a
  complete involution signature.

## Minor findings

- State once that $\leq$ and $\geq$ on vectors are componentwise, that
  $a\gg0$ means coordinatewise strict positivity, and that
  $\mathbf1=(1,\dots,1)$. These are standard but recurrent.

- Standardize derivative typography: $\partial_kF$ for scalar partials,
  $\nabla_pg$ for gradients, $D_pg$ for Jacobians, and $D_p^2g$ for Hessians.
  Current subscripts also serve as agents, goods, states, and derivatives.

- Preserve uppercase/lowercase discipline: uppercase for correspondences or
  sets ($D_i$, $Z$, $\mathcal Y$), lowercase for declared selections or
  functions ($x_i$, $z$, $y$).

- Problem-local symbols are generally well scoped. Their proposed anchors use
  a problem namespace so they can be linked without entering the global
  notation table.

## Hyperlink strategy

1. The current LyX source defines the LyX-resident formula macros
   $\backslash$notationfirst and $\backslash$notationdef. Pass the semantic key
   in the final TSV column to those two macros at the first use and canonical
   definition. Do not encode chapter numbers or line numbers in hyperlink IDs.

2. Require exactly one definition target for every semantic key. A second
   meaning of the same visible glyph receives a distinct qualified key, such
   as the separate output-price and asset-price entries for $q$.

3. Add one alphabetical notation glossary whose entries link back to the
   canonical definitions. Show glyph, type/domain, definition, and scope.
   Problem-local entries can live in a compact problem-notation subsection.

4. Link the first substantive use in each new scope and every deliberate type
   change. Repeated routine uses in the same section should not all be linked.
   For prose-only definitions, a native LyX Label/Cross-reference pair remains
   preferable to raw ERT.

5. Validate both PDF and HTML targets: every first-use target must resolve to a
   definition and every definition must link back. Keep back.tsv as an
   editorial audit and validation input only. The LyX manuscript remains
   authoritative; checks may report missing or duplicate anchors but must not
   rewrite mathematical content.

## Count summary

| Measure | Count |
|---|---:|
| Inventory entries | 192 |
| Explicitly defined at or before first use | 141 |
| Not explicitly defined before first use | 51 |
| OK | 65 |
| Local exercise/example notation | 18 |
| Conventional but unstated | 15 |
| Overloaded | 38 |
| Direct conflicts | 12 |
| Inconsistent | 7 |
| Late-defined | 10 |
| Undefined | 7 |
| Underdefined | 11 |
| Ambiguous | 5 |
| Notation drift | 4 |

Entries by chapter: Theory of the Firm 37; Competitive Markets and Partial
Equilibrium 28; General Equilibrium Theory 25; Positive Theory of Equilibrium
13; Testable Restrictions on the Equilibrium Manifold 10; Sequential Trade
17; Matching 6; Computable General Equilibrium 30; Order Theory 26.
