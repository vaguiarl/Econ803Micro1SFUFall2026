#!/usr/bin/env python3
"""Replace the aggregation lecture draft with a precise, non-repetitive chapter."""

from pathlib import Path


BOOK = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"


CHAPTER = r'''\begin_layout Chapter
Aggregate Demand
\end_layout

\begin_layout Section
Three questions about aggregation
\end_layout

\begin_layout Itemize
When does aggregate demand depend on prices and total wealth rather than on the entire wealth distribution?
\end_layout

\begin_layout Itemize
When does aggregate demand satisfy a demand restriction such as WARP?
\end_layout

\begin_layout Itemize
When can aggregate demand be given a welfare interpretation?
\end_layout

\begin_layout Standard
Let consumers be indexed by 
\begin_inset Formula $i=1,\ldots,I$
\end_inset

.
 Consumer 
\begin_inset Formula $i$
\end_inset

 has Marshallian demand 
\begin_inset Formula $x_i(p,w_i)$
\end_inset

 at common prices 
\begin_inset Formula $p\in\mathbb{R}_{++}^{L}$
\end_inset

 and wealth 
\begin_inset Formula $w_i>0$
\end_inset

.
 Aggregate demand is
\begin_inset Formula $X(p,\mathbf{w})=\sum_{i=1}^{I}x_i(p,w_i)$
\end_inset

,
 where 
\begin_inset Formula $\mathbf{w}=(w_1,\ldots,w_I)$
\end_inset

.
 Total wealth is 
\begin_inset Formula $W=\sum_iw_i$
\end_inset

.
 Without additional structure,
 two wealth distributions with the same 
\begin_inset Formula $W$
\end_inset

 can generate different aggregate bundles.
\end_layout

\begin_layout Section
Gorman aggregation
\end_layout

\begin_layout Definition
Gorman form.
 Consumer 
\begin_inset Formula $i$
\end_inset

 has Gorman-form indirect utility if
\begin_inset Formula $v_i(p,w_i)=a_i(p)+b(p)w_i$
\end_inset

 for a common function 
\begin_inset Formula $b(p)>0$
\end_inset

 and consumer-specific functions 
\begin_inset Formula $a_i(p)$
\end_inset

.
\end_layout

\begin_layout Proposition
Gorman aggregation (cited).
 Suppose each 
\begin_inset Formula $v_i$
\end_inset

 has the Gorman form and is differentiable.
 Roy's identity gives
\begin_inset Formula $x_i(p,w_i)=-\frac{\nabla_pa_i(p)+w_i\nabla_pb(p)}{b(p)}$
\end_inset

.
 Therefore
\begin_inset Formula $X(p,\mathbf{w})=A(p)+B(p)W$
\end_inset

,
 where 
\begin_inset Formula $A(p)=-\sum_i\nabla_pa_i(p)/b(p)$
\end_inset

 and 
\begin_inset Formula $B(p)=-\nabla_pb(p)/b(p)$
\end_inset

.
 Aggregate demand consequently depends on 
\begin_inset Formula $(p,W)$
\end_inset

 and not on the distribution of wealth.
\end_layout

\begin_layout Standard
Under the usual differentiability and integrability conditions,
 a common wealth derivative 
\begin_inset Formula $D_{w_i}x_i(p,w_i)=B(p)$
\end_inset

 is the local signature of Gorman aggregation.
 The converse is a local statement and should not be read as a global representation without the regularity assumptions.
\end_layout

\begin_layout Section
Aggregate demand and WARP
\end_layout

\begin_layout Standard
Even if every individual demand satisfies WARP,
 aggregate demand need not do so.
 Aggregate WARP compares two price--total-wealth pairs while holding fixed the rule that assigns total wealth across consumers;
 the corresponding compensation need not leave each consumer's wealth unchanged.
\end_layout

\begin_layout Definition
Aggregate WARP.
 A single-valued aggregate demand 
\begin_inset Formula $X(p,W)$
\end_inset

 satisfies WARP if, for distinct observations 
\begin_inset Formula $(p,W)$
\end_inset

 and 
\begin_inset Formula $(p',W')$
\end_inset

,
\begin_inset Formula $p\cdot X(p',W')\leq W$
\end_inset

 implies 
\begin_inset Formula $p'\cdot X(p,W)>W'$
\end_inset

 whenever 
\begin_inset Formula $X(p,W)\neq X(p',W')$
\end_inset

.
\end_layout

\begin_layout Proposition
Sufficient condition for aggregate WARP.
 Suppose wealth shares are fixed,
 
\begin_inset Formula $w_i=\alpha_iW$
\end_inset

 with 
\begin_inset Formula $\alpha_i\geq0$
\end_inset

 and 
\begin_inset Formula $\sum_i\alpha_i=1$
\end_inset

,
 and suppose each map 
\begin_inset Formula $p\mapsto x_i(p,\alpha_iW)$
\end_inset

 satisfies the weak uncompensated law of demand on a convex price domain.
 Then 
\begin_inset Formula $X(p,W)=\sum_ix_i(p,\alpha_iW)$
\end_inset

 satisfies the weak uncompensated law of demand.
 With Walras' law and the usual strictness condition,
 aggregate WARP follows.
\end_layout

\begin_layout Standard
The proof is additive: sum the individual inequalities at the common wealth shares.
 If the shares change with prices or if wealth is reallocated after compensation,
 this argument no longer applies.
\end_layout

\begin_layout Section
Representative consumers and welfare
\end_layout

\begin_layout Definition
Positive representative consumer.
 A preference relation 
\begin_inset Formula $\succeq^{rep}$
\end_inset

 is a positive representative consumer for 
\begin_inset Formula $X$
\end_inset

 if its Walrasian demand equals 
\begin_inset Formula $X(p,W)$
\end_inset

 for every price--wealth pair in the domain.
 This is a statement about demand representation,
 not about welfare.
\end_layout

\begin_layout Definition
Normative representative consumer.
 Fix a social welfare function 
\begin_inset Formula $\mathcal{W}:\mathbb{R}^{I}\to\mathbb{R}$
\end_inset

 and individual indirect utilities 
\begin_inset Formula $v_i$
\end_inset

.
 A wealth allocation 
\begin_inset Formula $\mathbf{w}(p,W)$
\end_inset

 is welfare-optimal if it solves
\begin_inset Formula $\max_{\mathbf{w}}\mathcal{W}(v_1(p,w_1),\ldots,v_I(p,w_I))\text{ subject to }\sum_iw_i\leq W$
\end_inset

.
 A positive representative consumer is normative relative to 
\begin_inset Formula $\mathcal{W}$
\end_inset

 only when the wealth rule used to form 
\begin_inset Formula $X$
\end_inset

 is welfare-optimal at every 
\begin_inset Formula $(p,W)$
\end_inset

.
\end_layout

\begin_layout Standard
Gorman aggregation can deliver a positive representative consumer,
 but it does not select a social welfare function or justify interpersonal utility comparisons.
 Normative claims require the welfare criterion and the wealth-allocation rule to be stated explicitly.
\end_layout
'''


def main() -> None:
    text = BOOK.read_text()
    start = text.index("\\begin_layout Chapter\nAggregate Demand\n\\end_layout")
    end = text.index("\\begin_layout Chapter\nDiscrete Choice and Random Utility", start)
    text = text[:start] + CHAPTER.rstrip() + "\n\n" + text[end:]
    BOOK.write_text(text)


if __name__ == "__main__":
    main()
