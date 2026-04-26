"""Molecular features: Morgan fingerprint (solute) + solvent descriptor vector."""

from __future__ import annotations

import numpy as np
import pandas as pd
from rdkit import DataStructs
from rdkit.Chem import AllChem
from rdkit import Chem

SOLVENT_NUM_COLS = ["epsilon", "n_refractive", "alpha", "beta", "gamma", "phi2", "psi2", "beta2"]


def morgan_numpy(smiles: str, radius: int = 2, n_bits: int = 2048) -> np.ndarray | None:
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    fp = AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)
    arr = np.zeros((n_bits,), dtype=np.float32)
    DataStructs.ConvertToNumpyArray(fp, arr)
    return arr


def build_feature_matrix(df: pd.DataFrame, smiles_col: str = "smiles") -> tuple[np.ndarray, np.ndarray, list[int]]:
    """
    Returns (X, y, invalid_row_indices).
    Rows with invalid SMILES are skipped in X/y; invalid_row_indices lists df index positions dropped.
    """
    solvent_vals = []
    for c in SOLVENT_NUM_COLS:
        if c in df.columns:
            solvent_vals.append(pd.to_numeric(df[c], errors="coerce").to_numpy(dtype=np.float64))
        else:
            solvent_vals.append(np.full(len(df), np.nan))
    S = np.column_stack(solvent_vals)
    col_medians = np.zeros(S.shape[1], dtype=np.float64)
    for j in range(S.shape[1]):
        col = S[:, j]
        col_medians[j] = float(np.nanmedian(col)) if np.any(np.isfinite(col)) else 0.0
    inds = S.copy()
    for j in range(S.shape[1]):
        mask = np.isnan(inds[:, j])
        inds[mask, j] = col_medians[j]

    X_list = []
    y_list = []
    invalid = []
    y = pd.to_numeric(df["delta_g_kcal_mol"], errors="coerce").to_numpy()
    for i, (_, row) in enumerate(df.iterrows()):
        smi = str(row[smiles_col]).strip()
        fp = morgan_numpy(smi)
        if fp is None:
            invalid.append(i)
            continue
        X_list.append(np.concatenate([fp, inds[i]]))
        y_list.append(y[i])
    if not X_list:
        raise ValueError("No valid rows for feature matrix.")
    return np.vstack(X_list), np.array(y_list, dtype=np.float64), invalid
