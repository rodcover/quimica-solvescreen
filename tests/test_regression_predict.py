"""Regressão leve: predição estável no fixture para SMILES conhecido."""

from __future__ import annotations

from pathlib import Path

import numpy as np

from solvscreen.etl_mnsol import clean_for_modeling, load_mnsol_table
from solvscreen.model_bundle import predict_bulk
from solvscreen.train_baseline import train_and_eval

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "fixtures" / "sample_mnsol_like.tsv"


def test_cco_prediction_stable():
    df = clean_for_modeling(load_mnsol_table(FIXTURE), require_smiles=True)
    r = train_and_eval(df, test_fold=0, seed=42, model_type="mlp")
    model = r["model"]
    bundle = {"model": model, "feature": "test"}
    y, _ = predict_bulk(bundle, "CCO")
    # Com split pequeno, a predição pode afastar-se do rótulo; checar finitude e estabilidade
    assert -25.0 < y < 25.0
    y2, _ = predict_bulk(bundle, "CCO")
    assert np.isclose(y, y2)
