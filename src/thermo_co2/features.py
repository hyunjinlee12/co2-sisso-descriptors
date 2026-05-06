"""Build SISSO input matrices from the canonical database.

For each reaction (methanation, RWGS), the pipeline:

1. reads ``data/processed/db.csv``
2. computes derived columns (log_STY, wet_dry_ratio, task_T_bin, ...)
3. applies the task split defined in ``sisso/<reaction>/tasks.yaml``
4. writes per-task SISSO input files to ``sisso/<reaction>/``

Stub — implement once the seed DB has enough rows to test the pipeline.
"""

from __future__ import annotations

from pathlib import Path

import pandas as pd

from .schema import TIER_COLS

SISSO_DIR = Path("sisso")
PROCESSED_DIR = Path("data/processed")


def derive_columns(df: pd.DataFrame) -> pd.DataFrame:
    """Compute log10(STY), wet/dry ratio, and assign task bins."""
    raise NotImplementedError


def select_features(df: pd.DataFrame, tiers: list[str]) -> pd.DataFrame:
    """Subset the DataFrame to identifier + selected tier columns."""
    cols: list[str] = []
    for t in tiers:
        cols.extend(TIER_COLS[t])
    return df[["sample_id", *cols]]


def write_sisso_input(df: pd.DataFrame, reaction: str, target: str) -> Path:
    """Write a SISSO-formatted CSV for one (reaction, target) combination."""
    raise NotImplementedError


def main() -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()
