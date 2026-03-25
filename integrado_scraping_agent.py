#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - Integrado Scraping Agent
Agente integrado de scraping granular e cirúrgico para MCPS jurídicos

Arquitetura: Transformer-Agentes (Encoder → Scraper → Validator → Decoder)
Camada: Collection (N04-N12)
"""

import json
import time
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, asdict

# Importar scraping engine
try:
    from advanced_scraping_engine import (
        AdvancedScrapingOrchestrator,
        ScrapingResult,
        STFScraper,
        IBGEScraper,
        PubMedScraper
    )
    HAS_SCRAPING_ENGINE = True
except ImportError:
    HAS_SCRAPING_ENGINE = False

@dataclass
class ScrapingAgentRequest:
    """Requisição do agente de scraping"""
    source: str
    query: str
    params: Dict[str, Any] = None
    priority: str = "normal"  # low, normal, high, critical
    require_fresh: bool = False

@dataclass
class ScrapingAgentResponse:
    """Resposta do agente de scraping"""
    success: bool
    data: Optional[Dict] = None
    error: Optional[str] = None
    source: str = ""
    technique: str = ""
    cached: bool = False
    latency_ms: float = 0
    transformer_layer: str = "Collection"

class IntegratedScrapingAgent:
    """
    Agente integrado de scraping para MCPS jurídicos
    
    Implementa arquitetura Transformer-Agentes:
    - Encoder: Parse da requisição
    - Collection: Scraping granular
    - Validation: Validação dos dados
    - Decoder: Formatação da resposta
    """
    
    def __init__(self, cache_ttl_hours: int = 24):
        self.agent_id = "N12_integrated_scraper"
        self.layer = "Collection"
        
        if HAS_SCRAPING_ENGINE:
            self.orchestrator = AdvancedScrapingOrchestrator(cache_ttl_hours)
        else:
            self.orchestrator = None
    
    def process_request(self, request: ScrapingAgentRequest) -> ScrapingAgentResponse:
        """Processar requisição de scraping"""
        start_time = time.time()
        
        if not self.orchestrator:
            return ScrapingAgentResponse(
                success=False,
                error="Scraping engine não disponível",
                source=request.source
            )
        
        try:
            # Encoder: Parse e validação
            validated_request = self._encoder_layer(request)
            
            # Collection: Scraping
            scraping_result = self._collection_layer(validated_request)
            
            # Validation: Verificar qualidade
            validated_data = self._validation_layer(scraping_result)
            
            # Decoder: Formatação final
            final_response = self._decoder_layer(validated_data)
            
            latency = (time.time() - start_time) * 1000
            
            return ScrapingAgentResponse(
                success=True,
                data=final_response,
                source=scraping_result.source,
                technique=scraping_result.technique,
                cached=scraping_result.cached,
                latency_ms=round(latency, 2),
                transformer_layer=self.layer
            )
            
        except Exception as e:
            return ScrapingAgentResponse(
                success=False,
                error=str(e),
                source=request.source,
                latency_ms=round((time.time() - start_time) * 1000, 2)
            )
    
    def _encoder_layer(self, request: ScrapingAgentRequest) -> ScrapingAgentRequest:
        """Camada Encoder: Parse e normalização"""
        # Normalizar source
        source_map = {
            'stf': 'STF',
            'supremo': 'STF',
            'tribunal': 'STF',
            'ibge': 'IBGE',
            'demografico': 'IBGE',
            'pubmed': 'PUBMED',
            'medico': 'PUBMED',
            'europe_pmc': 'PUBMED'
        }
        
        normalized_source = source_map.get(request.source.lower(), request.source.upper())
        
        return ScrapingAgentRequest(
            source=normalized_source,
            query=request.query,
            params=request.params or {},
            priority=request.priority,
            require_fresh=request.require_fresh
        )
    
    def _collection_layer(self, request: ScrapingAgentRequest) -> ScrapingResult:
        """Camada Collection: Scraping granular e cirúrgico"""
        
        params = request.params or {}
        
        if request.source == 'STF':
            return self.orchestrator.stf_scraper.search_jurisprudencia(
                request.query,
                limit=params.get('limit', 10)
            )
        
        elif request.source == 'IBGE':
            return self.orchestrator.ibge_scraper.get_demographic_data(
                municipality_code=params.get('municipality_code')
            )
        
        elif request.source == 'PUBMED':
            return self.orchestrator.pubmed_scraper.search_articles(
                request.query,
                limit=params.get('limit', 20)
            )
        
        else:
            # Tentar com orchestrator genérico
            return self.orchestrator.scrape_with_fallback(
                request.source,
                request.query,
                **params
            )
    
    def _validation_layer(self, result: ScrapingResult) -> ScrapingResult:
        """Camada Validation: Verificar qualidade dos dados"""
        
        if result.status != "success" or not result.data:
            return result
        
        # Verificar se há dados mínimos
        data = result.data
        
        if result.source == "STF":
            if data.get("total_results", 0) == 0:
                # Tentar técnica alternativa
                result.data["warning"] = "Nenhum resultado encontrado, dados podem estar incompletos"
        
        elif result.source == "IBGE":
            if "data" not in data and "indicators" not in data:
                result.data["warning"] = "Dados demográficos incompletos"
        
        elif result.source == "PUBMED":
            if data.get("total_results", 0) == 0:
                result.data["warning"] = "Nenhum artigo encontrado"
        
        return result
    
    def _decoder_layer(self, result: ScrapingResult) -> Dict:
        """Camada Decoder: Formatação para output"""
        
        return {
            "agent_id": self.agent_id,
            "layer": self.layer,
            "source": result.source,
            "technique": result.technique,
            "cached": result.cached,
            "data": result.data,
            "metadata": {
                "status": result.status,
                "latency_ms": result.latency_ms,
                "timestamp": result.timestamp
            }
        }
    
    def get_capabilities(self) -> Dict:
        """Retornar capacidades do agente"""
        return {
            "agent_id": self.agent_id,
            "layer": self.layer,
            "description": "Agente de scraping granular e cirúrgico",
            "supported_sources": ["STF", "IBGE", "PUBMED"],
            "techniques": {
                "STF": ["portal_search", "transparencia_search", "api_alternative"],
                "IBGE": ["api_sidra", "api_localidades", "scraping_web", "cache_fallback"],
                "PUBMED": ["europe_pmc_api", "ncbi_api", "scraping_europe_pmc"]
            },
            "features": [
                "retry_with_backoff",
                "cache_management",
                "browser_headers_rotation",
                "ssl_bypass",
                "fallback_strategies"
            ]
        }


class IntegratedScrapingWorkflow:
    """
    Workflow integrado de scraping para MCPS
    
    Coordena múltiplos agentes de scraping
    """
    
    def __init__(self):
        self.agent = IntegratedScrapingAgent()
        self.workflow_log = []
    
    def execute_jurisprudencia_search(self, query: str, courts: List[str] = None) -> Dict:
        """Executar busca de jurisprudência em múltiplos tribunais"""
        
        if courts is None:
            courts = ["STF"]
        
        results = {}
        
        for court in courts:
            request = ScrapingAgentRequest(
                source=court,
                query=query,
                params={"limit": 10},
                priority="high"
            )
            
            response = self.agent.process_request(request)
            
            results[court] = {
                "success": response.success,
                "data": response.data,
                "technique": response.technique,
                "cached": response.cached,
                "latency_ms": response.latency_ms
            }
            
            self.workflow_log.append({
                "action": "jurisprudencia_search",
                "court": court,
                "query": query,
                "success": response.success,
                "latency_ms": response.latency_ms,
                "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
            })
        
        return {
            "workflow": "jurisprudencia_search",
            "query": query,
            "courts": courts,
            "results": results,
            "summary": {
                "total_courts": len(courts),
                "successful": sum(1 for r in results.values() if r["success"]),
                "total_latency_ms": sum(r["latency_ms"] for r in results.values())
            }
        }
    
    def execute_demographic_analysis(self, municipality_code: str = None) -> Dict:
        """Executar análise demográfica"""
        
        request = ScrapingAgentRequest(
            source="IBGE",
            query="",
            params={"municipality_code": municipality_code},
            priority="normal"
        )
        
        response = self.agent.process_request(request)
        
        self.workflow_log.append({
            "action": "demographic_analysis",
            "municipality_code": municipality_code,
            "success": response.success,
            "latency_ms": response.latency_ms,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        })
        
        return {
            "workflow": "demographic_analysis",
            "municipality_code": municipality_code,
            "result": {
                "success": response.success,
                "data": response.data,
                "technique": response.technique,
                "latency_ms": response.latency_ms
            }
        }
    
    def execute_literature_search(self, query: str, max_results: int = 20) -> Dict:
        """Executar busca na literatura científica"""
        
        request = ScrapingAgentRequest(
            source="PUBMED",
            query=query,
            params={"limit": max_results},
            priority="normal"
        )
        
        response = self.agent.process_request(request)
        
        self.workflow_log.append({
            "action": "literature_search",
            "query": query,
            "success": response.success,
            "latency_ms": response.latency_ms,
            "timestamp": time.strftime("%Y-%m-%dT%H:%M:%SZ")
        })
        
        return {
            "workflow": "literature_search",
            "query": query,
            "result": {
                "success": response.success,
                "data": response.data,
                "technique": response.technique,
                "cached": response.cached,
                "latency_ms": response.latency_ms
            }
        }
    
    def get_workflow_report(self) -> Dict:
        """Gerar relatório do workflow"""
        
        return {
            "agent_id": self.agent.agent_id,
            "total_executions": len(self.workflow_log),
            "workflow_log": self.workflow_log,
            "capabilities": self.agent.get_capabilities()
        }


# Instância global
integrated_workflow = IntegratedScrapingWorkflow()

def test_integrated_scraping():
    """Testar agente integrado de scraping"""
    
    print("=" * 70)
    print("MASWOS V5 NEXUS - Integrated Scraping Agent Test")
    print("=" * 70)
    
    if not HAS_SCRAPING_ENGINE:
        print("[ERRO] Scraping engine não disponível")
        return False
    
    workflow = IntegratedScrapingWorkflow()
    
    # Teste 1: Jurisprudência STF
    print("\n[TEST 1] Jurisprudência STF")
    result = workflow.execute_jurisprudencia_search(
        "direito administrativo licitação",
        courts=["STF"]
    )
    print(f"  Success: {result['results']['STF']['success']}")
    print(f"  Technique: {result['results']['STF']['technique']}")
    print(f"  Latency: {result['summary']['total_latency_ms']:.2f}ms")
    
    # Teste 2: Dados demográficos
    print("\n[TEST 2] Análise Demográfica")
    result = workflow.execute_demographic_analysis("2303706")  # Crateus-CE
    print(f"  Success: {result['result']['success']}")
    print(f"  Technique: {result['result']['technique']}")
    print(f"  Latency: {result['result']['latency_ms']:.2f}ms")
    
    # Teste 3: Literatura científica
    print("\n[TEST 3] Literatura Científica")
    result = workflow.execute_literature_search("machine learning法学", max_results=5)
    print(f"  Success: {result['result']['success']}")
    print(f"  Technique: {result['result']['technique']}")
    print(f"  Cached: {result['result']['cached']}")
    print(f"  Latency: {result['result']['latency_ms']:.2f}ms")
    
    # Relatório
    print("\n" + "=" * 70)
    print("Workflow Report:")
    report = workflow.get_workflow_report()
    print(f"  Total Executions: {report['total_executions']}")
    print(f"  Agent ID: {report['agent_id']}")
    
    return True

if __name__ == "__main__":
    test_integrated_scraping()