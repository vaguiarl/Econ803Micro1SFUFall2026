#!/usr/bin/env python3
"""Replace the discrimination example's unsupported comparative statics."""

from pathlib import Path


BOOK = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"


SECTION = r'''\begin_layout Section
Discrimination with Rational Inattention
\end_layout

\begin_layout Standard
Consider a firm deciding whether to hire an applicant.
 The applicant's unobserved productivity is 
\begin_inset Formula $q$
\end_inset

 and hiring yields payoff 
\begin_inset Formula $q$
\end_inset

,
 while rejecting yields 
\begin_inset Formula $0$
\end_inset

.
 Before observing an applicant-specific signal,
 the firm observes a group label 
\begin_inset Formula $G\in\{R,B\}$
\end_inset

 and has prior 
\begin_inset Formula $q\mid G\sim\mathcal{N}(q_G,\sigma_q^2)$
\end_inset

,
 with 
\begin_inset Formula $q_R<q_B$
\end_inset

.
 Thus 
\begin_inset Formula $R$
\end_inset

 is the lower-mean group under this labeling.
\end_layout

\begin_layout Standard
The firm chooses signal noise and then observes 
\begin_inset Formula $y=q+\varepsilon$
\end_inset

,
 where 
\begin_inset Formula $\varepsilon\sim\mathcal{N}(0,\sigma_{\varepsilon}^{2})$
\end_inset

 is independent of 
\begin_inset Formula $q$
\end_inset

.
 Gaussian updating gives the posterior mean
\begin_inset Formula $m_G(y)=\mathbb{E}[q\mid y,G]=\alpha y+(1-\alpha)q_G$
\end_inset

 with
\begin_inset Formula $\alpha=\frac{\sigma_q^2}{\sigma_q^2+\sigma_{\varepsilon}^{2}}\in[0,1]$
\end_inset

.
\end_layout

\begin_layout Proposition
Optimal hiring rule.
 Given 
\begin_inset Formula $(y,G)$
\end_inset

,
 hiring is optimal if and only if 
\begin_inset Formula $m_G(y)>0$
\end_inset

;
 otherwise rejection is optimal.
\end_layout

\begin_layout Standard
The firm chooses the noise level by comparing the expected value of this rule with the information cost:
\begin_inset Formula $\max_{\sigma_{\varepsilon}^{2}\geq0}\mathbb{E}[\max\{m_G(y),0\}]-C(\sigma_{\varepsilon}^{2})$
\end_inset

.
 If 
\begin_inset Formula $C'(\sigma_{\varepsilon}^{2})<0$
\end_inset

,
 then higher noise is cheaper and lower noise is more precise.
 The optimum depends on the prior distribution of groups and on the full cost function;
 the posterior formula alone does not determine group-specific attention.
\end_layout

\begin_layout Standard
For a fixed 
\begin_inset Formula $\alpha$
\end_inset

,
 the hiring threshold in signal space is
\begin_inset Formula $y_G=-\frac{1-\alpha}{\alpha}q_G$
\end_inset

 when 
\begin_inset Formula $\alpha>0$
\end_inset

.
 If both group means are negative (a cherry-picking environment),
 the lower-mean group 
\begin_inset Formula $R$
\end_inset

 has the higher threshold and is hired less often for any common signal distribution.
 If both means are positive (a lemon-dropping environment),
 the same threshold formula applies,
 but which group is rejected depends on the signal and cannot be inferred from the means alone.
 Comparative statements about attention require additional primitives and should not be read as implications of Bayesian updating alone.
\end_layout
'''


def main() -> None:
    text = BOOK.read_text()
    start = text.index("\\begin_layout Section\nDiscrimination with Rational Inattention\n\\end_layout")
    end = text.index("\\begin_layout Chapter\nChoice under Uncertainty", start)
    text = text[:start] + SECTION.rstrip() + "\n\n" + text[end:]
    BOOK.write_text(text)


if __name__ == "__main__":
    main()
