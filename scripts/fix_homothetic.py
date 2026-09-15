from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"
s = path.read_text()
start_marker = r"""\begin_layout Definition
Homothetic preferences."""
start = s.index(start_marker)
end = s.index(r"""\begin_layout Standard
Examples:""", start)
block = r'''\begin_layout Definition
Homothetic preferences.
 A preference relation is homothetic if \begin_inset Formula $x\succeq y$\end_inset
 implies \begin_inset Formula $\alpha x\succeq\alpha y$\end_inset
 for every \begin_inset Formula $\alpha>0$\end_inset
 whenever the scaled bundles are feasible.
 Under the usual continuity and monotonicity assumptions, it admits a positively homogeneous utility representation; an arbitrary representation need not itself be homogeneous.
\end_layout

\begin_layout Standard
The Cobb--Douglas representation \begin_inset Formula $u(x_{1},x_{2})=x_{1}^{\alpha}x_{2}^{1-\alpha}$\end_inset
 is a standard example.
\end_layout

'''
s = s[:start] + block + s[end:]
# Remove the now-redundant quasilinear summary paragraph, retaining the definition.
old = r'''\begin_layout Standard
The utility function for quasilinear cases are 
\begin_inset Formula $u(x)=V(x_{1},\cdots,x_{L-1})+x_{L}$
\end_inset

.
\end_layout

'''
s = s.replace(old, "", 1)
duplicate = r'''\begin_layout Standard
Examples:
 Cobb-Douglas 
\begin_inset Formula $u(x_{1},x_{2})=x_{1}^{\alpha}x_{2}^{1-\alpha}$
\end_inset

.
 
\end_layout

'''
s = s.replace(duplicate, "", 1)
path.write_text(s)
print("repaired homothetic definition")
