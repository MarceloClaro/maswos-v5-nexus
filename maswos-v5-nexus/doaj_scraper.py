#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - DOAJ (Directory of Open Access Journals) Official Scraper

API Documentation: https://doaj.org/api/v4/docs
- Base URL: https://doaj.org/api
- No API key required for read access
- Rate limit: Documented but generally generous for research use

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
class DOAJArticle:
    """Artigo do DOAJ"""
    id: str = ""
    title: str = ""
    abstract: str = ""
    authors: List[str] = field(default_factory=list)
    year: str = ""
    doi: str = ""
    journal_title: str = ""
    journal_issn: str = ""
    publisher: str = ""
    license: str = ""
    keywords: List[str] = field(default_factory=list)
    subject: List[str] = field(default_factory=list)
    language: str = ""
    url: str = ""
    full_text_url: str = ""
    source: str = "doaj"


class DOAJScraper:
    """
    Scraper oficial para DOAJ API
    
    Conforme documentação (https://doaj.org/api/v4/docs):
    - Base URL: https://doaj.org/api
    - Endpoints:
        - /search/articles/{query} - Buscar artigos
        - /search/journals/{query} - Buscar periódicos
        - /articles/{article_id} - Detalhes do artigo
        - /journals/{journal_id} - Detalhes do periódico
    
    Query syntax: Elasticsearch-like
        - term - busca simples
        - "phrase exacta" - frase exata
        - field:value - busca por campo
        - AND, OR, NOT - operadores booleanos
    """
    
    BASE_URL = "https://doaj.org/api"
    
    def __init__(self, delay: float = 0.5):
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "MASWOS-DOAJ/1.0",
            "Accept": "application/json"
        })
    
    def _rate_limit(self):
        """Rate limiting para não sobrecarregar o servidor"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def search_articles(self, query: str, page: int = 1, 
                        page_size: int = 25,
                        sort: str = "relevance") -> Dict:
        """
        Buscar artigos no DOAJ
        
        Args:
            query: Termo de busca (suporta sintaxe Elasticsearch)
            page: Página (paginação)
            page_size: Itens por página (máx: 100)
            sort: Ordenação (relevance, created_date, last_updated)
        
        Returns:
            Dict com artigos encontrados
        
        Query examples:
            - "machine learning" - busca frase exata
            - title:"deep learning" - busca no título
            - bibjson.year:2023 - por ano
            - subject:"Computer Science" - por assunto
            - doi:10.1234/... - por DOI
        """
        self._rate_limit()
        
        url = f"{self.BASE_URL}/v4/search/articles/{query}"
        
        params = {
            "page": page,
            "pageSize": min(page_size, 100)
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30, verify=False)
            
            if response.status_code == 200:
                return self._parse_search_response(response.json())
            else:
                print(f"[DOAJ] HTTP {response.status_code}: {response.text[:200]}")
                return {"articles": [], "total": 0, "source": "doaj_error"}
                
        except Exception as e:
            print(f"[DOAJ ERROR] {e}")
            return {"articles": [], "total": 0, "source": "doaj_exception"}
    
    def search_journals(self, query: str, page: int = 1,
                        page_size: int = 25) -> Dict:
        """
        Buscar periódicos no DOAJ
        
        Args:
            query: Termo de busca
            page: Página
            page_size: Itens por página
        
        Returns:
            Dict com periódicos encontrados
        """
        self._rate_limit()
        
        url = f"{self.BASE_URL}/v4/search/journals/{query}"
        
        params = {
            "page": page,
            "pageSize": min(page_size, 100)
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
                    "total": data.get("total", len(journals)),
                    "source": "doaj"
                }
            else:
                print(f"[DOAJ] HTTP {response.status_code}")
                return {"journals": [], "total": 0, "source": "doaj_error"}
                
        except Exception as e:
            print(f"[DOAJ ERROR] {e}")
            return {"journals": [], "total": 0, "source": "doaj_exception"}
    
    def get_article(self, article_id: str) -> Optional[Dict]:
        """
        Obter detalhes de um artigo
        
        Args:
            article_id: ID do artigo no DOAJ
        
        Returns:
            Dict com detalhes do artigo
        """
        self._rate_limit()
        
        url = f"{self.BASE_URL}/v4/articles/{article_id}"
        
        try:
            response = self.session.get(url, timeout=30, verify=False)
            
            if response.status_code == 200:
                return self._parse_article(response.json())
            else:
                print(f"[DOAJ] HTTP {response.status_code} para {article_id}")
                return None
                
        except Exception as e:
            print(f"[DOAJ ERROR] {e}")
            return None
    
    def get_journal(self, journal_id: str) -> Optional[Dict]:
        """
        Obter detalhes de um periódico
        
        Args:
            journal_id: ID do periódico no DOAJ
        
        Returns:
            Dict com detalhes do periódico
        """
        self._rate_limit()
        
        url = f"{self.BASE_URL}/v4/journals/{journal_id}"
        
        try:
            response = self.session.get(url, timeout=30, verify=False)
            
            if response.status_code == 200:
                return self._parse_journal(response.json())
            else:
                return None
                
        except Exception as e:
            print(f"[DOAJ ERROR] {e}")
            return None
    
    def _parse_search_response(self, data: Dict) -> Dict:
        """Parser para resposta de busca"""
        articles = []
        
        for item in data.get("results", []):
            article = self._parse_article(item)
            articles.append(article)
        
        return {
            "articles": articles,
            "total": data.get("total", len(articles)),
            "page": data.get("page", 1),
            "pageSize": data.get("pageSize", 25),
            "source": "doaj"
        }
    
    def _parse_article(self, item: Dict) -> Dict:
        """Parser para artigo"""
        bibjson = item.get("bibjson", {})
        
        # Extrair autores
        authors = []
        for author in bibjson.get("author", []):
            name = author.get("name", "")
            if name:
                authors.append(name)
        
        # Extrair identificadores
        identifiers = bibjson.get("identifier", [])
        doi = ""
        for ident in identifiers:
            if ident.get("type") == "doi":
                doi = ident.get("id", "")
                break
        
        # Extrair keywords
        keywords = bibjson.get("keywords", [])
        
        # Extrair subject
        subjects = []
        for subj in bibjson.get("subject", []):
            term = subj.get("term", "")
            if term:
                subjects.append(term)
        
        # Extrair licença
        license_info = ""
        licenses = bibjson.get("license", [])
        if licenses:
            license_info = licenses[0].get("title", "")
        
        # Extrair URL do texto completo
        full_text_url = ""
        link = bibjson.get("link", [])
        for l in link:
            if l.get("type") == "fulltext":
                full_text_url = l.get("url", "")
                break
        
        # Informações do periódico
        journal = bibjson.get("journal", {})
        
        return {
            "id": item.get("id", ""),
            "title": bibjson.get("title", ""),
            "abstract": bibjson.get("abstract", ""),
            "authors": authors,
            "year": bibjson.get("year", ""),
            "doi": doi,
            "journal_title": journal.get("title", ""),
            "journal_issn": journal.get("issn", [""])[0] if journal.get("issn") else "",
            "publisher": journal.get("publisher", ""),
            "license": license_info,
            "keywords": keywords,
            "subject": subjects,
            "language": ", ".join(bibjson.get("language", [])),
            "url": f"https://doaj.org/article/{item.get('id', '')}",
            "full_text_url": full_text_url,
            "source": "doaj"
        }
    
    def _parse_journal(self, item: Dict) -> Dict:
        """Parser para periódico"""
        bibjson = item.get("bibjson", {})
        
        return {
            "id": item.get("id", ""),
            "title": bibjson.get("title", ""),
            "publisher": bibjson.get("publisher", ""),
            "issn": bibjson.get("issn", [""])[0] if bibjson.get("issn") else "",
            "eissn": bibjson.get("eissn", [""])[0] if bibjson.get("eissn") else "",
            "language": ", ".join(bibjson.get("language", [])),
            "subject": [s.get("term", "") for s in bibjson.get("subject", [])],
            "license": bibjson.get("license", [{}])[0].get("title", "") if bibjson.get("license") else "",
            "url": f"https://doaj.org/journal/{item.get('id', '')}",
            "source": "doaj"
        }


# Funções de conveniência
def search_doaj(query: str, max_results: int = 25) -> List[Dict]:
    """Buscar artigos no DOAJ"""
    scraper = DOAJScraper()
    result = scraper.search_articles(query, page_size=max_results)
    return result.get("articles", [])

def get_doaj_article(article_id: str) -> Optional[Dict]:
    """Obter artigo específico"""
    scraper = DOAJScraper()
    return scraper.get_article(article_id)


# Testes
def test_doaj_scraper():
    """Testar scraper DOAJ"""
    print("=" * 70)
    print("MASWOS V5 NEXUS - DOAJ Scraper Test")
    print("=" * 70)
    
    scraper = DOAJScraper(delay=1.0)
    
    # Teste 1: Busca simples
    print("\n[TEST 1] Busca artigos: 'open access'")
    result = scraper.search_articles("open access", page_size=5)
    print(f"  Total encontrado: {result['total']}")
    print(f"  Fonte: {result['source']}")
    print(f"  Artigos recuperados: {len(result['articles'])}")
    
    for i, article in enumerate(result['articles'][:3], 1):
        print(f"\n  Artigo {i}:")
        print(f"    Título: {article.get('title', '')[:60]}...")
        print(f"    Periódico: {article.get('journal_title', '')}")
        print(f"    Autores: {', '.join(article.get('authors', [])[:2])}")
        print(f"    DOI: {article.get('doi', 'N/A')}")
    
    # Teste 2: Busca por título específico
    print("\n[TEST 2] Busca artigos: 'title:machine learning'")
    result = scraper.search_articles("title:machine learning", page_size=3)
    print(f"  Total encontrado: {result['total']}")
    
    # Teste 3: Buscar periódicos
    print("\n[TEST 3] Busca periódicos: 'computer science'")
    result = scraper.search_journals("computer science", page_size=3)
    print(f"  Total encontrado: {result['total']}")
    
    for journal in result.get('journals', [])[:2]:
        print(f"  - {journal.get('title', '')}: {journal.get('issn', 'N/A')}")
    
    print("\n" + "=" * 70)
    print("DOAJ Scraper - Testes Concluídos")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    test_doaj_scraper()
