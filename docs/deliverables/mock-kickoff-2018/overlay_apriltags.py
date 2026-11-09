#!/usr/bin/env python3
"""Draw TAS fiction AprilTag markers on official manual JPEGs (classroom only)."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch
import numpy as np
from PIL import Image

ROOT = Path(__file__).parent
OFFICIAL = ROOT / "figures" / "official"
OUT = ROOT / "figures" / "tagged"
OUT.mkdir(parents=True, exist_ok=True)

WARN = "#8b0000"
TAG_FIXED = "#bdbdbd"
TAG_MOVE = "#ffe082"
TAG_EDGE = "#212121"
ARROW = "#c62828"


def save_fig(fig, name: str) -> Path:
    path = OUT / name
    fig.savefig(path, dpi=150, bbox_inches="tight", pad_inches=0.02, facecolor="white")
    plt.close(fig)
    print("wrote", path)
    return path


def tag_patch(ax, x, y, tid: int, movable: bool, size: float = 22):
    fc = TAG_MOVE if movable else TAG_FIXED
    ax.add_patch(
        FancyBboxPatch(
            (x - size / 2, y - size / 2),
            size,
            size,
            boxstyle="round,pad=0.15",
            fc=fc,
            ec=TAG_EDGE,
            lw=0.8,
            zorder=5,
        )
    )
    ax.text(x, y, str(tid), ha="center", va="center", fontsize=5.5, fontweight="bold", zorder=6)


def leader(ax, x1, y1, x2, y2):
    ax.add_patch(
        FancyArrowPatch(
            (x1, y1),
            (x2, y2),
            arrowstyle="-|>",
            mutation_scale=8,
            lw=0.9,
            color=ARROW,
            zorder=4,
        )
    )


def load_ax(path: Path):
    img = Image.open(path)
    w, h = img.size
    fig, ax = plt.subplots(figsize=(w / 100, h / 100), dpi=100)
    ax.imshow(np.asarray(img))
    ax.set_xlim(0, w)
    ax.set_ylim(h, 0)
    ax.axis("off")
    return fig, ax, w, h


def xy(w: int, h: int, fx: float, fy: float) -> tuple[float, float]:
    return fx * w, fy * h


def field_topdown_arrows():
    src = OFFICIAL / "figure-3-2-zones.jpg"
    if not src.exists():
        src = OFFICIAL / "figure-3-2-zones.png"
    fig, ax, w, h = load_ax(src)
    ax.text(
        w / 2,
        14,
        "TAS FICTION AprilTags (36h11) on official zones drawing — not on any 2018 field",
        ha="center",
        fontsize=8,
        color=WARN,
        fontweight="bold",
    )

    # (id, x_frac, y_frac, movable)
    tags = []
    cx, cys_b, cys_r, cys_s = 0.50, 0.76, 0.24, 0.50
    offsets = [(-0.04, -0.03), (0.04, -0.03), (-0.04, 0.03), (0.04, 0.03), (-0.07, -0.04), (0.07, -0.04), (-0.07, 0.04), (0.07, 0.04)]
    for i, (dx, dy) in enumerate(offsets):
        tags.append((i + 1, cx + dx, cys_b + dy, i < 4))
    for i, (dx, dy) in enumerate(offsets):
        tags.append((9 + i, cx + dx, cys_r + dy, i < 4))
    soff = [(-0.05, 0.02), (0.05, 0.02), (-0.08, 0.02), (0.08, 0.02), (-0.05, -0.02), (0.05, -0.02), (-0.08, -0.02), (0.08, -0.02)]
    for i, (dx, dy) in enumerate(soff):
        tags.append((17 + i, cx + dx, cys_s + dy, True))
    for tid, fx, fy, mv in [(25, 0.47, 0.46, False), (26, 0.53, 0.46, False), (27, 0.47, 0.54, False), (28, 0.53, 0.54, False)]:
        tags.append((tid, fx, fy, mv))
    tags += [(29, 0.18, 0.88, False), (30, 0.32, 0.88, False), (31, 0.18, 0.12, False), (32, 0.32, 0.12, False)]

    for tid, fx, fy, mv in tags:
        x, y = xy(w, h, fx, fy)
        tag_patch(ax, x, y, tid, mv, size=16)
        # Short leader from ID callout to tag (keeps all 32 readable on one sheet)
        off = 28 if fx < 0.5 else -28
        lx, ly = x + off, y - 22
        leader(ax, lx, ly, x, y)
        ax.text(
            lx,
            ly,
            str(tid),
            fontsize=5.5,
            ha="center",
            va="center",
            color=ARROW,
            fontweight="bold",
            bbox=dict(boxstyle="round,pad=0.15", fc="white", ec=ARROW, lw=0.4, alpha=0.85),
        )

    leg = [
        mpatches.Patch(fc=TAG_FIXED, ec=TAG_EDGE, label="Fixed (fence / tower / exchange)"),
        mpatches.Patch(fc=TAG_MOVE, ec=TAG_EDGE, label="Moves with PLATE"),
    ]
    ax.legend(handles=leg, loc="lower center", fontsize=6, framealpha=0.9)
    save_fig(fig, "field-topdown-apriltags-on-official.jpg")


def overlay_element(stem: str, out_name: str, tags: list[tuple[int, float, float, bool]], title: str):
    for ext in (".jpg", ".png"):
        src = OFFICIAL / f"{stem}{ext}"
        if src.exists():
            break
    else:
        print("skip", stem, "no source")
        return
    fig, ax, w, h = load_ax(src)
    ax.text(w / 2, 12, title, ha="center", fontsize=7, color=WARN, fontweight="bold")
    for tid, fx, fy, mv in tags:
        x, y = xy(w, h, fx, fy)
        tag_patch(ax, x, y, tid, mv, size=20)
        lx = 12 if fx > 0.35 else w - 12
        ly = y
        leader(ax, lx, ly, x, y)
        ax.text(lx + (-6 if lx < w / 2 else 6), ly, str(tid), fontsize=6, color=ARROW, ha="right" if lx < w / 2 else "left", va="center")
    save_fig(fig, out_name)


def element_overlays():
    overlay_element(
        "figure-3-4-scale",
        "figure-3-4-scale-apriltags.jpg",
        [
            (17, 0.35, 0.55, True),
            (18, 0.65, 0.55, True),
            (19, 0.28, 0.62, True),
            (20, 0.72, 0.62, True),
            (21, 0.35, 0.42, True),
            (22, 0.65, 0.42, True),
            (23, 0.28, 0.38, True),
            (24, 0.72, 0.38, True),
            (25, 0.46, 0.48, False),
            (26, 0.54, 0.48, False),
            (27, 0.46, 0.32, False),
            (28, 0.54, 0.32, False),
        ],
        "Fiction IDs 17–28 on SCALE (not official)",
    )
    overlay_element(
        "figure-3-13-switch",
        "figure-3-13-switch-apriltags.jpg",
        [
            (5, 0.22, 0.58, False),
            (6, 0.38, 0.58, False),
            (7, 0.22, 0.38, False),
            (8, 0.38, 0.38, False),
            (1, 0.55, 0.62, True),
            (2, 0.68, 0.62, True),
            (3, 0.55, 0.42, True),
            (4, 0.68, 0.42, True),
        ],
        "Fiction IDs 1–8 on BLUE SWITCH (mirror for Red 9–16)",
    )
    overlay_element(
        "figure-3-16-fence",
        "figure-3-16-fence-apriltags.jpg",
        [(5, 0.25, 0.55, False), (6, 0.42, 0.50, False), (7, 0.25, 0.35, False), (8, 0.42, 0.40, False)],
        "Fiction fence tags 5–8 (fixed)",
    )
    overlay_element(
        "figure-3-19-exchange",
        "figure-3-19-exchange-apriltags.jpg",
        [(29, 0.38, 0.55, False), (30, 0.62, 0.55, False)],
        "Fiction IDs 29–30 at EXCHANGE (31–32 on Red wall)",
    )
    overlay_element(
        "figure-3-23-vision-targets",
        "figure-3-23-vision-targets-apriltags.jpg",
        [(5, 0.30, 0.45, False), (6, 0.55, 0.45, False), (13, 0.30, 0.70, False)],
        "Fiction tags vs 2018 retro-reflective tape (comparison only)",
    )


def main() -> None:
    field_topdown_arrows()
    element_overlays()
    print("Tagged figures in", OUT)


if __name__ == "__main__":
    main()
