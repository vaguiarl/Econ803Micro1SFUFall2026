from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"
s = path.read_text()
orphan = r'''\begin_layout Standard
In particular,
 \begin_inset Formula $e_{1}^{\top}S(p,w)e_{1}=1>0$
\end_inset

, so this demand violates the compensated law of demand and WARP.
\end_layout

'''
if orphan not in s:
    print("orphan paragraph not found")
else:
    s = s.replace(orphan, "", 1)
    path.write_text(s)
    print("removed orphan Slutsky paragraph")
