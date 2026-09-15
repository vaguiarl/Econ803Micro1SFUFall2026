from pathlib import Path


path = Path(__file__).resolve().parents[1] / "notes" / "Microeconomics_1_notes_by_Victor_Aguiar.lyx"
s = path.read_text()
replacements = {
    "To incentivize decision making.": "To model a decision-maker's incentives,",
    "and his demand lie on the offer curve:": "and the demand lies on the offer curve:",
    "and then we can plug-it back in the OC for consumer 1 and 2 to obtain the allocations": "and substituting this ratio into the two offer curves gives the equilibrium allocation",
    "Any Walrasian Equilibrim allocation": "Any Walrasian-equilibrium allocation",
    "Claim 10 is saying is that the decentralized problem stated before has the same solution as the central planner problem.": "Claim 10 states that, under the stated assumptions, the decentralized equilibrium and the central-planner problem have the same allocation.",
    "Preferences maximization imply (ii) but (ii) does not implies preference maximization.": "Preference maximization implies (ii), but (ii) alone does not imply preference maximization.",
    "such tht": "such that",
    "We know that under certain conditions on preferences there exists a Walrasian equilibrium.": "Under the existence assumptions stated below, a Walrasian equilibrium exists.",
    "thus we cannot remain in equilibrium.": "so the proposed allocation cannot be an equilibrium.",
    "Step 1.We show": "Step 1. We show",
    "We show If ": "We show that if ",
    "We show For every ": "We show that for every ",
    "We show The wealth levels": "We show that the wealth levels",
    "Because of steps 5 and 6 we have.": "By Steps 5 and 6,",
    "the continuity of \\begin_inset Formula $\\succeq_{i}$\\end_inset\n\n imply": "continuity of \\begin_inset Formula $\\succeq_{i}$\\end_inset\n\n implies",
    "We say that the \n\\series bold\nSlutsky Matrix\n\\series default\nThe Slutsky matrix of a demand function": "The Slutsky matrix of a demand function",
}
for old, new in replacements.items():
    if old not in s:
        print(f"warning: not found: {old!r}")
    s = s.replace(old, new)
path.write_text(s)
print(f"cleaned prose in {path}")
