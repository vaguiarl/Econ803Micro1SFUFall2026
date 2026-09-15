#!/usr/bin/env python3
"""Replace the discrete-choice lecture draft with a correct compact chapter."""

from pathlib import Path


BOOK = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"


CHAPTER = r'''\begin_layout Chapter
Discrete Choice and Random Utility
\end_layout

\begin_layout Section
Choice from a finite menu
\end_layout

\begin_layout Standard
There are alternatives 
\begin_inset Formula $j\in\{0,1,\ldots,J\}$
\end_inset

,
 where 
\begin_inset Formula $j=0$
\end_inset

 is the outside option.
 Consumer 
\begin_inset Formula $i$
\end_inset

 chooses one alternative from the menu after comparing conditional indirect utilities
\begin_inset Formula $U_{ij}^{*}=V_j(x_j,p_j,y_i)+\varepsilon_{ij}$
\end_inset

.
 Here 
\begin_inset Formula $x_j$
\end_inset

 denotes observed attributes,
 
\begin_inset Formula $V_j$
\end_inset

 is mean utility,
 and 
\begin_inset Formula $\varepsilon_{ij}$
\end_inset

 is an unobserved preference shock.
 The choice probability is
\begin_inset Formula $P_{ij}=\Pr\{U_{ij}^{*}\geq U_{ik}^{*}\text{ for every }k\}$
\end_inset

,
 with strict inequalities almost surely when the shock distribution is continuous.
\end_layout

\begin_layout Standard
If the outside good has price 
\begin_inset Formula $p_0$
\end_inset

 and quantity 
\begin_inset Formula $z$
\end_inset

,
 a budget identity 
\begin_inset Formula $p_j+p_0z=y_i$
\end_inset

 yields 
\begin_inset Formula $z=(y_i-p_j)/p_0$
\end_inset

 for a purchased alternative.
 This reduction is valid only when the implied outside-good quantity is feasible.
\end_layout

\begin_layout Section
Multinomial logit and IIA
\end_layout

\begin_layout Standard
Suppose the shocks are independent and identically distributed Type-I extreme value with scale 
\begin_inset Formula $\mu>0$
\end_inset

.
 Then the multinomial-logit probabilities are
\begin_inset Formula $P_{ij}=\frac{\exp(V_j/\mu)}{\sum_{k=0}^{J}\exp(V_k/\mu)}$
\end_inset

.
\end_layout

\begin_layout Proposition
Independence of irrelevant alternatives.
 Under multinomial logit,
 for any two alternatives 
\begin_inset Formula $j,k$
\end_inset

 that remain available,
\begin_inset Formula $\frac{P_{ij}}{P_{ik}}=\exp((V_j-V_k)/\mu)$
\end_inset

 is independent of the other alternatives in the menu.
\end_layout

\begin_layout Example
Red-bus/blue-bus.
 If walking and a red bus initially have equal probabilities,
 adding a blue bus that is nearly identical to the red bus should split the bus share while leaving walking's share close to its original value.
 Multinomial logit instead preserves the walking-to-red-bus odds ratio,
 illustrating the empirical content and limitation of IIA.
\end_layout

\begin_layout Standard
The multinomial probit model replaces the extreme-value shocks with a jointly normal vector.
 Its pairwise differences are generally correlated,
 so it does not impose IIA.
\end_layout

\begin_layout Section
Random utility
\end_layout

\begin_layout Definition
Random-utility representation.
 Let 
\begin_inset Formula $A$
\end_inset

 be a finite menu and let 
\begin_inset Formula $\boldsymbol{U}:\Omega\to\mathbb{R}^{A}$
\end_inset

 be a measurable random utility vector.
 The induced choice probabilities are
\begin_inset Formula $\rho_A(a)=\mathbb{P}\{\boldsymbol{U}(a)>\boldsymbol{U}(b)\text{ for every }b\in A\setminus\{a\}\}$
\end_inset

.
\end_layout

\begin_layout Standard
When 
\begin_inset Formula $A$
\end_inset

 is finite and choice probabilities are observed on every nonempty menu,
 the deterministic types are the strict linear orders on 
\begin_inset Formula $A$
\end_inset

.
 Stacking the probabilities gives 
\begin_inset Formula $\rho=M\pi$
\end_inset

,
 where 
\begin_inset Formula $\pi\in\Delta(R)$
\end_inset

 is a distribution over those orders and 
\begin_inset Formula $M_{(a,B),r}=\mathbb{I}\{a\text{ is }r\text{-best in }B\}$
\end_inset

.
 The finite ASRP condition in the preceding chapter is equivalent to the existence of such a 
\begin_inset Formula $\pi$
\end_inset

.
\end_layout

\begin_layout Section
Random expected utility
\end_layout

\begin_layout Definition
Random expected utility.
 For a finite prize set 
\begin_inset Formula $Z$
\end_inset

 and lotteries 
\begin_inset Formula $p\in\Delta(Z)$
\end_inset

,
 a random Bernoulli utility 
\begin_inset Formula $\boldsymbol{u}:\Omega\to\mathbb{R}^{Z}$
\end_inset

 induces 
\begin_inset Formula $\boldsymbol{U}_{\omega}(p)=\sum_{z\in Z}\boldsymbol{u}_{\omega}(z)p(z)$
\end_inset

.
 Choice probabilities are obtained by maximizing this random expected utility on each menu of lotteries.
\end_layout

\begin_layout Standard
The representation imposes linearity in mixtures and regularity under menu expansion.
 Extremeness and weak-star continuity are additional conditions in the Gul--Pesendorfer characterization;
 that result is cited rather than reproved here.
\end_layout

\begin_layout Section
Attributes and consumer surplus
\end_layout

\begin_layout Standard
With observed attributes 
\begin_inset Formula $x=(x_a)_{a\in A}$
\end_inset

,
 a common specification is
\begin_inset Formula $U(a,x)=v(a,x_a)+\varepsilon_a$
\end_inset

,
 where the distribution of 
\begin_inset Formula $\varepsilon=(\varepsilon_a)_{a\in A}$
\end_inset

 is independent of 
\begin_inset Formula $x$
\end_inset

.
 The linear-index model uses 
\begin_inset Formula $v(a,x_a)=x_a^{\mathsf T}\beta$
\end_inset

.
 Independence is a maintained exogeneity assumption,
 not a consequence of the random-utility definition.
\end_layout

\begin_layout Definition
Expected maximum utility.
 The expected value of a menu is
\begin_inset Formula $V(x)=\mathbb{E}[\max_{a\in A}\{v(a,x_a)+\varepsilon_a\}]$
\end_inset

.
 If the deterministic utility contains 
\begin_inset Formula $-\alpha p_a$
\end_inset

 with 
\begin_inset Formula $\alpha>0$
\end_inset

 as the price coefficient,
 the money-metric consumer surplus is 
\begin_inset Formula $V(x)/\alpha$
\end_inset

 up to the chosen utility normalization.
 If shocks are merely decision errors rather than preference shocks,
 this expression is not a welfare measure.
\end_layout

\begin_layout Proposition
Williams--Daly--Zachary envelope result (cited).
 If the shock distribution has finite first moments and ties occur with probability zero,
 then 
\begin_inset Formula $V$
\end_inset

 is convex and differentiable in the vector of mean utilities,
 and
\begin_inset Formula $\frac{\partial V(x)}{\partial v(a)}=\rho(a,x)$
\end_inset

.
 Consequently the Jacobian of choice probabilities is the Hessian of 
\begin_inset Formula $V$
\end_inset

,
 hence symmetric and positive semidefinite.
 Translation invariance implies that the rows and columns sum to zero.
\end_layout

\begin_layout Standard
The envelope identity is the basis for likelihood and welfare calculations in discrete-choice models.
 Additional sign restrictions such as monotone substitution patterns require additional assumptions on the shock distribution and utility index;
 they do not follow from random utility alone.
\end_layout
'''


def main() -> None:
    text = BOOK.read_text()
    start = text.index("\\begin_layout Chapter\nDiscrete Choice and Random Utility\n\\end_layout")
    end = text.index("\\begin_layout Chapter\nTheory of the Firm", start)
    text = text[:start] + CHAPTER.rstrip() + "\n\n" + text[end:]
    BOOK.write_text(text)


if __name__ == "__main__":
    main()
