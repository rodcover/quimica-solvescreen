"""
SolvScreen API: bulk ΔG prediction + confinement placeholder.

Run from repo root:
  set PYTHONPATH=src
  set SOLVSCREEN_MODEL_PATH=models/baseline.joblib
  uvicorn api.main:app --reload
"""

from __future__ import annotations

import os
from pathlib import Path
from typing import Any

import joblib
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field

try:
    from solvscreen.model_bundle import predict_bulk as predict_bulk_model
except ImportError:
    import sys

    ROOT = Path(__file__).resolve().parents[1]
    sys.path.insert(0, str(ROOT / "src"))
    from solvscreen.model_bundle import predict_bulk as predict_bulk_model

app = FastAPI(
    title="SolvScreen",
    description="Bulk solvation (MNSOL-style) and confinement stubs. "
    "MNSOL raw data must not be redistributed; obtain under UMN license.",
    version="0.1.0",
)

_bundle: dict[str, Any] | None = None


def get_bundle() -> dict[str, Any]:
    global _bundle
    if _bundle is None:
        path = Path(os.environ.get("SOLVSCREEN_MODEL_PATH", "models/baseline.joblib"))
        if not path.is_file():
            raise HTTPException(
                status_code=503,
                detail=f"Model not found at {path}. Train with scripts/run_train.py or set SOLVSCREEN_MODEL_PATH.",
            )
        _bundle = joblib.load(path)
    return _bundle


class BulkPredictRequest(BaseModel):
    solute_smiles: str = Field(..., description="Solute SMILES")
    epsilon: float | None = Field(None, description="Solvent dielectric constant")
    n_refractive: float | None = Field(None, description="Refractive index")
    alpha: float | None = None
    beta: float | None = None
    gamma: float | None = None
    phi2: float | None = None
    psi2: float | None = None
    beta2: float | None = None


class BulkPredictResponse(BaseModel):
    delta_g_kcal_mol: float
    unit: str = "kcal/mol"
    uncertainty: float | None = Field(None, description="Reserved; null without ensemble calibration")
    model_note: str | None = None


class ConfinementPredictRequest(BaseModel):
    confinement_type: str = Field(..., description="e.g. graphene_slit, cnt_pore")
    effective_width_nm: float = Field(..., gt=0)
    surface_charge_density_cm2: float | None = None
    ion: str = Field(..., description="e.g. Li+, Mg2+, Ca2+")
    ionic_strength_molar: float | None = None
    temperature_k: float = Field(298.15, gt=0)
    md_rdf_gmax: float | None = Field(None, description="Optional: first-shell peak from MD")
    md_density_bulk_ratio: float | None = None


class ConfinementPredictResponse(BaseModel):
    status: str = "not_implemented"
    message: str
    suggested_targets: list[str]


@app.get("/health")
def health() -> dict[str, str]:
    return {"status": "ok"}


@app.post("/predict/bulk", response_model=BulkPredictResponse)
def predict_bulk(req: BulkPredictRequest) -> BulkPredictResponse:
    bundle = get_bundle()
    try:
        y, unc = predict_bulk_model(
            bundle,
            req.solute_smiles,
            epsilon=req.epsilon,
            n_refractive=req.n_refractive,
            alpha=req.alpha,
            beta=req.beta,
            gamma=req.gamma,
            phi2=req.phi2,
            psi2=req.psi2,
            beta2=req.beta2,
        )
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e)) from e
    note = bundle.get("feature")
    if bundle.get("ensemble"):
        nmem = bundle.get("n_members", len(bundle.get("models", [])))
        note = f"{note};ensemble_n={nmem}"
    return BulkPredictResponse(
        delta_g_kcal_mol=y,
        uncertainty=unc,
        model_note=note,
    )


@app.post("/predict/confinement", response_model=ConfinementPredictResponse)
def predict_confinement(req: ConfinementPredictRequest) -> ConfinementPredictResponse:
    """Placeholder until MD-derived labels exist (see schemas/confinement_dataset.schema.json)."""
    return ConfinementPredictResponse(
        status="stub",
        message=(
            "No confinement model is bundled. Collect PMF / barrier / RDF labels (schema in repo) "
            "and train a separate surrogate; do not extrapolate bulk ΔG to nanoconfinement."
        ),
        suggested_targets=[
            "pmf_barrier_kcal_mol",
            "delta_g_pore_minus_bulk_kcal_mol",
            "rdf_first_peak_position_angstrom",
            "rdf_first_peak_gmax",
            "n_hydration_shell_residence_ns",
        ],
    )
