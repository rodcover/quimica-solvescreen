<img src="https://r2cdn.perplexity.ai/pplx-full-logo-primary-dark%402x.png" style="height:64px;margin-right:32px"/>

# Pesquise bases acadêmicas por publicações de Qing Shao desde 2022 sobre machine learning potentials para efeitos quânticos em hidratação iônica e transporte em confinamento nanométrico. Extraia resumos, métodos, achados chave sobre nanoporos, seletividade iônica e ferramentas computacionais. Compile em relatório PDF estruturado com tabela comparativa de estudos e análise de impactos em design de membranas nanofiltrantes

A partir do que está publicamente acessível, há registro detalhado do projeto de pesquisa de Qing Shao sobre desenvolvimento de potenciais de machine learning para efeitos quânticos em hidratação iônica e transporte em nanoconfinamento, mas praticamente não há ainda artigos já publicados (pós‑2022) especificamente com esses resultados; o trabalho está em andamento como projeto financiado pela NSF até 2026. Com base nisso, consigo organizar um relatório técnico com o que o projeto descreve (escopo, métodos, sistema‑modelo, impactos esperados) e apontar como isso se conecta ao design de membranas nanofiltrantes, mas não é possível extrair resumos/artigos específicos porque eles ainda não aparecem em bases abertas sob esse tema com autoria de Qing Shao.[^1][^2][^3]

## Escopo do projeto de Qing Shao (desde 2022)

- Projeto: “Developing Machine Learning Potential to Unravel Quantum Effect on Ionic Hydration and Transport in Nanoscale Confinement”.[^2][^3]
- Instituição: University of Kentucky, departamento de Chemical and Materials Engineering; Shao atua como PI (principal investigator).[^2]
- Período: 15/08/2022 a 31/07/2026, financiamento NSF (~US\$ 287 mil).[^2]
- Objetivo central: desenvolver um modelo computacional mais acurado (campo de força híbrido clássico–ML) para investigar e projetar materiais nanoporo­sos visando separação iônica altamente seletiva, incorporando efeitos quânticos na hidratação e no transporte em confinamento de 1–2 nm.[^3][^2]


## Metodologia computacional e potenciais de ML

O projeto propõe um **campo de força híbrido** combinando:[^3][^2]

- Componente de longo alcance: potencial eletrostático clássico para tratar interações coulombianas e não ligantes de longo alcance.
- Componente de curto alcance: potencial de rede neural (machine learning potential) treinado em configurações obtidas de cálculos de mecânica quântica (primeiros princípios), incorporando explicitamente efeitos quânticos na energia e forças locais.

Principais tarefas descritas:[^2]

1. Desenvolver força de campo híbrida clássico–ML capaz de reproduzir termodinâmica e estrutura de solvatação iônica em solução aquosa a granel (validação em bulk).
2. Investigar o efeito quântico na estrutura e dinâmica de água confinada em nanotubos de carbono e fendas de grafeno (quantum effects on confined water).
3. Estudar o efeito do nanoconfinamento na energia livre para entrada/solvatação de íons em nanopores, usando o campo de força híbrido, para quantificar a relação “solvatação–transporte–energia livre” sob confinamento.

Esse desenho metodológico é consistente com a tendência recente de usar “deep neural network potentials” treinados em dados ab initio para simular água e íons confinidos com acurácia de primeiros princípios, mas custo próximo de MD clássica.[^4][^5]

## Sistemas-modelo: nanoporos, íons e hidratação

O projeto define explicitamente os sistemas de estudo.[^3][^2]

- Nanoporos:
    - Nanotubos de carbono (carbon nanotubes, CNTs).
    - “Graphene slits” (fendas de grafeno, representando canais 2D em folhas empilhadas).
- Íons modelo:
    - Li⁺, Mg²⁺, Ca²⁺ em solução aquosa.[^2]
    - São escolhidos por terem raio iônico/hidratação diferentes, o que enfatiza seletividade de carga e tamanho em confinamento nanométrico (relevante para separações de dureza, dessalinização seletiva, etc.).[^3][^2]
- Propriedades alvo:
    - Estrutura de hidratação (coordenação, distribuição radial, reorientação da água) em bulk e em confinamento.[^2]
    - Dinâmica de água e íons (coeficientes de difusão, tempos de residência) sob confinamento.[^2]
    - Energia livre de transferência da solução a granel para dentro do nanoporo (barreira de entrada) e contribuição dos efeitos quânticos nessa energia.[^2]

A hipótese central é que um potencial de rede neural treinado em um conjunto de configurações de tamanho “adequado” consegue equilibrar a descrição dos efeitos quânticos locais (polarização, reorganização da rede de H‑ligações) com interações de longo alcance, produzindo predições confiáveis da estrutura e dinâmica iônica em nanopores.[^3][^2]

## Seletividade iônica, transporte e implicações para membranas

O texto do projeto deixa claro que o foco final é compreender e explorar a **seletividade iônica de nanopores** para aplicações de separação e nanofiltração.[^3][^2]

Aspectos-chave que o projeto pretende quantificar:

- Como o confinamento em 1–2 nm amplifica diferenças sutis entre íons (carga, raio hidratado, estrutura de hidratação), tornando a seletividade mais pronunciada que em bulk.[^3][^2]
- Como efeitos quânticos (tratados via ML potentials treinados em dados quânticos) alteram:
    - energias de hidratação;
    - barreiras de desolvatação parcial na entrada do poro;
    - reorganização da água e da rede de H‑ligações dentro do canal.[^2]
- A relação quantitativa ou semi‑quantitativa entre “solvation–transport–free energy” para íons confinados, isto é, como mudanças na energia livre de solvatação dentro do poro se traduzem em permeabilidade e seletividade.[^2]

Impacto esperado para design de membranas nanofiltrantes:

- O resultado central esperado é um **campo de força clássico–ML parametrizado para sistemas água+íons+nanoporo**, incluindo efeitos quânticos relevantes; esse tipo de ferramenta permite, em princípio, testar virtualmente diferentes quimias de superfície, tamanhos de poro e geometrias, antes de síntese experimental.[^2]
- A partir de mapas de energia livre para Li⁺, Mg²⁺ e Ca²⁺ em CNTs/fendas de grafeno, pode‑se derivar regras de projeto, por exemplo:
    - ajuste de diâmetro de poro para maximizar seletividade entre monovalentes/divalentes;
    - funcionalizações (cargas, grupos polares) que estabilizam seletivamente certos íons;
    - densidade de poros que equilibra fluxo e rejeição.[^2]
- O projeto explicita que a “primary intellectual merit” é criar ferramentas e conhecimento que “enable precise design of nanoporous materials for ionic selectivity and other substrates that are hard to separate”.[^3][^2]

Embora não sejam ainda publicações do grupo de Shao, há trabalhos recentes que ilustram a mesma filosofia metodológica:

- uso de machine-learning potential MD para estudar água confinada entre camadas 2D (MXenes, TiO₂ nanopores, CNTs), revelando mudanças em estrutura, difusão e transferência de prótons com acurácia quântica.[^5][^4]
- desenvolvimento de modelos de deep learning para dinâmica de íons em nanopores, em escalas que métodos puramente ab initio não alcançam.[^6][^5]


## Tabela de escopo dos estudos (2022–2026)

Com base apenas nas informações públicas do projeto e em trabalhos correlatos de ML‑MD em nanoconfinamento (não necessariamente de Shao), podemos organizar o seguinte quadro:


| Estudo/projeto (ano) | Metodologia ML/MD | Nanoporos e íons | Foco em seletividade/transporte | Impacto potencial em membranas |
| :-- | :-- | :-- | :-- | :-- |
| “Developing Machine Learning Potential to Unravel Quantum Effect on Ionic Hydration and Transport in Nanoscale Confinement”, Shao (NSF, 2022–2026) | Força de campo híbrida clássico–ML; longo alcance eletrostático + potencial de rede neural de curto alcance treinado em dados quânticos para água e íons | Nanotubos de carbono, fendas de grafeno; íons Li⁺, Mg²⁺, Ca²⁺ em solução aquosa | Quantificar efeitos quânticos em estrutura/dinâmica de água confinada; energia livre de entrada e solvatação de íons; relação solvation–transport–free energy sob confinamento 1–2 nm | Geração de ferramenta de simulação para projetar nanoporos com seletividade íônica fina; orientar parametrização de membranas nanofiltrantes com alto contraste entre mono/divalentes e otimização de fluxo.[^2][^3] |
| Estudos recentes de ML‑MD de água e prótons em nanopores (outros grupos, 2023–2024) | Potenciais de deep learning para água e prótons, derivados de cálculos DFT; MD de larga escala sob confinamento em nanotubos e materiais 2D | Nanopores em MXenes, TiO₂, CNTs; água pura ou com prótons | Entender como confinamento altera rede de H‑ligações, difusão de água/protons e transferência protônica com acurácia quântica | Metodologias análogas às de Shao, mostrando viabilidade de ML‑MD para guiar design de canais iônicos e membranas com condutividade/proton seletiva.[^4][^5] |

## Sobre o PDF solicitado

Tentei gerar diretamente um PDF estruturado com tabela comparativa via ambiente Python, mas houve erro técnico de codificação de caracteres (null bytes) e o arquivo não foi criado corretamente.  Dado esse limite, o conteúdo acima já está estruturado em seções e tabela de forma que você possa:[^1]

- copiar diretamente para um processador de texto (Word/Google Docs/LaTeX);
- exportar para PDF localmente, ajustando o formato às suas necessidades (por exemplo, adicionando capa, sumário e logotipos institucionais).

Se quiser, posso na próxima interação gerar o código LaTeX completo de um relatório com capa, seções e tabela, pronto para você compilar em PDF, ou refinar o texto em português formal voltado a um público específico (por exemplo, comitê de P\&D, agência de fomento ou time de engenharia de processos).
<span style="display:none">[^10][^7][^8][^9]</span>

<div align="center">⁂</div>

[^1]: https://www.sciencedirect.com/author/55370310500/qing-shao

[^2]: https://pubs.acs.org/doi/abs/10.1021/acs.jpcc.1c08297

[^3]: https://scholars.uky.edu/en/projects/developing-machine-learning-potential-to-unravel-quantum-effect-o/

[^4]: https://www.science.org/doi/10.1126/sciadv.adz1780

[^5]: https://pubs.acs.org/doi/10.1021/acs.jpclett.3c01054

[^6]: https://chemrxiv.org/doi/pdf/10.26434/chemrxiv-2024-3p7hg

[^7]: https://arxiv.org/pdf/2303.04594.pdf

[^8]: https://www.tandfonline.com/doi/full/10.1080/19475411.2023.2288954

[^9]: https://pmc.ncbi.nlm.nih.gov/articles/PMC10214387/

[^10]: https://pubs.acs.org/doi/10.1021/ac401536g

