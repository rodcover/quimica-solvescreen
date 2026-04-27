# SolvScreen (implementação do plano)

[![CI](https://github.com/rodcover/quimica-solvescreen/actions/workflows/ci.yml/badge.svg)](https://github.com/rodcover/quimica-solvescreen/actions/workflows/ci.yml)
[![License: MIT](https://img.shields.io/badge/License-MIT-yellow.svg)](LICENSE)

**Tutorial fim a fim:** [docs/TUTORIAL.md](docs/TUTORIAL.md) · **Dados / licenças:** [data/README.md](data/README.md) · **Contato:** [docs/CONTACT.md](docs/CONTACT.md) · **Contribuir:** [CONTRIBUTING.md](CONTRIBUTING.md) · **Changelog:** [CHANGELOG.md](CHANGELOG.md) · **Citar software:** [CITATION.cff](CITATION.cff)

Pipeline para **energia livre de solvatação em meio bulk** (estilo MNSOL / [Delfos](https://doi.org/10.1039/C9SC02452B)) e **esboço de API** para confinamento (sem modelo treinado até haver labels de MD/literatura).

## Dados e citações

- **MNSOL**: obter em [Minnesota Solvation Database](https://comp.chem.umn.edu/mnsol/); licença UMN — **não redistribuir** o pacote bruto.
- **Delfos** (baseline conceitual): Lim & Jung, *Chem. Sci.*, 2019, [DOI 10.1039/C9SC02452B](https://doi.org/10.1039/C9SC02452B).
- Evoluções úteis para comparação de métricas: [SolvBERT](https://doi.org/10.1039/D2DD00107A); revisões sobre ML e membranas p.ex. [Environmental Chemistry Letters](https://doi.org/10.1007/s10311-023-01695-y).

## Uso rápido

```text
pip install -r requirements.txt
python scripts/run_etl.py path/to/MNSol_export.tsv -o data/processed/mnsol_clean.parquet
python scripts/run_train.py data/processed/mnsol_clean.parquet -o models/baseline.joblib --metrics models/metrics.json
```

Treino com **ensemble** (dispersão entre membros como incerteza heurística):

```text
python scripts/run_train.py data/processed/mnsol_clean.parquet -o models/baseline_ens.joblib --ensemble 5 --metrics models/metrics.json
```

Baseline **Random Forest** (rápido para comparação):

```text
python scripts/run_train.py data/processed/mnsol_clean.parquet -o models/baseline_rf.joblib --model-type rf --metrics models/metrics_rf.json
```

Com arquivo de configuração:

```text
python scripts/run_train.py data/processed/mnsol_clean.parquet -o models/out.joblib --config configs/train_mlp.yaml --metrics models/metrics.json
```

Comparar métricas com ordem de grandeza **Delfos** (qualitativo):

```text
python scripts/benchmark_literature.py models/metrics.json
```

OpenAPI estático:

```text
set PYTHONPATH=src
python scripts/export_openapi.py
```

Se o arquivo oficial não tiver SMILES, gere uma tabela auxiliar `entry_id,smiles` e use `--smiles-merge`.

### Interface Streamlit

```text
set PYTHONPATH=src
streamlit run streamlit_app/app.py
```

Ou: `python scripts/run_streamlit.py`. Modo **API** exige `uvicorn` rodando em paralelo.

### Testes

```text
pytest tests/ -q
```

### API

```text
set PYTHONPATH=src
set SOLVSCREEN_MODEL_PATH=models/baseline.joblib
uvicorn api.main:app --reload
```

- `POST /predict/bulk` — ΔG prevista (kcal/mol) a partir de SMILES + descritores opcionais do solvente.
- `POST /predict/confinement` — **stub** documentado; ver `schemas/confinement_dataset.schema.json` para o schema de labels (PMF, barreiras, RDF, etc.).

### Docker

- **`Dockerfile`**: API na porta 8000 (modelo demo a partir do fixture no build).
- **`Dockerfile.streamlit`**: interface na porta 8501.
- **`docker compose up --build`**: sobe API + Streamlit (veja `docker-compose.yml`).

### Make (opcional)

Com GNU Make (Git Bash / WSL): `make install`, `make train`, `make test`, `make openapi`, `make schema`.

### Desenvolvimento

```text
pip install -r requirements-dev.txt
pre-commit install
```

## Layout

| Caminho | Função |
|--------|--------|
| `src/solvscreen/etl_mnsol.py` | ETL → Parquet |
| `src/solvscreen/split_utils.py` | Split por cluster (Morgan) |
| `src/solvscreen/features.py` | Fingerprints + vetor de solvente |
| `src/solvscreen/train_baseline.py` | MLP + MAE/RMSE; opção `--ensemble` |
| `src/solvscreen/model_bundle.py` | Predição única ou ensemble |
| `streamlit_app/app.py` | Painel laboratório |
| `tests/` | Pytest (ETL, features, modelo, API) |
| `api/main.py` | FastAPI |
| `schemas/confinement_dataset.schema.json` | Registro de amostras confinamento |
| `notebooks/01_baseline_mnsol.ipynb` | Fluxo ETL + treino |
| `notebooks/02_error_analysis.ipynb` | Esqueleto análise de erros |
| `configs/`, `Makefile`, `docker-compose.yml` | Automação e deploy local |
| `docs/REFERENCIAS.md`, `docs/DATA_POLICY.md` | Bibliografia e política de dados |
