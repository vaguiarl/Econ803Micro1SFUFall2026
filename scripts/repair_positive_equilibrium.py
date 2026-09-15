from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"
s = path.read_text()
start_marker = r"""\begin_layout Chapter
Positive Theory of Equilibrium
\end_layout"""
end_marker = r"""\begin_layout Part
V.
 Advanced Equilibrium Applications
\end_layout"""
start = s.index(start_marker)
end = s.index(end_marker, start)

chapter = r'''\begin_layout Chapter
Positive Theory of Equilibrium
\end_layout

\begin_layout Standard
The preceding chapter established welfare properties of competitive equilibrium.  This chapter studies what those conditions imply—and what they leave undetermined—for aggregate excess demand, existence, local uniqueness, comparative statics, and the core.
\end_layout

\begin_layout Section
Aggregate excess demand in pure exchange
\end_layout

\begin_layout Standard
Consider a pure-exchange economy with consumers \begin_inset Formula $i=1,\ldots,I$\end_inset
, commodity space \begin_inset Formula $\mathbb{R}_{+}^{L}$\end_inset
, endowments \begin_inset Formula $\omega_i\in\mathbb{R}_{+}^{L}$\end_inset
, and aggregate endowment \begin_inset Formula $\omega=\sum_i\omega_i\gg0$\end_inset
.  At a strictly positive price vector \begin_inset Formula $p\gg0$\end_inset
, consumer \begin_inset Formula $i$\end_inset
 has wealth \begin_inset Formula $w_i=p\cdot\omega_i$\end_inset
 and demand correspondence
\begin_inset Formula 
\[
 c_i(p,w_i)=\arg\max\{u_i(x):x\geq0,\ p\cdot x\leq w_i\}.
\]
\end_inset
\end_layout

\begin_layout Definition
Aggregate excess demand.  Select a demand \begin_inset Formula $x_i(p)\in c_i(p,p\cdot\omega_i)$\end_inset
 and define
\begin_inset Formula 
\[
 z(p)=\sum_{i=1}^{I}x_i(p)-\omega.
\]
\end_inset
 When demands are single-valued this is a function; with multiple optima it is a correspondence.
\end_layout

\begin_layout Definition
Pure-exchange equilibrium.  A pair \begin_inset Formula $(p^*,x^*)$\end_inset
 with \begin_inset Formula $p^*\gg0$\end_inset
 is a Walrasian equilibrium when each \begin_inset Formula $x_i^*\in c_i(p^*,p^*\cdot\omega_i)$\end_inset
 and \begin_inset Formula $\sum_i x_i^*=\omega$\end_inset
.  Prices are equivalent up to multiplication by a positive scalar.
\end_layout

\begin_layout Proposition
Walras' law and homogeneity.  Suppose each consumer is locally nonsatiated and demands are single-valued.  Then
\begin_inset Formula 
\[
 p\cdot z(p)=0,\qquad z(\lambda p)=z(p)\quad(\lambda>0).
\]
\end_inset
 If \begin_inset Formula $p\gg0$\end_inset
 and markets clear in all but one commodity, Walras' law implies that the final market clears as well.
\end_layout

\begin_layout Standard
If preferences are continuous, strictly convex, and strongly monotone, the demand function is continuous on \begin_inset Formula $\mathbb{R}_{++}^{L}\times\mathbb{R}_{++}$\end_inset
.  Consequently \begin_inset Formula $z$\end_inset
 is continuous on strictly positive prices.  Its domain should not be silently extended to a zero price: demand may become unbounded there.  In an equilibrium with nonnegative prices, a good can have excess supply only at a zero price; under strong monotonicity and \begin_inset Formula $p\gg0$\end_inset
, every market clears.
\end_layout

\begin_layout Standard
For calculations it is convenient to normalize prices.  We use either the simplex
\begin_inset Formula 
\[
\Delta=\{p\in\mathbb{R}_{+}^{L}:\mathbf{1}\cdot p=1\}
\]
\end_inset
 or the chart \begin_inset Formula $p_L=1$\end_inset
.  These are equivalent for strictly positive prices.
\end_layout

\begin_layout Example
Cobb--Douglas exchange.  With \begin_inset Formula $u_i(x)=x_{1}^{\alpha}x_{2}^{1-\alpha}$\end_inset
 and \begin_inset Formula $0<\alpha<1$\end_inset
,
\begin_inset Formula 
\[
 x_i(p)=\left(\frac{\alpha\,p\cdot\omega_i}{p_1},\frac{(1-\alpha)\,p\cdot\omega_i}{p_2}\right).
\]
\end_inset
 Substitution into \begin_inset Formula $z(p)=0$\end_inset
 reduces equilibrium to one relative-price equation, because the second equation follows from Walras' law.
\end_layout

\begin_layout Section
Existence
\end_layout

\begin_layout Proposition
Walrasian existence theorem (cited).  In a finite pure-exchange economy, if consumption sets are closed and convex, preferences are complete, transitive, continuous, and locally nonsatiated, and the aggregate endowment is strictly positive, a Walrasian equilibrium exists under the standard boundedness condition that makes the relevant feasible set compact.  Strict convexity is not required for existence; it gives uniqueness of each consumer's demand.
\end_layout

\begin_layout Standard
The usual proof normalizes prices to \begin_inset Formula $\Delta$\end_inset
, constructs a demand or excess-demand correspondence with nonempty compact convex values, and applies a fixed-point theorem.  Boundary behavior is essential: the correspondence must be defined on the closed simplex, and the assumptions must rule out a fixed point at a zero-price vector.  Writing a fixed-point map only on \begin_inset Formula $\mathbb{R}_{++}^{L}$\end_inset
 does not by itself prove existence.
\end_layout

\begin_layout Section
Local uniqueness and regularity
\end_layout

\begin_layout Definition
Normalized local uniqueness.  A normalized equilibrium \begin_inset Formula $p^*\in\Delta$\end_inset
 is locally unique if some neighborhood of \begin_inset Formula $p^*$\end_inset
 contains no other normalized equilibrium.
\end_layout

\begin_layout Standard
Work in the chart \begin_inset Formula $p_L=1$\end_inset
 and write \begin_inset Formula $\widehat z(p_1,\ldots,p_{L-1})=(z_1,\ldots,z_{L-1})$\end_inset
.  The last component is redundant by Walras' law.
\end_layout

\begin_layout Definition
Regular equilibrium.  A differentiable equilibrium \begin_inset Formula $p^*$\end_inset
 is regular when the Jacobian \begin_inset Formula $D\widehat z(p^*)$\end_inset
 is nonsingular.
\end_layout

\begin_layout Proposition
Regularity implies local uniqueness (cited).  If \begin_inset Formula $D\widehat z(p^*)$\end_inset
 is nonsingular, the inverse function theorem implies that \begin_inset Formula $p^*$\end_inset
 is an isolated zero of \begin_inset Formula $\widehat z$\end_inset
.  This is a local statement; it does not rule out another equilibrium far away.
\end_layout

\begin_layout Standard
For a regular economy, the signed index of an equilibrium is the sign of the determinant of the Jacobian in an oriented price chart.  The index theorem (cited) states that, under the usual compactness and boundary hypotheses, the sum of indices over normalized equilibria equals one.  Hence a regular economy has an odd number of equilibria.  The conclusion is global and requires the theorem's boundary assumptions; it does not follow from the inverse function theorem alone.
\end_layout

\begin_layout Section
What equilibrium theory does not identify
\end_layout

\begin_layout Standard
At a differentiability point, Walras' law and homogeneity imply the exact derivative restrictions
\begin_inset Formula 
\[
 Dz(p)^{\mathsf T}p=-z(p),\qquad Dz(p)p=0.
\]
\end_inset
 At an equilibrium, the first identity becomes \begin_inset Formula $Dz(p)^{\mathsf T}p=0$\end_inset
; these are restrictions, not a complete theory of comparative statics.
\end_layout

\begin_layout Proposition
Sonnenschein--Mantel--Debreu theorem (cited).  Subject to continuity, homogeneity of degree zero, Walras' law, and the standard boundary condition, aggregate excess demand can have essentially arbitrary shape on compact subsets of the strictly positive normalized price simplex.  In particular, individual rationality does not generally imply uniqueness, stability, or monotone comparative statics for the aggregate equilibrium map.
\end_layout

\begin_layout Standard
The theorem is an impossibility result about restrictions on aggregate demand.  It does not say that every arbitrary function is a demand system: the stated regularity, Walras, homogeneity, and boundary conditions remain necessary, and the result concerns a constructed finite exchange economy.
\end_layout

\begin_layout Section
Uniqueness and gross substitutes
\end_layout

\begin_layout Standard
With a constant-returns production cone \begin_inset Formula $Y\subseteq\mathbb{R}^{L}$\end_inset
 containing zero, a strictly positive price \begin_inset Formula $p$\end_inset
 supports the technology when \begin_inset Formula $p\cdot y\leq0$\end_inset
 for every \begin_inset Formula $y\in Y$\end_inset
.  If aggregate excess demand satisfies \begin_inset Formula $z(p)\in Y$\end_inset
 and Walras' law, then choosing production \begin_inset Formula $y=z(p)$\end_inset
 clears markets and maximizes profit.  This observation separates the consumer condition from the technology-support condition.
\end_layout

\begin_layout Definition
Gross substitutes.  An excess-demand function has the strict gross-substitutes property if, whenever only the price of good \begin_inset Formula $\ell$\end_inset
 rises, excess demand for every other good \begin_inset Formula $k\neq\ell$\end_inset
 strictly rises.  Weak gross substitutes replaces strict inequalities with weak inequalities.  The property is imposed on the relevant price domain and is stronger than Walras' law or homogeneity.
\end_layout

\begin_layout Proposition
Gross-substitutes uniqueness theorem (cited).  Under continuity, homogeneity, Walras' law, and a strict gross-substitutes condition, a pure-exchange equilibrium has at most one normalized strictly positive price vector.  Existence still requires a separate existence theorem.  Without strictness, gross substitutes can deliver a convex or lattice-structured equilibrium set rather than a unique price.
\end_layout

\begin_layout Section
The core
\end_layout

\begin_layout Standard
For clarity, define the core first in a pure-exchange economy.  There are \begin_inset Formula $I$\end_inset
 consumers, endowments \begin_inset Formula $\omega_i\in\mathbb{R}_{+}^{L}$\end_inset
, and a feasible allocation satisfies \begin_inset Formula $\sum_i x_i=\sum_i\omega_i$\end_inset
 (free disposal can replace equality by \begin_inset Formula $\leq$\end_inset
).  A nonempty coalition \begin_inset Formula $S\subseteq\{1,\ldots,I\}$\end_inset
 can use only \begin_inset Formula $\sum_{i\in S}\omega_i$\end_inset
.
\end_layout

\begin_layout Definition
Blocking coalition.  Coalition \begin_inset Formula $S$\end_inset
 blocks a feasible allocation \begin_inset Formula $x$\end_inset
 if there are \begin_inset Formula $\{x_i'\}_{i\in S}$\end_inset
 with \begin_inset Formula $x_i'\succ_i x_i$\end_inset
 for every \begin_inset Formula $i\in S$\end_inset
 and \begin_inset Formula $\sum_{i\in S}x_i'\leq\sum_{i\in S}\omega_i$\end_inset
.
\end_layout

\begin_layout Definition
The core is the set of feasible allocations blocked by no coalition.
\end_layout

\begin_layout Proposition
Walrasian allocations are in the core (cited).  Suppose preferences are locally nonsatiated and \begin_inset Formula $(p^*,x^*)$\end_inset
 is a Walrasian equilibrium with \begin_inset Formula $p^*\gg0$\end_inset
.  If a coalition made every member strictly better off, each member would need a bundle with strictly greater value than \begin_inset Formula $p^*\cdot\omega_i$\end_inset
.  Summing over the coalition contradicts its resource constraint.  Thus no coalition blocks \begin_inset Formula $x^*$\end_inset
.
\end_layout

\begin_layout Standard
The converse need not hold in a finite economy: the core can contain noncompetitive allocations.  In replica economies, the core-convergence theorem (cited) says that as the number of identical copies grows, core allocations approach the set of Walrasian allocations under the standard convexity, continuity, and nonsatiation assumptions.
\end_layout

'''

path.write_text(s[:start] + chapter + s[end:])
print("Replaced Positive Theory of Equilibrium chapter")
