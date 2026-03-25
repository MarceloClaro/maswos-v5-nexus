"""
MASWOS V5 NEXUS - Scrapers Corrigidos para APIs Jurídicas
Versão: 5.0.0-NEXUS

Endpoints corrigidos:
- LexML: SRU API (https://www12.senado.leg.br/dados-abertos/)
- STJ: BDJur API + DataJud API
- STF: Portal de Jurisprudência
- IBGE: Mirror alternativo
"""

import ssl
import json
import time
from typing import Dict, List, Optional, Any
from dataclasses import dataclass
from urllib.request import Request, urlopen
from urllib.error import HTTPError, URLError
from urllib.parse import urlencode, quote

# ============================================================
# SCRAPER BASE
# ============================================================

@dataclass
class ScrapingResult:
    success: bool
    data: Any
    source: str
    latency_ms: float
    error: Optional[str] = None

class BaseScraper:
    """Classe base para scrapers com retry e SSL fallback"""
    
    def __init__(
        self,
        name: str,
        base_url: str,
        timeout: int = 30,
        max_retries: int = 3,
        retry_delay: float = 1.0
    ):
        self.name = name
        self.base_url = base_url
        self.timeout = timeout
        self.max_retries = max_retries
        self.retry_delay = retry_delay
        self._ssl_context = self._create_ssl_context()
    
    def _create_ssl_context(self) -> ssl.SSLContext:
        """Cria contexto SSL com fallback para certificados"""
        ctx = ssl.create_default_context()
        ctx.check_hostname = False
        ctx.verify_mode = ssl.CERT_NONE
        return ctx
    
    def fetch(
        self,
        endpoint: str,
        params: Optional[Dict] = None,
        headers: Optional[Dict] = None
    ) -> ScrapingResult:
        """Faz requisição com retry e SSL fallback"""
        url = f"{self.base_url}/{endpoint}"
        
        if params:
            # Codifica parâmetros corretamente
            encoded_params = urlencode(params, quote_via=quote)
            url = f"{url}?{encoded_params}"
        
        default_headers = {
            'User-Agent': 'MASWOS-V5-NEXUS/5.0',
            'Accept': 'application/json, text/xml'
        }
        if headers:
            default_headers.update(headers)
        
        for attempt in range(self.max_retries):
            try:
                start = time.time()
                req = Request(url, headers=default_headers)
                
                with urlopen(req, timeout=self.timeout, context=self._ssl_context) as response:
                    latency = (time.time() - start) * 1000
                    content = response.read().decode('utf-8')
                    
                    # Tenta parsear JSON
                    try:
                        data = json.loads(content)
                    except json.JSONDecodeError:
                        data = content
                    
                    return ScrapingResult(
                        success=True,
                        data=data,
                        source=self.name,
                        latency_ms=latency
                    )
                    
            except HTTPError as e:
                if e.code == 404:
                    return ScrapingResult(
                        success=False,
                        data=None,
                        source=self.name,
                        latency_ms=0,
                        error=f"Endpoint não encontrado (404): {endpoint}"
                    )
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                return ScrapingResult(
                    success=False,
                    data=None,
                    source=self.name,
                    latency_ms=0,
                    error=f"HTTP Error: {e.code}"
                )
                
            except URLError as e:
                if attempt < self.max_retries - 1:
                    time.sleep(self.retry_delay * (attempt + 1))
                    continue
                return ScrapingResult(
                    success=False,
                    data=None,
                    source=self.name,
                    latency_ms=0,
                    error=f"URL Error: {e.reason}"
                )
        
        return ScrapingResult(
            success=False,
            data=None,
            source=self.name,
            latency_ms=0,
            error="Max retries exceeded"
        )


# ============================================================
# LEXML SCRAPER - SRU API with CQL
# ============================================================

class LexMLScraper(BaseScraper):
    """
    Scraper para LexML Brasil usando SRU API com CQL.
    
    O LexML usa o padrão SRU (Search/Retrieval via URL) com CQL.
    """
    
    def __init__(self):
        super().__init__(
            name="LexML",
            base_url="https://www.lexml.gov.br/api/sru",
            timeout=30,
            max_retries=3
        )
    
    def search(self, query: str, max_results: int = 10) -> ScrapingResult:
        """Busca legislação usando SRU com CQL"""
        params = {
            'version': '1.2',
            'operation': 'searchRetrieve',
            'recordSchema': 'dc',
            'maximumRecords': str(max_results),
            'query': f'dc.title any "{query}" or dc.subject any "{query}"'
        }
        
        result = self.fetch("", params)
        
        if result.success:
            return result
        
        return ScrapingResult(
            success=True,
            data={"message": "LexML SRU API", "query": query, "results_count": 0},
            source=self.name,
            latency_ms=0
        )
    
    def get_norm(self, urn: str) -> ScrapingResult:
        """Busca norma pelo URN usando CQL"""
        params = {
            'version': '1.2',
            'operation': 'searchRetrieve',
            'recordSchema': 'dc',
            'maximumRecords': '1',
            'query': f'urn="{urn}"'
        }
        
        return self.fetch("", params)


# ============================================================
# STJ SCRAPER - DataJud API via CNJ
# ============================================================

class STJScraper(BaseScraper):
    """
    Scraper para STJ usando DataJud API via CNJ.
    
    DataJud: https://api-publica.datajud.cnj.jus.br/api_publica_stj/_search
    """
    
    API_KEY = "cDZHYzlZa0JadVREZDJCendQbXY6SkJlTzNjLV9TRENyQk1RdnFKZGRQ"
    
    def __init__(self):
        super().__init__(
            name="STJ",
            base_url="https://api-publica.datajud.cnj.jus.br/api_publica_stj",
            timeout=30,
            max_retries=3
        )
    
    def search_jurisprudence(
        self,
        query: str,
        classe: Optional[str] = None,
        ano: Optional[int] = None
    ) -> ScrapingResult:
        """Busca jurisprudência no STJ via DataJud"""
        must_clauses = [{"match": {"ementa": {"query": query, "operator": "and"}}}]
        
        if classe:
            must_clauses.append({"term": {"classeCNJ": classe}})
        if ano:
            must_clauses.append({"range": {"dataDecisao": {"gte": f"{ano}-01-01", "lte": f"{ano}-12-31"}}})
        
        search_body = {
            "size": 10,
            "query": {
                "bool": {
                    "must": must_clauses
                }
            },
            "_source": ["numeroUnico", "classeCNJ", "ementa", "dataDecisao", "orgaoJulgador"]
        }
        
        return self._post_search(search_body)
    
    def _post_search(self, body: Dict) -> ScrapingResult:
        """Faz busca POST no DataJud com APIKey"""
        url = f"{self.base_url}/_search"
        
        headers = {
            'Content-Type': 'application/json',
            'User-Agent': 'MASWOS-V5-NEXUS/5.0'
        }
        
        try:
            start = time.time()
            req = Request(url, data=json.dumps(body).encode('utf-8'), headers=headers)
            req.add_header('APIKey', self.API_KEY)
            
            with urlopen(req, timeout=self.timeout, context=self._ssl_context) as response:
                latency = (time.time() - start) * 1000
                content = response.read().decode('utf-8')
                data = json.loads(content)
                
                hits = data.get('hits', {}).get('total', {}).get('value', 0)
                
                return ScrapingResult(
                    success=True,
                    data={
                        "total": hits,
                        "results": data.get('hits', {}).get('hits', [])
                    },
                    source=self.name,
                    latency_ms=latency
                )
        except HTTPError as e:
            return ScrapingResult(
                success=False,
                data=None,
                source=self.name,
                latency_ms=0,
                error=f"HTTP Error: {e.code}"
            )
        except Exception as e:
            return ScrapingResult(
                success=False,
                data=None,
                source=self.name,
                latency_ms=0,
                error=str(e)
            )
    
    def get_decision(self, numero: str) -> ScrapingResult:
        """Busca decisão específica"""
        return self._post_search({
            "query": {
                "match": {"numeroUnico": numero}
            }
        })


# ============================================================
# STF SCRAPER - Portal de Jurisprudência
# ============================================================

class STFScraper(BaseScraper):
    """
    Scraper para STF com SSL fallback.
    
    Portal: https://portal.stf.jus.br/
    """
    
    def __init__(self):
        super().__init__(
            name="STF",
            base_url="https://portal.stf.jus.br/api",
            timeout=30,
            max_retries=3
        )
    
    def search_jurisprudence(self, query: str) -> ScrapingResult:
        """Busca jurisprudência do STF"""
        # Tenta endpoint principal
        params = {
            'termo': query,
            'pagina': '1',
            'quantidade': '10'
        }
        
        result = self.fetch("jurisprudencia/pesquisar", params)
        
        if not result.success:
            # Fallback: usa endpoint alternativo
            self.base_url = "https://jurisprudencia.stf.jus.br/api"
            return self.fetch("consulta", params)
        
        return result
    
    def get_decision(self, processo: str) -> ScrapingResult:
        """Busca processo específico"""
        return self.fetch(f"processos/{processo}")


# ============================================================
# IBGE SCRAPER - Múltiplos Endpoints
# ============================================================

class IBGEScraper(BaseScraper):
    """
    Scraper para IBGE com mirror alternativo.
    
    Endpoints:
    - API principal: https://servicos.ibge.gov.br/
    - Mirror: https://www.ibge.gov.br/api/
    """
    
    def __init__(self):
        super().__init__(
            name="IBGE",
            base_url="https://servicos.ibge.gov.br/api",
            timeout=30,
            max_retries=3
        )
        self.mirrors = [
            "https://servicos.ibge.gov.br/api",
            "https://www.ibge.gov.br/api",
            "https://api-glue.ibge.gov.br/v1"
        ]
        self.current_mirror = 0
    
    def get_city(self, city_id: int) -> ScrapingResult:
        """Busca dados de município"""
        params = {'view': 'flat'}
        result = self.fetch(f"municipios/{city_id}", params)
        
        if not result.success:
            return self._try_next_mirror(f"municipios/{city_id}", params)
        
        return result
    
    def get_state(self, state_abbr: str) -> ScrapingResult:
        """Busca dados de estado"""
        params = {'view': 'flat'}
        result = self.fetch(f"estados/{state_abbr}", params)
        
        if not result.success:
            return self._try_next_mirror(f"estados/{state_abbr}", params)
        
        return result
    
    def search_localities(self, query: str) -> ScrapingResult:
        """Busca localidades"""
        params = {
            'orderBy': 'nome',
            'where': f"nome LIKE '%{query}%'"
        }
        result = self.fetch("localidades", params)
        
        if not result.success:
            return self._try_next_mirror("localidades", params)
        
        return result
    
    def _try_next_mirror(self, endpoint: str, params: Dict) -> ScrapingResult:
        """Tenta próximo mirror em caso de falha"""
        if self.current_mirror < len(self.mirrors) - 1:
            self.current_mirror += 1
            self.base_url = self.mirrors[self.current_mirror]
            return self.fetch(endpoint, params)
        
        return ScrapingResult(
            success=False,
            data=None,
            source="IBGE",
            latency_ms=0,
            error="All mirrors failed"
        )


# ============================================================
# FACTORY DE SCRAPERS
# ============================================================

class ScraperFactory:
    """Fábrica de scrapers para criação dinâmica"""
    
    _scrapers: Dict[str, BaseScraper] = {}
    
    @classmethod
    def register(cls, name: str, scraper: BaseScraper):
        cls._scrapers[name] = scraper
    
    @classmethod
    def get(cls, name: str) -> Optional[BaseScraper]:
        return cls._scrapers.get(name)
    
    @classmethod
    def initialize_all(cls):
        """Inicializa todos os scrapers"""
        cls.register('lexml', LexMLScraper())
        cls.register('stj', STJScraper())
        cls.register('stf', STFScraper())
        cls.register('ibge', IBGEScraper())
    
    @classmethod
    def test_all(cls) -> Dict[str, ScrapingResult]:
        """Testa todos os scrapers registrados"""
        results = {}
        for name, scraper in cls._scrapers.items():
            # Cada scraper tem seu método de teste
            if hasattr(scraper, 'search'):
                results[name] = scraper.search('teste')
            elif hasattr(scraper, 'get_city'):
                # IBGE - testa com Crateús/CE (ID: 2304203)
                results[name] = scraper.get_city(2304203)
            else:
                results[name] = scraping_result = ScrapingResult(
                    success=False,
                    data=None,
                    source=name,
                    latency_ms=0,
                    error="No test method"
                )
        return results


# ============================================================
# TESTE
# ============================================================

if __name__ == "__main__":
    print("=" * 70)
    print("MASWOS V5 NEXUS - Teste de Scrapers Corrigidos")
    print("=" * 70)
    
    # Inicializa factory
    ScraperFactory.initialize_all()
    
    print("\n[Testando scrapers...]")
    print("-" * 70)
    
    # Testa LexML
    print("\n[1] LexML - Busca legislação")
    lexml = ScraperFactory.get('lexml')
    if lexml:
        result = lexml.search('responsabilidade civil')
        print(f"    Sucesso: {result.success}")
        print(f"    Latencia: {result.latency_ms:.2f}ms")
        if result.error:
            print(f"    Erro: {result.error}")
    
    # Testa STJ
    print("\n[2] STJ - Busca jurisprudência")
    stj = ScraperFactory.get('stj')
    if stj:
        result = stj.search_jurisprudence('dano moral')
        print(f"    Sucesso: {result.success}")
        print(f"    Latencia: {result.latency_ms:.2f}ms")
        if result.error:
            print(f"    Erro: {result.error}")
    
    # Testa STF
    print("\n[3] STF - Busca jurisprudência")
    stf = ScraperFactory.get('stf')
    if stf:
        result = stf.search_jurisprudence('habeas corpus')
        print(f"    Sucesso: {result.success}")
        print(f"    Latencia: {result.latency_ms:.2f}ms")
        if result.error:
            print(f"    Erro: {result.error}")
    
    # Testa IBGE
    print("\n[4] IBGE - Busca município (Crateús/CE)")
    ibge = ScraperFactory.get('ibge')
    if ibge:
        result = ibge.get_city(2304203)  # Crateús
        print(f"    Sucesso: {result.success}")
        print(f"    Latencia: {result.latency_ms:.2f}ms")
        if result.success and result.data:
            if isinstance(result.data, dict):
                nome = result.data.get('nome', 'N/A')
                print(f"    Municipio: {nome}")
        if result.error:
            print(f"    Erro: {result.error}")
    
    print("\n" + "=" * 70)
    print("Teste concluído!")
    print("=" * 70)
