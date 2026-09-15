#!/usr/bin/env python3
"""Replace the unfinished late-chapter blocks with concise, checked statements.

The Fall 2024 source contains several lecture-draft blocks in the chapters on
revealed equilibrium, sequential trade, matching, and CGE.  This script keeps
the surrounding LyX file intact while replacing those blocks with statements
whose domains, quantifiers, and equilibrium conventions are explicit.  Deep
results are labelled as cited theorems rather than presented with incomplete
proofs.
"""

from pathlib import Path
import sys


BOOK = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"


TESTABLE = r'''\begin_layout Chapter
Testable Restrictions on the Equilibrium Manifold
\end_layout

\begin_layout Standard
This chapter studies what a finite set of market observations can reveal about a pure-trade economy.
 The central tension is between individual utility maximization and market clearing:
 each consumer must rationalize their own choices,
 while the choices must add up to the observed aggregate endowment.
\end_layout

\begin_layout Section
Observables and the equilibrium manifold
\end_layout

\begin_layout Standard
Fix a finite set of consumers \begin_inset Formula $i=1,\ldots,I$\end_inset ,
 goods \begin_inset Formula $\ell=1,\ldots,L$\end_inset ,
 and observations \begin_inset Formula $t=1,\ldots,T$\end_inset .
 At observation \begin_inset Formula $t$\end_inset ,
 let \begin_inset Formula $p^{t}\in\mathbb{R}_{++}^{L}$\end_inset denote the price vector and let \begin_inset Formula $\omega_{i}^{t}\in\mathbb{R}_{+}^{L}$\end_inset denote consumer \begin_inset Formula $i$\end_inset 's endowment.
 Prices are normalized because only their positive scale is economically relevant.
\end_layout

\begin_layout Definition
(Pure-trade rationalization.)
 A finite dataset is rationalized by a pure-trade economy if there are continuous,
 locally nonsatiated,
 concave utility functions \begin_inset Formula $u_i$\end_inset and bundles \begin_inset Formula $x_i^t\in\mathbb{R}_{+}^{L}$\end_inset such that, for every \begin_inset Formula $i,t$\end_inset ,
 \begin_inset Formula $x_i^t\in\arg\max\{u_i(x):p^t\cdot x\leq p^t\cdot\omega_i^t\}$\end_inset ,
 and, for every \begin_inset Formula $t$\end_inset ,
 \begin_inset Formula $\sum_i x_i^t=\sum_i\omega_i^t$\end_inset .
\end_layout

\begin_layout Definition
(Equilibrium manifold.)
 For a market excess-demand function \begin_inset Formula $F(\hat\omega,p)$\end_inset ,
 where \begin_inset Formula $\hat\omega=(\omega_1,\ldots,\omega_I)$\end_inset ,
 the equilibrium manifold is
 \begin_inset Formula $\mathcal{M}=\{(\hat\omega,p):F(\hat\omega,p)=0\}$\end_inset .
 It records pairs of endowment profiles and prices that can clear markets for the fixed underlying preferences.
\end_layout

\begin_layout Section
Afriat inequalities and elimination of unobservables
\end_layout

\begin_layout Standard
For a finite collection of observed or latent bundles, Afriat's inequalities are the linear inequalities
\begin_inset Formula $u_i^t\leq u_i^s+\lambda_i^s p^s\cdot(x_i^t-x_i^s)$\end_inset
 for all \begin_inset Formula $s,t$\end_inset ,
 with \begin_inset Formula $\lambda_i^s>0$\end_inset .
 They are equivalent to the existence of a monotone,
 concave utility representation for the finite choice data.
\end_layout

\begin_layout Standard
The equilibrium restrictions combine these inequalities with the budget inequalities
\begin_inset Formula $p^t\cdot x_i^t\leq p^t\cdot\omega_i^t$\end_inset
 and the market-clearing equalities
\begin_inset Formula $\sum_i x_i^t=\sum_i\omega_i^t$\end_inset .
 The \begin_inset Formula $x_i^t,u_i^t,\lambda_i^t$\end_inset variables are unobserved;
 prices and the endowment profile are the data in the design considered here.
\end_layout

\begin_layout Standard
(Tarski--Seidenberg theorem.)
 The projection of a semialgebraic set is semialgebraic.
 Consequently,
 eliminating the unobserved variables from any finite polynomial system yields a quantifier-free semialgebraic condition in the observables.
 This theorem supplies an elimination principle;
 it does not say that the resulting restrictions are easy to compute or that every model has a nontrivial restriction.
\end_layout

\begin_layout Section
Brown--Matzkin theorem
\end_layout

\begin_layout Standard
Brown and Matzkin (1996) apply this principle to pure-trade equilibrium.
 Under their regularity and invariance assumptions,
 finite observations on prices,
 individual incomes or endowments,
 and aggregate endowments are rationalizable if and only if they satisfy a finite family of semialgebraic restrictions obtained after eliminating the latent utility levels,
 marginal utilities of income,
 and consumption bundles.
 The restrictions are nontrivial:
 some finite datasets cannot lie on the equilibrium manifold of any economy in the maintained class.
 The result is cited here;
 its quantifier-elimination construction is not reproved in this text.
\end_layout

\begin_layout Standard
The theorem should not be confused with the Sonnenschein--Mantel--Debreu result.
 The latter concerns the flexibility of aggregate excess demand when individual preferences are allowed to vary;
 Brown--Matzkin hold the individual preferences fixed across observations and exploit observed endowment changes.
\end_layout
'''


SEQUENTIAL = r'''\begin_layout Chapter
Sequential Trade
\end_layout

\begin_layout Section
Arrow--Debreu benchmark
\end_layout

\begin_layout Standard
There are \begin_inset Formula $S$\end_inset states and \begin_inset Formula $L$\end_inset goods in each state.
 Consumer \begin_inset Formula $i$\end_inset has state-contingent endowment \begin_inset Formula $\omega_i=(\omega_{i1},\ldots,\omega_{iS})$\end_inset and preference \begin_inset Formula $\succeq_i$\end_inset over contingent consumption plans \begin_inset Formula $x_i=(x_{i1},\ldots,x_{iS})$\end_inset .
\end_layout

\begin_layout Definition
(Arrow--Debreu equilibrium.)
 Prices \begin_inset Formula $p=(p_1,\ldots,p_S)\in(\mathbb{R}_{++}^{L})^{S}$\end_inset and an allocation \begin_inset Formula $x^*=(x_1^*,\ldots,x_I^*)$\end_inset form an Arrow--Debreu equilibrium if, for each consumer,
 \begin_inset Formula $x_i^*$\end_inset maximizes \begin_inset Formula $\succeq_i$\end_inset over
 \begin_inset Formula $B_i^{AD}(p)=\{x_i:\sum_{s=1}^{S}p_s\cdot x_{is}\leq\sum_{s=1}^{S}p_s\cdot\omega_{is}\}$\end_inset ,
 and markets clear state by state:
 \begin_inset Formula $\sum_i x_{is}^*=\sum_i\omega_{is}$\end_inset for every \begin_inset Formula $s$\end_inset .
\end_layout

\begin_layout Section
Spot markets and sequential trade
\end_layout

\begin_layout Standard
Suppose contingent commodity markets are unavailable at date \begin_inset Formula $t=0$\end_inset .
 There are \begin_inset Formula $K$\end_inset tradable assets with payoff matrix \begin_inset Formula $R\in\mathbb{R}^{S\times K}$\end_inset :
 one unit of asset \begin_inset Formula $k$\end_inset pays \begin_inset Formula $R_{sk}$\end_inset units of the first good in state \begin_inset Formula $s$\end_inset .
 Asset prices are \begin_inset Formula $q\in\mathbb{R}^{K}$\end_inset ,
 and spot-good prices in state \begin_inset Formula $s$\end_inset are \begin_inset Formula $p_s\in\mathbb{R}_{++}^{L}$\end_inset .
\end_layout

\begin_layout Definition
(Radner budget set.)
 Given asset holdings \begin_inset Formula $z_i\in\mathbb{R}^{K}$\end_inset and state-contingent consumption \begin_inset Formula $x_i$\end_inset ,
 consumer \begin_inset Formula $i$\end_inset satisfies
 \begin_inset Formula $q\cdot z_i\leq0$\end_inset and
 \begin_inset Formula $p_s\cdot x_{is}\leq p_s\cdot\omega_{is}+p_{s1}(Rz_i)_s$\end_inset for every \begin_inset Formula $s$\end_inset .
 The zero on the date-0 constraint is the normalization of zero initial asset endowment.
\end_layout

\begin_layout Definition
(Radner equilibrium.)
 A price system \begin_inset Formula $(q,p_1,\ldots,p_S)$\end_inset and plans \begin_inset Formula $(z_i^*,x_i^*)_{i=1}^{I}$\end_inset form a Radner equilibrium when every consumer maximizes their preference over the Radner budget set,
 asset markets clear \begin_inset Formula $\sum_i z_i^*=0$\end_inset ,
 and goods markets clear in every state:
 \begin_inset Formula $\sum_i x_{is}^*=\sum_i\omega_{is}$\end_inset for all \begin_inset Formula $s$\end_inset .
\end_layout

\begin_layout Proposition
(Arrow--Radner equivalence, cited.)
 If the payoff matrix has full row rank \begin_inset Formula $\operatorname{rank}(R)=S$\end_inset and the standard no-arbitrage,
 continuity,
 and monotonicity assumptions hold,
 the sets of consumption allocations supported by Arrow--Debreu and Radner equilibria coincide.
 If \begin_inset Formula $\operatorname{rank}(R)<S$\end_inset ,
 some contingent trades are unattainable and the equivalence need not hold.
\end_layout

\begin_layout Standard
The full-rank condition is the precise meaning of complete asset markets in this finite-state model.
 The equivalence theorem is cited rather than reproved;
 the proof constructs state prices from asset prices and uses the spanning property of \begin_inset Formula $R$\end_inset .
\end_layout
'''


MATCHING = r'''\begin_layout Chapter
Matching
\end_layout

\begin_layout Section
One-to-one matching
\end_layout

\begin_layout Standard
Let \begin_inset Formula $M$\end_inset and \begin_inset Formula $W$\end_inset be finite sets of agents.
 Each agent has a strict preference ordering over the agents on the other side and the option of remaining unmatched.
 A matching \begin_inset Formula $\mu$\end_inset assigns each agent either an acceptable partner or themselves,
 and satisfies \begin_inset Formula $\mu(\mu(a))=a$\end_inset .
\end_layout

\begin_layout Definition
(Stability.)
 A matching is individually rational if no agent is matched with an unacceptable partner.
 A pair \begin_inset Formula $(m,w)$\end_inset not matched to one another blocks \begin_inset Formula $\mu$\end_inset if \begin_inset Formula $w\succ_m\mu(m)$\end_inset and \begin_inset Formula $m\succ_w\mu(w)$\end_inset .
 A matching is stable when it is individually rational and has no blocking pair.
\end_layout

\begin_layout Section
Deferred acceptance
\end_layout

\begin_layout Standard
In the men-proposing deferred-acceptance algorithm,
 each unmatched man proposes to the most-preferred woman who has not rejected him.
 Each woman tentatively holds her most-preferred acceptable proposal received so far and rejects the rest.
 The process stops when no proposal is rejected.
\end_layout

\begin_layout Theorem
(Gale--Shapley theorem, cited.)
 For every finite marriage problem,
 deferred acceptance terminates and returns a stable matching.
 Among all stable matchings,
 the outcome is weakly best for every man and weakly worst for every woman.
\end_layout

\begin_layout Standard
Termination is finite because a man proposes to each woman at most once.
 The stability and proposer-optimality statements are the Gale--Shapley theorem;
 they are cited here rather than accompanied by an incomplete proof.
\end_layout

\begin_layout Section
Housing markets and top trading cycles
\end_layout

\begin_layout Standard
In a housing market,
 each agent initially owns one house and has a strict preference over houses.
 The core consists of allocations for which no coalition can make every member weakly better off and at least one member strictly better off using only the houses owned by that coalition.
\end_layout

\begin_layout Standard
The top-trading-cycles algorithm directs each agent to point to their favorite remaining house and each house to point to its owner.
 Every directed cycle is executed,
 the participating houses and agents are removed,
 and the procedure is repeated.
\end_layout

\begin_layout Theorem
(Top-trading-cycles theorem, cited.)
 With strict preferences and one-house ownership,
 top trading cycles terminates,
 is Pareto efficient,
 and returns an allocation in the core of the housing market.
\end_layout
'''


CGE = r'''\begin_layout Chapter
Computable General Equilibrium
\end_layout

\begin_layout Section
From accounts to counterfactuals
\end_layout

\begin_layout Standard
Computable general equilibrium (CGE) analysis uses a calibrated microeconomic model and a social accounting matrix to evaluate policy counterfactuals.
 Calibration chooses parameters so that the model reproduces a benchmark allocation and the associated accounting identities before the policy is changed.
\end_layout

\begin_layout Section
A two-sector small open economy
\end_layout

\begin_layout Standard
The benchmark economy has two goods,
 labor \begin_inset Formula $L$\end_inset ,
 and sector-specific capital \begin_inset Formula $K_i$\end_inset .
 A small open economy takes world prices as given.
 For sector \begin_inset Formula $i$\end_inset ,
 a constant-elasticity-of-substitution production function is
\begin_inset Formula $Q_i=A_i[\alpha_iK_i^{-\rho_i}+(1-\alpha_i)L_i^{-\rho_i}]^{-1/\rho_i}$\end_inset ,
 with \begin_inset Formula $A_i>0$\end_inset ,
 \begin_inset Formula $0<\alpha_i<1$\end_inset ,
 and \begin_inset Formula $\rho_i\ne0$\end_inset .
 The associated elasticity parameter is \begin_inset Formula $\sigma_i=1/(1+\rho_i)$\end_inset whenever \begin_inset Formula $1+\rho_i\ne0$\end_inset .
\end_layout

\begin_layout Definition
(Cost and conditional factor demand.)
 Given output \begin_inset Formula $\bar Q_i$\end_inset and factor prices \begin_inset Formula $(r_i,W)$\end_inset ,
 the unit-consistent cost function is
\begin_inset Formula $c_i(r_i,W,\bar Q_i)=\min_{K,L}\{r_iK+WL:Q_i(K,L)\geq\bar Q_i\}$\end_inset .
 When differentiable,
 conditional factor demands satisfy \begin_inset Formula $K_i^D=\partial c_i/\partial r_i$\end_inset and \begin_inset Formula $L_i^D=\partial c_i/\partial W$\end_inset .
 This derivative formulation avoids confusing the price \begin_inset Formula $P_i$\end_inset with the CES parameter \begin_inset Formula $\rho_i$\end_inset .
\end_layout

\begin_layout Section
Social accounting and calibration
\end_layout

\begin_layout Standard
The social accounting matrix records production,
 factor payments,
 household income,
 and expenditure flows that must balance at the benchmark.
 For a Cobb--Douglas expenditure equation \begin_inset Formula $P_iQ_{h,i}^D=\beta_{h,i}Y_h$\end_inset ,
 the observed benchmark share identifies \begin_inset Formula $\beta_{h,i}=P_iQ_{h,i}^D/Y_h$\end_inset .
 The calibrated model is checked by substituting the parameter values back into every accounting identity and market-clearing condition.
\end_layout

\begin_layout Section
Counterfactual policies
\end_layout

\begin_layout Standard
For an imported good \begin_inset Formula $i$\end_inset ,
 let \begin_inset Formula $ER$\end_inset be the exchange rate and \begin_inset Formula $PW_i$\end_inset the world price.
 A tariff rate \begin_inset Formula $\tau_i\geq0$\end_inset changes the domestic price according to
\begin_inset Formula $P_i=ER\cdot PW_i(1+\tau_i)$\end_inset .
 Free trade is the baseline \begin_inset Formula $\tau_i=0$\end_inset ;
 a tariff counterfactual changes \begin_inset Formula $\tau_i$\end_inset and resolves the full equilibrium system.
 Other counterfactuals change tax,
 subsidy,
 transfer,
 or technology equations while leaving the accounting identities and calibrated preference and technology parameters in place.
\end_layout
'''


APPENDIX_MARKER = r'''\begin_layout Standard
\begin_inset ERT
status open

\begin_layout Plain Layout


\backslash
appendix'''


def replace_between(text: str, start: str, end: str, replacement: str) -> str:
    left = text.find(start)
    if left < 0:
        raise RuntimeError(f"start marker not found: {start!r}")
    right = text.find(end, left + len(start))
    if right < 0:
        raise RuntimeError(f"end marker not found: {end!r}")
    return text[:left] + replacement.rstrip() + "\n\n" + text[right:]


def main() -> None:
    path = Path(sys.argv[1]) if len(sys.argv) > 1 else BOOK
    text = path.read_text()
    text = replace_between(
        text,
        "\\begin_layout Chapter\nTestable Restrictions on the Equilibrium Manifold",
        "\\begin_layout Chapter\nSequential Trade",
        TESTABLE,
    )
    text = replace_between(
        text,
        "\\begin_layout Chapter\nSequential Trade",
        "\\begin_layout Chapter\nMatching",
        SEQUENTIAL,
    )
    text = replace_between(
        text,
        "\\begin_layout Chapter\nMatching",
        "\\begin_layout Chapter\nComputable General Equilibrium (CGE)",
        MATCHING,
    )
    text = replace_between(
        text,
        "\\begin_layout Chapter\nComputable General Equilibrium (CGE)",
        APPENDIX_MARKER,
        CGE,
    )
    path.write_text(text)


if __name__ == "__main__":
    main()
