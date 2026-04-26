"""Single-row inference matching training features."""

from __future__ import annotations

import numpy as np

from solvscreen.features import SOLVENT_NUM_COLS, morgan_numpy

_DEFAULTS: dict[str, float] = {
    "epsilon": 78.39,
    "n_refractive": 1.333,
    "alpha": 0.0,
    "beta": 0.0,
    "gamma": 0.0,
    "phi2": 0.0,
    "psi2": 0.0,
    "beta2": 0.0,
}


def vector_for_prediction(
    solute_smiles: str,
    epsilon: float | None = None,
    n_refractive: float | None = None,
    alpha: float | None = None,
    beta: float | None = None,
    gamma: float | None = None,
    phi2: float | None = None,
    psi2: float | None = None,
    beta2: float | None = None,
) -> np.ndarray:
    fp = morgan_numpy(solute_smiles.strip())
    if fp is None:
        raise ValueError(f"Invalid SMILES: {solute_smiles!r}")
    provided = {
        "epsilon": epsilon,
        "n_refractive": n_refractive,
        "alpha": alpha,
        "beta": beta,
        "gamma": gamma,
        "phi2": phi2,
        "psi2": psi2,
        "beta2": beta2,
    }
    tail = []
    for key in SOLVENT_NUM_COLS:
        v = provided[key]
        if v is None:
            v = _DEFAULTS[key]
        tail.append(float(v))
    return np.concatenate([fp, np.array(tail, dtype=np.float32)])
