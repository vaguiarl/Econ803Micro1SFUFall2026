from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"
s = path.read_text()
s = s.replace("Consumer's \n\\begin_inset Formula $i$\\end_inset", "Consumer \\begin_inset Formula $i$\\end_inset")
s = s.replace("where \n\\begin_inset Formula $\\omega_{l}=\\sum_{i\\in I}\\omega_{li}$", "where \n\\begin_inset Formula $\\omega_{l}=\\sum_{i=1}^{I}\\omega_{i,l}$")
s = s.replace("and price vector \n\\begin_inset Formula $p\\in\\mathbb{R}^{L}$", "and a strictly positive price vector \n\\begin_inset Formula $p\\gg0$")
s = s.replace("We study an economy with two goods,\n good", "We study an economy with two goods: good")
s = s.replace("each consumer has a quasilinear utility", "and each consumer has quasilinear utility")
s = s.replace("is small relatively to the whole expenditure", "is small relative to total expenditure")
s = s.replace("The Second Fundamental Theorem of Welfare Economics) For any Pareto optimal levels of utility", "The Second Fundamental Theorem of Welfare Economics) Under the same convexity, continuity, and interiority assumptions, any Pareto-optimal utility vector")
s = s.replace("satisfiy", "satisfy")
s = s.replace("satisfies the market clearing condition", "satisfies market clearing")
s = s.replace("and if the consumers' budget constraints so that", "and if the consumers' budgets satisfy")
path.write_text(s)
print("cleaned competitive-market prose")
