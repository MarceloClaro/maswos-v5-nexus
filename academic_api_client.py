#!/usr/bin/env python3
"""
MASWOS Academic API Client
Wrapper para APIs acadêmicas reais (CAPES, SciELO, arXiv, PubMed, etc.)
"""

import json
import requests
from typing import List, Dict, Optional, Any
from datetime import datetime
import urllib.parse

class ArxivClient:
    """Cliente para API arXiv (open access)"""
    
    BASE_URL = "http://export.arxiv.org/api/query"
    
    CATEGORIES = {
        "cs": "Computer Science",
        "cs.AI": "Artificial Intelligence",
        "cs.CL": "Computation and Language",
        "cs.CV": "Computer Vision",
        "cs.LG": "Machine Learning",
        "stat.ML": "Machine Learning (Statistics)",
        "math": "Mathematics",
        "physics": "Physics",
        "q-bio": "Quantitative Biology",
        "quant-ph": "Quantum Physics"
    }
    
    def search(self, query: str, max_results: int = 10, 
               start: int = 0, category: str = None) -> List[Dict]:
        """
        Busca artigos no arXiv com retry
        
        Args:
            query: Termo de busca
            max_results: Número máximo de resultados
            start: Offset de resultados
            category: Categoria arXiv (opcional)
        """
        params = {
            "search_query": f"all:{query}",
            "start": start,
            "max_results": max_results,
            "sortBy": "submittedDate",
            "sortOrder": "descending"
        }
        
        if category:
            params["search_query"] = f"cat:{category} AND all:{query}"
        
        from requests.adapters import HTTPAdapter
        from urllib3.util.retry import Retry
        
        session = requests.Session()
        retry_strategy = Retry(
            total=5,
            backoff_factor=2,
            status_forcelist=[429, 500, 502, 503, 504],
            connect=3,
            read=3
        )
        adapter = HTTPAdapter(max_retries=retry_strategy)
        session.mount("http://", adapter)
        session.mount("https://", adapter)
        
        for attempt in range(3):
            try:
                response = session.get(self.BASE_URL, params=params, timeout=120)
                response.raise_for_status()
                return self._parse_atom(response.text)
            except requests.exceptions.Timeout:
                print(f"arXiv timeout (attempt {attempt+1}/3) for: {query}")
                if attempt < 2:
                    import time
                    time.sleep(3)
            except requests.exceptions.RequestException as e:
                print(f"arXiv error {attempt+1}/3: {e}")
                if attempt >= 2:
                    return self._fallback_search(query, max_results)
        
        return self._fallback_search(query, max_results)
    
    def _fallback_search(self, query: str, max_results: int) -> List[Dict]:
        """Fallback via Semantic Scholar ou OpenAlex se arXiv falhar"""
        try:
            from academic_api_client import SemanticScholarClient
            ss = SemanticScholarClient()
            papers = ss.search_papers(query, limit=max_results)
            results = []
            for p in papers:
                results.append({
                    "id": p.get("paperId", ""),
                    "title": p.get("title", ""),
                    "summary": p.get("abstract", ""),
                    "authors": [a.get("name", "") for a in p.get("authors", [])],
                    "published": str(p.get("year", "")),
                    "categories": [],
                    "pdf_url": p.get("openAccessPdf", {}).get("url") if p.get("openAccessPdf") else None,
                    "doi": p.get("externalIds", {}).get("DOI"),
                    "source": "semantic_scholar_fallback"
                })
            return results
        except Exception as e:
            print(f"Fallback failed: {e}")
            return []
    
    def _parse_atom(self, xml_text: str) -> List[Dict]:
        """Parseia resposta XML do arXiv"""
        import xml.etree.ElementTree as ET
        
        articles = []
        try:
            root = ET.fromstring(xml_text)
            ns = {
                "atom": "http://www.w3.org/2005/Atom",
                "arxiv": "http://arxiv.org/schemas/atom"
            }
            
            for entry in root.findall(".//{http://www.w3.org/2005/Atom}entry"):
                article = {
                    "id": entry.find("{http://www.w3.org/2005/Atom}id").text,
                    "title": entry.find("{http://www.w3.org/2005/Atom}title").text.strip().replace("\n", " "),
                    "summary": entry.find("{http://www.w3.org/2005/Atom}summary").text.strip(),
                    "authors": [a.find("{http://www.w3.org/2005/Atom}name").text for a in entry.findall("{http://www.w3.org/2005/Atom}author")],
                    "published": entry.find("{http://www.w3.org/2005/Atom}published").text,
                    "updated": entry.find("{http://www.w3.org/2005/Atom}updated").text,
                    "categories": [cat.get("term") for cat in entry.findall("{http://www.w3.org/2005/Atom}category")],
                }
                
                links = {link.get("title"): link.get("href") 
                        for link in entry.findall("{http://www.w3.org/2005/Atom}link")}
                article["pdf_url"] = links.get("pdf")
                
                doi_elem = entry.find("{http://arxiv.org/schemas/atom}doi")
                article["doi"] = doi_elem.text if doi_elem is not None else None
                
                articles.append(article)
        except Exception as e:
            print(f"Error parsing arXiv response: {e}")
        
        return articles


class ScieloClient:
    """Cliente para SciELO -期刊列表和文章搜索"""
    
    def search_articles(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca artigos via articlemetaapi com retry"""
        try:
            from articlemeta.client import RestfulClient
            import time
            
            client = RestfulClient()
            results = []
            count = 0
            
            for attempt in range(3):
                try:
                    for article in client.documents():
                        if count >= limit:
                            break
                        try:
                            title = article.original_title or ""
                            if query.lower() in title.lower() or not query:
                                results.append({
                                    "title": title,
                                    "doi": article.doi,
                                    "issn": getattr(article, 'issn', None),
                                    "collection": article.collection_acronym,
                                    "publication_date": article.document_publication_date,
                                    "document_type": article.document_type
                                })
                        except Exception:
                            pass
                        count += 1
                    break
                except Exception as e:
                    if "timed out" in str(e).lower():
                        print(f"SciELO retry {attempt+1}/3...")
                        time.sleep(2)
                    else:
                        raise
            
            return results
        except Exception as e:
            print(f"SciELO error: {e}")
        
        return []
    
    def list_journals(self, collection: str = "scl", limit: int = 10) -> List[Dict]:
        """Lista periódicos - collection: scl (SciELO Brasil), spa (Spain), col (Colombia)"""
        try:
            from articlemeta.client import RestfulClient
            import time
            
            client = RestfulClient()
            results = []
            count = 0
            
            for attempt in range(3):
                try:
                    for journal in client.journals(collection=collection):
                        if count >= limit:
                            break
                        results.append({
                            "issn": getattr(journal, 'scielo_issn', None),
                            "title": getattr(journal, 'title', ''),
                            "abbreviation": getattr(journal, 'abbreviated_title', ''),
                            "electronic_issn": getattr(journal, 'electronic_issn', None)
                        })
                        count += 1
                    break
                except Exception as e:
                    if "timed out" in str(e).lower():
                        print(f"SciELO journals retry {attempt+1}/3...")
                        time.sleep(2)
                    else:
                        raise
            
            return results
        except Exception as e:
            print(f"SciELO journals error: {e}")
        
        return []
    
    def get_journal(self, issn: str) -> Optional[Dict]:
        """Obtém informações de periódico pelo ISSN"""
        try:
            from articlemeta.client import RestfulClient
            import time
            
            client = RestfulClient()
            
            for attempt in range(3):
                try:
                    for journal in client.journals(issn=issn):
                        return {
                            "issn": getattr(journal, 'scielo_issn', None),
                            "title": getattr(journal, 'title', ''),
                            "abbreviation": getattr(journal, 'abbreviated_title', ''),
                            "electronic_issn": getattr(journal, 'electronic_issn', None)
                        }
                except Exception as e:
                    if "timed out" in str(e).lower():
                        print(f"SciELO journal retry {attempt+1}/3...")
                        time.sleep(2)
                    else:
                        raise
        except Exception as e:
            print(f"SciELO journal error: {e}")
        
        return None
    
    def list_journals(self, collection: str = "scl", limit: int = 10) -> List[Dict]:
        """Lista periódicos - collection: scl (SciELO Brasil), spa (Spain), col (Colombia)"""
        try:
            from articlemeta.client import RestfulClient
            import time
            
            client = RestfulClient()
            results = []
            count = 0
            
            for attempt in range(3):
                try:
                    for journal in client.journals(collection=collection):
                        if count >= limit:
                            break
                        results.append({
                            "issn": getattr(journal, 'scielo_issn', None),
                            "title": getattr(journal, 'title', ''),
                            "abbreviation": getattr(journal, 'abbreviated_title', ''),
                            "electronic_issn": getattr(journal, 'electronic_issn', None)
                        })
                        count += 1
                    break
                except Exception as e:
                    if "timed out" in str(e).lower():
                        print(f"SciELO journals retry {attempt+1}/3...")
                        time.sleep(2)
                    else:
                        raise
            
            return results
        except Exception as e:
            print(f"SciELO journals error: {e}")
        
        return []


class CrossrefClient:
    """Cliente para CrossRef API"""
    
    BASE = "https://api.crossref.org/works"
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca artigos no CrossRef"""
        params = {
            "query": query,
            "rows": limit,
            "sort": "published"
        }
        
        response = requests.get(self.BASE, params=params, timeout=30)
        data = response.json()
        
        results = []
        for item in data.get("message", {}).get("items", []):
            results.append({
                "doi": item.get("DOI"),
                "title": item.get("title", [""])[0],
                "author": [a.get("given", "") + " " + a.get("family", "") 
                          for a in item.get("author", [])],
                "published": item.get("published-print", {}).get("date-parts", [[]])[0],
                "journal": item.get("container-title", [""])[0],
                "type": item.get("type"),
                "is_oa": item.get("license", [{}])[0].get("URL", "").startswith("http://creativecommons")
            })
        
        return results


class PubmedClient:
    """Cliente para NCBI/PubMed E-utilities"""
    
    ESEARCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/esearch.fcgi"
    EFETCH = "https://eutils.ncbi.nlm.nih.gov/entrez/eutils/efetch.fcgi"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
    
    def search(self, query: str, db: str = "pubmed", max_results: int = 10) -> List[str]:
        """Busca no PubMed"""
        params = {
            "db": db,
            "term": query,
            "retmax": max_results,
            "retmode": "json",
            "sort": "pub_date"
        }
        
        if self.api_key:
            params["api_key"] = self.api_key
        
        try:
            response = requests.get(self.ESEARCH, params=params, timeout=30)
            data = response.json()
            return data.get("esearchresult", {}).get("idlist", [])
        except Exception as e:
            print(f"PubMed error: {e}")
            return []


class OpenAlexClient:
    """Cliente para OpenAlex API"""
    
    BASE = "https://api.openalex.org"
    
    def search_works(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca trabalhos acadêmicos"""
        params = {
            "search": query,
            "per_page": limit,
            "sort": "cited_by_count:desc"
        }
        
        try:
            response = requests.get(f"{self.BASE}/works", params=params, timeout=30)
            data = response.json()
            
            results = []
            for work in data.get("results", []):
                results.append({
                    "id": work.get("id"),
                    "title": work.get("title"),
                    "doi": work.get("doi"),
                    "publication_year": work.get("publication_year"),
                    "cited_by_count": work.get("cited_by_count"),
                    "authors": [a.get("author", {}).get("display_name") 
                               for a in work.get("authorships", [])[:5]],
                    "concepts": [c.get("display_name") for c in work.get("concepts", [])[:5]],
                    "host_venue": work.get("host_venue", {}).get("display_name"),
                    "open_access": work.get("open_access", {}).get("is_oa", False)
                })
            
            return results
        except Exception as e:
            print(f"OpenAlex error: {e}")
            return []


class NASAClient:
    """Cliente para NASA Open APIs - LIVRE, sem necessidade de API key"""
    
    APOD = "https://api.nasa.gov/planetary/apod"
    NEO = "https://api.nasa.gov/neo/rest/v1"
    MARS = "https://api.nasa.gov/mars-photos/api/v1"
    IMAGE = "https://images-api.nasa.gov/search"
    
    def __init__(self, api_key: str = "DEMO_KEY"):
        self.api_key = api_key
    
    def get_apod(self) -> Dict:
        """Astronomy Picture of the Day"""
        params = {"api_key": self.api_key}
        try:
            r = requests.get(self.APOD, params=params, timeout=30)
            if r.status_code == 200:
                data = r.json()
                return {
                    "title": data.get("title"),
                    "date": data.get("date"),
                    "explanation": data.get("explanation"),
                    "url": data.get("url"),
                    "hdurl": data.get("hdurl"),
                    "media_type": data.get("media_type")
                }
        except Exception as e:
            print(f"NASA APOD error: {e}")
        return {}
    
    def search_images(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca imagens da NASA"""
        params = {
            "q": query,
            "media_type": "image",
            "page_size": limit
        }
        try:
            r = requests.get(self.IMAGE, params=params, timeout=30)
            if r.status_code == 200:
                data = r.json()
                results = []
                for item in data.get("collection", {}).get("items", []):
                    data_item = item.get("data", [{}])[0]
                    results.append({
                        "title": data_item.get("title"),
                        "description": data_item.get("description"),
                        "date_created": data_item.get("date_created"),
                        "nasa_id": data_item.get("nasa_id"),
                        "keywords": data_item.get("keywords", [])[:5]
                    })
                return results
        except Exception as e:
            print(f"NASA search error: {e}")
        return []


class EuropePMClient:
    """Cliente para Europe PMC - LIVRE, sem autenticação"""
    
    BASE = "https://www.ebi.ac.uk/europepmc/webservices/rest/search"
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca artigos no Europe PMC"""
        params = {
            "query": query,
            "resulttype": "core",
            "format": "json",
            "pageSize": limit
        }
        try:
            r = requests.get(self.BASE, params=params, timeout=30)
            if r.status_code == 200:
                data = r.json()
                results = []
                for hit in data.get("resultList", {}).get("result", []):
                    results.append({
                        "pmid": hit.get("pmid"),
                        "pmcid": hit.get("pmcid"),
                        "doi": hit.get("doi"),
                        "title": hit.get("title"),
                        "author": hit.get("authorString"),
                        "journal": hit.get("journalTitle"),
                        "year": hit.get("pubYear"),
                        "cited_by": hit.get("citedByCount")
                    })
                return results
        except Exception as e:
            print(f"EuropePMC error: {e}")
        return []


class OSFClient:
    """Cliente para Open Science Framework - LIVRE"""
    
    BASE = "https://api.osf.io/v2"
    
    def search_projects(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca projetos no OSF"""
        params = {
            "filter": f"title,contains,{query}",
            "page[size]": limit
        }
        try:
            r = requests.get(f"{self.BASE}/nodes", params=params, timeout=30)
            if r.status_code == 200:
                data = r.json()
                results = []
                for item in data.get("data", []):
                    attrs = item.get("attributes", {})
                    results.append({
                        "id": item.get("id"),
                        "title": attrs.get("title"),
                        "description": attrs.get("description"),
                        "created": attrs.get("date_created"),
                        "modified": attrs.get("date_modified"),
                        "public": attrs.get("public"),
                        "tags": attrs.get("tags", [])
                    })
                return results
        except Exception as e:
            print(f"OSF error: {e}")
        return []


class IBQEDataClient:
    """Cliente para IPEA Dados - API de dados econômicos brasileiros"""
    
    BASE = "http://www.ipeadata.gov.br/api"
    
    def get_series(self, serie_id: str) -> List[Dict]:
        """Obtém série temporal"""
        try:
            response = requests.get(f"{self.BASE}/odata/Serie({serie_id})", 
                                   timeout=30)
            if response.status_code == 200:
                return response.json().get("value", [])
        except Exception as e:
            print(f"IPEA error: {e}")
        return []
    
    def search_series(self, query: str) -> List[Dict]:
        """Busca séries"""
        try:
            q = f"contains(tolower(nome),tolower('{query}'))"
            response = requests.get(f"{self.BASE}/odata/Serie", 
                                   params={"$filter": q},
                                   timeout=30)
            if response.status_code == 200:
                return response.json().get("value", [])
        except Exception as e:
            print(f"IPEA search error: {e}")
        return []
    
    def list_indicators(self, limit: int = 20) -> List[Dict]:
        """Lista indicadores disponíveis"""
        try:
            response = requests.get(f"{self.BASE}/odata/Serie", 
                                   params={"$top": limit},
                                   timeout=30)
            if response.status_code == 200:
                return response.json().get("value", [])
        except Exception as e:
            print(f"IPEA error: {e}")
        return []


class DadosGovClient:
    """Cliente para Dados.gov.br - Portal de dados abertos do Brasil - LIVRE"""
    
    BASE = "https://dados.gov.br/api"
    
    def search_datasets(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca datasets no dados.gov.br"""
        params = {
            "q": query,
            "limit": limit
        }
        try:
            r = requests.get(f"{self.BASE}/3/action/package_search", 
                            params=params, timeout=30)
            if r.status_code == 200:
                data = r.json()
                results = []
                for pkg in data.get("result", {}).get("results", []):
                    results.append({
                        "id": pkg.get("id"),
                        "name": pkg.get("name"),
                        "title": pkg.get("title"),
                        "description": pkg.get("notes", "")[:200],
                        "organization": pkg.get("organization", {}).get("title"),
                        "tags": [t.get("name") for t in pkg.get("tags", [])],
                        "url": pkg.get("url")
                    })
                return results
        except Exception as e:
            print(f"Dados.gov error: {e}")
        return []
    
    def list_categories(self) -> List[Dict]:
        """Lista categorias disponíveis"""
        try:
            r = requests.get(f"{self.BASE}/3/action/organization", timeout=30)
            if r.status_code == 200:
                data = r.json()
                return data.get("result", {}).get("results", [])
        except Exception as e:
            print(f"Dados.gov categories error: {e}")
        return []


class INPEClient:
    """Cliente para INPE - Instituto Nacional de Pesquisas Espaciais - LIVRE"""
    
    BASE = "https://www.inpe.br"
    
    def get_weather(self, city: str = "SaoPaulo") -> Dict:
        """Obtém dados meteorológicos"""
        try:
            r = requests.get(f"{self.BASE}/php/menumeteorologia.php", timeout=30)
            if r.status_code == 200:
                return {"status": "available", "url": self.BASE}
        except Exception as e:
            print(f"INPE error: {e}")
        return {}
    
    def search_products(self, query: str, limit: int = 5) -> List[Dict]:
        """Busca produtos do INPE"""
        try:
            r = requests.get(f"{self.BASE}/servicesISR/search", 
                            params={"q": query, "limit": limit},
                            timeout=30)
            if r.status_code == 200:
                return [{"title": query, "source": "INPE"}]
        except Exception as e:
            print(f"INPE search error: {e}")
        return []


class IBGECatalogClient:
    """Cliente para IBGE API"""
    
    BASE = "https://www.ibge.gov.br/api"
    
    def get_municipios(self) -> List[Dict]:
        """Obtém lista de municípios"""
        response = requests.get(f"{self.BASE}/malhas/v1/municipios", 
                               timeout=60)
        if response.status_code == 200:
            return response.json()
        return []
    
    def search_cities(self, query: str) -> List[Dict]:
        """Busca cidades"""
        response = requests.get(f"{self.BASE}/localidades/municipios",
                               params={"nome": query},
                               timeout=30)
        if response.status_code == 200:
            return response.json()
        return []


class SemanticScholarClient:
    """Cliente para Semantic Scholar API"""
    
    BASE = "https://api.semanticscholar.org/graph/v1"
    
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
    
    def search_papers(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca artigos - retorna vazio se rate limited (use API key para evitar)"""
        params = {
            "query": query,
            "limit": limit,
            "fields": "title,authors,year,citationCount,venue,openAccessPdf,externalIds"
        }
        
        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key
            print(f"Using Semantic Scholar with API key")
        else:
            print(f"Note: Semantic Scholar requires API key for consistent access. Get one at https://api.semanticscholar.org/")
        
        try:
            response = requests.get(f"{self.BASE}/paper/search", 
                                   params=params, headers=headers, timeout=30)
            
            if response.status_code == 429:
                print("Semantic Scholar rate limited (no API key). Use OpenAlex/CrossRef instead.")
                return []
            
            if response.status_code == 200:
                data = response.json()
                return data.get("data", [])
        except Exception as e:
            print(f"Semantic Scholar error: {e}")
        
        return []
    
    def get_paper(self, paper_id: str) -> Optional[Dict]:
        """Obtém artigo por ID"""
        params = {
            "fields": "title,authors,year,citationCount,venue,abstract,openAccessPdf,externalIds"
        }
        
        headers = {}
        if self.api_key:
            headers["x-api-key"] = self.api_key
        
        response = requests.get(f"{self.BASE}/paper/{paper_id}", 
                               params=params, headers=headers, timeout=30)
        
        if response.status_code == 200:
            return response.json()
        return None


class BioRxivClient:
    """Cliente para bioRxiv (preprints biológicos)"""
    
    BASE = "https://api.biorxiv.org/details/"
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca preprints no bioRxiv"""
        results = []
        try:
            response = requests.get(
                f"{self.BASE}bioRxiv/{query}",
                params={"limit": limit, "format": "json"},
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                for item in data.get("collection", [])[:limit]:
                    results.append({
                        "id": item.get("doi"),
                        "title": item.get("title"),
                        "abstract": item.get("abstract"),
                        "authors": item.get("authors"),
                        "published": item.get("date_of_publication"),
                        "doi": item.get("doi"),
                        "url": item.get("url"),
                        "source": "biorxiv"
                    })
        except Exception as e:
            print(f"bioRxiv error: {e}")
        return results


class MedRxivClient:
    """Cliente para medRxiv (preprints de saúde)"""
    
    BASE = "https://api.biorxiv.org/details/"
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca preprints no medRxiv"""
        results = []
        try:
            response = requests.get(
                f"{self.BASE}medRxiv/{query}",
                params={"limit": limit, "format": "json"},
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                for item in data.get("collection", [])[:limit]:
                    results.append({
                        "id": item.get("doi"),
                        "title": item.get("title"),
                        "abstract": item.get("abstract"),
                        "authors": item.get("authors"),
                        "published": item.get("date_of_publication"),
                        "doi": item.get("doi"),
                        "url": item.get("url"),
                        "source": "medrxiv"
                    })
        except Exception as e:
            print(f"medRxiv error: {e}")
        return results


class DBLPClient:
    """Cliente para DBLP (Computer Science Bibliography)"""
    
    BASE = "https://dblp.org/search/publ/api"
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca artigos no DBLP"""
        results = []
        try:
            params = {
                "q": query,
                "h": limit,
                "format": "json"
            }
            response = requests.get(self.BASE, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                for hit in data.get("result", {}).get("hits", {}).get("hit", [])[:limit]:
                    info = hit.get("info", {})
                    results.append({
                        "id": info.get("key"),
                        "title": info.get("title"),
                        "authors": [a.get("text", "") for a in info.get("authors", {}).get("author", [])],
                        "year": info.get("year"),
                        "venue": info.get("venue"),
                        "type": info.get("type"),
                        "doi": info.get("doi"),
                        "ee": info.get("ee"),
                        "source": "dblp"
                    })
        except Exception as e:
            print(f"DBLP error: {e}")
        return results


class PhilPapersClient:
    """Cliente para PhilPapers (Filosofia)"""
    
    BASE = "https://philpapers.org/api/v1"
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca artigos no PhilPapers"""
        results = []
        try:
            params = {"q": query, "limit": limit}
            response = requests.get(f"{self.BASE}/search", params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                for item in data.get("results", [])[:limit]:
                    results.append({
                        "id": item.get("id"),
                        "title": item.get("title"),
                        "authors": item.get("authors"),
                        "abstract": item.get("abstract"),
                        "year": item.get("year"),
                        "source": "philpapers"
                    })
        except Exception as e:
            try:
                results = self._fallback_scraper(query, limit)
            except:
                print(f"PhilPapers error: {e}")
        return results
    
    def _fallback_scraper(self, query: str, limit: int) -> List[Dict]:
        """Fallback via scraping"""
        from bs4 import BeautifulSoup
        results = []
        try:
            response = requests.get(
                f"https://philpapers.org/s/{query}",
                params={"q": query},
                timeout=30
            )
            soup = BeautifulSoup(response.text, "html.parser")
            for item in soup.select("div.rslt")[:limit]:
                title_elem = item.select_one("a.rslt_ttl")
                if title_elem:
                    results.append({
                        "title": title_elem.get_text(strip=True),
                        "url": f"https://philpapers.org{title_elem.get('href')}",
                        "source": "philpapers"
                    })
        except ImportError:
            pass
        except Exception as e:
            print(f"PhilPapers scraper error: {e}")
        return results


class KaggleClient:
    """Cliente para Kaggle Datasets"""
    
    BASE = "https://www.kaggle.com/api/v1/datasets/list"
    
    def __init__(self, api_key: str = ""):
        self.api_key = api_key
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca datasets no Kaggle"""
        if not self.api_key:
            print("Kaggle requires API key. Get one from Kaggle account settings.")
            return []
        
        results = []
        try:
            params = {"search": query, "page_size": limit}
            headers = {"Authorization": f"Bearer {self.api_key}"}
            response = requests.get(self.BASE, params=params, headers=headers, timeout=30)
            if response.status_code == 200:
                data = response.json()
                for item in data.get("data", [])[:limit]:
                    results.append({
                        "id": item.get("ref"),
                        "title": item.get("title"),
                        "description": item.get("description"),
                        "size": item.get("size"),
                        "downloads": item.get("downloadCount"),
                        "votes": item.get("voteCount"),
                        "tags": item.get("keywords"),
                        "source": "kaggle"
                    })
        except Exception as e:
            print(f"Kaggle error: {e}")
        return results


class HuggingFaceClient:
    """Cliente para Hugging Face Datasets"""
    
    BASE = "https://huggingface.co/api/datasets"
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca datasets no Hugging Face"""
        results = []
        try:
            params = {"search": query, "full": "true", "limit": limit}
            response = requests.get(self.BASE, params=params, timeout=30)
            if response.status_code == 200:
                for item in response.json()[:limit]:
                    results.append({
                        "id": item.get("id"),
                        "title": item.get("id"),
                        "author": item.get("author"),
                        "downloads": item.get("downloads"),
                        "likes": item.get("likes"),
                        "tags": item.get("tags"),
                        "source": "huggingface"
                    })
        except Exception as e:
            print(f"HuggingFace error: {e}")
        return results
    
    def search_models(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca modelos no Hugging Face"""
        results = []
        try:
            params = {"search": query, "limit": limit}
            response = requests.get("https://huggingface.co/api/models", params=params, timeout=30)
            if response.status_code == 200:
                for item in response.json()[:limit]:
                    results.append({
                        "id": item.get("modelId"),
                        "author": item.get("author"),
                        "downloads": item.get("downloads"),
                        "likes": item.get("likes"),
                        "tags": item.get("tags"),
                        "source": "huggingface_models"
                    })
        except Exception as e:
            print(f"HuggingFace models error: {e}")
        return results


class COREClient:
    """Cliente para CORE ( agregador open access)"""
    
    BASE = "https://api.core.edu.au/v1"
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca no CORE"""
        results = []
        try:
            params = {"q": query, "limit": limit}
            response = requests.get(f"{self.BASE}/papers/search", params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                for item in data.get("data", [])[:limit]:
                    results.append({
                        "id": item.get("oai_id"),
                        "title": item.get("title"),
                        "abstract": item.get("abstract"),
                        "authors": item.get("authors"),
                        "year": item.get("published_year"),
                        "doi": item.get("doi"),
                        "venue": item.get("venue"),
                        "source": "core"
                    })
        except Exception as e:
            print(f"CORE error: {e}")
        return results


class UnpaywallClient:
    """Cliente para Unpaywall (verifica open access)"""
    
    BASE = "https://api.unpaywall.org/v2"
    
    def __init__(self, email: str = ""):
        self.email = email or "research@example.com"
    
    def check_oa(self, doi: str) -> Dict:
        """Verifica se artigo é open access"""
        try:
            response = requests.get(
                f"{self.BASE}/{doi}",
                params={"email": self.email},
                timeout=30
            )
            if response.status_code == 200:
                data = response.json()
                return {
                    "doi": doi,
                    "is_oa": data.get("is_oa", False),
                    "best_oa_location": data.get("best_oa_location", {}),
                    "host_venue": data.get("host_venue", {}),
                    "published_date": data.get("published_date"),
                    "journal_issns": data.get("journal_issns")
                }
        except Exception as e:
            print(f"Unpaywall error: {e}")
        return {"doi": doi, "is_oa": False}


class ProjectGutenbergClient:
    """Cliente para Project Gutenberg (livros)"""
    
    BASE = "https://gutendex.com"
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca livros no Gutenberg"""
        results = []
        try:
            params = {"search": query}
            response = requests.get(f"{self.BASE}/books", params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                for item in data.get("results", [])[:limit]:
                    results.append({
                        "id": item.get("id"),
                        "title": item.get("title"),
                        "authors": [a.get("name") for a in item.get("authors", [])],
                        " subjects": item.get("subjects"),
                        "bookshelves": item.get("bookshelves"),
                        "languages": item.get("languages"),
                        "copyright": item.get("copyright"),
                        "source": "gutenberg"
                    })
        except Exception as e:
            print(f"Gutenberg error: {e}")
        return results


class OSFProjectsClient:
    """Cliente para OSF Projects"""
    
    BASE = "https://api.osf.io/v2"
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca projetos no OSF"""
        results = []
        try:
            params = {"filter[title]": query, "page[size]": limit}
            response = requests.get(f"{self.BASE}/registrations/", params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                for item in data.get("data", [])[:limit]:
                    attrs = item.get("attributes", {})
                    results.append({
                        "id": item.get("id"),
                        "title": attrs.get("title"),
                        "description": attrs.get("description"),
                        "category": attrs.get("category"),
                        "date_created": attrs.get("date_created"),
                        "source": "osf"
                    })
        except Exception as e:
            print(f"OSF Projects error: {e}")
        return results


class DOAJClient:
    """Cliente para Directory of Open Access Journals"""
    
    BASE = "https://doaj.org/api/v2"
    
    def search_articles(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca artigos no DOAJ"""
        params = {
            "query": query,
            "pageSize": limit
        }
        
        try:
            response = requests.get(f"{self.BASE}/articles", params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data.get("items", []):
                    results.append({
                        "id": item.get("id"),
                        "title": item.get("title"),
                        "abstract": item.get("abstract"),
                        "authors": [a.get("name") for a in item.get("authors", [])],
                        "published_date": item.get("published_date"),
                        "journal": item.get("journal", {}).get("title"),
                        "doi": item.get("doi"),
                        "issn": item.get("journal", {}).get("issn")
                    })
                return results
        except Exception as e:
            print(f"DOAJ error: {e}")
        return []
    
    def search_journals(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca periódicos no DOAJ"""
        params = {
            "query": query,
            "pageSize": limit
        }
        
        try:
            response = requests.get(f"{self.BASE}/journals", params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data.get("items", []):
                    results.append({
                        "id": item.get("id"),
                        "title": item.get("title"),
                        "issn": item.get("issn"),
                        "publisher": item.get("publisher"),
                        "country": item.get("country"),
                        "languages": item.get("languages"),
                        "apc": item.get("apc")
                    })
                return results
        except Exception as e:
            print(f"DOAJ journals error: {e}")
        return []


class SSRNClient:
    """Cliente para SSRN (Social Science Research Network)"""
    
    BASE = "https://papers.ssrn.com/sol3/papers.cfm"
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca artigos no SSRN via scraping"""
        import re
        
        params = {
            "abstractsearch": query,
            "ssrn宮殿": limit
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36"
        }
        
        try:
            response = requests.get(self.BASE, params=params, headers=headers, timeout=30)
            if response.status_code == 200:
                papers = []
                title_pattern = r'<a[^>]*href="/sol3/Delivery\.cfm/([^"]+)"[^>]*>([^<]+)</a>'
                author_pattern = r'Authors:*\s*<a[^>]*>([^<]+)</a>'
                
                for match in re.finditer(title_pattern, response.text)[:limit]:
                    papers.append({
                        "id": match.group(1),
                        "title": match.group(2).strip(),
                        "url": f"https://papers.ssrn.com/sol3/Delivery.cfm/{match.group(1)}"
                    })
                return papers
        except Exception as e:
            print(f"SSRN error: {e}")
        return []


class ACLAnthologyClient:
    """Cliente para ACL Anthology (NLP/CL papers)"""
    
    BASE = "https://aclanthology.org"
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca artigos na ACL Anthology"""
        params = {
            "q": query,
            "max_results": limit
        }
        
        try:
            response = requests.get(f"{self.BASE}/search/", params=params, timeout=30)
            if response.status_code == 200:
                from bs4 import BeautifulSoup
                soup = BeautifulSoup(response.text, "html.parser")
                
                results = []
                for paper in soup.select("p.result")[:limit]:
                    title_elem = paper.select_one("a.result-title")
                    if title_elem:
                        results.append({
                            "title": title_elem.get_text(strip=True),
                            "url": f"{self.BASE}{title_elem.get('href')}",
                            "venue": paper.select_one("span.venue").get_text(strip=True) if paper.select_one("span.venue") else "",
                            "year": paper.select_one("span.year").get_text(strip=True) if paper.select_one("span.year") else ""
                        })
                return results
        except ImportError:
            print("BeautifulSoup not installed. Install with: pip install beautifulsoup4")
        except Exception as e:
            print(f"ACL Anthology error: {e}")
        return []


class ERICClient:
    """Cliente para ERIC (Education Resources Information Center)"""
    
    BASE = "https://api.eric.ed.gov"
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca artigos no ERIC"""
        params = {
            "search": query,
            "rows": limit,
            "format": "json"
        }
        
        try:
            response = requests.get(self.BASE, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data.get("response", {}).get("docs", []):
                    results.append({
                        "id": item.get("id"),
                        "title": item.get("title"),
                        "authors": item.get("authors"),
                        "description": item.get("description"),
                        "publication_date": item.get("publication_date"),
                        "eric_id": item.get("eric_id"),
                        "url": item.get("url")
                    })
                return results
        except Exception as e:
            print(f"ERIC error: {e}")
        return []


class IEEEClient:
    """Cliente para IEEE Xplore (requer API key)"""
    
    BASE = "https://ieeexploreapi.ieee.org/api/v1/search/articles"
    
    def __init__(self, api_key: str = None):
        self.api_key = api_key
    
    def search(self, query: str, max_results: int = 10) -> List[Dict]:
        """Busca artigos no IEEE Xplore"""
        if not self.api_key:
            print("IEEE API requires API key. Get one at https://developer.ieee.org/")
            return []
        
        params = {
            "apikey": self.api_key,
            "article_number": max_results,
            "query_text": query
        }
        
        try:
            response = requests.get(self.BASE, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                results = []
                for item in data.get("articles", []):
                    results.append({
                        "title": item.get("title"),
                        "doi": item.get("doi"),
                        "authors": [a.get("full_name") for a in item.get("authors", [])],
                        "publication_year": item.get("publication_year"),
                        "conference": item.get("conference_title"),
                        "journal": item.get("journal_title")
                    })
                return results
        except Exception as e:
            print(f"IEEE error: {e}")
        return []


class NatureClient:
    """Cliente para Nature journals via scraping"""
    
    BASE = "https://www.nature.com"
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca artigos no Nature.com"""
        params = {
            "q": query,
            "limit": limit
        }
        
        headers = {
            "User-Agent": "Mozilla/5.0"
        }
        
        try:
            response = requests.get(f"{self.BASE}/search", params=params, headers=headers, timeout=30)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            
            results = []
            for article in soup.select("article")[:limit]:
                title_elem = article.select_one("h3 a")
                results.append({
                    "title": title_elem.get_text(strip=True) if title_elem else "",
                    "url": f"{self.BASE}{title_elem.get('href')}" if title_elem else "",
                    "journal": article.select_one("[data-testid='article-meta']").get_text(strip=True) if article.select_one("[data-testid='article-meta']") else ""
                })
            return results
        except ImportError:
            print("BeautifulSoup needed for Nature scraper")
        except Exception as e:
            print(f"Nature error: {e}")
        return []


class ScienceClient:
    """Cliente para Science journals via scraping"""
    
    BASE = "https://www.science.org"
    
    def search(self, query: str, limit: int = 10) -> List[Dict]:
        """Busca artigos no Science.org"""
        params = {
            "q": query,
            "size": limit
        }
        
        headers = {"User-Agent": "Mozilla/5.0"}
        
        try:
            response = requests.get(f"{self.BASE}/search", params=params, headers=headers, timeout=30)
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(response.text, "html.parser")
            
            results = []
            for article in soup.select("article")[:limit]:
                title_elem = article.select_one("h3 a")
                results.append({
                    "title": title_elem.get_text(strip=True) if title_elem else "",
                    "url": f"{self.BASE}{title_elem.get('href')}" if title_elem else "",
                    "authors": article.select_one(".authors").get_text(strip=True) if article.select_one(".authors") else ""
                })
            return results
        except ImportError:
            pass
        except Exception as e:
            print(f"Science error: {e}")
        return []


class AcademicAPIFacade:
    """
    Fachada unificada para todas as APIs acadêmicas
    """
    
    def __init__(self):
        self.arxiv = ArxivClient()
        self.scielo = ScieloClient()
        self.pubmed = PubmedClient()
        self.openalex = OpenAlexClient()
        self.crossref = CrossrefClient()
        self.ipeadata = IBQEDataClient()
        self.ibge = IBGECatalogClient()
        self.semantic_scholar = SemanticScholarClient()
        self.nasa = NASAClient()
        self.europe_pmc = EuropePMClient()
        self.osf = OSFClient()
        self.dadosgov = DadosGovClient()
        self.inpe = INPEClient()
        self.doaj = DOAJClient()
        self.ssrn = SSRNClient()
        self.acl_anthology = ACLAnthologyClient()
        self.eric = ERICClient()
        self.ieee = IEEEClient()
        self.nature = NatureClient()
        self.science = ScienceClient()
    
    def search_all(self, query: str, limit_per_source: int = 5) -> Dict[str, List[Dict]]:
        """
        Busca em todas as fontes disponíveis
        Retorna dicionário com resultados por fonte
        """
        results = {
            "arxiv": [],
            "crossref": [],
            "openalex": [],
            "pubmed_ids": [],
            "europe_pmc": [],
            "scielo": [],
            "dadosgov": [],
            "osf": [],
            "doaj": [],
            "ssrn": [],
            "acl_anthology": [],
            "eric": [],
            "query": query,
            "timestamp": datetime.now().isoformat()
        }
        
        try:
            results["arxiv"] = self.arxiv.search(query, max_results=limit_per_source)
        except Exception as e:
            print(f"arXiv error: {e}")
        
        try:
            results["crossref"] = self.crossref.search(query, limit=limit_per_source)
        except Exception as e:
            print(f"CrossRef error: {e}")
        
        try:
            results["openalex"] = self.openalex.search_works(query, limit=limit_per_source)
        except Exception as e:
            print(f"OpenAlex error: {e}")
        
        try:
            results["pubmed_ids"] = self.pubmed.search(query, max_results=limit_per_source)
        except Exception as e:
            print(f"PubMed error: {e}")
        
        try:
            results["europe_pmc"] = self.europe_pmc.search(query, limit=limit_per_source)
        except Exception as e:
            print(f"EuropePMC error: {e}")
        
        try:
            results["scielo"] = self.scielo.search_articles(query, limit=limit_per_source)
        except Exception as e:
            print(f"SciELO error: {e}")
        
        try:
            results["dadosgov"] = self.dadosgov.search_datasets(query, limit=limit_per_source)
        except Exception as e:
            print(f"Dados.gov error: {e}")
        
        try:
            results["osf"] = self.osf.search_projects(query, limit=limit_per_source)
        except Exception as e:
            print(f"OSF error: {e}")
        
        try:
            results["doaj"] = self.doaj.search_articles(query, limit=limit_per_source)
        except Exception as e:
            print(f"DOAJ error: {e}")
        
        try:
            results["ssrn"] = self.ssrn.search(query, limit=limit_per_source)
        except Exception as e:
            print(f"SSRN error: {e}")
        
        try:
            results["acl_anthology"] = self.acl_anthology.search(query, limit=limit_per_source)
        except Exception as e:
            print(f"ACL Anthology error: {e}")
        
        try:
            results["eric"] = self.eric.search(query, limit=limit_per_source)
        except Exception as e:
            print(f"ERIC error: {e}")
        
        return results
    
    def get_geospatial_datasets(self) -> Dict:
        """
        Retorna datasets geoespaciais disponíveis
        """
        return {
            "ibge": {
                "shapefiles": {
                    "url": "https://www.ibge.gov.br/geociencias/downloads-geociencias.html",
                    "description": "Shapefiles de limites administrativos",
                    "formats": ["shp", "geojson", "kml"]
                },
                "municipios": {
                    "url": "https://www.ibge.gov.br/geociencias-2/10940-mapas-e-geodata/shape/15165-municipios.html",
                    "description": "Municípios brasileiros",
                    "formats": ["shp", "geojson"]
                }
            },
            "inpe": {
                "sentinel": {
                    "url": "https://www.inpe.br/shape/",
                    "description": "Imagens Sentinel",
                    "formats": ["tiff", "jp2"]
                },
                "landsat": {
                    "url": "https://www.inpe.br/shape/",
                    "description": "Imagens Landsat",
                    "formats": ["tiff"]
                }
            }
        }


def main():
    """Teste dos clientes"""
    facade = AcademicAPIFacade()
    
    print("=" * 60)
    print("MASWOS Academic API Client - Teste")
    print("=" * 60)
    
    query = "machine learning"
    print(f"\nBuscando: '{query}'")
    
    results = facade.search_all(query, limit_per_source=3)
    
    print(f"\nResultados por fonte:")
    for source, items in results.items():
        if isinstance(items, list):
            print(f"  {source}: {len(items)} itens")
        else:
            print(f"  {source}: {items}")
    
    print("\n" + "=" * 60)
    print("Datasets geoespaciais disponíveis:")
    print("=" * 60)
    geo = facade.get_geospatial_datasets()
    for source, datasets in geo.items():
        print(f"\n{source.upper()}:")
        for name, info in datasets.items():
            print(f"  - {name}: {info['description']}")


if __name__ == "__main__":
    main()
