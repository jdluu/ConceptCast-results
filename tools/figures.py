#!/usr/bin/env python3
"""Generate thesis figures from frozen benchmark artifacts. Schema-driven, no hardcoded
model IDs: the model list and display labels come from manifest/model_metadata.json and
the observed arm data. Costs are derived from tokens x the benchmark's flat pricing rates
(the same rates the backend used for jobs.cost), because the Nano GPT subscription API
does not report per-call cost. All sources are frozen; no live state.

Outputs (300 DPI PNG + machine-readable figure_data.json):
  figures/fig5_1_arm_model_completion.png
  figures/fig5_2_latency.png
"""
from __future__ import annotations

import csv
import json
import sqlite3
import statistics
from collections import defaultdict
from pathlib import Path

import matplotlib

matplotlib.use("Agg")
import matplotlib.pyplot as plt  # noqa: E402
import numpy as np  # noqa: E402

REPO = Path(__file__).resolve().parent.parent
FIG = REPO / "figures"
OUT = REPO / "reports"
MANIFEST = REPO / "manifest" / "jobs.csv"
METADATA = REPO / "manifest" / "model_metadata.json"
TRACE_FILE = REPO / "traces" / "bench-20260913.jsonl"  # arms A/B (backend wrote C separately)

# Backend pricing rates (infra/settings.py) — the same flat rates jobs.cost used.
PRICING_INPUT_PER_1K = 0.005
PRICING_OUTPUT_PER_1K = 0.015

plt.rcParams.update({
    "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9,
    "figure.dpi": 300, "savefig.dpi": 300, "axes.spines.top": False,
    "axes.spines.right": False,
})
ARM_COLORS = {"A": "#94a3b8", "B": "#3b82f6", "C": "#8b5cf6"}


def load_models() -> list[dict]:
    """Model roster from the frozen metadata (id + short display label)."""
    meta = json.load(METADATA.open())
    return sorted(meta["models"], key=lambda m: m["id"])


def short_label(meta: dict) -> str:
    """Display label: metadata short field, fallback to the id after the slash."""
    return meta.get("short") or meta["id"].split("/")[-1]


def load_completion(models: list[dict]) -> dict[str, dict[str, int]]:
    """Completed counts per (arm, model_id), recomputed from frozen artifacts."""
    comp = {a: {m["id"]: 0 for m in models} for a in "ABC"}
    ids = {m["id"] for m in models}

    # Arms A/B: outcome files keyed by job_seq; map seq->model via the manifest.
    seq_model = {}
    with MANIFEST.open(newline="") as f:
        for row in csv.DictReader(f):
            if row["arm"] in ("A", "B"):
                seq_model[int(row["job_seq"])] = (row["arm"], row["model"])
    for p in (REPO / "traces" / "outcomes").glob("job-*.json"):
        o = json.load(p.open())
        key = seq_model.get(o["job_seq"])
        if key and o["status"] == "completed" and o["arm"] == key[0] and key[1] in ids:
            comp[o["arm"]][key[1]] += 1

    # Arm C: the snapshotted database.
    db = sqlite3.connect(REPO / "data" / "conceptcast.db")
    for m, st in db.execute(
        "SELECT model_id, status FROM jobs WHERE benchmark_arm='C'"
    ):
        if st == "completed" and m in ids:
            comp["C"][m] += 1
    return comp


def load_latency(models: list[dict]) -> dict[str, list[float]]:
    """Latency in SECONDS. A/B: per-call latency_ms from traces. C: job wall-clock
    total_execution_time (verified seconds against created->updated deltas)."""
    lat: dict[str, list[float]] = {"A": [], "B": [], "C": []}
    for line in TRACE_FILE.open():
        r = json.loads(line)
        if r.get("arm") in ("A", "B") and r.get("latency_ms"):
            lat[r["arm"]].append(r["latency_ms"] / 1000.0)
    db = sqlite3.connect(REPO / "data" / "conceptcast.db")
    for (t,) in db.execute(
        "SELECT total_execution_time FROM jobs WHERE benchmark_arm='C' "
        "AND status='completed' AND total_execution_time IS NOT NULL"
    ):
        lat["C"].append(t)
    return lat


def load_tokens() -> dict[str, dict[str, int]]:
    """True per-arm token totals. Schema note: the two emitters differ —
    Arms A/B (monolithic runner) record raw OpenAI-style usage where the real totals are
    prompt_tokens/completion_tokens (input_tokens there is only the cached subset);
    Arm C (pydantic-ai emitter) records normalized input_tokens/output_tokens."""
    tok = {a: {"input": 0, "output": 0} for a in "ABC"}
    for line in TRACE_FILE.open():
        r = json.loads(line)
        a = r.get("arm")
        if a in ("A", "B"):
            tok[a]["input"] += r.get("prompt_tokens") or 0
            tok[a]["output"] += r.get("completion_tokens") or 0
    for p in (REPO / "traces").glob("bench-v2-*.jsonl"):
        for line in p.open():
            r = json.loads(line)
            if r.get("arm") == "C":
                tok["C"]["input"] += r.get("input_tokens") or 0
                tok["C"]["output"] += r.get("output_tokens") or 0
    return tok


def load_cost() -> dict[str, float]:
    """Derived cost per arm from true tokens x the backend's flat pricing rates.
    (jobs.cost systematically undercounts — it accumulates only the orchestrator's
    top-level agent.run() usage, not the streaming tool-iteration calls the traces
    capture; the trace-derived figure is authoritative.)"""
    tok = load_tokens()
    return {
        a: round(v["input"] / 1000 * PRICING_INPUT_PER_1K
                 + v["output"] / 1000 * PRICING_OUTPUT_PER_1K, 2)
        for a, v in tok.items()
    }


def fig1(comp, models) -> None:
    fig, ax = plt.subplots(figsize=(6.3, 2.9))
    labels = [short_label(m) for m in models]
    x = np.arange(len(models))
    w = 0.26
    for i, arm in enumerate(("A", "B", "C")):
        vals = [comp[arm][m["id"]] * 10 for m in models]
        ax.bar(x + (i - 1) * w, vals, w, label=f"Arm {arm}", color=ARM_COLORS[arm])
    ax.set_xticks(x, labels, rotation=35, ha="right")
    ax.set_ylabel("Completed jobs (%)")
    ax.set_ylim(0, 105)
    ax.set_title("End-to-end completion rate by model and arm (10 jobs per cell)")
    ax.legend(frameon=False, ncols=3, loc="upper right")
    ax.yaxis.grid(True, lw=0.4, color="#e2e8f0")
    ax.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(FIG / "fig5_1_arm_model_completion.png", bbox_inches="tight")
    plt.close(fig)


def fig2(lat) -> None:
    """All latencies in SECONDS on log scale (C job wall-time is minutes-scale but stored
    in seconds; do not rescale — plot the stored unit directly)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.3, 2.7), gridspec_kw={"width_ratios": [1, 1.4]})
    arms = ["A", "B", "C"]
    medians = [statistics.median(lat[a]) for a in arms]
    ax1.bar(arms, medians, color=[ARM_COLORS[a] for a in arms], width=0.55)
    ax1.set_yscale("log")
    for i, v in enumerate(medians):
        label = f"{v:.0f} s" if v < 120 else f"{v/60:.0f} min"
        ax1.text(i, v, label, ha="center", va="bottom", fontsize=8)
    ax1.set_ylabel("Median latency (log s)")
    ax1.set_title("Median latency")
    ax1.set_ylim(1, max(medians) * 3)
    ax1.yaxis.grid(True, lw=0.4, color="#e2e8f0")
    ax1.set_axisbelow(True)
    bp = ax2.boxplot(
        [lat["A"], lat["B"], lat["C"]], tick_labels=["Arm A", "Arm B", "Arm C"],
        patch_artist=True, showfliers=False, medianprops={"color": "#0f172a"},
    )
    for patch, a in zip(bp["boxes"], arms):
        patch.set_facecolor(ARM_COLORS[a]); patch.set_alpha(0.7)
    ax2.set_yscale("log")
    ax2.set_ylabel("Latency (s, log scale)")
    ax2.set_title("Latency distribution (outliers hidden)")
    ax2.yaxis.grid(True, lw=0.4, color="#e2e8f0")
    ax2.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(FIG / "fig5_2_latency.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    models = load_models()
    comp = load_completion(models)
    lat = load_latency(models)
    cost = load_cost()
    tokens = load_tokens()
    FIG.mkdir(exist_ok=True)
    fig1(comp, models)
    fig2(lat)
    stats = {
        "completion_pct": {f"{a}|{m['id']}": comp[a][m["id"]] * 10 for a in comp for m in models},
        "latency_seconds": {
            a: {"n": len(v), "median": statistics.median(v) if v else None,
                "mean": statistics.mean(v) if v else None,
                "p90": sorted(v)[int(len(v) * 0.9)] if v else None}
            for a, v in lat.items()
        },
        "tokens_true": tokens,
        "derived_cost_usd_flat_rates": cost,
        "pricing_note": ("Flat backend rates ($0.005/1k in, $0.015/1k out) applied to true "
                         "token totals; provider does not report per-call cost. jobs.cost "
                         "undercounts (orchestrator usage accumulation misses streaming "
                         "tool-iteration calls) — trace-derived figures are authoritative."),
    }
    (OUT / "figure_data.json").write_text(json.dumps(stats, indent=1) + "\n")
    print("figures →", FIG / "fig5_1_arm_model_completion.png")
    print("figures →", FIG / "fig5_2_latency.png")


if __name__ == "__main__":
    main()
