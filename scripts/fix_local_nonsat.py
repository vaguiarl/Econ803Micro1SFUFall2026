from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"
s = path.read_text()
start_marker = r"""\begin_layout Definition
Local Nonsatiation"""
start = s.index(start_marker)
end = s.index(r"""\begin_layout Section
KKT Conditions for the UMP""", start)
replacement = r'''\begin_layout Definition
Local nonsatiation.
 A preference relation \begin_inset Formula $\succeq$\end_inset
 is locally nonsatiated if, for every \begin_inset Formula $x\in X$\end_inset
 and every \begin_inset Formula $\varepsilon>0$\end_inset
,
 there is \begin_inset Formula $y\in X$\end_inset
 with \begin_inset Formula $\lVert y-x\rVert<\varepsilon$\end_inset
 and \begin_inset Formula $y\succ x$\end_inset
.
\end_layout

\begin_layout Proposition
If a locally nonsatiated utility function generates the Marshallian demand correspondence, then every demanded bundle exhausts the budget: \begin_inset Formula $p\cdot x=w$\end_inset
 for every \begin_inset Formula $x\in x(p,w)$\end_inset
.
\end_layout

\begin_layout Standard
Proof.  If \begin_inset Formula $p\cdot x<w$\end_inset
,
 local nonsatiation supplies a strictly preferred bundle arbitrarily close to \begin_inset Formula $x$\end_inset
.
 For a sufficiently small neighborhood the bundle remains affordable, contradicting utility maximization.  Therefore the budget constraint binds.
\end_layout

\begin_layout Proposition
The same demand correspondence is homogeneous of degree zero.  If preferences are convex, demand is convex-valued; if preferences are strictly convex, demand is single-valued.
\end_layout

'''
path.write_text(s[:start] + replacement + s[end:])
print("repaired local-nonsatiation statement and proof")
