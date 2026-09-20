#!/usr/bin/env python3
"""Add the canonical finite Shannon rational-inattention model to Chapter 7."""

from __future__ import annotations

import argparse
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"

INSERT_BEFORE = "\\begin_layout Section\nA Gaussian Signal Example\n\\end_layout"
NEW_HEADING = (
    "\\begin_layout Section\n"
    "Rational Inattention: Choosing an Information Structure\n"
    "\\end_layout"
)

OLD_INTRO = """The benchmark consumer maximizes utility using the true budget and prices.  A sparse-max consumer keeps the true budget constraint but forms a decision using a perceived price vector.  This chapter states the behavioral rule explicitly and records which benchmark conclusions no longer follow automatically."""

NEW_INTRO = """The benchmark chapters assume that the decision maker observes the relevant environment and optimizes without cognitive friction.  This chapter separates two departures from that benchmark.  Sparse-max demand takes distorted or incomplete price perception as given.  Rational inattention instead makes information acquisition a choice: the decision maker trades the value of a more informative signal against its cost.  Keeping these mechanisms distinct clarifies both their empirical content and their connection to the stochastic-choice models of the preceding chapter."""

SECTION = r'''\begin_layout Section
Rational Inattention: Choosing an Information Structure
\end_layout

\begin_layout Standard
Sparse-max demand begins with perceived prices.
 Rational inattention explains why a decision maker may choose to observe only a noisy summary of the state.
 Let \begin_inset Formula $\mathcal S$\end_inset
 be a finite state space, let \begin_inset Formula $\notationfirst{ri-action-set}{\mathcal A}$\end_inset
 be a finite action set, and let \begin_inset Formula $\notationfirst{ri-prior}{\mu_{0}}\in\Delta(\mathcal S)$\end_inset
 have full support.
 The payoff from action \begin_inset Formula $a$\end_inset
 in state \begin_inset Formula $s$\end_inset
 is \begin_inset Formula $v(a,s)$\end_inset
.
 An information-and-decision strategy can be written directly as a stochastic choice rule \begin_inset Formula $\notationfirst{ri-channel}{q(a\mid s)}$\end_inset
, with \begin_inset Formula $q(\cdot\mid s)\in\Delta(\mathcal A)$\end_inset
 for every state.
 This direct formulation absorbs both the signal and the action chosen after each signal.
\end_layout

\begin_layout Definition
Shannon information cost.
 The unconditional action probability induced by \begin_inset Formula $q$\end_inset
 is \begin_inset Formula $q(a):=\sum_{s\in\mathcal S}\mu_{0}(s)q(a\mid s)$\end_inset
.
 The mutual information between the state and the chosen action is
\begin_inset Formula
\[
\notationfirst{mutual-information}{\mathcal I(q)}
=\sum_{s\in\mathcal S}\sum_{a\in\mathcal A}
\mu_{0}(s)q(a\mid s)
\log\!\left(\frac{q(a\mid s)}{q(a)}\right),
\]
\end_inset
with the convention \begin_inset Formula $0\log 0=0$\end_inset
.
 The cost of the channel is \begin_inset Formula $\kappa\mathcal I(q)$\end_inset
, where \begin_inset Formula $\kappa>0$\end_inset
 is the marginal cost of information.
\end_layout

\begin_layout Standard
The canonical rational-inattention problem is
\begin_inset Formula
\[
\max_{q(\cdot\mid s)\in\Delta(\mathcal A)}
\left\{
\sum_{s\in\mathcal S}\sum_{a\in\mathcal A}
\mu_{0}(s)q(a\mid s)v(a,s)
-\kappa\mathcal I(q)
\right\}.
\]
\end_inset
The first term is expected payoff and the second is the cost of making actions state-dependent.
 If \begin_inset Formula $q(a\mid s)=q(a)$\end_inset
 for every \begin_inset Formula $(a,s)$\end_inset
, then actions reveal no information about the state and \begin_inset Formula $\mathcal I(q)=0$\end_inset
.
 This formulation follows the Shannon-cost rational-inattention model
\begin_inset CommandInset citation
LatexCommand citep
key "sims2003,matejkamckay2015"
literal "false"

\end_inset
.
\end_layout

\begin_layout Proposition
Rational-inattention choice probabilities.
 At an optimum, every action with \begin_inset Formula $q(a)>0$\end_inset
 satisfies
\begin_inset Formula
\[
q(a\mid s)
=\frac{q(a)\exp\{v(a,s)/\kappa\}}
{\sum_{b\in\mathcal A}q(b)\exp\{v(b,s)/\kappa\}}
\qquad\text{for every }s\in\mathcal S.
\]
\end_inset
Conversely, a feasible channel satisfying these equations together with the consistency conditions \begin_inset Formula $q(a)=\sum_s\mu_{0}(s)q(a\mid s)$\end_inset
 solves the concave program on its active support.
\end_layout

\begin_layout Proof
Attach a multiplier to \begin_inset Formula $\sum_a q(a\mid s)=1$\end_inset
 for each state and differentiate the objective with respect to a positive \begin_inset Formula $q(a\mid s)$\end_inset
.
 Mutual information has derivative \begin_inset Formula $\mu_{0}(s)\log(q(a\mid s)/q(a))$\end_inset
.
 The first-order condition therefore makes \begin_inset Formula $\log(q(a\mid s)/q(a))$\end_inset
 equal to \begin_inset Formula $v(a,s)/\kappa$\end_inset
 plus a state-specific normalizing constant.
 Exponentiating and imposing that conditional probabilities sum to one gives the displayed formula.
 Concavity supplies sufficiency on the active support.
\end_layout

\begin_layout Standard
The formula resembles multinomial logit, but its baseline weight \begin_inset Formula $q(a)$\end_inset
 is endogenous and must satisfy a fixed-point condition.
 Thus random utility and rational inattention can produce similar choice probabilities for different structural reasons: the former randomizes tastes, whereas the latter optimally limits state information.
 The distinction matters for welfare and counterfactual information policies.
\end_layout

'''


def rewrite(text: str) -> str:
    if NEW_HEADING in text:
        return text
    if text.count(INSERT_BEFORE) != 1:
        raise ValueError("could not uniquely locate the Gaussian example")
    if text.count(OLD_INTRO) != 1:
        raise ValueError("could not uniquely locate the attention-chapter introduction")
    text = text.replace(
        "chaptermark{Sparse-Max and Rational Inattention}",
        "chaptermark{Limited Attention and Costly Information}",
        1,
    )
    text = text.replace(OLD_INTRO, NEW_INTRO, 1)
    return text.replace(INSERT_BEFORE, SECTION + INSERT_BEFORE, 1)


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    source = BOOK.read_text()
    revised = rewrite(source)
    changed = revised != source
    if args.check:
        if changed:
            raise SystemExit("rational-inattention core is pending")
        print("rational-inattention core is present")
    elif changed:
        BOOK.write_text(revised)
        print(f"updated {BOOK}")
    else:
        print("no changes needed")


if __name__ == "__main__":
    main()
