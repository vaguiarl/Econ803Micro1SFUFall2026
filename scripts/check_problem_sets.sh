#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
lyx_bin="${LYX_BIN:-/Applications/LyX.app/Contents/MacOS/lyx}"
poppler_dir="/Users/victoraguiar/.cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/poppler/bin"

if [[ ! -x "$lyx_bin" ]]; then
  printf 'LyX executable not found: %s\n' "$lyx_bin" >&2
  exit 1
fi

mapfile_cmd=(find "$repo_dir/problemsets" -mindepth 2 -maxdepth 2 -name 'PS*.lyx' -print)
while IFS= read -r source; do
  [[ -n "$source" ]] || continue
  packet_dir="$(dirname "$source")"
  stem="$(basename "$source" .lyx)"
  if ! rg -q 'Part I\. By hand' "$source" || ! rg -q 'Part II\. Verified scale-up' "$source"; then
    printf 'Two-part structure missing from %s\n' "$source" >&2
    exit 2
  fi
  if ! rg -q 'questions only' "$source"; then
    printf 'Student-edition marker missing from %s\n' "$source" >&2
    exit 2
  fi
  (cd "$packet_dir" && "$lyx_bin" --export pdflatex "$stem.lyx" >/dev/null)
  (cd "$packet_dir" && latexmk -pdf -interaction=nonstopmode -halt-on-error "$stem.tex" >/dev/null)
  if "$poppler_dir/pdfimages" -list "$packet_dir/$stem.pdf" | awk 'NR > 2 && $1 ~ /^[0-9]+$/ { bad=1 } END { exit bad }'; then
    :
  else
    printf 'Raster image found in %s.pdf\n' "$stem" >&2
    exit 3
  fi
  if "$poppler_dir/pdffonts" "$packet_dir/$stem.pdf" | awk 'NR > 2 && ($2 == "Type" && $3 == "3" || $5 == "no") { bad=1 } END { exit bad }'; then
    :
  else
    printf 'Font preflight failed for %s.pdf\n' "$stem" >&2
    exit 3
  fi
  printf 'PASS: %s\n' "$stem"
done < <("${mapfile_cmd[@]}")

(cd "$repo_dir/formal" && lake env lean ../problemsets/ps01_consumer_demand/Starter.lean >/dev/null)

if rg -n -i '\b(solutions|answer key|instructor solution)\b' "$repo_dir/problemsets" --glob '*.lyx'; then
  printf 'Restricted solution language found in a released packet.\n' >&2
  exit 4
fi

printf 'PASS: released problem sets are two-part, buildable, and question-only.\n'
