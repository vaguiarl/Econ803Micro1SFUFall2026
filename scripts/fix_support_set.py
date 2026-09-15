from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"
s = path.read_text()
start = s.index("The definition already gives the exact criterion:")
end = s.index("\\begin_layout Section\nUpper Bounds for Welfare Analysis", start)
replacement = r'''The definition already gives the exact criterion: a candidate bundle belongs to the support set if it exhausts the new budget and the augmented dataset satisfies GARP.
 The transitive closure must be checked, not only one-step comparisons.
 Whenever an old bundle \begin_inset Formula $x^{t}$\end_inset
 is indirectly revealed preferred to the candidate, GARP requires
\begin_inset Formula $p^{K+1}\cdot x\leq p^{K+1}\cdot x^{t}$\end_inset
.
\end_layout

'''
path.write_text(s[:start] + replacement + s[end:])
print("Repaired Varian support-set explanation")
