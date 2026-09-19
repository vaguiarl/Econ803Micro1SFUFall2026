# Middle-third notation audit

**Source of truth:** `notes/Microeconomics_1_notes_by_Victor_Aguiar.lyx`, current
physical lines 6137--9496 (from the `Choice under Uncertainty` chapter heading
through the line before `Competitive Markets and Partial Equilibrium`). Snapshot
SHA-256: `4042efb9bd579196640fcd36e049b778377eb46e4459298d8a719574e3e1cc76`.
The manuscript was read only; this audit does not alter it.

The accompanying `middle.tsv` records each cross-sentence mathematical object
whose notation matters editorially. `first_line` is the physical LyX line on
which the symbol first appears in this slice in the listed semantic role (for
display mathematics, the formula-content line rather than the inset-opening
line). Universal
operators such as `sum`, `int`, `max`, ordinary local indices, and variables
bound only inside a single display are excluded. Exercise parameters are kept
when they define a model or expose a collision with the main text.

## Priority findings

### Critical

1. **The firm chapter changes the type of `p` without notice.** At line 9104,
   `p` is an `L`-vector of net-output prices; at line 9159 it is silently a
   scalar output price in `p f(z)-w dot z`. The same line uses `w` before input
   prices are introduced at line 9179. Use `p_y` for the scalar specialization
   and define the input-price vector before the primal profit problem.
2. **The random-utility probability space is missing.** Line 8633 maps the
   random utility vector from `Omega`, and line 8638 invokes `mathbb P`, but no
   `(Omega,mathcal F,mathbb P)` is declared. Line 8662 likewise uses `Delta(R)`
   without assigning `R` to the strict-order set described in prose.
3. **The probability/choice/profit glyphs are collision-prone.** `pi` denotes a
   probability premium (6650), state probabilities (7323), a monetary risk
   premium in Problem 5.3 (7914), ranking-type masses (8662), and firm profit
   (9109). `rho` denotes the main-text monetary risk premium (6641), a
   menu-specific stochastic choice probability (8638), a stacked vector
   (8657), and an undefined attribute-conditional probability (8799). The
   exercise already contradicts the main chapter's risk-premium convention.
4. **General FOSD is used before it is typed.** The theorem invokes
   `F succeq^{FOSD} G` at line 7039 and gives the inequality only at line 7047,
   without declaring `F,G` to be CDFs. More importantly, `Z` was broadened to
   an arbitrary compact metric space at line 6677, whereas CDF dominance needs
   an ordered outcome space. The paragraph also folds “strict somewhere” into
   the displayed weak relation. Type the domain and separate weak from strict
   FOSD before stating the theorem.
5. **The first discrete-choice equation contains undeclared primitives.** In
   line 8524, `x_j`, `p_j`, `y_i`, `V_j`, and `epsilon_ij` all appear inside
   `U^*_{ij}`. Three are explained only afterward; `p_j` and `y_i` are never
   explicitly named as price and income. Define the tuple of primitives before
   displaying latent utility.
6. **Choice probability notation is not closed under the chapter's own
   transitions.** `P_{ij}`, `rho_A(a)`, stacked `rho`, `rho(a,x)`, and
   `P(j|A)` denote overlapping objects. In particular, line 8799 never defines
   how `rho(a,x)` relates to `rho_A(a)` or where the menu went. Choose one
   master notation, for example `rho_A(a|x)`, and define its special cases.

### Major

- `Z` successively means a finite prize set, a compact metric outcome space,
  and the risky return itself. `Delta(Z)` likewise changes from a finite
  simplex to a space of Borel measures. These extensions can be rigorous, but
  they need visibly typed anchors rather than silent overloading.
- The weak-convergence display introduces `p^n` without declaring a sequence
  and uses `f` before calling it bounded and continuous. The latter glyph later
  becomes the production function, so both objects need typed anchors.
- `phi` is displayed only as `phi(alpha*)` at line 6974 and then evaluated at
  zero. Neither the function on its feasible domain nor `alpha*` as the
  optimizer is declared before the KKT signs.
- The Allais section introduces `N=3` without `N=|Z|`, and uses `u_z` without
  defining `u_z:=u(z)`. The coordinate order of the four lottery vectors should
  be written explicitly.
- State probabilities `pi_s` are positive but are never stated to sum to one.
  The finite-data test introduces `beta_s^t` as bare positive numbers before
  explaining their marginal-utility role.
- The Aggregate Demand chapter uses dimension `L` without declaring the number
  of goods. Its Gorman components `a_i,b,A,B` are all displayed before their
  prose definitions. It also changes `X(p,bold w)` to `X(p,W)` without naming
  the fixed wealth-allocation rule, while Problem 6.3 replaces `X` with `x^A`.
- Within Discrete Choice, `V_j` is mean utility while `V(x)` is expected maximum
  utility; `M` is an incidence matrix immediately before becoming the number of
  outputs in the firm chapter. `beta` in the linear index has no dimension or
  prose definition, and `Pr` changes to `mathbb P` without either operator being
  tied to a declared probability space.
- `q`, `z`, `w`, and `W` are each reused for economically different types:
  lotteries/normalized prices/output; prizes/outside-good quantity/inputs;
  wealth/input prices; and terminal/aggregate wealth. Chapter resets help a
  reader but are insufficient for a linked global glossary.

### Minor

- Define the dot-product shorthand `u dot p` when switching from explicit
  expected-utility sums, and define the strict and indifferent parts of
  `succeq` once.
- State the conventions for `R_{++}^n`, `x >> 0`, componentwise vector order,
  and the all-ones vector. Use `mathbf 1^T pi=1` consistently rather than mixing
  a dot and a transpose.
- Preserve typographic distinctions (`u` versus bold `u`, `U` versus bold `U`,
  `W` versus calligraphic `W`) in prose, PDF bookmarks, alt text, and the index;
  several distinctions disappear when read aloud.

## Hyperlink and glossary strategy

1. Give each canonical object the stable anchor in the TSV's `anchor` column,
   implemented later as a LyX label such as `not:<anchor>` at the authoritative
   definition—not at every occurrence.
2. Link the first substantive use in each chapter to that definition. For a
   deliberately overloaded glyph, link to a typed anchor (`lottery-p`,
   `commodity-price-vector`, `firm-price-vector`) rather than a glyph-only
   entry.
3. The glossary should display four fields: symbol, mathematical type/domain,
   one-sentence definition, and scope. Add backlinks to the chapter/section,
   using the existing chapter labels where available.
4. Do not hyperlink bound summation indices, one-off proof-local symbols, or
   numerical-example labels. A proof-level object reused across paragraphs may
   receive one anchor at its definition; repeated links within one paragraph
   add noise without improving navigation.
5. Generate a collision check from the TSV: duplicate glyphs are allowed only
   when every row has a distinct typed anchor and an explicit scope note.

## Count summary

The inventory contains **150** substantive notation records across **4**
chapters and **30** sections. Of these, **106** are explicitly defined at or
before first use and **44** are not. Editorial status counts are: 41 `ok`, 59
`overload`, 20 `define`, 12 `forward`, 6 `conflict`, 8 `standardize`, and 4
`incomplete`. Anchors are unique, every row has exactly nine TSV fields, and
the records are sorted by current physical first-use line.
