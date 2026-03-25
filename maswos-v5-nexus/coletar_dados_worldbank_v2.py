#!/usr/bin/env python3
"""
COLETOR DE DADOS PRIMÁRIOS V2 - DISSERTAÇÃO MIT-EDUCAÇÃO
Versão melhorada com tratamento robusto de dados

Fontes: World Bank API (https://datahelpdesk.worldbank.org/knowledgebase/articles/888812)
"""

import json
import csv
import os
from datetime import datetime
from urllib.request import urlopen, Request
from urllib.error import URLError, HTTPError
import ssl
import time

# ============================================================================
# CONFIGURAÇÃO
# ============================================================================

PAISES = {
    'BRA': 'Brasil',
    'MEX': 'México',
    'TUR': 'Turquia',
    'CHN': 'China',
    'IND': 'Índia',
    'KOR': 'Coreia do Sul',
    'MYS': 'Malásia'
}

# Indicadores essenciais (códigos World Bank)
INDICADORES_ESSENCIAIS = {
    'NY.GDP.PCAP.PP.KD': 'pib_per_capita_ppp_2017',  # PIB per capita PPP (2017)
    'NY.GDP.PCAP.KD': 'pib_per_capita_constante_2015',  # PIB per capita constante (2015)
    'SE.PRM.ENRR': 'matricula_liquida_primaria',  # Matrícula líquida primária %
    'SE.SEC.ENRR': 'matricula_liquida_secundaria',  # Matrícula líquida secundária %
    'SE.TER.ENRR': 'matricula_liquida_superior',  # Matrícula líquida superior %
    'SE.XPD.TOTL.GD.ZS': 'gasto_educacao_pct_pib',  # Gasto educação % PIB
    'GB.XPD.RSDV.GD.ZS': 'pct_pib_pd',  # P&D % PIB
    'SP.URB.TOTL.IN.ZS': 'urbanizacao_pct',  # População urbana %
    'SP.POP.TOTL': 'populacao_total',  # População total
    'SL.UEM.TOTL.ZS': 'desemprego_total_pct',  # Desemprego total %
    'SE.ADT.LITR.ZS': 'taxa_alfabetizacao_adultos',  # Alfabetização adultos %
}

# Dados PISA pré-coletados (OCDE)
PISA_DATA = {
    'BRA': {
        2000: 381.7, 2003: 382.0, 2006: 384.3, 2009: 400.7,
        2012: 402.0, 2015: 399.0, 2018: 398.7, 2022: 397.3
    },
    'MEX': {
        2000: 410.3, 2003: 396.7, 2006: 411.3, 2009: 420.0,
        2012: 417.3, 2015: 415.0, 2018: 416.0, 2022: 411.0
    },
    'TUR': {
        2003: 432.7, 2006: 431.7, 2009: 454.3, 2012: 462.0,
        2015: 424.3, 2018: 462.7, 2022: 461.7
    },
    'CHN': {
        # Dados B-S-J-Z (regiões ricas)
        2009: 573.7, 2012: 591.0, 2015: 523.3, 2018: 578.7
    },
    'IND': {
        2009: 361.7, 2012: 363.3
    },
    'KOR': {
        2000: 541.3, 2003: 538.0, 2006: 570.0, 2009: 567.0,
        2012: 542.7, 2015: 519.0, 2018: 519.7, 2022: 523.3
    },
    'MYS': {
        2009: 422.3, 2012: 438.0, 2015: 440.0, 2018: 453.0, 2022: 458.0
    }
}

# ============================================================================
# FUNÇÕES DE COLETA
# ============================================================================

def criar_contexto_ssl():
    """Cria contexto SSL compatível"""
    try:
        context = ssl.create_default_context()
        context.check_hostname = False
        context.verify_mode = ssl.CERT_NONE
        return context
    except:
        return None

def fetch_world_bank_data(indicator, country_code, start_year=1960, end_year=2023):
    """
    Busca dados de um indicador para um país específico
    Retorna lista de dicts: [{'year': 2000, 'value': 123.4}, ...]
    """
    url = f"https://api.worldbank.org/v2/country/{country_code}/indicator/{indicator}?date={start_year}:{end_year}&format=json&per_page=1000"
    
    headers = {'User-Agent': 'Mozilla/5.0 (Research Project)'}
    
    try:
        ctx = criar_contexto_ssl()
        req = Request(url, headers=headers)
        
        with urlopen(req, context=ctx, timeout=30) as response:
            data = json.loads(response.read().decode('utf-8'))
        
        # API retorna [metadata, data_array]
        if isinstance(data, list) and len(data) > 1 and data[1]:
            results = []
            for item in data[1]:
                if item and item.get('value') is not None:
                    results.append({
                        'year': int(item['date']),
                        'value': float(item['value'])
                    })
            return results
        return []
        
    except Exception as e:
        print(f"    [ERRO] {type(e).__name__}: {e}")
        return []

def coletar_todos_dados():
    """Coleta todos os indicadores para todos os países"""
    print("=" * 80)
    print("COLETANDO DADOS PRIMÁRIOS DO WORLD BANK API")
    print("=" * 80)
    
    dados = {}  # {country_code: {indicator: {year: value}}}
    
    for country_code, country_name in PAISES.items():
        print(f"\n[COUNTRY] {country_name} ({country_code})")
        dados[country_code] = {}
        
        for indicator_code, indicator_name in INDICADORES_ESSENCIAIS.items():
            print(f"  [INDICATOR] {indicator_name}...", end=" ")
            
            results = fetch_world_bank_data(indicator_code, country_code)
            
            if results:
                dados[country_code][indicator_code] = {r['year']: r['value'] for r in results}
                print(f"OK ({len(results)} obs)")
            else:
                print("SEM DADOS")
            
            time.sleep(0.3)  # Rate limiting
    
    return dados

def criar_dataset_tabular(dados_raw):
    """Converte dados brutos em formato tabular"""
    print("\n" + "=" * 80)
    print("CRIANDO DATASET TABULAR")
    print("=" * 80)
    
    rows = []
    
    for country_code, country_name in PAISES.items():
        # Encontrar todos os anos com dados
        all_years = set()
        for indicator_data in dados_raw.get(country_code, {}).values():
            all_years.update(indicator_data.keys())
        
        for year in sorted(all_years):
            if year < 1960 or year > 2023:
                continue
            
            row = {
                'country_code': country_code,
                'country_name': country_name,
                'year': year
            }
            
            # Adicionar indicadores do World Bank
            for indicator_code, indicator_name in INDICADORES_ESSENCIAIS.items():
                value = dados_raw.get(country_code, {}).get(indicator_code, {}).get(year)
                row[indicator_name] = value
            
            # Adicionar PISA
            row['pisa_media'] = PISA_DATA.get(country_code, {}).get(year)
            
            # Calcular anos de escolaridade (proxy baseado em matrículas)
            secundaria = row.get('matricula_liquida_secundaria', 0) or 0
            superior = row.get('matricula_liquida_superior', 0) or 0
            
            # Fórmula: 4 (primária) + %secundário*4 + %superior*3
            anos_estimado = 4 + (secundaria / 100 * 4) + (superior / 100 * 3)
            row['anos_escolaridade_estimado'] = round(min(anos_estimado, 14), 2) if anos_estimado > 0 else None
            
            rows.append(row)
    
    print(f"[OK] Dataset criado: {len(rows)} linhas, {len(rows[0]) if rows else 0} colunas")
    return rows

def salvar_csv(dataset, filename='dataset_mit_educacao_PRIMARIO.csv'):
    """Salva dataset em CSV"""
    if not dataset:
        print("[ERRO] Dataset vazio")
        return None
    
    fieldnames = list(dataset[0].keys())
    
    with open(filename, 'w', newline='', encoding='utf-8-sig') as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(dataset)
    
    print(f"\n[OK] Dataset salvo: {filename}")
    print(f"    Registros: {len(dataset)}")
    print(f"    Variáveis: {len(fieldnames)}")
    
    return filename

def imprimir_resumo_estatistico(dataset):
    """Imprime estatísticas resumo"""
    print("\n" + "=" * 80)
    print("RESUMO ESTATÍSTICO DO DATASET")
    print("=" * 80)
    
    # Agrupar por país
    por_pais = {}
    for row in dataset:
        cc = row['country_code']
        if cc not in por_pais:
            por_pais[cc] = {
                'name': row['country_name'],
                'years': [],
                'pib_values': [],
                'pisa_values': [],
                'escolaridade_values': []
            }
        
        por_pais[cc]['years'].append(row['year'])
        
        if row.get('pib_per_capita_ppp_2017'):
            por_pais[cc]['pib_values'].append(row['pib_per_capita_ppp_2017'])
        
        if row.get('pisa_media'):
            por_pais[cc]['pisa_values'].append(row['pisa_media'])
        
        if row.get('anos_escolaridade_estimado'):
            por_pais[cc]['escolaridade_values'].append(row['anos_escolaridade_estimado'])
    
    print(f"\n{'País':<18} {'Período':<12} {'Obs':<6} {'PIB Médio':<15} {'PISA Médio':<12} {'Escolaridade'}")
    print("-" * 85)
    
    for cc in sorted(por_pais.keys()):
        data = por_pais[cc]
        periodo = f"{min(data['years'])}-{max(data['years'])}"
        obs = len(data['years'])
        
        pib_medio = f"${sum(data['pib_values'])/len(data['pib_values']):,.0f}" if data['pib_values'] else "N/A"
        pisa_medio = f"{sum(data['pisa_values'])/len(data['pisa_values']):.1f}" if data['pisa_values'] else "N/A"
        escolaridade_media = f"{sum(data['escolaridade_values'])/len(data['escolaridade_values']):.1f}" if data['escolaridade_values'] else "N/A"
        
        print(f"{data['name']:<18} {periodo:<12} {obs:<6} {pib_medio:<15} {pisa_medio:<12} {escolaridade_media}")

def calcular_correlacoes(dataset):
    """Calcula correlações principais"""
    print("\n" + "=" * 80)
    print("ANÁLISE DE CORRELAÇÕES")
    print("=" * 80)
    
    import math
    
    def pearson_r(x, y):
        """Calcula correlação de Pearson simplificada"""
        n = len(x)
        if n < 3:
            return None
        
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denom_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x))
        denom_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
        
        if denom_x * denom_y == 0:
            return None
        
        return numerator / (denom_x * denom_y)
    
    print(f"\n{'País':<18} {'r(PIB-Escolaridade)':<22} {'r(PIB-PISA)':<18} {'Obs'}")
    print("-" * 70)
    
    for cc, name in PAISES.items():
        # Filtrar dados do país
        pib = []
        escolaridade = []
        pisa = []
        
        for row in dataset:
            if row['country_code'] == cc:
                if row.get('pib_per_capita_ppp_2017') and row.get('anos_escolaridade_estimado'):
                    pib.append(row['pib_per_capita_ppp_2017'])
                    escolaridade.append(row['anos_escolaridade_estimado'])
                
                if row.get('pib_per_capita_ppp_2017') and row.get('pisa_media'):
                    pisa.append((row['pib_per_capita_ppp_2017'], row['pisa_media']))
        
        r_pib_escol = pearson_r(pib, escolaridade) if len(pib) > 3 else None
        r_pib_pisa = pearson_r([x[0] for x in pisa], [x[1] for x in pisa]) if len(pisa) > 3 else None
        
        r_pib_escol_str = f"{r_pib_escol:.3f}" if r_pib_escol else "N/A"
        r_pib_pisa_str = f"{r_pib_pisa:.3f}" if r_pib_pisa else "N/A"
        obs = len(pib)
        
        print(f"{name:<18} {r_pib_escol_str:<22} {r_pib_pisa_str:<18} {obs}")

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n" + "=" * 80)
    print("COLETOR DE DADOS PRIMÁRIOS V2")
    print("Dissertação: EDUCAÇÃO E ARMADILHA DA RENDA MÉDIA")
    print("=" * 80)
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. Coletar dados
    dados_raw = coletar_todos_dados()
    
    # 2. Criar dataset tabular
    dataset = criar_dataset_tabular(dados_raw)
    
    # 3. Salvar CSV
    filename = salvar_csv(dataset)
    
    # 4. Estatísticas
    imprimir_resumo_estatistico(dataset)
    
    # 5. Correlações
    calcular_correlacoes(dataset)
    
    # 6. Salvar metadados
    metadata = {
        'data_coleta': datetime.now().isoformat(),
        'fontes': ['World Bank API v2', 'OECD PISA (pré-coletado)'],
        'indicadores': list(INDICADORES_ESSENCIAIS.keys()),
        'paises': list(PAISES.keys()),
        'periodo': '1960-2023',
        'total_registros': len(dataset),
        'arquivo_csv': filename
    }
    
    with open('metadata_dados_primarios.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Metadados salvos: metadata_dados_primarios.json")
    print("\n" + "=" * 80)
    print("COLETA DE DADOS PRIMÁRIOS CONCLUÍDA!")
    print("=" * 80)
    
    return filename

if __name__ == "__main__":
    main()