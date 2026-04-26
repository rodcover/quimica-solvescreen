<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Quais datasets são usados para treinar Delfos e LSNN

Dá para responder com bastante segurança, porque isso está bem documentado.

### Delfos

- O Delfos é treinado em cima do **Minnesota Solvation Database (MNSOL)**, um banco com medidas experimentais de energias livres de solvatação e de transferência.[^1][^2]
- No artigo, eles mencionam usar **2 495 pares soluto–solvente** selecionados do MNSOL (dentro de um total de 3 037 entradas, 790 solutos, 92 solventes), todos com ΔG de solvatação/transferência experimental.[^2][^1]


### LSNN (Lambda Solvation Neural Network)

- O LSNN é um modelo de solvatação implícita baseado em GNN, treinado sobre um conjunto de aproximadamente **300 000 pequenas moléculas**.[^3][^4]
- Essas moléculas têm energias de solvatação obtidas por simulações alquemicas em solvente explícito; o LSNN é ajustado por *force matching* e por derivadas das variáveis alquemicas, para reproduzir essas energias livres com custo muito menor.[^4][^3]

Se você quiser, posso te ajudar a transformar isso em 1–2 frases para slide/artigo, explicando “Delfos foi treinado em X, LSNN em Y…”.
<span style="display:none">[^10][^5][^6][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://pubs.rsc.org/en/content/articlelanding/2019/sc/c9sc02452b

[^2]: https://pmc.ncbi.nlm.nih.gov/articles/PMC7017869/

[^3]: https://arxiv.org/abs/2510.20103

[^4]: https://arxiv.org/html/2510.20103v1

[^5]: https://chemrxiv.org/doi/full/10.26434/chemrxiv.8088482

[^6]: https://www.academia.edu/47863481/Deep_Learning_Model_for_Predicting_Solvation_Free_Energies_in_Generic_Organic_Solvents

[^7]: https://arxiv.org/html/2406.00183v1

[^8]: https://pubs.rsc.org/en/content/articlepdf/2019/sc/c9sc02452b

[^9]: https://pubs.aip.org/aip/jcp/article/161/23/234101/3325814/Predicting-solvation-free-energies-with-an

[^10]: https://sshep.snu.ac.kr/event/107/contributions/16/

