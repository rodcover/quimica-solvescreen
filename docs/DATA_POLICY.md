# Política de dados e licenças

## Código

O software neste repositório é licenciado conforme o arquivo **`LICENSE`** (MIT), com exceção explícita: **bases de dados de terceiros** não são cobertas por essa licença.

## Minnesota Solvation Database (MNSOL)

- Proprietário / distribuidor: **University of Minnesota**.
- Uso típico: acadêmico / não comercial, mediante aceite de termos no site oficial.
- **Não** inclua arquivos brutos do MNSOL neste repositório público.
- Cite o MNSOL e o manual em publicações que usem medidas derivadas dele.

## Literatura e PDFs

- Não armazene no repositório PDFs de periódicos sem permissão explícita.
- Prefira **DOI** e links estáveis nas referências ([docs/REFERENCIAS.md](REFERENCIAS.md)).

## Dados de simulação / confinamento

- Registros no formato `schemas/confinement_dataset.schema.json` devem indicar `source_type` (`simulation`, `literature_extraction`, `hybrid`) e **citação** quando aplicável.
- Dados pessoais ou identificáveis não são escopo deste projeto; não os armazene no repositório.

## Logs de API

Se em produção você registrar predições, defina retenção e base legal (LGPD/GDPR) conforme seu contexto institucional.
