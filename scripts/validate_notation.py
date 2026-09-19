#!/usr/bin/env python3
"""Validate the notation ledger and its first-use/glossary links in a LyX book."""

from __future__ import annotations

import argparse
import bisect
import re
import sys
from collections import Counter, defaultdict
from dataclasses import dataclass
from pathlib import Path


REQUIRED_COLUMNS = (
    "id",
    "symbol",
    "category",
    "scope",
    "definition",
    "first_section",
    "link_status",
)

# Conservative enough for LaTeX/PDF anchor names, while permitting the common
# namespace separators used elsewhere in the book (for example, ``not:price``).
ID_RE = re.compile(r"^[A-Za-z][A-Za-z0-9]*(?:[._:-][A-Za-z0-9]+)*$")
MACRO_RE = re.compile(r"\\notation(?P<kind>first|def)(?![A-Za-z@])")
CHAPTER_RE = re.compile(r"(?m)^\\begin_layout (?P<kind>Chapter\*?)\s*$")
BIBLIOGRAPHY_RE = re.compile(
    r"(?m)^\\begin_inset CommandInset bibtex\s*$"
)


@dataclass(frozen=True)
class LedgerRow:
    line: int
    values: dict[str, str]

    @property
    def identifier(self) -> str:
        return self.values["id"]


@dataclass(frozen=True)
class MacroCall:
    kind: str
    identifier: str
    body: str
    offset: int
    line: int
    column: int

    @property
    def anchor(self) -> str:
        role = "use" if self.kind == "first" else "def"
        return f"notation-{role}-{self.identifier}"


@dataclass(frozen=True)
class Chapter:
    title: str
    offset: int
    end_offset: int
    line: int


class LineMap:
    """Map character offsets to one-based line and column numbers."""

    def __init__(self, text: str) -> None:
        self._newlines = [index for index, char in enumerate(text) if char == "\n"]

    def location(self, offset: int) -> tuple[int, int]:
        line_index = bisect.bisect_left(self._newlines, offset)
        previous_newline = self._newlines[line_index - 1] if line_index else -1
        return line_index + 1, offset - previous_newline


class GroupParseError(ValueError):
    pass


def parse_args() -> argparse.Namespace:
    parser = argparse.ArgumentParser(
        description=(
            "Validate a notation TSV against balanced-brace notation links in "
            "a UTF-8 LyX manuscript."
        )
    )
    parser.add_argument("--lyx", required=True, type=Path, help="LyX manuscript")
    parser.add_argument(
        "--ledger",
        required=True,
        type=Path,
        help="notation TSV with the required seven-column schema",
    )
    return parser.parse_args()


def read_utf8(path: Path, label: str, errors: list[str]) -> str | None:
    try:
        return path.read_text(encoding="utf-8")
    except FileNotFoundError:
        errors.append(f"{label} does not exist: {path}")
    except IsADirectoryError:
        errors.append(f"{label} is not a file: {path}")
    except UnicodeDecodeError as exc:
        errors.append(f"{label} is not valid UTF-8: {path}: {exc}")
    except OSError as exc:
        errors.append(f"cannot read {label} {path}: {exc}")
    return None


def parse_ledger(path: Path, errors: list[str]) -> list[LedgerRow]:
    text = read_utf8(path, "ledger", errors)
    if text is None:
        return []

    lines = text.splitlines()
    if not lines:
        errors.append(f"ledger is empty: {path}")
        return []

    expected_header = "\t".join(REQUIRED_COLUMNS)
    if lines[0] != expected_header:
        errors.append(
            "ledger header must be exactly: " + expected_header.replace("\t", " | ")
        )
        return []
    if len(lines) == 1:
        errors.append("ledger must contain at least one data row")
        return []

    rows: list[LedgerRow] = []
    for line_number, raw_line in enumerate(lines[1:], start=2):
        if not raw_line:
            errors.append(f"ledger line {line_number}: blank rows are not allowed")
            continue

        tab_count = raw_line.count("\t")
        if tab_count != len(REQUIRED_COLUMNS) - 1:
            errors.append(
                f"ledger line {line_number}: expected 6 tab separators, found "
                f"{tab_count}"
            )
            continue

        fields = raw_line.split("\t")
        values = dict(zip(REQUIRED_COLUMNS, fields, strict=True))
        for column, value in values.items():
            if not value:
                errors.append(f"ledger line {line_number}: {column} must not be blank")
            elif value != value.strip():
                errors.append(
                    f"ledger line {line_number}: {column} has leading or trailing "
                    "whitespace"
                )
        rows.append(LedgerRow(line_number, values))

    identifiers = [row.identifier for row in rows if row.identifier]
    for identifier, count in sorted(Counter(identifiers).items()):
        if count > 1:
            locations = ", ".join(
                str(row.line) for row in rows if row.identifier == identifier
            )
            errors.append(
                f"duplicate ledger ID {identifier!r} on lines {locations} "
                f"({count} occurrences)"
            )

    for row in rows:
        if row.identifier and not ID_RE.fullmatch(row.identifier):
            errors.append(
                f"ledger line {row.line}: invalid notation ID {row.identifier!r}; "
                "use a letter-led slug containing only letters, digits, '.', '_', "
                "':', or '-'"
            )

    return rows


def is_escaped(text: str, offset: int) -> bool:
    backslashes = 0
    cursor = offset - 1
    while cursor >= 0 and text[cursor] == "\\":
        backslashes += 1
        cursor -= 1
    return backslashes % 2 == 1


def parse_braced_group(text: str, start: int) -> tuple[str, int]:
    """Return the contents and exclusive end of a balanced braced group."""

    if start >= len(text) or text[start] != "{":
        raise GroupParseError("expected '{'")

    depth = 1
    cursor = start + 1
    while cursor < len(text):
        char = text[cursor]
        if char == "{" and not is_escaped(text, cursor):
            depth += 1
        elif char == "}" and not is_escaped(text, cursor):
            depth -= 1
            if depth == 0:
                return text[start + 1 : cursor], cursor + 1
        cursor += 1

    raise GroupParseError("unterminated braced group")


def skip_space(text: str, offset: int) -> int:
    while offset < len(text) and text[offset].isspace():
        offset += 1
    return offset


def is_macro_declaration(text: str, macro_offset: int) -> bool:
    prefix = text[max(0, macro_offset - 64) : macro_offset]
    return bool(re.search(r"\\(?:re)?newcommand\s*\{\s*$", prefix))


def parse_notation_macros(text: str, errors: list[str]) -> list[MacroCall]:
    """Parse notation macro calls, including multiline and nested bodies."""

    calls: list[MacroCall] = []
    line_map = LineMap(text)

    for match in MACRO_RE.finditer(text):
        kind = match.group("kind")
        cursor = skip_space(text, match.end())
        line, column = line_map.location(match.start())

        # Ignore the command name inside \newcommand{\notationfirst} and
        # \newcommand{\notationdef}; it is a declaration, not a call.
        if cursor >= len(text) or text[cursor] != "{":
            if not is_macro_declaration(text, match.start()):
                errors.append(
                    f"LyX line {line}, column {column}: \\notation{kind} must "
                    "be followed by two braced arguments"
                )
            continue

        try:
            identifier, cursor = parse_braced_group(text, cursor)
            cursor = skip_space(text, cursor)
            if cursor >= len(text) or text[cursor] != "{":
                raise GroupParseError("missing second braced argument")
            body, _ = parse_braced_group(text, cursor)
        except GroupParseError as exc:
            errors.append(
                f"LyX line {line}, column {column}: malformed "
                f"\\notation{kind}: {exc}"
            )
            continue

        if not ID_RE.fullmatch(identifier):
            errors.append(
                f"LyX line {line}, column {column}: invalid notation ID "
                f"{identifier!r} in \\notation{kind}"
            )
        if not body.strip():
            errors.append(
                f"LyX line {line}, column {column}: \\notation{kind} body "
                "must not be empty"
            )

        calls.append(
            MacroCall(
                kind=kind,
                identifier=identifier,
                body=body,
                offset=match.start(),
                line=line,
                column=column,
            )
        )

    return calls


def extract_chapters(text: str) -> list[Chapter]:
    line_map = LineMap(text)
    chapters: list[Chapter] = []
    for match in CHAPTER_RE.finditer(text):
        content_start = match.end()
        end = text.find("\\end_layout", content_start)
        if end == -1:
            continue
        raw_title = text[content_start:end]
        # Chapter names in this manuscript are plain LyX layout text. Dropping
        # control lines keeps wrapped titles readable without pretending to
        # parse every possible LyX inset.
        title_parts = [
            line.strip()
            for line in raw_title.splitlines()
            if line.strip() and not line.lstrip().startswith("\\")
        ]
        title = " ".join(title_parts)
        line, _ = line_map.location(match.start())
        chapters.append(Chapter(title, match.start(), end, line))
    return chapters


def is_glossary_title(title: str) -> bool:
    return title.casefold().startswith("glossary")


def is_bibliography_title(title: str) -> bool:
    return title.casefold() in {"bibliography", "references"}


def validate_glossary_order(text: str, errors: list[str]) -> None:
    bibliography_matches = list(BIBLIOGRAPHY_RE.finditer(text))
    if not bibliography_matches:
        errors.append("LyX source has no CommandInset bibtex bibliography")
        return

    bibliography_offset = bibliography_matches[0].start()
    chapters = extract_chapters(text)
    glossary_chapters = [chapter for chapter in chapters if is_glossary_title(chapter.title)]

    if not glossary_chapters:
        errors.append("LyX source has no final Glossary chapter")
        return
    if len(glossary_chapters) > 1:
        locations = ", ".join(str(chapter.line) for chapter in glossary_chapters)
        errors.append(f"LyX source has multiple Glossary chapters on lines {locations}")

    glossary = glossary_chapters[-1]
    if glossary.offset >= bibliography_offset:
        errors.append(
            f"Glossary chapter on line {glossary.line} must occur before the "
            "bibliography"
        )

    chapters_before_bibliography = [
        chapter
        for chapter in chapters
        if chapter.offset < bibliography_offset
        and not is_bibliography_title(chapter.title)
    ]
    if not chapters_before_bibliography:
        errors.append("LyX source has no content chapter before the bibliography")
        return

    final_content_chapter = chapters_before_bibliography[-1]
    if final_content_chapter != glossary:
        errors.append(
            "Glossary must be the final content chapter before the bibliography; "
            f"the current final chapter is {final_content_chapter.title!r} on line "
            f"{final_content_chapter.line}"
        )


def validate_links(
    rows: list[LedgerRow], calls: list[MacroCall], errors: list[str]
) -> None:
    row_by_id = {row.identifier: row for row in rows if row.identifier}
    calls_by_id: dict[str, dict[str, list[MacroCall]]] = defaultdict(
        lambda: {"first": [], "def": []}
    )

    for call in calls:
        calls_by_id[call.identifier][call.kind].append(call)
        if call.identifier not in row_by_id:
            errors.append(
                f"LyX line {call.line}: \\notation{call.kind} uses unlisted ID "
                f"{call.identifier!r}"
            )

    anchors: dict[str, list[MacroCall]] = defaultdict(list)
    for call in calls:
        anchors[call.anchor].append(call)
    for anchor, anchor_calls in sorted(anchors.items()):
        if len(anchor_calls) > 1:
            locations = ", ".join(str(call.line) for call in anchor_calls)
            errors.append(
                f"duplicate anchor {anchor!r} generated on LyX lines {locations}"
            )

    for row in rows:
        identifier = row.identifier
        if not identifier:
            continue
        grouped = calls_by_id.get(identifier, {"first": [], "def": []})
        first_calls = grouped["first"]
        def_calls = grouped["def"]

        if row.values["link_status"] == "linked":
            if len(first_calls) != 1:
                errors.append(
                    f"ledger line {row.line}: linked ID {identifier!r} requires "
                    f"exactly one \\notationfirst call; found {len(first_calls)}"
                )
            if len(def_calls) != 1:
                errors.append(
                    f"ledger line {row.line}: linked ID {identifier!r} requires "
                    f"exactly one \\notationdef call; found {len(def_calls)}"
                )

        if first_calls and def_calls:
            earliest_first = min(call.offset for call in first_calls)
            earliest_def = min(call.offset for call in def_calls)
            if earliest_first >= earliest_def:
                errors.append(
                    f"notation ID {identifier!r}: first-use link must occur before "
                    "its glossary definition"
                )


def main() -> int:
    args = parse_args()
    errors: list[str] = []

    rows = parse_ledger(args.ledger, errors)
    lyx_text = read_utf8(args.lyx, "LyX source", errors)
    calls: list[MacroCall] = []
    if lyx_text is not None:
        calls = parse_notation_macros(lyx_text, errors)
        validate_glossary_order(lyx_text, errors)

    if lyx_text is not None:
        validate_links(rows, calls, errors)

    if errors:
        for error in errors:
            print(f"ERROR: {error}", file=sys.stderr)
        print(f"notation validation failed with {len(errors)} error(s)", file=sys.stderr)
        return 1

    linked_count = sum(row.values["link_status"] == "linked" for row in rows)
    print(
        "notation validation passed: "
        f"{len(rows)} ledger rows, {linked_count} linked IDs, {len(calls)} LyX calls"
    )
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
