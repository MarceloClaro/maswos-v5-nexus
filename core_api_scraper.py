#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - CORE API Official Scraper

API Documentation: https://api.core.ac.uk/docs/v3
- Base URL: https://api.core.ac.uk/v3
- API Key Required (free registration): https://core.ac.uk/services/api
- Rate limit: 1 request/10s (search), 10 requests/10s (article get)

Largest aggregator of open access research papers (300M+ papers)

Arquitetura: Transformer-Agentes (Encoder → API → Parser → Decoder)
"""

import requests
import time
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@dataclass
class COREArticle:
    """Artigo do CORE"""
    core_id: str = ""
    title: str = ""
    abstract: str = ""
    authors: List[str] = field(default_factory=list)
    year: Optional[int] = None
    doi: str = ""
    citations: int = 0
    downloadUrl: str = ""
    repositoryName: str = ""
    repositoryId: int = 0
    fullText: str = ""
    language: str = ""
    publisher: str = ""
    subjects: List[str] = field(default_factory=list)
    urls: List[str] = field(default_factory=list)
    identifiers: List[str] = field(default_factory=list)
    source: str = "core"


class COREScraper:
    """
    Scraper oficial para CORE API v3
    
    Conforme documentação (https://api.core.ac.uk/docs/v3):
    - Base URL: https://api.core.ac.uk/v3
    - Autenticação: Bearer token (API key)
    - Rate limits:
        - /search: 1 request / 10 segundos
        - /search/{query}: 5 requests / 10 segundos
        - /articles/get: 1 request / 10 segundos
        - /articles/get/{id}: 10 requests / 10 segundos
    
    Registro de API key: https://core.ac.uk/services/api
    
    Endpoints:
    - /search - Busca geral (papers, datasets, journals)
    - /search/works - Busca específica em works
    - /articles/get/{coreId} - Detalhes do artigo
    - /journals/search - Busca de periódicos
    - /journals/get/{issn} - Detalhes do periódico
    - /repositories/get/{repoId} - Detalhes do repositório
    """
    
    BASE_URL = "https://api.core.ac.uk/v3"
    
    def __init__(self, api_key: Optional[str] = None, delay: float = 10.0):
        # API key from parameter or environment variable
        self.api_key = api_key or os.environ.get("CORE_API_KEY")
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "MASWOS-CORE/1.0",
            "Accept": "application/json"
        })
        
        if self.api_key:
            self.session.headers["Authorization"] = f"Bearer {self.api_key}"
    
    def _rate_limit(self):
        """Rate limiting para não sobrecarregar o servidor"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def is_available(self) -> bool:
        """Verificar se API key está configurada"""
        return bool(self.api_key)
    
    def search_works(self, query: str, limit: int = 20, 
                     offset: int = 0,
                     full_text: bool = False,
                     sort: str = "relevance") -> Dict:
        """
        Buscar works (artigos) no CORE
        
        Args:
            query: Query de busca (suporta sintaxe especial)
            limit: Número de resultados (máx: 100)
            offset: Offset para paginação
            full_text: Apenas artigos com texto completo
            sort: Ordenação (relevance, cited_by_count, date_published)
        
        Returns:
            Dict com artigos encontrados
        
        Query syntax:
            - title:"query" - busca no título
            - abstract:"query" - busca no abstract
            - fullText:"query" - busca no texto completo
            - year>=2020 - filtro por ano
            - _exists_:fullText - artigos com full text
        """
        if not self.is_available():
            return {"articles": [], "total": 0, "source": "core_no_api_key"}
        
        self._rate_limit()
        
        url = f"{self.BASE_URL}/search/works"
        
        params = {
            "q": query,
            "limit": min(limit, 100),
            "offset": offset
        }
        
        if full_text:
            params["q"] = f"({query}) AND _exists_:fullText"
        
        try:
            response = self.session.get(url, params=params, timeout=30, verify=False)
            
            if response.status_code == 200:
                return self._parse_search_response(response.json())
            elif response.status_code == 401:
                print(f"[CORE] API key inválida ou não configurada")
                return {"articles": [], "total": 0, "source": "core_auth_error"}
            elif response.status_code == 429:
                print(f"[CORE] Rate limit atingido. Aguardando...")
                time.sleep(30)
                return {"articles": [], "total": 0, "source": "core_rate_limit"}
            else:
                print(f"[CORE] HTTP {response.status_code}: {response.text[:200]}")
                return {"articles": [], "total": 0, "source": "core_error"}
                
        except Exception as e:
            print(f"[CORE ERROR] {e}")
            return {"articles": [], "total": 0, "source": "core_exception"}
    
    def get_article(self, core_id: str) -> Optional[Dict]:
        """
        Obter detalhes de um artigo pelo CORE ID
        
        Args:
            core_id: ID do artigo no CORE
        
        Returns:
            Dict com detalhes do artigo
        """
        if not self.is_available():
            return None
        
        self._rate_limit()
        
        url = f"{self.BASE_URL}/articles/get/{core_id}"
        
        try:
            response = self.session.get(url, timeout=30, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                return self._parse_article(data)
            else:
                print(f"[CORE] HTTP {response.status_code} para {core_id}")
                return None
                
        except Exception as e:
            print(f"[CORE ERROR] {e}")
            return None
    
    def search_journals(self, query: str, limit: int = 20) -> Dict:
        """
        Buscar periódicos no CORE
        
        Args:
            query: Termo de busca
            limit: Número de resultados
        
        Returns:
            Dict com periódicos encontrados
        """
        if not self.is_available():
            return {"journals": [], "total": 0, "source": "core_no_api_key"}
        
        self._rate_limit()
        
        url = f"{self.BASE_URL}/journals/search"
        
        params = {
            "q": query,
            "limit": min(limit, 100)
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                journals = []
                for item in data.get("results", []):
                    journals.append(self._parse_journal(item))
                
                return {
                    "journals": journals,
                    "total": data.get("totalHits", len(journals)),
                    "source": "core"
                }
            else:
                return {"journals": [], "total": 0, "source": "core_error"}
                
        except Exception as e:
            print(f"[CORE ERROR] {e}")
            return {"journals": [], "total": 0, "source": "core_exception"}
    
    def get_repositories(self, limit: int = 20) -> Dict:
        """
        Listar repositórios no CORE
        
        Args:
            limit: Número de repositórios
        
        Returns:
            Dict com repositórios
        """
        if not self.is_available():
            return {"repositories": [], "total": 0, "source": "core_no_api_key"}
        
        self._rate_limit()
        
        url = f"{self.BASE_URL}/repositories/get"
        
        params = {"limit": min(limit, 100)}
        
        try:
            response = self.session.get(url, params=params, timeout=30, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                return {
                    "repositories": data.get("results", []),
                    "total": data.get("totalHits", 0),
                    "source": "core"
                }
            else:
                return {"repositories": [], "total": 0, "source": "core_error"}
                
        except Exception as e:
            print(f"[CORE ERROR] {e}")
            return {"repositories": [], "total": 0, "source": "core_exception"}
    
    def _parse_search_response(self, data: Dict) -> Dict:
        """Parser para resposta de busca"""
        articles = []
        
        for item in data.get("results", []):
            article = self._parse_article(item)
            articles.append(article)
        
        return {
            "articles": articles,
            "total": data.get("totalHits", len(articles)),
            "source": "core"
        }
    
    def _parse_article(self, item: Dict) -> Dict:
        """Parser para artigo"""
        # Extrair autores
        authors = []
        for author in item.get("authors", []):
            if isinstance(author, str):
                authors.append(author)
            elif isinstance(author, dict):
                authors.append(author.get("name", ""))
        
        # Extrair DOI
        doi = ""
        identifiers = item.get("identifiers", [])
        for ident in identifiers:
            if "doi.org" in ident or ident.startswith("10."):
                doi = ident.replace("https://doi.org/", "").replace("http://doi.org/", "")
                break
        
        return {
            "core_id": str(item.get("id", "")),
            "title": item.get("title", ""),
            "abstract": item.get("abstract", ""),
            "authors": authors,
            "year": item.get("yearPublished"),
            "doi": doi,
            "citations": item.get("citationCount", 0),
            "downloadUrl": item.get("downloadUrl", ""),
            "repositoryName": item.get("repositoryName", ""),
            "repositoryId": item.get("repositoryId", 0),
            "fullText": item.get("fullText", "")[:500] if item.get("fullText") else "",
            "language": item.get("language", ""),
            "publisher": item.get("publisher", ""),
            "subjects": item.get("subjects", []),
            "urls": item.get("urls", []),
            "identifiers": identifiers,
            "source": "core"
        }
    
    def _parse_journal(self, item: Dict) -> Dict:
        """Parser para periódico"""
        return {
            "core_id": str(item.get("id", "")),
            "title": item.get("title", ""),
            "issn": item.get("issn", ""),
            "publisher": item.get("publisher", ""),
            "language": item.get("language", ""),
            "subjects": item.get("subjects", []),
            "source": "core"
        }


# Funções de conveniência
def search_core(query: str, max_results: int = 20, 
                api_key: Optional[str] = None) -> List[Dict]:
    """Buscar artigos no CORE"""
    scraper = COREScraper(api_key=api_key)
    result = scraper.search_works(query, limit=max_results)
    return result.get("articles", [])

def get_core_article(core_id: str, api_key: Optional[str] = None) -> Optional[Dict]:
    """Obter artigo específico"""
    scraper = COREScraper(api_key=api_key)
    return scraper.get_article(core_id)


# Testes
def test_core_scraper():
    """Testar scraper CORE"""
    print("=" * 70)
    print("MASWOS V5 NEXUS - CORE API Scraper Test")
    print("=" * 70)
    
    # Tentar carregar API key
    api_key = os.environ.get("CORE_API_KEY")
    scraper = COREScraper(api_key=api_key, delay=10.0)
    
    if not scraper.is_available():
        print("\n[AVISO] CORE_API_KEY não configurada")
        print("  Registre-se em: https://core.ac.uk/services/api")
        print("  Configure: export CORE_API_KEY=sua_api_key")
        print("\n  Executando testes limitados...")
    
    # Teste 1: Busca simples
    print("\n[TEST 1] Busca: 'machine learning'")
    result = scraper.search_works("machine learning", limit=5)
    print(f"  Total encontrado: {result['total']}")
    print(f"  Fonte: {result['source']}")
    
    if result.get('articles'):
        for i, article in enumerate(result['articles'][:2], 1):
            print(f"\n  Artigo {i}:")
            print(f"    CORE ID: {article.get('core_id', '')}")
            print(f"    Título: {article.get('title', '')[:60]}...")
            print(f"    Repositório: {article.get('repositoryName', '')}")
    
    # Teste 2: Busca com filtro de full text
    print("\n[TEST 2] Busca com full text: 'cancer'")
    result = scraper.search_works("cancer", limit=3, full_text=True)
    print(f"  Total encontrado: {result['total']}")
    
    print("\n" + "=" * 70)
    print("CORE API Scraper - Testes Concluídos")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    test_core_scraper()
