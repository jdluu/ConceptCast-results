#!/usr/bin/env python3
"""Framework figures for the ConceptCast defense deck.

Two figures, both authored on a fixed 620 x 196 pt canvas, which is exactly the
area the deck gives a figure. Nothing is scaled at display time, so the point
sizes written here are the point sizes that appear on the slide, and font sizes
are chosen from measured text widths rather than guessed.

  framework_overview  the three agents, the Global Context Object, and the
                      deterministic verification and repair loop: the frame.
  code_stage          the Animator's verification and repair boundary, faithful
                      to figures/architecture.tex in the thesis (same nodes and
                      edges), redrawn so it is legible at slide size. The thesis
                      figure is authored for a 468 pt page and displayed here at
                      357 pt, which put its smallest labels near 5 pt.

No loop arrow carries a floating label. Each loop's meaning lives in the panel
it belongs to, which is what keeps a canvas this small readable.

Outputs:
  reports/figures/framework_overview_dark.png   deck variants
  reports/figures/code_stage_dark.png
  reports/figures/framework_overview.png        print / paper variants
  reports/figures/code_stage.png

Run: .venv/bin/python tools/framework_figure.py [--which overview|code-stage|both]
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
FONT = "DejaVu Sans"      # matches the deck's sans typography and the chart figures

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


def draw_code_stage(P: dict) -> plt.Figure:
    """The Animator's verification and repair boundary, redrawn at slide size.

    Faithful to figures/architecture.tex in the thesis (same nodes, same edges,
    same two loops); what changes is only the presentation, so it is legible at
    the size the deck actually shows it and shares the palette of the overview
    figure. The thesis figure is authored for a 468 pt-wide page and displayed
    here at 357 pt, which put its smallest labels near 5 pt.
    """
    fig = plt.figure(figsize=(W / 72.0, H / 72.0), dpi=300, facecolor=P["bg"])
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    ROW_Y, ROW_H = 124.0, 44.0
    yc = ROW_Y + ROW_H / 2.0

    def node(x, y, w, h, name, sub, edge, size=8.4):
        rbox(ax, x, y, w, h, P, edge=edge, fill=P["faint"] if edge == P["rule"] else None)
        cx, cy = x + w / 2.0, y + h / 2.0
        txt(ax, cx, cy + 5.0, name, P, size)
        if sub:
            txt(ax, cx, cy - 7.5, sub, P, 6.2, P["muted"])

    # --- scene level: generate, check, verify -----------------------------
    node(6.0, ROW_Y, 90.0, ROW_H, "Scene code", "generated per scene", P["rule"])
    node(120.0, ROW_Y, 100.0, ROW_H, "AST sanitizer", "structure and safety", P["accent"])
    node(244.0, ROW_Y, 100.0, ROW_H, "Layout and collision", "reserved boxes", P["accent"])
    node(368.0, ROW_Y, 100.0, ROW_H, "Compile and render", "scene executes", P["accent"])
    node(486.0, ROW_Y, 102.0, ROW_H, "Verified scene", None, P["rule"])

    rbox(ax, 112.0, 114.0, 364.0, 62.0, P, edge=P["warn"], fill=P["faint"],
         lw=1.3, dashed=True, r=6)
    txt(ax, 294.0, 186.0, "Deterministic verification boundary", P, 7.0, P["warn"])

    for x1, x2 in ((96.0, 120.0), (220.0, 244.0), (344.0, 368.0), (468.0, 486.0)):
        arrow(ax, (x1, yc), (x2, yc), P, lw=1.1)
    txt(ax, 232.0, yc + 9.0, "pass", P, 6.2, P["muted"])
    txt(ax, 356.0, yc + 9.0, "pass", P, 6.2, P["muted"])

    # --- failure bus: any check failing drops to the scene failure sink ----
    line(ax, (170.0, ROW_Y), (170.0, 100.0), P, P["warn"], lw=1.0)
    line(ax, (418.0, ROW_Y), (418.0, 100.0), P, P["warn"], lw=1.0)
    line(ax, (170.0, 100.0), (418.0, 100.0), P, P["warn"], lw=1.0)
    arrow(ax, (294.0, ROW_Y), (294.0, 96.0), P, color=P["warn"], dashed=True, lw=1.0, ms=6.0)
    txt(ax, 284.0, 108.0, "fail", P, 6.2, P["warn"], ha="right")

    node(246.0, 56.0, 96.0, 40.0, "Scene failure", "diagnostic and failed code", P["rule"])
    line(ax, (246.0, 76.0), (51.0, 76.0), P, P["warn"], lw=1.0)
    arrow(ax, (51.0, 76.0), (51.0, ROW_Y), P, color=P["warn"], dashed=True, lw=1.0, ms=6.0)
    txt(ax, 145.0, 84.0, "generated again, up to N tries", P, 6.4, P["warn"])

    # --- program level: only the assembled program is patched -------------
    node(486.0, 62.0, 102.0, 42.0, "Assembled program", "every verified scene", P["rule"])
    arrow(ax, (537.0, ROW_Y), (537.0, 104.0), P, lw=1.1)
    txt(ax, 547.0, 114.0, "all scenes", P, 6.2, P["muted"], ha="left")

    node(506.0, 14.0, 76.0, 36.0, "Full render", "video artifact", P["accent"])
    arrow(ax, (537.0, 62.0), (537.0, 50.0), P, lw=1.1)
    txt(ax, 547.0, 56.0, "pass", P, 6.2, P["muted"], ha="left")

    node(344.0, 14.0, 140.0, 36.0, "Search-and-replace repair", "surgical patch", P["warn"])
    arrow(ax, (506.0, 32.0), (484.0, 32.0), P, color=P["warn"], dashed=True, lw=1.0, ms=6.0)
    txt(ax, 495.0, 39.0, "fail", P, 6.2, P["warn"])
    line(ax, (414.0, 50.0), (414.0, 83.0), P, P["warn"], lw=1.0)
    arrow(ax, (414.0, 83.0), (486.0, 83.0), P, color=P["warn"], dashed=True, lw=1.0, ms=6.0)
    txt(ax, 450.0, 89.0, "patched", P, 6.2, P["warn"])

    return fig


BUILDERS = {"overview": draw, "code-stage": draw_code_stage}


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=("dark", "light", "both"), default="both")
    ap.add_argument("--which", choices=("overview", "code-stage", "both"), default="both")
    args = ap.parse_args()

    OUT.mkdir(parents=True, exist_ok=True)
    which = ("overview", "code-stage") if args.which == "both" else (args.which,)
    for name in (("dark", "light") if args.variant == "both" else (args.variant,)):
        for w in which:
            fig = BUILDERS[w](PALETTES[name])
            stem = "framework_overview" if w == "overview" else "code_stage"
            suffix = "_dark" if name == "dark" else ""
            path = OUT / f"{stem}{suffix}.png"
            fig.savefig(path, dpi=300, facecolor=PALETTES[name]["bg"])
            plt.close(fig)
            print("figure →", path)


if __name__ == "__main__":
    main()
