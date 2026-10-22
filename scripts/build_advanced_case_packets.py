#!/usr/bin/env python3
"""Generate question only gravity and Galor packets from stable chapter IDs.

The canonical bank, not these generated handouts, controls every question.
No private keys or numerical reference answers are read by this generator.
"""

from __future__ import annotations

import argparse
from dataclasses import dataclass
import os
from pathlib import Path
import re
import shutil
import subprocess

from inject_problem_sets import Problem, lyx_inline, parse_problem_bank


ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "problems/PROBLEM_BANK.md"
BOOK = ROOT / "notes/Microeconomics_1_notes_by_Victor_Aguiar.lyx"


@dataclass(frozen=True)
class Packet:
    name: str
    title: str
    identifiers: tuple[str, ...]
    relative_path: str
    introduction: str
    reading: str
    reading_url: str


PACKETS = (
    Packet(
        "gravity",
        "Gravity, Trade and Transport",
        ("16.A1", "16.A2"),
        "problemsets/gravity_trade/Gravity_Trade_Practice.lyx",
        "Questions only. Restored from both parts of the SFU December 2024 final: "
        "the structural gravity argument and the Arabasta and Baltigo modeling case. "
        "Each question separates hand work from Codex and verification. "
        "Timing refers to the hand work. The original contraction request and "
        "the counterfactual income closure are corrected explicitly.",
        "Anderson and van Wincoop (2003), Gravity with Gravitas",
        "https://doi.org/10.1257/000282803321455214",
    ),
    Packet(
        "galor",
        "From Household KKT to Growth",
        ("16.A3",),
        "problemsets/galor_general_equilibrium/Galor_KKT_General_Equilibrium.lyx",
        "Questions only. This original teaching extension of Problem 1.6 closes "
        "household quantity and quality choice with competitive firms, land ownership "
        "and resource clearing, then adds population and human capital dynamics. "
        "It is a tractable classroom model inspired by Unified Growth Theory, "
        "not a reproduction of the complete Galor model.",
        "Galor (2005), From Stagnation to Growth: Unified Growth Theory",
        "https://doi.org/10.1016/S1574-0684(05)01004-X",
    ),
)


def select_problems(chapters, identifiers: tuple[str, ...]) -> tuple[Problem, ...]:
    selected = []
    for identifier in identifiers:
        matches = [p for chapter in chapters for p in chapter.problems if p.identifier == identifier]
        if len(matches) != 1 or matches[0].level != "Advanced":
            raise ValueError(f"missing, ambiguous or nonadvanced packet problem: {identifier}")
        selected.append(matches[0])
    return tuple(selected)


def layout(kind: str, value: str) -> str:
    return f"\\begin_layout {kind}\n{value}\n\\end_layout\n\n"


def article_header(book: str) -> str:
    header = book[:book.index("\\begin_body")]
    header = header.replace("\\textclass book", "\\textclass article")
    header = header.replace("theorems-chap\n", "")
    header = re.sub(
        r"\\begin_preamble.*?\\end_preamble",
        lambda _: "\\begin_preamble\n\\pagestyle{plain}\n\\end_preamble",
        header,
        flags=re.S,
    )
    return header.replace("\\spacing double", "\\spacing onehalf").replace("\\secnumdepth 3", "\\secnumdepth 0")


def build_packet(packet: Packet, chapters, book: str) -> str:
    problems = select_problems(chapters, packet.identifiers)
    chunks = [article_header(book), "\n\\begin_body\n"]
    chunks.extend(layout(kind, value) for kind, value in (
        ("Title", packet.title),
        ("Author", "Victor H. Aguiar"),
        ("Date", "ECON 803, Fall 2026"),
        ("Standard", packet.introduction),
        ("Standard", "These are the same questions as the textbook. Begin with "
         "the hand calculations and state a solution plan before using tools. "
         "Report the economic assumptions, the hand seed, one scaling step and "
         "an exact verification command. Numerical output alone is not a proof."),
    ))
    chunks.append(
        "\\begin_layout Standard\nOptional background: "
        "\\begin_inset ERT\nstatus collapsed\n\n\\begin_layout Plain Layout\n\n"
        "\\backslash\nhref{" + packet.reading_url + "}{" + packet.reading + "}"
        "\n\\end_layout\n\n\\end_inset\n\n\\end_layout\n\n"
    )
    for position, problem in enumerate(problems):
        if position:
            chunks.append(layout(
                "Standard",
                "\\begin_inset ERT\nstatus collapsed\n\n"
                "\\begin_layout Plain Layout\n\n\\backslash\nclearpage\n"
                "\\end_layout\n\n\\end_inset",
            ))
        chunks.append(layout("Section*", f"Problem {problem.identifier}. {problem.title}"))
        for paragraph in problem.paragraphs:
            if paragraph in {"Part I. By hand.", "Part II. Codex and verification."}:
                chunks.append(layout("Subsection*", paragraph.rstrip(".")))
            else:
                chunks.append(layout("Standard", lyx_inline(paragraph)))
    chunks.append("\\end_body\n\\end_document\n")
    return "".join(chunks)


def check_pdf(packet: Packet) -> None:
    from pypdf import PdfReader

    path = (ROOT / packet.relative_path).with_suffix(".pdf")
    reader = PdfReader(path)
    content = " ".join(" ".join((page.extract_text() or "").split()) for page in reader.pages)
    for identifier in packet.identifiers:
        count = len(re.findall(r"\bProblem\s+" + re.escape(identifier) + r"\.", content))
        if count != 1:
            raise ValueError(f"expected one PDF heading for {identifier}, found {count}")
    if "Questions only" not in content:
        raise ValueError("student edition marker is missing")
    if re.search(r"(?i)instructor use only|private solution|answer key|rubric", content):
        raise ValueError("restricted material in the student PDF")
    print(f"{packet.name}: {len(reader.pages)} pages, canonical question headings and student marker checked")


def find_tool(name: str) -> str:
    direct = shutil.which(name)
    if direct:
        return direct
    candidates = [
        Path(os.environ.get("POPPLER_BIN", "/nonexistent")) / name,
        Path.home() / ".cache/codex-runtimes/codex-primary-runtime/dependencies/native/poppler/poppler/bin" / name,
    ]
    for candidate in candidates:
        if candidate.is_file():
            return str(candidate)
    raise ValueError(f"required tool is missing: {name}")


def compile_packet(packet: Packet) -> None:
    path = ROOT / packet.relative_path
    lyx = os.environ.get("LYX_BIN", shutil.which("lyx") or "/Applications/LyX.app/Contents/MacOS/lyx")
    subprocess.run([lyx, "--export", "pdflatex", path.name], cwd=path.parent, check=True)
    subprocess.run([
        find_tool("latexmk"), "-pdf", "-silent", "-interaction=nonstopmode",
        "-halt-on-error", path.with_suffix(".tex").name,
    ], cwd=path.parent, check=True)
    pdf = path.with_suffix(".pdf")
    images = subprocess.check_output([find_tool("pdfimages"), "-list", str(pdf)], text=True)
    fonts = subprocess.check_output([find_tool("pdffonts"), str(pdf)], text=True)
    if any(row.strip() for row in images.splitlines()[2:]):
        raise ValueError(f"raster image in {packet.name}")
    for row in fonts.splitlines()[2:]:
        if row.strip() and ("Type 3" in row or row.split()[-5] != "yes"):
            raise ValueError(f"unsafe font in {packet.name}: {row}")
    check_pdf(packet)
    print(f"{packet.name}: vector and embedded font preflight passed")


def main() -> None:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument("--check", action="store_true")
    parser.add_argument("--check-pdf", action="store_true")
    parser.add_argument("--compile", action="store_true")
    parser.add_argument("--case", choices=[p.name for p in PACKETS])
    args = parser.parse_args()
    packets = tuple(p for p in PACKETS if args.case is None or p.name == args.case)
    chapters, book = parse_problem_bank(BANK), BOOK.read_text()
    for packet in packets:
        if args.check_pdf:
            check_pdf(packet)
            continue
        source = build_packet(packet, chapters, book)
        target = ROOT / packet.relative_path
        if args.check:
            if not target.exists() or target.read_text() != source:
                raise SystemExit(f"{packet.name} packet is not synchronized with the bank")
            print(f"{packet.name} packet matches {', '.join(packet.identifiers)}")
        else:
            target.parent.mkdir(parents=True, exist_ok=True)
            target.write_text(source)
            print(target)
        if args.compile:
            compile_packet(packet)


if __name__ == "__main__":
    main()
