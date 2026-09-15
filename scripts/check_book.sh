#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
notes_dir="$repo_dir/notes"
stem="Microeconomics_1_notes_by_Victor_Aguiar"
lyx_bin="${LYX_BIN:-/Applications/LyX.app/Contents/MacOS/lyx}"

if [[ ! -x "$lyx_bin" ]]; then
  printf 'LyX executable not found: %s\n' "$lyx_bin" >&2
  exit 1
fi

printf '1/7 Exporting LyX source...\n'
(cd "$notes_dir" && "$lyx_bin" --export pdflatex "$stem.lyx")

printf '2/7 Compiling the book...\n'
(cd "$notes_dir" && latexmk -pdf -interaction=nonstopmode -halt-on-error "$stem.tex" >/dev/null)

printf '3/7 Compiling Lean checks...\n'
for lean_file in "$repo_dir"/formal/*.lean; do
  lean "$lean_file"
done

printf '4/7 Checking the external WGARP proof library when configured...\n'
if [[ -n "${WGARP_LEAN_DIR:-}" ]]; then
  if [[ ! -f "$WGARP_LEAN_DIR/lakefile.toml" && ! -f "$WGARP_LEAN_DIR/lakefile.lean" ]]; then
    printf 'WGARP_LEAN_DIR is not a Lean project: %s\n' "$WGARP_LEAN_DIR" >&2
    exit 1
  fi
  (cd "$WGARP_LEAN_DIR" && lake build)
else
  printf 'Skipped (set WGARP_LEAN_DIR to the existing WGARP Lean project).\n'
fi

printf '5/7 Checking proof trust and known editorial hazards...\n'
if rg -n '\b(sorry|admit)\b|^\s*axiom\b' "$repo_dir/formal" --glob '*.lean'; then
  printf 'Lean trust check failed.\n' >&2
  exit 1
fi

hazards='Homegeneity|equilibrum|substition|Missperception|continously|There exist a representative|if and only for|not defined here|I want to show|We are going to establish|proof is trivial|Necessity is trivial'
if rg -n -i "$hazards" "$notes_dir/$stem.lyx"; then
  printf '\nEditorial hazards remain; review the lines above.\n' >&2
  exit 2
fi

restricted_assessments="$(git -C "$repo_dir" ls-files | rg -i '(^|/)(midterm|exam)|^problemsets/.*(solution|answer|key)' || true)"
if [[ -n "$restricted_assessments" ]]; then
  printf '%s\n' "$restricted_assessments" >&2
  printf '\nRestricted assessment files are tracked in the public repository.\n' >&2
  exit 3
fi

printf '6/7 Regenerating the book map and duplication index...\n'
perl "$repo_dir/scripts/book_map.pl" "$notes_dir/$stem.lyx" > "$repo_dir/BOOK_MAP.md"

printf '7/7 Summarizing formal coverage...\n'
perl "$repo_dir/scripts/formal_inventory.pl" "$notes_dir/$stem.lyx" > "$repo_dir/formal/theorem_inventory.tsv"
for layout in Definition Theorem Proposition Lemma Corollary Fact Claim Proof; do
  count="$(rg -c "^\\\\begin_layout ${layout}$" "$notes_dir/$stem.lyx" || true)"
  printf '%-12s %s\n' "$layout" "${count:-0}"
done

printf '\nPASS: PDF builds and the Lean modules compile without placeholders.\n'
