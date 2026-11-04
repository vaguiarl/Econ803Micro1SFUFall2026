# The Price of Proof

McKenzie, Arrow and Debreu. ECON 803 self study for November 9 to 13, 2026.

[Listen to the complete 30 minute English episode (MP3)](https://raw.githubusercontent.com/vaguiarl/Econ803Micro1SFUFall2026/main/course/handouts/equilibrium_history/first_version/ECON803_The_Price_of_Proof_30_Minutes_English.mp3) or [read the English transcript and sources](first_version/ECON803_The_Price_of_Proof_Transcript_English.md). Reading the transcript is an equivalent way to use the episode. This version replaces the earlier 13 minute recording.

There is no ECON 803 class on Friday, November 13. I will be in California that week to present my research at Caltech and work on research with possible collaborators. Use this episode and the assigned reading for independent study in place of our class.

The episode connects the history of scientific credit to a precise question: when can individually optimal plans fit together at common prices? Each part runs approximately fifteen minutes.

1. [Part One: the historical drama](https://raw.githubusercontent.com/vaguiarl/Econ803Micro1SFUFall2026/main/course/handouts/equilibrium_history/first_version/ECON803_The_Price_of_Proof_Part_1_English.mp3) follows McKenzie, Arrow and Debreu, Nash's contribution, the documented editorial record and the debate over priority. It places the result in the context of markets and planning during the Cold War.
2. [Part Two: the proof and the invisible hand](https://raw.githubusercontent.com/vaguiarl/Econ803Micro1SFUFall2026/main/course/handouts/equilibrium_history/first_version/ECON803_The_Price_of_Proof_Part_2_English.mp3) explains how to visualize the existence argument, why its assumptions matter and what existence tells us about the invisible hand.

Part One uses a synthetic voice based on Victor's authorized recording. Part Two uses a clear English narrator. Other synthetic readers perform short document excerpts. These are performed readings, rather than original historical recordings. The source recording remains private.

## Reading in the live notes

Use [the current textbook PDF](https://raw.githubusercontent.com/vaguiarl/Econ803Micro1SFUFall2026/main/notes/Microeconomics_1_notes_by_Victor_Aguiar.pdf). Chapter 11 is the unified General Equilibrium chapter.

| Priority | Reading | Printed pages | PDF viewer pages |
| :--- | :--- | :--- | :--- |
| Main reading | §11.3, Existence through a continuous price map | 139–141 | 152–154 |
| Foundation and review | §11.1, Pure exchange economies: the Edgeworth box; §11.2, From individual choices to aggregate excess demand | 130–139 | 143–152 |
| Technical follow through | Appendix B, Fixed Points and Equilibrium Existence | 215–217 | 228–230 |

Page numbers refer to the November 4 PDF. Use section titles if a later build moves them. Figure 11.6, the fixed point illustration introduced in §11.3, currently floats to printed p.166, PDF viewer p.179.

Read Appendix B with three questions in mind: why are boundary prices delicate, why can the artificial consumption cap be removed, and what changes when demand has several optimal choices? The local Lean project does not certify the analytic equilibrium existence proof.

## A study plan

1. Listen to the episode or read its transcript. Keep a list of claims about existence, efficiency, uniqueness and stability. Give each claim its own meaning.
2. Read §11.3. Review §§11.1–11.2 wherever the economic objects need refreshing. State the main theorem in words, then list its hypotheses.
3. Read Appendix B. Draw a dependency map from capped choice problems to the fixed point and then to market clearing. Mark where each assumption is used.
4. Reconstruct the chapter's two consumer example by hand. Explain each step before calculating it.

The worked economy has $\omega_1=(1,3)$, $\omega_2=(3,1)$ and $u_i(x_i)=\sqrt{x_{i1}x_{i2}}$. With $p=(s,1-s)$, the notes obtain

$$
z_1(s)=\frac{2}{s}-4,\qquad T(s)=s+\frac{z_1(s)}{32},\qquad s\in[1/10,9/10].
$$

Here $x_{i\ell}$ is consumer $i$'s consumption of good $\ell$, $\omega_i$ is that consumer's endowment, $p$ is the price vector, $z_1$ is aggregate excess demand for good 1, and $T$ is the auxiliary price map. Verify that $T$ maps the stated interval into itself. Draw its graph and the diagonal, solve $T(s)=s$, recover both consumers' bundles, and use Walras's law to explain why the second market clears. Explain why this construction alone does not establish convergence of price adjustment in general.

For your own preparation, write short answers to these prompts:

1. Why does counting equations and unknowns fail to establish equilibrium existence?
2. Which hypotheses let the chapter apply Brouwer, and what economic work do they do?
3. Why does a fixed point of the constructed map imply the relevant equilibrium conditions?
4. What changes in the proof when demand is a correspondence, and where does Kakutani enter?
5. How should we describe the contributions of McKenzie, Arrow and Debreu while distinguishing documented chronology from interpretation?

No additional submission is required for this activity. The separate [problem set on the firm and partial equilibrium](https://canvas.sfu.ca/courses/16693/assignments/241163) remains due Friday, November 13, at 11:59 p.m., Vancouver time.

## Sources and production

Historical claims are attributed in the transcript. The episode distinguishes archival evidence and retrospective testimony from interpretations of motives. Its economic example follows the authoritative LyX notes.

The [release package](first_version/README.md) contains both parts, the complete episode, transcript, source notes, editable script, production manifests and technical QA. [CURRENT.json](CURRENT.json) identifies the current released version and its content hashes.

The earlier recording and its original script remain available as a superseded edition. The current version uses [produce_full_episode.py](produce_full_episode.py); see the release package for its dependencies and private input requirements. It is a course audio episode with a transcript, rather than a subscription podcast feed.
