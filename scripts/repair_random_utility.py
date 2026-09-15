#!/usr/bin/env python3
"""Tighten notation and quantifiers in the finite random-utility section."""

from pathlib import Path


BOOK = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"


ASRP = r'''\begin_layout Theorem
Finite random-utility characterization (cited).
 Let 
\begin_inset Formula $X$
\end_inset

 be finite and suppose a choice-probability system 
\begin_inset Formula $\rho=(\rho_A)_{\emptyset\neq A\subseteq X}$
\end_inset

 is observed on every nonempty menu.
 Let 
\begin_inset Formula $R$
\end_inset

 be the set of strict linear orders on 
\begin_inset Formula $X$
\end_inset

 and define 
\begin_inset Formula $M_{(a,A),r}=\mathbb{I}\{a\text{ is }r\text{-best in }A\}$
\end_inset

.
 Then the following are equivalent:
\end_layout

\begin_layout Standard
(i) 
\begin_inset Formula $\rho$
\end_inset

 satisfies the axiom of stochastic revealed preference (ASRP):
 for every finite list 
\begin_inset Formula $(a_k,A_k)_{k=1}^{n}$
\end_inset

 with 
\begin_inset Formula $a_k\in A_k$
\end_inset

,
\begin_inset Formula $\sum_{k=1}^{n}\rho_{A_k}(a_k)\leq\max_{r\in R}\sum_{k=1}^{n}M_{(a_k,A_k),r}$
\end_inset

.
\end_layout

\begin_layout Standard
(ii) There is a probability vector 
\begin_inset Formula $\pi\in\Delta(R)$
\end_inset

 such that 
\begin_inset Formula $\rho_A(a)=\sum_{r\in R}\pi(r)M_{(a,A),r}$
\end_inset

 for every nonempty 
\begin_inset Formula $A\subseteq X$
\end_inset

 and every 
\begin_inset Formula $a\in A$
\end_inset

.
 Equivalently,
 after stacking the observations,
\begin_inset Formula $M\pi=\rho$
\end_inset

.
\end_layout

\begin_layout Standard
The implication from (ii) to (i) is the elementary bound that an expectation cannot exceed the largest deterministic score.
 The converse is the finite-dimensional theorem of the alternative:
 ASRP is exactly the condition that 
\begin_inset Formula $\rho$
\end_inset

 lies in the convex hull of the deterministic ranking columns of 
\begin_inset Formula $M$
\end_inset

.
\end_layout

\begin_layout Standard
For 
\begin_inset Formula $|X|=m$
\end_inset

,
 
\begin_inset Formula $|R|=m!$
\end_inset

.
 Ties can be incorporated by allowing weak orders,
 but the strict-order formulation is sufficient for the generic no-ties model used here.
\end_layout
'''


def main() -> None:
    text = BOOK.read_text()
    start = text.index("\\begin_layout Lemma\n\\begin_inset CommandInset label\n")
    end = text.index("\\begin_layout Standard\nThere is a surprising result about random utility.", start)
    text = text[:start] + ASRP.rstrip() + "\n\n" + text[end:]
    text = text.replace(
        r"\begin_inset Formula $p^{M}(a,A)=\sum_{r\in R}\pi^{rep}(r)\mathbb{I}(arb\forall b\in A\setminus\{a\}).$\n\end_inset",
        r"\begin_inset Formula $p^{M}(a,A)=\sum_{r\in R}\pi^{rep}(r)\mathbb{I}\{a\text{ is }r\text{-best in }A\}$.\n\end_inset",
    )
    text = text.replace("there exist a random utility", "there exists a random-utility distribution")
    text = text.replace("(ii) implies RU (i).", "This completes the characterization.")
    text = text.replace("I can write the following when", "Thus, under random utility,")
    BOOK.write_text(text)


if __name__ == "__main__":
    main()
