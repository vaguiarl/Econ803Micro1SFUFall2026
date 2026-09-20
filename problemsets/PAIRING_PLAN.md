# Chapter use-case and release plan

The textbook, not the weekly packet, is the source of record. Every chapter closes with Core problems that can be solved by hand, followed by formal bridges and one capstone case. The capstone changes one named feature and requires a reproducible computational or formal check. Stable problem IDs make the book, released views, and private solutions auditable against one another.

`problems/CHAPTER_PATHWAYS.tsv` is the machine-readable authority for this table.

| Chapter | Part I: hand benchmarks | Final chapter use case | One scale axis | Primary tool |
|---:|---|---|---|---|
| 1 | 1.1, 1.2, 1.4 | 1.5 Household demand across subsistence and discretionary regimes | Wealth at fixed preferences and prices | Codex + Python |
| 2 | 2.1, 2.5 | 2.6 Local CES and translog welfare approximation | Distance from one reference price | Codex + Python |
| 3 | 3.1, 3.2, 3.3, 3.5 | 3.4 A counterfactual demand support set | Number of observed budgets | Codex + Python; Lean candidate certificates |
| 4 | 4.1 | 4.2 A menu-design rationality audit | Number of menus on a fixed alternative set | Codex + Lean |
| 5 | 5.1, 5.2 | 5.4 A multi-asset portfolio under risk | Number of jointly normal risky assets | Codex + Python |
| 6 | 6.1, 6.3 | 6.2 Red bus, blue bus, and duplicated products | Number of identical labels | Codex + Python |
| 7 | 7.1, 7.2 | 7.3 Paying for information before choosing | Number of matched state-action labels | Codex + Python |
| 8 | 8.1, 8.2 | 8.3 Aggregation when household wealth moves with prices | Number of consumers | Codex + Python; Lean finite-sum core |
| 9 | 9.1, 9.3 | 9.4 Input substitution in a multi-input firm | Number of inputs | Codex + Python; Lean finite algebra |
| 10 | 10.1 | 10.4 Music sales and concerts | Music-volume or royalty share | Codex + Python |
| 11 | 11.1 | 11.4 A consumer-owned firm | Production curvature | Codex + Python |
| 12 | 12.1 | 12.4 A coalition challenges a competitive allocation | Strength of the blocking predicate | Codex + Lean |
| 13 | 13.1 | 13.3 A counterfactual equilibrium identified set | Number of equilibrium observations | Codex + Python |
| 14 | 14.1, 14.2 | 14.3 Complete versus incomplete sequential markets | Rank of the asset span | Codex + Python; Lean target |
| 15 | 15.1 | 15.3 Housing allocation and coalitional stability | Number of agents and houses | Codex + Python; Lean target |
| 16 | 16.1, 16.2 | 16.3 A tariff counterfactual from partial to general equilibrium | One endogenous shared labor market | Codex + Python |
| Appendix A | A.1 | A.4 Finite preference completion and multiple utilities | Number of alternatives | Codex + Lean |

## Release rule

A weekly view may select the hand benchmarks needed for one meeting and add a workspace, due date, or starter file. When it releases a capstone, it must retain the stable IDs, assumptions, capstone identity, scale axis, and verification boundary from the chapter. A release that changes any of those is a revision to the textbook pathway and must update the canonical ledgers first.

## Verification rule

For every case, students record four lines before using a tool: **Seed**, **Fixed**, **Scaled**, and **Risk**. The artifact must reproduce the hand case, include one boundary or deliberately failing test, and distinguish the mathematical statement checked by Lean or code from the economic assumptions and interpretation. Compilation of a nearby theorem never certifies the entire case.
