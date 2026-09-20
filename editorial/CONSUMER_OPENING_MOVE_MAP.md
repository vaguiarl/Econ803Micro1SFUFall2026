# Consumer opening: intact-block move map

This is the mechanical first-pass map used by
`scripts/restructure_consumer_opening.py`. It is deliberately conservative:
every current `Section` block is moved whole, with all nested LyX layouts and
insets unchanged. Mixed sections are split only in the later editorial pass.

## Chapter 1. Utility Maximization and Consumer Demand

- `Basics of Consumer Theory / Preliminaries`
- `Basics of Consumer Theory / Environment: Commodities and Budget Set`
- `Consumer Theory: Utility Maximization / The Utility Maximization Problem`
- `Consumer Theory: Utility Maximization / Demand Correspondences`
- `Consumer Theory: Utility Maximization / KKT Conditions for the UMP`
- `Consumer Theory: Utility Maximization / Homothetic and Quasilinear Utility Functions`
- `Basics of Consumer Theory / Problems`
- The existing `Consumer Theory: Utility Maximization` chapter prologue is
  retained here under a non-exported provenance marker.

## Chapter 2. Duality, Comparative Statics, and Welfare

- `Consumer Theory: Utility Maximization / Properties of the Indirect Utility Function`
- `Consumer Theory: Utility Maximization / Roy's Identity`
- `Consumer Theory: Utility Maximization / Expenditure Minimization Problem (EMP)`
- `Consumer Theory: Utility Maximization / Hicksian Compensated Demand`
- `Consumer Theory: Utility Maximization / KKT Conditions for the EMP`
- `Consumer Theory: Utility Maximization / Shephard's Lemma`
- `Consumer Theory: Utility Maximization / Additional Properties`
- `Consumer Theory: Utility Maximization / Summary of Relationships between the EMP and UMP`
- `Consumer Theory: Utility Maximization / Slutsky Equation`
- `Consumer Theory: Utility Maximization / Summary of the Implications of Utility Maximization`
- `Consumer Theory: Utility Maximization / Welfare Evaluation`

## Chapter 3. Revealed Preference and Recoverability

- `Basics of Consumer Theory / Demand Functions`
- `Basics of Consumer Theory / Consistency in Consumption`
- `Basics of Consumer Theory / Comparative Statics and Slutsky Matrix`
- `Consumer Theory: Utility Maximization / Integrability`
- `Consumer Theory: Utility Maximization / Examples and Applications of Demand Integrability`
- `Consumer Theory: Utility Maximization / Generalized Axiom of Revealed Preference (GARP)`
- `Consumer Theory: Utility Maximization / Revealed Preference and the Strong Axiom`
- `Consumer Theory: Utility Maximization / Forecasting with Varian's Support Set`
- `Consumer Theory: Utility Maximization / Upper Bounds for Welfare Analysis`
- `Consumer Theory: Utility Maximization / Experiments about Testing Rationality`
- `Consumer Theory: Utility Maximization / Results`
- `Consumer Theory: Utility Maximization / Afriat's Cost-Efficiency Index`
- `Consumer Theory: Utility Maximization / Measurement Error`
- `Consumer Theory: Utility Maximization / Problems`

## Chapter 4. Choice Without Budget Geometry

- `Preference and Choice / From Choice Data to Preference`
- `Preference and Choice / Choice environments`
- `Preference and Choice / Preference relations`
- `Consumer Theory: Utility Maximization / Utility Representation`
- `Preference and Choice / Revealed choice and WGARP`
- `Preference and Choice / GARP on finite data`
- `Preference and Choice / Problems`

## Intentional limitations

- The script does not yet split the current mixed `Consistency in Consumption`
  or `Comparative Statics and Slutsky Matrix` sections. Their Walras/HD0,
  Slutsky, and revealed-preference components require an editorial split after
  the byte-preserving move.
- It does not merge the EMP/Hicksian/Shephard sequence or the experiment,
  results, CCEI, and measurement-error sequence.
- It preserves all three generated `Problems` sections exactly where shown;
  problem-by-prerequisite redistribution is a later problem-bank operation.
- It preserves the old utility-maximization chapter prologue even though its
  roadmap becomes stale. The prose should be rewritten only after the move has
  passed the source/PDF comparison checks.
- It adds new chapter shells, questions, semantic labels, old-label aliases,
  and collapsed provenance notes. It does not claim that the moved prose is
  already a finished editorial revision.
