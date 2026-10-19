#!/usr/bin/env python3
"""Reject restricted assessments except exact, explicitly released artifacts.

By default, inspect tracked paths and their working-tree contents.  --staged
instead inspects the index, including the manifest and every checked blob.
Untracked files never authorize a release.
"""

from __future__ import annotations

import argparse
import datetime as dt
import hashlib
import json
from pathlib import Path, PurePosixPath
import re
import subprocess
import sys


RELEASE_DIR = "course/released_assessments"
MANIFEST = f"{RELEASE_DIR}/PUBLIC_RELEASES.json"
SUPPORTED_SUFFIXES = {".lyx", ".pdf", ".md"}
# Preserve the previous check_book.sh policy outside explicitly released files.
RESTRICTED = re.compile(
    r"(^|/)(midterm|exam)|^problemsets/.*(solution|answer|key)", re.IGNORECASE
)


def git(repo: Path, *args: str) -> bytes:
    result = subprocess.run(
        ["git", "-C", str(repo), *args], capture_output=True, check=False
    )
    if result.returncode:
        raise ValueError("Could not read the repository index.")
    return result.stdout


def tracked_modes(repo: Path) -> dict[str, str]:
    paths: dict[str, str] = {}
    for record in git(repo, "ls-files", "--stage", "-z").split(b"\0"):
        if not record:
            continue
        metadata, raw_path = record.split(b"\t", 1)
        mode, _oid, stage = metadata.decode("ascii").split()
        path = raw_path.decode("utf-8", errors="surrogateescape")
        if stage != "0":
            raise ValueError("Resolve unmerged index entries before checking releases.")
        paths[path] = mode
    return paths


def read_tracked(repo: Path, path: str, modes: dict[str, str], staged: bool) -> bytes:
    if modes.get(path) not in {"100644", "100755"}:
        raise ValueError(f"Release artifact must be a tracked regular file: {path!r}")
    if staged:
        return git(repo, "show", f":{path}")
    candidate = repo / path
    # Never follow an artifact or directory symlink to read another location.
    if any(part.is_symlink() for part in (candidate, *candidate.parents) if part != repo):
        raise ValueError(f"Release artifact must not use a symlink: {path!r}")
    try:
        return candidate.read_bytes()
    except OSError:
        raise ValueError(f"Could not read tracked release artifact: {path!r}") from None


def parse_manifest(data: bytes) -> dict[str, str]:
    try:
        manifest = json.loads(data)
    except (UnicodeDecodeError, json.JSONDecodeError):
        raise ValueError("PUBLIC_RELEASES.json is not valid JSON.") from None
    if not isinstance(manifest, dict) or set(manifest) != {"releases"}:
        raise ValueError("PUBLIC_RELEASES.json must contain only a 'releases' array.")
    if not isinstance(manifest["releases"], list):
        raise ValueError("The manifest 'releases' value must be an array.")
    allowed: dict[str, str] = {}
    for release in manifest["releases"]:
        if not isinstance(release, dict) or set(release) != {"assessment", "released_on", "files"}:
            raise ValueError("Each release needs assessment, released_on and files fields.")
        if not isinstance(release["assessment"], str) or not release["assessment"].strip():
            raise ValueError("Every release needs a nonempty assessment label.")
        date = release["released_on"]
        try:
            if not isinstance(date, str) or not re.fullmatch(r"\d{4}-\d{2}-\d{2}", date):
                raise ValueError
            dt.date.fromisoformat(date)
        except ValueError:
            raise ValueError("Every release needs a valid ISO released_on date.") from None
        if not isinstance(release["files"], list) or not release["files"]:
            raise ValueError("Every release needs a nonempty files array.")
        for entry in release["files"]:
            if not isinstance(entry, dict) or set(entry) != {"path", "sha256"}:
                raise ValueError("Each released file needs path and sha256 fields.")
            path, digest = entry["path"], entry["sha256"]
            if not isinstance(path, str):
                raise ValueError("Release paths must be repository-relative strings.")
            parsed = PurePosixPath(path)
            if (
                parsed.is_absolute()
                or ".." in parsed.parts
                or "\\" in path
                or path != parsed.as_posix()
                or not path.startswith(f"{RELEASE_DIR}/")
                or path == MANIFEST
                or parsed.suffix not in SUPPORTED_SUFFIXES
            ):
                raise ValueError(f"Invalid public release artifact path: {path!r}")
            if not isinstance(digest, str) or not re.fullmatch(r"[0-9a-fA-F]{64}", digest):
                raise ValueError(f"Invalid SHA-256 for release artifact: {path!r}")
            if path in allowed:
                raise ValueError(f"Duplicate release artifact path: {path!r}")
            allowed[path] = digest.lower()
    return allowed


def check(repo: Path, staged: bool) -> list[str]:
    modes = tracked_modes(repo)
    release_paths = {
        path for path in modes if path.startswith(f"{RELEASE_DIR}/") and path != MANIFEST
    }
    errors = []
    allowed: dict[str, str] = {}
    if MANIFEST in modes:
        allowed = parse_manifest(read_tracked(repo, MANIFEST, modes, staged))
    elif release_paths:
        errors.append("Tracked release artifacts require a tracked PUBLIC_RELEASES.json.")

    for path in sorted(release_paths - allowed.keys()):
        errors.append(f"Unlisted tracked release artifact: {path!r}")
    for path in sorted(allowed.keys() - release_paths):
        errors.append(f"Manifest artifact is not tracked in the release subtree: {path!r}")
    valid = set()
    for path in sorted(release_paths & allowed.keys()):
        try:
            digest = hashlib.sha256(read_tracked(repo, path, modes, staged)).hexdigest()
        except ValueError as exc:
            errors.append(str(exc))
            continue
        if digest != allowed[path]:
            errors.append(f"Release artifact SHA-256 mismatch: {path!r}")
        else:
            valid.add(path)

    for path in sorted(modes):
        if RESTRICTED.search(path) and path not in valid:
            errors.append(f"Restricted assessment path is not explicitly released: {path!r}")
    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--staged", action="store_true", help="Read index blobs, not working files.")
    parser.add_argument(
        "--repo", type=Path, default=Path(__file__).resolve().parents[1],
        help="Repository to check (defaults to this script's repository).",
    )
    args = parser.parse_args()
    try:
        repo = Path(git(args.repo, "rev-parse", "--show-toplevel").decode().strip()).resolve()
        errors = check(repo, args.staged)
    except ValueError as exc:
        errors = [str(exc)]
    if errors:
        print("Public assessment release check failed:", file=sys.stderr)
        for error in errors:
            print(f"- {error}", file=sys.stderr)
        return 3
    print(f"PASS: public assessment release guard ({'index' if args.staged else 'tracked working files'}).")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
