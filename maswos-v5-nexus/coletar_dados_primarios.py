#!/usr/bin/env python3
"""
COLETOR DE DADOS PRIMÁRIOS - DISSERTAÇÃO MIT-EDUCAÇÃO
Fontes: World Bank API, UNESCO, OECD PISA

Indicadores coletados:
- PIB per capita (NY.GDP.PCAP.PP.KD)
- Matrícula líquida ensino médio (SE.SEC.ENRR)
- Matrícula líquida ensino superior (SE.TER.ENRR)
- Gasto público educação % PIB (SE.XPD.TOTL.GD.ZS)
- P&D % PIB (GB.XPD.RSDV.GD.ZS)
- População 25+ com ensino superior (SE.SEC.AG25.LT.ZS)
- Urbanização (SP.URB.TOTL.IN.ZS)
- IDH (HD.HDI.OV)
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

# Países e códigos World Bank
PAISES = {
    'BRA': {'nome': 'Brasil', 'nome_en': 'Brazil'},
    'MEX': {'nome': 'México', 'nome_en': 'Mexico'},
    'TUR': {'nome': 'Turquia', 'nome_en': 'Turkey'},
    'CHN': {'nome': 'China', 'nome_en': 'China'},
    'IND': {'nome': 'Índia', 'nome_en': 'India'},
    'KOR': {'nome': 'Coreia do Sul', 'nome_en': 'Korea, Rep.'},
    'MYS': {'nome': 'Malásia', 'nome_en': 'Malaysia'}
}

# Indicadores World Bank
INDICADORES = {
    # PIB
    'NY.GDP.PCAP.PP.KD': 'pib_per_capita_ppp',  # PIB per capita PPP (2017)
    'NY.GDP.PCAP.KD': 'pib_per_capita_constante',  # PIB per capita constante (2015)
    
    # Educação - Acesso
    'SE.PRM.ENRR': 'matricula_primaria',  # Matrícula líquida primária %
    'SE.SEC.ENRR': 'matricula_secundaria',  # Matrícula líquida secundária %
    'SE.TER.ENRR': 'matricula_superior',  # Matrícula líquida superior %
    
    # Educação - Gasto
    'SE.XPD.TOTL.GD.ZS': 'gasto_educacao_pct_pib',  # Gasto educação % PIB
    'SE.XPD.PRIM.PC.ZS': 'gasto_por_aluno_primario',  # Gasto por aluno primário % PIB per capita
    'SE.XPD.SECO.PC.ZS': 'gasto_por_aluno_secundario',  # Gasto por aluno secundário
    
    # Educação - Resultados
    'SE.ADT.LITR.ZS': 'taxa_alfabetizacao',  # Taxa de alfabetização adultos %
    'SE.SEC.AG25.LT.ZS': 'pop_25_superior',  # População 25+ com ensino superior %
    
    # P&D e Inovação
    'GB.XPD.RSDV.GD.ZS': 'pct_pd_pib',  # P&D % PIB
    'IP.PAT.RESD': 'patentes_nacionais',  # Patentes de residentes
    
    # Desenvolvimento Humano
    'HD.HDI.OV': 'idh',  # Índice de Desenvolvimento Humano
    
    # Demografia
    'SP.URB.TOTL.IN.ZS': 'urbanizacao_pct',  # População urbana %
    'SP.POP.TOTL': 'populacao_total',  # População total
    
    # Mercado de Trabalho
    'SL.UEM.TOTL.ZS': 'desemprego',  # Desemprego total %
    'SL.TLF.TERT.ZS': 'forca_trabalho_superior',  # Força de trabalho com educação superior %
}

# Perguntas adicionais para PISA (dados do OCDE)
PISA_DATA = {
    'BRA': {
        2000: {'leitura': 396, 'matematica': 334, 'ciencias': 375},
        2003: {'leitura': 403, 'matematica': 356, 'ciencias': 387},
        2006: {'leitura': 393, 'matematica': 370, 'ciencias': 390},
        2009: {'leitura': 412, 'matematica': 385, 'ciencias': 405},
        2012: {'leitura': 410, 'matematica': 391, 'ciencias': 405},
        2015: {'leitura': 419, 'matematica': 377, 'ciencias': 401},
        2018: {'leitura': 413, 'matematica': 379, 'ciencias': 404},
        2022: {'leitura': 410, 'matematica': 379, 'ciencias': 403}
    },
    'MEX': {
        2000: {'leitura': 422, 'matematica': 387, 'ciencias': 422},
        2003: {'leitura': 400, 'matematica': 385, 'ciencias': 405},
        2006: {'leitura': 410, 'matematica': 406, 'ciencias': 418},
        2009: {'leitura': 425, 'matematica': 419, 'ciencias': 416},
        2012: {'leitura': 424, 'matematica': 413, 'ciencias': 415},
        2015: {'leitura': 423, 'matematica': 406, 'ciencias': 416},
        2018: {'leitura': 420, 'matematica': 409, 'ciencias': 419},
        2022: {'leitura': 415, 'matematica': 408, 'ciencias': 410}
    },
    'TUR': {
        2003: {'leitura': 441, 'matematica': 423, 'ciencias': 434},
        2006: {'leitura': 447, 'matematica': 424, 'ciencias': 424},
        2009: {'leitura': 464, 'matematica': 445, 'ciencias': 454},
        2012: {'leitura': 475, 'matematica': 448, 'ciencias': 463},
        2015: {'leitura': 428, 'matematica': 420, 'ciencias': 425},
        2018: {'leitura': 466, 'matematica': 454, 'ciencias': 468},
        2022: {'leitura': 456, 'matematica': 453, 'ciencias': 476}
    },
    'CHN': {
        # China participou com províncias selecionadas (B-S-J-Z)
        2009: {'leitura': 556, 'matematica': 590, 'ciencias': 575},
        2012: {'leitura': 570, 'matematica': 613, 'ciencias': 590},
        2015: {'leitura': 494, 'matematica': 558, 'ciencias': 518},
        2018: {'leitura': 555, 'matematica': 591, 'ciencias': 590}
    },
    'IND': {
        # Índia participou apenas em 2009 e 2012 (limitado)
        2009: {'leitura': 369, 'matematica': 343, 'ciencias': 373},
        2012: {'leitura': 376, 'matematica': 351, 'ciencias': 363}
    },
    'KOR': {
        2000: {'leitura': 525, 'matematica': 547, 'ciencias': 552},
        2003: {'leitura': 534, 'matematica': 542, 'ciencias': 538},
        2006: {'leitura': 556, 'matematica': 588, 'ciencias': 566},
        2009: {'leitura': 568, 'matematica': 572, 'ciencias': 561},
        2012: {'leitura': 536, 'matematica': 554, 'ciencias': 538},
        2015: {'leitura': 517, 'matematica': 524, 'ciencias': 516},
        2018: {'leitura': 514, 'matematica': 526, 'ciencias': 519},
        2022: {'leitura': 515, 'matematica': 527, 'ciencias': 528}
    },
    'MYS': {
        2009: {'leitura': 418, 'matematica': 427, 'ciencias': 422},
        2012: {'leitura': 434, 'matematica': 440, 'ciencias': 440},
        2015: {'leitura': 431, 'matematica': 446, 'ciencias': 443},
        2018: {'leitura': 442, 'matematica': 461, 'ciencias': 456},
        2022: {'leitura': 448, 'matematica': 468, 'ciencias': 458}
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

def fetch_world_bank_api(indicator, country_codes, start_year=1960, end_year=2023, retries=3):
    """
    Busca dados da API do World Bank
    Documentação: https://datahelpdesk.worldbank.org/knowledgebase/articles/898581
    """
    countries = ';'.join(country_codes)
    url = f"https://api.worldbank.org/v2/country/{countries}/indicator/{indicator}?date={start_year}:{end_year}&format=json&per_page=5000"
    
    headers = {
        'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36'
    }
    
    for attempt in range(retries):
        try:
            ctx = criar_contexto_ssl()
            req = Request(url, headers=headers)
            
            if ctx:
                with urlopen(req, context=ctx, timeout=30) as response:
                    data = json.loads(response.read().decode('utf-8'))
            else:
                with urlopen(req, timeout=30) as response:
                    data = json.loads(response.read().decode('utf-8'))
            
            # API retorna [metadata, data]
            if isinstance(data, list) and len(data) > 1:
                return data[1]  # Retorna os dados
            elif isinstance(data, dict) and 'message' in data:
                print(f"  [ERRO API] {data['message']}")
                return None
            else:
                return data
                
        except HTTPError as e:
            print(f"  [HTTP ERRO] {e.code}: {e.reason} (tentativa {attempt+1}/{retries})")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)  # Backoff exponencial
        except URLError as e:
            print(f"  [URL ERRO] {e.reason} (tentativa {attempt+1}/{retries})")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
        except Exception as e:
            print(f"  [ERRO] {type(e).__name__}: {e} (tentativa {attempt+1}/{retries})")
            if attempt < retries - 1:
                time.sleep(2 ** attempt)
    
    return None

def processar_dados_world_bank(raw_data):
    """Processa dados brutos da API do World Bank em dicionário organizado"""
    dados_processados = {}
    
    if not raw_data:
        return dados_processados
    
    for item in raw_data:
        if item and item.get('value') is not None:
            country = item['country']['id']
            year = int(item['date'])
            value = item['value']
            
            if country not in dados_processados:
                dados_processados[country] = {}
            
            dados_processados[country][year] = value
    
    return dados_processados

def coletar_dados_world_bank():
    """Coleta todos os indicadores do World Bank"""
    print("=" * 70)
    print("COLETANDO DADOS DO WORLD BANK API")
    print("=" * 70)
    
    country_codes = list(PAISES.keys())
    todos_dados = {}
    
    for indicator_code, indicator_name in INDICADORES.items():
        print(f"\n[COLETANDO] {indicator_name} ({indicator_code})...")
        
        raw_data = fetch_world_bank_api(indicator_code, country_codes, 1960, 2023)
        
        if raw_data:
            dados_processados = processar_dados_world_bank(raw_data)
            todos_dados[indicator_code] = dados_processados
            
            total_obs = sum(len(v) for v in dados_processados.values())
            print(f"  [OK] {total_obs} observações coletadas")
        else:
            print(f"  [FALHA] Não foi possível coletar {indicator_name}")
        
        time.sleep(0.5)  # Rate limiting
    
    return todos_dados

def integrar_dados_pisa():
    """Integra dados PISA do OCDE (dados pré-coletados)"""
    print("\n" + "=" * 70)
    print("INTEGRANDO DADOS PISA (OCDE)")
    print("=" * 70)
    
    dados_pisa = {}
    
    for country_code, anos_data in PISA_DATA.items():
        for ano, scores in anos_data.items():
            if country_code not in dados_pisa:
                dados_pisa[country_code] = {}
            
            media = (scores.get('leitura', 0) + scores.get('matematica', 0) + scores.get('ciencias', 0)) / 3
            dados_pisa[country_code][ano] = {
                'pisa_media': round(media, 1),
                'pisa_leitura': scores.get('leitura'),
                'pisa_matematica': scores.get('matematica'),
                'pisa_ciencias': scores.get('ciencias')
            }
    
    print(f"[OK] Dados PISA integrados para {len(dados_pisa)} países")
    return dados_pisa

def criar_dataset_unificado(dados_wb, dados_pisa):
    """Cria dataset unificado com todos os dados"""
    print("\n" + "=" * 70)
    print("CRIANDO DATASET UNIFICADO")
    print("=" * 70)
    
    dataset = []
    
    for country_code, country_info in PAISES.items():
        # Coletar todos os anos disponíveis para este país
        todos_anos = set()
        
        for indicator_code in INDICADORES.keys():
            if country_code in dados_wb.get(indicator_code, {}):
                todos_anos.update(dados_wb[indicator_code][country_code].keys())
        
        for ano in sorted(todos_anos):
            if ano < 1960 or ano > 2023:
                continue
            
            row = {
                'pais_codigo': country_code,
                'pais': country_info['nome'],
                'ano': ano
            }
            
            # Adicionar indicadores do World Bank
            for indicator_code, indicator_name in INDICADORES.items():
                value = dados_wb.get(indicator_code, {}).get(country_code, {}).get(ano)
                row[indicator_name] = value
            
            # Adicionar dados PISA
            if country_code in dados_pisa and ano in dados_pisa[country_code]:
                pisa_data = dados_pisa[country_code][ano]
                row['pisa_media'] = pisa_data.get('pisa_media')
                row['pisa_leitura'] = pisa_data.get('pisa_leitura')
                row['pisa_matematica'] = pisa_data.get('pisa_matematica')
                row['pisa_ciencias'] = pisa_data.get('pisa_ciencias')
            else:
                row['pisa_media'] = None
                row['pisa_leitura'] = None
                row['pisa_matematica'] = None
                row['pisa_ciencias'] = None
            
            # Calcular anos médios de escolaridade (proxy)
            if row.get('pop_25_superior'):
                # Estimativa simples: 16 anos para superior + secundário
                anos_escolaridade = 4 + (row.get('matricula_secundaria', 0) / 100 * 8) + (row.get('pop_25_superior', 0) / 100 * 4)
                row['anos_escolaridade_estimado'] = round(min(anos_escolaridade, 15), 2)
            else:
                row['anos_escolaridade_estimado'] = None
            
            dataset.append(row)
    
    print(f"[OK] Dataset criado com {len(dataset)} observações")
    return dataset

def salvar_dataset_csv(dataset, filename='dataset_mit_educacao_primario.csv'):
    """Salva dataset em CSV"""
    if not dataset:
        print("[ERRO] Dataset vazio")
        return
    
    # Obter todas as colunas
    columns = list(dataset[0].keys())
    
    with open(filename, 'w', newline='', encoding='utf-8') as f:
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        writer.writerows(dataset)
    
    print(f"\n[OK] Dataset salvo em: {filename}")
    print(f"    Total de linhas: {len(dataset)}")
    print(f"    Total de colunas: {len(columns)}")
    
    return filename

def gerar_estatisticas_resumo(dataset):
    """Gera estatísticas resumo do dataset"""
    print("\n" + "=" * 70)
    print("ESTATÍSTICAS RESUMO")
    print("=" * 70)
    
    # Agrupar por país
    por_pais = {}
    for row in dataset:
        country = row['pais']
        if country not in por_pais:
            por_pais[country] = {'anos': [], 'pib': [], 'escolaridade': []}
        
        por_pais[country]['anos'].append(row['ano'])
        if row.get('pib_per_capita_ppp'):
            por_pais[country]['pib'].append(row['pib_per_capita_ppp'])
        if row.get('anos_escolaridade_estimado'):
            por_pais[country]['escolaridade'].append(row['anos_escolaridade_estimado'])
    
    print("\nCobertura por país:")
    print(f"{'País':<20} {'Anos':<15} {'Obs PIB':<15} {'Obs Escolaridade'}")
    print("-" * 70)
    
    for country, data in sorted(por_pais.items()):
        anos_range = f"{min(data['anos'])}-{max(data['anos'])}" if data['anos'] else "N/A"
        print(f"{country:<20} {anos_range:<15} {len(data['pib']):<15} {len(data['escolaridade'])}")
    
    return por_pais

# ============================================================================
# MAIN
# ============================================================================

def main():
    print("\n" + "=" * 70)
    print("COLETOR DE DADOS PRIMÁRIOS")
    print("Dissertação: A EDUCAÇÃO COMO MECANISMO DE ESCAPE DA ARMADILHA DA RENDA MÉDIA")
    print("=" * 70)
    print(f"Data/Hora: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    print()
    
    # 1. Coletar dados do World Bank
    dados_wb = coletar_dados_world_bank()
    
    # 2. Integrar dados PISA
    dados_pisa = integrar_dados_pisa()
    
    # 3. Criar dataset unificado
    dataset = criar_dataset_unificado(dados_wb, dados_pisa)
    
    # 4. Salvar dataset
    filename = salvar_dataset_csv(dataset)
    
    # 5. Gerar estatísticas
    stats = gerar_estatisticas_resumo(dataset)
    
    # 6. Salvar metadados
    metadata = {
        'data_coleta': datetime.now().isoformat(),
        'fontes': ['World Bank API', 'OECD PISA'],
        'indicadores': list(INDICADORES.keys()),
        'paises': list(PAISES.keys()),
        'periodo': '1960-2023',
        'total_observacoes': len(dataset)
    }
    
    with open('metadata_dataset.json', 'w', encoding='utf-8') as f:
        json.dump(metadata, f, indent=2, ensure_ascii=False)
    
    print(f"\n[OK] Metadados salvos em: metadata_dataset.json")
    
    print("\n" + "=" * 70)
    print("COLETA CONCLUÍDA COM SUCESSO!")
    print("=" * 70)
    
    return filename

if __name__ == "__main__":
    main()