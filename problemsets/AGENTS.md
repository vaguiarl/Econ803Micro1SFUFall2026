# ECON 803 student-lab instructions

These rules apply to Codex work inside `problemsets/`.

## Learning contract

- Read the assigned Part I problem before editing or generating files.
- Begin by listing the economic assumptions, the hand-solved seed, the single scaling step, and the proposed verification command.
- Do not replace the assigned model, notation, data, or theorem statement unless the student explicitly asks for a correction and records it.
- Help with implementation and verification, but leave the final economic interpretation to the student.

## Lean work

- Reuse the pinned project in `formal/` and its existing namespaces.
- Do not use `sorry`, `admit`, `axiom`, or an unchecked placeholder.
- Compile the focused file with `lake env lean PATH`, then report the exact command and result.
- Distinguish a theorem proved locally, a theorem consumed from the pinned WGARP dependency, and an informal claim not encoded in Lean.
- When requested, run `#print axioms` on the completed student theorem and explain the trust boundary.

## Computational work

- Derive the formula symbolically before coding it.
- Validate dimensions and economic domains, including strict positivity where required.
- Add tests for accounting or adding-up identities, homogeneity, and at least one boundary or rejected input.
- Keep full-precision calculations in code and round only displayed output.
- Never infer an economic theorem from a finite numerical grid.

## Submission hygiene

- Keep question packets free of solutions.
- Put student-created artifacts in the assignment's `work/` directory or in a personal fork.
- Do not modify the textbook, canonical problem bank, private solutions, or pinned dependency revisions for an assignment.
- Before finishing, summarize every changed file and every check run.
