"""
ETL for Minnesota Solvation Database (MNSOL) tab-delimited exports.

The raw database is licensed by the University of Minnesota; obtain it from
https://comp.chem.umn.edu/mnsol/ and do not redistribute bundled files.

Supports:
- Files with a header row (recommended export / merged SMILES table).
- Headerless ``MNSol_alldata.txt``-style layout per MNSol-v2012 manual (column positions).
"""

from __future__ import annotations

import argparse
import re
from pathlib import Path
from typing import Iterable

import numpy as np
import pandas as pd

# Canonical output columns
OUT_COLS = [
    "entry_id",
    "solute_name",
    "stoichiometric_formula",
    "solute_charge",
    "solvent_name",
    "delta_g_kcal_mol",
    "solvation_type",
    "smiles",
    "epsilon",
    "n_refractive",
    "alpha",
    "beta",
    "gamma",
    "phi2",
    "psi2",
    "beta2",
]

# MNSol v2012 ``MNSol_alldata.txt`` positional layout (0-based indices).
# Manual: entry, file, name, formula, subset, charge, cls1, cls2, cls3, solvent,
#         deltaG (kcal/mol), type abs/rel, then solvent descriptors (8 cols), ...
_MANUAL_POSITION_NAMES = [
    "entry_id",
    "_file_handle",
    "solute_name",
    "stoichiometric_formula",
    "_subset",
    "solute_charge",
    "_solute_class_1",
    "_solute_class_2",
    "_solute_class_3",
    "solvent_name",
    "delta_g_kcal_mol",
    "solvation_type",
    "epsilon",
    "n_refractive",
    "alpha",
    "beta",
    "gamma",
    "phi2",
    "psi2",
    "beta2",
]


def _normalize_header(name: str) -> str:
    s = name.strip().lower()
    s = re.sub(r"\s+", "_", s)
    s = re.sub(r"[^a-z0-9_]", "", s)
    return s


HEADER_ALIASES: dict[str, str] = {
    "database_entry_number": "entry_id",
    "entry": "entry_id",
    "entry_id": "entry_id",
    "id": "entry_id",
    "name_of_the_solute": "solute_name",
    "solute": "solute_name",
    "compound": "solute_name",
    "stoichiometric_formula_of_the_solute": "stoichiometric_formula",
    "formula": "stoichiometric_formula",
    "total_charge_of_the_solute": "solute_charge",
    "charge": "solute_charge",
    "solvent_in_which_the_solvation_free_energy_of_the_solute_is_listed": "solvent_name",
    "solvent": "solvent_name",
    "the_solvation_free_energy_in_kcalmol": "delta_g_kcal_mol",
    "deltag": "delta_g_kcal_mol",
    "dg": "delta_g_kcal_mol",
    "g_solv": "delta_g_kcal_mol",
    "delta_g": "delta_g_kcal_mol",
    "description_of_the_type_of_solvation_free_energy": "solvation_type",
    "type": "solvation_type",
    "smiles": "smiles",
    "canonical_smiles": "smiles",
}


def _rename_from_aliases(df: pd.DataFrame) -> pd.DataFrame:
    out = df.copy()
    mapping = {}
    for c in out.columns:
        key = _normalize_header(str(c))
        if key in HEADER_ALIASES:
            mapping[c] = HEADER_ALIASES[key]
        else:
            mapping[c] = key
    out = out.rename(columns=mapping)
    return out


def _looks_like_header_row(row: pd.Series) -> bool:
    """Heuristic: header row rarely has a parseable float in the delta_G slot."""
    text = " ".join(str(x) for x in row.values[:15] if pd.notna(x))
    if "solvat" in text.lower() or "solvent" in text.lower():
        return True
    # If column 10 (K) is numeric, likely data row
    if len(row) > 10:
        try:
            float(str(row.iloc[10]).replace(",", "."))
            return False
        except (TypeError, ValueError):
            pass
    return True


def load_mnsol_table(path: Path | str, encoding: str = "utf-8", errors: str = "replace") -> pd.DataFrame:
    """Load tab-delimited MNSOL export; tries header first, then positional layout."""
    path = Path(path)
    raw = pd.read_csv(path, sep="\t", dtype=str, encoding=encoding, encoding_errors=errors, header=None)

    if raw.shape[1] < 12:
        raise ValueError(f"Expected at least 12 tab-separated columns; got {raw.shape[1]}")

    first = raw.iloc[0]
    if _looks_like_header_row(first):
        header_vals = [str(x).strip() if pd.notna(x) else f"col_{i}" for i, x in enumerate(first)]
        df = raw.iloc[1:].copy()
        df.columns = header_vals[: df.shape[1]]
        df = _rename_from_aliases(df)
    else:
        ncols = raw.shape[1]
        names = _MANUAL_POSITION_NAMES[: min(len(_MANUAL_POSITION_NAMES), ncols)]
        if ncols > len(names):
            extra = [f"_extra_{i}" for i in range(len(names), ncols)]
            names = names + extra
        df = raw.copy()
        df.columns = names

    return df


def clean_for_modeling(
    df: pd.DataFrame,
    require_smiles: bool = True,
    solvation_types: Iterable[str] | None = ("abs",),
    drop_ionic: bool = False,
) -> pd.DataFrame:
    """Filter rows suitable for ΔG regression."""
    out = df.copy()

    if "delta_g_kcal_mol" not in out.columns:
        raise KeyError("Column delta_g_kcal_mol not found after load/merge.")

    out["delta_g_kcal_mol"] = pd.to_numeric(out["delta_g_kcal_mol"], errors="coerce")
    out = out.dropna(subset=["delta_g_kcal_mol", "solvent_name"])

    if solvation_types is not None and "solvation_type" in out.columns:
        st = out["solvation_type"].astype(str).str.lower().str.strip()
        mask = st.isin({s.lower() for s in solvation_types})
        out = out[mask | st.isna()]

    if "solute_charge" in out.columns:
        out["solute_charge"] = pd.to_numeric(out["solute_charge"], errors="coerce").fillna(0)
        if drop_ionic:
            out = out[out["solute_charge"] == 0]

    if require_smiles:
        if "smiles" not in out.columns:
            raise KeyError(
                "SMILES column missing. Merge identifiers from coordinates/SMILES "
                "lookup (see README); export must include a 'smiles' column."
            )
        out = out[out["smiles"].notna() & (out["smiles"].astype(str).str.strip() != "")]

    for c in ["epsilon", "n_refractive", "alpha", "beta", "gamma", "phi2", "psi2", "beta2"]:
        if c in out.columns:
            out[c] = pd.to_numeric(out[c], errors="coerce")

    return out.reset_index(drop=True)


def merge_smiles_table(df: pd.DataFrame, smiles_path: Path | str, on: str = "entry_id") -> pd.DataFrame:
    """Left-merge SMILES from a CSV/TSV with columns ``entry_id`` (or ``on``) and ``smiles``."""
    path = Path(smiles_path)
    sep = "\t" if path.suffix.lower() in {".tsv", ".txt"} else ","
    side = pd.read_csv(path, sep=sep, dtype=str)
    side = _rename_from_aliases(side)
    if on not in df.columns or on not in side.columns:
        raise KeyError(f"Merge key '{on}' must exist in both frames.")
    if "smiles" not in side.columns:
        raise KeyError("smiles_path table must include 'smiles'.")
    return df.merge(side[[on, "smiles"]], on=on, how="left", suffixes=("", "_merged"))


def to_standard_parquet(df: pd.DataFrame, out_path: Path | str) -> None:
    """Write cleaned table with stable column order (missing cols filled with NA)."""
    out = pd.DataFrame()
    for c in OUT_COLS:
        out[c] = df[c] if c in df.columns else np.nan
    out.to_parquet(out_path, index=False)


def run_cli() -> None:
    p = argparse.ArgumentParser(description="MNSOL → cleaned Parquet (UMN license applies to raw data).")
    p.add_argument("input", type=Path, help="Path to MNSol_alldata.txt or merged TSV with header")
    p.add_argument("-o", "--output", type=Path, required=True, help="Output .parquet path")
    p.add_argument("--smiles-merge", type=Path, default=None, help="Optional TSV/CSV with entry_id, smiles")
    p.add_argument("--merge-on", type=str, default="entry_id")
    p.add_argument("--allow-no-smiles", action="store_true", help="Do not require SMILES (ETL only)")
    p.add_argument("--include-rel", action="store_true", help="Include solvation_type != abs")
    args = p.parse_args()

    df = load_mnsol_table(args.input)
    if args.smiles_merge:
        df = merge_smiles_table(df, args.smiles_merge, on=args.merge_on)
    types = None if args.include_rel else ("abs",)
    clean = clean_for_modeling(df, require_smiles=not args.allow_no_smiles, solvation_types=types)
    to_standard_parquet(clean, args.output)
    print(f"Wrote {len(clean)} rows to {args.output}")
