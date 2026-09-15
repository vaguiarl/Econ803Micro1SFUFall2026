from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"
s = path.read_text()
section_start = s.index(r"""\begin_layout Section
Properties of the Indirect Utility Function
\end_layout""")
proof_start = s.index(r"""\begin_layout Standard
\begin_inset ERT
status open""", section_start)
proof_end = s.index(r"""\begin_layout Section
Roy's Identity""", proof_start)
replacement = r'''\begin_layout Standard
Proof.  Existence, homogeneity, monotonicity, and continuity follow from the compact budget correspondence and Berge's maximum theorem.
\end_layout

\begin_layout Standard
For quasiconvexity, fix \begin_inset Formula $\overline v$\end_inset
 and let \begin_inset Formula $L_{\overline v}=\{(p,w):v(p,w)\leq\overline v\}$\end_inset
.
 If \begin_inset Formula $u(x)>\overline v$\end_inset
,
 then every \begin_inset Formula $(p,w)\in L_{\overline v}$\end_inset
 must satisfy \begin_inset Formula $p\cdot x>w$\end_inset
,
 because otherwise \begin_inset Formula $x$\end_inset
 would be affordable and the value would exceed \begin_inset Formula $\overline v$\end_inset
.
 Conversely, this strict inequality for every \begin_inset Formula $x$\end_inset
 with \begin_inset Formula $u(x)>\overline v$\end_inset
 rules out an affordable bundle with utility above \begin_inset Formula $\overline v$\end_inset
.
 Hence
\end_layout

\begin_layout Standard
\begin_inset Formula 
\[
L_{\overline v}=\bigcap_{u(x)>\overline v}\{(p,w):p\cdot x>w\}.
\]
\end_inset
\end_layout

\begin_layout Standard
Each set in the intersection is a linear half-space in \begin_inset Formula $(p,w)$\end_inset
,
 so the lower contour set is convex and \begin_inset Formula $v$\end_inset
 is quasiconvex.
\end_layout

'''
path.write_text(s[:proof_start] + replacement + s[proof_end:])
print("fixed indirect-utility proof layout")
