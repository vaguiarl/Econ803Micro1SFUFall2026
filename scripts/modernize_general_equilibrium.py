#!/usr/bin/env python3
"""One time native LyX consolidation; preserve all later live manuscript edits.

The canonical question groups retain their released identifiers. The separate
problem injector places those groups at the end of the unified chapter.
Historical repair scripts for the former three chapters must not be rerun.
"""

from __future__ import annotations

import argparse
from pathlib import Path
import re

from inject_problem_sets import lyx_inline, marker, parse_problem_bank, strip_generated_blocks

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "notes/Microeconomics_1_notes_by_Victor_Aguiar.lyx"
STAMP = "ECON803_GENERAL_EQUILIBRIUM_UNIFIED:1"


def inline(value: str) -> str:
    value = lyx_inline(value)
    return re.sub(
        r"\[\[ref:([^\]]+)\]\]",
        lambda m: '\n\\begin_inset CommandInset ref\nLatexCommand ref\nreference "'
        + m.group(1) + '"\nnolink "false"\n\n\\end_inset\n',
        value,
    )


def block(kind: str, value: str, *, labels: tuple[str, ...] = ()) -> str:
    anchors = "".join(label_inset(name) for name in labels)
    return f"\\begin_layout {kind}\n{anchors}{inline(value)}\n\\end_layout\n\n"


def p(value: str) -> str:
    return block("Standard", value)


def math(value: str) -> str:
    return "\\begin_layout Standard\n\\begin_inset Formula\n\\[\n" + value + "\n\\]\n\\end_inset\n\\end_layout\n\n"


def label_inset(name: str) -> str:
    return '\\begin_inset CommandInset label\nLatexCommand label\nname "' + name + '"\n\n\\end_inset\n'


def label(name: str) -> str:
    return '\\begin_layout Standard\n' + label_inset(name) + '\\end_layout\n\n'


def cite(keys: str) -> str:
    return '\\begin_layout Standard\n\\begin_inset CommandInset citation\nLatexCommand citep\nkey "' + keys + '"\nliteral "false"\n\n\\end_inset\n\\end_layout\n\n'


def heading(kind: str, name: str) -> str:
    return f"\\begin_layout {kind}\n{name}\n\\end_layout"


def figure(name: str, caption: str) -> str:
    return (
        "\\begin_layout Standard\n\\begin_inset Float figure\nplacement ht\nwide false\n"
        "sideways false\nstatus open\n\n\\begin_layout Plain Layout\n\\align center\n"
        "\\begin_inset Graphics\n\tfilename figures/tikz/" + name + ".pdf\n\twidth 100text%\n\n"
        "\\end_inset\n\\end_layout\n\n\\begin_layout Plain Layout\n"
        "\\begin_inset Caption Standard\n\n\\begin_layout Plain Layout\n"
        + inline(caption) + "\n\\end_layout\n\\end_inset\n\\end_layout\n\\end_inset\n\\end_layout\n\n"
    )


INTRO = "".join([
    p("General equilibrium connects individual choices through common prices and common resource constraints. Begin with the Edgeworth box: one picture makes feasibility, gains from trade and endowment wealth visible. Then ask whether a clearing price exists, what welfare properties the allocation has, whether prices are unique, and what observed equilibria can reveal about preferences."),
    p("The chapter follows one economic model rather than restarting it under separate headings. Exchange supplies the first benchmark; production adds transformation and ownership income. Existence, welfare, uniqueness, adjustment and identification are different questions. Each needs its own assumptions, even when the same example illustrates several of them."),
    p("For a first reading, work through the box, aggregate excess demand, the Brouwer proof and the welfare arguments. Then study regularity, gross substitutes, coalition blocking and the empirical restrictions. The technical appendix gives the boundary details and the Kakutani extension when demand is not unique. The chapter ends with one problem program organized into three topic groups, preserving the released problem identifiers."),
    marker(STAMP),
])


EXISTENCE = "".join([
    block("Section", "Existence through a continuous price map"),
    label("sec:ge-existence"),
    block("Subsection", "From a crossing to a fixed point"),
    p(r"With two goods write $f(q)=z_1(q,1)$. Continuity and $f(a)>0>f(b)$ at positive $a<b$ give a clearing price by the intermediate value theorem; Walras' law then clears the other market. In our worked economy $f(q)=2/q-2$, so existence is immediate. Its negative derivative proves uniqueness separately. With many goods there is no single horizontal axis on which to look for a crossing. A fixed point supplies the corresponding argument."),
    block("Theorem", r"Brouwer fixed point theorem. Let $K\subseteq\mathbb R^m$ be nonempty, compact and convex. Every continuous function $T:K\to K$ has a point $v^*\in K$ such that $T(v^*)=v^*$."),
    block("Subsection", "A sufficient exchange economy theorem"),
    block("Proposition", r"Walrasian existence via Brouwer. Consider finitely many consumers with consumption sets $\mathbb R_+^L$, endowments $\omega_i\gg0$, and complete, transitive, continuous, strictly convex and strongly monotone preferences. Then there are normalized prices $p^*\gg0$ and utility maximizing bundles $x_i^*$ with $\sum_i x_i^*=\omega:=\sum_i\omega_i$. Here strong monotonicity means that $x\geq y$ and $x\ne y$ imply $x\succ_i y$. Strict convexity is a property of preferences, not convexity of a utility function.", labels=("thmstar:walrasian-existence",)),
    p("Strict convexity makes demand a function, which lets us use Brouwer directly. It is not necessary for equilibrium existence. Appendix [[ref:app:ge-existence]] proves the corresponding result with convex preferences using Kakutani and supplies the technical lemmas used below. Both statements are sufficient versions for finite pure exchange, not claims about every production or zero price model."),
    block("Subsection", "Build the map, then read its fixed point"),
    p(r"First make demand well defined at every candidate price. Normalize prices to the closed simplex $\Delta=\{p\geq0:\sum_\ell p_\ell=1\}$ and temporarily cap every individual's consumption at $2\omega$. Let $d_i^B(p)$ be the unique best bundle in $B=[0,2\omega]$ satisfying $p\cdot x\leq p\cdot\omega_i$. The cap is only a proof device: an allocation that clears cannot give anyone more than $\omega$. Positive individual endowments make wealth positive even at a zero candidate price. The maximum theorem therefore makes $d_i^B$ continuous on the whole closed simplex; the appendix checks this step."),
    math(r"z^B(p)=\sum_i d_i^B(p)-\omega,\qquad a_\ell(p)=\max\{z_\ell^B(p),0\},\qquad S(p)=\sum_\ell a_\ell(p)."),
    p(r"Now add the positive excess demand to each price weight and normalize. The positive part $a_\ell$ is the desired purchase in excess of supply when that imbalance is positive, and zero otherwise. This gives the continuous function"),
    math(r"T_\ell(p)=\frac{p_\ell+a_\ell(p)}{1+S(p)},\qquad T:\Delta\longrightarrow\Delta."),
    p(r"Every coordinate is nonnegative and the coordinates sum to one. Brouwer gives $p^*=T(p^*)$. To interpret it, suppress the argument $p^*$ and rearrange the fixed point identity as $a_\ell=Sp_\ell$. If $S>0$, every good with positive price has $z_\ell^B=Sp_\ell>0$. Consequently"),
    math(r"p^*\cdot z^B=S\sum_\ell(p_\ell^*)^2>0\quad\text{if }S>0."),
    p(r"That is impossible: adding the individual budget inequalities gives $p^*\cdot z^B\leq0$. Thus $S=0$ and $z^B\leq0$. Notice that we used affordability, not expenditure equality: the artificial cap could have prevented spending the whole budget before the fixed point was found."),
    p(r"Finally remove the proof device. Since aggregate demand does not exceed $\omega$, each chosen bundle lies strictly below $2\omega$. A zero priced good could now be increased within the cap and would strictly improve utility, so every price is positive. With room below the cap, optimality makes every budget bind. Hence $p^*\cdot z^B=0$; positive prices and $z^B\leq0$ force $z^B=0$. If an unrestricted affordable bundle were strictly preferred, a small mixture with the capped optimum would still be inside the cap and would be strictly preferred by strict convexity. This contradiction proves unrestricted optimality. We have an equilibrium of the original economy."),
    p("The proof has three jobs: make a continuous map on a compact price set, use the budget contradiction to rule out positive excess demand at its fixed point, and show that the artificial bounds do not affect the answer. The map is an existence construction, not a model of actual trading or a convergence theorem."),
    block("Subsection", "A fixed point we can draw"),
    block("Example", r"For the worked Cobb Douglas economy use simplex prices $(s,1-s)$ with $s\in[1/10,9/10]$. Then $z_1(s)=2/s-4$. The illustrative scalar function $T(s)=s+z_1(s)/32=s+1/(16s)-1/8$ maps this interval into itself: its minimum is $3/8$ at $s=1/4$ and its maximum is $38/45$. Its fixed point has $z_1(s)=0$, giving $s^*=1/2$. This scalar map is a transparent illustration, not a replacement for checking the general price map's hypotheses."),
    figure("ge_fixed_point", "A continuous self map and its fixed point. The crossing with the diagonal is the normalized clearing price in the worked economy. Existence of the crossing does not show that every price iteration converges."),
    p("Cobb Douglas preferences on the closed orthant have zero utility edges, so they do not literally satisfy every global strictness assumption of the conservative theorem above. Their displayed equilibrium was derived directly. For further function based existence proofs see the following references; the correspondence extension and broader economic existence results are distinguished in the appendix."),
    cite("geanakoplos2003,tonin2018,arrowdebreu1954,debreu1959"),
])


APPENDIX = "".join([
    block("Chapter", "Fixed Points and Equilibrium Existence"),
    label("app:ge-existence"),
    p("The main chapter uses Brouwer for a function. This appendix supplies its compact budget and truncation details, then explains what changes when a consumer has several optimal bundles. The fixed point theorems are classical results used here. They and the analytic economic existence proofs are not claimed as locally Lean verified."),
    block("Section", "Compact budgets and demand at boundary prices"),
    p(r"Retain finitely many consumers, $\omega_i\gg0$, $\omega=\sum_i\omega_i$, $B=[0,2\omega]$ and $\Delta=\{p\geq0:\sum_\ell p_\ell=1\}$. Define $C_i(p)=\{x\in B:p\cdot x\leq p\cdot\omega_i\}$ and $D_i^B(p)=\arg\max_{x\in C_i(p)}u_i(x)$, using a continuous representation of the stated preferences. These are artificial compact budget problems. Ordinary unrestricted demand need not exist at a free good and is not silently extended to the closed simplex."),
    block("Lemma", r"Compact budget continuity. The correspondence $C_i$ is nonempty, compact valued and continuous on $\Delta$. Under continuous preferences, $D_i^B$ is nonempty, compact valued and upper hemicontinuous. Convex preferences make its values convex; strict convexity makes it a single valued continuous function."),
    p(r"For the budget claim, zero is feasible and strictly affordable because $p\cdot\omega_i\geq\min_\ell\omega_{i\ell}>0$. Closed graph and the common compact box give upper hemicontinuity. To see lower hemicontinuity, take $x\in C_i(p)$ and any sequence $p^n\to p$. If $p\cdot x<p\cdot\omega_i$, then $x$ remains feasible eventually. Otherwise $p\cdot x=p\cdot\omega_i>0$. The bundles $x^n=\alpha_n x$, with $\alpha_n=\min\{1,(p^n\cdot\omega_i)/(p^n\cdot x)\}$ for large $n$, are feasible and converge to $x$. The maximum theorem gives the demand conclusions; convex upper contour sets give convex demand values, and strict convexity rules out two distinct maximizers."),
    p("Upper hemicontinuity here means that optimal bundles cannot acquire a new limiting value: if prices converge and a corresponding sequence of chosen bundles converges, the limit is optimal at the limiting prices. Compactness of the common box makes this closed graph description equivalent to upper hemicontinuity. It is not a license to select one optimum arbitrarily and assume that the selection is continuous."),
    block("Section", "Why the artificial cap disappears"),
    block("Lemma", r"Removing truncation. Suppose $p\gg0$, $x_i\in D_i^B(p)$ and $\sum_i x_i\leq\omega$. Under continuous, convex and strongly monotone preferences, $x_i$ also solves the unrestricted budget problem. Its budget binds."),
    p(r"Every $x_i\leq\omega$ lies strictly below the artificial ceiling. Any slack budget would allow a small positive increase of a commodity inside $B$, contradicting strong monotonicity. Now suppose an unrestricted affordable $y$ is strictly preferred to $x_i$. By continuity, $y'=\alpha y$ is still strictly preferred for some $\alpha<1$ sufficiently close to one. Since wealth is positive, $p\cdot y'<p\cdot\omega_i$. For small $t>0$, $v=(1-t)x_i+ty'$ lies inside $B$ and has strict budget slack. Convex preferences give $v\succeq_i x_i$. A sufficiently small increase of one coordinate preserves both constraints and makes the bundle strictly preferred to $v$, hence to $x_i$. This contradicts capped optimality. Under strict convexity a small mixture with $y$ is already strictly preferred, giving the shorter argument in the main chapter."),
    block("Section", "Kakutani and nonunique demand"),
    block("Theorem", r"Kakutani fixed point theorem. Let $K\subseteq\mathbb R^m$ be nonempty, compact and convex. If $\Phi:K\rightrightarrows K$ is upper hemicontinuous and has nonempty compact convex values, then some $v^*\in K$ satisfies $v^*\in\Phi(v^*)$. Brouwer is the single valued continuous special case."),
    cite("kakutani1941"),
    block("Proposition", r"Walrasian existence with convex preferences. Consider finitely many consumers with consumption sets $\mathbb R_+^L$, individual endowments $\omega_i\gg0$, and complete, transitive, continuous, convex and strongly monotone preferences. Then a Walrasian equilibrium with $p^*\gg0$ exists. Demand need not be unique. This includes the stricter preference assumptions of the main chapter's Brouwer theorem as a special case.", labels=("thmfull:walrasian-existence", "thm:ge-existence-kakutani")),
    p(r"Use the compact domain $K=\Delta\times B^I$. For a proposed allocation $x$, let $z(x)=\sum_i x_i-\omega$ and let the auxiliary price response be $P(x)=\arg\max_{r\in\Delta}r\cdot z(x)$. Its values are the price weights maximizing the value of the proposed imbalance, not a market trading rule. Define"),
    math(r"\Phi(p,x)=P(x)\times\prod_{i=1}^{I}D_i^B(p)."),
    p("The budget lemma gives nonempty compact convex demand values and upper hemicontinuity. The auxiliary price response has the same properties by the maximum theorem and linearity in prices. Their finite product is therefore an upper hemicontinuous correspondence from the nonempty compact convex domain into itself. Kakutani gives a fixed point with each household choosing optimally in its capped budget and the auxiliary price maximizing the imbalance's value."),
    math(r"p\cdot z(x)\leq0,\qquad p\cdot z(x)=\max_{r\in\Delta}r\cdot z(x)=\max_\ell z_\ell(x)."),
    p(r"Thus every excess demand coordinate is nonpositive. Aggregate feasibility puts every individual choice below $\omega<2\omega$. If a price were zero, its good could be increased within the cap and would strictly improve utility, so all prices are positive. Every budget now binds. Walras' law and nonpositive excess demands give exact clearing. The cap removal lemma proves unrestricted household optimality, completing the economic existence proof."),
    p("Strict convexity was needed only to replace demand correspondences by continuous functions in the main proof. The appendix removes that restriction, not the positive endowment or strong desirability assumptions. Leontief edges, zero price equilibria, general consumption sets, production and quasi equilibria require the corresponding hypotheses of a broader theorem. They are not established merely by naming Kakutani."),
    cite("arrowdebreu1954,debreu1959,mwg1995"),
])


def replace_once(source: str, old: str, new: str) -> str:
    if source.count(old) != 1:
        raise ValueError(f"missing or ambiguous revision anchor: {old[:100]}")
    return source.replace(old, new, 1)


def validate(source: str) -> None:
    required = [heading("Chapter", "General Equilibrium"), heading("Chapter", "Fixed Points and Equilibrium Existence"), STAMP,
                'name "thmstar:walrasian-existence"', 'name "thm:ge-existence-kakutani"',
                "figures/tikz/edgeworth_coordinates.pdf", "figures/tikz/edgeworth_redistribution.pdf"]
    for token in required:
        if source.count(token) != 1:
            raise ValueError(f"unified GE token missing or repeated: {token}")
    for title in ("General Equilibrium Theory", "Positive Theory of Equilibrium", "Testable Restrictions on the Equilibrium Manifold"):
        if heading("Chapter", title) in source:
            raise ValueError(f"former GE chapter remains: {title}")


def rewrite(source: str) -> str:
    if STAMP in source:
        validate(source)
        return source
    chapters = parse_problem_bank(ROOT / "problems/PROBLEM_BANK.md")
    source = strip_generated_blocks(source, chapters)
    a0 = source.index(heading("Chapter", "General Equilibrium Theory"))
    a1 = source.index(heading("Chapter", "Positive Theory of Equilibrium"), a0)
    a2 = source.index(heading("Part", "Advanced Equilibrium Applications"), a1)
    a3 = source.index(heading("Chapter", "Sequential Trade"), a2)
    exchange, positive, empirical = source[a0:a1], source[a1:a2], source[a2:a3]
    geometry_start = exchange.index(heading("Section", "Pure exchange economies: the Edgeworth box"))
    production_start = exchange.index(heading("Section", "One consumer and one producer"))
    behavior_start = exchange.index(heading("Section", "General equilibrium with inattention"))
    geometry = exchange[geometry_start:production_start]
    production = exchange[production_start:behavior_start]
    behavior = exchange[behavior_start:]
    market_start = positive.index(heading("Section", "From individual choices to aggregate excess demand"))
    local_start = positive.index(heading("Section", "Local uniqueness, regularity and comparative statics"))
    core_start = positive.index(heading("Section", "Coalitions, the core and the discipline of replication"))
    summary_start = positive.index(heading("Section", "How to use the chapter in a difficult problem"))
    market = positive[market_start:local_start]
    existence_start = market.index(heading("Section", "Existence: why a clearing price should be there"))
    market = market[:existence_start] + EXISTENCE
    local = positive[local_start:core_start]
    core = positive[core_start:summary_start]
    core = replace_once(core, heading("Section", "Coalitions, the core and the discipline of replication"), heading("Section", "Coalitions, the core and the discipline of replication") + "\n\n" + label("sec:ge-core"))
    empirical = empirical[empirical.index(heading("Section", "Observables and the equilibrium manifold")):]
    empirical = replace_once(empirical, heading("Section", "Observables and the equilibrium manifold"), heading("Section", "What equilibrium observations can reveal") + "\n\n" + label("sec:equilibrium-testability") + p("The same preferences must now explain several observed equilibria, not one market at one price. This adds empirical discipline: the latent individual choices must satisfy both rationality across observations and resource clearing within each observation. Keep this question distinct from the flexibility of aggregate excess demand in one economy."))
    geometry = geometry.replace("convention used in Chapter 12:", "strong blocking convention:")
    # The legacy text may serialize the chapter reference on one plain line.
    geometry = geometry.replace("convention used in Chapter\n12:", "strong blocking convention:")
    geometry = geometry.replace("follow\n\\begin_inset CommandInset citation", "follow\n\\begin_inset space ~\n\\end_inset\n\\begin_inset CommandInset citation")
    # Use a semantic paragraph anchor because native LyX can reflow formula insets.
    anchor = geometry.index("Production will change this resource accounting later in the chapter.")
    anchor = geometry.index("\\end_layout", anchor) + len("\\end_layout")
    geometry = geometry[:anchor] + "\n\n" + figure("edgeworth_coordinates", r"One point, two bundles. The endowment $W$ gives consumer 1 $(1,3)$ from the lower left origin and consumer 2 $(3,1)$ from the upper right origin. At the illustrative prices $(2,1)$ the shared boundary has slope $-2$, and the affordable sides are opposite. These prices illustrate budgets, not equilibrium.") + geometry[anchor:]
    anchor = geometry.index("Efficiency does not imply voluntary acceptance of redistribution.")
    anchor = geometry.index("\\end_layout", anchor) + len("\\end_layout")
    geometry = geometry[:anchor] + "\n\n" + figure("edgeworth_redistribution", r"Redistribution changes wealth within a fixed box. Transferring half a unit of each good from consumer 1 to consumer 2 changes wealth from $(4,4)$ to $(3,5)$. At prices $(1,1)$ equilibrium moves from $E$ to $F$. Each colored curve is tangent to its panel's budget line. The relative price stays fixed in this example, not as a general rule.") + geometry[anchor:]
    # The equilibrium zero set need not be a differentiable manifold.
    empirical = replace_once(empirical, "It records pairs of latent individual-endowment profiles and prices that can clear markets for fixed underlying preferences.", "It records pairs of latent individual endowment profiles and prices that can clear markets for fixed underlying preferences. Without differentiability and an appropriate rank condition this is only an equilibrium set; the smooth manifold terminology requires those additional regularity assumptions.")
    synthesis = "".join([
        block("Section", "A unified solution plan"),
        p("Begin with resources, preferences and ownership. Derive individual choices at announced prices, keeping the endowment wealth terms. Normalize one price and use Walras' law to remove one redundant equation. Establish existence with the hypotheses of the relevant theorem, then verify every candidate against optimization, budgets and all markets. Distinguish a welfare comparison from affordability and distinguish a regular local branch from a globally unique equilibrium."),
        p("For a policy response, specify which primitive changes and which equilibrium branch is followed. For a proposed price update, check the update's own domain and derivative; the Brouwer construction is not a convergence guarantee. For a coalition deviation, use the coalition's original resources. For equilibrium data, keep each consumer's preference fixed across observations and separate passing a rationalization test from identifying a counterfactual."),
        p("The problem program below follows these connections. The 11 series develops exchange, production, ownership and welfare; the 12 series studies excess demand, uniqueness and coalitions; the 13 series studies empirical restrictions and counterfactual identification. These are permanent catalog identifiers, retained to keep released assignments and private answer keys consistent, not three separate printed chapters."),
    ])
    market = replace_once(market, heading("Section", "From individual choices to aggregate excess demand"), heading("Section", "From individual choices to aggregate excess demand") + "\n\n" + label("sec:positive-equilibrium"))
    unified = block("Chapter", "General Equilibrium") + label("chap:general-equilibrium") + label("chap:positive-equilibrium") + label("chap:equilibrium-testability") + INTRO + geometry + market + production + local + core + behavior + empirical + synthesis
    source = source[:a0] + unified + block("Part", "Advanced Equilibrium Applications") + source[a3:]
    source = replace_once(source, heading("Chapter", "Technical Theorem Records"), APPENDIX + heading("Chapter", "Technical Theorem Records"))
    first = source.index("Problem identifiers are stable across")
    end = source.index("\\end_layout", first)
    source = source[:end] + " Problem identifiers are permanent catalog labels. They can differ from the printed chapter number after topics are combined, and they remain unchanged in weekly assignments, case studies and the solutions handbook.\n" + source[end:]
    source = source.replace("Every chapter ends with a two-part problem section.", "Every substantive chapter ends with a two part problem program.", 1)
    source = source.replace(" Part II uses Proof and Applied problems as bridges to one named chapter case,\n which always appears last.", " Part II uses Proof and Applied problems as bridges to a named topic case,\n which appears last within its topic group.\n The unified general equilibrium chapter contains three such groups and preserves all three cases.\n Technical appendices supply proofs rather than a separate weekly assignment.", 1)
    # Replace only the existing preface paragraph, leaving the rest untouched.
    preface = source.index("The material is cumulative.")
    end = source.index("\\end_layout", preface)
    source = source[:preface] + "The material is cumulative. Part I begins with utility maximization and consumer demand, then develops duality, comparative statics, welfare, revealed preference and abstract choice. Part II studies expected utility, stochastic choice and attention. Part III turns to aggregation. Part IV develops production, competitive markets and one unified general equilibrium chapter, including existence, welfare, equilibrium behavior and empirical restrictions. Part V treats sequential trade, matching and computable general equilibrium. Appendix A collects order theory, Appendix B develops fixed points and equilibrium existence, Appendix C records the exact versions of starred consumer theorems, and the final glossary provides linked notation.\n" + source[end:]
    validate(source)
    return source


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    old = BOOK.read_text()
    new = rewrite(old)
    if args.check:
        if old != new:
            raise SystemExit("general equilibrium consolidation is pending")
        print("unified general equilibrium chapter and technical appendix are present")
    elif old != new:
        BOOK.write_text(new)
        print(BOOK)


if __name__ == "__main__":
    main()
