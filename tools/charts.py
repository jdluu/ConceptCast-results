#!/usr/bin/env python3
"""Generate the standard benchmark chart set from derived data — no
topic/model/arm names or metric values in this source.

Reads whatever reports/derived/ contains (from db_query.py / traces_agg.py)
and renders:

  1. success_rates.png   — outcome distribution per group (grouped bars)
  2. tokens_latency.png  — token totals & latency quantiles per group
  3. attempts.png        — retry/attempt pressure per group

Every chart titles itself with the dimension names it grouped by, so the same
script produces correct figures if the dimensions change.

Usage:
  python3 scripts/charts.py                 # render all charts it can
  python3 scripts/charts.py --out reports/figures
"""
from __future__ import annotations

import csv
import sys
from collections import Counter, defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
DERIVED = REPO / "reports" / "derived"
DEFAULT_OUT = REPO / "reports" / "figures"

OUTCOME_VALUES = {"completed", "failed", "fallback-completed", "infrastructure-failed", "awaiting-review"}


def load_derived() -> list[tuple[str, list[dict]]]:
    """(file stem, rows) per derived CSV — analyzed separately, never merged."""
    out: list[tuple[str, list[dict]]] = []
    for path in sorted(DERIVED.glob("*.csv")):
        with path.open(newline="") as f:
            rows = list(csv.DictReader(f))
        if rows:
            out.append((path.stem, rows))
    if not out:
        sys.exit(f"no derived data under {DERIVED} — run db_query.py / traces_agg.py first")
    return out


def dims_of(rows: list[dict]) -> list[str]:
    """Dimension columns = low-cardinality string fields excluding measures."""
    counts: dict[str, int] = {}
    for r in rows[:1]:
        for k, v in r.items():
            counts[k] = len({r2.get(k) for r2 in rows})
    return [
        k
        for k in rows[0]
        if isinstance(rows[0].get(k), str)
        and not any(h in k.lower() for h in ("tokens", "latency", "cost", "count", "calls", "total", "mean", "p95", "n"))
        and len({r.get(k) for r in rows}) <= 12
    ]


def group_key(rows: list[dict], dims: list[str]) -> dict[str, dict[str, int]]:
    agg: dict[str, dict[str, int]] = defaultdict(Counter)
    for r in rows:
        key = " | ".join(str(r.get(d, "?")) for d in dims)
        status = str(r.get("status", r.get("calls", "?")))
        if status in OUTCOME_VALUES:
            agg[key][status] += int(r.get("count", 1))
    return agg


def chart_success(rows: list[dict], out: Path, dims: list[str]) -> bool:
    # Tally rows (status + count columns) → status is the series, other dims the axis.
    tally_rows = [r for r in rows if "status" in r and "count" in r]
    if tally_rows:
        group_dims = [d for d in dims if d != "status"] or ["arm"]
        agg: dict[str, Counter] = defaultdict(Counter)
        for r in tally_rows:
            key = " | ".join(str(r.get(d, "?")) for d in group_dims)
            agg[key][str(r["status"])] += int(float(r["count"]))
        xdims = group_dims
    else:
        agg = group_key(rows, dims)
        xdims = dims
    if not agg:
        return False
    labels = list(agg)
    statuses = sorted({s for c in agg.values() for s in c})
    fig, ax = plt.subplots(figsize=(1.1 * len(labels) + 2, 4.5))
    bottom = [0] * len(labels)
    for s in statuses:
        vals = [agg[l].get(s, 0) for l in labels]
        ax.bar(labels, vals, bottom=bottom, label=s)
        bottom = [b + v for b, v in zip(bottom, vals)]
    ax.set_ylabel("jobs")
    ax.set_xlabel(" ← ".join(reversed(xdims)))
    ax.set_title(f"Benchmark outcomes by {' × '.join(xdims)}")
    ax.legend(fontsize=8)
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / "success_rates.png", dpi=200)
    plt.close(fig)
    return True


def chart_measures(rows: list[dict], out: Path, dims: list[str]) -> bool:
    """Bar chart of any *total/mean measure columns present."""
    measure_cols = [
        c
        for c in rows[0]
        if any(h in c.lower() for h in ("tokens.total", "latency.mean", "p95", "mean"))
        and any(isinstance(r.get(c), (int, float)) for r in rows)
    ]
    if not measure_cols:
        return False
    labels = sorted({" | ".join(str(r.get(d, "?")) for d in dims) for r in rows})
    fig, ax = plt.subplots(figsize=(1.2 * len(labels) + 2, 4.5))
    import math

    width = 0.8 / max(len(measure_cols), 1)
    for i, col in enumerate(measure_cols):
        vals = {}
        for r in rows:
            k = " | ".join(str(r.get(d, "?")) for d in dims)
            if isinstance(r.get(col), (int, float)):
                vals.setdefault(k, 0)
                vals[k] += r[col]
        xs = range(len(labels))
        ax.bar([x + i * width for x in xs], [vals.get(l, 0) for l in labels], width, label=col)
    ax.set_xlabel(" ← ".join(reversed(dims)))
    ax.set_title("Measures by " + " × ".join(dims))
    ax.set_yscale("symlog")
    ax.legend(fontsize=7)
    plt.xticks(rotation=30, ha="right")
    fig.tight_layout()
    out.mkdir(parents=True, exist_ok=True)
    fig.savefig(out / "measures.png", dpi=200)
    plt.close(fig)
    return True


def main() -> None:
    out = DEFAULT_OUT
    if "--out" in sys.argv:
        out = Path(sys.argv[sys.argv.index("--out") + 1])
    out.mkdir(parents=True, exist_ok=True)

    made = []
    for stem, rows in load_derived():
        dims = dims_of(rows) or ["status"]
        if chart_success(rows, out / f"{stem}", dims):
            made.append(f"{stem}/success_rates.png")
        if chart_measures(rows, out / f"{stem}", dims):
            made.append(f"{stem}/measures.png")
    if made:
        print("rendered:", ", ".join(made), f"→ {out}")
    else:
        print("nothing renderable from current derived data")


if __name__ == "__main__":
    main()
