#!/usr/bin/env python3
"""Validate the reader/full-theorem migration ledger.

The ledger is deliberately conservative: a row may record a planned theorem
and a compiled Lean core without claiming that either the Appendix-B theorem
or its complete formalization already exists.
"""

from __future__ import annotations

import argparse
import csv
import re
import sys
from collections import Counter
from pathlib import Path


EXPECTED_PAIR_IDS = (
    "TS-C01-WARP-CLD",
    "TS-C02-RATIONAL-WARP",
    "TS-C03-CONTINUOUS-UTILITY",
    "TS-C03-DEMAND-CONTINUITY",
    "TS-C03-CONSUMER-DUALITY",
    "TS-C03-AFRIAT",
    "TS-C03-WGARP-CMU",
    "TS-C03-WARP-CMU",
    "TS-C05-EU-FINITE",
    "TS-C05-FOSD",
    "TS-C05-RISK-DATA",
    "TS-C06-GORMAN",
    "TS-C07-SURPLUS-ENVELOPE",
    "TS-C08-FIRM-DUALITY",
    "TS-C09-PARTIAL-EQUILIBRIUM",
    "TS-C10-FIRST-WELFARE",
    "TS-C10-SECOND-WELFARE",
    "TS-C11-EXISTENCE",
    "TS-C11-GROSS-SUBSTITUTES",
    "TS-C11-SMD",
    "TS-C12-BROWN-MATZKIN",
    "TS-C13-ARROW-RADNER",
    "TS-C14-GALE-SHAPLEY",
    "TS-C14-TTC",
)

# Pair IDs are stable public identifiers.  Their embedded Cxx segments record
# the chapter in which the pair was first registered and are not renumbered
# when the book architecture changes.  This separate map is the authoritative
# current placement and prevents a move from silently changing an identifier.
CURRENT_CHAPTER_BY_PAIR = {
    "TS-C01-WARP-CLD": "3",
    "TS-C02-RATIONAL-WARP": "4",
    "TS-C03-CONTINUOUS-UTILITY": "4",
    "TS-C03-DEMAND-CONTINUITY": "1",
    "TS-C03-CONSUMER-DUALITY": "2",
    "TS-C03-AFRIAT": "3",
    "TS-C03-WGARP-CMU": "3",
    "TS-C03-WARP-CMU": "3",
    "TS-C05-EU-FINITE": "5",
    "TS-C05-FOSD": "5",
    "TS-C05-RISK-DATA": "5",
    "TS-C06-GORMAN": "8",
    "TS-C07-SURPLUS-ENVELOPE": "6",
    "TS-C08-FIRM-DUALITY": "9",
    "TS-C09-PARTIAL-EQUILIBRIUM": "10",
    "TS-C10-FIRST-WELFARE": "11",
    "TS-C10-SECOND-WELFARE": "11",
    "TS-C11-EXISTENCE": "12",
    "TS-C11-GROSS-SUBSTITUTES": "12",
    "TS-C11-SMD": "12",
    "TS-C12-BROWN-MATZKIN": "13",
    "TS-C13-ARROW-RADNER": "14",
    "TS-C14-GALE-SHAPLEY": "15",
    "TS-C14-TTC": "15",
}

REQUIRED_COLUMNS = (
    "pair_id",
    "chapter",
    "reader_label",
    "full_label",
    "reader_title",
    "full_title",
    "migration_status",
    "proof_status",
    "lean_status",
    "lean_module",
    "lean_decl",
    "source_key",
    "assumption_bundle",
    "dependencies",
)

MIGRATION_STATUSES = {"planned", "source_gated", "migrated"}
PROOF_STATUSES = {
    "not_started",
    "partial",
    "draft_complete",
    "delegated",
    "source_gated",
    "complete",
}
LEAN_STATUSES = {"none", "planned", "core_only", "external_core", "complete"}
LOCAL_LEAN_STATUSES = {"core_only", "external_core", "complete"}
BANNED_VAGUE_PHRASES = (
    "usual assumptions",
    "usual regularity",
    "under regularity",
    "preceding assumptions",
    "preceding conditions",
    "and so on",
)
DECLARATION_RE_TEMPLATE = r"^\s*(?:theorem|lemma|def|abbrev)\s+{name}\b"


def split_list(value: str) -> list[str]:
    return [item.strip() for item in value.split(";") if item.strip()]


def split_dependencies(value: str) -> list[str]:
    return [] if value == "none" else split_list(value)


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--ledger",
        type=Path,
        default=Path("formal/theorem_pairs.tsv"),
        help="path to theorem_pairs.tsv",
    )
    parser.add_argument(
        "--lyx",
        type=Path,
        help="LyX source used to substantiate rows marked migrated",
    )
    parser.add_argument(
        "--bib",
        type=Path,
        help="BibTeX database used to validate source_key entries",
    )
    parser.add_argument(
        "--formal-dir",
        type=Path,
        help="directory containing the local Lean module tree",
    )
    return parser.parse_args()


def read_ledger(path: Path, errors: list[str]) -> list[dict[str, str]]:
    if not path.is_file():
        errors.append(f"ledger does not exist: {path}")
        return []

    with path.open(newline="", encoding="utf-8") as handle:
        reader = csv.DictReader(handle, delimiter="\t")
        if tuple(reader.fieldnames or ()) != REQUIRED_COLUMNS:
            errors.append(
                "ledger header must be exactly: " + "\t".join(REQUIRED_COLUMNS)
            )
            return []
        rows = list(reader)

    for line_number, row in enumerate(rows, start=2):
        if None in row:
            errors.append(f"line {line_number}: too many tab-separated fields")
            continue
        for column, value in row.items():
            if value is None:
                errors.append(f"line {line_number}: missing field {column}")
            elif value != value.strip():
                errors.append(
                    f"line {line_number}: {column} has leading or trailing whitespace"
                )
    return rows


def validate_identity(rows: list[dict[str, str]], errors: list[str]) -> None:
    if set(CURRENT_CHAPTER_BY_PAIR) != set(EXPECTED_PAIR_IDS):
        errors.append("current-chapter map must cover exactly the expected pair IDs")

    ids = [row["pair_id"] for row in rows]
    duplicates = sorted(key for key, count in Counter(ids).items() if count > 1)
    if duplicates:
        errors.append("duplicate pair IDs: " + ", ".join(duplicates))

    missing = sorted(set(EXPECTED_PAIR_IDS) - set(ids))
    unexpected = sorted(set(ids) - set(EXPECTED_PAIR_IDS))
    if missing:
        errors.append("missing pair IDs: " + ", ".join(missing))
    if unexpected:
        errors.append("unexpected pair IDs: " + ", ".join(unexpected))
    if not missing and not unexpected and ids != list(EXPECTED_PAIR_IDS):
        errors.append("pair IDs are complete but not in the canonical order")

    for field in ("reader_label", "full_label"):
        labels = [row[field] for row in rows]
        repeated = sorted(key for key, count in Counter(labels).items() if count > 1)
        if repeated:
            errors.append(f"duplicate {field} values: " + ", ".join(repeated))

    reader_labels = {row["reader_label"] for row in rows}
    full_labels = {row["full_label"] for row in rows}
    overlap = sorted(reader_labels & full_labels)
    if overlap:
        errors.append("labels used as both reader and full targets: " + ", ".join(overlap))


def validate_rows(rows: list[dict[str, str]], errors: list[str]) -> None:
    pair_ids = {row["pair_id"] for row in rows}
    graph: dict[str, list[str]] = {}

    for line_number, row in enumerate(rows, start=2):
        pair_id = row["pair_id"] or f"line {line_number}"
        required_values = (
            "pair_id",
            "chapter",
            "reader_label",
            "full_label",
            "reader_title",
            "full_title",
            "migration_status",
            "proof_status",
            "lean_status",
            "assumption_bundle",
            "dependencies",
        )
        for field in required_values:
            if not row[field]:
                errors.append(f"{pair_id}: {field} must not be blank")

        expected_chapter = CURRENT_CHAPTER_BY_PAIR.get(row["pair_id"])
        if expected_chapter is not None and row["chapter"] != expected_chapter:
            errors.append(
                f"{pair_id}: chapter {row['chapter']!r} disagrees with the "
                f"current architecture ({expected_chapter})"
            )
        if row["reader_label"] and not row["reader_label"].startswith("thmstar:"):
            errors.append(f"{pair_id}: reader_label must begin with 'thmstar:'")
        if row["full_label"] and not row["full_label"].startswith("thmfull:"):
            errors.append(f"{pair_id}: full_label must begin with 'thmfull:'")

        migration = row["migration_status"]
        proof = row["proof_status"]
        lean = row["lean_status"]
        if migration not in MIGRATION_STATUSES:
            errors.append(f"{pair_id}: unknown migration_status {migration!r}")
        if proof not in PROOF_STATUSES:
            errors.append(f"{pair_id}: unknown proof_status {proof!r}")
        if lean not in LEAN_STATUSES:
            errors.append(f"{pair_id}: unknown lean_status {lean!r}")

        if (migration == "source_gated") != (proof == "source_gated"):
            errors.append(
                f"{pair_id}: source-gated migration and proof statuses must agree"
            )
        if migration == "source_gated" and not row["source_key"]:
            errors.append(f"{pair_id}: source_gated requires at least one source_key")
        if proof == "delegated" and not row["source_key"]:
            errors.append(f"{pair_id}: delegated proof requires at least one source_key")
        if proof == "complete" and migration != "migrated":
            errors.append(
                f"{pair_id}: proof complete overclaims a theorem not marked migrated"
            )
        if migration == "migrated" and proof in {"not_started", "source_gated"}:
            errors.append(
                f"{pair_id}: migrated is incompatible with proof_status {proof}"
            )
        if lean == "complete" and (migration != "migrated" or proof != "complete"):
            errors.append(
                f"{pair_id}: Lean complete requires migrated text and a complete proof"
            )

        has_module = bool(row["lean_module"])
        has_decl = bool(row["lean_decl"])
        if lean in LOCAL_LEAN_STATUSES and not (has_module and has_decl):
            errors.append(f"{pair_id}: {lean} requires lean_module and lean_decl")
        if lean not in LOCAL_LEAN_STATUSES and (has_module or has_decl):
            errors.append(
                f"{pair_id}: {lean} must not name an unverified module or declaration"
            )
        if lean == "external_core" and not row["source_key"]:
            errors.append(f"{pair_id}: external_core requires a source_key")

        searchable = " ".join(
            (row["reader_title"], row["full_title"], row["assumption_bundle"])
        ).lower()
        for phrase in BANNED_VAGUE_PHRASES:
            if phrase in searchable:
                errors.append(f"{pair_id}: vague phrase is forbidden: {phrase!r}")

        dependencies = split_dependencies(row["dependencies"])
        graph[row["pair_id"]] = dependencies
        if len(dependencies) != len(set(dependencies)):
            errors.append(f"{pair_id}: duplicate dependency")
        for dependency in dependencies:
            if dependency == row["pair_id"]:
                errors.append(f"{pair_id}: theorem cannot depend on itself")
            elif dependency not in pair_ids:
                errors.append(f"{pair_id}: unknown dependency {dependency}")

    visiting: set[str] = set()
    visited: set[str] = set()

    def visit(pair_id: str, trail: list[str]) -> None:
        if pair_id in visiting:
            cycle_start = trail.index(pair_id)
            errors.append("dependency cycle: " + " -> ".join(trail[cycle_start:]))
            return
        if pair_id in visited:
            return
        visiting.add(pair_id)
        for dependency in graph.get(pair_id, []):
            if dependency in graph:
                visit(dependency, trail + [dependency])
        visiting.remove(pair_id)
        visited.add(pair_id)

    for pair_id in graph:
        visit(pair_id, [pair_id])


def bib_keys(path: Path, errors: list[str]) -> set[str]:
    if not path.is_file():
        errors.append(f"BibTeX database does not exist: {path}")
        return set()
    text = path.read_text(encoding="utf-8")
    return set(re.findall(r"^\s*@\w+\s*\{\s*([^,\s]+)", text, re.MULTILINE))


def validate_sources(
    rows: list[dict[str, str]], path: Path | None, errors: list[str]
) -> None:
    if path is None:
        return
    known = bib_keys(path, errors)
    for row in rows:
        for key in split_list(row["source_key"]):
            if key not in known:
                errors.append(f"{row['pair_id']}: unknown BibTeX key {key}")


def module_path(formal_dir: Path, module: str) -> Path:
    return formal_dir.joinpath(*module.split(".")).with_suffix(".lean")


def validate_lean(
    rows: list[dict[str, str]], formal_dir: Path | None, errors: list[str]
) -> None:
    local_rows = [row for row in rows if row["lean_status"] in LOCAL_LEAN_STATUSES]
    if not local_rows:
        return
    if formal_dir is None:
        errors.append("--formal-dir is required when the ledger claims a local Lean core")
        return
    for row in local_rows:
        path = module_path(formal_dir, row["lean_module"])
        if not path.is_file():
            errors.append(f"{row['pair_id']}: Lean module does not exist: {path}")
            continue
        text = path.read_text(encoding="utf-8")
        for declaration in split_list(row["lean_decl"]):
            pattern = re.compile(
                DECLARATION_RE_TEMPLATE.format(name=re.escape(declaration)),
                re.MULTILINE,
            )
            if not pattern.search(text):
                errors.append(
                    f"{row['pair_id']}: declaration {declaration} not found in {path}"
                )


def top_level_layout_for_offset(text: str, offset: int) -> str | None:
    stack: list[str] = []
    layout_at_offset: str | None = None
    cursor = 0
    for line in text.splitlines(keepends=True):
        if line.startswith("\\begin_layout "):
            stack.append(line[len("\\begin_layout ") :].strip())
        if cursor <= offset < cursor + len(line):
            layout_at_offset = stack[0] if stack else None
            break
        if line.startswith("\\end_layout") and stack:
            stack.pop()
        cursor += len(line)
    return layout_at_offset


def validate_migration(
    rows: list[dict[str, str]], lyx_path: Path | None, errors: list[str]
) -> None:
    migrated = [row for row in rows if row["migration_status"] == "migrated"]
    if not migrated:
        return
    if lyx_path is None:
        errors.append("--lyx is required when any theorem pair is marked migrated")
        return
    if not lyx_path.is_file():
        errors.append(f"LyX source does not exist: {lyx_path}")
        return
    text = lyx_path.read_text(encoding="utf-8")
    for row in migrated:
        for role, field, permitted in (
            ("reader", "reader_label", {"ReaderTheorem", "Theorem*", "Theorem"}),
            ("full", "full_label", {"FullTheorem", "Theorem"}),
        ):
            label = row[field]
            matches = list(re.finditer(rf'(?<![\w:-]){re.escape(label)}(?![\w:-])', text))
            if len(matches) != 1:
                errors.append(
                    f"{row['pair_id']}: migrated {role} label {label!r} occurs "
                    f"{len(matches)} times in the LyX source"
                )
                continue
            layout = top_level_layout_for_offset(text, matches[0].start())
            if layout not in permitted:
                expected = " or ".join(sorted(permitted))
                errors.append(
                    f"{row['pair_id']}: {role} label is in {layout!r}, expected {expected}"
                )
            elif role == "reader" and layout == "Theorem":
                layout_start = text.rfind("\\begin_layout Theorem", 0, matches[0].start())
                layout_end = text.find("\\end_layout", matches[0].end())
                layout_text = text[layout_start:layout_end]
                if "Reader theorem" not in layout_text or "\\star" not in layout_text:
                    errors.append(
                        f"{row['pair_id']}: reader label in a numbered Theorem layout "
                        "must explicitly identify itself as a reader theorem with a star"
                    )


def main() -> int:
    args = parse_args()
    errors: list[str] = []
    rows = read_ledger(args.ledger, errors)
    if rows:
        validate_identity(rows, errors)
        validate_rows(rows, errors)
        validate_sources(rows, args.bib, errors)
        validate_lean(rows, args.formal_dir, errors)
        validate_migration(rows, args.lyx, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1
    print(f"PASS: {len(rows)} theorem pairs validated in {args.ledger}")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
