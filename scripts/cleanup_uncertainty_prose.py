from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"
s = path.read_text()
s = s.replace("when \n\\begin_inset Formula $U$\\end_inset\n\n is expected utility (\n\\begin_inset Formula $u$\\end_inset\n\n is strictly increasing \n\\begin_inset Formula $\\succ$\\end_inset\n\n and increasing \n\\begin_inset Formula $\\succeq$\\end_inset\n\n).", "for every expected-utility representation with an increasing Bernoulli utility.")
s = s.replace("This follows from \n\\bar under\n\n\\begin_inset Formula $u'(w)>0$", "Because \n\\begin_inset Formula $u'(w)>0$")
s = s.replace("there exists a \n\\begin_inset Formula $u:Z\\to\\mathbb{R}$\\end_inset\n\n bounded and continuous such that", "there exists a bounded continuous function \n\\begin_inset Formula $u:Z\\to\\mathbb{R}$\\end_inset\n\n such that")
path.write_text(s)
print("cleaned uncertainty prose")
