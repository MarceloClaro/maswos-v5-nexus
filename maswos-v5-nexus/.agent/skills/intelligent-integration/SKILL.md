# Intelligent Integration Skill

> Sistema de integração inteligente entre agentes, MCPs e skills na rede Transformer do OpenCode.

## Quando Usar

Use este skill quando:
- Requisição requer múltiplos agentes especializados
- Necessita de skills específicos por domínio
- Requer integração entre múltiplos MCPS (juridico, academic, maswos-mcp, pageindex)
- Workflows complexos necessitam orquestração

## Arquitetura de Integração

```
User Request
     │
     ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│   Intent    │────►│   Routing   │────►│   Skill     │
│   Parser    │     │   Engine    │     │   Matcher   │
└─────────────┘     └─────────────┘     └─────────────┘
                                              │
                                              ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│    MCP      │◄────│    Agent     │◄────│  Execution  │
│   Router    │     │   Selector   │     │   Planner   │
└─────────────┘     └─────────────┘     └─────────────┘
      │                    │                    │
      ▼                    ▼                    ▼
┌─────────────┐     ┌─────────────┐     ┌─────────────┐
│ maswos-     │     │ antigravity │     │  Result     │
│ juridico    │     │   agents    │     │ Aggregator  │
└─────────────┘     └─────────────┘     └─────────────┘
```

## MCPs Disponíveis

| MCP | Domínio | Agentes | Capabilities |
|-----|---------|---------|--------------|
| maswos-juridico | Jurídico | 60 | peticao, jurisprudencia, legislacao |
| maswos-mcp | Skill Generation | 15 | create_skill, generate_agents |
| academic | Pesquisa | 55 | research_paper, collect_data, scrape_government |
| pageindex | Vectorless RAG | 10 | index_documents, query_documents, tree_reasoning |
| opencode | Coding Agent | 17 | build, edit, ask, plan, orchestrate |

## Roteamento Inteligente

| Pattern | MCP | Agents | Skills |
|---------|-----|--------|--------|
| petição, jurisprudência | juridico | 60 | legal-agents |
| artigo, pesquisa | academic | 55 | criador-de-artigo-v2 |
| criar skill | maswos-mcp | 15 | mcp-builder |
| api, backend | opencode | backend-specialist | api-patterns |
| segurança | opencode | security-auditor | vulnerability-scanner |

## Fluxo de Execução

```python
from cross_mcp_protocol import classify_and_route, execute_workflow

# Classificar e planejar rota
result = classify_and_route("Precisa de uma petição de danos")
# → intent: juridico, mcp: maswos-juridico, agents: [...]

# Executar workflow completo
await execute_workflow("Escreva artigo sobre IA")
# → executa múltiplos MCPs em paralelo
```

## Handoff entre Agentes

```python
from handoff_protocol import create_session, execute_handoff, get_full_context

# Criar sessão
session_id = create_session(
    original_request="Crie uma API",
    user_decisions=["tech=Node.js", "auth=JWT"]
)

# Handoff entre agentes
execute_handoff(
    session_id=session_id,
    from_agent="project-planner",
    to_agent="backend-specialist",
    action="Implementar API",
    quality_score=0.95
)

# Obter contexto completo
context = get_full_context(session_id)
```

## Dashboard de Monitoramento

```python
from integration_dashboard import show_dashboard, get_report

# Mostrar dashboard
show_dashboard()

# Obter relatório JSON
report = get_report()
```

## Quality Gates

| Gate | Threshold | Agents |
|------|-----------|--------|
| G0 - Input | 1.0 | intent_parser |
| G1 - Routing | 0.85 | routing_engine |
| G2 - Execution | 0.90 | cross_validator |
| G3 - Aggregation | 0.92 | result_aggregator |
| GF - Final | 0.95 | quality_scorer |

## Arquivos Criados

- `mcp_enhanced_integration.json` - Configuração completa de integração
- `cross_mcp_protocol.py` - Protocolo de comunicação cross-MCP
- `handoff_protocol.py` - Protocolo de handoff com preservação de contexto
- `integration_dashboard.py` - Dashboard de monitoramento
- `.agent/skills/intelligent-integration/SKILL.md` - Este skill