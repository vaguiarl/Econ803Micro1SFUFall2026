#!/usr/bin/env python3
"""Recover plotted coordinates from Quah's 2015 survey-slide vectors.

This deliberately accepts the source PDF, not the manuscript PNGs.  It checks
the exact source hash, converts only the two relevant PDF pages to SVG with
pdftocairo, and emits auditable CSV coordinates.  The extraction is tied to
the known vector structure and fails loudly if that structure changes.
"""

from __future__ import annotations

import argparse
import csv
import hashlib
import re
import subprocess
import tempfile
import xml.etree.ElementTree as ET
from pathlib import Path


EXPECTED_SHA256 = "f2dea2324abac5624ad3ef23a9a96dc7b805bf1843382d4688cd42d0eae2e1a8"
SVG_NS = "{http://www.w3.org/2000/svg}"
NUMBER = re.compile(r"[-+]?(?:\d+(?:\.\d*)?|\.\d+)(?:[Ee][-+]?\d+)?")


def numbers(path_data: str) -> list[float]:
    return [float(value) for value in NUMBER.findall(path_data)]


def line_endpoints(path_data: str) -> tuple[float, float, float, float]:
    values = numbers(path_data)
    if len(values) != 4:
        raise ValueError(f"Expected one M--L segment, found {len(values)} coordinates")
    return values[0], values[1], values[2], values[3]


def svg_page(pdftocairo: str, pdf: Path, page: int, destination: Path) -> Path:
    prefix = destination / f"quah-page-{page}"
    subprocess.run(
        [pdftocairo, "-svg", "-f", str(page), "-l", str(page), str(pdf), str(prefix)],
        check=True,
    )
    # Poppler versions differ: some append .svg and some write the exact prefix.
    candidates = [prefix, prefix.with_suffix(".svg")]
    for candidate in candidates:
        if candidate.is_file():
            return candidate
    raise FileNotFoundError(f"pdftocairo produced neither {candidates[0]} nor {candidates[1]}")


def write_csv(path: Path, fieldnames: list[str], rows: list[dict[str, object]]) -> None:
    path.parent.mkdir(parents=True, exist_ok=True)
    with path.open("w", newline="", encoding="utf-8") as stream:
        writer = csv.DictWriter(stream, fieldnames=fieldnames, lineterminator="\n")
        writer.writeheader()
        writer.writerows(rows)


def extract_rationality(svg: Path, output_dir: Path) -> None:
    root = ET.parse(svg).getroot()
    x_min, x_max = 486.782314, 4014.776283
    y_min, y_max = 360.428322, 3888.422291

    def scale(x: float, y: float) -> tuple[float, float]:
        return (100 * (x - x_min) / (x_max - x_min), 100 * (y - y_min) / (y_max - y_min))

    budgets: list[dict[str, object]] = []
    for index in range(3, 53):
        clip = f"url(#clip-{index})"
        groups = [group for group in root.iter(SVG_NS + "g") if group.get("clip-path") == clip]
        if len(groups) != 1:
            raise ValueError(f"Expected one group for {clip}; found {len(groups)}")
        paths = list(groups[0].iter(SVG_NS + "path"))
        if len(paths) != 1:
            raise ValueError(f"Expected one budget path for {clip}; found {len(paths)}")
        x0, y0, x1, y1 = line_endpoints(paths[0].get("d", ""))
        sx0, sy0 = scale(x0, y0)
        sx1, sy1 = scale(x1, y1)
        budgets.append(
            {
                "observation": index - 2,
                "x_start": f"{sx0:.6f}",
                "y_start": f"{sy0:.6f}",
                "x_end": f"{sx1:.6f}",
                "y_end": f"{sy1:.6f}",
            }
        )

    points_unscaled: list[tuple[float, float]] = []
    for path in root.iter(SVG_NS + "path"):
        data = path.get("d", "")
        if (
            path.get("stroke") != "rgb(0%, 0%, 0%)"
            or path.get("stroke-width") != "4.99999"
            or not path.get("transform", "").startswith("matrix(0.0398719")
            or data.count(" C ") < 3
        ):
            continue
        values = numbers(data)
        if len(values) % 2:
            continue
        xs, ys = values[0::2], values[1::2]
        cx, cy = (min(xs) + max(xs)) / 2, (min(ys) + max(ys)) / 2
        width, height = max(xs) - min(xs), max(ys) - min(ys)
        if 45 < width < 75 and 45 < height < 75 and x_min - 40 <= cx <= x_max + 40 and y_min - 40 <= cy <= y_max + 40:
            points_unscaled.append((cx, cy))
    if len(points_unscaled) != 50:
        raise ValueError(f"Expected 50 revealed choices; found {len(points_unscaled)}")

    points: list[dict[str, object]] = []
    maximum_residual = 0.0
    for observation, ((px, py), budget) in enumerate(zip(points_unscaled, budgets), start=1):
        sx, sy = scale(px, py)
        x0 = float(budget["x_start"])
        y0 = float(budget["y_start"])
        x1 = float(budget["x_end"])
        y1 = float(budget["y_end"])
        numerator = abs((y1 - y0) * sx - (x1 - x0) * sy + x1 * y0 - y1 * x0)
        denominator = ((y1 - y0) ** 2 + (x1 - x0) ** 2) ** 0.5
        residual = numerator / denominator
        maximum_residual = max(maximum_residual, residual)
        points.append({"observation": observation, "x1": f"{sx:.6f}", "x2": f"{sy:.6f}"})
    if maximum_residual > 0.15:
        raise ValueError(f"Choice/budget ordering check failed; maximum distance is {maximum_residual:.6f}")

    write_csv(
        output_dir / "rationality_budgets.csv",
        ["observation", "x_start", "y_start", "x_end", "y_end"],
        budgets,
    )
    write_csv(output_dir / "rationality_points.csv", ["observation", "x1", "x2"], points)
    print(f"rationality: 50 budgets, 50 choices; max choice-to-budget distance {maximum_residual:.6f}")


def extract_path_pairs(path_data: str) -> list[tuple[float, float]]:
    values = numbers(path_data)
    if len(values) % 2:
        raise ValueError("Odd number of SVG path coordinates")
    return list(zip(values[0::2], values[1::2]))


def extract_ccei(observed_svg: Path, simulated_svg: Path, output_dir: Path) -> None:
    x_min, x_max = 666.813323, 5130.792095
    y_min, y_max = 475.227947, 3996.030925

    def scale(pair: tuple[float, float]) -> tuple[float, float]:
        x, y = pair
        return ((x - x_min) / (x_max - x_min), (y - y_min) / (y_max - y_min))

    observed_root = ET.parse(observed_svg).getroot()
    observed_paths = [
        path
        for path in observed_root.iter(SVG_NS + "path")
        if path.get("stroke") == "rgb(100%, 0%, 0%)" and len(path.get("d", "")) > 100
    ]
    if len(observed_paths) != 1:
        raise ValueError(f"Expected one observed CCEI curve; found {len(observed_paths)}")
    observed = [scale(pair) for pair in extract_path_pairs(observed_paths[0].get("d", ""))]

    simulated_root = ET.parse(simulated_svg).getroot()
    simulated_paths = [
        path
        for path in simulated_root.iter(SVG_NS + "path")
        if path.get("stroke") == "rgb(50%, 50%, 50%)"
        and path.get("stroke-dasharray") == "60"
        and len(path.get("d", "")) > 100
    ]
    if len(simulated_paths) != 14:
        raise ValueError(f"Expected 14 dashed-curve fragments; found {len(simulated_paths)}")
    simulated = [scale(pair) for path in simulated_paths for pair in extract_path_pairs(path.get("d", ""))]
    simulated.sort(key=lambda pair: (pair[0], -pair[1]))

    def in_axes(pair: tuple[float, float]) -> bool:
        x, y = pair
        return -1e-6 <= x <= 1 + 1e-6 and -1e-6 <= y <= 1 + 1e-6

    def deduplicate(points: list[tuple[float, float]]) -> list[tuple[float, float]]:
        result: list[tuple[float, float]] = []
        for point in points:
            point = (min(1.0, max(0.0, point[0])), min(1.0, max(0.0, point[1])))
            if not result or abs(point[0] - result[-1][0]) > 1e-8 or abs(point[1] - result[-1][1]) > 1e-8:
                result.append(point)
        return result

    observed = deduplicate([point for point in observed if in_axes(point)])
    simulated = deduplicate([point for point in simulated if in_axes(point)])
    if len(observed) < 50 or len(simulated) < 200:
        raise ValueError(f"Curve extraction too short: observed={len(observed)}, simulated={len(simulated)}")

    write_csv(
        output_dir / "ccei_observed.csv",
        ["threshold", "share"],
        [{"threshold": f"{x:.6f}", "share": f"{y:.6f}"} for x, y in observed],
    )
    write_csv(
        output_dir / "ccei_simulated.csv",
        ["threshold", "share"],
        [{"threshold": f"{x:.6f}", "share": f"{y:.6f}"} for x, y in simulated],
    )
    print(f"CCEI: {len(observed)} observed vertices, {len(simulated)} simulated vertices")


def main() -> None:
    parser = argparse.ArgumentParser()
    parser.add_argument("source_pdf", type=Path, help="Quah (2015) survey-slide PDF")
    parser.add_argument("--output", type=Path, default=Path(__file__).resolve().parents[1] / "data")
    parser.add_argument("--pdftocairo", default="pdftocairo")
    arguments = parser.parse_args()

    digest = hashlib.sha256(arguments.source_pdf.read_bytes()).hexdigest()
    if digest != EXPECTED_SHA256:
        raise SystemExit(f"Refusing unknown source PDF: expected {EXPECTED_SHA256}, found {digest}")

    with tempfile.TemporaryDirectory(prefix="quah-vector-extract-") as temporary:
        temporary_path = Path(temporary)
        rationality_svg = svg_page(arguments.pdftocairo, arguments.source_pdf, 31, temporary_path)
        observed_svg = svg_page(arguments.pdftocairo, arguments.source_pdf, 46, temporary_path)
        simulated_svg = svg_page(arguments.pdftocairo, arguments.source_pdf, 47, temporary_path)
        extract_rationality(rationality_svg, arguments.output)
        extract_ccei(observed_svg, simulated_svg, arguments.output)

    print(f"source SHA-256 verified: {digest}")


if __name__ == "__main__":
    main()
