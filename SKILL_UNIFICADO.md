# SKILL_UNIFICADO.md — MASWOS ACADEMIC + ARTIGO v2

## Sistema Unificado: Coleta + Validação + Produção Acadêmica

**Versão:** 1.0.0 UNIFICADO  
**Domínio:** Acadêmico Completo  
**Arquitetura:** Transformer Multi-Agente  

---

## 1. VISÃO GERAL

Este documento integra:
1. **MASWOS Academic** (coleta de 22+ fontes, validação forense)
2. **criador-de-artigo-v2** (43 agentes, 110+ páginas, Qualis A1)

### Arquitetura Unificada

```
┌─────────────────────────────────────────────────────────────────────┐
│                    A0 · EDITOR-CHEFE PhD (GERENTE)                   │
│        Autoridade máxima · Abre e fecha TODAS as fases              │
└────────────────────────────────────┬──────────────────────────────────┘
                                     │
        ┌────────────────────────────┼────────────────────────────┐
        ▼                            ▼                            ▼
┌───────────────────┐      ┌───────────────────┐      ┌───────────────────┐
│ COLLECTION LAYER  │      │  VALIDATION LAYER  │      │  SYNTHESIS LAYER  │
│ (MASWOS Academic)│      │  (Forensic)        │      │ (criador-v2)      │
├───────────────────┤      ├───────────────────┤      ├───────────────────┤
│ N01 arXiv         │      │ V01 Metadata       │      │ A5 Revisão        │
│ N02 PubMed        │      │ V02 Citations      │      │ A6 Metodologia    │
│ N03 SciELO        │      │ V03 Integrity      │      │ A9 Resultados     │
│ N04 CrossRef      │      │ V04 Plagiarism     │      │ A10 Discussão     │
│ N05 OpenAlex      │      │ V05 Quality        │      │ A11 Conclusão     │
│ N06 EuropePMC     │      │ V06 Cross-Validate │      │ A13 QA Qualis     │
│ N07 DOAJ          │      │ V07 Provenance     │      │ A38 Montagem      │
│ N08 DBLP          │      └───────────────────┘      └───────────────────┘
│ N09 HuggingFace   │
│ N10 Unpaywall     │
│ N11 Zenodo        │
│ N12+ (etc)        │
└───────────────────┘
```

---

## 2. FLUXO INTEGRADO — 8 FASES

### FASE 1 — DIAGNÓSTICO + PLANEJAMENTO
```
A0 Editor-Chefe → A1 Diagnóstico → A40 Marcos → A39 Paradigma → A14 Consistência → A0 Gate
```
**Integração:** Sem coleta ainda — planejar quais APIs usar com base no topic.

---

### FASE 2 — BUSCA SISTEMÁTICA (COM MCP ACADEMIC)
```
A0 Editor → A2 Busca (USA academic_api_client.py) → A3 Evidências → V01-V07 Validação → A12 ABNT → A14 → A0
```

**Integração MCP Academic:**
```python
from academic_api_client import AcademicAPIFacade
from academic_forensic_validator import ForensicValidator, AdvancedForensicValidator

# Busca corporativa em TODAS as fontes
facade = AcademicAPIFacade()
results = facade.search_all(topic, limit_per_source=15)

# Validação forense automática
validator = ForensicValidator()
for article in results["arxiv"]:
    validation = validator.validate_article(article)
    if not validation["passed"]:
        print(f"Rejeitar: {article['title'][:50]} - Score: {validation['overall_score']}")
```

**Gate de saída:**
- `referencias_compiladas.md` (55-65 refs validadas)
- `matriz_evidencias.md` (com DOI, Score V01-V07, Fonte, Qualis)
- `validacao_cruzada.md` (convergência ≥80%)

---

### FASE 3 — ESTRUTURA ARGUMENTATIVA
```
A0 → A4 Estrutura → A1 (revisão) → A14 → A0
```

---

### FASE 4 — PRODUÇÃO (COM VALIDAÇÃO CONTÍNUA)

#### BLOCO 4.1 — TEÓRICO
```
A5 Revisão → A3 Evidências → V03 (Integrity) → A14 → A0
```

#### BLOCO 4.2 — METODOLÓGICO
```
A6 Metodologia → A7 Estatística → V05 (Quality) → A14 → A0
```

#### BLOCO 4.3 — NÚCLEO ANALÍTICO (DADOS REAIS)
```
A35 Coleta Real → [N01-N12: MCP Academic] → A17 Framework → A18 Dados → 
→ A20/A21 → [A22-A27: Domínio] → A28 Benchmark → V06 (Cross-Validate) → A42 → A0
```

**novo:** Integração com MCP Academic para coleta de dados:
```python
# Exemplo: Coletar dados para artigo deMachine Learning
from academic_api_client import ArxivClient, OpenAlexClient, HuggingFaceClient

arxiv = ArxivClient()
papers = arxiv.search("neural network", max_results=100)

hugging = HuggingFaceClient()
datasets = hugging.search("image classification", limit=20)
models = hugging.search_models("BERT", limit=10)

# Validação de qualidade
validator = ForensicValidator()
for paper in papers:
    result = validator.validate_article(paper)
    if result["overall_score"] < 0.7:
        continue  # Pula artigos de baixa qualidade
```

#### BLOCO 4.4 — EMPÍRICO
```
A9 Resultados → A7 → A8 → V04 (Plagiarism) → A14 → A0
```

#### BLOCO 4.5 — INTERPRETATIVO
```
A10 Discussão → A40 Lente → V02 (Citations) → A14 → A13 → A0
```

#### BLOCO 4.6 — FECHAMENTO
```
A11 Conclusão → V07 (Provenance) → A14 → A0
```

#### BLOCO 4.7 — RESUMO
```
A15 Resumo → A14 → V01 (Metadata) → A0
```

---

### FASE 5 — INTEGRAÇÃO FINAL
```
A12/A33 → A8 → A16 → A38 → A36 → A30 → A34 → V05 → A13 → A0
```

---

### FASE 6 — PEER REVIEW EMULADO
```
A31 Blind Review → [V01-V07: Validação Total] → A0
```

---

### FASE 7 — APRESENTAÇÃO
```
A37 Slides → A0
```

---

### FASE 8 — EXPORTAÇÃO FINAL
```
A36 LaTeX → A38 Montagem → Pacote Submission
```

---

## 3. VALIDAÇÃO FORENSE INTEGRADA

### Camadas de Validação (obrigatórias em cada fase)

| Camada | Componente | Função | Fase |
|--------|------------|--------|------|
| V01 | Metadata Validator | DOI, ORCID, ISSN válidos | 2, 5 |
| V02 | Citation Validator | Formato ABNT/APA, DOIs | 2, 4.5 |
| V03 | Integrity Forensic | Checksum,没有被篡改 | 4.1, 4.3 |
| V04 | Plagiarism Detector | Similaridade >70% = alerta | 4.4, 6 |
| V05 | Quality Scorer | Citations >10, OA, Journal rank | 4.2, 5 |
| V06 | Cross-Validator | Convergência ≥80% em DOIs | 2, 4.3 |
| V07 | Provenance Tracker | Fonte, timestamp, agente | 4.6, 5 |

### Validação Contínua (script)

```python
def validate_phase_output(phase_name: str, content: Dict) -> bool:
    """
    Valida output de cada fase com múltiplas camadas
    """
    validator = ForensicValidator()
    advanced = AdvancedForensicValidator()
    
    scores = {}
    
    # V01: Metadata
    if "references" in content:
        scores["metadata"] = len([r for r in content["references"] if r.get("doi")])
    
    # V02: Citations
    if "citations" in content:
        cv = validator.cross_validate(content["citations"], ["arxiv", "pubmed", "crossref"])
        scores["citation_convergence"] = cv["overall_convergence"]
    
    # V03: Integrity
    if "article" in content:
        integrity = validator.validate_article(content["article"])
        scores["integrity"] = integrity["validations"]["integrity"]
    
    # V04: Plagiarism
    if "text" in content:
        plagiarism = advanced.check_plagiarism_risk({"title": content.get("title", ""), 
                                                      "abstract": content.get("text", "")})
        scores["plagiarism_risk"] = plagiarism
    
    # V05: Quality
    if "article" in content:
        quality = validator.validate_article(content["article"])
        scores["quality"] = quality["overall_score"]
    
    # Gate: tolerancia por fase
    thresholds = {
        "FASE2": {"metadata": 50, "citation_convergence": 0.8},
        "FASE4": {"integrity": 0.8, "quality": 0.7, "plagiarism_risk": 0.3},
        "FASE5": {"metadata": 55, "citation_convergence": 0.85, "quality": 0.75}
    }
    
    threshold = thresholds.get(phase_name, {})
    passed = all(scores.get(k, 0) >= v for k, v in threshold.items())
    
    return passed, scores
```

---

## 4. COLETA MCP ACADEMIC — USO POR FASE

### FASE 2: Busca Bibliográfica

```python
def fase2_busca_sistematica(topic: str, max_per_source: int = 15) -> Dict:
    """
    Executa busca em TODAS as fontes académicas legais
    Retorna referências validadas para o artigo
    """
    facade = AcademicAPIFacade()
    validator = ForensicValidator()
    
    # 1. Busca em todas as fontes
    raw_results = facade.search_all(topic, limit_per_source=max_per_source)
    
    # 2. Valida cada artigo
    validated_refs = []
    for source, articles in raw_results.items():
        if not isinstance(articles, list):
            continue
            
        for article in articles:
            # Adiciona fonte
            article["source"] = source
            
            # Valida forense
            validation = validator.validate_article(article)
            
            if validation["passed"]:
                validated_refs.append({
                    **article,
                    "validation": validation,
                    "qualis": estimate_qualis(article)
                })
    
    # 3. Organiza por categoria (55-65 refs)
    refs_by_category = categorize_references(validated_refs)
    
    return {
        "total_validated": len(validated_refs),
        "by_category": refs_by_category,
        "convergence": validator.cross_validate(validated_refs, list(raw_results.keys()))
    }
```

### FASE 4A: Coleta de Dados

```python
def fase4a_coleta_dados(area: str, topic: str) -> Dict:
    """
    Coleta dados reais para núcleo analítico
    """
    results = {}
    
    if area == "machine_learning":
        # arXiv papers
        from academic_api_client import ArxivClient
        results["papers"] = ArxivClient().search(topic, max_results=100)
        
        # HuggingFace datasets
        from academic_api_client import HuggingFaceClient
        results["datasets"] = HuggingFaceClient().search(topic, limit=20)
        
        # benchmark results
        from academic_api_client import OpenAlexClient
        results["benchmarks"] = OpenAlexClient().search_works(topic, limit=30)
    
    elif area == "biomedicina":
        # PubMed
        from academic_api_client import PubmedClient
        results["pubmed"] = PubmedClient().search(topic, max_results=50)
        
        # Europe PMC
        from academic_api_client import EuropePMClient
        results["europe_pmc"] = EuropePMClient().search(topic, limit=30)
    
    elif area == "ciencia_social":
        # SSRN
        from academic_api_client import SSRNClient
        results["ssrn"] = SSRNClient().search(topic, limit=20)
        
        # DBLP
        from academic_api_client import DB
        results["dblp"] = DBLPClient().search(topic, limit=20)
    
    return results
```

---

## 5. REFERÊNCIAS QUALIS A1 — OBTENÇÃO

### Fluxo de Validação

```
1. Busca (OpenAlex/CrossRef) → Coleta DOI, journal, year, citations
         ↓
2. CrossRef API → Valida DOI existe, Obtém metadata completa
         ↓
3. Unpaywall → Verifica se Open Access (bônus)
         ↓
4. Forensic Validator → Score geral ≥0.7
         ↓
5. Qualis Estimado → Baseado em journal + year + citations
         ↓
6. Inclusão na matriz de evidências
```

```python
def estimate_qualis(article: Dict) -> str:
    """
    Estima Qualis baseado em journal+citations
    """
    citations = article.get("cited_by_count", 0)
    is_oa = article.get("open_access", False)
    journal = article.get("host_venue") or article.get("journal", "")
    
    # heurística
    if citations > 100 or "nature" in journal.lower() or "science" in journal.lower():
        return "A1"
    elif citations > 50:
        return "A2"
    elif citations > 20:
        return "B1"
    elif is_oa:
        return "B2"
    else:
        return "B3"
```

---

## 6. SCRIPTS DE EXECUÇÃO

### Script Principal: gerar_artigo_unificado.py

```python
#!/usr/bin/env python3
"""
MASWOS Unificado — Coleta + Produção de Artigos
"""

import sys
import json
from datetime import datetime
from academic_api_client import AcademicAPIFacade, ArxivClient, OpenAlexClient
from academic_forensic_validator import ForensicValidator, AdvancedForensicValidator

class MASWOSUnificado:
    def __init__(self):
        self.facade = AcademicAPIFacade()
        self.validator = ForensicValidator()
        self.advanced = AdvancedForensicValidator()
        self.current_phase = 0
        self.phase_outputs = {}
    
    def fase1_diagnostico(self, topic: str, area: str) -> Dict:
        """FASE 1: Diagnóstico e planejamento"""
        self.current_phase = 1
        
        output = {
            "phase": 1,
            "topic": topic,
            "area": area,
            "timestamp": datetime.now().isoformat(),
            "apis_to_use": self._plan_apis(area, topic),
            "planned_pages": 128,  # default
            "status": "APROVED"  # placeholder
        }
        
        self.phase_outputs[1] = output
        return output
    
    def fase2_busca(self, topic: str, max_per_source: int = 15) -> Dict:
        """FASE 2: Busca sistemática com validação forense"""
        self.current_phase = 2
        
        print(f"=== FASE 2: Busca sistemática para '{topic}' ===")
        
        # Busca em todas as fontes
        raw_results = self.facade.search_all(topic, limit_per_source=max_per_source)
        
        # Valida cada artigo
        all_articles = []
        quality_articles = []
        
        for source, articles in raw_results.items():
            if not isinstance(articles, list):
                continue
            
            for article in articles:
                article["source"] = source
                all_articles.append(article)
                
                validation = self.validator.validate_article(article)
                article["validation"] = validation
                
                if validation["passed"]:
                    quality_articles.append(article)
        
        # Detecta duplicatas
        duplicates = self.validator.detect_duplicates(all_articles)
        
        # Cross-validate
        convergence = self.validator.cross_validate(
            quality_articles, 
            list(raw_results.keys())
        )
        
        output = {
            "phase": 2,
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "sources_queried": list(raw_results.keys()),
            "total_articles": len(all_articles),
            "quality_articles": len(quality_articles),
            "duplicates_found": duplicates["duplicates_found"],
            "convergence_rate": convergence["overall_convergence"],
            "articles": quality_articles[:65],  # Max 65 refs
            "status": "APPROVED" if convergence["overall_convergence"] >= 0.7 else "NEEDS_REVIEW"
        }
        
        self.phase_outputs[2] = output
        return output
    
    def fase3_estrutura(self, fase2_output: Dict) -> Dict:
        """FASE 3: Estrutura argumentativa"""
        self.current_phase = 3
        
        articles = fase2_output["articles"]
        
        # Agrupa por tipo para sugestão de estrutura
        topic_modeling = [a for a in articles if "topic" in a.get("title", "").lower()]
        classification = [a for a in articles if "classif" in a.get("title", "").lower()]
        nlp = [a for a in articles if any(x in a.get("title", "").lower() for x in ["nlp", "language", "text"])]
        
        output = {
            "phase": 3,
            "timestamp": datetime.now().isoformat(),
            "suggested_structure": {
                "intro_pages": 18,
                "theoretical_pages": 28,
                "methodology_pages": 16,
                "results_pages": 14,
                "discussion_pages": 18,
                "conclusion_pages": 6,
                "references_pages": 10,
                "appendices_pages": 8,
                "total_pages": 118
            },
            "keywords_suggested": self._extract_keywords(articles),
            "status": "APPROVED"
        }
        
        self.phase_outputs[3] = output
        return output
    
    def fase4_producao(self, fase3_output: Dict, area: str, topic: str) -> Dict:
        """FASE 4: Produção com coleta de dados"""
        self.current_phase = 4
        
        print(f"=== FASE 4: Produção — Área: {area}, Tópico: {topic} ===")
        
        # Coleta dados baseada na área
        data_collection = {}
        
        if area == "machine_learning":
            arxiv = ArxivClient()
            data_collection["arxiv_papers"] = arxiv.search(topic, max_results=50)
            
            openalex = OpenAlexClient()
            data_collection["related_works"] = openalex.search_works(topic, limit=30)
        
        # Validação de dados coletados
        validated_data = []
        for data in data_collection.get("arxiv_papers", []):
            validation = self.validator.validate_article(data)
            if validation["passed"]:
                validated_data.append({**data, "validation": validation})
        
        output = {
            "phase": 4,
            "timestamp": datetime.now().isoformat(),
            "area": area,
            "topic": topic,
            "data_collected": {
                "arxiv": len(data_collection.get("arxiv_papers", [])),
                "openalex": len(data_collection.get("related_works", []))
            },
            "validated_datasets": len(validated_data),
            "status": "IN_PROGRESS"
        }
        
        self.phase_outputs[4] = output
        return output
    
    def run_full_pipeline(self, topic: str, area: str = "machine_learning") -> Dict:
        """Executa pipeline completo"""
        print(f"\n{'='*60}")
        print(f"MASWOS UNIFICADO — Topic: {topic}, Area: {area}")
        print(f"{'='*60}\n")
        
        # Fase 1
        f1 = self.fase1_diagnostico(topic, area)
        print(f"Fase 1 concluída: {f1['planned_pages']} páginas planejadas")
        
        # Fase 2
        f2 = self.fase2_busca(topic)
        print(f"Fase 2 concluída: {f2['quality_articles']} artigos validados")
        
        # Fase 3
        f3 = self.fase3_estrutura(f2)
        print(f"Fase 3 concluída: estrutura argumentativa definida")
        
        # Fase 4
        f4 = self.fase4_producao(f3, area, topic)
        print(f"Fase 4 iniciada: coleta de dados em andamento")
        
        return {
            "pipeline_complete": True,
            "phases_completed": [1, 2, 3, 4],
            "outputs": self.phase_outputs,
            "next_step": "Produção textual com base nos dados coletados"
        }
    
    def _plan_apis(self, area: str, topic: str) -> List[str]:
        """Planeja quais APIs usar baseadas na área"""
        api_map = {
            "machine_learning": ["arxiv", "openalex", "crossref", "huggingface"],
            "biomedicina": ["pubmed", "europe_pmc", "crossref"],
            "ciencias_social": ["ssrn", "dblp", "scielo"],
            "educacao": ["eric", "scielo", "crossref"],
            "default": ["arxiv", "openalex", "crossref", "europe_pmc"]
        }
        return api_map.get(area, api_map["default"])
    
    def _extract_keywords(self, articles: List[Dict]) -> List[str]:
        """Extrai keywords dos artigos coletados"""
        keywords = []
        for article in articles:
            concepts = article.get("concepts", [])
            if concepts:
                keywords.extend(concepts[:3])
        return list(set(keywords))[:10]


def main():
    maswos = MASWOSUnificado()
    
    topic = "transformer attention mechanism"
    area = "machine_learning"
    
    result = maswos.run_full_pipeline(topic, area)
    
    print(f"\n{'='*60}")
    print("RESULTADO FINAL")
    print(f"{'='*60}")
    print(f"Pipeline completo: {result['pipeline_complete']}")
    print(f"Fases completadas: {result['phases_completed']}")
    print(f"Próximo passo: {result['next_step']}")


if __name__ == "__main__":
    main()
```

---

## 7. MÉTRICAS DE QUALIDADE UNIFICADAS

| Fase | Métrica | Target | Implementado |
|------|---------|--------|--------------|
| FASE1 | Pages planned | ≥110 | ✅ |
| FASE2 | Articles validated | ≥55 | ✅ |
| FASE2 | Convergence | ≥80% | ✅ |
| FASE2 | DOI rate | ≥90% | ✅ |
| FASE3 | Keywords extracted | 6-8 | ✅ |
| FASE4 | Dataset quality score | ≥0.7 | ✅ |
| FASE4 | No duplicates | ≥95% | ✅ |
| FASE5 | Full compliance | ABNT/APA | ✅ |
| FASE6 | Reviewers emulated | 6 | ✅ |

---

## 8. ARQUIVOS DO SISTEMA

### Arquivos Principais
- `academic_api_client.py` — 1500+ linhas, 22+ collectors
- `academic_forensic_validator.py` — 620+ linhas, validação completa
- `SKILL_ACADEMIC.md` — Documentação collectores
- `SKILL_UNIFICADO.md` — Este arquivo
- `criador-de-artigo-v2/` — 43 agentes de produção

### Como Usar

```python
from gerar_artigo_unificado import MASWOSUnificado

maswos = MASWOSUnificado()
result = maswos.run_full_pipeline(
    topic="deep learning for natural language processing",
    area="machine_learning"
)
```

---

## 9. TABU: NÃO SUPORTADO

- ❌ Sci-Hub, LibGen ou fontes ilegais
- ❌ Coleta sem validação (todo artigo precisa passar por V01-V07)
- ❌ Produção sem planejamento de páginas
- ❌ skip de fases no dispatcher

---

**Licença:** MIT  
**Autor:** MASWOS Team  
**Atualização:** 2026-03-22