#!/usr/bin/env python3
"""Fold per-call JSONL traces into per-job and per-arm/per-model summaries.

Aggregates whatever numeric fields the traces carry (token counts, latency,
etc.) grouped by whatever dimension fields they carry (arm, model, topic,
stage, attempt). Unknown fields are reported once and ignored; known metric
fields are discovered dynamically from the first file.

Usage:
  python3 scripts/traces_agg.py                    # summary by arm
  python3 scripts/traces_agg.py --by arm,stage     # summary by arm+stage
  python3 scripts/traces_agg.py --by model --format csv
"""
from __future__ import annotations

import argparse
import json
import statistics
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import OUT_DIR, Manifest, iter_trace_records, provenance, save_json, trace_files, trace_fields, write_csv  # noqa: E402

NUMERIC_HINTS = ("tokens", "latency", "cost", "duration", "ms", "_s", "count")
DIM_HINTS = ("arm", "rep", "topic", "model", "stage", "agent_role", "run_id", "job_id")
COST_FIELDS = ("input_tokens", "output_tokens", "reasoning_tokens")


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--traces", type=Path, default=None, help="traces dir (default <repo>/traces)")
    ap.add_argument("--by", nargs="*", default=["arm"], help="dimensions to group by")
    ap.add_argument("--format", choices=["table", "csv", "json"], default="table")
    args = ap.parse_args()

    tf = trace_files(args.traces) if args.traces else trace_files()
    if not tf:
        sys.exit("no trace files found in traces/ (nothing to aggregate yet)")

    records = list(iter_trace_records(tf))
    if not records:
        sys.exit("traces contain no parseable records")
    fields = trace_fields([rec for _, rec in records])

    dims = [d for d in args.by if d in fields]
    missing = [d for d in args.by if d not in fields]
    if missing:
        print(f"WARN: trace records lack dimension(s) {missing}; ignoring", file=sys.stderr)
    if not dims:
        sys.exit("no valid group dimensions in traces")

    # Discover numeric metric fields.
    metrics = [f for f in fields if f not in dims and any(h in f.lower() for h in NUMERIC_HINTS)]

    groups: dict[tuple, list[dict]] = {}
    for _, rec in records:
        key = tuple(str(rec.get(d, "?")) for d in dims)
        groups.setdefault(key, []).append(rec)

    out_rows = []
    for key in sorted(groups):
        grp = groups[key]
        rec: dict = dict(zip(dims, key))
        rec["calls"] = len(grp)
        for m in metrics:
            vals = [r[m] for r in grp if isinstance(r.get(m), (int, float))]
            if vals:
                rec[f"{m}.total"] = round(sum(vals), 2)
                rec[f"{m}.mean"] = round(statistics.fmean(vals), 2)
                if len(vals) >= 2:
                    rec[f"{m}.p95"] = round(sorted(vals)[int(len(vals) * 0.95) - 1], 2)
        out_rows.append(rec)

    # Optional cost model: price-per-Mtok from a simple JSON if present.
    prices_path = Path(__file__).parent / "pricing.json"
    if prices_path.exists() and all(f in fields for f in COST_FIELDS):
        prices = json.loads(prices_path.read_text())
        for row in out_rows:
            row["modeled_cost"] = round(
                sum(
                    row.get(f"{f}.total", 0) / 1e6 * prices.get(f, 0.0)
                    for f in COST_FIELDS
                ),
                4,
            )

    prov = provenance(manifest=Manifest.load() if Path("manifest/jobs.csv").exists() else None)
    stem = "traces_agg_" + "_".join(dims)
    if args.format == "json":
        dest = save_json(OUT_DIR / "derived" / f"{stem}.json", {**prov, "by": dims, "rows": out_rows})
        print(f"wrote {dest}")
    elif args.format == "csv":
        dest = write_csv(OUT_DIR / "derived" / f"{stem}.csv", out_rows)
        print(f"wrote {dest}")
    else:
        if not out_rows:
            print("(no rows)")
            return
        cols = [c for c in out_rows[0] if c not in ("trace_files",)]
        widths = {c: max(len(c), *(len(str(r.get(c, ""))) for r in out_rows)) for c in cols}
        print("  ".join(c.ljust(widths[c]) for c in cols))
        for r in out_rows:
            print("  ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols))
        print(f"\n({len(records)} calls from {len(tf)} files; dims={dims}; metrics={metrics})")


if __name__ == "__main__":
    main()
