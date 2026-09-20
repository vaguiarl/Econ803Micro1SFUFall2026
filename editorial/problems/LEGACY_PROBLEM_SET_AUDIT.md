# Western and SFU problem-set audit

## Editorial decision

The Fall 2026 problem bank is the canonical question source. Historical Western/UWO and SFU 2024 sheets are not copied verbatim: they mix obsolete numbering, duplicated questions, partial answer text, and several mathematically incorrect prompts or keys. Their durable ideas have been rewritten as the 48 non-case problems in the current book; the 17 chapter cases remain a separate assignment stream.

This audit records provenance and disposition without publishing solution text. Corrected instructor derivations and the approval ledger live only in the private Fall 2024 repository.

## Source inventory and canonical destinations

| Historical source | Main subject | Fall 2026 destination | Disposition |
|---|---|---|---|
| Western summer PS1 | Utility maximization, Cobb-Douglas, CES | 1.1-1.4 | Canonicalized and split into board-scale exercises |
| Western/SFU PS1 | Incomplete preference, multiple utility, finite choice | 4.1-4.3; A.1-A.4 | Rewritten; unsafe counterexamples removed |
| Western PS2-PS3; SFU PS2 | Duality, integrability, SARP, Afriat | 2.1-2.5; 3.1-3.6 | Canonicalized; implicit log-expenditure item quarantined |
| SFU PS3 | Sparse-max and perceived prices | 7.1-7.2 | Canonicalized with quantity/share notation separated |
| Western/SFU PS4 | Expected utility, portfolios, Allais | 5.1-5.4 | Portfolio core retained with its domain stated; incomplete Allais key quarantined |
| Western/SFU PS5 | Random utility and aggregation | 6.1-6.3; 8.1-8.3 | Selected core rewritten; probit and truncated-mean items quarantined pending fresh solutions |
| Western/SFU PS6 | Production, cost, profit | 9.1-9.4 | Canonicalized; historical mislabeled solution file not treated as a key |
| Western/SFU PS7 | Partial equilibrium, heterogeneity, IV | 10.1-10.3; 13.1-13.2 | Core economics retained; invalid numeraire/IV statements removed |
| Western/SFU PS8 | Edgeworth box, welfare, core | 11.1-11.3; 12.4 | Rewritten; broken figures and invalid welfare arguments removed |
| Western/SFU PS9 | Regularity, uniqueness, multiple equilibrium | 12.1-12.3 | General theory canonicalized; explicit numerical example held in reserve |
| Western PS10 | Contingent commodities, OLG, sequential trade | 14.1-14.3 | Asset-span core retained; unsafe parameter cases quarantined |
| Western PS11 | Matching and manipulation | 15.1-15.3 | Canonicalized |
| Fall 2026 additions | CGE and modern consumer theory | 8.3; 16.1-16.3 | New material; no historical source claimed |

## Material errors found in the archive

The following are source defects, not optional stylistic changes.

1. The old implicit log-expenditure exercise drops a quadratic term when recovering utility from expenditure shares and states an incorrect adding-up condition.
2. Several incomplete-preference examples use undefined alternatives or relations that fail the stated transitivity requirement.
3. A sparse-max exercise alternates between quantities and expenditure shares without changing its budget identity.
4. The binary-probit key uses the wrong variance for a difference of independent normal shocks.
5. An aggregation key writes the wrong sign in the own-good Slutsky expression and omits conditions needed for representative-demand claims.
6. A partial-equilibrium key has an incorrect numeraire-demand formula and proposes an invalid demand shifter as an instrument for demand estimation.
7. Several Edgeworth-box welfare arguments reverse the relevant budget inequalities; their absolute figure paths are also not portable.
8. A regularity solution treats gross substitutes as sufficient without the strictness or irreducibility needed for uniqueness.
9. A producer-theory solution filename actually contains answers to the following partial-equilibrium set.
10. A contingent-claims solution mishandles the cases at and above a unit curvature parameter, and an OLG golden-rule calculation confuses depreciation with the survival rate.
11. A 2024 midterm claim that pairwise intersection of multiple-utility criteria guarantees WARP is false.
12. A 2024 final asks for a Banach-contraction proof under a calibration whose Jacobian has norm one at a stated point, so the requested strict contraction does not follow.

## Admission rule

A historical item enters the public bank only when all four conditions hold:

1. its economic premise is still part of the Fall 2026 chapter map;
2. the question has a unique, well-defined mathematical target or explicitly requests a correspondence/set;
3. an instructor solution has been independently checked, including corner and boundary cases; and
4. the stable public identifier appears in the private solution-coverage check before a weekly packet can be approved.

Items failing one of these tests remain in the archive rather than being silently repaired in a released handout.
