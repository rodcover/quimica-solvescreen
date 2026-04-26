from __future__ import annotations

from pathlib import Path

from solvscreen.etl_mnsol import clean_for_modeling, load_mnsol_table
from solvscreen.model_bundle import predict_bulk
from solvscreen.train_baseline import train_and_eval, train_ensemble_and_eval

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "fixtures" / "sample_mnsol_like.tsv"


def _df():
    return clean_for_modeling(load_mnsol_table(FIXTURE), require_smiles=True)


def test_predict_single():
    r = train_and_eval(_df(), test_fold=0, seed=0)
    model = r.pop("model")
    bundle = {"model": model, "feature": "test"}
    y, u = predict_bulk(bundle, "CCO")
    assert isinstance(y, float)
    assert u is None


def test_predict_ensemble():
    r = train_ensemble_and_eval(_df(), n_members=3, test_fold=0, seed=0)
    models = r.pop("models")
    bundle = {"ensemble": True, "models": models, "n_members": 3, "feature": "test"}
    y, u = predict_bulk(bundle, "CCO")
    assert isinstance(y, float)
    assert u is not None and u >= 0
