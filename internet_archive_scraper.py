#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - Internet Archive (Archive.org) Scraper

API Documentation: https://archive.readme.io/reference/getting-started
Base URL: https://archive.org/advancedsearch.php
Acesso: Gratuito, sem API key (mas autenticação aumenta rate limits)

Serviços disponíveis:
- Archive.org: 40+ milhões de itens (textos, livros, filmes, música, etc.)
- Wayback Machine: 800+ bilhões de páginas web arquivadas
- OpenLibrary: 20+ milhões de livros
- Books: 10+ milhões de livros digitalizados
- IIIF API: Imagens de alta resolução

Arquitetura: Transformer-Agentes (Encoder → API → Parser → Decoder)
"""

import requests
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from urllib.parse import quote, urlencode
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class InternetArchiveScraper:
    """
    Scraper para Internet Archive (Archive.org)
    
    Conforme documentação: https://archive.readme.io/reference/getting-started
    """
    
    SEARCH_URL = "https://archive.org/advancedsearch.php"
    METADATA_URL = "https://archive.org/metadata"
    WAYBACK_URL = "https://archive.org/wayback/available"
    CDX_URL = "https://web.archive.org/cdx/search/cdx"
    OPENLIBRARY_URL = "https://openlibrary.org/api"
    
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "MASWOS-InternetArchive/1.0",
            "Accept": "application/json"
        })
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    # ==================== ARCHIVE.ORG SEARCH ====================
    
    def search(self, query: str, rows: int = 50, page: int = 1,
               sort: str = "relevance", field: str = None,
               media_type: str = None) -> Dict:
        """
        Buscar itens no Archive.org
        
        Args:
            query: Termo de busca (suporta Lucene syntax)
            rows: Número de resultados (máx: 10000)
            page: Página
            sort: Ordenação (relevance, date, downloads)
            field: Campo específico (title, creator, date, etc.)
            media_type: Filtro por tipo (texts, movies, audio, image, software)
        """
        self._rate_limit()
        
        params = {
            "q": query,
            "output": "json",
            "rows": min(rows, 10000),
            "page": page,
            "sort[]": f"{sort} desc" if sort != "relevance" else sort
        }
        
        if field:
            params["fl[]"] = field
        else:
            params["fl[]"] = ["identifier", "title", "creator", "date", 
                              "description", "mediatype", "downloads"]
        
        if media_type:
            params["q"] += f" AND mediatype:{media_type}"
        
        try:
            response = self.session.get(self.SEARCH_URL, params=params, timeout=30)
            if response.status_code == 200:
                return self._parse_search_response(response.json())
        except Exception as e:
            print(f"[InternetArchive] Error: {e}")
        
        return {"items": [], "total": 0, "source": "internet_archive"}
    
    def search_books(self, query: str, limit: int = 20) -> Dict:
        """Buscar livros"""
        return self.search(query, rows=limit, media_type="texts")
    
    def search_audio(self, query: str, limit: int = 20) -> Dict:
        """Buscar áudio"""
        return self.search(query, rows=limit, media_type="audio")
    
    def search_videos(self, query: str, limit: int = 20) -> Dict:
        """Buscar vídeos"""
        return self.search(query, rows=limit, media_type="movies")
    
    def search_images(self, query: str, limit: int = 20) -> Dict:
        """Buscar imagens"""
        return self.search(query, rows=limit, media_type="image")
    
    def search_software(self, query: str, limit: int = 20) -> Dict:
        """Buscar software"""
        return self.search(query, rows=limit, media_type="software")
    
    # ==================== ITEM METADATA ====================
    
    def get_item_metadata(self, identifier: str) -> Optional[Dict]:
        """Obter metadados de um item"""
        self._rate_limit()
        url = f"{self.METADATA_URL}/{identifier}"
        
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"[InternetArchive] Error: {e}")
        
        return None
    
    def get_item_files(self, identifier: str) -> List[Dict]:
        """Obter lista de arquivos de um item"""
        self._rate_limit()
        url = f"{self.METADATA_URL}/{identifier}/files"
        
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"[InternetArchive] Error: {e}")
        
        return []
    
    def get_item_reviews(self, identifier: str) -> List[Dict]:
        """Obter reviews de um item"""
        self._rate_limit()
        url = f"{self.METADATA_URL}/{identifier}/reviews"
        
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"[InternetArchive] Error: {e}")
        
        return []
    
    # ==================== WAYBACK MACHINE ====================
    
    def get_wayback_snapshot(self, url: str, timestamp: str = None) -> Optional[Dict]:
        """
        Obter snapshot do Wayback Machine
        
        Args:
            url: URL para buscar
            timestamp: Data específica (YYYYMMDD) ou None para mais recente
        """
        self._rate_limit()
        
        params = {"url": url}
        if timestamp:
            params["timestamp"] = timestamp
        
        try:
            response = self.session.get(self.WAYBACK_URL, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"[Wayback] Error: {e}")
        
        return None
    
    def search_wayback_cdx(self, url: str, from_date: str = None,
                           to_date: str = None, limit: int = 100) -> List[Dict]:
        """
        Buscar no CDX Server (histórico completo de snapshots)
        
        Args:
            url: URL para buscar
            from_date: Data inicial (YYYYMMDD)
            to_date: Data final (YYYYMMDD)
            limit: Limite de resultados
        """
        self._rate_limit()
        
        params = {
            "url": url,
            "output": "json",
            "limit": limit
        }
        
        if from_date:
            params["from"] = from_date
        if to_date:
            params["to"] = to_date
        
        try:
            response = self.session.get(self.CDX_URL, params=params, timeout=60)
            if response.status_code == 200:
                data = response.json()
                if data and len(data) > 1:
                    # Primeira linha é o cabeçalho
                    headers = data[0]
                    results = []
                    for row in data[1:]:
                        results.append(dict(zip(headers, row)))
                    return results
        except Exception as e:
            print(f"[CDX] Error: {e}")
        
        return []
    
    # ==================== OPENLIBRARY ====================
    
    def search_openlibrary(self, query: str, limit: int = 20) -> List[Dict]:
        """Buscar no OpenLibrary"""
        self._rate_limit()
        url = f"{self.OPENLIBRARY_URL}/search.json"
        params = {"q": query, "limit": limit}
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data.get("docs", [])
        except Exception as e:
            print(f"[OpenLibrary] Error: {e}")
        
        return []
    
    def get_openlibrary_book(self, isbn: str = None, oclc: str = None,
                             lccn: str = None, olid: str = None) -> Optional[Dict]:
        """Obter detalhes de um livro do OpenLibrary"""
        self._rate_limit()
        
        if isbn:
            url = f"{self.OPENLIBRARY_URL}/books/ISBN/{isbn}.json"
        elif olid:
            url = f"{self.OPENLIBRARY_URL}/books/{olid}.json"
        else:
            return None
        
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"[OpenLibrary] Error: {e}")
        
        return None
    
    def get_openlibrary_author(self, author_key: str) -> Optional[Dict]:
        """Obter detalhes de um autor"""
        self._rate_limit()
        url = f"https://openlibrary.org/authors/{author_key}.json"
        
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"[OpenLibrary] Error: {e}")
        
        return None
    
    # ==================== BOOKS ====================
    
    def get_book_pages(self, identifier: str, page: int = 1) -> Dict:
        """Obter páginas de um livro"""
        self._rate_limit()
        url = f"https://archive.org/download/{identifier}"
        
        try:
            response = self.session.get(f"{url}/page/n{page}", timeout=30)
            if response.status_code == 200:
                return {"url": f"{url}/page/n{page}", "identifier": identifier}
        except Exception as e:
            print(f"[Books] Error: {e}")
        
        return {}
    
    def get_book_manifest(self, identifier: str) -> Optional[Dict]:
        """Obter manifest IIIF de um livro"""
        self._rate_limit()
        url = f"https://iiif.archivelab.org/iiif/{identifier}/manifest.json"
        
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"[IIIF] Error: {e}")
        
        return None
    
    def get_book_availability(self, oclc: str) -> Dict:
        """Verificar disponibilidade de empréstimo"""
        self._rate_limit()
        url = "https://archive.org/services/available.php"
        params = {"oclc": oclc}
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
        except Exception as e:
            print(f"[Availability] Error: {e}")
        
        return {}
    
    # ==================== HELPER METHODS ====================
    
    def _parse_search_response(self, data: Dict) -> Dict:
        """Parser para resposta de busca"""
        items = []
        response = data.get("response", {})
        
        for doc in response.get("docs", []):
            items.append({
                "identifier": doc.get("identifier", ""),
                "title": doc.get("title", [""])[0] if isinstance(doc.get("title"), list) else doc.get("title", ""),
                "creator": doc.get("creator", []),
                "date": doc.get("date", ""),
                "description": doc.get("description", ""),
                "mediatype": doc.get("mediatype", ""),
                "downloads": doc.get("downloads", 0),
                "url": f"https://archive.org/details/{doc.get('identifier', '')}",
                "source": "internet_archive"
            })
        
        return {
            "items": items,
            "total": response.get("numFound", 0),
            "source": "internet_archive"
        }


# ==================== FUNÇÕES DE CONVENIÊNCIA ====================

def search_archive(query: str, limit: int = 20, media_type: str = None) -> List[Dict]:
    """Buscar no Archive.org"""
    scraper = InternetArchiveScraper()
    result = scraper.search(query, rows=limit, media_type=media_type)
    return result.get("items", [])

def get_wayback_snapshot(url: str) -> Optional[Dict]:
    """Obter snapshot do Wayback"""
    scraper = InternetArchiveScraper()
    return scraper.get_wayback_snapshot(url)

def search_openlibrary(query: str, limit: int = 10) -> List[Dict]:
    """Buscar livros no OpenLibrary"""
    scraper = InternetArchiveScraper()
    return scraper.search_openlibrary(query, limit)


# ==================== TESTES ====================

def test_internet_archive():
    """Testar Internet Archive APIs"""
    print("=" * 70)
    print("MASWOS V5 NEXUS - Internet Archive Test")
    print("=" * 70)
    
    ia = InternetArchiveScraper()
    
    # Test 1: Busca geral
    print("\n[TEST 1] Busca: 'artificial intelligence'")
    result = ia.search("artificial intelligence", rows=5)
    print(f"  Total encontrado: {result['total']}")
    for item in result['items'][:3]:
        print(f"  - {item['title'][:50]}... ({item['mediatype']})")
    
    # Test 2: Busca livros
    print("\n[TEST 2] Busca livros: 'machine learning'")
    result = ia.search_books("machine learning", limit=5)
    print(f"  Total livros: {result['total']}")
    for item in result['items'][:3]:
        print(f"  - {item['title'][:50]}...")
    
    # Test 3: Wayback Machine
    print("\n[TEST 3] Wayback: 'google.com'")
    snapshot = ia.get_wayback_snapshot("google.com")
    if snapshot and "archived_snapshots" in snapshot:
        snap = snapshot["archived_snapshots"].get("closest", {})
        print(f"  Snapshot mais recente: {snap.get('timestamp', 'N/A')}")
        print(f"  URL: {snap.get('url', 'N/A')[:60]}...")
    
    # Test 4: CDX (histórico)
    print("\n[TEST 4] CDX History: 'ibge.gov.br' (2020-2023)")
    cdx = ia.search_wayback_cdx("ibge.gov.br", "2020", "2023", limit=5)
    print(f"  Snapshots encontrados: {len(cdx)}")
    for entry in cdx[:3]:
        print(f"  - {entry.get('timestamp', '')}: {entry.get('original', '')[:50]}...")
    
    # Test 5: OpenLibrary
    print("\n[TEST 5] OpenLibrary: 'python programming'")
    books = ia.search_openlibrary("python programming", limit=5)
    print(f"  Livros encontrados: {len(books)}")
    for book in books[:3]:
        print(f"  - {book.get('title', '')[:50]}...")
    
    # Test 6: Metadados de item
    print("\n[TEST 6] Item metadata: 'arxiv'")
    metadata = ia.get_item_metadata("arxiv")
    if metadata:
        print(f"  Título: {metadata.get('metadata', {}).get('title', 'N/A')}")
        print(f"  Tipo: {metadata.get('metadata', {}).get('mediatype', 'N/A')}")
    
    print("\n" + "=" * 70)
    print("Internet Archive - Testes Concluídos")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    test_internet_archive()
