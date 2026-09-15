#!/usr/bin/env python3
"""Replace the unfinished profit-function proof with a precise proposition."""

from pathlib import Path


BOOK = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"


BLOCK = r'''\begin_layout Proposition
Properties of the profit function (cited).
 Assume 
\begin_inset Formula $Y$
\end_inset

 is nonempty,
 closed and convex,
 and has free disposal.
 Let 
\begin_inset Formula $\pi(p)=\sup_{y\in Y}p\cdot y$
\end_inset

 and 
\begin_inset Formula $y(p)=\arg\max_{y\in Y}p\cdot y$
\end_inset

 whenever the maximum is finite and attained.
 Then:
\end_layout

\begin_layout Itemize
\begin_inset Formula $\pi$
\end_inset

 is convex and homogeneous of degree one in prices.
\end_layout

\begin_layout Itemize
\begin_inset Formula $y$
\end_inset

 is homogeneous of degree zero.
 If 
\begin_inset Formula $Y$
\end_inset

 is convex,
 the argmax set is convex-valued.
\end_layout

\begin_layout Itemize
 If supply is single-valued and differentiable at 
\begin_inset Formula $p$
\end_inset

,
 Hotelling's lemma gives 
\begin_inset Formula $\nabla\pi(p)=y(p)$
\end_inset

.
 If 
\begin_inset Formula $\pi$
\end_inset

 is twice differentiable,
 
\begin_inset Formula $D_py(p)=D_p^2\pi(p)$
\end_inset

 is symmetric and positive semidefinite and satisfies 
\begin_inset Formula $D_py(p)p=0$
\end_inset

.
\end_layout

\begin_layout Standard
These statements follow from the supremum representation of 
\begin_inset Formula $\pi$
\end_inset

,
 Euler's theorem for a degree-one function,
 and the envelope theorem.
 If the supremum is infinite or unattained,
 the corresponding supply statement is not defined and should not be used.
\end_layout
'''


def main() -> None:
    text = BOOK.read_text()
    start = text.index("\\begin_layout Proposition\n(Properties of the profit function)")
    end = text.index("\\begin_layout Standard\nProperty (viii) can also be stated", start)
    text = text[:start] + BLOCK.rstrip() + "\n\n" + text[end:]
    BOOK.write_text(text)


if __name__ == "__main__":
    main()
