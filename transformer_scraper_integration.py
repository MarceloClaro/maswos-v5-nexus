#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - Transformer-Scraper Integration
Integra todos os scrapers ao ecossistema Transformer-Agentes

Arquitetura: Encoder → Collection (Scrapers) → Validation → Analysis → Synthesis → Output

Scrapers integrados:
- ARXIV: Artigos científicos
- PUBMED: Artigos biomédicos
- SEMANTICSCHOLAR: 200M+ papers
- DOAJ: Periódicos OA
- CORE: 300M+ OA papers
- AMINER: China academic
- DADOSGOV: Dados abertos Brasil
- CAPES: Portal de Periódicos
- IBGE: Dados demográficos Brasil
- WORLD_BANK: Indicadores mundiais
- INTERNATIONAL: ONGs, WHO, IMF, FAO
- INTERNET_ARCHIVE: Historical data
- OPENREVIEW: AI conferences
"""

import json
import time
import logging
from datetime import datetime
from typing import Dict, List, Optional, Any, Tuple
from dataclasses import dataclass, field
from enum import Enum
from pathlib import Path

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("TransformerScraper")

SCRAPER_REGISTRY = {}
SCRAPER_AGENTS = {}


class ScraperSource(Enum):
    ARXIV = "arxiv"
    PUBMED = "pubmed"
    SEMANTICSCHOLAR = "semantic_scholar"
    DOAJ = "doaj"
    CORE = "core"
    AMINER = "aminer"
    CNKI = "cnki"
    DADOSGOV = "dados_gov"
    CAPES = "capes"
    IBGE = "ibge"
    WORLD_BANK = "world_bank"
    WORLD_BANK_DOCS = "world_bank_documents"
    INTERNATIONAL = "international_organizations"
    INTERNET_ARCHIVE = "internet_archive"
    OPENREVIEW = "openreview"
    OPENALEX = "openalex"


@dataclass
class ScraperResult:
    source: str
    query: str
    status: str
    data: Optional[Dict] = None
    error: Optional[str] = None
    latency_ms: float = 0
    cached: bool = False
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


@dataclass
class CollectionContext:
    query: str
    sources: List[str]
    domain: str = "general"
    tier: str = "STANDARD"
    limit: int = 10
    filters: Dict[str, Any] = field(default_factory=dict)
    metadata: Dict[str, Any] = field(default_factory=dict)


class TransformerScraperAgent:
    """
    Agente de coleta mapeado para Transformer Layer: Collection
    Coordena coleta de dados de múltiplas fontes usando scrapers
    """
    
    def __init__(self, agent_id: str, sources: List[str]):
        self.agent_id = agent_id
        self.sources = sources
        self.scrapers = {}
        self._init_scrapers()
        
    def _init_scrapers(self):
        """Inicializa scrapers disponíveis"""
        # Importar scrapers do advanced_scraping_engine
        try:
            from advanced_scraping_engine import AdvancedScrapingOrchestrator
            self.orchestrator = AdvancedScrapingOrchestrator()
            logger.info(f"[TransformerScraper] Orchestrator initialized with sources: {self.sources}")
        except ImportError as e:
            logger.error(f"[TransformerScraper] Failed to import orchestrator: {e}")
            self.orchestrator = None
        
        # Mapear fontes para scrapers
        self.source_mapping = {
            "ARXIV": "ARXIV",
            "PUBMED": "PUBMED",
            "SEMANTICSCHOLAR": "SEMANTICSCHOLAR",
            "DOAJ": "DOAJ",
            "CORE": "CORE",
            "AMINER": "AMINER",
            "DADOSGOV": "DADOSGOV",
            "CAPES": "CAPES",
            "IBGE": "IBGE",
            "WORLD_BANK": "WORLD_BANK",
            "WORLD_BANK_DOCS": "WORLD_BANK_DOCS",
            "INTERNATIONAL": "INTERNATIONAL",
            "INTERNET_ARCHIVE": "INTERNET_ARCHIVE",
            "OPENREVIEW": "OPENREVIEW",
            "OPENALEX": "OPENALEX"
        }
    
    def collect(self, context: CollectionContext) -> Dict[str, ScraperResult]:
        """Executa coleta de dados de múltiplas fontes"""
        logger.info(f"[TransformerScraper] Collecting from {len(context.sources)} sources")
        
        results = {}
        start_time = time.time()
        
        for source in context.sources:
            scraper_key = self.source_mapping.get(source.upper(), source.upper())
            
            try:
                result = self._collect_from_source(
                    scraper_key,
                    context.query,
                    context.limit,
                    context.filters
                )
                results[source] = result
            except Exception as e:
                logger.error(f"[TransformerScraper] Error collecting from {source}: {e}")
                results[source] = ScraperResult(
                    source=source,
                    query=context.query,
                    status="error",
                    error=str(e)
                )
        
        total_time = (time.time() - start_time) * 1000
        logger.info(f"[TransformerScraper] Collection completed in {total_time:.0f}ms")
        
        return {
            "results": results,
            "total_sources": len(context.sources),
            "successful": sum(1 for r in results.values() if r.status == "success"),
            "failed": sum(1 for r in results.values() if r.status != "success"),
            "total_latency_ms": total_time
        }
    
    def _collect_from_source(self, source: str, query: str, limit: int, filters: Dict) -> ScraperResult:
        """Coleta dados de uma fonte específica"""
        start_time = time.time()
        
        if not self.orchestrator:
            return ScraperResult(
                source=source,
                query=query,
                status="error",
                error="Orchestrator not available"
            )
        
        try:
            result = self.orchestrator.scrape_with_fallback(source, query, limit=limit)
            
            return ScraperResult(
                source=source,
                query=query,
                status=result.status,
                data=result.data,
                error=result.error,
                latency_ms=result.latency_ms,
                cached=result.cached
            )
        except Exception as e:
            return ScraperResult(
                source=source,
                query=query,
                status="error",
                error=str(e),
                latency_ms=(time.time() - start_time) * 1000
            )
    
    def collect_all(self, query: str, limit: int = 10) -> Dict[str, ScraperResult]:
        """Coleta de todas as fontes disponíveis"""
        all_sources = list(self.source_mapping.keys())
        context = CollectionContext(query=query, sources=all_sources, limit=limit)
        result = self.collect(context)
        return result.get("results", {})


class AcademicCollectionAgent(TransformerScraperAgent):
    """Agente especializado em coleta acadêmica"""
    
    def __init__(self, agent_id: str = "academic_collector"):
        sources = ["ARXIV", "PUBMED", "SEMANTICSCHOLAR", "DOAJ", "CORE", "AMINER", "OPENALEX", "OPENREVIEW"]
        super().__init__(agent_id, sources)
        self.academic_domains = {
            "cs": ["ARXIV", "SEMANTICSCHOLAR", "OPENREVIEW"],
            "biomedical": ["PUBMED", "SEMANTICSCHOLAR", "DOAJ"],
            "general": ["ARXIV", "PUBMED", "SEMANTICSCHOLAR", "DOAJ"]
        }
    
    def collect_academic(self, query: str, domain: str = "general", limit: int = 10) -> Dict:
        """Coleta dados acadêmicos filtrados por domínio"""
        sources = self.academic_domains.get(domain, self.academic_domains["general"])
        context = CollectionContext(query=query, sources=sources, domain=domain, limit=limit)
        return self.collect(context)


class BrazilianDataAgent(TransformerScraperAgent):
    """Agente especializado em dados brasileiros"""
    
    def __init__(self, agent_id: str = "brazilian_data_collector"):
        sources = ["DADOSGOV", "CAPES", "IBGE", "INTERNET_ARCHIVE"]
        super().__init__(agent_id, sources)
        self.data_types = {
            "demographic": ["IBGE"],
            "government": ["DADOSGOV", "IBGE"],
            "academic": ["CAPES"],
            "historical": ["INTERNET_ARCHIVE"]
        }
    
    def collect_brazilian(self, query: str, data_type: str = "all", limit: int = 10) -> Dict:
        """Coleta dados brasileiros filtrados por tipo"""
        if data_type == "all":
            sources = self.sources
        else:
            sources = self.data_types.get(data_type, self.sources)
        
        context = CollectionContext(query=query, sources=sources, domain="brazilian", limit=limit)
        return self.collect(context)


class InternationalDataAgent(TransformerScraperAgent):
    """Agente especializado em dados internacionais"""
    
    def __init__(self, agent_id: str = "international_data_collector"):
        sources = ["WORLD_BANK", "WORLD_BANK_DOCS", "INTERNATIONAL"]
        super().__init__(agent_id, sources)
    
    def collect_international(self, query: str, limit: int = 10) -> Dict:
        """Coleta dados internacionais"""
        context = CollectionContext(query=query, sources=self.sources, domain="international", limit=limit)
        return self.collect(context)


class CollectionOrchestrator:
    """
    Orquestrador de coleta - coordena múltiplos agentes de coleta
    Mapeado para Transformer: Multi-Head Attention no Collection Layer
    """
    
    def __init__(self):
        self.agents = {
            "transformer_scraper": TransformerScraperAgent("main_collector", []),
            "academic": AcademicCollectionAgent(),
            "brazilian": BrazilianDataAgent(),
            "international": InternationalDataAgent()
        }
        logger.info(f"[CollectionOrchestrator] Initialized with {len(self.agents)} agents")
    
    def collect_with_strategy(self, query: str, strategy: str = "all", **kwargs) -> Dict:
        """
        Coleta dados usando estratégia específica
        
        Estratégias:
        - all: Todas as fontes
        - academic: Apenas fontes acadêmicas
        - brazilian: Apenas fontes brasileiras
        - international: Apenas fontes internacionais
        - balanced: Fontes acadêmicas + brasileiras + internacionais
        """
        strategies = {
            "all": self._collect_all,
            "academic": self._collect_academic,
            "brazilian": self._collect_brazilian,
            "international": self._collect_international,
            "balanced": self._collect_balanced
        }
        
        collector = strategies.get(strategy, self._collect_all)
        return collector(query, **kwargs)
    
    def _collect_all(self, query: str, **kwargs) -> Dict:
        """Coleta de todas as fontes"""
        limit = kwargs.get("limit", 10)
        agent = self.agents["transformer_scraper"]
        context = CollectionContext(
            query=query,
            sources=list(agent.source_mapping.keys()),
            limit=limit
        )
        return agent.collect(context)
    
    def _collect_academic(self, query: str, **kwargs) -> Dict:
        """Coleta acadêmica"""
        limit = kwargs.get("limit", 10)
        domain = kwargs.get("domain", "general")
        return self.agents["academic"].collect_academic(query, domain, limit)
    
    def _collect_brazilian(self, query: str, **kwargs) -> Dict:
        """Coleta brasileira"""
        limit = kwargs.get("limit", 10)
        data_type = kwargs.get("data_type", "all")
        return self.agents["brazilian"].collect_brazilian(query, data_type, limit)
    
    def _collect_international(self, query: str, **kwargs) -> Dict:
        """Coleta internacional"""
        limit = kwargs.get("limit", 10)
        return self.agents["international"].collect_international(query, limit)
    
    def _collect_balanced(self, query: str, **kwargs) -> Dict:
        """Coleta balanceada: acadêmico + brasileiro + internacional"""
        limit = kwargs.get("limit", 10)
        
        results = {
            "academic": self._collect_academic(query, limit=limit // 3 + 1),
            "brazilian": self._collect_brazilian(query, limit=limit // 3 + 1),
            "international": self._collect_international(query, limit=limit // 3)
        }
        
        return {
            "strategy": "balanced",
            "results": results,
            "total_sources": (
                results["academic"].get("successful", 0) +
                results["brazilian"].get("successful", 0) +
                results["international"].get("successful", 0)
            )
        }


# Registry de agentes para ecossistema Transformer
def register_scraper_agents():
    """Registra agentes no ecossistema"""
    global SCRAPER_AGENTS
    
    SCRAPER_AGENTS = {
        "transformer_scraper": TransformerScraperAgent("main_collector", []),
        "academic_collector": AcademicCollectionAgent(),
        "brazilian_collector": BrazilianDataAgent(),
        "international_collector": InternationalDataAgent(),
        "collection_orchestrator": CollectionOrchestrator()
    }
    
    return SCRAPER_AGENTS


def get_collection_agent(agent_type: str = "main") -> Optional[TransformerScraperAgent]:
    """Obtém agente de coleta específico"""
    global SCRAPER_AGENTS
    
    if not SCRAPER_AGENTS:
        register_scraper_agents()
    
    return SCRAPER_AGENTS.get(agent_type)


# Mapeamento Transformer-Agentes para Collection Layer
TRANSFORMER_COLLECTION_MAPPING = {
    "Input Embedding": "Query Encoder",
    "Positional Encoding": "Source Prioritizer", 
    "Encoder Stack": "Multi-Source Collector",
    "Self-Attention": "Cross-Source Correlator",
    "Layer Normalization": "Quality Normalizer",
    "Feed-Forward": "Data Enricher",
    "Output Projection": "Result Formatter"
}


# Funções de conveniência
def collect_academic_papers(query: str, limit: int = 10, domain: str = "general") -> Dict:
    """Coleta rápida de papers acadêmicos"""
    agent = get_collection_agent("academic")
    if agent:
        return agent.collect_academic(query, domain, limit)
    return {"error": "Agent not available"}


def collect_brazilian_data(query: str, limit: int = 10, data_type: str = "all") -> Dict:
    """Coleta rápida de dados brasileiros"""
    agent = get_collection_agent("brazilian")
    if agent:
        return agent.collect_brazilian(query, data_type, limit)
    return {"error": "Agent not available"}


def collect_all_sources(query: str, limit: int = 10) -> Dict:
    """Coleta de todas as fontes"""
    orchestrator = CollectionOrchestrator()
    return orchestrator.collect_with_strategy(query, "all", limit=limit)


# Teste
def test_collection():
    """Testa integração de coleta"""
    print("=" * 70)
    print("MASWOS V5 NEXUS - Transformer-Scraper Integration Test")
    print("=" * 70)
    
    orchestrator = CollectionOrchestrator()
    
    # Test 1: Coleta acadêmica
    print("\n[TEST 1] Coleta Acadêmica: 'machine learning'")
    result = orchestrator.collect_with_strategy("machine learning", "academic", limit=5)
    print(f"  Fontes bem-sucedidas: {result.get('successful', 0)}/{result.get('total_sources', 0)}")
    
    # Test 2: Coleta brasileira
    print("\n[TEST 2] Coleta Brasileira: 'educacao'")
    result = orchestrator.collect_with_strategy("educacao", "brazilian", limit=5)
    print(f"  Fontes bem-sucedidas: {result.get('successful', 0)}/{result.get('total_sources', 0)}")
    
    # Test 3: Coleta balanceada
    print("\n[TEST 3] Coleta Balanceada: 'saude publica'")
    result = orchestrator.collect_with_strategy("saude publica", "balanced", limit=9)
    print(f"  Total fontes: {result.get('total_sources', 0)}")
    
    # Test 4: Coleta completa
    print("\n[TEST 4] Coleta Completa: 'artificial intelligence'")
    result = orchestrator.collect_all("artificial intelligence", limit=3)
    successful = result.get("successful", 0)
    total = result.get("total_sources", 0)
    print(f"  Resultado: {successful}/{total} fontes")
    
    print("\n" + "=" * 70)
    print("Transformer-Scraper Integration - Testes Concluídos")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    test_collection()
