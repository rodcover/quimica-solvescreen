# Changelog

Formato baseado em [Keep a Changelog](https://keepachangelog.com/pt-BR/1.0.0/).

## [Unreleased]

## [0.2.0] — 2026-04-26

### Adicionado

- Config YAML de treino (`configs/train_mlp.yaml`), `--config` e `--model-type rf|mlp` no treino.
- `scripts/benchmark_literature.py` para comparar métricas com ordem de grandeza Delfos.
- `scripts/export_openapi.py` e documentação OpenAPI gerada sob demanda.
- `Makefile`, `docker-compose.yml`, `Dockerfile.streamlit`.
- `data/README.md`, `docs/DATA_POLICY.md`, `docs/REFERENCIAS.md`, `CONTRIBUTING.md`, `CHANGELOG.md`.
- `CITATION.cff`, `pyproject.toml`, `.pre-commit-config.yaml`, `requirements-dev.txt`.
- Exemplo `examples/confinement_literature.json` e testes `jsonschema`.
- Teste de regressão leve em predição (`tests/test_regression_predict.py`).
- Streamlit: aba **Lote (CSV)** com export de resultados.
- Notebook `notebooks/02_error_analysis.ipynb` (esqueleto).
- Diagrama de fluxo (Mermaid) no tutorial.

### Notas

- Atualizar badges/URLs do repositório e metadados de citação conforme o remoto Git.

## [0.1.0] — 2026-04-26

### Adicionado

- Pipeline ETL MNSOL, treino MLP/ensemble, FastAPI, Streamlit básico, schema confinamento, CI, Docker API, tutorial.
