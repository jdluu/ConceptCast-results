#!/usr/bin/env python3
"""Generic SQLite query/aggregate CLI for the benchmark database.

Introspects the schema — no table or column names are hardcoded beyond the
two known tables (jobs, thoughts). Group-by dimensions and metrics are chosen
at invocation time.

Usage:
  # status counts per arm (arm comes from the manifest join)
  python3 scripts/db_query.py --by arm --metric status

  # mean execution time per model
  python3 scripts/db_query.py --by model --metric total_execution_time --agg mean

  # raw rows for one dimension value
  python3 scripts/db_query.py --by topic --where "arm=C" --format csv

  # print available columns
  python3 scripts/db_query.py --schema
"""
from __future__ import annotations

import argparse
import json
import sqlite3
import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).parent))
from common import DB_PATH, OUT_DIR, Manifest, open_db, provenance, save_json, table_columns, write_csv  # noqa: E402

AGGS = {
    "count": None,  # special: counts rows per group
    "mean": lambda xs: sum(xs) / len(xs) if xs else None,
    "sum": sum,
    "min": min,
    "max": max,
    "median": lambda xs: sorted(xs)[len(xs) // 2] if xs else None,
}


def main() -> None:
    ap = argparse.ArgumentParser(description=__doc__)
    ap.add_argument("--db", type=Path, default=DB_PATH)
    ap.add_argument("--by", nargs="*", default=[], help="group-by dimensions: manifest columns (arm, rep, topic, model) and/or jobs table columns (status, model_id, ...)")
    ap.add_argument("--metric", default=None, help="jobs column to aggregate (with --agg) or just include per group (with --agg count, e.g. status)")
    ap.add_argument("--agg", default="count", choices=list(AGGS), help="aggregation: count (tally metric values) or mean/sum/min/max/median (numeric metric)")
    ap.add_argument("--where", default=None, help='sqlite WHERE clause on jobs columns, e.g. "status=\'completed\'"')
    ap.add_argument("--format", choices=["table", "csv", "json"], default="table")
    ap.add_argument("--schema", action="store_true", help="print jobs/thoughts columns and manifest dimensions, then exit")
    args = ap.parse_args()

    manifest = Manifest.load()
    conn = open_db(args.db)
    jobs_cols = table_columns(conn, "jobs")

    if args.schema:
        print("jobs columns:", ", ".join(jobs_cols))
        print("thoughts columns:", ", ".join(table_columns(conn, "thoughts")))
        print("manifest dimensions:", ", ".join(manifest.columns()))
        return

    # Resolve --by entries: manifest dims vs jobs columns.
    manifest_dims = [d for d in args.by if d in manifest.columns()]
    job_dims = [d for d in args.by if d in jobs_cols]
    unknown = [d for d in args.by if d not in manifest_dims and d not in job_dims]
    if unknown:
        sys.exit(f"unknown --by dimensions (not in manifest or jobs): {unknown}")
    if not args.by:
        sys.exit("nothing to do: pass --by with at least one dimension (see --schema)")

    # Pull jobs rows (only needed columns) and join manifest dims on (topic, model_id).
    select_cols = sorted(set(job_dims) | ({args.metric} if args.metric and args.agg != "count" else set()) | ({"status"} if args.metric == "status" else set()))
    where = f"WHERE {args.where}" if args.where else ""
    rows = conn.execute(
        f"SELECT {', '.join(select_cols) if select_cols else 'job_id'} FROM jobs {where}"
    ).fetchall()
    idx = {c: i for i, c in enumerate(select_cols)}

    # Manifest lookup. Preferred join: jobs.benchmark_job_seq == manifest.job_seq (exact, unambiguous).
    # Fallback join: (topic, model_id) — ambiguous when reps exist; unresolved rows are labeled '?'.
    seq_col = "benchmark_job_seq" if "benchmark_job_seq" in jobs_cols else None
    by_seq: dict[str, dict] = {r["job_seq"]: r for r in manifest.rows}
    m_index: dict[tuple[str, str], list[dict]] = {}
    for r in manifest.rows:
        m_index.setdefault((r["topic"].strip().lower(), r["model"]), []).append(r)

    # Simpler: re-query topic+model_id for the join if not already selected.
    need_join_cols = [c for c in ("topic", "model_id", seq_col or "") if c and c not in idx]
    if manifest_dims and (need_join_cols or seq_col is None):
        if need_join_cols:
            sel = select_cols + need_join_cols
            rows = conn.execute(
                f"SELECT {', '.join(sel)} FROM jobs {where}"
            ).fetchall()
            idx = {c: i for i, c in enumerate(sel)}

    ambiguous = 0
    # Group.
    groups: dict[tuple, list] = {}
    for row in rows:
        mdims: dict[str, str] = {}
        if manifest_dims:
            if seq_col is not None:
                seq = str(row[idx[seq_col]])
                m = by_seq.get(seq)
                if m is not None:
                    mdims = {d: m[d] for d in manifest_dims}
                else:
                    ambiguous += 1
            else:
                topic = str(row[idx["topic"]] or "").strip().lower()
                model = str(row[idx["model_id"]] or "").strip()
                cands = m_index.get((topic, model), [])
                if len(cands) == 1:
                    mdims = {d: cands[0][d] for d in manifest_dims}
                elif len(cands) > 1:
                    # rep>1: same (topic, model) appears once per rep. Without a job-level
                    # rep column the join is ambiguous — label as unresolved rather than guess.
                    ambiguous += 1
        key_parts = []
        for d in manifest_dims:
            key_parts.append(mdims.get(d, "?"))
        for d in job_dims:
            key_parts.append(str(row[idx[d]]))
        groups.setdefault(tuple(key_parts), []).append(row)

    if ambiguous:
        print(f"WARN: {ambiguous} job rows had >1 manifest match (topic+model, multiple reps) and no job-level rep column; labeled '?' — add arm/rep columns to the jobs table or match on job_id instead.", file=sys.stderr)

    if args.agg == "count":
        out_rows = []
        for key, grp in sorted(groups.items()):
            rec = dict(zip([*manifest_dims, *job_dims], key))
            if args.metric:
                tally: dict[str, int] = {}
                for row in grp:
                    v = str(row[idx[args.metric]]) if args.metric in idx else "?"
                    tally[v] = tally.get(v, 0) + 1
                for v, n in sorted(tally.items()):
                    out_rows.append({**rec, args.metric: v, "count": n})
            else:
                out_rows.append({**rec, "count": len(grp)})
        out = out_rows
    else:
        if not args.metric or args.metric not in idx:
            sys.exit(f"--agg {args.agg} needs a numeric --metric that is a jobs column")
        out_rows = []
        for key, grp in sorted(groups.items()):
            rec = dict(zip([*manifest_dims, *job_dims], key))
            vals = [row[idx[args.metric]] for row in grp if row[idx[args.metric]] is not None]
            rec[f"{args.agg}_{args.metric}"] = round(AGGS[args.agg](vals), 4) if vals else None
            rec["n"] = len(vals)
            out_rows.append(rec)
        out = out_rows

    # Output.
    if args.format == "json":
        payload = provenance(args.db, manifest)
        payload["query"] = {"by": args.by, "metric": args.metric, "agg": args.agg, "where": args.where}
        payload["rows"] = out
        stem = "db_query_" + "_".join(args.by) + (("___" + args.metric) if args.metric else "")
        dest = save_json(OUT_DIR / "derived" / f"{stem}.json", payload)
        print(f"wrote {dest}")
    elif args.format == "csv":
        stem = "db_query_" + "_".join(args.by) + (("___" + args.metric) if args.metric else "")
        dest = write_csv(OUT_DIR / "derived" / f"{stem}.csv", out)
        print(f"wrote {dest}")
    else:
        if not out:
            print("(no rows)")
        cols = list(out[0].keys())
        widths = {c: max(len(c), *(len(str(r.get(c, ""))) for r in out)) for c in cols}
        print("  ".join(c.ljust(widths[c]) for c in cols))
        for r in out:
            print("  ".join(str(r.get(c, "")).ljust(widths[c]) for c in cols))


if __name__ == "__main__":
    main()
