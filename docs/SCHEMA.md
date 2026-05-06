# Database column reference

Each row in `data/processed/db.csv` represents **one (catalyst, condition) pair**.
The same material at a different temperature, humidity, or feed composition is a
separate row.

## How to use this document

1. Pick a paper from `docs/references.bib` (or add a new one)
2. Copy `data/raw/_template.csv` to `data/raw/<paper_id>/data.csv`
3. For each (catalyst, condition) the paper reports, add one row
4. Fill the columns you can — leave the rest blank (empty cell, not zero)
5. When ≥1 paper is filled, `python -m thermo_co2.ingest` merges everything

## Priority legend

| Tag | Meaning |
|---|---|
| **M** | **MUST** — SISSO needs this or the row is unusable |
| **R** | **RECOMMENDED** — strongly improves descriptor quality |
| **O** | **OPTIONAL** — fill if reported, otherwise skip |

A row is acceptable if all **M** columns are filled and at least one target is
present. Aim for ≥4 of the 9 Tier-1 columns to be filled per row.

---

## Identifiers (3)

| Column | Pri | Type | Description | Example |
|---|---|---|---|---|
| `sample_id` | M | str | Unique per row. Convention: `<paper_id>.<row_no>` | `RSCAdv-2023-NiCaAl.1` |
| `paper_id` | M | str | Internal short tag (matches the BibTeX key style) | `RSCAdv-2023-NiCaAl` |
| `doi` | M | str | DOI of source paper | `10.1039/D2RA07554G` |

## Protocol metadata (4)

| Column | Pri | Type | Description / Where in paper | Example |
|---|---|---|---|---|
| `protocol_family` | R | str | Group label for samples sharing synthesis–pretreatment–test bundle | `Ni_Ca_Al2O3_DFM` |
| `reaction_mode` | M | enum | `methanation` / `RWGS` / `mixed`. Take from the paper's stated reaction. | `methanation` |
| `catalyst_formula` | M | str | Composition string with loadings if reported | `10%Ni-30%Ca/Al2O3` |
| `support_state` | R | enum | `calcined` / `reduced` / `hydroxylated` / `vacancy-rich`. From the experimental section (final pretreatment state before reaction) | `reduced` |

## Reaction conditions (13)

| Column | Pri | Type | Unit | Description / Where in paper |
|---|---|---|---|---|
| `temperature_C` | M | float | °C | Reaction temperature. If the paper reports a sweep, make one row per T. |
| `pressure_bar` | R | float | bar | Total pressure. 1 atm ≈ 1.013 bar. Convert MPa → bar (1 MPa = 10 bar). |
| `feed_H2_pct` | R | float | mol % | Volume/mol fraction of H2 in the feed (0–100). |
| `feed_CO2_pct` | R | float | mol % | Volume/mol fraction of CO2 in the feed. |
| `feed_CO_pct` | O | float | mol % | Only if CO is co-fed. |
| `feed_H2O_pct` | R | float | mol % | If wet feed; else 0. **This is what makes a row "wet" vs "dry".** |
| `feed_O2_pct` | O | float | mol % | If O2 is co-fed (e.g., realistic flue gas). |
| `feed_inert_pct` | O | float | mol % | Ar / N2 balance. |
| `space_velocity_value` | R | float | — | The number reported (e.g., 30000) |
| `space_velocity_unit` | R | enum | — | `GHSV` (h⁻¹) / `WHSV` (h⁻¹) / `RGSV` (h⁻¹) — match the paper |
| `space_velocity_GHSV_h_per_mL` | O | float | h⁻¹ mL_cat⁻¹ | If you can normalize WHSV/RGSV → GHSV using mass and packing density, fill here |
| `task_T_bin` | M | enum | — | Auto-assigned: `T_200_250` / `T_250_300` / `T_300_350` (methanation) or `T_500_600` / `T_600_700` (RWGS). Leave blank if T is outside these ranges. |
| `task_humidity` | M | enum | — | `dry` if `feed_H2O_pct = 0`, else `wet` |

## Targets (Y) — at least one **M** must be present (11)

| Column | Pri | Type | Unit | Description |
|---|---|---|---|---|
| `X_CO2_pct` | M* | float | % | CO2 conversion. *At least one of `X_CO2_pct`, `S_CH4_pct`/`STY_CH4`, `S_CO_pct`/`STY_CO` must be filled.* |
| `S_CH4_pct` | M* | float | % | CH4 selectivity (methanation). |
| `S_CO_pct` | M* | float | % | CO selectivity (RWGS). |
| `STY_CH4_mmol_g_h` | R | float | mmol g⁻¹ h⁻¹ | Site-time yield of CH4. |
| `STY_CO_mmol_g_h` | R | float | mmol g⁻¹ h⁻¹ | Site-time yield of CO. |
| `log_STY_CH4` | — | float | — | **Computed** — leave blank, ingest computes log10(STY) |
| `log_STY_CO` | — | float | — | **Computed** — leave blank |
| `decay_slope` | O | float | %/cycle | Slope of activity vs cycle number. Fit yourself if a deactivation curve is shown. |
| `retention_50cycle_pct` | O | float | % | Activity remaining at cycle 50 / cycle 1. |
| `wet_dry_ratio` | — | float | — | **Computed** — joins matched dry+wet rows |
| `O2_tolerance_score` | O | float | — | Auxiliary; define if needed (e.g., `S_CH4(O2)/S_CH4(noO2)`) |

## Tier-0 — elemental / compositional (16)

These are **cheap to fill**: the active metal and support are stated in every paper,
and elemental constants come from periodic-table lookups (the ingest pipeline can
auto-fill Z, period, group, electronegativity, etc. from the metal symbol).

| Column | Pri | Type | Unit | Description |
|---|---|---|---|---|
| `active_metal` | M | str | — | Element symbol of main active metal (`Ni`, `Co`, `Fe`, `Ru`, ...). |
| `active_metal_loading_wt_pct` | R | float | wt% | From experimental section. |
| `active_metal_Z` | O | int | — | Auto-filled from `active_metal` |
| `active_metal_period` | O | int | — | Auto-filled |
| `active_metal_group` | O | int | — | Auto-filled |
| `active_metal_electroneg_pauling` | O | float | — | Auto-filled |
| `active_metal_IE_eV` | O | float | eV | First ionization energy. Auto-filled |
| `active_metal_atomic_radius_pm` | O | float | pm | Auto-filled |
| `active_metal_d_band_center_eV` | O | float | eV | Look up from literature; element-only value, not catalyst-specific |
| `support_class` | M | str | — | `Al2O3` / `CeO2` / `ZrO2` / `MgO` / `SiO2` / `SBA-15` / `TiO2` / `CaO` / ... |
| `support_band_gap_eV` | O | float | eV | Look-up table value, not paper-specific |
| `support_basicity_class` | R | enum | — | `acidic` / `amphoteric` / `basic` |
| `sorbent` | R | str | — | CO2-sorbent component if present (CaO, MgO, none) |
| `sorbent_loading_wt_pct` | R | float | wt% | If DFM-style |
| `promoter` | O | str | — | `Mn`, `K`, `La`, `none` |
| `promoter_loading_wt_pct` | O | float | wt% | If a promoter is added |

## Tier-1 — experimental characterisation (9)

Found in characterisation tables/figures. Fill ≥4 of these per row if possible.

| Column | Pri | Type | Unit | Description / Where in paper |
|---|---|---|---|---|
| `BET_m2_g` | R | float | m² g⁻¹ | BET surface area, characterisation table |
| `pore_volume_cm3_g` | R | float | cm³ g⁻¹ | BJH or t-plot pore volume |
| `metal_particle_size_nm` | R | float | nm | TEM-derived average; if XRD-derived (Scherrer) note in `notes` |
| `TPR_main_peak_C` | R | float | °C | Main reduction peak (most prominent) |
| `TPD_CO2_uptake_mmol_g` | R | float | mmol g⁻¹ | Total CO2 uptake from TPD |
| `XPS_metal_BE_eV` | O | float | eV | Binding energy of dominant metal 2p / 3d peak |
| `XPS_metal_oxidation_state` | O | float | — | If reported (e.g., 0 for metallic Ni, 2 for NiO; can be fractional from deconvolution) |
| `DRIFTS_carbonate_intensity_a_u` | O | float | a.u. | Integrated carbonate band intensity if reported |
| `EXAFS_M_M_coord` | O | float | — | First-shell M-M coordination number |

## Tier-2 — DFT primary features (10)

Fill **only if the paper reports DFT**. Otherwise leave blank — Tier-2 will be
filled later by your own DFT calculations driven by the project's DFT axis.

| Column | Pri | Type | Unit | Description |
|---|---|---|---|---|
| `dG_CO2_ads_eV` | O | float | eV | ΔG of CO2 adsorption |
| `dG_H2O_ads_eV` | O | float | eV | ΔG of H2O adsorption |
| `dG_COOH_eV` | O | float | eV | ΔG of carboxyl intermediate |
| `dG_HCOO_eV` | O | float | eV | ΔG of formate intermediate |
| `dG_CO_ads_eV` | O | float | eV | ΔG of CO adsorption |
| `dG_OH_ads_eV` | O | float | eV | ΔG of OH adsorption |
| `dG_H_ads_eV` | O | float | eV | ΔG of H adsorption |
| `E_O_vacancy_eV` | O | float | eV | Oxygen vacancy formation energy on the support |
| `E_H_spillover_barrier_eV` | O | float | eV | H spillover from metal → support |
| `metal_support_adhesion_eV` | O | float | eV | Adhesion / binding of metal cluster on support |

## Tier-3 — operando / in-situ (5)

| Column | Pri | Type | Unit | Description |
|---|---|---|---|---|
| `drifts_carbonate_peak_cm1` | O | float | cm⁻¹ | Position of dominant carbonate peak |
| `drifts_formate_peak_cm1` | O | float | cm⁻¹ | Position of dominant formate peak |
| `drifts_carbonyl_peak_cm1` | O | float | cm⁻¹ | Adsorbed CO band |
| `in_situ_XAS_oxidation_state` | O | float | — | If reported under reaction conditions |
| `in_situ_XAS_coordination_number` | O | float | — | First-shell CN under reaction conditions |

## Quality / provenance (3)

| Column | Pri | Type | Description |
|---|---|---|---|
| `uncertainty_tag` | M | enum | `digitized` (read off chart) / `direct_text` (number in text/table) / `internal_experiment` (own data) |
| `data_quality_score` | R | int | 1 (digitized chart, low confidence) → 5 (own measurement, high confidence). Use 3 for text-table values, 4 for clear table values, 2 for chart digitization. |
| `notes` | O | str | Free-form caveats: "STY computed assuming ρ=1 g/mL", "T outside current bins", "deactivation curve nonlinear", etc. |

---

## Required minimum per row

To be usable for SISSO, a row must have:

- All identifiers (`sample_id`, `paper_id`, `doi`)
- `reaction_mode`, `catalyst_formula`, `temperature_C`
- `task_T_bin` and `task_humidity` (auto-derivable but please set)
- `active_metal`, `support_class`
- At least **one** target column (X_CO2 OR S_CH4/STY_CH4 OR S_CO/STY_CO)
- `uncertainty_tag`

Anything else is a bonus that improves descriptor quality.
