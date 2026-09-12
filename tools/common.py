#!/usr/bin/env python3
"""Shared helpers for benchmark data tooling.

Design rules (see README):
- Nothing about topics, models, arms, or metric values is hardcoded.
- Grouping dimensions come from manifest/jobs.csv joined on (topic, model, arm, rep).
- DB/JSONL schemas are introspected; missing fields become "unavailable",
  never wrong numbers.
- Every output records its inputs (db path, manifest commit, trace file set)
  so results are traceable to a frozen state.
"""
from __future__ import annotations

import csv
import hashlib
import json
import sqlite3
import sys
from dataclasses import dataclass, field
from pathlib import Path

REPO_ROOT = Path(__file__).resolve().parent.parent
MANIFEST = REPO_ROOT / "manifest" / "jobs.csv"
DB_PATH = REPO_ROOT / "data" / "conceptcast.db"
TRACES_DIR = REPO_ROOT / "traces"
OUT_DIR = REPO_ROOT / "reports"


# ---------------------------------------------------------------- manifest ---
@dataclass
class Manifest:
    """The 270-job grid; the authoritative join key for every analysis."""

    rows: list[dict] = field(default_factory=list)

    @classmethod
    def load(cls, path: Path = MANIFEST) -> "Manifest":
        if not path.exists():
            sys.exit(f"manifest not found: {path}")
        with path.open(newline="") as f:
            rows = list(csv.DictReader(f))
        if not rows:
            sys.exit(f"manifest is empty: {path}")
        return cls(rows=rows)

    def columns(self) -> list[str]:
        return list(self.rows[0].keys())

    def dimension_values(self, dim: str) -> list[str]:
        """Distinct values of a manifest dimension, in first-seen order."""
        seen: list[str] = []
        for r in self.rows:
            v = r.get(dim, "")
            if v and v not in seen:
                seen.append(v)
        return seen

    def completed(self) -> list[dict]:
        """Only rows marked completed in the manifest (status field)."""
        return [r for r in self.rows if r.get("status", "pending") == "completed"]


# --------------------------------------------------------------------- db ----
def open_db(path: Path = DB_PATH) -> sqlite3.Connection:
    if not path.exists():
        sys.exit(f"database not found: {path} (run the benchmark first)")
    conn = sqlite3.connect(f"file:{path}?mode=ro", uri=True)
    return conn


def table_columns(conn: sqlite3.Connection, table: str) -> list[str]:
    return [r[1] for r in conn.execute(f"PRAGMA table_info({table})")]


def hash_file(path: Path) -> str:
    h = hashlib.sha256()
    with path.open("rb") as f:
        for chunk in iter(lambda: f.read(65536), b""):
            h.update(chunk)
    return h.hexdigest()[:16]


# ----------------------------------------------------------------- traces ----
def trace_files(traces_dir: Path = TRACES_DIR) -> list[Path]:
    if not traces_dir.exists():
        return []
    return sorted(traces_dir.glob("*.jsonl"))


def iter_trace_records(paths: list[Path]):
    """Yield (source_file, record) for each JSON object in the JSONL files.

    Records failing to parse are counted and reported, never silently dropped.
    """
    for p in paths:
        with p.open() as f:
            for lineno, line in enumerate(f, 1):
                line = line.strip()
                if not line:
                    continue
                try:
                    yield p, json.loads(line)
                except json.JSONDecodeError as e:
                    print(f"WARN: {p.name}:{lineno} unparseable: {e}", file=sys.stderr)


def trace_fields(records) -> list[str]:
    """Union of keys across bare record dicts (order-stable)."""
    seen: list[str] = []
    for rec in records:
        for k in rec:
            if k not in seen:
                seen.append(k)
    return seen


# ----------------------------------------------------------------- output ----
def write_csv(path: Path, rows: list[dict]) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    if not rows:
        path.write_text("")
        return path
    with path.open("w", newline="") as f:
        w = csv.DictWriter(f, fieldnames=list(rows[0].keys()))
        w.writeheader()
        w.writerows(rows)
    return path


def provenance(db_path: Path = DB_PATH, manifest: Manifest | None = None) -> dict:
    """Stamp every generated artifact with the exact inputs it came from."""
    prov: dict = {"generated_by": Path(sys.argv[0]).name}
    if db_path.exists():
        prov["db"] = {"path": str(db_path), "sha256_16": hash_file(db_path)}
    if manifest is not None:
        prov["manifest_rows"] = len(manifest.rows)
        if MANIFEST.exists():
            prov["manifest_sha256_16"] = hash_file(MANIFEST)
    tf = trace_files()
    prov["trace_files"] = [p.name for p in tf]
    return prov


def save_json(path: Path, obj) -> Path:
    path.parent.mkdir(parents=True, exist_ok=True)
    path.write_text(json.dumps(obj, indent=2, sort_keys=True) + "\n")
    return path
