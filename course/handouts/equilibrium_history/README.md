# The Race to Prove the Invisible Hand

McKenzie, Arrow and Debreu. ECON 803 self study for November 9 to 13, 2026.

[Listen to the episode (MP3)](https://raw.githubusercontent.com/vaguiarl/Econ803Micro1SFUFall2026/main/course/handouts/equilibrium_history/ECON803_The_Race_to_Prove_the_Invisible_Hand.mp3) or [read the transcript and sources](TRANSCRIPT.md). The recording uses synthetic narration and does not reproduce anyone's voice. Reading the transcript is an equivalent way to use the episode.

There is no ECON 803 class on Friday, November 13. Use this week to understand the existence argument and its assumptions. The episode connects the history of scientific credit to a precise question: when can individually optimal plans fit together at common prices?

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

Historical claims are attributed in the transcript. The episode distinguishes archival evidence from judgments about motives and includes a critical perspective on the historical interpretation. It contains no reenacted dialogue or invented quotations. Its economic example follows the authoritative LyX notes.

The editable script is [episode.json](episode.json). The transcript and audio can be rebuilt on macOS with the installed Daniel voice, Python 3 and FFmpeg:

```sh
python3 course/handouts/equilibrium_history/build_episode.py
```

Use `--transcript-only` to regenerate the transcript on another platform. The build records chapter timings, the voice, duration and content hashes in `audio_manifest.json` and decodes the complete MP3 to check encoding integrity. Audio synthesis requires no API credentials. It is a course audio episode with a transcript, rather than a subscription podcast feed.
