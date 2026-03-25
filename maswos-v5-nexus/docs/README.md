# MASWOS V5 NEXUS - Documentação Técnica do Ecossistema

## Visão Geral

MASWOS (Multi-Agent Scientific Writing Operating System) é um ecossistema completo de produção acadêmica e jurídica, desenvolvido com arquitetura Transformer para orchestrar múltiplos Model Context Protocol (MCP).

### Versão
- **V5 NEXUS** - 5.0.0-NEXUS

### Arquitetura Principal
- Cross-MCP Orchestration
- Transformer-based routing
- Multi-domain support (academic, legal, RAG)

---

## Estrutura do Ecossistema

```
maswos-v5-nexus-dist/
├── docs/                          # Documentação
├── rag/                           # Módulo RAG (9 estratégias)
│   ├── base/                      # Componentes base
│   ├── classic/                   # Vanilla RAG
│   ├── memory/                    # Memory RAG
│   ├── agentic/                   # Agentic RAG
│   ├── graph/                     # Graph RAG
│   ├── hybrid/                    # Hybrid RAG
│   ├── corrective/                # CRAG
│   ├── adaptive/                  # Adaptive RAG
│   ├── fusion/                    # RAG-Fusion
│   ├── hyde/                      # HyDE
│   └── orchestrator/              # RAG Orchestrator
├── PageIndex/                     # Integração PageIndex
├── mcp-ecossistema-tese/         # Scripts de geração
├── criador-de-artigo-v2/         # Agentes de artigo
├── .agent/skills/                # Skills do sistema
├── *.json                        # Configurações
└── *.py                          # Módulos Python
```

---

## MCPs Integrados

### 1. maswos-juridico
- **Agentes**: 60+
- **Domínios**: legal
- **Camadas**: Encoder, Collection, Validation, Analysis, Synthesis, Output

### 2. maswos-mcp
- **Agentes**: 15
- **Domínios**: skill-generation
- **Camadas**: Encoder, Validation, AgentFactory, Decoder, Control

### 3. academic
- **Agentes**: 55+
- **Domínios**: academic, research, data_collection, document_rag
- **Scrapers**: 11 (arXiv, PubMed, Semantic Scholar, CAPES, etc.)
- **APIs Governamentais**: 7 (IBGE, DATASUS, IPEA, etc.)

### 4. pageindex-mcp
- **Agentes**: 10
- **Domínios**: document_rag, reasoning_search, tree_indexing
- **Features**: vectorless_rag, tree_indexing, no_chunking

### 5. maswos-rag
- **Agentes**: 21
- **Estratégias**: 9 (Vanilla, Memory, Agentic, Graph, Hybrid, CRAG, Adaptive, Fusion, HyDE)

---

## Estratégias RAG

### Vanilla RAG
Fluxo básico: Retriever → Augmentation → Generation

### Memory RAG
Utiliza Redis para sessões longas e histórico de conversa

### Agentic RAG
Agentes dinâmicos que roteiam entre múltiplas fontes de dados

### Graph RAG
Utiliza Neo4j para grafos de conhecimento (entidades e relações)

### Hybrid RAG
Combina busca vetorial com busca em grafos

### CRAG (Corrective RAG)
Valida qualidade das fontes antes de enviar ao LLM

### Adaptive RAG
Adapta estratégia automaticamente conforme complexidade da query

### RAG-Fusion (RRF)
Combina múltiplas fontes usando Reciprocal Rank Fusion

### HyDE
Gera documentos hipotéticos para melhorar precisão da busca

---

## Pipelines de Pesquisa

| Pipeline | Tipo RAG | Agentes | Quality Gate |
|----------|----------|---------|--------------|
| basic_research | vanilla | R01,R02,R03 | GR0 |
| validated_research | crag | R13,R14,R15,R02,R03 | GR2 |
| comprehensive_research | hybrid | R09,R10,R11,R12,R02,R03 | GR4 |
| adaptive_research | adaptive | R16,R17,R01,R02,R03 | GR3 |
| multi_source_research | fusion | R18,R19,R20,R02,R03 | GR4 |

---

## Scrapers Acadêmicos

| ID | Nome | Tipo | Volume |
|----|------|------|--------|
| A04 | arXiv | academic | 2M+ |
| A05 | PubMed/NCBI | biomedical | 35M+ |
| A06 | Semantic Scholar | academic | 200M+ |
| A07 | DOAJ | journals | 21K+ |
| A08 | CORE | academic | 300M+ |
| A09 | OpenAlex | academic | 250M+ |
| A10 | Europe PMC | biomedical | 37M+ |
| A11 | AMiner | academic_china | 300M+ |
| A12 | OpenReview | ai_conferences | 50+ |
| A13 | CAPES | brazilian_academic | 460M+ |
| A14 | Internet Archive | historical | 40M+ |

---

## APIs Governamentais

| ID | Nome | Tipo | Recursos |
|----|------|------|----------|
| N09 | IBGE | demographic | 25+ APIs |
| N10 | INEP | education | - |
| N11 | CNJ | justice | - |
| N12 | DATASUS | health | - |
| N13 | IPEA | economic | - |
| N14 | World Bank | international | 14K+ indicadores |
| N15 | dados.gov.br | government_open_data | 15K+ datasets |

---

## Agentes de Auditoria

O sistema inclui 6 auditores especializados para validação de artigos:

1. **Auditor Estatístico** - Valida estatísticas, testes qui-quadrado, p-values, intervalos de confiança
2. **Auditor Dados Econômicos** - Valida dados IBGE/IPEA/DATASUS, séries temporais
3. **Auditor de Citações** - Valida citações ABNT/APA, consistência com referências
4. **Auditor de Datasets** - Valida missing data, outliers, distribuição
5. **Auditor de Tratamento de Dados** - Valida normalização, scaling, encoding
6. **Auditor de Metodologia** - Valida rigor metodológico, amostragem, VI/VD
7. **Auditor Qualis A1** - Supervisão final para submissão

---

## Quality Gates

| Gate | Threshold | Agentes |
|------|------------|---------|
| GR0 | 1.0 | R01 |
| GR1 | 0.80 | R04,R06,R09 |
| GR2 | 0.85 | R13,R14,R15 |
| GR3 | 0.90 | R16,R17 |
| GR4 | 0.95 | R11,R12,R18 |
| GRF | 0.98 | R03,R05,R08 |

---

## Configurações JSON

### ecosystem-transformer-config.json
Configuração principal do ecossistema com todos os MCPs registrados.

### mcp_rag_config.json
Configuração específica do módulo RAG com 9 estratégias e 21 agentes.

### maswos-juridico-config.json
Configuração do MCP jurídico com 60+ agentes especializados.

### maswos-academic-config.json
Configuração do MCP acadêmico com scrapers e APIs.

### mcp_servers_config.json
Definição das portas e endpoints dos servidores MCP.

---

## Uso

```python
# Importar módulo RAG
from rag import RAGOrchestrator, AdaptiveRAG, CRAG

# Criar orchestrator
orchestrator = create_orchestrator(
    default_type="adaptive",
    enable_correction=True,
    enable_memory=True
)

# Executar pesquisa
result = orchestrator.execute(
    query="impacto mudanças climáticas saúde pública Brasil",
    strategy="adaptive"
)
```

---

## KPIs do Sistema

| Métrica | Valor Target |
|---------|--------------|
| Total de Agentes | 136+ |
| Estratégias RAG | 9 |
| Pipelines de Pesquisa | 5 |
| Scrapers Acadêmicos | 11 |
| APIs Governamentais | 7 |
| Qualidade Mínima | Qualis A1 |
| Páginas por Artigo | 110+ |
| Referências por Artigo | 80+ |

---

## Fluxo de Produção de Artigo

1. **Entrada do Usuário** → Orchestrator detecta intent
2. **Coleta de Dados** → Scrapers + APIs governamentais
3. **Processamento RAG** → 9 estratégias disponíveis
4. **Geração do Manuscrito** → 110+ páginas
5. **Auditoria Completa** → 6 auditores especializados
6. **Output Final** → Pronto para submissão Qualis A1

---

## Referências

- Versão: 5.0.0-NEXUS
- Arquitetura: Transformer-based
- Integração: Cross-MCP
- Status: Produção

---

*Documento gerado automaticamente pelo MASWOS V5 NEXUS*

