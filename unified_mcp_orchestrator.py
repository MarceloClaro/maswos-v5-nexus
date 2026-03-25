#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - Unified MCP Orchestrator
Orquestra todos os MCPs e scrapers do ecossistema

Arquitetura: Transformer-Agentes
MCPS: maswos-juridico, maswos-mcp, pageindex, opencode
Scrapers: 15+ fontes (arXiv, PubMed, CAPES, IBGE, etc.)
"""

import json
import os
import logging
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from datetime import datetime

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("UnifiedOrchestrator")

@dataclass
class MCPStatus:
    name: str
    endpoint: str
    status: str
    latency_ms: float = 0
    capabilities: List[str] = None
    error: Optional[str] = None

class UnifiedMCPOrchestrator:
    """
    Orquestrador unificado de todos os MCPs
    
    Integra:
    - PageIndex (vectorless RAG)
    - OpenCode (AI coding agent)
    - Scraper Collection (15+ fontes)
    - MASWOS Jurídico (60 agentes)
    - MASWOS MCP (skill generation)
    """
    
    def __init__(self):
        self.mcps: Dict[str, MCPStatus] = {}
        self.scrapers = None
        self.pageindex_client = None
        self._init_components()
    
    def _init_components(self):
        """Inicializa componentes"""
        # PageIndex
        try:
            from pageindex_mcp_integration import PageIndexMCPClient
            self.pageindex_client = PageIndexMCPClient()
            self.mcps["pageindex"] = MCPStatus(
                name="pageindex",
                endpoint="https://api.pageindex.ai/mcp",
                status="configured" if self.pageindex_client.api_key else "no_api_key",
                capabilities=["index_documents", "query_documents", "tree_reasoning"]
            )
        except Exception as e:
            logger.warning(f"PageIndex not available: {e}")
            self.mcps["pageindex"] = MCPStatus(
                name="pageindex",
                endpoint="https://api.pageindex.ai/mcp",
                status="error",
                error=str(e)
            )
        
        # OpenCode MCP
        self.mcps["opencode"] = MCPStatus(
            name="opencode",
            endpoint="stdio",
            status="active",
            capabilities=["ai_coding", "multi_model", "plan_mode"]
        )
        
        # Scraper Orchestrator
        try:
            from transformer_scraper_integration import CollectionOrchestrator
            self.scrapers = CollectionOrchestrator()
            self.mcps["scrapers"] = MCPStatus(
                name="scrapers",
                endpoint="internal",
                status="active",
                capabilities=["academic_collection", "brazilian_data", "international_data"]
            )
        except Exception as e:
            logger.warning(f"Scrapers not available: {e}")
        
        # MASWOS Jurídico (simulado)
        self.mcps["maswos_juridico"] = MCPStatus(
            name="maswos-juridico",
            endpoint="http://localhost:3001/mcp",
            status="configured",
            capabilities=["peticoes", "jurisprudencia", "legislacao"]
        )
        
        # MASWOS MCP
        self.mcps["maswos_mcp"] = MCPStatus(
            name="maswos-mcp",
            endpoint="http://localhost:3002/mcp",
            status="configured",
            capabilities=["skill_generation", "agent_factory"]
        )
    
    def status(self) -> Dict:
        """Retorna status de todos os MCPs"""
        return {
            "mcp_count": len(self.mcps),
            "timestamp": datetime.now().isoformat(),
            "mcps": {
                name: {
                    "endpoint": mcp.endpoint,
                    "status": mcp.status,
                    "latency_ms": mcp.latency_ms,
                    "capabilities": mcp.capabilities,
                    "error": mcp.error
                }
                for name, mcp in self.mcps.items()
            }
        }
    
    def query(self, query: str, strategy: str = "all") -> Dict:
        """
        Query unificado usando estratégia otimizada
        
        Estratégias:
        - all: Todos os MCPs
        - academic: Scrapers acadêmicos
        - document: PageIndex + OpenCode
        - legal: MASWOS Jurídico
        """
        results = {
            "query": query,
            "strategy": strategy,
            "timestamp": datetime.now().isoformat(),
            "results": {}
        }
        
        if strategy in ["all", "academic"]:
            if self.scrapers:
                results["results"]["scrapers"] = self.scrapers.collect_with_strategy(
                    query, "academic", limit=10
                )
        
        if strategy in ["all", "document"]:
            if self.pageindex_client:
                try:
                    page_result = self.pageindex_client.query("", query)
                    results["results"]["pageindex"] = {
                        "status": page_result.status,
                        "documents": page_result.query_results or []
                    }
                except Exception as e:
                    results["results"]["pageindex"] = {"status": "error", "error": str(e)}
        
        return results


# Funções de conveniência
def get_orchestrator() -> UnifiedMCPOrchestrator:
    """Obtém instância do orquestrador"""
    return UnifiedMCPOrchestrator()

def quick_query(query: str, strategy: str = "all") -> Dict:
    """Query rápido"""
    orchestrator = get_orchestrator()
    return orchestrator.query(query, strategy)


# Teste
def test_unified_orchestrator():
    """Testa orquestrador unificado"""
    print("=" * 70)
    print("MASWOS V5 NEXUS - Unified MCP Orchestrator Test")
    print("=" * 70)
    
    orchestrator = UnifiedMCPOrchestrator()
    
    # Status
    print("\n[STATUS] MCPs Configurados")
    status = orchestrator.status()
    print(f"  Total MCPs: {status['mcp_count']}")
    for name, mcp in status['mcps'].items():
        print(f"  - {name}: {mcp['status']}")
        if mcp.get('capabilities'):
            print(f"    Capabilities: {', '.join(mcp['capabilities'][:3])}...")
    
    # Quick query
    print("\n[QUERY] Testando: 'machine learning'")
    result = orchestrator.query("machine learning", "academic")
    print(f"  Strategy: {result['strategy']}")
    if result['results'].get('scrapers'):
        s = result['results']['scrapers']
        print(f"  Scrapers: {s.get('successful', 0)}/{s.get('total_sources', 0)}")
    
    print("\n" + "=" * 70)
    print("Unified Orchestrator - Ready!")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    test_unified_orchestrator()
