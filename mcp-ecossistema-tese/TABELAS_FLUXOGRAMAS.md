# TABELAS E FLUXOGRAMAS PARA A TESE

## Sumário Visual

1. [Tabelas](#tabelas)
2. [Fluxogramas](#fluxogramas)
3. [Diagramas Cirúrgicos](#diagramas-cirúrgicos)
4. [Elementos Autoexplicativos](#elementos-autoexplicativos)

---

# TABELAS

## Tabela 1: Estrutura do Ecossistema MCP

| Camada | Componente | Função | Tecnologias |
|--------|-----------|--------|--------------|
| **Encoder** | Intent Parser | Processamento de linguagem natural | NLP, Transformers |
| | Tier Router | Roteamento por complexidade | Classification |
| | RAG Builder | Enriquecimento contextual | Vector DB, Embeddings |
| | Domain Analyzer | Identificação de domínio | Ontology matching |
| | Scope Mapper | Mapeamento de escopo | Graph algorithms |
| **Collection** | LexML Scraper | Legislação brasileira | Web scraping |
| | STF Scraper | Jurisprudência STF | API integration |
| | STJ Scraper | Jurisprudência STJ | API integration |
| | IBGE Scraper | Dados demográficos | Official APIs |
| | INEP Scraper | Dados educacionais | Official APIs |
| | DATASUS Scraper | Dados de saúde | Official APIs |
| **Validation** | Cross Validator | Validação cruzada | Multi-source check |
| | Citation Validator | Verificação de citações | Regex, DOI lookup |
| | Source Authenticator | Autenticação de fontes | OAuth, API keys |
| **Analysis** | Precedent Analyzer | Análise de precedentes | NLP, Jurisprudence |
| | Legislation Checker | Verificação legislativa | LexML integration |
| | Specialists (37) | Análise por área | Domain expertise |
| **Decoder** | Agent Factory | Geração de agentes | Code generation |
| | Skill Assembler | Compilação de habilidades | Composition |
| | Output Formatters | Formatação de saída | Multiple formats |
| **Control** | Critic-Router | Controle de qualidade | Quality assessment |

---

## Tabela 2: Métricas de Adoção do MCP (2024-2026)

| Métrica | Valor | Fonte |
|---------|-------|-------|
| Data de lançamento | 25/11/2024 | Anthropic |
| Downloads mensais do SDK | 97+ milhões | Conversion (2026) |
| Servidores MCP ativos | 10.000+ | Conversion (2026) |
| Empresas adotantes | OpenAI, Google, Microsoft, Amazon, 500+ Fortune 500 | Thoughtworks (2025) |
| Transferência de governança | Dez/2025 → Linux Foundation | Anthropic (2025) |

---

## Tabela 3: Indicadores Educacionais - Região Nordeste vs. Brasil

| Indicador | Nordeste | Brasil | Fonte |
|-----------|----------|--------|-------|
| Taxa de analfabetismo (15+ anos) | 12,7% | 7,0% | IBGE (2022) |
| Anos de escolaridade médio | 9,2 | 10,5 | PNAD (2022) |
| % com ensino superior | 8,3% | 12,7% | PNAD (2022) |
| Escolas com internet | 67% | 84% | INEP (2023) |
| DOCs por 100.000 hab. | 12,5 | 18,3 | CNJ (2023) |

---

## Tabela 4: Comparação de Arquiteturas de Integração de IA

| Característica | MCP | Plugins Tradicionais | APIs REST |
|----------------|-----|---------------------|-----------|
| Padronização | Alta | Baixa | Média |
| Interoperabilidade | Universal | Limitada | Específica |
| Segurança | Em evolução | Variável | Alta |
| Complexidade | Média-Alta | Baixa | Média |
| Escalabilidade | Alta | Baixa | Alta |
| Comunidade | Crescente | Estagnada | Grande |

---

## Tabela 5: Requisitos de Implementação MCP no Sertão do Ceará

| Requisito | Disponibilidade | Gap |
|-----------|-----------------|-----|
| Conectividade internet | Parcial (74%) | 26% |
| Servidores para hospedagem | Limitada | Alto |
| Profissionais qualificados | Escassos | Crítico |
| Energia elétrica estável | 89% | 11% |
| Dispositivos móveis | Alta penetração | Baixo |

---

## Tabela 6: Servidores MCP Educacionais Identificados

| Categoria | Exemplos | Funcionalidades |
|-----------|----------|----------------|
| LMS Integration | Moodle, Blackboard, Canvas | Sync, analytics |
| Data Educational | INEP, ENEM, PROVA BRASIL | Indicators, results |
| Research | Semantic Scholar, arXiv | Literature review |
| Administrative | SIA, SIM, RAIS | Institutional data |

---

## Tabela 7: Hipóteses e Resultados

| Hipótese | Descrição | Resultado |
|---------|-----------|-----------|
| H1 | Arquitetura Transformer de 6 camadas | Confirmada |
| H2 | Mecanismos de validação robustos | Confirmada c/ ressalvas |
| H3 | Limitações de segurança, interoperabilidade e implementação | Confirmada |
| H4 | Potencial para democratização do acesso | Confirmada |
| H5 | Desafios específicos para Sertão do Ceará | Confirmada |

---

# FLUXOGRAMAS

## Fluxograma 1: Arquitetura Geral do Ecossistema MCP

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                              FLUXO DE PROCESSAMENTO                          │
└─────────────────────────────────────────────────────────────────────────────┘

     ┌──────────┐
     │ USUÁRIO  │
     │(Pergunta)│
     └────┬─────┘
          │
          ▼
┌─────────────────────────────┐
│      CAMADA ENCODER          │
│  ┌────────────────────────┐ │
│  │  • Intent Parser       │ │
│  │  • Tier Router         │ │
│  │  • RAG Builder         │ │
│  │  • Domain Analyzer    │ │
│  │  • Scope Mapper        │ │
│  └────────────────────────┘ │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│      CAMADA COLLECTION       │
│  ┌────────────────────────┐ │
│  │  • LexML (Legislação) │ │
│  │  • STF/STJ (Jurisp.)  │ │
│  │  • IBGE (Demográfico) │ │
│  │  • INEP (Educacional) │ │
│  │  • DATASUS (Saúde)     │ │
│  └────────────────────────┘ │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│      CAMADA VALIDATION        │
│  ┌────────────────────────┐ │
│  │  • Cross Validator     │ │
│  │  • Citation Validator  │ │
│  │  • Source Authenticator │ │
│  └────────────────────────┘ │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│      CAMADA ANALYSIS        │
│  ┌────────────────────────┐ │
│  │  • Precedent Analyzer  │ │
│  │  • Legislation Checker │ │
│  │  • 37 Specialists      │ │
│  └────────────────────────┘ │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│      CAMADA DECODER          │
│  ┌────────────────────────┐ │
│  │  • Agent Factory       │ │
│  │  • Skill Assembler     │ │
│  │  • Output Formatters   │ │
│  └────────────────────────┘ │
└────────────┬────────────────┘
             │
             ▼
┌─────────────────────────────┐
│      CAMADA CONTROL          │
│  ┌────────────────────────┐ │
│  │  • Critic-Router       │ │
│  │  • Quality Check       │ │
│  └────────────────────────┘ │
└────────────┬────────────────┘
             │
             ▼
     ┌──────────┐
     │ RESPOSTA │
     │ FINAL    │
     └──────────┘
```

---

## Fluxograma 2: Processo de Validação de Citações

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    PROCESSO DE VALIDAÇÃO DE CITAÇÕES                         │
└─────────────────────────────────────────────────────────────────────────────┘

     ┌──────────────┐
     │   CITAÇÃO    │
     │   DETECTADA  │
     └──────┬───────┘
            │
            ▼
┌───────────────────────┐
│  1. VALIDAÇÃO SINTÁTICA│
│  ┌─────────────────┐  │
│  │ Formato correto? │  │
│  └────────┬────────┘  │
│      SIM ╱│╲ NÃO      │
│        ╱ │ ╲          │
│       ▼  │  ▼         │
│  CONTINUA│ ERRO       │
│         │ REGISTRA   │
└─────────┼────────────┘
          │
          ▼
┌───────────────────────┐
│ 2. VALIDAÇÃO SEMÂNTICA │
│ ┌──────────────────┐  │
│ │ Publicação existe?│  │
│ └────────┬─────────┘  │
│    SIM ╱│╲ NÃO        │
│      ╱  │  ╲          │
│     ▼   │   ▼         │
│ CONTINUA│ ERRO         │
│        │ REGISTRA     │
└────────┼──────────────┘
         │
         ▼
┌───────────────────────┐
│ 3. VALIDAÇÃO CONTEXTUAL│
│ ┌──────────────────┐  │
│ │ Citação relevante│  │
│ │ ao argumento?   │  │
│ └────────┬─────────┘  │
│    SIM ╱│╲ NÃO        │
│      ╱  │  ╲          │
│     ▼   │   ▼         │
│ APROVADO│ REVISÃO     │
│         │ NECESSÁRIA  │
└────────┼──────────────┘
         │
         ▼
┌───────────────────────┐
│    CITAÇÃO VÁLIDA     │
│    REGISTRADA         │
└───────────────────────┘
```

---

## Fluxograma 3: Decisão de Implementação MCP

```
┌─────────────────────────────────────────────────────────────────────────────┐
│           FLUXO DE DECISÃO PARA IMPLEMENTAÇÃO NO SERTÃO                    │
└─────────────────────────────────────────────────────────────────────────────┘

         ┌───────────────────┐
         │ AVALIAR CONTEXTO  │
         └────────┬──────────┘
                  │
                  ▼
    ┌─────────────────────────┐
    │ TEM CONECTIVIDADE?       │
    └───────────┬─────────────┘
         SIM ╱ │ ╲ NÃO
           ╱  │  ╲
          ▼   │   ▼
    ┌─────────┐│┌──────────────┐
    │ Online  │ ││ Offline-first│
    │ MCP     │ ││ Solution     │
    └────┬────┘ │└──────┬───────┘
         │            │
         ▼            ▼
┌───────────────┐ ┌────────────────┐
│ TEM SERVIDOR?│ │ REQUISITOS     │
└──────┬───────┘ │    MINIMOS     │
   SIM╱│╲NÃO    │ └───────┬────────┘
     ╱ │ ╲      │         │
    ▼  │  ▼     │         ▼
┌─────┐│┌──────┐│  ┌──────────────┐
│Cloud│ ││Local ││  │ PWA/Mobile   │
│Deploy│ ││Deploy│  │ Approach     │
└──┬──┘ │└──┬───┘  └───────┬────────┘
   │     │   │              │
   ▼     ▼   ▼              ▼
┌─────────────────┐  ┌─────────────────────┐
│ IMPLEMENTAÇÃO   │  │ TREINAMENTO LOCAL   │
│ TRADICIONAL     │  │ + DOCUMENTAÇÃO      │
└────────┬────────┘  └──────────┬──────────┘
         │                      │
         ▼                      ▼
┌─────────────────────────────────┐
│      PILOTO + MONITORAMENTO     │
│      CONTÍNUO                  │
└─────────────────────────────────┘
```

---

# DIAGRAMAS CIRÚRGICOS

## Diagrama Cirúrgico 1: Arquitetura Transformer Aplicada ao MCP

```
┌─────────────────────────────────────────────────────────────────────────────┐
│              ARQUITECTURA TRANSFORMER → MCP (CIRCULAR)                     │
└─────────────────────────────────────────────────────────────────────────────┘

                    ┌──────────────────────────────────────┐
                    │      ENCODER (Input)                 │
                    │  ┌────────────────────────────────┐   │
                    │  │  Embedding + Positional       │   │
                    │  │  Encoding (Intents)           │   │
                    │  └───────────────────────────────┘   │
                    │              │                        │
                    └──────────────┼────────────────────────┘
                                   ▼ Self-Attention
                    ┌──────────────┬────────────────────────┐
                    │              │                        │
                    │    ┌─────────┴─────────┐              │
                    │    │  Multi-Head       │              │
                    │    │  Attention        │              │
                    │    │  (Domain Select)  │              │
                    │    └─────────┬─────────┘              │
                    │              │                        │
                    │              ▼ Feed-Forward           │
                    │    ┌─────────┴─────────┐              │
                    │    │  Feed Forward     │              │
                    │    │  Networks         │              │
                    │    └─────────┬─────────┘              │
                    │              │                        │
                    └──────────────┼────────────────────────┘
                                   ▼ Self-Attention (Output)
                    ┌──────────────┬────────────────────────┐
                    │              │                        │
                    │    ┌─────────┴─────────┐              │
                    │    │  Cross-Validation  │              │
                    │    │  Layer            │              │
                    │    └─────────┬─────────┘              │
                    │              │                        │
                    └──────────────┼────────────────────────┘
                                   ▼
                    ┌──────────────────────────────────────┐
                    │      DECODER (Output)                │
                    │  ┌────────────────────────────────┐   │
                    │  │  Linear + Softmax              │   │
                    │  │  (Response Generation)        │   │
                    │  └───────────────────────────────┘   │
                    └──────────────────────────────────────┘
```

---

## Diagrama Cirúrgico 2: Validação Cruzada de Dados (Surgical View)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                    VALIDAÇÃO CRUZADA CIRÚRGICA                              │
│                         (Multi-Source Verification)                         │
└─────────────────────────────────────────────────────────────────────────────┘

     ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
     │   IBGE     │      │   INEP     │      │  DATASUS   │
     │  (Dados   │      │  (Dados   │      │  (Dados   │
     │ Demográf.)│      │ Educac.)   │      │  Saúde)    │
     └─────┬───────┘      └─────┬───────┘      └─────┬───────┘
           │                    │                    │
           ▼                    ▼                    ▼
     ┌─────────────┐      ┌─────────────┐      ┌─────────────┐
     │  Parser    │      │  Parser    │      │  Parser    │
     │  Standard  │      │  Standard  │      │  Standard  │
     └─────┬───────┘      └─────┬───────┘      └─────┬───────┘
           │                    │                    │
           └────────────────────┼────────────────────┘
                                │
                    ┌───────────┴───────────┐
                    │   CROSS VALIDATOR    │
                    │  ┌─────────────────┐  │
                    │  │  Comparação    │  │
                    │  │  de Dados      │  │
                    │  │  (Surgical)    │  │
                    │  └─────────────────┘  │
                    └───────────┬───────────┘
                                │
              ┌────────────────┼────────────────┐
              │                │                │
              ▼                ▼                ▼
     ┌────────────┐    ┌────────────┐    ┌────────────┐
     │  CONFLITO  │    │ CONSISTENTE│    │  ALERTA   │
     │ DETECTADO  │    │            │    │  MANUAL   │
     └─────┬──────┘    └─────┬──────┘    └─────┬──────┘
           │                 │                 │
           ▼                 └────────┬────────┘
     ┌─────────────┐                  │
     │  RESOLUÇÃO   │                  ▼
     │  HUMANA      │          ┌─────────────┐
     │  REQUERIDA   │          │  REGISTRO   │
     └─────────────┘          │  DE LOG     │
                              └─────────────┘
```

---

## Diagrama Cirúrgico 3: Camadas de Integração MCP (Surgical Architecture)

```
┌─────────────────────────────────────────────────────────────────────────────┐
│               ARQUITECTURA CIRÚRGICA DO MCP - VISÃO TOP-DOWN                │
└─────────────────────────────────────────────────────────────────────────────┘

┌──────────────────────────────────────────────────────────────────────────┐
│  CAMADA 6: INTERFACE DO USUÁRIO                                          │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │ Chat • Web Interface • API • Mobile App • Voice                     │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────────────────────┤
│  CAMADA 5: ORQUESTRAÇÃO (Control)                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                    Critic-Router                                    │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │  │
│  │  │ Quality  │  │  Retry   │  │  Cache   │  │  Rate    │          │  │
│  │  │ Check    │  │ Logic    │  │ Manager  │  │ Limit    │          │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────────────────────┤
│  CAMADA 4: ANÁLISE (Analysis)                                            │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │                                                                      │  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │  │
│  │  │ Precedent│  │Legislat. │  │ Specialist│ │ Content │          │  │
│  │  │ Analyzer │  │ Checker  │  │   (37)   │  │  Gen.   │          │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │  │
│  │                                                                      │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────────────────────┤
│  CAMADA 3: VALIDAÇÃO (Validation)                                        │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐                          │  │
│  │  │  Cross   │  │ Citation │  │  Source  │                          │  │
│  │  │ Validator│  │ Validator│  │Authentic.│                          │  │
│  │  └──────────┘  └──────────┘  └──────────┘                          │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────────────────────┤
│  CAMADA 2: COLETA (Collection)                                           │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  ┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐┌────────┐       │  │
│  │  │ LexML  ││  STF   ││  STJ   ││  IBGE  ││  INEP  ││DATASUS │       │  │
│  │  │(Lei)   ││(Jurisp)││(Jurisp)││(Demo)  ││(Edu)   ││(Saúde) │       │  │
│  │  └────────┘└────────┘└────────┘└────────┘└────────┘└────────┘       │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
├──────────────────────────────────────────────────────────────────────────┤
│  CAMADA 1: ENCODER (Input)                                               │
│  ┌──────────────────────────────────────────────────────────────────────┐  │
│  │  ┌──────────┐  ┌──────────┐  ┌──────────┐  ┌──────────┐          │  │
│  │  │  Intent  │  │   Tier   │  │   RAG    │  │  Domain  │          │  │
│  │  │  Parser  │  │  Router  │  │ Builder  │  │ Analyzer │          │  │
│  │  └──────────┘  └──────────┘  └──────────┘  └──────────┘          │  │
│  └──────────────────────────────────────────────────────────────────────┘  │
└──────────────────────────────────────────────────────────────────────────┘
```

---

# ELEMENTOS AUTOEXPLICATIVOS

## Diagrama Autoexplicativo 1: O que é o MCP?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│   ┌───────────────────────────────────────────────────────────────────┐   │
│   │                                                                   │   │
│   │                     O QUE É O MCP?                               │   │
│   │                                                                   │   │
│   │   ┌───────────────┐                                               │   │
│   │   │               │                                               │   │
│   │   │  MODEL        │  ──►  (O que a IA "lê" e "pensa")           │   │
│   │   │  CONTEXT      │                                               │   │
│   │   │  PROTOCOL     │  ──►  (Como sistemas conversam entre si)   │   │
│   │   │               │                                               │   │
│   │   └───────────────┘                                               │   │
│   │                                                                   │   │
│   │   RESUMINDO EM 3 PALAVRAS:                                        │   │
│   │                                                                   │   │
│   │        ┌─────────┐  ┌─────────┐  ┌─────────┐                    │   │
│   │        │PADRÃO   │  │INTERFACE│  │PONTE    │                    │   │
│   │        │UNIVERSAL│  │ABERTA   │  │INTELIGENTE                  │   │
│   │        └─────────┘  └─────────┘  └─────────┘                    │   │
│   │                                                                   │   │
│   └───────────────────────────────────────────────────────────────────┘   │
│                                                                             │
│   ANTES:  IA ←──✕──→ Sistema A                                          │
│           IA ←──✕──→ Sistema B                                          │
│           IA ←──✕──→ Sistema C                                          │
│                                                                             │
│   DEPOIS: IA ←─────────── MCP ───────────→ Sistema A                    │
│                    │                      → Sistema B                    │
│                    │                      → Sistema C                   │
│                    └──────────────────────→ [Todos os sistemas]        │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Diagrama Autoexplicativo 2: Por que o MCP importa para a Educação?

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│    ┌─────────────────────────────────────────────────────────────────┐    │
│    │                                                                 │    │
│    │            MCP × EDUCAÇÃO: POR QUE IMPORTA?                    │    │
│    │                                                                 │    │
│    └─────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│    ┌──────────────────┐    ┌──────────────────┐    ┌──────────────────┐│
│    │ ANTES            │    │ COM MCP          │    │ BENEFÍCIOS       ││
│    │                  │    │                  │    │                  ││
│    │ Professor busca │    │ Sistema integra  │    │ ✓ Democratiza    ││
│    │ manualmente em  │    │ dados de:       │    │   acesso         ││
│    │ 5+ sistemas      │    │ - INEP           │    │ ✓ Personaliza    ││
│    │ diferentes       │    │ - IBGE           │    │   aprendizagem   ││
│    │                  │    │ - DATASUS         │    │ ✓ Automatiza     ││
│    │                  │    │ - Moodle          │    │   tarefas        ││
│    │                  │    │ - Blackboard      │    │ ✓ Audita         ││
│    │                  │    │ em UM só lugar    │    │   qualidade      ││
│    └──────────────────┘    └──────────────────┘    └──────────────────┘│
│                                                                             │
│    EXEMPLO PRÁTICO:                                                        │
│                                                                             │
│    Pergunta: "Quais escolas do Sertão do Ceará têm a maior taxa          │
│               de evasão e quais os principais motivos?"                  │
│                                                                             │
│    SEM MCP: Professor precisa consultar INEP, IBGE, SIM, e               │
│             pesquisar manualmente em múltiplas bases...                  │
│                                                                             │
│    COM MCP: O sistema integra todas as fontes automaticamente             │
│             e responde em linguagem natural com dados fundamentados.     │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Diagrama Autoexplicativo 3: Desafios para o Sertão do Ceará

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│    ┌─────────────────────────────────────────────────────────────────┐    │
│    │                                                                 │    │
│    │           DESAFIOS PARA IMPLEMENTAÇÃO NO SERTÃO                │    │
│    │                                                                 │    │
│    └─────────────────────────────────────────────────────────────────┘    │
│                                                                             │
│    ┌─────────────────────────────┐   ┌─────────────────────────────┐    │
│    │ 1. CONECTIVIDADE           │   │ 2. INFRAESTRUTURA            │    │
│    │                            │   │                             │    │
│    │  ┌─────────────────────┐   │   │  ┌─────────────────────┐   │    │
│    │  │ 74% de cobertura   │   │   │  │ Servidores escassos │   │    │
│    │  │ Internet no campo  │   │   │  │ em áreas remotas    │   │    │
│    │  │                     │   │   │  │                     │   │    │
│    │  │ ████████░░ 74%     │   │   │  │ ████░░░░░░ 30%      │   │    │
│    │  └─────────────────────┘   │   │  └─────────────────────┘   │    │
│    └─────────────────────────────┘   └─────────────────────────────┘    │
│                                                                             │
│    ┌─────────────────────────────┐   ┌─────────────────────────────┐    │
│    │ 3. PROFISSIONAIS           │   │ 4. CONTEÚDOS                │    │
│    │                            │   │                             │    │
│    │  ┌─────────────────────┐   │   │  ┌─────────────────────┐   │    │
│    │  │ Poucos técnicos    │   │   │  │ Conteúdos pouco     │   │    │
│    │  │ qualificados       │   │   │  │ relevantes para     │   │    │
│    │  │ na região          │   │   │  │ realidade local      │   │    │
│    │  │                     │   │   │  │                     │   │    │
│    │  │ ██████░░░░ 45%     │   │   │  │ ██████░░░░░ 40%     │   │    │
│    │  └─────────────────────┘   │   │  └─────────────────────┘   │    │
│    └─────────────────────────────┘   └─────────────────────────────┘    │
│                                                                             │
│    ═══════════════════════════════════════════════════════════════════     │
│                              OPORTUNIDADES                                  │
│    ═══════════════════════════════════════════════════════════════════     │
│                                                                             │
│    ✓ Penetração mobile alta (smartphones como bridge)                    │
│    ✓ IFCE Campus Crateús como polo de inovação                          │
│    ✓ Comunidades menores = maior agilidade para testar                   │
│    ✓ Crescente interesse em formação técnica                             │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

## Diagrama Autoexplicativo 4: Fluxo Completo do Usuário ao Resultado

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                                                                             │
│    ┌─────────────────────────────────────────────────────────────────────┐ │
│    │                    JORNADA DO USUÁRIO                               │ │
│    │              (Do سؤال à resposta fundamentada)                     │ │
│    └─────────────────────────────────────────────────────────────────────┘ │
│                                                                             │
│    ┌──────────┐     ┌──────────┐     ┌──────────┐     ┌──────────┐       │
│    │  PASSO 1 │────►│  PASSO 2 │────►│  PASSO 3 │────►│  PASSO 4 │       │
│    │          │     │          │     │          │     │          │       │
│    │  USUÁRIO │     │ ENCODER  │     │ COLETA   │     │VALIDAÇÃO │       │
│    │  FAZ    │     │ PROCESSA │     │ DADOS    │     │ CRUZADA  │       │
│    │ PERGUNTA │     │          │     │          │     │          │       │
│    └──────────┘     └──────────┘     └──────────┘     └────┬─────┘       │
│         │                                                  │              │
│         │                                                  ▼              │
│         │                                           ┌──────────┐          │
│         │                                           │  PASSO 5 │          │
│         │                                           │          │          │
│         │                                           │ ANÁLISE │          │
│         │                                           │ESPECIALIZADA         │
│         │                                           └────┬─────┘          │
│         │                                                │                │
│         │                                                ▼                │
│         │                                         ┌──────────┐          │
│         │                                         │  PASSO 6 │          │
│         │                                         │          │          │
│         │                                         │ CRÍTICA  │          │
│         │                                         │ (Qualid.)│          │
│         │                                         └────┬─────┘          │
│         │                                              │                │
│         │                                              ▼                │
│    ┌────┴────┐                                   ┌──────────┐          │
│    │ APROVADO│◄──────────────────────────────────│  PASSO 7 │          │
│    │         │                                   │          │          │
│    │ RETORNA │                                   │ GERAR   │          │
│    │RESPOSTA │                                   │RESPOSTA │          │
│    └─────────┘                                   └──────────┘          │
│                                                                             │
│    ══════════════════════════════════════════════════════════════════════   │
│                            AUTOEXPLICAÇÃO                                    │
│    ══════════════════════════════════════════════════════════════════════   │
│                                                                             │
│    Este diagrama mostra como uma pergunta do usuário passa por            │
│    todas as camadas do MCP até gerar uma resposta fundamentada.           │
│                                                                             │
│    A etapa de "Crítica" (PASSO 6) é fundamental: ela verifica            │
│    se a qualidade da resposta atende aos padrões esperados antes          │
│    de entregar ao usuário. Se não atende, o processo retorna             │
│    para refinamento.                                                       │
│                                                                             │
└─────────────────────────────────────────────────────────────────────────────┘
```

---

# LEGENDAS DAS FIGURAS

| Figura | Título | Local no Texto |
|--------|--------|----------------|
| Figura 1 | Mapa do Brasil com destaque para Nordeste | Capítulo 1 |
| Figura 2 | Mapa da região Nordeste | Capítulo 1 |
| Figura 3 | Mapa do Ceará com destaque para Crateús | Capítulo 1 |
| Figura 4 | Mapa interativo de Crateús | Capítulo 1 |
| Figura 5 | Arquitetura em camadas do MCP | Capítulo 2 |
| Figura 6 | Fluxo de processamento | Capítulo 2 |
| Figura 7 | Processo de validação de citações | Capítulo 3 |
| Figura 8 | Fluxo de decisão para implementação | Capítulo 4 |
| Figura 9 | Validação cruzada cirúrgica | Capítulo 4 |
| Figura 10 | Jornada do usuário ao resultado | Conclusão |

---

*Elaborado para a Tese de Doutorado de Marcelo Claro Laranjeira*
*Programa de Pós-Graduação em Ciência da Computação - UFC Campus Crateús*
*Março de 2026*
