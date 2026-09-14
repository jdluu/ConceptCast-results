#!/usr/bin/env python3
"""Generate thesis figures from the frozen bench-20260913 data.

Outputs (300 DPI PNG, thesis-ready):
  figures/fig5_1_arm_model_completion.png  — grouped bars: completion % by model × arm
  figures/fig5_2_latency.png               — latency comparison across arms

Data sources: traces/outcomes/*.json (A/B), data/conceptcast.db (C),
traces/*.jsonl (per-call latency). All frozen artifacts; no live state.
"""
from __future__ import annotations

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
MODELS = [
    "moonshotai/kimi-k2.6", "xiaomi/mimo-v2.5-pro", "meta/muse-glimmer-30b",
    "google/gemma-4-31b-it", "tencent/hy3", "z-ai/glm-5.3",
    "deepseek/deepseek-v4-flash", "nvidia/nemotron-3-ultra-550b-a55b",
    "openai/gpt-oss-120b", "qwen/qwen3.8-flash",
]
SHORT = {
    "moonshotai/kimi-k2.6": "kimi-k2.6", "xiaomi/mimo-v2.5-pro": "mimo-v2.5",
    "meta/muse-glimmer-30b": "muse-glim.", "google/gemma-4-31b-it": "gemma-4-31b",
    "tencent/hy3": "hy3", "z-ai/glm-5.3": "glm-5.3",
    "deepseek/deepseek-v4-flash": "ds-v4-flash",
    "nvidia/nemotron-3-ultra-550b-a55b": "nemotron-3u",
    "openai/gpt-oss-120b": "gpt-oss-120b", "qwen/qwen3.8-flash": "qwen3.8",
}

plt.rcParams.update({
    "font.size": 9, "axes.titlesize": 10, "axes.labelsize": 9,
    "figure.dpi": 300, "savefig.dpi": 300, "axes.spines.top": False,
    "axes.spines.right": False,
})
COLORS = {"A": "#94a3b8", "B": "#3b82f6", "C": "#8b5cf6"}


def load() -> tuple[dict, dict]:
    outcomes = [json.load(p.open()) for p in (REPO / "traces" / "outcomes").glob("job-*.json")]
    db = sqlite3.connect(REPO / "data" / "conceptcast.db")
    crows = db.execute(
        "SELECT model_id, status, total_execution_time FROM jobs WHERE benchmark_arm='C'"
    ).fetchall()
    comp = {arm: {m: 0 for m in MODELS} for arm in ("A", "B", "C")}
    for o in outcomes:
        if o["status"] == "completed":
            comp[o["arm"]][o["model"]] += 1
    for m, st, _ in crows:
        if st == "completed":
            comp["C"][m] += 1
    # latency
    lat = {"A": [], "B": [], "C": []}
    for line in (REPO / "traces" / "bench-20260913.jsonl").open():
        r = json.loads(line)
        if r.get("arm") in ("A", "B") and r.get("latency_ms"):
            lat[r["arm"]].append(r["latency_ms"] / 1000.0)
    for m, t, st in db.execute(
        "SELECT model_id, total_execution_time, status FROM jobs WHERE benchmark_arm='C' "
        "AND status='completed' AND total_execution_time IS NOT NULL"
    ):
        lat["C"].append(t)  # total_execution_time is already seconds
    return comp, lat


def fig1(comp) -> None:
    fig, ax = plt.subplots(figsize=(6.3, 2.9))
    x = np.arange(len(MODELS))
    w = 0.26
    for i, arm in enumerate(("A", "B", "C")):
        vals = [comp[arm][m] * 10 for m in MODELS]
        ax.bar(x + (i - 1) * w, vals, w, label=f"Arm {arm}", color=COLORS[arm])
    ax.set_xticks(x, [SHORT[m] for m in MODELS], rotation=35, ha="right")
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
    """All latencies normalized to SECONDS (C job wall-time is minutes in the DB)."""
    fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(6.3, 2.7), gridspec_kw={"width_ratios": [1, 1.4]})
    arms = ["A", "B", "C"]
    medians = [statistics.median(lat[a]) for a in arms]
    ax1.bar(arms, medians, color=[COLORS[a] for a in arms], width=0.55)
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
        patch.set_facecolor(COLORS[a]); patch.set_alpha(0.7)
    ax2.set_yscale("log")
    ax2.set_ylabel("Latency (s, log scale)")
    ax2.set_title("Latency distribution (outliers hidden)")
    ax2.yaxis.grid(True, lw=0.4, color="#e2e8f0")
    ax2.set_axisbelow(True)
    fig.tight_layout()
    fig.savefig(FIG / "fig5_2_latency.png", bbox_inches="tight")
    plt.close(fig)


def main() -> None:
    comp, lat = load()
    FIG.mkdir(exist_ok=True)
    fig1(comp)
    fig2(lat)
    # machine-readable provenance
    stats = {
        "completion_pct": {f"{a}|{m}": comp[a][m] * 10 for a in comp for m in comp[a]},
        "latency": {
            a: {"n": len(v), "median": statistics.median(v) if v else None,
                "mean": statistics.mean(v) if v else None,
                "p90": sorted(v)[int(len(v) * 0.9)] if v else None}
            for a, v in lat.items()
        },
    }
    (OUT / "figure_data.json").write_text(json.dumps(stats, indent=1) + "\n")
    print("figures →", FIG / "fig5_1_arm_model_completion.png")
    print("figures →", FIG / "fig5_2_latency.png")


if __name__ == "__main__":
    main()
