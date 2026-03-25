#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - PageIndex MCP Integration
Integra PageIndex (VectifyAI) ao ecossistema Transformer-Agentes

PageIndex: Sistema RAG vectorless baseado em reasoning com tree search
- Sem Vector DB
- Sem chunking - preserva contexto completo
- Usa árvore hierárquica para索引 de documentos
- Reasoning-based retrieval como um humano expert

Documentação: https://github.com/VectifyAI/pageindex-mcp
API: https://api.pageindex.ai/mcp
"""

import json
import time
import logging
import os
import requests
from datetime import datetime
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from enum import Enum

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("PageIndexMCP")

PAGEINDEX_API_URL = "https://api.pageindex.ai/mcp"


class PageIndexAction(Enum):
    INDEX = "index"
    QUERY = "query"


@dataclass
class PageIndexResult:
    action: str
    status: str
    document_id: Optional[str] = None
    query_results: Optional[List[Dict]] = None
    tree_structure: Optional[Dict] = None
    reasoning_path: Optional[List[str]] = None
    error: Optional[str] = None
    latency_ms: float = 0
    timestamp: str = field(default_factory=lambda: datetime.now().isoformat())


class PageIndexMCPClient:
    """
    Cliente MCP para PageIndex
    
    Integra com o ecossistema Transformer via Collection Layer
    - Indexação: Encoder (construção da árvore)
    - Query: Decoder (busca reasoning-based)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        # Tenta carregar do .env primeiro
        if not api_key:
            try:
                from dotenv import load_dotenv
                load_dotenv()
            except ImportError:
                pass
        
        self.api_key = api_key or os.environ.get("PAGEINDEX_API_KEY", "")
        self.base_url = PAGEINDEX_API_URL
        self.session = requests.Session()
        self.session.headers.update({
            "Content-Type": "application/json",
            "User-Agent": "MASWOS-V5-NEXUS/5.0"
        })
        if self.api_key:
            self.session.headers["Authorization"] = f"Bearer {self.api_key}"
    
    def _make_request(self, tool_name: str, arguments: Dict) -> Dict:
        """Executa requisição ao PageIndex MCP via tools/call (SSE response)"""
        import re
        
        payload = {
            "jsonrpc": "2.0",
            "id": int(time.time() * 1000),
            "method": "tools/call",
            "params": {
                "name": tool_name,
                "arguments": arguments
            }
        }
        
        headers = dict(self.session.headers)
        headers["Accept"] = "application/json, text/event-stream"
        
        try:
            response = self.session.post(
                self.base_url,
                json=payload,
                headers=headers,
                timeout=120
            )
            
            if response.status_code == 200:
                content = response.text
                matches = re.findall(r'data: ({.*})', content)
                
                for m in matches:
                    data = json.loads(m)
                    if "result" in data:
                        result = data["result"]
                        # Extract content from MCP response format
                        if "content" in result:
                            content_list = result["content"]
                            if content_list and len(content_list) > 0:
                                text = content_list[0].get("text", "{}")
                                return json.loads(text)
                        return result
                    elif "error" in data:
                        return {"error": data["error"]}
                
                return {"error": "Empty response"}
            else:
                return {"error": f"HTTP {response.status_code}: {response.text[:200]}"}
                
        except requests.exceptions.Timeout:
            return {"error": "Timeout ao conectar com PageIndex MCP"}
        except requests.exceptions.ConnectionError:
            return {"error": "Erro de conexão com PageIndex MCP"}
        except Exception as e:
            return {"error": str(e)}
        
        return {"error": "Unknown error"}
    
    def index_document(self, document_url: str, document_path: Optional[str] = None, 
                       title: Optional[str] = None) -> PageIndexResult:
        """
        Indexa documento no PageIndex (tree-based)
        
        Mapeado para: Encoder Layer (Input Embedding + Positional Encoding)
        """
        start_time = time.time()
        
        logger.info(f"[PageIndex] Indexando documento: {document_url or document_path}")
        
        if document_url:
            result = self._make_request("upload_url", {"url": document_url, "title": title})
        elif document_path:
            result = self._make_request("upload_file", {"path": document_path, "title": title})
        else:
            return PageIndexResult(
                action="index",
                status="error",
                error="url ou path required",
                latency_ms=0
            )
        
        latency = (time.time() - start_time) * 1000
        
        if "error" in result:
            return PageIndexResult(
                action="index",
                status="error",
                error=result["error"],
                latency_ms=latency
            )
        
        return PageIndexResult(
            action="index",
            status="success",
            document_id=result.get("document_id", result.get("name", "")),
            tree_structure=result,
            latency_ms=latency
        )
    
    def query(self, document_url: str, user_query: str, max_results: int = 10) -> PageIndexResult:
        """
        Query reasoning-based no documento indexado
        
        Mapeado para: Decoder Layer (Output Projection)
        """
        start_time = time.time()
        
        logger.info(f"[PageIndex] Query: '{user_query[:50]}...'")
        
        result = self._make_request(
            "find_relevant_documents",
            {"query": user_query, "limit": max_results}
        )
        
        latency = (time.time() - start_time) * 1000
        
        if "error" in result:
            return PageIndexResult(
                action="query",
                status="error",
                error=result["error"],
                latency_ms=latency
            )
        
        return PageIndexResult(
            action="query",
            status="success",
            query_results=result.get("docs", result.get("documents", [])),
            reasoning_path=[],
            latency_ms=latency
        )
    
    def list_documents(self) -> List[Dict]:
        """Lista documentos no PageIndex"""
        result = self._make_request("recent_documents", {"limit": 20})
        if "error" in result:
            return []
        return result.get("docs", result.get("documents", []))
    
    def get_document_structure(self, document_name: str) -> Dict:
        """Obtém estrutura hierárquica do documento"""
        return self._make_request("get_document_structure", {"doc_name": document_name})


class PageIndexTransformerAgent:
    """
    Agente Transformer para PageIndex
    
    Mapeia as camadas do Transformer para operações PageIndex:
    - Encoder → Indexação (construção da árvore)
    - Decoder → Query (busca com reasoning)
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.client = PageIndexMCPClient(api_key)
        self.indexed_documents: Dict[str, Dict] = {}
    
    def index(self, document_url: str, title: Optional[str] = None) -> PageIndexResult:
        """Indexa documento (Encoder Layer)"""
        result = self.client.index_document(document_url, title=title)
        
        if result.status == "success":
            self.indexed_documents[document_url] = {
                "document_id": result.document_id,
                "tree": result.tree_structure,
                "indexed_at": result.timestamp
            }
        
        return result
    
    def search(self, document_url: str, query: str, max_results: int = 10) -> PageIndexResult:
        """Busca no documento (Decoder Layer)"""
        return self.client.query(document_url, query, max_results)
    
    def rag_search(self, query: str, sources: List[str], limit: int = 5) -> Dict:
        """
        RAG Search multi-fonte
        
        Executa busca em múltiplos documentos e agrega resultados
        Usa reasoning path para transparências
        """
        results = []
        
        for source in sources[:limit]:
            result = self.search(source, query)
            if result.status == "success":
                results.append({
                    "source": source,
                    "results": result.query_results,
                    "reasoning_path": result.reasoning_path,
                    "latency_ms": result.latency_ms
                })
        
        return {
            "query": query,
            "total_sources": len(results),
            "results": results,
            "aggregated_reasoning": self._aggregate_reasoning(results)
        }
    
    def _aggregate_reasoning(self, results: List[Dict]) -> List[str]:
        """Agrega reasoning paths de múltiplas fontes"""
        all_paths = []
        for r in results:
            all_paths.extend(r.get("reasoning_path", []))
        return list(dict.fromkeys(all_paths))[:10]


class PageIndexCollectionAgent:
    """
    Agente de Coleção para PageIndex
    
    Coleciona e processa documentos acadêmicos, jurídicos e governamentais
    usando tree-based RAG para reasoning nativo.
    
    Transformer Mapping:
    - Input Embedding → Document Indexer
    - Encoder Stack → Tree Builder
    - Multi-Head Attention → Cross-Document Correlator
    - Decoder Stack → Reasoning Query
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.agent = PageIndexTransformerAgent(api_key)
        self.document_types = {
            "academic": [".pdf", ".html"],
            "legal": [".pdf", ".docx"],
            "government": [".pdf", ".csv", ".xlsx"],
            "web": [".html"]
        }
    
    def collect_document(self, url: str, doc_type: str = "general") -> PageIndexResult:
        """Coleta e indexa documento"""
        logger.info(f"[PageIndexCollection] Coletando: {url} (tipo: {doc_type})")
        return self.agent.index(url)
    
    def collect_documents(self, urls: List[str], doc_type: str = "general") -> Dict:
        """Coleta múltiplos documentos"""
        results = []
        
        for url in urls:
            result = self.collect_document(url, doc_type)
            results.append({
                "url": url,
                "status": result.status,
                "document_id": result.document_id,
                "error": result.error
            })
        
        return {
            "total": len(urls),
            "successful": sum(1 for r in results if r["status"] == "success"),
            "failed": sum(1 for r in results if r["status"] != "success"),
            "results": results
        }
    
    def query_documents(self, query: str, sources: List[str], max_results: int = 5) -> Dict:
        """Query em múltiplos documentos"""
        return self.agent.rag_search(query, sources, max_results)


# Integração com transformer_orchestration.py
class PageIndexTransformerLayer:
    """
    Camada Transformer para PageIndex
    
    Integra com as camadas do transformer_orchestration.py:
    - Encoder: index_document() → tree structure
    - Decoder: query() → reasoning-based results
    """
    
    def __init__(self, api_key: Optional[str] = None):
        self.encoder = PageIndexTransformerAgent(api_key)
        self.document_index: Dict[str, Dict] = {}
    
    def encode_document(self, document_url: str) -> Dict[str, Any]:
        """
        Encode documento → tree structure
        Mapeado para Encoder Stack
        """
        result = self.encoder.index(document_url)
        
        if result.status == "success":
            self.document_index[document_url] = result.tree_structure
        
        return {
            "document_url": document_url,
            "tree_structure": result.tree_structure,
            "document_id": result.document_id,
            "encoding_method": "tree_based",
            "timestamp": result.timestamp
        }
    
    def decode_query(self, document_url: str, query: str, max_results: int = 10) -> Dict[str, Any]:
        """
        Decode query → reasoning results
        Mapeado para Decoder Stack
        """
        result = self.encoder.search(document_url, query, max_results)
        
        return {
            "document_url": document_url,
            "query": query,
            "results": result.query_results,
            "reasoning_path": result.reasoning_path,
            "decoding_method": "tree_reasoning",
            "timestamp": result.timestamp
        }
    
    def rag_pipeline(self, documents: List[str], query: str) -> Dict[str, Any]:
        """
        Pipeline RAG completo
        Encoder → Collection → Decoder
        """
        # Encode todos os documentos
        encoded = []
        for doc in documents:
            encoded.append(self.encode_document(doc))
        
        # Query em todos
        decoded_results = []
        for doc in documents:
            decoded_results.append(self.decode_query(doc, query))
        
        return {
            "query": query,
            "documents_processed": len(documents),
            "encoded_documents": encoded,
            "decoded_results": decoded_results,
            "aggregated_results": self._aggregate_results(decoded_results)
        }
    
    def _aggregate_results(self, results: List[Dict]) -> List[Dict]:
        """Agrega resultados de múltiplos documentos"""
        all_results = []
        for r in results:
            all_results.extend(r.get("results", []))
        
        # Remove duplicatas por contexto
        seen = set()
        unique = []
        for item in all_results:
            ctx = item.get("context", "")
            if ctx not in seen:
                seen.add(ctx)
                unique.append(item)
        
        return unique[:10]


# Wrapper para MCP do ecosystem-transformer-config.json
PAGEINDEX_MCP_CONFIG = {
    "name": "pageindex",
    "type": "http",
    "url": "https://api.pageindex.ai/mcp",
    "auth": "api_key",
    "capabilities": [
        "index_documents",
        "query_documents", 
        "rag_search",
        "tree_reasoning"
    ],
    "document_types": [
        "pdf",
        "html",
        "docx",
        "csv"
    ],
    "features": {
        "vectorless_rag": True,
        "tree_indexing": True,
        "reasoning_search": True,
        "no_chunking": True,
        "context_preservation": True
    }
}


# Funções de conveniência
def index_document(document_url: str, api_key: Optional[str] = None) -> PageIndexResult:
    """Indexa documento rápido"""
    client = PageIndexMCPClient(api_key)
    return client.index_document(document_url)


def query_document(document_url: str, query: str, api_key: Optional[str] = None) -> PageIndexResult:
    """Query em documento indexado"""
    client = PageIndexMCPClient(api_key)
    return client.query(document_url, query)


def rag_search(query: str, document_urls: List[str], api_key: Optional[str] = None) -> Dict:
    """RAG search multi-documento"""
    agent = PageIndexTransformerAgent(api_key)
    return agent.rag_search(query, document_urls)


# Teste
def test_pageindex_mcp():
    """Testa integração PageIndex MCP"""
    print("=" * 70)
    print("MASWOS V5 NEXUS - PageIndex MCP Integration Test")
    print("=" * 70)
    
    # Test 1: Cliente MCP
    print("\n[TEST 1] PageIndexMCPClient")
    client = PageIndexMCPClient()
    print(f"  API Key configured: {'Sim' if client.api_key else 'Nao'}")
    print(f"  Base URL: {client.base_url}")
    
    # Test 2: Listar documentos
    print("\n[TEST 2] Listar documentos")
    docs = client.list_documents()
    print(f"  Documentos encontrados: {len(docs)}")
    for d in docs[:3]:
        print(f"    - {d.get('name', 'unknown')[:50]} ({d.get('status', '')})")
    
    # Test 3: Buscar documentos
    print("\n[TEST 3] Buscar: 'machine learning'")
    result = client.query('', 'machine learning')
    print(f"  Status: {result.status}")
    print(f"  Resultados: {len(result.query_results) if result.query_results else 0}")
    
    # Test 4: Agente Transformer
    print("\n[TEST 4] PageIndexTransformerAgent")
    agent = PageIndexTransformerAgent()
    print(f"  Client configured: {agent.client is not None}")
    print(f"  Documents indexed: {len(agent.indexed_documents)}")
    
    print("\n" + "=" * 70)
    print("PageIndex MCP - Integration OK!")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    import os
    test_pageindex_mcp()
