# The Price of Proof

Released for ECON 803 independent study during November 9 to 13, 2026. English throughout. Total running time: thirty minutes, in two parts of approximately fifteen minutes each.

Part One was recast on November 4 with the energetic English delivery approved by Victor. The links below serve this updated edition.

There is no ECON 803 class on Friday, November 13. I will be in California that week to present my research at Caltech and work on research with possible collaborators. Use the episode and [reading guide](../README.md) in place of our class.

[Complete episode](ECON803_The_Price_of_Proof_30_Minutes_English.mp3)

[Opening preview, 60 seconds](ECON803_The_Price_of_Proof_Preview_English.mp3), copied from the final encoded mix.

[Part One: the historical drama](ECON803_The_Price_of_Proof_Part_1_English.mp3)

[Part Two: the proof and the invisible hand](ECON803_The_Price_of_Proof_Part_2_English.mp3)

[English transcript and sources](ECON803_The_Price_of_Proof_Transcript_English.md)

Part One follows the competition over equilibrium existence, Nash’s mathematical contribution, the editorial record and the debate over credit. It places the result beside questions about markets and planning in the Cold War. Short document excerpts receive distinct performed readings.

Part Two is a conceptual guide for PhD students. It separates allocation space from price space, constructs the capped demand map, explains the fixed point contradiction, and checks price positivity, market clearing and removal of the artificial cap. It then introduces the Kakutani extension and distinguishes existence from welfare, distribution, uniqueness, convergence, computation and information.

Part One uses Victor’s authorized synthetic teaching voice, recast locally with his approved energetic English delivery. Part Two uses a clear English narrator. Other synthetic readers perform the document excerpts. Source recordings stay private and are not included in the episode. These are performed readings rather than original historical recordings.

## Listen with pencil and paper

Use Chapter 11, especially §11.3, and Appendix B of the [live textbook](../../../../notes/Microeconomics_1_notes_by_Victor_Aguiar.pdf). The source remains the LyX textbook.

1. Draw an [Edgeworth box](../../../../notes/figures/tikz/edgeworth_coordinates.pdf). Each point assigns resources to consumers. Put this beside a separate drawing of normalized price space.
2. Draw a triangle for three nonnegative prices summing to one. The edges include zero prices. Think about why ordinary demand may fail there, and why the proof first caps each person’s choices.
3. Draw arrows for the auxiliary price map. Positive excess demand adds weight to a price; normalization returns the point to the simplex. The map is a mathematical device, with no convergence claim attached to the drawing.
4. Inspect the [scalar fixed point illustration](../../../../notes/figures/tikz/ge_fixed_point.pdf). The curve crosses the diagonal at a clearing price in the worked economy. Keep this scalar illustration distinct from the general simplex map.
5. Write the sequence: summed budget inequalities, no positive excess demand, room below the cap, positive prices, binding budgets, exact clearing, unrestricted optimality. Mark where each assumption enters.

In the November 4 textbook build, §11.3 is on printed pages 139 to 141, Appendix B on pages 215 to 217, and Figure 11.6 floats to page 166. Follow section titles if later builds move the pages.

## Script and production

The [current script](episode_30min_v2.json) contains the two parts, document readings, source references and visual cues. [The earlier producer](../produce_full_episode.py) documents the original rendering workflow. The current edition uses cached local narration, retains the four document readings, and preserves the standalone Part Two recording. The final MP3 includes two chapters.

Local production uses MLX Audio, NumPy, SoundFile, FFmpeg and local voice models. Reference audio, its transcript and the segment cache remain private. Content hashes and measured timings accompany the finished audio. Historical years and calendar dates are spelled out for synthesis while retaining their ordinary written form in the transcript. One sentence was clarified to read “protect authors and support credible decisions.”

[release_qa.json](release_qa.json) records final encoded audio measurements and the limits of the review. Part One was normalized in two measured passes. The standalone Part Two MP3 is unchanged; the combined MP3 reencodes its preserved audio. Technical checks and automatic transcription do not establish a full human listening review.
