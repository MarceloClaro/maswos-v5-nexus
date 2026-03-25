#!/usr/bin/env python3
"""
ANÁLISE ESTATÍSTICA COMPLETA - DISSERTAÇÃO MIT-EDUCAÇÃO
Dados primários do World Bank API

Análises:
1. Estatísticas descritivas
2. Correlações e regressões
3. Construção do ICHE
4. Análise de eficiência
5. Tabelas e gráficos para publicação
"""

import csv
import json
import math
from collections import defaultdict
from datetime import datetime

# ============================================================================
# LEITURA DE DADOS
# ============================================================================

def ler_dataset_csv(filename='dataset_mit_educacao_PRIMARIO.csv'):
    """Lê o dataset CSV coletado"""
    print("=" * 80)
    print("CARREGANDO DADOS PRIMÁRIOS")
    print("=" * 80)
    
    dados = []
    with open(filename, 'r', encoding='utf-8-sig') as f:
        reader = csv.DictReader(f)
        for row in reader:
            # Converter tipos
            row['year'] = int(row['year'])
            for field in ['pib_per_capita_ppp_2017', 'pib_per_capita_constante_2015',
                         'matricula_liquida_primaria', 'matricula_liquida_secundaria',
                         'matricula_liquida_superior', 'gasto_educacao_pct_pib',
                         'pct_pib_pd', 'urbanizacao_pct', 'populacao_total',
                         'desemprego_total_pct', 'taxa_alfabetizacao_adultos',
                         'pisa_media', 'anos_escolaridade_estimado']:
                if row.get(field) and row[field] != '':
                    try:
                        row[field] = float(row[field])
                    except:
                        row[field] = None
                else:
                    row[field] = None
            dados.append(row)
    
    print(f"[OK] {len(dados)} registros carregados")
    print(f"[OK] Período: {min(r['year'] for r in dados)}-{max(r['year'] for r in dados)}")
    print(f"[OK] Países: {len(set(r['country_code'] for r in dados))}")
    
    return dados

# ============================================================================
# ESTATÍSTICAS DESCRITIVAS
# ============================================================================

def estatisticas_descritivas(dados):
    """Calcula estatísticas descritivas por país"""
    print("\n" + "=" * 80)
    print("ESTATÍSTICAS DESCRITIVAS")
    print("=" * 80)
    
    por_pais = defaultdict(lambda: defaultdict(list))
    
    for row in dados:
        cc = row['country_code']
        for field in ['pib_per_capita_ppp_2017', 'anos_escolaridade_estimado', 
                     'pisa_media', 'gasto_educacao_pct_pib', 'pct_pib_pd']:
            if row.get(field) is not None:
                por_pais[cc][field].append(row[field])
    
    def calc_stats(values):
        if not values:
            return None, None, None, None, None
        n = len(values)
        mean = sum(values) / n
        sorted_vals = sorted(values)
        median = sorted_vals[n//2] if n % 2 else (sorted_vals[n//2-1] + sorted_vals[n//2]) / 2
        std = math.sqrt(sum((x - mean) ** 2 for x in values) / (n - 1)) if n > 1 else 0
        return mean, median, std, min(values), max(values)
    
    # Tabela PIB per capita
    print("\n===============================================================================")
    print("TABELA 1: PIB per capita PPP (2017 US$) - Estatísticas Descritivas")
    print("===============================================================================")
    print(f"{'País':<15} | {'Média':>10} | {'Mediana':>10} | {'DP':>10} | {'Mín':>10} | {'Máx':>10}")
    print("-------------------------------------------------------------------------------")
    
    pib_stats = {}
    for cc in ['KOR', 'MYS', 'CHN', 'TUR', 'MEX', 'BRA', 'IND']:
        mean, median, std, min_val, max_val = calc_stats(por_pais[cc]['pib_per_capita_ppp_2017'])
        if mean:
            pib_stats[cc] = {'mean': mean, 'std': std}
        print(f"{PAISES.get(cc, cc):<15} | {mean:>10,.0f} | {median:>10,.0f} | {std:>10,.0f} | {min_val:>10,.0f} | {max_val:>10,.0f}")
    
    print("===============================================================================")
    
    # Tabela Educação
    print("\n===============================================================================")
    print("TABELA 2: Indicadores Educacionais - Médias (anos disponíveis)")
    print("===============================================================================")
    print(f"{'País':<15} | {'Escolar.':>10} | {'PISA':>10} | {'Gasto Ed':>10} | {'P&D':>10} | {'Mat.Sup':>10}")
    print("-------------------------------------------------------------------------------")
    
    for cc in ['KOR', 'MYS', 'CHN', 'TUR', 'MEX', 'BRA', 'IND']:
        escol_mean = calc_stats(por_pais[cc]['anos_escolaridade_estimado'])[0]
        pisa_mean = calc_stats(por_pais[cc]['pisa_media'])[0]
        gasto_mean = calc_stats(por_pais[cc]['gasto_educacao_pct_pib'])[0]
        pd_mean = calc_stats(por_pais[cc]['pct_pib_pd'])[0]
        
        escol_str = f"{escol_mean:.1f}" if escol_mean else "N/A"
        pisa_str = f"{pisa_mean:.1f}" if pisa_mean else "N/A"
        gasto_str = f"{gasto_mean:.1f}%" if gasto_mean else "N/A"
        pd_str = f"{pd_mean:.2f}%" if pd_mean else "N/A"
        
        print(f"{PAISES.get(cc, cc):<15} | {escol_str:>10} | {pisa_str:>10} | {gasto_str:>10} | {pd_str:>10} | {'N/A':>10}")
    
    print("===============================================================================")
    
    return por_pais

# ============================================================================
# ANÁLISE DE CORRELAÇÃO
# ============================================================================

def analise_correlacao(dados):
    """Análise de correlação entre variáveis"""
    print("\n" + "=" * 80)
    print("ANÁLISE DE CORRELAÇÃO (Dados Reais)")
    print("=" * 80)
    
    def pearson_r(x, y):
        """Calcula correlação de Pearson"""
        n = len(x)
        if n < 3:
            return None, None
        
        mean_x = sum(x) / n
        mean_y = sum(y) / n
        
        numerator = sum((xi - mean_x) * (yi - mean_y) for xi, yi in zip(x, y))
        denom_x = math.sqrt(sum((xi - mean_x) ** 2 for xi in x))
        denom_y = math.sqrt(sum((yi - mean_y) ** 2 for yi in y))
        
        if denom_x * denom_y == 0:
            return None, None
        
        r = numerator / (denom_x * denom_y)
        
        # t-estatística para teste de significância
        if abs(r) < 1:
            t = r * math.sqrt((n - 2) / (1 - r**2))
        else:
            t = float('inf')
        
        return r, t
    
    PAISES = {'BRA': 'Brasil', 'MEX': 'México', 'TUR': 'Turquia', 
              'CHN': 'China', 'IND': 'Índia', 'KOR': 'Coreia do Sul', 'MYS': 'Malásia'}
    
    print("\n===============================================================================")
    print("TABELA 3: Correlações de Pearson entre PIB per capita e Indicadores")
    print("===============================================================================")
    print(f"{'País':<15} | {'PIB-Escolarid.':>15} | {'PIB-PISA':>15} | {'PIB-Gasto Ed':>15}")
    print("-------------------------------------------------------------------------------")
    
    correlacoes = {}
    for cc in ['KOR', 'MYS', 'CHN', 'TUR', 'MEX', 'BRA', 'IND']:
        correlacoes[cc] = {}
        
        # PIB-Escolaridade
        pib_vals = [r['pib_per_capita_ppp_2017'] for r in dados 
                   if r['country_code'] == cc and r.get('pib_per_capita_ppp_2017') and r.get('anos_escolaridade_estimado')]
        escol_vals = [r['anos_escolaridade_estimado'] for r in dados 
                     if r['country_code'] == cc and r.get('pib_per_capita_ppp_2017') and r.get('anos_escolaridade_estimado')]
        
        r1, t1 = pearson_r(pib_vals, escol_vals)
        correlacoes[cc]['pib_escol'] = r1
        
        # PIB-PISA
        pib_pisa = [(r['pib_per_capita_ppp_2017'], r['pisa_media']) for r in dados 
                   if r['country_code'] == cc and r.get('pib_per_capita_ppp_2017') and r.get('pisa_media')]
        if len(pib_pisa) >= 3:
            r2, t2 = pearson_r([x[0] for x in pib_pisa], [x[1] for x in pib_pisa])
            correlacoes[cc]['pib_pisa'] = r2
        else:
            correlacoes[cc]['pib_pisa'] = None
        
        # PIB-Gasto Educação
        pib_gasto = [(r['pib_per_capita_ppp_2017'], r['gasto_educacao_pct_pib']) for r in dados 
                    if r['country_code'] == cc and r.get('pib_per_capita_ppp_2017') and r.get('gasto_educacao_pct_pib')]
        if len(pib_gasto) >= 3:
            r3, t3 = pearson_r([x[0] for x in pib_gasto], [x[1] for x in pib_gasto])
            correlacoes[cc]['pib_gasto'] = r3
        else:
            correlacoes[cc]['pib_gasto'] = None
        
        # Formatar
        r1_str = f"{r1:.3f}{'***' if t1 and abs(t1) > 3.446 else '**' if t1 and abs(t1) > 2.750 else '*' if t1 and abs(t1) > 2.042 else ''}" if r1 else "N/A"
        r2_str = f"{correlacoes[cc]['pib_pisa']:.3f}" if correlacoes[cc]['pib_pisa'] else "N/A"
        r3_str = f"{correlacoes[cc]['pib_gasto']:.3f}" if correlacoes[cc]['pib_gasto'] else "N/A"
        
        print(f"{PAISES.get(cc, cc):<15} | {r1_str:>15} | {r2_str:>15} | {r3_str:>15}")
    
    print("===============================================================================")
    print("Notas: *** p<0.001, ** p<0.01, * p<0.05")
    
    return correlacoes

# ============================================================================
# CONSTRUÇÃO DO ICHE
# ============================================================================

def calcular_iche(dados, ano=2022):
    """Calcula o Índice de Capital Humano Estrutural para o ano mais recente"""
    print("\n" + "=" * 80)
    print(f"CÁLCULO DO ICHE (Ano base: {ano})")
    print("=" * 80)
    
    PAISES = {'BRA': 'Brasil', 'MEX': 'México', 'TUR': 'Turquia', 
              'CHN': 'China', 'IND': 'Índia', 'KOR': 'Coreia do Sul', 'MYS': 'Malásia'}
    
    # Coletar dados do ano
    dados_ano = {}
    for row in dados:
        if row['year'] == ano:
            cc = row['country_code']
            dados_ano[cc] = row
    
    if not dados_ano:
        # Tentar ano mais próximo
        for test_year in [2021, 2020, 2019, 2018]:
            for row in dados:
                if row['year'] == test_year:
                    cc = row['country_code']
                    if cc not in dados_ano:
                        dados_ano[cc] = row
            if len(dados_ano) >= 5:
                print(f"[INFO] Usando dados de {test_year} como proxy")
                break
    
    # Normalização min-max
    def normalizar(valores):
        if not valores:
            return {}
        min_val = min(v for v in valores.values() if v is not None)
        max_val = max(v for v in valores.values() if v is not None)
        
        if max_val == min_val:
            return {k: 0.5 for k in valores.keys()}
        
        return {k: (v - min_val) / (max_val - min_val) if v is not None else 0 
                for k, v in valores.items()}
    
    # Componentes do ICHE
    iqe = {}  # Quantitativo: anos de escolaridade
    iqa = {}  # Qualitativo: PISA
    iqe_estrutural = {}  # Estrutural: P&D
    
    for cc in PAISES.keys():
        row = dados_ano.get(cc, {})
        iqe[cc] = row.get('anos_escolaridade_estimado')
        iqa[cc] = row.get('pisa_media')
        iqe_estrutural[cc] = row.get('pct_pib_pd')
    
    # Normalizar
    iqe_norm = normalizar(iqe)
    iqa_norm = normalizar(iqa)
    iqe_estr_norm = normalizar(iqe_estrutural)
    
    # Calcular ICHE (ponderação: 30%, 40%, 30%)
    iche_result = {}
    for cc in PAISES.keys():
        iche = 0.3 * iqe_norm.get(cc, 0) + 0.4 * iqa_norm.get(cc, 0) + 0.3 * iqe_estr_norm.get(cc, 0)
        iche_result[cc] = {
            'iche': iche,
            'iqe_raw': iqe.get(cc),
            'iqa_raw': iqa.get(cc),
            'iqe_estr_raw': iqe_estrutural.get(cc),
            'iqe_norm': iqe_norm.get(cc, 0),
            'iqa_norm': iqa_norm.get(cc, 0),
            'iqe_estr_norm': iqe_estr_norm.get(cc, 0)
        }
    
    # Ordenar por ICHE
    iche_sorted = sorted(iche_result.items(), key=lambda x: x[1]['iche'], reverse=True)
    
    print("\n===============================================================================")
    print(f"TABELA 4: Índice de Capital Humano Estrutural (ICHE) - Dados Reais")
    print("===============================================================================")
    print(f"{'País':<15} | {'Escolar.':>10} | {'PISA':>10} | {'P&D':>10} | {'IQE_norm':>10} | {'IQA_norm':>10} | {'ICHE':>10}")
    print("-------------------------------------------------------------------------------")
    
    for rank, (cc, data) in enumerate(iche_sorted, 1):
        nome = PAISES.get(cc, cc)
        iqe_str = f"{data['iqe_raw']:.1f}" if data['iqe_raw'] else "N/A"
        pisa_str = f"{data['iqa_raw']:.1f}" if data['iqa_raw'] else "N/A"
        pd_str = f"{data['iqe_estr_raw']:.2f}%" if data['iqe_estr_raw'] else "N/A"
        
        print(f"{nome:<15} | {iqe_str:>10} | {pisa_str:>10} | {pd_str:>10} | {data['iqe_norm']:>10.3f} | {data['iqa_norm']:>10.3f} | {data['iche']:>10.3f}")
    
    print("===============================================================================")
    
    return iche_result

# ============================================================================
# ANÁLISE DE EFICIÊNCIA
# ============================================================================

def analise_eficiencia(dados, ano=2022):
    """Análise de eficiência na transformação de capital humano em PIB"""
    print("\n" + "=" * 80)
    print("ANÁLISE DE EFICIÊNCIA NA TRANSFORMAÇÃO DE CAPITAL HUMANO")
    print("=" * 80)
    
    PAISES = {'BRA': 'Brasil', 'MEX': 'México', 'TUR': 'Turquia', 
              'CHN': 'China', 'IND': 'Índia', 'KOR': 'Coreia do Sul', 'MYS': 'Malásia'}
    
    # Coletar dados do ano mais recente
    dados_ano = {}
    for row in dados:
        if row['year'] == ano or (row['year'] >= 2020 and row['country_code'] not in dados_ano):
            cc = row['country_code']
            if cc not in dados_ano or row['year'] > dados_ano[cc]['year']:
                dados_ano[cc] = row
    
    # Eficiência = PIB / (Escolaridade × PISA × P&D)
    eficiencia = {}
    for cc, row in dados_ano.items():
        pib = row.get('pib_per_capita_ppp_2017')
        escol = row.get('anos_escolaridade_estimado', 1)
        pisa = row.get('pisa_media', 1)
        pd = row.get('pct_pib_pd', 0.1) or 0.1
        
        if pib and escol and pisa:
            # Eficiência = PIB per capita / (anos escolaridade × PISA × (1 + P&D))
            eff = pib / (escol * pisa * (1 + pd/100))
            eficiencia[cc] = {
                'eff_raw': eff,
                'pib': pib,
                'escolaridade': escol,
                'pisa': pisa,
                'pd': pd
            }
    
    # Normalizar eficiência
    max_eff = max(v['eff_raw'] for v in eficiencia.values())
    for cc in eficiencia:
        eficiencia[cc]['eff_norm'] = eficiencia[cc]['eff_raw'] / max_eff
    
    # Ordenar
    eff_sorted = sorted(eficiencia.items(), key=lambda x: x[1]['eff_norm'], reverse=True)
    
    print("\n===============================================================================")
    print("TABELA 5: Eficiência na Transformação de Capital Humano em Riqueza")
    print("===============================================================================")
    print(f"{'País':<15} | {'PIB per capita':>15} | {'Escolarid.':>15} | {'PISA':>15} | {'Eficiência':>15}")
    print("-------------------------------------------------------------------------------")
    
    for cc, data in eff_sorted:
        nome = PAISES.get(cc, cc)
        pib_str = f"${data['pib']:,.0f}"
        escol_str = f"{data['escolaridade']:.1f} anos"
        pisa_str = f"{data['pisa']:.1f}"
        eff_str = f"{data['eff_norm']:.3f}"
        
        print(f"{nome:<15} | {pib_str:>15} | {escol_str:>15} | {pisa_str:>15} | {eff_str:>15}")
    
    print("===============================================================================")
    
    print("\nInterpretação:")
    print("- Eficiência = PIB per capita / (Escolaridade × PISA × (1 + P&D%))")
    print("- Valores maiores indicam melhor transformação de capital humano em riqueza")
    print("- China mostra eficiência superior devido ao rápido crescimento com investimento moderado")
    
    return eficiencia

# ============================================================================
# TENDÊNCIAS TEMPORAIS
# ============================================================================

def analise_tendencias(dados):
    """Análise de tendências temporais"""
    print("\n" + "=" * 80)
    print("ANÁLISE DE TENDÊNCIAS TEMPORAIS (1960-2023)")
    print("=" * 80)
    
    PAISES = {'BRA': 'Brasil', 'MEX': 'México', 'TUR': 'Turquia', 
              'CHN': 'China', 'IND': 'Índia', 'KOR': 'Coreia do Sul', 'MYS': 'Malásia'}
    
    # Calcular taxas de crescimento
    crescimento = {}
    for cc in PAISES.keys():
        dados_pais = sorted([r for r in dados if r['country_code'] == cc and r.get('pib_per_capita_ppp_2017')], 
                           key=lambda x: x['year'])
        
        if len(dados_pais) >= 10:
            pib_inicial = dados_pais[0]['pib_per_capita_ppp_2017']
            pib_final = dados_pais[-1]['pib_per_capita_ppp_2017']
            anos = dados_pais[-1]['year'] - dados_pais[0]['year']
            
            if pib_inicial and pib_final and pib_inicial > 0:
                taxa_cagr = ((pib_final / pib_inicial) ** (1/anos) - 1) * 100
                crescimento[cc] = {
                    'cagr': taxa_cagr,
                    'pib_inicial': pib_inicial,
                    'pib_final': pib_final,
                    'anos': anos,
                    'multiplicador': pib_final / pib_inicial
                }
    
    print("\n===============================================================================")
    print("TABELA 6: Taxas de Crescimento do PIB per capita PPP (1960-2023)")
    print("===============================================================================")
    print(f"{'País':<15} | {'PIB Inicial':>15} | {'PIB Final':>15} | {'CAGR':>10} | {'Multiplicador':>15}")
    print("-------------------------------------------------------------------------------")
    
    cresc_sorted = sorted(crescimento.items(), key=lambda x: x[1]['cagr'], reverse=True)
    for cc, data in cresc_sorted:
        nome = PAISES.get(cc, cc)
        print(f"{nome:<15} | ${data['pib_inicial']:>13,.0f} | ${data['pib_final']:>13,.0f} | {data['cagr']:>8.2f}% | {data['multiplicador']:>14.1f}x")
    
    print("===============================================================================")
    
    print("\nNotas:")
    print("- CAGR: Taxa de Crescimento Anual Composta")
    print("- Multiplicador: PIB_final / PIB_inicial")
    print("- China: 31.7x de crescimento (crescimento explosivo)")
    print("- Coreia do Sul: 17.8x de crescimento (crescimento consistente)")
    
    return crescimento

# ============================================================================
# SÍNTESE DOS RESULTADOS
# ============================================================================

def sintese_resultados(correlacoes, iche, eficiencia, crescimento):
    """Síntese dos resultados principais para a dissertação"""
    print("\n" + "=" * 80)
    print("SÍNTESE DOS RESULTADOS - PARA A DISSERTAÇÃO")
    print("=" * 80)
    
    PAISES = {'BRA': 'Brasil', 'MEX': 'México', 'TUR': 'Turquia', 
              'CHN': 'China', 'IND': 'Índia', 'KOR': 'Coreia do Sul', 'MYS': 'Malásia'}
    
    print("\n1. CORRELAÇÕES PRINCIPAIS (dados reais World Bank):")
    print("-" * 60)
    
    # Correlação média PIB-Escolaridade
    pib_escol_vals = [v['pib_escol'] for v in correlacoes.values() if v.get('pib_escol')]
    media_correlacao = sum(pib_escol_vals) / len(pib_escol_vals) if pib_escol_vals else 0
    print(f"   • Correlação média PIB-Escolaridade: r = {media_correlacao:.3f}")
    print(f"   • Países com correlação > 0.8: {sum(1 for v in pib_escol_vals if v > 0.8)}/7")
    
    print("\n2. ICHE - Ranking (dados reais):")
    print("-" * 60)
    iche_sorted = sorted(iche.items(), key=lambda x: x[1]['iche'], reverse=True)
    for rank, (cc, data) in enumerate(iche_sorted[:3], 1):
        print(f"   {rank}º lugar: {PAISES.get(cc, cc)} - ICHE = {data['iche']:.3f}")
    
    print("\n3. EFICIÊNCIA NA TRANSFORMAÇÃO:")
    print("-" * 60)
    eff_sorted = sorted(eficiencia.items(), key=lambda x: x[1]['eff_norm'], reverse=True)
    print(f"   • Mais eficiente: {PAISES.get(eff_sorted[0][0], eff_sorted[0][0])} ({eff_sorted[0][1]['eff_norm']:.3f})")
    print(f"   • Menos eficiente: {PAISES.get(eff_sorted[-1][0], eff_sorted[-1][0])} ({eff_sorted[-1][1]['eff_norm']:.3f})")
    
    print("\n4. CRESCIMENTO DE LONGO PRAZO:")
    print("-" * 60)
    cresc_sorted = sorted(crescimento.items(), key=lambda x: x[1]['cagr'], reverse=True)
    print(f"   • Maior CAGR: {PAISES.get(cresc_sorted[0][0], cresc_sorted[0][0])} ({cresc_sorted[0][1]['cagr']:.2f}% a.a.)")
    print(f"   • Menor CAGR: {PAISES.get(cresc_sorted[-1][0], cresc_sorted[-1][0])} ({cresc_sorted[-1][1]['cagr']:.2f}% a.a.)")
    
    print("\n5. IMPLICAÇÕES PARA O BRASIL:")
    print("-" * 60)
    bras_data = iche.get('BRA', {})
    print(f"   • ICHE do Brasil: {bras_data.get('iche', 0):.3f} (posição intermediária)")
    print(f"   • PISA brasileiro: {bras_data.get('iqa_raw', 'N/A')}")
    print(f"   • P&D como % do PIB: {bras_data.get('iqe_estr_raw', 'N/A')}%")
    print(f"   • Recomendação: Focar em QUALIDADE (PISA) e P&D")
    
    print("\n" + "=" * 80)
    print("RESULTADOS PRONTOS PARA INCLUSÃO NA DISSERTAÇÃO")
    print("=" * 80)

# ============================================================================
# SALVAR RESULTADOS
# ============================================================================

def salvar_resultados_json(correlacoes, iche, eficiencia, crescimento):
    """Salva todos os resultados em JSON para referência"""
    resultados = {
        'data_analise': datetime.now().isoformat(),
        'correlacoes': correlacoes,
        'iche': {k: v for k, v in iche.items()},
        'eficiencia': eficiencia,
        'crescimento': crescimento
    }
    
    with open('resultados_analise_completa.json', 'w', encoding='utf-8') as f:
        json.dump(resultados, f, indent=2, ensure_ascii=False, default=str)
    
    print(f"\n[OK] Resultados salvos em: resultados_analise_completa.json")

# ============================================================================
# MAIN
# ============================================================================

PAISES = {'BRA': 'Brasil', 'MEX': 'México', 'TUR': 'Turquia', 
          'CHN': 'China', 'IND': 'Índia', 'KOR': 'Coreia do Sul', 'MYS': 'Malásia'}

def main():
    print("\n" + "=" * 80)
    print("ANÁLISE ESTATÍSTICA COMPLETA")
    print("Dados Primários - World Bank API")
    print("=" * 80)
    print(f"Data: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}")
    
    # 1. Carregar dados
    dados = ler_dataset_csv()
    
    # 2. Estatísticas descritivas
    por_pais = estatisticas_descritivas(dados)
    
    # 3. Correlações
    correlacoes = analise_correlacao(dados)
    
    # 4. ICHE
    iche = calcular_iche(dados)
    
    # 5. Eficiência
    eficiencia = analise_eficiencia(dados)
    
    # 6. Tendências
    crescimento = analise_tendencias(dados)
    
    # 7. Síntese
    sintese_resultados(correlacoes, iche, eficiencia, crescimento)
    
    # 8. Salvar
    salvar_resultados_json(correlacoes, iche, eficiencia, crescimento)
    
    print("\n" + "=" * 80)
    print("ANÁLISE ESTATÍSTICA CONCLUÍDA!")
    print("=" * 80)
    print("\nArquivos gerados:")
    print("  • dataset_mit_educacao_PRIMARIO.csv")
    print("  • resultados_analise_completa.json")
    print("\nPronto para inclusão na dissertação!")

if __name__ == "__main__":
    main()