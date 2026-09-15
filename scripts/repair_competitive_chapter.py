from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"
s = path.read_text()
start_marker = r"""\begin_layout Chapter
Competitive Markets and Partial Equilibrium
\end_layout"""
end_marker = r"""\begin_layout Chapter
General Equilibrium Theory
\end_layout"""
start = s.index(start_marker)
end = s.index(end_marker, start)

chapter = r'''\begin_layout Chapter
Competitive Markets and Partial Equilibrium
\end_layout

\begin_layout Standard
This chapter collects the competitive-equilibrium definitions used later and develops a transparent partial-equilibrium model with a numeraire.  The partial-equilibrium model is deliberately specialized: its quasilinear preferences remove income effects for the good of interest.
\end_layout

\begin_layout Section
Competitive equilibrium
\end_layout

\begin_layout Standard
There are \begin_inset Formula $I$\end_inset
 consumers, \begin_inset Formula $J$\end_inset
 firms, and \begin_inset Formula $L$\end_inset
 goods.  Consumer \begin_inset Formula $i$\end_inset
 has consumption set \begin_inset Formula $X_i\subseteq\mathbb{R}^{L}$\end_inset
, preference relation \begin_inset Formula $\succeq_i$\end_inset
, and endowment \begin_inset Formula $\omega_i\in\mathbb{R}^{L}$\end_inset
.  Firm \begin_inset Formula $j$\end_inset
 has production set \begin_inset Formula $Y_j\subseteq\mathbb{R}^{L}$\end_inset
, where positive coordinates are net outputs and negative coordinates are inputs.  Let \begin_inset Formula $\omega=\sum_i\omega_i$\end_inset
.
\end_layout

\begin_layout Definition
Feasibility.  An allocation \begin_inset Formula $(x_1,\ldots,x_I;y_1,\ldots,y_J)$\end_inset
 is feasible when \begin_inset Formula $x_i\in X_i$\end_inset
, \begin_inset Formula $y_j\in Y_j$\end_inset
, and
\begin_inset Formula 
\[
 \sum_{i=1}^{I}x_i\leq\omega+\sum_{j=1}^{J}y_j.
\]
\end_inset
 Equality is imposed when all goods have strictly positive prices and free disposal is not used.
\end_layout

\begin_layout Definition
Competitive (Walrasian) equilibrium.  A strictly positive price vector \begin_inset Formula $p\gg0$\end_inset
 and a feasible allocation \begin_inset Formula $(x^*,y^*)$\end_inset
 form an equilibrium if every firm solves
\begin_inset Formula 
\[
 y_j^*\in\arg\max_{y_j\in Y_j}p\cdot y_j
\]
\end_inset
 and every consumer solves
\begin_inset Formula 
\[
 x_i^*\in\arg\max_{x_i\in X_i}\{u_i(x_i):p\cdot x_i\leq p\cdot\omega_i+\sum_j\theta_{ij}p\cdot y_j^*\}.
\]
\end_inset
 Ownership shares satisfy \begin_inset Formula $\theta_{ij}\geq0$\end_inset
 and \begin_inset Formula $\sum_i\theta_{ij}=1$\end_inset
 for each firm.
\end_layout

\begin_layout Proposition
Price normalization and Walras' law.  If \begin_inset Formula $(p,x^*,y^*)$\end_inset
 is a competitive equilibrium, then so is \begin_inset Formula $(\lambda p,x^*,y^*)$\end_inset
 for every \begin_inset Formula $\lambda>0$\end_inset
.  If consumers exhaust their budgets, summing the budget equalities and using market clearing gives
\begin_inset Formula 
\[
 p\cdot\left(\sum_i x_i^* -\omega-\sum_j y_j^*\right)=0.
\]
\end_inset
 Therefore, if all but one market clear, the last market clears as well.
\end_layout

\begin_layout Section
Partial equilibrium with a numeraire
\end_layout

\begin_layout Standard
There are two goods.  Good \begin_inset Formula $x$\end_inset
 is the good of interest and \begin_inset Formula $m$\end_inset
 is a numeraire with price one.  Consumer \begin_inset Formula $i$\end_inset
 has
\begin_inset Formula 
\[
 u_i(m_i,x_i)=m_i+\phi_i(x_i),\qquad X_i=\mathbb{R}\times\mathbb{R}_{+},
\]
\end_inset
 where \begin_inset Formula $\phi_i$\end_inset
 is increasing, strictly concave, twice continuously differentiable, and bounded above.  Let \begin_inset Formula $p>0$\end_inset
 be the price of \begin_inset Formula $x$\end_inset
.
\end_layout

\begin_layout Standard
Firm \begin_inset Formula $j$\end_inset
 produces \begin_inset Formula $q_j\geq0$\end_inset
 units of \begin_inset Formula $x$\end_inset
 at numeraire cost \begin_inset Formula $c_j(q_j)$\end_inset
.  Its net-output set is
\begin_inset Formula 
\[
 Y_j=\{(-z_j,q_j):q_j\geq0,\ z_j\geq c_j(q_j)\}.
\]
\end_inset
 Assume \begin_inset Formula $c_j$\end_inset
 is increasing, strictly convex, twice continuously differentiable, and \begin_inset Formula $c_j'(q)\to\infty$\end_inset
 as \begin_inset Formula $q\to\infty$\end_inset
.
\end_layout

\begin_layout Definition
Partial competitive equilibrium.  A price \begin_inset Formula $p$\end_inset
 and quantities \begin_inset Formula $(x_1,\ldots,x_I;q_1,\ldots,q_J)$\end_inset
 form an equilibrium when
\begin_inset Formula 
\[
 \phi_i'(x_i)\leq p,\quad x_i>0\Rightarrow\phi_i'(x_i)=p,
\]
\end_inset
\begin_inset Formula 
\[
 p\leq c_j'(q_j),\quad q_j>0\Rightarrow p=c_j'(q_j),
\]
\end_inset
 and the market for \begin_inset Formula $x$\end_inset
 clears:
\begin_inset Formula 
\[
 \sum_i x_i=\sum_j q_j.
\]
\end_inset
 These are the KKT conditions for consumer and firm optimization plus market clearing.
\end_layout

\begin_layout Standard
Equivalently, the unique choices are characterized by
\begin_inset Formula 
\[
 x_i(p)=\arg\max_{x\geq0}\{\phi_i(x)-px\},\qquad
 q_j(p)=\arg\max_{q\geq0}\{pq-c_j(q)\}.
\]
\end_inset
 The associated aggregate excess demand is \begin_inset Formula $Z(p)=\sum_i x_i(p)-\sum_j q_j(p)$\end_inset
.
\end_layout

\begin_layout Proposition
Existence and uniqueness in the partial model.  Suppose
\begin_inset Formula $\max_i\phi_i'(0)>\min_j c_j'(0)$
\end_inset
 and the preceding curvature and tail assumptions hold.  Then \begin_inset Formula $Z$\end_inset
 is continuous and nonincreasing, supply is continuous and nondecreasing, and there is at least one \begin_inset Formula $p^*\in[\min_j c_j'(0),\max_i\phi_i'(0)]$\end_inset
 with \begin_inset Formula $Z(p^*)=0$\end_inset
.  If at least one active side has strict curvature at the equilibrium, the equilibrium price is unique; otherwise the zero set can be an interval.
\end_layout

\begin_layout Standard
To see the sign change, at a price no larger than \begin_inset Formula $\min_j c_j'(0)$\end_inset
 all firms choose zero output while at least one consumer demands a positive amount.  At a price at least \begin_inset Formula $\max_i\phi_i'(0)$\end_inset
 all consumers choose zero while at least one firm supplies a positive amount.  The intermediate value theorem then gives a clearing price.
\end_layout

\begin_layout Standard
The numeraire allocation is recovered from the budget identity
\begin_inset Formula 
\[
 m_i=\omega_{mi}+\sum_j\theta_{ij}\bigl(pq_j-c_j(q_j)\bigr)-px_i.
\]
\end_inset
 Partial equilibrium deliberately suppresses the wealth effects that would reappear with general preferences or additional markets.
\end_layout

\begin_layout Section
Welfare in the partial model
\end_layout

\begin_layout Definition
Pareto efficiency.  A feasible allocation is Pareto efficient if no other feasible allocation makes every consumer weakly better off and at least one consumer strictly better off.
\end_layout

\begin_layout Proposition
First welfare theorem for the quasilinear model (cited).  A competitive allocation is Pareto efficient under the stated convexity and local nonsatiation assumptions.
\end_layout

\begin_layout Standard
The planner's problem is
\begin_inset Formula 
\[
 \max_{x_i,q_j\geq0}\left\{\sum_i\phi_i(x_i)-\sum_jc_j(q_j)\right\}
 \quad\text{subject to}\quad \sum_i x_i\leq\sum_jq_j.
\]
\end_inset
 Its KKT multiplier \begin_inset Formula $\mu$\end_inset
 satisfies \begin_inset Formula $\phi_i'(x_i)\leq\mu$\end_inset
 with equality for \begin_inset Formula $x_i>0$\end_inset
 and \begin_inset Formula $\mu\leq c_j'(q_j)$\end_inset
 with equality for \begin_inset Formula $q_j>0$\end_inset
.  Thus a competitive equilibrium satisfies the planner conditions with \begin_inset Formula $\mu=p$\end_inset
.
\end_layout

\begin_layout Proposition
Second welfare theorem for the quasilinear model (cited).  Under concavity, continuity, and the usual interiority conditions, any solution of the planner's problem can be decentralized at a supporting price \begin_inset Formula $p=\mu$\end_inset
 by lump-sum transfers of the numeraire whose sum is zero.  The theorem concerns allocations or utility vectors attainable by the planner; an arbitrary utility vector need not be feasible.
\end_layout

'''

path.write_text(s[:start] + chapter + s[end:])
print("Replaced Competitive Markets and Partial Equilibrium chapter")
