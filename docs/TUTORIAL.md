# Tutorial fim a fim — SolvScreen

Este guia explica **para que serve** cada parte do projeto, **como implementar** o ambiente, **como executar** o fluxo completo (dados → modelo → API → interface), dá **exemplos práticos** e relaciona o trabalho com a **literatura** que o fundamenta.

---

## 1. Objetivo do projeto

O **SolvScreen** é uma base técnica para:

1. **Prever energia livre de solvatação (ΔG)** de solutos orgânicos em solventes, no espírito de bases experimentais como o **MNSOL** e modelos de aprendizado profundo como o **Delfos**.
2. **Servir essas predições** por uma **API HTTP** e por uma **interface Streamlit** para uso em laboratório.
3. **Preparar uma segunda linha de pesquisa** (confinamento em nanoporos / membranas): hoje há apenas **schema de dados** e **endpoint stub**, sem modelo treinado — alinhado à ideia de não extrapolar ΔG “bulk” para nanoconfinamento sem labels próprios.

---

## 2. Base científica e relação com o código

| Tema | Ideia na literatura | O que o repositório faz |
|------|---------------------|-------------------------|
| **Dados experimentais de solvatação** | O **Minnesota Solvation Database (MNSOL)** agrega energias livres de solvatação e transferência para muitos solutos e solventes; é a base usada no artigo do **Delfos**. | `etl_mnsol.py` lê exportações tabulares no estilo `MNSol_alldata.txt` ou TSV com cabeçalho; **não** inclui o MNSOL bruto (licença UMN). |
| **ΔG em solventes orgânicos genéricos** | **Delfos** (Lim & Jung, *Chemical Science*, 2019) usa aprendizado profundo com representações de soluto e solvente para predizer ΔG com acurácia comparável a métodos caros. | Baseline **MLP** sobre **fingerprint Morgan (RDKit)** + **descritores de solvente** (ε, n, α, β, …): mais simples que Delfos, mas **comparável em métricas** (MAE/RMSE em kcal/mol) para relatórios e evolução futura. |
| **Modelos mais recentes** | Trabalhos como **SolvBERT** (*Digital Discovery*, RSC) exploram linguagem molecular / transformers para ΔG e propriedades relacionadas. | O desenho do pipeline (Parquet → treino → API) permite **trocar** o regressor por GNN/transformer sem mudar o contrato da API. |
| **Solvatação implícita em escala** | **LSNN** e similares usam grandes volumes de dados de simulação (ex.: alquimia em solvente explícito), paradigma diferente do MNSOL experimental. | Este repo foca no eixo **experimental / MNSOL**; LSNN aparece como **referência conceitual** em `fontes/`. |
| **Íons, confinamento, membranas** | Revisões sobre **membranas de óxido de grafeno**, **ML no design de membranas**, **XAI em transporte iônico** em nanofiltração; projetos como o de **Qing Shao** (NSF) sobre potenciais híbridos clássico–ML e efeitos quânticos em nanoporos. | `schemas/confinement_dataset.schema.json` formaliza **entradas e labels** (PMF, barreiras, RDF, seletividade); `POST /predict/confinement` é **stub** até existir treino. |
| **Validação “química”** | Splits aleatórios puros podem vazar moléculas quase idênticas entre treino e teste. | `split_utils.py` sugere **agrupamento por fingerprint** para folds mais conservadores. |

### Referências sugeridas (leitura e citação)

1. **Marenich, A. V. et al.; Minnesota Solvation Database** — página e manual: [MNSOL](https://comp.chem.umn.edu/mnsol/); uso sujeito à **licença da University of Minnesota** (não redistribuir o pacote bruto no GitHub).
2. **Lim, H.; Jung, Y.** “Delfos: deep learning model for prediction of solvation free energies in generic organic solvents.” *Chem. Sci.* **2019**, 10, 8306–8315. [DOI 10.1039/C9SC02452B](https://doi.org/10.1039/C9SC02452B) — PMC: [PMC7017869](https://pmc.ncbi.nlm.nih.gov/articles/PMC7017869/).
3. **SolvBERT** — modelo NLP para ΔG/solubilidade: [DOI 10.1039/D2DD00107A](https://doi.org/10.1039/D2DD00107A) (*Digital Discovery*).
4. **Revisão ML e membranas** — *Environ. Chem. Lett.* [DOI 10.1007/s10311-023-01695-y](https://doi.org/10.1007/s10311-023-01695-y).
5. **Transporte iônico e XAI (poliamida)** — *Environ. Sci. Technol.* [DOI 10.1021/acs.est.2c08384](https://doi.org/10.1021/acs.est.2c08384).
6. **Separ iônica / membranas nanofluídicas GO** — revisão *Chem. Eng. J.* (ex.: [ScienceDirect](https://www.sciencedirect.com/science/article/abs/pii/S0011916424009299)).
7. **Projeto Qing Shao (UKY / NSF)** — descrição pública do escopo ML + confinamento: [Scholars @ UK](https://scholars.uky.edu/en/projects/developing-machine-learning-potential-to-unravel-quantum-effect-o/).

Os arquivos em **`fontes/`** no repositório são notas de apoio (incluindo links para parte dessa literatura); o tutorial oficial para execução é este documento.

---

## 3. O que é cada componente do repositório

| Caminho | Função |
|---------|--------|
| `src/solvscreen/etl_mnsol.py` | Carrega TSV/TXT MNSOL, normaliza colunas, filtra tipos (ex. `abs`), exige SMILES para modelagem, grava **Parquet** padronizado. |
| `src/solvscreen/split_utils.py` | **Folds** por similaridade de Morgan (evita vazamento estrutural grosseiro). |
| `src/solvscreen/features.py` | **Vetor de entrada**: fingerprint Morgan (2048 bits) + 8 descritores numéricos de solvente. |
| `src/solvscreen/train_baseline.py` | Treina **MLP** (`sklearn`) + métricas MAE/RMSE; opção **`--ensemble N`** (bootstrap de N modelos). |
| `src/solvscreen/model_bundle.py` | Predição unificada: um modelo ou **média ± desvio** entre membros do ensemble. |
| `src/solvscreen/inference.py` | Monta o vetor de features a partir de SMILES + solvente (valores padrão tipo “água” quando omitidos). |
| `api/main.py` | **FastAPI**: `POST /predict/bulk`, `POST /predict/confinement` (stub), `GET /health`. |
| `streamlit_app/app.py` | Interface web: predição via **joblib local** ou **API remota**. |
| `scripts/run_etl.py`, `run_train.py`, `run_streamlit.py` | Entradas de linha de comando com `PYTHONPATH` ajustado. |
| `schemas/confinement_dataset.schema.json` | Contrato JSON para futuros dados de **MD/literatura** (nanoporos, PMF, etc.). |
| `examples/confinement_sample.json` | Exemplo preenchendo o schema. |
| `data/fixtures/sample_mnsol_like.tsv` | **Fixture mínimo** para testes e demo sem MNSOL real. |
| `tests/` | **Pytest**: ETL, features, treino, predição, API. |
| `.github/workflows/ci.yml` | CI: ETL + treino no fixture + pytest. |
| `Dockerfile` | Imagem que treina no fixture no **build** e expõe só a API. |
| `fontes/` | Notas e referências em Markdown (contexto do projeto). |
| `notebooks/01_baseline_mnsol.ipynb` | Fluxo ETL + treino via subprocess. |

---

## 4. Pré-requisitos

- **Python 3.11** (recomendado; 3.10+ costuma funcionar).
- **Git** (para clonar o repositório).
- **Dados MNSOL** (opcional para produção): download após aceitar a licença em [comp.chem.umn.edu/mnsol](https://comp.chem.umn.edu/mnsol/).

**Windows (PowerShell):** use `;` em vez de `&&` entre comandos, se necessário.

---

## 5. Instalação

No diretório raiz do projeto:

```powershell
cd C:\caminho\para\quimica
python -m venv .venv
.\.venv\Scripts\Activate.ps1
pip install -r requirements.txt
```

Dependências principais: `pandas`, `pyarrow`, `numpy`, `scikit-learn`, `rdkit`, `fastapi`, `uvicorn`, `streamlit`, `pytest`, `joblib`, `requests`.

---

## 6. Fluxo fim a fim (sem MNSOL real) — demo com fixture

Ideal para validar a instalação e o CI local.

### 6.1. ETL

```powershell
python scripts/run_etl.py data/fixtures/sample_mnsol_like.tsv -o data/processed/demo.parquet
```

Saída esperada: mensagem `Wrote 5 rows to ...`.

### 6.2. Treino (modelo único)

```powershell
python scripts/run_train.py data/processed/demo.parquet -o models/baseline.joblib --metrics models/metrics.json
type models\metrics.json
```

Você verá **MAE** e **RMSE** no conjunto de teste (no fixture os números são só ilustrativos).

### 6.3. Treino com ensemble (incerteza heurística)

```powershell
python scripts/run_train.py data/processed/demo.parquet -o models/ensemble.joblib --ensemble 5 --metrics models/metrics_ens.json
```

O arquivo `ensemble.joblib` guarda vários MLPs; na predição, a API/UI podem exibir **desvio entre membros** (não é intervalo de confiança calibrado).

### 6.4. Testes automatizados

```powershell
pytest tests/ -q
```

---

## 7. Fluxo com dados MNSOL reais

1. Baixe o pacote **MNSolDatabase-v2012** (ou exportação compatível) após a **licença UMN**.
2. Coloque o arquivo em `data/raw/` **apenas na sua máquina** (não faça commit).
3. Se o TXT não tiver coluna **SMILES**, crie `smiles_aux.tsv`:

   ```text
   entry_id	smiles
   123	CCO
   ```

4. Rode o ETL:

   ```powershell
   python scripts/run_etl.py data/raw/MNSol_alldata.txt -o data/processed/mnsol_clean.parquet --smiles-merge data/raw/smiles_aux.tsv --merge-on entry_id
   ```

   Ajuste `--merge-on` ao nome da coluna comum. Use `--allow-no-smiles` só se quiser Parquet sem treinar ainda.

5. Treine como na seção 6.

**Split químico:** o treino padrão usa folds por cluster; para datasets grandes, compare sempre com a literatura (Delfos reporta erros da ordem ~0.5–1 kcal/mol em cenários específicos — seu baseline MLP pode ser melhorado com arquiteturas do tipo Delfos/SolvBERT).

---

## 8. Executar a API (FastAPI)

Em um terminal, na raiz do projeto:

```powershell
$env:PYTHONPATH = "src"
$env:SOLVSCREEN_MODEL_PATH = "models/baseline.joblib"
python -m uvicorn api.main:app --reload --host 127.0.0.1 --port 8000
```

- Documentação interativa: [http://127.0.0.1:8000/docs](http://127.0.0.1:8000/docs)

### Exemplo: predição bulk com `curl` (PowerShell pode usar `Invoke-RestMethod`)

Corpo JSON mínimo:

```json
{
  "solute_smiles": "CCO"
}
```

Com solvente explícito (ex.: água aproximada por ε e n):

```json
{
  "solute_smiles": "c1ccccc1",
  "epsilon": 78.39,
  "n_refractive": 1.333
}
```

Resposta típica:

```json
{
  "delta_g_kcal_mol": -5.01,
  "unit": "kcal/mol",
  "uncertainty": null,
  "model_note": "morgan_r2_2048_plus_solvent8"
}
```

Com modelo **ensemble**, `uncertainty` pode trazer o **desvio entre membros**.

### Exemplo: stub de confinamento

```json
POST /predict/confinement
{
  "confinement_type": "graphene_slit",
  "effective_width_nm": 0.8,
  "ion": "Li+",
  "temperature_k": 298.15
}
```

Resposta: `status: "stub"` e lista de **targets sugeridos** alinhados ao schema (PMF, ΔG inserção, RDF, etc.).

---

## 9. Executar a interface Streamlit

Terminal 1 (API, opcional se usar só modelo local):

```powershell
$env:PYTHONPATH = "src"
$env:SOLVSCREEN_MODEL_PATH = "models/baseline.joblib"
python -m uvicorn api.main:app --host 127.0.0.1 --port 8000
```

Terminal 2:

```powershell
$env:PYTHONPATH = "src"
streamlit run streamlit_app/app.py
```

Ou:

```powershell
python scripts/run_streamlit.py
```

No painel: escolha **modelo local** e o caminho do `.joblib`, ou **API** com URL `http://127.0.0.1:8000`, informe **SMILES** e opcionalmente ε / n, e clique em **Calcular ΔG**.

---

## 10. Docker (só API)

```powershell
docker build -t solvscreen .
docker run -p 8000:8000 solvscreen
```

A imagem treina um modelo mínimo a partir do **fixture** durante o `build`. Para MNSOL real, adapte o Dockerfile ou monte volume com `baseline.joblib` e defina `SOLVSCREEN_MODEL_PATH`.

---

## 11. Integração contínua (GitHub Actions)

O workflow `.github/workflows/ci.yml` executa, em push/PR para `main`/`master`:

1. `pip install -r requirements.txt`
2. ETL no fixture → Parquet
3. Treino baseline → `models/ci_baseline.joblib`
4. `pytest tests/`

Isso garante que o **produto técnico** (pipeline + API + testes) permaneça reprodutível.

---

## 12. Como evoluir o projeto (ligação com a ciência)

| Meta | Próximo passo sugerido | Referência |
|------|------------------------|------------|
| Baseline mais forte | Substituir MLP por GNN ou modelo tipo **Delfos** / **SolvBERT**, mantendo o mesmo Parquet | Lim & Jung 2019; SolvBERT |
| Métricas publicáveis | Reportar MAE/RMSE no teste por cluster; comparar com Tabela/ESI do Delfos | *Chem. Sci.* 2019 |
| Incerteza calibrada | Conformal prediction, ensembles profundos, ou incerteza epistêmica/aleatória separada | Literatura de UQ em QSAR |
| Confinamento | Preencher JSON conforme `schemas/confinement_dataset.schema.json`; treinar surrogate; **não** misturar labels de poro com MNSOL bulk no mesmo alvo sem justificativa | Revisões GO + ML membranas; Shao (NSF) |
| Explicabilidade | SHAP em descritores ou attention maps em GNN | Ex.: XAI em membranas (EST) |

---

## 13. Problemas comuns

| Sintoma | Causa provável | Ação |
|---------|----------------|------|
| `Invalid SMILES` | SMILES incorreto ou RDKit não parseia | Corrigir string; testar no RDKit |
| `Model not found` | `SOLVSCREEN_MODEL_PATH` errado ou arquivo inexistente | Treinar ou apontar caminho correto |
| Colunas faltando no ETL | Arquivo não é MNSOL v2012 nem TSV com cabeçalho esperado | Conferir manual MNSOL ou exportar colunas padronizadas |
| API 503 após trocar modelo | Processo antigo em memória | Reiniciar `uvicorn` |
| Ensemble lento | N MLPs em bootstrap | Reduzir N ou usar GPU em implementações futuras |

---

## 14. Licença e dados

- Código do repositório: ver **`LICENSE`** (MIT), com nota de que **MNSOL** tem licença **separada** da UMN.
- **Não** commite arquivos brutos do MNSOL nem PDFs de periódicos sem direito de redistribuição; use links **DOI** nas citações.

---

## 15. Checklist rápido

- [ ] `pip install -r requirements.txt`
- [ ] ETL no fixture ou no MNSOL licenciado
- [ ] `run_train.py` gerou `.joblib`
- [ ] `pytest` verde
- [ ] API responde em `/docs`
- [ ] Streamlit calcula uma predição
- [ ] Artigos citados no relatório/banca (Delfos + MNSOL + evoluções escolhidas)

---

*Última atualização alinhada ao estado do repositório SolvScreen (pipeline bulk + stub confinamento + testes + UI).*
