# ECON 803 two-part chapter and problem-set standard

## Purpose

Every chapter ends with a model that can be solved and discussed by hand, then one named use case that scales the model with Codex, Lean, or a small transparent program. The end-of-chapter section is authoritative; a weekly packet is a synchronized release view. The second part is not a request to outsource the first part. It is an exercise in stating a generalization, constructing a verifiable artifact, and separating mathematical verification from economic interpretation.

## Part I: By hand

Each set contains two or three compact problems. A good Part I problem:

- has numerical values or a two- or three-element domain chosen to keep arithmetic clean;
- makes one economic point rather than surveying an entire chapter;
- can be completed in roughly 10-15 minutes at the board;
- asks for a derivation, a check, and a one-sentence interpretation; and
- exposes the assumption that will matter in Part II.

Students may compare handwritten work in class, but the submitted reasoning must be their own.

## The bridge

Before using a tool, students complete this four-line bridge:

| Question | Required answer |
|---|---|
| Seed | Which Part I result is being extended? |
| Fixed | Which preferences, technology, equilibrium concept, or behavioral assumptions remain unchanged? |
| Scaled | Is the extension in dimension, observations, parameters, or theorem strength? |
| Risk | What new failure mode becomes possible after scaling? |

This dependency order is mandatory: economic premise and model assumptions precede the scaled claim; the verified artifact precedes its interpretation. A program or Lean proof can check a stated implication, but it cannot establish that the assumptions are economically appropriate.

## Part II: Chapter use case and verified scale-up

Proof and Applied problems may provide intermediate bridges, but the final problem in every chapter is the designated use case. Its public pathway must name the hand benchmark, exactly one scale axis, the primary tool, the deterministic checks, and the boundary of current Lean coverage.

Every scale-up names one primary tool.

- **Codex + Python:** for calibration, enumeration, comparative statics, plots, or counterexamples. The submission includes executable source, a small test suite, and a concise table or figure.
- **Codex + Lean:** for definitions, algebraic implications, finite arguments, and reusable theorem statements. The submission includes a compiling Lean file and its trust report.
- **Codex + Python + Lean:** when computation suggests a claim and Lean verifies the exact symbolic core. Numerical evidence and proof must be reported separately.

The tool task must specify the starting file or theorem, the allowed assumptions, the output path, and the exact command that validates the artifact. Students may ask Codex to inspect, explain, implement, and test. They remain responsible for the statement being proved, the model being computed, and the final economic interpretation.

## Required verification contract

Every Part II submission contains:

1. the completed four-line bridge;
2. the initial prompt and any material follow-up prompts;
3. the final source file, with descriptive names and comments;
4. the exact validation command and its successful output;
5. one boundary case, counterexample, or deliberately failing test;
6. a short audit identifying one generated step the student checked independently; and
7. a paragraph interpreting the result without treating tool output as economic evidence.

Lean work may not contain `sorry`, `admit`, or a locally introduced axiom. A successful compile establishes only the formal statement encoded in the file. Computational work must reject inputs outside the stated economic domain and use tolerances explicitly for floating-point comparisons.

## Standard Codex prompt shape

Students should adapt the following, rather than asking for an answer in one sentence:

> Read the named Part I problem and the referenced source files. First restate the economic assumptions and propose a dependency-ordered plan. Do not change the model. Implement only the stated scale-up, add the required checks and one boundary test, run the validation command, and report any assumption or statement that must be clarified. Leave the economic interpretation for me to write.

Repository-local instructions in `problemsets/AGENTS.md` give Codex the same verification rules whenever it is launched from this directory.

## Source-of-record rule

`problems/PROBLEM_BANK.md` owns the question text and stable identifiers. `problems/CHAPTER_PATHWAYS.tsv` owns the chapter capstone, seed list, scale axis, tool, and verification contract. A released packet may add a due date, workspace, or starter artifact; it may not silently change those mathematical assumptions or introduce an unrelated scale-up.

## Instructor design test

A set is ready to release only if all five answers are yes:

- Can the Part I seed be solved cleanly on one board?
- Does Part II scale exactly one named feature?
- Can a student tell what the tool verified and what it did not?
- Is there a deterministic validation command?
- Can the instructor solution reproduce every numerical result and formal claim independently?
