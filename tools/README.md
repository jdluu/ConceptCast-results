# Data Tooling (scripts/)

Generic, schema-driven tools for analyzing benchmark v2 data. Nothing about
topics, models, arms, or metric values is hardcoded — grouping dimensions come
from `manifest/jobs.csv` and the traces themselves; DB/JSONL schemas are
introspected at runtime.

## The one join rule

Every analysis joins DB rows to the manifest:

- **Preferred**: `jobs.benchmark_job_seq == manifest.job_seq` (exact). The
  benchmark runner writes the manifest `job_seq` into each job row.
- **Fallback**: `(topic, model_id)` — only safe when reps don't exist; if a
  (topic, model) pair matches multiple manifest rows, those jobs are labeled
  `?` with a loud warning rather than guessed.

## Scripts

| Script | Purpose |
|---|---|
| `db_query.py` | Aggregate any jobs column by any dimension. `--schema` shows available columns. |
| `traces_agg.py` | Fold per-call `traces/*.jsonl` into per-group token/latency/cost summaries. Metric and dimension fields are discovered from the data. |
| `charts.py` | Render one stacked-outcome chart (plus measures, when present) per derived CSV. Chart titles/axes derive from the data. |
| `summarize.py` | One command: run the full pipeline → `reports/derived/*.csv`, `reports/figures/`, `reports/summary.md`. |
| `common.py` | Shared helpers: manifest loading, read-only DB access, trace iteration, provenance stamping (every JSON output records its input hashes). |

## Usage

```bash
# After (or during) a benchmark run:
python3 scripts/db_query.py --schema                       # what's queryable
python3 scripts/db_query.py --by arm --metric status       # outcomes per arm
python3 scripts/db_query.py --by arm model --metric status --format csv
python3 scripts/db_query.py --by model --metric total_execution_time --agg mean

# Trace measures (tokens, latency, cost per call):
python3 scripts/traces_agg.py --by arm stage
python3 scripts/traces_agg.py --by arm model --format csv

# Full pipeline:
python3 scripts/summarize.py
```

## Dependencies

Python 3.11+, `matplotlib` + `pandas` (only `charts.py` needs them). A venv is
expected at `.venv/` (`uv venv .venv && uv pip install matplotlib pandas`).

## Rules

1. Aggregates in `reports/derived/` are always regenerable from
   `data/conceptcast.db` + `traces/` + `manifest/jobs.csv`. Never hand-edit.
2. Unknown columns/fields are reported and skipped — tools fail loud, never
   silently wrong.
3. If you change the trace schema, the tools adapt automatically; if you add a
   dimension to the manifest, it's immediately usable as a group-by.
