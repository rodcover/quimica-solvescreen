"""Load trained artifact and predict ΔG (mean ± std for bootstrap ensembles)."""

from __future__ import annotations

from typing import Any

import numpy as np

from solvscreen.inference import vector_for_prediction


def predict_bulk(
    bundle: dict[str, Any],
    solute_smiles: str,
    *,
    epsilon: float | None = None,
    n_refractive: float | None = None,
    alpha: float | None = None,
    beta: float | None = None,
    gamma: float | None = None,
    phi2: float | None = None,
    psi2: float | None = None,
    beta2: float | None = None,
) -> tuple[float, float | None]:
    """
    Returns (delta_g_kcal_mol, uncertainty_std_or_none).
    uncertainty is empirical spread across ensemble members when present.
    """
    x = vector_for_prediction(
        solute_smiles,
        epsilon=epsilon,
        n_refractive=n_refractive,
        alpha=alpha,
        beta=beta,
        gamma=gamma,
        phi2=phi2,
        psi2=psi2,
        beta2=beta2,
    ).reshape(1, -1)

    if bundle.get("ensemble"):
        models: list = bundle["models"]
        preds = np.array([float(m.predict(x)[0]) for m in models], dtype=np.float64)
        mean = float(preds.mean())
        if len(preds) > 1:
            unc = float(preds.std(ddof=1))
        else:
            unc = None
        return mean, unc

    if "model" not in bundle:
        raise KeyError("Bundle must contain 'model' or ensemble 'models'.")
    return float(bundle["model"].predict(x)[0]), None
