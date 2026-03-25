# MASWOS Academic RAG - Documentação de Integração

## Visão Geral

Este módulo implementa 9 tipos de RAG para o ecossistema MASWOS Academic, permitindo busca semântica em bases de artigos científicos, jurisprudência e dados governamentais.

## Arquitetura

```
┌─────────────────────────────────────────────────────────────────────┐
│                    MASWOS RAG Orchestrator                           │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │ Vanilla  │ │  Memory  │ │ Agentic  │ │  Graph   │            │
│  │   RAG    │ │   RAG    │ │   RAG    │ │   RAG    │            │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
│                                                                      │
│  ┌──────────┐ ┌──────────┐ ┌──────────┐ ┌──────────┐            │
│  │  Hybrid  │ │   CRAG   │ │ Adaptive │ │  Fusion  │            │
│  │   RAG    │ │          │ │   RAG    │ │          │            │
│  └──────────┘ └──────────┘ └──────────┘ └──────────┘            │
│                                                                      │
│  ┌──────────┐                                                      │
│  │   HyDE   │                                                      │
│  │          │                                                      │
│  └──────────┘                                                      │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Instalação

```bash
pip install sentence-transformers redis neo4j chromadb
```

## Uso Rápido

### Criando o Orchestrator

```python
from rag import create_orchestrator, RAGType

# Criar com configurações padrão
orchestrator = create_orchestrator(
    default_type="adaptive",
    enable_correction=True,
    enable_memory=True
)

# Ou usar o builder
from rag import MASWOSRAGBuilder

orchestrator = (
    MASWOSRAGBuilder()
    .with_default_rag(RAGType.ADAPTIVE)
    .with_correction(True)
    .with_memory(True)
    .with_llm_model("gpt-4")
    .build()
)
```

### Executando Queries

```python
# Query simples com RAG adaptativo (padrão)
result = orchestrator.query("Qual a relação entre educação e PIB?")

# Especificar tipo de RAG
result = orchestrator.query(
    "Quais os impactos da educação no desenvolvimento?",
    rag_type=RAGType.CRAG  # Com validação de qualidade
)

# Com memória de sessão
result = orchestrator.query(
    "Continue a análise anterior sobre desigualdade",
    rag_type=RAGType.MEMORY,
    session_id="usuario_123"
)
```

## Tipos de RAG Disponíveis

| Tipo | Descrição | Uso Ideal |
|------|-----------|-----------|
| **Vanilla** | Fluxo básico RAG | Queries simples |
| **Memory** | Com histórico Redis | Sessões longas |
| **Agentic** | Roteamento dinâmico | Múltiplas fontes |
| **Graph** | Conhecimento estrutural | Citações, autores |
| **Hybrid** | Vetorial + Grafo | Análise completa |
| **CRAG** | Validação de qualidade | Dados críticos |
| **Adaptive** | Estratégia adaptativa | Queries variadas |
| **Fusion** | Múltiplas fontes | CAPES, SciELO, etc |
| **HyDE** | Docs hipotéticos | Conceitos específicos |

## Exemplos por Tipo

### CRAG (Validação de Qualidade)

```python
# Útil para validar fontes estatísticas e jurisprudência
result = orchestrator.query(
    "Qual o PIB do Brasil em 2023?",
    rag_type=RAGType.CRAG,
    return_quality_report=True
)

print(result['correction'])
# {'original_chunks': 10, 'retained_chunks': 5, 'discarded_chunks': 5}
```

### Adaptive RAG (Estratégia Automática)

```python
# O sistema detecta complexidade automaticamente
result = orchestrator.query(
    "Compare os sistemas educacionais brasileiro e argentino",
    rag_type=RAGType.ADAPTIVE
)
# Detecta como comparativo, usa estratégia multi-step
```

### RAG-Fusion (Múltiplas Fontes)

```python
# Adicionar fontes
orchestrator.add_source_to_fusion("capes", capes_vector_store)
orchestrator.add_source_to_fusion("scielo", scielo_vector_store)
orchestrator.add_source_to_fusion("tribunais", jurisprudencia_store)

result = orchestrator.query(
    " jurisprudence on labor rights",
    rag_type=RAGType.FUSION
)
```

## Configurações Avançadas

### Com Neo4j (GraphRAG)

```python
from rag.graph import Neo4jConnector

neo4j = Neo4jConnector(
    uri="bolt://localhost:7687",
    username="neo4j",
    password="sua_senha"
)

from rag import RAGOrchestrator, RAGConfig

config = RAGConfig(default_rag_type=RAGType.GRAPH)
orchestrator = RAGOrchestrator(
    config=config,
    neo4j_connector=neo4j
)
```

### Com Redis (Memory RAG)

```python
from rag.memory import MemoryStore

memory_store = MemoryStore(
    use_redis=True,
    redis_host="localhost",
    redis_port=6379,
    expiration_seconds=86400  # 24 horas
)
```

## Integração com MASWOS Academic

O RAG pode ser integrado com os módulos existentes:

```python
# Com scrapers existentes
from capes_scraper import CAPESCollector
from ibge_complete_scraper import IBGEScraper
from jurisprudencia_mcp import JurisprudenciaMCP

# Coletar dados
capes_data = CAPESCollector().collect()
ibge_data = IBGEScraper().fetch()

# Indexar
orchestrator.get_rag(RAGType.VANILLA).index_documents(capes_data)

# Buscar com validação CRAG
result = orchestrator.query(
    "Dados sobre desigualdade educacional",
    rag_type=RAGType.CRAG
)
```

## Estatísticas do Sistema

```python
info = orchestrator.get_system_info()
print(info)

# {
#     'config': {'default_rag': 'adaptive', 'top_k': 5},
#     'available_rags': [...],
#     'stats': {'total_queries': 150, 'queries_by_type': {...}},
#     'components': {'vector_store': True, 'neo4j': False}
# }
```

## Contribuição

Para estender com novos tipos de RAG:

1. Criar novo módulo em `rag/novo_tipo/`
2. Implementar método `query(query, **kwargs)`
3. Registrar no `RAGType` enum
4. Adicionar no `RAGOrchestrator._initialize_all_rags()`

## Licença

MASWOS Academic - Multi-Agent Scientific Writing Operating System
