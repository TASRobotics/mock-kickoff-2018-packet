#!/usr/bin/env python3
"""Fail if packet PDF is missing embedded official manual diagrams."""
from __future__ import annotations

import re
import sys
from pathlib import Path

import pymupdf

MIN_W, MIN_H = 350, 150

CAPTION_PATTERNS = [
    r"Figure 2-1",
    r"Figure 3-1",
    r"Figure 3-2",
    r"Figure 3-4",
    r"Figure 3-6",
    r"Figure 3-9",
    r"Figure 3-11",
    r"Figure 3-13",
    r"Figure 3-16",
    r"Figure 3-19",
    r"Figure 3-21",
    r"Figure 3-22",
    r"Figure 3-23",
    r"Figure B-1",
]


def big_images(page: pymupdf.Page) -> list[dict]:
    return [
        i
        for i in page.get_image_info()
        if i["width"] >= MIN_W and i["height"] >= MIN_H
    ]


def main() -> int:
    pdf_path = Path(sys.argv[1] if len(sys.argv) > 1 else "mock-kickoff-2018-packet.pdf")
    doc = pymupdf.open(pdf_path)
    pages = len(doc)
    official_pages = 0
    missing: list[str] = []

    for pat in CAPTION_PATTERNS:
        hit = False
        for i in range(pages):
            text = doc[i].get_text()
            if not re.search(pat, text):
                continue
            if big_images(doc[i]):
                hit = True
                if pat.startswith("Figure 3-") or pat.startswith("Figure 2-"):
                    official_pages += 1
                break
        if not hit:
            missing.append(pat)

    # Count unique official diagram embeds (width >= 600) in §3-ish page band
    official_jpegs = 0
    for i in range(pages):
        text = doc[i].get_text()
        if "Section 3 ARCADE" in text or "Figure 3-" in text or "Figure 2-1" in text:
            for info in big_images(doc[i]):
                if info["width"] >= 600:
                    official_jpegs += 1

    doc.close()

    print(f"verify {pdf_path}: pages={pages} caption_patterns_ok={len(CAPTION_PATTERNS)-len(missing)}/{len(CAPTION_PATTERNS)}")
    print(f"official large embeds (w>=600) on figure pages: {official_jpegs}")

    if missing:
        print("MISSING diagrams for:", ", ".join(missing))
        return 1
    if official_jpegs < 12:
        print("FAIL: too few large official embeds (likely broken build cwd)")
        return 1
    if pdf_path.stat().st_size < 500_000:
        print("FAIL: PDF too small — images probably not embedded")
        return 1
    print("OK")
    return 0


if __name__ == "__main__":
    raise SystemExit(main())
