# Figure audit and vector reconstruction

**Audit date:** 2026-09-19

**Manuscript audited:** `notes/Microeconomics_1_notes_by_Victor_Aguiar.lyx`

**Repository snapshot:** `eee2573166e1` plus the figure-workspace files described below

## Executive finding

At the audited snapshot, the authoritative LyX manuscript included exactly
**five** external graphics, all 96-dpi PNGs. At their former LyX scales their effective
resolution is approximately 96--213 dpi, below a conservative 300-dpi print
standard; text, rules, and curves are therefore visibly soft. Two of the five
are tables saved as screenshots, which also creates accessibility and editing
problems.

All five now have reviewed, one-page vector replacements in
`notes/figures/tikz/`. The empirical plots were recovered from the original
vector slides rather than traced from the PNGs; the two tables were freshly
typeset from source values; and the FOSD diagram was replaced by a new,
mathematically explicit illustration. The build verifies embedded fonts and the
absence of raster image objects.

**Post-audit integration status.** The LyX manuscript now links all five checked
PDFs, uses corrected self-contained captions and primary citations, and builds
to a final PDF with no raster image objects, Type 3 fonts, or unembedded fonts.
The five superseded PNGs and nine unreferenced legacy assets have been removed
from the current public release tree. They remain recoverable from commit
`eee2573166e1` if a private provenance archive needs another copy.

The directory also contained nine tracked but unreferenced legacy assets and
eleven ignored EPS conversion files. Several of the legacy PDFs appear to be
low-resolution textbook or article scans with no rights record. They no longer
ship in the current public tree.

## Scope and method

The inventory was obtained by parsing every `Graphics` inset in the LyX source,
then reconciling those references with every file physically present under
`notes/figures/` and every path tracked by Git. This accounts for:

- 5 referenced source assets;
- 9 unreferenced, tracked legacy assets; and
- 11 untracked/ignored EPS conversion products.

PNG dimensions and metadata were read directly from the files. Effective DPI
is `96 / LyX scale` when a scale is declared and 96 dpi at the natural size.
For legacy PDFs, `pdfinfo`, `pdfimages`, and `pdffonts` were used to distinguish
true vectors from page-sized raster wrappers. The EPS files identify
ImageMagick as their creator and contain raster image data; changing the
container from PNG/PDF to EPS did not make them vector artwork.

## Figures at the audited snapshot and their replacements

| LyX location | Current asset | Kind | Current quality | Caption and provenance status | Rebuild and recommendation |
|---|---|---|---|---|---|
| line 4811; scale 80% | `rationality_experiment.png` | Empirical budget/choice plot | 524×492 px; 96-dpi metadata; **120 effective dpi** | Caption: “Subject 216 (symmetric treatment). Source: Quah.” This is not a publication citation. | `tikz/rationality_experiment.pdf`; faithful coordinates recovered from Quah's source vector. Retain subject/treatment wording, add full Quah and underlying Choi et al. citations, and resolve reproduction permission. |
| line 4924; scale 65% | `CCEI_Afriat_index.png` | Empirical and simulated survival curves | 734×569 px; 96-dpi metadata; **148 effective dpi** | Caption: “CCEI Source: Quah.” Dataset, simulation, date, and full source are omitted. The old y label says “Percentage” but uses a 0--1 scale. | `tikz/ccei_afriat_index.pdf`; faithful curves recovered from Quah's vector. The rebuild labels the ordinate as a share. Add a full citation and specify the sample/simulation in the surrounding text if known. |
| line 7031; natural size | `fosd.png` | Didactic CDF diagram | 513×311 px; **96 effective dpi** | Caption: “First order stochastic dominance. Option A dominates Option B.” No source is stated. The underlying distributions are not defined. | `tikz/fosd.pdf`; new semantic illustration with declared CDFs and the correct inequality. Use the caption proposed below and hyphenate “first-order.” |
| line 7445; scale 60% | `polissonquah_passingrates_table_expectedutility.png` | Screenshot of a numerical table | 665×277 px; 96-dpi metadata; **160 effective dpi** | Caption gives no source. The values match Table 1 of Polisson and Quah's 2013 working paper, not merely the later three-author AER article discussed nearby. | `tikz/passing_rates_expected_utility.pdf`; exact values freshly typeset. For the final book, prefer a native LyX table and cite the 2013 source explicitly. |
| line 7490; scale 45% | `holt_laury.png` | Screenshot conflating the price-list design and an empirical frequency table | 871×287 px; 96-dpi metadata; **213 effective dpi** | Caption gives no source. The last two columns sum to one because they are distributions over the **number of safe choices**; they are not row-wise proportions choosing Option B. Combining those columns with ten individual lottery rows gives them the wrong statistical unit. | `tikz/holt_laury.pdf`; corrected to an exact, clearly labeled subset of Holt and Laury (2002, Table 3): safe-choice count, CRRA interval, low-real ($\times1$), and real $\times20$ distributions. Prefer a native LyX table in the final book. |

### 1. Subject 216 revealed-preference plot

The source is John K.-H. Quah, *Survey Lecture on Revealed Preference
Analysis*, QUT, 16 November 2015, PDF page 31 (slide 13/37):
[source slides](https://www.johnquah.com/uploads/7/5/6/7/75676677/survey-qutweb.pdf).
The audited PDF has SHA-256 digest
`f2dea2324abac5624ad3ef23a9a96dc7b805bf1843382d4688cd42d0eae2e1a8`.
The slide attributes the experiment to Choi, Fisman, Gale, and Kariv,
“Consistency and Heterogeneity of Individual Behavior under Uncertainty,”
*American Economic Review* 97(5), 1921--1938
([DOI](https://doi.org/10.1257/aer.97.5.1921)).

The extraction recovers all 50 clipped budget segments and all 50 chosen
bundles. Pairing choices and budgets in the source-vector order gives a maximum
perpendicular discrepancy of 0.0644 on a 0--100 axis, consistent with rounding
of plotted coordinates. No data were inferred from pixels.

**Proposed caption:** “Revealed-preference choices of Subject 216 in the
symmetric treatment. Gray lines are observed budgets, black dots are chosen
bundles, and the dashed line is the 45-degree line. Coordinates recovered from
Quah (2015, slide 13); underlying experiment: Choi et al. (2007).”

**Rights action:** Quah's slides state no reusable license. Coordinate facts and
a fresh rendering reduce, but do not eliminate, permissions risk. Obtain the
author's permission for wide commercial circulation or reconstruct directly
from the experiment's archived data under its terms.

### 2. CCEI survival curves

The observed curve appears on PDF page 46 and the observed-plus-simulated
version on page 47 of the same Quah slide deck. The extractor recovers 73
vertices for the observed path and 1,042 vertices across the 14 dashed
fragments of the simulated path. The rebuild uses those source-vector
coordinates and applies a fresh visual style.

The old image's ordinate is a proportion, despite the word “Percentage.” The
replacement uses “Share with CCEI $\geq \alpha$.” The exact empirical sample
and simulation protocol were not independently recoverable from the image and
must not be guessed.

**Proposed caption:** “Share of observations whose CCEI is at least
$\alpha$: observed GARP compliance and Quah's simulated GARP benchmark. Curves
recovered from Quah (2015, slide 27).” Add the sample and simulation design only
after checking the source research file.

**Rights action:** same as for the Subject 216 plot.

### 3. First-order stochastic dominance

The legacy drawing stated the ordering but supplied no distributions or source.
The replacement is an original, reproducible illustration. It uses

\[
F_A(z)=\frac{1}{1+\exp(-(z-110)/18)},\qquad
F_B(z)=\frac{1}{1+\exp(-(z-70)/18)}.
\]

Because the logistic CDF is increasing and Option A is a 40-unit right shift,
$F_A(z)\leq F_B(z)$ for every real $z$. Therefore A first-order stochastically
dominates B. The plotted range is $0\leq z\leq200$; the mathematical claim is
global.

**Proposed caption:** “First-order stochastic dominance. Option A is a
rightward location shift of Option B, so $F_A(z)\leq F_B(z)$ for every payoff
$z$.” No external-image permission is required for this new illustration.

### 4. Revealed-preference passing rates

The values are Table 1 on page 17 of Matthew Polisson and John K.-H. Quah,
“Revealed Preference Tests under Risk and Uncertainty,” University of Leicester
Working Paper 13/24 (December 2013):
[working paper](https://www.le.ac.uk/economics/research/RePEc/lec/leecon/dp13-24.pdf).
The current placement near the later work by Polisson, Quah, and Renou makes it
easy to misattribute the screenshot. The source history should be explicit.

The rebuild preserves all 16 fractions and percentages. `EU*` must be defined
in the immediately preceding text or table note; the screenshot alone does not
make that notation self-contained.

**Proposed caption:** “Share of 47 subjects passing each
revealed-preference test after dropping up to three observations. Source:
Polisson and Quah (2013, Table 1).”

### 5. Holt--Laury distribution of safe choices

The primary source is Charles A. Holt and Susan K. Laury, “Risk Aversion and
Incentive Effects,” *American Economic Review* 92(5), 1644--1655
([DOI](https://doi.org/10.1257/000282802762024700)). Rechecking the original
article's Table 3 revealed a substantive error in the legacy screenshot and the
first reconstruction: the final columns are probability distributions over a
respondent's **total number of safe (Option A) choices across the ten-decision
task**. They are not proportions choosing Option B in each decision. Each of
the two displayed columns therefore sums to one.

The corrected rebuild is an exact subset of Table 3. It contains the nine
safe-choice categories (0--1, 2, ..., 8, 9--10), their CRRA intervals under
$U(x)=x^{1-r}/(1-r)$, the low-real ($\times1$) distribution, and the real
$\times20$ distribution. The low-real column averages the first and second
low-real decisions, as in the article's footnote. The omitted $\times20$
hypothetical column and verbal risk classifications can be restored later if
the exposition needs them.

The lottery pairs and probabilities belong to the experiment's Table 1. If the
book needs the price-list instrument itself, Table 1 should be recreated as a
separate native table; its rows must not be grafted onto Table 3's distribution
columns. The screenshot's immediate secondary source remains unknown, so the
new table cites the primary article rather than the image.

The final text should distinguish **eliciting risk attitudes** from assuming
risk aversion: early switching can represent risk-seeking preferences, and a
non-monotone response pattern receives its own category.

**Proposed caption:** “Distribution of the number of safe choices in the
Holt--Laury task. Entries in the final two columns are proportions of observed
choice patterns classified by the total number of Option A choices under low
real ($\times1$) and real $\times20$ payoffs. The low-real column averages the
first and second low-real decisions. Source: Holt and Laury (2002, Table 3).”

## Unreferenced tracked legacy assets

These files are not included anywhere in the authoritative LyX manuscript.
“Archive privately” means remove them from the public book tree after retaining
a recoverable copy in a rights-restricted project archive; it does not mean
destroy the only copy.

| Asset | What it contains / technical finding | Provenance and rights | TikZ/native feasibility | Recommendation |
|---|---|---|---|---|
| `COUNTEREXAMPLE.pdf` | One 574×226 RGB bitmap placed on a 2160×824 pt page; only **19×20 ppi** at placement size; no text fonts. Diagram meaning is not self-documenting. | Unknown. | High only after the intended mathematical construction and labels are identified; exact recovery is impossible from this file alone. | **Archive privately; remove from public tree.** Write a reconstruction specification when the associated proposition is located. |
| `ExtremenessREU.png` | 2153×1558 RGBA diagram at 96-dpi metadata: parallel blue lines, crossing gray lines, circled points, “Max,” and question-mark arrows. Pixel count is adequate for review, but line/text treatment is not publication quality. | Unknown; appears locally annotated, but no source record exists. | High after the intended objects, inequalities, and extrema are stated formally. | **Archive privately.** Rebuild only if the concept re-enters the manuscript; do not reverse-engineer missing mathematics from the drawing. |
| `MGWfig4c1_violationsofWA.pdf` | Letter page containing a 496×668 one-bit CCITT image at about **61 ppi**, plus unembedded Courier. It is a scan-like labeled diagram with sets A--G and price/wealth labels. Filename likely transposes “MWG” as “MGW.” | Strong signs of a textbook scan; no permission record. | Conceptually redrawable, but only from an original exposition and new pedagogical design, not by tracing. | **Remove from public tree and archive privately.** Cite Mas-Colell, Whinston, and Green in any new exposition. |
| `MWGfig2f1WARP.pdf` | Letter page containing a 625×739 one-bit CCITT image at **150 ppi**, plus unembedded Courier; rotated/scan-like Figure 2.F.1. | Strong signs of a copyrighted textbook scan; no permission record. | High as a fresh WARP diagram once the surrounding argument fixes bundles, budgets, and arrows. | **Remove from public tree and archive privately.** Do not publish the scan. |
| `OfferCurves.emf` | Windows Enhanced Metafile, 419,488 bytes; duplicate-content source container for the two-panel “Traditional agent / Sparse agent” offer-curve graphic. EMF is poorly portable in a modern LaTeX toolchain. | Unknown; no equations, notebook, or license linked. | High with the generating demand/offer-curve equations or original code; not faithfully recoverable from appearance alone. | **Retain privately as a forensic source** until equations/code are found; exclude from production assets. |
| `OfferCurves.pdf` | A 446×235 RGB bitmap wrapped in a 245×129 pt PDF, approximately **131 ppi**. It is not a vector alternative to the EMF. | Same unknown status as the EMF. | Source-data-gated as above. | **Remove from public production tree.** Rebuild with PGFPlots only after recovering the model and parameter values. |
| `SAM.emf` | Windows Enhanced Metafile, 993,048 bytes, containing a numerical social-accounting/material-balances table. | Unknown; title visible, but no author, publication, or license record. | Better as a native, accessible table than as TikZ artwork. Exact numerical re-entry is feasible after source checking. | **Archive privately pending provenance.** If used, verify every cell and recreate as a LyX table with a source note. |
| `SMD.pdf` | Letter page containing a 558×632 one-bit CCITT image at about **66 ppi**, plus unembedded Courier; rotated scan-like equilibrium/SMD diagram. | Likely a literature or textbook scan; no permission record. | A fresh conceptual equilibrium diagram is feasible after the theorem/exposition fixes its semantics. | **Remove from public tree and archive privately.** Redraw rather than trace if later required. |
| `separatinghyperplanes.png` | 609×236 RGB at 96-dpi metadata; a two-panel strong-separation/nonseparation diagram with typeset-looking labels. | Unknown and visually scan-like. | High after the two set configurations and claims are formally specified. | **Archive privately pending provenance.** If restored, create an original TikZ diagram tied to the separation theorem's notation. |

## Ignored EPS conversion products

The following eleven files are present in the working directory but ignored by
Git: `CCEI_Afriat_index.eps`, `COUNTEREXAMPLE.eps`, `ExtremenessREU.eps`,
`MGWfig4c1_violationsofWA.eps`, `OfferCurves.eps`, `SMD.eps`, `fosd.eps`,
`holt_laury.eps`, `polissonquah_passingrates_table_expectedutility.eps`,
`rationality_experiment.eps`, and `separatinghyperplanes.eps`.

All identify ImageMagick as creator and encapsulate raster content. They provide
no resolution, editability, accessibility, or rights advantage. They should be
treated as disposable LyX/conversion cache and deleted by an eventual clean
step, never promoted to source assets. No EPS counterpart is currently present
for `MWGfig2f1WARP.pdf` or `SAM.emf`.

## Reproducible vector workspace

Authoritative figure sources are in `figures_tikz/src/`, with shared styling in
`figures_tikz/figure_style.tex`. Source-derived coordinates are committed as
CSV files under `figures_tikz/data/`. The Quah extractor in
`figures_tikz/tools/extract_quah_vector_data.py`:

1. rejects any source PDF whose SHA-256 digest differs from the audited copy;
2. extracts the relevant vector pages with `pdftocairo`;
3. asserts exactly 50 budgets and 50 choices for Subject 216;
4. validates the choice/budget pairing geometrically; and
5. asserts the expected observed and simulated CCEI path structure.

Run the full build and QA from the repository root:

```sh
./figures_tikz/build_and_check.sh
```

Passing PDFs are exported to `notes/figures/tikz/`. Auxiliary files, logs, and
180-dpi visual-review PNGs remain in the ignored `figures_tikz/build/`
directory.

### Current automated QA evidence

| Export | Pages | Fonts | Type 3 | Unembedded | Raster image objects | Result |
|---|---:|---:|---:|---:|---:|---|
| `ccei_afriat_index.pdf` | 1 | 3 | 0 | 0 | 0 | PASS |
| `fosd.pdf` | 1 | 4 | 0 | 0 | 0 | PASS |
| `holt_laury.pdf` | 1 | 7 | 0 | 0 | 0 | PASS |
| `passing_rates_expected_utility.pdf` | 1 | 2 | 0 | 0 | 0 | PASS |
| `rationality_experiment.pdf` | 1 | 3 | 0 | 0 | 0 | PASS |

All five 180-dpi QA renders were also inspected for clipping, collisions,
legibility, tick/legend correctness, and table-rule alignment.

## Remaining publication actions

1. Resolve or document rights for the two Quah-derived plots. If commercial
   permission is unavailable, rebuild from licensed/raw experiment data.
2. For a press edition, consider replacing the two vector table figures with
   native LyX tables for tagged accessibility. Their current text remains
   selectable and the checked vector exports are suitable for the classroom
   edition.
3. Maintain a release-level figure register with creator, source,
   license/permission, data/code provenance, alt text, caption, and the theorem
   or proposition supported by each item.
