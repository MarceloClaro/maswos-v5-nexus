# CAPÍTULO 3: METODOLOGIA

## 3.1 Paradigma e Abordagem de Pesquisa

O presente estudo fundamenta-se em uma perspectiva epistemológica que combina elementos do paradigma pós-positivista com abordagens interpretativas. O pós-positivismo reconhece a existência de uma realidade objetiva que pode ser aproximada através de investigação sistemática, mas aceita que todo conhecimento é conjectural e sujeito a revisão (Creswell e Creswell, 2018). Esta perspectiva permite a aplicação de métodos sistemáticos de coleta e análise de dados, típicos das ciências naturais, ao mesmo tempo em que reconhece a importância do contexto e da interpretação na compreensão de fenômenos sociais e tecnológicos.

A abordagem de pesquisa combina elementos quantitativos e qualitativos em um desenho misto. Os componentes quantitativos incluem a análise de indicadores de educação e produção científica, a avaliação de métricas de validação do ecossistema MCP e o mapeamento de infraestrutura digital. Os componentes qualitativos envolvem a interpretação de arquiteturas de sistemas, a análise de políticas públicas e a compreensão de dinâmicas institucionais. Esta combinação permite uma compreensão mais completa do objeto de estudo do que seria possível com qualquer uma das abordagens isoladamente.

A pesquisa adota uma perspectiva crítico-reflexiva que reconhece as relações de poder implicadas na distribuição de tecnologias de IA e seus impactos na educação. As questões de desigualdade regional, acesso a recursos e concentração de capacidades produtivas são tratadas não como variáveis neutras, mas como elementos que refletem e reproduzem estruturas sociais mais amplas. Esta perspectiva orienta a análise das implicações do MCP para a democratização do acesso à educação e à produção científica no Brasil.

## 3.2 Classificação da Pesquisa

Quanto aos objetivos, a pesquisa classifica-se como exploratória e descritiva. A natureza exploratória justifica-se pelo fato de o objeto de estudo (o ecossistema MCP) ser relativamente novo no campo da tecnologia, com menos de dois anos de existência pública. Os estudos exploratórios são apropriados quando o tema é pouco conhecido ou quando se busca identificar fenômenos e relações ainda não estabelecidos na literatura (Gil, 2019). A natureza descritiva manifesta-se no esforço de caracterizar detalhadamente a arquitetura, componentes e mecanismos de validação do ecossistema MCP.

Quanto aos procedimentos técnicos, a pesquisa classifica-se como estudo de caso múltiplo, análise documental e pesquisa bibliográfica. O estudo de caso envolve a investigação aprofundada do ecossistema MCP como um todo, considerando suas implementações específicas e o contexto de aplicação no Brasil. A análise documental refere-se ao exame de documentação técnica, especificações de protocolos e relatórios de implementação. A pesquisa bibliográfica sustenta a revisão de literatura e o enquadramento teórico do estudo.

O horizonte temporal da pesquisa situa-se entre novembro de 2024, data do lançamento público do MCP pela Anthropic, e março de 2026, momento da conclusão da análise. Este período de aproximadamente um ano e meio é suficiente para capturar a fase inicial de adoção do protocolo e as tendências emergentes, mas não permite avaliação de impactos de longo prazo, que ficam como sugestão para trabalhos futuros.

## 3.3 Procedimentos Metodológicos

A metodologia da pesquisa estrutura-se em quatro fases sequenciais, cada uma respondendo a objetivos específicos e utilizando técnicas de coleta e análise adequadas. As fases não são completamente independentes, havendo retroalimentação entre elas à medida que descobertas em uma fase informam investigação em outras.

### 3.3.1 Fase 1: Análise Sistemática da Literatura

A primeira fase consistiu em uma análise sistemática da literatura sobre os temas relacionados ao estudo: Model Context Protocol, arquiteturas de sistemas de IA, impacto de tecnologias de IA na educação e produção científica brasileira. O objetivo desta fase foi estabelecer o referencial teórico e identificar lacunas de conhecimento que a pesquisa poderia contribuir para preencher.

A busca por literatura foi realizada em múltiplas bases de dados, incluindo Web of Science, Scopus, IEEE Xplore, ACM Digital Library, Google Scholar e repositórios de acesso aberto. As strings de busca incluíram combinações de termos como "Model Context Protocol", "MCP", "artificial intelligence education", "AI education Brazil", "science production Brazil", "Northeast Brazil education" e variações. A busca não se limitou a artigos acadêmicos, incluindo também documentação técnica, white papers de empresas, relatórios de organizações internacionais e materiais de organizações governamentais.

Os critérios de inclusão priorizaram publicações a partir de 2023, para capturar a literatura mais recente sobre IA e suas aplicações na educação. Foram incluídas publicações em português, inglês e espanhol, abrangendo as principais literaturas sobre o tema. A triagem resultou em um conjunto de aproximadamente 150 fontes que foram analisadas integralmente, das quais cerca de 65 foram efetivamente utilizadas como referências no texto final.

A análise da literatura envolveu a categorização das fontes em temas (arquitetura de IA, protocolos de comunicação, impacto educacional, políticas de ciência e tecnologia) e a identificação de tendências,consensos e controvérsias. A síntese da literatura seguiu diretrizes de revisão sistemática, mas com a flexibilidade necessária para incorporar fontes de naturezas diversas, incluindo literatura técnica e cinza.

### 3.3.2 Fase 2: Avaliação Técnica da Arquitetura MCP

A segunda fase envolveu a avaliação técnica da arquitetura do ecossistema MCP. O objetivo foi mapear os componentes, camadas e fluxos de processamento do ecossistema, identificar os mecanismos de validação implementados e avaliar as capacidades técnicas em relação aos objetivos de pesquisa.

A avaliação técnica foi realizada através de múltiplas estratégias complementares. Primeiramente, procedeu-se à análise da documentação oficial do MCP, incluindo a especificação do protocolo, guias de implementação e materiais educacionais disponibilizados pelos desenvolvedores. Esta análise permitiu compreender a arquitetura planejada e as capacidades pretendidas do protocolo.

Em segundo lugar, procedeu-se à análise das implementações disponíveis do ecossistema. A pesquisa analisou as implementações do maswos-juridico (37 ferramentas), maswos-mcp (11 ferramentas) e ecosystem-transformer (9 agentes), identificando suas funcionalidades, interconexões e padrões de funcionamento. A análise das ferramentas de auditoria do ecossistema permitiu avaliar os mecanismos de validação implementados.

Em terceiro lugar, foram realizadas consultas aos sistemas de análise de contexto disponíveis, utilizando as ferramentas do ecossistema para realizar consultas específicas sobre indicadores de educação e produção científica. Esta abordagem permitiu coletar dados primários que complementaram a análise documental.

A análise técnica resultou na construção de um modelo conceitual da arquitetura MCP que identifica seis camadas funcionais (Encoder, Collection, Validation, Analysis, Decoder, Control), seus componentes específicos e os fluxos de informação entre eles. Este modeloserve como base para as análises subsequentes sobre potencial e limitações do ecossistema.

### 3.3.3 Fase 3: Mapeamento do Ecossistema Brasileiro

A terceira fase consistiu no mapeamento do ecossistema brasileiro de educação e produção científica em relação às tecnologias de IA. O objetivo foi identificar os dados, sistemas e recursos disponíveis que poderiam ser integrados através do MCP, bem como os atores institucionais relevantes para a implementação do protocolo.

O mapeamento envolveu a identificação de bases de dados governamentais relevantes, incluindo IBGE (Instituto Brasileiro de Geografia e Estatística), INEP (Instituto Nacional de Estudos e Pesquisas Educacionais), DATASUS (Sistema de Informações do SUS), CNPq (Conselho Nacional de Desenvolvimento Científico e Tecnológico) e outros órgãos. Para cada base, identificaram-se os dados disponíveis, os formatos de acesso e as possibilidades de integração via MCP.

A análiseincluiu também a identificação de plataformas educacionais utilizadas no Brasil, incluindo sistemas de aprendizagem virtual (Moodle, Blackboard, Google Classroom), sistemas de gestão acadêmica (Totvs, outras soluções) e repositórios de conteúdo educacional. A avaliação considerou as possibilidades de desenvolvimento de servidores MCP específicos para estas plataformas.

O mapeamento identificou ainda os principais atores institucionais relevantes para a implementação de MCP no contexto educacional brasileiro, incluindo órgãos governamentais (MEC, MCTI), instituições de ensino superior (universidades federais, estaduais, Institutos Federais), centros de pesquisa e organizações da sociedade civil. Esta análise permite compreender o ecossistema de stakeholders que seria involucrado na adoção do MCP.

### 3.3.4 Fase 4: Análise Prospectiva de Impacto Regional

A quarta fase envolveu a análise prospectiva do impacto potencial do MCP em regiões específicas do Brasil, com foco na região Nordeste e no Sertão do Ceará. O objetivo foi avaliar como o ecossistema MCP poderia contribuir para a redução de desigualdades no acesso à educação e à produção científica, considerando as especificidades regionais.

A análise prospectiva combinou a avaliação das capacidades técnicas do MCP (identificadas na Fase 2) com o mapeamento das características regionais (identificadas na Fase 3). Esta combinação permitiu identificar matchings entre as capacidades do protocolo e as necessidades regionais, bem como os desafios de implementação específicos.

A análise considerou especialmente o contexto do Sertão do Ceará, com atenção ao município de Crateús. A região do Sertão cearense apresenta características de infraestrutura limitada, indicadores educacionais abaixo da média nacional e desafios específicos para implementação de tecnologias digitais. A análise prospectiva evaluou como o MCP poderia ser adaptado para atender a essas especificidades.

A análise prospectiva utilizou cenários para explorar diferentes possibilidades de implementação. Os cenários variaram em termos de nível de investimento em infraestrutura, disponibilidade de formação de recursos humanos e estratégia de implementação. Esta abordagem permite identificar condições favoráveis e barreiras para a adoção do MCP em contextos de infraestrutura limitada.

## 3.4 Técnicas de Coleta de Dados

A coleta de dados para a pesquisa envolveu múltiplas técnicas, adequadas aos diferentes tipos de informação necessários para responder às questões de pesquisa.

A pesquisa bibliográfica constituiu a técnica primária de coleta de dados, envolvendo a busca, seleção, análise e síntese de publicações acadêmicas, documentos técnicos e materiais de diferentes naturezas. O processo seguiu protocolos de revisão sistemática adaptados, com critérios de inclusão e exclusão claramente definidos.

A análise documental envolveu o exame de documentos oficiais, incluindo legislação, regulamentos, relatórios de gestão e materiais de organizações governamentais. Especificamente, foram analisados documentos do MEC (Ministério da Educação), MCTI (Ministério da Ciência, Tecnologia e Inovação), IBGE, INEP e outros órgãos relevantes. A análise documental permitiu compreender o contexto institucional e as políticas que impactam a adoção de tecnologias de IA na educação.

A análise técnica envolveu o exame de especificações de protocolos, documentação de software, código fonte disponível publicamente e materiais de fornecedores. Esta técnica foi essencial para compreender a arquitetura técnica do MCP e suas capacidades de integração.

A consulta a bases de dados governamentais foi realizada através das ferramentas de análise disponíveis no ecossistema MCP estudado. foramconsultadas bases como IBGE (dados demográficos, econômicos), DATASUS (dados de saúde), INEP (dados educacionais) para coletar indicadores relevantes para a análise regional.

## 3.5 Técnicas de Análise de Dados

As técnicas de análise de dados foram organizadas em três categorias principais, correspondendo aos diferentes tipos de dados coletados e aos objetivos específicos de cada fase da pesquisa.

A análise de conteúdo foi aplicada aos dados qualitativos, incluindo literatura acadêmica, documentação técnica e materiais institucionais. A análise envolveu a codificação temática dos materiais, identificação de categorias emergentes e construção de sínteses interpretativas. O software de análise qualitativa não foi utilizado, Optando-se por análise manual que permitiu maior controle sobre o processo interpretativo.

A análise estatística descritiva foi aplicada aos dados quantitativos sobre indicadores de educação e produção científica. A análise incluiu cálculo de medidas de tendência central e dispersão, construção de tabelas e gráficos paravisualização de distribuição de indicadores, e comparação de indicadores entre regiões. Os dados foram obtidos principalmente através de consultas às bases de dados governamentais e literatura especializada.

A análise de arquitetura foi aplicada aos dados técnicos sobre o ecossistema MCP. Esta análise envolveu a identificação de componentes, suas inter-relações e fluxos de processamento. O resultado foi um modelo conceitual que representa a estrutura e funcionamento do ecossistema. A análise de arquitetura foi suportada pela experiência prática com as ferramentas disponíveis no ecossistema.

A integração dos resultados das diferentes análises foi realizada através de síntese interpretativa, que buscou articular os achados das diferentes fases em uma narrativa coerente que responde às questões de pesquisa. A triangulação de fontes e métodos foi utilizada para validar os resultados, verificando se diferentes abordagens convergiam para conclusões similares.

## 3.6 Validação e Confiabilidade

A validade e confiabilidade da pesquisa foram asseguradas através de múltiplas estratégias ao longo de todo o processo investigativo.

A triangulação de fontes envolveu a consulta a múltiplas fontes de informação para os mesmos tópicos de investigação. Por exemplo, informações sobre a arquitetura do MCP foram obtidas tanto da documentação oficial quanto da análise de implementações reais, permitindo verificar a consistência das informações. Informações sobre indicadores educacionais foram obtidas de múltiplas fontes governamentais, permitindovalidação cruzada dos dados.

A validação através de especialistas foi realizada através da apresentação dos resultados preliminares a pesquisadores da área de educação e tecnologia, solicitando feedback sobre a adequação das interpretações. Este processo permitiu identificar pontos cegos e fortalecer as análises.

A transparência metodológica foi assegurada através da documentação detalhada de todos os procedimentos de coleta e análise de dados. Os critérios de seleção de fontes, os procedimentos de análise e as decisões interpretativas foram explicitamente documentados, permitindo avaliação crítica por leitores.

As limitações da pesquisa foram explicitamente reconhecidas e registradas. A principal limitação refere-se à impossibilidade de realizar verificação empírica das capacidades do MCP em contextos educacionais brasileiros específicos, dado o estágio inicial de adoção do protocolo. As análises são, portanto, baseadas em avaliação técnica e prospectiva, não em estudos de implementação real. Esta limitação é inerente ao estudo de tecnologias emergentes e indica uma direção para trabalhos futuros.

## 3.7 Delimitação do Estudo

A delimitação do estudo define o escopo da pesquisa em termos de conteúdo, espaço e tempo.

Em termos de conteúdo, a pesquisa focus exclusivamente no Model Context Protocol, não abordando outros protocolos de comunicação para sistemas de IA como o Agent2Agent (A2A) desenvolvido pelo Google. O foco também não inclui aspectos de hardware, infraestrutura computacional ou modelos de linguagem específicos, concentrando-se na camada de integração e interoperabilidade que o MCP proporciona.

Em termos espaciais, o estudo delimita-se ao Brasil, com atenção especial à região Nordeste e ao Sertão do Ceará. O foco regional justifica-se pelas desigualdades que caracterizam o sistema educacional e de pesquisa brasileiro, e pela oportunidade de investigar como o MCP poderia contribuir para mitigá-las. O município de Crateús é mencionado como exemplo de contexto de implementação, mas a análise não se limita a este município específico.

Em termos temporais, a pesquisa foca no período de desenvolvimento inicial do MCP, desde seu lançamento em novembro de 2024 até março de 2026. Este horizonte permite capturar a fase de emergência e adoção inicial do protocolo, mas não permite avaliação de impactos de longo prazo. Estudos longitudinais seriam necessários para avaliar a evolução do ecossistema e seus impactos efetivos ao longo do tempo.

A pesquisa não aborda diretamente a implementação técnica de servidores MCP específicos para o contexto brasileiro, limitando-se à análise prospectiva de oportunidades e desafios. A implementação efetiva ficacomo sugestão para trabalhos futuros que podem ser desenvolvidos com base nos achados desta pesquisa.

## Síntese do Capítulo

Este capítulo apresentou a metodologia que orientou a condução da pesquisa. A combinação de paradigmas pós-positivistas com perspectivas crítico-reflexivas permitiu uma abordagem que valoriza tanto a precisão técnica quanto a consciência das dimensões sociais e políticas do objeto de estudo.

A classificação da pesquisa como exploratória, descritiva, com utilização de múltiplos procedimentos técnicos, adequa-se à natureza do objeto de estudo, uma tecnologia emergente que requer mapeamento e compreensão inicial antes de investigação mais aprofundada.

As quatro fases metodológicas - análise sistemática da literatura, avaliação técnica da arquitetura MCP, mapeamento do ecossistema brasileiro e análise prospectiva de impacto regional - foram detalhadas em termos de objetivos, procedimentos, técnicas de coleta e análise. A sequenciação das fases permite uma progressão lógica do conhecimento geral (literatura) para o conhecimento específico (arquitetura técnica) e suas aplicações contextuais (ecossistema brasileiro, impacto regional).

As técnicas de coleta e análise de dados foram explicitadas, demonstrando a diversidade de abordagens necessárias para investigar um objeto de estudo complexo que envolve dimensões técnicas, institucionais e sociais. As estratégias de validação e confiabilidade foram apresentadas, reconhecendo tanto as possibilidades quanto as limitações inerentes à pesquisa.

As delimitações do estudo estabeleceram o escopo da investigação, explicitando o que foi incluído e o que ficou de fora. Estas delimitações são fundamentais para que leitores possam avaliar a aplicabilidade dos resultados e identificar possíveis extensões da pesquisa.

O próximo capítulo apresenta os resultados da aplicação desta metodologia, organizando as descobertas em seções que abordam a análise do ecossistema MCP global, a avaliação da arquitetura, os mecanismos de validação, as limitações identificadas e a análise do impacto potencial no contexto brasileiro e regional.