from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"
s = path.read_text()

# Clean the primitive and stochastic-dominance setup.
start = s.index(r"""\begin_layout Section
Primitives
\end_layout""")
end = s.index(r"""\begin_layout Section
Independence Axiom
\end_layout""", start)
primitive = r'''\begin_layout Section
Primitives
\end_layout

\begin_layout Standard
Let \begin_inset Formula $Z\subseteq\mathbb{R}$\end_inset
 be a finite set of monetary prizes.  A lottery is a probability mass function \begin_inset Formula $p:Z\to[0,1]$\end_inset
 satisfying \begin_inset Formula $\sum_{z\in Z}p(z)=1$\end_inset
.
 Write \begin_inset Formula $\Delta(Z)$\end_inset
 for the set of lotteries and \begin_inset Formula $\delta_z$\end_inset
 for the degenerate lottery assigning probability one to \begin_inset Formula $z$\end_inset
.
 Mixtures are defined pointwise by
\end_layout

\begin_layout Standard
\begin_inset Formula 
\[
[\alpha p+(1-\alpha)q](z)=\alpha p(z)+(1-\alpha)q(z),
\qquad \alpha\in[0,1].
\]
\end_inset
\end_layout

\begin_layout Standard
For a Bernoulli utility \begin_inset Formula $u:Z\to\mathbb{R}$\end_inset
,
 expected utility is \begin_inset Formula $U(p)=\sum_{z\in Z}u(z)p(z)$\end_inset
.
\end_layout

\begin_layout Section
Stochastic dominance
\end_layout

\begin_layout Definition
First-order stochastic dominance.
 For lotteries \begin_inset Formula $p,q\in\Delta(Z)$\end_inset
 with cumulative distribution functions \begin_inset Formula $F_p(t)=\sum_{z\leq t}p(z)$\end_inset
 and \begin_inset Formula $F_q(t)=\sum_{z\leq t}q(z)$\end_inset
,
 write \begin_inset Formula $p\succeq^{FOSD}q$\end_inset
 if \begin_inset Formula $F_p(t)\leq F_q(t)$\end_inset
 for every \begin_inset Formula $t\in\mathbb{R}$\end_inset
.
 The relation is generally incomplete.
\end_layout

\begin_layout Theorem
If \begin_inset Formula $p\succeq^{FOSD}q$\end_inset
 and \begin_inset Formula $u$\end_inset
 is increasing, then \begin_inset Formula $U(p)\geq U(q)$\end_inset
 for expected utility \begin_inset Formula $U$\end_inset
.
 Strict inequality follows when the dominance is strict on a set that receives positive probability and \begin_inset Formula $u$\end_inset
 is strictly increasing there.
\end_layout

\begin_layout Section
Model and expected utility
\end_layout

\begin_layout Standard
We observe a choice correspondence on a family of subsets of \begin_inset Formula $\Delta(Z)$\end_inset
 and represent the decision maker's preference by a relation \begin_inset Formula $\succeq$\end_inset
 on lotteries.
\end_layout

\begin_layout Definition
Expected utility representation.
 The preference relation has an expected utility representation if there is a Bernoulli utility \begin_inset Formula $u:Z\to\mathbb{R}$\end_inset
 such that \begin_inset Formula $p\succeq q\iff\sum_{z\in Z}u(z)p(z)\geq\sum_{z\in Z}u(z)q(z)$\end_inset
.
\end_layout

'''
s = s[:start] + primitive + s[end:]

# Replace the risk-attitude definitions, whose earlier version confused CE with utility.
start = s.index(r"""\begin_layout Section
Attitudes towards Risk
\end_layout""")
end = s.index(r"""\begin_layout Section
Expected Utility for Infinite Sets
\end_layout""", start)
risk = r'''\begin_layout Section
Attitudes towards Risk
\end_layout

\begin_layout Standard
Assume that the certainty set contains the convex hull of the finite prize set.  For a lottery \begin_inset Formula $p$\end_inset
,
 its expected monetary value is \begin_inset Formula $\overline z(p)=\sum_{z\in Z}zp(z)$\end_inset
 and the corresponding certain outcome is \begin_inset Formula $\delta_{\overline z(p)}$\end_inset
.
\end_layout

\begin_layout Definition
Risk aversion.
 A decision maker is risk averse if \begin_inset Formula $\delta_{\overline z(p)}\succeq p$\end_inset
 for every lottery \begin_inset Formula $p$\end_inset
.
 Under expected utility, risk aversion is equivalent to concavity of the Bernoulli utility:
\begin_inset Formula 
\[
\sum_{z\in Z}p(z)u(z)\leq u\!\left(\sum_{z\in Z}p(z)z\right).
\]
\end_inset
\end_layout

\begin_layout Definition
Certainty equivalent and risk premium.
 If \begin_inset Formula $u$\end_inset
 is strictly increasing and its range contains \begin_inset Formula $U(p)$\end_inset
,
 the certainty equivalent is the prize \begin_inset Formula $CE(p,u)=u^{-1}(U(p))$\end_inset
 and the (monetary) risk premium is \begin_inset Formula $\rho(p,u)=\overline z(p)-CE(p,u)$\end_inset
.
 A risk-averse expected-utility decision maker has \begin_inset Formula $\rho(p,u)\geq0$\end_inset
.
\end_layout

\begin_layout Definition
Probability premium.
 For prizes \begin_inset Formula $x-\varepsilon,x,x+\varepsilon$\end_inset
 in the certainty set, \begin_inset Formula $\pi(x,\varepsilon,u)$\end_inset
 is defined by
\begin_inset Formula 
\[
u(x)=\left(\frac12+\pi\right)u(x+\varepsilon)+\left(\frac12-\pi\right)u(x-\varepsilon).
\]
\end_inset
 It is the change in probability needed to make the symmetric two-point lottery equivalent to the sure prize.
\end_layout

\begin_layout Proposition
For a twice differentiable, strictly increasing Bernoulli utility, the local risk premium for a symmetric small spread satisfies
\begin_inset Formula 
\[
\rho\bigl(\tfrac12\delta_{x-\varepsilon}+\tfrac12\delta_{x+\varepsilon},u\bigr)
 =-\frac{u''(x)}{2u'(x)}\varepsilon^{2}+o(\varepsilon^{2}).
\]
\end_inset
 Thus local concavity corresponds to a nonnegative local risk premium.
\end_layout

'''
s = s[:start] + risk + s[end:]

# Small grammar and sign fixes in the asset application.
s = s.replace("A risk neutral subject will choose", "A risk-neutral subject chooses")
s = s.replace("An individual who switches to", "An individual who switches to")
s = s.replace("The first order conditions are:", "The first-order conditions are:")
s = s.replace("cannot satisfiy", "cannot satisfy")
s = s.replace("The expected outcome of", "The expected value of")
s = s.replace("the more risk-averse individual the switch will be later", "a more risk-averse individual typically switches later, under the maintained utility and payoff assumptions")
s = s.replace("Theorem\nIf \n\\begin_inset Formula $F\\succeq^{FOD}G$", "Theorem\nIf \n\\begin_inset Formula $F\\succeq^{FOSD}G$")
s = s.replace("F\\succeq^{FOD}G", "F\\succeq^{FOSD}G")
s = s.replace("FOSD means that", "FOSD means")

path.write_text(s)
print(f"repaired uncertainty definitions in {path}")
