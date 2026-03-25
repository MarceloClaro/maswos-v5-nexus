#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - CNKI (China National Knowledge Infrastructure) Scraper

CNKI é o maior banco de dados acadêmico da China.

API oficial requer parceria institucional, então este scraper usa:
1. Busca via web scraping (similar ao MagicCNKI/CnkiSpider)
2. Metadados básicos (título, autores, ano, abstract)

Nota: O acesso completo (download de PDFs) requer instituição parceira.

Arquitetura: Transformer-Agentes (Encoder → Web → Parser → Decoder)
"""

import requests
import time
import json
import re
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
from urllib.parse import quote, urlencode
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

@dataclass
class CNKIPaper:
    """Paper do CNKI"""
    id: str = ""
    title: str = ""
    title_cn: str = ""
    abstract: str = ""
    abstract_cn: str = ""
    authors: List[str] = field(default_factory=list)
    year: str = ""
    source: str = ""  # Journal/Conference name
    keywords: List[str] = field(default_factory=list)
    doi: str = ""
    citation_count: int = 0
    url: str = ""
    database: str = ""  # CDFD, CJD, etc.
    source_type: str = "cnki"


class CNKIScraper:
    """
    Scraper para CNKI (知网) via web scraping
    
    CNKI não fornece API pública para não-instituições.
    Este scraper acessa os resultados de busca via web.
    
    Fontes de dados:
    - CDFD (中国博士学位论文全文数据库) - Teses de doutorado
    - CMFD (中国优秀硕士学位论文全文数据库) - Teses de mestrado
    - CJD (中国期刊全文数据库) - Periódicos
    - CCND (中国重要报纸全文数据库) - Jornais
    - CCVD (中国重要会议论文全文数据库) - Conferências
    
    Limitações:
    - Sem API oficial para usuários externos
    - Acesso completo requer instituição parceira
    - Web scraping pode ser bloqueado por rate limiting
    """
    
    BASE_URL = "https://kns.cnki.net"
    SEARCH_URL = "https://kns.cnki.net/kns8s/defaultresult/index"
    
    def __init__(self, delay: float = 2.0):
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/120.0.0.0 Safari/537.36",
            "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
            "Accept-Language": "zh-CN,zh;q=0.9,en;q=0.8",
            "Accept-Encoding": "gzip, deflate, br",
            "Connection": "keep-alive"
        })
    
    def _rate_limit(self):
        """Rate limiting para não ser bloqueado"""
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def search(self, query: str, limit: int = 20,
               database: str = "CJD") -> Dict:
        """
        Buscar artigos no CNKI
        
        Args:
            query: Termo de busca (em chinês ou inglês)
            limit: Número de resultados
            database: Banco de dados
                - CJD: Periódicos (中国期刊)
                - CDFD: Doutorado (博士)
                - CMFD: Mestrado (硕士)
                - CCVD: Conferências (会议)
        
        Returns:
            Dict com artigos encontrados
        """
        self._rate_limit()
        
        # URL de busca do CNKI
        params = {
            "classid": "TTODAYoperation",
            "kw": query,
            "korder": "su",  #排序方式: su=相关度, date=发表时间, cit=被引次数
            "dbprefix": database,
            "scope": "CKOD_search",
            "kbase": "",
            "kqf": "",
            "kqt": "",
            "bt": "",
            "et": "",
            "offset": 0,
            "sfield": "SU",  # 搜索字段: TI=篇名, AU=作者, SU=主题, AB=摘要
            "pagesize": min(limit, 50)
        }
        
        try:
            response = self.session.get(
                self.SEARCH_URL,
                params=params,
                timeout=30,
                verify=False
            )
            
            if response.status_code == 200:
                return self._parse_search_results(response.text, query)
            else:
                print(f"[CNKI] HTTP {response.status_code}")
                return {"articles": [], "total": 0, "source": "cnki_error"}
                
        except Exception as e:
            print(f"[CNKI ERROR] {e}")
            return {"articles": [], "total": 0, "source": "cnki_exception"}
    
    def search_alternative(self, query: str, limit: int = 20) -> Dict:
        """
        Busca alternativa via API interna do CNKI
        
        Usa endpoint interno que retorna JSON
        """
        self._rate_limit()
        
        url = "https://kns.cnki.net/kns8s/defaultresult/index"
        
        params = {
            "classid": "TTODAYoperation",
            "kw": query,
            "korder": "su",
            "dbprefix": "CJD",
            "scope": "CKOD_search",
            "offset": 0,
            "sfield": "SU",
            "pagesize": min(limit, 50)
        }
        
        headers = {
            "Accept": "application/json, text/javascript, */*; q=0.01",
            "X-Requested-With": "XMLHttpRequest",
            "Referer": "https://kns.cnki.net/kns8s/defaultresult/index"
        }
        
        try:
            response = self.session.get(
                url,
                params=params,
                headers=headers,
                timeout=30,
                verify=False
            )
            
            if response.status_code == 200:
                # Tentar parse como JSON
                try:
                    data = response.json()
                    return self._parse_json_results(data)
                except:
                    # Se não for JSON, tentar HTML
                    return self._parse_search_results(response.text, query)
            else:
                return {"articles": [], "total": 0, "source": "cnki_error"}
                
        except Exception as e:
            print(f"[CNKI ERROR] {e}")
            return {"articles": [], "total": 0, "source": "cnki_exception"}
    
    def _parse_search_results(self, html: str, query: str) -> Dict:
        """Parser para resultados de busca em HTML"""
        articles = []
        
        # Padrões regex para extrair informações
        # Nota: O HTML do CNKI pode mudar, estes são padrões comuns
        
        # Extrair artigos usando padrões comuns
        # Título e autores geralmente estão em elementos específicos
        title_pattern = r'<h1[^>]*class="title"[^>]*>(.*?)</h1>'
        titles = re.findall(title_pattern, html, re.DOTALL)
        
        # Se não encontrar pelo padrão, tentar alternativas
        if not titles:
            title_pattern = r'class="name"[^>]*>(.*?)</a>'
            titles = re.findall(title_pattern, html, re.DOTALL)
        
        for i, title in enumerate(titles[:20]):
            # Limpar HTML tags
            clean_title = re.sub(r'<[^>]+>', '', title).strip()
            
            articles.append({
                "id": f"cnki_{i}",
                "title": clean_title,
                "title_cn": clean_title,
                "authors": [],
                "year": "",
                "source": "",
                "abstract": "",
                "url": "",
                "source_type": "cnki"
            })
        
        # Tentar extrair total de resultados
        total_pattern = r'共\s*(\d+)\s*条'
        total_match = re.search(total_pattern, html)
        total = int(total_match.group(1)) if total_match else len(articles)
        
        return {
            "articles": articles,
            "total": total,
            "source": "cnki_web"
        }
    
    def _parse_json_results(self, data: Dict) -> Dict:
        """Parser para resultados JSON"""
        articles = []
        
        records = data.get("records", data.get("result", []))
        for record in records:
            article = self._parse_article(record)
            articles.append(article)
        
        return {
            "articles": articles,
            "total": data.get("total", len(articles)),
            "source": "cnki_api"
        }
    
    def _parse_article(self, item: Dict) -> Dict:
        """Parser para artigo"""
        return {
            "id": item.get("id", ""),
            "title": item.get("title", ""),
            "title_cn": item.get("title_cn", item.get("ctitle", "")),
            "abstract": item.get("abstract", ""),
            "abstract_cn": item.get("abstract_cn", item.get("cabstract", "")),
            "authors": item.get("authors", "").split(";") if isinstance(item.get("authors"), str) else [],
            "year": item.get("year", item.get("pubyear", "")),
            "source": item.get("source", item.get("journal", "")),
            "keywords": item.get("keywords", "").split(";") if isinstance(item.get("keywords"), str) else [],
            "doi": item.get("doi", ""),
            "citation_count": item.get("cited", 0),
            "url": item.get("url", ""),
            "database": item.get("database", ""),
            "source_type": "cnki"
        }


# Funções de conveniência
def search_cnki(query: str, max_results: int = 20) -> List[Dict]:
    """Buscar artigos no CNKI"""
    scraper = CNKIScraper()
    result = scraper.search(query, limit=max_results)
    return result.get("articles", [])


# Testes
def test_cnki_scraper():
    """Testar scraper CNKI"""
    print("=" * 70)
    print("MASWOS V5 NEXUS - CNKI Scraper Test")
    print("=" * 70)
    
    scraper = CNKIScraper(delay=2.0)
    
    # Teste: Busca simples
    print("\n[TEST 1] Busca: '人工智能' (Artificial Intelligence)")
    result = scraper.search("人工智能", limit=5)
    print(f"  Total encontrado: {result['total']}")
    print(f"  Fonte: {result['source']}")
    print(f"  Artigos recuperados: {len(result['articles'])}")
    
    if result.get('articles'):
        for i, article in enumerate(result['articles'][:2], 1):
            print(f"\n  Artigo {i}:")
            print(f"    Título: {article.get('title', '')[:60]}...")
    
    print("\n" + "=" * 70)
    print("CNKI Scraper - Testes Concluídos")
    print("\nNota: CNKI requer instituição parceira para acesso completo.")
    print("Para metadados completos, considere usar AMiner ou outros agregadores.")
    print("=" * 70)
    
    return True

if __name__ == "__main__":
    test_cnki_scraper()
