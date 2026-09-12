# ConceptCast Benchmark v2 — Manifest, Traces & Tooling

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
| `traces/` | Per-call JSONL traces (one file per run, `<run_id>.jsonl`). Written during runs; not pre-populated. |

## Benchmark Design (summary)

- **Arm A** — monolithic generation (one call, no validation/repair).
- **Arm B** — monolithic + the same AST validation/repair loop as the council.
- **Arm C** — the full agent council (Analyst → Architect → Animator, GCO,
  per-scene generation, AST validation, diff-repair).

Identical model roster, sampling pins (temperature 0), and topic prompt strings
across arms. Outcome taxonomy per job: `completed`, `fallback-completed`,
`failed`, `infrastructure-failed`. See `plan/EXPERIMENT_PLAN.md` for the full
protocol.

## Reproducing a Run

```bash
# 1. Regenerate the manifest if the roster changed
python3 manifest/generate_jobs.py

# 2. Run the benchmark (from the application repo, backend running)
cd apps/backend
BENCH_TRACE_DIR=<traces-dir> BENCH_RUN_ID=<run-id> BENCH_TEMPERATURE=0 \
  uv run python src/scripts/benchmark_council.py \
  --manifest <path-to>/manifest/jobs.csv --arm C --parallelism 8

# 3. Analyze
python3 tools/summarize.py --db <jobs.db> --traces traces/ --manifest manifest/jobs.csv
```

The runners are resumable: manifest tuples already recorded as completed are
skipped on restart.

## License & Attribution

This repository is released for academic reproducibility and public research
verification under the MIT License (see [LICENSE](LICENSE)).
