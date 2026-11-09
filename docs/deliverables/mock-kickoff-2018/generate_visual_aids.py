#!/usr/bin/env python3
"""Generate POWER UP mock kickoff visual aids (PNG). Not to scale for official field drawings."""
from __future__ import annotations

from pathlib import Path

import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from matplotlib.patches import FancyBboxPatch, Rectangle, FancyArrowPatch, Circle

OUT = Path(__file__).parent / "figures"
OUT.mkdir(exist_ok=True)

BLUE = "#004b86"
RED = "#c62828"
YELLOW = "#f9a825"
GRAY = "#9e9e9e"
TAG = "#212121"
WARN = "#8b0000"

# Field inches (nominal 2018): 27 x 54 ft
FW, FH = 27 * 12, 54 * 12
CX = FW / 2


def save(fig, name: str) -> None:
    path = OUT / name
    fig.savefig(path, dpi=160, bbox_inches="tight", facecolor="white")
    plt.close(fig)
    print("wrote", path)


def field_topdown_apriltags():
    fig, ax = plt.subplots(figsize=(11, 14))
    ax.set_aspect("equal")
    ax.set_xlim(-20, FW + 20)
    ax.set_ylim(-20, FH + 20)
    ax.invert_yaxis()
    ax.add_patch(Rectangle((0, 0), FW, FH, fill=False, lw=2, ec=GRAY))
    ax.text(FW / 2, FH + 8, "TOP VIEW — TAS FICTION AprilTags (36h11)", ha="center", fontsize=11, fontweight="bold", color=WARN)
    ax.text(FW / 2, -12, "Field carpet 27 ft × 54 ft (nominal) · Blue alliance below · Not official FIRST drawing", ha="center", fontsize=8)

    # Alliance walls
    ax.add_patch(Rectangle((0, 0), FW, 22, fc=BLUE, alpha=0.12, ec=BLUE, lw=1.5))
    ax.add_patch(Rectangle((0, FH - 22), FW, 22, fc=RED, alpha=0.12, ec=RED, lw=1.5))
    ax.text(8, 10, "BLUE ALLIANCE WALL", fontsize=8, color=BLUE, fontweight="bold")
    ax.text(8, FH - 12, "RED ALLIANCE WALL", fontsize=8, color=RED, fontweight="bold")

    auto_y_b = 10 * 12
    auto_y_r = FH - 10 * 12
    ax.plot([0, FW], [auto_y_b, auto_y_b], "k--", lw=1, alpha=0.6)
    ax.plot([0, FW], [auto_y_r, auto_y_r], "k--", lw=1, alpha=0.6)
    ax.text(FW - 4, auto_y_b, "AUTO LINE", fontsize=7, ha="right")

    def switch(cx, cy, color, label):
        w, d = 12 * 12, 8 * 12
        ax.add_patch(Rectangle((cx - w / 2, cy - d / 2), w, d, fc=color, alpha=0.2, ec=color, lw=2))
        ax.text(cx, cy, label, ha="center", va="center", fontsize=9, fontweight="bold", color=color)

    switch(CX, 14 * 12, BLUE, "BLUE\nSWITCH")
    switch(CX, FH - 14 * 12, RED, "RED\nSWITCH")

    # Scale
    sw, sd = 15 * 12, 10 * 12
    ax.add_patch(Rectangle((CX - sw / 2, FH / 2 - sd / 2), sw, sd, fc=YELLOW, alpha=0.25, ec="#f57f17", lw=2))
    ax.text(CX, FH / 2, "SCALE", ha="center", va="center", fontsize=10, fontweight="bold")

    # Portals (corners)
    for x, y, c in [(36, 80, BLUE), (FW - 36, 80, BLUE), (36, FH - 80, RED), (FW - 36, FH - 80, RED)]:
        ax.add_patch(Rectangle((x - 18, y - 48), 36, 96, fill=False, ec=c, ls=":", lw=1.2))
        ax.text(x, y + 58, "PORTAL", fontsize=6, ha="center", color=c)

    def tag(tx, ty, tid, movable=False):
        fc = "#ffecb3" if movable else "#e0e0e0"
        ax.add_patch(FancyBboxPatch((tx - 10, ty - 10), 20, 20, boxstyle="round,pad=0.2", fc=fc, ec=TAG, lw=0.8))
        ax.text(tx, ty, str(tid), ha="center", va="center", fontsize=6, fontweight="bold")

    # Blue switch tags 1-8
    bsy = 14 * 12
    for i, (dx, dy) in enumerate([(-30, -20), (30, -20), (-30, 20), (30, 20), (-50, -30), (50, -30), (-50, 30), (50, 30)]):
        tag(CX + dx, bsy + dy, i + 1, movable=(i < 4))

    rsy = FH - 14 * 12
    for i, (dx, dy) in enumerate([(-30, -20), (30, -20), (-30, 20), (30, 20), (-50, -30), (50, -30), (-50, 30), (50, 30)]):
        tag(CX + dx, rsy + dy, 9 + i, movable=(i < 4))

    # Scale moving 17-24 around plates; fixed 25-28 on tower
    for i, (dx, dy) in enumerate([(-40, -25), (40, -25), (-70, -25), (70, -25), (-40, 25), (40, 25), (-70, 25), (70, 25)]):
        tag(CX + dx, FH / 2 + dy, 17 + i, movable=True)
    for i, (dy,) in enumerate([( -35,), (35,), (-15,), (15,)]):
        tag(CX, FH / 2 + dy, 25 + i, movable=False)

    # Exchange tags 29-32
    tag(CX - 40, 6 * 12, 29)
    tag(CX + 40, 6 * 12, 30)
    tag(CX - 40, FH - 6 * 12, 31)
    tag(CX + 40, FH - 6 * 12, 32)

    legend = [
        mpatches.Patch(fc="#e0e0e0", ec=TAG, label="Fixed tag (fence / tower / exchange)"),
        mpatches.Patch(fc="#ffecb3", ec=TAG, label="Moves with SWITCH or SCALE plate"),
    ]
    ax.legend(handles=legend, loc="upper right", fontsize=7)
    ax.set_xticks([])
    ax.set_yticks([])
    for sp in ax.spines.values():
        sp.set_visible(False)
    save(fig, "field-topdown-apriltags-fiction.png")


def element_scale():
    fig, ax = plt.subplots(figsize=(10, 6))
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 96)
    ax.set_ylabel("Height above carpet (in.)")
    ax.set_title("SCALE — plate edge heights & RUNG (2018 §3.3, paraphrased)")
    heights = [(48, 56, "Blue OWNERSHIP", BLUE), (56, 64, "Balanced", GRAY), (64, 72, "Red OWNERSHIP", RED)]
    for y0, y1, label, c in heights:
        ax.add_patch(Rectangle((1, y0), 3, y1 - y0, fc=c, alpha=0.35, ec=c))
        ax.text(4.2, (y0 + y1) / 2, label, va="center", fontsize=9)
    ax.axhline(60, ls=":", color="k", lw=1)
    ax.text(5.5, 60.5, "Level start ≈ 60 in. (±1)", fontsize=8)
    ax.plot([7, 7], [0, 84], "k-", lw=3)
    ax.plot([7.3, 9], [84, 84], "k-", lw=4)
    ax.text(7.8, 86, "RUNG top 84 in.", ha="center", fontsize=9)
    ax.add_patch(Rectangle((6.5, 0), 1.5, 12, fc=YELLOW, alpha=0.4))
    ax.text(6.5, -4, "BRICKS", fontsize=8)
    ax.set_xlabel("Schematic (not to scale)")
    save(fig, "element-scale-heights.png")


def element_switch():
    fig, ax = plt.subplots(figsize=(9, 5))
    ax.set_title("SWITCH cross-section (fence 18.75 in. · plate 9 in.)")
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 22)
    ax.plot([1, 9], [0, 0], "k-", lw=2)
    ax.plot([2, 2], [0, 18.75], "k-", lw=4)
    ax.plot([8, 8], [0, 18.75], "k-", lw=4)
    ax.add_patch(Rectangle((2.5, 9), 5, 1.5, fc=BLUE, alpha=0.3))
    ax.annotate("Plate ~9 in.", (5, 9.8), ha="center", fontsize=9)
    ax.annotate("", xy=(8.2, 18.75), xytext=(8.2, 0), arrowprops=dict(arrowstyle="<->", color=RED))
    ax.text(8.6, 9, "18.75 in.\nfence", fontsize=8, color=RED)
    ax.set_ylabel("inches")
    ax.set_xticks([])
    save(fig, "element-switch-crosssection.png")


def element_exchange_portal():
    fig, axes = plt.subplots(1, 2, figsize=(10, 4))
    ax = axes[0]
    ax.set_title("EXCHANGE (robot side)")
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 22)
    ax.add_patch(Rectangle((2, 0), 16, 16.25, fill=False, lw=2))
    ax.text(10, 8, "Lower opening\n16.25 in. tall", ha="center", fontsize=9)
    ax.axhline(20, xmin=0.3, xmax=0.7, color=BLUE, lw=2)
    ax.text(10, 21, "RETURN 20 in. up", ha="center", fontsize=8)

    ax = axes[1]
    ax.set_title("PORTAL (HUMAN PLAYER)")
    ax.set_xlim(0, 20)
    ax.set_ylim(0, 36)
    ax.add_patch(Rectangle((4, 20), 12, 14, fill=False, lw=2))
    ax.text(10, 27, "Feed opening", ha="center", fontsize=9)
    ax.set_ylabel("Height (in.)")
    fig.suptitle("Alliance wall openings (2018 §3.6–3.7)")
    save(fig, "element-exchange-portal.png")


def element_platform():
    fig, ax = plt.subplots(figsize=(8, 4))
    ax.set_title("PLATFORM & ENDGAME climb zone (side view, schematic)")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 90)
    ax.add_patch(Rectangle((2, 0), 6, 3.5, fc="#90caf9", ec=BLUE))
    ax.text(5, 1.2, "PLATFORM 3.5 in.", ha="center", fontsize=8)
    ax.plot([5, 5], [3.5, 84], "k--", lw=1)
    ax.plot([4.5, 5.5], [84, 84], "k-", lw=3)
    ax.text(6.2, 84, "RUNG", fontsize=9)
    ax.annotate("G05 16 in. reach\nexempt if fully\nin PLATFORM ZONE", (7, 40), fontsize=8, color=BLUE)
    ax.set_ylabel("in. above carpet")
    save(fig, "element-platform-rung.png")


def element_cube():
    fig = plt.figure(figsize=(6, 4))
    ax = fig.add_subplot(111, projection="3d")
    ax.bar3d(0, 0, 0, 13, 13, 11, color=YELLOW, alpha=0.85, edgecolor="#f57f17")
    ax.set_title("POWER CUBE 13 × 13 × 11 in. (~3¼ lb)")
    ax.set_xlabel("in.")
    ax.set_ylabel("in.")
    ax.set_zlabel("in.")
    save(fig, "element-power-cube.png")


def overview_elements():
    fig, ax = plt.subplots(figsize=(12, 5))
    ax.axis("off")
    items = [
        ("SWITCH", "Per-alliance tilt plates\nOwnership 3–6 in. plate edge\nFence 18.75 in."),
        ("SCALE", "Shared center seesaw\nPlate edges 48–72 in.\nRUNG climb 84 in."),
        ("VAULT / POWER UPS", "Human loads cubes\nFORCE · BOOST · LEVITATE"),
        ("EXCHANGE", "Robot ↔ human cube pass\n16.25 in. lower opening"),
        ("PORTAL", "Corner cube feeder\nOpening ~20–34 in."),
        ("PLATFORM", "Park 5 pts / climb prep\n3.5 in. ramps"),
    ]
    for i, (title, body) in enumerate(items):
        x = (i % 3) * 4 + 0.3
        y = 0.55 if i < 3 else 0.05
        ax.add_patch(FancyBboxPatch((x, y), 3.6, 0.38, boxstyle="round,pad=0.02", fc="#f5f5f5", ec=BLUE))
        ax.text(x + 0.15, y + 0.28, title, fontsize=11, fontweight="bold", color=BLUE)
        ax.text(x + 0.15, y + 0.08, body, fontsize=8, va="bottom")
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 1)
    ax.set_title("FIRST POWER UP — game elements at a glance (TAS mock)", fontsize=12, fontweight="bold", pad=12)
    save(fig, "elements-overview.png")


def main():
    field_topdown_apriltags()
    overview_elements()
    element_scale()
    element_switch()
    element_exchange_portal()
    element_platform()
    element_cube()
    print("All figures in", OUT)


if __name__ == "__main__":
    main()
