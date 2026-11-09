#!/usr/bin/env python3
"""Render official 2018 FRC manual figure pages from blob PDF (team-use excerpt)."""
from pathlib import Path

import pymupdf

PDF = Path("/tmp/frc2018-manual-analysis/2018FRCGameSeasonManual.pdf")
OUT = Path(__file__).parent / "figures" / "official"
OUT.mkdir(parents=True, exist_ok=True)

# Page numbers 1-based from pymupdf scan (Nov 2026)
FIGURE_PAGES = {
    "figure-2-1-playing-area": 13,
    "figure-3-1-playing-area": 15,
    "figure-3-2-zones": 16,
    "figure-3-4-scale": 18,
    "figure-3-6-scale-motion": 20,
    "figure-3-9-rungs": 22,
    "figure-3-12-platform": 23,
    "figure-3-13-switch": 24,
    "figure-3-16-fence": 26,
    "figure-3-18-alliance-station": 28,
    "figure-3-19-exchange": 29,
    "figure-3-21-portal": 32,
    "figure-3-22-power-cube": 33,
    "figure-3-23-vision-targets": 34,
}

MATRIX = pymupdf.Matrix(2.0, 2.0)  # ~144 dpi
# Clip out footer/header band on Letter manual pages (pts)
CLIP = pymupdf.Rect(54, 54, 558, 720)


def main():
    doc = pymupdf.open(PDF)
    for name, pno in FIGURE_PAGES.items():
        page = doc[pno - 1]
        pix = page.get_pixmap(matrix=MATRIX, clip=CLIP, alpha=False)
        path = OUT / f"{name}.png"
        pix.save(path)
        print(path, pix.width, "x", pix.height)
    doc.close()


if __name__ == "__main__":
    main()
