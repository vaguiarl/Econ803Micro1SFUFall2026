# Formal checking

Run the complete reproducible check from the repository root:

```bash
bash scripts/check_book.sh
```

To reuse the separate, already-verified WGARP/Afriat library in the same run:

```bash
WGARP_LEAN_DIR=/path/to/wgarp_final_revision bash scripts/check_book.sh
```

`OrderTheory.lean` and `ChoiceTheory.lean` contain actual kernel-checked mathematical proofs. `BookNarrativeLogic.lean` checks the declared logical dependencies, distinguishes logical order from the book's reading order, and records a verification level for each block. The dependency audit does **not** prove the specialized economic theorems.

The WGARP project remains an external dependency rather than being copied into this public teaching repository. When configured, the script runs its own `lake build`; that library kernel-checks the formal revealed-preference results, while this repository cites and explains them at textbook level.

The script also exports the LyX source, compiles the PDF, rejects `sorry`, `admit`, and local `axiom` declarations in the formal modules, and flags a maintained set of high-risk prose patterns.

It regenerates `theorem_inventory.tsv`, a compact index of every axiom, definition, result, proof, exercise, and example in the LyX source. It also regenerates `BOOK_MAP.md`, which records the chapter/section sequence, formal-block counts, and exact duplicate section titles. These files make subsequent passes incremental: reviewers can work from the indexes instead of repeatedly sending the entire book through a model.
