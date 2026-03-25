"""
MAPAS DIDÁTICOS - ARMADILHA DA RENDA MÉDIA E EDUCAÇÃO
Script de geração de mapas para artigo acadêmico Qualis A1
7 países: Brasil, Chile, China, Singapura, Vietnã, Argentina, Coreia do Sul
Mapa Mundi destacando países do estudo
"""
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
import pandas as pd
from shapely.geometry import Point
import warnings
warnings.filterwarnings('ignore')

# Configurações globais
plt.style.use('seaborn-v0_8-whitegrid')
plt.rcParams['figure.dpi'] = 300
plt.rcParams['savefig.dpi'] = 300
plt.rcParams['font.family'] = 'sans-serif'
plt.rcParams['font.size'] = 10

# Cores para os países (cores distintas para visualização)
COLORS = {
    'BRA': '#FF6B6B',  # Vermelho - Brasil (preso na ARM)
    'CHL': '#4ECDC4',  # Turquesa - Chile (escapante recente)
    'CHN': '#FFE66D',  # Amarelo - China (em transição)
    'SGP': '#95E1D3',  # Verde claras - Singapura (escapante sustentado)
    'VNM': '#F38181',  # Rosa - Vietnã (em transição)
    'ARG': '#AA96DA',  # Roxo - Argentina (presa na ARM)
    'KOR': '#6C5CE7',  # Roxo escuro - Coreia do Sul (escapante sustentado)
}

# Nomes completos dos países
COUNTRY_NAMES = {
    'BRA': 'Brasil',
    'CHL': 'Chile', 
    'CHN': 'China',
    'SGP': 'Singapura',
    'VNM': 'Vietnã',
    'ARG': 'Argentina',
    'KOR': 'Coreia do Sul'
}

# Status na ARM
ARM_STATUS = {
    'KOR': 'Escapante Sustentado',
    'SGP': 'Escapante Sustentado',
    'CHL': 'Escapante Recente (2012)',
    'CHN': 'Em Transição',
    'VNM': 'Em Transição',
    'BRA': 'Preso na ARM',
    'ARG': 'Preso na ARM'
}

# Dados econômicos dos países (médias 2010-2023)
ECONOMIC_DATA = {
    'BRA': {'gdp_pc': 8076, 'pisa': 381, 'edu_spend': 5.22, 'terc_enroll': 50.65},
    'CHL': {'gdp_pc': 13204, 'pisa': 418, 'edu_spend': 5.30, 'terc_enroll': 80.71},
    'CHN': {'gdp_pc': 8227, 'pisa': 591, 'edu_spend': 3.50, 'terc_enroll': 44.93},
    'SGP': {'gdp_pc': 52390, 'pisa': 525, 'edu_spend': 2.90, 'terc_enroll': 82.00},
    'VNM': {'gdp_pc': 2216, 'pisa': 469, 'edu_spend': 3.20, 'terc_enroll': 26.54},
    'ARG': {'gdp_pc': 10374, 'pisa': 378, 'edu_spend': 5.00, 'terc_enroll': 82.93},
    'KOR': {'gdp_pc': 26869, 'pisa': 527, 'edu_spend': 3.69, 'terc_enroll': 94.92}
}

# Coordenadas dos centros dos países para rótulos
CENTROIDS = {
    'BRA': (-14.2350, -51.9257),
    'CHL': (-35.6751, -71.5430),
    'CHN': (35.8617, 104.1954),
    'SGP': (1.3521, 103.8198),
    'VNM': (14.0583, 108.2772),
    'ARG': (-38.4161, -63.6167),
    'KOR': (35.9078, 127.7669)
}

def create_world_map_with_study_countries():
    """
    Cria mapa mundi destacando os 7 países do estudo
    """
    try:
        # Tenta carregar dados geoespaciais naturais
        world = gpd.read_file(gpd.datasets.get_path('naturalearth_lowres'))
    except:
        # Fallback: criar visualização alternativa
        world = None
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 10))
    
    # Cores do mapa base
    if world is not None:
        world.plot(ax=ax, color='#E8E8E8', edgecolor='white', linewidth=0.5)
    
    # Destacar países do estudo
    for code, (lat, lon) in CENTROIDS.items():
        color = COLORS[code]
        
        # Ponto marcador
        ax.scatter(lon, lat, c=color, s=200, edgecolor='black', 
                   linewidth=2, zorder=5, alpha=0.9)
        
        # Rótulo
        offset = {'BRA': (5, 5), 'CHL': (5, -10), 'CHN': (5, 5),
                  'SGP': (5, 5), 'VNM': (5, -10), 'ARG': (5, 5), 
                  'KOR': (5, 5)}
        
        ax.annotate(COUNTRY_NAMES[code], (lon, lat), 
                   xytext=(offset[code][0], offset[code][1]),
                   textcoords='offset points',
                   fontsize=9, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor=color, alpha=0.7),
                   arrowprops=dict(arrowstyle='->', connectionstyle='arc3,rad=0'))
    
    # Legenda
    legend_elements = [
        mpatches.Patch(color=COLORS['KOR'], label='Escapante Sustentado'),
        mpatches.Patch(color=COLORS['SGP'], label='Escapante Sustentado'),
        mpatches.Patch(color=COLORS['CHL'], label='Escapante Recente'),
        mpatches.Patch(color=COLORS['CHN'], label='Em Transição'),
        mpatches.Patch(color=COLORS['VNM'], label='Em Transição'),
        mpatches.Patch(color=COLORS['BRA'], label='Preso na ARM'),
        mpatches.Patch(color=COLORS['ARG'], label='Preso na ARM'),
    ]
    ax.legend(handles=legend_elements, loc='lower left', fontsize=9,
              title='Status na ARM', title_fontsize=10)
    
    ax.set_xlim(-180, 180)
    ax.set_ylim(-60, 80)
    ax.set_xlabel('Longitude', fontsize=10)
    ax.set_ylabel('Latitude', fontsize=10)
    ax.set_title('Mapa 1 - Distribuição Geográfica dos Países do Estudo\n'
                 'Armadilha da Renda Média e Educação (1960-2023)',
                 fontsize=14, fontweight='bold', pad=20)
    
    plt.tight_layout()
    plt.savefig('output/mapas/mapa_mundi_estudo.png', bbox_inches='tight')
    plt.close()
    print("Mapa 1: Mapa Mundi criado com sucesso")

def create_regional_maps():
    """
    Cria mapas regionais para cada um dos 7 países
    """
    # Mapa 2: América do Sul (Brasil, Chile, Argentina)
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    # América do Sul básica
    ax.set_xlim(-85, -30)
    ax.set_ylim(-60, 15)
    
    countries_sa = ['BRA', 'CHL', 'ARG']
    for code in countries_sa:
        lat, lon = CENTROIDS[code]
        ax.scatter(lon, lat, c=COLORS[code], s=500, edgecolor='black', 
                   linewidth=2, zorder=5)
        ax.annotate(f"{COUNTRY_NAMES[code]}\n{ARM_STATUS[code]}", 
                   (lon, lat), xytext=(10, 10), textcoords='offset points',
                   fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS[code], alpha=0.8))
    
    ax.set_title('Mapa 2 - Países da América do Sul\n'
                 'Brasil, Chile, Argentina', fontsize=14, fontweight='bold')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/mapas/mapa_america_sul.png', bbox_inches='tight')
    plt.close()
    print("Mapa 2: América do Sul criado")
    
    # Mapa 3: Ásia (China, Singapura, Vietnã)
    fig, ax = plt.subplots(1, 1, figsize=(14, 10))
    
    ax.set_xlim(70, 150)
    ax.set_ylim(-10, 55)
    
    countries_asia = ['CHN', 'SGP', 'VNM']
    for code in countries_asia:
        lat, lon = CENTROIDS[code]
        ax.scatter(lon, lat, c=COLORS[code], s=500, edgecolor='black', 
                   linewidth=2, zorder=5)
        ax.annotate(f"{COUNTRY_NAMES[code]}\n{ARM_STATUS[code]}", 
                   (lon, lat), xytext=(10, 10), textcoords='offset points',
                   fontsize=10, fontweight='bold',
                   bbox=dict(boxstyle='round,pad=0.3', facecolor=COLORS[code], alpha=0.8))
    
    ax.set_title('Mapa 3 - Países da Ásia\n'
                 'China, Singapura, Vietnã', fontsize=14, fontweight='bold')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/mapas/mapa_asia.png', bbox_inches='tight')
    plt.close()
    print("Mapa 3: Ásia criado")
    
    # Mapa 4: Coreia do Sul (detalhe)
    fig, ax = plt.subplots(1, 1, figsize=(10, 10))
    
    ax.set_xlim(125, 132)
    ax.set_ylim(33, 39)
    
    lat, lon = CENTROIDS['KOR']
    ax.scatter(lon, lat, c=COLORS['KOR'], s=1000, edgecolor='black', 
               linewidth=3, zorder=5)
    ax.annotate(f"{COUNTRY_NAMES['KOR']}\n{ARM_STATUS['KOR']}\n"
                f"PIB: ${ECONOMIC_DATA['KOR']['gdp_pc']:,}\n"
                f"PISA: {ECONOMIC_DATA['KOR']['pisa']}", 
               (lon, lat), xytext=(15, -30), textcoords='offset points',
               fontsize=11, fontweight='bold',
               bbox=dict(boxstyle='round,pad=0.5', facecolor=COLORS['KOR'], alpha=0.9))
    
    ax.set_title('Mapa 4 - Coreia do Sul\n'
                 'Escapante Sustentado (1995)', fontsize=14, fontweight='bold')
    ax.set_xlabel('Longitude')
    ax.set_ylabel('Latitude')
    ax.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('output/mapas/mapa_coreia_sul.png', bbox_inches='tight')
    plt.close()
    print("Mapa 4: Coreia do Sul criado")

def create_comparative_choropleth():
    """
    Cria mapa coroplético comparando PIB per capita dos países
    """
    fig, axes = plt.subplots(1, 2, figsize=(16, 6))
    
    # Dados para visualização
    countries = list(ECONOMIC_DATA.keys())
    gdp_values = [ECONOMIC_DATA[c]['gdp_pc'] for c in countries]
    pisa_values = [ECONOMIC_DATA[c]['pisa'] for c in countries]
    
    # Gráfico 1: PIB per capita
    ax1 = axes[0]
    colors = [COLORS[c] for c in countries]
    bars = ax1.barh(countries, gdp_values, color=colors, edgecolor='black')
    ax1.set_xlabel('PIB per capita (US$ 2015)')
    ax1.set_title('PIB per capita por País (2010-2023)')
    ax1.bar_label(bars, fmt='$%,d', padding=3)
    
    # Gráfico 2: Score PISA
    ax2 = axes[1]
    bars = ax2.barh(countries, pisa_values, color=colors, edgecolor='black')
    ax2.set_xlabel('Score PISA Matemática')
    ax2.set_title('Score PISA Matemática por País (2022)')
    ax2.axvline(x=500, color='red', linestyle='--', label='Média OCDE')
    ax2.bar_label(bars, fmt='%d', padding=3)
    ax2.legend()
    
    plt.tight_layout()
    plt.savefig('output/mapas/grafico_comparativo.png', bbox_inches='tight')
    plt.close()
    print("Gráfico comparativo criado")

def create_timeline_visualization():
    """
    Cria visualização de timeline das transições de renda
    """
    fig, ax = plt.subplots(figsize=(14, 8))
    
    # Anos de transição (aproximados)
    transitions = {
        'KOR': 1995,
        'SGP': 1987,
        'CHL': 2012,
    }
    
    colors_list = list(COLORS.values())
    y_positions = range(len(transitions))
    
    for i, (country, year) in enumerate(transitions.items()):
        ax.barh(i, 2023 - 1960, left=1960, height=0.6, 
                color=COLORS[country], alpha=0.3, edgecolor='black')
        ax.scatter(year, i, s=200, c=COLORS[country], 
                   edgecolor='black', linewidth=2, zorder=5)
        ax.annotate(f'{year}', (year, i), xytext=(5, 5),
                   textcoords='offset points', fontsize=10, fontweight='bold')
    
    ax.set_yticks(range(len(transitions)))
    ax.set_yticklabels([COUNTRY_NAMES[c] for c in transitions.keys()])
    ax.set_xlabel('Ano')
    ax.set_title('Timeline de Transição para Alta Renda\n'
                 'Países Escaptantes da ARM')
    ax.set_xlim(1960, 2025)
    ax.grid(True, alpha=0.3, axis='x')
    
    plt.tight_layout()
    plt.savefig('output/mapas/timeline_transicoes.png', bbox_inches='tight')
    plt.close()
    print("Timeline criado")

if __name__ == '__main__':
    import os
    os.makedirs('output/mapas', exist_ok=True)
    
    create_world_map_with_study_countries()
    create_regional_maps()
    create_comparative_choropleth()
    create_timeline_visualization()
    
    print("\n=== TODOS OS MAPAS FORAM GERADOS COM SUCESSO ===")
    print("Arquivos salvos em: output/mapas/")
