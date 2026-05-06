# co2-sisso-descriptors

CO2 conversion catalysis (methanation, RWGS) descriptor discovery using **SISSO++**,
based on a literature-curated experimental database. See `docs/proposal.md` (TBD) for
the underlying research plan.

## Setup (on this server)

SISSO++ binary and `sissopp_env` conda environment are already installed at
`/home/hyunjin/sissopp/` and `/home/hyunjin/.conda/envs/sissopp_env/`. Activate them with:

```bash
source scripts/activate_sisso.sh
```

This loads `intel/oneapi/2023.0.0` (MPI + MKL), activates `sissopp_env`, and prepends
the `sisso++` binary to PATH.

Verify:
```bash
make check
```

Enable pre-commit hooks once:
```bash
pre-commit install
```

## Setup (on a fresh machine)

1. Build SISSO++ — see https://sissopp_developers.gitlab.io/sissopp/
2. `conda env create -f environment.yml`

## Database design

Each row in `data/processed/db.csv` is **one catalyst-condition pair** (the same
material at a different temperature, humidity, or feed is a separate row).
Schema: `src/thermo_co2/schema.py` (74 columns, grouped by tier).

| group | purpose |
|---|---|
| identifiers | sample_id, paper_id, doi |
| protocol | reaction_mode, catalyst_formula, support_state, ... |
| conditions | T, P, feed composition, GHSV, task_T_bin, task_humidity |
| targets | X_CO2, S_CH4, S_CO, STY, retention_50cycle, ... |
| Tier-0 elemental | active metal Z / electroneg / d-band / support class / sorbent / promoter |
| Tier-1 experimental | BET, particle size, TPR, TPD, XPS, DRIFTS, EXAFS |
| Tier-2 DFT | ΔG of CO2*, H2O*, COOH*, HCOO*, CO*, OH*, H*, vacancy energy, adhesion |
| Tier-3 operando | DRIFTS / in-situ XAS peaks |
| quality | uncertainty_tag, data_quality_score, notes |

Files:
- `data/processed/db_template.csv` — empty header-only template (74 columns)
- `data/processed/db_seed.csv` — 8 reference rows (TR-01..TR-08) seeded from
  the proposal's §8 paper list; only fields stated in the proposal are filled,
  the rest is for the user to extract from full text / SI

## Workflow

1. **For each paper**:
   - Copy `data/raw/_template.csv` → `data/raw/<paper_id>/data.csv`
   - Read column meanings in [`docs/SCHEMA.md`](docs/SCHEMA.md) — each column shows
     priority (M / R / O), unit, and where to find it in a typical paper
   - Add one row per (catalyst, condition) pair the paper reports
   - Raw files are not tracked by git; the template is
2. `python -m thermo_co2.ingest` → merges `data/raw/` into `data/processed/db.csv`
3. `python -m thermo_co2.features` → applies task split from
   `sisso/<reaction>/tasks.yaml` and writes per-task SISSO inputs
4. `python -m thermo_co2.sisso_run` → runs MT-SISSO via `sisso++`
5. `python -m thermo_co2.postprocess` → leave-one-X-out validation, figures,
   tables in `results/`

`make help` lists Make targets.

## MT-SISSO task split (proposal §6)

| reaction | T-bin | humidity |
|---|---|---|
| methanation | T_200_250 / T_250_300 / T_300_350 | dry / wet |
| RWGS | T_500_600 / T_600_700 | dry / wet |

Configured in `sisso/methanation/tasks.yaml` and `sisso/rwgs/tasks.yaml`.
Initial complexity: Q=2, D=2 (rung 2, 2-D model). Increase once ≥100 rows are
available across tasks.

## Layout

| path | purpose |
|---|---|
| `data/raw/` | original literature CSV/Excel (not tracked) |
| `data/processed/` | cleaned & merged DB + template + seed |
| `data/external/` | Materials Project, NIST, etc. |
| `src/thermo_co2/` | Python source — schema, ingest, features, sisso_run, postprocess |
| `sisso/<reaction>/` | SISSO inputs/outputs + tasks.yaml |
| `notebooks/` | exploratory analysis |
| `results/{figures,tables}/` | publication-ready outputs |
| `scripts/activate_sisso.sh` | environment activation |
| `docs/references.bib` | citations matching proposal refs [1]–[15] |
