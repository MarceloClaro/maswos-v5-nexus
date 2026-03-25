#!/usr/bin/env python3
"""
================================================================================
MAPAS CARTOGRÁFICOS PROFISSIONAIS - TESE DOUTORADO MCP
================================================================================
Cartografia de alta qualidade seguindo padrões IBGE para publicação acadêmica.

Recursos:
- SIRGAS 2000 (EPSG:4674)
- Escala gráfica profissional
- Norte geográfico
- Encarte (inset map) mostrando localização no Brasil
- Setores censitários via geobr
- Elementos limpos sem marcadores exagerados

Uso:
    python gerar_mapas_ibge_completo.py

Dependências:
    pip install geopandas matplotlib geobr matplotlib-scalebar contextily
================================================================================
"""
import geopandas as gpd
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.patheffects as path_effects
from matplotlib.lines import Line2D
from matplotlib_scalebar.scalebar import ScaleBar
from mpl_toolkits.axes_grid1.inset_locator import inset_axes
import warnings
warnings.filterwarnings('ignore')

import os

OUTPUT_DIR = "output/"
os.makedirs(OUTPUT_DIR, exist_ok=True)

CRATEUS_LAT = -5.7433
CRATEUS_LON = -40.4108
CRATEUS_IBGE = "2304103"


def get_ibge_states():
    """Obtém malha territorial do Brasil via GeoJSON alternativo."""
    url = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/brazil-states.geojson"
    return gpd.read_file(url)


def get_municipality_boundary(ibge_code=None):
    """Obtém limite municipal - usa arquivo local se disponível."""
    local_file = f"output/geobr_data/crateus_municipio.geojson"
    if os.path.exists(local_file):
        return gpd.read_file(local_file)
    return None


def get_census_tracts(ibge_code=None):
    """Obtém setores censitários - usa arquivo local se disponível."""
    local_file = f"output/geobr_data/crateus_setores_censitarios.geojson"
    if os.path.exists(local_file):
        return gpd.read_file(local_file)
    return None


def get_neighborhoods(ibge_code=None):
    """Obtém bairros - usa arquivo local se disponível."""
    local_file = f"output/geobr_data/crateus_bairros.geojson"
    if os.path.exists(local_file):
        return gpd.read_file(local_file)
    return None


def create_professional_figure(title, xlim, ylim, size=(16, 14)):
    """Cria figura profissional com configurações padrão."""
    fig, ax = plt.subplots(1, 1, figsize=size)
    fig.patch.set_facecolor('white')
    ax.set_xlim(xlim)
    ax.set_ylim(ylim)
    ax.grid(True, linestyle=':', alpha=0.4, color='gray')
    ax.set_xlabel('Longitude', fontsize=10)
    ax.set_ylabel('Latitude', fontsize=10)
    return fig, ax


def add_scale_bar(ax, location='lower right'):
    """Adiciona escala gráfica profissional."""
    scalebar = ScaleBar(
        dx=1, 
        units='km', 
        location=location,
        length_fraction=0.20,
        height_fraction=0.015,
        pad=0.4,
        border_pad=0.5,
        color='black',
        box_color='white',
        box_alpha=0.9,
        font_properties={'size': 9}
    )
    ax.add_artist(scalebar)
    return scalebar


def add_north_arrow(ax, x=0.95, y=0.95):
    """Adiciona norte geográfico estilizado."""
    ax.annotate(
        'N', 
        xy=(x, y), 
        xytext=(x, y - 0.08),
        xycoords='axes fraction',
        textcoords='axes fraction',
        arrowprops=dict(
            facecolor='#333333', 
            edgecolor='#333333',
            width=3,
            headwidth=10,
            headlength=8
        ),
        ha='center', 
        va='center', 
        fontsize=14, 
        fontweight='bold',
        color='#333333'
    )


def add_legend(ax, elements, location='lower left', title='Legenda'):
    """Adiciona legenda profissional."""
    legend = ax.legend(
        handles=elements,
        loc=location,
        fontsize=9,
        title=title,
        title_fontsize=10,
        framealpha=0.95,
        edgecolor='gray'
    )
    return legend


def add_source_footer(fig, source_text, system_text="SIRGAS 2000 (EPSG:4674)", author="Marcelo Claro Laranjeira | UFC Crateús | 2026"):
    """Adiciona rodapé com fonte e metadados."""
    full_text = f"{source_text}\n{author}"
    fig.text(0.15, 0.02, full_text, fontsize=8, ha='left', va='bottom',
            style='italic', color='#555555')
    fig.text(0.85, 0.02, system_text, fontsize=8, ha='right', va='bottom',
            bbox=dict(facecolor='white', alpha=0.9, edgecolor='gray', pad=3))


def add_inset_location(ax, location='upper left', width='25%', height='25%'):
    """Adiciona encarte mostrando localização no contexto nacional."""
    ax_inset = inset_axes(ax, width=width, height=height, loc=location,
                         borderpad=0, bbox_to_anchor=(0.02, 0.98, 1, 1),
                         bbox_transform=ax.transAxes)
    
    url = "https://raw.githubusercontent.com/codeforgermany/click_that_hood/main/public/data/brazil-states.geojson"
    brasil = gpd.read_file(url)
    
    brasil.plot(ax=ax_inset, color='#E8E8E8', edgecolor='#CCCCCC', linewidth=0.3)
    
    nordeste = ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']
    ne = brasil[brasil['sigla'].isin(nordeste)]
    ne.plot(ax=ax_inset, color='#FF6B35', edgecolor='#CC4400', linewidth=0.5)
    
    ax_inset.plot(-40.4108, -5.7433, 'o', markersize=5, color='red', 
                  markeredgecolor='darkred', zorder=10)
    
    ax_inset.set_xlim(-75, -30)
    ax_inset.set_ylim(-35, 6)
    ax_inset.set_xticks([])
    ax_inset.set_yticks([])
    ax_inset.set_title('Localização no Brasil', fontsize=8, fontweight='bold', pad=2)
    ax_inset.spines['top'].set_visible(True)
    ax_inset.spines['right'].set_visible(True)
    ax_inset.spines['bottom'].set_visible(True)
    ax_inset.spines['left'].set_visible(True)
    
    return ax_inset


def create_brazil_map_with_inset():
    """Mapa do Brasil com encarte mostrando Nordeste."""
    print("\n[1/6] Gerando mapa do Brasil com encarte...")
    
    fig, ax = create_professional_figure(
        "MAPA DO BRASIL: REGIÃO NORDESTE EM DESTAQUE",
        xlim=(-75, -30),
        ylim=(-35, 6),
        size=(18, 14)
    )
    
    estados = get_ibge_states()
    nordeste = ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']
    
    outras = estados[~estados['sigla'].isin(nordeste)]
    gpd.GeoSeries(outras.geometry.values).plot(
        ax=ax, color='#D8D8D8', edgecolor='#AAAAAA', linewidth=0.5
    )
    
    ne_states = estados[estados['sigla'].isin(nordeste)]
    gpd.GeoSeries(ne_states.geometry.values).plot(
        ax=ax, color='#FF6B35', edgecolor='#CC4400', linewidth=1.2
    )
    
    for _, row in ne_states.iterrows():
        centroid = row.geometry.centroid
        ax.annotate(
            row['sigla'], 
            xy=(centroid.x, centroid.y),
            fontsize=10, 
            ha='center', 
            va='center', 
            fontweight='bold', 
            color='white',
            path_effects=[path_effects.withStroke(linewidth=2, foreground='#444444')]
        )
    
    ax.plot(-40.4108, -5.7433, 'o', markersize=8, color='red', 
           markeredgecolor='darkred', markeredgewidth=1.5, zorder=10)
    
    ax.set_title(
        "MAPA DO BRASIL: REGIÃO NORDESTE EM DESTAQUE\n"
        r"$\bf{Área\ de\ Estudo:\ IFCE\ Campus\ Crateús\ -\ Ceará}$",
        fontsize=16, fontweight='bold', pad=20
    )
    
    elements = [
        mpatches.Patch(color='#FF6B35', label='Região Nordeste'),
        mpatches.Patch(color='#D8D8D8', label='Outras Regiões'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='red', 
                  markersize=8, markeredgecolor='darkred', label='IFCE Crateús')
    ]
    add_legend(ax, elements, location='lower right', title='Legenda')
    
    add_inset_location(ax)
    add_scale_bar(ax, location='lower left')
    add_north_arrow(ax, x=0.92, y=0.92)
    
    add_source_footer(
        fig, 
        "Fonte: IBGE Malhas Territoriais (API v3, 2024)",
        "SIRGAS 2000 | EPSG:4674"
    )
    
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig(f'{OUTPUT_DIR}mapa_brasil_com_inset.png', dpi=300, 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("  [OK] mapa_brasil_com_inset.png")


def create_northeast_map():
    """Mapa da região Nordeste com estados coloridos."""
    print("\n[2/6] Gerando mapa do Nordeste...")
    
    fig, ax = create_professional_figure(
        "REGIÃO NORDESTE DO BRASIL",
        xlim=(-48, -32),
        ylim=(-16, -1),
        size=(16, 12)
    )
    
    estados = get_ibge_states()
    nordeste = ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']
    
    cores = {
        'MA': '#E74C3C', 'PI': '#F39C12', 'CE': '#27AE60', 
        'RN': '#3498DB', 'PB': '#9B59B6', 'PE': '#1ABC9C',
        'AL': '#E91E63', 'SE': '#00BCD4', 'BA': '#FF5722'
    }
    
    labels = {
        'MA': 'Maranhão', 'PI': 'Piauí', 'CE': 'Ceará', 
        'RN': 'Rio Grande do Norte', 'PB': 'Paraíba', 'PE': 'Pernambuco',
        'AL': 'Alagoas', 'SE': 'Sergipe', 'BA': 'Bahia'
    }
    
    for _, row in estados[estados['sigla'].isin(nordeste)].iterrows():
        cor = cores.get(row['sigla'], '#888888')
        gpd.GeoSeries([row.geometry]).plot(
            ax=ax, color=cor, edgecolor='black', linewidth=1.5
        )
        centroid = row.geometry.centroid
        ax.annotate(
            row['sigla'], 
            xy=(centroid.x, centroid.y),
            fontsize=12, 
            ha='center', 
            va='center', 
            fontweight='bold', 
            color='white',
            path_effects=[path_effects.withStroke(linewidth=2, foreground='#333333')]
        )
    
    ax.plot(-40.4108, -5.7433, 'D', markersize=10, color='red', 
           markeredgecolor='darkred', markeredgewidth=2, zorder=10)
    
    ax.set_title(
        "REGIÃO NORDESTE DO BRASIL\n"
        r"$\bf{9\ Estados\ -\ Área\ de\ Estudo\ Destacada}$",
        fontsize=16, fontweight='bold', pad=20
    )
    
    elements = [mpatches.Patch(color=cor, label=f"{labels[sigla]} ({sigla})") 
               for sigla, cor in cores.items()]
    elements.append(plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='red',
                               markersize=10, markeredgecolor='darkred', 
                               label='IFCE Crateús (CE)'))
    add_legend(ax, elements, location='lower right', title='Estados')
    
    add_inset_location(ax, width='22%', height='22%')
    add_scale_bar(ax, location='lower left')
    add_north_arrow(ax)
    
    add_source_footer(
        fig, 
        "Fonte: IBGE Malhas Territoriais (API v3, 2024)",
        "SIRGAS 2000 | EPSG:4674"
    )
    
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig(f'{OUTPUT_DIR}mapa_nordeste_estados.png', dpi=300, 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("  [OK] mapa_nordeste_estados.png")


def create_ceara_map():
    """Mapa do estado do Ceará com destaque para Crateús."""
    print("\n[3/6] Gerando mapa do Ceará...")
    
    fig, ax = create_professional_figure(
        "ESTADO DO CEARÁ",
        xlim=(-41.5, -37),
        ylim=(-8, -2.5),
        size=(14, 12)
    )
    
    estados = get_ibge_states()
    ceara = estados[estados['sigla'] == 'CE']
    
    vizinhos = estados[estados['sigla'].isin(['PI', 'RN', 'PB', 'PE'])]
    for _, row in vizinhos.iterrows():
        gpd.GeoSeries([row.geometry]).plot(
            ax=ax, color='#E8E8E8', edgecolor='#CCCCCC', linewidth=1
        )
    
    gpd.GeoSeries(ceara.geometry.values).plot(
        ax=ax, facecolor='#27AE60', edgecolor='#1E8449', linewidth=2.5
    )
    
    centroid = ceara.geometry.iloc[0].centroid
    ax.annotate(
        'CEARÁ', 
        xy=(centroid.x, centroid.y), 
        fontsize=28, 
        ha='center', 
        va='center',
        fontweight='bold', 
        color='white',
        path_effects=[path_effects.withStroke(linewidth=3, foreground='#145A32')]
    )
    
    ax.plot(-40.4108, -5.7433, 'D', markersize=12, color='red', 
           markeredgecolor='darkred', markeredgewidth=2, zorder=10)
    ax.annotate(
        'IFCE Campus Crateús\n(-5.7433, -40.4108)', 
        xy=(-40.4108, -5.7433),
        xytext=(-41.0, -4.5),
        fontsize=10,
        fontweight='bold',
        arrowprops=dict(arrowstyle='->', color='red', lw=1.5),
        bbox=dict(boxstyle='round,pad=0.3', facecolor='white', edgecolor='red', alpha=0.9)
    )
    
    ax.set_title(
        "ESTADO DO CEARÁ\n"
        r"$\bf{Destaque\ para\ IFCE\ Campus\ Crateús\ -\ Região\ do\ Sertão\ Central}$",
        fontsize=16, fontweight='bold', pad=20
    )
    
    elements = [
        mpatches.Patch(color='#27AE60', label='Ceará'),
        mpatches.Patch(color='#E8E8E8', label='Estados Vizinhos'),
        plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='red',
                  markersize=10, markeredgecolor='darkred', label='IFCE Crateús')
    ]
    add_legend(ax, elements, location='upper left', title='Legenda')
    
    add_inset_location(ax, width='28%', height='28%')
    add_scale_bar(ax)
    add_north_arrow(ax)
    
    add_source_footer(
        fig, 
        "Fonte: IBGE Malhas Territoriais (API v3, 2024)",
        "SIRGAS 2000 | EPSG:4674"
    )
    
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig(f'{OUTPUT_DIR}mapa_ceara_crateus.png', dpi=300, 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("  [OK] mapa_ceara_crateus.png")


def create_crateus_map_with_tracts():
    """Mapa detalhado de Crateús com setores censitários."""
    print("\n[4/6] Gerando mapa de Crateús com setores censitários...")
    
    fig, ax = create_professional_figure(
        "LOCALIZAÇÃO: IFCE CAMPUS CRATEÚS",
        xlim=(-41.2, -39.6),
        ylim=(-6.3, -5.1),
        size=(14, 11)
    )
    
    ax.plot(CRATEUS_LON, CRATEUS_LAT, 'D', markersize=14, color='#C0392B', 
           markeredgecolor='darkred', markeredgewidth=2, zorder=10)
    ax.annotate(
        'IFCE Campus Crateús\nSertão Central - Ceará',
        xy=(CRATEUS_LON, CRATEUS_LAT),
        xytext=(-41.0, -5.2),
        fontsize=11,
        fontweight='bold',
        ha='center',
        arrowprops=dict(arrowstyle='->', color='#C0392B', lw=2),
        bbox=dict(boxstyle='round,pad=0.4', facecolor='white', 
                  edgecolor='#C0392B', alpha=0.95)
    )
    
    muni = get_municipality_boundary()
    if muni is not None and len(muni) > 0:
        gpd.GeoSeries(muni.geometry.values).plot(
            ax=ax, facecolor='none', edgecolor='#2C3E50', 
            linewidth=2.5, linestyle='--'
        )
        ax.annotate(
            'Limite Municipal\nCrateús', 
            xy=(muni.geometry.iloc[0].centroid.x, muni.geometry.iloc[0].centroid.y),
            fontsize=9, ha='center', style='italic', color='#2C3E50',
            fontweight='bold'
        )
        print(f"  Limite municipal: OK")
    
    tracts = get_census_tracts()
    if tracts is not None and len(tracts) > 0:
        urban = tracts[tracts['zone'] == 'URBANO']
        rural = tracts[tracts['zone'] == 'RURAL']
        
        if len(urban) > 0:
            gpd.GeoSeries(urban.geometry.values).plot(
                ax=ax, facecolor='#FADBD8', edgecolor='#E74C3C', 
                linewidth=0.4, alpha=0.8
            )
        if len(rural) > 0:
            gpd.GeoSeries(rural.geometry.values).plot(
                ax=ax, facecolor='#D5F5E3', edgecolor='#27AE60', 
                linewidth=0.4, alpha=0.7
            )
        
        print(f"  Setores urbanos: {len(urban)}")
        print(f"  Setores rurais: {len(rural)}")
    
    neighborhoods = get_neighborhoods()
    if neighborhoods is not None and len(neighborhoods) > 0:
        gpd.GeoSeries(neighborhoods.geometry.values).plot(
            ax=ax, facecolor='none', edgecolor='#8E44AD', 
            linewidth=0.8, alpha=0.6
        )
        print(f"  Bairros: {len(neighborhoods)}")
    
    cidades = {
        'Tamboril': (-4.79, -40.82), 'Ipueiras': (-4.35, -40.71),
        'Novo Oriente': (-5.47, -40.74), 'Pereiro': (-5.96, -38.47),
        'Varjota': (-4.53, -40.47), 'Santa Quitéria': (-4.33, -40.15),
        'Cantuária': (-5.15, -39.90), 'Guaraci': (-4.82, -39.70)
    }
    for cidade, (lat, lon) in cidades.items():
        ax.plot(lon, lat, 'o', markersize=6, color='#2ECC71', 
               markeredgecolor='#27AE60', zorder=5)
        ax.annotate(cidade, xy=(lon, lat), xytext=(0.15, 0.15),
                   textcoords='offset points', fontsize=8,
                   arrowprops=dict(arrowstyle='->', color='#27AE60', lw=0.8))
    
    ax.set_title(
        "LOCALIZAÇÃO: IFCE CAMPUS CRATEÚS - SERTÃO CENTRAL DO CEARÁ\n"
        r"$\bf{Município\ de\ Crateús\ (IBGE:\ 2304103)\ -\ Setores\ Censitários\ (2010)}$",
        fontsize=14, fontweight='bold', pad=15
    )
    
    elements = [
        plt.Line2D([0], [0], marker='D', color='w', markerfacecolor='#C0392B',
                  markersize=12, markeredgecolor='darkred', 
                  markeredgewidth=2, label='IFCE Campus Crateús'),
        mpatches.Patch(color='#AED6F1', edgecolor='#5DADE2', 
                      label='Setores Censitários (2010)'),
        mpatches.Patch(color='none', edgecolor='#2C3E50', linestyle='--',
                      linewidth=2, label='Limite Municipal'),
        plt.Line2D([0], [0], marker='o', color='w', markerfacecolor='#2ECC71',
                  markersize=6, markeredgecolor='#27AE60', label='Municípios Vizinhos')
    ]
    add_legend(ax, elements, location='upper right', title='Legenda')
    
    add_scale_bar(ax, location='lower left')
    add_north_arrow(ax)
    
    add_source_footer(
        fig, 
        "Coordenadas: -5.7433, -40.4108 | Fonte: IBGE/GeoLB (2024)",
        "SIRGAS 2000 | EPSG:4674"
    )
    
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig(f'{OUTPUT_DIR}mapa_crateus_setores.png', dpi=300, 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("  [OK] mapa_crateus_setores.png")


def create_crateus_closeup():
    """Zoom máximo no campus IFCE Crateús."""
    print("\n[5/6] Gerando zoom do campus IFCE...")
    
    fig, ax = create_professional_figure(
        "CAMPUS IFCE CRATEÚS - VISTA AMPLIADA",
        xlim=(-40.45, -40.38),
        ylim=(-5.78, -5.72),
        size=(12, 10)
    )
    
    ax.plot(CRATEUS_LON, CRATEUS_LAT, 's', markersize=20, color='#E74C3C', 
           markeredgecolor='darkred', markeredgewidth=2, zorder=10)
    ax.annotate(
        'IFCE\nCampus\nCrateús',
        xy=(CRATEUS_LON, CRATEUS_LAT),
        xytext=(10, 10),
        textcoords='offset points',
        fontsize=12,
        fontweight='bold',
        ha='left',
        arrowprops=dict(arrowstyle='->', color='red', lw=2)
    )
    
    ax.set_title(
        "CAMPUS IFCE CRATEÚS - VISTA AMPLIADA\n"
        r"$\bf{Instituição\ Federal\ de\ Educação,\ Ciência\ e\ Tecnologia\ do\ Ceará}$",
        fontsize=14, fontweight='bold', pad=15
    )
    
    elements = [
        plt.Line2D([0], [0], marker='s', color='w', markerfacecolor='#E74C3C',
                  markersize=15, markeredgecolor='darkred', 
                  label='IFCE Campus Crateús')
    ]
    add_legend(ax, elements, location='upper left')
    
    add_scale_bar(ax)
    add_north_arrow(ax)
    
    add_source_footer(
        fig, 
        "Coordenadas geográficas: -5.7433, -40.4108 | Google Maps / OpenStreetMap",
        "SIRGAS 2000 | EPSG:4674"
    )
    
    plt.tight_layout(rect=[0, 0.04, 1, 1])
    plt.savefig(f'{OUTPUT_DIR}mapa_ifce_zoom.png', dpi=300, 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("  [OK] mapa_ifce_zoom.png")


def create_multi_panel_summary():
    """Painel múltiplo com todos os mapas."""
    print("\n[6/6] Gerando painel resumo...")
    
    fig, axes = plt.subplots(2, 2, figsize=(20, 16))
    fig.suptitle(
        "MAPAS CARTOGRÁFICOS - TESE DE DOUTORADO\n"
        r"$\bf{MCP\ e\ Educação\ no\ Sertão\ do\ Ceará:\ Uma\ Abordagem\ Computacional}$",
        fontsize=18, fontweight='bold', y=0.98
    )
    
    estados = get_ibge_states()
    nordeste = ['MA', 'PI', 'CE', 'RN', 'PB', 'PE', 'AL', 'SE', 'BA']
    
    ax1 = axes[0, 0]
    outras = estados[~estados['sigla'].isin(nordeste)]
    gpd.GeoSeries(outras.geometry.values).plot(ax=ax1, color='#D8D8D8', edgecolor='#AAA')
    ne = estados[estados['sigla'].isin(nordeste)]
    gpd.GeoSeries(ne.geometry.values).plot(ax=ax1, color='#FF6B35', edgecolor='#CC4400', linewidth=1)
    ax1.plot(-40.4108, -5.7433, 'D', markersize=6, color='red', markeredgecolor='darkred', zorder=10)
    ax1.set_xlim(-75, -30)
    ax1.set_ylim(-35, 6)
    ax1.set_title('A) Brasil: Nordeste em Destaque', fontsize=12, fontweight='bold')
    ax1.set_xlabel('Longitude')
    ax1.set_ylabel('Latitude')
    ax1.grid(True, linestyle=':', alpha=0.3)
    
    ax2 = axes[0, 1]
    cores = ['#E74C3C', '#F39C12', '#27AE60', '#3498DB', '#9B59B6', 
             '#1ABC9C', '#E91E63', '#00BCD4', '#FF5722']
    for i, (_, row) in enumerate(estados[estados['sigla'].isin(nordeste)].iterrows()):
        gpd.GeoSeries([row.geometry]).plot(ax=ax2, color=cores[i], edgecolor='black', linewidth=1)
        cent = row.geometry.centroid
        ax2.annotate(row['sigla'], xy=(cent.x, cent.y), fontsize=9, ha='center', va='center',
                    fontweight='bold', color='white')
    ax2.plot(-40.4108, -5.7433, 'D', markersize=8, color='red', markeredgecolor='darkred', zorder=10)
    ax2.set_xlim(-48, -32)
    ax2.set_ylim(-16, -1)
    ax2.set_title('B) Região Nordeste: 9 Estados', fontsize=12, fontweight='bold')
    ax2.set_xlabel('Longitude')
    ax2.grid(True, linestyle=':', alpha=0.3)
    
    ax3 = axes[1, 0]
    ceara = estados[estados['sigla'] == 'CE']
    gpd.GeoSeries(ceara.geometry.values).plot(ax=ax3, facecolor='#27AE60', edgecolor='#1E8449', linewidth=2)
    ax3.plot(-40.4108, -5.7433, 'D', markersize=10, color='red', markeredgecolor='darkred', zorder=10)
    ax3.annotate('IFCE Crateús', xy=(-40.4108, -5.7433), xytext=(-41.0, -4.8),
                fontsize=9, fontweight='bold', arrowprops=dict(arrowstyle='->', color='red'))
    ax3.set_xlim(-41.5, -37)
    ax3.set_ylim(-8, -2.5)
    ax3.set_title('C) Ceará: IFCE Campus Crateús', fontsize=12, fontweight='bold')
    ax3.set_xlabel('Longitude')
    ax3.set_ylabel('Latitude')
    ax3.grid(True, linestyle=':', alpha=0.3)
    
    ax4 = axes[1, 1]
    ax4.plot(CRATEUS_LON, CRATEUS_LAT, 'D', markersize=15, color='#C0392B', 
            markeredgecolor='darkred', markeredgewidth=2, zorder=10)
    ax4.annotate('IFCE Campus Crateús\n(-5.7433, -40.4108)', 
                xy=(CRATEUS_LON, CRATEUS_LAT), xytext=(-40.42, -5.75),
                fontsize=10, fontweight='bold', ha='center',
                arrowprops=dict(arrowstyle='->', color='#C0392B'))
    
    cidades = {
        'Tamboril': (-4.79, -40.82), 'Ipueiras': (-4.35, -40.71),
        'Novo Oriente': (-5.47, -40.74), 'Santa Quitéria': (-4.33, -40.15)
    }
    for cidade, (lat, lon) in cidades.items():
        ax4.plot(lon, lat, 'o', markersize=6, color='#2ECC71', markeredgecolor='#27AE60')
        ax4.annotate(cidade, xy=(lon, lat), fontsize=7)
    
    ax4.set_xlim(-41.2, -39.6)
    ax4.set_ylim(-6.3, -5.1)
    ax4.set_title('D) Crateús: Área Urbana e Entorno', fontsize=12, fontweight='bold')
    ax4.set_xlabel('Longitude')
    ax4.grid(True, linestyle=':', alpha=0.3)
    
    fig.text(0.15, 0.02, 
             "Fonte: IBGE Malhas Territoriais (2024) | Sistema: SIRGAS 2000 (EPSG:4674)\n"
             "Autor: Marcelo Claro Laranjeira | UFC Crateús | 2026",
             fontsize=9, style='italic', color='#555555')
    
    plt.tight_layout(rect=[0, 0.04, 1, 0.95])
    plt.savefig(f'{OUTPUT_DIR}painel_resumo_mapas.png', dpi=300, 
                bbox_inches='tight', facecolor='white')
    plt.close()
    print("  [OK] painel_resumo_mapas.png")


def main():
    """Executa geração de todos os mapas."""
    print("=" * 70)
    print("  MAPAS CARTOGRÁFICOS PROFISSIONAIS - PADRÃO IBGE")
    print("  Tese: MCP e Educação no Sertão do Ceará")
    print("  Sistema de Referência: SIRGAS 2000 (EPSG:4674)")
    print("=" * 70)
    
    create_brazil_map_with_inset()
    create_northeast_map()
    create_ceara_map()
    create_crateus_map_with_tracts()
    create_crateus_closeup()
    create_multi_panel_summary()
    
    print("\n" + "=" * 70)
    print("  ✓ TODOS OS MAPAS GERADOS COM SUCESSO!")
    print("=" * 70)
    print(f"\n  Localização: {OUTPUT_DIR}")
    print("\n  Arquivos gerados:")
    print("  - mapa_brasil_com_inset.png     (Brasil com encarte)")
    print("  - mapa_nordeste_estados.png    (9 estados do Nordeste)")
    print("  - mapa_ceara_crateus.png        (Ceará com IFCE)")
    print("  - mapa_crateus_setores.png      (Crateús + setores censitários)")
    print("  - mapa_ifce_zoom.png            (Zoom IFCE)")
    print("  - painel_resumo_mapas.png       (Painel 2x2)")
    print("=" * 70)


if __name__ == "__main__":
    main()
