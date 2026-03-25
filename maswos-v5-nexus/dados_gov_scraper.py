#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - dados.gov.br Official Scraper
Portal de Dados Abertos do Governo Federal Brasileiro

API Base: https://dados.gov.br
Documentação: https://dados.gov.br/swagger-ui/index.html

SDK Reference: https://pypi.org/project/dados-gov-sdk/

⚠️ IMPORTANTE - AUTHENTICATION REQUIRED:
O portal dados.gov.br requer autenticação para acesso à API.
Para obter uma API key/credenciais:
1. Registre-se em: https://dados.gov.br/usuario/registrar
2. Acesse: https://dados.gov.br/usuario/perfil para gerar API key
3. Use a API key via parâmetro api_key ou variável de ambiente DADOS_GOV_API_KEY

Arquitetura: Transformer-Agentes (Encoder → API → Parser → Decoder)

Fallback Strategy:
1. API Pública com autenticação (principal)
2. API CKAN (alternativa)
3. Web Scraping (último recurso, sem necessidade de auth)
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
class DadosGovDataset:
    """Dataset do dados.gov.br"""
    id: str = ""
    title: str = ""
    description: str = ""
    organization: str = ""
    organization_title: str = ""
    tags: List[str] = field(default_factory=list)
    resources: List[Dict] = field(default_factory=list)
    themes: List[str] = field(default_factory=list)
    created: str = ""
    modified: str = ""
    frequency: str = ""
    license: str = ""
    url: str = ""
    spatial_area: str = ""
    temporal_coverage: str = ""
    metadata_modified: str = ""
    num_resources: int = 0
    num_tags: int = 0
    source: str = "dados.gov.br"


class DadosGovScraper:
    """
    Scraper oficial para Portal de Dados Abertos (dados.gov.br)
    
    Conforme API documentação:
    - Base URL: https://dados.gov.br
    - Autenticação: OAuth / API Key (token)
    - Formato: JSON
    
    Endpoints disponíveis:
    - /dados/api/publico/conjuntos-dados - Listar datasets públicos
    - /dados/api/publico/conjuntos-dados/{id} - Detalhes do dataset
    - /dados/api/publico/organizacoes - Listar organizações
    - /dados/api/publico/grupos - Listar grupos/categorias
    - /dados/api/publico/tags - Listar tags
    
    Nota: Dados públicos podem não requerer autenticação para leitura
    """
    
    BASE_URL = "https://dados.gov.br"
    
    def __init__(self, api_key: Optional[str] = None, delay: float = 1.0):
        # Get API key from parameter or environment variable
        self.api_key = api_key or os.environ.get("DADOS_GOV_API_KEY")
        self.delay = delay
        self.last_request_time = 0
        self.has_auth = bool(self.api_key)
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "application/json, text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "pt-BR,pt;q=0.9,en-US;q=0.8,en;q=0.7",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        })
        
        if self.api_key:
            self.session.headers["Authorization"] = f"Bearer {self.api_key}"
    
    def _rate_limit(self):
        """Rate limiting para não sobrecarregar o servidor"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def search_datasets(self, query: str, page: int = 1, 
                        page_size: int = 20, organization: str = None,
                        theme: str = None, format_filter: str = None) -> Dict:
        """
        Buscar datasets no portal
        
        Args:
            query: Termo de busca
            page: Página (paginação)
            page_size: Itens por página (máx: 100)
            organization: Filtrar por organização
            theme: Filtrar por tema
            format_filter: Filtrar por formato (csv, json, xml, etc.)
        
        Returns:
            Dict com datasets encontrados
            
        Strategy:
            1. Se tem auth -> tentar API pública
            2. Se não tem auth -> usar web scraping diretamente
        """
        self._rate_limit()
        
        # Se não tem autenticação, usar web scraping diretamente
        if not self.has_auth:
            print("[DadosGov] Sem API key - usando web scraping")
            return self._search_web_scraping(query, page_size)
        
        # Endpoint público (requer autenticação)
        url = f"{self.BASE_URL}/dados/api/publico/conjuntos-dados"
        
        params = {
            "q": query,
            "pagina": page,
            "tamanhoPagina": min(page_size, 100)
        }
        
        if organization:
            params["organizacao"] = organization
        if theme:
            params["tema"] = theme
        if format_filter:
            params["formato"] = format_filter
        
        try:
            response = self.session.get(url, params=params, timeout=30, verify=False)
            
            # Verificar se redirecionou para login (HTML response)
            if response.status_code == 200 and "text/html" in response.headers.get("Content-Type", ""):
                print("[DadosGov] Redirecionado para login - sem autenticação válida")
                return self._search_web_scraping(query, page_size)
            
            if response.status_code == 200:
                return self._parse_search_response(response.json())
            else:
                print(f"[DadosGov] HTTP {response.status_code}: {response.text[:200]}")
                return self._search_alternative(query, page, page_size)
                
        except Exception as e:
            print(f"[DadosGov ERROR] {e}")
            return self._search_alternative(query, page, page_size)
    
    def _search_alternative(self, query: str, page: int, page_size: int) -> Dict:
        """API alternativa (CKAN-style)"""
        self._rate_limit()
        
        # Tentar endpoint CKAN
        url = f"{self.BASE_URL}/api/3/action/package_search"
        
        params = {
            "q": query,
            "rows": page_size,
            "start": (page - 1) * page_size
        }
        
        try:
            response = self.session.get(url, params=params, timeout=30, verify=False)
            
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return self._parse_ckan_response(data.get("result", {}))
            
            # Último recurso: scraping da página web
            return self._search_web_scraping(query, page_size)
            
        except Exception as e:
            print(f"[DadosGov ALT ERROR] {e}")
            return self._search_web_scraping(query, page_size)
    
    def _search_web_scraping(self, query: str, limit: int) -> Dict:
        """
        Web scraping como fallback
        
        Nota: dados.gov.br usa JavaScript SPA (Vue.js), o HTML estático
        não contém os dados. Para web scraping completo seria necessário
        usar Selenium/Playwright para renderizar o JavaScript.
        
        Esta função retorna vazio pois a página dinâmica não pode ser
        raspada com requests simples.
        """
        print(f"[DadosGov] Web scraping limitado - site usa JavaScript SPA")
        print(f"[DadosGov] Para acesso completo, obtenha API key em: https://dados.gov.br/usuario/registrar")
        return {"datasets": [], "total": 0, "source": "dados.gov.br_no_auth"}
    
    def get_dataset(self, dataset_id: str) -> Optional[Dict]:
        """
        Obter detalhes de um dataset específico
        
        Args:
            dataset_id: ID do dataset
        
        Returns:
            Dict com detalhes do dataset
        """
        self._rate_limit()
        
        url = f"{self.BASE_URL}/dados/api/publico/conjuntos-dados/{dataset_id}"
        
        try:
            response = self.session.get(url, timeout=30, verify=False)
            
            if response.status_code == 200:
                return self._parse_dataset_detail(response.json())
            else:
                # Tentar CKAN
                return self._get_dataset_ckan(dataset_id)
                
        except Exception as e:
            print(f"[DadosGov ERROR] {e}")
            return None
    
    def _get_dataset_ckan(self, dataset_id: str) -> Optional[Dict]:
        """Obter dataset via CKAN API"""
        url = f"{self.BASE_URL}/api/3/action/package_show"
        params = {"id": dataset_id}
        
        try:
            response = self.session.get(url, params=params, timeout=30, verify=False)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return self._parse_ckan_dataset(data.get("result", {}))
        except Exception as e:
            print(f"[DadosGov CKAN ERROR] {e}")
        
        return None
    
    def get_organizations(self) -> List[Dict]:
        """Listar organizações"""
        self._rate_limit()
        
        url = f"{self.BASE_URL}/dados/api/publico/organizacoes"
        
        try:
            response = self.session.get(url, timeout=30, verify=False)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        
        return []
    
    def get_themes(self) -> List[Dict]:
        """Listar temas"""
        self._rate_limit()
        
        url = f"{self.BASE_URL}/dados/api/publico/grupos"
        
        try:
            response = self.session.get(url, timeout=30, verify=False)
            if response.status_code == 200:
                return response.json()
        except:
            pass
        
        return []
    
    def get_resource(self, resource_id: str) -> Optional[Dict]:
        """
        Obter recurso (arquivo/dado) de um dataset
        
        Args:
            resource_id: ID do recurso
        
        Returns:
            Dict com informação do recurso ou URL para download
        """
        self._rate_limit()
        
        url = f"{self.BASE_URL}/api/3/action/resource_show"
        params = {"id": resource_id}
        
        try:
            response = self.session.get(url, params=params, timeout=30, verify=False)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return data.get("result", {})
        except Exception as e:
            print(f"[DadosGov RESOURCE ERROR] {e}")
        
        return None
    
    def download_resource(self, url: str) -> Optional[bytes]:
        """Download de recurso"""
        self._rate_limit()
        
        try:
            response = self.session.get(url, timeout=60, verify=False)
            response.raise_for_status()
            return response.content
        except Exception as e:
            print(f"[DadosGov DOWNLOAD ERROR] {e}")
            return None
    
    def _parse_search_response(self, data: Any) -> Dict:
        """Parser para resposta de busca"""
        datasets = []
        
        if isinstance(data, list):
            items = data
        elif isinstance(data, dict):
            items = data.get("conteudo", data.get("results", []))
        else:
            items = []
        
        for item in items[:20]:
            dataset = self._parse_dataset(item)
            datasets.append(dataset)
        
        total = len(data) if isinstance(data, list) else data.get("totalElements", len(datasets))
        
        return {
            "datasets": datasets,
            "total": total,
            "source": "dados.gov.br_api"
        }
    
    def _parse_ckan_response(self, result: Dict) -> Dict:
        """Parser para resposta CKAN"""
        datasets = []
        
        for item in result.get("results", []):
            dataset = self._parse_ckan_dataset(item)
            datasets.append(dataset)
        
        return {
            "datasets": datasets,
            "total": result.get("count", 0),
            "source": "dados.gov.br_ckan"
        }
    
    def _parse_dataset(self, item: Dict) -> Dict:
        """Parser para dataset"""
        return {
            "id": item.get("id", ""),
            "title": item.get("titulo", item.get("title", "")),
            "description": item.get("descricao", item.get("description", ""))[:200],
            "organization": item.get("organizacao", ""),
            "organization_title": item.get("organizacaoTitulo", ""),
            "tags": [t.get("nome", t.get("name", "")) for t in item.get("tags", [])],
            "themes": [t.get("titulo", t.get("title", "")) for t in item.get("grupos", [])],
            "created": item.get("dataCriacao", ""),
            "modified": item.get("dataModificacao", ""),
            "frequency": item.get("frequenciaAtualizacao", ""),
            "license": item.get("licenca", ""),
            "url": f"{self.BASE_URL}/dados/conjuntos-dados/{item.get('id', '')}",
            "num_resources": item.get("totalRecursos", 0),
            "num_tags": item.get("totalTags", 0),
            "source": "dados.gov.br"
        }
    
    def _parse_ckan_dataset(self, item: Dict) -> Dict:
        """Parser para dataset CKAN"""
        return {
            "id": item.get("id", ""),
            "title": item.get("title", ""),
            "description": item.get("notes", "")[:200],
            "organization": item.get("organization", {}).get("name", ""),
            "organization_title": item.get("organization", {}).get("title", ""),
            "tags": [t.get("display_name", "") for t in item.get("tags", [])],
            "themes": [g.get("display_name", "") for g in item.get("groups", [])],
            "created": item.get("metadata_created", ""),
            "modified": item.get("metadata_modified", ""),
            "license": item.get("license_title", ""),
            "url": item.get("url", f"{self.BASE_URL}/dataset/{item.get('name', '')}"),
            "resources": [{
                "id": r.get("id", ""),
                "name": r.get("name", ""),
                "format": r.get("format", ""),
                "url": r.get("url", ""),
                "size": r.get("size", 0)
            } for r in item.get("resources", [])],
            "num_resources": len(item.get("resources", [])),
            "num_tags": len(item.get("tags", [])),
            "source": "dados.gov.br"
        }
    
    def _parse_dataset_detail(self, data: Dict) -> Dict:
        """Parser para detalhes do dataset"""
        return self._parse_dataset(data)
    
    def _parse_html_search(self, html: str, limit: int) -> Dict:
        """Parser para busca HTML"""
        try:
            from bs4 import BeautifulSoup
            soup = BeautifulSoup(html, 'html.parser')
            
            datasets = []
            for item in soup.find_all('article', class_='dataset-item')[:limit]:
                dataset = {
                    "title": item.find('h3', class_='dataset-heading')
                              and item.find('h3', class_='dataset-heading').get_text(strip=True) or "",
                    "description": item.find('div', class_='notes')
                                   and item.find('div', class_='notes').get_text(strip=True)[:200] or "",
                    "url": item.find('a') and item.find('a').get('href', '') or ""
                }
                if dataset["title"]:
                    datasets.append(dataset)
            
            return {
                "datasets": datasets,
                "total": len(datasets),
                "source": "dados.gov.br_html"
            }
        except:
            return {"datasets": [], "total": 0, "source": "dados.gov.br"}


# Funções de conveniência
def search_dados_gov(query: str, max_results: int = 20, 
                     api_key: str = None) -> List[Dict]:
    """Buscar datasets no dados.gov.br"""
    scraper = DadosGovScraper(api_key=api_key)
    result = scraper.search_datasets(query, page_size=max_results)
    return result.get("datasets", [])

def get_dados_gov_dataset(dataset_id: str, api_key: str = None) -> Optional[Dict]:
    """Obter dataset específico"""
    scraper = DadosGovScraper(api_key=api_key)
    return scraper.get_dataset(dataset_id)

def get_dados_gov_recent(max_results: int = 10) -> List[Dict]:
    """Obter datasets recentes"""
    scraper = DadosGovScraper()
    result = scraper.search_datasets("", page_size=max_results)
    return result.get("datasets", [])


# Testes
def test_dados_gov_scraper():
    """Testar scraper dados.gov.br"""
    print("=" * 70)
    print("MASWOS V5 NEXUS - dados.gov.br Scraper Test")
    print("=" * 70)
    
    print("\n[INFO] dados.gov.br requer autenticação para API")
    print("    Sem API key, o scraper usa web scraping como fallback")
    print("    Para API completa, defina DADOS_GOV_API_KEY ou passe api_key")
    
    scraper = DadosGovScraper(delay=1.0)
    print(f"\n  Autenticação: {'Sim' if scraper.has_auth else 'Não - usando web scraping'}")
    
    # Teste 1: Web scraping (funciona sem auth)
    print("\n[TEST 1] Busca via web scraping: 'educacao'")
    result = scraper.search_datasets("educacao", page_size=5)
    print(f"  Total encontrado: {result['total']}")
    print(f"  Fonte: {result['source']}")
    print(f"  Datasets recuperados: {len(result['datasets'])}")
    
    for i, dataset in enumerate(result['datasets'][:3], 1):
        print(f"\n  Dataset {i}:")
        print(f"    Título: {dataset.get('title', '')[:70]}...")
        print(f"    URL: {dataset.get('url', '')[:60]}...")
        if dataset.get('description'):
            print(f"    Descrição: {dataset.get('description', '')[:80]}...")
    
    # Teste 2: Busca por saúde
    print("\n[TEST 2] Busca por: 'saude'")
    result = scraper.search_datasets("saude", page_size=3)
    print(f"  Total encontrado: {result['total']}")
    print(f"  Fonte: {result['source']}")
    
    print("\n" + "=" * 70)
    print("dados.gov.br Scraper - Testes Concluídos")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    test_dados_gov_scraper()