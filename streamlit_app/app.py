"""
SolvScreen lab UI: predição bulk ΔG (molécula única ou lote CSV) via joblib ou API.

Run: pip install streamlit requests && set PYTHONPATH=src && streamlit run streamlit_app/app.py
"""

from __future__ import annotations

import os
import sys
from io import StringIO
from pathlib import Path

import pandas as pd
import requests
import streamlit as st

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT / "src") not in sys.path:
    sys.path.insert(0, str(ROOT / "src"))

import joblib  # noqa: E402
from solvscreen.model_bundle import predict_bulk  # noqa: E402

st.set_page_config(page_title="SolvScreen", layout="wide")
st.title("SolvScreen — ΔG de solvatação (bulk)")
st.caption(
    "MNSOL não é redistribuído; obtenha sob licença UMN. "
    "Referência: Lim & Jung, Chem. Sci. 2019 (Delfos)."
)

tab_single, tab_batch = st.tabs(["Molécula única", "Lote (CSV)"])

default_model = os.environ.get("SOLVSCREEN_MODEL_PATH", str(ROOT / "models" / "baseline.joblib"))

with st.sidebar:
    mode = st.radio("Fonte da predição", ["Modelo local (.joblib)", "API FastAPI"], index=0)
    model_path = st.text_input("Caminho do modelo (.joblib)", value=default_model)
    api_base = st.text_input("URL base da API (modo API)", value="http://127.0.0.1:8000")
    st.markdown("### Solvente padrão (opcional)")
    eps_s = st.text_input("ε (vazio = água ~78.39)", value="")
    nref_s = st.text_input("n refrativo (vazio = ~1.333)", value="")


def _solvent_kw() -> dict:
    kw = {}
    if eps_s.strip():
        try:
            kw["epsilon"] = float(eps_s.replace(",", "."))
        except ValueError:
            st.sidebar.error("ε inválido")
    if nref_s.strip():
        try:
            kw["n_refractive"] = float(nref_s.replace(",", "."))
        except ValueError:
            st.sidebar.error("n inválido")
    return kw


kw = _solvent_kw()

bundle = None
if mode == "Modelo local (.joblib)" and model_path and Path(model_path).is_file():
    bundle = joblib.load(model_path)
elif mode == "Modelo local (.joblib)" and model_path:
    st.sidebar.warning("Modelo não encontrado; treine com `scripts/run_train.py`.")


def _predict_row_local(smiles: str, b) -> tuple[float, float | None]:
    return predict_bulk(b, smiles.strip(), **kw)


def _predict_row_api(smiles: str) -> dict:
    url = api_base.rstrip("/") + "/predict/bulk"
    body: dict = {"solute_smiles": smiles.strip()}
    body.update(kw)
    r = requests.post(url, json=body, timeout=120)
    r.raise_for_status()
    return r.json()


with tab_single:
    smiles = st.text_input("SMILES", value="CCO")
    if st.button("Calcular ΔG", type="primary"):
        if not smiles.strip():
            st.error("Informe SMILES.")
        elif mode == "Modelo local (.joblib)":
            if bundle is None:
                st.error("Carregue um modelo válido.")
            else:
                try:
                    y, unc = _predict_row_local(smiles, bundle)
                    st.metric("ΔG prevista", f"{y:.3f} kcal/mol")
                    if unc is not None:
                        st.metric("Incerteza (ensemble)", f"± {unc:.3f} kcal/mol")
                except ValueError as e:
                    st.error(str(e))
        else:
            try:
                data = _predict_row_api(smiles)
                st.metric("ΔG prevista", f"{data['delta_g_kcal_mol']:.3f} kcal/mol")
                if data.get("uncertainty") is not None:
                    st.metric("Incerteza", f"± {data['uncertainty']:.3f} kcal/mol")
            except requests.RequestException as e:
                st.error(f"API: {e}")

with tab_batch:
    st.markdown(
        "CSV com coluna **`smiles`** (obrigatória). Opcionais: `epsilon`, `n_refractive` "
        "(por linha; sobrescreve sidebar se preenchidas)."
    )
    up = st.file_uploader("Arquivo CSV", type=["csv"])
    if up and st.button("Processar lote", type="primary"):
        raw = up.read().decode("utf-8", errors="replace")
        df = pd.read_csv(StringIO(raw))
        col = None
        for c in df.columns:
            if str(c).lower().strip() in ("smiles", "smile", "cano_smiles"):
                col = c
                break
        if col is None:
            st.error("Nenhuma coluna smiles encontrada (use 'smiles').")
        else:
            rows = []
            for _, r in df.iterrows():
                smi = str(r[col]).strip()
                if not smi or smi.lower() == "nan":
                    continue
                row_kw = dict(kw)
                if "epsilon" in df.columns and pd.notna(r.get("epsilon")):
                    row_kw["epsilon"] = float(r["epsilon"])
                if "n_refractive" in df.columns and pd.notna(r.get("n_refractive")):
                    row_kw["n_refractive"] = float(r["n_refractive"])
                try:
                    if mode == "Modelo local (.joblib)":
                        if bundle is None:
                            raise RuntimeError("sem modelo")
                        y, unc = predict_bulk(bundle, smi, **row_kw)
                        rows.append({"smiles": smi, "delta_g_kcal_mol": y, "uncertainty": unc})
                    else:
                        url = api_base.rstrip("/") + "/predict/bulk"
                        body = {"solute_smiles": smi}
                        body.update({k: v for k, v in row_kw.items() if v is not None})
                        resp = requests.post(url, json=body, timeout=120)
                        resp.raise_for_status()
                        d = resp.json()
                        rows.append(
                            {
                                "smiles": smi,
                                "delta_g_kcal_mol": d["delta_g_kcal_mol"],
                                "uncertainty": d.get("uncertainty"),
                            }
                        )
                except Exception as e:
                    rows.append({"smiles": smi, "delta_g_kcal_mol": None, "uncertainty": None, "error": str(e)})
            out = pd.DataFrame(rows)
            st.dataframe(out, use_container_width=True)
            st.download_button(
                "Baixar resultados CSV",
                data=out.to_csv(index=False).encode("utf-8"),
                file_name="solvscreen_predictions.csv",
                mime="text/csv",
            )

st.divider()
st.markdown(
    "Confinamento: `POST /predict/confinement` (stub) e `schemas/confinement_dataset.schema.json`."
)
