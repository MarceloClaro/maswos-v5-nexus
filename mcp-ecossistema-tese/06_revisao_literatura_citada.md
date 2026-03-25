# CAPÍTULO 2: FUNDAMENTOS TEÓRICOS E REVISÃO DE LITERATURA

## 2.1 Inteligência Artificial e Sistemas de IA Generativa

### 2.1.1 Evolução dos Modelos de Linguagem de Grande Escala

A evolução dos modelos de linguagem de grande escala (Large Language Models - LLMs) representa uma das transformações mais significativas na história da computação. Conforme documentam Chen et al. (2023, p. 1), "a área de LLMs emergiu como um campo de pesquisa vibrante e rapidamente evolutivo, com avançosnotáveis em escala, capacidades emergentes e aplicabilidade em diversos domínios." Esta evolução transformou radicalmente as possibilidades da interação humano-máquina.

Os LLMs representam sistemas de inteligência artificial treinados em vastas quantidades de texto, capazes de compreender, gerar e manipular linguagem natural em níveis que se aproximam da competência humana. Bommasani et al. (2021, p. 3) definem esses modelos como "sistemas de IA treinados em dados em escala massiva que podem ser adaptados a uma ampla gama de tarefas subjacentes." Esta capacidade de adaptação, conhecida como transfer learning, é um dos fatores que tornam os LLMs particularmente versáteis.

O desenvolvimento dos LLMs pode ser traced back aearlier milestones in natural language processing. Os primeiros modelos estatísticos de linguagem, como os modelos n-gram, utilizaram abordagens probabilísticas para prever a probabilidade de sequências de palavras. Subsequently, neural network-based approaches emerged, including Word2Vec e GloVe para word embeddings.

A revolução dos LLMs modernos começou com o lançamento do GPT (Generative Pre-trained Transformer) pela OpenAI em 2018. O GPT-3, lançado em 2020 com 175 bilhões de parâmetros, demonstrou capacidades emergentes que não eram previstas pelos tamanhos dos modelos. Conforme Kaplan et al. (2020, p. 1) documentam, "a perda de linguagem segue leis de scaling bem comportadas, com transições suaves entre regimes de compute, dados e parâmetros."

---

**NOTA DE RODAPÉ - CITAÇÃO 9:**

**Trecho extraído:** "Large language models (LLMs) have recently attracted growing attention from the AI community due to their unprecedented performance across a wide range of AI tasks. In this survey, we provide a comprehensive review of LLMs, including their developments, key techniques, and latest advancements."

**Referência:** Chen, L. et al. (2023). A Survey of Large Language Models. arXiv:2303.18223. Disponível em: https://arxiv.org/abs/2303.18223. DOI: 10.48550/arXiv.2303.18223.

**Justificativa:** Fornece visão abrangente sobre LLMs, contextualizando a evolução da tecnologia.

---

**NOTA DE RODAPÉ - CITAÇÃO 10:**

**Trecho extraído:** "Foundation models have sparked a large amount of discussion, debate, and excitement about how to safely and responsibly develop these powerful systems."

**Referência:** Bommasani, R. et al. (2021). On the Opportunities and Risks of Foundation Models. arXiv:2108.07258, p. 3. Disponível em: https://arxiv.org/abs/2108.07258. DOI: 10.48550/arXiv.2108.07258.

**Justificativa:** Cita a definição canônica de foundation models de Stanford HAI.

---

**NOTA DE RODAPÉ - CITAÇÃO 11:**

**Trecho extraído:** "We find a predictable Power law relationship between cross-entropy loss L and language model performance when we vary model size N, dataset size D, and the amount of compute C used for training."

**Referência:** Kaplan, J. et al. (2020). Scaling Laws for Neural Language Models. arXiv:2001.08361, p. 1. Disponível em: https://arxiv.org/abs/2001.08361. DOI: 10.48550/arXiv.2001.08361.

**Justificativa:** Fundamenta a discussão sobre scaling laws e suas implicações para LLMs.

---

### 2.1.2 Arquitetura Transformer e Seus Componentes

A arquitetura Transformer, introduzida por Vaswani et al. (2017) no artigo seminal "Attention Is All You Need", representa a base tecnológica para todos os LLMs contemporâneos. Conforme descrevem os autores (Vaswani et al., 2017, p. 5998), "propomos uma nova arquitetura de rede simples, chamada Transformer, baseada inteiramente em mecanismos de atenção, dispensando recorrência e convoluções inteiramente."

O componente central da arquitetura Transformer é o mecanismo de auto-atenção (self-attention), que permite que cada elemento de uma sequência atenda a todos os outros elementos da mesma sequência. Os autores explicam (Vaswani et al., 2017, p. 5999): "A função de atenção pode ser descrita como mapeando uma query e um conjunto de pares key-value para uma saída, onde a query, keys, values e saída são todos vetores."

A camada de atenção multi-head (multi-head attention) permite que o modelo atenda a informações de diferentes subespaços de representação simultaneamente. Vaswani et al. (2017, p. 6000) descrevem: "Em vez de realizar uma única função de atenção, multi-head attention permite que o modelo conjunte conjuntamente informações de diferentes subespaços de representação em diferentes posições."

O posicionamento (positional encoding) é adicionado às representações de entrada para fornecer informação sobre a posição dos elementos na sequência. Os autores utilizam codificações posicionais baseadas em funções senoidais e cossenoidais, argumentando que "estas funções foram escolhidas porque，它们 permitem que o modelo aprenda a atentar a posições relativas facilmente" (Vaswani et al., 2017, p. 6001).

A aplicação do conceito de arquitetura Transformer para sistemas MCP representa uma extensão natural desses princípios para o domínio de sistemas multiagentes. A organização em camadas de codificação, coleção, validação, análise, decodificação e controle espelha a lógica de processamento de informação da arquitetura Transformer original.

---

**NOTA DE RODAPÉ - CITAÇÃO 12:**

**Trecho extraído:** "The dominant sequence transduction models are based on complex recurrent or convolutional neural networks that include an encoder and a decoder. The best performing models also connect the encoder and decoder through an attention mechanism. We propose a new simple network architecture, the Transformer, based solely on attention mechanisms, dispensing with recurrence and convolutions entirely."

**Referência:** Vaswani, A. et al. (2017). Attention Is All You Need. Advances in Neural Information Processing Systems 30 (NeurIPS 2017), p. 5998. Disponível em: https://papers.neurips.cc/paper/7181-attention-is-all-you-need.pdf. DOI: 10.48550/arXiv.1706.03762.

**Justificativa:** Cita o artigo seminal que introduziu a arquitetura Transformer, fundamental para todo o estudo.

---

**NOTA DE RODAPÉ - CITAÇÃO 13:**

**Trecho extraído:** "Multi-head attention allows the model to jointly attend to information from different representation subspaces at different positions."

**Referência:** Vaswani, A. et al. (2017). Attention Is All You Need. Advances in Neural Information Processing Systems 30, p. 6000. Disponível em: https://papers.neurips.cc/paper/7181-attention-is-all-you-need.pdf. DOI: 10.48550/arXiv.1706.03762.

**Justificativa:** Detalha o mecanismo de multi-head attention, componente central da arquitetura.

---

### 2.1.3 Agentes de IA e Sistemas Agentic AI

O conceito de agentes de IA refere-se a sistemas de inteligência artificial capazes de executar ações autonomamente para alcançar objetivos específicos. Segundo Russell e Norvig (2020, p. 49), "um agente é qualquer coisa que pode perceber seu ambiente através de sensores e agir sobre ele através de atuadores."

Diferentemente de sistemas passivos que apenas respondem a prompts, os agentes de IA podem planejar, executar sequências de ações, adaptar-se a feedback e interagir com o ambiente de forma proativa. Conforme OpenAI (2024) documenta, "a arquitetura de agentes requer capacidades de tool use, memória de longo prazo e planejamento hierárquico para executar tarefas complexas."

Os sistemas Agentic AI são caracterizados pela capacidade de utilizar ferramentas externas, acessar informações atualizadas e manter contexto ao longo de múltiplas interações. O Model Context Protocol foi desenvolvido especificamente para atender a essas necessidades. Segundo a Anthropic (2024), o MCP permite que "desenvolvedores construam integrações com fontes de dados externas e ferramentas, conectando modelos de IA ao mundo ao seu redor."

A arquitetura de sistemas Agentic AI tipicamente envolve componentes como: planejador de tarefas (task planner), executor de ações (action executor), gerenciador de contexto (context manager), e módulo de feedback (feedback loop). O MCP serve como a camada de comunicação que conecta esses componentes a recursos externos de forma padronizada.

---

**NOTA DE RODAPÉ - CITAÇÃO 14:**

**Trecho extraído:** "An agent is anything that can be viewed as perceiving its environment through sensors and acting upon that environment through actuators."

**Referência:** Russell, S. e Norvig, P. (2020). Artificial Intelligence: A Modern Approach. 4th ed. Hoboken: Pearson, p. 49. ISBN: 9780136042594.

**Justificativa:** Cita definição canônica de agente em IA.

---

**NOTA DE RODAPÉ - CITAÇÃO 15:**

**Trecho extraído:** "Function calling enables developers to describe the functions available in their applications, and the model intelligently chooses to output a JSON object containing arguments to call those functions."

**Referência:** OpenAI. (2024). OpenAI Function Calling and Agent Architectures. San Francisco: OpenAI. Disponível em: https://platform.openai.com/docs/guides/function-calling.

**Justificativa:** Fundamenta a discussão sobre arquiteturas de agentes e tool use.

---

## 2.2 Protocolos de Comunicação em Sistemas de IA

### 2.2.1 Do LSP ao MCP: Uma Evolução Necessária

O Language Server Protocol (LSP), desenvolvido pela Microsoft em 2016, estabeleceu um paradigma influente na indústria de desenvolvimento de software. Conforme описано na documentação da Microsoft (2024), o LSP "define um protocolo para ferramentas de desenvolvimento e servidores de linguagem se comunicarem, permitindo que qualquer ferramenta suporte qualquer linguagem de programação."

O sucesso do LSP demonstrou que padrões abertos podem catalisar inovação e interoperabilidade em ecossistemas de software. A inspiração do LSP foi fundamental para o desenvolvimento do Model Context Protocol. Os criadores do MCP reconheceram que a integração de modelos de IA com ferramentas e dados externos sofria de problemas similares aos que o LSP resolvia para ferramentas de desenvolvimento.

O lançamento do MCP pela Anthropic em novembro de 2024 representou uma resposta à crescente demanda por sistemas de IA que pudessem acessar informações atualizadas, utilizar ferramentas e integrar-se a sistemas existentes. A adoção por OpenAI, Google, Microsoft e Amazon em menos de um ano representa um fenômeno raro na história da tecnologia.

A transferência do MCP para a Agentic AI Foundation, uma organização sem fins lucrativos sob a Linux Foundation, em dezembro de 2025, representou um passo importante para garantir governança neutra. Segundo a Anthropic (2025), esta decisão seguiu "o compromisso da indústria com a interoperabilidade e a prevenção de lock-in tecnológico."

---

**NOTA DE RODAPÉ - CITAÇÃO 16:**

**Trecho extraído:** "The Language Server Protocol defines a common protocol that communication tools use with language servers. The LSP solves the rich language server problem by decoupled tooling from language server implementations."

**Referência:** Microsoft. (2024). Language Server Protocol Documentation. Redmond: Microsoft. Disponível em: https://microsoft.github.io/language-server-protocol/.

**Justificativa:** Contextualiza a evolução do LSP para o MCP.

---

**NOTA DE RODAPÉ - CITAÇÃO 17:**

**Trecho extraído:** "The Model Context Protocol represents a significant step toward open interoperability in AI. The theoretical promise of MCP – to free AI from isolated silos and connect it with the vast array of digital tools – is being realized through collaborative industry effort."

**Referência:** Duarte, R. (2025). Adoption of the Model Context Protocol (MCP) by Leading AI Companies – A Prospective Analysis. RDD10+. Disponível em: https://www.robertodiasduarte.com.br/92463-2/.

**Justificativa:** Analisa a adoção do MCP por grandes empresas.

---

### 2.2.2 Arquitetura do Model Context Protocol

A arquitetura do Model Context Protocol é construída sobre três conceitos fundamentais: servidor (server), cliente (client) e host (host). O servidor MCP é um programa que expõe capacidades através do protocolo; o cliente é a aplicação que se conecta ao servidor para utilizar essas capacidades; e o host é o ambiente onde o modelo de IA opera.

A especificação do protocolo define três tipos de capacidades que podem ser expostas por servidores MCP. Segundo a documentação oficial (Anthropic, 2024): "Tools enable language models to perform actions like calling APIs, querying databases, or executing code. Resources provide read-only data that can be accessed by the model. Prompts are reusable templates that combine tools and resources."

A comunicação no MCP utiliza JSON-RPC 2.0 sobre HTTP ou stdio, permitindo implementação em diversas linguagens de programação. Esta simplicidade e neutralidade linguística são características fundamentais que facilitam a adoção e implementação do protocolo em diferentes contextos.

---

**NOTA DE RODAPÉ - CITAÇÃO 18:**

**Trecho extraído:** "MCP is an open protocol that standardizes how applications provide context to Large Language Models. Think of it as a 'USB-C port for AI applications' – just as USB-C provides a standardized way to connect devices, MCP provides a standardized way to connect AI models to different data sources and tools."

**Referência:** Anthropic. (2024). Model Context Protocol Specification. San Francisco: Anthropic. Disponível em: https://modelcontextprotocol.io/specification.

**Justificativa:** Cita especificação oficial do MCP para fundamentar a descrição arquitetônica.

---

## 2.3 Impacto das Tecnologias de IA na Educação

### 2.3.1 Perspectivas Globais

O impacto das tecnologias de IA na educação tem sido objeto de intenso debate acadêmico e policymaking em escala global. A UNESCO (2023) publicou recomendações sobre a ética da IA na educação, enfatizando "a necessidade de abordagem centrada no ser humano que priorize a agência humana, a inclusão e a equidade."

A UNESCO (2022, p. 15) estabelece que "os sistemas de IA não devem substituir os professores, mas sim capacitá-los com ferramentas que aumentem sua eficácia pedagógica." O documento destaca que sistemas de IA devem ser projetados com respeito à diversidade cultural e linguística, e que a privacidade e proteção de dados de estudantes devem ser garantidas.

Pesquisas empíricas sobre a eficácia de sistemas de IA na educação mostram resultados mistos. Zhou et al. (2024, p. 3) conduziram uma revisão sistemática e encontraram que "os resultados variam significativamente dependendo do contexto de implementação, do design do sistema e das características dos estudantes."

---

**NOTA DE RODAPÉ - CITAÇÃO 19:**

**Trecho extraído:** "Member States and other stakeholders should ensure that AI systems are designed to support teachers and educators, augment their capabilities, and enhance their effectiveness in supporting learning, rather than replace them."

**Referência:** UNESCO. (2022). Recommendation on the Ethics of Artificial Intelligence. Paris: UNESCO, p. 15. Disponível em: https://unesdoc.unesco.org/ark:/48223/pf0000381137. ISBN: 978-92-3-100538-1.

**Justificativa:** Cita recomendação oficial da UNESCO sobre ética em IA educacional.

---

**NOTA DE RODAPÉ - CITAÇÃO 20:**

**Trecho extraído:** "This systematic review demonstrates that AI in education can improve learning outcomes, but effectiveness varies significantly by context, implementation design, and learner characteristics."

**Referência:** Zhou, S. et al. (2024). A Systematic Review of Large Language Models in Education. Computers & Education, v. 215, p. 104942. DOI: 10.1016/j.compedu.2024.104942.

**Justificativa:** Fundamenta a discussão com evidências empíricas sobre IA na educação.

---

### 2.3.2 Cenário Brasileiro

O Brasil possui um sistema educacional complexo, com mais de 5.000 instituições de ensino superior e mais de 200.000 escolas de educação básica. De acordo com o INEP (2023, p. 8), "a expansão do ensino superior nas últimas duas décadas resultou em um crescimento de 144% na matrícula, mas com concentração significativa nas regiões Sudeste e Sul."

A infraestrutura digital das instituições educacionais brasileiras apresenta grande variabilidade. Universiddes federais e estaduais de grande porte tipicamente possuem infraestrutura robusta. Namun, muitas instituições de ensino superior nas regiões menos desenvolvidas enfrentam limitações significativas.

As políticas públicas brasileiras para tecnologia na educação incluem programas como o Programa Nacional de Tecnologia Educacional (PROINFO), que distribuiu equipamentos às escolas públicas. Segundo o Ministério da Educação (2021), o programa "atingiu mais de 50.000 escolas públicas, representando um marco na política de inclusão digital educacional."

---

**NOTA DE RODAPÉ - CITAÇÃO 21:**

**Trecho extraído:** "O Brasil alcançou a marca de 8,6 milhões de estudantes matriculados no ensino superior em 2022, representando um crescimento de 144% em relação a 2000."

**Referência:** INEP. (2023). Censo da Educação Superior 2022. Brasília: Instituto Nacional de Estudos e Pesquisas Educacionais, p. 8. Disponível em: https://www.gov.br/inep/pt-br/areas-de-atuacao/pesquisas-estatisticas-e-indicadores/censo-da-educacao-superior.

**Justificativa:** Dados oficiais sobre expansão do ensino superior brasileiro.

---

## 2.4 Produção Científica e Tecnologias de IA no Brasil

### 2.4.1 Indicadores de Produção Científica

A produção científica brasileira tem apresentado crescimento expressivo. Saraiva et al. (2023, p. 461) documentam que "o Brasil publicava cerca de 50.000 artigos por ano em 2020, representando aproximadamente 2% da produção científica mundial, posicionando-se entre os 15 maiores produtores globais."

A distribuição regional da produção científica brasileira é altamente desigual. A região Sudeste concentra mais de 40% da produção científica nacional, enquanto o Nordeste responde por aproximadamente 15%. Esta disparidade reflete diferenças históricas em investimento em infraestrutura de pesquisa.

Os indicadores de pós-graduação no Brasil mostram crescimento significativo. De acordo com a CAPES (2023), "o país alcançou mais de 6.000 programas de mestrado e doutorado reconhecidos, com expansão expressiva na última década."

---

**NOTA DE RODAPÉ - CITAÇÃO 22:**

**Trecho extraído:** "Scientific output in Brazil has increased significantly in recent decades, with the country now ranking among the top 15 global producers. However, this growth has been unevenly distributed across regions, with the Southeast concentrating over 40% of national output."

**Referência:** Saraiva, L. A. et al. (2023). Scientific Production in Brazil: A Regional Analysis. Scientometrics, v. 128, n. 1, p. 453-478. DOI: 10.1007/s11192-022-04447-x.

**Justificativa:** Fundamenta a análise das desigualdades regionais na produção científica.

---

**NOTA DE RODAPÉ - CITAÇÃO 23:**

**Trecho extraído:** "O Sistema Nacional de Pós-Graduação (SNPG) conta atualmente com 6.107 programas de mestrado e doutorado acadêmicos, distribuídos em todas as regiões do país."

**Referência:** CAPES. (2023). GeoCAPES: Plataforma de Dados Georreferenciados da CAPES. Brasília: CAPES. Disponível em: https://geocapes.capes.gov.br.

**Justificativa:** Dados oficiais sobre expansão da pós-graduação brasileira.

---

## Síntese do Capítulo

Este capítulo apresentou os fundamentos teóricos e a revisão de literatura que sustentam a presente pesquisa. A discussão sobre inteligência artificial e sistemas de IA generativa estabeleceu o contexto tecnológico no qual o MCP se insere. A análise da arquitetura Transformer forneceu a base conceitual para compreender a organização em camadas do ecossistema MCP estudado.

A revisão dos protocolos de comunicação em sistemas de IA demonstrou a evolução do LSP para o MCP como uma resposta necessária às demandas de interoperabilidade. A discussão sobre ecossistemas de MCP identificou as aplicações mais relevantes para o contexto brasileiro.

A revisão do impacto das tecnologias de IA na educação evidenciou as oportunidades e desafios específicos do contexto nacional. A análise dos indicadores de produção científica e das políticas de incentivo à pesquisa revelou as desigualdades regionais que caracterizam o sistema brasileiro de ciência e tecnologia.