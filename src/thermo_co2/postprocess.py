"""Collect SISSO outputs, run leave-one-out validation, and produce final tables.

Cross-validation strategies (proposal §9):
    - leave-one-material-out
    - leave-one-support-out
    - leave-one-family-out

Outputs are written to ``results/{figures,tables}/``.

Stub — to be implemented after the first SISSO run produces real outputs.
"""

from __future__ import annotations

from pathlib import Path

RESULTS_DIR = Path("results")


def collect_models(reaction: str) -> dict:
    """Parse ``sisso/<reaction>/<task>/SISSO.out`` files into a structured dict."""
    raise NotImplementedError


def loo_cv(strategy: str = "material") -> None:
    """Run leave-one-X-out validation and save metrics to results/tables."""
    raise NotImplementedError


def make_figures() -> None:
    """Produce parity plots, descriptor importance maps, etc."""
    raise NotImplementedError


def main() -> None:
    raise NotImplementedError


if __name__ == "__main__":
    main()
