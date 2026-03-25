#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - IBGE Complete API Scraper

API Documentation: https://servicodados.ibge.gov.br/api/docs/
Base URL: https://servicodados.ibge.gov.br/api/v1/
Acesso: Gratuito, sem API key

APIs disponíveis:
- Agregados: /api/v3/agregados/ - Estatísticas multidimensionais
- Localidades: /api/v1/localidades/ - Divisões administrativas
- Nomes: /api/v2/v1/nomes/ - Nomes no Brasil
- Malhas: /api/v3/malhas/ - Malhas geográficas
- CNAE: /api/v2/v1/cnae/ - Classificação de atividades
- Países: /api/v1/paises/ - Indicadores socioeconômicos
- Pesquisas: /api/v1/pesquisas/ - Pesquisas estatísticas
- Noticias: /api/v3/noticias/ - News e releases
- Produtos: /api/v1/produtos/ - Produtos estatísticos
- Calendário: /api/v3/calendario/ - Cronograma de publicações
- BNGB: /api/v1/bngb/ - Banco de Nomes Geográficos
- Metadados: /api/v2/metadados/ - Metadados das pesquisas

Arquitetura: Transformer-Agentes (Encoder → API → Parser → Decoder)
"""

import requests
import time
import json
from pathlib import Path
from typing import Dict, List, Optional, Any, Union
from dataclasses import dataclass, field
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class IBGECompleteScraper:
    """
    Scraper completo para todas as APIs do IBGE
    
    Conforme documentação: https://servicodados.ibge.gov.br/api/docs/
    """
    
    BASE_URL = "https://servicodados.ibge.gov.br/api/v1"
    BASE_URL_V2 = "https://servicodados.ibge.gov.br/api/v2"
    BASE_URL_V3 = "https://servicodados.ibge.gov.br/api/v3"
    
    def __init__(self, delay: float = 0.5):
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "MASWOS-IBGE/1.0",
            "Accept": "application/json"
        })
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    # ==================== LOCALIDADES ====================
    
    def get_localidades(self, nivel: str = "municipio") -> List[Dict]:
        """
        Obter localidades do Brasil
        
        Níveis: pais, regiao, estado, mesorregiao, microrregiao, municipio
        """
        self._rate_limit()
        url = f"{self.BASE_URL}/localidades/{nivel}"
        try:
            r = self.session.get(url, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[IBGE] Error: {e}")
        return []
    
    def get_estados(self) -> List[Dict]:
        """Obter lista de estados"""
        return self.get_localidades("estados")
    
    def get_municipios(self, estado_id: int = None) -> List[Dict]:
        """Obter municípios"""
        self._rate_limit()
        if estado_id:
            url = f"{self.BASE_URL}/localidades/estados/{estado_id}/municipios"
        else:
            url = f"{self.BASE_URL}/localidades/municipios"
        try:
            r = self.session.get(url, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[IBGE] Error: {e}")
        return []
    
    # ==================== NOMES ====================
    
    def get_nomes(self, nome: str = None, sexo: str = None, 
                  decada: int = None, limit: int = 50) -> List[Dict]:
        """
        Consultar frequência de nomes no Brasil
        
        Args:
            nome: Nome específico
            sexo: M ou F
            decada: Década (ex: 1950)
            limit: Limite de resultados
        """
        self._rate_limit()
        url = f"{self.BASE_URL_V2}/v1/nomes/{nome if nome else ''}"
        params = {"limit": limit}
        if sexo:
            params["sexo"] = sexo
        if decada:
            params["decada"] = decada
        
        try:
            r = self.session.get(url, params=params, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[IBGE] Error: {e}")
        return []
    
    def ranking_nomes(self, sexo: str = "M", decada: int = 2010) -> List[Dict]:
        """Ranking de nomes mais frequentes"""
        self._rate_limit()
        url = f"{self.BASE_URL_V2}/v1/nomes/ranking/{decada}"
        params = {"sexo": sexo}
        try:
            r = self.session.get(url, params=params, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[IBGE] Error: {e}")
        return []
    
    # ==================== AGREGADOS ====================
    
    def get_agregados(self) -> List[Dict]:
        """Listar agregados disponíveis"""
        self._rate_limit()
        url = f"{self.BASE_URL_V3}/agregados"
        try:
            r = self.session.get(url, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[IBGE] Error: {e}")
        return []
    
    def get_agregado(self, agregado_id: int) -> Optional[Dict]:
        """Obter detalhes de um agregado"""
        self._rate_limit()
        url = f"{self.BASE_URL_V3}/agregados/{agregado_id}"
        try:
            r = self.session.get(url, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[IBGE] Error: {e}")
        return None
    
    def get_agregado_periodos(self, agregado_id: int) -> List[Dict]:
        """Obter períodos de um agregado"""
        self._rate_limit()
        url = f"{self.BASE_URL_V3}/agregados/{agregado_id}/periodos"
        try:
            r = self.session.get(url, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[IBGE] Error: {e}")
        return []
    
    def get_agregado_variaveis(self, agregado_id: int) -> List[Dict]:
        """Obter variáveis de um agregado"""
        self._rate_limit()
        url = f"{self.BASE_URL_V3}/agregados/{agregado_id}/variaveis"
        try:
            r = self.session.get(url, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[IBGE] Error: {e}")
        return []
    
    def get_agregado_valores(self, agregado_id: int, variaveis: str = "all",
                             nivel_territorial: str = "N1", 
                             localidades: str = "all",
                             periodo: str = "last") -> Dict:
        """
        Obter valores de um agregado
        
        Args:
            agregado_id: ID do agregado
            variaveis: IDs das variáveis (ex: "93" ou "all")
            nivel_territorial: N1=Brasil, N2=Região, N3=Estado, N4=Município
            localidades: IDs das localidades ou "all"
            periodo: "last" ou período específico (ex: "2022")
        """
        self._rate_limit()
        url = f"{self.BASE_URL_V3}/agregados/{agregado_id}/periodos/{periodo}/variaveis/{variaveis}"
        params = {
            "localidades": f"{nivel_territorial}[{localidades}]"
        }
        try:
            r = self.session.get(url, params=params, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[IBGE] Error: {e}")
        return {}
    
    # ==================== PESQUISAS ====================
    
    def get_pesquisas(self) -> List[Dict]:
        """Listar pesquisas disponíveis"""
        self._rate_limit()
        url = f"{self.BASE_URL}/pesquisas"
        try:
            r = self.session.get(url, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[IBGE] Error: {e}")
        return []
    
    def get_pesquisa(self, pesquisa_id: int) -> Optional[Dict]:
        """Obter detalhes de uma pesquisa"""
        self._rate_limit()
        url = f"{self.BASE_URL}/pesquisas/{pesquisa_id}"
        try:
            r = self.session.get(url, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[IBGE] Error: {e}")
        return None
    
    # ==================== PAÍSES ====================
    
    def get_paises(self) -> List[Dict]:
        """Obter indicadores de países"""
        self._rate_limit()
        url = f"{self.BASE_URL}/paises"
        try:
            r = self.session.get(url, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[IBGE] Error: {e}")
        return []
    
    # ==================== CNAE ====================
    
    def get_cnae(self, nivel: str = "subclasse") -> List[Dict]:
        """
        Obter classificação CNAE
        
        Níveis: secao, divisao, grupo, classe, subclasse
        """
        self._rate_limit()
        url = f"{self.BASE_URL_V2}/v1/cnae/{nivel}"
        try:
            r = self.session.get(url, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[IBGE] Error: {e}")
        return []
    
    # ==================== NOTÍCIAS ====================
    
    def get_noticias(self, pagina: int = 1, tamanho_pagina: int = 10) -> Dict:
        """Obter notícias e releases"""
        self._rate_limit()
        url = f"{self.BASE_URL_V3}/noticias"
        params = {"page": pagina, "page-size": tamanho_pagina}
        try:
            r = self.session.get(url, params=params, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[IBGE] Error: {e}")
        return {}
    
    # ==================== PRODUTOS ====================
    
    def get_produtos(self) -> List[Dict]:
        """Listar produtos estatísticos"""
        self._rate_limit()
        url = f"{self.BASE_URL}/produtos"
        try:
            r = self.session.get(url, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[IBGE] Error: {e}")
        return []
    
    # ==================== CALENDÁRIO ====================
    
    def get_calendario(self, ano: int = None) -> List[Dict]:
        """Obter calendário de publicações"""
        self._rate_limit()
        url = f"{self.BASE_URL_V3}/calendario"
        params = {}
        if ano:
            params["ano"] = ano
        try:
            r = self.session.get(url, params=params, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[IBGE] Error: {e}")
        return []
    
    # ==================== MALHAS ====================
    
    def get_malha(self, nivel: str = "estados", versao: int = 4) -> Dict:
        """
        Obter malha geográfica
        
        Níveis: Brasil, regiao, estados, mesorregiao, microrregiao, municipio
        """
        self._rate_limit()
        url = f"https://servicodados.ibge.gov.br/api/v{versao}/malhas/{nivel}"
        params = {"formato": "application/vnd.geo+json"}
        try:
            r = self.session.get(url, params=params, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[IBGE] Error: {e}")
        return {}
    
    # ==================== BNGB ====================
    
    def get_nomes_geograficos(self, termo: str = "", limit: int = 50) -> List[Dict]:
        """Buscar nomes geográficos"""
        self._rate_limit()
        url = f"{self.BASE_URL}/bngb"
        params = {"q": termo, "limit": limit}
        try:
            r = self.session.get(url, params=params, timeout=30)
            if r.status_code == 200:
                return r.json()
        except Exception as e:
            print(f"[IBGE] Error: {e}")
        return []


# ==================== FUNÇÕES DE CONVENIÊNCIA ====================

def search_ibge_names(name: str) -> List[Dict]:
    """Buscar frequência de um nome"""
    scraper = IBGECompleteScraper()
    return scraper.get_nomes(name)

def get_ibge_municipios(state_code: int) -> List[Dict]:
    """Obter municípios de um estado"""
    scraper = IBGECompleteScraper()
    return scraper.get_municipios(state_code)

def get_ibge_population() -> Dict:
    """Obter dados populacionais (Agregado 4714 - População residente)"""
    scraper = IBGECompleteScraper()
    return scraper.get_agregado_valores(4714, periodo="last")


# ==================== TESTES ====================

def test_ibge_apis():
    """Testar APIs do IBGE"""
    print("=" * 70)
    print("MASWOS V5 NEXUS - IBGE Complete APIs Test")
    print("=" * 70)
    
    ibge = IBGECompleteScraper()
    
    # Test 1: Estados
    print("\n[TEST 1] Estados")
    estados = ibge.get_estados()
    print(f"  Total estados: {len(estados)}")
    for e in estados[:3]:
        print(f"  - {e.get('nome', '')} ({e.get('sigla', '')})")
    
    # Test 2: Municípios de SP
    print("\n[TEST 2] Municípios de São Paulo")
    sp = ibge.get_municipios(35)  # SP = 35
    print(f"  Total municípios SP: {len(sp)}")
    for m in sp[:3]:
        print(f"  - {m.get('nome', '')}")
    
    # Test 3: Nomes
    print("\n[TEST 3] Nome 'Maria'")
    nomes = ibge.get_nomes("Maria", sexo="F", limit=5)
    print(f"  Resultados: {len(nomes)}")
    for n in nomes[:3]:
        print(f"  - {n.get('nome', '')}: {n.get('frequencia', 0)}")
    
    # Test 4: Ranking
    print("\n[TEST 4] Ranking de nomes (masculino, década 2010)")
    ranking = ibge.ranking_nomes("M", 2010)
    print(f"  Resultados: {len(ranking)}")
    for r in ranking[:5]:
        print(f"  - {r.get('nome', '')}: {r.get('frequencia', 0)}")
    
    # Test 5: Agregados disponíveis
    print("\n[TEST 5] Primeiros agregados")
    agregados = ibge.get_agregados()
    print(f"  Total agregados: {len(agregados)}")
    for a in agregados[:3]:
        print(f"  - {a.get('ID', '')}: {a.get('Nome', '')[:50]}...")
    
    # Test 6: Países
    print("\n[TEST 6] Países")
    paises = ibge.get_paises()
    print(f"  Total países: {len(paises)}")
    
    print("\n" + "=" * 70)
    print("IBGE APIs - Testes Concluídos")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    test_ibge_apis()
