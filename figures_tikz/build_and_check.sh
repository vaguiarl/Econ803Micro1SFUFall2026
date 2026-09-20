#!/usr/bin/env bash
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")" && pwd)"
SOURCE_DIR="${ROOT_DIR}/src"
BUILD_DIR="${ROOT_DIR}/build"
QA_DIR="${BUILD_DIR}/qa"
DELIVERY_DIR="${ROOT_DIR}/../notes/figures/tikz"

find_poppler_tool() {
  local tool_name="$1"
  local direct_path
  direct_path="$(command -v "${tool_name}" 2>/dev/null || true)"
  if [[ -n "${direct_path}" ]]; then
    printf '%s\n' "${direct_path}"
    return
  fi
  if [[ -n "${POPPLER_BIN:-}" && -x "${POPPLER_BIN}/${tool_name}" ]]; then
    printf '%s\n' "${POPPLER_BIN}/${tool_name}"
    return
  fi
  local pdfinfo_path proxy_dir candidate
  pdfinfo_path="$(command -v pdfinfo 2>/dev/null || true)"
  if [[ -n "${pdfinfo_path}" ]]; then
    proxy_dir="$(cd "$(dirname "${pdfinfo_path}")" && pwd)"
    candidate="${proxy_dir}/../../native/poppler/poppler/bin/${tool_name}"
    if [[ -x "${candidate}" ]]; then
      printf '%s\n' "${candidate}"
      return
    fi
  fi
  printf 'Required tool not found: %s (set POPPLER_BIN if needed)\n' "${tool_name}" >&2
  return 1
}

LATEXMK="${LATEXMK:-$(command -v latexmk)}"
PDFINFO="$(find_poppler_tool pdfinfo)"
PDFFONTS="$(find_poppler_tool pdffonts)"
PDFIMAGES="$(find_poppler_tool pdfimages)"
PDFTOPPM="$(find_poppler_tool pdftoppm)"

mkdir -p "${BUILD_DIR}" "${QA_DIR}" "${DELIVERY_DIR}"
printf 'figure\tpages\tfonts\ttype3\tunembedded\traster_images\tstatus\n' > "${BUILD_DIR}/checks.tsv"

status=0
for source in "${SOURCE_DIR}"/*.tex; do
  name="$(basename "${source}" .tex)"
  figure_epoch="${SOURCE_DATE_EPOCH:-$(git -C "${ROOT_DIR}/.." log -1 --format=%ct -- "figures_tikz/src/${name}.tex")}"
  if [[ -z "${figure_epoch}" ]]; then
    figure_epoch=0
  fi
  (
    cd "${SOURCE_DIR}"
    export SOURCE_DATE_EPOCH="${figure_epoch}"
    export FORCE_SOURCE_DATE=1
    "${LATEXMK}" -g -pdf -silent -interaction=nonstopmode -halt-on-error -outdir="${BUILD_DIR}" "${name}.tex"
  )
  pdf="${BUILD_DIR}/${name}.pdf"
  pages="$(${PDFINFO} "${pdf}" | awk '/^Pages:/ {print $2}')"
  font_rows="$(${PDFFONTS} "${pdf}" | awk 'NR > 2 && NF {count++} END {print count+0}')"
  type3="$(${PDFFONTS} "${pdf}" | awk 'NR > 2 && $2 == "Type" && $3 == "3" {count++} END {print count+0}')"
  unembedded="$(${PDFFONTS} "${pdf}" | awk 'NR > 2 && $5 == "no" {count++} END {print count+0}')"
  raster_images="$(${PDFIMAGES} -list "${pdf}" | awk 'NR > 2 && $1 ~ /^[0-9]+$/ {count++} END {print count+0}')"
  figure_status="PASS"
  if [[ "${pages}" != "1" || "${type3}" != "0" || "${unembedded}" != "0" || "${raster_images}" != "0" ]]; then
    figure_status="FAIL"
    status=1
  fi
  printf '%s\t%s\t%s\t%s\t%s\t%s\t%s\n' \
    "${name}" "${pages}" "${font_rows}" "${type3}" "${unembedded}" "${raster_images}" "${figure_status}" \
    >> "${BUILD_DIR}/checks.tsv"
  if [[ "${figure_status}" == "PASS" ]]; then
    cp "${pdf}" "${DELIVERY_DIR}/${name}.pdf"
  fi
  "${PDFTOPPM}" -png -r 180 -f 1 -l 1 -singlefile "${pdf}" "${QA_DIR}/${name}" >/dev/null
done

cat "${BUILD_DIR}/checks.tsv"
exit "${status}"
