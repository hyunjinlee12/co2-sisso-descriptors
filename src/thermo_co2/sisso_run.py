"""Wrapper around the ``sisso++`` binary and the ``sissopp`` Python module.

Reads ``sisso/<reaction>/tasks.yaml``, materialises one SISSO input file per
task, runs SISSO++, and collects the resulting models.

Stub — to be implemented after :mod:`thermo_co2.features` is in place.
"""

from __future__ import annotations

from pathlib import Path

SISSO_DIR = Path("sisso")


def run_reaction(reaction: str) -> None:
    """Run MT-SISSO for one reaction (methanation | RWGS)."""
    raise NotImplementedError


def main() -> None:
    for reaction in ("methanation", "rwgs"):
        run_reaction(reaction)


if __name__ == "__main__":
    main()
