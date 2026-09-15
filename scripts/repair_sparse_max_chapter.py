from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"
s = path.read_text()
start_marker = r"""\begin_layout Chapter
Behavioral Economics:
 The Sparse-Max Consumer
\end_layout"""
end_marker = r"""\begin_layout Chapter
Choice under Uncertainty
\end_layout"""
start = s.index(start_marker)
end = s.index(end_marker, start)
chapter = r'''\begin_layout Chapter
Behavioral Economics: Sparse-Max and Rational Inattention
\end_layout

\begin_layout Standard
The benchmark consumer maximizes utility using the true budget and prices.  A sparse-max consumer keeps the true budget constraint but forms a decision using a perceived price vector.  This chapter states the behavioral rule explicitly and records which benchmark conclusions no longer follow automatically.
\end_layout

\begin_layout Section
The Sparse-Max Decision Rule
\end_layout

\begin_layout Standard
Let \begin_inset Formula $X=\mathbb{R}_{+}^{L}$\end_inset
,
 true prices \begin_inset Formula $p\gg0$\end_inset
,
 perceived prices \begin_inset Formula $\widehat p\gg0$\end_inset
,
 and wealth \begin_inset Formula $w>0$\end_inset
.
 Assume \begin_inset Formula $u$\end_inset
 is differentiable and that the tangency system below has a solution.
 A sparse-max choice is obtained by first selecting a bundle that satisfies the perceived-price first-order condition
\end_layout

\begin_layout Standard
\begin_inset Formula 
\[
\nabla u(x)=\lambda\widehat p,
\qquad \lambda>0,
\]
\end_inset
\end_layout

\begin_layout Standard
and then choosing \begin_inset Formula $\lambda$\end_inset
 so that the selected bundle satisfies the actual budget equation \begin_inset Formula $p\cdot x=w$\end_inset
.
 At a boundary solution, replace the equality by the corresponding KKT inequalities.
 This two-stage rule is written \begin_inset Formula $x^{s}(p,\widehat p,w)$\end_inset
.
 It is not the ordinary utility-maximization problem with \begin_inset Formula $\widehat p$\end_inset
 in the budget constraint.
\end_layout

\begin_layout Standard
When the rational demand \begin_inset Formula $x^{r}(\widehat p,\widetilde w)$\end_inset
 is single-valued and locally invertible in wealth, the same sparse-max bundle can be written as \begin_inset Formula $x^{s}(p,\widehat p,w)=x^{r}(\widehat p,\widetilde w)$\end_inset
 for the unique \begin_inset Formula $\widetilde w$\end_inset
 satisfying \begin_inset Formula $p\cdot x^{r}(\widehat p,\widetilde w)=w$\end_inset
.
 This is a change of representation, not an assertion that the consumer faces \begin_inset Formula $\widehat p$\end_inset
 in the market.
\end_layout

\begin_layout Section
Cobb--Douglas Sparse-Max Demand
\end_layout

\begin_layout Example
Let \begin_inset Formula $u(x)=\sum_{\ell=1}^{L}\alpha_{\ell}\log x_{\ell}$\end_inset
 with \begin_inset Formula $\alpha_{\ell}>0$\end_inset
 and \begin_inset Formula $\sum_{\ell}\alpha_{\ell}=1$\end_inset
.
 The perceived-price first-order conditions give
\end_layout

\begin_layout Example
\begin_inset Formula 
\[
x_{\ell}=\frac{\alpha_{\ell}}{\lambda\widehat p_{\ell}}.
\]
\end_inset
\end_layout

\begin_layout Standard
Imposing the actual budget yields \begin_inset Formula $\lambda=\frac{1}{w}\sum_{k=1}^{L}\alpha_k\frac{p_k}{\widehat p_k}$\end_inset
 and therefore
\end_layout

\begin_layout Example
\begin_inset Formula 
\[
x^{s}_{\ell}(p,\widehat p,w)=
\frac{\alpha_{\ell}w/\widehat p_{\ell}}
{\sum_{k=1}^{L}\alpha_k p_k/\widehat p_k}.
\]
\end_inset
\end_layout

\begin_layout Standard
Indeed, \begin_inset Formula $\sum_{\ell}p_{\ell}x^{s}_{\ell}=w$\end_inset
.
 If \begin_inset Formula $\widehat p=p$\end_inset
,
 this reduces to the ordinary Cobb--Douglas demand \begin_inset Formula $x_{\ell}=\alpha_{\ell}w/p_{\ell}$\end_inset
.
\end_layout

\begin_layout Section
Perceived Prices and Limited Attention
\end_layout

\begin_layout Standard
One parsimonious attention rule combines the true price with a default price \begin_inset Formula $p^{d}\gg0$\end_inset
:
\end_layout

\begin_layout Standard
\begin_inset Formula 
\[
\widehat p_{\ell}(p)=m_{\ell}p_{\ell}+(1-m_{\ell})p^{d}_{\ell},
\qquad m_{\ell}\in[0,1].
\]
\end_inset
\end_layout

\begin_layout Standard
The vector \begin_inset Formula $m=(m_{1},\ldots,m_{L})$\end_inset
 measures attention to price components.  Full attention is \begin_inset Formula $m_{\ell}=1$\end_inset
 for every \begin_inset Formula $\ell$\end_inset
; setting \begin_inset Formula $m_{\ell}=0$\end_inset
 makes that component equal to its default.  With \begin_inset Formula $M=\operatorname{diag}(m_{1},\ldots,m_{L})$\end_inset
,
 \begin_inset Formula $\widehat p(p)=Mp+(I-M)p^{d}$\end_inset
.
\end_layout

\begin_layout Proposition
Comparative statics under perceived prices.
 Suppose the tangency bundle can be written as a differentiable map \begin_inset Formula $r(\widehat p,\lambda)$\end_inset
 and \begin_inset Formula $x^{s}(p,w)=r(\widehat p(p),\lambda(p,w))$\end_inset
,
 where \begin_inset Formula $\lambda(p,w)$\end_inset
 is determined by \begin_inset Formula $p\cdot r(\widehat p(p),\lambda)=w$\end_inset
.
 Then the chain rule gives
\begin_inset Formula 
\[
D_p x^{s}=D_{\widehat p}r\,M+\partial_{\lambda}r\,(\nabla_p\lambda)^{\top},
\qquad
D_w x^{s}=\partial_{\lambda}r\,\partial_w\lambda.
\]
\end_inset
\end_layout

\begin_layout Standard
The second terms are the response of the multiplier needed to restore the actual budget.  Consequently, an identity such as \begin_inset Formula $S^{s}=S^{r}M$\end_inset
 requires additional compensation and normalization assumptions; it is not a generic implication of the attention rule.
\end_layout

\begin_layout Standard
Because the default price is fixed, scaling \begin_inset Formula $(p,w)$\end_inset
 by a common positive factor generally changes \begin_inset Formula $\widehat p(p)$\end_inset
 and therefore can violate homogeneity of degree zero.  WARP, Slutsky symmetry, and welfare theorems must likewise be checked for the specified behavioral demand rather than imported from the rational benchmark.
\end_layout

\begin_layout Section
Endogenizing Attention
\end_layout

\begin_layout Standard
Let the unknown state be \begin_inset Formula $X\sim\mathcal{N}(x^{d},\sigma_x^{2})$\end_inset
 and let the signal be \begin_inset Formula $S=X+\varepsilon$\end_inset
 with independent \begin_inset Formula $\varepsilon\sim\mathcal{N}(0,\sigma_{\varepsilon}^{2})$\end_inset
.
 Under quadratic loss \begin_inset Formula $\ell(a,X)=\frac12(a-X)^2$\end_inset
,
 the optimal action is the posterior mean
\end_layout

\begin_layout Standard
\begin_inset Formula 
\[
a^{*}(s)=\mathbb{E}[X\mid S=s]=m s+(1-m)x^{d},
\qquad m=\frac{\sigma_x^{2}}{\sigma_x^{2}+\sigma_{\varepsilon}^{2}}\in[0,1].
\]
\end_inset
\end_layout

\begin_layout Standard
The posterior variance is \begin_inset Formula $(1-m)\sigma_x^{2}$\end_inset
,
 so expected loss at the optimal action is \begin_inset Formula $\frac12(1-m)\sigma_x^{2}$\end_inset
.
 If attention itself is costly, represent the cost by an increasing function \begin_inset Formula $C(m)$\end_inset
 and solve
\end_layout

\begin_layout Standard
\begin_inset Formula 
\[
\max_{0\leq m<1}-\frac12(1-m)\sigma_x^{2}-C(m).
\]
\end_inset
\end_layout

\begin_layout Standard
For example, with \begin_inset Formula $C(m)=\kappa m^{2}/2$\end_inset
,
 an interior optimum satisfies \begin_inset Formula $m=\sigma_x^{2}/(2\kappa)$\end_inset
 and is truncated to \begin_inset Formula $[0,1)$\end_inset
 when the unconstrained value lies outside that interval.  The comparative statics depend on the cost specification.
\end_layout

\begin_layout Standard
A capacity formulation is also transparent.  If the information cost is \begin_inset Formula $-\frac12\log(1-m)$\end_inset
 and capacity is bounded by \begin_inset Formula $K$\end_inset
,
 then \begin_inset Formula $-\frac12\log(1-m)\leq K$\end_inset
 implies \begin_inset Formula $m\leq1-e^{-2K}$\end_inset
.
 Since the value of information is increasing in \begin_inset Formula $m$\end_inset
,
 the capacity-constrained optimum attains this upper bound.
\end_layout

\begin_layout Section
Discrimination with Rational Inattention
\end_layout

\begin_layout Standard
Consider a firm deciding whether to hire an applicant.  Productivity is \begin_inset Formula $Q$\end_inset
 and hiring yields payoff \begin_inset Formula $Q$\end_inset
,
 while rejecting yields \begin_inset Formula $0$\end_inset
.
 Before observing an applicant-specific signal, the firm observes \begin_inset Formula $G\in\{R,B\}$\end_inset
 and has prior \begin_inset Formula $Q\mid G\sim\mathcal{N}(q_G,\sigma_q^{2})$\end_inset
 with \begin_inset Formula $q_R<q_B$\end_inset
.
\end_layout

\begin_layout Standard
The firm observes \begin_inset Formula $Y=Q+\varepsilon$\end_inset
,
 where \begin_inset Formula $\varepsilon\sim\mathcal{N}(0,\sigma_{\varepsilon}^{2})$\end_inset
 is independent.  The posterior mean is
\end_layout

\begin_layout Standard
\begin_inset Formula 
\[
m_G(y)=\mathbb{E}[Q\mid Y=y,G]=\alpha y+(1-\alpha)q_G,
\qquad \alpha=\frac{\sigma_q^{2}}{\sigma_q^{2}+\sigma_{\varepsilon}^{2}}.
\]
\end_inset
\end_layout

\begin_layout Proposition
Optimal hiring rule.  Conditional on \begin_inset Formula $(y,G)$\end_inset
,
 hire if and only if \begin_inset Formula $m_G(y)>0$\end_inset
; otherwise reject.  For \begin_inset Formula $\alpha>0$\end_inset
 the signal threshold is \begin_inset Formula $y_G=-(1-\alpha)q_G/\alpha$\end_inset
.
\end_layout

\begin_layout Standard
If both group means are negative, the lower-mean group has the higher threshold and is hired less often under a common signal distribution.  If both means are positive, the same threshold formula applies, but group-specific rejection rates depend on the signal distribution.  Choosing the noise level solves
\begin_inset Formula $\max_{\sigma_{\varepsilon}^{2}\geq0}\mathbb{E}[\max\{m_G(Y),0\}]-C(\sigma_{\varepsilon}^{2})$\end_inset
;
 group-specific attention requires the group priors and a fully specified cost function.
\end_layout

'''
path.write_text(s[:start] + chapter + s[end:])
print(f"rewrote sparse-max chapter in {path}")
