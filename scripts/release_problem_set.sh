#!/usr/bin/env bash
set -euo pipefail

repo_dir="$(cd "$(dirname "$0")/.." && pwd)"
if (( $# < 2 )); then
  printf 'usage: %s PACKET_SLUG FILE.lyx [FILE.pdf FILE.lean README.md ...]\n' "$0" >&2
  exit 1
fi

packet_slug="$1"
shift
if [[ ! "$packet_slug" =~ ^ps[0-9][0-9]_[a-z0-9_]+$ ]]; then
  printf 'Packet slug must look like ps01_consumer_demand: %s\n' "$packet_slug" >&2
  exit 2
fi

release_dir="$repo_dir/problemsets/$packet_slug"
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
    *.lyx|*.pdf|*.lean|README.md) cp "$source_file" "$release_dir/$base" ;;
    *)
      printf 'Only LyX, PDF, Lean starter, and README files may be released: %s\n' "$base" >&2
      exit 2
      ;;
  esac
done

printf 'Staged for review in %s:\n' "$release_dir"
git -C "$repo_dir" status --short -- problemsets
printf 'Review the files, run scripts/check_book.sh, then commit and push.\n'
