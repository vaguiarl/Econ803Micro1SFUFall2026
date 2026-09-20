#!/usr/bin/env python3
"""One-time expansion into native, editable LyX layouts; never overwrite a stamped edit."""

from __future__ import annotations

import argparse
from pathlib import Path

from inject_problem_sets import lyx_inline, marker, separator

ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "notes/Microeconomics_1_notes_by_Victor_Aguiar.lyx"
STAMP = "ECON803_WORKHORSE_EXPANSION:1"


def block(kind: str, text: str) -> str:
    text = text.replace("--", "-")
    native = f"\\begin_layout {kind}\n{lyx_inline(text)}\n\\end_layout\n\n"
    return native + (separator() + "\n" if kind == "Example" else "")


def p(text: str) -> str:
    return block("Standard", text)


def math(text: str) -> str:
    return "\\begin_layout Standard\n\\begin_inset Formula\n\\[\n" + text + "\n\\]\n\\end_inset\n\\end_layout\n\n"


def label(name: str) -> str:
    return '\\begin_layout Standard\n\\begin_inset CommandInset label\nLatexCommand label\nname "' + name + '"\n\n\\end_inset\n\\end_layout\n\n'


def cite(keys: str) -> str:
    return '\\begin_layout Standard\n\\begin_inset CommandInset citation\nLatexCommand citep\nkey "' + keys + '"\n\n\\end_inset\n\\end_layout\n\n'


INTRO = p("A useful specification gives more than a closed-form answer: it identifies the assumptions behind expenditure shares, substitution, and corner choices. We derive several families from the same budget problem. Throughout, prices are strictly positive and wealth is positive; additional consumption-domain restrictions are stated for each model.") + block("Subsection", "Homotheticity and Cobb--Douglas Demand")

DIRECT = "".join([
    p(r"For $L$ goods, fix positive taste weights $\notationfirst{utility-weights}{a_\ell}$ with $\sum_{\ell=1}^{L}a_\ell=1$. Cobb--Douglas utility is $u(x)=\prod_{\ell=1}^{L}x_\ell^{a_\ell}$. Every boundary bundle has utility zero and a strictly positive affordable bundle has positive utility, so the optimum is interior. Maximizing its logarithm gives $a_\ell/x_\ell=\lambda p_\ell$. Multiplying by $x_\ell$ and summing gives $\lambda=1/w$, hence"),
    math(r"x_\ell(p,w)=a_\ell\frac{w}{p_\ell},\qquad \notationfirst{expenditure-shares}{b_\ell(p,w)}:=\frac{p_\ell x_\ell(p,w)}{w}=a_\ell."),
    p(r"The expenditure share $b_\ell$ is the fraction of the budget allocated to good $\ell$; the share vector is $\boldsymbol b=(b_1,\ldots,b_L)^\top$. Cobb--Douglas shares are constant even though quantities respond to prices. Each wealth elasticity is one, each own-price elasticity is minus one, and each uncompensated cross-price elasticity is zero."),
    block("Example", r"A fixed budget share. Let $a=(1/4,3/4)$, $p=(2,1)$, and $w=80$. Demand is $(10,60)$ and expenditure is $(20,60)$. Doubling only the first price halves $x_1$ while leaving $x_2$ unchanged. Doubling wealth doubles both quantities. A constant share is a restriction on behavior, not a property of all homothetic preferences."),
    block("Subsection", "CES: A Family of Substitution Patterns"),
    p(r"The constant-elasticity-of-substitution (CES) family varies substitution while retaining explicit demand. Keep the positive normalized weights above. Let $\notationfirst{ces-curvature}{\rho}<1$ and define the substitution elasticity $\notationfirst{substitution-elasticity}{\sigma}=1/(1-\rho)>0$. For $\rho\ne0$, use"),
    math(r"u_\rho(x)=\left(\sum_{\ell=1}^{L}a_\ell x_\ell^\rho\right)^{1/\rho}."),
    p(r"For $0<\rho<1$ this formula is defined on $\mathbb R_+^L$. For $\rho<0$, define it first on $\mathbb R_{++}^L$ and extend it continuously by assigning zero utility to bundles with any zero coordinate. At $\rho=0$, take the continuous limit $u_0(x)=\prod_\ell x_\ell^{a_\ell}$. Each representation is homogeneous of degree one. CES preferences are therefore homothetic, including cases in which expenditure shares vary with relative prices."),
    p(r"The optimum is interior. For $\rho\le0$, a positive bundle dominates every boundary bundle in utility. For $0<\rho<1$, a small transfer of expenditure toward a missing good is beneficial because its marginal utility becomes arbitrarily large near zero. For $\rho\ne0$, an equivalent objective on the positive orthant, including the sign needed when $\rho<0$, is"),
    math(r"\widetilde u_\rho(x)=\frac{\sum_\ell a_\ell x_\ell^\rho-1}{\rho},\qquad \partial_{x_\ell x_\ell}^{2}\widetilde u_\rho=a_\ell(\rho-1)x_\ell^{\rho-2}<0."),
    p(r"At $\rho=0$, instead use $\widetilde u_0(x)=\sum_\ell a_\ell\log x_\ell$, with own second derivatives $-a_\ell/x_\ell^2<0$. In both cases all cross derivatives vanish, so the objective is strictly concave. Its first-order conditions $a_\ell x_\ell^{\rho-1}=\lambda p_\ell$, together with budget exhaustion, identify the unique maximizer. For negative $\rho$, maximizing the untransformed sum of powers would reverse the intended ranking. Taking ratios and then imposing the budget gives"),
    math(r"\frac{x_\ell}{x_k}=\left(\frac{a_\ell/p_\ell}{a_k/p_k}\right)^\sigma,\qquad x_\ell(p,w)=\frac{w a_\ell^\sigma p_\ell^{-\sigma}}{\sum_{k=1}^{L}a_k^\sigma p_k^{1-\sigma}}."),
    p(r"The same demand formula applies at $\sigma=1$ and gives Cobb--Douglas. It satisfies Walras' law, has degree zero in $(p,w)$, and scales linearly with wealth. Its shares are"),
    math(r"b_\ell(p)=\frac{a_\ell^\sigma p_\ell^{1-\sigma}}{\sum_k a_k^\sigma p_k^{1-\sigma}}."),
    p(r"Except in the Cobb--Douglas case, a taste weight is generally not an expenditure share. Raising a good's price lowers its share if $\sigma>1$ and raises its share if $0<\sigma<1$, even though its purchased quantity falls in both cases. The name CES refers to the response of a quantity ratio to a relative price:"),
    math(r"-\frac{d\log(x_\ell/x_k)}{d\log(p_\ell/p_k)}=\sigma."),
    p(r"This relative-demand elasticity differs from an individual good's own-price elasticity. Differentiating the demand formula at fixed wealth gives, for $k\ne\ell$,"),
    math(r"\begin{aligned}\frac{\partial\log x_\ell}{\partial\log w}&=1,\\ \frac{\partial\log x_\ell}{\partial\log p_\ell}&=-\sigma(1-b_\ell)-b_\ell,\\ \frac{\partial\log x_\ell}{\partial\log p_k}&=(\sigma-1)b_k.\end{aligned}"),
    p(r"Thus every good is normal. Distinct goods are gross substitutes when $\sigma>1$ and gross complements when $0<\sigma<1$: these terms describe the cross-price response at fixed wealth. Chapter 2 separates this response into substitution and purchasing-power effects. In particular, a negative uncompensated cross effect need not imply a negative compensated cross effect."),
    block("Example", r"Substitution and relative expenditure. Let $a_1=a_2=1/2$, $\rho=1/2$, $p=(1,2)$, and $w=120$. Then $\sigma=2$ and the denominator is $1/4+1/8=3/8$, giving $x=(80,20)$. The quantity ratio is four but the expenditure ratio is two. The budget check is $80+2(20)=120$. The own-price elasticity of good 1 is $-4/3$, rather than $-2$."),
    block("Example", r"Gross complementarity. Let $a_1=a_2=1/2$, $\rho=-1$, $p=(1,4)$, and $w=90$. Here $\sigma=1/2$, demand is $(30,15)$, and shares are $(1/3,2/3)$. Raising only $p_2$ to 9 gives $(22.5,7.5)$. Both quantities fall: the greater purchasing-power burden outweighs the relative-price incentive to consume more of good 1."),
    block("Example", r"Weights versus shares in three goods. Let $a=(0.5,0.3,0.2)$, $\sigma=2$, $p=(1,1,1)$, and $w=38$. The denominator is $0.25+0.09+0.04=0.38$, so $x=(25,9,4)$. Shares are $(25/38,9/38,4/38)$, not the taste weights. The same weights under Cobb--Douglas give $(19,11.4,7.6)$. A change in curvature with weights fixed generally changes the reference allocation as well as price responses."),
    p(r"Calibration makes the distinction operational. Given positive reference shares $b_\ell^0=p_\ell^0x_\ell^0/w^0$ and a specified $\sigma$, weights reproducing that observation are"),
    math(r"a_\ell=\frac{(b_\ell^0)^{1/\sigma}(p_\ell^0)^{(\sigma-1)/\sigma}}{\sum_k (b_k^0)^{1/\sigma}(p_k^0)^{(\sigma-1)/\sigma}}."),
    p(r"One positive observation therefore cannot identify the substitution elasticity: each specified $\sigma$ admits calibrated weights. Different elasticities can fit the same initial allocation and predict different responses to a price change."),
    block("Subsection", "Limiting Cases: Substitutes and Complements"),
    p(r"Holding weights fixed, $\rho\to0$ gives Cobb--Douglas, $\rho\uparrow1$ gives $u(x)=\sum_\ell a_\ell x_\ell$, and $\rho\to-\infty$ gives $u(x)=\min_\ell x_\ell$. Fixed weights disappear in the last limit. Unequal required proportions instead arise by applying the CES aggregator to $x_\ell/d_\ell$, with $d_\ell>0$, before taking that limit. The endpoint models must be solved directly; their solutions need not satisfy the interior CES conditions."),
    block("Example", r"Perfect substitutes and a demand correspondence. For $u(x)=3x_1+x_2$, $p=(2,1)$, and $w=12$, utility per dollar is $3/2$ for good 1 and 1 for good 2, so the unique choice is $(6,0)$. At $p=(3,1)$ the two ratios tie: every nonnegative bundle satisfying $3x_1+x_2=12$ maximizes utility. Reporting a single demand formula would omit valid choices."),
    block("Example", r"Perfect complements and a kink. For $u(x)=\min\{x_1/2,x_2\}$, the consumer buys $x_1=2x_2$. At $p=(1,3)$ and $w=20$, the chosen bundle is $(8,4)$ because $2(4)+3(4)=20$. In general $x_2=w/(2p_1+p_2)$ and $x_1=2w/(2p_1+p_2)$. Tangency of differentiable indifference curves is unavailable at the optimum."),
    block("Subsection", "Subsistence and Stone--Geary Demand"),
    p(r"To allow expenditure shares to vary with wealth, introduce a nonnegative subsistence bundle $\notationfirst{subsistence-bundle}{\gamma}\in\mathbb R_+^L$. On $X=\gamma+\mathbb R_+^L$, let $u(x)=\prod_\ell(x_\ell-\gamma_\ell)^{a_\ell}$ with positive normalized weights. Suppose $w>p\cdot\gamma$. Setting $z=x-\gamma$ leaves discretionary wealth $w-p\cdot\gamma$, so Cobb--Douglas demand in $z$ gives"),
    math(r"x_\ell(p,w)=\gamma_\ell+a_\ell\frac{w-p\cdot\gamma}{p_\ell}."),
    p(r"At $w=p\cdot\gamma$, the only feasible bundle is $\gamma$; below that level this subsistence-constrained model has no feasible bundle. It is not a model of behavior below subsistence. Except in special cases, these preferences are not homothetic about the origin and their budget shares depend on wealth."),
    block("Example", r"A necessity and discretionary spending. Let $\gamma=(2,1)$, $a=(1/2,1/2)$, $p=(2,1)$, and $w=15$. Subsistence costs 5, leaving 10 to allocate; demand is $(4.5,6)$ and shares are $(0.6,0.4)$. At wealth 25, demand is $(7,11)$ and shares are $(0.56,0.44)$. The first good's share falls even though its quantity increases."),
    block("Subsection", "Quasilinearity and Wealth-Dependent Corners"),
])

AFTER_QUASILINEAR = "".join([
    p(r"A nonnegative numeraire creates a boundary that matters for demand. Let $u(x_1,x_2)=2\sqrt{x_1}+x_2$ on $\mathbb R_+^2$, normalize $p_2=1$, and write $r=p_1>0$. Substituting the budget gives the strictly concave problem $\max_{0\le x_1\le w/r}\{2\sqrt{x_1}-rx_1+w\}$. Its unique solution is"),
    math(r"x_1(r,w)=\min\{r^{-2},w/r\},\qquad x_2(r,w)=\max\{w-r^{-1},0\}."),
    block("Example", r"When zero wealth effects stop applying. At $r=2$ and $w=3$, demand is $(1/4,5/2)$: extra wealth is spent entirely on good 2. At $w=1/4$, demand is $(1/8,0)$ and all wealth is spent on good 1. The claim that quasilinear demand has no wealth effect for the non-numeraire good requires an interior numeraire choice, here $w>1/r$."),
    block("Subsection", "From CES to Flexible Translog Demand"),
    p(r"CES imposes one common, constant substitution elasticity. Applied demand analysis often needs substitution patterns that vary with relative prices. A translog specification uses a quadratic polynomial in logarithms, allowing such variation. Direct-utility, indirect-utility, and expenditure translog specifications are different parametric restrictions: the dual of a direct translog utility need not be translog. Chapter 2 develops a homothetic translog expenditure model, derives its demand shares, and checks the price region on which it represents a classical rational consumer. This order lets us explain the model through expenditure minimization rather than present an unexplained demand formula."),
    p(r"For further practice, Problems 1.2--1.5 compare these specifications. The artists case study, Problem 10.4, uses CES fan demand as the first stage of a model of streaming revenue, concert production, and ticket pricing; its consumer part can be completed now."),
    marker(STAMP),
])

DUAL = "".join([
    block("Section", "Workhorse Demand through Duality"),
    label("sec:workhorse-duality"),
    block("Subsection", "CES Expenditure, Compensation, and Substitution"),
    p(r"Keep Chapter 1's degree-one CES normalization. Its unit expenditure index $\notationfirst{unit-expenditure-index}{\mathcal P(p)}:=e(p,1)$ records the minimum cost of one unit of that utility index. Substituting the CES demand into utility, and then using duality, gives"),
    math(r"\mathcal P(p)=\begin{cases}\left(\sum_\ell a_\ell^\sigma p_\ell^{1-\sigma}\right)^{1/(1-\sigma)},&\sigma\ne1,\\ \prod_\ell(p_\ell/a_\ell)^{a_\ell},&\sigma=1,\end{cases}"),
    math(r"v(p,w)=\frac{w}{\mathcal P(p)},\qquad e(p,\bar u)=\bar u\mathcal P(p),\qquad h_\ell(p,\bar u)=\bar u a_\ell^\sigma p_\ell^{-\sigma}\mathcal P(p)^\sigma."),
    p(r"Here $\bar u>0$. The Cobb--Douglas factors $a_\ell$ in the unit expenditure formula follow from the chosen utility normalization; omitting them changes the utility units. Marshallian demand itself is unaffected by a positive rescaling of utility. Differentiating Hicksian demand gives own-price elasticity $-\sigma(1-b_\ell)$ and, for $k\ne\ell$, cross-price elasticity $\sigma b_k>0$. CES goods are compensated substitutes even when $\sigma<1$ makes them gross complements at fixed wealth."),
    block("Example", r"Exact compensation after a price increase. With equal weights, $\sigma=2$, $p^0=(1,2)$, and $w=120$, Chapter 1 found $x^0=(80,20)$. Here $\mathcal P(p^0)=8/3$ and initial utility is 45. If $p^1=(2,2)$, then $\mathcal P(p^1)=4$. Maintaining utility 45 requires wealth 180, so compensation is 60 and the compensated bundle is $(45,45)$. At unchanged wealth 120, the final bundle is $(30,30)$. For good 1, the total change $-50$ is the compensated change $-35$ plus the remaining wealth effect $-15$. This is a finite-change Hicks decomposition; the Slutsky equation describes the corresponding local derivative."),
    block("Subsection", "A Homothetic Translog Expenditure Model"),
    label("sec:translog-demand"),
    p(r"The translog family provides a flexible quadratic approximation in logarithms. We use a homothetic expenditure specification; richer translog families also permit wealth-dependent shares. Prices are measured relative to fixed reference units, so each logarithm is dimensionless. Write"),
    math(r"\log\mathcal P_{\mathrm{TL}}(p)=\alpha_0+\sum_{\ell=1}^{L}\alpha_\ell\log p_\ell+\frac12\sum_{\ell=1}^{L}\sum_{k=1}^{L}\gamma_{\ell k}\log p_\ell\log p_k."),
    p(r"The intercept is $\alpha_0$, the linear coefficients are $\alpha_\ell$, and the symmetric curvature matrix is $\notationfirst{translog-curvature}{\Gamma}=(\gamma_{\ell k})$. Impose $\sum_\ell\alpha_\ell=1$ and $\Gamma\mathbf1_L=0$. These restrictions make $\mathcal P_{\mathrm{TL}}$ homogeneous of degree one in prices. The matrix $\Gamma$ here is unrelated to the subsistence vector $\gamma$ in Stone--Geary utility. The translog approach originates with Christensen, Jorgenson, and Lau; the expenditure formulation and curvature calculation below also follow Diewert's treatment."),
    cite("christensenjorgensonlau1975,diewert2023"),
    p(r"Suppose the price region under study is regular, as specified below. With $e(p,\bar u)=\bar u\mathcal P_{\mathrm{TL}}(p)$ and $v(p,w)=w/\mathcal P_{\mathrm{TL}}(p)$, Shephard's lemma gives"),
    math(r"\begin{aligned}b_\ell(p)&=\frac{\partial\log\mathcal P_{\mathrm{TL}}(p)}{\partial\log p_\ell}=\alpha_\ell+\sum_k\gamma_{\ell k}\log p_k,\\ h_\ell(p,\bar u)&=\frac{\bar u\mathcal P_{\mathrm{TL}}(p)}{p_\ell}b_\ell(p),\qquad x_\ell(p,w)=\frac{w}{p_\ell}b_\ell(p).\end{aligned}"),
    p(r"Adding up and homogeneity follow from the coefficient restrictions, but nonnegative demand and substitution restrictions require more. On an open convex cone $\mathcal D\subseteq\mathbb R_{++}^{L}$, require $b_\ell(p)>0$ and the following matrix to be negative semidefinite at every price in $\mathcal D$:"),
    math(r"H(p):=\Gamma+\boldsymbol b(p)\boldsymbol b(p)^\top-\operatorname{diag}(\boldsymbol b(p))."),
    p(r"To see the role of this condition, let $D=\operatorname{diag}(p_1,\ldots,p_L)$. Differentiating $\partial_{p_\ell}\mathcal P_{\mathrm{TL}}=\mathcal P_{\mathrm{TL}}b_\ell/p_\ell$ yields"),
    math(r"\nabla_p^2\mathcal P_{\mathrm{TL}}(p)=\mathcal P_{\mathrm{TL}}(p)D^{-1}H(p)D^{-1}."),
    p(r"Thus $H(p)\preceq0$ is exactly the local curvature restriction. Requiring it throughout a convex price domain establishes concavity on that domain. Positive fitted shares alone do not establish rationalizability, and checking curvature at one observation does not justify a distant counterfactual. The Slutsky matrix is $S(p,w)=wD^{-1}H(p)D^{-1}$, so symmetry, negativity, and the zero price direction are explicit."),
    p(r"There is a direct optimizing model behind these formulas. Define, for $x\in\mathbb R_+^L$,"),
    math(r"u_{\mathcal D}(x)=\inf_{r\in\mathcal D}\frac{r\cdot x}{\mathcal P_{\mathrm{TL}}(r)}."),
    p(r"This is a nonnegative, concave, homogeneous, nondecreasing utility. At $p\in\mathcal D$, concavity and homogeneity of the price index imply $r\cdot\nabla\mathcal P_{\mathrm{TL}}(p)\ge\mathcal P_{\mathrm{TL}}(r)$ for every $r\in\mathcal D$, with equality at $r=p$. Hence $u_{\mathcal D}(\nabla\mathcal P_{\mathrm{TL}}(p))=1$. Scaling that bundle attains target utility $\bar u>0$ at expenditure $\bar u\mathcal P_{\mathrm{TL}}(p)$; any bundle reaching the target costs at least that much. This proves the expenditure formula, and therefore the displayed demand, at prices in $\mathcal D$. It does not extend the translog formula to prices outside its regular region."),
    p(r"The compensated and uncompensated elasticities make the extra flexibility visible. Let $\delta_{\ell k}$ equal one when $\ell=k$ and zero otherwise. Then"),
    math(r"\frac{\partial\log x_\ell}{\partial\log p_k}=\frac{\gamma_{\ell k}}{b_\ell}-\delta_{\ell k},\qquad \frac{\partial\log h_\ell}{\partial\log p_k}=\frac{\gamma_{\ell k}}{b_\ell}+b_k-\delta_{\ell k}."),
    p(r"Wealth elasticities are one in this homothetic version, while price elasticities vary with the shares. For two goods, the elasticity of substitution is $1+\gamma_{12}/(b_1b_2)$ on the regular region. With more goods the same expression is the Allen--Uzawa pairwise elasticity, rather than a universal elasticity of every quantity ratio. Setting $\Gamma=0$ recovers constant shares and a Cobb--Douglas price index. General translog utility models need not be homothetic."),
    block("Example", r"A translog model with changing shares. Let $L=2$, $\alpha_0=0$, $\alpha_1=\alpha_2=1/2$, and $\Gamma=\tfrac1{10}\left(\begin{smallmatrix}1&-1\\-1&1\end{smallmatrix}\right)$. Writing $r=p_1/p_2$ gives"),
    math(r"\mathcal P_{\mathrm{TL}}(p)=\sqrt{p_1p_2}\exp\!\left(\frac{(\log r)^2}{20}\right),\qquad b_1=\frac12+\frac{\log r}{10},\quad b_2=1-b_1."),
    p(r"At $p=(1,1)$ and $w=100$, demand is $(50,50)$. At $p=(2,1)$ and the same wealth, shares are approximately $(0.569315,0.430685)$ and demand is $(28.4657,43.0685)$. The first quantity falls while its budget share rises. The substitution elasticity changes from $0.6$ at equal prices to approximately $0.592162$ at $(2,1)$; a single CES elasticity cannot reproduce that variation throughout the region."),
    block("Example", r"Positive shares can conceal invalid curvature. In the preceding model, $H=(1/10-b_1b_2)\left(\begin{smallmatrix}1&-1\\-1&1\end{smallmatrix}\right)$. Shares are positive when $|\log r|<5$, but curvature holds only when $|\log r|\le\sqrt{15}$. Thus $|\log r|<\sqrt{15}$ defines an open convex cone on which the construction above is valid. At $r=\exp(4)$ the shares $(0.9,0.1)$ still look admissible, yet $1/10-b_1b_2=0.01>0$: compensated own-price responses have the wrong sign. This counterfactual must be rejected for this parameterization."),
])


def rewrite(source: str) -> str:
    if STAMP in source:
        return source
    heading = "\\begin_layout Section\nWorkhorse Utility Specifications\n\\end_layout"
    if source.count(heading) != 1:
        raise ValueError("workhorse heading missing or ambiguous")
    source = source.replace(heading, heading + "\n\n" + INTRO, 1)
    quasi = "\\begin_layout Definition\nQuasilinear preferences."
    if source.count(quasi) != 1:
        raise ValueError("quasilinear definition missing or ambiguous")
    source = source.replace(quasi, DIRECT + quasi, 1)
    provenance = "ECON803_CONSUMER_RESTRUCTURE_SOURCE:section:basics-of-consumer-theory:06:problems"
    anchor = source.index(provenance)
    anchor = source.rfind("\\begin_layout Standard", 0, anchor)
    source = source[:anchor] + AFTER_QUASILINEAR + source[anchor:]
    summary = "\\begin_layout Section\nWhat Utility Maximization Implies\n\\end_layout"
    if source.count(summary) != 1:
        raise ValueError("duality insertion point missing or ambiguous")
    source = source.replace(summary, DUAL + summary, 1)
    return source


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--source", type=Path, default=BOOK)
    parser.add_argument("--check", action="store_true")
    args = parser.parse_args()
    old = args.source.read_text()
    new = rewrite(old)
    if args.check:
        if new != old:
            raise SystemExit("workhorse expansion is pending")
        print("workhorse expansion is present")
    elif new != old:
        args.source.write_text(new)
        print(f"expanded native LyX workhorse material: {args.source}")


if __name__ == "__main__":
    main()
