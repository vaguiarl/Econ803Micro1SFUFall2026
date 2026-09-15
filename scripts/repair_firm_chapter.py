from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"
s = path.read_text()
start_marker = r"""\begin_layout Chapter
Theory of the Firm
\end_layout"""
end_marker = r"""\begin_layout Chapter
Competitive Markets and Partial Equilibrium
\end_layout"""
start = s.index(start_marker)
end = s.index(end_marker, start)
chapter = r'''\begin_layout Chapter
Theory of the Firm
\end_layout

\begin_layout Standard
This chapter treats technology as a feasible set of net-output vectors.  Profit maximization and cost minimization are dual ways of valuing that set at prices; aggregation and efficiency follow from the same support-function geometry.
\end_layout

\begin_layout Section
Production sets
\end_layout

\begin_layout Standard
There are \begin_inset Formula $L\geq1$\end_inset
 commodities.  A production plan \begin_inset Formula $y\in\mathbb{R}^{L}$\end_inset
 records net outputs: \begin_inset Formula $y_\ell>0$\end_inset
 is an output and \begin_inset Formula $y_\ell<0$\end_inset
 is an input.  The production set \begin_inset Formula $Y\subseteq\mathbb{R}^{L}$\end_inset
 contains exactly the technologically feasible plans.
\end_layout

\begin_layout Standard
The benchmark assumptions are: \begin_inset Formula $Y$\end_inset
 is nonempty and closed; \begin_inset Formula $0\in Y$\end_inset
 (inaction); and free disposal, \begin_inset Formula $y\in Y$\end_inset
 and \begin_inset Formula $y'\leq y$\end_inset
 imply \begin_inset Formula $y'\in Y$\end_inset
.
 A no-free-lunch condition rules out \begin_inset Formula $y\in Y\cap\mathbb{R}_{+}^{L}$\end_inset
 other than \begin_inset Formula $0$\end_inset
.
 Convexity of \begin_inset Formula $Y$\end_inset
 is the standard diminishing-returns assumption in net-output form.
\end_layout

\begin_layout Standard
If a differentiable transformation function satisfies \begin_inset Formula $Y=\{y:F(y)\leq0\}$\end_inset
 and \begin_inset Formula $F(\overline y)=0$\end_inset
,
 the local slope of the transformation frontier is
\end_layout

\begin_layout Standard
\begin_inset Formula 
\[
\frac{d y_k}{d y_\ell}=-\frac{F_\ell(\overline y)}{F_k(\overline y)}.
\]
\end_inset
\end_layout

\begin_layout Standard
The minus sign is essential: increasing one net output requires a compensating reduction in the other when the frontier is written as \begin_inset Formula $F(y)=0$\end_inset
.
\end_layout

\begin_layout Section
Production functions and input substitution
\end_layout

\begin_layout Standard
With \begin_inset Formula $M$\end_inset
 outputs and \begin_inset Formula $L-M$\end_inset
 inputs, write outputs as \begin_inset Formula $q\in\mathbb{R}_{+}^{M}$\end_inset
 and input use as \begin_inset Formula $z\in\mathbb{R}_{+}^{L-M}$\end_inset
.
 In the single-output case a production function \begin_inset Formula $f$\end_inset
 describes free disposal through \begin_inset Formula $q\leq f(z)$\end_inset
.
 If \begin_inset Formula $f$\end_inset
 is differentiable, the marginal rate of technical substitution between inputs \begin_inset Formula $\ell$\end_inset
 and \begin_inset Formula $k$\end_inset
 is
\end_layout

\begin_layout Standard
\begin_inset Formula 
\[
MRTS_{\ell k}(z)=\frac{f_{\ell}(z)}{f_{k}(z)},
\]
\end_inset
\end_layout

\begin_layout Standard
the amount of input \begin_inset Formula $k$\end_inset
 needed to offset a marginal reduction in input \begin_inset Formula $\ell$\end_inset
 while holding output fixed.  Concavity of \begin_inset Formula $f$\end_inset
 makes the input requirement set \begin_inset Formula $\{z:f(z)\geq q\}$\end_inset
 convex.
\end_layout

\begin_layout Section
Profit maximization
\end_layout

\begin_layout Definition
For a price vector \begin_inset Formula $p\in\mathbb{R}^{L}$\end_inset
,
 the profit function is
\begin_inset Formula 
\[
\pi(p)=\sup_{y\in Y}p\cdot y,
\]
\end_inset
\end_layout

\begin_layout Standard
and the supply correspondence is \begin_inset Formula $y(p)=\arg\max_{y\in Y}p\cdot y$\end_inset
 whenever the supremum is finite and attained.  If \begin_inset Formula $Y$\end_inset
 is closed and unbounded, finiteness and attainment require separate assumptions.
\end_layout

\begin_layout Proposition
Profit-function properties (cited).  The function \begin_inset Formula $\pi$\end_inset
 is convex and homogeneous of degree one in prices.  The supply correspondence is homogeneous of degree zero; if \begin_inset Formula $Y$\end_inset
 is convex, it is convex-valued.  At a differentiability point, Hotelling's lemma gives \begin_inset Formula $\nabla\pi(p)=y(p)$\end_inset
.
 If \begin_inset Formula $\pi$\end_inset
 is twice differentiable, \begin_inset Formula $D_py(p)=D_p^{2}\pi(p)$\end_inset
 is symmetric positive semidefinite and \begin_inset Formula $D_py(p)p=0$\end_inset
.
\end_layout

\begin_layout Standard
The non-differentiable law of supply is the monotonicity inequality
\begin_inset Formula 
\[
(p-p')\cdot(y-y')\geq0
\]
\end_inset
\end_layout

\begin_layout Standard
for \begin_inset Formula $y\in y(p)$\end_inset
 and \begin_inset Formula $y'\in y(p')$\end_inset
.
 It follows by adding the two profit-maximization inequalities.
\end_layout

\begin_layout Standard
For a single-output technology, \begin_inset Formula $q=f(z)$\end_inset
,
 profit maximization is \begin_inset Formula $\max_{z\geq0}\{p f(z)-w\cdot z\}$\end_inset
.
 At a differentiable interior optimum, \begin_inset Formula $p\nabla f(z^*)=w$\end_inset
; with nonnegative inputs the KKT conditions are
\end_layout

\begin_layout Standard
\begin_inset Formula 
\[
p f_{\ell}(z^*)\leq w_{\ell},
\qquad z^*_{\ell}\bigl(w_{\ell}-p f_{\ell}(z^*)\bigr)=0.
\]
\end_inset
\end_layout

\begin_layout Section
Cost minimization
\end_layout

\begin_layout Definition
Given input prices \begin_inset Formula $w\gg0$\end_inset
 and a target \begin_inset Formula $q>0$\end_inset
,
 the cost function is
\begin_inset Formula 
\[
c(w,q)=\min_{z\geq0}\{w\cdot z:f(z)\geq q\}.
\]
\end_inset
\end_layout

\begin_layout Standard
Assume the minimum is finite and attained.  The conditional factor-demand correspondence is the argmin set \begin_inset Formula $z(w,q)$\end_inset
.
 At a differentiable optimum, the KKT conditions are
\begin_inset Formula 
\[
w_{\ell}\geq\lambda f_{\ell}(z^*),
\qquad z^*_{\ell}\bigl(w_{\ell}-\lambda f_{\ell}(z^*)\bigr)=0,
\qquad \lambda\geq0.
\]
\end_inset
\end_layout

\begin_layout Proposition
Cost-function properties (cited).  The cost function is homogeneous of degree one and concave in input prices, nondecreasing in the output target, and—when \begin_inset Formula $f$\end_inset
 is concave—convex in \begin_inset Formula $q$\end_inset
.
 If the cost function is differentiable, Shephard's lemma gives \begin_inset Formula $\nabla_w c(w,q)=z(w,q)$\end_inset
 and \begin_inset Formula $\partial_q c(w,q)=\lambda$\end_inset
.
 If twice differentiable, \begin_inset Formula $D_w z=D_w^{2}c$\end_inset
 is symmetric negative semidefinite and \begin_inset Formula $D_w z\,w=0$\end_inset
 by price homogeneity.
\end_layout

\begin_layout Standard
The firm's output choice can be written as \begin_inset Formula $\max_{q\geq0}\{p q-c(w,q)\}$\end_inset
.
 If the cost function is differentiable, an interior optimum satisfies \begin_inset Formula $p=\partial_q c(w,q)$\end_inset
; at \begin_inset Formula $q=0$\end_inset
 the corresponding one-sided inequality applies.
\end_layout

\begin_layout Section
Aggregation and efficiency
\end_layout

\begin_layout Standard
For firms \begin_inset Formula $j=1,\ldots,J$\end_inset
 with production sets \begin_inset Formula $Y_j$\end_inset
,
 the aggregate technology is the Minkowski sum
\begin_inset Formula 
\[
Y=\sum_{j=1}^{J}Y_j=\left\{\sum_{j=1}^{J}y_j:y_j\in Y_j\right\}.
\]
\end_inset
\end_layout

\begin_layout Proposition
If each firm's profit maximum is finite and attained, then
\begin_inset Formula 
\[
\pi_Y(p)=\sum_{j=1}^{J}\pi_{Y_j}(p),
\qquad
y_Y(p)=\sum_{j=1}^{J}y_j(p)
\]
\end_inset
\end_layout

\begin_layout Standard
where the second equality is understood as equality of attainable aggregate supply sets.  The first equality follows directly from separability of the maximization over the Minkowski sum.
\end_layout

\begin_layout Definition
A feasible production plan \begin_inset Formula $y\in Y$\end_inset
 is efficient if there is no \begin_inset Formula $y'\in Y$\end_inset
 with \begin_inset Formula $y'\geq y$\end_inset
 and \begin_inset Formula $y'\neq y$\end_inset
.
\end_layout

\begin_layout Proposition
If \begin_inset Formula $p\gg0$\end_inset
 and \begin_inset Formula $y\in y(p)$\end_inset
,
 then \begin_inset Formula $y$\end_inset
 is efficient.  If \begin_inset Formula $Y$\end_inset
 is convex and closed and satisfies free disposal, every efficient plan is supported by some nonzero \begin_inset Formula $p\geq0$\end_inset
; this supporting-price statement is a separating-hyperplane theorem and may allow zero prices.
\end_layout

'''
path.write_text(s[:start] + chapter + s[end:])
print(f"rewrote firm chapter in {path}")
