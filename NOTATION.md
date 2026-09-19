# House notation standard

This is the authoritative house style for notation in the Fall 2026 notes. The
LyX manuscript remains authoritative for mathematical content; this file
governs how that content is notated. The machine-readable
[glossary](editorial/notation/glossary.tsv) supplies the registered symbol,
semantic ID, definition, and scope. A disagreement between this standard, the
glossary, and the manuscript is an editorial defect, not an invitation to pick
whichever form is convenient.

The [notation audit](NOTATION_AUDIT.md) records the evidence and unresolved
manuscript risks behind these rules. The regional audit files are diagnostic;
they do not override this standard.

## Global conventions

| Object | Canonical notation | Rule |
|---|---|---|
| Commodities | $L$; $\ell,k\in\{1,\ldots,L\}$ | Use $\ell,k$ only for commodity coordinates; never use lowercase $l$. |
| Consumers and firms | $i=1,\ldots,I$; $j=1,\ldots,J$ | A chapter may use $j$ for a discrete alternative only after declaring that local scope. |
| Observations and states | $s,t=1,\ldots,T$; state $s\in\mathcal S$ | Observation labels are superscripts, as in $(p^t,x^t)$; entity labels come first in arrays, as in $x_{i\ell}$ and $x_{is\ell}$. |
| Sets | $X,Y,A,B$ | Uppercase Roman letters denote sets unless a typed local aggregate is declared. Use $\lvert A\rvert$, $2^X$, and $A\setminus B$. |
| Vectors | $x,y,p,\omega$ | Vectors are columns. Use $a\cdot b$, $a^\top$, and $ab^\top$ for an inner product, transpose, and outer product. |
| Alternatives | $a',a''$ | A prime always marks another object of the same type. It never means transpose. |
| Solutions | $x^*,p^*$ | A star marks an optimizer, selected solution, or equilibrium; it never marks a second observation. |
| Definitions | $:=$ | Use $:=$ to introduce notation and $=$ for an asserted equality. |
| Vector order | $a\leq b$, $a\geq b$, $a\gg0$ | Inequalities are componentwise; $a\gg0$ means every coordinate is strictly positive. |
| Derivatives | $\partial_k f$, $\nabla_z f$, $D_z f$, $D_z^2f$ | These denote a scalar partial, column gradient, Jacobian, and Hessian, respectively. |
| Optimization | $\arg\max$, $\arg\min$ | These are sets. Identify a singleton selection before treating one as a function value. |
| Probability | $(\Omega,\mathcal F,\mathbb P)$; $\Pr$, $\mathbb E$ | Declare the probability space for an infinite or random-utility model. The finite-lottery model may use explicit sums. |
| Logarithm | $\log$ | $\log$ is natural; information quantities are measured in nats unless another base and unit are stated. |

Every persistent symbol must be typed before its first substantive use. A map
gets its domain and codomain, a relation gets its ground set, a random object
gets its probability space, and an index gets its range. Symbols bound only in
one display need no glossary entry.

## Choice, demand, and revealed preference

| Object | Canonical notation | Rule |
|---|---|---|
| Feasible or consumption set | $X$, normally $X\subseteq\mathbb R_+^L$ | Announce a broader abstract-choice meaning at the chapter boundary. |
| Preferences | $\succeq$, $\succ$, $\sim$ | These are the weak, asymmetric, and symmetric parts. For a generic relation $R$, use $P_R$ and $I_R$. |
| Choice correspondence | $c:\mathcal A\rightrightarrows X$ | $\mathcal A\subseteq2^X\setminus\{\varnothing\}$ and $c(A)\subseteq A$. |
| Prices and wealth | $p\in\mathsf P:=\mathbb R_{++}^L$; $w\in\mathsf W:=\mathbb R_{++}$ | $p$ is a commodity-price vector and $w$ is scalar wealth. |
| Budget set | $B(p,w):=\{x\in X:p\cdot x\leq w\}$ | Use a colon inside set-builder notation. |
| Marshallian and Hicksian demand | $x(p,w)$; $h(p,\bar u)$ | Treat each as a correspondence unless uniqueness has been established. |
| Utility, indirect utility, expenditure | $u$; $v(p,w)$; $e(p,\bar u)$ | Reserve $u$ for direct or Bernoulli utility and $v$ for indirect utility. |
| Slutsky matrix | $S(p,w):=D_px(p,w)+D_wx(p,w)x(p,w)^\top$ | Its entries are $[S(p,w)]_{\ell k}$, never $S_{ij}$. |
| Dataset | $\mathbb T:=\{1,\ldots,T\}$; $\mathcal O:=\{(p^t,x^t)\}_{t\in\mathbb T}$ | Use $s,t$ for observations and $T+1$ for an appended observation. |
| Budget revealed preference | $\succeq^{R,D}$, $\succ^{R,D}$, $\succeq^R$ | These are direct weak, direct strict, and the reflexive-transitive revealed relation. The compositional superscripts follow Aguiar--Hjertstrand--Serrano--Evren: $R$ means revealed and $D$ adds direct. |
| Abstract revealed choice | $\succeq^C$, $\succ^C$, $\succeq^{C*}$ | These menu-based relations are deliberately distinct from affordability-based revealed preference. |
| Varian support | $\mathcal S_{\mathcal O}(p,w)$ | The dataset qualifier distinguishes it from the Slutsky matrix and other sets. |
| Aggregate demand | $x^A(p,\mathbf w)$ | Define $\mathbf w$ and its aggregation to total wealth $W$ before suppressing arguments. |

The notation $x(p,w)$ is set-valued by default even though it is lowercase. A
formula that differentiates it must first impose uniqueness and the required
regularity, thereby identifying the unique selection being differentiated.

## Uncertainty and discrete choice

| Object | Canonical notation | Rule |
|---|---|---|
| Prizes and lotteries | $Z$; $\mu,\nu,\eta\in\Delta(Z)$ | Never use $p$ for a lottery. For general outcome spaces, declare the measurable structure explicitly. |
| Degenerate lottery and expected utility | $\delta_z$; $U(\mu)$ | Keep the Bernoulli index as $u(z)$. |
| Lottery CDF and FOSD | $F_\mu$; $\succeq^{\mathrm{FOSD}}$ | Define FOSD on an ordered outcome space and distinguish weak dominance from a strict comparison. |
| Certainty equivalent and premiums | $\operatorname{CE}(\mu;u)$, $\operatorname{RP}(\mu;u)$, $\operatorname{PP}(x,\varepsilon;u)$ | Do not recycle $\rho$ or $\pi$ for either premium. |
| State probabilities | $\varpi_s>0$, $\sum_s\varpi_s=1$ | $\pi$ is reserved for profit in firm theory. |
| Latent utility and choice probability | $U^*_{ij}$; $P_{ij}$ | Declare attributes, prices, income, coefficients, shocks, and the menu before the first latent-utility display. |
| Random utility | $\boldsymbol U:\Omega\to\mathbb R^A$; $P_A(a)$ | Interpret $\mathbb R^A$ as the vectors (equivalently, real-valued functions) indexed by the finite menu $A$; use $\mathcal R_A$ for strict order types and keep the menu in the probability notation. |

The symbol $\sim$ may also mean “distributed as” only in the syntactic form
$X\sim\mathcal D$ inside a declared probability model. Between alternatives it
always means indifference.

## Firms, equilibrium, and order theory

| Object | Canonical notation | Rule |
|---|---|---|
| Production | $Y$ or $Y_j$; $y\in Y$ | $y$ is a net-output vector: positive coordinates are outputs and negative coordinates are inputs. |
| Profit and supply | $\pi_Y(p)$; $\mathcal Y_Y(p)$ | Supply is a correspondence. Use $y(p)$ only for a declared singleton selection. |
| Single-output model | output $q$, output price $p_q$, inputs $\boldsymbol z$, input prices $\boldsymbol w$ | The boldface distinctions are mandatory when wealth $w$ or excess demand $z(p)$ is nearby. |
| Cost and factor demand | $C(\boldsymbol w,q)$; $\mathcal Z(\boldsymbol w,q)$ | Lowercase $c$ remains the choice correspondence; $\mathcal C$ is information cost. |
| Ownership and excess demand | $\theta_{ij}$; $z(p)$ | Define ownership shares before they enter a budget. |
| Sequential trade | state space $\mathcal S$, payoff matrix $R$, asset prices $q$, state prices $\psi$ | These meanings are local to the chapter and must be declared together. |
| Matching | sides $M,W$; matching map $\varphi$ | Do not use $\mu$ for the matching map. State its typed involution and unmatched-agent convention. |
| Generic relation | $R\subseteq X\times X$ | Use $R^{-1}$, $I_R$, $P_R$, $R^+$, and $R^*:=\Delta_X\cup R^+$. State the orientation of composition before defining $R^n$. |
| Quotient order | $[x]_E$, $X/E$, $\bar R$ | Never abbreviate the symmetric part to bare $I$. |
| Extremal elements | $\operatorname{Max}(S,R)$, $\operatorname{Great}(S,R)$ | Keep maximal distinct from greatest, and minimal distinct from least. |

## Collision rules

The following resolutions are mandatory even when an older chapter uses a
different glyph.

| Collision | Resolution |
|---|---|
| $I$ for consumers, indifference, and identity | $I$ is the number of consumers; use $\sim$ or $I_R$ for indifference and $I_L$ for the $L\times L$ identity. |
| $S$ for Slutsky, support, states, and feasible subsets | Use $S(p,w)$, $\mathcal S_{\mathcal O}(p,w)$, $\mathcal S$, and appendix-local $S$, respectively. |
| $p$ for prices and lotteries | $p$ is a price vector; use $\mu,\nu,\eta$ for lotteries and $p_q$ for a scalar output price. |
| $\pi$ and $\rho$ for probabilities, premiums, and profit | Use $\varpi_s$ for state probabilities, $P_{ij}$ or $P_A(a)$ for choice probabilities, $\operatorname{RP}$ and $\operatorname{PP}$ for premiums, and $\pi_Y$ for profit. |
| Bare $m$ or $\mu$ for unrelated persistent objects | Use $\mu$ for a lottery, $\mu_p(x)$ for money-metric utility, $a_\ell$ for attention, $\gamma$ for a posterior weight, and $\varphi$ for matching. Qualify multipliers semantically. |
| $C$ for choice, cost, information cost, and constants | Use $c$ for choice, $C(\boldsymbol w,q)$ for production cost, $\mathcal C$ for information cost, and $K_0$ for an integration constant. |
| $\ell$ for an index, labor, or loss | Reserve $\ell$ for commodity coordinates; use $n$ for labor and $\mathscr L$ for a loss function. |
| $y$ or $z$ as both sets and vectors | Use $\mathcal Y_Y$ and $\mathcal Z$ for correspondences, $y$ for a production plan, $\boldsymbol z$ for physical inputs, and $z(p)$ for excess demand. |
| Unqualified multipliers | Attach a problem or role label, such as $\lambda^{\mathrm{UMP}}$ or $\lambda_q$, whenever two multiplier systems occur in the same chapter. |

## Permitted local scope

Matching may use $M$ and $W$ for the two market sides; sequential trade may
use $q$ for asset prices and $R$ for its payoff matrix; the order appendix may
use $R$ for a binary relation; and computable general equilibrium may retain
capitalized social-accounting variables. Within matching, $m\in M$ and $w\in W$
may name individual agents. Problem-local notation may be reused. Each
exception must be declared at the start of its scope, typed before use, and
prevented from leaking into the next section.

## Formal statements and maintenance

- Introduce every persistent symbol before it appears in a theorem or
  optimization problem.
- Put domains on maps: write $f:X\to Y$ or $F:X\rightrightarrows Y$ before
  using the map.
- Use “if and only if” only for a genuine biconditional and prove both
  directions.
- Use “wealth” for $w$ unless the economic source of income matters; spell the
  property “local nonsatiation” and the adjective “locally nonsatiated.”
- Keep “affine” distinct from “linear,” just as maximal is distinct from
  greatest and minimal from least.
- Do not change an index order, transpose convention, or strict-inequality
  convention inside a proof.
- A new persistent object requires a unique row in
  [the glossary](editorial/notation/glossary.tsv). Its stable `id` is semantic,
  not a glyph or line number.
- In LyX, wrap exactly one global first use in
  `\notationfirst{id}{symbol}` and exactly one glossary definition in
  `\notationdef{id}{symbol}`. A deliberate type change gets a new ID; routine
  repetitions do not get links.
- Keep the glossary as the final content chapter before the bibliography and
  run `scripts/validate_notation.py` through the book check before release.
