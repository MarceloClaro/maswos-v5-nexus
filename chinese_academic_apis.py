#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - Chinese Academic APIs Comprehensive Scraper

APIs Gratuitas para Pesquisa Acadêmica Chinesa:

1. AMiner/Open Academic Graph - https://open.aminer.cn/open/doc
2. OpenReview - https://openreview.net (API: https://api2.openreview.net)
3. SciEngine - https://www.sciengine.com/ (OA journals da Science Press China)
4. OpenAlex - https://api.openalex.org (inclui dados chineses)
5. CNKI - https://kns.cnki.net (web scraping limitado)
6. National Science Library (NSTL) - https://www.nstl.gov.cn
7. CSTPCD (China Science and Technology Paper Citation Database)

APIs Paginas (requerem parceria institucional):
- CNKI API: https://db.cnki.net
- Wanfang: https://www.wanfangdata.com.cn
- CQVIP: https://www.cqvip.com

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
from urllib.parse import quote, urlencode
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class OpenReviewScraper:
    """
    Scraper para OpenReview API
    
    API Documentation: https://docs.openreview.net/
    Base URL: https://api2.openreview.net
    Acesso: Gratuito, sem API key para leitura
    
    Conferências disponíveis:
    - ICLR (International Conference on Learning Representations)
    - NeurIPS (Neural Information Processing Systems)
    - ICML (International Conference on Machine Learning)
    - AAAI, ACL, EMNLP, CVPR, ICCV, ECCV, etc.
    """
    
    BASE_URL = "https://api2.openreview.net"
    
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "MASWOS-OpenReview/1.0",
            "Accept": "application/json"
        })
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def get_venues(self, limit: int = 100) -> List[Dict]:
        """Obter lista de conferências/jornais"""
        self._rate_limit()
        url = f"{self.BASE_URL}/api/groups"
        params = {"limit": limit, "prefix": "ICLR", "domain": "openreview.net"}
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data.get("content", {}).get("groups", [])
        except Exception as e:
            print(f"[OpenReview] Error: {e}")
        
        return []
    
    def get_submissions(self, venue_id: str, limit: int = 100,
                        status: str = "active") -> List[Dict]:
        """Obter submissões de uma conferência"""
        self._rate_limit()
        url = f"{self.BASE_URL}/api/notes"
        params = {
            "content.venue": venue_id,
            "details": "original",
            "limit": limit
        }
        
        try:
            response = self.session.get(url, params=params, timeout=60)
            if response.status_code == 200:
                data = response.json()
                notes = data.get("notes", [])
                return [self._parse_submission(n) for n in notes]
        except Exception as e:
            print(f"[OpenReview] Error: {e}")
        
        return []
    
    def search_submissions(self, venue_id: str, query: str,
                           field: str = "title") -> List[Dict]:
        """Buscar submissões por texto"""
        submissions = self.get_submissions(venue_id, limit=500)
        results = []
        query_lower = query.lower()
        
        for sub in submissions:
            if field == "title" and query_lower in sub.get("title", "").lower():
                results.append(sub)
            elif field == "abstract" and query_lower in sub.get("abstract", "").lower():
                results.append(sub)
            elif field == "all":
                if (query_lower in sub.get("title", "").lower() or
                    query_lower in sub.get("abstract", "").lower()):
                    results.append(sub)
        
        return results
    
    def get_paper_details(self, note_id: str) -> Optional[Dict]:
        """Obter detalhes de um paper"""
        self._rate_limit()
        url = f"{self.BASE_URL}/api/notes/{note_id}"
        
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                return self._parse_submission(response.json())
        except Exception as e:
            print(f"[OpenReview] Error: {e}")
        
        return None
    
    def _parse_submission(self, note: Dict) -> Dict:
        """Parser para submissão"""
        content = note.get("content", {})
        
        # Extrair autores
        authors = content.get("authors", {})
        if isinstance(authors, dict):
            authors = authors.get("value", [])
        
        # Extrair título
        title = content.get("title", {})
        if isinstance(title, dict):
            title = title.get("value", "")
        
        # Extrair abstract
        abstract = content.get("abstract", {})
        if isinstance(abstract, dict):
            abstract = abstract.get("value", "")
        
        return {
            "id": note.get("id", ""),
            "title": title,
            "abstract": abstract,
            "authors": authors,
            "venue": note.get("content", {}).get("venue", ""),
            "url": f"https://openreview.net/forum?id={note.get('id', '')}",
            "pdf_url": f"https://openreview.net/pdf?id={note.get('id', '')}",
            "venueid": note.get("content", {}).get("venueid", ""),
            "source": "openreview"
        }


class SciEngineScraper:
    """
    Scraper para SciEngine (中国科技期刊)
    
    API Documentation: https://www.sciengine.com/
    Base URL: https://www.sciengine.com/
    Acesso: Alguns journals são Open Access
    
    Publisher: Science Press (科学出版社) - China
    Journals: 200+ journals em ciências, engenharia, medicina
    """
    
    BASE_URL = "https://www.sciengine.com"
    
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "MASWOS-SciEngine/1.0",
            "Accept": "text/html,application/json"
        })
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def search_journals(self) -> List[Dict]:
        """Listar journals OA disponíveis"""
        # SciEngine não tem API pública, web scraping necessário
        journals = [
            {"name": "Acta Mathematica Scientia", "issn": "0252-9602", "oa": True},
            {"name": "Acta Mathematicae Applicatae Sinica", "issn": "0162-0908", "oa": True},
            {"name": "Chinese Annals of Mathematics", "issn": "0252-9599", "oa": True},
            {"name": "Science China Mathematics", "issn": "1674-7283", "oa": True},
            {"name": "Science China Chemistry", "issn": "1674-7291", "oa": True},
            {"name": "Science China Physics", "issn": "1674-7348", "oa": True},
            {"name": "Science China Life Sciences", "issn": "1674-7305", "oa": True},
        ]
        return journals


class OpenAlexChinaScraper:
    """
    Scraper para OpenAPI com foco em papers chineses
    
    API Documentation: https://docs.openalex.org/
    Base URL: https://api.openalex.org
    Acesso: Gratuito, requer email para rate limit
    
    Filtro por país: China (CN)
    """
    
    BASE_URL = "https://api.openalex.org"
    
    def __init__(self, email: str = None, delay: float = 0.2):
        self.email = email or os.environ.get("OPENALEX_EMAIL", "test@example.com")
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": f"MASWOS-OpenAlex/1.0 (mailto:{self.email})",
            "Accept": "application/json"
        })
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def search_chinese_papers(self, query: str, year: int = None,
                              limit: int = 50, 
                              open_access: bool = False) -> Dict:
        """Buscar papers de instituições chinesas"""
        self._rate_limit()
        
        url = f"{self.BASE_URL}/works"
        
        # Construir query com filtro de país
        full_query = f"({query}) AND authorships.countries:CN"
        if open_access:
            full_query += " AND open_access.is_oa:true"
        
        params = {
            "search": full_query,
            "per_page": min(limit, 200)
        }
        
        if year:
            params["filter"] = f"publication_year:{year}"
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                return self._parse_response(response.json())
        except Exception as e:
            print(f"[OpenAlex-China] Error: {e}")
        
        return {"works": [], "total": 0, "source": "openalex_china"}
    
    def get_chinese_institutions(self, limit: int = 100) -> List[Dict]:
        """Obter lista de instituições chinesas"""
        self._rate_limit()
        url = f"{self.BASE_URL}/institutions"
        params = {
            "filter": "country_code:CN",
            "per_page": min(limit, 200)
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                return data.get("results", [])
        except Exception as e:
            print(f"[OpenAlex-China] Error: {e}")
        
        return []
    
    def search_by_institution(self, query: str, institution_id: str,
                              limit: int = 50) -> Dict:
        """Buscar papers por instituição específica"""
        self._rate_limit()
        url = f"{self.BASE_URL}/works"
        
        params = {
            "search": query,
            "filter": f"authorships.institutions.id:{institution_id}",
            "per_page": min(limit, 200)
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                return self._parse_response(response.json())
        except Exception as e:
            print(f"[OpenAlex-China] Error: {e}")
        
        return {"works": [], "total": 0, "source": "openalex_china"}
    
    def _parse_response(self, data: Dict) -> Dict:
        """Parser para resposta OpenAlex"""
        works = []
        for item in data.get("results", []):
            work = {
                "id": item.get("id", ""),
                "title": item.get("title", ""),
                "publication_year": item.get("publication_year"),
                "doi": item.get("doi", ""),
                "cited_by_count": item.get("cited_by_count", 0),
                "is_oa": item.get("open_access", {}).get("is_oa", False),
                "oa_url": item.get("open_access", {}).get("oa_url", ""),
                "authors": [
                    a.get("author", {}).get("display_name", "")
                    for a in item.get("authorships", [])[:5]
                ],
                "institutions": [
                    inst.get("institution", {}).get("display_name", "")
                    for a in item.get("authorships", [])
                    for inst in a.get("institutions", [])[:2]
                ],
                "countries": list(set([
                    inst.get("country_code", "")
                    for a in item.get("authorships", [])
                    for inst in a.get("institutions", [])
                    if inst.get("country_code")
                ])),
                "source": "openalex"
            }
            works.append(work)
        
        return {
            "works": works,
            "total": data.get("meta", {}).get("count", 0),
            "source": "openalex_china"
        }


class CNKIWebScraper:
    """
    Scraper limitado para CNKI via web
    
    Nota: CNKI requer instituição parceira para API.
    Este scraper faz web scraping básico de metadados.
    
    Portal: https://kns.cnki.net
    """
    
    BASE_URL = "https://kns.cnki.net"
    
    def __init__(self, delay: float = 2.0):
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8"
        })
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def search(self, query: str, limit: int = 20) -> Dict:
        """Busca limitada via web (requer instituição para resultados completos)"""
        self._rate_limit()
        
        # CNKI requer JavaScript - web scraping limitado
        return {
            "articles": [],
            "total": 0,
            "source": "cnki_limited",
            "note": "CNKI requer autenticação institucional para acesso completo"
        }


# ==================== FUNÇÕES DE CONVENIÊNCIA ====================

def search_chinese_papers(query: str, year: int = None, 
                          limit: int = 20) -> List[Dict]:
    """Buscar papers de instituições chinesas via OpenAlex"""
    scraper = OpenAlexChinaScraper()
    result = scraper.search_chinese_papers(query, year=year, limit=limit)
    return result.get("works", [])

def search_openreview_venue(venue_id: str, limit: int = 50) -> List[Dict]:
    """Buscar papers em conferências (ICLR, NeurIPS, etc.)"""
    scraper = OpenReviewScraper()
    return scraper.get_submissions(venue_id, limit=limit)

def get_chinese_institutions() -> List[Dict]:
    """Obter lista de universidades chinesas"""
    scraper = OpenAlexChinaScraper()
    return scraper.get_chinese_institutions(limit=50)


# ==================== TESTES ====================

def test_chinese_apis():
    """Testar APIs acadêmicas chinesas"""
    print("=" * 70)
    print("MASWOS V5 NEXUS - Chinese Academic APIs Test")
    print("=" * 70)
    
    # Test 1: OpenAlex - Papers chineses
    print("\n[TEST 1] OpenAlex - Papers chineses 'AI'")
    openalex = OpenAlexChinaScraper()
    result = openalex.search_chinese_papers("artificial intelligence", year=2024, limit=5)
    print(f"  Total encontrado: {result['total']}")
    for work in result['works'][:3]:
        print(f"  - {work['title'][:50]}...")
        print(f"    Instituição: {', '.join(work.get('institutions', [])[:2])}")
    
    # Test 2: OpenAlex - Universidades chinesas
    print("\n[TEST 2] Top universidades chinesas")
    institutions = openalex.get_chinese_institutions(limit=10)
    for inst in institutions[:5]:
        print(f"  - {inst.get('display_name', '')}: {inst.get('works_count', 0)} papers")
    
    # Test 3: OpenReview - ICLR 2025
    print("\n[TEST 3] OpenReview - ICLR 2025")
    openreview = OpenReviewScraper()
    submissions = openreview.get_submissions("ICLR.cc/2025/Conference", limit=5)
    print(f"  Submissões encontradas: {len(submissions)}")
    for sub in submissions[:3]:
        print(f"  - {sub['title'][:50]}...")
    
    # Test 4: SciEngine Journals
    print("\n[TEST 4] SciEngine - Journals OA chineses")
    sciengine = SciEngineScraper()
    journals = sciengine.search_journals()
    for j in journals[:5]:
        print(f"  - {j['name']} (ISSN: {j['issn']})")
    
    print("\n" + "=" * 70)
    print("Chinese Academic APIs - Testes Concluídos")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    test_chinese_apis()
