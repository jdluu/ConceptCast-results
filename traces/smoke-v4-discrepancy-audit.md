# Smoke v4 Extended Test — Discrepancy Audit (2026-09-12)

Run: smoke-v4-maxpar | manifest: 5 topics x 10 models x 1 rep = 50 jobs | parallelism 8

## D1. Premature full-run creation (process, fixed)
- The 90-job arm C matrix was created from a stale manifest when the plan was still smoke testing.
- Remediation: cancelled 71 in-flight jobs, wiped arm C records, rebuilt manifest with user's 10-model list.

## D2. Trace run_id attribution is backend-controlled (OPEN, remediate post-run)
- benchmark_council.py "exports" BENCH_RUN_ID, but traces are written by the BACKEND process,
  whose env BENCH_RUN_ID (bench-v2-20260912) wins. Smoke v4 traces land in
  bench-v2-20260912.jsonl, not smoke-v4-maxpar.jsonl.
- Data impact: none — records are complete (job_seq attribution via contextvars verified).
- Remediation: rename file at run end; long-term, have jobs/create pass run_id per-request
  (or backend reads it from job metadata, not process env).

## D3. Intermittent provider 400 "model_not_available" (observed, self-healing)
- nvidia/nemotron-3-ultra-550b-a55b got one 400 model_not_available at the architect stage
  despite being listed in /models and passing direct probes. Orchestrator retry recovered;
  job proceeded to animating. Provider-side capacity issue; no code change needed.

## D4. Model ID alias divergence (fixed)
- User list has bare "gpt-oss-120b"; Nano GPT lists "openai/gpt-oss-120b". Chat endpoint
  accepts both (probed 200 on each). Canonical listed form recorded in model_metadata.json
  with bare id as alias.

## Config sync completed
- results/manifest/model_metadata.json -> 10-model roster with per-model verified date,
  tiers, params, aliases. Pushed to ConceptCast-results repo (commit 8e4a2e1).
- manifest/jobs.csv -> 50 jobs (seqs 1-50). Pushed.

## Pipeline readiness verified
- Backend health: database connected, manim available, storage writable.
- Trace schema: all documented fields present in live records; per-job attribution correct.
- Artifact storage: renders landing in data/jobs/<uuid>/videos/ (fresh mp4s confirmed).
- Retry logic exercised and effective (transient 400 + scene attempt counters).
- Gates: hermes verify --json green; 75 backend tests pass; mypy clean.
