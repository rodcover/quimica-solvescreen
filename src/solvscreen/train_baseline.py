"""
Train a baseline regressor for ΔG (kcal/mol): MLP on [Morgan FP || solvent descriptors].

Optional bootstrap ensemble for a simple epistemic spread (not calibrated CI).
Metrics: MAE, RMSE (comparable scale to Delfos / SolvBERT literature).
"""

from __future__ import annotations

import argparse
import json
from pathlib import Path

import joblib
import numpy as np
import pandas as pd
from sklearn.metrics import mean_absolute_error, mean_squared_error
from sklearn.neural_network import MLPRegressor
from sklearn.pipeline import Pipeline
from sklearn.preprocessing import StandardScaler

from solvscreen.features import build_feature_matrix
from solvscreen.split_utils import assign_fold_by_cluster


def _mlp_pipeline(n_samples: int, seed: int) -> Pipeline:
    if n_samples < 8:
        hidden = (64, 32)
        max_iter = 2000
    elif n_samples < 200:
        hidden = (256, 128)
        max_iter = 2000
    else:
        hidden = (512, 256, 128)
        max_iter = 500

    mlp = MLPRegressor(
        hidden_layer_sizes=hidden,
        activation="relu",
        solver="adam",
        alpha=1e-4,
        max_iter=max_iter,
        random_state=seed,
        early_stopping=n_samples >= 20,
        validation_fraction=0.15 if n_samples >= 20 else 0.0,
        n_iter_no_change=30,
    )
    return Pipeline([("scale", StandardScaler()), ("mlp", mlp)])


def _train_test_split_folds(df: pd.DataFrame, test_fold: int, seed: int):
    df = df.reset_index(drop=True)
    folds = assign_fold_by_cluster(df, n_folds=5, seed=seed)
    train_mask = folds != test_fold
    test_mask = folds == test_fold
    df_tr = df[train_mask].reset_index(drop=True)
    df_te = df[test_mask].reset_index(drop=True)

    if len(df_te) == 0:
        rng = np.random.default_rng(seed)
        idx = np.arange(len(df))
        rng.shuffle(idx)
        cut = max(1, int(0.8 * len(df)))
        tr_i, te_i = set(idx[:cut]), set(idx[cut:])
        df_tr = df.iloc[[i for i in range(len(df)) if i in tr_i]].reset_index(drop=True)
        df_te = df.iloc[[i for i in range(len(df)) if i in te_i]].reset_index(drop=True)
    return df_tr, df_te


def train_and_eval(df: pd.DataFrame, test_fold: int = 0, seed: int = 42) -> dict:
    df_tr, df_te = _train_test_split_folds(df, test_fold, seed)
    X_tr, y_tr, _ = build_feature_matrix(df_tr)
    X_te, y_te, _ = build_feature_matrix(df_te)

    model = _mlp_pipeline(len(df_tr), seed)
    model.fit(X_tr, y_tr)
    pred = model.predict(X_te)
    mae = mean_absolute_error(y_te, pred)
    rmse = float(np.sqrt(mean_squared_error(y_te, pred)))
    return {
        "model": model,
        "mae_kcal_mol": float(mae),
        "rmse_kcal_mol": rmse,
        "n_train": int(len(y_tr)),
        "n_test": int(len(y_te)),
    }


def train_ensemble_and_eval(
    df: pd.DataFrame,
    n_members: int = 5,
    test_fold: int = 0,
    seed: int = 42,
) -> dict:
    df_tr, df_te = _train_test_split_folds(df, test_fold, seed)
    X_te, y_te, _ = build_feature_matrix(df_te)
    n = len(df_tr)
    rng = np.random.default_rng(seed)
    models: list = []

    for k in range(n_members):
        idx = rng.integers(0, n, size=max(n, 1))
        df_b = df_tr.iloc[idx].reset_index(drop=True)
        X_b, y_b, _ = build_feature_matrix(df_b)
        m = _mlp_pipeline(len(df_b), seed + k + 17)
        m.fit(X_b, y_b)
        models.append(m)

    pred_stack = np.column_stack([m.predict(X_te) for m in models])
    pred_mean = pred_stack.mean(axis=1)
    mae = mean_absolute_error(y_te, pred_mean)
    rmse = float(np.sqrt(mean_squared_error(y_te, pred_mean)))
    return {
        "models": models,
        "mae_kcal_mol": float(mae),
        "rmse_kcal_mol": rmse,
        "n_train": int(n),
        "n_test": int(len(y_te)),
        "n_ensemble_members": int(n_members),
    }


def run_cli() -> None:
    p = argparse.ArgumentParser(description="Train baseline ΔG model from cleaned MNSOL Parquet.")
    p.add_argument("parquet", type=Path, help="Cleaned Parquet from ETL")
    p.add_argument("-o", "--output", type=Path, required=True, help="Output .joblib model path")
    p.add_argument("--metrics", type=Path, default=None, help="Optional JSON path for test metrics")
    p.add_argument("--test-fold", type=int, default=0)
    p.add_argument("--seed", type=int, default=42)
    p.add_argument(
        "--ensemble",
        type=int,
        default=0,
        metavar="N",
        help="If N>=2, train N bootstrap MLPs and save ensemble (uncertainty = member std).",
    )
    args = p.parse_args()

    df = pd.read_parquet(args.parquet)
    if args.ensemble >= 2:
        result = train_ensemble_and_eval(df, n_members=args.ensemble, test_fold=args.test_fold, seed=args.seed)
        models = result.pop("models")
        payload = {
            "ensemble": True,
            "models": models,
            "feature": "morgan_r2_2048_plus_solvent8",
            "n_members": int(args.ensemble),
        }
    else:
        result = train_and_eval(df, test_fold=args.test_fold, seed=args.seed)
        model = result.pop("model")
        payload = {"model": model, "feature": "morgan_r2_2048_plus_solvent8"}

    args.output.parent.mkdir(parents=True, exist_ok=True)
    joblib.dump(payload, args.output)
    print(json.dumps(result, indent=2))
    if args.metrics:
        args.metrics.parent.mkdir(parents=True, exist_ok=True)
        with open(args.metrics, "w", encoding="utf-8") as f:
            json.dump(result, f, indent=2)


if __name__ == "__main__":
    run_cli()
