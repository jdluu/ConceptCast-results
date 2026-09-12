# ConceptCast Thesis Benchmark Results & Dataset

This repository contains the empirical benchmark dataset, execution logs, model evaluations, and rendered figure graphics supporting the **ConceptCast** thesis.

> **Companion repository:** application source lives in
> [ConceptCast](https://github.com/jdluu/ConceptCast).

## Repository Contents

* `data/conceptcast.db`: SQLite database containing complete job runs, agent thought streams, execution timings, token/dollar costs, and AST diff repair logs across tested LLM models.
* `reports/`: Raw execution log text files (`.txt`), evaluation CSVs (`compilation_success.csv`, `latency_cost.csv`, `token_consumption.csv`), and aggregate performance summaries (`.json`) for each evaluation run across models (DeepSeek, Gemma, MiniMax, Kimi, GPT-OSS, Qwen, GLM).
* `figures/`: Rendered high-resolution chart graphics (`.png` and `.svg`) for thesis figures:
  * `fig5_1_model_success_progress`: E2E video rendering success progress across 6 iterative runs.
  * `fig5_2_compilation_repair_rates`: First-pass compilation vs AST diff repair success rates across 9 models.
  * `fig5_3_token_consumption_savings`: Monolithic vs Layered GCO token window savings across pipeline phases.
  * `fig5_4_latency_cost_comparison`: Latency and API cost reduction comparing Multimodal Vision vs Programmatic AST verification loops.

## Dataset Usage

The dataset can be queried directly via SQLite (`data/conceptcast.db`), inspected via the structured CSV reports in `reports/evaluation/`, or visualized using the graphic files in `figures/`.

## Reproducing the Thesis Results

The controlled four-topic benchmark (thesis Tables 5.5 and 5.6) and the historical
compilation table (Table 5.1) are reproduced directly from `data/conceptcast.db`:

```bash
# Controlled benchmark tables 5.5 + 5.6 (36 jobs, provenance sub-counts)
python3 verify_controlled_benchmark.py

# Historical Table 5.1 (74.5% / 92.7%) from the FROZEN 136-job snapshot @5f4f7f5
# NOTE: this must NOT be run against the current data/conceptcast.db, which has
# grown to ~224 jobs / 525 scenes and would yield different numbers.
python3 verify_table51_historical.py

# Regenerate the controlled-outcome figure (Fig 5.5)
python3 ../scripts/generate_controlled_benchmark_figure.py
```

> **Important — historical vs. current database.** `data/conceptcast.db` is the
> grown, live database (224 jobs / ~525 scenes). Thesis Table 5.1 is pinned to the
> frozen **136-job historical snapshot at commit `5f4f7f5`** (275 scenes, 74.5% /
> 92.7%). Querying the current DB directly produces *different* numbers
> (64.6% / 84.8%) that do **not** match the published thesis. To reproduce the
> published table, use `verify_table51_historical.py`, which extracts the frozen
> snapshot from git history.

### Cohort identification

The `jobs` table has no cohort/run column, so the 36 controlled-benchmark jobs are
isolated by the four sequential topic windows defined in
`verify_controlled_benchmark.py` and `../scripts/generate_controlled_benchmark_figure.py`.
These windows must stay in sync with `benchmark-manifest.json` (the authoritative run
start times); see `benchmark-manifest.README.md` for the exact relationship. Provenance
sub-counts (fallback usage, architect transport) are read from each job's `validation`
JSON blob, not from free text.

## License & Attribution

This dataset is released for academic open data reproducibility and public research verification.
