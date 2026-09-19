# Publication figure sources

This directory contains the reproducible, resolution-independent sources for
all five graphics included by the authoritative LyX manuscript. The former
raster assets have been replaced in the current manuscript and removed from
the release tree; they remain recoverable from repository history.

## Build

From this directory, run:

```sh
./build_and_check.sh
```

The script compiles every file in `src/`, checks that each output is a
single-page vector PDF with embedded non-Type-3 fonts and no raster image
objects.  It exports only passing PDFs to the tracked, LyX-ready directory
`../notes/figures/tikz/` and renders review PNGs into the ignored `build/qa/`
directory.  Set `LATEXMK` or `POPPLER_BIN` if those tools are not on `PATH`.

## Source-derived coordinate data

The two Quah figures are rebuilt from coordinates recovered from the vector
source slides, not by tracing the manuscript PNGs.  Given a local copy of the
source PDF, regenerate them with:

```sh
python3 tools/extract_quah_vector_data.py /path/to/survey-qutweb.pdf \
  --pdftocairo /path/to/pdftocairo
```

The extractor accepts only the audited SHA-256 digest and verifies the expected
numbers of budgets, choices, and curve fragments before replacing the CSVs.
See `../FIGURE_AUDIT.md` for provenance, rights status, and the integration
recommendation for each figure.

`holt_laury.pdf` is an exact four-column subset of Holt and Laury (2002,
Table 3): number of safe choices, the implied CRRA interval, the low-real
($\times1$) distribution, and the real $\times20$ distribution. Its last two
columns are distributions over safe-choice totals and each sums to one. The
price-list lotteries belong to the article's Table 1 and are intentionally not
mixed into this Table 3 reconstruction.
