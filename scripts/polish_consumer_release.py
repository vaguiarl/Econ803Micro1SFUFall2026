#!/usr/bin/env python3
"""Apply or verify the mathematical release fixes for Chapters 1--8.

The replacements are intentionally literal.  That makes the script an executable
editorial record: a future source change cannot silently reintroduce one of the
claims corrected for the Fall 2026 public release.
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path


REPO = Path(__file__).resolve().parents[1]
LYX = REPO / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"


REPLACEMENTS: list[tuple[str, str, str]] = [
    (
        "benchmark demand type",
        r"""\[
x(p,w)\in\arg\max_{x\in B(p,w)}u(x).
\]""",
        r"""\[
x^{*}\in x(p,w):=\arg\max_{y\in B(p,w)}u(y).
\]""",
    ),
    (
        "demand correspondence definition",
        r"""x(p,w)\equiv \arg\max_{y\in B(p,w)}u(y).""",
        r"""x(p,w):=\arg\max_{y\in B(p,w)}u(y).""",
    ),
    (
        "budget correspondence upper hemicontinuity",
        r""" If 
\begin_inset Formula $x^{n}\in B(p^{n},w^{n})$
\end_inset
 and 
\begin_inset Formula $x^{n}\rightarrow x$
\end_inset
, then 
\begin_inset Formula $p^{n}\cdot x^{n}\leq w^{n}$
\end_inset
; taking limits gives 
\begin_inset Formula $p\cdot x\leq w$
\end_inset
, so the graph is closed.
""",
        r""" If 
\begin_inset Formula $x^{n}\in B(p^{n},w^{n})$
\end_inset
 and 
\begin_inset Formula $x^{n}\rightarrow x$
\end_inset
, then 
\begin_inset Formula $p^{n}\cdot x^{n}\leq w^{n}$
\end_inset
; taking limits gives 
\begin_inset Formula $p\cdot x\leq w$
\end_inset
, so the graph is closed.
 Moreover, near any 
\begin_inset Formula $(p,w)$
\end_inset
, prices are bounded away from zero and wealth is bounded above; hence the nearby budget sets are uniformly bounded.
 Closed graph plus this local boundedness gives upper hemicontinuity.
""",
    ),
    (
        "definition transition",
        "We need some definitions.",
        "The next definitions separate the assumptions used in the comparative-statics results.",
    ),
    (
        "local nonsatiation wording",
        "If a locally nonsatiated utility function generates the Marshallian demand correspondence, then every demanded bundle exhausts the budget:",
        "If a utility function representing a locally nonsatiated preference relation generates the Marshallian demand correspondence, then every demanded bundle exhausts the budget:",
    ),
    (
        "quasilinearity converse",
        r""" Equivalently, translating both bundles by the same amount of the numeraire does not change their ranking whenever both translated bundles remain feasible.""",
        r""" Such preferences are invariant to a common translation of both bundles in the numeraire whenever the translated bundles remain feasible.
 The converse is not implied by translation invariance alone.
 On a product domain 
\begin_inset Formula $Z\times\mathbb R$
\end_inset
, one sufficient formulation adds strict monotonicity in the numeraire and numeraire solvability: for a fixed 
\begin_inset Formula $z_0\in Z$
\end_inset
 and every 
\begin_inset Formula $z\in Z$
\end_inset
, there is a unique 
\begin_inset Formula $g(z)$
\end_inset
 such that 
\begin_inset Formula $(z,0)\sim(z_0,g(z))$
\end_inset
.
 Translation invariance then gives 
\begin_inset Formula $(z,m)\sim(z_0,g(z)+m)$
\end_inset
, which yields the displayed representation.""",
    ),
    (
        "set-valued indirect utility",
        r"""Alternatively it is the utility evaluated in the Marshallian demand 
\begin_inset Formula $v(p,w)=u(x(p,w))$
\end_inset

.""",
        r"""Every Marshallian maximizer yields this same value: 
\begin_inset Formula $v(p,w)=u(x^{*})$
\end_inset
 for every 
\begin_inset Formula $x^{*}\in x(p,w)$
\end_inset
.""",
    ),
    (
        "Roy unique-demand notation",
        r"""Recall the definition of indirect utility 
\begin_inset Formula $v(p,w)=u(x(p,w))$
\end_inset

.

\end_layout

\begin_layout Standard
Assume the maximizer is unique and the value function is differentiable.""",
        r"""Assume the maximizer is unique, denote it by 
\begin_inset Formula $x(p,w)$
\end_inset
, and assume the value function is differentiable.
 Then 
\begin_inset Formula $v(p,w)=u(x(p,w))$
\end_inset
.""",
    ),
    (
        "indirect utility proof",
        r"""Proof.  Existence, homogeneity, monotonicity, and continuity follow from the compact budget correspondence and Berge's maximum theorem.""",
        r"""Proof.  Homogeneity follows from 
\begin_inset Formula $B(\lambda p,\lambda w)=B(p,w)$
\end_inset
 for every 
\begin_inset Formula $\lambda>0$
\end_inset
.
 If 
\begin_inset Formula $p'\geq p$
\end_inset
 componentwise, then 
\begin_inset Formula $B(p',w)\subseteq B(p,w)$
\end_inset
, so the value is nonincreasing in every price.
 Continuity follows from Berge's maximum theorem and the continuity and compact-valuedness of the budget correspondence.
 To prove strict monotonicity in wealth, let 
\begin_inset Formula $w'>w$
\end_inset
 and choose 
\begin_inset Formula $x^{*}\in x(p,w)$
\end_inset
.
 The bundle 
\begin_inset Formula $x^{*}$
\end_inset
 lies strictly inside 
\begin_inset Formula $B(p,w')$
\end_inset
.
 Local nonsatiation supplies a bundle arbitrarily close to 
\begin_inset Formula $x^{*}$
\end_inset
 that is strictly preferred; choosing it close enough keeps it in 
\begin_inset Formula $B(p,w')$
\end_inset
.
 Hence 
\begin_inset Formula $v(p,w')>v(p,w)$
\end_inset
.""",
    ),
    (
        "summary demand type",
        r"""\begin_inset Formula $x(p,w)\in\arg\max_{y\in B(p,w)}u(y)$
\end_inset
""",
        r"""\begin_inset Formula $x(p,w)=\arg\max_{y\in B(p,w)}u(y)$
\end_inset
""",
    ),
    (
        "duality domain",
        r"""Under continuity and local nonsatiation, at positive prices and feasible utility targets, the demand and value functions satisfy the duality identities

\end_layout

\begin_layout Standard
\begin_inset Formula
\[
\begin{aligned}
h(p,v(p,w))&=x(p,w),\\
x(p,e(p,\overline{u}))&=h(p,\overline{u}),\\
v(p,e(p,\overline{u}))&=\overline{u},\\
e(p,v(p,w))&=w.
\end{aligned}
\]

\end_inset
 The first two equalities are equalities of correspondences; when demand is single-valued, the same notation denotes functions.""",
        r"""Suppose that 
\begin_inset Formula $u$
\end_inset
 is continuous and represents a locally nonsatiated preference relation on 
\begin_inset Formula $X=\mathbb R_+^L$
\end_inset
.
 For 
\begin_inset Formula $p\gg0$
\end_inset
, 
\begin_inset Formula $w>0$
\end_inset
, and every attainable target 
\begin_inset Formula $\overline u\in u(X)$
\end_inset
 with 
\begin_inset Formula $\overline u>u(0)$
\end_inset
, the demand and value functions satisfy

\end_layout

\begin_layout Standard
\begin_inset Formula
\[
\begin{aligned}
h(p,v(p,w))&=x(p,w),\\
x(p,e(p,\overline{u}))&=h(p,\overline{u}),\\
v(p,e(p,\overline{u}))&=\overline{u},\\
e(p,v(p,w))&=w.
\end{aligned}
\]

\end_inset
 The first two equalities are equalities of correspondences; when demand is single-valued, the same notation denotes functions.
 The restriction 
\begin_inset Formula $\overline u>u(0)$
\end_inset
 ensures 
\begin_inset Formula $e(p,\overline u)>0$
\end_inset
, so the Marshallian demand appearing in the second and third identities lies in the declared wealth domain.
 At the boundary target 
\begin_inset Formula $u(0)$
\end_inset
, the identities require an explicit extension of Marshallian demand to zero wealth.""",
    ),
    (
        "CMU compensated law proof",
        r"""Strict increase and asymmetry imply budget exhaustion at every nonempty demand.
 Thus \begin_inset Formula $p'\cdot(x'-x)=0$\end_inset
.
 At the new budget, the old choice \begin_inset Formula $x$\end_inset
 is affordable at equality.
 WGARP therefore rules out \begin_inset Formula $p\cdot x>p\cdot x'$\end_inset
, so \begin_inset Formula $p\cdot(x'-x)\geq0$\end_inset
.
 Subtracting the two expressions gives the result.
 The claim is conditional on both demand sets being nonempty.""",
        r"""First note that strict increase and asymmetry imply budget exhaustion at every nonempty demand.
 If a demanded bundle had slack, a strictly larger feasible bundle 
\begin_inset Formula $z$
\end_inset
 would satisfy 
\begin_inset Formula $r(x,z)\geq0$
\end_inset
 by maximality, while strict increase in the first argument would give 
\begin_inset Formula $r(z,z)>r(x,z)\geq0$
\end_inset
, contradicting asymmetry at 
\begin_inset Formula $(z,z)$
\end_inset
.
 Hence 
\begin_inset Formula $p'\cdot(x'-x)=0$
\end_inset
.
 Suppose, toward a contradiction, that 
\begin_inset Formula $p\cdot x'<p\cdot x$
\end_inset
.
 Then some 
\begin_inset Formula $z>x'$
\end_inset
 remains affordable at the original budget.
 Since 
\begin_inset Formula $x'$
\end_inset
 defeats 
\begin_inset Formula $x$
\end_inset
 at the compensated budget, 
\begin_inset Formula $r(x',x)\geq0$
\end_inset
.
 Strict increase gives 
\begin_inset Formula $r(z,x)>0$
\end_inset
, and asymmetry then gives 
\begin_inset Formula $r(x,z)<0$
\end_inset
, contradicting 
\begin_inset Formula $x\in x_r(p,w)$
\end_inset
.
 Therefore 
\begin_inset Formula $p\cdot(x'-x)\geq0$
\end_inset
, and subtracting this inequality from 
\begin_inset Formula $p'\cdot(x'-x)=0$
\end_inset
 yields the result.
 The claim is conditional on both demand sets being nonempty.""",
    ),
    (
        "SARP roadmap",
        r"""The preceding section used GARP to characterize weak rationalization,
 allowing ties in observed choice.
 This section records the corresponding strict result:
 with single-valued choice and strict concavity,
 SARP replaces GARP and the Afriat inequalities become strict.
 The two results are parallel but answer different rationalizability questions.""",
        r"""The preceding section used GARP to characterize weak rationalization, allowing ties in observed choice.
 SARP is the acyclicity condition associated with strict or unique rationalization.
 The exact equivalence depends on how duplicate observed bundles and strict choice are treated, so this section states the condition without claiming that merely replacing every Afriat inequality by a strict one is sufficient.""",
    ),
    (
        "Varian welfare upper bound",
        r"""Given a finite dataset 
\begin_inset Formula $\mathcal{O}$
\end_inset

, Varian proposes the following upper bound for money-metric utility:
\end_layout

\begin_layout Standard
\begin_inset Formula
\[
m^{+}(p,x)=\min\{p\cdot x^{t}:x^{t}\succeq^{R}x,\ t=1,\ldots,T\}.
\]

\end_inset


\end_layout""",
        r"""For a counterfactual bundle 
\begin_inset Formula $x$
\end_inset
, extend direct revealed preference to the set 
\begin_inset Formula $\{x,x^1,\ldots,x^T\}$
\end_inset
 by declaring
\begin_inset Formula
\[
x^t\succeq^{R,D}_{\mathcal O,x}y
\quad\Longleftrightarrow\quad
p^t\cdot x^t\geq p^t\cdot y,
\qquad y\in\{x,x^1,\ldots,x^T\},
\]
\end_inset
and let 
\begin_inset Formula $\succeq^R_{\mathcal O,x}$
\end_inset
 be its transitive closure.
 The data-dependent upper bound is
\begin_inset Formula
\[
m^{+}_{\mathcal O}(p,x)
=\min\{p\cdot x^{t}:x^{t}\succeq^{R}_{\mathcal O,x}x,\ t=1,\ldots,T\},
\]
\end_inset
when the index set is nonempty, and 
\begin_inset Formula $m^{+}_{\mathcal O}(p,x)=+\infty$
\end_inset
 otherwise.
 If 
\begin_inset Formula $u$
\end_inset
 rationalizes 
\begin_inset Formula $\mathcal O$
\end_inset
, every revealed chain in the extended relation implies 
\begin_inset Formula $u(x^t)\geq u(x)$
\end_inset
.
 Monotonicity of expenditure in its utility target and feasibility of 
\begin_inset Formula $x^t$
\end_inset
 then give
\begin_inset Formula
\[
\mu_p(x)=e(p,u(x))\leq e(p,u(x^t))\leq p\cdot x^t.
\]
\end_inset
Taking the minimum proves 
\begin_inset Formula $\mu_p(x)\leq m^{+}_{\mathcal O}(p,x)$
\end_inset
 whenever the bound is finite.
\end_layout""",
    ),
    (
        "continuous utility proof record",
        r"""This is Debreu's continuous-utility theorem specialized to Euclidean commodity space.
 The substantive topological input is that 
\begin_inset Formula $\mathbb{R}^{L}_{+}$
\end_inset

 is second countable and connected.
 Continuity of the preorder and the gap lemma provide a countable order-dense family of indifference classes.
 Mapping those classes into a countable dense subset of 
\begin_inset Formula $\mathbb{R}$
\end_inset

 and extending across the gaps yields an order-preserving continuous map.
 The result cannot be obtained by taking arbitrary limits of a utility defined only on 
\begin_inset Formula $\mathbb{Q}^{L}$
\end_inset

: such limits need not exist or be independent of the approximating sequence.""",
        r"""Proof record.
 This is Debreu's continuous-utility theorem specialized to the Euclidean orthant; see
\begin_inset CommandInset citation
LatexCommand citep
key "debreu1959"
literal "false"

\end_inset
.
 The orthant is second countable, separable, and connected, and a continuous total preorder on this space satisfies the theorem's topological hypotheses.
 The published proof constructs an order-dense countable family of indifference classes, assigns compatible real values to those classes, and extends the assignment continuously to the whole space.
 We rely on that theorem here rather than reproduce its topological construction.
 An arbitrary limit of a utility defined only on 
\begin_inset Formula $\mathbb{Q}^{L}$
\end_inset
 would not suffice, because existence and independence of the approximating sequence would still have to be proved.""",
    ),
    (
        "FOSD strictness",
        r""" If \begin_inset Formula $F\succeq^{\mathrm{FOSD}}G$\end_inset
,
 then \begin_inset Formula $\int u\,dF\geq\int u\,dG$\end_inset
 for every increasing Bernoulli utility \begin_inset Formula $u$\end_inset
 for which the integrals exist.  Strict dominance together with strict monotonicity yields a strict inequality under the usual support conditions.""",
        r""" If \begin_inset Formula $F\succeq^{\mathrm{FOSD}}G$\end_inset
,
 then \begin_inset Formula $\int u\,dF\geq\int u\,dG$\end_inset
 for every nondecreasing measurable Bernoulli utility \begin_inset Formula $u$\end_inset
 for which both expectations are finite.
 If 
\begin_inset Formula $F\neq G$
\end_inset
 and 
\begin_inset Formula $u$
\end_inset
 is strictly increasing, the inequality is strict.""",
    ),
    (
        "sparse-max equivalence",
        r"""When the full-information demand \begin_inset Formula $x^{\mathrm{FI}}(\widehat p,\widetilde w)$\end_inset
 is single-valued and locally invertible in wealth, the same sparse-max bundle can be written as \begin_inset Formula $x^{\mathrm{SM}}(p,\widehat p,w)=x^{\mathrm{FI}}(\widehat p,\widetilde w)$\end_inset
 for the unique \begin_inset Formula $\widetilde w$\end_inset
 satisfying \begin_inset Formula $p\cdot x^{\mathrm{FI}}(\widehat p,\widetilde w)=w$\end_inset
.
 This is a change of representation, not an assertion that the consumer faces \begin_inset Formula $\widehat p$\end_inset
 in the market.""",
        r"""Suppose instead that 
\begin_inset Formula $u$
\end_inset
 is strictly concave and differentiable and that the relevant solutions are interior.
 For a sparse-max tangency bundle 
\begin_inset Formula $x$
\end_inset
, set 
\begin_inset Formula $\widetilde w=\widehat p\cdot x$
\end_inset
.
 The perceived-price first-order condition is then sufficient for the unique global optimum, so
\begin_inset Formula
\[
x=x^{\mathrm{FI}}(\widehat p,\widetilde w).
\]
\end_inset
Conversely, any full-information bundle 
\begin_inset Formula $x^{\mathrm{FI}}(\widehat p,\widetilde w)$
\end_inset
 satisfying 
\begin_inset Formula $p\cdot x^{\mathrm{FI}}(\widehat p,\widetilde w)=w$
\end_inset
 obeys the sparse-max rule.
 If the map 
\begin_inset Formula $\widetilde w\mapsto p\cdot x^{\mathrm{FI}}(\widehat p,\widetilde w)$
\end_inset
 is continuous, strictly increasing, and has 
\begin_inset Formula $w$
\end_inset
 in its range, this 
\begin_inset Formula $\widetilde w$
\end_inset
 is unique.
 This is a change of representation, not an assertion that the consumer faces 
\begin_inset Formula $\widehat p$
\end_inset
 in the market.""",
    ),
    (
        "Shannon zero mass convention",
        r"""with the convention \begin_inset Formula $0\log 0=0$\end_inset
.""",
        r"""The sum may equivalently be taken only over actions with 
\begin_inset Formula $q(a)>0$
\end_inset
.
 A term with 
\begin_inset Formula $q(a\mid s)=0<q(a)$
\end_inset
 is defined as zero; because the prior has full support, 
\begin_inset Formula $q(a)=0$
\end_inset
 implies 
\begin_inset Formula $q(a\mid s)=0$
\end_inset
 for every state, so that inactive action contributes zero.""",
    ),
    (
        "Gaussian precision closed domain",
        r"""\max_{0\leq \gamma<1}-\frac12(1-\gamma)\sigma_\theta^{2}-\mathcal C(\gamma).""",
        r"""\max_{0\leq \gamma\leq1}-\frac12(1-\gamma)\sigma_\theta^{2}-\mathcal C(\gamma).""",
    ),
    (
        "Gaussian quadratic optimum",
        r"""For example, with \begin_inset Formula $\mathcal C(\gamma)=\kappa\gamma^{2}/2$\end_inset
,
 an interior optimum satisfies \begin_inset Formula $\gamma=\sigma_\theta^{2}/(2\kappa)$\end_inset
 and is truncated to \begin_inset Formula $[0,1)$\end_inset
 when the unconstrained value lies outside that interval.  The comparative statics depend on the cost specification.""",
        r"""For example, with \begin_inset Formula $\mathcal C(\gamma)=\kappa\gamma^{2}/2$\end_inset
,
 the solution is 
\begin_inset Formula $\gamma^{*}=\min\{1,\sigma_\theta^{2}/(2\kappa)\}$
\end_inset
.
 Here 
\begin_inset Formula $\gamma=1$
\end_inset
 denotes the limiting noiseless signal 
\begin_inset Formula $\sigma_{\varepsilon}^{2}=0$
\end_inset
.
 Cost specifications that diverge as 
\begin_inset Formula $\gamma\uparrow1$
\end_inset
, such as the logarithmic specification below, instead guarantee an interior precision.
 The comparative statics therefore depend on the cost specification.""",
    ),
    (
        "Gaussian illustration title",
        "A Gaussian Signal Example",
        "A Gaussian Precision-Choice Illustration",
    ),
    (
        "group threshold title",
        "Discrimination with Rational Inattention",
        "Group Thresholds under Noisy Signals",
    ),
    (
        "group signal comparison",
        r"""If both group means are negative, the lower-mean group has the higher threshold and is hired less often under a common signal distribution.  If both means are positive, the same threshold formula applies, but group-specific rejection rates depend on the signal distribution.  If information is chosen, parameterize the decision by precision or by the informativeness index 
\begin_inset Formula $\gamma\in[0,1)$
\end_inset
 and solve 
\begin_inset Formula $\max_{0\leq\gamma<1}\mathbb{E}[\max\{\mu_g(Y),0\}]-\mathcal C(\gamma)$\end_inset
 with an increasing attention cost """,
        r"""If both group means are negative, the lower-mean group has the higher signal threshold.
 Hiring rates must nevertheless be computed from the group-conditional distributions because 
\begin_inset Formula $Y\mid G=g$
\end_inset
 has mean 
\begin_inset Formula $q_g$
\end_inset
; the groups share a noise variance, not a common signal distribution.
 If information is chosen, parameterize the decision by precision or by the informativeness index 
\begin_inset Formula $\gamma\in[0,1]$
\end_inset
 and solve 
\begin_inset Formula $\max_{0\leq\gamma\leq1}\mathbb{E}[\max\{\mu_g(Y),0\}]-\mathcal C(\gamma)$\end_inset
 with an increasing attention cost """,
    ),
    (
        "aggregate demand paragraph spacing",
        r"""\begin_inset Formula $w_i>0$
\end_inset

.
Aggregate demand is """,
        r"""\begin_inset Formula $w_i>0$
\end_inset
.
 Aggregate demand is """,
    ),
    (
        "Gorman display punctuation",
        r"""v_i(p,w_i)=a_i(p)+b(p)w_i,
\]

\end_inset

.""",
        r"""v_i(p,w_i)=a_i(p)+b(p)w_i.
\]

\end_inset""",
    ),
    (
        "Gorman derivative scope",
        r"""Under the usual differentiability and integrability conditions,
 the local signature of Gorman aggregation is the common wealth derivative """,
        r"""Differentiating the displayed Gorman form yields the common wealth derivative """,
    ),
    (
        "Gorman converse caution",
        r""" The converse is a local statement and should not be read as a global representation without the regularity assumptions.""",
        r""" This equality is necessary for the displayed Gorman representation; no global converse is asserted without separate integrability and domain hypotheses.""",
    ),
    (
        "aggregate WARP exact assumptions",
        r"""Sufficient condition for aggregate WARP.
 Suppose wealth shares are fixed and strictly positive,
 
\begin_inset Formula $w_i=\alpha_iW$
\end_inset

 with 
\begin_inset Formula $\alpha_i>0$
\end_inset

 and 
\begin_inset Formula $\sum_i\alpha_i=1$
\end_inset

.
 Suppose every individual demand is homogeneous of degree zero and satisfies the weak uncompensated law of demand on the normalized-price domain.
 With 
\begin_inset Formula $q=p/W$
\end_inset
, homogeneity gives 
\begin_inset Formula $x_i(p,\alpha_iW)=x_i(q,\alpha_i)$
\end_inset
.
 Then 
\begin_inset Formula $x^A(p,W)=\sum_ix_i(p,\alpha_iW)$
\end_inset

 satisfies the weak uncompensated law of demand.
 With Walras' law and the usual strictness condition,
 aggregate WARP follows.
\end_layout

\begin_layout Standard
The proof first normalizes each price--total-wealth pair to unit total wealth and then sums the individual inequalities at the common normalized wealth shares 
\begin_inset Formula $\alpha_i$
\end_inset
.
 If the shares change with prices or if wealth is reallocated after compensation,
 this argument no longer applies.""",
        r"""Sufficient condition for aggregate WARP.
 Suppose wealth shares are fixed and strictly positive,
 
\begin_inset Formula $w_i=\alpha_iW$
\end_inset
, where 
\begin_inset Formula $\alpha_i>0$
\end_inset
 and 
\begin_inset Formula $\sum_i\alpha_i=1$
\end_inset
.
 Suppose every individual demand is single-valued, homogeneous of degree zero, and satisfies Walras' law.
 Assume also that, for every normalized price pair 
\begin_inset Formula $q,q'\gg0$
\end_inset
,
\begin_inset Formula
\[
(q-q')\cdot\bigl[x_i(q,\alpha_i)-x_i(q',\alpha_i)\bigr]\leq0,
\]
\end_inset
with strict inequality whenever the two individual demanded bundles differ.
 Then the aggregate demand formed with these fixed shares satisfies aggregate WARP.
\end_layout

\begin_layout Proof
Set 
\begin_inset Formula $q=p/W$
\end_inset
 and 
\begin_inset Formula $X(q)=\sum_i x_i(q,\alpha_i)$
\end_inset
.
 Homogeneity gives 
\begin_inset Formula $x^A(p,W)=X(q)$
\end_inset
, while Walras' law gives 
\begin_inset Formula $q\cdot X(q)=1$
\end_inset
.
 Summing the individual inequalities yields
\begin_inset Formula
\[
(q-q')\cdot[X(q)-X(q')]\leq0,
\]
\end_inset
and the inequality is strict whenever 
\begin_inset Formula $X(q)\neq X(q')$
\end_inset
.
 If 
\begin_inset Formula $q\cdot X(q')\leq1$
\end_inset
 and the aggregate bundles differ, then
\begin_inset Formula
\[
0>(q-q')\cdot[X(q)-X(q')]
=2-q\cdot X(q')-q'\cdot X(q),
\]
\end_inset
so 
\begin_inset Formula $q'\cdot X(q)>2-q\cdot X(q')\geq1$
\end_inset
.
 This is aggregate WARP on the normalized domain and hence on the original price--wealth domain.
 Fixed shares are essential: if shares change with prices or after compensation, the summation argument does not apply.""",
    ),
]


FORBIDDEN = [
    "truncated to \\begin_inset Formula $[0,1)$",
    "under the usual support conditions",
    "WGARP therefore rules out",
    "weak uncompensated law of demand",
]


_FORMULA_INSET = re.compile(
    r"\\begin_inset Formula(?P<formula>.*?)\\end_inset", re.DOTALL
)
_DISPLAY_MATH = re.compile(r"\\\[(?P<formula>.*?)\\\]", re.DOTALL)


def _canonicalize_tex(formula: str) -> str:
    """Canonicalize equivalent one-token TeX argument and script syntax."""

    # LyX 2.5 adds braces to one-token command arguments and scripts.  It may
    # also serialize a superscript before a subscript although TeX treats the
    # two orders identically.
    formula = re.sub(
        r"\\(mathbf|mathbb|mathcal|overline|widehat|widetilde)"
        r"(?:\{([A-Za-z])\}|\s+([A-Za-z]))",
        lambda found: rf"\{found.group(1)}{{{found.group(2) or found.group(3)}}}",
        formula,
    )
    formula = re.sub(
        r"\\frac([A-Za-z0-9])([A-Za-z0-9])",
        r"\\frac{\1}{\2}",
        formula,
    )
    script = r"(?:\{(?:[^{}]|\{[^{}]*\})+\}|\\[A-Za-z]+|[A-Za-z0-9+*\-])"
    formula = re.sub(
        rf"\^(?P<sup>{script})_(?P<sub>{script})",
        lambda found: f"_{found.group('sub')}^{found.group('sup')}",
        formula,
    )
    formula = re.sub(
        r"([_^])\{(\\[A-Za-z]+|[A-Za-z0-9+*\-])\}", r"\1\2", formula
    )
    return formula


def _canonicalize_formula(match: re.Match[str]) -> str:
    """Erase only LyX/TeX serialization choices that preserve a formula."""

    formula = _canonicalize_tex(match.group("formula"))

    # Line wrapping and spacing inside a Formula inset are LyX serialization,
    # not manuscript content.  Command arguments above are braced first so
    # removing this whitespace cannot join a command to its argument.
    formula = re.sub(r"\s+", "", formula)
    return rf"\begin_inset Formula{formula}\end_inset"


def _canonicalize_display(match: re.Match[str]) -> str:
    formula = _canonicalize_tex(match.group("formula"))
    return rf"\[{re.sub(r'\s+', '', formula)}\]"


def canonicalize_for_check(text: str) -> str:
    """Return a comparison form shared by compact and LyX 2.5 sources.

    The release assertions below still compare every complete replacement
    block.  This function only ignores line reflow, formula whitespace, and
    equivalent one-token TeX script serialization.
    """

    text = _canonicalize_tex(text)
    text = _FORMULA_INSET.sub(_canonicalize_formula, text)
    text = _DISPLAY_MATH.sub(_canonicalize_display, text)
    text = re.sub(r"(\\[A-Za-z]+)\s+(?=[A-Za-z\\])", r"\1", text)
    text = re.sub(r"\s*(\\\])\s*(?=\\end_inset)", r"\1", text)
    return re.sub(r"\s+", " ", text).strip()


def apply_replacements(text: str) -> tuple[str, list[str]]:
    changed: list[str] = []
    for name, old, new in REPLACEMENTS:
        if old in new and new in text:
            continue
        count = text.count(old)
        if count == 1:
            text = text.replace(old, new)
            changed.append(name)
            continue
        if count == 0 and new in text:
            continue
        if count != 1:
            raise SystemExit(
                f"{name}: expected one old block or the completed replacement; found {count}"
            )
    return text, changed


def validate(text: str) -> None:
    checked = canonicalize_for_check(text)
    canonical_replacements = [
        (name, canonicalize_for_check(old), canonicalize_for_check(new))
        for name, old, new in REPLACEMENTS
    ]
    missing = [
        name for name, _old, new in canonical_replacements if new not in checked
    ]
    if missing:
        raise SystemExit("missing release fixes: " + ", ".join(missing))
    superseded = [
        name
        for name, old, new in canonical_replacements
        if old not in new and old in checked
    ]
    if superseded:
        raise SystemExit("superseded source blocks remain: " + ", ".join(superseded))
    lingering = [fragment for fragment in FORBIDDEN if fragment in text]
    if lingering:
        raise SystemExit("forbidden release fragments remain: " + ", ".join(lingering))


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("--apply", action="store_true", help="rewrite the LyX source")
    parser.add_argument("--check", action="store_true", help="verify the fixes are present")
    args = parser.parse_args()
    if args.apply == args.check:
        parser.error("choose exactly one of --apply or --check")

    original = LYX.read_text(encoding="utf-8")
    if args.apply:
        updated, changed = apply_replacements(original)
        validate(updated)
        if updated != original:
            LYX.write_text(updated, encoding="utf-8")
        print(f"Applied {len(changed)} consumer-release fixes; {len(REPLACEMENTS)} verified.")
    else:
        validate(original)
        print(f"PASS: {len(REPLACEMENTS)} consumer-release fixes are present.")


if __name__ == "__main__":
    main()
