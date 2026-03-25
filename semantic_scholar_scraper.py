#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - Semantic Scholar Official Scraper

API Documentation: https://api.semanticscholar.org/
- Base URL: https://api.semanticscholar.org/graph/v1
- No API key required for basic use (100 requests/5 min)
- API key optional for higher rate limits (1 request/sec with key)

Arquitetura: Transformer-Agentes (Encoder → API → Parser → Decoder)
"""

import requests
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@dataclass
class SemanticScholarPaper:
    """Paper do Semantic Scholar"""
    paper_id: str = ""
    title: str = ""
    abstract: str = ""
    authors: List[str] = field(default_factory=list)
    year: Optional[int] = None
    citation_count: int = 0
    reference_count: int = 0
    influential_citation_count: int = 0
    venue: str = ""
    journal: str = ""
    external_ids: Dict[str, str] = field(default_factory=dict)
    open_access_pdf: Optional[str] = None
    publication_types: List[str] = field(default_factory=list)
    fields_of_study: List[str] = field(default_factory=list)
    publication_date: str = ""
    url: str = ""
    source: str = "semanticscholar"


class SemanticScholarScraper:
    """
    Scraper oficial para Semantic Scholar API
    
    Conforme documentação:
    - Base URL: https://api.semanticscholar.org/graph/v1
    - Rate limit: 100 requests / 5 minutes (sem API key)
    - Rate limit: 1 request / segundo (com API key)
    
    Endpoints disponíveis:
    - /paper/search - Buscar papers
    - /paper/{paper_id} - Detalhes do paper
    - /paper/{paper_id}/citations - Citações
    - /paper/{paper_id}/references - Referências
    - /author/{author_id} - Detalhes do autor
    - /author/search - Buscar autores
    """
    
    BASE_URL = "https://api.semanticscholar.org/graph/v1"
    
    def __init__(self, api_key: Optional[str] = None, delay: float = 0.2):
        self.api_key = api_key
        self.delay = delay  # 0.2s = 5 req/s, 1.0s = 1 req/s with key
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "MASWOS-SemanticScholar/1.0",
            "Accept": "application/json"
        })
        
        if api_key:
            self.session.headers["x-api-key"] = api_key
            self.delay = 1.0  # Com API key, limitar para 1 req/s
    
    def _rate_limit(self):
        """Rate limiting para não sobrecarregar o servidor"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def search_papers(self, query: str, limit: int = 20, 
                      year: Optional[str] = None,
                      fields_of_study: Optional[List[str]] = None,
                      min_citation_count: Optional[int] = None,
                      open_access_only: bool = False,
                      sort: str = "relevance") -> Dict:
        """
        Buscar papers no Semantic Scholar
        
        Args:
            query: Termo de busca
            limit: Número máximo de resultados (máx: 100)
            year: Filtro de ano (ex: "2020-", "2020-2023")
            fields_of_study: Campos de estudo (ex: ["Computer Science", "Medicine"])
            min_citation_count: Mínimo de citações
            open_access_only: Apenas open access
            sort: Ordenação (relevance, citationCount, year)
        
        Returns:
            Dict com papers encontrados
        """
        self._rate_limit()
        
        url = f"{self.BASE_URL}/paper/search"
        
        fields = [
            "paperId", "title", "abstract", "authors", "year",
            "citationCount", "referenceCount", "influentialCitationCount",
            "venue", "journal", "externalIds", "openAccessPdf",
            "publicationTypes", "fieldsOfStudy", "publicationDate", "url"
        ]
        
        params = {
            "query": query,
            "limit": min(limit, 100),
            "fields": ",".join(fields)
        }
        
        if year:
            params["year"] = year
        if fields_of_study:
            params["fieldsOfStudy"] = ",".join(fields_of_study)
        if min_citation_count is not None:
            params["minCitationCount"] = min_citation_count
        if open_access_only:
            params["openAccessPdf"] = ""
        if sort:
            params["sort"] = sort
        
        try:
            response = self.session.get(url, params=params, timeout=30, verify=False)
            
            if response.status_code == 200:
                return self._parse_search_response(response.json())
            elif response.status_code == 429:
                print(f"[SemanticScholar] Rate limit atingido. Aguardando...")
                time.sleep(60)
                return {"papers": [], "total": 0, "source": "semanticscholar_rate_limit"}
            else:
                print(f"[SemanticScholar] HTTP {response.status_code}: {response.text[:200]}")
                return {"papers": [], "total": 0, "source": "semanticscholar_error"}
                
        except Exception as e:
            print(f"[SemanticScholar ERROR] {e}")
            return {"papers": [], "total": 0, "source": "semanticscholar_exception"}
    
    def get_paper(self, paper_id: str, 
                  id_type: str = "paper_id") -> Optional[Dict]:
        """
        Obter detalhes de um paper específico
        
        Args:
            paper_id: ID do paper (paper_id, DOI, arXiv ID, etc.)
            id_type: Tipo de ID (paper_id, DOI, arXiv, MAG, etc.)
        
        Returns:
            Dict com detalhes do paper
        """
        self._rate_limit()
        
        # Determinar endpoint baseado no tipo de ID
        if id_type == "DOI":
            endpoint = f"{self.BASE_URL}/paper/DOI:{paper_id}"
        elif id_type == "arXiv":
            endpoint = f"{self.BASE_URL}/paper/ARXIV:{paper_id}"
        elif id_type == "MAG":
            endpoint = f"{self.BASE_URL}/paper/MAG:{paper_id}"
        else:
            endpoint = f"{self.BASE_URL}/paper/{paper_id}"
        
        fields = [
            "paperId", "title", "abstract", "authors", "year",
            "citationCount", "referenceCount", "influentialCitationCount",
            "venue", "journal", "externalIds", "openAccessPdf",
            "publicationTypes", "fieldsOfStudy", "publicationDate", "url",
            "tldr", "citationStyles"
        ]
        
        params = {"fields": ",".join(fields)}
        
        try:
            response = self.session.get(endpoint, params=params, timeout=30, verify=False)
            
            if response.status_code == 200:
                return self._parse_paper(response.json())
            else:
                print(f"[SemanticScholar] HTTP {response.status_code} para {paper_id}")
                return None
                
        except Exception as e:
            print(f"[SemanticScholar ERROR] {e}")
            return None
    
    def get_citations(self, paper_id: str, limit: int = 100) -> List[Dict]:
        """
        Obter citações de um paper
        
        Args:
            paper_id: ID do paper
            limit: Número máximo de citações
        
        Returns:
            Lista de citações
        """
        self._rate_limit()
        
        url = f"{self.BASE_URL}/paper/{paper_id}/citations"
        
        fields = ["paperId", "title", "year", "citationCount", "authors", "venue"]
        params = {
            "fields": ",".join(fields),
            "limit": min(limit, 1000)
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                citations = []
                for item in data.get("data", []):
                    if "citingPaper" in item:
                        citations.append(self._parse_paper(item["citingPaper"]))
                return citations
            else:
                return []
                
        except Exception as e:
            print(f"[SemanticScholar Citations ERROR] {e}")
            return []
    
    def get_references(self, paper_id: str, limit: int = 100) -> List[Dict]:
        """
        Obter referências de um paper
        
        Args:
            paper_id: ID do paper
            limit: Número máximo de referências
        
        Returns:
            Lista de referências
        """
        self._rate_limit()
        
        url = f"{self.BASE_URL}/paper/{paper_id}/references"
        
        fields = ["paperId", "title", "year", "citationCount", "authors", "venue"]
        params = {
            "fields": ",".join(fields),
            "limit": min(limit, 1000)
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                references = []
                for item in data.get("data", []):
                    if "citedPaper" in item:
                        references.append(self._parse_paper(item["citedPaper"]))
                return references
            else:
                return []
                
        except Exception as e:
            print(f"[SemanticScholar References ERROR] {e}")
            return []
    
    def search_authors(self, query: str, limit: int = 20) -> List[Dict]:
        """
        Buscar autores
        
        Args:
            query: Nome do autor
            limit: Número máximo de resultados
        
        Returns:
            Lista de autores
        """
        self._rate_limit()
        
        url = f"{self.BASE_URL}/author/search"
        
        fields = ["authorId", "name", "affiliations", "paperCount", 
                  "citationCount", "hIndex", "homepage"]
        params = {
            "query": query,
            "limit": min(limit, 100),
            "fields": ",".join(fields)
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                authors = []
                for author in data.get("data", []):
                    authors.append({
                        "author_id": author.get("authorId", ""),
                        "name": author.get("name", ""),
                        "affiliations": author.get("affiliations", []),
                        "paper_count": author.get("paperCount", 0),
                        "citation_count": author.get("citationCount", 0),
                        "h_index": author.get("hIndex", 0),
                        "homepage": author.get("homepage", ""),
                        "url": f"https://www.semanticscholar.org/author/{author.get('authorId', '')}"
                    })
                return authors
            else:
                return []
                
        except Exception as e:
            print(f"[SemanticScholar Authors ERROR] {e}")
            return []
    
    def _parse_search_response(self, data: Dict) -> Dict:
        """Parser para resposta de busca"""
        papers = []
        
        for item in data.get("data", []):
            paper = self._parse_paper(item)
            papers.append(paper)
        
        return {
            "papers": papers,
            "total": data.get("total", len(papers)),
            "source": "semanticscholar",
            "next": data.get("next", None)
        }
    
    def _parse_paper(self, item: Dict) -> Dict:
        """Parser para paper"""
        # Extrair autores
        authors = []
        for author in item.get("authors", []):
            authors.append(author.get("name", ""))
        
        # Extrair IDs externos
        external_ids = item.get("externalIds", {}) or {}
        
        # Extrair PDF open access
        open_access_pdf = None
        if item.get("openAccessPdf"):
            open_access_pdf = item["openAccessPdf"].get("url")
        
        return {
            "paper_id": item.get("paperId", ""),
            "title": item.get("title", ""),
            "abstract": item.get("abstract", ""),
            "authors": authors,
            "year": item.get("year"),
            "citation_count": item.get("citationCount", 0),
            "reference_count": item.get("referenceCount", 0),
            "influential_citation_count": item.get("influentialCitationCount", 0),
            "venue": item.get("venue", ""),
            "journal": item.get("journal", {}).get("name", "") if isinstance(item.get("journal"), dict) else str(item.get("journal", "")),
            "external_ids": external_ids,
            "doi": external_ids.get("DOI", ""),
            "arxiv_id": external_ids.get("ArXiv", ""),
            "pmid": external_ids.get("PubMed", ""),
            "open_access_pdf": open_access_pdf,
            "publication_types": item.get("publicationTypes", []),
            "fields_of_study": item.get("fieldsOfStudy", []),
            "publication_date": item.get("publicationDate", ""),
            "url": item.get("url", f"https://www.semanticscholar.org/paper/{item.get('paperId', '')}"),
            "source": "semanticscholar"
        }


# Funções de conveniência
def search_semantic_scholar(query: str, max_results: int = 20, 
                            api_key: Optional[str] = None) -> List[Dict]:
    """Buscar papers no Semantic Scholar"""
    scraper = SemanticScholarScraper(api_key=api_key)
    result = scraper.search_papers(query, limit=max_results)
    return result.get("papers", [])

def get_semantic_scholar_paper(paper_id: str, api_key: Optional[str] = None) -> Optional[Dict]:
    """Obter paper específico"""
    scraper = SemanticScholarScraper(api_key=api_key)
    return scraper.get_paper(paper_id)


# Testes
def test_semantic_scholar_scraper():
    """Testar scraper Semantic Scholar"""
    print("=" * 70)
    print("MASWOS V5 NEXUS - Semantic Scholar Scraper Test")
    print("=" * 70)
    
    scraper = SemanticScholarScraper(delay=1.0)
    
    # Teste 1: Busca simples
    print("\n[TEST 1] Busca: 'transformer neural network'")
    result = scraper.search_papers("transformer neural network", limit=5)
    print(f"  Total encontrado: {result['total']}")
    print(f"  Fonte: {result['source']}")
    print(f"  Papers recuperados: {len(result['papers'])}")
    
    for i, paper in enumerate(result['papers'][:3], 1):
        print(f"\n  Paper {i}:")
        print(f"    ID: {paper.get('paper_id', '')[:20]}...")
        print(f"    Título: {paper.get('title', '')[:60]}...")
        print(f"    Autores: {', '.join(paper.get('authors', [])[:3])}")
        print(f"    Ano: {paper.get('year', 'N/A')}")
        print(f"    Citações: {paper.get('citation_count', 0)}")
    
    # Teste 2: Busca com filtro de ano
    print("\n[TEST 2] Busca com filtro: 'deep learning' (2023-)")
    result = scraper.search_papers("deep learning", limit=3, year="2023-")
    print(f"  Total encontrado: {result['total']}")
    
    # Teste 3: Busca com filtro de citações
    print("\n[TEST 3] Busca: 'cancer' (mín 100 citações)")
    result = scraper.search_papers("cancer", limit=3, min_citation_count=100)
    print(f"  Total encontrado: {result['total']}")
    
    # Teste 4: Buscar autores
    print("\n[TEST 4] Buscar autor: 'Geoffrey Hinton'")
    authors = scraper.search_authors("Geoffrey Hinton", limit=3)
    for author in authors[:2]:
        print(f"  - {author['name']}: {author['citation_count']} citações, h-index: {author['h_index']}")
    
    print("\n" + "=" * 70)
    print("Semantic Scholar Scraper - Testes Concluídos")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    test_semantic_scholar_scraper()
