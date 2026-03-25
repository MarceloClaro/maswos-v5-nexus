# SISTEMA DE PRODUÇÃO ACADÊMICA - MASWOS V5 NEXUS

## Visão Geral

Sistema completo de produção de teses acadêmicas com **validação cruzada obrigatória** e alto rigor científico. Segue padrões **QUALIS A1** com auditoria completa.

## Arquitetura do Sistema

```
┌─────────────────────────────────────────────────────────────────────┐
│                    ACADEMIC THESIS PRODUCTION                        │
├─────────────────────────────────────────────────────────────────────┤
│                                                                      │
│  ┌─────────────────┐    ┌──────────────────┐    ┌───────────────┐  │
│  │  DEFINIÇÃO     │───▶│  VALIDAÇÃO DE    │───▶│  CRIAÇÃO DE   │  │
│  │  DO TEMA       │    │  FONTES (OBRIG)  │    │  CAPÍTULOS   │  │
│  └─────────────────┘    └──────────────────┘    └───────────────┘  │
│                                    │                    │            │
│                                    ▼                    ▼            │
│  ┌─────────────────┐    ┌──────────────────┐    ┌───────────────┐  │
│  │  ESCRITA COM    │───▶│  VALIDAÇÃO EM    │───▶│  RELATÓRIO    │  │
│  │  FONTES        │    │  3 NÍVEIS        │    │  DE AUDITORIA│  │
│  └─────────────────┘    └──────────────────┘    └───────────────┘  │
│                                                                      │
└─────────────────────────────────────────────────────────────────────┘
```

## Módulos Principais

| Arquivo | Função |
|---------|--------|
| `academic_thesis_orchestrator.py` | Orquestração principal da tese |
| `academic_source_validator.py` | Validação de fontes governamentais e acadêmicas |
| `academic_thesis_orchestrator.py` | CrossValidationEngine - Motor de validação |
| `academic_source_validator.py` | GovernmentSourceValidator + AcademicSourceValidator |
| `.agent/skills/academic-thesis-production/SKILL.md` | Skill de produção |

## Fluxo de Validação (3 Níveis)

### Nível 1: Validação Governamental
- IBGE, INEP, DATASUS, World Bank
- Verifica URL oficial governamental
- Confere autenticidade da fonte

### Nível 2: Validação Acadêmica
- arXiv, PubMed, Semantic Scholar, DOAJ, SciELO
- Verifica DOI e URL em bases acadêmicas
- Confirma publicação em periódico revisado

### Nível 3: Validação Cruzada
- Verifica consistência entre citações
- Detecta inconsistências de autor/ano
- Confirma rastreabilidade até fonte primária

## Fontes Autorizadas

### Governamentais (OBRIGATÓRIAS para dados factuais)
- IBGE: https://www.ibge.gov.br
- INEP: https://www.gov.br/inep
- DATASUS: https://datasus.saude.gov.br
- World Bank: https://data.worldbank.org
- SIDRA: https://sidra.ibge.gov.br
- IPEA: https://www.ipea.gov.br
- CNPq: https://www.cnpq.br

### Acadêmicas (OBRIGATÓRIAS para fundamentação)
- arXiv: https://arxiv.org
- PubMed: https://pubmed.ncbi.nlm.nih.gov
- Semantic Scholar: https://www.semanticscholar.org
- DOAJ: https://www.doaj.org
- SciELO: https://www.scielo.br
- CAPES Periódicos: https://periodicos.capes.gov.br

## Fontes Proibidas (REJEITADAS automaticamente)
- ❌ Blogs pessoais
- ❌ Wikis não acadêmicos
- ❌ Sites sem verificação
- ❌ Redes sociais como fonte
- ❌ Artigos sem DOI/URL verificável

## Métricas de Qualidade

| Métrica | Target QUALIS A1 | Verificação |
|---------|-----------------|--------------|
| Factual Coverage | >= 80% | Parágrafos factuais / total |
| Citation Density | >= 3/1000 words | Citações / palavras |
| Validated Sources | >= 20 | Fontes governamentais + acadêmicas |
| Quality Score | >= 9.0/10 | Média ponderada |
| ABNT Compliance | 100% | Verificação automática |
| Audit Trail | 100% | Cada ação registrada |

## Protocolo de Uso

```python
# 1. Criar tese
thesis = create_thesis("Seu Tema de Pesquisa")

# 2. Validar fontes (OBRIGATÓRIO)
gov_source = validate_academic_source({
    "authors": "IBGE",
    "title": "Censo Demográfico 2022",
    "year": 2022,
    "url": "https://www.ibge.gov.br"
})
thesis.add_validated_source(gov_source["source"])

acad_source = validate_academic_source({
    "authors": "Vaswani, A. et al.",
    "title": "Attention Is All You Need",
    "year": 2017,
    "doi": "10.48550/arXiv.1706.03762"
})
thesis.add_validated_source(acad_source["source"])

# 3. Criar capítulos e parágrafos
chapter = thesis.create_chapter(1, "INTRODUÇÃO")
thesis.add_paragraph(
    chapter_num=1,
    content="Seu texto com citação (Autor, Ano)",
    source_ids=[source_id],
    is_factual=True,
    factual_basis="Fonte que valida esta afirmação"
)

# 4. Validar e gerar relatório
print(thesis.generate_report())
```

## Regra de Ouro

> **"Se não pode ser validado cruzadamente, não existe."**

- Toda informação é rastreável até sua fonte primária
- Não há "black box" - cada afirmação é verificável
- Validação em 3 níveis impede informações não verificáveis

## Status do Sistema

✅ Sistema operacional
✅ Validação de fontes governamentais
✅ Validação de fontes acadêmicas
✅ Validação cruzada
✅ Auditoria completa
✅ Integração MCP disponível
✅ Formato ABNT verificável

## Próximos Passos

1. Usar o sistema para produção de teses
2. Integrar com MCPs de coleta de dados
3. Adicionar mais fontes governamentais brasileiras
4. Implementar validação de periódicos Qualis

---

**Versão:** 5.1.0-PHD-GRADE  
**Data:** 2026-03-23  
**Validação:** OBRIGATÓRIA em 3 níveis  
**Qualidade:** QUALIS A1 Target