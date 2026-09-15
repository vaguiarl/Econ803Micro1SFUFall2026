from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"
s = path.read_text()
start_marker = r"""\begin_layout Subsubsection*
Ramen noodles vs.
 meat.
 
\end_layout"""
end_marker = r"""\begin_layout Chapter
Preference and Choice
\end_layout"""
start = s.index(start_marker)
end = s.index(end_marker, start)
replacement = r'''\begin_layout Subsubsection*
Marshallian and compensated price effects
\end_layout

\begin_layout Standard
The Slutsky decomposition separates the total response of demand to a price change from the response at fixed purchasing power.  For a differentiable demand function,
\end_layout

\begin_layout Standard
\begin_inset Formula 
\[
\partial_{p_k}x_\ell(p,w)=S_{\ell k}(p,w)-x_k(p,w)\,\partial_w x_\ell(p,w).
\]
\end_inset
\end_layout

\begin_layout Standard
Under WARP and Walras' law the compensated matrix has a negative-semidefinite symmetric part.  Thus a positive Marshallian own-price derivative \begin_inset Formula $\partial_{p_\ell}x_\ell>0$\end_inset
 is possible only when the income effect is sufficiently adverse: the good is inferior (\begin_inset Formula $\partial_w x_\ell<0$\end_inset
), and the income effect dominates the nonpositive compensated effect.  This is the Giffen mechanism.
\end_layout

\begin_layout Standard
The possibility of a Giffen response does not by itself establish a utility representation.  To derive one from data, impose and test the full integrability conditions developed later: budget exhaustion, homogeneity, WARP (or the stronger GARP on finite data), and the relevant regularity assumptions.  The compensated response, rather than the Marshallian derivative alone, is the object restricted by revealed preference.
\end_layout

'''
path.write_text(s[:start] + replacement + s[end:])
print(f"replaced Giffen illustration in {path}")
