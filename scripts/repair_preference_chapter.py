#!/usr/bin/env python3
"""Replace the lecture-draft choice chapter with a compact, precise version."""

from pathlib import Path


BOOK = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"


PREFERENCE = r'''\begin_layout Chapter
Preference and Choice
\end_layout

\begin_layout Section
From Choice Data to Preference
\end_layout

\begin_layout Standard
Choice data,
 preference relations,
 and utility representations are three descriptions of the same decision problem.
 This chapter fixes the logical relations among them before prices and wealth are introduced in the consumer-theory chapter.
\end_layout

\begin_layout Section
Choice environments
\end_layout

\begin_layout Standard
Let
\begin_inset Formula $X$
\end_inset

 be a nonempty set of alternatives and let
\begin_inset Formula $\mathcal{A}\subseteq2^{X}\setminus\{\emptyset\}$
\end_inset

 be the family of feasible menus.
\end_layout

\begin_layout Definition
Choice correspondence.
 A choice correspondence is a map
\begin_inset Formula $c:\mathcal{A}\rightrightarrows X$
\end_inset

 satisfying
\begin_inset Formula $\emptyset\neq c(A)\subseteq A$
\end_inset

 for every
\begin_inset Formula $A\in\mathcal{A}$
\end_inset

.
 A choice structure is the pair
\begin_inset Formula $(\mathcal{A},c)$
\end_inset

.
\end_layout

\begin_layout Definition
Rationalization.
 A binary relation
\begin_inset Formula $\succeq$
\end_inset

 rationalizes
\begin_inset Formula $(\mathcal{A},c)$
\end_inset

 if
\begin_inset Formula $c(A)=\{x\in A:x\succeq y\text{ for every }y\in A\}$
\end_inset

 for every
\begin_inset Formula $A\in\mathcal{A}$
\end_inset

.
 It weakly rationalizes the data if the equality is replaced by inclusion.
 A rational preference relation is complete and transitive.
\end_layout

\begin_layout Section
Preference relations
\end_layout

\begin_layout Definition
For a relation
\begin_inset Formula $\succeq\subseteq X\times X$
\end_inset

,
 define its strict and symmetric parts by
\begin_inset Formula $x\succ y\iff x\succeq y\text{ and not }y\succeq x$
\end_inset

 and
\begin_inset Formula $x\sim y\iff x\succeq y\text{ and }y\succeq x$
\end_inset

.
 If
\begin_inset Formula $\succeq$
\end_inset

 is complete and transitive,
 then
\begin_inset Formula $\succ$
\end_inset

 is irreflexive and transitive,
 while
\begin_inset Formula $\sim$
\end_inset

 is an equivalence relation.
 These elementary implications are the order-theoretic basis for utility representation.
\end_layout

\begin_layout Proposition
Finite utility representation.
 If
\begin_inset Formula $X$
\end_inset

 is finite,
 a preference relation on
\begin_inset Formula $X$
\end_inset

 has a real-valued utility representation if and only if it is complete and transitive.
 A representation is unique up to a strictly increasing transformation of its range.
\end_layout

\begin_layout Standard
For an infinite commodity or choice space,
 representation requires additional assumptions such as continuity and a suitable countability condition.
 The continuous-utility theorem used later is stated in the consumer-theory chapter.
\end_layout

\begin_layout Section
Revealed choice and WGARP
\end_layout

\begin_layout Definition
Direct revealed preference.
 For a choice structure
\begin_inset Formula $(\mathcal{A},c)$
\end_inset

,
 write
\begin_inset Formula $x\succeq^{C}y$
\end_inset

 if there is a menu
\begin_inset Formula $A\in\mathcal{A}$
\end_inset

 with
\begin_inset Formula $x\in c(A)$
\end_inset

 and
\begin_inset Formula $y\in A$
\end_inset

.
 Write
\begin_inset Formula $x\succ^{C}y$
\end_inset

 if, in addition,
\begin_inset Formula $y\notin c(A)$
\end_inset

.
 Let
\begin_inset Formula $\succeq^{C*}$
\end_inset

 be the reflexive-transitive closure of
\begin_inset Formula $\succeq^{C}$
\end_inset

.
\end_layout

\begin_layout Definition
Weak Generalized Axiom of Revealed Preference (WGARP).
 The data satisfy WGARP when
\begin_inset Formula $x\succeq^{C}y$
\end_inset

 implies not
\begin_inset Formula $y\succ^{C}x$
\end_inset

.
 Equivalently,
 if two menus contain both
\begin_inset Formula $x$
\end_inset

 and
\begin_inset Formula $y$
\end_inset

,
 choosing
\begin_inset Formula $x$
\end_inset

 from one and strictly choosing
\begin_inset Formula $y$
\end_inset

 from the other is ruled out.
\end_layout

\begin_layout Proposition
Necessity of WGARP.
 If a complete and transitive preference relation rationalizes a choice structure,
 then the structure satisfies WGARP.
\end_layout

\begin_layout Standard
Proof.
 If
\begin_inset Formula $x\in c(A)$
\end_inset

 and
\begin_inset Formula $y\in A$
\end_inset

,
 rationalization gives
\begin_inset Formula $x\succeq y$
\end_inset

.
 If a second menu strictly chose
\begin_inset Formula $y$
\end_inset

 over
\begin_inset Formula $x$
\end_inset

,
 it would give
\begin_inset Formula $y\succ x$
\end_inset

,
 contradicting the first comparison.
\end_layout

\begin_layout Section
GARP on finite data
\end_layout

\begin_layout Definition
Generalized Axiom of Revealed Preference (GARP).
 A finite dataset satisfies GARP when
\begin_inset Formula $x\succeq^{C*}y$
\end_inset

 never occurs together with
\begin_inset Formula $y\succ^{C}x$
\end_inset

.
 Thus an indirect revealed-preference chain may return to an alternative only when the return comparison is not strict.
\end_layout

\begin_layout Theorem
Finite-data rationalizability (cited).
 For a finite dataset with nonempty observed choice sets,
 GARP is equivalent to weak rationalizability by a complete and transitive preference relation.
 Under the standard budget-set and monotonicity assumptions,
 Afriat's theorem strengthens this conclusion to a locally nonsatiated,
 continuous and concave utility representation.
 The proof is deferred to the Afriat section of the consumer-theory chapter,
 where the finite inequalities are written explicitly.
\end_layout

\begin_layout Standard
WGARP is the one-step restriction for a correspondence;
 GARP is its transitive closure and is therefore the relevant condition when the data do not contain every pair of alternatives in a common menu.
 Exact single-valued rationalization can require additional tie-breaking assumptions,
 so the theorem above is stated for weak rationalization.
\end_layout

\begin_layout Example
Let
\begin_inset Formula $X=\{a,b,c\}$
\end_inset

 and suppose
\begin_inset Formula $a\succ^{C}b$
\end_inset

,

\begin_inset Formula $b\succ^{C}c$
\end_inset

,
 and
\begin_inset Formula $c\succ^{C}a$
\end_inset

.
 This strict cycle violates GARP and cannot be generated by a transitive preference relation.
\end_layout

\begin_layout Standard
The separation between the abstract choice language and the budget-set language is deliberate.
 In the next chapter,
 prices and wealth impose additional structure,
 and the Afriat inequalities provide a finite certificate that can be checked mechanically.
\end_layout
'''


def replace_between(text: str, start: str, end: str, replacement: str) -> str:
    i = text.index(start)
    j = text.index(end, i)
    return text[:i] + replacement.rstrip() + "\n\n" + text[j:]


def main() -> None:
    text = BOOK.read_text()
    text = replace_between(
        text,
        "\\begin_layout Chapter\nPreference and Choice\n\\end_layout",
        "\\begin_layout Chapter\nConsumer Theory:",
        PREFERENCE,
    )
    BOOK.write_text(text)


if __name__ == "__main__":
    main()
