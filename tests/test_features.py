from __future__ import annotations

from pathlib import Path

from solvscreen.features import build_feature_matrix, morgan_numpy
from solvscreen.etl_mnsol import clean_for_modeling, load_mnsol_table
ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "fixtures" / "sample_mnsol_like.tsv"


def test_morgan_shape():
    v = morgan_numpy("CCO")
    assert v is not None
    assert v.shape == (2048,)


def test_feature_matrix_rows():
    df = clean_for_modeling(load_mnsol_table(FIXTURE), require_smiles=True)
    X, y, invalid = build_feature_matrix(df)
    assert X.shape[0] == len(df)
    assert X.shape[1] == 2048 + 8
    assert y.shape[0] == len(df)
    assert invalid == []
