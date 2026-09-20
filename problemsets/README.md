# Problem sets and chapter release views

The book's end-of-chapter sections are the source of record. Every chapter ends with two deliberately different parts and one named use case; a weekly packet is a release view of that architecture, not a parallel curriculum.

1. **Part I: By hand.** Short, tractable problems intended for the board or a seminar table. Each problem isolates one economic mechanism and is solvable without code.
2. **Part II: Chapter use case and verified scale-up.** Proof and Applied problems build toward one capstone case. Students use Codex with Python, Lean, or both, but must state the scaling step, inspect the generated work, run the required checks, and interpret the result economically.

The distinction is about the intellectual job, not difficulty alone. Part I establishes the benchmark students should understand without automation. Part II changes one dimension at a time - more goods, more observations, weaker assumptions, or a formal theorem - so that computation does not obscure the economics.

The canonical prompts live in [`../problems/PROBLEM_BANK.md`](../problems/PROBLEM_BANK.md); [`../problems/CHAPTER_PATHWAYS.tsv`](../problems/CHAPTER_PATHWAYS.tsv) records the capstone case, seed, one-dimensional scale-up, and verification boundary for all sixteen chapters and the mathematical appendix. The [problem-set standard](PROBLEM_SET_STANDARD.md) defines the bridge and submission contract. Released student views appear below in teaching order.

The [chapter pathway plan](PAIRING_PLAN.md) presents the same metadata in a reader-facing table. It is a release roadmap, not a schedule of due dates.

The [Fall 2026 weekly release plan](WEEKLY_RELEASE_PLAN.md) assigns every non-case problem exactly once across the thirteen meetings. It keeps chapter case studies on their own release stream and records the same schedule in machine-readable form in `WEEKLY_RELEASE_PLAN.tsv`.

- [Problem Set 1: From Two-Good Demand to Verified General Demand](ps01_consumer_demand/README.md)

Solutions, answer keys, examinations, and unreleased sets are maintained in the private Fall 2024 repository and are intentionally absent from the public branch. A release may add a starter file or select only the benchmark work needed for one class meeting. When it releases a chapter capstone, it must retain the book's stable IDs, assumptions, case identity, scale axis, and verification boundary.
