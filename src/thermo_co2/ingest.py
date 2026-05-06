"""Ingest raw literature data files into the canonical database.

The CLI scans ``data/raw/`` for per-paper input files (CSV/Excel/YAML), validates
them against :mod:`thermo_co2.schema`, and writes a merged ``data/processed/db.csv``.
Each input file is expected to provide one or more rows where each row is a
single material-condition pair.

Stub — to be implemented as papers are added.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .schema import ALL_COLS

RAW_DIR = Path("data/raw")
PROCESSED_DIR = Path("data/processed")


def load_paper(path: Path) -> pd.DataFrame:
    """Load a single per-paper file and return a DataFrame in canonical schema."""
    raise NotImplementedError


def merge_all() -> pd.DataFrame:
    """Walk ``data/raw/`` and concatenate every per-paper file."""
    raise NotImplementedError


def write_db(df: pd.DataFrame, path: Path = PROCESSED_DIR / "db.csv") -> None:
    """Write the merged DataFrame in canonical column order."""
    df.reindex(columns=ALL_COLS).to_csv(path, index=False)


def main() -> None:
    df = merge_all()
    write_db(df)


if __name__ == "__main__":
    main()
