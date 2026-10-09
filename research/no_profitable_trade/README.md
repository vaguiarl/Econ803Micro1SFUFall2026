# No Profitable Trade

This folder contains the brainstorming paper **“No Profitable Trade: From KKT to Revealed Preference.”** It develops the support-gap view of concave optimization, recovers KKT multipliers from the one-budget closed form, and connects the resulting local certificates to Afriat inequalities, GARP, cyclic monotonicity, CMU blocking, stochastic choice, and continuum goods.

- [LaTeX source](No_Profitable_Trade_From_KKT_to_Revealed_Preference.tex)
- [Compiled PDF](../../output/pdf/No_Profitable_Trade_From_KKT_to_Revealed_Preference.pdf)

The manuscript is deliberately labeled a research agenda. Its final ledger separates established results, interpretive synthesis, candidate diagnostics, and open questions; it does not claim that the underlying KKT, Frank--Wolfe, Afriat, or cyclic-monotonicity results are new.

Build from the repository root with:

```sh
latexmk -xelatex -interaction=nonstopmode -halt-on-error \
  -outdir=output/pdf \
  research/no_profitable_trade/No_Profitable_Trade_From_KKT_to_Revealed_Preference.tex
```
