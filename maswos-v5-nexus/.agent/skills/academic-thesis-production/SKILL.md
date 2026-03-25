# Academic Thesis Production Skill

> Sistema de produção de teses acadêmicas com validação cruzada obrigatória e alto rigor científico.

## Quando Usar

Use este skill **OBRIGATORIAMENTE** para:
- Produzir qualquer artigo científico
- Produzir dissertação de mestrado
- Produzir tese de doutorado
- Produzir trabalho acadêmico
- Qualquer produção que exija fundamentação científica

## Princípios Fundamentais (PROIBIDO VIOLAR)

### 1. Validação Cruzada OBRIGATÓRIA
- **NENHUMA** afirmação factual pode ser feita sem fonte validada
- **TODAS** as fontes DEVEM ser verificadas via `academic_source_validator.py`
- Fontes governamentais (IBGE, INEP, DATASUS, World Bank) são **OBRIGATÓRIAS**
- Fontes acadêmicas (arXiv, PubMed, Semantic Scholar) são **OBRIGATÓRIAS**

### 2. Rastreabilidade Total
- Toda citação deve ter auditoría
- Todo dado deve ter fonte verificável
- Todo argumento deve ter fundamentação

### 3. Formato ABNT
- Citações (Autor, Ano)
- Notas de rodapé formatadas
- Referências bibliográficas completas

### 4. Qualidade QUALIS A1
- Estrutura IMRAD completa
- Metodologia explícita
- Resultados verificáveis
- Discussão crítica
- Contribuições originais

## Arquitetura do Sistema

### Módulos

| Módulo | Função |
|--------|--------|
| `academic_thesis_orchestrator.py` | Orquestração principal da tese |
| `academic_source_validator.py` | Validação de fontes governamentais e acadêmicas |
| `cross_mcp_protocol.py` | Integração com MCPs para coleta de dados |
| `handoff_protocol.py` | Gestão de contexto entre agentes |
| `integration_dashboard.py` | Monitoramento da produção |

### Fluxo de Produção

```
1. DEFINIÇÃO
   ├── Definir tema/tópico
   ├── Definir tipo (artigo/dissertação/tese)
   └── Definir área de conhecimento

2. VALIDAÇÃO DE FONTES (OBRIGATÓRIO)
   ├── Adicionar fontes governamentais (IBGE, INEP, etc)
   ├── Adicionar fontes acadêmicas (arXiv, PubMed, etc)
   └── Validar cada fonte via UnifiedSourceValidator

3. ESTRUTURAÇÃO
   ├── Criar capítulos/seções
   ├── Definir fluxo argumentativo
   └── Planejar seções (Intro, Metodologia, etc)

4. ESCRITA COM VALIDAÇÃO
   ├── Escrever parágrafo
   ├── Vincular fontes validadas (OBRIGATÓRIO)
   ├── Marcar afirmações factuais
   └── Validar via CrossValidationEngine

5. VALIDAÇÃO FINAL
   ├── Verificar ABNT
   ├── Verificar qualidade
   ├── Gerar relatório de auditoria
   └── Verificar score >= 9.0

6. REVISÃO (se necessário)
   ├── Corrigir erros identificados
   ├── Re-validar seções
   └── Preparar para submissão
```

## Uso do Sistema

### Passo 1: Criar Tese
```python
from academic_thesis_orchestrator import create_thesis

thesis = create_thesis("Inteligência Artificial na Educação Brasileira")
```

### Passo 2: Adicionar Fontes Validadas (OBRIGATÓRIO)
```python
from academic_source_validator import validate_academic_source

# Fonte governamental
ibge_source = validate_academic_source({
    "authors": "IBGE",
    "title": "Censo Demográfico 2022",
    "year": 2022,
    "url": "https://www.ibge.gov.br",
    "pages": "45"
})

# Fonte acadêmica
arxiv_source = validate_academic_source({
    "authors": "Vaswani, A. et al.",
    "title": "Attention Is All You Need",
    "year": 2017,
    "url": "https://arxiv.org/abs/1706.03762",
    "doi": "10.48550/arXiv.1706.03762",
    "pages": "5998"
})

# Adicionar à tese
thesis.add_validated_source(ibge_source["source"])
thesis.add_validated_source(arxiv_source["source"])
```

### Passo 3: Escrever Capítulos
```python
# Criar capítulo
chapter1 = thesis.create_chapter(1, "INTRODUÇÃO")

# Adicionar parágrafo com fontes (OBRIGATÓRIO)
thesis.add_paragraph(
    chapter_num=1,
    content="Segundo dados do IBGE (2022), a região Nordeste representa...",
    source_ids=["source_id_1"],  # ID da fonte validada
    is_factual=True,
    factual_basis="Dados oficiais do IBGE"
)
```

### Passo 4: Validar e Gerar Relatório
```python
print(thesis.generate_report())
```

## Validação de Fontes - Fontes Autorizadas

### Fontes Governamentais (OBRIGATÓRIAS)
- IBGE: https://www.ibge.gov.br
- INEP: https://www.gov.br/inep
- DATASUS: https://datasus.saude.gov.br
- World Bank: https://data.worldbank.org
- SIDRA: https://sidra.ibge.gov.br
- IPEA: https://www.ipea.gov.br
- CNPq: https://www.cnpq.br

### Fontes Acadêmicas (OBRIGATÓRIAS)
- arXiv: https://arxiv.org
- PubMed: https://pubmed.ncbi.nlm.nih.gov
- Semantic Scholar: https://www.semanticscholar.org
- DOAJ: https://www.doaj.org
- SciELO: https://www.scielo.br
- CAPES Periódicos: https://periodicos.capes.gov.br

### Fontes Proibidas
- ❌ blogs pessoais
- ❌ wikis não académicos
- ❌ sites sem verificação
- ❌ redes sociais como fonte
- ❌ artigos sem DOI/URL verificável

## Métricas de Qualidade

| Métrica | Target | Verificação |
|---------|--------|--------------|
| Factual Coverage | >= 80% | Parágrafos factuais / total |
| Citation Density | >= 3/1000 words | Citações / palavras |
| Validated Sources | >= 20 | Fontes governamentais + acadêmicas |
| Quality Score | >= 9.0/10 | Média ponderada |
| ABNT Compliance | 100% | Verificação automática |

## Regra de Ouro

> **"Se não pode ser validado cruzadamente, não existe."**

 Toda informação gerada por este sistema é rastreável até sua fonte primária. Não há "black box" - cada afirmação pode ser verificada até sua origem.

## Arquivos do Sistema

- `academic_thesis_orchestrator.py` - Orquestrador principal
- `academic_source_validator.py` - Validador de fontes
- `cross_mcp_protocol.py` - Integração MCP
- `handoff_protocol.py` - Gestão de contexto
- `integration_dashboard.py` - Monitoramento
- `mcp_enhanced_integration.json` - Configuração MCP