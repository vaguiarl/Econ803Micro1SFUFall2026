# Weekly assessment release workflow

The private Fall 2024 repository is the archive for unreleased problem sets, solutions, and examinations. The public Fall 2026 repository contains only material deliberately released to students.

For each weekly release:

1. revise the source in the private/local archive;
2. build and inspect the student PDF;
3. stage only the student LyX/PDF files with `scripts/release_problem_set.sh`;
4. review `git status` and confirm that no solution or answer key is present;
5. run `bash scripts/check_book.sh`, commit, and push.

The staging script refuses filenames containing `solution`, `answer`, `key`, `midterm`, or `exam`. This is a guardrail, not a substitute for checking the actual document contents.

