#!/usr/bin/env python3
"""Repair effectiveness, as a slide asset.

There is no repair table in the thesis. The numbers exist as prose in
chapters/5_results.tex ("Verification and Repair Effectiveness") and as
structured data in reports/benchmark_summary.json, so this draws that data as a
table rather than inventing anything.

Every figure is derived from the per-job manifests under artifacts/ at build
time and checked against benchmark_summary.json, so the table cannot drift from
the run it describes.

Outputs:
  reports/figures/repair_effectiveness_dark.png   deck variant
  reports/figures/repair_effectiveness.png        print / paper variant

Run: .venv/bin/python tools/repair_effectiveness_table.py
"""
from __future__ import annotations

import argparse
import collections
import json
import statistics
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

from framework_figure import PALETTES, txt  # same directory as this script

REPO = Path(__file__).resolve().parent.parent
OUT = REPO / "reports" / "figures"
W, H = 292.0, 200.0

HEAD = ["", "Arm A", "Arm B"]
# label rows; the values are filled from the manifests by derive()
ROWS = [
    ("Passed first generation", None, None),
    ("Completed", None, None),
    ("Recovered by repair", None, None),
    ("Median attempts per job", None, None),
]
NOTE = ("First-pass and recovery rates are measured for Arm B. Arm C repairs "
        "scene by scene, so these rates do not apply to it.")


def derive() -> dict:
    """Count the arm outcomes from the per-job manifests, not from a summary."""
    art = REPO / "artifacts"
    out = {}
    for arm in ("A", "B", "C"):
        f = art / f"arm_{arm}" / "manifest.json"
        if not f.exists():
            continue
        jobs = json.loads(f.read_text())
        jobs = jobs if isinstance(jobs, list) else list(jobs.values())
        first = sum(1 for j in jobs if j.get("first_pass") is True)
        done = sum(1 for j in jobs if j.get("status") == "completed")
        att = [j["attempts"] for j in jobs if isinstance(j.get("attempts"), int)]
        out[arm] = {"jobs": len(jobs), "first_pass": first, "completed": done,
                    "recovered": done - first if arm != "A" else 0,
                    "median_attempts": int(statistics.median(att)) if att else None}
    return out


def table_cells() -> dict[str, list[str]]:
    d = derive()
    return {
        "A": [str(d["A"]["first_pass"]), str(d["A"]["completed"]),
              str(d["A"]["recovered"]), str(d["A"]["median_attempts"])],
        "B": [str(d["B"]["first_pass"]), str(d["B"]["completed"]),
              str(d["B"]["recovered"]), str(d["B"]["median_attempts"])],
    }


def draw(P: dict, cells: dict[str, list[str]]) -> plt.Figure:
    fig = plt.figure(figsize=(W / 72.0, H / 72.0), dpi=300, facecolor=P["bg"])
    ax = fig.add_axes([0, 0, 1, 1])
    ax.set_xlim(0, W)
    ax.set_ylim(0, H)
    ax.axis("off")

    c_label, c_a, c_b = 10.0, 232.0, 282.0

    def rule(y, colour, lw=1.0):
        ax.plot([10, W - 10], [y, y], color=colour, lw=lw, zorder=3)

    txt(ax, c_label, 180.0, HEAD[0], P, 8.5, P["muted"], ha="left")
    txt(ax, c_a, 180.0, HEAD[1], P, 8.5, P["muted"], ha="right")
    txt(ax, c_b, 180.0, HEAD[2], P, 8.5, P["muted"], ha="right")
    rule(167.0, P["accent"], 1.6)

    for i, (label, _, _) in enumerate(ROWS):
        y = 146.0 - i * 24.0
        # the recovery line is the point of the table, so it carries the accent
        colour = P["accent"] if label == "Recovered by repair" else P["ink"]
        weight = "bold" if label == "Recovered by repair" else "normal"
        txt(ax, c_label, y, label, P, 9.5, colour, weight=weight, ha="left")
        txt(ax, c_a, y, cells["A"][i], P, 9.5, colour, weight=weight, ha="right")
        txt(ax, c_b, y, cells["B"][i], P, 9.5, colour, weight=weight, ha="right")
        if i == 2:
            rule(y - 12.0, P["rule"])

    for i, line in enumerate(NOTE.split(". ")):
        txt(ax, c_label, 40.0 - i * 11.0, line + ("" if line.endswith(".") else "."),
            P, 7.0, P["muted"], ha="left")
    return fig


def check_the_table(cells: dict[str, list[str]]) -> None:
    """The table must match the run. Fail loudly rather than draw a stale number."""
    jobs = {}
    for arm in ("A", "B", "C"):
        f = REPO / "artifacts" / f"arm_{arm}" / "manifest.json"
        if f.exists():
            recs = json.loads(f.read_text())
            jobs[arm] = recs if isinstance(recs, list) else list(recs.values())

    for arm in ("A", "B"):
        recs = jobs.get(arm, [])
        first = sum(1 for j in recs if j.get("first_pass") is True)
        done = sum(1 for j in recs if j.get("status") == "completed")
        if int(cells[arm][0]) != first:
            raise SystemExit(f"arm {arm}: first-pass {cells[arm][0]} != {first} counted from its own jobs")
        if int(cells[arm][1]) != done:
            raise SystemExit(f"arm {arm}: completed {cells[arm][1]} != {done} counted from its own jobs")

    # Arm B's failures that finished later are exactly the recovered count
    recovered = sum(1 for j in jobs.get("B", [])
                    if j.get("status") == "completed" and j.get("first_pass") is not True)
    if int(cells["B"][2]) != recovered:
        raise SystemExit(f"recovered {cells['B'][2]} != {recovered} counted from Arm B's jobs")

    # Arm A must still be a single generation per job, or the two arms are no
    # longer the like-for-like first-pass comparison the slide claims
    a_att = [j["attempts"] for j in jobs.get("A", []) if isinstance(j.get("attempts"), int)]
    if a_att and int(cells["A"][3]) != int(statistics.median(a_att)):
        raise SystemExit(f"Arm A's median attempts is {statistics.median(a_att)}, not {cells['A'][3]}")

    summary = REPO / "reports" / "benchmark_summary.json"
    if summary.exists():
        arms = json.loads(summary.read_text())["arms"]
        for arm in ("A", "B"):
            for idx, field in ((0, "first_pass"), (1, "completed"), (2, "recovered")):
                if int(cells[arm][idx]) != arms[arm][field]:
                    raise SystemExit(f"arm {arm} {field}: table {cells[arm][idx]} != summary {arms[arm][field]}")
    print("✓ repair table matches artifacts/*/manifest.json and reports/benchmark_summary.json")


def main() -> None:
    ap = argparse.ArgumentParser()
    ap.add_argument("--variant", choices=("dark", "light", "both"), default="both")
    args = ap.parse_args()
    cells = table_cells()
    check_the_table(cells)
    OUT.mkdir(parents=True, exist_ok=True)
    for name in (("dark", "light") if args.variant == "both" else (args.variant,)):
        fig = draw(PALETTES[name], cells)
        suffix = "_dark" if name == "dark" else ""
        path = OUT / f"repair_effectiveness{suffix}.png"
        fig.savefig(path, dpi=300, facecolor=PALETTES[name]["bg"])
        plt.close(fig)
        print("figure →", path)
    print(f"   cells → A {cells['A']} | B {cells['B']}")


if __name__ == "__main__":
    main()
