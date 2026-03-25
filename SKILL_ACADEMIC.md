# SKILL.md - MASWOS ACADEMIC COLLECTION AND VALIDATION

## Sistema Multiagente para Coleta e Validação de Artigos Acadêmicos

**Versão:** 1.0.0-ACADEMIC  
**Arquitetura:** Transformer-Agentes  
**Domínio:** Acadêmico (Fontes Legais)  
**Standards:** Open Access, FAIR, preprint servers

---

## 1. VISÃO GERAL

### 1.1 Propósito
Sistema multiagente baseado em arquitetura Transformer para coleta de artigos acadêmicos de fontes legais (arXiv, PubMed, SciELO, etc.) com validação forense de integridade.

### 1.2 Fontes Suportadas

| Fonte | Tipo | API | Status |
|-------|------|-----|--------|
| arXiv | preprint | OAI-PMH | ✅ |
| PubMed | biomedical | E-utilities | ✅ |
| SciELO | journal | articlemeta | ⚠️ timeout |
| CrossRef | metadata | REST | ✅ |
| OpenAlex | aggregate | GraphQL | ✅ |
| Semantic Scholar | aggregate | REST | ⚠️ rate limit |
| Europe PMC | biomedical | REST | ✅ |
| DOAJ | journals | API | ✅ |
| SSRN | preprint | HTML | ✅ |
| Zenodo | repository | API | ✅ |
| CORE | aggregate | OAI-PMH | ✅ |
| IEEE Xplore | journal | API | 🔐 |
| ACM DL | journal | API | 🔐 |
| DBLP | bibliography | XML | ✅ |
| bioRxiv | preprint | API | ✅ |
| medRxiv | preprint | API | ✅ |
| PhilPapers | philosophy | API | ✅ |
| Kaggle | datasets | API | 🔐 |
| Hugging Face | datasets/models | API | ✅ |
| Unpaywall | OA checker | REST | ✅ |
| Project Gutenberg | books | API | ✅ |
| OSF Projects | research | API | ✅ |
| ACL Anthology | NLP | API | ✅ |
| ERIC | education | API | ⚠️ timeout |
| Nature | journal | HTML | ✅ |
| Science | journal | HTML | ✅ |

### 1.3 Agentes Criados (18 collectors + validators)

```
┌────────────────────────────────────────────────────────────────────┐
│                      ACADEMIC ORCHESTRATOR                         │
│                     (Intent Parser + Router)                       │
└────────────────────────────────────────────────────────────────────┘
                                  │
        ┌─────────────────────────┼─────────────────────────┐
        ▼                         ▼                         ▼
┌───────────────┐        ┌───────────────┐        ┌───────────────┐
│ COLLECTOR     │        │ VALIDATOR     │        │ FORENSIC      │
│ LAYER         │        │ LAYER         │        │ LAYER         │
├───────────────┤        ├───────────────┤        ├───────────────┤
│ N01 arXiv     │        │ N07 Metadata  │        │ N11 Integrity │
│ N02 PubMed    │        │ N08 Citation  │        │ N12 Plagiarism│
│ N03 SciELO    │        │ N09 CrossRef  │        │ N13 Duplicate │
│ N04 CrossRef  │        │ N10 Source    │        │ N14 Quality   │
│ N05 OpenAlex  │        │               │        │ N15 Provenance│
│ N06 EuropePMC │        │               │        │               │
│ N17 bioRxiv   │        │               │        │               │
│ N18 DBLP      │        │               │        │               │
│ N19 HuggingFS │        │               │        │               │
│ N20 Unpaywall │        │               │        │               │
│ N21 Zenodo    │        │               │        │               │
│ N22 Kaggle    │        │               │        │               │
└───────────────┘        └───────────────┘        └───────────────┘
```

---

## 2. CAMADAS DO SISTEMA

### 2.1 COLLECTION LAYER

#### N01: arXiv Collector
- **API**: http://export.arxiv.org/api/query
- **Categorias**: cs.*, math.*, physics.*, q-bio, quant-ph
- **Rate limit**: 1 req/3s
- **Retorna**: title, abstract, authors, PDF, categories, DOI

#### N02: PubMed Collector
- **API**: E-utilities (NCBI)
- **Endpoint**: https://eutils.ncbi.nlm.nih.gov/entrez/eutils/
- **Retorna**: PMID, title, abstract, MeSH terms, citations

#### N03: SciELO Collector
- **API**: articlemeta
- **Coleções**: scl (Brasil), spa, col, mex
- **Retorna**: title, DOI, ISSN, publication date

#### N04: CrossRef Collector
- **API**: https://api.crossref.org/works
- **Retorna**: metadata completa, references, ORCID

#### N05: OpenAlex Collector
- **API**: https://api.openalex.org
- **Cobertura**: todas as fontesopen access
- **Retorna**: works, authors, venues, concepts

#### N06: Europe PMC Collector
- **API**: https://www.ebi.ac.uk/europepmc/webservices
- **Retorna**: full-text XML, abstracts, MeSH

### 2.2 VALIDATION LAYER

#### N07: Metadata Validator
- **Verifica**: DOI, ORCID, ISSN, ISBN, dates
- **Normas**: CSL, Datacite
- **Score**: Completude + Formato

#### N08: Citation Validator
- **Verifica**:格式 citations, matching with CrossRef
- **Detecta**: citações órfãs, formatos inválidos

#### N09: CrossRef Validator
- **Verifica**: existência DOIs em CrossRef
- **Score**: Taxa de match

#### N10: Source Authenticator
- **Verifica**: URL do repositório oficial
- **Score**: Confiabilidade da fonte

### 2.3 FORENSIC LAYER

#### N11: Integrity Forensic
- **Verifica**: Checksum PDF, estrutura XML
- **Detecta**: corrupção, manipulação

#### N12: Plagiarism Detector
- **Verifica**: Similaridade de abstract
- **Fontes**: CrossRef, arXiv, semantic scholar

#### N13: Duplicate Detector
- **Verifica**: DOI duplicates, title variants
- **Merge**: consolida duplicates

#### N14: Quality Scorer
- **Métricas**: Citations, journal rank, open access
- **Score**: 0-100

#### N15: Provenance Tracker
- **Rastreia**: origem do artigo, chain of custody
- **Log**: timestamp, source, agent

---

## 3. QUALITY GATES

| Gate | Nome | Threshold | Agentes |
|------|------|-----------|---------|
| G0 | Início | 1.0 | Orchestrator |
| G1 | Coleta | 0.80 | N01-N06 |
| G2 | Validação | 0.85 | N07-N10 |
| G3 | Forensic | 0.90 | N11-N15 |
| GF | Final | 0.95 | Aggregator |

---

## 4. VALIDADOR FORENSE AVANÇADO

### Classes disponíveis:

```python
from academic_forensic_validator import ForensicValidator, AdvancedForensicValidator

# Validador básico
validator = ForensicValidator()
result = validator.validate_article(article)
audit = validator.generate_audit_report(articles)
duplicates = validator.detect_duplicates(articles)

# Validador avançado
advanced = AdvancedForensicValidator()

# Computa fingerprint
fingerprint = advanced.compute_article_fingerprint(article)

# Detecta similaridade
similarity = advanced.detect_similarity(article1, article2)

# Encontra artigos similares
similar = advanced.find_similar_articles(article, corpus, threshold=0.7)

# Clusteriza artigos
clusters = advanced.cluster_articles(articles, threshold=0.7)

# Validação completa
comprehensive = advanced.comprehensive_validate(article)
```

---

## 5. COLETA DE ARTIGOS

### Exemplo de uso (Python):

```python
from academic_api_client import AcademicAPIFacade

facade = AcademicAPIFacade()

# Busca em todas as fontes
results = facade.search_all("machine learning", limit_per_source=10)

# Acessa resultados por fonte
for paper in results["arxiv"]:
    print(f"arXiv: {paper['title']}")
    
for paper in results["pubmed_ids"]:
    print(f"PubMed: {paper['title']}")
```

### API Individual:

```python
from academic_api_client import ArxivClient, PubmedClient

arxiv = ArxivClient()
papers = arxiv.search("neural network", category="cs.LG", max_results=50)

pubmed = PubmedClient()
articles = pubmed.search("COVID-19", max_results=20)
```

---

## 5. VALIDAÇÃO FORENSE

### Pipeline completo:

```python
def validate_article(article):
    # N07: Valida metadata
    metadata_score = validate_metadata(article)
    
    # N08: Valida citações
    citation_score = validate_citations(article)
    
    # N11: Verifica integridade
    integrity_score = check_integrity(article)
    
    # N12: Detecta plágio
    plagiarism_score = check_plagiarism(article)
    
    # N14: Calcula qualidade
    quality_score = calculate_quality(article)
    
    return {
        "scores": {
            "metadata": metadata_score,
            "citation": citation_score,
            "integrity": integrity_score,
            "plagiarism": plagiarism_score,
            "quality": quality_score
        },
        "overall": (metadata_score + citation_score + integrity_score + 
                   plagiarism_score + quality_score) / 5
    }
```

---

## 6. MÉTRICAS

| Métrica | Target | Descrição |
|---------|--------|-----------|
| Coleta | 100% | Artigos encontrados |
| Validação | ≥85% | Metadata válida |
| Integridade | 100% | Checksum OK |
| Qualidade | ≥70% | Score médio |
| Duplicates | <5% | Taxa de duplicatas |

---

## 7. AGENTES ESPECIALIZADOS

### Por Domínio
| ID | Domínio | Fontes |
|----|---------|--------|
| A1 | CS/AI | arXiv, DBLP, ACM |
| A2 | Biomedical | PubMed, Europe PMC |
| A3 | Multidisciplinary | OpenAlex, CrossRef |
| A4 | Brasileira | SciELO, LILACS, BVS |

### Por Função
| ID | Função | Descrição |
|----|--------|-----------|
| C1 | Aggregator | Consolida resultados |
| V1 | Verifier | Verifica dados |
| F1 | Forensic | Análise forense |
| R1 | Reporter | Gera relatórios |

---

## 6. REFERÊNCIAS

- arXiv API: https://arxiv.org/help/api
- NCBI E-utilities: https://www.ncbi.nlm.nih.gov/books/NBK25501/
- CrossRef API: https://www.crossref.org/documentation/retrieve-metadata/rest-api/
- OpenAlex: https://docs.openalex.org/
- SciELO: https://articlemeta.scielo.org/
- bioRxiv API: https://www.biorxiv.org/about(*about*)
- DBLP: https://dblp.org/xml
- Unpaywall: https://unpaywall.org/products/api
- Hugging Face: https://huggingface.co/api

---

## 7. MÉTRICAS DE COLETA

| Métrica | Target | Atual |
|---------|--------|-------|
| Taxa de sucesso | ≥95% | ~85% |
| Tempo médio | <5s/fonte | ~3s |
| Duplicatas | <5% | implementado |
| Validação | ≥85% | implementado |

---

## 8. LIMITE DE RESPONSABILIDADE

**APENAS FONTES LEGAIS**: Este sistema usa exclusivamente APIs públicas e legais. Não suporta Sci-Hub, LibGen ou outras fontes piracy.

**Licença**: MIT  
**Autor**: MASWOS Team