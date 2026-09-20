#!/usr/bin/env python3
"""Keep the book roadmap and cross-references aligned with the current architecture."""

from __future__ import annotations

import argparse
import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]
BOOK = ROOT / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"


REPLACEMENTS = (
    (
        "book roadmap",
        """The material is cumulative.
 Part I develops the mathematical language of binary relations and connects preferences to observable choice.
 Part II derives individual demand and extends the benchmark model to limited attention and uncertainty.
 Part III studies aggregation and stochastic choice.
 Part IV develops production,
 competitive markets,
 and general equilibrium.
 Part V treats equilibrium restrictions,
 trade under uncertainty,
 matching,
 and computable general equilibrium.""",
        """The material is cumulative.
 Part I begins with utility maximization and consumer demand,
 then develops duality,
 comparative statics,
 welfare,
 revealed preference,
 and abstract choice.
 Part II studies expected utility,
 stochastic choice,
 limited attention,
 and rational inattention.
 Part III turns to aggregation and representative consumers.
 Part IV develops production,
 competitive markets,
 and general equilibrium.
 Part V treats equilibrium restrictions,
 sequential trade,
 matching,
 and computable general equilibrium.
 Appendix A collects order theory,
 Appendix B records the exact versions of starred theorems,
 and the Glossary of Symbols provides linked notation.""",
    ),
    (
        "notation-glossary pointer",
        "In the PDF, a symbol shown in dark blue at its first substantive use links to its entry in Appendix B;",
        "In the PDF, a symbol shown in dark blue at its first substantive use links to its entry in the Glossary of Symbols;",
    ),
    (
        "continuous-representation pointer",
        "The continuous-utility theorem used later is stated in the consumer-theory chapter.",
        "The next theorem gives the continuous-utility result for the Euclidean commodity space used in Chapter 1.",
    ),
    (
        "glossary introduction",
        "This appendix records the book's persistent notation.  Each blue symbol links back to its first substantive use in the text.  There, the blue first use links here.  A symbol described as scoped may be reused only after the new local meaning is stated explicitly.",
        "This glossary records the book's persistent notation.  Each blue symbol links back to its first substantive use in the text.  There, the blue first use links here.  A symbol described as scoped may be reused only after the new local meaning is stated explicitly.",
    ),
)


def phrase_pattern(phrase: str) -> re.Pattern[str]:
    """Match a prose phrase independently of LyX's physical line wrapping."""
    tokens = phrase.split()
    if not tokens:
        raise ValueError("editorial phrase must not be empty")
    return re.compile(r"[ \t\r\n]+".join(re.escape(token) for token in tokens))


def rewrite(source: str) -> str:
    revised = source
    for label, old, new in REPLACEMENTS:
        old_matches = list(phrase_pattern(old).finditer(revised))
        new_matches = list(phrase_pattern(new).finditer(revised))
        if new_matches:
            if len(new_matches) != 1:
                raise ValueError(
                    f"{label}: expected one new match, found {len(new_matches)}"
                )
            if old_matches:
                raise ValueError(f"{label}: both old and new text are present")
            continue
        if len(old_matches) != 1:
            raise ValueError(
                f"{label}: expected one old match, found {len(old_matches)}"
            )
        match = old_matches[0]
        revised = revised[: match.start()] + new + revised[match.end() :]
    return revised


def main() -> None:
    parser = argparse.ArgumentParser()
    mode = parser.add_mutually_exclusive_group(required=True)
    mode.add_argument("--check", action="store_true")
    mode.add_argument("--apply", action="store_true")
    args = parser.parse_args()

    source = BOOK.read_text()
    revised = rewrite(source)
    if args.check:
        if revised != source:
            raise SystemExit("front-matter and roadmap polish is pending")
        print("front-matter and roadmap polish is present")
    elif revised != source:
        BOOK.write_text(revised)
        print(f"updated {BOOK}")
    else:
        print("no changes needed")


if __name__ == "__main__":
    main()
