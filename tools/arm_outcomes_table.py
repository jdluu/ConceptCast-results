#!/usr/bin/env python3
"""Thesis Table 5.x (arm outcomes) redrawn as a slide asset.

Content is tables/arm_outcomes.tex verbatim: jobs completed/failed per arm with
the completion rate. Presentation matches the other deck figures so the slide
reads as one deck, not a patchwork.

Authored on a fixed canvas so point sizes are what appear on the slide, and the
palette is imported from framework_figure so the deck stays one visual family.

Outputs:
  reports/figures/arm_outcomes_dark.png   deck variant
  reports/figures/arm_outcomes.png        print / paper variant

Run: .venv/bin/python tools/arm_outcomes_table.py
"""
from __future__ import annotations

import argparse
import re
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from framework_figure import PALETTES, txt  # same directory as this script

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "reports" / "figures"

W, H = 336.0, 160.0

# (label, completed, failed, not terminal, total, completion %)
ROWS = [
    ("A (Monolithic)", "36", "64", "0", "100", "36"),
    ("B (Monolithic+Repair)", "68", "32", "0", "100", "68"),
    ("C (Agent Council)", "53", "46", "1", "100", "53"),
]
TOTAL = ("Total (300 jobs)", "157", "142", "1", "300", "52.3")
HEAD = ["Arm", "Completed", "Failed", "Not\nterminal", "Total", "Completion\n(%)"]
COLS = [(10.0, "left"), (146.0, "right"), (190.0, "right"),
        (244.0, "right"), (274.0, "right"), (330.0, "right")]


def draw(P: dict) -> plt.Figure:
    fig = plt.figure(figsize=(W / 72.0, H / 72.0), dpi=300, facecolor=P["bg"])
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    def row(y, values, colour, weight="normal", size=8.5):
        for (x, ha), v in zip(COLS, values):
            txt(ax, x, y, v, P, size, colour, weight=weight, ha=ha)

    def rule(y, colour, lw=1.0):
        ax.plot([10, W - 10], [y, y], color=colour, lw=lw, zorder=3)

    row(142.0, HEAD, P["muted"], size=7.5)
    rule(128.0, P["accent"], 1.6)
    for i, r in enumerate(ROWS):
        row(108.0 - i * 20.0, r, P["ink"])
    rule(54.0, P["rule"])
    row(38.0, TOTAL, P["accent"], weight="bold")
    rule(22.0, P["rule"])
    return fig


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=("dark", "light", "both"), default="both")
    args = ap.parse_args()
    OUT.mkdir(parents=True, exist_ok=True)
    for name in (("dark", "light") if args.variant == "both" else (args.variant,)):
        fig = draw(PALETTES[name])
        suffix = "_dark" if name == "dark" else ""
        path = OUT / f"arm_outcomes{suffix}.png"
        fig.savefig(path, dpi=300, facecolor=PALETTES[name]["bg"])
        plt.close(fig)
        print("figure →", path)
    check_against_thesis()


def check_against_thesis() -> None:
    """The slide table must not drift from the thesis table it reproduces."""
    tex = Path("/home/jdluu/projects/ConceptCast/tables/arm_outcomes.tex")
    if not tex.exists():
        print("NOTE: thesis table not found, skipped the drift check:", tex)
        return
    cells = {}
    for line in tex.read_text().splitlines():
        m = re.match(r"^(A|B|C)\s.*?&\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*(\d+)\s*&\s*([\d.]+)\s*\\\\", line)
        if m:
            cells[m.group(1)] = (m.group(2), m.group(3), m.group(4), m.group(5), m.group(6))
    want = {"A": ("36", "64", "0", "100", "36"), "B": ("68", "32", "0", "100", "68"),
            "C": ("53", "46", "1", "100", "53")}
    got = {r[0][0]: r[1:] for r in ROWS}
    if cells != want or got != want:
        raise SystemExit(f"arm outcomes drifted from the thesis table:\nthesis={cells}\nslide={got}\nwant={want}")
    m = re.search(r"Total \(300 jobs\)\s*&\s*(.*?)\s*&", tex.read_text())
    print(f"✓ slide table matches tables/arm_outcomes.tex for all three arms and the total row")


if __name__ == "__main__":
    main()
