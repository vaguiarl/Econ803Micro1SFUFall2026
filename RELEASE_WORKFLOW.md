# Weekly assessment release workflow

The private Fall 2024 repository is the archive for unreleased problem sets, solutions, and examinations. The public Fall 2026 repository contains only material deliberately released to students.

For each weekly release:

1. select a short Part I hand seed and name the single Part II scaling axis;
2. revise the questions and solutions together in the private/local archive;
3. build and inspect the question-only student PDF;
4. compile every Lean starter and independently reproduce every numerical check;
5. stage only the student LyX/PDF and permitted starter files with `scripts/release_problem_set.sh`;
6. review `git status` and confirm that no solution or answer key is present;
7. run `bash scripts/check_book.sh`, commit, and push.

The staging script refuses filenames containing `solution`, `answer`, `key`, `midterm`, or `exam`. This is a guardrail, not a substitute for checking the actual document contents.
