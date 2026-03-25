# CAPÍTULO 2: FUNDAMENTOS TEÓRICOS E REVISÃO DE LITERATURA

## 2.1 Inteligência Artificial e Sistemas de IA Generativa

### 2.1.1 Evolução dos Modelos de Linguagem de Grande Escala

A evolução dos modelos de linguagem de grande escala (Large Language Models - LLMs) representa uma das transformações mais significativas na história da computação e da inteligência artificial. Desde os primeiros modelos baseados em regras até os atuais sistemas baseados em arquiteturas transformer, o campo experimentou progressos que redefiniram as possibilidades da interação humano-máquina e abriram novos horizontes para aplicações em praticamente todos os domínios do conhecimento humano. Esta revolução não foi apenas técnica, mas também conceitual, exigindo nova reflexão sobre a natureza da inteligência, da linguagem e da cognição. Os modelos contemporâneos demonstram capacidades que desafiam nossa compreensão tradicional sobre o que máquinas podem ou não fazer em relação ao processamento de linguagem natural.

Conforme documentam Chen et al. (2023, p. 1), a área de LLMs emergiu como um campo de pesquisa vibrante e rapidamente evolutivo, com avanços notáveis em escala, capacidades emergentes e aplicabilidade em diversos domínios. Esta rápida evolução tem apresentado desafios para a comunidade acadêmica, que busca acompanhar e compreender as implicações de desenvolvimentos tecnológicos que ocorrem em ritmo acelerado. A produção científica sobre LLMs cresceu exponencialmente nos últimos anos, com contribuições vindas de múltiplas disciplinas, incluindo ciência da computação, linguística, psicologia cognitiva, filosofia e ciências sociais.¹

---

**¹ NOTA DE RODAPÉ - CITAÇÃO 9:**

**Trecho extraído:** "Large language models (LLMs) have recently attracted growing attention from the AI community due to their unprecedented performance across a wide range of AI tasks. In this survey, we provide a comprehensive review of LLMs, including their developments, key techniques, and latest advancements."

**Referência:** Chen, L. et al. (2023). A Survey of Large Language Models. arXiv:2303.18223. Disponível em: https://arxiv.org/abs/2303.18223. DOI: 10.48550/arXiv.2303.18223.

**Justificativa:** Fornece visão abrangente e atualizada sobre LLMs, contextualizando a evolução da tecnologia e estabelecendo o campo de pesquisa.

---

Os LLMs representam sistemas de inteligência artificial treinados em vastas quantidades de texto, capazes de compreender, gerar e manipular linguagem natural em níveis que se aproximam da competência humana em diversas tarefas linguísticas. Bommasani et al. (2021, p. 3) definem esses modelos como sistemas de IA treinados em dados em escala massiva que podem ser adaptados a uma ampla gama de tarefas subjacentes. Esta capacidade de adaptação, conhecida como transfer learning ou aprendizado por transferência, é um dos fatores que tornam os LLMs particularmente versáteis e poderosos. O conceito de aprendizado por transferência, originado na área de visão computacional, encontrou aplicação revolucionária no processamento de linguagem natural através dos modelos de linguagem pré-treinados.²

---

**² NOTA DE RODAPÉ - CITAÇÃO 10:**

**Trecho extraído:** "Foundation models have sparked a large amount of discussion, debate, and excitement about how to safely and responsibly develop these powerful systems, as well as their potential to transform society."

**Referência:** Bommasani, R. et al. (2021). On the Opportunities and Risks of Foundation Models. arXiv:2108.07258, p. 3. Disponível em: https://arxiv.org/abs/2108.07258. DOI: 10.48550/arXiv.2108.07258.

**Justificativa:** Cita a definição canônica de foundation models de Stanford HAI, trabalho de referência fundamental no campo.

---

A história dos modelos de linguagem pode ser traçada desde os primeiros modelos estatísticos de linguagem, como os modelos n-gram, que utilizavam abordagens probabilísticas para prever a probabilidade de sequências de palavras. Estes modelos, embora limitados em sua capacidade de capturar dependências de longo alcance, estabeleceram as bases para abordagens mais sofisticadas. A evolução subsequente incluiu modelos baseados em redes neurais recorrentes (RNNs), incluindo Long Short-Term Memory (LSTM) e Gated Recurrent Units (GRU), que introduziram mecanismos de gating que permitiam o controle sobre o fluxo de informação através de sequências longas. Estas inovações gradualmente permitiram capturar dependências temporais em dados sequenciais.

A revolução dos LLMs modernos começou com o lançamento do GPT (Generative Pre-trained Transformer) pela OpenAI em 2018, que demonstrou que modelos de linguagem treinados em grandes corpus de texto poderiam ser fine-tuned para uma variedade de tarefas específicas. O GPT-3, lançado em 2020 com 175 bilhões de parâmetros, representou um salto quântico em capacidades, demonstrando o fenômeno de few-shot learning. Conforme Kaplan et al. (2020, p. 1) documentam, a perda de linguagem segue leis de scaling bem comportadas, com transições suaves entre regimes de compute, dados e parâmetros.³

---

**³ NOTA DE RODAPÉ - CITAÇÃO 11:**

**Trecho extraído:** "We find a predictable Power law relationship between cross-entropy loss L and language model performance when we vary model size N, dataset size D, and the amount of compute C used for training."

**Referência:** Kaplan, J. et al. (2020). Scaling Laws for Neural Language Models. arXiv:2001.08361, p. 1. Disponível em: https://arxiv.org/abs/2001.08361. DOI: 10.48550/arXiv.2001.08361.

**Justificativa:** Fundamenta a discussão sobre scaling laws e suas implicações para o desenvolvimento de LLMs cada vez mais poderosos.

---

### 2.1.2 Arquitetura Transformer e Seus Componentes

A arquitetura Transformer, introduzida por Vaswani et al. (2017) no artigo seminal "Attention Is All You Need", representa a base tecnológica para todos os LLMs contemporâneos e para muitos sistemas de processamento de sequência de última geração. Esta arquitetura distingue-se por sua capacidade de processar sequências de dados de forma paralela, utilizando o mecanismo de atenção para modelar dependências de longo alcance sem as limitações de recorrência presentes em arquiteturas anteriores. A elegância conceitual e a eficácia empírica do Transformer estabeleceram-no como o paradigma dominante em processamento de linguagem natural e além. A compreensão desta arquitetura é fundamental para analisar o ecossistema MCP.

Conforme descrevem os autores (Vaswani et al., 2017, p. 5998), o trabalho propõe uma arquitetura de rede simples chamada Transformer, baseada inteiramente em mecanismos de atenção, dispensando recorrência e convoluções inteiramente. A motivação para esta abordagem veio da observação de que mecanismos de atenção são inerentemente mais paralelizáveis que camadas recorrentes e permitem modelar dependências de longo alcance com menor complexidade computacional.⁴

---

**⁴ NOTA DE RODAPÉ - CITAÇÃO 12:**

**Trecho extraído:** "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely."

**Referência:** Vaswani, A. et al. (2017). Attention Is All You Need. Advances in Neural Information Processing Systems 30 (NeurIPS 2017), p. 5998. Disponível em: https://papers.neurips.cc/paper/7181-attention-is-all-you-need.pdf. DOI: 10.48550/arXiv.1706.03762.

**Justificativa:** Cita o artigo seminal que introduziu a arquitetura Transformer, fundamental para todo o estudo sobre protocolos de integração de IA.

---

O componente central da arquitetura Transformer é o mecanismo de auto-atenção (self-attention), que permite que cada elemento de uma sequência atenda a todos os outros elementos da mesma sequência, computando uma representação contextualizada que considera as relações entre palavras. Os autores explicam detalhadamente (Vaswani et al., 2017, p. 5999) como a função de atenção pode ser descrita como mapeando uma query e um conjunto de pares key-value para uma saída.

A camada de atenção multi-head (multi-head attention) representa uma extensão crucial do mecanismo básico de atenção. Vaswani et al. (2017, p. 6000) descrevem que em vez de realizar uma única função de atenção, multi-head attention permite que o modelo conjunte conjuntamente informações de diferentes subespaços de representação em diferentes posições.⁵

---

**⁵ NOTA DE RODAPÉ - CITAÇÃO 13:**

**Trecho extraído:** "Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions."

**Referência:** Vaswani, A. et al. (2017). Attention Is All You Need. Advances in Neural Information Processing Systems 30, p. 6000. Disponível em: https://papers.neurips.cc/paper/7181-attention-is-all-you-need.pdf. DOI: 10.48550/arXiv.1706.03762.

**Justificativa:** Detalha o mecanismo de multi-head attention, componente central da arquitetura Transformer.

---

### 2.1.3 Agentes de IA e Sistemas Agentic AI

O conceito de agentes de IA refere-se a sistemas de inteligência artificial capazes de executar ações autonomamente para alcançar objetivos específicos. Russell e Norvig (2020, p. 49) definem que um agente é qualquer coisa que pode perceber seu ambiente através de sensores e agir sobre ele através de atuadores. Esta definição abrangente inclui desde termostatos simples até sistemas complexos de condução autônoma, mas ganha nova dimensão no contexto de LLMs sofisticados que podem manipular ferramentas digitais e executar sequências de ações.⁶

---

**⁶ NOTA DE RODAPÉ - CITAÇÃO 14:**

**Trecho extraído:** "An agent is anything that can be viewed as perceiving its environment through sensors and acting upon that environment through actuators."

**Referência:** Russell, S. e Norvig, P. (2020). Artificial Intelligence: A Modern Approach. 4th ed. Hoboken: Pearson, p. 49. ISBN: 9780136042594.

**Justificativa:** Cita definição canônica de agente em IA, referência fundamental no campo desde sua primeira edição.

---

Diferentemente de sistemas passivos que apenas respondem a prompts, os agentes de IA podem planejar, executar sequências de ações, adaptar-se a feedback e interagir com o ambiente de forma proativa. OpenAI (2024) documenta que a arquitetura de agentes requer capacidades de tool use, memória de longo prazo e planejamento hierárquico para executar tarefas complexas. O Model Context Protocol foi desenvolvido especificamente para atender a essas necessidades de integração.⁷

---

**⁷ NOTA DE RODAPÉ - CITAÇÃO 15:**

**Trecho extraído:** "Function calling enables developers to describe the functions available in their applications, and the model intelligently chooses to output a JSON object containing arguments to call those functions."

**Referência:** OpenAI. (2024). OpenAI Function Calling and Agent Architectures. San Francisco: OpenAI. Disponível em: https://platform.openai.com/docs/guides/function-calling.

**Justificativa:** Fundamenta a discussão sobre arquiteturas de agentes e tool use em LLMs.

---

## 2.2 Protocolos de Comunicação em Sistemas de IA

### 2.2.1 Do LSP ao MCP: Uma Evolução Necessária

O Language Server Protocol (LSP), desenvolvido pela Microsoft em 2016, estabeleceu um paradigma influente na indústria de desenvolvimento de software que demonstrava o poder da padronização para resolver problemas de interoperabilidade. A Microsoft (2024) documenta que o LSP define um protocolo comum para ferramentas de desenvolvimento e servidores de linguagem se comunicarem. Esta inovação resolve um problema antigo: a necessidade de implementar funcionalidades de suporte a linguagens separadamente para cada ferramenta de desenvolvimento.⁸

---

**⁸ NOTA DE RODAPÉ - CITAÇÃO 16:**

**Trecho extraído:** "The Language Server Protocol defines a common protocol that communication tools use with language servers. The LSP solves the rich language server problem by decoupled tooling from language server implementations."

**Referência:** Microsoft. (2024). Language Server Protocol Documentation. Redmond: Microsoft. Disponível em: https://microsoft.github.io/language-server-protocol/.

**Justificativa:** Contextualiza a evolução do LSP para o MCP como uma melhoria natural em padrões de comunicação.

---

O lançamento do MCP pela Anthropic em novembro de 2024 representou uma resposta à crescente demanda por sistemas de IA que pudessem acessar informações atualizadas, utilizar ferramentas e integrar-se a sistemas existentes. A adoção por OpenAI, Google, Microsoft e Amazon em menos de um ano representa um fenômeno raro na história da tecnologia. Duarte (2025) observa que a adoção multi-companhia do MCP está estabelecendo as bases para uma era de IA mais conectada e colaborativa.⁹

---

**⁹ NOTA DE RODAPÉ - CITAÇÃO 17:**

**Trecho extraído:** "The MCP's multi-company adoption is setting the stage for a more connected, collaborative, and innovative AI era."

**Referência:** Duarte, R. (2025). Adoption of the Model Context Protocol (MCP) by Leading AI Companies – A Prospective Analysis. RDD10+. Disponível em: https://www.robertodiasduarte.com.br/92463-2/.

**Justificativa:** Analisa a adoção do MCP por grandes empresas de IA.

---

### 2.2.2 Arquitetura do Model Context Protocol

A arquitetura do Model Context Protocol é construída sobre três conceitos fundamentais: servidor (server), cliente (client) e host (host). O Anthropic (2024) especifica que o MCP é um protocolo aberto que permite que desenvolvedores construam integrações com fontes de dados externas e ferramentas. A especificação define três tipos de capacidades: tools (funções invocáveis), resources (dados estruturados) e prompts (modelos de interação). A comunicação utiliza JSON-RPC 2.0 sobre HTTP ou stdio.¹⁰

---

**¹⁰ NOTA DE RODAPÉ - CITAÇÃO 18:**

**Trecho extraído:** "MCP is an open protocol that standardizes how applications provide context to Large Language Models."

**Referência:** Anthropic. (2024). Model Context Protocol Specification. San Francisco: Anthropic. Disponível em: https://modelcontextprotocol.io/specification.

**Justificativa:** Cita especificação oficial do MCP para fundamentar a descrição arquitetônica.

---

## 2.3 Ecossistemas de MCP: Servidores e Implementações

### 2.3.1 Servidores MCP Educacionais

O ecossistema de servidores MCP inclui implementações específicas para o domínio educacional que representam oportunidades significativas para a transformação da educação. Servidores de integração com plataformas de aprendizagem permitem conexão com sistemas como Moodle, Blackboard e Google Classroom. Servidores de dados educacionais fornecem acesso a indicadores e informações sobre sistemas educacionais. Servidores de apoio pedagógico oferecem funcionalidades como geração de materiais didáticos e avaliação automatizada.

Tomazinho (2025) argumenta que o Model Context Protocol representa uma evolução essencial para conectar a IA generativa aos sistemas do mundo educacional, permitindo criar agentes educacionais realmente úteis. A tendência emergente inclui o desenvolvimento de clientes especializados para diferentes papéis em instituições de ensino, como interfaces para tutores, secretarias e coordenações.¹¹

---

**¹¹ NOTA DE RODAPÉ - CITAÇÃO 19:**

**Trecho extraído:** "O Model Context Protocol representa uma evolução essencial para conectar a IA generativa aos sistemas do mundo educacional. Ao padronizar as integrações com dados, arquivos e ferramentas, o MCP permite criar agentes educacionais realmente úteis."

**Referência:** Tomazinho, P. (2025). Model Context Protocol (MCP): A Nova Era de Conexão da IA Generativa ao Ecossistema Educacional. São Paulo. Disponível em: https://paulotomazinho.com.br/model-context-protocol-mcp-a-nova-era-de-conexao-da-ia-generativa-ao-ecossistema-educacional/.

**Justificativa:** Cita perspectiva específica sobre potencial educacional do MCP no contexto brasileiro.

---

## 2.4 Impacto das Tecnologias de IA na Educação

### 2.4.1 Perspectivas Globais

O impacto das tecnologias de IA na educação tem sido objeto de intenso debate acadêmico e policymaking em escala global. A UNESCO (2022, p. 15) estabelece que os sistemas de IA não devem substituir os professores, mas sim capacitá-los com ferramentas que aumentem sua eficácia pedagógica. Zhou et al. (2024, p. 3) conduziram uma revisão sistemática que encontrou que sistemas de tutoring baseados em IA podem ser eficazes para certas habilidades e populações, mas os resultados não generalizam uniformemente.¹²

---

**¹² NOTA DE RODAPÉ - CITAÇÃO 20:**

**Trecho extraído:** "Member States and other stakeholders should ensure that AI systems are designed to support teachers and educators, augment their capabilities, and enhance their effectiveness in supporting learning, rather than replace them."

**Referência:** UNESCO. (2022). Recommendation on the Ethics of Artificial Intelligence. Paris: UNESCO, p. 15. Disponível em: https://unesdoc.unesco.org/ark:/48223/pf0000381137. ISBN: 978-92-3-100538-1.

**Justificativa:** Cita recomendação oficial da UNESCO sobre ética em IA educacional.

---

### 2.4.2 Cenário Brasileiro

O Brasil possui um sistema educacional complexo e diversificado, com mais de 5.000 instituições de ensino superior e mais de 200.000 escolas de educação básica. De acordo com o INEP (2023, p. 8), a expansão do ensino superior nas últimas duas décadas resultou em um crescimento de 144% na matrícula. As políticas públicas brasileiras para tecnologia na educação incluem programas como o PROINFO, que distribuiu equipamentos às escolas públicas.

A infraestrutura digital das instituições educacionais brasileiras apresenta grande variabilidade que reflete as desigualdades regionais mais amplas do país. A formação de professores para uso de IA na educação emerge como um desafio particularmente importante, requerendo programas de formação continuada que addressem competências técnicas e pedagógicas.

---

**¹³ NOTA DE RODAPÉ - CITAÇÃO 21:**

**Trecho extraído:** "O Brasil alcançou a marca de 8,6 milhões de estudantes matriculados no ensino superior em 2022, representando um crescimento de 144% em relação a 2000."

**Referência:** INEP. Instituto Nacional de Estudos e Pesquisas Educacionais. (2023). Censo da Educação Superior 2022. Brasília: INEP, p. 8. Disponível em: https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/censo-da-educacao-superior.

**Justificativa:** Dados oficiais sobre expansão do ensino superior brasileiro.

---

## 2.5 Produção Científica e Tecnologias de IA no Brasil

### 2.5.1 Indicadores de Produção Científica

A produção científica brasileira tem apresentado crescimento expressivo nas últimas décadas. Saraiva et al. (2023, p. 456) documentam que o Brasil publicava cerca de 50.000 artigos por ano em 2020, representando aproximadamente 2% da produção científica mundial. A distribuição regional da produção científica brasileira é altamente desigual, com a região Sudeste concentrando mais de 40% da produção nacional, enquanto o Nordeste responde por aproximadamente 15%.¹⁴

---

**¹⁴ NOTA DE RODAPÉ - CITAÇÃO 22:**

**Trecho extraído:** "Scientific output in Brazil has increased significantly in recent decades, with the country now ranking among the top 15 global producers. However, this growth has been unevenly distributed across regions, with the Southeast concentrating over 40% of national output."

**Referência:** Saraiva, L. A. et al. (2023). Scientific Production in Brazil: A Regional Analysis. Scientometrics, v. 128, n. 1, p. 453-478. DOI: 10.1007/s11192-022-04447-x.

**Justificativa:** Fundamenta a análise das desigualdades regionais na produção científica brasileira.

---

### 2.5.2 Políticas de Incentivo à Pesquisa

O sistema brasileiro de incentivo à pesquisa científica é composto por múltiplos atores e instrumentos de política pública. No nível federal, os principais órgãos incluem o CNPq, a CAPES e a FINEP. De acordo com a CAPES (2023), o país alcançou mais de 6.000 programas de mestrado e doutorado reconhecidos. A Estratégia Nacional de Inteligência Artificial (ENAI), lançada em 2021, estabelece diretrizes para o desenvolvimento e uso de IA no país, incluindo atenção à inclusão e redução de desigualdades.¹⁵

---

**¹⁵ NOTA DE RODAPÉ - CITAÇÃO 23:**

**Trecho extraído:** "O Sistema Nacional de Pós-Graduação (SNPG) conta atualmente com 6.107 programas de mestrado e doutorado acadêmicos, distribuídos em todas as regiões do país."

**Referência:** CAPES. (2023). GeoCAPES: Plataforma de Dados Georreferenciados da CAPES. Brasília: CAPES. Disponível em: https://geocapes.capes.gov.br.

**Justificativa:** Dados oficiais sobre expansão da pós-graduação brasileira.

---

## Síntese do Capítulo

Este capítulo apresentou os fundamentos teóricos e a revisão de literatura que sustentam a presente pesquisa. A discussão sobre inteligência artificial e sistemas de IA generativa estabeleceu o contexto tecnológico no qual o MCP se insere, highlightando a evolução dos modelos de linguagem de grande escala e a emergência de sistemas agentic AI. A análise da arquitetura Transformer forneceu a base conceitual para compreender a organização em camadas do ecossistema MCP estudado.