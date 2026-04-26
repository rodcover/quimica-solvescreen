from __future__ import annotations

from pathlib import Path

import pandas as pd

from solvscreen.etl_mnsol import clean_for_modeling, load_mnsol_table, to_standard_parquet

ROOT = Path(__file__).resolve().parents[1]
FIXTURE = ROOT / "data" / "fixtures" / "sample_mnsol_like.tsv"


def test_load_and_clean_fixture():
    df = load_mnsol_table(FIXTURE)
    clean = clean_for_modeling(df, require_smiles=True, solvation_types=("abs",))
    assert len(clean) == 5
    assert "delta_g_kcal_mol" in clean.columns
    assert clean["smiles"].notna().all()


def test_parquet_roundtrip(tmp_path: Path):
    df = load_mnsol_table(FIXTURE)
    clean = clean_for_modeling(df, require_smiles=True)
    out = tmp_path / "t.parquet"
    to_standard_parquet(clean, out)
    back = pd.read_parquet(out)
    assert len(back) == 5
