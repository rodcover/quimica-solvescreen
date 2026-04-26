# SolvScreen (implementação do plano)

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

Se o arquivo oficial não tiver SMILES, gere uma tabela auxiliar `entry_id,smiles` e use `--smiles-merge`.

### API

```text
set PYTHONPATH=src
set SOLVSCREEN_MODEL_PATH=models/baseline.joblib
uvicorn api.main:app --reload
```

- `POST /predict/bulk` — ΔG prevista (kcal/mol) a partir de SMILES + descritores opcionais do solvente.
- `POST /predict/confinement` — **stub** documentado; ver `schemas/confinement_dataset.schema.json` para o schema de labels (PMF, barreiras, RDF, etc.).

### Docker

Coloque `baseline.joblib` em `models/` após treinar (ou ajuste o `Dockerfile`). `docker build` copia `models/` para a imagem.

## Layout

| Caminho | Função |
|--------|--------|
| `src/solvscreen/etl_mnsol.py` | ETL → Parquet |
| `src/solvscreen/split_utils.py` | Split por cluster (Morgan) |
| `src/solvscreen/features.py` | Fingerprints + vetor de solvente |
| `src/solvscreen/train_baseline.py` | MLP + MAE/RMSE |
| `api/main.py` | FastAPI |
| `schemas/confinement_dataset.schema.json` | Registro de amostras confinamento |
| `notebooks/01_baseline_mnsol.ipynb` | Fluxo ETL + treino |
