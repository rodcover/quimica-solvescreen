<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Como baixar o dataset MNSOL para Delfos

Sim, dá para baixar o MNSOL, mas ele não está “no GitHub do Delfos”; vem do site de Minnesota.

### Caminho mais direto (acadêmico / não comercial)

1. Acesse a página oficial do MNSOL:
    - Home: Minnesota Solvation Database Home Page.[^1]
    - Site de distribuição: Minnesota Solvation Database Distribution Site.[^2]
2. No site de distribuição, eles deixam claro que:
    - A base é gratuita para uso **acadêmico/governo/sem fins lucrativos**, mas requer aceitação de licença de uso.[^1][^2]
    - O download é feito via web após você concordar com os termos (não redistribuir, uso não comercial, etc.).[^2][^1]
3. Versão e formato do arquivo:
    - A versão atual disponibilizada é a **MNSolDatabase‑v2012**, baixada como arquivo `MNSolDatabase-v2012.tar.gz` ou similar.[^3][^4]
    - Dentro dele há:
        - Um arquivo tab-delimited `MNSol_alldata.txt` com todos os dados.
        - Uma planilha `MNSol_alldata.xls`.
        - Manual em PDF explicando colunas, unidades e formatos.[^4]
4. Passos práticos (Linux/macOS, por exemplo):
    - Baixe o `.tar.gz` pela página de distribuição (após aceitar a licença).[^2]
    - No terminal:
        - `gunzip MNSolDatabase-v2012.tar.gz`
        - `tar -xvf MNSolDatabase-v2012.tar`
    - Os arquivos de dados e o manual ficarão em um diretório tipo `MNSolDatabase-v2012/`.[^4]

Isso é exatamente o que o pessoal do Delfos usou: eles pegam as 3 037 entradas do MNSOL (790 solutos, 92 solventes) e a partir daí constroem o dataset de ~2 495 pares soluto–solvente usados no treino/validação.[^5][^6]
<span style="display:none">[^10][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://comp.chem.umn.edu/mnsol/

[^2]: https://comp.chem.umn.edu/sds/mnsol/mnsol.cgi

[^3]: https://conservancy.umn.edu/items/c3db00cf-d573-461b-adf5-389ff929d918

[^4]: https://comp.chem.umn.edu/mnsol/MNSol-v2012_Manual.pdf

[^5]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7017869/

[^6]: https://pubs.rsc.org/en/content/articlelanding/2019/sc/c9sc02452b

[^7]: https://license.umn.edu/product/minnesota-solvation-mnsol-database

[^8]: https://pubs.acs.org/doi/10.1021/acs.jpcb.3c07447

[^9]: https://github.com/OpenFreeEnergy/openfe-benchmarks/pulls

[^10]: https://github.com/su-group/SolvBERT

