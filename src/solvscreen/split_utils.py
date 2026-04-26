"""Chemically sensible splits: cluster solutes by Morgan fingerprint."""

from __future__ import annotations

import numpy as np
import pandas as pd
from rdkit import Chem, DataStructs
from rdkit.Chem import AllChem
from sklearn.cluster import AgglomerativeClustering


def morgan_fp_bitvect(smiles: str, radius: int = 2, n_bits: int = 2048):
    mol = Chem.MolFromSmiles(smiles)
    if mol is None:
        return None
    return AllChem.GetMorganFingerprintAsBitVect(mol, radius, nBits=n_bits)


def _bv_from_numpy(row: np.ndarray, n_bits: int) -> DataStructs.ExplicitBitVect:
    bv = DataStructs.ExplicitBitVect(n_bits)
    for k in range(n_bits):
        if row[k]:
            bv.SetBit(int(k))
    return bv


def cluster_solutes(
    smiles_list: list[str],
    distance_threshold: float = 0.4,
    radius: int = 2,
    n_bits: int = 2048,
) -> tuple[np.ndarray, list[int | None]]:
    """
    Build Morgan fingerprints and cluster with average linkage on (1 - Tanimoto).
    Returns (X fingerprint matrix for valid rows, cluster label per original row; None if invalid SMILES).
    """
    fps: list[DataStructs.ExplicitBitVect] = []
    valid_idx: list[int] = []
    for i, smi in enumerate(smiles_list):
        fp = morgan_fp_bitvect(smi, radius=radius, n_bits=n_bits)
        if fp is None:
            continue
        fps.append(fp)
        valid_idx.append(i)

    if not fps:
        raise ValueError("No valid fingerprints for clustering.")

    n = len(fps)
    dist = np.zeros((n, n), dtype=np.float64)
    for i in range(n):
        for j in range(i + 1, n):
            d = 1.0 - DataStructs.TanimotoSimilarity(fps[i], fps[j])
            dist[i, j] = dist[j, i] = d

    clustering = AgglomerativeClustering(
        n_clusters=None,
        distance_threshold=distance_threshold,
        metric="precomputed",
        linkage="average",
    )
    labels = clustering.fit_predict(dist)

    X = np.zeros((n, n_bits), dtype=np.int8)
    for i, fp in enumerate(fps):
        DataStructs.ConvertToNumpyArray(fp, X[i])

    full_labels: list[int | None] = [None] * len(smiles_list)
    for idx, lab in zip(valid_idx, labels):
        full_labels[idx] = int(lab)
    return X, full_labels


def assign_fold_by_cluster(
    df: pd.DataFrame,
    smiles_col: str = "smiles",
    n_folds: int = 5,
    seed: int = 42,
    distance_threshold: float = 0.4,
) -> pd.Series:
    """Assign fold 0..n_folds-1 so chemically similar solutes tend to share a cluster (single fold)."""
    _, labels = cluster_solutes(
        df[smiles_col].astype(str).tolist(),
        distance_threshold=distance_threshold,
    )
    clusters = np.array([l if l is not None else -1 for l in labels])
    rng = np.random.default_rng(seed)
    unique = sorted({c for c in clusters if c >= 0})
    rng.shuffle(unique)
    cluster_to_fold = {c: i % n_folds for i, c in enumerate(unique)}
    folds = []
    for c in clusters:
        if c < 0:
            folds.append(int(rng.integers(0, n_folds)))
        else:
            folds.append(cluster_to_fold[c])
    return pd.Series(folds, index=df.index, name="fold")
