#!/usr/bin/env python3
"""Remap the public problem bank to the reorganized Fall 2026 chapters.

Existing prompts are preserved verbatim apart from their numeric identifiers.
``problems/PROBLEM_ID_ALIASES.tsv`` records every old-to-new number so weekly
handouts and older citations remain traceable.
"""

from __future__ import annotations

import argparse
import re
from dataclasses import dataclass
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BANK = ROOT / "problems" / "PROBLEM_BANK.md"
ALIASES = ROOT / "problems" / "PROBLEM_ID_ALIASES.tsv"
STAMP = "<!-- ECON803_PROBLEM_RESTRUCTURE:1 -->"


@dataclass(frozen=True)
class Problem:
    old_id: str
    level: str
    title: str
    body: str
    old_chapter: str


TARGETS: tuple[tuple[str, tuple[tuple[str, str], ...]], ...] = (
    ("Utility Maximization and Consumer Demand", (("1.1", "1.1"),)),
    (
        "Duality, Comparative Statics, and Welfare",
        (("3.1", "2.1"), ("1.3", "2.2"), ("3.4", "2.3")),
    ),
    (
        "Revealed Preference and Recoverability",
        (("1.2", "3.1"), ("3.2", "3.2"), ("3.3", "3.3"), ("3.5", "3.4")),
    ),
    (
        "Choice Without Budget Geometry",
        (("2.1", "4.1"), ("2.2", "4.2"), ("2.3", "4.3")),
    ),
    (
        "Expected Utility and Risk",
        (("5.1", "5.1"), ("5.2", "5.2"), ("5.3", "5.3"), ("5.4", "5.4")),
    ),
    (
        "Stochastic Choice and Random Utility",
        (("7.1", "6.1"), ("7.2", "6.2"), ("7.3", "6.3")),
    ),
    (
        "Limited Attention and Costly Information",
        (("4.1", "7.1"), ("4.2", "7.2"), ("4.3", "7.3")),
    ),
    (
        "Aggregate Demand and Representative Consumers",
        (("6.1", "8.1"), ("6.2", "8.2"), ("6.3", "8.3")),
    ),
    (
        "Theory of the Firm",
        (("8.1", "9.1"), ("8.2", "9.2"), ("8.3", "9.3"), ("8.4", "9.4")),
    ),
    (
        "Competitive Markets and Partial Equilibrium",
        (("9.1", "10.1"), ("9.2", "10.2"), ("9.3", "10.3")),
    ),
    (
        "General Equilibrium Theory",
        (("10.1", "11.1"), ("10.2", "11.2"), ("10.3", "11.3"), ("10.4", "11.4")),
    ),
    (
        "Positive Theory of Equilibrium",
        (("11.1", "12.1"), ("11.2", "12.2"), ("11.3", "12.3"), ("11.4", "12.4")),
    ),
    (
        "Testable Restrictions on the Equilibrium Manifold",
        (("12.1", "13.1"), ("12.2", "13.2"), ("12.3", "13.3")),
    ),
    (
        "Sequential Trade",
        (("13.1", "14.1"), ("13.2", "14.2"), ("13.3", "14.3")),
    ),
    (
        "Matching",
        (("14.1", "15.1"), ("14.2", "15.2"), ("14.3", "15.3")),
    ),
    (
        "Computable General Equilibrium",
        (("15.1", "16.1"), ("15.2", "16.2"), ("15.3", "16.3")),
    ),
    (
        "Order Theory",
        (("A.1", "A.1"), ("A.2", "A.2"), ("A.3", "A.3"), ("A.4", "A.4")),
    ),
)

CMU_PROBLEMS = r'''## 3.5 | Core | Classical utility as singleton CMU

Let $u:X\to\mathbb R$ be continuous, let $\Omega_u=\{\{u\}\}$, and define
$r_{\Omega_u}(x,y)=\max_{U\in\Omega_u}\min_{v\in U}[v(x)-v(y)]$.

(a) Prove that $r_{\Omega_u}(x,y)=u(x)-u(y)$.

(b) Prove that $x_{r_{\Omega_u}}(p,w)=\arg\max_{x\in B(p,w)}u(x)$.

(c) Explain precisely which conclusions require continuity, strict monotonicity, or concavity of $u$, and which do not.

## 3.6 | Proof | WGARP without GARP

Consider prices $p^1=(4,1,5)$, $p^2=(5,4,1)$, $p^3=(1,5,4)$ and choices $x^1=(4,1,1)$, $x^2=(1,4,1)$, $x^3=(1,1,4)$.

(a) Compute the $3\times3$ matrix with $(t,s)$ entry $p^t\cdot x^s$.

(b) Show that the data satisfy WGARP and WARP but violate GARP. Identify the revealed three-cycle and explain why no pair forms a reversal.

(c) Suppose an asymmetric, strictly increasing preference function $r$ rationalizes two choices $x\in x_r(p,w)$ and $x'\in x_r(p',p'\cdot x)$. Prove the compensated law of demand $(p'-p)\cdot(x'-x)\leq0$. State where nonemptiness of demand is used.
'''


def parse(source: str) -> dict[str, Problem]:
    current_chapter: str | None = None
    matches = list(re.finditer(r"(?m)^## ([^|\n]+)\| ([^|\n]+)\| ([^\n]+)$", source))
    chapter_matches = list(re.finditer(r"(?m)^# (?!Publication problem bank$)([^\n]+)$", source))
    problems: dict[str, Problem] = {}
    for index, match in enumerate(matches):
        preceding = [item for item in chapter_matches if item.start() < match.start()]
        if not preceding:
            raise ValueError(f"problem {match.group(1).strip()} has no chapter")
        current_chapter = preceding[-1].group(1).strip()
        end_candidates = [
            value
            for value in (
                matches[index + 1].start() if index + 1 < len(matches) else len(source),
                next(
                    (item.start() for item in chapter_matches if item.start() > match.start()),
                    len(source),
                ),
            )
            if value > match.start()
        ]
        end = min(end_candidates)
        identifier = match.group(1).strip()
        if identifier in problems:
            raise ValueError(f"duplicate problem ID {identifier}")
        problems[identifier] = Problem(
            old_id=identifier,
            level=match.group(2).strip(),
            title=match.group(3).strip(),
            body=source[match.end() : end].strip(),
            old_chapter=current_chapter,
        )
    return problems


def render(source: str) -> tuple[str, str]:
    problems = parse(source)
    planned = [old for _, pairs in TARGETS for old, _ in pairs]
    if set(planned) != set(problems):
        raise ValueError(
            f"problem map mismatch; missing={sorted(set(problems)-set(planned))}, "
            f"unknown={sorted(set(planned)-set(problems))}"
        )

    chunks = [
        "# Publication problem bank\n\n",
        "This file is the editable source for the end-of-chapter problems in the Fall 2026 textbook. Each problem has a stable current identifier and one of three labels: Core, Proof, or Applied. The public book contains questions only; solutions are maintained in the private instructor repository. Legacy Fall 2024/Fall 2026-baseline numbers are recorded in `PROBLEM_ID_ALIASES.tsv`.\n\n",
        STAMP + "\n\n",
    ]
    aliases = ["old_id\tnew_id\told_chapter\tnew_chapter\tnote"]
    for chapter, pairs in TARGETS:
        chunks.append(f"# {chapter}\n\n")
        for old_id, new_id in pairs:
            item = problems[old_id]
            chunks.append(f"## {new_id} | {item.level} | {item.title}\n\n")
            chunks.append(item.body + "\n\n")
            note = "unchanged" if old_id == new_id else "renumbered after consumer-block restructure"
            aliases.append(
                "\t".join((old_id, new_id, item.old_chapter, chapter, note))
            )
        if chapter == "Revealed Preference and Recoverability":
            chunks.append(CMU_PROBLEMS.strip() + "\n\n")
    return "".join(chunks).rstrip() + "\n", "\n".join(aliases) + "\n"


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    args = parser.parse_args()
    source = BANK.read_text()
    if STAMP in source:
        if not ALIASES.is_file():
            raise SystemExit("problem bank is migrated but alias ledger is missing")
        print("problem bank restructure is present")
        return
    bank, aliases = render(source)
    if args.check:
        raise SystemExit("problem bank restructure is pending")
    BANK.write_text(bank)
    ALIASES.write_text(aliases)
    print(f"updated {BANK} and {ALIASES}")


if __name__ == "__main__":
    main()
