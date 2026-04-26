"""
SolvScreen lab UI: predict bulk ΔG via local joblib or remote FastAPI.

Run from repo root:
  pip install streamlit requests
  set PYTHONPATH=src
  streamlit run streamlit_app/app.py
"""

from __future__ import annotations

import os
import sys
from pathlib import Path

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
    "Dados MNSOL não são redistribuídos; obtenha sob licença UMN. "
    "Referência: Lim & Jung, Chem. Sci. 2019 (Delfos)."
)

mode = st.sidebar.radio("Fonte da predição", ["Modelo local (.joblib)", "API FastAPI"], index=0)
default_model = os.environ.get("SOLVSCREEN_MODEL_PATH", str(ROOT / "models" / "baseline.joblib"))

if mode == "Modelo local (.joblib)":
    model_path = st.sidebar.text_input("Caminho do modelo", value=default_model)
    bundle = None
    if model_path and Path(model_path).is_file():
        bundle = joblib.load(model_path)
    elif model_path:
        st.sidebar.warning("Arquivo não encontrado; treine com `scripts/run_train.py`.")
else:
    api_base = st.sidebar.text_input("URL base da API", value="http://127.0.0.1:8000")
    bundle = None

st.sidebar.markdown("### Solvente (opcional)")
eps_s = st.sidebar.text_input("ε (dielétrico; vazio = padrão água)", value="")
nref_s = st.sidebar.text_input("Índice de refração (vazio = padrão)", value="")

col1, col2 = st.columns(2)
with col1:
    smiles = st.text_input("SMILES do soluto", value="CCO", help="Ex.: etanol")
with col2:
    run = st.button("Calcular ΔG", type="primary")

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


def _post_api():
    url = api_base.rstrip("/") + "/predict/bulk"
    body = {"solute_smiles": smiles.strip()}
    if "epsilon" in kw:
        body["epsilon"] = kw["epsilon"]
    if "n_refractive" in kw:
        body["n_refractive"] = kw["n_refractive"]
    r = requests.post(url, json=body, timeout=60)
    r.raise_for_status()
    return r.json()


if run:
    if not smiles.strip():
        st.error("Informe um SMILES.")
    elif mode == "Modelo local (.joblib)":
        if bundle is None:
            st.error("Carregue um modelo válido.")
        else:
            try:
                y, unc = predict_bulk(bundle, smiles.strip(), **kw)
                st.metric("ΔG prevista", f"{y:.3f} kcal/mol")
                if unc is not None:
                    st.metric("Incerteza (ensemble)", f"± {unc:.3f} kcal/mol")
                else:
                    st.info("Incerteza só disponível para modelos treinados com `--ensemble N` (N≥2).")
            except ValueError as e:
                st.error(str(e))
    else:
        try:
            data = _post_api()
            st.metric("ΔG prevista", f"{data['delta_g_kcal_mol']:.3f} kcal/mol")
            u = data.get("uncertainty")
            if u is not None:
                st.metric("Incerteza", f"± {u:.3f} kcal/mol")
            st.caption(data.get("model_note", ""))
        except requests.RequestException as e:
            st.error(f"Falha na API: {e}")

st.divider()
st.markdown(
    """
    **Confinamento / membranas:** use o endpoint `POST /predict/confinement` (stub) e o schema
    `schemas/confinement_dataset.schema.json` para preparar dados de treino.
    """
)
