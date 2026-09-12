#!/usr/bin/env python3
"""One command → full derived dataset + thesis-ready summary tables.

Pipeline: db_query.py (outcomes) + traces_agg.py (tokens/latency/cost) →
markdown summary tables in reports/summary.md, all recomputed from raw data.

Usage:
  python3 scripts/summarize.py            # full pipeline + summary.md
"""
from __future__ import annotations

import subprocess
import sys
from pathlib import Path

REPO = Path(__file__).resolve().parent.parent
SCRIPTS = Path(__file__).parent
DERIVED = REPO / "reports" / "derived"


def run(script: str, *args: str) -> None:
    r = subprocess.run(
        [sys.executable, str(SCRIPTS / script), *args],
        capture_output=True,
        text=True,
        timeout=300,
    )
    if r.returncode != 0:
        print(f"WARN: {script} {' '.join(args)} failed:\n{r.stderr}", file=sys.stderr)


def md_table(rows: list[dict], title: str) -> str:
    if not rows:
        return f"## {title}\n\n(no data)\n"
    cols = list(rows[0].keys())
    lines = [f"## {title}", "", "| " + " | ".join(cols) + " |", "|" + "---|" * len(cols)]
    for r in rows:
        lines.append("| " + " | ".join(str(r.get(c, "")) for c in cols) + " |")
    return "\n".join(lines) + "\n"


def main() -> None:
    # 1. Outcomes by arm (or whatever dims the manifest has).
    run("db_query.py", "--by", "arm", "--metric", "status", "--format", "csv")
    run("db_query.py", "--by", "arm", "model", "--metric", "status", "--format", "csv")
    run("db_query.py", "--by", "topic", "arm", "--metric", "status", "--format", "csv")
    # 2. Trace measures if traces exist.
    run("traces_agg.py", "--by", "arm", "stage", "--format", "csv")
    run("traces_agg.py", "--by", "arm", "model", "--format", "csv")
    # 3. Charts.
    run("charts.py")

    # 4. Summary markdown from whatever derived CSVs exist (one section per file).
    sections: list[str] = ["# Benchmark v2 Summary", "", "All numbers recomputed from raw data at report time.", ""]
    import csv

    for p in sorted(DERIVED.glob("*.csv")):
        with p.open(newline="") as f:
            rows = list(csv.DictReader(f))
        title = p.stem.replace("_", " ").replace("db query ", "").replace("traces agg ", "")
        sections.append(md_table(rows, title))

    out = REPO / "reports" / "summary.md"
    out.write_text("\n".join(sections))
    print(f"summary → {out}")


if __name__ == "__main__":
    main()
