#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - AMiner (Open Academic Graph) Official Scraper

API Documentation: https://open.aminer.cn/open/doc
- Base URL: https://datacenter.aminer.cn/gateway/open_platform
- API Token: https://open.aminer.cn/open/board?tab=control (free registration)
- Rate limit: Varies by endpoint (free tier available)

AMiner é uma das maiores plataformas acadêmicas da China com:
- 300M+ papers
- 160M+ scholars
- 600K+ venues

Inclui dados do Open Academic Graph (OAG) - unificação Microsoft Academic Graph + AMiner

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
class AMinerPaper:
    """Paper do AMiner"""
    id: str = ""
    title: str = ""
    abstract: str = ""
    authors: List[Dict] = field(default_factory=list)
    year: int = 0
    doi: str = ""
    venue: str = ""
    venue_id: str = ""
    keywords: List[str] = field(default_factory=list)
    citation_count: int = 0
    reference_count: int = 0
    fields_of_study: List[str] = field(default_factory=list)
    language: str = ""
    url: str = ""
    source: str = "aminer"


class AMinerScraper:
    """
    Scraper oficial para AMiner Open Platform API
    
    Conforme documentação (https://open.aminer.cn/open/doc):
    - Base URL: https://datacenter.aminer.cn/gateway/open_platform
    - Autenticação: Token via header X-TOKEN ou parameter token
    - APIs disponíveis:
        - POST /api/person/search - Buscar scholars (grátis)
        - GET /api/paper/search - Buscar papers (grátis)
        - GET /api/paper/search/pro - Buscar papers pro (¥0.01/req)
        - POST /api/patent/search - Buscar patentes (grátis)
        - POST /api/organization/search - Buscar organizações (grátis)
        - GET /api/paper/{paper_id} - Detalhes do paper (grátis)
        - POST /api/paper/qa/search - Q&A de papers (¥0.05/req)
    
    Registro de API token: https://open.aminer.cn/open/board?tab=control
    """
    
    BASE_URL = "https://datacenter.aminer.cn/gateway/open_platform"
    
    def __init__(self, api_token: Optional[str] = None, delay: float = 1.0):
        # API token from parameter or environment variable
        self.api_token = api_token or os.environ.get("AMINER_API_KEY")
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "MASWOS-AMiner/1.0",
            "Accept": "application/json",
            "Content-Type": "application/json"
        })
        
        if self.api_token:
            self.session.headers["X-TOKEN"] = self.api_token
    
    def _rate_limit(self):
        """Rate limiting para não sobrecarregar o servidor"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def is_available(self) -> bool:
        """Verificar se API token está configurado"""
        return bool(self.api_token)
    
    def search_papers(self, query: str, limit: int = 20, 
                      offset: int = 0,
                      year_from: Optional[int] = None,
                      year_to: Optional[int] = None,
                      fields_of_study: Optional[List[str]] = None) -> Dict:
        """
        Buscar papers no AMiner
        
        Args:
            query: Termo de busca
            limit: Número de resultados (máx: 100)
            offset: Offset para paginação
            year_from: Ano inicial
            year_to: Ano final
            fields_of_study: Campos de estudo (ex: ["Computer Science"])
        
        Returns:
            Dict com papers encontrados
        """
        self._rate_limit()
        
        url = f"{self.BASE_URL}/api/paper/search"
        
        params = {
            "query": query,
            "size": min(limit, 100),
            "page": offset // max(limit, 1) + 1 if limit > 0 else 1
        }
        
        if self.api_token:
            params["token"] = self.api_token
        
        try:
            response = self.session.get(url, params=params, timeout=30, verify=False)
            
            if response.status_code == 200:
                return self._parse_search_response(response.json())
            elif response.status_code == 401:
                print("[AMiner] Token inválido ou não configurado")
                return {"papers": [], "total": 0, "source": "aminer_auth_error"}
            elif response.status_code == 429:
                print("[AMiner] Rate limit atingido")
                return {"papers": [], "total": 0, "source": "aminer_rate_limit"}
            else:
                print(f"[AMiner] HTTP {response.status_code}: {response.text[:200]}")
                return {"papers": [], "total": 0, "source": "aminer_error"}
                
        except Exception as e:
            print(f"[AMiner ERROR] {e}")
            return {"papers": [], "total": 0, "source": "aminer_exception"}
    
    def search_papers_advanced(self, query: str, limit: int = 20,
                               offset: int = 0) -> Dict:
        """
        Busca avançada de papers (endpoint POST)
        
        Args:
            query: Termo de busca
            limit: Número de resultados
            offset: Offset
        
        Returns:
            Dict com papers encontrados
        """
        if not self.is_available():
            return {"papers": [], "total": 0, "source": "aminer_no_token"}
        
        self._rate_limit()
        
        url = f"{self.BASE_URL}/api/paper/search"
        
        payload = {
            "query": query,
            "size": min(limit, 100),
            "page": offset // max(limit, 1) + 1 if limit > 0 else 1
        }
        
        headers = {
            "X-TOKEN": self.api_token
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers, 
                                     timeout=30, verify=False)
            
            if response.status_code == 200:
                return self._parse_search_response(response.json())
            else:
                print(f"[AMiner] HTTP {response.status_code}")
                return {"papers": [], "total": 0, "source": "aminer_error"}
                
        except Exception as e:
            print(f"[AMiner ERROR] {e}")
            return {"papers": [], "total": 0, "source": "aminer_exception"}
    
    def get_paper(self, paper_id: str) -> Optional[Dict]:
        """
        Obter detalhes de um paper
        
        Args:
            paper_id: ID do paper no AMiner
        
        Returns:
            Dict com detalhes do paper
        """
        self._rate_limit()
        
        url = f"{self.BASE_URL}/api/paper/{paper_id}"
        
        params = {}
        if self.api_token:
            params["token"] = self.api_token
        
        try:
            response = self.session.get(url, params=params, timeout=30, verify=False)
            
            if response.status_code == 200:
                return self._parse_paper(response.json())
            else:
                return None
                
        except Exception as e:
            print(f"[AMiner ERROR] {e}")
            return None
    
    def search_scholars(self, query: str, limit: int = 20) -> Dict:
        """
        Buscar scholars (pesquisadores)
        
        Args:
            query: Nome ou termo de busca
            limit: Número de resultados
        
        Returns:
            Dict com scholars encontrados
        """
        if not self.is_available():
            return {"scholars": [], "total": 0, "source": "aminer_no_token"}
        
        self._rate_limit()
        
        url = f"{self.BASE_URL}/api/person/search"
        
        payload = {
            "query": query,
            "size": min(limit, 100)
        }
        
        headers = {
            "X-TOKEN": self.api_token,
            "Content-Type": "application/json"
        }
        
        try:
            response = requests.post(url, json=payload, headers=headers,
                                     timeout=30, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                scholars = []
                for item in data.get("data", []):
                    scholars.append(self._parse_scholar(item))
                
                return {
                    "scholars": scholars,
                    "total": data.get("total", len(scholars)),
                    "source": "aminer"
                }
            else:
                return {"scholars": [], "total": 0, "source": "aminer_error"}
                
        except Exception as e:
            print(f"[AMiner ERROR] {e}")
            return {"scholars": [], "total": 0, "source": "aminer_exception"}
    
    def _parse_search_response(self, data: Dict) -> Dict:
        """Parser para resposta de busca"""
        papers = []
        
        for item in data.get("data", []):
            paper = self._parse_paper(item)
            papers.append(paper)
        
        return {
            "papers": papers,
            "total": data.get("total", len(papers)),
            "source": "aminer"
        }
    
    def _parse_paper(self, item: Dict) -> Dict:
        """Parser para paper"""
        # Extrair autores
        authors = []
        for author in item.get("authors", []):
            if isinstance(author, dict):
                authors.append({
                    "name": author.get("name", ""),
                    "id": author.get("id", ""),
                    "org": author.get("org", ""),
                    "h_index": author.get("h_index", 0)
                })
            elif isinstance(author, str):
                authors.append({"name": author})
        
        return {
            "id": item.get("id", ""),
            "title": item.get("title", ""),
            "abstract": item.get("abstract", ""),
            "authors": authors,
            "year": item.get("year", 0),
            "doi": item.get("doi", ""),
            "venue": item.get("venue", "") if isinstance(item.get("venue"), str) else item.get("venue", {}).get("name", ""),
            "venue_id": item.get("venue_id", ""),
            "keywords": item.get("keywords", []),
            "citation_count": item.get("num_citation", 0),
            "reference_count": item.get("num_reference", 0),
            "fields_of_study": item.get("fields", []),
            "language": item.get("lang", ""),
            "url": f"https://www.aminer.org/pub/{item.get('id', '')}",
            "source": "aminer"
        }
    
    def _parse_scholar(self, item: Dict) -> Dict:
        """Parser para scholar"""
        return {
            "id": item.get("id", ""),
            "name": item.get("name", ""),
            "org": item.get("org", ""),
            "h_index": item.get("h_index", 0),
            "citation_count": item.get("num_citation", 0),
            "paper_count": item.get("num_paper", 0),
            "homepage": item.get("homepage", ""),
            "avatar": item.get("avatar", ""),
            "source": "aminer"
        }


# Funções de conveniência
def search_aminer(query: str, max_results: int = 20,
                  api_token: Optional[str] = None) -> List[Dict]:
    """Buscar papers no AMiner"""
    scraper = AMinerScraper(api_token=api_token)
    result = scraper.search_papers(query, limit=max_results)
    return result.get("papers", [])

def get_aminer_paper(paper_id: str, api_token: Optional[str] = None) -> Optional[Dict]:
    """Obter paper específico"""
    scraper = AMinerScraper(api_token=api_token)
    return scraper.get_paper(paper_id)


# Testes
def test_aminer_scraper():
    """Testar scraper AMiner"""
    print("=" * 70)
    print("MASWOS V5 NEXUS - AMiner Scraper Test")
    print("=" * 70)
    
    # Tentar carregar API token
    api_token = os.environ.get("AMINER_API_KEY")
    scraper = AMinerScraper(api_token=api_token, delay=1.0)
    
    if not scraper.is_available():
        print("\n[AVISO] AMINER_API_KEY não configurada")
        print("  Registre-se em: https://open.aminer.cn/open/board?tab=control")
        print("  Configure: export AMINER_API_KEY=seu_token")
        print("\n  Executando testes sem autenticação...")
    
    # Teste 1: Busca de papers
    print("\n[TEST 1] Busca papers: 'artificial intelligence'")
    result = scraper.search_papers("artificial intelligence", limit=5)
    print(f"  Total encontrado: {result['total']}")
    print(f"  Fonte: {result['source']}")
    
    if result.get('papers'):
        for i, paper in enumerate(result['papers'][:2], 1):
            print(f"\n  Paper {i}:")
            print(f"    Título: {paper.get('title', '')[:60]}...")
            print(f"    Autores: {', '.join([a.get('name', '') for a in paper.get('authors', [])[:2]])}")
            print(f"    Ano: {paper.get('year', 'N/A')}")
            print(f"    Citações: {paper.get('citation_count', 0)}")
    
    # Teste 2: Busca de scholars (requer token)
    if scraper.is_available():
        print("\n[TEST 2] Busca scholars: 'Yoshua Bengio'")
        result = scraper.search_scholars("Yoshua Bengio", limit=3)
        print(f"  Total encontrado: {result['total']}")
        
        for scholar in result.get('scholars', [])[:2]:
            print(f"  - {scholar.get('name', '')}: {scholar.get('h_index', 0)} h-index")
    
    print("\n" + "=" * 70)
    print("AMiner Scraper - Testes Concluídos")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    test_aminer_scraper()
