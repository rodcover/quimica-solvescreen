from __future__ import annotations

from pathlib import Path

import joblib
import pytest
from fastapi.testclient import TestClient

ROOT = Path(__file__).resolve().parents[1]


@pytest.fixture
def client(tmp_path, monkeypatch):
    import sys

    sys.path.insert(0, str(ROOT / "src"))
    from solvscreen.etl_mnsol import clean_for_modeling, load_mnsol_table
    from solvscreen.train_baseline import train_and_eval

    df = clean_for_modeling(
        load_mnsol_table(ROOT / "data" / "fixtures" / "sample_mnsol_like.tsv"),
        require_smiles=True,
    )
    r = train_and_eval(df, test_fold=0, seed=42)
    p = tmp_path / "m.joblib"
    joblib.dump({"model": r["model"], "feature": "t"}, p)
    monkeypatch.setenv("SOLVSCREEN_MODEL_PATH", str(p))

    import importlib

    import api.main as api_main

    importlib.reload(api_main)
    return TestClient(api_main.app)


def test_confinement_stub(client: TestClient):
    r = client.post(
        "/predict/confinement",
        json={
            "confinement_type": "graphene_slit",
            "effective_width_nm": 1.0,
            "ion": "Li+",
        },
    )
    assert r.status_code == 200
    d = r.json()
    assert d["status"] == "stub"
    assert "pmf_barrier" in " ".join(d.get("suggested_targets", []))
