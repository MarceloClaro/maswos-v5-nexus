#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - arXiv Official Scraper
Scraper baseado na API oficial do arXiv conforme documentação:
- https://info.arxiv.org/help/api/index.html
- https://info.arxiv.org/help/api/basics.html#python_simple_example

Endpoint: http://export.arxiv.org/api/query
Formato: Atom 1.0 (XML)
Rate Limit: 1 request / 3 segundos (sem API key)

Arquitetura: Transformer-Agentes (Encoder → API → Atom Parser → Decoder)
"""

import requests
import time
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime
import re
import urllib.parse
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Namespaces Atom
ATOM_NS = "http://www.w3.org/2005/Atom"
ARXIV_NS = "http://arxiv.org/schemas/atom"
OPENSEARCH_NS = "http://a9.com/-/spec/opensearch/1.1/"

@dataclass
class ArXivPaper:
    """Artigo arXiv padronizado"""
    arxiv_id: str = ""
    title: str = ""
    abstract: str = ""
    authors: List[str] = field(default_factory=list)
    categories: List[str] = field(default_factory=list)
    primary_category: str = ""
    published: str = ""
    updated: str = ""
    doi: str = ""
    journal_ref: str = ""
    comment: str = ""
    pdf_url: str = ""
    abs_url: str = ""
    version: str = ""
    source: str = "arXiv"


class ArXivOfficialScraper:
    """
    Scraper oficial para arXiv API
    
    Conforme documentação: https://info.arxiv.org/help/api/basics.html
    
    API Base: http://export.arxiv.org/api/query
    
    Rate Limiting (conforme TOU):
    - Sem API key: 1 request / 3 segundos
    - Recomendado: 3 segundos entre requests
    
    Query Syntax:
    - all:term - busca em todos os campos
    - ti:term - título
    - au:term - autor
    - abs:term - abstract
    - cat:category - categoria
    - AND, OR, ANDNOT - operadores lógicos
    """
    
    BASE_URL = "http://export.arxiv.org/api/query"
    
    def __init__(self, delay: float = 3.0):
        """
        Args:
            delay: Segundos entre requests (conforme guidelines: 3s mínimo)
        """
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "MASWOS-Scraper/1.0 (research; contact: research@maswos.ai)"
        })
    
    def _rate_limit(self):
        """Aplicar rate limiting conforme guidelines arXiv"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def search(self, query: str, start: int = 0, max_results: int = 10,
               sort_by: str = "relevance", sort_order: str = "descending",
               filter_list: Optional[List[str]] = None) -> Dict:
        """
        Buscar artigos no arXiv
        
        Conforme: https://info.arxiv.org/help/api/user-manual.html
        
        Args:
            query: Termo de busca (suporta sintaxe arXiv)
            start: Início da paginação (0-indexed)
            max_results: Máximo de resultados (máx: 30000)
            sort_by: Ordenar por (relevance, lastUpdatedDate, submittedDate)
            sort_order: Ordem (ascending, descending)
            filter_list: Filtro por categorias (ex: ['cs.AI', 'cs.LG'])
        
        Returns:
            Dict com papers encontrados e metadados
        """
        self._rate_limit()
        
        # Construir parâmetros
        params = {
            "search_query": query,
            "start": start,
            "max_results": min(max_results, 100),  # Limite por request
            "sortBy": sort_by,
            "sortOrder": sort_order
        }
        
        # Filtro por categorias
        if filter_list:
            category_query = " OR ".join([f"cat:{cat}" for cat in filter_list])
            params["search_query"] = f"({query}) AND ({category_query})"
        
        # Fazer request
        try:
            response = self.session.get(
                self.BASE_URL,
                params=params,
                timeout=30,
                verify=False
            )
            response.raise_for_status()
            
            # Parse Atom XML
            return self._parse_atom_response(response.text)
            
        except Exception as e:
            print(f"[arXiv ERROR] {e}")
            return {"papers": [], "total_results": 0, "error": str(e)}
    
    def search_by_id(self, arxiv_ids: List[str]) -> Dict:
        """
        Buscar artigos por IDs arXiv
        
        Args:
            arxiv_ids: Lista de IDs (ex: ['1603.01234', 'hep-th/9901001'])
        
        Returns:
            Dict com papers encontrados
        """
        self._rate_limit()
        
        # ID list pode ter até 8000 caracteres
        id_list = ",".join(arxiv_ids)
        
        params = {
            "id_list": id_list,
            "max_results": len(arxiv_ids)
        }
        
        try:
            response = self.session.get(
                self.BASE_URL,
                params=params,
                timeout=30,
                verify=False
            )
            response.raise_for_status()
            
            return self._parse_atom_response(response.text)
            
        except Exception as e:
            print(f"[arXiv ERROR] {e}")
            return {"papers": [], "total_results": 0, "error": str(e)}
    
    def search_by_author(self, author: str, max_results: int = 20) -> Dict:
        """Buscar por autor"""
        return self.search(f"au:{author}", max_results=max_results)
    
    def search_by_title(self, title: str, max_results: int = 20) -> Dict:
        """Buscar por título"""
        return self.search(f"ti:{title}", max_results=max_results)
    
    def search_by_category(self, category: str, max_results: int = 50) -> Dict:
        """Buscar por categoria"""
        return self.search(f"cat:{category}", max_results=max_results)
    
    def get_recent(self, category: str = "cs.AI", max_results: int = 20) -> Dict:
        """Obter artigos recentes de uma categoria"""
        return self.search(
            f"cat:{category}",
            sort_by="submittedDate",
            sort_order="descending",
            max_results=max_results
        )
    
    def get_pdf(self, arxiv_id: str) -> Optional[bytes]:
        """
        Baixar PDF do artigo
        
        Args:
            arxiv_id: ID do artigo (ex: '1603.01234')
        
        Returns:
            Bytes do PDF ou None
        """
        self._rate_limit()
        
        # Limpar ID
        clean_id = arxiv_id.replace("arxiv:", "").replace("http://arxiv.org/abs/", "")
        
        pdf_url = f"http://arxiv.org/pdf/{clean_id}"
        
        try:
            response = self.session.get(pdf_url, timeout=60, verify=False)
            response.raise_for_status()
            
            if response.headers.get("content-type", "").startswith("application/pdf"):
                return response.content
            else:
                print(f"[arXiv WARN] Resposta não é PDF: {response.headers.get('content-type')}")
                return None
                
        except Exception as e:
            print(f"[arXiv PDF ERROR] {e}")
            return None
    
    def _parse_atom_response(self, xml_text: str) -> Dict:
        """
        Parser para Atom 1.0 response
        
        Conforme formato descrito em:
        https://info.arxiv.org/help/api/user-manual.html#sample-input
        """
        papers = []
        
        try:
            root = ET.fromstring(xml_text)
            
            # Metadados do feed
            total_results = root.findtext(f"{{{OPENSEARCH_NS}}}totalResults", "0")
            start_index = root.findtext(f"{{{OPENSEARCH_NS}}}startIndex", "0")
            items_per_page = root.findtext(f"{{{OPENSEARCH_NS}}}itemsPerPage", "0")
            
            # Parse entries
            for entry in root.findall(f"{{{ATOM_NS}}}entry"):
                paper = self._parse_entry(entry)
                if paper.arxiv_id:
                    papers.append(paper)
            
            return {
                "papers": [self._paper_to_dict(p) for p in papers],
                "total_results": int(total_results),
                "start_index": int(start_index),
                "items_per_page": int(items_per_page),
                "source": "arXiv_API"
            }
            
        except Exception as e:
            print(f"[arXiv PARSE ERROR] {e}")
            return {"papers": [], "total_results": 0, "error": str(e)}
    
    def _parse_entry(self, entry) -> ArXivPaper:
        """Parser individual de entry Atom"""
        paper = ArXivPaper()
        
        # arXiv ID (do link ou id)
        paper_id = entry.findtext(f"{{{ATOM_NS}}}id", "")
        if paper_id:
            # Extrair ID limpo
            paper.arxiv_id = paper_id.split("/abs/")[-1] if "/abs/" in paper_id else paper_id
        
        # Título (remover newline extras)
        title = entry.findtext(f"{{{ATOM_NS}}}title", "")
        paper.title = " ".join(title.split()) if title else ""
        
        # Abstract
        abstract = entry.findtext(f"{{{ATOM_NS}}}summary", "")
        paper.abstract = " ".join(abstract.split()) if abstract else ""
        
        # Autores
        for author in entry.findall(f"{{{ATOM_NS}}}author"):
            name = author.findtext(f"{{{ATOM_NS}}}name", "")
            if name:
                paper.authors.append(name)
        
        # Categorias
        for category in entry.findall(f"{{{ATOM_NS}}}category"):
            term = category.get("term", "")
            if term:
                paper.categories.append(term)
        
        # Primary category
        primary = entry.find(f"{{{ARXIV_NS}}}primary_category")
        if primary is not None:
            paper.primary_category = primary.get("term", "")
        
        # Datas
        paper.published = entry.findtext(f"{{{ATOM_NS}}}published", "")
        paper.updated = entry.findtext(f"{{{ATOM_NS}}}updated", "")
        
        # Comment
        paper.comment = entry.findtext(f"{{{ARXIV_NS}}}comment", "")
        
        # Journal reference
        paper.journal_ref = entry.findtext(f"{{{ARXIV_NS}}}journal_ref", "")
        
        # DOI
        paper.doi = entry.findtext(f"{{{ARXIV_NS}}}doi", "")
        
        # Links
        for link in entry.findall(f"{{{ATOM_NS}}}link"):
            href = link.get("href", "")
            rel = link.get("rel", "")
            title = link.get("title", "")
            
            if rel == "alternate":
                paper.abs_url = href
            elif title == "pdf":
                paper.pdf_url = href
        
        # Versão
        if paper.arxiv_id and "v" in paper.arxiv_id:
            paper.version = paper.arxiv_id.split("v")[-1]
        
        return paper
    
    def _paper_to_dict(self, paper: ArXivPaper) -> Dict:
        """Converter paper para dict"""
        return {
            "arxiv_id": paper.arxiv_id,
            "title": paper.title,
            "abstract": paper.abstract,
            "authors": paper.authors,
            "categories": paper.categories,
            "primary_category": paper.primary_category,
            "published": paper.published,
            "updated": paper.updated,
            "doi": paper.doi,
            "journal_ref": paper.journal_ref,
            "comment": paper.comment,
            "pdf_url": paper.pdf_url,
            "abs_url": paper.abs_url,
            "version": paper.version,
            "source": paper.source
        }
    
    def build_query(self, title: str = None, author: str = None,
                    abstract: str = None, category: str = None,
                    operator: str = "AND") -> str:
        """
        Construir query arXiv
        
        Sintaxe suportada:
        - ti:título - título
        - au:autor - autor
        - abs:termo - abstract
        - cat:categoria - categoria
        - all:termo - todos os campos
        
        Operadores: AND, OR, ANDNOT
        """
        parts = []
        
        if title:
            parts.append(f"ti:{title}")
        if author:
            parts.append(f"au:{author}")
        if abstract:
            parts.append(f"abs:{abstract}")
        if category:
            parts.append(f"cat:{category}")
        
        return f" {operator} ".join(parts) if parts else ""


# Funções de conveniência
def search_arxiv(query: str, max_results: int = 20) -> List[Dict]:
    """Função simplificada para busca arXiv"""
    scraper = ArXivOfficialScraper()
    result = scraper.search(query, max_results=max_results)
    return result.get("papers", [])

def get_arxiv_by_id(arxiv_id: str) -> Optional[Dict]:
    """Obter artigo arXiv por ID"""
    scraper = ArXivOfficialScraper()
    result = scraper.search_by_id([arxiv_id])
    papers = result.get("papers", [])
    return papers[0] if papers else None

def get_recent_arxiv(category: str = "cs.AI", max_results: int = 10) -> List[Dict]:
    """Obter artigos recentes de uma categoria"""
    scraper = ArXivOfficialScraper()
    result = scraper.get_recent(category=category, max_results=max_results)
    return result.get("papers", [])


# Testes
def test_arxiv_official_scraper():
    """Testar scraper oficial arXiv"""
    print("=" * 70)
    print("MASWOS V5 NEXUS - arXiv Official Scraper Test")
    print("=" * 70)
    
    scraper = ArXivOfficialScraper(delay=3.0)
    
    # Teste 1: Busca simples
    print("\n[TEST 1] Busca simples: 'machine learning'")
    result = scraper.search("machine learning", max_results=3)
    print(f"  Total encontrado: {result['total_results']}")
    print(f"  Papers recuperados: {len(result['papers'])}")
    
    for i, paper in enumerate(result['papers'][:2], 1):
        print(f"\n  Paper {i}:")
        print(f"    ID: {paper['arxiv_id']}")
        print(f"    Título: {paper['title'][:60]}...")
        print(f"    Autores: {', '.join(paper['authors'][:2])}...")
        print(f"    Categoria: {paper['primary_category']}")
    
    # Teste 2: Busca por autor
    print("\n[TEST 2] Busca por autor: 'Yann LeCun'")
    result = scraper.search_by_author("Yann LeCun", max_results=2)
    print(f"  Total encontrado: {result['total_results']}")
    
    # Teste 3: Busca por categoria
    print("\n[TEST 3] Busca por categoria: 'cs.AI'")
    result = scraper.search_by_category("cs.AI", max_results=2)
    print(f"  Total encontrado: {result['total_results']}")
    
    # Teste 4: Artigos recentes
    print("\n[TEST 4] Artigos recentes em cs.LG")
    result = scraper.get_recent("cs.LG", max_results=2)
    print(f"  Papers recuperados: {len(result['papers'])}")
    
    # Teste 5: Query complexa
    print("\n[TEST 5] Query complexa: 'deep learning' AND 'neural network'")
    query = scraper.build_query(title="deep learning", abstract="neural network")
    print(f"  Query: {query}")
    result = scraper.search(query, max_results=2)
    print(f"  Total encontrado: {result['total_results']}")
    
    print("\n" + "=" * 70)
    print("arXiv Official Scraper - Testes Concluídos")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    test_arxiv_official_scraper()