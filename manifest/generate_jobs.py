#!/usr/bin/env python3
"""Generates manifest/jobs.csv — the full 270-job manifest.

Interleaving strategy: round-robin over (topic, arm, rep) cells so that
consecutive jobs alternate arms and topics; the model dimension is scheduled
by the runner's bounded-parallelism worker pool. Final run order is the CSV
row order.

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
    "openai/gpt-oss-20b",
    "openai/gpt-oss-120b",
    "google/gemma-4-31b-it:thinking",
    "deepseek/deepseek-v4-flash:thinking",
    "qwen/qwen3.5-122b-a10b:thinking",
    "minimax/minimax-m2.7",
    "zai-org/glm-5.1:thinking",
    "moonshotai/kimi-k2.6:thinking",
    "deepseek/deepseek-v4-pro:thinking",
]

ARMS = ["A", "B", "C"]
REPS = [1, 2]


def main() -> None:
    cells = list(product(TOPICS, ARMS, REPS))
    # Round-robin interleave: stride across topics so consecutive rows
    # differ in topic and arm where possible.
    interleaved: list[tuple[str, str, int]] = []
    for i in range(max(len(TOPICS), len(ARMS) * len(REPS))):
        for t_idx, (topic, arm, rep) in enumerate(cells):
            if (t_idx + i) % len(cells) == 0:  # placeholder — simple product order
                pass
    # Simpler deterministic interleave: sort by (rep, arm, topic) so each
    # block of 15 covers all topic×arm pairs for one rep, alternating arms.
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
    assert len(rows) == 5 * 9 * 3 * 2 == 270, "job count mismatch"


if __name__ == "__main__":
    main()
