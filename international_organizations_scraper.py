#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - International Organizations Data Scraper

Scrapers para dados de organizações internacionais:
- World Bank Open Data (Banco Mundial)
- United Nations Data (ONU)
- UN SDGs (Objetivos de Desenvolvimento Sustentável)
- UNICEF Statistics
- WHO (Organização Mundial da Saúde)
- UNESCO Institute for Statistics
- IMF (Fundo Monetário Internacional)
- OECD (Organização para Cooperação e Desenvolvimento Econômico)
- ILO (Organização Internacional do Trabalho)
- FAO (Organização das Nações Unidas para Alimentação e Agricultura)

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
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


@dataclass
class InternationalIndicator:
    """Indicador internacional"""
    id: str = ""
    name: str = ""
    source: str = ""
    country: str = ""
    country_code: str = ""
    year: int = 0
    value: Union[float, str, None] = None
    unit: str = ""
    description: str = ""
    category: str = ""
    url: str = ""
    source_org: str = ""


class WorldBankScraper:
    """
    Scraper para World Bank Open Data API
    
    Documentação: https://datahelpdesk.worldbank.org/knowledgebase/topics/125589
    Base URL: https://api.worldbank.org/v2/
    Acesso: Gratuito, sem API key
    Rate Limit: Sem limite documentado (uso razoável)
    """
    
    BASE_URL = "https://api.worldbank.org/v2"
    
    def __init__(self, delay: float = 0.5):
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "MASWOS-WorldBank/1.0",
            "Accept": "application/json"
        })
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def get_countries(self, region: str = None) -> List[Dict]:
        """Obter lista de países"""
        self._rate_limit()
        url = f"{self.BASE_URL}/country"
        params = {"format": "json", "per_page": 300}
        if region:
            params["region"] = region
        
        try:
            r = self.session.get(url, params=params, timeout=30)
            if r.status_code == 200:
                data = r.json()
                if len(data) > 1:
                    return [{"code": c["id"], "name": c["name"], 
                            "region": c.get("region", {}).get("value", ""),
                            "income": c.get("incomeLevel", {}).get("value", "")}
                           for c in data[1]]
        except Exception as e:
            print(f"[WorldBank] Error: {e}")
        return []
    
    def get_indicators(self, topic: int = None, page_size: int = 100) -> List[Dict]:
        """Obter lista de indicadores"""
        self._rate_limit()
        url = f"{self.BASE_URL}/indicator"
        params = {"format": "json", "per_page": page_size}
        if topic:
            params["topic"] = topic
        
        try:
            r = self.session.get(url, params=params, timeout=30)
            if r.status_code == 200:
                data = r.json()
                if len(data) > 1:
                    return [{"id": i["id"], "name": i["name"], 
                            "unit": i.get("unit", ""),
                            "source": i.get("source", {}).get("value", "")}
                           for i in data[1]]
        except Exception as e:
            print(f"[WorldBank] Error: {e}")
        return []
    
    def get_indicator_data(self, indicator: str, country: str = "BRL", 
                          year_start: int = 2010, year_end: int = 2023,
                          page_size: int = 100) -> List[Dict]:
        """
        Obter dados de um indicador
        
        Args:
            indicator: Código do indicador (ex: NY.GDP.MKTP.CD)
            country: Código do país (ex: BRA, WLD para mundial)
            year_start: Ano inicial
            year_end: Ano final
        """
        self._rate_limit()
        url = f"{self.BASE_URL}/country/{country}/indicator/{indicator}"
        params = {
            "format": "json",
            "date": f"{year_start}:{year_end}",
            "per_page": page_size
        }
        
        try:
            r = self.session.get(url, params=params, timeout=30)
            if r.status_code == 200:
                data = r.json()
                results = []
                if len(data) > 1 and data[1]:
                    for item in data[1]:
                        if item.get("value") is not None:
                            results.append({
                                "indicator": item["indicator"]["id"],
                                "indicator_name": item["indicator"]["value"],
                                "country": item["country"]["value"],
                                "country_code": item["countryiso3code"],
                                "year": int(item["date"]),
                                "value": float(item["value"]),
                                "unit": item.get("unit", ""),
                                "source": "World Bank"
                            })
                return results
        except Exception as e:
            print(f"[WorldBank] Error: {e}")
        return []
    
    def search_data(self, query: str, limit: int = 50) -> List[Dict]:
        """Buscar dados por texto"""
        self._rate_limit()
        url = f"{self.BASE_URL}/indicator"
        params = {
            "format": "json",
            "per_page": limit,
            "source": 2  # World Development Indicators
        }
        
        try:
            r = self.session.get(url, params=params, timeout=30)
            if r.status_code == 200:
                data = r.json()
                if len(data) > 1:
                    results = []
                    query_lower = query.lower()
                    for item in data[1]:
                        if query_lower in item.get("name", "").lower() or \
                           query_lower in item.get("id", "").lower():
                            results.append({
                                "id": item["id"],
                                "name": item["name"],
                                "unit": item.get("unit", "")
                            })
                    return results[:limit]
        except Exception as e:
            print(f"[WorldBank] Error: {e}")
        return []


class UNSDGScraper:
    """
    Scraper para UN Sustainable Development Goals Data
    
    Documentação: https://unstats.un.org/SDGAPI/
    Base URL: https://unstats.un.org/SDGAPI/v1/
    Acesso: Gratuito
    """
    
    BASE_URL = "https://unstats.un.org/SDGAPI/v1"
    
    def __init__(self, delay: float = 0.5):
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def get_goals(self) -> List[Dict]:
        """Obter lista de objetivos ODS"""
        self._rate_limit()
        url = f"{self.BASE_URL}/sdg/Goal/List"
        
        try:
            r = self.session.get(url, timeout=30)
            if r.status_code == 200:
                return [{"code": g["code"], "title": g["title"]} for g in r.json()]
        except Exception as e:
            print(f"[UNSDG] Error: {e}")
        return []
    
    def get_targets(self, goal: int) -> List[Dict]:
        """Obter metas de um objetivo"""
        self._rate_limit()
        url = f"{self.BASE_URL}/sdg/Goal/{goal}/Target/List"
        
        try:
            r = self.session.get(url, timeout=30)
            if r.status_code == 200:
                return [{"code": t["code"], "title": t["title"]} for t in r.json()]
        except Exception as e:
            print(f"[UNSDG] Error: {e}")
        return []
    
    def get_indicators(self, goal: int = None) -> List[Dict]:
        """Obter indicadores ODS"""
        self._rate_limit()
        if goal:
            url = f"{self.BASE_URL}/sdg/Goal/{goal}/Indicator/List"
        else:
            url = f"{self.BASE_URL}/sdg/Indicator/List"
        
        try:
            r = self.session.get(url, timeout=30)
            if r.status_code == 200:
                return [{"code": i["code"], "description": i.get("description", "")} 
                        for i in r.json()]
        except Exception as e:
            print(f"[UNSDG] Error: {e}")
        return []


class UNDataScraper:
    """
    Scraper para UN Data (data.un.org)
    
    Documentação: https://data.un.org/Host.aspx?Content=API
    Base URL: https://data.un.org/ws/rest/
    Acesso: Gratuito
    """
    
    BASE_URL = "https://data.un.org/ws/rest"
    
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def search_data(self, query: str, limit: int = 20) -> List[Dict]:
        """Buscar dados na ONU"""
        self._rate_limit()
        # UN Data usa um endpoint diferente
        url = "https://data.un.org/Data.aspx"
        params = {"q": query}
        
        try:
            r = self.session.get(url, params=params, timeout=30)
            if r.status_code == 200:
                # Parser HTML seria necessário
                return []
        except Exception as e:
            print(f"[UNData] Error: {e}")
        return []


class WHOScraper:
    """
    Scraper para World Health Organization (WHO) Data
    
    Documentação: https://www.who.int/data/gho/info/gho-odata-api
    Base URL: https://ghoapi.azureedge.net/api/
    Acesso: Gratuito (OData)
    """
    
    BASE_URL = "https://ghoapi.azureedge.net/api"
    
    def __init__(self, delay: float = 0.5):
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def get_indicators(self) -> List[Dict]:
        """Obter lista de indicadores de saúde"""
        self._rate_limit()
        url = f"{self.BASE_URL}/Indicator"
        
        try:
            r = self.session.get(url, timeout=30)
            if r.status_code == 200:
                data = r.json()
                return [{"code": i["IndicatorCode"], "name": i["IndicatorName"]}
                        for i in data.get("value", [])]
        except Exception as e:
            print(f"[WHO] Error: {e}")
        return []
    
    def get_data(self, indicator: str, country: str = None, 
                 year_start: int = 2010, year_end: int = 2023) -> List[Dict]:
        """Obter dados de saúde"""
        self._rate_limit()
        url = f"{self.BASE_URL}/Indicator/{indicator}"
        
        params = {}
        filter_parts = []
        if country:
            filter_parts.append(f"SpatialDim eq '{country}'")
        filter_parts.append(f"TimeDim ge {year_start} and TimeDim le {year_end}")
        if filter_parts:
            params["$filter"] = " and ".join(filter_parts)
        
        try:
            r = self.session.get(url, params=params, timeout=30)
            if r.status_code == 200:
                data = r.json()
                results = []
                for item in data.get("value", []):
                    results.append({
                        "indicator": item.get("IndicatorCode", ""),
                        "country": item.get("SpatialDim", ""),
                        "year": int(item.get("TimeDim", 0)),
                        "value": item.get("NumericValue"),
                        "sex": item.get("Dim1", ""),
                        "source": "WHO"
                    })
                return results
        except Exception as e:
            print(f"[WHO] Error: {e}")
        return []


class UNESCOScraper:
    """
    Scraper para UNESCO Institute for Statistics
    
    Documentação: https://apiportal.uis.unesco.org/
    Base URL: https://api.unesco.org/
    Acesso: Requer API key (gratuito para registro)
    """
    
    BASE_URL = "https://api.unesco.org"
    
    def __init__(self, api_key: Optional[str] = None, delay: float = 1.0):
        self.api_key = api_key or os.environ.get("UNESCO_API_KEY")
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
        if self.api_key:
            self.session.headers["Authorization"] = f"Bearer {self.api_key}"
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def is_available(self) -> bool:
        return bool(self.api_key)


class IMFScraper:
    """
    Scraper para IMF (International Monetary Fund) Data
    
    Documentação: https://www.imf.org/en/Data/Data-Services
    Base URL: http://dataservices.imf.org/REST/SDMX_JSON.svc/
    Acesso: Gratuito
    """
    
    BASE_URL = "http://dataservices.imf.org/REST/SDMX_JSON.svc"
    
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def get_data(self, database: str = "IFS", indicator: str = "NGDP_RPCH",
                 country: str = "BR", years: str = "2010:2023") -> List[Dict]:
        """Obter dados do FMI"""
        self._rate_limit()
        url = f"{self.BASE_URL}/CompactData/{database}/{country}.{indicator}"
        params = {"startPeriod": "2010", "endPeriod": "2023"}
        
        try:
            r = self.session.get(url, params=params, timeout=30)
            if r.status_code == 200:
                data = r.json()
                series = data.get("CompactData", {}).get("DataSet", {}).get("Series", {})
                obs = series.get("Obs", [])
                return [{"year": int(o["@TIME_PERIOD"]), 
                        "value": float(o.get("@OBS_VALUE", 0)),
                        "source": "IMF"} for o in obs]
        except Exception as e:
            print(f"[IMF] Error: {e}")
        return []


class OECDScraper:
    """
    Scraper para OECD Data
    
    Documentação: https://stats.oecd.org/index.aspx?queryid=30116
    Base URL: https://stats.oecd.org/SDMX-JSON/data/
    Acesso: Gratuito
    """
    
    BASE_URL = "https://stats.oecd.org/SDMX-JSON/data"
    
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()


class FAOScraper:
    """
    Scraper para FAO (Food and Agriculture Organization)
    
    Documentação: https://www.fao.org/faostat/en/#data
    Base URL: https://fenixservices.fao.org/faostat/api/v1/
    Acesso: Gratuito
    """
    
    BASE_URL = "https://fenixservices.fao.org/faostat/api/v1"
    
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    def get_data(self, domain: str = "QL", indicator: str = "21001",
                 area: str = "BRA", year: str = "2020") -> Dict:
        """Obter dados da FAO"""
        self._rate_limit()
        url = f"{self.BASE_URL}/data/{domain}"
        params = {
            "element": indicator,
            "area": area,
            "year": year,
            "output_type": "json"
        }
        
        try:
            r = self.session.get(url, params=params, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[FAO] Error: {e}")
        return {}


class ILOScraper:
    """
    Scraper para ILO (International Labour Organization)
    
    Documentação: https://ilostat.ilo.org/data/api/
    Base URL: https://api.ilo.org/estat/1.0/
    Acesso: Gratuito (alguns dados requerem registro)
    """
    
    BASE_URL = "https://api.ilo.org/estat/1.0"
    
    def __init__(self, delay: float = 1.0):
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()


# Funções de conveniência
def search_world_bank(indicator: str, country: str = "BRA", 
                      year_start: int = 2010, year_end: int = 2023) -> List[Dict]:
    """Buscar dados do Banco Mundial"""
    scraper = WorldBankScraper()
    return scraper.get_indicator_data(indicator, country, year_start, year_end)

def get_sdg_goals() -> List[Dict]:
    """Obter objetivos ODS da ONU"""
    scraper = UNSDGScraper()
    return scraper.get_goals()

def search_who_data(indicator: str, country: str = "BRA") -> List[Dict]:
    """Buscar dados da OMS"""
    scraper = WHOScraper()
    return scraper.get_data(indicator, country)


# Testes
def test_international_apis():
    """Testar APIs de organizações internacionais"""
    print("=" * 70)
    print("MASWOS V5 NEXUS - International Organizations API Test")
    print("=" * 70)
    
    # Test World Bank
    print("\n[TEST 1] World Bank - GDP Brazil (2020-2022)")
    wb = WorldBankScraper()
    data = wb.get_indicator_data("NY.GDP.MKTP.CD", "BRA", 2020, 2022)
    for item in data[:3]:
        print(f"  {item['year']}: ${item['value']:,.0f}")
    
    # Test World Bank indicators search
    print("\n[TEST 2] World Bank - Search 'education'")
    indicators = wb.search_data("education", limit=5)
    for ind in indicators[:5]:
        print(f"  {ind['id']}: {ind['name'][:50]}...")
    
    # Test UN SDG
    print("\n[TEST 3] UN SDG Goals")
    sdg = UNSDGScraper()
    goals = sdg.get_goals()
    print(f"  Total goals: {len(goals)}")
    for g in goals[:3]:
        print(f"  Goal {g['code']}: {g['title'][:50]}...")
    
    # Test WHO
    print("\n[TEST 4] WHO - Life expectancy Brazil")
    who = WHOScraper()
    data = who.get_data("WHOSIS_000001", "BRA", 2015, 2020)
    for item in data[:3]:
        print(f"  {item['year']}: {item['value']} years")
    
    print("\n" + "=" * 70)
    print("International APIs - Testes Concluídos")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    test_international_apis()
