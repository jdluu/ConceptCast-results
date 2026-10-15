#!/usr/bin/env python3
"""Whole-framework overview figure: the three agents, the Global Context Object,
and the deterministic verification and repair loop.

This complements `reports/figures/architecture.{png,_dark.png}`, which zooms in
on the Animator's code-stage boundary only. This figure is the frame that
contains it.

Layout is authored on a fixed 620 x 196 pt canvas, which is exactly the area the
defense deck gives a figure, so the point sizes written here are the point sizes
that appear on the slide. Nothing is scaled at display time, and no loop arrow
carries a floating label: each loop's meaning lives in the panel it belongs to,
which is what keeps a canvas this small readable.

Outputs:
  reports/figures/framework_overview_dark.png   dark ground, for the deck
  reports/figures/framework_overview.png        light ground, for print / paper

Run: .venv/bin/python tools/framework_figure.py
"""
from __future__ import annotations

import argparse
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
from matplotlib.patches import FancyArrowPatch, FancyBboxPatch  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "reports" / "figures"

W, H = 620.0, 196.0          # pt; matches the deck's figure area 1:1
FONT = "DejaVu Serif"

PALETTES = {
    "dark": {
        "bg": "#0C0F13", "panel": "#171E26", "ink": "#E7EAEE", "muted": "#98A2B0",
        "rule": "#38424E", "accent": "#3FA796", "warn": "#E5A54B", "faint": "#141A21",
    },
    "light": {
        "bg": "#FFFFFF", "panel": "#F4F6F8", "ink": "#12181F", "muted": "#5C6673",
        "rule": "#AEB8C2", "accent": "#2E7D6B", "warn": "#B0740F", "faint": "#EDF1F4",
    },
}

DASH = (0, (2.6, 2.2))


def rbox(ax, x, y, w, h, P, edge=None, fill=None, lw=1.3, dashed=False, r=5.0):
    ax.add_patch(FancyBboxPatch(
        (x, y), w, h, boxstyle=f"round,pad=0,rounding_size={r}",
        linewidth=lw, edgecolor=edge or P["rule"], facecolor=fill or P["panel"],
        linestyle=(0, (3.2, 2.2)) if dashed else "solid", zorder=2,
    ))


def txt(ax, x, y, s, P, size=8.0, color=None, weight="normal", ha="center",
        va="center", z=5):
    ax.text(x, y, s, ha=ha, va=va, fontsize=size, color=color or P["ink"],
            fontweight=weight, family=FONT, zorder=z)


def arrow(ax, p1, p2, P, color=None, dashed=False, lw=1.2, rad=0.0, ms=7.5,
          both=False):
    ax.add_patch(FancyArrowPatch(
        p1, p2, arrowstyle="<|-|>" if both else "-|>", mutation_scale=ms,
        linewidth=lw, color=color or P["muted"],
        linestyle=DASH if dashed else "solid",
        connectionstyle=f"arc3,rad={rad}", shrinkA=0, shrinkB=0, zorder=3,
    ))


def line(ax, p1, p2, P, color, dashed=True, lw=1.1):
    ax.plot([p1[0], p2[0]], [p1[1], p2[1]], color=color, lw=lw,
            linestyle=DASH if dashed else "solid", solid_capstyle="butt", zorder=3)


def draw(P: dict) -> plt.Figure:
    fig = plt.figure(figsize=(W / 72.0, H / 72.0), dpi=300, facecolor=P["bg"])
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    # ---- pipeline row ----------------------------------------------------
    PY, PH = 104.0, 48.0
    nodes = [                       # (x, w, label, sub, is_input)
        (8.0, 88.0, "Topic", None, True),
        (116.0, 106.0, "Analyst", "writes the plan", False),
        (242.0, 122.0, "Architect", "writes the storyboard", False),
        (384.0, 106.0, "Animator", "one call per scene", False),
        (510.0, 102.0, "Assemble", "then render to video", False),
    ]
    spans = []
    for x, w, label, sub, is_in in nodes:
        rbox(ax, x, PY, w, PH, P, edge=P["rule"] if is_in else P["accent"],
             dashed=is_in, fill=P["faint"] if is_in else None)
        cx, cy = x + w / 2.0, PY + PH / 2.0
        spans.append((x, w))
        txt(ax, cx, cy + 6.5, label, P, 9.8, P["muted"] if is_in else P["ink"])
        if sub:
            txt(ax, cx, cy - 8.5, sub, P, 6.5, P["muted"])
    for (x1, w1), (x2, _) in zip(spans, spans[1:]):
        arrow(ax, (x1 + w1, PY + PH / 2.0), (x2, PY + PH / 2.0), P, lw=1.1)

    # ---- Global Context Object ------------------------------------------
    gx, gw, gy, gh = 116.0, 374.0, 164.0, 26.0
    rbox(ax, gx, gy, gw, gh, P, edge=P["accent"], fill=P["faint"], lw=1.5)
    txt(ax, gx + gw / 2, gy + gh / 2,
        "Global Context Object  \u00b7  one validated record, injected per phase",
        P, 8.2)
    for x, w in spans[1:4]:
        cx = x + w / 2.0
        arrow(ax, (cx, gy), (cx, PY + PH), P, color=P["accent"], lw=1.0, ms=5.0,
              both=True)

    # ---- deterministic checks (scene loop, back to the Animator) --------
    bx, by, bw, bh = 8.0, 12.0, 438.0, 80.0
    rbox(ax, bx, by, bw, bh, P, edge=P["warn"], fill=P["faint"], lw=1.3,
         dashed=True, r=6)
    txt(ax, 28.0, 76.0, "Deterministic checks", P, 7.8, P["warn"], ha="left")
    txt(ax, 28.0, 64.0, "no model in the loop", P, 6.8, P["muted"], ha="left")
    for i, s in enumerate((
        "structure, safety, and API",
        "layout and collision",
        "the scene renders on its own",
    )):
        txt(ax, 168.0, 76.0 - i * 12.0, "\u00b7 " + s, P, 7.0, P["ink"], ha="left")
    txt(ax, 318.0, 76.0, "a failure regenerates", P, 6.8, P["warn"], ha="left")
    txt(ax, 318.0, 64.0, "that scene, not the rest", P, 6.8, P["warn"], ha="left")
    arrow(ax, (437.0, by + bh), (437.0, PY), P, color=P["warn"], dashed=True, lw=1.1)

    # ---- program-level repair (back to Assemble) ------------------------
    line(ax, (602.0, PY), (602.0, 76.0), P, P["warn"])
    line(ax, (602.0, 76.0), (518.0, 76.0), P, P["warn"])
    arrow(ax, (518.0, 76.0), (518.0, PY), P, color=P["warn"], dashed=True, lw=1.1)
    txt(ax, 560.0, 62.0, "program-level repair", P, 7.2, P["warn"])
    txt(ax, 560.0, 50.0, "the code is patched,", P, 6.8, P["muted"])
    txt(ax, 560.0, 40.0, "not rewritten", P, 6.8, P["muted"])

    return fig


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=("dark", "light", "both"), default="both")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    for name in (("dark", "light") if args.variant == "both" else (args.variant,)):
        fig = draw(PALETTES[name])
        suffix = "_dark" if name == "dark" else ""
        path = OUT / f"framework_overview{suffix}.png"
        fig.savefig(path, dpi=300, facecolor=PALETTES[name]["bg"])
        plt.close(fig)
        print("figure →", path)


if __name__ == "__main__":
    main()
