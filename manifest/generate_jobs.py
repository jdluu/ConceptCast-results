#!/usr/bin/env python3
"""Generates manifest/jobs.csv — the benchmark manifest.

Roster: the validated 10-model smoke list (see model_metadata.json, all IDs
verified live against Nano GPT on 2026-09-12). Structure: 5 topics x 10
models x 3 arms x 2 reps = 300 jobs. Arm C (council) is the framework arm;
arms A/B are baseline arms used by benchmark_monolithic.py.

Usage: python3 manifest/generate_jobs.py
"""
from __future__ import annotations

import csv
from itertools import product
from pathlib import Path

TOPICS = [
    "derivative of a function in calculus",
    "backpropagation",
    "Fourier transform",
    "Doppler effect",
    "eigenvectors",
]

MODELS = [
    "z-ai/glm-5.3",
    "qwen/qwen3.8-flash",
    "deepseek/deepseek-v4-flash",
    "moonshotai/kimi-k2.6",
    "xiaomi/mimo-v2.5-pro",
    "tencent/hy3",
    "nvidia/nemotron-3-ultra-550b-a55b",
    "meta/muse-glimmer-30b",
    "google/gemma-4-31b-it",
    "openai/gpt-oss-120b",
]

ARMS = ["A", "B", "C"]
REPS = [1, 2]


def main() -> None:
    cells = list(product(TOPICS, ARMS, REPS))
    # Deterministic interleave: sort by (rep, arm, topic) so each block
    # covers all topic x arm pairs for one rep, arms grouped.
    interleaved = sorted(cells, key=lambda c: (c[2], ARMS.index(c[1]), TOPICS.index(c[0])))

    rows = []
    job_seq = 0
    for topic, arm, rep in interleaved:
        for model in MODELS:
            job_seq += 1
            rows.append(
                {
                    "job_seq": job_seq,
                    "topic": topic,
                    "model": model,
                    "arm": arm,
                    "rep": rep,
                    "status": "pending",
                    "started_at": "",
                    "finished_at": "",
                    "framework_commit": "",
                }
            )

    out = Path(__file__).parent / "jobs.csv"
    with out.open("w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        writer.writeheader()
        writer.writerows(rows)

    print(f"Wrote {len(rows)} jobs to {out}")
    assert len(rows) == len(TOPICS) * len(MODELS) * len(ARMS) * len(REPS) == 300, (
        "job count mismatch"
    )


if __name__ == "__main__":
    main()
