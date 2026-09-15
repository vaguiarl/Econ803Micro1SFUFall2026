#!/usr/bin/env python3
"""Remove assessment-layout blocks from the book-only public edition."""

from pathlib import Path


BOOK = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"


def remove_layouts(text: str, names: set[str]) -> tuple[str, int]:
    lines = text.splitlines(keepends=True)
    out: list[str] = []
    removed = 0
    i = 0
    while i < len(lines):
        line = lines[i]
        if line.startswith("\\begin_layout ") and line.rstrip().split(maxsplit=1)[1] in names:
            removed += 1
            depth = 1
            i += 1
            while i < len(lines):
                if lines[i].startswith("\\begin_layout "):
                    depth += 1
                elif lines[i].startswith("\\end_layout"):
                    depth -= 1
                    if depth == 0:
                        i += 1
                        break
                i += 1
            continue
        out.append(line)
        i += 1
    return "".join(out), removed


def main() -> None:
    text = BOOK.read_text()
    text, removed = remove_layouts(text, {"Exercise"})
    BOOK.write_text(text)
    print(f"removed {removed} exercise blocks")


if __name__ == "__main__":
    main()
