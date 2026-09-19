# Front-matter and consumer-theory notation audit

## Scope and method

This audit covers current LyX source lines 191--6136: the global notation chapter, *Basics of Consumer Theory*, *Preference and Choice*, *Consumer Theory: Utility Maximization*, and *Behavioral Economics: Sparse-Max and Rational Inattention*. The `.lyx` file remains the authoritative source and was not edited. `front.tsv` records substantive notation rather than disposable variables bound inside a single proof or display.

The audit finds a strong core notation system, but not yet a publication-ready one. Most primitive consumer-theory objects are introduced clearly. The main editorial problem is semantic collision: the same glyph is assigned several durable meanings, sometimes only a page or two apart. Several operators and domain conventions also appear before they are defined.

## Critical findings

1. **Five high-frequency glyphs are materially overloaded.** `$I$` means the number of consumers (line 220), the symmetric part of a preorder (line 2155), and an identity matrix (line 5798). `$S$` means the Slutsky matrix (line 717) and Varian's support set (line 4644). `$m$` means money-metric utility (line 4672), price attention (line 5792), and a Gaussian posterior weight (line 5849). `$C$` is allowed as a choice rule (line 345), then becomes an integration constant (line 3850) and an information-cost function (line 5859). `$\ell$` is the commodity index (line 207) and a loss function (line 5840). These require renaming, not merely glossary qualifications.

2. **Revealed preference has three competing languages.** The opening chapter uses `$R^D$`; abstract choice uses `$\succeq^D,\succ^D,\succeq^*$`; the Afriat chapter returns to `$R^D,P^D,R$`, then adds efficiency-adjusted versions. The strict relation `$P^D$` also collides visually with the price domain `$P$`. A single system should be imposed book-wide. The cleanest is `$\succeq^D$` (direct weak), `$\succ^D$` (direct strict), and `$\succeq^R$` (reflexive-transitive closure), with a domain qualifier only when necessary.

3. **The integrability example is not notation-complete.** `$\mu$` first appears at line 3804 with no economic definition or declared domain. Its arity changes from `$\mu(p_1,1)$` to `$\mu(p_1)$` and then to `$\mu(p^*,p_1,w)$`. The example must first define the price path, the wealth/expenditure solution along that path, its initial condition, and the reference price; only then should it solve the ODE.

4. **Observation indexing is inconsistent.** Budget data use superscripts `$p^t,x^t$`, measurement error switches to subscripts `$p_t,x_t$`, and the support-set section introduces an undefined `$K+1$` although the sample size is `$T$`. Choose superscripts for observation indices throughout and use `$T+1$` for a new observation.

5. **Star and prime conventions are violated early.** The notation chapter reserves primes for alternative objects, but WARP uses `$(p^*,w^*)$` as the second observation. Stars later denote optimizers and a normalized reference price. Use `$(p',w')$` for alternatives and reserve `$*$` for optimizers.

6. **Several expressions are genuinely undefined at first use.** These include `$2^X$`, `$\rightrightarrows$`, `$\|\cdot\|$`, `$\arg\max$`, `$\arg\min$`, `$p_{-L},x_{-L}$`, `$D_p^2e$`, the identity matrix `$I$` and its dimension, `$S^s,S^r$`, `$\mathcal N$`, and the expectation operators. `$p\gg0$` is used repeatedly without a componentwise-order convention. Most need only one-line glossary entries; `$\mu$` and `$S^s,S^r$` require substantive repair in the chapter text.

## Major consistency findings

- `$x$` is simultaneously a bundle, a function, and a correspondence. This is conventional but must be type-disciplined: define Marshallian demand as a correspondence by default, and say explicitly when uniqueness licenses function notation.
- Commodity indices switch from `$\ell,k$` to `$i,j$` in the scalar Slutsky formula at line 3734, despite `$i$` and `$j$` being globally reserved for consumers and firms. Use `$[S(p,w)]_{\ell k}$` everywhere.
- The generic quadratic-form vector `$v$` at line 3510 conflicts with indirect utility `$v(p,w)$`. Rename the vector `$z$`.
- The behavioral chapter's `$x^s$` conflicts with the observation superscript `$s$`; `$x^{\mathrm{SM}}$` is unambiguous. Likewise `$x^r$` should be `$x^{\mathrm M}$` or another explicitly linked benchmark-demand symbol.
- Group labels `$R,B$` at line 5901 conflict with the revealed-preference relation `$R$` and budget set `$B$`. Neutral labels `$g\in\{0,1\}$` avoid both the mathematical collision and unintended semantic loading.
- `$\sim$` legitimately means both indifference and “distributed as.” This conventional overload can remain, but the glossary must list both syntactic uses.
- `$\log$` should be declared natural logarithm. The rational-inattention formulas then measure information in nats; another base requires an explicit unit conversion.
- The UMP KKT display introduces `$\lambda^*$` without explicitly stating `$\lambda^*\ge0$`. This is a definition/completeness issue, not just typography.

## Canonical renaming set

The following small renaming set resolves most collisions without changing the mathematics:

| Current | Canonical |
|---|---|
| indifference relation called `$I$` | use the existing `$\sim$` |
| identity `$I$` | `$I_L$` |
| Varian support set `$S$` | `$\mathcal V$` |
| money metric `$m(p,x)$` | `$\mu_p(x)$` |
| attention weights `$m_\ell$` | `$a_\ell$` |
| Gaussian posterior weight `$m$` or `$\alpha$` | `$\gamma$` |
| information cost `$C$` | `$\mathcal C$` |
| quadratic loss `$\ell$` | `$\mathscr L$` |
| integration constant `$C$` or `$K$` | `$K_0$` |
| sparse demand `$x^s$` | `$x^{\mathrm{SM}}$` |
| behavioral posterior mean `$m_G$` | `$\mu_g$` |
| measurement errors `$w_t^c,w_t^p$` | `$\eta_t^x,\eta_t^p$` |

## LyX-native glossary and hyperlink strategy

LyX must remain the source of truth. The glossary should therefore be a real final LyX chapter, not a generated TeX file pasted back into the project.

1. Add a final unnumbered chapter **Glossary of Symbols and Operators** in the `.lyx` document. Organize it by *Sets and indices*, *Choice and preference*, *Consumer duality*, *Revealed preference and data*, *Probability and attention*, and *Operators*.
2. Give every glossary entry a native LyX label using the stable anchors in `front.tsv`, for example `not:slutsky-matrix`.
3. At the first semantic occurrence of each symbol, add a native LyX cross-reference immediately after the defining phrase. Because `\use_hyperref true` is already set at source line 57, the resulting PDF reference will be clickable. If the symbol itself must be the clickable object, use a narrowly defined LyX flex inset backed by `\hyperref[anchor]{symbol}`; do not replace ordinary mathematics throughout the source with raw ERT.
4. Link once at the global first definition and again only when a chapter explicitly changes scope, such as generic `$X$` in *Preference and Choice*. Linking every repeated occurrence would make the PDF visually noisy and the LyX source hard to maintain.
5. Keep the glossary definition normative and chapter prose pedagogical. A glossary entry should state type, domain, codomain, indexing set, and scope in one or two lines; it should not carry theorem assumptions.
6. Add an automated check that each `not:*` first-use reference resolves, each glossary label is unique, and every TSV symbol marked `UNDEFINED` or `CONFLICT` is either repaired or explicitly waived.

## Counts

`front.tsv` contains 120 audited notation entries or distinct semantic senses. Statuses distinguish harmless scoped reuse from symbols requiring editorial repair. The highest-priority repair queue is: `CONFLICT`, `OVERLOADED`, `UNDEFINED`, `INCONSISTENT`, then `PARTIAL`; `OK` entries can be transferred directly into the glossary. The status counts should be regenerated automatically when the three regional ledgers are merged rather than maintained manually in prose.
