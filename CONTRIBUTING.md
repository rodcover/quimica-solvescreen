# Contribuindo

Obrigado pelo interesse em melhorar o SolvScreen.

## Antes de abrir um PR

1. **Não** inclua dados brutos do **MNSOL** nem PDFs com restrição de copyright.
2. Rode testes localmente: `pytest tests/ -q`
3. Opcional: `pre-commit run --all-files` (após `pip install -r requirements-dev.txt && pre-commit install`)

## Estilo de código

- Python 3.10+; preferência por 3.11.
- `ruff` configurado em `pyproject.toml` (hooks em `.pre-commit-config.yaml`).

## Escopo sugerido

- Correções de bugs no ETL ou na API.
- Melhorias de documentação (`docs/TUTORIAL.md`, `data/README.md`).
- Novos testes (incluindo validação de exemplos JSON contra o schema).
- Baselines adicionais **sem** substituir o contrato da API sem discussão (versionar endpoint se necessário).

## Confinamento

Modelos treinados para `POST /predict/confinement` devem ser acompanhados de schema de dados e métricas reprodutíveis; mantenha bulk e confinamento conceitualmente separados.
