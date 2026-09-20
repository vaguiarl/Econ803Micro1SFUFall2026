#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
notes_dir="$repo_dir/notes"
stem="Microeconomics_1_notes_by_Victor_Aguiar"
lyx_bin="${LYX_BIN:-/Applications/LyX.app/Contents/MacOS/lyx}"

find_poppler_tool() {
  local tool_name="$1"
  local direct_path pdfinfo_path proxy_dir candidate
  direct_path="$(command -v "$tool_name" 2>/dev/null || true)"
  if [[ -n "$direct_path" ]]; then
    printf '%s\n' "$direct_path"
    return
  fi
  if [[ -n "${POPPLER_BIN:-}" && -x "$POPPLER_BIN/$tool_name" ]]; then
    printf '%s\n' "$POPPLER_BIN/$tool_name"
    return
  fi
  pdfinfo_path="$(command -v pdfinfo 2>/dev/null || true)"
  if [[ -n "$pdfinfo_path" ]]; then
    proxy_dir="$(cd "$(dirname "$pdfinfo_path")" && pwd)"
    candidate="$proxy_dir/../../native/poppler/poppler/bin/$tool_name"
    if [[ -x "$candidate" ]]; then
      printf '%s\n' "$candidate"
      return
    fi
  fi
  printf 'Required Poppler tool not found: %s\n' "$tool_name" >&2
  return 1
}

if [[ ! -x "$lyx_bin" ]]; then
  printf 'LyX executable not found: %s\n' "$lyx_bin" >&2
  exit 1
fi

printf '1/10 Building and validating vector figures...\n'
bash "$repo_dir/figures_tikz/build_and_check.sh"

printf '2/10 Checking that generated problem sets match the public bank...\n'
python3 "$repo_dir/scripts/inject_problem_sets.py" --check \
  "$notes_dir/$stem.lyx" "$repo_dir/problems/PROBLEM_BANK.md"
python3 "$repo_dir/scripts/build_artists_case.py" --check
bash "$repo_dir/scripts/check_problem_sets.sh"

printf '3/10 Validating notation ledger and first-use/glossary links...\n'
python3 "$repo_dir/scripts/validate_notation.py" \
  --lyx "$notes_dir/$stem.lyx" \
  --ledger "$repo_dir/editorial/notation/glossary.tsv"

printf '4/10 Exporting LyX source...\n'
(cd "$notes_dir" && "$lyx_bin" --export pdflatex "$stem.lyx")

printf '5/10 Compiling the book...\n'
(cd "$notes_dir" && latexmk -pdf -interaction=nonstopmode -halt-on-error "$stem.tex" >/dev/null)

printf '6/10 Auditing final PDF fonts and vector content...\n'
pdf_path="$notes_dir/$stem.pdf"
pdfimages_bin="$(find_poppler_tool pdfimages)"
pdffonts_bin="$(find_poppler_tool pdffonts)"
raster_images="$("$pdfimages_bin" -list "$pdf_path" | awk 'NR > 2 && $1 ~ /^[0-9]+$/ {n++} END {print n+0}')"
type3_fonts="$("$pdffonts_bin" "$pdf_path" | awk 'NR > 2 && $2 == "Type" && $3 == "3" {n++} END {print n+0}')"
unembedded_fonts="$("$pdffonts_bin" "$pdf_path" | awk 'NR > 2 && $5 == "no" {n++} END {print n+0}')"
printf 'Raster images: %s; Type 3 fonts: %s; unembedded fonts: %s\n' \
  "$raster_images" "$type3_fonts" "$unembedded_fonts"
if [[ "$raster_images" != "0" || "$type3_fonts" != "0" || "$unembedded_fonts" != "0" ]]; then
  printf 'Final PDF preflight failed.\n' >&2
  exit 4
fi
python3 "$repo_dir/scripts/check_pdf_notation_links.py" \
  --pdf "$pdf_path" \
  --ledger "$repo_dir/editorial/notation/glossary.tsv"

printf '7/10 Building the pinned Lean project and auditing kernel trust...\n'
bash "$repo_dir/formal/scripts/check.sh"

printf '8/10 Checking theorem pairs and known editorial hazards...\n'
python3 "$repo_dir/scripts/validate_theorem_pairs.py" \
  --ledger "$repo_dir/formal/theorem_pairs.tsv" \
  --lyx "$notes_dir/$stem.lyx" \
  --bib "$notes_dir/references.bib" \
  --formal-dir "$repo_dir/formal"
python3 "$repo_dir/scripts/polish_front_matter.py" --check
python3 "$repo_dir/scripts/polish_consumer_release.py" --check
python3 "$repo_dir/scripts/polish_empirical_evidence.py" --check
python3 "$repo_dir/scripts/expand_workhorse_models.py" --check

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

printf '9/10 Regenerating the book map and duplication index...\n'
perl "$repo_dir/scripts/book_map.pl" "$notes_dir/$stem.lyx" > "$repo_dir/BOOK_MAP.md"

printf '10/10 Regenerating the theorem inventory...\n'
perl "$repo_dir/scripts/formal_inventory.pl" "$notes_dir/$stem.lyx" > "$repo_dir/formal/theorem_inventory.tsv"
for layout in Axiom Definition Theorem Proposition Lemma Corollary Fact Claim Proof; do
  count="$(awk -F '\t' -v kind="$layout" 'NR > 1 && $2 == kind { n++ } END { print n + 0 }' \
    "$repo_dir/formal/theorem_inventory.tsv")"
  printf '%-12s %s\n' "$layout" "$count"
done

printf '\nPASS: figures, problem bank, notation links, PDF, Lean, theorem ledger, and generated indexes passed.\n'
