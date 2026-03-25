#!/usr/bin/env python3
"""
MASWOS V5 NEXUS - CAPES Dados Abertos Scraper

API Documentation: https://dadosabertos.capes.gov.br
Portal: https://www.gov.br/capes

Dados disponíveis:
- Acessos ao Portal de Periódicos (2023-2025)
- Dados por: Ano, UF, Estado, Município, Região, IES
- Formatos: CSV, XLSX
- Licença: Creative Commons Atribuição (CC BY)

Arquitetura: Transformer-Agentes (Encoder → Download → Parse → Store)
"""

import requests
import time
import json
import os
import csv
from pathlib import Path
from typing import Dict, List, Optional, Any
from dataclasses import dataclass, field
from datetime import datetime
import urllib3

urllib3.disable_warnings(urllib3.exceptions.InsecureRequestWarning)


class CAPESScraper:
    """
    Scraper para dados abertos da CAPES
    
    Conforme: https://dadosabertos.capes.gov.br
    """
    
    BASE_URL = "https://dadosabertos.capes.gov.br"
    CKAN_URL = "https://dadosabertos.capes.gov.br/api/3/action"
    
    # Downloads diretos dos arquivos
    RESOURCES = {
        "acessos_2023_csv": {
            "url": "https://dadosabertos.capes.gov.br/dataset/7d357e84-814d-423f-b27a-a9b80520189b/resource/7cd574be-7a3d-4750-a246-2ed0a7573073/download/br-capes-acessos-portal-periodicos-2023-2025-06-01.csv",
            "ano": 2023,
            "formato": "CSV"
        },
        "acessos_2023_xlsx": {
            "url": "https://dadosabertos.capes.gov.br/dataset/7d357e84-814d-423f-b27a-a9b80520189b/resource/95a82ab5-88b4-4ec0-afd7-f9c281239248/download/br-capes-acessos-portal-periodicos-2023-2025-06-01.xlsx",
            "ano": 2023,
            "formato": "XLSX"
        },
        "acessos_2024_csv": {
            "url": "https://dadosabertos.capes.gov.br/dataset/7d357e84-814d-423f-b27a-a9b80520189b/resource/2cc363d3-987d-4feb-8542-d3819148b5dc/download/br-capes-acessos-portal-periodicos-2024-2025-06-01.csv",
            "ano": 2024,
            "formato": "CSV"
        },
        "acessos_2024_xlsx": {
            "url": "https://dadosabertos.capes.gov.br/dataset/7d357e84-814d-423f-b27a-a9b80520189b/resource/f8dd2446-914c-4782-a1ea-7025e3fe05b1/download/br-capes-acessos-portal-periodicos-2024-2025-06-01.xlsx",
            "ano": 2024,
            "formato": "XLSX"
        }
    }
    
    def __init__(self, data_dir: str = "capes_data", delay: float = 1.0):
        self.data_dir = Path(data_dir)
        self.data_dir.mkdir(exist_ok=True)
        self.delay = delay
        self.last_request_time = 0
        self.session = requests.Session()
        self.session.headers.update({
            "User-Agent": "MASWOS-CAPES/1.0",
            "Accept": "*/*"
        })
    
    def _rate_limit(self):
        elapsed = time.time() - self.last_request_time
        if elapsed < self.delay:
            time.sleep(self.delay - elapsed)
        self.last_request_time = time.time()
    
    # ==================== CKAN API ====================
    
    def list_datasets(self, limit: int = 50) -> List[Dict]:
        """Listar datasets disponíveis"""
        self._rate_limit()
        url = f"{self.CKAN_URL}/package_list"
        
        try:
            response = self.session.get(url, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return data.get("result", [])
        except Exception as e:
            print(f"[CAPES] Error: {e}")
        
        return []
    
    def get_dataset(self, dataset_id: str) -> Optional[Dict]:
        """Obter metadados de um dataset"""
        self._rate_limit()
        url = f"{self.CKAN_URL}/package_show"
        params = {"id": dataset_id}
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return data.get("result")
        except Exception as e:
            print(f"[CAPES] Error: {e}")
        
        return None
    
    def search_datasets(self, query: str, limit: int = 20) -> List[Dict]:
        """Buscar datasets por termo"""
        self._rate_limit()
        url = f"{self.CKAN_URL}/package_search"
        params = {"q": query, "rows": limit}
        
        try:
            response = self.session.get(url, params=params, timeout=30)
            if response.status_code == 200:
                data = response.json()
                if data.get("success"):
                    return data.get("result", {}).get("results", [])
        except Exception as e:
            print(f"[CAPES] Error: {e}")
        
        return []
    
    # ==================== DOWNLOADS ====================
    
    def download_resource(self, resource_key: str, force: bool = False) -> Optional[Path]:
        """Download de recurso"""
        if resource_key not in self.RESOURCES:
            print(f"[CAPES] Resource '{resource_key}' não encontrado")
            return None
        
        resource = self.RESOURCES[resource_key]
        filename = resource["url"].split("/")[-1]
        filepath = self.data_dir / filename
        
        if filepath.exists() and not force:
            print(f"[CAPES] Arquivo já existe: {filepath}")
            return filepath
        
        self._rate_limit()
        print(f"[CAPES] Downloading: {filename}")
        
        try:
            response = self.session.get(resource["url"], timeout=120, stream=True)
            
            if response.status_code == 200:
                with open(filepath, "wb") as f:
                    for chunk in response.iter_content(chunk_size=8192):
                        f.write(chunk)
                print(f"[CAPES] Salvo: {filepath}")
                return filepath
            else:
                print(f"[CAPES] HTTP {response.status_code}")
                
        except Exception as e:
            print(f"[CAPES] Download error: {e}")
        
        return None
    
    def download_all_acessos(self) -> Dict[str, Path]:
        """Download de todos os arquivos de acesso"""
        results = {}
        for key in ["acessos_2023_csv", "acessos_2024_csv"]:
            filepath = self.download_resource(key)
            if filepath:
                results[key] = filepath
        return results
    
    # ==================== PARSING ====================
    
    def parse_csv(self, filepath: Path) -> List[Dict]:
        """Parser para CSV da CAPES"""
        results = []
        
        # Colunas reais do CSV:
        # AN_REFERENCIA, SG_UF, NM_UF, NM_MUNICIPIO, NM_REGIAO, CD_IES, SG_IES, NM_IES
        # NR_TC, NR_TC_TDM, NR_TR_SEARCHES, NR_TR_OUTROS, NR_TR_TDM
        
        try:
            with open(filepath, "r", encoding="latin-1") as f:
                reader = csv.DictReader(f, delimiter=";")
                for row in reader:
                    try:
                        results.append({
                            "ano": int(row.get("AN_REFERENCIA", 0) or 0),
                            "uf": row.get("SG_UF", ""),
                            "estado": row.get("NM_UF", ""),
                            "municipio": row.get("NM_MUNICIPIO", ""),
                            "regiao": row.get("NM_REGIAO", ""),
                            "ies_codigo": row.get("CD_IES", ""),
                            "ies_sigla": row.get("SG_IES", ""),
                            "ies_nome": row.get("NM_IES", ""),
                            "texto_completo": int(row.get("NR_TC", 0) or 0),
                            "texto_completo_tdm": int(row.get("NR_TC_TDM", 0) or 0),
                            "texto_referencial_searches": int(row.get("NR_TR_SEARCHES", 0) or 0),
                            "texto_referencial_outros": int(row.get("NR_TR_OUTROS", 0) or 0),
                            "texto_referencial_tdm": int(row.get("NR_TR_TDM", 0) or 0),
                            "source": "capes"
                        })
                    except Exception as e:
                        pass  # Skip malformed rows
                        
        except Exception as e:
            print(f"[CAPES] CSV parse error: {e}")
        
        return results
    
    def get_acessos_by_year(self, ano: int) -> List[Dict]:
        """Obter acessos de um ano específico"""
        key = f"acessos_{ano}_csv"
        filepath = self.download_resource(key)
        if filepath:
            return self.parse_csv(filepath)
        return []
    
    def get_acessos_summary(self) -> Dict:
        """Resumo dos acessos por ano"""
        summary = {}
        
        for ano in [2023, 2024]:
            acessos = self.get_acessos_by_year(ano)
            if acessos:
                total_tc = sum(a["texto_completo"] for a in acessos)
                total_tc_tdm = sum(a["texto_completo_tdm"] for a in acessos)
                total_tr = sum(a["texto_referencial_searches"] + a["texto_referencial_outros"] for a in acessos)
                ufs = list(set(a["uf"] for a in acessos if a["uf"]))
                ies = list(set(a["ies_nome"] for a in acessos if a["ies_nome"]))
                regioes = list(set(a["regiao"] for a in acessos if a["regiao"]))
                
                summary[str(ano)] = {
                    "total_registros": len(acessos),
                    "total_texto_completo": total_tc,
                    "total_texto_completo_tdm": total_tc_tdm,
                    "total_texto_referencial": total_tr,
                    "total_geral": total_tc + total_tr,
                    "ufs": len(ufs),
                    "ies": len(ies),
                    "regioes": len(regioes),
                    "lista_ufs": sorted(ufs),
                    "lista_regioes": sorted(regioes)
                }
            else:
                summary[str(ano)] = {"total_registros": 0}
        
        return summary
    
    def get_top_ies(self, ano: int = 2023, limit: int = 10) -> List[Dict]:
        """Top IES por número de acessos"""
        acessos = self.get_acessos_by_year(ano)
        
        # Agregar por IES
        ies_dict = {}
        for a in acessos:
            ies_name = a.get("ies_nome", "Desconhecido")
            if ies_name not in ies_dict:
                ies_dict[ies_name] = {
                    "ies": ies_name,
                    "uf": a.get("uf", ""),
                    "regiao": a.get("regiao", ""),
                    "total_acessos": 0
                }
            ies_dict[ies_name]["total_acessos"] += a["texto_completo"] + a["texto_referencial_searches"]
        
        # Ordenar
        sorted_ies = sorted(ies_dict.values(), key=lambda x: x["total_acessos"], reverse=True)
        return sorted_ies[:limit]
    
    def get_top_ufs(self, ano: int = 2023, limit: int = 10) -> List[Dict]:
        """Top UFs por número de acessos"""
        acessos = self.get_acessos_by_year(ano)
        
        # Agregar por UF
        uf_dict = {}
        for a in acessos:
            uf = a.get("uf", "Desconhecido")
            if uf not in uf_dict:
                uf_dict[uf] = {
                    "uf": uf,
                    "estado": a.get("estado", ""),
                    "regiao": a.get("regiao", ""),
                    "total_acessos": 0
                }
            uf_dict[uf]["total_acessos"] += a["texto_completo"] + a["texto_referencial_searches"]
        
        # Ordenar
        sorted_ufs = sorted(uf_dict.values(), key=lambda x: x["total_acessos"], reverse=True)
        return sorted_ufs[:limit]


# ==================== FUNÇÕES DE CONVENIÊNCIA ====================

def download_capes_data() -> Dict[str, Path]:
    """Download dos dados da CAPES"""
    scraper = CAPESScraper()
    return scraper.download_all_acessos()

def get_capes_summary() -> Dict:
    """Obter resumo dos acessos CAPES"""
    scraper = CAPESScraper()
    return scraper.get_acessos_summary()

def search_capes_datasets(query: str) -> List[Dict]:
    """Buscar datasets na CAPES"""
    scraper = CAPESScraper()
    return scraper.search_datasets(query)


# ==================== TESTES ====================

def test_capes_scraper():
    """Testar scraper CAPES"""
    print("=" * 70)
    print("MASWOS V5 NEXUS - CAPES Dados Abertos Test")
    print("=" * 70)
    
    scraper = CAPESScraper()
    
    # Test 1: Listar datasets
    print("\n[TEST 1] Listar datasets disponíveis")
    datasets = scraper.list_datasets(limit=10)
    print(f"  Total datasets: {len(datasets)}")
    for d in datasets[:5]:
        print(f"  - {d}")
    
    # Test 2: Buscar datasets de acesso
    print("\n[TEST 2] Buscar: 'acessos'")
    results = scraper.search_datasets("acessos", limit=5)
    for r in results[:3]:
        print(f"  - {r.get('title', '')}")
    
    # Test 3: Download 2023
    print("\n[TEST 3] Download dados 2023")
    filepath = scraper.download_resource("acessos_2023_csv")
    if filepath:
        print(f"  Arquivo: {filepath}")
        print(f"  Tamanho: {filepath.stat().st_size / 1024:.1f} KB")
        
        # Parse
        data = scraper.parse_csv(filepath)
        print(f"  Registros: {len(data)}")
        if data:
            print(f"  Exemplo: {data[0]}")
    
    # Test 4: Resumo
    print("\n[TEST 4] Resumo dos acessos")
    summary = scraper.get_acessos_summary()
    for ano, stats in summary.items():
        if stats:
            print(f"  Ano {ano}:")
            print(f"    Total acessos: {stats.get('total_geral', 0):,}")
            print(f"    Texto completo: {stats.get('total_texto_completo', 0):,}")
            print(f"    IES: {stats.get('ies', 0)}")
    
    print("\n" + "=" * 70)
    print("CAPES Scraper - Testes Concluídos")
    print("=" * 70)
    
    return True


if __name__ == "__main__":
    test_capes_scraper()
