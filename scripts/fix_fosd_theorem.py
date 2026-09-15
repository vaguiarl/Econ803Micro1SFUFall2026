from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"
s = path.read_text()
start = s.index(r"""\begin_layout Theorem
If 
\begin_inset Formula $F\succeq^{FOSD}G$""")
end = s.index(r"""\begin_layout Standard
\begin_inset Formula $F\succeq^{FOSD}G$""", start)
block = r'''\begin_layout Theorem
First-order stochastic dominance.
 If \begin_inset Formula $F\succeq^{FOSD}G$\end_inset
,
 then \begin_inset Formula $\int u\,dF\geq\int u\,dG$\end_inset
 for every increasing Bernoulli utility \begin_inset Formula $u$\end_inset
 for which the integrals exist.  Strict dominance together with strict monotonicity yields a strict inequality under the usual support conditions.
\end_layout

'''
s = s[:start] + block + s[end:]
path.write_text(s)
print("fixed FOSD theorem")
