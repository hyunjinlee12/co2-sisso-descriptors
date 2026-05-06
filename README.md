# co2-sisso-descriptors

CO2 conversion catalysis (methanation, RWGS) descriptor discovery using **SISSO++**,
based on a literature-curated experimental database.

## Setup (on this server)

SISSO++ binary and `sissopp_env` conda environment are already installed at
`/home/hyunjin/sissopp/` and `/home/hyunjin/.conda/envs/sissopp_env/`. Activate them with:

```bash
source scripts/activate_sisso.sh
```

This loads `intel/oneapi/2023.0.0` (MPI + MKL) and activates `sissopp_env`.

Verify:
```bash
sisso++ --help
python -c "import sissopp; print(sissopp.__file__)"
```

Then enable the pre-commit hooks once:
```bash
pre-commit install
```

## Setup (on a fresh machine)

1. Build SISSO++ — see https://sissopp_developers.gitlab.io/sissopp/
2. Create the Python env: `conda env create -f environment.yml`

## Workflow

1. Collect literature data → `data/raw/`
2. `python -m thermo_co2.ingest` → `data/processed/db.csv`
3. `python -m thermo_co2.features` → SISSO inputs in `sisso/<reaction>/`
4. `sisso++ sisso/<reaction>/sisso.json` → SISSO outputs
5. `python -m thermo_co2.postprocess` → `results/`

`make help` lists Make targets.

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
| `scripts/` | shell helpers (activation, etc.) |
| `docs/references.bib` | citations |
