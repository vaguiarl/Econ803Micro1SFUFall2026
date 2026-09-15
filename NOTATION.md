# Notation standard

This ledger is the house style for the Fall 2026 notes. Chapter-specific departures must be introduced explicitly where they occur.

| Object | Canonical notation | Convention |
|---|---|---|
| Number and index of commodities | $L$ and $\ell$ | $\ell=1,\ldots,L$; avoid using lowercase $l$ when it can be read as 1. |
| Commodity space | $X\subseteq\mathbb R_+^L$ | Bundles are column vectors. |
| Consumers | $i=1,\ldots,I$ | $I$ is reserved for the number of consumers outside explicitly local examples. |
| Firms | $j=1,\ldots,J$ | Production sets are $Y_j$. |
| Consumption / production / endowment | $x$, $y$, $\omega$ | Use superscript $i$ or subscript $i$ consistently within a chapter, not interchangeably. |
| Prices / wealth | $p$, $w$ | $p\in\mathbb R_{++}^L$ and $w>0$ in consumer theory. “Income” is used only when the economic source of wealth matters. |
| Budget set | $B(p,w)=\{x\in X:p\cdot x\le w\}$ | Use a colon for “such that.” |
| Marshallian / Hicksian demand | $x(p,w)$ / $h(p,\bar u)$ | A correspondence is declared set-valued; a function is declared single-valued. |
| Indirect utility / expenditure | $v(p,w)$ / $e(p,\bar u)$ | Reserve $u$ for direct utility. |
| Preference / strict preference / indifference | $\succeq$, $\succ$, $\sim$ | For a generic relation $R$, its symmetric and asymmetric parts are $I_R$ and $P_R$. |
| Direct / indirect revealed preference | $R^D$, $R$ | $R$ is the reflexive-transitive closure of the direct relation; attach strictness to the affordability comparison, not to reachability. |
| Inner product | $a\cdot b$ | Do not use a prime to mean an inner product. |
| Transpose | $a^\top$ | A prime denotes an alternative object: $a'$, $a''$. |
| Jacobian / gradient | $D_p x$ / $\nabla u$ | Gradients are column vectors. Outer products use $ab^\top$. |
| Observations | $\mathcal O=\{(p^t,x^t)\}_{t=1}^T$ | $t,s$ index observations and $T$ is sample size. Reserve $i,j$ for agents and firms. |
| Strict positivity | $x\gg0$ or $x\in\mathbb R_{++}^L$ | State the convention before first use in each major part. |
| Sets / cardinality / power set | $A,B$ / $|A|$ / $2^X$ | Uppercase Roman letters denote sets unless a chapter announces an economic aggregate. |
| Choice correspondence | $c(A)\subseteq A$ | Use $c:\mathcal A\rightrightarrows X$ when choice may be multivalued, where $\mathcal A$ is the family of feasible sets. |
| Aggregate demand / excess demand | $x(p,w)$ / $z(p)$ | Define agent aggregation before suppressing wealth or endowment arguments. |
| Probability / expectation | $\Pr$ / $\mathbb E$ | State the probability space for infinite models; finite lottery sums need no measure-theoretic shorthand. |
| Equality by definition | $:=$ | Use $=$ for a claimed identity and $:=$ when introducing notation. |

## Known local exceptions

- In choice under uncertainty, $p$ denotes a lottery rather than a price vector. The chapter announces this change at the start.
- In matching, $M$ and $W$ denote the two sides of the market, and lowercase $m,w$ denote agents. This is local to that chapter.
- In computable general equilibrium, capitalized variable names follow the underlying social-accounting model and are defined locally.

## Normalizations completed in the first pass

- Scalar products are written with $\cdot$.
- Transposes are written with $\top$.
- Stars use proper superscripts, such as $p^*$ and $w^*$; a star always denotes an optimizer or equilibrium, not a transpose.
- “Local nonsatiation” and “locally nonsatiated” use consistent spelling.
- The generic equivalence relation is $E$; the symmetric part of $R$ is $I_R$, avoiding a collision with the number of consumers $I$.
- Observation indices use $s,t=1,\ldots,T$ in the revealed-preference chapters.

## Typographic rules for formal statements

- Introduce every symbol before it appears in a theorem statement.
- Put domains on maps: write $f:X\to Y$ or $F:X\rightrightarrows Y$ before using them.
- Use “if and only if” only for a genuine biconditional and split its proof into the two directions.
- Distinguish “maximal” from “greatest,” “minimal” from “least,” and “affine” from “linear.”
- Do not change an index family, transpose convention, or strict-inequality convention inside a proof.
