#!/usr/bin/env python3
"""Verify compiled PDF destinations and links for the notation glossary."""

from __future__ import annotations

import argparse
import csv
import sys
from collections import Counter
from pathlib import Path

try:
    from pypdf import PdfReader
except ImportError as exc:  # pragma: no cover - environment diagnostic
    raise SystemExit(
        "pypdf is required for compiled notation-link validation"
    ) from exc


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser()
    parser.add_argument("--pdf", required=True, type=Path)
    parser.add_argument("--ledger", required=True, type=Path)
    return parser.parse_args()


def linked_ids(path: Path) -> list[str]:
    with path.open(encoding="utf-8", newline="") as handle:
        rows = csv.DictReader(handle, delimiter="\t")
        return [row["id"] for row in rows if row["link_status"] == "linked"]


def annotation_destination(annotation: object) -> str | None:
    obj = annotation.get_object()
    if obj.get("/Subtype") != "/Link":
        return None
    destination = obj.get("/Dest")
    action = obj.get("/A")
    if action is not None and action.get("/S") == "/GoTo":
        destination = action.get("/D")
    if destination is None:
        return None
    return str(destination)


def main() -> int:
    args = parse_args()
    identifiers = linked_ids(args.ledger)
    expected = {
        f"notation-{role}-{identifier}"
        for identifier in identifiers
        for role in ("use", "def")
    }

    reader = PdfReader(args.pdf)
    destinations = set(reader.named_destinations)
    notation_destinations = {
        name for name in destinations if name.startswith("notation-")
    }
    missing_destinations = sorted(expected - notation_destinations)
    extra_destinations = sorted(notation_destinations - expected)

    link_targets: Counter[str] = Counter()
    for page in reader.pages:
        for annotation in page.get("/Annots") or []:
            destination = annotation_destination(annotation)
            if destination and destination.startswith("notation-"):
                link_targets[destination] += 1

    missing_links = sorted(expected - set(link_targets))
    extra_links = sorted(set(link_targets) - expected)
    errors: list[str] = []
    if missing_destinations:
        errors.append("missing PDF destinations: " + ", ".join(missing_destinations))
    if extra_destinations:
        errors.append("unregistered PDF destinations: " + ", ".join(extra_destinations))
    if missing_links:
        errors.append("missing PDF link annotations: " + ", ".join(missing_links))
    if extra_links:
        errors.append("unregistered PDF link targets: " + ", ".join(extra_links))

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        return 1

    print(
        "compiled notation links passed: "
        f"{len(identifiers)} IDs, {len(expected)} destinations, "
        f"{sum(link_targets.values())} link annotations"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
