#!/usr/bin/env python3
"""
MASWOS Unificado — Coleta + Produção de Artigos
Sistema Integrado: MCP Academic +criador-de-artigo-v2
"""

import sys
import json
from datetime import datetime
from typing import Dict, List, Optional, Any
from academic_api_client import (
    AcademicAPIFacade, ArxivClient, OpenAlexClient, CrossrefClient,
    PubmedClient, EuropePMClient, DBLPClient, DOAJClient, HuggingFaceClient
)
from academic_forensic_validator import ForensicValidator, AdvancedForensicValidator

class MASWOSUnificado:
    """
    Sistema unificado que integra:
    - Coleta acadêmica (MCP Academic)
    - Validação forense
    - Produção de artigos (criador-de-artigo-v2)
    """
    
    def __init__(self):
        self.facade = AcademicAPIFacade()
        self.validator = ForensicValidator()
        self.advanced = AdvancedForensicValidator()
        self.current_phase = 0
        self.phase_outputs = {}
        self.validation_history = []
        
    def fase1_diagnostico(self, topic: str, area: str) -> Dict:
        """FASE 1: Diagnóstico e planejamento"""
        self.current_phase = 1
        
        output = {
            "phase": 1,
            "topic": topic,
            "area": area,
            "timestamp": datetime.now().isoformat(),
            "apis_to_use": self._plan_apis(area, topic),
            "planned_pages": 128,
            "min_references": 55,
            "max_references": 65,
            "status": "APPROVED"
        }
        
        self.phase_outputs[1] = output
        print(f"[OK] Fase 1 concluida: {output['planned_pages']} paginas planejadas")
        return output
    
    def fase2_busca(self, topic: str, max_per_source: int = 15) -> Dict:
        """FASE 2: Busca sistemática com validação forense completa"""
        self.current_phase = 2
        
        print(f"\n=== FASE 2: Busca sistemática para '{topic}' ===")
        
        raw_results = self.facade.search_all(topic, limit_per_source=max_per_source)
        
        all_articles = []
        quality_articles = []
        
        for source, articles in raw_results.items():
            if not isinstance(articles, list):
                continue
            
            for article in articles:
                if not isinstance(article, dict):
                    continue
                    
                article["source"] = source
                all_articles.append(article)
                
                validation = self.validator.validate_article(article)
                article["validation"] = validation
                
                if validation["passed"]:
                    article["qualis_estimated"] = self._estimate_qualis(article)
                    quality_articles.append(article)
        
        duplicates = self.validator.detect_duplicates(all_articles)
        
        sources_queried = [s for s in raw_results.keys() if raw_results.get(s)]
        
        convergence = self.validator.cross_validate(quality_articles, sources_queried)
        
        output = {
            "phase": 2,
            "topic": topic,
            "timestamp": datetime.now().isoformat(),
            "sources_queried": sources_queried,
            "total_articles_found": len(all_articles),
            "articles_validated": len(quality_articles),
            "duplicates_found": duplicates["duplicates_found"],
            "convergence_rate": convergence["overall_convergence"],
            "references": quality_articles[:65],
            "status": "APPROVED" if convergence["overall_convergence"] >= 0.7 else "NEEDS_REVIEW"
        }
        
        self.phase_outputs[2] = output
        
        print(f"  Fontes consultadas: {len(sources_queried)}")
        print(f"  Total artigos: {len(all_articles)}")
        print(f"  Validados (score ≥0.7): {len(quality_articles)}")
        print(f"  Duplicatas: {duplicates['duplicates_found']}")
        print(f"  Convergência: {convergence['overall_convergence']:.1%}")
        
        return output
    
    def fase3_estrutura(self, fase2_output: Dict) -> Dict:
        """FASE 3: Estrutura argumentativa"""
        self.current_phase = 3
        
        articles = fase2_output["references"]
        
        topic_modeling = [a for a in articles if "topic" in a.get("title", "").lower()]
        classification = [a for a in articles if "classif" in a.get("title", "").lower()]
        nlp = [a for a in articles if any(x in a.get("title", "").lower() for x in ["nlp", "language", "text"])]
        
        output = {
            "phase": 3,
            "timestamp": datetime.now().isoformat(),
            "suggested_structure": {
                "pre_text": 8,
                "abstract_pt_en": 2,
                "chapter1_intro": 18,
                "chapter2_theoretical": 28,
                "chapter3_methodology": 16,
                "chapter4_results": 14,
                "chapter5_discussion": 18,
                "chapter6_conclusion": 6,
                "references": 10,
                "appendices": 8,
                "total_pages": 128
            },
            "keywords_suggested": self._extract_keywords(articles),
            "article_classification": {
                "topic_modeling": len(topic_modeling),
                "classification": len(classification),
                "nlp": len(nlp)
            },
            "status": "APPROVED"
        }
        
        self.phase_outputs[3] = output
        print(f"[OK] Fase 3 concluida: estrutura de 128 paginas definida")
        
        return output
    
    def fase4_producao(self, fase3_output: Dict, area: str, topic: str) -> Dict:
        """FASE 4: Produção com coleta de dados específicos"""
        self.current_phase = 4
        
        print(f"\n=== FASE 4: Coleta de dados para {area} / {topic} ===")
        
        data_collection = {}
        
        if area in ["machine_learning", "ai", "data_science"]:
            arxiv = ArxivClient()
            data_collection["arxiv_papers"] = arxiv.search(topic, max_results=50)
            
            openalex = OpenAlexClient()
            data_collection["related_works"] = openalex.search_works(topic, limit=30)
            
            from academic_api_client import HuggingFaceClient
            hugging = HuggingFaceClient()
            data_collection["datasets"] = hugging.search(topic, limit=20)
            data_collection["models"] = hugging.search_models(topic, limit=10)
        
        elif area in ["biomedicina", "saude", "medicina"]:
            pubmed = PubmedClient()
            data_collection["pubmed_articles"] = pubmed.search(topic, max_results=50)
            
            europe_pmc = EuropePMClient()
            data_collection["europe_pmc"] = europe_pmc.search(topic, limit=30)
        
        elif area in ["ciencias_sociais", "sociologia", "educacao"]:
            from academic_api_client import SSRNClient, ERICClient
            ssrn = SSRNClient()
            data_collection["ssrn"] = ssrn.search(topic, limit=20)
            
            eric = ERICClient()
            data_collection["eric"] = eric.search(topic, limit=20)
        
        validated_data = []
        all_data = []
        
        for key, items in data_collection.items():
            if isinstance(items, list):
                for item in items:
                    item["data_type"] = key
                    all_data.append(item)
                    
                    validation = self.validator.validate_article(item)
                    if validation["passed"]:
                        validated_data.append({**item, "validation": validation})
        
        output = {
            "phase": 4,
            "timestamp": datetime.now().isoformat(),
            "area": area,
            "topic": topic,
            "data_sources_queried": list(data_collection.keys()),
            "total_items_collected": len(all_data),
            "validated_items": len(validated_data),
            "validation_rate": len(validated_data) / len(all_data) if all_data else 0,
            "sample_data": validated_data[:10] if validated_data else [],
            "status": "IN_PROGRESS"
        }
        
        self.phase_outputs[4] = output
        
        print(f"  Fontes de dados: {list(data_collection.keys())}")
        print(f"  Itens coletados: {len(all_data)}")
        print(f"  Validados: {len(validated_data)} ({len(validated_data)/len(all_data):.1%})")
        
        return output
    
    def run_full_pipeline(self, topic: str, area: str = "machine_learning") -> Dict:
        """Executa pipeline completo de 4 fases"""
        print(f"\n{'='*60}")
        print(f"MASWOS UNIFICADO — Geração de Artigos Acadêmicos")
        print(f"Tópico: {topic}")
        print(f"Área: {area}")
        print(f"{'='*60}\n")
        
        f1 = self.fase1_diagnostico(topic, area)
        
        f2 = self.fase2_busca(topic)
        
        f3 = self.fase3_estrutura(f2)
        
        f4 = self.fase4_producao(f3, area, topic)
        
        output = {
            "pipeline_complete": True,
            "phases_completed": [1, 2, 3, 4],
            "summary": {
                "topic": topic,
                "area": area,
                "planned_pages": f1["planned_pages"],
                "references_count": len(f2["references"]),
                "convergence_rate": f2["convergence_rate"],
                "data_collected": f4["total_items_collected"]
            },
            "next_steps": [
                "Redigir revisão de literatura (FASE 4.1)",
                "Elaborar metodologia (FASE 4.2)",
                "Executar análise (FASE 4.3)",
                "Redigir resultados (FASE 4.4)",
                "Discutir achados (FASE 4.5)"
            ]
        }
        
        self.phase_outputs["final"] = output
        
        print(f"\n{'='*60}")
        print("RESUMO FINAL")
        print(f"{'='*60}")
        print(f"Páginas planejadas: {f1['planned_pages']}")
        print(f"Referências validadas: {len(f2['references'])}")
        print(f"Taxa de convergência: {f2['convergence_rate']:.1%}")
        print(f"Dados coletados: {f4['total_items_collected']}")
        
        return output
    
    def _plan_apis(self, area: str, topic: str) -> List[str]:
        """Planeja APIs baseadas na área"""
        api_map = {
            "machine_learning": ["arxiv", "openalex", "crossref", "huggingface", "dblp"],
            "ai": ["arxiv", "openalex", "semantic_scholar", "crossref"],
            "data_science": ["arxiv", "kaggle", "huggingface", "openalex"],
            "biomedicina": ["pubmed", "europe_pmc", "crossref", "biorxiv"],
            "saude": ["pubmed", "europe_pmc", "crossref"],
            "medicina": ["pubmed", "europe_pmc"],
            "ciencias_sociais": ["ssrn", "dblp", "scielo"],
            "sociologia": ["ssrn", "scielo", "eric"],
            "educacao": ["eric", "scielo", "crossref"],
            "default": ["arxiv", "openalex", "crossref", "europe_pmc"]
        }
        return api_map.get(area, api_map["default"])
    
    def _extract_keywords(self, articles: List[Dict]) -> List[str]:
        """Extrai keywords dos artigos"""
        keywords = []
        for article in articles:
            concepts = article.get("concepts", [])
            if concepts:
                keywords.extend(concepts[:3])
            if article.get("categories"):
                keywords.extend(article.get("categories", [])[:2])
        return list(set(keywords))[:10]
    
    def _estimate_qualis(self, article: Dict) -> str:
        """Estima Qualis baseado em journal+citations+OA"""
        citations = article.get("cited_by_count", 0)
        is_oa = article.get("open_access", False)
        journal = article.get("host_venue") or article.get("journal", "") or ""
        
        if citations > 100 or "nature" in journal.lower() or "science" in journal.lower():
            return "A1"
        elif citations > 50 or "plos" in journal.lower() or "bmc" in journal.lower():
            return "A2"
        elif citations > 20:
            return "B1"
        elif is_oa or citations > 5:
            return "B2"
        else:
            return "B3"


def main():
    """Executa pipeline de exemplo"""
    maswos = MASWOSUnificado()
    
    topic = input("Tópico do artigo: ") or "transformer attention mechanism"
    area = input("Área (machine_learning/biomedicina/ciencias_sociais): ") or "machine_learning"
    
    result = maswos.run_full_pipeline(topic, area)
    
    print("\n" + "="*60)
    print("PRÓXIMOS PASSOS")
    print("="*60)
    for step in result["next_steps"]:
        print(f"  → {step}")
    
    return result


if __name__ == "__main__":
    main()