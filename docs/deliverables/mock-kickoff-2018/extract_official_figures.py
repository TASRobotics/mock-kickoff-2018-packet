#!/usr/bin/env python3
"""Extract embedded diagram JPEGs from the official 2018 FRC manual PDF."""
from __future__ import annotations

from pathlib import Path

import pymupdf

PDF = Path("/tmp/frc2018-manual-analysis/2018FRCGameSeasonManual.pdf")
OUT = Path(__file__).parent / "figures" / "official"
OUT.mkdir(parents=True, exist_ok=True)

# 1-based PDF page → output stem (matches packet figure references)
FIGURE_PAGES: dict[str, int] = {
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

MIN_W, MIN_H = 350, 175


def diagram_images(page: pymupdf.Page) -> list[dict]:
    cands: list[dict] = []
    for info in page.get_image_info(xrefs=True):
        w, h = info["width"], info["height"]
        if w < MIN_W or h < MIN_H:
            continue
        if w > 1100 and h < 120:
            continue
        cands.append(info)
    cands.sort(key=lambda i: i["width"] * i["height"], reverse=True)
    return cands


def save_xref(doc: pymupdf.Document, xref: int, path: Path) -> None:
    blob = doc.extract_image(xref)
    ext = blob["ext"]
    data = blob["image"]
    if ext in ("jpeg", "jpg"):
        path = path.with_suffix(".jpg")
    elif ext == "png":
        path = path.with_suffix(".png")
    else:
        path = path.with_suffix(f".{ext}")
    path.write_bytes(data)
    print(path.name, len(data), ext, f"{blob.get('width')}x{blob.get('height')}")


def main() -> None:
    doc = pymupdf.open(PDF)
    for name, pno in FIGURE_PAGES.items():
        page = doc[pno - 1]
        cands = diagram_images(page)
        if not cands:
            print("WARN no image", name, "page", pno)
            continue
        save_xref(doc, cands[0]["xref"], OUT / name)
        if len(cands) > 1 and cands[1]["width"] * cands[1]["height"] > MIN_W * MIN_H * 2:
            save_xref(doc, cands[1]["xref"], OUT / f"{name}-detail")
    doc.close()


if __name__ == "__main__":
    main()
