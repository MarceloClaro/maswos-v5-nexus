#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - World Bank Documents & Reports Scraper

API Documentation: https://documents.worldbank.org/en/publication/documents-reports/api
Base URL: https://search.worldbank.org/api/v3/wds
Acesso: Gratuito, sem API key
Conteúdo: ~400K documentos (relatórios, projetos, Avaliações Ambientais e Sociais, etc.)

Endpoints principais:
- Busca de documentos: /api/v3/wds
- Detalhes do documento: /api/v3/documents/{id}
- Download PDF: url ou pdfurl dos metadados

Arquitetura: Transformer-Agentes (Encoder → API → Parser → Decoder)
"""

import requests
import time
import json
import os
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
from urllib.parse import quote, urlencode
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass
class WorldBankDocument:
    """Documento do World Bank"""
    id: str = ""
    title: str = ""
    abstract: str = ""
    doc_type: str = ""
    doc_type_major: str = ""
    date: str = ""
    country: List[str] = field(default_factory=list)
    country_code: List[str] = field(default_factory=list)
    region: str = ""
    authors: List[str] = field(default_factory=list)
    report_number: str = ""
    report_name: str = ""
    document_name: str = ""
    url: str = ""
    pdf_url: str = ""
    txt_url: str = ""
    language: List[str] = field(default_factory=list)
    keywords: List[str] = field(default_factory=list)
    themes: List[str] = field(default_factory=list)
    project_id: str = ""
    project_name: str = ""
    collection: str = ""
    volume_number: int = 0
    total_volumes: int = 0
    source: str = "worldbank_docs"


class WorldBankDocumentsScraper:
    """
    Scraper para World Bank Documents & Reports API
    
    Conforme documentação:
    - Base URL: https://search.worldbank.org/api/v3/wds
    - Formato: JSON ou XML
    - Rate Limit: Sem limite documentado (uso razoável)
    - Autenticação: Não requerida
    """
    
    BASE_URL = "https://search.worldbank.org/api/v3/wds"
    DOC_URL = "https://search.worldbank.org/api/v3/documents"
    
    # Tipos de documentos comuns
    DOC_TYPES = [
        "Project Appraisal Document",
        "Implementation Completion and Results Report", 
        "Project Information Document",
        "Environmental and Social Framework",
        "Evaluation Report",
        "Strategy Paper",
        "Economic and Sector Work",
        "Research Report",
        "Policy Research Working Paper",
        "Country Economic Memorandum",
        "Poverty Assessment",
        "Public Investment Review"
    ]
    
    # Países principais (ISO codes)
    COUNTRIES = {
        "BR": "Brazil",
        "CN": "China", 
        "IN": "India",
        "RU": "Russia",
        "ZA": "South Africa",
        "MX": "Mexico",
        "AR": "Argentina",
        "CO": "Colombia",
        "PE": "Peru",
        "CL": "Chile"
    }
    
    def __init__(self, delay: float = 0.5):
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "MASWOS-WorldBank-Docs/1.0",
            "Accept": "application/json"
        })
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def search(self, query: str, rows: int = 20, offset: int = 0,
               country: str = None, doc_type: str = None,
               date_start: str = None, date_end: str = None,
               language: str = None, topic: str = None,
               theme: str = None, format: str = "json") -> Dict:
        """
        Buscar documentos no World Bank
        
        Args:
            query: Termo de busca (qterm)
            rows: Número de resultados por página (default: 10, máx: 1000)
            offset: Offset para paginação (começa em 0)
            country: Filtro por país (nome ou código ISO)
            doc_type: Tipo de documento
            date_start: Data inicial (YYYY-MM-DD ou MM-DD-YYYY)
            date_end: Data final (YYYY-MM-DD ou MM-DD-YYYY)
            language: Idioma (ex: English, Spanish, French)
            topic: Tópico
            theme: Tema
            format: Formato de saída (json ou xml)
        
        Returns:
            Dict com documentos encontrados
        """
        self._rate_limit()
        
        params = {
            "format": format,
            "qterm": query,
            "rows": min(rows, 1000),
            "os": offset
        }
        
        # Campos a retornar
        fields = [
            "id", "display_title", "abstracts", "docty", "majdocty",
            "docdt", "count", "countrycode", "geo_reg", "authr",
            "repnb", "repnme", "docna", "url", "pdfurl", "txturl",
            "lang", "keywd", "theme", "majtheme", "projectid", "projn",
            "colti", "volnb", "totvolnb"
        ]
        params["fl"] = ",".join(fields)
        
        # Filtros opcionais
        if country:
            params["count_exact"] = country
        if doc_type:
            params["docty_exact"] = doc_type
        if date_start:
            params["strdate"] = date_start
        if date_end:
            params["enddate"] = date_end
        if language:
            params["lang_exact"] = language
        if topic:
            params["topic_exact"] = topic
        if theme:
            params["theme_exact"] = theme
        
        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=60)
            
            if response.status_code == 200:
                return self._parse_search_response(response.json())
            else:
                print(f"[WorldBank-Docs] HTTP {response.status_code}")
                return {"documents": [], "total": 0, "source": "worldbank_docs_error"}
                
        except Exception as e:
            print(f"[WorldBank-Docs ERROR] {e}")
            return {"documents": [], "total": 0, "source": "worldbank_docs_exception"}
    
    def search_by_country(self, country_code: str, rows: int = 50, 
                          doc_type: str = None) -> Dict:
        """Buscar documentos por país"""
        return self.search(
            query="*:*",
            rows=rows,
            country=country_code,
            doc_type=doc_type
        )
    
    def search_projects(self, query: str, country: str = None,
                        limit: int = 20) -> Dict:
        """Buscar projetos do World Bank"""
        return self.search(
            query=query,
            rows=limit,
            country=country,
            doc_type="Project Appraisal Document"
        )
    
    def search_evaluation_reports(self, query: str = "*", 
                                  country: str = None,
                                  limit: int = 20) -> Dict:
        """Buscar relatórios de avaliação"""
        return self.search(
            query=query,
            rows=limit,
            country=country,
            doc_type="Implementation Completion and Results Report"
        )
    
    def search_policies(self, query: str, limit: int = 20) -> Dict:
        """Buscar documentos de política"""
        return self.search(
            query=query,
            rows=limit,
            doc_type="Policy Research Working Paper"
        )
    
    def get_document(self, doc_id: str) -> Optional[Dict]:
        """Obter detalhes de um documento específico"""
        self._rate_limit()
        
        url = f"{self.DOC_URL}/{doc_id}"
        params = {"format": "json"}
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                docs = data.get("documents", [])
                if docs:
                    return self._parse_document(docs[0])
            return None
        except Exception as e:
            print(f"[WorldBank-Docs ERROR] {e}")
            return None
    
    def get_facets(self, facet_fields: List[str] = None) -> Dict:
        """Obter valores de facets (estatísticas)"""
        self._rate_limit()
        
        if not facet_fields:
            facet_fields = ["count_exact", "docty_exact", "lang_exact", "theme_exact"]
        
        params = {
            "format": "json",
            "fct": ",".join(facet_fields),
            "rows": 0
        }
        
        try:
            response = self.session.get(self.BASE_URL, params=params, timeout=30)
            if response.status_code == 200:
                return response.json()
            return {}
        except Exception as e:
            print(f"[WorldBank-Docs ERROR] {e}")
            return {}
    
    def get_countries_facets(self) -> List[str]:
        """Obter lista de países disponíveis"""
        facets = self.get_facets(["count_exact"])
        countries = []
        if "facets" in facets:
            for facet in facets["facets"]:
                if facet.get("name") == "count_exact":
                    countries = [f["value"] for f in facet.get("facets", [])]
        return countries
    
    def get_document_types(self) -> List[str]:
        """Obter tipos de documentos disponíveis"""
        facets = self.get_facets(["docty_exact"])
        doc_types = []
        if "facets" in facets:
            for facet in facets["facets"]:
                if facet.get("name") == "docty_exact":
                    doc_types = [f["value"] for f in facet.get("facets", [])]
        return doc_types
    
    def _parse_search_response(self, data: Dict) -> Dict:
        """Parser para resposta de busca"""
        documents = []
        total = data.get("total", 0)
        
        # Documents is a dict where keys are document IDs
        docs_dict = data.get("documents", {})
        if isinstance(docs_dict, dict):
            for doc_id, doc_data in docs_dict.items():
                if isinstance(doc_data, dict) and doc_id != "facets":
                    doc = self._parse_document(doc_data)
                    documents.append(doc)
        
        return {
            "documents": documents,
            "total": total,
            "source": "worldbank_docs"
        }
    
    def _parse_document(self, item: Dict) -> Dict:
        """Parser para documento"""
        def ensure_list(value):
            """Ensure value is a list"""
            if value is None:
                return []
            if isinstance(value, str):
                return [value]
            if isinstance(value, list):
                return value
            return [str(value)]
        
        def ensure_str(value, default=""):
            """Ensure value is a string"""
            if value is None:
                return default
            if isinstance(value, (list, dict)):
                return str(value) if value else default
            return str(value)
        
        # Extrair países
        countries = ensure_list(item.get("count"))
        
        # Extrair códigos de país
        country_codes = ensure_list(item.get("countrycode"))
        
        # Extrair autores
        authors = ensure_list(item.get("authr"))
        
        # Extrair idiomas
        languages = ensure_list(item.get("lang"))
        
        # Extrair keywords
        keywords = ensure_list(item.get("keywd"))
        
        # Extrair temas
        themes = ensure_list(item.get("theme"))
        major_themes = ensure_list(item.get("majtheme"))
        all_themes = list(set(themes + major_themes))
        
        # URL do documento
        doc_url = ensure_str(item.get("url"))
        doc_id = ensure_str(item.get("id"))
        if not doc_url and doc_id:
            doc_url = f"https://documents.worldbank.org/en/publication/documents-reports/document/{doc_id}"
        
        # Data do documento
        doc_date = ensure_str(item.get("docdt"))
        
        return {
            "id": doc_id,
            "title": ensure_str(item.get("display_title")),
            "abstract": ensure_str(item.get("abstracts")),
            "doc_type": ensure_str(item.get("docty")),
            "doc_type_major": ensure_str(item.get("majdocty")),
            "date": doc_date[:10] if doc_date else "",
            "country": countries,
            "country_code": country_codes,
            "region": ensure_str(item.get("geo_reg")),
            "authors": authors,
            "report_number": ensure_str(item.get("repnb")),
            "report_name": ensure_str(item.get("repnme")),
            "document_name": ensure_str(item.get("docna")),
            "url": doc_url,
            "pdf_url": ensure_str(item.get("pdfurl")),
            "txt_url": ensure_str(item.get("txturl")),
            "language": languages,
            "keywords": keywords,
            "themes": all_themes,
            "project_id": ensure_str(item.get("projectid")),
            "project_name": ensure_str(item.get("projn")),
            "collection": ensure_str(item.get("colti")),
            "volume_number": int(item.get("volnb") or 0),
            "total_volumes": int(item.get("totvolnb") or 0),
            "source": "worldbank_docs"
        }
    
    def download_pdf(self, pdf_url: str, output_path: str = None) -> Optional[bytes]:
        """Download de PDF do documento"""
        self._rate_limit()
        
        try:
            response = self.session.get(pdf_url, timeout=120)
            if response.status_code == 200:
                if output_path:
                    with open(output_path, 'wb') as f:
                        f.write(response.content)
                return response.content
            return None
        except Exception as e:
            print(f"[WorldBank-Docs] Download error: {e}")
            return None


# Funções de conveniência
def search_worldbank_documents(query: str, max_results: int = 20,
                               country: str = None) -> List[Dict]:
    """Buscar documentos no World Bank"""
    scraper = WorldBankDocumentsScraper()
    result = scraper.search(query, rows=max_results, country=country)
    return result.get("documents", [])

def get_worldbank_document(doc_id: str) -> Optional[Dict]:
    """Obter documento específico"""
    scraper = WorldBankDocumentsScraper()
    return scraper.get_document(doc_id)


# Testes
def test_worldbank_documents():
    """Testar scraper de documentos do World Bank"""
    print("=" * 70)
    print("MASWOS V5 NEXUS - World Bank Documents API Test")
    print("=" * 70)
    
    scraper = WorldBankDocumentsScraper()
    
    # Test 1: Busca geral
    print("\n[TEST 1] Busca: 'climate change'")
    result = scraper.search("climate change", rows=5)
    print(f"  Total encontrado: {result['total']}")
    print(f"  Documentos recuperados: {len(result['documents'])}")
    
    for i, doc in enumerate(result['documents'][:3], 1):
        print(f"\n  Doc {i}:")
        print(f"    Título: {doc['title'][:60]}...")
        print(f"    Tipo: {doc['doc_type']}")
        print(f"    Data: {doc['date'][:10] if doc['date'] else 'N/A'}")
        print(f"    País: {', '.join(doc['country'][:2])}")
    
    # Test 2: Busca por país
    print("\n[TEST 2] Documentos do Brasil")
    result = scraper.search_by_country("BRA", rows=3)
    print(f"  Total: {result['total']}")
    for doc in result['documents'][:2]:
        print(f"  - {doc['title'][:50]}...")
    
    # Test 3: Tipos de documentos
    print("\n[TEST 3] Tipos de documentos disponíveis")
    types = scraper.get_document_types()
    for t in types[:10]:
        print(f"  - {t}")
    
    print("\n" + "=" * 70)
    print("World Bank Documents - Testes Concluídos")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    test_worldbank_documents()
