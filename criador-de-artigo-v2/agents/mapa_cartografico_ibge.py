#!/usr/bin/env python3
"""
================================================================================
MAPA_CARTOGRAFICO_IBGE.py — Cartografia Profissional com Padrão IBGE
================================================================================
Este script gera mapas profissionais seguindo rigor cartográfico do IBGE:
- Sistema de Referência: SIRGAS 2000 (EPSG:4674)
- Projeção: Plate Carree ou UTM conforme escala
- Elementos obrigatórios: Título, Legenda, Escala, Norte, Fonte, EPSG

Uso:
    python mapa_cartografico_ibge.py --regiao brasil --tema "IDH" --output mapas/

Dependências:
    pip install geopandas matplotlib cartopy matplotlib-scalebar
================================================================================
"""
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as path_effects
from matplotlib.patches import FancyArrowPatch
from matplotlib_scalebar.scalebar import ScaleBar
import warnings
warnings.filterwarnings('ignore')

OUTPUT_DIR = "mapas/"

def get_brazil_states():
    """Baixa malha territorial do Brasil via IBGE API."""
    url = "https://servicodados.ibge.gov.br/api/v3/malhas/paises/BR?formato=application/vnd.geo+json&intrarregiao=UF"
    gdf = gpd.read_file(url)
    return gdf

def gerar_mapa_brasil_ibge(dados=None, estados=None, titulo="Mapa do Brasil", arquivo="mapa_brasil.png"):
    """
    Gera mapa do Brasil seguindo padrão cartográfico IBGE.
    
    Elementos obrigatórios incluídos:
    1. Título
    2. Legenda
    3. Escala gráfica
    4. Norte geográfico
    5. Sistema de coordenadas (EPSG)
    6. Fonte dos dados
    7. Autoria/Data
    """
    print(f"Gerando: {titulo}")
    
    fig, ax = plt.subplots(1, 1, figsize=(18, 14))
    
    nordeste = ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']
    
    for idx, row in estados.iterrows():
        color = '#FF6B35' if row['sigla'] in nordeste else '#D3D3D3'
        edge = '#CC4400' if row['sigla'] in nordeste else '#A0A0A0'
        lw = 1.5 if row['sigla'] in nordeste else 0.8
        
        gpd.GeoSeries([row.geometry]).plot(ax=ax, color=color, edgecolor=edge, linewidth=lw)
        
        if row['sigla'] in nordeste:
            centroid = row.geometry.centroid
            ax.annotate(row['sigla'], xy=(centroid.x, centroid.y),
                       fontsize=10, ha='center', va='center', fontweight='bold', color='white')
    
    # 1. TÍTULO
    ax.set_title(titulo, fontsize=18, fontweight='bold', pad=20)
    
    # 2. EIXOS COM GRATICULA
    ax.set_xlabel('Longitude', fontsize=11)
    ax.set_ylabel('Latitude', fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.3, color='gray')
    ax.set_xlim(-75, -30)
    ax.set_ylim(-35, 6)
    
    # 3. ESCALA GRÁFICA
    scalebar = ScaleBar(dx=1, units='km', location='lower right', 
                        length_fraction=0.15, height_fraction=0.02,
                        font_properties={'size': 10})
    ax.add_artist(scalebar)
    
    # 4. NORTE GEOGRÁFICO
    x_n, y_n, arrow_l = 0.97, 0.97, 0.06
    ax.annotate('N', xy=(x_n, y_n), xytext=(x_n, y_n - arrow_l),
                arrowprops=dict(facecolor='black', width=4, headwidth=12),
                ha='center', va='center', fontsize=16, fontweight='bold',
                xycoords=ax.transAxes)
    
    # 5. LEGENDA
    legend = ax.legend(handles=[
        mpatches.Patch(color='#FF6B35', label='Nordeste'),
        mpatches.Patch(color='#D3D3D3', label='Outras Regioes')
    ], loc='lower left', fontsize=10, title='Regioes', title_fontsize=11)
    
    # 6. FONTE E METADADOS
    texto_fonte = (
        "Fonte: IBGE Malhas Territoriais (API v3)\n"
        "Sistema de Referencia: SIRGAS 2000 (EPSG:4674)\n"
        "Elaboracao: Tese MCP - UFC Crateus | 2026\n"
        "Projecao: Geografica (Plate Carree)"
    )
    fig.text(0.15, 0.08, texto_fonte, fontsize=9, ha='left', va='bottom',
            bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray'))
    
    plt.tight_layout()
    caminho = f"{OUTPUT_DIR}{arquivo}"
    plt.savefig(caminho, dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  [OK] {caminho}")

def gerar_mapa_nordeste_ibge(dados=None, titulo="Regiao Nordeste", arquivo="mapa_nordeste.png"):
    """Gera mapa da regiao Nordeste com padrao IBGE."""
    print(f"Gerando: {titulo}")
    
    fig, ax = plt.subplots(1, 1, figsize=(16, 12))
    
    estados = get_brazil_states()
    nordeste = ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']
    
    cores = ['#FF6B35', '#FFD700', '#32CD32', '#1E90FF', '#FF1493',
             '#8A2BE2', '#00CED1', '#FF6347', '#4682B4']
    
    ne = estados[estados['sigla'].isin(nordeste)]
    
    for i, (idx, row) in enumerate(ne.iterrows()):
        gpd.GeoSeries([row.geometry]).plot(ax=ax, color=cores[i], 
                                          edgecolor='black', linewidth=1.5)
        centroid = row.geometry.centroid
        ax.annotate(row['sigla'], xy=(centroid.x, centroid.y),
                   fontsize=14, ha='center', va='center', fontweight='bold', color='white')
    
    ax.set_title(titulo, fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Longitude', fontsize=11)
    ax.set_ylabel('Latitude', fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_xlim(-48, -32)
    ax.set_ylim(-16, -1)
    
    # Escala
    scalebar = ScaleBar(dx=1, units='km', location='lower right', 
                        length_fraction=0.15, font_properties={'size': 9})
    ax.add_artist(scalebar)
    
    # Norte
    ax.annotate('N', xy=(0.97, 0.97), xytext=(0.97, 0.91),
                arrowprops=dict(facecolor='black', width=4, headwidth=12),
                ha='center', va='center', fontsize=14, fontweight='bold',
                xycoords=ax.transAxes)
    
    # Fonte
    texto_fonte = (
        "Fonte: IBGE (2024)\n"
        "Sistema: SIRGAS 2000 (EPSG:4674)\n"
        "Elaboracao: Marcelo Claro Laranjeira | UFC Crateus"
    )
    fig.text(0.12, 0.06, texto_fonte, fontsize=9, ha='left', va='bottom',
            bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray'))
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}{arquivo}", dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  [OK] {OUTPUT_DIR}{arquivo}")

def gerar_mapa_ceara_ibge(titulo="Estado do Ceara", arquivo="mapa_ceara.png"):
    """Gera mapa do estado do Ceara com padrao IBGE."""
    print(f"Gerando: {titulo}")
    
    fig, ax = plt.subplots(1, 1, figsize=(14, 12))
    
    estados = get_brazil_states()
    ceara = estados[estados['sigla'] == 'CE']
    
    gpd.GeoSeries(ceara.geometry.values).plot(ax=ax, facecolor='#FFB347', 
                                             edgecolor='black', linewidth=2)
    
    centroid = ceara.geometry.iloc[0].centroid
    ax.annotate('CEARA', xy=(centroid.x, centroid.y), fontsize=24, ha='center', va='center',
               fontweight='bold', color='white')
    
    # Marker para Crateus
    ax.plot(-40.4108, -5.7433, 'o', markersize=10, color='red', 
           markeredgecolor='darkred', zorder=10)
    ax.annotate('IFCE\nCrateus', xy=(-40.4108, -5.7433), xytext=(10, 10),
               textcoords='offset points', fontsize=10, fontweight='bold',
               arrowprops=dict(arrowstyle='->', color='red'))
    
    ax.set_title(titulo, fontsize=18, fontweight='bold', pad=20)
    ax.set_xlabel('Longitude', fontsize=11)
    ax.set_ylabel('Latitude', fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.3)
    ax.set_xlim(-41.5, -37)
    ax.set_ylim(-8, -2.5)
    
    # Escala
    scalebar = ScaleBar(dx=1, units='km', location='lower right', 
                        length_fraction=0.2, font_properties={'size': 9})
    ax.add_artist(scalebar)
    
    # Norte
    ax.annotate('N', xy=(0.97, 0.97), xytext=(0.97, 0.91),
                arrowprops=dict(facecolor='black', width=4, headwidth=12),
                ha='center', va='center', fontsize=14, fontweight='bold',
                xycoords=ax.transAxes)
    
    # Legenda
    ax.plot([], [], 'o', color='red', label='IFCE Campus Crateus')
    ax.legend(loc='upper left', fontsize=9)
    
    # Fonte
    texto_fonte = (
        "Fonte: IBGE Malhas (2024)\n"
        "Sistema: SIRGAS 2000 (EPSG:4674)\n"
        "Elaboracao: Tese MCP - UFC Crateus"
    )
    fig.text(0.10, 0.05, texto_fonte, fontsize=9, ha='left', va='bottom',
            bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray'))
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}{arquivo}", dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  [OK] {OUTPUT_DIR}{arquivo}")

def gerar_mapa_crateus_ibge(titulo="Localizacao: IFCE Campus Crateus", arquivo="mapa_crateus.png"):
    """Gera mapa detalhado de Crateus com padrao IBGE."""
    print(f"Gerando: {titulo}")
    
    fig, ax = plt.subplots(1, 1, figsize=(12, 10))
    
    crateus_lat, crateus_lon = -5.7433, -40.4108
    
    # IFCE marker
    ax.plot(crateus_lon, crateus_lat, 'o', markersize=12, color='#FF0000', 
           markeredgecolor='#8B0000', markeredgewidth=2, zorder=10)
    ax.annotate('IFCE Campus\nCrateus', xy=(crateus_lon, crateus_lat),
               xytext=(0.5, 0.5), textcoords='offset points',
               fontsize=11, fontweight='bold', color='#8B0000',
               arrowprops=dict(arrowstyle='->', color='#8B0000', lw=2))
    
    # Cidades do entorno
    cidades = {
        'Tamboril': (-4.79, -40.82), 'Ipueiras': (-4.35, -40.71),
        'Novo Oriente': (-5.47, -40.74), 'Pereiro': (-5.96, -38.47),
        'Varjota': (-4.53, -40.47), 'Santa Quiteria': (-4.33, -40.15)
    }
    for cidade, (lat, lon) in cidades.items():
        ax.plot(lon, lat, 'o', markersize=8, color='#228B22', zorder=5)
        ax.annotate(cidade, xy=(lon, lat), xytext=(0.2, 0.2),
                   textcoords='offset points', fontsize=9,
                   arrowprops=dict(arrowstyle='->', color='#228B22'))
    
    ax.set_title(titulo, fontsize=16, fontweight='bold', pad=15)
    ax.set_xlabel('Longitude', fontsize=11)
    ax.set_ylabel('Latitude', fontsize=11)
    ax.grid(True, linestyle='--', alpha=0.4)
    ax.set_xlim(-41.5, -38)
    ax.set_ylim(-7, -4)
    
    # Escala
    scalebar = ScaleBar(dx=1, units='km', location='lower right', 
                        length_fraction=0.2, font_properties={'size': 8})
    ax.add_artist(scalebar)
    
    # Norte
    ax.annotate('N', xy=(0.97, 0.97), xytext=(0.97, 0.91),
                arrowprops=dict(facecolor='black', width=3, headwidth=10),
                ha='center', va='center', fontsize=12, fontweight='bold',
                xycoords=ax.transAxes)
    
    # Legenda
    legend_elements = [
        plt.Line2D([0], [0], marker='o', color='w', label='IFCE Campus Crateus',
                  markerfacecolor='#FF0000', markersize=10, markeredgecolor='#8B0000'),
        plt.Line2D([0], [0], marker='o', color='w', label='Municipios',
                  markerfacecolor='#228B22', markersize=8),
    ]
    ax.legend(handles=legend_elements, loc='upper right', fontsize=9)
    
    # Fonte
    texto_fonte = (
        "Coordenadas: -5.7433, -40.4108\n"
        "Sistema: SIRGAS 2000 (EPSG:4674)\n"
        "Elaboracao: Marcelo Claro Laranjeira | 2026"
    )
    fig.text(0.08, 0.05, texto_fonte, fontsize=8, ha='left', va='bottom',
            bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray'))
    
    plt.tight_layout()
    plt.savefig(f"{OUTPUT_DIR}{arquivo}", dpi=300, bbox_inches='tight', facecolor='white')
    plt.close()
    print(f"  [OK] {OUTPUT_DIR}{arquivo}")

def main():
    import os
    os.makedirs(OUTPUT_DIR, exist_ok=True)
    
    print("=" * 60)
    print("  MAPAS CARTOGRAFICOS - PADRAO IBGE")
    print("  Sistema: SIRGAS 2000 (EPSG:4674)")
    print("=" * 60)
    
    estados = get_brazil_states()
    
    gerar_mapa_brasil_ibge(
        estados=estados,
        titulo="MAPA DO BRASIL: Regiao Nordeste em Destaque\n(Tese: MCP e Educacao no Sertao do Ceara)",
        arquivo="mapa_brasil_ibge.png"
    )
    
    gerar_mapa_nordeste_ibge(
        titulo="MAPA DA REGIAO NORDESTE DO BRASIL\n(Estados Incluidos no Estudo)",
        arquivo="mapa_nordeste_ibge.png"
    )
    
    gerar_mapa_ceara_ibge(
        titulo="MAPA DO ESTADO DO CEARA\nDestaque para IFCE Campus Crateus",
        arquivo="mapa_ceara_ibge.png"
    )
    
    gerar_mapa_crateus_ibge(
        titulo="LOCALIZACAO: IFCE Campus Crateus - Sertao do Ceara",
        arquivo="mapa_crateus_ibge.png"
    )
    
    print("=" * 60)
    print("  TODOS OS MAPAS GERADOS COM SUCESSO!")
    print("  Formato: PNG (300 DPI)")
    print("  Sistema: SIRGAS 2000 (EPSG:4674)")
    print("=" * 60)

if __name__ == "__main__":
    main()
