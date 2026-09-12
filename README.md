# ConceptCast Benchmark — Manifest, Traces & Tooling

This repository holds everything needed to reproduce the ConceptCast
benchmark: the pre-registered job manifest, per-call execution traces, the
experiment plan, and schema-driven analysis tooling.

> **Companion repository:** application source lives in
> [ConceptCast](https://github.com/jdluu/ConceptCast).

## Repository Contents

| Path | Contents |
|---|---|
| `manifest/jobs.csv` | The pre-registered job grid (topic × model × arm × rep). Single source of truth — the runner writes each row's `job_seq` into the job record for exact joins. |
| `manifest/model_metadata.json` | The validated model roster (IDs verified live against the Nano GPT API), tiers, params, licenses, sampling pins. |
| `manifest/generate_jobs.py` | Regenerates `jobs.csv` from `model_metadata.json`. |
| `manifest/topics.json` | Canonical topic prompt strings (identical across arms). |
| `plan/EXPERIMENT_PLAN.md` | Hypotheses, arm definitions, controls, outcome taxonomy, metrics, run protocol. |
| `tools/` | Schema-driven analysis scripts (`db_query.py`, `traces_agg.py`, `charts.py`, `summarize.py`) — see `tools/README.md`. |
| `data/conceptcast.db` | SQLite snapshot of the benchmark run (populated by `scripts/snapshot_db.sh` after a run; empty until then). |
| `traces/` | Per-call JSONL traces (one file per run, `<run_id>.jsonl`). Written during runs. |

## Benchmark Design (summary)

- **Arm A** — monolithic generation (one call, no validation/repair).
- **Arm B** — monolithic + the same AST validation/repair loop as the council.
- **Arm C** — the full agent council (Analyst → Architect → Animator, GCO,
  per-scene generation, AST validation, diff-repair).

Identical model roster, sampling pins (temperature 0), and topic prompt strings
across arms. Outcome taxonomy per job: `completed`, `fallback-completed`,
`failed`, `infrastructure-failed`. See `plan/EXPERIMENT_PLAN.md` for the full
protocol.

## What the data will look like

The analysis tools are schema-driven and ready to run the moment data lands.
Expected shapes:

- **`data/conceptcast.db`** — `jobs` table with one row per manifest tuple:
  `status` ∈ {completed, fallback-completed, failed, infrastructure-failed},
  per-job `cost`/`total_execution_time`, and the `benchmark_job_seq` /
  `benchmark_arm` / `benchmark_rep` provenance columns for exact manifest joins.
- **`traces/<run_id>.jsonl`** — one JSON object per LLM call: stage
  (analyst/architect/animator), token counts (input/output/reasoning),
  latency, cost, and the same `job_seq`/arm/rep provenance.

From these two sources the full metric set in `plan/EXPERIMENT_PLAN.md`
derives: E2E completion rate per arm × model × topic, first-pass compile
rates, post-repair success rates, tokens and cost per job and per successful
video, and latency distributions.

## Reproducing a Run

```bash
# 1. Regenerate the manifest if the roster changed
python3 manifest/generate_jobs.py

# 2. Run the benchmark (from the application repo, backend running)
cd apps/backend
BENCH_TRACE_DIR=<traces-dir> BENCH_RUN_ID=<run-id> BENCH_TEMPERATURE=0 \
  uv run python src/scripts/benchmark_council.py \
  --manifest <path-to>/manifest/jobs.csv --arm C --parallelism 8

# 3. Snapshot the database into this repo
python3 <app-repo>/scripts/snapshot_sqlite.py \
  <app-repo>/data/conceptcast.db data/conceptcast.db

# 4. Analyze — the full pipeline in one command
python3 tools/summarize.py
```

The runners are resumable: manifest tuples already recorded as completed are
skipped on restart.

## License & Attribution

This repository is released for academic reproducibility and public research
verification under the MIT License (see [LICENSE](LICENSE)).
