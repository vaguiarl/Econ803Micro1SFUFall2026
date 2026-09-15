#!/usr/bin/env python3
"""Replace the under-specified expected-utility revealed-preference proof."""

from pathlib import Path


BOOK = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"


SECTION = r'''\begin_layout Section
Revealed Preference of Expected Utility under Concavity
\end_layout

\begin_layout Standard
Let 
\begin_inset Formula $S$
\end_inset

 be a finite set of states with fixed probabilities 
\begin_inset Formula $\pi_s>0$
\end_inset

,
 and let a contingent consumption plan be 
\begin_inset Formula $x=(x_s)_{s\in S}\in\mathbb{R}_{++}^{S}$
\end_inset

.
 At prices 
\begin_inset Formula $p\in\mathbb{R}_{++}^{S}$
\end_inset

 and wealth 
\begin_inset Formula $w>0$
\end_inset

,
 the consumer solves
\begin_inset Formula $\max_{x}\sum_{s\in S}\pi_su(x_s)\text{ subject to }\sum_{s\in S}p_sx_s\leq w$
\end_inset

,
 where 
\begin_inset Formula $u$
\end_inset

 is continuous,
 increasing and concave.
\end_layout

\begin_layout Proposition
Interior first-order conditions.
 If 
\begin_inset Formula $u$
\end_inset

 is differentiable and an optimum is interior,
 then there is 
\begin_inset Formula $\lambda>0$
\end_inset

 such that
\begin_inset Formula $\pi_su'(x_s)=\lambda p_s$
\end_inset

 for every 
\begin_inset Formula $s\in S$
\end_inset

.
 Concavity makes these conditions sufficient for a global optimum;
 boundary observations require the corresponding KKT inequalities.
\end_layout

\begin_layout Definition
Risk-averse expected-utility rationalization.
 A finite dataset 
\begin_inset Formula $O^T=\{(p^t,x^t)\}_{t=1}^{T}$
\end_inset

 is rationalized if there is one continuous,
 increasing and concave Bernoulli utility 
\begin_inset Formula $u$
\end_inset

 such that each 
\begin_inset Formula $x^t$
\end_inset

 maximizes 
\begin_inset Formula $\sum_s\pi_su(x_s)$
\end_inset

 on the budget set 
\begin_inset Formula $\{x:p^t\cdot x\leq p^t\cdot x^t\}$
\end_inset

.
\end_layout

\begin_layout Theorem
Finite-data test (cited).
 Assume all observations are interior and 
\begin_inset Formula $\pi_s>0$
\end_inset

.
 The dataset has a risk-averse expected-utility rationalization if and only if there are numbers 
\begin_inset Formula $\beta_s^t>0$
\end_inset

 and 
\begin_inset Formula $\lambda^t>0$
\end_inset

 such that
\begin_inset Formula $\pi_s\beta_s^t=\lambda^tp_s^t$
\end_inset

 for every 
\begin_inset Formula $s,t$
\end_inset

 and
\begin_inset Formula $x_s^t>x_{s'}^{t'}\Longrightarrow\beta_s^t\leq\beta_{s'}^{t'}$
\end_inset

 for every pair of observed state-contingent quantities.
 The monotonicity condition is the finite signature of a single decreasing marginal-utility function;
 the price equations are the common first-order conditions.
\end_layout

\begin_layout Standard
The theorem is an Afriat-style interpolation result for one Bernoulli utility across states and observations.
 It is stated for interior data to keep the notation transparent;
 zero quantities are handled by replacing equalities with KKT inequalities.
\end_layout
'''


def main() -> None:
    text = BOOK.read_text()
    start = text.index("\\begin_layout Section\nRevealed Preference of Expected Utility under Concavity\n\\end_layout")
    end = text.index("\\begin_layout Section\nExperimental Evidence", start)
    text = text[:start] + SECTION.rstrip() + "\n\n" + text[end:]
    BOOK.write_text(text)


if __name__ == "__main__":
    main()
