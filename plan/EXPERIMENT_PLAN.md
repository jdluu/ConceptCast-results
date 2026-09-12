# Pre-registration: Experiment plan (draft — finalize before run 1)

This file MUST be committed before the first benchmark job runs. After the run
starts it is immutable; any deviation must be documented in `DEVIATIONS.md`.

## 1. Hypotheses

- H1: Arm C (council) achieves higher E2E video-completion rate than Arm A
  (monolithic) across models and topics.
- H2: Arm B (monolithic + repair) captures a substantial share of C's
  improvement, isolating the contribution of deterministic repair tooling vs.
  decomposition/orchestration (B vs C).
- H3: Cost-per-successful-video and tokens-per-successful-video are reported as
  trade-offs, not assumed improvements.

## 2. Conditions

### Arm A — Monolithic
Single LLM call per job: topic prompt → complete Manim script. No GCO, no AST
validation, no docs retrieval, no repair loop, no retries (infrastructure
retries only).

### Arm B — Monolithic + repair
Same generation as A, then the SAME AST validator + search-and-replace diff
repair used by C operates on the full script. Bounded at 10 repair attempts
(matching C's per-scene bound). Repair prompt structure, temperature, and
validator identical to C.

### Arm C — Council
The ConceptCast pipeline unchanged (planning → architecting → animating →
rendering, GCO, per-scene generation, docs retrieval, bounded retries at the
same configured limits as the frozen framework commit).

## 3. Parity statement

- Identical topic prompt strings across arms (committed under manifest/).
- Identical sampling parameters across arms: temperature 0, seed recorded,
  echoed provider parameters logged per call.
- Identical model roster, provider gateway, max-token policy.
- Arms interleaved in execution order; no arm runs to completion before the
  next begins.
- Infrastructure vs generation retries distinguished at the trace level.
- Framework code frozen at tag `<TBD>` before run 1.

## 4. Outcome taxonomy (per job)

- `completed` — terminal completed state with video artifact, no deterministic
  fallback in the storyboard provenance
- `fallback-completed` — video artifact produced, but architect fallback /
  recovery engaged (not a clean model success)
- `failed` — exhausted generation or render attempts
- `infrastructure-failed` — provider/API interruption prevented completion
  (never attributed to the model)

Comparison unit: one rendered educational video per (topic, model, arm, rep).
Scene-level first-pass rates (C) and script-level first-pass rates (A/B) are
reported in separate tables with units stated in captions.

## 5. Metrics

Per arm × model × topic:
- E2E completion rate (primary)
- First-pass compile rate (with unit)
- Post-repair success rate
- Attempts per success
- Total tokens (input / output / reasoning, separated) per job and per success
- Wall-time latency (median / p95), per-call latency
- Modeled cost per job and per successful video

## 6. Trace schema (per-call JSONL, append-only)

```json
{"ts": "...", "run_id": "...", "arm": "A|B|C", "rep": 1, "topic": "...",
 "stage": "plan|architect|animate|repair|generate", "attempt": 1,
 "model": "...", "job_seq": 1, "benchmark_job_seq": 1,
 "prompt_sha256": "...", "prompt_chars": 0, "response_sha256": "...",
 "input_tokens": 0, "cache_write_tokens": 0, "cache_read_tokens": 0,
 "output_tokens": 0, "details": {}, "requests": 0, "tool_calls": 0,
 "latency_ms": 0.0, "temperature": 0.0, "error": null}
```

Reasoning-token accounting: provider-reported reasoning tokens surface in
`details` (provider-specific keys); the aggregation tools sum them separately
from `input_tokens`/`output_tokens` and never conflate them.

Audience parameter: removed from the framework entirely (commit e7ff72a) —
prompts contain no audience field; arms cannot diverge on it.

## 7. Execution order

1. Instrument `streaming.py` (per-call JSONL) + pin temperature/seed.
2. Smoke test: 1 model × 1 topic × 3 arms.
3. Full run: 270 jobs from `manifest/jobs.csv`, interleaved, PARALLELISM=4,
   resumable (completed tuples skipped on restart).
4. Freeze: SQLite snapshot + traces + manifest committed and tagged.
5. Verification: `verify/` script recomputes every reported number.

## 8. Declared fallback

If the 270-job budget proves infeasible: n=2 for arms A and B, n=1 for arm C
(180 jobs). Must be declared here BEFORE run 1, not retroactively.
