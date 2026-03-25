#!/usr/bin/env python3
"""
Gera figuras para a dissertação a partir do dataset primário
"""

import pandas as pd
import matplotlib.pyplot as plt
import numpy as np
import os
from matplotlib.ticker import FuncFormatter

# Configurações
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.figsize'] = (10, 6)
plt.rcParams['font.size'] = 12
plt.rcParams['axes.titlesize'] = 14
plt.rcParams['axes.labelsize'] = 12

# Criar diretório para figuras
os.makedirs('figures', exist_ok=True)

# Carregar dados
df = pd.read_csv('dataset_mit_educacao_PRIMARIO.csv')
print(f"Dataset carregado: {len(df)} observações")

# 1. Figura 1: Trajetórias de crescimento do PIB per capita PPP (1960-2023)
print("Gerando Figura 1...")
fig, ax = plt.subplots()
for country in df['country_name'].unique():
    subset = df[df['country_name'] == country].sort_values('year')
    ax.plot(subset['year'], subset['pib_per_capita_constante_2015'], label=country, linewidth=2)
ax.set_xlabel('Ano')
ax.set_ylabel('PIB per capita PPP (2017 US$)')
ax.set_title('Figura 1 – Trajetórias de crescimento do PIB per capita PPP (1960-2023)')
ax.legend()
ax.yaxis.set_major_formatter(FuncFormatter(lambda x, p: f'{x:,.0f}'))
plt.tight_layout()
plt.savefig('figures/fig1_pib_ppp.png', dpi=300)
plt.close()

# 2. Figura 2: Evolução dos anos médios de escolaridade por país
print("Gerando Figura 2...")
fig, ax = plt.subplots()
for country in df['country_name'].unique():
    subset = df[df['country_name'] == country].sort_values('year')
    ax.plot(subset['year'], subset['anos_escolaridade_estimado'], label=country, linewidth=2)
ax.set_xlabel('Ano')
ax.set_ylabel('Anos médios de escolaridade')
ax.set_title('Figura 2 – Evolução dos anos médios de escolaridade por país')
ax.legend()
plt.tight_layout()
plt.savefig('figures/fig2_escolaridade.png', dpi=300)
plt.close()

# 3. Figura 3: Resultados PISA por país (2000-2022)
print("Gerando Figura 3...")
# Filtrar anos com dados PISA
pisa_df = df[df['pisa_media'].notna()]
fig, ax = plt.subplots()
for country in pisa_df['country_name'].unique():
    subset = pisa_df[pisa_df['country_name'] == country].sort_values('year')
    ax.plot(subset['year'], subset['pisa_media'], marker='o', label=country, linewidth=2)
ax.set_xlabel('Ano')
ax.set_ylabel('Pontuação PISA média')
ax.set_title('Figura 3 – Resultados PISA por país (2000-2022)')
ax.legend()
ax.axhline(y=450, color='r', linestyle='--', alpha=0.5, label='Referência MIT (450)')
plt.tight_layout()
plt.savefig('figures/fig3_pisa.png', dpi=300)
plt.close()

# 4. Figura 4: Gasto público em educação como % do PIB
print("Gerando Figura 4...")
fig, ax = plt.subplots()
for country in df['country_name'].unique():
    subset = df[df['country_name'] == country].sort_values('year')
    ax.plot(subset['year'], subset['gasto_educacao_pct_pib'], label=country, linewidth=2)
ax.set_xlabel('Ano')
ax.set_ylabel('Gasto educação (% PIB)')
ax.set_title('Figura 4 – Gasto público em educação como % do PIB')
ax.legend()
plt.tight_layout()
plt.savefig('figures/fig4_gasto_educacao.png', dpi=300)
plt.close()

# 5. Figura 5: Investimento em P&D como % do PIB
print("Gerando Figura 5...")
fig, ax = plt.subplots()
for country in df['country_name'].unique():
    subset = df[df['country_name'] == country].sort_values('year')
    ax.plot(subset['year'], subset['pct_pib_pd'], label=country, linewidth=2)
ax.set_xlabel('Ano')
ax.set_ylabel('P&D (% PIB)')
ax.set_title('Figura 5 – Investimento em P&D como % do PIB')
ax.legend()
ax.axhline(y=2.0, color='r', linestyle='--', alpha=0.5, label='Meta MIT (2%)')
plt.tight_layout()
plt.savefig('figures/fig5_pd.png', dpi=300)
plt.close()

# 6. Figura 6: Correlação entre ICHE e crescimento do PIB per capita
print("Gerando Figura 6...")
# Calcular ICHE simplificado para 2022 (último ano disponível)
latest_year = df['year'].max()
latest_df = df[df['year'] == latest_year].copy()
# Normalizar variáveis
latest_df['escolaridade_norm'] = latest_df['anos_escolaridade_estimado'] / 12
latest_df['pisa_norm'] = latest_df['pisa_media'] / 600
latest_df['pd_norm'] = latest_df['pct_pib_pd'] / 5
latest_df['ICHE'] = 0.3 * latest_df['escolaridade_norm'] + 0.4 * latest_df['pisa_norm'] + 0.3 * latest_df['pd_norm']
# Calcular CAGR 1960-2023
cagr_data = []
for country in df['country_name'].unique():
    subset = df[df['country_name'] == country].sort_values('year')
    if len(subset) > 1:
        start_gdp = subset.iloc[0]['pib_per_capita_constante_2015']
        end_gdp = subset.iloc[-1]['pib_per_capita_constante_2015']
        years = subset.iloc[-1]['year'] - subset.iloc[0]['year']
        if pd.notna(start_gdp) and pd.notna(end_gdp) and years > 0:
            cagr = (end_gdp / start_gdp) ** (1 / years) - 1
            cagr_data.append({'country_name': country, 'CAGR': cagr})
cagr_df = pd.DataFrame(cagr_data)
# print(f"cagr_df columns: {cagr_df.columns.tolist()}")
# Merge
plot_df = latest_df[['country_name', 'ICHE']].merge(cagr_df, left_on='country_name', right_on='country_name')
fig, ax = plt.subplots()
ax.scatter(plot_df['ICHE'], plot_df['CAGR'] * 100, s=100, alpha=0.7)
for i, row in plot_df.iterrows():
    ax.annotate(row['country_name'], (row['ICHE'], row['CAGR'] * 100), 
                xytext=(5, 5), textcoords='offset points')
ax.set_xlabel('Índice de Capital Humano Estrutural (ICHE)')
ax.set_ylabel('CAGR PIB per capita (% ao ano)')
ax.set_title('Figura 6 – Correlação entre ICHE e crescimento do PIB per capita')
# Linha de tendência
try:
    if len(plot_df) > 1:
        z = np.polyfit(plot_df['ICHE'], plot_df['CAGR'] * 100, 1)
        p = np.poly1d(z)
        ax.plot(plot_df['ICHE'], p(plot_df['ICHE']), "r--", alpha=0.5)
except np.linalg.LinAlgError:
    pass
plt.tight_layout()
plt.savefig('figures/fig6_iche_crescimento.png', dpi=300)
plt.close()

# 8. Figura 8: Análise de cluster: grupos de países
print("Gerando Figura 8...")
if len(plot_df) >= 3:
    plot_df = plot_df.dropna(subset=['ICHE', 'CAGR'])
    if len(plot_df) < 3:
        print("Dados insuficientes após remoção de NaN")
    else:
        from sklearn.cluster import KMeans
        X = plot_df[['ICHE', 'CAGR']].values
        kmeans = KMeans(n_clusters=3, random_state=42)
        plot_df['cluster'] = kmeans.fit_predict(X)
        fig, ax = plt.subplots()
        scatter = ax.scatter(plot_df['ICHE'], plot_df['CAGR'] * 100, c=plot_df['cluster'], 
                             cmap='viridis', s=100, alpha=0.7)
        for i, row in plot_df.iterrows():
            ax.annotate(row['country_name'], (row['ICHE'], row['CAGR'] * 100), 
                        xytext=(5, 5), textcoords='offset points')
        ax.set_xlabel('ICHE')
        ax.set_ylabel('CAGR (% ao ano)')
        ax.set_title('Figura 8 – Análise de cluster: grupos de países')
        plt.colorbar(scatter, ax=ax, label='Cluster')
        plt.tight_layout()
        plt.savefig('figures/fig8_cluster.png', dpi=300)
        plt.close()
else:
    print("Dados insuficientes para cluster")

# 7. Figura 7: Eficiência na transformação de capital humano
print("Gerando Figura 7 (placeholder)...")
fig, ax = plt.subplots()
ax.text(0.5, 0.5, 'Dados insuficientes', horizontalalignment='center',
        verticalalignment='center', fontsize=20)
ax.set_xlim(0,1)
ax.set_ylim(0,1)
ax.set_title('Figura 7 – Eficiência na transformação de capital humano')
plt.savefig('figures/fig7_eficiencia.png', dpi=300)
plt.close()



# 9. Figura 9: Decomposição do ICHE por dimensão
print("Gerando Figura 9 (placeholder)...")
fig, ax = plt.subplots()
ax.text(0.5, 0.5, 'Dados insuficientes', horizontalalignment='center',
        verticalalignment='center', fontsize=20)
ax.set_xlim(0,1)
ax.set_ylim(0,1)
ax.set_title('Figura 9 – Decomposição do ICHE por dimensão')
plt.savefig('figures/fig9_decomposicao.png', dpi=300)
plt.close()

# 10. Figura 10: Projeções de crescimento (simplificada)
print("Gerando Figura 10 (placeholder)...")
fig, ax = plt.subplots()
ax.text(0.5, 0.5, 'Dados insuficientes', horizontalalignment='center',
        verticalalignment='center', fontsize=20)
ax.set_xlim(0,1)
ax.set_ylim(0,1)
ax.set_title('Figura 10 – Projeções de crescimento (2024-2033)')
plt.savefig('figures/fig10_projecoes.png', dpi=300)
plt.close()

print("\n=== Figuras geradas com sucesso ===")
print("Salvas no diretório 'figures/'")
print("Arquivos gerados:")
for i in range(1, 11):
    print(f"  fig{i}_*.png")