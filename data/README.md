# Dados (`data/`)

## O que pode ir para o Git

| Caminho | Descrição |
|---------|-----------|
| `fixtures/sample_mnsol_like.tsv` | Amostra mínima (5 linhas) para testes e demo **sem** MNSOL real. |
| `raw/.gitkeep` | Pasta reservada; mantém `raw/` vazia no Git. |
| `processed/.gitkeep` | Parquets gerados localmente ficam **fora** do Git (ver `.gitignore`). |

## O que **não** commitar

- **`data/raw/MNSol*`** ou qualquer exportação bruta do **Minnesota Solvation Database**: licença da **University of Minnesota** — não redistribuir.
- **`data/processed/*.parquet`**: reproduza com `scripts/run_etl.py`.
- PDFs de artigos sem direito claro de redistribuição.

## Obter MNSOL

1. [Minnesota Solvation Database](https://comp.chem.umn.edu/mnsol/)
2. Aceitar a licença e baixar o pacote (ex. v2012).
3. Colocar `MNSol_alldata.txt` (ou TSV exportado) em **`data/raw/`** apenas na sua máquina.
4. Rodar o ETL (ver [docs/TUTORIAL.md](../docs/TUTORIAL.md)).

## Manifest (opcional)

Para rastrear arquivos processados **locais**, você pode manter um `data_manifest.json` com hashes **fora do Git** ou em notas privadas — não inclua caminhos absolutos com dados licenciados em repositório público.

Ver também: [docs/DATA_POLICY.md](../docs/DATA_POLICY.md).
