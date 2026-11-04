# The Price of Proof

Released for ECON 803 independent study during November 9 to 13, 2026. English throughout. Total running time: thirty minutes, in two parts of approximately fifteen minutes each.

There is no ECON 803 class on Friday, November 13. I will be in California that week to present my research at Caltech and work on research with possible collaborators. Use the episode and [reading guide](../README.md) in place of our class.

[Complete episode](ECON803_The_Price_of_Proof_30_Minutes_English.mp3)

[Opening preview, 60 seconds](ECON803_The_Price_of_Proof_Preview_English.mp3), separately encoded from the final mix.

[Part One: the historical drama](ECON803_The_Price_of_Proof_Part_1_English.mp3)

[Part Two: the proof and the invisible hand](ECON803_The_Price_of_Proof_Part_2_English.mp3)

[English transcript and sources](ECON803_The_Price_of_Proof_Transcript_English.md)

Part One follows the competition over equilibrium existence, Nash’s mathematical contribution, the editorial record and the debate over credit. It places the result beside questions about markets and planning in the Cold War. Short document excerpts receive distinct performed readings.

Part Two is a conceptual guide for PhD students. It separates allocation space from price space, constructs the capped demand map, explains the fixed point contradiction, and checks price positivity, market clearing and removal of the artificial cap. It then introduces the Kakutani extension and distinguishes existence from welfare, distribution, uniqueness, convergence, computation and information.

Part One uses a synthetic voice based on Victor’s authorized recording. Part Two uses a clear English narrator. Other synthetic readers perform the document excerpts. The source recording stays private and is not included in the episode. These are performed readings rather than original historical recordings.

## Listen with pencil and paper

Use Chapter 11, especially §11.3, and Appendix B of the [live textbook](../../../../notes/Microeconomics_1_notes_by_Victor_Aguiar.pdf). The source remains the LyX textbook.

1. Draw an [Edgeworth box](../../../../notes/figures/tikz/edgeworth_coordinates.pdf). Each point assigns resources to consumers. Put this beside a separate drawing of normalized price space.
2. Draw a triangle for three nonnegative prices summing to one. The edges include zero prices. Think about why ordinary demand may fail there, and why the proof first caps each person’s choices.
3. Draw arrows for the auxiliary price map. Positive excess demand adds weight to a price; normalization returns the point to the simplex. The map is a mathematical device, with no convergence claim attached to the drawing.
4. Inspect the [scalar fixed point illustration](../../../../notes/figures/tikz/ge_fixed_point.pdf). The curve crosses the diagonal at a clearing price in the worked economy. Keep this scalar illustration distinct from the general simplex map.
5. Write the sequence: summed budget inequalities, no positive excess demand, room below the cap, positive prices, binding budgets, exact clearing, unrestricted optimality. Mark where each assumption enters.

In the November 4 textbook build, §11.3 is on printed pages 139 to 141, Appendix B on pages 215 to 217, and Figure 11.6 floats to page 166. Follow section titles if later builds move the pages.

## Reproduce the audio

The [script](episode_30min_v1.json) contains the two parts, document readings, source references and visual cues. [The producer](../produce_full_episode.py) renders short resumable segments, keeps private reference data in a separate cache, measures each part and adjusts pacing to fifteen minutes. The final MP3 includes two chapters.

The producer requires MLX Audio, NumPy, SoundFile, num2words, FFmpeg and the local voice models. It takes explicit paths for the private reference audio, its transcript and the cache. No private reference data are stored in this folder. Content hashes and measured timings accompany the finished audio. Historical years and calendar dates are spelled out for synthesis while retaining their ordinary written form in the transcript.

[release_qa.json](release_qa.json) records final encoded audio measurements and the limits of the review. The final master applies a gain of minus 0.7 dB to retain peak headroom after encoding. Technical checks and automatic transcription do not establish a human listening review.
