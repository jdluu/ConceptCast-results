# ConceptCast Benchmark — Manifest, Traces & Tooling

This repository holds everything needed to reproduce the ConceptCast
benchmark: the pre-registered job manifest, per-call execution traces, the
experiment plan, schema-driven analysis tooling, and the frozen results of
the completed run (`bench-20260913`).

> **Companion repository:** application source lives in
> [ConceptCast](https://github.com/jdluu/ConceptCast).

## Repository Contents

| Path | Contents |
|---|---|
| `manifest/jobs.csv` | The pre-registered job grid (topic × model × arm × rep). Single source of truth — the runner writes each row's `job_seq` into the job record for exact joins. Final per-job statuses reconciled from the outcome files and the council journal. |
| `manifest/model_metadata.json` | The validated model roster (IDs verified live against the Nano GPT API), display labels, licenses, and sampling pins. |
| `manifest/generate_jobs.py` | Regenerates `jobs.csv` from `model_metadata.json`. |
| `manifest/topics.json` | Canonical topic prompt strings (identical across arms). |
| `plan/EXPERIMENT_PLAN.md` | Hypotheses, arm definitions, controls, outcome taxonomy, metrics, run protocol. |
| `data/conceptcast.db` | SQLite snapshot of the benchmark run (Arm C jobs; written by `snapshot_sqlite.py` from the application repo after a run). |
| `traces/` | Per-call JSONL traces: `bench-v2-20260915.jsonl` (Arms A/B, monolithic runner emitter) and `bench-v2-20260912.jsonl` (Arm C, backend emitter; the run ID in the filename reflects the backend's configured `BENCH_RUN_ID`). |
| `traces/outcomes_v2/` | Per-job outcome records for Arms A/B (`job-<seq>.json`), used for resumability and reconciliation. |
| `reports/` | Machine-readable result summaries (`benchmark_summary.json`, `figure_data.json`). |
| `figures/` | Thesis figures rendered by `tools/figures.py` (300 DPI PNG). |
| `tools/` | Schema-driven analysis scripts — see `tools/README.md`. |
| `artifacts/` | Frozen per-arm outputs: generated Manim code (`seq*.py`), rendered videos (`videos.tar.gz`), and a `manifest.json` mapping job_seq → model/topic/files. Subdirs: `arm_A/` (36 videos), `arm_B/` (68 videos), `arm_C/` (53 videos). |

## Benchmark Design (summary)

- **Arm A** — monolithic generation: one call produces the full multi-scene
  script (no validation, repair, or rendering feedback).
- **Arm B** — monolithic + repair: the same single-call generation, followed by
  the AST validation suite, render check, and search-and-replace repair loop.
- **Arm C** — the full agent council (Analyst → Architect → Animator, GCO,
  per-scene generation, AST validation, diff-repair).

All arms share the same success criterion: the script must render to video
through the same sandboxed Manim engine. `completed` requires a produced
video artifact.

Identical model roster (10 models), topic set (5 topics), sampling pins
(temperature 0), and topic prompt strings across arms; 2 repetitions per
cell (300 jobs total). Outcome taxonomy per job: `completed`,
`fallback-completed`, `failed`, `infrastructure-failed`. See
`plan/EXPERIMENT_PLAN.md` for the full protocol.

## Results

All 300 jobs attempted; every arm used the same task: generate a multi-scene
Manim script and render it to video. Completed: Arm A 36/100, Arm B 68/100,
Arm C 53/100. Headline numbers, per-model breakdowns, and latency statistics
live in `reports/benchmark_summary.json` and `reports/figure_data.json`;
thesis figures in `figures/` are rendered from the same frozen artifacts.

**Cost note:** the provider (Nano GPT subscription API) does not report
per-call cost. Costs in this repository are *derived* from true token totals
using the backend's flat pricing rates ($0.005/1k input, $0.015/1k output)
and are estimates — their relative ordering across arms is meaningful, their
absolute values are not. The `jobs.cost` column in the database snapshot
systematically undercounts (it accumulates only top-level agent usage, not
streaming tool-iteration calls); the trace-derived figures are authoritative.

**Token schema note:** the two trace emitters differ. Arms A/B record raw
OpenAI-style usage (`prompt_tokens` / `completion_tokens` are the real
totals; `input_tokens` there is only the cached subset). Arm C's emitter
records normalized `input_tokens` / `output_tokens`. `tools/figures.py`
handles both; check the emitter before aggregating raw fields.

## Reproducing the Analysis

```bash
# 0. One-time: analysis environment
uv venv .venv && uv pip install --python .venv/bin/python matplotlib numpy

# 1. Aggregate the database snapshot (Arm C) — any column by any dimension
python3 tools/db_query.py --by arm --format table

# 2. Fold per-call traces into per-arm/per-model summaries
python3 tools/traces_agg.py --by arm,stage

# 3. Render the thesis figures (300 DPI, deterministic pixel content)
.venv/bin/python tools/figures.py

# 4. Headline summary
cat reports/benchmark_summary.json
```

## Reproducing a Run

```bash
# 1. Regenerate the manifest if the roster changed
python3 manifest/generate_jobs.py

# 2. Run the benchmark (from the application repo, backend running)
cd apps/backend
BENCH_TRACE_DIR=<traces-dir> BENCH_RUN_ID=<run-id> BENCH_TEMPERATURE=0 \
  uv run python src/scripts/run_full_benchmark.py          # all three arms, sequential
# or per-arm:
uv run python src/scripts/benchmark_council.py \
  --manifest <path-to>/manifest/jobs.csv --arm C --parallelism 8
uv run python src/scripts/benchmark_monolithic_v2.py \
  --manifest <path-to>/manifest/jobs.csv --arm A --trace-dir <traces-dir>

# 3. Snapshot the database into this repo
python3 <app-repo>/scripts/snapshot_sqlite.py \
  <app-repo>/data/conceptcast.db data/conceptcast.db
```

The runners are resumable: Arms A/B skip jobs with an existing
`traces/outcomes_v2/job-<seq>.json`; Arm C skips manifest tuples already
recorded as completed in the database.

## License & Attribution

This repository is released for academic reproducibility and public research
verification under the MIT License (see [LICENSE](LICENSE)).
