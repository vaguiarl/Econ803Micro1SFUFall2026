# Notation audit and resolution record

This record consolidates the three regional audits into the decisions encoded
in the [house notation standard](NOTATION.md) and the machine-readable
[glossary](editorial/notation/glossary.tsv). The regional files preserve the
pre-revision evidence; the disposition below records the repairs incorporated
into the canonical LyX manuscript.

## Scope

The source audit covered the full mathematical manuscript in three slices:

- [Front matter and consumer theory](editorial/notation/front.md), source lines
  191--6136.
- [Uncertainty through the opening of firm theory](editorial/notation/middle.md),
  source lines 6137--9496.
- [Firm theory through the order-theory appendix](editorial/notation/back.md),
  source lines 8998--13457.

The overlap around firm theory is intentional: it exposes changes of type at a
chapter boundary. The middle and back audits record manuscript snapshot
SHA-256
`4042efb9bd579196640fcd36e049b778377eb46e4459298d8a719574e3e1cc76`.
Disposable variables bound within a single proof or display were excluded;
persistent problem notation was retained when it exposed a collision. The
regional TSV and Markdown files are immutable audit snapshots. The integrated
revision subsequently edited both the LyX manuscript and the public problem
bank without rewriting those snapshots.

## Counts

| Region | Audited senses | Defined by first use | Not defined by first use |
|---|---:|---:|---:|
| Front | 120 | 82 | 38 |
| Middle | 150 | 106 | 44 |
| Back | 192 | 141 | 51 |
| **Total** | **462** | **329** | **133** |

The regional status taxonomies differ, so their labels should not be added
across regions as though they were one scale. The exact counts are:

| Region | Status counts |
|---|---|
| Front | 34 OK; 6 scoped; 2 overloaded; 28 conflict; 30 partial; 11 undefined; 9 inconsistent |
| Middle | 41 OK; 59 overload; 20 define; 12 forward; 6 conflict; 8 standardize; 4 incomplete |
| Back | 65 OK; 18 local OK; 15 standard; 38 overloaded; 12 conflict; 7 inconsistent; 10 late-defined; 7 undefined; 11 underdefined; 5 ambiguous; 4 notation drift |

The consolidated glossary contains **115 registered semantic IDs in 16
categories**. Every row has the required seven fields, every ID is unique, and
all 115 rows currently request linked first-use and definition targets. The
glossary is deliberately smaller than the 462-row audit: it includes
book-level and durable chapter-level objects, not every local semantic sense.

## Critical collisions and resolutions

| Collision or drift | Adopted resolution |
|---|---|
| Commodity coordinate $\ell$ also used as labor or a loss | Reserve $\ell,k$ for commodities; use $n$ for labor and $\mathscr L$ for loss. |
| Primes, stars, and observation labels compete | Primes mark alternatives, stars mark solutions/equilibria, and superscripts $s,t$ mark observations. |
| $p$ denotes a commodity price, lottery, scalar output price, and other prices | Keep $p$ as the commodity-price vector; use $\mu,\nu,\eta$ for lotteries and $p_q$ for the scalar output price. Typed chapter-local asset prices remain $q$. |
| Revealed preference alternates among $R^D$, $P^D$, $R$, $\succeq^*$, and decorated variants | Use $\succeq^{R,D}$, $\succ^{R,D}$, and $\succeq^R$ for budget data, following Aguiar--Hjertstrand--Serrano--Evren. Use $\succeq^C$, $\succ^C$, and $\succeq^{C*}$ for abstract menu choice. Reserve $R^*$ for a generic relation's reflexive-transitive closure in the appendix. |
| $I$ denotes consumer count, identity, and indifference | Keep $I$ for consumer count, $I_L$ for identity, $\sim$ for preference indifference, and $I_R$ for the symmetric part of a generic relation. |
| $S$ denotes the Slutsky matrix, Varian support, a state space, coalition, and feasible subset | Use $S(p,w)$, $\mathcal S_{\mathcal O}(p,w)$, and $\mathcal S$ for the first three; coalition and feasible-subset notation must remain locally typed. |
| $m$, $\mu$, $\pi$, and $\rho$ carry several unrelated probability, multiplier, matching, attention, premium, and profit meanings | Use $a_\ell$ for attention, $\gamma$ for posterior weight, $\varphi$ for matching, $\varpi_s$ for state probabilities, $P$ for choice probability, named `RP`/`PP` operators for premiums, and $\pi_Y$ for profit. Qualify multipliers by role. |
| $C$ denotes choice, production cost, information cost, and an integration constant | Use $c$, $C(\boldsymbol w,q)$, $\mathcal C$, and $K_0$, respectively. |
| Demand and supply alternate silently between correspondences and vectors | Demand is a correspondence unless uniqueness is stated; use $\mathcal Y_Y(p)$ and $\mathcal Z(\boldsymbol w,q)$ for supply and factor-demand correspondences and lowercase letters only for declared selections. |
| Agent, commodity, state, and observation indices change order | Use entity-first arrays: $x_{i\ell}$ and $x_{is\ell}$; reserve $i$ for consumers, $j$ for firms or locally declared alternatives, $\ell,k$ for commodities, and $s,t$ for states or observations as declared. |
| Generic and chapter-specific $R$, $q$, $w/W$, $z$, $M$, and $\Delta$ collide | Retain only typed, announced chapter-local reuse; use boldface or calligraphic forms where the glossary prescribes them. Every distinct persistent sense gets its own semantic anchor. |

## Audit findings and current disposition

The count of 133 definition-order gaps is a baseline measurement, not the
current defect count. The integrated pass made the following repairs:

1. **Definition order:** 115 durable objects now have exactly one linked first
   use and one glossary definition. Local proof variables remain subject to
   ordinary editorial review rather than glossary registration.
2. **Integrability:** the expenditure path now has a declared domain, initial
   condition, and reference price; the earlier untyped use of bare $\mu$ has
   been removed.
3. **Uncertainty:** finite and general lottery domains are separated, FOSD is
   typed on an ordered outcome space, random utility has a probability space,
   and risk aversion no longer compares an out-of-domain degenerate lottery.
4. **Discrete choice:** attributes, coefficient dimensions, shocks, mean
   utilities, conditional choice probabilities, and the expected-maximum
   function $\mathcal V(v)$ are introduced in dependency order.
5. **Firm theory:** vector and scalar prices, supply and factor-demand
   correspondences, and the hypotheses behind Hotelling and Shephard results
   are now distinguished explicitly.
6. **General equilibrium:** ownership, utility representations, the Pareto
   improver index, behavioral demand, and Jacobian transposes have been typed
   or disambiguated before use.
7. **Sequential trade and matching:** the consumer population, payoff and
   price vectors, matching signature, and unmatched-agent convention are now
   stated locally.
8. **CGE:** household, sector, factor, domestic-price, world-price, exchange-
   rate, tariff, and resource-balance objects now form a closed reproducible
   system with a declared nominal normalization.
9. **Order theory:** $\Delta_X$, $I_R$, relation composition, quotient objects,
   and extension notation are introduced in logical order. Appendix A remains
   the mathematical appendix even when a first-use link originates earlier.
10. **Typography and accessibility:** the final PDF preserves bold,
    calligraphic, uppercase, and lowercase distinctions, embeds every font,
    contains no raster figures, and exposes both directions of all 115
    notation links. Full tagged-PDF and spoken-math accessibility remain a
    later production task.

## Link architecture

The links use semantic IDs rather than glyphs, chapter numbers, or source-line
numbers. This permits deliberate scoped reuse without anchor collisions.

1. `editorial/notation/glossary.tsv` is the registry. Each row stores a unique
   `id`, visible symbol, category, scope, normative definition, first section,
   and link status.
2. The first global substantive use is wrapped once as
   `\notationfirst{id}{symbol}`. A later change of mathematical type uses a
   different semantic ID rather than a second target with the same ID.
3. The final LyX glossary defines the same ID once with
   `\notationdef{id}{symbol}` and displays the symbol, type/domain, definition,
   and scope. The glossary is the final content chapter before the
   bibliography.
4. `\notationfirst` links forward to `notation-def-id`; `\notationdef` links
   back to `notation-use-id`. Routine repetitions, bound indices, and
   one-display variables remain unlinked.
5. `scripts/validate_notation.py` checks the seven-column schema, unique and
   legal IDs, exactly one first-use and definition call for every row marked
   `linked`, unique generated anchors, first-use order, and glossary placement.
   It reports defects but never rewrites the manuscript.

With 115 rows marked `linked`, the completed manuscript architecture contains
115 first-use calls and 115 definition calls. Release readiness requires the
validator to pass; a ledger status of `linked` by itself is not proof that all
legacy prose has been normalized.
