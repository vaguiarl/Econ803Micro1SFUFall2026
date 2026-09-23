#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
practice_dir="$repo_dir/problemsets/practice_book"
stem="ECON803_Practice_Book_Fall2026"
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

python3 "$repo_dir/scripts/build_practice_book.py" --check
(cd "$practice_dir" && "$lyx_bin" --export pdflatex "$stem.lyx")
(cd "$practice_dir" && latexmk -pdf -interaction=nonstopmode -halt-on-error "$stem.tex" >/dev/null)
python3 "$repo_dir/scripts/build_practice_book.py" --check-pdf

pdf_path="$practice_dir/$stem.pdf"
pdfimages_bin="$(find_poppler_tool pdfimages)"
pdffonts_bin="$(find_poppler_tool pdffonts)"
raster_images="$("$pdfimages_bin" -list "$pdf_path" | awk 'NR > 2 && $1 ~ /^[0-9]+$/ {n++} END {print n+0}')"
type3_fonts="$("$pdffonts_bin" "$pdf_path" | awk 'NR > 2 && $2 == "Type" && $3 == "3" {n++} END {print n+0}')"
unembedded_fonts="$("$pdffonts_bin" "$pdf_path" | awk 'NR > 2 && $5 == "no" {n++} END {print n+0}')"

printf 'Practice-book preflight: %s raster images; %s Type 3 fonts; %s unembedded fonts.\n' \
  "$raster_images" "$type3_fonts" "$unembedded_fonts"
if [[ "$raster_images" != "0" || "$type3_fonts" != "0" || "$unembedded_fonts" != "0" ]]; then
  printf 'Practice-book PDF preflight failed.\n' >&2
  exit 2
fi
