"""
MASWOS V5 NEXUS - Script de Validação de APIs Governamentais
Autor: Arquitetura Transformer-Agentes
Versão: 5.0.0-NEXUS

Este script testa a conectividade e disponibilidade das APIs
integradas ao MASWOS V5 NEXUS.

Arquitetura: Transformer-Agentes com Scraping Granular como Fallback
"""

import subprocess
import json
import urllib3
from dataclasses import dataclass
from typing import Dict, List, Optional
from datetime import datetime

# Desativar avisos de SSL para APIs governamentais com certificados problemáticos
urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)

# Importar engine de scraping avançado
try:
    from advanced_scraping_engine import scraping_orchestrator, ScrapingResult
    HAS_ADVANCED_SCRAPING = True
except ImportError:
    HAS_ADVANCED_SCRAPING = False
    print("[AVISO] advanced_scraping_engine não disponível. Fallbacks limitados.")

@dataclass
class APIResult:
    name: str
    url: str
    status_code: int
    available: bool
    latency_ms: Optional[float] = None
    error: Optional[str] = None
    scraping_fallback: bool = False
    fallback_technique: Optional[str] = None
    fallback_data: Optional[Dict] = None

class APIValidator:
    """
    Validador de APIs governamentais e acadêmicas.
    
    Integra com os scrapers do MASWOS V5 NEXUS:
    - N05: LexML (Legislação)
    - N06: STF (Jurisprudência)
    - N07: STJ (Jurisprudência)
    - N09: IBGE (Demografia)
    - N10: INEP (Educação)
    - N11: CNJ (Estatísticas)
    - A04: arXiv (Preprints)
    - A05: CrossRef (Referências)
    - A06: OpenAlex (Citations)
    - A07: PubMed (Biomedicina)
    - A10: IPEA (Dados econômicos)
    """
    
    def __init__(self):
        self.apis = {
            # APIs Jurídicas Brasileiras
            'LexML': {
                'url': 'https://www.lexml.gov.br/api/',
                'scraper_id': 'N05',
                'type': 'juridico'
            },
            'STF': {
                'url': 'https://portal.stf.jus.br/api/',
                'scraper_id': 'N06',
                'type': 'juridico'
            },
            'STJ': {
                'url': 'https://www.stj.jus.br/api/',
                'scraper_id': 'N07',
                'type': 'juridico'
            },
            'TJ-CE': {
                'url': 'https://www.tjce.jus.br/api/',
                'scraper_id': 'N08',
                'type': 'juridico'
            },
            
            # APIs Governamentais
            'IBGE': {
                'url': 'https://servicos.ibge.gov.br/geoserver/publico/wms',
                'scraper_id': 'N09',
                'type': 'governamental'
            },
            'INEP': {
                'url': 'https://www.gov.br/inep/pt-br',
                'scraper_id': 'N10',
                'type': 'governamental'
            },
            'CNJ': {
                'url': 'https://www.cnj.jus.br/api/',
                'scraper_id': 'N11',
                'type': 'governamental'
            },
            'IPEA': {
                'url': 'https://www.ipeadata.gov.br/api/odata4/',
                'scraper_id': 'A11',
                'type': 'governamental'
            },
            'Dados.gov.br': {
                'url': 'https://dados.gov.br/api/',
                'scraper_id': 'N/A',
                'type': 'governamental'
            },
            
            # APIs Acadêmicas Internacionais
            'arXiv': {
                'url': 'http://export.arxiv.org/api/query',
                'scraper_id': 'A04',
                'type': 'academico'
            },
            'CrossRef': {
                'url': 'https://api.crossref.org/',
                'scraper_id': 'A05',
                'type': 'academico'
            },
            'OpenAlex': {
                'url': 'https://api.openalex.org/',
                'scraper_id': 'A06',
                'type': 'academico'
            },
            'PubMed': {
                'url': 'https://eutils.ncbi.nlm.nih.gov/entrez/eutils/',
                'scraper_id': 'A07',
                'type': 'academico'
            },
            'Europe PMC': {
                'url': 'https://www.ebi.ac.uk/europepmc/webservices/rest/',
                'scraper_id': 'A08',
                'type': 'academico'
            },
            'Semantic Scholar': {
                'url': 'https://api.semanticscholar.org/graph/v1/paper/search',
                'scraper_id': 'A09',
                'type': 'academico'
            },
            'DOAJ': {
                'url': 'https://doaj.org/api/v4/search/articles/',
                'scraper_id': 'A10',
                'type': 'academico'
            },
            'CORE': {
                'url': 'https://api.core.ac.uk/v3/search/works',
                'scraper_id': 'A11',
                'type': 'academico'
            },
            'AMiner': {
                'url': 'https://datacenter.aminer.cn/gateway/open_platform/api/paper/search',
                'scraper_id': 'A12',
                'type': 'academico'
            },
            
            # CAPES - Portal de Periódicos
            'CAPES': {
                'url': 'https://dadosabertos.capes.gov.br/api/3/action/package_list',
                'scraper_id': 'A13',
                'type': 'academico'
            },
        }
    
    def test_api(self, name: str, config: Dict) -> APIResult:
        """Testa uma única API"""
        import time
        import requests
        
        url = config['url']
        
        try:
            start = time.time()
            
            # Faz requisição com timeout e verify=False para SSL problemático
            response = requests.get(
                url,
                headers={'User-Agent': 'MASWOS-V5-NEXUS/5.0'},
                timeout=10,
                verify=False  # Desativar verificação SSL para APIs governamentais
            )
            
            latency = (time.time() - start) * 1000
            
            # Se status >= 400, tentar fallback com scraping
            if response.status_code >= 400 and HAS_ADVANCED_SCRAPING:
                fallback_result = self._try_scraping_fallback(name, config)
                if fallback_result:
                    return fallback_result
            
            return APIResult(
                name=name,
                url=url,
                status_code=response.status_code,
                available=response.status_code < 400,
                latency_ms=round(latency, 2)
            )
                
        except requests.exceptions.HTTPError as e:
            return APIResult(
                name=name,
                url=url,
                status_code=e.response.status_code if e.response else 0,
                available=e.response.status_code < 500 if e.response else False,
                error=str(e)
            )
        except requests.exceptions.ConnectionError as e:
            return APIResult(
                name=name,
                url=url,
                status_code=0,
                available=False,
                error=f"Connection error: {e}"
            )
        except requests.exceptions.Timeout as e:
            return APIResult(
                name=name,
                url=url,
                status_code=0,
                available=False,
                error=f"Timeout: {e}"
            )
        except Exception as e:
            # Tentar fallback com scraping avançado
            if HAS_ADVANCED_SCRAPING:
                fallback_result = self._try_scraping_fallback(name, config)
                if fallback_result:
                    return fallback_result
            
            return APIResult(
                name=name,
                url=url,
                status_code=0,
                available=False,
                error=str(e)
            )
    
    def _try_scraping_fallback(self, name: str, config: Dict) -> Optional[APIResult]:
        """Tentar fallback com scraping avançado"""
        import time
        
        if not HAS_ADVANCED_SCRAPING:
            return None
        
        scraper_map = {
            'STF': ('STF', ''),
            'IBGE': ('IBGE', ''),
            'PubMed': ('PUBMED', 'cancer'),
            'Europe PMC': ('PUBMED', 'cancer'),
            'arXiv': ('ARXIV', 'machine learning'),
            'Dados.gov.br': ('DADOSGOV', 'educacao'),
            'Semantic Scholar': ('SEMANTICSCHOLAR', 'deep learning'),
            'DOAJ': ('DOAJ', 'open access'),
            'CORE': ('CORE', 'research papers'),
            'AMiner': ('AMINER', 'artificial intelligence'),
            'CAPES': ('CAPES', 'periodicos')
        }
        
        if name in scraper_map:
            source, query = scraper_map[name]
            
            print(f"  [FALLBACK] Tentando scraping granular para {name}...")
            
            start = time.time()
            result = scraping_orchestrator.scrape_with_fallback(source, query)  # type: ignore
            latency = (time.time() - start) * 1000
            
            if result.status == "success":
                # Dados.gov.br sem auth é limitado mas considerado "disponível"
                is_available = result.status == "success"
                
                return APIResult(
                    name=name,
                    url=f"scraping_fallback:{name}",
                    status_code=200,
                    available=is_available,
                    latency_ms=round(latency, 2),
                    scraping_fallback=True,
                    fallback_technique=result.technique,
                    fallback_data=result.data
                )
        
        return None
    
    def test_all_apis(self) -> List[APIResult]:
        """Testa todas as APIs configuradas"""
        results = []
        for name, config in self.apis.items():
            result = self.test_api(name, config)
            results.append(result)
        return results
    
    def generate_report(self, results: List[APIResult]) -> Dict:
        """Gera relatório de validação"""
        total = len(results)
        available = sum(1 for r in results if r.available)
        unavailable = total - available
        
        by_type = {}
        for result in results:
            api_config = self.apis.get(result.name, {})
            api_type = api_config.get('type', 'unknown')
            
            if api_type not in by_type:
                by_type[api_type] = {'total': 0, 'available': 0}
            
            by_type[api_type]['total'] += 1
            if result.available:
                by_type[api_type]['available'] += 1
        
        return {
            'timestamp': datetime.now().isoformat(),
            'summary': {
                'total_apis': total,
                'available': available,
                'unavailable': unavailable,
                'availability_rate': round(available / total * 100, 2) if total > 0 else 0
            },
            'by_type': by_type,
            'results': [
                {
                    'name': r.name,
                    'scraper_id': self.apis.get(r.name, {}).get('scraper_id', 'N/A'),
                    'type': self.apis.get(r.name, {}).get('type', 'unknown'),
                    'status_code': r.status_code,
                    'available': r.available,
                    'latency_ms': r.latency_ms,
                    'error': r.error,
                    'scraping_fallback': r.scraping_fallback,
                    'fallback_technique': r.fallback_technique
                }
                for r in results
            ],
            'fallbacks_used': sum(1 for r in results if r.scraping_fallback)
        }


def main():
    print("=" * 70)
    print("MASWOS V5 NEXUS - Validação de APIs Governamentais")
    print("=" * 70)
    
    validator = APIValidator()
    
    print("\n[Testando APIs...]")
    results = validator.test_all_apis()
    
    # Imprime resultados
    print("\n" + "-" * 70)
    print(f"{'API':<20} {'Scraper':<10} {'Tipo':<15} {'Status':<8} {'Latencia':<10}")
    print("-" * 70)
    
    for result in results:
        scraper = validator.apis.get(result.name, {}).get('scraper_id', 'N/A')
        api_type = validator.apis.get(result.name, {}).get('type', 'unknown')
        status = "[OK]" if result.available else "[FAIL]"
        latency = f"{result.latency_ms}ms" if result.latency_ms else "N/A"
        fallback = " [FALLBACK]" if result.scraping_fallback else ""
        
        print(f"{result.name:<20} {scraper:<10} {api_type:<15} {status:<8} {latency:<10}{fallback}")
    
    # Gera relatório
    report = validator.generate_report(results)
    
    print("\n" + "=" * 70)
    print("RESUMO")
    print("=" * 70)
    print(f"Total de APIs: {report['summary']['total_apis']}")
    print(f"Disponíveis: {report['summary']['available']}")
    print(f"Indisponíveis: {report['summary']['unavailable']}")
    print(f"Taxa de Disponibilidade: {report['summary']['availability_rate']}%")
    
    print("\nPor Tipo:")
    for api_type, stats in report['by_type'].items():
        rate = stats['available'] / stats['total'] * 100 if stats['total'] > 0 else 0
        print(f"  - {api_type.capitalize()}: {stats['available']}/{stats['total']} ({rate:.1f}%)")
    
    if report.get('fallbacks_used', 0) > 0:
        print(f"\n[FALLBACK] Scraping granular utilizado: {report['fallbacks_used']} APIs")
    
    # Salva relatório
    report_path = 'api_validation_report.json'
    with open(report_path, 'w', encoding='utf-8') as f:
        json.dump(report, f, indent=2, ensure_ascii=False)
    
    print(f"\n[Relatório salvo em: {report_path}]")
    print("=" * 70)
    
    return report


if __name__ == "__main__":
    main()
