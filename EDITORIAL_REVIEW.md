# Editorial review: publication baseline

**Manuscript:** *Microeconomic Theory I* (ECON 803, Fall 2026)
**Authoritative source:** `notes/Microeconomics_1_notes_by_Victor_Aguiar.lyx`
**Review date:** 19 September 2026

## Editorial judgment

The manuscript is now a coherent textbook candidate rather than a collection of lecture notes. Its mathematical spine, notation, chapter sequence, theorem apparatus, references, and assessment workflow have been regularized sufficiently for a first public classroom edition. It should not yet be described as press-ready: figure rights and provenance, independent mathematical review, professional copyediting, and final typeset inspection remain publication gates.

The intended identity is clear and defensible: a modern graduate microeconomics text with the navigational breadth of Mas-Colell, Whinston, and Green, extended by revealed preference, behavioral models, random choice, empirical equilibrium restrictions, matching, sequential trade, and computable equilibrium. The text should retain that identity rather than imitate another book chapter by chapter.

## Architecture and editorial control

The book has five parts, sixteen substantive chapters, an order-theory appendix, a technical theorem-record appendix, and a linked glossary of symbols. The physical reading order now begins with utility maximization and consumer demand, proceeds through duality and welfare, and then treats revealed preference as the observable content and extension of the benchmark model. Abstract choice, risk, stochastic choice, attention, and aggregation follow without restarting the consumer theory. The logical dependency map correctly treats order theory as foundational even though it is placed in Appendix A. `BOOK_MAP.md` records the full sequence and identifies repeated section titles. Material that legitimately recurs—WARP, GARP, Slutsky restrictions, aggregation, and equilibrium—is separated by purpose and level of abstraction rather than repeated as parallel introductions.

The principal repository controls are:

- `NOTATION.md` is the book-wide notation and typographic standard.
- `editorial/notation/glossary.tsv` records the stable semantic IDs used to validate linked first uses and glossary definitions; it does not supersede the LyX manuscript.
- `BOOK_MAP.md` records chapter architecture, formal-block counts, and duplicate headings.
- `formal/COVERAGE.md` states the verification level of each major topic.
- `formal/theorem_inventory.tsv` indexes the manuscript's definitions, results, proofs, and examples.
- `formal/theorem_pairs.tsv` gives 24 stable reader/full theorem identifiers, records migration and proof status separately, and forbids completion overclaims.
- `FIGURE_AUDIT.md` records every live and legacy figure's technical quality, provenance, rights status, and disposition.

Theorem-like environments now use a common counter reset by chapter, and every chapter has a stable label. The bibliography contains 30 primary or standard sources, with citations attached to the relevant representation, duality, equilibrium, revealed-preference, experimental, matching, attention, and extension results.

## Mathematical and expository revision completed

The revision concentrated on places where compressed lecture notation could change a theorem's meaning. The principal improvements are:

- consumer theory now states domains, differentiability, constraint qualifications, boundary conditions, and the hypotheses needed for Roy's identity, Shephard's lemma, Slutsky differentiation, and duality;
- finite revealed preference distinguishes direct comparison, transitive closure, strict affordability, GARP, SARP, and Afriat efficiency, with the boundary-slack and finite-feasibility arguments repaired;
- expected utility distinguishes affine from linear representations, finite from infinite lottery domains, and weak convergence from finite-mixture arguments;
- aggregation separates individual restrictions from restrictions that survive aggregation and corrects the normalization used in the WARP discussion;
- production and cost theory now exposes attainment, local regularity, corner inequalities, output complementarity, and the conditions under which envelope formulas apply;
- partial and general equilibrium now state feasibility and market clearing exactly, distinguish equilibrium from quasi-equilibrium, and make the local-nonsatiation step in the welfare arguments explicit;
- positive equilibrium theory distinguishes correspondences from differentiable selections and states the hypotheses used for existence, local regularity, index arguments, gross substitutes, and core convergence;
- the Brown--Matzkin chapter now separates observed prices, individual incomes, and aggregate endowment from latent individual endowments, and presents the test as a finite semialgebraic feasibility problem;
- sequential trade makes the Arrow--Debreu/Radner spanning assumptions and state-price mapping explicit;
- matching distinguishes the ordinary core from the strong core and states the scope of deferred-acceptance and top-trading-cycles results;
- the CGE chapter now closes the model with household income and demand, goods and factor markets, government and external balances, a numeraire, and explicit replication and welfare checks;
- Appendix A distinguishes maximal from greatest elements, repairs the completeness requirement, and gives a substantive proof route for order extension rather than treating it as immediate.

This is a high-value correctness pass, not a substitute for external peer review of every theorem.

## Notation policy

The manuscript's defaults are now stable: $L$ and $\ell$ index commodities; $i$ indexes consumers; $j$ indexes firms; $s,t=1,\ldots,T$ index observations; $p,w$ denote prices and wealth; $x,h,v,e$ denote Marshallian demand, Hicksian demand, indirect utility, and expenditure. Bundles are column vectors, $a\cdot b$ is an inner product, $a^\top$ is a transpose, and a prime identifies an alternative object. Maps display their domains, and functions are distinguished from correspondences. Local exceptions—for lotteries, matching markets, and social-accounting notation—must be announced where introduced.

These conventions should be treated as a style sheet: later additions must not silently introduce competing index families, transpose conventions, or meanings for strict inequalities.

The `.lyx` manuscript remains the canonical source for notation definitions and link placement. In the built PDF, each tracked symbol at first use links to its entry in the final glossary, and the symbol in the glossary links back to that first use. The release validator checks the TSV ledger against those source-level links and requires the glossary to remain the final content chapter before the bibliography.

## Formal verification: precise claim boundary

The book is **not** fully Lean verified, and no release language should imply that it is.

| Material | Current assurance |
|---|---|
| Relation parts, finite greatest elements, transitive closure, and order extension | Local Lean proof plus textbook exposition |
| Rational choice, set-valued WARP, and strict dominance | Local Lean proof plus textbook exposition |
| GARP, Afriat inequalities, budget exhaustion, and compensated demand | Exact wrappers around a pinned WGARP commit, compiled in the same Lake build |
| Finite WGARP and coherent CMU | Checked wrapper around the pinned six-way finite characterization; the bridge to the book's broader compact-coalition formulation remains explicit |
| WARP and strict coherent CMU | Cited theorem only; the pinned project has no WARP/strict-star-concavity certificate, so no Lean verification is claimed |
| Consumer/firm value-function algebra, finite stochastic dominance, and welfare/core price arguments | Delimited local Lean cores; the coverage ledger names each missing analytic or model-encoding bridge |
| Narrative dependency order | Lean-checked structural map only; it does not prove the economic claims |
| Standard analysis, representation, equilibrium, and matching results | Audited textbook proof or an explicit citation, as recorded in `formal/COVERAGE.md` |
| Calibrations and model applications | Algebraic/expository verification |

The release script rejects Lean placeholders and local axioms, builds the pinned local and WGARP libraries, prints the kernel assumptions of every public certificate, and validates a 32-target machine-readable coverage ledger. The theorem-pair ledger currently records 24 pairs: 2 migrated, 19 planned, and 3 source-gated. This transparent, result-level ledger is preferable to a blanket verification claim.

## Problems and solutions

The canonical public bank contains 57 question-only problems covering every chapter and Appendix A. Stable identifiers and the labels **Core**, **Proof**, and **Applied** permit later syllabus and weekly-release references without renumbering. The alias table in `problems/PROBLEM_ID_ALIASES.tsv` preserves references to pre-restructure identifiers. An idempotent generator inserts the bank into the LyX manuscript, and the release check rejects a manuscript that has drifted from the bank.

Solutions are maintained in a separate private instructor handbook and must never enter the public repository or its reachable Git history. Before assigning a set, its public prompt and private solution should be checked together for identical assumptions, notation, subpart order, and numerical data. Weekly standalone sheets may select from the same stable bank; the public textbook remains the question-only source of record.

## Release inspection completed

The classroom-edition PDF has received a whole-book visual inspection. All 137 pages were rendered and reviewed in order, including every chapter opening, displayed-mathematics spread, problem section, both appendices, the linked glossary, and the bibliography. No clipped text, overlapping objects, malformed equations, broken headings, or unintended blank pages were found. `scripts/check_book.sh` independently rebuilds the five vector figures, compiles the book, and verifies that the final PDF contains no raster images, Type 3 fonts, or unembedded fonts.

The public-tree assessment check also passes: the release contains the 57 question-only problems but no solutions, answer keys, examinations, or unreleased weekly sets. This inspection establishes a classroom-edition baseline; it does not replace press production review or independent mathematical refereeing.

## Remaining publication gates

### Required before wide commercial circulation

1. **Close the remaining figure-rights record.** All five live PNG/screenshot figures have been replaced by reproducible vector artwork with self-contained captions and primary citations. The two plots reconstructed from Quah's vector slides still require permission for wide commercial circulation or a fresh reconstruction from licensed experimental data. Unreferenced scan-like legacy assets should remain outside the production tree and be retained only in a private provenance archive.
2. **Obtain an independent mathematical sign-off.** At minimum, assign separate reviewers to consumer/revealed-preference material; production and equilibrium; and risk, random choice, matching, and the mathematical appendix. Track each correction against the theorem inventory.

### Required before submission to an academic press

3. **Commission a professional copyedit.** Apply one publisher style consistently to capitalization, punctuation, displayed equations, theorem names, hyphenation, terminology, citations, and bibliography. The copyeditor should work from LyX and return a change log rather than flattening the source into a one-off PDF.
4. **Complete publisher-facing apparatus.** Add a preface defining prerequisites and scope, a reader's guide, chapter objectives and summaries, a subject index, and acknowledgments; retain and polish the linked notation glossary. Audit every cross-reference and bibliography entry against the original publication.
5. **Make the book accessible and reproducible.** Provide meaningful figure descriptions, selectable mathematical text, embedded fonts, bookmarks, and reproducible source data or code for redrawn figures. Pin the Lean and WGARP toolchain versions used for any formal-verification statement attached to a release.
6. **Independently test the assessment system.** Have a second solver complete every problem without the handbook, then reconcile the solution, difficulty label, prerequisites, expected time, and any admissible alternative answer.

## Release recommendation

Treat the current manuscript as a strong **classroom edition** and an auditable publication baseline. Describe Lean coverage by result and link to the coverage ledger; do not call the book fully formalized. Reserve “publication-ready” for the later edition that has cleared the two remaining figure permissions, external mathematical review, professional copyediting, and press-quality production review.
