"""Column schema for the CO2-conversion literature database.

Each row represents ONE catalyst-condition pair (the same material at a different
temperature, humidity, or feed composition is a separate row). Columns are grouped
by tier so that descriptor blocks can be enabled or disabled independently:

    Tier-0  elemental properties (always cheap to fill)
    Tier-1  experimental characterisation (BET, TEM, TPR, TPD, XPS, ...)
    Tier-2  DFT primary features (adsorption energies, vacancy energies, ...)
    Tier-3  operando spectroscopy (DRIFTS, XAS, ...)

The :data:`ALL_COLS` list is the canonical column order for ``data/processed/db.csv``.
"""

from __future__ import annotations

# ---------------------------------------------------------------------------
# Identifiers
# ---------------------------------------------------------------------------
IDENTIFIER_COLS = [
    "sample_id",  # unique per material-condition pair, e.g. "TR-01.1"
    "paper_id",  # internal short tag, e.g. "JACS-2024-CoSBA"
    "doi",
]

# ---------------------------------------------------------------------------
# Protocol metadata
# ---------------------------------------------------------------------------
PROTOCOL_COLS = [
    "protocol_family",  # synthesis-pretreatment-test bundle id
    "reaction_mode",  # methanation | RWGS | mixed
    "catalyst_formula",  # e.g. "10%Ni-30%Ca/Al2O3"
    "support_state",  # calcined | reduced | hydroxylated | vacancy-rich
]

# ---------------------------------------------------------------------------
# Reaction conditions (always explicit, never hidden background)
# ---------------------------------------------------------------------------
CONDITION_COLS = [
    "temperature_C",
    "pressure_bar",
    "feed_H2_pct",
    "feed_CO2_pct",
    "feed_CO_pct",
    "feed_H2O_pct",
    "feed_O2_pct",
    "feed_inert_pct",
    "space_velocity_value",
    "space_velocity_unit",  # GHSV | WHSV | RGSV
    "space_velocity_GHSV_h_per_mL",  # normalized to GHSV (h^-1 mL_cat^-1)
    "task_T_bin",  # T_200_250 | T_250_300 | T_300_350 | T_500_600 | T_600_700
    "task_humidity",  # dry | wet
]

# ---------------------------------------------------------------------------
# Targets (Y)
# ---------------------------------------------------------------------------
TARGET_COLS = [
    "X_CO2_pct",  # CO2 conversion
    "S_CH4_pct",  # CH4 selectivity
    "S_CO_pct",  # CO selectivity
    "STY_CH4_mmol_g_h",
    "STY_CO_mmol_g_h",
    "log_STY_CH4",  # log10 of STY_CH4 (computed)
    "log_STY_CO",  # log10 of STY_CO  (computed)
    "decay_slope",  # k_d for activity loss vs cycle / time
    "retention_50cycle_pct",
    "wet_dry_ratio",  # performance ratio at matched T (computed)
    "O2_tolerance_score",  # auxiliary, defined in proposal §6
]

# ---------------------------------------------------------------------------
# Tier-0 — elemental / compositional features
# ---------------------------------------------------------------------------
TIER0_ELEMENTAL_COLS = [
    "active_metal",  # Ni | Co | Fe | ...
    "active_metal_loading_wt_pct",
    "active_metal_Z",
    "active_metal_period",
    "active_metal_group",
    "active_metal_electroneg_pauling",
    "active_metal_IE_eV",
    "active_metal_atomic_radius_pm",
    "active_metal_d_band_center_eV",
    "support_class",  # Al2O3 | CeO2 | ZrO2 | MgO | SBA-15 | CaO | TiO2 | ...
    "support_band_gap_eV",
    "support_basicity_class",  # acidic | amphoteric | basic
    "sorbent",  # CaO | MgO | none
    "sorbent_loading_wt_pct",
    "promoter",  # Mn | K | Ca | none
    "promoter_loading_wt_pct",
]

# ---------------------------------------------------------------------------
# Tier-1 — experimental characterisation
# ---------------------------------------------------------------------------
TIER1_EXP_COLS = [
    "BET_m2_g",
    "pore_volume_cm3_g",
    "metal_particle_size_nm",
    "TPR_main_peak_C",
    "TPD_CO2_uptake_mmol_g",
    "XPS_metal_BE_eV",
    "XPS_metal_oxidation_state",
    "DRIFTS_carbonate_intensity_a_u",
    "EXAFS_M_M_coord",
]

# ---------------------------------------------------------------------------
# Tier-2 — DFT primary features (interface-aware, see proposal §5)
# ---------------------------------------------------------------------------
TIER2_DFT_COLS = [
    "dG_CO2_ads_eV",
    "dG_H2O_ads_eV",
    "dG_COOH_eV",
    "dG_HCOO_eV",
    "dG_CO_ads_eV",
    "dG_OH_ads_eV",
    "dG_H_ads_eV",
    "E_O_vacancy_eV",
    "E_H_spillover_barrier_eV",
    "metal_support_adhesion_eV",
]

# ---------------------------------------------------------------------------
# Tier-3 — operando / in-situ spectroscopy
# ---------------------------------------------------------------------------
TIER3_OPERANDO_COLS = [
    "drifts_carbonate_peak_cm1",
    "drifts_formate_peak_cm1",
    "drifts_carbonyl_peak_cm1",
    "in_situ_XAS_oxidation_state",
    "in_situ_XAS_coordination_number",
]

# ---------------------------------------------------------------------------
# Quality / provenance tags
# ---------------------------------------------------------------------------
QUALITY_COLS = [
    "uncertainty_tag",  # digitized | direct_text | internal_experiment
    "data_quality_score",  # 1=low (digitized chart), 5=high (own measurement)
    "notes",
]

# ---------------------------------------------------------------------------
# Canonical column order
# ---------------------------------------------------------------------------
ALL_COLS: list[str] = (
    IDENTIFIER_COLS
    + PROTOCOL_COLS
    + CONDITION_COLS
    + TARGET_COLS
    + TIER0_ELEMENTAL_COLS
    + TIER1_EXP_COLS
    + TIER2_DFT_COLS
    + TIER3_OPERANDO_COLS
    + QUALITY_COLS
)

TIER_COLS: dict[str, list[str]] = {
    "tier0": TIER0_ELEMENTAL_COLS,
    "tier1": TIER1_EXP_COLS,
    "tier2": TIER2_DFT_COLS,
    "tier3": TIER3_OPERANDO_COLS,
}

# ---------------------------------------------------------------------------
# Controlled vocabularies
# ---------------------------------------------------------------------------
REACTION_MODES = {"methanation", "RWGS", "mixed"}
SUPPORT_STATES = {"calcined", "reduced", "hydroxylated", "vacancy-rich"}
TASK_T_BINS = {
    "methanation": ("T_200_250", "T_250_300", "T_300_350"),
    "RWGS": ("T_500_600", "T_600_700"),
}
TASK_HUMIDITY = {"dry", "wet"}
UNCERTAINTY_TAGS = {"digitized", "direct_text", "internal_experiment"}
