# co2-sisso-descriptors

CO2 conversion catalysis (methanation, RWGS) descriptor discovery using **SISSO**,
based on a literature-curated experimental database.

## Setup

```bash
conda env create -f environment.yml
conda activate co2-sisso
pre-commit install
```

## Workflow

1. Collect literature data → `data/raw/`
2. `python -m thermo_co2.ingest` → `data/processed/db.csv`
3. `python -m thermo_co2.features` → SISSO input files in `sisso/<reaction>/`
4. Run SISSO externally (binary not in this repo)
5. `python -m thermo_co2.postprocess` → `results/`

`make help` lists pipeline targets.

## Layout

| path | purpose |
|---|---|
| `data/raw/` | original literature CSV/Excel (not tracked) |
| `data/processed/` | cleaned & merged DB |
| `data/external/` | Materials Project, NIST, etc. |
| `src/thermo_co2/` | Python source |
| `sisso/<reaction>/` | SISSO inputs/outputs (heavy outputs not tracked) |
| `notebooks/` | exploratory analysis |
| `results/{figures,tables}/` | publication-ready outputs |
| `docs/references.bib` | citations |
