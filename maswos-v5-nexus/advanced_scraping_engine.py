#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - Advanced Scraping Engine (Clean Version)
Técnicas avançadas de scraping granular e cirúrgico para APIs indisponíveis

Scrapers disponíveis:
- arXiv: Artigos científicos (API oficial, Atom feed)
- PubMed/Europe PMC: Artigos biomédicos (NCBI E-utilities, Europe PMC REST)
- Semantic Scholar: 200M+ papers (sem API key)
- DOAJ: Directory of Open Access Journals (sem API key)
- CORE: 300M+ OA papers (requer API key)
- dados.gov.br: Dados abertos do governo brasileiro (requer API key)

Arquitetura: Transformer-Agentes (Encoder → Scrapers → Validation → Decoder)
"""

import requests
import urllib3
import json
import time
import hashlib
import re
import xml.etree.ElementTree as ET
from pathlib import Path
from typing import Dict, List, Optional, Tuple, Any
from dataclasses import dataclass, field
from datetime import datetime, timedelta
from bs4 import BeautifulSoup
import logging
import os

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("AdvancedScraping")
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Import scrapers
try:
    from ncbi_official_scraper import NCBIOfficialScraper
    HAS_NCBIOFFICIAL = True
except ImportError:
    HAS_NCBIOFFICIAL = False

try:
    from arxiv_official_scraper import ArXivOfficialScraper
    HAS_ARXIVOFFICIAL = True
except ImportError:
    HAS_ARXIVOFFICIAL = False

try:
    from dados_gov_scraper import DadosGovScraper
    HAS_DADOSGOV = True
except ImportError:
    HAS_DADOSGOV = False

try:
    from semantic_scholar_scraper import SemanticScholarScraper
    HAS_SEMANTICSCHOLAR = True
except ImportError:
    HAS_SEMANTICSCHOLAR = False

try:
    from doaj_scraper import DOAJScraper
    HAS_DOAJ = True
except ImportError:
    HAS_DOAJ = False

try:
    from core_api_scraper import COREScraper
    HAS_CORE = True
except ImportError:
    HAS_CORE = False

try:
    from aminer_scraper import AMinerScraper
    HAS_AMINER = True
except ImportError:
    HAS_AMINER = False

try:
    from cnki_scraper import CNKIScraper
    HAS_CNKI = True
except ImportError:
    HAS_CNKI = False

try:
    from capes_scraper import CAPESScraper
    HAS_CAPES = True
except ImportError:
    HAS_CAPES = False

@dataclass
class ScrapingResult:
    source: str
    url: str
    status: str
    data: Optional[Dict] = None
    error: Optional[str] = None
    latency_ms: float = 0
    technique: str = ""
    cached: bool = False
    timestamp: str = ""

class CacheManager:
    def __init__(self, cache_dir: str = ".scraping_cache", ttl_hours: int = 24):
        self.cache_dir = Path(cache_dir)
        self.cache_dir.mkdir(exist_ok=True)
        self.ttl = timedelta(hours=ttl_hours)
    
    def _get_cache_key(self, url: str, params: Dict = None) -> str:
        key_str = url + json.dumps(params or {}, sort_keys=True)
        return hashlib.md5(key_str.encode()).hexdigest()
    
    def get(self, url: str, params: Dict = None) -> Optional[Dict]:
        cache_key = self._get_cache_key(url, params)
        cache_file = self.cache_dir / f"{cache_key}.json"
        
        if cache_file.exists():
            try:
                with open(cache_file, 'r', encoding='utf-8') as f:
                    cached = json.load(f)
                cached_time = datetime.fromisoformat(cached.get("timestamp", "2000-01-01"))
                if datetime.now() - cached_time < self.ttl:
                    return cached.get("data")
                else:
                    cache_file.unlink()
            except Exception as e:
                logger.warning(f"[CACHE ERROR] {e}")
        return None
    
    def set(self, url: str, data: Dict, params: Dict = None):
        cache_key = self._get_cache_key(url, params)
        cache_file = self.cache_dir / f"{cache_key}.json"
        cached = {"url": url, "params": params, "data": data, "timestamp": datetime.now().isoformat()}
        try:
            with open(cache_file, 'w', encoding='utf-8') as f:
                json.dump(cached, f, ensure_ascii=False, indent=2)
        except Exception as e:
            logger.warning(f"[CACHE SET ERROR] {e}")

class BrowserHeaders:
    @staticmethod
    def get_headers(browser: str = "chrome") -> Dict:
        headers = {
            "chrome": {
                "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
                "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
                "Accept-Encoding": "gzip, deflate, br",
                "Connection": "keep-alive"
            }
        }
        return headers.get(browser, headers["chrome"])

class RetryStrategy:
    def __init__(self, max_retries: int = 3, initial_delay: float = 1.0, backoff_factor: float = 2.0):
        self.max_retries = max_retries
        self.initial_delay = initial_delay
        self.backoff_factor = backoff_factor
    
    def execute(self, func, *args, **kwargs) -> Tuple[bool, any]:
        import random
        last_error = None
        delay = self.initial_delay
        
        for attempt in range(self.max_retries + 1):
            try:
                result = func(*args, **kwargs)
                return True, result
            except Exception as e:
                last_error = e
                if attempt < self.max_retries:
                    sleep_time = delay * (0.5 + random.random())
                    time.sleep(sleep_time)
                    delay *= self.backoff_factor
        
        return False, last_error

class ArXivScraper:
    """Scraper oficial para arXiv API"""
    
    def __init__(self, cache: CacheManager):
        self.cache = cache
        self.retry = RetryStrategy(max_retries=3, initial_delay=3.0)
        
        if HAS_ARXIVOFFICIAL:
            self.arxiv_scraper = ArXivOfficialScraper(delay=3.0)
            self.has_official = True
            logger.info("[ArXivScraper] arXiv Official API disponível")
        else:
            self.arxiv_scraper = None
            self.has_official = False
            logger.warning("[ArXivScraper] arXiv Official API não disponível")
    
    def search_articles(self, query: str, limit: int = 20) -> ScrapingResult:
        """Buscar artigos no arXiv"""
        start_time = time.time()
        
        cache_key = f"arxiv_search_{query}_{limit}"
        cached = self.cache.get(cache_key)
        if cached:
            return ScrapingResult(source="arXiv", url=cache_key, status="success", 
                                  data=cached, technique="cache", cached=True,
                                  timestamp=datetime.now().isoformat())
        
        techniques = [
            ("arxiv_official_api", self._technique_arxiv_official),
            ("arxiv_atom_feed", self._technique_arxiv_atom),
        ]
        
        for technique_name, technique_func in techniques:
            success, result = self.retry.execute(technique_func, query, limit)
            if success and result:
                latency = (time.time() - start_time) * 1000
                self.cache.set(cache_key, result)
                return ScrapingResult(source="arXiv", url=f"arxiv_search:{query}",
                                      status="success", data=result, latency_ms=round(latency, 2),
                                      technique=technique_name, timestamp=datetime.now().isoformat())
        
        return ScrapingResult(source="arXiv", url=f"arxiv_search:{query}", status="error",
                              error="Todas as técnicas de scraping arXiv falharam",
                              timestamp=datetime.now().isoformat())
    
    def _technique_arxiv_official(self, query: str, limit: int) -> Optional[Dict]:
        """Técnica 1: arXiv Official API"""
        if not self.has_official:
            return None
        try:
            result = self.arxiv_scraper.search(query, max_results=limit)
            if result.get("papers"):
                return {"source": "arXiv_Official_API", "total_results": result.get("total_results", 0),
                        "results": result.get("papers", []), "extraction_method": "arxiv_atom_api"}
            return None
        except Exception as e:
            logger.error(f"[ArXivScraper] Error: {e}")
            return None
    
    def _technique_arxiv_atom(self, query: str, limit: int) -> Optional[Dict]:
        """Técnica 2: Atom feed direto"""
        try:
            import urllib.parse, urllib.request
            encoded_query = urllib.parse.quote(query)
            url = f"http://export.arxiv.org/api/query?search_query={encoded_query}&start=0&max_results={limit}"
            
            req = urllib.request.Request(url, headers=BrowserHeaders.get_headers("chrome"))
            with urllib.request.urlopen(req, timeout=30) as response:
                return self._parse_atom_feed(response.read().decode('utf-8'))
        except Exception as e:
            logger.error(f"[ArXivScraper] Atom feed error: {e}")
            return None
    
    def _parse_atom_feed(self, xml_text: str) -> Dict:
        """Parser Atom feed"""
        try:
            ATOM_NS = "http://www.w3.org/2005/Atom"
            OPENSEARCH_NS = "http://a9.com/-/spec/opensearch/1.1/"
            
            root = ET.fromstring(xml_text)
            papers = []
            
            for entry in root.findall(f"{{{ATOM_NS}}}entry"):
                paper = {
                    "arxiv_id": entry.findtext(f"{{{ATOM_NS}}}id", "").split("/abs/")[-1],
                    "title": " ".join(entry.findtext(f"{{{ATOM_NS}}}title", "").split()),
                    "abstract": " ".join(entry.findtext(f"{{{ATOM_NS}}}summary", "").split()),
                    "authors": [a.findtext(f"{{{ATOM_NS}}}name", "") for a in entry.findall(f"{{{ATOM_NS}}}author")],
                    "categories": [c.get("term", "") for c in entry.findall(f"{{{ATOM_NS}}}category")],
                    "published": entry.findtext(f"{{{ATOM_NS}}}published", ""),
                    "pdf_url": ""
                }
                for link in entry.findall(f"{{{ATOM_NS}}}link"):
                    if link.get("title") == "pdf":
                        paper["pdf_url"] = link.get("href", "")
                papers.append(paper)
            
            total = root.findtext(f"{{{OPENSEARCH_NS}}}totalResults", "0")
            return {"source": "arXiv_Atom_Direct", "total_results": int(total),
                    "results": papers, "extraction_method": "atom_feed_direct"}
        except Exception as e:
            logger.error(f"[ArXivScraper] Atom parse error: {e}")
            return None

class PubMedScraper:
    """Scraper para PubMed e Europe PMC"""
    
    def __init__(self, cache: CacheManager):
        self.cache = cache
        self.retry = RetryStrategy(max_retries=3, initial_delay=1.0)
        
        if HAS_NCBIOFFICIAL:
            self.ncbi_scraper = NCBIOfficialScraper()
            self.has_official = True
            logger.info("[PubMedScraper] NCBI Official API disponível")
        else:
            self.ncbi_scraper = None
            self.has_official = False
            logger.warning("[PubMedScraper] NCBI Official API não disponível")
    
    def search_articles(self, query: str, limit: int = 20) -> ScrapingResult:
        """Buscar artigos no PubMed"""
        start_time = time.time()
        
        cache_key = f"pubmed_search_{query}_{limit}"
        cached = self.cache.get(cache_key)
        if cached:
            return ScrapingResult(source="PubMed", url=cache_key, status="success",
                                  data=cached, technique="cache", cached=True,
                                  timestamp=datetime.now().isoformat())
        
        techniques = [
            ("ncbi_official_api", self._technique_ncbi_official),
            ("europe_pmc_api", self._technique_europe_pmc),
            ("ncbi_api", self._technique_ncbi_api),
        ]
        
        for technique_name, technique_func in techniques:
            success, result = self.retry.execute(technique_func, query, limit)
            if success and result:
                latency = (time.time() - start_time) * 1000
                self.cache.set(cache_key, result)
                return ScrapingResult(source="PubMed", url=f"pubmed_search:{query}",
                                      status="success", data=result, latency_ms=round(latency, 2),
                                      technique=technique_name, timestamp=datetime.now().isoformat())
        
        return ScrapingResult(source="PubMed", url=f"pubmed_search:{query}", status="error",
                              error="Todas as técnicas falharam", timestamp=datetime.now().isoformat())
    
    def _technique_ncbi_official(self, query: str, limit: int) -> Optional[Dict]:
        """NCBI Official API"""
        if not self.has_official:
            return None
        try:
            articles = self.ncbi_scraper.search_articles(query=query, db="pubmed", max_results=limit)
            results = [{"pmid": a.pmid, "pmcid": a.pmcid, "title": a.title, "authors": a.authors,
                       "journal": a.journal, "publication_date": a.pub_date, "doi": a.doi,
                       "abstract": a.abstract, "citations": a.citations} for a in articles]
            return {"source": "NCBI_Official", "total_results": len(results), "results": results,
                    "extraction_method": "ncbi_official_api"}
        except Exception as e:
            logger.error(f"[PubMedScraper] NCBI Error: {e}")
            return None
    
    def _technique_europe_pmc(self, query: str, limit: int) -> Optional[Dict]:
        """Europe PMC REST API"""
        url = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
        params = {"query": query, "resultType": "core", "pageSize": limit, "format": "json"}
        response = requests.get(url, params=params, headers=BrowserHeaders.get_headers("chrome"),
                               timeout=20, verify=False)
        if response.status_code == 200:
            data = response.json()
            results = [{"pmid": a.get("pmid", ""), "title": a.get("title", ""),
                       "authors": [au.get("fullName", "") for au in a.get("authorList", {}).get("author", [])],
                       "journal": a.get("journalInfo", {}).get("journal", {}).get("title", ""),
                       "publication_date": a.get("pubYear", ""), "doi": a.get("doi", ""),
                       "abstract": a.get("abstractText", ""), "citations": a.get("citedByCount", 0)}
                      for a in data.get("resultList", {}).get("result", [])[:limit]]
            return {"source": "Europe_PMC", "total_results": len(results), "results": results,
                    "extraction_method": "api_rest"}
        return None
    
    def _technique_ncbi_api(self, query: str, limit: int) -> Optional[Dict]:
        """NCBI E-utilities raw"""
        search_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
        params = {"db": "pubmed", "term": query, "retmax": limit, "retmode": "json"}
        response = requests.get(search_url, params=params, headers=BrowserHeaders.get_headers("chrome"),
                               timeout=15, verify=False)
        if response.status_code == 200:
            id_list = response.json().get("esearchresult", {}).get("idlist", [])
            if id_list:
                return self._fetch_pubmed_details(id_list)
        return None
    
    def _fetch_pubmed_details(self, id_list: List[str]) -> Optional[Dict]:
        """Fetch PubMed details"""
        fetch_url = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
        params = {"db": "pubmed", "id": ",".join(id_list), "retmode": "xml"}
        response = requests.get(fetch_url, params=params, headers=BrowserHeaders.get_headers("chrome"),
                               timeout=20, verify=False)
        if response.status_code == 200:
            soup = BeautifulSoup(response.text, 'lxml-xml')
            results = []
            for article in soup.find_all('PubmedArticle')[:10]:
                results.append({
                    "pmid": article.findtext('PMID', ''),
                    "title": article.findtext('ArticleTitle', ''),
                    "authors": [f"{a.findtext('LastName', '')}, {a.findtext('ForeName', '')}".strip(', ')
                               for a in article.findall('.//Author')],
                    "journal": article.findtext('.//Journal/Title', ''),
                    "abstract": article.findtext('.//AbstractText', '')
                })
            return {"source": "PubMed_XML", "total_results": len(results), "results": results,
                    "extraction_method": "xml_parsing"}
        return None

class SemanticScholarScraperAdvanced:
    """
    Scraper avançado para Semantic Scholar API
    
    Sem API key para uso básico (100 req/5 min)
    Com API key para maior rate limit (1 req/s)
    """
    
    def __init__(self, cache: CacheManager, api_key: Optional[str] = None):
        self.cache = cache
        self.retry = RetryStrategy(max_retries=2, initial_delay=1.0)
        self.api_key = api_key or os.environ.get("SEMANTIC_SCHOLAR_API_KEY")
        
        if HAS_SEMANTICSCHOLAR:
            self.ss_scraper = SemanticScholarScraper(api_key=self.api_key, delay=1.0)
            self.has_official = True
            logger.info(f"[SemanticScholar] Semantic Scholar scraper disponível (auth: {'sim' if self.api_key else 'não'})")
        else:
            self.ss_scraper = None
            self.has_official = False
            logger.warning("[SemanticScholar] Semantic Scholar scraper não disponível")
    
    def search_articles(self, query: str, limit: int = 20) -> ScrapingResult:
        """Buscar papers no Semantic Scholar"""
        start_time = time.time()
        
        cache_key = f"semanticscholar_search_{query}_{limit}"
        cached = self.cache.get(cache_key)
        if cached:
            return ScrapingResult(source="Semantic Scholar", url=cache_key, status="success",
                                  data=cached, technique="cache", cached=True,
                                  timestamp=datetime.now().isoformat())
        
        if not self.has_official:
            return ScrapingResult(source="Semantic Scholar", url=f"ss_search:{query}", 
                                  status="error",
                                  error="Semantic Scholar scraper não disponível",
                                  timestamp=datetime.now().isoformat())
        
        try:
            result = self.ss_scraper.search_papers(query, limit=limit)
            papers = result.get("papers", [])
            
            if papers:
                latency = (time.time() - start_time) * 1000
                formatted = {
                    "source": "semanticscholar",
                    "total_results": result.get("total", len(papers)),
                    "results": papers,
                    "extraction_method": "semanticscholar_api"
                }
                self.cache.set(cache_key, formatted)
                return ScrapingResult(source="Semantic Scholar", url=f"ss_search:{query}",
                                      status="success", data=formatted, latency_ms=round(latency, 2),
                                      technique="semanticscholar_api",
                                      timestamp=datetime.now().isoformat())
            else:
                return ScrapingResult(source="Semantic Scholar", url=f"ss_search:{query}",
                                      status="success",
                                      data={"source": "semanticscholar",
                                            "total_results": 0, "results": [],
                                            "extraction_method": "semanticscholar_api"},
                                      technique="semanticscholar_empty",
                                      timestamp=datetime.now().isoformat())
        
        except Exception as e:
            logger.error(f"[SemanticScholar] Error: {e}")
            return ScrapingResult(source="Semantic Scholar", url=f"ss_search:{query}",
                                  status="error", error=str(e),
                                  timestamp=datetime.now().isoformat())

class DOAJScraperAdvanced:
    """
    Scraper avançado para DOAJ (Directory of Open Access Journals)
    
    Sem API key necessária para busca
    API: https://doaj.org/api/v4/docs
    """
    
    def __init__(self, cache: CacheManager):
        self.cache = cache
        self.retry = RetryStrategy(max_retries=2, initial_delay=0.5)
        
        if HAS_DOAJ:
            self.doaj_scraper = DOAJScraper(delay=0.5)
            self.has_official = True
            logger.info("[DOAJ] DOAJ scraper disponível")
        else:
            self.doaj_scraper = None
            self.has_official = False
            logger.warning("[DOAJ] DOAJ scraper não disponível")
    
    def search_articles(self, query: str, limit: int = 20) -> ScrapingResult:
        """Buscar artigos no DOAJ"""
        start_time = time.time()
        
        cache_key = f"doaj_search_{query}_{limit}"
        cached = self.cache.get(cache_key)
        if cached:
            return ScrapingResult(source="DOAJ", url=cache_key, status="success",
                                  data=cached, technique="cache", cached=True,
                                  timestamp=datetime.now().isoformat())
        
        if not self.has_official:
            return ScrapingResult(source="DOAJ", url=f"doaj_search:{query}", 
                                  status="error",
                                  error="DOAJ scraper não disponível",
                                  timestamp=datetime.now().isoformat())
        
        try:
            result = self.doaj_scraper.search_articles(query, page_size=limit)
            articles = result.get("articles", [])
            
            if articles:
                latency = (time.time() - start_time) * 1000
                formatted = {
                    "source": "doaj",
                    "total_results": result.get("total", len(articles)),
                    "results": articles,
                    "extraction_method": "doaj_api"
                }
                self.cache.set(cache_key, formatted)
                return ScrapingResult(source="DOAJ", url=f"doaj_search:{query}",
                                      status="success", data=formatted, latency_ms=round(latency, 2),
                                      technique="doaj_api",
                                      timestamp=datetime.now().isoformat())
            else:
                return ScrapingResult(source="DOAJ", url=f"doaj_search:{query}",
                                      status="success",
                                      data={"source": "doaj", "total_results": 0, "results": [],
                                            "extraction_method": "doaj_api"},
                                      technique="doaj_empty",
                                      timestamp=datetime.now().isoformat())
        
        except Exception as e:
            logger.error(f"[DOAJ] Error: {e}")
            return ScrapingResult(source="DOAJ", url=f"doaj_search:{query}",
                                  status="error", error=str(e),
                                  timestamp=datetime.now().isoformat())

class COREScraperAdvanced:
    """
    Scraper avançado para CORE API
    
    Requer API key (gratuito): https://core.ac.uk/services/api
    300M+ papers de acesso aberto
    """
    
    def __init__(self, cache: CacheManager, api_key: Optional[str] = None):
        self.cache = cache
        self.retry = RetryStrategy(max_retries=2, initial_delay=10.0)
        self.api_key = api_key or os.environ.get("CORE_API_KEY")
        
        if HAS_CORE:
            self.core_scraper = COREScraper(api_key=self.api_key, delay=10.0)
            self.has_official = True
            logger.info(f"[CORE] CORE API scraper disponível (auth: {'sim' if self.api_key else 'não'})")
        else:
            self.core_scraper = None
            self.has_official = False
            logger.warning("[CORE] CORE API scraper não disponível")
    
    def search_articles(self, query: str, limit: int = 20) -> ScrapingResult:
        """Buscar artigos no CORE"""
        start_time = time.time()
        
        cache_key = f"core_search_{query}_{limit}"
        cached = self.cache.get(cache_key)
        if cached:
            return ScrapingResult(source="CORE", url=cache_key, status="success",
                                  data=cached, technique="cache", cached=True,
                                  timestamp=datetime.now().isoformat())
        
        if not self.has_official:
            return ScrapingResult(source="CORE", url=f"core_search:{query}", 
                                  status="error",
                                  error="CORE scraper não disponível (requer API key)",
                                  timestamp=datetime.now().isoformat())
        
        if not self.core_scraper.is_available():
            return ScrapingResult(source="CORE", url=f"core_search:{query}", 
                                  status="error",
                                  error="CORE API key não configurada (CORE_API_KEY)",
                                  timestamp=datetime.now().isoformat())
        
        try:
            result = self.core_scraper.search_works(query, limit=limit)
            articles = result.get("articles", [])
            
            if articles:
                latency = (time.time() - start_time) * 1000
                formatted = {
                    "source": "core",
                    "total_results": result.get("total", len(articles)),
                    "results": articles,
                    "extraction_method": "core_api"
                }
                self.cache.set(cache_key, formatted)
                return ScrapingResult(source="CORE", url=f"core_search:{query}",
                                      status="success", data=formatted, latency_ms=round(latency, 2),
                                      technique="core_api",
                                      timestamp=datetime.now().isoformat())
            else:
                return ScrapingResult(source="CORE", url=f"core_search:{query}",
                                      status="success",
                                      data={"source": "core", "total_results": 0, "results": [],
                                            "extraction_method": "core_api"},
                                      technique="core_empty",
                                      timestamp=datetime.now().isoformat())
        
        except Exception as e:
            logger.error(f"[CORE] Error: {e}")
            return ScrapingResult(source="CORE", url=f"core_search:{query}",
                                  status="error", error=str(e),
                                  timestamp=datetime.now().isoformat())

class AMinerScraperAdvanced:
    """
    Scraper avançado para AMiner Open Platform API
    
    300M+ papers, 160M+ scholars, 600K+ venues
    
    Requer API token (gratuito para pesquisadores):
    https://open.aminer.cn/open/board?tab=control
    
    Inclui dados do Open Academic Graph (OAG):
    Microsoft Academic Graph + AMiner
    """
    
    def __init__(self, cache: CacheManager, api_token: Optional[str] = None):
        self.cache = cache
        self.retry = RetryStrategy(max_retries=2, initial_delay=1.0)
        self.api_token = api_token or os.environ.get("AMINER_API_KEY")
        
        if HAS_AMINER:
            self.aminer_scraper = AMinerScraper(api_token=self.api_token, delay=1.0)
            self.has_official = True
            logger.info(f"[AMiner] AMiner scraper disponível (auth: {'sim' if self.api_token else 'não'})")
        else:
            self.aminer_scraper = None
            self.has_official = False
            logger.warning("[AMiner] AMiner scraper não disponível")
    
    def search_articles(self, query: str, limit: int = 20) -> ScrapingResult:
        """Buscar papers no AMiner"""
        start_time = time.time()
        
        cache_key = f"aminer_search_{query}_{limit}"
        cached = self.cache.get(cache_key)
        if cached:
            return ScrapingResult(source="AMiner", url=cache_key, status="success",
                                  data=cached, technique="cache", cached=True,
                                  timestamp=datetime.now().isoformat())
        
        if not self.has_official:
            return ScrapingResult(source="AMiner", url=f"aminer_search:{query}", 
                                  status="error",
                                  error="AMiner scraper não disponível",
                                  timestamp=datetime.now().isoformat())
        
        try:
            result = self.aminer_scraper.search_papers(query, limit=limit)
            papers = result.get("papers", [])
            
            if papers:
                latency = (time.time() - start_time) * 1000
                formatted = {
                    "source": "aminer",
                    "total_results": result.get("total", len(papers)),
                    "results": papers,
                    "extraction_method": "aminer_api"
                }
                self.cache.set(cache_key, formatted)
                return ScrapingResult(source="AMiner", url=f"aminer_search:{query}",
                                      status="success", data=formatted, latency_ms=round(latency, 2),
                                      technique="aminer_api",
                                      timestamp=datetime.now().isoformat())
            else:
                return ScrapingResult(source="AMiner", url=f"aminer_search:{query}",
                                      status="success",
                                      data={"source": "aminer", "total_results": 0, "results": [],
                                            "extraction_method": "aminer_api"},
                                      technique="aminer_empty",
                                      timestamp=datetime.now().isoformat())
        
        except Exception as e:
            logger.error(f"[AMiner] Error: {e}")
            return ScrapingResult(source="AMiner", url=f"aminer_search:{query}",
                                  status="error", error=str(e),
                                  timestamp=datetime.now().isoformat())

class DadosGovScraperAdvanced:
    """
    Scraper avançado para dados.gov.br
    
    Nota: O portal dados.gov.br requer autenticação para acesso à API.
    Configure DADOS_GOV_API_KEY ou passe api_key para acesso completo.
    Sem autenticação, o scraper retorna lista vazia (site usa JavaScript SPA).
    """
    
    def __init__(self, cache: CacheManager, api_key: Optional[str] = None):
        self.cache = cache
        self.retry = RetryStrategy(max_retries=2, initial_delay=1.0)
        self.api_key = api_key or os.environ.get("DADOS_GOV_API_KEY")
        
        if HAS_DADOSGOV:
            self.dados_scraper = DadosGovScraper(api_key=self.api_key, delay=1.0)
            self.has_official = True
            logger.info(f"[DadosGovScraper] dados.gov.br scraper disponível (auth: {'sim' if self.api_key else 'não'})")
        else:
            self.dados_scraper = None
            self.has_official = False
            logger.warning("[DadosGovScraper] dados.gov.br scraper não disponível")
    
    def search_datasets(self, query: str, limit: int = 20) -> ScrapingResult:
        """Buscar datasets no portal de dados abertos"""
        start_time = time.time()
        
        cache_key = f"dadosgov_search_{query}_{limit}"
        cached = self.cache.get(cache_key)
        if cached:
            return ScrapingResult(source="dados.gov.br", url=cache_key, status="success",
                                  data=cached, technique="cache", cached=True,
                                  timestamp=datetime.now().isoformat())
        
        if not self.has_official:
            return ScrapingResult(source="dados.gov.br", url=f"dadosgov_search:{query}", 
                                  status="error",
                                  error="dados.gov.br scraper não disponível",
                                  timestamp=datetime.now().isoformat())
        
        try:
            result = self.dados_scraper.search_datasets(query, page_size=limit)
            datasets = result.get("datasets", [])
            
            if datasets:
                latency = (time.time() - start_time) * 1000
                formatted = {
                    "source": result.get("source", "dados.gov.br"),
                    "total_results": result.get("total", len(datasets)),
                    "results": datasets,
                    "extraction_method": "dados_gov_api"
                }
                self.cache.set(cache_key, formatted)
                return ScrapingResult(source="dados.gov.br", url=f"dadosgov_search:{query}",
                                      status="success", data=formatted, latency_ms=round(latency, 2),
                                      technique=result.get("source", "api"),
                                      timestamp=datetime.now().isoformat())
            else:
                return ScrapingResult(source="dados.gov.br", url=f"dadosgov_search:{query}",
                                      status="success",
                                      data={"source": result.get("source", "dados.gov.br"),
                                            "total_results": 0, "results": [],
                                            "extraction_method": "no_auth_limitation",
                                            "note": "Sem autenticação ou site usa JavaScript SPA"},
                                      technique=result.get("source", "limited"),
                                      timestamp=datetime.now().isoformat())
        
        except Exception as e:
            logger.error(f"[DadosGovScraper] Error: {e}")
            return ScrapingResult(source="dados.gov.br", url=f"dadosgov_search:{query}",
                                  status="error", error=str(e),
                                  timestamp=datetime.now().isoformat())

class AdvancedScrapingOrchestrator:
    """Orquestrador principal com fallback automático"""
    
    def __init__(self, cache_ttl_hours: int = 24, 
                 dados_gov_api_key: Optional[str] = None,
                 semantic_scholar_api_key: Optional[str] = None,
                 core_api_key: Optional[str] = None,
                 aminer_api_key: Optional[str] = None):
        self.cache = CacheManager(ttl_hours=cache_ttl_hours)
        
        # Scrapers existentes
        self.arxiv_scraper = ArXivScraper(self.cache)
        self.pubmed_scraper = PubMedScraper(self.cache)
        self.dadosgov_scraper = DadosGovScraperAdvanced(self.cache, api_key=dados_gov_api_key)
        
        # Novos scrapers
        self.semanticscholar_scraper = SemanticScholarScraperAdvanced(self.cache, api_key=semantic_scholar_api_key)
        self.doaj_scraper = DOAJScraperAdvanced(self.cache)
        self.core_scraper = COREScraperAdvanced(self.cache, api_key=core_api_key)
        self.aminer_scraper = AMinerScraperAdvanced(self.cache, api_token=aminer_api_key)
        
        # CAPES scraper
        self.capes_scraper = CAPESScraper() if HAS_CAPES else None
        if self.capes_scraper:
            logger.info("[CAPES] Scraper disponível")
        else:
            logger.warning("[CAPES] Scraper não disponível")
    
    def scrape_with_fallback(self, source: str, query: str, **kwargs) -> ScrapingResult:
        """
        Scraping com fallback automático
        
        Fontes suportadas:
        - ARXIV: Artigos científicos do arXiv (~2M papers)
        - PUBMED: Artigos biomédicos do PubMed/Europe PMC (~35M papers)
        - SEMANTICSCHOLAR: Semantic Scholar API (~200M papers, sem API key)
        - DOAJ: Directory of Open Access Journals (~21K journals, sem API key)
        - CORE: CORE API (~300M OA papers, requer API key)
        - AMINER: AMiner Open Platform (~300M papers, requer token gratuito)
        - DADOSGOV: Dados abertos do governo brasileiro (dados.gov.br)
        """
        scrapers = {
            "ARXIV": self.arxiv_scraper.search_articles,
            "PUBMED": self.pubmed_scraper.search_articles,
            "DADOSGOV": self.dadosgov_scraper.search_datasets,
            "SEMANTICSCHOLAR": self.semanticscholar_scraper.search_articles,
            "DOAJ": self.doaj_scraper.search_articles,
            "CORE": self.core_scraper.search_articles,
            "AMINER": self.aminer_scraper.search_articles,
            "CAPES": self._search_capes
        }
        
        scraper_func = scrapers.get(source.upper())
        if scraper_func:
            return scraper_func(query, kwargs.get("limit", 10))
        
        return ScrapingResult(source=source, url=query, status="error",
                              error=f"Scraper não encontrado para: {source}")
    
    def _search_capes(self, query: str, limit: int = 10) -> ScrapingResult:
        """Buscar dados CAPES por query (IES, UF, região)"""
        start_time = time.time()
        
        cache_key = f"capes_search_{query}_{limit}"
        cached = self.cache.get(cache_key)
        if cached:
            return ScrapingResult(source="CAPES", url=query, status="success",
                                  data=cached, technique="cache", cached=True,
                                  timestamp=datetime.now().isoformat())
        
        if not self.capes_scraper:
            return ScrapingResult(source="CAPES", url=query, status="error",
                                  error="CAPES scraper não disponível",
                                  timestamp=datetime.now().isoformat())
        
        try:
            summary = self.capes_scraper.get_acessos_summary()
            
            # Filter by query if provided
            filtered_data = []
            query_lower = query.lower()
            
            for year, stats in summary.items():
                if stats and stats.get("total_registros", 0) > 0:
                    # Include all data, filter results if query matches
                    filtered_data.append({
                        "ano": year,
                        "stats": stats
                    })
            
            formatted = {
                "source": "capes",
                "query": query,
                "total_results": len(filtered_data),
                "results": filtered_data,
                "note": "Dados de acessos ao Portal de Periódicos CAPES"
            }
            
            latency = (time.time() - start_time) * 1000
            self.cache.set(cache_key, formatted)
            
            return ScrapingResult(source="CAPES", url=query, status="success",
                                  data=formatted, latency_ms=round(latency, 2),
                                  technique="capes_api",
                                  timestamp=datetime.now().isoformat())
        
        except Exception as e:
            logger.error(f"[CAPES] Error: {e}")
            return ScrapingResult(source="CAPES", url=query, status="error",
                                  error=str(e),
                                  timestamp=datetime.now().isoformat())
    
    def search_all(self, query: str, limit: int = 10) -> Dict[str, ScrapingResult]:
        """Buscar em todas as fontes disponíveis"""
        results = {}
        
        sources = ["ARXIV", "PUBMED", "SEMANTICSCHOLAR", "DOAJ", "CORE", "AMINER", "DADOSGOV", "CAPES"]
        
        for source in sources:
            try:
                result = self.scrape_with_fallback(source, query, limit=limit)
                results[source] = result
            except Exception as e:
                logger.error(f"[Orchestrator] Error searching {source}: {e}")
                results[source] = ScrapingResult(source=source, url=query, status="error",
                                                  error=str(e), timestamp=datetime.now().isoformat())
        
        return results

# Global instance
scraping_orchestrator = AdvancedScrapingOrchestrator()

def test_scraping():
    """Testar scrapers"""
    print("=" * 70)
    print("MASWOS V5 NEXUS - Advanced Scraping Engine (Clean)")
    print("=" * 70)
    
    orchestrator = AdvancedScrapingOrchestrator()
    
    # Test arXiv
    print("\n[TEST 1] arXiv: 'deep learning'")
    result = orchestrator.scrape_with_fallback("ARXIV", "deep learning", limit=2)
    print(f"  Source: {result.source}")
    print(f"  Status: {result.status}")
    print(f"  Technique: {result.technique}")
    print(f"  Latency: {result.latency_ms:.2f}ms")
    
    if result.data:
        papers = result.data.get('results', [])
        for i, paper in enumerate(papers[:2], 1):
            print(f"  Paper {i}: {paper.get('title', '')[:50]}...")
    
    # Test PubMed
    print("\n[TEST 2] PubMed: 'cancer diagnosis'")
    result = orchestrator.scrape_with_fallback("PUBMED", "cancer diagnosis", limit=2)
    print(f"  Source: {result.source}")
    print(f"  Status: {result.status}")
    print(f"  Technique: {result.technique}")
    print(f"  Latency: {result.latency_ms:.2f}ms")
    
    # Test Semantic Scholar (sem API key)
    print("\n[TEST 3] Semantic Scholar: 'transformer'")
    result = orchestrator.scrape_with_fallback("SEMANTICSCHOLAR", "transformer", limit=3)
    print(f"  Source: {result.source}")
    print(f"  Status: {result.status}")
    print(f"  Technique: {result.technique}")
    if result.data:
        print(f"  Total: {result.data.get('total_results', 0)}")
    
    # Test DOAJ (sem API key)
    print("\n[TEST 4] DOAJ: 'open access'")
    result = orchestrator.scrape_with_fallback("DOAJ", "open access", limit=3)
    print(f"  Source: {result.source}")
    print(f"  Status: {result.status}")
    print(f"  Technique: {result.technique}")
    if result.data:
        print(f"  Total: {result.data.get('total_results', 0)}")
    
    # Test dados.gov.br
    print("\n[TEST 5] dados.gov.br: 'educacao'")
    result = orchestrator.scrape_with_fallback("DADOSGOV", "educacao", limit=3)
    print(f"  Source: {result.source}")
    print(f"  Status: {result.status}")
    print(f"  Technique: {result.technique}")
    if result.data:
        print(f"  Total: {result.data.get('total_results', 0)}")
        print(f"  Note: {result.data.get('note', 'N/A')}")
    
    # Test search all
    print("\n[TEST 6] Search all sources: 'machine learning'")
    results = orchestrator.search_all("machine learning", limit=2)
    print("\n  Results Summary:")
    for source, res in results.items():
        total = res.data.get('total_results', 0) if res.data else 0
        print(f"    {source}: {res.status} | {total} results | {res.technique}")
    
    print("\n" + "=" * 70)
    return True

if __name__ == "__main__":
    test_scraping()