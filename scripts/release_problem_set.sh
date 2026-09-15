#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
release_dir="$repo_dir/problemsets"

if (( $# == 0 )); then
  printf 'usage: %s FILE.lyx [FILE.pdf ...]\n' "$0" >&2
  exit 1
fi

mkdir -p "$release_dir"
for source_file in "$@"; do
  if [[ ! -f "$source_file" ]]; then
    printf 'Source file not found: %s\n' "$source_file" >&2
    exit 1
  fi
  base="$(basename "$source_file")"
  if [[ "$base" =~ [Ss]olution|[Aa]nswer|[Kk]ey|[Mm]idterm|[Ee]xam ]]; then
    printf 'Refusing to stage restricted assessment file: %s\n' "$base" >&2
    exit 2
  fi
  case "$base" in
    *.lyx|*.pdf) cp "$source_file" "$release_dir/$base" ;;
    *)
      printf 'Only LyX and PDF problem-set files may be released: %s\n' "$base" >&2
      exit 2
      ;;
  esac
done

printf 'Staged for review in %s:\n' "$release_dir"
git -C "$repo_dir" status --short -- problemsets
printf 'Review the files, run scripts/check_book.sh, then commit and push.\n'

